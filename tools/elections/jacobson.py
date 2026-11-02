"""Gary C. Jacobson's district file, read and held against the series' returns (the owner, Oct. 31, 2026: keep his file;
a standing check of our House shares and lags against his; the baseline three ways; his presidential figures where no
Census volume prints the district). The file and its codebook: sources/jacobson/README.md.

    python3 -I tools/elections/jacobson.py [--write]      prints the comparison's counts; --write the listing,
                                                           notes/jacobson-compare.md (generated; never edit)

STYLE
 1. The seats. His `stcd` is the State's place in the alphabetical list of the fifty (1-50) times 100 plus the
    district. A seat at large in a State that also has districts is his n+1 (Texas's of 1962, 23); a State's only
    seat, 1. Ours: elections/<year>.yaml, `seat` 0 for a seat at large. A race for several seats at large (Alabama's
    eight of 1962, Hawaii's two, New Mexico's two) and a special are not compared.
 2. The share: ours, D / (D + R) of the votes the Clerk's returns mark D and R (make_baseline.py STYLE 1); his `dv`,
    in points, missing where a seat was unopposed. They agree where both are missing, or within half a point; else
    the seat is listed, with both figures.
 3. The lag: his `dvp`, the Democratic share at the election before; held against ours, the Clerk's returns of the
    election before for the same-numbered seat, by the same rule as 2. Where a State was redrawn his `dvp` is often
    another seat's (its predecessor, as he matched them; the codebook does not say how): where it is our share in
    one other seat of the State, within 0.15 point, and no other, that seat is named ("lags another seat's"). His `redist` (1 where the district was redrawn since the last election) is held against the series' shapes
    (congress/geo.json: the seat's shape the same in the two Congresses, make_pvi.py STYLE 5); each difference listed.
 4. His presidential figure, `dpres`: the Democratic share of the two-party presidential vote in the district, in a
    presidential year that year's, in a midterm the election's two years before; on the lines of the House election
    the row is for (the row's Congress). He gives none for the districts redrawn in 1962 and 1966 (219 and 223 of
    435 given); the 1970 and 1974 rows carry the earlier vote retabulated onto the new lines (the 1970 row agrees
    with the Census's CDD-92 to a tenth of a point in 419 of 430 districts). make_pvi.py takes it only where no
    Census volume prints the district (its STYLE 13).
 5. The listing is generated with the hash of its inputs in its first line; `check` warns when an input has changed
    since [jacobson].
"""
import csv
import hashlib
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TAB = os.path.join(ROOT, "sources", "jacobson", "JOPrepfile1.tab")
OUT = os.path.join(ROOT, "notes", "jacobson-compare.md")
GEO = os.path.join(ROOT, "congress", "geo.json")
ST = ("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA "
      "RI SC SD TN TX UT VT VA WA WV WI WY").split()
YEARS = range(1958, 1976, 2)
TOL = 0.5
_CACHE = {}


def _yaml(path):
    """The parse, through the series' cache (tools/bib/store.py, .cache/yaml) where it can be had."""
    try:
        sys.path.insert(0, ROOT)
        from tools.bib import store
        return store.load_yaml(path)
    except ImportError:
        return yaml.safe_load(open(path, encoding="utf-8"))


def congress_of(year):
    return 87 + (year - 1960) // 2


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load():
    """{(year, st, his district): {field: float or None}}, 1956-76."""
    if "j" in _CACHE:
        return _CACHE["j"]
    out = {}
    with open(TAB, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            y, s = _num(r.get("year")), _num(r.get("stcd"))
            if y is None or s is None or not 1956 <= y <= 1976:
                continue
            s = int(s)
            out[(int(y), ST[s // 100 - 1], s % 100)] = {k: _num(v) for k, v in r.items() if k not in ("year", "stcd")}
    _CACHE["j"] = out
    return out


def returns(year):
    """{(st, seat): (D, R)} of the single-seat regular House races (STYLE 1), and the seat-0 keys to leave out."""
    p = os.path.join(ROOT, "elections", f"{year}.yaml")
    if not os.path.exists(p):
        return {}, set()
    if ("r", year) in _CACHE:
        return _CACHE[("r", year)]
    out, zero = {}, {}
    for r in _yaml(p)["races"]:
        if r["ch"] != "h" or r.get("special"):
            continue
        k = (r["st"], int(r["seat"]))
        if k[1] == 0:
            zero[k[0]] = zero.get(k[0], 0) + ((r.get("seats") or 1))
        if (r.get("seats") or 1) != 1:
            continue
        dv = sum(c.get("v") or 0 for c in r["cands"] if c.get("p") == "D")
        rv = sum(c.get("v") or 0 for c in r["cands"] if c.get("p") == "R")
        out[k] = (dv, rv)
    skip = {(st, 0) for st, n in zero.items() if n > 1}
    _CACHE[("r", year)] = out, skip
    return out, skip


def his_seat(st, d, seats):
    """Our (st, d) as his district number (STYLE 1); seats, our keys that year."""
    if d:
        return d
    n = max((x for s, x in seats if s == st), default=0)
    return n + 1 if n else 1


def our_share(dr):
    if dr is None:
        return None
    D, R = dr
    return 100 * D / (D + R) if D > 0 and R > 0 else None


def dpres():
    """{(lines, presidential year): {(st, d): Democratic two-party share, points}}, numbered districts only (STYLE 4)."""
    out = {}
    for (y, st, d), r in load().items():
        if r.get("dpres") is None:
            continue
        p = y if y % 4 == 0 else y - 2
        out.setdefault((congress_of(y), p), {})[(st, d)] = r["dpres"]
    # a seat at large in a districted State (his n+1) is no district of ours: make_pvi.py gives it the State's column
    for (L, p), cells in out.items():
        n = {}
        for st, d in cells:
            n[st] = max(n.get(st, 0), d)
        y = 1960 + 2 * (L - 87)
        seats, _ = returns(y)
        for st in list(n):
            if (st, 0) in seats:
                cells.pop((st, n[st]), None)
                if not any(s == st and x for s, x in seats):
                    cells.pop((st, 1), None)
    return out


def lags():
    """{year: {(st, d): his dvp in points, or None}} for the races ours holds (STYLE 3), and his redist."""
    J = load()
    out = {}
    for y in YEARS:
        seats, skip = returns(y)
        out[y] = {}
        for k in seats:
            if k in skip:
                continue
            r = J.get((y, k[0], his_seat(k[0], k[1], seats)))
            if r is not None:
                out[y][k] = (r.get("dvp"), r.get("redist"))
    return out


def inputs_hash():
    h = hashlib.sha1()
    for p in [TAB, GEO, __file__] + [os.path.join(ROOT, "elections", f"{y}.yaml") for y in range(YEARS[0] - 2, YEARS[-1] + 1, 2)]:
        if os.path.exists(p):
            with open(p, "rb") as f:
                h.update(f.read())
    return h.hexdigest()[:12]


def compare():
    """{year: {"share": [...], "lag": [...], "redist": [...], "counts": {...}}}."""
    J = load()
    geo = json.load(open(GEO, encoding="utf-8"))["congress"]

    def shape(c, st, d):
        return (geo.get(str(c)) or {}).get(st, {}).get(str(d))
    out = {}
    for y in YEARS:
        now, skip = returns(y)
        before, _ = returns(y - 2)
        c = congress_of(y)
        res = {"share": [], "lag": [], "pred": [], "redist": [], "counts": {"seats": 0, "his": 0, "share_ok": 0, "lag_ok": 0}}
        mine = set()
        for k in sorted(now):
            if k in skip:
                continue
            st, d = k
            hd = his_seat(st, d, now)
            mine.add((st, hd))
            res["counts"]["seats"] += 1
            r = J.get((y, st, hd))
            if r is None:
                res["share"].append((st, d, our_share(now[k]), "no row"))
                continue
            res["counts"]["his"] += 1
            a, b = our_share(now[k]), r.get("dv")
            if (a is None and b is None) or (a is not None and b is not None and abs(a - b) <= TOL):
                res["counts"]["share_ok"] += 1
            else:
                res["share"].append((st, d, a, b))
            la, lb = our_share(before.get((st, d))), r.get("dvp")
            if (la is None and lb is None) or (la is not None and lb is not None and abs(la - lb) <= TOL):
                res["counts"]["lag_ok"] += 1
            else:
                pred = [x for (s2, x), dr in sorted(before.items()) if s2 == st and x != d and lb is not None
                        and our_share(dr) is not None and abs(our_share(dr) - lb) <= 0.15]
                if len(pred) == 1:
                    res["pred"].append((st, d, pred[0], lb))
                else:
                    res["lag"].append((st, d, la, lb))
            same = bool(shape(c, st, d)) and shape(c, st, d) == shape(c - 1, st, d)
            if r.get("redist") is not None and (r["redist"] == 0) != same:
                res["redist"].append((st, d, int(r["redist"]), "same" if same else "changed"))
        res["his_only"] = sorted(f"{st}-{d}" for (yy, st, d) in J if yy == y and (st, d) not in mine)
        out[y] = res
    return out


def _f(x):
    return "—" if x is None else (x if isinstance(x, str) else f"{x:.1f}")


def listing(cmp=None):
    cmp = cmp or compare()
    L = [f"<!-- generated by tools/elections/jacobson.py --write; inputs {inputs_hash()}; never edit -->",
         "# The series' House returns against Jacobson's file",
         "",
         "Gary C. Jacobson's district file (`sources/jacobson/`, its README), 1958-74, held against the series' returns",
         "(`elections/<year>.yaml`, the Clerk's) seat by seat: the Democratic share of the two-party vote (`dv`), the",
         "share at the election before in the seat of the same number (`dvp`), and whether the district was redrawn",
         "(`redist`) against the series' shapes (`congress/geo.json`). Within half a point is agreement; a seat where",
         "both have no contest agrees. The rules: `tools/elections/jacobson.py`, its STYLE. Each difference is a lead",
         "to the Clerk's page (`elections/readings/`), not a correction: the Clerk's figures stand.",
         "",
         "| Year | Seats | In his file | Shares agree | Lags agree | Shares differ | Lags another seat's | Lags differ | Redrawn, differ |",
         "|---|---|---|---|---|---|---|---|---|"]
    for y, r in cmp.items():
        c = r["counts"]
        L.append(f"| {y} | {c['seats']} | {c['his']} | {c['share_ok']} | {c['lag_ok']} | {len(r['share'])} | "
                 f"{len(r['pred'])} | {len(r['lag'])} | {len(r['redist'])} |")
    for y, r in cmp.items():
        L += ["", f"## {y}", ""]
        if r["share"]:
            L.append("Shares (ours, his): " + "; ".join(f"{st}-{d or 'AL'} {_f(a)}, {_f(b)}" for st, d, a, b in r["share"]) + ".")
            L.append("")
        if r["lag"]:
            L.append(f"Lags, {y - 2} (ours, the same-numbered seat; his `dvp`): "
                     + "; ".join(f"{st}-{d or 'AL'} {_f(a)}, {_f(b)}" for st, d, a, b in r["lag"]) + ".")
            L.append("")
        if r["pred"]:
            L.append(f"Lags another seat's (his `dvp` is our {y - 2} share in the seat named, within 0.15 point, and in"
                     " no other of the State's): " + "; ".join(f"{st}-{d or 'AL'} from {st}-{x or 'AL'} {_f(b)}"
                                                           for st, d, x, b in r["pred"]) + ".")
            L.append("")
        if r["redist"]:
            L.append("Redrawn (his `redist`; the series' shapes): "
                     + "; ".join(f"{st}-{d or 'AL'} {v}, {s}" for st, d, v, s in r["redist"]) + ".")
            L.append("")
        if r["his_only"]:
            L.append("His rows with no single-seat race of ours (seats at large, several at once): "
                     + ", ".join(r["his_only"]) + ".")
    return "\n".join(L).rstrip() + "\n"


def problems():
    """[(level, where, message)] for ./bib check [jacobson]: the listing stale."""
    rel = os.path.relpath(OUT, ROOT)
    if not os.path.exists(TAB):
        return [("error", "sources/jacobson/JOPrepfile1.tab", "missing")]
    if not os.path.exists(OUT):
        return [("warn", rel, "not written: python3 -I tools/elections/jacobson.py --write")]
    with open(OUT, encoding="utf-8") as f:
        first = f.readline()
    if f"inputs {inputs_hash()};" not in first:
        return [("warn", rel, "stale (an input changed): python3 -I tools/elections/jacobson.py --write")]
    return []


def main():
    cmp = compare()
    for y, r in cmp.items():
        print(y, r["counts"], "share", len(r["share"]), "lag", len(r["lag"]), "redist", len(r["redist"]))
    if "--write" in sys.argv:
        with open(OUT, "w", encoding="utf-8") as f:
            f.write(listing(cmp))
        print("wrote", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
