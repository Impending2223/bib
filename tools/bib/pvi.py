"""Checks for the partisan voting index by district: the presidential vote by district read off the Census's Data Books
(elections/readings/districts/, loaded by tools/elections/cd_readings.py) and what tools/elections/make_pvi.py makes of
it (elections/pvi-districts.yaml, elections/cd-president.yaml). Not shown on any page yet (the owner's call).

STYLE
 1. Errors: a reading's figures that do not add (cd_readings.problems: the districts to the State column, the States
    to the printed United States figures unless the volume says `us_holds: false`, D and R (and A, where the volume's
    `fields` hold it) not over the total unless `over` says the page prints it so); an `eye`, `marks`, `over` or
    `as_printed` entry naming no cell; a `pages` list that does not name every column once; a district the
    Congress of the source's `lines` does not seat; a generated file missing, or made from other inputs (its `inputs`,
    a hash of every file make_pvi.py reads: cd_readings.inputs_hash).
 2. Warnings [pvi]: a printed percent the figures do not give, not listed in `percent_as_printed` (the percent is not
    used).
"""
import os

from . import store

ROOT = store.ROOT


def _readings():
    import sys
    sys.path.insert(0, os.path.join(ROOT, "tools", "elections"))
    import cd_readings
    return cd_readings


def problems(series=None):
    """[(level, where, message)]."""
    cd = _readings()
    out = []
    srcs = cd.load()
    for k, d in srcs.items():
        where = d["path"]
        for w, m in cd.problems(d):
            out.append(("error", w, m))
        for w, m in cd.warnings(d):
            out.append(("warn", w, m))
        roster = os.path.join(ROOT, "congress", f"{d.get('lines')}.yaml")
        seated = None
        if os.path.exists(roster):
            seated = {(m["st"], int(m["d"])) for m in store.load_yaml(roster)["house"]}
        years = [str(y) for y in d.get("years") or []]
        for st, e in (d.get("states") or {}).items():
            rows = {int(x) for x in (e.get("d") or {})}
            cols = [int(x) for p in (e.get("pages") or {}).values() for x in p]
            if sorted(cols) != sorted(rows):
                out.append(("error", where, f"{st}: pages name {sorted(cols)}; rows are {sorted(rows)}"))
            if seated is not None:
                for x in rows:
                    if x and (st, x) not in seated:
                        out.append(("error", where, f"{st} {x}: no such district in the {d.get('lines')}th Congress"))
            for fld in ("eye", "marks"):
                if e.get(fld) == "all":
                    continue
                for ent in e.get(fld) or []:
                    p = str(ent).split()
                    if len(p) != 3 or int(p[0]) not in rows or p[1] not in years or p[2] not in cd.fields(d):
                        out.append(("error", where, f"{st} {fld}: '{ent}' names no cell"))
            for ent in e.get("as_printed") or []:
                p = str(ent).split()
                if len(p) != 2 or p[0] not in years or p[1] not in cd.fields(d):
                    out.append(("error", where, f"{st} as_printed: '{ent}' names no State figure"))
            for ent in e.get("over") or []:
                p = str(ent).split()
                if len(p) != 2 or int(p[0]) not in rows or p[1] not in years:
                    out.append(("error", where, f"{st} over: '{ent}' names no row"))
    if srcs:
        want = cd.inputs_hash()
        for name in ("pvi-districts.yaml", "cd-president.yaml"):
            path = os.path.join(ROOT, "elections", name)
            have = (store.load_yaml(path) or {}).get("inputs") if os.path.exists(path) else None
            if have != want:
                out.append(("warn", f"elections/{name}",
                            "missing or made from other inputs: run python3 -I tools/elections/make_pvi.py"))
    return out
