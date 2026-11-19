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
