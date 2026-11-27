"""The Places pages (the owner, Nov. 26, 2026: "it's hard to follow any given national thread anywhere outside the
United States and China, and hard to follow any subnational or local thread anywhere"; ruling 66, the default taken;
notes/proposals/place-pages.md): a page for each nation, each U.S. State, each Chinese province of 1966 and each city
of CITY_MIN entries or more, built on every build from the entries' `place:`, their tags and the visibility register.
Nothing is stored: no entry is re-read or re-threaded for them.

    ./bib build places       build/places-<slug>.html, a page a place (and its parts); threads.html, whose section
                             "Places" lists them (threads.py, STYLE 7)

STYLE
 1. Which places have a page. A nation: each polity of sources/polities.yaml that is no organization (`org`) and
    stands for itself (FOLD: the National Liberation Front's entries go on both North and South Vietnam's pages, the owner, Nov. 26, 2026; the Pathet
    Lao, a polity of its own in the register, is Laos's here, since its acts are in Laos), with an entry. A State:
    each gazetteer row `kind: state` (the fifty), with an entry. A province: each provincial unit of the PRC as of
    1966 on the map of China (sources/china/units.json: the provinces, autonomous regions and the two
    municipalities), with an entry. A city: each other row of the gazetteer that is no province of China, with
    CITY_MIN entries or more; a city whose key is a nation's or a province's (Singapore; Peking and Shanghai, the
    municipalities) has that page alone.
 2. Which entries a page holds (every calendar entry with a `when`, a subentry too):
    a nation's: those that took place there (a `place:` key whose gazetteer row is `in` the nation, or has a State's
    `st` for the United States) and those that concern it (the visibility register's address, vis.address: the
    polities of the entry's name, place, State, city, province and `polity:` tags; where its tags give none, its
    threads'). Each line marked which in its rubric, before the threads: "In Laos", "About Laos" (MARK).
    a State's: those that took place in it (a `place:` row whose `st` is the State's) and those tagged for it: its
    `state:` tag (its postal code, or its gazetteer key), or the `city:` or `place:` tag of a place in it.
    a province's: those that took place in it (a `place:` key the map of China puts in the province: cnmap.placed's
    points and units), those tagged `province:<the unit>`, and those whose line (`c`) names it, in Pinyin or in
    characters (named_provinces; the owner, Nov. 27, 2026: the provinces the entries name had no "Places:" link; the
    municipalities, Peking and Shanghai, by place only, since a line's "Peking" is the city).
    a city's: those whose `place:` is the city (a key or an alias of its row) or that carry its `city:` or `place:`
    tag.
 3. The page is a thread's page (threads.py): the same template and styles, the same day headings, year and month
    headings, the same entries rendered by the calendar's renderer, the same anchors (`t-<id>`, `t-d<date>`: threads
    STYLE 3), the same parts' bar, seam and forwarding, the same map at the head where the place lies on one of the
    two maps (maps.py; the place's own placed entries alone, MAP). What differs: no statement (a place has none);
    the head's line says what the page holds and why; a nation's rubric carries its mark.
 4. The budget (pages.py): a place's page over budget is in parts by date as a thread's is (threads.plan_parts, the
    same budget and fill), its own page then the index; pages.yaml `places:` holds a plan once `./bib pages --plan`
    has written it, so that the parts keep their names. A place with no plan yet whose page comes out over budget is
    planned at the build from its own entries' sizes (pages._thread_sizes), so no page is ever written over budget.
 5. The index: threads.html, after the threads, a section "Places" (h2#places): the nations, the States, the
    provinces, the cities, each a list in the threads' own markup (ol.e.thx), by name, each with its count and, for a
    split page, its parts by span.
 6. The dateline (the owner, Nov. 26, 2026, 9:19 p.m.; ruling 67): a place in an entry's dateline that has a page of
    its own links to it, in the one style of the calendar's links within the site (templates/list.html, the rule for
    `:where(main) a`: the text's own colour, a faint solid underline, darker on hover). No new style; the dateline is
    no longer than it was. A tap on the link follows it, though the rubric beside it is cut short (dateline.py,
    SCRIPT). The clock's city, given where the entry has no place, is not linked: it is not a place of record.
 7. "Places:" (the same ruling): in every calendar entry's citation block, just before "Names:" (else at its end), a
    sentence written by the build, never stored: the nations, States, provinces and cities with a page that the
    entry took place in or concerns (STYLE 2), in that order (the index's: the nations as the register lists them, the
    others by name), each linked to its page as the names are.
 8. The place tags held to the entry (the owner, Nov. 26, 2026, 9:36 p.m.: "What would minimize error at least
    cost?"; ruling 67; notes/proposals/place-pages.md, "The States' tags"), in `./bib check` (check.entry_problems):
    an error, a tag that names nothing (tag_errors): `state:` not a postal code of the States or D.C. in lower case
    (sources.STATES), `polity:` not in sources/polities.yaml. A warning, a tag nothing else in the calendar entry
    supports (tag_findings; `ok:<rule>` on the entry where it is right): [polity-tag], a nation's tag (not an
    organization's) none of whose nations (FOLD both ways) the entry's place, its people (their register rows, private
    persons too), its threads, its other place tags, its `vis:` rulings or the gazetteer places its line names give,
    and whose name, adjective, capital or code (nation_words, NATION_WORDS) its line does not write; [state-tag], on an
    entry placed outside the State (in another State, D.C. or abroad), a State tag that no thread of the State (a
    thread or an ancestor whose slug is the State's), no city or place tag in it, no gazetteer place in it that the
    line names and no word of the line for it (state_words: its name, its Bluebook abbreviation) supports; [city-tag],
    on an entry placed only at other places, in another State or nation, a city tag whose city the line does not name.
    An entry with no place is never warned on its State or city tags. The line's words are the narrowing: without
    them the polity rule raised 2,883 warnings over the calendar, most of them right (the countries of a delegation
    Zhou receives, named in the line, their people untagged); the State and city rules, 266 and 68, most of them acts
    in Washington or at a convention about a State or a city the line names.
 9. What a place tag names (tag_name), for `./bib patch-check` (patchcheck.py, STYLE 15): a polity's register name, a
    State's name, a city's or place's gazetteer name, a province's on either map.
"""
import datetime
import html
import json
import os
import re

from . import store

PREFIX = "t-"                    # the anchors of a thread's page (threads STYLE 3): the place pages are thread pages
PAGE = "places-"
CITY_MIN = 50                    # a city with this many entries or more has a page (ruling 66)
FOLD = {"nlf": ("drv", "rvn"), "pathet-lao": ("laos",)}   # a polity on others' pages (STYLE 1)
KINDS = [("nation", "Nations"), ("state", "States"), ("province", "Provinces of China, 1966"), ("city", "Cities")]
_C = {}


def esc(t):
    return html.escape(str(t), quote=True)


def page_of(slug):
    return f"{PAGE}{slug}"


def reset():
    _C.clear()


# ---------------------------------------------------------------- what each entry is in (STYLE 2)

def _cal(series):
    return next((l for l in series.lists.values() if l.kind == "calendar"), None)


def _fold(p):
    """The pages a polity's entries go on: its own, or those FOLD names."""
    return FOLD.get(p, (p,))


def nations():
    """{polity id: name}: the polities that are nations (STYLE 1), in the register's order."""
    from . import vis
    out = {}
    for k, v in vis.polities()["polities"].items():
        if (v or {}).get("org") or (v or {}).get("folded") or k in FOLD:
            continue
        out[k] = short_name((v or {}).get("name") or k)
    return out


def short_name(name):
    """A polity's name without its gloss: "China (the People's Republic)" -> "China"; a parenthesis that tells one
    from another kept ("Congo (Brazzaville)", "United Arab Republic (Egypt)")."""
    return re.sub(r"\s*\(the .*\)\s*$", "", str(name)).strip() or str(name)


THE = re.compile(r"^(United |Soviet |Republic |Democratic |German |Dominican |Central African |Congo\b|Netherlands$|"
                 r"Philippines$|Ivory Coast$|Vatican$)")


def in_words(pl):
    """A place's name as it reads after "in" or "about": "the United States", "the Congo"; "Laos", "Alabama"."""
    n = pl["name"]
    return f"the {n}" if pl["kind"] == "nation" and THE.match(n) else n


def states():
    """{postal code: gazetteer row}: the States (gazetteer rows `kind: state`)."""
    from . import places
    rows, _ = places._load()
    return {str(r["st"]).upper(): r for r in rows if r.get("kind") == "state" and r.get("st")}


def provinces():
    """{unit id: name}: the PRC's provincial units of 1966 on the map of China (cnmap.units)."""
    from . import cnmap
    return {u["id"]: u["name"] for u in cnmap.units().values() if u.get("c") == "prc"}


def _row_polities(row):
    """A gazetteer row's nations: its `in`, folded; a U.S. place (`st`) the United States's."""
    if row.get("st"):
        return ["us"]
    return [q for p in store.as_list(row.get("in")) if p and p != "?" for q in _fold(str(p))]


def tag_row(tag):
    """The gazetteer row a `city:` or `place:` tag names, or None."""
    from . import places
    ns, _, k = str(tag).partition(":")
    return places.get(k) if ns in ("city", "place") and k else None


NAMED_SKIP = {"peking", "shanghai"}       # municipalities: a line's "Peking" is the city, its place's business


def _province_patterns():
    """[(unit id, compiled pattern)]: each PRC province's and region's name of 1966 as the calendar writes it (the
    map's name, in Pinyin) and in characters (its `made_of` name less 省 or 自治区), the municipalities left out."""
    from . import cnmap
    out = []
    for u in cnmap.units().values():
        if u.get("c") != "prc" or u["id"] in NAMED_SKIP:
            continue
        names = [u["name"]] + [re.sub(r"(省|维吾尔自治区|回族自治区|壮族自治区|自治区)$", "", str(m))
                                for m in (u.get("made_of") or [])]
        alts = "|".join(re.escape(n) for n in names if n)
        out.append((u["id"], re.compile(rf"(?<![A-Za-z])(?:{alts})(?![A-Za-z])")))
    return out


_PATS = None


def named_provinces(text):
    """The PRC provinces and regions a line names (STYLE 2): an entry that names Hebei is about Hebei, wherever it
    took place."""
    global _PATS
    from . import cnmap
    key = tuple(sorted(cnmap.units()))
    if _PATS is None or _PATS[0] != key:                # the map's units, read once while they stay the same
        _PATS = (key, _province_patterns())
    return {pid for pid, pat in _PATS[1] if pat.search(text)}


def where(series, lst, e):
    """What an entry is in (STYLE 2): {"there": {kind: set of slugs}, "tagged": {kind: set of slugs}}, kind one of
    nation, state, province, city; a nation's "tagged" its concern by the register."""
    from . import cnmap, places, vis
    there = {k: set() for k, _ in KINDS}
    tagged = {k: set() for k, _ in KINDS}
    codes = states()
    ST = {c.lower(): c for c in codes}
    st_keys = {str(r["key"]): c for c, r in codes.items()}
    prov = provinces()
    G = cnmap.gazetteer()
    for k in places.keys(e):
        r = places.get(k)
        if r is None:
            continue
        there["nation"] |= set(_row_polities(r))
        if str(r.get("st") or "").upper() in codes:
            there["state"].add(str(r["st"]).upper())
        p = G.get(r["key"])
        if p and p.get("unit") in prov:
            there["province"].add(p["unit"])
        if r.get("kind") != "state":
            there["city"].add(r["key"])
    for g in e.get("tags") or []:
        g = str(g)
        ns, _, k = g.partition(":")
        if ns == "state":
            c = ST.get(k) or st_keys.get(k)
            if c:
                tagged["state"].add(c)
        elif ns in ("city", "place"):
            r = tag_row(g)
            if r is not None:
                tagged["city"].add(r["key"])
                if str(r.get("st") or "").upper() in codes:
                    tagged["state"].add(str(r["st"]).upper())
        elif ns == "province" and k in prov:
            tagged["province"].add(k)
    tagged["province"] |= named_provinces(e.get("c") or "")      # the line names it (the owner, Nov. 27, 2026)
    date = vis.iso(e.get("date")) or "1960-01-01"
    addr = vis.address(lst, e, None, date)[0]
    tagged["nation"] = {q for p in addr if not vis.is_org(p) for q in _fold(p)}
    return {"there": there, "tagged": tagged}


def gather(series):
    """{(kind, slug): {"name", "kind", "slug", "ents": [entries in the calendar's order], "there": set of ids}} for
    every place with a page (STYLE 1, 2), and the order of the index: nations as the register lists them, the rest
    by name."""
    key = id(series)
    if _C.get("key") == key:
        return _C["got"]
    from . import chron, places
    lst = _cal(series)
    got = {}
    if lst is None:
        return got
    N, S, P = nations(), states(), provinces()
    names = {"nation": N, "state": {c: r["name"] for c, r in S.items()}, "province": P}
    acc, each = {}, {}
    for _, e in lst.entries():
        if "when" not in e:
            continue
        w = each[e["id"]] = where(series, lst, e)
        for kind, _ in KINDS:
            for slug in w["there"][kind] | w["tagged"][kind]:
                a = acc.setdefault((kind, slug), [[], set()])
                a[0].append(e)
                if slug in w["there"][kind]:
                    a[1].add(e["id"])
    taken = set(N) | set(P)
    for (kind, slug), (ents, there) in acc.items():
        if kind == "city":
            r = places.get(slug)
            if r is None or len(ents) < CITY_MIN or slug in taken or r.get("kind") == "state":
                continue
            if slug in P or (cnmap_area(slug)):
                continue
            name = places.name_on(r, None)
        elif slug not in names[kind]:
            continue
        else:
            name = names[kind][slug]
        page = page_slug(kind, slug)
        got[(kind, slug)] = {"kind": kind, "slug": slug, "page": page_of(page), "name": name,
                             "ents": chron.sort(lst, ents), "there": there}
    order = {k: i for i, k in enumerate(N)}
    got = dict(sorted(got.items(), key=lambda kv: ([k for k, _ in KINDS].index(kv[0][0]),
                                                   order.get(kv[0][1], 0) if kv[0][0] == "nation" else 0,
                                                   store.fold(kv[1]["name"]).lower())))
    _C.update(key=key, got=got, each=each)
    return got


def cnmap_area(key):
    """A gazetteer key the map of China takes as a unit, not a point (a province named as a place)."""
    from . import cnmap
    p = cnmap.gazetteer().get(key)
    return bool(p and p.get("area"))


def page_slug(kind, slug):
    """A place's page's name after `places-`: a nation's polity id, a State's gazetteer key (alabama,
    new-york-state), a province's unit id, a city's gazetteer key."""
    if kind == "state":
        return str(states()[slug]["key"])
    return str(slug)


# ---------------------------------------------------------------- the pages (STYLE 3, 4)

def parts(page):
    """A place's parts where the plan splits it (pages.yaml `places:`; else as an earlier build divided it, kept in
    .cache: STYLE 4), else None: [{page, from, label}]."""
    from . import pages
    slug = page[len(PAGE):]
    if "planned" not in _C:                      # read once a run
        _C["planned"] = pages.planned("places")
    ps = (pages.conf().get("places") or {}).get(slug) or _C["planned"].get(slug)
    return [dict(p) for p in ps] if ps else None


def _mark(pl):
    """A nation's rubric's mark (STYLE 2): "In Laos" where the entry took place there, else "About Laos"."""
    if pl["kind"] != "nation":
        return None
    there, name = pl["there"], esc(in_words(pl))
    return lambda e: f"In {name}" if e["id"] in there else f"About {name}"


def _map(pl):
    """The map a place's page carries (STYLE 3): China's for China, the Republic of China, a province and a place on
    it; Indochina's for the two Vietnams, Laos and Cambodia and a place on it; else None."""
    from . import cnmap, vnmap
    k, s = pl["kind"], pl["slug"]
    if k == "province" or (k == "nation" and s in ("prc", "roc")):
        return cnmap
    if k == "nation" and s in ("rvn", "drv", "laos", "cambodia"):
        return vnmap
    if k == "city":
        p = cnmap.gazetteer().get(s)
        if p and p.get("lat") is not None:
            return cnmap
        if s in vnmap.gazetteer():
            return vnmap
    return None


def figure(series, pl, ents, lo, hi):
    from . import maps
    m = _map(pl)
    if m is None or not m.ready():
        return ""
    return maps.figure(series, m, lo, hi, here=PREFIX, ids={e["id"] for e in ents})


def _what(pl, n, whole, n_there):
    """The head's line (STYLE 3): what the page holds and why."""
    name, k = esc(in_words(pl)), pl["kind"]
    here = "" if whole else " here"
    if k == "nation":
        why = (f"those that took place in {name}, marked <i>In {name}</i>, and those that concern it by its people, "
               f"its places or its threads, marked <i>About {name}</i>")
        if whole:
            why = (f"{n_there:,} that took place in {name}, marked <i>In {name}</i>, and {n - n_there:,} that concern "
                   f"it by its people, its places or its threads, marked <i>About {name}</i>")
    elif k == "state":
        why = f"those that took place in {name} and those that carry its tag or the tag of a city in it"
    elif k == "province":
        why = f"those that took place in {name}, the province as it was in 1966"
    else:
        why = f"those that took place in {name} and those that carry its tag"
    return f"{_n(n)}{here}, in the calendar's order: {why}. Each as the calendar gives it; its □ leads to it there."


def _n(n):
    return f"{n:,} {'entry' if n == 1 else 'entries'}"


def _head(pl, n, whole, n_there):
    links = ['<a href="threads.html#places">All places</a>']
    return [f'<p class="logic">{_what(pl, n, whole, n_there)} ' + ". ".join(links) + ".</p>"]


def title(pl, part=None):
    return f"Places: {pl['name']}" + (f", {part['label']}" if part else "")


def place_page(series, linker, template, pl, ents, part=None, ps=None):
    """One page: the place's (part None), or a part of it (ps the parts, part its index): a thread's page (threads.py,
    thread_page), its head the place's."""
    from . import build, calsplit, chron, cjk, pages, threads, vispage
    me = ps[part]["page"] if ps else pl["page"]
    text_html = build.list_text_html(series, _cal(series).key, linker)
    lst = _cal(series)
    calsplit.CUR.update(half=None, mode="list")
    lo, hi = calsplit.part_range(lst, None)
    if ps:
        lo = max(lo, datetime.date.fromisoformat(threads._pad(ps[part]["from"]))) if part else lo
        if part + 1 < len(ps):
            hi = datetime.date.fromisoformat(threads._pad(ps[part + 1]["from"])) - datetime.timedelta(days=1)
    main = [f"<h1>{esc(pl['name'])}" + (f", {esc(ps[part]['label'])}" if ps else "") + "</h1>"]
    main += _head(pl, len(ents), not ps, sum(1 for e in ents if e["id"] in pl["there"]))
    if ps:
        main.append(pages.bar(pl["page"], ps, part))
    main += [f for f in [figure(series, pl, ents, lo, hi)] if f]
    main.append(vispage.MARK)
    vispage.begin()
    with cjk.as_page(series, lst, ents, me):
        body = threads._days(series, lst, chron.groups(lst, ents), text_html, build.thread_name, _mark(pl))
    if ps:
        body.append(pages.seam(pl["page"], ps, part))
    text = "\n".join(body)
    own = set(threads.IDS.findall("\n".join(main) + text))
    main.append(threads._rewrite(text, own))
    return threads._wrap(series, template, title(pl, ps[part] if ps else None), main, threads.onward(lst.key), "places")


def place_index(series, template, pl, ps, counts):
    """A split place's own page: its head, its map, its parts, and old links forwarded (threads.thread_index)."""
    from . import calsplit, pages, threads
    lst = _cal(series)
    lo, hi = calsplit.part_range(lst, None)
    main = [f"<h1>{esc(pl['name'])}</h1>"] + _head(pl, len(pl["ents"]), True,
                                                    sum(1 for e in pl["ents"] if e["id"] in pl["there"]))
    main += [f for f in [figure(series, pl, pl["ents"], lo, hi)] if f]
    main.append('<ul class="pgl">' + "".join(
        f'<li><a href="{esc(p["page"])}.html">{esc(p["label"])}</a>: {_n(n)}</li>' for p, n in zip(ps, counts)) + "</ul>")
    return threads._wrap(series, template, title(pl), main, pages.PART_CSS + threads.forward(ps, pl["page"]), "places")


def _split(pl, ps):
    from . import loose, threads
    by = [[] for _ in ps]
    for e in pl["ents"]:
        by[threads.part_index(ps, loose.place_iso(e))].append(e)
    return by


def plan(page_html, pl):
    """STYLE 4: the parts a page over budget is cut into, from its own entries' sizes (pages._thread_sizes; the
    threads' planner, threads.plan_parts), or None where it is within budget or holds one part's worth."""
    from . import pages, threads
    if len(page_html.encode("utf-8")) <= pages.budget(f"{pl['page']}.html"):
        return None
    sizes, rest = pages._thread_sizes(page_html)
    target = int(pages.budget(f"{pl['page']}.html") * pages.fill())
    ps = threads.plan_parts(pl["slug"], sizes, target - rest, page=pl["page"]) if sizes else []
    return ps if len(ps) > 1 else None


def pages_(series, linker, template, only=None, save=True):
    """(file name, html), one page at a time: every place's page (a split place's index and parts), and a part a
    later plan dropped (pages.yaml `retired`) as a page that forwards. only: these pages' slugs alone (a test, the
    preview: "laos", "alabama", "shaanxi", "chicago"). save: keep a plan made at the build in .cache (STYLE 4)."""
    from . import pages, threads
    got = gather(series)
    for pl in got.values():
        slug = pl["page"][len(PAGE):]
        if only and slug not in only:
            continue
        ps = parts(pl["page"])
        if not ps:
            page = place_page(series, linker, template, pl, pl["ents"])
            ps = plan(page, pl)
            if not ps:
                yield f"{pl['page']}.html", page
                continue
            pl["planned"] = ps                   # planned at the build (STYLE 4): `./bib pages --plan` keeps it
            if save:
                pages.save_planned("places", slug, ps)
        by = _split(pl, ps)
        yield f"{pl['page']}.html", place_index(series, template, pl, ps, [len(b) for b in by])
        for i, p in enumerate(ps):
            yield f"{p['page']}.html", place_page(series, linker, template, pl, by[i], i, ps)
    live = set(pages.live_pages())
    for old in pages.conf().get("retired") or []:
        if not old.startswith(PAGE) or old in live:
            continue
        pl = retired_of(got, old)
        if pl and (not only or pl["page"][len(PAGE):] in only):
            ps = parts(pl["page"]) or pl.get("planned") or [{"from": "", "page": pl["page"]}]
            yield f"{old}.html", pages.stub("Places", pl["page"], {}, old).replace(
                pages.forward_script({}, old), threads.forward(ps, old))


def retired_of(got, old):
    """The place a dropped part was a part of: the page's name less its unit (threads.retired_of)."""
    from . import threads
    m = threads.UNIT.search(old)
    base = old[:m.start()] if m else None
    return next((pl for pl in got.values() if pl["page"] == base), None)


# ---------------------------------------------------------------- the index's section (STYLE 5)

def index_section(series):
    """The section "Places" of threads.html: [html], or [] where no place has a page."""
    got = gather(series)
    if not got:
        return []
    out = ['<h2 id="places" data-short="Places" data-crumb="Places">Places</h2>',
           '<p class="logic">A page a place, built from the entries: a nation\'s holds the entries that took place '
           "there and those that concern it by its people, its places or its threads, each marked which; a State's, "
           "a province's or a city's, those that took place there and those that carry its tag. A province is as it "
           f"was in 1966; a city has a page where it has {CITY_MIN} entries or more. Each page is laid out as a "
           "thread's, and a large one is in parts by date.</p>"]
    for kind, head in KINDS:
        rows = []
        for pl in got.values():
            if pl["kind"] != kind:
                continue
            ps = parts(pl["page"]) or pl.get("planned")
            more = (": " + ", ".join(f'<a href="{esc(p["page"])}.html">{esc(p["label"])}</a>' for p in ps)) if ps else ""
            rows.append(f'<li id="pl-{esc(pl["page"][len(PAGE):])}"><span class="s"><a href="{pl["page"]}.html">'
                        f'{esc(pl["name"])}</a></span><span class="n">{_n(len(pl["ents"]))}{more}.</span></li>')
        if rows:
            out.append(f'<h3 id="places-{kind}" data-short="{esc(head)}" data-crumb="{esc(head)}">{esc(head)}</h3>')
            out.append('<ol class="e thx">' + "".join(rows) + "</ol>")
    return out


# ---------------------------------------------------------------- in every entry: the dateline and "Places:" (STYLE 6, 7)

def _series(series=None):
    """The series the place pages are gathered from: the one given, else the build's (daybook.SERIES), else None."""
    if series is not None:
        return series
    from . import daybook
    return daybook.SERIES


def _by_page(series):
    """{(kind, slug): place} for the places with a page, and {gazetteer key: place} for those a gazetteer row names: a
    city by its key, a State by its row, a province by its row as a whole."""
    got = gather(series)
    if _C.get("bykey_of") is not got:
        rows = {}
        for (kind, slug), pl in got.items():
            if kind == "city":
                rows[slug] = pl
            elif kind == "state":
                rows[str(states()[slug]["key"])] = pl
        for k, p in _province_rows().items():
            if ("province", p) in got:
                rows.setdefault(k, got[("province", p)])
        _C.update(bykey_of=got, bykey=rows)
    return got, _C["bykey"]


def _province_rows():
    from . import cnmap
    return {k: p["unit"] for k, p in cnmap.gazetteer().items() if p.get("area") and p.get("unit")}


def dateline_link(e, place, series=None):
    """STYLE 6: the page of the place a dateline names (dateline.py, STYLE 3), or None: the entry's first `place:`
    where that place itself has a page (a city, a State, a province named whole); else its `city:` or `state:` tag's,
    where the dateline names that. A clock's city (Washington for the eastern zone) is no place of record: no link."""
    from . import places
    series = _series(series)
    if series is None or not place:
        return None
    got, rows = _by_page(series)
    r = places.first(e)
    if r is not None:
        pl = rows.get(str(r["key"]))
        return pl["page"] if pl and places.name_on(r, e.get("date")) == place else None
    for g in e.get("tags") or []:
        ns, _, k = str(g).partition(":")
        if ns == "city":
            r = places.get(k)
            pl = rows.get(str(r["key"])) if r else None
        elif ns == "state":
            c = {c.lower(): c for c in states()}.get(k)
            pl = got.get(("state", c)) if c else None
        else:
            continue
        if pl and pl["name"] == place:
            return pl["page"]
    return None


def line(e, series=None):
    """STYLE 7: the "Places:" sentence of an entry's citation block, as HTML, or "": the places with a page the entry
    took place in or concerns (its nations, States, provinces, cities, in that order), each linked to its page. A State
    named as a city of the line is (New York, Washington) is written "New York State"."""
    series = _series(series)
    if series is None or "when" not in e:
        return ""
    got = gather(series)
    w = (_C.get("each") or {}).get(e["id"])
    if w is None:
        return ""
    if _C.get("pos_of") is not got:
        _C.update(pos_of=got, pos={k: i for i, k in enumerate(got)})
    pos = _C["pos"]                     # the index's order: the nations as the register lists them, the rest by name
    keys = [(kind, slug) for kind, _ in KINDS for slug in w["there"][kind] | w["tagged"][kind] if (kind, slug) in pos]
    out = [got[k] for k in sorted(keys, key=pos.get)]
    if not out:
        return ""
    cities = {pl["name"] for pl in out if pl["kind"] == "city"}
    names = [f"{pl['name']} State" if pl["kind"] == "state" and pl["name"] in cities else pl["name"] for pl in out]
    return "Places: " + ", ".join(f'<a href="{pl["page"]}.html">{esc(n)}</a>' for pl, n in zip(out, names)) + "."


def into_note(note_html, places_html):
    """The "Places:" sentence set into a citation block's last line (its HTML): just before "Names:", else at its
    end."""
    if not places_html:
        return note_html
    at = note_html.rfind("Names: ")
    if at >= 0:
        return note_html[:at] + places_html + " " + note_html[at:]
    return note_html + (" " if note_html else "") + places_html


# ---------------------------------------------------------------- the place tags held to the entry (STYLE 8, 9)

TAG_RULES = {"polity": "polity-tag", "state": "state-tag", "city": "city-tag"}     # check's warnings, ok:<rule>
# The words a line writes for a nation, beyond its register name, key and code (STYLE 8): its adjective where the
# name does not give it, its capital and the names the calendar's sources use. A support for a tag, never a tag.
NATION_WORDS = {
    "us": ["American", "U.S.", "USA", "United States", "Washington"],
    "ussr": ["Soviet", "Russian", "Russia", "Moscow", "Kremlin"],
    "prc": ["Chinese", "Peking", "Beijing", "Sino"],
    "uk": ["Britain", "British", "English", "England", "London", "Scottish"],
    "frg": ["West German", "German", "Bonn", "Federal Republic"], "gdr": ["East German", "German", "DDR", "Pankow"],
    "fr": ["French", "Paris"],
    "drv": ["North Vietnam", "Hanoi", "Vietnam", "Vietnamese"], "rvn": ["South Vietnam", "Saigon", "Vietnam", "Vietnamese"],
    "nlf": ["Front", "Viet Cong", "Liberation"], "pathet-lao": ["Neo Lao"],
    "roc": ["Taiwan", "Formosa", "Nationalist", "Kuomintang", "Chiang", "Taipei", "GRC"],
    "rok": ["South Korea", "Korea", "Korean", "Seoul"], "dprk": ["Korea", "Korean", "Pyongyang"],
    "uar": ["Egypt", "Egyptian", "Cairo", "Nasser", "Syria", "Syrian"],
    "laos": ["Lao", "Laotian", "Vientiane"], "cambodia": ["Khmer", "Sihanouk", "Phnom Penh"], "thailand": ["Thai"],
    "cuba": ["Castro", "Havana"], "indonesia": ["Sukarno", "Djakarta", "Jakarta"], "japan": ["Tokyo"], "india": ["Delhi"],
    "netherlands": ["Dutch", "Holland", "Hague"], "switzerland": ["Swiss", "Geneva", "Bern"],
    "philippines": ["Filipino", "Philippine", "Manila"], "el-salvador": ["Salvadoran"], "norway": ["Norwegian"],
    "denmark": ["Danish", "Dane"], "finland": ["Finnish", "Finn"], "poland": ["Polish", "Pole", "Warsaw"],
    "ireland": ["Irish"], "greece": ["Greek"], "turkey": ["Turkish", "Turk"], "cyprus": ["Cypriot"],
    "sweden": ["Swedish", "Swede"], "portugal": ["Portuguese"], "iceland": ["Icelandic"],
    "vatican": ["Pope", "Holy See", "Paul VI", "John XXIII"], "saudi-arabia": ["Saudi"],
    "yugoslavia": ["Yugoslav", "Tito", "Belgrade"], "czechoslovakia": ["Czechoslovak", "Czech", "Slovak", "Prague"],
    "afghanistan": ["Afghan"], "congo": ["Congolese", "Leopoldville", "Léopoldville", "Kinshasa"],
    "congo-brazzaville": ["Brazzaville"], "ivory-coast": ["Ivorian"], "upper-volta": ["Voltaic"],
    "western-samoa": ["Samoan"], "south-yemen": ["Aden", "Southern Yemen"], "dominican-republic": ["Dominican"],
    "central-african-republic": ["Central African"], "malaysia": ["Malaya", "Malayan"], "tanzania": ["Tanganyika", "Zanzibar"],
}
SUFFIX = r"(?:|e|n|an|ian|nian|ean|ese|lese|i|ish|ic|s|ns|ans|ians)(?:'s|’s)?"   # Cuban, Ghanaian, Nepalese, Iraqi
STATE_WORDS = {"CA": ["Calif."], "KS": ["Kans."], "NE": ["Nebr."], "OR": ["Ore.", "Oreg."], "NM": ["N.Mex.", "N. Mex."],
               "ND": ["N.Dak."], "SD": ["S.Dak."], "WV": ["W.Va."], "TX": ["Texan"]}   # beside the Bluebook's
_WORD = r"(?<![^\W\d_])(?:{})(?![^\W\d_])"


def _alts(forms):
    """A pattern's alternatives, the longest first: a form of capitals or with a stop as written ("UK", "U.S."),
    any other in any case, with a suffix."""
    out = []
    for f in forms:
        if f.isupper() or "." in f:
            out.append(re.escape(f))
        else:
            out.append(f"(?i:{re.escape(f)}{SUFFIX})")
    return "|".join(sorted(set(out), key=len, reverse=True))


def nation_words(pid):
    """The pattern of the words a line writes for a polity (STYLE 8): its register name, its name without its gloss,
    its key's words and its code (of five letters or fewer), each with an adjective's suffix and, past four letters,
    without its last vowel (Bulgaria, Bulgarian); and NATION_WORDS."""
    from . import vis
    reg = vis.polities()["polities"]
    key = ("words", pid, id(reg))
    if key not in _C:
        v = reg.get(pid) or {}
        forms = set(NATION_WORDS.get(pid, []))
        name = str(v.get("name") or pid)
        for f in {name, short_name(name), re.sub(r"\s*\(.*\)", "", name), pid.replace("-", " ")}:
            f = f.strip()
            if len(f) < 3:
                continue
            forms.add(f.lower())
            if f[-1] in "aeiouy" and len(f) >= 5:
                forms.add(f[:-1].lower())
        if v.get("tag") and len(str(v["tag"])) <= 5:
            forms.add(str(v["tag"]).upper())
        _C[key] = re.compile(_WORD.format(_alts(forms)))
    return _C[key]


def state_words(code):
    """The pattern of the words a line writes for a State (STYLE 8): its name, its Bluebook abbreviation (congress.py)
    and STATE_WORDS."""
    from . import congress
    key = ("state-words", code)
    if key not in _C:
        forms = [congress.STATE.get(code, code).lower(), congress.BLUEBOOK.get(code, code)] + STATE_WORDS.get(code, [])
        _C[key] = re.compile(_WORD.format(_alts(forms)))
    return _C[key]


def tag_name(tag):
    """What a place tag names (STYLE 9): a polity's name in the register, a State's name (its postal code), a city's or
    place's in the gazetteer, a province's on the map of China or of Indochina; None for a tag that names nothing."""
    from . import congress, vis, vnmap
    ns, _, k = str(tag).partition(":")
    if ns == "polity":
        v = vis.polities()["polities"].get(k)
        return str(v.get("name") or k) + (" (an organization)" if v.get("org") else "") if isinstance(v, dict) else None
    if ns == "state":
        c = k.upper()
        return ("District of Columbia" if c == "DC" else congress.STATE.get(c)) if k == k.lower() else None
    if ns in ("city", "place"):
        r = tag_row(tag)
        if r is not None:
            from . import places
            return places.name_on(r, None)
        if ns == "place":
            p = vnmap.gazetteer().get(k)
            return vnmap.shown(p) if p else None
        return None
    if ns == "province":
        if k in provinces():
            return provinces()[k]
        u = vnmap.units().get(k)
        return u.get("name") if u else None
    return None


def tag_errors(e):
    """[message] for an entry's place tags that name nothing (STYLE 8): a `state:` tag not a postal code of the
    States or D.C. (tools/bib/sources.py, STATES), in lower case; a `polity:` tag not in sources/polities.yaml (where
    the tree has the register)."""
    import difflib
    from . import sources, vis
    out = []
    reg = vis.polities()["polities"]
    st_keys = None
    for g in store.as_list(e.get("tags")):
        ns, _, k = str(g).partition(":")
        if ns == "state":
            if k.upper() in sources.STATES and k == k.lower():
                continue
            if st_keys is None:
                st_keys = {str(r["key"]): c for c, r in states().items()}
                from . import congress
                st_keys.update({store.fold(n).lower().replace(" ", "-"): c for c, n in congress.STATE.items()})
            fix = k.lower() if k.upper() in sources.STATES else (st_keys.get(k.lower()) or "").lower()
            out.append(f"{g}: not a State's postal code in lower case (state:al; state:dc for D.C.)"
                       + (f"; write state:{fix}" if fix else ""))
        elif ns == "polity" and reg and k not in reg:
            by_tag = {str((v or {}).get("tag") or "").lower(): p for p, v in reg.items()}
            near = by_tag.get(k.lower()) or next(iter(difflib.get_close_matches(k, list(reg), n=1, cutoff=0.75)), None)
            out.append(f"{g}: no such polity in sources/polities.yaml"
                       + (f" (polity:{near}, {tag_name('polity:' + near)}?)" if near else "; add its row there first"))
    return out


def _nations_of_row(r):
    return set(_row_polities(r)) | {str(p) for p in store.as_list(r.get("in")) if p and p != "?"}


def support(lst, e, named=True):
    """What an entry's place, people, threads, other tags and line give it (STYLE 8): {"nations": polities (folded
    both ways: the NLF's are North and South Vietnam's), "states": postal codes in lower case, from its place, its
    threads (a thread whose name is a State's, or a subthread of one) and its city and place tags, "named": the
    gazetteer keys its line names, "named_states": their States}. named=False leaves out the places its line names
    (fields.place_hits, the dearest part: tag_findings asks for it only where the rest does not do)."""
    from . import fields, places, vis
    tags = [str(g) for g in store.as_list(e.get("tags"))]
    date = vis.iso(e.get("date")) or "1960-01-01"
    nations, sts = set(), set()
    for r in [places.get(k) for k in places.keys(e)]:
        if r is not None:
            nations |= _nations_of_row(r)
            if r.get("st"):
                sts.add(str(r["st"]).lower())
    for g in tags:
        ns, _, k = g.partition(":")
        if ns == "name":
            p = vis.person_polity(k, date)
            if p:
                nations.add(p)
        elif ns in ("city", "place"):
            r = tag_row(g)
            if r is not None:
                nations |= _nations_of_row(r)
                if r.get("st"):
                    sts.add(str(r["st"]).lower())
            else:
                nations |= set(vis.place_polities(g))
        elif ns == "state":
            nations.add("us")
        elif ns == "province":
            nations |= {"prc"} if k in provinces() else set(vis.place_polities(g))
        elif ns == "vis":
            m = vis.RULE_RX.match(g)
            if m:
                nations |= set(m.group(2).split("+"))
    for slug in [e.get("thread")] + store.as_list(e.get("also")):
        if not slug:
            continue
        nations |= set(vis.thread_polities(lst, slug))
        sts |= {c for s in (lst.thread_line(slug) if lst is not None else [slug]) for c in [_state_thread(s)] if c}
    named = [places.get(k) for _, _, k in fields.place_hits(e)] if named else []
    named = [r for r in named if r is not None]
    for r in named:
        nations |= _nations_of_row(r)
    nations |= {q for p in list(nations) for q in _fold(p)}
    return {"nations": nations, "states": sts, "named": {r["key"] for r in named},
            "named_states": {str(r["st"]).lower() for r in named if r.get("st")}}


def _state_thread(slug):
    """The postal code (lower case) of the State a thread's slug names (alabama, south-carolina), or None."""
    if "state-slugs" not in _C:
        from . import congress
        m = {str(r["key"]): c.lower() for c, r in states().items()}
        m.update({store.fold(n).lower().replace(" ", "-"): c.lower() for c, n in congress.STATE.items()})
        _C["state-slugs"] = m
    return _C["state-slugs"].get(str(slug))


def _line(e):
    from .markup import plain
    return " ".join(plain(str(x)) for x in [e.get("c")] + store.as_list(e.get("c2")) + store.as_list(e.get("c3")) if x)


def _placed(r):
    """Where a row is, for a message: "in Alabama" for a State, else "at Atlanta, in Georgia"."""
    from . import places
    if r.get("kind") == "state":
        return f"in {places.name_on(r, None)}"
    return f"at {places.name_on(r, None)}, in {_where_words(r)}"


def _where_words(r):
    if r.get("st"):
        c = str(r["st"]).upper()
        return "the District of Columbia" if c == "DC" else (tag_name(f"state:{c.lower()}") or c)
    ns = [n for n in _nations_of_row(r)]
    return in_words({"name": short_name(tag_name(f"polity:{ns[0]}") or ns[0]), "kind": "nation"}) if ns else "no State"


def tag_findings(lst, e):
    """[(rule, message)]: an entry's place tags that nothing else in it supports (STYLE 8): a `polity:` tag (no
    organization's) none of whose nations its place, its people, its threads, its other tags or its line give; a
    `state:` tag on an entry placed outside that State, which no thread, city tag or word of its line ties to it; a
    `city:` tag on an entry placed only in other cities of another State or nation, whose line does not name it."""
    from . import places, vis
    tags = [str(g) for g in store.as_list(e.get("tags"))]
    if not any(g.partition(":")[0] in TAG_RULES for g in tags):
        return []
    with vis.held():
        return _tag_findings(lst, e, tags, vis.polities()["polities"], places)


def _supported(ns, k, sup, text, rows):
    if ns == "polity":
        return bool(set(_fold(k)) & sup["nations"]) or k in sup["nations"] or bool(nation_words(k).search(text))
    if ns == "state":
        return k in sup["states"] or k in sup["named_states"] or k.upper() not in _state_codes() or \
            bool(state_words(k.upper()).search(text))
    r = tag_row(f"{ns}:{k}")
    if r is None or r["key"] in sup["named"] or any(x["key"] == r["key"] for x in rows):
        return True
    cst = str(r.get("st") or "").lower()
    return any((str(x.get("st") or "").lower() == cst) if cst else bool(_nations_of_row(x) & _nations_of_row(r))
               for x in rows)


def _tag_findings(lst, e, tags, reg, places):
    rows = [r for r in (places.get(k) for k in places.keys(e)) if r is not None]
    sup, text, out = None, None, []
    for g in tags:
        ns, _, k = g.partition(":")
        if ns not in TAG_RULES or f"ok:{TAG_RULES[ns]}" in tags:
            continue
        if ns == "polity" and (k not in reg or (reg.get(k) or {}).get("org")):
            continue                              # an unknown polity is an error (tag_errors); an organization no nation
        if ns != "polity" and not rows:
            continue                              # an entry the record does not place: nothing to set against the tag
        if sup is None:
            sup, text = support(lst, e, named=False), _line(e)
        if _supported(ns, k, sup, text, rows):
            continue
        if not sup.get("full"):                   # the places the line names, only now (support's dearest part)
            sup = dict(support(lst, e), full=True)
            if _supported(ns, k, sup, text, rows):
                continue
        name = tag_name(g)
        if ns == "polity":
            out.append(("polity-tag", f"{g} ({name}): nothing in the entry gives it (its place, its people's nations, "
                        "its threads, its other tags, a nation its line names): the code meant? (tag ok:polity-tag if "
                        "it is right)"))
        elif ns == "state":
            where = "; ".join(_placed(r) for r in rows)
            out.append(("state-tag", f"{g} ({name}): the entry is placed {where}, and no thread, city tag or word "
                        f"of its line ties it to {name} (tag ok:state-tag if it is right)"))
        else:
            r = tag_row(g)
            where = "; ".join(_placed(x) for x in rows)
            out.append(("city-tag", f"{g} ({name}, in {_where_words(r)}): the entry is placed {where}, and its line "
                        f"does not name {name} (tag ok:city-tag if it is right)"))
    return out


def _state_codes():
    from . import sources
    return sources.STATES
