"""The order of a year on the calendar's page: its heading, its block and its intercalary days (偽日), each month's
heading and indicators, the months' and the days' own (daybook.py, STYLE 16-17; loose.py, STYLE 2).

Written Nov. 19, 2026, from the owner's rulings (notes/owner-brief.md): Nov. 15, "Year alone goes before 'January,'
which is before 'early January,' which is before 'January 1'"; "'Early May' after 'May' and before 'May 1'"; seasons
before the season's first day; "after X" after X's day. Nov. 19: "'Early 1960' seems to come after 'January 1960'. I
thought I directed otherwise? Can we fix that, and all similar mis-placements?"; "The 'January 1960' heading and
indicators table comes before '1960.' Can we fix that?"

A synthetic year, 1960, a section a month, January's opening on the 6th as the calendar's does, laid out by
build.section_body (entries stubbed); each month's indicators set after its heading as indicators.inject sets them.
The page's anchors, read in order, must run in the owner's sequence.
"""
import calendar
import datetime
import re

import pytest

from bib import build, loose, store


def E(eid, date, when, **kw):
    return dict(id=f"cal.{eid}", date=date, when=when, thread="t", c="x", **kw)


ENTRIES = [
    E("year", "1960", "1960"),
    E("early-year", "1960", "1960, early", at="before 1960-01"),
    E("first-half", "1960", "1960, first half", at="before 1960-01"),
    E("mid-year", "1960", "1960, mid-year", at="before 1960-05"),
    E("second-half", "1960", "1960, second half", at="before 1960-07"),
    E("late-year", "1960", "1960, late", at="before 1960-09"),
    E("spring", "1960", "1960, spring", at="before " + loose.season_starts(1960)["spring"].isoformat()),
    E("jan", "1960-01", "Jan."),
    E("early-jan", "1960-01", "Jan., early", at="before 1960-01-01"),
    E("jan6", "1960-01-06", "Jan. 6"),
    E("mid-jan", "1960-01", "Jan., mid", at="before 1960-01-11"),
    E("jan11", "1960-01-11", "Jan. 11"),
    E("mar12", "1960-03-12", "Mar. 12"),
    E("after-mar12", "1960-03", "Mar., after the 12th", at="after 1960-03-12"),
    E("before-mar13", "1960-03", "Mar., before the 13th", at="before 1960-03-13"),
    E("mar13", "1960-03-13", "Mar. 13"),
    E("apr30", "1960-04-30", "Apr. 30"),
    E("may", "1960-05", "May"),
    E("early-may", "1960-05", "May, early", at="before 1960-05-01"),
    E("may1", "1960-05-01", "May 1"),
    E("before-jul10", "1960-07", "July, before the 10th", at="before 1960-07-10"),    # a Sunday
    E("jul10", "1960-07-10", "July 10"),
    E("sep", "1960-09", "Sept."),
]


def year_list():
    secs = []
    for m in range(1, 13):
        last = calendar.monthrange(1960, m)[1]
        secs.append({"id": f"1960{m:02d}", "title": f"{calendar.month_name[m]} 1960", "file": f"1960{m:02d}.yaml",
                     "from": f"1960-{m:02d}-{6 if m == 1 else 1:02d}", "to": f"1960-{m:02d}-{last}"})
    lst = store.List("cal", {"kind": "calendar", "sections": secs}, {"key": "cal", "abbr": "Cal."})
    jan = lst.sections[0]
    for e in ENTRIES:                  # filed as the data files them: a year's in January, a month's in its month
        d = e["date"]
        sec = jan if len(d) == 4 else lst.sections[int(d[5:7]) - 1]
        sec.entries.append(dict(e))
    return lst


@pytest.fixture
def page(monkeypatch):
    monkeypatch.setattr(build, "entry_html", lambda series, lst, sec, e, *a, **k: f'<li id="{e["id"]}"></li>')
    lst = year_list()
    loose._HOSTS.clear()
    out = []
    for sec in lst.sections:
        out.extend(build.section_body(None, lst, sec, lambda s: s.id, lambda t, f: t))
    html = "\n".join(out)
    for sec in lst.sections:          # the month's indicators after its heading, as indicators.inject puts them
        pat = re.compile(r'(<h\d id="' + sec.id + r'"[^>]*>.*?</h\d>)', re.S)
        html = pat.sub(lambda m: m.group(1) + f'<table id="ind-{sec.id}"></table>', html, count=1)
    return html


def order(html):
    return re.findall(r'id="([^"]+)"', html)


def before(ids, *seq):
    """Each id of seq stands before the next on the page."""
    at = [ids.index(x) for x in seq]
    assert at == sorted(at), " < ".join(f"{x} ({i})" for x, i in zip(seq, at))


def test_the_year_before_january(page):
    ids = order(page)
    before(ids, "y1960", "cal.year", "ix-1960-01-month", "cal.early-year", "cal.first-half",
           "196001", "ind-196001", "cal.jan", "ix-1960-01-01-before", "cal.early-jan", "d1960-01-06", "cal.jan6",
           "ix-1960-01-11-before", "cal.mid-jan", "d1960-01-11", "cal.jan11")
    assert ids[0] == "y1960"


def test_the_year_heading(page):
    h = re.search(r'<h(\d) class="yh" id="y1960"[^>]*>1960</h\d>', page)
    assert h and h.group(1) == "2"                         # the month's level (a month: h2)
    assert 'data-short="1960" data-crumb="1960"' in h.group(0)
    assert page.count('class="yh"') == 1                   # over the year's first month only
    assert '<span class="dn">1960</span>' not in page      # the heading is the block's: no second "1960"
    assert 'data-ytop="#y1960"' in page                    # a month's year in the top bar: to the year's heading


def test_a_year_part_before_its_month_heading(page):
    ids = order(page)
    before(ids, "d1960-04-30", "cal.apr30", "ix-1960-05-month", "cal.mid-year",
           "196005", "ind-196005", "cal.may", "ix-1960-05-01-before", "cal.early-may", "d1960-05-01", "cal.may1")
    before(ids, "d1960-06-30", "ix-1960-07-month", "cal.second-half", "196007", "ind-196007")
    before(ids, "d1960-08-31", "ix-1960-09-month", "cal.late-year", "196009", "ind-196009", "cal.sep", "d1960-09-01")


def test_a_season_before_its_first_day(page):
    ids = order(page)
    day = loose.season_starts(1960)["spring"]
    prev = day - datetime.timedelta(days=1)
    before(ids, f"d{prev.isoformat()}", f"ix-{day.isoformat()}-before", "cal.spring", f"d{day.isoformat()}")


def test_after_a_day_and_before_the_next(page):
    ids = order(page)
    before(ids, "d1960-03-12", "cal.mar12", "ix-1960-03-12-after", "cal.after-mar12",
           "ix-1960-03-13-before", "cal.before-mar13", "d1960-03-13", "cal.mar13")


def test_before_a_sunday_under_its_week(page):
    assert datetime.date(1960, 7, 10).weekday() == 6
    ids = order(page)
    before(ids, "d1960-07-09", "wk1960-07-10", "ix-1960-07-10-before", "cal.before-jul10", "d1960-07-10")


def test_the_thread_order_agrees():
    """The thread pages' and the thread navigation's order (loose.order_key) is the page's."""
    keyed = sorted(ENTRIES, key=loose.order_key)
    ids = [e["id"][4:] for e in keyed]
    assert ids[:6] == ["year", "early-year", "first-half", "jan", "early-jan", "jan6"]
    assert ids.index("apr30") < ids.index("mid-year") < ids.index("may") < ids.index("early-may") < ids.index("may1")
