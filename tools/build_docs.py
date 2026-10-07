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
from model.references import REFERENCES  # noqa: E402

OUT = ROOT / "outputs"


# ----------------------------------------------------------------------------------------------------- context
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
        ("**FTE demand** (2026 = 1): median (P10–P90)", band("demand", f2)),
        ("  FTE demand: P25–P75", iqr("demand", f2)),
        ("**FTE supply** (2026 = 1): median (P10–P90)", band("supply", f2)),
        ("  FTE supply: P25–P75", iqr("supply", f2)),
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
        rows.append(f"| {p.group} | {p.label} (`{p.name}`) | {p.summary()} | {q[0]:.3g} / {q[1]:.3g} / {q[2]:.3g} | {p.unit} | "
                    f"**{p.evidence}** | {src} {note} |")
    return "\n".join(rows)


n_sims = json.loads((ROOT / "docs" / "data" / "forecast.json").read_text())["n_sims"]
CTX = dict(n_params=len(PARAMS), n_sims=n_sims, sm=sm, pr=pr, jv=jv, rg=rg, tor=tor, val=val, x=x, pct=pct, num=num, chg=chg, yr=yr, ev_shrink=ev_shrink,
           ev_n=ev_n, headline_table=headline_table, jevons_md=jevons_md, regimes_md=regimes_md, tornado_md=tornado_md,
           signposts_md=signposts_md, eta_md=eta_md, eta_nt=eta_nt, composition_md=composition_md, pipeline_md=pipeline_md,
           params_md=params_md, float=float, round=round, abs=abs)


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
    order: list[str] = []

    def rep(m):
        keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
        nums = []
        for k in keys:
            if k not in REFERENCES:
                raise KeyError(f"unknown citation key: {k}")
            if k not in order:
                order.append(k)
            nums.append(order.index(k) + 1)
        return f"<sup>{_ranges(nums)}</sup>"

    body = re.sub(r"\[(@[^\]]+)\]", rep, text)
    return body, order


def ama_md(s: str) -> str:
    return s.replace("<i>", "*").replace("</i>", "*").replace("&amp;", "&")


def build():
    src = (ROOT / "report" / "REPORT.src.md").read_text()
    body = fill(src)
    body, order = cite(body)
    refs = ["", "## References", ""]
    for n, k in enumerate(order, 1):
        r = REFERENCES[k]
        link = f" [Link]({r['url']})" if r.get("url") and "doi.org" not in r["ama"] and r["url"] not in r["ama"] else ""
        refs.append(f"{n}. {ama_md(r['ama'])}{link}")
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


if __name__ == "__main__":
    build()
