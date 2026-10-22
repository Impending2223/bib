"""The war in the calendar's monthly tables: U.S. deaths in Southeast Asia and U.S. military personnel in South
Vietnam (indicators/war-deaths.yaml, indicators/war-strength.yaml, kind: war; written by tools/indicators/make_war.py).
tools/bib/indicators.py files and lays out the rows (group "The war"); this module writes their cells. The definitions
are the master's (indicators/concepts.yaml; tools/bib/concepts.py).

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


# The definitions: the master's (indicators/concepts.yaml; tools/bib/concepts.py).
from . import concepts
DEFS = {k: v for k, v in concepts.master_texts().items() if k in ("war-deaths", "war-strength")}

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
