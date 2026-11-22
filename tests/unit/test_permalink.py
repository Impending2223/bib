"""permalink.py: e.json's map (an alias, a split page, an entry moved off its month's page) and the mark's place (outside
the claims' spans and the footnote marks). On the fixture: the calendar in two halves, cal1961H1 and cal1961H2."""
from html.parser import HTMLParser

import pytest

from bib import build, calsplit, permalink, store


@pytest.fixture(scope="module")
def series():
    return store.Series()


@pytest.fixture
def cal(series):
    return series.lists["cal"]


def test_map_alias_and_split(cal):
    D = permalink.emap(cal, permalink.homes(cal))
    assert D["m"] == {"1961-04": "cal1961H1", "1961-08": "cal1961H2"}
    # an entry on each half's page, by its month
    assert permalink.resolve(D, "cal.1961-04-17.cuba") == ("cal1961H1", "cal.1961-04-17.cuba")
    assert permalink.resolve(D, "cal.1961-04.africa") == ("cal1961H1", "cal.1961-04.africa")
    # a combined entry's DROP id: to its KEEP's anchor, on its page
    assert D["a"]["cal.1961-08-30.school-aid-2"] == "cal.1961-08-30.cuba-bay-of-pigs"
    assert permalink.resolve(D, "cal.1961-08-30.school-aid-2") == ("cal1961H2", "cal.1961-08-30.cuba-bay-of-pigs")
    assert permalink.resolve(D, "cal.1961-04-20.vietnam") == ("cal1961H1", "cal.1961-04-20.cuba-2")
    # not an entry: none
    for bad in ("cal.1961-04-17.nonesuch", "cal.1961-05-01.cuba", "cal.thread.cuba", "junk", ""):
        assert permalink.resolve(D, bad) is None
    # every entry a page holds resolves to that page
    home = permalink.homes(cal)
    assert home and all(permalink.resolve(D, i) == (p, i) for i, p in home.items() if not i.startswith("cal.thread."))


def test_map_moved_entry(cal):
    """An entry whose page is not its month's (a loose entry shown elsewhere, a later split): listed in x."""
    home = permalink.homes(cal)
    eid = "cal.1961-08-30.cuba-bay-of-pigs"
    home[eid] = "cal1961H1"
    D = permalink.emap(cal, home)
    assert D["x"] == {eid: "cal1961H1"}
    assert permalink.resolve(D, eid) == ("cal1961H1", eid)
    assert permalink.resolve(D, "cal.1961-08-30.school-aid-2") == ("cal1961H1", eid)


def test_map_unsplit(cal, monkeypatch):
    monkeypatch.setattr(calsplit, "cfg", lambda lst: None)
    D = permalink.emap(cal, permalink.homes(cal))
    assert D["d"] == "cal" and D["x"] == {}
    assert permalink.resolve(D, "cal.1961-08-30.school-aid-2") == ("cal", "cal.1961-08-30.cuba-bay-of-pigs")


class Marks(HTMLParser):
    """Each a.pl: its entry's id and its ancestors' (tag, class)."""
    VOID = {"br", "img", "hr", "meta", "link", "input", "wbr", "source", "col"}

    def __init__(self):
        super().__init__()
        self.stack, self.found = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("class") == "pl":
            li = next((x for x in reversed(self.stack) if x[0] == "li"), None)
            self.found.append((li and li[2], a.get("href"), list(self.stack)))
        if tag not in self.VOID:
            self.stack.append((tag, a.get("class") or "", a.get("id")))

    def handle_endtag(self, tag):
        for k in range(len(self.stack) - 1, -1, -1):
            if self.stack[k][0] == tag:
                del self.stack[k:]
                return


@pytest.mark.parametrize("place", ["corner", "inline"])
def test_mark_outside_claims(series, cal, place, monkeypatch):
    monkeypatch.setattr(permalink, "PERMALINK_PLACE", place)
    calsplit.CUR.update(half=1, mode="list")
    try:
        page = build.build_list(series, "cal", build.Linker(series), 1)
    finally:
        calsplit.CUR.update(half=None)
    p = Marks()
    p.feed(page)
    assert len(p.found) > 20
    assert 'data-cl="1"' in page and 'class="fm"' in page          # the page has claims' spans and footnote marks
    for eid, href, stack in p.found:
        assert href == f"e.html#{eid}"
        classes = [(t, c.split()) for t, c, _ in stack]
        assert not any("cl" in c for _, c in classes)                  # not in a claim's span
        assert not any(t == "sup" for t, _ in classes)                 # nor a footnote's mark
        assert not any(t in ("ol",) and "fn" in c for t, c in classes)   # nor the footnotes
        parent = stack[-1]
        if place == "corner":
            assert parent[0] == "li"                                    # the box's own child
        else:
            assert parent[0] in ("span", "li") and (parent[0] == "li" or parent[1] == "c")
    ids = [eid for eid, _, _ in p.found]
    assert len(ids) == len(set(ids))                                    # one mark an entry
    assert not any(i.startswith("cal.thread.") for i in ids)            # not on a thread's statement


def test_inline_after_text(monkeypatch):
    monkeypatch.setattr(permalink, "PERMALINK_PLACE", "inline")
    monkeypatch.setattr(permalink, "PERMALINK_GAP", "\u2002")
    got = permalink.in_text('<span class="cl" data-u="a">A met B.</span>', "cal.1961-04-17.cuba")
    assert got == ('<span class="cl" data-u="a">A met B.</span>\u2002'
                   '<a href="e.html#cal.1961-04-17.cuba" class="pl" title="Permalink">\u25a1</a>')
    assert permalink.in_box("x", inlined=True) == ""
    monkeypatch.setattr(permalink, "PERMALINK_PLACE", "corner")
    assert permalink.in_text("A.", "x") == "A."
    assert permalink.in_box("x") == '<a href="e.html#x" class="pl" title="Permalink">\u25a1</a>'
