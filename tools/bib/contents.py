"""The contents at the head of each calendar page, and the register of the tables and maps the calendar carries.

    put(page, eid, blk, kind, key)   every inject that sets a table or map in a calendar entry calls it: it puts the
                                     block at the end of the entry's <li> and, for a kind KINDS lists, an anchor before
                                     it ("tb-<kind>-<key>"), labelled for the contents and the thread statements
    KINDS                            kind -> its label from the tag's value ("election": "1960" -> "Election of Nov. 8,
                                     1960"), or None for a kind the contents leave out (special, primary)
    nav(lst, sections, half)         the contents of a calendar page: the threads, the month grid (the whole calendar's
                                     where it is in parts), a slot for the tables
    day_mark(kind, key, iso, threads)   the anchor of a block set under a date, not in an entry (tools/bib/dayblocks.py:
                                     the Southeast Asia table and map, Armed Forces Day): it names the day and the threads in place of an
                                     entry, and finish() lists it as it lists an entry's
    finish(page, lst, half, defer)   after every inject: the tables and maps listed in their threads' statements and in
                                     the contents (the page's own; in the reader, the whole calendar's, in its Cal.
                                     block); with defer, recorded (FOUND) for fill()
    fill(page, lst, half)            once every part is built: the whole calendar's tables and maps in a part's
                                     contents, or the index's (half 0), each linked to its page

A new table or map type registers itself: it adds its kind to KINDS (put refuses a kind not there) and sets its blocks
with put, and the contents and the thread index list it with no more code (the owner's rule, Oct. 21, 2026).

STYLE (the owner's rules, Oct. 21, 2026):
 1. The months in a grid: a year cell spanning the year's rows, then six months a row, Jan to Jun and Jul to Dec, each
    month its three-letter form ("Sep", not "Sept.": here only; the Bluebook's forms elsewhere), linked to its section,
    the section's own title on hover. A month the page does not hold leaves its cell empty and the columns stand. A year
    takes only the rows it has months in (1969: one row; 1972, Mar.-Aug.: two). A year not following the one before
    (1969, then the primary seasons of 1972) takes a little space above. January 1966 is two sections (196601, Jan. 1-9;
    196601b, from the session's opening), one cell: the first's. The threads section keeps its place, first,
    a line of its own in the contents' type.
 2. After the grid, under "Tables and maps", every table and map on the page in the order it first appears there, each
    linked to its anchor, by its label ("Election of Nov. 8, 1960"), one a line, grouped by year in the grid's year
    column: a page holds twenty to forty, too many for a run, and the year column, already the grid's, finds them by
    year. Not the one-off elections (a special, a single primary day) nor the month's indicators: they are under every
    month or nearly, and the grid finds them.
 3. One table: the grid and the tables share the year column, so the two align; the table at most 27rem wide, 16% of
    it the year, 14% each month; at 400px it fits (main's 1.25rem and 2.6rem gutters leave 338px). The Outline drawer
    shows the same, cloned from the contents (templates/list.html), the month being read marked as before.
 4. A thread's statement in the index lists the tables and maps carried by its entries on the page (its own entries
    and its subthreads'), in order of appearance, in a muted line at the statement's foot, set right as the See also
    line is and above it (See also stays last): "*Tables and maps* Election of Nov. 8, 1960 · Governors, Nov. 8, 1960",
    the label in italics, a middle dot between, each linked to its anchor; in the sans at the See also line's size, in
    regular weight and muted, so the two read as one footing. In the reader, each part's index lists its part's.
 5. A listed table or map takes its label as its title (the owner's request, Oct. 23, 2026: "a distinct title style to
    visually demarcate them from the calendar day entries"): centered, in the sans's small capitals, a little smaller
    than the type, as the Executive roster's parts are ("ELECTIONS OF NOV. 8, 1960"); so the labels stay brief. One
    title only (the owner, Nov. 4, 2026: "Remove doubled titles ... keep the small caps title alone"): the block's own
    first heading goes (DROP_HEAD, HEAD: the opening, the governors, the legislatures, the primaries, the conventions'
    delegations, the budget, the debt limit acts, State finance, the appropriations, world oil; the Executive's and the
    roll calls' their modules leave out in the calendar, Armed Forces Day's caption too). A day block (day_mark) takes
    its title the same way, but the Southeast Asia table, whose own caption, in the indicators' style, is its title
    (tools/bib/wartable.py, STYLE 2): day_mark(titled=False). A title ending in a bare year takes no comma before it;
    one ending in a month and year, or a day, keeps it ("only bare years drop the comma", the owner, Nov. 4, 2026: "Democratic primaries 1960", "Armed forces
    1962", "Southeast Asia 1966"; but "Southeast Asia, Sept. 1966", "Executive Branch, Jan. 20, 1957", "State finance,
    fiscal 1960"); a bill's course is its act's name alone. The day of a November
    election is one block, "Elections of Nov. 8, 1960" (congress.election_day): "Presidential electors", "Congress",
    "State elections" (governors, legislatures) under it in the blocks' bold subheadings; the governors' and the
    legislatures' own entries point to their parts ("The table: ...", kind "see", unlisted).
 6. The whole calendar on every page (the owner, Oct. 30, 2026: "The 'list' should include link-throughs to the
    months, headings, and tables on the individual calendar pages"; volume.md, section 3): each year's page, and the
    index, carry every part's months in the grid, each linked through to its place on its year's page (calsplit.href;
    the reader, in its block). The tables and maps: a year's page lists its own only, the index every part's (the
    owner, Nov. 4, 2026: "Drop other-year tables from the year-calendar view"). Another part's year in the year column is
    a link to its page's top, muted; the page's own, in the text's color, unlinked. The threads line is the page's
    own threads (the index's: its list of threads).
"""
import calendar
import html
import re

from . import calsplit, store

MON3 = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
FULL = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
        "November", "December"]
PARTY = {"R": "Republican", "D": "Democratic"}
SLOT = "<!--tb-contents-->"


def esc(t):
    return html.escape(str(t), quote=True)


def fmt(d):
    y, m, dd = str(d)[:10].split("-")
    return f"{MONTHS[int(m) - 1]} {int(dd)}, {y}"


def ordinal(n):
    n = int(n)
    return f"{n}{'th' if 11 <= n % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


# ---------------------------------------------------------------- the register

def _election(key):
    from . import elections
    d = (elections.load().get(int(key)) or {}).get("date")
    return f"Elections of {fmt(d)}" if d else f"Elections of {key}"


def _approp(key):
    from . import appropriations
    return appropriations.label(key)


def _bill(key):
    from . import bills
    b = bills.load().get(key) or {}
    return b.get("title", key)


def _rollcall(key):
    from . import conventions
    y, p, ballot = key.split("-", 2)
    B = ((conventions.load().get(f"{y}-{p}") or {}).get("ballots") or {}).get(ballot) or {}
    office = {"President": "presidential", "Vice President": "vice-presidential"}.get(B.get("office"), ballot)
    n = re.sub(r"\D", "", ballot)
    more = f", ballot {n}" if n and n != "1" else ""
    return f"Roll call: {PARTY.get(p, p)} {office} nomination {y}{more}"


def _mon_year(key):
    """'1966-01' -> 'Jan. 1966'."""
    return f"{MONTHS[int(key[5:7]) - 1]} {key[:4]}" if re.match(r"^\d{4}-\d\d$", key) else key


KINDS = {
    "executive": lambda k: f"Executive Branch, {fmt(k)}",                       # executive.py
    "congress": lambda k: f"{ordinal(k)} Congress at its opening",              # congress.py
    "committees": lambda k: f"Leaders and committees, {ordinal(k)} Congress",   # committee_rosters.py via congress.py
    "election": _election,                     # congress.election_day: the electors, Congress, the State elections
    "governors": lambda k: f"Governors, {fmt(k)}",                              # governors.py
    "legislatures": lambda k: f"State legislatures {k}",                        # legislatures.py
    "statefin": lambda k: f"State finance, fiscal {k}",                         # statefin.py
    "budget": lambda k: f"Budget, fiscal {k}",                                  # budgets.py
    "debt-limits": lambda k: "Debt limit acts",                                 # budgets.py
    "bill": _bill,                                                             # bills.py
    "appropriations": _approp,                                                 # appropriations.py
    "primaries": lambda k: f"{PARTY.get(k[-1], k[-1])} primaries {k[:4]}",      # primaries.py
    "conventions": lambda k: f"{PARTY.get(k[-1], k[-1])} convention, {k[:4]}: delegations",   # conventions.py
    "rollcall": _rollcall,                                                     # conventions.py
    "vnmap": lambda k: f"Southeast Asia {k}",                                   # vnmap.py
    "war": lambda k: f"Southeast Asia, {_mon_year(k)}",                         # wartable.py via dayblocks.py
    "forces": lambda k: f"Armed forces {k}",                                    # afday.py via dayblocks.py
    "oilworld": lambda k: f"World oil {k}",                                     # oilworld.py
    "oilprice": lambda k: "Posted prices of crude oil",                         # oilworld.py
    "special": None,                                                           # specials.py: one-off races
    "primary": None,                                                           # primaries.py: one primary day
    "see": None,                                         # a pointer to a table set in another entry (governors.py)
}


def label(kind, key):
    """The block's label, or None for a kind the contents leave out; a kind not registered is an error."""
    if kind not in KINDS:
        raise KeyError(f"contents.KINDS: no kind {kind!r}: register it before putting its blocks")
    f = KINDS[kind]
    return f(str(key)) if f else None


def anchor_id(kind, key):
    return "tb-" + re.sub(r"[^A-Za-z0-9-]+", "-", f"{kind}-{key}").strip("-")


LI = re.compile(r"<li\b|</li>")


def put(page, eid, blk, kind, key, nav=None):
    """The block at the end of the calendar entry eid's <li> (its own </li>, nested lists counted), with its anchor
    where the kind is listed: (page, 1), or (page, 0) where the page has no such entry. nav: the title's chevrons to
    the same kind's blocks before and after, ((href, hover) or None, (href, hover) or None) (indicators STYLE 18)."""
    lab = label(kind, key)
    m = re.search(r'<li id="' + re.escape(eid) + r'"[^>]*>', page)
    if not m or not blk:
        return page, 0
    depth, at = 0, None
    for t in LI.finditer(page, m.start()):
        depth += 1 if t.group() != "</li>" else -1
        if depth == 0:
            at = t.start()
            break
    if at is None:
        return page, 0
    if lab:
        if kind in DROP_HEAD:                   # STYLE 5: the title stands in the block's own heading's place
            blk = HEAD.sub(r"\1", blk, count=1)
        blk = (f'<span class="tba" id="{esc(anchor_id(kind, key))}" data-tb="{esc(lab)}" data-tbe="{esc(eid)}"></span>'
               + title(lab, nav) + blk)
    return page[:at] + blk + page[at:], 1


DROP_HEAD = {"congress", "governors", "legislatures", "primaries", "conventions", "budget", "debt-limits", "statefin",
             "appropriations", "oilworld"}
HEAD = re.compile(r'^((?:\s*<div[^>]*>)+)\s*<p class="(?:cgh|bgh|sfh|aph|owh)">.*?</p>', re.S)   # the block's heading


def title(lab, nav=None):
    """A listed table's title (STYLE 5): its label, centered, in small capitals; with nav, between 〈〈 and 〉〉."""
    if nav:
        from .indicators import caption
        return caption(lab, *nav, cls="tbt")
    return f'<p class="tbt">{esc(lab)}</p>'



def day_mark(kind, key, iso, threads, titled=True, nav=None):
    """The anchor of a day block (tools/bib/dayblocks.py): set before a block that stands under a date, not in an entry.
    It carries the day and the block's threads in place of an entry's id ("day:<iso>:<thread>,<thread>"), so finish()
    lists it in the contents and the threads' statements as it lists an entry's tables. titled: the small-capital title
    after it (not for the Southeast Asia table, whose caption is its title: STYLE 5); nav: its 〈〈 〉〉, as put's."""
    lab = label(kind, key)
    if not lab:
        return ""
    return (f'<span class="tba" id="{esc(anchor_id(kind, key))}" data-tb="{esc(lab)}" '
            f'data-tbe="{esc("day:" + iso + ":" + ",".join(threads))}"></span>' + (title(lab, nav) if titled else ""))


# ---------------------------------------------------------------- the contents

def _month(sec):
    m = re.match(r"^(\d{4})(\d\d)b?$", str(sec.id))
    return (int(m.group(1)), int(m.group(2))) if m else None


def _title(sec, y, mo):
    a, b = str(sec.extra.get("from") or ""), str(sec.extra.get("to") or "")
    last = calendar.monthrange(y, mo)[1]
    if a[:7] == b[:7] == f"{y}-{mo:02d}" and (int(a[8:10]) != 1 or int(b[8:10]) != last):
        return f"{FULL[mo - 1]} {int(a[8:10])}–{int(b[8:10])}, {y}"
    return plain_title(sec)


def plain_title(sec):
    from .markup import plain
    return plain(sec.title)


def nav(lst, sections, half=None):
    """The calendar page's contents (STYLE 1, 3, 6): the threads line, the grid, the slot finish() or fill() fills. Where
    the calendar is in parts, the grid is the whole calendar's: every month of every part, linked through to its page
    (half: the page's part; 0, the index)."""
    lines, years = [], {}
    whole = calsplit.cfg(lst) and half is not None
    series = calsplit.CUR["mode"] == "series"
    for s in sections:
        if not _month(s):
            sid = f"{lst.key}--{s.id}" if series else s.id
            lines.append(f'<li><a href="#{esc(sid)}" data-id="{esc(sid)}">{esc(plain_title(s))}</a></li>')
    for s in (lst.sections if whole else sections):
        ym = _month(s)
        if ym:
            years.setdefault(ym[0], {}).setdefault(ym[1], s)      # 196601 and 196601b: the cell the first's
    rows, prev = [], None
    for y in sorted(years):
        ms = years[y]
        part = calsplit.half_of_section(lst, ms[min(ms)]) if whole else half
        halves = [h for h in (0, 1) if any(h * 6 + k in ms for k in range(1, 7))]
        trs = []
        for j, h in enumerate(halves):
            cells = []
            for k in range(1, 7):
                mo = h * 6 + k
                s = ms.get(mo)
                cells.append(f'<td><a href="{esc(_sec_href(lst, s, whole))}" data-id="{esc(_sec_id(lst, s))}" '
                             f'title="{esc(_title(s, y, mo))}">{MON3[mo - 1]}</a></td>' if s else "<td></td>")
            yc = str(y)
            if whole and part != half:          # another part's year: its page's top (STYLE 6)
                key = calsplit.page_key(lst, part)
                yc = f'<a href="{esc(f"#{key}--top" if series else f"{key}.html")}">{y}</a>'
            th = f'<th scope="rowgroup" rowspan="{len(halves)}">{yc}</th>' if j == 0 else ""
            trs.append(f"<tr>{th}{''.join(cells)}</tr>")
        gap = ' class="gap"' if prev is not None and y != prev + 1 else ""
        here = ' data-here="1"' if whole and part == half else ""
        rows.append(f"<tbody{gap}{here}>{''.join(trs)}</tbody>")
        prev = y
    grid = (f'<table class="tocg" aria-label="Months"><colgroup><col class="y">{"<col>" * 6}</colgroup>'
            f'{"".join(rows)}{SLOT}</table>') if rows else SLOT
    return ('<nav class="toc" aria-label="Contents">\n<h3 id="contents" style="border-top:0;margin-top:1.5rem" '
            'data-short="Contents">Contents</h3>\n<div id="tocCal" class="tocc">'
            f'<ol class="tocl">{"".join(lines)}</ol>{grid}</div>\n</nav>')


def _sec_id(lst, s):
    return f"{lst.key}--{s.id}" if calsplit.CUR["mode"] == "series" else s.id


def _sec_href(lst, s, whole):
    """A month's link: on the page, or through to its part's page (the reader: its block's section)."""
    if calsplit.CUR["mode"] == "series" or not whole:
        return "#" + _sec_id(lst, s)
    return calsplit.href(lst, calsplit.half_of_section(lst, s), s.id)


MARK = re.compile(r'<span class="tba" id="([^"]+)" data-tb="([^"]*)" data-tbe="([^"]+)"></span>')
THREAD_SLOT = re.compile(r"<!--tb:(\d+):([^>]*?)-->")


def thread_slot(lst, slug):
    """The placeholder at a thread statement's foot (entry_html in build.py), filled by finish()."""
    return f"<!--tb:{calsplit.CUR['half'] or 1}:{slug}-->"


FOUND = {}       # part -> [(anchor, label, date)]: each part page's tables and maps, for the whole calendar's list


def finish(page, lst, half=None, defer=False):
    """The tables and maps on the page, listed in their threads' statements and in the contents: the page's own; with
    defer (a calendar in parts), recorded for fill(), which lists the whole calendar's once every part is built."""
    from .build import entry_threads
    ents = {e["id"]: e for _, e in lst.entries()}
    found = []                                  # (anchor, label, entry), in order of appearance
    for m in MARK.finditer(page):
        eid = html.unescape(m.group(3))
        e = ents.get(eid)
        if e is None and eid.startswith("day:"):    # a day block's anchor (day_mark): its day and threads
            _, iso, ts = eid.split(":", 2)
            ts = [t for t in ts.split(",") if t and t in lst.threads()]
            e = {"id": eid, "date": iso, "thread": ts[0], "also": ts[1:]} if ts else None
        if e is not None:
            found.append((m.group(1), html.unescape(m.group(2)), e))
    if defer:
        FOUND[half] = [(aid, lab, str(e.get("date") or "")) for aid, lab, e in found]
    elif SLOT in page:
        page = page.replace(SLOT, _list([("#" + aid, lab, str(e.get("date") or "")) for aid, lab, e in found]), 1)
        page = style(page)
    by = {}
    for aid, lab, e in found:
        h = calsplit.half_of_date(lst, e.get("date") or "")
        for t in entry_threads(lst, e):
            by.setdefault((h, t), []).append((aid, lab))

    def sub(m):
        got = by.get((int(m.group(1)), m.group(2)))
        if not got:
            return ""
        links = " · ".join(f'<a href="#{aid}">{esc(lab)}</a>' for aid, lab in got)
        return f'<span class="ttb"><i>Tables and maps</i> {links}</span>'
    page = THREAD_SLOT.sub(sub, page)
    if found and 'id="ttbstyle"' not in page:
        page = page.replace("</head>", TSTYLE + "\n</head>", 1)
    return page


def fill(page, lst, half):
    """A part's page (half; 0, the index) once every part is built: its own tables and maps in its contents, the
    index the whole calendar's (STYLE 6), each linked to its anchor on its page."""
    if SLOT not in page:
        return page
    items = []
    for h in sorted(FOUND):
        if half and h != half:                  # a year's page: its own tables and maps only (STYLE 6)
            continue
        for aid, lab, d in FOUND[h]:
            items.append((calsplit.href(lst, h, aid), lab, d))
    return style(page.replace(SLOT, _list(items), 1))


def style(page):
    return page if 'id="tocstyle"' in page else page.replace("</head>", STYLE + "\n</head>", 1)


def _list(found):
    """The tables and maps (href, label, date), grouped by year (STYLE 2)."""
    if not found:
        return ""
    years = {}
    for href, lab, d in found:
        years.setdefault(d[:4], []).append((href, lab))
    out = ['<tbody class="tbh"><tr><td></td><td colspan="6">Tables and maps</td></tr></tbody>']
    for y, items in years.items():
        trs = []
        for j, (href, lab) in enumerate(items):
            th = f'<th scope="rowgroup" rowspan="{len(items)}">{esc(y)}</th>' if j == 0 else ""
            trs.append(f'<tr>{th}<td colspan="6" class="tbi"><a href="{esc(href)}">{esc(lab)}</a></td></tr>')
        out.append(f'<tbody class="tbs">{"".join(trs)}</tbody>')
    return "".join(out)


def problems(series):
    """Every tagged block has a label: a tag whose kind is registered and whose value the label cannot read."""
    out = []
    pat = re.compile(r"^(" + "|".join(re.escape(k) for k, f in KINDS.items() if f) + r"):(.+)$")
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for _, e in lst.entries():
            for t in e.get("tags") or []:
                m = pat.match(str(t))
                if not m:
                    continue
                try:
                    label(m.group(1), m.group(2))
                except Exception as x:          # noqa: BLE001: any failure is the tag's
                    out.append((e["id"], f"{t}: no label for the contents ({x})"))
    return out


STYLE = """<style id="tocstyle">
/* the calendar's contents: the threads, the month grid, the tables and maps (tools/bib/contents.py, STYLE) */
.tocc{font-family:var(--sans)}
.tocc ol.tocl{list-style:none;padding:0;margin:.9rem 0 .45rem}
.tocc ol.tocl a{font-weight:700;font-size:1rem}
table.tocg{border-collapse:collapse;table-layout:fixed;width:min(100%,27rem);margin:0;font-size:.95rem;line-height:1.3;border:0;background:none}
table.tocg col.y{width:16%}
table.tocg th,table.tocg td{border:0;background:none;padding:.2rem 0;text-align:left;vertical-align:top}
table.tocg th{font-weight:700;color:var(--ink);font-size:.95rem}
.tocc table.tocg th a{color:var(--muted)}
table.tocg tbody.gap>tr:first-child>*{padding-top:.75rem}
table.tocg tbody.tbh td{padding-top:1.1rem;font-weight:700;font-size:1rem}
table.tocg tbody.tbs>tr:first-child>*{padding-top:.45rem}
table.tocg td.tbi{font-size:.9rem;padding:.1rem 0;line-height:1.35}
.tocc a{text-decoration:none;color:var(--ink)}
.tocc a:hover{color:var(--accent);text-decoration:underline}
#drawer .tocc a.cur{padding:0 .15rem}
</style>"""

TSTYLE = """<style id="ttbstyle">
/* a thread statement's tables and maps (tools/bib/contents.py, STYLE 4) */
.ttb{display:block;text-align:right;font-family:var(--sans);font-size:.92rem;color:var(--muted);margin-top:.2rem}
.ttb a{color:inherit;text-decoration-color:var(--rule)}
.tba{display:block;height:0}
.tbt{text-align:center;font-family:var(--sans);font-size:1rem;font-weight:600;font-variant-caps:all-small-caps;
  letter-spacing:.06em;margin:1.4rem 0 .3rem;color:var(--ink)}
.tbt a.tnb,.tbt a.tnb:hover{color:var(--muted);text-decoration:none}
.eday>p.cgh{font-family:var(--sans);font-weight:700;font-size:.95rem;margin:1.2rem 0 .4rem}
.cg .cgh.sub{font-weight:600;font-style:italic}
.tbp{font-family:var(--sans);font-size:.92rem;color:var(--muted);margin:.3rem 0}
.tbp a{color:inherit;text-decoration-color:var(--rule)}
</style>"""
