"""The calendar's dated entries against the brief (CLAUDE.md, "The calendar"): ./bib audit-cal writes
notes/calendar-audit.md. A review list, not a check: it reports, and changes nothing.

  Names      persons in `c` with a Part III entry whom neither `Names:` nor a hidden `name:` tag gives (by surname; a
             surname shared by several Part III persons lists them all, and a word that is also a place or a thing is
             marked "?"). Not read as persons (Oct. 22, 2026, from the three audits' false hits): italic titles, a
             case's names, a law or round named for persons (Kerr-Mills, Kennedy Round), places and bodies (Cape
             Kennedy, West Virginia, Walter Reed, a County or University), "Gallup" as the poll; a word in AMBIG or a
             given name in GIVEN counts only with the person's given name, an initial or a title before it; a justice
             named in an opinion line-up is skipped wherever a Part III justice has the surname. A review list: a
             person named by a bare ambiguous surname ("Jackson" alone) can be missed
  Event      entries with neither a bibliography of their own (a work's card, [[w.…]]; a work in *italics*; or a list's
             Part II section)
             nor a `See [[id]]` back to an earlier entry
  Primary    entries whose note neither links nor names a primary record (statute, Federal Register,
             Congressional Record, Public Papers, a presidential library's file, FRUS, a case; a State's or a city's
             own record: its returns, register, manual, session laws, journals, ballot pamphlet, charter, minutes, a
             State court's report; any government site, .gov; the *Bulletin* and *Current Documents* by their
             cards; a government document on archive.org cited by page under its title; a table the build sets in
             the entry from its own sources, by its tag); and entries that name one without linking it
  Threads    each thread's statement in th.yaml, for review: the brief asks for one or two clipped sentences
             saying what the thread is, with its stations
"""
import os
import re
from collections import defaultdict

from . import store

OUT = os.path.join(store.ROOT, "notes", "calendar-audit.md")

PRIMARY_HOSTS = ("govinfo.gov", "eur-lex.europa.eu", "undocs.org", "docs.un.org", "documents.un.org", "presidency.ucsb.edu", "history.state.gov", "federalregister.gov", "archives.gov",
                 "congress.gov", "jfklibrary.org", "lbjlibrary", "eisenhowerlibrary.gov", "trumanlibrary", "loc.gov",
                 "justia.com", "law.cornell.edu", "senate.gov", "house.gov", "supremecourt.gov", "oyez.org",
                 "uscode.house.gov", "cia.gov", "nsarchive", "fraser.stlouisfed.org", "bls.gov", "voteview.com", "static.case.law", "federalreserve.gov", "clerk.house.gov", "nasa.gov",
                 "prde.upress.virginia.edu", "millercenter.org",
                 # the courts' and the movement's own documents, the States' digital libraries
                 "courtlistener.com", "crmvet.org", "okra.stanford.edu", "kinginstitute.stanford.edu", "dlg.usg.edu",
                 "archives.lib.state.ma.us", "mdh.contentdm.oclc.org", "snccdigital.org", "dlg.galileo.usg.edu",
                 # the States' election databases and libraries, Parliament, the World Court, handles to repositories
                 "digitalmaine.com", "civera.com", "api.parliament.uk", "hansard.parliament.uk", "library.unt.edu",
                 "aarclibrary.org", "nga.org", "icj-cij.org", "hdl.handle.net")
PRIMARY_NAMES = re.compile(r"\bStat\.|Fed\. Reg\.|Cong\. Rec\.|\bFRUS\b|Public Papers|\bAPP\b|\d+ U\.S\. \d+|"
                           r"Op\. Att'y Gen\.|Op\. O\.L\.C\.|"   # the Attorney General's and OLC's opinions (opinions.py)
                           r"Exec\. Order|Executive Order|Proclamation|Pub\. L\.|H\.R\. \d|S\. \d|Reorganization Plan|"
                           r"\bNSAM\b|Weekly Compilation|Department of State Bulletin|Election Statistics|Statistics of the Congressional|\(PRDE(?: only)?\)|\(Miller Center\)|"
                           # the States' and the cities' own records: returns, registers and manuals, session laws,
                           # journals, ballot pamphlets, charters, minutes; State and lower federal courts' reports
                           r"Official (?:Vote|Returns|Canvass|Report|and Statistical)|Canvass|Abstract of (?:the )?(?:Votes?|Returns)|"
                           r"Statement of (?:the )?Vote|Official Record|Journal of Proceedings|\bHearings?\b|Official (?:Abstract|Report)|Result of Votes|Tabulation of Official Vote|Results of the (?:Primary|General) Election|Report of the President's Commission|S\. Rep\. No\.|H\.R\. Rep\. No\.|Statistical Register|Election Returns|Blue Book|Legislative Manual|"
                           r"\bManual\b|Red Book|Political History of Nevada|(?:Acts|Laws|Session Laws|Statutes) of |"
                           r"\b(?:House|Senate) Journal|Journal of the (?:House|Senate)|Ballot (?:Pamphlet|Proposition)|"
                           r"\bProposition \d|State Question|Charter|Minutes|Ordinance|"
                           r"\bL\. \d{4}, c\. \d|\bLaws \d{4}\b|Sess\. Laws|\b[A-Z][a-z]{1,4}\. Acts\b|\bStats\. \d{4}|\bDirective\b|"
                           r"\d+ (?:So\.(?: 2d)?|S\.W\.(?:2d)?|S\.E\.(?:2d)?|N\.E\.(?:2d)?|N\.W\.(?:2d)?|A\.(?:2d)?|P\.(?:2d)?|"
                           r"F\. ?Supp\.|F\.(?:2d)?|Cal\.(?: ?2d)?|N\.Y\.(?: ?2d)?|Misc\.(?: 2d)?|A\.D\.(?: ?2d)?|Ill\.(?: ?2d)?|"
                           r"Mich\.|Ohio St\.(?: ?2d)?|Wash\.(?: ?2d)?|Ga\.|Ala\.|Miss\.|La\.|Tex\.|Okla\.) \d+")
GOVDOC = re.compile(r"Manual|Statistics|Journal|Laws|Acts|Yearbook|Report|Bulletin|Register|Returns|Canvass|Abstract|"
                    r"Hearings?|Proceedings|Digest|Record|Systems Analysis|Statistical|Minerals|Census|Session")
TABLE_TAGS = {"primary", "primaries", "election", "governors", "special", "legislatures", "statefin", "budget", "bill",
              "appropriations", "debt-limits", "oilworld", "oilprice", "conventions", "rollcall", "congress",
              "committees", "executive", "wardead"}
LISTREF = re.compile(r"\b(?:K–J Adm\.|K–J Cong\.|Opp\.|1968|Adm\.|Cong\.|Wg\.|Viet\.)\s+II\b")
# words that are surnames in Part III but also places or things; a hit on one is marked "?"
AMBIG = {"Temple", "Alcorn", "Armstrong", "Kelly", "White", "Black", "Brown", "Green", "Long", "King", "Young", "Little", "Rich", "Washington", "Jackson",
         "Lincoln", "Houston", "Marshall", "Ford", "Hall", "Rock", "Church", "Bell", "Price", "Day", "May", "March",
         "Rivers", "Moss", "Wood", "Woods", "Lodge", "Byrd", "Gates", "Bowles", "Love", "Hope", "Christian", "Banks",
         "Stone", "Field", "Fields", "Hand", "Pierce", "Monroe", "Madison", "Rogers", "Hill", "Mills", "Barnes",
         "English", "Burns", "Rose", "Cotton", "Ball", "Bridges", "Grant", "Chase", "Cooper", "Carpenter", "Baker",
         "Clark", "Jack", "Franklin", "Hill", "Lake", "Gary", "Mason", "Day", "Love", "Hall", "Moore", "Cox",
         "West", "Jordan", "Andrews", "Camp", "Kaiser", "Shell", "Nation", "Means", "High", "Fort", "Gallup", "Home",
         "Taylor", "Kerner", "Hopkins", "Reed", "Round", "Lord", "Morton", "Edwards", "Maddox", "Hannah", "Flemming"}


PRESIDENTS = {"Eisenhower", "Kennedy", "Johnson"}

# what is not a person, struck from `c` before the names are read (the audits of Oct. 22, 2026 listed the false hits):
# italic titles (a case, a book, a ship), a case's names, a law or a round named for persons, places and bodies
NOT_PERSONS = re.compile(
    r"\*[^*]+\*|\b[A-Z][\w.'’-]*(?: [A-Z][\w.'’-]*)* v\. [A-Z][\w.'’-]*(?: [A-Z][\w.'’-]*)*|"
    r"\b[A-Z]\w+[-–][A-Z]\w+\b|"
    r"\b[A-Z]\w+ (?:Round|Commission|Law|Act|Amendment|Bill|Doctrine|Report|Plan|Award|Prize|Foundation|University|"
    r"College|County|Island|Islands|Tunnel|Hall|Hill|Lake|Dam|Field|Air Force Base|Memorial|Center|Library|Hospital)\b|"
    r"\b(?:Cape|Fort|Camp|Lake|Mount|Port|Key|Rock|Lord|Sir|King|Queen|Prince|Princess|Shah|Emir|Sheikh|Operation|Commando) [A-Z]\w+|"
    r"\bWest (?:Virginia|Berlin|Point|Germany|Bank|Coast|Indies|Africa|Side)\b|\b(?:Walter Reed|Johns Hopkins|"
    r"Black Power|Black Panthers?|Winston-Salem|Ocean Hill|Gallup(?= poll|,| Poll|:))\b")
# words a surname shares with a given name or a common word: a hit on one counts only where it reads as the person
# (his given name or initial, or a title, just before it); a given name followed by a capitalized word is a given name
TITLES = re.compile(r"(?:Senator|Sen\.|Representative|Rep\.|Governor|Gov\.|Mayor|Judge|Justice|Secretary|"
                    r"General|Gen\.|Admiral|Adm\.|Ambassador|President|Speaker|Dr\.|Mr\.|Mrs\.|Miss|"
                    r"Reverend|Rev\.|Father|Bishop|Cardinal|Director|Chairman|Senators|Representatives)\s+$")
GIVEN = {"Henry", "James", "Walter", "Lawrence", "Franklin", "Allen", "Douglas", "Jack", "Hayes", "Collins", "Keith",
         "Marshall", "Gilbert", "Albert", "Alexander", "Howard", "Curtis", "Russell", "Wesley", "Harvey", "Carley",
         "Clyde", "Terry", "Gordon", "Lee", "Percy", "Clay", "Burke", "Edward", "Moore", "Thomas", "Ellis",
         "Foote"}


def as_person(sur, text, persons):
    """True where some mention of `sur` in `text` reads as a person: not a given name before another name, and, for
    a word that is also a place or a thing (AMBIG), with his given name or initial, or a title, before it."""
    givens = set()
    for n, _ in persons or []:
        g = n.split(",", 1)[1].strip() if "," in n else ""
        if g:
            givens.add(g.split()[0].strip("."))
    for m in re.finditer(r"\b" + re.escape(sur) + r"\b", text):
        after = text[m.end():m.end() + 30]
        before = text[max(0, m.start() - 40):m.start()]
        if sur in GIVEN and re.match(r" (?:[A-Z]\. )*[A-Z][a-z]", after):
            continue                                # Percy Sutton, Clay Shaw, Gilbert R. Mason: a given name
        if sur not in AMBIG and sur not in GIVEN:
            return True
        if TITLES.search(before) or any(re.search(r"\b" + re.escape(g) + r"\.?\s+(?:[A-Z]\.\s+)*$", before)
                                        for g in givens):
            return True
    return False


OPINION = re.compile(r"\b(?:opinion|dissent\w*|concurr\w*|for the (?:Court|court|majority)|joined|writing|"
                     r"per curiam|holds?|rules?)\b")


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
        c_plain = NOT_PERSONS.sub(" ", c_plain)
        missing = []
        tagged = {str(t)[5:] for t in e.get("tags") or [] if str(t).startswith("name:")}
        for sur in dict.fromkeys(sur_rx.findall(c_plain)):
            slug = re.sub(r"[^a-z0-9]+", "-", sur.lower()).strip("-") + "-"
            if sur in given or any(k.startswith(slug) for k in tagged):
                continue
            if not as_person(sur, c_plain, p3[sur]):
                continue
            # a judge named only for an opinion he wrote or joined goes unnamed (the owner's ruling, Oct. 14, 2026)
            if p3[sur] and any("III.G" in w for _, w in p3[sur]) and OPINION.search(c):
                continue
            per = defaultdict(list)          # each person once, with all his sections
            for n_, where in p3[sur]:
                if where not in per[n_]:
                    per[n_].append(where)
            who = "; ".join(f"{n_} ({', '.join(ws)})" for n_, ws in per.items())
            missing.append((sur, ("? " if sur in AMBIG else "") + f"{sur}: {who}"))
        if missing:
            names.append((sec, e, missing))
        own = bool(re.search(r"\*[^*]+\*|\[\[w\.", n) or LISTREF.search(n))
        see = "See [[" in n or "Bibliography: [[" in n or re.search(r"see \[\[", n)
        if not own and not see:
            event.append((sec, e))
        # a record may be linked in either field; a link counts by its host, or by its text naming a record (a
        # State Bulletin or a State's returns on archive.org)
        links = re.findall(r"\[((?:[^\[\]]|\[[^\]]*\])*)\]\((https?://[^)]+)\)", c + " " + n)
        linked = any(any(h in u for h in PRIMARY_HOSTS) or re.search(r"^https?://[^/]*\.(?:gov|us)(?:/|$)", u)
                     or PRIMARY_NAMES.search(txt) for txt, u in links)
        # a poll's record is its release, which *The Gallup Poll* prints by page ([[w.gallup-poll]], III, 1868)
        linked = linked or bool(re.search(r"\[\[w\.gallup-poll\]\],? [IVX]+, \d", n))
        # the Bulletin and Current Documents (government publications, cited by their cards), a government document on
        # archive.org cited by its page under its title, and a table the build sets in the entry from its sources
        linked = linked or bool(re.search(r"\[\[w\.(?:department-of-state-bulletin|current-documents-\d{4}|"
                                          r"report-of-the-national)\]\]", n))
        cn = c + " " + n
        linked = linked or any("archive.org" in u and re.fullmatch(r"[\d–, ]+(?:n\.\d+)?", txt.strip())
                               and GOVDOC.search(cn[:cn.find(u)][-160:]) for txt, u in links)
        linked = linked or any(str(t).split(":")[0] in TABLE_TAGS for t in e.get("tags") or [])
        named = PRIMARY_NAMES.search(n)
        if not linked and not named:
            prim_none.append((sec, e))
        elif named and not linked:
            prim_unlinked.append((sec, e, named.group(0)))
    threads = [(e["id"].split(".", 2)[2], e.get("s"), " ".join(store.as_list(e.get("c"))))
               for e in cal.threads().values() if not e.get("see")]
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
           f"| A person in `c` with a Part III entry in neither `Names:` nor a `name:` tag | {len(names)} |",
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
