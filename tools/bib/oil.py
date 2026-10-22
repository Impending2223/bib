"""The Oil group of the calendar's monthly indicator tables: how its cells read, its table, its checks.

    indicators/oil-*.yaml, written by tools/indicators/make_oil.py (its docstring has the sources). indicators.py files
    the rows; this module renders the oil cells (first_cell, now_cell) and lays out the Oil table (table). The
    definitions are the master's (indicators/concepts.yaml; tools/bib/concepts.py).

STYLE (settled; keep it):
 1. Volumes in millions of barrels a day, two decimals: "7.23m b/d". The Survey of Current Business printed barrels in
    the month (thousands to Sept. 1961, millions after); the first column divides by the month's days, the source
    figure on hover. EIA's figures today are in thousand barrels a day. Reserves in billions of barrels, two decimals:
    "31.61bn bbl".
 2. Changes (the owner's question, Oct. 21, 2026), on the indicators' basis (indicators STYLE 5), each column in its
    own figures. Production and products supplied: percent from the month before, day for day (a day's rate to a day's
    rate, so a short February is no fall), not annualized, and from the same month a year earlier, "y/y" in grey: the
    figures are not seasonally adjusted, as the CPI's are not. The first column's are from the earlier months as first
    printed, each in its own issue: the Survey's revision of the month before, in the later issue, is not read. Trade:
    the change in net imports, million barrels a day, a last "Change" line (indicators STYLE 10). Reserves: the change
    from the year before, billion barrels. No change to or from a row whose first figure carries a note (a misprint,
    or a change of what the row counts); today's figures carry no such note and keep theirs.
 3. Trade stacked, one line each, label left, figure right (as the budgets): Imports, Exports, Net (imports less
    exports); the first column sums crude and refined products as the Survey printed them, "<.05" (its note, under
    50,000 barrels) and "—" (none printed) counted as nothing. Monthly figures then; EIA's monthly trade begins in 1973,
    so the year's row (filed in December) carries today's figures.
 4. A corrected misprint or a change of what a row counts shows in grey after the figure, as printed (NOTE in the
    script): Survey figures stand as first printed.
 5. The Oil table (the owner's ruling, Oct. 21, 2026: no vacant columns): a table of its own under the month's
    indicators, before Money and credit, set off by the same double rule, caption "Oil". The rows with both figures in
    Indicator | As first reported | Released | Revised, today; under it, the rows with one figure (trade by month and
    products supplied before 1963, first reported only; trade by year, today only) in Indicator | Figure | Reported,
    "As first reported, <issue>" or "Revised, today", the source on hover. Today's crude production equals the
    Survey's, to the Survey's rounding, in most months: the data, not a bug (make_oil.py reads the two apart, the
    Survey by eye, EIA's workbook by download); the months they differ are in the statement.
 6. The world's oil and the posted prices are not rows here (a year's table by country; dated postings, not a monthly
    row): tools/bib/oilworld.py renders them under the December entries of the Oil thread (oilworld:<YYYY>) and under
    Esso Export's cut of Aug. 9, 1960 (oilprice:ras-tanura), from sources/oil-world.yaml; its STYLE notes.
"""
import calendar

from . import concepts

SERIES = ("oil-production", "oil-supplied", "oil-trade", "oil-trade-year", "oil-reserves")
MINUS = "−"
DEFS = {k: v for k, v in concepts.master_texts().items() if k in SERIES}
_IDX = {}


def _days(p):
    y, m = int(str(p)[:4]), int(str(p)[5:7])
    return calendar.monthrange(y, m)[1]


def _bbl(v, unit):
    """A Survey figure in barrels."""
    if not isinstance(v, (int, float)):
        return 0
    return v * (1e3 if unit and unit.startswith("thousands") else 1e6)


def _mbd(x):
    return f"{x:.2f}m b/d"


def _grey(t):
    from .indicators import grey
    return grey(t)


def _signed(v, nd=1):
    from .indicators import signed
    return signed(round(v, nd) + 0.0, nd)


def _kv(lines):
    from .indicators import esc
    return '<span class="kv">' + "".join(
        f'<span class="k">{esc(a)}</span><span class="v">{esc(b)}</span>' for a, b in lines) + "</span>"


# ---------------------------------------------------------------- changes (STYLE 2)

def _index(s):
    k = id(s)
    if k not in _IDX:
        _IDX[k] = {str(r["p"]): r for r in s.get("rows", [])}
    return _IDX[k]


def _back(p, months):
    p = str(p)
    if len(p) == 4:
        return str(int(p) - months // 12)
    y, m = int(p[:4]), int(p[5:7]) - months
    while m < 1:
        y, m = y - 1, m + 12
    return f"{y}-{m:02d}"


def _level(sid, r, col):
    """The row's level in the column: m b/d (production, supplied), net imports m b/d (trade), bn bbl (reserves)."""
    if r is None:
        return None
    v = r.get(col)
    if v is None:
        return None
    if col == "first" and r.get("note"):
        return None                      # a misprint or a change of what the row counts: no change to or from it
    if sid in ("oil-production", "oil-supplied"):
        if col == "first":
            return _bbl(v, r.get("unit")) / _days(r["p"]) / 1e6 if isinstance(v, (int, float)) else None
        return v / 1000
    if sid == "oil-trade" and col == "first":
        d, u = _days(r["p"]), r.get("unit")
        return ((_bbl(v.get("crude_imports"), u) + _bbl(v.get("product_imports"), u))
                - (_bbl(v.get("crude_exports"), u) + _bbl(v.get("product_exports"), u))) / d / 1e6
    if sid == "oil-trade-year" and col == "now":
        return v["net"] / 1000
    if sid == "oil-reserves":
        return v / 1000
    return None


def change(sid, s, r, col, months=None):
    """The change from the period before (months=None: the month before, or the year before for a year's row), or
    from `months` earlier; None where either figure is wanting."""
    back = months or (12 if len(str(r["p"])) == 4 else 1)
    a, b = _level(sid, r, col), _level(sid, _index(s).get(_back(r["p"], back)), col)
    if a is None or b is None:
        return None
    if sid in ("oil-production", "oil-supplied"):
        return (a / b - 1) * 100 if b else None
    return a - b


def _pct(sid, s, r, col):
    """", +1.2% (+2.0% y/y)" for production and supplied."""
    c, y = change(sid, s, r, col), change(sid, s, r, col, 12)
    out = f", {_signed(c)}%" if c is not None else ""
    if y is not None:
        out += (f" ({_signed(y)}% {_grey('y/y')})" if c is not None else f", {_signed(y)}% {_grey('y/y')}")
    return out


# ---------------------------------------------------------------- cells

def first_cell(sid, s, r):
    v, unit, p = r.get("first"), r.get("unit"), r["p"]
    if v is None:
        return "—"
    note = (" " + _grey(f"({r['note']})")) if r.get("note") else ""
    if sid in ("oil-production", "oil-supplied"):
        return _mbd(_bbl(v, unit) / _days(p) / 1e6) + _pct(sid, s, r, "first") + note
    if sid == "oil-trade":
        d = _days(p)
        imp = (_bbl(v.get("crude_imports"), unit) + _bbl(v.get("product_imports"), unit)) / d / 1e6
        exp = (_bbl(v.get("crude_exports"), unit) + _bbl(v.get("product_exports"), unit)) / d / 1e6
        lines = [("Imports", _mbd(imp)), ("Exports", _mbd(exp)), ("Net", _mbd(imp - exp))]
        c = change(sid, s, r, "first")
        if c is not None:
            lines.append(("Change", _signed(c, 2) + "m b/d"))
        return _kv(lines) + (f"<br>{_grey(r['note'])}" if r.get("note") else "")
    if sid == "oil-reserves":
        c = change(sid, s, r, "first")
        return f"{v / 1000:.2f}bn bbl" + (f", {_signed(c, 2)}bn" if c is not None else "") + note
    return "—"


def now_cell(sid, s, r):
    v = r.get("now")
    if v is None:
        return "—"
    if sid in ("oil-production", "oil-supplied"):
        return _mbd(v / 1000) + _pct(sid, s, r, "now")
    if sid == "oil-trade-year":
        lines = [("Imports", _mbd(v["imports"] / 1000)), ("Exports", _mbd(v["exports"] / 1000)),
                 ("Net", _mbd(v["net"] / 1000))]
        c = change(sid, s, r, "now")
        if c is not None:
            lines.append(("Change", _signed(c, 2) + "m b/d"))
        return _kv(lines)
    if sid == "oil-reserves":
        c = change(sid, s, r, "now")
        return f"{v / 1000:.2f}bn bbl" + (f", {_signed(c, 2)}bn" if c is not None else "")
    return "—"


# ---------------------------------------------------------------- the Oil table (STYLE 5)

def table(rows, year, name, cells):
    """rows: [(sid, s, r)]; name(sid, s, r): the name cell; cells(sid, s, r, year): (first, released, today)."""
    from .indicators import esc, date_label
    both, one = [], []
    for sid, s, r in rows:
        has_first, has_now = r.get("first") is not None, r.get("now") is not None
        first, rel, now = cells(sid, s, r, year)
        if has_first and has_now:
            both.append(f'<tr><td class="iname">{name(sid, s, r)}</td><td>{first}</td><td class="rel">{rel}</td>'
                        f'<td>{now}</td></tr>')
        elif has_first:
            src = r.get("source") or ""
            when = f"As first reported, {date_label(r['released'], year)}" if r.get("released") else "As first reported"
            one.append(f'<tr><td class="iname">{name(sid, s, r)}</td><td>{first}</td>'
                       f'<td class="rel"><span title="{esc(src)}">{esc(when)}</span></td></tr>')
        elif has_now:
            src = (s.get("now") or {}).get("source") or ""
            one.append(f'<tr><td class="iname">{name(sid, s, r)}</td><td>{now}</td>'
                       f'<td class="rel"><span title="{esc(src)}">Revised, today</span></td></tr>')
    if not both and not one:
        return ""
    out = '<div class="ind ind-sep ind-oil"><p class="ind-cap">Oil</p>'
    if both:
        out += ('<table><thead><tr><th>Indicator</th><th>As first reported</th><th>Released</th><th>Revised, today</th>'
                '</tr></thead><tbody>' + "".join(both) + "</tbody></table>")
    if one:
        out += ('<table class="ind-one"><thead><tr><th>Indicator</th><th>Figure</th><th>Reported</th></tr></thead><tbody>'
                + "".join(one) + "</tbody></table>")
    return out + "</div>"


def problems(data):
    """For ./bib check: each oil row's first figure has its unit, issue and source; trade rows all four parts."""
    out = []
    for sid in SERIES:
        s = data.get(sid)
        if not s:
            continue
        for r in s.get("rows", []):
            if "first" not in r:
                continue
            if not r.get("unit") or not r.get("source"):
                out.append((sid, f"{r['p']}: first figure without its unit or source"))
            if sid == "oil-trade":
                f = r["first"]
                if not isinstance(f, dict) or set(f) != {"crude_imports", "product_imports", "crude_exports",
                                                         "product_exports"}:
                    out.append((sid, f"{r['p']}: trade figure lacks one of its four parts"))
                elif any(not isinstance(x, (int, float)) and x not in ("<.05", "—") for x in f.values()):
                    out.append((sid, f"{r['p']}: trade part neither a figure nor '<.05' or '—'"))
            if sid in ("oil-production", "oil-supplied") and r.get("now") is not None \
                    and isinstance(r["first"], (int, float)) and not r.get("note"):
                bd = _bbl(r["first"], r["unit"]) / _days(r["p"]) / 1000
                if abs(bd / r["now"] - 1) > 0.05:
                    out.append((sid, f"{r['p']}: first figure {bd:.0f} thousand b/d is more than 5% from today's "
                                     f"{r['now']:.0f}; a misreading? (note it if the source printed it so)"))
    return out
