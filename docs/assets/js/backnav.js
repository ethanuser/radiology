/* In-page jump history: any click on an in-page link remembers where you were and shows a
   "Back to where you were" pill. Works alongside the browser's own Back button. */
(function () {
  const pill = document.getElementById("backPill");
  if (!pill) return;
  const stack = [];
  const reduced = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const flash = (el) => {
    if (!el) return;
    el.classList.remove("flash");
    void el.offsetWidth;
    el.classList.add("flash");
  };
  document.addEventListener("click", (ev) => {
    const a = ev.target.closest && ev.target.closest('a[href^="#"]');
    if (!a || a.closest(".topnav") || a.getAttribute("href") === "#") return;
    const target = document.getElementById(decodeURIComponent(a.getAttribute("href").slice(1))) ||
      document.querySelector(`[name="${a.getAttribute("href").slice(1)}"]`);
    if (!target) return;
    ev.preventDefault();
    stack.push({ y: window.scrollY, el: a });
    history.pushState({ jump: stack.length }, "", a.getAttribute("href"));
    // One scroll to the final position. (scrollIntoView followed by scrollBy cancels the first smooth scroll,
    // so the page appeared not to move.) Offset by the sticky header, and on narrow screens by the sticky dashboard.
    scrollToTarget(target);
    flash(target.closest("li, tr, h2, h3, h4, .gcard, .card, p, section") || target);
    pill.hidden = false;
  });
  function offsetFor(target) {
    const nav = document.querySelector(".topnav");
    let offset = (nav ? nav.offsetHeight : 56) + 14;
    const dash = target.closest(".scrolly") && document.querySelector(".dash");
    if (dash && getComputedStyle(dash).position === "sticky" && window.innerWidth <= 1000) offset += dash.offsetHeight;
    return offset;
  }
  let fixTimer = 0;
  function scrollToTarget(target) {
    const top = target.getBoundingClientRect().top + window.scrollY - offsetFor(target);
    window.scrollTo({ top: Math.max(0, top), behavior: reduced() ? "auto" : "smooth" });
    // Charts drawn lazily while scrolling can shift the layout; once the scroll settles, correct any drift.
    clearTimeout(fixTimer);
    const fix = () => {
      clearTimeout(fixTimer);
      window.removeEventListener("scrollend", fix);
      const d = target.getBoundingClientRect().top - offsetFor(target);
      if (Math.abs(d) > 12) window.scrollTo({ top: Math.max(0, window.scrollY + d), behavior: "auto" });
    };
    window.addEventListener("scrollend", fix, { once: true });
    fixTimer = setTimeout(fix, 1500);
  }
  function goBack() {
    const last = stack.pop();
    if (!last) { pill.hidden = true; return; }
    window.scrollTo({ top: last.y, behavior: reduced() ? "auto" : "smooth" });
    flash(last.el.closest("p, li, td, .callout, .tile, .stat") || last.el);
    pill.hidden = stack.length === 0;
  }
  pill.addEventListener("click", () => { history.back(); });
  window.addEventListener("popstate", () => { if (stack.length) goBack(); });
  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && stack.length && !document.querySelector(".citepop:not([hidden])")) history.back();
  });
})();
