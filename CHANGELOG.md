# Changelog

## 0.4.0 — 2026-11-01

- The mark is a whole pixel lemon with a play triangle and a leaf, drawn on a 32-cell grid with a 16-cell redraw for small sizes; the wordmark is drawn in the same cells, with "fiber" in amber.
- `scripts/logo.py` draws every file under `assets/logo/` from those grids, with every colour taken from `tokens/tokens.json`; `just logo` writes them and `just ci` fails on any drift.
- Added `hero.svg`, `social.svg`, `app-icon-16.svg`, `tray-template.svg` and `tray-knockout.svg`, and PNG exports for app icons, favicons, tray icons and the social preview.

## 0.3.0 — 2026-10-05

- Severity colours: `ok` and `alarm`, with `warn-tint` and `alarm-tint`, in the paper and the ink theme. `fiber` is the warning colour. Each meets WCAG AA on every ground its theme draws.

## 0.2.0 — 2026-07-24

- Wordmark converted to outlines in all lockup and wordmark SVGs — assets render identically without the font installed.
- Added one-colour and knockout horizontal lockups, plus `wordmark-mono.svg`.
- Added `.docs/asset-sheet.html` contact sheet.

## 0.1.0 — 2026-07-24

- Initial brand release: patch-panel-slice mark, horizontal and stacked lockups.
- One-colour, knockout, and small-size crop variants.
- Colour, type, and space tokens as CSS custom properties and JSON.
- Logo, colour, and typography usage docs.
