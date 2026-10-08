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
    # D = B - L + I  (labour saved and induced demand reconcile exactly)
    assert np.allclose(o["D"], o["B"] - o["L"] + o["I"], atol=1e-9)
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


def test_prior_reweighting_main_is_identity():
    from model import analysis, robustness
    s, o = analysis.run(3000, seed=9)
    pri = robustness.prior_sets(s, o)
    p = (o["R"][:, 2045 - 2026] > 1.10).mean()
    assert abs(pri["main"]["2045"]["p_over"] - p) < 0.01  # main weights ≈ sampled regime frequencies
    assert pri["ai_bullish"]["2045"]["p_over"] > pri["ai_skeptic"]["2045"]["p_over"]
