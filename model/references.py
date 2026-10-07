"""Bibliography (AMA 11th edition style).

Each entry is keyed so that parameters, the report, and the website can cite it.
`tools/build_docs.py` numbers citations in order of first appearance per document,
as AMA style requires.
"""

REFERENCES = {
    # ---------------------------------------------------------------- workforce / utilization
    "christensen_util": {
        "ama": "Christensen EW, Drake AR, Parikh JR, Rubin EM, Rula EY. Projected US imaging utilization, 2025 to 2055. "
               "<i>J Am Coll Radiol</i>. 2025;22(2):151-158. doi:10.1016/j.jacr.2024.10.017",
        "url": "https://doi.org/10.1016/j.jacr.2024.10.017",
    },
    "christensen_supply": {
        "ama": "Christensen EW, Parikh JR, Drake AR, Rubin EM, Rula EY. Projected US radiologist supply, 2025 to 2055. "
               "<i>J Am Coll Radiol</i>. 2025;22(2):161-169. doi:10.1016/j.jacr.2024.10.019",
        "url": "https://doi.org/10.1016/j.jacr.2024.10.019",
    },
    "rula_2026": {
        "ama": "Rula EY. The radiologist shortage: a workforce update from HPI. <i>ACR Bulletin</i>. February 5, 2026. "
               "Accessed October 7, 2026. https://www.acr.org/Clinical-Resources/Publications-and-Research/ACR-Bulletin/2026/radiologist-shortage-work-force-update",
        "url": "https://www.acr.org/Clinical-Resources/Publications-and-Research/ACR-Bulletin/2026/radiologist-shortage-work-force-update",
    },
    "smith_bindman_2019": {
        "ama": "Smith-Bindman R, Kwan ML, Marlow EC, et al. Trends in use of medical imaging in US health care systems and in Ontario, "
               "Canada, 2000-2016. <i>JAMA</i>. 2019;322(9):843-856. doi:10.1001/jama.2019.11456",
        "url": "https://doi.org/10.1001/jama.2019.11456",
    },
    "smith_bindman_2025": {
        "ama": "Smith-Bindman R, Chu PW, Azman Firdaus H, et al. Projected lifetime cancer risks from current computed tomography imaging. "
               "<i>JAMA Intern Med</i>. 2025;185(6):710-719. doi:10.1001/jamainternmed.2025.0505",
        "url": "https://doi.org/10.1001/jamainternmed.2025.0505",
    },
    "mcdonald_2015": {
        "ama": "McDonald RJ, Schwartz KM, Eckel LJ, et al. The effects of changes in utilization and technological advancements of "
               "cross-sectional imaging on radiologist workload. <i>Acad Radiol</i>. 2015;22(9):1191-1198. doi:10.1016/j.acra.2015.05.007",
        "url": "https://doi.org/10.1016/j.acra.2015.05.007",
    },
    "dhanoa_2013": {
        "ama": "Dhanoa D, Dhesi TS, Burton KR, Nicolaou S, Liang T. The evolving role of the radiologist: the Vancouver workload "
               "utilization evaluation study. <i>J Am Coll Radiol</i>. 2013;10(10):764-769. doi:10.1016/j.jacr.2013.04.001",
        "url": "https://doi.org/10.1016/j.jacr.2013.04.001",
    },
    "rosenkrantz_2016": {
        "ama": "Rosenkrantz AB, Hughes DR, Duszak R Jr. The U.S. radiologist workforce: an analysis of temporal and geographic variation "
               "by using large national datasets. <i>Radiology</i>. 2016;279(1):175-184. doi:10.1148/radiol.2015150921",
        "url": "https://doi.org/10.1148/radiol.2015150921",
    },
    "sharafinski_2016": {
        "ama": "Sharafinski ME Jr, Nussbaum D, Jha S. Supply/demand in radiology: a historical perspective and comparison to other "
               "labor markets. <i>Acad Radiol</i>. 2016;23(2):245-251. doi:10.1016/j.acra.2015.10.009",
        "url": "https://doi.org/10.1016/j.acra.2015.10.009",
    },
    "shi_2015": {
        "ama": "Shi J. May the Match be ever in your favor. <i>Diagnostic Imaging</i>. May 7, 2015. Accessed October 7, 2026.",
        "url": "https://www.diagnosticimaging.com/view/may-match-be-ever-your-favor",
    },
    "nrmp_2026": {
        "ama": "National Resident Matching Program. <i>Results and Data: 2026 Main Residency Match</i>. National Resident Matching Program; 2026. "
               "Summarized in: Match Day 2026: radiology programs offer more positions than ever, but applicant pool declines. "
               "<i>Radiology Business</i>. March 20, 2026. Accessed October 7, 2026.",
        "url": "https://radiologybusiness.com/topics/healthcare-management/healthcare-staffing/match-day-2026-radiology-programs-offer-more-positions-ever-applicant-pool-declines",
    },
    "aamc_2024": {
        "ama": "Association of American Medical Colleges. <i>Physician Specialty Data Report: Active Physicians by Specialty, 2024</i>. "
               "AAMC; 2024. Accessed October 7, 2026. https://www.aamc.org/data-reports/workforce",
        "url": "https://www.aamc.org/data-reports/workforce",
    },
    "doximity_2026": {
        "ama": "Doximity. <i>2026 Physician Compensation Report</i>. Doximity; August 25, 2026. Summarized in: Radiology among top "
               "specialties for pay, compensation growth. <i>AuntMinnie</i>. 2026. Accessed October 7, 2026.",
        "url": "https://www.auntminnie.com/practice-management/news/15822383/radiology-among-top-specialties-for-pay-compensation-growth",
    },
    "asrt_2025": {
        "ama": "American Society of Radiologic Technologists. ASRT staffing and workplace survey shows vacancy rate increases near record "
               "highs. Published July 24, 2025. Accessed October 7, 2026.",
        "url": "https://www.asrt.org/main/news-publications/news/article/2025/07/24/asrt-staffing-and-workplace-survey-shows-vacancy-rate-increases-near-record-highs-aligning-with-overall-health-care-profession-trends",
    },
    "cbo_2026": {
        "ama": "Congressional Budget Office. <i>The Demographic Outlook: 2026 to 2056</i>. Publication 61879. Congressional Budget Office; January 2026.",
        "url": "https://www.cbo.gov/publication/61879",
    },
    "trustees_2026": {
        "ama": "Boards of Trustees of the Federal Hospital Insurance and Federal Supplementary Medical Insurance Trust Funds. "
               "<i>2026 Annual Report</i>. Centers for Medicare &amp; Medicaid Services; June 2026.",
        "url": "https://www.cms.gov/oact/tr",
    },
    "bandi_2024": {
        "ama": "Bandi P, Star J, Ashad-Bishop K, Kratzer T, Smith R, Jemal A. Lung cancer screening in the US, 2022. "
               "<i>JAMA Intern Med</i>. 2024;184(8):882-891. doi:10.1001/jamainternmed.2024.1655",
        "url": "https://doi.org/10.1001/jamainternmed.2024.1655",
    },
    "lee_2026": {
        "ama": "Lee MH, Garrett JW, Warner JD, Pickhardt PJ. Opportunistic screening with imaging: actionable insights from unused data. "
               "<i>Radiol Clin North Am</i>. 2026;64(3):605-621. doi:10.1016/j.rcl.2026.01.013",
        "url": "https://doi.org/10.1016/j.rcl.2026.01.013",
    },
    "baker_2010": {
        "ama": "Baker LC. Acquisition of MRI equipment by doctors drives up imaging use and spending. "
               "<i>Health Aff (Millwood)</i>. 2010;29(12):2252-2259. doi:10.1377/hlthaff.2009.1099",
        "url": "https://doi.org/10.1377/hlthaff.2009.1099",
    },
    # ---------------------------------------------------------------- AI in radiology
    "langlotz_2025": {
        "ama": "Langlotz CP. The effect of AI on the radiologist workforce: a task-based analysis. <i>medRxiv</i>. Preprint posted online "
               "December 22, 2025. doi:10.64898/2025.12.20.25342714",
        "url": "https://doi.org/10.64898/2025.12.20.25342714",
    },
    "langlotz_2019": {
        "ama": "Langlotz CP. Will artificial intelligence replace radiologists? <i>Radiol Artif Intell</i>. 2019;1(3):e190058. "
               "doi:10.1148/ryai.2019190058",
        "url": "https://doi.org/10.1148/ryai.2019190058",
    },
    "huang_2025": {
        "ama": "Huang J, Wittbrodt MT, Teague CN, et al. Efficiency and quality of generative AI-assisted radiograph reporting. "
               "<i>JAMA Netw Open</i>. 2025;8(6):e2513921. doi:10.1001/jamanetworkopen.2025.13921",
        "url": "https://doi.org/10.1001/jamanetworkopen.2025.13921",
    },
    "lang_2023": {
        "ama": "Lång K, Josefsson V, Larsson AM, et al. Artificial intelligence-supported screen reading versus standard double reading "
               "in the Mammography Screening with Artificial Intelligence trial (MASAI): a clinical safety analysis of a randomised, "
               "controlled, non-inferiority, single-blinded, screening accuracy study. <i>Lancet Oncol</i>. 2023;24(8):936-944. "
               "doi:10.1016/S1470-2045(23)00298-X",
        "url": "https://doi.org/10.1016/S1470-2045(23)00298-X",
    },
    "hernstrom_2025": {
        "ama": "Hernström V, Josefsson V, Sartor H, et al. Screening performance and characteristics of breast cancer detected in the "
               "Mammography Screening with Artificial Intelligence trial (MASAI): a randomised, controlled, parallel-group, "
               "non-inferiority, single-blinded, screening accuracy study. <i>Lancet Digit Health</i>. 2025;7(3):e175-e183. "
               "doi:10.1016/S2589-7500(24)00267-X",
        "url": "https://doi.org/10.1016/S2589-7500(24)00267-X",
    },
    "eisemann_2025": {
        "ama": "Eisemann N, Bunk S, Mukama T, et al. Nationwide real-world implementation of AI for cancer detection in "
               "population-based mammography screening. <i>Nat Med</i>. 2025;31(3):917-924. doi:10.1038/s41591-024-03408-6",
        "url": "https://doi.org/10.1038/s41591-024-03408-6",
    },
    "wenderott_2024": {
        "ama": "Wenderott K, Krups J, Zaruchas F, Weigl M. Effects of artificial intelligence implementation on efficiency in medical "
               "imaging—a systematic literature review and meta-analysis. <i>NPJ Digit Med</i>. 2024;7(1):265. "
               "doi:10.1038/s41746-024-01248-9",
        "url": "https://doi.org/10.1038/s41746-024-01248-9",
    },
    "agarwal_2023": {
        "ama": "Agarwal N, Moehring A, Rajpurkar P, Salz T. Combining human expertise with artificial intelligence: experimental "
               "evidence from radiology. NBER Working Paper 31422. National Bureau of Economic Research; 2023. doi:10.3386/w31422",
        "url": "https://doi.org/10.3386/w31422",
    },
    "rajpurkar_2023": {
        "ama": "Rajpurkar P, Lungren MP. The current and future state of AI interpretation of medical images. "
               "<i>N Engl J Med</i>. 2023;388(21):1981-1990. doi:10.1056/NEJMra2301725",
        "url": "https://doi.org/10.1056/NEJMra2301725",
    },
    "wu_2024": {
        "ama": "Wu K, Wu E, Theodorou B, et al. Characterizing the clinical adoption of medical AI devices through U.S. insurance "
               "claims. <i>NEJM AI</i>. 2024;1(1). doi:10.1056/AIoa2300030",
        "url": "https://doi.org/10.1056/AIoa2300030",
    },
    "fda_ai_2026": {
        "ama": "US Food and Drug Administration. Artificial intelligence-enabled medical devices. Updated September 2026. "
               "Accessed October 7, 2026. https://www.fda.gov/medical-devices/digital-health-center-excellence/artificial-intelligence-enabled-medical-devices",
        "url": "https://www.fda.gov/medical-devices/digital-health-center-excellence/artificial-intelligence-enabled-medical-devices",
    },
    "bernstein_2025": {
        "ama": "Bernstein MH, Sheppard B, Bruno MA, Lay PS, Baird GL. Randomized study of the impact of AI on perceived legal "
               "liability for radiologists. <i>NEJM AI</i>. 2025;2(6). doi:10.1056/AIoa2400785",
        "url": "https://doi.org/10.1056/AIoa2400785",
    },
    "abramoff_2018": {
        "ama": "Abràmoff MD, Lavin PT, Birch M, Shah N, Folk JC. Pivotal trial of an autonomous AI-based diagnostic system for "
               "detection of diabetic retinopathy in primary care offices. <i>NPJ Digit Med</i>. 2018;1:39. doi:10.1038/s41746-018-0040-6",
        "url": "https://doi.org/10.1038/s41746-018-0040-6",
    },
    "oxipit_2022": {
        "ama": "AI enters the radiology department: ChestLink, an AI x-ray tool approved by European officials. <i>The Batch</i>. "
               "DeepLearning.AI; 2022. Accessed October 7, 2026.",
        "url": "https://www.deeplearning.ai/the-batch/ai-enters-the-radiology-department",
    },
    "cms_pfs_2026": {
        "ama": "Medicare Physician Fee Schedule includes CPT code, $1,000 payment amount for imaging AI software. "
               "<i>Radiology Business</i>. 2025. Accessed October 7, 2026.",
        "url": "https://radiologybusiness.com/topics/artificial-intelligence/medicare-physician-fee-schedule-includes-cpt-code-1000-payment-amount-imaging-ai-software",
    },
    "johnson_2023": {
        "ama": "Johnson PM, Lin DJ, Zbontar J, et al. Deep learning reconstruction enables prospectively accelerated clinical knee MRI. "
               "<i>Radiology</i>. 2023;307(2):e220425. doi:10.1148/radiol.220425",
        "url": "https://doi.org/10.1148/radiol.220425",
    },
    "mousa_2025": {
        "ama": "Mousa D. AI isn’t replacing radiologists. <i>Works in Progress</i>. 2025. Accessed October 7, 2026.",
        "url": "https://worksinprogress.co/",
    },
    "hinton_2016": {
        "ama": "Hinton G. Remarks at: Machine Learning and the Market for Intelligence conference; 2016; Creative Destruction Lab, "
               "University of Toronto, Toronto, Ontario, Canada.",
        "url": None,
    },
    "lehman_2015": {
        "ama": "Lehman CD, Wellman RD, Buist DSM, Kerlikowske K, Tosteson ANA, Miglioretti DL; Breast Cancer Surveillance Consortium. "
               "Diagnostic accuracy of digital screening mammography with and without computer-aided detection. "
               "<i>JAMA Intern Med</i>. 2015;175(11):1828-1837. doi:10.1001/jamainternmed.2015.5231",
        "url": "https://doi.org/10.1001/jamainternmed.2015.5231",
    },
    "larson_2011": {
        "ama": "Larson DB, Johnson LW, Schnell BM, Salisbury SR, Forman HP. National trends in CT use in the emergency department: "
               "1995-2007. <i>Radiology</i>. 2011;258(1):164-173. doi:10.1148/radiol.10100640",
        "url": "https://doi.org/10.1148/radiol.10100640",
    },
    "adler_milstein_2017": {
        "ama": "Adler-Milstein J, Jha AK. HITECH Act drove large gains in hospital electronic health record adoption. "
               "<i>Health Aff (Millwood)</i>. 2017;36(8):1416-1422. doi:10.1377/hlthaff.2016.1651",
        "url": "https://doi.org/10.1377/hlthaff.2016.1651",
    },
    # ---------------------------------------------------------------- economics
    "acemoglu_restrepo_2019": {
        "ama": "Acemoglu D, Restrepo P. Automation and new tasks: how technology displaces and reinstates labor. "
               "<i>J Econ Perspect</i>. 2019;33(2):3-30. doi:10.1257/jep.33.2.3",
        "url": "https://doi.org/10.1257/jep.33.2.3",
    },
    "acemoglu_restrepo_2018": {
        "ama": "Acemoglu D, Restrepo P. The race between man and machine: implications of technology for growth, factor shares, "
               "and employment. <i>Am Econ Rev</i>. 2018;108(6):1488-1542. doi:10.1257/aer.20160696",
        "url": "https://doi.org/10.1257/aer.20160696",
    },
    "autor_2024": {
        "ama": "Autor D, Chin C, Salomons A, Seegmiller B. New frontiers: the origins and content of new work, 1940-2018. "
               "<i>Q J Econ</i>. 2024;139(3):1399-1465. doi:10.1093/qje/qjae008",
        "url": "https://doi.org/10.1093/qje/qjae008",
    },
    "bessen_2019": {
        "ama": "Bessen J. Automation and jobs: when technology boosts employment. <i>Econ Policy</i>. 2019;34(100):589-626. "
               "doi:10.1093/epolic/eiaa001",
        "url": "https://doi.org/10.1093/epolic/eiaa001",
    },
    "jevons_1865": {
        "ama": "Jevons WS. <i>The Coal Question: An Inquiry Concerning the Progress of the Nation, and the Probable Exhaustion of Our "
               "Coal-Mines</i>. Macmillan and Co; 1865.",
        "url": "https://oll.libertyfund.org/titles/jevons-the-coal-question",
    },
    "manning_1987": {
        "ama": "Manning WG, Newhouse JP, Duan N, Keeler EB, Leibowitz A, Marquis MS. Health insurance and the demand for medical care: "
               "evidence from a randomized experiment. <i>Am Econ Rev</i>. 1987;77(3):251-277.",
        "url": "https://www.jstor.org/stable/1804094",
    },
    "aron_dine_2013": {
        "ama": "Aron-Dine A, Einav L, Finkelstein A. The RAND Health Insurance Experiment, three decades later. "
               "<i>J Econ Perspect</i>. 2013;27(1):197-222. doi:10.1257/jep.27.1.197",
        "url": "https://doi.org/10.1257/jep.27.1.197",
    },
    "brot_goldberg_2017": {
        "ama": "Brot-Goldberg ZC, Chandra A, Handel BR, Kolstad JT. What does a deductible do? The impact of cost-sharing on health "
               "care prices, quantities, and spending dynamics. <i>Q J Econ</i>. 2017;132(3):1261-1318. doi:10.1093/qje/qjx013",
        "url": "https://doi.org/10.1093/qje/qjx013",
    },
    "nicholson_2002": {
        "ama": "Nicholson S. Physician specialty choice under uncertainty. <i>J Labor Econ</i>. 2002;20(4):816-847. doi:10.1086/342039",
        "url": "https://doi.org/10.1086/342039",
    },
    "pc_share": {
        "ama": "Radiology alignment: common structures and the value of radiologists’ services. <i>Radiology Business</i>. "
               "Accessed October 7, 2026.",
        "url": "https://radiologybusiness.com/sponsored/1067/vmg/topics/healthcare-management/business-intelligence/radiology-alignment-common-structures-and-value-radiologists-services",
    },
    # ---------------------------------------------------------------- forecasting & AI progress
    "tetlock_2015": {
        "ama": "Tetlock PE, Gardner D. <i>Superforecasting: The Art and Science of Prediction</i>. Crown; 2015.",
        "url": "https://en.wikipedia.org/wiki/Superforecasting",
    },
    "mellers_2014": {
        "ama": "Mellers B, Ungar L, Baron J, et al. Psychological strategies for winning a geopolitical forecasting tournament. "
               "<i>Psychol Sci</i>. 2014;25(5):1106-1115. doi:10.1177/0956797614524255",
        "url": "https://doi.org/10.1177/0956797614524255",
    },
    "kahneman_1993": {
        "ama": "Kahneman D, Lovallo D. Timid choices and bold forecasts: a cognitive perspective on risk taking. "
               "<i>Manage Sci</i>. 1993;39(1):17-31. doi:10.1287/mnsc.39.1.17",
        "url": "https://doi.org/10.1287/mnsc.39.1.17",
    },
    "metaculus": {
        "ama": "Metaculus. Track record. Accessed October 7, 2026. https://www.metaculus.com/questions/track-record/",
        "url": "https://www.metaculus.com/questions/track-record/",
    },
    "karger_2023": {
        "ama": "Karger E, Rosenberg J, Jacobs Z, et al. <i>Forecasting Existential Risk: Evidence From a Long-Run Forecasting "
               "Tournament</i>. Forecasting Research Institute Working Paper No. 1; 2023.",
        "url": "https://forecastingresearch.org/xpt",
    },
    "ai2027": {
        "ama": "Kokotajlo D, Alexander S, Larsen T, Lifland E, Dean R. AI 2027. AI Futures Project. Published April 3, 2025. "
               "Accessed October 7, 2026. https://ai-2027.com",
        "url": "https://ai-2027.com",
    },
    "metr_2025": {
        "ama": "Kwa T, West B, Becker J, et al. Measuring AI ability to complete long tasks. <i>arXiv</i>. Preprint posted online "
               "March 18, 2025. doi:10.48550/arXiv.2503.14499",
        "url": "https://doi.org/10.48550/arXiv.2503.14499",
    },
    "metr_2026": {
        "ama": "METR. Time Horizon 1.1. METR; January 2026. Accessed October 7, 2026. https://metr.org/notes/2026-01-22-time-horizon-limitations/",
        "url": "https://metr.org/notes/2026-01-22-time-horizon-limitations/",
    },
}


def ama(key: str) -> str:
    return REFERENCES[key]["ama"]
