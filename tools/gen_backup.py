#!/usr/bin/env python3
"""Build HeliBoard settings backups (Settings > Advanced > Backup and restore > Restore) that set up
the Hacker's Keyboard look-alike: custom layouts, transparent colour theme, hint/popup options.

Also writes the equivalent SharedPreferences XML + file tree, used to provision Waydroid directly.

Usage: gen_backup.py [--height-landscape F] [--height-portrait F]
Outputs (heliboard-config/):
  heliboard-hk-backup-stock.zip    for the stock HeliBoard release
  heliboard-hk-backup-patched.zip  for the patched build (glow, overlay, extra key codes)
  provision/<variant>/...          shared_prefs XML + files/ tree (test provisioning only)
"""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
from xml.sax.saxutils import quoteattr

ROOT = Path(__file__).resolve().parent.parent
CFG = ROOT / "heliboard-config"
LAYOUTS = CFG / "layouts"
THEME = "HK Transparent"
VERSION_CODE = 4300  # HeliBoard 4.3-beta1; avoids re-running upgrade migrations on restore


def b36(name: str) -> str:
    n = int.from_bytes(name.encode(), "big")  # == BigInteger(bytes).toString(36) for positive values
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    while n:
        n, r = divmod(n, 36)
        out = digits[r] + out
    return out


MAIN_NAME = f"custom.Latn.{b36('HK Deutsch')}."
FUNC_NAME = f"custom.{b36('HK functional')}."
FN_NAME = f"custom.{b36('HK Fn layer')}."


def argb(hex_str: str) -> int:
    v = int(hex_str, 16)
    return v - (1 << 32) if v >= 1 << 31 else v


COLORS = {  # ColorType -> #AARRGGBB, after Hacker's Keyboard res/layout/input_trans_neon.xml
    "MAIN_BACKGROUND": "D8000000",  # android:background="#c0000000"
    "KEY_BACKGROUND": "0AFFFFFF",  # btn_keyboard_key_ics drawn with backgroundAlpha 32
    "FUNCTIONAL_KEY_BACKGROUND": "0AFFFFFF",
    "SPACE_BAR_BACKGROUND": "0AFFFFFF",
    "ACTION_KEY_BACKGROUND": "0AFFFFFF",
    "ACTION_KEY_POPUP_KEYS_BACKGROUND": "F0202020",
    "KEY_TEXT": "FFFFFFFF",  # keyTextColor
    "FUNCTIONAL_KEY_TEXT": "FFFFFFFF",
    "KEY_ICON": "FFFFFFFF",
    "SHIFT_KEY_ICON": "FFFFFFFF",
    "ACTION_KEY_ICON": "FFFFFFFF",
    "KEY_HINT_TEXT": "FFDDDDDD",
    "SPACE_BAR_TEXT": "FFFFFFFF",
    "KEY_PREVIEW_BACKGROUND": "F0202020",
    "KEY_PREVIEW_TEXT": "FFFFFFFF",
    "POPUP_KEYS_BACKGROUND": "F0202020",
    "POPUP_KEY_TEXT": "FFFFFFFF",
    "POPUP_KEY_ICON": "FFFFFFFF",
    "STRIP_BACKGROUND": "C0000000",
    "NAVIGATION_BAR": "FF000000",
    "GESTURE_TRAIL": "FF33B5E5",
    "GESTURE_PREVIEW": "F0202020",
    "TOOL_BAR_KEY": "FFFFFFFF",
    "TOOL_BAR_EXPAND_KEY": "FFFFFFFF",
    "SUGGESTED_WORD": "FFFFFFFF",
    "SUGGESTION_TYPED_WORD": "FFFFFFFF",
    "SUGGESTION_VALID_WORD": "FFFFFFFF",
    "SUGGESTION_AUTO_CORRECT": "FF33B5E5",
    "MORE_SUGGESTIONS_BACKGROUND": "F0202020",
}


def prefs(patched: bool, h_land: float, h_port: float, font: float) -> dict[str, dict]:
    subtype = "de§" + ",".join(sorted([
        "AsciiCapable", "EmojiCapable", "SupportTouchPositionCorrection", "isAdditionalSubtype",
        f"KeyboardLayoutSet=MAIN:{MAIN_NAME}",
    ]))
    strings = {
        "theme_style": "Material",
        "icon_style": "Material",
        "theme_colors": THEME,
        "theme_colors_night": THEME,
        f"user_all_colors_{THEME}": ";".join(f"{k},{argb(v)}" for k, v in COLORS.items()),
        f"user_colors_{THEME}": "[]",
        "additional_subtypes": subtype,
        "enabled_subtypes": subtype,
        "selected_subtype": subtype,
        "layout_FUNCTIONAL": FUNC_NAME,
        "layout_NUMPAD": FN_NAME,
        "layout_NUMPAD_LANDSCAPE": FN_NAME,
        "popup_keys_order": "layout:true|language_priority:true|language:true|number:false|symbols:false",
        "popup_keys_labels_order": "layout:true|language_priority:false|language:false|number:false|symbols:false",
        "toolbar_mode": "HIDDEN",
    }
    booleans = {
        "theme_auto_day_night": False,
        "theme_key_borders": True,
        "show_hints": True,
        "show_number_row": False,
        "show_popup_hints": False,
        "popup_on": False,  # HK: popup_on=false (no key press preview)
        "auto_cap": True,
        "auto_correction": False,
        "show_suggestions": False,
        "gesture_input": False,
        "show_emoji_key": False,
        "show_language_switch_key": False,
        "abc_after_numpad_space": False,
        "vibrate_on": True,
        "sound_on": True,
        "navbar_color": True,
    }
    ints = {"version_code": VERSION_CODE, f"user_more_colors_{THEME}": 2}
    floats = {
        "keyboard_height_scale_true_false": h_land,
        "keyboard_height_scale_false_false": h_port,
        "bottom_padding_scale_true_false": 0.0,
        "bottom_padding_scale_false_false": 0.0,
        "font_scale": font,
        "hint_font_scale": 1.35,
    }
    if patched:
        booleans["overlay_keyboard"] = True
        booleans["key_text_bold"] = True
        ints["key_text_glow_radius_dp"] = 8
        ints["key_text_glow_color"] = argb("FF33B5E5")
    return {"boolean": booleans, "int": ints, "float": floats, "string": strings}


def layout_files(patched: bool) -> dict[str, Path]:
    sfx = "_patched" if patched else ""
    fn = LAYOUTS / f"hk_fn_layer{sfx}.json"
    return {
        f"layouts/main/{MAIN_NAME}json": LAYOUTS / "hk_de_main.json",
        f"layouts/functional/{FUNC_NAME}json": LAYOUTS / f"hk_functional{sfx}.json",
        f"layouts/numpad/{FN_NAME}json": fn,
        f"layouts/numpad_landscape/{FN_NAME}json": fn,
    }


def prefs_json(p: dict[str, dict]) -> str:
    def d(x: dict) -> str:
        return json.dumps(x, ensure_ascii=False, separators=(",", ":"))
    return "\n".join([
        "boolean settings", d(p["boolean"]), "int settings", d(p["int"]), "long settings", d({}),
        "float settings", d(p["float"]), "string settings", d(p["string"]), "string set settings", d({}),
    ])


def prefs_xml(p: dict[str, dict]) -> str:
    lines = ["<?xml version='1.0' encoding='utf-8' standalone='yes' ?>", "<map>"]
    for k, v in p["boolean"].items():
        lines.append(f"    <boolean name={quoteattr(k)} value=\"{str(v).lower()}\" />")
    for k, v in p["int"].items():
        lines.append(f"    <int name={quoteattr(k)} value=\"{v}\" />")
    for k, v in p["float"].items():
        lines.append(f"    <float name={quoteattr(k)} value=\"{v}\" />")
    for k, v in p["string"].items():
        esc = v.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        lines.append(f"    <string name={quoteattr(k)}>{esc}</string>")
    lines.append("</map>")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--height-landscape", type=float, default=1.0)
    ap.add_argument("--height-portrait", type=float, default=1.0)
    ap.add_argument("--font-scale", type=float, default=1.0)
    a = ap.parse_args()
    for patched in (False, True):
        variant = "patched" if patched else "stock"
        p = prefs(patched, a.height_landscape, a.height_portrait, a.font_scale)
        files = layout_files(patched)
        zpath = CFG / f"heliboard-hk-backup-{variant}.zip"
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            for name, src in files.items():
                # device-protected files are stored under "unprotected/" (BackupRestorePreference.kt)
                z.write(src, "unprotected/" + name)
            z.writestr("preferences.json", prefs_json(p))
        prov = CFG / "provision" / variant
        for name, src in files.items():
            dst = prov / "files" / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(src.read_bytes())
        (prov / "shared_prefs").mkdir(parents=True, exist_ok=True)
        (prov / "shared_prefs" / "helium314.keyboard.debug_preferences.xml").write_text(prefs_xml(p), encoding="utf-8")
        print("wrote", zpath)


if __name__ == "__main__":
    main()
