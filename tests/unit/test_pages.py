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


# ---------------------------------------------------------------- the audit of Nov. 19 (each fix pinned)

def conf_(monkeypatch, c):
    pages.reset()
    monkeypatch.setitem(pages._CONF, "c", c)


ONE = [{"page": "names-ja-johnsonlynda", "from": "j", "label": "Ja–Johnson, Lynda"},
       {"page": "names-johnsonlyndonb", "from": "johnson-lyndon-b", "only": "johnson-lyndon-b",
        "label": "Johnson, Lyndon B."},
       {"page": "names-johnsonm-jz", "from": "johnson-m", "label": "Johnson, M–Jz"}]


@pytest.mark.parametrize("key,page", [
    ("johnson-lyndon-b", "names-johnsonlyndonb"),
    ("johnson-lyndon-a", "names-ja-johnsonlynda"),          # a later person just before him: the page before
    ("johnson-lyndon-c", "names-johnsonm-jz"),              # just after him: the page after, not his
    ("johnson-lyndon-b-jr", "names-johnsonm-jz"),           # his key's extension is another person
    ("johnson-matthew", "names-johnsonm-jz"),
])
def test_one_person_page_holds_him_alone(monkeypatch, key, page):
    conf_(monkeypatch, {"names": {"j": ONE}})
    assert pages.names_page("j", key) == page
    pages.reset()


def test_names_ranges_one_person_bounded():
    sizes = [("ja-x", 40), ("ja-y", 40), ("johnson-lyndon-b", 500), ("johnson-m", 40), ("jz", 40)]
    got = pages.names_ranges("j", sizes, 90, {"johnson-lyndon-b": "Johnson, Lyndon B."})
    mid = got[1]
    assert mid["label"] == "Johnson, Lyndon B." and mid["from"] == mid["only"] == "johnson-lyndon-b"
    assert "only" not in got[0] and "only" not in got[-1]


def test_names_stub_one_person(monkeypatch):
    conf_(monkeypatch, {"names": {"j": ONE}})
    s = pages.names_stub("j", {})
    assert '["johnson-lyndon-b","names-johnsonlyndonb","johnson-lyndon-b"]' in s
    assert "<noscript>" in s
    pages.reset()


def lv(key, n):
    return f'<section class="lv" id="{key}"><h2 class="lvh">{key}</h2>' + "x" * n + "</section>"


def names_built(tmp_path, page, keys):
    body = "".join(lv(k, n) for k, n in keys)
    (tmp_path / f"{page}.html").write_text(f'<html><body><main id="doc">{body}</main></body></html>', encoding="utf-8")


def test_replan_names_keeps_ranges_within_budget(monkeypatch, tmp_path):
    """A letter in ranges planned again: a range within budget kept as it is; only the one over re-cut, its pieces
    beginning and ending where it did."""
    c = {"budget": 3000, "fill": 1.0, "names": {"m": [
        {"page": "names-ma-mb", "from": "m", "label": "Ma–Mb"},
        {"page": "names-mc-mn", "from": "mc", "label": "Mc–Mn"},
        {"page": "names-mo-mz", "from": "mo", "label": "Mo–Mz"}]}}
    conf_(monkeypatch, c)
    names_built(tmp_path, "names-ma-mb", [("macarthur-douglas", 1000)])
    names_built(tmp_path, "names-mc-mn", [("mccarthy-eugene-j", 1500), ("mcnamara-robert-s", 1500),
                                          ("mills-wilbur", 1500)])
    names_built(tmp_path, "names-mo-mz", [("morse-wayne", 1000)])
    rows = pages.measure(str(tmp_path))
    got = pages.propose(str(tmp_path), rows)["names"]["m"]
    assert got[0] == c["names"]["m"][0] and got[-1] == c["names"]["m"][-1]
    mid = got[1:-1]
    assert len(mid) >= 2 and mid[0]["from"] == "mc"
    assert mid[0]["label"].startswith("Mc–") and mid[-1]["label"].endswith("–Mn")
    assert mid[0]["page"].startswith("names-mc-") and mid[-1]["page"].endswith("-mn")
    pages.reset()


EXEC_PIECE = ('<html><head><title>Exec</title></head><body><main id="doc"><h1>E</h1>'
              '<h2 class="pgcont" id="pgc-t196501-departments" data-of="t196501" '
              'data-short="Jan. 20, 1965, Departments">Jan. 20, 1965, continued</h2>'
              '<h3 id="t196501-departments" data-short="Departments">Departments</h3>' + "d" * 800 +
              '<h3 id="t196501-state" data-short="State">State</h3>' + "s" * 800 + '</main></body></html>')
EXEC_HEAD = ('<html><head><title>Exec</title></head><body><main id="doc"><h1>E</h1>'
             '<h2 id="t196501" data-short="Jan. 20, 1965">Jan. 20, 1965</h2><p id="ex-head">h</p></main></body></html>')
EXEC_FULL = ('<html><head><title>Exec</title></head><body><header><div id="crumb"><b>Exec</b></div></header>'
             '<main id="doc"><h1>E</h1><h2 id="t196501" data-short="Jan. 20, 1965">Jan. 20, 1965</h2><p id="ex-head">h</p>'
             '<h3 id="t196501-departments" data-short="Departments">Departments</h3>' + "d" * 800 +
             '<h3 id="t196501-state" data-short="State">State</h3>' + "s" * 800 + '</main></body></html>')


def test_replan_a_continued_piece_alone(monkeypatch, tmp_path):
    """executive-1965-departments, a piece of a term, over budget, planned again alone: its pieces by the h2/h3 ids
    cut() knows, and cut() makes them."""
    c = {"budget": 1500, "fill": 1.0, "executive": {"parts": [
        {"page": "executive-1965", "label": "Jan. 20, 1965", "sections": ["t196501"]},
        {"page": "executive-1965-departments", "label": "Jan. 20, 1965, Departments",
         "sections": ["t196501/t196501-departments"]}]}}
    conf_(monkeypatch, c)
    (tmp_path / "executive-1965.html").write_text(EXEC_HEAD, encoding="utf-8")
    (tmp_path / "executive-1965-departments.html").write_text(EXEC_PIECE, encoding="utf-8")
    rows = pages.measure(str(tmp_path))
    assert [r["page"] for r in rows if r["over"]] == ["executive-1965-departments.html"]
    parts = pages.propose(str(tmp_path), rows)["executive"]["parts"]
    assert parts[0] == c["executive"]["parts"][0]                          # kept as it was
    secs = [s for p in parts[1:] for s in p["sections"]]
    assert secs == ["t196501/t196501-departments", "t196501/t196501-state"]
    assert len({p["page"] for p in parts}) == len(parts)
    conf_(monkeypatch, {"executive": {"parts": parts}})
    out = pages.cut("executive", EXEC_FULL, "Exec")
    holds = {pages.MAPS["executive"][a] for a in ("t196501-departments", "t196501-state")}
    assert len(holds) == 2 and all(f"{h}.html" in out for h in holds)
    assert 'id="ex-head"' in out[f"{parts[0]['page']}.html"]
    pages.reset()


def test_retired_never_a_live_page(monkeypatch):
    c = {"names": {"m": [{"page": "names-ma-mb", "from": "m", "label": "Ma–Mb"}]},
         "executive": {"parts": [{"page": "executive-1965", "label": "x", "sections": ["t196501"]}]},
         "works": {"by": "letter"}}
    live = pages.live_pages(c)
    assert {"names-ma-mb", "executive-1965", "works-a", "executive"} <= live
    assert "names-mc-mn" not in live


def test_one_person_page_warned(monkeypatch):
    """./bib pages warns where a page of one person holds another, or a range labelled for one person is unbounded."""
    conf_(monkeypatch, {"names": {"j": ONE[:1] + [dict(ONE[1], only=None)] + ONE[2:]}})
    rows = [{"page": "names-johnsonlyndonb.html", "bytes": 10, "units": 2, "unit": "persons", "budget": 5,
             "over": True, "alone": False, "exempt": None, "stub": False, "family": "names"}]
    text = pages.report(rows)
    assert "warn" in text and "names-johnsonlyndonb" in text
    pages.reset()
