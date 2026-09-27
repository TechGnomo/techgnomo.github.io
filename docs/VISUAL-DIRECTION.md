# TechGnomo visual direction

Proposal for review. The live pages are unchanged. Working prototypes: `/prototype/`, `/prototype/home/`, `/prototype/news/`. They are `noindex` and are not linked from the public navigation.

## 1. Brand concept

TechGnomo is a lit test bench where digital products are built, broken, and shipped: cool metal, hard frames, one signal colour, and the product under test sitting in its own skin.

“Workshop” here means prototype, build, test, break, fix, ship. It does not mean paper, craft, or a magazine.

## 2. Typography

Two families. No serif. Fraunces was the voice of the rejected system, so a serif does not come back as an accent.

**Schibsted Grotesk** (SIL OFL, variable, Latin subset, about 46KB) is the voice: names, titles, navigation, and body. It was cut for dense reading and runs to a heavy weight, so a headline can be large without turning into fashion type. It is not Inter, Geist, or Space Grotesk, which would make the lab look like a default software advert. File: `/assets/fonts/schibsted-grotesk-latin.woff2`. `font-display: swap`.

**DM Mono** (SIL OFL, one weight, Latin subset, about 15KB) is only for timestamps, status, build numbers, coordinates, and short labels. It is geometric and quiet. It is not JetBrains Mono, so the page does not dress as an IDE. File: `/assets/fonts/dm-mono-latin.woff2`.

Fallbacks are size-adjusted to the webfont’s Latin average width and vertical metrics (`size-adjust`, `ascent-override`, `descent-override`, `line-gap-override`) against Arial for the grotesque and Courier New for the mono, with Liberation Sans / Liberation Mono as the same-metric locals. Body copy stays at weight 400, which is the instance the fallback was matched to, so a swap should not reflow a paragraph.

| Use | Family | Size | Weight | Leading |
| --- | --- | --- | --- | --- |
| Name on the home hero | Schibsted Grotesk | `clamp(2.5rem, 14vw, 3.5rem)`, up to `6.25rem` on a wide screen | 820 | 0.92 |
| Page title, such as Feed | Schibsted Grotesk | `clamp(2.2rem, 8vw, 3.25rem)` | 820 | 0.92 |
| Section title | Schibsted Grotesk | 1.35rem | 750 | 1.15 |
| Body | Schibsted Grotesk | 1.0625rem | 400 | 1.45 |
| Navigation, product names in the feed | Schibsted Grotesk | 0.9375rem | 600–700 | 1.35 |
| Time, status, build, coordinates, labels | DM Mono | 0.8125rem | 400 | 1.35 |

Large type is left-aligned and tightly fitted, not letterspaced capitals. Mono is not used for sentences.

## 3. Colour

One light theme. ClearMoneyPath already owns a dark navy; a second dark theme would blur that handover and slide toward a generic dark product site. Cream and brown are not kept.

The signal is one hex, a magenta, used for navigation state, status labels, links, focus, the live lamp, rig corners, and the rig’s hover edge. It is not a page wash. It is not ClearMoneyPath blue `#2D7BFF`, and it is not the old sealing wax `#7E3424`.

| Token | Hex | Use |
| --- | --- | --- |
| `--bench` | `#E3E6EC` | Page ground. Cool, slightly blue-grey. |
| `--panel` | `#F6F7F9` | Header, post surface, modules. |
| `--ink` | `#14171C` | Primary text. Frames around objects. |
| `--soft` | `#2A3140` | Supporting sentences. |
| `--meta` | `#3E4656` | Timestamps, handles, quiet labels. |
| `--line` | `#C5CAD3` | Edges inside a framed object. |
| `--signal` | `#BA0068` | The TechGnomo mark of state. |

Contrast, WCAG 2.1:

| Pair | Ratio |
| --- | --- |
| Ink on bench | 14.4:1 |
| Ink on panel | 16.8:1 |
| Soft on bench | 10.4:1 |
| Soft on panel | 12.2:1 |
| Meta on bench | 7.6:1 |
| Meta on panel | 8.8:1 |
| Signal on bench | 5.1:1 |
| Signal on panel | 6.0:1 |
| White `#FFFFFF` on signal | 6.4:1 |

Signal clears AA for small text and for interface marks (the 3:1 graphic threshold). Do not set ink text on a signal fill: that pair is about 3.1:1. A filled control uses white on signal. Focus is a 2px signal outline.

Inside a ClearMoneyPath frame only, the product colours stay `#06101E`, `#101827`, `#F7FAFF`, `#8292A8`, `#2D7BFF`. Those ratios are unchanged from `DESIGN.md` (ink 18.2:1 on the navy, accent 4.9:1).

## 4. Homepage

The first screen is a bench readout, not a poster.

A sticky bar (below). Then a system line, `TG-LAB`, `BRISBANE`, `OPEN`, with a signal lamp. The name is set large, left aligned, in the grotesque. One sentence says what this is: a lab for software, tools, and experiments.

The object on the bench is **the rig**: a hard ink frame, signal corner ticks, a faint coordinate grid, and a monospace readout (`WINDOW`, `X 16` `Y 42`). Inside the frame, ClearMoneyPath’s own screenshot sits on `#06101E` with the app’s 22px radius. The caption is the public status, “Coming in 3 weeks”, plus the summary from `data/products.json`. On a phone this stack fits the first view: name, sentence, product in a test frame. On a wide screen the type and the rig sit side by side.

Below that, in the same content model as now: what we build (products, experiments, tools), why (one problem, then it ships; products need not look alike), the three newest posts, and what’s next (ClearMoneyPath in 3 weeks; nothing else announced).

`BUILD 001` in the bar is the one dry line. It is not repeated.

## 5. News

The page is a feed. The title is **Feed**. It is not “The log”.

A post is a social post with a build status, not a diary entry:

- The gnome mark in a small square, as the avatar.
- Byline: `TechGnomo` in the grotesque, then `@techgnomo` and a short Brisbane time in mono, for example `27 Sep · 1:52 pm`. The time is the permalink. A date-only post shows the day and no clock, as `NEWS.md` already requires.
- A status in mono brackets, in the signal colour: `[ SHIPPING ]`, `[ TEASER ]`, `[ UPDATE ]`. The word is the status. Colour is not the only cue.
- The post text, unchanged.
- When the post names an announced product, `ClearMoneyPath` links to `/products/clearmoneypath/`, with a small navy-and-blue swatch so the product peeks through. The surrounding page stays the bench.
- A Share control (system share sheet, or copy the permalink). Without JavaScript the time link still works.

Home shows the three newest posts and links to the full feed. The prototype prints only the five posts in `data/news.json`, newest first, including the noon-Brisbane sort for the date-only fix note. No posts were invented. The rent bug stays `[ UPDATE ]`, which is the status stored on that post.

Examples Fabio suggested, shown here only, not as posts and not in the prototype except `BUILD 001`:

- Status style: `[ FIXED ]`, `[ TEASER ]`, `[ SHIPPING ]`, `[ UPDATE ]`, `[ BUILDING ]`.
- Spare lines: `SHIPPED`, `CURRENTLY BREAKING`, `FIXED`, `PROBABLY`, `IT WORKED ON MY MACHINE`.

`[ FIXED ]` would suit the rent-bug post if that status is added to the renderer’s enum later. It is not added in this proposal, so the published log and `data/news.json` stay as they are.

The live route remains `/news/`. “Feed” is the title and the prototype label.

## 6. Products

A product is an object leaving the bench, not a pricing card.

The page around it stays TechGnomo: bench, grotesque, signal, mono labels. Each preview is a rig, a window into that product’s own world. ClearMoneyPath’s window uses its navy, its blue, its screenshot, and its “Coming in 3 weeks” line. A future product would get the same frame and a different interior, taken from its own theme file. Unannounced work does not get a window. GnomoRestaurant stays an empty theme.

The catalogue is a short row of those objects, plus the same “nothing else is announced” line. It is not a grid of equal marketing cards.

## 7. Navigation and header

A sticky bar on the bench panel, with a 2px ink edge under it. Not a centred wordmark, not a hidden menu.

Left: the mark and TechGnomo, in the grotesque. Middle, on a wide screen: `BUILD 001` and the lamp. Right: About, Feed, Products, always visible, because there are three links. The current item is signal, with a 2px signal underline. On a phone the links wrap onto a second row; they are not behind a button.

About and Products in the prototype point at the live pages, which are not restyled. Feed points at the prototype. The public labels can stay About, News, Products when this is approved; the route for news stays `/news/`.

The footer keeps Studio, Lab, Fabio, Contact, Privacy, the Brisbane line, and the email.

## 8. Motion

Fast and local. Nothing loops for attention, nothing fades in slowly, no parallax, no page transition.

- The rig arrives once, 220ms, 8px and opacity. Transform and opacity only, so it does not move layout.
- The lamp blinks once, 900ms.
- Hover on a fine pointer turns the rig’s border signal in 120ms, and the coordinate readout follows the pointer. The digits sit in a monospace pair (`X 00` `Y 00`) so the line does not grow. Touch scrolling does not chase the finger.
- Pressing the rig turns the same border signal, so a phone gets the state without hover.
- Share confirms by changing its label to “Copied”.
- A permalink target draws a signal outline. Instant, not a fade.

`prefers-reduced-motion: reduce` removes the arrival, the blink, and the colour transition. The rig is visible immediately. Coordinates stay at their resting values. Focus outlines remain.

## 9. Handing over to ClearMoneyPath

The transition engine stays: `data-product`, `data-stage` (`parent`, `approach`, `crossover`, `product`), `product-transition.css`, `product-transition.js`, and `themes/clearmoneypath.css`. This proposal does not edit them. When the direction is approved, only the parent values and the field stops change.

The opening of `/products/clearmoneypath/` is still the bench: Schibsted Grotesk, DM Mono for labels, ink on `#E3E6EC`, signal for links and focus. The header stays the parent bar. Its veil becomes 90% bench instead of 90% paper, so the field can tint it.

The field is the same OKLCH gradient, retuned off the warm sand and onto a cool path from the bench to the navy. Parent text stays on the light stops. The middle, where neither ink would pass, stays behind the screenshots. Light product text starts once the field has reached the navy. Signal magenta does not enter `data-stage="product"`. ClearMoneyPath blue `#2D7BFF` remains that world’s accent. The product chapter keeps the system UI stack. Type does not swap live with the scroll.

Proposed stops, and contrast of parent meta `#3E4656` or product ink `#F7FAFF`:

| Stop | Hex | What holds |
| --- | --- | --- |
| Bench | `#E3E6EC` | Parent meta 7.6:1 |
| `--field-a` | `#D3D7DF` | Parent meta 6.6:1 |
| `--field-b` | `#C3C8D1` | Parent meta 5.6:1. Last stop for parent sentences. |
| `--field-pass` | `#AEB3BC` | Near-neutral. Not a text stop. |
| `--field-pass-cool` | `#969BA4` | Behind the screenshots. |
| `--field-c` | `#4E5E76` | Behind the screenshots. Product ink 6.3:1. |
| `--field-d` | `#1A2B42` | Last step before the navy. Product ink 13.7:1. |
| Surface | `#06101E` | Product chapter. Unchanged. |

The footer returns along the bottom of that gradient to the bench, the mark, and the lab links. The brass sill does not return. The line “A TechGnomo product” stays.

The home rig is the short version of the same idea: TechGnomo frames the object; the object is already ClearMoneyPath.

## 10. What changes, what stays

Changes, and only inside this proposal and the prototypes:

- Ground, type, and accent. Cream `#F1EADC`, Fraunces, Source Sans 3 as the UI voice, sealing wax `#7E3424`, and brass `#8A5E32` are retired as the parent identity.
- The centred poster hero, the slow rise, the hairline fashion rules, and the brass sill.
- News stops being an editorial log. The title becomes Feed. Posts gain a handle, a short time, bracket status, a product reference, and share.
- Homepage becomes the rig: a product under test, with system labels and one build number.
- Motion becomes short state changes. `BUILD 001` is the single joke.

Stays:

- Routes, `data/news.json`, `data/products.json`, and `tools/render_site.py`. No new posts. The rent note is still `UPDATE`.
- Product status values and the public line “Coming in 3 weeks”.
- ClearMoneyPath colours, type stack, screenshots, and theme file, until the field stops above are approved.
- The transition engine’s behaviour and files.
- The mark at `/assets/brand/mark.svg`.
- Accessibility basics (skip link, focus, reduced motion, labelled controls), self-hosted fonts, no analytics.
- Privacy, contact, and the rest of the footer.
- `release.json` and `REVEAL.md`.
- `DESIGN.md`, until this direction replaces it. The live CSS still follows that file.
- `main`, secrets, Pages, deploy settings, and `CNAME`. Not touched.

The prototypes load `/assets/css/prototype.css` and `/assets/js/prototype.js` only. They are absent from the sitemap and from the live header.
