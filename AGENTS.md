# AGENTS.md — brand

Guidance for any AI agent working in this repo.

> **Common rules for every lemonfiber repo are canonical in the spec:**
> [50-governance/ai-contributors.md](https://github.com/lemonfiber/spec/blob/main/50-governance/ai-contributors.md).
> This file is the `brand`-specific header only.

## What this repo is

The design system — logo assets, colour/type/space tokens, usage docs. Published
as `@lemonfiber/brand`. Spec:
[`30-repos/brand.md`](https://github.com/lemonfiber/spec/blob/main/30-repos/brand.md)
and [`60-brand/`](https://github.com/lemonfiber/spec/tree/main/60-brand).

## The rules you cannot break

- **The palette is closed.** No colour outside the tokens; no blue/teal/cyan;
  amber is signal-only, never a background fill or body text (`DES-R1`–`DES-R3`).
- **css/json parity.** `tokens.css` and `tokens.json` hold identical values —
  `scripts/check_tokens.py` enforces it (`ARCH-R38`).
- **WCAG AA.** Body-text pairings must meet AA; the same script checks it
  (`ARCH-R40`). A failing pairing is a contract violation, not a preference.
- **The marks are proprietary** (`assets/logo/*`). Tokens and `.docs/` are open.
- **Wordmarks ship outlined** — never re-typeset; edit the SVG or add an export.

## Governance for a visual repo

Aesthetic changes *within* the rules cite `GOV-R12`. Changes to what the rules
*permit* (a palette addition, a new minimum size) are `DES-R` changes following
the normal lifecycle.

## Before you open a PR

- `python3 scripts/check_tokens.py` passes.
- Cite a spec identifier in a commit `Spec:` trailer and the PR body.
- No AI attribution in commits.
