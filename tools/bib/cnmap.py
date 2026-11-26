"""The map of China (the owner, Nov. 22, 2026: "We should probably give ourselves a China map. Like our Southeast
Asia/Indochina map. The minimum viable product would give us the provinces, counties, places."): on a page of its own,
build/china.html; in each page of the calendar that holds an entry placed on it and at the head of the pages of
`china` and every thread under it, for the page's own span of dates (the owner, Nov. 25, 2026; tools/bib/maps.py
places it there and keeps the span). Here: the figure, its data beside the pages, and `check`'s rules for its files.
The page around it is tools/bib/china.py. The map is the maps of Indochina's (tools/bib/vnmap.py): the same client (vnmap.js, vnmap.css), the
same library and font, the same figure; what differs is data, the figure's own and the manifest's `opt`.

The data (sources/china/, its README; made once by tools/cnmap/, committed): admin.geojson (the countries of East and
Central Asia, the PRC's provinces as of 1966 and the Republic of China's two, one coverage), counties.geojson (the
counties of 1964 as unions of a later boundary file's units; the Republic of China's counties and cities of the
1960s as unions of today's townships), units.json, counties.json (each county, what it was made of and on what basis),
places.json (the calendar's gazetteer's places in China, each keyed by its gazetteer key, with Wikidata's or
Wikipedia's coordinates, its 1966 province and 1964 county by point in polygon). No geometry is computed here: the
build needs no shapely.

STYLE
 1. The map: the PRC's provinces, autonomous regions and municipalities as of 1966 in one plain tint (Provinces, the
    default), their lines thin; the international borders in ink, the lines of the disputed areas dashed, as the
    demarcation line is on the maps of Indochina; the countries in the land colour, named in italics. Borders: the
    countries and their borders only. Land and water: no border at all. Hong Kong and Macau the colonies; Taiwan a
    country of the map, named as one, and drawn by the Republic of China's own units (the owner, Nov. 25, 2026: "Give
    Formosa and Free China their ROC subdivisions"): its two provinces, Taiwan and Fujian (Kinmen and Matsu), in the
    provinces' tint, and with Counties its counties and cities. North up; no rotation.
 2. The places: the calendar's own gazetteer (sources/places.yaml), every place of it that lies in China, Hong Kong,
    Macau or Taiwan and that Wikidata or Wikipedia gives coordinates for; a dot each, in the accent, larger by the
    number of the span's entries there (by area; the scale a ninth of the maps of Indochina's, `DOT`, the calendar
    having some 8,000 entries in Peking alone); the other places small and muted. A tap on a dot lists its entries, each
    linked. A province named as a place (`place: sichuan`) is no dot: its entries are listed by a tap on the province.
 3. Names: as on the maps of Indochina (the span's places first, then the gazetteer's by rank); rank 1 the capitals of
    1964 and Hong Kong and Taipei, rank 2 a place with RANK2 entries or more, rank 3 the rest. Names (a box): the
    provinces' names and, with Counties, the counties'.
 4. Counties (a box): the counties and cities of the end of 1964, each a union of a later boundary file's units, their
    lines thin and the provinces' then in ink; a tap names the county, its kind and what it rests on. A unit the
    record could not trace back to 1964 is shown as the later unit it is, and a tap says so (the owner, Nov. 25, 2026:
    "Show the later units").
 5. The page: every calendar entry whose `place:` is a place on the map; a year selector (All years, then 1960-69 and
    any other year with a placed entry), anchored as indochina.html's are, which fills the span's two fields (maps.py
    STYLE 2). The entries are thousands: they go in files of their own, one a year (build/geo/cn-entries-<year>-
    <hash>.json; maps.py STYLE 1), of which the client reads the span's years; the folded list is written when it is
    opened.
 6. Nothing here is styled anew: the figure, the controls, the legend and the list are vnmap.css's classes. Away from
    its page (a calendar page, a thread's) the figure keeps the page's proportion (.vnm.full, `--vnar`).
"""
import json
import math
import os
import sys

from . import chron, places as gaz, store, vnmap

SRC = os.path.join(store.ROOT, "sources", "china")
BOUNDS = [67.0, 11.0, 141.0, 57.0]      # the map's bounds: inside tools/cnmap/base.py's FRAME
HOME = [73.0, 17.5, 135.5, 54.0]        # the page's first view: the PRC
DOT = 0.3                               # a dot's radius, px, is DOT * sqrt(entries) (vnmap.js: 2.6 for Indochina)
RANK2 = 10
FILES = {"admin": "admin.geojson", "counties": "counties.geojson"}
CREDIT = {
    "admin": 'Borders: <a href="https://www.geoboundaries.org">geoBoundaries</a> CGAZ (CC BY 4.0); the provinces as '
             'of 1966',
    "counties": "Counties: as of 1964, from later lines (geoBoundaries, China ADM2, PDDL; "
                '<a href="http://www.xzqh.org">行政区划网</a>\'s lists)',
}
_C = {}
# what tools/bib/maps.py asks of a map's module: its names, its page, its figure away from that page
KEY, KIND, PAGE, NAME = "cn", "cnmap", "china.html", "China"
LABEL = "Map of China"
TAIL = "Provinces as of 1966, counties as of 1964; lines approximate."
BLURB = ("China, 1960–1970: the calendar's placed entries on one map, by year; the provinces of 1966, the counties of "
         "1964; the gazetteer")
SPAN = "1960–70"
_m = lambda lat: math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))      # the box's proportion only
AR = math.radians(HOME[2] - HOME[0]) / (_m(HOME[3]) - _m(HOME[1]))
FIGURE = f'class="vnm full" style="--vnar:{AR:.4f}"'
DATA = {"map": "cn", "mode": "prov"}    # the key its choices are kept under; the first kind of map
THREADS = ("china",)                    # the thread the contents list a calendar page's map under


def _json(name, default):
    p = os.path.join(SRC, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else default


def gazetteer():
    """{gazetteer key: the map's row}: sources/china/places.json."""
    if "pl" not in _C:
        _C["pl"] = {x["key"]: x for x in _json("places.json", {"places": []})["places"]}
    return _C["pl"]


def units():
    if "u" not in _C:
        _C["u"] = {u["id"]: u for u in _json("units.json", {"units": []})["units"]}
    return _C["u"]


def counties():
    if "c" not in _C:
        _C["c"] = {c["id"]: c for c in _json("counties.json", {"counties": []})["counties"]}
    return _C["c"]


def in_china(row):
    """A row of sources/places.yaml that lies in China as the map takes it: the PRC, Taiwan, Hong Kong, Macau."""
    return bool({"prc", "roc"} & set(map(str, store.as_list(row.get("in"))))) or row.get("key") in ("hong-kong", "macau")


def shown(key):
    """A place's name as the calendar writes it: the gazetteer's own (sources/places.yaml)."""
    r = gaz.get(key)
    return r["name"] if r else key


def placed(e):
    """An entry's places on the map: (the points' keys, the units named as places)."""
    G = gazetteer()
    pts, us = [], []
    for k in gaz.keys(e):
        r = gaz.get(k)
        p = G.get(r["key"] if r else k)
        if not p:
            continue
        if p.get("area"):
            us.append(p["unit"])
        elif p.get("lat") is not None:
            pts.append(p["key"])
    return pts, us


def by_year(series):
    """{year: [(entry, places, units)]}, the calendar's entries placed on the map, in the calendar's order."""
    if "by" in _C:
        return _C["by"]
    lst = series.lists.get("cal")
    out = {}
    if lst and gazetteer():
        for sec, e in lst.entries():
            if "when" not in e or "place" not in e:
                continue
            pl, us = placed(e)
            if pl or us:
                out.setdefault(str(e["date"])[:4], []).append((e, pl, us))
        for y, rows in out.items():
            at = chron.position(lst, [e for e, _, _ in rows])
            rows.sort(key=lambda t: at[t[0]["id"]])
    _C["by"] = out
    return out


def years(series):
    """The years the selector offers: 1960-69, and any other year with a placed entry."""
    from . import maps
    return sorted(set(map(str, range(1960, 1970))) | set(maps.entries(series, sys.modules[__name__])["ys"]))


def rank(p, n):
    """A place's rank for its name (STYLE 3)."""
    return 1 if p.get("capital") else 2 if n >= RANK2 else 3


def _places(counts):
    feats = []
    for k, p in gazetteer().items():
        if p.get("lat") is None or p.get("area"):
            continue
        feats.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [p["lon"], p["lat"]]},
                      "properties": {"id": k, "name": shown(k), "r": rank(p, counts.get(k, 0)), "c": p.get("c", "prc")}})
    return {"type": "FeatureCollection", "features": feats}


def _put_json(stem, d):
    data = json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode()
    return vnmap._put(f"geo/cn-{stem}-{vnmap._hash(data)}.json", data)


def manifest(series):
    """The data beside the pages: the manifest's path from a page; the client is vnmap.client(), the entries' files
    maps.entries's."""
    if "manifest" in _C:
        return _C["manifest"]
    from . import maps
    counts = {}
    for x in maps.entries(series, sys.modules[__name__])["rows"]:
        for p in x["p"]:
            counts[p] = counts.get(p, 0) + 1
    files = {}
    for k, f in FILES.items():
        p = os.path.join(SRC, f)
        if os.path.exists(p):
            data = open(p, "rb").read()
            files[k] = vnmap._put(f"geo/cn-{os.path.splitext(f)[0]}-{vnmap._hash(data)}.geojson", data)
    M = {"bounds": BOUNDS, "home": {"all": HOME}, "files": files, "fonts": vnmap._fonts(), "places": _places(counts),
         "credit": {**{k: v for k, v in CREDIT.items() if k in files},
                    "page": '<a href="china.html#sources">Sources and licenses</a>'},
         "opt": {"shown": ["prc", "roc", "hong-kong", "macau"], "dot": DOT, "unit": "as of 1966"}}
    _C["manifest"] = _put_json("manifest", M)
    return _C["manifest"]


def _key():
    """The legend (vnmap.css's .vnm-key; each part shown by the client with what it explains)."""
    parts = []

    def part(show, html):
        parts.append(f'<span data-show="{show}">{html}</span>')
    part("notland", '<s><i class="l"></i>International border</s><s><i class="d"></i>Line of a disputed area</s>')
    part("always", '<s><i class="o" style="background:var(--vdot)"></i><span class="vnm-dotlab">entries, by number</span></s>')
    part("mode:prov", "<em>Provinces, autonomous regions and municipalities as of 1966: Tianjin in Hebei, Hainan in "
                      "Guangdong, Chongqing in Sichuan; Taiwan and Kinmen and Matsu as the Republic of China's two "
                      "provinces. A tap on one lists the entries placed in it as a whole.</em>")
    part("lay:counties", "<em>Counties and cities as of the end of 1964, each drawn from the lines of a later year "
                         f"(about {_json('counties.json', {}).get('file_year', 1994)}): a city at its later size; a county made or divided since given whole to one "
                         "county of 1964; a unit not traced back to 1964 shown as the later unit it is. Taiwan's, "
                         "Kinmen's and Matsu's are the Republic of China's counties and cities of the 1960s, from "
                         "today's townships. A tap names the county and what it rests on.</em>")
    return '<div class="vnm-key">' + "".join(parts) + "</div>"


def _bar():
    seg = ('<span class="seg" role="group" aria-label="Map">'
           + "".join(f'<button type="button" data-mode="{m}" aria-pressed="false">{t}</button>'
                     for m, t in (("prov", "Provinces"), ("borders", "Borders"), ("land", "Land and water"))) + "</span>")
    boxes = [("names", "Names", True), ("counties", "Counties", os.path.exists(os.path.join(SRC, FILES["counties"])))]
    return ('<div class="vnm-bar">' + seg
            + "".join(f'<label><input type="checkbox" data-l="{k}"> {t}</label>' for k, t, ok in boxes if ok) + "</div>")


def box(label):
    """The controls, the map's box and the legend: what every figure of this map holds under its span's fields."""
    return (_bar() + f'<div class="vnm-box"><div class="vnm-gl" role="region" aria-label="{label}"></div>'
            '<div class="vnm-pop" hidden></div></div>' + _key())


def full_figure(series):
    """The map on china.html (STYLE 5): the figure of vnmap.full_figure, with this map's data."""
    from . import calsplit, maps
    E = maps.entries(series, sys.modules[__name__])
    ys = years(series)
    lo, hi = calsplit.part_range(maps.calendar(series), None)       # "All years": the calendar's whole span
    yrs = ('<nav class="vnm-yrs" aria-label="Year"><a id="yall" href="#yall" data-yr="all">All years</a>'
           + "".join(f'<a id="y{y}" href="#y{y}" data-yr="{y}">{y}</a>' for y in ys) + "</nav>")
    all_ = [lo.isoformat(), hi.isoformat()]
    d = dict(DATA, eu=E["files"], ys=ys, sp=all_, all=all_, gz="")
    return (f'<figure {FIGURE} data-geo="{manifest(series)}">'
            f'<figcaption class="vnm-cap"><span class="vnm-cnt">All years: {maps.count(E["rows"])}</span> {TAIL}'
            '</figcaption>' + yrs + maps.fields(lo, hi) + box(f"{LABEL}, {ys[0]}–{ys[-1]}") +
            f'<details class="vnm-list"><summary>The placed entries ({len(E["rows"])})</summary><ol></ol></details>'
            f'<script type="application/json" class="vnm-d">{maps.data(d)}</script></figure>')


def problems(series):
    """`check`'s errors for the map's files, as vnmap.problems's are for Indochina's: a file missing or too large; a
    row of places.json that names nothing (no such gazetteer key, unit or county) or has a point without its source."""
    out = []
    total = 0
    for k, f in FILES.items():
        p = os.path.join(SRC, f)
        if not os.path.exists(p):
            if k == "admin":
                out.append(("cnmap", f"sources/china/{f}: missing (tools/cnmap/base.py writes it)"))
            continue
        n = os.path.getsize(p)
        total += n
        if n > vnmap.MAX_FILE:
            out.append(("cnmap", f"sources/china/{f}: {n:,} bytes, over {vnmap.MAX_FILE:,}"))
    if total > vnmap.MAX_ALL:
        out.append(("cnmap", f"sources/china: the map's files {total:,} bytes together, over {vnmap.MAX_ALL:,}"))
    U, C = units(), counties()
    for k, p in gazetteer().items():
        r = gaz.get(k)
        if r is None or r.get("key") != k:
            out.append(("cnmap", f"sources/china/places.json: {k}: no such key in the gazetteer (sources/places.yaml)"))
        if p.get("unit") and U and p["unit"] not in U:
            out.append(("cnmap", f"sources/china/places.json: {k}: unit {p['unit']}: no such 1966 unit in units.json"))
        if p.get("county") and C and p["county"] not in C:
            out.append(("cnmap", f"sources/china/places.json: {k}: county {p['county']}: no such county in counties.json"))
        if p.get("area"):
            if not p.get("unit"):
                out.append(("cnmap", f"sources/china/places.json: {k}: an area needs its unit"))
        elif p.get("lat") is not None:
            if not isinstance(p.get("lat"), (int, float)) or not isinstance(p.get("lon"), (int, float)) or not p.get("src"):
                out.append(("cnmap", f"sources/china/places.json: {k}: a point needs lat, lon and src"))
            elif not (BOUNDS[0] <= p["lon"] <= BOUNDS[2] and BOUNDS[1] <= p["lat"] <= BOUNDS[3]):
                out.append(("cnmap", f"sources/china/places.json: {k}: its point lies off the map"))
        elif not p.get("unplaced"):
            out.append(("cnmap", f"sources/china/places.json: {k}: neither a point, an area nor `unplaced` with its reason"))
    return out


def warnings(series):
    """`check`'s warnings: a gazetteer place in China the map's file does not hold yet (tools/cnmap/places.py)."""
    G = gazetteer()
    if not G:
        return []
    rows, _ = gaz._load()
    return [("sources/places.yaml", f"{r['key']}: in China, not in sources/china/places.json (tools/cnmap/places.py "
             "places it)") for r in rows if in_china(r) and r["key"] not in G]
