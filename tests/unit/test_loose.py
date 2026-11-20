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
    (("1962-10", "Oct., first half"), None),
    # a year's weeks, days and end: a reader's (the lead's audit, Nov. 19)
    (("1962", "1962, end"), None),
    (("1967", "1967, end"), None),
    (("1962", "1962, last week"), None),
    (("1962", "1962, mid-month"), None),
    (("1962", "1962, the last days"), None),
    (("1962", "1962, about the end"), None),
    (("1962", "1962, middle"), "before 1962-05"),
    (("1962", "1962, late, after the plenum"), "before 1962-09"),
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


HEADING = [   # the loose date in the entry's own words (STYLE 1; the lead's audit, Nov. 19, 2026)
    (("1962-05", "May, early", "before 1962-05-01"), "Early May"),
    (("1962-05", "May, mid", "before 1962-05-11"), "Mid-May"),
    (("1962-05", "May, mid-month", "before 1962-05-11"), "Mid-May"),
    (("1962-05", "May, late", "before 1962-05-21"), "Late May"),
    (("1962-05", "May, first week", "before 1962-05-01"), "First week of May"),
    (("1962-04", "Apr., the first week", "before 1962-04-01"), "First week of April"),
    (("1960-10", "Oct., the last week", "before 1960-10-21"), "Last week of October"),
    (("1960-11", "Nov., end", "before 1960-11-21"), "End of November"),
    (("1960-01", "Jan., the last days", "before 1960-01-21"), "Last days of January"),
    (("1962-11", "Nov., late, the Thanksgiving holidays", "before 1962-11-22"),
     "Late November, the Thanksgiving holidays"),
    (("1964-06", "June, early, by the 10th", "before 1964-06-01"), "Early June, by the 10th"),
    (("1963-09", "Sept., early fall", "before 1963-09-23"), "Early fall"),
    (("1965", "1965, autumn", "before 1965-09-23"), "Autumn"),
    (("1962-10", "Oct., first half", "before 1962-10-01"), "First half of October"),
    (("1962-05", "May, second week", "before 1962-05-08"), "Second week of May"),
    (("1962-05", "May, third week", "before 1962-05-15"), "Third week of May"),
    (("1961", "1961, early", "before 1961-01"), "Early 1961"),
    (("1961", "1961, first half", "before 1961-01"), "First half of 1961"),
    (("1967", "1967, end", "before 1967-09"), "End of 1967"),
    (("1965", "1965", "before 1965-05"), "Before May"),
    (("1965", "1965", "before 1965-05-20"), "Before May 20"),
    (("1965", "1965", "after 1965-05-30"), "After May 30"),
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
    (("1962", "1962, late", "before 1962-09-01"),         # the old day form: after September's heading
     ["at 'before 1962-09-01' on a year-dated entry: before the month's heading is 'at: before 1962-09'"]),
    (("1960", "1960, early", "before 1960-01-01"),
     ["at 'before 1960-01-01' on a year-dated entry: before the month's heading is 'at: before 1960-01'"]),
    (("1962", "1962, spring", "before 1962-03-21"), []),
    (("1962-05", "May, late", "before 1962-05"),
     ["at 'before 1962-05': before a month's block is for a year-dated entry; a month's own takes 'before YYYY-MM-DD'"]),
]


@pytest.mark.parametrize("args,want", AT_PROBLEMS)
def test_at_problems(args, want):
    d, w, a = args
    assert loose.at_problems(E(d, w, at=a)) == want



def BEFORE(d, at, solstice):
    what = "the year" if len(d) == 4 else "the month"
    return [("loose-at-month", f"at {at!r} falls before the entry's date {d}: it would show the entry in {what} before "
                               f"its own; at is a day within the date (a winter ending in March, on a January to March "
                               f"or a year's entry whose when names it: before {solstice}, the December solstice), or "
                               f"keep a reader's own day with the tag ok:loose-at")]


AT_FINDINGS = [   # [loose-at-month]: an `at` before the entry's own month or year (the audit, Nov. 19, 2026)
    # the audit's case: before the 1962 solstice (Dec. 22 in Washington) on a plain February: the old rule let it by
    (("1963-02", "Feb.", "before 1962-12-22", ()), BEFORE("1963-02", "before 1962-12-22", "1962-12-22")),
    (("1963-02", "Feb.", "after 1963-01-31", ()), BEFORE("1963-02", "after 1963-01-31", "1962-12-22")),
    (("1963-02", "Feb.", "before 1963-01-15", ()), BEFORE("1963-02", "before 1963-01-15", "1962-12-22")),
    (("1962", "1962", "before 1961-12-21", ()), BEFORE("1962", "before 1961-12-21", "1961-12-21")),
    (("1962", "1962, mid-", "before 1961-05", ()), BEFORE("1962", "before 1961-05", "1961-12-21")),
    # the winter ending in March (STYLE 4): a winter `when`, January to March or the year, the solstice itself
    (("1962-01", "Jan., winter", "before 1961-12-21", ()), []),         # cal.1962-01.africa
    (("1963-02", "Feb., winter", "before 1962-12-22", ()), []),
    (("1963-03", "Mar., late winter", "before 1962-12-22", ()), []),
    (("1962", "1962, winter", "before 1961-12-21", ()), []),
    (("1962-01", "Jan., winter", "before 1961-12-20", ()), BEFORE("1962-01", "before 1961-12-20", "1961-12-21")),
    (("1962-01", "Jan., winter", "before 1961-12-28", ()), BEFORE("1962-01", "before 1961-12-28", "1961-12-21")),
    (("1962-01", "Jan., winter", "after 1961-12-21", ()), BEFORE("1962-01", "after 1961-12-21", "1961-12-21")),
    (("1962-04", "Apr., winter", "before 1961-12-21", ()), BEFORE("1962-04", "before 1961-12-21", "1961-12-21")),
    (("1962-01", "Jan., spring", "before 1961-12-21", ()), BEFORE("1962-01", "before 1961-12-21", "1961-12-21")),
    # a reader's own day, kept
    (("1963-02", "Feb.", "before 1963-01-15", ("ok:loose-at",)), []),
    (("1963-02", "Feb.", "before 1963-01-15", ("ok:loose-at-month",)), []),
    (("1963-02", "Feb.", "before 1963-01-15", ("ok:thread-first",)), BEFORE("1963-02", "before 1963-01-15", "1962-12-22")),
    # within the date, and after it (the general rule, unchanged; no tag silences it)
    (("1963-02", "Feb., early", "before 1963-02-01", ()), []),
    (("1963-02", "Feb.", "after 1963-02-28", ()), []),
    (("1963-02", "Feb.", "after 1963-03-02", ("ok:loose-at",)),
     [("general", "at 'after 1963-03-02' falls outside the entry's date 1963-02")]),
]


@pytest.mark.parametrize("args,want", AT_FINDINGS)
def test_at_findings(args, want):
    d, w, a, tags = args
    e = E(d, w, at=a, tags=list(tags))
    assert loose.at_findings(e) == want
    assert loose.at_problems(e) == [m for _, m in want]

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
