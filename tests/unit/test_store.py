"""store.py: slug and fold (accents, Đ), normalize_entry, rev.

Generated once from the code's behaviour on Nov. 19, 2026 (tests/README.md): each row pins what the function returned
then. A row that fails is a change of behaviour: a regression, or a fix to be read and the row rewritten with it.
"""
import datetime
import hashlib
import os
import pickle

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


# ---------------------------------------------------------------- the loader (code review C, PERF 2)

def test_loader_is_libyaml_when_available():
    import yaml
    if getattr(yaml, "__with_libyaml__", False):
        assert store.LOADER_KIND == "libyaml" and issubclass(store._Loader, yaml.CSafeLoader)
    else:
        assert store.LOADER_KIND == "python"


def test_loader_keeps_dates_as_strings(tmp_path):
    p = tmp_path / "x.yaml"
    p.write_text("date: 1961-04-15\nwhen: 2026-11-19T10:00:00\nn: yes\nk: 1\n", encoding="utf-8")
    assert store._parse_yaml(str(p)) == {"date": "1961-04-15", "when": "2026-11-19T10:00:00", "n": True, "k": 1}


def test_bad_yaml_message_is_the_python_loaders(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("entries:\n- id: a\n  c: one: two\n", encoding="utf-8")
    with pytest.raises(store.DataError) as e:
        store._parse_yaml(str(p))
    assert ":3: not valid YAML (mapping values are not allowed here)." in str(e.value)


def test_cache_key_names_the_loader(tmp_path, monkeypatch):
    """A parse kept under one loader is not taken for the other's: the key carries the loader's kind."""
    p = tmp_path / "x.yaml"
    p.write_text("a: 1\n", encoding="utf-8")
    monkeypatch.setattr(store, "CACHE_DIR", str(tmp_path / "cache"))
    store._PARSED.pop(str(p), None)
    assert store.load_yaml(str(p)) == {"a": 1}
    store._PARSED.pop(str(p), None)
    (disk,) = os.listdir(tmp_path / "cache")
    with open(tmp_path / "cache" / disk, "rb") as f:
        assert pickle.load(f)[0].endswith("/" + store.LOADER_KIND)
    monkeypatch.setattr(store, "LOADER_KIND", "other")
    with open(tmp_path / "cache" / disk, "wb") as f:     # a parse kept by the other loader: not taken
        pickle.dump((hashlib.sha1(b"a: 1\n").hexdigest() + "/libyaml", pickle.dumps({"a": 2})), f)
    assert store.load_yaml(str(p)) == {"a": 1}
