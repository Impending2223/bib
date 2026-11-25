"""Substance left in the note: what an entry's citations hold that its line does not (the owner, Nov. 21, 2026, of a
National Day entry whose cites named the leaders present while its text named one: "Shouldn't this material go out of
the citation block and into the entry, and the name tags?"; Nov. 22: a comprehensive pass for substance left in the
notes; the reader's brief, R33a).

    ./bib check                                  one warning line: the count [note-substance]
    python3 -I tools/notes/substance.py [--strong]   the entries, strongest first (tab-separated: score, id, what)

STYLE
 1. The test reads each parenthetical of the note's sources (the works read and the records; not "To check:", "See",
    "Names:", "Check:", "Made public:") and looks for three things the line (`c`) lacks:
      persons    a person the calendar tags somewhere (a `name:` tag), by his full name in either order ("Chen
                 Yi", "Dean Rusk"), or by a surname of six letters or more that is no common word, not in the line;
      words      a quotation of three words or more, not in the line; a title in quotation marks ("Kennedy's
                 Reply to Truman," the comma inside) is no quotation;
      figures    a number in thousands, or a number with its unit (percent, million, tons, votes, troops, a dollar
                 sign), not in the line; a year, a day of the month, a page and a document number are no figure.
 2. The score: a point a person (three at most), two for a quotation, a point a figure (two at most). An entry
    scores where it has any; "strong" is three points or more.
 3. A parenthetical that is the source's alone is not substance of the entry: a variant ("gives Oct. 20"; R41), a
    pinpoint's label of a word or two ("the vote", "the text"), a date. The test cannot tell every case: it is a
    warning and a reading list, never an error. `ok:note-substance` on an entry a reader has read and left.
"""
import collections
import re

from . import claims

QUOTE = re.compile(r"[\"“]([^\"“”]{12,})[\"”]")
MONTH = r"(?:Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)[a-z]*\.?"
FIG = re.compile(r"\$\s?\d[\d,.]*|\b\d[\d,.]*\s?(?:percent|per cent|million|billion|thousand|tons?|tonnes?|jin|mu|votes?|"
                 r"troops|men|dead|killed|wounded|delegates|members|divisions|aircraft|sorties)\b|\b\d{1,3}(?:,\d{3})+\b")
COMMON = {"Washington", "Lawrence", "Morris", "Church", "Bishop", "Marshall", "Mansfield", "Russell", "Martin", "Thomas",
          "George", "Robert", "Walter", "Arthur", "Stanley", "Douglas", "Gordon", "Howard", "Wilson", "Jackson",
          "Lincoln", "Jordan", "Israel", "Monday", "Friday", "Sunday", "August", "Central", "Senate", "Justice",
          "Hunter", "Parker", "Porter", "Carter", "Taylor", "Turner", "Walker", "Butler", "Cooper", "Fisher", "Mason",
          "Miller", "Baker", "Foster", "Gardner", "Chapman", "Bridges", "Rivers", "Rhodes", "Fields", "Brooks"}
NOT_FIG = re.compile(rf"{MONTH} \d{{1,2}}|\b(?:19|20)\d\d\b|\b(?:doc|docs|no|nos|p|pp|n|nn|at|vol|box|file|folder|tape|"
                     r"conversation|reel|item)\.? ?\d[\d–-]*|\d+ (?:Stat|U\.S|F\.\d?d?|Cong\. Rec)\b|\d+:\d\d")
VARIANT = re.compile(r"\b(?:gives|dates it|has it|puts it|reads|prints|misdates|not the|so printed|sic)\b")
_PARENS = re.compile(r"\(([^()]*(?:\([^()]*\)[^()]*)*)\)")


def surnames(series):
    """(full names, surnames) from the calendar's `name:` tags: each key's two first words in both orders ("Chen Yi",
    "Yi Chen"; "Rusk Dean", "Dean Rusk"), and its first word where six letters or more and no common word."""
    if getattr(series, "_notesub_names", None) is None:
        full, sur = set(), set()
        for _, e in claims.calendar(series):
            for t in e.get("tags") or []:
                if str(t).startswith("name:"):
                    w = [x.capitalize() for x in str(t)[5:].split("-") if x]
                    if len(w) >= 2:
                        full.add(f"{w[0]} {w[1]}")
                        full.add(f"{w[1]} {w[0]}")
                    if w and len(w[0]) >= 6 and w[0] not in COMMON:
                        sur.add(w[0])
        series._notesub_names = (full, sur)
    return series._notesub_names


def found(series, e):
    """(score, [what]) for an entry (STYLE 1, 2)."""
    c, n = e.get("c"), e.get("n")
    if not isinstance(c, str) or not isinstance(n, str) or "(" not in n or "ok:note-substance" in (e.get("tags") or []):
        return 0, []
    full, sur = surnames(series)
    cl = c.lower()
    persons, words, figures = [], [], []
    for item in claims.note_parts(n)[0]:
        for m in _PARENS.finditer(item):
            p = m.group(1)
            if len(p.split()) < 3 or VARIANT.search(p):
                continue
            for q in QUOTE.findall(p):
                if len(q.split()) >= 3 and not q.rstrip().endswith(",") and q.lower().strip(" .,;") not in cl:
                    words.append(q[:40])
            bare = QUOTE.sub(" ", p)
            caps = re.findall(r"\b[A-Z][a-z]+\b", bare)
            for w in [f"{a} {b}" for a, b in zip(caps, caps[1:]) if f"{a} {b}" in full and f"{a} {b}" in bare] + \
                     [w for w in caps if w in sur]:
                last = w.split()[-1] if w in full and w.split()[-1] in sur else w.split()[0] if " " in w else w
                if not any(x in c for x in (w, " ".join(reversed(w.split())))) and (w not in sur or not re.search(rf"\b{w}\b", c)) \
                        and w not in persons and last not in " ".join(persons):
                    persons.append(w)
            for f in FIG.findall(NOT_FIG.sub(" ", bare)):
                digits = re.sub(r"\D", "", f)
                if digits and digits not in re.sub(r"[^\d ]", "", c).split() and f.strip() not in c and f not in figures:
                    figures.append(f.strip())
    score = min(len(persons), 3) + (2 if words else 0) + min(len(figures), 2)
    what = ([f"persons: {', '.join(persons[:6])}"] if persons else []) + ([f"words: {words[0]}"] if words else []) + \
           ([f"figures: {', '.join(figures[:4])}"] if figures else [])
    return score, what


def survey(series):
    """[(score, id, what)], strongest first."""
    out = []
    for _, e in claims.calendar(series):
        score, what = found(series, e)
        if score:
            out.append((score, e["id"], "; ".join(what)))
    return sorted(out, key=lambda r: (-r[0], r[1]))


def problems(series):
    """One warning for `check`: the counts."""
    rows = survey(series)
    if not rows:
        return []
    strong = sum(1 for r in rows if r[0] >= 3)
    return [("lists/cal/", f"{len(rows)} entries whose citations hold persons, words or figures the line lacks, "
                           f"{strong} of them strongly (python3 -I tools/notes/substance.py lists them; the reader's brief, R33a)")]

