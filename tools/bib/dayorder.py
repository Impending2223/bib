"""The day's order, and the time of day (the owner's rulings, Oct. 29, 2026: "Alphabetic sort, first by the name of the
entry's (primary) thread, then by the text of the entry. Anything else is too opaque or too ad hoc"; `follows` and
`time_approx`: "Please do! That sounds wonderful.").

STYLE
1. The order. A day's entries, and a month's undated block alike, are sorted at build by the primary thread's key, the
   thread index's own (check.thread_key: th.yaml's hidden `sort:`, "1960 elections" as "Elections of 1960"; a
   subthread under its parent, "Parent: Sub"), folded, then `c` as plain text, folded (store.fold: no accents, case
   or punctuation). No file is reordered: where the merge or a writer places an entry within its month no longer
   matters to the page.
2. `follows: [<id>, ...]`, optional, hidden: the entry follows the entries named, the same day. The day's order is then
   a topological sort (Kahn's), the ready entry taken first by the key of 1, so entries with no link keep the
   alphabetical order. The basis goes in the note ("By O'Donnell's account, after the meeting"). Not `after:` (the
   patch format's word). Later, in a tick-tock, an untimed linked entry shows "later", never a made-up hour.
3. `time:`, optional, hidden: a full ISO instant in UTC, '1961-10-17T00:30Z' (seconds where the record gives them),
   the local time turned to UTC by the place's zone in the IANA database (a Washington evening falls on the next UTC
   day). Checked, not shown or sorted on, until days are thick enough for a tick-tock. `time_approx: true` beside it:
   a time the source gives loosely ("that evening", "about 7"), shown "about 7 p.m." when times are shown (EDTF's
   `~`). Never a placeholder to force an order: that is what `follows` is for.
4. check [day-order]: an error on a `time` not in the form, or more than a day from the entry's date; `time_approx`
   without `time`, or not true; a `follows` id that names nothing, an entry of another day, itself, a cycle; a pair
   whose times contradict the link (the follower's time before the one it follows).
"""
import datetime
import re

from . import store

TIME = re.compile(r"^(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2})(?::(\d{2}))?Z$")


def plain_c(e):
    c = e.get("c") or ""
    if isinstance(c, list):
        c = " ".join(map(str, c))
    c = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", str(c))
    c = re.sub(r"\[\[[^\]]*\]\]", " ", c)
    c = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", c)
    return store.fold(c.replace("*", ""))


def key(lst, e, cache=None):
    from .check import thread_key
    slug = e.get("thread") or ""
    if cache is not None and slug in cache:
        tk = cache[slug]
    else:
        try:
            tk = store.fold(thread_key(lst, slug))
        except KeyError:
            tk = store.fold(slug)
        if cache is not None:
            cache[slug] = tk
    return (tk, plain_c(e), e.get("id", ""))


def order(lst, entries):
    """The day's (or the month block's) entries in their order: alphabetical (STYLE 1), `follows` honored (STYLE 2)."""
    cache = {}
    keys = {e["id"]: key(lst, e, cache) for e in entries}
    ids = {e["id"] for e in entries}
    before = {e["id"]: [f for f in store.as_list(e.get("follows")) if f in ids and f != e["id"]] for e in entries}
    if not any(before.values()):
        return sorted(entries, key=lambda e: keys[e["id"]])
    by_id = {e["id"]: e for e in entries}
    waiting = {i: set(b) for i, b in before.items()}
    out, done = [], set()
    while len(out) < len(entries):
        ready = [i for i in by_id if i not in done and not (waiting[i] - done)]
        if not ready:                       # a cycle (check fails on it): the rest alphabetically
            ready = [i for i in by_id if i not in done]
        nxt = min(ready, key=lambda i: keys[i])
        done.add(nxt)
        out.append(by_id[nxt])
    return out


def _instant(t):
    m = TIME.match(str(t))
    if not m:
        return None
    try:
        return datetime.datetime.fromisoformat(f"{m.group(1)}T{m.group(2)}:{m.group(3)}:{m.group(4) or '00'}")
    except ValueError:
        return None


def problems(series):
    out = []
    lst = series.lists.get("cal")
    if not lst:
        return out
    idx = {e["id"]: e for _, e in lst.entries()}
    aliases = {a: e["id"] for e in idx.values() for a in e.get("aliases") or []}
    for eid, e in idx.items():
        t = e.get("time")
        if t is not None:
            at = _instant(t)
            if at is None:
                out.append((eid, f"time {t!r}: a UTC instant, '1961-10-17T00:30Z'"))
            else:
                d = str(e.get("date", ""))
                if len(d) == 10:
                    gap = abs((at.date() - datetime.date.fromisoformat(d)).days)
                    if gap > 1:
                        out.append((eid, f"time {t} is {gap} days from the entry's date {d}"))
        if "time_approx" in e:
            if e["time_approx"] is not True:
                out.append((eid, "time_approx: true, or leave it out"))
            if t is None:
                out.append((eid, "time_approx without a time"))
        for f in store.as_list(e.get("follows")):
            g = idx.get(f) or idx.get(aliases.get(f, ""))
            if f == eid:
                out.append((eid, "follows itself"))
            elif g is None:
                out.append((eid, f"follows {f}: no such entry"))
            elif str(g.get("date")) != str(e.get("date")) or len(str(e.get("date", ""))) != 10:
                out.append((eid, f"follows {f}, an entry of another day ({g.get('date')})"))
            else:
                a, b = _instant(g.get("time")), _instant(e.get("time"))
                if a and b and b < a:
                    out.append((eid, f"follows {f} but its time {e['time']} is before {g['time']}"))
    # cycles
    graph = {eid: [f for f in store.as_list(e.get("follows")) if f in idx and f != eid] for eid, e in idx.items() if e.get("follows")}
    state = {}

    def visit(n, path):
        state[n] = 1
        for m in graph.get(n, []):
            if state.get(m) == 1:
                out.append((n, "a cycle of follows: " + " -> ".join(path[path.index(m):] + [m]) if m in path else n))
            elif not state.get(m):
                visit(m, path + [m])
        state[n] = 2
    for n in graph:
        if not state.get(n):
            visit(n, [n])
    return out
