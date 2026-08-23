# Colour

Lemon carries the personality, ink carries the structure, fibre-amber is reserved for the fibre itself — it is a signal colour, not a decorative one.

The tokens hold the values and this page holds the roles: read a hex from
[`tokens/tokens.json`](../tokens/tokens.json) or
[`tokens/tokens.css`](../tokens/tokens.css), never from here.

| Token | Role |
| --- | --- |
| `--lf-color-ink` | Text, outlines, dark surfaces |
| `--lf-color-ink-soft` | Raised surface in the ink theme |
| `--lf-color-lemon` | The fruit; primary brand colour |
| `--lf-color-lemon-bright` | The step above lemon — hover, lift |
| `--lf-color-fiber` | Fibre cores, active states |
| `--lf-color-fiber-deep` | "fiber" in the wordmark, links |
| `--lf-color-fiber-light` | Amber in the ink theme, where the deep tone loses contrast |
| `--lf-color-leaf` | Leaf only |
| `--lf-color-paper` | Default surface |
| `--lf-color-pith` | Inner surface, cards on paper |
| `--lf-color-canvas` | Page behind cards |
| `--lf-color-line` | Borders and dividers |
| `--lf-color-line-soft` | Dividers within a card |
| `--lf-color-text-muted` | Secondary text |
| `--lf-color-text-faint` | Tertiary text, one step lighter than muted |

## Rules

- Never more than two background colours in one layout.
- Amber never becomes a background fill at scale — it is line, core, and accent.
- No blues, teals, or cyans anywhere in the palette.
- Dark mode: set `data-lf-theme="ink"` on the root; amber lightens to `--lf-color-fiber-light` for contrast.
