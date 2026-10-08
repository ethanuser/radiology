/* In-page jump history: any click on an in-page link remembers where you were and shows a
   "Back to where you were" pill. Works alongside the browser's own Back button. */
(function () {
  const pill = document.getElementById("backPill");
  if (!pill) return;
  const stack = [];
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
    target.scrollIntoView({ block: "start" });
    window.scrollBy(0, -70);
    flash(target.closest("li, tr, h2, h3, h4, section, .card, p") || target);
    pill.hidden = false;
  });
  function goBack() {
    const last = stack.pop();
    if (!last) { pill.hidden = true; return; }
    window.scrollTo({ top: last.y });
    flash(last.el.closest("p, li, td, .callout, .tile, .stat") || last.el);
    pill.hidden = stack.length === 0;
  }
  pill.addEventListener("click", () => { history.back(); });
  window.addEventListener("popstate", () => { if (stack.length) goBack(); });
  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && stack.length) history.back();
  });
})();
