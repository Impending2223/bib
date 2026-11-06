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
5. `time_range: [<from>, <to>]`, optional, hidden (the owner's ruling, Nov. 5, 2026: "Yes, add the ranges and sort by
   time first"): where the record places an event in a span of the day but gives no hour, the earliest and latest
   instants it allows, in UTC as `time` is; its basis in the note (the chamber sat from noon to 6:07 p.m.: the Daily
   Digest's page; "that evening": the work's page). Never with `time`: an exact hour is a `time`, a loose one a `time`
   with `time_approx`. A clock in doubt (a place whose 1960s daylight time is not settled) is a range of the two
   readings, an hour wide. `time_band:` beside it, optional, names the band the range was drawn from (BANDS: the owner's
   list, Nov. 5, 2026), in the place's zone (`time_zone:`, IANA), so a page can say "evening, Saigon" or "workday
   afternoon ET"; band_range() turns a date, a band and a zone into the range. `range_basis:` beside it says what
   placed it: `record` (the default: a record or work gives the span, its basis in the note: the Digest's hours, the
   source's "that evening") or `kind` (no record gives it; the event's kind places it, the owner's "where their contents
   or placement suggests so", Nov. 5, 2026: an office act, a meeting, a signing, a hearing or a paper written in an
   office, the workday daytime of its place; a breakfast, the pre-work morning; a lunch, midday; a dinner or a toast,
   the evening; KINDS_PLACE). A `kind` range carries its band and zone, adds nothing to the note, and gives way to any
   record found later.
6. The order, from Nov. 5, 2026 (the owner: "sort by time first"): a day's entries by their place in the day (a `time`,
   or the middle of a `time_range`, in UTC), then by the key of 1; the entries with neither after the placed ones, by
   the key of 1; `follows` honored over both (2). An unplaced entry that a placed one follows takes, for the sort, the
   earliest place among those that follow it, directly or through others, so the pair keeps its place in the day and
   the link puts it first (a meeting with no hour before the 8 p.m. address it decided; Nov. 6, 2026). A month's undated block keeps 1. check adds: a `time_range` not two
   instants in order, more than a day from the date or wider than 36 hours, beside a `time`; a `time_band` not in
   BANDS or without its range and zone; a `follows` whose ranges contradict it (the follower's range wholly before).
"""
import datetime
import re

from . import store

TIME = re.compile(r"^(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2})(?::(\d{2}))?Z$")

# The bands of a day, local time (STYLE 5; the owner's list, Nov. 5, 2026, and the looser words a source uses): name ->
# (start hour, end hour), the end 24 for midnight.
BANDS = {
    "predawn": (0, 6), "pre-work morning": (6, 9), "workday morning": (9, 12), "workday midday": (12, 14),
    "workday afternoon": (14, 17), "workday daytime": (9, 17), "after-workday daytime": (17, 19), "evening": (19, 22),
    "night": (22, 24), "morning": (6, 12), "afternoon": (12, 18), "daytime": (6, 19), "day": (0, 24),
}


# The kinds of event that place an entry with no record of its hour (STYLE 5, range_basis: kind): kind -> band.
KINDS_PLACE = {
    "office act": "workday daytime",      # a meeting, a call, a signing, a swearing-in, a briefing, in an office
    "paper": "workday daytime",           # a memorandum, letter, cable or report written in an office
    "hearing": "workday daytime",         # a committee's hearing or session
    "floor": "workday afternoon",         # a chamber's floor act where the Digest gives no hours (both met at noon)
    "breakfast": "pre-work morning",
    "lunch": "workday midday",
    "dinner": "evening",                  # a dinner, a reception, a toast, a gala
}


def band_range(date, band, zone):
    """[from, to] in UTC for a band of a local day: band_range('1964-08-04', 'evening', 'America/New_York')."""
    import zoneinfo
    a, b = BANDS[band]
    z = zoneinfo.ZoneInfo(zone)
    d = datetime.date.fromisoformat(date)
    lo = datetime.datetime.combine(d, datetime.time(a), z)
    hi = datetime.datetime.combine(d, datetime.time(0), z) + datetime.timedelta(hours=b)
    f = lambda t: t.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    return [f(lo), f(hi)]


def place(e):
    """The entry's place in its day, a UTC datetime: its `time`, or the middle of its `time_range`; None where neither."""
    t = _instant(e.get("time")) if e.get("time") else None
    if t:
        return t
    r = e.get("time_range")
    if isinstance(r, (list, tuple)) and len(r) == 2:
        a, b = _instant(r[0]), _instant(r[1])
        if a and b:
            return a + (b - a) / 2
    return None


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


def order(lst, entries, by_time=True):
    """The day's entries in their order: by their place in the day, then the key of 1, the unplaced after (STYLE 6),
    `follows` honored (STYLE 2). by_time=False (a month's undated block): the key of 1 alone."""
    cache = {}
    far = datetime.datetime.max

    ids = {e["id"] for e in entries}
    before = {e["id"]: [f for f in store.as_list(e.get("follows")) if f in ids and f != e["id"]] for e in entries}
    places = {e["id"]: (place(e) if by_time else None) for e in entries}
    if by_time:                             # an unplaced entry a placed one follows: the earliest such place (STYLE 6)
        inherited = set()
        changed = True
        while changed:
            changed = False
            for i, bs in before.items():
                if places[i] is None:
                    continue
                for b in bs:
                    if places[b] is None or (b in inherited and places[i] < places[b]):
                        places[b] = places[i]
                        inherited.add(b)
                        changed = True

    def k(e):
        p = places[e["id"]]
        return (0 if p else 1, p or far) + key(lst, e, cache)
    keys = {e["id"]: k(e) for e in entries}
    if not any(before.values()):
        return sorted(entries, key=lambda e: keys[e["id"]])
    by_id = {e["id"]: e for e in entries}
    waiting = {i: set(b) for i, b in before.items()}
    out, done = [], set()
    while len(out) < len(entries):
        ready = [i for i in by_id if i not in done and not (waiting[i] - done)]
        if not ready:                       # a cycle (check fails on it): the rest in key order
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
        r = e.get("time_range")
        if r is not None:
            rr = [_instant(x) for x in r] if isinstance(r, (list, tuple)) and len(r) == 2 else None
            if not rr or None in rr:
                out.append((eid, f"time_range {r!r}: two UTC instants, ['1961-10-17T14:00Z', '1961-10-17T22:00Z']"))
            elif rr[1] < rr[0]:
                out.append((eid, f"time_range {r!r}: its end before its start"))
            elif (rr[1] - rr[0]).total_seconds() > 36 * 3600:
                out.append((eid, f"time_range {r!r}: wider than 36 hours"))
            else:
                d = str(e.get("date", ""))
                if len(d) == 10 and abs((rr[0].date() - datetime.date.fromisoformat(d)).days) > 1:
                    out.append((eid, f"time_range {r!r} is more than a day from the entry's date {d}"))
            if t is not None:
                out.append((eid, "time and time_range both: an exact hour is a time, a span a time_range"))
        if e.get("range_basis") is not None:
            if e["range_basis"] not in ("record", "kind"):
                out.append((eid, "range_basis: record or kind"))
            if r is None or (e["range_basis"] == "kind" and not (e.get("time_band") and e.get("time_zone"))):
                out.append((eid, "range_basis without its range (a kind range: with its time_band and time_zone)"))
        if e.get("time_band") is not None:
            if e["time_band"] not in BANDS:
                out.append((eid, f"time_band {e['time_band']!r}: one of {', '.join(BANDS)}"))
            if r is None or not e.get("time_zone"):
                out.append((eid, "time_band without its time_range and time_zone"))
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
                ga = _instant((g.get("time_range") or [None])[0]) if g.get("time_range") else a
                eb = _instant((e.get("time_range") or [None, None])[1]) if e.get("time_range") else b
                if ga and eb and eb < ga and not (a and b):
                    out.append((eid, f"follows {f} but its range ends before the other's begins"))
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
