# Typography

Three faces, each with one job.

| Face | Token | Sets |
| --- | --- | --- |
| **Bricolage Grotesque** | `--lf-font-display` | Display headings on marketing surfaces |
| **Golos Text** | `--lf-font-body` | Interface text — every product surface, headings included |
| **DM Mono** | `--lf-font-mono` | Figures, identifiers, paths, and anything read as data |

Bricolage Grotesque is geometric enough to read technical and round enough to
read friendly, which is right for a marketing headline and loud over a screen of controls.
Golos Text carries the interface at small sizes; DM Mono keeps columns of
numbers aligned and makes an identifier look like one.

The wordmark is not set in any of the three: it is drawn in pixel cells with the
mark, and ships only as the SVGs under `assets/logo/`
([logo usage](logo-usage.md)). Product surfaces reach for Bricolage Grotesque
through `--lf-font-display` and nothing else.

| Role | Token | Weight | Tracking |
| --- | --- | --- | --- |
| Display | `--lf-size-display-xl` | 800 | -0.045em |
| Section heading | `--lf-size-display-m` | 700 | -0.04em |
| Body | `--lf-size-body` | 500 | 0 |
| Caption | `--lf-size-caption` | 500 | 0 |
| Eyebrow / label | `--lf-size-eyebrow` | 700 | 0.18em, uppercase |

Self-hosted, never the Google Fonts CDN — no lemonfiber surface loads an asset
from a third party at runtime:

```console
npm install @fontsource-variable/bricolage-grotesque
```

```ts
import "@fontsource-variable/bricolage-grotesque";
```

All three faces are SIL Open Font License. This repository carries no font
binaries: a surface installs the packages it needs and serves them itself.

## The wordmark

The wordmark is always lowercase, always one word, "fiber" always in amber except in one-colour reproduction. It is pixel cells drawn by `scripts/logo.py`, not live text: never re-set it in a text field or a typeface. If you need a size or colour pairing that does not exist, add it to the generator rather than restyling text.
