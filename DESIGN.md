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
- `/assets/css/product-transition.css` — one page-height field (a gradient, not a colour per chapter), the pay-cycle rail, and the header veil.
- `/assets/css/themes/<product>.css` — that product's destination values, plus the field stops `--field-a` through `--field-d`. A product that needs a hue change on the way to its ground can also set `--field-pass` and `--field-pass-cool`, the near-neutral pair between sand and the dusk.
- `/assets/js/product-transition.js` — loads the transition stylesheet and the theme (`data-product-theme`) on the first scroll, a jump to a hash, or shortly after load. An optional `data-product-fonts` stylesheet loads the same way when a product self-hosts a face. Those files stay off the first paint so they do not compete with Fraunces and Source Sans. If the browser cannot do `animation-timeline: view()` and the reader has not asked for reduced motion, the same file sets `--shift` from an `IntersectionObserver`. The field does not use that value. The observer reads the entry's own geometry. It does not measure the page on scroll.

Chapters are marked in order:

| `data-stage` | Type and ink | What the reader should feel |
| --- | --- | --- |
| `parent` | Parent type, dark ink | Still TechGnomo. The field is paper. |
| `approach` | Parent type, dark ink | The field warms. Easy to feel, easy to miss. |
| `crossover` | Parent type, dark ink, then the product's light ink on the closing line | The app's screens sit in the field while it passes from warm sand into the product ground. |
| `product` | Product type, light ink | The product's own world. |

`body` carries `data-product="<slug>"`. Chapters do not paint their own backgrounds. One gradient on `body::before`, interpolated in OKLCH, runs the height of the page: paper, the theme's field stops, the theme surface, then paper again under the footer. There is no seam between chapters. The header keeps the parent wordmark, nav and mark, and its bar is a 90% paper veil so the field tints it. The footer and the brass sill stay on the parent tokens. The return to paper is the bottom of the same gradient, in the padding under the last chapter.

The rail is the product's graphic. It is faint and short over the crossover, longer at the product chapter, and fully drawn above the sketch. It does not take space. Product type is only on the product chapter, so a font does not reflow the opening.

`prefers-reduced-motion: reduce` changes nothing about the field: it is a gradient, not a scroll animation. The rail simply shows its resting opacity. Without JavaScript the same CSS applies, linked from `noscript`.

### Why the field is not a straight mix

Cream paper with dark ink and a navy ground with light ink cannot be blended under the text. In the middle, neither ink passes WCAG AA. The field still travels that whole way, in OKLCH, through a warm sand and a cool dusk. Where the hue has to leave the sand, two near-neutral stops (`--field-pass`, `--field-pass-cool`) keep the chroma too low to paint a brown or a green middle. The part of the ramp where text would fail sits behind the screenshots, where the only type is on the app cards. Dark ink stays on the field while it is still sand. Light ink starts once the field has reached the theme surface. Do not put a chapter background back on the stages, and do not run the failing part of the ramp under a paragraph.

## Add a product

1. Derive the palette, type and components from the real product. Do not invent a second brand, and do not add a theme for a product that has no build yet.
2. Add `/assets/css/themes/<slug>.css`. On `[data-product="<slug>"]`, set `--theme-surface`, `--theme-surface-inset`, `--theme-ink`, `--theme-ink-soft`, `--theme-ink-faint`, `--theme-accent`, `--theme-rule`, `--theme-warm`, `--accent-fill` and `--font-product`. Set `--field-a` through `--field-d` to the stops between paper and the theme surface. If the hue has to swing, set `--field-pass` and `--field-pass-cool` as a near-neutral pair so the mix does not pick up a strong chroma in between. Record where each value came from. If the chapters sit at very different heights than ClearMoneyPath, adjust the stop positions in `product-transition.css` so the failing middle of the ramp stays behind art, not under paragraphs.
3. Prefer the product's own font stack when it is already on the system. Self-host at most two extra font files (woff2, subset) and only when the product actually ships those files. No third-party font request. Confirm `--theme-ink`, `--theme-ink-soft`, `--theme-ink-faint` and `--theme-accent` are at least 4.5:1 on both `--theme-surface` and `--theme-surface-inset`.
4. On that page only, link `tokens.css` and `site.css`. Set `data-product` and `data-product-theme` on `body`. Set `data-product-fonts` only when a self-hosted face is required. Include `product-transition.js`. In `<noscript>`, link `product-transition.css`, the theme, and the font file when there is one, so the page is complete with JavaScript off. Mark the chapters `data-stage="parent"`, then `approach`, `crossover`, and `product`, in that order. One `product` wrapper may hold several sections. If the theme changes a component's size, put that box model in a short style block on the page so the first paint already has it.
5. Keep the line "A TechGnomo product" (or the same attribution). Keep the header on the parent. Leave the copy, status and legal lines as they are.
6. Check contrast at the top, at 25%, 50%, 75% and the main action, including the colours between the resting stages. Check reduced motion, JavaScript off, and that other pages did not change.

GnomoRestaurant is the empty slot: `/assets/css/themes/gnomorestaurant.css` is comments only, and the page does not link it.

## ClearMoneyPath

The Android beta is the source. Colours and type below are the values the current build paints, from `App.js` at commit `ea19ef9ec0e49fcf3622b6b371fe9456024d50ad`. `App.js` sets no `fontFamily`. Text uses the React Native Web system stack (`SYSTEM_FONT_STACK` in `createReactDOMStyle.js`, applied from `Text`).

The web identity is that UI, set for a long page: the painted page ground, cards a step lighter, the app's own text colours, one blue, and a pay-cycle rail (a line from payday to payday with a mark for now). The rail is the page's motif. It is CSS, it does not take space, and it appears from the crossover on.

| Token | Value | Provenance |
| --- | --- | --- |
| `--theme-surface` | `#06101E` | Painted page and the stage behind it. `appBackgroundDark.backgroundColor` (`App.js` line 4845) and `stage.backgroundColor` (line 4856). |
| `--theme-surface-inset` | `#101827` | Cards, stat tiles, and action cards. `card.backgroundColor` (`App.js` line 4407). |
| `--theme-ink` | `#F7FAFF` | Page titles. `pageTitle.color` (`App.js` line 4296). 18.2:1 on the page, 17.0:1 on the card. |
| `--theme-ink-soft` | `#8292A8` | Explanatory copy. `emptyText.color` (`App.js` line 4442). 6.0:1 on the page, 5.6:1 on the card. |
| `--theme-ink-faint` | `#7F90A8` | Supporting lines. `smallMutedText.color` (`App.js` line 4436). 5.9:1 on the page, 5.5:1 on the card. |
| `--theme-accent`, `--accent-fill` | `#2D7BFF` | Primary buttons, the home tab, and icons. `primaryButton.backgroundColor` (`App.js` line 4510). 4.9:1 on the page, 4.6:1 on the card. The hero fill `#0B203A` (`premiumHero.backgroundColor`, line 4014) is a separate surface; this blue is 4.2:1 there, so the page does not set small accent text on that hero blue. |
| `--theme-rule` | `#1F2D43` | Card hairline. `card.borderColor` (`App.js` line 4412). |
| `--font-product` | system UI stack | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`. The `Roboto` name is the local family on Android, not a file this site serves. No self-hosted product face. |
| Corners | 22px cards, 15px fields | `card.borderRadius` is 22 (`App.js` line 4408). `primaryButton.borderRadius` is 15 (line 4511). The sketch card uses the card radius. |
| Rail | payday, now, payday | Drawn in `#2D7BFF`. Faint over the screens, full above the sketch. |
| `--field-a` | `#efe5d2` | The page's own stop, not a pixel in the app. Paper moved a short way toward the navy, hue kept warm. |
| `--field-b` | `#e2d4bd` | Same path, still light enough for the parent faint ink (the screens introduction). |
| `--field-pass` | `#bfbdb9` | Near-neutral, still warm. Chroma low enough that the next hue change does not paint a brown or a green band. |
| `--field-pass-cool` | `#9b9fa3` | The same near-neutral, hue already with the slate. |
| `--field-c` | `#4c6075` | Cool dusk behind the screenshot row. |
| `--field-d` | `#1d2f44` | The last deep blue before `#06101E`. |

Parent Fraunces and Source Sans 3 stay through the opening, the problem and the screens. The product chapter (what the beta does, the sketch, what it is not) uses the system UI stack. Type is not scrubbed with the scroll: a live font swap would move the line lengths. The sketch figure is weight 700, in the range the app uses for emphasis (`smallMutedText.fontWeight` is 700; titles go heavier).

Spacing stays on the parent scale. Changing it as you scroll would move the layout.

On `/products/clearmoneypath/`:

- Header and the opening (the "A TechGnomo product" line, the name, the beta status) are parent. The header bar is a paper veil, so it warms toward the field instead of staying a solid cream strip.
- "The problem" is the approach. The field has only begun to warm.
- "Screens with sample data" is the crossover. Parent type. The field passes from sand into the cool dusk and then the navy behind the shots. The line under the shots is already the product's light ink, on the navy. The shots themselves sit on `#06101E`, with a 22px card and a `#1F2D43` hairline. That box is repeated in a short style block in the page head, the same rules as the theme, so the cards do not change size when the theme file arrives. The rail is faint here.
- "What this beta does", the sketch, and "What it is not" are the product world, in the system UI stack. The same attribution, "A TechGnomo product", sits above the sketch. The rail is fully drawn there.
- The footer returns to the parent along the bottom of the same field: navy eases back through the cool dusk and the sand in the padding under the last chapter, then the mark, the workshop links and the brass sill. The visit ends in the workshop.

Copy, the beta status, "General information only, not personal financial advice.", "Left this cycle" / "Short this cycle", and the schema are unchanged. No FinanceApplication. No new claims.
