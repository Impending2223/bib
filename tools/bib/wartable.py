"""The Southeast Asia table: the war's numbers, apart from the month's economic tables, under the first Monday of the
month they refer to.

    indicators/war-*.yaml     the series (kind: war): U.S. deaths and strength (tools/indicators/make_war.py); the enemy's
                              order of battle, the national estimate, infiltration, the enemy and RVNAF killed, the RVNAF's
                              and the other allies' strength (tools/indicators/make_war_forces.py); the attack sorties
                              (tools/indicators/make_war_air.py)
    tools/bib/war.py          their cells
    tools/bib/dayblocks.py    sets this table in the day layout, under its date (a day block)

The owner's request, Oct. 22, 2026: the military numbers apart from the macroeconomic ones, "in a separate table
altogether", on "the first X of each month"; renamed, refiled and restyled Nov. 4, 2026 ("Southeast Asia, MMM YYYY", on
"the first Monday of each month to which its figures refer", the indicators' title and background).

STYLE (keep it):
 1. Filing, as the indicators': by the period the figures cover, not the date they were given. A month's rows, the
    quarter ending in it and the year ending in it (a quarter in its last month, a year in December) make one table,
    "Southeast Asia, Jan. 1966", set under the FIRST MONDAY of that month. Where the calendar does not hold that Monday,
    the nearest day it holds within the month (table_date); a month it holds no day of has no table.
 2. A standard table, as the indicators' (indicators STYLE 1, 18): the page's own background, no panel or rule above;
    one title, its caption, in the indicators caption's type, color and case, centered, between 〈〈 and 〉〉 (the
    Southeast Asia tables before and after, on whatever page, the Monday's date on hover; none at the first or the
    last). No small-capital title above it (contents.day_mark, titled=False) and no descriptive line under it: what
    the figures are is the servant's and the master's (6). Under the date and the day's entries, before the day's
    documents.
 3. Two columns, Reported then | Later, each figure with its date in grey under it, the year always given: "then", the
    figure as first given (the indicators' "As first reported"); "later", a revision or a retrospective (the indicators'
    "Revised, today"), U.S. deaths and strength today's. A figure read once, from a source dated more than a year after
    its period, is "later" (tools/indicators/make_war_forces.py). Concepts that are not comparable never share a row
    (indicators STYLE 8): MACV's old and new orders of battle, the national estimate, and the quarterly enemy strength
    are separate series.
 4. Each series a tbody: its name (linked to its statement) and period on a line of its own across both columns, the
    two cells under it, so the table fits a 400px phone without sideways scrolling (the owner hates panning).
 5. Order (ORDER in tools/bib/indicators.py), forces above casualties (the owner, Nov. 4, 2026): the forces, U.S.
    strength, the enemy's (order of battle, old format, estimate, quarter's end), infiltration, the RVNAF's and the
    other allies' strength, the attack sorties (by country, by route package); then the casualties, U.S. deaths, the
    enemy killed, the RVNAF killed.
 6. Concepts and sources: the master's (indicators/concepts.yaml), the war statements written as servants after the
    table where a series first appears on the page (not after the month table), "Southeast Asia: concepts and
    sources", each piece only where the page's tables file a period it concerns (tools/bib/concepts.py, its STYLE). A
    row's name links to its servant on the page, else the master.
 7. Contents: the first table of each year on a page is listed in the page's contents and in the Vietnam thread's
    "Tables and maps", by its title ("Southeast Asia, Jan. 1966": a month and year keep their comma, only a bare year
    drops it, as the map's "Southeast Asia 1966"); the rest are not (they are under every month, as the
    indicators are). Above that first table stands the year's map, "Southeast Asia 1966" (tools/bib/vnmap.py, STYLE 8).
"""
import calendar
import datetime
import re

from . import concepts, war
from .markup import to_html

MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
THREADS = ["vietnam"]
TITLE = "Southeast Asia"


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def first_monday(y, m):
    d = datetime.date(y, m, 1)
    return d + datetime.timedelta(days=(0 - d.weekday()) % 7)


def table_date(month, held=None):
    """'1966-01' -> the first Monday of that month; where held (the calendar's days) lacks it, the nearest day held
    within the month (the earlier on a tie), or None where the month has none (STYLE 1)."""
    y, m = int(month[:4]), int(month[5:7])
    d = first_monday(y, m)
    if held is None or d.isoformat() in held:
        return d
    days = [datetime.date(y, m, k) for k in range(1, calendar.monthrange(y, m)[1] + 1)]
    days = [x for x in days if x.isoformat() in held]
    return min(days, key=lambda x: (abs((x - d).days), x)) if days else None


def load():
    from .indicators import load as ld, ORDER
    data = ld()
    sids = [x for x in ORDER if data.get(x, {}).get("kind") == "war"]
    sids += sorted(x for x, s in data.items() if s.get("kind") == "war" and x not in sids)
    return data, sids


def filed():
    """{'1965-02-04': ('1965-01', [(sid, s, r)])}: every war row, by the date of its table."""
    from .indicators import period_end
    from .dayblocks import held_on_disk
    data, sids = load()
    held = held_on_disk()
    out = {}
    for sid in sids:
        s = data[sid]
        for r in s.get("rows", []):
            e = period_end(r["p"])
            month = f"{e.year}-{e.month:02d}"
            d = table_date(month, held)
            if d is None:
                continue
            out.setdefault(d.isoformat(), (month, []))[1].append((sid, s, r))
    for d, (month, rows) in out.items():          # within a series: months, quarters, then the year
        rows.sort(key=lambda t: (sids.index(t[0]), 0 if "-" in str(t[2]["p"]) else 1 if "Q" in str(t[2]["p"]) else 2))
    return out


def month_name(month):
    """'1966-01' -> 'Jan. 1966': the series' abbreviation, no comma before the year."""
    return f"{MON[int(month[5:7]) - 1]} {month[:4]}"


def title(month):
    """'Southeast Asia, Sept. 1966': the comma kept before a month and year; only a bare year drops it (STYLE 2)."""
    return f"{TITLE}, {month_name(month)}"


class Plan:
    """Per part: the war tables the page shows, the series each first appears in, each series' servant text."""

    def __init__(self, lst, dates):
        from . import calsplit
        from .indicators import period_end
        self.parts = {}
        info = calsplit.parts(lst)
        f = filed()
        master = concepts.load().get("series") or {}
        ends = {}
        for d in sorted(dates):
            if d not in f:
                continue
            part = calsplit.half_of_date(lst, d) if calsplit.cfg(lst) else 1
            P = self.parts.setdefault(part, {"key": info[part - 1]["page"] if calsplit.cfg(lst) else lst.key,
                                             "first": {}, "text": {}, "years": set()})
            for sid, s, r in f[d][1]:
                ends.setdefault(part, {}).setdefault(sid, set()).add(period_end(r["p"]))
                P["first"].setdefault(sid, d)
        for part, P in self.parts.items():
            for sid, es in ends.get(part, {}).items():
                t = master.get(sid)
                try:
                    P["text"][sid] = concepts.render(t, sorted(es)) if t else ""
                except ValueError:
                    P["text"][sid] = ""

    def href(self, part, sid):
        P = self.parts.get(part) or {}
        if P.get("text", {}).get(sid):
            return f"#ind-{P['key']}-{sid}"
        return f"{concepts.MASTER}#{sid}"


def rows_html(rows, year, href):
    from .indicators import period_label, date_label
    out = []
    for sid, s, r in rows:
        name = (f'<a href="{esc(href(sid))}">{esc(s["name"])}</a> '
                f'<span class="per">{esc(period_label(r["p"]))}</span>')
        cells = []
        for col, rk in (("first", "released"), ("now", "now_released")):
            c = war.cell(sid, s, r, col)
            if c != "—":
                tip = war.tip(sid, r, col)
                src = r.get("source" if col == "first" else "now_source") or (s.get(col if col == "now" else "then") or {}).get("source", "")
                c = f'<span title="{esc(tip)}">{c}</span>'
                when = r.get(rk)
                if when:
                    c += f'<span class="wr" title="{esc(src)}">{esc(date_label(when))}</span>'
                elif col == "now":
                    c += f'<span class="wr" title="{esc(src)}">today</span>'
            cells.append(c)
        out.append(f'<tbody><tr class="wn"><th colspan="2">{name}</th></tr>'
                   f'<tr><td>{cells[0]}</td><td>{cells[1]}</td></tr></tbody>')
    return "".join(out)


def servant(plan, part, sids, at):
    P = plan.parts.get(part)
    if not P:
        return ""
    sids = [x for x in sids if P["text"].get(x)]
    if not sids:
        return ""
    data, _ = load()
    out = [f'<div class="ind-defs ind-srv war-srv" id="ind-{P["key"]}-at-war-{esc(at)}">'
           f'<p class="ind-cap">{TITLE}: concepts and sources</p><dl>']
    for sid in sids:
        out.append(f'<dt id="ind-{P["key"]}-{esc(sid)}"><a href="{concepts.MASTER}#{esc(sid)}">'
                   f'{esc(data[sid]["name"])}</a></dt><dd>{to_html(P["text"][sid])}</dd>')
    out.append(f'</dl><p class="ind-master">{concepts.LINE.format(a=f"<a href={chr(34)}{concepts.MASTER}{chr(34)}>")}</p></div>')
    return "".join(out)


def sequence(held):
    """The Southeast Asia tables the calendar shows, by date: those on a day it holds (STYLE 2)."""
    return sorted(d for d in filed() if d in held)


def block(plan, part, iso, seq=None):
    """The Southeast Asia table for its date (with the servant of the series first used there), or ''. seq: every
    table's date in order (sequence), for the caption's 〈〈 and 〉〉 (STYLE 2)."""
    from .indicators import caption, date_label
    f = filed().get(iso)
    if not f:
        return ""
    month, rows = f
    year = int(iso[:4])
    h = lambda sid: plan.href(part, sid)
    nav = [None, None]
    if seq and iso in seq:
        j = seq.index(iso)
        nav = [(f"#war-{filed()[seq[k]][0]}", date_label(seq[k], year)) if 0 <= k < len(seq) else None
               for k in (j - 1, j + 1)]
    out = (f'<div class="wart" id="war-{month}">{caption(title(month), *nav)}'
           '<table><thead><tr><th>Reported then</th><th>Later</th></tr></thead>'
           + rows_html(rows, year, h) + "</table></div>")
    P = plan.parts.get(part) or {}
    new = []
    for sid, s, r in rows:
        if P.get("first", {}).get(sid) == iso and sid not in new:
            new.append(sid)
    return out + servant(plan, part, new, month)


def problems(series):
    """For ./bib check: every Southeast Asia table falls on a day the calendar holds (else it is not shown: a warning),
    but for one past the calendar's last day."""
    from . import dayblocks
    out = []
    import datetime as dt
    held = dayblocks.held_days(series)

    def inside(d):                  # within the calendar's run of days, not past its end or in a gap of seasons
        x = dt.date.fromisoformat(d)
        return all((x + dt.timedelta(days=k)).isoformat() in held for k in (-31, 31))
    for d, (month, rows) in sorted(filed().items()):
        if d not in held and inside(d):
            out.append(("warn", f"Southeast Asia table {month}", f"its day, {d}, is in no dated section of the calendar"))
    from . import afday
    for d, y in afday.dates().items():
        if d not in held:
            out.append(("warn", f"Armed Forces Day {y}", f"{d} is in no dated section of the calendar"))
    return out


STYLE = """<style id="wartstyle">
/* The Southeast Asia table, under the first Monday (tools/bib/wartable.py, STYLE); Armed Forces Day's (afday.py) */
div.wart{margin:.6rem 0 .8rem;font-family:var(--sans);font-size:.8rem;line-height:1.35;color:var(--ink);
  font-variant-numeric:tabular-nums}
div.wart .ind-cap{margin:0 0 .15rem;font-family:var(--sans);font-size:.72rem;font-weight:600;color:var(--muted);
  text-transform:uppercase;letter-spacing:.06em;text-align:center}
div.wart .ind-cap a.tnb,div.wart .ind-cap a.tnb:hover{color:var(--muted);text-decoration:none}
div.wart .wart-foot{margin:0 0 .35rem;font-size:.72rem;color:var(--muted);line-height:1.35}
div.wart table{border-collapse:collapse;width:100%;table-layout:fixed}
div.wart thead th{text-align:left;font-weight:600;color:var(--muted);font-size:.72rem;padding:.1rem .4rem .15rem 0;
  border-bottom:1px solid var(--ink)}
div.wart tr.wn th{text-align:left;font-weight:600;padding:.35rem 0 .05rem;border:0}
div.wart tr.wn a{color:inherit;text-decoration-color:var(--rule)}
div.wart .per,div.wart .u,div.wart .wr{color:var(--muted);font-weight:400}
div.wart td{vertical-align:top;padding:0 .8rem .3rem 0;border-bottom:1px solid var(--rule);overflow-wrap:anywhere}
div.wart td:last-child{padding-right:0}
div.wart .wr,div.wart .wnote{display:block;font-size:.72rem}
div.wart .kv{display:inline-grid;grid-template-columns:minmax(2.5em,auto) auto;column-gap:.4rem;max-width:100%}
div.wart .kv .v{text-align:right}
div.war-srv{margin:.2rem 0 1rem}
</style>"""
