/* Progressive enhancement for browsers without animation-timeline: view().
   Sets --shift on each stage from IntersectionObserver entries.
   No scroll listener. Reduced motion and supporting browsers keep the CSS. */
(function () {
  var root = document.querySelector("[data-product]");
  if (!root || !window.IntersectionObserver) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (window.CSS && CSS.supports("animation-timeline: view()")) return;

  var ranges = {
    parent: [0, 0],
    approach: [0, 0.18],
    crossover: [0.18, 0.46],
    product: [0.58, 1]
  };
  var stages = Array.prototype.slice.call(document.querySelectorAll("[data-stage]"));
  if (!stages.length) return;

  var thresholds = [];
  for (var i = 0; i <= 20; i += 1) thresholds.push(i / 20);

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      var name = entry.target.getAttribute("data-stage");
      var range = ranges[name];
      var box = entry.rootBounds;
      if (!range || !box || !box.height) return;
      var progress = (box.height - entry.boundingClientRect.top) / (box.height * 0.7);
      if (progress < 0) progress = 0;
      if (progress > 1) progress = 1;
      var shift = range[0] + (range[1] - range[0]) * progress;
      entry.target.style.setProperty("--shift", shift.toFixed(4));
    });
  }, { threshold: thresholds });

  stages.forEach(function (stage) {
    observer.observe(stage);
  });
})();

/* Colour, product type and the theme file are not on the first paint.
   The opening is the parent brand, and its frame is already in site.css.
   Load them on the first scroll (or a jump to a hash), otherwise shortly
   after load, so they do not compete with Fraunces and Source Sans. */
(function () {
  var root = document.querySelector("[data-product]");
  if (!root) return;
  var hrefs = ["/assets/css/product-transition.css"];
  var theme = root.getAttribute("data-product-theme");
  var fonts = root.getAttribute("data-product-fonts");
  if (theme) hrefs.push(theme);
  if (fonts) hrefs.push(fonts);
  var started = false;
  function loadSheets() {
    if (started) return;
    started = true;
    hrefs.forEach(function (href) {
      if (document.querySelector('link[rel="stylesheet"][href="' + href + '"]')) return;
      var link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = href;
      document.head.appendChild(link);
    });
  }
  if (window.location.hash) loadSheets();
  window.addEventListener("scroll", loadSheets, { once: true, passive: true, capture: true });
  window.addEventListener("pointerdown", loadSheets, { once: true, passive: true });
  window.addEventListener("keydown", loadSheets, { once: true });
  function later() {
    window.setTimeout(loadSheets, 2500);
  }
  if (document.readyState === "complete") later();
  else window.addEventListener("load", later);
})();
