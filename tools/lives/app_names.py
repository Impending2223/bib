"""The presidential documents (APP) that name each person with a Lives entry: sources/app-names/<letter>.json and
sources/app-index.jsonl.
# Usage: python3 tools/lives/app_names.py CACHE_DIR
#   CACHE_DIR: the corpus tools/lives/app_corpus.py read (index.jsonl and docs/).
#   Writes sources/app-index.jsonl, one document a line {url, date, who, title} in the corpus's order, and for
#   each person {key: [line numbers]}.
#   A document names a person where its text gives the person's name: the first given name (or a name in
#   parentheses, 'Ted'), any further given names or initials, and the surname ('Hubert Humphrey', 'Hubert H.
#   Humphrey'); or an office title and the surname ('Senator Humphrey', 'Vice President Humphrey'; not 'Mr.')
#   where the person held such an office (the Executive roster, the Congresses, Part III's role, the Directory) and
#   no other person of the surname did ('Vice President Humphrey' is Hubert; 'Secretary Humphrey', George M.).
#   Two persons sharing a first name and surname, a father and a son with a suffix: a document dated in or before
#   the father's death (the Directory's year, or POCOM's) names the father, a later one the son. Namesakes whose
#   further given names differ (John W. Dean III and John G. Dean): a document names one where it gives his further
#   name or initial or his suffix ('John W. Dean III'); the bare name ('John Dean') only where
#   sources/app-matches.yaml gives it to one of them, for the years it gives, with the reason. A son the file marks
#   strict, whose father of the same name is better known (Franklin D. Roosevelt, Jr.), only by his suffix, an office
#   title only he held, or the file's years; his father, where the series holds him, by the bare name in every year
#   (not where the son's suffix follows). Any other shared
#   first name and surname is left out: the text cannot tell them apart. A document does not name its own author.
#   A title two persons of the surname hold ('Governor Hughes': Harold E. of Iowa, Richard J. of New Jersey): a document
#   is one's where its title or text names his State, a place in it, or his name in full, and nothing of the other's
#   (marks); where the text does not settle it, his where he alone held the title that day (holds: `tenure` in
#   sources/app-matches.yaml, else his offices' years); else, for a pair whose tenure that file gives, each of
#   theirs, recorded in sources/app-names-checks.json and shown "Check" on the Names pages.
#   A name Part III writes in its own order ('Ngo Dinh Diem'): the name, and its forms in sources/name-forms.yaml
#   ('President Diem', 'Mao Tse-tung'), as phrases.
#   APP's 'Event Timeline' pages (its chronology of each presidency) are not documents and are left out.
"""
import datetime, gzip, hashlib, json, os, re, sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))
from bib import store  # noqa: E402
from bib.lives import people, key_of, split_name, same_person, natural, name_forms  # noqa: E402

OUT = os.path.join(HERE, "..", "..", "sources")
def forms(p, strict=False, sfx="", mids_ok=True):
    """The regex for a person's names. strict: only the forms that give a further given name or initial after the
    first name, or the suffix after the surname ('John W. Dean', 'John Wesley Dean', 'John Dean III')."""
    firsts, mids = set(), set()
    for n in p["names"]:
        sur, given = split_name(n)
        nick = re.findall(r"\(([A-Z][a-z]+)\)", n)
        g = re.sub(r"\([^)]*\)", "", given).replace(",", " ").split()
        g = [w for w in g if not re.fullmatch(r"(Jr|Sr|II|III|IV)\.?", w)]
        if g:
            firsts.add(g[0].rstrip("."))
            if len(g) > 1 and len(g[0].rstrip(".")) == 1 and len(g[1].rstrip(".")) > 1:
                firsts.add(g[1])         # the middle name he went by: 'M. Caldwell Butler', 'Caldwell Butler'
            for w in g[1:]:              # for namesakes (strict) an initial also stands for its name ('M.', 'Matson')
                mids.add(re.escape(w) + r"|" + re.escape(w[0]) + r"[a-z]{2,}" if strict and w.endswith(".") and len(w) == 2
                         else re.escape(w) if w.endswith(".") else re.escape(w) + r"|" + re.escape(w[0]) + r"\.")
        firsts.update(nick)
    for n in p["names"]:
        g = [w for w in re.sub(r"\([^)]*\)", "", split_name(n)[1]).replace(",", " ").split()
             if not re.fullmatch(r"(Jr|Sr|II|III|IV)\.?", w)]
        # the Congress rosters' 'C. W. Bill': a full word after the initials is the name he went by
        if len(g) > 1 and all(len(w.rstrip(".")) == 1 for w in g[:-1]) and len(g[-1]) > 1 and not g[-1].endswith("."):
            firsts.add(g[-1])
    first = "|".join(re.escape(f) for f in sorted(firsts) if len(f) > 1)
    inits = sorted({r"\s*".join(re.escape(w) for w in g) for g in
                    ([w for w in re.sub(r"\([^)]*\)", "", split_name(n)[1]).replace(",", " ").split()
                      if not re.fullmatch(r"(Jr|Sr|II|III|IV)\.?", w)] for n in p["names"])
                    if len(g) > 1 and all(re.fullmatch(r"[A-Z]\.", w) for w in g)})
    if inits:                            # initials alone, all of them: 'C. D. Jackson', 'C.D. Jackson'
        return rf"\b(?:{'|'.join(inits)}{'|' + first if first else ''})\s+{re.escape(p['sur'])}\b"
    if not first:
        return None
    if strict:
        alts = []
        if mids and mids_ok:
            alts.append(rf"\b(?:{first})(?:\s+(?:" + "|".join(sorted(mids)) + rf"))+\s+{re.escape(p['sur'])}\b")
        if sfx:                          # the suffix, with or without the further names ('Franklin D. Roosevelt, Jr.')
            any_mid = r"(?:\s+(?:" + "|".join(sorted(mids) + [r"[A-Z]\."]) + r"))*"
            alts.append(rf"\b(?:{first}){any_mid}\s+{re.escape(p['sur'])},?\s+{re.escape(sfx)}(?![a-z])")
        return "|".join(alts) or None
    mid = r"(?:\s+(?:" + "|".join(sorted(mids)) + r"))*" if mids else ""
    return rf"\b(?:{first}){mid}\s+{re.escape(p['sur'])}\b"


# office titles only, not 'Mr.' or 'Dr.': 'Mr. Hunt' may be anyone of the name
TITLE_WORDS = [  # a title in the text, and the words of an office that bears it
    (r"Senator", r"senat"), (r"Representative|Congressman|Congresswoman", r"representative|\bhouse\b|congressman"),
    (r"Vice President", r"vice president"), (r"Attorney General", r"attorney general"),
    (r"Postmaster General", r"postmaster general"), (r"Under Secretary", r"under secretary"),
    (r"Assistant Secretary", r"assistant secretary"), (r"Secretary", r"secretary"), (r"Ambassador", r"ambassador"),
    (r"Governor", r"governor"), (r"General|Gen\.", r"\bgen(eral)?\b(?<!attorney general)(?<!postmaster general)"
                                                    r"(?! counsel)(?<!inspector general)(?<!surgeon general)"
                                                    r"(?<!secretary general)(?<!director general)"), (r"Admiral|Adm\.", r"\badm(iral)?\b"),
    (r"Judge", r"judge"), (r"Justice", r"justice"), (r"Director", r"director"), (r"Chairman", r"chairman"),
    (r"Commissioner", r"commissioner"), (r"Speaker", r"speaker"), (r"Leader", r"leader")]


def offices_text(series, p):
    """The person's offices, folded: the Executive roster's titles and ranks, the chambers he sat in, Part III's roles,
    the Directory's description."""
    from bib import lives as L, executive as X
    t = []
    for u, o, h in L.holders_of(p["sur"]):
        if h["name"] in p["names"]:
            t.append(f"{X.title_at(o, h['from'])} {h.get('title') or ''} {h.get('rank') or o.get('rank') or ''}")
    for d, c, ch, *_ in L.roster_pointers(p["sur"], p["given"], p["names"]):
        t.append("senator" if ch == "s" else "representative")
    for n in p["names"]:
        t.append(ROLES.get(n, ""))
    e = L.bd_entry(p["sur"], p["given"], True, (), L.person_suffix(series, p)[0])
    if e and L.roster_pointers(p["sur"], p["given"], p["names"]):
        t.append(re.split(r";", e["text"])[0])
    return store.fold(" ".join(t))


STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
          "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
          "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
          "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
          "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
          "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]


ABBR = {"Ala": "Alabama", "Ariz": "Arizona", "Ark": "Arkansas", "Calif": "California", "Cal": "California",
        "Colo": "Colorado", "Conn": "Connecticut", "Del": "Delaware", "Fla": "Florida", "Ga": "Georgia",
        "Ill": "Illinois", "Ind": "Indiana", "Kans": "Kansas", "Kan": "Kansas", "Ky": "Kentucky", "La": "Louisiana",
        "Md": "Maryland", "Mass": "Massachusetts", "Mich": "Michigan", "Minn": "Minnesota", "Miss": "Mississippi",
        "Mo": "Missouri", "Mont": "Montana", "Nebr": "Nebraska", "Neb": "Nebraska", "Nev": "Nevada",
        "N.H": "New Hampshire", "N.J": "New Jersey", "N. Mex": "New Mexico", "N.M": "New Mexico", "N.Y": "New York",
        "N.C": "North Carolina", "N. Dak": "North Dakota", "N.D": "North Dakota", "Okla": "Oklahoma", "Oreg": "Oregon",
        "Ore": "Oregon", "Pa": "Pennsylvania", "R.I": "Rhode Island", "S.C": "South Carolina", "S. Dak": "South Dakota",
        "S.D": "South Dakota", "Tenn": "Tennessee", "Tex": "Texas", "Vt": "Vermont", "Va": "Virginia",
        "Wash": "Washington", "W. Va": "West Virginia", "Wis": "Wisconsin", "Wisc": "Wisconsin", "Wyo": "Wyoming"}
POSTAL = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
          "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
          "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
          "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
          "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
          "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
          "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
          "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia",
          "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"}
NAMED = ("Times|Post|City|Herald|Daily|Tribune|Journal|World|Mirror|News|Star|Register|Sun|Telegram|Evening|Avenue|"
         "Street|Turnpike|Central|Trail|Railroad|Railway|Power|Light|Gas|Bar|Life")
PLACES = {}                              # place -> its State, learned from the corpus (places)


def places(texts):
    """{place: State}: the towns the documents write with their State ('Atlantic City, N.J.', 'Glassboro, New
    Jersey', 'Des Moines, Iowa'), where they so write it at least twice, nearly always with the one State (nine
    times in ten), and not mostly without it (a place word the documents use alone thirty times for each time with
    a State, 'Washington', 'Lincoln', is no mark of a State); not a name of an organization, a newspaper, a building.
    A newspaper's or a reporter's 'New York' (followed by 'Times') or 'Washington' (the city) is no State."""
    import collections
    full = "|".join(re.escape(x) for x in sorted(STATES, key=len, reverse=True) if x != "Washington")
    abbr = "|".join(re.escape(a).replace(r"\.", r"\.\s?") + r"\." for a in sorted(ABBR, key=len, reverse=True) if a != "Wash")
    place = r"((?:[A-Z][a-z]+\.? ){0,2}[A-Z][a-z]+)"
    # a State in full, not where it names a newspaper or a city ('New York Times', 'Kansas City', 'Des Moines Register'
    # is not 'Des Moines, Iowa'); an abbreviation, or APP's postal code ('Atlantic City, NJ'). 'Washington' is the city
    # ('National Press Club, Washington'), not the State.
    postal = "|".join(sorted(POSTAL, key=len, reverse=True))
    rx = re.compile(rf"\b{place}, (?:({full})(?![a-z])(?!\s+(?:{NAMED})\b)|({abbr})|({postal})(?![A-Za-z]))")
    org = re.compile(r"\b(Committee|Party|Press|Conference|Meeting|Association|Division|Company|Co|Workers|Editors|Bill|"
                     r"Club|Unit|Campaign|Railway|Railroad|Department|Council|Union|Hotel|Building|Office|Board|"
                     r"Resources|Steps|Plaza|Square|Coliseum|Auditorium|Times|Herald|News|Post|Tribune|Journal|Rally|Mrs|"
                     r"Disagreements|Recession|God|Agency|Counties|Center)\b")
    norm = {re.sub(r"\s", "", a + "."): st for a, st in ABBR.items()}
    pairs = collections.Counter()
    for t in texts:
        for m in rx.finditer(t):
            st = m.group(2) or norm.get(re.sub(r"\s", "", m.group(3) or "")) or POSTAL.get(m.group(4) or "")
            if st and m.group(1) not in STATES and not org.search(m.group(1)):
                pairs[(m.group(1), st)] += 1
    by = collections.defaultdict(collections.Counter)
    for (pl, st), n in pairs.items():
        by[pl][st] += n
    cand = {}
    for pl, c in by.items():
        st, n = c.most_common(1)[0]
        if n >= 2 and n >= 0.9 * sum(c.values()):
            cand[pl] = (st, sum(c.values()))
    if not cand:
        return {}
    every = collections.Counter()        # each candidate's uses, with a State or without, in one pass
    big = re.compile(r"\b(" + "|".join(re.escape(x) for x in sorted(cand, key=len, reverse=True)) + r")\b")
    for t in texts:
        every.update(m.group(1) for m in big.finditer(t))
    return {pl: st for pl, (st, n) in cand.items() if every[pl] <= 30 * n}


def marks(p, mine, others):
    """What in a document marks the person apart from others of the surname and title: his name in full (his forms),
    the States his offices name that none of theirs does ('Iowa' for Harold E. Hughes), and the places in those
    States (PLACES: 'Des Moines'; 'Atlantic City', 'Glassboro', 'Princeton' for Richard J. Hughes)."""
    sts = [st for st in STATES if re.search(rf"\b{st.lower()}\b", mine)
           and not any(re.search(rf"\b{st.lower()}\b", o) for o in others)
           and not (st == "Virginia" and "west virginia" in mine)]
    pls = [pl for pl, st in PLACES.items() if (st if isinstance(st, list) else [st]) and set(st if isinstance(st, list) else [st]) & set(sts)]
    alts = [x for x in [forms(p)] + [rf"\b{re.escape(x)}\b" for x in sts + sorted(pls, key=len, reverse=True)] if x]
    return re.compile("|".join(alts)) if alts else None


def holds(p, title, day, office_text):
    """Whether the person held the title on the day (ISO): True, False, or None where nothing says. His `tenure` in
    sources/app-matches.yaml ({title: [from, to]}) where given; else the years his offices give after the title's word
    ('governor of iowa 1963 69'), True only for a year strictly inside them, False for a year outside."""
    ten = ((MATCHES.get(p["name"]) or {}).get("tenure") or {}).get(title)
    if ten:
        return str(ten[0]) <= day <= str(ten[1])
    w = dict(TITLE_WORDS).get(title)
    spans = []
    for m in re.finditer(rf"(?:{w})[^0-9;]{{0,40}}?\b(1[89]\d\d)\b(?:\s*[-–]?\s*(\d{{2,4}})\b)?", office_text):
        a = int(m.group(1))
        b = m.group(2)
        b = int(b) if b and len(b) == 4 else (a // 100 * 100 + int(b) if b else a)
        spans.append((a, b))
    if not spans:
        return None
    y = int(day[:4])
    if any(a < y < b for a, b in spans):
        return True
    if all(y < a or y > b for a, b in spans):
        return False
    return None


def death_year(series, p):
    from bib import lives as L
    e = L.bd_entry(p["sur"], p["given"], True, (), L.person_suffix(series, p)[0])
    if e and L.roster_pointers(p["sur"], p["given"], p["names"]):
        m = re.findall(r"died[^;]*?\b(1[89]\d\d|20\d\d)\b", e["text"])
        if m:
            return m[-1]
    pc = POCOM.get("persons", {}).get(POCOM.get("match", {}).get(key_of(p["name"])), {})
    return pc.get("death") or None


def main():
    cache = sys.argv[1]
    rows = [json.loads(l) for l in open(os.path.join(cache, "index.jsonl"), encoding="utf-8")]
    with open(os.path.join(OUT, "app-index.jsonl"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps({k: r[k] for k in ("url", "date", "who", "title")}, ensure_ascii=False) + "\n")
    global ROLES, POCOM
    series = store.Series()
    from bib.lives import everyone as all_people
    everyone = all_people(series)        # the persons FRUS's lists alone give too (sources/frus-names/persons.json)
    ROLES = {}
    for l in series.lists.values():
        for sec, e in l.entries():
            if (sec.code or "").startswith("III") and e.get("s"):
                for n in re.split(r";\s*", e["s"]):
                    n = re.sub(r"\s*\(.*?\)\s*$", "", n).strip()
                    ROLES[n] = ROLES.get(n, "") + " " + (e.get("r") or "")
    global MATCHES
    mp = os.path.join(OUT, "app-matches.yaml")
    MATCHES = (store.load_yaml(mp) or {}) if os.path.exists(mp) else {}
    pp = os.path.join(OUT, "pocom.json")
    POCOM = json.load(open(pp, encoding="utf-8")) if os.path.exists(pp) else {}
    from bib.lives import person_suffix
    office = {p["name"]: "" if p.get("frus") else offices_text(series, p) for p in everyone}
    by_sur = {}
    for p in everyone:
        by_sur.setdefault(p["sur"], []).append(p)
    # first name and surname shared by two entries: the text cannot tell them apart
    seen = {}
    for p in everyone:
        for n in p["names"]:
            g = split_name(n)[1].split()
            if g:
                seen.setdefault((p["sur"], g[0]), set()).add(p["name"])
    surnames = set(by_sur)
    texts, docs_by_sur = [], {}
    for i, r in enumerate(rows):
        h = hashlib.sha1(r["url"].encode()).hexdigest()[:16]
        path = os.path.join(cache, "docs", h + ".json.gz")
        t = json.load(gzip.open(path, "rt", encoding="utf-8"))["text"] if os.path.exists(path) else ""
        texts.append(t)
        if r["title"].endswith("Event Timeline"):   # APP's own chronology of a presidency, not a document
            continue
        # the words, a possessive's 's dropped ('Roth's' is Roth)
        for w in {re.sub(r"['’]s$", "", x) for x in re.findall(r"[A-Z][a-zA-Z'’\-]+", t)} & surnames:
            docs_by_sur.setdefault(w, []).append(i)
    global PLACES
    PLACES = places([r["title"] + " " + t for r, t in zip(rows, texts)])
    hp = os.path.join(OUT, "app-places.yaml")      # kept by hand: a place in two States ('Delaware Water Gap')
    PLACES.update({k: list(v) for k, v in ((store.load_yaml(hp) or {}) if os.path.exists(hp) else {}).items()})
    print(len(PLACES), "places with their States", file=sys.stderr)
    year = lambda i: (re.findall(r"\d{4}", rows[i]["date"]) or ["0"])[-1]
    names_of = {p["name"]: p for p in everyone}
    out, checks = {}, {}                 # checks: {key: {document line: [title, [the others it may be]]}}
    for p in everyone:
        if natural(p["name"]):
            # a name in its own order: its forms as phrases ('Ngo Dinh Diem', 'President Diem', 'Mao Tse-tung'), not
            # the comma forms a list writes; 'Ho Chi Minh' not in 'the Ho Chi Minh Trail' or 'Ho Chi Minh City'
            fs = [f for f in name_forms(p["name"]) if "," not in f]
            words = {f.split()[-1] for f in fs}
            rx = re.compile(r"\b(?:" + "|".join(re.escape(f).replace(r"\ ", r"\s+") for f in fs) + r")\b"
                            r"(?!\s+(?:Trail|trail|City|city))")
            hits = [i for i, t in enumerate(texts) if not rows[i]["title"].endswith("Event Timeline")
                    and any(w in t for w in words) and rx.search(t)]
            if hits:
                out[key_of(p["name"])] = hits
            continue
        cand = docs_by_sur.get(p["sur"], [])
        if not cand:
            continue
        group = set().union(*[v for (s, g), v in seen.items() if s == p["sur"] and p["name"] in v]) or {p["name"]}
        span = None                      # (from, to) years, for a father and a son of one name
        apart = False                    # namesakes whose further given names differ: John W. and John G. Dean
        strict = bool((MATCHES.get(p["name"]) or {}).get("strict"))   # a son known by his suffix (app-matches)
        tail = ""                        # a father whose son is strict: not where the son's suffix follows
        if p.get("frus"):                # one FRUS's lists alone give: not where another name follows ('John
            tail = r"(?!\s+(?!Jr\b|Sr\b|I+\b)[A-Z][a-z])"   # Fitzgerald Kennedy' is not John F. Fitzgerald)
        if strict:
            apart, group = True, {p["name"]}
        if len(group) > 1:
            others = [names_of[n] for n in group if n != p["name"]]
            if all(not same_person(p["sur"], p["given"], q["sur"], q["given"]) for q in others):
                apart = True
            elif len(group) != 2:
                continue
        if len(group) > 1 and not apart:
            other = names_of[next(n for n in group if n != p["name"])]
            mine_s, other_s = person_suffix(series, p)[0], person_suffix(series, other)[0]
            if bool(mine_s) == bool(other_s):
                continue                 # neither is the son by his suffix: the text cannot tell them apart
            elder = other if mine_s else p
            if elder is p and (MATCHES.get(other["name"]) or {}).get("strict"):
                tail = rf"(?!,?\s+{re.escape(other_s)}\b)"   # the son goes by his suffix: every year is the father's
            else:
                died = death_year(series, elder)
                if not died:
                    continue
                span = ("0", died) if elder is p else (str(int(died) + 1), "9999")
                cand = [i for i in cand if span[0] <= year(i) <= span[1]]
        hand = (MATCHES.get(p["name"]) or {}).get("bare")
        if apart:
            # only the forms that tell him from his namesake: a further given name or initial, or his suffix; the
            # bare name where sources/app-matches.yaml gives it to him, for the years it gives
            pats = [forms(p, strict=True, sfx=person_suffix(series, p)[0], mids_ok=not strict)]
            if hand:
                lo_, hi_ = (str(x) for x in hand)
                also = [re.escape(x) for x in (MATCHES.get(p["name"]) or {}).get("forms") or []]
                bare = "|".join(x for x in [forms(p)] + [rf"\b{a}\b" for a in also] if x)
                bare_hits = {i for i in cand if lo_ <= year(i) <= hi_ and bare and re.search(bare, texts[i])}
        else:
            pats = [forms(p) and forms(p) + tail]
        rivals = [q for q in by_sur[p["sur"]] if q is not p]
        mine_t = [t for t, w in TITLE_WORDS if re.search(w, office[p["name"]])
                  and not any(re.search(w, office[q["name"]]) for q in rivals)]
        if mine_t and not strict:        # a strict son's titles were his father's too ('General Clay', 'Senator Taft')
            pats.append(rf"\b(?:{'|'.join(mine_t)})\s+{re.escape(p['sur'])}\b")
        if not any(pats):
            continue                     # nothing to look for: an empty pattern would match every document
        rx = re.compile("|".join(x for x in pats if x))
        own = {store.fold(f"{split_name(n)[1].split()[0]} {p['sur']}") for n in p["names"] if split_name(n)[1]}
        hits = [i for i in cand if (rx.search(texts[i]) or (apart and hand and i in bare_hits))
                and not any(o and o in store.fold(rows[i]["who"]) for o in own)]
        # a title he shares with another of the surname ('Governor Hughes': Harold E. of Iowa, Richard J. of New
        # Jersey): the document is his where it also names his State or gives his name in full, and nothing of the
        # other's
        shared_t = [(t, w) for t, w in TITLE_WORDS if re.search(w, office[p["name"]])
                    and any(re.search(w, office[q["name"]]) for q in rivals)] if not strict and not p.get("frus") else []
        for t, w in shared_t:
            others = [q for q in rivals if re.search(w, office[q["name"]])]
            mine = marks(p, office[p["name"]], [office[q["name"]] for q in others])
            theirs = [marks(q, office[q["name"]], [office[p["name"]]]) for q in others]
            trx = re.compile(rf"\b(?:{t})\s+{re.escape(p['sur'])}\b")
            for i in cand:
                if i in hits or not trx.search(texts[i]):
                    continue
                tx = rows[i]["title"] + " " + texts[i]     # the title names the place too ('Bergen, New Jersey')
                me_, them = bool(mine and mine.search(tx)), [bool(m and m.search(tx)) for m in theirs]
                if me_ and not any(them):
                    hits.append(i)
                    continue
                if any(them) and not me_:
                    continue
                # the text does not settle it: who held the title that day (tenure); else all of them, with a Check
                day = datetime.datetime.strptime(rows[i]["date"], "%b %d, %Y").date().isoformat()
                held = holds(p, t, day, office[p["name"]])
                theirs_held = [holds(q, t, day, office[q["name"]]) for q in others]
                if held is True and all(h is False for h in theirs_held):
                    hits.append(i)           # he alone held it that day
                elif held is not False and ((MATCHES.get(p["name"]) or {}).get("tenure") or {}).get(t):
                    # a pair kept by hand (app-matches.yaml, tenure): each of them, with a Check
                    hits.append(i)
                    checks.setdefault(key_of(p["name"]), {})[str(i)] = [t, [q["name"] for q in others]]
        hits.sort()
        if hits:
            out[key_of(p["name"])] = hits
    with open(os.path.join(OUT, "app-names-checks.json"), "w", encoding="utf-8") as f:
        json.dump(checks, f, separators=(",", ":"))
    letters = {}
    for k, v in out.items():
        letters.setdefault(k[0].upper(), {})[k] = v
    os.makedirs(os.path.join(OUT, "app-names"), exist_ok=True)
    for f in os.listdir(os.path.join(OUT, "app-names")):
        os.remove(os.path.join(OUT, "app-names", f))
    for L, v in letters.items():
        with open(os.path.join(OUT, "app-names", f"{L}.json"), "w", encoding="utf-8") as f:
            json.dump(v, f, separators=(",", ":"))
    print(len(out), "persons named", sum(len(v) for v in out.values()), "references")


if __name__ == "__main__":
    main()
