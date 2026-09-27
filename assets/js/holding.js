(function () {
  var launchEl = document.getElementById("launch");
  var launchIso = launchEl.getAttribute("datetime");
  var launchMs = Date.parse(launchIso);
  document.documentElement.setAttribute("data-launch", launchIso);

  var nodes = ["days", "hours", "mins", "secs"].map(function (id) {
    return document.getElementById(id);
  });
  var clock = document.getElementById("clock");
  var line = document.getElementById("line");
  var opens = document.getElementById("opens");
  var sr = document.getElementById("sr");
  var lastMinute = null;
  var timer = 0;
  var looking = false;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function pad(n) {
    return (n < 10 ? "0" : "") + n;
  }

  function paint(el, value) {
    var next = pad(value);
    if (el.getAttribute("data-value") === next) return;
    var seen = el.getAttribute("data-seen") === "1";
    var cells = el.querySelectorAll(".digit");
    cells[0].textContent = next.charAt(0);
    cells[1].textContent = next.charAt(1);
    el.setAttribute("data-value", next);
    el.setAttribute("data-seen", "1");
    if (!seen || reduced) return;
    el.classList.remove("is-tick");
    void el.offsetWidth;
    el.classList.add("is-tick");
  }

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

  function showHold() {
    clock.hidden = true;
    opens.hidden = true;
    line.textContent = "Nearly there. The workshop opens soon.";
    sr.textContent = "Nearly there. The workshop opens soon.";
    if (timer) {
      clearTimeout(timer);
      timer = 0;
    }
    if (!looking) {
      looking = true;
      lookForRelease();
    }
  }

  function tick() {
    if (isNaN(launchMs)) {
      clock.hidden = true;
      opens.hidden = false;
      return true;
    }
    var diff = launchMs - Date.now();
    if (diff <= 0) {
      showHold();
      return true;
    }
    if (!opens.hasAttribute("data-armed")) {
      launchEl.textContent = "Opens Monday, 9:00 AM";
      opens.setAttribute("data-armed", "");
      sr.textContent = "Counting down to Monday 28 September 2026, 9:00 AM Brisbane time.";
    }
    var total = Math.floor(diff / 1000);
    var days = Math.floor(total / 86400);
    var hours = Math.floor((total % 86400) / 3600);
    var mins = Math.floor((total % 3600) / 60);
    var secs = total % 60;
    paint(nodes[0], days);
    paint(nodes[1], hours);
    paint(nodes[2], mins);
    paint(nodes[3], secs);

    var minuteBucket = Math.floor(diff / 60000);
    if (lastMinute === null) {
      lastMinute = minuteBucket;
    } else if (minuteBucket !== lastMinute) {
      lastMinute = minuteBucket;
      sr.textContent =
        days +
        " days, " +
        hours +
        " hours, " +
        mins +
        " minutes until Monday 28 September 2026, 9:00 AM Brisbane time.";
    }
    return false;
  }

  function arm() {
    if (tick()) return;
    timer = setTimeout(arm, 1000 - (Date.now() % 1000));
  }

  arm();
})();
