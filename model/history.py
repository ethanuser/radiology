"""Radiology's own history, 1995-2026: a test of the model's accounting and forecasting rules, the calibration of the
market adjustment, and the reconstruction of today's supply/demand balance.

The evidence is split by time: job-market episodes up to 2013 are *training*; episodes from 2015 on are *validation* and are
not used to fit anything that is then scored on them. The driver ranges and episode bands were set in 2026, after the
outcomes were known, so only the time split guards against fitting to the held-out years.

1. Supply check. The model's cohort machinery, run backward, against measured headcount growth and exit rates.
2. Reconstruction. Supply ÷ demand evolves by accounting,
       ln R*(t) = ln R*(t-1) + [headcount growth + capacity per radiologist - demographics - per-person work] in year t,
   plus a *market adjustment* A that closes a share `lam` of the remaining gap each year, up to a cumulative limit `b`
   (work moving between radiologists and other physicians, the pace of labour-saving change):
       A(t) = clip(A(t-1) + lam * ln R(t-1), -b, b),   ln R(t) = ln R*(t) - A(t).
   Each era's growth rates are drawn from ranges set from published series (DRIVERS); the 1995 balance, lam and b are
   unknown. Futures are weighted by agreement with the documented state of the job market (EPISODES, soft bands). Training
   weights use the 1995-2013 episodes; their predictions for 2015-2025 are checked against the validation episodes, with
   and without the adjustment. With all episodes, the reconstruction estimates the 2026 balance and recent per-person work
   growth, which the main model uses.
3. Forecasts from past start years (2000, 2005, 2010, 2016). A mechanical version of the method's demand rule (the recent
   per-person trend, decaying toward a third of itself with a half-life of 6-20 years, with the main model's spreads times
   a multiplier w) and capacity rule (the recent trend continues) forecasts supply ÷ demand from the reconstruction as it
   stood at the start year (episodes up to then only). Scored by the log probability given to each later episode's band.
   Variants: v1.5 rules (no adjustment, w = 1) and history-trained rules (adjustment from the training fit; w chosen on
   training episodes). Baselines: persistence (a random walk from the start) and "always balanced".
4. Pay. Radiologist pay relative to other physicians rose in shortages and fell in surpluses. A rate model,
   d ln(relative pay)/dt = -beta * ln R(t-1), is fitted on 2001-2014 and checked on 2022-2025.
"""
from __future__ import annotations

import numpy as np

from .simulate import H_RET, HAZARD, _historical_entrants

Y0, Y1 = 1995, 2026
YH = np.arange(Y0, Y1 + 1)

# ------------------------------------------------------------------------------------------------ inputs (%/yr ranges)
# Year t's rate applies from t-1 to t. Ranges are uniform; one draw per era per future.
DRIVERS = {
    # population growth (≈1.2%/yr in the late 1990s falling to ≈0.5%/yr) plus aging (≈0.3-0.5%/yr more imaging work)
    "demo": [(1995, 1999, 1.3, 1.7), (2000, 2010, 1.1, 1.5), (2011, 2019, 0.9, 1.3), (2020, 2026, 0.7, 1.1)],
    # radiologist work per person (volume x complexity): Medicare radiologist volume +3.4%/yr 1998-2005 and +0.8%/yr
    # 2005-2008, with complexity adding ≈1.6%/yr; professional RVU rates fell 2009-2014; use stabilized by 2016; growth since
    "work": [(1995, 1999, 2.5, 6.0), (2000, 2005, 2.5, 6.5), (2006, 2008, -0.5, 2.0), (2009, 2014, -3.0, 0.0),
             (2015, 2019, 0.0, 2.5), (2020, 2021, -1.0, 1.0), (2022, 2026, 0.5, 3.0)],
    # work capacity per radiologist at normal effort (PACS, voice recognition, teleradiology). Measured RVUs per FTE rose
    # ≈4%/yr in 1992-2003 and ≈2.4%/yr in 2003-2007, partly by working harder during the shortage; flat 2018-2024
    "prod": [(1995, 1999, 1.0, 3.5), (2000, 2005, 2.0, 5.5), (2006, 2008, 1.0, 3.0), (2009, 2017, 0.0, 2.0),
             (2018, 2026, -0.5, 1.0)],
    # practicing radiologists (FTE): +39% 1995-2011; +12% 2010-2022; recent pipeline growth
    "supply": [(1995, 2010, 1.5, 2.4), (2011, 2022, 0.5, 1.5), (2023, 2026, 0.6, 1.5)],
}
DRIVER_LABELS = {"demo": "Population and aging", "work": "Radiologist work per person",
                 "prod": "Work capacity per radiologist", "supply": "Practicing radiologists"}
DRIVER_SOURCES = {
    "demo": ["census_pop", "christensen_util"],
    "work": ["levin_2011", "bhargavan_2009", "levin_2017", "hong_2020", "christensen_util", "zamani_2026"],
    "prod": ["bhargavan_2009", "zamani_2026"],
    "supply": ["rosenkrantz_2016", "malhotra_2026", "christensen_supply"],
}
R_1995 = (0.95, 1.20)   # unknown starting balance (prior)
LAM = (0.0, 0.6)        # adjustment speed prior, share of the gap closed per year
BOUND = (0.0, 0.3)      # cumulative adjustment limit prior

# Documented state of the job market. Bands are on the episode-average supply ÷ demand.
EPISODES = [
    dict(key="mid1990s", years=(1995, 1996), band=(1.03, 1.20), state="Surplus", split="train",
         evidence="job ads fell to one-eighth of their 1991 peak; as few as 0.25 job listings per job seeker; residency "
                  "positions cut", sources=["forman_2000", "sunshine_2007"]),
    dict(key="y2000", years=(1999, 2001), band=(0.85, 0.96), state="Shortage", split="train",
         evidence="ads up 75% in 1999; up to 3.8 listings per job seeker; 51% of radiologists wanted less work in 2000",
         sources=["covey_2000", "sunshine_2007", "sunshine_2004"]),
    dict(key="y2004", years=(2003, 2005), band=(0.97, 1.03), state="Balanced", split="train",
         evidence="net desired workload change ≈0% (2003); about 1.1 listings per job seeker",
         sources=["meghea_2005", "sunshine_2007"]),
    dict(key="y2007", years=(2007, 2007), band=(1.00, 1.07), state="Mild surplus", split="train",
         evidence="0.72 listings per job seeker; desirable jobs harder to find", sources=["sunshine_2007"]),
    dict(key="y2012", years=(2012, 2013), band=(1.01, 1.12), state="Surplus", split="train",
         evidence="hiring flat and roughly equal to the ≈1,200 graduates; job deficits for new graduates",
         sources=["bluth_2012", "bluth_2014", "pfeifer_2017"]),
    dict(key="y2015", years=(2015, 2016), band=(0.96, 1.04), state="Recovering", split="validate",
         evidence="job opportunities rising since 2013; 2016 hiring projected 16% above 2015",
         sources=["bluth_2015", "bluth_2016"]),
    dict(key="y2018", years=(2017, 2019), band=(0.92, 1.01), state="Tightening", split="validate",
         evidence="1,434-1,861 hires in 2017 against ≈1,200 graduates; a 'positive picture' for job seekers",
         sources=["bender_2019"]),
    dict(key="y2023", years=(2022, 2025), band=(0.85, 0.97), state="Shortage", split="validate",
         evidence="67% of radiologists said their practices were understaffed (2022 survey); practice turnover up to 8.5% (2022); "
                  "record residency positions (coded without pay data, which test the pay readout)",
         sources=["dibble_2025", "parikh_2026", "nrmp_2026"]),
]
SOFT = 0.01  # softness of band edges (supply ÷ demand units)

# Supply check targets
HEADCOUNT = [dict(years=(1995, 2011), growth=0.392, split="train", source="rosenkrantz_2016"),
             dict(years=(2010, 2022), growth=0.12, split="validate", source="malhotra_2026")]
EXIT_RATES = [dict(year=2014, rate=0.011, split="train"), dict(year=2019, rate=0.020, split="train"),
              dict(year=2022, rate=0.025, split="validate")]  # Medicare radiologists' unadjusted exit rate (rula_2026)

# Radiologist pay growth minus other physicians' pay growth, %/yr. One rule for every era: the band runs from 1 point below
# the smallest to 1 point above the largest yearly difference reported in the cited sources for years in that era.
PAY = [dict(years=(2001, 2006), lo=2.0, hi=4.0, split="train", sources=["mgma_2007"],
            note="2006: radiology +4.7% vs specialists +1.7% (+3.0 points); radiology rose about 5%/yr over the five years"),
       dict(years=(2009, 2014), lo=-7.6, hi=-3.3, split="train", sources=["mgma_2011", "amga_2015"],
            note="2010: radiology -1.6% vs +4% to +6% for other specialties (about -6.6 points); 2014: +1.6% vs +5.9% for "
                 "medical specialties (-4.3)"),
       dict(years=(2022, 2025), lo=2.8, hi=5.6, split="validate",
            sources=["doximity_2023", "doximity_2025", "doximity_2026"],
            note="radiology minus all physicians: +4.0 points (2022), +3.8 (2024), +4.6 (2025); 2023 has no comparator in "
                 "the cited sources")]

ORIGINS = (2000, 2005, 2010, 2016)
WIDTHS = (0.75, 1.0, 1.5, 2.0)
SD_G0, SD_GINF, SD_PROD = 0.76, 0.5, 0.75  # v1.5 spreads: per-person + complexity growth now; long run; capacity (judgment)
HALF_LIFE = (6.0, 20.0)
FLOOR = 0.02  # probability floor in log scores, so one miss does not dominate


def _rates(rng, n):
    """Annual growth (fraction) per driver for n futures: one uniform draw per era."""
    out = {}
    for k, eras in DRIVERS.items():
        r = np.zeros((n, len(YH)))
        for a, b, lo, hi in eras:
            r[:, (YH >= a) & (YH <= b)] = rng.uniform(lo, hi, n)[:, None] / 100
        out[k] = r
    return out


def _evolve(r0, g, lam, b):
    """Supply ÷ demand from a starting value, annual accounting growth g (first column ignored) and the market adjustment."""
    lnR = np.zeros(g.shape)
    lnR[:, 0] = np.log(r0)
    lnS = lnR[:, 0].copy()
    A = np.zeros(len(r0))
    for j in range(1, g.shape[1]):
        A = np.clip(A + lam * lnR[:, j - 1], -b, b)
        lnS = lnS + g[:, j]
        lnR[:, j] = lnS - A
    return np.exp(lnR)


def _growth(rates, lo=None):
    g = rates["supply"] + rates["prod"] - rates["demo"] - rates["work"]
    return g if lo is None else g[:, lo:]


def _episode_mean(R, years, upto=None, start=Y0):
    a, b = years
    b = min(b, upto) if upto is not None else b
    yrs = np.arange(start, start + R.shape[1])
    m = (yrs >= a) & (yrs <= b)
    return R[:, m].mean(axis=1)


def _band_lik(x, band):
    lo, hi = band
    return 1 / (1 + np.exp(-(x - lo) / SOFT)) / (1 + np.exp(-(hi - x) / SOFT))


def _weights(R, episodes, upto=None):
    w = np.ones(R.shape[0])
    for e in episodes:
        if upto is not None and e["years"][0] > upto:
            continue
        w *= _band_lik(_episode_mean(R, e["years"], upto), e["band"])
    return w / w.sum()


def _wq(x, w, qs=(10, 50, 90)):
    o = np.argsort(x)
    c = np.cumsum(w[o])
    return {f"p{q}": float(x[o][min(np.searchsorted(c, q / 100), len(x) - 1)]) for q in qs}


def ess(w):
    return float(1 / np.sum(w ** 2))


# ------------------------------------------------------------------------------------------------ 1. supply check
def supply_check() -> dict:
    """Headcount growth and exit rates implied by the model's own cohort machinery (entry history and exit hazard)."""
    surv = np.cumprod(np.r_[1.0, 1 - HAZARD[:-1]])
    coh = lambda Y: np.array([_historical_entrants(Y - k) * surv[k] for k in range(len(HAZARD))])  # noqa: E731
    out = {"headcount": [], "exits": [], "retire_hazard": H_RET}
    for h in HEADCOUNT:
        a, b = h["years"]
        out["headcount"].append(dict(h, model=float(coh(b).sum() / coh(a).sum() - 1)))
    for e in EXIT_RATES:
        c = coh(e["year"])
        out["exits"].append(dict(e, model=float((c * HAZARD).sum() / c.sum())))
    return out


def supply_refit() -> dict:
    """Can the cohort machinery fit history if its pre-1995 entry and exit hazard are refitted? Grid search on the training
    targets (1995-2011 growth; 2014 and 2019 exit rates) with mean career length kept within 34.2-35.7 years
    (Christensen et al), then scored on the held-out targets."""
    import itertools

    def hazard(y50, h0, hs):
        y = np.arange(len(HAZARD))
        h = np.clip(h0 + H_RET / (1 + np.exp(-(y - y50) / hs)), 0, 1)
        h[-1] = 1.0
        return h

    def entrants(Y, base, mid):  # logistic ramp before 1995 (radiology grew rapidly from the 1960s), model's series after
        if Y >= 1995:
            return _historical_entrants(Y)
        f = lambda y: base + (1 - base) / (1 + np.exp(-(y - mid) / 4.0))  # noqa: E731
        return _historical_entrants(1995) * f(Y) / f(1995)

    best = None
    for base, mid, y50, h0, hs in itertools.product((0.2, 0.3, 0.4, 0.5), range(1970, 1992, 2), np.arange(31, 38.5, 0.5),
                                                    (0.0005, 0.001, 0.002, 0.004), (2.0, 3.0)):
        h = hazard(y50, h0, hs)
        surv = np.cumprod(np.r_[1.0, 1 - h[:-1]])
        life = float((surv * h * (np.arange(len(h)) + 0.5)).sum())
        coh = lambda Y: np.array([entrants(Y - k, base, mid) * surv[k] for k in range(len(h))])  # noqa: E731
        ex = lambda Y: float((coh(Y) * h).sum() / coh(Y).sum())  # noqa: E731
        g = float(coh(2011).sum() / coh(1995).sum() - 1)
        loss = ((g - 0.392) / 0.05) ** 2 + ((ex(2014) - 0.011) / 0.004) ** 2 + ((ex(2019) - 0.020) / 0.004) ** 2 \
            + (max(0.0, abs(life - 34.95) - 0.75) / 0.5) ** 2
        if best is None or loss < best[0]:
            best = (loss, dict(growth_1995_2011=g, exit_2014=ex(2014), exit_2019=ex(2019), career=life,
                               growth_2010_2022=float(coh(2022).sum() / coh(2010).sum() - 1), exit_2022=ex(2022)))
    return best[1]


# ------------------------------------------------------------------------------------------------ 2. reconstruction
def reconstruct(n: int = 300_000, seed: int = 1995, adjust: bool = True, lam_prior=LAM, b_prior=BOUND) -> dict:
    rng = np.random.default_rng(seed)
    r0 = rng.uniform(*R_1995, n)
    rates = _rates(rng, n)
    lam = rng.uniform(*lam_prior, n) if adjust else np.zeros(n)
    b = rng.uniform(*b_prior, n) if adjust else np.zeros(n)
    R = _evolve(r0, _growth(rates), lam, b)
    train = [e for e in EPISODES if e["split"] == "train"]
    w_train = _weights(R, train)
    w_all = _weights(R, EPISODES)
    ep = []
    for e in EPISODES:
        x = _episode_mean(R, e["years"])
        hit = _band_lik(x, e["band"]) > 0.5
        ep.append(dict(e, p_prior=float(hit.mean()), p_train=float((w_train * hit).sum()),
                       p_all=float((w_all * hit).sum()), train_q=_wq(x, w_train), all_q=_wq(x, w_all)))
    val = [e for e in ep if e["split"] == "validate"]
    out = dict(adjust=adjust, years=YH.tolist(), episodes=ep, n=n, ess_train=ess(w_train), ess_all=ess(w_all),
               brier_validation={k: float(np.mean([(1 - e[f"p_{k}"]) ** 2 for e in val])) for k in ("prior", "train")},
               ratio2026_train=_wq(R[:, -1], w_train), ratio2026_all=_wq(R[:, -1], w_all),
               _R=R, _w_train=w_train, _w_all=w_all, _rates=rates, _lam=lam, _b=b)
    if adjust:
        out["lam_train"], out["lam_all"] = _wq(lam, w_train), _wq(lam, w_all)
        out["b_train"], out["b_all"] = _wq(b, w_train), _wq(b, w_all)
        out["p_weak_adjustment_train"] = float(w_train[b < 0.05].sum())
    bands = {}
    for name, w in (("train", w_train), ("all", w_all)):
        q = np.array([[_wq(R[:, j], w)[f"p{p}"] for p in (10, 50, 90)] for j in range(len(YH))])
        bands[name] = {"p10": q[:, 0].tolist(), "p50": q[:, 1].tolist(), "p90": q[:, 2].tolist()}
    out["bands"] = bands
    drivers = {}
    for k, eras in DRIVERS.items():
        for a, bb, lo, hi in eras:
            x = rates[k][:, int(np.searchsorted(YH, a))] * 100
            drivers[f"{k}_{a}_{bb}"] = dict(driver=k, years=(a, bb), lo=lo, hi=hi, train=_wq(x, w_train), all=_wq(x, w_all))
    out["drivers"] = drivers
    return out


# ------------------------------------------------------------------------------------------------ 3. past start years
def _trailing(k, t0, span=5):
    """Recent trend as a forecaster at t0 would have read it: the mean of the era midpoints over the last `span` years."""
    vals = [(lo + hi) / 2 for y in range(t0 - span + 1, t0 + 1) for a, b, lo, hi in DRIVERS[k] if a <= y <= b]
    return float(np.mean(vals))


def forecast_from(t0: int, rec: dict, w: float = 1.0, adjust: bool = False, n: int = 20_000, seed: int = 7) -> np.ndarray:
    """Supply ÷ demand for t0..2026 as forecast at t0 by the method's rules; rows are futures."""
    rng = np.random.default_rng(seed + t0)
    R = rec["_R"]
    i0 = int(t0 - Y0)
    w0 = _weights(R, EPISODES, upto=t0)  # what was known about the market by t0
    r0 = R[rng.choice(len(w0), size=n, p=w0), i0]
    fresh = _rates(rng, n)  # demographics and headcount: realized ranges (population and the training pipeline were known)
    yrs = YH[i0:]
    dt = (yrs - t0).astype(float)[None, :]
    g_tr, p_tr = _trailing("work", t0), _trailing("prod", t0)
    g0 = rng.normal(g_tr, SD_G0 * w, n)[:, None]
    ginf = rng.normal(g_tr / 3, SD_GINF * w, n)[:, None]
    hl = rng.uniform(*HALF_LIFE, n)[:, None]
    work = (ginf + (g0 - ginf) * 2 ** (-dt / hl)) / 100
    prod = np.repeat(rng.normal(p_tr, SD_PROD * w, n)[:, None], len(yrs), axis=1) / 100
    g = fresh["supply"][:, i0:] + prod - fresh["demo"][:, i0:] - work
    if adjust:  # adjustment speed and limit from the training fit only
        k = rng.choice(len(rec["_w_train"]), size=n, p=rec["_w_train"])
        lam, b = rec["_lam"][k], rec["_b"][k]
    else:
        lam = b = np.zeros(n)
    return _evolve(r0, g, lam, b)


def _baseline(t0, rec, kind, n=20_000, seed=11, sigma=0.02):
    rng = np.random.default_rng(seed + t0)
    i0 = int(t0 - Y0)
    m = len(YH) - i0
    if kind == "balanced":
        return np.exp(rng.normal(0, 0.06, (n, 1))) * np.ones((1, m))
    w0 = _weights(rec["_R"], EPISODES, upto=t0)
    r0 = rec["_R"][rng.choice(len(w0), size=n, p=w0), i0]
    steps = rng.normal(0, sigma, (n, m))
    steps[:, 0] = 0
    return r0[:, None] * np.exp(np.cumsum(steps, axis=1))


def _prob(Rf, t0, e):
    """Probability a forecast made at t0 gives to episode e's band (episode-average supply ÷ demand)."""
    x = _episode_mean(Rf, e["years"], start=t0)
    return float(((x >= e["band"][0]) & (x <= e["band"][1])).mean())


def past_forecasts(rec: dict, horizon: int = 16) -> dict:
    pairs = [(t0, e) for t0 in ORIGINS for e in EPISODES if e["years"][0] > t0 and e["years"][1] <= t0 + horizon]
    methods = {"v15": [(t0, forecast_from(t0, rec, 1.0, False)) for t0 in ORIGINS]}
    for w in WIDTHS:
        methods[f"trained_w{w}"] = [(t0, forecast_from(t0, rec, w, True)) for t0 in ORIGINS]
    for k in ("persistence", "balanced"):
        methods[k] = [(t0, _baseline(t0, rec, k)) for t0 in ORIGINS]
    scores, probs = {}, {}
    for name, fcs in methods.items():
        fd = dict(fcs)
        sc = {"train": [], "validate": []}
        probs[name] = []
        for t0, e in pairs:
            p = _prob(fd[t0], t0, e)
            probs[name].append(p)
            sc[e["split"]].append(np.log(max(FLOOR, p)))
        scores[name] = {k: float(np.mean(v)) for k, v in sc.items()}
    best = max(WIDTHS, key=lambda w: scores[f"trained_w{w}"]["train"])
    trained = f"trained_w{best}"
    fans = {}
    for name in ("v15", trained):
        for t0, F in methods[name]:
            q = np.percentile(F, [10, 50, 90], axis=0)
            fans[f"{name}_{t0}"] = {"years": YH[int(t0 - Y0):].tolist(), "p10": q[0].tolist(), "p50": q[1].tolist(),
                                    "p90": q[2].tolist()}
    table = [dict(origin=t0, episode=e["key"], state=e["state"], split=e["split"], years=e["years"],
                  p_v15=probs["v15"][i], p_trained=probs[trained][i], p_persistence=probs["persistence"][i],
                  p_balanced=probs["balanced"][i]) for i, (t0, e) in enumerate(pairs)]
    return dict(scores=scores, best_width=best, trained=trained, pairs=table, fans=fans, floor=FLOOR,
                trailing={t0: {"work": _trailing("work", t0), "prod": _trailing("prod", t0)} for t0 in ORIGINS})


# ------------------------------------------------------------------------------------------------ 4. pay
def pay_fit(rec: dict, n_draws: int = 4000, seed: int = 3) -> dict:
    """beta in d ln(relative pay)/dt = -beta ln R(t-1), by weighted least squares across pay eras, per reconstruction draw.
    Supply ÷ demand comes from the reconstruction with all job-market episodes, which are coded without pay data; beta is
    fitted on the training pay eras and checked on the held-out one, then refitted on all eras for use in model/labor.py."""
    rng = np.random.default_rng(seed)
    R = rec["_R"][rng.choice(len(rec["_w_all"]), size=n_draws, p=rec["_w_all"])]
    lag_mean = lambda a, b: -np.log(R[:, (YH >= a - 1) & (YH <= b - 1)]).mean(axis=1)  # noqa: E731
    out = {}
    for fit in ("train", "all"):
        eras = [p for p in PAY if fit == "all" or p["split"] == "train"]
        X = np.stack([lag_mean(*p["years"]) for p in eras], 1)
        y = np.array([(p["lo"] + p["hi"]) / 2 / 100 for p in eras])
        s = np.array([(p["hi"] - p["lo"]) / 2 / 100 for p in eras])
        beta = np.maximum(0.0, (X * y / s ** 2).sum(1) / (X ** 2 / s ** 2).sum(1))
        out[f"beta_{fit}"] = {f"p{q}": float(np.percentile(beta, q)) for q in (10, 50, 90)}
        if fit == "train":
            out["validation"] = []
            for p in PAY:
                if p["split"] == "validate":
                    pred = beta * lag_mean(*p["years"]) * 100
                    q = {f"p{k}": float(np.percentile(pred, k)) for k in (10, 50, 90)}
                    out["validation"].append(dict(years=p["years"], lo=p["lo"], hi=p["hi"], pred=q,
                                                  inside=bool(p["lo"] <= q["p50"] <= p["hi"])))
    return out


def driver_sensitivity(n: int = 300_000, widen: float = 1.5) -> dict:
    """Held-out Brier scores with every driver range widened by `widen` around its midpoint: is the gain from the market
    adjustment an artefact of driver ranges set too narrow?"""
    global DRIVERS
    saved = DRIVERS
    DRIVERS = {k: [(a, b, (lo + hi) / 2 - widen * (hi - lo) / 2, (lo + hi) / 2 + widen * (hi - lo) / 2) for a, b, lo, hi in v]
               for k, v in saved.items()}
    try:
        out = {"widen": widen, "adjust": reconstruct(n=n)["brier_validation"]["train"],
               "noadj": reconstruct(n=n, adjust=False)["brier_validation"]["train"]}
    finally:
        DRIVERS = saved
    return out


def asymmetry(n: int = 300_000, seed: int = 1995) -> dict:
    """Can history tell surplus-side from shortage-side adjustment? Separate limits for each direction, fitted on the
    training episodes; also the held-out Brier score with only one direction allowed."""
    rng = np.random.default_rng(seed)
    r0 = rng.uniform(*R_1995, n)
    g = _growth(_rates(rng, n))
    lam = rng.uniform(*LAM, n)
    b_up, b_down = rng.uniform(*BOUND, n), rng.uniform(*BOUND, n)

    def path(up, down):
        lnR = np.zeros(g.shape)
        lnR[:, 0] = np.log(r0)
        lnS, A = lnR[:, 0].copy(), np.zeros(n)
        for j in range(1, g.shape[1]):
            A = np.clip(A + lam * lnR[:, j - 1], -down, up)
            lnS = lnS + g[:, j]
            lnR[:, j] = lnS - A
        return np.exp(lnR)

    train = [e for e in EPISODES if e["split"] == "train"]
    val = [e for e in EPISODES if e["split"] == "validate"]

    def brier(R):
        w = _weights(R, train)
        return float(np.mean([(1 - (w * (_band_lik(_episode_mean(R, e["years"]), e["band"]) > 0.5)).sum()) ** 2 for e in val]))

    R = path(b_up, b_down)
    w = _weights(R, train)
    return dict(b_up=_wq(b_up, w), b_down=_wq(b_down, w), brier_both=brier(R),
                brier_surplus_only=brier(path(b_up, np.zeros(n))), brier_shortage_only=brier(path(np.zeros(n), b_down)))


def identification(n: int = 300_000) -> dict:
    """Does history bound the adjustment from above? Refit with wider priors (speed 0-0.8, limit 0-0.5) and compare the weight
    on each range of the limit with its prior share: a ratio near 1 means the data are silent there."""
    rec = reconstruct(n=n, lam_prior=(0.0, 0.8), b_prior=(0.0, 0.5))
    b, w = rec["_b"], rec["_w_train"]
    bins = [(0.0, 0.05), (0.05, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 0.5)]
    return dict(lam=rec["lam_train"], b=rec["b_train"], brier=rec["brier_validation"]["train"],
                b_bins=[dict(lo=lo, hi=hi, weight=float(w[(b >= lo) & (b < hi)].sum()), prior=(hi - lo) / 0.5) for lo, hi in bins])


def run() -> dict:
    rec = reconstruct(adjust=True)
    rec0 = reconstruct(adjust=False)
    past = past_forecasts(rec)
    pay = pay_fit(rec)
    strip = lambda d: {k: v for k, v in d.items() if not k.startswith("_")}  # noqa: E731
    sup = supply_check()
    sup["refit"] = supply_refit()
    return dict(reconstruction=strip(rec), no_adjustment=strip(rec0), past=past, pay=pay, supply=sup, wide=identification(),
                driver_sensitivity=driver_sensitivity(), asymmetry=asymmetry(),
                drivers_meta={k: dict(label=DRIVER_LABELS[k], sources=DRIVER_SOURCES[k], eras=v) for k, v in DRIVERS.items()})
