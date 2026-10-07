# Radiology 2066: a probabilistic forecast of the U.S. radiologist workforce

**Will AI take the radiology job a 2026 medical student is training for?** This repository contains a Monte Carlo model of
U.S. diagnostic-radiology demand and supply from 2026 to 2066, an interactive website, and a long technical report with
AMA-style citations.

* **Interactive site:** <https://ethanuser.github.io/radiology/>
* **Full report:** [`REPORT.md`](REPORT.md) (also rendered at <https://ethanuser.github.io/radiology/report.html>)
* **Model code:** [`model/`](model/) · **Results:** [`outputs/`](outputs/) · **Figures:** [`figures/`](figures/)

![Demand vs supply fan chart](figures/fig01_demand_supply.png)

## What the model does

Five components are modeled separately, each with explicit probability distributions, and propagated through 20,000
correlated Monte Carlo simulations:

1. **Baseline imaging demand**: population growth and aging (Christensen et al, JACR 2025, adjusted to CBO 2026
   demographics), per-capita utilization trends, and growing work per exam.
2. **AI productivity**: a task-based model following Langlotz (2025) and Acemoglu & Restrepo. Interpretation,
   measurement/drafting, consultation, administration and procedural work each have their own AI ceiling, capability curve
   and adoption curve. AI also creates new oversight work.
3. **Jevons/rebound effects**: cheaper interpretation (price elasticity × professional-fee share), faster turnaround, scanner
   throughput and latent demand, new applications and screening, incidental follow-up and new radiologist tasks. These are
   offset by AI utilization management and scope shift, and capped by scanner/technologist capacity.
4. **Regulation and adoption**: for four tiers of exam difficulty, the chain technical capability → clinical validation → FDA
   authorization → liability/reimbursement acceptance → hospital adoption → labor substitution.
5. **Radiologist supply**: a cohort model calibrated to Christensen et al's supply projection (+25.7% by 2055 with flat
   residency), with residency positions and fill rates that respond to the market with a lag.

The inputs are correlated through three latent factors (AI progress, regulatory friction, appetite for imaging) and four
AI-progress regimes (stall / trend / fast / transformative, weighted 15/55/18/12). Every parameter is graded **E**mpirical,
**A**nchored or **S**ubjective. See [`model/params.py`](model/params.py) and [`outputs/parameters.md`](outputs/parameters.md).

## Headline results

| | 2030 | 2035 | 2045 | 2055 | 2066 |
|---|---|---|---|---|---|
| FTE demand, median (P10–P90), 2026 = 1 | 1.04 (0.96–1.11) | 1.05 (0.80–1.19) | 1.10 (0.65–1.39) | 1.14 (0.63–1.57) | 1.19 (0.66–1.79) |
| FTE supply, median | 1.03 | 1.08 | 1.20 | 1.27 | 1.33 |
| Supply ÷ demand, median (2026 ≈ 0.93) | 0.91 | 0.96 | 1.01 | 1.05 | 1.06 |
| AI productivity, median | 1.06× | 1.21× | 1.39× | 1.48× | 1.56× |
| AI-first / autonomous share, median | <1% | 3% | 15% | 29% | 48% |
| P(demand < 2026) | 21% | 35% | 32% | 32% | 31% |
| P(demand < 50% of 2026) | 0% | <1% | 5% | 6% | 5% |
| **P(meaningful oversupply, S/D > 1.10)** | 3% | 17% | 34% | 42% | 42% |
| P(true Jevons paradox) | 16% | 3% | 3% | 2% | 1% |

*Numbers from the default run (`python run_model.py`, seed 20261007). The report and website regenerate from the outputs.*

**In one paragraph:** the market when a 2026 M1 finishes residency (2035) is most likely still short (64% chance) with a 17%
chance of meaningful oversupply. Most of that risk is concentrated in a 12%-weighted "transformative AI" branch; excluding it
the risk is 6%. Risk grows over a career (34% by 2045, 42% by 2055) as autonomous reading clears regulation and payment. A true
Jevons paradox, where AI-induced imaging outweighs the labor AI saves, is unlikely (≈3%): induced demand offsets about half
of the savings. Future per-capita imaging utilization and the AI-progress regime drive most of the uncertainty, and about half
of it comes from subjective parameters.

## Reproduce

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run_model.py          # simulation + sensitivity analysis -> outputs/, figures/, docs/data/  (~15 s)
python -m pytest             # calibration, accounting-identity and copula tests
python tools/build_docs.py   # regenerate REPORT.md and docs/report.html from the outputs
```

To view the site locally: `python -m http.server --directory docs` and open <http://localhost:8000>.

## Repository layout

```
model/
  params.py        every uncertain input: distribution, evidence grade, sources, factor loadings
  sampling.py      structured Gaussian-copula Monte Carlo sampler
  simulate.py      demand, AI task model, regulatory pipeline, Jevons channels, supply cohorts
  analysis.py      summary tables, Jevons accounting, η² and tornado sensitivity, signposts
  plots.py         report figures (matplotlib)
  export_web.py    JSON for the website
  references.py    bibliography (AMA style)
report/REPORT.src.md   report source with {{placeholders}} filled from model outputs
tools/build_docs.py    builds REPORT.md + docs/report.html, numbers citations by first appearance
docs/              GitHub Pages site (D3; data in docs/data/)
outputs/           CSV/JSON results;  figures/  PNG figures;  tests/  pytest suite
```

## Caveats

This is a forecasting exercise, not career, financial or medical advice. Long-range probabilities are coarse, and many inputs
are explicit judgment calls (graded **S**). The model, code and prose were drafted with an AI assistant (Claude, Anthropic)
from the public sources cited in [`REPORT.md`](REPORT.md#references) and should be read critically. Corrections and
alternative parameter choices are welcome: change [`model/params.py`](model/params.py) and re-run.

Code: MIT License. Text and figures: CC BY 4.0.
