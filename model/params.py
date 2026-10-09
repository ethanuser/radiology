"""Parameter definitions: every uncertain input, its distribution, evidence grade and sources.

Evidence grades
---------------
E  Empirical   -- distribution centred on a published estimate; spread reflects sampling/definition uncertainty.
A  Anchored    -- an empirical anchor exists, but extrapolation or translation to this model needs judgment.
S  Subjective  -- author judgment; deliberately wide. These are the assumptions most worth arguing about.

Correlation structure
---------------------
Inputs are drawn through a structured Gaussian copula with three latent factors:

  z_ai   speed of general AI capability progress (+ = faster)
  z_reg  regulatory / liability / institutional friction   (+ = slower, stricter)
  z_dem  underlying appetite for imaging (payer generosity, defensive medicine, technology push) (+ = more imaging)

Each parameter has loadings rho_f on these factors; its latent normal is
    x = sum_f rho_f * z_f + sqrt(1 - sum_f rho_f^2) * eps
and the parameter value is F^{-1}(Phi(x)) for its marginal distribution F.
This keeps every marginal exactly as stated while inducing the intended
correlations (e.g. faster AI -> earlier capability AND larger new-application demand AND more scanner throughput).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import stats

FACTORS = ("z_ai", "z_reg", "z_dem")


@dataclass
class Param:
    name: str
    group: str
    label: str
    dist: str
    args: dict
    unit: str
    evidence: str
    sources: list = field(default_factory=list)
    note: str = ""
    loadings: dict = field(default_factory=dict)

    # -- marginal inverse CDF ---------------------------------------------------------------------------------
    def ppf(self, u: np.ndarray) -> np.ndarray:
        u = np.clip(u, 1e-9, 1 - 1e-9)
        a = self.args
        d = self.dist
        if d == "normal":
            lo, hi = a.get("lo", -np.inf), a.get("hi", np.inf)
            dist = stats.truncnorm((lo - a["mu"]) / a["sd"], (hi - a["mu"]) / a["sd"], loc=a["mu"], scale=a["sd"])
            return dist.ppf(u)
        if d == "lognormal":
            return a["median"] * np.exp(a["sigma"] * stats.norm.ppf(u))
        if d == "uniform":
            return a["lo"] + (a["hi"] - a["lo"]) * u
        if d == "triangular":
            lo, mode, hi = a["lo"], a["mode"], a["hi"]
            c = (mode - lo) / (hi - lo)
            return stats.triang(c, loc=lo, scale=hi - lo).ppf(u)
        if d == "beta":
            return stats.beta(a["a"], a["b"]).ppf(u)
        if d == "ai_mixture":
            return ai_multiplier(u)
        raise ValueError(d)

    def summary(self) -> str:
        """Human-readable description of the marginal distribution."""
        a, d = self.args, self.dist
        if d == "normal":
            s = f"Normal(μ={a['mu']:g}, σ={a['sd']:g})"
            if "lo" in a or "hi" in a:
                s += f", truncated [{a.get('lo', '-∞')}, {a.get('hi', '∞')}]"
            return s
        if d == "lognormal":
            return f"Lognormal(median={a['median']:g}, σ_log={a['sigma']:g})"
        if d == "uniform":
            return f"Uniform({a['lo']:g}, {a['hi']:g})"
        if d == "triangular":
            return f"Triangular({a['lo']:g}, mode {a['mode']:g}, {a['hi']:g})"
        if d == "beta":
            m = a["a"] / (a["a"] + a["b"])
            return f"Beta({a['a']:g}, {a['b']:g}) [mean {m:.2f}]"
        if d == "ai_mixture":
            return ("Regime mixture: 15% stall (M 1.6-3.0), 55% trend (lognormal, median 1, σ_log 0.25), "
                    "18% fast (M 0.40-0.65), 12% transformative (M 0.25-0.45, task ceilings lifted)")
        return d

    def quantiles(self, qs=(0.1, 0.5, 0.9)) -> list:
        # sorted so P10 <= P50 <= P90 even for decreasing transforms (e.g. AI-speed quantile -> timeline multiplier)
        return sorted(float(self.ppf(np.array([q]))[0]) for q in qs)


# -------------------------------------------------------------------------------------------------------------
# AI timeline multiplier M: multiplies "years from 2026 until a capability arrives".
#   M < 1 compresses AI timelines (fast progress), M > 1 stretches them (stall / plateau).
# Loosely informed by METR time-horizon trends and AI 2027 (fast tail) and by superforecaster scepticism
# in the XPT tournament (slow tail). This is NOT a medical forecast; it only scales capability arrival dates.
# -------------------------------------------------------------------------------------------------------------
# Regime weights (subjective). Quantile u = Phi(z_ai) of the AI-speed factor selects the regime:
#   [0, 0.15) stall | [0.15, 0.70) trend | [0.70, 0.88) fast | [0.88, 1] transformative
REGIME_CUTS = (0.15, 0.70, 0.88)
REGIME_NAMES = ("Stall", "Trend", "Fast", "Transformative")

# In the transformative branch, AI eventually performs nearly all radiologist cognitive work and the
# institutional pipeline compresses under political/economic pressure. These lifts are applied in simulate.py.
TAI_TASK_CEILINGS = {"interp": 0.70, "draft": 0.90, "consult": 0.70, "admin": 0.85, "proc": 0.50}
TAI_AMAX, TAI_FSUB = 0.95, 0.98
TAI_LAG_MULT, TAI_ADOPT_MULT = 0.6, 0.7
TAI_NEW_MULT, TAI_SCOPE_MULT = 1.5, 2.0


def ai_multiplier(u: np.ndarray) -> np.ndarray:
    u = np.asarray(u, dtype=float)
    c1, c2, c3 = REGIME_CUTS
    M = np.empty_like(u)
    stall, trend = u < c1, (u >= c1) & (u < c2)
    fast, tai = (u >= c2) & (u < c3), u >= c3
    M[stall] = 3.0 - (u[stall] / c1) * (3.0 - 1.6)
    v = (u[trend] - c1) / (c2 - c1)
    M[trend] = np.clip(np.exp(-0.25 * stats.norm.ppf(np.clip(v, 1e-6, 1 - 1e-6))), 0.65, 1.6)
    M[fast] = 0.65 - ((u[fast] - c2) / (c3 - c2)) * (0.65 - 0.40)
    M[tai] = 0.45 - ((u[tai] - c3) / (1 - c3)) * (0.45 - 0.25)
    return M


def ai_regime(u: np.ndarray) -> np.ndarray:
    """0 = stall, 1 = trend, 2 = fast, 3 = transformative."""
    c1, c2, c3 = REGIME_CUTS
    u = np.asarray(u)
    return np.select([u < c1, u < c2, u < c3], [0, 1, 2], default=3)


# -------------------------------------------------------------------------------------------------------------
# Parameter table
# -------------------------------------------------------------------------------------------------------------
P = Param  # brevity

PARAMS: list[Param] = [
    # ======================================= 1. BASELINE IMAGING DEMAND (no AI) ===============================
    P("dem_rate", "demand", "Demographic (population + aging) growth of radiologist work, 2026-2045",
      "normal", dict(mu=0.52, sd=0.10, lo=0.15, hi=0.9), "%/yr", "A",
      ["christensen_util", "cbo_2026"],
      "Christensen et al project +16.9% to +26.9% exams by modality 2023-2055 from population growth and aging alone "
      "(≈0.49-0.75%/yr) using Census 2023 projections. CBO's 2026 outlook has slower population growth "
      "(349M→364M, 2026-2056), so the centre is shaded down ≈0.1 pt."),
    P("dem_late", "demand", "Demographic growth in 2066 relative to 2026-2045 rate",
      "uniform", dict(lo=0.4, hi=0.9), "ratio", "A", ["cbo_2026"],
      "CBO projects population growth slowing to zero by 2056; aging continues to add imaging per capita."),
    P("util_g0", "demand", "Per-capita (age/sex-adjusted) utilization growth, 2026",
      "normal", dict(mu=1.2, sd=1.05, lo=-2.0, hi=4.5), "%/yr", "S",
      ["christensen_util", "rula_2026", "smith_bindman_2019", "rosenkrantz_2025", "smith_bindman_2025", "zamani_2026"],
      "National 2018-22 claims (Christensen et al): projected total utilization in 2055 vs 2023 is +16.9% to +26.9% by modality "
      "from population growth and aging alone, and -5.6% to +45.2% if each modality's recent per-person trend continues to 2030 "
      "(radiography and nuclear medicine falling, CT and MRI rising). The Neiman Institute's 2026 update projects +17% (MRI) to "
      "+25% (CT) by 2055. Older health-system data show faster CT growth (3.7-5.2%/yr, 2013-16) and ED CT per Medicare "
      "beneficiary nearly doubled 2013-2023. Each end of the trend range is a single modality (CT up, nuclear medicine down), "
      "so a work-weighted claims-based figure is lower than CT's. Version 1.5 centred per-person growth at 0.6%/yr (σ 0.7). The "
      "history test (model/history.py) needs radiologist work per person to have grown about 2.2%/yr in 2022-2026 (80%: "
      "1.1-2.9) to explain today's shortage, about 1.8%/yr after removing complexity growth. The centre, 1.2%/yr, weights the "
      "two equally by precision; the spread is 1.5 times v1.5's because that width forecast best from past start years "
      "(trained on 1995-2013, also better on 2015-2025). Growth decays toward ~0.2%/yr. The 'imaging restraint' prior set "
      "(near claims-based trends) and 'imaging growth' (the history estimate) bracket it.",
      {"z_dem": 0.7}),
    P("util_ginf", "demand", "Long-run per-capita utilization growth (asymptote)",
      "normal", dict(mu=0.2, sd=0.75, lo=-2.0, hi=3.0), "%/yr", "S", ["smith_bindman_2019", "christensen_util"],
      "Growth in CT/MRI per capita has decelerated each decade since 2000; we assume further deceleration but allow either sign. "
      "Spread 1.5 times v1.5's, as for the current rate.",
      {"z_dem": 0.7}),
    P("util_half", "demand", "Half-life of convergence from current to long-run utilization growth",
      "uniform", dict(lo=6, hi=20), "years", "S"),
    P("cmplx_g0", "demand", "Growth in radiologist work per exam (complexity, images/study), 2026",
      "normal", dict(mu=0.4, sd=0.3, lo=-0.2, hi=1.2), "%/yr", "A", ["mcdonald_2015"],
      "Images per cross-sectional study rose ~10x at Mayo 1999-2010 while exams doubled. Work per exam (RVU-weighted) "
      "grows far more slowly than image counts; we decay this term with a 20-year half-life.",
      {"z_dem": 0.3}),
    P("alt_max", "demand", "Imaging displaced by alternative diagnostics by 2066 (blood tests, AI-ECG, genomics)",
      "triangular", dict(lo=0.0, mode=0.04, hi=0.15), "share", "S"),
    P("alt_mid", "demand", "Midpoint year of alternative-diagnostic substitution",
      "uniform", dict(lo=2035, hi=2055), "year", "S"),
    P("ratio0", "demand", "Supply ÷ demand for radiologist FTEs in 2026 (current shortage)",
      "triangular", dict(lo=0.88, mode=0.945, hi=0.99), "ratio", "S",
      ["rula_2026", "zamani_2026", "parikh_2026", "doximity_2026", "nrmp_2026", "dibble_2025"],
      "No measured national figure exists; this is a judgment from indirect signals. HRSA projects radiology at ≈90% adequacy "
      "in 2038 (a projection, not today's gap), and the Neiman Institute calls the shortage 'fairly static'. Compensation rose "
      "6.6% in a year and DR positions keep expanding. Average exams read per radiologist-day were flat 2018-2024 (+0.6%) but the busiest quartile read 31% "
      "more, and practice turnover rose from 5.3% to 8.5% (2013-2022): a real but uneven, moderate shortage. The history "
      "reconstruction (model/history.py), which fits the documented job market since 1995, puts 2026 at 0.95 (80%: 0.92-0.98); "
      "v1.5's judgment was Triangular(0.85, 0.93, 0.99). This prior combines the two."),

    # ======================================= 2. AI CAPABILITY & ASSISTIVE PRODUCTIVITY =========================
    P("ai_u", "ai_capability", "AI progress speed (quantile → timeline multiplier M)",
      "ai_mixture", {}, "multiplier", "S", ["metr_2025", "metr_2026", "ai2027", "grace_2025", "leap_2025", "karger_2023"],
      "Loose guidance only; M multiplies the years from 2026 until each capability arrives. AI researchers put 50% odds on "
      "machines outperforming humans at every task by 2047 but on full automation of occupations only by 2116; expert "
      "panels put far lower odds on near-term transformative AI than lab leaders. Fast + transformative = 30% of worlds.",
      {"z_ai": 1.0}),
    P("cap_draft_T0", "ai_capability", "Midpoint year: reliable draft reports & automated measurements (M=1)",
      "normal", dict(mu=2028.0, sd=1.5), "year", "A", ["huang_2025", "hong_2025", "tanno_2025", "aidoc_2026", "langlotz_2025"],
      "Generative draft reporting gave +15.5% documentation efficiency on 24k radiographs in live use; AI-drafted chest "
      "radiograph reports cut reading time 42% in a reader study; generative chest-radiograph drafting tools received FDA "
      "Breakthrough designations in 2026."),
    P("cap_admin_T0", "ai_capability", "Midpoint year: protocoling, scheduling, QA and admin automation (M=1)",
      "normal", dict(mu=2030.5, sd=2.0), "year", "A", ["langlotz_2025"]),
    P("cap_interp_T0", "ai_capability", "Midpoint year: AI assistance that materially speeds interpretation (M=1)",
      "normal", dict(mu=2033, sd=3.0), "year", "A", ["wenderott_2024", "yu_2024", "agarwal_2023", "rajpurkar_2023"],
      "Real-world meta-analysis finds no significant time savings yet; effects of AI assistance vary widely across "
      "radiologists and erroneous AI output hurts performance; radiologists under-weight AI predictions."),
    P("cap_consult_T0", "ai_capability", "Midpoint year: AI support for clinical synthesis/communication (M=1)",
      "normal", dict(mu=2034, sd=3.0), "year", "S", ["langlotz_2025"]),
    P("cap_proc_T0", "ai_capability", "Midpoint year: meaningful automation of procedural/physical work (M=1)",
      "normal", dict(mu=2050, sd=8.0), "year", "S"),
    P("cap_width", "ai_capability", "Capability S-curve width (logistic scale; 10→90% ≈ 4.4×)",
      "uniform", dict(lo=2.0, hi=4.0), "years", "S"),
    P("m_interp", "ai_tasks", "Max time saved on interpretation by assistive AI (radiologist still reads)",
      "beta", dict(a=6, b=14), "share", "A", ["langlotz_2025", "yu_2024", "hong_2025"],
      "Langlotz's task analysis and reader studies of AI assistance. (European screening workload cuts of 33-44% come from "
      "replacing the second reader in double reading, a substitution effect that does not transfer to single-read U.S. "
      "practice, so they are not used here.)", {"z_ai": 0.4}),
    P("m_draft", "ai_tasks", "Max time saved on measurement & report drafting",
      "beta", dict(a=12, b=8), "share", "A", ["huang_2025", "hong_2025", "li_2026", "liu_2026", "langlotz_2025"],
      "Measured savings span 0% to 42% of reading time: +15.5% (live radiographs), −42% (chest-radiograph reader study), "
      "−0.46 min per impression (multicentre LLM study), and no sustained gain at one of two CT sites. If drafting and "
      "measurement are ~30% of reading time, current tools already capture roughly half of this sub-task.", {"z_ai": 0.4}),
    P("m_consult", "ai_tasks", "Max time saved on clinical synthesis/consultation/communication",
      "beta", dict(a=5, b=15), "share", "A", ["langlotz_2025"],
      "Langlotz: record summarization −30% tech/provider communication; non-routine communication −30%; patient explanation −30%.",
      {"z_ai": 0.4}),
    P("m_admin", "ai_tasks", "Max time saved on administrative work (protocoling, QA, scheduling)",
      "beta", dict(a=8, b=12), "share", "A", ["langlotz_2025"],
      "Langlotz: automated protocoling −60% (30-70%).", {"z_ai": 0.4}),
    P("m_proc", "ai_tasks", "Max time saved on physical/procedural work",
      "beta", dict(a=1.5, b=17), "share", "S", [], "", {"z_ai": 0.4}),
    P("adopt_mid", "ai_tasks", "Midpoint year of effective clinical adoption of assistive AI",
      "normal", dict(mu=2029.5, sd=2.0, lo=2027, hi=2040), "year", "A",
      ["wu_2024", "allen_2021", "rcr_2026", "fda_ai_2026", "lehman_2015"],
      "≈1,100 radiology AI devices cleared by 2025 but claims-based use was concentrated in a handful of products; 33.5% "
      "of US radiologists reported using any AI in 2020, and 75% of UK departments used AI clinically in 2025 without "
      "an overall workload reduction. Precedent: mammography CAD reached most US screening exams within ~6 years of payment.",
      {"z_reg": 0.4, "z_ai": -0.3}),
    P("adopt_pressure", "ai_tasks", "Shortage acceleration of AI adoption (extra adoption-clock speed per unit ln(D/S))",
      "uniform", dict(lo=0.0, hi=4.0), "multiplier", "S", ["rula_2026", "rcr_2026"],
      "Practices adopt labour-saving AI faster when radiologists are scarce. At a 7% shortage and the midpoint value (2), "
      "assistive and autonomous adoption clocks run ~14% faster. Applied only while demand exceeds supply."),
    P("adopt_width", "ai_tasks", "Assistive adoption S-curve width", "uniform", dict(lo=1.5, hi=3.5), "years", "S"),
    P("adopt_max", "ai_tasks", "Saturation share of work done with assistive AI", "beta", dict(a=18, b=2), "share", "S"),
    P("ovh_max", "ai_tasks", "New oversight work created by AI (governance, auditing, validation), share of time",
      "uniform", dict(lo=0.02, hi=0.08), "share", "S", ["langlotz_2025", "humlum_2025", "acemoglu_restrepo_2019"],
      "Langlotz does not model AI monitoring/oversight time. In Danish administrative data, chatbot adoption created new "
      "integration and oversight tasks that offset most of a ~3% time saving."),

    # ======================================= 3. AUTONOMY & THE REGULATORY PIPELINE =============================
    P("w1", "autonomy", "Tier 1 share of interpretive work: normal/negative radiographs & screening exams",
      "triangular", dict(lo=0.04, mode=0.07, hi=0.12), "share", "A",
      ["plesner_2023", "plesner_2024", "lauritzen_2024", "gommers_2026", "oxipit_2022"],
      "AI could autonomously report 7.8% of all posteroanterior chest radiographs at >99% sensitivity (2023) and ~17.5% at "
      "99% sensitivity with a tuned threshold (2024); AI triage let about two-thirds of Danish screening mammograms be single-read (33.5% fewer reads), "
      "though that saving comes from European double reading and U.S. screening is single-read. "
      "Radiographs and screening mammography are ~20-25% of radiologist work, so tier 1 is ≈4-12% of interpretive work."),
    P("w2", "autonomy", "Tier 2 share: all radiographs, screening mammography, standardized follow-ups",
      "triangular", dict(lo=0.10, mode=0.17, hi=0.25), "share", "A", ["langlotz_2025"],
      "Langlotz delegation assumptions: mammography 50%, radiography 40%, other modalities 3%."),
    P("w3", "autonomy", "Tier 3 share: complex diagnostic CT/MR/US/NM",
      "triangular", dict(lo=0.35, mode=0.47, hi=0.57), "share", "S", [], "", {"z_ai": 0.2}),
    P("tcap1_T0", "autonomy", "Tier 1 technical capability year (not AI-speed scaled)",
      "normal", dict(mu=2025, sd=1.0), "year", "A", ["oxipit_2022"],
      "An autonomous normal-chest-radiograph product received EU CE Class IIb marking in 2022."),
    P("tcap2_T0", "autonomy", "Tier 2 technical capability year (M=1)", "normal", dict(mu=2031, sd=3.0), "year", "S"),
    P("tcap3_T0", "autonomy", "Tier 3 technical capability year (M=1)", "normal", dict(mu=2040, sd=5.0), "year", "S"),
    P("tcap4_T0", "autonomy", "Tier 4 (residual hardest work) capability year (M=1)", "normal", dict(mu=2052, sd=8.0), "year", "S"),
    P("lval", "regulation", "Clinical-validation lag (prospective, multi-site) after capability; tier-1 median",
      "lognormal", dict(median=2.5, sigma=0.4), "years", "A", ["gommers_2026", "lang_2023", "chouffani_2024"],
      "MASAI randomised from April 2021; its interval-cancer endpoint was published in January 2026 (~5 years). 43% of "
      "FDA-authorised AI devices had no published clinical validation and only 4% had randomised trials. "
      "Tiers 2-4 multiply by 1.2/1.5/1.8.",
      {"z_reg": 0.3, "z_ai": -0.3}),
    P("lfda", "regulation", "FDA authorization lag for autonomous claims; tier-2 median",
      "lognormal", dict(median=2.0, sigma=0.5), "years", "A",
      ["fda_ai_2026", "fda_draft_2025", "aidoc_2026", "deephealth_2026", "abramoff_2018"],
      "As of October 2026 no autonomous radiology read is FDA-authorized; generative report drafting has reached FDA "
      "Breakthrough designation (2026) and one 510(k) report-generating tool keeps the radiologist in control; FDA's AI "
      "lifecycle guidance remains a draft. IDx-DR (2018) is the main autonomous precedent. Tier multipliers 0.75/1.0/1.5/2.0.",
      {"z_reg": 0.7, "z_ai": -0.3}),
    P("lpay", "regulation", "Liability + reimbursement + scope-of-practice acceptance lag; tier-2 median",
      "lognormal", dict(median=4.0, sigma=0.6), "years", "A", ["abramoff_2018", "bernstein_2025", "mello_2024", "cms_pfs_2026"],
      "Autonomous retinal AI: FDA 2018 → Category I CPT 92229 in 2021. Mock jurors penalize radiologists who disagree with AI. "
      "Medicare professional-component billing presumes physician interpretation. Tier multipliers 0.75/1.0/1.4/1.8.",
      {"z_reg": 0.7, "z_ai": -0.3}),
    P("ahalf", "regulation", "Hospital adoption: years from 'ready' to half of eventual uptake",
      "lognormal", dict(median=5.5, sigma=0.35), "years", "A", ["adler_milstein_2017", "lehman_2015", "wu_2024"],
      "Hospital EHR adoption passed 50% about four years after the 2009 HITECH subsidies; reimbursed mammography CAD diffused within ≈4-6 years.",
      {"z_reg": 0.4, "z_ai": -0.2}),
    P("awidth", "regulation", "Autonomy adoption S-curve width", "uniform", dict(lo=1.5, hi=3.5), "years", "S"),
    P("amax1", "regulation", "Eventual uptake of tier-1 autonomy (share of eligible work)", "beta", dict(a=17, b=3), "share", "S",
      [], "", {"z_reg": -0.4, "z_ai": 0.3}),
    P("amax2", "regulation", "Eventual uptake of tier-2 autonomy", "beta", dict(a=14, b=6), "share", "S", [], "",
      {"z_reg": -0.4, "z_ai": 0.3}),
    P("amax3", "regulation", "Eventual uptake of tier-3 autonomy", "beta", dict(a=11, b=9), "share", "S", [], "",
      {"z_reg": -0.4, "z_ai": 0.3}),
    P("amax4", "regulation", "Eventual uptake of tier-4 autonomy", "beta", dict(a=8, b=12), "share", "S", [], "",
      {"z_reg": -0.4, "z_ai": 0.3}),
    P("f_sub", "regulation", "Share of interpretation+drafting time actually removed per AI-first/autonomous study",
      "uniform", dict(lo=0.60, hi=0.95), "share", "S", ["agarwal_2023", "tanno_2025"],
      "Residual human time: sampling QA, sign-off, escalations, liability review. Clinically significant errors still "
      "appeared in 22.8% of AI-only versus 14.0% of human-only chest-radiograph reports in a 2025 evaluation.", {"z_ai": 0.3}),

    # ======================================= 4. JEVONS / REBOUND ================================================
    P("pc_share", "jevons", "Professional (interpretation) share of the all-in price of an imaging exam",
      "triangular", dict(lo=0.10, mode=0.20, hi=0.30), "share", "A", ["pc_share"],
      "≈20% for MRI, ≈25% for radiography of Medicare global fees; lower where hospital facility fees apply."),
    P("pass_through", "jevons", "Share of cost savings passed through to prices paid",
      "beta", dict(a=4, b=6), "share", "S", [],
      "Fee schedules are administered and revalued slowly; commercial prices are sticky."),
    P("elasticity", "jevons", "Price elasticity of imaging demand",
      "triangular", dict(lo=-0.6, mode=-0.2, hi=-0.05), "elasticity", "A",
      ["manning_1987", "aron_dine_2013", "brot_goldberg_2017"],
      "RAND HIE ≈ −0.2 for medical care, with respect to the patient's out-of-pocket price; professional-fee cuts mostly "
      "fall on payers, so this channel is if anything overstated. Deductible shocks cut imaging alongside other services."),
    P("access", "jevons", "Turnaround/availability rebound: extra work per unit of radiologist time freed",
      "triangular", dict(lo=0.0, mode=0.10, hi=0.30), "ratio", "A", ["larson_2011"],
      "Non-price rationing: when reads become fast and available 24/7, clinicians order more (ED CT visits rose from 2.8% to 13.9%, "
      "1995-2007). Applied to the share of radiologist time saved."),
    P("new_max", "jevons", "New AI-enabled imaging applications by 2066 (share of baseline work, before capacity limits)",
      "lognormal", dict(median=0.18, sigma=0.7), "share", "S",
      ["kwee_2025", "bandi_2024", "lee_2026", "cms_pfs_2026", "hernstrom_2025"],
      "Of 2024 imaging studies with direct patient-care impact, 49% would increase radiologist workload and <1% would "
      "decrease it; AI studies were about 14 times higher odds of adding work (odds ratio 14.3). Examples: opportunistic CT screening, lung screening "
      "(18% uptake in 2022), AI coronary plaque analysis (Category I CPT 75577 from 2026).",
      {"z_ai": 0.5, "z_dem": 0.3}),
    P("new_T0", "jevons", "Midpoint year of new-application uptake (M=1)", "normal", dict(mu=2038, sd=4.0), "year", "S"),
    P("new_width", "jevons", "New-application S-curve width", "uniform", dict(lo=3, hi=6), "years", "S"),
    P("lambda_new", "jevons", "Radiologist labour intensity of new-application work vs a typical exam",
      "uniform", dict(lo=0.4, hi=1.0), "ratio", "S"),
    P("iota", "jevons", "Extra follow-up work from AI-detected (incidental) findings at full deployment",
      "triangular", dict(lo=0.0, mode=0.03, hi=0.08), "share", "A", ["hernstrom_2025", "eisemann_2025"],
      "AI-supported screening raised cancer detection 17.6-29% with flat recall; more findings mean more follow-up."),
    P("latent", "jevons", "Latent demand currently rationed by scanner/technologist capacity",
      "triangular", dict(lo=0.02, mode=0.06, hi=0.12), "share", "A", ["asrt_2025"],
      "CT technologist vacancy 19.4% and MRI 17.4% in 2025."),
    P("thru_H", "jevons", "AI-driven acquisition throughput gain at maturity (faster scans, auto-positioning)",
      "lognormal", dict(median=0.30, sigma=0.45), "share", "A", ["johnson_2023"],
      "Deep-learning reconstruction cut knee MRI time ≈44% prospectively; CT is already fast and table time dominates.",
      {"z_ai": 0.5}),
    P("thru_T0", "jevons", "Midpoint year of throughput gains (M=1)", "normal", dict(mu=2032, sd=3.0), "year", "A", ["johnson_2023"]),
    P("cap_invest", "jevons", "Long-run extra scanner/technologist capacity built in response to demand (by 2066)",
      "uniform", dict(lo=0.0, hi=0.25), "share", "S", ["baker_2010"]),
    P("um_max", "jevons", "AI-enabled utilization management (order decision support, payer AI prior auth)",
      "triangular", dict(lo=0.0, mode=0.03, hi=0.08), "share", "A", ["langlotz_2025", "trustees_2026"],
      "Langlotz: order-entry decision support −3% (0-6%) of advanced imaging; Medicare HI trust fund depletion projected 2033.",
      {"z_dem": -0.4}),
    P("scope_max", "jevons", "Reads shifting to non-radiologists with AI support by 2066",
      "triangular", dict(lo=0.0, mode=0.03, hi=0.10), "share", "S"),
    P("nt_max", "jevons", "New radiologist tasks created alongside AI (reinstatement), share of 2026 FTE",
      "triangular", dict(lo=0.0, mode=0.04, hi=0.12), "share", "S", ["acemoglu_restrepo_2019", "autor_2024", "kwee_2025"],
      "e.g. AI governance roles, theranostics, quantitative-imaging consults, multidisciplinary precision-medicine work.",
      {"z_ai": 0.3}),

    # ======================================= 5. RADIOLOGIST SUPPLY =============================================
    P("attr_mult", "supply", "Attrition hazard multiplier (post-COVID ≈ high end)",
      "uniform", dict(lo=0.95, hi=1.25), "multiplier", "A", ["christensen_supply", "rula_2026", "parikh_2026"],
      "Measured attrition rose from 1.1%/yr (2014) to 2.0% (2019) and 2.5% (2022). With flat residency positions, multipliers of "
      "1.0 and 1.2 reproduce the published supply projections under blended 2014-23 attrition (+25.7% by 2055) and post-COVID "
      "attrition (+20.9%); the range is centred between them, nearer the post-COVID case the Neiman 2026 update emphasises. "
      "Turnover between practices also roughly doubled (adjusted odds 1.96, 2022 vs 2013)."),
    P("slot_g", "supply", "Trend growth in DR residency positions (before market response)",
      "normal", dict(mu=1.5, sd=0.8, lo=-1.0, hi=3.5), "%/yr", "A", ["malhotra_2026", "nrmp_2026", "christensen_supply"],
      "DR positions rose 33% from 2010 to 2025 (about 1.9%/yr) and from 1,132 (2022) to 1,241 (2026), about 2.3%/yr. We centre "
      "slightly lower (1.5%/yr) because Medicare GME caps bind and PGY-1 applicants fell 14% over 2023-2026; the "
      "'residency growth continues' prior set uses 1.9%/yr."),
    P("resid_gamma", "supply", "Residency-position response to market signal (elasticity to ln D/S)",
      "uniform", dict(lo=0.3, hi=1.5), "elasticity", "A", ["sharafinski_2016", "rosenkrantz_2016", "nicholson_2002"],
      "After the mid-1990s downturn, radiology trainee numbers fell to a 1997 nadir (3,080) and then rose 84% by 2011; "
      "medical-student interest tracks the job market."),
    P("fill_kappa", "supply", "Fill-rate response to oversupply (applicant flight)",
      "uniform", dict(lo=0.3, hi=1.5), "elasticity", "A", ["sharafinski_2016", "shi_2015"],
      "2015 Match, during the last oversupply: 86% of advanced DR positions filled, 55 of 166 programs went unfilled, and "
      "U.S. graduates took 67% of matched positions."),
    P("resid_lag", "supply", "Information/perception lag before the pipeline reacts", "uniform", dict(lo=1, hi=3), "years", "A",
      ["sharafinski_2016"]),
    P("fear", "supply", "Applicant deterrence from visible AI progress (max fill-rate loss)",
      "uniform", dict(lo=0.0, hi=0.08), "share", "A", ["nrmp_2026", "reeder_2022"],
      "DR PGY-1 applicants fell 14% over 2023-2026 even as positions hit records and still filled 97.6%. In a 32-school "
      "survey, radiology's first-choice share fell from 21.4% to 17.7% when students considered AI."),
    P("fte_drift", "supply", "Drift in FTE per radiologist (part-time, generational preferences)",
      "normal", dict(mu=-0.10, sd=0.15), "%/yr", "S"),

    # ======================================= 6. MARKET ADJUSTMENT ==============================================
    P("adj_speed", "market", "Market adjustment speed: share of the remaining shortage or surplus closed each year",
      "uniform", dict(lo=0.2, hi=0.55), "per year", "A", ["sunshine_2007", "levin_2011", "bhargavan_2009"],
      "Fitted in the history test on the documented job market of 1995-2013 (80% range 0.19-0.55); with it, the held-out "
      "2015-2025 episodes are predicted far better than without. The radiology job market has repeatedly self-corrected "
      "within a few years, faster than the training pipeline allows: work moved to non-radiologists while radiologists were "
      "scarce (their imaging grew twice as fast in 1998-2005), and radiologists' output per FTE rose 70% in 1992-2007 as PACS "
      "and teleradiology spread. The reverse flows during surpluses are assumed, not observed directly."),
    P("adj_max", "market", "Largest cumulative market adjustment (share of radiologist work that can shift)",
      "uniform", dict(lo=0.08, hi=0.28), "share", "S", ["levin_2011"],
      "The history test (1995-2013) rules out a weak adjustment (limits below about 0.08-0.10 get little weight) but cannot bound "
      "it from above, because past imbalances never exceeded about 10-15%; the upper end, 0.28, is a judgment. Beyond the limit, imbalances are not absorbed: "
      "AI-driven changes larger than the historical swings still show up as shortage or surplus."),
]

PARAM_INDEX = {p.name: p for p in PARAMS}

# Task-share Dirichlet (share of radiologist working time, 2026, before AI)
TASKS = ("interp", "draft", "consult", "admin", "proc")
TASK_LABELS = {
    "interp": "Interpretation / reporting",
    "draft": "Measurement & report drafting",
    "consult": "Clinical synthesis & consultation",
    "admin": "Administrative (protocoling, QA)",
    "proc": "Physical / procedural",
    "oversight": "AI oversight (new task)",
}
TASK_MEANS = np.array([0.42, 0.18, 0.13, 0.15, 0.12])
TASK_CONC = 80.0
TASK_SOURCES = ["langlotz_2025", "dhanoa_2013"]
TASK_NOTE = ("Langlotz's synthesis: perform/interpret 66.7%, protocoling 5.5%, communication 11.8%, other 6.8%, personal 9.1%. "
             "Dhanoa's time-motion study: 36.4% pure interpretation, 43.8% non-interpretive. We renormalize to working time and split "
             "'perform/interpret' into interpretation, drafting/measurement and procedures.")

# Tier multipliers on regulatory lags
TIER_VAL_MULT = np.array([1.0, 1.2, 1.5, 1.8])
TIER_FDA_MULT = np.array([0.75, 1.0, 1.5, 2.0])
TIER_PAY_MULT = np.array([0.75, 1.0, 1.4, 1.8])


def evidence_counts() -> dict:
    out = {"E": 0, "A": 0, "S": 0}
    for p in PARAMS:
        out[p.evidence] += 1
    return out

# Short display names (charts and tables)
SHORT = {
    "dem_rate": "Demographic growth", "dem_late": "Late demographic slowdown", "util_g0": "Per-capita imaging growth (now)",
    "util_ginf": "Per-capita imaging growth (long run)", "util_half": "Utilization convergence speed",
    "cmplx_g0": "Work-per-exam growth", "alt_max": "Alternative diagnostics", "alt_mid": "Alt. diagnostics timing",
    "ratio0": "Today's shortage (2026 S/D)", "ai_u": "AI progress speed / regime", "cap_draft_T0": "Drafting-AI arrival",
    "cap_admin_T0": "Admin-AI arrival", "cap_interp_T0": "Interpretation-assist arrival",
    "cap_consult_T0": "Consultation-AI arrival", "cap_proc_T0": "Procedural automation arrival",
    "cap_width": "Capability S-curve width", "m_interp": "Ceiling: interpretation savings",
    "m_draft": "Ceiling: drafting savings", "m_consult": "Ceiling: consultation savings", "m_admin": "Ceiling: admin savings",
    "m_proc": "Ceiling: procedural savings", "adopt_mid": "Assistive-AI adoption timing", "adopt_width": "Adoption S-curve width",
    "adopt_max": "Assistive adoption ceiling", "ovh_max": "AI oversight burden", "w1": "Tier-1 work share",
    "w2": "Tier-2 work share", "w3": "Tier-3 work share", "tcap1_T0": "Tier-1 capability year",
    "tcap2_T0": "Tier-2 capability year", "tcap3_T0": "Tier-3 capability year", "tcap4_T0": "Tier-4 capability year",
    "lval": "Clinical-validation lag", "lfda": "FDA authorization lag", "lpay": "Liability & payment lag",
    "ahalf": "Hospital adoption half-time", "awidth": "Autonomy adoption width", "amax1": "Tier-1 eventual uptake",
    "amax2": "Tier-2 eventual uptake", "amax3": "Tier-3 eventual uptake", "amax4": "Tier-4 eventual uptake",
    "f_sub": "Labor removed per AI-first read", "pc_share": "Professional share of price", "pass_through": "Cost pass-through",
    "elasticity": "Price elasticity of imaging", "access": "Turnaround/availability rebound",
    "new_max": "New AI-enabled applications", "new_T0": "New-application timing", "new_width": "New-application ramp",
    "lambda_new": "Radiologist intensity of new work", "adopt_pressure": "Shortage-driven AI adoption", "iota": "Incidental-finding follow-up",
    "latent": "Latent (rationed) demand", "thru_H": "Scanner throughput gain", "thru_T0": "Throughput timing",
    "cap_invest": "Capacity investment", "um_max": "AI utilization management", "scope_max": "Scope shift to non-radiologists",
    "nt_max": "New radiologist tasks", "attr_mult": "Attrition rate", "slot_g": "Residency slot growth",
    "resid_gamma": "Residency responsiveness", "fill_kappa": "Applicant flight if oversupplied",
    "resid_lag": "Pipeline reaction lag", "fear": "AI deterrence of applicants", "fte_drift": "FTE-per-radiologist drift",
    "adj_speed": "Market adjustment speed", "adj_max": "Market adjustment limit",
    "s_interp": "Task share: interpretation", "s_draft": "Task share: drafting", "s_consult": "Task share: consultation",
    "s_admin": "Task share: administration", "s_proc": "Task share: procedures",
}
