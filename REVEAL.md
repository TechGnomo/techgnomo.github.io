# Monday reveal

Production `main` keeps the Coming Soon page until the reveal. Do not merge this branch into `main` before then.

The V1 build contains `/release.json`:

```json
{
  "name": "TechGnomo",
  "release": "v1"
}
```

That file is not on `main` today. The countdown page cannot see V1 until GitHub Pages has finished rebuilding after the merge.

## What has to change on main before Monday

The poll has to live in the Coming Soon page that is already public. Putting it in V1’s home page is too late: by the time V1 is served, the countdown page is gone. This branch does not change `main`.

At about 8:57 AM Brisbane on Monday 28 September 2026, merge `fellowship/v1-site` into `main`. Pages usually rebuilds in 1 to 3 minutes. The countdown hits zero at `2026-09-27T23:00:00Z` (9:00 AM Brisbane).

### `assets/js/holding.js` on main

Inside `showLive`, after the existing “The workshop is open.” update, start a poll. Leave the refresh button in place so a failed check still has a way through.

```js
function lookForRelease() {
  var url = "/release.json?ts=" + Date.now();
  fetch(url, { cache: "no-store" })
    .then(function (response) {
      if (!response.ok) throw new Error("missing");
      return response.json();
    })
    .then(function (data) {
      if (!data || data.release !== "v1") throw new Error("not-v1");
      var plate = document.getElementById("plate");
      if (reduced) {
        window.location.replace("/");
        return;
      }
      if (plate) plate.classList.add("is-revealing");
      window.setTimeout(function () {
        window.location.replace("/");
      }, 700);
    })
    .catch(function () {
      window.setTimeout(lookForRelease, 4000);
    });
}
lookForRelease();
```

Call `lookForRelease()` at the end of `showLive`. `reduced` is already defined in that file. `replace("/")` loads the new home once Pages is serving V1. Until `release.json` exists, the request 404s and the countdown page stays, with “Refresh the page” still there.

### `assets/css/holding.css` on main

```css
.plate.is-revealing {
  opacity: 0;
  transition: opacity 700ms var(--ease-out);
}

@media (prefers-reduced-motion: reduce) {
  .plate.is-revealing {
    transition: none;
  }
}
```

The script skips the fade when reduced motion is on, and navigates immediately.

### `index.html` on main, for JavaScript off

The noscript line should be a real link, not only a sentence:

```html
<noscript>
  <p class="noscript"><a href="/">TechGnomo</a>. Opens Monday, 9:00 AM Brisbane. The countdown needs JavaScript.</p>
</noscript>
```

`/` is this same page until the rebuild. After the rebuild it is the V1 home. No loop.

## If main is not patched

At 9:00 the public page still says “The workshop is open. Refresh the page.” A refresh after the Pages rebuild shows V1. There is no automatic fade. That is the whole gap.
