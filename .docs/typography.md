# Typography

**Bricolage Grotesque** across the board — geometric enough to read technical, round enough to read friendly.

| Role | Token | Weight | Tracking |
| --- | --- | --- | --- |
| Wordmark / display | `--lf-size-display-xl` | 800 | -0.045em |
| Section heading | `--lf-size-display-m` | 700 | -0.04em |
| Body | `--lf-size-body` | 500 | 0 |
| Caption | `--lf-size-caption` | 500 | 0 |
| Eyebrow / label | `--lf-size-eyebrow` | 700 | 0.18em, uppercase |

```html
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&display=swap" rel="stylesheet">
```

The wordmark is always lowercase, always one word, "fiber" always in a second colour except in one-colour reproduction.

## Wordmark files

Wordmark and lockup SVGs are outlined vectors, not live text. Do not re-set the wordmark in a text field — scale the SVG instead. If you need a size or colour pairing that does not exist, add an export rather than restyling text.
