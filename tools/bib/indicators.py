"""Economic indicators in the calendar, filed by the period they report on.

    indicators/<id>.yaml   one series: its definitions then and now, and one row per reporting
                           period (p: 1961-03, 1961Q2, FY1962, 1961) with the figure as first
                           reported, its release date and source, and the figure as revised today.
                           Made by tools/indicators/make_indicators.py; see that script.

Filing. Each calendar month section whose dates hold the last day of a period carries that
period's figures in a table under its heading: months in their month, quarters in the quarter's
last month, fiscal years (ending June 30) in June, calendar years in December. Periods that end
before the first dated section go to it. Concepts and sources (the owner's rule, Oct. 21, 2026): one master text,
indicators/concepts.yaml, tagged by series and by the periods each piece concerns (tools/bib/concepts.py); each
calendar page writes, after the month table where a series first appears on it, a servant: that page's series, only
what concerns the periods it files; each row's name links to its servant on the page, else to the master,
build/indicators.html, which also holds every series' full table.

STYLE (settled; keep it, and fix anything that drifts from it):
 1. Columns: Indicator | As first reported | Released | Revised, today. Gallup's approval (kind: poll) in a table
    of its own under it (and under Money and credit, 13), set off by a double gray rule, centered, three-quarters of the table's width (the last row above a rule has none)
    and its own caption ("Presidential approval, Gallup"; the first table's
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
    figures; the gold stock alone has two decimals (its monthly changes run to tens of millions). A ratio there
    carries its own "%" and its denominator in grey, "54.7% of GNP" ("of GDP" today), its change in points; net
    interest to GNP has two decimals (its quarterly changes run to hundredths). A level with a change (the gold
    stock, the public debt) and a stacked balance with a change take a last "Change" line.
    Stacked figures sit in a fixed two-column grid (label 7.5em, figure 4.2em) so they align
    down the column.
11. Source qualifiers stay: "about $28bn", "some $30–40bn"; a note the source attaches to one
    figure (NOTE in the script) shows after it in grey: "(Q1–Q3, annual rate)".
12. Definitions (DEFS, from the master, indicators/concepts.yaml): what the figure was then, what it is today, and
    pointers, in the brief's register: compact, plain, no judgment of the figures. Written once, in the master, each
    piece tagged with the periods it concerns; the calendar's servants and the Indicators page are made from it
    (tools/bib/concepts.py, its STYLE). Never write a definition into a module or a page.
13. Money and credit: a table of its own, between the indicators and the approval table, set off by the same
    rule, with its own caption and two columns, Rate | Percent: rates are not revised, so each has one figure.
    Interest rates in percent to two decimals, as the Bulletin and H.15 print them, "3.85%"; changes in
    points, "+0.33 pt". Market rates as FRED gives them (the source on hover). The discount rate is set, not
    measured: the rate in effect at the month's end; in a month it changed, the change and, in grey, the
    Board's announcement and the day it took effect, "4.00%, +0.50 pt (announced Nov. 23; effective Nov. 24)";
    in other months the day it took effect on hover. An administered rate (discount, prime) shows a change
    only in a month it changed.
14. A release known only by its issue (the Treasury Bulletin, monthly) has its month for a date ("released:
    1962-02"), shown "Feb. 1962".
15. Oil (oil-*): a table of its own under the indicators, before Money and credit, without vacant columns; its cells
    in millions of barrels a day, with changes; STYLE in tools/bib/oil.py.
16. The war (war-*, kind: war): not in the month's tables. A table of its own under the first Thursday of the next
    month, in the day layout (the owner's request, Oct. 22, 2026; tools/bib/wartable.py, its STYLE); its cells in
    tools/bib/war.py.
17. Money, the foreign accounts and the debt's terms (tools/bib/finance.py, its STYLE; written by
    tools/indicators/make_finance.py): the money stock and free reserves in a group "Money and credit" of the indicators
    table, the yields and mortgage rates in the Money and credit table (13); reserve assets and the trade balances under
    International; the debt's holders and length under "Federal debt" (the public debt and its ratios with them), $bn in
    its header as Federal finance; exchange rates and the gold price, when read, in a table of their own (one figure).
"""
import calendar
import datetime
import functools
import os
import re

from . import store
from .markup import to_html
from . import oil
from . import war
from . import finance
from . import concepts

DIR = os.path.join(store.ROOT, "indicators")
ORDER = ["cpi", "wpi", "deflator", "unemployment", "payrolls", "industrial-production", "gnp", "real-gnp",
         "gap-cea", "gap-cbo", "administrative-budget", "cash-budget", "unified-budget", "federal-national-accounts",
         "federal-primary-balance", "interest-gnp", "public-debt", "debt-gnp", "debt-gdp-omb",
         "balance-of-payments", "balance-of-payments-regular", "balance-of-payments-liquidity",
         "balance-of-payments-official", "gold-stock", "oil-production", "oil-supplied", "oil-trade", "oil-trade-year",
         "oil-reserves", "war-deaths", "war-strength",
         "war-enemy-ob", "war-enemy-ob-old", "war-enemy-snie", "war-enemy-strength-q", "war-infiltration", "war-enemy-kia", "war-rvnaf-kia", "war-rvnaf-strength", "war-fwmaf-strength", "war-air-attack", "war-air-nvn-rp", "discount-rate", "federal-funds",
         "prime-rate", "treasury-bill", "treasury-10-year", "approval"]
GROUP = {"cpi": "Prices", "wpi": "Prices", "deflator": "Prices",
         "unemployment": "Employment", "payrolls": "Employment",
         "industrial-production": "Output", "gnp": "Output", "real-gnp": "Output",
         "gap-cea": "Output", "gap-cbo": "Output",
         "discount-rate": "Money and credit", "federal-funds": "Money and credit", "prime-rate": "Money and credit",
         "treasury-bill": "Money and credit", "treasury-10-year": "Money and credit",
         "administrative-budget": "Federal finance", "cash-budget": "Federal finance", "unified-budget": "Federal finance",
         "federal-national-accounts": "Federal finance", "federal-primary-balance": "Federal finance",
         "interest-gnp": "Federal finance", "public-debt": "Federal finance", "debt-gnp": "Federal finance",
         "debt-gdp-omb": "Federal finance",
         "balance-of-payments": "International", "balance-of-payments-regular": "International",
         "balance-of-payments-liquidity": "International", "balance-of-payments-official": "International",
         "gold-stock": "International",
         "oil-production": "Oil", "oil-supplied": "Oil", "oil-trade": "Oil", "oil-trade-year": "Oil",
         "oil-reserves": "Oil",
         "war-deaths": "The war", "war-strength": "The war",
         **{x: "The war" for x in ("war-enemy-ob", "war-enemy-ob-old", "war-enemy-snie", "war-enemy-strength-q", "war-infiltration", "war-enemy-kia", "war-rvnaf-kia", "war-rvnaf-strength", "war-fwmaf-strength", "war-air-attack", "war-air-nvn-rp")},
         "approval": "Opinion"}
def _place(after, ids):
    """Put ids into ORDER after `after` (the series tools/bib/finance.py renders, kept out of the lists above)."""
    i = ORDER.index(after) + 1
    ORDER[i:i] = [x for x in ids if x not in ORDER]


# Money, the foreign accounts, the debt's terms, unit labor costs (tools/bib/finance.py; tools/indicators/make_finance.py)
_place("payrolls", finance.COSTS)
_place("debt-gdp-omb", finance.DEBT)
_place("gold-stock", finance.INTL + finance.FX + finance.MONEY)
_place("treasury-10-year", finance.RATES)
GROUP.update({x: "Employment" for x in finance.COSTS})
GROUP.update({x: "Federal debt" for x in ("interest-gnp", "public-debt", "debt-gnp", "debt-gdp-omb") + finance.DEBT})
GROUP.update({x: "International" for x in finance.INTL + finance.FX})
GROUP.update({x: "Money and credit" for x in finance.MONEY + finance.RATES})
FIELD_LABEL = {"receipts": "Receipts", "expenditures": "Expenditures", "payments": "Payments", "outlays": "Outlays",
               "balance": "Balance", "interest": "Net interest", "primary": "Primary"}
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]

RATES = {"discount-rate", "federal-funds", "prime-rate", "treasury-bill", "treasury-10-year"}
# Definitions: each series' concepts and sources, one text, the master's (indicators/concepts.yaml, read by
# tools/bib/concepts.py): the Indicators page prints it whole; each calendar page writes servants of it (STYLE 12).
DEFS = concepts.master_texts()


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def load():
    if not os.path.isdir(DIR):
        return {}
    out = {}
    for f in sorted(os.listdir(DIR)):
        if f.endswith(".yaml") and f != "concepts.yaml":      # concepts.yaml: the master text (tools/bib/concepts.py)
            d = store.load_yaml(os.path.join(DIR, f))
            out[d["id"]] = d
    return out


# ---------------------------------------------------------------- periods and dates

@functools.lru_cache(maxsize=None)
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
    if re.match(r"^\d{4}$", str(iso)):                # a volume known by its year (the Minerals Yearbook)
        return str(iso)
    if re.match(r"^\d{4}-\d{2}$", str(iso)):          # an issue month (STYLE 14)
        return f"{MON[int(str(iso)[5:7]) - 1]} {str(iso)[:4]}"
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
    if sid == "public-debt":
        lines = [("Debt", num(to_bn(v, unit)))]
        if c is not None:
            lines.append(("Change", signed(c / 1000)))
        return '<span class="kv">' + "".join(
            f'<span class="k">{esc(a)}</span><span class="v">{esc(b)}</span>' for a, b in lines) + "</span>"
    if sid in ("debt-gnp", "interest-gnp"):
        nd = 2 if sid == "interest-gnp" else 1
        out = f"{num(v, nd)}% " + grey("of GDP" if unit and "GDP" in unit else "of GNP")
        return out + (f", {signed(c, nd)} pt" if c is not None else "")
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
    if sid in RATES:
        return f"{num(v, 2)}%" + (f", {signed(c, 2)} pt" if c is not None else "")
    b = base_of(unit)
    out = f"{qual}{num(v)}" + (" " + grey(f"({b})") if b else "") + chg_text(kind, c)
    if yoy is not None and c is None:
        return out + f", {signed(yoy)}%\u00a0{grey('y/y')}"
    return out + yoy_text(yoy)


def stacked(fields, v, unit, ests, year, field_names, chg=None):
    """Receipts / expenditures / balance, one line each, figures right-aligned, $bn; a change from the prior period
    in the series' last field, where one is kept (the primary balance), as a last line."""
    lines = []
    for k in fields:
        x = v.get(k) if v else None
        lines.append((FIELD_LABEL.get(k, k.capitalize()), num(to_bn(x, unit))))
    if chg is not None:
        lines.append(("Change", signed(to_bn(chg, unit))))
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

def rows_for(data, lo, hi, prev_to=None, next_from=None):
    """The rows a section files: periods ending within it, and those ending in the gap since the last dated section
    (all before it, in the first). A month the section
    ends within (Jan. 1965, the calendar ending Jan. 20) is filed there too, where no later section begins in it.
    Not across a gap of years: the primary seasons after the calendar's last month (Mar. 1972) take no figures that
    end after it (the estimates for fiscal 1969 and 1970 stay in the data, unshown)."""
    out = []
    far = prev_to is not None and (lo - prev_to).days > 92
    for sid in ORDER + [k for k in data if k not in ORDER]:
        s = data.get(sid)
        if not s or s.get("kind") == "war":    # The war: a table of its own, on the first Thursday (wartable.py)
            continue
        for r in s.get("rows", []):
            end = period_end(r["p"])
            part = (re.match(r"^\d{4}-\d{2}", str(r["p"])) and end.replace(day=1) <= hi < end
                    and (next_from is None or end < next_from))
            if lo <= end <= hi or (end < lo and not far and (prev_to is None or end > prev_to)) or part:
                out.append((sid, s, r))
    return out


def cell_first(sid, s, r, year):
    if sid in finance.SERIES:             # money, the foreign accounts, the debt's terms (tools/bib/finance.py)
        return finance.cell(sid, s, r, "first")
    if sid in oil.SERIES:                 # the Oil group (tools/bib/oil.py, its STYLE)
        return oil.first_cell(sid, s, r)
    if s.get("kind") == "war":            # The war (tools/bib/war.py, its STYLE)
        return war.cell(sid, s, r, "first")
    if "first" not in r and not r.get("est"):
        return "—"
    unit, kind = r.get("unit"), s.get("change")
    if s.get("fields"):
        out = stacked(s["fields"], r.get("first"), unit, r.get("est"), year, s["fields"], r.get("chg"))
        return out + (f'<br>{grey(r["note"])}' if r.get("note") else "")
    out = single(sid, r["first"], unit, kind, r.get("chg"), r.get("q"), r.get("yoy"))
    return out + (" " + grey(f"({r['note']})") if r.get("note") else "")


def cell_now(sid, s, r):
    if sid in finance.SERIES:
        return finance.cell(sid, s, r, "now")
    if sid in oil.SERIES:
        return oil.now_cell(sid, s, r)
    if s.get("kind") == "war":
        return war.cell(sid, s, r, "now")
    v = r.get("now")
    if v is None or (isinstance(v, dict) and not any(x is not None for x in v.values())):
        return "—"
    unit, kind = (s.get("now") or {}).get("unit"), s.get("change")
    if sid == "debt-gdp-omb":                # two ratios, each with its change in points
        def part(x, cx, what):
            return f"{num(x)}% {grey(what)}" + (f", {signed(cx)} pt" if cx is not None else "")
        return (part(v.get("public"), r.get("chg_now"), "held by the public") + "<br>"
                + part(v.get("gross"), r.get("chg_now_gross"), "gross"))
    if s.get("fields"):
        return stacked(s["fields"], v, unit, None, None, s["fields"], r.get("chg_now"))
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


def def_href(sid):
    """A row name's link where no servant plan is given: the master (tools/bib/concepts.py)."""
    return f"{concepts.MASTER}#{sid}"


def name_cell(sid, s, r, href=None, text=None):
    """A row's name, linked to its concepts and sources (its servant on the page, else the master), and its period."""
    return (f'<a href="{esc((href or def_href)(sid))}">{esc(text or s["name"])}</a> '
            f'<span class="per">{esc(period_label(r["p"]))}</span>')


def rate_row(sid, s, r, year, href=None, label=None):
    """A rate (STYLE 13): its name and month, then the one figure: the discount rate as the Board set it (its change,
    the day announced and the day it took effect, in a month it changed), a market rate as FRED gives it today.
    label: the first cell's text in place of the name (the Indicators page's tables, by month)."""
    name = f'<span class="per">{esc(label)}</span>' if label else name_cell(sid, s, r, href)
    if "first" in r:
        rr = dict(r)
        if r.get("released") and sid not in finance.SERIES:   # "(announced Nov. 23; effective Nov. 24)"
            ann = f"announced {date_label(r['released'], year)}"
            rr["note"] = f"{ann}; {r['note']}" if r.get("note") else ann
        val = cell_first(sid, s, rr, year)
        tip = exact(r["first"], r.get("unit"))
        if r.get("since"):
            tip += f"; in effect from {date_label(r['since'])}"
        tip += f"; {r.get('source', '')}" if r.get("source") else ""
    else:
        val = cell_now(sid, s, r)
        now = s.get("now") or {}
        tip = now.get("source", "") + (": " + exact(r["now"], now.get("unit")) if r.get("now") is not None else "")
    return f'<tr><td class="iname">{name}</td><td><span title="{esc(tip)}">{val}</span></td></tr>'


def cells(sid, s, r, year):
    """A row's three value cells, as first reported (the source figure on hover), released (its source on hover),
    and today (today's source on hover)."""
    then, now = s.get("then") or {}, s.get("now") or {}
    first = cell_first(sid, s, r, year)
    if "first" in r:
        tip = exact(r["first"], r.get("unit"))
        if r.get("since"):          # a standing rate (STYLE 13): when it took effect, and where it is printed
            tip += f'; in effect from {date_label(r["since"])}; {r.get("source", "")}'
        first = f'<span title="{esc(tip)}">{first}</span>'
    rel = "—"
    if r.get("released"):
        src = r.get("source") or (then.get("source") and f'{then["source"]}, released {r["released"]}')
        rel = f'<span title="{esc(src or "")}">{esc(date_label(r["released"], year))}</span>'
    nowv = cell_now(sid, s, r)
    if nowv != "—" and now.get("source"):
        nowv = f'<span title="{esc(now["source"] + (": " + exact(r["now"], now.get("unit")) if r.get("now") is not None else ""))}">{nowv}</span>'
    return first, rel, nowv


def block(data, sec_from, sec_to, prev_to, year, next_from=None, href=None):
    """The month's tables. href(sid): where a row's name links (its servant on the page; tools/bib/concepts.py)."""
    lo, hi = datetime.date.fromisoformat(sec_from), datetime.date.fromisoformat(sec_to)
    rows = rows_for(data, lo, hi, prev_to and datetime.date.fromisoformat(prev_to),
                    next_from and datetime.date.fromisoformat(next_from))
    if not rows:
        return ""
    href = href or def_href
    trs, shown, polls, rates, oils, fxs = [], set(), [], [], [], []
    for sid, s, r in rows:
        if sid in oil.SERIES:            # Oil apart, in a table of its own (STYLE 15; tools/bib/oil.py)
            oils.append((sid, s, r))
            continue
        if sid in finance.FX:            # exchange rates and gold apart, one figure (STYLE 17; tools/bib/finance.py)
            fxs.append((sid, s, r))
            continue
        g = GROUP.get(sid)
        if s.get("kind") in ("poll", "rate"):
            g = None
        if g and g not in shown:
            shown.add(g)
            unit_note = " $bn" if g in ("Federal finance", "Federal debt", "International") else ""
            trs.append(f'<tr class="g"><th colspan="4">{esc(g)}{grey(unit_note)}</th></tr>')
        if s.get("kind") == "poll":
            pname, per, first, rel, now = poll_row(sid, s, r, year)
            polls.append(f'<tr><td class="iname"><a href="{esc(href(sid))}">{esc(pname)}</a> '
                         f'<span class="per">{esc(per)}</span></td><td>{first}</td><td class="rel">{rel}</td><td>{now}</td></tr>')
            continue
        if s.get("kind") == "rate":
            rates.append(rate_row(sid, s, r, year, href))
            continue
        name = name_cell(sid, s, r, href)
        first, rel, nowv = cells(sid, s, r, year)
        trs.append(f'<tr><td class="iname">{name}</td><td>{first}</td><td class="rel">{rel}</td><td>{nowv}</td></tr>')
    out = ""
    if trs:
        out += ('<div class="ind"><p class="ind-cap">Economic indicators</p><table><thead><tr><th>Indicator</th><th>As first reported</th>'
                '<th>Released</th><th>Revised, today</th></tr></thead><tbody>'
                + "".join(trs) + "</tbody></table></div>")
    if oils:                             # Oil apart: no vacant columns (STYLE 15; tools/bib/oil.py)
        out += oil.table(oils, year, lambda sid, s, r: name_cell(sid, s, r, href), cells)
    if fxs:                              # exchange rates and gold: not revised, one figure (STYLE 17)
        out += finance.fx_table(fxs, year, lambda sid, s, r: name_cell(sid, s, r, href), cells)
    if rates:                            # rates apart: not revised, so one figure (STYLE 13)
        out += ('<div class="ind ind-sep ind-rt"><p class="ind-cap">Money and credit</p><table><thead><tr><th>Rate</th>'
                '<th>Percent</th></tr></thead><tbody>' + "".join(rates) + "</tbody></table></div>")
    if polls:                            # opinion apart: a reading has its field dates and no revision
        out += ('<div class="ind ind-sep ind-op"><p class="ind-cap">Presidential approval, Gallup</p><table><thead><tr><th>Reading</th><th>As published</th>'
                '<th>Released</th><th>Today</th></tr></thead><tbody>' + "".join(polls) + "</tbody></table></div>")
    return out


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
div.ind:has(+ div.ind) tbody tr:last-child td{border-bottom:0}
div.ind.ind-sep{margin-top:1.1rem}
div.ind.ind-sep::before{content:"";display:block;width:75%;margin:0 auto .7rem;border-top:3px double var(--muted)}
div.ind.ind-rt td.iname{width:42%}
div.ind.ind-op td.rel,div.ind.ind-op .per{white-space:nowrap}
div.ind-defs{font-family:var(--sans);font-size:.85rem;line-height:1.45;margin:1rem 0 1.5rem}
div.ind-defs dt{font-weight:600;margin-top:.6rem}
div.ind-defs dd{margin:.1rem 0 0 0;color:var(--ink)}
</style>"""


def inject(page, series, mode):
    """Put each calendar month's indicators under its heading and, where a series first appears on the page, its
    servant statement of concepts and sources after the table (tools/bib/concepts.py); rows link to their servants."""
    data = load()
    if not data:
        return page
    from . import calsplit
    plan = concepts.plan(series, data)
    here = calsplit.CUR.get("half") if mode == "list" else None
    done = False
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        dated = [s for s in lst.sections if s.extra.get("from") and s.extra.get("to")]
        for i, sec in enumerate(dated):
            if here and plan.part_of(sec) not in (None, here):
                continue                           # another part's page
            year = int(str(sec.extra["to"])[:4])
            hid = f"{lst.key}--{sec.id}" if mode == "series" else sec.id
            nxt = str(dated[i + 1].extra["from"]) if i + 1 < len(dated) else None
            prv = str(dated[i - 1].extra["to"]) if i else None
            blk = block(data, str(sec.extra["from"]), str(sec.extra["to"]), prv, year, nxt, plan.href(sec))
            if not blk:
                continue
            blk += plan.servant(sec)
            pat = re.compile(r'(<h\d id="' + re.escape(hid) + r'"[^>]*>.*?</h\d>(?:\s*<p class="logic">.*?</p>)*)', re.S)
            page, n = pat.subn(lambda m: m.group(1) + "\n" + blk, page, count=1)
            done = done or bool(n)
    if done:
        page = page.replace("</head>", STYLE + "\n" + concepts.STYLE + "\n</head>", 1)
        page = concepts.link_logic(page)
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
            if "first" in r and not r.get("released" if s.get("kind") != "poll" else "published") and not r.get("since"):
                out.append((sid, f"{r['p']}: first-reported figure without a release date"))
            if "first" in r and s.get("manual") and not r.get("source"):
                out.append((sid, f"{r['p']}: transcribed figure without a source"))
    return out
