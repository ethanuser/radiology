/* Reusable D3 chart components. Colours come from CSS custom properties so light/dark themes work.
   Every chart takes axis titles: { xLabel, yLabel }. */
/* global d3 */
const Charts = (() => {
  const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const tip = document.getElementById("tooltip");
  const fmt = {
    x2: d3.format(".2f"),
    pct: (v) => (v > 0 && v < 0.005 ? "<1%" : d3.format(".0%")(v)),
    pct1: d3.format(".1%"),
    chg: (v) => (v >= 1 ? "+" : "−") + d3.format(".0%")(Math.abs(v - 1)),
    mult: (v) => d3.format(".2f")(v) + "×",
  };

  // ---------------------------------------------------------------- tooltip (DOM-built; labels via textContent)
  function tipShow(ev, title, rows) {
    if (!tip) return;
    tip.replaceChildren();
    const h = document.createElement("div");
    h.className = "tt-h";
    h.textContent = title;
    tip.appendChild(h);
    rows.forEach((r) => {
      const row = document.createElement("div");
      row.className = "row";
      const i = document.createElement("i");
      i.style.background = r.color || "transparent";
      const s = document.createElement("span");
      s.textContent = r.label;
      const b = document.createElement("b");
      b.textContent = r.value;
      row.append(i, s, b);
      tip.appendChild(row);
    });
    tip.style.opacity = 1;
    tipMove(ev);
  }
  function tipMove(ev) {
    const pad = 14, w = tip.offsetWidth, h = tip.offsetHeight;
    let x = ev.clientX + pad, y = ev.clientY + pad;
    if (x + w > window.innerWidth - 8) x = ev.clientX - w - pad;
    if (y + h > window.innerHeight - 8) y = ev.clientY - h - pad;
    tip.style.left = x + "px";
    tip.style.top = y + "px";
  }
  function tipHide() { if (tip) tip.style.opacity = 0; }

  function frame(el, { height = 320, margin = { t: 14, r: 64, b: 30, l: 44 }, xLabel, yLabel } = {}) {
    const node = typeof el === "string" ? document.querySelector(el) : el;
    if (!node) return null;
    node.replaceChildren();
    const m = { ...margin };
    if (xLabel) m.b += 18;
    if (yLabel) m.l += 18;
    const width = Math.max(280, node.clientWidth || 600);
    const svg = d3.select(node).append("svg").attr("viewBox", `0 0 ${width} ${height}`).attr("preserveAspectRatio", "xMinYMin meet");
    const g = svg.append("g").attr("transform", `translate(${m.l},${m.t})`);
    const F = { node, svg, g, w: width - m.l - m.r, h: height - m.t - m.b, width, height, margin: m };
    if (xLabel) svg.append("text").attr("class", "axis-title").attr("x", m.l + F.w / 2).attr("y", height - 4)
      .attr("text-anchor", "middle").text(xLabel);
    if (yLabel) svg.append("text").attr("class", "axis-title").attr("transform", `translate(12,${m.t + F.h / 2}) rotate(-90)`)
      .attr("text-anchor", "middle").text(yLabel);
    return F;
  }

  function axes(F, x, y, { yFmt = (d) => d, xTicks = 8, yTicks = 5 } = {}) {
    F.g.append("g").attr("class", "gridline").call(d3.axisLeft(y).ticks(yTicks).tickSize(-F.w).tickFormat(""));
    F.g.append("g").attr("class", "axis").attr("transform", `translate(0,${F.h})`)
      .call(d3.axisBottom(x).ticks(Math.min(xTicks, Math.floor(F.w / 60))).tickFormat(d3.format("d")).tickSizeOuter(0));
    F.g.append("g").attr("class", "axis").call(d3.axisLeft(y).ticks(yTicks).tickFormat(yFmt).tickSizeOuter(0))
      .call((s) => s.select(".domain").remove());
  }

  function legend(F, items) {
    const lg = d3.select(F.node).append("div").attr("class", "dash-legend").style("margin", "6px 4px 0");
    items.forEach((s) => {
      const k = lg.append("span").attr("class", "key");
      const i = k.append("i").style("background", s.box ? s.color : s.color);
      if (s.box) i.attr("class", "box").style("opacity", s.opacity || 1);
      if (s.dash) i.style("background", "none").style("border-top", `2px dashed ${s.color}`).style("height", "0");
      k.append("span").text(s.label);
    });
  }

  // ---------------------------------------------------------------- fan chart
  function fan(el, { years, series, height = 320, yDomain, yFmt = fmt.x2, refs = [], mark, endLabels = true, animate = false,
    reveal = null, valueFmt = fmt.x2, bands = [[10, 90], [25, 75]], extraLines = [], xLabel = "Year", yLabel, showLegend = false }) {
    const F = frame(el, { height, margin: { t: 14, r: endLabels ? 70 : 16, b: 28, l: 44 }, xLabel, yLabel });
    if (!F) return null;
    const x = d3.scaleLinear().domain(d3.extent(years)).range([0, F.w]);
    let lo = d3.min(series, (s) => d3.min(s.q.p10)), hi = d3.max(series, (s) => d3.max(s.q.p90));
    extraLines.forEach((l) => { lo = Math.min(lo, d3.min(l.values)); hi = Math.max(hi, d3.max(l.values)); });
    const y = d3.scaleLinear().domain(yDomain || [Math.min(lo, ...refs.map((r) => r.y)) * 0.97, Math.max(hi, ...refs.map((r) => r.y)) * 1.03]).nice().range([F.h, 0]);
    axes(F, x, y, { yFmt });
    const clipId = "clip" + Math.random().toString(36).slice(2);
    const clipRect = F.svg.append("defs").append("clipPath").attr("id", clipId).append("rect")
      .attr("x", -2).attr("y", -3).attr("height", F.h + 6).attr("width", animate ? 0 : (reveal ? x(reveal) + 2 : F.w + 4));
    const plot = F.g.append("g").attr("clip-path", `url(#${clipId})`);
    refs.forEach((r, i) => { // alternate label sides so close reference lines don't collide
      F.g.append("line").attr("x1", 0).attr("x2", F.w).attr("y1", y(r.y)).attr("y2", y(r.y)).attr("stroke", r.color || css("--axis")).attr("stroke-width", 1);
      if (r.label) F.g.append("text").attr("x", i % 2 ? F.w - 4 : 4).attr("text-anchor", i % 2 ? "end" : "start")
        .attr("y", y(r.y) - 4).attr("class", "lbl-ink2 halo").text(r.label);
    });
    series.forEach((s) => {
      bands.forEach(([a, b], k) => {
        const area = d3.area().x((d, i) => x(years[i])).y0((d, i) => y(s.q["p" + a][i])).y1((d, i) => y(s.q["p" + b][i])).curve(d3.curveMonotoneX);
        plot.append("path").attr("d", area(years)).attr("fill", s.color).attr("opacity", k === 0 ? 0.13 : 0.2);
      });
    });
    extraLines.forEach((l) => {
      const line = d3.line().x((d, i) => x(years[i])).y((d) => y(d)).curve(d3.curveMonotoneX);
      plot.append("path").attr("d", line(l.values)).attr("fill", "none").attr("stroke", l.color).attr("stroke-width", l.width || 0.8).attr("opacity", l.opacity || 0.35)
        .attr("stroke-dasharray", l.dash || null);
      if (l.endLabel) plot.append("text").attr("x", F.w - 4).attr("y", y(l.values[l.values.length - 1]) - 7).attr("text-anchor", "end")
        .attr("class", "lbl-ink2 halo").text(l.endLabel);
    });
    series.forEach((s) => {
      const line = d3.line().x((d, i) => x(years[i])).y((d) => y(d)).curve(d3.curveMonotoneX);
      plot.append("path").attr("d", line(s.q.p50)).attr("fill", "none").attr("stroke", s.color).attr("stroke-width", 2.2).attr("stroke-linecap", "round");
    });
    if (endLabels) {
      const last = years.length - 1;
      const pts = series.map((s) => ({ s, y: y(s.q.p50[last]) })).sort((a, b) => a.y - b.y);
      for (let i = 1; i < pts.length; i++) if (pts[i].y - pts[i - 1].y < 32) pts[i].y = pts[i - 1].y + 32;
      const over = pts.length ? pts[pts.length - 1].y + 16 - F.h : 0; // keep the stack inside the plot
      if (over > 0) pts.forEach((p) => { p.y -= over; });
      pts.forEach((p) => {
        const t = F.g.append("text").attr("x", F.w + 8).attr("y", p.y).attr("class", "lbl-ink").attr("dy", "-0.1em");
        t.append("tspan").text(p.s.label);
        t.append("tspan").attr("x", F.w + 8).attr("dy", "1.15em").attr("class", "lbl-ink2").text((p.s.fmt || valueFmt)(p.s.q.p50[last]));
      });
    }
    let markG = null;
    const drawMark = (m) => {
      if (markG) markG.remove();
      if (!m) return;
      markG = F.g.append("g");
      markG.append("line").attr("x1", x(m.x)).attr("x2", x(m.x)).attr("y1", 0).attr("y2", F.h).attr("stroke", css("--ink-2")).attr("stroke-dasharray", "3 3");
      markG.append("text").attr("x", x(m.x) + 4).attr("y", F.h - 6).attr("class", "lbl-ink2 halo").text(m.label);
    };
    drawMark(mark);
    let cursor = null;
    if (reveal !== null) cursor = F.g.append("line").attr("y1", 0).attr("y2", F.h).attr("stroke", css("--ink")).attr("stroke-width", 1.2).attr("x1", x(reveal)).attr("x2", x(reveal));
    if (animate) clipRect.transition().duration(reduced ? 0 : 1800).ease(d3.easeCubicOut).attr("width", F.w + 4);
    const hover = F.g.append("g").style("display", "none");
    const vline = hover.append("line").attr("y1", 0).attr("y2", F.h).attr("stroke", css("--muted")).attr("stroke-width", 1);
    const dots = series.map((s) => hover.append("circle").attr("r", 4.5).attr("fill", s.color).attr("stroke", css("--surface")).attr("stroke-width", 2));
    F.g.append("rect").attr("width", F.w).attr("height", F.h).attr("fill", "transparent")
      .on("pointermove", (ev) => {
        const [mx] = d3.pointer(ev);
        const yr = Math.round(x.invert(mx));
        const i = Math.max(0, Math.min(years.length - 1, years.indexOf(yr) >= 0 ? years.indexOf(yr) : 0));
        if (reveal !== null && years[i] > reveal) { hover.style("display", "none"); tipHide(); return; }
        hover.style("display", null);
        vline.attr("x1", x(years[i])).attr("x2", x(years[i]));
        series.forEach((s, k) => dots[k].attr("cx", x(years[i])).attr("cy", y(s.q.p50[i])));
        tipShow(ev, String(years[i]), series.map((s) => ({
          color: s.color, label: s.label + " (median, 80% range)",
          value: `${(s.fmt || valueFmt)(s.q.p50[i])}  (${(s.fmt || valueFmt)(s.q.p10[i])}–${(s.fmt || valueFmt)(s.q.p90[i])})`,
        })));
      })
      .on("pointerleave", () => { hover.style("display", "none"); tipHide(); });
    if (showLegend) legend(F, [...series.map((s) => ({ label: s.label + " (median)", color: s.color })),
      ...extraLines.filter((l) => l.label).map((l) => ({ label: l.label, color: l.color, dash: !!l.dash })),
      ...(bands.some((b) => b[0] === 25) ? [{ label: "50% range", color: series[0].color, box: true, opacity: 0.45 }] : []),
      { label: "80% range", color: series[0].color, box: true, opacity: 0.2 }]);
    return {
      setReveal(yr) {
        clipRect.transition().duration(reduced ? 0 : 700).ease(d3.easeCubicInOut).attr("width", x(yr) + 2);
        if (cursor) cursor.transition().duration(reduced ? 0 : 700).attr("x1", x(yr)).attr("x2", x(yr));
        reveal = yr;
      },
      setMark: drawMark,
    };
  }

  // ---------------------------------------------------------------- multi-line
  function lines(el, { years, series, height = 300, yDomain, yFmt = fmt.pct, valueFmt = fmt.pct, refs = [], mark, legend: showLegend = false,
    xLabel = "Year", yLabel }) {
    const F = frame(el, { height, margin: { t: 14, r: 52, b: 28, l: 44 }, xLabel, yLabel });
    if (!F) return;
    const x = d3.scaleLinear().domain(d3.extent(years)).range([0, F.w]);
    const y = d3.scaleLinear().domain(yDomain || [0, d3.max(series, (s) => d3.max(s.values)) * 1.08]).nice().range([F.h, 0]);
    axes(F, x, y, { yFmt });
    refs.forEach((r) => F.g.append("line").attr("x1", 0).attr("x2", F.w).attr("y1", y(r.y)).attr("y2", y(r.y)).attr("stroke", r.color || css("--axis")));
    const line = d3.line().x((d, i) => x(years[i])).y((d) => y(d)).curve(d3.curveMonotoneX);
    series.forEach((s) => F.g.append("path").attr("d", line(s.values)).attr("fill", "none").attr("stroke", s.color).attr("stroke-width", s.width || 2).attr("stroke-dasharray", s.dash || null));
    const last = years.length - 1;
    const pts = series.filter((s) => !s.noLabel).map((s) => ({ s, y: y(s.values[last]) })).sort((a, b) => a.y - b.y);
    for (let i = 1; i < pts.length; i++) if (pts[i].y - pts[i - 1].y < 13) pts[i].y = pts[i - 1].y + 13;
    pts.forEach((p) => F.g.append("text").attr("x", F.w + 6).attr("y", p.y).attr("dy", "0.32em").attr("class", "lbl-ink2").text(valueFmt(p.s.values[last])));
    if (mark) {
      F.g.append("line").attr("x1", x(mark.x)).attr("x2", x(mark.x)).attr("y1", 0).attr("y2", F.h).attr("stroke", css("--ink-2")).attr("stroke-dasharray", "3 3");
      F.g.append("text").attr("x", x(mark.x) + 4).attr("y", 10).attr("class", "lbl-ink2 halo").text(mark.label);
    }
    const hover = F.g.append("g").style("display", "none");
    const vline = hover.append("line").attr("y1", 0).attr("y2", F.h).attr("stroke", css("--muted"));
    const dots = series.map((s) => hover.append("circle").attr("r", 4.5).attr("fill", s.color).attr("stroke", css("--surface")).attr("stroke-width", 2));
    F.g.append("rect").attr("width", F.w).attr("height", F.h).attr("fill", "transparent")
      .on("pointermove", (ev) => {
        const [mx] = d3.pointer(ev);
        const i = Math.max(0, Math.min(years.length - 1, Math.round(x.invert(mx)) - years[0]));
        hover.style("display", null);
        vline.attr("x1", x(years[i])).attr("x2", x(years[i]));
        series.forEach((s, k) => dots[k].attr("cx", x(years[i])).attr("cy", y(s.values[i])));
        tipShow(ev, String(years[i]), series.map((s) => ({ color: s.color, label: s.label, value: valueFmt(s.values[i]) })));
      })
      .on("pointerleave", () => { hover.style("display", "none"); tipHide(); });
    if (showLegend) legend(F, series.map((s) => ({ label: s.label, color: s.color, dash: !!s.dash })));
  }

  // ---------------------------------------------------------------- stacked area (+/-) with overlay lines
  function stacked(el, { years, layers, overlays = [], height = 340, yFmt = (d) => d, valueFmt = fmt.x2, yDomain, showLegend = true,
    xLabel = "Year", yLabel }) {
    const F = frame(el, { height, margin: { t: 14, r: 16, b: 28, l: 48 }, xLabel, yLabel });
    if (!F) return;
    const x = d3.scaleLinear().domain(d3.extent(years)).range([0, F.w]);
    const pos = layers.filter((l) => d3.mean(l.values) >= 0), neg = layers.filter((l) => d3.mean(l.values) < 0);
    const cum = (ls) => { const base = years.map(() => 0); return ls.map((l) => { const y0 = base.slice(); l.values.forEach((v, i) => { base[i] += v; }); return { l, y0, y1: base.slice() }; }); };
    const P = cum(pos), N = cum(neg);
    const top = d3.max([...P.map((p) => d3.max(p.y1)), ...overlays.map((o) => d3.max(o.values)), 0]);
    const bot = d3.min([...N.map((p) => d3.min(p.y1)), 0]);
    const y = d3.scaleLinear().domain(yDomain || [bot * 1.1, top * 1.08]).nice().range([F.h, 0]);
    axes(F, x, y, { yFmt });
    const area = d3.area().x((d, i) => x(years[i])).curve(d3.curveMonotoneX);
    [...P, ...N].forEach((p) => F.g.append("path").attr("d", area.y0((d, i) => y(p.y0[i])).y1((d, i) => y(p.y1[i]))(years))
      .attr("fill", p.l.color).attr("opacity", 0.85).attr("stroke", css("--surface")).attr("stroke-width", 1));
    F.g.append("line").attr("x1", 0).attr("x2", F.w).attr("y1", y(0)).attr("y2", y(0)).attr("stroke", css("--axis"));
    const line = d3.line().x((d, i) => x(years[i])).y((d) => y(d)).curve(d3.curveMonotoneX);
    overlays.forEach((o) => F.g.append("path").attr("d", line(o.values)).attr("fill", "none").attr("stroke", o.color).attr("stroke-width", o.width || 2.2).attr("stroke-dasharray", o.dash || null));
    const hover = F.g.append("g").style("display", "none");
    const vline = hover.append("line").attr("y1", 0).attr("y2", F.h).attr("stroke", css("--muted"));
    F.g.append("rect").attr("width", F.w).attr("height", F.h).attr("fill", "transparent")
      .on("pointermove", (ev) => {
        const [mx] = d3.pointer(ev);
        const i = Math.max(0, Math.min(years.length - 1, Math.round(x.invert(mx)) - years[0]));
        hover.style("display", null);
        vline.attr("x1", x(years[i])).attr("x2", x(years[i]));
        tipShow(ev, String(years[i]), [...overlays.map((o) => ({ color: o.color, label: o.label, value: valueFmt(o.values[i]) })),
          ...layers.slice().reverse().map((l) => ({ color: l.color, label: l.label, value: valueFmt(l.values[i]) }))]);
      })
      .on("pointerleave", () => { hover.style("display", "none"); tipHide(); });
    if (showLegend) legend(F, [...overlays.map((o) => ({ label: o.label, color: o.color, dash: !!o.dash })), ...layers.map((l) => ({ label: l.label, color: l.color, box: true }))]);
  }

  // ---------------------------------------------------------------- tornado
  function tornado(el, rows, metric, { pctScale = metric.startsWith("pOver"), xLabel, yLabel = "Assumption group" } = {}) {
    const data = rows.filter((r) => Math.abs(r[metric + "_high"] - r[metric + "_low"]) > 1e-6)
      .sort((a, b) => Math.abs(b[metric + "_high"] - b[metric + "_low"]) - Math.abs(a[metric + "_high"] - a[metric + "_low"]));
    const narrow = (document.querySelector(el)?.clientWidth || 700) < 560;
    const rowH = narrow ? 42 : 30;
    const F = frame(el, { height: data.length * rowH + (narrow ? 14 : 8) + 28 + (xLabel ? 18 : 0) + 4, margin: { t: narrow ? 14 : 8, r: narrow ? 16 : 46, b: 28, l: narrow ? 8 : 220 }, xLabel, yLabel: narrow ? null : yLabel });
    if (!F) return;
    const base = rows[0][metric + "_base"];
    const vals = data.flatMap((r) => [r[metric + "_low"], r[metric + "_high"], base]);
    const x = d3.scaleLinear().domain(d3.extent(vals)).nice().range([0, F.w]);
    const y = d3.scaleBand().domain(data.map((r) => r.group)).range([0, data.length * rowH]).paddingInner(narrow ? 0.5 : 0.28).paddingOuter(0.2).align(1);
    const vf = pctScale ? fmt.pct : fmt.x2;
    F.g.append("g").attr("class", "gridline").attr("transform", `translate(0,${data.length * rowH})`).call(d3.axisBottom(x).ticks(narrow ? 4 : 6).tickSize(-data.length * rowH).tickFormat(""));
    F.g.append("g").attr("class", "axis").attr("transform", `translate(0,${data.length * rowH})`).call(d3.axisBottom(x).ticks(narrow ? 4 : Math.floor(F.w / 70)).tickFormat(vf).tickSizeOuter(0));
    data.forEach((r) => {
      const g = F.g.append("g").attr("transform", `translate(0,${y(r.group)})`);
      const lo = r[metric + "_low"], hi = r[metric + "_high"];
      [[lo, css("--s1")], [hi, css("--s2")]].forEach(([v, c]) => {
        const x0 = Math.min(x(base), x(v)), wd = Math.max(1.5, Math.abs(x(v) - x(base)));
        g.append("rect").attr("x", x0).attr("width", 0).attr("height", y.bandwidth()).attr("rx", 3).attr("fill", c).attr("opacity", r.focus ? 0.95 : 0.5)
          .on("pointermove", (ev) => tipShow(ev, r.group, [
            { color: css("--s1"), label: "group at its 10th percentile", value: vf(lo) },
            { color: css("--s2"), label: "group at its 90th percentile", value: vf(hi) },
            { color: css("--ink"), label: "all assumptions uncertain", value: vf(base) },
            { label: "parameters: " + r.members, value: "" }]))
          .on("pointerleave", tipHide)
          .transition().duration(reduced ? 0 : 700).attr("width", wd);
      });
      const t = F.g.append("text").attr("class", r.focus ? "lbl-ink" : "lbl-ink2").text((r.focus ? "● " : "") + r.group);
      if (narrow) t.attr("x", 0).attr("y", y(r.group) - 4);
      else t.attr("x", -10).attr("y", y(r.group) + y.bandwidth() / 2).attr("dy", "0.32em").attr("text-anchor", "end");
    });
    F.g.append("line").attr("x1", x(base)).attr("x2", x(base)).attr("y1", -4).attr("y2", data.length * rowH).attr("stroke", css("--ink"));
    F.g.append("text").attr("x", x(base) + 4).attr("y", data.length * rowH).attr("dy", "-0.3em").attr("class", "lbl-ink2 halo").text("all uncertain: " + vf(base));
  }

  // ---------------------------------------------------------------- horizontal bars
  function hbars(el, rows, { valueFmt = fmt.x2, max, colorFn, badge, height, xLabel, yLabel } = {}) {
    const narrow = (document.querySelector(el)?.clientWidth || 700) < 520;
    const rowH = narrow ? 38 : 26;
    const F = frame(el, { height: height || rows.length * rowH + (narrow ? 14 : 4) + 24 + (xLabel ? 18 : 0) + 4, margin: { t: narrow ? 14 : 4, r: 48, b: 24, l: narrow ? 6 : 250 }, xLabel, yLabel: narrow ? null : yLabel });
    if (!F) return;
    const x = d3.scaleLinear().domain([0, max || d3.max(rows, (r) => r.value) * 1.05]).nice().range([0, F.w]);
    const y = d3.scaleBand().domain(rows.map((r, i) => i)).range([0, rows.length * rowH]).paddingInner(narrow ? 0.5 : 0.3).paddingOuter(0.2).align(1);
    F.g.append("g").attr("class", "gridline").attr("transform", `translate(0,${rows.length * rowH})`).call(d3.axisBottom(x).ticks(5).tickSize(-rows.length * rowH).tickFormat(""));
    F.g.append("g").attr("class", "axis").attr("transform", `translate(0,${rows.length * rowH})`).call(d3.axisBottom(x).ticks(narrow ? 4 : 5).tickFormat(valueFmt).tickSizeOuter(0));
    rows.forEach((r, i) => {
      const c = colorFn ? colorFn(r) : css("--s1");
      F.g.append("rect").attr("x", 0).attr("y", y(i)).attr("height", y.bandwidth()).attr("rx", 3).attr("width", 0).attr("fill", c)
        .on("pointermove", (ev) => tipShow(ev, r.label, [{ color: c, label: r.tipLabel || "value", value: valueFmt(r.value) }]))
        .on("pointerleave", tipHide)
        .transition().duration(reduced ? 0 : 600).delay(i * 25).attr("width", Math.max(1, x(r.value)));
      F.g.append("text").attr("x", x(r.value) + 5).attr("y", y(i) + y.bandwidth() / 2).attr("dy", "0.32em").attr("class", "lbl-ink2").text(valueFmt(r.value));
      const lab = F.g.append("text").attr("class", "lbl-ink2");
      const maxChars = narrow ? 44 : 40;
      lab.text((r.label.length > maxChars ? r.label.slice(0, maxChars - 1) + "…" : r.label) + (badge ? `  [${badge(r)}]` : ""));
      if (narrow) lab.attr("x", 0).attr("y", y(i) - 4);
      else lab.attr("x", -8).attr("y", y(i) + y.bandwidth() / 2).attr("dy", "0.32em").attr("text-anchor", "end");
      lab.append("title").text(r.label);
    });
  }

  // ---------------------------------------------------------------- regulatory pipeline dot-range
  function pipeline(el, P, { xLabel = "Year (dot = median, line = 80% range)", yLabel = "Tier of exam difficulty" } = {}) {
    const narrow = (document.querySelector(el)?.clientWidth || 700) < 560;
    const tiers = P.tiers, stages = P.stages, rowH = 92;
    const F = frame(el, { height: tiers.length * rowH + 10 + 30 + (xLabel ? 18 : 0) + 4, margin: { t: 10, r: 18, b: 30, l: narrow ? 70 : 210 }, xLabel, yLabel: narrow ? null : yLabel });
    if (!F) return;
    const x = d3.scaleLinear().domain([2024, 2085]).range([0, F.w]);
    const colors = [css("--s1"), css("--s2"), css("--s3"), css("--s4"), css("--s7")];
    F.g.append("g").attr("class", "gridline").attr("transform", `translate(0,${tiers.length * rowH})`).call(d3.axisBottom(x).ticks(7).tickSize(-tiers.length * rowH).tickFormat(""));
    F.g.append("g").attr("class", "axis").attr("transform", `translate(0,${tiers.length * rowH})`).call(d3.axisBottom(x).ticks(Math.floor(F.w / 70)).tickFormat(d3.format("d")).tickSizeOuter(0));
    F.g.append("line").attr("x1", x(2066)).attr("x2", x(2066)).attr("y1", 0).attr("y2", tiers.length * rowH).attr("stroke", css("--axis"));
    F.g.append("text").attr("x", x(2066) + 4).attr("y", 10).attr("class", "lbl-ink2").text("end of forecast");
    tiers.forEach((t, j) => {
      const y0 = j * rowH + 14;
      F.g.append("text").attr("x", -10).attr("y", y0 + 32).attr("text-anchor", "end").attr("class", "lbl-ink").text(`Tier ${j + 1}`);
      if (!narrow) F.g.append("text").attr("x", -10).attr("y", y0 + 48).attr("text-anchor", "end").attr("class", "lbl-ink2").text(t);
      else F.g.append("text").attr("x", -60).attr("y", y0 + 72).attr("class", "lbl-ink2").text(t);
      stages.forEach((s, k) => {
        const yy = y0 + k * 13;
        const lo = Math.max(2024, P.p10[j][k]), hi = Math.min(2085, P.p90[j][k]), med = P.p50[j][k];
        F.g.append("line").attr("x1", x(lo)).attr("x2", x(lo)).attr("y1", yy).attr("y2", yy).attr("stroke", colors[k]).attr("stroke-width", 2.5).attr("opacity", 0.55).attr("stroke-linecap", "round")
          .transition().duration(reduced ? 0 : 900).delay(j * 150 + k * 60).attr("x2", x(hi));
        if (med <= 2085) {
          F.g.append("circle").attr("cx", x(Math.max(2024, med))).attr("cy", yy).attr("r", 0).attr("fill", colors[k]).attr("stroke", css("--surface")).attr("stroke-width", 2)
            .on("pointermove", (ev) => tipShow(ev, `Tier ${j + 1}: ${s}`, [{ color: colors[k], label: "median year", value: d3.format("d")(med) },
              { label: "80% range", value: `${d3.format("d")(P.p10[j][k])}–${P.p90[j][k] > 2100 ? "2100+" : d3.format("d")(P.p90[j][k])}` }]))
            .on("pointerleave", tipHide)
            .transition().duration(reduced ? 0 : 500).delay(j * 150 + k * 60 + 300).attr("r", 5);
        }
      });
    });
    legend(F, stages.map((s, k) => ({ label: s, color: colors[k], box: true })));
  }

  // ---------------------------------------------------------------- backtest interval chart
  function backtest(el, B, { xLabel = "Employment in 2025 relative to 2016 (1.0 = unchanged)" } = {}) {
    const rows = B.occupations;
    const narrow = (document.querySelector(el)?.clientWidth || 700) < 560;
    const rowH = 64;
    const F = frame(el, { height: rows.length * rowH + 8 + 34 + 18, margin: { t: 8, r: 20, b: 34, l: narrow ? 8 : 190 }, xLabel, yLabel: narrow ? null : "Occupation" });
    if (!F) return;
    const vals = rows.flatMap((r) => [r.q.p10, r.q.p90, r.actual, r.trend, r.bls]);
    const x = d3.scaleLinear().domain([Math.min(0.9, d3.min(vals)) * 0.95, d3.max(vals) * 1.03]).nice().range([0, F.w]);
    F.g.append("g").attr("class", "gridline").attr("transform", `translate(0,${rows.length * rowH})`).call(d3.axisBottom(x).ticks(6).tickSize(-rows.length * rowH).tickFormat(""));
    F.g.append("g").attr("class", "axis").attr("transform", `translate(0,${rows.length * rowH})`).call(d3.axisBottom(x).ticks(6).tickFormat(d3.format(".1f")).tickSizeOuter(0));
    F.g.append("line").attr("x1", x(1)).attr("x2", x(1)).attr("y1", 0).attr("y2", rows.length * rowH).attr("stroke", css("--axis"));
    const sym = { actual: [d3.symbolDiamond, css("--ink"), "Actual (2025)"], bls: [d3.symbolSquare, css("--s2"), "BLS projection made in 2016"],
      trend: [d3.symbolTriangle, css("--s3"), "Prior-decade trend"], model: [d3.symbolCircle, css("--s1"), "Structured model (median)"] };
    rows.forEach((r, i) => {
      const yy = i * rowH + rowH / 2;
      const lab = F.g.append("text").attr("class", "lbl-ink").text(r.label);
      if (narrow) lab.attr("x", 0).attr("y", yy - 18); else lab.attr("x", -10).attr("y", yy).attr("dy", "0.32em").attr("text-anchor", "end");
      F.g.append("line").attr("x1", x(r.q.p10)).attr("x2", x(r.q.p90)).attr("y1", yy).attr("y2", yy).attr("stroke", css("--s1")).attr("stroke-width", 8).attr("opacity", 0.22);
      F.g.append("line").attr("x1", x(r.q.p25)).attr("x2", x(r.q.p75)).attr("y1", yy).attr("y2", yy).attr("stroke", css("--s1")).attr("stroke-width", 8).attr("opacity", 0.5);
      [["model", r.q.p50, 0], ["trend", r.trend, -14], ["bls", r.bls, 14], ["actual", r.actual, 0]].forEach(([k, v, dy]) => {
        const [shape, c, label] = sym[k];
        F.g.append("path").attr("d", d3.symbol().type(shape).size(k === "actual" ? 110 : 80)()).attr("transform", `translate(${x(v)},${yy + dy})`)
          .attr("fill", c).attr("stroke", css("--surface")).attr("stroke-width", 1.5)
          .on("pointermove", (ev) => tipShow(ev, r.label, [{ color: c, label, value: d3.format(".2f")(v) },
            { label: "model 80% range", value: `${d3.format(".2f")(r.q.p10)}–${d3.format(".2f")(r.q.p90)}` }]))
          .on("pointerleave", tipHide);
      });
    });
    legend(F, [{ label: "Structured model 50% / 80% range", color: css("--s1"), box: true, opacity: 0.5 },
      ...Object.values(sym).map(([, c, l]) => ({ label: l, color: c, box: true }))]);
  }

  return { fan, lines, stacked, tornado, hbars, pipeline, backtest, fmt, css, tipShow, tipHide };
})();
