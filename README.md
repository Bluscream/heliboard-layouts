# HeliBoard Layouts

A collection of custom layouts, themes, and configuration packages for [HeliBoard](https://github.com/HeliBorg/HeliBoard) (the customizable and privacy-conscious open-source Android keyboard).

For full features (such as transparent overlay mode, glowing bold text, and extra hardware keycodes), use the [patched HeliBoard build](https://github.com/Bluscream/HeliBoard/releases/tag/hk-overlay-1).

---

## Available Layouts

### ⌨️ [Hacker's Keyboard Layout](layouts/hackerskeyboard/)
Full 5-row German PC QWERTZ layout replicating [Hacker's Keyboard](https://github.com/klausw/hackerskeyboard) with dedicated arrow keys, Esc, Tab, Ctrl, Alt, ❖ (Meta), an Fn layer with F1–F12 & numpad, and the transparent neon theme.

Available in two versions:
- **`HackersKeyboardLayoutClassic`:** Exact 1:1 replica of Hacker's Keyboard keys and popups.
- **`HackersKeyboardLayoutEnhanced`:** Adds an emoji picker on long-press of `.` (`Win + .` convention), common text emotes (`qwq`, `twt`, `lol`, `rofl`, `uwu`, `:3`), and styled Unicode font characters (`🅰`, `🄰`, `🅐`, `Ⓐ`, `🇦`) on letter long-presses.

👉 [See Hacker's Keyboard layout details and downloads](layouts/hackerskeyboard/)

### 🔤 [Emoji & Styled Font Layouts](layouts/emojifonts/)
Direct typing layouts for styled Unicode typography, regional indicator flags (`🇦 🇧 🇨`), boxed/squared (`🅰 🅱 🅲` / `🄰 🄱 🄲`), circled (`🅐 🅑 🅒` / `Ⓐ Ⓑ Ⓒ`), and double-struck math letters (`𝔸 𝔹 ℂ` / `𝕒 𝕓 𝕔`).

Includes:
- Standalone 3-row layout JSON files with matching styled number popups.
- Ready-to-restore backup packages (`EmojiFontsLayouts.zip`).

👉 [See Emoji & Styled Font layouts and downloads](layouts/emojifonts/)

---

## Releases & Downloads

Pre-built restore zip files are available on the [Releases page](https://github.com/Bluscream/heliboard-layouts/releases/latest).

## Discussions & Community

Have ideas for new layouts, requests, or questions? Check out the [GitHub Discussions](https://github.com/Bluscream/heliboard-layouts/discussions)!

## Contributing

Want to contribute a layout?
1. Create a subdirectory under `layouts/<layout-name>/`.
2. Add your layout JSON files, a generator script (if applicable), screenshots in `images/`, and a `README.md` describing the layout and how to import it.
3. Submit a pull request!
