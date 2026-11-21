"""chron.py: the chronological sort, the one order of every list of calendar entries (the owner, Nov. 21, 2026: "It's
just 'the chronological sort'"). Each test pins an order the calendar shows; a failure is a change of behaviour.
"""
import random

from bib import chron, dayorder


class Sec:
    def __init__(self, entries):
        self.entries = entries


class Cal:
    """A calendar of one section: no thread index, so a thread sorts by its slug (dayorder.key)."""
    key = "cal"

    def __init__(self, entries):
        self.secs = [Sec(list(entries))]

    def walk(self):
        return iter(self.secs)

    def entries(self):
        return ((s, e) for s in self.secs for e in s.entries)

    def threads(self):
        return {}


def E(i, date, when, thread="t", c="", **kw):
    return dict(id=f"cal.{i}", date=date, when=when, thread=thread, c=c or i, **kw)


def ids(es):
    return [e["id"][4:] for e in es]


def check(entries, want):
    """The calendar's order, whatever the order given."""
    lst = Cal(entries)
    for seed in range(5):
        es = list(entries)
        random.Random(seed).shuffle(es)
        assert ids(chron.sort(lst, es)) == want


def test_a_year_and_its_month():
    """"1962", "Early 1962", "January", "Early January", Jan. 1 (loose STYLE 2)."""
    check([E("jan1", "1962-01-01", "Jan. 1"),
           E("early-jan", "1962-01", "Jan., early", at="before 1962-01-01"),
           E("jan", "1962-01", "Jan."),
           E("early-1962", "1962", "1962, early", at="before 1962-01"),
           E("y1962", "1962", "1962"),
           E("dec31", "1961-12-31", "Dec. 31")],
          ["dec31", "y1962", "early-1962", "jan", "early-jan", "jan1"])


def test_a_month_with_at():
    """"May", "Early May", May 1 ... May 20, "Late May", May 21; "After May 12" straight after May 12."""
    check([E("may21", "1962-05-21", "May 21"),
           E("late", "1962-05", "May, late", at="before 1962-05-21"),
           E("may20", "1962-05-20", "May 20"),
           E("after12", "1962-05", "May, after the 12th", at="after 1962-05-12"),
           E("may12", "1962-05-12", "May 12"),
           E("may13", "1962-05-13", "May 13"),
           E("may", "1962-05", "May"),
           E("may1", "1962-05-01", "May 1")],
          ["may", "may1", "may12", "after12", "may13", "may20", "late", "may21"])


def test_a_mid_year_part_before_its_month():
    """"Mid-1962" before "May"; the year's own block before January."""
    check([E("may", "1962-05", "May"),
           E("mid", "1962", "1962, mid-year", at="before 1962-05"),
           E("apr30", "1962-04-30", "Apr. 30"),
           E("y", "1962", "1962")],
          ["y", "apr30", "mid", "may"])


def test_a_span_by_its_first_day():
    """A span stands on its first day, among that day's entries by thread, before the next day's."""
    check([E("may4", "1962-05-04", "May 4", thread="a"),
           E("span", "1962-05-03", "May 3–5", thread="c"),
           E("may3", "1962-05-03", "May 3", thread="b")],
          ["may3", "span", "may4"])


def test_a_time_band_by_its_middle():
    """The day by its place (a `time`, the middle of a band's range), then by thread; the unplaced after."""
    ev = dayorder.band_range("1962-05-03", "evening", "America/New_York")
    check([E("none", "1962-05-03", "May 3", thread="a"),
           E("evening", "1962-05-03", "May 3", thread="b", time_range=ev, time_band="evening",
             time_zone="America/New_York"),
           E("ten", "1962-05-03", "May 3", thread="c", time="1962-05-03T14:00Z")],
          ["ten", "evening", "none"])


def test_an_election_night_pin():
    """A kind range of the band "election night" sorts at 11:59 p.m. of its date, not at the range's middle."""
    r = dayorder.band_range("1962-11-06", "election night", "America/Chicago")
    check([E("late", "1962-11-06", "Nov. 6", thread="z", time="1962-11-07T05:30Z"),
           E("vote", "1962-11-06", "Nov. 6", thread="a", time_range=r, time_band="election night",
             time_zone="America/Chicago", range_basis="kind")],
          ["late", "vote"])


def test_follows():
    """`follows` over the thread: the leader first; an unplaced leader at its follower's place."""
    check([E("lead", "1962-05-03", "May 3", thread="z"),
           E("follow", "1962-05-03", "May 3", thread="a", follows=["cal.lead"])],
          ["lead", "follow"])
    check([E("meeting", "1962-05-03", "May 3", thread="z"),
           E("noon", "1962-05-03", "May 3", thread="m", time="1962-05-03T16:00Z"),
           E("speech", "1962-05-03", "May 3", thread="a", time="1962-05-04T00:00Z", follows=["cal.meeting"])],
          ["noon", "meeting", "speech"])


def test_ties_on_one_day():
    """No place: the thread, then the text (folded), then the id."""
    check([E("b2", "1962-05-03", "May 3", thread="b", c="Zorin to Rusk"),
           E("b1", "1962-05-03", "May 3", thread="b", c="Ádams to Rusk"),
           E("a", "1962-05-03", "May 3", thread="a", c="Zebra"),
           E("b3", "1962-05-03", "May 3", thread="b", c="Zorin to Rusk")],
          ["a", "b1", "b2", "b3"])


def test_subentries_after_their_parent():
    check([E("kid", "1962-05-03", "May 3", thread="a", part_of="cal.parent"),
           E("parent", "1962-05-03", "May 3", thread="m"),
           E("b", "1962-05-03", "May 3", thread="b")],
          ["b", "parent", "kid"])


def test_some_entries_in_the_calendars_order():
    """A person's or a work's entries stand as the calendar shows them, the day ordered whole: an unplaced leader
    keeps its follower's place though the follower is not among them."""
    day = [E("meeting", "1962-05-03", "May 3", thread="z"),
           E("noon", "1962-05-03", "May 3", thread="m", time="1962-05-03T16:00Z"),
           E("speech", "1962-05-03", "May 3", thread="a", time="1962-05-04T00:00Z", follows=["cal.meeting"]),
           E("may", "1962-05", "May", thread="z")]
    lst = Cal(day)
    some = [day[0], day[1], day[3]]
    assert ids(chron.sort(lst, some[::-1])) == ["may", "noon", "meeting"]
    assert [(k[1], [(e["id"][4:], s) for e, s in rows]) for k, rows in chron.groups(lst, some)] == \
        [(-1, [("may", False)]), (1, [("noon", False), ("meeting", False)])]


def test_the_cache_follows_the_list():
    """An entry added to the list is placed (the cache keyed by the sections' counts)."""
    es = [E("b", "1962-05-03", "May 3", thread="b")]
    lst = Cal(es)
    assert ids(chron.sort(lst, es)) == ["b"]
    a = E("a", "1962-05-03", "May 3", thread="a")
    lst.secs[0].entries.append(a)
    assert ids(chron.sort(lst, es + [a])) == ["a", "b"]


def test_an_entry_the_list_does_not_hold():
    lst = Cal([E("b", "1962-05-03", "May 3", thread="b")])
    out = chron.sort(lst, [E("c", "1962-05-04", "May 4"), E("a", "1962-05-03", "May 3", thread="a")])
    assert ids(out) == ["a", "c"]


def test_the_fixture_calendar():
    """On the fixture: any of the calendar's entries, shuffled, come back in its pages' order (dayorder.page_rows)."""
    from bib import store
    lst = store.Series().lists["cal"]
    rows = [e for _, e in dayorder.page_rows(lst)]
    some = rows[::3]
    random.Random(1).shuffle(some)
    assert [e["id"] for e in chron.sort(lst, some)] == [e["id"] for e in rows[::3]]
