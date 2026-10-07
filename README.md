<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/lockup-horizontal-on-ink.svg">
    <img alt="lemonfiber" src="assets/logo/lockup-horizontal.svg" height="72">
  </picture>
</p>

<h1 align="center">Lemonfiber &mdash; brand</h1>

<p align="center">
  The logo, colours and type of lemonfiber, a self-hosted media stack. Take
  assets and design tokens from here rather than re-drawing or re-exporting them.
</p>

<p align="center">
  <a href="https://github.com/lemonfiber/brand/actions/workflows/tokens.yml"><img alt="tokens" src="https://github.com/lemonfiber/brand/actions/workflows/tokens.yml/badge.svg"></a>
  <a href="https://scorecard.dev/viewer/?uri=github.com/lemonfiber/brand"><img alt="OpenSSF Scorecard" src="https://api.scorecard.dev/projects/github.com/lemonfiber/brand/badge"></a>
</p>

---

## Licence — read this first

This repo is **split**:

| Path | Licence |
|------|---------|
| `assets/logo/*` | **Proprietary — all rights reserved** ([LICENSE](LICENSE)) |
| `tokens/*` | Hippocratic 3.0 ([LICENSE-tokens](LICENSE-tokens)) |
| `.docs/*` | CC BY-SA 4.0 |

The **marks are protected**: you may build on the code and use the tokens, but
you may not ship a fork under the lemonfiber name or logo. Rust, Mozilla and
Python protect their identities the same way. See the
[rationale](https://github.com/lemonfiber/spec/blob/main/90-appendix/license-rationale.md).

## Structure

```
assets/logo/   SVG marks (primary, mono, crops, lockups) — proprietary
  export/      PNG renders of the marks where a platform asks for them — proprietary
tokens/        colour / type / space tokens (CSS custom props + JSON) — open
.docs/         usage: logo, colour, typography, contact sheet
```

## Quick start

```html
<link rel="stylesheet" href="tokens/tokens.css">
<img src="assets/logo/lockup-horizontal.svg" alt="lemonfiber" height="48">
```

Or as a package. It is not published to a registry — `lemonfiber-web`
installs it straight from this repo, pinned to a commit:

```console
npm install github:lemonfiber/brand#<commit-sha>
```

```css
@import "@lemonfiber/brand/tokens.css";
.header { background: var(--lf-color-paper); color: var(--lf-color-ink); }
```

For the dark theme, set `data-lf-theme="ink"` on the root element: the colour
tokens then hold the dark values under the same names.

The type tokens name three typefaces, Bricolage Grotesque, Golos Text and DM
Mono, with system fallbacks. This repository does not ship the font files;
[`.docs/typography.md`](.docs/typography.md) says where to get them.

## The rules, briefly

Never re-colour the mark outside the token palette, never add a tagline, never
stretch or rotate the lockups. **Amber is a signal colour, never a background fill
or body text** — it fails contrast as text (which is why the brand forbids it).
Full rules in [`.docs/logo-usage.md`](.docs/logo-usage.md); the binding
constraints and the accessibility contract are in the spec's
[60-brand](https://github.com/lemonfiber/spec/tree/main/60-brand).

## Accessibility is checked

Body-text colour pairings are verified against WCAG AA in CI
(`scripts/check_tokens.py`). A token change that puts a failing pairing into body
use is a contract violation, not a preference. See spec
[60-brand/accessibility.md](https://github.com/lemonfiber/spec/blob/main/60-brand/accessibility.md).

## Contributing and security

Read the [contributing guide](https://github.com/lemonfiber/spec/blob/main/50-governance/contributing.md)
before opening a pull request. A change within the rules above is routine; a
change to what the rules allow is a change to the specification's
[brand rules](https://github.com/lemonfiber/spec/tree/main/60-brand) first.
Report a vulnerability as the
[security policy](https://github.com/lemonfiber/.github/blob/main/SECURITY.md)
describes, not in a public issue.

What changed in each release is in [CHANGELOG.md](CHANGELOG.md).

---

<p align="center">
  <a href="https://nightworks.io">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset=".github/nightworks-white.png">
      <img alt="NightWorks.io" src=".github/nightworks-dark.png" height="20">
    </picture>
  </a>
  &nbsp;&middot;&nbsp;<a href="https://discord.nightworks.io"><img alt="Discord" src=".github/discord.svg" height="20"></a>
</p>
