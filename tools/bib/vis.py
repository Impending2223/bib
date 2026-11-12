"""Visibility: whose record each claim is, and who knew it when (the owner's design, Nov. 11, 2026; the spec,
notes/proposals/visibility-spec.md, its rules §3-§5, what is stored and derived §8; this is phase 1, §9.1).
Derived, never stored: every tag (`US:public-P`, `USSR:nonpublic-A`, `US:public-PA`), its dates, and `US:all`.

    sources/provenance.yaml     the provenance registry: each periodical, official series, document series and
                                archive the calendar cites (by its links' addresses and its names), FRUS's volumes'
                                years and documents' parties, the publishers, and each cited card's kind, country
                                and first edition's year (seeded by tools/vis/seed.py; kept by hand after)
    sources/polities.yaml       the polities; each tagged person's polity, with dates where it changes; each place
                                tag's polities; each thread's (subthreads inherit)
    ./bib show ID               prints each claim's tags at the time and the dates behind them
    ./bib check [vis]           warnings only, a line each: claims with nothing computable, persons with no polity,
                                cited works whose country is `?`

STYLE
 1. A claim is a unit of `c` (tools/bib/claims.py, STYLE 1) with the rows of the entry's map (a reader's `src`, else the
    mechanical one) that ground it. An entry with no map, or whose rows are all `?`, is one claim, `all`, marked
    unmapped; a `?` row joins every unit's witnesses and marks the unit unmapped (it may ground any of them); a unit
    no row covers takes the whole entry's witnesses, unmapped. "Made public:" (the note's sentence for a private act)
    is a witness of every unit: its items' dates and series.
 2. A witness (a row's source) is classified by the registry: a card by `works` (its kind, country, year; a periodical
    card by its series), a link by the first series whose `url` its address holds, an item without a link by the first
    whose `text` it names, a registered witness (`via` rows; sources/witnesses/) by its kind, its agents and its copies
    (a FRUS copy: the volume's year). Each gives: kind (KINDS); where published (a polity, or `?`); when public (a
    date, `?` known public but not when, or never so far as the record shows); and who knew it privately (parties).
 3. Dates: the claim's own is the entry's `date` (the first day of a loose one: '1961-02' is 1961-02-01; a span's
    first day). "At the time" (the default reference, §5, ruled Nov. 11) is that day and the next morning's papers:
    a witness public by the next day counts (REF_DAYS). A year is its Jan. 1 (§5: "a memoir of 1976 is public from
    Jan. 1, 1976"). A series `dated: item` is public on the item's own date (a link's date, the cite's "(Aug. 16,
    1967)"; a later year printed in it, a later publication); `dated: event` the same, else the event's day (a record
    of the time: the Record, the Papers, a roll call); `dated: volume` FRUS's volume year; `dated: year` the card's.
 4. The rules (§3), for each polity X:
    P public: from the earliest date a witness published in X is public.
    P nonpublic, from the event's day, before then, where X knew in private: territory (the entry's place, state,
    city and province tags: every act within X's territory, as ruled), agency (the persons the claim names: tags do not
    tell the actor from the object, so every tagged person's polity; and a memoir's, diary's or oral history's agent),
    parties (a FRUS document's sender and recipients, by its heading: frus_parties; a document series' or archive's
    agents).
    A: the polities the claim addresses (STYLE 5): nonpublic from the event's day, public from the earliest public
    witness anywhere, whatever its country (a work of country `?` too).
    Organizations (§2, ruled Nov. 11) are no polities: an organization's record (the UN's documents) is published in,
    and known to, the state parties the claim addresses; an organization's person (U Thant) adds no polity. The
    organization as a polity of its own (`EEC:nonpublic-P`) waits for a ruling claim by claim (§8, `vis:`).
 5. Address (§4), in order: the tags the unit itself names (a name tag whose surname, or a place whose name, stands in
    the unit's text: the maps do not yet tie tags to units, so the text ties them); else the entry's name, place,
    state, city, province and `polity:` tags; else the thread's polities (sources/polities.yaml, a subthread its
    parent's unless it has its own).
 6. Tags at a reference date r: P public where its public date <= r; else nonpublic where its nonpublic date <= r;
    A public where any witness is public by r, else nonpublic. Where P and A agree, one tag: `X:public-PA`. Before the
    claim's own date nothing is known (§5: greyed). A public date `?` is not "by r" (a document series or a book is
    never public within a day of its event; a press or official item without a date takes the event's).
 7. Nothing computable: a claim none of whose witnesses the registry can classify (a link to a host it does not know,
    a reference work, no source) carries the placeholder `US:all` (§7), never stored, and `check` counts it.
"""
import datetime
import os
import re

from . import store

PROV = os.path.join(store.ROOT, "sources", "provenance.yaml")
POL = os.path.join(store.ROOT, "sources", "polities.yaml")
KINDS = ("press", "official", "document series", "memoir", "diary", "oral history", "scholarship", "archive",
         "reference")
# what the spec's kinds (§8) are; two more the calendar's links need: an archive's file or recording, unpublished
# (public only when "Made public" or a copy says so), and a reference work (an encyclopedia, a finding aid), which
# dates nothing and makes nothing public
PUBLIC_KINDS = {"press", "official"}          # public from their own date, a record of the time (§3, "Public sources")
LATER_KINDS = {"document series", "memoir", "diary", "oral history", "scholarship"}  # public when published
PRIVY_KINDS = {"memoir", "diary", "oral history", "document series", "archive"}   # their agents knew from the event
TOP = ("us", "ussr", "prc", "fr", "frg", "uk")
REF_DAYS = 1                                   # the next morning's papers (§5; the newspaper band, dayorder.py)
_cache = {}

MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7, "aug": 8,
          "sept": 9, "sep": 9, "oct": 10, "nov": 11, "dec": 12, "january": 1, "february": 2, "march": 3,
          "april": 4, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}
DATE_MDY = re.compile(r"\b(Jan|Feb|Mar|Apr|May|June?|July?|Aug|Sept?|Oct|Nov|Dec|January|February|March|April|"
                      r"August|September|October|November|December)\.? (\d{1,2}), (\d{4})\b")
DATE_DMY = re.compile(r"\b(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|"
                      r"December) (\d{4})\b")
DATE_URL = re.compile(r"/((?:19|20)\d\d)/(\d\d)/(\d\d)/")
YEAR_PAREN = re.compile(r"\(((?:19|20)\d\d)(?:[–-]\d{2,4})?\)")
LINK = re.compile(r"\[([^\]]*)\]\((https?://[^)\s]+)\)")


# ---------------------------------------------------------------- the registry and the polities

def _mtime(p):
    return os.path.getmtime(p) if os.path.exists(p) else None


def registry():
    """The provenance registry (sources/provenance.yaml), read once a run: {series: [...], frus_volumes, frus_parties,
    publishers, works}."""
    k = ("prov", _mtime(PROV))
    if _cache.get("prov_key") != k:
        d = (store.load_yaml(PROV) if os.path.exists(PROV) else None) or {}
        for key in ("series", "frus_volumes", "frus_parties", "publishers", "works"):
            d.setdefault(key, [] if key == "series" else {})
        _cache.update(prov_key=k, prov=d)
    return _cache["prov"]


def polities():
    """sources/polities.yaml: {polities, names, places, threads}."""
    k = ("pol", _mtime(POL))
    if _cache.get("pol_key") != k:
        d = (store.load_yaml(POL) if os.path.exists(POL) else None) or {}
        for key in ("polities", "names", "places", "threads"):
            d.setdefault(key, {})
        _cache.update(pol_key=k, pol=d)
    return _cache["pol"]


def is_org(pid):
    return bool((polities()["polities"].get(pid) or {}).get("org"))


def tag_code(pid):
    p = polities()["polities"].get(pid) or {}
    return p.get("tag") or str(pid).upper()


def order_key(pid):
    return (TOP.index(pid) if pid in TOP else len(TOP), str(pid))


def person_polity(key, date):
    """A name key's polity at a date: its row's `polity`, or the range holding the date; None where it has none."""
    v = polities()["names"].get(key)
    if v is None:
        return None
    if isinstance(v, str):
        return None if v == "?" else v
    if isinstance(v, dict):
        p = v.get("polity")
        return None if p in (None, "?") else p
    if isinstance(v, list):                  # [{polity, from?, until?}]: office or allegiance changes
        for r in v:
            if (not r.get("from") or str(r["from"]) <= date) and (not r.get("until") or date < str(r["until"])):
                return None if r.get("polity") in (None, "?") else r.get("polity")
        return None
    return None


def place_polities(tag):
    """A place tag's polities: its own row, else its namespace's (`state:*`), else []."""
    P = polities()["places"]
    v = P.get(tag)
    if v is None and ":" in tag:
        v = P.get(tag.split(":", 1)[0] + ":*")
    if isinstance(v, dict):
        v = v.get("polities")
    return [x for x in store.as_list(v) if x and x != "?"]


def thread_polities(lst, slug):
    """A thread's polities: its own, else its nearest ancestor's (subthreads inherit, §4)."""
    T = polities()["threads"]
    for s in (lst.thread_line(slug) if lst is not None else [slug]):
        v = T.get(s)
        if isinstance(v, dict):
            v = v.get("polities")
        if v:
            return [x for x in store.as_list(v) if x != "?"]
    return []


# ---------------------------------------------------------------- dates

def iso(d):
    """'1961-02' -> '1961-02-01'; '1976' -> '1976-01-01'; a full date as it is; None for anything else."""
    s = str(d or "")
    if re.match(r"^\d{4}-\d\d-\d\d$", s):
        return s
    if re.match(r"^\d{4}-\d\d$", s):
        return s + "-01"
    if re.match(r"^\d{4}$", s):
        return s + "-01-01"
    return None


def plus_days(d, n):
    y, m, dd = (int(x) for x in d.split("-"))
    return (datetime.date(y, m, dd) + datetime.timedelta(days=n)).isoformat()


def dates_in(text):
    """Every full date the text (or a link's address) gives, as ISO strings, in order."""
    out = []
    for m in DATE_URL.finditer(text or ""):
        out.append(f"{m.group(1)}-{m.group(2)}-{m.group(3)}")
    for m in DATE_MDY.finditer(text or ""):
        mo = MONTHS.get(m.group(1).lower().rstrip("."))
        if mo:
            out.append(f"{m.group(3)}-{mo:02d}-{int(m.group(2)):02d}")
    for m in DATE_DMY.finditer(text or ""):
        out.append(f"{m.group(3)}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}")
    return out


def item_date(text, event, dated):
    """When an item of a series `dated: item|event` was public (STYLE 3): its own date; else a year it prints after
    the event's (a later publication: '(2015)'); else, for `event`, the event's day; else '?'."""
    plain_text = LINK.sub(lambda m: m.group(1) + " " + m.group(2), text or "")
    ds = [d for d in dates_in(plain_text) if "1900" < d < "2100"]
    if ds:
        return min(ds) if dated == "event" and min(ds) >= event else ds[0]
    ys = [int(y) for y in YEAR_PAREN.findall(plain_text)]
    later = [y for y in ys if event and y > int(event[:4])]
    if later:
        return f"{min(later)}-01-01"
    return event if dated == "event" else "?"


# ---------------------------------------------------------------- witnesses

def W(label, kind, pub, public, privity=(), basis=""):
    """A witness: its label, kind, where published (a polity, '?', or None: not published), when public (an ISO date,
    '?', or None), the polities privy to it from the event, and where the registry found it."""
    return {"label": label, "kind": kind, "pub": pub, "public": public, "privity": set(privity), "basis": basis}


def series_for_url(url):
    host_path = re.sub(r"^https?://", "", url or "")
    for s in registry()["series"]:
        for pat in store.as_list(s.get("url")):
            if host_path.startswith(pat) or ("/" not in pat and host_path.split("/", 1)[0].endswith("." + pat)):
                return s
    return None


def series_for_text(text):
    t = text or ""
    for s in registry()["series"]:
        for pat in store.as_list(s.get("text")):
            if pat and pat in t:
                return s
    return None


def series_for_card(cid):
    for s in registry()["series"]:
        if cid in store.as_list(s.get("cards")):
            return s
    return None


def frus_volume(url_or_text):
    """'frus1961-63v10' for a FRUS link or cite ('FRUS 1961–63, X')."""
    m = re.search(r"(frus\d{4}-\d{2}v\d{2}(?:p\d)?)", url_or_text or "")
    if m:
        return m.group(1)
    m = re.search(r"FRUS (\d{4})[–-](\d{2}), ([IVXL]+)\b", url_or_text or "")
    if m:
        return f"frus{m.group(1)}-{m.group(2)}v{_roman(m.group(3)):02d}"
    return None


def frus_year(vol):
    """A FRUS volume's publication year (frus_volumes; a part's volume, 'v29p1', falls back to the whole's), or None."""
    V = registry()["frus_volumes"]
    if not vol:
        return None
    y = V.get(vol) or V.get(re.sub(r"p\d$", "", vol))
    return str(y) if y and str(y) != "?" else None


def _roman(r):
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
    n = 0
    for a, b in zip(r, r[1:] + " "):
        n += -vals[a] if vals.get(b, 0) > vals[a] else vals[a]
    return n


def from_series(s, label, text, event, addressed):
    """A witness of a registry series, for an item (its text and link) under an event."""
    kind, pol, dated = s.get("kind"), s.get("polity"), s.get("dated") or "event"
    if kind == "reference":
        return W(label, kind, None, None, basis=s.get("key", ""))
    if dated == "volume":
        y = frus_year(frus_volume(text))
        public = f"{y}-01-01" if y else "?"
    elif kind == "archive":
        public = None
    elif dated == "year":
        ys = re.findall(r"\b((?:19|20)\d\d)\b", text or "")
        public = f"{ys[-1]}-01-01" if ys else "?"
    else:
        public = item_date(text, event, dated)
    privity = set(store.as_list(s.get("privity")))
    pub = pol
    if pol == "parties":                   # an organization's record: its state parties' (STYLE 4)
        pub = None
        privity |= set(addressed)
    if kind in ("document series", "archive"):
        vol_key = re.search(r"(frus\d{4}-\d{2}v\d{2}(?:p\d)?/d\d+)", text or "")
        parties = registry()["frus_parties"].get(vol_key.group(1)) if vol_key else None
        privity |= set(store.as_list(parties)) or ({pol} if pol not in (None, "?", "parties") else set())
    return W(label, kind, pub, public, privity, s.get("key", ""))


def from_card(series, cid, event, addressed):
    s = series_for_card(cid)
    if s:
        return from_series(s, cid, "", event, addressed)
    row = registry()["works"].get(cid)
    f = series.works.fields(cid) or {}
    if row is None:
        y = re.match(r"\d{4}", str(f.get("year") or ""))
        return W(cid, "?", "?", f"{y.group(0)}-01-01" if y else "?", basis="no registry row")
    kind = row.get("kind") or "scholarship"
    year = str(row.get("year") or f.get("year") or "?")
    y = re.match(r"\d{4}", year)
    public = f"{y.group(0)}-01-01" if y else "?"
    country = row.get("country") or "?"
    if kind in PUBLIC_KINDS and row.get("dated") == "event":
        public = event
    privity = set()
    if kind in PRIVY_KINDS:
        for a in store.as_list(row.get("agent")):
            p = person_polity(a, event) if not str(a) in polities()["polities"] else a
            if p and not is_org(p):
                privity.add(p)
    return W(cid, kind, country, public, privity, "works")


WITNESS_KIND = {"press": "press", "speech": "official", "statement": "official", "hearing": "official",
                "diary": "diary", "interview": "oral history", "oral history": "oral history", "memoir": "memoir",
                "study": "scholarship", "collection": "document series"}
# the registry's archives and their polities, by the words a witness's `where` gives
ARCHIVES = [(re.compile(r"\b(LBJ|JFK|Johnson|Kennedy|Eisenhower|Nixon|Truman) Library|\bNARA\b|National Archives\b(?!"
                        r" of)|\bRG \d|\bNSF\b|\bPOF\b|\bWHCF\b|Library of Congress|\bCIA\b|\bFBI\b"), "us"),
            (re.compile(r"\bFO \d|\bFCO \d|\bPREM \d|\bCAB \d|\bDEFE \d|\bNAUK\b|\bTNA\b|\bPRO\b"), "uk"),
            (re.compile(r"\bAVP ?RF\b|\bRGANI\b|\bAPRF\b|\bTsKhSD\b|\bRGASPI\b|\bTsAMO\b"), "ussr"),
            (re.compile(r"\bMAE\b|Quai d|\bAN, \d|Archives nationales"), "fr"),
            (re.compile(r"\bPA ?AA\b|\bBArch\b|Bundesarchiv"), "frg"),
            (re.compile(r"\bSAPMO\b"), "gdr"),
            (re.compile(r"PRC (?:Foreign Ministry|FMA)|\bCFMA\b|Chinese Foreign Ministry"), "prc")]


def text_polity(text):
    """The polity a witness's agent or place names outright ('British Embassy, Peking'), or None."""
    from . import vis_words
    return vis_words.polity_of(text)


def from_witness(series, wid, event, addressed):
    from . import witnesses
    rows = witnesses.load()[0]
    w = rows.get(wid)
    if w is None:
        return W(wid, "?", "?", "?", basis="no witness")
    k = WITNESS_KIND.get(w.get("kind"), "archive")
    privity, pub = set(), None
    for a in store.as_list(w.get("agent")):
        a = str(a)
        p = person_polity(a[5:], event) if a.startswith("name:") else text_polity(a)
        if p and not is_org(p):
            privity.add(p)
    for rx, p in ARCHIVES:
        if rx.search(str(w.get("where") or "")):
            privity.add(p)
    d = iso(w.get("date")) or event
    if k in ("press", "official"):
        public = d
        pub = next(iter(sorted(privity)), "?") if privity else "?"
    else:
        public = None
        for c in store.as_list(w.get("copies")):
            y = frus_year(frus_volume(str(c)))
            if y:
                pub, public = "us", min(public or "9999", f"{y}-01-01")
    if k in ("memoir", "scholarship", "diary", "oral history", "document series") and public is None:
        public = "?"
    return W(wid, k, pub, public, privity if k != "official" else privity, "witnesses")


def made_public(e, event, addressed):
    """The witnesses the note's "Made public:" sentence names (STYLE 1): each item's series and date."""
    from .claims import note_parts
    out = []
    for s in note_parts(e.get("n"))[1]:
        if not s.startswith("Made public"):
            continue
        body = re.sub(r"^Made public[^:]*:\s*", "", s).rstrip(".")
        for it in re.split(r";\s+", body):
            lk = LINK.search(it)
            ser = (series_for_url(lk.group(2)) if lk else None) or series_for_text(it)
            card = re.search(r"\[\[(w\.[^\]|]+)", it)
            ds = [d for d in dates_in(it)]
            ys = YEAR_PAREN.findall(it) or re.findall(r"\b((?:19|20)\d\d)\b", it)
            public = ds[0] if ds else (f"{ys[-1]}-01-01" if ys else "?")
            if ser and ser.get("dated") == "volume" and not ys:
                y = frus_year(frus_volume(it))
                public = f"{y}-01-01" if y else "?"
            if ser:
                pub = ser.get("polity") if ser.get("polity") not in ("parties",) else None
                kind = ser.get("kind")
            elif card:
                row = registry()["works"].get(card.group(1)) or {}
                pub, kind = row.get("country") or "?", row.get("kind") or "scholarship"
            else:
                pub, kind = "?", "?"
            if public == "?" and kind == "?":
                continue
            out.append(W("Made public: " + it.strip()[:60], kind if kind != "archive" else "press", pub, public,
                         basis="made public"))
    return out


def witness_for_row(series, e, row, event, addressed):
    """(the row's raw text, kind, key, pin, note, units, the note's item) -> a witness (STYLE 2)."""
    r, kind, key, pin, note, u, item = row
    if kind == "card":
        return from_card(series, key, event, addressed)
    if kind == "via":
        from . import claims
        reg = claims.register(series)
        w = reg.get((key, str(pin), str(note)))
        if w:
            return from_witness(series, w["id"], event, addressed)
        return W(f"{key} {pin} n.{note}", "?", "?", "?", basis="no witness")
    if kind == "witness":
        return from_witness(series, key, event, addressed)
    if kind == "url":
        s = series_for_url(key)
        if s is None:
            return W(key, "?", "?", "?", basis="no series for the address")
        return from_series(s, key, (item or "") + " " + key, event, addressed)
    if kind == "text":
        s = series_for_text(item or key)
        if s is None:
            return W(key, "?", "?", "?", basis="no series for the words")
        return from_series(s, key, item or key, event, addressed)
    return W(str(r), "?", "?", "?", basis="row")


# ---------------------------------------------------------------- address, territory, agency

def unit_ties(tags, text):
    """The tags a unit's text names: a name tag by its surname (the key's first part) or, for a name in its own order,
    its last; a place by its key's words; else []."""
    t = " " + re.sub(r"[^a-z0-9]+", " ", store.fold(text or "").lower()) + " "
    out = []
    for g in tags:
        g = str(g)
        ns, _, k = g.partition(":")
        if ns not in ("name", "place", "city", "province", "polity"):
            continue
        parts = [p for p in k.split("-") if p not in ("jr", "sr", "ii", "iii", "iv")]
        if not parts:
            continue
        cands = {parts[0], parts[-1]} if ns == "name" else {" ".join(parts)}
        if any(len(c) >= 3 and f" {c} " in t for c in cands):
            out.append(g)
    return out


def tag_polities(tags, date):
    """(address polities, territory polities, agency polities) of a list of tags."""
    addr, terr, agency = [], [], []
    for g in tags:
        g = str(g)
        ns, _, k = g.partition(":")
        if ns == "name":
            p = person_polity(k, date)
            if p and not is_org(p):
                addr.append(p)
                agency.append(p)
        elif ns in ("place", "state", "city", "province"):
            ps = [p for p in place_polities(g) if not is_org(p)]
            addr += ps
            terr += ps
        elif ns == "polity" and k and not is_org(k):
            addr.append(k)
    u = lambda xs: sorted(set(xs), key=order_key)
    return u(addr), u(terr), u(agency)


def address(lst, e, unit_text, date):
    """(address polities, territory, agency, basis) for a unit (STYLE 5)."""
    tags = [str(t) for t in e.get("tags") or []]
    tied = unit_ties(tags, unit_text) if unit_text is not None else []
    a, terr_all, ag_all = tag_polities(tags, date)
    if tied:
        ta, tt, tg = tag_polities(tied, date)
        if ta:
            return ta, terr_all, tg or ag_all, "unit"
    if a:
        return a, terr_all, ag_all, "entry"
    th = [p for p in thread_polities(lst, e.get("thread")) if not is_org(p)]
    return sorted(set(th), key=order_key), terr_all, ag_all, ("thread" if th else "none")


# ---------------------------------------------------------------- the compute

def claims_of(series, lst, e):
    """The entry's claims (STYLE 1): [{unit, text, map, unmapped, rows}] with each claim's rows."""
    from . import claims as C
    us = C.units(e.get("c") or "")
    eff = C.effective(e)
    rows = C.resolve(e) if eff else []
    how = "reader" if e.get("src") else ("mechanical" if eff else None)
    lettered = [r for r in rows if r[5] not in (None, "?")]
    qrows = [r for r in rows if r[5] == "?"]
    if not rows or not lettered or not us:
        return [{"unit": "all", "text": e.get("c") or "", "map": how, "unmapped": True, "rows": rows}]
    out = []
    for i, u in enumerate(us):
        L = C.LETTERS[i]
        mine = [r for r in lettered if L in r[5]]
        unm = bool(qrows) or not mine
        out.append({"unit": L, "text": u, "map": how, "unmapped": unm, "rows": (mine + qrows) if mine else rows})
    return out


def compute(series, lst, e):
    """Each claim of a calendar entry with its witnesses, its polities' P and A dates, and its tags at the time
    (STYLE 4-6): [{unit, text, map, unmapped, date, ref, witnesses, polities: {X: {P: [np, pub], A: [np, pub]}},
    address_basis, tags, computed}]."""
    date = iso(e.get("date"))
    out = []
    for cl in claims_of(series, lst, e):
        if date is None:
            out.append(dict(cl, date=None, ref=None, witnesses=[], polities={}, address_basis="none",
                            tags=["US:all"], computed=False))
            continue
        addr, terr, agency, basis = address(lst, e, cl["text"] if cl["unit"] != "all" else None, date)
        ws = [witness_for_row(series, e, r, date, addr) for r in cl["rows"] if r[1]]
        ws += made_public(e, date, addr)
        known = [w for w in ws if w["kind"] not in ("?", "reference")]
        ref = plus_days(date, REF_DAYS)
        res = dict(cl, date=date, ref=ref, witnesses=ws, address_basis=basis)
        if not known:
            out.append(dict(res, polities={}, tags=["US:all"], computed=False))
            continue
        privy = set(terr) | set(agency)
        for w in known:
            privy |= {p for p in w["privity"] if p and p != "?" and not is_org(p)}
        pubs = {}
        any_public = None
        for w in known:
            d = w["public"]
            if d and d != "?":
                d = max(d, date) if w["kind"] in PUBLIC_KINDS else d
                any_public = min(any_public or d, d)
                if w["pub"] and w["pub"] != "?" and not is_org(w["pub"]):
                    pubs[w["pub"]] = min(pubs.get(w["pub"], d), d)
        unknown_public = any(w["public"] == "?" for w in known)
        pol = {}
        for X in sorted(set(addr) | privy | set(pubs), key=order_key):
            rec = {}
            p_pub = pubs.get(X)
            if X in privy or p_pub:
                np_from = date if X in privy and (p_pub is None or p_pub > date) else None
                rec["P"] = [np_from, p_pub or ("?" if unknown_public and X in privy else None)]
            if X in addr:
                a_pub = any_public if any_public and any_public > date else (date if any_public else None)
                rec["A"] = [date if not any_public or any_public > date else None,
                            a_pub or ("?" if unknown_public else None)]
            pol[X] = rec
        out.append(dict(res, polities=pol, tags=tags_at(pol, ref, date), computed=True))
    return out


def status(span, r):
    """'public', 'nonpublic' or None for a [nonpublic from, public from] pair at reference date r."""
    np_from, pub_from = span
    if pub_from and pub_from != "?" and pub_from <= r:
        return "public"
    if np_from and np_from <= r:
        return "nonpublic"
    return None


def tags_at(pol, r, date=None):
    """The tags at reference date r (STYLE 6): ['US:public-PA', 'USSR:nonpublic-A', ...]; [] before the claim's date."""
    if date and r < date:
        return []
    out = []
    for X in sorted(pol, key=order_key):
        rec = pol[X]
        p = status(rec["P"], r) if "P" in rec else None
        a = status(rec["A"], r) if "A" in rec else None
        code = tag_code(X)
        if p and p == a:
            out.append(f"{code}:{p}-PA")
        else:
            if p:
                out.append(f"{code}:{p}-P")
            if a:
                out.append(f"{code}:{a}-A")
    return out


def entry_claims(series):
    """Every calendar entry's claims: [(list, entry, [claims])]."""
    from . import claims as C
    out = []
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec in lst.walk():
            for e in sec.entries:
                if e["id"].startswith(f"{lst.key}.thread.") or not isinstance(e.get("c"), str):
                    continue
                out.append((lst, e, compute(series, lst, e)))
    return out


# ---------------------------------------------------------------- show and check

def _span(span):
    np_from, pub_from = span
    bits = []
    if np_from:
        bits.append(f"nonpublic from {np_from}")
    if pub_from:
        bits.append(f"public from {pub_from}" if pub_from != "?" else "public from ? (date unknown)")
    return ", ".join(bits) or "-"


def _wline(w):
    pub = w["pub"] if w["pub"] else "-"
    priv = ",".join(sorted(w["privity"], key=order_key)) or "-"
    return (f"{w['label'][:60]}  [{w['kind']}; published {tag_code(pub) if pub not in ('-', '?') else pub}, "
            f"{w['public'] or 'not public'}; privy {priv.upper() if priv != '-' else '-'}]")


def show_lines(series, lst, e):
    """`./bib show`'s lines for an entry's claims: each unit, its tags at the time, the dates behind them."""
    out = []
    cls = compute(series, lst, e)
    if not cls:
        return out
    d = cls[0].get("date")
    out.append(f"# visibility (tools/bib/vis.py): at the time, {d} and the next morning's papers (to {cls[0].get('ref')})")
    for cl in cls:
        mark = " (unmapped)" if cl["unmapped"] else ""
        out.append(f"#   {cl['unit']}{mark}: {' '.join(cl['tags']) or '(none)'}"
                   + ("" if cl["computed"] else "   (nothing computable: the placeholder)")
                   + (f"   address from the {cl['address_basis']}" if cl["computed"] else ""))
        for X in sorted(cl["polities"], key=order_key):
            rec = cl["polities"][X]
            parts = [f"{k} {_span(rec[k])}" for k in ("P", "A") if k in rec]
            out.append(f"#       {tag_code(X):5} " + "; ".join(parts))
        for w in cl["witnesses"]:
            out.append(f"#       - {_wline(w)}")
    return out


def problems(series):
    """Warnings only (the spec §9.1; never an error, so the site still deploys): (where, message), one line each."""
    warns = []
    try:
        ec = entry_claims(series)
    except Exception as x:                    # a fault here must never stop a build
        return [("tools/bib/vis.py", f"the visibility pass failed: {type(x).__name__}: {x}")]
    n_cl = sum(len(c) for _, _, c in ec)
    none = [(e["id"], c["unit"]) for _, e, cs in ec for c in cs if not c["computed"]]
    if none:
        ents = sorted({i for i, _ in none})
        warns.append(("lists/cal/", f"{len(none):,} of {n_cl:,} claims ({len(ents):,} entries) with no computable "
                                    f"tag: the placeholder US:all (e.g. {', '.join(ents[:3])}; `./bib show ID`)"))
    names = polities()["names"]
    seen = set()
    for lst, e, _ in ec:
        for t in e.get("tags") or []:
            t = str(t)
            if t.startswith("name:") and t not in seen:
                seen.add(t)
                k = t[5:]
                if k not in names:
                    warns.append((e["id"], f"{t}: no polity in sources/polities.yaml (names)"))
                elif person_polity(k, iso(e.get("date")) or "1965-01-01") is None and names.get(k) not in ("?",) \
                        and not (isinstance(names.get(k), dict) and names[k].get("polity") == "?"):
                    pass
    q = sum(1 for v in polities()["names"].values() if v == "?" or (isinstance(v, dict) and v.get("polity") == "?"))
    if q:
        warns.append(("sources/polities.yaml", f"{q:,} persons whose polity is `?` (names)"))
    for lst, e, _ in ec:
        th = e.get("thread")
        if th and not thread_polities(lst, th):
            warns.append((e["id"], f"thread {th!r}: no polities in sources/polities.yaml (threads)"))
            break
    reg = registry()["works"]
    cited = set()
    for _, _, cs in ec:
        for c in cs:
            for w in c["witnesses"]:
                if w["basis"] == "works" or w["basis"] == "no registry row":
                    cited.add(w["label"])
    unk = sorted(c for c in cited if (reg.get(c) or {}).get("country", "?") == "?")
    if unk:
        warns.append(("sources/provenance.yaml", f"{len(unk):,} of {len(cited):,} cited works with country `?` "
                                                 "(the publisher not yet known)"))
    missing = sorted(c for c in cited if c not in reg)
    if missing:
        warns.append(("sources/provenance.yaml", f"{len(missing):,} cited works with no registry row "
                                                 f"(python3 -I tools/vis/seed.py adds them; e.g. {missing[0]})"))
    return warns


def stats(series):
    """Counts for the report: entries and claims with computed tags against US:all."""
    import collections
    t = collections.Counter()
    for lst, e, cs in entry_claims(series):
        t["entries"] += 1
        t["claims"] += len(cs)
        t["claims computed"] += sum(1 for c in cs if c["computed"])
        t["claims unmapped"] += sum(1 for c in cs if c["unmapped"])
        if all(c["computed"] for c in cs):
            t["entries all computed"] += 1
        elif any(c["computed"] for c in cs):
            t["entries partly computed"] += 1
        else:
            t["entries US:all"] += 1
        for c in cs:
            if c["computed"]:
                if any(tg.endswith("nonpublic-P") or tg.endswith("nonpublic-PA") for tg in c["tags"]):
                    t["claims with a nonpublic P at the time"] += 1
                if any(not tg.startswith("US:") for tg in c["tags"]):
                    t["claims with a polity other than the US"] += 1
                t["address: " + c["address_basis"]] += 1
    return t
