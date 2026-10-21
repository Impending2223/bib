"""statefin/states.yaml: the finances of each State government, and of the State and its local governments together,
fiscal years 1959–1968, from the Census Bureau's historical finance databases (Governments Division; the figures its
annual *State Government Finances* and *Governmental Finances* printed). One-time; the build does not need the network.

    python3 tools/statefin/make_statefin.py STATE_MDB [GOVT_MDB [CITY_MDB]]

STATE_MDB is State_Govt_Finances.mdb from
https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/State_Govt_Fin.zip ("Data Base on Historical
Finances of State Governments, Fiscal Years 1942-2008", Aug. 2010); GOVT_MDB is Govt_Finances.mdb from .../Govt_Finances.zip
("Data Base on Historical Finances of State and Local Governments, Fiscal Years 1957-2008", Aug. 2010). Read with mdbtools (`mdb-export`).

STYLE (the file):
 1. `states`: by fiscal year (Census's: the State's fiscal year ending in that year; `fy_end` the date, as the database
    gives it), each State by postal code, D.C. (the database's exhibit, a city government, not in the U.S. total) and
    `US` (the fifty States): population (thousands) and personal income (millions) of that year, and `pi_prev`, the
    personal income of the calendar year before (the Census tables relate a fiscal year's taxes to it: STYLE 3 in
    tools/bib/statefin.py); the money in thousands of dollars, as the database prints it: total and general revenue,
    taxes and five of them (property, general sales, motor fuel, individual and corporate income), federal aid
    (intergovernmental revenue from the federal government), total expenditure, current operation, capital outlay,
    aid to local governments (intergovernmental expenditure to them), long-term debt outstanding at the year's end.
 2. `local`: the same State areas, the State and its local governments together (`Govt_Finances`, type 1, rounded by
    Census to hundreds of thousands): the same items where the database gives them; `state_tax` the State
    government's taxes in the same file. A flag (-11111: not published that year) is written as null.
 3. `cities`: the census years 1962 and 1967, the cities the database flags large (43, of 300,000 or more at the 1960
    census), from CITY_MDB, City_Govt_Finances.mdb in .../City_Govt_Fin.zip ("Data Base on Historical Finances of
    Municipal Governments, Fiscal Years 1951-2006"): the city's name as Census writes it, its State, the 1960 population
    (persons), and in thousands of dollars: taxes, property, general sales, selective sales, all other taxes (the
    database has no column for a city's income tax), general revenue, federal and State aid, total expenditure,
    long-term debt outstanding.
 4. `reports`: each year's printed report, its title, series number and year of publication, and the tables (number,
    first page, from the report's contents) that print the items used. Kept by hand in REPORTS below; the scans are in
    Census's "1900-1992 State Government Finance.zip".
 5. Never edit the file by hand: fix the script and rerun.
"""
import csv
import io
import os
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "statefin", "states.yaml")
YEARS = range(1959, 1969)
SCANS = ("https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/"
         "1900-1992%20State%20Government%20Finance.zip")
SOURCE = {
    "states": {"title": "Data Base on Historical Finances of State Governments, Fiscal Years 1942–2008 (Aug. 2010)",
               "url": "https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/State_Govt_Fin.zip",
               "card": "w.bureau-data-base-on-historical"},
    "local": {"title": "Data Base on Historical Finances of State and Local Governments, Fiscal Years 1957–2008 (Aug. 2010)",
              "url": "https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/Govt_Finances.zip",
              "card": "w.bureau-data-base-on-historical-2010"},
    "cities": {"title": "Data Base on Historical Finances of Municipal Governments, Fiscal Years 1951–2006 (July 2011)",
               "url": "https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/City_Govt_Fin.zip"},
    "scans": SCANS,
}
# each year's report: title, series, published; tables [number, first page] from its contents page
C = "Compendium of State Government Finances in {}"
REPORTS = {
    1960: dict(title=C.format(1960), series="G-SF60-No. 2", published="1961",
               tables=dict(aggregates=[3, 11], general=[4, 12], taxes=[5, 13], character=[12, 23], debt=[25, 40],
                           percap=[35, 52], income=[37, 58])),
    1961: dict(title=C.format(1961), series="G-SF61-No. 2", published="1962",
               tables=dict(aggregates=[3, 9], general=[4, 10], taxes=[5, 11], character=[12, 21], debt=[25, 38],
                           percap=[35, 50], income=[37, 56])),
    1962: dict(title=C.format(1962), series="G-SF62-No. 2", published="1963",
               tables=dict(aggregates=[3, 9], general=[4, 10], taxes=[5, 11], character=[12, 21], debt=[25, 38],
                           percap=[35, 50], income=[37, 56])),
    1963: dict(title=C.format(1963), series="G-SF63-No. 2", published="1964",
               tables=dict(aggregates=[3, 9], general=[4, 10], taxes=[5, 11], character=[12, 21], debt=[25, 38],
                           percap=[36, 47], relation=[37, 49], income=[38, 50])),
    1964: dict(title=C.format(1964), series="G-SF64-No. 2", published="1965",
               tables=dict(aggregates=[3, 10], general=[4, 11], taxes=[5, 12], character=[12, 22], debt=[25, 40],
                           percap=[35, 48], relation=[36, 50], income=[37, 51])),
    1965: dict(title=C.format(1965), series="GF-No. 4", published="1966",
               tables=dict(aggregates=[3, 10], percap=[4, 11], relation=[6, 18], revenue=[7, 19], character=[8, 27],
                           debt=[12, 40], income=[20, 49])),
    1966: dict(title="State Government Finances in 1966", series="GF No. 11", published="1967",
               tables=dict(aggregates=[3, 10], percap=[4, 11], relation=[6, 18], revenue=[7, 19], character=[8, 27],
                           debt=[12, 40], income=[20, 49])),
    1967: dict(title="State Government Finances in 1967", series="GF67 No. 1", published="1968",
               tables=dict(aggregates=[3, 11], percap=[4, 12], relation=[6, 19], revenue=[7, 20], character=[8, 28],
                           debt=[12, 41], income=[20, 50])),
    1968: dict(title="State Government Finances in 1968", series="GF68 No. 3", published="1969",
               tables=dict(aggregates=[3, 11], percap=[4, 12], relation=[6, 19], revenue=[7, 20], character=[8, 28],
                           debt=[12, 41], income=[20, 50])),
}
CODE = {"US": "00"}
REV = {"pop": "Population (000)", "pi": "Personal Income ($mil)", "rev": "Total Revenue", "genrev": "General Revenue",
       "tax": "Total Taxes", "property": "Property Tax (T01)", "sales": "Total Gen Sales Tax (T09)",
       "fuel": "Motor Fuels Tax (T13)", "income": "Individual Income Tax (T40)", "corp": "Corp Net Income Tax (T41)",
       "fed": "Total Fed IG Revenue"}
EXP = {"exp": "Total Expenditure", "curop": "Total Current Oper", "capital": "Total Capital Outlays",
       "tolocal": "IG Exp-To Local Govts"}
DEBT = {"ltd": "Total Long-Term Debt Out"}
CITY_YEARS = (1962, 1967)
CITY = {"pop": "Population", "tax": "Total Taxes", "property": "Property Tax (T01)", "sales": "Total Gen Sales Tax (T09)",
        "selective": "Total Select Sales Tax", "other": "Other Taxes", "genrev": "General Revenue",
        "fed": "Total Fed IG Revenue", "state": "Total State IG Revenue", "exp": "Total Expenditure",
        "ltd": "Total Long-Term Debt Out"}


def table(mdb, name):
    out = subprocess.run(["mdb-export", mdb, name], capture_output=True, text=True, check=True).stdout
    return list(csv.DictReader(io.StringIO(out)))


def num(v):
    if v in (None, ""):
        return None
    n = int(float(v))
    return None if n <= -11111 else n


def postal(name):
    """'AL STATE GOVT', 'US STATE GOVTS', 'EXHIBIT: WASH DC', 'CA STATE-LOCAL TOTAL' -> AL, US, DC, CA."""
    if "WASH DC" in name:
        return "DC"
    return name.split()[0]


def fy_end(v):
    v = (v or "").strip()
    if len(v) != 6:
        return None
    return f"19{v[4:]}-{v[:2]}-{v[2:4]}"


def rows(mdb, tname, cols, keep, years):
    out = {}
    for r in table(mdb, tname):
        y = int(r["Year4"])
        if y not in years or not keep(r):
            continue
        st = postal(r["Name"])
        rec = out.setdefault(y, {}).setdefault(st, {})
        for k, c in cols.items():
            rec[k] = num(r.get(c))
        if "FY Ending Date" in r and st != "US":
            rec["fy_end"] = fy_end(r["FY Ending Date"])
    return out


def merge(*parts):
    out = {}
    for p in parts:
        for y, S in p.items():
            for st, rec in S.items():
                out.setdefault(y, {}).setdefault(st, {}).update(rec)
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    smdb = sys.argv[1]
    gmdb = sys.argv[2] if len(sys.argv) > 2 else None
    yrs = set(range(YEARS.start - 1, YEARS.stop))            # the year before the first, for pi_prev
    state = lambda r: r["Type Code"] in ("2", "6")          # the State governments, the U.S., D.C.'s exhibit
    st = merge(rows(smdb, "1_Revenues", REV, state, yrs), rows(smdb, "2_ExpendituresA", EXP, state, yrs),
               rows(smdb, "4_Debt_and_Cash_&_Securities", DEBT, state, yrs))
    for y in YEARS:
        for k, rec in st[y].items():
            rec["pi_prev"] = (st.get(y - 1, {}).get(k) or {}).get("pi")
    order = ["fy_end", "pop", "pi", "pi_prev", "rev", "genrev", "tax", "property", "sales", "fuel", "income", "corp",
             "fed", "exp", "curop", "capital", "tolocal", "ltd"]
    data = {"source": SOURCE, "reports": REPORTS,
            "states": {y: {k: {f: st[y][k].get(f) for f in order if f in st[y][k]} for k in sorted(st[y])} for y in YEARS}}
    if gmdb:
        tot = lambda r: r["Type Code"] == "1"
        gst = lambda r: r["Type Code"] == "2"
        loc = merge(rows(gmdb, "1_Revenues", REV, tot, yrs), rows(gmdb, "2_Expenditures", {"exp": "Total Expenditure"}, tot, yrs),
                    rows(gmdb, "3_Debt_and_Cash_and_Securities", DEBT, tot, yrs))
        sg = rows(gmdb, "1_Revenues", {"state_tax": "Total Taxes"}, gst, yrs)
        for y in YEARS:
            for k, rec in loc[y].items():
                rec["pi_prev"] = (loc.get(y - 1, {}).get(k) or {}).get("pi")
                rec["state_tax"] = (sg.get(y, {}).get(k) or {}).get("state_tax")
        lorder = ["pop", "pi", "pi_prev", "rev", "genrev", "tax", "state_tax", "property", "sales", "fuel", "income",
                  "corp", "fed", "exp", "ltd"]
        data["local"] = {y: {k: {f: loc[y][k].get(f) for f in lorder} for k in sorted(loc[y])} for y in YEARS}
    cmdb = sys.argv[3] if len(sys.argv) > 3 else None
    if cmdb:
        code = {}
        for r in table(smdb, "1_Revenues"):
            if r["Type Code"] == "2" and r["State Code"] != "00":
                code[r["State Code"]] = postal(r["Name"])
        code["09"] = "DC"
        out = {}
        for r in table(cmdb, "City_Govt_Finances"):
            y = int(r["Year4"])
            if y not in CITY_YEARS or r["Large City Flag"] != "1":
                continue
            rec = {"name": r["Name"].strip(), "st": code.get(r["State Code"], r["State Code"])}
            rec.update({k: num(r.get(c)) for k, c in CITY.items()})
            out.setdefault(y, {})[r["ID"].strip()] = rec
        data["cities"] = {y: dict(sorted(S.items(), key=lambda kv: -(kv[1]["pop"] or 0))) for y, S in sorted(out.items())}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("# The finances of each State government, and of each State's governments together, fiscal 1959-68: written by\n"
                "# tools/statefin/make_statefin.py from the Census Bureau's historical finance databases (its docstring has the\n"
                "# fields). Money in thousands of dollars; population in thousands; personal income in millions. Never edit by hand.\n")
        head = {k: v for k, v in data.items() if k not in ("states", "local", "cities")}
        yaml.safe_dump(head, f, allow_unicode=True, sort_keys=False, width=120)
        for part in ("states", "local", "cities"):  # one line a State-year, a city-year
            if part not in data:
                continue
            f.write(f"{part}:\n")
            for y, S in data[part].items():
                f.write(f"  {y}:\n")
                for k, rec in S.items():
                    line = yaml.safe_dump(rec, default_flow_style=True, sort_keys=False, width=10000).strip()
                    f.write(f"    '{k}': {line}\n" if part == "cities" else f"    {k}: {line}\n")
    print("wrote", OUT, {y: len(v) for y, v in data["states"].items()})


if __name__ == "__main__":
    main()
