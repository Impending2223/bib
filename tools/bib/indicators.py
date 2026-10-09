"""Economic indicators in the calendar, filed by the period they report on.

    indicators/<id>.yaml   one series: its definitions then and now, and one row per reporting
                           period (p: 1961-03, 1961Q2, FY1962, 1961) with the figure as first
                           reported, its release date and source, and the figure as revised today.
                           Made by tools/indicators/make_indicators.py; see that script.

Filing. Each calendar month section whose dates hold the last day of a period carries that
period's figures in a table under its heading: months in their month, quarters in the quarter's
last month, fiscal years (ending June 30) in June, calendar years in December. Periods that end
before the first dated section go to it (the Prologue). A block of definitions, "Indicators:
concepts and sources", goes before the Prologue; each series name in a table links to its entry.

STYLE (settled; keep it, and fix anything that drifts from it):
 1. Columns: Indicator | As first reported | Released | Revised, today. Gallup's approval (kind: poll) in a table
    of its own under it, set off by a rule and its own caption ("Presidential approval, Gallup"; the first table's
    "Economic indicators"), on the same plan: Reading (with the field dates) | As published | Released | Today. "Released" is the date the
    first-reported figure was published (or the Economic Report transmitted); its source shows on
    hover.
 2. Periods: "Mar. 1961", "Q1 1961", "FY1962" (July 1961-June 1962), "1961".
 3. Money in the Economist's style: "$499.8bn", "$17.3bn". One scale per group: every dollar figure
    in Output, Federal finance, and International is in $bn, one decimal. The YAML keeps the source's
    own unit and precision; the exact source figure shows on hover.
 4. People: "52.0m"; changes in persons, "+24,000". Rates: "6.9%"; changes in points, "+0.1 pt".
    Indexes: one decimal, the base after in grey, "127.5 (1947-49=100)".
 5. Changes, on the same basis in both value columns (CHANGE in the script): monthly series, percent
    from the prior month, not annualized; quarterly series, percent from the prior quarter at an
    annual rate, marked "ar". Positive changes carry "+"; minus is U+2212.
    CPI, WPI and industrial production add the change from the same month a year earlier, in
    parentheses, "y/y" in grey: "+0.1% (+1.0% y/y)". Each column computes it in its own figures:
    the year-earlier figure in the same release or Report, and today's series. Not annualized
    monthly rates: the CPI and WPI are not seasonally adjusted, and one-decimal indexes make a
    monthly rate times twelve mostly rounding.
 6. Receipts / expenditures / balance: one line each, label left, figure right-aligned in tabular
    figures; estimates as further "Balance, est." lines. A negative balance is a deficit.
 7. "—" means no figure in this column by design (a different concept, or none published);
    "n.a." means the source marks the figure not available.
 8. Concepts that are not comparable never share a row. Give each its own row, with "—" in the
    other's column: a contemporary estimate fills "As first reported", a retrospective one
    "Revised, today" (the CEA and CBO output gaps).
 9. Exception to 3: a source given in whole billions keeps its precision ("$51bn", the CEA gap),
    and a shortfall stated as a positive amount says so ("below potential").
10. In Federal finance and International the group header carries "$bn" and cells carry bare
    figures; the gold stock alone has two decimals (its monthly changes run to tens of millions).
    Stacked figures sit in a fixed two-column grid (label 7.5em, figure 4.2em) so they align
    down the column.
11. Source qualifiers stay: "about $28bn", "some $30–40bn"; a note the source attaches to one
    figure (NOTE in the script) shows after it in grey: "(Q1–Q3, annual rate)".
12. Definitions (DEFS): what the figure was then, what it is today, and pointers, in the brief's
    register: compact, plain, no judgment of the figures.
"""
import calendar
import datetime
import os
import re

from . import store
from .markup import to_html

DIR = os.path.join(store.ROOT, "indicators")
ORDER = ["cpi", "wpi", "deflator", "unemployment", "payrolls", "industrial-production", "gnp", "real-gnp",
         "gap-cea", "gap-cbo", "administrative-budget", "cash-budget", "federal-national-accounts",
         "balance-of-payments", "gold-stock", "approval"]
GROUP = {"cpi": "Prices", "wpi": "Prices", "deflator": "Prices",
         "unemployment": "Employment", "payrolls": "Employment",
         "industrial-production": "Output", "gnp": "Output", "real-gnp": "Output",
         "gap-cea": "Output", "gap-cbo": "Output",
         "administrative-budget": "Federal finance", "cash-budget": "Federal finance",
         "federal-national-accounts": "Federal finance",
         "balance-of-payments": "International", "gold-stock": "International",
         "approval": "Opinion"}
FIELD_LABEL = {"receipts": "Receipts", "expenditures": "Expenditures", "payments": "Payments", "balance": "Balance"}
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]

ERP62 = "https://www.govinfo.gov/app/details/SERIALSET-12497_00_00-002-0278-0000"
ERP63 = "https://www.govinfo.gov/app/details/SERIALSET-12600_00_00-002-0028-0000"
ERP64 = "https://www.govinfo.gov/app/details/SERIALSET-12658_00_00-002-0278-0000"
F = "https://fred.stlouisfed.org/series/"
A = "https://alfred.stlouisfed.org/series?seid="
APPROVAL = "https://www.presidency.ucsb.edu/statistics/data/presidential-job-approval"
DEFS = {
    "approval": f"Gallup: \"Do you approve or disapprove of the way [the President] is handling his job as President?\" Each reading, filed by the month its fieldwork ended. As published: the release, in *The Gallup Poll: Public Opinion, 1935–1971*, vol. III (1972), by page (K–J Cong. II.E); approval among Democrats, independents, and Republicans in grey where the release gives it; \"—\" for a reading Gallup did not release at the time. Today: Gallup's series as the [American Presidency Project]({APPROVAL}) compiles it (Gerhard Peters), which differs from the releases in places: Sept. 12–17, 1963, released at 62 percent approving, is 56 in the series today. The race for 1964 and the issues are calendar entries in the thread Opinion.",
    "cpi": f"BLS. Retail prices of a fixed basket bought by city wage-earner and clerical-worker families; 1947–49=100 through Dec. 1961, 1957–59=100 from Jan. 1962. Today: CPI for all urban consumers, 1982–84=100. Neither seasonally adjusted. First releases: [ALFRED]({A}CPIAUCNS); today: [FRED]({F}CPIAUCNS).",
    "wpi": f"BLS. Primary-market prices of all commodities; 1947–49=100 through 1961, 1957–59=100 from 1962. Today the producer price index, all commodities, 1982=100 ([FRED]({F}PPIACO)). First reported here means as tabled in the next January's *Economic Report* ([1962]({ERP62}), Table B-40; [1963]({ERP63}), Table C-41; [1964]({ERP64}), Table C-41).",
    "deflator": f"Commerce, Office of Business Economics. GNP in current dollars over GNP in 1954 dollars, times 100, computed from the release that first carried the quarter ([ALFRED]({A}GNP)). Today BEA's GNP deflator, chained, 2017=100 ([FRED]({F}GNPDEF)).",
    "unemployment": f"Unemployed as a percent of the civilian labor force, seasonally adjusted, from the Current Population Survey (household survey), collected by Census, published by BLS. Then ages 14 and over; today's series ages 16 and over ([ALFRED]({A}UNRATE); [FRED]({F}UNRATE)).",
    "payrolls": f"BLS establishment survey: wage and salary workers in nonagricultural establishments, seasonally adjusted. Today's figures are benchmarked to later counts of insured employment ([ALFRED]({A}PAYEMS); [FRED]({F}PAYEMS)).",
    "industrial-production": f"Federal Reserve Board. Physical output of manufacturing, mining, and utilities; 1957=100 then, 2017=100 today ([ALFRED]({A}INDPRO); [FRED]({F}INDPRO)).",
    "gnp": f"Commerce, Office of Business Economics. Output of the nation's residents at market prices, seasonally adjusted annual rates. Today's BEA figures carry later definitions and benchmarks ([ALFRED]({A}GNP); [FRED]({F}GNP)).",
    "real-gnp": f"GNP in 1954 prices then; in chained 2017 dollars today (chain weighting from 1996) ([ALFRED]({A}GNPC96); [FRED]({F}GNPC96)).",
    "gap-cea": f"Council of Economic Advisers. Potential GNP: a 3½ percent trend line through actual GNP in mid-1955, taken as full use of resources; full employment taken as 4 percent unemployment, an interim target. Gap: potential less actual, in 1961 prices (Jan. 1962), 1962 prices (Jan. 1963), or 1963 prices (Jan. 1964). Each point of unemployment above 4 percent put at about 3 percent of output (Okun's relation). [*Economic Report*, Jan. 1962]({ERP62}), \"Full Production,\" p. 49; [Jan. 1963]({ERP63}), Chart 5; [Jan. 1964]({ERP64}), \"Unemployment and Unused Potential Output,\" p. 37. Arthur M. Okun, \"Potential GNP: Its Measurement and Significance,\" *Proceedings of the Business and Economic Statistics Section*, American Statistical Association (1962).",
    "gap-cbo": f"Congressional Budget Office, estimated decades later. Potential GDP: output at CBO's noncyclical rate of unemployment (about 5.5 percent for 1961) and trend productivity, from a model revised with each budget outlook. Gap: real GDP over potential, less 1, in percent; negative is output below potential. Not comparable with the CEA's figures: GDP not GNP, chained 2017 dollars, a later concept of full employment, a different benchmark. [FRED GDPPOT]({F}GDPPOT), [GDPC1]({F}GDPC1), [NROU]({F}NROU); CBO, *CBO's Method for Estimating Potential Output: An Update* (2001).",
    "administrative-budget": f"Three federal budgets were reported. The administrative budget: receipts and expenditures of federal funds only, the deficit of the headlines; fiscal years ending June 30. [*Economic Report*, Jan. 1962]({ERP62}), Table 7, p. 78, compares the three. Today: OMB's unified budget receipts, outlays, and deficit, recast back from the unified budget adopted for fiscal 1969 on the President's Commission on Budget Concepts (*Report*, 1967) ([FRED]({F}FYFSD)).",
    "cash-budget": f"The consolidated cash statement: federal receipts from and payments to the public, including the trust funds (Social Security, highways). Today: the unified budget, as above ([FRED]({F}FYONET)).",
    "federal-national-accounts": f"Commerce: federal receipts and expenditures in the national income accounts, seasonally adjusted annual rates; accrual basis, excluding loans and purchases of land and existing assets. Today: BEA's federal current receipts and current expenditures, a narrower and later definition; their balance is not the old surplus or deficit ([FRED]({F}FGRECPT); [FGEXPND]({F}FGEXPND)).",
    "balance-of-payments": f"Commerce: the over-all balance, measured by the change in U.S. gold, convertible currencies, and liquid liabilities to foreigners; seasonally adjusted annual rates. The figure behind the gold and dollar measures of 1961–63. No longer published; no figure today. [*Economic Report*, Jan. 1963]({ERP63}), Table C-78; [Jan. 1964]({ERP64}), Table C-77.",
    "gold-stock": f"Treasury monetary gold stock, end of month, as compiled by NBER from the *Federal Reserve Bulletin* ([FRED]({F}M1476CUSM144NNBR)). Not a revised series; one column.",
}


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def load():
    if not os.path.isdir(DIR):
        return {}
    out = {}
    for f in sorted(os.listdir(DIR)):
        if f.endswith(".yaml"):
            d = store.load_yaml(os.path.join(DIR, f))
            out[d["id"]] = d
    return out


# ---------------------------------------------------------------- periods and dates

def period_end(p):
    p = str(p)
    if p.startswith("FY"):
        return datetime.date(int(p[2:]), 6, 30)
    if "Q" in p:
        y, q = p.split("Q")
        m = 3 * int(q)
        return datetime.date(int(y), m, calendar.monthrange(int(y), m)[1])
    if re.match(r"^\d{4}$", p):
        return datetime.date(int(p), 12, 31)
    y, m = int(p[:4]), int(p[5:7])
    return datetime.date(y, m, calendar.monthrange(y, m)[1])


def period_label(p):
    p = str(p)
    if p.startswith("FY"):
        return p
    if "Q" in p:
        y, q = p.split("Q")
        return f"Q{q} {y}"
    if re.match(r"^\d{4}$", p):
        return p
    return f"{MON[int(p[5:7]) - 1]} {p[:4]}"


def date_label(iso, year=None):
    d = datetime.date.fromisoformat(str(iso))
    s = f"{MON[d.month - 1]} {d.day}"
    return s if year == d.year else f"{s}, {d.year}"


# ---------------------------------------------------------------- numbers

MINUS = "−"


def num(v, nd=1, comma=True):
    if v is None:
        return "n.a."
    if isinstance(v, str):
        return v
    s = f"{abs(v):,.{nd}f}" if comma else f"{abs(v):.{nd}f}"
    return (MINUS if v < 0 else "") + s


def signed(v, nd=1):
    s = f"{abs(v):,.{nd}f}"
    return ("+" if v > 0 else MINUS if v < 0 else "±") + s


def to_bn(v, unit):
    """Dollar figures to $bn: the source unit is millions or billions of dollars."""
    if v is None or isinstance(v, str):
        return v
    return v / 1000 if unit and "millions of dollars" in unit else v


def grey(t):
    return f'<span class="u">{esc(t)}</span>' if t else ""


def base_of(unit):
    """The index base or price basis worth showing after a level, from the stored unit."""
    if not unit:
        return None
    m = re.search(r"(\d{4}(?:–\d{2})?=100)", unit)
    if m:
        return m.group(1)
    m = re.search(r"(\d{4}) dollars", unit)
    if m:
        return f"{m.group(1)} dollars" if "chained" not in unit else f"chained {m.group(1)} dollars"
    return None


def chg_text(kind, c):
    if c is None:
        return ""
    if kind == "pct":
        return f", {signed(c)}%"
    if kind == "pct_ar":
        return f", {signed(c)}% {grey('ar')}"
    if kind == "pts":
        return f", {signed(c)} pt"
    return ""


def yoy_text(y):
    return f" ({signed(y)}%\u00a0{grey('y/y')})" if y is not None else ""


def single(sid, v, unit, kind, c, q=None, yoy=None):
    """One figure in its series' form."""
    qual = f"{esc(q)} " if q else ""
    if v is None:
        return "n.a."
    if sid == "unemployment":
        return f"{num(v)}%" + chg_text(kind, c)
    if sid == "payrolls":
        out = f"{v / 1000:.1f}m"
        return out + (f", {signed(c * 1000, 0)}" if c is not None else "")
    if sid == "gold-stock":
        lines = [("Stock", num(to_bn(v, unit), 2))]
        if c is not None:
            lines.append(("Change", signed(c / 1000, 2)))
        return '<span class="kv">' + "".join(
            f'<span class="k">{esc(a)}</span><span class="v">{esc(b)}</span>' for a, b in lines) + "</span>"
    if sid == "gap-cea":
        out = f"{qual}${num(v, 0)}bn"
        b = base_of(unit)
        return out + " " + grey(f"below potential ({b})" if b else "below potential")
    if sid in ("gnp", "real-gnp"):
        out = f"{qual}${num(to_bn(v, unit))}bn"
        b = base_of(unit)
        if b:
            out += " " + grey(f"({b})")
        return out + chg_text(kind, c)
    if sid == "gap-cbo":
        return f"{num(v)}% {grey('of potential')}"
    b = base_of(unit)
    out = f"{qual}{num(v)}" + (" " + grey(f"({b})") if b else "") + chg_text(kind, c)
    if yoy is not None and c is None:
        return out + f", {signed(yoy)}%\u00a0{grey('y/y')}"
    return out + yoy_text(yoy)


def stacked(fields, v, unit, ests, year, field_names):
    """Receipts / expenditures / balance, one line each, figures right-aligned, $bn."""
    lines = []
    for k in fields:
        x = v.get(k) if v else None
        lines.append((FIELD_LABEL.get(k, k.capitalize()), num(to_bn(x, unit))))
    for e in ests or []:
        bal = e["value"].get("balance")
        d = datetime.date.fromisoformat(str(e["as_of"]))
        lines.append((f"Est. {MON[d.month - 1]} {d.year}", num(to_bn(bal, unit))))
    return '<span class="kv">' + "".join(
        f'<span class="k">{esc(a)}</span><span class="v">{esc(b)}</span>' for a, b in lines) + "</span>"


def exact(v, unit):
    """The source figure as stored, for the hover title."""
    if isinstance(v, dict):
        return "; ".join(f"{k} {x}" for k, x in v.items()) + (f" ({unit})" if unit else "")
    return f"{v}" + (f" ({unit})" if unit else "")


# ---------------------------------------------------------------- the table

def rows_for(data, lo, hi, first_section):
    out = []
    for sid in ORDER + [k for k in data if k not in ORDER]:
        s = data.get(sid)
        if not s:
            continue
        for r in s.get("rows", []):
            end = period_end(r["p"])
            if lo <= end <= hi or (first_section and end < lo):
                out.append((sid, s, r))
    return out


def cell_first(sid, s, r, year):
    if "first" not in r and not r.get("est"):
        return "—"
    unit, kind = r.get("unit"), s.get("change")
    if s.get("fields"):
        out = stacked(s["fields"], r.get("first"), unit, r.get("est"), year, s["fields"])
        return out + (f'<br>{grey(r["note"])}' if r.get("note") else "")
    out = single(sid, r["first"], unit, kind, r.get("chg"), r.get("q"), r.get("yoy"))
    return out + (" " + grey(f"({r['note']})") if r.get("note") else "")


def cell_now(sid, s, r):
    v = r.get("now")
    if v is None or (isinstance(v, dict) and not any(x is not None for x in v.values())):
        return "—"
    unit, kind = (s.get("now") or {}).get("unit"), s.get("change")
    if s.get("fields"):
        return stacked(s["fields"], v, unit, None, None, s["fields"])
    if sid in ("gnp", "real-gnp", "gold-stock"):
        unit = unit or ""
        if sid == "gold-stock":
            unit = "millions of dollars"
    return single(sid, v, unit, kind, r.get("chg_now"), yoy=r.get("yoy_now"))


def poll_row(sid, s, r, year):
    """A Gallup approval reading: (name, field dates, as published, released, today)."""
    def dates(a, b):
        da, db = datetime.date.fromisoformat(a), datetime.date.fromisoformat(b)
        if (da.year, da.month) == (db.year, db.month):
            return f"{MON[da.month - 1]} {da.day}–{db.day}"
        return f"{MON[da.month - 1]} {da.day}–{MON[db.month - 1]} {db.day}"
    def reading(v):
        if not v:
            return "—"
        parties = [f"{lab} {v[k]}" for k, lab in (("dem", "Dem."), ("ind", "Ind."), ("rep", "Rep.")) if v.get(k) is not None]
        return (f"{v['approve']}% approve, {v['disapprove']}% disapprove"
                + (" " + grey("(" + ", ".join(parties) + ")") if parties else ""))
    name = f"Approval of {r['president']}"
    first = reading(r.get("first"))
    if r.get("first"):
        first = f'<span title="The Gallup Poll, III, {r["page"]}">{first}</span>'
    rel = (f'<span title="The Gallup Poll, III, {r["page"]}">{esc(date_label(r["published"], year))}</span>'
           if r.get("published") else "—")
    now = reading(r.get("today"))
    if r.get("today"):
        now = f'<span title="{esc((s.get("now") or {}).get("source", ""))}">{now}</span>'
    return name, dates(r["from"], r["to"]), first, rel, now


def block(data, sec_from, sec_to, first_section, year):
    lo, hi = datetime.date.fromisoformat(sec_from), datetime.date.fromisoformat(sec_to)
    rows = rows_for(data, lo, hi, first_section)
    if not rows:
        return ""
    trs, shown, polls = [], set(), []
    for sid, s, r in rows:
        g = GROUP.get(sid)
        if s.get("kind") == "poll":
            g = None
        if g and g not in shown:
            shown.add(g)
            unit_note = " $bn" if g in ("Federal finance", "International") else ""
            trs.append(f'<tr class="g"><th colspan="4">{esc(g)}{grey(unit_note)}</th></tr>')
        if s.get("kind") == "poll":
            pname, per, first, rel, now = poll_row(sid, s, r, year)
            polls.append(f'<tr><td class="iname"><a href="#ind-def-{esc(sid)}">{esc(pname)}</a> '
                         f'<span class="per">{esc(per)}</span></td><td>{first}</td><td class="rel">{rel}</td><td>{now}</td></tr>')
            continue
        then, now = s.get("then") or {}, s.get("now") or {}
        name = f'<a href="#ind-def-{esc(sid)}">{esc(s["name"])}</a> <span class="per">{esc(period_label(r["p"]))}</span>'
        first = cell_first(sid, s, r, year)
        if "first" in r:
            first = f'<span title="{esc(exact(r["first"], r.get("unit")))}">{first}</span>'
        rel = "—"
        if r.get("released"):
            src = r.get("source") or (then.get("source") and f'{then["source"]}, released {r["released"]}')
            rel = f'<span title="{esc(src or "")}">{esc(date_label(r["released"], year))}</span>'
        nowv = cell_now(sid, s, r)
        if nowv != "—" and now.get("source"):
            nowv = f'<span title="{esc(now["source"] + (": " + exact(r["now"], now.get("unit")) if r.get("now") is not None else ""))}">{nowv}</span>'
        trs.append(f'<tr><td class="iname">{name}</td><td>{first}</td><td class="rel">{rel}</td><td>{nowv}</td></tr>')
    out = ""
    if trs:
        out += ('<div class="ind"><p class="ind-cap">Economic indicators</p><table><thead><tr><th>Indicator</th><th>As first reported</th>'
                '<th>Released</th><th>Revised, today</th></tr></thead><tbody>'
                + "".join(trs) + "</tbody></table></div>")
    if polls:                            # opinion apart: a reading has its field dates and no revision
        out += ('<div class="ind ind-op"><p class="ind-cap">Presidential approval, Gallup</p><table><thead><tr><th>Reading</th><th>As published</th>'
                '<th>Released</th><th>Today</th></tr></thead><tbody>' + "".join(polls) + "</tbody></table></div>")
    return out


def defs_block(data):
    items = []
    for sid in ORDER:
        if sid in data and sid in DEFS:
            items.append(f'<dt id="ind-def-{esc(sid)}">{esc(data[sid]["name"])}</dt>'
                         f'<dd>{to_html(DEFS[sid], lambda eid, shown: None)}</dd>')
    return ('<div class="ind-defs" id="indicators"><h3 data-short="Indicators">Indicators: concepts and sources</h3>'
            '<p class="logic">Under each month: the figures for that month, its quarter, fiscal year, or year, '
            'as first reported and as revised today. Monthly changes from the prior month; quarterly changes '
            'from the prior quarter at an annual rate (ar). "—": no figure in that column; "n.a.": not available in the source. '
            'Figures in $bn throughout federal finance and international; the source figure shows on hover. '
            'Data and transcriptions: indicators/ in the repository.</p><dl>'
            + "".join(items) + "</dl></div>")


STYLE = """<style>
/* class names here are prefixed or scoped: the page's own .n (entry notes) once made the first cell a block */
div.ind{margin:.4rem 0 1.1rem;overflow-x:auto}
div.ind table{border-collapse:collapse;font-family:var(--sans);font-size:.8rem;line-height:1.35;color:var(--ink);min-width:100%;font-variant-numeric:tabular-nums}
div.ind th,div.ind td{display:table-cell;text-align:left;vertical-align:top;padding:.2rem .6rem .2rem 0;border-bottom:1px solid var(--rule)}
div.ind thead th{color:var(--muted);font-weight:600}
div.ind th:last-child,div.ind td:last-child{padding-right:0}
@media (max-width:480px){div.ind th,div.ind td{padding-right:.3rem}}
div.ind tr.g th{padding-top:.55rem;color:var(--muted);font-weight:600;font-size:.75rem;text-transform:uppercase;letter-spacing:.04em;border-bottom:0}
div.ind tr.g th .u{text-transform:none;letter-spacing:0}
div.ind .per,div.ind .u,div.ind td.rel{color:var(--muted)}
div.ind td.iname a{color:inherit;text-decoration-color:var(--rule)}
div.ind .kv{display:inline-grid;grid-template-columns:minmax(3.5em,7.5em) auto;column-gap:.4rem}
div.ind .kv .v{text-align:right}
div.ind .ind-cap{margin:0 0 .15rem;font-family:var(--sans);font-size:.72rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
div.ind.ind-op{margin-top:1.2rem;padding-top:.45rem;border-top:2px solid var(--ink)}
div.ind.ind-op td.rel,div.ind.ind-op .per{white-space:nowrap}
div.ind-defs{font-family:var(--sans);font-size:.85rem;line-height:1.45;margin:1rem 0 1.5rem}
div.ind-defs dt{font-weight:600;margin-top:.6rem}
div.ind-defs dd{margin:.1rem 0 0 0;color:var(--ink)}
</style>"""


def inject(page, series, mode):
    """Put each calendar month's indicators under its heading, and the definitions before the Prologue."""
    data = load()
    if not data:
        return page
    done = False
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        dated = [s for s in lst.sections if s.extra.get("from") and s.extra.get("to")]
        for i, sec in enumerate(dated):
            year = int(str(sec.extra["to"])[:4])
            hid = f"{lst.key}--{sec.id}" if mode == "series" else sec.id
            if i == 0:
                pat0 = re.compile(r'(<h\d id="' + re.escape(hid) + r'")')
                page, n0 = pat0.subn(lambda m: defs_block(data) + "\n" + m.group(1), page, count=1)
            blk = block(data, str(sec.extra["from"]), str(sec.extra["to"]), i == 0, year)
            if not blk:
                continue
            pat = re.compile(r'(<h\d id="' + re.escape(hid) + r'"[^>]*>.*?</h\d>(?:\s*<p class="logic">.*?</p>)*)', re.S)
            page, n = pat.subn(lambda m: m.group(1) + "\n" + blk, page, count=1)
            done = done or bool(n)
    if done:
        page = page.replace("</head>", STYLE + "\n</head>", 1)
    return page


def problems():
    """For ./bib check: malformed periods, rows without a source, unknown series, missing definitions."""
    out = []
    for sid, s in load().items():
        if sid not in ORDER:
            out.append((sid, f"indicator series {sid!r} not in ORDER (tools/bib/indicators.py)"))
        if sid not in DEFS:
            out.append((sid, f"indicator series {sid!r} has no definition in DEFS (tools/bib/indicators.py)"))
        for r in s.get("rows", []):
            try:
                period_end(r["p"])
            except Exception:
                out.append((sid, f"bad period {r.get('p')!r}"))
            if "first" in r and not r.get("released" if s.get("kind") != "poll" else "published"):
                out.append((sid, f"{r['p']}: first-reported figure without a release date"))
            if "first" in r and s.get("manual") and not r.get("source"):
                out.append((sid, f"{r['p']}: transcribed figure without a source"))
    return out
