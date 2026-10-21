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


def year(y, cache):
    issues = [r for r in yaml.safe_load(open(ix.ISSUES, encoding="utf-8"))["issues"] if r["date"][:4] == str(y)]
    items = json.load(open(ix.PAGES, encoding="utf-8"))["items"]
    pages = {}
    for iid, it in items.items():
        if str(y) in (it["from"][:4],) and not it.get("unread"):
            for p, t in texts(cache, iid).items():
                pages.setdefault((it["vol"], p), t)
    rows, stats = [], {"issues": len(issues), "indexed": 0, "items": 0, "release": 0, "no index": []}
    for r in issues:
        if not r.get("first") or not r.get("last"):
            stats["no index"].append(r["date"])
            continue
        issue = datetime.date.fromisoformat(r["date"])
        found = []
        for p in range(r["last"], max(r["first"], r["last"] - 4), -1):      # the index: the issue's last pages
            t = pages.get((r["vol"], p), "")
            own = re.search(FULL[issue.month - 1] + r"\s+" + str(issue.day) + r"\b", t[:80])   # its head: the issue's date
            if INDEX.search(t[:150]) or own or re.search(r"No\.\s*" + str(r["no"]), t[:300]) or (
                    found and p == found[-1][0] - 1 and len(index_entries(t, r["first"], r["last"])) > 5):
                found.append((p, t))
        if not found:
            stats["no index"].append(r["date"])
            continue
        stats["indexed"] += 1
        seen = {}                                   # page -> [titles], one an item (several OCR readings of one)
        for _p, t in sorted(found):
            for title, page in index_entries(t, r["first"], r["last"]):
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
            d = release_date(pages.get((r["vol"], page)), issue) if one else None
            n += 1
            row = {"key": f"dsb:{r['date']}:{page}:{n}", "src": "dsb", "date": (d or issue).isoformat(),
                   "issue": r["date"], "page": page, "title": title, "dated": "release" if d else "issue"}
            u = printed.page_url(r["date"], page)
            if u:
                row["url"] = u
            rows.append(row)
            stats["release"] += bool(d)
        stats["items"] += n
    rows.sort(key=lambda x: (x["date"], x["issue"], x["page"]))
    os.makedirs(OUT, exist_ok=True)
    head = ("# Generated by tools/daybook/make_bulletin.py from archive.org's copies of the Department of State\n"
            "# Bulletin. Edit the script, not this file. One row an item of an issue's own index: key, src (dsb),\n"
            "# date (the day filed: its release where its page prints one, else the issue's), issue, page, title (as the\n"
            "# OCR reads the index), dated (release|issue), url (the copy's page).\n")
    open(os.path.join(OUT, f"{y}.yaml"), "w", encoding="utf-8").write(
        head + yaml.safe_dump({"year": int(y), "docs": rows}, sort_keys=False, allow_unicode=True, width=200))
    print(y, stats)


def main():
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else os.path.join(tempfile.gettempdir(), "dsb")
    years = [a for a in sys.argv[1:] if re.match(r"^\d{4}$", a)]
    for y in years:
        year(int(y), cache)


if __name__ == "__main__":
    main()
