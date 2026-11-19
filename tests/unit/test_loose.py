"""loose.py: the wordings at_for reads, the headings, and the order of a year's and a month's intercalary days.

Written Nov. 19, 2026, with the owner's rulings (notes/owner-brief.md: Nov. 15, "Year alone goes before 'January,'
which is before 'early January,' which is before 'January 1'"; thirds; seasons; Nov. 19, the ghost days). Each row
pins what the function returns; a row that fails is a change of behaviour.
"""
import datetime

import pytest

from bib import loose


def E(date, when, **kw):
    return dict(id="cal.x", date=date, when=when, thread="t", **kw)


AT_FOR = [
    # a month's thirds, and the words that mean them
    (("1962-05", "May, early"), "before 1962-05-01"),
    (("1962-05", "May, first week"), "before 1962-05-01"),
    (("1962-05", "May, the first week"), "before 1962-05-01"),
    (("1962-05", "May, mid-"), "before 1962-05-11"),
    (("1962-05", "May, late"), "before 1962-05-21"),
    (("1962-05", "May, last week"), "before 1962-05-21"),
    (("1962-05", "May, the last week"), "before 1962-05-21"),
    (("1962-05", "May, end"), "before 1962-05-21"),
    (("1962-05", "May, about the end"), "before 1962-05-21"),
    (("1962-05", "May, the last days"), "before 1962-05-21"),
    (("1962-02", "Feb., end"), "before 1962-02-19"),
    (("1964-02", "Feb., end"), "before 1964-02-20"),
    (("1962-11", "Nov., late, the Thanksgiving holidays"), "before 1962-11-21"),
    (("1964-06", "June, early, by the 10th"), "before 1964-06-01"),
    (("1964-07", "July, late, by the 24th"), "before 1964-07-21"),
    # the second and third weeks
    (("1962-05", "May, second week"), "before 1962-05-08"),
    (("1962-05", "May, third week"), "before 1962-05-15"),
    # a season that opens in the month
    (("1963-09", "Sept., early fall"), "before 1963-09-23"),
    (("1961-10", "Oct., autumn"), None),
    # the block: the earliest day implied is the month's first
    (("1962-05", "May, by the 15th"), None),
    (("1962-01", "Jan., early in the year"), None),
    (("1962-01", "Jan., first half"), None),
    (("1961-12", "Dec. (late 1961)"), None),
    (("1967-11", "Nov., late 1967"), None),
    (("1964-03", "Mar., by mid-month"), None),
    (("1968-06", "June, last two weeks"), None),
    # event-relative and named days: a reader's
    (("1960-07", "July, after the convention"), None),
    (("1965-12", "Dec., Christmas"), None),
    (("1961-11", "Nov., Thanksgiving"), None),
    # a year's parts, by months
    (("1961", "1961, early"), "before 1961-01"),
    (("1961", "1961, first half"), "before 1961-01"),
    (("1961", "1961, early in the year"), "before 1961-01"),
    (("1965", "1965, mid-year"), "before 1965-05"),
    (("1967", "1967, mid-"), "before 1967-05"),
    (("1960", "1960, second half"), "before 1960-07"),
    (("1966", "1966, late"), "before 1966-09"),
    (("1968", "1968, spring"), "before 1968-03-20"),
    (("1966", "1966, by the year's end"), None),
    (("1966", "1966, early, or late 1965"), None),
    (("1962", "1962, later"), None),
    (("1960", "1960, Spring Festival"), None),
    (("1960", "1960, 11th lunar month, 7th day"), None),
    (("1964", "1964–65"), None),
]


@pytest.mark.parametrize("args,want", AT_FOR)
def test_at_for(args, want):
    assert loose.at_for(E(*args)) == want


def test_at_for_leaves_an_at_alone():
    assert loose.at_for(E("1962-05", "May, late", at="before 1962-05-11")) is None


HEADING = [
    (("1962-05", "May, first week", "before 1962-05-01"), "Early May"),
    (("1962-05", "May, end", "before 1962-05-21"), "Late May"),
    (("1962-05", "May, second week", "before 1962-05-08"), "Second week of May"),
    (("1962-05", "May, third week", "before 1962-05-15"), "Third week of May"),
    (("1961", "1961, early", "before 1961-01"), "Early 1961"),
    (("1961", "1961, first half", "before 1961-01"), "Early 1961"),
    (("1965", "1965, mid-year", "before 1965-05"), "Mid-1965"),
    (("1966", "1966, late", "before 1966-09"), "Late 1966"),
    (("1960", "1960, second half", "before 1960-07"), "Second half of 1960"),
]


@pytest.mark.parametrize("args,want", HEADING)
def test_heading(args, want):
    d, w, a = args
    assert loose.heading(E(d, w, at=a)) == want


def test_parse_at_month():
    assert loose.parse_at("before 1962-05") == ("month", datetime.date(1962, 5, 1))
    assert loose.parse_at("after 1962-05") is None
    assert loose.parse_at("before 1962-13") is None


AT_PROBLEMS = [
    (("1962", "1962, mid-", "before 1962-05"), []),
    (("1962", "1962, mid-", "before 1963-05"), ["at 'before 1963-05' falls outside the entry's date 1962"]),
    (("1962-05", "May, late", "before 1962-05"),
     ["at 'before 1962-05': before a month's block is for a year-dated entry; a month's own takes 'before YYYY-MM-DD'"]),
]


@pytest.mark.parametrize("args,want", AT_PROBLEMS)
def test_at_problems(args, want):
    d, w, a = args
    assert loose.at_problems(E(d, w, at=a)) == want


def test_order_of_a_year_and_its_months():
    """"1961", "Early 1961", "January", "Early January", Jan. 1 ...; "Mid-1961", "May", "Early May", May 1 ...;
    "Second half of 1961", "July"; "Late 1961", "September" (loose.py, STYLE 2)."""
    rows = [
        ("Jan. 1", E("1961-01-01", "Jan. 1")),
        ("Early January", E("1961-01", "Jan., early", at="before 1961-01-01")),
        ("January", E("1961-01", "Jan.")),
        ("Early 1961", E("1961", "1961, early", at="before 1961-01")),
        ("1961", E("1961", "1961")),
        ("May 1", E("1961-05-01", "May 1")),
        ("Early May", E("1961-05", "May, first week", at="before 1961-05-01")),
        ("May", E("1961-05", "May")),
        ("Mid-1961", E("1961", "1961, mid-year", at="before 1961-05")),
        ("Apr. 30 bis", E("1961-04", "Apr., after the 30th", at="after 1961-04-30")),
        ("July", E("1961-07", "July")),
        ("Second half of 1961", E("1961", "1961, second half", at="before 1961-07")),
        ("Sept. 1", E("1961-09-01", "Sept. 1")),
        ("September", E("1961-09", "Sept.")),
        ("Late 1961", E("1961", "1961, late", at="before 1961-09")),
    ]
    got = [name for name, e in sorted(rows, key=lambda r: loose.order_key(r[1]))]
    assert got == ["1961", "Early 1961", "January", "Early January", "Jan. 1", "Apr. 30 bis", "Mid-1961", "May",
                   "Early May", "May 1", "Second half of 1961", "July", "Late 1961", "September", "Sept. 1"]


def test_a_year_part_moves_to_its_month():
    e = E("1961", "1961, mid-year", at="before 1961-05")
    assert loose.moves(e) and loose.place_day(e) == datetime.date(1961, 5, 1) and loose.place_iso(e) == "1961-05-01"
