# Colour

Four working colours and two surfaces. Lemon carries the personality, ink carries the structure, fibre-amber is reserved for the fibre itself — it is a signal colour, not a decorative one.

| Token | Hex | Role |
| --- | --- | --- |
| `--lf-color-ink` | #17160F | Text, outlines, dark surfaces |
| `--lf-color-lemon` | #F0C419 | The fruit; primary brand colour |
| `--lf-color-fiber` | #E07A17 | Fibre cores, active states |
| `--lf-color-fiber-deep` | #A85A12 | "fiber" in the wordmark, links |
| `--lf-color-leaf` | #5B6B2A | Leaf only |
| `--lf-color-paper` | #FBF7EA | Default surface |
| `--lf-color-pith` | #FBF6E7 | Inner surface, cards on paper |
| `--lf-color-canvas` | #EDE7D5 | Page behind cards |

## Rules

- Never more than two background colours in one layout.
- Amber never becomes a background fill at scale — it is line, core, and accent.
- No blues, teals, or cyans anywhere in the palette.
- Dark mode: set `data-lf-theme="ink"` on the root; amber lightens to `--lf-color-fiber-light` for contrast.
