"""pages.py: the pages' budget, the splits it directs, and the links that follow them.

Written Nov. 19, 2026 with the pass (tests/README.md): each row pins what the function returned then.
"""
import pytest

from bib import pages


@pytest.fixture
def plan(monkeypatch):
    """A plan as pages.yaml would hold it: M in three ranges, works by letter, the Executive in two parts."""
    c = {"budget": 1000, "budgets": {"cal": 2000}, "fill": 0.5, "exempt": {"series.html": "the reader"},
         "names": {"m": [{"page": "names-ma-mb", "from": "m", "label": "Ma–Mb"},
                         {"page": "names-mc-mn", "from": "mc", "label": "Mc–Mn"},
                         {"page": "names-mo-mz", "from": "mo", "label": "Mo–Mz"}]},
         "works": {"by": "letter"},
         "executive": {"parts": [{"page": "executive-1953", "label": "One", "sections": ["t195301"]},
                                 {"page": "executive-1957", "label": "Two", "sections": ["t195701"]}]}}
    monkeypatch.setitem(pages._CONF, "c", c)
    yield c
    pages.reset()


FAMILY = [
    ("cal1961H1.html", "cal"), ("cal.html", "cal"), ("cal63.html", "cal"), ("calprimaries.html", "cal"),
    ("cal1967-04.html", "cal"), ("names-m.html", "names"), ("names-ma-mb.html", "names"), ("names.html", "names"),
    ("works-a.html", "works"), ("executive-1961.html", "executive"), ("congress.html", "congress"),
    ("kja.html", "kja"), ("series.html", "series"),
]


@pytest.mark.parametrize("name,fam", FAMILY)
def test_family(name, fam):
    assert pages.family(name) == fam


def test_budget(plan):
    assert pages.budget("cal1961H1.html") == 2000
    assert pages.budget("names-m.html") == 1000
    assert pages.exempt("series.html") == "the reader"


NAMES = [
    ("m", "macarthur-douglas", "names-ma-mb"), ("m", "mb-x", "names-ma-mb"), ("m", "mc-x", "names-mc-mn"), ("m", "mccarthy-eugene-j", "names-mc-mn"),
    ("m", "mnu", "names-mc-mn"), ("m", "mo", "names-mo-mz"), ("m", "muskie-edmund-s", "names-mo-mz"),
    ("k", "kennedy-john-f", "names-k"),
]


@pytest.mark.parametrize("letter,key,page", NAMES)
def test_names_page(plan, letter, key, page):
    assert pages.names_page(letter, key) == page
    assert pages.names_href(letter, key) == f"{page}.html#{key}"


def test_names_unsplit():
    pages.reset()
    assert pages.names_href("m", "muskie-edmund-s") == "names-m.html#muskie-edmund-s"


def test_names_ranges():
    sizes = [("mao-zedong", 40), ("macarthur-douglas", 40), ("mccarthy-eugene-j", 40), ("mcnamara-robert-s", 40),
             ("muskie-edmund-s", 40), ("morse-wayne", 40)]
    got = pages.names_ranges("m", sizes, 90)
    assert got == [{"page": "names-ma", "from": "m", "label": "Ma"},
                   {"page": "names-mc", "from": "mc", "label": "Mc"},
                   {"page": "names-mo-mz", "from": "mo", "label": "Mo–Mz"}]
    assert pages.names_ranges("m", sizes, 1000) is None        # under the target: no split


def test_pack():
    assert pages.pack([("a", 3), ("b", 3), ("c", 5), ("d", 1)], 6) == [["a", "b"], ["c", "d"]]
    assert pages.pack([("a", 9), ("b", 1)], 6) == [["a"], ["b"]]


def test_sections_parts():
    secs = [("t195301", "Eisenhower, first term", 5), ("t195701", "Eisenhower, second term", 5),
            ("c87", "87th", 2), ("c88", "88th", 2)]
    got = pages.sections_parts("executive", secs, 6)
    assert [p["page"] for p in got] == ["executive-1953", "executive-1957", "executive-87-88"]
    assert got[2]["label"] == "87th–88th"


def test_compress():
    amap = {"ex195301-state": "executive-1953", "ex195301-war": "executive-1953", "t195301": "executive-1953",
            "sources": "executive-1957", "src-x": "executive-1953", "src-y": "executive-1957"}
    c = pages.compress(amap)
    assert c["t"] == {"ex195301": "executive-1953", "t195301": "executive-1953", "sources": "executive-1957"}
    assert c["x"] == {"src-x": "executive-1953", "src-y": "executive-1957"}


PAGE = ('<html><head><title>Exec</title></head><body><header><div id="crumb"><b>Exec</b></div></header>'
        '<main id="doc"><h1>Exec</h1><p><a href="#sources">sources</a></p>'
        '<h2 id="t195301">One</h2><p id="ex195301-state">S</p><a href="#ex195701-state">later</a>'
        '<h2 id="t195701">Two</h2><p id="ex195701-state">S</p><p id="sources">x</p></main></body></html>')


def test_cut(plan):
    out = pages.cut("executive", PAGE, "Exec")
    assert sorted(out) == ["executive-1953.html", "executive-1957.html", "executive.html"]
    one = out["executive-1953.html"]
    assert "<title>Exec: One</title>" in one and '<div id="crumb"><b>Exec: One</b>' in one
    assert 'href="executive-1957.html#ex195701-state"' in one          # another part's anchor
    assert 'href="executive-1957.html#sources"' in one                 # from the intro, to its part
    assert 'id="ex195701-state"' not in one
    assert pages.MAPS["executive"]["ex195701-state"] == "executive-1957"
    idx = out["executive.html"]
    assert 'href="executive-1953.html#t195301"' in idx and "location.replace" in idx


def test_route(plan):
    pages.cut("executive", PAGE, "Exec")
    pages.WORKS.update({"w.beschloss-crisis-years": "works-b"})
    html = ('<a href="executive.html#ex195701-state">x</a><a href="names-m.html#mccarthy-eugene-j">y</a>'
            '<a href="works.html#w.beschloss-crisis-years">z</a><a href="cal.html#x">c</a>'
            '<a href="https://example.org/works.html#w.beschloss-crisis-years">e</a>')
    got = pages.route(html)
    assert 'href="executive-1957.html#ex195701-state"' in got
    assert 'href="names-mc-mn.html#mccarthy-eugene-j"' in got
    assert 'href="works-b.html#w.beschloss-crisis-years"' in got
    assert 'href="cal.html#x"' in got
    assert 'href="https://example.org/works-b.html#w.beschloss-crisis-years"' in got   # a base url kept (lives.SITE)


def test_route_inactive():
    pages.reset()
    html = '<a href="names-m.html#mccarthy-eugene-j">y</a>'
    assert pages.route(html) == html


def test_part_fields():
    base = {"from": "1967-01-01", "page": "cal1967H1", "title": "Calendar, January–June 1967: the 90th Congress's first session"}
    f, span = pages._part_fields(base, "Q", ["1967-01", "1967-02", "1967-03"], "1967-01-01")
    assert f == {"from": "1967-01-01", "page": "cal1967Q1", "abbr": "Cal. Jan.–Mar. 1967",
                 "called": "the calendar of January–March 1967",
                 "title": "Calendar, January–March 1967: the 90th Congress's first session",
                 "span": "Jan. 1–Mar. 31, 1967", "page_title": "Calendar, January–March 1967",
                 "h1": "1967, January–March", "lede": "Executive, legislative, judicial, and state events of January–March 1967."}
    assert span == ("1967-01-01", "1967-03-31")
    f, span = pages._part_fields(base, "M", ["1967-04"])
    assert (f["page"], f["abbr"], f["span"], f["h1"]) == ("cal1967-04", "Cal. Apr. 1967", "Apr. 1–30, 1967", "1967, April")


BY_RULE = [
    ("cal1964-01.thread.cuba", "cal1964-01"),      # a month's page, its name whole (not cal1964)
    ("th-cal1964-01", "cal1964-01"),
    ("cal1964Q1.thread.cuba", "cal1964Q1"),
    ("cal1964.thread.cuba", "cal1964"),
    ("ind-cal1964-cpi", "cal1964"),
]


@pytest.mark.parametrize("anchor,page", BY_RULE)
def test_by_rule_month_page_whole(monkeypatch, anchor, page):
    """calsplit.by_rule: a part's page named in an anchor, a month's with its hyphen."""
    from bib import calsplit

    class L:
        key = "cal"
    monkeypatch.setattr(calsplit, "parts", lambda lst: [{"page": p} for p in
                                                         ("cal", "cal1964", "cal1964Q1", "cal1964-01")])
    monkeypatch.setattr(calsplit, "years", lambda lst: {})
    assert calsplit.by_rule(L, anchor) == page


def test_index_anchor_of_a_piece():
    """The index links a piece of a section cut by its "continued" heading's id, which its page holds."""
    assert pages._anchor("t196101") == "t196101"
    assert pages._anchor("t196101/t196101-departments") == "pgc-t196101-departments"
