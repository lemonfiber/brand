# Logo usage

## The mark

A whole pixel lemon with a play triangle on its face and a leaf on its stem: the fruit, and the thing it is for. It is drawn on a grid of square cells and every cell takes a colour from the token palette.

The master grid is 32 cells square. A 16-cell redraw carries the same lemon, triangle and leaf at the sizes where 32 cells cannot each get a pixel of their own.

Every file under `assets/logo/` is drawn by [`scripts/logo.py`](../scripts/logo.py) from those grids: run `just logo` after changing a grid, and `just ci` fails while a file differs from what the grids draw. Nothing in `assets/logo/` is edited by hand.

## Versions

| Version | Files | Use |
| --- | --- | --- |
| **Hero** | `hero.svg` | The lemon on a sofa between a floor lamp and a popcorn bucket, under string lights, with the wordmark on an ink band below. It carries its own ground and reads on paper and ink alike: README headers, landing pages, about screens |
| **Social** | `social.svg`, `export/social.png` | The hero scene at 1280×640 with the wordmark beside it in two lines. Repository social previews and link cards |
| **Icon** | `app-icon.svg`, `app-icon-16.svg` | The lemon on a rounded paper tile. App icons, launchers, home-screen shortcuts, the Home Assistant brand image |
| **Mark** | `mark-primary.svg`, `mark-primary-on-ink.svg` | The lemon alone, in full colour, on a transparent or an ink ground |
| **Favicon** | `favicon.svg`, `mark-small.svg` | The 16-cell lemon alone. Browser tabs and every place the mark sits below 32px |
| **Tray template** | `tray-template.svg`, `tray-knockout.svg` | The lemon as one silhouette with the triangle cut out. `tray-template` is ink on transparency, the template image a macOS menu bar tints from its alpha alone; `tray-knockout` is paper on transparency, for dark trays and taskbars that do not tint |
| **Mono** | `mark-mono-ink.svg`, `mark-mono-knockout.svg` | The same silhouette in one colour: ink on light, or paper knocked out of `--lf-color-fiber-deep`. Screenprint, embroidery, etch, single-plate print |

## Lockups

- **Horizontal** — `lockup-horizontal.svg`: the mark left, the wordmark right, 4 cells apart, the wordmark centred on the lemon's body. Variants: `-on-ink`, `-mono`, `-knockout`.
- **Stacked** — `lockup-stacked.svg`: the mark above the wordmark, 4 cells apart, centred, for narrow or square placements.
- **Wordmark alone** — `wordmark.svg`, `wordmark-mono.svg`: only where the mark already appears in the same view.

The wordmark is drawn in cells like the mark: each letter is a 5-row pixel glyph at 2 cells a glyph pixel, so it stands 10 cells tall beside the 32-cell mark.

## Exports

PNG renders for platforms that ask for a bitmap, each at a whole multiple of its grid, some inside a border of whole pixels. A render with no transparent pixel carries no alpha channel:

| Files | Drawn from | Sizes |
| --- | --- | --- |
| `export/app-icon-<size>.png` | `app-icon-16.svg` at 16 and 48, `app-icon.svg` at 32, 192, 512 and 1024 | 16, 32, 48, 192, 512, 1024 |
| `export/app-icon-touch-180.png` | the icon's lemon on a full paper square | 180 (Apple touch icon) |
| `export/app-icon-touch-1024.png` | the same square at 28px a cell inside an 8px paper border, fully opaque | 1024 (iOS app icon) |
| `export/favicon-<size>.png` | `favicon.svg` | 16, 32, 48 |
| `export/tray-template-<size>[@2x].png`, `export/tray-knockout-<size>[@2x].png` | the tray grid | 16, 22, 32, each with `@2x` |
| `export/social.png` | `social.svg` | 1280×640 |
| `export/home-assistant/icon[@2x].png` | `app-icon.svg` | 256, 512 |
| `export/home-assistant/logo[@2x].png` | `lockup-horizontal.svg` | 256 and 512 tall |

## Clear space and minimum size

Clear space on all four sides equals **x = 4 cells** of the mark's own grid, measured from the lemon's outermost cell, leaf included: one eighth of the 32-cell master, 2 cells on the 16-cell. Nothing else enters it. The files with a baked ground (`mark-primary-on-ink`, `mark-mono-knockout`) carry that ground as their clear space.

| Version | Minimum | Below that |
| --- | --- | --- |
| 32-cell mark, icon and lockups | 32px screen (one pixel a cell), 9mm print | the 16-cell: `app-icon-16.svg` for the icon, `mark-small.svg` or `favicon.svg` for the mark |
| 16-cell icon, favicon and small mark | 16px | — |
| Tray | 16, 22 and 32px, each with a `@2x` | — |
| Hero | 160px wide (two pixels a cell) | a lockup |

The tray grid is 16 cells: one pixel a cell at 16px, the same 16 pixels centred in a 22px square, and two pixels a cell at 32px.

Show a mark at a whole multiple of its grid — the 32-cell at 32, 64, 96px and on, the 16-cell at 16, 32, 48px — so every cell lands on whole pixels. Scale with nearest-neighbour sampling, never smoothing.

## Colour pairings

"fiber" in the wordmark is always amber: `--lf-color-fiber-light` on the upper three glyph rows over `--lf-color-fiber` on the lower two, on every ground, except in one-colour reproduction.

| Background | Mark | Wordmark | Files |
| --- | --- | --- | --- |
| `--lf-color-paper` | primary | "lemon" in `--lf-color-ink`, "fiber" in amber | `lockup-horizontal`, `lockup-stacked`, `wordmark` |
| `--lf-color-ink` | primary on ink | "lemon" in `--lf-color-paper` over `--lf-color-canvas`, "fiber" in amber, with a one-cell shadow in the ink theme's `canvas` | `lockup-horizontal-on-ink`, `hero`, `social` |
| `--lf-color-fiber-deep` | knockout | paper, single colour | `lockup-horizontal-knockout`, `mark-mono-knockout` |
| One-colour reproduction | mono ink | ink, single colour | `lockup-horizontal-mono`, `mark-mono-ink`, `wordmark-mono` |
| Photography | knockout, on its own `--lf-color-fiber-deep` ground | paper, single colour | `lockup-horizontal-knockout` |

## Don't

- Add a tagline, descriptor, or strapline to the lockup.
- Recolour cells outside the token palette.
- Rotate, skew, stretch, or add gradients, bevels, or drop shadows to the mark.
- Scale a mark by a fraction of its grid or smooth its cells.
- Place the 32-cell mark below 32px — switch to the 16-cell.
- Re-draw, re-set or re-space the wordmark — take its SVG.
- Outline the mark or set it in an unapproved colour to "match" a partner brand.
