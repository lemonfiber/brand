# Typography

Three faces, each with one job.

| Face | Token | Sets |
| --- | --- | --- |
| **Bricolage Grotesque** | `--lf-font-display` | The wordmark, and display headings on marketing surfaces |
| **Golos Text** | `--lf-font-body` | Interface text — every product surface, headings included |
| **DM Mono** | `--lf-font-mono` | Figures, identifiers, paths, and anything read as data |

Bricolage Grotesque is geometric enough to read technical and round enough to
read friendly, which is right for a wordmark and loud over a screen of controls.
Golos Text carries the interface at small sizes; DM Mono keeps columns of
numbers aligned and makes an identifier look like one.

**The wordmark is set only in Bricolage Grotesque ExtraBold (800)**, and never
re-typeset from its outlined form. Product surfaces reach for it through
`--lf-font-display` and nothing else.

| Role | Token | Weight | Tracking |
| --- | --- | --- | --- |
| Wordmark / display | `--lf-size-display-xl` | 800 | -0.045em |
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

The wordmark is always lowercase, always one word, "fiber" always in a second colour except in one-colour reproduction.

## Wordmark files

Wordmark and lockup SVGs are outlined vectors, not live text. Do not re-set the wordmark in a text field — scale the SVG instead. If you need a size or colour pairing that does not exist, add an export rather than restyling text.
