"""Where FRUS's documents and the texts their notes cite were printed at the time: the *Department of State Bulletin*
and *American Foreign Policy: Current Documents*. Shown under each FRUS document in the daybook (tools/bib/daybook.py).

    daybook/printed.yaml     FRUS key -> [{work: dsb|cd, date|year, pages, note, self, url, check}]; written by
                             tools/daybook/make_printed.py from FRUS's own notes (never edit)
    sources/dsb-pages.json   the Bulletin's copies on archive.org (the Boston Public Library's, a quarter an item): each
                             item's volume, quarter and printed pages; written by tools/daybook/make_dsb_index.py
    sources/dsb-issues.yaml  the Bulletin's issues, 1956-69: number, date, volume, first and last page, read from each
                             volume's index ("Issue Number / Date of Issue / Pages"); the same script

STYLE:
 1. Under the FRUS document, muted, one line: "Printed: *Bulletin*, Jan. 15, 1962, p. 93" where the source note says
    the document's own text was printed (`self`); then, on its own line, "In the notes: *Bulletin*, Mar. 27, 1961,
    pp. 449–454 (n. 3); *Current Documents, 1961*, pp. 579–583 (n. 4)" for the texts its footnotes cite there ("source
    note" for one its source note cites). The works by short title, italic; the Bulletin's issue by its date, the
    series' month forms; each work's name linked to its card's entry in the A–Z bibliography (works.html).
 2. A Bulletin citation links its pages to the archive.org copy at the printed page (`/page/93/mode/1up`), where a copy
    holds the page; *Current Documents* is unlinked (no open copy found). A citation whose date is no issue's, or whose
    page is not in its issue's pages (sources/dsb-issues.yaml), shows "Check" after it, the reason on hover; its page
    stays linked (the page FRUS cites, whatever the date).
 3. Nothing of FRUS's wording is shown: the work, the date or year, the pages, the note.
"""
import bisect
import datetime
import html
import json
import os

import yaml

from . import store

PRINTED = os.path.join(store.ROOT, "daybook", "printed.yaml")
PAGES = os.path.join(store.ROOT, "sources", "dsb-pages.json")
ISSUES = os.path.join(store.ROOT, "sources", "dsb-issues.yaml")
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
IA = "https://archive.org/details/{item}/page/{page}/mode/1up"

_cache = {}


def esc(t):
    return html.escape(str(t), quote=True)


def vol_of(date):
    """The Bulletin's volume for an issue date: two a year, Jan.-June and July-Dec. (34 = Jan.-June 1956)."""
    d = datetime.date.fromisoformat(str(date))
    return 34 + 2 * (d.year - 1956) + (d.month >= 7)


def items():
    if "items" not in _cache:
        _cache["items"] = (json.load(open(PAGES, encoding="utf-8")).get("items", {}) if os.path.exists(PAGES) else {})
    return _cache["items"]


def issues():
    """{date: issue} from sources/dsb-issues.yaml."""
    if "issues" not in _cache:
        rows = (yaml.safe_load(open(ISSUES, encoding="utf-8")) or {}).get("issues", []) if os.path.exists(ISSUES) else []
        _cache["issues"] = {str(r["date"]): r for r in rows}
    return _cache["issues"]


def _has(ranges, p):
    i = bisect.bisect_right([a for a, b in ranges], p) - 1
    return i >= 0 and ranges[i][0] <= p <= ranges[i][1]


def page_url(date, page):
    """The archive.org copy at the printed page of the Bulletin's volume for that date, or None. Of the volume's items
    the one holding the page (both: the one whose quarter holds the date); a page the copy's numbering skipped, the
    nearest it holds within two pages."""
    v = vol_of(date)
    cands = [(k, it) for k, it in items().items() if it["vol"] == v]
    for delta in (0, -1, 1, -2, 2):     # archive.org finds a printed page only where its numbering read one
        hit = [(k, it) for k, it in cands if it.get("pages") and _has(it["pages"], page + delta)
               and it["main"][0] <= page + delta <= it["main"][1]]
        if not hit:
            continue
        if len(hit) > 1:
            hit = [h for h in hit if h[1]["from"] <= str(date) <= h[1]["to"]] or hit
        return IA.format(item=hit[0][0], page=page + delta)
    for k, it in cands:                  # a copy archive.org would not serve when the pages were read: by its quarter
        if it.get("unread") and it["from"] <= str(date) <= it["to"]:
            return IA.format(item=k, page=page)
    return None


def locate(date, page):
    """(url, check) for a Bulletin citation: the copy's page, and why it needs checking (None where it agrees with
    the issue's pages)."""
    iss = issues()
    vols = {r["vol"] for r in iss.values()}
    r = iss.get(str(date))
    check = None
    if r is None:
        if vol_of(date) in vols:
            check = "no issue of that date"
    elif r.get("first") and r.get("last") and not r.get("check") and not r["first"] <= page <= r["last"]:
        check = f"the issue of that date is pp. {r['first']}–{r['last']}"
    return page_url(date, page), check


def day(date):
    d = datetime.date.fromisoformat(str(date))
    return f"{MON[d.month - 1]} {d.day}, {d.year}"


def load():
    if "rows" not in _cache:
        _cache["rows"] = ((yaml.safe_load(open(PRINTED, encoding="utf-8")) or {}).get("printed", {})
                          if os.path.exists(PRINTED) else {})
    return _cache["rows"]


def cite_html(r, with_note=True):
    pp = ("pp. " if any(c in r["pages"] for c in "–,") else "p. ") + r["pages"]
    from .markup import WORKS_PAGE
    cid = card(r)
    if r["work"] == "dsb":
        pg = f'<a class="src" href="{esc(r["url"])}" title="archive.org">{esc(pp)}</a>' if r.get("url") else esc(pp)
        name = "<i>Bulletin</i>"
        rest = f", {esc(day(r['date']))}, {pg}"
    else:
        name = f"<i>Current Documents, {esc(r['year'])}</i>"
        rest = f", {esc(pp)}"
    out = (f'<a href="{WORKS_PAGE}#{esc(cid)}">{name}</a>' if cid else name) + rest
    if r.get("check"):
        out += f' <i title="{esc(r["check"])}">Check</i>'
    if with_note:
        out += " (source note)" if r.get("note") == "source" else (f" (n. {esc(r['note'])})" if r.get("note") else "")
    return out


BULLETIN = "w.department-of-state-bulletin"


def card(r):
    """The works catalogue's card for a row's work: the Bulletin's, or Current Documents' of the year (1956-67)."""
    if r["work"] == "dsb":
        return BULLETIN
    return f"w.current-documents-{r['year']}" if 1956 <= int(r.get("year") or 0) <= 1967 else None


def cards():
    """The cards the daybook's rows point to (for the works check: a card nothing points to)."""
    return {c for rows in load().values() for r in rows for c in [card(r)] if c}


def lines(key):
    """The muted lines under a FRUS document (STYLE 1-3); '' where its notes cite neither work."""
    rows = load().get(key)
    if not rows:
        return ""
    own = [r for r in rows if r.get("self")]
    rest = [r for r in rows if not r.get("self")]
    out = []
    if own:
        out.append('<span class="pr">Printed: ' + "; ".join(cite_html(r, False) for r in own) + "</span>")
    if rest:
        out.append('<span class="pr">In the notes: ' + "; ".join(cite_html(r) for r in rest) + "</span>")
    return "".join(out)


def made_public(key):
    """The rows of a FRUS document's own text printed (`self`), for the calendar's "Made public:" line."""
    return [r for r in load().get(key, []) if r.get("self")]


def problems(daybook_keys):
    """For ./bib check: a row for a document the daybook lacks, an unknown work, a bad date or year, a link off
    archive.org; sources/dsb-issues.yaml out of order."""
    out = []
    for k, rows in load().items():
        if k not in daybook_keys:
            out.append((k, "printed: a document not in daybook/"))
        for r in rows:
            if r.get("work") not in ("dsb", "cd"):
                out.append((k, f"printed: unknown work {r.get('work')!r}"))
            elif r["work"] == "dsb":
                try:
                    datetime.date.fromisoformat(str(r.get("date")))
                except ValueError:
                    out.append((k, f"printed: bad Bulletin date {r.get('date')!r}"))
            elif not (1950 <= int(r.get("year") or 0) <= 1990):
                out.append((k, f"printed: bad Current Documents year {r.get('year')!r}"))
            if r.get("url") and not str(r["url"]).startswith("https://archive.org/details/"):
                out.append((k, f"printed: link off archive.org {r['url']}"))
            if not r.get("pages"):
                out.append((k, "printed: no pages"))
    prev = None
    for d, r in sorted(issues().items()):
        if prev and r.get("first") and prev.get("last") and r["vol"] == prev["vol"] and r["first"] <= prev["last"]:
            out.append((d, f"dsb-issues: no. {r.get('no')} begins before no. {prev.get('no')} ends"))
        prev = r
    return out
