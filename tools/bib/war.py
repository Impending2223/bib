"""The war's cells: U.S. deaths in Southeast Asia and U.S. military personnel in South Vietnam (indicators/war-deaths.yaml,
war-strength.yaml; tools/indicators/make_war.py), and the enemy, the Republic of Vietnam's forces and the other allies
(indicators/war-enemy-*.yaml, war-infiltration, war-rvnaf-*, war-fwmaf-strength; tools/indicators/make_war_forces.py).
All kind: war. They are not in the month's indicator tables: tools/bib/wartable.py sets them in The war table under the
first Thursday of the next month (its STYLE); this module writes their cells, there and on the Indicators page. The
definitions are the master's (indicators/concepts.yaml; tools/bib/concepts.py).

STYLE (keep it):
 1. Deaths, a stacked cell: "All causes", "Hostile", "Since 1961" (all causes from Jan. 1, 1961, the DoD's period,
    through the period's end), persons with commas. A figure the source does not give is left out, not shown as zero:
    as first reported, the hostile deaths alone (the Statistical Abstract's "battle deaths"; the Systems Analysis
    office's "deaths resulting from hostile action").
 2. Months from Jan. 1965; years 1960-68, filed in December after the month. Before 1965 the years only (the plan of
    Oct. 20, 2026).
 3. Strength: persons with commas; "about" kept ("about 900"). Rows at June 30 and Dec. 31 (the DoD's table), and the
    first quarter's end where the Statistical Abstract printed it then.
 4. No change column: a count of the dead is not a level, and the rows are irregular.
 5. Persons always, with commas: a source printing thousands to one decimal (MACV's order of battle, "235.4") is
    multiplied out (235,400), the figure as printed on hover with its unit. A range as printed, an en dash between
    ("70,000–90,000"). A cell of several figures is a stacked grid (label, figure), the parts DISPLAY names in its order
    and the rest on hover (the order of battle's VC and NVA split, the territorial forces' parts); a cell of one figure
    is the bare figure.
 6. A row's note (preliminary, approximate, a quarterly average) in grey after the figure (in the war table on a line
    of its own under it); a "Check" (a figure faint
    in the copy) and a "printed" note (where a printed total and its parts disagree) on hover, and the Check in grey.
"""


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# The definitions: the master's (indicators/concepts.yaml; tools/bib/concepts.py).
from . import concepts
SERIES = ("war-deaths", "war-strength", "war-enemy-ob", "war-enemy-ob-old", "war-enemy-snie", "war-enemy-strength-q",
          "war-infiltration", "war-enemy-kia", "war-rvnaf-kia", "war-rvnaf-strength", "war-fwmaf-strength",
          "war-air-attack", "war-air-nvn-rp")
DEFS = {k: v for k, v in concepts.master_texts().items() if k in SERIES}

LABELS = {"all": "All causes", "hostile": "Hostile", "cum": "Since 1961",
          "combat": "Combat", "vc": "VC", "nva": "NVA", "guer": "Guerrillas", "admin": "Admin.",
          "admin_nva": "NVA admin.", "sd": "Self-defense", "political": "Political cadre", "regular": "Regular forces",
          "total": "Total", "accepted": "Accepted", "possible": "Possible", "rvnaf": "RVNAF",
          "army": "Army", "af": "Air Force", "navy": "Navy", "marines": "Marines", "rf": "Regional Forces",
          "pf": "Popular Forces", "territorial": "Territorial",
          "korea": "Korea", "australia": "Australia", "thailand": "Thailand", "nz": "New Zealand",
          "phil": "Philippines", "roc": "Rep. of China", "spain": "Spain",
          "nvn": "North Vietnam", "laos": "Laos", "svn": "South Vietnam", "other": "Other",
          "rp1": "RP 1", "rp2": "RP 2", "rp3": "RP 3", "rp4": "RP 4", "rp5": "RP 5", "rp6a": "RP 6A", "rp6b": "RP 6B",
          "rp_unk": "Not coded"}
# the parts a cell shows, in order; the rest of the row's figures on hover
DISPLAY = {"war-deaths": ("all", "hostile", "cum"),
           "war-enemy-ob": ("combat", "guer", "admin", "total"),
           "war-enemy-ob-old": ("combat", "admin", "guer", "sd", "political", "total"),
           "war-enemy-snie": ("regular", "guer", "admin", "political"),
           "war-enemy-strength-q": ("combat", "guer", "admin", "admin_nva", "total"),
           "war-infiltration": ("accepted", "possible", "total"),
           "war-rvnaf-strength": ("regular", "territorial", "total"),
           "war-fwmaf-strength": ("korea", "australia", "thailand", "total"),
           "war-air-attack": ("nvn", "laos", "svn", "total"),
           "war-air-nvn-rp": ("rp1", "rp2", "rp3", "rp4", "rp5", "rp6a", "rp6b", "total")}
LABEL = tuple((k, LABELS[k]) for k in DISPLAY["war-deaths"])      # kept for the deaths


def unit(r, col):
    return r.get("unit_first" if col == "first" else "unit_now") or r.get("unit")


def persons(v, u=None):
    if isinstance(v, (list, tuple)):
        return "–".join(persons(x, u) for x in v)
    if u == "thousands":
        v = int(round(v * 1000))
    return f"{int(v):,}"


def kv(lines):
    return '<span class="kv">' + "".join(
        f'<span class="k">{esc(a)}</span><span class="v">{esc(b)}</span>' for a, b in lines) + "</span>"


def parts(sid, v):
    """The keys a dict cell shows, in order."""
    order = DISPLAY.get(sid) or tuple(v)
    keys = [k for k in order if v.get(k) is not None]
    return keys or [k for k in v if v[k] is not None]


def figure(sid, s, r, col):
    """The bare figure or stacked grid of a war row's column, without its note: '—' where none."""
    v = r.get(col)
    if v is None:
        return "—"
    u = unit(r, col)
    if isinstance(v, dict):
        ks = parts(sid, v)
        if len(v) == 1:
            return persons(next(iter(v.values())), u)
        return kv([(LABELS.get(k, k), persons(v[k], u)) for k in ks])
    qual = r.get("q_now" if col == "now" else "q")
    return (f"{esc(qual)} " if qual else "") + persons(v, u)


def cell(sid, s, r, col):
    """The cell of a war row: col "first" (as first reported) or "now" (later, or today)."""
    out = figure(sid, s, r, col)
    if out == "—":
        return out
    extra = [x for x in (r.get("note"),) if x]
    if r.get("check") and col == "first":
        extra.append("Check")
    if extra:
        out += f' <span class="u wnote">({esc("; ".join(extra))})</span>'
    return out


def tip(sid, r, col):
    """The figures as printed, with their unit, and the row's Check and printed notes: for the hover."""
    v = r.get(col)
    if v is None:
        return ""
    u = unit(r, col)
    if isinstance(v, dict):
        t = "; ".join(f"{LABELS.get(k, k)} {('–'.join(str(y) for y in x) if isinstance(x, (list, tuple)) else x)}"
                      for k, x in v.items())
    else:
        t = str(v)
    t += " (thousands)" if u == "thousands" else ""
    for k in ("check", "printed"):
        if r.get(k) and (k == "printed" or col == "first"):
            t += f"; {'Check: ' if k == 'check' else ''}{r[k]}"
    return t


def _counts(v):
    if isinstance(v, dict):
        out = []
        for x in v.values():
            out += list(x) if isinstance(x, (list, tuple)) else [x]
        return out
    return [] if v is None else [v]


def problems():
    """For ./bib check: every war series has a statement; figures are counts (or thousands where the row says so) and
    sourced; a death row's hostile do not exceed all causes; a cell's parts add to its total where the source gives them
    all (combat, admin, guerrillas; accepted, possible; the services; the countries), unless the row says how the
    printed total differs ("printed")."""
    from .indicators import load
    out = []
    for sid, s in load().items():
        if s.get("kind") != "war":
            continue
        if sid not in DEFS:
            out.append((sid, f"war series {sid!r} has no statement in indicators/concepts.yaml"))
        for r in s.get("rows", []):
            for col in ("first", "now"):
                v = r.get(col)
                if v is None:
                    continue
                u = unit(r, col)
                for x in _counts(v):
                    ok = isinstance(x, (int, float)) and x >= 0 and (isinstance(x, int) or u == "thousands")
                    if not ok:
                        out.append((sid, f"{r['p']}: {col} not a count"))
                src = r.get("source" if col == "first" else "now_source")
                if s.get("manual") and not src and sid not in ("war-deaths", "war-strength"):
                    out.append((sid, f"{r['p']}: {col} figure without a source"))
                if col == "now" and sid not in ("war-deaths", "war-strength") and not r.get("now_released"):
                    out.append((sid, f"{r['p']}: later figure without its date"))
                if isinstance(v, dict) and v.get("hostile") is not None and v.get("all") is not None \
                        and v["hostile"] > v["all"]:
                    out.append((sid, f"{r['p']}: {col} hostile deaths exceed all causes"))
                if isinstance(v, dict) and not r.get("printed"):
                    tol = 0.05 if u == "thousands" else 0
                    for whole, ps in (("total", ("combat", "admin", "guer")), ("combat", ("vc", "nva")),
                                      ("total", ("accepted", "possible")), ("regular", ("army", "af", "navy", "marines")),
                                      ("territorial", ("rf", "pf")), ("total", ("regular", "territorial")),
                                      ("total", ("korea", "australia", "thailand", "nz", "phil", "roc", "spain"))):
                        extra = {"sd", "political", "admin_nva"} & set(v) if ps == ("combat", "admin", "guer") else ()
                        if not extra and all(isinstance(v.get(k), (int, float)) for k in ps + (whole,)) \
                                and abs(sum(v[k] for k in ps) - v[whole]) > tol:
                            out.append((sid, f"{r['p']}: {col} parts ({', '.join(ps)}) do not add to {whole}"))
    return out
