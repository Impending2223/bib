"""placepages.py: which entries a place's page holds (a nation's: those that took place there and those that concern it
by the register, each marked which; a State's, a province's, a city's: those that took place there and those that
carry its tag), which places have a page, and the page laid out as a thread's (its anchors, its rubric's mark, its
parts by the budget). On the fixture: the calendar's April and August 1961, with a small register and map of China of
the test's own where the fixture has none."""
import datetime
import os
import re

import pytest

from bib import build, chron, cnmap, pages, places, placepages as pp, store, threads, vis

LI = re.compile(r'<li (?:class="[^"]*" )?id="t-([^"]+)"')

REGISTER = {
    "polities": {"us": {"name": "United States"}, "prc": {"name": "China (the People's Republic)"},
                 "laos": {"name": "Laos"}, "pathet-lao": {"name": "Pathet Lao"},
                 "drv": {"name": "Democratic Republic of Vietnam"}, "nlf": {"name": "NLF", "folded": "drv"},
                 "congo-brazzaville": {"name": "Congo (Brazzaville)"}, "un": {"name": "United Nations", "org": True}},
    "names": {"souvanna-phouma": {"polity": "laos"}, "souphanouvong": {"polity": "pathet-lao"},
              "thant-u": {"polity": "un"}},
    "places": {"state:*": ["us"], "city:*": ["us"]},
    "threads": {"laos": ["laos", "us", "drv"]},
}
UNITS = {"shaanxi": {"id": "shaanxi", "name": "Shaanxi", "c": "prc"},
         "fujian-roc": {"id": "fujian-roc", "name": "Fujian (Republic of China)", "c": "roc"}}
CN = {"peking": {"key": "peking", "lat": 39.9, "lon": 116.4, "unit": "peking"},
      "xian": {"key": "xian", "lat": 34.3, "lon": 108.9, "unit": "shaanxi"},
      "shaanxi": {"key": "shaanxi", "area": True, "unit": "shaanxi"}}


@pytest.fixture
def register(monkeypatch):
    monkeypatch.setattr(vis, "polities", lambda: REGISTER)
    monkeypatch.setattr(cnmap, "units", lambda: UNITS)
    monkeypatch.setattr(cnmap, "gazetteer", lambda: CN)
    pp.reset()
    yield
    pp.reset()


@pytest.fixture(scope="module")
def series():
    return store.Series()


@pytest.fixture(scope="module")
def cal(series):
    return series.lists["cal"]


def E(**kw):
    e = {"id": "cal.1961-04-01.x", "when": "Apr. 1", "date": "1961-04-01", "thread": "none", "c": "A."}
    e.update(kw)
    return e


def W(series, cal, e):
    return pp.where(series, cal, e)


# ---------------------------------------------------------------- which entries (STYLE 2)

def test_nation_there_by_place(series, cal, register):
    w = W(series, cal, E(place="peking"))
    assert w["there"]["nation"] == {"prc"} and w["there"]["city"] == {"peking"}
    w = W(series, cal, E(place="washington"))              # a U.S. place (`st`): the United States's
    assert w["there"]["nation"] == {"us"} and w["there"]["state"] == set()        # DC is no State


def test_nation_about_by_people_tags_and_thread(series, cal, register):
    w = W(series, cal, E(tags=["name:souvanna-phouma"]))
    assert w["tagged"]["nation"] == {"laos"} and w["there"]["nation"] == set()
    w = W(series, cal, E(tags=["polity:congo-brazzaville"]))
    assert w["tagged"]["nation"] == {"congo-brazzaville"}
    w = W(series, cal, E(thread="laos"))                     # no tag that names a nation: the thread's (vis.address)
    assert w["tagged"]["nation"] == {"laos", "us", "drv"}
    w = W(series, cal, E(thread="laos", tags=["name:souvanna-phouma"]))   # the tags first, as the register's address
    assert w["tagged"]["nation"] == {"laos"}
    w = W(series, cal, E(tags=["name:thant-u"]))             # an organization is no nation
    assert w["tagged"]["nation"] == set()


def test_folded_polities(series, cal, register):
    assert W(series, cal, E(tags=["polity:nlf"]))["tagged"]["nation"] == {"drv", "rvn"}   # both Vietnams (the owner, Nov. 26, 2026)
    assert W(series, cal, E(tags=["name:souphanouvong"]))["tagged"]["nation"] == {"laos"}
    assert set(pp.nations()) == {"us", "prc", "laos", "drv", "congo-brazzaville"}
    assert pp.nations()["prc"] == "China" and pp.nations()["congo-brazzaville"] == "Congo (Brazzaville)"


def test_state_by_place_and_tags(series, cal):
    S = pp.states()
    al = next(c for c, r in S.items() if r["key"] == "alabama")
    assert W(series, cal, E(place="birmingham"))["there"]["state"] == {al}
    for tags in (["state:al"], ["state:alabama"], ["city:birmingham"]):   # its code, its key, a city in it
        w = W(series, cal, E(tags=tags))
        assert w["tagged"]["state"] == {al} and w["there"]["state"] == set(), tags


def test_province_by_place(series, cal, register):
    assert W(series, cal, E(place="xian"))["there"]["province"] == {"shaanxi"}
    assert W(series, cal, E(place="peking"))["there"]["province"] == set()       # no unit of the PRC in this map
    assert set(pp.provinces()) == {"shaanxi"}                                     # the Republic of China's are not


def test_city_by_place_alias_and_tag(series, cal):
    assert W(series, cal, E(place="new-york"))["there"]["city"] == {"nyc"}      # an alias: its row's key
    assert W(series, cal, E(tags=["city:new-york"]))["tagged"]["city"] == {"nyc"}
    assert W(series, cal, E(place="alabama"))["there"]["city"] == set()          # a State as a place is no city


# ---------------------------------------------------------------- which places (STYLE 1)

def brute(cal, test):
    return [e["id"] for e in chron.sort(cal, [e for _, e in cal.entries() if "when" in e and test(e)])]


def test_gather_states_and_cities(series, cal):
    pp.reset()
    got = pp.gather(series)
    ny = got[("state", "NY")]
    assert ny["page"] == "places-new-york-state" and ny["name"] == "New York"

    def in_ny(e):
        w = pp.where(series, cal, e)
        return "NY" in w["there"]["state"] | w["tagged"]["state"]
    assert [e["id"] for e in ny["ents"]] == brute(cal, in_ny)
    assert ny["there"] < {e["id"] for e in ny["ents"]}             # some by their tags alone
    cities = [v for v in got.values() if v["kind"] == "city"]
    assert cities and all(len(v["ents"]) >= pp.CITY_MIN for v in cities)
    assert len({v["page"] for v in got.values()}) == len(got)       # no two places one page


def test_gather_nations_with_register(series, cal, register):
    got = pp.gather(series)
    us = got[("nation", "us")]
    placed = brute(cal, lambda e: any((places.get(k) or {}).get("st") or (places.get(k) or {}).get("in") == "us"
                                      for k in places.keys(e)))       # a State's place, or one `in: us` (Puerto Rico)
    assert set(placed) <= {e["id"] for e in us["ents"]} and us["there"] == set(placed)
    assert ("city", "peking") in got and ("nation", "prc") in got


# ---------------------------------------------------------------- the page (STYLE 3, 4, 5)

@pytest.fixture
def template():
    return os.path.join(build.TEMPLATES, "list.html")


def test_page_is_a_threads_page(series, cal, register, template):
    pages.reset()
    got = dict(pp.pages_(series, build.Linker(series), template, only={"us", "new-york-state"}, save=False))
    page = got["places-us.html"]
    us = pp.gather(series)[("nation", "us")]
    assert LI.findall(page) == [e["id"] for e in us["ents"]]
    assert "<title>Places: United States</title>" in page and "<h1>United States</h1>" in page
    for e in us["ents"][:20]:                                       # each line marked which (STYLE 2)
        li = page[page.index(f'id="t-{e["id"]}"'):]
        rub = re.search(r'<span class="s rub">(.*?) · ', li).group(1)
        assert rub == ("In the United States" if e["id"] in us["there"] else "About the United States")
    own = set(re.findall(r'\sid="([^"]+)"', page))
    assert not own & {x["id"] for _, x in cal.entries()}            # no calendar id repeated (threads STYLE 3)
    assert 'id="t-d1961-04-' in page and '<h2 id="t-y1961"' in page
    ny = got["places-new-york-state.html"]
    assert '<span class="s rub">In ' not in ny and '<span class="s rub">About ' not in ny     # a State: no mark
    assert "those that took place in New York and those that carry its tag" in ny


def test_split_by_budget(series, cal, template, monkeypatch):
    """A page over budget is in parts by date, planned from its own entries' sizes; its own page the index."""
    pages.reset()
    pp.reset()
    c = dict(pages.conf(), budget=300_000, budgets={})
    monkeypatch.setitem(pages._CONF, "c", c)
    monkeypatch.setattr(pages, "planned", lambda fam: {})
    got = dict(pp.pages_(series, build.Linker(series), template, only={"washington"}, save=False))
    pl = pp.gather(series)[("city", "washington")]
    ps = pl["planned"]
    assert len(ps) > 1 and all(p["page"].startswith("places-washington-1961") for p in ps)
    idx = got["places-washington.html"]
    assert '<ul class="pgl">' in idx and all(f'href="{p["page"]}.html"' in idx for p in ps)
    held = []
    for i, p in enumerate(ps):
        part = got[f"{p['page']}.html"]
        assert 'class="pgparts"' in part and 'class="pgseam"' in part
        held += LI.findall(part)
        month = re.match(r"^[A-Z][a-z]+\.? \d{4}$", p["label"])     # a month is the least part (threads STYLE 6)
        assert len(part.encode()) <= 300_000 or month
    assert held == [e["id"] for e in pl["ents"]]
    sec = "\n".join(pp.index_section(series))
    assert all(f'href="{p["page"]}.html"' in sec for p in ps)
    pp.reset()


def test_index_section(series, cal, template):
    pp.reset()
    page = threads.index_page(series, template, cal)
    assert '<h2 id="places"' in page and '<h3 id="places-state"' in page and '<h3 id="places-city"' in page
    for pl in pp.gather(series).values():
        assert f'<a href="{pl["page"]}.html">' in page


def test_pages_plan_family():
    assert pages.family("places-laos.html") == "places" and pages.family("places-laos-1962.html") == "places"
    assert {"places-laos", "places-laos-1962"} <= pages.live_pages({"places": {"laos": [
        {"page": "places-laos-1962", "from": "1962", "label": "1962"}]}})
    ps = threads.plan_parts("laos", [(datetime.date(1961, 1, 1), 10), (datetime.date(1962, 1, 1), 10)], 10,
                            page="places-laos")
    assert [p["page"] for p in ps] == ["places-laos-1961", "places-laos-1962"]


# ---------------------------------------------------------------- the dateline and "Places:" (STYLE 6, 7)

def test_places_line(series, cal, register):
    pp.gather(series)
    ent = next(e for _, e in cal.entries() if "when" in e and e.get("place") == "peking")
    got = pp.line(ent, series)
    assert got.startswith('Places: <a href="places-prc.html">China</a>')
    assert '<a href="places-peking.html">Peking</a>' in got and got.endswith(".")
    assert pp.line(E(id="cal.nowhere"), series) == ""             # an entry it does not know: none
    assert pp.line(ent, None) == "" or pp.line(ent, None) == got   # no series, no build: none (or the build's)


def test_places_line_new_york_state(series, cal, monkeypatch):
    """A State named as a city of the same line is: "New York State", beside the city's "New York"."""
    pp.reset()
    monkeypatch.setattr(pp, "CITY_MIN", 1)
    assert ("city", "nyc") in pp.gather(series)
    ent = next(e for _, e in cal.entries() if "when" in e and e.get("place") in ("nyc", "new-york"))
    got = pp.line(ent, series)
    assert '<a href="places-new-york-state.html">New York State</a>' in got
    assert '<a href="places-nyc.html">New York</a>' in got
    pp.reset()


def test_into_note():
    assert pp.into_note("A, 3. Names: <a>X</a>.", "Places: P.") == "A, 3. Places: P. Names: <a>X</a>."
    assert pp.into_note("A, 3.", "Places: P.") == "A, 3. Places: P."
    assert pp.into_note("", "Places: P.") == "Places: P."
    assert pp.into_note("A.", "") == "A."


def test_dateline_links_its_place(series, monkeypatch):
    from bib import daybook, dateline
    pp.reset()
    monkeypatch.setattr(daybook, "SERIES", series)
    timed = {"id": "x", "when": "Apr. 17", "date": "1961-04-17", "time": "1961-04-17T15:30Z"}
    h = dateline.html_(dict(timed, place="washington"))
    assert '<a href="places-washington.html">Washington</a> · 10:30 a.m.' in h
    h = dateline.html_(dict(timed, time_zone="America/New_York"))  # the clock's city: no place of record, no link
    assert "<a " not in h and "Washington · 10:30 a.m." in h
    h = dateline.html_(dict(timed, place="selma"))                 # a place with no page of its own
    assert "<a " not in h
    assert "closest('.dl a')" in dateline.SCRIPT                   # a tap follows the link
    pp.reset()


def test_a_line_that_names_a_province_is_about_it(register, monkeypatch):
    """The owner, Nov. 27, 2026: the Chinese provinces the entries name had no "Places:" link. A line that names a
    province, in Pinyin or in characters, puts the entry on its page; Peking and Shanghai go by place only."""
    units = dict(UNITS, hebei={"id": "hebei", "name": "Hebei", "c": "prc", "made_of": ["河北省"]},
                 shanxi={"id": "shanxi", "name": "Shanxi", "c": "prc", "made_of": ["山西省"]},
                 peking={"id": "peking", "name": "Peking", "c": "prc", "made_of": ["北京市"]})
    monkeypatch.setattr(cnmap, "units", lambda: units)
    assert pp.named_provinces("Mao in Hebei inspects the communes") == {"hebei"}
    assert pp.named_provinces("the 河北 committee") == {"hebei"}
    assert pp.named_provinces("Shaanxi and Shanxi") == {"shaanxi", "shanxi"}
    assert pp.named_provinces("the Peking meeting") == set()
    assert pp.named_provinces("Hebeian troops") == set()
