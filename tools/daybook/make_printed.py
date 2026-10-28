"""Write daybook/printed.yaml: where FRUS's own notes say a text was printed at the time, in the *Department of State
Bulletin* or *American Foreign Policy: Current Documents*, by FRUS document.

    python3 tools/daybook/make_printed.py [--cache DIR]      (DIR: the FRUS TEI files make_daybook.py reads)

One pass over every FRUS volume the daybook reads (make_daybook.VOLS; a volume missing from the cache is fetched from
github.com/HistoryAtState/frus), each document's notes read for the two works' citations, as FRUS writes them:

    Department of State Bulletin, March 27, 1961, pp. 449-454      -> {work: dsb, date: 1961-03-27, pages: 449–454}
    American Foreign Policy: Current Documents, 1961, pp. 579-583  -> {work: cd, year: 1961, pages: 579–583}

and what follows them in the same note: "and April 3, 1961, p. 5" (another issue), "ibid., p. 843" (the same issue or
volume), "ibid., May 8, 1961, p. 662". Only the documents the daybook holds (daybook/<YYYY-MM>.yaml) are kept.

Each row says which note holds it: `note: source` (the source note under the heading) or the footnote's number. A
source note's citation is the document's own text printed (`self: true`) where its sentence says so: "Source:
Department of State Bulletin ...", "Printed in ...", "Also printed in ...", "The letter is also printed in ...", "A
slightly different text is printed in ..."; not "For text of the joint communiqué, see ...", nor "..., which is printed
in ...". The Bulletin's citations take a link to the Boston Public Library's copy on archive.org at the printed page
(tools/bib/printed.py, `bulletin_url`, from sources/dsb-pages.json), and a `check` where the date is no issue's (the
issues: sources/dsb-issues.yaml) or the page is not in that issue's pages. Nothing is linked for *Current Documents*:
no open copy found (notes/extensions/memos/fiscal-congress-conventions-state.md, section 6).

Rendered by tools/bib/printed.py (its STYLE notes), under each FRUS document in the daybook.
"""
import datetime
import glob
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import make_daybook as mk  # noqa: E402
from bib import printed  # noqa: E402

OUT = os.path.join(ROOT, "daybook", "printed.yaml")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
M = "(?:" + "|".join(MONTHS) + ")"
DATE = rf"({M}) (\d{{1,2}}),? (\d{{4}})"
PAGES = r"(?:pp?[.,]?|pages?)\s?(\d+(?:\s?[-–]\s?\d+)?(?:,? (?:and )?\d+(?:\s?[-–]\s?\d+)?)*)"
BULL = re.compile(rf"(?:Department of State |the )?Bulletin[,;]? {DATE}[,.] {PAGES}")
CURR = re.compile(rf"Current Documents,? (\d{{4}}),? {PAGES}")
# after a citation: another issue or year of the same work
MORE_B = re.compile(rf"^(?:,|;)? (?:and|or) (?:in )?{DATE}, {PAGES}")
MORE_C = re.compile(rf"^(?:,|;)? (?:and|or) (?:in )?(\d{{4}}), {PAGES}")
IBID = re.compile(rf"\bibid\.,? (?:{DATE}, |(\d{{4}}), )?{PAGES}")
OTHER = re.compile(r"Documents on|Public Papers|Foreign Relations|Pravda|Izvestia|Times|Post\b|U\.N\. doc|"
                   r"Kennedy, 19|Johnson, 19|Eisenhower, 19|Claflin|Department of State, |Central Files|Lot \d")
SELF = re.compile(r"^(?:Source:|Printed\b|Also printed|Text is also printed|A slightly different|(?:The|This)\b[^.;]{0,200}"
                  r"\b(?:is|are) (?:also )?(?:printed|summarized)\b)")
NOT_SELF = re.compile(r"\b(?:For (?:the )?text|For a summary|see\b|which is|of which|issued|released)\b", re.I)
ABBR = re.compile(r"(?:\b(?:pp?|vol|Vol|No|no|doc|Doc|Dr|Mr|Mrs|St|ed|eds|ff|Jr|Sr|[A-Z])\.)$")


def norm_pages(p):
    p = re.sub(r"\s?[-–]\s?", "–", p)
    return re.sub(r",? and ", ", ", p)


def first_page(p):
    return int(re.match(r"\d+", p).group(0))


def sentence_start(t, i):
    """Index of the start of the sentence holding position i: after the last '. ' (or ') ') before it that ends
    a sentence (not 'p. ', 'U.S. ', 'F. ')."""
    j = i
    while True:
        k = max(t.rfind(". ", 0, j), t.rfind("; ", 0, j))
        if k < 0:
            return 0
        if t[k] == ";" or not ABBR.search(t[:k + 1]):
            return k + 2
        j = k


def iso(mon, day, year):
    try:
        return datetime.date(int(year), MONTHS.index(mon) + 1, int(day)).isoformat()
    except ValueError:
        return None


def cites(t, source):
    """The two works' citations in one note's text, in order."""
    out = []
    for m in sorted(list(BULL.finditer(t)) + list(CURR.finditer(t)), key=lambda m: m.start()):
        if m.re is BULL:
            row = {"work": "dsb", "date": iso(*m.groups()[:3]), "pages": norm_pages(m.group(4))}
            if row["date"] is None:
                continue
        else:
            row = {"work": "cd", "year": int(m.group(1)), "pages": norm_pages(m.group(2))}
        rows = [(m.start(), row)]
        rest, end = t[m.end():], m.end()
        while True:                                  # "and April 3, 1961, p. 5"; "and 1962, pp. 12–14"
            n = (MORE_B if row["work"] == "dsb" else MORE_C).match(rest)
            if not n:
                break
            if row["work"] == "dsb":
                d = iso(*n.groups()[:3])
                if d:
                    rows.append((end, {"work": "dsb", "date": d, "pages": norm_pages(n.group(4))}))
            else:
                rows.append((end, {"work": "cd", "year": int(n.group(1)), "pages": norm_pages(n.group(2))}))
            end += n.end()
            rest = t[end:]
        k = end
        for n in IBID.finditer(t, end):             # "ibid., p. 843": the same work, if nothing came between
            if OTHER.search(t[k:n.start()]) or BULL.search(t[k:n.start()]) or CURR.search(t[k:n.start()]):
                break
            r = {"work": row["work"], "pages": norm_pages(n.group(5))}
            if row["work"] == "dsb":
                r["date"] = iso(*n.groups()[:3]) if n.group(1) else row["date"]
                if not r["date"]:
                    break
            else:
                r["year"] = int(n.group(4)) if n.group(4) else row["year"]
            rows.append((n.start(), r))
            k = n.end()
        for pos, r in rows:
            if source:
                s = t[sentence_start(t, pos):pos]
                if SELF.match(s) and not NOT_SELF.search(s):
                    r["self"] = True
            out.append(r)
    return out


def held():
    """The FRUS documents the daybook holds."""
    keys = set()
    for f in glob.glob(os.path.join(ROOT, "daybook", "[0-9][0-9][0-9][0-9]-[0-9][0-9].yaml")):
        for x in (yaml.safe_load(open(f, encoding="utf-8")) or {}).get("docs", []):
            if x.get("src") == "frus":
                keys.add(x["key"])
    return keys


def main():
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else os.path.join(tempfile.gettempdir(), "frus-tei")
    os.makedirs(cache, exist_ok=True)
    keys = held()
    out, n = {}, {"dsb": 0, "cd": 0, "self": 0, "check": 0, "linked": 0}
    for vol in mk.VOLS:
        path = os.path.join(cache, vol + ".xml")
        if not os.path.exists(path):
            open(path, "wb").write(mk.fetch(mk.RAW + vol + ".xml"))
        root = ET.parse(path).getroot()
        for d in root.iter(mk.T + "div"):
            if d.get("type") != "document":
                continue
            key = f"frus:{vol}/{d.get(mk.XID)}"
            if key not in keys:
                continue
            rows = []
            for note in d.iter(mk.T + "note"):
                t = re.sub(r"\s+", " ", "".join(note.itertext())).strip()
                if "Bulletin" not in t and "Current Documents" not in t:
                    continue
                source = note.get("type") == "source" or t.startswith("Source:")
                for r in cites(t, source):
                    r["note"] = "source" if source else str(note.get("n") or "")
                    if r["work"] == "dsb":
                        url, check = printed.locate(r["date"], first_page(r["pages"]))
                        if url:
                            r["url"] = url
                            n["linked"] += 1
                        if check:
                            r["check"] = check
                            n["check"] += 1
                    if r not in rows:
                        rows.append(r)
            if rows:
                out[key] = [{k: r[k] for k in ("work", "date", "year", "pages", "note", "self", "url", "check") if k in r}
                            for r in rows]
                for r in rows:
                    n[r["work"]] += 1
                    n["self"] += bool(r.get("self"))
    head = ("# Generated by tools/daybook/make_printed.py from FRUS's notes. Edit the script, not this file.\n"
            "# FRUS key -> the texts its notes cite in the Department of State Bulletin (dsb: issue date, pages) or\n"
            "# American Foreign Policy: Current Documents (cd: year, pages); note: source or the footnote's number;\n"
            "# self: the document itself printed; url: the Bulletin's page on archive.org; check: to verify.\n")
    body = yaml.safe_dump({"printed": out}, sort_keys=False, allow_unicode=True, width=200)
    open(OUT, "w", encoding="utf-8").write(head + body)
    print(len(out), "documents;", n)


if __name__ == "__main__":
    main()
