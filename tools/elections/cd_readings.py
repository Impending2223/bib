"""The presidential vote by congressional district, as read off the Census's Data Books: elections/readings/districts/.

A reading file a volume (its header the schema; cdb-1961.yaml the first). Loaded and held here, for
tools/elections/make_pvi.py (which refuses figures that do not add) and tools/bib/pvi.py (`check`).

    load()             -> {source: data}, each file's YAML with `path`
    load_house()       -> the same for the vote for Representative (elections/readings/districts-house/)
    house_problems(d)  -> problems(d), and the seats at large (`al`) held to the years and fields
    figures(data)      -> {(st, d): {year: {"t", "D", "R", "p"}}}: the district rows (0 the State column, or the at-large
                          State's one column), a cell "fn" or "na" left as it is (and "A", where the volume's `fields`
                          name the third party's column: the 1973 Data Book's American Independent Party)
    problems(data)     -> [(where, message)]: every way a file's figures fail to add

STYLE
 1. A district row is {year: [t, D, R]} or [t, D, R, p] (p, the printed percent for the majority party, where the
    volume prints one); `fn` a footnote mark in place of a figure ("Not available" and the like), `na` "n.a." (not available),
    `nil` dots or a blank (nothing: no vote there that year, counted as zero).
 4. `suspect` ("district year"): figures the page prints that cannot be right (a row repeating another year's); held
    to nothing and never used. A printed percent within 0.1 of the figures' is no warning (the volumes truncate).
 2. What must add: in each State, the districts' t, D and R to the State column's, year by year (the State total plus
    `adjust` where the footnote gives the votes not distributed; no check for a `footnoted` item, nor for a year with
    a district `fn` or `na`, the State column then counting votes no row shows); every State's D and R to the printed
    United States figures (`us`); D + R not over t (unless `printed` says the page prints it so); p within 0.05 of
    the larger of D and R over t (a warning: a printed percent is not used).
 3. A district the volume combines with another (`combined`: Texas's 8th and 22d before 1958) counts as zero in the
    sums: its figures stand under the other.
 5. A volume's cells follow its `fields` (default [t, D, R, p]; the 1973 Data Book [t, D, R, A, p], A the American
    Independent Party's vote, item 16): every field but p is held to the State column, and D + R + A not over t.
 6. `as_printed: ["year field"]`: a State column that the districts do not make and no footnote explains, each figure
    read again by eye off the page (Michigan's 1968 total, 2 over its districts): not held. `us_holds: false`: the
    volume's United States figures are not the States' sum (the 1973 Data Book prints no District of Columbia column,
    and its U.S. figures are not the States' plus the District's): recorded, not held (`us_note` says by how much).
"""
import glob
import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR = os.path.join(ROOT, "elections", "readings", "districts")
HOUSE = os.path.join(ROOT, "elections", "readings", "districts-house")
FIELDS = ("t", "D", "R", "p")


def fields(data):
    return tuple(data.get("fields") or FIELDS)


def load(where=None):
    out = {}
    for f in sorted(glob.glob(os.path.join(where or DIR, "*.yaml"))):
        d = yaml.safe_load(open(f, encoding="utf-8")) or {}
        d["path"] = os.path.relpath(f, ROOT)
        out[d.get("source") or os.path.basename(f)[:-5]] = d
    return out


def load_house():
    """The vote for Representative by district, as the same volumes print it (elections/readings/districts-house/;
    the same schema, `al` the seats at large apart from the districts): {source: data}, as load()."""
    return load(HOUSE)


def house_problems(data):
    """problems(data), and the seats at large (`al`: {seat: {year: cell}}) held to the volume's years and fields."""
    out = problems(data)
    years = sorted(int(y) for y in data.get("years") or [])
    for st, e in (data.get("states") or {}).items():
        for seat, r in (e.get("al") or {}).items():
            if sorted(int(y) for y in r) != years or any(len(c) not in (len(fields(data)), len(fields(data)) - 1)
                                                         for c in r.values()):
                out.append((data.get("path", "?"), f"{st} at large {seat}: not {list(fields(data))} for each of {years}"))
                continue
            for y, c in r.items():
                c = dict(zip(fields(data), c))
                parts = [c.get(f) for f in fields(data) if f not in ("t", "p")]
                if _num(c.get("t")) and all(_num(x) for x in parts) and sum(parts) > c["t"]:
                    out.append((data.get("path", "?"), f"{st} at large {seat} {y}: the parties exceed the total"))
    return out


def inputs_hash():
    """A hash of everything tools/elections/make_pvi.py reads for the districts: the readings, the scripts, the
    presidential returns, the rosters and the shapes. The generated files carry it; `check` recomputes it."""
    import hashlib
    h = hashlib.sha256()
    files = sorted(glob.glob(os.path.join(DIR, "*.yaml"))) + \
        [os.path.join(ROOT, "tools", "elections", f) for f in ("make_pvi.py", "cd_readings.py")] + \
        sorted(glob.glob(os.path.join(ROOT, "elections", "19[5-7][0-9].yaml"))) + \
        sorted(glob.glob(os.path.join(ROOT, "congress", "[0-9][0-9].yaml"))) + [os.path.join(ROOT, "congress", "geo.json")]
    for f in files:
        if os.path.exists(f):
            h.update(os.path.relpath(f, ROOT).encode())
            h.update(open(f, "rb").read())
    return h.hexdigest()[:16]


def figures(data):
    """{(st, d): {year: {field: value}}}."""
    out = {}
    for st, e in (data.get("states") or {}).items():
        for d, row in (e.get("d") or {}).items():
            out[(st, int(d))] = {int(y): dict(zip(fields(data), cell)) for y, cell in row.items()}
    return out


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def problems(data):
    out = []
    where = data.get("path", "?")
    years = [int(y) for y in data.get("years") or []]
    us = data.get("us") or {}
    fl = fields(data)
    summed = [f for f in fl if f != "p"]
    sums = {}
    for st, e in (data.get("states") or {}).items():
        rows = {int(d): {int(y): c for y, c in r.items()} for d, r in (e.get("d") or {}).items()}
        bad = [d for d, r in rows.items() if sorted(r) != sorted(years) or
               any(len(c) not in (len(fl), len(fl) - 1) for c in r.values())]
        if bad:
            out.append((where, f"{st}: rows {bad} are not {list(fl)} for each of {years}"))
            continue
        comb = set(e.get("combined") or [])
        for y in years:
            for i, f in enumerate(summed):
                item = f"{y} {f}"
                cells = {d: r[y][i] for d, r in rows.items()}
                if 0 in cells and _num(cells[0]):
                    sums[(y, f)] = sums.get((y, f), 0) + cells[0]
                ds = {d: v for d, v in cells.items() if d}
                if not ds or not _num(cells.get(0)) or item in (e.get("footnoted") or []) + (e.get("as_printed") or []):
                    continue
                if any(v in ("fn", "na") and d not in comb for d, v in ds.items()):
                    continue
                s = sum(v for v in ds.values() if _num(v)) + (e.get("adjust") or {}).get(item, 0)
                if s != cells[0]:
                    out.append((where, f"{st} {item}: the districts add to {s:,}; the State column prints {cells[0]:,}"))
            for d, r in rows.items():
                c = dict(zip(fl, r[y]))
                parts = [c.get(f) for f in summed[1:]]
                t = c.get("t")
                if _num(t) and all(_num(x) for x in parts) and sum(parts) > t and f"{d} {y}" not in (e.get("over") or []):
                    out.append((where, f"{st} {d} {y}: {', '.join(summed[1:])} ({', '.join(f'{x:,}' for x in parts)}) "
                                       f"exceed the total ({t:,})"))
    if data.get("us_holds") is False:
        return out
    for (y, f), v in sums.items():
        want = us.get(f"{f}{str(y)[2:]}")
        if want is not None and f in ("D", "R") and v != want:
            out.append((where, f"{y} {f}: the States add to {v:,}; the United States column prints {want:,}"))
    return out


def warnings(data):
    """The printed percents that do not follow from the figures (not used)."""
    out = []
    for st, e in (data.get("states") or {}).items():
        for d, r in (e.get("d") or {}).items():
            for y, c in r.items():
                c = dict(zip(fields(data), c))
                if "p" not in c:
                    continue
                t, p = c["t"], c["p"]
                parties = [c[f] for f in fields(data) if f not in ("t", "p")]
                if all(_num(x) for x in [t, p] + parties) and t and abs(100 * max(parties) / t - p) > 0.11 \
                        and f"{d} {y}" not in (e.get("percent_as_printed") or []):
                    out.append((data.get("path"), f"{st} {d} {y}: printed percent {p}; the figures give "
                                                  f"{100 * max(parties) / t:.1f}"))
    return out
