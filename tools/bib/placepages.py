"""The Places pages (the owner, Nov. 26, 2026: "it's hard to follow any given national thread anywhere outside the
United States and China, and hard to follow any subnational or local thread anywhere"; ruling 66, the default taken;
notes/proposals/place-pages.md): a page for each nation, each U.S. State, each Chinese province of 1966 and each city
of CITY_MIN entries or more, built on every build from the entries' `place:`, their tags and the visibility register.
Nothing is stored: no entry is re-read or re-threaded for them.

    ./bib build places       build/places-<slug>.html, a page a place (and its parts); threads.html, whose section
                             "Places" lists them (threads.py, STYLE 7)

STYLE
 1. Which places have a page. A nation: each polity of sources/polities.yaml that is no organization (`org`) and
    stands for itself (FOLD: the National Liberation Front is the DRV's, by the register's own `folded:`; the Pathet
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
    points and units) and those tagged `province:<the unit>`.
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
FOLD = {"nlf": "drv", "pathet-lao": "laos"}      # a polity that is another's on its page (STYLE 1)
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
    return FOLD.get(p, p)


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
    return [_fold(str(p)) for p in store.as_list(row.get("in")) if p and p != "?"]


def tag_row(tag):
    """The gazetteer row a `city:` or `place:` tag names, or None."""
    from . import places
    ns, _, k = str(tag).partition(":")
    return places.get(k) if ns in ("city", "place") and k else None


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
    date = vis.iso(e.get("date")) or "1960-01-01"
    addr = vis.address(lst, e, None, date)[0]
    tagged["nation"] = {_fold(p) for p in addr if not vis.is_org(p)}
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
    acc = {}
    for _, e in lst.entries():
        if "when" not in e:
            continue
        w = where(series, lst, e)
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
    _C.update(key=key, got=got)
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
