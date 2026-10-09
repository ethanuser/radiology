"""Summaries, Jevons accounting and sensitivity analysis."""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from scipy import stats

from .params import PARAM_INDEX, PARAMS, REGIME_NAMES, SHORT, TASKS
from .stages import STAGES
from .sampling import sample
from .simulate import REPORT_YEARS, YEARS, consistent_with_today, simulate, subset

warnings.filterwarnings("ignore", message="All-NaN slice")
QS = (10, 25, 50, 75, 90)
OVERSUPPLY = 1.10  # "meaningful oversupply": >=10% more radiologist FTE than needed
SEVERE = 1.25


def yi(year: int) -> int:
    return int(year - YEARS[0])


def run(n: int = 20000, seed: int = 20261007, overrides: dict | None = None, condition: bool = True):
    """Sample and simulate n futures, then drop those already contradicted by events (see consistent_with_today)."""
    s = sample(n, seed=seed, overrides=overrides)
    o = simulate(s)
    if not condition:
        return s, o
    keep = consistent_with_today(o)
    o = subset(o, keep)
    o["n_drawn"] = n
    return subset(s, keep), o


# ------------------------------------------------------------------------------------------------ headline table
def summary_table(o: dict, years=REPORT_YEARS) -> pd.DataFrame:
    rows = []
    for y in years:
        i = yi(y)
        D, S, R, P, A = o["D"][:, i], o["S"][:, i], o["R"][:, i], o["P"][:, i], o["auto"][:, i]
        Sd = o["Sd"][:, i]  # supply in units of 2026 demand (same scale as demand)
        row = {"year": y}
        for name, arr in (("demand", D), ("supply", S), ("supplyd", Sd), ("ratio", R), ("productivity", P), ("autonomous", A)):
            for q, v in zip(QS, np.percentile(arr, QS)):
                row[f"{name}_p{q}"] = v
        row["p_demand_below_today"] = (D < 1.0).mean()
        row["p_demand_below_80"] = (D < 0.8).mean()
        row["p_demand_below_50"] = (D < 0.5).mean()
        row["p_supply_exceeds_demand"] = (R > 1.0).mean()
        row["p_oversupply"] = (R > OVERSUPPLY).mean()
        row["p_severe_oversupply"] = (R > SEVERE).mean()
        row["p_shortage_10"] = (R < 0.9).mean()
        row["time_saved_p50"] = np.median(1 - 1 / P)
        rows.append(row)
    return pd.DataFrame(rows)


def yearly_quantiles(o: dict, key: str, qs=(5, 10, 25, 50, 75, 90, 95)) -> dict:
    arr = o[key]
    return {f"p{q}": np.percentile(arr, q, axis=0) for q in qs}


def yearly_probs(o: dict) -> pd.DataFrame:
    D, R = o["D"], o["R"]
    return pd.DataFrame({
        "year": YEARS,
        "p_demand_below_today": (D < 1).mean(0),
        "p_demand_below_80": (D < 0.8).mean(0),
        "p_demand_below_50": (D < 0.5).mean(0),
        "p_supply_exceeds_demand": (R > 1).mean(0),
        "p_oversupply": (R > OVERSUPPLY).mean(0),
        "p_severe_oversupply": (R > SEVERE).mean(0),
        "p_shortage_10": (R < 0.9).mean(0),
        "p_jevons": o["jevons"].mean(0),
    })


# ------------------------------------------------------------------------------------------------ Jevons accounting
def jevons_table(o: dict, years=REPORT_YEARS) -> pd.DataFrame:
    rows = []
    for y in years:
        i = yi(y)
        L, I, off = o["L"][:, i], o["I"][:, i], o["offset"][:, i]
        row = {"year": y, "labor_saved_p50": np.median(L), "induced_p50": np.median(I),
               "labor_saved_mean": L.mean(), "induced_mean": I.mean(),
               "offset_mean_ratio": I.mean() / L.mean(), "p_jevons": o["jevons"][:, i].mean()}
        for q, v in zip(QS, np.nanpercentile(off, QS)):
            row[f"offset_p{q}"] = v
        for k, v in o["channels"].items():
            row[f"ch::{k}"] = v[:, i].mean()
        rows.append(row)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------ regime breakdown
def regime_table(o: dict, years=(2035, 2045, 2055, 2066)) -> pd.DataFrame:
    rows = []
    for r, name in enumerate(REGIME_NAMES):
        m = o["regime"] == r
        row = {"regime": name, "weight": m.mean()}
        for y in years:
            i = yi(y)
            row[f"D{y}_p50"] = np.median(o["D"][m, i])
            row[f"P{y}_p50"] = np.median(o["P"][m, i])
            row[f"auto{y}_p50"] = np.median(o["auto"][m, i])
            row[f"pOver{y}"] = (o["R"][m, i] > OVERSUPPLY).mean()
            row[f"pBelow{y}"] = (o["D"][m, i] < 1).mean()
        rows.append(row)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------ sensitivity
def input_matrix(s: dict) -> pd.DataFrame:
    cols = {p.name: s[p.name] for p in PARAMS}
    cols["ai_u"] = s["ai_u"]  # timeline multiplier M
    for t in TASKS:
        cols[f"s_{t}"] = s[f"s_{t}"]
    return pd.DataFrame(cols)


def correlation_ratio(x: np.ndarray, y: np.ndarray, bins: int = 20) -> float:
    """First-order sensitivity eta^2 = Var(E[Y|X]) / Var(Y), estimated by quantile binning of X.
    Valid with correlated inputs (it then includes effects carried through correlated parameters)."""
    ok = np.isfinite(y)
    x, y = x[ok], y[ok]
    edges = np.unique(np.quantile(x, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:
        return 0.0
    idx = np.clip(np.searchsorted(edges, x, side="right") - 1, 0, len(edges) - 2)
    means = np.bincount(idx, weights=y) / np.maximum(np.bincount(idx), 1)
    counts = np.bincount(idx)
    var_cond = np.sum(counts * (means - y.mean()) ** 2) / len(y)
    eta = var_cond / y.var()
    # subtract the expected value under independence (bias of the binning estimator)
    return max(0.0, eta - (len(edges) - 2) / len(y))


SENS_OUTPUTS = {
    "Demand 2035": lambda o: np.log(o["D"][:, yi(2035)]),
    "Demand 2045": lambda o: np.log(o["D"][:, yi(2045)]),
    "Demand 2055": lambda o: np.log(o["D"][:, yi(2055)]),
    "Supply/demand 2035": lambda o: np.log(o["R"][:, yi(2035)]),
    "Supply/demand 2045": lambda o: np.log(o["R"][:, yi(2045)]),
    "Supply/demand 2055": lambda o: np.log(o["R"][:, yi(2055)]),
}


def eta2_table(s: dict, o: dict, mask: np.ndarray | None = None) -> pd.DataFrame:
    X = input_matrix(s)
    m = np.ones(len(X), bool) if mask is None else mask
    rows = []
    for name in X.columns:
        row = {"param": name}
        for out_name, f in SENS_OUTPUTS.items():
            y = f(o)[m]
            x = X[name].values[m]
            row[out_name] = correlation_ratio(x, y)
            row[f"rho::{out_name}"] = stats.spearmanr(x, y, nan_policy="omit").statistic
        rows.append(row)
    df = pd.DataFrame(rows)
    df["label"] = [PARAM_INDEX[p].label if p in PARAM_INDEX else f"Task share: {p[2:]}" for p in df["param"]]
    df["evidence"] = [PARAM_INDEX[p].evidence if p in PARAM_INDEX else "A" for p in df["param"]]
    df["label"] = np.where(df["param"] == "ai_u", "AI progress speed (timeline multiplier M, incl. regime)", df["label"])
    df["short"] = [SHORT.get(p, p) for p in df["param"]]
    return df.sort_values("Demand 2045", ascending=False).reset_index(drop=True)


# Named assumption groups for the tornado; value = list of (param, direction) where direction +1 means
# "high scenario = high quantile", -1 means "high scenario = low quantile".
GROUPS = {
    "AI capability speed": [("ai_u", +1)],
    "Future imaging utilization": [("util_g0", +1), ("util_ginf", +1), ("cmplx_g0", +1)],
    "AI-first / autonomous adoption": [("amax1", +1), ("amax2", +1), ("amax3", +1), ("amax4", +1), ("f_sub", +1),
                                       ("ahalf", -1)],
    "Regulatory delay": [("lval", +1), ("lfda", +1), ("lpay", +1)],
    "New imaging applications": [("new_max", +1), ("lambda_new", +1), ("new_T0", -1)],
    "Scanner throughput & capacity": [("thru_H", +1), ("latent", +1), ("cap_invest", +1), ("thru_T0", -1)],
    "Residency adjustment": [("resid_gamma", +1), ("fill_kappa", +1), ("resid_lag", -1)],
    "Assistive-AI time savings": [("m_interp", +1), ("m_draft", +1), ("m_consult", +1), ("m_admin", +1),
                                  ("adopt_mid", -1)],
    "Residency slot growth": [("slot_g", +1)],
    "Demographics": [("dem_rate", +1), ("dem_late", +1)],
    "Price elasticity & pass-through": [("elasticity", -1), ("pass_through", +1), ("pc_share", +1), ("access", +1)],
    "Attrition": [("attr_mult", +1)],
    "Today's shortage (2026 S/D)": [("ratio0", +1)],
    "Shortage-driven AI adoption": [("adopt_pressure", +1)],
}
FOCUS_GROUPS = ["Future imaging utilization", "AI-first / autonomous adoption", "Regulatory delay",
                "New imaging applications", "Scanner throughput & capacity", "Residency adjustment"]


def tornado(n: int = 8000, seed: int = 7, lo_q: float = 0.1, hi_q: float = 0.9) -> pd.DataFrame:
    _, base = run(n, seed)
    metrics = {
        "D2035_p50": lambda o: np.median(o["D"][:, yi(2035)]),
        "D2045_p50": lambda o: np.median(o["D"][:, yi(2045)]),
        "D2055_p50": lambda o: np.median(o["D"][:, yi(2055)]),
        "pOver2035": lambda o: (o["R"][:, yi(2035)] > OVERSUPPLY).mean(),
        "pOver2045": lambda o: (o["R"][:, yi(2045)] > OVERSUPPLY).mean(),
        "pOver2055": lambda o: (o["R"][:, yi(2055)] > OVERSUPPLY).mean(),
        "R2045_p50": lambda o: np.median(o["R"][:, yi(2045)]),
    }
    base_vals = {k: f(base) for k, f in metrics.items()}
    rows = []
    for g, members in GROUPS.items():
        res = {}
        for tag, q in (("low", lo_q), ("high", hi_q)):
            ov = {p: (q if d > 0 else 1 - q) for p, d in members}
            _, o = run(n, seed, ov)
            res[tag] = {k: f(o) for k, f in metrics.items()}
        row = {"group": g, "focus": g in FOCUS_GROUPS, "members": ", ".join(p for p, _ in members)}
        for k in metrics:
            row[f"{k}_base"] = base_vals[k]
            row[f"{k}_low"] = res["low"][k]
            row[f"{k}_high"] = res["high"][k]
            row[f"{k}_swing"] = abs(res["high"][k] - res["low"][k])
        rows.append(row)
    return pd.DataFrame(rows).sort_values("D2045_p50_swing", ascending=False).reset_index(drop=True)


def evidence_attribution(n: int = 8000, seed: int = 11) -> pd.DataFrame:
    """How much would the 80% interval shrink if each evidence class were known exactly (pinned at its median)?"""
    _, base = run(n, seed)

    def width(o, key, y):
        a = o[key][:, yi(y)]
        return np.percentile(a, 90) - np.percentile(a, 10)

    rows = []
    for grade, label in (("E", "Empirical"), ("A", "Anchored"), ("S", "Subjective")):
        names = [p.name for p in PARAMS if p.evidence == grade]
        _, o = run(n, seed, {nm: 0.5 for nm in names})
        for y in (2035, 2045, 2055):
            for key in ("D", "R"):
                rows.append({"grade": label, "n_params": len(names), "year": y, "metric": key,
                             "width_base": width(base, key, y), "width_pinned": width(o, key, y),
                             "shrink": 1 - width(o, key, y) / width(base, key, y)})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------ validation
def validation(s: dict, o: dict) -> dict:
    from .simulate import COHORT_2023, HAZARD, KAPPA, STOCK_2023, FILLED_HIST
    # (1) supply: flat positions reproduce Christensen (+25.7% 2023-2055) by construction; growth scenario check
    c = COHORT_2023.copy()
    surv_years = []
    for year in range(2024, 2056):
        c = np.r_[KAPPA * FILLED_HIST[2024], (c - c * HAZARD)[:-1]]
        surv_years.append(c.sum())
    flat_2055 = c.sum() / STOCK_2023
    sflat = dict(zip(range(2024, 2056), surv_years))
    # independent check: Neiman 2026 update projects +20.9% by 2055 if post-COVID attrition persists (flat positions)
    c_hi = COHORT_2023.copy()
    hz_hi = np.clip(HAZARD * 1.2, 0, 1)
    for year in range(2024, 2056):
        c_hi = np.r_[KAPPA * FILLED_HIST[2024], (c_hi - c_hi * hz_hi)[:-1]]
    flat_2055_high_attr = c_hi.sum() / STOCK_2023
    c_hi2, sflat_hi = COHORT_2023.copy(), {}
    for year in range(2024, 2056):
        c_hi2 = np.r_[KAPPA * FILLED_HIST[2024], (c_hi2 - c_hi2 * hz_hi)[:-1]]
        sflat_hi[year] = c_hi2.sum()
    mean_career = np.cumprod(np.r_[1.0, 1 - HAZARD[:-1]]).sum()
    attr_2023 = (COHORT_2023 * HAZARD).sum() / COHORT_2023.sum()
    # (2) demographics-only growth 2026-2055 vs Christensen 2023-2055 range (+16.9% to +26.9%)
    dem = o["B_dem"][:, yi(2055)]
    # (3) Langlotz comparison: technical potential vs realized time saved around 2031
    i31 = yi(2031)
    pot = (s["s_interp"] * s["m_interp"] * o["cap_interp"][:, i31] + s["s_draft"] * s["m_draft"] * o["cap_draft"][:, i31])
    return {
        "supply_flat_2055_vs_2023": flat_2055,
        "christensen_flat_2055": 1.257,
        "supply_flat_2055_high_attrition": flat_2055_high_attr,
        # like-for-like with Neiman's "if no action is taken": no further AI, flat residency positions, no market response
        "neiman_matched_ratio_p50": {str(y): float(np.median(np.asarray(s["ratio0"]) * sflat_hi[y] / sflat_hi[2026] / o["B_dem"][:, yi(y)]))
                                     for y in (2035, 2045, 2055)},
        "noai_flat_ratio_p50": {str(y): float(np.median(np.asarray(s["ratio0"]) * sflat[y] / sflat[2026] / o["B"][:, yi(y)]))
                                for y in (2035, 2045, 2055)},
        "mean_career_years": mean_career,
        "christensen_career_years": "34.2-35.7",
        "attrition_2023": attr_2023,
        "kappa_entrants_per_filled_position": KAPPA,
        "demographic_growth_2026_2055_p50": float(np.median(dem) - 1),
        "dem_util_growth_2026_2055": [float(np.percentile(o["B_dem"][:, yi(2055)] * o["B_util"][:, yi(2055)], q) - 1) for q in (10, 50, 90)],
        "demographic_growth_2026_2055_p10_p90": [float(np.percentile(dem, 10) - 1), float(np.percentile(dem, 90) - 1)],
        "realized_time_saved_2031_p50": float(np.median(1 - 1 / o["P"][:, i31])),
        "realized_time_saved_2031_p90": float(np.percentile(1 - 1 / o["P"][:, i31], 90)),
        "assistive_potential_interp_draft_2031_p50": float(np.median(pot)),
        "langlotz_5yr_hours_reduction": "33% (range 14%-49%)",
        "baseline_no_ai_2055_p50": float(np.median(o["B"][:, yi(2055)]) - 1),
    }


# ------------------------------------------------------------------------------------------------ extra metrics
def extra_metrics(s: dict, o: dict) -> dict:
    """Derived numbers quoted in the report and on the website (so prose always matches the model)."""
    D, R, P, A = o["D"], o["R"], o["P"], o["auto"]
    over = R > OVERSUPPLY
    x: dict = {}
    x["m1"] = {
        "p_ratio_gt1_2035": (R[:, yi(2035)] > 1).mean(),
        "p_over_2035": over[:, yi(2035)].mean(),
        "p_over_2036": over[:, yi(2036)].mean(),
        "p_shortage10_2035": (R[:, yi(2035)] < 0.9).mean(),
        "p_shortage_2035": (R[:, yi(2035)] < 1).mean(),
        "p_any_over_2035_2040": over[:, yi(2035):yi(2041)].any(1).mean(),
        "p_any_over_2035_2066": over[:, yi(2035):].any(1).mean(),
        "p_D2045_below_D2035": (D[:, yi(2045)] < D[:, yi(2035)]).mean(),
        "p_D2066_below_D2035": (D[:, yi(2066)] < D[:, yi(2035)]).mean(),
    }
    m = o["regime"] != 3
    x["non_tai"] = {"weight": m.mean()}
    for y in (2035, 2045, 2055, 2066):
        i = yi(y)
        x["non_tai"][str(y)] = {
            "D_p10": np.percentile(D[m, i], 10), "D_p50": np.median(D[m, i]), "D_p90": np.percentile(D[m, i], 90),
            "p_over": over[m, i].mean(), "p_below": (D[m, i] < 1).mean(), "p_below80": (D[m, i] < 0.8).mean(),
            "p_below50": (D[m, i] < 0.5).mean(), "p_jevons": o["jevons"][m, i].mean(),
            "R_p50": np.median(R[m, i]),
        }
    q_u = np.quantile(s["util_g0"], [1 / 3, 2 / 3])
    q_n = np.quantile(s["new_max"], [1 / 3, 2 / 3])
    signposts = [
        ("All simulated futures", np.ones(len(D), bool)),
        ("AI saves >15% of radiologist time by 2031", P[:, yi(2031)] > 1 / (1 - 0.15)),
        ("AI saves <5% of radiologist time by 2031", P[:, yi(2031)] < 1 / (1 - 0.05)),
        ("AI-first reading exceeds 5% of interpretive work by 2033", A[:, yi(2033)] > 0.05),
        ("AI-first reads paid for through tier 2 (all radiographs & screening) before 2035", o["ready"][:, 1] < 2035),
        ("AI-first reads not paid for through tier 2 until after 2045", o["ready"][:, 1] > 2045),
        (f"Per-person imaging growth in the top third (≥{q_u[1]:.1f}%/yr in 2026)", s["util_g0"] > q_u[1]),
        (f"Per-person imaging growth in the bottom third (≤{q_u[0]:.1f}%/yr in 2026)", s["util_g0"] < q_u[0]),
        ("Many new AI-enabled imaging uses (top third)†", s["new_max"] > q_n[1]),
        ("Few new AI-enabled imaging uses (bottom third)†", s["new_max"] < q_n[0]),
        ("Transformative-AI regime", o["regime"] == 3),
        ("Any regime except transformative AI", o["regime"] != 3),
    ]
    x["signposts"] = []
    for label, mk in signposts:
        x["signposts"].append({
            "label": label, "share": mk.mean(), "n": int(mk.sum()),
            "p_over_2035": over[mk, yi(2035)].mean(), "p_over_2045": over[mk, yi(2045)].mean(),
            "p_over_2055": over[mk, yi(2055)].mean(), "D2045_p50": np.median(D[mk, yi(2045)]),
            "p_below_2045": (D[mk, yi(2045)] < 1).mean(),
        })
    # Displacement pressure: demand falling faster than natural attrition (~2.7%/yr) over any 5-year window
    # means incumbents (not just new graduates) would face involuntary job loss or forced part-time work.
    attr = 0.025  # measured attrition in 2022 (Rula 2026); the model's own exit rate is a little higher
    win = 5
    dec = 1 - (D[:, win:] / D[:, :-win]) ** (1 / win)  # annualized 5-year decline rate starting each year
    start = YEARS[:-win]
    career = start >= 2035
    x["displacement"] = {
        "attrition_rate": attr,
        "p_any_decline_faster_than_attrition_2035_2066": (dec[:, career] > attr).any(1).mean(),
        "p_any_decline_faster_than_attrition_non_tai": (dec[o["regime"] != 3][:, career] > attr).any(1).mean(),
        "p_any_decline_2x_attrition_2035_2066": (dec[:, career] > 2 * attr).any(1).mean(),
    }
    # Sustained severe surplus: supply ÷ demand above 1.25 for 5+ consecutive years after 2035. New graduates keep
    # entering, so a surplus can persist even when demand falls slower than attrition; who bears it is not modeled.
    sev = o["R"][:, YEARS >= 2035] > 1.25
    run_len = np.zeros(sev.shape[0], int)
    best = np.zeros(sev.shape[0], int)
    for j in range(sev.shape[1]):
        run_len = np.where(sev[:, j], run_len + 1, 0)
        best = np.maximum(best, run_len)
    x["displacement"]["p_sustained_severe_surplus"] = (best >= 5).mean()
    x["displacement"]["p_sustained_severe_surplus_non_tai"] = (best[o["regime"] != 3] >= 5).mean()
    stage_rows = []
    for key, label, start in STAGES:
        row = {"key": key, "label": label, "start": start}
        for k, off in (("entry", 0), ("y10", 10), ("y20", 20), ("y30", 30)):
            yr = min(start + off, 2066)
            row[f"{k}_year"] = yr
            row[f"{k}_p_over"] = over[:, yi(yr)].mean()
            row[f"{k}_p_short10"] = (o["R"][:, yi(yr)] < 0.9).mean()
            row[f"{k}_p_short"] = (R[:, yi(yr)] < 1).mean()
            row[f"{k}_p_below"] = (D[:, yi(yr)] < 1).mean()
            row[f"{k}_D_p50"] = np.median(D[:, yi(yr)])
        row["p_any_over_career"] = over[:, yi(start):].any(1).mean()
        stage_rows.append(row)
    x["stages"] = stage_rows
    x["supply"] = {
        "head_2026_p50": np.median(o["head"][:, 0]), "head_2035_p50": np.median(o["head"][:, yi(2035)]),
        "positions_2035_p50": np.median(o["positions"][:, yi(2035)]),
        "positions_2045_p50": np.median(o["positions"][:, yi(2045)]),
        "positions_2045_p10": np.percentile(o["positions"][:, yi(2045)], 10),
        "positions_2055_p10": np.percentile(o["positions"][:, yi(2055)], 10),
    }
    # What a surplus would mean in practice (illustrative arithmetic, not a labor-market model): a 15% surplus could be
    # absorbed entirely by shorter hours, or by cutting new-graduate entry, at the model's 2035 entry rate.
    entry_rate = np.median(o["entrants"][:, yi(2035)] / o["head"][:, yi(2035)])
    cut = 1 - 1 / 1.15  # share of supply that must go to remove a 15% surplus
    x["surplus_arith"] = {"surplus": 0.15, "hours_cut": cut, "entry_rate_2035": float(entry_rate),
                          "years_half_entry": float(cut / (entry_rate / 2))}
    # Prospective tracking: near-term, checkable predictions archived with each release
    st = o["stages"]  # (n, tier, [capable, validated, FDA, paid, 50% adoption])
    pos30 = o["positions"][:, yi(2030)]
    # Condition on what is already known in October 2026: no FDA-authorized autonomous radiology read yet
    known = st[:, 0, 2] >= 2026.8
    stk, posk = st[known], o["positions"][known]
    pos30 = posk[:, yi(2030)]
    x["predictions"] = [
        {"id": "fda_tier1_2029", "check": "By 31 Dec 2029",
         "event": "FDA authorizes a device that finalizes some normal chest radiographs without radiologist review",
         "resolution": "FDA device database (510(k)/De Novo/PMA) decision summary states autonomous reporting without radiologist review",
         "p": float((stk[:, 0, 2] < 2030).mean())},
        {"id": "paid_tier1_2032", "check": "By 31 Dec 2032",
         "event": "Medicare pays separately for such autonomous reads",
         "resolution": "A national Medicare payment rate (physician fee schedule or OPPS) for autonomous AI interpretation, not contractor pricing",
         "p": float((stk[:, 0, 3] < 2033).mean())},
        {"id": "positions_2030", "check": "2030 Match",
         "event": "Diagnostic-radiology first-year residency positions offered (2026: 1,241)",
         "resolution": "NRMP Main Residency Match results: diagnostic radiology positions offered, the same series that reported 1,241 in 2026",
         "p50": float(np.median(pos30)), "p10": float(np.percentile(pos30, 10)), "p90": float(np.percentile(pos30, 90)),
         "q": {str(q): float(np.percentile(pos30, q)) for q in (5, 25, 50, 75, 95)}},
    ]
    x["predictions_meta"] = {"conditioned_on": "no FDA-authorized autonomous radiology read before October 2026",
                             "share_of_draws_kept": float(len(o["R"]) / o.get("n_drawn", len(o["R"]))),
                             "scoring": "Brier score for yes/no events; for positions, whether the outcome falls in the 80% interval and its percentile rank"}
    x["baseline"] = {str(y): {f"p{q}": np.percentile(o["B"][:, yi(y)], q) for q in (10, 50, 90)}
                     for y in (2030, 2035, 2045, 2055, 2066)}
    x["time_saved"] = {str(y): {f"p{q}": np.percentile(1 - 1 / P[:, yi(y)], q) for q in (10, 50, 90)}
                       for y in (2030, 2031, 2035, 2045, 2055, 2066)}
    x["composition"] = {str(y): {k: float(v[:, yi(y)].mean()) for k, v in o["composition"].items()}
                        for y in (2026, 2035, 2045, 2055, 2066)}
    st = o["stages"]
    x["stages_p50"] = np.percentile(st, 50, axis=0).tolist()
    x["stages_p10"] = np.percentile(st, 10, axis=0).tolist()
    x["stages_p90"] = np.percentile(st, 90, axis=0).tolist()
    x["capacity_bind_2045_mean"] = float(o["capacity_bind"][:, yi(2045)].mean())
    return x
