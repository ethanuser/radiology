"""How a shortage or surplus would be felt: pay relative to other physicians, and the job market for new graduates.

This is a readout of supply ÷ demand (R), not a labour-market model: pay does not feed back into supply or demand.

Pay. In radiology's history (model/history.py), pay relative to other physicians rose while radiologists were scarce and
fell while they were plentiful, roughly in proportion to the size of the imbalance:
    d ln(relative pay)/dt = -beta * ln R(t-1) - alpha * [ln(relative pay)(t-1) - ln p*].
beta is drawn from the history fit (80% range), which spans era-average imbalances of only about 2-5%; applying it to the
larger imbalances of fast-AI futures would be a large extrapolation, so imbalances beyond ±10% are treated as ±10% (the
readout then understates how far pay could move in those futures). Fitted on 2001-2014, it predicted the 2022-2025 pay surge
(+3.3%/yr predicted against about +4%/yr observed). alpha, a slow drift toward a normal relative level p* as fees, hours and entry respond, is a judgment
(half-life 3.5-14 years); without it a long surplus would cut pay without limit. p* is the pre-shortage relative level,
between about 15% below today's (before the 2022-2025 premium of about +4%/yr) and today's.

Job market for new graduates. Compared with 2012-13, the last surplus, which the history reconstruction puts at supply ÷
demand ≈1.05 (hiring flat at roughly the number of graduates; many took extra fellowships). "Meaningful oversupply"
(R > 1.10) is about twice that surplus.

Fees. Who keeps AI's time savings is a policy question: if fees per exam stay fixed, a radiologist's earnings per hour rise
by 1/(1 - time saved); if fees fall in proportion, they do not. Reported as illustrative arithmetic only.
"""
from __future__ import annotations

import numpy as np

from .simulate import YEARS

BETA = (0.79, 1.65)   # history.pay_fit()["beta_all"] p10-p90 (checked in tests)
ALPHA = (0.05, 0.20)  # judgment
CLIP = 0.10           # largest |ln R| fed to the pay response: about twice the largest era-average imbalance in the fit
P_STAR = (0.85, 1.0)  # judgment: normal relative pay, as a ratio to 2026
R_2012 = 1.05         # history reconstruction, 2012-13 episode, median (checked in tests)


def pay_index(R: np.ndarray, seed: int = 41) -> np.ndarray:
    """Radiologist pay relative to other physicians, 2026 = 1, for each future."""
    rng = np.random.default_rng(seed)
    n = R.shape[0]
    beta = rng.uniform(*BETA, n)
    alpha = rng.uniform(*ALPHA, n)
    lnstar = np.log(rng.uniform(*P_STAR, n))
    lnp = np.zeros_like(R)
    for j in range(1, R.shape[1]):
        x = np.clip(np.log(R[:, j - 1]), -CLIP, CLIP)  # do not extrapolate the history fit to much larger imbalances
        lnp[:, j] = lnp[:, j - 1] - beta * x - alpha * (lnp[:, j - 1] - lnstar)
    return np.exp(lnp)


def summary(o: dict, years=(2030, 2035, 2045, 2055, 2066)) -> dict:
    R = o["R"]
    pay = pay_index(R)
    yi = lambda y: int(y - YEARS[0])  # noqa: E731
    q = np.percentile(pay, [10, 25, 50, 75, 90], axis=0)
    out = {
        "pay_q": {f"p{p}": q[k].tolist() for k, p in enumerate((10, 25, 50, 75, 90))},
        "r_2012": R_2012, "beta": BETA, "alpha": ALPHA, "p_star": P_STAR, "clip": CLIP,
        "by_year": {},
    }
    for y in years:
        i = yi(y)
        out["by_year"][str(y)] = {
            "pay_p10": float(q[0, i]), "pay_p50": float(q[2, i]), "pay_p90": float(q[4, i]),
            "p_pay_down10": float((pay[:, i] <= 0.9).mean()), "p_pay_up10": float((pay[:, i] >= 1.1).mean()),
            "p_weak_hiring": float((R[:, i] >= R_2012).mean()),
        }
    return out
