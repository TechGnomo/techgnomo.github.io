(function () {
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var rig = document.querySelector(".rig");
  var cx = document.getElementById("cx");
  var cy = document.getElementById("cy");

  if (rig && cx && cy && fine && !reduced) {
    rig.addEventListener("pointermove", function (event) {
      var box = rig.getBoundingClientRect();
      if (!box.width || !box.height) return;
      var x = Math.round(((event.clientX - box.left) / box.width) * 99);
      var y = Math.round(((event.clientY - box.top) / box.height) * 99);
      x = Math.max(0, Math.min(99, x));
      y = Math.max(0, Math.min(99, y));
      cx.textContent = "X " + String(x).padStart(2, "0");
      cy.textContent = "Y " + String(y).padStart(2, "0");
    });
  }

  function flash(button, label) {
    var previous = button.textContent;
    button.textContent = label;
    window.setTimeout(function () {
      button.textContent = previous;
    }, 1200);
  }

  function copy(url, button) {
    if (!navigator.clipboard || !navigator.clipboard.writeText) {
      flash(button, "Unavailable");
      return;
    }
    navigator.clipboard.writeText(url).then(
      function () {
        flash(button, "Copied");
      },
      function () {
        flash(button, "Unavailable");
      }
    );
  }

  document.querySelectorAll("[data-share]").forEach(function (button) {
    button.addEventListener("click", function () {
      var url = new URL(button.getAttribute("data-share"), window.location.origin).href;
      if (navigator.share) {
        navigator.share({ title: "TechGnomo", url: url }).catch(function (error) {
          if (!error || error.name !== "AbortError") copy(url, button);
        });
        return;
      }
      copy(url, button);
    });
  });
})();
