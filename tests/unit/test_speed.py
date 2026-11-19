"""The speed fixes (code review C, PERF): what each keeps the same. The outputs themselves are proved by the goldens
and by tests/ab.py on the full data; these pin the mechanisms (built once, cached values not shared mutably)."""
from bib import congress, refs


class _List:
    kind = "calendar"
    key = "cal"

    def __init__(self, entries):
        self._entries = entries

    def entries(self):
        return [(None, e) for e in self._entries]


class _Series:
    def __init__(self, entries):
        self.lists = {"cal": _List(entries)}


class _Linker:
    refs = refs.Refs


def test_pointers_calendar_index_built_once_per_series(monkeypatch):
    calls = []
    heller = {"id": "kja.heller", "s": "Heller, Walter W."}

    def named(self, lst, e):
        calls.append(e["id"])
        return [heller, heller] if e["id"] == "a" else []
    monkeypatch.setattr(congress.Pointers, "named", named)
    a, b = {"id": "a", "c": "x"}, {"id": "b", "c": "x"}
    series, linker = _Series([a, b]), _Linker()
    p1 = congress.Pointers(series, linker)
    p2 = congress.Pointers(series, linker, {})
    assert calls == ["a", "b"]                                    # the calendar walked once
    assert p1.cal is p2.cal and p1.calx is p2.calx
    assert p1.cal["heller walter"] == [a] and p1.calx["kja.heller"] == [a]   # an entry once, though named twice
    congress.Pointers(_Series([a, b]), linker)                    # another series: walked afresh
    assert calls == ["a", "b", "a", "b"]


def test_name_keys_cached_and_immutable():
    k = refs.Refs.name_keys("Kennedy, Robert F.; Mao Zedong")
    assert k == (("kennedy robert", "Kennedy, Robert F."), ("mao zedong", "Mao Zedong"))
    assert refs.Refs.name_keys("Kennedy, Robert F.; Mao Zedong") is k and isinstance(k, tuple)


# ---------------------------------------------------------------- PERF 8: pure string functions computed once

def test_memo_falls_back_for_unhashable_arguments():
    from bib import store
    seen = []

    @store.memo
    def f(x):
        seen.append(x)
        return len(x)
    assert (f("ab"), f("ab"), f(["a"]), f(["a"])) == (2, 2, 1, 1)
    assert seen == ["ab", ["a"], ["a"]]                           # the string once; the list each time


def test_cached_splits_hand_out_new_lists():
    from bib import claims, notemerge
    n = "Fact. [[w.x]], 12. To check: [[w.y]]. Names: Heller."
    a = notemerge.sentences(n)
    a.append("changed")
    assert notemerge.sentences(n) == ["Fact.", "[[w.x]], 12.", "To check: [[w.y]].", "Names: Heller."]
    src, other = claims.note_parts(n)
    src.append("changed")
    other.clear()
    assert claims.note_parts(n) == (["Fact", "[[w.x]], 12"], ["To check: [[w.y]].", "Names: Heller."])
    u = claims.units("One. Two; three.")
    u.pop()
    assert claims.units("One. Two; three.") == ["One.", "Two;", "three."]


# ---------------------------------------------------------------- PERF 5: the merge's index kept, not rebuilt per op

def _same_index(series):
    """The index as reindex left it, against a whole rebuild: the same keys, each to the very same objects."""
    kept = series.index()
    series.invalidate()
    whole = series.index()
    assert set(kept) == set(whole)
    assert all(all(a is b for a, b in zip(kept[k], whole[k])) for k in whole)


def test_reindex_gives_what_a_rebuild_gives():
    from conftest import FIXTURE
    from bib import store
    series = store.Series(FIXTURE)
    cal = series.lists["cal"]
    secs = [s for s in cal.walk() if len(s.entries) >= 3][:2]
    a, b = secs
    series.index()
    assert series._index_keys is not None                   # the fixture: no key two entries claim
    a.entries[0] = dict(a.entries[0], n="replaced")          # an entry replaced (an edit)
    a.entries.insert(1, {"id": "cal.test-new", "c": "x"})    # added
    gone = a.entries.pop()                                   # deleted
    moved = b.entries.pop(0)                                 # moved from b to a
    a.entries.append(moved)
    b.entries[0] = dict(b.entries[0], aliases=["cal.test-old-id"])   # an alias (combine)
    series.reindex({a, b})
    assert series._index is not None and series.get(gone["id"]) is None
    assert series.get("cal.test-old-id")[2] is b.entries[0] and series.get(moved["id"])[1] is a
    _same_index(series)


def test_reindex_drops_the_index_on_a_clash():
    from conftest import FIXTURE
    from bib import store
    series = store.Series(FIXTURE)
    a, b = [s for s in series.lists["cal"].walk() if s.entries][:2]
    series.index()
    a.entries.append(dict(b.entries[0]))                     # b's id now held twice
    series.reindex({a})
    assert series._index is None
    _same_index(series)
    series.index()
    assert series._index_keys is None                        # a rebuild that met the clash: never reindexed
    series.reindex({a})
    assert series._index is None


def test_names_resolved_kept_per_line_and_tags():
    from bib.build import Linker
    calls = []

    class L(Linker):
        def __init__(self):
            pass

        def who_named(self, t, tags=(), taken=()):
            calls.append((t, frozenset(tags)))
            return (None, "#" + t) if t in tags else None
    lk = L()
    first = lk.names_resolved(["a", "b"], ["a"])
    first.append("changed")
    assert lk.names_resolved(["a", "b"], {"a"}) == [(None, "#a"), None]   # the same tags as a set: the same key
    n = len(calls)
    lk.names_resolved(["a", "b"], ("a",))
    assert len(calls) == n
    lk.names_resolved(["a", "b"], ["b"])
    assert len(calls) > n
