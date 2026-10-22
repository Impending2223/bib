"""Maps of Vietnam, Laos and Cambodia in the calendar: one a year, 1960–68, at the year's first entry tagged with a
place in the Republic of Vietnam, showing every entry of the year that is tagged with a place; and the same map, every
year, on a page of its own (build/indochina.html; STYLE 6).

The data (each directory's README): sources/vn-provinces-1966/ (the provinces of late 1966, the gazetteer places.json),
sources/indochina/ (the one border geometry admin.geojson and the layers, made once by tools/vnmap/). Calendar entries
carry hidden tags: `place:<id>` (a gazetteer place) and `province:<id>` (a 1966 unit); `check` fails on one that names
nothing, and on a map file missing or too large (`problems`).

The map is drawn by MapLibre GL JS (vendored in sources/vendor/, BSD-3-Clause), the tiled layers read through the
PMTiles protocol (sources/vendor/pmtiles-*, BSD-3-Clause). This module writes the figure (its controls and legend in
HTML), copies the library, the client (tools/bib/vnmap.js and vnmap.css) and the data beside the pages, and writes the
manifest the client reads. No geometry is computed here: the build needs no shapely, and no projection is made in
Python or in the page; the library's Web Mercator draws the GeoJSON's longitudes and latitudes.

STYLE
 1. The map: the RVN's provinces of late 1966 in their corps zone's tint (Corps zones, the default: the records' own
    division), or today's region's (Regions), or plain (Provinces); province lines thin, zone or region lines heavier;
    the international borders and the demarcation line of 1954 (dashed) in ink; the countries in the land colour,
    named in italics. Borders: the countries and their borders only, no tint, no province. Land and water: no border
    at all. Every line from one geometry (tools/vnmap/base.py): a line is drawn once, at its highest rank, and the
    tints meet the borders exactly. North up; no rotation.
 2. The year's places: a dot each, in the accent, larger by the number of the year's entries there (by area, constant
    on screen); the gazetteer's other places small and muted. A tap on a dot lists its entries (date, thread, the first
    words of the statement), each linked to the entry; a tap elsewhere names the unit under it (and the month's rain,
    where shown). Under the map, folded, the year's placed entries in date order.
 3. Names: the year's places first, most entries first, then the gazetteer's by rank (1, the capitals and the largest
    cities; 2, province capitals, the main bases and battlefields, from about twice the first view; 3, the rest, from
    six times), placed by the library's collision (right, left, above, below the dot; never over another); a constant
    size on screen. Names (a box): the units' names, the corps zones' or regions', and the rivers' along their course.
 4. Zoom: the library's gestures: a drag (two fingers on a touch screen), a pinch, a double tap, the buttons; the
    wheel only with Ctrl or ⌘ (the page scrolls under it otherwise: `cooperativeGestures`); full screen. To 64 times
    the first view. North Vietnam, Laos, Cambodia (a box): their provinces (today's, the legend says so) beside the
    RVN's, and North Vietnam's regions under Regions.
 5. Nothing heavy in the pages: the client (one module, build/vnmap/vnmap-<hash>.js, its CSS beside it) loads the
    library only when a map comes within 600 px of the screen; the manifest (build/geo/vn-<hash>.json: the files, the
    legends, the places) and the borders then; each layer's file the first time the layer is shown. Rasters are tiles
    in one PMTiles file each, read by range requests (GitHub Pages answers them; locally, a server that does:
    `npx http-server build`, not `python3 -m http.server`). At most four maps drawn at once on a page; the farthest is
    given up and drawn again when it nears.
 6. The map on a page of its own, build/indochina.html (the owner's request, Oct. 22, 2026; the page around it is
    tools/bib/indochina.py): the same figure, styles and script (`full_figure`, class `full`), with every placed
    entry, each carrying its year, and a year selector above the controls (All years, the default, then 1960–68 and
    any other year with a placed entry), each year a link anchored `y<YYYY>` (`yall`), so `indochina.html#y1965`
    opens on 1965; a choice rewrites the address, no scroll. The selected year's entries make the dots, the tap's
    list, the folded list and the caption's count; in All years each date carries its year; lakes drawn from their
    dam's year to the year chosen (1968 for All years). The first view the layers' frame (lon 100–110.5, lat
    8–23.5), the box in its proportion, as tall as the screen allows; a tap's list links the place's gazetteer row
    (`#pl-<id>`). Each annual map in the calendar closes with a muted line to the page, at its year.
 7. Layers (boxes), each with its legend part and credit, drawn only when chosen: Relief (the library's hillshade of
    the elevation tiles), Elevation (the library's colour relief of the same tiles, the sea's depth bands under the
    land), Contours, Rivers (and lakes: a reservoir from its dam's year), Climate (Köppen–Geiger, 1961–1990), Rain
    (by month, 1961–1990), Population (persons a km², 1960 or 1970: modelled, made later; the legend says so) and
    Cities (the populations the UN Demographic Yearbook printed, 1960–68, each cited by page). The thematic layers
    mute the tints. The credits under the map name every source shown; the page's Sources gives them in full.
"""
import hashlib
import json
import os
import re
import shutil

from . import contents, store

SRC = os.path.join(store.ROOT, "sources", "vn-provinces-1966")
LAYERS = os.path.join(store.ROOT, "sources", "indochina")
VENDOR = os.path.join(store.ROOT, "sources", "vendor")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(store.ROOT, "build")
MAPLIBRE = "maplibre-gl-6.13.0"          # sources/vendor/<dir>: the pinned versions (sources/vendor/README.md)
PMTILES = "pmtiles-4.5.0"
FONT = "libre-franklin-5.3.0"
BOUNDS = [98.0, 6.0, 112.5, 25.5]       # the map's bounds: inside tools/vnmap/base.py's FRAME
HOME_ALL = [100.0, 8.0, 110.5, 23.5]    # the page's first view: the layers' old frame
HOME_RVN = [102.1, 8.4, 109.5, 17.2]    # an annual map's: the RVN, widened to the year's places
MAX_FILE = 50 * 2 ** 20                 # check: a map file over this is an error (git takes 100 MB)
MAX_ALL = 60 * 2 ** 20                  # check: the map's files together
_C = {}

# names the series writes in English (CLAUDE.md: English names stay), for the gazetteer's Vietnamese ones
ENGLISH = {"Sài Gòn": "Saigon", "Thung lũng Ia Drang": "Ia Drang valley", "Đồi 875": "Hill 875",
           "Tam giác Sắt": "Iron Triangle", "Chiến khu C": "War Zone C", "Căn cứ Không quân Biên Hòa": "Biên Hòa Air Base",
           "Khu phi quân sự (DMZ)": "DMZ", "Thung lũng A Sầu": "A Shau valley", "Địa đạo Củ Chi": "Củ Chi tunnels",
           "Hải Vân Pass": "Hải Vân pass", "Bến Hải": "Bến Hải river", "Hà Nội": "Hanoi", "Hải Phòng": "Haiphong"}

# the data files the client may draw: key -> file in sources/indochina/ (a missing optional file drops its layer)
FILES = {"admin": "admin.geojson", "rivers": "rivers.geojson", "lakes": "lakes.geojson", "contours": "contours.geojson",
         "bathy": "bathymetry.geojson", "climate": "climate.geojson", "pop": "population.geojson",
         "dem": "dem.pmtiles", "koppen": "koppen.pmtiles"}

CREDIT = {
    "admin": 'Borders: <a href="https://www.geoboundaries.org">geoBoundaries</a> CGAZ (CC BY 4.0); the 1966 provinces '
             'rebuilt from its districts',
    "dem": "Relief: NOAA NCEI, ETOPO 2022",
    "bathy": "Depths: NOAA NCEI, ETOPO 2022",
    "contours": "Contours: NOAA NCEI, ETOPO 2022",
    "rivers": "Rivers: HydroSHEDS v1 © World Wildlife Fund, Inc. (2006–2022), used under license; SWORD v17c (CC BY 4.0)",
    "lakes": "Lakes: HydroLAKES v1.0, GRanD (CC BY 4.0)",
    "koppen": "Climate: Beck et al. 2023 (CC BY 4.0)",
    "climate": "Rain: CRU CL 2.0, Climatic Research Unit, University of East Anglia (ODbL)",
    "pop": "Population: ISIMIP3a, from HYDE 3.2.1 (modelled)",
}

# the legends' scales (colours: ColorBrewer's Blues and YlOrBr, Apache 2.0)
RAIN = [0, 25, 50, 100, 200, 300, 400, 500]
RAIN_C = ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#084594"]
POP = [0, 1, 10, 25, 50, 100, 250, 500, 1000]          # tools/vnmap/population.py CLASSES
POP_C = ["#ffffe5", "#fff7bc", "#fee391", "#fec44f", "#fe9929", "#ec7014", "#cc4c02", "#993404", "#662506"]
ZONES = {"I": "I Corps", "II": "II Corps", "III": "III Corps", "IV": "IV Corps", "CMD": "Capital Military District"}
REGIONS = ["Northwest", "Northeast", "Red River Delta", "North Central Coast", "South Central Coast", "Central Highlands",
           "Southeast", "Mekong Delta"]
RVAR = {"North Central Coast": 1, "South Central Coast": 2, "Central Highlands": 3, "Southeast": 4, "Mekong Delta": 5,
        "Northwest": 6, "Northeast": 7, "Red River Delta": 8}


def _gj(name):
    p = os.path.join(SRC, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {"features": []}


def gazetteer():
    if "pl" not in _C:
        p = os.path.join(SRC, "places.json")
        _C["pl"] = {x["id"]: x for x in (json.load(open(p, encoding="utf-8")) if os.path.exists(p) else [])}
    return _C["pl"]


def units():
    if "u" not in _C:
        _C["u"] = {f["properties"]["id"]: f["properties"] for f in _gj("provinces1966.geojson")["features"]}
    return _C["u"]


def shown(p):
    return ENGLISH.get(p["name"], p["name"])


def in_rvn(p):
    return bool(p.get("province")) or p.get("country") == "vn-south"


def _hash(b):
    return hashlib.sha1(b).hexdigest()[:10]


def _put(rel, data):
    """Write build/<rel> unless it is there already (names carry their hash or version)."""
    path = os.path.join(OUT, rel)
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        open(tmp, "wb").write(data)
        os.replace(tmp, path)
    return rel


def _copy_hashed(src, stem):
    """A data file copied beside the pages as geo/vn-<stem>-<hash><ext>: its path from a page."""
    data = open(src, "rb").read()
    ext = os.path.splitext(src)[1]
    return _put(f"geo/vn-{stem}-{_hash(data)}{ext}", data)


def _vendor(d):
    """A vendored directory copied whole to build/vnmap/<d>/ (its name carries its version)."""
    for f in sorted(os.listdir(os.path.join(VENDOR, d))):
        if not f.startswith(".") and f != "README.md":
            _put(f"vnmap/{d}/{f}", open(os.path.join(VENDOR, d, f), "rb").read())
    return f"vnmap/{d}"


def _fonts():
    """The style's font faces (MapLibre `font-faces`): Libre Franklin, the pages' sans, vendored (OFL), the latin,
    latin-ext and vietnamese subsets with their unicode ranges (@fontsource's unicode.json)."""
    rng = {"latin": "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,"
                    "U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD",
           "latin-ext": "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,"
                        "U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF",
           "vietnamese": "U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,"
                         "U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB"}
    d = _vendor(FONT)
    faces = {}
    for name, w in (("Libre Franklin Regular", "400-normal"), ("Libre Franklin SemiBold", "600-normal"),
                    ("Libre Franklin Italic", "400-italic")):
        faces[name] = [{"url": f"{d}/libre-franklin-{s}-{w}.woff2", "unicode-range": r.split(",")} for s, r in rng.items()]
    return faces


def _places():
    feats = []
    for k, p in gazetteer().items():
        if p.get("lat") is None:
            continue
        feats.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [p["lon"], p["lat"]]},
                      "properties": {"id": k, "name": shown(p), "r": p.get("rank", 3), "kind": p.get("kind"),
                                     "c": p.get("country")}})
    return {"type": "FeatureCollection", "features": feats}


def _cities():
    """sources/indochina/cities.yaml as points, each with its rows as the tap shows them, cited by page."""
    import yaml
    p = os.path.join(LAYERS, "cities.yaml")
    if not os.path.exists(p):
        return {"type": "FeatureCollection", "features": []}
    d = yaml.safe_load(open(p, encoding="utf-8"))
    G, feats = gazetteer(), []
    for c in d["cities"]:
        g = G.get(c["place"])
        if not g or g.get("lat") is None:
            continue
        rows = []
        for r in c["rows"]:
            src = d["sources"][r["src"]].replace("*", "")
            when = _date(str(r["date"]))
            kind = "census" if r["kind"] == "C" else "estimate"
            rows.append({"text": f'{r["pop"]:,} ({r["of"]}), {kind} of {when}: {src}, p. {r["page"]}.'
                                 + (f' {r["note"]}' if r.get("note") else "")})
        first = c["rows"][0]
        feats.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [g["lon"], g["lat"]]},
                      "properties": {"id": c["place"], "name": shown(g), "pop": first["pop"],
                                     "label": f'{shown(g)} {first["pop"]:,}', "rows": json.dumps(rows, ensure_ascii=False)}})
    return {"type": "FeatureCollection", "features": feats}


MONTH = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]


def _date(s):
    m = re.fullmatch(r"(\d{4})(?:-(\d\d))?(?:-(\d\d))?", s)
    if not m:
        return s
    y, mo, d = m.groups()
    if d:
        return f"{MONTH[int(mo) - 1]} {int(d)}, {y}"
    if mo:
        return f"{MONTH[int(mo) - 1]} {y}"
    return y


def _legends():
    out = {}
    hp = os.path.join(LAYERS, "hypso.json")
    if os.path.exists(hp):
        h = json.load(open(hp, encoding="utf-8"))["classes"]
        out["hypso"] = [{"from": c["from_m"], "color": c["color"], "label": c["label"]} for c in h if c["kind"] == "land"]
        out["depths"] = [{"from": c["depth_from_m"], "color": c["color"], "label": c["label"]} for c in h
                         if c["kind"] == "sea" and c["depth_from_m"] > 0]
        out["shallow"] = next((c["color"] for c in h if c["kind"] == "sea" and c["depth_from_m"] == 0), None)
    kp = os.path.join(LAYERS, "koppen.json")
    if os.path.exists(kp):
        out["koppen"] = [c for c in json.load(open(kp, encoding="utf-8"))["classes"] if c.get("share_of_land_in_frame", 1) >= 0.001]
    out["rain"] = [{"from": v, "color": c} for v, c in zip(RAIN, RAIN_C)]
    out["pop"] = {"years": [1960, 1970], "classes": [{"from": v, "color": c} for v, c in zip(POP, POP_C)]}
    return out


def assets():
    """The client, the library and the data beside the pages: (css, js, manifest) paths from a page."""
    if "assets" in _C:
        return _C["assets"]
    lib = {"maplibre": f"{MAPLIBRE}/maplibre-gl.mjs", "css": f"{MAPLIBRE}/maplibre-gl.css", "pmtiles": f"{PMTILES}/pmtiles.js"}
    _vendor(MAPLIBRE)
    _vendor(PMTILES)
    css = open(os.path.join(HERE, "vnmap.css"), "rb").read()
    js = open(os.path.join(HERE, "vnmap.js"), encoding="utf-8").read().replace("/*LIB*/{}", json.dumps(lib), 1).encode()
    css_p = _put(f"vnmap/vnmap-{_hash(css)}.css", css)
    js_p = _put(f"vnmap/vnmap-{_hash(js)}.js", js)
    files = {}
    for k, f in FILES.items():
        p = os.path.join(LAYERS, f)
        if os.path.exists(p):
            files[k] = _copy_hashed(p, os.path.splitext(f)[0])
    files["cities"] = _put_json("cities", _cities())
    # the manifest's paths are from a page in build/; the font faces' from the page too
    M = {"bounds": BOUNDS, "home": {"all": HOME_ALL, "rvn": HOME_RVN}, "files": files, "fonts": _fonts(),
         "places": _places(), "credit": {**{k: CREDIT[k] for k in CREDIT}, "page": '<a href="indochina.html#sources">Sources and licenses</a>'},
         **_legends()}
    man = _put_json("manifest", M)
    _C["assets"] = (css_p, js_p, man)
    return _C["assets"]


def _put_json(stem, d):
    data = json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode()
    return _put(f"geo/vn-{stem}-{_hash(data)}.json", data)


def head_tags():
    css, js, _ = assets()
    return f'<link rel="stylesheet" href="{css}">', f'<script type="module" src="{js}"></script>'


def placed(e):
    tags = e.get("tags") or []
    return ([t.split(":", 1)[1] for t in tags if t.startswith("place:")],
            [t.split(":", 1)[1] for t in tags if t.startswith("province:")])


def by_year(series):
    """{year: [(entry, places, provinces)]}, the calendar's entries tagged with a place, in date order."""
    lst = series.lists.get("cal")
    out = {}
    if not lst:
        return out
    for sec, e in lst.entries():
        if "when" not in e:
            continue
        pl, pv = placed(e)
        if pl or pv:
            out.setdefault(str(e["date"])[:4], []).append((e, pl, pv))
    for y in out:
        out[y].sort(key=lambda t: str(t[0]["date"]))
    return out


def anchors(series):
    """{year: entry id}: the map goes with the year's first entry placed in the RVN (1960–68)."""
    G, out = gazetteer(), {}
    for y, rows in by_year(series).items():
        if not "1960" <= y <= "1968":
            continue
        for e, pl, pv in rows:
            if pv or any(in_rvn(G.get(p, {})) for p in pl):
                out[y] = e["id"]
                break
    return out


def _summary(c):
    from .markup import plain
    t = plain(" ".join(store.as_list(c)))
    t = re.sub(r"\s+", " ", t).strip()
    first = re.split(r"(?<=[.;])\s", t, maxsplit=1)[0]
    return first if len(first) <= 150 else first[:147].rsplit(" ", 1)[0] + " …"


def _ents(series, rows, with_year=False):
    """The entries a map shows, for its data: link (on the calendar page the entry is in), when, thread, the first
    words of the statement, places, provinces; and the year, on the page of its own."""
    from . import calsplit
    from .build import thread_name
    lst = series.lists["cal"]
    out = []
    for e, pl, pv in rows:
        half = calsplit.half_of_date(lst, e["date"]) if calsplit.cfg(lst) else None
        x = {"h": calsplit.href(lst, half or 1, e["id"]), "w": e["when"], "t": thread_name(lst, e["thread"]),
             "s": _summary(e.get("c")), "p": [p for p in pl if p in gazetteer()], "v": pv}
        if with_year:
            x["y"] = str(e["date"])[:4]
        out.append(x)
    return out


def _data(d, ents):
    """The figure's own data: the entries, and the names of their places (for the folded list before the map)."""
    d["e"] = ents
    d["pn"] = {p: shown(gazetteer()[p]) for x in ents for p in x["p"]}
    return json.dumps(d, ensure_ascii=False).replace("</", "<\\/")


def _sw(color, text, cls=""):
    return f'<s><i class="{cls}" style="background:{color}"></i>{text}</s>'


def _key():
    """The legend, every part written here and shown by the client with what it explains (data-show)."""
    L = _legends()
    parts = []

    def part(show, html):
        parts.append(f'<span data-show="{show}">{html}</span>')
    part("mode:ctz", "".join(_sw(f"var(--vz{i + 1})", n) for i, n in enumerate(ZONES.values())))
    part("mode:reg", "".join(_sw(f"var(--vr{RVAR[r]})", r) for r in REGIONS if RVAR[r] <= 5)
         + '<s>(today\'s regions, before 2025)</s>')
    part("mode:reg+nb", "".join(_sw(f"var(--vr{RVAR[r]})", r) for r in REGIONS if RVAR[r] > 5))
    part("notland", '<s><i class="l"></i>International border</s><s><i class="d"></i>Demarcation line, 1954 (the Bến Hải)</s>')
    part("always", '<s><i class="o" style="background:var(--vdot)"></i><span class="vnm-dotlab">entries, by number</span></s>')
    part("nb", "<em>North Vietnam, Laos, Cambodia: today's provinces (geoBoundaries), not those of the 1960s; "
               "Vĩnh Linh, north of the Bến Hải, the DRV's special zone of 1954–76.</em>")
    part("lay:relief", "<em>Relief: shaded from NOAA's ETOPO 2022 (15″, about 460 m).</em>")
    if L.get("hypso"):
        part("lay:elevation", "<em>Elevation:</em>" + "".join(_sw(h["color"], h["label"]) for h in L["hypso"])
             + "".join(_sw(h["color"], h["label"]) for h in L["depths"]))
    part("lay:contours", "<em>Contours at 500 m (dashed), 1,000, 1,500 and 2,000 m.</em>")
    part("lay:rivers", "<em>Rivers and lakes, today's courses; a reservoir from its dam's year.</em>")
    if L.get("koppen"):
        part("lay:koppen", "<em>Köppen–Geiger climate, 1961–1990:</em>" + "".join(_sw(c["color"], f'{c["code"]} {c["name"]}') for c in L["koppen"]))
    part("lay:rain", '<em>Rain, <span class="vnm-month">July</span>, mean of 1961–1990, mm a month (lon. 100–110.5° E, '
                     'lat. 8–23.5° N only):</em>' + "".join(_sw(r["color"], f'{r["from"]}{"+" if i == len(RAIN) - 1 else ""}')
                                                            for i, r in enumerate(L["rain"])))
    part("lay:pop", '<em>Population, <span class="vnm-popyear">1960</span>, persons a km²: modelled, and made later '
                    '(ISIMIP3a, from HYDE 3.2.1); not a census:</em>'
         + "".join(_sw(c["color"], (f'{c["from"]:,}–{L["pop"]["classes"][i + 1]["from"]:,}' if i + 1 < len(POP) else f'{c["from"]:,} and over'))
                   for i, c in enumerate(L["pop"]["classes"])))
    part("lay:cities", '<s><i class="o" style="background:var(--vcity);opacity:.5"></i>Cities: the populations the UN '
                       '<i>Demographic Yearbook</i> printed, 1960–68 (a tap gives each figure and its page)</s>')
    return '<div class="vnm-key">' + "".join(parts) + "</div>"


def _bar(full):
    have = {k for k in FILES if os.path.exists(os.path.join(LAYERS, FILES[k]))}
    seg = ('<span class="seg" role="group" aria-label="Map">'
           + "".join(f'<button type="button" data-mode="{m}" aria-pressed="false">{t}</button>'
                     for m, t in (("ctz", "Corps zones"), ("reg", "Regions"), ("prov", "Provinces"), ("borders", "Borders"),
                                  ("land", "Land and water"))) + "</span>")
    boxes = [("names", "Names", True), ("nb", "North Vietnam, Laos, Cambodia", True), ("relief", "Relief", "dem" in have),
             ("elevation", "Elevation", "dem" in have), ("contours", "Contours", "contours" in have),
             ("rivers", "Rivers", "rivers" in have), ("koppen", "Climate", "koppen" in have),
             ("rain", "Rain", "climate" in have), ("pop", "Population", "pop" in have), ("cities", "Cities", True)]
    h = seg + "".join(f'<label><input type="checkbox" data-l="{k}"> {t}</label>' for k, t, ok in boxes if ok)
    if "climate" in have:
        h += ('<select data-m aria-label="Month of the rain">'
              + "".join(f'<option value="{i + 1}"{" selected" if i == 6 else ""}>{m}</option>' for i, m in enumerate(MONTH))
              + "</select>")
    if "pop" in have:
        h += '<select data-py aria-label="Year of the population"><option>1960</option><option>1970</option></select>'
    return f'<div class="vnm-bar">{h}</div>'


def _box(label, full):
    return (_bar(full) + f'<div class="vnm-box"><div class="vnm-gl" role="region" aria-label="{label}"></div>'
            '<div class="vnm-pop" hidden></div></div>' + _key())


def block(series, y):
    rows = by_year(series).get(y, [])
    ents = _ents(series, rows)
    n_pl = len({p for x in ents for p in x["p"]})
    _, _, man = assets()
    return (f'<figure class="vnm" data-geo="{man}" data-y="{y}">'
            f'<figcaption class="vnm-cap">Vietnam, Laos and Cambodia, {y}: the year\'s {len(ents)} placed entries, at '
            f'{n_pl} places. Provinces as of late 1966; lines approximate (sources/vn-provinces-1966).</figcaption>'
            + _box(f"Map of Vietnam, Laos and Cambodia, {y}", False) +
            '<details class="vnm-list"><summary>The year\'s placed entries</summary>'
            f'<ol></ol></details><p class="vnm-pg">Every year on one map, with the gazetteer: '
            f'<a href="indochina.html#y{y}">Indochina</a>.</p>'
            f'<script type="application/json" class="vnm-d">{_data({"y": y}, ents)}</script></figure>')


def years(series):
    """The years the page's selector offers: 1960–68, and any other year with a placed entry."""
    return sorted(set(map(str, range(1960, 1969))) | set(by_year(series)))


def full_figure(series):
    """The map on indochina.html (STYLE 6): every placed entry, a year selector, the frame of the layers."""
    import math
    by = by_year(series)
    ys = years(series)
    rows = [r for y in sorted(by) for r in by[y]]
    ents = _ents(series, rows, with_year=True)
    n_pl = len({p for x in ents for p in x["p"]})
    yrs = ('<nav class="vnm-yrs" aria-label="Year"><a id="yall" href="#yall" data-yr="all">All years</a>'
           + "".join(f'<a id="y{y}" href="#y{y}" data-yr="{y}">{y}</a>' for y in ys) + "</nav>")
    m = lambda lat: math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))   # the box's proportion only
    ar = math.radians(HOME_ALL[2] - HOME_ALL[0]) / (m(HOME_ALL[3]) - m(HOME_ALL[1]))
    _, _, man = assets()
    return (f'<figure class="vnm full" data-geo="{man}" data-y="all" style="--vnar:{ar:.4f}">'
            f'<figcaption class="vnm-cap"><span class="vnm-cnt">All years: {len(ents)} placed entries, at {n_pl} '
            'places.</span> Provinces as of late 1966; lines approximate.</figcaption>'
            + yrs + _box("Map of Vietnam, Laos and Cambodia, 1960–1968", True) +
            '<details class="vnm-list"><summary>The placed entries</summary><ol></ol></details>'
            f'<script type="application/json" class="vnm-d">{_data({"y": "all", "ys": ys}, ents)}</script></figure>')


def inject(page, series):
    used = False
    for y, eid in anchors(series).items():
        if f'<li id="{eid}"' not in page:
            continue
        blk = block(series, y)
        page, k = contents.put(page, eid, blk, "vnmap", y)
        used = used or bool(k)
    if used and 'class="vnm-css"' not in page:
        css, js = head_tags()
        page = page.replace("</head>", css.replace("<link ", '<link class="vnm-css" ') + "\n</head>", 1)
        page = page.replace("</body>", js + "\n</body>", 1)
    return page


def problems(series):
    out = []
    G, U = gazetteer(), units()
    lst = series.lists.get("cal")
    if lst:
        for sec, e in lst.entries():
            for t in e.get("tags") or []:
                if t.startswith("place:") and t[6:] not in G:
                    out.append((e["id"], f"{t}: no such place in sources/vn-provinces-1966/places.json"))
                elif t.startswith("province:") and t[9:] not in U:
                    out.append((e["id"], f"{t}: no such 1966 unit in sources/vn-provinces-1966/provinces1966.geojson"))
    # the map's files: there, under the size limits, the vendored library whole
    total = 0
    for k, f in FILES.items():
        p = os.path.join(LAYERS, f)
        if not os.path.exists(p):
            if k == "admin":
                out.append(("vnmap", f"sources/indochina/{f}: missing (tools/vnmap/base.py writes it)"))
            continue
        n = os.path.getsize(p)
        total += n
        if n > MAX_FILE:
            out.append(("vnmap", f"sources/indochina/{f}: {n:,} bytes, over {MAX_FILE:,}"))
    if total > MAX_ALL:
        out.append(("vnmap", f"sources/indochina: the map's files {total:,} bytes together, over {MAX_ALL:,}"))
    for d, fs in ((MAPLIBRE, ("maplibre-gl.mjs", "maplibre-gl-worker.mjs", "maplibre-gl.css", "LICENSE.txt")),
                  (PMTILES, ("pmtiles.js", "LICENSE")), (FONT, ("LICENSE",))):
        for f in fs:
            if not os.path.exists(os.path.join(VENDOR, d, f)):
                out.append(("vnmap", f"sources/vendor/{d}/{f}: missing"))
    import yaml
    cp = os.path.join(LAYERS, "cities.yaml")
    if os.path.exists(cp):
        c = yaml.safe_load(open(cp, encoding="utf-8"))
        for x in c.get("cities", []):
            if x["place"] not in G:
                out.append(("vnmap", f"sources/indochina/cities.yaml: {x['place']}: no such place"))
            for r in x.get("rows", []):
                if r.get("src") not in c.get("sources", {}) or not r.get("page") or not isinstance(r.get("pop"), int):
                    out.append(("vnmap", f"sources/indochina/cities.yaml: {x['place']} {r.get('date')}: needs pop, src and page"))
    return out
