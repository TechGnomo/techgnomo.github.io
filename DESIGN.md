# TechGnomo design foundations

Shared by the launch door (`fellowship/coming-soon`) and the V1 site. The door is the first use of this system: a closed workshop before opening morning. V1 should feel like the same room with the door open, not a second brand.

Tokens live in `/assets/css/tokens.css`. Components use the semantic names (`--surface`, `--ink`, `--accent`, and the rest listed under Semantic tokens). The primitive names (`--color-paper`, `--color-ink`, …) keep the values the launch door and V1 already ship; do not change those values. The maker's mark is `/assets/brand/mark.svg`. Fonts are self-hosted under `/assets/fonts/` (SIL Open Font License; see the OFL files beside them). No third-party font host, no analytics.

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

## Semantic tokens

Components in `/assets/css/site.css` read semantic tokens. The primitives above are unchanged, and each semantic token is an alias of one primitive, so a page that is not a product transition renders the same workshop.

| Semantic | Alias of | Role |
| --- | --- | --- |
| `--surface` | `--color-paper` | Page ground. |
| `--surface-inset` | `--color-paper-deep` | Second surface: a bench, a field, a quiet inset. |
| `--ink` | `--color-ink` | Primary text. |
| `--ink-soft` | `--color-ink-soft` | The sentence under a title. |
| `--ink-faint` | `--color-ink-faint` | Labels, captions, meta. |
| `--accent` | `--color-seal` | Rare emphasis, focus, and the mark. Must stay WCAG AA on `--surface` and `--surface-inset`. |
| `--warm` | `--color-brass` | The sill, and one warm line. |
| `--rule` | `--color-line` | Hairlines. |
| `--font-display` | (unchanged) | Names and titles. Fraunces. |
| `--font-body` | `--font-text` | Navigation, body, forms. Source Sans 3. |
| `--radius` | `--radius-sm` | The default control corner. |
| `--space-*` | (unchanged) | The 4px scale, including `--space-page`. |
| `--motion-ease` | `--ease-out` | Arrival and state changes. |
| `--motion-quick`, `--motion-calm`, `--motion-slow` | the three durations | |

Do not point a semantic token at a new hex on `:root`. A product overrides the semantic tokens inside its own stages.

## Product transition

TechGnomo is the parent. A product page may leave that room as the reader scrolls, and come back to it in the footer. The mechanism is shared. A new product does not edit it.

Files:

- `/assets/css/site.css` — the stage frame (padding and the centred measure). It is in the first paint, so the opening does not move when the colour arrives.
- `/assets/css/product-transition.css` — the safe mix, the pay-cycle rail, and the scroll-driven `--shift`.
- `/assets/css/themes/<product>.css` — that product's destination values for the same semantic roles.
- `/assets/js/product-transition.js` — loads the transition stylesheet, the theme (`data-product-theme`) and any product faces (`data-product-fonts`) on the first scroll, a jump to a hash, or shortly after load. Those files stay off the first paint so they do not compete with Fraunces and Source Sans. If the browser cannot do `animation-timeline: view()` and the reader has not asked for reduced motion, the same file sets `--shift` from an `IntersectionObserver`. The observer reads the entry's own geometry. It does not measure the page on scroll.

Chapters are marked in order:

| `data-stage` | Where it rests | What the reader should feel |
| --- | --- | --- |
| `parent` | `--shift: 0` | Still TechGnomo. Type, colour, header. |
| `approach` | `0.18` | The ground cools. Easy to feel, easy to miss. |
| `crossover` | `0.46` | Both are present. Product headings, parent body, the product's graphic, the parent's ink. |
| `product` | `1` | The product's own world. |

`body` carries `data-product="<slug>"`. The header, the footer and the brass sill stay on the parent tokens. With motion allowed, each stage eases `--shift` as it enters the viewport (`animation-timeline: view()`), then holds. Only colour is eased, through custom properties. Type, radius and the rail are set per stage, not scrubbed, so the layout does not move.

`prefers-reduced-motion: reduce` turns those animations off. Each stage shows the resting state in the table. Same destinations, no scroll-linked change. Without JavaScript the page does the same, because the resting states are in CSS.

### Why the mix is not a straight line

Cream paper with dark ink and a navy ground with light ink cannot be blended in one smooth ramp. Around the middle gray, every text colour fails WCAG AA. The shared CSS therefore keeps two legal bands:

- Light chapters mix the ground only as far as `--m: 0.36` (still dark text). Faint, soft and accent darken toward the parent ink as the ground cools, so they do not wash out.
- The product chapter starts at `--m: 0.56`, where light text is already safe, and eases to the theme's own colours.

The step between those bands is the chapter turn into the product. It is deliberate. Do not "smooth" `--m` through `0.36`–`0.56`.

## Add a product

1. Derive the palette, type and components from the real product. Do not invent a second brand, and do not add a theme for a product that has no build yet.
2. Add `/assets/css/themes/<slug>.css`. On `[data-product="<slug>"]`, set `--theme-surface`, `--theme-surface-inset`, `--theme-ink`, `--theme-ink-soft`, `--theme-ink-faint`, `--theme-accent`, `--theme-rule`, `--theme-warm`, `--accent-fill` and `--font-product`. Record where each value came from.
3. Self-host at most two extra font files (woff2, subset). No third-party font request. Confirm `--theme-ink`, `--theme-ink-soft`, `--theme-ink-faint` and `--theme-accent` are at least 4.5:1 on both `--theme-surface` and `--theme-surface-inset`.
4. On that page only, link `tokens.css` and `site.css`. Set `data-product`, `data-product-theme` and, when the product has its own files, `data-product-fonts` on `body`. Include `product-transition.js`. In `<noscript>`, link `product-transition.css`, the theme and the font file, so the page is complete with JavaScript off. Mark the chapters `data-stage="parent"`, then `approach`, `crossover`, and `product`, in that order. One `product` wrapper may hold several sections. If the theme changes a component's size, put that box model in a short style block on the page so the first paint already has it.
5. Keep the line "A TechGnomo product" (or the same attribution). Keep the header on the parent. Leave the copy, status and legal lines as they are.
6. Check contrast at the top, at 25%, 50%, 75% and the main action, including the colours between the resting stages. Check reduced motion, JavaScript off, and that other pages did not change.

GnomoRestaurant is the empty slot: `/assets/css/themes/gnomorestaurant.css` is comments only, and the page does not link it.

## ClearMoneyPath

The Android beta is the source. `https://github.com/TechGnomo/ClearMoneyPath` is not public (the page says so, and the remote returns 404), including `fellowship/web-mvp` and `main`. There is no theme file to quote. Every colour below was measured on the screenshots already published at `/assets/img/cmp-home.webp`, `cmp-money.webp`, `cmp-debts.webp` and `cmp-plan.webp`. Flat fills were counted as exact pixels, not sampled by eye.

The web identity is that UI, set for a long page: a navy ground, cards a step lighter, near-white text, one blue, and a pay-cycle rail (a line from payday to payday with a mark for now). The rail is the page's motif. It is CSS, it does not take space, and it appears from the crossover on.

| Token | Value | Provenance |
| --- | --- | --- |
| `--theme-surface` | `#07101f` | Screen ground. Exact fill, 81,807 pixels on `cmp-home.webp`, and the same navy at the edges of the other three shots. |
| `--theme-surface-inset` | `#111727` | Cards. Most common exact colour on `cmp-home.webp` (121,941 pixels). |
| `--theme-ink` | `#f4faff` | Near-white figures. The mode of the light text is `#ffffff`; `#f4faff` is the cool white clustered on the home hero (y 199–238). |
| `--theme-ink-soft` | `#d5deea` | Secondary text. Small labels on `cmp-home.webp` antialias through `#a5b9c9`–`#c4d8ea`. This token stays in that cool gray, light enough for paragraphs. |
| `--theme-ink-faint` | `#75849a` | Meta text. `cmp-plan.webp` holds a flat `#64748c` (3,459 pixels in the lower band; Tailwind slate-500, the inactive track). `#64748c` is 4.01:1 on `#07101f` and 3.76:1 on `#111727`, short of AA for small text. `#75849a` is that track moved toward `#f4faff` until it clears 5.0:1 on the ground and 4.7:1 on the card. |
| `--accent-fill` | `#2d7cfe` | The app's blue. Exact mode of the saturated pixels (6,675 on `cmp-money.webp`): progress, selected tab. Used for the rail and for selection, not for small text. |
| `--theme-accent` | `#3480fe` | The same blue, 3% toward `#f4faff`. `#2d7cfe` is 4.61:1 on the card, legal but tight once the ground is still easing. The text accent keeps a margin on both surfaces. |
| `--theme-rule` | `#30445f` | Hairline for the dark UI. Not a flat fill in the shots; the cards meet the ground with no separate stroke. Mixed so a rule remains visible on `#07101f` without becoming a second accent. |
| `--font-product` | Roboto 400 and 500 | The shots are the Android beta. React Native's default face there is Roboto. A custom font file could not be checked. Two self-hosted Latin woff2 files, about 22KB each (`/assets/fonts/roboto-latin-400-normal.woff2`, `roboto-latin-500-normal.woff2`, OFL). The faces arrive with the theme, on the first scroll or shortly after load (`data-product-fonts`), so they do not compete with Fraunces and Source Sans. Without JavaScript the same file is linked from `noscript`. |
| Corners | 16px cards, 12px fields | Card corners on `cmp-money.webp` ease in over about 28 bitmap pixels on a 540-wide shot, roughly a 16px web corner. Not pills. |
| Rail | payday, now, payday | The shots use horizontal progress fills in `#2d7cfe`. The page turns that into one cycle line. |

Parent Fraunces and Source Sans 3 stay through the top and the approach. At the crossover, headings switch to Roboto and the body stays Source Sans. In the product chapter both are Roboto. Type is not scrubbed with the scroll: a live font swap would move the line lengths.

Spacing stays on the parent scale. Changing it as you scroll would move the layout.

On `/products/clearmoneypath/`:

- Header and the opening (the "A TechGnomo product" line, the name, the beta status) are parent.
- "The problem" is the approach.
- "Screens with sample data" is the crossover. The shots themselves sit on `#07101f`, so the app is already in the room while the page is still between the two. Their box and ground are repeated in a short style block in the page head, the same rules as the theme, so they do not change size when the theme file arrives.
- "What this beta does", the sketch, and "What it is not" are the product world. The sketch is the action on this page.
- The footer returns to the parent: the mark, the workshop links and the brass sill are the frame the header never left. The visit ends in the workshop. A hairline separates that frame from the product chapter.

Copy, the beta status, "General information only, not personal financial advice.", "Left this cycle" / "Short this cycle", and the schema are unchanged. No FinanceApplication. No new claims.
