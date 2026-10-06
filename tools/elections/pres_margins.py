"""Every contested race for presidential electors, 1824-2024, by constituency: elections/pres-margins.csv.

The Margin view's quantile rule (templates/congress.html, QM) reads this file at build time: a race's darkness
is the share of these races decided by a smaller margin.

    python3 tools/elections/pres_margins.py --cache DIR     (needs the network, pandas and lxml; the build does not)

Constituencies: the States and D.C.; Maine's and Nebraska's districts since 1972 and 1992; the district
systems of 1828 (Maine, Maryland, New York, Tennessee), 1832 (Maryland) and 1892 (Michigan), whose statewide
sums are dropped where every elector was chosen by district. Left out: electors chosen by legislatures, and
races with one slate. Margin: the leader's votes less the runner-up's, in points of all the votes cast.

Sources: Wikipedia's results-by-state table on each "<year> United States presidential election" page (the
article pages; the API is rate-limited); 1956-1972 from the series' own returns (elections/<year>.yaml), which
replace Wikipedia's statewide rows. Wikipedia's 1960 Alabama row counts the Democratic slate twice (as Kennedy
and as unpledged); ours counts it once.
"""
import argparse
import csv
import io
import os
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
OUT = os.path.join(ROOT, "elections", "pres-margins.csv")
UA = "bib-margins/1.0 (https://github.com/Impending2223/bib)"
YEARS = range(1824, 2025, 4)
# district-system States whose statewide row is only a sum
SUMS = {(1828, "NY"), (1828, "MD"), (1828, "TN"), (1832, "MD"), (1892, "MI")}
ABBR = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
        "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "D.C.": "DC", "D. C.": "DC",
        "Washington, D.C.": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
        "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME",
        "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
        "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
        "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
        "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
        "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI",
        "Wyoming": "WY"}
VOTES = re.compile(r"\|\s*(#|Votes?|votes?|Votes cast)\s*$")


def fetch(year, cache):
    path = os.path.join(cache, f"{year}.html")
    if not os.path.exists(path):
        url = f"https://en.wikipedia.org/wiki/{year}_United_States_presidential_election"
        for i in range(6):
            try:
                body = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
                break
            except urllib.error.HTTPError as e:
                if e.code != 429:
                    raise
                time.sleep(5 * (i + 1))
        open(path, "wb").write(body)
        time.sleep(0.5)
    return open(path, encoding="utf-8").read()


def num(x):
    s = re.sub(r"\[.*?\]", "", str(x)).replace(",", "").replace("−", "-").replace("–", "").strip()
    try:
        return float(s)
    except ValueError:
        return None


def label(c):
    return " | ".join(map(str, c)) if isinstance(c, tuple) else str(c)


def table(html):
    """The results-by-state table: the longest with a State or Total column and two or more vote columns."""
    import pandas as pd
    html = re.sub(r'(row|col)span="[^"0-9]*"', "", html)
    best = None
    for t in pd.read_html(io.StringIO(html)):
        cols = [label(c) for c in t.columns]
        if (len(t) >= 10 and any(re.search(r"\b(State|Total)\b", c) for c in cols)
                and sum(bool(VOTES.search(c)) for c in cols) >= 2 and (best is None or len(t) > len(best))):
            best = t
    return best


def unit(name):
    """(State, district or None) for a row label: 'Maine-2', "NE-2Tooltip ...", "Maine's 1st", 'New York'."""
    n = re.sub(r"Tooltip.*$", "", name).replace("†", "").replace("*", "").strip()
    m = re.match(r"^([A-Z]{2})-(\d+)$", n) or re.match(r"^([A-Za-z .]+?)(?:-|'s )(\d+|1st|2nd|3rd|[A-Z][\w &]+)$", n)
    if m:
        st = m.group(1) if len(m.group(1)) == 2 else ABBR.get(m.group(1).strip())
        return (st, re.sub(r"(st|nd|rd)$", "", m.group(2))) if st else (None, None)
    return ABBR.get(n), None


def wiki_rows(year, html):
    t = table(html)
    cols = [label(c) for c in t.columns]
    top = [c.split(" | ")[-2] if " | " in c else c for c in cols]
    vote = [i for i, c in enumerate(cols) if VOTES.search(c) and not re.search(r"margin|total|swing|state", top[i], re.I)
            and not top[i].startswith("Unnamed")]
    tot = next((i for i, c in enumerate(cols) if re.search(r"total", c, re.I)), None)
    for _, r in t.iterrows():
        st, d = unit(re.sub(r"\[.*?\]", "", str(r.iloc[0])).strip())
        if not st or (d is None and (year, st) in SUMS):
            continue
        vs = sorted([v for v in (num(r.iloc[i]) for i in vote) if v and v > 0], reverse=True)
        if len(vs) < 2:
            continue
        total = num(r.iloc[tot]) if tot is not None else None
        if not total or total < vs[0]:
            total = sum(vs)
        yield {"year": year, "st": st, "d": d or "", "margin": round(100 * (vs[0] - vs[1]) / total, 2), "src": "wikipedia"}


def ours():
    from bib import elections as E
    data, out = E.load(), {}
    for y, e in data.items():
        for r in (e.get("president") or {}).get("states", []):
            m = E.pmetrics(r)
            if m.get("margin_pts") is not None:
                out[(y, r["st"])] = m["margin_pts"]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache", default="/tmp/pres-margins", help="where to keep the fetched pages")
    a = ap.parse_args()
    os.makedirs(a.cache, exist_ok=True)
    mine, rows = ours(), []
    for y in YEARS:
        rs = list(wiki_rows(y, fetch(y, a.cache)))
        for r in rs:
            if not r["d"] and (y, r["st"]) in mine:
                r["margin"], r["src"] = mine[(y, r["st"])], "series"
        have = {r["st"] for r in rs if not r["d"]}
        rs += [{"year": y, "st": st, "d": "", "margin": v, "src": "series"} for (yy, st), v in mine.items() if yy == y and st not in have]
        rows += rs
        print(y, len(rs))
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["year", "st", "d", "margin", "src"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} races -> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
