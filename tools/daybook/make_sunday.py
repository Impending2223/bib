"""Write daybook/sunday.yaml: the guests of the Sunday interview programs in the calendar's span, Jan. 1961–Jan. 10, 1966.

    python3 tools/daybook/make_sunday.py        (needs pdftotext; the network for the listings, else they are skipped)

Meet the Press (NBC):
  - the record: the Library of Congress's Prints and Photographs Division, "Visual Materials from the Lawrence E. Spivak
    Papers" (pp020019), its inventory of photographs from Meet the Press television programs (LOT 13025), arranged by
    show date, each with its guests as the Library writes them ("Halleck, Charles A."). The pages for Aug. 1959–Jan.
    1966 (finding aid, pp. 50–74, as produced Aug. 23, 2026) are kept in sources/loc/, with the front matter. A show
    of which no photograph survives is not in it.
  - the listings: the Classic TV Archive's episode guide (ctva.biz), compiled from the TV listings, Jan. 1961–Aug. 25,
    1963. It fills a Sunday the inventory lacks, and where it names another person than the inventory, the row says
    so (`check`). Its misspellings (Sorenson, Norrstad) are not disagreements.
Face the Nation (CBS) and Issues and Answers (ABC): not yet; no list of either has been found that can be read here.

STYLE (rendered by tools/bib/daybook.py and tools/bib/lives.py):
 1. One row a program: date, show, network, guests (as the Library writes them, one a person; the listings' guest put
    in the same form where the listings alone give the program), src ('LOC' or 'listings'), lot (the inventory's
    call number), note (the Library's heading for a group: "Governors' Conference"), check (where the listings name
    another person: "Listings: Orville L. Freeman. Check.").
 2. A program on another day than Sunday (Jan. 5, 1962, a Friday) is kept, on its day.
"""
import datetime
import html
import os
import re
import subprocess
import sys
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PDF = os.path.join(ROOT, "sources", "loc", "spivak-visual-pp020019-pp50-74.pdf")
OUT = os.path.join(ROOT, "daybook", "sunday.yaml")
CTVA = "https://ctva.biz/US/TalkShow/MeetThePress_(1953-65)_NedBrooks.htm"
FROM, TO = "1961-01-01", "1966-01-10"
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
# the listings' guest, put as the Library writes names, where the listings alone give the program
LISTED = {"1962-05-27": ["Annis, Edward R."]}
# misreadings of the finding aid's text
FIX = {"Mark 0.": "Mark O.", "Bums, James MacGregor": "Burns, James MacGregor"}
# a guest the Library writes by title, put as Part III writes the person (a name in its own order has no comma)
AS_SERIES = {"Nhu, Mme. Ngo Dinh": "Trần Lệ Xuân"}


def inventory():
    t = subprocess.run(["pdftotext", "-layout", PDF, "-"], capture_output=True, text=True, check=True).stdout
    t = re.sub(r"\n\s*- Page \d+ -\s*\n", "\n", t)
    t = re.sub(r"\n\s*Visual Materials from the Lawrence E\. Spivak Papers\s*\n", "\n", t)
    out = {}
    pat = rf"((?:{MONTHS}) \d{{1,2}}, \d{{4}})\s*\n(.*?)(?=\n\s*(?:Box \d+\s+)?(?:{MONTHS}) \d{{1,2}}, \d{{4}}\s*\n|\Z)"
    for m in re.finditer(pat, t, re.S):
        d = datetime.datetime.strptime(m.group(1), "%B %d, %Y").date().isoformat()
        body = m.group(2)
        lot = re.search(r"LOT (13025-\d+)", body)
        g = re.search(r"Guests?:\s*(.*?)(?=\n\s*(?:Related Materials|Physical Description|Scope|Identifier)|\Z)", body, re.S)
        if not g:
            continue
        text = re.sub(r"\s+", " ", re.sub(r"\bBox \d+\b", "", g.group(1))).strip()
        for a, b in FIX.items():
            text = text.replace(a, b)
        guests, note = split(text)
        guests = [AS_SERIES.get(g, g) for g in guests]
        out[d] = {"guests": guests, "note": note, "lot": lot.group(1) if lot else None}
    return out


def split(text):
    """'Humphrey, Hubert H., and Morton, Thruston B.' -> (['Humphrey, Hubert H.', 'Morton, Thruston B.'], None);
    "Governors' Conference: Connally, John B., ..., and Smylie, Robert" -> ([...], "Governors' Conference"). The
    Library writes each name 'Surname, Given' and a suffix after it ('King, Martin Luther, Jr.')."""
    note = None
    m = re.match(r"^([^,]+?):\s+(.*)$", text)
    if m:
        note, text = m.group(1).strip(), m.group(2)
    toks = [x.strip() for x in re.split(r",\s*(?:and\s+)?|\s+and\s+(?=[A-Z][\w'’.\- ]*,)|;\s*", text) if x.strip()]
    toks = [re.sub(r"^and\s+", "", x) for x in toks]
    toks = [x for x in toks if not re.match(r"^(Sir|Dr\.|Rev\.|Gen\.)$", x)]   # a title after the given names
    names = []
    i = 0
    while i < len(toks):
        if i + 1 < len(toks):
            n = f"{toks[i]}, {toks[i + 1]}"
            i += 2
            if i < len(toks) and re.match(r"^(Jr\.|Sr\.|II|III|IV)$", toks[i]):
                n += f", {toks[i]}"
                i += 1
        else:
            n = toks[i]
            i += 1
        names.append(n)
    return names, note


def listings():
    try:
        req = urllib.request.Request(CTVA, headers={"User-Agent": "bib-daybook (https://impending2223.github.io/bib/)"})
        t = urllib.request.urlopen(req, timeout=60).read().decode("latin-1")
    except Exception as e:
        print(f"listings skipped: {e}", file=sys.stderr)
        return {}
    s = html.unescape(re.sub(r"<br[^>]*>|</p>|</tr>|</td>|</div>", "\n", t))
    s = re.sub(r"[ \t\xa0]+", " ", re.sub(r"<[^>]+>", "", s))
    out = {}
    blocks = re.split(r"\n\s*\[\d+\]\s*Meet the Press\s*\n", s)
    for b in blocks[1:]:
        m = re.match(r"\s*(\d{2}[A-Z][a-z]{2}\d{4})", b)
        g = re.search(r"Guests?\s*\n(.*?)(?=\n#|\Z)", b, re.S)
        if m and g:
            d = datetime.datetime.strptime(m.group(1), "%d%b%Y").date().isoformat()
            out[d] = re.sub(r"\s+", " ", g.group(1)).strip()
    return out


def letters(s):
    return re.sub(r"[^a-z]", "", s.lower())


def main():
    inv, lst = inventory(), listings()
    rows = []
    for d in sorted(set(inv) | set(lst)):
        if not (FROM <= d <= TO):
            continue
        r = {"date": d, "show": "Meet the Press", "network": "NBC"}
        if d in inv:
            r["guests"] = inv[d]["guests"]
            if inv[d]["note"]:
                r["note"] = inv[d]["note"]
            r["src"] = "LOC"
            if inv[d]["lot"]:
                r["lot"] = inv[d]["lot"]
            other = lst.get(d)
            if other:
                surs = [letters(g.split(",")[0]) for g in r["guests"]]
                if not any(x and x in letters(other) for x in surs):
                    r["check"] = f"Listings: {re.sub(r'[.]$', '', other.split(',')[0])}. Check."
        elif d in LISTED:
            r["guests"] = LISTED[d]
            r["src"] = "listings"
        else:
            continue
        rows.append(r)
    head = ("# Generated by tools/daybook/make_sunday.py (the Library of Congress's inventory of Meet the Press, with the\n"
            "# listings). Edit the script, not this file. One row a program: date, show, network, guests, src, lot, check.\n")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(head)
        yaml.safe_dump({"programs": rows}, f, allow_unicode=True, sort_keys=False, width=1000)
    print(f"{len(rows)} programs; {sum(1 for r in rows if r.get('check'))} with a Check", file=sys.stderr)


if __name__ == "__main__":
    main()
