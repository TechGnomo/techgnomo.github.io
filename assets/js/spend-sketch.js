(function () {
  var form = document.getElementById("spend-sketch");
  if (!form) return;

  var label = document.getElementById("left-label");
  var amount = document.getElementById("left-amount");
  var money = new Intl.NumberFormat("en-AU", {
    style: "currency",
    currency: "AUD",
  });

  function read(name) {
    var value = Number(form.elements[name].value);
    if (!Number.isFinite(value) || value < 0) return 0;
    return value;
  }

  function update() {
    var left = read("pay") - read("bills") - read("debt") - read("save");
    if (left >= 0) {
      label.textContent = "Left this cycle";
      amount.textContent = money.format(left);
    } else {
      label.textContent = "Short this cycle";
      amount.textContent = money.format(Math.abs(left));
    }
  }

  form.addEventListener("input", update);
  update();
})();
