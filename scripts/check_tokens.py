#!/usr/bin/env python3
"""Token checks: css/json parity and WCAG AA contrast for body-text pairings.
See spec 60-brand/accessibility.md and 20-architecture/contracts/design-tokens.md.

`--self-test` holds the contrast arithmetic to ratios WCAG states, and the parity
check to every way the two files can drift apart, before either decides anything.
Parity compares two values somebody wrote down; contrast computes one, and a wrong
answer there is the only kind that ships a colour nobody can read while reporting
that every pairing meets AA.
"""

import json
import pathlib
import re
import sys

BR = pathlib.Path(__file__).resolve().parent.parent
errs = []

# --- parity: every token in both files, with identical values (ARCH-R38) ---
PX = ("space", "radius")
FONT_CATEGORIES = ("weight", "tracking")


def kebab(key):
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r"-\1", key).lower()


def own_category(key):
    """The category a key under `font` names a token of, where it is not a family."""
    head = kebab(key).split("-", 1)[0]
    return head if head in FONT_CATEGORIES else None


def declared(block):
    """Every custom property a CSS block declares, by name, with its value as written."""
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"(--lf-[a-z0-9-]+)\s*:\s*([^;]+);", block)}


def stack(value):
    """A CSS font stack as the list of families it names, quotes taken off."""
    return [family.strip().strip('"').strip("'") for family in value.split(",")]


def written(category, value):
    """A JSON value as tokens.css writes it."""
    if category in PX and isinstance(value, int) and not isinstance(value, bool):
        return f"{value}px"
    return str(value)


def expected(data):
    """Every CSS property tokens.json implies for the default theme, with its value, and what cannot be mapped.

    `color.ink` is `--lf-color-ink`, `size.displayXl` is `--lf-size-display-xl`, and
    `font.weightBody` and `font.trackingDisplay` are `--lf-weight-body` and
    `--lf-tracking-display`. A number under `space` or `radius` is that many px, and
    a family under `font` heads its CSS stack, `fallback` naming the rest in order.
    """
    want, problems = {}, []
    fallback = data.get("fallback", {})
    for category, tokens in data.items():
        if category in ("theme", "fallback"):
            continue
        if not isinstance(tokens, dict):
            problems.append(f"parity: tokens.json `{category}` is not a group of tokens")
            continue
        for key, value in tokens.items():
            name = kebab(key)
            if category == "font" and own_category(key):
                want[f"--lf-{name}"] = written(own_category(key), value)
            elif category == "font":
                want[f"--lf-font-{name}"] = [value, *fallback.get(key, [])]
            else:
                want[f"--lf-{category}-{name}"] = written(category, value)
    families = {key for key in data.get("font", {}) if not own_category(key)}
    for key in sorted(set(fallback) - families):
        problems.append(f"parity: tokens.json fallback `{key}` names no family under `font`")
    return want, problems


def parity(data, css):
    """Every way tokens.css and tokens.json differ, as one line each."""
    errs = []
    root = re.search(r":root\s*\{([^}]*)\}", css)
    ink_css = re.search(r'\[data-lf-theme="ink"\]\s*\{([^}]*)\}', css)
    if not root:
        return ["parity: tokens.css has no :root block"]
    want, problems = expected(data)
    errs.extend(problems)
    have = declared(root.group(1))
    for prop in sorted(set(want) | set(have)):
        a, b = have.get(prop), want.get(prop)
        if isinstance(b, list) and a is not None:
            a = stack(a)
        if a != b:
            errs.append(f"parity: {prop} css={a} != json={b}")
    ink_json = {f"--lf-color-{name}": value for name, value in data.get("theme", {}).get("ink", {}).items()}
    if not ink_css:
        errs.append('parity: tokens.css has no [data-lf-theme="ink"] block')
    else:
        in_css = declared(ink_css.group(1))
        for prop in sorted(set(in_css) | set(ink_json)):
            a, b = in_css.get(prop), ink_json.get(prop)
            if a != b:
                errs.append(f"parity: ink theme {prop} css={a} != json={b}")
    return errs


with (BR / "tokens" / "tokens.json").open(encoding="utf-8") as f:
    data = json.load(f)
css = (BR / "tokens" / "tokens.css").read_text(encoding="utf-8")
ink_json = data.get("theme", {}).get("ink", {})
errs.extend(parity(data, css))


# --- contrast ---
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


SMALL_JSON = {
    "color": {"ink": "#17160F"},
    "font": {"body": "Golos Text", "weightBody": 500},
    "fallback": {"body": ["Segoe UI", "sans-serif"]},
    "space": {"1": 4},
    "theme": {"ink": {"paper": "#17160F"}},
}
SMALL_CSS = """:root {
  --lf-color-ink: #17160F;
  --lf-font-body: "Golos Text", "Segoe UI", sans-serif;
  --lf-weight-body: 500;
  --lf-space-1: 4px;
}
[data-lf-theme="ink"] {
  --lf-color-paper: #17160F;
}
"""

# Each drift the parity check exists to catch, with the line it must report it by.
DRIFTS = [
    (
        "a value changed in the css",
        ("#17160F;", "#17160E;"),
        None,
        "--lf-color-ink css=#17160E != json=#17160F",
    ),
    (
        "a token only the css carries",
        ("--lf-space-1: 4px;", "--lf-space-1: 4px; --lf-shadow-lift: none;"),
        None,
        "--lf-shadow-lift css=none != json=None",
    ),
    ("a token only the json carries", None, ("space", {"1": 4, "2": 8}), "--lf-space-2 css=None != json=8px"),
    ("a length in another unit", ("4px", "4rem"), None, "--lf-space-1 css=4rem != json=4px"),
    (
        "a fallback the json does not list",
        ('"Segoe UI", sans-serif', "sans-serif"),
        None,
        "--lf-font-body css=['Golos Text', 'sans-serif'] != json=['Golos Text', 'Segoe UI', 'sans-serif']",
    ),
    (
        "a fallback for no family",
        None,
        ("fallback", {"body": ["sans-serif"], "mono": ["monospace"]}),
        "fallback `mono` names no family",
    ),
    (
        "an ink value only the css carries",
        ("--lf-color-paper: #17160F;", "--lf-color-paper: #17160F; --lf-color-ok: #000000;"),
        None,
        "ink theme --lf-color-ok css=#000000 != json=None",
    ),
]


def parity_self_test():
    """The parity check, against a pair that agrees and each way the two can drift apart."""
    problems = [f"a matching pair reports: {e}" for e in parity(SMALL_JSON, SMALL_CSS)]
    for said, css_edit, json_edit, want in DRIFTS:
        css_text = SMALL_CSS.replace(*css_edit, 1) if css_edit else SMALL_CSS
        json_data = {**SMALL_JSON, json_edit[0]: json_edit[1]} if json_edit else SMALL_JSON
        reported = parity(json_data, css_text)
        if not any(want in line for line in reported):
            problems.append(f"parity misses {said}: wanted `{want}`, got {reported}")
    return problems


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

    problems.extend(parity_self_test())

    if problems:
        print("\n".join(f"::error::self-test: {p}" for p in problems))
        print(
            "\nA check that is wrong passes tokens it exists to refuse.",
            file=sys.stderr,
        )
        return 1
    print(
        f"tokens self-test: all {len(PINNED)} ratios match WCAG, AA falls where it should, "
        f"and parity reports all {len(DRIFTS)} drifts"
    )
    return 0


if "--self-test" in sys.argv[1:]:
    sys.exit(self_test())

if errs:
    print("\n".join(f"::error::{e}" for e in errs))
    sys.exit(1)
print("tokens: css/json parity OK, ink theme included; body-text pairings meet WCAG AA in both themes")
