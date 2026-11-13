#!/usr/bin/env python3
"""Generate standalone Emoji / Font Keyboard layouts and restore packages for HeliBoard.

Generates 3-row mobile keyboard layouts with custom number popups on row 0 for:
- Regional Indicator Flags (🇦 🇧 🇨 ...)
- Boxed Black (Negative Squared: 🅰 🅱 🅲 ...)
- Boxed (Squared Latin: 🄰 🄱 🄲 ...)
- Circled Black (Negative Circled: 🅐 🅑 🅒 ...)
- Circled (Circled Latin & Digits: Ⓐ Ⓑ Ⓒ ... / ⓪ ① ② ...)
- Double Struck (Mathematical: 𝔸 𝔹 ℂ ... / 𝕒 𝕓 𝕔 ...)

Outputs into:
  layouts/emojifonts/layouts/<font_slug>.json
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAYOUTS = ROOT / "layouts"
FONTS_DATA = Path("/tmp/extracted_fonts.json")

QWERTY_ROWS = [
    list("qwertyuiop"),
    list("asdfghjkl"),
    list("zxcvbnm"),
]

# Standard row 0 key order maps to digits 1, 2, 3, 4, 5, 6, 7, 8, 9, 0
DIGITS_ROW0 = "1234567890"

FONTS_TO_BUILD = [
    ("Emoji Regional", "emoji_regional", "Emoji Regional (Flags)"),
    ("Boxed Black", "boxed_black", "Boxed Black (Negative Squared)"),
    ("Boxed", "boxed", "Boxed (Squared)"),
    ("Circled Black", "circled_black", "Circled Black"),
    ("Circled", "circled", "Circled"),
    ("Double Struck", "double_struck", "Double Struck"),
]


def b36(name: str) -> str:
    n = int.from_bytes(name.encode(), "big")
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    while n:
        n, r = divmod(n, 36)
        out = digits[r] + out
    return out


def make_layout(font_name: str, font_data: dict) -> list:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    u_map = {c: font_data["upper"][i].strip() for i, c in enumerate(alphabet) if i < len(font_data["upper"])}
    l_map = {c: font_data["lower"][i].strip() for i, c in enumerate(alphabet) if i < len(font_data["lower"])}
    # Note: font_data["numbers"] is ordered 0..9 (index 0 is '0', index 1 is '1', etc.)
    num_map = {str(i): font_data["numbers"][i].strip() for i in range(10) if i < len(font_data.get("numbers", []))}

    # Row 0: QWERTYUIOP with matching number popups (q->1, w->2, ..., o->9, p->0)
    row0 = []
    for i, char in enumerate(QWERTY_ROWS[0]):
        unsh = l_map.get(char, char)
        sh = u_map.get(char, char.upper())
        digit = DIGITS_ROW0[i]
        mapped_num = num_map.get(digit, digit)
        pop = {"main": {"label": mapped_num}}

        if unsh == sh:
            row0.append({"label": unsh, "popup": pop})
        else:
            row0.append({
                "$": "shift_state_selector",
                "default": {"label": unsh, "popup": pop},
                "manualOrLocked": {"label": sh, "popup": pop}
            })

    # Row 1: ASDFGHJKL
    row1 = []
    for char in QWERTY_ROWS[1]:
        unsh = l_map.get(char, char)
        sh = u_map.get(char, char.upper())
        if unsh == sh:
            row1.append({"label": unsh})
        else:
            row1.append({
                "$": "shift_state_selector",
                "default": {"label": unsh},
                "manualOrLocked": {"label": sh}
            })

    # Row 2: ZXCVBNM
    row2 = []
    for char in QWERTY_ROWS[2]:
        unsh = l_map.get(char, char)
        sh = u_map.get(char, char.upper())
        if unsh == sh:
            row2.append({"label": unsh})
        else:
            row2.append({
                "$": "shift_state_selector",
                "default": {"label": unsh},
                "manualOrLocked": {"label": sh}
            })

    return [row0, row1, row2]


def main():
    fonts = json.load(open(FONTS_DATA))
    LAYOUTS.mkdir(parents=True, exist_ok=True)

    for font_key, slug, display_name in FONTS_TO_BUILD:
        if font_key not in fonts:
            print("Skipping missing font:", font_key)
            continue
        data = fonts[font_key]
        layout = make_layout(font_key, data)
        out_file = LAYOUTS / f"{slug}.json"
        out_file.write_text(json.dumps(layout, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"Wrote layout: {out_file}")

    print("All emoji font layouts generated successfully.")


if __name__ == "__main__":
    main()
