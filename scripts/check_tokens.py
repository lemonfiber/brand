#!/usr/bin/env python3
"""Token checks: css/json parity and WCAG AA contrast for body-text pairings.
See spec 60-brand/accessibility.md and 20-architecture/contracts/design-tokens.md.

`--self-test` holds the contrast arithmetic to ratios WCAG states, before it is
used to decide anything. Everything else here compares two values somebody wrote
down; this part computes one, and a wrong answer is the only kind that ships a
colour nobody can read while reporting that every pairing meets AA.
"""
import json
import pathlib
import re
import sys

BR = pathlib.Path(__file__).resolve().parent.parent
errs = []

# --- parity: every colour in tokens.json appears in tokens.css with same value ---
with (BR / "tokens" / "tokens.json").open(encoding="utf-8") as f:
    data = json.load(f)
css = (BR / "tokens" / "tokens.css").read_text()
for name, val in data.get("color", {}).items():
    prop = f"--lf-color-{name}"
    m = re.search(re.escape(prop) + r"\s*:\s*([^;]+);", css)
    if not m:
        errs.append(f"parity: {prop} missing from tokens.css")
    elif m.group(1).strip().lower() != str(val).strip().lower():
        errs.append(f"parity: {prop} css={m.group(1).strip()} != json={val}")

# --- contrast ---
# The ink theme is published in both files too (ARCH-R38), and it is held both
# ways: a value one file carries and the other does not is a dark mode that
# differs by which file a surface read.
ink_css = re.search(r'\[data-lf-theme="ink"\]\s*\{([^}]*)\}', css)
ink_json = data.get("theme", {}).get("ink", {})
if not ink_css:
    errs.append('parity: tokens.css has no [data-lf-theme="ink"] block')
else:
    in_css = {
        m.group(1): m.group(2).strip()
        for m in re.finditer(r"--lf-color-([a-z-]+)\s*:\s*([^;\s][^;]*);", ink_css.group(1))
    }
    for name in sorted(set(in_css) | set(ink_json)):
        a, b = in_css.get(name), ink_json.get(name)
        if a is None or b is None or a.lower() != str(b).lower():
            errs.append(f"parity: ink theme --lf-color-{name} css={a} != json={b}")


def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

col = data["color"]
# Body-safe pairings that MUST meet AA (4.5). Baseline from 60-brand/accessibility.md.
BODY_ON_PAPER = ["ink", "ink-soft", "text-muted", "leaf", "fiber-deep"]
for fg in BODY_ON_PAPER:
    r = ratio(col[fg], col["paper"])
    if r < 4.5:
        errs.append(f"contrast: {fg} on paper is {r:.2f}, below AA 4.5 (body-safe set)")

# The same guarantee on the ink theme's own paper, with the ink theme's values:
# a dark mode is read as much as a light one (ARCH-R40).
BODY_ON_INK_PAPER = ["text", "text-muted", "text-faint", "fiber-deep"]
for fg in BODY_ON_INK_PAPER:
    if fg in ink_json and "paper" in ink_json:
        r = ratio(ink_json[fg], ink_json["paper"])
        if r < 4.5:
            errs.append(f"contrast: {fg} on the ink theme's paper is {r:.2f}, below AA 4.5")

# --- the arithmetic, against ratios WCAG states ---
# Two of these are the canonical AA boundary: #767676 on white is the darkest
# grey that passes and #777777 the lightest that fails, one step apart. A
# luminance curve that has drifted lands on the wrong side of exactly that pair
# while still answering plausibly everywhere else.
PINNED = [
    ("#000000", "#ffffff", 21.0, "black on white is the widest ratio there is"),
    ("#ffffff", "#000000", 21.0, "the same pair the other way round is the same ratio"),
    ("#ffffff", "#ffffff", 1.0, "a colour on itself is no contrast at all"),
    ("#767676", "#ffffff", 4.54, "the darkest grey that meets AA on white"),
    ("#777777", "#ffffff", 4.48, "one step lighter, and it does not"),
    ("#0000ff", "#ffffff", 8.59, "a saturated blue, where the channel weights show"),
]


def self_test():
    """The maths, before it is trusted to decide anything."""
    problems = []
    for fg, bg, want, said in PINNED:
        got = ratio(fg, bg)
        if abs(got - want) > 0.01:
            problems.append(f"{fg} on {bg} is {got:.4f}, and WCAG says {want} — {said}")

    # The boundary is what the check actually rests on, so it is asserted as a
    # boundary rather than as two numbers that happen to be right.
    if not (ratio("#767676", "#ffffff") >= 4.5 > ratio("#777777", "#ffffff")):
        problems.append("the AA boundary no longer falls between #767676 and #777777")

    if problems:
        print("\n".join(f"::error::self-test: {p}" for p in problems))
        print("\nA contrast check whose arithmetic is wrong reports that unreadable "
              "text meets AA.", file=sys.stderr)
        return 1
    print(f"tokens self-test: all {len(PINNED)} ratios match WCAG, and AA falls where it should")
    return 0


if "--self-test" in sys.argv[1:]:
    sys.exit(self_test())

if errs:
    print("\n".join(f"::error::{e}" for e in errs))
    sys.exit(1)
print("tokens: css/json parity OK, ink theme included; body-text pairings meet WCAG AA in both themes")
