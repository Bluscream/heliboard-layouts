# Emoji & Styled Font Layouts for HeliBoard

Custom keyboard layouts for [HeliBoard](https://github.com/HeliBorg/HeliBoard) that directly type decorative Unicode characters, regional indicator emoji flags, boxed/squared letters, circled letters, and mathematical typography from the [FontKeyboard](https://github.com/Bluscream/FontKeyboard) collection.

---

## Available Fonts

| Font | Example (A–E) | Digits (0–4) | Layout JSON | Restore Zip |
| :--- | :--- | :--- | :--- | :--- |
| **Emoji Regional** | 🇦 🇧 🇨 🇩 🇪 | 0️⃣ 1️⃣ 2️⃣ 3️⃣ 4️⃣ | [`layouts/emoji_regional.json`](layouts/emoji_regional.json) | [`emoji_regional.zip`](emoji_regional.zip) |
| **Boxed Black** | 🅰 🅱 🅲 🅳 🅴 | 0 1 2 3 4 | [`layouts/boxed_black.json`](layouts/boxed_black.json) | [`boxed_black.zip`](boxed_black.zip) |
| **Boxed** | 🄰 🄱 🄲 🄳 🄴 | 0 1 2 3 4 | [`layouts/boxed.json`](layouts/boxed.json) | [`boxed.zip`](boxed.zip) |
| **Circled Black** | 🅐 🅑 🅒 🅓 🅔 | 0 1 2 3 4 | [`layouts/circled_black.json`](layouts/circled_black.json) | [`circled_black.zip`](circled_black.zip) |
| **Circled** | Ⓐ Ⓑ Ⓒ Ⓓ Ⓔ | ⓪ ① ② ③ ④ | [`layouts/circled.json`](layouts/circled.json) | [`circled.zip`](circled.zip) |
| **Double Struck** | 𝔸 𝔹 ℂ 𝔻 𝔼 | 𝟘 𝟙 𝟚 𝟛 𝟜 | [`layouts/double_struck.json`](layouts/double_struck.json) | [`double_struck.zip`](double_struck.zip) |

All 6 layouts are also bundled in a single restore package: **[`EmojiFontsLayouts.zip`](EmojiFontsLayouts.zip)**.

---

## Features

- **Standard 3-Row Mobile Layout:** Perfectly integrates with HeliBoard's default functional keys (Shift, Delete, Space, Language Switch, Enter) without overflow.
- **Direct Styled Typing:** Tap any key to immediately produce the styled font character.
- **Styled Number Popups:** Long-pressing any key on the top row (`Q`–`P`) inputs the corresponding styled digit (`1`–`0`).
- **Shift Support:** For dual-case fonts like Double Struck (`𝕒` / `𝔸`), toggling Shift switches between uppercase and lowercase typography.

---

## How to Install in HeliBoard

### Option A: One-Click Restore Package (Easiest)

1. Download **[`EmojiFontsLayouts.zip`](EmojiFontsLayouts.zip)** (or any individual font `.zip`).
2. Open **HeliBoard Settings → Advanced → Backup and restore → Restore**.
3. Select the `.zip` file.
4. HeliBoard will restore all 6 custom layouts into your layouts collection.
5. Go to **Settings → Languages & Layouts**, pick your language subtype (e.g. English or German), tap **Layout**, and select your desired font layout!

### Option B: Individual JSON Layout Import

1. Copy the desired `.json` file from [`layouts/`](layouts/) to your device.
2. Open **HeliBoard Settings → Languages & Layouts**.
3. Select an existing language subtype (or tap **Add language**).
4. Tap **Layout** → **"+" (Custom)**.
5. Pick the layout JSON file using Android's file picker.
6. Switch layouts anytime using the spacebar swipe or language globe key!

---

> **Tip:** If you use the [Hacker's Keyboard Enhanced Layout](../hackerskeyboard/), these font styles are also available on **long-press of each respective letter** on the standard keyboard!
