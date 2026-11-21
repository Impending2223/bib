"""The chronological sort: the calendar's order, the one order of every list of calendar entries (the owner, Nov. 21,
2026: "I don't want the calendar sort to be a one-off, ad hoc, page-specific sort. It's just 'the chronological
sort'").

By the entry's place (loose.order_key: the year, a year's intercalary day, the month, a day's before, the day, its
after; loose STYLE 2), then as the calendar lays the place out: a day by time, thread and text, `follows` honored
(dayorder.order); a block or an intercalary day by thread and text; a parent's subentries after it (subentries.nest).
Some of the calendar's entries (a person's, a work's, a thread's) stand in the order the calendar shows them.
"""
import weakref

from . import dayorder, loose, subentries

_CACHE = weakref.WeakKeyDictionary()     # the list -> (its entry counts, {id: (rank, place, is_sub)})


def _layout(lst, es):
    """[(entry, is_sub)]: the entries of one place, as the calendar lays them out."""
    by_time = loose.order_key(es[0])[1] == 1
    o = lambda l, xs: dayorder.order(l, xs, by_time=by_time)
    return subentries.nest(lst, o(lst, es), o)


def _ranked(lst, entries):
    """{id: (rank, place, is_sub)} for the entries, each place laid out whole."""
    pools = {}
    for e in entries:
        pools.setdefault(loose.order_key(e), []).append(e)
    out = {}
    for k in sorted(pools):
        for e, sub in _layout(lst, pools[k]):
            out[e["id"]] = (len(out), k, sub)
    return out


def _index(lst):
    sig = tuple(len(s.entries) for s in lst.walk())
    got = _CACHE.get(lst)
    if got is None or got[0] != sig:
        got = _CACHE[lst] = (sig, _ranked(lst, [e for _, e in lst.entries() if "when" in e]))
    return got[1]


def _rows(lst, entries):
    es = list(entries)
    ix = _index(lst)
    if not all(e.get("id") in ix for e in es):       # entries the list does not hold as they are (a dry run's)
        ix = _ranked(lst, es)
    return sorted(((ix[e["id"]], e) for e in es), key=lambda r: r[0][0])


def sort(lst, entries):
    """The entries in the calendar's order. lst: the calendar, or a series (each entry's own calendar)."""
    if hasattr(lst, "lists"):
        by = {}
        for e in entries:
            hit = lst.get(e["id"])
            by.setdefault(hit[0].key if hit else None, []).append(e)
        return [e for k in lst.lists if k in by for e in sort(lst.lists[k], by[k])] + sorted(by.get(None, []), key=loose.order_key)
    return [e for _, e in _rows(lst, entries)]


def groups(lst, entries):
    """[(place, [(entry, is_sub)])]: the entries in the calendar's order, by place (loose.order_key)."""
    out = []
    for (_, k, sub), e in _rows(lst, entries):
        if not out or out[-1][0] != k:
            out.append((k, []))
        out[-1][1].append((e, sub))
    return out
