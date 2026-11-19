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
    ((12, 0), '12:00 p.m.'),
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
    ((12, 0), (14, 0), '12:00–2 p.m.'),
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
    ({'id': 'd', 'date': '1961-04-17', 'time': '1961-04-17T02:00Z', 'time_zone': 'Asia/Shanghai'}, 'Peking · 10 a.m.'),
    ({'id': 'e', 'date': '1961-04-17', 'time': '1961-04-17T02:00Z', 'thread': 'china-leadership'}, 'Peking · 10 a.m.'),
    ({'id': 'f',
 'date': '1961-04-17',
 'time_range': ['1961-04-17T14:20Z', '1961-04-17T15:20Z'],
 'time_zone': 'America/New_York'}, 'Washington · 9:20 a.m.'),
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
    ({'id': 'm', 'date': '1961-04-17', 'time': '1961-04-17T23:30Z', 'time_zone': 'Europe/Moscow'}, 'Moscow · 2:30 a.m.'),
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


FULL = [
    # the dateline in full, its `title` (STYLE 4): the range's end and Washington's hour where the day differs
    ({'id': 'd', 'date': '1961-04-17', 'time': '1961-04-17T02:00Z', 'time_zone': 'Asia/Shanghai'},
     'Peking · 10 a.m. (Apr. 16, 9 p.m. Wash.)'),
    ({'id': 'f', 'date': '1961-04-17', 'time_range': ['1961-04-17T14:20Z', '1961-04-17T15:20Z'],
      'time_zone': 'America/New_York'}, 'Washington · 9:20–10:20 a.m.'),
    ({'id': 'r', 'date': '1961-04-17', 'time_range': ['1961-04-17T02:00Z', '1961-04-17T03:00Z'],
      'time_zone': 'Asia/Shanghai'}, 'Peking · 10–11 a.m. (Apr. 16, 9 p.m. Wash.)'),
    ({'id': 'g', 'date': '1961-04-17', 'time_range': ['1961-04-17T14:00Z', '1961-04-17T22:00Z'],
      'time_zone': 'America/New_York', 'range_basis': 'kind', 'time_band': 'evening'}, 'Washington · evening'),
    # (8) a band a reader gave from the record (上午), its hours the band's own: the line its word; the title
    # Washington's day, no hour (none was recorded)
    ({'id': 's', 'date': '1961-04-29', 'time_range': ['1961-04-28T22:00Z', '1961-04-29T04:00Z'],
      'time_zone': 'Asia/Shanghai', 'time_band': 'morning'}, 'Peking · morning (Apr. 28 Wash.)'),
    ({'id': 's2', 'date': '1961-04-29', 'time_range': ['1961-04-29T04:00Z', '1961-04-29T10:00Z'],
      'time_zone': 'Asia/Shanghai', 'time_band': 'afternoon'}, 'Peking · afternoon (Apr. 28–29 Wash.)'),
    # (6) hours of record a reader also gave a band word: the start on the line, the range in the title
    ({'id': 'w', 'date': '1963-06-26', 'time_range': ['1963-06-26T14:30Z', '1963-06-26T21:00Z'],
      'time_zone': 'America/New_York', 'time_band': 'workday daytime', 'range_basis': 'record'},
     'Washington · 10:30 a.m.–5 p.m.'),
    ({'id': 'p', 'date': '1961-10-30', 'time_range': ['1961-10-29T18:00Z', '1961-10-29T19:00Z'],
      'time_zone': 'Asia/Shanghai', 'time_band': 'predawn'}, 'Peking · 2–3 a.m. (Oct. 29, 1 p.m. Wash.)'),
    ({'id': 't', 'date': '1963-01-18', 'time_range': ['1963-01-17T23:00Z', '1963-01-18T05:00Z'],
      'time_zone': 'Asia/Ho_Chi_Minh', 'time_band': 'morning', 'range_basis': 'record'},
     'Saigon · 7 a.m.–1 p.m. (Jan. 17, 6 p.m. Wash.)'),
    ({'id': 'a', 'date': '1961-04-17', 'time': '1961-04-17T17:00Z'}, '12:00 p.m. Wash.'),
    ({'id': 'k', 'date': '1961-04-17'}, ''),
]
HTML = [
    ({'id': 'c', 'date': '1961-04-17', 'time': '1961-04-17T15:30Z', 'time_zone': 'America/New_York'},
     '<span class="dl">Washington · 10:30 a.m.</span>'),
    ({'id': 'r', 'date': '1961-04-17', 'time_range': ['1961-04-17T02:00Z', '1961-04-17T03:00Z'],
      'time_zone': 'Asia/Shanghai'},
     '<span class="dl" title="Peking · 10–11 a.m. (Apr. 16, 9 p.m. Wash.)">Peking · 10 a.m.</span>'),
    ({'id': 's', 'date': '1961-04-29', 'time_range': ['1961-04-28T22:00Z', '1961-04-29T04:00Z'],
      'time_zone': 'Asia/Shanghai', 'time_band': 'morning'},
     '<span class="dl" title="Peking · morning (Apr. 28 Wash.)">Peking · morning</span>'),
    ({'id': 'w', 'date': '1963-06-26', 'time_range': ['1963-06-26T14:30Z', '1963-06-26T21:00Z'],
      'time_zone': 'America/New_York', 'time_band': 'workday daytime', 'range_basis': 'record'},
     '<span class="dl" title="Washington · 10:30 a.m.–5 p.m.">Washington · 10:30 a.m.</span>'),
    ({'id': 'n', 'date': '1961-04-17', 'time': '1961-04-17T17:00Z', 'time_zone': 'America/New_York'},
     '<span class="dl">Washington · 12:00 p.m.</span>'),
    ({'id': 'k', 'date': '1961-04-17'}, ''),
]


@pytest.mark.parametrize("e,want", FULL)
def test_full(e, want):
    assert dateline.full(e) == want


BANDS = [
    # (7) the bands in plain words
    ({'id': 'q', 'date': '1961-05-19', 'time_range': ['1961-05-19T05:00Z', '1961-05-19T11:00Z'],
      'time_zone': 'America/Chicago', 'time_band': 'predawn', 'city': 'x'}, 'before dawn'),
    ({'id': 'v', 'date': '1964-01-08', 'time_range': ['1964-01-08T22:00Z', '1964-01-09T00:00Z'],
      'time_zone': 'America/New_York', 'time_band': 'after-workday daytime'}, 'evening'),
    # (6) the band's own hours: its word; hours of record: their start
    ({'id': 'w', 'date': '1963-06-26', 'time_range': ['1963-06-26T13:00Z', '1963-06-26T21:00Z'],
      'time_zone': 'America/New_York', 'time_band': 'workday daytime', 'range_basis': 'record'}, 'workday'),
    ({'id': 'w2', 'date': '1963-06-26', 'time_range': ['1963-06-26T14:30Z', '1963-06-26T21:00Z'],
      'time_zone': 'America/New_York', 'time_band': 'workday daytime', 'range_basis': 'record'}, '10:30 a.m.'),
    # a band's hours an hour off at one end where summer time was taken for standard: still the band's own
    ({'id': 'm', 'date': '1963-05-06', 'time_range': ['1963-05-06T11:00Z', '1963-05-06T18:00Z'],
      'time_zone': 'America/Chicago', 'time_band': 'morning', 'range_basis': 'record'}, 'morning'),
    # ... but not where the zone keeps one time all year: Lushan's 1 a.m. was recorded
    ({'id': 'l', 'date': '1961-08-30', 'time_range': ['1961-08-29T17:00Z', '1961-08-29T22:00Z'],
      'time_zone': 'Asia/Shanghai', 'time_band': 'predawn'}, '1 a.m.'),
]


@pytest.mark.parametrize("e,want", BANDS)
def test_band_words(e, want):
    assert dateline.text(e).split(" · ")[-1] == want


@pytest.mark.parametrize("e,want", HTML)
def test_html(e, want):
    """The line shows the start alone; the rest in the title, only where it says more."""
    assert dateline.html_(e) == want
