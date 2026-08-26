const root = document.documentElement;
const header = document.getElementById("siteHeader");
const progress = document.getElementById("pageProgress");
const pointerGlow = document.getElementById("pointerGlow");
const menuToggle = document.getElementById("menuToggle");
const navigation = document.getElementById("siteNavigation");
const briefForm = document.getElementById("briefForm");
const formStatus = document.getElementById("formStatus");
const year = document.getElementById("currentYear");
const scenes = document.querySelectorAll("[data-scene]");
const navLinks = document.querySelectorAll("[data-nav]");
const railLinks = document.querySelectorAll("[data-rail]");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

root.classList.add("js");

function trackEvent(name, details = {}) {
  const safeName = String(name || "interaction").replace(/[^a-z0-9_]/gi, "_").toLowerCase();

  if (typeof window.gtag === "function") {
    window.gtag("event", safeName, details);
  }

  window.dispatchEvent(
    new CustomEvent("techgnomo:event", {
      detail: { name: safeName, ...details },
    }),
  );
}

window.techGnomoTrack = trackEvent;

function updateScrollState() {
  const scrollTop = window.scrollY;
  const scrollable = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
  const completion = Math.min(Math.max(scrollTop / scrollable, 0), 1);

  header?.classList.toggle("is-scrolled", scrollTop > 20);

  if (progress) {
    progress.style.width = `${completion * 100}%`;
  }

  const marker = window.innerHeight * 0.42;
  let activeScene = "top";

  scenes.forEach((scene) => {
    const bounds = scene.getBoundingClientRect();
    if (bounds.top <= marker && bounds.bottom >= marker) {
      activeScene = scene.dataset.scene || activeScene;
    }
  });

  setActiveScene(activeScene);
}

let scrollFrame;
window.addEventListener(
  "scroll",
  () => {
    if (scrollFrame) {
      return;
    }

    scrollFrame = window.requestAnimationFrame(() => {
      updateScrollState();
      scrollFrame = null;
    });
  },
  { passive: true },
);

updateScrollState();

if (pointerGlow && window.matchMedia("(pointer: fine)").matches && !reduceMotion) {
  document.body.classList.add("has-pointer");

  window.addEventListener(
    "pointermove",
    (event) => {
      root.style.setProperty("--pointer-x", `${event.clientX}px`);
      root.style.setProperty("--pointer-y", `${event.clientY}px`);
    },
    { passive: true },
  );
}

function setMenu(open) {
  if (!menuToggle || !navigation) {
    return;
  }

  menuToggle.setAttribute("aria-expanded", String(open));
  menuToggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
  navigation.classList.toggle("is-open", open);
  document.body.classList.toggle("menu-open", open);
}

menuToggle?.addEventListener("click", () => {
  setMenu(menuToggle.getAttribute("aria-expanded") !== "true");
});

navigation?.addEventListener("click", (event) => {
  if (event.target.closest("a")) {
    setMenu(false);
  }
});

window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    setMenu(false);
  }
});

const revealItems = document.querySelectorAll(".reveal");
document.querySelectorAll("#top .reveal").forEach((item) => item.classList.add("is-visible"));

if (reduceMotion || !("IntersectionObserver" in window)) {
  revealItems.forEach((item) => item.classList.add("is-visible"));
} else {
  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { rootMargin: "0px 0px -10%", threshold: 0.08 },
  );

  revealItems.forEach((item) => {
    if (!item.classList.contains("is-visible")) {
      revealObserver.observe(item);
    }
  });
}

function setActiveScene(sceneId) {
  navLinks.forEach((link) => {
    const active = link.dataset.nav === sceneId;
    link.classList.toggle("is-active", active);

    if (active) {
      link.setAttribute("aria-current", "location");
    } else {
      link.removeAttribute("aria-current");
    }
  });

  railLinks.forEach((link) => {
    const railScene = sceneId === "about" ? "process" : sceneId;
    const active = link.dataset.rail === railScene;
    link.classList.toggle("is-active", active);

    if (active) {
      link.setAttribute("aria-current", "location");
    } else {
      link.removeAttribute("aria-current");
    }
  });
}

document.querySelectorAll("[data-event]").forEach((element) => {
  element.addEventListener("click", () => {
    trackEvent(element.dataset.event, {
      page_path: window.location.pathname,
    });
  });
});

briefForm?.addEventListener("submit", (event) => {
  event.preventDefault();

  if (!briefForm.reportValidity()) {
    return;
  }

  const data = new FormData(briefForm);
  const name = String(data.get("name") || "").trim();
  const email = String(data.get("email") || "").trim();
  const projectType = String(data.get("projectType") || "Project enquiry").trim();
  const problem = String(data.get("problem") || "").trim();
  const subject = `[TechGnomo enquiry] ${projectType} — ${name}`;
  const body = [
    `Hi Fabio,`,
    "",
    `My name is ${name}.`,
    `My email is ${email}.`,
    `Project type: ${projectType}`,
    "",
    "The problem I want to solve:",
    problem,
    "",
    "I would like to discuss the clearest next step.",
  ].join("\n");

  if (formStatus) {
    formStatus.textContent = "Opening a new email with your brief…";
  }

  trackEvent("project_brief_prepared", { project_type: projectType });
  window.location.href = `mailto:gnomocode@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
});

if (year) {
  year.textContent = String(new Date().getFullYear());
}
