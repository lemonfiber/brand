# AGENTS.md — brand

> **Start at the roadmap and board on [lemonfiber.app](https://lemonfiber.app),
> rendered from the report of where every unreleased version stands. Then the
> rules** every repository shares:
> [working in the repositories](https://github.com/lemonfiber/spec/blob/main/50-governance/working-in-the-repositories.md)
> and [the rules for agents](https://github.com/lemonfiber/spec/blob/main/50-governance/ai-contributors.md).
> This file holds only what is true of this repository.

## What this repo is

The design system — logo assets, colour/type/space tokens, usage docs. Packaged
as `@lemonfiber/brand`, installed from this repo rather than from a registry.
Spec:
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

```sh
just ci
```

The token gate and the script that decides it, which is the whole of what CI
reads in this tree. The `justfile` names what it leaves out and what answers
each.

Its first step turns this clone's git hooks on.
