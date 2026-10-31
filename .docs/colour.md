# Colour

Lemon carries the personality, ink carries the structure, fibre-amber is reserved for the fibre itself — "fiber" in the wordmark, cores, active states — it is a signal colour, not a decorative one.

The tokens hold the values and this page holds the roles: read a hex from
[`tokens/tokens.json`](../tokens/tokens.json) or
[`tokens/tokens.css`](../tokens/tokens.css), never from here.

| Token | Role |
| --- | --- |
| `--lf-color-ink` | Text, outlines, dark surfaces |
| `--lf-color-ink-soft` | Raised surface in the ink theme |
| `--lf-color-lemon` | The fruit; primary brand colour |
| `--lf-color-lemon-bright` | The step above lemon — hover, lift, the lit edge of the lemon in the mark |
| `--lf-color-fiber` | Fibre cores, active states, the lower rows of "fiber" in the wordmark |
| `--lf-color-fiber-deep` | Links, the lemon's stem, the ground of the knockout marks |
| `--lf-color-fiber-light` | Amber in the ink theme, where the deep tone loses contrast; the upper rows of "fiber" in the wordmark and the shaded edge of the lemon |
| `--lf-color-leaf` | Leaf only |
| `--lf-color-paper` | Default surface |
| `--lf-color-pith` | Inner surface, cards on paper |
| `--lf-color-canvas` | Page behind cards |
| `--lf-color-line` | Borders and dividers |
| `--lf-color-line-soft` | Dividers within a card |
| `--lf-color-text-muted` | Secondary text |
| `--lf-color-text-faint` | Tertiary text, one step lighter than muted |
| `--lf-color-ok` | A thing standing as it should; always beside its shape |
| `--lf-color-alarm` | A thing that has stopped or failed; always beside its shape |
| `--lf-color-warn-tint` | Ground behind a warning, which `--lf-color-fiber` marks |
| `--lf-color-alarm-tint` | Ground behind an alarm |

## Rules

- Never more than two background colours in one layout.
- Amber never becomes a background fill at scale — it is line, core, and accent.
- A severity colour is never the only sign of a state; a shape of its own sits beside it. `--lf-color-fiber` is the warning colour.
- No blues, teals, or cyans anywhere in the palette.
- Dark mode: set `data-lf-theme="ink"` on the root; amber lightens to `--lf-color-fiber-light` for contrast.
