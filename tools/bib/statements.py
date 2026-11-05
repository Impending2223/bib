"""Thread statements written once (notes/extensions/memos/volume.md, §4; the owner, Oct. 30, 2026: the dates, ranges and
tagged years "invisible to the human reader. They're just sorting and redrafting aids"; no "Stations:"). Built Nov. 4,
2026.

A thread's entry in th.yaml keeps one statement, `c`, for every part of the calendar, however many parts there are (three
now; a page a year next). For a part, from its first day to its last (`calsplit.part_range`), the statement shown is:

    the scope      the text of `c` outside span tags, on every page the thread is on
    the spans      each `{{FROM..TO|text}}` inside `c`, without its tag, where FROM..TO meets the part's range
    the events     the names (`short:`) of the thread's events whose first entry falls in the part, in date order, as
                   one clipped sentence: "Bay of Pigs; Mongoose." (`render`)

A thread that still has `c2` or `c3` keeps the old choice, a statement a part (`calsplit.statement`), until it is
converted; `tools/statements/apply.py` converts one (it writes `c` and drops `c2`, `c3`), `tools/statements/show.py`
shows what a draft would print, a year at a time.

STYLE (settled; keep it):
 1. The span syntax is the indicators' master's (tools/bib/concepts.py, `parse`, `ranges`): FROM and TO as YYYY,
    YYYY-MM or YYYY-MM-DD; either end open (`{{..1962|...}}`, `{{1966..|...}}`); one date alone is its own span
    (`{{1961-04|...}}` is April 1961); several spans joined by commas; `{{not SPAN|...}}` shown only where SPAN does not
    meet the part. A span meets a part where it begins on or before the part's last day and ends on or after its first.
    Put a piece's separator inside its braces; a separator a dropped piece leaves at an opening or a close is tidied
    away (`concepts.tidy`), and only in a statement that has a span: an untagged statement prints as written.
 2. Nothing of the span shows: not the tag, not its dates. A tagged sentence is written so that it reads alone and
    beside the scope on any page it meets.
 3. The events: a calendar entry carrying `short:` (the event's name, on its first entry, until the event record of
    §5) whose primary `thread:` is the thread, or a ghost subthread of it (a subthread without a statement: its events
    have no statement of their own to stand in, so its parent's carries them, through any depth of ghosts). A subthread
    with a statement names its own events, under its parent in the index, and the parent does not repeat them (or
    Vietnam's would name every event of its twenty-odd subthreads; the index's dates, too, give a parent its own
    entries only since Nov. 4, 2026, calsplit.py STYLE 15, but a ghost's events stay in its parent's statement). An entry the thread holds through `also:` is named there too, repeated (the
    owner's ruling, Nov. 4, 2026: "Don't drop the parent thread events unless the child has a thread summary. Repeat
    them. Everything needs to be in plain Roman text somewhere"): a State of the Union listed in Vietnam by `also:` is
    named in the Program's statement and in Vietnam's; the only event a thread does not name is one filed under a
    subthread of it that has its own statement, where it is named. Each name plain text, not
    linked (the owner, Nov. 4, 2026: "Please unlink the event names"), a semicolon between, a full stop at the end, the first letter a capital (a name is written as it
    reads within the sentence: "the second round", "Resolution 1725"); no label, no dates. An entry dated by month
    alone falls on its month's first day for the order, and in every part its month meets (a month-only entry of January
    1960 shows though the calendar opens Jan. 6). In date order, then file order.
 4. `short:` has one other use: an entry with `to:` (an address that sets several threads going) is named by its
    `short:` in the "From:" lines under the entries it reaches (`program_links`, `program_html` in build.py; check
    requires the `short:` there). The From lines read only the entries named in some `to:`, so a `short:` on an entry
    without `to:` prints nothing anywhere but its thread's statement. An address's `short:` is its event's name too:
    the Program's statements name its States of the Union.
 5. Placement: the scope and the spans as written, in their order; the events' sentence after them, in the same
    paragraph (the last, where `c` is a list).
 6. check [statements] (`problems`): an error on a span it cannot read; a warning on an untagged sentence of a
    converted thread's `c` that names a year (19xx, or a decade, "1960s"), since it shows on every page the thread is
    on, unless every entry of the thread falls within the years it names (it then shows only on their pages); a
    warning on a tagged sentence whose text names a year its span does not meet; a warning on an event's name that
    holds "|", "[[" or "]]" (the link would break); one warning counting the threads that still have `c2`/`c3`, so
    the conversion's progress shows. An `ok:statements` tag on the thread's entry silences its warnings.
"""
import datetime
import re

from . import store
from .concepts import parse, tidy

LEGACY = tuple(f"c{n}" for n in range(2, 10))
YEAR = re.compile(r"(?<![\d.-])(19\d\d)(s?)(?![\d])")
_EVENTS = {}


def legacy(e):
    """A thread not yet converted: it still has a statement a part (c2, c3 ...)."""
    return any(e.get(k) for k in LEGACY)


def day(d, end=False):
    """A date, a month ('1961-04') or a year ('1961') as a day: its first, or with end its last."""
    s = str(d)[:10]
    if len(s) == 10:
        return datetime.date.fromisoformat(s)
    if len(s) == 7:
        y, m = int(s[:4]), int(s[5:7])
        if not end:
            return datetime.date(y, m, 1)
        nxt = datetime.date(y + (m == 12), m % 12 + 1, 1)
        return nxt - datetime.timedelta(days=1)
    return datetime.date(int(s[:4]), 12, 31) if end else datetime.date(int(s[:4]), 1, 1)


def meets(rs, lo, hi):
    """Whether any of the spans [(from, to)] meets the range lo..hi (dates)."""
    return any(a <= hi and b >= lo for a, b in rs)


def spans(text, lo, hi):
    """The text with each span kept, untagged, where it meets lo..hi, and dropped elsewhere (STYLE 1, 2)."""
    if "{{" not in text:
        return text

    def walk(nodes):
        out = []
        for n in nodes:
            if isinstance(n, str):
                out.append(n)
                continue
            rs, neg, kids = n
            if meets(rs, lo, hi) != neg:
                out.append(walk(kids))
        return "".join(out)
    return tidy(walk(parse(text)))


def _index(lst):
    """slug -> [(first day, file order, id, name)]: the entries carrying `short:`, under their primary thread and, where
    that is a ghost, its parent (and so on up while the parent is a ghost too) (STYLE 3). Kept while the sections' entry counts stand."""
    key = (id(lst), tuple(len(s.entries) for s in lst.walk()))
    if _EVENTS.get(id(lst), (None,))[0] == key:
        return _EVENTS[id(lst)][1]
    out = {}
    for n, (sec, e) in enumerate(lst.entries()):
        if not e.get("short") or not e.get("date") or not e.get("thread"):
            continue
        prim = e["thread"]
        row = (day(e["date"]), n, e["id"], str(e["short"]), day(e["date"], end=True))
        got = set()
        for t in [prim] + list(e.get("also") or []):   # its threads, each up through ghost subthreads to the parent
            while t and t not in got:
                got.add(t)
                if not lst.is_ghost(t):
                    break
                t = lst.thread_parent(t)
        for t in got:                     # not a parent's where the event is a child's that has its own statement
            if t != prim and _summarized_child(lst, prim, t):
                continue
            out.setdefault(t, []).append(row)
    for v in out.values():
        v.sort()
    _EVENTS[id(lst)] = (key, out)
    return out


def _summarized_child(lst, child, parent):
    """Whether `child` lies under `parent` through a subthread with a statement of its own (STYLE 3): on the way up
    from `child` to `parent`, a thread that is no ghost."""
    path, t = [], child
    while t and t != parent:
        path.append(t)
        t = lst.thread_parent(t)
    return t == parent and any(not lst.is_ghost(x) for x in path)


def events(lst, slug, lo, hi):
    """[(id, name)]: the thread's events whose first entry falls in lo..hi, in date order (STYLE 3)."""
    return [(eid, name) for d, _, eid, name, last in _index(lst).get(slug, []) if d <= hi and last >= lo]


def events_sentence(evs):
    """'Bay of Pigs; Mongoose.' -- or '' where there are none: plain text, unlinked (STYLE 3)."""
    if not evs:
        return ""
    names = [name for _, name in evs]
    names[0] = re.sub(r"^(\W*)([a-z])", lambda m: m.group(1) + m.group(2).upper(), names[0])   # the sentence's capital
    t = "; ".join(names)
    return t if re.search(r"[.!?]$", t) else t + "."


def render(lst, e, lo, hi):
    """The statement of thread entry e for the part lo..hi (dates): the scope, the spans that meet it, the events in it.
    A string, or a list where `c` is a list of paragraphs; None where there is nothing to say."""
    slug = e["id"].split(".", 2)[2]
    paras = [spans(str(t), lo, hi) for t in store.as_list(e.get("c"))]
    paras = [p for p in paras if p.strip()]
    ev = events_sentence(events(lst, slug, lo, hi))
    if ev:
        if paras:
            paras[-1] = f"{paras[-1].rstrip()} {ev}"
        else:
            paras = [ev]
    if not paras:
        return None
    return paras[0] if len(paras) == 1 else paras


# ---------------------------------------------------------------- check

def plain(t):
    """The words a reader sees: a link's text, not its target."""
    t = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[\[[^\]]*\]\]", " ", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    return t


def years(t):
    """[(first, last)] of the years a text names: 1961 -> (1961, 1961); 1960s -> (1960, 1969)."""
    out = []
    for m in YEAR.finditer(plain(t)):
        y = int(m.group(1))
        out.append((y - y % 10, y - y % 10 + 9) if m.group(2) else (y, y))
    return out


def sentences(t):
    """A text cut at its sentences' ends, near enough for a warning ("Jan. 20" may cut; nothing is lost)."""
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z*\"'\[(])", t) if s.strip()]


def _flat(nodes):
    return "".join(n if isinstance(n, str) else _flat(n[2]) for n in nodes)


def _tagged(nodes):
    """Every positive span in the nodes, nested ones too: (ranges, its text)."""
    for n in nodes:
        if isinstance(n, str):
            continue
        rs, neg, kids = n
        if not neg:
            yield rs, _flat(kids)
        yield from _tagged(kids)


def thread_years(lst):
    """slug -> the years of its entries, as the index counts them (the primary thread, `also`, their ancestors)."""
    out = {}
    for sec, e in lst.entries():
        if "when" not in e or not e.get("date") or not e.get("thread"):
            continue
        for t in [e["thread"]] + list(e.get("also") or []):
            for s in lst.thread_line(t):
                out.setdefault(s, set()).add(int(str(e["date"])[:4]))
    return out


def problems(series):
    """For ./bib check: (level, where, message) [statements] (STYLE 6)."""
    lst = next((l for l in series.lists.values() if l.kind == "calendar"), None)
    if lst is None:
        return []
    out, old = [], 0
    ty = thread_years(lst)
    for slug, e in lst.threads().items():
        if e.get("see"):
            continue
        conv = not legacy(e)
        old += not conv
        for t in store.as_list(e.get("c")):
            try:
                nodes = parse(str(t))
            except ValueError as err:
                out.append(("error", e["id"], f"statement: a span it cannot read: {err}"))
                continue
            if conv:
                mine = ty.get(slug, set())
                for n in nodes:
                    if not isinstance(n, str):
                        continue
                    for s in sentences(n):
                        ys = years(s)
                        if not ys:
                            continue
                        lo, hi = min(a for a, _ in ys), max(b for _, b in ys)
                        if mine and all(lo <= y <= hi for y in mine):
                            continue
                        out.append(("warn", e["id"], f"statement: an untagged sentence names a year and shows on every "
                                                     f"page the thread is on: {s.strip()[:90]!r}"))
            for rs, text in _tagged(nodes):
                for a, b in years(text):
                    if not meets(rs, datetime.date(a, 1, 1), datetime.date(b, 12, 31)):
                        out.append(("warn", e["id"], f"statement: a tagged sentence names {a if a == b else f'{a}s'}, "
                                                     f"outside its span: {text.strip()[:90]!r}"))
                        break
    for sec, e in lst.entries():
        nm = e.get("short")
        if nm and "when" in e and re.search(r"\||\[\[|\]\]", str(nm)):
            out.append(("warn", e["id"], f"short: {nm!r} holds '|', '[[' or ']]', which break its link in the statement"))
    if old:
        out.append(("warn", f"lists/{lst.key}/th.yaml",
                    f"{old} threads still have c2/c3: not yet converted to one statement (tools/bib/statements.py; "
                    "tools/statements/apply.py)"))
    return out
