"""Build REPORT.md (and docs/report.html) from report/REPORT.src.md.

* `{{ expr }}` placeholders are evaluated against the model outputs in outputs/, so every number in the
  report is regenerated whenever the model is re-run.
* `[@key]` / `[@a; @b]` citations become AMA-style superscript numbers in order of first appearance, and a
  numbered reference list is appended.

    python tools/build_docs.py
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.params import PARAMS, REGIME_NAMES  # noqa: E402
from model.references import REFERENCES, format_ama  # noqa: E402
from model.stages import STAGES  # noqa: E402

OUT = ROOT / "outputs"


# ----------------------------------------------------------------------------------------------------- context
def _fmt_num(v: float) -> str:
    """Readable parameter values: years as integers, otherwise 3 significant digits."""
    return f"{v:.0f}" if abs(v) >= 1000 else f"{v:.3g}"


def _by(df: pd.DataFrame, key: str) -> dict:
    return {r[key]: r for r in df.to_dict("records")}


sm = _by(pd.read_csv(OUT / "summary_by_year.csv"), "year")
pr = _by(pd.read_csv(OUT / "probabilities_by_year.csv"), "year")
jv = _by(pd.read_csv(OUT / "jevons_by_year.csv"), "year")
rg = _by(pd.read_csv(OUT / "regimes.csv"), "regime")
tor = _by(pd.read_csv(OUT / "sensitivity_tornado.csv"), "group")
ev = pd.read_csv(OUT / "evidence_attribution.csv")
eta = pd.read_csv(OUT / "sensitivity_eta2.csv")
eta_nt = pd.read_csv(OUT / "sensitivity_eta2_excluding_transformative.csv")
val = json.loads((OUT / "validation.json").read_text())
x = json.loads((OUT / "extra_metrics.json").read_text())
bt = json.loads((OUT / "backtest.json").read_text())
rb = json.loads((OUT / "robustness.json").read_text())
YEARS5 = (2030, 2035, 2045, 2055, 2066)


def pct(v, d=0):
    v = float(v) * 100
    if 0 < v < 0.5 and d == 0:
        return "<1%"
    if v == 0:
        return "0%"
    return f"{v:.{d}f}%"


def num(v, d=2):
    return f"{float(v):.{d}f}"


def chg(v, d=0):
    return f"{(float(v) - 1) * 100:+.{d}f}%".replace("-", "−")


def yr(v):
    return f"{float(v):.0f}"


def ev_shrink(grade, year, metric="D"):
    r = ev[(ev["grade"] == grade) & (ev["year"] == year) & (ev["metric"] == metric)].iloc[0]
    return r["shrink"]


def ev_n(grade):
    return int(ev[ev["grade"] == grade]["n_params"].iloc[0])


def headline_table():
    rows = ["| Metric | " + " | ".join(str(y) for y in YEARS5) + " |", "|---|" + "---|" * len(YEARS5)]

    def band(key, fmt):
        return [f"{fmt(sm[y][f'{key}_p50'])} ({fmt(sm[y][f'{key}_p10'])}–{fmt(sm[y][f'{key}_p90'])})" for y in YEARS5]

    def iqr(key, fmt):
        return [f"{fmt(sm[y][f'{key}_p25'])}–{fmt(sm[y][f'{key}_p75'])}" for y in YEARS5]

    f2 = lambda v: num(v, 2)  # noqa: E731
    fp = lambda v: pct(v, 0)  # noqa: E731
    lines = [
        ("**FTE demand** (2026 demand = 1): median (P10–P90)", band("demand", f2)),
        ("  FTE demand: P25–P75", iqr("demand", f2)),
        ("**FTE supply** (2026 demand = 1): median (P10–P90)", band("supplyd", f2)),
        ("  FTE supply: P25–P75", iqr("supplyd", f2)),
        ("**Supply ÷ demand** (2026 ≈ 0.93): median (P10–P90)", band("ratio", f2)),
        ("  Supply ÷ demand: P25–P75", iqr("ratio", f2)),
        ("**AI productivity** (work per radiologist-hour, 2026 = 1)", band("productivity", f2)),
        ("  AI productivity: P25–P75", iqr("productivity", f2)),
        ("**AI-first / autonomous share** of interpretive work", band("autonomous", fp)),
        ("  AI-first share: P25–P75", iqr("autonomous", fp)),
        ("P(demand < 2026 level)", [pct(sm[y]["p_demand_below_today"]) for y in YEARS5]),
        ("P(demand < 80% of 2026)", [pct(sm[y]["p_demand_below_80"]) for y in YEARS5]),
        ("P(demand < 50% of 2026)", [pct(sm[y]["p_demand_below_50"]) for y in YEARS5]),
        ("P(supply > demand)", [pct(sm[y]["p_supply_exceeds_demand"]) for y in YEARS5]),
        ("**P(meaningful oversupply: S/D > 1.10)**", [pct(sm[y]["p_oversupply"]) for y in YEARS5]),
        ("P(severe oversupply: S/D > 1.25)", [pct(sm[y]["p_severe_oversupply"]) for y in YEARS5]),
        ("P(shortage worse than 10%: S/D < 0.90)", [pct(sm[y]["p_shortage_10"]) for y in YEARS5]),
    ]
    for label, vals in lines:
        rows.append(f"| {label} | " + " | ".join(vals) + " |")
    return "\n".join(rows)


def jevons_md():
    ch = [c for c in jv[2035] if c.startswith("ch::")]
    rows = ["| | " + " | ".join(str(y) for y in YEARS5) + " |", "|---|" + "---|" * len(YEARS5)]
    rows.append("| Labor saved by AI productivity (mean, share of 2026 FTE) | " +
                " | ".join(num(jv[y]["labor_saved_mean"], 3) for y in YEARS5) + " |")
    for c in ch:
        rows.append(f"| ↳ induced: {c[4:]} | " + " | ".join(f"{float(jv[y][c]):+.3f}".replace("-", "−") for y in YEARS5) + " |")
    rows.append("| **Net AI-induced demand (mean)** | " + " | ".join(num(jv[y]["induced_mean"], 3) for y in YEARS5) + " |")
    rows.append("| Offset ratio, induced ÷ saved: median (P10–P90) | " + " | ".join(
        f"{num(jv[y]['offset_p50'])} ({num(jv[y]['offset_p10'])}–{num(jv[y]['offset_p90'])})" for y in YEARS5) + " |")
    rows.append("| Ratio of means | " + " | ".join(num(jv[y]["offset_mean_ratio"]) for y in YEARS5) + " |")
    rows.append("| **P(true Jevons paradox: induced > saved)** | " + " | ".join(pct(jv[y]["p_jevons"], 1) for y in YEARS5) + " |")
    return "\n".join(rows)


def regimes_md():
    rows = ["| AI regime | Weight | Timeline multiplier M | Median demand 2035 / 2045 / 2055 | AI productivity 2045 | "
            "AI-first share 2045 | P(oversupply) 2035 / 2045 / 2055 |", "|---|---|---|---|---|---|---|"]
    mdesc = {"Stall": "1.6–3.0", "Trend": "≈0.65–1.6 (median 1)", "Fast": "0.40–0.65", "Transformative": "0.25–0.45 + ceilings lifted"}
    for name in REGIME_NAMES:
        r = rg[name]
        rows.append(f"| {name} | {pct(r['weight'])} | {mdesc[name]} | {num(r['D2035_p50'])} / {num(r['D2045_p50'])} / "
                    f"{num(r['D2055_p50'])} | {num(r['P2045_p50'])}× | {pct(r['auto2045_p50'])} | "
                    f"{pct(r['pOver2035'])} / {pct(r['pOver2045'])} / {pct(r['pOver2055'])} |")
    return "\n".join(rows)


def tornado_md(focus_only=False):
    rows = ["| Assumption group (10th → 90th percentile) | Median demand 2035 | Median demand 2045 | Median demand 2055 | "
            "P(oversupply) 2035 | P(oversupply) 2045 | P(oversupply) 2055 |", "|---|---|---|---|---|---|---|"]
    for g, r in tor.items():
        if focus_only and not r["focus"]:
            continue
        star = "**" if r["focus"] else ""
        rows.append(f"| {star}{g}{star} | {num(r['D2035_p50_low'])} → {num(r['D2035_p50_high'])} | "
                    f"{num(r['D2045_p50_low'])} → {num(r['D2045_p50_high'])} | {num(r['D2055_p50_low'])} → {num(r['D2055_p50_high'])} | "
                    f"{pct(r['pOver2035_low'])} → {pct(r['pOver2035_high'])} | {pct(r['pOver2045_low'])} → {pct(r['pOver2045_high'])} | "
                    f"{pct(r['pOver2055_low'])} → {pct(r['pOver2055_high'])} |")
    b = next(iter(tor.values()))
    rows.append(f"| *All assumptions at their sampled distributions (reference)* | {num(b['D2035_p50_base'])} | {num(b['D2045_p50_base'])} | "
                f"{num(b['D2055_p50_base'])} | {pct(b['pOver2035_base'])} | {pct(b['pOver2045_base'])} | {pct(b['pOver2055_base'])} |")
    return "\n".join(rows)


def signposts_md():
    rows = ["| If we observe… | Share of simulated worlds | P(oversupply) 2035 | P(oversupply) 2045 | P(oversupply) 2055 | "
            "Median demand 2045 |", "|---|---|---|---|---|---|"]
    for r in x["signposts"]:
        rows.append(f"| {r['label']} | {pct(r['share'])} | {pct(r['p_over_2035'])} | {pct(r['p_over_2045'])} | "
                    f"{pct(r['p_over_2055'])} | {num(r['D2045_p50'])} |")
    return "\n".join(rows)


def eta_md(df=None, n=10):
    df = eta if df is None else df
    rows = ["| Rank | Parameter | Evidence | η² demand 2035 | η² demand 2045 | η² demand 2055 | η² S/D 2045 | Spearman ρ (demand 2045) |",
            "|---|---|---|---|---|---|---|---|"]
    for k, r in enumerate(df.sort_values("Demand 2045", ascending=False).head(n).to_dict("records"), 1):
        rows.append(f"| {k} | {r['label']} (`{r['param']}`) | {r['evidence']} | {num(r['Demand 2035'])} | {num(r['Demand 2045'])} | "
                    f"{num(r['Demand 2055'])} | {num(r['Supply/demand 2045'])} | {float(r['rho::Demand 2045']):+.2f} |")
    return "\n".join(rows)


def composition_md():
    labels = {"interp": "Interpretation / reporting", "draft": "Measurement & report drafting",
              "consult": "Clinical synthesis & consultation", "admin": "Administrative (protocoling, QA)",
              "proc": "Physical / procedural", "oversight": "AI oversight (new task)", "newtasks": "Other new radiologist tasks"}
    ys = ["2026", "2035", "2045", "2055", "2066"]
    rows = ["| Task | " + " | ".join(ys) + " |", "|---|" + "---|" * len(ys)]
    for k, lab in labels.items():
        rows.append(f"| {lab} | " + " | ".join(pct(x["composition"][y][k]) for y in ys) + " |")
    return "\n".join(rows)


def backtest_md():
    rows = ["| Occupation | Employment 2016 → 2025, actual | This method: median (80% interval) | BLS + trend combination, no AI layer | "
            "BLS projection (2016) | Prior trend | Inside 80% interval? | Frey & Osborne automation probability |", "|---|---|---|---|---|---|---|---|"]
    for r in bt["occupations"]:
        q = r["q"]
        rows.append(f"| {r['label']} | {num(r['actual'])} | {num(q['p50'])} ({num(q['p10'])}–{num(q['p90'])}) | {num(r['combo'])} | {num(r['bls'])} | "
                    f"{num(r['trend'])} | {'yes' if r['in80'] else 'no'} | {r['fo_prob']:.2f} |")
    rq = bt["radiology"]["ratio_q"]
    rows.append(f"| Radiologists (supply ÷ demand in 2025) | shortage (≈0.93) | {num(rq['p50'])} ({num(rq['p10'])}–{num(rq['p90'])}); "
                f"P(shortage) {pct(bt['radiology']['p_shortage'])} | — | — | — | yes | 0.0042 |")
    return "\n".join(rows)


def robust_md():
    ys = ("2035", "2045", "2055")
    rows = ["| Prior set or structure | " + " | ".join(f"P(oversupply) {y}" for y in ys) + " | P(Jevons) 2045 | Median demand 2045 |",
            "|---|" + "---|" * (len(ys) + 2)]
    for kind, d in (("Prior", rb["priors"]), ("Structure", rb["structures"])):
        for k, v in d.items():
            if kind == "Structure" and k == "base":
                continue
            rows.append(f"| {kind}: {v['label']} | " + " | ".join(pct(v[y]["p_over"]) for y in ys) +
                        f" | {pct(v['2045']['p_jevons'])} | {num(v['2045']['D_p50'])} |")
    b = rb["band"]
    rows.append("| **Range across rows** | " + " | ".join(f"**{pct(b[y]['lo'])}–{pct(b[y]['hi'])}**" for y in ys) +
                f" | **{pct(b['2045']['jev_lo'])}–{pct(b['2045']['jev_hi'])}** | |")
    return "\n".join(rows)


def pipeline_md():
    tiers = ["Tier 1 — normal/negative radiographs & screening", "Tier 2 — all radiographs, screening mammography, standardized follow-up",
             "Tier 3 — complex diagnostic CT/MR/US/NM", "Tier 4 — hardest residual work"]
    stages = ["Capable", "Validated", "FDA-authorized", "Paid & liability-accepted", "50% of eventual adoption"]
    rows = ["| Tier | " + " | ".join(stages) + " |", "|---|" + "---|" * len(stages)]
    for j, t in enumerate(tiers):
        cells = [f"{yr(x['stages_p50'][j][k])} ({yr(x['stages_p10'][j][k])}–{yr(x['stages_p90'][j][k])})" for k in range(5)]
        rows.append(f"| {t} | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def params_md():
    rows = ["| Group | Parameter | Distribution | P10 / P50 / P90 | Unit | Evidence | Sources & notes |", "|---|---|---|---|---|---|---|"]
    for p in PARAMS:
        q = p.quantiles()
        src = ", ".join(f"[@{s}]" for s in p.sources)
        corr = ", ".join(f"{k}: {v:+.1f}" for k, v in p.loadings.items())
        note = (p.note + (f" *Factor loadings: {corr}.*" if corr else "")).replace("|", "/")
        rows.append(f"| {p.group} | {p.label} (`{p.name}`) | {p.summary()} | {_fmt_num(q[0])} / {_fmt_num(q[1])} / {_fmt_num(q[2])} | {p.unit} | "
                    f"**{p.evidence}** | {src} {note} |")
    return "\n".join(rows)


n_sims = json.loads((ROOT / "docs" / "data" / "forecast.json").read_text())["n_sims"]
SECTIONS = {
    "question": ("sec-question", "§1"), "approach": ("sec-approach", "§2"), "evidence": ("sec-evidence", "§3"),
    "model": ("sec-model", "§4"), "baseline": ("sec-baseline", "§4.1"), "ai": ("sec-ai", "§4.2"),
    "pipeline": ("sec-pipeline", "§4.3"), "jevons": ("sec-jevons", "§4.4"), "supply": ("sec-supply", "§4.5"),
    "uncertainty": ("sec-uncertainty", "§4.6"), "params": ("sec-params", "§5"), "validation": ("sec-validation", "§6"),
    "results": ("sec-results", "§7"), "ds": ("sec-ds", "§7.1"), "balance": ("sec-balance", "§7.2"),
    "aiprod": ("sec-aiprod", "§7.3"), "jevres": ("sec-jevres", "§7.4"), "regimes": ("sec-regimes", "§7.5"),
    "tasks": ("sec-tasks", "§7.6"), "baseres": ("sec-baseres", "§7.7"), "sensitivity": ("sec-sensitivity", "§8"),
    "tornado": ("sec-tornado", "§8.1"), "eta": ("sec-eta", "§8.2"), "evshare": ("sec-evshare", "§8.3"),
    "careers": ("sec-careers", "§9"), "margins": ("sec-margins", "§9.2"), "signposts": ("sec-signposts", "§9.3"),
    "limits": ("sec-limits", "§10"), "repro": ("sec-repro", "§11"), "approaches": ("sec-approaches", "§2.1"),
    "backtest": ("sec-backtest", "§6.2"), "robust": ("sec-robust", "§8.4"),
}


def m(key):
    """Inline link from a claim to the section that supports it."""
    anchor, label = SECTIONS[key]
    return f'<sup>[{label}](#{anchor} "Method / evidence for this claim")</sup>'


def anchor(key):
    return f'<a name="{SECTIONS[key][0]}"></a>'


def stage_table():
    rows = ["| Where you are in fall 2026 | Typical first attending year* | P(oversupply) when you start | 10 years in | 20 years in | "
            "30 years in (or 2066) | P(demand below 2026) 10 years in | P(still a shortage) when you start |",
            "|---|---|---|---|---|---|---|---|"]
    for r in x["stages"]:
        rows.append(f"| {r['label']} | {r['start']} | {pct(r['entry_p_over'])} | {pct(r['y10_p_over'])} | "
                    f"{pct(r['y20_p_over'])} | {pct(r['y30_p_over'])} ({r['y30_year']}) | {pct(r['y10_p_below'])} | "
                    f"{pct(r['entry_p_short'])} |")
    return "\n".join(rows)


CTX = dict(m=m, anchor=anchor, stage_table=stage_table, n_params=len(PARAMS), n_sims=n_sims, sm=sm, pr=pr, jv=jv, rg=rg, tor=tor, val=val, x=x, pct=pct, num=num, chg=chg, yr=yr, ev_shrink=ev_shrink,
           ev_n=ev_n, headline_table=headline_table, jevons_md=jevons_md, regimes_md=regimes_md, tornado_md=tornado_md,
           signposts_md=signposts_md, backtest_md=backtest_md, bt=bt, robust_md=robust_md, rb=rb, eta_md=eta_md, eta_nt=eta_nt, composition_md=composition_md, pipeline_md=pipeline_md,
           params_md=params_md, float=float, round=round, abs=abs, min=min, max=max)


def fill(text: str) -> str:
    def rep(m):
        return str(eval(m.group(1), {"__builtins__": {}}, CTX))  # noqa: S307 (trusted local template)

    # iterate because tables can contain citations but not placeholders
    return re.sub(r"\{\{(.+?)\}\}", rep, text, flags=re.S)


# ----------------------------------------------------------------------------------------------------- citations
def _ranges(nums):
    nums = sorted(set(nums))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(f"{nums[i]}-{nums[j]}" if j - i >= 2 else ",".join(str(n) for n in nums[i:j + 1]))
        i = j + 1
    return ",".join(out)


def cite(text: str):
    """Replace [@a; @b] with linked AMA superscripts; record each occurrence for back-links."""
    order: list[str] = []
    occ: dict[int, int] = {}

    def link(n):
        return f"[{n}](#ref-{n})"

    def rep(mobj):
        keys = [k.strip().lstrip("@") for k in mobj.group(1).split(";")]
        nums = []
        for k in keys:
            if k not in REFERENCES:
                raise KeyError(f"unknown citation key: {k}")
            if k not in order:
                order.append(k)
            nums.append(order.index(k) + 1)
        nums = sorted(set(nums))
        anchors = ""
        for n in nums:
            occ[n] = occ.get(n, 0) + 1
            anchors += f'<a name="c{n}-{occ[n]}"></a>'
        # ranges of 3+ consecutive numbers are shown as first-last (AMA)
        parts, i = [], 0
        while i < len(nums):
            j = i
            while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
                j += 1
            if j - i >= 2:
                parts.append(f"{link(nums[i])}-{link(nums[j])}")
            else:
                parts.extend(link(n) for n in nums[i:j + 1])
            i = j + 1
        return f"{anchors}<sup>{','.join(parts)}</sup>"

    body = re.sub(r"\[(@[^\]]+)\]", rep, text)
    return body, order, occ


def ama_md(s: str) -> str:
    return s.replace("<i>", "*").replace("</i>", "*").replace("&amp;", "&")


def build():
    src = (ROOT / "report" / "REPORT.src.md").read_text()
    body = fill(src)
    body, order, occ = cite(body)
    refs = ["", '<a name="references"></a>', "", "## References", "",
            "*AMA Manual of Style, 11th edition. ↩ links return to each place a source is cited.*", ""]
    letters = "abcdefghijklmnopqrstuvwxyz"
    for n, k in enumerate(order, 1):
        back = " ".join(f"[↩{letters[i] if occ[n] > 1 else ''}](#c{n}-{i + 1})" for i in range(occ.get(n, 0)))
        refs.append(f'{n}. <a name="ref-{n}"></a>{format_ama(k, "md")} {back}')
    marker = "<!-- REFERENCES -->"
    body = body.replace(marker, "\n".join(refs)) if marker in body else body + "\n".join(refs)
    (ROOT / "REPORT.md").write_text(body)
    print(f"REPORT.md: {len(body.split())} words, {len(order)} references")
    build_html(body)


def build_html(md_text: str):
    try:
        import markdown
    except ImportError:
        print("python-markdown not installed; skipping docs/report.html")
        return
    # protect TeX from the markdown parser (underscores/asterisks), restore afterwards for KaTeX
    stash: list[str] = []

    def keep(m):
        stash.append(m.group(0))
        return f"@@MATH{len(stash) - 1}@@"

    md_text = re.sub(r"\$\$.+?\$\$", keep, md_text, flags=re.S)
    md_text = re.sub(r"(?<![\\$])\$(?!\s)([^$\n]+?)\$", keep, md_text)
    html = markdown.markdown(md_text, extensions=["tables", "fenced_code", "toc", "attr_list"])
    html = re.sub(r"@@MATH(\d+)@@", lambda m: stash[int(m.group(1))].replace("<", "&lt;").replace(">", "&gt;"), html)
    html = html.replace('src="figures/', 'src="figures/')
    html = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>',
                  lambda m: '<pre class="mermaid">' + m.group(1).replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&") + "</pre>",
                  html, flags=re.S)
    tpl = (ROOT / "report" / "report_template.html").read_text()
    (ROOT / "docs" / "report.html").write_text(tpl.replace("<!--CONTENT-->", html))
    dst = ROOT / "docs" / "figures"
    dst.mkdir(exist_ok=True)
    for f in (ROOT / "figures").glob("*.png"):
        shutil.copy2(f, dst / f.name)
    print("docs/report.html written")


def readme_block() -> str:
    """Headline numbers for README.md (between the RESULTS markers), regenerated with the report."""
    ys = YEARS5
    row = lambda label, vals: f"| {label} | " + " | ".join(vals) + " |"  # noqa: E731
    band = lambda k, f: [f"{f(sm[y][k + '_p50'])} ({f(sm[y][k + '_p10'])}–{f(sm[y][k + '_p90'])})" for y in ys]  # noqa: E731
    f2 = lambda v: num(v, 2)  # noqa: E731
    lines = ["| | " + " | ".join(map(str, ys)) + " |", "|---|" + "---|" * len(ys),
             row("FTE demand, median (P10–P90), 2026 demand = 1", band("demand", f2)),
             row("FTE supply, median, 2026 demand = 1", [f2(sm[y]["supplyd_p50"]) for y in ys]),
             row("Supply ÷ demand, median (2026 ≈ 0.93)", [f2(sm[y]["ratio_p50"]) for y in ys]),
             row("AI productivity, median", [f"{float(sm[y]['productivity_p50']):.2f}×" for y in ys]),
             row("AI-first / autonomous share, median", [pct(sm[y]["autonomous_p50"]) for y in ys]),
             row("P(demand < 2026)", [pct(sm[y]["p_demand_below_today"]) for y in ys]),
             row("P(demand < 50% of 2026)", [pct(sm[y]["p_demand_below_50"]) for y in ys]),
             row("**P(meaningful oversupply, S/D > 1.10)**", [f"**{pct(sm[y]['p_oversupply'])}**" for y in ys]),
             row("P(true Jevons paradox)", [pct(jv[y]["p_jevons"]) for y in ys])]
    m1 = x["m1"]
    para = (f"**In one paragraph:** for someone entering practice in the mid-2030s, the market is more likely than not still short "
            f"({pct(m1['p_shortage_2035'])} chance in 2035), with a {pct(sm[2035]['p_oversupply'])} chance of meaningful oversupply. "
            f"Most of that risk sits in a 12%-weighted \"transformative AI\" branch; without it the risk is "
            f"{pct(x['non_tai']['2035']['p_over'])}. Risk grows over a career ({pct(sm[2045]['p_oversupply'])} by 2045, "
            f"{pct(sm[2055]['p_oversupply'])} by 2055) as autonomous reading clears regulation and payment. A true Jevons paradox, "
            f"where AI-induced imaging outweighs the labor AI saves, is unlikely under the main assumptions (≈{pct(jv[2045]['p_jevons'])} in 2045): induced "
            f"demand offsets about {pct(jv[2045]['offset_p50'])} of the savings. A 2016→2025 backtest gave the method a "
            f"{pct(bt['radiology']['p_shortage'])} chance of today's shortage, driven by supply-versus-demand fundamentals rather than AI; for "
            f"three other automation-exposed occupations, the simple average of BLS projections and trend extrapolation (mean log "
            f"error {num(bt['mae_log']['combo'])}) beat the full method ({num(bt['mae_log']['model'])}), so the backtest is a weak "
            f"sanity check. The direction is robust, the "
            f"digits are not: under alternative priors and model structures the 2045 oversupply probability ranges from "
            f"{pct(rb['band']['2045']['lo'])} to {pct(rb['band']['2045']['hi'])}, so read the numbers as model-conditioned judgment, "
            f"not a calibrated forecast (report §8.4).")
    return "\n".join(lines) + "\n\n*Numbers from the default run (`python run_model.py`, seed 20261007), regenerated by `tools/build_docs.py`.*\n\n" + para


def update_readme():
    p = ROOT / "README.md"
    text = p.read_text()
    a, b = "<!-- RESULTS:START -->", "<!-- RESULTS:END -->"
    if a in text and b in text:
        text = text[: text.index(a) + len(a)] + "\n" + readme_block() + "\n" + text[text.index(b):]
        p.write_text(text)
        print("README.md results updated")


if __name__ == "__main__":
    build()
    update_readme()
