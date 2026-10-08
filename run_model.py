"""Run the full radiology workforce forecast: simulation, analysis, figures, tables and web data.

    python run_model.py               # 20,000 simulations (default)
    python run_model.py --n 50000     # more simulations
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from model import analysis, backtest, export_web, plots, robustness
from model.params import PARAMS, evidence_counts

ROOT = Path(__file__).parent


def _fmt_num(v: float) -> str:
    """Readable parameter values: years as integers, otherwise 3 significant digits."""
    return f"{v:.0f}" if abs(v) >= 1000 else f"{v:.3g}"


def params_markdown() -> str:
    lines = ["| Parameter | Distribution | P10 / P50 / P90 | Unit | Evidence | Sources |", "|---|---|---|---|---|---|"]
    for p in PARAMS:
        q = p.quantiles()
        lines.append(f"| `{p.name}`: {p.label} | {p.summary()} | {_fmt_num(q[0])} / {_fmt_num(q[1])} / {_fmt_num(q[2])} | {p.unit} | "
                     f"{p.evidence} | {', '.join(p.sources)} |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=20261007)
    ap.add_argument("--tornado-n", type=int, default=8000)
    args = ap.parse_args()
    t0 = time.time()

    s, o = analysis.run(args.n, args.seed)
    summary = analysis.summary_table(o)
    probs = analysis.yearly_probs(o)
    jev = analysis.jevons_table(o)
    regimes = analysis.regime_table(o)
    eta = analysis.eta2_table(s, o)
    eta_ntai = analysis.eta2_table(s, o, mask=o["regime"] != 3)
    tor = analysis.tornado(args.tornado_n)
    ev = analysis.evidence_attribution(args.tornado_n)
    val = analysis.validation(s, o)
    extra = analysis.extra_metrics(s, o)
    bt = backtest.run_backtest()
    rb = robustness.run(s, o, args.n, args.seed)

    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    summary.to_csv(out / "summary_by_year.csv", index=False, float_format="%.4f")
    probs.to_csv(out / "probabilities_by_year.csv", index=False, float_format="%.4f")
    jev.to_csv(out / "jevons_by_year.csv", index=False, float_format="%.4f")
    regimes.to_csv(out / "regimes.csv", index=False, float_format="%.4f")
    eta.to_csv(out / "sensitivity_eta2.csv", index=False, float_format="%.4f")
    eta_ntai.to_csv(out / "sensitivity_eta2_excluding_transformative.csv", index=False, float_format="%.4f")
    tor.to_csv(out / "sensitivity_tornado.csv", index=False, float_format="%.4f")
    ev.to_csv(out / "evidence_attribution.csv", index=False, float_format="%.4f")
    (out / "validation.json").write_text(json.dumps(val, indent=2, default=float))
    (out / "extra_metrics.json").write_text(json.dumps(extra, indent=2, default=float))
    (out / "backtest.json").write_text(json.dumps(bt, indent=2, default=float))
    (out / "robustness.json").write_text(json.dumps(rb, indent=2, default=float))
    (out / "parameters.md").write_text(params_markdown())
    for k in ("D", "S", "R", "P", "auto"):
        q = np.percentile(o[k], [5, 10, 25, 50, 75, 90, 95], axis=0)
        pd.DataFrame(q.T, columns=["p5", "p10", "p25", "p50", "p75", "p90", "p95"]).assign(year=range(2026, 2067)) \
          .to_csv(out / f"quantiles_{k}.csv", index=False, float_format="%.4f")

    plots.make_all(s, o, probs, tor, eta, ev, ROOT / "figures", eta_ntai=eta_ntai)
    plots.fig_backtest(bt, ROOT / "figures")
    plots.fig_robustness(rb, ROOT / "figures")
    fj = export_web.forecast_json(s, o, summary, probs, jev, regimes, tor, eta, ev, val)
    fj["eta2_excluding_transformative"] = [
        {k: (export_web._r(r[k]) if k not in ("param", "label", "short", "evidence") else r[k])
         for k in ("param", "label", "short", "evidence", "Demand 2045", "Supply/demand 2045")}
        for r in eta_ntai.sort_values("Demand 2045", ascending=False).head(15).to_dict("records")]
    fj["evidence_counts"] = evidence_counts()
    fj["extra"] = json.loads(json.dumps(extra, default=float))
    fj["backtest"] = json.loads(json.dumps(bt, default=float))
    fj["robust"] = json.loads(json.dumps(rb, default=lambda v: v.tolist() if hasattr(v, "tolist") else float(v)))
    export_web.write(ROOT / "docs" / "data", fj, export_web.samples_json(s, o))
    print(f"done in {time.time() - t0:.1f}s  ->  outputs/, figures/, docs/data/")
    with pd.option_context("display.width", 200, "display.max_columns", 50):
        print(summary.round(3).T)


if __name__ == "__main__":
    main()
