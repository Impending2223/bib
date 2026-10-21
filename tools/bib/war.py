"""The war in the calendar's monthly tables: U.S. deaths in Southeast Asia and U.S. military personnel in South
Vietnam (indicators/war-deaths.yaml, indicators/war-strength.yaml, kind: war; written by tools/indicators/make_war.py).
tools/bib/indicators.py files and lays out the rows (group "The war"); this module writes their cells and definitions.

STYLE (keep it):
 1. Deaths, a stacked cell in the indicators' grid: "All causes", "Hostile", "Since 1961" (all causes from Jan. 1,
    1961, the DoD's period, through the period's end), persons with commas. A figure the source does not give is left
    out, not shown as zero: as first reported, the hostile deaths alone (the Statistical Abstract's "battle deaths";
    the Systems Analysis office's "deaths resulting from hostile action").
 2. Months from Jan. 1965, filed in their month; years 1960-68, filed in December after the month. Before 1965 the
    years only (the plan of Oct. 20, 2026).
 3. Strength: persons with commas; "about" kept ("about 900"). Rows at June 30 and Dec. 31 (the DoD's table), and the
    first quarter's end where the Statistical Abstract printed it then.
 4. No change column: a count of the dead is not a level, and the strength rows are six months apart.
"""


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


NARA = "https://catalog.archives.gov/id/2240992"
NARA_STATS = "https://www.archives.gov/research/military/vietnam-war/casualty-statistics"
SA67 = "https://www.census.gov/library/publications/1967/compendia/statab/88ed.html"
SA68 = "https://www.census.gov/library/publications/1968/compendia/statab/89ed.html"
SA69 = "https://www.census.gov/library/publications/1969/compendia/statab/90ed.html"
THAYER8 = "https://archive.org/details/DTIC_ADA051613"
SMS74 = "https://archive.org/details/DTIC_ADA043053"

DEFS = {
    "war-deaths": (
        "Members of the armed forces who died in the war in Southeast Asia, by the month (from Jan. 1965) or year of "
        "the incident or death: all causes, hostile (killed in action, died of wounds, died while missing or "
        "captured), and all causes since Jan. 1, 1961, the start of the Department of Defense's period. Today: "
        f"[NARA, Defense Casualty Analysis System, Vietnam Conflict Extract Data File, as of Apr. 29, 2008]({NARA}) "
        "(RG 330, NAID 2240992), one record a death, 58,220, counted by the incident or death date; the missing "
        "declared dead years later are filed at the incident. NARA's own counts by year agree "
        f"([casualty statistics]({NARA_STATS})). As first reported: the hostile deaths as first printed. By year, "
        f"the *Statistical Abstract of the United States*, from the Defense Department's *Selected Manpower "
        f"Statistics*: [88th ed. (July 1967)]({SA67}), table 372, p. 264 (1961 to 1966; no earlier edition prints the "
        f"table); [89th ed. (June 1968)]({SA68}), table 373, p. 258 (1967); [90th ed. (June 1969)]({SA69}), table 373, "
        "p. 256 (1968). By month, Jan.-Sept. 1967 only: the Office of the Assistant Secretary of Defense (Systems "
        "Analysis), *Southeast Asia Analysis Report*, Oct. 1967, \"U.S. Casualties,\" Table 1, dated Oct. 10, 1967, "
        "Confidential then, not a release ([Thomas C. Thayer, ed., *A Systems Analysis View of the Vietnam War, "
        f"1965–1972*, vol. 8 (1975)]({THAYER8}), p. 102). The weekly figures MACV and the Pentagon announced each "
        "Thursday, as the papers printed them, are not read here: \"—\". The two columns differ by the late "
        "reports and by the missing later declared dead, counted at the incident today."),
    "war-strength": (
        "Members of the armed forces in South Vietnam (personnel on ships off the coast excluded), all services. "
        f"Today: the Defense Department's table of 1974, *Selected Manpower Statistics*, FY 1974 ([OASD "
        f"(Comptroller), 1975]({SMS74})), \"U.S. Military Personnel in South Vietnam 1960–1973,\" p. 63: June 30 and "
        "Dec. 31 each year; the peak, 543,400, Apr. 30, 1969. As first reported: the *Statistical Abstract*'s table "
        f"\"Viet-Nam Conflict—U.S. Military Forces and Casualties,\" Dec. 31 and the end of the edition's first "
        f"quarter ([88th ed., July 1967]({SA67}), table 372, p. 264; [89th ed., June 1968]({SA68}), table 373, p. "
        f"258; [90th ed., June 1969]({SA69}), table 373, p. 256). MACV's month-end strength (its command histories) "
        "and the weekly strength announced in Saigon are not read here: \"—\"."),
}

LABEL = (("all", "All causes"), ("hostile", "Hostile"), ("cum", "Since 1961"))


def persons(v):
    return f"{v:,}"


def kv(lines):
    return '<span class="kv">' + "".join(
        f'<span class="k">{esc(a)}</span><span class="v">{esc(b)}</span>' for a, b in lines) + "</span>"


def cell(sid, s, r, col):
    """The cell of a war row: col "first" (as first reported) or "now" (today)."""
    v = r.get(col)
    if v is None:
        return "—"
    if sid == "war-deaths":
        return kv([(lab, persons(v[k])) for k, lab in LABEL if isinstance(v, dict) and v.get(k) is not None])
    qual = r.get("q_now" if col == "now" else "q")
    return (f"{esc(qual)} " if qual else "") + persons(v)


def tip(sid, r, col):
    v = r.get(col)
    if v is None:
        return ""
    if isinstance(v, dict):
        return "; ".join(f"{k} {x}" for k, x in v.items())
    return str(v)


def problems():
    """For ./bib check: a war row whose figures are not counts, a death row whose hostile exceed all causes."""
    from .indicators import load
    out = []
    for sid, s in load().items():
        if s.get("kind") != "war":
            continue
        if sid not in DEFS:
            out.append((sid, f"war series {sid!r} has no definition in DEFS (tools/bib/war.py)"))
        for r in s.get("rows", []):
            for col in ("first", "now"):
                v = r.get(col)
                vals = v.values() if isinstance(v, dict) else [v] if v is not None else []
                if any(not isinstance(x, int) or x < 0 for x in vals):
                    out.append((sid, f"{r['p']}: {col} not a count"))
                if isinstance(v, dict) and v.get("hostile") is not None and v.get("all") is not None \
                        and v["hostile"] > v["all"]:
                    out.append((sid, f"{r['p']}: {col} hostile deaths exceed all causes"))
    return out
