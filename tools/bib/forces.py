"""The armed forces a year: forces/us.yaml (the United States: men, where they were, units, ships, aircraft, missiles,
nuclear weapons) and forces/world.yaml (the world's men under arms, ships and warheads), both kept by hand, every
figure read off a page (their headers are the schema).

    block(year)          the year's tables, as HTML: the United States, then the world, each table with its date, its
                         note and its sources. year is the year the figures count (June 30, 1965, is 1965).
    afd_block(y)         what goes under Armed Forces Day of year y (tools/bib/afday.py, a day block): block(y - 1), the
                         last figures dated before the day. afday calls it and sets the anchor (contents.day_mark,
                         kind "forces", label "Armed forces, <y>"); the style comes with the block.
    years()              the years with figures; label(year): "Armed forces, 1965"
    problems(series)     the checks (tools/bib/check.py)

The owner's request, Oct. 20-22, 2026: the machines (aircraft, ships, armor, missiles) and the men, a table a year,
apart from the economic tables, under Armed Forces Day; the world beside them where an open source gives it.

STYLE (keep it):
 1. One block a year, the United States first ("United States"), then the world ("The world"), each a small-capital
    heading. Each table folds (a <details>), its summary the table's title and date ("Military personnel on active
    duty, June 30, 1965"); the first, the men on active duty, open. The order is the file's.
 2. A table's columns are the sources' figures for that date: "Printed then" (what was published at the time, the
    *Statistical Abstract* reprinting the Department's and the Budget's tables) beside "DMDC today" or "FAS today"
    where a later figure exists; a column a year lacks is left out, never shown empty (budgets STYLE 2). A table
    classified then (the Air Force's *Statistical Digest*) says so in its note.
 3. Rows the year has, in the file's order; a heading row (`group`) only where a row under it shows; a total (`sum`)
    in bold, its parts indented above it. The source's dash is "–"; "(Z)" its "less than 500"; a fraction or a pair
    as printed ("26½", "4/3").
 4. Figures right-aligned, tabular, with commas; the unit in the date line ("in thousands"). A figure the source prints
    though its parts do not make it, or with a footnote of its own, is underlined dotted with the note on hover, and
    the notes follow the table in a line ("Notes: ..."), so a phone shows them too. A row the source labels otherwise
    that year carries the source's label on hover.
 5. Phone width: no table wider than the column; a table of many columns (the world's ships) is split into tables of
    three or four figures (`split`), the label repeated, the label column at least 8.5em. The labels wrap; the figures do not.
 6. Under each table, its sources, each linked to the page read: the column's head, a colon, the citation.
 7. Not persons: no names are linked here; the block is figures.
"""
import html
import os
import re

from . import store

DIR = os.path.join(store.ROOT, "forces")
FILES = {"us": "us.yaml", "world": "world.yaml"}
PART = {"us": "United States", "world": "The world"}
YEARS = range(1960, 1969)
UNIT = {"persons": "", "count": "", "thousands": "in thousands"}
_C = {}

STYLE = """<style id="fcstyle">
/* The armed forces a year (tools/bib/forces.py, STYLE) */
div.fc{font-family:var(--sans);font-size:.8rem;line-height:1.35;font-variant-numeric:tabular-nums;margin:.3rem 0 .4rem}
div.fc .fch{margin:.55rem 0 .15rem;font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
div.fc details{margin:0 0 .15rem}
div.fc summary{cursor:pointer;font-weight:600;padding:.12rem 0}
div.fc summary .fcd{font-weight:400;color:var(--muted)}
div.fc table.fct{border-collapse:collapse;width:100%;table-layout:auto;margin:.15rem 0 .2rem}
div.fc table.fct th,div.fc table.fct td{padding:.08rem 0 .08rem .7rem;border-bottom:1px solid var(--rule);vertical-align:bottom;
  text-align:right;font-weight:400;white-space:nowrap}
div.fc table.fct th:first-child,div.fc table.fct td:first-child{text-align:left;padding-left:0;white-space:normal;width:100%;
  min-width:8.5em}
div.fc table.fct thead th{color:var(--muted);font-weight:600;font-size:.72rem;line-height:1.2;white-space:normal;
  border-bottom:1px solid var(--ink);vertical-align:bottom}
div.fc table.fct tr.fcg td{font-weight:600;padding-top:.35rem;border-bottom:0}
div.fc table.fct tr.fcs td{font-weight:700}
div.fc table.fct td.i1{padding-left:.8rem}
div.fc table.fct td.i2{padding-left:1.6rem}
div.fc .fcp{text-decoration:underline dotted;text-underline-offset:2px;cursor:help}
div.fc .fcn,div.fc .fcsrc{margin:.1rem 0 .3rem;font-size:.72rem;color:var(--muted);line-height:1.35}
div.fc .fcsrc a{color:inherit}
</style>"""


def esc(t):
    return html.escape(str(t), quote=True)


def md(t):
    """The cite's *italics* and plain text, escaped."""
    return re.sub(r"\*([^*]+)\*", r"<i>\1</i>", esc(t))


def load(which):
    if which not in _C:
        p = os.path.join(DIR, FILES[which])
        _C[which] = (store.load_yaml(p) if os.path.exists(p) else None) or {}
    return _C[which]


def years():
    out = set()
    for w in FILES:
        for t in load(w).get("tables") or []:
            out |= {int(y) for y in (t.get("years") or {})}
    return sorted(out)


def label(year):
    return f"Armed forces, {year}"


def num(v):
    if v is None:
        return "–"
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, int):
        return f"{v:,}"
    if isinstance(v, float):
        return f"{v:,}"
    return str(v)


def value(v):
    """The figure as a number for the sums: a fraction as printed ('26½') counts, '(Z)' and a pair do not."""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return v
    if isinstance(v, str):
        m = re.match(r"^(\d+)([¼½¾])?E?$", v.replace(",", ""))
        if m:
            return int(m.group(1)) + {"¼": .25, "½": .5, "¾": .75, None: 0}[m.group(2)]
    return 0


def _shown_rows(t, cols):
    """The rows the year shows: each row any column has (a dash included); a heading where a row under it shows."""
    keys = [r for r in t["rows"] if not r.get("group") and any(r["key"] in c for c in cols.values())]
    have = {r["key"] for r in keys}
    out, pend = [], None
    for r in t["rows"]:
        if r.get("group"):
            pend = r
        elif r["key"] in have:
            if pend is not None:
                out.append(pend)
                pend = None
            out.append(r)
    return out


def _cell(c, key, note_rows):
    v = c.get(key)
    s = esc(num(v))
    if v == "(Z)":
        return '<span class="fcp" title="Less than 500">(Z)</span>'
    if key in note_rows:
        return f'<span class="fcp" title="{esc(note_rows[key])}">{s}</span>'
    return s


def _date(t, year):
    a = str(t.get("asof") or "")
    when = (f"{a}, {year}" if re.match(r"^[A-Z][a-z]{2,4}\.? \d", a) else f"{year}, {a}" if a and a != str(year)
            else str(year))
    u = UNIT.get(t.get("unit"), "")
    return when + (f"; {u}" if u else "")


def table_html(which, t, year, open_=False):
    srcs = load(which).get("sources") or {}
    ys = (t.get("years") or {}).get(year) or (t.get("years") or {}).get(str(year))
    if not ys:
        return ""
    colspec = [c for c in t["cols"] if c["key"] in ys]
    cols = {c["key"]: ys[c["key"]] for c in colspec}
    rows = _shown_rows(t, cols)
    notes = []                                       # (row label, column head, note)
    labels = {r["key"]: r["label"] for r in t["rows"]}
    heads = {c["key"]: c["head"] for c in colspec}
    for ck, c in cols.items():
        for rk, why in (c.get("printed") or {}).items():
            notes.append((labels.get(rk, rk), heads[ck], why))
    groups = t.get("split") or [[c["key"] for c in colspec]]
    tables = []
    for g in groups:
        g = [k for k in g if k in cols]
        if not g:
            continue
        head = "<th></th>" + "".join(f"<th>{esc(heads[k])}</th>" for k in g)
        body = []
        for r in rows:
            if r.get("group"):
                body.append(f'<tr class="fcg"><td colspan="{len(g) + 1}">{esc(r["label"])}</td></tr>')
                continue
            as_ = [c.get("as", {}).get(r["key"]) for c in cols.values() if (c.get("as") or {}).get(r["key"])]
            lab = esc(r["label"])
            if as_:
                lab = f'<span class="fcp" title="Printed: {esc(as_[0])}">{lab}</span>'
            ind = r.get("indent")
            cls = ' class="fcs"' if r.get("sum") else ""
            tds = "".join(f"<td>{_cell(cols[k], r['key'], cols[k].get('printed') or {})}</td>" for k in g)
            body.append(f'<tr{cls}><td{f" class=\"i{ind}\"" if ind else ""}>{lab}</td>{tds}</tr>')
        tables.append(f'<table class="fct"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table>')
    note = f'<p class="fcn">{md(t["note"])}</p>' if t.get("note") else ""
    if notes:
        note += ('<p class="fcn">Notes: ' + " ".join(f"{esc(a)}{', ' + esc(b) if len(cols) > 1 else ''}: {md(c)}"
                                                  + ("" if c.rstrip().endswith((".", "?")) else ".")
                                                  for a, b, c in notes) + "</p>")
    seen, parts = set(), []
    for ck, c in cols.items():
        s = srcs.get(c.get("src")) or {}
        key = c.get("src")
        cite = (f'<a href="{esc(s["url"])}">{md(s.get("cite", key))}</a>' if s.get("url") else md(s.get("cite", key)))
        if key in seen:
            continue
        seen.add(key)
        same = [heads[k] for k, cc in cols.items() if cc.get("src") == key]
        note_s = md(s["note"]) if s.get("note") else ""
        parts.append((f"{esc(', '.join(same))}: " if len(set(cc.get('src') for cc in cols.values())) > 1 else "") + cite
                     + (f". {note_s.rstrip('.')}" if note_s else ""))
    src = '<p class="fcsrc">Sources: ' + "; ".join(parts) + ".</p>"
    return (f'<details{" open" if open_ else ""}><summary>{esc(t["title"])} <span class="fcd">{esc(_date(t, year))}'
            f'</span></summary>{"".join(tables)}{note}{src}</details>')


def block(year):
    """The year's tables (figures counted in that year), or '' where there are none."""
    year = int(year)
    out = []
    first = True
    for w in FILES:
        ts = [table_html(w, t, year, open_=first and w == "us" and i == 0)
              for i, t in enumerate(load(w).get("tables") or [])]
        ts = [x for x in ts if x]
        if ts:
            out.append(f'<p class="fch">{esc(PART[w])}, {year}</p>' + "".join(ts))
            first = False
    if not out:
        return ""
    return STYLE + f'<div class="fc" data-forces="{year}">{"".join(out)}</div>'


def afd_block(y):
    """Under Armed Forces Day of year y: the figures of the year before (afday.py's caption says so)."""
    return block(int(y) - 1)


# ---------------------------------------------------------------- checks

def problems(series=None):
    out = []
    for w, fn in FILES.items():
        where = f"forces/{fn}"
        d = load(w)
        if not d:
            out.append((where, "missing or empty"))
            continue
        srcs = d.get("sources") or {}
        for k, s in srcs.items():
            if not (s or {}).get("cite"):
                out.append((where, f"source {k}: no cite"))
        keys = set()
        for t in d.get("tables") or []:
            tk = t.get("key")
            if tk in keys:
                out.append((where, f"table {tk}: key used twice"))
            keys.add(tk)
            rows = {r["key"]: r for r in t.get("rows") or []}
            if len(rows) != len(t.get("rows") or []):
                out.append((where, f"{tk}: a row key used twice"))
            colk = [c["key"] for c in t.get("cols") or []]
            for r in t.get("rows") or []:
                if set(r) - {"key", "label", "sum", "group", "indent"} or not isinstance(r.get("label"), str):
                    out.append((where, f"{tk}: row {r.get('key')}: stray fields {sorted(set(r) - {'key', 'label', 'sum', 'group', 'indent'})} (a comma in an unquoted label?)"))
            for c in t.get("cols") or []:
                if set(c) - {"key", "head"} or not isinstance(c.get("head"), str):
                    out.append((where, f"{tk}: column {c.get('key')}: stray fields (a comma in an unquoted head?)"))
            tol = t.get("tol", 0)
            for r in rows.values():
                for p in r.get("sum") or []:
                    if p not in rows:
                        out.append((where, f"{tk}: row {r['key']} sums {p}, no such row"))
            for g in t.get("split") or []:
                for k in g:
                    if k not in colk:
                        out.append((where, f"{tk}: split names column {k}, no such column"))
            if t.get("split") and sorted(k for g in t["split"] for k in g) != sorted(colk):
                out.append((where, f"{tk}: split does not take every column once"))
            sumcols = t.get("sumcols") or {}
            for y, ys in (t.get("years") or {}).items():
                if int(y) not in YEARS:
                    out.append((where, f"{tk} {y}: outside 1960-68"))
                for ck, c in (ys or {}).items():
                    at = f"{tk} {y} {ck}"
                    if ck not in colk:
                        out.append((where, f"{at}: no such column"))
                        continue
                    if c.get("src") not in srcs:
                        out.append((where, f"{at}: source {c.get('src')!r} not in sources"))
                    printed = c.get("printed") or {}
                    for rk in list(printed) + list(c.get("as") or {}):
                        if rk not in rows:
                            out.append((where, f"{at}: note on {rk}, no such row"))
                    for rk, v in c.items():
                        if rk in ("src", "printed", "as"):
                            continue
                        if rk not in rows:
                            out.append((where, f"{at}: {rk}, no such row"))
                        elif rows[rk].get("group"):
                            out.append((where, f"{at}: {rk} is a heading, not a figure"))
                        elif not (v is None or isinstance(v, (int, str)) and not isinstance(v, bool)):
                            out.append((where, f"{at} {rk}: {v!r} is not a figure"))
                    for r in rows.values():
                        parts = [p for p in r.get("sum") or [] if p in c]
                        if not r.get("sum") or r["key"] not in c or not parts or r["key"] in printed:
                            continue
                        s = sum(value(c[p]) for p in parts)
                        if abs(value(c[r["key"]]) - s) > tol:
                            out.append((where, f"{at}: {r['key']} {num(c[r['key']])}, its parts {num(s)}"))
                for total, parts in sumcols.items():
                    tc = (ys or {}).get(total)
                    if not tc:
                        continue
                    for rk, v in tc.items():
                        if rk in ("src", "printed", "as") or rk in (tc.get("printed") or {}):
                            continue
                        got = [(ys[p] or {}).get(rk) for p in parts if p in ys and rk in (ys[p] or {})]
                        if not got:
                            continue
                        s = sum(value(x) for x in got)
                        if abs(value(v) - s) > tol:
                            out.append((where, f"{tk} {y}: {rk} total {num(v)}, the columns {num(s)}"))
    return out
