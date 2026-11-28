"""The map of China: cnmap.py (the figure's data, check's rules), china.py (the gazetteer's rows), the shared client's
options, and tools/cnmap/counties.py (the record's reading and the walk back to 1964).

Written Nov. 26, 2026, with the map. The rows pin what the functions returned then; a row that fails is a change of
behaviour: a regression, or a fix to be read and the row rewritten with it. The map's own data (sources/china/) is not
in the fixture: the tests give the code a small gazetteer of their own.
"""
import json
import os
import re
import sys

import pytest

from bib import calsplit, china, cnmap, maps, places as gaz, store, vnmap

TOOLS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "tools")
sys.path.insert(0, os.path.join(TOOLS, "cnmap"))
import counties  # noqa: E402  (tools/cnmap/counties.py: its reading functions need no download and no shapely)

ROWS = [
    {"key": "peking", "name": "Peking", "zone": "Asia/Shanghai", "in": "prc"},
    {"key": "sichuan", "name": "Sichuan", "zone": "Asia/Shanghai", "in": "prc"},
    {"key": "niujiao", "name": "Niujiao", "zone": "Asia/Shanghai", "in": "prc"},
    {"key": "taipei", "name": "Taipei", "zone": "Asia/Taipei", "in": "roc"},
    {"key": "hong-kong", "name": "Hong Kong", "zone": "Asia/Hong_Kong", "in": "uk"},
    {"key": "saigon", "name": "Saigon", "zone": "Asia/Ho_Chi_Minh", "in": "rvn"},
    {"key": "zhenbao-island", "name": "Zhenbao Island", "zone": "Asia/Shanghai", "in": ["prc", "ussr"]},
]
MAP = {
    "peking": {"key": "peking", "zh": "北京市", "lat": 39.904, "lon": 116.4075, "src": "wikidata", "q": "Q956",
               "wiki": "https://en.wikipedia.org/wiki/Beijing", "unit": "peking", "c": "prc", "capital": True},
    "sichuan": {"key": "sichuan", "area": True, "unit": "sichuan"},
    "niujiao": {"key": "niujiao", "unplaced": "a village of Chang'an county, Shaanxi; neither source has it"},
    "taipei": {"key": "taipei", "zh": "台北市", "lat": 25.0375, "lon": 121.5625, "src": "wikidata", "q": "Q1867",
               "wiki": "https://en.wikipedia.org/wiki/Taipei", "country": "Taiwan", "c": "roc", "capital": True},
}
UNITS = {"peking": {"id": "peking", "name": "Peking", "kind": "municipality"},
         "sichuan": {"id": "sichuan", "name": "Sichuan", "kind": "province"}}


@pytest.fixture
def china_map(monkeypatch, tmp_path):
    """A small gazetteer and the map's rows for it; the build's files go to a directory of the test's own."""
    monkeypatch.setattr(gaz, "_ROWS", [dict(r) for r in ROWS])
    monkeypatch.setattr(gaz, "_INDEX", {r["key"]: r for r in ROWS})
    monkeypatch.setattr(cnmap, "_C", {"pl": {k: dict(v) for k, v in MAP.items()}, "u": dict(UNITS), "c": {}})
    monkeypatch.setattr(vnmap, "_C", {})
    monkeypatch.setattr(maps, "_C", {})
    monkeypatch.setattr(vnmap, "OUT", str(tmp_path))
    monkeypatch.setattr(vnmap, "VENDOR", str(tmp_path / "vendor"))   # the fixture holds no vendored library:
    for d in (vnmap.MAPLIBRE, vnmap.PMTILES):                         # an empty one, so that the map is ready
        os.makedirs(tmp_path / "vendor" / d)
    monkeypatch.setattr(vnmap, "_fonts", lambda: {})          # nor a vendored font
    return tmp_path


@pytest.mark.parametrize("key, want", [("peking", True), ("taipei", True), ("hong-kong", True), ("saigon", False),
                                       ("zhenbao-island", True)])
def test_in_china(key, want):
    assert cnmap.in_china(next(r for r in ROWS if r["key"] == key)) is want


@pytest.mark.parametrize("row, n, want", [({"capital": True}, 0, 1), ({}, 10, 2), ({}, 9, 3), ({}, 0, 3)])
def test_rank(row, n, want):
    assert cnmap.rank(row, n) == want


@pytest.mark.parametrize("place, want", [
    ("peking", (["peking"], [])),                       # a point
    ("sichuan", ([], ["sichuan"])),                     # a province named as a place: its unit, no dot
    ("niujiao", ([], [])),                              # not on the map
    (["peking", "sichuan"], (["peking"], ["sichuan"])),  # a list of two
    ("saigon", ([], [])),                               # not in China
])
def test_placed(china_map, place, want):
    assert cnmap.placed({"place": place}) == want


def test_problems_clean(china_map):
    assert [m for w, m in cnmap.problems(None) if "missing" not in m] == []


@pytest.mark.parametrize("row, want", [
    ({"key": "nowhere", "lat": 30.0, "lon": 110.0, "src": "wikidata"}, "nowhere: no such key in the gazetteer"),
    ({"key": "peking", "lat": 39.9, "lon": 116.4, "src": "wikidata", "unit": "atlantis"}, "peking: unit atlantis: no such 1966 unit"),
    ({"key": "peking", "lat": 39.9, "lon": 116.4}, "peking: a point needs lat, lon and src"),
    ({"key": "peking", "lat": 39.9, "lon": 16.4, "src": "wikidata"}, "peking: its point lies off the map"),
    ({"key": "peking"}, "peking: neither a point, an area nor `unplaced` with its reason"),
    ({"key": "sichuan", "area": True}, "sichuan: an area needs its unit"),
])
def test_problems(china_map, row, want):
    cnmap._C["pl"] = {row["key"]: row}
    got = [m for w, m in cnmap.problems(None)]
    assert any(want in m for m in got), got


def test_warnings(china_map):
    """A gazetteer place in China the map's file lacks is a warning, not an error: a reader's new place stops no deploy."""
    got = [m for w, m in cnmap.warnings(None)]
    assert sorted(m.split(":")[0] for m in got) == ["hong-kong", "zhenbao-island"]


def test_missing_files_on_the_fixture(monkeypatch):
    monkeypatch.setattr(cnmap, "_C", {})
    assert ("cnmap", "sources/china/admin.geojson: missing (tools/cnmap/base.py writes it)") in cnmap.problems(None)
    assert cnmap.warnings(None) == []                   # no map data: nothing to hold the gazetteer against


def _series():
    return store.Series()


def test_figure_and_data(china_map):
    """The figure is the maps of Indochina's (its classes), told apart by data; the entries are in files of their own,
    one a year; the year buttons and the span's two fields, filled with the calendar's whole span."""
    s = _series()
    lst = s.lists["cal"]
    es = [e for _, e in lst.entries() if "when" in e and "place" not in e][:3]
    try:
        for e, p in zip(es, ["sichuan", ["peking", "sichuan"], "niujiao"]):
            e["place"] = p
        fig = cnmap.full_figure(s)
    finally:
        for e in es:
            e.pop("place", None)
    for cls in ('class="vnm full"', 'class="vnm-cap"', 'class="vnm-yrs"', 'class="vnm-bar"', 'class="vnm-box"',
                'class="vnm-gl"', 'class="vnm-pop"', 'class="vnm-key"', 'class="vnm-list"', 'class="vnm-d"'):
        assert cls in fig, cls
    assert [m for m in ("prov", "borders", "land") if f'data-mode="{m}"' in fig] == ["prov", "borders", "land"]
    assert 'data-mode="ctz"' not in fig and 'data-l="names"' in fig
    d = json.loads(fig.split('class="vnm-d">', 1)[1].split("</script>", 1)[0])
    lo, hi = (x.isoformat() for x in calsplit.part_range(lst, None))
    assert set(d) == {"map", "mode", "eu", "ys", "sp", "all", "gz"}                 # no entry in the page, no names
    assert d["map"] == "cn" and d["mode"] == "prov" and d["sp"] == d["all"] == [lo, hi] and d["gz"] == ""
    assert d["ys"][0] == "1960" and "1969" in d["ys"] and list(d["eu"]) == ["1961"]
    assert re.fullmatch(r"geo/cn-entries-1961-[0-9a-f]{10}\.json", d["eu"]["1961"])
    assert fig.index('class="vnm-yrs"') < fig.index('data-sp="from"') < fig.index('data-mode="prov"')
    assert f'data-sp="from" size="13" value="{maps.day(calsplit.part_range(lst, None)[0])}"' in fig
    year = json.load(open(os.path.join(china_map, d["eu"]["1961"]), encoding="utf-8"))
    ents = year["e"]
    assert f"All years: {len(ents)} placed entries, at 1 place." in fig
    mine = {e["id"]: next((x for x in ents if x["h"].endswith("#" + e["id"])), None) for e in es}
    assert (mine[es[0]["id"]]["p"], mine[es[0]["id"]]["v"]) == ([], ["sichuan"])      # the province as a whole
    assert (mine[es[1]["id"]]["p"], mine[es[1]["id"]]["v"]) == (["peking"], ["sichuan"])
    assert mine[es[2]["id"]] is None                                                    # a place not on the map
    assert all(set(x) == {"h", "w", "d", "t", "s", "p", "v", "k"} for x in ents)
    assert all(x["p"] == ["peking"] for x in ents if x["v"] == [])                      # the fixture's own entries in Peking
    man = json.load(open(os.path.join(china_map, fig.split('data-geo="', 1)[1].split('"', 1)[0]), encoding="utf-8"))
    assert man["opt"] == {"shown": ["prc", "roc", "hong-kong", "macau"], "dot": cnmap.DOT, "city": cnmap.CITY,
                          "unit": "as of 1966"}
    assert man["bounds"] == cnmap.BOUNDS and man["home"] == {"all": cnmap.HOME}
    pts = {f["properties"]["id"]: f["properties"] for f in man["places"]["features"]}
    assert set(pts) == {"peking", "taipei"} and pts["peking"]["r"] == 1 and pts["peking"]["name"] == "Peking"
    assert man["files"] == {} and "page" in man["credit"]      # no geometry in the fixture: the build copies none


def test_gazetteer_table(china_map):
    s = _series()
    es = [e for _, e in s.lists["cal"].entries() if "when" in e and "place" not in e][:2]
    try:
        for e, p in zip(es, ["sichuan", "niujiao"]):
            e["place"] = p
        html, n, n_on = china._gazetteer(s)
    finally:
        for e in es:
            e.pop("place", None)
    assert (n, n_on) == (4, 2)
    assert '<tr id="pl-peking"><td><a href="https://en.wikipedia.org/wiki/Beijing">Peking</a></td><td lang="zh">北京市</td><td>Peking</td>' in html
    assert 'Sichuan <span class="m">(the province as a whole)</span>' in html
    assert "not on the map: a village of Chang&#x27;an county, Shaanxi; neither source has it" in html
    assert '<span class="m">Taiwan</span>' in html
    assert '<a href="#y1961">' in html                         # Peking: over LIST entries, the year's count, to the map
    assert html.count('<b class="ty">1961</b>') == 3           # Peking, Sichuan and Niujiao, each by year


def test_one_client():
    """One client for both maps: no second script or stylesheet, and the client's China is data, not code."""
    here = os.path.join(TOOLS, "bib")
    assert not [f for f in os.listdir(here) if f.startswith("cnmap") and f.endswith((".js", ".css"))]
    js = open(os.path.join(here, "vnmap.js"), encoding="utf-8").read()
    code = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    code = "\n".join(l.split("//")[0] for l in code.split("\n"))
    assert not re.search(r"\bchina\b|'prc'|'cn'", code, re.I)
    for opt in ("O.shown ||", "O.dot ||", "O.city ||", "O.unit", "this.D.eu", "this.D.map", "this.D.mode", "this.D.home"):
        assert opt in js, opt
    assert "['rvn', 'drv', 'laos', 'cambodia']" in js and "O.dot || 2.6" in js      # Indochina's own stay the defaults
    assert "O.city || 0.0105" in js and cnmap.CITY == 0.0105 / 2


# ---- the layers (the owner, Nov. 25, 2026: "Which of the SEA map overlays can we also use on our China map? Bring
# them over."): the maps of Indochina's boxes, legend and files, by the same code; the data alone differs

LAYER_BOXES = ["relief", "elevation", "contours", "rivers", "koppen", "rain", "pop", "cities"]
CITIES = """sources:
  dyb1966: United Nations, *Demographic Yearbook 1966*, table 6
cities:
- place: peking
  as: PEKING
  rows:
  - {date: '1957-12-31', kind: E, pop: 4010000, of: city proper, src: dyb1966, page: 185}
- id: fushun
  name: Fushun
  lat: 41.87
  lon: 123.89
  q: Q75026
  rows:
  - {date: '1957-12-31', kind: E, pop: 985000, of: city proper, src: dyb1966, page: 185, note: In italics.}
- place: sichuan
  rows:
  - {date: '1953-06-30', kind: C, pop: 1, of: city proper, src: dyb1966, page: 185}
"""


@pytest.fixture
def china_layers(china_map, monkeypatch, tmp_path):
    """The map's directory with every layer's file in it (a few bytes each: the build copies, it reads no geometry)."""
    src = tmp_path / "china"
    os.makedirs(src)
    for f in cnmap.FILES.values():
        (src / f).write_bytes(b"{}")
    (src / "hypso.json").write_text(json.dumps({"classes": [
        {"index": 0, "kind": "land", "from_m": 0, "to_m": 5000, "label": "0–5,000 m", "color": "#acd0a5"},
        {"index": 1, "kind": "land", "from_m": 5000, "to_m": None, "label": "5,000 m and over", "color": "#cac3b8"},
        {"index": 2, "kind": "sea", "depth_from_m": 0, "depth_to_m": 50, "label": "0–50 m deep", "color": "#d8eaf4"},
        {"index": 3, "kind": "sea", "depth_from_m": 50, "depth_to_m": None, "label": "50 m and deeper", "color": "#c6dff0"}]}))
    (src / "koppen.json").write_text(json.dumps({"classes": [
        {"value": 7, "code": "BSk", "name": "Arid, steppe, cold", "color": "#ffdc64", "share_of_land_in_frame": 0.2},
        {"value": 1, "code": "Af", "name": "Tropical, rainforest", "color": "#0000ff", "share_of_land_in_frame": 0.0001}]}))
    (src / "cities.yaml").write_text(CITIES, encoding="utf-8")
    monkeypatch.setattr(cnmap, "SRC", str(src))
    return src


def test_layer_boxes(china_layers):
    """The layers' boxes are the maps of Indochina's, in their order, after this map's own two; the rain's month and
    the population's year after them. With no file, no box (the fixture: test_figure_and_data)."""
    bar = cnmap._bar()
    assert re.findall(r'data-l="(\w+)"', bar) == ["names", "counties"] + LAYER_BOXES
    assert re.findall(r'data-mode="(\w+)"', bar) == ["prov", "borders", "land"]
    assert bar.index('data-l="cities"') < bar.index("<select data-m") < bar.index("<select data-py")
    theirs = vnmap.bar((), [], set(vnmap.FILES), True)
    mine = cnmap._bar()
    cut = lambda h: h[h.index('<label><input type="checkbox" data-l="relief">'):]
    assert cut(mine) == cut(theirs)                         # the same markup to the last byte
    os.remove(china_layers / "contours.geojson")
    os.remove(china_layers / "cities.yaml")
    assert re.findall(r'data-l="(\w+)"', cnmap._bar()) == ["names", "counties", "relief", "elevation", "rivers", "koppen", "rain", "pop"]


def test_layer_key(china_layers):
    """The legend's layer parts are vnmap.layer_key's, with this map's own words; a class under 0.1 percent of the
    frame is left out, as on the maps of Indochina."""
    key = cnmap._key()
    for k in LAYER_BOXES:
        assert f'data-show="lay:{k}"' in key, k
    assert "ETOPO 2022 (30″, about 900 m)" in key and "5,000 m and over" in key and "50 m and deeper" in key
    assert "Contours at 500 m (dashed), 1,000, 2,000, 3,000, 4,000 and 5,000 m." in key
    assert "mm a month (cells of half a degree):" in key and "lon. 100" not in key
    assert "BSk Arid, steppe, cold" in key and "Tropical, rainforest" not in key
    assert key.index('data-show="lay:counties"') < key.index('data-show="lay:relief"')
    parts = []
    vnmap.layer_key(lambda show, html: parts.append(show), vnmap._legends(str(china_layers)), vnmap.WORDS)
    assert parts == ["lay:" + k for k in LAYER_BOXES]


def test_layer_files(china_layers):
    """Each layer's file goes beside the pages under its own hash and extension; the cities as points, a city at its
    gazetteer place or at its own point; the credits of the files that are there; the legends' data."""
    s = _series()
    man = json.load(open(os.path.join(china_layers.parent, cnmap.manifest(s)), encoding="utf-8"))
    assert set(man["files"]) == set(cnmap.FILES) | {"cities"}
    for k, f in cnmap.FILES.items():
        assert re.fullmatch(rf"geo/cn-{f.split('.')[0]}-[0-9a-f]{{10}}\.{f.split('.')[1]}", man["files"][k]), k
    assert set(man["credit"]) == set(cnmap.FILES) | {"page"}
    assert "their names from SWORD" in man["credit"]["rivers"] and man["credit"]["dem"] == vnmap.CREDIT["dem"]
    assert [h["from"] for h in man["hypso"]] == [0, 5000] and [d["from"] for d in man["depths"]] == [50]
    assert man["shallow"] == "#d8eaf4" and man["pop"]["years"] == [1960, 1970] and len(man["rain"]) == len(vnmap.RAIN)
    fc = json.load(open(os.path.join(china_layers.parent, man["files"]["cities"]), encoding="utf-8"))
    got = {f["properties"]["id"]: f for f in fc["features"]}
    assert set(got) == {"peking", "fushun"}                 # a province named as a place has no point: no circle
    assert got["peking"]["geometry"]["coordinates"] == [116.4075, 39.904] and got["peking"]["properties"]["label"] == "Peking 4,010,000"
    assert got["fushun"]["geometry"]["coordinates"] == [123.89, 41.87] and got["fushun"]["properties"]["pop"] == 985000
    rows = json.loads(got["peking"]["properties"]["rows"])
    assert rows == [{"text": "4,010,000 (city proper), estimate of Dec. 31, 1957: United Nations, Demographic Yearbook "
                             "1966, table 6, p. 185."}, {"text": "The Yearbook's name: PEKING."}]
    assert json.loads(got["fushun"]["properties"]["rows"])[0]["text"].endswith("p. 185. In italics.")


def test_layers_wherever_the_map_stands(china_layers):
    """The layers are offered wherever the map stands, as the maps of Indochina's are: the map's own page, a calendar
    page's figure and a thread's all carry the one box, with the same boxes and legend."""
    import datetime
    s = _series()
    lst = s.lists["cal"]
    full = cnmap.full_figure(s)
    cal = maps.figure(s, cnmap, datetime.date(1961, 1, 1), datetime.date(1961, 12, 31))
    slug = next(k for r in maps.entries(s, cnmap)["rows"] for k in r["k"])
    th = maps.figure(s, cnmap, datetime.date(1961, 1, 1), datetime.date(1961, 12, 31), th=slug, here="t-")
    box = lambda fig: re.sub(r'aria-label="[^"]*"', "", fig[fig.rindex('<div class="vnm-bar">'):fig.index('<details class="vnm-list">')])
    assert cal and th and box(full) == box(cal) == box(th)
    assert re.findall(r'data-l="(\w+)"', box(cal)) == ["names", "counties"] + LAYER_BOXES
    assert all(f'data-show="lay:{k}"' in cal for k in LAYER_BOXES)
    assert cal.split('data-geo="', 1)[1].split('"', 1)[0] == full.split('data-geo="', 1)[1].split('"', 1)[0]   # one manifest


@pytest.mark.parametrize("city, want", [
    ("- place: atlantis\n  rows: []\n", "atlantis: no such place"),
    ("- id: x\n  name: X\n  lat: 1.0\n  rows: []\n", "x: needs a place, or id, name, lat, lon and q"),
    ("- place: peking\n  rows:\n  - {date: '1957', kind: E, pop: 1, of: city proper, src: dyb1966}\n", "peking 1957: needs pop, src and page"),
    ("- place: peking\n  rows:\n  - {date: '1957', kind: E, pop: '1', of: city proper, src: dyb1966, page: 1}\n", "peking 1957: needs pop, src and page"),
    ("- place: peking\n  rows:\n  - {date: '1957', kind: E, pop: 1, of: city proper, src: dyb1999, page: 1}\n", "peking 1957: needs pop, src and page"),
])
def test_city_problems(china_layers, city, want):
    (china_layers / "cities.yaml").write_text(CITIES.split("cities:")[0] + "cities:\n" + city, encoding="utf-8")
    got = [m for w, m in cnmap.problems(None) if w == "cnmap"]
    assert any(m == "sources/china/cities.yaml: " + want or m.startswith("sources/china/cities.yaml: " + want) for m in got), got


def test_cities_clean(china_layers):
    assert [m for w, m in cnmap.problems(None) if "cities.yaml" in m] == []


def test_yearbook_cities_are_places():
    """The map's own cities.yaml (the owner, Nov. 25, 2026: "Add the cities to the gazetteer"): every city names a
    gazetteer place with a point and carries none of its own; the 34 made places for it are tools/cnmap/places.py's
    CITY, each at the Wikidata item named there. "Malibo" and the Yangmingshan Administration stay unplaced."""
    import importlib.util
    root = os.path.dirname(TOOLS)                           # the repository's own files, not the fixture's
    src = os.path.join(root, "sources", "china")
    spec = importlib.util.spec_from_file_location("cnmap_places", os.path.join(TOOLS, "cnmap", "places.py"))
    cnplaces = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cnplaces)
    c = store.load_yaml(os.path.join(src, "cities.yaml"))
    G = {p["key"]: p for p in json.load(open(os.path.join(src, "places.json"), encoding="utf-8"))["places"]}
    gz = {r["key"]: r for r in store.load_yaml(os.path.join(root, "sources", "places.yaml"))}
    assert len(c["cities"]) == 116 and len({x["place"] for x in c["cities"]}) == 116
    for x in c["cities"]:
        assert not {"id", "name", "lat", "lon", "q"} & set(x), x["place"]
        assert x["place"] in gz and G[x["place"]].get("lat") is not None, x["place"]
    assert len(cnplaces.CITY) == 34 and set(cnplaces.CITY) <= {x["place"] for x in c["cities"]}
    for k, q in cnplaces.CITY.items():
        assert G[k]["q"] == q and cnmap.in_china(gz[k]), k
    assert [u["as"] for u in c["unplaced"]] == ["Malibo", "Yangmingshan Administration"]


def test_layer_sizes(china_layers, monkeypatch):
    """`check`'s size rules hold for China's layers as for Indochina's: a file over the limit, the files together."""
    monkeypatch.setattr(vnmap, "MAX_FILE", 1)
    got = [m for w, m in cnmap.problems(None)]
    for f in cnmap.FILES.values():
        assert f"sources/china/{f}: 2 bytes, over 1" in got, f
    monkeypatch.setattr(vnmap, "MAX_FILE", 10)
    monkeypatch.setattr(vnmap, "MAX_ALL", 5)
    got = [m for w, m in cnmap.problems(None)]
    assert got == [f"sources/china: the map's files {2 * len(cnmap.FILES)} bytes together, over 5"]


def test_layers_load_when_ticked():
    """The client fetches nothing of a layer before its box is ticked or a pin is dropped (vnmap STYLE 9): every GeoJSON
    layer's source starts empty, the cities' too, and takes its file in `load`; the tiles are read by the library when
    their layer is first shown."""
    js = open(os.path.join(TOOLS, "bib", "vnmap.js"), encoding="utf-8").read()
    lazy = re.search(r"const LAZY = \{([^}]*)\}", js)[1]
    for k in ("rivers", "lakes", "contours", "bathy", "climate", "pop", "counties"):
        assert f"{k}: '{k}'" in lazy, k
    assert "cities: {type: 'geojson', data: EMPTY}" in js and "if (lay.cities) load('cities');" in js
    assert "data: EMPTY, attribution: M.credit[k]" in js
    css = open(os.path.join(TOOLS, "bib", "vnmap.css"), encoding="utf-8").read()
    assert ".vnm-key s>i{" in css and ".vnm-key i{" not in css      # a swatch is an <i> in an <s>; a title's <i> is italics
    for k in ("dem", "koppen"):
        assert f"if (f.{k}) src.{k} = " in js and f"f.{k} && {{id: " in js


def test_frames():
    """tools/vnmap/frames.py: the layer scripts' numbers. Indochina's are those the scripts held before they served a
    second frame, so its files come out the same; China's are the choices sources/china/README.md states."""
    sys.path.insert(0, os.path.join(TOOLS, "vnmap"))
    import frames
    f, rest = frames.get(["DIR"])
    assert f["id"] == "indochina" and rest == ["DIR"] and f["out"].endswith(os.path.join("sources", "indochina"))
    assert (f["frame"], f["extent"]) == ((97.5, 5.5, 113.0, 26.0), (100.0, 8.0, 110.5, 23.5))
    assert (f["dem_maxz"], f["koppen_maxz"], f["mean"], f["levels"]) == (8, 7, 4, [500, 1000, 1500, 2000])
    assert (f["depth_tol"], f["contour_tol"], f["contour_min"], f["bands"]) == (0.01, 0.003, 0.03, None)
    assert (f["pop_cells"], f["pop_tol"], f["pop_prec"], f["rain_cells"]) == (1, 0.004, 3, 1)
    assert (f["river_min"], f["river_read"], f["river_tol"], f["lake_min"], f["lake_tol"]) == (10, None, 0.002, 1.0, 0.001)
    assert f["sword"] == (43, 44) and len(f["delta"]) == 8 and f["etopo_sec"] == 15 and f["lake_fill"] is None
    c, rest = frames.get(["DIR", "OUT", "china", "hydro"])
    assert c["id"] == "china" and rest == ["DIR", "OUT", "hydro"] and c["out"].endswith(os.path.join("sources", "china"))
    assert c["frame"] == (66.0, 10.0, 142.0, 58.0) and list(c["extent"]) == cnmap.BOUNDS
    assert c["river_min"] == c["river_read"] and c["pop_cells"] == c["rain_cells"] == 3
    # the deltas (the owner, Nov. 25, 2026: "Draw the river deltas"): seven rings inside the rivers' extent, SWORD's
    # channels of 50 m and wider in them; Indochina's one ring, with every reach, as before
    assert list(c["delta"]) == ["pearl", "han", "yangtze", "yellow", "red", "irrawaddy", "ganges"]
    w, s, e, n = c["extent"]
    assert all(len(r) >= 5 and all(w < x < e and s < y < n for x, y in r) for r in c["delta"].values())
    assert (c["delta_min"], f["delta_min"], f["delta_to_sea"]) == (50, 0, ("Mekong River", "Bassac"))
    assert set(c["delta_to_sea"]) >= set(c["to_sea"]) - {"Amur"}
    # the relief: a zoom deeper than the rule of four gives (the owner, Nov. 25, 2026: "Make the relief sharp!"), and
    # the lakes whose floor the model holds raised to their surface ("Mend Lake Baikal.")
    assert (c["dem_maxz"], c["etopo_sec"], c["lake_fill"]) == (6, 30, (10.0, 50.0))
    assert [b[0] for b in c["bands"]] == [0, 100, 200, 500, 1000, 1500, 2000, 3000, 4000, 5000]
    assert c["bands"][:6] == frames.LAND7 and c["levels"][0] == 500 and c["levels"][-1] == 5000
    assert "5,000" in cnmap.WORDS["contours"] and all(f"{v:,}" in cnmap.WORDS["contours"] for v in c["levels"][1:])


# ---- tools/cnmap/counties.py: the record

@pytest.mark.parametrize("name, base, kind", [
    ("阳曲县", "阳曲", "county"), ("太原市", "太原", "city"), ("应县", "应县", "county"),
    ("杜尔伯特蒙古族自治县", "杜尔伯特", "autonomous county"), ("东兴各族自治县", "东兴", "autonomous county"),
    ("阿鲁科尔沁旗", "阿鲁科尔沁", "banner"), ("鄂伦春自治旗", "鄂伦春", "autonomous banner"),
    ("莫力达瓦达斡尔族自治旗", "莫力达瓦", "autonomous banner"), ("桓仁满族自治县", "桓仁", "autonomous county"),
    ("六枝特区", "六枝", "special district"), ("潇水林区管理局", "潇水林区", "administration"),
])
def test_base_and_kind(name, base, kind):
    assert (counties.base(name), counties.kind(name)) == (base, kind)


PREV = [{"n": n} for n in ("大同市", "离石县", "中阳县", "沙湾县", "舟曲县", "朔县", "长治市", "长治县")] + [{"n": "城区", "d": True}]


@pytest.mark.parametrize("name, want", [
    ("离石县", "离石县"),            # the same name
    ("朔州市", None),                # another name: the year's changes must say
    ("离石市", "离石县"),            # a county made a city
    ("长治县", "长治县"), ("长治市", "长治市"),   # a city and a county of one name: each its own
    ("大同县", "大同市"),            # a county restored out of the city of its name
    ("城区", None),                  # a city's district is no unit
])
def test_find_prev(name, want):
    assert counties.find_prev(name, PREV) == want


@pytest.mark.parametrize("name, notes, want", [
    ("古交工矿区", "★1964年10月31日国务院全体会议第148次会议决定：\n1．设立古交工矿区。以阳曲县的部分行政区域为古交工矿区的行政区域。", None),
    ("柳林县", "设立柳林县，以离石县和中阳县的部分行政区域为其行政区域。（国务院1971年5月批准）", ("离石县", "first of several")),
    ("石河子市", "设立石河子市，以沙湾县的石河子镇和沙湾县的部分地区为其行政区域。（国务院1976年1月2日批准）", ("沙湾县", "part")),
    ("龙叠县", "1.舟曲县改名为龙叠县（国务院1959年1月3日批准）", ("舟曲县", "renamed")),
    ("朔州市", "撤销朔县，设立朔州市。", ("朔县", "renamed")),
    ("新县", "平山县驻地由岗南迁回城关。", None),
])
def test_from_notes(name, notes, want):
    got = counties.from_notes(name, notes, PREV)
    assert (got and got[:2]) == want


def _rec(years):
    return {"L": {y: {"units": [{"n": n} for n in names], "notes": notes} for y, (names, notes) in years.items()}}


def test_walk():
    rec = _rec({
        1964: (["离石县", "中阳县", "朔县"], ""),
        1971: (["离石县", "中阳县", "朔县", "柳林县"], "设立柳林县，以离石县和中阳县的部分行政区域为其行政区域。"),
        1989: (["离石县", "中阳县", "朔州市", "柳林县"], "撤销朔县，设立朔州市。"),
        1994: (["离石市", "中阳县", "朔州市", "柳林县", "新城县"], ""),
    })
    w = lambda n: counties.walk("L", n, 1994, rec)[:3]
    assert w("中阳县") == ("L", "中阳县", "same")
    assert w("离石市") == ("L", "离石县", "same")              # a county made a city is the same unit
    assert w("朔州市") == ("L", "朔县", "renamed")
    assert w("柳林县") == ("L", "离石县", "first of several")   # a guess: the first named of two
    assert w("新城县") == ("L", None, "unresolved")            # the changes do not say: shown under its later name


PAGE = """<html><div class="content">1964年末，某省辖1专区、1省辖市，3县、2市辖区。<br />
<strong>县级以上行政区划一览</strong><br />
<strong>太原市</strong>　2区、1县<br />
　南城区　　　　北城区<br />
　阳曲县（黄寨）<br />
<strong>雁北专区</strong>　　专署驻大同市　　2县<br />
　应　县（城关镇）　朔　县（城关镇）<br />
★1964年10月31日国务院决定：<br />1．恢复大同县。<div class="ad_26"></div></div></html>""".encode("gb18030")


def test_page():
    p = counties.page(PAGE, "10005")
    assert p["summary"].startswith("1964年末")
    assert [(u["n"], u.get("pref"), bool(u.get("top")), bool(u.get("d")), u.get("seat", "")) for u in p["units"]] == [
        ("太原市", "太原市", True, False, ""), ("南城区", "太原市", False, True, ""), ("北城区", "太原市", False, True, ""),
        ("阳曲县", "太原市", False, False, "黄寨"), ("应县", "雁北专区", False, False, "城关镇"),
        ("朔县", "雁北专区", False, False, "城关镇")]
    assert p["notes"] == "★1964年10月31日国务院决定：\n1．恢复大同县。"


def test_page_slips():
    """The record's own slips are set right as a page is read: a character anywhere, a name in one province's lists."""
    b = "<html><div class=\"content\">1965年末，某省辖3县。<br />\n　灃　县（城关镇）　临灃县　庆元县<br /></div></html>".encode("gb18030")
    assert [u["n"] for u in counties.page(b, "10020")["units"]] == ["澧县", "临澧县", "庆元县"]
    assert [u["n"] for u in counties.page(b, "10017")["units"]] == ["澧县", "临澧县", "庆云县"]


def test_walk_restored():
    """A unit joined to another after 1964 and restored is the unit of 1964, not the one it was joined to."""
    rec = _rec({
        1964: (["辽阳市", "辽阳县", "松溪县", "政和县"], ""),
        1970: (["辽阳市", "松溪县"], "将辽阳县并入辽阳市。"),
        1980: (["辽阳市", "辽阳县", "松溪县", "政和县"], "一、恢复辽阳县。恢复政和县，以合并于松溪县的原政和县的行政区域为政和县的行政区域。"),
    })
    w = lambda n: counties.walk("L", n, 1980, rec)[:3]
    assert w("政和县") == ("L", "政和县", "same")              # the changes say restored, and the list of 1964 has it
    assert w("辽阳县") == ("L", "辽阳县", "same")              # by way of the city of its name, back to the county
    assert w("辽阳市") == ("L", "辽阳市", "same")


def test_hand_tables():
    """The rows settled by hand name real lists; a unit is named once."""
    assert all(l in counties.LISTS and zh for l, zh in counties.NAMED.values())
    assert all(l in counties.LISTS for l in counties.PROVINCE.values())
    assert not set(counties.NAMED) & set(counties.PROVINCE)
    for (l, zh), (l64, zh64, basis, ground) in counties.BACK.items():
        assert l in counties.LISTS and l64 in counties.LISTS and ground
        assert basis in ("renamed", "part", "first of several", "unresolved") and (zh64 is None) == (basis == "unresolved")


def test_romanise():
    pytest.importorskip("pypinyin")
    assert [counties.romanise(n) for n in ("阳曲县", "西安市", "应县", "东兴各族自治县")] == ["Yangqu", "Xi'an", "Ying", "Dongxing"]
    assert counties.pinyin("漠河县") == "mohexian"
    # the place-name readings the library misses, and a one-character name read with its kind
    assert [counties.romanise(n) for n in ("于都县", "朝阳县", "长子县", "长葛县", "漯河市", "泊头市", "蔚县", "都安瑶族自治县")] == [
        "Yudu", "Chaoyang", "Zhangzi", "Changge", "Luohe", "Botou", "Yu", "Du'an"]
