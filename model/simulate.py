"""Core simulation: annual steps 2026-2066 (supply cohorts start in 2023 for calibration).

Notation (all demand quantities are indices with 2026 = 1):
  B(t)    baseline radiologist workload with AI frozen at its 2026 level
  W(t)    imaging work including AI-induced (rebound / Jevons) demand
  tau(t)  radiologist time per unit of work relative to a no-AI world (1.0 = no AI)
  D(t)    radiologist FTE demand = W·tau/tau0 + new non-reading tasks
  S(t)    radiologist FTE supply index
  R(t)    supply ÷ demand in absolute FTE (R(2026) = ratio0 < 1, i.e. today's shortage)
"""
from __future__ import annotations

import numpy as np

from .params import (TAI_ADOPT_MULT, TAI_AMAX, TAI_FSUB, TAI_LAG_MULT, TAI_NEW_MULT, TAI_SCOPE_MULT,
                     TAI_TASK_CEILINGS, TIER_FDA_MULT, TIER_PAY_MULT, TIER_VAL_MULT, ai_regime)

YEARS = np.arange(2026, 2067)
T = len(YEARS)
REPORT_YEARS = (2030, 2035, 2045, 2055, 2066)

# ----------------------------------------------------------------------------------------------- supply constants
SUPPLY_START = 2023
STOCK_2023 = 37_482  # Medicare-enrolled radiologists, Christensen et al (supply)
CAREER_MAX = 55  # years-of-practice bins
H0, H_RET, Y50, H_S = 0.004, 0.30, 36.0, 3.0  # attrition hazard by years in practice (calibrated below)
CHRISTENSEN_FLAT_2055 = 1.257  # +25.7% 2023->2055 if residency positions stop growing after 2024
POSITIONS_2026 = 1_241  # DR positions offered, 2026 Match
FILL_2026 = 0.976
GME_CAP = 1.8  # positions cannot exceed 1.8x 2026 level (GME funding constraint)
TRAINING_LAG = 6  # match year -> independent practice (PGY1 + 4 DR + ~1 fellowship)

# Approximate filled DR positions by match year (NRMP; 2022-2026 anchored on reported totals).
FILLED_HIST = {
    2017: 1060, 2018: 1075, 2019: 1090, 2020: 1105, 2021: 1115, 2022: 1120,
    2023: 1135, 2024: 1150, 2025: 1190, 2026: round(POSITIONS_2026 * FILL_2026),
}


def logistic(t, mid, width):
    return 1.0 / (1.0 + np.exp(-(t - mid) / width))


def base_hazard() -> np.ndarray:
    y = np.arange(CAREER_MAX)
    h = H0 + H_RET / (1 + np.exp(-(y - Y50) / H_S))
    h[-1] = 1.0
    return np.clip(h, 0, 1)


def _historical_entrants(year: int) -> float:
    # Shape of historical entry into practice (1990s residency cuts, 2000s expansion), scaled to the 2023 stock.
    if year <= 1995:
        return 950.0
    if year <= 2000:
        return 950.0 + (year - 1995) * 10
    if year <= 2003:
        return 830.0
    if year <= 2012:
        return 830.0 + (year - 2003) * (1150 - 830) / 9
    return 1150.0 + (year - 2012) * 5


def initial_cohorts() -> np.ndarray:
    h = base_hazard()
    surv = np.cumprod(np.r_[1.0, 1 - h[:-1]])
    coh = np.array([_historical_entrants(SUPPLY_START - k) * surv[k] for k in range(CAREER_MAX)])
    return coh * STOCK_2023 / coh.sum()


def _calibrate_kappa() -> float:
    """Entrants per filled position so that flat positions reproduce Christensen's +25.7% by 2055."""
    h = base_hazard()
    coh0 = initial_cohorts()

    def proj(e_flat):
        c = coh0.copy()
        for _ in range(SUPPLY_START + 1, 2056):
            c = np.r_[e_flat, (c - c * h)[:-1]]
        return c.sum() / STOCK_2023

    lo, hi = 500.0, 3000.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if proj(mid) < CHRISTENSEN_FLAT_2055 else (lo, mid)
    return lo / FILLED_HIST[2024]


KAPPA = _calibrate_kappa()
HAZARD = base_hazard()
COHORT_2023 = initial_cohorts()


# ----------------------------------------------------------------------------------------------- main simulation
STRUCTURES = {
    "base": "Main model",
    "no_signoff": "No audit or sign-off time at all on AI-first reads",
    "unordered": "Complex exams may be automated before simple ones",
    "open_demand": "3× as many new AI-enabled imaging uses and 2× the new radiologist tasks",
    "payer_pushback": "Payers' AI blocks twice as many scans; twice as many reads shift to other doctors",
    "uncapped_new_uses": "New uses such as screening existing scans are not limited by scanner capacity",
    "tai_gated": "Transformative AI's extra time savings must also wait for regulation and adoption",
    "no_adjustment": "Market adjustment removed (v1.5's design) but v1.6's other inputs kept; those were calibrated with the adjustment on",
    "shortage_only": "The market absorbs shortages as fitted but not surpluses: work does not flow back to radiologists",
    "adj_cap15": "Adjustment limit capped at 15% of demand, the largest gap seen in 1995-2026",
    "adj_wide": "Adjustment speed and limit drawn from the wider fit (limit up to 50% of demand)",
    # counterfactuals (not alternatives): how much of the risk comes from AI at all
    "assistive_only": "AI helps radiologists read but never reads first",
    "no_ai": "Radiology AI frozen at its 2026 level (other diagnostics such as AI-ECG still displace some imaging)",
}
COUNTERFACTUALS = ("assistive_only", "no_ai")


def consistent_with_today(o: dict) -> np.ndarray:
    """Futures already contradicted by events: an autonomous radiology read FDA-authorized before October 2026."""
    return o["stages"][:, :, 2].min(axis=1) >= 2026.8


def subset(d: dict, mask: np.ndarray) -> dict:
    """Keep the futures in `mask` in every per-future array of a sample or output dict."""
    n = len(mask)
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out[k] = subset(v, mask)
        elif isinstance(v, np.ndarray) and v.ndim >= 1 and v.shape[0] == n:
            out[k] = v[mask]
        else:
            out[k] = v
    return out


def simulate(s: dict, structure: str = "base") -> dict:
    """Two-pass solve. Pass 1 runs with AI adoption on calendar time and yields the shortage path ln(D/S).
    Pass 2 re-runs with adoption clocks that run faster while demand exceeds supply (practices adopt
    labour-saving AI faster when radiologists are scarce): one fixed-point iteration of the coupled system."""
    n = len(s["dem_rate"])
    first = _simulate_once(s, np.zeros((n, T)), structure)
    pressure = np.maximum(0.0, np.log(first["D_abs"] / first["S_fte"]))
    press_cum = np.zeros_like(pressure)
    press_cum[:, 1:] = np.cumsum(pressure[:, :-1], axis=1)  # lagged one year
    out = _simulate_once(s, press_cum, structure)
    out["pressure_pass1"] = pressure
    out["Sd"] = out["R"] * out["D"]  # supply in units of 2026 demand: lines cross where supply = demand
    return out


def _simulate_once(s: dict, press_cum: np.ndarray, structure: str = "base") -> dict:
    """`structure` switches between the main model and the alternative structures in STRUCTURES."""
    assert structure in STRUCTURES, structure
    n = len(s["dem_rate"])
    t = YEARS[None, :].astype(float)
    dt = t - 2026.0
    col = lambda k: np.asarray(s[k], dtype=float)[:, None]  # noqa: E731
    M = col("ai_u")
    sqM = np.sqrt(M)
    regime = ai_regime(np.asarray(s["ai_u_raw"]))
    tai = (regime == 3).astype(float)[:, None]  # transformative-AI branch indicator

    def lift(x, ceiling):
        """In the transformative branch, raise a ceiling parameter toward `ceiling` (never lower it)."""
        return x + tai * np.maximum(0.0, ceiling - x)

    def scaled(T0):
        # only future capability dates are compressed or stretched by the AI-speed multiplier
        d = col(T0) - 2026.0
        return 2026.0 + np.maximum(d, 0.0) * M + np.minimum(d, 0.0)

    out: dict[str, np.ndarray] = {}

    # ===================================================================== 1. baseline demand (AI frozen at 2026)
    late = np.where(t <= 2045, 1.0, 1.0 + (col("dem_late") - 1.0) * (t - 2045) / (2066 - 2045))
    r_dem = col("dem_rate") / 100 * late
    r_util = (col("util_ginf") + (col("util_g0") - col("util_ginf")) * 2 ** (-dt / col("util_half"))) / 100
    r_cmplx = col("cmplx_g0") / 100 * 2 ** (-dt / 20.0)

    def cum(r):
        g = 1 + r
        g[:, 0] = 1.0
        return np.cumprod(g, axis=1)

    B_dem, B_util, B_cmplx = cum(r_dem), cum(r_util), cum(r_cmplx)
    alt = col("alt_max") * logistic(t, col("alt_mid"), 4.0)
    B_alt = (1 - alt) / (1 - alt[:, :1])
    B = B_dem * B_util * B_cmplx * B_alt
    out.update(B=B, B_dem=B_dem, B_util=B_util, B_cmplx=B_cmplx, B_alt=B_alt)

    # ===================================================================== 2. AI productivity (task-based)
    cw = col("cap_width") * sqM
    cap = {
        "interp": logistic(t, scaled("cap_interp_T0"), cw),
        "draft": logistic(t, scaled("cap_draft_T0"), cw),
        "consult": logistic(t, scaled("cap_consult_T0"), cw),
        "admin": logistic(t, scaled("cap_admin_T0"), cw),
        # robotics lags software: procedural capability never compresses faster than M = 0.6
        "proc": logistic(t, 2026.0 + (col("cap_proc_T0") - 2026.0) * np.maximum(M, 0.6), cw),
    }
    kappa_a = col("adopt_pressure")
    t_adopt = t + kappa_a * press_cum  # adoption clock: calendar time plus shortage-driven acceleration
    adopt = col("adopt_max") * logistic(t_adopt, col("adopt_mid"), col("adopt_width"))
    no_ai = structure == "no_ai"
    if no_ai:
        cap = {k: np.zeros_like(v) for k, v in cap.items()}
    sig = {k: lift(col(f"m_{k}"), TAI_TASK_CEILINGS[k]) * cap[k] * adopt for k in cap}

    # ===================================================================== 3-4. autonomy through the regulatory pipeline
    w = [col("w1"), col("w2"), col("w3")]
    w.append(np.maximum(0.0, 1.0 - w[0] - w[1] - w[2]))
    tcap = [col("tcap1_T0"), scaled("tcap2_T0"), scaled("tcap3_T0"), scaled("tcap4_T0")]
    mult_val, mult_fda, mult_pay = TIER_VAL_MULT, TIER_FDA_MULT, TIER_PAY_MULT
    if structure == "unordered":
        # no universal difficulty ladder: each future assigns the four capability dates to tiers in random order,
        # and validation, FDA and payment are equally hard for every tier
        perm = np.random.default_rng(11).permuted(np.tile(np.arange(4), (n, 1)), axis=1)
        tcap4 = np.take_along_axis(np.hstack(tcap), perm, axis=1)
        tcap = [tcap4[:, j:j + 1] for j in range(4)]
        mult_val, mult_fda, mult_pay = (np.full(4, m.mean()) for m in (TIER_VAL_MULT, TIER_FDA_MULT, TIER_PAY_MULT))
    auto = np.zeros_like(t * M)
    auto_parts = []
    ready, stage = [], []
    lag_mult = 1 - (1 - TAI_LAG_MULT) * tai
    ahalf = col("ahalf") * (1 - (1 - TAI_ADOPT_MULT) * tai)
    for j in range(4):
        lm = lag_mult if j > 0 else 1.0  # tier 1 is already technically capable; its regulatory clock is not compressed
        lv = col("lval") * mult_val[j] * lm
        lf = col("lfda") * mult_fda[j] * lm
        lp = col("lpay") * mult_pay[j] * lm
        rj = tcap[j] + lv + lf + lp
        ready.append(rj)
        stage.append(np.hstack([tcap[j], tcap[j] + lv, tcap[j] + lv + lf, rj, rj + ahalf]))
        amax = lift(col(f"amax{j + 1}"), TAI_AMAX)
        # adoption progress since readiness, on the shortage-accelerated clock
        idx = np.clip(np.floor(rj[:, 0] - 2026).astype(int), 0, T - 1)
        pc_ready = np.where(rj[:, 0] < 2026, 0.0, press_cum[np.arange(n), idx])[:, None]
        tau_j = (t - rj) + kappa_a * np.maximum(0.0, press_cum - pc_ready) * (t >= rj)
        part = w[j] * amax * logistic(tau_j, ahalf, col("awidth"))
        if structure in ("assistive_only", "no_ai"):
            part = np.zeros_like(part)
        auto_parts.append(part)
        auto = auto + part
    out["auto"] = auto
    out["stages"] = np.stack(stage, axis=1)
    if structure == "tai_gated":
        # extra assistive savings in the transformative branch count as de facto autonomy: they phase in only as the
        # tier-3 (complex exams) validation, FDA and payment pipeline clears, not on capability alone
        gate = logistic(t - ready[2], ahalf, col("awidth"))  # tier-3 regulatory clearance plus hospital adoption
        sig = {k: (col(f"m_{k}") + tai * gate * np.maximum(0.0, TAI_TASK_CEILINGS[k] - col(f"m_{k}"))) * cap[k] * adopt
               for k in cap}  # (n, tier, [capability, validated, FDA, paid/liability, 50% adoption])

    fsub = lift(col("f_sub"), TAI_FSUB)
    # radiologist time left on AI-first studies (share of interpretive work); zero in every tier under "no_signoff"
    fsub_t = [np.ones_like(fsub) if structure == "no_signoff" else fsub for j in range(4)]
    resid = sum(auto_parts[j] * (1 - fsub_t[j]) for j in range(4))
    iI = col("s_interp") * ((1 - auto) * (1 - sig["interp"]) + resid)
    iD = col("s_draft") * ((1 - auto) * (1 - sig["draft"]) + resid)
    iC = col("s_consult") * (1 - sig["consult"])
    iA = col("s_admin") * (1 - sig["admin"])
    iP = col("s_proc") * (1 - sig["proc"])
    raw = iI + iD + iC + iA + iP
    ovh = col("ovh_max") * np.minimum(1.0, (1 - raw) / 0.4)
    tau = raw + ovh
    tau0 = tau[:, :1]
    out.update(tau=tau, P=tau0 / tau, time_saved=1 - raw, adopt=adopt, cap_interp=cap["interp"], cap_draft=cap["draft"])

    # ===================================================================== 5. Jevons / rebound channels
    thru = col("thru_H") * logistic(t, scaled("thru_T0"), 3.0 * sqM) * (0.0 if no_ai else 1.0)
    price_cut = col("pass_through") * (col("pc_share") * (1 - tau) + (1 - col("pc_share")) * 0.5 * thru / (1 + thru))
    J_price = (1 - price_cut) ** col("elasticity") - 1
    k_new, k_nt, k_um = {"open_demand": (3.0, 2.0, 1.0), "payer_pushback": (1.0, 1.0, 2.0),
                         "no_ai": (0.0, 0.0, 0.0)}.get(structure, (1.0, 1.0, 1.0))
    new_max = k_new * col("new_max") * (1 + (TAI_NEW_MULT - 1) * tai)
    J_new = col("lambda_new") * new_max * logistic(t, scaled("new_T0"), col("new_width") * sqM)
    J_inc = col("iota") * adopt * cap["interp"]
    J_lat = col("latent") * thru / col("thru_H")
    J_acc = col("access") * (1 - tau)  # faster turnaround / 24-7 availability releases rationed demand
    G_pot = J_price + J_new + J_inc + J_lat + J_acc
    capacity = thru + col("cap_invest") * dt / 40 + 0.02
    if structure == "uncapped_new_uses":  # new uses that need no extra scanner time bypass the capacity cap
        G_rest = G_pot - J_new
        G = G_rest * (1 + (np.maximum(G_rest, 0) / capacity) ** 4) ** -0.25 + J_new
    else:
        G = G_pot * (1 + (G_pot / capacity) ** 4) ** -0.25  # smooth min(G_pot, capacity)
    share = np.divide(G, G_pot, out=np.zeros_like(G), where=G_pot > 1e-12)
    J_um = k_um * col("um_max") * adopt
    J_scope = k_um * col("scope_max") * (1 + (TAI_SCOPE_MULT - 1) * tai) * logistic(t, ready[1], 4.0)
    J = G - J_um - J_scope
    NT = k_nt * col("nt_max") * logistic(t, col("adopt_mid") + 8.0, 4.0)
    out["thru"] = thru
    out["capacity_bind"] = 1 - share  # fraction of potential induced exams blocked by capacity

    J0 = J[:, :1]
    rel_tau = tau / tau0
    W = B * (1 + J) / (1 + J0)
    D = W * rel_tau + B * (NT - NT[:, :1])
    out.update(W=W, D=D, J=J)

    # Jevons decomposition (FTE index units, relative to AI frozen at 2026)
    L = B * (1 - rel_tau)  # labour saved by productivity, holding work fixed at B
    k = B / (1 + J0) * rel_tau
    ch = {
        "Cheaper interpretation (price)": k * (J_price * share - (J_price * share)[:, :1]),
        "Faster turnaround & availability": k * (J_acc * share - (J_acc * share)[:, :1]),
        "Scanner throughput / latent demand": k * (J_lat * share - (J_lat * share)[:, :1]),
        "New applications & screening": k * (J_new * share - (J_new * share)[:, :1]),
        "Incidental findings & follow-up": k * (J_inc * share - (J_inc * share)[:, :1]),
        "New radiologist tasks": B * (NT - NT[:, :1]),
        "Utilization management (AI)": -k * (J_um - J_um[:, :1]),
        "Scope shift to non-radiologists": -k * (J_scope - J_scope[:, :1]),
    }
    I = sum(ch.values())
    out.update(L=L, I=I, channels=ch)
    out["offset"] = np.divide(I, L, out=np.full_like(I, np.nan), where=L > 1e-4)
    out["jevons"] = D > B

    # task composition of radiologist time (shares)
    nt_fte = B * (NT - NT[:, :1])
    read_share = np.clip(1 - nt_fte / D, 0, 1)
    comp = {"interp": iI, "draft": iD, "consult": iC, "admin": iA, "proc": iP, "oversight": ovh}
    out["composition"] = {kk: v / tau * read_share for kk, v in comp.items()}
    out["composition"]["newtasks"] = 1 - read_share

    # ===================================================================== 6. supply with endogenous residency response
    sup = simulate_supply(s, D, out["P"], structure)
    out.update(sup)
    out["D_struct"] = D  # before the market adjustment; the Jevons accounting D_struct = B - L + I refers to this
    out["D"] = D * np.exp(sup["adj"])  # demand for radiologists after work shifts to or from them with the market
    out["regime"] = regime
    out["M"] = np.asarray(s["ai_u"])
    out["ready"] = np.hstack(ready)
    return out


def simulate_supply(s: dict, D: np.ndarray, P: np.ndarray, structure: str = "base") -> dict:
    n = D.shape[0]
    ratio0 = np.asarray(s["ratio0"])
    gamma = np.asarray(s["resid_gamma"])
    kappa_f = np.asarray(s["fill_kappa"])
    lag = np.clip(np.rint(np.asarray(s["resid_lag"])), 1, 3).astype(int)
    fear = np.asarray(s["fear"])
    slot_g = np.asarray(s["slot_g"]) / 100
    drift = np.asarray(s["fte_drift"]) / 100
    hz = np.clip(HAZARD[None, :] * np.asarray(s["attr_mult"])[:, None], 0, 1)
    hz[:, -1] = 1.0

    coh = np.tile(COHORT_2023, (n, 1))
    filled = {y: np.full(n, float(v)) for y, v in FILLED_HIST.items()}
    positions = np.full(n, float(POSITIONS_2026))
    trend_level = np.full(n, float(POSITIONS_2026))  # the trend only accrues growth while the market is not in surplus

    S_fte = np.zeros((n, T))
    head = np.zeros((n, T))
    entrants_t = np.zeros((n, T))
    openings = np.zeros((n, T))
    pos_t = np.zeros((n, T))
    fill_t = np.zeros((n, T))
    lnratio = np.zeros((n, T))  # ln(D_abs / S_fte), + = shortage
    D_abs = None
    rows = np.arange(n)
    adjusting = "adj_speed" in s and structure != "no_adjustment"
    adj_speed = np.asarray(s["adj_speed"]) if adjusting else None
    adj_max = np.asarray(s["adj_max"]) if adjusting else None
    adj_up = adj_max  # how far work can flow to radiologists in a surplus
    if adjusting and structure == "shortage_only":
        adj_up = np.zeros(n)
    elif adjusting and structure == "adj_cap15":
        adj_max = adj_up = np.minimum(adj_max, 0.15)
    elif adjusting and structure == "adj_wide":  # rescale U(0.08, 0.28) to U(0.08, 0.5) and U(0.2, 0.55) to U(0.2, 0.8)
        adj_max = adj_up = 0.08 + (adj_max - 0.08) * (0.42 / 0.20)
        adj_speed = 0.2 + (adj_speed - 0.2) * (0.6 / 0.35)
    adj = np.zeros(n)
    adj_t = np.zeros((n, T))

    for year in range(SUPPLY_START + 1, 2067):
        exits = coh * hz
        surv = coh - exits
        match_year = year - TRAINING_LAG
        ent = KAPPA * filled[match_year]
        coh = np.concatenate([ent[:, None], surv[:, :-1]], axis=1)
        if year < 2026:
            continue
        i = year - 2026
        fte = (1 + drift) ** (year - 2026)
        head[:, i] = coh.sum(axis=1)
        S_fte[:, i] = head[:, i] * fte
        entrants_t[:, i] = ent
        if i == 0:
            D_abs = D * (S_fte[:, :1] / ratio0[:, None])
            D_struct_abs = D_abs.copy()
        elif adj_speed is not None:
            # market adjustment: each year a share of the remaining imbalance is closed by work moving between radiologists
            # and others and by the pace of labour-saving change, up to a cumulative limit (history test, model/history.py)
            adj = np.clip(adj - adj_speed * lnratio[:, i - 1], -adj_max, adj_up)
            D_abs[:, i] = D_struct_abs[:, i] * np.exp(adj)
        lnratio[:, i] = np.log(D_abs[:, i] / S_fte[:, i])
        adj_t[:, i] = adj
        surv_fte = surv.sum(axis=1) * fte
        openings[:, i] = np.maximum(0.0, D_abs[:, i] - surv_fte) / np.maximum(ent * fte, 1.0)

        # ---- next residency match (year+1) reacts to the market signal observed `lag` years earlier
        m = year + 1
        if m > max(FILLED_HIST):
            idx_hi = np.clip(i + 1 - lag, 0, i)
            idx_lo = np.clip(idx_hi - 2, 0, i)
            xbar = (lnratio[rows, idx_hi] + lnratio[rows, idx_lo] + lnratio[rows, (idx_hi + idx_lo) // 2]) / 3
            xbar = np.clip(xbar, -0.7, 0.4)
            growing = xbar >= 0
            trend_level = np.minimum(trend_level * (1 + slot_g * growing), GME_CAP * POSITIONS_2026)
            trend = trend_level
            g_eff = np.where(xbar < 0, gamma, 0.3 * gamma)
            target = np.minimum(trend * np.exp(g_eff * xbar), GME_CAP * POSITIONS_2026)
            grown = np.minimum(positions * (1 + slot_g * growing), GME_CAP * POSITIONS_2026)
            positions = grown + 0.35 * (target - grown)
            vis = np.clip((1 - 1 / P[:, i]) / 0.3, 0, 1)  # visible AI labour-saving deters applicants
            fill = np.clip(FILL_2026 * np.exp(kappa_f * np.minimum(xbar, 0)) - fear * vis, 0.4, 0.99)
            filled[m] = positions * fill
            if m - 2026 < T:
                pos_t[:, m - 2026] = positions
                fill_t[:, m - 2026] = fill
    pos_t[:, 0], fill_t[:, 0] = POSITIONS_2026, FILL_2026

    S_idx = S_fte / S_fte[:, :1]
    R = S_fte / D_abs
    return dict(S=S_idx, R=R, head=head, entrants=entrants_t, openings=openings, positions=pos_t,
                fill=fill_t, D_abs=D_abs, S_fte=S_fte, adj=adj_t)
