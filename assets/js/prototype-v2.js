(function () {
  var button = document.querySelector("[data-power]");
  var object = document.getElementById("demo-object");
  if (button && object) {
    button.addEventListener("click", function () {
      var on = object.classList.toggle("is-on");
      button.setAttribute("aria-pressed", on ? "true" : "false");
      button.textContent = on ? "Dim the frame" : "Light the frame";
    });
  }

  document.querySelectorAll("[data-share]").forEach(function (node) {
    node.addEventListener("click", function (event) {
      var url = new URL(node.getAttribute("data-share"), window.location.origin).href;
      if (navigator.share) {
        event.preventDefault();
        navigator.share({ title: "TechGnomo", url: url }).catch(function (error) {
          if (!error || error.name === "AbortError") return;
          copy(url, node);
        });
        return;
      }
      if (node.tagName === "BUTTON") {
        event.preventDefault();
        copy(url, node);
      }
    });
  });

  function copy(url, node) {
    if (!navigator.clipboard || !navigator.clipboard.writeText) return;
    var previous = node.textContent;
    navigator.clipboard.writeText(url).then(function () {
      node.textContent = "Copied";
      window.setTimeout(function () {
        node.textContent = previous;
      }, 1200);
    });
  }
})();
