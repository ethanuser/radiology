"""Hindcast: run the method from 2016 and score it against what happened by 2025.

Protocol (fixed before looking at outcomes, applied mechanically to every occupation):
  * Baseline (non-AI) growth = an equal-weight combination of two forecasts available in 2016:
      - the BLS 2016-26 Employment Projection (interpolated geometrically to 2025), and
      - the prior trend (2006/2008 -> 2016 compound growth) extended 9 years.
    The spread between them sets the baseline uncertainty (forecast combination; disagreement = uncertainty).
  * An AI layer identical in structure to the main model: a share of work exposed to automation (mapped from
    Frey & Osborne's 2013 automation probability, the most-cited exposure estimate available in 2016),
    a capability S-curve whose timing uses the SAME AI-regime mixture as the main model, an adoption lag
    (longer where regulation applies), and a demand rebound (Jevons) term set by the occupation's demand
    elasticity class.
  * Radiology additionally gets a supply side (training pipeline is predetermined) and a 2016 starting balance.
Nothing below was tuned to the 2025 outcomes; misses are reported as they fall.
"""
from __future__ import annotations

import numpy as np
from scipy import stats

from .params import ai_multiplier, ai_regime

BASE, END = 2016, 2025
H = END - BASE

# ------------------------------------------------------------------------------------------------ data
# Employment (BLS Occupational Outlook Handbook / Employment Projections national matrix).
OCCUPATIONS = {
    "software": dict(
        label="Software developers", prior_year=2008, prior_emp=909_600, base_emp=1_256_200, bls_10yr=0.24,
        actual_end=1_717_800, fo_prob=0.085, elastic="high", regulated=False, cap_T0=2030.0,
        sources=["bls_ooh_2010_sw", "bls_ooh_2018_sw", "bls_ooh_2026_sw", "frey_osborne_2013"],
        note="2008 = applications + systems software engineers (OOH 2010-11); 2025 = software developers (OOH 2025-35)."),
    "translators": dict(
        label="Interpreters & translators", prior_year=2006, prior_emp=41_000, base_emp=68_200, bls_10yr=0.18,
        actual_end=73_900, fo_prob=0.38, elastic="mid", regulated=False, cap_T0=2022.0,
        sources=["bls_ooh_2008_tr", "bls_ooh_2018_tr", "bls_ooh_2026_tr", "frey_osborne_2013"],
        note="Neural machine translation launched at scale in 2016."),
    "transcription": dict(
        label="Medical transcriptionists", prior_year=2006, prior_emp=98_000, base_emp=57_400, bls_10yr=-0.03,
        actual_end=42_000, fo_prob=0.89, elastic="low", regulated=False, cap_T0=2020.0,
        sources=["bls_ooh_2008_mt", "bls_ooh_2018_mt", "bls_ooh_2026_mt", "frey_osborne_2013"],
        note="BLS projected +14% for 2006-16 (actual -41%) and -3% for 2016-26."),
}
ELASTIC_REBOUND = {"high": (0.6, 1.3), "mid": (0.2, 0.8), "low": (0.0, 0.3)}  # share of saved labour re-absorbed


def _beta_mean(mean, k=12):
    return mean * k, (1 - mean) * k


def _logistic(t, mid, width):
    return 1 / (1 + np.exp(-(t - mid) / width))


def hindcast_occupation(key: str, n: int = 20000, seed: int = 2016) -> dict:
    o = OCCUPATIONS[key]
    rng = np.random.default_rng(seed)
    # forecasts available in 2016
    trend = (o["base_emp"] / o["prior_emp"]) ** (1 / (BASE - o["prior_year"]))
    bls_idx = (1 + o["bls_10yr"]) ** (H / 10)
    trend_idx = trend ** H
    mu = 0.5 * (np.log(bls_idx) + np.log(trend_idx))
    sd = 0.5 * abs(np.log(trend_idx) - np.log(bls_idx)) + 0.03
    base = np.exp(rng.normal(mu, sd, n))
    # AI layer (same regime mixture as the main model)
    u = rng.uniform(size=n)
    M = ai_multiplier(u)
    exposure = rng.beta(*_beta_mean(0.05 + 0.5 * o["fo_prob"]), size=n)
    cap_mid = BASE + (o["cap_T0"] - BASE) * M
    cap = _logistic(END, cap_mid, 3.0)
    ahalf = rng.lognormal(np.log(5.5 if o["regulated"] else 3.0), 0.35, n)
    adopt = _logistic(END - cap_mid, ahalf, 1.5)
    lo, hi = ELASTIC_REBOUND[o["elastic"]]
    rebound = rng.uniform(lo, hi, n)
    ai_effect = np.maximum(0.05, 1 - exposure * cap * adopt * (1 - rebound))
    idx = base * ai_effect
    actual = o["actual_end"] / o["base_emp"]
    q = np.percentile(idx, [5, 10, 25, 50, 75, 90, 95])
    return dict(key=key, label=o["label"], actual=actual, trend=trend_idx, bls=bls_idx, fo_prob=o["fo_prob"],
                q={f"p{p}": v for p, v in zip((5, 10, 25, 50, 75, 90, 95), q)},
                pit=float((idx < actual).mean()), in80=bool(q[1] <= actual <= q[5]),
                err_model=float(np.log(q[3] / actual)), err_trend=float(np.log(trend_idx / actual)),
                err_bls=float(np.log(bls_idx / actual)), sources=o["sources"], note=o["note"],
                regime=ai_regime(u))


def hindcast_radiology(n: int = 20000, seed: int = 2017) -> dict:
    """Radiology as of 2016: will there be a shortage (supply < demand) in 2025?"""
    rng = np.random.default_rng(seed)
    u = rng.uniform(size=n)
    M = ai_multiplier(u)
    # demand without AI: demographics + per-capita use + complexity, as known in 2016
    g = rng.normal(0.020, 0.010, n)
    base = np.exp(g * H)
    # AI: 2016 priors were more aggressive about imaging AI than today's evidence (deep-learning optimism)
    exposure = rng.beta(*_beta_mean(0.35), size=n)
    cap_mid = BASE + (2024.0 - BASE) * M
    cap = _logistic(END, cap_mid, 3.0)
    reg_lag = rng.lognormal(np.log(8.0), 0.45, n)  # validation + FDA + payment/liability for labour substitution
    adopt = _logistic(END - cap_mid, reg_lag, 2.0)
    rebound = rng.uniform(0.2, 0.6, n)
    demand = base * np.maximum(0.05, 1 - exposure * cap * adopt * (1 - rebound))
    # supply: training pipeline largely fixed in 2016; starting balance near or above 1 (2015 glut)
    supply = np.exp(rng.normal(0.010, 0.003, n) * H)
    r2016 = stats.triang(0.5, loc=0.95, scale=0.15).rvs(n, random_state=rng)
    r2025 = r2016 * supply / demand
    return dict(p_shortage=float((r2025 < 1).mean()), p_oversupply=float((r2025 > 1.10).mean()),
                demand_q={f"p{p}": float(v) for p, v in zip((10, 50, 90), np.percentile(demand, [10, 50, 90]))},
                ratio_q={f"p{p}": float(v) for p, v in zip((10, 50, 90), np.percentile(r2025, [10, 50, 90]))},
                observed="shortage", hinton_p_shortage=0.05)


def run_backtest() -> dict:
    occ = [hindcast_occupation(k) for k in OCCUPATIONS]
    rad = hindcast_radiology()
    brier = {"model": (1 - rad["p_shortage"]) ** 2, "hinton": (1 - rad["hinton_p_shortage"]) ** 2,
             "coin_flip": 0.25}
    mae = {m: float(np.mean([abs(r[f"err_{m}"]) for r in occ])) for m in ("model", "trend", "bls")}
    for r in occ:
        r.pop("regime")
    # Frey & Osborne as a ranking: does higher automation probability go with weaker employment growth?
    fo = [r["fo_prob"] for r in occ] + [0.0042]
    growth = [r["actual"] for r in occ] + [None]
    return dict(base=BASE, end=END, occupations=occ, radiology=rad, brier=brier, mae_log=mae,
                coverage80=float(np.mean([r["in80"] for r in occ])), fo_rank=list(zip(fo, growth)))
