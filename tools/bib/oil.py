"""The Oil group of the calendar's monthly indicator tables: how its cells read, its definitions, its checks.

    indicators/oil-*.yaml, written by tools/indicators/make_oil.py (its docstring has the sources). indicators.py files
    the rows and lays out the table; this module renders the oil cells (first_cell, now_cell) and supplies DEFS.

STYLE (settled; keep it):
 1. Volumes in millions of barrels a day, two decimals: "7.23m b/d". The Survey of Current Business printed barrels in
    the month (thousands to Sept. 1961, millions after); the first column divides by the month's days, the source
    figure on hover. EIA's figures today are in thousand barrels a day. Reserves in billions of barrels, two decimals:
    "31.61bn bbl".
 2. No changes: the Survey's latest column is the figure read, and a change from the month before would mix two
    issues' figures. Levels only, in both columns.
 3. Trade stacked, one line each, label left, figure right (as the budgets): Imports, Exports, Net (imports less
    exports); the first column sums crude and refined products as the Survey printed them, "<.05" (its note, under
    50,000 barrels) and "—" (none printed) counted as nothing. Monthly figures then; EIA's monthly trade begins in 1973,
    so the year's row (filed in December) carries today's figures and the month's rows "—" today (indicators STYLE 8).
 4. A corrected misprint or a change of what a row counts shows in grey after the figure, as printed (NOTE in the
    script): Survey figures stand as first printed.
"""
import calendar

SERIES = ("oil-production", "oil-supplied", "oil-trade", "oil-trade-year", "oil-reserves")
MINUS = "−"

EIA = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s="
SCB = "https://fraser.stlouisfed.org/title/survey-current-business-46"
MER = "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T03.01"
MYB = "https://archive.org/details/pub_usgov-minerals-yearbook_"
_SCB_NOTE = (f"As first reported: the Bureau of Mines' figure as the [*Survey of Current Business*]({SCB}) (Commerce) "
             "first printed it, in its monthly statistical pages, \"Petroleum and products\" (p. S-35), two to four months "
             "after the month; barrels in the month, shown here a day. The Bureau's own Monthly Petroleum Statement, "
             "earlier, not read here. Released: the Survey's issue.")
DEFS = {
    "oil-production": f"Crude petroleum produced in the United States, field production. {_SCB_NOTE} Today: EIA, U.S. field production of crude oil, thousand barrels a day ([EIA MCRFPUS2]({EIA}MCRFPUS2&f=M)). The Survey misprinted May 1965 (283.3m bbl for 238.3) and Dec. 1966 (286.3 for 263.8), corrected in later issues; shown as printed, the correction in grey. Crude only: natural gas liquids not included.",
    "oil-supplied": f"Domestic demand for all oils: crude, refined products and natural gas liquids taken into domestic use (\"products supplied\" today), by disappearance: production plus imports, less exports and the change in stocks. {_SCB_NOTE} Today: EIA, U.S. product supplied of crude oil and petroleum products ([EIA MTTUPUS2]({EIA}MTTUPUS2&f=M)), monthly from 1963 only; \"—\" before.",
    "oil-trade": f"Imports and exports of crude petroleum and of refined products, by month: the Survey's four figures summed by kind, net imports the difference. {_SCB_NOTE} From the issue of Apr. 1969 crude imports are \"crude and unfinished oils\". Imports were limited from Mar. 10, 1959, by Proclamation 3279 (the Mandatory Oil Import Program; the thread Oil). No monthly figure today: EIA's monthly trade series begin in 1973; the year's figures today are the row below, in December.",
    "oil-trade-year": f"Petroleum imports, exports and net imports for the year, crude and products together, thousand barrels a day: EIA, [*Monthly Energy Review*, Table 3.1]({MER}), annual from 1949. Retrospective: one column. The month's figures as first reported are the row above.",
    "oil-reserves": f"Proved reserves of crude oil at Dec. 31: oil recoverable from known fields under existing economic and operating conditions. As first reported: the estimate of the American Petroleum Institute's Committee on Petroleum Reserves, as the Bureau of Mines' *Minerals Yearbook* for the year printed it, a year or more later (the API's own report, each spring, not read here): [1960]({MYB}1960_2), II, 372; [1961]({MYB}1961_2), II, 365; [1962]({MYB}1962_2), II, 382; [1963]({MYB}1963_2), II, 398; [1964]({MYB}1964_2), II, 391; [1965]({MYB}1965_2), II, 357; [1966]({MYB}1966_12), I–II, 816, Table 3; [1967]({MYB}1967_12), I–II, 843; [1968]({MYB}1968_12), I–II, 817. Released: the Yearbook's year of printing. Today: EIA ([RCRR01NUS_1]({EIA}RCRR01NUS_1&f=A)), whose figures before 1977 are the API's. Natural gas liquids not included.",
}


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


def _kv(lines):
    from .indicators import esc
    return '<span class="kv">' + "".join(
        f'<span class="k">{esc(a)}</span><span class="v">{esc(b)}</span>' for a, b in lines) + "</span>"


def first_cell(sid, s, r):
    v, unit, p = r.get("first"), r.get("unit"), r["p"]
    if v is None:
        return "—"
    note = (" " + _grey(f"({r['note']})")) if r.get("note") else ""
    if sid in ("oil-production", "oil-supplied"):
        return _mbd(_bbl(v, unit) / _days(p) / 1e6) + note
    if sid == "oil-trade":
        d = _days(p)
        imp = (_bbl(v.get("crude_imports"), unit) + _bbl(v.get("product_imports"), unit)) / d / 1e6
        exp = (_bbl(v.get("crude_exports"), unit) + _bbl(v.get("product_exports"), unit)) / d / 1e6
        return _kv([("Imports", _mbd(imp)), ("Exports", _mbd(exp)), ("Net", _mbd(imp - exp))]) + (
            f"<br>{_grey(r['note'])}" if r.get("note") else "")
    if sid == "oil-reserves":
        return f"{v / 1000:.2f}bn bbl" + note
    return "—"


def now_cell(sid, s, r):
    v = r.get("now")
    if v is None:
        return "—"
    if sid in ("oil-production", "oil-supplied"):
        return _mbd(v / 1000)
    if sid == "oil-trade-year":
        return _kv([("Imports", _mbd(v["imports"] / 1000)), ("Exports", _mbd(v["exports"] / 1000)),
                     ("Net", _mbd(v["net"] / 1000))])
    if sid == "oil-reserves":
        return f"{v / 1000:.2f}bn bbl"
    return "—"


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
