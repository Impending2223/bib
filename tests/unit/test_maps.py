"""The two maps wherever they stand (tools/bib/maps.py): the span and its labels, the entries' files, a figure in a
calendar page and at the head of a thread's page, where a map stands, the page that lists the two; the client's
reading of a date typed into a span's field (vnmap.js, run in node where node is there); and the table of the
Republic of China's units (tools/cnmap/roc.py).

Written Nov. 26, 2026, with the maps' second step (notes/briefs/maps-2.md). The rows pin what the functions returned
then. The maps' own data is not in the fixture: the tests give the map of China a small gazetteer of their own, as
test_cnmap.py does, and the fixture's entries placed in Peking are its entries.
"""
import datetime
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

from bib import calsplit, cnmap, contents, daybook, dayblocks, maps, places as gaz, store, vnmap

from test_cnmap import MAP, ROWS, UNITS

TOOLS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "tools")
sys.path.insert(0, os.path.join(TOOLS, "cnmap"))
import roc  # noqa: E402  (tools/cnmap/roc.py: the table needs no download and no shapely)

D = datetime.date


@pytest.fixture
def china(monkeypatch, tmp_path):
    """The map of China ready on the fixture: a small gazetteer, an empty vendored library, the build's files in a
    directory of the test's own; the map of Indochina as the fixture has it (no data: not ready)."""
    monkeypatch.setattr(gaz, "_ROWS", [dict(r) for r in ROWS])
    monkeypatch.setattr(gaz, "_INDEX", {r["key"]: r for r in ROWS})
    monkeypatch.setattr(cnmap, "_C", {"pl": {k: dict(v) for k, v in MAP.items()}, "u": dict(UNITS), "c": {}})
    monkeypatch.setattr(vnmap, "_C", {})
    monkeypatch.setattr(maps, "_C", {})
    monkeypatch.setattr(vnmap, "OUT", str(tmp_path))
    monkeypatch.setattr(vnmap, "VENDOR", str(tmp_path / "vendor"))
    for d in (vnmap.MAPLIBRE, vnmap.PMTILES):
        os.makedirs(tmp_path / "vendor" / d)
    monkeypatch.setattr(vnmap, "_fonts", lambda: {})
    monkeypatch.setattr(calsplit, "CUR", {"half": None, "mode": "list"})
    return store.Series(), tmp_path


# ---------------------------------------------------------------- dates, spans, titles

@pytest.mark.parametrize("d, want", [("1963", "1963-01-01"), ("1963-04", "1963-04-01"), ("1963-04-15", "1963-04-15")])
def test_pad(d, want):
    assert maps.pad(d) == want


@pytest.mark.parametrize("lo, hi, want", [
    (D(1961, 4, 1), D(1961, 6, 30), "Apr. 1–June 30, 1961"),            # one year: the year once
    (D(1960, 1, 6), D(1976, 8, 31), "Jan. 6, 1960–Aug. 31, 1976"),
    (D(1969, 1, 1), D(1969, 1, 20), "Jan. 1–20, 1969"),                 # one month: the month once
    (D(1962, 9, 3), D(1962, 9, 3), "Sept. 3, 1962"),                    # one day
])
def test_span(lo, hi, want):
    assert maps.span(lo, hi) == want


@pytest.mark.parametrize("key, vn, cn", [
    ("1966-01-01.1966-03-31", "Southeast Asia, Jan.–Mar. 1966", "China, Jan.–Mar. 1966"),
    ("1960-01-06.1960-06-30", "Southeast Asia, Jan.–June 1960", "China, Jan.–June 1960"),   # the calendar's first page
    ("1961-01-01.1961-12-31", "Southeast Asia 1961", "China 1961"),            # a bare year: no comma
    ("1969-01-01.1969-01-20", "Southeast Asia, Jan. 1969", "China, Jan. 1969"),
    ("1972-03-01.1976-08-31", "Southeast Asia, Mar. 1972–Aug. 1976", "China, Mar. 1972–Aug. 1976"),
    ("1966", "Southeast Asia 1966", "China 1966"),                             # the key of before Nov. 26, 2026
])
def test_titles(key, vn, cn):
    assert (contents.label("vnmap", key), contents.label("cnmap", key)) == (vn, cn)


def test_fields():
    """Two text fields, filled with the page's range in the calendar's form: no date picker, no slider."""
    h = maps.fields(D(1961, 4, 1), D(1961, 6, 30))
    assert h.startswith('<div class="vnm-bar"><label>From <input type="text" data-sp="from"')
    assert re.findall(r'<input type="(\w+)" data-sp="(\w+)" size="13" value="([^"]+)"', h) == [
        ("text", "from", "Apr. 1, 1961"), ("text", "to", "June 30, 1961")]


@pytest.mark.parametrize("rows, want", [([], "0 placed entries, at 0 places."),
                                        ([{"p": ["a"]}], "1 placed entry, at 1 place."),
                                        ([{"p": ["a", "b"]}, {"p": ["a"]}, {"p": []}], "3 placed entries, at 2 places.")])
def test_count(rows, want):
    assert maps.count(rows) == want


# ---------------------------------------------------------------- the threads that carry a map

class Threads:
    T = {"china": {}, "china-foreign": {"parent": "china"}, "china-moscow": {"parent": "china-foreign"},
         "china-old": {"parent": "china", "see": "china-foreign"}, "vietnam": {}, "vietnam-tet": {"parent": "vietnam"},
         "laos": {}, "cambodia": {}, "southeast-asia": {}, "korea": {}, "korea-troops": {"parent": "korea"},
         "loop": {"parent": "loop"}, "orphan": {"parent": "gone"}}

    def threads(self):
        return self.T


@pytest.mark.parametrize("slug, want", [
    ("china", "cn"), ("china-foreign", "cn"), ("china-moscow", "cn"),      # by the line of parents, two deep
    ("vietnam", "vn"), ("vietnam-tet", "vn"), ("laos", "vn"), ("cambodia", "vn"), ("southeast-asia", "vn"),
    ("korea", None), ("korea-troops", None), ("loop", None), ("orphan", None), ("no-such", None)])
def test_of_thread(slug, want):
    m = maps.of_thread(Threads(), slug)
    assert (m.KEY if m else None) == want


def test_thread_slugs():
    """A new thread under `china` carries the map with no list of names kept; an old name (`see:`) has no page."""
    got = maps.thread_slugs(Threads())
    assert got == {"cn": ["china", "china-foreign", "china-moscow"],
                   "vn": ["vietnam", "vietnam-tet", "laos", "cambodia", "southeast-asia"]}


# ---------------------------------------------------------------- the entries' files and a figure

def test_not_ready_on_the_fixture(monkeypatch):
    """The fixture holds no map data: no entries, no figure, no page of the two maps."""
    for m in (cnmap, vnmap, maps):
        monkeypatch.setattr(m, "_C", {})
    s = store.Series()
    assert not vnmap.ready() and not cnmap.ready()
    assert maps.entries(s, cnmap) == {"rows": [], "files": {}, "ys": []} and maps.stands(s) == {}
    assert maps.figure(s, cnmap, D(1961, 1, 1), D(1961, 12, 31)) == ""
    assert maps.page(s, os.path.join(store.ROOT, "templates", "list.html")) is None
    assert maps.inject("<head></head><body></body>", s, "list") == "<head></head><body></body>"


def test_entries(china):
    s, out = china
    E = maps.entries(s, cnmap)
    assert E["ys"] == ["1961"] and list(E["files"]) == ["1961"]
    assert re.fullmatch(r"geo/cn-entries-1961-[0-9a-f]{10}\.json", E["files"]["1961"])
    f = json.load(open(out / E["files"]["1961"], encoding="utf-8"))
    assert set(f) == {"k", "e"} and len(f["e"]) == len(E["rows"]) > 0
    assert all(set(x) == {"h", "w", "d", "t", "s", "p", "v", "k"} for x in f["e"])
    assert all(re.fullmatch(r"1961-\d\d-\d\d", x["d"]) for x in f["e"])
    assert [x["d"] for x in f["e"]] == sorted(x["d"] for x in f["e"])                 # the calendar's order
    assert all(x["h"].startswith(("cal1961H1.html#cal.", "cal1961H2.html#cal.")) for x in f["e"])   # its page named
    assert f["k"] == sorted(set(f["k"])) and all(all(0 <= i < len(f["k"]) for i in x["k"]) for x in f["e"])
    lst = s.lists["cal"]
    by = {e["id"]: e for _, e in lst.entries()}
    for r, x in zip(E["rows"], f["e"]):                 # an entry's threads: its `thread`, then its `also`
        e = by[r["_id"]]
        assert [f["k"][i] for i in x["k"]] == list(dict.fromkeys([e["thread"]] + list(e.get("also") or [])))
        assert r["_n"] == calsplit.half_of_date(lst, x["d"])
    assert all(x["p"] == ["peking"] or x["v"] for x in f["e"])                        # on the map, each of them


def test_figure(china):
    """A figure away from its map's page: the page's range in the fields, no entry in the page, the years' files."""
    s, out = china
    E = maps.entries(s, cnmap)
    lo, hi = D(1961, 1, 1), D(1961, 6, 30)
    fig = maps.figure(s, cnmap, lo, hi)
    inn = maps.within(E["rows"], lo, hi)
    assert 0 < len(inn) < len(E["rows"])                # April's, not August's
    assert fig.startswith(f'<figure class="vnm full" style="--vnar:{cnmap.AR:.4f}" data-geo="geo/cn-manifest-')
    assert f'<span class="vnm-cnt">Jan. 1–June 30, 1961: {len(inn)} placed entries, at 1 place.</span>' in fig
    assert 'value="Jan. 1, 1961"' in fig and 'value="June 30, 1961"' in fig
    assert fig.count('class="vnm-bar"') == 2 and 'class="vnm-yrs"' not in fig       # the fields' bar, the controls'
    assert f"<summary>The placed entries ({len(inn)})</summary><ol></ol>" in fig
    assert '<a href="china.html#y1961">China</a>' in fig
    d = json.loads(fig.split('class="vnm-d">', 1)[1].split("</script>", 1)[0])
    assert d == {"map": "cn", "mode": "prov", "eu": E["files"], "ys": ["1961"], "sp": ["1961-01-01", "1961-06-30"],
                 "gz": "china.html"}
    assert len(fig) < 6000                              # a few kilobytes in the page, whatever the entries
    assert maps.figure(s, cnmap, D(1962, 1, 1), D(1962, 12, 31)) == ""               # no placed entry: no map
    assert json.loads(maps.figure(s, cnmap, lo, hi, here="").split('class="vnm-d">', 1)[1].split("</script>", 1)[0])["here"] == ""
    assert '<a href="china.html">China</a>' in maps.figure(s, cnmap, D(1960, 1, 6), D(1976, 8, 31))   # no one year


def test_indochina_figure(china, monkeypatch, tmp_path):
    """The map of Indochina away from its page: the calendar's box (not .full), the Republic widened to the span's
    places, its own controls; the same figure, fields and data as the map of China's."""
    s, out = china
    layers = tmp_path / "layers"
    os.makedirs(layers)
    (layers / "admin.geojson").write_text('{"type":"FeatureCollection","features":[]}')
    monkeypatch.setattr(vnmap, "LAYERS", str(layers))
    monkeypatch.setattr(vnmap, "_C", {"pl": {"hanoi": {"id": "hanoi", "name": "Hà Nội", "lat": 21.03, "lon": 105.85,
                                                       "country": "vn-north", "rank": 1}}, "u": {}})
    assert vnmap.ready()
    E = maps.entries(s, vnmap)
    assert E["ys"] == ["1961"] and len(E["rows"]) == 2 and all(r["p"] == ["hanoi"] for r in E["rows"])
    lo, hi = D(1961, 7, 1), D(1961, 12, 31)
    fig = maps.figure(s, vnmap, lo, hi)
    assert fig.startswith('<figure class="vnm" data-geo="geo/vn-manifest-')
    assert '<span class="vnm-cnt">July 1–Dec. 31, 1961: 1 placed entry, at 1 place.</span> Provinces as of late 1966' in fig
    assert 'data-mode="ctz"' in fig and 'data-l="nb"' in fig and fig.count('class="vnm-bar"') == 2
    assert '<a href="indochina.html#y1961">Indochina</a>' in fig
    d = json.loads(fig.split('class="vnm-d">', 1)[1].split("</script>", 1)[0])
    assert d == {"home": "rvn", "eu": E["files"], "ys": ["1961"], "sp": ["1961-07-01", "1961-12-31"], "gz": "indochina.html"}
    assert set(maps.stands(s)) == {(1, "vnmap"), (2, "vnmap"), (1, "cnmap"), (2, "cnmap")}
    full = vnmap.full_figure(s)
    d = json.loads(full.split('class="vnm-d">', 1)[1].split("</script>", 1)[0])
    assert set(d) == {"eu", "ys", "sp", "all", "gz"} and d["sp"] == d["all"] and d["gz"] == "" and "1968" in d["ys"]
    assert full.startswith('<figure class="vnm full" data-geo=') and "All years: 2 placed entries, at 1 place." in full
    assert full.index('class="vnm-yrs"') < full.index('data-sp="from"') < full.index('data-mode="ctz"')
    pg = maps.page(s, os.path.join(store.ROOT, "templates", "list.html"))      # both maps, Indochina first
    assert pg.index('href="indochina.html"><span class="ab">') < pg.index('href="china.html"><span class="ab">')


def test_thread_figure(china):
    """A thread's map: its own entries alone, the links kept on the page (t-), the years it has entries in."""
    s, out = china
    lst = s.lists["cal"]
    E = maps.entries(s, cnmap)
    slug = next(k for r in E["rows"] for k in r["k"])
    mine = [r for r in E["rows"] if slug in r["k"]]
    lo, hi = calsplit.part_range(lst, None)
    saved = dict(lst.threads()[slug])
    try:
        lst.threads()[slug]["parent"] = "china"         # under China by its line of parents, whatever its name
        lst.threads().setdefault("china", {"s": "China"})
        fig = maps.thread_figure(s, lst, slug, lo, hi)
        none = maps.thread_figure(s, lst, slug, D(1962, 1, 1), D(1962, 12, 31))
    finally:
        lst.threads()[slug].clear()
        lst.threads()[slug].update(saved)
    d = json.loads(fig.split('class="vnm-d">', 1)[1].split("</script>", 1)[0])
    assert d["th"] == slug and d["here"] == "t-" and d["sp"] == [lo.isoformat(), hi.isoformat()]
    assert d["ys"] == sorted({r["d"][:4] for r in mine}) and set(d["eu"]) == set(d["ys"])
    assert f"{len(mine)} placed entr" in fig and none == ""
    assert maps.thread_figure(s, lst, "no-such-thread", lo, hi) == ""


def test_stands_and_inject(china, monkeypatch):
    """In the calendar: under the day of the part's first placed entry that stands on a day, above the day's blocks;
    titled and listed by its span; the style and script once."""
    s, out = china
    lst = s.lists["cal"]
    E = maps.entries(s, cnmap)
    st = maps.stands(s)
    assert set(st) == {(1, "cnmap"), (2, "cnmap")}      # April in the first half, August in the second
    for (n, kind), (iso, eid) in st.items():
        rows = [r for r in E["rows"] if r["_n"] == n]
        assert eid == rows[0]["_id"] and iso == next(r["d"] for r in rows if r["_day"])
    assert maps.days(s) == {iso for iso, _ in st.values()}
    monkeypatch.setattr(daybook, "SERIES", s)
    iso, eid = st[(1, "cnmap")]
    assert dayblocks.marker(iso) == f"<!--dblk:{iso}-->"
    monkeypatch.setattr(calsplit, "CUR", {"half": 1, "mode": "list"})
    lo, hi = calsplit.part_range(lst, 1)
    mark = dayblocks.MARK.format(iso)
    page = maps.inject(f"<head></head><body><ol></ol>{mark}</body>", s, "list")
    key = f"{lo.isoformat()}.{hi.isoformat()}"
    aid = contents.anchor_id("cnmap", key)
    assert f'<span class="tba" id="{aid}" data-tb="{contents.label("cnmap", key)}" data-tbe="day:{iso}:china"></span>' in page
    assert page.index('class="tbt"') < page.index("<figure ") < page.index(mark)     # title, map, the day's blocks
    assert page.count("<figure ") == 1 and f'"sp":["{lo.isoformat()}","{hi.isoformat()}"]' in page
    assert page.count('class="vnm-css"') == 1 and page.count('<script type="module"') == 1
    # no day block's place on the page: at the end of the part's first placed entry
    page = maps.inject(f'<head></head><body><ol><li id="{eid}">x</li></ol></body>', s, "list")
    assert re.search(r'<li id="[^"]+">x<span class="tba" id="' + re.escape(aid) + '"', page) and "<figure " in page
    # the reader: every part's map, each on its part's range, its links kept in the page
    monkeypatch.setattr(calsplit, "CUR", {"half": None, "mode": "list"})
    marks = "".join(dayblocks.MARK.format(d) for d, _ in st.values())
    page = maps.inject(f"<head></head><body>{marks}</body>", s, "series")
    assert page.count("<figure ") == 2 and page.count('"here":""') == 2 and page.count('class="vnm-css"') == 1


def test_page(china):
    """maps.html: the maps that can be drawn, in the front page's markup for a list of pages."""
    s, out = china
    pg = maps.page(s, os.path.join(store.ROOT, "templates", "list.html"))
    assert "<h1>Maps</h1>" in pg and 'id="mapscss"' in pg
    assert ('<ol class="e lists"><li><a class="lk" href="china.html"><span class="ab">China</span><span class="tt">'
            in pg) and '<span class="r">1960–70</span></li></ol>' in pg
    assert "indochina.html" not in pg.split("<main", 1)[1].split("</main>", 1)[0]    # not ready on the fixture
    assert maps.listing(vnmap).startswith('<li><a class="lk" href="indochina.html"><span class="ab">Indochina</span>')
    front = open(os.path.join(TOOLS, "..", "templates", "series.html"), encoding="utf-8").read()
    for rule in maps.CSS.split("\n")[2:-1]:             # each rule is the front page's own, to the letter
        assert rule in front, rule


def test_top_bar():
    """The one mark 図 serves both maps: it leads to the page that lists them."""
    t = open(os.path.join(TOOLS, "..", "templates", "list.html"), encoding="utf-8").read()
    assert t.count("図") == 1 and '<a href="maps.html" title="Maps" aria-label="Maps" lang="ja">図</a>' in t


# ---------------------------------------------------------------- the client: one script, the span's fields

def test_client_span():
    """The client keeps no entry in the page and no year of its own: a span, the years' files, a thread."""
    js = open(os.path.join(TOOLS, "bib", "vnmap.js"), encoding="utf-8").read()
    for word in ("this.D.sp", "this.D.eu[y]", "this.D.th", "this.D.all", "this.D.here", "this.D.gz", "this.D.home",
                 "input[data-sp=\"from\"]", "addEventListener('input'", "addEventListener('change'"):
        assert word in js, word
    assert "setYear" not in js and "this.full" not in js and "this.D.e " not in js
    css = open(os.path.join(TOOLS, "bib", "vnmap.css"), encoding="utf-8").read()
    assert '.vnm-bar select,.vnm-bar input[type="text"]{' in css     # the fields in the select's look: no new rule


DATES = [  # (typed, the first field, the second field)
    ("1961-04-15", "1961-04-15", "1961-04-15"), ("1961-4-5", "1961-04-05", "1961-04-05"),
    ("1961-04", "1961-04-01", "1961-04-30"), ("1961", "1961-01-01", "1961-12-31"),
    ("Apr. 15, 1961", "1961-04-15", "1961-04-15"), ("apr 15 1961", "1961-04-15", "1961-04-15"),
    ("April 15, 1961", "1961-04-15", "1961-04-15"), ("Sept. 3, 1962", "1962-09-03", "1962-09-03"),
    ("15 Apr. 1961", "1961-04-15", "1961-04-15"), ("Mar. 1,1961", "1961-03-01", "1961-03-01"),
    ("Feb. 1964", "1964-02-01", "1964-02-29"), ("June 1961", "1961-06-01", "1961-06-30"),
    ("  1961-04-15 ", "1961-04-15", "1961-04-15"),
    # what does not read: half typed, a day the month lacks, figures that cannot be told apart, words
    ("", None, None), ("196", None, None), ("1961-", None, None), ("Apr.", None, None), ("Apr. 15", None, None),
    ("Apr. 15, 19", None, None), ("Feb. 30, 1961", None, None), ("1961-02-29", None, None), ("1961-13", None, None),
    ("June 31, 1961", None, None), ("4/15/1961", None, None), ("15/4/1961", None, None), ("Ma 1961", None, None),
    ("spring 1961", None, None), ("1961-00-10", None, None),
]


@pytest.mark.skipif(not shutil.which("node"), reason="node is not installed: the client's date reading is not run")
def test_read_date(tmp_path):
    """A field reads the calendar's form or a plain ISO date; a month or a year its first or last day; else nothing."""
    js = open(os.path.join(TOOLS, "bib", "vnmap.js"), encoding="utf-8").read()
    a, b, c = js.index("const MONTHS"), js.index("const FULLM"), js.index("let libP")
    code = js[a:js.index("\n", a) + 1] + js[b:c].replace("export ", "")
    code += ("\nconst rows = " + json.dumps([t for t, _, _ in DATES]) + ";\n"
             "console.log(JSON.stringify(rows.map((t) => [readDate(t, false), readDate(t, true)])));\n"
             "console.log(JSON.stringify([showDate('1961-04-05'), showSpan('1961-04-01', '1961-06-30'), "
             "showSpan('1960-01-06', '1976-08-31'), showSpan('1969-01-01', '1969-01-20'), "
             "showSpan('1962-09-03', '1962-09-03')]));\n")
    p = tmp_path / "dates.mjs"
    p.write_text(code, encoding="utf-8")
    out = subprocess.run(["node", str(p)], capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    got, shown = (json.loads(l) for l in out.stdout.strip().split("\n"))
    assert [(t, a, b) for (t, _, _), (a, b) in zip(DATES, got)] == DATES
    assert shown == ["Apr. 5, 1961", maps.span(D(1961, 4, 1), D(1961, 6, 30)), maps.span(D(1960, 1, 6), D(1976, 8, 31)),
                     maps.span(D(1969, 1, 1), D(1969, 1, 20)), maps.span(D(1962, 9, 3), D(1962, 9, 3))]


# ---------------------------------------------------------------- tools/cnmap/roc.py: the Republic of China's units

def test_roc_units():
    """Taiwan Province's sixteen counties, five provincial cities and one bureau; Fujian's two counties."""
    kinds = {}
    for name, zh, kind, prov, how in roc.UNITS.values():
        kinds[(prov, kind)] = kinds.get((prov, kind), 0) + 1
        assert prov in roc.PROVINCES and how
    assert kinds == {("taiwan", "county"): 16, ("taiwan", "provincial city"): 5,
                     ("taiwan", "administrative bureau"): 1, ("fujian-roc", "county"): 2}
    assert set(roc.WHOLE.values()) | {to for rules in roc.SPLIT.values() for _, to in rules} == set(roc.UNITS)


@pytest.mark.parametrize("county, town, want", [
    ("台北市", "中正區", "taipei-city"), ("台北市", "信義區", "taipei-city"),      # the city as it stood before July 1968
    ("台北市", "士林區", "yangmingshan"), ("台北市", "北投區", "yangmingshan"),
    ("台北市", "內湖區", "taipei"), ("台北市", "文山區", "taipei"), ("新北市", "板橋區", "taipei"),
    ("台北市", "新區", None),                                                    # a district the table does not know
    ("新竹市", "東區", "hsinchu"), ("新竹縣", "竹北市", "hsinchu"), ("嘉義市", "西區", "chiayi"),
    ("台中市", "西屯區", "taichung-city"), ("台中市", "豐原區", "taichung"),
    ("台中市", "梧棲鎮(海區", "taichung"),                                        # a harbour's waters: its district's
    ("台南市", "中西區", "tainan-city"), ("台南市", "永康區", "tainan"),
    ("高雄市", "前鎮區(海)", "kaohsiung-city"), ("高雄市", "小港區", "kaohsiung"), ("高雄市", "鳳山區", "kaohsiung"),
    ("金門縣", "金城鎮", "kinmen"), ("連江縣", "南竿鄉", "lienchiang"), ("澎湖縣", "馬公市", "penghu"),
    ("台東縣", "海端鄉", "taitung"),                                              # 海 in a name is no harbour mark
    ("福建省", "廈門市", None),
])
def test_roc_unit_of(county, town, want):
    assert roc.unit_of(county, town) == want


def test_roc_in_the_map_data():
    """The map's own files (the repository's, not the fixture's) hold the Republic's units as the table has them."""
    src = os.path.join(TOOLS, "..", "sources", "china")
    units = {u["id"]: u for u in json.load(open(os.path.join(src, "units.json"), encoding="utf-8"))["units"]}
    assert {k for k, u in units.items() if u["c"] == "roc"} == set(roc.PROVINCES)
    rows = [c for c in json.load(open(os.path.join(src, "counties.json"), encoding="utf-8"))["counties"] if c.get("c") == "roc"]
    assert {c["id"] for c in rows} == {f"{v[3]}-{k}" for k, v in roc.UNITS.items()}
    assert all(c["unit"] in roc.PROVINCES and c["made_of"] and not c["guess"] for c in rows)
    pl = {p["key"]: p for p in json.load(open(os.path.join(src, "places.json"), encoding="utf-8"))["places"]}
    assert (pl["taipei"]["unit"], pl["taipei"]["county"]) == ("taiwan", "taiwan-taipei-city")
