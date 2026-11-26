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

from bib import china, cnmap, places as gaz, store, vnmap

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
    monkeypatch.setattr(vnmap, "OUT", str(tmp_path))
    monkeypatch.setattr(vnmap, "_fonts", lambda: {})          # the fixture holds no vendored font
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
    """The figure is the maps of Indochina's (its classes), told apart by data; the entries are in a file of their own."""
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
    assert d["map"] == "cn" and d["mode"] == "prov" and d["y"] == "all" and "e" not in d
    assert d["ys"][0] == "1960" and "1969" in d["ys"] and d["pn"] == {"peking": "Peking"}
    assert d["eu"].startswith("geo/cn-entries-") and d["eu"].endswith(".json")
    ents = json.load(open(os.path.join(china_map, d["eu"]), encoding="utf-8"))
    assert f"All years: {len(ents)} placed entries, at 1 places." in fig
    mine = {e["id"]: next((x for x in ents if x["h"].endswith("#" + e["id"])), None) for e in es}
    assert (mine[es[0]["id"]]["p"], mine[es[0]["id"]]["v"]) == ([], ["sichuan"])      # the province as a whole
    assert (mine[es[1]["id"]]["p"], mine[es[1]["id"]]["v"]) == (["peking"], ["sichuan"])
    assert mine[es[2]["id"]] is None                                                    # a place not on the map
    assert all(set(x) == {"h", "w", "t", "s", "p", "v", "y"} for x in ents)
    assert all(x["p"] == ["peking"] for x in ents if x["v"] == [])                      # the fixture's own entries in Peking
    man = json.load(open(os.path.join(china_map, fig.split('data-geo="', 1)[1].split('"', 1)[0]), encoding="utf-8"))
    assert man["opt"] == {"shown": ["prc", "hong-kong", "macau"], "dot": cnmap.DOT, "unit": "as of 1966"}
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
    for opt in ("O.shown ||", "O.dot ||", "O.unit", "this.D.eu", "this.D.map", "this.D.mode"):
        assert opt in js, opt
    assert "['rvn', 'drv', 'laos', 'cambodia']" in js and "O.dot || 2.6" in js      # Indochina's own stay the defaults


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
