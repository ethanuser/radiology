/* Page logic shared by the main page and the personal page.
   <body data-page="main|personal" data-root="." data-stage="m1" data-start="2035"> */
/* global d3, Charts */
(async function () {
  const { fmt, css } = Charts;
  const BODY = document.body;
  const ROOTP = BODY.dataset.root || ".";
  const F = await (await fetch(`${ROOTP}/data/forecast.json`)).json();
  const years = F.years;
  const yi = (y) => years.indexOf(Math.min(2066, Math.max(2026, y)));
  const SUM = Object.fromEntries(F.summary.map((r) => [r.year, r]));
  const JEV = Object.fromEntries(F.jevons.table.map((r) => [r.year, r]));
  const REG = Object.fromEntries(F.regimes.table.map((r) => [r.regime, r]));
  const X = F.extra;
  const S = F.series;
  F.ratio0_gap = 1 - S.R.p50[0];
  F.n_params = F.params.length;
  // aliases so page text can bind tornado swings and derived figures instead of hard-coding them
  const TOR = Object.fromEntries(F.tornado.map((r) => [r.group, r]));
  F.tor = { ai: TOR["AI capability speed"], util: TOR["Future imaging utilization"], assist: TOR["Assistive-AI time savings"],
    reg: TOR["Regulatory delay"], slots: TOR["Residency slot growth"], r0: TOR["Today's shortage (2026 S/D)"] };
  F.tor_other_max = d3.max(F.tornado.filter((r) => !["AI capability speed", "Future imaging utilization", "Assistive-AI time savings"].includes(r.group)),
    (r) => Math.abs(r.pOver2045_high - r.pOver2045_low));
  F.fte2026 = F.extra.supply.head_2026_p50 / F.series.R.p50[0];
  F.ratio0 = F.params.find((p) => p.name === "ratio0");
  // how much narrower the 2045 demand range gets if the judgment-call inputs were known exactly
  F.subj_shrink = (F.evidence_attribution.find((r) => r.metric === "D" && r.year === 2045 && r.grade === "Subjective") || {}).shrink;
  const BT = F.backtest;
  const ROOT = { F, SUM, JEV, REG, X, VAL: F.validation, BT };
  const FMT = { pct: fmt.pct, pct1: fmt.pct1, x2: fmt.x2, chg: fmt.chg, mult: fmt.mult, int: (v) => d3.format(",.0f")(v),
    r100: (v) => d3.format(",.0f")(Math.round(v / 100) * 100), gr: (v) => fmt.pct(v - 1), pp: (v) => (v * 100).toFixed(1) + " percentage points", pts: (v) => Math.round(v * 100) + " percentage points",
    k: (v) => d3.format(",")(Math.round(v / 1000) * 1000),
    yr: (v) => String(Math.round(v)) };
  const $ = (s) => document.querySelector(s);
  const has = (s) => !!document.querySelector(s);

  // ------------------------------------------------------------------ career stage (optional personalization)
  const stages = F.stages;
  let stage = null;
  function loadStage() {
    if (BODY.dataset.stage) {
      const st = stages.find((s) => s.key === BODY.dataset.stage);
      stage = { ...st, start: +(BODY.dataset.start || st.start) };
      return;
    }
    try { const k = localStorage.getItem("stage"); if (k) stage = stages.find((s) => s.key === k) || null; } catch (e) { stage = null; }
  }
  loadStage();
  // years from the Match to independent practice: PGY-1 + 4 DR years + 1-year fellowship (data-train="5" without fellowship)
  const TRAIN = +(BODY.dataset.train || 6);
  function phaseOf(year) {
    if (!stage) return "";
    const A = stage.start;
    if (year >= A) return year === A ? "starting independent practice" : `${year - A} years into practice`;
    if (year >= A - TRAIN) return TRAIN === 6 ? "in residency or fellowship" : "in residency";
    if (year >= A - TRAIN - 4) return "in medical school";
    return "before medical school";
  }

  // ------------------------------------------------------------------ data binding
  const resolve = (path) => path.split(".").reduce((o, k) => (o == null ? undefined : o[k]), ROOT);
  function bind(root = document) {
    root.querySelectorAll("[data-v]").forEach((el) => {
      const v = resolve(el.dataset.v);
      if (v === undefined || v === null) return;
      const f = FMT[el.dataset.f] || FMT.x2; // unknown format: fall back rather than break the page
      if (el.hasAttribute("data-count") && typeof v === "number") countUp(el, v, f); else el.textContent = f(v);
    });
  }
  function countUp(el, v, f) {
    const io = new IntersectionObserver((ents) => ents.forEach((e) => {
      if (!e.isIntersecting) return;
      io.disconnect();
      const t0 = performance.now();
      const step = (t) => { const k = Math.min(1, (t - t0) / 1100); el.textContent = f(v * d3.easeCubicOut(k)); if (k < 1) requestAnimationFrame(step); };
      requestAnimationFrame(step);
    }));
    io.observe(el);
  }

  // ------------------------------------------------------------------ citations: numbering, pop-overs, back-links
  const refOrder = [];
  const citeOcc = {};
  function cite(root = document) {
    root.querySelectorAll("sup.cite[data-ref]:not([data-done])").forEach((el) => {
      el.dataset.done = "1";
      const keys = el.dataset.ref.split(/[;,\s]+/).filter((k) => F.references[k]);
      el.replaceChildren();
      keys.forEach((k, i) => {
        if (!refOrder.includes(k)) refOrder.push(k);
        const n = refOrder.indexOf(k) + 1;
        citeOcc[n] = (citeOcc[n] || 0) + 1;
        const a = document.createElement("a");
        a.href = "#ref-" + n;
        a.id = `cite-${n}-${citeOcc[n]}`;
        a.className = "citelink";
        a.dataset.key = k;
        a.textContent = n;
        el.appendChild(a);
        if (i < keys.length - 1) el.appendChild(document.createTextNode(","));
      });
    });
    renderRefs();
  }
  function renderRefs() {
    const ol = $("#refList");
    if (!ol) return;
    ol.replaceChildren();
    const letters = "abcdefghijklmnopqrstuvwxyz";
    refOrder.forEach((k, i) => {
      const n = i + 1;
      const li = document.createElement("li");
      li.id = "ref-" + n;
      const body = document.createElement("span");
      body.innerHTML = F.references[k].html; // generated by model/references.py: AMA text with <i> and <a> only
      li.appendChild(body);
      // only places still on the page (diagram details and filtered tables re-render their citations)
      const live = [];
      for (let j = 1; j <= (citeOcc[n] || 0); j++) if (document.getElementById(`cite-${n}-${j}`)) live.push(j);
      if (live.length) {
        const back = document.createElement("span");
        back.className = "backlinks";
        back.appendChild(document.createTextNode(" Cited at: "));
        live.forEach((j, m) => {
          const tag = live.length > 1 ? (letters[m] || String(m + 1)) : "";
          const a = document.createElement("a");
          a.href = `#cite-${n}-${j}`;
          a.textContent = "↩" + tag;
          a.title = "Back to where this is cited" + (tag ? ` (${tag})` : "");
          back.appendChild(a);
          back.appendChild(document.createTextNode(" "));
        });
        li.appendChild(back);
      }
      ol.appendChild(li);
    });
  }
  // pop-over
  const pop = document.createElement("div");
  pop.id = "citePop";
  pop.className = "citepop";
  pop.setAttribute("role", "dialog");
  pop.setAttribute("aria-label", "Reference details");
  pop.hidden = true;
  document.body.appendChild(pop);
  let popPinned = false, popHideTimer = 0;
  function showPop(a, pin) {
    const k = a.dataset.key, r = F.references[k], n = refOrder.indexOf(k) + 1;
    pop.replaceChildren();
    const head = document.createElement("div");
    head.className = "cp-head";
    head.textContent = `Reference ${n}`;
    const ref = document.createElement("div");
    ref.className = "cp-ref";
    ref.innerHTML = r.html; // trusted, generated
    pop.append(head, ref);
    if (r.use) {
      const u = document.createElement("div");
      u.className = "cp-use";
      const b = document.createElement("b");
      b.textContent = "What this source supports here: ";
      u.append(b, document.createTextNode(r.use));
      pop.appendChild(u);
    }
    const acts = document.createElement("div");
    acts.className = "cp-acts";
    const mk = (href, text, ext) => { const x = document.createElement("a"); x.href = href; x.textContent = text; if (ext) { x.target = "_blank"; x.rel = "noopener"; } return x; };
    if (r.passage) acts.appendChild(mk(r.passage, "Open source at this passage ↗", true));
    else acts.appendChild(mk(r.href, "Open source ↗", true));
    acts.appendChild(mk("#ref-" + n, "Go to reference list ↓"));
    pop.appendChild(acts);
    if (r.passage) {
      const note = document.createElement("div");
      note.className = "cp-note";
      note.textContent = "Opens the abstract with the supporting sentence highlighted (browsers with text-fragment support).";
      pop.appendChild(note);
    }
    pop.hidden = false;
    const rc = a.getBoundingClientRect();
    const w = Math.min(420, window.innerWidth - 24);
    pop.style.width = w + "px";
    pop.style.left = Math.min(window.innerWidth - w - 12, Math.max(12, rc.left - w / 2)) + "px";
    pop.style.top = rc.bottom + 8 + "px";
    const ph = pop.offsetHeight;
    if (rc.bottom + 8 + ph > window.innerHeight - 8) pop.style.top = Math.max(8, rc.top - ph - 8) + "px";
    popPinned = !!pin;
  }
  function hidePop() { pop.hidden = true; popPinned = false; }
  document.addEventListener("pointerover", (ev) => {
    const a = ev.target.closest && ev.target.closest("a.citelink");
    if (a && ev.pointerType !== "touch") { clearTimeout(popHideTimer); if (!popPinned) showPop(a, false); }
  });
  document.addEventListener("pointerout", (ev) => {
    const a = ev.target.closest && ev.target.closest("a.citelink");
    if (a && !popPinned) popHideTimer = setTimeout(() => { if (!pop.matches(":hover")) hidePop(); }, 300);
  });
  pop.addEventListener("pointerleave", () => { if (!popPinned) popHideTimer = setTimeout(hidePop, 250); });
  pop.addEventListener("pointerenter", () => clearTimeout(popHideTimer));
  document.addEventListener("focusin", (ev) => { const a = ev.target.closest && ev.target.closest("a.citelink"); if (a) showPop(a, false); });
  document.addEventListener("click", (ev) => {
    const a = ev.target.closest && ev.target.closest("a.citelink");
    if (a) { ev.preventDefault(); ev.stopPropagation(); showPop(a, true); return; }
    if (!pop.hidden && !pop.contains(ev.target)) hidePop();
    if (pop.contains(ev.target) && ev.target.closest('a[href^="#"]')) setTimeout(hidePop, 0);
  }, true);
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") hidePop(); });
  window.addEventListener("scroll", () => { if (!pop.hidden && !popPinned) hidePop(); }, { passive: true });

  bind();
  cite();

  // ------------------------------------------------------------------ helpers
  const col = () => ({ d: css("--s1"), s: css("--s2"), r: css("--s7"), a: css("--s3"), y: css("--s4"), m: css("--s5"), g: css("--s6"), red: css("--s8") });
  const youMark = () => (stage ? { x: Math.min(2066, stage.start), label: `you start practice (${stage.start})` } : null);

  // ------------------------------------------------------------------ hero
  function heroChart() {
    if (!has("#heroChart")) return;
    const c = col();
    Charts.fan("#heroChart", { years, height: 310, animate: true, mark: youMark(), bands: [[10, 90]],
      series: [{ label: "Demand", color: c.d, q: S.D }, { label: "Supply", color: c.s, q: S.Sd }], yLabel: "Radiologist FTEs (2026 demand = 1)",
      extraLines: [{ values: S.B.p50, color: c.d, opacity: 0.8, width: 1.4, dash: "4 4", label: "Demand without new AI (median)", endLabel: "demand without new AI" }] });
  }

  // ------------------------------------------------------------------ stage selector & stage-dependent text
  function stageUI() {
    const sel = $("#stageSelect");
    if (sel && !sel.options.length) {
      const o0 = document.createElement("option"); o0.value = ""; o0.textContent = "Just exploring (no personal timeline)"; sel.appendChild(o0);
      stages.forEach((s) => { const o = document.createElement("option"); o.value = s.key; o.textContent = `${s.label} · practice from ~${s.start}`; sel.appendChild(o); });
      sel.value = stage ? stage.key : "";
      sel.addEventListener("change", () => {
        stage = stages.find((s) => s.key === sel.value) || null;
        try { if (stage) localStorage.setItem("stage", stage.key); else localStorage.removeItem("stage"); } catch (e) { /* storage unavailable */ }
        renderAll();
      });
    }
    const out = $("#stageSummary");
    if (out) {
      if (!stage) out.textContent = "Pick a stage to mark your own timeline on the charts and in the year-by-year story.";
      else {
        const A = stage.start;
        const p = (y) => fmt.pct(F.probs.p_oversupply[yi(y)]);
        out.innerHTML = `Typical start of independent practice: <b>${A}</b>. Chance of meaningful oversupply then: <b>${p(A)}</b>; ` +
          `10 years in: <b>${p(A + 10)}</b>; 20 years in: <b>${p(A + 20)}</b>. Chance the market is still short when you start: <b>${fmt.pct(1 - F.probs.p_supply_exceeds_demand[yi(A)])}</b>.`;
      }
    }
    document.querySelectorAll(".stage-note").forEach((el) => {
      const y = +el.dataset.year;
      el.hidden = !stage;
      if (stage) el.textContent = `Your timeline: in ${y} you would be ${phaseOf(y)}.`;
    });
  }

  // ------------------------------------------------------------------ scrollytelling dashboard
  let dash = null, curYear = 2026, curTag = "";
  function dashChart() {
    if (!has("#dashChart")) return;
    const c = col();
    dash = Charts.fan("#dashChart", { years, height: 230, reveal: curYear, endLabels: false, yDomain: [0.55, 1.85], bands: [[10, 90]],
      series: [{ label: "Demand", color: c.d, q: S.D }, { label: "Supply", color: c.s, q: S.Sd }], refs: [{ y: 1 }], mark: youMark(), yLabel: "FTEs (2026 demand = 1)" });
  }
  function careerTrack() {
    const tr = $("#careerTrack");
    if (!tr) return;
    tr.replaceChildren();
    const x = (y) => ((Math.min(2066, Math.max(2026, y)) - 2026) / 40) * 100 + "%";
    if (stage) {
      const A = stage.start;
      [[A - TRAIN - 4, A - TRAIN, "--axis"], [A - TRAIN, A, "--s4"], [A, 2066, "--s1"]].forEach(([a, b, cc]) => {
        if (b <= 2026) return;
        const d = document.createElement("div");
        d.className = "bar"; d.style.left = x(a); d.style.width = `calc(${x(b)} - ${x(a)} - 2px)`; d.style.background = `var(${cc})`;
        tr.appendChild(d);
      });
      [[A - TRAIN, "Residency"], [A, "Practice"], [A + 10, "+10"], [A + 20, "+20"], [A + 30, "+30"]].forEach(([y, t]) => {
        if (y < 2026 || y > 2066) return;
        const l = document.createElement("div"); l.className = "lbl"; l.style.left = x(y); l.textContent = t; tr.appendChild(l);
      });
    } else {
      const d = document.createElement("div"); d.className = "bar"; d.style.left = "0"; d.style.width = "100%"; d.style.background = "var(--grid)"; tr.appendChild(d);
      [2026, 2036, 2046, 2056, 2066].forEach((y) => { const l = document.createElement("div"); l.className = "lbl"; l.style.left = x(y); l.textContent = y; tr.appendChild(l); });
    }
    const now = document.createElement("div"); now.className = "now"; now.id = "careerNow"; now.style.left = x(curYear); tr.appendChild(now);
  }
  function setYear(y, tag) {
    if (!has("#dYear")) return;
    curYear = y; curTag = tag;
    const i = yi(y);
    const q = (k) => [S[k].p10[i], S[k].p50[i], S[k].p90[i]];
    $("#dYear").textContent = y;
    $("#dTag").textContent = stage ? `${tag} · you: ${phaseOf(y)}` : tag;
    const [r10, r50, r90] = q("R");
    $("#dRatio").textContent = fmt.x2(r50);
    $("#dRatioR").textContent = `80% range: ${fmt.x2(r10)}–${fmt.x2(r90)}`;
    const po = F.probs.p_oversupply[i];
    $("#dOver").textContent = fmt.pct(po);
    $("#dOverM").style.width = Math.min(100, po * 100) + "%";
    const [t10, t50, t90] = q("time_saved");
    $("#dSaved").textContent = fmt.pct(t50);
    $("#dSavedR").textContent = `80% range: ${fmt.pct(t10)}–${fmt.pct(t90)}`;
    const [d10, d50, d90] = q("D");
    $("#dDem").textContent = fmt.x2(d50);
    $("#dDemR").textContent = `80% range: ${fmt.x2(d10)}–${fmt.x2(d90)}`;
    const [a10, a50, a90] = q("auto");
    $("#dAuto").textContent = fmt.pct(a50);
    $("#dAutoR").textContent = `80% range: ${fmt.pct(a10)}–${fmt.pct(a90)}`;
    $("#dBelow").textContent = y === 2026 ? "–" : fmt.pct(F.probs.p_demand_below_today[i]);
    const now = $("#careerNow");
    if (now) now.style.left = ((y - 2026) / 40) * 100 + "%";
    if (dash) dash.setReveal(Math.max(2026.6, y));
  }
  const chapters = [...document.querySelectorAll(".chapter")];
  if (chapters.length) {
    curTag = chapters[0].dataset.tag;
    const io = new IntersectionObserver((ents) => ents.forEach((e) => {
      if (e.isIntersecting) { chapters.forEach((c) => c.classList.toggle("on", c === e.target)); setYear(+e.target.dataset.year, e.target.dataset.tag); }
    }), { rootMargin: "-45% 0px -45% 0px" });
    chapters.forEach((c) => io.observe(c));
    chapters[0].classList.add("on");
  }

  // ------------------------------------------------------------------ model diagram
  const NODES = {
    base: { x: 16, y: 40, t: "1 · Baseline demand", s: "population, aging, utilization" },
    ai: { x: 320, y: 40, t: "AI-progress factor", s: "4 regimes; shifts tagged boxes", factor: true },
    sup: { x: 624, y: 40, t: "5 · Radiologist supply", s: "cohorts, residency, attrition" },
    prod: { x: 16, y: 160, t: "2 · AI productivity", s: "task-based time savings", ai: true },
    dem: { x: 320, y: 160, t: "FTE demand", s: "work × time per unit of work" },
    rat: { x: 624, y: 160, t: "Supply ÷ demand", s: "shortage ↔ oversupply" },
    reg: { x: 16, y: 280, t: "4 · Regulation & uptake", s: "validation, FDA, payment", ai: true },
    jev: { x: 320, y: 280, t: "3 · Jevons / rebound", s: "induced & offsetting work", ai: true },
  };
  const NW = 200, NH = 64;
  const citeHTML = (keys) => `<sup class="cite" data-ref="${keys}"></sup>`;
  const DETAIL = {
    base: () => `<h4>1 · Baseline imaging demand</h4><p>How much radiologist work there would be if AI stayed at its 2026 level:</p>
      <ul><li><b>Demographics</b>: about +0.5%/yr from population growth and aging${citeHTML("christensen_util,cbo_2026")}</li>
      <li><b>Imaging per person</b>: starts near 1.2%/yr (CT grew 3.7–5.2%/yr before 2016) and slows over time${citeHTML("smith_bindman_2019,rosenkrantz_2025")}</li>
      <li><b>Work per exam</b>: studies keep getting bigger${citeHTML("mcdonald_2015")}</li></ul>
      <p>Median: <b>${fmt.chg(X.baseline["2045"].p50)}</b> more work by 2045 without further AI. <a href="#m-baseline">Method →</a></p>`,
    prod: () => `<h4>2 · AI productivity</h4><p>Radiologist time is split into interpretation (42%), drafting and measurement (18%),
      consultation (13%), administration (15%) and procedures (12%)${citeHTML("langlotz_2025,dhanoa_2013")}. Each task has its own AI time-saving
      ceiling, capability curve and adoption curve, anchored on measured effects from 0% to 42%${citeHTML("huang_2025,hong_2025,liu_2026")}.
      AI also <b>adds</b> oversight work${citeHTML("humlum_2025")}. <a href="#m-ai">Method →</a></p>`,
    reg: () => `<h4>4 · Regulation & uptake</h4><p>Before AI can read a class of exams on its own, it must pass, in order:
      <b>technical capability → clinical validation → FDA authorization → liability & payment → hospital adoption</b>.
      No autonomous radiology read is FDA-authorized as of 2026${citeHTML("fda_ai_2026")}. Median year autonomy for complex CT/MR becomes payable:
      <b>${Math.round(X.stages_p50[2][3])}</b> (tier 3). <a href="#m-pipeline">Method →</a></p>`,
    jev: () => `<h4>3 · Jevons / rebound</h4><p>Cheaper and faster reads, faster scanners, new screening uses, and follow-up of AI-found
      findings create <i>more</i> work. Utilization management and reads shifting to other doctors remove some. Scanner and technologist capacity caps
      the extra exams${citeHTML("asrt_2025")}. By 2045, the new work offsets a median <b>${fmt.pct(JEV[2045].offset_p50)}</b> of the labor AI saves.
      <a href="#m-jevons">Method →</a></p>`,
    dem: () => `<h4>FTE demand</h4><p>Radiologist full-time equivalents needed = baseline work × (1 + AI-induced work) × radiologist time per unit
      of work. Median (2026 = 1): 2035 <b>${fmt.x2(SUM[2035].demand_p50)}</b>, 2045 <b>${fmt.x2(SUM[2045].demand_p50)}</b>.
      <a href="#term-demand">Definition →</a></p>`,
    sup: () => `<h4>5 · Radiologist supply</h4><p>A cohort model by years in practice, calibrated to reproduce the Neiman Institute's +25.7% growth
      (2023–2055) with flat residency positions${citeHTML("christensen_supply")}. Residency positions (1,241 in 2026${citeHTML("nrmp_2026")})
      react to the market with a lag. New residents become attendings about six years after matching. <a href="#m-supply">Method →</a></p>`,
    rat: () => `<h4>Supply ÷ demand</h4><p>Below 1 means a shortage (today ≈ ${fmt.x2(S.R.p50[0])}). Above 1.10 is <a href="#term-oversupply">meaningful
      oversupply</a>. The ratio feeds back into residency positions and, when short, speeds up AI adoption.</p>`,
    ai: () => `<h4>AI-progress factor</h4><p>One shared factor moves many inputs together: faster AI means earlier capability, higher time-saving
      ceilings, more new applications and faster scanners. It picks one of four <a href="#term-regimes">regimes</a>: stall 15%, trend 55%,
      fast 18%, transformative 12%.</p>`,
  };
  function diagram() {
    const el = $("#diagram");
    if (!el) return;
    el.replaceChildren();
    const svg = d3.select(el).append("svg").attr("viewBox", "0 0 860 370").attr("role", "img")
      .attr("aria-label", "Model structure: baseline demand, AI productivity, regulation and Jevons effects determine FTE demand; supply and demand give the supply/demand ratio");
    // Arrows are drawn by hand so every line ends exactly at the base of its arrowhead: the (animated, dashed) shaft
    // stops at the base, a short solid stub guarantees the line visibly reaches it, and the head is a separate triangle.
    const HEAD = 11, HALF = 5;
    function arrow(d, cls) {
      const tmp = svg.append("path").attr("d", d).attr("fill", "none");
      const node = tmp.node(), L = node.getTotalLength(), end = L - HEAD;
      const at = (s) => { const q = node.getPointAtLength(Math.max(0, Math.min(L, s))); return [q.x, q.y]; };
      const pts = d3.range(41).map((i) => at((end * i) / 40));
      const base = at(end), tip = at(L), stub = at(end - 8);
      tmp.remove();
      svg.append("path").attr("d", d3.line()(pts)).attr("class", "flow " + cls);
      svg.append("path").attr("d", d3.line()([stub, base])).attr("class", "stub " + cls);
      const dx = tip[0] - base[0], dy = tip[1] - base[1], len = Math.hypot(dx, dy) || 1, nx = -dy / len, ny = dx / len;
      svg.append("path").attr("class", "head " + cls)
        .attr("d", `M${tip[0]},${tip[1]} L${base[0] + nx * HALF},${base[1] + ny * HALF} L${base[0] - nx * HALF},${base[1] - ny * HALF} Z`);
    }
    const N = NODES;
    const P = (n, fx, fy) => [N[n].x + NW * fx, N[n].y + NH * fy];
    const flows = [
      [P("base", 1, 0.5), P("dem", 0, 0.3), "", "baseline work", "start"],
      [P("prod", 1, 0.55), P("dem", 0, 0.75), "neg", "", ""],
      [P("reg", 0.5, 0), P("prod", 0.5, 1), "", "AI-first share", "v"],
      [P("prod", 1, 0.9), P("jev", 0, 0.5), "", "cheaper reads", "end"],
      [P("jev", 0.5, 0), P("dem", 0.5, 1), "", "induced work", "v"],
      [P("dem", 1, 0.5), P("rat", 0, 0.5), "", "", ""],
      [P("sup", 0.5, 1), P("rat", 0.5, 0), "", "", ""],
    ];
    flows.forEach(([a, b, cls, lab, pos]) => {
      const p = d3.path();
      p.moveTo(...a);
      if (Math.abs(a[1] - b[1]) < 4 || Math.abs(a[0] - b[0]) < 4) p.lineTo(...b);
      else { const mx = (a[0] + b[0]) / 2; p.bezierCurveTo(mx, a[1], mx, b[1], b[0], b[1]); }
      arrow(p.toString(), cls);
      if (!lab) return;
      const t = svg.append("text").attr("class", "flowlab halo");
      if (pos === "v") t.attr("x", a[0] + 8).attr("y", (a[1] + b[1]) / 2 + 4);
      else if (pos === "start") t.attr("x", a[0] + 10).attr("y", a[1] - 9);
      else t.attr("x", b[0] - 10).attr("y", b[1] - 10).attr("text-anchor", "end");
      t.text(lab);
    });
    arrow(`M ${N.rat.x + NW} ${N.rat.y + NH / 2} C 852 ${N.rat.y + NH / 2}, 852 ${N.sup.y + NH / 2}, ${N.sup.x + NW} ${N.sup.y + NH / 2}`, "fb");
    svg.append("text").attr("class", "flowlab halo").attr("x", 848).attr("y", 140).attr("text-anchor", "end").text("lagged signal");
    Object.entries(N).forEach(([k, n]) => {
      const g = svg.append("g").attr("class", "node" + (n.factor ? " factor" : "")).attr("data-k", k).attr("transform", `translate(${n.x},${n.y})`)
        .attr("tabindex", 0).attr("role", "button").attr("aria-label", n.t)
        .on("click", () => select(k)).on("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); select(k); } });
      g.append("rect").attr("class", "box").attr("width", NW).attr("height", NH);
      const t1 = g.append("text").attr("x", 14).attr("y", 30).text(n.t);
      const t2 = g.append("text").attr("x", 14).attr("y", 50).attr("class", "sub").text(n.s);
      [[t1, 15], [t2, 12.5]].forEach(([t, size]) => { // shrink text that would overflow the box
        let s = size;
        while (t.node().getComputedTextLength() > NW - 28 && s > 9) { s -= 0.5; t.style("font-size", s + "px"); }
      });
      if (n.ai || n.factor) { // badge sits on the box's top edge, clear of the text
        const b = g.append("g").attr("transform", `translate(${NW - 26},0)`);
        b.append("rect").attr("x", -16).attr("y", -10).attr("width", 32).attr("height", 20).attr("rx", 10).attr("class", "badge-bg");
        b.append("text").attr("text-anchor", "middle").attr("dy", "0.35em").attr("class", "badge").text("AI");
      }
    });
    function select(k) {
      svg.selectAll(".node").classed("sel", function () { return this.dataset.k === k; });
      const d = $("#diagramDetail");
      d.innerHTML = DETAIL[k](); // authored content
      cite(d);
    }
    select("ai");
  }

  // ------------------------------------------------------------------ charts
  function regimeChart() {
    if (!has("#regimeChart")) return;
    const ramp = [css("--ramp-1"), css("--ramp-2"), css("--ramp-3"), css("--ramp-4")];
    Charts.lines("#regimeChart", { years, height: 290, yFmt: fmt.x2, valueFmt: fmt.x2, refs: [{ y: 1 }], mark: youMark(), yDomain: [0.4, 1.5], legend: true,
      yLabel: "Median FTEs (2026 demand = 1)",
      series: [...F.regimes.names.map((n, r) => ({ label: `${n} (${fmt.pct(F.regimes.weights[r])} of futures)`, color: ramp[r], values: F.regimes.D_p50[r] })),
        { label: "Supply, all futures (median)", color: css("--s2"), values: S.Sd.p50, width: 1.5, dash: "4 3" }] });
  }
  function backtestChart() {
    if (!has("#backtestChart")) return;
    Charts.backtest("#backtestChart", BT);
    const t = $("#backtestTable");
    if (t) {
      const rows = BT.occupations.map((r) => `<tr><td>${r.label}</td><td class="num"><b>${fmt.x2(r.actual)}</b></td><td class="num">${fmt.x2(r.q.p50)} (${fmt.x2(r.q.p10)}–${fmt.x2(r.q.p90)})</td>
        <td class="num">${fmt.x2(r.combo)}</td><td class="num">${fmt.x2(r.bls)}</td><td class="num">${fmt.x2(r.trend)}</td><td class="num">${r.in80 ? "yes" : "no"}</td></tr>`).join("");
      t.innerHTML = `<thead><tr><th>Occupation (2025 ÷ 2016)</th><th class="num">Actual</th><th class="num">This method: median (80% range)</th><th class="num">BLS + trend, no AI layer</th><th class="num">BLS</th><th class="num">Trend</th><th class="num">In 80% range?</th></tr></thead><tbody>${rows}</tbody>`;
    }
  }
  function forecastCharts() {
    const c = col();
    if (has("#mainChart")) Charts.fan("#mainChart", { years, height: 390, mark: youMark(), showLegend: true,
      series: [{ label: "Demand", color: c.d, q: S.D }, { label: "Supply", color: c.s, q: S.Sd }], refs: [{ y: 1 }], yLabel: "Radiologist FTEs (2026 demand = 1)",
      extraLines: [{ values: S.B.p50, color: c.d, opacity: 0.8, width: 1.4, dash: "4 4", label: "Demand without new AI (median)", endLabel: "demand without new AI" }] });
    if (has("#ratioChart")) Charts.fan("#ratioChart", { years, height: 320, yDomain: [0.6, 1.8], mark: youMark(),
      series: [{ label: "S ÷ D", color: c.r, q: S.R }], yLabel: "Supply ÷ demand",
      refs: [{ y: 1, color: css("--ink-2"), label: "balance (1.0)" }, { y: 1.1, color: c.red, label: "meaningful oversupply (1.10)" }] });
    if (has("#probChart")) Charts.lines("#probChart", { years, height: 320, yDomain: [0, 0.6], mark: youMark(), legend: true, yLabel: "Share of simulated futures",
      series: [
        { label: "Demand below 2026 level", color: c.d, values: F.probs.p_demand_below_today },
        { label: "Meaningful oversupply (supply ÷ demand > 1.10)", color: c.s, values: F.probs.p_oversupply },
        { label: "Demand below 80% of 2026", color: c.a, values: F.probs.p_demand_below_80 },
        { label: "Demand below 50% of 2026", color: c.y, values: F.probs.p_demand_below_50 }] });
  }
  function headlineTable() {
    const t = $("#headlineTable");
    if (!t) return;
    const ys = F.report_years;
    const band = (k, f) => ys.map((y) => `${f(SUM[y][k + "_p50"])} <span class="muted">(${f(SUM[y][k + "_p10"])}–${f(SUM[y][k + "_p90"])})</span>`);
    const rows = [
      ["FTE demand (2026 demand = 1)", band("demand", fmt.x2)], ["FTE supply (2026 demand = 1)", band("supplyd", fmt.x2)], ["Supply ÷ demand", band("ratio", fmt.x2)],
      ["AI time saved (share of radiologist time)", ys.map((y) => { const i = yi(y); return `${fmt.pct(S.time_saved.p50[i])} <span class="muted">(${fmt.pct(S.time_saved.p10[i])}–${fmt.pct(S.time_saved.p90[i])})</span>`; })],
      ["AI-first share of interpretive work", band("autonomous", fmt.pct)],
      ["P(demand < 2026)", ys.map((y) => fmt.pct(SUM[y].p_demand_below_today))], ["P(demand < 80% of 2026)", ys.map((y) => fmt.pct(SUM[y].p_demand_below_80))],
      ["P(demand < 50% of 2026)", ys.map((y) => fmt.pct(SUM[y].p_demand_below_50))],
      ["<b>P(meaningful oversupply)</b>", ys.map((y) => `<b>${fmt.pct(SUM[y].p_oversupply)}</b>`)],
      ["  range under alternative priors and structures", ys.map((y) => F.robust && F.robust.band[y] ? `${fmt.pct(F.robust.band[y].lo)}–${fmt.pct(F.robust.band[y].hi)}` : "–")],
      ["P(severe oversupply, supply ÷ demand > 1.25)", ys.map((y) => fmt.pct(SUM[y].p_severe_oversupply))],
      ["P(supply exceeds demand)", ys.map((y) => fmt.pct(SUM[y].p_supply_exceeds_demand))],
      ["P(meaningful shortage, supply ÷ demand < 0.90)", ys.map((y) => fmt.pct(SUM[y].p_shortage_10))]];
    t.innerHTML = `<thead><tr><th>Metric</th>${ys.map((y) => `<th class="num">${y}</th>`).join("")}</tr></thead>
      <tbody>${rows.map(([l, v]) => `<tr><td>${l}</td>${v.map((cc) => `<td class="num">${cc}</td>`).join("")}</tr>`).join("")}</tbody>`;
  }
  function aiCharts() {
    const c = col();
    if (has("#prodChart")) Charts.fan("#prodChart", { years, height: 300, series: [{ label: "Time saved", color: c.d, q: S.time_saved, fmt: fmt.pct }], yDomain: [0, 1],
      valueFmt: fmt.pct, yFmt: d3.format(".0%"), mark: youMark(), yLabel: "Share of radiologist time saved" });
    if (has("#autoChart")) Charts.fan("#autoChart", { years, height: 300, series: [{ label: "AI-first", color: c.a, q: S.auto, fmt: fmt.pct }], yDomain: [0, 1],
      valueFmt: fmt.pct, yFmt: d3.format(".0%"), mark: youMark(), yLabel: "Share of interpretive work" });
    if (has("#pipelineChart")) Charts.pipeline("#pipelineChart", F.pipeline);
  }
  function jevonsCharts() {
    const c = col();
    const chColors = { "Cheaper interpretation (price)": c.d, "Faster turnaround & availability": c.a, "Scanner throughput / latent demand": c.y,
      "New applications & screening": c.m, "Incidental findings & follow-up": c.g, "New radiologist tasks": c.r, "Utilization management (AI)": c.s,
      "Scope shift to non-radiologists": c.red };
    if (has("#jevonsChart")) Charts.stacked("#jevonsChart", { years, height: 380, valueFmt: (v) => d3.format("+.1%")(v).replace("-", "−"), yFmt: d3.format(".0%"),
      yLabel: "Share of 2026 radiologist FTEs (mean)",
      layers: Object.entries(F.jevons.channels).map(([k, v]) => ({ label: k, values: v, color: chColors[k] })),
      overlays: [{ label: "Radiologist time saved by AI", values: F.jevons.labor_saved_mean, color: css("--ink"), width: 2.4 },
        { label: "Net new work created by AI", values: F.jevons.induced_mean, color: css("--ink-2"), width: 2, dash: "6 4" }] });
    if (has("#offsetChart")) {
      const j = F.jevons;
      const idx = years.map((y, i) => i).filter((i) => years[i] >= 2028);
      Charts.fan("#offsetChart", { years: idx.map((i) => years[i]), height: 300, yDomain: [0, 1.4], valueFmt: fmt.pct, yFmt: d3.format(".0%"), bands: [[10, 90]],
        yLabel: "New work ÷ time saved",
        series: [{ label: "Offset", color: c.m, q: { p10: idx.map((i) => j.offset_p10[i]), p25: idx.map((i) => j.offset_p10[i]), p50: idx.map((i) => j.offset_p50[i]), p75: idx.map((i) => j.offset_p90[i]), p90: idx.map((i) => j.offset_p90[i]) } }],
        refs: [{ y: 1, color: c.red, label: "Jevons threshold (1.0)" }] });
    }
  }
  let tornadoMetric = "pOver2045";
  const METRIC_LABEL = { pOver2035: "P(meaningful oversupply) in 2035", pOver2045: "P(meaningful oversupply) in 2045", pOver2055: "P(meaningful oversupply) in 2055",
    D2035_p50: "Median FTE demand in 2035 (2026 = 1)", D2045_p50: "Median FTE demand in 2045 (2026 = 1)", D2055_p50: "Median FTE demand in 2055 (2026 = 1)" };
  function tornadoChart() { if (has("#tornadoChart")) Charts.tornado("#tornadoChart", F.tornado, tornadoMetric, { xLabel: METRIC_LABEL[tornadoMetric] }); }
  document.querySelectorAll("#tornadoControls button").forEach((b) => b.addEventListener("click", () => {
    document.querySelectorAll("#tornadoControls button").forEach((x) => x.setAttribute("aria-pressed", x === b));
    tornadoMetric = b.dataset.m; tornadoChart();
  }));
  let etaScope = "all";
  function etaChart() {
    if (!has("#etaChart")) return;
    const src = etaScope === "all" ? F.eta2 : F.eta2_excluding_transformative;
    const rows = src.slice().sort((a, b) => b["Demand 2045"] - a["Demand 2045"]).slice(0, 12)
      .map((r) => ({ label: r.short || r.label, value: r["Demand 2045"], ev: r.evidence, tipLabel: "η², demand 2045" }));
    const gc = { E: css("--good"), A: css("--s1"), S: css("--serious") };
    Charts.hbars("#etaChart", rows, { valueFmt: d3.format(".2f"), max: 0.6, colorFn: (r) => gc[r.ev], badge: (r) => r.ev,
      xLabel: "Share of variance in 2045 demand explained (η²)", yLabel: "Input parameter" });
  }
  // charts inside collapsed <details> are drawn at a default width; redraw at the real width when opened
  document.querySelectorAll("details").forEach((d) => d.addEventListener("toggle", () => { if (d.open && d.querySelector("#etaChart")) etaChart(); }));
  document.querySelectorAll("[data-s]").forEach((b) => b.addEventListener("click", () => {
    document.querySelectorAll("[data-s]").forEach((x) => x.setAttribute("aria-pressed", x === b));
    etaScope = b.dataset.s; etaChart();
  }));
  function evidenceChart() {
    if (!has("#evidenceChart")) return;
    const ev = F.evidence_attribution.filter((r) => r.metric === "D" && r.year === 2045);
    const gc = { Empirical: css("--good"), Anchored: css("--s1"), Subjective: css("--serious") };
    Charts.hbars("#evidenceChart", ev.map((r) => ({ label: `${r.grade} (${r.n_params} parameters)`, value: Math.max(0, r.shrink), g: r.grade, tipLabel: "interval narrows by" })),
      { valueFmt: d3.format(".0%"), max: 0.6, colorFn: (r) => gc[r.g], xLabel: "How much narrower the 80% range for 2045 demand gets", yLabel: "Parameters pinned" });
  }
  function compChart() {
    if (!has("#compChart")) return;
    const c = col();
    const keys = ["interp", "draft", "consult", "admin", "proc", "oversight", "newtasks"];
    const colors = [c.d, c.s, c.a, c.y, c.m, c.g, c.r];
    Charts.stacked("#compChart", { years, height: 360, yDomain: [0, 1], yFmt: d3.format(".0%"), valueFmt: d3.format(".0%"), yLabel: "Share of working time (mean)",
      layers: keys.map((k, i) => ({ label: F.composition_labels[k], values: F.composition[k], color: colors[i] })) });
  }

  // ------------------------------------------------------------------ robustness: prior sets and model structures
  function robustTable() {
    const t = $("#robustTable");
    if (!t || !F.robust) return;
    const R = F.robust, ys = ["2035", "2045", "2055"];
    const row = (v, kind) => `<tr><td>${v.label}${kind ? `<div class="muted small">${kind}</div>` : ""}</td>` +
      ys.map((y) => `<td class="num">${fmt.pct(v[y].p_over)}</td>`).join("") + `<td class="num">${fmt.pct(v["2045"].p_jevons)}</td></tr>`;
    const pri = Object.entries(R.priors).map(([k, v]) => row(v, k === "main" ? "main model" : v.note)).join("");
    const st = Object.entries(R.structures).filter(([k]) => k !== "base").map(([, v]) => row(v, v.detail)).join("");
    const band = `<tr><td><b>Range across all rows</b></td>${ys.map((y) => `<td class="num"><b>${fmt.pct(R.band[y].lo)}–${fmt.pct(R.band[y].hi)}</b></td>`).join("")}` +
      `<td class="num"><b>${fmt.pct(R.band["2045"].jev_lo)}–${fmt.pct(R.band["2045"].jev_hi)}</b></td></tr>`;
    t.innerHTML = `<thead><tr><th>Assumption set or model structure</th>${ys.map((y) => `<th class="num">P(oversupply) ${y}</th>`).join("")}<th class="num">P(Jevons) 2045</th></tr></thead>
      <tbody><tr><td colspan="5" class="muted small"><b>Different priors</b> (same model, reweighted futures)</td></tr>${pri}
      <tr><td colspan="5" class="muted small"><b>Different model structures</b> (main priors, re-simulated)</td></tr>${st}${band}</tbody>`;
  }

  // ------------------------------------------------------------------ careers
  function careerTable() {
    const t = $("#stageTable");
    if (!t) return;
    t.innerHTML = `<thead><tr><th>Where you are in fall 2026</th><th class="num">Typical start of practice*</th><th class="num">P(oversupply) at start</th>
      <th class="num">10 years in</th><th class="num">20 years in</th><th class="num">30 years in (or 2066)</th><th class="num">P(still a shortage) at start</th></tr></thead><tbody>` +
      X.stages.map((r) => `<tr class="${stage && stage.key === r.key ? "hl" : ""}"><td>${r.label}</td><td class="num">${r.start}</td><td class="num">${fmt.pct(r.entry_p_over)}</td>
      <td class="num">${fmt.pct(r.y10_p_over)}</td><td class="num">${fmt.pct(r.y20_p_over)}</td><td class="num">${fmt.pct(r.y30_p_over)} (${r.y30_year})</td>
      <td class="num">${fmt.pct(r.entry_p_short)}</td></tr>`).join("") + "</tbody>";
  }
  function horizon() {
    const el = $("#horizon");
    if (!el) return;
    const A = stage ? stage.start : 2035;
    const cards = [[A, stage ? "When you start practice" : "Mid-2030s entry"], [A + 10, "10 years later"], [A + 20, "20 years later"],
      [Math.min(A + 30, 2066), A + 30 > 2066 ? `End of forecast (${2066 - A} years in)` : "30 years later"]];
    el.innerHTML = cards.map(([y, t]) => {
      const i = yi(y);
      return `<div class="hcard"><div class="y">${Math.min(y, 2066)}</div><div class="t">${t}</div><div class="big">${fmt.pct(F.probs.p_oversupply[i])}</div>
      <div class="cap">chance of <a href="#term-oversupply">meaningful oversupply</a></div>
      <ul><li>Supply ÷ demand: <b>${fmt.x2(S.R.p50[i])}</b></li><li>FTE demand: <b>${fmt.x2(S.D.p50[i])}</b> (80% range ${fmt.x2(S.D.p10[i])}–${fmt.x2(S.D.p90[i])})</li>
      <li>AI time saved: <b>${fmt.pct(S.time_saved.p50[i])}</b></li><li>P(demand below today): <b>${fmt.pct(F.probs.p_demand_below_today[i])}</b></li></ul></div>`;
    }).join("");
  }
  function signposts() {
    const t = $("#signpostTable");
    if (!t) return;
    t.innerHTML = `<thead><tr><th>If we observe…</th><th class="num">2035</th><th class="num">2045</th><th class="num">2055</th></tr></thead><tbody>` +
      X.signposts.map((r) => `<tr><td>${r.label}<div class="muted small">${fmt.pct(r.share)} of simulated futures</div></td><td class="num">${fmt.pct(r.p_over_2035)}</td><td class="num">${fmt.pct(r.p_over_2045)}</td><td class="num">${fmt.pct(r.p_over_2055)}</td></tr>`).join("") + "</tbody>";
  }

  // ------------------------------------------------------------------ parameter table
  const GROUPS = { demand: "Baseline demand", ai_capability: "AI capability", ai_tasks: "AI productivity", autonomy: "Autonomy tiers",
    regulation: "Regulation & adoption", jevons: "Jevons / rebound", supply: "Supply" };
  function paramTable() {
    const sel = $("#groupFilter");
    if (!sel) return;
    Object.entries(GROUPS).forEach(([k, v]) => { const o = document.createElement("option"); o.value = k; o.textContent = v; sel.appendChild(o); });
    let grade = "all";
    const nf = (v) => (Math.abs(v) >= 1000 ? d3.format("d")(v) : d3.format(".3~g")(v));
    const render = () => {
      const q = $("#paramSearch").value.toLowerCase(), g = sel.value;
      const rows = F.params.filter((p) => (grade === "all" || p.evidence === grade) && (g === "all" || p.group === g) && (!q || (p.label + p.name + p.note).toLowerCase().includes(q)));
      const t = $("#paramTable");
      t.replaceChildren();
      const thead = t.createTHead().insertRow();
      ["Component", "Parameter", "Distribution", "P10 / P50 / P90", "Grade", "Sources & notes"].forEach((h, i) => { const th = document.createElement("th"); th.textContent = h; if (i === 3) th.className = "num"; thead.appendChild(th); });
      const tb = t.createTBody();
      rows.forEach((p) => {
        const tr = tb.insertRow();
        tr.insertCell().textContent = GROUPS[p.group];
        const c1 = tr.insertCell(); const b = document.createElement("b"); b.textContent = p.label; c1.appendChild(b);
        const code = document.createElement("div"); code.className = "muted small"; code.textContent = p.name + " · " + p.unit; c1.appendChild(code);
        tr.insertCell().textContent = p.dist;
        const c3 = tr.insertCell(); c3.className = "num"; c3.textContent = `${nf(p.q10)} / ${nf(p.q50)} / ${nf(p.q90)}`;
        const c4 = tr.insertCell(); const gs = document.createElement("span"); gs.className = "grade " + p.evidence; gs.textContent = p.evidence; c4.appendChild(gs);
        const c5 = tr.insertCell();
        if (p.sources.length) { const s = document.createElement("sup"); s.className = "cite"; s.dataset.ref = p.sources.join(","); c5.appendChild(s); c5.appendChild(document.createTextNode(" ")); }
        const note = document.createElement("span"); note.className = "small ink2"; note.textContent = p.note; c5.appendChild(note);
        const ld = Object.entries(p.loadings || {});
        if (ld.length) { const l = document.createElement("div"); l.className = "small muted"; l.textContent = "Correlated via " + ld.map(([k, v]) => `${k} ${v > 0 ? "+" : ""}${v}`).join(", "); c5.appendChild(l); }
      });
      cite(t);
    };
    document.querySelectorAll("#gradeFilter button").forEach((b) => b.addEventListener("click", () => {
      document.querySelectorAll("#gradeFilter button").forEach((x) => x.setAttribute("aria-pressed", x === b));
      grade = b.dataset.g; render();
    }));
    sel.addEventListener("change", render);
    $("#paramSearch").addEventListener("input", render);
    render();
  }

  // ------------------------------------------------------------------ explorer
  let SAM = null;
  const filt = { regime: "any", reg_lag: "any", util_g0: "any", new_max: "any", slot_g: "any" };
  const baseW = F.regimes.weights.slice();
  let userW = baseW.slice();
  const terc = {};
  async function loadSamples() {
    if (SAM) return;
    SAM = await (await fetch(`${ROOTP}/data/samples.json`)).json();
    ["reg_lag", "util_g0", "new_max", "slot_g"].forEach((k) => { const v = SAM.inputs[k].slice().sort((a, b) => a - b); terc[k] = [v[Math.floor(v.length / 3)], v[Math.floor((2 * v.length) / 3)]]; });
    const cnt = [0, 0, 0, 0]; SAM.inputs.regime.forEach((r) => cnt[r]++);
    SAM.freq = cnt.map((c) => c / SAM.n);
    explorerRender();
  }
  function weightsUI() {
    const el = $("#weights");
    if (!el) return;
    el.replaceChildren();
    F.regimes.names.forEach((n, r) => {
      const row = document.createElement("label"); row.className = "wslider";
      const a = document.createElement("span"); a.textContent = n;
      const inp = document.createElement("input"); inp.type = "range"; inp.min = 0; inp.max = 100; inp.value = Math.round(userW[r] * 100); inp.setAttribute("aria-label", n + " weight");
      const v = document.createElement("span"); v.className = "wval"; v.textContent = inp.value + "%";
      inp.addEventListener("input", () => { userW[r] = +inp.value / 100; v.textContent = inp.value + "%"; explorerRender(); });
      row.append(a, inp, v); el.appendChild(row);
    });
  }
  if (has("#resetW")) $("#resetW").addEventListener("click", () => { userW = baseW.slice(); weightsUI(); explorerRender(); });
  document.querySelectorAll("#filters .chips").forEach((seg) => seg.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => {
    seg.querySelectorAll("button").forEach((x) => x.setAttribute("aria-pressed", x === b));
    filt[seg.dataset.filter] = b.dataset.v; explorerRender();
  })));
  function wq(vals, w, q) {
    const idx = vals.map((v, i) => i).sort((a, b) => vals[a] - vals[b]);
    const tot = w.reduce((s, x) => s + x, 0);
    let c = 0;
    for (const i of idx) { c += w[i]; if (c >= q * tot) return vals[i]; }
    return vals[idx[idx.length - 1]];
  }
  function explorerRender() {
    if (!SAM || !has("#exChart")) return;
    const n = SAM.n, I = SAM.inputs, keep = [], w = [];
    for (let i = 0; i < n; i++) {
      if (filt.regime !== "any" && I.regime[i] !== +filt.regime) continue;
      let ok = true;
      for (const k of ["reg_lag", "util_g0", "new_max", "slot_g"]) {
        if (filt[k] === "any") continue;
        const v = I[k][i], [a, b] = terc[k];
        if ((v < a ? "lo" : v < b ? "mid" : "hi") !== filt[k]) { ok = false; break; }
      }
      if (!ok) continue;
      keep.push(i);
      w.push(filt.regime === "any" ? userW[I.regime[i]] / SAM.freq[I.regime[i]] : 1);
    }
    const mc = $("#matchCount");
    mc.innerHTML = keep.length < 30 ? `<b>${keep.length}</b> of ${n} futures match. Too few for stable estimates; relax a filter.`
      : `<b>${keep.length}</b> of ${n} sampled futures match${filt.regime === "any" ? ", weighted by your regime weights" : ""}.`;
    if (keep.length < 5) return;
    const qs = (key) => {
      const out = { p10: [], p25: [], p50: [], p75: [], p90: [] };
      SAM.outputs[key].forEach((arr) => { const vals = keep.map((i) => arr[i] / 1000); [10, 25, 50, 75, 90].forEach((q) => out["p" + q].push(wq(vals, w, q / 100))); });
      return out;
    };
    const D = qs("D"), Sq = qs("Sd"), R = qs("R");
    const prob = (key, yr, test) => { const j = SAM.years.indexOf(yr); let s = 0, t = 0; keep.forEach((i, k) => { t += w[k]; if (test(SAM.outputs[key][j][i] / 1000)) s += w[k]; }); return s / t; };
    const te = $("#exTiles");
    te.replaceChildren();
    [["P(oversupply) 2035", fmt.pct(prob("R", 2035, (v) => v > 1.1))], ["P(oversupply) 2045", fmt.pct(prob("R", 2045, (v) => v > 1.1))],
      ["P(oversupply) 2055", fmt.pct(prob("R", 2055, (v) => v > 1.1))], ["Median FTE demand 2045", fmt.x2(D.p50[yi(2045)])]].forEach(([l, v]) => {
      const d = document.createElement("div"); d.className = "tile";
      const a = document.createElement("div"); a.className = "label"; a.style.minHeight = "0"; a.textContent = l;
      const b = document.createElement("div"); b.className = "value"; b.style.fontSize = "28px"; b.textContent = v;
      d.append(a, b); te.appendChild(d);
    });
    const c = col();
    const pick = keep.filter((_, k) => k % Math.max(1, Math.floor(keep.length / 24)) === 0).slice(0, 24);
    Charts.fan("#exChart", { years, height: 340, yDomain: [0.3, 2.0], mark: youMark(), bands: [[10, 90]], refs: [{ y: 1 }], yLabel: "Radiologist FTEs (2026 demand = 1)",
      series: [{ label: "Demand", color: c.d, q: D }, { label: "Supply", color: c.s, q: Sq }],
      extraLines: pick.map((i) => ({ values: SAM.outputs.D.map((arr) => arr[i] / 1000), color: c.d, opacity: 0.28, width: 0.9 })) });
    Charts.fan("#exRatio", { years, height: 260, yDomain: [0.5, 2.0], bands: [[10, 90], [25, 75]], yLabel: "Supply ÷ demand",
      series: [{ label: "S ÷ D", color: c.r, q: R }], refs: [{ y: 1, color: css("--ink-2"), label: "balance" }, { y: 1.1, color: c.red, label: "oversupply" }] });
  }
  if (has("#explore")) {
    const exIO = new IntersectionObserver((e) => { if (e.some((x) => x.isIntersecting)) { exIO.disconnect(); loadSamples(); } }, { rootMargin: "400px" });
    exIO.observe($("#explore"));
    weightsUI();
  }

  // ------------------------------------------------------------------ render all + theme/resize
  function renderAll() {
    stageUI();
    heroChart(); dashChart(); careerTrack(); setYear(curYear, curTag);
    diagram(); regimeChart(); backtestChart(); forecastCharts(); headlineTable(); aiCharts(); jevonsCharts();
    tornadoChart(); etaChart(); evidenceChart(); compChart(); careerTable(); horizon(); explorerRender(); robustTable();
  }
  signposts(); paramTable();
  renderAll();
  cite();

  if (has("#themeBtn")) $("#themeBtn").addEventListener("click", () => {
    const cur = document.documentElement.dataset.theme === "dark" ? "dark" : "light"; // light unless the reader chose dark
    const next = cur === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (e) { /* storage unavailable */ }
    renderAll();
  });
  let rw = 0, lastW = window.innerWidth;
  window.addEventListener("resize", () => { if (Math.abs(window.innerWidth - lastW) < 40) return; lastW = window.innerWidth; clearTimeout(rw); rw = setTimeout(renderAll, 200); });
  const prog = $("#progress");
  const navs = [...document.querySelectorAll(".navlinks a[href^='#']")];
  const secs = navs.map((a) => document.querySelector(a.getAttribute("href")));
  window.addEventListener("scroll", () => {
    const h = document.documentElement;
    if (prog) prog.style.width = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100 + "%";
    let act = -1;
    secs.forEach((s, i) => { if (s && s.getBoundingClientRect().top < 120) act = i; });
    navs.forEach((a, i) => a.classList.toggle("active", i === act));
  }, { passive: true });
})();
