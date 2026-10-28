"""The presidential vote by congressional district, as read off the Census's Data Books: elections/readings/districts/.

A reading file a volume (its header the schema; cdb-1961.yaml the first). Loaded and held here, for
tools/elections/make_pvi.py (which refuses figures that do not add) and tools/bib/pvi.py (`check`).

    load()             -> {source: data}, each file's YAML with `path`
    figures(data)      -> {(st, d): {year: {"t", "D", "R", "p"}}}: the district rows (0 the State column, or the at-large
                          State's one column), a cell "fn" or "na" left as it is
    problems(data)     -> [(where, message)]: every way a file's figures fail to add

STYLE
 1. A district row is {year: [t, D, R]} or [t, D, R, p] (p, the printed percent for the majority party, where the
    volume prints one); `fn` a footnote mark in place of a figure ("Not available" and the like), `na` "n.a." (not available),
    `nil` dots or a blank (nothing: no vote there that year, counted as zero).
 2. What must add: in each State, the districts' t, D and R to the State column's, year by year (the State total plus
    `adjust` where the footnote gives the votes not distributed; no check for a `footnoted` item, nor for a year with
    a district `fn` or `na`, the State column then counting votes no row shows); every State's D and R to the printed
    United States figures (`us`); D + R not over t (unless `printed` says the page prints it so); p within 0.05 of
    the larger of D and R over t (a warning: a printed percent is not used).
 3. A district the volume combines with another (`combined`: Texas's 8th and 22d before 1958) counts as zero in the
    sums: its figures stand under the other.
"""
import glob
import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR = os.path.join(ROOT, "elections", "readings", "districts")
FIELDS = ("t", "D", "R", "p")


def load():
    out = {}
    for f in sorted(glob.glob(os.path.join(DIR, "*.yaml"))):
        d = yaml.safe_load(open(f, encoding="utf-8")) or {}
        d["path"] = os.path.relpath(f, ROOT)
        out[d.get("source") or os.path.basename(f)[:-5]] = d
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
            out[(st, int(d))] = {int(y): dict(zip(FIELDS, cell)) for y, cell in row.items()}
    return out


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def problems(data):
    out = []
    where = data.get("path", "?")
    years = [int(y) for y in data.get("years") or []]
    us = data.get("us") or {}
    sums = {}
    for st, e in (data.get("states") or {}).items():
        rows = {int(d): {int(y): c for y, c in r.items()} for d, r in (e.get("d") or {}).items()}
        bad = [d for d, r in rows.items() if sorted(r) != sorted(years) or any(len(c) not in (3, 4) for c in r.values())]
        if bad:
            out.append((where, f"{st}: rows {bad} are not [t, D, R(, p)] for each of {years}"))
            continue
        comb = set(e.get("combined") or [])
        for y in years:
            for i, f in enumerate(("t", "D", "R")):
                item = f"{y} {f}"
                cells = {d: r[y][i] for d, r in rows.items()}
                if 0 in cells and _num(cells[0]):
                    sums[(y, f)] = sums.get((y, f), 0) + cells[0]
                ds = {d: v for d, v in cells.items() if d}
                if not ds or not _num(cells.get(0)) or item in (e.get("footnoted") or []):
                    continue
                if any(v in ("fn", "na") and d not in comb for d, v in ds.items()):
                    continue
                s = sum(v for v in ds.values() if _num(v)) + (e.get("adjust") or {}).get(item, 0)
                if s != cells[0]:
                    out.append((where, f"{st} {item}: the districts add to {s:,}; the State column prints {cells[0]:,}"))
            for d, r in rows.items():
                t, dv, rv = r[y][:3]
                if _num(t) and _num(dv) and _num(rv) and dv + rv > t and f"{d} {y}" not in (e.get("over") or []):
                    out.append((where, f"{st} {d} {y}: D and R ({dv:,} and {rv:,}) exceed the total ({t:,})"))
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
                if len(c) < 4:
                    continue
                t, dv, rv, p = c
                if all(_num(x) for x in (t, dv, rv, p)) and t and abs(100 * max(dv, rv) / t - p) > 0.051 \
                        and f"{d} {y}" not in (e.get("percent_as_printed") or []):
                    out.append((data.get("path"), f"{st} {d} {y}: printed percent {p}; the figures give "
                                                  f"{100 * max(dv, rv) / t:.1f}"))
    return out
