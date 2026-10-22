"""Write daybook/bulletin/<YYYY>.yaml: the *Department of State Bulletin*'s contents, item by item, filed by day.

    python3 tools/daybook/make_bulletin.py YEAR [YEAR ...] [--cache DIR]   (DIR: make_dsb_index.py's cache; network
                                                                            for what it lacks; the build needs none)

For each issue of the year (sources/dsb-issues.yaml, its first and last pages), from the Boston Public Library's copy on
archive.org, page by page (the hOCR text and the page numbers make_dsb_index.py reads):

 1. The issue's own index, on its inside back cover ("Index / Vol. XLVI, No. 1176"): every entry, "Subject. Title
    (names) page", the subject heading taken off (a line of its own, or the words before the first full stop where
    they are a short heading). An item the index lists under several subjects is one item: the same page and the same
    first words of its title. The title as the OCR reads it, its spaces and hyphens at line breaks mended.
 2. The item's date: where the item's first page prints its release ("Press release 23 dated January 15", "White House
    press release dated ..."), the date it gives (the year the issue's, or the one before for a December release in a
    January issue), not after the issue's date nor more than 60 days before it (`dated: release`); else the issue's
    date (`dated: issue`).
 3. Rows: key ('dsb:<issue date>:<page>:<n>'), src 'dsb', date (the day filed), issue, page, title, url (the copy's
    page). Shown in the daybook as a fifth list, "Bulletin" (tools/bib/daybook.py, STYLE 10).

Quality (1962, the first year done): see the counts this prints; titles keep OCR errors the index's type invited.
"""
import datetime
import gzip
import json
import os
import re
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import make_dsb_index as ix  # noqa: E402
from bib import printed  # noqa: E402

OUT = os.path.join(ROOT, "daybook", "bulletin")
FROM, TO = datetime.date(1960, 1, 6), datetime.date(1969, 1, 20)        # the calendar's first and last days
FULL = ix.FULL
RELEASE = re.compile(r"(?:press\s+release|release)\s+(?:No\.\s*)?(?:\d+\s+)?dated\s+(" + "|".join(FULL)
                     + r")\s+(\d{1,2})", re.I)
NAME = re.compile(r"^[A-Z][\w'’\-]+(?: [A-Z][\w'’\-]+)?, [A-Z][\w.]*(?: [A-Z][\w.]*){0,3}(?:, Jr)?$")   # "Ball, George W"
INDEX = re.compile(r"\b(?:I\s?n\s?d\s?e\s?x|ndex|Inde)\b")
LINE_END = re.compile(r"^(.*?\S)\s*[.\s]*?\s(\d{1,4})\s*$")


def texts(cache, iid):
    """{printed page: text} for one copy."""
    pn = json.load(open(ix.cached(cache, iid + ".pn.json", f"https://archive.org/download/{iid}/{iid}_page_numbers.json"),
                        encoding="utf-8"))
    leaf_page = {p["leafNum"]: int(p["pageNumber"]) for p in pn["pages"] if str(p.get("pageNumber") or "").isdigit()}
    pi = json.loads(gzip.open(ix.cached(cache, iid + ".pi.gz",
                                        f"https://archive.org/download/{iid}/{iid}_hocr_pageindex.json.gz")).read())
    st = gzip.open(ix.cached(cache, iid + ".st.gz",
                             f"https://archive.org/download/{iid}/{iid}_hocr_searchtext.txt.gz")).read().decode("utf-8", "replace")
    out = {}
    for k, span in enumerate(pi):
        if k in leaf_page:
            out.setdefault(leaf_page[k], st[span[0]:span[1]])
    return out


def mend(t):
    t = re.sub(r"(\w)- (\w)", lambda m: m.group(1) + ("-" if m.group(2)[0].isupper() else "") + m.group(2), t)
    t = re.sub(r"\s+", " ", t).strip(" .")
    return re.sub(r"\s+([,.;:)])", r"\1", t)


def index_entries(text, first, last):
    """(title, page) from an issue's index page text."""
    text = re.split(r"\n\s*N\s*a\s*m\s*e\s+I\s*n\s*d\s*e\s*x\b", text)[0]     # the names' index after it: not items
    # an entry ending mid-line, another after it: "... (Rusk) .. 83 U.S. Refutes ..."
    text = re.sub(r"(\S)\s*\.*\s+(\d{1,4})\s+(?=[A-Z\"“])",
                  lambda m: m.group(1) + " " + m.group(2) + ("\n" if first <= int(m.group(2)) <= last else " "), text)
    lines = [x.strip() for x in text.split("\n")]
    out, buf, heading = [], "", None
    for ln in lines:
        if not ln or re.match(r"^(?:Index|Vol\.?\s|[A-Z][a-z]+\s+\d{1,2},\s*\d{4})", ln) and not buf:
            continue
        cur = (buf + " " + ln).strip() if buf else ln
        m = LINE_END.match(cur)
        if m and first <= int(m.group(2)) <= last:
            body = m.group(1)
            sub = re.match(r"^([A-Z][\w,'’()\-]*(?:\s+[\w,'’()\-]+){0,4}?)\.\s+(?=[A-Z0-9\"“])", body)
            if sub and not re.search(r"\b(?:U|S|Mr|Mrs|Dr|St|No)$", sub.group(1)):
                heading, body = sub.group(1), body[sub.end():]
            title = mend(body)
            if not NAME.match(title) and not re.search(r"\d,?$", title):
                out.append((title, int(m.group(2))))
            buf = ""
        elif len(cur) < 45 and not re.search(r"\d", cur) and not buf:
            heading, buf = cur, ""                       # a subject heading on a line of its own
        else:
            buf = cur
            if len(buf) > 400:
                buf = ""
    return out


def words(title):
    return set(re.findall(r"[a-z]{3,}", title.lower())) - {"the", "and", "for", "text", "with"}


def release_date(text, issue):
    """The one release date a page prints (none where it prints several: whose is whose is not known)."""
    found = RELEASE.findall(text or "")
    if len({(a.lower(), b) for a, b in found}) != 1:
        return None
    for m in RELEASE.finditer(text or ""):
        mon, day = FULL.index(m.group(1).capitalize()) + 1, int(m.group(2))
        y = issue.year - (1 if mon > issue.month + 1 else 0)
        try:
            d = datetime.date(y, mon, day)
        except ValueError:
            continue
        if issue - datetime.timedelta(days=60) <= d <= issue:
            return d
    return None


def leaves(cache, iid):
    """[(leaf, printed page or None, text)] for one copy, in leaf order."""
    pn = json.load(open(ix.cached(cache, iid + ".pn.json", f"https://archive.org/download/{iid}/{iid}_page_numbers.json"),
                        encoding="utf-8"))
    leaf_page = {p["leafNum"]: int(p["pageNumber"]) for p in pn["pages"] if str(p.get("pageNumber") or "").isdigit()}
    pi = json.loads(gzip.open(ix.cached(cache, iid + ".pi.gz",
                                        f"https://archive.org/download/{iid}/{iid}_hocr_pageindex.json.gz")).read())
    st = gzip.open(ix.cached(cache, iid + ".st.gz",
                             f"https://archive.org/download/{iid}/{iid}_hocr_searchtext.txt.gz")).read().decode("utf-8", "replace")
    return [(k, leaf_page.get(k), st[span[0]:span[1]]) for k, span in enumerate(pi)]


HEAD_INDEX = re.compile(r"I\s?N\s?D\s?E\s?X|I\s?n\s?d\s?e\s?[xX]|\bndex\b|\bInde\b")
VOL_INDEX = re.compile(r"Volume\s+\S+\s*:?\s*Numbers|Numbers\s+\d{4}\s*-\s*\d{4}")
BACK = re.compile(r"OFFICIAL\s+BUSINESS|PENALTY\s+FOR\s+PRIVATE|POSTAGE\s+AND\s+FEES\s+PAID", re.I)
HEAD_DATE = re.compile(r"(" + "|".join(FULL) + r")\s*(\d{1,2})\s*[,.]\s*(19[56]\d)")
HEAD_NO = re.compile(r"No\.?\s*(1[0-5]\d\d)\b")


def run(pages):
    """The longest run of printed pages rising in leaf order (steps of 1 to 6: plates, numbers the OCR missed)."""
    best, cur = [], []
    for n in pages:
        cur = cur + [n] if cur and 0 < n - cur[-1] <= 6 else [n]
        if len(cur) > len(best):
            best = list(cur)
    return best


def index_leaves(L, lo, hi):
    """The leaves of a copy holding an issue's own index (RULES 1): a head with "Index" (not the volume's index), or
    the leaf before the back cover (its mailing text), whose text reads as at least eight index entries within the
    volume's pages, most of them within 150 of one another."""
    out = []
    for i, (k, p, t) in enumerate(L):
        h = t[:250]
        if VOL_INDEX.search(h):
            continue
        before_back = i + 1 < len(L) and BACK.search(L[i + 1][2][:600])
        if not (HEAD_INDEX.search(h) or before_back):
            continue
        ents = index_entries(t, lo, hi)
        pg = sorted(e[1] for e in ents)
        if len(pg) < 8:
            continue
        mid = pg[len(pg) // 2]
        if sum(abs(x - mid) <= 75 for x in pg) < max(8, 0.6 * len(pg)):     # an OCR's 6 for 5 in a column
            continue
        out.append(i)
    return out


def head_issue(h, quarter, by_date, by_no):
    """The issue an index leaf's head names: its date, else its number, where the quarter holds it."""
    m = HEAD_DATE.search(h)
    if m:
        try:
            r = by_date.get(datetime.date(int(m.group(3)), FULL.index(m.group(1)) + 1, int(m.group(2))).isoformat())
        except ValueError:
            r = None
        if r in quarter:
            return r
    m = HEAD_NO.search(h)
    r = by_no.get(int(m.group(1))) if m else None
    return r if r in quarter else None


def place(L, segs, quarter, by_date, by_no, lo, hi):
    """[(seg, issue)] for one copy's index leaves (RULES 2): by the head's date or number; else the issue whose pages
    (sources/dsb-issues.yaml) hold the entries' median page; else, between two placed leaves, in order, where as many
    issues as leaves lie between them."""
    got = []
    for s in segs:
        r = head_issue(L[s[0]][2][:300], quarter, by_date, by_no)
        if r is None:
            ents = sorted(e[1] for e in index_entries(L[s[0]][2], lo, hi))
            med = ents[len(ents) // 2]
            cand = [q for q in quarter if q.get("first") and q.get("last") and not q.get("check")
                    and q["first"] <= med <= q["last"]]
            r = cand[0] if len(cand) == 1 else None
        got.append(r)
    nos = [q["no"] for q in quarter]
    k = 0
    while k < len(got):
        if got[k] is not None:
            k += 1
            continue
        e = k
        while e < len(got) and got[e] is None:
            e += 1
        a = got[k - 1]["no"] if k > 0 else nos[0] - 1
        b = got[e]["no"] if e < len(got) else nos[-1] + 1
        between = [q for q in quarter if a < q["no"] < b]
        if len(between) == e - k:
            got[k:e] = between
        k = e
    seen, out = set(), []
    for s, r in zip(segs, got):                    # each issue once, and in order
        if r is not None and r["no"] not in seen and (not out or r["no"] > out[-1][1]["no"]):
            seen.add(r["no"])
            out.append((s, r))
    return out


def year(y, cache, since=None, until=None):
    """One year's rows: the issues dated in it (from since), and to until those of the next sixty days whose releases
    fall before it."""
    allrows = yaml.safe_load(open(ix.ISSUES, encoding="utf-8"))["issues"]
    by_date = {r["date"]: r for r in allrows}
    by_no = {r["no"]: r for r in allrows}
    lo_d = since or datetime.date(y, 1, 1)
    hi_d = (until + datetime.timedelta(days=60)) if until else datetime.date(y, 12, 31)
    issues = [r for r in allrows if lo_d.isoformat() <= r["date"] <= hi_d.isoformat()]
    want = {r["date"] for r in issues}
    items = json.load(open(ix.PAGES, encoding="utf-8"))["items"]
    pages, found, log = {}, {}, []
    for iid, it in sorted(items.items(), key=lambda kv: kv[1]["from"]):
        if it.get("unread") or not any(it["from"] <= d <= it["to"] for d in want):
            continue
        L = leaves(cache, iid)
        for k, p, t in L:
            if p is not None:
                pages.setdefault((it["vol"], p), t)
        lo, hi = 1, 1300                               # any page of a volume: a copy's numbering can run out of order
        quarter = [r for r in allrows if it["from"] <= r["date"] <= it["to"]]
        segs, prev = [], None
        for i in index_leaves(L, lo, hi):             # the issue's pages: the numbered leaves since the last index
            top = it["main"][0] + 200 if not segs else hi       # not the volume's index bound before the first issue
            seq = [L[j][1] for j in range((prev + 1) if prev is not None else 0, i + 1)
                   if L[j][1] is not None and it["main"][0] - 80 <= L[j][1] <= top]
            r_ = run(seq)
            sf, sl = (r_[0], r_[-1]) if r_ else (None, None)
            if sf is not None and (not segs or segs[-1][2] is None) and it["from"][5:7] in ("01", "07") and sf <= 20:
                sf = 1                                 # a volume's first issue: its covers carry no number
            elif sf is not None and segs and segs[-1][2] is not None and 0 < sf - segs[-1][2] <= 20:
                sf = segs[-1][2] + 1                   # pages the numbering missed: after the last issue's
            segs.append((i, sf, sl))
            prev = i
        placed = place(L, segs, quarter, by_date, by_no, lo, hi)
        for s in segs:
            if s not in [x for x, _ in placed]:
                log.append(f"{iid} leaf {s[0]}: an index not placed")
        for (i, sf, sl), r in placed:
            ls = [i]
            j = i + 1                                   # an index run on to the next leaf (not the back cover, a cover)
            if j < len(L) and not BACK.search(L[j][2][:600]) and not HEAD_INDEX.search(L[j][2][:250]) \
                    and not ix.MAST.search(L[j][2][:700]) and len(index_entries(L[j][2], lo, hi)) > 8:
                ls.append(j)
            found[r["date"]] = {"iid": iid, "vol": it["vol"], "sf": sf, "sl": sl, "leaves": ls, "L": L}
    rows, stats = [], {"issues": len(issues), "indexed": 0, "items": 0, "release": 0, "no index": []}
    for r in issues:
        if r["date"] not in found:
            stats["no index"].append(r["date"])
            continue
        f = found[r["date"]]
        vol, sf, sl, ls, L = f["vol"], f["sf"], f["sl"], f["leaves"], f["L"]
        first, last = r.get("first"), r.get("last")
        if not first or not last or r.get("check"):    # the pages the leaves give (RULES 3)
            first, last = sf, sl
            log.append(f"{r['date']}: pages from the leaves, {sf}-{sl}")
        elif sf and sl and (abs(sf - first) > 2 or abs(sl - last) > 4):
            log.append(f"{r['date']}: issues {first}-{last}, leaves {sf}-{sl}")
        if not first or not last:
            stats["no index"].append(r["date"])
            continue
        stats["indexed"] += 1
        issue = datetime.date.fromisoformat(r["date"])
        seen = {}                                   # page -> [titles], one an item (several OCR readings of one)
        for j in sorted(set(ls)):
            for title, page in index_entries(L[j][2], first, last):
                w = words(title)
                if not w:
                    continue
                have = seen.setdefault(page, [])
                same = next((i for i, x in enumerate(have) if len(w & words(x)) >= 0.5 * min(len(w), len(words(x)))), None)
                if same is None:
                    have.append(title)
                elif len(title) > len(have[same]) and len(title) < 2 * len(have[same]):
                    have[same] = title                  # the fuller reading
        n = 0
        for page, title, one in [(p, t, len(ts) == 1) for p, ts in sorted(seen.items()) for t in ts]:
            d = release_date(pages.get((vol, page)), issue) if one else None
            n += 1
            day = d or issue
            if since and day < since or until and day > until or not until and issue.year > y:
                continue
            row = {"key": f"dsb:{r['date']}:{page}:{n}", "src": "dsb", "date": day.isoformat(),
                   "issue": r["date"], "page": page, "title": title, "dated": "release" if d else "issue"}
            u = printed.page_url(r["date"], page)
            if u:
                row["url"] = u
            rows.append(row)
            stats["release"] += bool(d)
            stats["items"] += 1
    rows.sort(key=lambda x: (x["date"], x["issue"], x["page"]))
    os.makedirs(OUT, exist_ok=True)
    head = ("# Generated by tools/daybook/make_bulletin.py from archive.org's copies of the Department of State\n"
            "# Bulletin. Edit the script, not this file. One row an item of an issue's own index: key, src (dsb),\n"
            "# date (the day filed: its release where its page prints one, else the issue's), issue, page, title (as the\n"
            "# OCR reads the index), dated (release|issue), url (the copy's page).\n")
    open(os.path.join(OUT, f"{y}.yaml"), "w", encoding="utf-8").write(
        head + yaml.safe_dump({"year": int(y), "docs": rows}, sort_keys=False, allow_unicode=True, width=200))
    print(y, stats)
    for x in log:
        print("  ", x)


def main():
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else os.path.join(tempfile.gettempdir(), "dsb")
    years = [a for a in sys.argv[1:] if re.match(r"^\d{4}$", a)]
    for y in years:                                   # the calendar's span: from Jan. 6, 1960, to Jan. 20, 1969
        y = int(y)
        year(y, cache, since=FROM if y == FROM.year else None, until=TO if y == TO.year else None)


if __name__ == "__main__":
    main()
