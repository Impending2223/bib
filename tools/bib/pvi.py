"""Checks for the partisan voting index by district: the presidential vote by district read off the Census's Data Books
(elections/readings/districts/, loaded by tools/elections/cd_readings.py) and what tools/elections/make_pvi.py makes of
it (elections/pvi-districts.yaml, elections/cd-president.yaml); and renders them (the owner, Oct. 28, 2026: "Show both.
Be sure to cite and attribute": the indexes and the figures they are made from).

STYLE
 1. Errors: a reading's figures that do not add (cd_readings.problems: the districts to the State column, the States
    to the printed United States figures unless the volume says `us_holds: false`, D and R (and A, where the volume's
    `fields` hold it) not over the total unless `over` says the page prints it so); an `eye`, `marks`, `over` or
    `as_printed` entry naming no cell; a `pages` list that does not name every column once; a district the
    Congress of the source's `lines` does not seat; a generated file missing, or made from other inputs (its `inputs`,
    a hash of every file make_pvi.py reads: cd_readings.inputs_hash).
 2. Warnings [pvi]: a printed percent the figures do not give, not listed in `percent_as_printed` (the percent is not
    used).

SHOWN (in each election's block on congress.html and the calendar's `election:` entries; elections.block calls these)
 3. The index: "R+5" (a point, rounded), "EVEN" under half a point, as make_pvi.py writes it. Under each House race's
    seat, the district's; under each Senate race's class, the State's; in the President's table, the State's for that
    year's House and Senate elections. A map view of its own, "PVI" (`pv`, points, Republican positive): gray at even
    to eR4 or eB4 at PVI_MAX points, the swing view's scale (templates/congress.html).
 4. Folded under the race tables: "Partisan voting index: States" (the State, its index, the two years' two-party
    Republican shares and the nation's, the basis) and "... districts" (each district of the Congress, its index and
    inputs, or "n.a." and why: `none`); and, in the block of the election whose Congress's lines a Data Book gives, "The
    presidential vote by district" as the volume prints it (total, Democratic, Republican, and American Independent
    for 1968), a row a district and year, the State's column first, each State linked to its page in the copy read,
    the page's footnotes under it, what does not add said as `printed` says it.
 5. Attribution (the owner's rule): every table names its source by page and the compilers the Census names for each
    year's figures (the Republican Congressional Committee for 1952; Congressional Quarterly for 1956 and 1960 in the
    1961 volume, *America Votes* and CQ in the 1963 and 1965 volumes; the National Republican Congressional Committee
    for 1968), in the volume's words where it gives them. Facts, not their selection or arrangement, are taken
    (Feist Publications, Inc. v. Rural Telephone Service Co., 499 U.S. 340 (1991)); the tables are the series' own.
"""
import os

from . import store

ROOT = store.ROOT


def _readings():
    import sys
    sys.path.insert(0, os.path.join(ROOT, "tools", "elections"))
    import cd_readings
    return cd_readings


def problems(series=None):
    """[(level, where, message)]."""
    cd = _readings()
    out = []
    srcs = cd.load()
    for k, d in srcs.items():
        where = d["path"]
        for w, m in cd.problems(d):
            out.append(("error", w, m))
        for w, m in cd.warnings(d):
            out.append(("warn", w, m))
        roster = os.path.join(ROOT, "congress", f"{d.get('lines')}.yaml")
        seated = None
        if os.path.exists(roster):
            seated = {(m["st"], int(m["d"])) for m in store.load_yaml(roster)["house"]}
        years = [str(y) for y in d.get("years") or []]
        for st, e in (d.get("states") or {}).items():
            rows = {int(x) for x in (e.get("d") or {})}
            cols = [int(x) for p in (e.get("pages") or {}).values() for x in p]
            if sorted(cols) != sorted(rows):
                out.append(("error", where, f"{st}: pages name {sorted(cols)}; rows are {sorted(rows)}"))
            if seated is not None:
                for x in rows:
                    if x and (st, x) not in seated:
                        out.append(("error", where, f"{st} {x}: no such district in the {d.get('lines')}th Congress"))
            for fld in ("eye", "marks"):
                if e.get(fld) == "all":
                    continue
                for ent in e.get(fld) or []:
                    p = str(ent).split()
                    if len(p) != 3 or int(p[0]) not in rows or p[1] not in years or p[2] not in cd.fields(d):
                        out.append(("error", where, f"{st} {fld}: '{ent}' names no cell"))
            for ent in e.get("as_printed") or []:
                p = str(ent).split()
                if len(p) != 2 or p[0] not in years or p[1] not in cd.fields(d):
                    out.append(("error", where, f"{st} as_printed: '{ent}' names no State figure"))
            for ent in e.get("over") or []:
                p = str(ent).split()
                if len(p) != 2 or int(p[0]) not in rows or p[1] not in years:
                    out.append(("error", where, f"{st} over: '{ent}' names no row"))
    if srcs:
        want = cd.inputs_hash()
        for name in ("pvi-districts.yaml", "cd-president.yaml"):
            path = os.path.join(ROOT, "elections", name)
            have = (store.load_yaml(path) or {}).get("inputs") if os.path.exists(path) else None
            if have != want:
                out.append(("warn", f"elections/{name}",
                            "missing or made from other inputs: run python3 -I tools/elections/make_pvi.py"))
    return out


# ---------------------------------------------------------------- shown (STYLE 3-5)

ARCHIVE = "https://archive.org/details/{item}/page/n{leaf}"
GOVINFO = "https://www.govinfo.gov/content/pkg/{pkg}/pdf/{pkg}.pdf#page={page}"
CENSUS = "U.S. Bureau of the Census"
# Each volume: its citation, the copy read, how a printed page finds its scan (leaf = page + leaf; govinfo's PDF page
# = page + pdf), and the compilers the volume names, year by year (each header in elections/readings/districts/).
VOLUMES = {
    "cdb-1961": {
        "cite": "*Congressional District Data Book (Districts of the 87th Congress)* (1961), table 1, items 75–84",
        "item": "congressionaldis1961unit", "leaf": 29, "copy": "the Boston Public Library's copy, archive.org",
        "compiled": "1952: the Republican Congressional Committee, *Congressional and Presidential Vote Comparison* "
                    "(1957); 1956: Congressional Quarterly, CQ Weekly Report, supplement to May 10, 1957; 1960: CQ "
                    "Weekly Report, pt. II of Mar. 10, 1961 (p. XI). The volume's notice (p. XI): \u201cThe 1956 and "
                    "1960 figures are copyrighted by Congressional Quarterly News Features.\u201d Not recomputed on "
                    "the 87th Congress's lines for the districts redrawn after 1952 or 1956 (p. XI).",
        "intro": 11},
    "cdb-1963": {
        "cite": "*Congressional District Data Book (Districts of the 88th Congress)* (1963; H. Doc. 132, 88th Cong., "
                "1st Sess.), table 1, items 1–10",
        "pkg": "SERIALSET-12613_00_00-002-0132-0000", "pdf": 45, "copy": "govinfo's scan of the Serial Set",
        "compiled": "Whole-county districts: the Governmental Affairs Institute, *America Votes* 1, 3 and 4 (1956, "
                    "1959, 1962); split-county districts: Congressional Quarterly, CQ Weekly Report, supplement to "
                    "May 10, 1957, and Mar. 10, 1961, pt. II (p. XV). \u201cFor many split-county districts, however, "
                    "it was not possible to recompute the vote cast figures for 1960 and prior years, as indicated "
                    "by the entry \u2018n.a.\u2019\u201d (p. XV).",
        "intro": 15},
    "cdb-1965": {
        "cite": "*Congressional District Data Book (Districts of the 89th Congress)*, Supplements Nos. 1–7, "
                "*Redistricted States* (Jan. 1965; H. Doc. 33, 89th Cong., 1st Sess.)",
        "pkg": "SERIALSET-12706_01_00-002-0033-0000", "pdf": 0, "pdf_pages": True,
        "copy": "govinfo's scan of the Serial Set (unpaged: the PDF's page)",
        "compiled": "The 88th Congress's volume's figures \u201cretabulated for the geographic areas encompassed "
                    "within the new boundaries\u201d (Supp. No. 1, p. 1): *America Votes* for whole-county districts, "
                    "Congressional Quarterly for split-county ones; \u201c(NA)\u201d where a split-county district "
                    "could not be retabulated."},
    "cdb-1973": {
        "cite": "*Congressional District Data Book, 93d Congress* (1973; H. Doc. 93-109), table 1, items 13–17",
        "item": "congressionaldis00unit", "leaf": 21, "copy": "the NIH Library's copy, archive.org",
        "compiled": "The National Republican Congressional Committee, *Congressional District Vote Comparison*, "
                    "\u201cretabulated by the Committee to reflect the congressional district boundaries as "
                    "established for the 1972 elections\u201d; the votes of third parties endorsing a major party's "
                    "candidate are in the total, not in that party's column (pp. X–XI): New York's Democratic figures "
                    "leave out Humphrey's Liberal line.",
        "intro": 10},
}
LABEL = {"t": "Total", "D": "Dem.", "R": "Rep.", "A": "Am. Ind."}


def _esc(t):
    import html
    return html.escape(str(t), quote=True)


def _md(t):
    """*italics* and the escape."""
    import re
    return re.sub(r"\*([^*]+)\*", r"<i>\1</i>", _esc(t))


def page_url(src, page):
    v = VOLUMES[src]
    if "item" in v:
        return ARCHIVE.format(item=v["item"], leaf=int(page) + v["leaf"])
    return GOVINFO.format(pkg=v["pkg"], page=int(page) + v["pdf"])


def page_label(src, page):
    return f"PDF p. {page}" if VOLUMES[src].get("pdf_pages") else f"p. {page}"


def source_line(src):
    """The volume's citation, linked to the copy read, and its compilers (STYLE 5)."""
    v = VOLUMES[src]
    first = page_url(src, v.get("intro") or 1)
    return (f'{CENSUS}, <a href="{_esc(first)}">{_md(v["cite"])}</a> ({_esc(v["copy"])}). '
            f'Compiled by: {_md(v["compiled"])}')


_CACHE = {}


def _gen(name):
    if name not in _CACHE:
        path = os.path.join(ROOT, "elections", name)
        _CACHE[name] = store.load_yaml(path) if os.path.exists(path) else {}
    return _CACHE[name]


def states(year):
    """{st: rec} of elections/pvi.yaml for the election of `year` (the States' index)."""
    y = (_gen("pvi.yaml").get("years") or {}).get(year) or {}
    return y.get("states") or {}


def districts(year):
    """The election's district block of elections/pvi-districts.yaml, or {}."""
    return (_gen("pvi-districts.yaml").get("elections") or {}).get(year) or {}


def dkey(st, seat):
    return f"{st}-{'AL' if not seat else seat}"


def seat_pvi(year, ch, st, seat):
    """The record shown under a race's seat: the district's (House) or the State's (Senate); None."""
    if ch == "h":
        return (districts(year).get("districts") or {}).get(dkey(st, seat))
    return states(year).get(st)


def cell(rec, what):
    """'<br><span class="es pvi" title="...">R+5</span>' under a seat, or ''."""
    if not rec or not rec.get("pvi"):
        return ""
    return (f'<br><span class="es pvi" title="Partisan voting index of the {what}: {_esc(rec.get("basis") or "")}">'
            f'{_esc(rec["pvi"])}</span>')


def _share(v):
    return "—" if v is None else f"{v:.1f}"


def _defn(year, frm):
    a, b = frm
    return (f'The partisan voting index: the two-party Republican share of the presidential vote, {a} and {b} '
            f'averaged, less the nation\'s; \u201cR+5\u201d leans Republican by five points, \u201cEVEN\u201d '
            f'under half a point (the Cook Political Report\'s construct as it stood 1997–2021). Computed by the '
            f'series (tools/elections/make_pvi.py).')


def state_table(year):
    """Folded: each State's index for the election (STYLE 4)."""
    from .congress import STATE
    y = (_gen("pvi.yaml").get("years") or {}).get(year)
    if not y:
        return ""
    a, b = y["from"]
    nat = y.get("nation") or {}
    rows = []
    for st in sorted(y["states"], key=lambda s: STATE.get(s, s)):
        r = y["states"][st]
        basis = r.get("basis") or ""
        rows.append(f'<tr><td>{_esc(STATE.get(st, st))}</td><td class="pvn">{_esc(r.get("pvi") or "n.a.")}</td>'
                    f'<td class="pvn">{_share(r.get("r" + str(a)))}</td><td class="pvn">{_share(r.get("r" + str(b)))}</td>'
                    f'<td class="pvb">{_esc("" if basis == f"{a} and {b}" else basis)}</td></tr>')
    return (f'<details class="cgr er pvt"><summary>Partisan voting index: States, from {a} and {b}</summary>'
            f'<table><thead><tr><th>State</th><th>PVI</th><th>R {a}</th><th>R {b}</th><th>Basis</th></tr></thead>'
            f'<tbody><tr class="st"><td>Nation</td><td class="pvn"></td><td class="pvn">{_share(nat.get("r" + str(a)))}</td>'
            f'<td class="pvn">{_share(nat.get("r" + str(b)))}</td><td></td></tr>{"".join(rows)}</tbody></table>'
            f'<p class="elsrc">{_defn(year, (a, b))} R {a}, R {b}: the Republican share of the two-party vote for '
            f'President, percent. The States\' returns: the Clerk\'s <i>Statistics of the Presidential and '
            f'Congressional Election</i> for each year, as in the President\'s tables.</p></details>')


def district_table(year):
    """Folded: each district's index for the election, or why none (STYLE 4)."""
    from .congress import STATE
    E = districts(year)
    if not E or not E.get("computed"):
        return ""
    a, b = E["from"]
    ds = E.get("districts") or {}
    none = E.get("none") or {}
    nat = _gen("pvi-districts.yaml").get("nation") or {}

    def order(k):
        st, d = k.split("-", 1)
        return (STATE.get(st, st), 0 if d == "AL" else int(d))
    out = []
    last = None
    used = set()
    for k in sorted(set(ds) | set(none), key=order):
        st, d = k.split("-", 1)
        if st != last:
            out.append(f'<tr class="st"><th colspan="5">{_esc(STATE.get(st, st))}</th></tr>')
            last = st
        if k in ds:
            r = ds[k]
            used.update(r.get("from") or [])
            basis = r.get("basis") or ""
            out.append(f'<tr><td>{_esc(d)}</td><td class="pvn">{_esc(r["pvi"])}</td>'
                       f'<td class="pvn">{_share(r.get("r" + str(a)))}</td><td class="pvn">{_share(r.get("r" + str(b)))}</td>'
                       f'<td class="pvb">{_esc("" if basis == f"{a} and {b}" else basis)}</td></tr>')
        else:
            out.append(f'<tr class="pvx"><td>{_esc(d)}</td><td class="pvn">n.a.</td>'
                       f'<td class="pvb" colspan="3">{_esc(why(none[k]))}</td></tr>')
    srcs = " ".join(source_line(s) for s in sorted(used))
    return (f'<details class="cgr er pvt"><summary>Partisan voting index: districts, from {a} and {b}, '
            f'{E["computed"]} with an index, {E.get("without", 0)} without</summary>'
            f'<table><thead><tr><th>District</th><th>PVI</th><th>R {a}</th><th>R {b}</th><th>Basis</th></tr></thead>'
            f'<tbody><tr class="st"><td>Nation</td><td></td><td class="pvn">{_share((nat.get(a) or {}).get("r"))}</td>'
            f'<td class="pvn">{_share((nat.get(b) or {}).get("r"))}</td><td></td></tr>{"".join(out)}</tbody></table>'
            f'<p class="elsrc">{_defn(year, (a, b))} A district takes figures on another Congress\'s lines only '
            f'where its shape is the same in both; a State with no two-party race in a year takes the other year '
            f'alone. The district figures: {srcs}</p></details>')


def why(text):
    """make_pvi.py's reason a district has no index, in words (STYLE 4): each year's, the same said once."""
    import re
    out = []
    for part in text.split("; "):
        m = re.match(r"(\d{4}): (.*)$", part)
        if not m:
            out.append(part)
            continue
        y, r = m.groups()
        if r == "no source gives the State":
            r = "not read by district"
        elif "lines not the" in r:
            r = "on other lines, the district since redrawn"
        elif "not given (na)" in r:
            r = "\u201cn.a.\u201d in the Data Book (a split county not recomputed)"
        elif "not given (nil)" in r:
            r = "no vote printed"
        elif "not given (fn)" in r:
            r = "not available, as the Data Book's footnote says"
        elif "no such district" in r:
            r = "no such district on the source's lines"
        elif "redrawn after" in r:
            r = "redrawn since, as the Data Book's note says; not recomputed"
        out.append((y, r))
    said = {}
    for x in out:
        if isinstance(x, tuple):
            said.setdefault(x[1], []).append(x[0])
    parts = [f"{' and '.join(ys)}: {r}" for r, ys in said.items()] + [x for x in out if not isinstance(x, tuple)]
    return "; ".join(parts) + "."


def _footnote(data, st, d, mark):
    """The text of footnote `mark` on the page that holds district d of State st (the 1961 volume's footnotes by page)."""
    e = data["states"][st]
    fn = data.get("footnotes") or {}
    for page, cols in (e.get("pages") or {}).items():
        if d in cols:
            return ((fn.get(page) or {}).get(mark)) if isinstance(fn.get(page), dict) else None
    return None


def vote_table(lines):
    """Folded: the presidential vote by district as the Data Book on these lines prints it (STYLE 4), or ''."""
    import sys
    from .congress import STATE
    cd = _readings()
    out = []
    for src, data in cd.load().items():
        if data.get("lines") != lines or src not in VOLUMES:
            continue
        flds = [f for f in cd.fields(data) if f != "p"]
        years = [int(y) for y in data.get("years") or []]
        ncol = 1 + len(flds)
        rows = []
        for st, e in (data.get("states") or {}).items():
            pages = e.get("pages") or {}
            plinks = ", ".join(f'<a href="{_esc(page_url(src, pg))}">{page_label(src, pg)}</a>' for pg in pages)
            rows.append(f'<tr class="st"><th colspan="{ncol}">{_esc(STATE.get(st, st))} <span class="pvp">{plinks}</span></th></tr>')
            marks = e.get("marks") or {}
            notes = {}
            single = list((e.get("d") or {})) == [0]
            for d in sorted(int(x) for x in (e.get("d") or {})):
                row = e["d"][d]
                lab = "AL" if single else ("State" if d == 0 else str(d))
                for i, y in enumerate(years):
                    vals = dict(zip(cd.fields(data), row.get(y) or row.get(str(y)) or []))
                    cells = []
                    for f in flds:
                        v = vals.get(f)
                        txt = "n.a." if v in ("na", "fn") else "…" if v in ("nil", None) else f"{v:,}"
                        m = marks.get(f"{d} {y} {f}")
                        if m is not None:
                            t = _footnote(data, st, d, m)
                            if t:
                                notes[m] = t
                            txt += f"<sup>{m}</sup>"
                        cells.append(f'<td class="pvn">{txt}</td>')
                    rows.append(f'<tr{" class=pvs" if d == 0 and not single else ""}><td class="pvy">'
                                f'<span class="pvd">{lab if i == 0 else ""}</span>{y}</td>{"".join(cells)}</tr>')
            fns = e.get("footnotes")
            text = " ".join(f"{k} {v}" for k, v in sorted(notes.items())) if notes else (fns if isinstance(fns, str) else "")
            extra = " ".join(x for x in (text, e.get("printed") or "") if x)
            if extra:
                rows.append(f'<tr class="pvf"><td colspan="{ncol}">{_md(extra)}</td></tr>')
        head = "".join(f"<th>{LABEL[f]}</th>" for f in flds)
        yrs = ", ".join(str(y) for y in sorted(years))
        nst = len(data.get("states") or {})
        n_st = f" ({nst} States redistricted)" if nst < 50 else ""
        out.append(f'<details class="cgr er pvt pvv"><summary>The vote for President by district, {yrs}, on the '
                   f'{_ord(lines)} Congress\'s lines{n_st}, as the Census printed it</summary>'
                   f'<table><thead><tr><th><span class="pvd">Dist.</span>Year</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>'
                   f'<p class="elsrc">{source_line(src)} Figures as printed; superscripts the page\'s footnotes; '
                   f'\u201cn.a.\u201d not available, \u201c…\u201d no vote. The State\'s row is its printed column.</p></details>')
    return "\n".join(out)


def _ord(n):
    from .congress import ordinal
    return ordinal(n)


def block(year, congress):
    """Everything the election's block shows of the index and its figures (STYLE 4)."""
    return "\n".join(x for x in (state_table(year), district_table(year), vote_table(congress)) if x)
