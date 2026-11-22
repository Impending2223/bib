"""threads.py: a thread's page (its entries, the thread's own and its `also:` ones, in the chronological sort; a
subentry after its parent; each as the calendar renders it, footnotes and marks; anchors never the calendar's), the
parts the budget plans (by year, quarter, month), and the footnotes on a Names entry (lives.calendar_sentences). On the
fixture: the calendar's April and August 1961."""
import datetime
import os
import re

import pytest

from bib import build, chron, footnotes, lives, pages, permalink, store, threads

LI = re.compile(r'<li (?:class="[^"]*" )?id="t-([^"]+)"')


@pytest.fixture(scope="module")
def series():
    return store.Series()


@pytest.fixture(scope="module")
def cal(series):
    return series.lists["cal"]


@pytest.fixture(scope="module")
def built(series):
    pages.reset()
    linker = build.Linker(series)
    tpl = os.path.join(build.TEMPLATES, "list.html")
    return dict(threads.pages_(series, linker, tpl, only={"republican-party", "soviet-union-leadership",
                                                          "cuba-bay-of-pigs"}))


def ids(page):
    return LI.findall(page)


def test_members_own_and_also_in_order(series, cal, built):
    """Every entry whose thread is the thread or whose also: names it, in chron.sort's order."""
    page = built["threads-republican-party.html"]
    want = [e["id"] for e in chron.sort(cal, [e for _, e in cal.entries() if "when" in e and (
        e.get("thread") == "republican-party" or "republican-party" in (e.get("also") or []))])]
    assert ids(page) == want
    also = series.get("cal.1961-04.cuba")[2]
    assert also["thread"] == "cuba" and "republican-party" in also["also"]
    assert "cal.1961-04.cuba" in ids(page)
    assert f"{len(want)} entries, in the calendar" in page


def test_subentry_after_parent(cal, built):
    page = built["threads-soviet-union-leadership.html"]
    got = ids(page)
    kids = ["cal.1961-04-06.soviet-union", "cal.1961-04-06.soviet-union-2"]
    for k in kids:
        e = next(x for _, x in cal.entries() if x["id"] == k)
        assert e.get("part_of") in got and got.index(e["part_of"]) < got.index(k)
        assert f'<li class="sub" id="t-{k}"' in page
    assert got.index(kids[1]) == got.index(kids[0]) + 1


def test_rendered_as_calendar(series, cal, built):
    """The calendar's renderer: the footnotes and their marks as the calendar's, the □ to e.html#ID, the rubric; no
    calendar id repeated; a bare link the page does not hold goes to the calendar."""
    page = built["threads-cuba-bay-of-pigs.html"]
    eid = "cal.1961-04.cuba-bay-of-pigs-4"
    e = series.get(eid)[2]
    fns = footnotes.build(series, e)
    assert fns and len(fns[1]) > 1
    li = page[page.index(f'<li id="t-{eid}"'):]
    li = li[:li.index('id="t-', 10)]
    assert li.count('<sup class="fm">') == len(fns[1]) and li.count(f'<li id="fn-{eid}-') == len(fns[1])
    assert f'<a href="{permalink.href(eid)}" class="pl" title="Permalink">' in li
    assert 'class="s rub"' in li
    own = set(re.findall(r'\sid="([^"]+)"', page))
    cal_ids = {x["id"] for _, x in cal.entries()}
    assert not own & cal_ids
    for a in re.findall(r'href="#([^"]+)"', page):
        assert a in own, a
    assert 'href="cal.html#' in page or 'href="cal1961' in page
    # the day headings as the calendar's, under the year's and the month's
    assert '<h2 id="t-y1961"' in page and '<h3 id="t-m1961-04"' in page
    assert re.search(r'<div class="day[^"]*" id="t-d1961-04-\d\d"', page)


def test_index_and_links(cal, built):
    ix = built["threads.html"]
    assert '<a href="threads-cuba.html">Cuba</a>' in ix
    assert threads.index_link(cal, "cuba") == '<span class="n tha"><a href="threads-cuba.html">All entries</a>.</span>'
    assert threads.index_link(cal, "desegregation-schools-old-name") == ""


def test_emap_calendar_only(cal):
    """e.json maps ids to the calendar's pages alone (permalink.py, STYLE 4)."""
    D = permalink.emap(cal, permalink.homes(cal))
    assert not any(str(p).startswith("threads") for p in list(D["m"].values()) + list(D["x"].values()))


def test_plan_parts():
    d = datetime.date
    sizes = [(d(1960, 1, 5), 100), (d(1961, 2, 1), 50), (d(1962, 3, 1), 30),
             (d(1963, 1, 2), 90), (d(1963, 5, 2), 90), (d(1963, 11, 2), 90)]
    ps = threads.plan_parts("x", sizes, 140)        # a year a part, small ones packed; 1963 over, in quarters
    assert [(p["page"], p["from"], p["label"]) for p in ps] == [
        ("threads-x-1960", "1960-01-01", "1960"),
        ("threads-x-1961", "1961-01-01", "1961–1962"),
        ("threads-x-1963Q1", "1963-01-01", "Jan.–Mar. 1963"),
        ("threads-x-1963Q2", "1963-04-01", "Apr.–June 1963"),
        ("threads-x-1963Q4", "1963-10-01", "Oct.–Dec. 1963")]
    assert threads.part_index(ps, "1959-12") == 0 and threads.part_index(ps, "1962-12-31") == 1
    assert threads.part_index(ps, "1963-07-01") == 3 and threads.part_index(ps, "1964") == 4
    assert [p["label"] for p in threads.plan_parts("x", sizes, 150)][:2] == ["1960–1961", "Jan. 1962–Mar. 1963"]
    # a quarter over in months
    sizes = [(d(1966, 1, 1), 100), (d(1966, 2, 1), 100), (d(1966, 3, 1), 100)]
    assert [p["label"] for p in threads.plan_parts("x", sizes, 150)] == ["Jan. 1966", "Feb. 1966", "Mar. 1966"]
    # a part planned again keeps its own first day
    assert threads.plan_parts("x", sizes, 150, start="1965-12-15")[0]["from"] == "1965-12-15"


def test_names_entry_footnotes(series):
    """A Names entry's calendar paragraph has the calendar's footnotes, its anchors the person's own."""
    from bib.congress import Pointers
    eid = "cal.1961-04.cuba-bay-of-pigs-4"
    e = series.get(eid)[2]
    ptrs = Pointers(series, build.Linker(series))
    got = lives.calendar_sentences(ptrs, [e], "kennedy-john-f")
    text = got[0]["text"]
    n = len(footnotes.build(series, e)[1])
    assert text.count('<sup class="fm">') == n and text.count('<li id="fn-kennedy-john-f~') == n
    assert '<ol class="fn">' in text and permalink.mark(eid) in text
    assert "".join(got[0]["ext"]).startswith("To check: ")   # its cites in the footnotes, the rest after them
    para = lives.life_html(got)
    assert para.startswith('<div class="lvl">') and para.endswith("</div>")
