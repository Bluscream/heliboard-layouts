#!/usr/bin/env python3
"""Build HeliBoard settings backup packages for Emoji / Font Keyboard layouts.

Builds:
  EmojiFontsLayouts.zip: All 6 font layouts bundled for one-click restore.
  Individual packages: <FontSlug>.zip for each font.

Users can restore these in HeliBoard via:
  Settings -> Advanced -> Backup and restore -> Restore
"""
from __future__ import annotations

import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAYOUTS = ROOT / "layouts"

FONTS_TO_BUILD = [
    ("Emoji Regional", "emoji_regional", "Emoji Regional"),
    ("Boxed Black", "boxed_black", "Boxed Black"),
    ("Boxed", "boxed", "Boxed"),
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


def main() -> None:
    # 1. Build master bundle containing all font layouts
    all_zip_path = ROOT / "EmojiFontsLayouts.zip"
    with zipfile.ZipFile(all_zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for font_key, slug, display_name in FONTS_TO_BUILD:
            src = LAYOUTS / f"{slug}.json"
            if not src.exists():
                print(f"Warning: {src} missing, skipping.")
                continue
            main_id = f"custom.Latn.{b36(display_name)}."
            dest_in_zip = f"unprotected/layouts/main/{main_id}json"
            z.write(src, dest_in_zip)
    print("Wrote master bundle:", all_zip_path)

    # 2. Build individual font layout restore zips
    for font_key, slug, display_name in FONTS_TO_BUILD:
        src = LAYOUTS / f"{slug}.json"
        if not src.exists():
            continue
        indiv_zip = ROOT / f"{slug}.zip"
        main_id = f"custom.Latn.{b36(display_name)}."
        with zipfile.ZipFile(indiv_zip, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(src, f"unprotected/layouts/main/{main_id}json")
        print("Wrote individual bundle:", indiv_zip)


if __name__ == "__main__":
    main()
