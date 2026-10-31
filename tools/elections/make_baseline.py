"""The baseline each House candidate ran against (the owner's request, Oct. 30-31, 2026: PVI's "primary use is to set
that baseline"; then, the national House vote misspecified before reapportionment, by the uncontested seats and by
turnout, "calculating the swing against prior Congressional results in each election-day district ... and then taking
the mean"; "Run the numbers twice, once with [the incumbency term], and once without").

    python3 -I tools/elections/make_baseline.py [--print]      writes elections/baseline.yaml (generated; never edit)

The specification is Gelman and King's ("Estimating Incumbency Advantage without Bias", 34 Am. J. Pol. Sci. 1142
(1990); recalled, not read: Check), a year at a time, over the contested seats with a lagged vote:

    with incumbency      v = a + b v_lag + d P + psi I + e
    without              v = a + b v_lag + d P + e

v the Democratic share of the two-party House vote, v_lag the seat's share at the last election, P the party holding
the seat, I the incumbent running. The residual e, in points of the two-party vote, is the race's figure: how far the
Democrat ran ahead (+) of the seat's baseline or behind it (-); the Republican's is its negative. Beside the models, the
mean swing (v - v_lag over the same seats, unweighted: each district one), the owner's first construct.

STYLE
 1. The share: D / (D + R), the votes of the candidates the returns mark D and R (a fusion candidate's total as the
    Clerk prints it). Contested: both above zero. Specials and races for several seats at large are not taken.
 2. The lag: the seat's share at the election before, on the same lines. Where the seat's shape is the same in both
    Congresses (congress/geo.json, the key make_pvi.py uses), the Clerk's returns of that election (elections/<y-2>.yaml);
    else the Census's retabulation of the earlier House vote onto the current lines, where read
    (elections/readings/districts-house/, its year y-2), or onto another Congress's lines where the seat's shape is
    the same in both (the 92d's retabulation of 1966 serves a 1968 race whose district the 1970 lines kept); else none. The lag's source is kept a race.
 3. I: +1 where a Democratic incumbent of the seat runs in it, -1 a Republican, the sum where two run (a merged seat);
    0 an open seat. Running: the returns' `inc` result "Incumbent re-elected" or "Incumbent lost re-election".
 4. P: the party holding the seat before the election: the incumbents' (+1 D, -1 R, summed and signed), else, for an
    open or new seat, the lag's winner.
 5. Least squares, each year apart; the coefficients, n, R squared and the residuals' standard deviation, in points.
    A year with fewer than 30 seats is not fitted.
"""
import json
import os
import re
import sys

import numpy as np
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "elections", "baseline.yaml")
HOUSE_DIR = os.path.join(ROOT, "elections", "readings", "districts-house")
RUNS = re.compile(r"^Incumbent (re-elected|lost re-election)")
YEARS = range(1958, 1976, 2)


def congress_of(year):
    return 87 + (year - 1960) // 2


def returns(year):
    p = os.path.join(ROOT, "elections", f"{year}.yaml")
    if not os.path.exists(p):
        return {}
    out = {}
    for r in yaml.safe_load(open(p, encoding="utf-8"))["races"]:
        if r["ch"] != "h" or r.get("special") or (r.get("seats") or 1) != 1:
            continue
        dv = sum(c.get("v") or 0 for c in r["cands"] if c.get("p") == "D")
        rv = sum(c.get("v") or 0 for c in r["cands"] if c.get("p") == "R")
        win = next((c.get("p") for c in r["cands"] if c.get("w")), None)
        inc_p = [i.get("p") for i in r.get("inc") or []]
        running = [i.get("p") for i in r.get("inc") or [] if RUNS.match(i.get("result") or "")]
        out[(r["st"], int(r["seat"]))] = {"D": dv, "R": rv, "win": win, "inc": inc_p, "running": running,
                                         "cand": {c.get("p"): c.get("n") for c in r["cands"] if c.get("p") in ("D", "R")}}
    return out


def sign(ps):
    s = sum(1 if p == "D" else -1 if p == "R" else 0 for p in ps)
    return (s > 0) - (s < 0)


def retabulated():
    """{(lines, year): {(st, d): (D, R, source)}} from the Census's House readings, where read."""
    out = {}
    if not os.path.isdir(HOUSE_DIR):
        return out
    sys.path.insert(0, os.path.join(ROOT, "tools", "elections"))
    import cd_readings
    for f in sorted(os.listdir(HOUSE_DIR)):
        if not f.endswith(".yaml"):
            continue
        d = yaml.safe_load(open(os.path.join(HOUSE_DIR, f), encoding="utf-8")) or {}
        if not d.get("recomputed") and d.get("lines") is None:
            continue
        figs = cd_readings.figures(d)
        for (st, dist), years in figs.items():
            for y, cell in years.items():
                D, R = cell.get("D"), cell.get("R")
                if isinstance(D, (int, float)) and isinstance(R, (int, float)):
                    out.setdefault((d["lines"], int(y)), {})[(st, int(dist))] = (D, R, d.get("source") or f[:-5])
    return out


def fit(X, y):
    X, y = np.asarray(X, float), np.asarray(y, float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    r2 = 1 - (res @ res) / (((y - y.mean()) ** 2).sum() or 1)
    return beta, res, r2


def main():
    geo = json.load(open(os.path.join(ROOT, "congress", "geo.json"), encoding="utf-8"))["congress"]

    def shape(c, st, d):
        return (geo.get(str(c)) or {}).get(st, {}).get(str(d))

    retab = retabulated()
    out = {"generated_by": "tools/elections/make_baseline.py", "years": {}}
    for y in YEARS:
        now, before = returns(y), returns(y - 2)
        if not now:
            continue
        c = congress_of(y)
        rows = []
        for (st, d), r in sorted(now.items()):
            if not (r["D"] > 0 and r["R"] > 0):
                continue
            lag = src = None
            if shape(c, st, d) and shape(c, st, d) == shape(c - 1, st, d) and (st, d) in before:
                b = before[(st, d)]
                if b["D"] > 0 and b["R"] > 0:
                    lag, src = b["D"] / (b["D"] + b["R"]), f"elections/{y - 2}.yaml"
                    lag_win = b["win"]
            else:
                for (L, yr), cells in sorted(retab.items(), key=lambda kv: (kv[0][0] != c, abs(kv[0][0] - c))):
                    if yr != y - 2 or (st, d) not in cells:
                        continue
                    if L != c and not (shape(c, st, d) and shape(c, st, d) == shape(L, st, d)):
                        continue
                    D, R, s = cells[(st, d)]
                    if D > 0 and R > 0:
                        lag, src = D / (D + R), f"readings: {s}"
                        lag_win = "D" if D > R else "R"
                    break
            if lag is None:
                continue
            I = sign(r["running"]) if len(r["running"]) == 1 else sum(1 if p == "D" else -1 for p in r["running"])
            P = sign(r["inc"]) if r["inc"] else (1 if lag_win == "D" else -1)
            rows.append({"st": st, "d": d, "v": r["D"] / (r["D"] + r["R"]), "lag": lag, "lag_src": src, "I": I, "P": P,
                         "D": r["cand"].get("D"), "R": r["cand"].get("R")})
        if len(rows) < 30:
            continue
        v = [x["v"] for x in rows]
        Xw = [[1, x["lag"], x["P"], x["I"]] for x in rows]
        Xo = [[1, x["lag"], x["P"]] for x in rows]
        bw, rw, r2w = fit(Xw, v)
        bo, ro, r2o = fit(Xo, v)
        swing = float(np.mean([x["v"] - x["lag"] for x in rows]))
        for x, e1, e2 in zip(rows, rw, ro):
            x["with"] = round(float(e1) * 100, 1)
            x["without"] = round(float(e2) * 100, 1)
            x["v"] = round(x["v"] * 100, 1)
            x["lag"] = round(x["lag"] * 100, 1)
        out["years"][y] = {
            "n": len(rows),
            "lag_sources": {s: sum(1 for x in rows if x["lag_src"] == s) for s in sorted({x["lag_src"] for x in rows})},
            "mean_swing": round(swing * 100, 2),
            "with": {"a": round(float(bw[0]), 4), "b": round(float(bw[1]), 4), "delta": round(float(bw[2]) * 100, 2),
                     "psi": round(float(bw[3]) * 100, 2), "r2": round(float(r2w), 3),
                     "sd": round(float(np.std(rw, ddof=4)) * 100, 2)},
            "without": {"a": round(float(bo[0]), 4), "b": round(float(bo[1]), 4), "delta": round(float(bo[2]) * 100, 2),
                        "r2": round(float(r2o), 3), "sd": round(float(np.std(ro, ddof=3)) * 100, 2)},
            "races": rows,
        }
    header = ("The baseline each House candidate ran against: Gelman and King's regression, a year at a time, with and "
              "without the incumbency term (tools/elections/make_baseline.py, its STYLE). Generated; never edit. "
              "Shares and residuals in points of the two-party vote; delta and psi in points.")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("# " + header + "\n")
        yaml.safe_dump(out, f, sort_keys=False, allow_unicode=True, width=120)
    if "--print" in sys.argv:
        print(f"{'year':>4} {'n':>4} {'swing':>6} | with: {'b':>5} {'delta':>6} {'psi':>5} {'R2':>5} {'sd':>5}"
              f" | without: {'b':>5} {'delta':>6} {'R2':>5} {'sd':>5}")
        for y, Y in out["years"].items():
            w, o = Y["with"], Y["without"]
            print(f"{y:>4} {Y['n']:>4} {Y['mean_swing']:>6} | {w['b']:>11} {w['delta']:>6} {w['psi']:>5} {w['r2']:>5}"
                  f" {w['sd']:>5} | {o['b']:>14} {o['delta']:>6} {o['r2']:>5} {o['sd']:>5}")


if __name__ == "__main__":
    main()
