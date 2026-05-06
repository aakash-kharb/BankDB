(function () {
  /* ── Theme Toggle with persistence ─────────────────────────────── */
  const toggle = document.getElementById("themeToggle");
  const html = document.documentElement;

  // Restore saved preference
  const saved = localStorage.getItem("bankdb-theme");
  if (saved) {
    html.setAttribute("data-bs-theme", saved);
  }
  updateIcon();

  if (toggle) {
    toggle.addEventListener("click", function () {
      const current = html.getAttribute("data-bs-theme") || "light";
      const next = current === "light" ? "dark" : "light";
      html.setAttribute("data-bs-theme", next);
      localStorage.setItem("bankdb-theme", next);
      updateIcon();
    });
  }

  function updateIcon() {
    if (!toggle) return;
    const icon = toggle.querySelector(".material-symbols-outlined");
    if (!icon) return;
    const isDark = html.getAttribute("data-bs-theme") === "dark";
    icon.textContent = isDark ? "light_mode" : "dark_mode";
  }

  /* ── Auto-dismiss toasts after 4s ──────────────────────────────── */
  document.querySelectorAll(".toast.show").forEach(function (toast) {
    setTimeout(function () {
      toast.classList.remove("show");
      toast.style.opacity = "0";
      toast.style.transition = "opacity 0.4s ease";
      setTimeout(function () { toast.remove(); }, 400);
    }, 4000);
  });

  /* ── Active nav link highlighting ──────────────────────────────── */
  var path = window.location.pathname;
  document.querySelectorAll(".site-nav .nav-link").forEach(function (link) {
    var href = link.getAttribute("href");
    if (href && href !== "/" && path.startsWith(href)) {
      link.classList.add("active");
    } else if (href === "/" && path === "/") {
      link.classList.add("active");
    }
  });
})();
