# Monday reveal

Production `main` keeps the Coming Soon page until the reveal. Do not merge `fellowship/v1-site` into `main` before the time below. The Coming Soon poll lives on its own branch, `fellowship/reveal-handoff`, because the public page has to learn how to look for V1 before V1 replaces it.

The V1 build contains `/release.json`:

```json
{
  "name": "TechGnomo",
  "release": "v1"
}
```

That file is not on `main` today. The countdown page cannot see V1 until GitHub Pages has finished rebuilding after the merge.

## When to merge V1

The countdown hits zero at `2026-09-27T23:00:00Z` (Monday 28 September 2026, 9:00 AM Brisbane, AEST, no daylight saving).

Recent GitHub Pages deployments for this repository, from the Pages builds API:

- The latest success is the Coming Soon deploy, commit `36d22bb` (merge of `fellowship/coming-soon`). It was created `2026-09-26T22:04:30Z` and updated `2026-09-26T22:05:40Z`: **71 seconds**.
- Of the other successful builds on record, 21 of 24 finished in **30 to 90 seconds**. The median is 44 seconds.
- Three ran longer: 105 seconds, 90 seconds is inside the band, and the longest success is commit `f5353ce` at **3 minutes 51 seconds** (231 seconds). A 1.5 second “built” row was ignored; it is not a real publish.

**Merge `fellowship/v1-site` into `main` at 8:58 AM Brisbane.** A build that takes the latest measured 71 seconds then finishes at 8:59, and one in the usual 30–90 second band finishes between 8:58 and 8:59. That is about 9:00. The countdown page does not poll until zero, so a build that finishes a minute early does not open the workshop early.

If a build runs as long as the longest recent success (3 minutes 51 seconds), an 8:58 merge finishes about 9:02. The poll below starts at 9:00 and keeps looking, and the refresh button still works.

## Coming Soon poll

The poll has to live in the Coming Soon page that is already public. Putting it in V1’s home page is too late: by the time V1 is served, the countdown page is gone. `fellowship/v1-site` does not change `main`. The change is the open pull request from `fellowship/reveal-handoff` into `main`. Merge that first, long enough before 8:58 that its own Pages build (about a minute) is done, and do not merge it on Monday morning in the same minute as V1.

### `assets/js/holding.js` on main

`lookForRelease()` is called from `showLive()` only. `showLive()` runs when `tick()` finds the countdown at or past zero, including a visit that loads after zero. It is not called on a page load while time is still left. `/release.json` is cache-busted. The refresh button stays, so a failed check still has a way through.

```js
var looking = false;

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

function showLive() {
  clock.hidden = true;
  opens.hidden = true;
  hint.hidden = false;
  line.textContent = "The workshop is open.";
  line.classList.add("is-open");
  sr.textContent = "The workshop is open. Refresh the page.";
  if (timer) {
    clearTimeout(timer);
    timer = 0;
  }
  if (!looking) {
    looking = true;
    lookForRelease();
  }
}
```

`reduced` is already defined in that file. `replace("/")` loads the new home once Pages is serving V1. Until `release.json` exists, the request 404s and the countdown page stays, with “Refresh the page” still there.

### `assets/css/holding.css` on main

```css
.plate.is-revealing {
  opacity: 0;
  transition: opacity 700ms var(--ease-out);
}
```

The script skips the fade when reduced motion is on, and navigates immediately. The existing reduced-motion block already sets `transition: none`.

### `index.html` on main

Cache-bust the holding script so a hard refresh after this change picks up the poll:

```html
<script src="/assets/js/holding.js?v=20260928"></script>
```

The noscript line is a real link, not only a sentence:

```html
<noscript>
  <p class="noscript"><a href="/">TechGnomo</a>. Opens Monday, 9:00 AM Brisbane. The countdown needs JavaScript.</p>
</noscript>
```

`/` is this same page until the V1 rebuild. After the rebuild it is the V1 home. No loop.

## If the Coming Soon page is not patched

At 9:00 the public page still says “The workshop is open. Refresh the page.” A refresh after the Pages rebuild shows V1. There is no automatic fade.
