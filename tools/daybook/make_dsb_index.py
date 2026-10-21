"""Write sources/dsb-pages.json and sources/dsb-issues.yaml: the *Department of State Bulletin*'s open copies on
archive.org and its issues, 1956-69.

    python3 tools/daybook/make_dsb_index.py [--cache DIR]     (needs the network; the build does not)

The copies: the Boston Public Library's bound volumes, scanned a quarter an item (`departmentofstat461962unit`, vol. 46,
Jan.-Mar. 1962; `departmentofstat4662unit`, Apr.-June), found by archive.org's search; vol. 59 (July-Dec. 1968) is not
among them. For each item, from archive.org's own files: the volume and quarter (its `volume` metadata), the printed
pages its page-number file finds (`_page_numbers.json`), and its text page by page (`_hocr_pageindex.json.gz`,
`_hocr_searchtext.txt.gz`), cached in DIR.

The issues: each issue's cover carries its masthead ("Vol. XLVI, No. 1176 ... January 8, 1962") and its contents; the
leaf's printed page is the issue's first page, the next issue's first page less one its last (a volume's last issue:
the last page of its run). Issue numbers run one a week, Mondays, so a cover the OCR missed takes its number's date
from its neighbours and no pages (`check`). Rows: no, date, vol, first, last, item (the copy holding the cover), leaf.

sources/dsb-pages.json: {items: {id: {vol, from, to, pages: [[a, b], ...], main: [a, b]}}}, `pages` the printed pages
found, as ranges; `main` the run of the issues' pages (not the index bound before or after it). tools/bib/printed.py
links a page by them.
"""
import datetime
import gzip
import json
import os
import re
import sys
import tempfile
import time
import urllib.parse
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = os.path.join(ROOT, "sources", "dsb-pages.json")
ISSUES = os.path.join(ROOT, "sources", "dsb-issues.yaml")
UA = {"User-Agent": "bib-daybook (https://impending2223.github.io/bib/)"}
SEARCH = ("https://archive.org/advancedsearch.php?q=identifier%3Adepartmentofstat*&fl%5B%5D=identifier&fl%5B%5D=title"
          "&fl%5B%5D=volume&rows=1000&output=json")
MONTHS = {m: i + 1 for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
                                          "Dec"])}
FULL = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
        "December"]
MAST = re.compile(r"Vol\.?\s*[LXVI1l]{1,6}[,.]?\s*No\.?\s*(\d{3,4})\b")
TABLE = re.compile(r"\b(\d{3,4})\s+(?:Jan|Feb|Mar|Apr|May|M[au]y|June|July|Aug|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},\s*\S{4}\s+"
                   r"(\d{1,4})\s*-")
DATE = re.compile(r"(" + "|".join(FULL) + r")\s+(\d{1,2}),\s*(19[56]\d)")


def fetch(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
                return r.read()
        except Exception:
            time.sleep(3 * (i + 1))
    raise IOError("failed: " + url)


def cached(cache, name, url):
    p = os.path.join(cache, name)
    if not os.path.exists(p) or os.path.getsize(p) < 1000:
        open(p, "wb").write(fetch(url))
    return p


def quarter(vol_meta):
    """'v. 46, Jan- Mar 1962' -> (46, '1962-01-01', '1962-03-31')."""
    m = re.match(r"v\. (\d+), ([A-Z][a-z]{2})-\s*([A-Z][a-z]{2})\s*(\d{4})", vol_meta)
    if not m:
        return None
    y, a, b = int(m.group(4)), MONTHS[m.group(2)], MONTHS[m.group(3)]
    end = (datetime.date(y + (b == 12), b % 12 + 1, 1) - datetime.timedelta(days=1))
    return int(m.group(1)), datetime.date(y, a, 1).isoformat(), end.isoformat()


def ranges(nums):
    out = []
    for n in sorted(set(nums)):
        if out and n == out[-1][1] + 1:
            out[-1][1] = n
        else:
            out.append([n, n])
    return out


def main_run(seq):
    """The longest run of printed pages rising in leaf order (gaps of up to sixty pages: plates, numbers the OCR
    missed); a run from the volume's first pages starts at 1 (the covers carry no number)."""
    best, cur = [], []
    for n in seq:
        if cur and 0 < n - cur[-1] <= 60:
            cur.append(n)
        else:
            cur = [n]
        if len(cur) > len(best):
            best = list(cur)
    if not best:
        return [0, 0]
    return [1 if best[0] <= 20 else best[0], best[-1]]


def main():
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else os.path.join(tempfile.gettempdir(), "dsb")
    os.makedirs(cache, exist_ok=True)
    docs = json.loads(open(cached(cache, "search.json", SEARCH), "rb").read())["response"]["docs"]
    items = {}
    for x in docs:
        q = quarter(x.get("volume") or "") if "ulletin" in (x.get("title") or "") else None
        if q and 1956 <= int(q[1][:4]) <= 1969 and not x["identifier"].endswith("_0"):
            items[x["identifier"]] = {"vol": q[0], "from": q[1], "to": q[2]}
    covers = []
    for iid in sorted(items, key=lambda k: items[k]["from"]):
        try:
            read(cache, iid, items[iid], covers)
        except IOError as e:                         # a copy archive.org will not serve today: linked by quarter alone
            items[iid]["unread"] = True
            print(iid, e)
    rows = issues(covers, items)
    json.dump({"items": dict(sorted(items.items(), key=lambda kv: kv[1]["from"]))}, open(PAGES, "w", encoding="utf-8"),
              indent=0)
    head = ("# Generated by tools/daybook/make_dsb_index.py from archive.org's copies. Edit the script, not this file.\n"
            "# The Department of State Bulletin's issues: number, date (a Monday), volume, first and last printed page,\n"
            "# the archive.org item and leaf of its cover; check where the cover was not found or the pages disagree.\n")
    open(ISSUES, "w", encoding="utf-8").write(head + yaml.safe_dump({"issues": rows}, sort_keys=False, width=200))
    print(len(items), "items;", len(rows), "issues;", sum("check" in r for r in rows), "to check")


def read(cache, iid, item, covers):
    """One copy: its printed pages, and the covers its text shows (covers: [(no, date, item, leaf, page)])."""
    pn = json.load(open(cached(cache, iid + ".pn.json",
                               f"https://archive.org/download/{iid}/{iid}_page_numbers.json"), encoding="utf-8"))
    leaf_page = {p["leafNum"]: int(p["pageNumber"]) for p in pn["pages"] if str(p.get("pageNumber") or "").isdigit()}
    seq = [leaf_page[k] for k in sorted(leaf_page)]
    item["pages"] = ranges(seq)
    item["main"] = main_run(seq)
    pi = json.loads(gzip.open(cached(cache, iid + ".pi.gz",
                                     f"https://archive.org/download/{iid}/{iid}_hocr_pageindex.json.gz")).read())
    st = gzip.open(cached(cache, iid + ".st.gz",
                          f"https://archive.org/download/{iid}/{iid}_hocr_searchtext.txt.gz")).read().decode("utf-8", "replace")
    lo, hi = item["main"]
    for k, span in enumerate(pi):                    # the hOCR's page k is the leaf numbered k
        head = st[span[0]:span[1]][:700]
        m = MAST.search(head)
        if not m or re.search(r"Publication\s+\d{4}", head):     # the inside masthead (the cover's verso)
            continue
        if re.search(r"(?:^|\n)\s*Index\s*\n", head[:m.start()]):   # the issue's own index (inside back cover)
            continue
        page = next((leaf_page[k + j] - j for j in (0, 1, 2, 3, -1, -2) if k + j in leaf_page), None)
        if page is None or not lo <= page <= hi:
            continue
        d = DATE.search(head)
        date = None
        if d:
            try:
                date = datetime.date(int(d.group(3)), FULL.index(d.group(1)) + 1, int(d.group(2)))
            except ValueError:
                date = None
        covers.append((int(m.group(1)), date, iid, k, page))
    for k, span in enumerate(pi):                    # the volume's index: "1176 Jan. 8, 1962 41- 80" (TABLE)
        rows = [(int(n), int(pg)) for n, pg in TABLE.findall(st[span[0]:span[1]])]
        if len(rows) >= 5 and max(n for n, _ in rows) - min(n for n, _ in rows) <= 30:
            for n, pg in rows:
                item.setdefault("_table", {}).setdefault(n, []).append(pg)


def issues(covers, items):
    """The issues, one a week, numbered in order: each number's date from the covers whose masthead dates agree
    (a Monday, the same count of weeks from the number), the first page from its cover in the copy of its quarter."""
    def base(no, date):
        return date - datetime.timedelta(weeks=no)
    votes = {}
    for no, date, *_ in covers:
        if date and date.weekday() == 0:
            votes[base(no, date)] = votes.get(base(no, date), 0) + 1
    good = [b for b, v in votes.items() if v > 2]
    anchors = sorted((no, date) for no, date, *_ in covers if date and date.weekday() == 0 and base(no, date) in good)

    def date_of(no):
        n0, d0 = min(anchors, key=lambda a: abs(a[0] - no))      # the nearest agreeing cover
        return d0 + datetime.timedelta(weeks=no - n0)
    first = {}
    for no, date, iid, k, page in covers:            # a cover in the copy of its own quarter, its page in the run
        d = date_of(no)
        it = items[iid]
        if not (it["from"] <= d.isoformat() <= it["to"]) or (no in first and first[no][0] <= page):
            continue
        first[no] = (page, iid, k)
    table = {}                                       # the index's first pages, where its OCR reads them
    for it in items.values():
        for n, pgs in it.pop("_table", {}).items():
            table.setdefault(n, []).extend(pgs)
    for n, pgs in table.items():
        pg = max(set(pgs), key=pgs.count)
        if n in first and first[n][0] != pg:
            first[n] = (pg, first[n][1], None)       # the index stands over the cover's leaf
        elif n not in first:
            first[n] = (pg, None, None)
    lo = min(n for n, _d in anchors)
    hi = max(n for n, _d in anchors)
    rows = []
    for no in range(lo, hi + 1):
        d = date_of(no)
        r = {"no": no, "date": d.isoformat(), "vol": 34 + 2 * (d.year - 1956) + (d.month >= 7)}
        if no in first:
            r.update(first=first[no][0], item=first[no][1], leaf=first[no][2])
            if no in table:
                r["src"] = "index"
        rows.append(r)
    for i, r in enumerate(rows):                     # pages: a cover's page after the last one's, before the next one's
        prev = next((s for s in reversed(rows[:i]) if s["vol"] == r["vol"] and s.get("first")), None)
        nxt = next((s for s in rows[i + 1:] if s["vol"] == r["vol"] and s.get("first")), None)
        if r.get("first") and (prev and prev["first"] >= r["first"] or nxt and nxt["first"] <= r["first"]):
            r["check"] = f"cover read as p. {r.pop('first')}: out of order"
            r.pop("item", None), r.pop("leaf", None), r.pop("src", None)
    for i, r in enumerate(rows):
        nxt = rows[i + 1] if i + 1 < len(rows) and rows[i + 1]["vol"] == r["vol"] else None
        if not r.get("first"):
            r.setdefault("check", "cover not found in the copy's text")
            continue
        if nxt is None:
            ends = [it["main"][1] for it in items.values() if it["vol"] == r["vol"] and it.get("main")]
            r["last"] = max(ends) if ends else None
        elif nxt.get("first"):
            r["last"] = nxt["first"] - 1
        if r.get("last") is not None and not 8 <= r["last"] - r["first"] + 1 <= 120:
            r["check"] = f"pages doubtful (read {r['first']}–{r.pop('last')})"
    return [{k: r[k] for k in ("no", "date", "vol", "first", "last", "src", "item", "leaf", "check") if r.get(k) is not None}
            for r in rows]


if __name__ == "__main__":
    main()
