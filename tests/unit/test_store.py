"""store.py: slug and fold (accents, Đ), normalize_entry, rev.

Generated once from the code's behaviour on Nov. 19, 2026 (tests/README.md): each row pins what the function returned
then. A row that fails is a change of behaviour: a regression, or a fix to be read and the row rewritten with it.
"""
import datetime

import pytest

from bib import store

SLUG = [
    ('Ngô Đình Diệm', 'ngo-dinh-diem'),
    ('Đà Nẵng', 'da-nang'),
    ("Kennedy's Thousand Days", 'kennedys-thousand-days'),
    ('A & B', 'a-and-b'),
    ('  Spaces   and—dashes ', 'spaces-and-dashes'),
    ('Café Società', 'cafe-societa'),
    ('one two three four five six seven', 'one-two-three-four-five-six'),
    ('Ü', 'u'),
    ('đ lower', 'd-lower'),
    ('It’s', 'its'),
    ('', ''),
    ('1961: Berlin', '1961-berlin'),
]
SLUG_SHORT = [
    ('a b c d', 2, 'a-b'),
    ('a b c', 0, ''),
]
FOLD = [
    ('Ngô Đình Diệm', 'ngo dinh diem'),
    ('Đà Nẵng', 'da nang'),
    ("Kennedy's Thousand Days", 'kennedys thousand days'),
    ('A & B', 'a and b'),
    ('  Spaces   and—dashes ', 'spaces and dashes'),
    ('Café Società', 'cafe societa'),
    ('one two three four five six seven', 'one two three four five six seven'),
    ('Ü', 'u'),
    ('đ lower', 'd lower'),
    ('It’s', 'its'),
    ('', ''),
    ('1961: Berlin', '1961 berlin'),
]
NORMALIZE = [
    ({'n': 'x', 'id': 'a', 'c': ['one'], 'tags': 't', 'date': 1962}, {'id': 'a', 'date': '1962', 'c': 'one', 'n': 'x', 'tags': ['t']}),
    ({'id': 'a', 'also': [], 'tags': [], 'zzz': 1, 'when': 'Apr. 1', 'thread': 't'}, {'id': 'a', 'when': 'Apr. 1', 'thread': 't', 'zzz': 1}),
    ({'id': 'a', 'aliases': ['b', 3], 'work': ['w.a'], 'c': ['a', 'b']}, {'id': 'a', 'work': 'w.a', 'c': ['a', 'b'], 'aliases': ['b', '3']}),
    ({'conflict': [1], 'id': 'a', 'place': 'x', 'time_zone': 'UTC'}, {'id': 'a', 'place': 'x', 'conflict': [1], 'time_zone': 'UTC'}),
]
REV = [
    ({'id': 'a'}, '60d31326'),
    ({'id': 'a', 'c': 'x'}, '8ae617f1'),
    ({'id': 'a', 'c': 'x', 'conflict': [1]}, '8ae617f1'),
    ({'id': 'a', '_derived': {}, 'c': 'x'}, '8ae617f1'),
]


@pytest.mark.parametrize("text,want", SLUG)
def test_slug(text, want):
    assert store.slug(text) == want


@pytest.mark.parametrize("text,n,want", SLUG_SHORT)
def test_slug_maxwords(text, n, want):
    assert store.slug(text, n) == want


@pytest.mark.parametrize("text,want", FOLD)
def test_fold(text, want):
    assert store.fold(text) == want


@pytest.mark.parametrize("e,want", NORMALIZE)
def test_normalize_entry(e, want):
    got = store.normalize_entry(dict(e))
    assert got == want and list(got) == list(want)          # the order of the fields too


def test_normalize_date_object():
    assert store.normalize_entry({"id": "a", "date": datetime.date(1961, 4, 17)})["date"] == "1961-04-17"


@pytest.mark.parametrize("e,want", REV)
def test_rev(e, want):
    assert store.rev(e) == want


def test_rev_ignores_key_order_and_conflicts():
    a = {"id": "x", "c": "C", "n": "N", "tags": ["t"]}
    b = {"tags": ["t"], "n": "N", "c": "C", "id": "x", "conflict": [{"field": "c"}]}
    assert store.rev(a) == store.rev(b)


def test_as_list():
    assert [store.as_list(None), store.as_list("a"), store.as_list(["a"])] == [[], ["a"], ["a"]]
