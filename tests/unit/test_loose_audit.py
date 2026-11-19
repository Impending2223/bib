"""The ghost days kept placed (the lead's audit of Nov. 19, 2026): merge.place_loose, check's [loose-at-differs], the
seam's link to the next part's first anchor. On the fixture (April and August 1961)."""
import datetime

import pytest

from bib import calsplit, check, loose, merge, store


@pytest.fixture(scope="module")
def series():
    return store.Series()


def E(eid, date, when, **kw):
    return dict(id=eid, date=date, when=when, thread="space", c="x", n="x.", **kw)


def rules(series, e):
    lst = series.lists["cal"]
    sec = lst.section("196104")
    return [r for _, _, r in check.entry_problems(series, lst, sec, e)]


def test_differs_warns(series):
    e = E("cal.1961-04.t1", "1961-04", "Apr., early", at="before 1961-04-11")
    assert "loose-at-differs" in rules(series, e)


def test_differs_silenced_by_ok(series):
    e = E("cal.1961-04.t2", "1961-04", "Apr., early", at="before 1961-04-11", tags=["ok:loose-at"])
    assert "loose-at-differs" not in rules(series, e)


def test_differs_quiet_when_it_agrees_or_the_when_gives_none(series):
    assert "loose-at-differs" not in rules(series, E("cal.1961-04.t3", "1961-04", "Apr., early", at="before 1961-04-01"))
    assert "loose-at-differs" not in rules(series, E("cal.1961-04.t4", "1961-04", "Apr., Easter", at="before 1961-04-02"))


class Sec:
    def __init__(self, kind, entries):
        self.lst = type("L", (), {"kind": kind})()
        self.entries = entries
        self.id = "x"


def test_place_loose_calendar_only_and_ok_kept():
    cal = Sec("calendar", [E("a", "1961-04", "Apr., late"), E("b", "1961-04", "Apr., late", tags=["ok:loose-at"])])
    bib = Sec("bibliography", [E("c", "1961-04", "Apr., late")])
    rep = merge.Report()
    merge.place_loose({cal, bib}, rep)
    assert cal.entries[0]["at"] == "before 1961-04-21"
    assert "at" not in cal.entries[1] and "at" not in bib.entries[0]
    assert [l.split()[:2] for l in rep.lines] == [["placed", "a:"]]


def test_seam_points_at_the_next_parts_first_anchor(series):
    lst = series.lists["cal"]
    a = datetime.date(1961, 8, 1)
    assert calsplit.first_anchor(lst, a) == "d1961-08-01"      # no year heading, no year's part there
