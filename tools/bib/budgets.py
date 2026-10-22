"""Federal budgets and the debt limit in the calendar: budgets/budgets.yaml (each fiscal year's budget, fiscal 1961-1970,
kept by hand from the Budget documents), budgets/today.yaml (OMB's figures today, written by tools/budgets/make_today.py)
and budgets/debt-limits.yaml (the thirteen acts changing the debt limit, June 30, 1960-Apr. 7, 1969, kept by hand).

A calendar entry tagged budget:<FY> (the January budget message for that fiscal year) carries the year's two tables; the
entry tagged debt-limits (the Debt limit thread's first) carries the table of acts.

STYLE
 1. The budget block: two tables, stacked, each fitting the calendar's column and a phone (~400px) without sideways
    scrolling. First the budget as the January Budget proposed it and as first reported (the Budget two Januaries
    later, which first printed the year's actual; for fiscal 1967's expenditures by function, the Treasury's Annual
    Report), receipts by source then expenditures by function, on its own basis (the administrative budget to fiscal
    1968, the unified from fiscal 1969; its title says which): "Fiscal 1964: the administrative budget, proposed and
    first reported". Then OMB's Historical Tables (2.1, 3.1) today, unified, on today's functions, receipts by source
    then outlays by function, never summed with the first: "Fiscal 1964 on today's unified basis (OMB, Historical
    Tables 2.1, 3.1)", its column headed by the edition read ("FY2025 ed."). "Today" never stands alone in a title or a
    head, where it could be read as the current fiscal year (the owner's request, Oct. 22, 2026).
 2. No column empty for every row of its table: a column a source does not give is left out, not filled with "—" or
    "n.a." (fiscal 1968 has no first-reported column; its note says why). Rows: a line shares a row with the other
    column's only where the source means the same thing by it (the key in the data). A renamed line keeps its row, the
    source's own words on hover; a reclassified line (the functions of fiscal 1963's budget, Food for Peace moved to
    international affairs in fiscal 1966's) is a row of its own, "—" in the other column. The sources' order, the
    proposal's lines first. OMB's function with no outlays that year (Medicare before fiscal 1966) is left out.
 3. Money in $bn, one decimal, the head saying "$bn", the cells bare and unbroken, right-aligned (indicators STYLE 3,
    10); the line's name wraps; the source's own figure and unit on hover. A deduction printed as such is negative
    (U+2212). "*" is the source's "less than $50 million"; "—" no such line in this column.
 4. Totals: the printed total of each column, whatever the lines add to (`check` holds the lines to it within
    rounding: half a unit a line); a total the source labels otherwise says so on hover.
 5. Under each table its notes, then its sources: for the first, each column's document, table, printed page, linked
    to the page of FRASER's scan; for the second, OMB's tables, linked, and the edition.
 6. The debt-limit table: one row an act, in order: the day approved (linked to its calendar entry), the Statutes cite
    (linked to govinfo) with the bill under it, muted (four columns, to fit a phone without scrolling), the limits it set, each with its term, and the permanent limit after it. Limits in
    whole $bn ("$308bn"), terms as dates in the series' form; a limit with no end date is permanent.
"""
import os
import re

from . import contents, store

DIR = os.path.join(store.ROOT, "budgets")
_C = {}
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
FRASER = "https://fraser.stlouisfed.org/files/docs/publications/{series}/{file}#page={page}"
STAT = "https://www.govinfo.gov/content/pkg/STATUTE-{vol}/pdf/{granule}.pdf"
TOL = {"m": 0.5, "bn": 0.05}
STYLE = """<style id="bgstyle">
.bg{margin:1rem 0 .5rem;font-family:var(--sans)}
.bg .bgh{font-weight:700;font-size:.95rem;margin:.2rem 0 .4rem}
.bg .bgw{overflow-x:auto;-webkit-overflow-scrolling:touch}
.bg .bgh2{margin-top:1.1rem}
.bg table{border-collapse:collapse;width:100%;font-size:.78rem;font-variant-numeric:tabular-nums;line-height:1.35}
.bg th,.bg td{text-align:right;padding:.18rem 0 .18rem .6rem;vertical-align:bottom;border-bottom:1px solid var(--rule)}
.bg table.bgb td{white-space:nowrap}
.bg table.bgb td:first-child{white-space:normal}
.bg th:first-child,.bg td:first-child{text-align:left;padding-left:0}
.bg thead th{font-weight:600;color:var(--muted);font-size:.74rem;line-height:1.25}
.bg tr.bgs th{text-align:left;font-weight:700;padding-top:.6rem;color:var(--ink);border-bottom:1px solid var(--ink)}
.bg tr.bgt td{font-weight:700}
.bg td.na{color:var(--muted)}
.bg .bgn{font-size:.78rem;line-height:1.45;color:var(--note);margin:.3rem 0}
.bg .bgsrc{font-size:.78rem;color:var(--muted);line-height:1.4;margin:.3rem 0}
.bg td.dlt{text-align:left;white-space:normal}
@media (max-width:520px){.bg td.dlt{min-width:7rem}}
@media (max-width:380px){.bg td.dlt{min-width:5.5rem}}
.bg .dlb{color:var(--muted);white-space:nowrap}  /* the bill under its statute: four columns fit a phone */
</style>"""


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def ital(t):
    return re.sub(r"\*([^*]+)\*", r"<i>\1</i>", esc(t))


def load(name):
    if name not in _C:
        p = os.path.join(DIR, name)
        _C[name] = (store.load_yaml(p) if os.path.exists(p) else None) or {}
    return _C[name]


def budgets():
    return {int(k): v for k, v in load("budgets.yaml").items() if str(k).isdigit()}


def docs():
    return load("budgets.yaml").get("docs") or {}


def today():
    return {int(k): v for k, v in (load("today.yaml").get("years") or {}).items()}


def acts():
    return load("debt-limits.yaml").get("acts") or []


def date(iso):
    y, m, d = (iso.split("-") + ["", ""])[:3]
    if not d:
        return f"{MON[int(m) - 1]} {y}"
    return f"{MON[int(m) - 1]} {int(d)}, {y}"


def minus(s):
    return s.replace("-", "−")


def bn(v, unit):
    """The figure in $bn, one decimal; None for a missing one."""
    if v is None or v == "*":
        return None
    return v / 1000.0 if unit == "m" else float(v)


def cell(v, unit, printed=None):
    if v == "*":
        return '<td title="less than $50 million">*</td>'
    if v is None:
        return '<td class="na">—</td>'
    src = f"{v:,}" if unit == "m" else f"{v:.1f}"
    tip = f"{src} ({'millions' if unit == 'm' else 'billions'})" + (f"; printed: {printed}" if printed else "")
    return f'<td title="{esc(minus(tip))}">{minus(f"{bn(v, unit):,.1f}")}</td>'


NA = '<td class="na">—</td>'


def then_table(fy):
    """The budget as the Budget proposed it and as first reported: the columns that have a figure, and the sections
    (title, [(key, [cells])], [total cells]), receipts then expenditures."""
    B = budgets().get(fy) or {}
    cols = [(name, B.get(col)) for col, name in (("proposed", "Proposed"), ("actual", "First reported")) if B.get(col)]
    secs = []
    for part, title in (("receipts", "Receipts by source"), ("expenditures", "Expenditures by function")):
        blks = [c.get(part) or {} for _, c in cols]
        if any(b.get("basis") == "unified" for b in blks):
            title = title.replace("Expenditures", "Outlays")
        keys = []
        for blk in blks:
            for r in blk.get("rows") or []:
                if r[0] not in keys:
                    keys.append(r[0])
        rows = []
        for k in keys:
            cells = []
            for blk in blks:
                hit = [r for r in blk.get("rows") or [] if r[0] == k]
                cells.append(cell(hit[0][1], blk["unit"], hit[0][2] if len(hit[0]) > 2 else None) if hit else NA)
            rows.append((k, cells))
        tot = [cell(b.get("total"), b.get("unit"), b.get("total_label")) if b else NA for b in blks]
        secs.append((title, rows, tot))
    return cols, secs


def now_table(fy):
    """OMB's figures today: [(title, [(key, cell)], total cell)], receipts then outlays; a function with no outlays
    that year (Medicare before fiscal 1966) left out."""
    T = today().get(fy) or {}
    out = []
    for part, title in (("receipts", "Receipts by source"), ("outlays", "Outlays by function")):
        t = T.get(part) or {}
        rows = [(r[0], cell(r[1], "m")) for r in t.get("rows") or [] if r[1] is not None]
        out.append((title, rows, cell(t.get("total"), "m") if t.get("total") is not None else NA))
    return out


def colhead(blk, label):
    d = docs().get((blk or {}).get("doc")) or {}
    when = f"<br>{date(d['sent'])}" if d.get("sent") else ""
    return f"<th>{label}{when}</th>"


def cite(blk):
    d = docs().get(blk["doc"]) or {}
    url = FRASER.format(series=d.get("series", "usbudget"), file=d.get("file", ""), page=blk.get("pdf", 1))
    return f'<i>{esc(d.get("title", ""))}</i>, {esc(blk.get("table", ""))}, p. {esc(blk.get("page", ""))} (<a href="{esc(url)}">FRASER</a>)'


def sources(fy):
    B = budgets().get(fy) or {}
    out = []
    for col, name in (("proposed", "Proposed"), ("actual", "First reported")):
        c = B.get(col)
        if not c:
            continue
        r, e = c.get("receipts"), c.get("expenditures")
        if r and e and (r["doc"], r.get("table"), r.get("page")) == (e["doc"], e.get("table"), e.get("page")):
            out.append(f"{name}: {cite(r)}.")
        else:
            out.append(f"{name}: receipts, {cite(r)}; expenditures, {cite(e)}.")
    return " ".join(out)


def now_sources():
    src = load("today.yaml").get("source") or {}
    if not src:
        return ""
    return (f'<a href="{esc(src["receipts"]["url"])}">{ital(src["receipts"]["title"])}</a>; '
            f'<a href="{esc(src["outlays"]["url"])}">{ital(src["outlays"]["title"])}</a> ({esc(src.get("edition", ""))}).')


def edition():
    """The OMB edition read, short: "FY2025 ed." from "Budget of the U.S. Government, Fiscal Year 2025"."""
    m = re.search(r"Fiscal Year (\d{4})", (load("today.yaml").get("source") or {}).get("edition", ""))
    return f"FY{m.group(1)} ed." if m else "OMB"


def table(head, secs):
    n = head.count("<th")
    body = []
    for title, rows, tot in secs:
        body.append(f'<tr class="bgs"><th colspan="{n}">{esc(title)}</th></tr>')
        for k, cells in rows:
            body.append(f"<tr><td>{esc(k)}</td>{''.join(cells)}</tr>")
        body.append(f'<tr class="bgt"><td>Total</td>{"".join(tot)}</tr>')
    return f'<div class="bgw"><table class="bgb"><thead>{head}</thead><tbody>{"".join(body)}</tbody></table></div>'


def block(fy):
    B = budgets().get(fy)
    if not B:
        return ""
    cols, secs = then_table(fy)
    unified = any((c.get(p) or {}).get("basis") == "unified" for _, c in cols for p in ("receipts", "expenditures"))
    names = [n for n, _ in cols]
    title = (f'Fiscal {fy}: the {"unified" if unified else "administrative"} budget, '
             + (" and ".join(n.lower() for n in names)))
    head = "<tr><th>$bn</th>" + "".join(colhead(c.get("receipts"), n) for n, c in cols) + "</tr>"
    notes = [c.get("note") for _, c in cols if c.get("note")]
    if B.get("note"):
        notes.append(B["note"])
    out = (f'<div class="bg" id="bg{fy}"><p class="bgh">{esc(title)}</p>{table(head, secs)}'
           + "".join(f'<p class="bgn">{esc(n)}</p>' for n in notes)
           + f'<p class="bgsrc">{sources(fy)}</p>')
    now = now_table(fy)
    if any(rows for _, rows, _ in now):
        out += (f'<p class="bgh bgh2">Fiscal {fy} on today\'s unified basis (OMB, <i>Historical Tables</i> 2.1, 3.1)</p>'
                + table(f"<tr><th>$bn</th><th>{esc(edition())}</th></tr>", [(t, [(k, [c]) for k, c in rows], [tot])
                                                                         for t, rows, tot in now])
                + '<p class="bgn">OMB\'s figures, revised, on the unified basis and today\'s functions: not comparable '
                  'line by line with the budget above.</p>'
                + f'<p class="bgsrc">{now_sources()}</p>')
    return out + "</div>"


def limit_text(t):
    frm, to, lim = t
    if to is None:
        return f"${lim:g}bn from {date(frm)}, permanent"
    if frm == to:
        return f"${lim:g}bn on {date(frm)}"
    return f"${lim:g}bn, {date(frm)}–{date(to)}"


def debt_block():
    rows, perm = [], load("debt-limits.yaml").get("permanent")
    for a in acts():
        vol, page = a["stat"].split("|")
        perm = a.get("permanent", perm)
        d = date(a["date"])
        when = f'<a href="#{esc(a["entry"])}">{d}</a>' if a.get("entry") else d
        lims = "<br>".join(esc(limit_text(t)) for t in a["terms"])
        tip = f' title="{esc(a["does"])}"' if a.get("does") else ""
        rows.append(f'<tr><td>{when}</td><td><a href="{esc(STAT.format(vol=vol, granule=a["granule"]))}">{vol} Stat. {page}</a>'
                    f'<br><span class="dlb">{esc(a["bill"])}</span></td><td class="dlt"{tip}>{lims}</td>'
                    f'<td>${perm:g}bn</td></tr>')
    src = load("debt-limits.yaml").get("source") or {}
    return ('<div class="bg" id="bgdebt"><p class="bgh">The debt limit: the acts of 1960–69</p><div class="bgw"><table>'
            '<thead><tr><th>Approved</th><th>Statute, bill</th><th>Limit and term</th><th>Permanent</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="bgn">The limit in section 21 of the Second Liberty Bond Act on the public debt outstanding; each '
            'temporary limit lapsed at the end of its term to the permanent one.</p>'
            f'<p class="bgsrc">The limits: <a href="{esc(src.get("url", ""))}">{ital(src.get("title", ""))}</a>; each act '
            'read in the Statutes at Large.</p></div>')


def tagged(series):
    out = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^budget:(\d{4})$", t)
                if m:
                    out[int(m.group(1))] = e["id"]
                elif t == "debt-limits":
                    out["debt"] = e["id"]
    return out


def inject(page, series):
    used = False
    for key, eid in tagged(series).items():
        blk = debt_block() if key == "debt" else block(key)
        if not blk:
            continue
        page, k = contents.put(page, eid, blk, "debt-limits" if key == "debt" else "budget", key)
        used = used or bool(k)
    if used and 'id="bgstyle"' not in page:
        page = page.replace("</head>", STYLE + "\n</head>", 1)
    return page


def problems(series=None):
    out = []
    B, T = budgets(), today()
    for fy, b in B.items():
        if fy not in T:
            out.append(("budgets/today.yaml", f"fiscal {fy}: no figures for today"))
        for col in ("proposed", "actual"):
            c = b.get(col)
            if c is None:
                if col == "proposed":
                    out.append(("budgets/budgets.yaml", f"fiscal {fy}: no proposal"))
                continue
            for part in ("receipts", "expenditures"):
                blk = c.get(part)
                if not blk:
                    out.append(("budgets/budgets.yaml", f"fiscal {fy} {col}: no {part}"))
                    continue
                if blk.get("doc") not in docs():
                    out.append(("budgets/budgets.yaml", f"fiscal {fy} {col} {part}: no such document {blk.get('doc')}"))
                if blk.get("unit") not in TOL or blk.get("basis") not in ("administrative", "unified"):
                    out.append(("budgets/budgets.yaml", f"fiscal {fy} {col} {part}: unit or basis missing"))
                    continue
                rows = blk.get("rows") or []
                bad = [r for r in rows if not (isinstance(r, list) and len(r) in (2, 3) and isinstance(r[0], str)
                                               and (r[1] == "*" or isinstance(r[1], (int, float))))]
                if bad:
                    out.append(("budgets/budgets.yaml", f"fiscal {fy} {col} {part}: malformed rows {bad[:2]}"))
                    continue
                keys = [r[0] for r in rows]
                if len(set(keys)) != len(keys):
                    out.append(("budgets/budgets.yaml", f"fiscal {fy} {col} {part}: a row twice"))
                s = sum(r[1] for r in rows if r[1] != "*")
                tol = TOL[blk["unit"]] * (len(rows) + 1)
                if blk.get("total") is None or abs(s - blk["total"]) > tol:
                    out.append(("budgets/budgets.yaml", f"fiscal {fy} {col} {part}: the lines add to {s:g}, the printed "
                                                         f"total is {blk.get('total')}"))
    for fy, t in T.items():
        for part in ("receipts", "outlays"):
            s = sum(r[1] or 0 for r in t[part]["rows"])
            if abs(s - t[part]["total"]) > len(t[part]["rows"]):
                out.append(("budgets/today.yaml", f"fiscal {fy} {part}: the lines add to {s}, the total is {t[part]['total']}"))
    last, perm = "", load("debt-limits.yaml").get("permanent")
    for a in acts():
        where = f"budgets/debt-limits.yaml {a.get('date')}"
        if not re.match(r"^\d{4}-\d\d-\d\d$", str(a.get("date", ""))) or a["date"] <= last:
            out.append((where, "a date missing or out of order"))
        last = str(a.get("date", ""))
        if not re.match(r"^\d+\|\d+$", str(a.get("stat", ""))) or not str(a.get("granule", "")).startswith(
                "STATUTE-" + str(a.get("stat", "")).split("|")[0] + "-Pg" + str(a.get("stat", "|")).split("|")[1]):
            out.append((where, f"the cite {a.get('stat')} and the govinfo granule {a.get('granule')} disagree"))
        for t in a.get("terms") or []:
            if not (isinstance(t, list) and len(t) == 3 and isinstance(t[2], (int, float))
                    and (t[1] is None or str(t[0]) <= str(t[1]))):
                out.append((where, f"a malformed term {t}"))
        if not a.get("terms"):
            out.append((where, "no limit"))
    if series is not None:
        ids = {e["id"] for lst in series.lists.values() if lst.kind == "calendar" for _, e in lst.entries()}
        for a in acts():
            if a.get("entry") and a["entry"] not in ids:
                out.append(("budgets/debt-limits.yaml", f"{a['date']}: no calendar entry {a['entry']}"))
        for key, eid in tagged(series).items():
            if key != "debt" and key not in B:
                out.append((eid, f"budget:{key}: no such fiscal year in budgets/budgets.yaml"))
    return out
