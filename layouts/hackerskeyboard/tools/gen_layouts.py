#!/usr/bin/env python3
"""Generate HeliBoard layout JSON files replicating Hacker's Keyboard (German, Full 5-row).

Source of truth: hackerskeyboard res/xml-de/kbd_full.xml, res/xml/kbd_full_fn.xml and
res/values-de/donottranslate-keymap.xml (key_*_main / _shift / _alt strings).

Outputs into ../heliboard-config/layouts/:
  hk_de_main_classic.json    classic main layout (exact Hacker's Keyboard keys/popups)
  hk_de_main_enhanced.json   enhanced main layout (with emoji on period and common emotes on letters)
  hk_de_main.json            default (same as enhanced)
  hk_functional.json         functional keys for all 5 rows (Tab/Ctrl/Shift/Esc/Alt/Meta/Fn/arrows)
  hk_fn_layer.json           Fn layer (used as NUMPAD / NUMPAD_LANDSCAPE layout), stock HeliBoard
  hk_fn_layer_patched.json   same, with Del/SysRq/ScrollLock/Break/NumLock/D-pad-centre codes that
                             need the hk-keycodes patch
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "layouts"

# HeliBoard key codes (app/.../keyboard_parser/floris/KeyCode.kt)
CTRL_LEFT, ALT_LEFT, META_LEFT = -10044, -10046, -10048
ESCAPE, TAB, INSERT = -10017, -10014, -10018
ARROW_LEFT, ARROW_RIGHT, ARROW_UP, ARROW_DOWN = -21, -22, -23, -24
HOME, END = -27, -28  # MOVE_START_OF_LINE / MOVE_END_OF_LINE -> KEYCODE_MOVE_HOME / _END
PAGE_UP, PAGE_DOWN = -10010, -10011
NUMPAD, ALPHA, SETTINGS, VOICE = -205, -201, -301, -233
F_KEYS = [-10028 - i for i in range(12)]  # F1..F12
UNSPECIFIED = 0  # key is shown, press does nothing (stock HeliBoard has no such key code)
# only with patches/0001-hk-keycodes.patch
FORWARD_DELETE, DPAD_CENTER, SYSRQ, SCROLL_LOCK, BREAK, NUM_LOCK = -9, -10055, -10056, -10057, -10058, -10059

U = 1 / 14  # one Hacker's Keyboard column (7.142857%p)

NUMBER_ROW = [
    ("^", "°", "^°"), ("1", "!", "1!¹¡½⅓¼⅛"), ("2", '"', '2"²⅛⅔'), ("3", "§", "3§³£¾⅜"),
    ("4", "$", "4$¼¤⁴¢¥"), ("5", "%", "5%½⅜‰"), ("6", "&", "6&¬⅝"), ("7", "/", "7/{⅞♪√"),
    ("8", "(", "8([™∞"), ("9", ")", "9)]±"), ("0", "=", "0=}°ⁿ≈≠"), ("ß", "?", "ß?\¿"),
    ("\x27", "`", "\x27`‚’‘„”“"),
]
ROW_Q = [
    ("q", None, "1@"), ("w", None, "2"), ("e", None, "3€éèêë"), ("r", None, "4"), ("t", None, "5"),
    ("z", None, "6ž"), ("u", None, "7üúùûū"), ("i", None, "8íìîïī"), ("o", None, "9öóòôõōø"),
    ("p", None, "0π₱"), ("ü", None, ""), ("+", "*", "+*~•★±"), ("#", "'", "#'†‡"),
]
ROW_A = [
    ("a", None, "äáàâãåāæ"), ("s", None, "§ßš"), ("d", None, "đ"), ("f", None, "₣"), ("g", None, ""),
    ("h", None, ""), ("j", None, ""), ("k", None, ""), ("l", None, "£₤λ"), ("ö", None, "♦♥♠♣"),
    ("ä", None, "↑↓←→"),
]
ROW_Y = [
    ("<", ">", "<>|≤«‹≥»›"), ("y", None, "ýÿ¥"), ("x", None, ""), ("c", None, "çčć¢"), ("v", None, ""),
    ("b", None, ""), ("n", None, "ñ"), ("m", None, "μ"), (",", ";", ",;·×"), (".", ":", ".:…÷"),
    ("-", "_", "-_–—"),
]

EMOTES = {
    "q": ["q.q", "qwq"],
    "Q": ["Q.Q", "QwQ"],
    "w": ["owo", "^w^"],
    "W": ["OwO", "^W^"],
    "e": ["^^", "xd"],
    "E": ["^^", "XD"],
    "r": ["rofl"],
    "R": ["ROFL"],
    "t": ["t.t", "twt"],
    "T": ["T.T", "TwT"],
    "y": ["yay"],
    "Y": ["YAY"],
    "u": ["uwu"],
    "U": ["UwU"],
    "i": ["^-^"],
    "I": ["^-^"],
    "o": ["o.o", "owo"],
    "O": ["O.O", "OwO"],
    "p": [":p", ";p"],
    "P": [":P", ";P"],
    "a": ["(^-^)/"],
    "A": ["(^-^)/"],
    "s": ["(._.)/"],
    "S": ["(._.)/"],
    "d": [":d", "xd"],
    "D": [":D", "XD"],
    "f": ["orz"],
    "F": ["ORZ"],
    "g": ["gg", "gj"],
    "G": ["GG", "GJ"],
    "h": ["(^o^)/"],
    "H": ["(^O^)/"],
    "j": ["jk"],
    "J": ["JK"],
    "k": ["k"],
    "K": ["K"],
    "l": ["lol", "lmao", "lmfao"],
    "L": ["LOL", "LMAO", "LMFAO"],
    "x": ["xd", "xp"],
    "X": ["XD", "XP"],
    "c": [":3"],
    "C": [":3"],
    "v": ["v.v"],
    "V": ["V.V"],
    "b": ["brb"],
    "B": ["BRB"],
    "n": ["n_n", "np"],
    "N": ["N_N", "NP"],
    "m": ["m(_ _)m"],
    "M": ["M(_ _)M"],
}

_ESCAPE = {"@", "#", "%", "|", "\\"}


def esc(ch: str) -> str:
    return "".join(chr(92) + c if c in _ESCAPE else c for c in ch)


def popup(items: list[str]) -> dict:
    return {"relevant": [{"label": esc(c)} for c in items]}


def char_key(main: str, shift: str | None, alt: str, width: float = U, enhanced: bool = False) -> dict:
    alts = [c for c in alt if c != main and c != shift and not (c.isdigit() and not main.isdigit())]
    seen: set[str] = set()
    alts = [c for c in alts if not (c in seen or seen.add(c))]

    if shift is None:
        key: dict = {"label": esc(main), "width": width}
        pop_items = list(alts)
        if enhanced:
            if main in EMOTES:
                pop_items.extend(EMOTES[main])
            upper = main.upper()
            if upper != main and upper in EMOTES:
                upper_pop = list(alts) + EMOTES[upper]
                shifted_key = {"label": esc(upper), "width": width}
                if upper_pop:
                    shifted_key["popup"] = popup(upper_pop)
                if pop_items:
                    key["popup"] = popup(pop_items)
                return {"$": "shift_state_selector", "manualOrLocked": shifted_key, "default": key}
        if pop_items:
            key["popup"] = popup(pop_items)
        return key

    unshifted_pop = [shift, *alts]
    shifted_pop = [main, *alts]
    if enhanced and main == ".":
        unshifted_pop.insert(1, "emoji")
        shifted_pop.insert(1, "emoji")

    unshifted = {"label": esc(main), "width": width, "popup": popup(unshifted_pop)}
    shifted = {"label": esc(shift), "width": width, "popup": popup(shifted_pop)}
    return {"$": "shift_state_selector", "manualOrLocked": shifted, "default": unshifted}


def main_layout(enhanced: bool = False) -> list:
    row1 = [char_key(*NUMBER_ROW[0], width=0.0457142855, enhanced=enhanced), *(char_key(*k, enhanced=enhanced) for k in NUMBER_ROW[1:])]
    return [
        row1,
        [char_key(*k, enhanced=enhanced) for k in ROW_Q],
        [char_key(*k, enhanced=enhanced) for k in ROW_A],
        [char_key(*k, enhanced=enhanced) for k in ROW_Y]
    ]


PRESERVE_CASE = 65536
NO_HINT = 1073741824


def fk(label: str, code: int, width: float = U, **extra) -> dict:
    return {"label": label, "code": code, "width": width, "type": "function", "labelFlags": PRESERVE_CASE, **extra}


def bottom_row(patched: bool, fn_code: int) -> list:
    return [
        fk("Esc", ESCAPE, 1.5 * U),
        {"label": "settings", "width": U, "type": "function", "popup": {"relevant": [{"label": "voice"}]}},
        fk("Alt", ALT_LEFT),
        fk("❖", META_LEFT),
        {"label": "space", "width": 4.5 * U},
        fk("Fn", fn_code),
        fk("○", DPAD_CENTER if patched else UNSPECIFIED),
        fk("◁", ARROW_LEFT),
        fk("▽", ARROW_DOWN),
        fk("▷", ARROW_RIGHT),
    ]


TAB_KEY = {"label": "tab", "width": U, "popup": {"relevant": [{"label": "settings"}]}}
PLACEHOLDER = {"type": "placeholder"}


def functional_layout() -> list:
    return [
        [PLACEHOLDER, {"label": "delete", "width": 0.0971428550}],
        [TAB_KEY, PLACEHOLDER],
        [fk("Ctrl", CTRL_LEFT, 1.5 * U), PLACEHOLDER, {"label": "action", "width": 1.5 * U, "labelFlags": NO_HINT}],
        [{"label": "shift", "width": U}, PLACEHOLDER, fk("△", ARROW_UP), {"label": "shift", "width": U}],
        bottom_row(patched=False, fn_code=NUMPAD),
    ]


def fn_layer(patched: bool) -> list:
    w = 0.08035714
    nop = UNSPECIFIED

    def n(label: str) -> dict:
        return {"label": esc(label), "width": w}

    def fkey(i: int) -> dict:
        return fk(f"F{i + 1}", F_KEYS[i], w)

    return [
        [{"label": "voice", "width": 1.5 * U, "type": "function"}, *(fkey(i) for i in range(4)),
         n("7"), n("8"), n("9"), n("/"), fk("Home", HOME, 1.5 * U), {"label": "delete", "width": 2 * U}],
        [TAB_KEY | {"width": 1.5 * U}, *(fkey(i) for i in range(4, 8)),
         n("4"), n("5"), n("6"), n("*"), fk("End", END, 1.5 * U), fk("Ins", INSERT),
         fk("Del", FORWARD_DELETE if patched else nop)],
        [fk("Ctrl", CTRL_LEFT, 1.5 * U), *(fkey(i) for i in range(8, 12)),
         n("1"), n("2"), n("3"), n("-"), fk("PgUp", PAGE_UP, 1.5 * U), {"label": "action", "width": 2 * U, "labelFlags": NO_HINT}],
        [{"label": "shift", "width": 1.5 * U},
         fk("SyRq", SYSRQ if patched else nop, w), fk("ScrL", SCROLL_LOCK if patched else nop, w),
         fk("Brk", BREAK if patched else nop, w), fk("NumL", NUM_LOCK if patched else nop, w),
         n("0"), n(","), n("."), n("+"), fk("PgDn", PAGE_DOWN, 1.5 * U), fk("△", ARROW_UP),
         {"label": "shift", "width": U}],
        bottom_row(patched, fn_code=ALPHA),
    ]


def patched_functional() -> list:
    rows = functional_layout()
    rows[-1] = bottom_row(patched=True, fn_code=NUMPAD)
    return rows


def write(name: str, data: list) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=1) + chr(10), encoding="utf-8")

if __name__ == "__main__":
    write("hk_de_main_classic.json", main_layout(enhanced=False))
    write("hk_de_main_enhanced.json", main_layout(enhanced=True))
    write("hk_de_main.json", main_layout(enhanced=True))
    write("hk_functional.json", functional_layout())
    write("hk_functional_patched.json", patched_functional())
    write("hk_fn_layer.json", fn_layer(patched=False))
    write("hk_fn_layer_patched.json", fn_layer(patched=True))
    print("written to", OUT)
