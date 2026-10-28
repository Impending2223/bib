"""Each State's partisan voting index (PVI) for the elections of 1962-1974: elections/pvi.yaml; and each congressional
district's, for the House elections of 1960-1974 whose lines the presidential vote by district can be put on:
elections/pvi-districts.yaml, with the figures it uses, elections/cd-president.yaml (all generated; never edit).

Off the shelf Oct. 28, 2026 (the owner: "If we can calculate the CD numbers, we should take the extension off the shelf");
the district level and its sources: notes/extensions/memos/pvi-districts.md. Shown by tools/bib/pvi.py.

    python3 tools/elections/make_pvi.py          (reads elections/<year>.yaml, elections/readings/districts/,
                                                  congress/<NN>.yaml and congress/geo.json; no network)

The construct (the Cook Political Report's, as it stood from 1997 to 2021): a State's two-party Republican share of
the presidential vote, averaged over the last two presidential elections, less the nation's two-party Republican share
averaged over the same two; written "R+5" or "D+3" (a point, rounded; "EVEN" under half a point). An election takes the
two presidential elections before it: 1962 and 1964 take 1956 and 1960; 1966 and 1968, 1960 and 1964; 1970 and 1972,
1964 and 1968; 1974, 1968 and 1972. (Cook has weighted the later election 3 to 1 since 2022; the 1960s are given
here by the older, even rule, the one a reader of the period's later literature meets.) 1960 would take 1952 and
1956; the series holds no 1952 returns, so 1960 has none.

STYLE
 1. Two-party share: the Democratic and Republican slates alone (elections/<year>.yaml, each slate's highest
    elector's vote, as the tables show it); the nation's from the same States' sums.
 2. A State where either party ran no slate of its own, or where an unpledged or third slate carried the State, has
    no two-party share that year (Mississippi 1960, Alabama 1964; Wallace's States, 1968): its PVI is computed from
    the other year alone where that one is sound, and carries `basis` saying so; with neither, none. Alabama's 1960
    Democratic slate counts as the Democrats' (the 1963 Data Book's note, p. 7: "6 of the 11 Democratic electors were
    not committed in advance to support the National candidate").
 3. Each row keeps the inputs: the two years' shares and the nation's, so a reader can check the arithmetic.

DISTRICTS (the presidential vote by district, read off the Census's Data Books: elections/readings/districts/, its schema
in each file's header; tools/elections/cd_readings.py loads and holds them)
 4. The construct is the States' (1-3): the district's two-party Republican share, the two presidential elections
    before the House election averaged, less the nation's averaged over the same two (the nation's from the States'
    returns, as above; 1952's, which the series holds no State returns for, the Data Book's printed U.S. figures).
    1960 takes 1952 and 1956.
 5. The lines. A House election's districts are its Congress's (1960, the 87th; 1962, the 88th; ...; 1974, the 94th:
    congress/<NN>.yaml). A source's figures are on its own Congress's lines (`lines`); they serve another Congress's
    district only where congress/geo.json gives that district the same shape in both (the swing rule of
    tools/bib/elections.py). Where the source did not recompute an earlier year's vote on its lines (`recomputed:
    false`: the 1961 Data Book), a district its note says was redrawn after that year (`redrawn`) takes no figure for
    that year.
 5a. Where several sources give a district, the one on its own Congress's lines comes first (the 88th's Data Book
    for 1962 and 1964, though the 1961 Data Book gives the unchanged districts too); the figures differ between
    volumes by their sources (America Votes or CQ), mostly by a few hundred votes (notes/extensions/memos/pvi-districts.md).
 6. A district the source does not give (a footnote "Not available", "n.a.", a cell with no figure) has no PVI from
    it; nor has a district one of whose two years is missing, except where its State had no two-party race that year
    (STYLE 2: the State's own share is None) or did not yet vote (Alaska and Hawaii before 1960): then the other year
    alone, with `basis` saying so, as for the States.
 7. A seat at large in a State that also has districts (Connecticut's, Texas's, Michigan's, Ohio's, Maryland's)
    takes the State's column; so does a State chosen wholly at large (one seat, or Alabama's eight in 1962, Hawaii's
    two, New Mexico's two: congress/geo.json's one shape for the State), counted once.
 8. Each district row keeps its inputs (the two years' shares, the source of each); every district of the Congress
    without a PVI is listed under `none` with the reason, so the counts can be read off.
 9. Refused: a source whose figures do not add (cd_readings.problems): the script stops and prints them.
10. Each State column is held against the Clerk's returns (elections/<year>.yaml, the slates by party): every
    difference is listed under the volume's `vs_clerk` in elections/cd-president.yaml ("GA 1956 D": [the volume's,
    the Clerk's]). They are the sources' (CQ, America Votes, the NRCC against the Clerk), not misreadings: a State
    column is held to its districts (cd_readings) or read by eye where a footnote says it is not their sum.
    notes/extensions/memos/pvi-districts.md gives the large ones.
11. A year whose State had no two-party race (STYLE 2) gives no district figure either: Alabama's 1964,
    Wallace's five States of 1968; Mississippi's 1960 likewise.
12. A State whose figures leave out a party line the candidate also ran on (`excludes` in the reading: New York's
    Liberal line, 1968, in the 1973 Data Book) is taken as printed, the row's `basis` saying so.
"""
import json
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cd_readings  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "elections", "pvi.yaml")
OUT_D = os.path.join(ROOT, "elections", "pvi-districts.yaml")
OUT_F = os.path.join(ROOT, "elections", "cd-president.yaml")
HOUSE = {1960: (1952, 1956), **{y: p for y, p in {1962: (1956, 1960), 1964: (1956, 1960), 1966: (1960, 1964),
                                                   1968: (1960, 1964), 1970: (1964, 1968), 1972: (1964, 1968),
                                                   1974: (1968, 1972)}.items()}}
PAIRS = {1962: (1956, 1960), 1964: (1956, 1960), 1966: (1960, 1964), 1968: (1960, 1964), 1970: (1964, 1968),
         1972: (1964, 1968), 1974: (1968, 1972)}


def shares(year):
    """Each State's two-party Republican share, or None where it has none (STYLE 2); the nation's."""
    E = yaml.safe_load(open(os.path.join(ROOT, "elections", f"{year}.yaml"), encoding="utf-8"))["president"]
    out, nd, nr = {}, 0, 0
    for s in E["states"]:
        tot = {}
        for x in s["slates"]:
            tot[x["k"]] = tot.get(x["k"], 0) + (x.get("v") or 0)
        d, r = tot.get("D", 0), tot.get("R", 0)
        top = max(tot, key=tot.get) if tot else None
        if not d or not r or top not in ("D", "R"):
            out[s["st"]] = None
            continue
        nd, nr = nd + d, nr + r
        out[s["st"]] = r / (d + r)
    return out, nr / (nd + nr)


_SLATES = {}


def slates(year):
    """{st: {party key: votes}} from elections/<year>.yaml ({} where the series holds no returns for the year)."""
    if year not in _SLATES:
        path = os.path.join(ROOT, "elections", f"{year}.yaml")
        out = {}
        if os.path.exists(path):
            for s in yaml.safe_load(open(path, encoding="utf-8"))["president"]["states"]:
                tot = {}
                for x in s["slates"]:
                    tot[x["k"]] = tot.get(x["k"], 0) + (x.get("v") or 0)
                out[s["st"]] = tot
        _SLATES[year] = out
    return _SLATES[year]


def label(v):
    if v is None:
        return None
    if abs(v) < 0.5:
        return "EVEN"
    return f"R+{round(v)}" if v > 0 else f"D+{round(-v)}"


def ordinal(n):
    return f"{n}{'st' if n % 10 == 1 and n % 100 != 11 else 'd' if n % 10 in (2, 3) and n % 100 not in (12, 13) else 'th'}"


def congress_of(year):
    return 87 + (year - 1960) // 2


def seats(c):
    """The Congress's House seats at its opening: [(st, d)], each once (two members at large are one seat here)."""
    p = os.path.join(ROOT, "congress", f"{c}.yaml")
    if not os.path.exists(p):
        return []
    out = []
    for m in yaml.safe_load(open(p, encoding="utf-8"))["house"]:
        k = (m["st"], int(m["d"]))
        if k not in out:
            out.append(k)
    return out


def districts(cache):
    """(pvi-districts, cd-president): STYLE 4-9."""
    sources = cd_readings.load()
    bad = [(w, m) for d in sources.values() for w, m in cd_readings.problems(d)]
    if bad:
        for w, m in bad:
            print(f"{w}: {m}", file=sys.stderr)
        sys.exit(f"refused: {len(bad)} figures that do not add")
    geo = json.load(open(os.path.join(ROOT, "congress", "geo.json"), encoding="utf-8"))["congress"]

    def shape(c, st, d):
        return (geo.get(str(c)) or {}).get(st, {}).get(str(d))

    figs = {k: cd_readings.figures(d) for k, d in sources.items()}
    nation = {}
    for k, d in sources.items():
        us = d.get("us") or {}
        for y in d.get("years") or []:
            dv, rv = us.get(f"D{str(y)[2:]}"), us.get(f"R{str(y)[2:]}")
            if dv and rv and y not in nation:
                nation[y] = (rv / (dv + rv), f"{k} (printed U.S. figures)")
    for y in range(1956, 1976, 4):
        if os.path.exists(os.path.join(ROOT, "elections", f"{y}.yaml")):
            if y not in cache:
                cache[y] = shares(y)
            nation[y] = (cache[y][1], f"elections/{y}.yaml")

    def figure(st, d, c, y):
        """(share, source) or (None, why)."""
        whys = []
        for k, src in sorted(sources.items(), key=lambda kv: (kv[1].get("lines") != c, abs(kv[1].get("lines") - c))):
            if y not in (src.get("years") or []):
                continue
            lines = src["lines"]
            col = d
            row = figs[k].get((st, col))
            if row is None and d == 0:
                row = figs[k].get((st, 0))
            if row is None:
                if st in (src.get("states") or {}):
                    whys.append(f"{k}: no such district on the {ordinal(lines)} Congress's lines")
                continue
            if c != lines and d != 0:
                if not shape(c, st, d) or shape(c, st, d) != shape(lines, st, d):
                    whys.append(f"{k}: lines not the {ordinal(lines)} Congress's")
                    continue
            if not src.get("recomputed") and d in ((src.get("redrawn") or {}).get(y) or {}).get(st, []):
                whys.append(f"{k}: redrawn after {y} (its note)")
                continue
            if f"{d} {y}" in ((src.get("states") or {}).get(st, {}).get("suspect") or []):
                whys.append(f"{k}: {y} suspect (as printed)")
                continue
            cell = row.get(y) or {}
            dv, rv = cell.get("D"), cell.get("R")
            if not (isinstance(dv, int) and isinstance(rv, int)) or dv + rv == 0:
                whys.append(f"{k}: {y} not given ({dv if not isinstance(dv, int) else rv})")
                continue
            return rv / (dv + rv), k
        return None, (whys[0] if whys else "no source gives the State")   # the reason of the nearest source holding it

    out = {"source": "elections/readings/districts/ (make_pvi.py, its STYLE 4-9)", "inputs": cd_readings.inputs_hash(),
           "nation": {y: {"r": round(100 * v, 2), "from": f} for y, (v, f) in sorted(nation.items())}, "elections": {}}
    for e, (a, b) in sorted(HOUSE.items()):
        c = congress_of(e)
        rows, none = {}, {}
        ss = []
        # without a roster (the 94th), the shapes: a State's "0" is its outline where it has districts too
        for st, d in seats(c) or [(st, int(d)) for st, ds in (geo.get(str(c)) or {}).items() for d in ds
                                  if d != "0" or set(ds) == {"0"}]:
            if set((geo.get(str(c)) or {}).get(st) or {}) == {"0"}:
                d = 0          # the roster numbers the seats of a State chosen wholly at large (Hawaii's two)
            if (st, d) not in ss:
                ss.append((st, d))
        for st, d in ss:
            key = f"{st}-{d if d else 'AL'}"
            if a not in nation or b not in nation:
                none[key] = f"no figures for {a if a not in nation else b} by district"
                continue
            sa, ka = figure(st, d, c, a)
            sb, kb = figure(st, d, c, b)
            state_a = cache[a][0].get(st, "x") if a in cache else "x"
            state_b = cache[b][0].get(st, "x") if b in cache else "x"
            if sa is not None and sb is not None and state_a is not None and state_b is not None:
                v, basis = 100 * ((sa + sb) / 2 - (nation[a][0] + nation[b][0]) / 2), f"{a} and {b}"
            elif sb is not None and state_b is not None and (state_a is None or (a in cache and st not in cache[a][0])):
                why = "not yet voting" if a in cache and st not in cache[a][0] else "no two-party race in the State"
                v, basis = 100 * (sb - nation[b][0]), f"{b} alone ({a}: {why})"
            elif sa is not None and state_a is not None and (state_b is None or (b in cache and st not in cache[b][0])):
                why = "not yet voting" if b in cache and st not in cache[b][0] else "no two-party race in the State"
                v, basis = 100 * (sa - nation[a][0]), f"{a} alone ({b}: {why})"
            else:
                why = [f"{y}: {w}" for y, s_, w in ((a, sa, ka), (b, sb, kb)) if s_ is None]
                why += [f"{y}: no two-party race in the State" for y, s_, x in ((a, sa, state_a), (b, sb, state_b))
                        if s_ is not None and x is None]
                none[key] = "; ".join(why)
                continue
            note = "; ".join(sorted({sources[k_]["states"][st]["excludes"] for s_, k_ in ((sa, ka), (sb, kb))
                                      if s_ is not None and (sources[k_].get("states") or {}).get(st, {}).get("excludes")}))
            if note:
                basis += f" (as printed: {note})"
            rows[key] = {"pvi": label(v), "points": round(v, 2), "basis": basis,
                         f"r{a}": None if sa is None else round(100 * sa, 2), f"r{b}": None if sb is None else round(100 * sb, 2),
                         "from": sorted({k for s_, k in ((sa, ka), (sb, kb)) if s_ is not None})}
        out["elections"][e] = {"congress": c, "from": [a, b], "computed": len(rows), "without": len(none),
                               "districts": rows, "none": none}
    fig = {"source": "elections/readings/districts/ (make_pvi.py)", "inputs": out["inputs"], "volumes": {}}
    for k, src in sources.items():
        flds = [f for f in cd_readings.fields(src) if f != "p"]
        vol = {"lines": src["lines"], "years": src["years"], "fields": flds, "vs_clerk": {}, "districts": {}}
        for (st, d), yrs in sorted(figs[k].items()):
            vol["districts"][f"{st}-{d}"] = {y: [c.get(f) for f in flds] for y, c in yrs.items()}
            for y, c in yrs.items():          # STYLE 10: each State column against the Clerk's slates
                clerk = slates(y).get(st) if d == 0 else None
                for f in ("D", "R", "A"):
                    if clerk is None or f not in c or not isinstance(c.get(f), int) or c[f] == clerk.get(f):
                        continue
                    vol["vs_clerk"][f"{st} {y} {f}"] = [c[f], clerk.get(f)]
        fig["volumes"][k] = vol
    return out, fig


def main():
    cache = {}
    out = {"source": "elections/<year>.yaml, the presidential vote by State (make_pvi.py, its STYLE)", "years": {}}
    for y, (a, b) in sorted(PAIRS.items()):
        for z in (a, b):
            if z not in cache:
                cache[z] = shares(z)
        (sa, na), (sb, nb) = cache[a], cache[b]
        rows = {}
        for st in sorted(set(sa) | set(sb)):
            xa, xb = sa.get(st), sb.get(st)
            if xa is not None and xb is not None:
                v, basis = 100 * ((xa + xb) / 2 - (na + nb) / 2), f"{a} and {b}"
            elif xa is not None or xb is not None:
                one, nat, yr = (xa, na, a) if xa is not None else (xb, nb, b)
                other = b if yr == a else a
                why = "not yet voting" if st not in (sb if other == b else sa) else "no two-party race"
                v, basis = 100 * (one - nat), f"{yr} alone ({other}: {why})"
            else:
                v, basis = None, "neither year a two-party race"
            rows[st] = {"pvi": label(v), "points": None if v is None else round(v, 2), "basis": basis,
                        f"r{a}": None if xa is None else round(100 * xa, 2),
                        f"r{b}": None if xb is None else round(100 * xb, 2)}
        out["years"][y] = {"from": [a, b], "nation": {f"r{a}": round(100 * na, 2), f"r{b}": round(100 * nb, 2)},
                           "states": rows}
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("# Generated by tools/elections/make_pvi.py from elections/<year>.yaml; never edit.\n")
        yaml.safe_dump(out, f, allow_unicode=True, sort_keys=False, width=120)
    print(f"wrote {OUT}: {len(out['years'])} election years")
    dist, fig = districts(cache)
    with open(OUT_D, "w", encoding="utf-8") as f:
        f.write("# Generated by tools/elections/make_pvi.py from elections/readings/districts/; never edit.\n")
        yaml.safe_dump(dist, f, allow_unicode=True, sort_keys=False, width=120)
    with open(OUT_F, "w", encoding="utf-8") as f:
        f.write("# Generated by tools/elections/make_pvi.py from elections/readings/districts/; never edit.\n"
                "# By volume: each district's [total, Democratic, Republican] a year, as read (0 the State column).\n")
        yaml.safe_dump(fig, f, allow_unicode=True, sort_keys=False, width=120, default_flow_style=None)
    for e, x in dist["elections"].items():
        print(f"  {e} ({ordinal(x['congress'])} Congress): {x['computed']} districts, {x['without']} without")


if __name__ == "__main__":
    sys.exit(main())
