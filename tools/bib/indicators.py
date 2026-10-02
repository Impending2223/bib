"""Economic indicators in the calendar, filed by the period they report on.

    indicators/<id>.yaml   one series: its definitions then and now, and one row per reporting
                           period (p: 1961-03, 1961Q2, FY1962, 1961) with the figure as first
                           reported, its release date and source, and the figure as revised today.
                           Made by tools/indicators/make_indicators.py; see that script.

Each calendar month section whose dates hold the last day of a period carries that period's
figures in a table under its heading: months in their month, quarters in the quarter's last
month, fiscal years (ending June 30) in June, calendar years in December. Periods that end
before the first dated section go to it (the Prologue).
"""
import calendar
import datetime
import os
import re

from . import store

DIR = os.path.join(store.ROOT, "indicators")
ORDER = ["cpi", "wpi", "deflator", "unemployment", "payrolls", "industrial-production", "gnp", "real-gnp",
         "administrative-budget", "cash-budget", "federal-national-accounts", "balance-of-payments", "gold-stock"]
GROUP = {"cpi": "Prices", "wpi": "Prices", "deflator": "Prices",
         "unemployment": "Employment", "payrolls": "Employment",
         "industrial-production": "Output", "gnp": "Output", "real-gnp": "Output",
         "administrative-budget": "Federal finance", "cash-budget": "Federal finance",
         "federal-national-accounts": "Federal finance",
         "balance-of-payments": "International", "gold-stock": "International"}
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
MONTH = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December"]


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
        return f"fiscal {p[2:]}"
    if "Q" in p:
        y, q = p.split("Q")
        return f"{['first', 'second', 'third', 'fourth'][int(q) - 1]} quarter {y}"
    if re.match(r"^\d{4}$", p):
        return f"year {p}"
    return f"{MONTH[int(p[5:7]) - 1]} {p[:4]}"


def date_label(iso, year=None):
    d = datetime.date.fromisoformat(str(iso))
    s = f"{MON[d.month - 1]} {d.day}"
    return s if year == d.year else f"{s}, {d.year}"


def fmt(v, nd=1):
    if v is None:
        return "n.a."
    if abs(v) >= 1000 or isinstance(v, int):
        s = f"{abs(v):,.0f}"
    else:
        s = f"{abs(v):.{nd}f}"
    return ("−" if v < 0 else "") + s


def signed(v, nd=1, pct=False):
    if v is None:
        return ""
    s = ("+" if v > 0 else "−" if v < 0 else "±") + (f"{abs(v):,.0f}" if abs(v) >= 1000 else f"{abs(v):.{nd}f}")
    return s + ("%" if pct else "")


def unit_note(u):
    return f' <span class="u">({esc(u)})</span>' if u else ""


def value_cell(sid, v, unit, chg, kind):
    """One figure, with its unit and change, in the series' house form."""
    if isinstance(v, dict):
        parts = []
        for k, x in v.items():
            name = {"balance": "surplus" if (x or 0) >= 0 else "deficit"}.get(k, k)
            parts.append(f"{name} {fmt(x)}")
        return "; ".join(parts) + unit_note(unit)
    if sid == "unemployment":
        out = f"{fmt(v)}%"
        if chg is not None:
            out += f", {signed(chg)} pt"
        return out
    elif sid in ("payrolls",):
        out = f"{v / 1000:.1f} million"
        if chg is not None:
            out += f", {signed(chg * 1000, 0)}"
        return out
    elif sid in ("gnp", "real-gnp"):
        out = f"${fmt(v)} billion"
    elif sid == "gold-stock":
        out = f"${fmt(v)} million"
    else:
        out = fmt(v)
    out += unit_note(unit)
    if chg is not None:
        out += ", " + signed(chg, 1 if kind == "pct" else 1, pct=(kind == "pct"))
    return out


def gnp_unit(u):
    return {"billions of dollars, seasonally adjusted annual rate": "annual rate"}.get(u, u)


def rows_for(data, lo, hi, first_section):
    """Rows of every series whose period ends in [lo, hi] (or before lo, for the first section)."""
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


def block(data, sec_from, sec_to, first_section, year):
    lo, hi = datetime.date.fromisoformat(sec_from), datetime.date.fromisoformat(sec_to)
    rows = rows_for(data, lo, hi, first_section)
    if not rows:
        return ""
    trs = []
    shown_groups = set()
    for sid, s, r in rows:
        g = GROUP.get(sid)
        if g and g not in shown_groups:
            shown_groups.add(g)
            trs.append(f'<tr class="g"><th colspan="4">{esc(g)}</th></tr>')
        then, now = s.get("then") or {}, s.get("now") or {}
        name = esc(s["name"])
        if then.get("url"):
            name = f'<a href="{esc(then["url"])}" title="{esc(then.get("label", ""))}">{name}</a>'
        per = esc(period_label(r["p"]))
        first = "—"
        if "first" in r:
            u = r.get("unit")
            u = gnp_unit(u) if sid == "gnp" else ("1954 dollars" if u == "billions of 1954 dollars, SAAR" else u)
            if isinstance(r["first"], dict) or sid in ("unemployment", "payrolls"):
                u = u if isinstance(r["first"], dict) else None
            first = value_cell(sid, r["first"], u, r.get("chg"), s.get("change"))
        rel = ""
        if r.get("released"):
            rel = esc(date_label(r["released"], year))
            src = r.get("source") or (then.get("source") and f'{then["source"]}, released {r["released"]}')
            if src:
                rel = f'<span title="{esc(src)}">{rel}</span>'
        for e in r.get("est", []):
            v = e["value"]
            bal = v.get("balance") if isinstance(v, dict) else v
            first += f'<br><span class="est">est. {esc(date_label(e["as_of"], year))}: {fmt(bal)}</span>'
        nu = now.get("unit")
        nu = {"billions of dollars, SAAR": None, "percent": None, "thousands": None,
              "millions of dollars": "$ millions" if isinstance(r.get("now"), dict) else None,
              "billions of chained 2017 dollars, SAAR": "2017 dollars"}.get(nu, nu)
        nowv = "—" if r.get("now") is None else value_cell(sid, r["now"], nu, None, None)
        if now.get("url") and r.get("now") is not None:
            nowv = f'<a href="{esc(now["url"])}" title="{esc(now.get("label", ""))}">{nowv}</a>'
        trs.append(f"<tr><td>{name} <span class=\"per\">{per}</span></td><td>{first}</td>"
                   f"<td class=\"rel\">{rel}</td><td>{nowv}</td></tr>")
    return ('<div class="ind"><table><thead><tr><th>Indicator</th><th>As first reported</th>'
            '<th>Released</th><th>Revised, today</th></tr></thead><tbody>'
            + "".join(trs) + "</tbody></table></div>")


STYLE = """<style>
div.ind{margin:.4rem 0 1.1rem;overflow-x:auto}
div.ind table{border-collapse:collapse;font-family:var(--sans);font-size:.8rem;line-height:1.35;color:var(--ink);min-width:100%}
div.ind th,div.ind td{text-align:left;vertical-align:top;padding:.18rem .5rem .18rem 0;border-bottom:1px solid var(--rule)}
div.ind thead th{color:var(--muted);font-weight:600}
div.ind tr.g th{padding-top:.5rem;color:var(--muted);font-weight:600;font-size:.75rem;text-transform:uppercase;letter-spacing:.04em;border-bottom:0}
div.ind .per,div.ind .u,div.ind .est,div.ind td.rel{color:var(--muted)}
div.ind a{color:inherit;text-decoration-color:var(--rule)}
</style>"""


def inject(page, series, mode):
    """Put each calendar month's indicators under its heading in a built page."""
    data = load()
    if not data:
        return page
    done = False
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        dated = [s for s in lst.sections if s.extra.get("from") and s.extra.get("to")]
        for i, sec in enumerate(dated):
            year = int(sec.extra["to"][:4])
            blk = block(data, str(sec.extra["from"]), str(sec.extra["to"]), i == 0, year)
            if not blk:
                continue
            hid = f"{lst.key}--{sec.id}" if mode == "series" else sec.id
            pat = re.compile(r'(<h\d id="' + re.escape(hid) + r'"[^>]*>.*?</h\d>(?:\s*<p class="logic">.*?</p>)*)', re.S)
            page, n = pat.subn(lambda m: m.group(1) + "\n" + blk, page, count=1)
            done = done or bool(n)
    if done:
        page = page.replace("</head>", STYLE + "\n</head>", 1)
    return page


def problems():
    """For ./bib check: malformed periods, rows without a source, unknown series."""
    out = []
    for sid, s in load().items():
        if sid not in ORDER:
            out.append((sid, f"indicator series {sid!r} not in ORDER (tools/bib/indicators.py)"))
        for r in s.get("rows", []):
            try:
                period_end(r["p"])
            except Exception:
                out.append((sid, f"bad period {r.get('p')!r}"))
            if "first" in r and not r.get("released"):
                out.append((sid, f"{r['p']}: first-reported figure without a release date"))
            if "first" in r and s.get("manual") and not r.get("source"):
                out.append((sid, f"{r['p']}: transcribed figure without a source"))
    return out
