"""dateline.py: the clock, spans, zone labels and the dateline's text.

Generated once from the code's behaviour on Nov. 19, 2026 (tests/README.md): each row pins what the function returned
then. A row that fails is a change of behaviour: a regression, or a fix to be read and the row rewritten with it.
"""
import datetime

import pytest

from bib import dateline

UTC = datetime.timezone.utc

CLOCK = [
    ((0, 0), 'midnight'),
    ((12, 0), 'noon'),
    ((9, 5), '9:05 a.m.'),
    ((13, 30), '1:30 p.m.'),
    ((23, 59), '11:59 p.m.'),
    ((11, 0), '11 a.m.'),
    ((12, 15), '12:15 p.m.'),
]
SPAN = [
    ((9, 0), (11, 0), '9–11 a.m.'),
    ((11, 0), (13, 0), '11 a.m.–1 p.m.'),
    ((13, 0), (15, 30), '1–3:30 p.m.'),
    ((12, 0), (14, 0), 'noon–2 p.m.'),
    ((22, 0), (0, 0), '10 p.m.–midnight'),
]
ZLABEL = [
    ('America/New_York', {}, 'Washington'),
    ('Asia/Bangkok', {'thread': 'vietnam-hanoi'}, 'Hanoi'),
    ('Asia/Bangkok', {'thread': 'laos'}, 'Bangkok'),
    ('Europe/Paris', {}, 'Paris'),
    ('America/Los_Angeles', {}, 'Los Angeles'),
    (None, {}, ''),
    ('Asia/Ho_Chi_Minh', {}, 'Saigon'),
]
TEXT = [
    ({'id': 'a', 'date': '1961-04-17', 'time': '1961-04-17T15:30Z'}, '10:30 a.m. Wash.'),
    ({'id': 'b', 'date': '1961-04-17', 'time': '1961-04-17T15:30Z', 'time_approx': True}, 'about 10:30 a.m. Wash.'),
    ({'id': 'c', 'date': '1961-04-17', 'time': '1961-04-17T15:30Z', 'time_zone': 'America/New_York'}, 'Washington · 10:30 a.m.'),
    ({'id': 'd', 'date': '1961-04-17', 'time': '1961-04-17T02:00Z', 'time_zone': 'Asia/Shanghai'}, 'Peking · 10 a.m. (Apr. 16, 9 p.m. Wash.)'),
    ({'id': 'e', 'date': '1961-04-17', 'time': '1961-04-17T02:00Z', 'thread': 'china-leadership'}, 'Peking · 10 a.m. (Apr. 16, 9 p.m. Wash.)'),
    ({'id': 'f',
 'date': '1961-04-17',
 'time_range': ['1961-04-17T14:20Z', '1961-04-17T15:20Z'],
 'time_zone': 'America/New_York'}, 'Washington · 9:20–10:20 a.m.'),
    ({'id': 'g',
 'date': '1961-04-17',
 'time_range': ['1961-04-17T14:00Z', '1961-04-17T22:00Z'],
 'time_zone': 'America/New_York',
 'range_basis': 'kind',
 'time_band': 'workday daytime'}, 'Washington · workday'),
    ({'id': 'h',
 'date': '1961-04-17',
 'time': '1961-04-17T15:30Z',
 'time_zone': 'America/Chicago',
 'tags': ['city:st-louis']}, 'St. Louis · 9:30 a.m.'),
    ({'id': 'i', 'date': '1961-04-17', 'time': '1961-04-17T15:30Z', 'time_zone': 'America/Chicago', 'tags': ['state:mo']}, 'Missouri · 9:30 a.m.'),
    ({'id': 'j', 'date': '1961-04-17', 'time': '1961-04-17T15:30Z', 'place': 'moscow'}, 'Moscow · 6:30 p.m.'),
    ({'id': 'k', 'date': '1961-04-17'}, ''),
    ({'id': 'l', 'date': '1961-04-17', 'time': '1961-04-17T16:00Z', 'time_zone': 'Not/AZone'}, '11 a.m. Wash.'),
    ({'id': 'm', 'date': '1961-04-17', 'time': '1961-04-17T23:30Z', 'time_zone': 'Europe/Moscow'}, 'Moscow · 2:30 a.m. (Apr. 17, 6:30 p.m. Wash.)'),
    ({'id': 'n',
 'date': '1964-11-03',
 'time_range': ['1964-11-04T00:00Z', '1964-11-04T06:00Z'],
 'time_zone': 'America/New_York',
 'time_band': 'election night'}, 'Washington · election night'),
]


def at(h, m):
    return datetime.datetime(1961, 4, 17, h, m, tzinfo=UTC)


@pytest.mark.parametrize("hm,want", CLOCK)
def test_clock(hm, want):
    assert dateline._clock(at(*hm)) == want


@pytest.mark.parametrize("a,b,want", SPAN)
def test_span(a, b, want):
    assert dateline._span(at(*a), at(*b)) == want


@pytest.mark.parametrize("zone,e,want", ZLABEL)
def test_zlabel(zone, e, want):
    assert dateline._zlabel(zone, e) == want


@pytest.mark.parametrize("e,want", TEXT)
def test_text(e, want):
    """The dateline of an entry (the fixture's gazetteer and States)."""
    assert dateline.text(e) == want
