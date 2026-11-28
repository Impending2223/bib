"""The place of a calendar entry's act, and the gazetteer its keys name (the owner, Nov. 18, 2026: "Please do add a place
field"; the pass that fills it, notes/briefs/places.md).

STYLE
 1. `place:` on a calendar entry: a gazetteer key, or a list of two (a call, an exchange across a line: the first the
    caller's or sender's place). Where the act was done (the brief's P1-P6); an entry the record does not place has
    none.
 2. The gazetteer, sources/places.yaml: a row a place, `key`, `name` (as the dateline prints it, the calendar's own
    form), `zone` (IANA), `st` (a U.S. State's code) or `in` (a polity, or a list), `kind: state` for a State taken as
    a place, `aliases` (other keys that name it). A key is unique across keys and aliases.
 3. The patch ops: `place: {id, at, basis, note}` (addops.py) sets an entry's place where it has none or the same
    (another place is an `edit`); `place-key: {key, name, zone, st | in, fix}` adds a row (or, with `fix: true`,
    replaces an existing row's name), applied before the patch's other ops.
 4. The zone the dateline reads: the entry's `time_zone`, else its first place's zone (dateline.py, STYLE 3).
 5. A place renamed in the span: `names:` on its row, each `{name, from, until}` (ISO dates, either open), the name
    the dateline prints for an entry of that date; `name` otherwise (Cape Kennedy, Nov. 29, 1963-Oct. 9, 1973).
 6. `check`: every place key resolves; a list holds at most two; every row has a name and a zone the zone database
    knows; no key or alias twice.
"""
import os
import re
from zoneinfo import ZoneInfo

from . import store

PATH = os.path.join(store.ROOT, "sources", "places.yaml")
KEY = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_ROWS = None
_INDEX = None
PENDING = {}          # key -> row: a patch's place-key ops, while it is checked or merged
DIRTY = False         # rows added in memory by a merge, not yet written (merge.apply_patch writes or drops them)
HEADER = None
GEN = 0               # bumped whenever the rows change (reset, add_row): fields.py builds its place pattern again


def _load():
    global _ROWS, _INDEX, HEADER
    if _ROWS is None:
        _ROWS = store.load_yaml(PATH) or [] if os.path.exists(PATH) else []
        with open(PATH, encoding="utf-8") as f:
            HEADER = [l[2:].rstrip("\n") for l in f if l.startswith("# ")] if os.path.exists(PATH) else []
        _INDEX = {}
        for r in _ROWS:
            _INDEX.setdefault(r["key"], r)
            for a in store.as_list(r.get("aliases")):
                _INDEX.setdefault(a, r)
    return _ROWS, _INDEX


def reset():
    global _ROWS, _INDEX, GEN
    _ROWS = _INDEX = None
    GEN += 1
    from . import fields
    fields.reset()


def get(key):
    """The gazetteer's row for a key or alias (a patch's pending row too), or None."""
    if key in PENDING:
        return PENDING[key]
    return _load()[1].get(str(key))


def keys(e):
    """An entry's place keys, as a list."""
    return [str(k) for k in store.as_list(e.get("place"))]


def first(e):
    ks = keys(e)
    return get(ks[0]) if ks else None


def row_problems(r):
    out = []
    k = r.get("key")
    if not k or not KEY.match(str(k)):
        out.append(f"key {k!r}: lowercase words and hyphens")
    if not r.get("name"):
        out.append(f"{k}: no name")
    try:
        ZoneInfo(str(r.get("zone")))
    except Exception:
        out.append(f"{k}: zone {r.get('zone')!r} is no zone the zone database knows")
    return out


def problems(series):
    """STYLE 5: (where, message) pairs."""
    out = []
    rows, _ = _load()
    seen = {}
    for r in rows:
        out += [("sources/places.yaml", m) for m in row_problems(r)]
        for k in [r.get("key")] + list(store.as_list(r.get("aliases"))):
            if k in seen:
                out.append(("sources/places.yaml", f"{k}: twice (rows {seen[k]} and {r.get('key')})"))
            seen[k] = r.get("key")
    lst = series.lists.get("cal")
    if lst:
        for _, e in lst.entries():
            out += [(e["id"], m) for m in entry_problems(e)]
    return out


def entry_problems(e):
    """STYLE 1 and 6 on one calendar entry: its `place` a gazetteer key (a patch's pending row too), or a list of two;
    check's [place] messages (patchcheck.py, STYLE 11, holds a patch's adds and edits to them)."""
    if "place" not in e:
        return []
    out = []
    ks = keys(e)
    if not ks or len(ks) > 2:
        out.append("place: a gazetteer key, or a list of two")
    for k in ks:
        if get(k) is None:
            out.append(f"place {k!r}: not in the gazetteer (sources/places.yaml; a place-key op adds it)")
    return out


def add_row(body, save=True):
    """A place-key op's row added (or, `fix: true`, its name and zone set on the row the key names). Returns an
    error or None."""
    global GEN
    row = {k: body[k] for k in ("key", "name", "names", "zone", "st", "in", "kind", "aliases") if body.get(k) not in (None, "")}
    errs = row_problems(row)
    if errs:
        return "; ".join(errs)
    rows, idx = _load()
    cur = idx.get(row["key"])
    if cur is not None:
        if not body.get("fix"):
            same = all(cur.get(k) == v for k, v in row.items() if k != "key")
            return None if same else f"place-key {row['key']}: the gazetteer has it ({cur.get('name')}); fix: true to change it"
        cur.update({k: v for k, v in row.items() if k != "key"})
    else:
        rows.append(row)
        idx[row["key"]] = row
    GEN += 1
    if save:
        write()
    return None


def write():
    """The gazetteer written, its rows in key order."""
    rows, _ = _load()
    rows.sort(key=lambda r: r["key"])
    store.dump_yaml(rows, PATH, header=HEADER)


def name_on(row, date):
    """The row's name on a date (STYLE 5)."""
    d = str(date or "")[:10]
    for n in store.as_list(row.get("names")):
        if isinstance(n, dict) and n.get("name") and d:
            if (not n.get("from") or d >= str(n["from"])) and (not n.get("until") or d <= str(n["until"])):
                return n["name"]
    return row.get("name")


def zone(e):
    """The entry's clock: its `time_zone`, else its first place's zone, else None (STYLE 4)."""
    if e.get("time_zone"):
        return e["time_zone"]
    r = first(e)
    return r.get("zone") if r else None
