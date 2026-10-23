"""Write daybook/diary.yaml: the days of the President's Daily Diary (Johnson's, Nov. 22, 1963-Jan. 20, 1969) that
the National Archives Catalog gives free, each with its page images: the address, the page count, the catalogue's
title. Nothing of the Diary's text is taken.

    python3 tools/daybook/make_daily_diary.py          (needs the network; the build does not)
    NARA_API_KEY=... python3 tools/daybook/make_daily_diary.py   (the Catalog's API v2, where a key is held)

The Diary is the LBJ Library's collection "President's Daily Diary" (NARA naId 1152, LBJ-PJDD); its series of the
Diary itself is naId 192429. The Catalog holds the Diary's pages for 51 days only (Nov. 22-30, 1963; Tonkin Gulf,
Selma, the signings, the trips; read Oct. 23, 2026), each an item ("President's Daily Diary Entry, August 4, 1964"),
its pages GIF images in order (`objectDesignator` 1, 2, ...). The series "Appointment Files [Diary Backup]" (naId
1756089; 1,893 file units, a day or a trip each) is the backup, not the Diary, and almost none of it is scanned: it is
not taken. The whole Diary, a page a day, is at the Library's own site (discoverlbj.org, item "pdd-YYYYMMDD", as
Wikipedia's citations give it); that site refused this environment (Cloudflare, 403) on Oct. 23, 2026, and its
robots.txt (Cloudflare's managed file) bars the AI crawlers by name, ClaudeBot, anthropic-ai and Claude-Web among them, and leaves other agents to its general rule (allowed: search=yes, ai-train=no, use=reference): it is not read, and nothing here reaches for it.

Read from the Catalog's search by parent (`ancestorNaId=192429`): the Catalog's API v2
(https://catalog.archives.gov/api/v2, header x-api-key) where NARA_API_KEY is set, else the public endpoint the
Catalog's own pages call (/proxy/records/search), which answers the same JSON. The key is never written anywhere.

STYLE (for whoever renders it; the Diary's line in the day layout is not wired in):
 1. One row a day: key 'pdd:YYYYMMDD', date, title (the Catalog's, its doubled "Entry Entry" mended), pages (the
    count of page images), naid, url (https://catalog.archives.gov/id/<naId>), nlj (the Library's control number,
    NLJ-PJDD-A-YYYYMMDD). A day the Catalog holds twice (Aug. 4, 1964: the Diary entry and an exhibit's copy of it)
    keeps the series' own item; the other goes.
 2. A calendar note cites the day as "[President's Daily Diary, Aug. 4, 1964](https://catalog.archives.gov/id/192446),
    images 3, 5 (LBJ Library; National Archives Catalog)": after the document of the act (the statute, the Public
    Papers item, the FRUS document), before the bibliography; an image is the page's number in the Catalog's item,
    not the Diary's own page number. tools/bib/diary.py checks the rows and the calendar's links (its STYLE).
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "daybook", "diary.yaml")
SERIES = 192429                      # President's Daily Diary (the Diary itself)
FROM, TO = "1963-11-22", "1969-01-20"
API = "https://catalog.archives.gov/api/v2/records/search"
PUBLIC = "https://catalog.archives.gov/proxy/records/search"
UA = "bib-daybook (https://impending2223.github.io/bib/)"
MONTHS = {m: i for i, m in enumerate(("January February March April May June July August September October November "
                                      "December").split(), 1)}


def fetch(page):
    key = os.environ.get("NARA_API_KEY")
    q = {"ancestorNaId": SERIES, "limit": 100, "page": page}
    headers = {"User-Agent": UA, "Accept": "application/json"}
    if key:
        headers["x-api-key"] = key
    url = (API if key else PUBLIC) + "?" + urllib.parse.urlencode(q)
    for attempt in range(5):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120))
        except Exception as ex:
            print(f"retry {attempt + 1}: {ex}", file=sys.stderr)
            time.sleep(2 ** (attempt + 1))
    raise SystemExit("the National Archives Catalog did not answer")


def day_of(title):
    m = re.search(r"([A-Z][a-z]+) (\d{1,2}), (\d{4})", title or "")
    if not m or m.group(1) not in MONTHS:
        return None
    return f"{m.group(3)}-{MONTHS[m.group(1)]:02d}-{int(m.group(2)):02d}"


def row(r):
    date = day_of(r.get("title"))
    if not date or not (FROM <= date <= TO):
        return None
    pages = [o for o in r.get("digitalObjects") or [] if (o.get("objectType") or "").startswith("Image")]
    if not pages:
        return None
    nlj = next((v["number"] for v in r.get("variantControlNumbers") or [] if v.get("number", "").startswith("NLJ")),
               None)
    out = {"key": "pdd:" + date.replace("-", ""), "date": date,
           "title": re.sub(r"\bEntry Entry\b", "Entry", r["title"]).strip(),
           "pages": len(pages), "naid": int(r["naId"]), "url": f"https://catalog.archives.gov/id/{r['naId']}"}
    if nlj:
        out["nlj"] = nlj
    return out


def main():
    rows, page, total = [], 1, None
    while True:
        hits = fetch(page)["body"]["hits"]
        total = hits["total"]["value"] if total is None else total
        for h in hits["hits"]:
            r = h["_source"]["record"]
            parent = [a["naId"] for a in r.get("ancestors") or [] if a.get("distance") == 1]
            if parent == [SERIES]:            # the series' own items (STYLE 1)
                x = row(r)
                if x:
                    rows.append(x)
        if page * 100 >= total:
            break
        page += 1
        time.sleep(1)
    by = {}
    for x in sorted(rows, key=lambda x: (x["date"], x["naid"])):
        by.setdefault(x["date"], x)           # a day held twice keeps its first (lower) item: the series' own
    out = [by[d] for d in sorted(by)]
    head = ("# Generated by tools/daybook/make_daily_diary.py from the National Archives Catalog (the LBJ Library's\n"
            "# President's Daily Diary, NARA naId 192429). Edit the script, not this file. One row a day: key, date,\n"
            "# title, pages, naid, url, nlj. The days the Catalog holds only; nothing of the Diary's text.\n")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(head)
        yaml.safe_dump({"days": out}, f, allow_unicode=True, sort_keys=False, width=1000)
    print(f"{total} records read, {len(out)} days", file=sys.stderr)


if __name__ == "__main__":
    main()
