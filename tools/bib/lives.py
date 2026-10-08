"""Names: a name entry for each person, gathered from the series' own files. build/names.html.

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
SERIES_FOR_LINKS = None   # the series, once the pages are being written: the record tables link the other candidates
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


def bd_entry(sur, given, member=True, words=(), sfx="", alive=None):
    """The Directory's entry for the person. The member lived into the period (the entry's latest year 1953 or
    later, and no death before 1953 or before alive, the first day the series shows the person: a seat at an
    opening, an office), so a namesake of the last century or a father is not taken ('Dingell, John D.' of the
    87th is not the John David Dingell who died in 1955). Of several, the one whose service spans that first day,
    then the one whose given names agree most fully ('Albert W.' is Albert Walter Johnson, not Washington's Albert
    Johnson). A member of Congress at an opening may match by a
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
        if not ok:
            # the middle name he went by ('Brooks Hays', 'Lawrence Brooks'); anyone else needs the words too (below)
            A, B = gtoks(given), gtoks(g)
            ok = len(A) == 1 and any(A[0] == b or nick(A[0], b) for b in B[1:])
        if ok and not member:
            bw = set(re.findall(r"[a-z]{4,}", fold(e["text"])))
            if re.search(r"\bPresident of the United States\b", re.split(r";\s*born\b", e["text"], 1)[0]):
                bw.add("@president")
            ok = bool(set(words) & bw)
        d = death_day(e)
        if ok and d and d < max("1953-01-01", alive or ""):
            ok = False
        if ok:
            A, B = gtoks(given), gtoks(g)
            score = sum(1 for a, b in zip(A, B) if a == b or (len(a) == 1 and b.startswith(a)) or
                        (len(b) == 1 and a.startswith(b)))
            # first, the one whose service spans the first day the series shows him (John James Duncan sat at the
            # 89th's opening, not his son John J.)
            if alive and any(x is e and ((ch_, congress_of(alive)) in wins or any(f <= alive < t for f, t in spans))
                             for x, _, seats, spans, wins in bd_service().get(fold(sur), []) for ch_ in "hs"):
                score += 100
            if not best or score > best[0]:
                best = (score, e)
    return best and best[1]


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


def person_words(sur, given, names=None, roles=""):
    """The distinctive words of the person's offices in the roster and his roles in Part III ('Governor of
    Arkansas'), for matching the Directory; '@president' for the President or Vice President, which the Directory
    gives in its head ('35th President of the United States')."""
    from . import executive as X
    hs = [(o, h) for u, o, h in holders_of(sur)
          if (h["name"] in names if names else same_person(*split_name(h["name"]), sur, given))]
    t = roles
    for o, h in hs:
        t += f"\n{X.title_at(o, h['from'])} {h.get('title') or ''}"
    w = set(re.findall(r"[a-z]{4,}", fold(t))) - STOP
    if re.search(r"^\s*(?:Vice )?President(?:,|\s*$| of the United States)", t, re.M):
        w.add("@president")
    return w


def part3_roles(series, names):
    """Part III's role lines for the person's names, each on its own line."""
    def make():
        idx = {}
        for l in series.lists.values():
            for sec, e in l.entries():
                if (sec.code or "").startswith("III") and e.get("s"):
                    for n in re.split(r";\s*", e["s"]):
                        n = re.sub(r"\s*\(.*?\)\s*$", "", n).strip()
                        idx[n] = idx.get(n, "") + "\n" + (e.get("r") or "")
        return idx
    return "".join(cached("part3-roles", make).get(n, "") for n in names)


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
        # the first term whose table holds the office and him (a unit begun later: the PSAC chair before 1957)
        i = next((j for j in range(i, len(X.TERMS)) if X.exists(u, *X.term_span(j)) and X.exists(o, *X.term_span(j))
                  and X.in_term(h, *X.term_span(j))), None)
        if i is None:
            return ext, []
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


def returns_given(n):
    """The given names of a name as the returns print it: 'Harry F. Byrd Jr.' -> 'Harry F.'."""
    ws = [w for w in re.sub(r",", " ", n).split() if not re.fullmatch(r"(Jr|Sr|II|III|IV)\.?", w)]
    return " ".join(ws[:-1])


def letters(s):
    """The letters alone, folded: 'St. Germain' and 'St Germain', 'du Pont' and 'DuPont' agree."""
    return re.sub(r"[^a-z]", "", fold(s))


def returns_split(n, sur):
    """(given names, suffix) of a name as the returns print it, where its surname is sur ('William Van Pelt',
    'Pierre S. DuPont IV', 'Fernand St Germain'); None where it is not."""
    m = re.search(r",? (Jr|Sr|II|III|IV)\.?$", n or "")
    ws = (n[:m.start()] if m else (n or "")).replace(",", " ").split()
    for k in (1, 2, 3):
        if len(ws) > k and letters(" ".join(ws[-k:])) == letters(sur):
            return " ".join(ws[:-k]), (m.group(1) if m else "")
    return None


def returns_suffix(n):
    """'Harry F. Byrd Jr.' -> 'Jr'; '' where none, or Sr."""
    m = re.search(r",? (Jr|II|III|IV)\.?$", n)
    return m.group(1) if m else ""


def roster_given():
    """{the roster's name: its full given names} ('Beall, James G.': 'James Glenn'), 87th to 93rd."""
    def make():
        idx = {}
        for f in sorted(os.listdir(os.path.join(store.ROOT, "congress"))):
            if re.match(r"\d\d\.yaml$", f):
                d = store.load_yaml(os.path.join(store.ROOT, "congress", f)) or {}
                for r in (d.get("senate") or []) + (d.get("house") or []):
                    if r.get("name") and r.get("given"):
                        idx.setdefault(r["name"], r["given"])
        return idx
    return cached("roster-given", make)


def seat_holders():
    """{(Congress, chamber, State, district or class): [the roster's names]} at each opening, 87th to 93rd (an
    at-large seat, 0, holds several)."""
    def make():
        idx = {}
        for f in sorted(os.listdir(os.path.join(store.ROOT, "congress"))):
            m = re.match(r"(\d\d)\.yaml$", f)
            if m:
                d = store.load_yaml(os.path.join(store.ROOT, "congress", f)) or {}
                for ch, rows in (("s", d.get("senate") or []), ("h", d.get("house") or [])):
                    for r in rows:
                        if r.get("name"):
                            idx.setdefault((int(m.group(1)), ch, r["st"], r.get("cl") if ch == "s" else r.get("d", 0)),
                                           []).append(r["name"])
        return idx
    return cached("seat-holders", make)


DATE = r"(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}),? (\d{4})"


ORD_UNITS = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
             "ninth": 9, "tenth": 10, "eleventh": 11, "twelfth": 12, "thirteenth": 13, "fourteenth": 14,
             "fifteenth": 15, "sixteenth": 16, "seventeenth": 17, "eighteenth": 18, "nineteenth": 19}
ORD_TENS = {"twentieth": 20, "thirtieth": 30, "fortieth": 40, "fiftieth": 50, "sixtieth": 60, "seventieth": 70,
            "eightieth": 80, "ninetieth": 90, "hundredth": 100}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
UNITS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
         "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
         "eighteen": 18, "nineteen": 19}
ORD_RX = r"\b(?:One Hundred(?:th)? )?[A-Z][a-z]+(?:-[a-z]+)?"


def ordinal_number(w):
    """'Sixty-third' 63, 'One Hundred First' 101, 'One Hundredth' 100; None for anything else."""
    w = w.lower().strip()
    n = 0
    if w.startswith("one hundredth"):
        return 100
    if w.startswith("one hundred "):
        n, w = 100, w[len("one hundred "):]
    if "-" in w:
        t, u = w.split("-", 1)
        return n + TENS[t] + ORD_UNITS[u] if t in TENS and u in ORD_UNITS else None
    v = ORD_UNITS.get(w) or ORD_TENS.get(w)
    return n + v if v else None


def cardinal_number(w):
    """'twenty-four' 24, 'two' 2; None for anything else."""
    w = w.lower()
    if "-" in w:
        t, u = w.split("-", 1)
        return TENS[t] + UNITS[u] if t in TENS and u in UNITS else None
    return UNITS.get(w) or TENS.get(w)


def bd_wins(text):
    """{(chamber, Congress)}: the Congresses the Directory says the member was elected to: 'elected ... to the
    Sixty-third and to the twenty-four succeeding Congresses', 'reelected to the six succeeding Congresses', 'elected
    to the United States Senate in 1952; reelected in 1958' (a Senate year is the race that chose the next Congress).
    Clauses of unsuccessful candidacies aside; a clause without 'Senate' keeps the chamber of the one before."""
    out, ch, last = set(), "h", None
    for cl in text.split(";"):
        if re.search(r"unsuccessful|not a candidate|candidate for", cl) or not re.search(r"\b(?:re)?elected\b", cl):
            continue
        if "Senate" in cl:
            ch = "s"
        elif "Congress" in cl:
            ch = "h"
        if re.search(r"\bSpeaker\b|\bchair", cl):
            continue
        nums = [n for n in (ordinal_number(m) for m in re.findall(ORD_RX, cl)) if n]
        if "Congress" in cl and nums:
            for n in nums:
                out.add((ch, n))
            last = max(nums)
        m = re.search(r"\bto the (?:([a-z]+(?:-[a-z]+)?) )?succeeding Congress", cl)
        if m and last:
            k = cardinal_number(m.group(1)) if m.group(1) else 1
            if k:
                for n in range(last + 1, last + k + 1):
                    out.add((ch, n))
                last += k
        head = re.split(r"\bserved\b|\bwhen\b", cl, 1)[0]
        if ch == "s" and not ("Congress" in cl and nums) and ("Senate" in cl or re.match(r"\s*re-?elected in", cl)) \
                and not re.search(r"\bPresident\b|\bGovernor\b", head):
            bare = re.sub(DATE, "", head)
            for y in re.findall(r"\b(?:in|and|again in)\s+(19\d\d|20\d\d)\b|,\s*(19\d\d|20\d\d)\b", bare):
                y = int(y[0] or y[1])
                out.add(("s", (y - 1788) // 2 + 1))
    return out


def bd_service():
    """{surname: [(entry, given names, {(chamber, State)}, [(from, to)])]}: whom the Directory seats from which State,
    and when, for the entries of the period. The chambers and States from the entry's head ('a Representative and a
    Senator from Massachusetts'); the spans from each clause that gives service from one full date to another or to
    'present' ('served from January 3, 1953 to December 22, 1960'; '(January 3, 1965-present)'); 'unsuccessful
    candidate' clauses aside. A span without its closing date is left out (the Directory's 'January 3,)')."""
    from .congress import STATE
    states = sorted(((v, k) for k, v in STATE.items()), key=lambda x: -len(x[0]))

    def make():
        idx = {}
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            for e in letter_json("bd", letter):
                m = re.match(r"([^,(]+), ([^(,]+)", e["name"])
                if not m:
                    continue
                yrs = [int(y) for y in re.findall(r"\b(1[789]\d\d|20\d\d)\b", e["text"])]
                if not yrs or max(yrs) < 1953:
                    continue
                head = re.split(r";\s*born\b", re.sub(r"\([^)]*\)", "", e["text"]), 1)[0]
                seats = set()
                for kind, kind2, rest in re.findall(r"\b(Representative|Senator|Delegate)(?: and a (Representative|Senator))? from "
                                                    r"([A-Z][^;]*)", head):
                    st = next((k for v, k in states if rest.startswith(v)), None)
                    for k_ in (kind, kind2):
                        if k_ and st:
                            seats.add(("s" if k_ == "Senator" else "h", st))
                spans = []
                for cl in e["text"].split(";"):
                    if re.search(r"unsuccessful|candidate", cl) or not re.search(r"served from|Congress|\(", cl):
                        continue
                    ds = [f"{y}-{FULL[mo]:02d}-{int(d):02d}" for mo, d, y in re.findall(DATE, cl)]
                    if "present" in cl and ds:
                        spans.append((ds[0], "9999"))
                    elif len(ds) >= 2:
                        spans.append((ds[0], ds[-1]))
                wins = bd_wins(e["text"])
                if seats and (spans or wins):
                    idx.setdefault(fold(m.group(1).strip()), []).append((e, m.group(2).strip(), seats, spans, wins))
        return idx
    return cached("bd-service", make)


def bd_winner(sur, n, ch, st, opened):
    """The Directory's member who won the race: the one entry of the surname whose given names agree with the
    returns' ('Lester Johnson': Lester Roland Johnson), who sat for the State in the chamber, and whose service
    spans the opening of the Congress the race chose. None where no entry or more than one answers."""
    cg = returns_given(n)

    def agree(g):                        # or by the middle name he went by ('Hale Boggs': Thomas Hale)
        A, B = gtoks(cg), gtoks(g)
        return same_person(sur, g, sur, cg) or (len(A) == 1 and any(A[0] == b or nick(A[0], b) for b in B[1:]))
    hits = {e["name"]: e for e, g, seats, spans, wins in bd_service().get(fold(sur), [])
            if (ch, st) in seats and agree(g)
            and ((ch, congress_of(opened)) in wins or any(f <= opened < t for f, t in spans))}
    return next(iter(hits.values())) if len(hits) == 1 else None   # (an entry printed twice is one)


def bd_names_agree(bd, sur, g):
    """The returns' given names agree with the Directory's full ones ('George B.' is not George Lloyd Murphy), or
    name the middle name he went by ('Hale': Thomas Hale Boggs)."""
    bg = re.sub(r"\([^)]*\)|\[[^]]*\]", " ", re.match(r"[^,]+, ([^(]+)", bd["name"] + " ").group(1))
    bg = re.sub(r",?\s*\b(Jr|Sr|II|III|IV)\b\.?", "", bg).strip(" ,")
    nicks = re.findall(r"\(([A-Z][a-z]+)\)", bd["name"])
    A, B = gtoks(g), gtoks(bg)
    return (same_person(sur, bg, sur, g) or any(same_person(sur, k, sur, g) for k in nicks)
            or (len(A) >= 1 and any(A[0] == b or nick(A[0], b) for b in B[1:])))


def race_key(y, r):
    """A race as the hand files name it: the year, then the readings' key ('1962 h AL 0', '1962 s OR 2 special')."""
    pos = f"-{r['position']}" if r.get("position") else ""
    return f"{y} {r['ch']} {r['st']} {r.get('seat') or 0}{pos}" + (" special" if r.get("special") else "")


def renominations_by():
    """elections/renominations.yaml: {'<race key> | <incumbent>': {party, source}}, the renominations lost by primary
    where a source says so (kept by hand)."""
    def make():
        p = os.path.join(store.ROOT, "elections", "renominations.yaml")
        return {re.sub(r"\s*\|\s*", " | ", k): v for k, v in ((store.load_yaml(p) or {}).items() if os.path.exists(p) else [])}
    return cached("renominations", make)


def primaries():
    """elections/primaries.yaml: {race key: {page, footnote, rounds: [{label, cands: [[name, party, votes, share]]}]}},
    CQ's primary returns (kept by hand)."""
    def make():
        p = os.path.join(store.ROOT, "elections", "primaries.yaml")
        return (store.load_yaml(p) or {}) if os.path.exists(p) else {}
    return cached("primaries", make)


def same_candidate(a_, b_):
    """Two names in one race are one candidate: the surnames agree, and the first initials (suffixes aside: CQ prints
    'Harry F. Byrd Sr.', the returns 'Harry F. Byrd')."""
    ga, gb = returns_given(a_), returns_given(b_)
    return letters(last_word(a_)) == letters(last_word(b_)) and (not ga or not gb or fold(ga)[:1] == fold(gb)[:1])


def primary_rounds(key, name):
    """The rounds of the race's primaries (elections/primaries.yaml) that name the candidate: [(label, rows, me)]."""
    p = primaries().get(key) or {}
    out = []
    for rd in p.get("rounds") or []:
        me = next((c for c in rd["cands"] if same_candidate(c[0], name)), None)
        if me:
            out.append((rd["label"], rd["cands"], me))
    return out


def primary_cells(key, name):
    """The record's cells for the primary rounds that name the candidate, each under its label, the person in bold;
    then the label of the November vote. [] where none."""
    rs = primary_rounds(key, name)
    if not rs:
        return []
    lab = lambda s: f'<span class="lvpl">{esc(s)}</span>'
    cells = []
    for label, rows, me in rs:
        cells.append(lab(label))
        cells += [cand(c[0], c[1], (f"{c[2]:,}" if c[2] else "") + (f" ({c[3]:.1f}%)" if c[3] is not None else ""), c is me)
                  for c in rows]
    return cells + [lab("General election")]


def primary_cite(key):
    p = primaries().get(key)
    return f"CQ Guide 6th (2010) {p['page']}" if p else ""


def race_matches():
    """sources/race-matches.yaml: {person: {refuse: {race: why}, confirm: {race: why}}}, kept by hand."""
    def make():
        p = os.path.join(store.ROOT, "sources", "race-matches.yaml")
        return (store.load_yaml(p) or {}) if os.path.exists(p) else {}
    return cached("race-matches", make)


def congress_of(day):
    """The Congress sitting on a day ('1961-01-03' the 87th): the one whose first year is the odd year at or before
    it; Jan. 1 and 2 of an odd year still the one before."""
    y = int(day[:4]) - (1 if day[5:] < "01-03" else 0)
    return (y - 1789) // 2 + 1


def problems(series):
    """sources/race-matches.yaml: each person a name the series holds; each race a key the returns hold, with a
    candidate of his surname; none both refused and confirmed."""
    from .elections import load
    where = "sources/race-matches.yaml"
    names = {n for p in cached("people", lambda: people(series)) for n in p["names"]}
    keys = {}
    for y, d in sorted(load().items()):
        for r in (d or {}).get("races") or []:
            keys.setdefault(race_key(str(y), r), set()).update(fold(last_word(c["n"])) for c in r.get("cands") or []
                                                                if c.get("n"))
    for k, p in primaries().items():           # elections/primaries.yaml: a race the returns hold
        if k not in keys:
            yield "elections/primaries.yaml", f"{k}: no such race"
        for rd in (p or {}).get("rounds") or []:
            for c in rd.get("cands") or []:
                if len(c) != 4 or (c[2] is not None and not isinstance(c[2], int)):
                    yield "elections/primaries.yaml", f"{k}, {rd.get('label')}: {c}: [name, party, votes, share]"
    for n, v in race_matches().items():
        if n not in names:
            yield where, f"{n}: no person of that name"
            continue
        if not isinstance(v, dict) or set(v) - {"refuse", "confirm"}:
            yield where, f"{n}: only refuse: and confirm: maps"
            continue
        for k in set(v.get("refuse") or {}) & set(v.get("confirm") or {}):
            yield where, f"{n}: {k} both refused and confirmed"
        for k in list(v.get("refuse") or {}) + list(v.get("confirm") or {}):
            if k not in keys:
                yield where, f"{n}: no race {k}"
            elif fold(split_name(n)[0]) not in keys[k]:
                yield where, f"{n}: no candidate of the name in {k}"


def opening(cong):
    """The day the Congress first met: the roster's 'opened', else Jan. 3 of its first year."""
    p = os.path.join(store.ROOT, "congress", f"{cong}.yaml")
    if os.path.exists(p):
        d = cached(f"congress-{cong}", lambda: store.load_yaml(p) or {})
        if d.get("opened"):
            return str(d["opened"])
    return f"{1789 + 2 * (cong - 1)}-01-03"


def election_sentences(sur, given, sfx="", strict=False, givens=(), held=(), seated=(), names=(), bd=None, last=None):
    """The person's races, from elections/. A candidate's suffix as Wikipedia writes it ('Harry F. Byrd Jr.') agrees
    with the person's; one without a suffix is taken only where no namesake has an entry (strict: the person is the
    son, and the father, written bare, has his own).

    A race the name gives is refused only on certain grounds (refused, below) or by hand (sources/race-matches.yaml);
    one nothing confirms (confirmed, below) is shown with a Check. bd: the person's Directory entry; last: the last
    day the series shows him alive."""
    from .elections import rid as erid
    from .congress import STATE, BLUEBOOK
    out = []
    first = fold(given.split()[0]) if given else ""
    died = death_day(bd)
    hand = {}
    for n in names or ():
        for k, v in (race_matches().get(n) or {}).items():
            hand.setdefault(k, {}).update(v or {})

    gs_ = [g for g in givens if g] or [given]
    nicks_ = {fold(x) for n in names or () for x in re.findall(r"\(([A-Z][a-z]+)\)", n)}   # the rosters' "(Dan)"
    further = {t for g in gs_ for t in gtoks(g)[1:] if len(t) > 1}
    # the name he went by after an initial, as the series writes him ('Sanders, H. Barefoot', 'Beall, J. Glenn')
    goes_by = {gtoks(n_)[1] for n_ in [split_name(x)[1] for x in names or ()] + [given]
               if len(gtoks(n_)) > 1 and len(gtoks(n_)[0]) == 1 and len(gtoks(n_)[1]) > 1}

    def mine(n):
        """The returns' name is the person's by its surname and first given name: the first name, or a short form
        of it ('Dick Clark' for Richard C. (Dick) Clark), or the rosters' own short form ('Dan Daniel': Wilbur C.
        (Dan)); an initial with more names after it ('H. Carl Andersen', 'O. C. Fisher'); or a further given name he
        went by, where the series writes him by it ('Barefoot Sanders': H. Barefoot); or the first initial and a
        further given name spelled out, where his full given names (the rosters', or as written) spell it ('H. Carl
        Andersen': Herman Carl; 'J. Glenn Beall'). Initials alone ('J. C. Carter' is not Jimmy Carter) and a
        further name alone ('Andrew Young' is not John A. Young; 'Dale Alford') are left to the seat (below).
        The rest agree below (mine_race)."""
        sp = returns_split(n, sur) if n else None
        if not sp or not gtoks(sp[0]):
            return False
        g, cs = sp
        t = gtoks(g)
        w0 = t[0]
        if not (w0 == first or nick(w0, first) or w0 in nicks_ or w0 in goes_by
                or (len(w0) == 1 and first.startswith(w0) and len(t) > 1 and t[1] in further)):
            return False
        cs = "" if cs == "Sr" else cs
        return (cs == sfx or {cs, sfx} == {"Jr", "II"}) if cs else not strict

    def given_agrees(cg):
        """The returns' given names agree with one of the person's: as same_person; or the rosters' short form
        ('Dan'); or a further given name and what follows it ('Dale' in Thomas Dale, 'Melvin' in Charles Melvin)."""
        t = gtoks(cg)
        if not t:
            return False
        if any(same_person(sur, g, sur, cg) for g in gs_) or (t[0] in nicks_ and len(t) == 1):
            return True
        for g in gs_:
            G = gtoks(g)
            for k in range(1, len(G)):
                if G[k] == t[0] and len(G[k]) > 1:
                    rest = iter(x[0] for x in G[k + 1:])
                    if all(x[0] in rest for x in t[1:]):
                        return True
        return False

    def mine_race(c):
        """A candidate in a race for Congress is the person by name: the name (above), and the further given names
        agree where both give one ('John F.' is not Illinois's John A. Kennedy)."""
        n = c.get("n")
        return mine(n) and given_agrees(returns_split(n, sur)[0])

    def agrees(g):
        return any(same_person(sur, x, sur, g) for x in ([x for x in givens if x] or [given]))

    def refused(r, y, day, me, by_seat=False):
        """Certain grounds that the candidate is another man:
        - the race is after the person's death (Howard H. Baker, d. Jan. 7, 1964: the son's race);
        - the roster seats another man of the name from it, or seated him as its incumbent (Texas's Charles Wilson,
          not Eisenhower's Secretary of Defense);
        - the Directory's member who won it is another man: the person has his own entry, or the member's given
          names disagree with his (Lester Roland Johnson, not Lester D.), or the member died before the series last
          shows the person alive (Senator William Langer, d. 1959, not the historian);
        - he won while holding an executive office on the day the Congress met (Art. I, sec. 6, cl. 2: no person
          holding any office under the United States shall be a member of either House during his continuance in
          office).
        A race the roster's seat gives him (by_seat) is refused only by his death or an executive office."""
        cong = (int(y) - 1788) // 2 + 1
        if died and day > died:
            return "after his death"
        if by_seat:
            return "in executive office when the Congress met" if me.get("w") and any(
                f <= opening(cong) <= t for f, t in held) else None
        if bd and not bd_names_agree(bd, sur, returns_split(me["n"], sur)[0]):
            return "the Directory's given names disagree"
        inc = any(i.get("n") == me.get("n") for i in r.get("inc") or [])
        for k, cond in (((cong, r["ch"], r["st"], r.get("seat") or 0), me.get("w")),
                        ((cong - 1, r["ch"], r["st"], r.get("seat") or 0), inc)):
            for h in seat_holders().get(k) or []:
                hs, hg = split_name(h)
                sp = returns_split(me["n"], hs)
                if cond and h not in names and sp and any(same_person(hs, g_, hs, sp[0])
                                                          for g_ in (hg, roster_given().get(h) or hg)) \
                        and returns_suffix(me["n"]) in ("", suffix(h).replace("Sr", "")):
                    # (a 'Jr.' in the returns the holder lacks is the son: Harry F. Byrd Jr. in his father's seat,
                    # 1966; the returns may drop a holder's 'Jr.', never add one)
                    return f"the roster seats {h}"
        if me.get("w"):
            w = bd_winner(sur, me["n"], r["ch"], r["st"], opening(cong))
            if w and not (bd and w["name"] == bd["name"]):
                wg = re.match(r"[^,]+, ([^(,]+)", w["name"]).group(1).strip()
                if bd or not agrees(wg) or (death_day(w) and last and death_day(w) < last):
                    return f"the Directory's member is {w['name']}"
            if any(f <= opening(cong) <= t for f, t in held):
                return "in executive office when the Congress met"
        return None

    def confirmed(r, y, me):
        """The race is the person's on other evidence than the name: the roster seats him from it or seated him as
        its incumbent; the Directory's member who won it is his entry; his entry names a candidacy that year."""
        cong = (int(y) - 1788) // 2 + 1
        seat = r.get("seat") or 0
        inc = any(i.get("n") == me.get("n") for i in r.get("inc") or [])
        if (me.get("w") and set(seat_holders().get((cong, r["ch"], r["st"], seat)) or []) & set(names or ())) or \
                (inc and set(seat_holders().get((cong - 1, r["ch"], r["st"], seat)) or []) & set(names or ())):
            return True
        if bd and me.get("w"):
            w = bd_winner(sur, me["n"], r["ch"], r["st"], opening(cong))
            if w and w["name"] == bd["name"]:
                return True
        return bool(bd) and any(y in cl and "candidate" in cl for cl in bd["text"].split(";"))

    def rostered():
        return cached("rostered", lambda: {k[0] for k in seat_holders()})

    def by_year():
        return cached("elections-by-year", lambda: dict(cached("elections", make)))

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
                        rs = idx.setdefault(letters(last_word(c["n"])), {}).setdefault(y, [])
                        if i not in rs:
                            rs.append(i)
            for c in (d.get("president") or {}).get("cands") or []:
                if c.get("n"):
                    idx.setdefault(letters(last_word(c["n"])), {}).setdefault(y, []).append(-1)
            from . import elections as E
            pf = E.facts().get("president") or {}
            vn = list(((pf.get("vice") or {}).get(int(y)) or {}).values())
            vn += [n for split in ((pf.get("vice_cast") or {}).get(int(y)) or {}).values() for n in split]
            for n in vn:                 # the running mates
                idx.setdefault(letters(last_word(n)), {}).setdefault(y, []).append(-1)
        return idx
    def renominations(r, y, d, cong, url):
        """The incumbent who lost renomination: not among the November candidates, named in the race's fates (Wikipedia's
        race tables). He is the person where the roster seated him from the State at the last opening (a redistricting
        contest moves him); else by name, with a Check. The fate as written ('Lost renomination in a redistricting
        contest'); whether by primary or convention the fate does not say."""
        res_ = []
        if not any("renomination" in (i.get("result") or "").lower() for i in r.get("inc") or []):
            return res_
        sat = {n_ for (c_, ch_, st_, s_), ns in seat_holders().items() if (c_, ch_, st_) == (cong - 1, r["ch"], r["st"])
               for n_ in ns} & set(names)
        for i in r.get("inc") or []:
            fate = i.get("result") or ""
            if "renomination" not in fate.lower() or not returns_split(i.get("n") or "", sur):
                continue
            if any(c.get("n") == i.get("n") for c in r.get("cands") or []):
                continue                         # he ran in November all the same: the race's own row says how
            if not (sat or mine_race(i)) or (died and d["date"] > died):
                continue
            key = race_key(y, r)
            if key in hand.get("refuse", {}):
                continue
            check = not (sat or key in hand.get("confirm", {}))
            what = re.sub(r"^Incumbent\s+", "", fate.split(". ")[0].split(";")[0]).strip().rstrip(".")
            what = what[:1].upper() + what[1:]
            by = renominations_by().get(f"{key} | {i.get('n')}")   # by primary, where a source says so
            rounds = primary_rounds(key, i.get("n") or "")
            if by and what == "Lost renomination":
                what += f" in the {by['party']} " + ("runoff" if rounds and "runoff" in rounds[-1][0].lower() else "primary")
            figs = ""
            if rounds:                           # the round he lost, as CQ prints it
                _, rows_, me_ = rounds[-1]
                others_ = "; ".join(f"{esc(c[0])} ({c[1]}) {c[2]:,}" for c in rows_ if c is not me_ and c[2])
                figs = (f": {me_[2]:,} votes ({me_[3]:.1f} percent)" if me_[2] else "") + (f"; {others_}" if others_ else "")
            where = STATE.get(r["st"], r["st"])
            seat_ = "Senate, " + where if r["ch"] == "s" else f"House, {r['st']}-{r['seat'] or 'AL'}"
            wiki = f"https://en.wikipedia.org/wiki/{y}_United_States_{'Senate' if r['ch'] == 's' else 'House_of_Representatives'}_elections"
            src = a(wiki, f"Wikipedia, {y} {'Senate' if r['ch'] == 's' else 'House'} elections")
            if by and by.get("source", "").startswith("Wikipedia: "):
                art = by["source"][len("Wikipedia: "):]
                src += "; " + a("https://en.wikipedia.org/wiki/" + art.replace(" ", "_"), f"Wikipedia, {esc(art)}")
            cs = r.get("cands") or []
            tot = sum(c.get("v") or 0 for c in cs) + (r.get("scat") or 0)
            if rounds:
                src += "; " + primary_cite(key)
            res_.append(sent(d["date"], f"{what}: {seat_}, {y}{figs}.", [src],
                             [ptr(f"{SITE}congress.html#{erid(y, r)}", f"Election {y}")], para=True, kind="election",
                             dates={d["date"]}))
            res_[-1]["row"] = {
                "cong": cong, "ch": r["ch"], "st": r["st"], "date": d["date"],
                "election": ptr(f"{SITE}congress.html#{erid(y, r)}", fmt(d["date"])),
                "seat": f"Senate, {BLUEBOOK.get(r['st'], r['st'])}" if r["ch"] == "s" else
                        f"{BLUEBOOK.get(r['st'], r['st'])}-{r['seat'] or 'AL'}",
                "result": what,
                # the nominees who ran in November
                "cands": [cand(c["n"], c.get("p"), (f"{c['v']:,}" + (f" ({pct(c['v'], tot)})" if tot else "")) if c.get("v")
                               else "") for c in sorted(cs, key=lambda c: -(c.get("v") or 0))],
                "cnames": [c["n"] for c in sorted(cs, key=lambda c: -(c.get("v") or 0))],
                "src": src + ("; Check: matched by name only" if check else ""),
                "key": key, "check": check, "n": i.get("n"), "renomination": True,
                "pre": primary_cells(key, i.get("n") or "")}
        return res_

    def special_rows():
        """The specials held between general elections (congress/specials.yaml, the States' and CQ's figures laid
        over), by the same rules: the name; the seat (the winner of the surname whom the roster seats from it at
        the next opening)."""
        from . import specials as SP
        res = []
        def index():
            """{letters of a candidate's last word: [(Congress, special, its final rows)]}"""
            loaded, idx = SP.load(), {}
            for c_ in sorted(loaded):
                for x in SP.between(c_, loaded):
                    rows = SP.final(x)
                    for k in {letters(last_word(r_[0])) for r_ in rows}:
                        idx.setdefault(k, []).append((c_, x, rows))
            return idx
        idx = cached("specials-by-name", index)
        found = []
        for k in dict.fromkeys((letters(last_word(sur)), letters(sur))):
            found += [t for t in idx.get(k, []) if t not in found]
        for c_, x, rows in found:
            if True:
                if not any(returns_split(r_[0], sur) for r_ in rows):
                    continue
                me = next((r_ for r_ in rows if mine_race({"n": r_[0]})), None)
                by_seat = False
                nxt = set(seat_holders().get((c_ + 1, x["ch"], x["st"], x["seat"])) or []) & set(names or ())
                hit = [r_ for r_ in rows if r_[4] and nxt and returns_split(r_[0], sur)]
                if len(hit) == 1 and (me is None or me is hit[0]):
                    me, by_seat = hit[0], True
                if not me:
                    continue
                if died and x["date"] > died:
                    continue
                if x["key"] in hand.get("refuse", {}):
                    continue
                check = not (by_seat or x["key"] in hand.get("confirm", {}))
                won = me[4]
                where = STATE.get(x["st"], x["st"])
                seat_ = "Senate" if x["ch"] == "s" else f"House, {x['st']}-{x['seat'] or 'AL'}"
                tot = sum(r_[2] or 0 for r_ in rows)
                votes = (f": {me[2]:,} votes ({100 * me[2] / tot:.1f} percent)" if me[2] and tot else
                         f": {me[3]:.1f} percent" if me[3] is not None else "")
                others = ", ".join(f"{esc(r_[0])} ({r_[1]}) " + (f"{r_[2]:,}" if r_[2] else f"{r_[3]:.1f}%" if r_[3] is not None else "")
                                   for r_ in rows if r_ is not me and r_[0] != "Scattering")
                t = (f"{'Elected' if won else 'Defeated'} {'to' if won else 'for'} the {seat_}"
                     f"{', ' + where if x['ch'] == 's' else ''} in {'the State' + chr(39) + 's first election' if x.get('new') else 'a special election'}, {fmt(x['date'])}{votes}"
                     + (f"; {others}" if others else "") + ".")
                from .congress import ordinal as ord_
                cite = re.sub(r"[*]([^*]+)[*]", r"<i>\1</i>", esc(x.get("source") or ""))
                src = a(x["url"], cite) if x.get("url") and cite else cite
                there = ptr(f"{SITE}congress.html#{SP.rid(x)}", f"Specials, {ord_(c_)} Cong.")
                res.append(sent(x["date"], t, [src] if src else [], [there], para=True, kind="election", dates={x["date"]}))
                res[-1]["row"] = {
                    "cong": c_, "ch": x["ch"], "st": x["st"], "date": x["date"],
                    "election": ptr(f"{SITE}congress.html#{SP.rid(x)}", fmt(x["date"]) + (" (first election)" if x.get("new") else " (special)")),
                    "seat": f"Senate, {BLUEBOOK.get(x['st'], x['st'])}" if x["ch"] == "s" else
                            f"{BLUEBOOK.get(x['st'], x['st'])}-{x['seat'] or 'AL'}",
                    "result": "",
                    "cands": [cand(r_[0], r_[1], (f"{r_[2]:,}" + (f" ({pct(r_[2], tot)})" if tot else "")) if r_[2]
                                   else (f"{r_[3]:.1f}%" if r_[3] is not None else ""), r_ is me) for r_ in rows],
                    "cnames": [None if r_ is me else r_[0] for r_ in rows],
                    "src": (src or "") + ("; Check: matched by name only" if check else ""),
                    "key": x["key"], "check": check, "n": me[0], "special": True}
        return res

    ci = cached("election-races", cand_index)
    years = {}
    for k in dict.fromkeys((letters(last_word(sur)), letters(sur))):      # 'Van Pelt' by 'pelt'; 'du Pont' by 'dupont'
        for y_, rs_ in ci.get(k, {}).items():
            years.setdefault(y_, [])
            years[y_] += [i for i in rs_ if i not in years[y_]]
    for y, d in cached("elections", make):
        if y not in years:
            continue
        url = (d.get("source") or {}).get("url", "")

        def clerk(pg=None):
            return a(url + (f"#page={pg}" if pg else ""), f"Clerk, Election Statistics {y}" + (f", p. {pg}" if pg else ""))
        races = d.get("races") or []
        for r in (races[i] for i in years[y] if i >= 0):
            cs = r.get("cands") or []
            me = next((c for c in cs if mine_race(c)), None)
            cong = (int(y) - 1788) // 2 + 1
            by_seat = False
            if names:
                # the seat: the winner of the surname whom the roster seats from this race at the Congress's opening
                # is the person, whatever the returns make of his given names ('Tip O'Neill', 'Mo Udall', 'Pete
                # McCloskey', 'John D. Dingell Jr.'); so is the incumbent of the surname it seated at the last
                # opening, where his first name agrees (mine) (a widow who succeeded her husband between openings
                # is not him). The seat decides even where the name matched.
                seat = r.get("seat") or 0
                incs = {i.get("n") for i in r.get("inc") or []}
                now = set(seat_holders().get((cong, r["ch"], r["st"], seat)) or []) & set(names)
                later = set()            # the names the race two years on gives as the seat's incumbents
                if cong not in rostered():
                    # a Congress with no roster (the 86th): the next one's, where nothing intervened: the Senator
                    # of the class at its opening; the Representative whom the seat's race two years on names as
                    # incumbent by the same name
                    now = set(seat_holders().get((cong + 1, r["ch"], r["st"], seat)) or []) & set(names)
                    later = {i.get("n") for x in (by_year().get(str(int(y) + 2)) or {}).get("races") or []
                             if x["ch"] == r["ch"] and x["st"] == r["st"] and (x.get("seat") or 0) == seat
                             and not x.get("special") for i in x.get("inc") or []}
                before = set(seat_holders().get((cong - 1, r["ch"], r["st"], seat)) or []) & set(names)
                won = lambda c: c.get("w") and now and (cong in rostered() or c["n"] in later or (r["ch"] == "s" and mine(c["n"])))
                hit = [c for c in cs if returns_split(c.get("n") or "", sur)
                       and (won(c) or (c.get("n") in incs and before
                                       and mine(re.sub(r",? (Jr|II|III|IV)\.?$", "", c["n"]) if not sfx else c["n"])))]
                if len(hit) == 1 and (me is None or me is hit[0]):
                    me, by_seat = hit[0], True
            if not me:
                if names:
                    out += renominations(r, y, d, cong, url)
                continue
            key = race_key(y, r)
            if key in hand.get("refuse", {}) or refused(r, y, d["date"], me, by_seat):
                continue
            check = not (key in hand.get("confirm", {}) or by_seat or confirmed(r, y, me))
            tot = sum(c.get("v") or 0 for c in cs) + (r.get("scat") or 0)
            share = f" ({100 * me['v'] / tot:.1f} percent)" if tot and me.get("v") else ""
            others = ", ".join(f"{esc(c['n'])} ({c['p']}) {c['v']:,}" for c in cs if c is not me and c.get("v"))
            inc = any(mine(i.get("n")) or i.get("n") == me["n"] for i in r.get("inc") or [])
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
                # the same candidates' names as the returns print them, for linking the others to their entries
                "cnames": [None if c is me else c["n"]
                           for c in sorted((c for c in cs if c is me or c.get("v")), key=lambda c: -(c.get("v") or 0))],
                "src": (re.sub(r"[*]([^*]+)[*]", r"<i>\1</i>", esc(r["src"])) if r.get("src") else   # the Clerk prints none
                        a(url + (f"#page={r['page']}" if r.get("page") else ""),
                          f"Clerk {y}" + (f", p. {r['page']}" if r.get("page") else "")))
                       + (f"; {primary_cite(key)}" if primary_rounds(key, me["n"]) else "")
                       + ("; Check: matched by name only" if check else ""),
                "key": key, "check": check, "n": me["n"], "pre": primary_cells(key, me["n"])}
        out += ticket_rows(y, d, url, mine)

    out += special_rows()
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
    """A candidate's line in the record, in three columns: 'Ray Wolfram (R)', '17,471', '14.1%' (the count and the
    share right-aligned); the person's own in bold. A row of the grid the cell's candidates make (lvcs)."""
    n = f"<b>{esc(name)}</b>" if me else esc(name)
    n += f' <span class="lvpa">{esc(party)}</span>' if party else ""       # the party as the election tables set it
    m = re.match(r"^(.*?)\s*\(([^()]*%)\)$", votes or "")
    v, s_ = (m.group(1), m.group(2)) if m else (votes or "", "")
    # a ticket's electoral votes over its popular, the popular in the shares' shade
    parts = v.split("; ")
    v = "<br>".join(f'<span class="lvpv">{x}</span>' if x.endswith(" PV") else x for x in parts)
    two = len(parts) > 1 and parts[-1].endswith(" PV")     # the share is the popular vote's: on its line
    return f'<span class="lvn">{n}</span><span class="lvv">{v}</span><span class="lvs{" lvs2" if two else ""}">{s_}</span>'


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
        shown = [(n2, k2, e2) for n2, k2, e2 in sorted(field, key=lambda f: (-f[2], -pv.get(f[1], 0)))
                 if (n2, k2) == (n, k) or e2 or pv.get(k2, 0) >= allv * 0.01]
        field_ = [cand(n2, letter.get(k2, "") if k2 else "", line(n2, k2, e2), (n2, k2) == (n, k)) for n2, k2, e2 in shown]
        t = (f"{result.split(' (')[0]} {'to' if won else 'for'} the office of {office}, {fmt(d['date'])}: {e} electoral "
             f"votes; {share(k)} popular." if k else f"{office}, {fmt(d['date'])}: {e} electoral votes.")
        out.append(sent(d["date"], t, [a(url, f"Clerk, Election Statistics {y}")],
                        [ptr(f"{SITE}congress.html#e{y}", f"Election {y}")], para=True, kind="election",
                        dates={d["date"]}))
        out[-1]["row"] = {
            "cong": None, "ch": "p" if office == "President" else "v", "st": "", "date": d["date"],
            "election": ptr(f"{SITE}congress.html#e{y}", fmt(d["date"])), "seat": office, "result": "",
            "exec": exec_pointer(n, office, f"{int(y) + 1}-01-20") if k == winner else "",
            "cands": field_, "src": a(url, f"Clerk {y}"),
            "cnames": [None if (n2, k2) == (n, k) else n2 for n2, k2, e2 in shown], "ticket": True}
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
        cands = r["cands"]
        if r.get("cnames") and r.get("ticket") and SERIES_FOR_LINKS is not None:
            # the other tickets' candidates, where one person with an entry fits the name
            from . import namelinks
            cands = [h if not n or not namelinks.written(SERIES_FOR_LINKS, n) else
                     h.replace(esc(n), namelinks.a(SERIES_FOR_LINKS, namelinks.written(SERIES_FOR_LINKS, n), esc(n)), 1)
                     for h, n in zip(cands, r["cnames"])]
        if r.get("cnames") and r.get("key"):
            # the other candidates linked to their name entries, where the entries confirm the race (race_people)
            idx = race_people(SERIES_FOR_LINKS) if SERIES_FOR_LINKS is not None else {}
            from . import namelinks
            cands = [h if not n or (r["date"][:4], r["key"], n) not in idx else
                     h.replace(esc(n), f'<a class="nm" href="{namelinks.url(SERIES_FOR_LINKS, idx[(r["date"][:4], r["key"], n)])}">'
                                       f'{esc(n)}</a>', 1)
                     for h, n in zip(cands, r["cnames"])]
        if r.get("pre"):                         # the primaries first, then the November vote
            cands = r["pre"] + list(cands)
        out.append((r["cong"] or 0, r["date"], hit[2] if hit else r.get("exec", ""), r["election"], r["seat"], r["result"],
                    f'<span class="lvcs">{"".join(cands)}</span>', r["src"]))
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
        f'<td>{cands}{f"""<span class="lvts">{src}</span>""" if src else ""}</td></tr>'
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
        # who issued it: in a President's own entry, nothing for his own documents and the name of the sitting
        # President for another's; elsewhere, nothing for the sitting President and the name for anyone else
        if me(r["who"]):
            who = ""
        elif is_president and sitting:
            who = esc(r["who"])
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


def death_day(e):
    """The day of the person's own death the Directory gives ('died in Dallas, Tex., November 22, 1963'; 'until his
    death in Knoxville, Tenn., January 7, 1964'), the last such; not 'the vacancy caused by the death of' another."""
    if not e:
        return None
    ms = re.findall(r"(?:\bdied\b|\buntil (?:his|her) death\b)[^;]*?\b(January|February|March|April|May|June|July|"
                    r"August|September|October|November|December) (\d{1,2}), (\d{4})", e["text"])
    return f"{ms[-1][2]}-{FULL[ms[-1][0]]:02d}-{int(ms[-1][1]):02d}" if ms else None


def last_day(rp, names):
    """The last day the series shows the person alive: his last seat at an opening, the end of his last office (its
    start where it has no end)."""
    days = [str(d) for d, *_ in rp] + [t if t != "9999" else f for f, t in held_spans(names)]
    return max(days) if days else None


def alive_day(rp, names):
    """The first day the series shows the person alive: his first seat at an opening, his first office."""
    days = [str(d) for d, *_ in rp] + [f for f, t in held_spans(names)]
    return min(days) if days else None


def held_spans(names):
    """[(from, to)]: the person's tenures in the Executive roster, ex officio offices aside."""
    out = []
    for u, o, h in [x for n in names for x in holders_of(split_name(n)[0]) if x[2]["name"] == n]:
        if o.get("appt") != "XO":
            # the days he was surely in office: a date by year or month only, its latest day for the start and its
            # earliest for the end ('1966' begins Dec. 31, 1966)
            f, t = str(h.get("from") or h.get("seen") or ""), str(h.get("to") or h.get("last") or "9999")
            if not f:
                continue
            f = f if len(f) == 10 else (f + "-12-31" if len(f) == 4 else f + "-31")
            t = t if len(t) == 10 or t == "9999" else (t + "-01-01" if len(t) == 4 else t + "-01")
            out.append((f, t))
    return out


def full_givens(names):
    """The full given names the rosters record for the person's names ('Edward Lewis'): the Executive roster's and
    the Congress rosters'."""
    out = []
    for u, o, h in [x for n in names for x in holders_of(split_name(n)[0]) if x[2]["name"] == n]:
        if h.get("given"):
            out.append(h["given"])

    def make():
        idx = {}
        for f in sorted(os.listdir(os.path.join(store.ROOT, "congress"))):
            if re.match(r"\d\d\.yaml$", f):
                d = store.load_yaml(os.path.join(store.ROOT, "congress", f)) or {}
                for r in (d.get("house") or []) + (d.get("senate") or []):
                    if r.get("name") and r.get("given"):
                        idx.setdefault(r["name"], r["given"])
        return idx
    out += [cached("roster-givens", make)[n] for n in names if n in cached("roster-givens", make)]
    return out


def person_races(series, p):
    """(roster pointers, Directory entry, election sentences) for a person: the races the returns give him."""
    return cached(("person-races", p["name"]), lambda: _person_races(series, p))


def _person_races(series, p):
    name, names = p["name"], p["names"]
    sur, given = split_name(name)
    sfx, strict = person_suffix(series, p)
    rp = roster_pointers(sur, given, names)
    member = bool(rp)
    e = bd_entry(sur, given, member, () if member else person_words(sur, given, names, part3_roles(series, names)), sfx,
                 alive_day(rp, names))
    races = election_sentences(sur, given, sfx, strict, [split_name(n)[1] for n in names] + full_givens(names),
                               held_spans(names), {(c, ch, st) for _, c, ch, st, *_ in rp}, names, e, last_day(rp, names))
    return rp, e, races


def race_people(series):
    """{(year, race key, candidate as the returns write him): the person's name}: every race a name entry gives its
    person and something confirms (not 'Check'), for linking the election tables to the entries."""
    def make():
        out = {}
        for p in cached("people", lambda: people(series)):
            for s_ in person_races(series, p)[2]:
                r = s_.get("row")
                if r and r.get("key") and not r.get("check"):
                    out[(r["date"][:4], r["key"], r["n"])] = p["name"]
        return out
    return cached("race-people", make)


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
    rp, e, races = person_races(series, p)
    structured = (office_sentences(sur, given, names) + races
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
        # from the description's article: the name's 'Jr.' and its '(brother of …)' left out
        m = re.search(r", ((?:an?|the) [A-Z0-9].*)", re.sub(r"\([^)]*\)|\[[^]]*\]", "", head))
        desc = (m.group(1) if m else (head.split("), ", 1)[-1] if "), " in head else head.split(", ", 2)[-1])).strip(" .")
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
/* Names (tools/bib/lives.py) */
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
table.lvt td:nth-child(1){white-space:nowrap}
table.lvt td:nth-child(3){padding-right:0}
table.lvt b{font-weight:600}
table.lvt .lvcs{display:grid;grid-template-columns:minmax(6em,1fr) auto auto;column-gap:.7em}
table.lvt .lvv,table.lvt .lvs{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
table.lvt .lvs,table.lvt .lvpv{color:var(--muted)}
table.lvt .lvpa{font-family:var(--sans);font-size:.78em;color:var(--muted)}
table.lvt .lvs{min-width:3.2em}
table.lvt .lvs2{padding-top:1.35em}
@media (max-width:520px){table.lvt .lvcs{grid-template-columns:minmax(6em,1fr) auto}table.lvt .lvn{grid-column:1;grid-row:span 2}
  table.lvt .lvv,table.lvt .lvs{grid-column:2}table.lvt .lvs2{padding-top:0}}
table.lvt .lvpl{grid-column:1/-1;font-family:var(--sans);font-size:.72em;letter-spacing:.04em;text-transform:uppercase;
  color:var(--muted);padding-top:.25em}
table.lvt .lvpl:first-child{padding-top:0}
table.lvt .lvts{display:block}
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
         "*Statistics of the Presidential and Congressional Election* of that year, by page; CQ Guide 6th (2010), "
         "Congressional Quarterly, *Guide to U.S. Elections*, 6th ed. (2010), by page; FRUS, by subseries, "
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
    global SERIES_FOR_LINKS
    SERIES_FOR_LINKS = series
    ptrs = Pointers(series, linker)
    main = ["<h1>Names</h1>"] + INTRO + [entry(series, linker, ptrs, n) for n in names]
    return wrap(template, "Names", main)


def wrap(template, title, main):
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", title).replace("{{main}}", "\n".join(main))
    return pg.replace("</body>", CSS + "\n</body>", 1)


def pages(series, linker, template):
    """{file name: html}: names.html, the index of names by letter; names-a.html ... names-z.html, the entries; and
    lives.html, lives-a.html ..., the pages' old names, sending a reader on (anchor kept)."""
    from .congress import Pointers
    global SITE, SERIES_FOR_LINKS
    SERIES_FOR_LINKS = series
    ptrs = Pointers(series, linker)
    everyone = cached("people", lambda: people(series))
    by_letter = {}
    for p in everyone:
        by_letter.setdefault(letter_of(p), []).append(p)
    out = {}
    index = ["<h1>Names</h1>"] + INTRO + [f'<p class="logic">{len(everyone):,} persons.</p>']
    nav = " ".join(f'<a class="lvp" href="names-{L}.html">{L.upper()}</a>' for L in sorted(by_letter))
    index.append(f'<p class="lvs">{nav}</p>')
    for L in sorted(by_letter):
        ps = by_letter[L]
        index.append(f'<h2 id="{L}" data-short="{L.upper()}">{L.upper()}</h2><ul class="lvx">' + "".join(
            f'<li><a href="names-{L}.html#{key_of(p["name"])}">{esc(p["name"])}</a></li>' for p in ps) + "</ul>")
        main = [f"<h1>Names: {L.upper()}</h1>", f'<p class="lvs">{nav} · <a class="lvp" href="names.html">Index</a></p>']
        for p in ps:
            try:
                main.append(entry(series, linker, ptrs, p))
            except Exception as ex:          # one entry's fault names the person and does not stop the page
                import traceback
                print(f"names: {p['name']}: {ex!r}", traceback.format_exc().splitlines()[-3], file=sys.stderr)
        out[f"names-{L}.html"] = wrap(template, f"Names: {L.upper()}", main)
        out[f"lives-{L}.html"] = moved(f"names-{L}.html")
    out["names.html"] = wrap(template, "Names", index)
    out["lives.html"] = moved("names.html")
    return out


def moved(to):
    """A page under its old name, sending the reader to the new one with the anchor."""
    return (f'<!doctype html><meta charset="utf-8"><title>Names</title><link rel="canonical" href="{to}">'
            f'<meta http-equiv="refresh" content="0; url={to}">'
            f'<script>location.replace("{to}" + location.hash)</script><p><a href="{to}">Names</a></p>')


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
    # a President's surname alone as a title is a work about him (Sorensen, *Kennedy*)
    bare = re.compile(r"\*" + re.escape(sur) + r"\*") if given and any(
        fold(last_word(n)) == fold(sur) and fold(n.split()[0]) == fold(given.split()[0]) for n, _, _ in PRESIDENTS) else None
    # a son whose father, written bare, has his own entry: only the entries whose subject is the son
    for l, s, e, txt, sec in ([] if strict else cached("works", make).get(words[-1] if words else "", [])):
        if True:
            if e["id"] in seen:
                continue
            if any(x in txt for x in q) or (bare and any(bare.search(c) for c in store.as_list(e.get("c")))):
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
            out.append(("primary", esc(e.get("s") or ""), f" {series_html(ptrs, e['n'], l.key, e)}" if e.get("n") else "", ptr_html))
            continue
        cs = store.as_list(e.get("c"))
        prev = None                      # the author a title-first line continues ('*Flawed Giant*' after Dallek)
        for i, c in enumerate(cs):
            author = author_of(c)
            if author is None and i:
                author = prev
            prev = author if author is not None else prev
            kind = work_kind(c, author, sur, bool(subject), sec, given)
            if kind != "own" and not any(x in fold(plain(c)) for x in q) and not (subject and kind) \
                    and not (bare and bare.search(c)):
                continue           # another work in the same entry
            if not kind:
                continue
            note = f" {series_html(ptrs, e['n'], l.key, e)}" if e.get("n") and len(cs) == 1 else ""
            from . import namelinks          # the authors linked to their entries, not the person's own name
            lead, rest = namelinks.author_split(series, c, own=name)
            if author is None and e.get("s") and ";" not in e["s"] and not subject:
                # a title alone in another's subject entry is that person's work (his memoir): his name before it
                subj = re.sub(r"\s*\([^)]*\)\s*$", "", plain(e["s"])).strip()
                if "," in subj and namelinks.person(series, subj) != namelinks.person(series, name):
                    lead = namelinks.a(series, subj, esc(running(subj))) + ", "
            out.append((kind, (lead or "") + to_html(rest), note, ptr_html))
    return out


def running(name):
    """'Sorensen, Theodore C.' -> 'Theodore C. Sorensen'; 'Schlesinger, Arthur M., Jr.' -> 'Arthur M. Schlesinger Jr.'"""
    parts = [x.strip() for x in name.split(",")]
    sfx = [x for x in parts[2:] if re.fullmatch(r"(Jr|Sr|II|III|IV)\.?", x)]
    return " ".join([parts[1]] if len(parts) > 1 else []) + (" " if len(parts) > 1 else "") + parts[0] + \
        (" " + sfx[0] if sfx else "")


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
                    if r.get("given"):
                        full.setdefault(r["name"], r["given"])
    def one(a, ra, b, rb):
        """Names a and b (from sources ra, rb) are one person: compatible with each other (every name the person
        has, so 'J. Skelly' and 'Jim' do not join through 'James'), and their suffixes agree. 'Jr.' and none may
        join across sources (Part III writes 'Humphrey, Hubert H.'; the rosters, 'Humphrey, Hubert H., Jr.'); two
        suffixes that differ never join (James L. Holloway, Jr., and III)."""
        if a == b:
            return True
        # a member Part III names by the name he went by: 'Patman, Wright' is 'Patman, John W.' (John William
        # Wright); 'Thurmond, Strom' is 'Thurmond, J. Strom'; 'Gravel, Mike' is 'Gravel, Maurice R. (Mike)'
        for (n0, r0), (n1, r1) in (((a, ra), (b, rb)), ((b, rb), (a, ra))):
            g0 = gtoks(split_name(n0)[1])
            if r0 == 0 and r1 == 2 and len(g0) == 1 and fold(split_name(n0)[0]) == fold(split_name(n1)[0]):
                later = set(gtoks(split_name(n1)[1])[1:]) | set(gtoks(full.get(n1, ""))[1:]) | {
                    fold(x) for x in re.findall(r"\(([^)]+)\)", n1)}
                if g0[0] in later:
                    return suffix(n0) in ("", "Sr") or suffix(n0) == suffix(n1)
        # the roster's full given names stand for its initials ('Robert' is 'Robert Fred'; 'Jim' is 'James Robert')
        ga, gb = full.get(a) or split_name(a)[1], full.get(b) or split_name(b)[1]
        if not (same_person(*split_name(a), *split_name(b)) or same_person(split_name(a)[0], ga, split_name(b)[0], gb)):
            return False
        A, B = gtoks(ga), gtoks(gb)
        # an initial that is not the other's first ('W. Thomas' and 'Thomas Francis'): only the bare name he went by
        for X, Y in ((A, B), (B, A)):
            if X and Y and len(X[0]) == 1 and not Y[0].startswith(X[0]) and not (len(Y) == 1 and X[1:2] == Y[:1]):
                return False
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
