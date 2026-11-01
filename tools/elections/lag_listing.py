"""notes/house-lags.md: every House seat's lag, seat by seat, where its district was redrawn (generated).

    python3 -I tools/elections/lag_listing.py      writes the listing (after make_baseline.py)

The baseline (make_baseline.py) needs each contested seat's vote at the election before on the seat's own lines. Where
the lines held, that is the Clerk's return for the same district: counted here, not listed. Where they did not, the
figure is a retabulation read off a page (the Census's Data Books, CQ's charts and tables): each such seat is listed
with its figure, the cell as the page prints it, the page, and Jacobson's figure for the seat beside it; and each
contested seat with no figure is listed with what the sources print for it instead.

STYLE
 1. A row: the seat; the lag as the Democratic share of the two-party vote, in points (CQ's charts: the leading
    party's percent of the total, converted as make_baseline.py STYLE 8 says, marked "≈"); the source and page; the
    cell as printed (the Census's [total, D, R]; CQ's leading party and percent; Missouri's D and R shares); marks
    (CQ's estimates, its corrections, a figure printed on old borders); Jacobson's `dvp` ("—" where he has none).
 2. A missing seat on lines that held: the earlier race had no major-party contest (or no single-seat race). A
    redrawn seat: what each reading file says of it (a rating, a registration figure, withdrawn, unmarked, a doubted
    digit, not final, "not computed"), else "no source read gives it".
 3. Generated, never edited; the first line carries a hash of its inputs.
"""
import glob
import hashlib
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "notes", "house-lags.md")
HOUSE = os.path.join(ROOT, "elections", "readings", "districts-house")
sys.path.insert(0, os.path.join(ROOT, "tools", "elections"))

LABEL = {"cdh-1963": "Census, CDD 1963 (88th Cong.)", "cdh-1965": "Census, CDD Supps. 1-7 (1965)",
         "cdh-1966s": "Census, CDD Supps. 8-32 (1966-67)", "cdh-1971": "Census, CDD-92 (1971)",
         "cdh-1973": "Census, CDD 93d Cong. (1973)", "cdh-1974": "Census, CDD-94 (1974)",
         "cq-1962": "CQ Weekly Rep., supp., May 4, 1962", "cq-1964": "CQ Weekly Rep. no. 46, Nov. 13, 1964",
         "cq-1966": "CQ Weekly Rep. no. 29, July 22, 1966", "cq-1968": "CQ Weekly Rep. no. 30, pt. 2, July 26, 1968"}


def files():
    out = {}
    for f in sorted(glob.glob(os.path.join(HOUSE, "*.yaml"))):
        d = yaml.safe_load(open(f, encoding="utf-8")) or {}
        out[d.get("source") or os.path.basename(f)[:-5]] = d
    return out


def inputs_hash():
    h = hashlib.sha256()
    for f in sorted(glob.glob(os.path.join(HOUSE, "*.yaml"))) + [os.path.join(ROOT, "elections", "baseline.yaml"),
                                                                 os.path.abspath(__file__)]:
        h.update(open(f, "rb").read())
    return h.hexdigest()[:12]


def seat(st, d):
    return f"{st}-{d or 'AL'}"


def page_of(e, d):
    if e.get("page"):
        return f"p. {e['page']}"
    for p, ds in (e.get("pages") or {}).items():
        if d in ds:
            return f"PDF p. {p}"
    return ""


def cell_of(src, data, st, d, y):
    e = (data.get("states") or {}).get(st) or {}
    row = ((e.get("d") or {}).get(d) or {}).get(y) or ((e.get("d") or {}).get(str(d)) or {}).get(y)
    marks = []
    cor = e.get("corrected") or {}
    cd = (cor.get("d") if isinstance(cor.get("d"), dict) else cor) or {}
    if d in cd or str(d) in cd:
        c = cd.get(d) or cd.get(str(d))
        marks.append(f"corrected to {c[0]} {c[1]} ({cor.get('cite', 'CQ')})")
    if d in (e.get("old") or []):
        marks.append("old borders")
    if f"{d} {y}" in (e.get("estimated") or []) or d in ((cor.get("estimated") if isinstance(cor, dict) else None) or []):
        marks.append("estimated")
    fields = data.get("fields") or ["t", "D", "R", "p"]
    if row is None:
        shown = "—"
    elif "party" in fields:
        shown = f"{row[0]} {row[1]} of the total"
    elif data.get("shares"):
        shown = f"D {row[0]}, R {row[1]}"
    else:
        shown = ", ".join(f"{k} {v:,}" if isinstance(v, int) else f"{k} {v}" for k, v in zip(fields, row) if k != "p")
    return shown, page_of(e, d), marks


def why_missing(fs, st, d, y):
    out = []
    for src, data in fs.items():
        if y not in (data.get("years") or []):
            continue
        e = (data.get("states") or {}).get(st)
        nf = (data.get("not_final") or {}).get(st)
        if nf:
            out.append(f"{LABEL.get(src, src)}: not final ({nf})")
        if not e:
            continue
        for k, say in (("rating", None), ("registration", "registration only"), ("special", "a special only")):
            v = (e.get(k) or {}).get(d)
            if v is not None:
                out.append(f"{LABEL.get(src, src)}, {page_of(e, d) or ''}: " + (say + f" ({v})" if say else str(v)))
        for k, say in (("withdrawn", "withdrawn by CQ's correction"), ("unmarked", "printed unmarked (held out)"),
                       ("unopposed", "no major-party contest")):
            if d in (e.get(k) or []):
                out.append(f"{LABEL.get(src, src)}: {say}")
        for k in ("doubt", "party_doubt"):
            if f"{d} {y}" in (e.get(k) or []):
                out.append(f"{LABEL.get(src, src)}: a doubted {'digit' if k == 'doubt' else 'party'} (held out)")
        r = ((e.get("d") or {}).get(d) or {}).get(y)
        if r is not None and "party" in (data.get("fields") or []) and isinstance(r[1], (int, float)) and r[1] <= 50:
            out.append(f"{LABEL.get(src, src)}: {r[0]} {r[1]}, a plurality (held out)")
    return "; ".join(out) or "no source read gives it"


def main():
    import make_baseline
    import json
    fs = files()
    geo = json.load(open(os.path.join(ROOT, "congress", "geo.json"), encoding="utf-8"))["congress"]
    B = (yaml.safe_load(open(os.path.join(ROOT, "elections", "baseline.yaml"), encoding="utf-8")) or {})["years"]
    L = [f"<!-- generated by tools/elections/lag_listing.py; inputs {inputs_hash()}; never edit -->",
         "# The House lags, seat by seat",
         "",
         "Each contested House race's Democratic share of the two-party vote at the election before, on the race's own",
         "lines (`elections/baseline.yaml`, the `census` lag). Where the lines held, the Clerk's return: counted, not",
         "listed. Where they did not, the figure read off a page: listed with the cell as printed and its page, and",
         "Jacobson's figure beside it. CQ's charts give the leading party's percent of the total vote: converted to a",
         "two-party share by taking the rest as the other party's (≈). The rules: `tools/elections/lag_listing.py`.",
         ""]
    for y in range(1962, 1976, 2):
        if y not in B:
            continue
        races = {(r["st"], r["d"]): r for r in B[y]["races"]}
        contested = {k: v for k, v in make_baseline.returns(y).items() if v["D"] > 0 and v["R"] > 0}
        same = [k for k, r in races.items() if (r.get("census") or {}).get("src", "").startswith("elections/")]
        read = sorted(k for k, r in races.items() if (r.get("census") or {}).get("src", "").startswith("readings:"))
        miss = sorted(k for k in contested if not (races.get(k) or {}).get("census"))
        before = make_baseline.returns(y - 2)
        c = make_baseline.congress_of(y)
        held = lambda st, d: geo.get(str(c), {}).get(st, {}).get(str(d)) and \
            geo.get(str(c), {}).get(st, {}).get(str(d)) == geo.get(str(c - 1), {}).get(st, {}).get(str(d))
        L += [f"## {y} (the {y - 2} vote)", "",
              f"{len(contested)} contested seats: {len(same)} on lines that held (the Clerk's {y - 2} return); "
              f"{len(read)} read off a page; {len(miss)} with no figure.", ""]
        if read:
            L += ["| Seat | Lag (D %) | Source | Page | As printed | Marks | Jacobson |", "|---|---|---|---|---|---|---|"]
            for st, d in read:
                r = races[(st, d)]
                src = r["census"]["src"].split(": ", 1)[1]
                shown, pg, marks = cell_of(src, fs.get(src, {}), st, d, y - 2)
                approx = "≈" if "party" in (fs.get(src, {}).get("fields") or []) else ""
                jv = (r.get("jacobson") or {}).get("lag")
                L.append(f"| {seat(st, d)} | {approx}{r['census']['lag']:.1f} | {LABEL.get(src, src)} | {pg} | {shown} | "
                         f"{'; '.join(marks)} | {jv if jv is not None else '—'} |")
            L.append("")
        if miss:
            L += [f"No figure ({len(miss)}):", ""]
            for st, d in miss:
                b = before.get((st, d))
                if held(st, d) and b is not None and not (b["D"] > 0 and b["R"] > 0):
                    L.append(f"- {seat(st, d)}: lines that held; the {y - 2} race had no major-party contest")
                elif held(st, d) and b is None:
                    L.append(f"- {seat(st, d)}: lines that held; no single-seat {y - 2} race in the returns")
                else:
                    L.append(f"- {seat(st, d)}: redrawn; {why_missing(fs, st, d, y - 2)}")
            L.append("")
    open(OUT, "w", encoding="utf-8").write("\n".join(L).rstrip() + "\n")
    print(OUT)


if __name__ == "__main__":
    main()
