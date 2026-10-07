"""Monte Carlo sampling through a structured Gaussian copula (see params.py for the factor model)."""
from __future__ import annotations

import numpy as np
from scipy import stats

from .params import FACTORS, PARAMS, TASK_CONC, TASK_MEANS, TASKS


def sample(n: int, seed: int = 20261007, overrides: dict | None = None) -> dict:
    """Draw `n` joint parameter sets.

    overrides: {param_name: quantile in (0,1)} pins a parameter at a quantile of its marginal
               (used for sensitivity analysis). Pinned parameters lose their factor correlation.
    Returns a dict of 1-D arrays, including the latent factors and Dirichlet task shares.
    """
    overrides = overrides or {}
    rng = np.random.default_rng(seed)
    z = {f: rng.standard_normal(n) for f in FACTORS}
    out: dict[str, np.ndarray] = {f: z[f] for f in FACTORS}

    for p in PARAMS:
        eps = rng.standard_normal(n)  # always drawn so common random numbers survive overrides
        if p.name in overrides:
            u = np.full(n, overrides[p.name])
        else:
            load = sum(p.loadings.get(f, 0.0) ** 2 for f in FACTORS)
            x = sum(p.loadings.get(f, 0.0) * z[f] for f in FACTORS) + np.sqrt(max(0.0, 1 - load)) * eps
            u = stats.norm.cdf(x)
        out[p.name] = p.ppf(u)
        if p.name == "ai_u":
            out["ai_u_raw"] = u  # keep quantile to classify regime

    g = rng.gamma(TASK_MEANS * TASK_CONC, 1.0, size=(n, len(TASKS)))
    if "task_shares" in overrides:
        g = np.tile(TASK_MEANS, (n, 1))
    g /= g.sum(axis=1, keepdims=True)
    for i, t in enumerate(TASKS):
        out[f"s_{t}"] = g[:, i]
    return out
