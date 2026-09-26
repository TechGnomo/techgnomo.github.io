# TechGnomo design foundations

Shared by the launch door (`fellowship/coming-soon`) and the V1 site. The door is the first use of this system: a closed workshop before opening morning. V1 should feel like the same room with the door open, not a second brand.

Tokens live in `/assets/css/tokens.css`. The maker's mark is `/assets/brand/mark.svg`. Fonts are self-hosted under `/assets/fonts/` (SIL Open Font License; see the OFL files beside them). No third-party font host, no analytics.

## Palette

Warm plaster and ink. Not white, not near-black, not neon.

| Token | Value | Use |
| --- | --- | --- |
| `--color-paper` | `#f1eadc` | Page ground. The default surface. |
| `--color-paper-deep` | `#e6dccb` | A second surface: a bench, a drawer, a quiet inset. Not a card grid. |
| `--color-ink` | `#1e1a16` | Primary text. Warm near-black. |
| `--color-ink-soft` | `#3f3832` | The sentence under a title. Still clearly readable. |
| `--color-ink-faint` | `#5c534c` | Labels, footer, meta. About 6:1 on paper. |
| `--color-seal` | `#7e3424` | Sealing wax. The mark, and rare emphasis. Not a link colour everywhere. |
| `--color-brass` | `#8a5e32` | One warm line. On the door it is the light under the sill. |
| `--color-line` | `#ddd2c3` | Hairlines, rules, dividers. |

Contrast pairs checked against paper: ink 14.4:1, ink-soft 9.6:1, ink-faint 6.3:1, seal 7.3:1.

Do not add a lime, a purple, or a pure black. Do not put type on brass. One accent in a view is enough.

## Type

Two families.

**Fraunces** (`--font-display`) is the voice: names, titles, the one sentence that matters, and any numeral that should feel set rather than widget-like. It is a variable font with optical size (`opsz` 9–144) and weight (`wght` 100–900). Leave `SOFT` and `WONK` at 0 — softness and wonk turn the mark of the workshop into a costume. Italic is for a single line, not for labels.

Do not set `opsz` to 144 for a word that is under about 120px. At that optical size the H crossbar is a hairline and "TECHGNOMO" reads as "TECIIGNOMO". The door uses `opsz` 12 and weight 650 at phone size, and `opsz` 32 and weight 560 on a large screen, with `font-optical-sizing: none` so the browser does not push the axis back up. This cut of Fraunces has no `lnum` or `tnum` glyphs (figures are proportional and sit on the baseline). Where digits must not shift as they tick, put each digit in a fixed `1ch` cell. Source Sans 3 does have real tabular lining figures for UI.

**Source Sans 3** (`--font-text`) is the apparatus: navigation, labels, footer, forms, body copy on V1. Weight 400 for reading, 500–600 for a label that must hold. It has tabular figures when a UI number must not jitter.

| Token | Size | Role |
| --- | --- | --- |
| `--text-xs` | 0.75rem | Rare. Not for sentences. |
| `--text-sm` | 0.8125rem | Footer, figure labels. |
| `--text-md` | 1.0625rem | Body, quiet controls. |
| `--text-lg` | 1.35rem | A short lead. |
| `--text-xl` | 1.75rem | A section title. |
| `--text-2xl` | 2.5rem | A page title inside the site. |
| `--text-display` | clamp(2.85rem, 8vw, 7.15rem) | The door wordmark only. |

Leading: `--leading-tight` 0.96 for the wordmark, `--leading-snug` 1.25 for a short line, `--leading-body` 1.5 for paragraphs. Wordmark tracking is `--tracking-wordmark` (0.05em). Wider tracking plus a hairline H is what made the name unreadable. Do not track body text out into letter-spaced capitals.

The door sets the name in Fraunces roman, uppercase, at the optical sizes above. The sentence under it is Fraunces italic. Countdown figures are Fraunces, one digit per `1ch` cell, with a hairline between units. Labels and the footer are Source Sans 3.

## Spacing

A 4px base, named `--space-1` through `--space-10`: 4, 8, 12, 16, 24, 32, 48, 72, 104, 128 px (as rem). `--space-page` is the page inset, `clamp(1.5rem, 8vw, 7.5rem)`.

Prefer fewer, larger gaps over even padding. The door is a centred stage: the name is large, the mark sits above it, and the paper around it is the quiet. A soft warm light sits behind the type. It is not a left-hand column on a blank page.

## Radii

`--radius-sm` 2px, `--radius-md` 6px, `--radius-lg` 12px. The door uses almost none. V1 should stay closer to cut wood than to pills. No full-round buttons as the default.

## Motion

`--ease-out` is `cubic-bezier(0.16, 1, 0.3, 1)`. Durations: `--duration-quick` 160ms, `--duration-calm` 380ms, `--duration-slow` 880ms.

Motion is a small arrival or a state change, then stillness. The door: the plate rises a few pixels once; a changed countdown figure fades and settles by `0.07em`; the brass sill fades in. Nothing loops. `prefers-reduced-motion: reduce` removes animation. Do not add parallax, cursor glows, or scroll-scrubbed scenes.

## Mark

`/assets/brand/mark.svg` is a filled gnome silhouette: hat, brim, beard. It is a stamp, not an illustration.

Recolor it by inlining the paths with `currentColor`, which stays crisp, or with a CSS mask. Do not redraw it with a face, eyes, or scenery. On the door it is about 3.25rem, large enough to read as a stamp, not a bullet. Clear space around it of at least half its height. It does not sit in a circle, a badge, or a neon tile, and it is not a mascot repeated through the page.

V1 can place it once above a title, or once in the margin or footer.

## The door, specifically

`/assets/css/holding.css` and `/assets/js/holding.js` are the launch page, not the V1 layout. Copy the tokens and the mark. Do not copy the countdown into the finished site.

Visible copy is only: the name, "Something new is taking shape.", "Opens Monday, 9:00 AM", the figures, and "© TechGnomo · Brisbane". At the launch instant the sentence becomes "The workshop is open." and the figures give way to "Refresh the page". The instant is fixed: `2026-09-27T23:00:00Z`.
