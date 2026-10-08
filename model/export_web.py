"""Export model results as compact JSON for the website (docs/data)."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .analysis import OVERSUPPLY, SEVERE, yi
from .params import PARAMS, REGIME_NAMES, SHORT, TASK_LABELS, TASK_MEANS, TASKS
from .references import REFERENCES, format_ama, href
from .stages import STAGES
from .simulate import REPORT_YEARS, YEARS

QSET = (5, 10, 25, 50, 75, 90, 95)


def _r(x, d=4):
    if isinstance(x, (list, tuple, np.ndarray)):
        return [_r(v, d) for v in np.asarray(x).tolist()]
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return None
    return round(float(x), d)


def _quants(arr):
    return {f"p{q}": _r(np.nanpercentile(arr, q, axis=0)) for q in QSET}


def forecast_json(s, o, summary, probs, jev, regimes, tor, eta, ev, val) -> dict:
    out = {"years": YEARS.tolist(), "report_years": list(REPORT_YEARS), "n_sims": int(len(o["D"])),
           "oversupply_threshold": OVERSUPPLY, "severe_threshold": SEVERE}
    out["series"] = {k: _quants(o[k]) for k in ("D", "S", "R", "P", "auto", "B", "W")}
    out["series"]["time_saved"] = _quants(1 - 1 / o["P"])
    out["probs"] = {c: _r(probs[c].values) for c in probs.columns if c != "year"}
    out["summary"] = [{k: (_r(v) if not isinstance(v, (int, np.integer)) else int(v)) for k, v in row.items()}
                      for row in summary.to_dict("records")]
    out["jevons"] = {
        "labor_saved_mean": _r(o["L"].mean(0)), "induced_mean": _r(o["I"].mean(0)),
        "offset_p50": _r(np.nanmedian(o["offset"], 0)), "offset_p10": _r(np.nanpercentile(o["offset"], 10, 0)),
        "offset_p90": _r(np.nanpercentile(o["offset"], 90, 0)), "p_jevons": _r(o["jevons"].mean(0)),
        "channels": {k: _r(v.mean(0)) for k, v in o["channels"].items()},
        "table": [{k: _r(v) for k, v in row.items()} for row in jev.to_dict("records")],
    }
    out["composition"] = {k: _r(v.mean(0)) for k, v in o["composition"].items()}
    out["composition_labels"] = {**TASK_LABELS, "newtasks": "New radiologist tasks"}
    out["regimes"] = {
        "names": list(REGIME_NAMES),
        "weights": [_r((o["regime"] == r).mean()) for r in range(4)],
        "D_p50": [_r(np.median(o["D"][o["regime"] == r], 0)) for r in range(4)],
        "R_p50": [_r(np.median(o["R"][o["regime"] == r], 0)) for r in range(4)],
        "P_p50": [_r(np.median(o["P"][o["regime"] == r], 0)) for r in range(4)],
        "auto_p50": [_r(np.median(o["auto"][o["regime"] == r], 0)) for r in range(4)],
        "table": [{k: (_r(v) if not isinstance(v, str) else v) for k, v in row.items()} for row in regimes.to_dict("records")],
    }
    out["tornado"] = [{k: (_r(v) if isinstance(v, (float, np.floating)) else (bool(v) if isinstance(v, (bool, np.bool_)) else v))
                       for k, v in row.items()} for row in tor.to_dict("records")]
    cols = ["param", "label", "short", "evidence", "Demand 2035", "Demand 2045", "Demand 2055", "Supply/demand 2035",
            "Supply/demand 2045", "Supply/demand 2055", "rho::Demand 2045"]
    out["eta2"] = [{k: (_r(row[k]) if k not in ("param", "label", "short", "evidence") else row[k]) for k in cols}
                   for row in eta.head(25).to_dict("records")]
    out["evidence_attribution"] = [{k: (_r(v) if not isinstance(v, str) else v) for k, v in row.items()}
                                   for row in ev.to_dict("records")]
    out["validation"] = {k: (_r(v) if isinstance(v, (float, np.floating)) else (_r(v) if isinstance(v, list) else v))
                         for k, v in val.items()}
    st = o["stages"]
    out["pipeline"] = {
        "stages": ["Technically capable", "Clinically validated", "FDA authorized", "Paid & liability-accepted",
                   "50% of eventual adoption"],
        "tiers": ["Normal screens & simple radiographs", "All radiographs & screening", "Complex CT / MR",
                  "Hardest residual work"],
        "p10": _r(np.percentile(st, 10, axis=0), 1), "p50": _r(np.percentile(st, 50, axis=0), 1),
        "p90": _r(np.percentile(st, 90, axis=0), 1),
    }
    out["params"] = []
    for p in PARAMS:
        q10, q50, q90 = p.quantiles()
        out["params"].append({"name": p.name, "short": SHORT.get(p.name, p.name), "group": p.group, "label": p.label, "dist": p.summary(), "unit": p.unit,
                              "evidence": p.evidence, "sources": p.sources, "note": p.note,
                              "loadings": p.loadings, "q10": _r(q10, 3), "q50": _r(q50, 3), "q90": _r(q90, 3)})
    out["task_means"] = dict(zip(TASKS, _r(TASK_MEANS)))
    out["references"] = {k: {"html": format_ama(k, "html"), "href": href(k)} for k in REFERENCES}
    out["stages"] = [{"key": k, "label": lab, "start": st} for k, lab, st in STAGES]
    return out


def samples_json(s, o, n_keep: int = 1500, seed: int = 3) -> dict:
    """Subsample of joint draws for the in-browser conditional explorer (values x1000 as ints)."""
    rng = np.random.default_rng(seed)
    idx = np.sort(rng.choice(len(o["D"]), size=n_keep, replace=False))
    enc = lambda a: np.rint(np.asarray(a)[idx] * 1000).astype(int).tolist()  # noqa: E731
    reg_lag = (s["lval"] * 1.2 + s["lfda"] * 1.0 + s["lpay"] * 1.0)  # tier-2 total regulatory lag (years)
    inputs = {
        "regime": o["regime"][idx].astype(int).tolist(),
        "M": enc(s["ai_u"]),
        "reg_lag": enc(reg_lag),
        "util_g0": enc(s["util_g0"]),
        "util_ginf": enc(s["util_ginf"]),
        "new_max": enc(s["new_max"]),
        "thru_H": enc(s["thru_H"]),
        "resid_gamma": enc(s["resid_gamma"]),
        "slot_g": enc(s["slot_g"]),
        "ratio0": enc(s["ratio0"]),
        "ready2": enc(o["ready"][:, 1]),
        "ready3": enc(o["ready"][:, 2]),
    }
    outputs = {k: [enc(o[k][:, j]) for j in range(len(YEARS))] for k in ("D", "S", "R", "P", "auto")}
    return {"years": YEARS.tolist(), "n": n_keep, "inputs": inputs, "outputs": outputs}


def write(out_dir: Path, forecast: dict, samples: dict):
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "forecast.json").write_text(json.dumps(forecast, separators=(",", ":"), ensure_ascii=False))
    (out_dir / "samples.json").write_text(json.dumps(samples, separators=(",", ":")))
