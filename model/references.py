"""Bibliography in structured form, rendered to AMA Manual of Style (11th ed.) by `format_ama`.

Every entry has a clickable link: a DOI (rendered as doi:10.xxxx, linked to https://doi.org/...) or a URL
(rendered with an access date). Titles of articles are stored in sentence case; journal names use NLM
abbreviations. `tools/build_docs.py` and the website number citations in order of first appearance.
"""
from __future__ import annotations

import html

ACCESSED = "October 7, 2026"


def J(authors, title, journal, year, vol=None, issue=None, pages=None, doi=None, url=None, group=None):
    return dict(type="journal", authors=authors, title=title, journal=journal, year=year, vol=vol, issue=issue,
                pages=pages, doi=doi, url=url, group=group)


def PRE(authors, title, server, posted, doi=None, url=None):
    return dict(type="preprint", authors=authors, title=title, server=server, posted=posted, doi=doi, url=url)


def WP(authors, title, series, publisher, year, doi=None, url=None, published=None):
    return dict(type="workingpaper", authors=authors, title=title, series=series, publisher=publisher, year=year,
                doi=doi, url=url, published=published)


def WEB(authors, title, site, url, published=None, updated=None):
    """Web page / news article. `authors` may be [] (AMA then starts with the title) or an organization."""
    return dict(type="web", authors=authors, title=title, site=site, url=url, published=published, updated=updated)


def REPORT(authors, title, publisher, year, url, number=None, published=None):
    return dict(type="report", authors=authors, title=title, publisher=publisher, year=year, url=url, number=number,
                published=published)


def BOOK(authors, title, publisher, year, url=None):
    return dict(type="book", authors=authors, title=title, publisher=publisher, year=year, url=url)


def VIDEO(authors, title, event, site, published, url):
    return dict(type="video", authors=authors, title=title, event=event, site=site, published=published, url=url)


REFERENCES: dict[str, dict] = {
    # ===================================================================== workforce, utilization, market
    "christensen_util": J(["Christensen EW", "Drake AR", "Parikh JR", "Rubin EM", "Rula EY"],
                          "Projected US imaging utilization, 2025 to 2055", "J Am Coll Radiol", 2025, 22, 2, "151-158",
                          "10.1016/j.jacr.2024.10.017"),
    "christensen_supply": J(["Christensen EW", "Parikh JR", "Drake AR", "Rubin EM", "Rula EY"],
                            "Projected US radiologist supply, 2025 to 2055", "J Am Coll Radiol", 2025, 22, 2, "161-169",
                            "10.1016/j.jacr.2024.10.019"),
    "parikh_2026": J(["Parikh JR", "Drake AR", "Rula EY", "Golding E", "Christensen EW"],
                     "Radiologist turnover in the United States", "J Am Coll Radiol", 2026, 23, 6, "1058-1066",
                     "10.1016/j.jacr.2026.01.009"),
    "zamani_2026": J(["Zamani H", "Fruscello T", "Burleson J", "Bhargavan-Chatfield M", "Davenport MS"],
                     "US radiology imaging and workforce volumes 2017-2024: an analysis of 46.4 million imaging "
                     "examinations from 167 radiology facilities", "J Am Coll Radiol", 2026, 23, 6, "1041-1048",
                     "10.1016/j.jacr.2025.12.026"),
    "rula_2026": WEB(["Rula EY"], "The radiologist shortage: a workforce update from HPI", "ACR Bulletin",
                     "https://www.acr.org/Clinical-Resources/Publications-and-Research/ACR-Bulletin/2026/radiologist-shortage-work-force-update",
                     published="February 5, 2026"),
    "rcr_2026": REPORT(["Royal College of Radiologists"], "Clinical Radiology Workforce Census 2025",
                       "Royal College of Radiologists", 2026,
                       "https://www.rcr.ac.uk/media/n1fjvrv4/rcr-2025-clinical-radiology-workforce-census-report.pdf"),
    "smith_bindman_2019": J(["Smith-Bindman R", "Kwan ML", "Marlow EC", "Theis MK", "Bolch W", "Cheng SY", "Bowles EJA"],
                            "Trends in use of medical imaging in US health care systems and in Ontario, Canada, 2000-2016",
                            "JAMA", 2019, 322, 9, "843-856", "10.1001/jama.2019.11456"),
    "smith_bindman_2025": J(["Smith-Bindman R", "Chu PW", "Azman Firdaus H", "Stewart C", "Malekhedayat M", "Alber S", "Bolch WE"],
                            "Projected lifetime cancer risks from current computed tomography imaging",
                            "JAMA Intern Med", 2025, 185, 6, "710-719", "10.1001/jamainternmed.2025.0505"),
    "rosenkrantz_2025": J(["Rosenkrantz AB", "Cummings RW"],
                          "Utilization of emergency department imaging from 2013 to 2023: a national Medicare analysis",
                          "Radiology", 2025, 316, 3, "e251395", "10.1148/radiol.251395"),
    "mcdonald_2015": J(["McDonald RJ", "Schwartz KM", "Eckel LJ", "Diehn FE", "Hunt CH", "Bartholmai BJ", "Erickson BJ"],
                       "The effects of changes in utilization and technological advancements of cross-sectional imaging "
                       "on radiologist workload", "Acad Radiol", 2015, 22, 9, "1191-1198", "10.1016/j.acra.2015.05.007"),
    "dhanoa_2013": J(["Dhanoa D", "Dhesi TS", "Burton KR", "Nicolaou S", "Liang T"],
                     "The evolving role of the radiologist: the Vancouver workload utilization evaluation study",
                     "J Am Coll Radiol", 2013, 10, 10, "764-769", "10.1016/j.jacr.2013.04.001"),
    "rosenkrantz_2016": J(["Rosenkrantz AB", "Hughes DR", "Duszak R Jr"],
                          "The U.S. radiologist workforce: an analysis of temporal and geographic variation by using "
                          "large national datasets", "Radiology", 2016, 279, 1, "175-184", "10.1148/radiol.2015150921"),
    "sharafinski_2016": J(["Sharafinski ME Jr", "Nussbaum D", "Jha S"],
                          "Supply/demand in radiology: a historical perspective and comparison to other labor markets",
                          "Acad Radiol", 2016, 23, 2, "245-251", "10.1016/j.acra.2015.10.009"),
    "shi_2015": WEB(["Shi J"], "May the Match be ever in your favor", "Diagnostic Imaging",
                    "https://www.diagnosticimaging.com/view/may-match-be-ever-your-favor", published="May 7, 2015"),
    "nrmp_2026": WEB([], "Match Day 2026: radiology programs offer more positions than ever, but applicant pool declines",
                     "Radiology Business",
                     "https://radiologybusiness.com/topics/healthcare-management/healthcare-staffing/match-day-2026-radiology-programs-offer-more-positions-ever-applicant-pool-declines",
                     published="March 20, 2026"),
    "aamc_2024": WEB(["Association of American Medical Colleges"], "Active physicians in the largest specialties, 2024",
                     "AAMC Physician Specialty Data Report",
                     "https://www.aamc.org/data-reports/workforce/data/active-physicians-largest-specialties-2024"),
    "doximity_2026": WEB([], "Interventional radiology tops compensation growth in 2025", "AuntMinnie",
                         "https://www.auntminnie.com/home/news/15833258/interventional-radiology-tops-compensation-growth-in-2025",
                         published="August 25, 2026"),
    "asrt_2025": WEB(["American Society of Radiologic Technologists"],
                     "ASRT staffing and workplace survey shows vacancy rate increases near record highs aligning with "
                     "overall health care profession trends", "ASRT News",
                     "https://www.asrt.org/main/news-publications/news/article/2025/07/24/asrt-staffing-and-workplace-survey-shows-vacancy-rate-increases-near-record-highs-aligning-with-overall-health-care-profession-trends",
                     published="July 24, 2025"),
    "cbo_2026": REPORT(["Congressional Budget Office"], "The Demographic Outlook: 2026 to 2056", "Congressional Budget Office",
                       2026, "https://www.cbo.gov/publication/61879", number="Publication 61879", published="January 2026"),
    "trustees_2026": REPORT(["Boards of Trustees of the Federal Hospital Insurance and Federal Supplementary Medical Insurance Trust Funds"],
                            "2026 Annual Report of the Boards of Trustees of the Federal Hospital Insurance and Federal "
                            "Supplementary Medical Insurance Trust Funds", "Centers for Medicare & Medicaid Services", 2026,
                            "https://www.cms.gov/oact/tr", published="June 9, 2026"),
    "bandi_2024": J(["Bandi P", "Star J", "Ashad-Bishop K", "Kratzer T", "Smith R", "Jemal A"], "Lung cancer screening in the US, 2022",
                    "JAMA Intern Med", 2024, 184, 8, "882-891", "10.1001/jamainternmed.2024.1655"),
    "lee_2026": J(["Lee MH", "Garrett JW", "Warner JD", "Pickhardt PJ"],
                  "Opportunistic screening with imaging: actionable insights from unused data", "Radiol Clin North Am",
                  2026, 64, 3, "605-621", "10.1016/j.rcl.2026.01.013"),
    "baker_2010": J(["Baker LC"], "Acquisition of MRI equipment by doctors drives up imaging use and spending",
                    "Health Aff (Millwood)", 2010, 29, 12, "2252-2259", "10.1377/hlthaff.2009.1099"),
    "kwee_2025": J(["Kwee TC", "Kwee RM"],
                   "Workload of diagnostic radiologists in the foreseeable future based on recent (2024) scientific "
                   "advances: updated growth expectations", "Eur J Radiol", 2025, 187, None, "112103",
                   "10.1016/j.ejrad.2025.112103"),
    "reeder_2022": J(["Reeder K", "Lee H"], "Impact of artificial intelligence on US medical students' choice of radiology",
                     "Clin Imaging", 2022, 81, None, "67-71", "10.1016/j.clinimag.2021.09.018"),
    "larson_2011": J(["Larson DB", "Johnson LW", "Schnell BM", "Salisbury SR", "Forman HP"],
                     "National trends in CT use in the emergency department: 1995-2007", "Radiology", 2011, 258, 1,
                     "164-173", "10.1148/radiol.10100640"),
    # ===================================================================== AI in radiology: evidence
    "langlotz_2025": PRE(["Langlotz CP"], "The effect of AI on the radiologist workforce: a task-based analysis", "medRxiv",
                         "December 22, 2025", "10.64898/2025.12.20.25342714"),
    "langlotz_2019": J(["Langlotz CP"], "Will artificial intelligence replace radiologists?", "Radiol Artif Intell", 2019, 1, 3,
                       "e190058", "10.1148/ryai.2019190058"),
    "huang_2025": J(["Huang J", "Wittbrodt MT", "Teague CN", "Karl E", "Galal G", "Thompson M", "Chapa A"],
                    "Efficiency and quality of generative AI-assisted radiograph reporting", "JAMA Netw Open", 2025, 8, 6,
                    "e2513921", "10.1001/jamanetworkopen.2025.13921"),
    "hong_2025": J(["Hong EK", "Roh B", "Park B", "Jo JB", "Bae W", "Soung Park J", "Sung DW"],
                   "Value of using a generative AI model in chest radiography reporting: a reader study", "Radiology",
                   2025, 314, 3, "e241646", "10.1148/radiol.241646"),
    "liu_2026": J(["Liu W", "Wu Y", "Yu W", "Bittle MJ", "Zheng Z", "Kharrazi H"],
                  "Measuring the impact of AI on report-drafting efficiency in chest computed tomography interpretation: "
                  "retrospective analysis", "J Med Internet Res", 2026, 28, None, "e77967", "10.2196/77967"),
    "li_2026": J(["Li M", "Wang Y", "Miao Z", "Gong J", "Yang S", "Xue H", "Yang Q"],
                 "Fine-tuned large language model for automated radiology impression generation: a multicenter evaluation",
                 "Radiol Artif Intell", 2026, 8, 3, "e250714", "10.1148/ryai.250714"),
    "tanno_2025": J(["Tanno R", "Barrett DGT", "Sellergren A", "Ghaisas S", "Dathathri S", "See A", "Welbl J"],
                    "Collaboration between clinicians and vision-language models in radiology report generation", "Nat Med",
                    2025, 31, 2, "599-608", "10.1038/s41591-024-03302-1"),
    "lang_2023": J(["Lång K", "Josefsson V", "Larsson AM", "Larsson S", "Högberg C", "Sartor H", "Hofvind S"],
                   "Artificial intelligence-supported screen reading versus standard double reading in the Mammography "
                   "Screening with Artificial Intelligence trial (MASAI): a clinical safety analysis of a randomised, "
                   "controlled, non-inferiority, single-blinded, screening accuracy study", "Lancet Oncol", 2023, 24, 8,
                   "936-944", "10.1016/S1470-2045(23)00298-X"),
    "hernstrom_2025": J(["Hernström V", "Josefsson V", "Sartor H", "Schmidt D", "Larsson AM", "Hofvind S", "Andersson I"],
                        "Screening performance and characteristics of breast cancer detected in the Mammography Screening "
                        "with Artificial Intelligence trial (MASAI): a randomised, controlled, parallel-group, "
                        "non-inferiority, single-blinded, screening accuracy study", "Lancet Digit Health", 2025, 7, 3,
                        "e175-e183", "10.1016/S2589-7500(24)00267-X"),
    "gommers_2026": J(["Gommers J", "Hernström V", "Josefsson V", "Sartor H", "Schmidt D", "Hjelmgren A", "Larsson AM"],
                      "Interval cancer, sensitivity, and specificity comparing AI-supported mammography screening with "
                      "standard double reading without AI in the MASAI study: a randomised, controlled, non-inferiority, "
                      "single-blinded, population-based, screening-accuracy trial", "Lancet", 2026, 407, 10527, "505-514",
                      "10.1016/S0140-6736(25)02464-X"),
    "lauritzen_2024": J(["Lauritzen AD", "Lillholm M", "Lynge E", "Nielsen M", "Karssemeijer N", "Vejborg I"],
                        "Early indicators of the impact of using AI in mammography screening for breast cancer", "Radiology",
                        2024, 311, 3, "e232479", "10.1148/radiol.232479"),
    "eisemann_2025": J(["Eisemann N", "Bunk S", "Mukama T", "Baltus H", "Elsner SA", "Gomille T", "Hecht G"],
                       "Nationwide real-world implementation of AI for cancer detection in population-based mammography "
                       "screening", "Nat Med", 2025, 31, 3, "917-924", "10.1038/s41591-024-03408-6"),
    "plesner_2023": J(["Plesner LL", "Müller FC", "Nybing JD", "Laustrup LC", "Rasmussen F", "Nielsen OW", "Boesen M"],
                      "Autonomous chest radiograph reporting using AI: estimation of clinical impact", "Radiology", 2023,
                      307, 3, "e222268", "10.1148/radiol.222268"),
    "plesner_2024": J(["Plesner LL", "Müller FC", "Brejnebøl MW", "Krag CH", "Laustrup LC", "Rasmussen F", "Nielsen OW"],
                      "Using AI to identify unremarkable chest radiographs for automatic reporting", "Radiology", 2024,
                      312, 2, "e240272", "10.1148/radiol.240272"),
    "wenderott_2024": J(["Wenderott K", "Krups J", "Zaruchas F", "Weigl M"],
                        "Effects of artificial intelligence implementation on efficiency in medical imaging-a systematic "
                        "literature review and meta-analysis", "NPJ Digit Med", 2024, 7, 1, "265",
                        "10.1038/s41746-024-01248-9"),
    "yu_2024": J(["Yu F", "Moehring A", "Banerjee O", "Salz T", "Agarwal N", "Rajpurkar P"],
                 "Heterogeneity and predictors of the effects of AI assistance on radiologists", "Nat Med", 2024, 30, 3,
                 "837-849", "10.1038/s41591-024-02850-w"),
    "agarwal_2023": WP(["Agarwal N", "Moehring A", "Rajpurkar P", "Salz T"],
                       "Combining human expertise with artificial intelligence: experimental evidence from radiology",
                       "NBER Working Paper 31422", "National Bureau of Economic Research", 2023, doi="10.3386/w31422"),
    "rajpurkar_2023": J(["Rajpurkar P", "Lungren MP"], "The current and future state of AI interpretation of medical images",
                        "N Engl J Med", 2023, 388, 21, "1981-1990", "10.1056/NEJMra2301725"),
    "malhotra_2026": J(["Malhotra A", "Kandala K", "Futela D", "Payabvash S", "Lakhani DA", "Gandhi D", "Whitlow C", "Duszak R"],
                       "The evolving US radiologist pipeline: trends in residency positions, resident workforce, and practicing radiologists per unit population",
                       "J Am Coll Radiol", 2026, 23, 8, "1587-1592", "10.1016/j.jacr.2026.04.005"),
    "ghuwalewala_2022": J(["Ghuwalewala S", "Kulkarni V", "Pant R", "Kharat A"], "Levels of autonomous radiology",
                          "Interact J Med Res", 2022, 11, 2, "e38655", "10.2196/38655"),
    # ===================================================================== radiology job-market history (history test)
    "forman_2000": J(["Forman HP", "Kamin DS", "Covey AM", "Sunshine JH"],
                     "Changes in the market for diagnostic radiologists as measured through a help wanted index",
                     "AJR Am J Roentgenol", 2000, 174, 4, "933-938", "10.2214/ajr.174.4.1740933"),
    "covey_2000": J(["Covey AM", "Sunshine J", "Forman HP"],
                    "The job market in diagnostic radiology 1999: updated findings from a help wanted index of job advertisements",
                    "AJR Am J Roentgenol", 2000, 175, 4, "957-961", "10.2214/ajr.175.4.1750957"),
    "sunshine_2004": J(["Sunshine JH", "Maynard CD", "Paros J", "Forman HP"], "Update on the diagnostic radiologist shortage",
                       "AJR Am J Roentgenol", 2004, 182, 2, "301-305", "10.2214/ajr.182.2.1820301"),
    "meghea_2005": J(["Meghea CI", "Sunshine JH"],
                     "Who's overworked and who's underworked among radiologists? An update on the radiologist shortage",
                     "Radiology", 2005, 236, 3, "932-938", "10.1148/radiol.2363041885"),
    "sunshine_2007": J(["Sunshine JH", "Maynard CD"], "Update on the diagnostic radiology employment market: findings through 2006-2007",
                       "J Am Coll Radiol", 2007, 4, 10, "686-690", "10.1016/j.jacr.2007.06.015"),
    "bhargavan_2009": J(["Bhargavan M", "Kaye AH", "Forman HP", "Sunshine JH"],
                        "Workload of radiologists in United States in 2006-2007 and trends since 1991-1992",
                        "Radiology", 2009, 252, 2, "458-467", "10.1148/radiol.2522081895"),
    "levin_2011": J(["Levin DC", "Rao VM", "Parker L", "Frangos AJ", "Sunshine JH"],
                    "Bending the curve: the recent marked slowdown in growth of noninvasive diagnostic imaging",
                    "AJR Am J Roentgenol", 2011, 196, 1, "W25-W29", "10.2214/AJR.10.4835"),
    "levin_2017": J(["Levin DC", "Parker L", "Palit CD", "Rao VM"],
                    "After nearly a decade of rapid growth, use and complexity of imaging declined, 2008-14",
                    "Health Aff (Millwood)", 2017, 36, 4, "663-670", "10.1377/hlthaff.2016.0836"),
    "hong_2020": J(["Hong AS", "Levin D", "Parker L", "Rao VM", "Ross-Degnan D", "Wharam JF"],
                   "Trends in diagnostic imaging utilization among Medicare and commercially insured adults from 2003 through 2016",
                   "Radiology", 2020, 294, 2, "342-350", "10.1148/radiol.2019191116"),
    "bluth_2012": J(["Bluth EI", "Short BW", "Willis-Walton S"], "2012 ACR Commission on Human Resources workforce survey",
                    "J Am Coll Radiol", 2012, 9, 9, "625-629", "10.1016/j.jacr.2012.06.001"),
    "bluth_2014": J(["Bluth EI", "Truong H", "Bansal S"], "The 2014 ACR Commission on Human Resources workforce survey",
                    "J Am Coll Radiol", 2014, 11, 10, "948-952", "10.1016/j.jacr.2014.06.003"),
    "bluth_2015": J(["Bluth EI", "Cox J", "Bansal S", "Green D"], "The 2015 ACR Commission on Human Resources workforce survey",
                    "J Am Coll Radiol", 2015, 12, 11, "1137-1141", "10.1016/j.jacr.2015.06.009"),
    "bluth_2016": J(["Bluth EI", "Bansal S"], "The 2016 ACR Commission on Human Resources workforce survey",
                    "J Am Coll Radiol", 2016, 13, 10, "1227-1232", "10.1016/j.jacr.2016.06.006"),
    "bender_2019": J(["Bender CE", "Bansal S", "Wolfman D", "Parikh JR"], "2018 ACR Commission on Human Resources workforce survey",
                     "J Am Coll Radiol", 2019, 16, "4 pt A", "508-512", "10.1016/j.jacr.2018.12.034"),
    "pfeifer_2017": J(["Pfeifer CM"], "Radiology resident supply and demand: a regional perspective", "J Am Coll Radiol", 2017,
                      14, 9, "1161-1168", "10.1016/j.jacr.2017.05.016"),
    "dibble_2025": J(["Dibble EH", "Rubin E", "Parikh JR"],
                     "Workforce shortage and strategies for mitigation: results from the 2022 ACR/Radiology Business Management "
                     "Association workforce survey", "J Am Coll Radiol", 2025, 22, 5, "573-576", "10.1016/j.jacr.2025.01.012"),
    "census_pop": WEB(["US Census Bureau"], "Historical population change data (1910-2020)", "US Census Bureau",
                      "https://www.census.gov/data/tables/time-series/dec/popchange-data-text.html", published="April 26, 2021"),
    "mgma_2007": WEB([], "Inflation swamps specialty salaries, but radiologists stay afloat", "AuntMinnie",
                     "https://www.auntminnie.com/practice-management/careers/article/15583656/inflation-swamps-specialty-salaries-but-radiologists-stay-afloat",
                     published="August 31, 2007"),
    "mgma_2009": WEB([], "Rad salaries don't keep pace with inflation", "AuntMinnie",
                     "https://www.auntminnie.com/practice-management/careers/article/15591508/rad-salaries-dont-keep-pace-with-inflation",
                     published="June 25, 2009"),
    "mgma_2011": WEB([], "MGMA: radiologist salaries dip 1.6% in 2010", "AuntMinnie",
                     "https://www.auntminnie.com/practice-management/careers/article/15599556/mgma-radiologist-salaries-dip-16-in-2010",
                     published="June 16, 2011"),
    "amga_2015": WEB(["RSNA News"], "Radiologists see increased pay for second year", "RSNA",
                     "https://www.rsna.org/news/2015/december/radiologists-see-increased-pay-for-second-year", published="December 1, 2015"),
    "doximity_2023": WEB([], "Radiologists among top 10 highest paid medical specialists in 2022", "AuntMinnie",
                         "https://www.auntminnie.com/practice-management/article/15633149/radiologists-among-top-10-highest-paid-medical-specialists-in-2022",
                         published="March 30, 2023"),
    "doximity_2024": WEB([], "Radiology, radiation oncology among highest paid medical specialties", "AuntMinnie",
                         "https://www.auntminnie.com/practice-management/article/15673416/radiology-radiation-oncology-among-highest-paid-medical-specialties",
                         published="May 23, 2024"),
    "doximity_2025": WEB([], "Doximity: radiology makes top 5 specialties for compensation growth", "AuntMinnie",
                         "https://www.auntminnie.com/industry-news/market-analysis/article/15751929/doximity-radiology-makes-top-5-specialties-for-compensation-growth",
                         published="July 31, 2025"),
    "wu_2024": J(["Wu K", "Wu E", "Theodorou B", "Liang W", "Mack C", "Glass L", "Sun J"],
                 "Characterizing the clinical adoption of medical AI devices through U.S. insurance claims", "NEJM AI",
                 2024, 1, 1, None, "10.1056/AIoa2300030"),
    "allen_2021": J(["Allen B", "Agarwal S", "Coombs L", "Wald C", "Dreyer K"],
                    "2020 ACR Data Science Institute artificial intelligence survey", "J Am Coll Radiol", 2021, 18, 8,
                    "1153-1159", "10.1016/j.jacr.2021.04.002"),
    "liu_burnout_2024": J(["Liu H", "Ding N", "Li X", "Chen Y", "Sun H", "Huang Y", "Liu C"],
                          "Artificial intelligence and radiologist burnout", "JAMA Netw Open", 2024, 7, 11, "e2448714",
                          "10.1001/jamanetworkopen.2024.48714"),
    "johnson_2023": J(["Johnson PM", "Lin DJ", "Zbontar J", "Zitnick CL", "Sriram A", "Muckley M", "Babb JS"],
                      "Deep learning reconstruction enables prospectively accelerated clinical knee MRI", "Radiology",
                      2023, 307, 2, "e220425", "10.1148/radiol.220425"),
    "lehman_2015": J(["Lehman CD", "Wellman RD", "Buist DSM", "Kerlikowske K", "Tosteson ANA", "Miglioretti DL"],
                     "Diagnostic accuracy of digital screening mammography with and without computer-aided detection",
                     "JAMA Intern Med", 2015, 175, 11, "1828-1837", "10.1001/jamainternmed.2015.5231",
                     group="Breast Cancer Surveillance Consortium"),
    "adler_milstein_2017": J(["Adler-Milstein J", "Jha AK"],
                             "HITECH Act drove large gains in hospital electronic health record adoption",
                             "Health Aff (Millwood)", 2017, 36, 8, "1416-1422", "10.1377/hlthaff.2016.1651"),
    "mousa_2025": WEB(["Mousa D"], "AI isn't replacing radiologists", "Works in Progress",
                      "https://www.worksinprogress.news/p/why-ai-isnt-replacing-radiologists", published="September 2025"),
    "hinton_2016": VIDEO(["Hinton G"], "Geoff Hinton: on radiology",
                         "Machine Learning and the Market for Intelligence; 2016; Toronto, Ontario, Canada",
                         "Creative Destruction Lab YouTube channel", "November 24, 2016",
                         "https://www.youtube.com/watch?v=2HMPRXstSvQ"),
    # ===================================================================== regulation, liability, payment
    "fda_ai_2026": WEB(["US Food and Drug Administration"], "Artificial intelligence-enabled medical devices", "FDA",
                       "https://www.fda.gov/medical-devices/digital-health-center-excellence/artificial-intelligence-enabled-medical-devices",
                       updated="September 2026"),
    "fda_draft_2025": REPORT(["US Food and Drug Administration"],
                             "Artificial Intelligence-Enabled Device Software Functions: Lifecycle Management and Marketing "
                             "Submission Recommendations. Draft Guidance for Industry and Food and Drug Administration Staff",
                             "US Food and Drug Administration", 2025,
                             "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/artificial-intelligence-enabled-device-software-functions-lifecycle-management-and-marketing",
                             published="January 7, 2025"),
    "chouffani_2024": J(["Chouffani El Fassi S", "Abdullah A", "Fang Y", "Natarajan S", "Masroor AB", "Kayali N", "Prakash S"],
                        "Not all AI health tools with regulatory authorization are clinically validated", "Nat Med", 2024,
                        30, 10, "2718-2720", "10.1038/s41591-024-03203-3"),
    "abramoff_2018": J(["Abràmoff MD", "Lavin PT", "Birch M", "Shah N", "Folk JC"],
                       "Pivotal trial of an autonomous AI-based diagnostic system for detection of diabetic retinopathy "
                       "in primary care offices", "NPJ Digit Med", 2018, 1, None, "39", "10.1038/s41746-018-0040-6"),
    "oxipit_2022": WEB(["Oxipit"], "CE mark for first autonomous AI medical imaging application", "Oxipit News",
                       "https://oxipit.ai/news/first-autonomous-ai-medical-imaging-application/", published="2022"),
    "aidoc_2026": WEB([], "Aidoc's chest X-ray reporting tool earns FDA Breakthrough Device designation", "Radiology Business",
                      "https://radiologybusiness.com/topics/healthcare-management/healthcare-policy/aidocs-chest-x-ray-reporting-tool-earns-fda-breakthrough-device-designation",
                      published="June 2026"),
    "deephealth_2026": WEB([], "DeepHealth gets FDA nod for AI tool that reads ultrasounds, creates reports", "Healthcare Dive",
                           "https://www.healthcaredive.com/news/deephealth-gets-fda-nod-for-ai-tool-that-reads-ultrasounds-creates-reports/827093/",
                           published="July 2026"),
    "bernstein_2025": J(["Bernstein MH", "Sheppard B", "Bruno MA", "Lay PS", "Baird GL"],
                        "Randomized study of the impact of AI on perceived legal liability for radiologists", "NEJM AI",
                        2025, 2, 6, None, "10.1056/AIoa2400785"),
    "mello_2024": J(["Mello MM", "Guha N"], "Understanding liability risk from using health care artificial intelligence tools",
                    "N Engl J Med", 2024, 390, 3, "271-278", "10.1056/NEJMhle2308901"),
    "cms_pfs_2026": J(["Centers for Medicare & Medicaid Services"],
                      "Medicare and Medicaid programs; CY 2026 payment policies under the physician fee schedule and other "
                      "changes to Part B payment and coverage policies; Medicare Shared Savings Program requirements; and "
                      "Medicare prescription drug inflation rebate program. Final rule", "Fed Regist", 2025, 90, 212,
                      "49266-50481", url="https://www.govinfo.gov/content/pkg/FR-2025-11-05/html/2025-19787.htm"),
    "pc_share": WEB([], "Radiology alignment: common structures and the value of radiologists' services", "Radiology Business",
                    "https://radiologybusiness.com/sponsored/1067/vmg/topics/healthcare-management/business-intelligence/radiology-alignment-common-structures-and-value-radiologists-services"),
    # ===================================================================== economics of automation & demand
    "acemoglu_restrepo_2018": J(["Acemoglu D", "Restrepo P"],
                                "The race between man and machine: implications of technology for growth, factor shares, "
                                "and employment", "Am Econ Rev", 2018, 108, 6, "1488-1542", "10.1257/aer.20160696"),
    "acemoglu_restrepo_2019": J(["Acemoglu D", "Restrepo P"],
                                "Automation and new tasks: how technology displaces and reinstates labor", "J Econ Perspect",
                                2019, 33, 2, "3-30", "10.1257/jep.33.2.3"),
    "acemoglu_2025": J(["Acemoglu D"], "The simple macroeconomics of AI", "Econ Policy", 2025, 40, 121, "13-58",
                       "10.1093/epolic/eiae042"),
    "autor_2024": J(["Autor D", "Chin C", "Salomons A", "Seegmiller B"], "New frontiers: the origins and content of new work, 1940-2018",
                    "Q J Econ", 2024, 139, 3, "1399-1465", "10.1093/qje/qjae008"),
    "autor_thompson_2025": J(["Autor D", "Thompson N"], "Expertise", "J Eur Econ Assoc", 2025, 23, 4, "1203-1271",
                             "10.1093/jeea/jvaf023"),
    "brynjolfsson_2025": J(["Brynjolfsson E", "Li D", "Raymond L"], "Generative AI at work", "Q J Econ", 2025, 140, 2, "889-942",
                           "10.1093/qje/qjae044"),
    "canaries_2025": WP(["Brynjolfsson E", "Chandar B", "Chen R"],
                        "Canaries in the coal mine? Six facts about the recent employment effects of artificial intelligence",
                        "Working paper", "Stanford Digital Economy Lab", 2025,
                        url="https://digitaleconomy.stanford.edu/app/uploads/2025/11/CanariesintheCoalMine_Nov25.pdf",
                        published="November 2025"),
    "humlum_2025": WP(["Humlum A", "Vestergaard E"], "Large language models, small labor market effects",
                      "NBER Working Paper 33777", "National Bureau of Economic Research", 2025, doi="10.3386/w33777"),
    "eloundou_2024": J(["Eloundou T", "Manning S", "Mishkin P", "Rock D"], "GPTs are GPTs: labor market impact potential of LLMs",
                       "Science", 2024, 384, 6702, "1306-1308", "10.1126/science.adj0998"),
    "bessen_2019": J(["Bessen J"], "Automation and jobs: when technology boosts employment", "Econ Policy", 2019, 34, 100,
                     "589-626", "10.1093/epolic/eiaa001"),
    "jevons_1865": BOOK(["Jevons WS"], "The Coal Question: An Inquiry Concerning the Progress of the Nation, and the Probable "
                        "Exhaustion of Our Coal-Mines", "Macmillan and Co", 1865,
                        "https://archive.org/details/coalquestionani00jevogoog"),
    "manning_1987": J(["Manning WG", "Newhouse JP", "Duan N", "Keeler EB", "Leibowitz A", "Marquis MS"],
                      "Health insurance and the demand for medical care: evidence from a randomized experiment",
                      "Am Econ Rev", 1987, 77, 3, "251-277", url="https://www.jstor.org/stable/1804094"),
    "aron_dine_2013": J(["Aron-Dine A", "Einav L", "Finkelstein A"], "The RAND Health Insurance Experiment, three decades later",
                        "J Econ Perspect", 2013, 27, 1, "197-222", "10.1257/jep.27.1.197"),
    "brot_goldberg_2017": J(["Brot-Goldberg ZC", "Chandra A", "Handel BR", "Kolstad JT"],
                            "What does a deductible do? The impact of cost-sharing on health care prices, quantities, and "
                            "spending dynamics", "Q J Econ", 2017, 132, 3, "1261-1318", "10.1093/qje/qjx013"),
    "nicholson_2002": J(["Nicholson S"], "Physician specialty choice under uncertainty", "J Labor Econ", 2002, 20, 4, "816-847",
                        "10.1086/342039"),
    # ===================================================================== forecasting & AI progress
    "tetlock_2015": BOOK(["Tetlock PE", "Gardner D"], "Superforecasting: The Art and Science of Prediction", "Crown", 2015,
                         "https://www.penguinrandomhouse.com/books/227815/superforecasting-by-philip-e-tetlock-and-dan-gardner/"),
    "mellers_2014": J(["Mellers B", "Ungar L", "Baron J", "Ramos J", "Gurcay B", "Fincher K", "Scott SE"],
                      "Psychological strategies for winning a geopolitical forecasting tournament", "Psychol Sci", 2014, 25, 5,
                      "1106-1115", "10.1177/0956797614524255"),
    "kahneman_1993": J(["Kahneman D", "Lovallo D"], "Timid choices and bold forecasts: a cognitive perspective on risk taking",
                       "Manage Sci", 1993, 39, 1, "17-31", "10.1287/mnsc.39.1.17"),
    "metaculus": WEB(["Metaculus"], "Track record", "Metaculus", "https://www.metaculus.com/questions/track-record/"),
    "karger_2023": WP(["Karger E", "Rosenberg J", "Jacobs Z", "Hickman M", "Hadshar R", "Gamin K", "Tetlock PE"],
                      "Forecasting existential risk: evidence from a long-run forecasting tournament",
                      "Forecasting Research Institute Working Paper 1", "Forecasting Research Institute", 2023,
                      url="https://forecastingresearch.org/xpt"),
    "grace_2025": J(["Grace K", "Sandkühler JF", "Stewart H", "Weinstein-Raun B", "Thomas S", "Stein-Perlman Z", "Salvatier J"],
                    "Thousands of AI authors on the future of AI", "J Artif Intell Res", 2025, 84, None, None,
                    "10.1613/jair.1.19087"),
    "leap_2025": WEB(["Forecasting Research Institute"], "Introducing LEAP: the Longitudinal Expert AI Panel",
                     "Forecasting Research Institute Substack", "https://forecastingresearch.substack.com/p/introducing-leap",
                     published="November 2025"),
    "ai2027": WEB(["Kokotajlo D", "Alexander S", "Larsen T", "Lifland E", "Dean R"], "AI 2027", "AI Futures Project",
                  "https://ai-2027.com", published="April 3, 2025"),
    "metr_2025": PRE(["Kwa T", "West B", "Becker J", "Deng A", "Garcia K", "Hasin M", "Jawhar S"],
                     "Measuring AI ability to complete long tasks", "arXiv", "March 18, 2025", "10.48550/arXiv.2503.14499"),
    "metr_2026": WEB(["METR"], "Time horizon 1.1 and the limitations of time-horizon measurements", "METR Notes",
                     "https://metr.org/notes/2026-01-22-time-horizon-limitations/", published="January 22, 2026"),
    # ===================================================================== backtest data & forecasting methods
    "frey_osborne_2013": WP(["Frey CB", "Osborne MA"], "The future of employment: how susceptible are jobs to computerisation?",
                            "Working paper", "Oxford Martin School, University of Oxford", 2013,
                            url="https://www.oxfordmartin.ox.ac.uk/downloads/academic/The_Future_of_Employment.pdf",
                            published="September 17, 2013"),
    "bls_ooh_2010_sw": WEB(["US Bureau of Labor Statistics"], "Computer software engineers and computer programmers",
                           "Occupational Outlook Handbook, 2010-11 Edition (archived)",
                           "http://web.archive.org/web/2008/http://www.bls.gov/oco/ocos303.htm"),
    "bls_ooh_2008_tr": WEB(["US Bureau of Labor Statistics"], "Interpreters and translators",
                           "Occupational Outlook Handbook, 2008-09 Edition (archived May 13, 2008)",
                           "http://web.archive.org/web/20080513155327/http://www.bls.gov/oco/ocos175.htm"),
    "bls_ooh_2008_mt": WEB(["US Bureau of Labor Statistics"], "Medical transcriptionists",
                           "Occupational Outlook Handbook, 2008-09 Edition (archived May 11, 2008)",
                           "http://web.archive.org/web/20080511153519/http://www.bls.gov/oco/ocos271.htm"),
    "bls_ooh_2018_sw": WEB(["US Bureau of Labor Statistics"], "Software developers (2016-26 projections)",
                           "Occupational Outlook Handbook, 2018-19 Edition (archived June 2018)",
                           "http://web.archive.org/web/20180615000000/https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm"),
    "bls_ooh_2018_tr": WEB(["US Bureau of Labor Statistics"], "Interpreters and translators (2016-26 projections)",
                           "Occupational Outlook Handbook, 2018-19 Edition (archived June 2018)",
                           "http://web.archive.org/web/20180615000000/https://www.bls.gov/ooh/media-and-communication/interpreters-and-translators.htm"),
    "bls_ooh_2018_mt": WEB(["US Bureau of Labor Statistics"], "Medical transcriptionists (2016-26 projections)",
                           "Occupational Outlook Handbook, 2018-19 Edition (archived June 2018)",
                           "http://web.archive.org/web/20180615000000/https://www.bls.gov/ooh/healthcare/medical-transcriptionists.htm"),
    "bls_ooh_2026_sw": WEB(["US Bureau of Labor Statistics"], "Software developers, quality assurance analysts, and testers",
                           "Occupational Outlook Handbook", "https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm"),
    "bls_ooh_2026_tr": WEB(["US Bureau of Labor Statistics"], "Interpreters and translators", "Occupational Outlook Handbook",
                           "https://www.bls.gov/ooh/media-and-communication/interpreters-and-translators.htm"),
    "bls_ooh_2026_mt": WEB(["US Bureau of Labor Statistics"], "Medical transcriptionists", "Occupational Outlook Handbook",
                           "https://www.bls.gov/ooh/healthcare/medical-transcriptionists.htm"),
    "tetlock_2005": dict(type="book", authors=["Tetlock PE"], title="Expert Political Judgment: How Good Is It? How Can We Know?",
                         publisher="Princeton University Press", year=2005, doi="10.1515/9781400830312"),
    "makridakis_2020": J(["Makridakis S", "Spiliotis E", "Assimakopoulos V"],
                         "The M4 Competition: 100,000 time series and 61 forecasting methods", "Int J Forecast", 2020, 36, 1,
                         "54-74", "10.1016/j.ijforecast.2019.04.014"),
    "clemen_1989": J(["Clemen RT"], "Combining forecasts: a review and annotated bibliography", "Int J Forecast", 1989, 5, 4,
                     "559-583", "10.1016/0169-2070(89)90012-5"),
    "arrow_2008": J(["Arrow KJ", "Forsythe R", "Gorham M", "Hahn R", "Hanson R", "Ledyard JO", "Levmore S"],
                    "The promise of prediction markets", "Science", 2008, 320, 5878, "877-878", "10.1126/science.1157679"),
    "fri_xpt_2025": WEB(["Forecasting Research Institute"],
                        "What did forecasters get right and wrong in the largest existential risk forecasting tournament?",
                        "Forecasting Research Institute Substack",
                        "https://forecastingresearch.substack.com/p/what-did-forecasters-get-right-and", published="2025"),
}


# ---------------------------------------------------------------------------------------------------- formatting
def _authors(a: list, group: str | None = None) -> str:
    if not a:
        return ""
    s = ", ".join(a) if len(a) <= 6 else ", ".join(a[:3]) + ", et al"
    if group:
        s += "; " + group
    return s + "."


def _sent(t: str) -> str:
    t = t.strip()
    return t if t.endswith(("?", "!", ".")) else t + "."


def format_ama(key: str, fmt: str = "html") -> str:
    """Return the AMA 11th-ed. reference string. fmt='html' (italics + <a> links) or 'md' (markdown)."""
    r = REFERENCES[key]
    esc = (lambda s: html.escape(str(s), quote=False)) if fmt == "html" else (lambda s: str(s))
    it = (lambda s: f"<i>{esc(s)}</i>") if fmt == "html" else (lambda s: f"*{s}*")

    def link(url, text=None):
        text = text or url
        return f'<a href="{html.escape(url)}" rel="noopener">{esc(text)}</a>' if fmt == "html" else f"[{text}]({url})"

    def doi(d):
        return "doi:" + (link("https://doi.org/" + d, d) if fmt == "html" else f"[{d}](https://doi.org/{d})")

    acc = f"Accessed {ACCESSED}."
    parts: list[str] = []
    au = _authors(r.get("authors", []), r.get("group"))
    t = r["type"]
    if t == "journal":
        if au:
            parts.append(esc(au))
        parts.append(esc(_sent(r["title"])))
        loc = f"{r['year']}"
        if r.get("vol") is not None:
            loc += f";{r['vol']}"
            if r.get("issue") is not None:
                loc += f"({r['issue']})"
        if r.get("pages"):
            loc += f":{r['pages']}"
        parts.append(f"{it(r['journal'])}. {esc(loc)}.")
        if r.get("doi"):
            parts.append(doi(r["doi"]))
        elif r.get("url"):
            parts.append(f"{acc} {link(r['url'])}")
    elif t == "preprint":
        parts += [esc(au), esc(_sent(r["title"])), f"{it(r['server'])}.", f"Preprint posted online {esc(r['posted'])}."]
        parts.append(doi(r["doi"]) if r.get("doi") else f"{acc} {link(r['url'])}")
    elif t == "workingpaper":
        parts += [esc(au), esc(_sent(r["title"])), esc(f"{r['series']}. {r['publisher']}; {r.get('published') or r['year']}.")]
        parts.append(doi(r["doi"]) if r.get("doi") else f"{acc} {link(r['url'])}")
    elif t == "web":
        if au:
            parts.append(esc(au))
        parts.append(esc(_sent(r["title"])))
        parts.append(f"{it(r['site'])}.")
        if r.get("published"):
            parts.append(esc(f"Published {r['published']}."))
        if r.get("updated"):
            parts.append(esc(f"Updated {r['updated']}."))
        parts.append(f"{acc} {link(r['url'])}")
    elif t == "report":
        parts.append(esc(au))
        parts.append(f"{it(r['title'])}.")
        if r.get("number"):
            parts.append(esc(f"{r['number']}."))
        parts.append(esc(f"{r['publisher']}; {r.get('published') or r['year']}."))
        parts.append(f"{acc} {link(r['url'])}")
    elif t == "book":
        parts += [esc(au), f"{it(r['title'])}.", esc(f"{r['publisher']}; {r['year']}.")]
        if r.get("doi"):
            parts.append(doi(r["doi"]))
        elif r.get("url"):
            parts.append(f"{acc} {link(r['url'])}")
    elif t == "video":
        parts += [esc(au), esc(_sent(r["title"])), esc(f"Presented at: {r['event']}."), f"{it(r['site'])}.",
                  esc(f"Published {r['published']}."), f"{acc} {link(r['url'])}"]
    return " ".join(p for p in parts if p)


def href(key: str) -> str:
    r = REFERENCES[key]
    return "https://doi.org/" + r["doi"] if r.get("doi") else r.get("url", "")


def ama(key: str) -> str:  # backward compatible
    return format_ama(key, "html")


# ---------------------------------------------------------------------------------------------------- usage notes
# One-line paraphrase of what each source supports in this project (shown in citation pop-overs).
USES = {
    "christensen_util": "Imaging use projected to rise 16.9%–26.9% (2023–2055) from population growth and aging alone; anchors the demographic demand term.",
    "christensen_supply": "37,482 Medicare-enrolled radiologists in 2023; +25.7% by 2055 with flat residency positions. The supply model is calibrated to reproduce this.",
    "parikh_2026": "Practice turnover among U.S. radiologists rose from 5.3% to 8.5% (2013–2022), linked to workload.",
    "zamani_2026": "Average exams read per radiologist-day were flat 2018–2024 (+0.6%), but the busiest quartile read 30.6% more.",
    "rula_2026": "HRSA projections summarized by the Neiman Institute put radiology at ≈90% workforce adequacy in 2038; attrition trends.",
    "rcr_2026": "UK census: 32% consultant radiologist shortfall; 75% of departments use AI clinically without an overall workload reduction.",
    "smith_bindman_2019": "Per-capita CT use grew 3.7%–5.2%/yr and MRI 1.3%–2.2%/yr in U.S. health systems before 2016; anchors utilization growth.",
    "smith_bindman_2025": "About 93 million CT exams were performed in the U.S. in 2023.",
    "rosenkrantz_2025": "Emergency-department CT per 100 Medicare beneficiaries nearly doubled 2013–2023 while ED visits fell.",
    "mcdonald_2015": "Images per CT/MR study rose about tenfold 1999–2010; a radiologist must read an image every 3–4 seconds. Anchors work-per-exam growth.",
    "dhanoa_2013": "Time-motion study: 36.4% of radiologist time on image interpretation; anchors the task shares.",
    "rosenkrantz_2016": "Radiologists rose 39.2% from 1995 (27,906) to 2011 (38,875); trainee numbers bottomed at 3,080 in 1997 and rose 84% by 2011: the pipeline reacts to the job market.",
    "sharafinski_2016": "The radiology job market was oversupplied in the mid-2010s as positions kept expanding; domestic interest fell.",
    "shi_2015": "2015 Match: 86% of advanced DR positions filled; 55 of 166 programs unfilled; U.S. graduates took 67% of positions.",
    "nrmp_2026": "2026 Match: a record 1,241 DR positions, 97.6% filled; PGY-1 applicants down 14% over three years.",
    "aamc_2024": "AAMC counts about 28,600 active radiology and diagnostic radiology physicians (narrower definition than CMS).",
    "doximity_2026": "Doximity 2026: radiology pay rose 6.6% in 2025 to $609,684, against 2% for all physicians: a sign of a tight market.",
    "forman_2000": "Radiology job ads fell to one-eighth of their late-1991 peak, then recovered; ads tracked radiologists' income relative to all physicians (R = 0.98).",
    "covey_2000": "3,926 diagnostic-radiology positions were advertised in 1999, 75% more than in 1998: the turn to shortage.",
    "sunshine_2004": "Advertised jobs fell 28% from 2002 to 2003 and listings per job seeker fell from 3.8 (2000) to 1.4 (2002): the shortage eased.",
    "meghea_2005": "In 2003 the net workload change radiologists wanted was about 0.1%: overall balance between supply and demand.",
    "sunshine_2007": "Job listings per job seeker: 0.25 to 3.8 in 1993-2002, about 1.1-1.2 in 2003-2006 and 0.72 in 2007.",
    "bhargavan_2009": "RVUs per FTE radiologist rose 70% from 1991-92 to 2006-07 (10% after 2002-03); procedures per FTE rose 34%.",
    "levin_2011": "Medicare imaging by radiologists grew 3.4%/yr in 1998-2005 and 0.8%/yr in 2005-2008; non-radiologists' imaging grew about twice as fast.",
    "levin_2017": "Medicare imaging use and professional RVU rates per 1,000 beneficiaries rose until 2008-09 and then fell through 2014.",
    "hong_2020": "Imaging use per 1,000 enrollees peaked in 2008-09 and declined, stabilizing near 2003 levels by 2016, in Medicare and commercial plans alike.",
    "bluth_2012": "About 1,241 radiologists hired in 2011: roughly one job for each of the ~1,200 residents finishing training.",
    "bluth_2014": "1,069 radiologists hired in 2013; a flat market with jobs close to the number of graduates.",
    "bluth_2015": "Job opportunities for radiologists rising compared with 2013.",
    "bluth_2016": "2016 hiring projected 16% above 2015; job opportunities rising since 2013.",
    "bender_2019": "1,434-1,861 radiologists hired in 2017 and similar numbers planned for 2018: a positive outlook for job seekers.",
    "pfeifer_2017": "Severe deficits in jobs for new radiology graduates from 2012 through 2015, while training programs kept growing.",
    "dibble_2025": "In the 2022 ACR/RBMA workforce survey, 67% of radiologists said their practices were understaffed.",
    "census_pop": "U.S. population growth by decade (about 1.2%/yr in the 1990s, 0.9% in the 2000s, 0.7% in the 2010s).",
    "mgma_2007": "MGMA: radiologist median pay rose 4.7% in 2006 and about 5%/yr over five years; specialists' rose 1.7% in 2006.",
    "mgma_2009": "MGMA: radiologist median pay rose 17% from 2004 to 2008 (2.7% after inflation); 2008: radiology +2.6%, specialists +2.2%.",
    "mgma_2011": "MGMA: radiologist median pay fell 1.6% in 2010 and rose 5.5% in total over 2006-2010, while other specialties rose 4%-6% in 2010.",
    "amga_2015": "AMGA: non-interventional radiologist pay rose 1.6% in 2014 against 5.9% for medical specialties.",
    "doximity_2023": "Doximity: radiology pay $503,564 in 2022 (+1.6%) while average physician pay fell 2.4%.",
    "doximity_2024": "Doximity: radiology pay $531,983 in 2023.",
    "doximity_2025": "Doximity: radiology pay rose 7.5% in 2024 to $571,749, against 3.7% overall.",
    "asrt_2025": "CT technologist vacancy rate 19.4% and MRI 17.4% in 2025: scanner capacity limits induced demand.",
    "cbo_2026": "U.S. population grows from 349 million (2026) to 364 million (2056); slower than Census 2023 assumptions.",
    "trustees_2026": "Medicare's Hospital Insurance trust fund is projected to be depleted in 2033: pressure toward utilization management.",
    "bandi_2024": "Only 18.1% of eligible adults were up to date with lung-cancer screening in 2022: room for screening growth.",
    "lee_2026": "Review of opportunistic screening using already-acquired images, a source of new radiologist work.",
    "baker_2010": "Owning MRI equipment raised orthopedists' MRI ordering ~38%: supply-induced imaging demand.",
    "kwee_2025": "Of 2024 imaging research with patient-care impact, 49% would increase workload and <1% decrease it; AI studies far more likely to add work.",
    "reeder_2022": "U.S. survey: AI concerns lowered students' ranking of radiology (first-choice share 21.4% → 17.7%).",
    "larson_2011": "ED visits with CT rose from 2.8% to 13.9% (1995–2007): faster availability raises ordering.",
    "langlotz_2025": "Task-based model: foreseeable AI applications could cut radiologist hours 33% (14%–49%) within 5 years if fully adopted (described as an upper bound).",
    "langlotz_2019": "Framing that AI will change radiologists' work rather than replace radiologists.",
    "huang_2025": "Live deployment over ~24,000 radiographs: generative draft reports gave a 15.5% documentation-efficiency gain without loss of accuracy.",
    "hong_2025": "Reader study: AI-generated draft reports cut chest-radiograph reading time from 34.2 s to 19.8 s.",
    "liu_2026": "185,044 chest CT reports at two hospitals: no sustained drafting-efficiency gain at one site; effects heterogeneous.",
    "li_2026": "Multicentre LLM impression generation: non-inferior in 69% of comparisons; saved ~0.46 min per report.",
    "tanno_2025": "AI chest-radiograph reports preferred or equivalent in 77.7% of cases; clinically significant errors still common in AI-only reports.",
    "lang_2023": "MASAI interim: AI-supported screening cut screen-reading workload by 44% without unsafe performance.",
    "hernstrom_2025": "MASAI: cancer detection 6.4 vs 5.0 per 1000 (29% higher) with AI-supported screening.",
    "gommers_2026": "MASAI final: interval-cancer rate non-inferior with AI (rate ratio 0.88); higher sensitivity; published ~5 years after randomisation began.",
    "lauritzen_2024": "Danish program after AI triage: 33.5% fewer screening reads, higher detection, lower recall.",
    "eisemann_2025": "German nationwide program: AI-supported double reading detected 17.6% more cancers with no rise in recalls.",
    "plesner_2023": "AI could autonomously report 7.8% of all chest radiographs (28% of normals) with >99% sensitivity: anchors tier-1 autonomy.",
    "plesner_2024": "With a tuned threshold, AI excluded pathology in ~47% of unremarkable chest radiographs at 99% sensitivity.",
    "wenderott_2024": "Meta-analysis of real-world AI deployments: most studies reported time savings but pooled effects were not significant.",
    "yu_2024": "140 radiologists: AI assistance helped some and hurt others; erroneous AI output degraded performance.",
    "agarwal_2023": "Radiologists under-weight AI predictions; AI-assisted humans often do not beat AI or humans alone.",
    "rajpurkar_2023": "Review of what current AI can and cannot do in medical image interpretation (recommended overview).",
    "malhotra_2026": "DR residency positions rose 33% from 2010 to 2025 (about 1.9%/yr); practicing radiologists rose 12% from 2010 to 2022; radiologists per 100,000 rose only from 11.1 to 11.5.",
    "ghuwalewala_2022": "Proposes levels of autonomy for radiology AI, from assistance to fully autonomous reads (by how much AI does, not which exams).",
    "wu_2024": "Insurance claims show clinical AI use concentrated in a few products despite hundreds of cleared devices.",
    "allen_2021": "2020 ACR survey: about a third of U.S. radiologists used any AI in practice.",
    "liu_burnout_2024": "In China, regular AI use was associated with higher burnout odds among radiologists.",
    "johnson_2023": "Deep-learning reconstruction cut knee MRI scan time ~44% prospectively: scanner throughput gains.",
    "lehman_2015": "Mammography CAD spread to most U.S. screening exams after Medicare payment (2002) despite no accuracy gain: diffusion follows payment.",
    "adler_milstein_2017": "Hospital EHR adoption accelerated sharply after HITECH subsidies: an adoption-speed precedent.",
    "mousa_2025": "Accessible essay on why AI has not replaced radiologists (recommended overview).",
    "hinton_2016": "Hinton's 2016 claim that training radiologists should stop because deep learning would soon outperform them.",
    "fda_ai_2026": "FDA's list of AI-enabled devices (>1,600 by 2026, ~3/4 radiology); no autonomous radiology read authorized.",
    "fda_draft_2025": "FDA's AI device lifecycle guidance remains a draft: regulatory pathway still evolving.",
    "chouffani_2024": "43% of FDA-authorized AI devices had no published clinical validation; only ~4% had randomized trials.",
    "abramoff_2018": "Pivotal trial behind the first FDA-authorized autonomous AI diagnostic (diabetic retinopathy): the main autonomy precedent.",
    "oxipit_2022": "First regulatory approval (EU CE Class IIb) of autonomous AI reporting for normal chest radiographs.",
    "aidoc_2026": "Generative chest-radiograph report drafting received FDA Breakthrough designation in 2026 (not yet cleared).",
    "deephealth_2026": "FDA-cleared breast-ultrasound AI that generates draft reports under radiologist control (2026).",
    "bernstein_2025": "Mock jurors judged radiologists more harshly when they missed findings AI had flagged: liability shapes adoption.",
    "mello_2024": "Analysis of how liability for AI-assisted care is likely to be allocated; unsettled law slows autonomy.",
    "cms_pfs_2026": "Medicare's 2026 fee schedule created payment for AI coronary-plaque analysis (CPT 75577): payment for AI is possible.",
    "pc_share": "The radiologist's professional fee is roughly 20%–25% of Medicare global imaging payments, less where facility fees apply.",
    "acemoglu_restrepo_2018": "Task framework: automation displaces labor from tasks; new tasks reinstate it.",
    "acemoglu_restrepo_2019": "Displacement, productivity and reinstatement effects of automation on labor demand.",
    "acemoglu_2025": "Macro estimate: AI's decade-scale productivity effect is modest under current evidence.",
    "autor_2024": "Most of today's employment is in job types created after 1940: new work emerges alongside automation.",
    "autor_thompson_2025": "Whether automation raises or lowers wages depends on whether it removes expert or inexpert tasks.",
    "brynjolfsson_2025": "Generative AI raised productivity of customer-support agents ~14%, most for less experienced workers.",
    "canaries_2025": "Early-career workers in AI-exposed occupations saw ~16% relative employment declines; experienced workers did not.",
    "humlum_2025": "Danish data: chatbots had near-zero effects on earnings and hours; AI created new oversight tasks.",
    "eloundou_2024": "Large shares of U.S. occupations have tasks exposed to large language models.",
    "bessen_2019": "Automation raised employment while demand was elastic, then reduced it as demand saturated.",
    "jevons_1865": "Origin of the 'Jevons paradox': efficiency gains can increase total resource use.",
    "manning_1987": "RAND experiment: medical care demand is price-inelastic (≈ −0.2).",
    "aron_dine_2013": "Reassessment of RAND HIE elasticity estimates (≈ −0.2 widely used).",
    "brot_goldberg_2017": "High-deductible switch cut spending ~12%, including imaging: patients do respond to price, modestly.",
    "nicholson_2002": "Medical students' specialty choices respond to expected income.",
    "tetlock_2015": "Superforecasting principles: base rates, decomposition, explicit probabilities, frequent updating.",
    "tetlock_2005": "20-year study: experts barely beat chance and did no better than informed generalists; 'foxes' beat 'hedgehogs'.",
    "mellers_2014": "Training, teaming and tracking improved accuracy in a large geopolitical forecasting tournament.",
    "kahneman_1993": "The 'outside view': forecasts should start from reference-class base rates.",
    "metaculus": "Track record of a public forecasting platform (calibration of aggregated forecasts).",
    "karger_2023": "Long-run tournament: domain experts and superforecasters disagreed most about AI.",
    "fri_xpt_2025": "Superforecasters and domain experts had nearly identical overall accuracy; both underestimated AI benchmark progress (9.7% vs 24.6% average probability on observed outcomes); median aggregation beat individuals.",
    "grace_2025": "Survey of 2,778 AI researchers: 50% odds of human-level task performance by 2047; full automation of jobs much later.",
    "leap_2025": "Expert panel forecasts of AI's impact are far below AI-lab leaders' predictions.",
    "ai2027": "Scenario of very rapid AI progress; used only to inform the fast/transformative regimes.",
    "metr_2025": "Length of tasks frontier AI can complete doubled ~every 7 months (2019–2024).",
    "metr_2026": "Updated time-horizon measurements and their limitations (faster growth after 2023).",
    "makridakis_2020": "M4 competition: combinations of methods beat single methods; simple benchmarks are hard to beat.",
    "clemen_1989": "Combining forecasts generally improves accuracy: the basis for blending trend and official projections.",
    "arrow_2008": "Prediction markets aggregate dispersed information into accurate probabilities.",
    "frey_osborne_2013": "Automation probabilities by occupation (e.g., transcriptionists 0.89, translators 0.38, software developers 0.04–0.13).",
    "bls_ooh_2010_sw": "Employment of software engineers in 2008 (start of the prior-decade trend).",
    "bls_ooh_2008_tr": "Interpreters and translators: 41,000 jobs in 2006; BLS projected +24% for 2006–16.",
    "bls_ooh_2008_mt": "Medical transcriptionists: 98,000 jobs in 2006; BLS projected +14% for 2006–16 (actual: −41%).",
    "bls_ooh_2018_sw": "Software developers: 1,256,200 jobs in 2016; projected +24% for 2016–26.",
    "bls_ooh_2018_tr": "Interpreters and translators: 68,200 jobs in 2016; projected +18% for 2016–26.",
    "bls_ooh_2018_mt": "Medical transcriptionists: 57,400 jobs in 2016; projected −3% for 2016–26.",
    "bls_ooh_2026_sw": "Software developers: 1,717,800 jobs in 2025.",
    "bls_ooh_2026_tr": "Interpreters and translators: 73,900 jobs in 2025.",
    "bls_ooh_2026_mt": "Medical transcriptionists: 42,000 jobs in 2025.",
}
