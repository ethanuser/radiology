"""Static figures for the report (matplotlib)."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from .analysis import FOCUS_GROUPS, OVERSUPPLY, yi  # noqa: E402
from .params import REGIME_NAMES, TASK_LABELS  # noqa: E402
from .simulate import YEARS  # noqa: E402

# Palette (validated categorical order; see dataviz reference palette)
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = (
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948")
RAMP = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]  # ordinal blue (stall -> transformative)
INK, INK2, MUTED, GRID, AXIS, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"

plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 10, "axes.titlesize": 12, "axes.titleweight": "bold", "axes.labelsize": 10,
    "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.spines.top": False,
    "axes.spines.right": False, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "legend.frameon": False, "lines.linewidth": 2, "lines.solid_capstyle": "round",
    "figure.dpi": 110, "savefig.dpi": 160, "axes.titlelocation": "left",
})

MARK_YEAR = 2035


def _fan(ax, arr, color, label, alpha_outer=0.12, alpha_inner=0.22):
    q = np.percentile(arr, [10, 25, 50, 75, 90], axis=0)
    ax.fill_between(YEARS, q[0], q[4], color=color, alpha=alpha_outer, lw=0)
    ax.fill_between(YEARS, q[1], q[3], color=color, alpha=alpha_inner, lw=0)
    ax.plot(YEARS, q[2], color=color, label=label)
    return q


def _mark(ax, text="M1 → attending (2035)"):
    ax.axvline(MARK_YEAR, color=AXIS, lw=1, zorder=0)
    lo, hi = ax.get_ylim()
    ax.text(MARK_YEAR + 0.4, lo + 0.02 * (hi - lo), text, va="bottom", ha="left", fontsize=8.5, color=INK2)


def _save(fig, out: Path, name: str):
    fig.tight_layout()
    fig.savefig(out / f"{name}.png")
    plt.close(fig)


def fig_demand_supply(o, out):
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    qd = _fan(ax, o["D"], BLUE, "Radiologist FTE demand")
    qs = _fan(ax, o["S"], ORANGE, "Radiologist FTE supply")
    ax.axhline(1, color=AXIS, lw=1)
    ax.set_ylabel("Index (2026 = 1.0)")
    ax.set_title("Demand vs supply of radiologist FTEs (median, 50% and 80% intervals)")
    ax.set_xlim(2026, 2066)
    ax.text(2066.3, qd[2][-1], f"Demand\n{qd[2][-1]:.2f}", va="center", fontsize=8.5, color=INK)
    ax.text(2066.3, qs[2][-1], f"Supply\n{qs[2][-1]:.2f}", va="center", fontsize=8.5, color=INK)
    ax.legend(loc="upper left")
    _mark(ax)
    _save(fig, out, "fig01_demand_supply")


def fig_ratio(o, out):
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    _fan(ax, o["R"], VIOLET, "Supply ÷ demand")
    ax.axhline(1.0, color=INK2, lw=1)
    ax.axhline(OVERSUPPLY, color=RED, lw=1)
    ax.text(2026.3, OVERSUPPLY + 0.01, "meaningful oversupply (>1.10)", fontsize=8.5, color=INK2, va="bottom")
    ax.text(2026.3, 0.985, "balance", fontsize=8.5, color=INK2, va="top")
    ax.set_ylim(0.6, 1.8)
    ax.set_xlim(2026, 2066)
    ax.set_ylabel("Supply ÷ demand (FTE)")
    ax.set_title("Supply/demand ratio (below 1 = shortage, above 1 = surplus)")
    _mark(ax)
    _save(fig, out, "fig02_ratio")


def fig_ai(o, out):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.0))
    import warnings
    warnings.filterwarnings("ignore", message="All-NaN slice")
    _fan(axes[0], o["P"], BLUE, "AI productivity")
    axes[0].set_title("AI productivity multiplier")
    axes[0].set_ylabel("Work per radiologist-hour (2026 = 1)")
    axes[0].set_ylim(0.9, 4.5)
    _fan(axes[1], o["auto"] * 100, AQUA, "Autonomous / AI-first share")
    axes[1].set_title("Share of interpretive work read AI-first / autonomously")
    axes[1].set_ylabel("% of interpretive work")
    for ax in axes:
        ax.set_xlim(2026, 2066)
        _mark(ax, "2035")
    _save(fig, out, "fig03_ai")


def fig_probs(probs, out):
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    series = [("p_demand_below_today", "Demand below 2026 level", BLUE),
              ("p_oversupply", "Meaningful oversupply (S/D > 1.10)", ORANGE),
              ("p_demand_below_80", "Demand below 80% of 2026", AQUA),
              ("p_demand_below_50", "Demand below 50% of 2026", YELLOW)]
    for key, label, c in series:
        ax.plot(probs["year"], probs[key] * 100, color=c, label=label)
        ax.text(2066.3, probs[key].iloc[-1] * 100, f"{probs[key].iloc[-1] * 100:.0f}%", va="center", fontsize=8.5)
    ax.set_ylabel("Probability (%)")
    ax.set_ylim(0, 60)
    ax.set_xlim(2026, 2066)
    ax.set_title("Probability of adverse workforce outcomes over time")
    ax.legend(loc="upper left")
    _mark(ax)
    _save(fig, out, "fig04_probabilities")


def fig_jevons(o, out):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), gridspec_kw={"width_ratios": [1.5, 1]})
    ax = axes[0]
    ch = o["channels"]
    names = list(ch)
    colors = [BLUE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, ORANGE, RED]
    pos_names = [n for n in names if ch[n].mean() >= 0]
    neg_names = [n for n in names if ch[n].mean() < 0]
    pos = np.vstack([ch[n].mean(0) for n in pos_names])
    neg = np.vstack([ch[n].mean(0) for n in neg_names])
    ax.stackplot(YEARS, pos, colors=[colors[names.index(n)] for n in pos_names], labels=pos_names, alpha=0.85,
                 edgecolor=SURFACE, linewidth=0.6)
    ax.stackplot(YEARS, neg, colors=[colors[names.index(n)] for n in neg_names], labels=neg_names, alpha=0.85,
                 edgecolor=SURFACE, linewidth=0.6)
    ax.plot(YEARS, o["L"].mean(0), color=INK, lw=2, label="Labor saved by AI productivity")
    ax.plot(YEARS, o["I"].mean(0), color=INK2, lw=1.5, ls=(0, (1, 1.5)), label="Net induced demand")
    ax.set_xlim(2026, 2066)
    ax.set_ylabel("FTE demand, share of 2026 level (mean)")
    ax.set_title("Labor saved vs AI-induced demand, by channel")
    ax.legend(fontsize=7.5, loc="upper left", ncol=1)
    ax = axes[1]
    yrs = [2030, 2035, 2045, 2055, 2066]
    data = [np.clip(o["offset"][:, yi(y)][np.isfinite(o["offset"][:, yi(y)])], -0.5, 2.0) for y in yrs]
    bp = ax.boxplot(data, positions=range(len(yrs)), widths=0.45, whis=(10, 90), showfliers=False, patch_artist=True,
                    medianprops=dict(color=INK, lw=1.5))
    for b in bp["boxes"]:
        b.set_facecolor("#cde2fb")
        b.set_edgecolor(BLUE)
    ax.axhline(1, color=RED, lw=1)
    ax.text(len(yrs) - 0.6, 1.03, "Jevons threshold", fontsize=8, ha="right", color=INK2)
    for k, y in enumerate(yrs):
        ax.text(k, -0.42, f"P={o['jevons'][:, yi(y)].mean() * 100:.0f}%", ha="center", fontsize=8, color=INK2)
    ax.set_xticks(range(len(yrs)), [str(y) for y in yrs])
    ax.set_ylim(-0.5, 1.6)
    ax.set_ylabel("Induced demand ÷ labor saved")
    ax.set_title("Offset ratio (box 25-75%, whiskers 10-90%)")
    _save(fig, out, "fig05_jevons")


def fig_tornado(tor, out, metric="D2045_p50", title="Median FTE demand in 2045", fname="fig06_tornado"):
    df = tor[tor[f"{metric}_swing"] > 1e-6].sort_values(f"{metric}_swing", ascending=True)
    fig, ax = plt.subplots(figsize=(8.5, 0.9 + 0.42 * len(df)))
    base = df[f"{metric}_base"].iloc[0]
    for k, (_, r) in enumerate(df.iterrows()):
        lo, hi = r[f"{metric}_low"], r[f"{metric}_high"]
        ax.barh(k, lo - base, left=base, color=BLUE, height=0.55, alpha=0.9 if r["focus"] else 0.45)
        ax.barh(k, hi - base, left=base, color=ORANGE, height=0.55, alpha=0.9 if r["focus"] else 0.45)
    ax.axvline(base, color=INK, lw=1)
    labels = [("● " if f else "") + g for g, f in zip(df["group"], df["focus"])]
    ax.set_yticks(range(len(df)), labels, fontsize=9)
    ax.set_xlabel(title)
    ax.set_title(f"What drives the forecast? {title}")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=BLUE, label="Assumption group at its 10th percentile"),
                       Patch(color=ORANGE, label="Assumption group at its 90th percentile")],
              loc="lower right", fontsize=8)
    ax.text(0.0, -0.13 if len(df) > 8 else -0.2, "● = assumption the question asked about specifically; faded = other groups",
            transform=ax.transAxes, fontsize=8, color=INK2)
    ax.grid(axis="y", visible=False)
    _save(fig, out, fname)


def _short(label, n=52):
    return label if len(label) <= n else label[: n - 1].rsplit(" ", 1)[0] + "…"


def fig_eta2(eta, out, top=18, fname="fig07_eta2", title="First-order sensitivity (η², share of output variance explained)"):
    cols = ["Demand 2035", "Demand 2045", "Demand 2055", "Supply/demand 2035", "Supply/demand 2045", "Supply/demand 2055"]
    df = eta.head(top)
    fig, ax = plt.subplots(figsize=(8.2, 6.4))
    mat = df[cols].values
    im = ax.imshow(mat, cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
        "b", ["#fcfcfb", "#86b6ef", "#2a78d6", "#0d366b"]), vmin=0, vmax=0.6, aspect="auto")
    ax.set_xticks(range(len(cols)), [c.replace("Supply/demand", "S/D").replace(" ", "\n", 1) for c in cols], fontsize=8.5)
    ax.set_yticks(range(len(df)), [f"[{e}] {l}" for e, l in zip(df["evidence"], df["short"])], fontsize=8.5)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center", fontsize=7.5,
                    color="white" if mat[i, j] > 0.3 else INK)
    ax.grid(False)
    ax.set_title(title)
    fig.colorbar(im, ax=ax, fraction=0.03)
    _save(fig, out, fname)


def fig_composition(o, out):
    comp = o["composition"]
    keys = ["interp", "draft", "consult", "admin", "proc", "oversight", "newtasks"]
    labels = [TASK_LABELS.get(k, "New radiologist tasks") for k in keys]
    colors = [BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET]
    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    data = np.vstack([comp[k].mean(0) * 100 for k in keys])
    ax.stackplot(YEARS, data, colors=colors, labels=labels, edgecolor=SURFACE, linewidth=0.8)
    ax.set_xlim(2026, 2066)
    ax.set_ylim(0, 100)
    ax.set_ylabel("% of radiologist working time (mean)")
    ax.set_title("How a radiologist's day changes (task composition)")
    ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=8)
    _save(fig, out, "fig08_composition")


def fig_baseline(o, out):
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    for key, label, c in (("B", "Total (no new AI)", BLUE), ("B_dem", "Demographics", ORANGE),
                          ("B_util", "Per-capita utilization", AQUA), ("B_cmplx", "Work per exam", YELLOW)):
        if key == "B":
            _fan(ax, o[key], c, label)
        else:
            ax.plot(YEARS, np.median(o[key], 0), color=c, label=label)
    ax.axhline(1, color=AXIS, lw=1)
    # Christensen et al: +16.9% to +26.9% (2023-2055, by modality) from population growth + aging alone,
    # rescaled to the 2026-2055 window (29 of 32 years, log-linear).
    lo, hi = np.exp(np.log(1.169) * 29 / 32), np.exp(np.log(1.269) * 29 / 32)
    ax.errorbar([2055], [(lo + hi) / 2], yerr=[[(hi - lo) / 2], [(hi - lo) / 2]], fmt="o", color=INK, ms=5,
                capsize=3, label="Christensen et al: demographics-only range (rescaled to 2026-55)")
    ax.set_xlim(2026, 2066)
    ax.set_ylabel("Index (2026 = 1.0)")
    ax.set_title("Baseline imaging workload without further AI")
    ax.legend(loc="upper left", fontsize=8.5)
    _save(fig, out, "fig09_baseline")


def fig_pipeline(o, out):
    st = o["stages"]  # n, tier, stage
    stage_names = ["Technically capable", "Clinically validated", "FDA authorized", "Paid & liability-accepted",
                   "50% of eventual adoption"]
    tiers = ["Tier 1: normal screens/radiographs", "Tier 2: all radiographs & screening",
             "Tier 3: complex CT/MR", "Tier 4: hardest residual work"]
    colors = [BLUE, ORANGE, AQUA, YELLOW, VIOLET]
    fig, ax = plt.subplots(figsize=(9, 4.6))
    for j in range(4):
        for k in range(5):
            v = st[:, j, k]
            q10, q50, q90 = np.percentile(v, [10, 50, 90])
            yy = j + (k - 2) * 0.14
            ax.plot([q10, q90], [yy, yy], color=colors[k], lw=2, alpha=0.6)
            ax.plot(q50, yy, "o", color=colors[k], ms=6, mec=SURFACE, mew=1.5, label=stage_names[k] if j == 0 else None)
    ax.set_yticks(range(4), tiers)
    ax.invert_yaxis()
    ax.set_xlim(2022, 2090)
    ax.axvline(2066, color=AXIS, lw=1)
    ax.text(2066.4, -0.45, "forecast horizon", fontsize=8, color=INK2)
    ax.set_xlabel("Year (dot = median, line = 10th-90th percentile)")
    ax.set_title("Regulatory pipeline: from capability to labor substitution")
    ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3)
    _save(fig, out, "fig10_pipeline")


def fig_regimes(o, out):
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    for r, name in enumerate(REGIME_NAMES):
        m = o["regime"] == r
        med = np.median(o["D"][m], 0)
        ax.plot(YEARS, med, color=RAMP[r], label=f"{name} ({m.mean() * 100:.0f}% of worlds)")
        ax.text(2066.3, med[-1], name, fontsize=8.5, va="center")
    ax.plot(YEARS, np.median(o["S"], 0), color=ORANGE, lw=1.5, label="Supply (all worlds, median)")
    ax.axhline(1, color=AXIS, lw=1)
    ax.set_xlim(2026, 2066)
    ax.set_ylabel("FTE demand index (2026 = 1)")
    ax.set_title("Median demand by AI-progress regime")
    ax.legend(loc="lower left", fontsize=8.5)
    _mark(ax)
    _save(fig, out, "fig11_regimes")


def fig_evidence(ev, out):
    df = ev[ev["metric"] == "D"]
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    grades = ["Empirical", "Anchored", "Subjective"]
    yrs = [2035, 2045, 2055]
    w = 0.25
    for k, y in enumerate(yrs):
        vals = [df[(df["grade"] == g) & (df["year"] == y)]["shrink"].iloc[0] * 100 for g in grades]
        ax.bar(np.arange(3) + (k - 1) * w, vals, width=w - 0.03, color=RAMP[k + 1], label=str(y))
    ax.set_xticks(range(3), [f"{g}\n({int(df[df['grade'] == g]['n_params'].iloc[0])} params)" for g in grades])
    ax.set_ylabel("% reduction in 80% interval width")
    ax.set_title("Where does the uncertainty come from? (demand)")
    ax.legend(title="Year", fontsize=8)
    _save(fig, out, "fig12_evidence")


def make_all(s, o, probs, tor, eta, ev, out: Path, eta_ntai=None):
    out.mkdir(parents=True, exist_ok=True)
    fig_demand_supply(o, out)
    fig_ratio(o, out)
    fig_ai(o, out)
    fig_probs(probs, out)
    fig_jevons(o, out)
    fig_tornado(tor, out)
    fig_tornado(tor, out, metric="pOver2045", title="P(meaningful oversupply) in 2045", fname="fig06b_tornado_oversupply")
    fig_eta2(eta, out)
    if eta_ntai is not None:
        fig_eta2(eta_ntai, out, fname="fig07b_eta2_excluding_transformative",
                 title="η² within non-transformative worlds (88% of simulations)")
    fig_composition(o, out)
    fig_baseline(o, out)
    fig_pipeline(o, out)
    fig_regimes(o, out)
    fig_evidence(ev, out)
