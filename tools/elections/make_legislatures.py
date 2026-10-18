"""elections/legislatures.yaml: the party make-up of every State legislature in each session, 1959–1969, from Carl Klarner's
State Partisan Balance Data, 1937–2011 (Harvard Dataverse, doi:10.7910/DVN/LZHMG3; the seat counts compiled from the
Council of State Governments' *Book of the States* and the States' manuals). Needs the network; the build does not.

    python3 tools/elections/make_legislatures.py [--xlsx PATH]

STYLE (the file):
 1. `sessions`: by the year a session met (1961: the legislature the elections of 1960 chose, with the States that
    elected none that year as they stood), each State's Senate (`sen`) and House (`hs`): Democrats, Republicans, others,
    vacancies, total, as in session (`_in_sess`; Klarner's counts after vacancies filled); the chamber's control
    (D, R, or split); `override`, the proportion of the legislators needed to pass a bill over the governor's veto,
    and `of`, whether of those elected or those present (Klarner: the provisions of 1956, assumed for every year of
    this span); the governor's party.
 2. HAND lays over what the data cannot say: North Carolina's governor had no veto (until 1997); Minnesota's and
    Nebraska's legislators were chosen without party labels (Minnesota's caucused as Liberals and Conservatives,
    counted here as Democrats and Republicans; Nebraska's one chamber has no party count).
 3. Never edit the file by hand: fix the script and rerun.
"""
import argparse
import os
import sys
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "elections", "legislatures.yaml")
URL = "https://dataverse.harvard.edu/api/access/datafile/2432030"     # Partisan_Balance_For_Use2011_06_09b.xlsx
YEARS = range(1959, 1970)
ST = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
      "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
      "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
      "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
      "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
      "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
      "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
      "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
      "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}
HAND = {
    "NC": {"override": None, "note": "The governor had no veto (until 1997)."},
    "MN": {"note": "Elected without party labels; the Liberal caucus counted with the Democrats, the Conservative with "
                   "the Republicans."},
    "NE": {"note": "One chamber, elected without party labels."},
}
HAND_YEAR = {
    ("KS", 1967): {"check": "Klarner's House counts, 48 D and 78 R, add to 126 of the 125 seats; the Kansas directory."},
    ("KS", 1968): {"check": "Klarner's House counts, 48 D and 78 R, add to 126 of the 125 seats; the Kansas directory."},
}


def control(c):
    return {1: "D", 0: "R", 0.5: "split"}.get(c) if c is not None else None


def num(v):
    return int(v) if isinstance(v, (int, float)) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx")
    a = ap.parse_args()
    path = a.xlsx
    if not path:
        path = "/tmp/partisan_balance.xlsx"
        urllib.request.urlretrieve(URL, path)
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True).worksheets[0]
    rows = ws.iter_rows(values_only=True)
    head = next(rows)
    i = {k: n for n, k in enumerate(head)}
    out = {}
    for r in rows:
        y = r[i["year"]]
        if y not in YEARS or r[i["state"]] not in ST:
            continue
        st = ST[r[i["state"]]]
        rec = {"elected": r[i["election_year"]]}
        for ch in ("sen", "hs"):
            rec[ch] = {k: num(r[i[f"{ch}_{f}_in_sess"]]) for k, f in
                       (("D", "dem"), ("R", "rep"), ("O", "ind"), ("V", "vac"), ("T", "tot"))}
            rec[ch]["control"] = control(r[i[f"{ch}_cont_alt"]])
        ov = r[i["veto_override_prop"]]
        rec["override"] = round(float(ov), 4) if ov is not None else None
        rec["of"] = "elected" if r[i["veto_override_prop_elected"]] == 1 else "present"
        rec["governor"] = control(r[i["govparty_c"]]) or "other"
        rec.update(HAND.get(st, {}))
        rec.update(HAND_YEAR.get((st, y), {}))
        if st == "NE":
            rec["hs"] = None
            rec["sen"] = {"T": rec["sen"]["T"], "control": None}
        out.setdefault(y, {})[st] = rec
    head = ("# The party make-up of every State legislature by session, 1959-67: written by tools/elections/make_legislatures.py\n"
            "# from Klarner's State Partisan Balance Data (its docstring has the fields). Never edit by hand.\n")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(head)
        yaml.safe_dump({"source": {"title": "Carl Klarner, State Partisan Balance Data, 1937–2011 (2013)",
                                   "url": "https://doi.org/10.7910/DVN/LZHMG3", "card": "w.klarner-state-partisan-balance-data"},
                        "sessions": {y: dict(sorted(v.items())) for y, v in sorted(out.items())}},
                       f, allow_unicode=True, sort_keys=False, width=120)
    print(f"{sum(len(v) for v in out.values())} State-sessions -> {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
