"""The war in the calendar's monthly tables, and the dead by home State: writes

    indicators/war-deaths.yaml     U.S. deaths in Southeast Asia, by month of incident or death from Jan. 1965, by year
                                   1960-68; hostile and all causes, and the total since Jan. 1, 1961
    indicators/war-strength.yaml   U.S. military personnel in South Vietnam, June 30 and Dec. 31, 1960-68
    sources/war-dead-states.yaml   deaths by home of record (State) and year, 1961-64 together and 1965-68 each, with the
                                   States' populations (rendered by tools/bib/wardead.py, tag wardead:<YYYY>)

    python3 tools/indicators/make_war.py [--cache DIR]

Needs the network the first time (the NARA file, 24 MB, and the Census table, 8 KB, downloaded into DIR, default
.cache/war); the build does not. The file holds the dead by name and service number: it stays in the cache, never in
the repository; nothing is written from it but counts.

Today (now): the Defense Casualty Analysis System's Vietnam Conflict Extract Data File, as of Apr. 29, 2008 (NARA, RG
330, NAID 2240992): one record a death, 58,220; field 35 the incident or death date (YYYYMMDD), 43 hostile (H) or not
(NH), 17 the home of record's State. Counted by the date's month and year; every record (all services, all person
types). The DoD's period begins Jan. 1, 1961: the total "since 1961" counts from then; 1960's dead (5) are in its row
alone. NARA's own counts by year agree (1965, 1,928; 1966, 6,350; 1967, 11,363; 1968, 16,899).

Then (first): read by hand from the pages, each figure with its source (THEN_*, below); nothing else. Where no figure
was read, the row has none and shows "—":
  - the *Statistical Abstract of the United States*, 88th ed. (July 1967), table 372, p. 264; 89th ed. (June 1968),
    table 373, p. 258; 90th ed. (June 1969), table 373, p. 256: "Viet-Nam Conflict--U.S. Military Forces and
    Casualties", from the Office of the Secretary of Defense, *Selected Manpower Statistics*: battle deaths by year
    (killed, died of wounds, died while missing or captured: hostile deaths), forces at Dec. 31 and at the end of the
    first quarter of the edition's year. Each year's figure from the first edition printing it; no earlier edition prints
    the table (the 87th, 1966, has none).
  - OASD(Systems Analysis), *Southeast Asia Analysis Report*, Oct. 1967, "U.S. Casualties", Table 1, "U.S. Deaths
    Resulting from Hostile Action, 1967", S.E. Asia total, Jan.-Sept. 1967 (dated Oct. 10, 1967; Confidential then);
    reprinted in Thayer, *A Systems Analysis View of the Vietnam War*, vol. 8, p. 102.
The weekly releases as the papers printed them (the Thursday figures in the *Times*) were not read: TimesMachine and
nytimes.com refuse this environment (notes/leads.md).

Strength today: *Selected Manpower Statistics*, FY 1974 (OASD (Comptroller), 1975), "U.S. Military Personnel in South
Vietnam 1960-1973", p. 63 (dated Mar. 19, 1974): June 30 and Dec. 31 each year. No monthly table was found open
(MACV's command histories, at Texas Tech, are refused here).

Populations: Census Bureau, "Intercensal Estimates of the Total Resident Population of States: 1960 to 1970" (st6070ts,
consistent with *Current Population Reports*, P-25, No. 460), July 1 of each year, in thousands; 1961-64 together
over the mean of the four years' estimates.
"""
import argparse
import collections
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))

DCAS_URL = ("https://catalog.archives.gov/medialive/92/2409/2240992/content/arcmedia/electronic-records/rg-330/"
            "dcase/DCAS.VN.EXT08.DAT")
DCAS_CAT = "https://catalog.archives.gov/id/2240992"
DCAS_DOC = ("https://catalog.archives.gov/medialive/92/2409/2240992/content/arcmedia/electronic-records/rg-330/"
            "dcase/DCAS.VN08.DOC.PDF")
POP_URL = "https://www2.census.gov/programs-surveys/popest/tables/1980-1990/state/asrh/st6070ts.txt"
SA = {1967: "https://www.census.gov/library/publications/1967/compendia/statab/88ed.html",
      1968: "https://www.census.gov/library/publications/1968/compendia/statab/89ed.html",
      1969: "https://www.census.gov/library/publications/1969/compendia/statab/90ed.html"}
SMS74 = "https://archive.org/details/DTIC_ADA043053"
THAYER8 = "https://archive.org/details/DTIC_ADA051613"

SA67 = "Statistical Abstract of the United States, 1967 (88th ed., July 1967), table 372, p. 264"
SA68 = "Statistical Abstract of the United States, 1968 (89th ed., June 1968), table 373, p. 258"
SA69 = "Statistical Abstract of the United States, 1969 (90th ed., June 1969), table 373, p. 256"
SEA67 = ("OASD(SA), Southeast Asia Analysis Report, Oct. 1967, U.S. Casualties, Table 1 (dated Oct. 10, 1967); "
         "Thayer, A Systems Analysis View of the Vietnam War, vol. 8, p. 102")

# battle deaths (hostile), by year, as first printed: (figure, released, source)
THEN_DEATHS_YEAR = {
    "1961": (11, "1967-07", SA67), "1962": (31, "1967-07", SA67), "1963": (78, "1967-07", SA67),
    "1964": (147, "1967-07", SA67), "1965": (1369, "1967-07", SA67), "1966": (5008, "1967-07", SA67),
    "1967": (9378, "1968-06", SA68), "1968": (14592, "1969-06", SA69),
}
# U.S. deaths resulting from hostile action, S.E. Asia, by month, 1967 (Table 1, "TOTAL" under "S.E. ASIA")
THEN_DEATHS_MONTH = {
    "1967-01": 520, "1967-02": 662, "1967-03": 944, "1967-04": 710, "1967-05": 1233,
    "1967-06": 830, "1967-07": 781, "1967-08": 535, "1967-09": 775,
}
# forces in South Vietnam, as first printed: Dec. 31, and the first quarter's end (the edition's "1st qtr." column)
THEN_STRENGTH = {
    "1961-12": (3200, "1967-07", SA67), "1962-12": (11300, "1967-07", SA67), "1963-12": (16300, "1967-07", SA67),
    "1964-12": (23300, "1967-07", SA67), "1965-12": (184300, "1967-07", SA67), "1966-12": (384400, "1967-07", SA67),
    "1967-03": (439400, "1967-07", SA67), "1967-12": (486600, "1968-06", SA68), "1968-03": (516400, "1968-06", SA68),
    "1968-12": (536100, "1969-06", SA69),
}
# today: Selected Manpower Statistics FY-74, p. 63, total (all services); (figure, qualifier)
NOW_STRENGTH = {
    "1960-12": (900, "about"), "1961-12": (3200, None), "1962-06": (9000, None), "1962-12": (11300, None),
    "1963-06": (15400, None), "1963-12": (16300, None), "1964-06": (16500, None), "1964-12": (23300, None),
    "1965-06": (59900, None), "1965-12": (184300, None), "1966-06": (267500, None), "1966-12": (385300, None),
    "1967-06": (448800, None), "1967-12": (485600, None), "1968-06": (534700, None), "1968-12": (536100, None),
}
SMS74_SRC = ("Selected Manpower Statistics, FY-74 (OASD (Comptroller), 1975), U.S. Military Personnel in South Vietnam "
             "1960-1973, p. 63")
DCAS_SRC = "NARA, DCAS Vietnam Conflict Extract Data File, as of Apr. 29, 2008 (NAID 2240992)"

STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
          "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
          "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
SPANS = {"1961-1964": [1961, 1962, 1963, 1964], "1965": [1965], "1966": [1966], "1967": [1967], "1968": [1968]}


def fetch(url, path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        subprocess.run(["curl", "-sS", "-f", "-o", path, url], check=True)
    return path


def read_dcas(path):
    """Counts: by month and year (all, hostile), by (year, home State) (all, hostile)."""
    month, year, home = collections.Counter(), collections.Counter(), collections.Counter()
    n = 0
    with open(path, encoding="latin-1") as f:
        for line in f:
            r = line.rstrip("\n").split("|")
            if len(r) < 47:
                continue
            n += 1
            d, hostile, st = r[34], r[42].strip() == "H", r[16].strip() or "?"
            if not re.match(r"^\d{8}$", d):
                continue
            for key in ((d[:4] + "-" + d[4:6]), d[:4]):
                (month if "-" in key else year)[(key, "all")] += 1
                if hostile:
                    (month if "-" in key else year)[(key, "hostile")] += 1
            if r[15].strip() not in ("US", ""):           # home of record outside the United States
                st = "foreign"
            home[(d[:4], st, "all")] += 1
            if hostile:
                home[(d[:4], st, "hostile")] += 1
    return n, month, year, home


def read_pop(path):
    """{year: {ST: thousands}} for July 1, 1960-69."""
    out, cols = collections.defaultdict(dict), None
    for line in open(path, encoding="latin-1"):
        if re.match(r"^\s+(April 1,|July 1,)", line):
            continue
        m = re.match(r"^\s+((?:\d{4}\s+)+\d{4})\s*$", line)
        if m:
            heads = m.group(1).split()
            cols = heads
            continue
        m = re.match(r"^([A-Z]{2})\s+([\d,\s]+)$", line.rstrip())
        if m and cols:
            vals = [int(v.replace(",", "")) for v in m.group(2).split()]
            for i, (y, v) in enumerate(zip(cols, vals)):
                # the first block: April 1, 1960, then July 1, 1960-64; the second: July 1, 1965-69, then April 1, 1970
                if cols[0] == "1960" and i == 0:
                    continue
                if y == "1970":
                    continue
                out[int(y)][m.group(1)] = v
    return out


def q(s):
    return "'" + str(s).replace("'", "''") + "'"


def dump_rows(rows):
    out = []
    for r in rows:
        parts = []
        for k, v in r.items():
            if isinstance(v, dict):
                v = "{" + ", ".join(f"{a}: {b}" for a, b in v.items()) + "}"
            elif isinstance(v, str):
                v = q(v)
            parts.append(f"{k}: {v}")
        out.append("- {" + ", ".join(parts) + "}")
    return "\n".join(out)


HEAD = ("# Generated by tools/indicators/make_war.py. Edit the script, not this file.\n"
        "# p: period; first: as first reported (released, source); now: today (the NARA file, or the DoD's table of 1974).\n")


def write_deaths(month, year):
    rows, cum = [], 0
    cums = {}
    for y in range(1961, 1970):
        for m in range(1, 13):
            k = f"{y}-{m:02d}"
            cum += month.get((k, "all"), 0)
            cums[k] = cum
    for y in range(1960, 1969):
        k = str(y)
        r = {"p": k, "now": {"all": year.get((k, "all"), 0), "hostile": year.get((k, "hostile"), 0)}}
        if y >= 1961:
            r["now"]["cum"] = cums[f"{y}-12"]
        if k in THEN_DEATHS_YEAR:
            v, rel, src = THEN_DEATHS_YEAR[k]
            r.update({"first": {"hostile": v}, "released": rel, "source": src})
        rows.append((f"{y}-12-99", r))
    for y in range(1965, 1970):
        for m in range(1, 13):
            k = f"{y}-{m:02d}"
            if k > "1969-01":
                break
            r = {"p": k, "now": {"all": month.get((k, "all"), 0), "hostile": month.get((k, "hostile"), 0),
                                 "cum": cums[k]}}
            if k in THEN_DEATHS_MONTH:
                r.update({"first": {"hostile": THEN_DEATHS_MONTH[k]}, "released": "1967-10-10", "source": SEA67})
            rows.append((k, r))
    rows = [r for _, r in sorted(rows, key=lambda t: t[0])]
    text = (HEAD + "id: war-deaths\nname: U.S. deaths, Southeast Asia\nfreq: M\nmanual: true\nkind: war\n"
            f"then: {{label: 'Hostile deaths (battle deaths), as first printed', source: {q(SA67)}}}\n"
            f"now: {{label: 'Deaths by incident or death date, all causes and hostile', source: {q(DCAS_SRC)}, "
            f"url: {q(DCAS_CAT)}}}\nrows:\n" + dump_rows(rows) + "\n")
    open(os.path.join(ROOT, "indicators", "war-deaths.yaml"), "w").write(text)
    return rows


def write_strength():
    keys = sorted(set(NOW_STRENGTH) | set(THEN_STRENGTH))
    rows = []
    for k in keys:
        r = {"p": k}
        if k in THEN_STRENGTH:
            v, rel, src = THEN_STRENGTH[k]
            r.update({"first": v, "released": rel, "source": src})
        if k in NOW_STRENGTH:
            v, qual = NOW_STRENGTH[k]
            r["now"] = v
            if qual:
                r["q_now"] = qual
        rows.append(r)
    text = (HEAD + "id: war-strength\nname: U.S. military personnel, South Vietnam\nfreq: M\nmanual: true\nkind: war\n"
            f"then: {{label: 'Forces in South Vietnam, Dec. 31 and the first quarter, as first printed', source: {q(SA67)}}}\n"
            f"now: {{label: 'U.S. military personnel in South Vietnam, June 30 and Dec. 31', source: {q(SMS74_SRC)}, "
            f"url: {q(SMS74)}}}\nrows:\n" + dump_rows(rows) + "\n")
    open(os.path.join(ROOT, "indicators", "war-strength.yaml"), "w").write(text)
    return rows


def write_states(home, pop):
    lines = ["# Generated by tools/indicators/make_war.py. Edit the script, not this file.",
             "# U.S. deaths in Southeast Asia by home of record (State) and the year of the incident or death, with the",
             "# State's population (thousands, July 1; for 1961-64 the mean of the four years). Rendered by tools/bib/wardead.py.",
             f"source: {{title: {q(DCAS_SRC)}, url: {q(DCAS_CAT)}, layout: {q(DCAS_DOC)}}}",
             f"population: {{title: 'Census Bureau, Intercensal Estimates of the Total Resident Population of States: "
             f"1960 to 1970 (Aug. 1996; consistent with Current Population Reports, P-25, No. 460), July 1', url: {q(POP_URL)}}}",
             "spans:"]
    for span, years in SPANS.items():
        lines.append(f"  '{span}':")
        lines.append("    states:")
        for st in STATES:
            a = sum(home.get((str(y), st, "all"), 0) for y in years)
            h = sum(home.get((str(y), st, "hostile"), 0) for y in years)
            p = round(sum(pop[y][st] for y in years) / len(years), 1)
            lines.append(f"      {st}: {{all: {a}, hostile: {h}, pop: {p}}}")
        others = [(st, sum(home.get((str(y), st, "all"), 0) for y in years))
                  for st in sorted({k[1] for k in home if k[1] not in STATES})]
        others = [(st, a) for st, a in others if a]
        lines.append("    elsewhere:" + ("" if others else " {}"))
        lines += [f"      '{st}': {a}" for st, a in others]
    open(os.path.join(ROOT, "sources", "war-dead-states.yaml"), "w").write("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.path.join(ROOT, ".cache", "war"))
    a = ap.parse_args()
    dcas = fetch(DCAS_URL, os.path.join(a.cache, "DCAS.VN.EXT08.DAT"))
    popf = fetch(POP_URL, os.path.join(a.cache, "st6070ts.txt"))
    n, month, year, home = read_dcas(dcas)
    pop = read_pop(popf)
    assert n == 58220, f"{n} records; the file of Apr. 29, 2008 holds 58,220"
    for y, v in ((1965, 1928), (1966, 6350), (1967, 11363), (1968, 16899)):   # NARA's counts by year
        assert year[(str(y), "all")] == v, (y, year[(str(y), "all")])
    for y in range(1960, 1970):
        assert len(pop[y]) == 51, (y, len(pop[y]))
    d = write_deaths(month, year)
    s = write_strength()
    write_states(home, pop)
    print(f"{n} records; war-deaths {len(d)} rows, war-strength {len(s)} rows; sources/war-dead-states.yaml")


if __name__ == "__main__":
    main()
