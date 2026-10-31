#!/usr/bin/env python3
"""Draws every file under assets/logo from the pixel grids below.

Every cell colour resolves through tokens/tokens.json. `python3 scripts/logo.py`
writes the SVGs and their PNG exports; `--check` fails when a file on disk differs
from what the grids draw, or when assets/logo holds a file they do not draw.
"""

import argparse
import json
import math
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "assets" / "logo"

CELL_TOKENS = {
    "k": ("color", "ink"),
    "P": ("color", "ink"),
    "s": ("color", "ink-soft"),
    "t": ("color", "text-muted"),
    "T": ("color", "text-faint"),
    "Y": ("color", "lemon"),
    "B": ("color", "lemon-bright"),
    "f": ("color", "fiber"),
    "F": ("color", "fiber-deep"),
    "a": ("color", "fiber-light"),
    "g": ("color", "leaf"),
    "p": ("color", "paper"),
    "c": ("color", "canvas"),
    "n": ("color", "line"),
    "K": ("theme", "ink", "canvas"),
    "L": ("theme", "ink", "line-soft"),
    "l": ("theme", "ink", "line"),
    "u": ("theme", "ink", "text-faint"),
    "U": ("theme", "ink", "text-muted"),
}


def load_palette():
    tokens = json.loads((ROOT / "tokens" / "tokens.json").read_text())
    palette = {}
    for cell, path in CELL_TOKENS.items():
        node = tokens
        for key in path:
            node = node[key]
        palette[cell] = node.upper()
    return palette


PALETTE = load_palette()

LEMON_HERO = """
..................................kkkk..........
................................kkggggk.........
..............................kkgggggggk........
.............................kgggggggggk........
............................kgggggggggk.........
...........................kggggggggkk..........
........................kk.kgggggggk............
.......................kFFkgggggkkk.............
.......................kFFkgkkkk................
.......................kFFkk....................
...................kkkkkFFkkk...................
...............kkkkBBBBYYYYYYkkkk...............
.............kkBBBBYYYYYYYYYYYYYYkk.............
............kBBYYYYYYYYYYYYYYYYYYYYk............
..........kkBYYYYYYYYYYYYYYYYYYYYYYYkk..........
.........kBBYppYYYYYYYYYYYYYYYYBYYYYYYk.........
........kBYYppYYYYYYYPYYYYYYYYYYYYYYYYYk........
.......kBYYYYYYYYYYYYPPYYYYYYYYYYYYYYYYYk.......
.......kBYYYYYYYYYYYYPPPYYYYYYYYYYYYBYYYk.......
......kBYYYYYYYYYYYYYPPPPYYYYYYYYYYYYYYYYk......
......kBYYYYYYYBYYYYYPPPPPYYYYYYYYYYYYYYYk......
.....kBYYYYYYYYYYYYYYPPPPPPYYYYYYYYYYYYYYYk.....
.....kBYYYYYYYYYYYYYYPPPPPPPYYYYYYYYYYYYYYk.....
....kBYYYYBYYYYYYYYYYPPPPPPPPYYYYYBYYYYYYYYk....
...kYYYYYYYYYYYYYYYYYPPPPPPPPPYYYYYYYYBYYYYYk...
....kBYYYYYYYYYYYYYYYPPPPPPPPYYYYYYYYYYYYYYk....
.....kBYYYYYYYYYYYYYYPPPPPPPYYYYYYYYYYYYYak.....
.....kBYYYYYYYYYYYYYYPPPPPPYYYYYYYYYYYYYYak.....
......kYYYYYYBYYYYYYYPPPPPYYYYYYYYYYYYYYak......
......kYYYYYYYYYYYYYYPPPPYYYYYYYYYYYYYYYak......
.......kYYYYYYYYYYYYYPPPYYYYYYYYYYYYYYYak.......
.......kYYYYYYYYYYYYYPPYYYYYYYYYYYYYYYYak.......
........kYYYYYYYYBYYYPYYYYYYYYYYYYYYYYak........
.........kYYYYYYYYYYYYYYYYYYYYYYYYYYaak.........
..........kkYYYYYYYYYYYYYYYYYYYYYYYakk..........
............kYYYYYYYYYYYYYYYYYYYYaak............
.............kkYYYYYYYYYYYYYYaaaakk.............
...............kkkkYYYYYYaaaakkkk...............
...................kkkkkkkkkk...................
................................................
"""

LEMON_ICON = """
................................
................................
................................
................................
........................kkk.....
......................kkggk.....
....................kkggggk.....
...................kgggggk......
..................kgggggk.......
..................kgggkk........
................kFFkkk..........
............kkkkkFFk............
.........kkkBBBYYYYYkkk.........
.......kkBBBYYYYYYYYYYYkk.......
......kBBYYYYYPYYYYYYYYYYk......
.....kBYYppYYYPPYYYYYYYYYYk.....
....kBYYppYYYYPPPYYYYYYYYYYk....
....kBYYYYYYYYPPPPYYYYYYYYYk....
...kBYYYYYYYYYPPPPPYYYYYYYYYk...
..kBYYYYYYYYYYPPPPPPYYYYYYYYYk..
..kBYYYYYYYYYYPPPPPPYYYYYYYYYk..
...kBYYYYYYYYYPPPPPYYYYYYYYak...
....kYYYYYYYYYPPPPYYYYYYYYak....
....kYYYYYYYYYPPPYYYYYYYYYak....
.....kYYYYYYYYPPYYYYYYYYYak.....
......kYYYYYYYPYYYYYYYYaak......
.......kkYYYYYYYYYYYaaakk.......
.........kkkYYYYaaaakkk.........
............kkkkkkkk............
................................
................................
................................
"""

LEMON_ICON16 = """
..pppppppppkkk..
.ppppppppkkggkp.
ppppppppkgggkppp
pppppppkFkkkpppp
pppppkkkkkkppppp
pppkkBBYYYYkkppp
ppkBpYPYYYYYYkpp
ppkBYYPPYYYYYkpp
ppkBYYPPPYYYYkpp
pkBYYYPPPPYYYYkp
ppkYYYPPPYYYakpp
ppkYYYPPYYYYakpp
ppkYYYPYYYYaakpp
pppkkYYYaaakkppp
.ppppkkkkkkpppp.
..pppppppppppp..
"""

LEMON_SMALL = """
.............kk.
...........kkgk.
..........kgggk.
.........kgggk..
.....kkkkkkkk...
...kkBBYYYYkk...
..kBBYPYYYYYYk..
.kBpYYPPYYYYYYk.
.kYYYYPPPYYYYYk.
kYYYYYPPPPYYYYYk
.kYYYYPPPYYYYYk.
.kYYYYPPYYYYYak.
..kYYYPYYYYaak..
...kkYYYYaakk...
.....kkkkkk.....
................
"""

LEMON_MONO = """
................................
.........................kkk....
.......................kkkkk....
.....................kkkkkkk....
....................kkkkkkk.....
...................kkkkkkk......
...................kkkkk........
...................kk...........
.................kk.............
.................kk.............
............kkkkkkkk............
.........kkkkkkkkkkkkkk.........
.......kkkkkk.kkkkkkkkkkk.......
......kkkkkkk..kkkkkkkkkkk......
.....kkkkkkkk...kkkkkkkkkkk.....
....kkkkkkkkk....kkkkkkkkkkk....
....kkkkkkkkk.....kkkkkkkkkk....
...kkkkkkkkkk......kkkkkkkkkk...
..kkkkkkkkkkk.......kkkkkkkkkk..
..kkkkkkkkkkk.......kkkkkkkkkk..
...kkkkkkkkkk......kkkkkkkkkk...
....kkkkkkkkk.....kkkkkkkkkk....
....kkkkkkkkk....kkkkkkkkkkk....
.....kkkkkkkk...kkkkkkkkkkk.....
......kkkkkkk..kkkkkkkkkkk......
.......kkkkkk.kkkkkkkkkkk.......
.........kkkkkkkkkkkkkk.........
............kkkkkkkk............
................................
................................
................................
................................
"""

LEMON_TRAY = """
............kkk.
..........kkkkk.
.........kkkkk..
........kkk.....
........k.......
.....kkkkkk.....
...kkkkkkkkkk...
..kkkk.kkkkkkk..
.kkkkk..kkkkkkk.
.kkkkk...kkkkkk.
kkkkkk....kkkkkk
.kkkkk...kkkkkk.
.kkkkk..kkkkkkk.
..kkkk.kkkkkkk..
...kkkkkkkkkk...
.....kkkkkk.....
"""

LAMP_SHADE = """
...kkkkkkkk...
...kBBBBBBak..
..kBBpBBBBak..
..kBppBBBBBak.
.kBBpBBBBBBak.
.kBBBBBBBBBBak
kaaaaaaaaaaaak
kkkkkkkkkkkkkk
"""

LAMP_FOOT = """
..kkkkkkkk..
.kuuuTTTTTk.
kTTTTTTTTtTk
"""

POPCORN = """
....kkk..kkk....
...kpppk.kpBpk..
..kppcpkkpppcpk.
.kpBpppcpcppBpk.
kppcpBpppppcpppk
kpppppcppBpppcpk
kkkkkkkkkkkkkkkk
.kfpfpfpfpfpfpk.
.kfpfpfpfpfpfpk.
.kfpfpfpfpfpfpk.
..kfpfpfpfpfpk..
..kfpfpfpfpfpk..
..kfpfpfpfpfpk..
..kfpfpfpfpfpk..
...kfpfpfpfpk...
...kkkkkkkkkk...
"""

GLYPHS = {
    "l": ["X.", "X.", "X.", "X.", "XX"],
    "e": ["...", "XXX", "XXX", "X..", "XXX"],
    "m": [".....", "XXXX.", "X.X.X", "X.X.X", "X.X.X"],
    "o": ["...", "XXX", "X.X", "X.X", "XXX"],
    "n": ["...", "XX.", "X.X", "X.X", "X.X"],
    "f": [".XX", ".X.", "XXX", ".X.", ".X."],
    "i": ["X", ".", "X", "X", "X"],
    "b": ["X..", "X..", "XXX", "X.X", "XXX"],
    "r": ["...", "XXX", "X..", "X..", "X.."],
}

WORD = "lemonfiber"
WORD_SCALE = 2
WORD_HEIGHT = 5 * WORD_SCALE
FIBER = ("a", "f")
ON_INK = [("p", "c")] * 5 + [FIBER] * 5
ON_PAPER = [("k", "k")] * 5 + [FIBER] * 5
MONO = {colour: [(colour, colour)] * 10 for colour in ("k", "p")}
MARK = 32
LEMON_TOP, LEMON_RIGHT, LEMON_BOTTOM = 4, 29, 28
BODY_TOP = 11
MARK_GAP = 4
MARGIN = 2


def parse(art):
    return art.strip("\n").split("\n")


class Canvas:
    def __init__(self, w, h, fill=None):
        self.w, self.h = w, h
        self.px = [[PALETTE[fill] if fill else None] * w for _ in range(h)]

    def set(self, x, y, ch):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = PALETTE[ch] if ch else None

    def get(self, x, y):
        return self.px[y][x] if 0 <= x < self.w and 0 <= y < self.h else None

    def rect(self, x, y, w, h, ch):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, ch)

    def blit(self, art, x0, y0, remap=None):
        for dy, row in enumerate(parse(art)):
            for dx, ch in enumerate(row):
                cell = (remap or {}).get(ch, ch)
                if cell != ".":
                    self.set(x0 + dx, y0 + dy, cell)


def merge(px):
    h, w = len(px), len(px[0])
    done = [[px[y][x] is None for x in range(w)] for y in range(h)]
    rects = []
    for y in range(h):
        x = 0
        while x < w:
            if done[y][x]:
                x += 1
                continue
            colour = px[y][x]
            run = 1
            while x + run < w and px[y][x + run] == colour and not done[y][x + run]:
                run += 1
            depth = 1
            while y + depth < h and all(
                px[y + depth][xx] == colour and not done[y + depth][xx] for xx in range(x, x + run)
            ):
                depth += 1
            for yy in range(y, y + depth):
                for xx in range(x, x + run):
                    done[yy][xx] = True
            rects.append((x, y, run, depth, colour))
            x += run
    return rects


def svg(canvas, cell, label):
    w, h = canvas.w * cell, canvas.h * cell
    lines = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {canvas.w} {canvas.h}" shape-rendering="crispEdges" role="img" aria-label="{label}">'
        ),
        f"  <title>{label}</title>",
    ]
    lines += [
        f'  <rect x="{x}" y="{y}" width="{rw}" height="{rh}" fill="{colour}"/>'
        for x, y, rw, rh, colour in merge(canvas.px)
    ]
    lines.append("</svg>")
    return ("\n".join(lines) + "\n").encode()


def png(canvas, scale, pad=0):
    w, h = canvas.w * scale + 2 * pad, canvas.h * scale + 2 * pad
    clear = b"\x00\x00\x00\x00"
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        cy = (y - pad) // scale if pad <= y < h - pad else None
        for x in range(w):
            colour = canvas.px[cy][(x - pad) // scale] if cy is not None and pad <= x < w - pad else None
            raw += bytes.fromhex(colour[1:]) + b"\xff" if colour else clear

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )


def disc(c, cx, cy, r, ch, only=None):
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            inside = (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 <= r * r
            if inside and (only is None or c.get(x, y) == PALETTE[only]):
                c.set(x, y, ch)


def rounded_square(c, n, r, ch):
    for y in range(n):
        for x in range(n):
            dx = max(r - x - 0.5, x + 0.5 - (n - r), 0)
            dy = max(r - y - 0.5, y + 0.5 - (n - r), 0)
            if dx * dx + dy * dy <= r * r:
                c.set(x, y, ch)


def text_width(word, f):
    return sum(len(GLYPHS[ch][0]) * f for ch in word) + (len(word) - 1) * f


def wordmark(c, word, x0, y0, f, ramps, shadow=0):
    def paint(ox, oy, shadow_pass):
        x = x0 + ox
        for i, ch in enumerate(word):
            top, bottom = ramps[i]
            glyph = GLYPHS[ch]
            for gy, row in enumerate(glyph):
                for gx, bit in enumerate(row):
                    if bit != "X":
                        continue
                    for yy in range(f):
                        py = gy * f + yy
                        colour = "K" if shadow_pass else top if py < 3 * f else bottom
                        c.rect(x + gx * f, y0 + oy + py, f, 1, colour)
            x += len(glyph[0]) * f + f

    if shadow:
        paint(shadow, shadow, True)
    paint(0, 0, False)


def lamp(c, x0, floor):
    disc(c, x0 + 7, 12, 19, "L", only="s")
    disc(c, x0 + 7, 12, 13, "l")
    for y in range(floor - 2, floor + 1):
        half = 9 - (floor - y) * 2
        c.rect(x0 + 7 - half, y, 2 * half, 1, "l")
    c.blit(LAMP_SHADE, x0, 7)
    c.rect(x0 + 6, 15, 2, floor - 17, "T")
    c.rect(x0 + 6, 15, 1, floor - 17, "u")
    c.blit(LAMP_FOOT, x0 + 1, floor - 3)


def sofa(c, x0, x1, back_top, seat_top, floor):
    c.rect(x0 + 4, back_top, x1 - x0 - 8, seat_top - back_top + 2, "n")
    c.rect(x0 + 4, back_top, x1 - x0 - 8, 1, "k")
    c.rect(x0 + 4, back_top + 1, x1 - x0 - 8, 1, "c")
    c.rect(x0 + 4 + (x1 - x0 - 8) // 2, back_top + 2, 1, seat_top - back_top - 2, "U")
    c.rect(x0 + 2, seat_top, x1 - x0 - 4, floor - seat_top - 2, "n")
    c.rect(x0 + 2, seat_top, x1 - x0 - 4, 1, "c")
    c.rect(x0 + 2, seat_top - 1, x1 - x0 - 4, 1, "k")
    c.rect(x0 + 2, floor - 4, x1 - x0 - 4, 2, "U")
    seat = x1 - x0 - 4
    for k in (1, 2):
        c.rect(x0 + 2 + seat * k // 3, seat_top, 1, floor - seat_top - 4, "U")
    for ax in (x0, x1 - 6):
        c.rect(ax, seat_top - 6, 6, floor - seat_top + 4, "c")
        c.rect(ax, seat_top - 7, 6, 1, "k")
        c.rect(ax + 1, seat_top - 6, 4, 1, "p")
        c.rect(ax, floor - 4, 6, 2, "U")
        c.rect(ax - 1, seat_top - 6, 1, floor - seat_top + 4, "k")
        c.rect(ax + 6, seat_top - 6, 1, floor - seat_top + 4, "k")
    c.rect(x0 + 3, floor - 2, 2, 2, "F")
    c.rect(x1 - 5, floor - 2, 2, 2, "F")


def lights(c, x0, x1, y0, sag):
    bulbs = ("B", "a", "B", "p")
    n = 0
    for x in range(x0, x1):
        y = y0 + round(sag * math.sin(math.pi * (x - x0) / (x1 - x0)))
        c.set(x, y, "l")
        if (x - x0) % 5 == 2:
            c.set(x, y + 1, "k")
            c.set(x, y + 2, bulbs[n % 4])
            n += 1


def scene(c, w, floor, lemon_x, lemon_y, garland, popcorn_x=None, lamp_x=1, sofa_x0=None, sofa_x1=None):
    c.rect(0, 0, w, floor, "s")
    lights(c, *garland)
    lamp(c, lamp_x, floor)
    sofa(
        c,
        lamp_x + 15 if sofa_x0 is None else sofa_x0,
        w - 1 if sofa_x1 is None else sofa_x1,
        floor - 22,
        floor - 10,
        floor,
    )
    c.rect(0, floor, w, 1, "L")
    if popcorn_x is not None:
        c.blit(POPCORN, popcorn_x, floor - 26)
    c.blit(LEMON_HERO, lemon_x, lemon_y)


def hero():
    c = Canvas(80, 72)
    floor = 58
    scene(c, 80, floor, 17, floor - 48, (20, 80, 1, 4), popcorn_x=63)
    c.rect(0, floor, 80, 1, "l")
    c.rect(0, floor + 1, 80, 72 - floor - 1, "k")
    wordmark(c, WORD, (80 - text_width(WORD, WORD_SCALE)) // 2, 61, WORD_SCALE, ON_INK, shadow=1)
    return c


def social():
    c = Canvas(128, 64)
    floor = 56
    c.rect(0, 0, 128, floor, "s")
    scene(c, 56, floor, 9, floor - 48, (16, 128, 1, 3), lamp_x=-3, sofa_x0=13, sofa_x1=56)
    c.rect(0, floor, 128, 1, "l")
    c.rect(0, floor + 1, 128, 64 - floor - 1, "k")
    for y, start in ((59, 1), (62, 3)):
        for x in range(start, 128, 5):
            c.set(x, y, "s")
    f, x0 = 3, 64
    wordmark(c, "lemon", x0, 12, f, ON_INK[:5], shadow=1)
    wordmark(c, "fiber", x0, 32, f, ON_INK[5:], shadow=1)
    for x in range(x0, x0 + text_width("lemon", f), 3):
        c.rect(x, 52, 2, 1, "F")
    return c


def app_icon():
    c = Canvas(32, 32)
    rounded_square(c, 32, 7.0, "p")
    c.blit(LEMON_ICON, 0, 0)
    return c


def touch_icon():
    c = Canvas(36, 36, "p")
    c.blit(LEMON_ICON, 2, 2)
    return c


def art(grid, w, h, ground=None, at=(0, 0), remap=None):
    c = Canvas(w, h, ground)
    c.blit(grid, *at, remap)
    return c


def blit_mark(c, x, y, mono=None):
    if mono:
        c.blit(LEMON_MONO, x, y + 1, {"k": mono})
    else:
        c.blit(LEMON_ICON, x, y)


def mark(mono=None, ground=None, margin=0):
    c = Canvas(MARK + 2 * margin, MARK + 2 * margin, ground)
    blit_mark(c, margin, margin, mono)
    return c


def lockup_horizontal(ramps, ground=None, mono=None, shadow=0):
    x = LEMON_RIGHT + 1 + MARK_GAP
    c = Canvas(x + text_width(WORD, WORD_SCALE) + MARGIN, MARK, ground)
    blit_mark(c, 0, 0, mono)
    wordmark(c, WORD, x, (BODY_TOP + LEMON_BOTTOM + 1 - WORD_HEIGHT) // 2, WORD_SCALE, ramps, shadow)
    return c


def lockup_stacked():
    w = text_width(WORD, WORD_SCALE) + 2 * MARGIN
    y = MARGIN - LEMON_TOP
    word_y = y + LEMON_BOTTOM + 1 + MARK_GAP
    c = Canvas(w, word_y + WORD_HEIGHT + MARGIN)
    blit_mark(c, (w - MARK) // 2, y)
    wordmark(c, WORD, MARGIN, word_y, WORD_SCALE, ON_PAPER)
    return c


def wordmark_alone(ramps):
    c = Canvas(text_width(WORD, WORD_SCALE) + 2 * MARGIN, WORD_HEIGHT + 2 * MARGIN)
    wordmark(c, WORD, MARGIN, MARGIN, WORD_SCALE, ramps)
    return c


def tray(colour):
    return art(LEMON_TRAY, 16, 16, remap={"k": colour})


def build():
    icon16 = art(LEMON_ICON16, 16, 16)
    small = art(LEMON_SMALL, 16, 16)
    icon = app_icon()
    horizontal = lockup_horizontal(ON_PAPER)
    trays = {"template": tray("k"), "knockout": tray("p")}
    files = {
        "hero.svg": svg(hero(), 8, "lemonfiber"),
        "social.svg": svg(social(), 10, "lemonfiber"),
        "mark-primary.svg": svg(mark(), 16, "lemonfiber mark"),
        "mark-primary-on-ink.svg": svg(mark(ground="k", margin=4), 16, "lemonfiber mark on ink"),
        "mark-mono-ink.svg": svg(mark("k"), 16, "lemonfiber one-colour mark"),
        "mark-mono-knockout.svg": svg(mark("p", "F", 4), 16, "lemonfiber knockout mark"),
        "mark-small.svg": svg(small, 4, "lemonfiber small-size mark"),
        "favicon.svg": svg(small, 4, "lemonfiber favicon"),
        "app-icon.svg": svg(icon, 16, "lemonfiber app icon"),
        "app-icon-16.svg": svg(icon16, 4, "lemonfiber app icon, 16-cell"),
        "lockup-horizontal.svg": svg(horizontal, 8, "lemonfiber horizontal lockup"),
        "lockup-horizontal-on-ink.svg": svg(
            lockup_horizontal(ON_INK, ground="k", shadow=1), 8, "lemonfiber horizontal lockup on ink"
        ),
        "lockup-horizontal-mono.svg": svg(
            lockup_horizontal(MONO["k"], mono="k"), 8, "lemonfiber one-colour horizontal lockup"
        ),
        "lockup-horizontal-knockout.svg": svg(
            lockup_horizontal(MONO["p"], ground="F", mono="p"), 8, "lemonfiber knockout horizontal lockup"
        ),
        "lockup-stacked.svg": svg(lockup_stacked(), 8, "lemonfiber stacked lockup"),
        "wordmark.svg": svg(wordmark_alone(ON_PAPER), 8, "lemonfiber wordmark"),
        "wordmark-mono.svg": svg(wordmark_alone(MONO["k"]), 8, "lemonfiber wordmark, one colour"),
        "export/social.png": png(social(), 10),
        "export/app-icon-touch-180.png": png(touch_icon(), 5),
        "export/home-assistant/icon.png": png(icon, 8),
        "export/home-assistant/icon@2x.png": png(icon, 16),
        "export/home-assistant/logo.png": png(horizontal, 8),
        "export/home-assistant/logo@2x.png": png(horizontal, 16),
    }
    for size, scale in ((16, 1), (48, 3)):
        files[f"export/app-icon-{size}.png"] = png(icon16, scale)
    for size, scale in ((32, 1), (192, 6), (512, 16), (1024, 32)):
        files[f"export/app-icon-{size}.png"] = png(icon, scale)
    for size in (16, 32, 48):
        files[f"export/favicon-{size}.png"] = png(small, size // 16)
    for name, canvas in trays.items():
        files[f"tray-{name}.svg"] = svg(canvas, 1, "lemonfiber tray icon")
        for size, scale, pad in ((16, 1, 0), (22, 1, 3), (32, 2, 0)):
            files[f"export/tray-{name}-{size}.png"] = png(canvas, scale, pad)
            files[f"export/tray-{name}-{size}@2x.png"] = png(canvas, scale * 2, pad * 2)
    return files


def decoded(data):
    if not data.startswith(b"\x89PNG"):
        return data
    header, idat, at = b"", b"", 8
    while at < len(data):
        (length,) = struct.unpack(">I", data[at : at + 4])
        kind, body = data[at + 4 : at + 8], data[at + 8 : at + 8 + length]
        if kind == b"IHDR":
            header = body
        elif kind == b"IDAT":
            idat += body
        at += 12 + length
    return header + zlib.decompress(idat)


def matches(name, data):
    path = LOGO / name
    return path.is_file() and decoded(path.read_bytes()) == decoded(data)


def on_disk():
    return {str(p.relative_to(LOGO)) for p in LOGO.rglob("*") if p.is_file() and p.name != ".DS_Store"}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail on any file the grids do not draw")
    args = parser.parse_args()
    files = build()
    stale = sorted(on_disk() - files.keys())
    if args.check:
        drift = sorted(name for name, data in files.items() if not matches(name, data))
        for name in drift:
            print(f"assets/logo/{name}: differs from what scripts/logo.py draws", file=sys.stderr)
        for name in stale:
            print(f"assets/logo/{name}: not drawn by scripts/logo.py", file=sys.stderr)
        if drift or stale:
            print("run: python3 scripts/logo.py", file=sys.stderr)
            return 1
        print(f"assets/logo: {len(files)} files match their grids")
        return 0
    for name in stale:
        (LOGO / name).unlink()
    for name, data in files.items():
        path = LOGO / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(f"assets/logo: wrote {len(files)} files, removed {len(stale)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
