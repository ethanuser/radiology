"""Build deep links that open each source at the passage we rely on (run once; output is committed).

For journal articles indexed in PubMed, we fetch the abstract, find the sentence containing the number or
phrase the model uses (the "needle"), and build a URL with a text fragment
(https://pubmed.ncbi.nlm.nih.gov/<PMID>/#:~:text=<start>,<end>). Browsers that support text fragments
(Chrome, Edge, Safari, Firefox 131+) scroll to and highlight that sentence; others simply open the page.
Only a few words of each sentence are stored (as the fragment anchor), not the sentence itself.

    python tools/make_passages.py
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.references import REFERENCES  # noqa: E402

NEEDLES = {
    "christensen_supply": "25.7%", "christensen_util": "16.9% to 26.9%", "smith_bindman_2019": "3.7%",
    "mcdonald_2015": "3-4 seconds", "dhanoa_2013": "36.4%", "huang_2025": "15.5%", "hong_2025": "34.2",
    "hernstrom_2025": "per 1000", "gommers_2026": "0·88", "eisemann_2025": "17.6%", "lauritzen_2024": "33.5%",
    "plesner_2023": "7.8%", "plesner_2024": "47.1%", "wenderott_2024": "67%", "tanno_2025": "77.7%",
    "li_2026": "69.0%", "kwee_2025": "48.9", "zamani_2026": "+0.6%", "parikh_2026": "8.5%", "bandi_2024": "18.1%",
    "baker_2010": "38 percent", "larson_2011": "13.9%", "lehman_2015": "1998", "sharafinski_2016": "oversupplied",
    "rosenkrantz_2016": "3080", "allen_2021": "33.5", "yu_2024": "heterogeneous", "reeder_2022": "radiology",
    "liu_2026": "1 of the 2", "liu_burnout_2024": "burnout", "smith_bindman_2025": "93 million",
    "lang_2023": "44·", "abramoff_2018": "autonomous", "adler_milstein_2017": "adoption",
    "forman_2000": "one eighth", "covey_2000": "75%", "meghea_2005": "0.1%", "sunshine_2007": "0.72",
    "bhargavan_2009": "70.3%", "levin_2011": "3.4%", "levin_2017": "2008 and 2009", "hong_2020": "declining trends",
    "bluth_2012": "1,241", "bluth_2014": "1,069", "bluth_2015": "1,131", "bluth_2016": "16.2%", "bender_2019": "1,434",
    "pfeifer_2017": "2012 through 2015",
}
MANUAL = {  # sources outside PubMed: page + a short anchor phrase verified on the page
    "langlotz_2025": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12755265/#:~:text=The%20model%20projects%20a%2033%25,of%2014%25%20to%2049%25",
}


def curl(url):
    return subprocess.run(["curl", "-s", "-A", "radiology-forecast/1.1", url], capture_output=True, text=True).stdout


def enc(s):
    return urllib.parse.quote(s, safe="").replace("-", "%2D")


def main():
    out = dict(MANUAL)
    for key, needle in NEEDLES.items():
        r = REFERENCES.get(key, {})
        if not r.get("doi"):
            continue
        ids = re.findall(r"<Id>(\d+)</Id>", curl(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=" + urllib.parse.quote(r["doi"] + "[doi]")))
        time.sleep(0.4)
        if not ids:
            print("no pmid", key)
            continue
        pmid = ids[0]
        xml = curl(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&rettype=abstract&retmode=xml")
        time.sleep(0.4)
        parts = re.findall(r"<AbstractText[^>]*>(.*?)</AbstractText>", xml, flags=re.S)
        text = " ".join(re.sub(r"<[^>]+>", "", p) for p in parts)
        text = html.unescape(re.sub(r"\s+", " ", text))
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z(])", text)
        hit = next((s for s in sentences if needle in s), None)
        url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        if hit:
            words = hit.rstrip(".").split()
            frag = enc(" ".join(words[:5])) if len(words) <= 9 else enc(" ".join(words[:5])) + "," + enc(" ".join(words[-4:]))
            url += "#:~:text=" + frag
        else:
            print("needle not found", key, needle)
        out[key] = url
    (ROOT / "model" / "passages.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"{len(out)} passage links written")


if __name__ == "__main__":
    main()
