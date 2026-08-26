// Some iOS in-app browsers expose a desktop-sized layout viewport even on a
// phone. Add a targeted fallback class without affecting normal mobile Safari.
const deviceWidth = window.screen?.width || 0;
const isIPhoneWebView = /iPhone|iPod/i.test(navigator.userAgent);
const hasCompactScreen = deviceWidth > 0 && deviceWidth <= 600;
const hasDesktopViewportOnPhone = window.innerWidth >= 700 && (isIPhoneWebView || hasCompactScreen);

if (hasDesktopViewportOnPhone) {
  document.documentElement.classList.add("tg-mobile-viewport-fallback");
}

// Project filters
const filterButtons = document.querySelectorAll(".filter-btn");
const projectCards = document.querySelectorAll(".project-card");

if (filterButtons.length && projectCards.length) {
  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const selectedFilter = button.dataset.filter;

      filterButtons.forEach((item) => item.classList.remove("active"));
      button.classList.add("active");

      projectCards.forEach((card) => {
        const categories = card.dataset.category || "";
        card.hidden = selectedFilter !== "all" && !categories.split(" ").includes(selectedFilter);
      });
    });
  });
}

// Full-screen navigation
const menuButton = document.getElementById("tgMenuToggle");
const navigation = document.getElementById("tgNavMenu");

if (menuButton && navigation) {
  const closeMenu = () => {
    document.body.classList.remove("tg-menu-open");
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "Open navigation menu");
  };

  menuButton.addEventListener("click", () => {
    const isOpen = document.body.classList.toggle("tg-menu-open");
    menuButton.setAttribute("aria-expanded", String(isOpen));
    menuButton.setAttribute("aria-label", isOpen ? "Close navigation menu" : "Open navigation menu");
  });

  navigation.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu();
  });
}
