# Will AI Shrink the Radiology Job Market?
## A probabilistic forecast of the U.S. diagnostic-radiology workforce, 2026–2066

*For anyone considering, training in, or early in a career in diagnostic radiology · Version 1.3 · October 2026 ·
Interactive version: <https://ethanuser.github.io/radiology/> · Code and data: this repository*

> **How to read this document.** Every number is produced by the Monte Carlo model in [`model/`](model/) and inserted by
> [`tools/build_docs.py`](tools/build_docs.py); re-running the model regenerates the report. Superscript section marks
> (for example <sup>§4.3</sup>) link each claim to the method or evidence behind it, and numbered superscripts link to references.
> Each reference has ↩ links back to every place it is cited, and your browser's Back button returns you to where you were.
> The model and text were drafted with an AI assistant (Claude, Anthropic) from the cited sources and should be read
> critically. This is a forecast, not career, financial or medical advice. The probabilities are conditional on the model's
> assumptions: read them as structured, model-based judgment (a scenario analysis with explicit weights), not as a calibrated
> statistical forecast. §8.4 shows how much they move under alternative assumptions and model structures.

---

## Summary

**Question.** Diagnostic radiology is the specialty most often named as a likely casualty of AI. For someone choosing the
specialty now, or already training in it, what will the market for radiologists' labor look like when they enter practice
and over the following decades? How much does AI change it?

**Approach.** We built a probabilistic model with five separately specified components: baseline imaging demand, task-level
AI productivity, the regulatory and adoption pipeline for autonomous AI, Jevons/rebound effects, and a cohort model of
radiologist supply with an endogenous residency response.<sup>[§4](#sec-model "Method / evidence for this claim")</sup> Its 66 uncertain inputs are drawn
from explicit probability distributions, correlated through three latent factors (AI progress, regulatory friction, appetite
for imaging), and propagated through 20,000 simulated futures.<sup>[§4.6](#sec-uncertainty "Method / evidence for this claim")</sup> Each input is graded
**empirical** (E), **anchored** (A: an empirical anchor plus judgment) or **subjective** (S).<sup>[§5](#sec-params "Method / evidence for this claim")</sup>

**Headline results** (median with 10th–90th percentile range; indices relative to 2026):

| Metric | 2030 | 2035 | 2045 | 2055 | 2066 |
|---|---|---|---|---|---|
| **FTE demand** (2026 demand = 1): median (P10–P90) | 1.02 (0.94–1.08) | 1.01 (0.77–1.13) | 1.05 (0.62–1.30) | 1.08 (0.59–1.43) | 1.11 (0.62–1.59) |
|   FTE demand: P25–P75 | 0.99–1.05 | 0.93–1.07 | 0.92–1.18 | 0.90–1.26 | 0.88–1.35 |
| **FTE supply** (2026 demand = 1): median (P10–P90) | 0.95 (0.91–0.99) | 1.00 (0.95–1.04) | 1.09 (1.02–1.16) | 1.15 (0.95–1.29) | 1.19 (0.82–1.46) |
|   FTE supply: P25–P75 | 0.93–0.97 | 0.97–1.02 | 1.06–1.13 | 1.07–1.22 | 1.04–1.33 |
| **Supply ÷ demand** (2026 ≈ 0.93): median (P10–P90) | 0.93 (0.87–1.02) | 0.99 (0.87–1.29) | 1.05 (0.85–1.66) | 1.09 (0.84–1.58) | 1.09 (0.81–1.41) |
|   Supply ÷ demand: P25–P75 | 0.90–0.97 | 0.92–1.07 | 0.94–1.19 | 0.95–1.25 | 0.95–1.24 |
| **AI productivity** (work per radiologist-hour, 2026 = 1) | 1.06 (1.02–1.23) | 1.22 (1.09–1.87) | 1.38 (1.22–2.90) | 1.47 (1.28–3.66) | 1.55 (1.33–3.79) |
|   AI productivity: P25–P75 | 1.04–1.11 | 1.15–1.32 | 1.29–1.50 | 1.36–1.63 | 1.42–1.73 |
| **AI-first / autonomous share** of interpretive work | <1% (<1%–3%) | 2% (<1%–12%) | 13% (4%–53%) | 26% (9%–88%) | 45% (16%–95%) |
|   AI-first share: P25–P75 | <1%–1% | 1%–5% | 7%–22% | 16%–47% | 27%–58% |
| P(demand < 2026 level) | 33% | 46% | 39% | 38% | 37% |
| P(demand < 80% of 2026) | 1% | 11% | 14% | 17% | 18% |
| P(demand < 50% of 2026) | 0% | <1% | 6% | 7% | 6% |
| P(supply > demand) | 14% | 45% | 60% | 67% | 68% |
| **P(meaningful oversupply: S/D > 1.10)** | 3% | 20% | 39% | 48% | 49% |
| P(severe oversupply: S/D > 1.25) | <1% | 11% | 19% | 25% | 24% |
| P(shortage worse than 10%: S/D < 0.90) | 27% | 17% | 18% | 18% | 19% |

**Key findings**

1. **Over the next decade the market most likely stays balanced or short.** Radiologists who will practice in 2035 have mostly already
   matched or started medical school, and imaging demand keeps growing with an aging population. The median
   supply/demand ratio in 2035 is 0.99 (below 1 means a shortage). The probability of meaningful
   oversupply (more than 10% excess radiologist capacity) is 20% in 2035, and most of it sits in
   a "transformative AI" branch with a 12% prior; outside that branch it is
   9%.<sup>[§7.2](#sec-balance "Method / evidence for this claim")</sup><sup>[§7.5](#sec-regimes "Method / evidence for this claim")</sup>
2. **Risk grows with time in practice.** Median FTE demand rises only modestly (+5% by 2045,
   +8% by 2055) because AI productivity absorbs most of the growth in imaging. The probability of
   meaningful oversupply rises to 39% in 2045 and 48% in 2055
   (any surplus, $R>1$: 60% in 2045),
   and from 2035 on, 37%–46%
   of futures have demand below today's level. With no further AI, oversupply would be
   6% likely in 2045 and 18% in 2055
   (supply slowly overtaking slow-growing demand); with assistive AI but no AI-first reading,
   31% and 32%. This
   later risk is not only a transformative-AI story: excluding that branch, oversupply is still
   31% likely in 2045 and 41% in 2055.<sup>[§7.1](#sec-ds "Method / evidence for this claim")</sup>
3. **A collapse is a tail, not a base case.** Demand falls below half of today's level with probability
   6% in 2045 and 6% in 2066, almost entirely in
   transformative-AI worlds.<sup>[§7.5](#sec-regimes "Method / evidence for this claim")</sup>
4. **AI productivity is real but slow to be realized.** Median time saved per unit of imaging work is
   18% in 2035 and 32% in 2055. AI-first or autonomous
   reading reaches a median 13% of interpretive work by 2045. For each tier of exam
   difficulty, the chain from technical capability to clinical validation, FDA authorization, liability and payment
   acceptance, and hospital adoption takes one to two decades.<sup>[§7.3](#sec-aiprod "Method / evidence for this claim")</sup><sup>[§4.3](#sec-pipeline "Method / evidence for this claim")</sup>
5. **A true Jevons paradox is unlikely under the main assumptions, but this depends on the demand channels assumed.**
   AI-induced demand (cheaper and faster reads, new applications, follow-up of AI-detected findings, scanner throughput, new
   radiologist tasks) offsets a median 50% of the labor AI saves by 2045 and exceeds it in only
   4% of simulated futures. If AI creates three times as many new imaging uses (and twice the new
   radiologist tasks) as assumed, that rises to
   27%.<sup>[§7.4](#sec-jevres "Method / evidence for this claim")</sup><sup>[§8.4](#sec-robust "Method / evidence for this claim")</sup>
6. **What drives the forecast:** the AI-progress regime and future per-capita imaging use, then the size of assistive-AI
   time savings. Regulatory delay, new applications and scanner throughput are second-order. Growth in residency positions
   becomes a top driver by 2055. About half the
   spread comes from parameters graded subjective.<sup>[§8](#sec-sensitivity "Method / evidence for this claim")</sup>
7. **For practicing radiologists, AI risk would most likely show up as slower hiring of new graduates, flatter pay and a
   changed job, not unemployment.** The model forecasts only the supply/demand balance; the split between hiring, pay and hours
   is an interpretation from past gluts, not a model output. Attrition of about 2.7% of the workforce a year absorbs gradual declines,
   but new graduates keep entering: a severe surplus ($R>1.25$) lasts five or more years in
   30% of futures (21% outside the
   transformative branch).
   Demand falls faster than attrition over some five-year window after 2035 in
   9% of futures, and in
   0.2% outside the transformative branch.<sup>[§9.2](#sec-margins "Method / evidence for this claim")</sup>
8. **The backtest is a weak sanity check.** Run from 2016 with only the information then available, a simplified version of
   the approach gave a 67% chance of the radiologist shortage seen in 2025, but that result
   comes from the supply-versus-demand fundamentals rather than the AI layer, and ranges from
   42% to 75% under other
   reasonable protocol choices. For the three other occupations, the BLS-plus-trend combination alone was more accurate
   than the full method on average: the AI layer helped for translators, tied for software and hurt badly for
   transcription.<sup>[§6.2](#sec-backtest "Method / evidence for this claim")</sup>
9. **The direction is robust; the exact numbers are not.** Under four alternative prior sets and six alternative model
   structures (including reads with no radiologist, automation that does not follow a difficulty ladder, and no shortage
   today), the 2045
   oversupply probability ranges from 23% to 53% (main
   model 39%); changing the AI and imaging priors together widens this to
   15%–61%. Every variant agrees that risk is lower in 2035 than later and rises over a
   career.<sup>[§8.4](#sec-robust "Method / evidence for this claim")</sup>

**By career stage** (details in §9<sup>[§9](#sec-careers "Method / evidence for this claim")</sup>):

| Where you are in fall 2026 | Typical first attending year* | P(oversupply) when you start | 10 years in | 20 years in | 30 years in (or 2066) | P(demand below 2026) 10 years in | P(still a shortage) when you start |
|---|---|---|---|---|---|---|---|
| Pre-med (college junior) | 2038 | 28% | 42% | 49% | 49% (2066) | 38% | 47% |
| Medical student, year 1 | 2036 | 23% | 40% | 48% | 49% (2066) | 39% | 51% |
| Medical student, year 2 | 2035 | 20% | 39% | 48% | 49% (2065) | 39% | 55% |
| Medical student, year 3 | 2034 | 17% | 38% | 47% | 49% (2064) | 39% | 59% |
| Medical student, year 4 | 2033 | 14% | 36% | 46% | 50% (2063) | 40% | 64% |
| Intern (PGY-1) | 2032 | 11% | 35% | 46% | 50% (2062) | 40% | 71% |
| Radiology resident, R1 | 2031 | 7% | 33% | 45% | 50% (2061) | 41% | 79% |
| Radiology resident, R2 | 2030 | 3% | 31% | 44% | 50% (2060) | 42% | 86% |
| Radiology resident, R3 | 2029 | 1% | 30% | 43% | 49% (2059) | 43% | 93% |
| Radiology resident, R4 | 2028 | <1% | 28% | 42% | 49% (2058) | 44% | 98% |
| Fellow | 2027 | 0% | 25% | 41% | 49% (2057) | 45% | 100% |
| Practicing radiologist | 2026 | 0% | 23% | 40% | 48% (2056) | 46% | 100% |

\*Assumes a 1-year fellowship; subtract one year without it.

---

<a name="sec-question"></a>
## 1. Question, scope and definitions

**Population.** U.S. diagnostic radiologists. Supply is calibrated to the Harvey L. Neiman Health Policy Institute count of
37,482 radiologists enrolled to serve Medicare patients in 2023 <a name="c1-1"></a><sup>[1](#ref-1)</sup>, a broader definition than the AAMC's
28,618 "radiology and diagnostic radiology" physicians <a name="c2-1"></a><sup>[2](#ref-2)</sup>. All outputs are indices relative to 2026, so the
definitional difference matters mainly through the ratio of entrants to the existing stock.

**Career timelines.** The stage table above shows when people at each stage in 2026 would typically start independent
practice: a pre-med around 2038, a first-year medical student around 2035–2036, a current R1 around 2031. The forecast
reports calendar years. Read across to your own start year.

**Definitions.**

* **FTE demand $D(t)$**: radiologist full-time equivalents needed to perform the imaging work demanded in year $t$, given the
  AI in use, as an index with $D(2026)=1$. It includes work that is currently backlogged or outsourced.
* **FTE supply $S(t)$**: practicing radiologists × FTE per head, as an index with $S(2026)=1$.
* **Supply/demand ratio $R(t)$**, in absolute FTEs. Today's market is short: $R(2026)$ ≈ 0.93 (range 0.85–0.99).<sup>[§4.1](#sec-baseline "Method / evidence for this claim")</sup>
  **Meaningful oversupply** is $R>1.10$. This threshold is a convention for a clearly noticeable surplus: the mid-1990s and
  mid-2010s gluts <a name="c3-1"></a><a name="c4-1"></a><sup>[3](#ref-3),[4](#ref-4)</sup> were never measured on this scale, so we also report $P(R>1)$.
  **Severe oversupply** is $R>1.25$.
* **AI productivity $P(t)$**: imaging work completed per radiologist-hour relative to 2026. Time saved is $1-1/P$.
* **AI-first/autonomous share**: share of interpretive work where AI is the primary reader and the radiologist audits,
  signs off or handles escalations.

---

<a name="sec-approach"></a>
## 2. Forecasting approach: outside view first

We follow practices that distinguish accurate forecasters in tournaments: decompose the question, start from base rates
(the "outside view"), state explicit probabilities with wide intervals, and name the observations that should move the
forecast <a name="c5-1"></a><a name="c6-1"></a><a name="c7-1"></a><a name="c8-1"></a><sup>[5](#ref-5)-[8](#ref-8)</sup>. Four reference classes anchor the priors.

1. **Confident predictions that AI would displace radiologists have so far failed.** In 2016 Geoffrey Hinton said that
   people "should stop training radiologists now" <a name="c9-1"></a><sup>[9](#ref-9)</sup>. A decade later, diagnostic-radiology programs offered a
   record 1,241 positions with a 97.6% fill rate <a name="c10-1"></a><sup>[10](#ref-10)</sup>, and average radiology compensation rose 6.6% in the latest
   annual survey <a name="c11-1"></a><sup>[11](#ref-11)</sup>. The FDA lists more than 1,600 AI-enabled devices, about three-quarters in radiology
   <a name="c12-1"></a><sup>[12](#ref-12)</sup>, but claims data show clinical use concentrated in a handful of products <a name="c13-1"></a><sup>[13](#ref-13)</sup>. Langlotz's framing
   since 2019 has been that AI changes the work rather than replacing the worker <a name="c14-1"></a><a name="c15-1"></a><sup>[14](#ref-14),[15](#ref-15)</sup>.
2. **The radiology labor market cycles with supply and utilization shocks.** After the mid-1990s downturn, radiology trainee
   numbers fell to a nadir of 3,080 in 1997 and then rose 84% by 2011 <a name="c16-1"></a><sup>[16](#ref-16)</sup>. Positions kept expanding despite
   a softening job market, and the market was oversupplied by the mid-2010s <a name="c3-2"></a><sup>[3](#ref-3)</sup>. In the 2015 Match only 86%
   of advanced DR positions filled and U.S. graduates took 67% of matched positions <a name="c4-2"></a><sup>[4](#ref-4)</sup>. Students respond to market
   signals within a few years <a name="c17-1"></a><a name="c18-1"></a><sup>[17](#ref-17),[18](#ref-18)</sup>.
3. **Clinical technology diffuses only after payment and liability are resolved, and then it can diffuse quickly.**
   Mammography computer-aided detection (FDA 1998, Medicare payment 2002) was used for most U.S. screening mammograms within a
   few years, despite no measurable accuracy benefit <a name="c19-1"></a><sup>[19](#ref-19)</sup>. Hospital EHR adoption passed 50% about four years after
   the 2009 HITECH subsidies <a name="c20-1"></a><sup>[20](#ref-20)</sup>. Autonomous diabetic-retinopathy AI took three years from FDA
   authorization (2018) to a payable CPT code <a name="c21-1"></a><sup>[21](#ref-21)</sup>.
4. **Automation economics.** In the task framework, automation displaces labor from automated tasks, raises demand through
   productivity, and can reinstate labor through new tasks <a name="c22-1"></a><a name="c23-1"></a><sup>[22](#ref-22),[23](#ref-23)</sup>. Whether
   employment rises depends on demand elasticity, which was high early in industrialization and fell as demand saturated
   <a name="c24-1"></a><sup>[24](#ref-24)</sup>. Most of today's U.S. employment is in job specialties created after 1940 <a name="c25-1"></a><sup>[25](#ref-25)</sup>. Whether automation
   raises or lowers wages depends on whether it removes the expert or the inexpert parts of a job <a name="c26-1"></a><sup>[26](#ref-26)</sup>.
   The idea that efficiency can increase total use goes back to Jevons <a name="c27-1"></a><sup>[27](#ref-27)</sup>.

**AI-progress inputs.** METR's measured task horizons for frontier models doubled about every seven months from 2019 to 2024
<a name="c28-1"></a><sup>[28](#ref-28)</sup>, and faster after 2023 <a name="c29-1"></a><sup>[29](#ref-29)</sup>. AI 2027 sketches very rapid progress <a name="c30-1"></a><sup>[30](#ref-30)</sup>. A survey of 2,778 AI
researchers put even odds on machines outperforming humans at every task by 2047, but on full automation of occupations only
by 2116 <a name="c31-1"></a><sup>[31](#ref-31)</sup>. Expert and superforecaster panels assign far lower probabilities to near-term transformative AI than
industry leaders do <a name="c32-1"></a><a name="c33-1"></a><sup>[32](#ref-32),[33](#ref-33)</sup>. We use these sources only to weight four AI-progress regimes and to scale
when radiology capabilities arrive.<sup>[§4.6](#sec-uncertainty "Method / evidence for this claim")</sup> None of them is a forecast about medicine.

<a name="sec-approaches"></a>
### 2.1 Ways to forecast a job market, and why this one

There are several ways to answer "will there be jobs?", each with a track record.

| Approach | Strength | Weakness | Evidence on accuracy |
|---|---|---|---|
| Ask a domain expert or a famous thinker | Rich context, fast | Overconfident; experts rarely beat informed generalists on long-range questions | In 20 years of tracked political and economic forecasts, specialists did no better than generalists, and "hedgehogs" with one big idea did worst <a name="c34-1"></a><sup>[34](#ref-34)</sup>. Hinton's 2016 call on radiology <a name="c9-2"></a><sup>[9](#ref-9)</sup> |
| Aggregate many forecasters (superforecasters, prediction markets) | Best record on 1–2 year questions | Few long-horizon or niche questions; thin markets | Teams of trained forecasters beat individuals and intelligence analysts <a name="c5-2"></a><a name="c6-2"></a><sup>[5](#ref-5),[6](#ref-6)</sup>; markets aggregate dispersed information well <a name="c8-2"></a><a name="c35-1"></a><sup>[8](#ref-8),[35](#ref-35)</sup>. In a 2022 tournament, superforecasters and domain experts had nearly identical overall accuracy, and both underestimated AI benchmark progress, superforecasters more so (9.7% vs 24.6% average probability on what happened); the median of all forecasts beat individuals <a name="c36-1"></a><sup>[36](#ref-36)</sup> |
| Extend the trend / reference-class base rates | Simple, hard to beat over short horizons | Misses turning points | The "outside view" corrects planning optimism <a name="c7-2"></a><sup>[7](#ref-7)</sup>; simple statistical methods were competitive in the M4 competition <a name="c37-1"></a><sup>[37](#ref-37)</sup> |
| Official projections (BLS) | Careful, occupation-level, public | Assume slow technology change | BLS projected +14% for medical transcriptionists over 2006–16; employment fell 41% <a name="c38-1"></a><a name="c39-1"></a><sup>[38](#ref-38),[39](#ref-39)</sup> |
| Task-exposure indices | Rank which jobs are exposed | No timing, regulation or demand response | Frey & Osborne ranked transcription as highly automatable and software as not <a name="c40-1"></a><sup>[40](#ref-40)</sup>; LLM exposure estimates <a name="c41-1"></a><sup>[41](#ref-41)</sup> |
| Scenarios | Make tails concrete | No probabilities | AI 2027 <a name="c30-2"></a><sup>[30](#ref-30)</sup> |
| Structured probabilistic model (this report) | Decomposes the question into parts with evidence; keeps every assumption explicit; outputs probabilities that can be updated | Only as good as its subjective inputs; can create false precision | Combining forecasts usually beats choosing one <a name="c37-2"></a><a name="c42-1"></a><sup>[37](#ref-37),[42](#ref-42)</sup>; backtest in §6.2<sup>[§6.2](#sec-backtest "Method / evidence for this claim")</sup> |

We use the structured model as the main tool, but borrow from the others: base rates set the priors (§2), official
projections and trends enter the backtest baseline, AI forecasts weight the regimes, and the signposts in §9.3 are designed
for updating, as superforecasters do. No method has a good record at 20–40-year horizons, so the long-range probabilities
in this report should be read as structured judgment, not measurement.

---

<a name="sec-evidence"></a>
## 3. Recent evidence (2024–2026)

For a general overview of what AI can and cannot yet do compared with radiologists, see the review by Rajpurkar and
Lungren in the *New England Journal of Medicine* <a name="c43-1"></a><sup>[43](#ref-43)</sup> and Mousa's accessible essay on why AI has not replaced
radiologists <a name="c15-2"></a><sup>[15](#ref-15)</sup>. This section summarizes the empirical work most relevant to the model's least certain components. Full texts of RSNA and
open-access journals were reviewed. For some Elsevier journals (including JACR), figures come from abstracts because
full-text access was blocked for automated reading.

**3.1 How much time does AI save radiologists today?**

| Study | Setting and design | Measured effect on radiologist time |
|---|---|---|
| Huang et al, 2025 <a name="c44-1"></a><sup>[44](#ref-44)</sup> | 23,960 radiographs, live deployment, 12 hospitals | 15.5% faster documentation; no loss of accuracy |
| Hong et al, 2025 <a name="c45-1"></a><sup>[45](#ref-45)</sup> | 758 chest radiographs, 5 readers, reader study | Reading time 34.2 s → 19.8 s (−42%) |
| Li et al, 2026 <a name="c46-1"></a><sup>[46](#ref-46)</sup> | LLM impressions, 42 hospitals, blinded comparison | −0.46 min per report; impressions non-inferior in 69% |
| Liu et al, 2026 <a name="c47-1"></a><sup>[47](#ref-47)</sup> | 185,044 chest CT reports, 2 hospitals, retrospective | No sustained efficiency gain at one of two sites |
| Tanno et al, 2025 <a name="c48-1"></a><sup>[48](#ref-48)</sup> | AI chest-radiograph reports vs radiologists | AI report preferred or equivalent in 77.7% (94% of normal cases); clinically significant errors in 22.8% of AI-only vs 14.0% of human-only reports |
| Wenderott et al, 2024 <a name="c49-1"></a><sup>[49](#ref-49)</sup> | Meta-analysis of real-world AI deployments | 67% of studies reported time reductions; pooled effects not significant |
| Yu et al, 2024 <a name="c50-1"></a><sup>[50](#ref-50)</sup> | 140 radiologists, 15 chest-radiograph tasks | Effects of AI assistance highly heterogeneous; erroneous AI output hurt performance |
| Lauritzen et al, 2024 <a name="c51-1"></a><sup>[51](#ref-51)</sup> | Danish screening program before vs after AI | 33.5% fewer screening reads; higher cancer detection, lower recall |
| MASAI, 2023–2026 <a name="c52-1"></a><a name="c53-1"></a><a name="c54-1"></a><sup>[52](#ref-52)-[54](#ref-54)</sup> | 105,934 women, randomised | 44% lower screen-reading workload; 29% more cancers detected; interval cancers non-inferior (rate ratio 0.88) |

The screening savings come from replacing the second reader in European double reading, a substitution effect that does
not transfer to single-read U.S. practice; we use them only to size tier 1, not to set assistive ceilings. The evidence
supports large savings on drafting and in screening programs, modest and heterogeneous savings on
interpretation, and little measured effect at system scale so far.<sup>[§4.2](#sec-ai "Method / evidence for this claim")</sup>

**3.2 How much work could be read autonomously?** A commercial tool could autonomously report 28% of normal posteroanterior
chest radiographs (7.8% of all) with 99.1% sensitivity for abnormal films <a name="c55-1"></a><sup>[55](#ref-55)</sup>. With a tuned threshold, about 47%
of unremarkable films (roughly 17.5% of all chest radiographs) could be excluded at 99% sensitivity <a name="c56-1"></a><sup>[56](#ref-56)</sup>. An
autonomous normal-chest-radiograph product has held EU CE Class IIb marking since 2022 <a name="c57-1"></a><sup>[57](#ref-57)</sup>. In the U.S., no
autonomous radiology read is FDA-authorized as of October 2026 <a name="c12-2"></a><sup>[12](#ref-12)</sup>. Generative chest-radiograph drafting tools
received FDA Breakthrough designations in 2026, and a cleared breast-ultrasound tool generates reports under radiologist
control <a name="c58-1"></a><a name="c59-1"></a><sup>[58](#ref-58),[59](#ref-59)</sup>. FDA's AI lifecycle guidance remains a draft <a name="c60-1"></a><sup>[60](#ref-60)</sup>. Of FDA-authorized AI
devices, 43% had no published clinical validation and about 4% had randomized evidence <a name="c61-1"></a><sup>[61](#ref-61)</sup>. Liability rules
are unsettled <a name="c62-1"></a><sup>[62](#ref-62)</sup>, and mock jurors judge radiologists more harshly when they miss something AI flagged
<a name="c63-1"></a><sup>[63](#ref-63)</sup>.<sup>[§4.3](#sec-pipeline "Method / evidence for this claim")</sup>

**3.3 Adoption.** In 2020, 33.5% of surveyed U.S. radiologists used any AI <a name="c64-1"></a><sup>[64](#ref-64)</sup>. By 2025, 75% of UK radiology
departments used AI clinically, but the Royal College of Radiologists found no overall reduction in workload. The UK
consultant shortfall was 32% <a name="c65-1"></a><sup>[65](#ref-65)</sup>. In China, AI use was associated with *higher* burnout odds among radiologists with
high workloads <a name="c66-1"></a><sup>[66](#ref-66)</sup>.

**3.4 Workforce and demand.** Average exams read per radiologist-day were flat from 2018 to 2024 (+0.6%), but the busiest
quartile read 30.6% more <a name="c67-1"></a><sup>[67](#ref-67)</sup>. Practice turnover rose from 5.3% to 8.5% between 2013 and 2022 and followed a
U-shaped relationship with workload <a name="c68-1"></a><sup>[68](#ref-68)</sup>. Emergency-department CT per 100 Medicare beneficiaries nearly doubled
from 2013 to 2023 even as ED visits fell <a name="c69-1"></a><sup>[69](#ref-69)</sup>. A review of 2024 imaging research found that 49% of articles
with direct patient-care impact would increase radiologist workload and fewer than 1% would decrease it. AI studies had about 14 times higher
odds of adding work (odds ratio 14.3, 95% CI 4.2–48.2; with a baseline near 49%, roughly twice
as likely) <a name="c70-1"></a><sup>[70](#ref-70)</sup>.<sup>[§4.1](#sec-baseline "Method / evidence for this claim")</sup><sup>[§4.4](#sec-jevons "Method / evidence for this claim")</sup>

**3.5 Labor-market evidence from other occupations.** In payroll data, workers aged 22–25 in the most AI-exposed occupations
saw a 16% relative employment decline after 2022, while experienced workers did not. Firms adjusted headcount rather than
pay <a name="c71-1"></a><sup>[71](#ref-71)</sup>. Danish administrative data show near-zero effects of chatbots on earnings and hours, partly because AI
created new oversight tasks <a name="c72-1"></a><sup>[72](#ref-72)</sup>. Field experiments find meaningful productivity gains concentrated among less
experienced workers <a name="c73-1"></a><sup>[73](#ref-73)</sup>. Macro estimates of AI's productivity effect over a decade are modest
<a name="c74-1"></a><sup>[74](#ref-74)</sup>, and measured exposure is broad across occupations <a name="c41-2"></a><sup>[41](#ref-41)</sup>. These findings shape the model's
assumption that the first adjustment margin is new-graduate hiring rather than layoffs of incumbents.<sup>[§9.2](#sec-margins "Method / evidence for this claim")</sup>

---

<a name="sec-model"></a>
## 4. Model structure

```mermaid
flowchart TB
  subgraph Demand["1 · Baseline demand"]
    A1[Population & aging] --> B[(Baseline work B)]
    A2[Per-capita utilization] --> B
    A3[Work per exam] --> B
  end
  subgraph AI["2 · AI productivity"]
    C1[Interpretation / drafting / consultation / admin / procedures] --> T[(Time per unit work τ)]
    C6[AI oversight ↑] --> T
  end
  subgraph Reg["4 · Regulation & adoption"]
    R1[Capability] --> R2[Validation] --> R3[FDA] --> R4[Liability & payment] --> R5[Adoption]
  end
  R5 --> T
  subgraph Jev["3 · Jevons / rebound"]
    J1[Cheaper & faster reads, throughput, new uses, follow-up, new tasks] --> J[(Induced work J)]
    J6[Utilization management, scope shift] -.-> J
  end
  T --> J1
  B --> D([FTE demand D])
  J --> D
  T --> D
  subgraph Sup["5 · Supply"]
    S1[Residency positions] --> S2[Entrants +6 yrs] --> S[(FTE supply S)]
    S3[Attrition by career year] --> S
  end
  D --> RR{Supply ÷ demand}
  S --> RR
  RR -->|lagged signal| S1
  RR -->|shortage speeds adoption| R5
```

<a name="sec-baseline"></a>
### 4.1 Baseline imaging demand (AI frozen at its 2026 level)

$$B(t)=\prod_{s=2027}^{t}\bigl(1+r_{\text{dem}}(s)+r_{\text{util}}(s)+r_{\text{cmplx}}(s)\bigr)\cdot\frac{1-a(t)}{1-a(2026)}$$

* **Demographics, $r_{\text{dem}}$.** Population growth and aging alone raise imaging 16.9%–26.9% from 2023 to 2055,
  depending on modality <a name="c75-1"></a><sup>[75](#ref-75)</sup>, under Census 2023 population forecasts. CBO's 2026 outlook has markedly lower
  population growth (349 million in 2026 to 364 million in 2056) <a name="c76-1"></a><sup>[76](#ref-76)</sup>, so we center demographic growth of radiologist
  work at 0.52%/yr (A), declining after 2045.
* **Per-capita utilization, $r_{\text{util}}$.** Age-specific CT use grew 3.7–5.2%/yr in 2013–2016 and MRI 1.3–2.2%/yr, while
  nuclear medicine declined <a name="c77-1"></a><sup>[77](#ref-77)</sup>. About 93 million CTs were performed in 2023 <a name="c78-1"></a><sup>[78](#ref-78)</sup>. ED CT per
  Medicare beneficiary nearly doubled from 2013 to 2023 <a name="c69-2"></a><sup>[69](#ref-69)</sup>. National 2018–22 claims data imply total utilization in
  2055 that is 16.9% to 26.9% above 2023 by modality from population growth and aging alone, and between 5.6% lower and 45.2%
  higher if each modality's recent per-person trend continues to 2030 (radiography and nuclear medicine falling, CT and MRI
  rising) <a name="c75-2"></a><sup>[75](#ref-75)</sup>. The Neiman Institute's 2026 update projects +17% (MRI) to +25% (CT) by 2055 and calls the
  shortage "fairly static" <a name="c79-1"></a><sup>[79](#ref-79)</sup>. We start the per-person trend at 0.6%/yr (σ 0.7) and let it converge to 0.2%/yr (σ 0.5) with an uncertain half-life. Demographics times per-person use then
  grows a median 29% from 2026 to 2055 (80%:
  6% to 58%). Each end of Christensen's
  trend range is a single modality (CT up, nuclear medicine down), so a work-weighted claims-based figure is lower than CT's;
  our center sits above the claims-based trends, because 2018–22 includes the COVID dip and we let growth continue past 2030,
  and below CT's own trend. This is a deliberate judgment, and the most consequential non-AI one (§8.1); the "imaging restraint"
  prior set in §8.4 is close to the claims-based trends. The input is graded subjective. Version 1.2 centered this trend at 1.2%/yr.
* **Work per exam, $r_{\text{cmplx}}$.** Images per cross-sectional study rose about tenfold at Mayo Clinic from 1999 to 2010
  <a name="c80-1"></a><sup>[80](#ref-80)</sup>. Work per exam grows far more slowly than image counts: 0.4%/yr, decaying with a 20-year half-life.
* **Alternative diagnostics, $a(t)$.** Blood-based tests, AI-ECG and similar tools displace up to 15% of imaging (mode 4%).
* **Today's gap (subjective).** No measured national figure exists. HRSA *projects* radiology at about 90% workforce
  adequacy in 2038, and the Neiman Institute describes the shortage as "fairly static" <a name="c79-2"></a><sup>[79](#ref-79)</sup>. Pay is rising and positions
  are expanding, but per-radiologist volumes are flat on average and the strain is uneven <a name="c67-2"></a><a name="c68-2"></a><sup>[67](#ref-67),[68](#ref-68)</sup>.
  $R(2026)$ is triangular on 0.85–0.99 (mode 0.93), graded subjective.

<a name="sec-ai"></a>
### 4.2 AI productivity: a task-based model

Following Langlotz's task-based analysis <a name="c81-1"></a><sup>[81](#ref-81)</sup> and the Acemoglu–Restrepo framework, radiologists' 2026 working time
is drawn from a Dirichlet distribution centered on interpretation 42%, measurement and drafting 18%, clinical synthesis and
consultation 13%, administration 15% and procedures 12%. Langlotz allocates 66.7% of time to performing and interpreting
studies, 5.5% to protocoling and 11.8% to communication. A time-motion study found 36.4% pure interpretation <a name="c82-1"></a><sup>[82](#ref-82)</sup>.
For each task $k$, assistive AI saves

$$\sigma_k(t)=m_k\cdot \text{cap}_k(t)\cdot \text{adopt}(t)$$

where $m_k$ is the eventual ceiling (anchored on §3.1), $\text{cap}_k$ a logistic capability curve scaled by the
AI-progress multiplier $M$, and $\text{adopt}$ the effective clinical adoption, whose clock runs faster while demand exceeds
supply (new in v1.1). For the AI-first share $\alpha(t)$, a fraction $f_{\text{sub}}$ of interpretation and drafting time is
removed. Oversight work $o(t)$ grows with AI use <a name="c72-2"></a><sup>[72](#ref-72)</sup>. Time per unit of work relative to a no-AI world is

$$\tau(t)=s_I\bigl[(1-\alpha)(1-\sigma_I)+\alpha(1-f_{\text{sub}})\bigr]+s_D\bigl[(1-\alpha)(1-\sigma_D)+\alpha(1-f_{\text{sub}})\bigr]+\sum_{k\in\{C,A,P\}}s_k(1-\sigma_k)+o(t)$$

and AI productivity is $P(t)=\tau(2026)/\tau(t)$.

<a name="sec-pipeline"></a>
### 4.3 Regulation and adoption: from capability to labor substitution

Interpretive work is split into four autonomy tiers. Tier 1 is normal or negative radiographs and screening exams, ≈7% of
interpretive work after recalibration to the Danish evidence in §3.2. Tier 2 is all radiographs, screening mammography and
standardized follow-ups (≈17%). Tier 3 is complex diagnostic CT/MR/US/NM (≈47%). Tier 4 is the hardest residual work. Each
tier passes, in sequence:

$$T^{\text{ready}}_j = T^{\text{cap}}_j + L^{\text{validation}}_j + L^{\text{FDA}}_j + L^{\text{liability/payment}}_j,\qquad
\alpha(t)=\sum_j w_j\,a^{\max}_j\,\text{logistic}\!\left(\tfrac{\tilde t_j(t)-h}{\text{width}}\right)$$

where $\tilde t_j$ is time since readiness on the shortage-accelerated adoption clock. Validation lags are anchored on
MASAI, which took about five years from randomization (April 2021) to its interval-cancer endpoint (January 2026)
<a name="c54-2"></a><sup>[54](#ref-54)</sup>, and on the scarcity of prospective validation <a name="c61-2"></a><sup>[61](#ref-61)</sup>. FDA lags are anchored on the absence of any
U.S. autonomous radiology authorization so far and on the IDx-DR precedent <a name="c12-3"></a><a name="c21-2"></a><sup>[12](#ref-12),[21](#ref-21)</sup>. Liability and
payment lags are anchored on CPT 92229 for autonomous retinal AI, CPT 75577 for AI coronary plaque analysis
<a name="c83-1"></a><sup>[83](#ref-83)</sup>, and liability research <a name="c62-2"></a><a name="c63-2"></a><sup>[62](#ref-62),[63](#ref-63)</sup>. Adoption half-times follow the CAD and EHR precedents
<a name="c19-2"></a><a name="c20-2"></a><sup>[19](#ref-19),[20](#ref-20)</sup>. All lags load on a common regulatory-friction factor.

<a name="sec-jevons"></a>
### 4.4 Jevons and rebound effects

| Channel | Specification | Evidence |
|---|---|---|
| Cheaper interpretation (price) | $(1-\Delta p)^{\varepsilon}-1$; professional share ≈20%, pass-through ≈40%, elasticity ≈−0.2 | <a name="c84-1"></a><a name="c85-1"></a><a name="c86-1"></a><a name="c87-1"></a><sup>[84](#ref-84)-[87](#ref-87)</sup> |
| Faster turnaround & availability | access × time saved | <a name="c88-1"></a><sup>[88](#ref-88)</sup> |
| Scanner throughput / latent demand | latent demand (2–12%) released as AI-accelerated acquisition frees capacity | <a name="c89-1"></a><a name="c90-1"></a><sup>[89](#ref-89),[90](#ref-90)</sup> |
| New applications & screening | lognormal, median 18% of baseline work by 2066 × radiologist intensity 0.4–1.0 | <a name="c70-2"></a><a name="c83-2"></a><a name="c91-1"></a><a name="c92-1"></a><sup>[70](#ref-70),[83](#ref-83),[91](#ref-91),[92](#ref-92)</sup> |
| Incidental findings & follow-up | up to 8% at full AI-detection deployment | <a name="c53-2"></a><a name="c93-1"></a><sup>[53](#ref-53),[93](#ref-93)</sup> |
| New radiologist tasks (reinstatement) | up to 12% of 2026 FTE | <a name="c23-2"></a><a name="c25-2"></a><sup>[23](#ref-23),[25](#ref-25)</sup> |
| AI utilization management (−) | up to 8% | <a name="c81-2"></a><a name="c94-1"></a><sup>[81](#ref-81),[94](#ref-94)</sup> |
| Scope shift to non-radiologists (−) | up to 10% | subjective |

Exam-generating channels pass through a smooth minimum with capacity: $G=G_{\text{pot}}(1+(G_{\text{pot}}/K)^4)^{-1/4}$. FTE
demand is

$$D(t)=B(t)\,\frac{1+J(t)}{1+J(2026)}\,\frac{\tau(t)}{\tau(2026)}+B(t)\bigl[N(t)-N(2026)\bigr]$$

Labor saved is $L=B(1-\tau/\tau_0)$, induced demand is $I=D-B\,\tau/\tau_0$, and the offset ratio is $I/L$. A *true Jevons
paradox* is $I>L$, equivalently $D>B$. The identity $D=B-L+I$ is unit-tested.

<a name="sec-supply"></a>
### 4.5 Radiologist supply

A cohort model tracks practicing radiologists by years in practice. Exit hazard rises to retirement levels after about 33
years and is scaled by a multiplier, U(0.95, 1.25). With flat positions, multipliers of 1.0 and 1.2 reproduce the published
supply projections under blended 2014–23 attrition (+25.7% by 2055) and post-COVID attrition (+20.9%); the range is centered
between them, nearer the post-COVID case. Measured attrition rose from 1.1% (2014) to 2.0% (2019) and 2.5% (2022)
<a name="c1-2"></a><a name="c79-3"></a><sup>[1](#ref-1),[79](#ref-79)</sup>; the cohort model's aggregate rate is not directly comparable, because the
entrants-per-position factor $\kappa$ absorbs definitional differences.
Practice turnover has also roughly doubled <a name="c68-3"></a><sup>[68](#ref-68)</sup>. Entrants in year $t$ equal $\kappa$ × filled DR positions from
the year $t-6$ Match, where $\kappa=$1.20 is calibrated so that flat residency
positions reproduce Christensen et al's +25.7% (2023–2055) <a name="c1-3"></a><sup>[1](#ref-1)</sup>. Positions start at 1,241 <a name="c10-2"></a><sup>[10](#ref-10)</sup>,
follow a trend (1%/yr, σ 0.8, capped at 1.8× by GME funding), and respond to the lagged signal $x=\ln(D/S)$:

$$\text{positions}^{*}=\text{trend}\cdot e^{\gamma x},\qquad \text{fill}=0.976\,e^{\kappa_f\min(x,0)}-\text{fear}\cdot\text{visibility}_{AI}$$

<a name="sec-uncertainty"></a>
### 4.6 Uncertainty, correlation, regimes and the shortage feedback

Inputs are drawn through a structured Gaussian copula with three factors: AI progress, regulatory friction and appetite for
imaging. This preserves every marginal while inducing the intended correlations, which are tested: faster AI means earlier
capability *and* higher task ceilings *and* more new applications *and* more throughput. The AI factor selects a regime with
these subjective weights:

| Regime | Weight | Timeline multiplier $M$ | Interpretation |
|---|---|---|---|
| Stall | 15% | 1.6–3.0 | radiology AI arrives 1.6–3× later than trend |
| Trend | 55% | lognormal, median 1 | current pace continues |
| Fast | 18% | 0.40–0.65 | roughly 2× faster |
| Transformative | 12% | 0.25–0.45 + lifted ceilings | AI eventually does nearly all radiologist cognitive work; institutional lags shrink 40%; robotics still lags |

**Shortage feedback (new in v1.1).** Version 1.0 assumed adoption speed was independent of the shortage. Now the model solves
in two passes. Pass 1 computes the shortage path $\ln(D/S)$. Pass 2 runs the assistive and autonomous adoption clocks faster
by $1+\kappa_a\max(0,\ln(D/S))$ with $\kappa_a\sim U(0,4)$ (subjective), so a 7% shortage speeds adoption by up to 28%. This is one
fixed-point iteration of the coupled system.

---

<a name="sec-params"></a>
## 5. Parameters and evidence

The model has 66 sampled parameters plus the task-share Dirichlet: 0 graded E,
32 graded A and 34 graded S. The empirical backbone sits mostly in **fixed calibration
targets**: the 2023 workforce, career length, attrition, the flat-residency supply projection, 2026 positions and fill rate,
and the demographic projection. The full table is in [Appendix A](#appendix-a). What is *not* well supported by data: the
speed of general AI progress, the ceilings on AI time savings for non-interpretive tasks, the size of AI-enabled new
applications, and regulatory and liability lags for autonomous reading. These are the parameters the sensitivity analysis
flags.<sup>[§8](#sec-sensitivity "Method / evidence for this claim")</sup>

---

<a name="sec-validation"></a>
## 6. Calibration and validation

### 6.1 Calibration checks

| Check | Model | Reference |
|---|---|---|
| Supply growth 2023→2055, flat residency (calibration target, matched by construction) | +25.7% | +25.7% <a name="c1-4"></a><sup>[1](#ref-1)</sup> |
| Supply growth 2023→2055, flat residency, attrition multiplier 1.2 (calibration end-point, not independent) | +21.5% | +20.9% with post-COVID attrition <a name="c79-4"></a><sup>[79](#ref-79)</sup> |
| No further AI, flat residency positions, no market response: supply ÷ demand (independent check) | median 0.89 (2035), 0.88 (2045), 0.86 (2055) | shortage "fairly static" if no action is taken <a name="c79-5"></a><sup>[79](#ref-79)</sup> |
| Mean career length | 34.6 years | 34.2–35.7 years |
| Aggregate attrition, 2023 | 2.7%/yr | 1.1% (2014) rising to 2.5% (2022) <a name="c79-6"></a><sup>[79](#ref-79)</sup> |
| Demographic growth of imaging work, 2026→2055 | 15.7% | +16.9% to +26.9% for 2023→2055 with higher Census population <a name="c75-3"></a><sup>[75](#ref-75)</sup> |
| Realized AI time savings by 2031 | median 8.6% (P90 25%) | Langlotz: 33% (14%–49%), an "upper end" potential if all applications are adopted <a name="c81-3"></a><sup>[81](#ref-81)</sup> |
| Demographics × per-person imaging use, 2026→2055 | median 29% (80%: 6% to 58%) | 2023→2055 across modalities: +16.9% to +26.9% (demographics only), −5.6% to +45.2% (recent trends to 2030) <a name="c75-4"></a><sup>[75](#ref-75)</sup>; +17% to +25% <a name="c79-7"></a><sup>[79](#ref-79)</sup> |
| Baseline radiologist work 2026→2055, no further AI | +32% median | Exam projections above plus work per exam (complexity); no direct benchmark |

The near-term AI effect is below Langlotz's potential because the model adds documented diffusion, validation and payment
lags. It sits within the range of measured real-world effects in §3.1. Unit tests check the calibrations, the exact Jevons
identity, copula marginals and correlation signs, regime weights, the shortage feedback, the alternative structures, and that
every reference has a link (links were checked by hand, not by the tests).

<a name="sec-backtest"></a>
### 6.2 Backtest: forecasting 2025 from 2016

Calibration checks show that the model reproduces published projections; they do not show that the *method* forecasts well.
To test that, we set the clock back to 2016 and forecast employment in 2025 using only information available then. 2016 is a
natural start: it is the year of Hinton's "stop training radiologists" remark and of large-scale neural machine translation.

**Protocol** (fixed before computing outcomes and applied the same way to every case; code in `model/backtest.py`). The
backtest replays a simplified version of the method, with the same structure and AI-regime mixture but a generic
task-exposure model, rather than the full radiology model:

* *Baseline (non-AI) growth* is an equal-weight combination of the BLS 2016–26 projection and the prior decade's trend. Their
  disagreement sets the baseline uncertainty <a name="c42-2"></a><sup>[42](#ref-42)</sup>.
* *AI layer*, with the same structure as the main model: a share of work exposed to automation (mapped from Frey & Osborne's
  2013 automation probabilities <a name="c40-2"></a><sup>[40](#ref-40)</sup>, the standard estimate in 2016), a capability S-curve timed by the
  **same AI-regime mixture** as the main model, an adoption lag, and a demand rebound set by the occupation's demand elasticity
  (high for software, middle for translation, low for transcription).
* *Radiology* also gets a supply side (the 2016–25 training pipeline was largely fixed) and a 2016 starting balance near
  or slightly above 1 after the mid-2010s glut <a name="c3-3"></a><a name="c4-3"></a><sup>[3](#ref-3),[4](#ref-4)</sup>. The question scored is whether 2025 shows a
  shortage.
* Employment data come from the BLS *Occupational Outlook Handbook* (2008, 2018 and 2026 editions) <a name="c38-2"></a><a name="c39-2"></a><a name="c95-1"></a><a name="c96-1"></a><a name="c97-1"></a><a name="c98-1"></a><a name="c99-1"></a><a name="c100-1"></a><a name="c101-1"></a><sup>[38](#ref-38),[39](#ref-39),[95](#ref-95)-[101](#ref-101)</sup>.

![Figure 13. Backtest: forecasts made with 2016 information vs outcomes in 2025 (left), and the radiology hindcast under alternative protocol choices (right).](figures/fig13_backtest.png)

| Occupation | Employment 2016 → 2025, actual | This method: median (80% interval) | BLS + trend combination, no AI layer | BLS projection (2016) | Prior trend | Inside 80% interval? | Frey & Osborne automation probability |
|---|---|---|---|---|---|---|---|
| Software developers | 1.37 | 1.32 (1.14–1.53) | 1.32 | 1.21 | 1.44 | yes | 0.09 |
| Interpreters & translators | 1.08 | 1.29 (1.00–1.65) | 1.36 | 1.16 | 1.58 | yes | 0.38 |
| Medical transcriptionists | 0.73 | 0.57 (0.37–0.86) | 0.78 | 0.97 | 0.62 | yes | 0.89 |
| Radiologists (supply ÷ demand in 2025) | shortage (≈0.93) | 0.95 (0.84–1.09); P(shortage) 67%; 42%–75% under protocol variants | — | — | — | yes | 0.0042 (physicians and surgeons; not used) |

**Results.** All three occupations fell inside the method's 80% intervals (coverage 100%). The mean
absolute log error was 0.15 for the full method, 0.16 for BLS,
0.20 for trend extrapolation, and **0.11 for the BLS-plus-trend combination
alone**. On average forecast combination did the work. Per occupation, the AI layer helped for translators (log error
0.17 vs 0.22), tied for software developers,
and hurt badly for medical transcription, where it over-predicted the
decline in medical transcription (median 0.57 vs 0.73;
combination alone 0.78), plausibly because speech recognition moved much of the work to editing
drafts rather than eliminating it <a name="c39-3"></a><sup>[39](#ref-39)</sup>, a rebound the "low elasticity" class understated. Translation growth was
over-predicted by every method that used the strong prior trend.

For radiology the method gave a 67% chance of a 2025 shortage, which is what the market
signals in §3 indicate. That result is driven by assumed demand growth (2%/yr) outpacing a nearly fixed supply (1%/yr) from
a 2016 starting point near balance; neither input is sourced to a 2016 document, and radiology's AI exposure (0.35) was
set by hand rather than from the Frey & Osborne mapping used for the other occupations. At the main model's own starting
demand growth (about 1.5%/yr) the hindcast is close to a coin flip. The AI layer moves it modestly (median
effect on 2025 demand 0.3%, because the regulatory lag delays most labor substitution
beyond 2025). Changed one
at a time, the result is 75% without the AI layer,
51% with demand growth of 1.5%/yr,
53% with a 3-year adoption lag, and
42% if 2016 began in a 10% surplus. The Brier score on this single
event is 0.11 (0.25 for a coin flip), which says little on its own; and the outcome it is scored against,
a shortage, rests on the indirect market signals behind the subjective 2026 starting point.

**Limits.** Four cases cannot establish forecasting skill or calibration at a 40-year horizon. The 2016 inputs were selected in
2026, and the capability timing for each occupation (for example, neural translation reaching production quality around 2022)
and the radiology regulatory lag are judgments that may carry hindsight even though they were fixed before scoring. Wide
intervals make coverage easy. What the backtest does support is narrower: combining forecasts helps, and in radiology the
supply pipeline and demand growth, not AI, determined the 2016–2025 outcome. Several start dates, a larger reference class
and forecasts recorded before outcomes are known would make a stronger test.

---

<a name="sec-results"></a>
## 7. Results

<a name="sec-ds"></a>
### 7.1 Demand and supply

![Figure 1. Radiologist FTE demand and supply, both in units of 2026 demand, median with 50% and 80% intervals. Supply starts below 1 because 2026 is a shortage; where the lines cross, supply equals demand.](figures/fig01_demand_supply.png)

Median FTE demand rises +1% by 2035, +5% by 2045 and
+11% by 2066. Baseline workload rises +23% by 2045 without further
AI.<sup>[§7.7](#sec-baseres "Method / evidence for this claim")</sup> Supply is predictable for a decade: relative to 2026 supply, the median index is 1.08 in 2035
(≈41,433 radiologists) and 1.18 in 2045.<sup>[§4.5](#sec-supply "Method / evidence for this claim")</sup>

<a name="sec-balance"></a>
### 7.2 The supply/demand balance

![Figure 2. Supply ÷ demand. Below 1 is a shortage; above 1.10 meaningful oversupply.](figures/fig02_ratio.png)

![Figure 4. Probability of adverse outcomes over time.](figures/fig04_probabilities.png)

In the median world the shortage narrows through the 2030s and the market is roughly balanced in the 2040s (median ratio
1.05 in 2045). The probability of meaningful oversupply rises from
3% (2030) to 20% (2035), 39% (2045)
and 48% (2055). A shortage worse than 10% remains possible but less likely in 2045
(18%).

<a name="sec-aiprod"></a>
### 7.3 AI productivity and autonomy

![Figure 3. AI productivity multiplier and AI-first/autonomous share.](figures/fig03_ai.png)

![Figure 10. The regulatory pipeline by autonomy tier.](figures/fig10_pipeline.png)

| Tier | Capable | Validated | FDA-authorized | Paid & liability-accepted | 50% of eventual adoption |
|---|---|---|---|---|---|
| Tier 1 — normal/negative radiographs & screening | 2025 (2024–2026) | 2028 (2026–2030) | 2029 (2027–2032) | 2032 (2029–2038) | 2038 (2033–2045) |
| Tier 2 — all radiographs, screening mammography, standardized follow-up | 2030 (2027–2037) | 2033 (2029–2041) | 2035 (2030–2044) | 2040 (2033–2051) | 2046 (2037–2058) |
| Tier 3 — complex diagnostic CT/MR/US/NM | 2038 (2031–2055) | 2042 (2033–2060) | 2045 (2035–2064) | 2052 (2038–2074) | 2058 (2043–2081) |
| Tier 4 — hardest residual work | 2048 (2035–2079) | 2053 (2038–2085) | 2058 (2041–2091) | 2066 (2045–2103) | 2072 (2049–2110) |

Tier 1 is typically payable in the early 2030s, but tier 3 (complex cross-sectional work, where most radiologist time goes)
only in the 2050s. The upper tail of productivity (P90 2.90× in 2045) comes from the
transformative branch.<sup>[§7.5](#sec-regimes "Method / evidence for this claim")</sup>

<a name="sec-jevres"></a>
### 7.4 Jevons accounting: does AI-induced demand offset AI productivity?

![Figure 5. Labor saved versus AI-induced demand by channel (left) and the offset ratio (right).](figures/fig05_jevons.png)

| | 2030 | 2035 | 2045 | 2055 | 2066 |
|---|---|---|---|---|---|
| Labor saved by AI productivity (mean, share of 2026 FTE) | 0.087 | 0.239 | 0.391 | 0.485 | 0.573 |
| ↳ induced: Cheaper interpretation (price) | +0.004 | +0.008 | +0.011 | +0.012 | +0.013 |
| ↳ induced: Faster turnaround & availability | +0.009 | +0.019 | +0.026 | +0.031 | +0.036 |
| ↳ induced: Scanner throughput / latent demand | +0.014 | +0.027 | +0.037 | +0.041 | +0.043 |
| ↳ induced: New applications & screening | +0.021 | +0.043 | +0.072 | +0.087 | +0.099 |
| ↳ induced: Incidental findings & follow-up | +0.005 | +0.014 | +0.021 | +0.023 | +0.025 |
| ↳ induced: New radiologist tasks | +0.004 | +0.017 | +0.053 | +0.067 | +0.074 |
| ↳ induced: Utilization management (AI) | −0.012 | −0.021 | −0.022 | −0.022 | −0.023 |
| ↳ induced: Scope shift to non-radiologists | −0.003 | −0.009 | −0.023 | −0.032 | −0.036 |
| **Net AI-induced demand (mean)** | 0.042 | 0.099 | 0.176 | 0.207 | 0.231 |
| Offset ratio, induced ÷ saved: median (P10–P90) | 0.46 (0.08–0.98) | 0.43 (0.17–0.74) | 0.50 (0.20–0.82) | 0.47 (0.19–0.78) | 0.43 (0.19–0.71) |
| Ratio of means | 0.49 | 0.41 | 0.45 | 0.43 | 0.40 |
| **P(true Jevons paradox: induced > saved)** | 9.2% | 2.1% | 3.5% | 2.5% | 1.5% |

* Induced demand offsets a median 43% (2035), 50% (2045) and 43% (2066) of the
  labor AI saves. A true Jevons paradox occurs in 2.1% of worlds in 2035 and
  2.5% in 2055. Early on (2030) it is more common (9%) because throughput
  gains can arrive before reading-time savings.
* Cheaper interpretation is the weakest channel. The professional fee is about 10%–30% of an exam's all-in price
  <a name="c84-2"></a><sup>[84](#ref-84)</sup>, and demand is price-inelastic (≈−0.2) <a name="c85-2"></a><a name="c86-2"></a><sup>[85](#ref-85),[86](#ref-86)</sup>, so halving interpretation cost adds
  roughly 1%–2% more exams.
* The large channels are new applications, new radiologist tasks, throughput/latent demand and faster turnaround: the
  "reinstatement" and "new work" mechanisms <a name="c23-3"></a><a name="c25-3"></a><sup>[23](#ref-23),[25](#ref-25)</sup>. Recent literature suggests AI tends to
  *add* radiologist work <a name="c70-3"></a><sup>[70](#ref-70)</sup>. Capacity limits remove on average 11% of potential
  induced exams in 2045.
* In Bessen's terms <a name="c24-2"></a><sup>[24](#ref-24)</sup>, radiologist demand behaves like a mature, fairly inelastic market.

<a name="sec-regimes"></a>
### 7.5 AI-progress regimes

![Figure 11. Median demand by AI-progress regime.](figures/fig11_regimes.png)

| AI regime | Weight | Timeline multiplier M | Median demand 2035 / 2045 / 2055 | AI productivity 2045 | AI-first share 2045 | P(oversupply) 2035 / 2045 / 2055 |
|---|---|---|---|---|---|---|
| Stall | 15% | 1.6–3.0 | 1.05 / 1.12 / 1.18 | 1.21× | 6% | 3% / 23% / 33% |
| Trend | 55% | ≈0.65–1.6 (median 1) | 1.02 / 1.08 / 1.12 | 1.36× | 11% | 9% / 31% / 39% |
| Fast | 18% | 0.40–0.65 | 1.00 / 1.04 / 1.05 | 1.48× | 20% | 16% / 39% / 52% |
| Transformative | 12% | 0.25–0.45 + ceilings lifted | 0.67 / 0.50 / 0.47 | 3.47× | 71% | 98% / 100% / 100% |

Excluding the transformative branch, the 2045 oversupply probability is 31%, and the
probability that 2045 demand is below 80% of today's is 3%.

<a name="sec-tasks"></a>
### 7.6 How the job changes

![Figure 8. Task composition of radiologist working time (mean across worlds).](figures/fig08_composition.png)

| Task | 2026 | 2035 | 2045 | 2055 | 2066 |
|---|---|---|---|---|---|
| Interpretation / reporting | 42% | 40% | 35% | 32% | 29% |
| Measurement & report drafting | 18% | 12% | 10% | 9% | 9% |
| Clinical synthesis & consultation | 13% | 14% | 14% | 15% | 15% |
| Administrative (protocoling, QA) | 15% | 13% | 13% | 13% | 14% |
| Physical / procedural | 12% | 15% | 16% | 17% | 17% |
| AI oversight (new task) | <1% | 4% | 6% | 7% | 8% |
| Other new radiologist tasks | 0% | 2% | 6% | 7% | 7% |

<a name="sec-baseres"></a>
### 7.7 Baseline demand without further AI

![Figure 9. Baseline radiologist workload with AI frozen at 2026 levels.](figures/fig09_baseline.png)

Without further AI, workload would grow a median +12% by 2035 and
+32% by 2055 (P10–P90: +5% to
+65%). That growth is the main reason the median market stays near balance: AI in the median
world mostly absorbs growth that would otherwise deepen the shortage. It is also the most consequential non-AI input (§8.1).

---

<a name="sec-sensitivity"></a>
## 8. Sensitivity analysis

<a name="sec-tornado"></a>
### 8.1 Which assumptions move the forecast?

Each assumption group is pinned at its 10th and then its 90th percentile while all other inputs keep their distributions
(8,000 simulations per run, common random numbers). All members of a group are pinned at the same percentile together, which is
more extreme than the group's combined 10th/90th percentile unless the members are perfectly correlated, and more so the
weaker their correlation. For future imaging utilization, this sets three inputs at their tails at once; the milder prior sets
in §8.4 are a better guide to its plausible effect. Bold rows are six commonly debated
assumptions.

![Figure 6. Tornado: median FTE demand in 2045.](figures/fig06_tornado.png)

![Figure 6b. Tornado: probability of meaningful oversupply in 2045.](figures/fig06b_tornado_oversupply.png)

| Assumption group (10th → 90th percentile) | Median demand 2035 | Median demand 2045 | Median demand 2055 | P(oversupply) 2035 | P(oversupply) 2045 | P(oversupply) 2055 |
|---|---|---|---|---|---|---|
| AI capability speed | 1.04 → 0.67 | 1.10 → 0.50 | 1.16 → 0.44 | 4% → 98% | 27% → 100% | 36% → 100% |
| **Future imaging utilization** | 0.92 → 1.12 | 0.88 → 1.30 | 0.83 → 1.46 | 40% → 11% | 92% → 12% | 97% → 12% |
| Assistive-AI time savings | 1.06 → 0.95 | 1.14 → 0.96 | 1.17 → 0.97 | 12% → 34% | 26% → 58% | 39% → 61% |
| **New imaging applications** | 0.99 → 1.06 | 1.01 → 1.12 | 1.03 → 1.15 | 23% → 15% | 47% → 29% | 54% → 39% |
| **Scanner throughput & capacity** | 0.98 → 1.04 | 1.01 → 1.08 | 1.03 → 1.11 | 26% → 16% | 48% → 35% | 54% → 45% |
| **Regulatory delay** | 1.00 → 1.02 | 1.03 → 1.09 | 1.05 → 1.13 | 22% → 17% | 44% → 32% | 51% → 41% |
| **AI-first / autonomous adoption** | 1.02 → 1.00 | 1.08 → 1.03 | 1.13 → 1.02 | 18% → 20% | 33% → 45% | 39% → 59% |
| Demographics | 1.00 → 1.02 | 1.03 → 1.08 | 1.04 → 1.13 | 21% → 18% | 43% → 33% | 54% → 41% |
| Price elasticity & pass-through | 1.00 → 1.03 | 1.04 → 1.08 | 1.06 → 1.11 | 22% → 16% | 42% → 34% | 50% → 44% |
| Today's shortage (2026 S/D) | 1.01 → 1.02 | 1.06 → 1.06 | 1.08 → 1.08 | 14% → 25% | 31% → 46% | 42% → 52% |
| Shortage-driven AI adoption | 1.02 → 1.00 | 1.06 → 1.06 | 1.08 → 1.08 | 18% → 20% | 39% → 38% | 48% → 47% |
| Attrition | 1.01 → 1.01 | 1.06 → 1.06 | 1.08 → 1.08 | 20% → 18% | 40% → 37% | 49% → 46% |
| Residency slot growth | 1.01 → 1.01 | 1.06 → 1.06 | 1.08 → 1.08 | 19% → 19% | 34% → 43% | 34% → 62% |
| **Residency adjustment** | 1.01 → 1.01 | 1.06 → 1.06 | 1.08 → 1.08 | 19% → 19% | 38% → 38% | 49% → 43% |
| *All assumptions at their sampled distributions (reference)* | 1.01 | 1.06 | 1.08 | 19% | 38% | 47% |

* **Future imaging utilization** is the most important named assumption. It moves the 2045 oversupply probability from
  92% to 12%.
* **AI capability speed** is the largest single driver, mostly through whether a world falls in the transformative branch.
* **AI-first adoption** and **regulatory delay** matter mainly after 2040.
* **New applications** and **scanner throughput** shift median demand by roughly ±5%–8%.
* **Residency adjustment** barely matters before 2045. New entrants are about 3% of the workforce a year and training takes
  six years, so the pipeline corrects slowly.

<a name="sec-eta"></a>
### 8.2 Variance-based sensitivity

The correlation ratio $\eta^2=\operatorname{Var}(E[Y\mid X])/\operatorname{Var}(Y)$ estimates first-order variance shares.
With correlated inputs it includes effects carried by correlated parameters.

![Figure 7. η² for the top parameters.](figures/fig07_eta2.png)

| Rank | Parameter | Evidence | η² demand 2035 | η² demand 2045 | η² demand 2055 | η² S/D 2045 | Spearman ρ (demand 2045) |
|---|---|---|---|---|---|---|---|
| 1 | AI progress speed (timeline multiplier M, incl. regime) (`ai_u`) | S | 0.58 | 0.59 | 0.55 | 0.56 | +0.42 |
| 2 | Per-capita (age/sex-adjusted) utilization growth, 2026 (`util_g0`) | S | 0.13 | 0.15 | 0.19 | 0.15 | +0.57 |
| 3 | Max time saved on interpretation by assistive AI (radiologist still reads) (`m_interp`) | A | 0.11 | 0.10 | 0.09 | 0.10 | -0.31 |
| 4 | Long-run per-capita utilization growth (asymptote) (`util_ginf`) | S | 0.07 | 0.10 | 0.16 | 0.10 | +0.47 |
| 5 | Max time saved on administrative work (protocoling, QA, scheduling) (`m_admin`) | A | 0.08 | 0.08 | 0.08 | 0.08 | -0.24 |
| 6 | Max time saved on clinical synthesis/consultation/communication (`m_consult`) | A | 0.08 | 0.08 | 0.07 | 0.07 | -0.23 |
| 7 | Max time saved on measurement & report drafting (`m_draft`) | A | 0.07 | 0.07 | 0.06 | 0.06 | -0.23 |
| 8 | Max time saved on physical/procedural work (`m_proc`) | S | 0.06 | 0.06 | 0.06 | 0.06 | -0.19 |
| 9 | Liability + reimbursement + scope-of-practice acceptance lag; tier-2 median (`lpay`) | A | 0.06 | 0.06 | 0.06 | 0.06 | +0.22 |
| 10 | AI-driven acquisition throughput gain at maturity (faster scans, auto-positioning) (`thru_H`) | A | 0.05 | 0.06 | 0.06 | 0.06 | -0.15 |

Excluding the transformative branch, per-capita utilization dominates:

| Rank | Parameter | Evidence | η² demand 2035 | η² demand 2045 | η² demand 2055 | η² S/D 2045 | Spearman ρ (demand 2045) |
|---|---|---|---|---|---|---|---|
| 1 | Per-capita (age/sex-adjusted) utilization growth, 2026 (`util_g0`) | S | 0.48 | 0.53 | 0.53 | 0.48 | +0.72 |
| 2 | Long-run per-capita utilization growth (asymptote) (`util_ginf`) | S | 0.25 | 0.36 | 0.46 | 0.34 | +0.59 |
| 3 | Growth in radiologist work per exam (complexity, images/study), 2026 (`cmplx_g0`) | A | 0.16 | 0.18 | 0.18 | 0.17 | +0.41 |
| 4 | AI-enabled utilization management (order decision support, payer AI prior auth) (`um_max`) | A | 0.12 | 0.11 | 0.11 | 0.10 | -0.32 |
| 5 | New AI-enabled imaging applications by 2066 (share of baseline work, before capacity limits) (`new_max`) | S | 0.05 | 0.07 | 0.06 | 0.07 | +0.25 |
| 6 | Max time saved on interpretation by assistive AI (radiologist still reads) (`m_interp`) | A | 0.08 | 0.06 | 0.04 | 0.05 | -0.23 |
| 7 | AI progress speed (timeline multiplier M, incl. regime) (`ai_u`) | S | 0.05 | 0.03 | 0.04 | 0.02 | +0.16 |
| 8 | Liability + reimbursement + scope-of-practice acceptance lag; tier-2 median (`lpay`) | A | 0.02 | 0.03 | 0.03 | 0.02 | +0.15 |

<a name="sec-evshare"></a>
### 8.3 How much of the uncertainty is subjective?

![Figure 12. Reduction in the 80% interval if each evidence class were known exactly.](figures/fig12_evidence.png)

Pinning all 34 subjective parameters at their medians narrows the 80% interval for 2045 demand by
69% and for the 2045 supply/demand ratio by 77%.
Pinning the anchored parameters narrows it by 1%. No sampled input is graded purely empirical
(the empirical anchors enter as fixed calibration targets without propagated uncertainty), so about half the spread comes from
purely subjective inputs and nearly all of it involves judgment.
Better measurement of the inputs graded empirical barely sharpens the demand range, although two measurable quantities,
today's per-person imaging growth and today's shortage, are large drivers of the oversupply probability and worth measuring
better. Note that this attribution measures the width of the demand interval, not the oversupply probability. What would
also sharpen it is information about AI, regulation and
future imaging use, which is why §9.3 is framed around signposts.

<a name="sec-robust"></a>
### 8.4 Beyond parameter uncertainty: alternative priors and model structures

A Monte Carlo simulation propagates uncertainty *within* a model. More simulations reduce numerical noise, but they cannot
correct errors shared by every simulated future, and possibilities the equations exclude contribute nothing. We therefore
separate three kinds of uncertainty:

1. **Numerical (Monte Carlo) error.** With 20,000 futures, the standard error of a probability near 30% is about
   0.3%. Negligible.
2. **Parameter uncertainty.** The distributions in Appendix A; everything in §7 reflects it.
3. **Choice of priors and of model structure.** Tested here.

**Alternative prior sets.** The same simulated futures are importance-reweighted so that the most consequential subjective
inputs follow different, separately motivated priors (effective sample sizes stay above 4,430). *AI-skeptical:* regime
weights 30/55/12/3, in the spirit of forecasting panels that put far lower odds on rapid transformative AI than AI-lab
leaders <a name="c32-2"></a><a name="c33-2"></a><sup>[32](#ref-32),[33](#ref-33)</sup>. *AI-bullish:* 5/35/30/30, closer to AI-lab leaders and the AI 2027 scenario <a name="c29-2"></a><a name="c30-3"></a><sup>[29](#ref-29),[30](#ref-30)</sup>. *Imaging restraint:* per-capita imaging growth centered on 0.3%/yr (Medicare cost pressure, appropriateness
rules) <a name="c94-2"></a><sup>[94](#ref-94)</sup>. *Imaging growth:* centered on 1.3%/yr, nearer recent CT growth <a name="c69-3"></a><a name="c78-2"></a><sup>[69](#ref-69),[78](#ref-78)</sup>.
Two *corner* sets change both at once (AI-skeptical with imaging growth; AI-bullish with imaging restraint), because
single changes understate how far the answer can move when assumptions err in the same direction.

**Alternative model structures.** The main model fixes several things by construction, so six alternatives are
re-simulated from the same draws:

* *No radiologist on AI-first reads:* in every tier, AI-first reads need no radiologist time at all (no audit or sign-off),
  rather than about a fifth of the usual time (2% in the transformative branch).
* *Tiers automated in any order:* capability dates are assigned to tiers at random in each future and regulatory lags are
  equal across tiers, so AI may master some complex CT tasks before simpler radiographs.
* *3× unforeseen new demand:* three times the new AI-enabled applications and twice the new radiologist tasks, standing in
  for channels such as image-derived biomarkers that are hard to forecast from current utilization.
* *Stronger payer pushback:* twice the AI-enabled utilization management and scope shift to other clinicians.
* *New uses not capped by scanners:* new AI-enabled uses (such as opportunistic screening of existing CTs) bypass the scanner and
  technologist capacity cap.
* *No shortage today:* supply ÷ demand in 2026 drawn from 0.95–1.03 instead of 0.85–0.99, since the main prior rules out a
  balanced market today.

**Counterfactuals: how much of the risk comes from AI?** Two further runs are not alternatives but decompositions: *no further
AI* (AI frozen at its 2026 level) and *assistive AI only* (no AI-first reading). Without further AI, meaningful oversupply has
probability 0.1% in 2035, 6% in
2045 and 18% in 2055, because supply grows faster than demand once the 2026
shortage is worked off. With assistive AI only it is 18%,
31% and 32%.
So near-term risk comes almost entirely from AI time savings; by 2055 about
37% of the risk would exist without further AI, and
AI-first reading adds most of the rest after 2045.

![Figure 14. P(meaningful oversupply) in 2035, 2045 and 2055 under alternative prior sets and model structures.](figures/fig14_robustness.png)

| Prior set or structure | P(oversupply) 2035 | P(oversupply) 2045 | P(oversupply) 2055 | P(Jevons) 2045 | Median demand 2045 |
|---|---|---|---|---|---|
| Prior: This site's assumptions | 20% | 39% | 48% | 4% | 1.05 |
| Prior: AI-skeptical | 11% | 31% | 41% | 4% | 1.08 |
| Prior: AI-bullish | 37% | 53% | 61% | 3% | 0.98 |
| Prior: Imaging restraint | 24% | 49% | 58% | 3% | 1.01 |
| Prior: Imaging growth | 14% | 23% | 29% | 4% | 1.17 |
| Prior: Both favorable: AI-skeptical + imaging growth | 5% | 15% | 21% | 5% | 1.21 |
| Prior: Both unfavorable: AI-bullish + imaging restraint | 41% | 61% | 69% | 2% | 0.93 |
| Structure: No radiologist on AI-first reads | 20% | 43% | 56% | 3% | 1.03 |
| Structure: Tiers automated in any order | 19% | 39% | 49% | 4% | 1.05 |
| Structure: 3× unforeseen new demand | 15% | 25% | 34% | 27% | 1.15 |
| Structure: Stronger payer pushback | 26% | 48% | 55% | 2% | 1.01 |
| Structure: New uses not capped by scanners | 18% | 36% | 45% | 8% | 1.07 |
| Structure: No shortage today | 33% | 51% | 54% | 4% | 1.05 |
| **Range across rows** | **5%–41%** | **15%–61%** | **21%–69%** | **2%–27%** | |
| Counterfactual: Assistive AI only (no AI-first reads) | 18% | 31% | 32% | 8% | 1.09 |
| Counterfactual: No further AI | <1% | 6% | 18% | 0% | 1.23 |

The qualitative conclusions survive every variant: oversupply risk is lower in 2035 than later and rises over a career,
and regulation and adoption lags matter. The quantitative ones do not: the 2045 oversupply probability spans
23%–53% across single changes and
15%–61% including the corners, driven mostly by the AI and imaging-growth
priors. The structural variants
move it less, except that the Jevons result is fragile: with three times the new demand, a true Jevons paradox occurs in
27% of futures in 2045. These bands are sensitivity ranges, not
confidence intervals; no variant was fitted to data, and others (a wage-and-hours labor market, regional markets) remain
untested. One structural feature deserves note: in the transformative branch, extra exams are capped by scanner and
technologist capacity while radiologist time per study falls by about 70% by 2045, so oversupply there is near-certain
and a Jevons outcome impossible by construction. The 2035 headline is therefore close to the transformative weight plus the
non-transformative risk (9%). Similarly, the collapse tail (demand below half of
today's) comes almost entirely from that 12% prior weight: outside the transformative branch, task ceilings keep 2045 demand
above 80% of today's in nearly every future. Finally, the capacity cap also limits new uses that need no extra scanner time
(such as opportunistic screening of existing CTs); exempting that channel raises P(Jevons, 2045) to
8% and lowers P(oversupply, 2045) to
36%.

---

<a name="sec-careers"></a>
## 9. What this means at different career stages

### 9.1 When you enter practice, and after

| Where you are in fall 2026 | Typical first attending year* | P(oversupply) when you start | 10 years in | 20 years in | 30 years in (or 2066) | P(demand below 2026) 10 years in | P(still a shortage) when you start |
|---|---|---|---|---|---|---|---|
| Pre-med (college junior) | 2038 | 28% | 42% | 49% | 49% (2066) | 38% | 47% |
| Medical student, year 1 | 2036 | 23% | 40% | 48% | 49% (2066) | 39% | 51% |
| Medical student, year 2 | 2035 | 20% | 39% | 48% | 49% (2065) | 39% | 55% |
| Medical student, year 3 | 2034 | 17% | 38% | 47% | 49% (2064) | 39% | 59% |
| Medical student, year 4 | 2033 | 14% | 36% | 46% | 50% (2063) | 40% | 64% |
| Intern (PGY-1) | 2032 | 11% | 35% | 46% | 50% (2062) | 40% | 71% |
| Radiology resident, R1 | 2031 | 7% | 33% | 45% | 50% (2061) | 41% | 79% |
| Radiology resident, R2 | 2030 | 3% | 31% | 44% | 50% (2060) | 42% | 86% |
| Radiology resident, R3 | 2029 | 1% | 30% | 43% | 49% (2059) | 43% | 93% |
| Radiology resident, R4 | 2028 | <1% | 28% | 42% | 49% (2058) | 44% | 98% |
| Fellow | 2027 | 0% | 25% | 41% | 49% (2057) | 45% | 100% |
| Practicing radiologist | 2026 | 0% | 23% | 40% | 48% (2056) | 46% | 100% |

\*Assumes a 1-year fellowship. "Oversupply" means more than 10% excess radiologist capacity nationally (a convention; §1).

* **Trainees finishing in the next five years** (current residents and fellows) enter a market that is most likely still
  short. The probability of meaningful oversupply is 3% in 2030.<sup>[§7.2](#sec-balance "Method / evidence for this claim")</sup>
* **Medical students and pre-meds** enter in the mid-to-late 2030s. They most likely enter a balanced or short market. Risk
  rises in the 2040s–2050s, in ordinary futures as well as the transformative-AI branch; the extreme outcomes (demand
  halving, layoffs) are almost entirely transformative.<sup>[§7.5](#sec-regimes "Method / evidence for this claim")</sup>
* **Everyone** should expect the job to change more than headcounts do: drafting, measurement and protocoling shrink, while
  consultation, procedures and AI oversight grow.<sup>[§7.6](#sec-tasks "Method / evidence for this claim")</sup>

<a name="sec-margins"></a>
### 9.2 Which margin does AI risk hit?

In order of likelihood:

1. **Task composition** (near-certain). See §7.6.
2. **Workload intensity.** In shortage worlds, productivity gains become more studies per hour rather than shorter days,
   consistent with rising volumes for the busiest radiologists <a name="c67-3"></a><sup>[67](#ref-67)</sup>.
3. **Hiring of new graduates.** In surplus worlds, the first adjustment is fewer openings and residency cuts, as in the
   mid-1990s and mid-2010s <a name="c4-4"></a><a name="c16-2"></a><sup>[4](#ref-4),[16](#ref-16)</sup>. In other AI-exposed occupations, early-career employment fell first
   while experienced workers were unaffected <a name="c71-2"></a><sup>[71](#ref-71)</sup>.
4. **Compensation.** Shortage-driven pay growth would likely flatten or reverse once the ratio exceeds 1, although
   reimbursement changes could pass part of the productivity gain to hospitals or insurers instead. If AI automates mostly the
   routine parts of the job, the remaining work becomes more expert, which tends to support pay but reduce headcount
   <a name="c26-2"></a><sup>[26](#ref-26)</sup>. Pay is not modeled explicitly.
5. **Pressure on practicing radiologists.** Demand falls faster than attrition in some five-year window after 2035 in
   9% of worlds, nearly all of them transformative. But
   because new graduates keep entering, a severe surplus ($R>1.25$) lasts five or more years in
   30% of worlds (21%
   outside the transformative branch). Who bears it, through pay, hours or jobs, is not modeled.

<a name="sec-signposts"></a>
### 9.3 What would make the forecast more optimistic or pessimistic

| If we observe… | Share of simulated worlds | P(oversupply) 2035 | P(oversupply) 2045 | P(oversupply) 2055 | Median demand 2045 |
|---|---|---|---|---|---|
| All simulated futures | 100% | 20% | 39% | 48% | 1.05 |
| AI saves >15% of radiologist time by 2031 | 20% | 69% | 77% | 81% | 0.62 |
| AI saves <5% of radiologist time by 2031 | 22% | 2% | 24% | 35% | 1.12 |
| >5% of interpretive work is AI-first/autonomous by 2033 | 16% | 66% | 76% | 79% | 0.60 |
| Autonomous reads paid for through tier 2 (all radiographs & screening) before 2035 | 21% | 58% | 72% | 75% | 0.75 |
| Autonomous reads not paid for through tier 2 until after 2045 | 25% | 4% | 22% | 31% | 1.13 |
| Per-capita imaging growth in the top third (≥0.9%/yr in 2026) | 33% | 12% | 16% | 22% | 1.19 |
| Per-capita imaging growth in the bottom third (≤0.3%/yr in 2026) | 33% | 32% | 68% | 76% | 0.94 |
| Many new AI-enabled imaging uses (top third)† | 33% | 28% | 39% | 47% | 1.07 |
| Few new AI-enabled imaging uses (bottom third)† | 33% | 15% | 42% | 52% | 1.03 |
| Transformative-AI regime | 12% | 98% | 100% | 100% | 0.50 |
| Any regime except transformative AI | 88% | 9% | 31% | 41% | 1.08 |

†Futures with many new AI uses are mostly fast-AI futures, where AI also saves more time, so they show *more* oversupply despite the extra imaging; these are signals, not levers.

* **Pessimistic signals:** prospective multi-site evidence of ≥15% real-world time savings from generative reporting by about
  2030; FDA authorization of autonomous reads for any U.S. exam class <a name="c12-4"></a><sup>[12](#ref-12)</sup>; payment for AI-only reads or liability
  safe harbors <a name="c62-3"></a><sup>[62](#ref-62)</sup>; per-capita imaging flattening as Medicare's trust fund nears depletion in 2033
  <a name="c94-3"></a><sup>[94](#ref-94)</sup>; DR positions passing about 1,400 a year; frontier AI reliably completing multi-day clinical reasoning
  tasks <a name="c29-3"></a><sup>[29](#ref-29)</sup>.
* **Optimistic signals:** real-world AI time savings staying in single digits <a name="c47-2"></a><a name="c49-2"></a><sup>[47](#ref-47),[49](#ref-49)</sup>; autonomous
  products stalling at FDA, liability or payment; continued strong CT growth <a name="c69-4"></a><sup>[69](#ref-69)</sup>; screening and opportunistic
  imaging scaling with radiologists in the loop <a name="c91-2"></a><a name="c92-2"></a><sup>[91](#ref-91),[92](#ref-92)</sup>; AI creating paid radiologist-led services.

---

<a name="sec-limits"></a>
## 10. Limitations

* **National aggregate.** The model has no geography, subspecialty mix, practice type or teleradiology. The shortage is local
  and uneven <a name="c67-4"></a><a name="c79-8"></a><sup>[67](#ref-67),[79](#ref-79)</sup>.
* **No wage, hours or reimbursement equilibrium.** $R$ is a pressure indicator, not an unemployment rate. A 30% productivity
  gain could show up as fewer hires, shorter hours, lower pay, shorter backlogs or lower prices; the model does not choose
  among these, and statements about pay and hiring are interpretations.
* **The starting point is a judgment.** The 2026 ratio (median 0.93) is inferred from pay, vacancies, workload and workforce
  projections, not measured. The model has not been shown to reproduce 2015–2026 exam volumes, work RVUs and workforce counts;
  doing so would strengthen the baseline. A milder starting shortage (0.96) raises the 2045 oversupply probability from about
  39% to 46%.
* **Structure is only partly tested.** §8.4 tests six alternative structures; others are untested.
* **The shortage feedback is a one-step approximation** of a coupled system, with a subjective strength.
* **The regimes are coarse.** The transformative branch is a stylization of a world far stranger than any parameter change
  can capture.
* **Subjective parameters dominate the spread** (§8.3).
* **Data definitions differ** (Medicare-enrolled radiologists vs AAMC counts; exams vs RVUs).
* **Limited validation.** The 2016→2025 backtest (§6.2) covers four cases over nine years with a simplified version of the
  method; the forecast runs 40 years. Several start dates, a larger reference class and prospectively recorded forecasts
  would be stronger.
* **Recent sources.** Several key sources are preprints, conference results or trade-press summaries. Some JACR figures come
  from abstracts.

<a name="sec-repro"></a>
## 11. Reproducibility

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run_model.py          # 20,000 simulations + sensitivity; writes outputs/, figures/, docs/data/
python -m pytest             # calibration, accounting, copula, feedback and reference tests
python tools/build_docs.py   # regenerates REPORT.md and docs/report.html
```

**Version history.** v1.0 (October 2026): initial model. v1.1 (October 2026): 2024–2026 evidence review (§3); tier-1/2
autonomy shares recalibrated to autonomous chest-radiograph and mammography evidence; per-capita utilization raised to
1.2%/yr; shortage-driven adoption feedback; AMA-standardized references with links and back-links; neutral career-stage
framing. v1.2 (October 2026): 2016→2025 backtest against BLS projections and trends for radiology, software developers,
translators and medical transcriptionists (§6.2); comparison of forecasting approaches (§2.1); supply shown in units of 2026
demand; axis titles on all figures; citation pop-overs with source passages on the website. v1.3 (October 2026): per-person
imaging growth recentered from 1.2% to 0.6%/yr after benchmarking against national claims-based projections (§4.1, §6.1);
alternative prior sets, corner combinations and alternative model structures (§8.4); three kinds of uncertainty separated;
backtest compared with forecast combination alone (§6.2); sustained-surplus metric; today's shortage regraded subjective;
oversupply threshold described as a convention.


<a name="references"></a>

## References

*AMA Manual of Style, 11th edition. ↩ links return to each place a source is cited.*

1. <a name="ref-1"></a>Christensen EW, Parikh JR, Drake AR, Rubin EM, Rula EY. Projected US radiologist supply, 2025 to 2055. *J Am Coll Radiol*. 2025;22(2):161-169. doi:[10.1016/j.jacr.2024.10.019](https://doi.org/10.1016/j.jacr.2024.10.019) [↩a](#c1-1) [↩b](#c1-2) [↩c](#c1-3) [↩d](#c1-4) [↩e](#c1-5) [↩f](#c1-6)
2. <a name="ref-2"></a>Association of American Medical Colleges. Active physicians in the largest specialties, 2024. *AAMC Physician Specialty Data Report*. Accessed October 7, 2026. [https://www.aamc.org/data-reports/workforce/data/active-physicians-largest-specialties-2024](https://www.aamc.org/data-reports/workforce/data/active-physicians-largest-specialties-2024) [↩](#c2-1)
3. <a name="ref-3"></a>Sharafinski ME Jr, Nussbaum D, Jha S. Supply/demand in radiology: a historical perspective and comparison to other labor markets. *Acad Radiol*. 2016;23(2):245-251. doi:[10.1016/j.acra.2015.10.009](https://doi.org/10.1016/j.acra.2015.10.009) [↩a](#c3-1) [↩b](#c3-2) [↩c](#c3-3) [↩d](#c3-4) [↩e](#c3-5) [↩f](#c3-6)
4. <a name="ref-4"></a>Shi J. May the Match be ever in your favor. *Diagnostic Imaging*. Published May 7, 2015. Accessed October 7, 2026. [https://www.diagnosticimaging.com/view/may-match-be-ever-your-favor](https://www.diagnosticimaging.com/view/may-match-be-ever-your-favor) [↩a](#c4-1) [↩b](#c4-2) [↩c](#c4-3) [↩d](#c4-4) [↩e](#c4-5)
5. <a name="ref-5"></a>Tetlock PE, Gardner D. *Superforecasting: The Art and Science of Prediction*. Crown; 2015. Accessed October 7, 2026. [https://www.penguinrandomhouse.com/books/227815/superforecasting-by-philip-e-tetlock-and-dan-gardner/](https://www.penguinrandomhouse.com/books/227815/superforecasting-by-philip-e-tetlock-and-dan-gardner/) [↩a](#c5-1) [↩b](#c5-2)
6. <a name="ref-6"></a>Mellers B, Ungar L, Baron J, et al. Psychological strategies for winning a geopolitical forecasting tournament. *Psychol Sci*. 2014;25(5):1106-1115. doi:[10.1177/0956797614524255](https://doi.org/10.1177/0956797614524255) [↩a](#c6-1) [↩b](#c6-2)
7. <a name="ref-7"></a>Kahneman D, Lovallo D. Timid choices and bold forecasts: a cognitive perspective on risk taking. *Manage Sci*. 1993;39(1):17-31. doi:[10.1287/mnsc.39.1.17](https://doi.org/10.1287/mnsc.39.1.17) [↩a](#c7-1) [↩b](#c7-2)
8. <a name="ref-8"></a>Metaculus. Track record. *Metaculus*. Accessed October 7, 2026. [https://www.metaculus.com/questions/track-record/](https://www.metaculus.com/questions/track-record/) [↩a](#c8-1) [↩b](#c8-2)
9. <a name="ref-9"></a>Hinton G. Geoff Hinton: on radiology. Presented at: Machine Learning and the Market for Intelligence; 2016; Toronto, Ontario, Canada. *Creative Destruction Lab YouTube channel*. Published November 24, 2016. Accessed October 7, 2026. [https://www.youtube.com/watch?v=2HMPRXstSvQ](https://www.youtube.com/watch?v=2HMPRXstSvQ) [↩a](#c9-1) [↩b](#c9-2)
10. <a name="ref-10"></a>Match Day 2026: radiology programs offer more positions than ever, but applicant pool declines. *Radiology Business*. Published March 20, 2026. Accessed October 7, 2026. [https://radiologybusiness.com/topics/healthcare-management/healthcare-staffing/match-day-2026-radiology-programs-offer-more-positions-ever-applicant-pool-declines](https://radiologybusiness.com/topics/healthcare-management/healthcare-staffing/match-day-2026-radiology-programs-offer-more-positions-ever-applicant-pool-declines) [↩a](#c10-1) [↩b](#c10-2) [↩c](#c10-3) [↩d](#c10-4) [↩e](#c10-5)
11. <a name="ref-11"></a>Radiology among top specialties for pay, compensation growth. *AuntMinnie*. Published August 2026. Accessed October 7, 2026. [https://www.auntminnie.com/practice-management/news/15822383/radiology-among-top-specialties-for-pay-compensation-growth](https://www.auntminnie.com/practice-management/news/15822383/radiology-among-top-specialties-for-pay-compensation-growth) [↩a](#c11-1) [↩b](#c11-2)
12. <a name="ref-12"></a>US Food and Drug Administration. Artificial intelligence-enabled medical devices. *FDA*. Updated September 2026. Accessed October 7, 2026. [https://www.fda.gov/medical-devices/digital-health-center-excellence/artificial-intelligence-enabled-medical-devices](https://www.fda.gov/medical-devices/digital-health-center-excellence/artificial-intelligence-enabled-medical-devices) [↩a](#c12-1) [↩b](#c12-2) [↩c](#c12-3) [↩d](#c12-4) [↩e](#c12-5) [↩f](#c12-6)
13. <a name="ref-13"></a>Wu K, Wu E, Theodorou B, et al. Characterizing the clinical adoption of medical AI devices through U.S. insurance claims. *NEJM AI*. 2024;1(1). doi:[10.1056/AIoa2300030](https://doi.org/10.1056/AIoa2300030) [↩a](#c13-1) [↩b](#c13-2) [↩c](#c13-3)
14. <a name="ref-14"></a>Langlotz CP. Will artificial intelligence replace radiologists? *Radiol Artif Intell*. 2019;1(3):e190058. doi:[10.1148/ryai.2019190058](https://doi.org/10.1148/ryai.2019190058) [↩](#c14-1)
15. <a name="ref-15"></a>Mousa D. AI isn't replacing radiologists. *Works in Progress*. Published September 2025. Accessed October 7, 2026. [https://www.worksinprogress.news/p/why-ai-isnt-replacing-radiologists](https://www.worksinprogress.news/p/why-ai-isnt-replacing-radiologists) [↩a](#c15-1) [↩b](#c15-2)
16. <a name="ref-16"></a>Rosenkrantz AB, Hughes DR, Duszak R Jr. The U.S. radiologist workforce: an analysis of temporal and geographic variation by using large national datasets. *Radiology*. 2016;279(1):175-184. doi:[10.1148/radiol.2015150921](https://doi.org/10.1148/radiol.2015150921) [↩a](#c16-1) [↩b](#c16-2) [↩c](#c16-3)
17. <a name="ref-17"></a>Nicholson S. Physician specialty choice under uncertainty. *J Labor Econ*. 2002;20(4):816-847. doi:[10.1086/342039](https://doi.org/10.1086/342039) [↩a](#c17-1) [↩b](#c17-2)
18. <a name="ref-18"></a>Reeder K, Lee H. Impact of artificial intelligence on US medical students' choice of radiology. *Clin Imaging*. 2022;81:67-71. doi:[10.1016/j.clinimag.2021.09.018](https://doi.org/10.1016/j.clinimag.2021.09.018) [↩a](#c18-1) [↩b](#c18-2)
19. <a name="ref-19"></a>Lehman CD, Wellman RD, Buist DSM, Kerlikowske K, Tosteson ANA, Miglioretti DL; Breast Cancer Surveillance Consortium. Diagnostic accuracy of digital screening mammography with and without computer-aided detection. *JAMA Intern Med*. 2015;175(11):1828-1837. doi:[10.1001/jamainternmed.2015.5231](https://doi.org/10.1001/jamainternmed.2015.5231) [↩a](#c19-1) [↩b](#c19-2) [↩c](#c19-3) [↩d](#c19-4)
20. <a name="ref-20"></a>Adler-Milstein J, Jha AK. HITECH Act drove large gains in hospital electronic health record adoption. *Health Aff (Millwood)*. 2017;36(8):1416-1422. doi:[10.1377/hlthaff.2016.1651](https://doi.org/10.1377/hlthaff.2016.1651) [↩a](#c20-1) [↩b](#c20-2) [↩c](#c20-3)
21. <a name="ref-21"></a>Abràmoff MD, Lavin PT, Birch M, Shah N, Folk JC. Pivotal trial of an autonomous AI-based diagnostic system for detection of diabetic retinopathy in primary care offices. *NPJ Digit Med*. 2018;1:39. doi:[10.1038/s41746-018-0040-6](https://doi.org/10.1038/s41746-018-0040-6) [↩a](#c21-1) [↩b](#c21-2) [↩c](#c21-3) [↩d](#c21-4)
22. <a name="ref-22"></a>Acemoglu D, Restrepo P. The race between man and machine: implications of technology for growth, factor shares, and employment. *Am Econ Rev*. 2018;108(6):1488-1542. doi:[10.1257/aer.20160696](https://doi.org/10.1257/aer.20160696) [↩](#c22-1)
23. <a name="ref-23"></a>Acemoglu D, Restrepo P. Automation and new tasks: how technology displaces and reinstates labor. *J Econ Perspect*. 2019;33(2):3-30. doi:[10.1257/jep.33.2.3](https://doi.org/10.1257/jep.33.2.3) [↩a](#c23-1) [↩b](#c23-2) [↩c](#c23-3) [↩d](#c23-4) [↩e](#c23-5)
24. <a name="ref-24"></a>Bessen J. Automation and jobs: when technology boosts employment. *Econ Policy*. 2019;34(100):589-626. doi:[10.1093/epolic/eiaa001](https://doi.org/10.1093/epolic/eiaa001) [↩a](#c24-1) [↩b](#c24-2)
25. <a name="ref-25"></a>Autor D, Chin C, Salomons A, Seegmiller B. New frontiers: the origins and content of new work, 1940-2018. *Q J Econ*. 2024;139(3):1399-1465. doi:[10.1093/qje/qjae008](https://doi.org/10.1093/qje/qjae008) [↩a](#c25-1) [↩b](#c25-2) [↩c](#c25-3) [↩d](#c25-4)
26. <a name="ref-26"></a>Autor D, Thompson N. Expertise. *J Eur Econ Assoc*. 2025;23(4):1203-1271. doi:[10.1093/jeea/jvaf023](https://doi.org/10.1093/jeea/jvaf023) [↩a](#c26-1) [↩b](#c26-2)
27. <a name="ref-27"></a>Jevons WS. *The Coal Question: An Inquiry Concerning the Progress of the Nation, and the Probable Exhaustion of Our Coal-Mines*. Macmillan and Co; 1865. Accessed October 7, 2026. [https://archive.org/details/coalquestionani00jevogoog](https://archive.org/details/coalquestionani00jevogoog) [↩](#c27-1)
28. <a name="ref-28"></a>Kwa T, West B, Becker J, et al. Measuring AI ability to complete long tasks. *arXiv*. Preprint posted online March 18, 2025. doi:[10.48550/arXiv.2503.14499](https://doi.org/10.48550/arXiv.2503.14499) [↩a](#c28-1) [↩b](#c28-2)
29. <a name="ref-29"></a>METR. Time horizon 1.1 and the limitations of time-horizon measurements. *METR Notes*. Published January 22, 2026. Accessed October 7, 2026. [https://metr.org/notes/2026-01-22-time-horizon-limitations/](https://metr.org/notes/2026-01-22-time-horizon-limitations/) [↩a](#c29-1) [↩b](#c29-2) [↩c](#c29-3) [↩d](#c29-4)
30. <a name="ref-30"></a>Kokotajlo D, Alexander S, Larsen T, Lifland E, Dean R. AI 2027. *AI Futures Project*. Published April 3, 2025. Accessed October 7, 2026. [https://ai-2027.com](https://ai-2027.com) [↩a](#c30-1) [↩b](#c30-2) [↩c](#c30-3) [↩d](#c30-4)
31. <a name="ref-31"></a>Grace K, Sandkühler JF, Stewart H, et al. Thousands of AI authors on the future of AI. *J Artif Intell Res*. 2025;84. doi:[10.1613/jair.1.19087](https://doi.org/10.1613/jair.1.19087) [↩a](#c31-1) [↩b](#c31-2)
32. <a name="ref-32"></a>Forecasting Research Institute. Introducing LEAP: the Longitudinal Expert AI Panel. *Forecasting Research Institute Substack*. Published November 2025. Accessed October 7, 2026. [https://forecastingresearch.substack.com/p/introducing-leap](https://forecastingresearch.substack.com/p/introducing-leap) [↩a](#c32-1) [↩b](#c32-2) [↩c](#c32-3)
33. <a name="ref-33"></a>Karger E, Rosenberg J, Jacobs Z, et al. Forecasting existential risk: evidence from a long-run forecasting tournament. Forecasting Research Institute Working Paper 1. Forecasting Research Institute; 2023. Accessed October 7, 2026. [https://forecastingresearch.org/xpt](https://forecastingresearch.org/xpt) [↩a](#c33-1) [↩b](#c33-2) [↩c](#c33-3)
34. <a name="ref-34"></a>Tetlock PE. *Expert Political Judgment: How Good Is It? How Can We Know?*. Princeton University Press; 2005. doi:[10.1515/9781400830312](https://doi.org/10.1515/9781400830312) [↩](#c34-1)
35. <a name="ref-35"></a>Arrow KJ, Forsythe R, Gorham M, et al. The promise of prediction markets. *Science*. 2008;320(5878):877-878. doi:[10.1126/science.1157679](https://doi.org/10.1126/science.1157679) [↩](#c35-1)
36. <a name="ref-36"></a>Forecasting Research Institute. What did forecasters get right and wrong in the largest existential risk forecasting tournament? *Forecasting Research Institute Substack*. Published 2025. Accessed October 7, 2026. [https://forecastingresearch.substack.com/p/what-did-forecasters-get-right-and](https://forecastingresearch.substack.com/p/what-did-forecasters-get-right-and) [↩](#c36-1)
37. <a name="ref-37"></a>Makridakis S, Spiliotis E, Assimakopoulos V. The M4 Competition: 100,000 time series and 61 forecasting methods. *Int J Forecast*. 2020;36(1):54-74. doi:[10.1016/j.ijforecast.2019.04.014](https://doi.org/10.1016/j.ijforecast.2019.04.014) [↩a](#c37-1) [↩b](#c37-2)
38. <a name="ref-38"></a>US Bureau of Labor Statistics. Medical transcriptionists. *Occupational Outlook Handbook, 2008-09 Edition (archived May 11, 2008)*. Accessed October 7, 2026. [http://web.archive.org/web/20080511153519/http://www.bls.gov/oco/ocos271.htm](http://web.archive.org/web/20080511153519/http://www.bls.gov/oco/ocos271.htm) [↩a](#c38-1) [↩b](#c38-2)
39. <a name="ref-39"></a>US Bureau of Labor Statistics. Medical transcriptionists (2016-26 projections). *Occupational Outlook Handbook, 2018-19 Edition (archived June 2018)*. Accessed October 7, 2026. [http://web.archive.org/web/20180615000000/https://www.bls.gov/ooh/healthcare/medical-transcriptionists.htm](http://web.archive.org/web/20180615000000/https://www.bls.gov/ooh/healthcare/medical-transcriptionists.htm) [↩a](#c39-1) [↩b](#c39-2) [↩c](#c39-3)
40. <a name="ref-40"></a>Frey CB, Osborne MA. The future of employment: how susceptible are jobs to computerisation? Working paper. Oxford Martin School, University of Oxford; September 17, 2013. Accessed October 7, 2026. [https://www.oxfordmartin.ox.ac.uk/downloads/academic/The_Future_of_Employment.pdf](https://www.oxfordmartin.ox.ac.uk/downloads/academic/The_Future_of_Employment.pdf) [↩a](#c40-1) [↩b](#c40-2)
41. <a name="ref-41"></a>Eloundou T, Manning S, Mishkin P, Rock D. GPTs are GPTs: labor market impact potential of LLMs. *Science*. 2024;384(6702):1306-1308. doi:[10.1126/science.adj0998](https://doi.org/10.1126/science.adj0998) [↩a](#c41-1) [↩b](#c41-2)
42. <a name="ref-42"></a>Clemen RT. Combining forecasts: a review and annotated bibliography. *Int J Forecast*. 1989;5(4):559-583. doi:[10.1016/0169-2070(89)90012-5](https://doi.org/10.1016/0169-2070(89)90012-5) [↩a](#c42-1) [↩b](#c42-2)
43. <a name="ref-43"></a>Rajpurkar P, Lungren MP. The current and future state of AI interpretation of medical images. *N Engl J Med*. 2023;388(21):1981-1990. doi:[10.1056/NEJMra2301725](https://doi.org/10.1056/NEJMra2301725) [↩a](#c43-1) [↩b](#c43-2)
44. <a name="ref-44"></a>Huang J, Wittbrodt MT, Teague CN, et al. Efficiency and quality of generative AI-assisted radiograph reporting. *JAMA Netw Open*. 2025;8(6):e2513921. doi:[10.1001/jamanetworkopen.2025.13921](https://doi.org/10.1001/jamanetworkopen.2025.13921) [↩a](#c44-1) [↩b](#c44-2) [↩c](#c44-3)
45. <a name="ref-45"></a>Hong EK, Roh B, Park B, et al. Value of using a generative AI model in chest radiography reporting: a reader study. *Radiology*. 2025;314(3):e241646. doi:[10.1148/radiol.241646](https://doi.org/10.1148/radiol.241646) [↩a](#c45-1) [↩b](#c45-2) [↩c](#c45-3) [↩d](#c45-4)
46. <a name="ref-46"></a>Li M, Wang Y, Miao Z, et al. Fine-tuned large language model for automated radiology impression generation: a multicenter evaluation. *Radiol Artif Intell*. 2026;8(3):e250714. doi:[10.1148/ryai.250714](https://doi.org/10.1148/ryai.250714) [↩a](#c46-1) [↩b](#c46-2)
47. <a name="ref-47"></a>Liu W, Wu Y, Yu W, Bittle MJ, Zheng Z, Kharrazi H. Measuring the impact of AI on report-drafting efficiency in chest computed tomography interpretation: retrospective analysis. *J Med Internet Res*. 2026;28:e77967. doi:[10.2196/77967](https://doi.org/10.2196/77967) [↩a](#c47-1) [↩b](#c47-2) [↩c](#c47-3)
48. <a name="ref-48"></a>Tanno R, Barrett DGT, Sellergren A, et al. Collaboration between clinicians and vision-language models in radiology report generation. *Nat Med*. 2025;31(2):599-608. doi:[10.1038/s41591-024-03302-1](https://doi.org/10.1038/s41591-024-03302-1) [↩a](#c48-1) [↩b](#c48-2) [↩c](#c48-3)
49. <a name="ref-49"></a>Wenderott K, Krups J, Zaruchas F, Weigl M. Effects of artificial intelligence implementation on efficiency in medical imaging-a systematic literature review and meta-analysis. *NPJ Digit Med*. 2024;7(1):265. doi:[10.1038/s41746-024-01248-9](https://doi.org/10.1038/s41746-024-01248-9) [↩a](#c49-1) [↩b](#c49-2) [↩c](#c49-3)
50. <a name="ref-50"></a>Yu F, Moehring A, Banerjee O, Salz T, Agarwal N, Rajpurkar P. Heterogeneity and predictors of the effects of AI assistance on radiologists. *Nat Med*. 2024;30(3):837-849. doi:[10.1038/s41591-024-02850-w](https://doi.org/10.1038/s41591-024-02850-w) [↩a](#c50-1) [↩b](#c50-2) [↩c](#c50-3)
51. <a name="ref-51"></a>Lauritzen AD, Lillholm M, Lynge E, Nielsen M, Karssemeijer N, Vejborg I. Early indicators of the impact of using AI in mammography screening for breast cancer. *Radiology*. 2024;311(3):e232479. doi:[10.1148/radiol.232479](https://doi.org/10.1148/radiol.232479) [↩a](#c51-1) [↩b](#c51-2)
52. <a name="ref-52"></a>Lång K, Josefsson V, Larsson AM, et al. Artificial intelligence-supported screen reading versus standard double reading in the Mammography Screening with Artificial Intelligence trial (MASAI): a clinical safety analysis of a randomised, controlled, non-inferiority, single-blinded, screening accuracy study. *Lancet Oncol*. 2023;24(8):936-944. doi:[10.1016/S1470-2045(23)00298-X](https://doi.org/10.1016/S1470-2045(23)00298-X) [↩a](#c52-1) [↩b](#c52-2)
53. <a name="ref-53"></a>Hernström V, Josefsson V, Sartor H, et al. Screening performance and characteristics of breast cancer detected in the Mammography Screening with Artificial Intelligence trial (MASAI): a randomised, controlled, parallel-group, non-inferiority, single-blinded, screening accuracy study. *Lancet Digit Health*. 2025;7(3):e175-e183. doi:[10.1016/S2589-7500(24)00267-X](https://doi.org/10.1016/S2589-7500(24)00267-X) [↩a](#c53-1) [↩b](#c53-2) [↩c](#c53-3) [↩d](#c53-4)
54. <a name="ref-54"></a>Gommers J, Hernström V, Josefsson V, et al. Interval cancer, sensitivity, and specificity comparing AI-supported mammography screening with standard double reading without AI in the MASAI study: a randomised, controlled, non-inferiority, single-blinded, population-based, screening-accuracy trial. *Lancet*. 2026;407(10527):505-514. doi:[10.1016/S0140-6736(25)02464-X](https://doi.org/10.1016/S0140-6736(25)02464-X) [↩a](#c54-1) [↩b](#c54-2) [↩c](#c54-3) [↩d](#c54-4)
55. <a name="ref-55"></a>Plesner LL, Müller FC, Nybing JD, et al. Autonomous chest radiograph reporting using AI: estimation of clinical impact. *Radiology*. 2023;307(3):e222268. doi:[10.1148/radiol.222268](https://doi.org/10.1148/radiol.222268) [↩a](#c55-1) [↩b](#c55-2)
56. <a name="ref-56"></a>Plesner LL, Müller FC, Brejnebøl MW, et al. Using AI to identify unremarkable chest radiographs for automatic reporting. *Radiology*. 2024;312(2):e240272. doi:[10.1148/radiol.240272](https://doi.org/10.1148/radiol.240272) [↩a](#c56-1) [↩b](#c56-2)
57. <a name="ref-57"></a>Oxipit. CE mark for first autonomous AI medical imaging application. *Oxipit News*. Published 2022. Accessed October 7, 2026. [https://oxipit.ai/news/first-autonomous-ai-medical-imaging-application/](https://oxipit.ai/news/first-autonomous-ai-medical-imaging-application/) [↩a](#c57-1) [↩b](#c57-2) [↩c](#c57-3)
58. <a name="ref-58"></a>Aidoc's chest X-ray reporting tool earns FDA Breakthrough Device designation. *Radiology Business*. Published June 2026. Accessed October 7, 2026. [https://radiologybusiness.com/topics/healthcare-management/healthcare-policy/aidocs-chest-x-ray-reporting-tool-earns-fda-breakthrough-device-designation](https://radiologybusiness.com/topics/healthcare-management/healthcare-policy/aidocs-chest-x-ray-reporting-tool-earns-fda-breakthrough-device-designation) [↩a](#c58-1) [↩b](#c58-2) [↩c](#c58-3)
59. <a name="ref-59"></a>DeepHealth gets FDA nod for AI tool that reads ultrasounds, creates reports. *Healthcare Dive*. Published July 2026. Accessed October 7, 2026. [https://www.healthcaredive.com/news/deephealth-gets-fda-nod-for-ai-tool-that-reads-ultrasounds-creates-reports/827093/](https://www.healthcaredive.com/news/deephealth-gets-fda-nod-for-ai-tool-that-reads-ultrasounds-creates-reports/827093/) [↩a](#c59-1) [↩b](#c59-2)
60. <a name="ref-60"></a>US Food and Drug Administration. *Artificial Intelligence-Enabled Device Software Functions: Lifecycle Management and Marketing Submission Recommendations. Draft Guidance for Industry and Food and Drug Administration Staff*. US Food and Drug Administration; January 7, 2025. Accessed October 7, 2026. [https://www.fda.gov/regulatory-information/search-fda-guidance-documents/artificial-intelligence-enabled-device-software-functions-lifecycle-management-and-marketing](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/artificial-intelligence-enabled-device-software-functions-lifecycle-management-and-marketing) [↩a](#c60-1) [↩b](#c60-2)
61. <a name="ref-61"></a>Chouffani El Fassi S, Abdullah A, Fang Y, et al. Not all AI health tools with regulatory authorization are clinically validated. *Nat Med*. 2024;30(10):2718-2720. doi:[10.1038/s41591-024-03203-3](https://doi.org/10.1038/s41591-024-03203-3) [↩a](#c61-1) [↩b](#c61-2) [↩c](#c61-3)
62. <a name="ref-62"></a>Mello MM, Guha N. Understanding liability risk from using health care artificial intelligence tools. *N Engl J Med*. 2024;390(3):271-278. doi:[10.1056/NEJMhle2308901](https://doi.org/10.1056/NEJMhle2308901) [↩a](#c62-1) [↩b](#c62-2) [↩c](#c62-3) [↩d](#c62-4)
63. <a name="ref-63"></a>Bernstein MH, Sheppard B, Bruno MA, Lay PS, Baird GL. Randomized study of the impact of AI on perceived legal liability for radiologists. *NEJM AI*. 2025;2(6). doi:[10.1056/AIoa2400785](https://doi.org/10.1056/AIoa2400785) [↩a](#c63-1) [↩b](#c63-2) [↩c](#c63-3)
64. <a name="ref-64"></a>Allen B, Agarwal S, Coombs L, Wald C, Dreyer K. 2020 ACR Data Science Institute artificial intelligence survey. *J Am Coll Radiol*. 2021;18(8):1153-1159. doi:[10.1016/j.jacr.2021.04.002](https://doi.org/10.1016/j.jacr.2021.04.002) [↩a](#c64-1) [↩b](#c64-2)
65. <a name="ref-65"></a>Royal College of Radiologists. *Clinical Radiology Workforce Census 2025*. Royal College of Radiologists; 2026. Accessed October 7, 2026. [https://www.rcr.ac.uk/media/n1fjvrv4/rcr-2025-clinical-radiology-workforce-census-report.pdf](https://www.rcr.ac.uk/media/n1fjvrv4/rcr-2025-clinical-radiology-workforce-census-report.pdf) [↩a](#c65-1) [↩b](#c65-2) [↩c](#c65-3)
66. <a name="ref-66"></a>Liu H, Ding N, Li X, et al. Artificial intelligence and radiologist burnout. *JAMA Netw Open*. 2024;7(11):e2448714. doi:[10.1001/jamanetworkopen.2024.48714](https://doi.org/10.1001/jamanetworkopen.2024.48714) [↩](#c66-1)
67. <a name="ref-67"></a>Zamani H, Fruscello T, Burleson J, Bhargavan-Chatfield M, Davenport MS. US radiology imaging and workforce volumes 2017-2024: an analysis of 46.4 million imaging examinations from 167 radiology facilities. *J Am Coll Radiol*. 2026;23(6):1041-1048. doi:[10.1016/j.jacr.2025.12.026](https://doi.org/10.1016/j.jacr.2025.12.026) [↩a](#c67-1) [↩b](#c67-2) [↩c](#c67-3) [↩d](#c67-4) [↩e](#c67-5)
68. <a name="ref-68"></a>Parikh JR, Drake AR, Rula EY, Golding E, Christensen EW. Radiologist turnover in the United States. *J Am Coll Radiol*. 2026;23(6):1058-1066. doi:[10.1016/j.jacr.2026.01.009](https://doi.org/10.1016/j.jacr.2026.01.009) [↩a](#c68-1) [↩b](#c68-2) [↩c](#c68-3) [↩d](#c68-4) [↩e](#c68-5)
69. <a name="ref-69"></a>Rosenkrantz AB, Cummings RW. Utilization of emergency department imaging from 2013 to 2023: a national Medicare analysis. *Radiology*. 2025;316(3):e251395. doi:[10.1148/radiol.251395](https://doi.org/10.1148/radiol.251395) [↩a](#c69-1) [↩b](#c69-2) [↩c](#c69-3) [↩d](#c69-4) [↩e](#c69-5)
70. <a name="ref-70"></a>Kwee TC, Kwee RM. Workload of diagnostic radiologists in the foreseeable future based on recent (2024) scientific advances: updated growth expectations. *Eur J Radiol*. 2025;187:112103. doi:[10.1016/j.ejrad.2025.112103](https://doi.org/10.1016/j.ejrad.2025.112103) [↩a](#c70-1) [↩b](#c70-2) [↩c](#c70-3) [↩d](#c70-4) [↩e](#c70-5)
71. <a name="ref-71"></a>Brynjolfsson E, Chandar B, Chen R. Canaries in the coal mine? Six facts about the recent employment effects of artificial intelligence. Working paper. Stanford Digital Economy Lab; November 2025. Accessed October 7, 2026. [https://digitaleconomy.stanford.edu/app/uploads/2025/11/CanariesintheCoalMine_Nov25.pdf](https://digitaleconomy.stanford.edu/app/uploads/2025/11/CanariesintheCoalMine_Nov25.pdf) [↩a](#c71-1) [↩b](#c71-2)
72. <a name="ref-72"></a>Humlum A, Vestergaard E. Large language models, small labor market effects. NBER Working Paper 33777. National Bureau of Economic Research; 2025. doi:[10.3386/w33777](https://doi.org/10.3386/w33777) [↩a](#c72-1) [↩b](#c72-2) [↩c](#c72-3)
73. <a name="ref-73"></a>Brynjolfsson E, Li D, Raymond L. Generative AI at work. *Q J Econ*. 2025;140(2):889-942. doi:[10.1093/qje/qjae044](https://doi.org/10.1093/qje/qjae044) [↩](#c73-1)
74. <a name="ref-74"></a>Acemoglu D. The simple macroeconomics of AI. *Econ Policy*. 2025;40(121):13-58. doi:[10.1093/epolic/eiae042](https://doi.org/10.1093/epolic/eiae042) [↩](#c74-1)
75. <a name="ref-75"></a>Christensen EW, Drake AR, Parikh JR, Rubin EM, Rula EY. Projected US imaging utilization, 2025 to 2055. *J Am Coll Radiol*. 2025;22(2):151-158. doi:[10.1016/j.jacr.2024.10.017](https://doi.org/10.1016/j.jacr.2024.10.017) [↩a](#c75-1) [↩b](#c75-2) [↩c](#c75-3) [↩d](#c75-4) [↩e](#c75-5) [↩f](#c75-6) [↩g](#c75-7)
76. <a name="ref-76"></a>Congressional Budget Office. *The Demographic Outlook: 2026 to 2056*. Publication 61879. Congressional Budget Office; January 2026. Accessed October 7, 2026. [https://www.cbo.gov/publication/61879](https://www.cbo.gov/publication/61879) [↩a](#c76-1) [↩b](#c76-2) [↩c](#c76-3)
77. <a name="ref-77"></a>Smith-Bindman R, Kwan ML, Marlow EC, et al. Trends in use of medical imaging in US health care systems and in Ontario, Canada, 2000-2016. *JAMA*. 2019;322(9):843-856. doi:[10.1001/jama.2019.11456](https://doi.org/10.1001/jama.2019.11456) [↩a](#c77-1) [↩b](#c77-2) [↩c](#c77-3)
78. <a name="ref-78"></a>Smith-Bindman R, Chu PW, Azman Firdaus H, et al. Projected lifetime cancer risks from current computed tomography imaging. *JAMA Intern Med*. 2025;185(6):710-719. doi:[10.1001/jamainternmed.2025.0505](https://doi.org/10.1001/jamainternmed.2025.0505) [↩a](#c78-1) [↩b](#c78-2) [↩c](#c78-3)
79. <a name="ref-79"></a>Rula EY. The radiologist shortage: a workforce update from HPI. *ACR Bulletin*. Published February 5, 2026. Accessed October 7, 2026. [https://www.acr.org/Clinical-Resources/Publications-and-Research/ACR-Bulletin/2026/radiologist-shortage-work-force-update](https://www.acr.org/Clinical-Resources/Publications-and-Research/ACR-Bulletin/2026/radiologist-shortage-work-force-update) [↩a](#c79-1) [↩b](#c79-2) [↩c](#c79-3) [↩d](#c79-4) [↩e](#c79-5) [↩f](#c79-6) [↩g](#c79-7) [↩h](#c79-8) [↩i](#c79-9) [↩j](#c79-10) [↩k](#c79-11) [↩l](#c79-12)
80. <a name="ref-80"></a>McDonald RJ, Schwartz KM, Eckel LJ, et al. The effects of changes in utilization and technological advancements of cross-sectional imaging on radiologist workload. *Acad Radiol*. 2015;22(9):1191-1198. doi:[10.1016/j.acra.2015.05.007](https://doi.org/10.1016/j.acra.2015.05.007) [↩a](#c80-1) [↩b](#c80-2)
81. <a name="ref-81"></a>Langlotz CP. The effect of AI on the radiologist workforce: a task-based analysis. *medRxiv*. Preprint posted online December 22, 2025. doi:[10.64898/2025.12.20.25342714](https://doi.org/10.64898/2025.12.20.25342714) [↩a](#c81-1) [↩b](#c81-2) [↩c](#c81-3) [↩d](#c81-4) [↩e](#c81-5) [↩f](#c81-6) [↩g](#c81-7) [↩h](#c81-8) [↩i](#c81-9) [↩j](#c81-10) [↩k](#c81-11) [↩l](#c81-12) [↩m](#c81-13) [↩n](#c81-14)
82. <a name="ref-82"></a>Dhanoa D, Dhesi TS, Burton KR, Nicolaou S, Liang T. The evolving role of the radiologist: the Vancouver workload utilization evaluation study. *J Am Coll Radiol*. 2013;10(10):764-769. doi:[10.1016/j.jacr.2013.04.001](https://doi.org/10.1016/j.jacr.2013.04.001) [↩a](#c82-1) [↩b](#c82-2)
83. <a name="ref-83"></a>Centers for Medicare & Medicaid Services. Medicare and Medicaid programs; CY 2026 payment policies under the physician fee schedule and other changes to Part B payment and coverage policies; Medicare Shared Savings Program requirements; and Medicare prescription drug inflation rebate program. Final rule. *Fed Regist*. 2025;90(212):49266-50481. Accessed October 7, 2026. [https://www.govinfo.gov/content/pkg/FR-2025-11-05/html/2025-19787.htm](https://www.govinfo.gov/content/pkg/FR-2025-11-05/html/2025-19787.htm) [↩a](#c83-1) [↩b](#c83-2) [↩c](#c83-3) [↩d](#c83-4)
84. <a name="ref-84"></a>Radiology alignment: common structures and the value of radiologists' services. *Radiology Business*. Accessed October 7, 2026. [https://radiologybusiness.com/sponsored/1067/vmg/topics/healthcare-management/business-intelligence/radiology-alignment-common-structures-and-value-radiologists-services](https://radiologybusiness.com/sponsored/1067/vmg/topics/healthcare-management/business-intelligence/radiology-alignment-common-structures-and-value-radiologists-services) [↩a](#c84-1) [↩b](#c84-2) [↩c](#c84-3)
85. <a name="ref-85"></a>Manning WG, Newhouse JP, Duan N, Keeler EB, Leibowitz A, Marquis MS. Health insurance and the demand for medical care: evidence from a randomized experiment. *Am Econ Rev*. 1987;77(3):251-277. Accessed October 7, 2026. [https://www.jstor.org/stable/1804094](https://www.jstor.org/stable/1804094) [↩a](#c85-1) [↩b](#c85-2) [↩c](#c85-3)
86. <a name="ref-86"></a>Aron-Dine A, Einav L, Finkelstein A. The RAND Health Insurance Experiment, three decades later. *J Econ Perspect*. 2013;27(1):197-222. doi:[10.1257/jep.27.1.197](https://doi.org/10.1257/jep.27.1.197) [↩a](#c86-1) [↩b](#c86-2) [↩c](#c86-3)
87. <a name="ref-87"></a>Brot-Goldberg ZC, Chandra A, Handel BR, Kolstad JT. What does a deductible do? The impact of cost-sharing on health care prices, quantities, and spending dynamics. *Q J Econ*. 2017;132(3):1261-1318. doi:[10.1093/qje/qjx013](https://doi.org/10.1093/qje/qjx013) [↩a](#c87-1) [↩b](#c87-2)
88. <a name="ref-88"></a>Larson DB, Johnson LW, Schnell BM, Salisbury SR, Forman HP. National trends in CT use in the emergency department: 1995-2007. *Radiology*. 2011;258(1):164-173. doi:[10.1148/radiol.10100640](https://doi.org/10.1148/radiol.10100640) [↩a](#c88-1) [↩b](#c88-2)
89. <a name="ref-89"></a>Johnson PM, Lin DJ, Zbontar J, et al. Deep learning reconstruction enables prospectively accelerated clinical knee MRI. *Radiology*. 2023;307(2):e220425. doi:[10.1148/radiol.220425](https://doi.org/10.1148/radiol.220425) [↩a](#c89-1) [↩b](#c89-2) [↩c](#c89-3)
90. <a name="ref-90"></a>American Society of Radiologic Technologists. ASRT staffing and workplace survey shows vacancy rate increases near record highs aligning with overall health care profession trends. *ASRT News*. Published July 24, 2025. Accessed October 7, 2026. [https://www.asrt.org/main/news-publications/news/article/2025/07/24/asrt-staffing-and-workplace-survey-shows-vacancy-rate-increases-near-record-highs-aligning-with-overall-health-care-profession-trends](https://www.asrt.org/main/news-publications/news/article/2025/07/24/asrt-staffing-and-workplace-survey-shows-vacancy-rate-increases-near-record-highs-aligning-with-overall-health-care-profession-trends) [↩a](#c90-1) [↩b](#c90-2)
91. <a name="ref-91"></a>Bandi P, Star J, Ashad-Bishop K, Kratzer T, Smith R, Jemal A. Lung cancer screening in the US, 2022. *JAMA Intern Med*. 2024;184(8):882-891. doi:[10.1001/jamainternmed.2024.1655](https://doi.org/10.1001/jamainternmed.2024.1655) [↩a](#c91-1) [↩b](#c91-2) [↩c](#c91-3)
92. <a name="ref-92"></a>Lee MH, Garrett JW, Warner JD, Pickhardt PJ. Opportunistic screening with imaging: actionable insights from unused data. *Radiol Clin North Am*. 2026;64(3):605-621. doi:[10.1016/j.rcl.2026.01.013](https://doi.org/10.1016/j.rcl.2026.01.013) [↩a](#c92-1) [↩b](#c92-2) [↩c](#c92-3)
93. <a name="ref-93"></a>Eisemann N, Bunk S, Mukama T, et al. Nationwide real-world implementation of AI for cancer detection in population-based mammography screening. *Nat Med*. 2025;31(3):917-924. doi:[10.1038/s41591-024-03408-6](https://doi.org/10.1038/s41591-024-03408-6) [↩a](#c93-1) [↩b](#c93-2)
94. <a name="ref-94"></a>Boards of Trustees of the Federal Hospital Insurance and Federal Supplementary Medical Insurance Trust Funds. *2026 Annual Report of the Boards of Trustees of the Federal Hospital Insurance and Federal Supplementary Medical Insurance Trust Funds*. Centers for Medicare & Medicaid Services; June 9, 2026. Accessed October 7, 2026. [https://www.cms.gov/oact/tr](https://www.cms.gov/oact/tr) [↩a](#c94-1) [↩b](#c94-2) [↩c](#c94-3) [↩d](#c94-4)
95. <a name="ref-95"></a>US Bureau of Labor Statistics. Computer software engineers and computer programmers. *Occupational Outlook Handbook, 2010-11 Edition (archived)*. Accessed October 7, 2026. [http://web.archive.org/web/2008/http://www.bls.gov/oco/ocos303.htm](http://web.archive.org/web/2008/http://www.bls.gov/oco/ocos303.htm) [↩](#c95-1)
96. <a name="ref-96"></a>US Bureau of Labor Statistics. Software developers (2016-26 projections). *Occupational Outlook Handbook, 2018-19 Edition (archived June 2018)*. Accessed October 7, 2026. [http://web.archive.org/web/20180615000000/https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm](http://web.archive.org/web/20180615000000/https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm) [↩](#c96-1)
97. <a name="ref-97"></a>US Bureau of Labor Statistics. Software developers, quality assurance analysts, and testers. *Occupational Outlook Handbook*. Accessed October 7, 2026. [https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm](https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm) [↩](#c97-1)
98. <a name="ref-98"></a>US Bureau of Labor Statistics. Interpreters and translators. *Occupational Outlook Handbook, 2008-09 Edition (archived May 13, 2008)*. Accessed October 7, 2026. [http://web.archive.org/web/20080513155327/http://www.bls.gov/oco/ocos175.htm](http://web.archive.org/web/20080513155327/http://www.bls.gov/oco/ocos175.htm) [↩](#c98-1)
99. <a name="ref-99"></a>US Bureau of Labor Statistics. Interpreters and translators (2016-26 projections). *Occupational Outlook Handbook, 2018-19 Edition (archived June 2018)*. Accessed October 7, 2026. [http://web.archive.org/web/20180615000000/https://www.bls.gov/ooh/media-and-communication/interpreters-and-translators.htm](http://web.archive.org/web/20180615000000/https://www.bls.gov/ooh/media-and-communication/interpreters-and-translators.htm) [↩](#c99-1)
100. <a name="ref-100"></a>US Bureau of Labor Statistics. Interpreters and translators. *Occupational Outlook Handbook*. Accessed October 7, 2026. [https://www.bls.gov/ooh/media-and-communication/interpreters-and-translators.htm](https://www.bls.gov/ooh/media-and-communication/interpreters-and-translators.htm) [↩](#c100-1)
101. <a name="ref-101"></a>US Bureau of Labor Statistics. Medical transcriptionists. *Occupational Outlook Handbook*. Accessed October 7, 2026. [https://www.bls.gov/ooh/healthcare/medical-transcriptionists.htm](https://www.bls.gov/ooh/healthcare/medical-transcriptionists.htm) [↩](#c101-1)
102. <a name="ref-102"></a>Agarwal N, Moehring A, Rajpurkar P, Salz T. Combining human expertise with artificial intelligence: experimental evidence from radiology. NBER Working Paper 31422. National Bureau of Economic Research; 2023. doi:[10.3386/w31422](https://doi.org/10.3386/w31422) [↩a](#c102-1) [↩b](#c102-2)
103. <a name="ref-103"></a>Baker LC. Acquisition of MRI equipment by doctors drives up imaging use and spending. *Health Aff (Millwood)*. 2010;29(12):2252-2259. doi:[10.1377/hlthaff.2009.1099](https://doi.org/10.1377/hlthaff.2009.1099) [↩](#c103-1)

---

<a name="appendix-a"></a>
## Appendix A. Full parameter table

E = empirical, A = anchored, S = subjective. Loadings are on $z_{AI}$ (AI progress), $z_{reg}$ (regulatory friction) and
$z_{dem}$ (appetite for imaging).

| Group | Parameter | Distribution | P10 / P50 / P90 | Unit | Evidence | Sources & notes |
|---|---|---|---|---|---|---|
| demand | Demographic (population + aging) growth of radiologist work, 2026-2045 (`dem_rate`) | Normal(μ=0.52, σ=0.1), truncated [0.15, 0.9] | 0.392 / 0.52 / 0.648 | %/yr | **A** | <a name="c75-5"></a><sup>[75](#ref-75)</sup>, <a name="c76-2"></a><sup>[76](#ref-76)</sup> Christensen et al project +16.9% to +26.9% exams by modality 2023-2055 from population growth and aging alone (≈0.49-0.75%/yr) using Census 2023 projections. CBO's 2026 outlook has slower population growth (349M→364M, 2026-2056), so the centre is shaded down ≈0.1 pt. |
| demand | Demographic growth in 2066 relative to 2026-2045 rate (`dem_late`) | Uniform(0.4, 0.9) | 0.45 / 0.65 / 0.85 | ratio | **A** | <a name="c76-3"></a><sup>[76](#ref-76)</sup> CBO projects population growth slowing to zero by 2056; aging continues to add imaging per capita. |
| demand | Per-capita (age/sex-adjusted) utilization growth, 2026 (`util_g0`) | Normal(μ=0.6, σ=0.7), truncated [-1.5, 3.5] | -0.292 / 0.601 / 1.5 | %/yr | **S** | <a name="c75-6"></a><sup>[75](#ref-75)</sup>, <a name="c79-9"></a><sup>[79](#ref-79)</sup>, <a name="c77-2"></a><sup>[77](#ref-77)</sup>, <a name="c69-5"></a><sup>[69](#ref-69)</sup>, <a name="c78-3"></a><sup>[78](#ref-78)</sup> National 2018-22 claims (Christensen et al): projected total utilization in 2055 vs 2023 is +16.9% to +26.9% by modality from population growth and aging alone, and -5.6% to +45.2% if each modality's recent per-person trend continues to 2030 (radiography and nuclear medicine falling, CT and MRI rising). The Neiman Institute's 2026 update projects +17% (MRI) to +25% (CT) by 2055. Older health-system data show faster CT growth (3.7-5.2%/yr, 2013-16) and ED CT per Medicare beneficiary nearly doubled 2013-2023. Each end of the trend range is a single modality (CT up, nuclear medicine down), so a work-weighted claims-based figure is lower than CT's. We centre per-person growth at 0.6%/yr, decaying toward ~0.2%/yr: above the claims-based trends because 2018-22 includes the COVID dip and we let growth continue past 2030, and below CT's own trend. This is a judgment; the 'imaging restraint' and 'imaging growth' prior sets bracket it. *Factor loadings: z_dem: +0.7.* |
| demand | Long-run per-capita utilization growth (asymptote) (`util_ginf`) | Normal(μ=0.2, σ=0.5), truncated [-1.5, 2.5] | -0.44 / 0.2 / 0.841 | %/yr | **S** | <a name="c77-3"></a><sup>[77](#ref-77)</sup>, <a name="c75-7"></a><sup>[75](#ref-75)</sup> Growth in CT/MRI per capita has decelerated each decade since 2000; we assume further deceleration but allow either sign. *Factor loadings: z_dem: +0.7.* |
| demand | Half-life of convergence from current to long-run utilization growth (`util_half`) | Uniform(6, 20) | 7.4 / 13 / 18.6 | years | **S** |   |
| demand | Growth in radiologist work per exam (complexity, images/study), 2026 (`cmplx_g0`) | Normal(μ=0.4, σ=0.3), truncated [-0.2, 1.2] | 0.0476 / 0.407 / 0.782 | %/yr | **A** | <a name="c80-2"></a><sup>[80](#ref-80)</sup> Images per cross-sectional study rose ~10x at Mayo 1999-2010 while exams doubled. Work per exam (RVU-weighted) grows far more slowly than image counts; we decay this term with a 20-year half-life. *Factor loadings: z_dem: +0.3.* |
| demand | Imaging displaced by alternative diagnostics by 2066 (blood tests, AI-ECG, genomics) (`alt_max`) | Triangular(0, mode 0.04, 0.15) | 0.0245 / 0.0592 / 0.109 | share | **S** |   |
| demand | Midpoint year of alternative-diagnostic substitution (`alt_mid`) | Uniform(2035, 2055) | 2037 / 2045 / 2053 | year | **S** |   |
| demand | Supply ÷ demand for radiologist FTEs in 2026 (current shortage) (`ratio0`) | Triangular(0.85, mode 0.93, 0.99) | 0.883 / 0.925 / 0.961 | ratio | **S** | <a name="c79-10"></a><sup>[79](#ref-79)</sup>, <a name="c67-5"></a><sup>[67](#ref-67)</sup>, <a name="c68-4"></a><sup>[68](#ref-68)</sup>, <a name="c11-2"></a><sup>[11](#ref-11)</sup>, <a name="c10-3"></a><sup>[10](#ref-10)</sup> No measured national figure exists; this is a judgment from indirect signals. HRSA projects radiology at ≈90% adequacy in 2038 (a projection, not today's gap), and the Neiman Institute calls the shortage 'fairly static'. Compensation rose 6.6% in a year and DR positions keep expanding. Average exams read per radiologist-day were flat 2018-2024 (+0.6%) but the busiest quartile read 31% more, and practice turnover rose from 5.3% to 8.5% (2013-2022): a real but uneven, moderate shortage. |
| ai_capability | AI progress speed (quantile → timeline multiplier M) (`ai_u`) | Regime mixture: 15% stall (M 1.6-3.0), 55% trend (lognormal, median 1, σ_log 0.25), 18% fast (M 0.40-0.65), 12% transformative (M 0.25-0.45, task ceilings lifted) | 0.417 / 0.917 / 2.07 | multiplier | **S** | <a name="c28-2"></a><sup>[28](#ref-28)</sup>, <a name="c29-4"></a><sup>[29](#ref-29)</sup>, <a name="c30-4"></a><sup>[30](#ref-30)</sup>, <a name="c31-2"></a><sup>[31](#ref-31)</sup>, <a name="c32-3"></a><sup>[32](#ref-32)</sup>, <a name="c33-3"></a><sup>[33](#ref-33)</sup> Loose guidance only; M multiplies the years from 2026 until each capability arrives. AI researchers put 50% odds on machines outperforming humans at every task by 2047 but on full automation of occupations only by 2116; expert panels put far lower odds on near-term transformative AI than lab leaders. Fast + transformative = 30% of worlds. *Factor loadings: z_ai: +1.0.* |
| ai_capability | Midpoint year: reliable draft reports & automated measurements (M=1) (`cap_draft_T0`) | Normal(μ=2028, σ=1.5) | 2026 / 2028 / 2030 | year | **A** | <a name="c44-2"></a><sup>[44](#ref-44)</sup>, <a name="c45-2"></a><sup>[45](#ref-45)</sup>, <a name="c48-2"></a><sup>[48](#ref-48)</sup>, <a name="c58-2"></a><sup>[58](#ref-58)</sup>, <a name="c81-4"></a><sup>[81](#ref-81)</sup> Generative draft reporting gave +15.5% documentation efficiency on 24k radiographs in live use; AI-drafted chest radiograph reports cut reading time 42% in a reader study; generative chest-radiograph drafting tools received FDA Breakthrough designations in 2026. |
| ai_capability | Midpoint year: protocoling, scheduling, QA and admin automation (M=1) (`cap_admin_T0`) | Normal(μ=2030.5, σ=2) | 2028 / 2030 / 2033 | year | **A** | <a name="c81-5"></a><sup>[81](#ref-81)</sup>  |
| ai_capability | Midpoint year: AI assistance that materially speeds interpretation (M=1) (`cap_interp_T0`) | Normal(μ=2033, σ=3) | 2029 / 2033 / 2037 | year | **A** | <a name="c49-3"></a><sup>[49](#ref-49)</sup>, <a name="c50-2"></a><sup>[50](#ref-50)</sup>, <a name="c102-1"></a><sup>[102](#ref-102)</sup>, <a name="c43-2"></a><sup>[43](#ref-43)</sup> Real-world meta-analysis finds no significant time savings yet; effects of AI assistance vary widely across radiologists and erroneous AI output hurts performance; radiologists under-weight AI predictions. |
| ai_capability | Midpoint year: AI support for clinical synthesis/communication (M=1) (`cap_consult_T0`) | Normal(μ=2034, σ=3) | 2030 / 2034 / 2038 | year | **S** | <a name="c81-6"></a><sup>[81](#ref-81)</sup>  |
| ai_capability | Midpoint year: meaningful automation of procedural/physical work (M=1) (`cap_proc_T0`) | Normal(μ=2050, σ=8) | 2040 / 2050 / 2060 | year | **S** |   |
| ai_capability | Capability S-curve width (logistic scale; 10→90% ≈ 4.4×) (`cap_width`) | Uniform(2, 4) | 2.2 / 3 / 3.8 | years | **S** |   |
| ai_tasks | Max time saved on interpretation by assistive AI (radiologist still reads) (`m_interp`) | Beta(6, 14) [mean 0.30] | 0.175 / 0.293 / 0.434 | share | **A** | <a name="c81-7"></a><sup>[81](#ref-81)</sup>, <a name="c50-3"></a><sup>[50](#ref-50)</sup>, <a name="c45-3"></a><sup>[45](#ref-45)</sup> Langlotz's task analysis and reader studies of AI assistance. (European screening workload cuts of 33-44% come from replacing the second reader in double reading, a substitution effect that does not transfer to single-read U.S. practice, so they are not used here.) *Factor loadings: z_ai: +0.4.* |
| ai_tasks | Max time saved on measurement & report drafting (`m_draft`) | Beta(12, 8) [mean 0.60] | 0.459 / 0.603 / 0.737 | share | **A** | <a name="c44-3"></a><sup>[44](#ref-44)</sup>, <a name="c45-4"></a><sup>[45](#ref-45)</sup>, <a name="c46-2"></a><sup>[46](#ref-46)</sup>, <a name="c47-3"></a><sup>[47](#ref-47)</sup>, <a name="c81-8"></a><sup>[81](#ref-81)</sup> Measured savings span 0% to 42% of reading time: +15.5% (live radiographs), −42% (chest-radiograph reader study), −0.46 min per impression (multicentre LLM study), and no sustained gain at one of two CT sites. If drafting and measurement are ~30% of reading time, current tools already capture roughly half of this sub-task. *Factor loadings: z_ai: +0.4.* |
| ai_tasks | Max time saved on clinical synthesis/consultation/communication (`m_consult`) | Beta(5, 15) [mean 0.25] | 0.134 / 0.242 / 0.378 | share | **A** | <a name="c81-9"></a><sup>[81](#ref-81)</sup> Langlotz: record summarization −30% tech/provider communication; non-routine communication −30%; patient explanation −30%. *Factor loadings: z_ai: +0.4.* |
| ai_tasks | Max time saved on administrative work (protocoling, QA, scheduling) (`m_admin`) | Beta(8, 12) [mean 0.40] | 0.263 / 0.397 / 0.541 | share | **A** | <a name="c81-10"></a><sup>[81](#ref-81)</sup> Langlotz: automated protocoling −60% (30-70%). *Factor loadings: z_ai: +0.4.* |
| ai_tasks | Max time saved on physical/procedural work (`m_proc`) | Beta(1.5, 17) [mean 0.08] | 0.0168 / 0.0663 / 0.166 | share | **S** |   *Factor loadings: z_ai: +0.4.* |
| ai_tasks | Midpoint year of effective clinical adoption of assistive AI (`adopt_mid`) | Normal(μ=2029.5, σ=2), truncated [2027, 2040] | 2028 / 2030 / 2032 | year | **A** | <a name="c13-2"></a><sup>[13](#ref-13)</sup>, <a name="c64-2"></a><sup>[64](#ref-64)</sup>, <a name="c65-2"></a><sup>[65](#ref-65)</sup>, <a name="c12-5"></a><sup>[12](#ref-12)</sup>, <a name="c19-3"></a><sup>[19](#ref-19)</sup> ≈1,100 radiology AI devices cleared by 2025 but claims-based use was concentrated in a handful of products; 33.5% of US radiologists reported using any AI in 2020, and 75% of UK departments used AI clinically in 2025 without an overall workload reduction. Precedent: mammography CAD reached most US screening exams within ~6 years of payment. *Factor loadings: z_reg: +0.4, z_ai: -0.3.* |
| ai_tasks | Shortage acceleration of AI adoption (extra adoption-clock speed per unit ln(D/S)) (`adopt_pressure`) | Uniform(0, 4) | 0.4 / 2 / 3.6 | multiplier | **S** | <a name="c79-11"></a><sup>[79](#ref-79)</sup>, <a name="c65-3"></a><sup>[65](#ref-65)</sup> Practices adopt labour-saving AI faster when radiologists are scarce. At a 7% shortage and the midpoint value (2), assistive and autonomous adoption clocks run ~14% faster. Applied only while demand exceeds supply. |
| ai_tasks | Assistive adoption S-curve width (`adopt_width`) | Uniform(1.5, 3.5) | 1.7 / 2.5 / 3.3 | years | **S** |   |
| ai_tasks | Saturation share of work done with assistive AI (`adopt_max`) | Beta(18, 2) [mean 0.90] | 0.81 / 0.913 / 0.972 | share | **S** |   |
| ai_tasks | New oversight work created by AI (governance, auditing, validation), share of time (`ovh_max`) | Uniform(0.02, 0.08) | 0.026 / 0.05 / 0.074 | share | **S** | <a name="c81-11"></a><sup>[81](#ref-81)</sup>, <a name="c72-3"></a><sup>[72](#ref-72)</sup>, <a name="c23-4"></a><sup>[23](#ref-23)</sup> Langlotz does not model AI monitoring/oversight time. In Danish administrative data, chatbot adoption created new integration and oversight tasks that offset most of a ~3% time saving. |
| autonomy | Tier 1 share of interpretive work: normal/negative radiographs & screening exams (`w1`) | Triangular(0.04, mode 0.07, 0.12) | 0.0555 / 0.0753 / 0.1 | share | **A** | <a name="c55-2"></a><sup>[55](#ref-55)</sup>, <a name="c56-2"></a><sup>[56](#ref-56)</sup>, <a name="c51-2"></a><sup>[51](#ref-51)</sup>, <a name="c54-3"></a><sup>[54](#ref-54)</sup>, <a name="c57-2"></a><sup>[57](#ref-57)</sup> AI could autonomously report 7.8% of all posteroanterior chest radiographs at >99% sensitivity (2023) and ~17.5% at 99% sensitivity with a tuned threshold (2024); AI triage let about two-thirds of Danish screening mammograms be single-read (33.5% fewer reads), though that saving comes from European double reading and U.S. screening is single-read. Radiographs and screening mammography are ~20-25% of radiologist work, so tier 1 is ≈4-12% of interpretive work. |
| autonomy | Tier 2 share: all radiographs, screening mammography, standardized follow-ups (`w2`) | Triangular(0.1, mode 0.17, 0.25) | 0.132 / 0.173 / 0.215 | share | **A** | <a name="c81-12"></a><sup>[81](#ref-81)</sup> Langlotz delegation assumptions: mammography 50%, radiography 40%, other modalities 3%. |
| autonomy | Tier 3 share: complex diagnostic CT/MR/US/NM (`w3`) | Triangular(0.35, mode 0.47, 0.57) | 0.401 / 0.465 / 0.523 | share | **S** |   *Factor loadings: z_ai: +0.2.* |
| autonomy | Tier 1 technical capability year (not AI-speed scaled) (`tcap1_T0`) | Normal(μ=2025, σ=1) | 2024 / 2025 / 2026 | year | **A** | <a name="c57-3"></a><sup>[57](#ref-57)</sup> An autonomous normal-chest-radiograph product received EU CE Class IIb marking in 2022. |
| autonomy | Tier 2 technical capability year (M=1) (`tcap2_T0`) | Normal(μ=2031, σ=3) | 2027 / 2031 / 2035 | year | **S** |   |
| autonomy | Tier 3 technical capability year (M=1) (`tcap3_T0`) | Normal(μ=2040, σ=5) | 2034 / 2040 / 2046 | year | **S** |   |
| autonomy | Tier 4 (residual hardest work) capability year (M=1) (`tcap4_T0`) | Normal(μ=2052, σ=8) | 2042 / 2052 / 2062 | year | **S** |   |
| regulation | Clinical-validation lag (prospective, multi-site) after capability; tier-1 median (`lval`) | Lognormal(median=2.5, σ_log=0.4) | 1.5 / 2.5 / 4.17 | years | **A** | <a name="c54-4"></a><sup>[54](#ref-54)</sup>, <a name="c52-2"></a><sup>[52](#ref-52)</sup>, <a name="c61-3"></a><sup>[61](#ref-61)</sup> MASAI randomised from April 2021; its interval-cancer endpoint was published in January 2026 (~5 years). 43% of FDA-authorised AI devices had no published clinical validation and only 4% had randomised trials. Tiers 2-4 multiply by 1.2/1.5/1.8. *Factor loadings: z_reg: +0.3, z_ai: -0.3.* |
| regulation | FDA authorization lag for autonomous claims; tier-2 median (`lfda`) | Lognormal(median=2, σ_log=0.5) | 1.05 / 2 / 3.8 | years | **A** | <a name="c12-6"></a><sup>[12](#ref-12)</sup>, <a name="c60-2"></a><sup>[60](#ref-60)</sup>, <a name="c58-3"></a><sup>[58](#ref-58)</sup>, <a name="c59-2"></a><sup>[59](#ref-59)</sup>, <a name="c21-3"></a><sup>[21](#ref-21)</sup> As of October 2026 no autonomous radiology read is FDA-authorized; generative report drafting has reached FDA Breakthrough designation (2026) and one 510(k) report-generating tool keeps the radiologist in control; FDA's AI lifecycle guidance remains a draft. IDx-DR (2018) is the main autonomous precedent. Tier multipliers 0.75/1.0/1.5/2.0. *Factor loadings: z_reg: +0.7, z_ai: -0.3.* |
| regulation | Liability + reimbursement + scope-of-practice acceptance lag; tier-2 median (`lpay`) | Lognormal(median=4, σ_log=0.6) | 1.85 / 4 / 8.63 | years | **A** | <a name="c21-4"></a><sup>[21](#ref-21)</sup>, <a name="c63-3"></a><sup>[63](#ref-63)</sup>, <a name="c62-4"></a><sup>[62](#ref-62)</sup>, <a name="c83-3"></a><sup>[83](#ref-83)</sup> Autonomous retinal AI: FDA 2018 → Category I CPT 92229 in 2021. Mock jurors penalize radiologists who disagree with AI. Medicare professional-component billing presumes physician interpretation. Tier multipliers 0.75/1.0/1.4/1.8. *Factor loadings: z_reg: +0.7, z_ai: -0.3.* |
| regulation | Hospital adoption: years from 'ready' to half of eventual uptake (`ahalf`) | Lognormal(median=5.5, σ_log=0.35) | 3.51 / 5.5 / 8.61 | years | **A** | <a name="c20-3"></a><sup>[20](#ref-20)</sup>, <a name="c19-4"></a><sup>[19](#ref-19)</sup>, <a name="c13-3"></a><sup>[13](#ref-13)</sup> Hospital EHR adoption passed 50% about four years after the 2009 HITECH subsidies; reimbursed mammography CAD diffused within ≈4-6 years. *Factor loadings: z_reg: +0.4, z_ai: -0.2.* |
| regulation | Autonomy adoption S-curve width (`awidth`) | Uniform(1.5, 3.5) | 1.7 / 2.5 / 3.3 | years | **S** |   |
| regulation | Eventual uptake of tier-1 autonomy (share of eligible work) (`amax1`) | Beta(17, 3) [mean 0.85] | 0.743 / 0.862 / 0.941 | share | **S** |   *Factor loadings: z_reg: -0.4, z_ai: +0.3.* |
| regulation | Eventual uptake of tier-2 autonomy (`amax2`) | Beta(14, 6) [mean 0.70] | 0.566 / 0.707 / 0.825 | share | **S** |   *Factor loadings: z_reg: -0.4, z_ai: +0.3.* |
| regulation | Eventual uptake of tier-3 autonomy (`amax3`) | Beta(11, 9) [mean 0.55] | 0.408 / 0.552 / 0.69 | share | **S** |   *Factor loadings: z_reg: -0.4, z_ai: +0.3.* |
| regulation | Eventual uptake of tier-4 autonomy (`amax4`) | Beta(8, 12) [mean 0.40] | 0.263 / 0.397 / 0.541 | share | **S** |   *Factor loadings: z_reg: -0.4, z_ai: +0.3.* |
| regulation | Share of interpretation+drafting time actually removed per AI-first/autonomous study (`f_sub`) | Uniform(0.6, 0.95) | 0.635 / 0.775 / 0.915 | share | **S** | <a name="c102-2"></a><sup>[102](#ref-102)</sup>, <a name="c48-3"></a><sup>[48](#ref-48)</sup> Residual human time: sampling QA, sign-off, escalations, liability review. Clinically significant errors still appeared in 22.8% of AI-only versus 14.0% of human-only chest-radiograph reports in a 2025 evaluation. *Factor loadings: z_ai: +0.3.* |
| jevons | Professional (interpretation) share of the all-in price of an imaging exam (`pc_share`) | Triangular(0.1, mode 0.2, 0.3) | 0.145 / 0.2 / 0.255 | share | **A** | <a name="c84-3"></a><sup>[84](#ref-84)</sup> ≈20% for MRI, ≈25% for radiography of Medicare global fees; lower where hospital facility fees apply. |
| jevons | Share of cost savings passed through to prices paid (`pass_through`) | Beta(4, 6) [mean 0.40] | 0.21 / 0.393 / 0.599 | share | **S** |  Fee schedules are administered and revalued slowly; commercial prices are sticky. |
| jevons | Price elasticity of imaging demand (`elasticity`) | Triangular(-0.6, mode -0.2, -0.05) | -0.452 / -0.268 / -0.141 | elasticity | **A** | <a name="c85-3"></a><sup>[85](#ref-85)</sup>, <a name="c86-3"></a><sup>[86](#ref-86)</sup>, <a name="c87-2"></a><sup>[87](#ref-87)</sup> RAND HIE ≈ −0.2 for medical care, with respect to the patient's out-of-pocket price; professional-fee cuts mostly fall on payers, so this channel is if anything overstated. Deductible shocks cut imaging alongside other services. |
| jevons | Turnaround/availability rebound: extra work per unit of radiologist time freed (`access`) | Triangular(0, mode 0.1, 0.3) | 0.0548 / 0.127 / 0.223 | ratio | **A** | <a name="c88-2"></a><sup>[88](#ref-88)</sup> Non-price rationing: when reads become fast and available 24/7, clinicians order more (ED CT visits rose from 2.8% to 13.9%, 1995-2007). Applied to the share of radiologist time saved. |
| jevons | New AI-enabled imaging applications by 2066 (share of baseline work, before capacity limits) (`new_max`) | Lognormal(median=0.18, σ_log=0.7) | 0.0734 / 0.18 / 0.441 | share | **S** | <a name="c70-4"></a><sup>[70](#ref-70)</sup>, <a name="c91-3"></a><sup>[91](#ref-91)</sup>, <a name="c92-3"></a><sup>[92](#ref-92)</sup>, <a name="c83-4"></a><sup>[83](#ref-83)</sup>, <a name="c53-3"></a><sup>[53](#ref-53)</sup> Of 2024 imaging studies with direct patient-care impact, 49% would increase radiologist workload and <1% would decrease it; AI studies were about 14 times higher odds of adding work (odds ratio 14.3). Examples: opportunistic CT screening, lung screening (18% uptake in 2022), AI coronary plaque analysis (Category I CPT 75577 from 2026). *Factor loadings: z_ai: +0.5, z_dem: +0.3.* |
| jevons | Midpoint year of new-application uptake (M=1) (`new_T0`) | Normal(μ=2038, σ=4) | 2033 / 2038 / 2043 | year | **S** |   |
| jevons | New-application S-curve width (`new_width`) | Uniform(3, 6) | 3.3 / 4.5 / 5.7 | years | **S** |   |
| jevons | Radiologist labour intensity of new-application work vs a typical exam (`lambda_new`) | Uniform(0.4, 1) | 0.46 / 0.7 / 0.94 | ratio | **S** |   |
| jevons | Extra follow-up work from AI-detected (incidental) findings at full deployment (`iota`) | Triangular(0, mode 0.03, 0.08) | 0.0155 / 0.0353 / 0.06 | share | **A** | <a name="c53-4"></a><sup>[53](#ref-53)</sup>, <a name="c93-2"></a><sup>[93](#ref-93)</sup> AI-supported screening raised cancer detection 17.6-29% with flat recall; more findings mean more follow-up. |
| jevons | Latent demand currently rationed by scanner/technologist capacity (`latent`) | Triangular(0.02, mode 0.06, 0.12) | 0.04 / 0.0652 / 0.0955 | share | **A** | <a name="c90-2"></a><sup>[90](#ref-90)</sup> CT technologist vacancy 19.4% and MRI 17.4% in 2025. |
| jevons | AI-driven acquisition throughput gain at maturity (faster scans, auto-positioning) (`thru_H`) | Lognormal(median=0.3, σ_log=0.45) | 0.169 / 0.3 / 0.534 | share | **A** | <a name="c89-2"></a><sup>[89](#ref-89)</sup> Deep-learning reconstruction cut knee MRI time ≈44% prospectively; CT is already fast and table time dominates. *Factor loadings: z_ai: +0.5.* |
| jevons | Midpoint year of throughput gains (M=1) (`thru_T0`) | Normal(μ=2032, σ=3) | 2028 / 2032 / 2036 | year | **A** | <a name="c89-3"></a><sup>[89](#ref-89)</sup>  |
| jevons | Long-run extra scanner/technologist capacity built in response to demand (by 2066) (`cap_invest`) | Uniform(0, 0.25) | 0.025 / 0.125 / 0.225 | share | **S** | <a name="c103-1"></a><sup>[103](#ref-103)</sup>  |
| jevons | AI-enabled utilization management (order decision support, payer AI prior auth) (`um_max`) | Triangular(0, mode 0.03, 0.08) | 0.0155 / 0.0353 / 0.06 | share | **A** | <a name="c81-13"></a><sup>[81](#ref-81)</sup>, <a name="c94-4"></a><sup>[94](#ref-94)</sup> Langlotz: order-entry decision support −3% (0-6%) of advanced imaging; Medicare HI trust fund depletion projected 2033. *Factor loadings: z_dem: -0.4.* |
| jevons | Reads shifting to non-radiologists with AI support by 2066 (`scope_max`) | Triangular(0, mode 0.03, 0.1) | 0.0173 / 0.0408 / 0.0735 | share | **S** |   |
| jevons | New radiologist tasks created alongside AI (reinstatement), share of 2026 FTE (`nt_max`) | Triangular(0, mode 0.04, 0.12) | 0.0219 / 0.0507 / 0.089 | share | **S** | <a name="c23-5"></a><sup>[23](#ref-23)</sup>, <a name="c25-4"></a><sup>[25](#ref-25)</sup>, <a name="c70-5"></a><sup>[70](#ref-70)</sup> e.g. AI governance roles, theranostics, quantitative-imaging consults, multidisciplinary precision-medicine work. *Factor loadings: z_ai: +0.3.* |
| supply | Attrition hazard multiplier (post-COVID ≈ high end) (`attr_mult`) | Uniform(0.95, 1.25) | 0.98 / 1.1 / 1.22 | multiplier | **A** | <a name="c1-5"></a><sup>[1](#ref-1)</sup>, <a name="c79-12"></a><sup>[79](#ref-79)</sup>, <a name="c68-5"></a><sup>[68](#ref-68)</sup> Measured attrition rose from 1.1%/yr (2014) to 2.0% (2019) and 2.5% (2022). With flat residency positions, multipliers of 1.0 and 1.2 reproduce the published supply projections under blended 2014-23 attrition (+25.7% by 2055) and post-COVID attrition (+20.9%); the range is centred between them, nearer the post-COVID case the Neiman 2026 update emphasises. Turnover between practices also roughly doubled (adjusted odds 1.96, 2022 vs 2013). |
| supply | Trend growth in DR residency positions (before market response) (`slot_g`) | Normal(μ=1, σ=0.8), truncated [-1.0, 3.0] | -0.00299 / 1 / 2 | %/yr | **A** | <a name="c1-6"></a><sup>[1](#ref-1)</sup>, <a name="c10-4"></a><sup>[10](#ref-10)</sup> DR positions rose from 1,132 (2022) to 1,241 (2026), ≈2.3%/yr; GME caps limit sustained growth. |
| supply | Residency-position response to market signal (elasticity to ln D/S) (`resid_gamma`) | Uniform(0.3, 1.5) | 0.42 / 0.9 / 1.38 | elasticity | **A** | <a name="c3-4"></a><sup>[3](#ref-3)</sup>, <a name="c16-3"></a><sup>[16](#ref-16)</sup>, <a name="c17-2"></a><sup>[17](#ref-17)</sup> After the mid-1990s downturn, radiology trainee numbers fell to a 1997 nadir (3,080) and then rose 84% by 2011; medical-student interest tracks the job market. |
| supply | Fill-rate response to oversupply (applicant flight) (`fill_kappa`) | Uniform(0.3, 1.5) | 0.42 / 0.9 / 1.38 | elasticity | **A** | <a name="c3-5"></a><sup>[3](#ref-3)</sup>, <a name="c4-5"></a><sup>[4](#ref-4)</sup> 2015 Match, during the last oversupply: 86% of advanced DR positions filled, 55 of 166 programs went unfilled, and U.S. graduates took 67% of matched positions. |
| supply | Information/perception lag before the pipeline reacts (`resid_lag`) | Uniform(1, 3) | 1.2 / 2 / 2.8 | years | **A** | <a name="c3-6"></a><sup>[3](#ref-3)</sup>  |
| supply | Applicant deterrence from visible AI progress (max fill-rate loss) (`fear`) | Uniform(0, 0.08) | 0.008 / 0.04 / 0.072 | share | **A** | <a name="c10-5"></a><sup>[10](#ref-10)</sup>, <a name="c18-2"></a><sup>[18](#ref-18)</sup> DR PGY-1 applicants fell 14% over 2023-2026 even as positions hit records and still filled 97.6%. In a 32-school survey, radiology's first-choice share fell from 21.4% to 17.7% when students considered AI. |
| supply | Drift in FTE per radiologist (part-time, generational preferences) (`fte_drift`) | Normal(μ=-0.1, σ=0.15) | -0.292 / -0.1 / 0.0922 | %/yr | **S** |   |

Task-share Dirichlet (concentration 80): interpretation 0.42, drafting/measurement 0.18, consultation 0.13, administration
0.15, procedures 0.12 <a name="c81-14"></a><a name="c82-2"></a><sup>[81](#ref-81),[82](#ref-82)</sup>.
