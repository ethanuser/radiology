"""Sanity, calibration and accounting tests.  Run:  python -m pytest -q"""
import numpy as np
import pytest
from scipy import stats

from model.analysis import run, validation
from model.params import PARAM_INDEX, PARAMS
from model.sampling import sample
from model.simulate import YEARS, simulate


@pytest.fixture(scope="module")
def sim():
    return run(6000, seed=123)


def test_index_normalisation(sim):
    s, o = sim
    assert np.allclose(o["D"][:, 0], 1.0)
    assert np.allclose(o["S"][:, 0], 1.0)
    assert np.allclose(o["P"][:, 0], 1.0)
    assert np.allclose(o["R"][:, 0], s["ratio0"])


def test_supply_reproduces_christensen(sim):
    s, o = sim
    v = validation(s, o)
    assert abs(v["supply_flat_2055_vs_2023"] - 1.257) < 0.002  # flat-residency scenario
    assert 33.5 < v["mean_career_years"] < 36.0  # Christensen: 34.2-35.7 years of practice
    assert 0.019 <= v["attrition_2023"] <= 0.031  # between pre- and post-COVID attrition


def test_demographics_consistent_with_christensen(sim):
    _, o = sim
    g = np.median(o["B_dem"][:, YEARS == 2055]) - 1
    # Christensen 2023-2055: +16.9% to +26.9% (Census 2023); CBO 2026 implies slower growth -> lower end
    assert 0.10 < g < 0.25


def test_jevons_accounting_identity(sim):
    _, o = sim
    # D_struct = B - L + I  (labour saved and induced demand reconcile exactly, before the market adjustment)
    assert np.allclose(o["D_struct"], o["B"] - o["L"] + o["I"], atol=1e-9)
    assert np.allclose(sum(o["channels"].values()), o["I"], atol=1e-9)
    assert np.array_equal(o["jevons"], o["I"] > o["L"])


def test_composition_sums_to_one(sim):
    _, o = sim
    tot = sum(o["composition"].values())
    assert np.allclose(tot, 1.0, atol=1e-9)


def test_bounds(sim):
    _, o = sim
    assert (o["auto"] >= 0).all() and (o["auto"] <= 1).all()
    assert (o["tau"] > 0).all()
    assert (o["D"] > 0).all() and (o["S"] > 0).all()


def test_marginals_preserved_by_copula():
    s = sample(20000, seed=5)
    for p in PARAMS:
        if p.dist == "ai_mixture":
            continue
        qs = np.array([0.1, 0.5, 0.9])
        expected = p.ppf(qs)
        got = np.quantile(s[p.name], qs)
        scale = max(1e-9, expected[2] - expected[0])
        assert np.all(np.abs(got - expected) / scale < 0.06), p.name


def test_intended_correlations():
    s = sample(20000, seed=6)
    M = s["ai_u"]  # timeline multiplier: small = fast AI
    assert stats.spearmanr(M, s["new_max"]).statistic < -0.2  # faster AI -> more new applications
    assert stats.spearmanr(M, s["thru_H"]).statistic < -0.2  # faster AI -> more scanner throughput
    assert stats.spearmanr(M, s["m_draft"]).statistic < -0.2  # faster AI -> higher task ceilings
    assert stats.spearmanr(s["lfda"], s["lpay"]).statistic > 0.3  # common regulatory friction factor


def test_regime_weights():
    s, o = run(20000, seed=9)
    w = np.bincount(o["regime"], minlength=4) / len(o["regime"])
    assert np.allclose(w, [0.15, 0.55, 0.18, 0.12], atol=0.015)


def test_overrides_pin_parameters():
    s = sample(1000, seed=1, overrides={"util_g0": 0.9})
    assert np.allclose(s["util_g0"], PARAM_INDEX["util_g0"].ppf(np.array([0.9]))[0])


def test_adoption_feedback_off_matches_single_pass():
    from model.simulate import _simulate_once
    s = sample(2000, seed=21, overrides={"adopt_pressure": 1e-9})
    o2 = simulate(s)
    o1 = _simulate_once(s, np.zeros_like(o2["D"]))
    assert np.allclose(o1["D"], o2["D"], atol=1e-6)


def test_market_adjustment():
    """The adjustment closes part of each gap, never exceeds its limit, and switching it off restores the v1.5 dynamics."""
    s = sample(3000, seed=17)
    on, off = simulate(s), simulate(s, structure="no_adjustment")
    lim = np.asarray(s["adj_max"])[:, None]
    assert (np.abs(on["adj"]) <= lim + 1e-12).all()
    assert np.allclose(off["adj"], 0) and np.allclose(off["D"], off["D_struct"])
    assert np.allclose(on["D"], on["D_struct"] * np.exp(on["adj"]))
    # surpluses raise and shortages lower the work that flows to radiologists
    i = 2045 - 2026
    assert np.corrcoef(np.log(off["R"][:, i]), on["adj"][:, i])[0, 1] > 0.5
    # it narrows the spread of supply ÷ demand
    assert np.std(np.log(on["R"][:, i])) < np.std(np.log(off["R"][:, i]))


def test_history_calibration_matches_model():
    """Numbers transferred by hand from the history test into params.py and labor.py must match the history fit."""
    from model import history, labor
    rec = history.reconstruct(n=120_000)
    for name, post in (("adj_speed", rec["lam_train"]), ("adj_max", rec["b_train"])):
        q = PARAM_INDEX[name].quantiles((0.1, 0.5, 0.9))
        assert all(abs(a - post[k]) < 0.03 for a, k in zip(q, ("p10", "p50", "p90"))), name
    q = rec["ratio2026_all"]
    assert 0.88 <= q["p10"] and q["p90"] <= 0.99  # the 2026 prior's range covers the reconstruction
    y12 = next(e for e in rec["episodes"] if e["key"] == "y2012")
    assert abs(y12["all_q"]["p50"] - labor.R_2012) < 0.015
    beta = history.pay_fit(rec)["beta_all"]
    assert abs(beta["p10"] - labor.BETA[0]) < 0.06 and abs(beta["p90"] - labor.BETA[1]) < 0.08
    # imaging growth: spread = v1.5 spread x the width chosen on the fitting episodes; centre between v1.5 and history
    past = history.past_forecasts(rec)
    u = PARAM_INDEX["util_g0"].args
    assert abs(u["sd"] - 0.7 * past["best_width"]) < 1e-9 and abs(PARAM_INDEX["util_ginf"].args["sd"] - 0.5 * past["best_width"]) < 1e-9
    hist_util = rec["drivers"]["work_2022_2026"]["all"]["p50"] - PARAM_INDEX["cmplx_g0"].args["mu"]
    assert 0.6 < u["mu"] < hist_util and abs(u["mu"] - (0.6 + hist_util) / 2) < 0.15
    # today's balance: the prior's mode is near the midpoint of v1.5's mode (0.93) and the reconstruction's median
    assert abs(PARAM_INDEX["ratio0"].args["mode"] - (0.93 + q["p50"]) / 2) < 0.01


def test_history_adjustment_validates():
    """Fitted on 1995-2013 only, the market adjustment predicts the held-out 2015-2025 episodes better than accounting alone."""
    from model import history
    with_adj = history.reconstruct(n=120_000)
    without = history.reconstruct(n=120_000, adjust=False)
    assert with_adj["brier_validation"]["train"] < without["brier_validation"]["train"] - 0.2


def test_every_reference_has_link_and_formats():
    from model.references import REFERENCES, format_ama, href
    for k in REFERENCES:
        assert href(k).startswith("http"), k
        assert format_ama(k, "md") and format_ama(k, "html")


def test_alternative_structures():
    """Alternative structures run, the default is unchanged, and each moves the result in the expected direction."""
    from model.sampling import sample
    from model.simulate import simulate
    s = sample(3000, seed=5)
    base, base2 = simulate(s), simulate(s, structure="base")
    assert np.allclose(base["D"], base2["D"])
    nos = simulate(s, structure="no_signoff")
    assert (nos["time_saved"] >= base["time_saved"] - 1e-12).all()  # removing sign-off can only save more time
    opn = simulate(s, structure="open_demand")
    assert opn["jevons"][:, -1].mean() >= base["jevons"][:, -1].mean()
    pay = simulate(s, structure="payer_pushback")
    assert np.median(pay["D"][:, -1]) <= np.median(base["D"][:, -1])
    unord = simulate(s, structure="unordered")
    assert np.isfinite(unord["D"]).all()
    # market-adjustment variants: bounds respected and oversupply ranked as expected
    so, cap, wide = (simulate(s, structure=k) for k in ("shortage_only", "adj_cap15", "adj_wide"))
    assert (so["adj"] <= 1e-12).all() and (np.abs(cap["adj"]) <= 0.15 + 1e-12).all()
    p = {k: (o["R"][:, 2045 - 2026] > 1.10).mean() for k, o in (("wide", wide), ("base", base), ("cap", cap), ("so", so))}
    assert p["wide"] <= p["base"] <= p["cap"] <= p["so"]


def test_prior_reweighting_main_is_identity():
    from model import analysis, robustness
    s, o = analysis.run(3000, seed=9)
    pri = robustness.prior_sets(s, o)
    p = (o["R"][:, 2045 - 2026] > 1.10).mean()
    assert abs(pri["main"]["2045"]["p_over"] - p) < 0.01  # main weights ≈ sampled regime frequencies
    assert pri["ai_bullish"]["2045"]["p_over"] > pri["ai_skeptic"]["2045"]["p_over"]


def test_no_ai_counterfactual_equals_baseline():
    """With AI frozen at 2026, demand is exactly baseline demand and AI saves no time."""
    from model.sampling import sample
    from model.simulate import simulate
    s = sample(2000, seed=13)
    o = simulate(s, structure="no_ai")
    assert np.allclose(o["D_struct"], o["B"], atol=1e-9)
    assert np.allclose(o["time_saved"], 0, atol=1e-12)
    a = simulate(s, structure="assistive_only")
    assert np.allclose(a["auto"], 0)


def test_archived_predictions_match_current_release():
    """Predictions are archived once per release; changing the model without bumping RELEASE must fail here."""
    import json
    from pathlib import Path
    import run_model
    from model import analysis
    root = Path(__file__).resolve().parents[1]
    arch = root / "outputs" / "predictions" / f"{run_model.RELEASE}.json"
    if not arch.exists():
        pytest.skip("no archive for this release yet; run run_model.py")
    s, o = analysis.run(20000)
    now = analysis.extra_metrics(s, o)["predictions"]
    old = json.loads(arch.read_text())["predictions"]
    assert [p["id"] for p in now] == [p["id"] for p in old]
    for a, b in zip(now, old):
        for k in ("p", "p50"):
            if k in b:
                assert abs(a[k] - b[k]) < 1e-6, (b["id"], k)
