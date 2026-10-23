"""The bound Congressional Record's granules, page by page: pages-YYYY.tsv for each year asked.
# Usage: python3 -I tools/congress/make_record_pages.py OUT_DIR YEAR [YEAR ...]
#   Reads each part's MODS on govinfo (https://www.govinfo.gov/metadata/pkg/GPO-CRECB-<year>-pt<n>/mods.xml), part 1
#   upward until a part answers nothing, and writes OUT_DIR/pages-<year>.tsv, one line a granule: first page, last
#   page, date, chamber (Senate, House, Extensions, Digest, Index, or the day's whole issue: Issue), granule id. The
#   file tools/executive/make_source_links.py reads (its CRECB_DIR), and the table the bills' Record pages are turned
#   to their days by (congress/bills.yaml, tools/bib/bills.py): a page of the History of Bills is looked up in the
#   year's file, the chamber's granule that holds it giving the day. Needs the network; the build does not.
"""
import os
import re
import sys
import time
import urllib.error
import urllib.request

MODS = "https://www.govinfo.gov/metadata/pkg/GPO-CRECB-{y}-pt{n}/mods.xml"


def fetch(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                if not r.geturl().endswith("/mods.xml"):   # a part that does not exist redirects to govinfo's error page
                    return None
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (404, 400):
                return None
            time.sleep(3 * (i + 1))
        except Exception:
            time.sleep(3 * (i + 1))
    return None


def granules(xml):
    for m in re.finditer(r'<relatedItem type="constituent" ID="id-([^"]+)".*?</relatedItem>\s*(?=<relatedItem type="constituent"|</mods>)',
                         xml, re.S):
        g, body = m.group(1), m.group(0)
        t = re.search(r"<title>([^<]*)</title>", body)
        p = re.search(r'<printPageRange first="([^"]*)" last="([^"]*)"', body)
        title = t.group(1).strip() if t else ""
        ch, _, day = title.rpartition(": ")
        ch = {"Senate": "Senate", "House of Representatives": "House", "Extensions of Remarks": "Extensions",
              "Daily Digest": "Digest"}.get(ch, ch or "Issue")
        yield (p.group(1) if p else "", p.group(2) if p else "", day or title, ch, g)


def main():
    out, years = sys.argv[1], sys.argv[2:]
    os.makedirs(out, exist_ok=True)
    for y in years:
        rows, n = [], 1
        while True:
            xml = fetch(MODS.format(y=y, n=n))
            if not xml or "<mods" not in xml:
                break
            rows.extend(granules(xml))
            n += 1
        with open(os.path.join(out, f"pages-{y}.tsv"), "w", encoding="utf-8") as f:
            for r in rows:
                f.write("\t".join(r) + "\n")
        print(y, "parts", n - 1, "granules", len(rows))


if __name__ == "__main__":
    main()
