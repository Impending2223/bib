"""Armed Forces Day: the year's forces tables, under the third Saturday in May.

The owner's request, Oct. 22, 2026: the yearly forces tables (U.S. forces and materiel, and the world's: tools/bib/forces.py,
another module's, called through FORCES below) go under Armed Forces Day each year, with the Republic of Vietnam's and the
other allies' forces beside them. A day block (tools/bib/dayblocks.py).

STYLE (keep it):
 1. The day: the third Saturday of May, as Kennedy proclaimed it for 1961 "and the third Saturday of May in each
    succeeding year" (Proclamation 3399, Mar. 18, 1961) and Johnson again for 1965 and after (Proclamation 3655, May 7,
    1965), both linked to the Public Papers (APP); for 1960, the same Saturday, May 21 (Eisenhower's proclamation not
    read: notes/leads.md). The caption names the day and the proclamation in force.
 2. The figures are the last year's: those of Dec. 31 or the calendar year before the day (1964's under May 15, 1965),
    as the sources give them by year: the RVNAF by service (Collins, 1975; the quarterly figures of the year's end
    where Collins has none) and the other allies by country, with their maneuver battalions (Larsen and Collins, 1975).
    Both series are in The war table too (tools/bib/wartable.py), filed by period; here the year's breakdown.
 3. Each table one column of figures (and the battalions'), the label at the left: it fits a 400px phone. The look is
    the war table's (its panel and solid rule), a caption a table.
 4. Contents: "Armed forces, 1965" in the page's contents and in the Defense and Vietnam threads' Tables and maps.
"""
import datetime

from . import war

THREADS = ["defense", "vietnam"]
PROCL = {1961: ("Proclamation 3399", "Mar. 18, 1961",
                "https://www.presidency.ucsb.edu/documents/proclamation-3399-armed-forces-day"),
         1965: ("Proclamation 3655", "May 7, 1965",
                "https://www.presidency.ucsb.edu/documents/proclamation-3655-armed-forces-day")}
YEARS = range(1960, 1969)
FORCES_FNS = ("afd_block", "armed_forces_day", "year_block", "day_block")   # what forces.py may expose: year -> html


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def third_saturday(y):
    d = datetime.date(y, 5, 1)
    d += datetime.timedelta(days=(5 - d.weekday()) % 7)
    return d + datetime.timedelta(days=14)


def dates():
    return {third_saturday(y).isoformat(): y for y in YEARS}


def proclamation(y):
    k = max((x for x in PROCL if x <= y), default=None)
    return PROCL[k] if k else None


def forces_html(y):
    """The U.S. and world forces block forces.py renders for the year, where that module and function exist."""
    try:
        from . import forces
    except ImportError:
        return ""
    for fn in FORCES_FNS:
        f = getattr(forces, fn, None)
        if callable(f):
            try:
                return f(y) or ""
            except Exception as x:                 # noqa: BLE001 - the other module's error, reported not fatal
                return f'<p class="wart-foot">forces.py: {esc(x)}</p>'
    return ""


def _row(sid, period):
    from .indicators import load
    s = load().get(sid) or {}
    for r in s.get("rows", []):
        if str(r["p"]) == period:
            return s, r
    return s, None


def _year_end(sid, y):
    """The row giving the year y by year, else its Dec. 31 or fourth quarter."""
    for p in (str(y), f"{y}-12", f"{y}Q4"):
        s, r = _row(sid, p)
        if r is not None:
            return s, r
    return None, None


def table(title, rows, src, extra_head=None):
    head = "<th></th><th>Strength</th>" + (f"<th>{esc(extra_head)}</th>" if extra_head else "")
    body = "".join(f'<tr><th>{esc(a)}</th><td>{b}</td>' + (f"<td>{c}</td>" if extra_head else "") + "</tr>"
                   for a, b, c in rows)
    return (f'<p class="afd-t">{esc(title)}</p><table class="afd"><thead><tr>{head}</tr></thead><tbody>{body}</tbody>'
            f'</table><p class="wart-foot">{esc(src)}</p>')


def rvn_html(y):
    s, r = _year_end("war-rvnaf-strength", y)
    if r is None:
        return ""
    col = "now" if r.get("now") is not None else "first"
    v, u = r[col], war.unit(r, col)
    rows = [(war.LABELS[k], war.persons(v[k], u), "") for k in
            ("army", "af", "navy", "marines", "regular", "rf", "pf", "territorial", "total") if k in v]
    note = f" ({r['note']})" if r.get("note") else ""
    period = str(r["p"])
    when = y if period == str(y) else f"Dec. 31, {y}" if period.endswith("-12") else f"fourth quarter {y}"
    return table(f"Republic of Vietnam Armed Forces, {when}", rows,
                 (r.get("now_source") if col == "now" else r.get("source")) + note)


def allies_html(y):
    s, r = _row("war-fwmaf-strength", str(y))
    if r is None:
        return ""
    col = "now" if r.get("now") is not None else "first"
    v = r[col]
    bn = r.get("battalions") or {}
    rows = [(war.LABELS[k], war.persons(v[k]), str(bn[k]) if k in bn else "") for k in
            ("korea", "australia", "thailand", "nz", "phil", "roc", "spain", "total") if k in v]
    src = (r.get("now_source") if col == "now" else r.get("source")) + (f"; {r['printed']}" if r.get("printed") else "")
    return table(f"Other allied forces in South Vietnam, {y}", rows, src, "Maneuver bns." if bn else None)


def block(iso, y):
    """The day's block: the caption, forces.py's tables for the year, the RVNAF's and the allies' of the year before."""
    inner = forces_html(y) + rvn_html(y - 1) + allies_html(y - 1)
    if not inner:
        return ""
    p = proclamation(y)
    d = third_saturday(y)
    day = f"{d.strftime('%B')} {d.day}, {y}"
    if p:
        proc = f'the third Saturday in May, by <a href="{p[2]}">{esc(p[0])}</a> ({esc(p[1])})'
    else:
        proc = "the third Saturday in May (the year's proclamation not read)"
    return (f'<div class="wart afd" id="afd-{y}"><p class="wart-cap">Armed forces, Armed Forces Day, {esc(day)}</p>'
            f'<p class="wart-foot">Armed Forces Day: {proc}. The forces of {y - 1}, as the sources give them by year.</p>{inner}</div>')


STYLE = """<style id="afdstyle">
/* Armed Forces Day (tools/bib/afday.py, STYLE); the panel and the caption are the war table's */
div.afd .afd-t{margin:.5rem 0 .1rem;font-weight:600}
div.afd table.afd{border-collapse:collapse;width:auto;min-width:60%;table-layout:auto}
div.afd table.afd th,div.afd table.afd td{text-align:left;padding:.08rem .8rem .08rem 0;border-bottom:1px solid var(--rule);font-weight:400}
div.afd table.afd td{text-align:right}
div.afd table.afd thead th{color:var(--muted);font-weight:600;font-size:.72rem;border-bottom:1px solid var(--ink)}
</style>"""
