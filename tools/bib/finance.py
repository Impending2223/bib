"""Money, the foreign accounts and the debt's terms in the calendar's monthly indicator tables: how their cells read,
the table of exchange rates and gold, and their checks.

    indicators/<id>.yaml for the ids in SERIES, written by tools/indicators/make_finance.py (its docstring has the
    sources, page by page). indicators.py files the rows; this module renders these series' cells (cell) and lays out
    the table of exchange rates and gold (fx_table). The definitions are the master's (indicators/concepts.yaml;
    tools/bib/concepts.py).

STYLE (settled; keep it, and the indicators' STYLE in tools/bib/indicators.py):
 1. Money and credit, in the indicators table (the money stock, free reserves): "$153.3bn, +0.4%" (the money stock, the
    change from the month before in percent, not annualized, as the CPI's); "$84m, −$78m" (free reserves: excess
    reserves less borrowings, in millions, the change in millions; net borrowed reserves are negative). Each column
    in its own figures: the first's change from the month before as printed in the same table (the December before
    from the same Report, for January).
 2. Yields and mortgage rates are rates (kind: rate): one figure each, in the Money and credit table (indicators STYLE
    13): "4.41%, +0.02 pt". Moody's as FRED gives them (not revised); the mortgage rates as first printed.
 3. International, in $bn, bare (indicators STYLE 10): reserve assets stacked, Gold, Currency, IMF, Total, Change,
    two decimals as the gold stock (their monthly changes run to tens of millions); today's, the IMF's reserves less
    gold (then the currencies and the IMF position together), "Excl. gold" and its change. Liquid liabilities to foreign official holders, Liabilities and Change, one decimal.
    The balances stacked: Trade (merchandise), With services (goods and services), Change (of the second), one decimal;
    quarterly, seasonally adjusted annual rates as the Reports print them (today's quarterly figures times four), the
    change from the quarter before in $bn.
 4. Exchange rates and the London gold price: not revised, so one figure each, in a table of their own under the
    indicators (and under Oil), before Money and credit, set off by the same double rule, caption "Exchange rates and
    gold": Rate | As first reported | Released. The noon buying rate in New York, monthly average, in cents a unit of
    the currency as the Bulletin printed it: "280.17¢ per pound", its change from the month before in cents; the gold
    price in dollars a fine ounce, "$35.08". A parity change or a market's opening shows in grey after the figure (its
    note).
 5. Federal debt ($bn in the group's header): the average interest rate, three decimals as the Treasury printed it,
    "3.285%", its change in points; the average length of the marketable debt in years and months, "4 yr 11 mo", its
    change in months; ownership stacked, Federal Reserve, Trust funds (the Government's investment accounts), Total,
    one decimal, $bn, no change (the private holders kept in the data for the check).
 6. Output per man-hour's companions (unit labor cost, compensation per man-hour), quarterly indexes: the indicators'
    default form, "112.3 (1957–59=100), +3.4% ar"; not handled here.
"""
from . import concepts

MONEY = ("money-m1", "money-m1-time", "money-m2", "free-reserves")
RATES = ("corporate-aaa", "corporate-baa", "mortgage-fha", "mortgage-conventional")
INTL = ("reserve-assets", "liquid-liabilities", "goods-services")
FX = ("fx-sterling", "fx-mark", "fx-franc", "gold-london")
DEBT = ("debt-interest-rate", "debt-maturity", "debt-ownership")
COSTS = ("unit-labor-cost", "compensation-hour")
SERIES = MONEY + RATES + INTL + FX + DEBT          # the cells this module renders
ALL = SERIES + COSTS                               # every series make_finance.py writes
DEFS = {k: v for k, v in concepts.master_texts().items() if k in ALL}
MINUS = "−"
FX_UNIT = {"fx-sterling": "per pound", "fx-mark": "per mark", "fx-franc": "per franc"}
OWN = (("fed", "Federal Reserve"), ("trust", "Trust funds"), ("total", "Total"))
RES = (("gold", "Gold"), ("currencies", "Currency"), ("imf", "IMF"), ("total", "Total"))
GS = (("merchandise", "Trade"), ("goods_services", "With services"))


def _grey(t):
    from .indicators import grey
    return grey(t)


def _signed(v, nd=1):
    from .indicators import signed
    return signed(round(v, nd) + 0.0, nd)


def _num(v, nd=1):
    from .indicators import num
    return num(v, nd)


def _kv(lines):
    from .indicators import esc
    return '<span class="kv">' + "".join(
        f'<span class="k">{esc(a)}</span><span class="v">{esc(b)}</span>' for a, b in lines) + "</span>"


def _bn(v, unit):
    return v / 1000 if unit and "millions" in unit else v


def _money(v, nd=0):
    """$84m, −$334m."""
    return (MINUS if v < 0 else "") + f"${abs(v):,.{nd}f}m"


def _nw(t):
    """Kept on one line (a minus sign is a break point)."""
    return f'<span style="white-space:nowrap">{t}</span>'


def _yrmo(months):
    y, m = divmod(int(round(months)), 12)
    return f"{y} yr {m} mo"


def cell(sid, s, r, col):
    """A value cell of one of SERIES: col 'first' (as first reported) or 'now' (today)."""
    v = r.get(col)
    if v is None or (isinstance(v, dict) and not any(x is not None for x in v.values())):
        return "—"
    c = r.get("chg" if col == "first" else "chg_now")
    unit = r.get("unit") if col == "first" else (s.get("now") or {}).get("unit")
    if col == "first" and not unit:
        unit = (s.get("then") or {}).get("unit")
    note = (" " + _grey(f"({r['note']})")) if col == "first" and r.get("note") else ""
    if sid in ("money-m1", "money-m1-time", "money-m2"):
        return f"${_num(_bn(v, unit))}bn" + (", " + _nw(f"{_signed(c)}%") if c is not None else "") + note
    if sid == "free-reserves":
        return (_nw(_money(v)) + (", " + _nw(f"{MINUS if c < 0 else '+'}${abs(c):,.0f}m") if c is not None else "")
                + note)
    if sid in RATES:
        return f"{_num(v, 2)}%" + (f", {_signed(c, 2)} pt" if c is not None else "") + note
    if sid == "reserve-assets" and col == "now":         # the IMF's reserves less gold: currencies and IMF then
        lines = [("Excl. gold", _num(_bn(v, unit), 2))]
        if c is not None:
            lines.append(("Change", _signed(_bn(c, unit), 2)))
        return _kv(lines)
    if sid == "reserve-assets":
        lines = [(lab, _num(_bn(v[k], unit), 2)) for k, lab in RES if v.get(k) is not None]
        if c is not None:
            lines.append(("Change", _signed(_bn(c, unit), 2)))
        return _kv(lines) + (f"<br>{_grey(r['note'])}" if col == "first" and r.get("note") else "")
    if sid == "liquid-liabilities":
        lines = [("Liabilities", _num(_bn(v, unit)))]
        if c is not None:
            lines.append(("Change", _signed(_bn(c, unit))))
        return _kv(lines) + (f"<br>{_grey(r['note'])}" if col == "first" and r.get("note") else "")
    if sid == "goods-services":
        lines = [(lab, _num(_bn(v[k], unit))) for k, lab in GS if v.get(k) is not None]
        if c is not None:
            lines.append(("Change", _signed(_bn(c, unit))))
        return _kv(lines) + (f"<br>{_grey(r['note'])}" if col == "first" and r.get("note") else "")
    if sid in ("fx-sterling", "fx-mark", "fx-franc"):
        return (f"{_num(v, 2)}¢ " + _grey(FX_UNIT[sid]) + (f", {_signed(c, 2)}¢" if c is not None else "") + note)
    if sid == "gold-london":
        return f"${_num(v, 2)}" + (f", {_signed(c, 2)}" if c is not None else "") + note
    if sid == "debt-interest-rate":
        return f"{_num(v, 3)}%" + (f", {_signed(c, 3)} pt" if c is not None else "") + note
    if sid == "debt-maturity":
        return _nw(_yrmo(v)) + (", " + _nw(f"{_signed(c, 0)} mo") if c is not None else "") + note
    if sid == "debt-ownership":
        lines = [(lab, _num(_bn(v[k], unit))) for k, lab in OWN if v.get(k) is not None]
        return _kv(lines) + (f"<br>{_grey(r['note'])}" if col == "first" and r.get("note") else "")
    return "—"


# ---------------------------------------------------------------- the table of exchange rates and gold (STYLE 4)

def fx_table(rows, year, name, cells):
    """rows: [(sid, s, r)]; name(sid, s, r): the name cell; cells(sid, s, r, year): (first, released, today)."""
    trs = []
    for sid, s, r in rows:
        first, rel, _ = cells(sid, s, r, year)
        trs.append(f'<tr><td class="iname">{name(sid, s, r)}</td><td>{first}</td><td class="rel">{rel}</td></tr>')
    if not trs:
        return ""
    return ('<div class="ind ind-sep ind-fx"><p class="ind-cap">Exchange rates and gold</p><table><thead><tr>'
            '<th>Rate</th><th>As first reported</th><th>Released</th></tr></thead><tbody>' + "".join(trs)
            + "</tbody></table></div>")


# ---------------------------------------------------------------- checks

def problems(data):
    """For ./bib check: each transcribed figure has its unit or the series' unit, its issue and its source; the
    stacked figures their parts, and their totals add up."""
    out = []
    for sid in ALL:
        s = data.get(sid)
        if not s:
            continue
        for r in s.get("rows", []):
            if "first" not in r:
                continue
            if not r.get("source") or not r.get("released"):
                out.append((sid, f"{r['p']}: first figure without its source or issue"))
            f = r["first"]
            if sid == "reserve-assets":
                if not isinstance(f, dict) or f.get("total") is None:
                    out.append((sid, f"{r['p']}: reserve assets without a total"))
                    continue
                parts = sum(f.get(k) or 0 for k in ("gold", "currencies", "imf"))
                if abs(parts - f["total"]) > 1.5:
                    out.append((sid, f"{r['p']}: gold, currencies and IMF ({parts}) do not make the total "
                                     f"({f['total']}); a misreading?"))
            if sid == "debt-ownership":
                if not isinstance(f, dict) or None in [f.get(k) for k in ("total", "trust", "fed", "private")]:
                    out.append((sid, f"{r['p']}: ownership lacks a part"))
                elif abs(f["trust"] + f["fed"] + f["private"] - f["total"]) > 0.15:
                    out.append((sid, f"{r['p']}: holders do not make the total; a misreading?"))
            if sid == "goods-services" and (not isinstance(f, dict) or f.get("goods_services") is None):
                out.append((sid, f"{r['p']}: balances not stacked"))
    return out
