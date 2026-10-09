"""How much do the headline probabilities depend on our choices?

Three kinds of uncertainty are kept apart:

* Monte Carlo (numerical) error: sampling noise from using a finite number of simulated futures. Tiny.
* Prior choice: the same model with different, separately motivated assumptions about the most subjective inputs.
  Implemented by importance-reweighting the main run (no re-simulation), so the futures are identical and only
  their weights change.
* Model structure: alternative equations for things the main model fixes by construction (no-sign-off autonomy,
  unordered automation, extra demand channels, payer pushback). Implemented by re-simulating.

The resulting range is a sensitivity band, not a confidence interval: it shows how far defensible alternative
choices move the answer.
"""
from __future__ import annotations

import numpy as np

from .params import PARAM_INDEX
from .sampling import sample
from .simulate import COUNTERFACTUALS, STRUCTURES, YEARS, consistent_with_today, simulate, subset

OVERSUPPLY = 1.10
YRS = (2030, 2035, 2045, 2055, 2066)
BASE_W = np.array([0.15, 0.55, 0.18, 0.12])

PRIOR_SETS = {
    "main": dict(label="This site's assumptions", weights=BASE_W, util=None,
                 note="Imaging growth per person starts near 1.2%/yr.", sources=[]),
    "ai_skeptic": dict(label="AI-skeptical", weights=np.array([0.30, 0.55, 0.12, 0.03]), util=None,
                       note="Regime weights 30/55/12/3, nearer forecasting panels, which put far lower odds on transformative AI than AI-lab leaders.",
                       sources=["leap_2025", "karger_2023"]),
    "ai_bullish": dict(label="AI-bullish", weights=np.array([0.05, 0.35, 0.30, 0.30]), util=None,
                       note="Regime weights 5/35/30/30, nearer AI-lab leaders and AI 2027 (a widely read scenario of very fast AI progress).",
                       sources=["ai2027", "metr_2026"]),
    "imaging_restraint": dict(label="Imaging restraint", weights=BASE_W, util=(0.4, 0.7),
                              note="Imaging per person grows ~0.4%/yr: close to claims-based 2018-22 trends, plus payer and Medicare cost pressure (v1.5 assumed 0.6%/yr).",
                              sources=["christensen_util", "trustees_2026"]),
    "imaging_growth": dict(label="Imaging growth", weights=BASE_W, util=(1.8, 0.8),
                           note="Imaging per person grows ~1.8%/yr: what the history reconstruction implies for 2022-2026, near recent CT growth.",
                           sources=["smith_bindman_2025", "rosenkrantz_2025"]),
    "residency_slows": dict(label="Residency growth slows", weights=BASE_W, util=None, slot=(0.5, 0.6),
                            note="Positions grow only ~0.5%/yr as Medicare GME caps bind.", sources=["malhotra_2026"]),
    "residency_growth": dict(label="Residency growth continues", weights=BASE_W, util=None, slot=(1.9, 0.8),
                             note="Residency positions keep growing ~1.9%/yr, the 2010-2025 pace.", sources=["malhotra_2026"]),
    # the two corners: change both of the most consequential priors at once
    "favorable": dict(label="Lowest-risk combination: AI-skeptical + imaging growth", weights=np.array([0.30, 0.55, 0.12, 0.03]),
                      util=(1.8, 0.8), note="Combines the two single changes that lower oversupply risk most.", sources=[]),
    "unfavorable": dict(label="Highest-risk combination: AI-bullish + imaging restraint", weights=np.array([0.05, 0.35, 0.30, 0.30]),
                        util=(0.4, 0.7), note="Combines the two single changes that raise oversupply risk most.", sources=[]),
}
CORNERS = ("favorable", "unfavorable")


def _cond(o):
    keep = consistent_with_today(o)
    out = subset(o, keep)
    out["kept_share"] = float(keep.mean())
    return out


def _wquantile(x, w, q):
    i = np.argsort(x)
    c = np.cumsum(w[i])
    return float(x[i][np.searchsorted(c, q * c[-1])])


def _metrics(o, w):
    kept = o.get("kept_share")
    w = np.ones(len(o["R"])) if w is None else w
    w = w / w.sum()
    yi = {y: int(y - YEARS[0]) for y in YRS}
    ess = 1.0 / np.sum(w ** 2)
    out = {"ess": float(ess), "kept_share": kept}
    for y in YRS:
        i = yi[y]
        p = float(np.sum(w * (o["R"][:, i] > OVERSUPPLY)))
        out[str(y)] = {
            "p_over": p,
            "se": float(np.sqrt(p * (1 - p) / ess)),
            "p_short10": float(np.sum(w * (o["R"][:, i] < 0.9))),
            "p_below_today": float(np.sum(w * (o["D"][:, i] < 1.0))),
            "p_below_50": float(np.sum(w * (o["D"][:, i] < 0.5))),
            "p_jevons": float(np.sum(w * o["jevons"][:, i])),
            "D_p50": _wquantile(o["D"][:, i], w, 0.5),
        }
    return out


def _util_density(x, mu, sd):
    return np.exp(-0.5 * ((x - mu) / sd) ** 2) / sd


def prior_sets(s, o):
    """Importance-reweight the main run to each alternative prior set."""
    reg = o["regime"]
    freq = np.bincount(reg, minlength=4) / len(reg)
    base_u = PARAM_INDEX["util_g0"].args
    res = {}
    for key, ps in PRIOR_SETS.items():
        # relative to the prior regime weights, so conditioning on events applies to every set alike
        w = np.ones(len(reg)) if key == "main" else ps["weights"][reg] / BASE_W[reg]
        if ps["util"]:
            mu, sd = ps["util"]
            w = w * _util_density(s["util_g0"], mu, sd) / _util_density(s["util_g0"], base_u["mu"], base_u["sd"])
        if ps.get("slot"):  # slot_g has no factor loadings, so reweighting its marginal is exact
            mu, sd = ps["slot"]
            bs = PARAM_INDEX["slot_g"].args
            w = w * _util_density(s["slot_g"], mu, sd) / _util_density(s["slot_g"], bs["mu"], bs["sd"])
        res[key] = {"label": ps["label"], "note": ps["note"], "sources": ps["sources"], **_metrics(o, w)}
    return res


STRUCT_SHORT = {"base": "Main model", "no_signoff": "No radiologist on AI-first reads", "unordered": "Tiers automated in any order",
                "open_demand": "Much more new imaging", "payer_pushback": "Stronger payer pushback",
                "uncapped_new_uses": "New uses not capped by scanners", "no_shortage_today": "No shortage today",
                "tai_gated": "Transformative boost waits for regulation", "no_adjustment": "No market adjustment",
                "assistive_only": "Assistive AI only", "no_ai": "No further radiology AI"}


def structures(n: int = 20000, seed: int = 20261007):
    """Re-simulate the same sampled futures under each alternative model structure."""
    s = sample(n, seed=seed)
    res = {}
    for key, label in STRUCTURES.items():
        o = _cond(simulate(s, structure=key))
        res[key] = {"label": STRUCT_SHORT[key], "detail": label, "counterfactual": key in COUNTERFACTUALS,
                    **_metrics(o, np.ones(len(o["R"])))}
    # the main prior rules out a balanced market today (0.88-0.99); re-simulate with no shortage in 2026
    s2 = dict(s)
    s2["ratio0"] = np.random.default_rng(seed + 1).uniform(0.95, 1.03, n)
    # tier-1 capability centred on 2022 (EU CE marking) instead of 2025
    s3 = dict(s)
    s3["tcap1_T0"] = np.asarray(s["tcap1_T0"]) - 3.0
    res["tier1_2022"] = {"label": "Normal-X-ray AI capable since 2022", "counterfactual": False,
                         "detail": "Tier-1 capability centred on 2022 (EU approval) instead of 2025. If AI could do this since 2022 and the FDA still has not approved it, regulation must be slow, so fewer fast-AI futures fit the facts",
                         **_metrics(_cond(simulate(s3)), None)}
    res["no_shortage_today"] = {"label": STRUCT_SHORT["no_shortage_today"], "counterfactual": False,
                                "detail": "Today's supply ÷ demand anywhere from 0.95 to 1.03 (main model: full range 0.88-0.99)",
                                **_metrics(_cond(simulate(s2)), None)}
    return res


def resim_check(n: int = 20000, seed: int = 20261007):
    """Cross-check of importance reweighting: re-simulate the imaging-growth prior sets by changing only the
    util_g0 marginal (the copula and every other input unchanged)."""
    from .params import PARAM_INDEX as PI
    out = {}
    p = PI["util_g0"]
    saved = dict(p.args)
    try:
        for key in ("imaging_restraint", "imaging_growth"):
            mu, sd = PRIOR_SETS[key]["util"]
            p.args.update(mu=mu, sd=sd)
            o = _cond(simulate(sample(n, seed=seed)))
            out[key] = {str(y): float((o["R"][:, int(y - YEARS[0])] > OVERSUPPLY).mean()) for y in YRS}
    finally:
        p.args.clear()
        p.args.update(saved)
    return out


def run(s, o, n: int = 20000, seed: int = 20261007) -> dict:
    pri = prior_sets(s, o)
    st = structures(n, seed)
    band = {}
    for y in YRS:
        alts = [v for v in st.values() if not v["counterfactual"]]
        single = [v[str(y)]["p_over"] for k, v in pri.items() if k not in CORNERS] + [v[str(y)]["p_over"] for v in alts]
        vals = single + [pri[k][str(y)]["p_over"] for k in CORNERS]
        jev = [v[str(y)]["p_jevons"] for v in pri.values()] + [v[str(y)]["p_jevons"] for v in alts]
        band[str(y)] = {"lo": min(vals), "hi": max(vals), "single_lo": min(single), "single_hi": max(single),
                        "jev_lo": min(jev), "jev_hi": max(jev)}
    min_ess = min(v["ess"] for v in pri.values())
    return {"priors": pri, "structures": st, "band": band, "n": n, "min_ess": min_ess, "resim_check": resim_check(n, seed)}
