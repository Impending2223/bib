"""The calendar's dated entries against the brief (CLAUDE.md, "The calendar"): ./bib audit-cal writes
notes/calendar-audit.md. A review list, not a check: it reports, and changes nothing.

  Names      persons in `c` with a Part III entry whom `Names:` leaves out (by surname; a surname shared by
             several Part III persons lists them all, and a word that is also a place or a thing is marked "?")
  Event      entries with neither a bibliography of their own (a work in *italics*, or a list's Part II section)
             nor a `See [[id]]` back to an earlier entry
  Primary    entries whose note neither links nor names a primary record (statute, Federal Register,
             Congressional Record, Public Papers, a presidential library's file, FRUS, a case); and entries that
             name one without linking it
  Threads    each thread's statement in th.yaml, for review: the brief asks for one or two clipped sentences
             saying what the thread is, with its stations
"""
import os
import re
from collections import defaultdict

from . import store

OUT = os.path.join(store.ROOT, "notes", "calendar-audit.md")

PRIMARY_HOSTS = ("govinfo.gov", "presidency.ucsb.edu", "history.state.gov", "federalregister.gov", "archives.gov",
                 "congress.gov", "jfklibrary.org", "lbjlibrary", "eisenhowerlibrary.gov", "trumanlibrary", "loc.gov",
                 "justia.com", "law.cornell.edu", "senate.gov", "house.gov", "supremecourt.gov", "oyez.org",
                 "uscode.house.gov", "cia.gov", "nsarchive", "fraser.stlouisfed.org", "bls.gov", "voteview.com")
PRIMARY_NAMES = re.compile(r"\bStat\.|Fed\. Reg\.|Cong\. Rec\.|\bFRUS\b|Public Papers|\bAPP\b|\d+ U\.S\. \d+|"
                           r"Exec\. Order|Executive Order|Proclamation|Pub\. L\.|H\.R\. \d|S\. \d|Reorganization Plan|"
                           r"\bNSAM\b|Weekly Compilation")
LISTREF = re.compile(r"\b(?:K–J Adm\.|K–J Cong\.|Opp\.|1968|Adm\.|Cong\.|Wg\.|Viet\.)\s+II\b")
# words that are surnames in Part III but also places or things; a hit on one is marked "?"
AMBIG = {"White", "Black", "Brown", "Green", "Long", "King", "Young", "Little", "Rich", "Washington", "Jackson",
         "Lincoln", "Houston", "Marshall", "Ford", "Hall", "Rock", "Church", "Bell", "Price", "Day", "May", "March",
         "Rivers", "Moss", "Wood", "Woods", "Lodge", "Byrd", "Gates", "Bowles", "Love", "Hope", "Christian", "Banks",
         "Stone", "Field", "Fields", "Hand", "Pierce", "Monroe", "Madison", "Rogers", "Hill", "Mills", "Barnes",
         "English", "Burns", "Rose", "Cotton", "Ball", "Bridges", "Grant", "Chase", "Cooper", "Carpenter", "Baker"}


PRESIDENTS = {"Eisenhower", "Kennedy", "Johnson"}


def part3(series):
    """{surname: [(name as written, 'List III.X')]} from every list's Part III."""
    out = defaultdict(list)
    for lst in series.lists.values():
        for sec, e in lst.entries():
            if (sec.code or "").startswith("III") and e.get("s"):
                for n in re.split(r";\s*", e["s"]):
                    n = re.sub(r"\s*\(.*?\)\s*$", "", n).strip()
                    if "," not in n:
                        continue
                    sur = n.split(",")[0].strip()
                    out[sur].append((n, f"{lst.abbr} {sec.code}"))
    return out


def run(series):
    cal = series.lists["cal"]
    p3 = part3(series)
    sur_rx = re.compile(r"\b(" + "|".join(sorted((re.escape(s) for s in p3), key=len, reverse=True)) + r")\b")
    rows = []
    for sec, e in cal.entries():
        if not e.get("date"):
            continue
        rows.append((sec, e))
    names, event, prim_none, prim_unlinked = [], [], [], []
    for sec, e in rows:
        c = " ".join(store.as_list(e.get("c")))
        n = str(e.get("n") or "")
        given = n.split("Names:", 1)[1] if "Names:" in n else ""
        c_plain = re.sub(r"White House|Brown v\.|Little Rock|Ford Foundation|Lincoln Memorial|Washington, D\.C\.", "", c)
        missing = []
        for sur in dict.fromkeys(sur_rx.findall(c_plain)):
            if sur in given:
                continue
            per = defaultdict(list)          # each person once, with all his sections
            for n_, where in p3[sur]:
                if where not in per[n_]:
                    per[n_].append(where)
            who = "; ".join(f"{n_} ({', '.join(ws)})" for n_, ws in per.items())
            missing.append((sur, ("? " if sur in AMBIG else "") + f"{sur}: {who}"))
        if missing:
            names.append((sec, e, missing))
        own = bool(re.search(r"\*[^*]+\*", n) or LISTREF.search(n))
        see = "See [[" in n or re.search(r"see \[\[", n)
        if not own and not see:
            event.append((sec, e))
        links = re.findall(r"\]\((https?://[^)]+)\)", c + " " + n)    # a record may be linked in either field
        linked = any(any(h in u for h in PRIMARY_HOSTS) for u in links)
        named = PRIMARY_NAMES.search(n)
        if not linked and not named:
            prim_none.append((sec, e))
        elif named and not linked:
            prim_unlinked.append((sec, e, named.group(0)))
    threads = [(e["id"].split(".", 2)[2], e.get("s"), " ".join(store.as_list(e.get("c"))))
               for e in cal.threads().values()]
    return rows, names, event, prim_none, prim_unlinked, threads


def report(series):
    rows, names, event, prim_none, prim_unlinked, threads = run(series)
    total = len(rows)
    line = lambda sec, e: f"- `{e['id']}` ({e.get('when')}, {sec.code} {sec.file}): " + \
        re.sub(r"\s+", " ", " ".join(store.as_list(e.get("c"))))[:110]
    out = ["# The calendar against the brief", "",
           "Written by `./bib audit-cal` (`tools/bib/calaudit.py`): the dated entries checked against the brief in",
           "CLAUDE.md (\"The calendar\"). A review list: a hit is a place to look, not an error. Rerun after editing.", "",
           f"{total} dated entries.", "",
           "| Check | Entries |", "|---|---|",
           f"| A person in `c` with a Part III entry missing from `Names:` | {len(names)} |",
           f"| (of which only a President's surname: Eisenhower, Kennedy, Johnson) | "
           f"{sum(1 for _, _, m in names if {s for s, _ in m} <= PRESIDENTS)} |",
           f"| Neither a bibliography of its own nor a `See [[id]]` back | {len(event)} |",
           f"| No primary record linked or named | {len(prim_none)} |",
           f"| A primary record named but not linked | {len(prim_unlinked)} |",
           f"| Threads (statements listed for review) | {len(threads)} |", "",
           "## Names", "",
           "Each person found in `c` by a surname that has a Part III entry, and the entries of that surname (one is",
           "the person; several mean the surname is shared). \"?\" marks a surname that is also a place or a thing",
           "(White, Byrd, Lodge as a word): look before adding.", ""]
    for sec, e, miss in names:
        out.append(line(sec, e))
        out += [f"  - {m}" for _, m in miss]
    out += ["", "## Event", "", "No work of its own and no `See [[id]]` back to the event's first entry.", ""]
    out += [line(sec, e) for sec, e in event]
    out += ["", "## Primary record", "", "### None linked or named", "",
            "Some events have none (a speech outside the Public Papers, a march, a strike); the rest want the statute,",
            "the order, the APP document, the FRUS document, the case.", ""]
    out += [line(sec, e) for sec, e in prim_none]
    out += ["", "### Named, not linked", ""]
    out += [line(sec, e) + f" — names \"{w}\"" for sec, e, w in prim_unlinked]
    out += ["", "## Threads", "", "The brief: what the thread is, and its stations, in one or two clipped sentences.", "",
            "| Thread | Statement |", "|---|---|"]
    out += [f"| {s} | {c.replace('|', '/')} |" for _, s, c in sorted(threads, key=lambda x: x[1] or "")]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
    return OUT, total, len(names), len(event), len(prim_none), len(prim_unlinked), len(threads)
