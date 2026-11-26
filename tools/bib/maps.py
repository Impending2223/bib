"""The two maps wherever they stand (the owner, Nov. 25, 2026: "Both. In each calendar under the day of the first China
entry. 図 for both SEA and China. Put them on the relevant threads top, scoped to the thread's content and the page's
range ... Default each calendar page to its range. Could we have a span filter, with two text fields entered by
default but modifiable by hand?"): the maps of Indochina (tools/bib/vnmap.py) and the map of China (cnmap.py) in the
calendar's pages, at the head of the threads' pages, and listed on a page of their own (build/maps.html), which the
top bar's one mark 図 leads to. Each map's own page (indochina.html, china.html) is its module's and its page's
(indochina.py, china.py); the span, its fields and the entries' files are here for all.

One figure and one client for every place (vnmap.js, vnmap.css): a figure differs from another by its data alone.

STYLE
 1. The entries' files. Each map's placed entries go beside the pages a file a year, build/geo/<vn|cn>-entries-<year>-
    <hash>.json: {"k": the threads' slugs, "e": the entries in the calendar's order}; an entry its link (`h`, to its
    calendar page), its date as written (`w`), its day (`d`: its place in the calendar, loose.place_iso: a month's
    first day for a month, Jan. 1 for a year, the day its `at:` gives; the calendar's first day where that falls
    before it, as "1960" and "January 1960" do), its chief thread's name (`t`), the first words
    of its statement (`s`), its places (`p`), the units it names whole (`v`), and its threads (`k`: its `thread` and
    its `also`, as numbers into the file's `k`). A page carries no entry: the client reads the files of the years the
    span touches, when the map nears the screen. So a calendar page is a few kilobytes the heavier for its two maps.
 2. The span. Every figure has two text fields, From and to, in a bar of their own above the map's controls (a second
    .vnm-bar; the fields in the select's look: vnmap.css). The build writes the page's own range into them, in the
    calendar's form ("Apr. 1, 1961"); the map, the tap's lists, the folded list and the count show the entries whose
    day falls within the span, both ends in. A field reads the calendar's form or a plain ISO date ("1961-04-15");
    a month or a year alone reads as its first day in the first field and its last in the second; what does not read
    (a date half typed, Feb. 30, "4/15/1961") changes nothing; a first day after the last shows no entry. The span is
    taken at each keystroke once both fields read; on leaving a field its date is written out in the calendar's form.
    On a map's own page the year buttons stay and fill the two fields; "All years" fills the calendar's whole span.
 3. In the calendar (replacing vnmap STYLE 8's map a year): each page that holds an entry placed on a map carries that
    map, at the day block's place (dayblocks STYLE 1: under the date and the day's entries) of the day of the page's
    first such entry that stands on a day; where none stands on a day, at the end of the first such entry. Titled as
    a listed table is, by its span ("China, Jan.–Mar. 1966"; "Southeast Asia 1969": contents.KINDS `vnmap`, `cnmap`),
    and listed in the page's contents; the fields open on the page's range (calsplit.part_range). Indochina's above
    China's where both fall on one day; both above the day's Southeast Asia table. In the reader, a part's block as
    its page.
 4. On a thread's page (threads STYLE 5): the map at the head, under the statement, the thread's subthreads (threads
    STYLE 9) and the parts' bar, for a thread
    whose line of parents holds one of the map's roots (ROOTS: `china`; `vietnam`, `laos`, `cambodia`,
    `southeast-asia`), by the line, not by a list of names; the thread's own entries alone (those the page lists:
    its `thread` or its `also`), the fields on the page's range (a part's dates; the calendar's whole span for a page
    not divided, and for a divided thread's own page). No placed entry in the page's range, no map.
 5. A figure away from its map's page keeps that page's figure: the map of China in its own proportion (.vnm.full),
    the map of Indochina in the calendar's box. Its last line leads to the map's page (.vnm-pg, as the annual maps'
    did); a tap's "In the gazetteer" leads to the place's row there.
 6. maps.html: a heading and the two maps as the front page lists them (ol.e.lists, its rules copied from
    templates/series.html, since templates/list.html lacks them): the name, what the page holds, its span.
"""
import datetime
import json

from . import calsplit, chron, contents, loose, store

_C = {}
ROOTS = {"cn": ("china",), "vn": ("vietnam", "laos", "cambodia", "southeast-asia")}


def modules():
    from . import cnmap, vnmap
    return [vnmap, cnmap]


def calendar(series):
    return next((l for l in series.lists.values() if l.kind == "calendar"), None)


# ---------------------------------------------------------------- dates and spans

def pad(d):
    """An entry's day from its date as written: '1963' -> '1963-01-01', '1963-04' -> '1963-04-01'."""
    s = str(d)[:10]
    return s + {4: "-01-01", 7: "-01"}.get(len(s), "")


def day(d):
    """A day in the calendar's form: "Apr. 15, 1961" (vnmap.js showDate)."""
    return f"{contents.MONTHS[d.month - 1]} {d.day}, {d.year}"


def span(lo, hi):
    """A span as the calendar writes one: "Apr. 1–June 30, 1961"; "Aug. 1–31, 1966"; "Jan. 6, 1960–Aug. 31, 1976"; one
    day, "Apr. 15, 1961" (vnmap.js showSpan)."""
    if lo == hi:
        return day(lo)
    if (lo.year, lo.month) == (hi.year, hi.month):
        return f"{contents.MONTHS[lo.month - 1]} {lo.day}–{hi.day}, {lo.year}"
    a = day(lo)
    return (a[:-6] if lo.year == hi.year else a) + "–" + day(hi)


def title(key):
    """A calendar map's span for its title, from its key ("1966-01-01.1966-03-31"): "Jan.–Mar. 1966", "1969"; and
    whether it is a bare year (no comma before it: contents STYLE 5)."""
    from . import threads
    try:
        lo, hi = (datetime.date.fromisoformat(x) for x in key.split("."))
    except ValueError:
        return key, key.isdigit()
    lab = threads.label(lo, hi)
    return lab, lab.replace("–", "").isdigit()


def fields(lo, hi):
    """The span's two fields (STYLE 2), filled with the page's range."""
    f = lambda k, d: (f'<input type="text" data-sp="{k}" size="13" value="{day(d)}" autocomplete="off" '
                      'spellcheck="false">')
    return f'<div class="vnm-bar"><label>From {f("from", lo)}</label><label>to {f("to", hi)}</label></div>'


# ---------------------------------------------------------------- the entries, a file a year (STYLE 1)

def entries(series, m):
    """{"rows": every placed entry of the map m, in the calendar's order, "files": {year: path from a page},
    "ys": the years}. A row is the file's entry, with what the build alone needs under `_` keys: `_id`, `_n` (its
    part of the calendar), `_day` (it stands on a day), and `k` its threads' slugs."""
    key = (m.KEY, id(series))
    if key in _C:
        return _C[key]
    from . import vnmap
    from .build import thread_name
    lst = calendar(series)
    saved = dict(calsplit.CUR)
    calsplit.CUR.update(half=None, mode="list")       # every link names its calendar page
    rows = []
    try:
        G = m.gazetteer()
        got = {e["id"]: (e, [p for p in pl if p in G], pv) for rs in (m.by_year(series) if m.ready() else {}).values()
               for e, pl, pv in rs}
        got = {k: v for k, v in got.items() if v[1] or v[2]}       # on the map: a place it holds, or a unit
        split = bool(calsplit.cfg(lst))
        first = calsplit.bounds(lst)[0].isoformat()     # "1960", "January 1960": before the calendar's first day
        for e in chron.sort(lst, [t[0] for t in got.values()]):
            _, pl, pv = got[e["id"]]
            iso = loose.place_iso(e)
            n = calsplit.half_of_date(lst, iso) if split else 1
            rows.append({"h": calsplit.href(lst, n, e["id"]), "w": e["when"], "d": max(pad(iso), first),
                         "t": thread_name(lst, e["thread"]), "s": vnmap._summary(e.get("c")),
                         "p": pl, "v": pv,
                         "k": list(dict.fromkeys([e["thread"]] + list(e.get("also") or []))),
                         "_id": e["id"], "_n": n, "_day": loose.order_key(e)[1] == 1})
    finally:
        calsplit.CUR.clear()
        calsplit.CUR.update(saved)
    by = {}
    for r in rows:
        by.setdefault(r["d"][:4], []).append(r)
    files = {}
    for y, rs in sorted(by.items()):
        slugs = sorted({s for r in rs for s in r["k"]})
        ix = {s: i for i, s in enumerate(slugs)}
        d = {"k": slugs, "e": [{**{k: v for k, v in r.items() if k[0] != "_"}, "k": [ix[s] for s in r["k"]]} for r in rs]}
        data = json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode()
        files[y] = vnmap._put(f"geo/{m.KEY}-entries-{y}-{vnmap._hash(data)}.json", data)
    _C[key] = {"rows": rows, "files": files, "ys": sorted(by)}
    return _C[key]


def within(rows, lo, hi, th=None):
    a, b = lo.isoformat(), hi.isoformat()
    return [r for r in rows if a <= r["d"] <= b and (th is None or th in r["k"])]


def count(rows):
    """"12 placed entries, at 9 places.": the caption's count, as the client writes it (vnmap.js refresh)."""
    n, p = len(rows), len({p for r in rows for p in r["p"]})
    return f"{n:d} placed {'entry' if n == 1 else 'entries'}, at {p} {'place' if p == 1 else 'places'}."


def data(d):
    return json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


# ---------------------------------------------------------------- a figure away from its map's page

def figure(series, m, lo, hi, th=None, here=None):
    """The map m for the span lo to hi (dates), a thread's entries alone with `th`: '' where the span holds no placed
    entry. here: the prefix of the page's own anchors for the entries it holds ('' in the reader, 't-' on a thread's
    page), so that a list's link stays on the page where it can; None on a calendar page."""
    E = entries(series, m)
    rows = [r for r in E["rows"] if th is None or th in r["k"]]
    inn = within(rows, lo, hi)
    if not inn:
        return ""
    ys = sorted({r["d"][:4] for r in rows})
    d = dict(m.DATA, eu={y: E["files"][y] for y in ys}, ys=ys, sp=[lo.isoformat(), hi.isoformat()], gz=m.PAGE)
    if th:
        d["th"] = th
    if here is not None:
        d["here"] = here
    at = f"#y{lo.year}" if lo.year == hi.year else ""
    return (f'<figure {m.FIGURE} data-geo="{m.manifest(series)}">'
            f'<figcaption class="vnm-cap"><span class="vnm-cnt">{span(lo, hi)}: {count(inn)}</span> {m.TAIL}</figcaption>'
            + fields(lo, hi) + m.box(f"{m.LABEL}, {span(lo, hi)}") +
            f'<details class="vnm-list"><summary>The placed entries ({len(inn)})</summary><ol></ol></details>'
            f'<p class="vnm-pg">Every year on one map, with the gazetteer: <a href="{m.PAGE}{at}">{m.NAME}</a>.</p>'
            f'<script type="application/json" class="vnm-d">{data(d)}</script></figure>')


def head(page):
    """The client's style and script on a page that carries a figure, once."""
    from . import vnmap
    if 'class="vnm-css"' in page or '<figure class="vnm' not in page:
        return page
    css, js = vnmap.head_tags()
    page = page.replace("</head>", css.replace("<link ", '<link class="vnm-css" ') + "\n</head>", 1)
    return page.replace("</body>", js + "\n</body>", 1)


# ---------------------------------------------------------------- in the calendar (STYLE 3)

def stands(series):
    """{(part, kind): (day or None, entry id)}: where each map stands in each part of the calendar: the day of the
    part's first placed entry that stands on a day, and the part's first placed entry."""
    key = ("stands", id(series))
    if key not in _C:
        out = {}
        if calendar(series) is not None:
            for m in modules():
                for r in entries(series, m)["rows"]:
                    k = (r["_n"], m.KIND)
                    got = out.setdefault(k, [None, r["_id"]])
                    if got[0] is None and r["_day"]:
                        got[0] = r["d"]
        _C[key] = {k: tuple(v) for k, v in out.items()}
    return _C[key]


def days(series):
    """The days a map stands under, for the day blocks' placeholders (dayblocks.marker)."""
    key = ("days", id(series))
    if key not in _C:
        _C[key] = frozenset(d for d, _ in stands(series).values() if d)
    return _C[key]


def inject(page, series, mode):
    """Each map set in the calendar page being built (mode "list": the part calsplit.CUR names, or the whole of a
    calendar not in parts) or in the reader ("series": every part's block), before the day blocks are filled."""
    from . import dayblocks
    lst = calendar(series)
    if lst is None:
        return page
    split = calsplit.cfg(lst)
    half = calsplit.CUR["half"] if mode == "list" else None
    parts = [half] if half else list(range(1, len(calsplit.parts(lst)) + 1))
    plan = stands(series)
    for n in parts:
        lo, hi = calsplit.part_range(lst, n if split else None)
        for m in modules():
            iso, eid = plan.get((n, m.KIND), (None, None))
            if eid is None:
                continue
            fig = figure(series, m, lo, hi, here="" if mode == "series" else None)
            if not fig:
                continue
            key = f"{lo.isoformat()}.{hi.isoformat()}"
            mark = dayblocks.MARK.format(iso) if iso else None
            if mark and mark in page:
                page = page.replace(mark, contents.day_mark(m.KIND, key, iso, list(m.THREADS)) + fig + mark, 1)
            elif f'<li id="{eid}"' in page:
                page, _ = contents.put(page, eid, fig, m.KIND, key)
    return head(page)


# ---------------------------------------------------------------- on a thread's page (STYLE 4)

def of_thread(lst, slug):
    """The map a thread's page carries, by the thread's line of parents: the module, or None."""
    T = lst.threads()
    line, s = [], slug
    while s and s not in line:
        line.append(s)
        s = (T.get(s) or {}).get("parent")
    for m in modules():
        if any(x in ROOTS[m.KEY] for x in line):
            return m
    return None


def thread_figure(series, lst, slug, lo, hi):
    """The figure at the head of a thread's page for its range, or ''."""
    m = of_thread(lst, slug)
    return figure(series, m, lo, hi, th=slug, here="t-") if m else ""


def thread_slugs(lst):
    """{map key: [the threads whose pages may carry it]}, in the index's order: for the guide and the report."""
    out = {}
    for s, te in lst.threads().items():
        m = None if te.get("see") else of_thread(lst, s)
        if m:
            out.setdefault(m.KEY, []).append(s)
    return out


# ---------------------------------------------------------------- maps.html (STYLE 6)

CSS = """<style id="mapscss">
/* the two maps as the front page lists them: templates/series.html's own rules (tools/bib/maps.py, STYLE 6) */
ol.lists>li{display:flex;align-items:baseline;gap:1rem;justify-content:space-between}
ol.lists a.lk{text-decoration:none;color:var(--ink);display:flex;gap:.75rem;align-items:baseline;min-width:0}
ol.lists .ab{font-family:var(--sans);font-weight:800;min-width:6.6rem;flex:none}
ol.lists a.lk:hover .tt{color:var(--accent);text-decoration:underline}
ol.lists .r{white-space:nowrap}
</style>"""


def listing(m, series=None):
    """A map's line in a list of pages, in the front page's markup: its name, what its page holds, its span."""
    return (f'<li><a class="lk" href="{m.PAGE}"><span class="ab">{m.NAME}</span><span class="tt">{m.BLURB}</span></a>'
            f'<span class="r">{m.SPAN}</span></li>')


def page(series, template):
    """build/maps.html: the page the top bar's 図 leads to."""
    ms = [m for m in modules() if m.ready()]
    if not ms:
        return None
    main = ["<h1>Maps</h1>",
            '<p class="lede">The calendar\'s placed entries on a map: Vietnam, Laos and Cambodia on one, China on the '
            'other. Each map stands also in the calendar\'s pages, under the day of the page\'s first entry placed on '
            'it, and at the head of its threads\' pages.</p>',
            '<ol class="e lists">' + "".join(listing(m) for m in ms) + "</ol>"]
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", "Maps").replace("{{main}}", "\n".join(main))
    return pg.replace("</head>", CSS + "\n</head>", 1)
