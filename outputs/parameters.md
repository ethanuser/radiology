| Parameter | Distribution | P10 / P50 / P90 | Unit | Evidence | Sources |
|---|---|---|---|---|---|
| `dem_rate`: Demographic (population + aging) growth of radiologist work, 2026-2045 | Normal(μ=0.52, σ=0.1), truncated [0.15, 0.9] | 0.392 / 0.52 / 0.648 | %/yr | E | christensen_util, cbo_2026 |
| `dem_late`: Demographic growth in 2066 relative to 2026-2045 rate | Uniform(0.4, 0.9) | 0.45 / 0.65 / 0.85 | ratio | A | cbo_2026 |
| `util_g0`: Per-capita (age/sex-adjusted) utilization growth, 2026 | Normal(μ=0.8, σ=0.7), truncated [-1.5, 3.5] | -0.0953 / 0.8 / 1.7 | %/yr | A | christensen_util, rula_2026, smith_bindman_2019, rosenkrantz_2025, smith_bindman_2025 |
| `util_ginf`: Long-run per-capita utilization growth (asymptote) | Normal(μ=0.2, σ=0.5), truncated [-1.5, 2.5] | -0.44 / 0.2 / 0.841 | %/yr | S | smith_bindman_2019, christensen_util |
| `util_half`: Half-life of convergence from current to long-run utilization growth | Uniform(6, 20) | 7.4 / 13 / 18.6 | years | S |  |
| `cmplx_g0`: Growth in radiologist work per exam (complexity, images/study), 2026 | Normal(μ=0.4, σ=0.3), truncated [-0.2, 1.2] | 0.0476 / 0.407 / 0.782 | %/yr | A | mcdonald_2015 |
| `alt_max`: Imaging displaced by alternative diagnostics by 2066 (blood tests, AI-ECG, genomics) | Triangular(0, mode 0.04, 0.15) | 0.0245 / 0.0592 / 0.109 | share | S |  |
| `alt_mid`: Midpoint year of alternative-diagnostic substitution | Uniform(2035, 2055) | 2037 / 2045 / 2053 | year | S |  |
| `ratio0`: Supply ÷ demand for radiologist FTEs in 2026 (current shortage) | Triangular(0.85, mode 0.93, 0.99) | 0.883 / 0.925 / 0.961 | ratio | S | rula_2026, zamani_2026, parikh_2026, doximity_2026, nrmp_2026 |
| `ai_u`: AI progress speed (quantile → timeline multiplier M) | Regime mixture: 15% stall (M 1.6-3.0), 55% trend (lognormal, median 1, σ_log 0.25), 18% fast (M 0.40-0.65), 12% transformative (M 0.25-0.45, task ceilings lifted) | 0.417 / 0.917 / 2.07 | multiplier | S | metr_2025, metr_2026, ai2027, grace_2025, leap_2025, karger_2023 |
| `cap_draft_T0`: Midpoint year: reliable draft reports & automated measurements (M=1) | Normal(μ=2028, σ=1.5) | 2026 / 2028 / 2030 | year | A | huang_2025, hong_2025, tanno_2025, aidoc_2026, langlotz_2025 |
| `cap_admin_T0`: Midpoint year: protocoling, scheduling, QA and admin automation (M=1) | Normal(μ=2030.5, σ=2) | 2028 / 2030 / 2033 | year | A | langlotz_2025 |
| `cap_interp_T0`: Midpoint year: AI assistance that materially speeds interpretation (M=1) | Normal(μ=2033, σ=3) | 2029 / 2033 / 2037 | year | A | wenderott_2024, yu_2024, agarwal_2023, rajpurkar_2023 |
| `cap_consult_T0`: Midpoint year: AI support for clinical synthesis/communication (M=1) | Normal(μ=2034, σ=3) | 2030 / 2034 / 2038 | year | S | langlotz_2025 |
| `cap_proc_T0`: Midpoint year: meaningful automation of procedural/physical work (M=1) | Normal(μ=2050, σ=8) | 2040 / 2050 / 2060 | year | S |  |
| `cap_width`: Capability S-curve width (logistic scale; 10→90% ≈ 4.4×) | Uniform(2, 4) | 2.2 / 3 / 3.8 | years | S |  |
| `m_interp`: Max time saved on interpretation by assistive AI (radiologist still reads) | Beta(6, 14) [mean 0.30] | 0.175 / 0.293 / 0.434 | share | A | langlotz_2025, yu_2024, hong_2025 |
| `m_draft`: Max time saved on measurement & report drafting | Beta(12, 8) [mean 0.60] | 0.459 / 0.603 / 0.737 | share | A | huang_2025, hong_2025, li_2026, liu_2026, langlotz_2025 |
| `m_consult`: Max time saved on clinical synthesis/consultation/communication | Beta(5, 15) [mean 0.25] | 0.134 / 0.242 / 0.378 | share | A | langlotz_2025 |
| `m_admin`: Max time saved on administrative work (protocoling, QA, scheduling) | Beta(8, 12) [mean 0.40] | 0.263 / 0.397 / 0.541 | share | A | langlotz_2025 |
| `m_proc`: Max time saved on physical/procedural work | Beta(1.5, 17) [mean 0.08] | 0.0168 / 0.0663 / 0.166 | share | S |  |
| `adopt_mid`: Midpoint year of effective clinical adoption of assistive AI | Normal(μ=2029.5, σ=2), truncated [2027, 2040] | 2028 / 2030 / 2032 | year | A | wu_2024, allen_2021, rcr_2026, fda_ai_2026, lehman_2015 |
| `adopt_pressure`: Shortage acceleration of AI adoption (extra adoption-clock speed per unit ln(D/S)) | Uniform(0, 4) | 0.4 / 2 / 3.6 | multiplier | S | rula_2026, rcr_2026 |
| `adopt_width`: Assistive adoption S-curve width | Uniform(1.5, 3.5) | 1.7 / 2.5 / 3.3 | years | S |  |
| `adopt_max`: Saturation share of work done with assistive AI | Beta(18, 2) [mean 0.90] | 0.81 / 0.913 / 0.972 | share | S |  |
| `ovh_max`: New oversight work created by AI (governance, auditing, validation), share of time | Uniform(0.02, 0.08) | 0.026 / 0.05 / 0.074 | share | S | langlotz_2025, humlum_2025, acemoglu_restrepo_2019 |
| `w1`: Tier 1 share of interpretive work: normal/negative radiographs & screening exams | Triangular(0.04, mode 0.07, 0.12) | 0.0555 / 0.0753 / 0.1 | share | A | plesner_2023, plesner_2024, lauritzen_2024, gommers_2026, oxipit_2022 |
| `w2`: Tier 2 share: all radiographs, screening mammography, standardized follow-ups | Triangular(0.1, mode 0.17, 0.25) | 0.132 / 0.173 / 0.215 | share | A | langlotz_2025 |
| `w3`: Tier 3 share: complex diagnostic CT/MR/US/NM | Triangular(0.35, mode 0.47, 0.57) | 0.401 / 0.465 / 0.523 | share | S |  |
| `tcap1_T0`: Tier 1 technical capability year (not AI-speed scaled) | Normal(μ=2025, σ=1) | 2024 / 2025 / 2026 | year | A | oxipit_2022 |
| `tcap2_T0`: Tier 2 technical capability year (M=1) | Normal(μ=2031, σ=3) | 2027 / 2031 / 2035 | year | S |  |
| `tcap3_T0`: Tier 3 technical capability year (M=1) | Normal(μ=2040, σ=5) | 2034 / 2040 / 2046 | year | S |  |
| `tcap4_T0`: Tier 4 (residual hardest work) capability year (M=1) | Normal(μ=2052, σ=8) | 2042 / 2052 / 2062 | year | S |  |
| `lval`: Clinical-validation lag (prospective, multi-site) after capability; tier-1 median | Lognormal(median=2.5, σ_log=0.4) | 1.5 / 2.5 / 4.17 | years | A | gommers_2026, lang_2023, chouffani_2024 |
| `lfda`: FDA authorization lag for autonomous claims; tier-2 median | Lognormal(median=2, σ_log=0.5) | 1.05 / 2 / 3.8 | years | A | fda_ai_2026, fda_draft_2025, aidoc_2026, deephealth_2026, abramoff_2018 |
| `lpay`: Liability + reimbursement + scope-of-practice acceptance lag; tier-2 median | Lognormal(median=4, σ_log=0.6) | 1.85 / 4 / 8.63 | years | A | abramoff_2018, bernstein_2025, mello_2024, cms_pfs_2026 |
| `ahalf`: Hospital adoption: years from 'ready' to half of eventual uptake | Lognormal(median=5.5, σ_log=0.35) | 3.51 / 5.5 / 8.61 | years | A | adler_milstein_2017, lehman_2015, wu_2024 |
| `awidth`: Autonomy adoption S-curve width | Uniform(1.5, 3.5) | 1.7 / 2.5 / 3.3 | years | S |  |
| `amax1`: Eventual uptake of tier-1 autonomy (share of eligible work) | Beta(17, 3) [mean 0.85] | 0.743 / 0.862 / 0.941 | share | S |  |
| `amax2`: Eventual uptake of tier-2 autonomy | Beta(14, 6) [mean 0.70] | 0.566 / 0.707 / 0.825 | share | S |  |
| `amax3`: Eventual uptake of tier-3 autonomy | Beta(11, 9) [mean 0.55] | 0.408 / 0.552 / 0.69 | share | S |  |
| `amax4`: Eventual uptake of tier-4 autonomy | Beta(8, 12) [mean 0.40] | 0.263 / 0.397 / 0.541 | share | S |  |
| `f_sub`: Share of interpretation+drafting time actually removed per AI-first/autonomous study | Uniform(0.6, 0.95) | 0.635 / 0.775 / 0.915 | share | S | agarwal_2023, tanno_2025 |
| `pc_share`: Professional (interpretation) share of the all-in price of an imaging exam | Triangular(0.1, mode 0.2, 0.3) | 0.145 / 0.2 / 0.255 | share | A | pc_share |
| `pass_through`: Share of cost savings passed through to prices paid | Beta(4, 6) [mean 0.40] | 0.21 / 0.393 / 0.599 | share | S |  |
| `elasticity`: Price elasticity of imaging demand | Triangular(-0.6, mode -0.2, -0.05) | -0.452 / -0.268 / -0.141 | elasticity | E | manning_1987, aron_dine_2013, brot_goldberg_2017 |
| `access`: Turnaround/availability rebound: extra work per unit of radiologist time freed | Triangular(0, mode 0.1, 0.3) | 0.0548 / 0.127 / 0.223 | ratio | A | larson_2011 |
| `new_max`: New AI-enabled imaging applications by 2066 (share of baseline work, before capacity limits) | Lognormal(median=0.18, σ_log=0.7) | 0.0734 / 0.18 / 0.441 | share | S | kwee_2025, bandi_2024, lee_2026, cms_pfs_2026, hernstrom_2025 |
| `new_T0`: Midpoint year of new-application uptake (M=1) | Normal(μ=2038, σ=4) | 2033 / 2038 / 2043 | year | S |  |
| `new_width`: New-application S-curve width | Uniform(3, 6) | 3.3 / 4.5 / 5.7 | years | S |  |
| `lambda_new`: Radiologist labour intensity of new-application work vs a typical exam | Uniform(0.4, 1) | 0.46 / 0.7 / 0.94 | ratio | S |  |
| `iota`: Extra follow-up work from AI-detected (incidental) findings at full deployment | Triangular(0, mode 0.03, 0.08) | 0.0155 / 0.0353 / 0.06 | share | A | hernstrom_2025, eisemann_2025 |
| `latent`: Latent demand currently rationed by scanner/technologist capacity | Triangular(0.02, mode 0.06, 0.12) | 0.04 / 0.0652 / 0.0955 | share | A | asrt_2025 |
| `thru_H`: AI-driven acquisition throughput gain at maturity (faster scans, auto-positioning) | Lognormal(median=0.3, σ_log=0.45) | 0.169 / 0.3 / 0.534 | share | A | johnson_2023 |
| `thru_T0`: Midpoint year of throughput gains (M=1) | Normal(μ=2032, σ=3) | 2028 / 2032 / 2036 | year | A | johnson_2023 |
| `cap_invest`: Long-run extra scanner/technologist capacity built in response to demand (by 2066) | Uniform(0, 0.25) | 0.025 / 0.125 / 0.225 | share | S | baker_2010 |
| `um_max`: AI-enabled utilization management (order decision support, payer AI prior auth) | Triangular(0, mode 0.03, 0.08) | 0.0155 / 0.0353 / 0.06 | share | A | langlotz_2025, trustees_2026 |
| `scope_max`: Reads shifting to non-radiologists with AI support by 2066 | Triangular(0, mode 0.03, 0.1) | 0.0173 / 0.0408 / 0.0735 | share | S |  |
| `nt_max`: New radiologist tasks created alongside AI (reinstatement), share of 2026 FTE | Triangular(0, mode 0.04, 0.12) | 0.0219 / 0.0507 / 0.089 | share | S | acemoglu_restrepo_2019, autor_2024, kwee_2025 |
| `attr_mult`: Attrition hazard multiplier (post-COVID ≈ high end) | Uniform(0.85, 1.2) | 0.885 / 1.02 / 1.17 | multiplier | E | christensen_supply, rula_2026, parikh_2026 |
| `slot_g`: Trend growth in DR residency positions (before market response) | Normal(μ=1, σ=0.8), truncated [-1.0, 3.0] | -0.00299 / 1 / 2 | %/yr | A | christensen_supply, nrmp_2026 |
| `resid_gamma`: Residency-position response to market signal (elasticity to ln D/S) | Uniform(0.3, 1.5) | 0.42 / 0.9 / 1.38 | elasticity | A | sharafinski_2016, rosenkrantz_2016, nicholson_2002 |
| `fill_kappa`: Fill-rate response to oversupply (applicant flight) | Uniform(0.3, 1.5) | 0.42 / 0.9 / 1.38 | elasticity | A | sharafinski_2016, shi_2015 |
| `resid_lag`: Information/perception lag before the pipeline reacts | Uniform(1, 3) | 1.2 / 2 / 2.8 | years | A | sharafinski_2016 |
| `fear`: Applicant deterrence from visible AI progress (max fill-rate loss) | Uniform(0, 0.08) | 0.008 / 0.04 / 0.072 | share | A | nrmp_2026, reeder_2022 |
| `fte_drift`: Drift in FTE per radiologist (part-time, generational preferences) | Normal(μ=-0.1, σ=0.15) | -0.292 / -0.1 / 0.0922 | %/yr | S |  |