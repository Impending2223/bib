"""The war table: the war's numbers, apart from the month's economic tables, under the first Thursday of each month.

    indicators/war-*.yaml     the series (kind: war): U.S. deaths and strength (tools/indicators/make_war.py); the enemy's
                              order of battle, the national estimate, infiltration, the enemy and RVNAF killed, the RVNAF's
                              and the other allies' strength (tools/indicators/make_war_forces.py)
    tools/bib/war.py          their cells
    tools/bib/dayblocks.py    sets this table in the day layout, under its date (a day block)

The owner's request, Oct. 22, 2026: the military numbers apart from the macroeconomic ones, "in a separate table
altogether", on a day with a facial justification, "something like the first X of each month", so the figures are not
oppressive.

STYLE (keep it):
 1. Filing, as the indicators': by the period the figures cover, not the date they were given. A month's rows, the
    quarter ending in it and the year ending in it make one table, "The war, January 1965", set under the FIRST THURSDAY
    of the next month: the day of the week the command in Saigon and the Pentagon gave out the week's casualty figures
    in these years (a convention for the table's place, as the plan of Oct. 20, 2026 has it; the releases themselves
    not read: notes/leads.md). A table whose Thursday the calendar does not hold is not shown (Jan. 1969's, Feb. 6).
 2. Its own block, not a continuation of the month table: a caption in small capitals over a solid rule in the text's
    color (the economic tables have a grey caption and grey rules), the sans at the tables' size, a light panel, and a
    foot line on the page's first table saying what the day is. Under the date and the day's entries, before the day's
    documents.
 3. Two columns, Reported then | Later, each figure with its date in grey under it, the year always given: "then", the figure as first given
    (the indicators' "As first reported"); "later", a revision or a retrospective (the indicators' "Revised, today"),
    U.S. deaths and strength today's. A figure read once, from a source dated more than a year after its period, is
    "later" (tools/indicators/make_war_forces.py). Concepts that are not comparable never share a row (indicators
    STYLE 8): MACV's old and new orders of battle, the national estimate, and the quarterly enemy strength are
    separate series.
 4. Each series a tbody: its name (linked to its statement) and period on a line of its own across both columns, the
    two cells under it, so the table fits a 400px phone without sideways scrolling (the owner hates panning).
 5. Order: U.S. deaths and strength; the enemy (order of battle, old format, estimate, quarter's end, infiltration,
    killed); the RVNAF (killed, strength); the other allies (ORDER in tools/bib/indicators.py).
 6. Concepts and sources: the master's (indicators/concepts.yaml), the war statements written as servants after the
    war table where a series first appears on the page (not after the month table), "The war: concepts and sources",
    each piece only where the page's war tables file a period it concerns (tools/bib/concepts.py, its STYLE). A row's
    name links to its servant on the page, else the master.
 7. Contents: the first war table of each year on a page is listed in the page's contents and in the Vietnam thread's
    "Tables and maps" ("The war, 1965: first Thursdays"); the rest are not (they are under every month, as the
    indicators are).
"""
import calendar
import datetime
import re

from . import concepts, war
from .markup import to_html

MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
THREADS = ["vietnam"]
FOOT = ("Filed by the month the figures cover and set under the first Thursday after it, the day of the week the "
        "command in Saigon and the Pentagon gave out the week's casualty figures. Reported then: the figure as first "
        "given, with its date. Later: as revised or given afterward, with its date; U.S. deaths and strength as the "
        "Defense Department's records give them today.")


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def first_thursday(y, m):
    d = datetime.date(y, m, 1)
    return d + datetime.timedelta(days=(3 - d.weekday()) % 7)


def table_date(month):
    """'1965-01' -> the first Thursday of the next month."""
    y, m = int(month[:4]), int(month[5:7])
    return first_thursday(y + (m == 12), m % 12 + 1)


def load():
    from .indicators import load as ld, ORDER
    data = ld()
    sids = [x for x in ORDER if data.get(x, {}).get("kind") == "war"]
    sids += sorted(x for x, s in data.items() if s.get("kind") == "war" and x not in sids)
    return data, sids


def filed():
    """{'1965-02-04': ('1965-01', [(sid, s, r)])}: every war row, by the date of its table."""
    from .indicators import period_end
    data, sids = load()
    out = {}
    for sid in sids:
        s = data[sid]
        for r in s.get("rows", []):
            e = period_end(r["p"])
            month = f"{e.year}-{e.month:02d}"
            d = table_date(month).isoformat()
            out.setdefault(d, (month, []))[1].append((sid, s, r))
    for d, (month, rows) in out.items():          # within a series: months, quarters, then the year
        rows.sort(key=lambda t: (sids.index(t[0]), 0 if "-" in str(t[2]["p"]) else 1 if "Q" in str(t[2]["p"]) else 2))
    return out


def month_name(month):
    return f"{calendar.month_name[int(month[5:7])]} {month[:4]}"


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
           '<p class="ind-cap">The war: concepts and sources</p><dl>']
    for sid in sids:
        out.append(f'<dt id="ind-{P["key"]}-{esc(sid)}"><a href="{concepts.MASTER}#{esc(sid)}">'
                   f'{esc(data[sid]["name"])}</a></dt><dd>{to_html(P["text"][sid])}</dd>')
    out.append(f'</dl><p class="ind-master">{concepts.LINE.format(a=f"<a href={chr(34)}{concepts.MASTER}{chr(34)}>")}</p></div>')
    return "".join(out)


def block(plan, part, iso, first_on_page):
    """The war table for its date (with the servant of the series first used there), or ''."""
    f = filed().get(iso)
    if not f:
        return ""
    month, rows = f
    year = int(iso[:4])
    h = lambda sid: plan.href(part, sid)
    foot = f'<p class="wart-foot">{esc(FOOT)}</p>' if first_on_page else ""
    out = (f'<div class="wart" id="war-{month}"><p class="wart-cap">The war, {esc(month_name(month))}</p>{foot}'
           '<table><thead><tr><th>Reported then</th><th>Later</th></tr></thead>'
           + rows_html(rows, year, h) + "</table></div>")
    P = plan.parts.get(part) or {}
    new = []
    for sid, s, r in rows:
        if P.get("first", {}).get(sid) == iso and sid not in new:
            new.append(sid)
    return out + servant(plan, part, new, month)


def problems(series):
    """For ./bib check: every war table falls on a day the calendar holds (else it is not shown: a warning), but for the
    one past the calendar's last day."""
    from . import dayblocks
    out = []
    import datetime as dt
    held = dayblocks.held_days(series)

    def inside(d):                  # within the calendar's run of days, not past its end or in a gap of seasons
        x = dt.date.fromisoformat(d)
        return all((x + dt.timedelta(days=k)).isoformat() in held for k in (-31, 31))
    for d, (month, rows) in sorted(filed().items()):
        if d not in held and inside(d):
            out.append(("warn", f"war table {month}", f"its first Thursday, {d}, is in no dated section of the calendar"))
    from . import afday
    for d, y in afday.dates().items():
        if d not in held:
            out.append(("warn", f"Armed Forces Day {y}", f"{d} is in no dated section of the calendar"))
    return out


STYLE = """<style id="wartstyle">
/* The war table, under the first Thursday (tools/bib/wartable.py, STYLE) */
div.wart{margin:.6rem 0 .8rem;padding:.45rem .6rem .5rem;background:var(--panel);border-top:2px solid var(--ink);
  font-family:var(--sans);font-size:.8rem;line-height:1.35;color:var(--ink);font-variant-numeric:tabular-nums}
div.wart .wart-cap{margin:0 0 .25rem;font-size:.74rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
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
