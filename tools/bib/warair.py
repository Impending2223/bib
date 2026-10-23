"""The air war's rows: attack sorties by country (indicators/war-air-attack.yaml) and in North Vietnam by route package
(indicators/war-air-nvn-rp.yaml), written by tools/indicators/make_war_air.py from the Combat Air Activities file
(CACTA, NARA) and from OSD's Southeast Asia Analysis Report as Thayer reprints it (vol. 5). They are war series (kind:
war): tools/bib/wartable.py sets them in The war table, tools/bib/war.py writes their cells (LABELS, DISPLAY there).
The definitions are the master's (indicators/concepts.yaml).

STYLE (keep it):
 1. Two series, never one: the Report's figures (then) and CACTA's count (later) are different reckonings of the same
    sorties, side by side in the row; neither stands in for the other where it is missing ("—").
 2. A cell: North Vietnam, Laos, South Vietnam, Total (the war table's stacked grid); the few sorties CACTA files
    under another country or none ("other") on hover. Route packages 1-5, 6A, 6B and the uncoded, with the total.
 3. A month CACTA holds only in part (July 1966, the 1st to the 15th) says so in the row's note.

check: the counts add up (North Vietnam, Laos, South Vietnam and other to the total; the route packages to the North
Vietnam total), unless the row carries the source's `printed` note; the CACTA counts file names every month a row
gives.
"""
import json
import os

from . import store

COUNTS = os.path.join(store.ROOT, "sources", "war-air-cacta.json")


def problems():
    from .indicators import load
    out = []
    data = load()
    try:
        months = json.load(open(COUNTS))["months"]
    except (OSError, ValueError, KeyError):
        months = None
        if any(s.get("id", "").startswith("war-air") for s in data.values()):
            out.append(("war-air-attack", "sources/war-air-cacta.json missing or unreadable"))
    for sid in ("war-air-attack", "war-air-nvn-rp"):
        s = data.get(sid)
        if not s:
            continue
        for r in s.get("rows", []):
            for col in ("first", "now"):
                v = r.get(col)
                if not isinstance(v, dict) or "total" not in v or r.get("printed"):
                    continue
                if sid == "war-air-attack":
                    ks = ("nvn", "laos", "svn", "other")
                    if not all(k in v for k in ("nvn", "laos", "svn")):
                        continue
                else:
                    ks = tuple(k for k in v if k != "total")
                if sum(v.get(k, 0) for k in ks) != v["total"]:
                    out.append((sid, f"{r['p']}: {col} parts do not add to the total"))
            if r.get("now") is not None and months is not None:
                yymm = r["p"][2:4] + r["p"][5:7]
                if yymm not in months:
                    out.append((sid, f"{r['p']}: no CACTA count for the month in sources/war-air-cacta.json"))
    return out
