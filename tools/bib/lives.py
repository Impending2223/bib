"""Lives: a name entry for each person, gathered from the series' own files. build/lives.html.

Each entry: the name as Part III writes it, the Directory's description, the pointers into the series, then
  Life                 running text, in order of date: each fact with the date in it and its pincite, linked
                       to the ground source; the series' own pages as pointers beside it (sans serif, not underlined)
                         the Biographical Directory (BD, the 2005 printed edition, by page), one fact a clause;
                         offices held, with their ex officio offices after them (the holder's sources; the
                         Executive Roster as a pointer); seats (BD; the Congress rosters as pointers); elections
                         (the Clerk's Statistics, by page; the election's block as a pointer); the calendar
  Publications         the person's own works in the series and in the Directory's bibliography
  FRUS documents sent  by the daybook's rules for authors
  Primary sources      oral histories, papers, speeches and recordings in the series
  Secondary sources    works on the person: the series' entries, the Directory's bibliography, works citing the name
  Named                FRUS documents that name the person, by volume; presidential documents (APP: the Public
                       Papers and the campaign documents), one a line, by year

STYLE:
 1. Telegraphic: the Directory's clauses as printed, the first letter raised; nicknames and honors of color cut.
 2. Each fact cites its ground source, linked; the series' pages are pointers, not sources. A run of facts from
    the same page of the same source cites it once, at the end of the run.
 3. A fact the Directory and our structured files both give shows once, with both cites.
 4. Abbreviations: BD, CDir., CR, FR, DSB, GOM, APP; FRUS by subseries, volume and doc.; Clerk, Election
    Statistics, by year and page; pointers: Exec. (the roster at a term), Cong. (a Congress at its opening),
    Election, Cal.
 6. Each run of sentences sharing their sources and pointers is a sentence block; its source block follows it,
    the cites first, then the pointers.
 5. FRUS headings with 'from' in lower case; works from the Directory's bibliography in the series' form.
"""
import datetime
import functools
import json
import sys
import os
import re

from . import store
from .markup import to_html, plain, lower_from

fold = functools.lru_cache(maxsize=None)(store.fold)     # the same names are folded many thousand times

SITE = ""   # a base url for the links to the other pages ('' on the site itself)
MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
FULL = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                     "September", "October", "November", "December"], 1)}
BD_URL = "https://www.govinfo.gov/content/pkg/GPO-CDOC-108hdoc222/pdf/GPO-CDOC-108hdoc222-4-{part}.pdf#page={pdf}"
BD_CITE = ("*Biographical Directory of the United States Congress, 1774–2005*, H. Doc. 108-222 (Government "
           "Printing Office, 2005)")
HSG = "https://history.state.gov/historicaldocuments/"
# The Presidents' terms: a President's own papers in his term are listed without his name
PRESIDENTS = [("Dwight D. Eisenhower", "1953-01-20", "1961-01-20"), ("John F. Kennedy", "1961-01-20", "1963-11-22"),
              ("Lyndon B. Johnson", "1963-11-22", "1969-01-20"), ("Richard Nixon", "1969-01-20", "1974-08-09"),
              ("Gerald R. Ford", "1974-08-09", "1977-01-20")]
INITIALS = {"Dwight D. Eisenhower": "DDE", "John F. Kennedy": "JFK", "Lyndon B. Johnson": "LBJ", "Richard Nixon": "RN",
            "Gerald R. Ford": "GRF"}
# Clauses of the Directory left out: color, not record
CUT = re.compile(r"^(known (in|as)|called |nicknamed )", re.I)


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def a(url, text):
    return f'<a href="{esc(url)}">{text}</a>'


def ptr(url, text):
    """A pointer into the series: not a source."""
    return f'<a class="lvp" href="{esc(url)}">{text}</a>'


def fmt(d):
    d = str(d)
    if len(d) == 10:
        return f"{MONTHS[int(d[5:7]) - 1]} {int(d[8:])}, {d[:4]}"
    if len(d) == 7:
        return f"{MONTHS[int(d[5:7]) - 1]} {d[:4]}"
    return d


def key_of(name):
    """'Byrd, Harry F., Jr.' -> 'byrd-harry-f-jr': the anchor, and the key of the person's FRUS and APP lists."""
    return re.sub(r"[^a-z]+", "-", fold(re.sub(r"\s*\([^)]*\)", "", name)).lower()).strip("-")


def split_name(name):
    bare = re.sub(r"\s*\([^)]*\)", "", name)
    p = [x.strip() for x in bare.split(",")]
    return p[0], (p[1] if len(p) > 1 else "")


SUFFIX = {"jr", "sr", "ii", "iii", "iv"}


def gtoks(g):
    """'Hubert H., Jr.' -> ['hubert', 'h']; 'George H.W.' -> ['george', 'h', 'w']; a name in parentheses dropped."""
    g = re.sub(r"\([^)]*\)", " ", g)
    return [t for t in re.split(r"[\s.,]+", fold(g)) if t and t not in SUFFIX]


def suffix(name):
    """'Vinson, Fred M., Jr.' -> 'Jr'; 'McCain, John S., III' -> 'III'; '' if none."""
    m = re.search(r",\s*(Jr|Sr|II|III|IV)\b\.?(?=\s*(\(|$))", name)
    return m.group(1) if m else ""


def nick(a, b):
    """Bill and William, Ted and Edward: the short forms the Congress rosters use."""
    from .congress import SHORT
    return b in SHORT.get(a, ()) or a in SHORT.get(b, ())


def same_person(sur, given, other_sur, other_given):
    """The surnames agree; the first given names agree, by initial, or as a short form; and where both give a second
    given name or initial, those agree."""
    if fold(sur) != fold(other_sur):
        return False
    A, B = gtoks(given), gtoks(other_given)
    if not A or not B:
        return False
    a, b = A[0], B[0]
    if not (a == b or (len(a) == 1 and b.startswith(a)) or (len(b) == 1 and a.startswith(b)) or nick(a, b)):
        return False
    # each further initial the one gives is among the other's further names, in order ('Thomas L.' and 'Thomas
    # William Ludlow'; not 'William O.' and 'William P.')
    # 'J. Skelly' goes by Skelly: the other gives Skelly too ('James Skelly'; not 'Jim')
    for X, Y in ((A, B), (B, A)):
        if len(X[0]) == 1 and len(X) > 1 and len(X[1]) > 1 and X[1] not in Y[:2]:
            return False
    short, long_ = (A, B) if len(A) <= len(B) else (B, A)
    rest = iter(t[0] for t in long_[1:])
    return all(t[0] in rest for t in short[1:])


# ---------------------------------------------------------------- sentences

def sent(key, text, ext=(), intl=(), para=False, kind="", dates=()):
    return {"key": str(key), "text": text, "ext": list(ext), "int": list(intl), "para": para, "kind": kind,
            "dates": set(dates)}


DATE_RE = re.compile(r"(January|February|March|April|May|June|July|August|September|October|November|December) "
                     r"(\d{1,2}), (\d{4})")


def iso_dates(t):
    return [f"{y}-{FULL[m]:02d}-{int(d):02d}" for m, d, y in DATE_RE.findall(t)]


_CACHE = {}


def cached(key, make):
    if key not in _CACHE:
        _CACHE[key] = make()
    return _CACHE[key]


def letter_json(folder, letter):
    def make():
        p = os.path.join(store.ROOT, "sources", folder, letter + ".json")
        return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else ([] if folder == "bd" else {})
    return cached((folder, letter), make)


STOP = {"united", "states", "department", "office", "assistant", "deputy", "special", "general", "director", "chief",
        "member", "chairman", "president", "secretary", "under", "national", "council", "commission", "board", "affairs",
        "administration", "service", "executive", "with", "from", "after", "before", "until", "acting"}


def bd_entry(sur, given, member=True, words=(), sfx=""):
    """The Directory's entry for the person. The member lived into the period (the entry's latest year 1953 or
    later), so a namesake of the last century is not taken. A member of Congress at an opening may match by a
    middle name he went by ('Thad Cochran', 'William Thad'); anyone else only where the entry also names one of
    his offices (a word of its title: 'Ambassador to India')."""
    best = None
    for e in letter_json("bd", fold(sur)[:1].upper()):
        m = re.match(r"([^,(]+), ([^(]+?)(?:,? \(|$)", e["name"]) or re.match(r"([^,]+), (.+)", e["name"])
        if not m or fold(m.group(1)) != fold(sur):
            continue
        yrs = [int(y) for y in re.findall(r"\b(1[789]\d\d|20\d\d)\b", e["text"])]
        if not yrs or max(yrs) < 1953:
            continue
        g = m.group(2)
        # the suffix agrees: Fred M. Vinson, Jr., is not his father; Adm. John S. McCain, Jr., not the Senator, III
        head = re.sub(r"\([^)]*\)|\[[^]]*\]", "", re.split(r", (?:an?|the) [A-Z]", e["text"], 1)[0])
        sm = re.search(r"\b(Jr|Sr|II|III|IV)\b", head.split(",", 1)[-1])
        if sfx not in ("", "Sr") and (sm.group(1) if sm else "") != sfx:
            continue
        ok = same_person(sur, given, sur, g)
        if ok and not member:
            # anyone else gives his initials in full in the Directory ('William P.' is not 'Will')
            ok = len(gtoks(g)) >= len(gtoks(given)) and not nick(gtoks(given)[0], gtoks(g)[0])
        if not ok and member:
            A, B = gtoks(given), gtoks(g)
            ok = len(A) == 1 and any(A[0] == b or nick(A[0], b) for b in B[1:])
        if ok and not member:
            ok = bool(set(words) & set(re.findall(r"[a-z]{4,}", fold(e["text"]))))
        if ok:
            return e
    return best


def holders_of(sur):
    """[(unit, office, holder)] in the Executive roster with the surname."""
    from . import executive as X

    def make():
        idx = {}
        for u in X.load().values():
            for o in u.get("offices") or []:
                for h in o.get("holders") or []:
                    idx.setdefault(fold(split_name(h["name"])[0]), []).append((u, o, h))
        return idx
    return cached("holders", make).get(fold(sur), [])


def person_words(sur, given, names=None):
    """The distinctive words of the person's offices in the roster, for matching the Directory."""
    from . import executive as X
    hs = [(o, h) for u, o, h in holders_of(sur)
          if (h["name"] in names if names else same_person(*split_name(h["name"]), sur, given))]
    w = set()
    for o, h in hs:
        w |= set(re.findall(r"[a-z]{4,}", fold(f"{X.title_at(o, h['from'])} {h.get('title') or ''}")))
    return w - STOP


def bd_cite(e):
    return a(BD_URL.format(part=e["part"], pdf=e["pdf"]), f"BD {e['page']}")


def bd_sentences(e):
    text = e["text"].replace("‘‘", "“").replace("’’", "”")
    text = re.sub(r"(?<=[a-z])(?=(?:1[789]|20)\d\d\b)", " ", text)        # 'State senate1915-1925': a space lost
    out, last = [], "0000"
    for c in [c.strip() for c in re.split(r";\s+", text)][1:]:     # the first: the name and description
        if CUT.match(c):
            continue
        ds = iso_dates(c)
        yrs = re.findall(r"\b(1[789]\d\d|20\d\d)\b", c)
        k = ds[0] if ds else (yrs[0] if yrs else last)
        last = k
        t = re.sub(r"\b(1[789]\d\d|20\d\d)-(1[789]\d\d|20\d\d)\b", r"\1–\2", c)
        t = re.sub(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b",
                   lambda m: MONTHS[FULL[m.group(1)] - 1], t)
        t = t[0].upper() + t[1:]
        t = re.sub(r"(\d)-(\d)", r"\1–\2", t)
        out.append(sent(k, esc(t.rstrip(".")) + ".", [bd_cite(e)], kind="bd", dates=ds))
    return out


def roster_href(day):
    from . import executive as X
    return max(j for j, t in enumerate(X.TERMS) if t[0] <= day)


THE = {"Soviet Union", "United Kingdom", "Netherlands", "Philippines", "Holy See", "Dominican Republic", "Bahamas",
       "Gambia", "Central African Republic", "United Arab Emirates", "United Arab Republic", "Ivory Coast",
       "Marshall Islands", "Maldives", "Seychelles", "Comoros", "Solomon Islands", "Czech Republic",
       "Slovak Republic", "Kyrgyz Republic"}
TITLE_STOP = {"department", "office", "united", "states", "administration", "agency", "bureau", "service",
              "commission", "council", "board", "national", "federal", "with", "from", "the", "and", "for"}


def the(place):
    """'the Soviet Union', 'the United Nations'; 'India', 'UNESCO'."""
    lead = place.split(" (")[0].split(";")[0]
    org = lead.startswith(("United Nations", "Organization", "North Atlantic", "European", "International"))
    return f"the {place}" if lead in THE or org or lead.startswith("Congo") else place


def shown_title(u, o, h):
    """(title, acting prefix wanted): the office as a reader needs it outside its unit. A chief of mission by his
    post ('Ambassador to the Soviet Union'); an office whose title does not name its agency, with the agency
    ('Commissioner, Federal Trade Commission')."""
    from . import executive as X
    raw = h.get("title") or X.title_at(o, h["from"])
    if u["unit"] == "missions":
        place = X.title_at(o, h["from"])
        org = (o.get("group") or "") == "International organizations"
        if h.get("acting"):
            return f"Chargé d'Affaires ad interim {'to' if org else 'in'} {the(place)}", False
        return f"{h.get('title') or ('Representative' if org else 'Ambassador')} to {the(place)}", True
    words = lambda t: set(re.findall(r"[a-z]{4,}", fold(t))) - TITLE_STOP
    if u.get("name") and not words(raw) & words(u["name"]):
        return f"{raw}, {u['name']}", True
    return raw, True


def office_sentences(sur, given, names=None):
    """Each office held, with the ex officio offices held by virtue of it after it."""
    from . import executive as X, executive_sources as S

    held = [(u, o, h) for u, o, h in holders_of(sur)
            if (h["name"] in names if names else same_person(*split_name(h["name"]), sur, given))]

    def cites(u, o, h):
        s = S.html(h)
        ext = [s.replace('<span class="exs">Sources: ', "").replace(".</span>", "")] if s else []
        start = max(str(h["from"]), X.TERMS[0][0]).ljust(10, "0").replace("-00", "-01")
        i = roster_href(start)
        rid = X.rid_for()(i, u["unit"], o["id"])
        return ext, [ptr(f"{SITE}executive.html#{rid}", f"Exec. {X.TERMS[i][0][:4]}")]

    def when(h, host=None):
        f, t = h["from"], h.get("to")
        if host and str(f) == str(host["from"]) and str(t) == str(host.get("to")):
            return ""
        a_ = (f"in office by {fmt(f)}" if h.get("_seen") else f"from {fmt(f)}") if not host or str(f) != str(host["from"]) else ""
        b_ = (f"last listed {fmt(t)}" if h.get("_last") else f"to {fmt(t)}") if t and (not host or str(t) != str(host.get("to"))) else ""
        return " ".join(x for x in (a_, b_) if x)

    xo = [(u, o, h) for u, o, h in held if o.get("appt") == "XO"]
    hosts = [(u, o, h) for u, o, h in held if o.get("appt") != "XO"]
    out = []
    for u, o, h in sorted(hosts, key=lambda x: str(x[2]["from"])):
        title = h.get("title") or X.title_at(o, h["from"])
        pairs = [(k, h[k]) for k in ("nominated", "confirmed") if h.get(k)]
        if h.get("recess"):
            pairs.insert(0, ("recess appointment", h["recess"]))
        extra = "; " + X.dates_run(pairs) if pairs else ""
        out_ = " " + to_html(h["out"]).rstrip(".") + "." if h.get("out") else ""
        shown, prefix = shown_title(u, o, h)
        acting = "Acting " if prefix and h.get("acting") and not shown.startswith("Acting") else ""
        t = f"{acting}{esc(shown)} {when(h)}{extra}.{out_}"
        ext, intl = cites(u, o, h)
        ds = {str(h[k]) for k in ("from", "to", "nominated", "confirmed", "appointed") if h.get(k)}
        out.append(sent(h["from"], t, ext, intl, para=not h.get("acting"), kind="office", dates=ds))
        # the ex officio offices held by virtue of this one, with their own dates where they differ
        for xu, xo_, xh in sorted(xo, key=lambda x: str(x[2]["from"])):
            if (xh.get("title") or "") == title or (xh.get("title") and xh["title"] in title):
                w = when(xh, h)
                ext, intl = cites(xu, xo_, xh)
                t = f"{esc(shown_title(xu, xo_, xh)[0])}, ex officio{', ' + w if w else ''}."
                out.append(sent(h["from"], t, ext, intl, kind="xo"))
                xh["_placed"] = True
    for xu, xo_, xh in xo:
        if not xh.pop("_placed", False):
            ext, intl = cites(xu, xo_, xh)
            out.append(sent(xh["from"], f"{esc(shown_title(xu, xo_, xh)[0])}, ex officio, {when(xh)}.", ext, intl,
                            kind="office"))
    return out


POCOM_URL = "https://history.state.gov/departmenthistory/people/"
POCOM_END = {"Left post on": "Left post.", "Left post on or soon after": "Left post.", "Presented recall on":
             "Presented recall.", "Died at post on": "Died at post.", "Relinquished charge": "Relinquished charge.",
             "Superseded": "Superseded."}
WINDOW = ("1953-01-20", "1974-08-31")


def pocom_sentences(p, has_bd):
    """From POCOM (sources/pocom.json, tools/lives/make_pocom.py): the years of birth and death where the Directory
    gives none; the career type and home State; and the posts the Executive roster does not hold, those ended
    before Jan. 20, 1953, or begun after Aug. 31, 1974."""
    from .congress import STATE
    d = cached("pocom", lambda: json.load(open(os.path.join(store.ROOT, "sources", "pocom.json"), encoding="utf-8"))
               if os.path.exists(os.path.join(store.ROOT, "sources", "pocom.json")) else {})
    pid = (d.get("match") or {}).get(key_of(p["name"]))
    r = (d.get("persons") or {}).get(pid) if pid else None
    if not r:
        return []
    cite = [a(POCOM_URL + pid, "POCOM")]
    out = []
    states = [{"DC": "the District of Columbia"}.get(x.upper()) or STATE.get(x.upper(), x.upper())
              for x in r.get("states") or []]
    home = ", of " + (" and ".join(states) if len(states) < 3 else ", ".join(states[:-1]) + ", and " + states[-1]) \
        if states else ""
    first = (r.get("posts") or [[None, "", ""]])[0]
    k0 = r.get("birth") or (first[2] or first[1] or "")[:4]
    if r.get("birth") and not has_bd:
        out.append(sent(r["birth"], f"Born {r['birth']}.", cite, kind="pocom"))
    if r.get("career") or home:
        t = (r.get("career") or "") + home if r.get("career") else home[2:].capitalize()
        out.append(sent(k0, f"{t}.", cite, kind="pocom"))
    note = (d.get("check") or {}).get(key_of(p["name"]))
    if note:                             # a match made by hand, to verify
        out.append(sent(k0, f"Check: {esc(note.rstrip('.'))}.", cite, kind="pocom"))
    for label, ap, began, ended, end_note, note in r.get("posts") or []:
        b = began or ap
        if b and b <= WINDOW[1] and (ended or "9999") >= WINDOW[0]:
            continue                     # the roster holds it
        label = re.sub(r"\s+", " ", label)
        if not re.search(r"State|Ambassador|Representative|Minister|Chargé|Envoy|Agent|Administrator|Director of the|"
                         r"Trade|Chief of Mission|Principal Officer", label):
            label += ", Department of State"   # POCOM's principal officers of the Department: 'Counselor'
        if began:
            t = f"{esc(label)} from {fmt(began)}" + (f" to {fmt(ended)}" if ended else "")
            t += (f"; commissioned {fmt(ap)}" if ap and ap != began else "") + "."
        elif ap:
            t = f"Commissioned {esc(label)}, {fmt(ap)}."
        else:
            continue
        if POCOM_END.get(end_note):
            t += " " + POCOM_END[end_note]
        elif end_note and not end_note.endswith(" on"):
            t += " " + esc(end_note.rstrip(".")) + "."
        if note:
            t += " " + esc(re.sub(r"\s+", " ", note).rstrip(".")) + "."
        out.append(sent(b, t, cite, para=True, kind="office", dates={x for x in (ap, began, ended) if x}))
    if r.get("death") and not has_bd:
        out.append(sent(f"{r['death']}-99", f"Died {r['death']}.", cite, kind="pocom"))
    return out


def roster_pointers(sur, given, names=None):
    """[(day, Congress, pointer)] for each Congress at whose opening the person held a seat."""
    from .congress import ordinal

    def make():
        idx = {}
        for f in sorted(os.listdir(os.path.join(store.ROOT, "congress"))):
            m = re.match(r"(\d\d)\.yaml$", f)
            if not m:
                continue
            d = store.load_yaml(os.path.join(store.ROOT, "congress", f)) or {}
            for ch, rows in (("s", d.get("senate") or []), ("h", d.get("house") or [])):
                for r in rows:
                    if r.get("name"):
                        idx.setdefault(fold(split_name(r["name"])[0]), []).append((int(m.group(1)), d, ch, r))
        return idx
    out = []
    for c, d, ch, r in cached("congress", make).get(fold(sur), []):
        if True:
            if True:
                rs, rg = split_name(r.get("name") or ",")
                if r.get("name") and (r["name"] in names if names else same_person(rs, rg, sur, given)):
                    seat = r.get("cl") if ch == "s" else r.get("d", 0)
                    out.append((str(d.get("opened")), c, ch, r["st"],
                                ptr(f"{SITE}congress.html#cg{c}-{ch}-{r['st']}-{seat}", f"{ordinal(c)} Cong."), seat))
    return out





def last_word(n):
    """The surname of a name as the returns print it: 'Harry F. Byrd Jr.' -> 'Byrd'."""
    w = [x for x in re.sub(r",", " ", n).split() if not re.fullmatch(r"(Jr|Sr|II|III|IV)\.?", x)]
    return w[-1] if w else n


def election_sentences(sur, given, sfx="", strict=False):
    """The person's races, from elections/. A candidate's suffix as Wikipedia writes it ('Harry F. Byrd Jr.') agrees
    with the person's; one without a suffix is taken only where no namesake has an entry (strict: the person is the
    son, and the father, written bare, has his own)."""
    from .elections import rid as erid
    from .congress import STATE, BLUEBOOK
    out = []
    first = fold(given.split()[0]) if given else ""

    def mine(n):
        if not n or fold(last_word(n)) != fold(sur) or fold(n.split()[0]) != first:
            return False
        m = re.search(r",? (Jr|Sr|II|III|IV)\.?$", n)
        cs = m.group(1) if m and m.group(1) != "Sr" else ""
        return cs == sfx if cs else not strict
    def make():                          # the elections module's copy: the build has read them once already
        from .elections import load
        return [(str(y), d or {}) for y, d in sorted(load().items()) if y != 1956]

    def cand_index():
        """surname -> {year: [the races (by index) with a candidate of that surname]}; -1 the presidential race."""
        idx = {}
        for y, d in cached("elections", make):
            for i, r in enumerate(d.get("races") or []):
                for c in (r.get("cands") or []) + (r.get("inc") or []):
                    if c.get("n"):
                        rs = idx.setdefault(fold(last_word(c["n"])), {}).setdefault(y, [])
                        if i not in rs:
                            rs.append(i)
            for c in (d.get("president") or {}).get("cands") or []:
                if c.get("n"):
                    idx.setdefault(fold(last_word(c["n"])), {}).setdefault(y, []).append(-1)
            from . import elections as E
            pf = E.facts().get("president") or {}
            vn = list(((pf.get("vice") or {}).get(int(y)) or {}).values())
            vn += [n for split in ((pf.get("vice_cast") or {}).get(int(y)) or {}).values() for n in split]
            for n in vn:                 # the running mates
                idx.setdefault(fold(last_word(n)), {}).setdefault(y, []).append(-1)
        return idx
    years = cached("election-races", cand_index).get(fold(sur), {})
    for y, d in cached("elections", make):
        if y not in years:
            continue
        url = (d.get("source") or {}).get("url", "")

        def clerk(pg=None):
            return a(url + (f"#page={pg}" if pg else ""), f"Clerk, Election Statistics {y}" + (f", p. {pg}" if pg else ""))
        races = d.get("races") or []
        for r in (races[i] for i in years[y] if i >= 0):
            cs = r.get("cands") or []
            me = next((c for c in cs if mine(c.get("n"))), None)
            if not me:
                continue
            tot = sum(c.get("v") or 0 for c in cs) + (r.get("scat") or 0)
            share = f" ({100 * me['v'] / tot:.1f} percent)" if tot and me.get("v") else ""
            others = ", ".join(f"{esc(c['n'])} ({c['p']}) {c['v']:,}" for c in cs if c is not me and c.get("v"))
            inc = any(mine(i.get("n")) for i in r.get("inc") or [])
            what = ("Reelected" if inc else "Elected") if me.get("w") else ("Defeated for reelection" if inc else "Defeated")
            where = STATE.get(r["st"], r["st"])
            seat = "Senate" if r["ch"] == "s" else f"House, {r['st']}-{r['seat'] or 'AL'}"
            votes = f": {me['v']:,} votes{share}" + (f"; {others}" if others else "") if me.get("v") else (
                ": unopposed, no vote printed" if len(cs) == 1 else "")
            t = f"{what} {'to' if me.get('w') or inc else 'for'} the {seat}{', ' + where if r['ch'] == 's' else ''}, {fmt(d['date'])}{votes}."
            out.append(sent(d["date"], t, [clerk(r.get("page"))], [ptr(f"{SITE}congress.html#{erid(y, r)}", f"Election {y}")],
                            para=True, kind="election", dates={d["date"]}))
            out[-1]["row"] = {
                "cong": (int(y) - 1788) // 2 + 1, "ch": r["ch"], "st": r["st"], "date": d["date"],
                "election": ptr(f"{SITE}congress.html#{erid(y, r)}", fmt(d["date"])),
                "seat": f"Senate, {BLUEBOOK.get(r['st'], r['st'])}" if r["ch"] == "s" else
                        f"{BLUEBOOK.get(r['st'], r['st'])}-{r['seat'] or 'AL'}",
                "result": "",
                # every candidate by the final tally, the person among them in bold
                "cands": [cand(c["n"], c.get("p"), (f"{c['v']:,}" + (f" ({pct(c['v'], tot)})" if tot else "")) if c.get("v")
                               else ("unopposed; no vote printed" if len(cs) == 1 else ""), c is me)
                          for c in sorted((c for c in cs if c is me or c.get("v")), key=lambda c: -(c.get("v") or 0))],
                "src": a(url + (f"#page={r['page']}" if r.get("page") else ""),
                         f"Clerk {y}" + (f", p. {r['page']}" if r.get("page") else ""))}
        out += ticket_rows(y, d, url, mine)
    return out


def series_html(ptrs, text, home, e=None):
    """Text with the series' own markup made pointers: '[[id]]' (a calendar date, the year added where it differs)
    and the references to lists and sections ('K–J Adm. II.D')."""
    from .build import label_of
    series, linker = ptrs.series, ptrs.linker
    toks = []

    def tok(html):
        toks.append(html)
        return f"\x01{len(toks) - 1}\x01"

    def link(m):
        eid, shown = m.group(1), m.group(2)
        hit = series.get(eid)
        if not hit:
            return shown or eid
        lst, sec, x = hit
        lab = shown or label_of(series, eid) or eid
        if not shown and x.get("date") and e is not None and x["date"][:4] != (e.get("date") or "")[:4]:
            lab += f", {x['date'][:4]}"
        return tok(ptr(f"{SITE}{lst.key}.html#{eid}", esc(lab)))
    text = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", link, text)
    out, pos = [], 0
    for a_, b_, key, code in linker.refs.scan(text, home):
        sec = linker.refs.section_for(key, code) if code else None
        lst = series.lists.get(key)
        if not lst:
            continue
        href = f"{SITE}{key}.html#{sec.id}" if sec else f"{SITE}{key}.html"
        out.append(text[pos:a_] + tok(ptr(href, esc(text[a_:b_]))))
        pos = b_
    out.append(text[pos:])
    html = to_html("".join(out))
    return re.sub(r"\x01(\d+)\x01", lambda m: toks[int(m.group(1))], html)


def subjects(ptrs, name, ok):
    """[(list, section, entry)]: the series' entries whose subject line ('s') is the person (Part III and the
    subject entries of Part II), by the name keys, a namesake's suffix left out (ok)."""
    out, seen = [], set()
    for k in ptrs.keys(name)[0]:
        for l, s, e in ptrs.linker.people.get(k, []):
            if e["id"] not in seen and ok(e.get("s") or ""):
                seen.add(e["id"])
                out.append((l, s, e))
    return out


def calendar_of(ptrs, subs):
    """The calendar entries whose 'Names:' line names one of the person's Part III entries, by date."""
    out, seen = [], set()
    for l, s, x in subs:
        for e in ptrs.calx.get(x["id"], []):
            if e["id"] not in seen:
                seen.add(e["id"])
                out.append(e)
    return sorted(out, key=lambda e: e["date"])


def series_lines(subs, cal):
    """The 'In the series' pointers: each entry by list and section, then the calendar's dates."""
    out = [ptr(f"{SITE}{l.key}.html#{e['id']}", f"{esc(l.abbr)} {esc(s.code)}") for l, s, e in subs]
    dates, prev = [], None
    for e in cal:
        y = e["date"][:4]
        dates.append(ptr(f"{SITE}cal.html#{e['id']}", esc(e["when"] + (f", {y}" if y != prev else ""))))
        prev = y
    if dates:
        out.append("Cal. " + ", ".join(dates))
    return out


def calendar_sentences(ptrs, cal):
    out = []
    for e in cal:
        if True:
            c = series_html(ptrs, store.as_list(e.get("c"))[0] if e.get("c") else "", "cal", e)
            n = series_html(ptrs, re.sub(r"\s*Names:.*$", "", e.get("n") or "").strip(), "cal", e) if e.get("n") else ""
            out.append(sent(e["date"], f"{esc(e['when'])}, {e['date'][:4]}: {c}", [n] if n else [],
                            [ptr(f"{SITE}cal.html#{e['id']}", f"Cal. {esc(e['when'])}, {e['date'][:4]}")], kind="cal"))
    return out


def merge(structured, bd, rosters):
    """The Directory's clauses into the structured sentences: a clause whose full dates all fall in one sentence's
    dates, or whose year and words match one, becomes that sentence's second cite. The rosters as pointers on the
    clause that gives the service they fall in."""
    out = [s for s in structured]
    hosts = [s for s in structured if s["kind"] in ("office", "election")]
    W = lambda t: set(re.findall(r"[a-z]{4,}", plain(re.sub(r"<[^>]+>", " ", t)).lower())) - {"united", "states", "with", "from", "until"}
    for b in bd:
        words = W(b["text"])
        cand = [s for s in hosts if b["dates"] and s["dates"] and b["dates"] <= s["dates"]]
        if not cand and not b["dates"]:
            cand = [s for s in hosts if s["key"][:4] == b["key"][:4] and len(words & W(s["text"])) >= 2]
        if cand:
            host = max(cand, key=lambda s: (len(words & W(s["text"])), -len(W(s["text"]) - words)))
            # a cite the host already gives (the roster's own 'BD 1415') is not given twice
            have = "; ".join(re.sub(r"<[^>]+>", "", y) for y in host["ext"])
            host["ext"] = host["ext"] + [x for x in b["ext"] if x not in host["ext"] and not re.search(
                r"(?:^|; )" + re.escape(re.sub(r"<[^>]+>", "", x)) + r"(?:;|$)", have)]
            continue
        out.append(b)
    from .congress import ordinal

    def serves(b, day):
        """A clause of service ('served from Jan. 3, 1971, until his death') that holds the day."""
        if b["kind"] != "bd" or not re.search(r"served from", b["text"]) or not b["dates"]:
            return False
        end = max(b["dates"]) if len(b["dates"]) >= 2 else "9999"
        return min(b["dates"]) <= day <= end
    for day, c, ch, st, p, *_ in rosters:
        span = next((b for b in out if serves(b, day)), None)
        if span:
            span["int"].append(p)
        else:
            out.append(sent(day, f"In the {'Senate' if ch == 's' else 'House'} at the opening of the {ordinal(c)} "
                                 f"Congress.", [], [p], kind="seat"))
    return sorted(out, key=lambda s: (s["key"][:10].ljust(10, "0")))


def pointers(ps):
    """'87th Cong.' and '88th Cong.' as one pointer, '87th, 88th Cong.', each Congress linked."""
    out, cg = [], []
    for p in dict.fromkeys(ps):
        m = re.match(r'(<a class="lvp" href="[^"]+">)(\d+\w+) Cong\.</a>', p)
        if m:
            cg.append(m.group(1) + m.group(2) + "</a>")
        else:
            out.append(p)
    if cg:
        out.append(", ".join(cg) + ' <span class="lvp">Cong.</span>')
    return "; ".join(out)


def cand(name, party, votes, me=False):
    """A candidate's line in the record: 'Ray Wolfram (R) 17,471 (14.1%)'; the person's own first, in bold."""
    n = esc(name) + (f" ({esc(party)})" if party else "")
    n = f"<b>{n}</b>" if me else n
    return n + (f' <span class="lvv">{votes}</span>' if votes else "")


def pct(v, tot):
    """A share of the vote: '85.9%'; under a tenth of a point, '<0.1%'."""
    x = 100 * v / tot
    return f"{x:.1f}%" if x >= 0.05 else "<0.1%"


PARTY_LETTER = {"Democratic": "D", "Republican": "R", "American Independent": "AIP", "Libertarian": "L",
                "Socialist Labor": "SL", "Unpledged Democratic": "U"}


def ticket_rows(y, d, url, mine):
    """The person's candidacies for President and Vice President in the year: a sentence and a table row each, with
    the electoral votes before the popular. The running mates and their electoral votes: elections/facts.yaml
    (president: vice, vice_cast)."""
    from . import elections as E
    p = d.get("president")
    if not p:
        return []
    facts = (E.facts().get("president") or {}) if hasattr(E, "facts") else {}
    vice, vcast = (facts.get("vice") or {}).get(int(y), {}), (facts.get("vice_cast") or {}).get(int(y), {})
    pv, ev = {}, {}
    for st in p["states"]:
        for s_ in st.get("slates") or []:
            if s_.get("k"):
                pv[s_["k"]] = pv.get(s_["k"], 0) + s_["v"]
        for k_, n_ in (st.get("cast") or {}).items():
            ev[k_] = ev.get(k_, 0) + n_
    allv = sum(pv.values()) or 1
    letter = {c["k"]: PARTY_LETTER.get(c.get("party") or "", "") for c in p["cands"]}
    pres = {c["k"]: c.get("n") or c["k"] for c in p["cands"]}
    winner = max(ev, key=ev.get)
    out = []
    for office, names in (("President", pres), ("Vice President", vice)):
        # (name, key, electoral votes): a running mate takes his ticket's, an elector's split its own
        field = [(n, k_, ev.get(k_, 0)) for k_, n in names.items() if k_ not in vcast or office == "President"]
        if office == "Vice President":
            for k_, split in vcast.items():
                field += [(n, None, v) for n, v in split.items()]
        me = next((f for f in field if mine(f[0])), None)
        if not me:
            continue
        n, k, e = me
        lt = letter.get(k, "")
        won = k == winner
        result = "Elected" if won else "Defeated"
        share = lambda x: f"{pv.get(x, 0):,} PV ({pct(pv.get(x, 0), allv)})" if pv.get(x) else ""
        line = lambda n2, k2, e2: "; ".join(x for x in (f"{e2} EV" if e2 else "", share(k2) if k2 else "") if x)
        # every candidate by electoral votes, then popular; the person among them in bold
        field_ = [cand(n2, letter.get(k2, "") if k2 else "", line(n2, k2, e2), (n2, k2) == (n, k))
                  for n2, k2, e2 in sorted(field, key=lambda f: (-f[2], -pv.get(f[1], 0)))
                  if (n2, k2) == (n, k) or e2 or pv.get(k2, 0) >= allv * 0.01]
        t = (f"{result.split(' (')[0]} {'to' if won else 'for'} the office of {office}, {fmt(d['date'])}: {e} electoral "
             f"votes; {share(k)} popular." if k else f"{office}, {fmt(d['date'])}: {e} electoral votes.")
        out.append(sent(d["date"], t, [a(url, f"Clerk, Election Statistics {y}")],
                        [ptr(f"{SITE}congress.html#e{y}", f"Election {y}")], para=True, kind="election",
                        dates={d["date"]}))
        out[-1]["row"] = {
            "cong": None, "ch": "p" if office == "President" else "v", "st": "", "date": d["date"],
            "election": ptr(f"{SITE}congress.html#e{y}", fmt(d["date"])), "seat": office, "result": "",
            "exec": exec_pointer(n, office, f"{int(y) + 1}-01-20") if k == winner else "",
            "cands": field_, "src": a(url, f"Clerk {y}")}
    return out


def exec_pointer(name, office, day):
    """'Exec. 1965', to the office in the term the election chose, as the roster holds it."""
    from . import executive as X
    sur = last_word(name)
    for u, o, h in holders_of(sur):
        if str(h.get("from")) <= day <= str(h.get("to") or "9999") and X.title_at(o, day) in (office, f"{office} of the United States") \
                and fold(split_name(h["name"])[1].split()[0] if split_name(h["name"])[1] else "") == fold(name.split()[0]):
            i = roster_href(day)
            return ptr(f"{SITE}executive.html#{X.rid_for()(i, u['unit'], o['id'])}", f"Exec. {X.TERMS[i][0][:4]}")
    return ""


def record_html(rows, rosters):
    """The record in Congress, a table after the life: a row an election, with the Congress it chose and the seat at
    that Congress's opening; a row a Congress where the member sat at its opening without an election here (a Senator
    between elections, "Continuing"); a row a candidacy for President or Vice President. The candidates by the final
    tally (electoral votes, then popular), the person in bold: where he stands shows how he did. Every cite and
    pointer the running text gave."""
    from .congress import BLUEBOOK
    seats = {(c, ch): (day, st, p, seat) for day, c, ch, st, p, seat in rosters}
    used, out = set(), []
    for r in rows:
        k = (r["cong"], r["ch"]) if r["cong"] else None
        hit = seats.get(k) if k else None
        if hit and hit[1] == r["st"]:
            used.add(k)
        else:
            hit = None
        out.append((r["cong"] or 0, r["date"], hit[2] if hit else r.get("exec", ""), r["election"], r["seat"], r["result"],
                    "<br>".join(r["cands"]), r["src"]))
    for (c, ch), (day, st, p, seat) in seats.items():
        if (c, ch) in used:
            continue
        where = f"Senate, {BLUEBOOK.get(st, st)}" if ch == "s" else f"{BLUEBOOK.get(st, st)}-{seat or 'AL'}"
        out.append((c, day, p, "", where, "", "Continuing", ""))
    if not out:
        return ""
    out.sort(key=lambda x: (x[1][:4], x[0]))
    head = "<tr><th>Election<br>Congress</th><th>Seat</th><th>Candidates<br>Source</th></tr>"
    two = lambda a_, b_: f"{a_}<br>{b_}" if a_ and b_ else (a_ or b_)
    body = "".join(
        f"<tr><td>{two(el, cg)}</td><td>{two(seat, res)}</td>"
        f'<td>{two(cands, f"""<span class="lvts">{src}</span>""" if src else "")}</td></tr>'
        for _, _, cg, el, seat, res, cands, src in out)
    return (f'<h3>Elections and Congresses</h3><div class="lvtw"><table class="lvt"><thead>{head}</thead>'
            f"<tbody>{body}</tbody></table></div>")


def life_html(sents):
    """Running text, in paragraphs at each office and election. Each run of sentences with the same sources and the
    same pointers is one sentence block; its source block follows it: the cites, then the pointers."""
    paras, cur, block = [], [], None

    def close():
        nonlocal block
        if block:
            ext, intl = block
            if ext:
                cur.append(f'<span class="lvc">{"; ".join(x.rstrip(".") for x in ext)}.</span>')
            if intl:
                cur.append('<span class="lvq">' + pointers(list(intl)) + "</span>")
        block = None
    for s in sents:
        key = (tuple(dict.fromkeys(s["ext"])), tuple(dict.fromkeys(s["int"])))
        if block is not None and (key != block or s["para"]):
            close()
        if s["para"] and cur:
            paras.append(" ".join(cur))
            cur = []
        cur.append(s["text"])
        block = key
    close()
    if cur:
        paras.append(" ".join(cur))
    return "".join(f'<p class="lvl">{p}</p>' for p in paras)


# ---------------------------------------------------------------- the lists

def article(title, rest):
    """“Title,” in Where (1977)."""
    rest = re.sub(r"^In\b", "in", rest.strip()).rstrip(".")
    return f"“{title.rstrip('.,')}{',' if rest else ''}”" + (f" {rest}" if rest else "")


def bd_work(item):
    """The Directory's 'Thurber, Timothy N. The Politics of Equality. New York: Columbia University Press, 1999.'
    in the series' form: 'Timothy N. Thurber, *The Politics of Equality* (1999)'."""
    m = re.match(r"^([A-Z][\w'’\- ]+), (.*)$", item)
    if not m:
        return f"*{item.rstrip('.')}*"
    sur, toks = m.group(1), m.group(2).split(" ")
    sm = re.match(r"^([^,]+), (Jr\.|Sr\.|II|III|IV)\.? (.*)$", m.group(2))
    if sm:                               # 'Byrd, Harry F., Jr. ‘‘The Limitations of Detente.’’ In ...'
        given, sfx, rest = sm.group(1).strip(), sm.group(2), sm.group(3)
        q = re.match(r"^(?:‘‘|“|\")(.+?)[.,]?(?:’’|”|\")\s*(.*)$", rest)
        if q:
            return f"{given} {sur}, {sfx}, " + article(q.group(1), q.group(2))
        return bd_work(f"{sur}, {given} {rest}").replace(f"{given} {sur},", f"{given} {sur}, {sfx},", 1)
    # an article: 'Smith, John. ‘‘Title.’’ In Journal ...'
    am = re.match(r"^(.*?)\. (?:‘‘|“)(.+?)[.,]?(?:’’|”)\s*(.*)$", m.group(2))
    if am and len(am.group(1)) < 40:
        return f"{am.group(1)} {sur}, " + article(am.group(2), am.group(3))
    # the given names run to a word that ends with a period, or to an initial not followed by another initial
    k = 0
    while k < len(toks):
        t_ = toks[k]
        if re.fullmatch(r"[A-Z]\.", t_):
            if k + 1 < len(toks) and re.fullmatch(r"[A-Z]\.", toks[k + 1]):
                k += 1
                continue
            break
        if t_.endswith("."):
            break
        k += 1
    given, rest = " ".join(toks[:k + 1]).rstrip("."), " ".join(toks[k + 1:])
    given = re.sub(r"\b([A-Z])$", r"\1.", given)
    # the title runs to the imprint ('. New York: Columbia University Press, 1999') or the bare year ('. 1976.')
    imp = re.search(r"\.\s+(?:[A-Z][A-Za-z ,'’]*(?:[A-Z]\.){0,3}: [^.:]*?, |)(1[89]\d\d|20\d\d)\b", rest)
    title = rest[:imp.start()] if imp else rest.rstrip(".")
    return f"{given} {sur}, *{title}*" + (f" ({imp.group(1)})" if imp else "")


def bd_bib(e, sur, lines):
    if not e or not e.get("bib"):
        return [], []
    own, about = [], []
    for item in re.split(r";\s+", e["bib"]):
        parts = item.split(". ")
        title = fold(parts[1] if len(parts) > 1 and "," in parts[0] else parts[0])
        title = re.split(r"[:.]", title)[0].strip()
        hit = next((i for i, l in enumerate(lines) if title and title in fold(plain(re.sub(r"<[^>]+>", "", l)))), None)
        if hit is not None:
            lines[hit] = lines[hit][:-len("</span>")] + f"; {bd_cite(e)}</span>"
            continue
        line = f'{to_html(bd_work(item))}. <span class="lvc">{bd_cite(e)}</span>'
        (own if re.match(re.escape(sur) + r",", item, re.I) else about).append(line)
    return own, about


def frus_lists(name):
    d = letter_json("frus-names", key_of(name)[:1].upper()).get(key_of(name), {})
    titles = cached("frus-volumes", lambda: json.load(open(os.path.join(store.ROOT, "sources", "frus-names", "volumes.json"),
                                                         encoding="utf-8")) if os.path.exists(os.path.join(
                                                         store.ROOT, "sources", "frus-names", "volumes.json")) else {})
    from .executive_sources import frus_label
    sent_, named = [], []
    for vol, v in d.items():
        lab = frus_label(vol)
        # one line a heading in a volume: 'Telegram from the Department of State to the Embassy in France.
        # FRUS 1961–63, XIV, docs. 12 (Feb. 3, 1961), 15 (Feb. 9, 1961)'
        heads = {}
        for n, date, title in v["sent"]:
            heads.setdefault(lower_from(title), []).append((n, date))
        for title, docs in heads.items():
            first = min(d for _, d in docs) if any(d for _, d in docs) else ""
            nums = ", ".join(f'<span class="lvg" data-v="{esc(vol)}" data-n="{esc(n)}">{esc(n)}</span>'
                             + (f" ({fmt(d)})" if d else "") for n, d in docs)
            sent_.append((first, f'{esc(title)}. <span class="lvc">{esc(lab)}, {"doc." if len(docs) == 1 else "docs."} '
                                 f'{nums}</span>'))
        # the numbers only; the page links each to its document (the script below), to keep the pages light
        docs = " ".join(esc(n) for n, _ in v["named"])
        k = len(v["named"])
        named.append((vol, f'{esc(lab)}{": " + esc(titles.get(vol, "")) if titles.get(vol) else ""}: '
                           f'{"doc." if k == 1 else "docs."} <span class="lvf" data-v="{esc(vol)}">{docs}</span>.'))
    sent_.sort()
    return [x for _, x in sent_], [x for _, x in sorted(named, key=lambda t: vol_order(t[0]))]


def vol_order(vol):
    m = re.match(r"frus(\d{4})-\d+v(e?)(\d+)", vol)
    return (m.group(1), m.group(2), int(m.group(3))) if m else (vol, "", 0)


def app_list(name, sur):
    """The presidential documents that name the person (sources/app-names: indexes into sources/app-index.jsonl)."""
    hits = letter_json("app-names", key_of(name)[:1].upper()).get(key_of(name), [])
    if not hits:
        return []
    rows = cached("app-index", lambda: [json.loads(l) for l in open(os.path.join(store.ROOT, "sources", "app-index.jsonl"),
                                                                    encoding="utf-8")])
    keep = []
    for i in hits:
        r = rows[i]
        d = datetime.datetime.strptime(r["date"], "%b %d, %Y").date().isoformat()
        keep.append((d, r))
    keep.sort(key=lambda t: t[0])
    by_year = {}
    given = split_name(name)[1]
    me = lambda who: fold(last_word(who)) == fold(sur) and fold(who.split()[0]) == fold((given.split() or [""])[0])
    is_president = any(me(n) for n, _, _ in PRESIDENTS)
    for d, r in keep:
        sitting = any(n == r["who"] and f <= d < t for n, f, t in PRESIDENTS)
        # who issued it: in a President's own entry, nothing for his own documents and the initials of the sitting
        # President for another's (DDE); elsewhere, nothing for the sitting President and the name for anyone else
        if me(r["who"]):
            who = ""
        elif is_president and sitting:
            who = INITIALS[r["who"]]
        else:
            who = "" if sitting else esc(r["who"])
        # the title, then who and when, as the speeches are cited: 'Address on Mississippi (Sept. 30, 1962), APP.'
        by_year.setdefault(d[:4], []).append(
            f'{esc(r["title"].rstrip("."))} ({who + ", " if who else ""}{fmt(d)}), '
            + f'<span class="lvc">{a(r["url"], "APP")}</span>.')
    return [f'<b>{y}</b><br>' + "<br>".join(v) for y, v in by_year.items()]


# ---------------------------------------------------------------- the entry

def person_for(series, name):
    """The person (people()) a name given on the command line is: the one holding it as written, else one whose
    names it agrees with."""
    everyone = cached("people", lambda: people(series))
    return (next((p for p in everyone if name in p["names"]), None)
            or next((p for p in everyone if same_person(p["sur"], p["given"], *split_name(name))), None)
            or {"name": name, "sur": split_name(name)[0], "given": split_name(name)[1], "names": {name}})


def namesakes(series):
    """(surname, first given name) held by more than one person: there a bare name in the returns is not taken."""
    def make():
        n = {}
        for p in cached("people", lambda: people(series)):
            k = (fold(p["sur"]), (gtoks(p["given"]) or [""])[0])
            n[k] = n.get(k, 0) + 1
        return {k for k, v in n.items() if v > 1}
    return cached("namesakes", make)


def person_suffix(series, p):
    """(suffix, strict): the person's Jr., II, III or IV, if any name gives one; strict where a namesake has his own
    entry, so a bare name elsewhere is the namesake's."""
    sfx = next((suffix(n) for n in sorted(p["names"]) if suffix(n) not in ("", "Sr")), "")
    sur, given = split_name(p["name"])
    return sfx, bool(sfx) and (fold(sur), (gtoks(given) or [""])[0]) in namesakes(series)


def entry(series, linker, ptrs, p):
    if isinstance(p, str):
        p = person_for(series, p)
    name, names = p["name"], p["names"]
    sur, given = split_name(name)
    sfx, strict = person_suffix(series, p)
    # Part III's pointers go by surname and first name: a person Part III does not hold, whose namesake it does
    # (Harry F. Byrd, Jr.; Adlai E. Stevenson III), has none
    def ok(s_):
        es = suffix(re.sub(r"\s*\([^)]*\)\s*$", "", plain(s_)))
        return es == sfx if es not in ("", "Sr") else not strict
    subs = subjects(ptrs, name, ok)
    cal = calendar_of(ptrs, [x for x in subs if (x[1].code or "").startswith("III")])
    rp = roster_pointers(sur, given, names)
    member = bool(rp)
    e = bd_entry(sur, given, member, () if member else person_words(sur, given, names), sfx)
    structured = (office_sentences(sur, given, names) + election_sentences(sur, given, sfx, strict)
                  + calendar_sentences(ptrs, cal) + pocom_sentences(p, bool(e)))
    record = [s_["row"] for s_ in structured if s_.get("row")]
    structured = [s_ for s_ in structured if s_["kind"] != "election"]
    life = merge(structured, bd_sentences(e) if e else [], [])
    # the Directory's account of service in Congress opens a paragraph, with its own source block
    for s_ in life:
        if s_["kind"] == "bd" and re.match(r"(Elected|Appointed|Was elected|Successfully contested)\b", s_["text"]) \
                and re.search(r"Congress|Senate|House", s_["text"]):
            s_["para"] = True
            break
    works = series_works(series, linker, ptrs, name, subs, strict)
    sent_, named = frus_lists(name)
    ppp = app_list(name, sur)
    out = [f'<section class="lv" id="{key_of(name)}"><h2 id="{key_of(name)}-h" data-short="{esc(sur)}">{esc(name)}</h2>']
    if e:
        head = re.split(r";\s+", e["text"])[0]
        desc = head.split("), ", 1)[-1] if "), " in head else head.split(", ", 2)[-1]
        desc = re.sub(r" and (?:an?) ", " and ", re.sub(r"^(?:an?) ", "", desc))   # 'Senator from Minnesota and Vice President' 
        out.append(f'<p class="lvd">{esc(desc[0].upper() + desc[1:])}. <span class="lvc">{bd_cite(e)}.</span></p>')
    else:
        roles = [(l, s_, x) for l, s_, x in subs if (s_.code or "").startswith("III") and x.get("r")]
        if roles:
            l, s_, x = roles[0]
            out.append(f'<p class="lvd">{to_html(x["r"])}. <span class="lvq">'
                       f'{ptr(f"{SITE}{l.key}.html#{x["id"]}", f"{esc(l.abbr)} {esc(s_.code)}")}</span></p>')
    pts = series_lines(subs, cal)
    if pts:
        out.append('<p class="lvs">In the series: ' + "; ".join(pts) + ".</p>")
    out.append("<h3>Life</h3>" + life_html(life))
    out.append(record_html(record, rp))

    def section(title, items, empty="None in the series.", cls="lvb", fold=None):
        if not items:                    # an empty section is left out
            return
        body = f'<ul class="{cls}">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"
        if fold:                         # the long lists closed until opened
            out.append(f'<details class="lvz"><summary><h3>{title}</h3> <span class="lvc">{fold}</span></summary>{body}</details>')
        else:
            out.append(f"<h3>{title}</h3>" + body)
    kinds = lambda k: [w for w in works if w[0] == k]
    g_own, g_prim, g_about = grouped(kinds("own")), grouped(kinds("primary")), grouped(kinds("about"))
    every = g_own + g_prim + g_about
    bown, babout = bd_bib(e, sur, every)
    n1, n2 = len(g_own), len(g_own) + len(g_prim)
    g_own, g_prim, g_about = every[:n1], every[n1:n2], every[n2:]
    section("Publications", by_date(g_own + bown))
    ns = sum(x.count('class="lvg"') for x in sent_)
    section("FRUS documents sent", sent_, "None found.", fold=f"{ns:,}" if len(sent_) > 20 else None)
    section("Oral histories given, papers, and other primary sources", by_date(g_prim))
    nf = sum(x.count(" ") + 1 for x in re.findall(r'class="lvf" data-v="[^"]*">([^<]*)<', "".join(named)))
    section("FRUS documents that name", named, "None found.", "lvb lvf",
            fold=f"{nf:,} in {len(named)} {'volume' if len(named) == 1 else 'volumes'}")
    na = sum(x.count("<br>") for x in ppp)
    section("Presidential documents that name", ppp, "None found.", "lvb lvf lvy", fold=f"{na:,}")
    section("Secondary sources", by_date(g_about + babout))
    out.append("</section>")
    return "\n".join(out)


CSS = """<style>
/* Lives (tools/bib/lives.py) */
.lv h2{margin-top:2rem}
.lv h3{font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:1.4rem 0 .4rem}
.lvd{font-size:.95rem}
.lvs{font-size:.82rem;color:var(--muted)}
p.lvl{margin:.5rem 0;line-height:1.55}
ul.lvx{list-style:none;margin:.3rem 0 1rem;padding:0;columns:2;column-gap:1.5rem;font-size:.92rem;line-height:1.5}
ul.lvx li{break-inside:avoid;padding-left:1em;text-indent:-1em}
ul.lvx a{color:var(--ink);text-decoration:none}
ul.lvx a:hover{text-decoration:underline;text-decoration-color:var(--muted)}
.lvtw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:.3rem 0 .8rem}
table.lvt{border-collapse:collapse;font-size:.82rem;line-height:1.35;min-width:100%}
table.lvt th{font-family:var(--sans);font-size:.7rem;font-weight:600;letter-spacing:.04em;text-transform:uppercase;
  color:var(--muted);text-align:left;border-bottom:1px solid var(--rule,#ccc);padding:.25rem .5rem .25rem 0;white-space:nowrap}
table.lvt td{vertical-align:top;padding:.3rem .6rem .3rem 0;border-bottom:1px solid var(--rule,#e5e5e5)}
table.lvt td:nth-child(-n+2){white-space:nowrap}
table.lvt td:nth-child(3){padding-right:0}
table.lvt b{font-weight:600}
table.lvt .lvv{white-space:nowrap}
table.lvt .lvts,table.lvt .lvts a{color:var(--muted);font-size:.92em}
table.lvt td a.lvp{font-size:.9em}
.lvc{font-size:.85em;color:var(--muted)}
.lvc a{color:inherit}
/* pointers into the series: sans serif, not underlined, as the headings */
a.lvp,span.lvp{font-family:var(--sans);font-size:.74em;font-weight:600;letter-spacing:.01em;color:var(--muted);text-decoration:none}
a.lvp:hover{color:var(--ink);text-decoration:underline}
.lvq{white-space:normal}
.lvq a.lvp{margin-left:.15em}
ul.lvb{margin:.2rem 0 .6rem;padding-left:1.1rem;font-size:.9rem;line-height:1.45}
ul.lvb li{margin:.25rem 0}
ul.lvf{font-size:.84rem}
ul.lvy{list-style:none;padding-left:0}
ul.lvy li{margin:.6rem 0}
.lvn{font-size:.85rem;color:var(--muted)}
details.lvz>summary{cursor:pointer;list-style:none}
details.lvz>summary h3{display:inline}
details.lvz>summary::before{content:"▸ ";color:var(--muted)}
details.lvz[open]>summary::before{content:"▾ "}
</style>
<script>
/* the FRUS document numbers, linked when their list is first opened */
function lvLink(d) {
  if (d.dataset.done) return;
  d.dataset.done = 1;
  d.querySelectorAll("span.lvg").forEach(function (s) {
    s.innerHTML = '<a href="https://history.state.gov/historicaldocuments/' + s.getAttribute("data-v") + '/d' +
      s.getAttribute("data-n") + '">' + s.innerHTML + '</a>';
  });
  d.querySelectorAll("span.lvf").forEach(function (s) {
    var v = s.getAttribute("data-v");
    s.innerHTML = s.textContent.trim().split(/\\s+/).map(function (n) {
      return '<a href="https://history.state.gov/historicaldocuments/' + v + '/d' + n + '">' + n + '</a>';
    }).join(", ");
  });
}
document.addEventListener("toggle", function (ev) {
  var d = ev.target;
  if (d.open && d.classList && d.classList.contains("lvz")) lvLink(d);
}, true);
/* the short lists, never folded, linked at once */
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".lv ul.lvb").forEach(function (u) {
    if (!u.closest("details.lvz")) lvLink(u);
  });
});
</script>"""


INTRO = ['<p class="lede">A name entry for each person in the series, the Executive roster, and the Congresses at '
         "their openings: the life, each fact with its source; then the person's publications and papers, the FRUS "
         "documents the person sent, the works on the person, and the FRUS and presidential documents that name the "
         "person.</p>",
         '<p class="logic">Sources: BD, the ' + to_html(BD_CITE) + ", by page; CDir., the *Congressional "
         "Directory*; CR, the *Congressional Record*; FR, the *Federal Register*; DSB, the *Department of State "
         "Bulletin*; GOM, the *Government Organization Manual*; Clerk, Election Statistics, the Clerk of the House's "
         "*Statistics of the Presidential and Congressional Election* of that year, by page; FRUS, by subseries, "
         "volume, and document; APP, the American Presidency Project (the Public Papers and the campaign "
         'documents). Pointers into the series: <span class="lvp">Exec.</span>, the Executive '
         'Branch at the term named; <span class="lvp">Cong.</span>, a Congress at its opening; '
         '<span class="lvp">Election</span>, the election\'s block; <span class="lvp">Cal.</span>, the '
         "calendar.</p>"]
INTRO = [re.sub(r"\*([^*]+)\*", r"<i>\1</i>", x) for x in INTRO]      # the series' *Title* as italics


def letter_of(p):
    return (fold(p["sur"])[:1] or "x").lower()


def page(series, linker, template, names):
    """One page for the persons named ('Humphrey, Hubert H.')."""
    from .congress import Pointers
    ptrs = Pointers(series, linker)
    main = ["<h1>Lives</h1>"] + INTRO + [entry(series, linker, ptrs, n) for n in names]
    return wrap(template, "Lives", main)


def wrap(template, title, main):
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", title).replace("{{main}}", "\n".join(main))
    return pg.replace("</body>", CSS + "\n</body>", 1)


def pages(series, linker, template):
    """{file name: html}: lives.html, the index of names by letter; lives-a.html ... lives-z.html, the entries."""
    from .congress import Pointers
    global SITE
    ptrs = Pointers(series, linker)
    everyone = cached("people", lambda: people(series))
    by_letter = {}
    for p in everyone:
        by_letter.setdefault(letter_of(p), []).append(p)
    out = {}
    index = ["<h1>Lives</h1>"] + INTRO + [f'<p class="logic">{len(everyone):,} persons.</p>']
    nav = " ".join(f'<a class="lvp" href="lives-{L}.html">{L.upper()}</a>' for L in sorted(by_letter))
    index.append(f'<p class="lvs">{nav}</p>')
    for L in sorted(by_letter):
        ps = by_letter[L]
        index.append(f'<h2 id="{L}" data-short="{L.upper()}">{L.upper()}</h2><ul class="lvx">' + "".join(
            f'<li><a href="lives-{L}.html#{key_of(p["name"])}">{esc(p["name"])}</a></li>' for p in ps) + "</ul>")
        main = [f"<h1>Lives: {L.upper()}</h1>", f'<p class="lvs">{nav} · <a class="lvp" href="lives.html">Index</a></p>']
        for p in ps:
            try:
                main.append(entry(series, linker, ptrs, p))
            except Exception as ex:          # one entry's fault names the person and does not stop the page
                import traceback
                print(f"lives: {p['name']}: {ex!r}", traceback.format_exc().splitlines()[-3], file=sys.stderr)
        out[f"lives-{L}.html"] = wrap(template, f"Lives: {L.upper()}", main)
    out["lives.html"] = wrap(template, "Lives", index)
    return out


PRIMARY = re.compile(r"Recording|Archive|Document|Record|Paper|Oral|Speech|Tape|Interview|Film|Screen")
# the sections of records (not the portrayals, Part I): what they hold that names a person is his record
RECORD_SEC = re.compile(r"^(?!.*Portrayal).*(Recording|Archive|Document|Record|Paper|Oral|Speech|Tape|Interview)")


def series_works(series, linker, ptrs, name, subs=None, strict=False):
    """[(kind, citation html, pointer html)] for every citation in the series that is by or names the person:
    kind 'own' (the person's work), 'primary' (the person's speech, recording, or papers: an entry in a section
    of documents, recordings, or archives), or 'about'."""
    sur, given = split_name(name)
    out, seen = [], set()
    hits = []
    for l, s, e in subs:
        if e["id"] not in seen and not (s.code or "").startswith("III"):
            seen.add(e["id"])
            hits.append((l, s, e, True))
    q = [fold(x) for x in ([f"{given.split()[0]} {sur}", f"{sur}, {given.split()[0]}", f"{given} {sur}"]
                                 if given else [sur])]
    def make():
        """Every entry outside Part III and the calendar, with its folded text, indexed by its words."""
        idx = {}
        for l in series.lists.values():
            if l.kind == "calendar":
                continue
            for s, e in l.entries():
                if (s.code or "").startswith("III"):
                    continue
                txt = fold(plain(" ".join(store.as_list(e.get("c"))) + " " + (e.get("n") or "") + " " + (e.get("s") or "")))
                row = (l, s, e, txt, " ".join(x.title for x in chain(s)))
                for w in set(re.findall(r"[a-z]+", txt)):
                    idx.setdefault(w, []).append(row)
        return idx
    words = re.findall(r"[a-z]+", fold(sur))
    # a son whose father, written bare, has his own entry: only the entries whose subject is the son
    for l, s, e, txt, sec in ([] if strict else cached("works", make).get(words[-1] if words else "", [])):
        if True:
            if e["id"] in seen:
                continue
            if any(x in txt for x in q):
                seen.add(e["id"])
                hits.append((l, s, e, False))
            elif PRIMARY.search(sec) and \
                    re.search(r"\b" + re.escape(fold(sur)) + r"(?:s| papers)\b", txt):
                seen.add(e["id"])        # an archive holding the person's papers ('Humphrey's papers')
                hits.append((l, s, e, "papers"))
    for l, s, e, subject in hits:
        sec = " ".join(x.title for x in chain(s))
        ptr_html = ptr(f"{SITE}{l.key}.html#{e['id']}", f"{esc(l.abbr)} {esc(s.code or s.id)}")
        if subject == "papers":
            out.append(("primary", esc(e.get("s") or ""), f" {to_html(e['n'])}" if e.get("n") else "", ptr_html))
            continue
        cs = store.as_list(e.get("c"))
        prev = None                      # the author a title-first line continues ('*Flawed Giant*' after Dallek)
        for i, c in enumerate(cs):
            author = author_of(c)
            if author is None and i:
                author = prev
            prev = author if author is not None else prev
            kind = work_kind(c, author, sur, bool(subject), sec, given)
            if kind != "own" and not any(x in fold(plain(c)) for x in q) and not (subject and kind):
                continue           # another work in the same entry
            if not kind:
                continue
            note = f" {to_html(e['n'])}" if e.get("n") and len(cs) == 1 else ""
            out.append((kind, to_html(c), note, ptr_html))
    return out


def chain(s):
    while s is not None:
        yield s
        s = s.parent


RECORDS = re.compile(r"\b(Tapes|Recordings?|Papers|Diary|Diaries|Letters|Speeches|Press Conferences|Transcripts?)\b")


def author_of(c):
    """The author a citation names before its title ('Robert Dallek, *Flawed Giant*'), or None where it opens with
    the title ('*Taking Charge*', '*Flawed Giant*' continuing the line above)."""
    if c.lstrip().startswith(("*", "'", "\"", "“")):
        return None
    # a name, then the title or what it is: 'Robert Dallek, *Flawed Giant*'; 'Lyndon B. Johnson, address to a joint
    # session (Nov. 27, 1963)'; not 'Speech to Am. Friends of Viet., June 1956, *in* ...'
    nm = r"[A-Z][\w'’.\-]*(?: (?:[A-Z][\w'’.\-]*|de|van|von|du|la))*(?:,? (?:Jr|Sr)\.|,? I{2,3})?"
    m = re.match(rf"^({nm}(?: (?:&|and) {nm})*), ", plain(c))
    return m.group(1) if m and len(m.group(1).split()) <= 8 else None


def work_kind(c, author, sur, subject, sec, given=""):
    """'own', 'primary', 'about', or '' (not about the person). The person's own: a citation he is the author of, or
    one with no author in his own subject entry. A collection someone else edited ('Beschloss ed.') is not his: his
    tapes, papers and the like are primary sources; essays and remembrances are about him."""
    edited = re.search(r"\(([^()]*?) eds?\.,", plain(c)) if c.lstrip().startswith("*") else None
    if author is not None:
        if any(is_person(a, sur, given) for a in re.split(r" & | and |, ", author)):
            return "primary" if PRIMARY.search(sec) or not re.search(r"\*", c) else "own"
        # a recording, a document, an archive that names him is his record, whoever heads it (the CBS tour of the
        # White House, in which Kennedy appears; the Kennedy Library)
        return "primary" if RECORD_SEC.search(sec) else "about"
    if RECORD_SEC.search(sec) and not subject:
        return "primary"
    if edited and not (fold(sur) in fold(edited.group(1))):
        if subject and fold(sur) not in fold(plain(c).split("(")[0]):
            return "own"                 # his writings, collected by another: *The Strategy of Peace* (Nevins ed.)
        return "primary" if RECORDS.search(plain(c)) else "about"
    if subject:
        return "primary" if PRIMARY.search(sec) else "own"
    return "primary" if RECORDS.search(plain(c)) and fold(sur) in fold(plain(c)) else "about"


def is_person(a, sur, given):
    """'Lyndon Baines Johnson' and 'Lyndon B. Johnson' are the person; 'Jacqueline Kennedy' is not John F."""
    a = a.strip()
    if not a or fold(last_word(a)) != fold(sur):
        return False
    g = a[: a.rfind(last_word(a))].strip()
    return not g or not given or same_person(sur, given, sur, g) or nick(gtoks(given)[0], (gtoks(g) or [""])[0])


def by_date(items):
    """Citations in the order of their dates: the first parenthesis that gives a year ('(Jan. 20, 1961)', '(CBS
    Feb. 14, 1962)', '(Michael R. Beschloss ed., 1997)', '(3 vols., 1962–64)'), with its month and day where given;
    one without a date last."""
    mo = {m.lower(): i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "june", "july", "aug", "sept",
                                                     "oct", "nov", "dec"])}

    def key(x):
        t = re.sub(r"<[^>]+>", "", x)
        pp = re.match(r"Public Papers of the Presidents[^(]*\([^()]*?(\d{4})(?:[–-](\d{2,4}))?\)", t)
        if pp:                           # a President's Public Papers after his last speech: the year the set closed
            end = pp.group(2) or pp.group(1)
            return ((pp.group(1)[:4 - len(end)] + end) if len(end) < 4 else end, 13, 0)
        for inner in re.findall(r"\(([^()]*)\)", t):
            y = re.search(r"\b(1[5-9]\d\d|20\d\d)\b", inner)
            if y:
                m = re.search(r"\b(Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)[a-z]*\.?(?: (\d{1,2}))?", inner[:y.start()])
                return (y.group(1), mo[m.group(1).lower()] if m else 0, int(m.group(2) or 0) if m else 0)
        return ("9999", 0, 0)
    return sorted(items, key=key)


def grouped(items):
    """Citations of the same work (by its title in italics) on one line, with every pointer."""
    by, order = {}, []
    for kind, c, note, ptr in items:
        m = re.search(r"<i>(.*?)</i>", c)
        k = fold(re.sub(r":.*", "", m.group(1))) if m else c
        if k not in by:
            by[k] = [c, note, []]
            order.append(k)
        if len(c) > len(by[k][0]):
            by[k][0] = c
        if note and not by[k][1]:
            by[k][1] = note
        by[k][2].append(ptr)
    return [f'{by[k][0]}.{by[k][1]} <span class="lvc">{"; ".join(dict.fromkeys(by[k][2]))}</span>' for k in order]




# ---------------------------------------------------------------- who has an entry

CONG = re.compile(r"\b(Senators?|Senate|Representatives?|House|Congress|Speaker|Rep\.|Sen\.|Whip|Leader)\b")


def people(series):
    """Everyone with an entry: the persons of Part III, the Executive roster's holders, and the members of Congress at
    each opening, one a person. Two names are one person where the surnames agree and the given names are
    compatible ('Hubert H.' and 'Hubert H., Jr.'; not 'Hubert' and 'Harold'). The name shown: Part III's form, else
    the roster's, else the Congress roster's."""
    from . import executive as X
    cands = []                           # (name, source rank)
    role = {}                            # Part III name -> its roles and section titles
    office = {}                          # roster name -> its offices' titles and units
    full = {}                            # roster name -> its full given names ('Ellsworth, Robert': 'Robert Fred')
    words = lambda t: set(re.findall(r"[a-z]{4,}", fold(t))) - STOP
    for l in series.lists.values():
        for s, e in l.entries():
            if (s.code or "").startswith("III") and e.get("s") and "," in e["s"]:
                for n in re.split(r";\s*", e["s"]):          # 'Dirksen, Everett M.; Kuchel, Thomas H.': two
                    n = re.sub(r"\s*\(.*?\)\s*$", "", n).strip()
                    if "," in n:
                        cands.append((n, 0))
                        role[n] = role.get(n, "") + " " + (e.get("r") or "") + " " + " ".join(x.title for x in chain(s))
    for u in X.load().values():
        for o in u.get("offices") or []:
            for h in o.get("holders") or []:
                cands.append((h["name"], 1))
                office[h["name"]] = office.get(h["name"], "") + f" {X.title_at(o, h['from'])} {h.get('title') or ''} {u.get('name') or ''}"
                if h.get("given"):
                    full.setdefault(h["name"], h["given"])
    for f in sorted(os.listdir(os.path.join(store.ROOT, "congress"))):
        if re.match(r"\d\d\.yaml$", f):
            d = store.load_yaml(os.path.join(store.ROOT, "congress", f)) or {}
            for r in (d.get("house") or []) + (d.get("senate") or []):
                if r.get("name"):
                    cands.append((r["name"], 2))
    def one(a, ra, b, rb):
        """Names a and b (from sources ra, rb) are one person: compatible with each other (every name the person
        has, so 'J. Skelly' and 'Jim' do not join through 'James'), and their suffixes agree. 'Jr.' and none may
        join across sources (Part III writes 'Humphrey, Hubert H.'; the rosters, 'Humphrey, Hubert H., Jr.'); two
        suffixes that differ never join (James L. Holloway, Jr., and III)."""
        if a == b:
            return True
        # the roster's full given names stand for its initials ('Robert' is 'Robert Fred'; 'Jim' is 'James Robert')
        ga, gb = full.get(a) or split_name(a)[1], full.get(b) or split_name(b)[1]
        if not (same_person(*split_name(a), *split_name(b)) or same_person(split_name(a)[0], ga, split_name(b)[0], gb)):
            return False
        A, B = gtoks(ga), gtoks(gb)
        paren = {fold(x) for x in re.findall(r"\(([^)]+)\)", a + " " + b)}
        in_cong = lambda n, r: r == 0 and CONG.search(role.get(n, ""))
        if A[0] != B[0] and not (len(A[0]) == 1 or len(B[0]) == 1):
            # by a short form ('Bob' and 'Robert'): where the roster gives it ('Robert C. (Bob)'), or both give
            # the middle initial, or Part III's man of that name sat in Congress and the other is a member
            if not (paren & {A[0], B[0]} or (len(A) > 1 and len(B) > 1)
                    or (in_cong(a, ra) and rb == 2) or (in_cong(b, rb) and ra == 2)):
                return False
        if (len(A) == 1) != (len(B) == 1) and ra != rb:
            # a bare name and a fuller one ('Anderson, Jack' and 'Anderson, Jack Z.'): Part III's role shares a
            # word with the roster's office, or Part III's man sat in Congress and the other is a member
            # a roster name Part III also writes takes Part III's word for it
            (n0, r0), (n1, r1) = sorted(((a, 0 if a in role else ra), (b, 0 if b in role else rb)), key=lambda x: x[1])
            if r0 == r1 == 0:
                pass
            elif r0 == 0 and r1 == 1:
                if role.get(n0, "").strip() and not words(role[n0]) & words(office.get(n1, "")):
                    return False
            elif r0 == 0 and r1 == 2:
                # or the member's Directory entry gives Part III's role ('Governor of Oklahoma')
                if not in_cong(n0, r0) and not paren & {A[0], B[0]}:
                    e = bd_entry(*split_name(n1), True, (), suffix(n1))
                    if not (e and len(words(role.get(n0, "")) & words(e["text"])) >= 2):
                        return False
            else:                        # the Executive roster and the Congress rosters: initials both, or none
                return False
        sa, sb = suffix(a), suffix(b)
        real = lambda x: x not in ("", "Sr")
        if real(sa) and real(sb) and sa != sb:
            return False
        if ra != rb:
            return True
        # within one source. The Congress rosters write each member one way: two names are two members (Charles
        # Wilson and Charles H. Wilson). Part III may drop a middle initial (Clark Clifford, Clark M. Clifford) but
        # writes a suffix every time. The Executive roster may drop a suffix but not an initial (Philip M. and
        # Philip M., Jr.; not Robert and Robert B. Anderson).
        if ra == 2:
            return False
        if ra == 0:
            return sa.replace("Sr", "") == sb.replace("Sr", "") and A[0] == B[0]
        return len(A) == len(B) and all(x == y or (len(x) == 1 and y.startswith(x)) or (len(y) == 1 and x.startswith(y))
                                        for x, y in zip(A, B))

    by_sur, out = {}, []
    # a name as written is one person in every source; then names written differently join, a suffixed name first
    exact = {}
    for name, rank in cands:
        exact.setdefault(name, set()).add(rank)
    for name, ranks in sorted(exact.items(), key=lambda x: (min(x[1]), suffix(x[0]) in ("", "Sr"), x[0])):
        sur, given = split_name(name)
        if not given:
            continue
        mine = {(name, r) for r in ranks}
        group = by_sur.setdefault(fold(sur), [])
        hit = next((p for p in group if all(one(a, ra, b, rb) for a, ra in mine for b, rb in p["ranks"])), None)
        if hit:
            hit["names"].add(name)
            hit["ranks"] |= mine
            continue
        p = {"name": name, "sur": sur, "given": given, "names": {name}, "ranks": mine}
        group.append(p)
        out.append(p)
    return sorted(out, key=lambda p: (fold(p["sur"]), fold(p["given"])))
