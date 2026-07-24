#!/usr/bin/env python3
"""Token checks: css/json parity and WCAG AA contrast for body-text pairings.
See spec 60-brand/accessibility.md and 20-architecture/contracts/design-tokens.md.
"""
import json, re, sys, pathlib

BR = pathlib.Path(__file__).resolve().parent.parent
errs = []

# --- parity: every colour in tokens.json appears in tokens.css with same value ---
data = json.load(open(BR / "tokens" / "tokens.json"))
css = (BR / "tokens" / "tokens.css").read_text()
for name, val in data.get("color", {}).items():
    prop = f"--lf-color-{name}"
    m = re.search(re.escape(prop) + r"\s*:\s*([^;]+);", css)
    if not m:
        errs.append(f"parity: {prop} missing from tokens.css")
    elif m.group(1).strip().lower() != str(val).strip().lower():
        errs.append(f"parity: {prop} css={m.group(1).strip()} != json={val}")

# --- contrast ---
def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
def L(h):
    h = h.lstrip("#"); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b)
def ratio(a, b):
    la, lb = L(a), L(b); hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

col = data["color"]
# Body-safe pairings that MUST meet AA (4.5). Baseline from 60-brand/accessibility.md.
BODY_ON_PAPER = ["ink", "ink-soft", "text-muted", "leaf", "fiber-deep"]
for fg in BODY_ON_PAPER:
    r = ratio(col[fg], col["paper"])
    if r < 4.5:
        errs.append(f"contrast: {fg} on paper is {r:.2f}, below AA 4.5 (body-safe set)")

if errs:
    print("\n".join(f"::error::{e}" for e in errs))
    sys.exit(1)
print("tokens: css/json parity OK; body-text pairings meet WCAG AA")
