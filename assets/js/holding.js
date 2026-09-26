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
  var hint = document.getElementById("hint");
  var sr = document.getElementById("sr");
  var lastMinute = null;
  var timer = 0;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function pad(n) {
    return (n < 10 ? "0" : "") + n;
  }

  function paint(el, value) {
    var next = pad(value);
    if (el.textContent === next) return;
    var seen = el.getAttribute("data-seen") === "1";
    el.textContent = next;
    el.setAttribute("data-seen", "1");
    if (!seen || reduced) return;
    el.classList.remove("is-tick");
    void el.offsetWidth;
    el.classList.add("is-tick");
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
  }

  function tick() {
    if (isNaN(launchMs)) {
      clock.hidden = true;
      opens.hidden = false;
      return true;
    }
    var diff = launchMs - Date.now();
    if (diff <= 0) {
      showLive();
      return true;
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

  document.getElementById("reload").addEventListener("click", function () {
    window.location.reload();
  });

  function arm() {
    if (tick()) return;
    timer = setTimeout(arm, 1000 - (Date.now() % 1000));
  }

  arm();
})();
