"""The calendar by year: one list in the data (lists/cal/), a page a half-year in the build (cal1960a.html, Jan. 6-June
30, 1960, cal1960b.html, July 1-Dec. 31, ... cal1969.html, Jan. 1-20, 1969; the year pages of Nov. 4, 2026 split in
halves Nov. 12, past the 8 MB of the memo, `retired_parts`, their pages forwarding old links), a page for the primary seasons of 1972 and 1976 (calprimaries.html), and the
index, cal.html (the owner's memo, Nov. 4, 2026: notes/extensions/memos/volume.md, section 3).

    lists/cal/list.yaml, `split:`   a part a page: its `page`, the date it begins (`from`; the first, the calendar's
                                    first day), and its abbr ("Cal. 1961"), `called` (the words other parts' ledes name it
                                    by: "the calendar of 1961"), title, span, page_title, h1, lede and logic
    the list's own page_title, h1, lede, index_logic   the index's; its `logic` shows on the index and on every part's
                                    page, before the part's own
    `legacy_parts`                  the three parts of Oct. 17, 2026 (cal, cal63, cal66): their pages forward old links
                                    (STYLE 14), and a thread not yet converted keeps its c, c2, c3 by them (STYLE 12)

The threads section (`th`) is in every part: each part's thread index lists only the threads with entries in it, each
with its statement for that part (STYLE 12) and its dates there. Everything else goes by date: a dated section to the
part its first day falls in (January 1966's two sections, 196601 and 196601b, both in 1966). A part runs from its
`from` (the first, from the calendar's first day) to the last day of its last dated section (`part_range`; 1969 to
Jan. 20, the primaries to Aug. 31, 1976), for any number of parts. The parts are a list of dates: a busy year that grows
past some 8 MB splits again by the same line (the memo).

STYLE:
 1. A thread's dates by year, as every list of calendar dates is written (tools/bib/datelist.py, its STYLE):
    ("1961 Jan. 23, Feb. 20. 1962 ..."), each date linked to its entry.
 2. Across the seams, muted, linked: after its dates, the year of the thread's next entry in a later part, linked to
    the thread's entry in that part's index, and that entry's date, linked to the entry (". 1963 Jan. 14."); the year
    not underlined; before its dates, the year and date of the thread's last entry in an earlier part, linked the same
    way ("1962 Dec. 11. 1963 ...").
 3. A part's thread entries take the anchor <page>.thread.<slug> (cal1961.thread.cuba), so that every part's index can
    stand in the reader's one page; a rubric links to its own part's index. The section that holds them takes th-<page>
    (th-cal1961); the index's list of threads, th, its lines cal.thread.<slug>.
 4. At each seam, muted, in sans: at the head of a part's first day, "‹ Dec. 31, 1960, in Cal. 1960"; at the foot of
    the part before's last, "Jan. 1, 1961, in Cal. 1961 ›", by the parts' abbr and their dated sections' first and last
    days (seam: 1969's last, Jan. 20, and the primaries' first, Mar. 1, 1972).
 5. On a part's page a link to an anchor that lives in another part goes to that page; on every other page, a link to
    any part's page, to the index or to an old part's page (cal.html#X, cal63.html#X) goes to the page that holds X
    (route): by the data's anchors (entries, days, sections and their old ids), and, in a build that has built the
    calendar, by every id each part's page holds alone (REAL: the tables', the servants', the blocks').
 7. A thread highlighted: a tap on a thread's entry in the index, or on a thread's line under a calendar entry ("⟨⟨ Testing
    ⟩⟩"), anywhere but on a link, sets that thread's entries, and its entry in the index, on
    white (in the dark theme, a lighter panel): the entry's own box, square, from its rule to the next, and an en dash (.515em of the serif)
    past the rules' ends on either side, into the margin (side shadows of the fill); nothing moves and no edge crosses
    text. A day's first entry, which has no rule above
    it, and its last, none below, take one while lit, drawn inside the box; the same tap again clears it, a tap on another thread moves it. The
    links (⟨⟨ and ⟩⟩) go where they go and leave the highlight as it is. A rubric's thread name, a link to the thread's
    entry in the index, goes there and lights the thread too; it never clears it. It holds across the parts and
    the reader for the session (sessionStorage), and is the reader's alone: nothing in the address. While a thread is
    lit, the left and right arrow keys go to its entry before and after the one at the top of the screen (the owner,
    Nov. 5, 2026): that entry's ⟨⟨ or ⟩⟩ followed, so the thread's own order and across the parts; where no lit entry
    is at the top, the nearest above or below it in the thread's order. Not with a modifier, nor in a field, a map or a chart.
 6. Each part's lede names the year before and the year after by their `called` words ("The calendar of 1960 precedes
    it; the calendar of 1962 follows; every year in the calendar's index"), each linked to its page's top, or its
    block's in the reader, and "the calendar's index" to the index (other_link).
 8. While a thread is lit, a mark for each of its lit entries, as a find-on-page bar marks its hits: no edge, no bar
    behind, the thumb's width, in the thumb's column, right of the headings. Amber (--hlmark, as Chrome marks its finds)
    while the scroll wheel is held and its headings show, and for the 1.5 s they stay after it is let go (LINGER in the
    templates); then white (--hl, the lit entries' own fill), until the thread is cleared. The thumb's travel stands for
    the page: a mark's place and height are the entry's place and height as shares of the page, and at least 3px
    (--hlmin), fattened about the entry's middle, so the thumb's centre on a mark brings the entry to the top, and the
    marks hold still while the page scrolls. A click on a mark (or within 6px of it), not on the thumb, brings its
    entry to the top. Two canvases, the amber over the white, faded in and out with the headings; drawn when the
    thread or the headings change or the page changes size, never on scroll (canvas.hlm, SCRIPT; --hlhalo, --hlhalow,
    a band behind each mark, unset).
 9. A ghost subthread (a `parent:` and no statement) has a line in the index, in its place under its parent: its full
    name ("Vietnam: Pennsylvania"), muted, as the A–Z bibliography's ghost entries are, not underlined, linked to its
    first entry in the part; then its dates there, by year (1, 2), as any thread's are, links and all (the owner's
    ruling, Oct. 21, 2026: the name muted, not the links); no line in a part where it has no entries. A rubric naming
    it links to that line, and a tap on it lights the ghost's entries (7). Given a statement, it is a thread's entry
    like any other (`ghost_thread_html` in build.py). Its line stands in a part where it, or a ghost under it, has
    entries; its dates are its own (15).
10. A thread's old name stays in the index where the reader may look for it: a th.yaml entry with `s:` the old name
    and `see:` the thread's slug ("Desegregation: schools", see desegregation-schools), in its alphabetical place,
    muted and not underlined, the whole of it a link to the thread's entry in the part; nothing else, and no line in
    a part where the thread has none (`redirect_thread_html` in build.py). No entry takes it as a thread. The line
    names the thread it now goes by, the whole of it muted: "Desegregation: schools: School desegregation" (the name
    alone where the two are the same: "Special elections", whose thread sorts as "Elections, special" by its hidden
    `sort:`). Where the old name went to several threads (`see:` a list), the old name in the text's color, then each
    thread muted and linked, a middle dot between: "Legislatures: Districting and apportionment · State legislatures"
    (the owner's ruling, Oct. 21, 2026). Only the threads with entries in the part.
11. A thread statement may end in a See also line (`see_also:` in th.yaml, a list of slugs): set right, at the foot of
    the thread's entry in the index, in the thread names' type (the sans, bold), "See also" in italics, the threads
    in roman, a middle dot between, each linked to its entry in the part ("*See also* Goldwater", under 1964
    Elections); a thread with no entries in the part is left out, the line too where none has. Not for a thread's own
    parent or subthreads, nor its alphabetical neighbors (Cuba, Cuban Missile Crisis), which the index already sets
    together: for related matter elsewhere in the index (the owner's rule, Oct. 21, 2026; `see_also_html` in
    build.py).
12. A thread's statement is written once (`c`) and chosen for each part by its range (`part_range`): the scope, the
    span-tagged sentences whose spans meet the range, the names of the thread's events that fall in it
    (tools/bib/statements.py, its STYLE; notes/extensions/memos/volume.md, §4). A thread not yet converted keeps a
    statement a part (`c2`, `c3`: its own where the thread begins in an earlier part, else the latest before it; `c`
    in the part it begins in) until tools/statements/apply.py writes its one `c` (`statement`).
13. The index, cal.html (the list's own page; `index_page`): the list's h1, lede and logic and its `index_logic`; the
    whole calendar's contents (contents.py, STYLE 6); then the threads, alphabetical as th.yaml keeps them, each its
    name linked to its entry in the first part's index it has entries in, then the years it has entries in, each
    linked to the thread in that year's index (a ghost's name muted; an old name left out); each line anchored
    cal.thread.<slug>. In the reader, the Cal. block, before the years'. No thread statements here: each year's index
    has its own (12). The primary seasons of 1972 and 1976 are one part: they hold only the primaries and the
    conventions' openings, a few dozen entries; a part a season when those years are written.
14. Old links. Every page of this series is routed at build (5). A link from outside to the index or to an old part's
    page (cal63.html, cal66.html: a line to the index and a script) goes to the page that holds its anchor, by a script
    (forward_script): the anchor's form names its page where it holds one (cal1961.thread.cuba, th-cal1961,
    ind-cal1961-cpi), else its year (cal.1961-04-15.cuba, d1961-04-15, 196104); a map the build writes (forward) gives
    the rest: an entry whose date has left its id's year, a section's old id (apr60), a table's anchor (tb-...), and
    the old parts' own (cal63.thread.cuba, th2, ind-cal63-cpi: the first year over the old part's span that holds the
    like). On the index an anchor it holds stays; one nothing places, there too; an old part's page without one goes
    to the index.
15. The index's dates are a thread's own entries (the owner's memo, Nov. 4, 2026: volume.md, section 2): those whose
    `thread:` names it, or whose `also:` does. An entry filed under a subthread is dated on the subthread's line, a
    ghost's included (9), not on its parent's, unless `also:` lists it in the parent too (`index_members` in build.py).
    So every entry is dated, in plain text, on one line at least: its own thread's. A parent keeps its line, its
    statement and its seam links (2: to its own entries) in a part where only its subthreads have entries; its
    statement names its ghosts' events as before (statements.py, STYLE 3). The family stays together everywhere else:
    the thread-nav line under each entry, the highlight (7), the statements, `entry_threads`, `thread_members`. On the
    index (13) a thread's years stay its family's: each links to the thread's entry in that year's index, which stands
    while the family has entries there.
16. A date in a thread's run the same as the one before it ("July 31, July 31") is left out, for now (the owner, Nov.
    5, 2026): the run shows each label once, linked to its first entry ("Aug. 27, Aug. 27–28" keeps both). The
    same-day entries may come back with labels of their own (a time, a place) after the time-label pass.
"""
import datetime
import re

from . import datelist, store

# the part being built (0, the index) and the page kind, set by the build around each part
CUR = {"half": None, "mode": "list"}


def parts(lst):
    """The calendar's parts, in order: [{page, from, abbr, title, span, called, page_title, h1, lede, logic}]; the
    first's page its own `page` (cal1960), else the list's (list.yaml `split:`: each item a part, every one but the first
    with its `from`). One part where the list has no split."""
    s = (lst.data or {}).get("split") if lst is not None else None
    if not s:
        return [{"page": lst.key if lst is not None else None, "from": None}]
    first = dict(s[0], **{"from": None})
    first.setdefault("page", lst.key)
    return [first] + [dict(x) for x in s[1:]]


def index_page(lst):
    """The list's own page (cal) where it is the calendar's index (STYLE 13): the first part has a page of its own."""
    p = cfg(lst)
    return lst.key if p and p[0]["page"] != lst.key else None


def cfg(lst):
    """The parts where the calendar has more than one, else None."""
    p = parts(lst) if lst is not None else None
    return p if p and len(p) > 1 else None


def page_key(lst, half):
    return parts(lst)[half - 1]["page"]


def half_of_date(lst, d):
    """The part a date falls in (1, 2, 3 ...): the last whose first day is on or before it. A month-only date ('1963-01')
    is its month's first day, a year its first: as text, '1963-01' sorts before '1963-01-01'."""
    s = str(d)[:10]
    s += {4: "-01-01", 7: "-01"}.get(len(s), "")
    n = 1
    for i, p in enumerate(parts(lst)[1:], start=2):
        if s >= str(p["from"]):
            n = i
    return n


def half_of_section(lst, sec):
    """The part a top section falls in by its first day; None for the threads section, which is in every part."""
    if sec.id == lst.data.get("threads_section", "th"):
        return None
    top = sec
    while top.parent is not None:
        top = top.parent
    d = top.extra.get("from")
    if not d:
        return 1
    return half_of_date(lst, d)


def sections(lst, half):
    """The list's top sections in the part, the threads section first."""
    return [s for s in lst.sections if half_of_section(lst, s) in (None, half)]


def half_of_entry(lst, sec, e):
    h = half_of_section(lst, sec)
    if h is None:
        return CUR["half"] or 1
    return h


def thread_anchor(lst, slug, half):
    """A thread's entry in a part's index: <page>.thread.<slug> (cal1961.thread.cuba; STYLE 3)."""
    return f"{page_key(lst, half or 1)}.thread.{slug}"


def href(lst, half, anchor):
    """A link to an anchor in a part: in the page itself, or the other page; in the reader always in the page."""
    if CUR["mode"] == "series" or half == CUR["half"]:
        return f"#{anchor}"
    return f"{page_key(lst, half)}.html#{anchor}"


_BOUNDS = {}


def bounds(lst):
    """The calendar's first and last days (dates): its dated top sections' first `from` and last `to`."""
    if id(lst) not in _BOUNDS:
        los = [str(s.extra["from"]) for s in lst.sections if s.extra.get("from")]
        his = [str(s.extra["to"]) for s in lst.sections if s.extra.get("to")]
        _BOUNDS[id(lst)] = (datetime.date.fromisoformat(min(los)), datetime.date.fromisoformat(max(his)))
    return _BOUNDS[id(lst)]


def part_range(lst, half):
    """A part's first and last days (dates): its `from`, or the calendar's first day; the last day of its last dated
    section (1969's ends Jan. 20, not the day before the primaries of 1972). Any number of parts; half None (or no
    split), the whole calendar."""
    lo, hi = bounds(lst)
    ps = parts(lst)
    if not half or len(ps) < 2:
        return lo, hi
    key = (id(lst), half)
    if key not in _RANGE:
        a = datetime.date.fromisoformat(str(ps[half - 1]["from"])) if half > 1 else lo
        tos = [str(s.extra["to"]) for s in lst.sections if s.extra.get("to") and half_of_section(lst, s) == half]
        if tos:
            b = datetime.date.fromisoformat(max(tos))
        elif half < len(ps):
            b = datetime.date.fromisoformat(str(ps[half]["from"])) - datetime.timedelta(days=1)
        else:
            b = hi
        _RANGE[key] = (a, b)
    return _RANGE[key]


_RANGE = {}


def legacy_part(lst, d):
    """The part of the three of Oct. 17, 2026 (cal, cal63, cal66; list.yaml `legacy_parts`) a date fell in: 1, 2, 3.
    A thread not yet converted keeps its statements by them (c, c2, c3; STYLE 12)."""
    s = str(d)[:10]
    s += {4: "-01-01", 7: "-01"}.get(len(s), "")
    n = 1
    for i, p in enumerate(((lst.data or {}).get("legacy_parts") or [])[1:], start=2):
        if s >= str(p["from"]):
            n = i
    return n


def statement(lst, e, half, first, members=None):
    """The thread's statement in a part (STYLE 12): written once, `c`, its spans and events chosen by the part's range
    (tools/bib/statements.py). A thread not yet converted (c2, c3) keeps a statement for each of the three parts of
    Oct. 17, 2026: its own where the thread begins in an earlier one; else the latest before it; c in the one the thread
    begins in. Those parts are reckoned by date (`legacy_part`): the thread's last entry in this part, else the part's
    last day; its first entry anywhere, else the first day of the part `first`."""
    from . import statements
    if not statements.legacy(e):
        lo, hi = part_range(lst, half if cfg(lst) else None)
        return statements.render(lst, e, lo, hi)
    if not half or not cfg(lst):
        return e.get("c")
    lo, hi = part_range(lst, half)
    ds = sorted(str(m["date"]) for m in members or [])
    here = [d for d in ds if lo <= statements.day(d) <= hi]
    now = legacy_part(lst, here[-1] if here else hi.isoformat())
    begins = legacy_part(lst, ds[0] if ds else part_range(lst, first or 1)[0].isoformat())
    for n in range(now, begins, -1):
        if e.get(f"c{n}"):
            return e[f"c{n}"]
    return e.get("c")


# ---------------------------------------------------------------- the anchors of each part

_ANCHORS = {}


def anchors(lst):
    """[set per part]: the anchors each part's page holds of the list's own: entries, days, sections."""
    key = id(lst)
    if key in _ANCHORS:
        return _ANCHORS[key]
    bags = [set() for _ in parts(lst)]
    for sec in lst.sections:
        h = half_of_section(lst, sec)
        if h is None:
            continue
        bag = bags[h - 1]

        def walk(s):
            bag.add(s.id)
            if s.extra.get("old_id"):
                bag.add(str(s.extra["old_id"]))
            for e in s.entries:
                bag.add(e["id"])
                for a in e.get("aliases", []):
                    bag.add(a)
            lo, hi = s.extra.get("from"), s.extra.get("to")
            if lo and hi:
                d = datetime.date.fromisoformat(str(lo))
                end = datetime.date.fromisoformat(str(hi))
                while d <= end:
                    bag.add(f"d{d.isoformat()}")
                    d += datetime.timedelta(days=1)
            for c in s.children:
                walk(c)
        walk(sec)
    _ANCHORS[key] = bags
    return bags


HREF = re.compile(r'href="([^"#]*)#([^"]+)"')
REAL = {}          # anchor -> part (0-based): every id a built part's page holds alone (build.run, after the parts)


def _homes(lst):
    """anchor -> part (0-based): the anchors of the data (`anchors`) that one part's page holds."""
    key = ("homes", id(lst))
    if key not in _ANCHORS:
        n = {}
        for i, bag in enumerate(anchors(lst)):
            for a in bag:
                n[a] = None if a in n else i
        _ANCHORS[key] = {a: i for a, i in n.items() if i is not None}
    return _ANCHORS[key]


def route(page, lst, own):
    """Links to anchors that live on another part's page (STYLE 5): own is the part (1, 2, 3 ...) for the calendar's
    pages (a bare '#X' whose X lives in another part), None for any other page ('cal1961.html#X', or the index's
    'cal.html#X' or an old page's 'cal63.html#X', whose X lives in another part)."""
    if not cfg(lst):
        return page
    homes = _homes(lst)
    files = [f"{p['page']}.html" for p in parts(lst)]
    known = set(files) | {f"{p}.html" for p in old_pages(lst)}

    def home(anchor):
        h = REAL.get(anchor)
        return h if h is not None else homes.get(anchor)

    def sub(m):
        path, anchor = m.group(1), m.group(2)
        if own and path == "":
            h = home(anchor)
            if h is not None and h != own - 1:
                return f'href="{files[h]}#{anchor}"'
            return m.group(0)
        base = path.rsplit("/", 1)[-1]
        if base in known:
            h = home(anchor)
            if h is not None and files[h] != base:
                return f'href="{path[:len(path) - len(base)]}{files[h]}#{anchor}"'
        return m.group(0)
    return HREF.sub(sub, page)


def old_pages(lst):
    """The pages links may still name that hold no part now: the index (cal) and the parts of Oct. 17, 2026."""
    out = [p["page"] for p in ((lst.data or {}).get("legacy_parts") or [])]
    out += [p["page"] for p in ((lst.data or {}).get("retired_parts") or [])]   # the year pages, split (STYLE 14)
    ix = index_page(lst)
    return [p for p in dict.fromkeys(([ix] if ix else []) + out) if p not in {q["page"] for q in parts(lst)}]


# ---------------------------------------------------------------- old links, forwarded (STYLE 14)

ID = re.compile(r'\sid="([^"]+)"')
YEAR = re.compile(r"^(?:cal\.|d)?(\d{4})-?(\d\d)")


def years(lst):
    """{'YYYY-MM': page}: the part each month is on (a year is two parts since Nov. 12, 2026; 1972 and 1976: the
    primaries')."""
    out = {}
    for x in lst.sections:
        if x.extra.get("from"):
            out.setdefault(str(x.extra["from"])[:7], page_key(lst, half_of_section(lst, x)))
    return out


def by_rule(lst, a):
    """The page an anchor names by its form: a part's page in it (cal1961.thread.cuba, th-cal1961, ind-cal1961-cpi), else
    its year (cal.1961-04-15.cuba, d1961-04-15, 196104, 196601b); None where the form says nothing."""
    pages = {p["page"] for p in parts(lst)} - {lst.key}
    for t in re.split(r"[.-]", a):
        if t in pages:
            return t
    m = YEAR.match(a)
    return years(lst).get(f"{m.group(1)}-{m.group(2)}") if m else None


def forward(lst):
    """{anchor: 'page' or 'page#anchor'}: what the form of an anchor does not tell (by_rule): the anchors a part's page
    holds that its year does not give (an entry whose date moved from its id's, an old section id, a table's), and
    the old parts' own (cal63.thread.cuba, th2, ind-cal63-cpi: the first of the year pages over the old part's span
    that holds the like). From the built pages' anchors (REAL)."""
    ps = parts(lst)
    files = [p["page"] for p in ps]
    olds = (lst.data or {}).get("legacy_parts") or []
    out = {}
    have = {}
    for a, h in REAL.items():
        have.setdefault(files[h], set()).add(a)
        if by_rule(lst, a) == files[h]:
            continue
        if YEAR.match(a) or a.startswith("tb-") or a in _old_ids(lst):
            out[a] = files[h]
    lo0, hi0 = bounds(lst)
    for i, o in enumerate(olds):
        a = datetime.date.fromisoformat(str(o["from"])) if i else lo0
        b = (datetime.date.fromisoformat(str(olds[i + 1]["from"])) - datetime.timedelta(days=1)) if i + 1 < len(olds) else hi0
        over = [n for n in range(1, len(ps) + 1) if part_range(lst, n)[0] <= b and part_range(lst, n)[1] >= a]
        old = o["page"]
        for n in over:
            pg = files[n - 1]
            for x in sorted(have.get(pg, ())):
                if x.startswith(f"{pg}.thread."):
                    key = f"{old}.thread.{x.split('.thread.', 1)[1]}"
                elif x.startswith(f"ind-{pg}-"):
                    key = f"ind-{old}-{x[len(pg) + 5:]}"
                elif x == f"th-{pg}" and i:
                    key = f"th{i + 1}"
                else:
                    continue
                if key != x and key not in out and not (old == lst.key and key.startswith(f"{old}.thread.")):
                    out[key] = f"{pg}#{x}"
    for o in (lst.data or {}).get("retired_parts") or []:     # a year page split in halves: its own anchors to the first
        a = datetime.date.fromisoformat(str(o["from"]))         # half that holds the like (cal1964.thread.cuba,
        b = datetime.date.fromisoformat(str(o["to"]))           # th-cal1964, ind-cal1964-cpi)
        old = o["page"]
        for n in range(1, len(ps) + 1):
            if not (part_range(lst, n)[0] <= b and part_range(lst, n)[1] >= a):
                continue
            pg = files[n - 1]
            for x in sorted(have.get(pg, ())):
                if x.startswith(f"{pg}.thread."):
                    key = f"{old}.thread.{x.split('.thread.', 1)[1]}"
                elif x.startswith(f"ind-{pg}-"):
                    key = f"ind-{old}-{x[len(pg) + 5:]}"
                elif x == f"th-{pg}":
                    key = f"th-{old}"
                else:
                    continue
                out.setdefault(key, f"{pg}#{x}")
    return out


def _old_ids(lst):
    return {str(x.extra["old_id"]) for x in lst.sections if x.extra.get("old_id")}


def forward_script(lst, fwd, me):
    """The script that sends a link's anchor to its page (STYLE 14): on the index (me, the list's key) only an anchor
    the page does not hold; on an old part's page every one, and no anchor to the index."""
    import json
    first = {}                          # a retired year page with no anchor: its year's first half
    for o in (lst.data or {}).get("retired_parts") or []:
        first[o["page"]] = page_key(lst, half_of_date(lst, o["from"]))
    data = json.dumps({"f": fwd, "y": years(lst), "p": sorted({p["page"] for p in parts(lst)} - {lst.key}),
                       "me": me, "ix": lst.key, "r": first}, ensure_ascii=False, sort_keys=True, separators=(",", ":")).replace("</", "<\\/")
    return f"""<script>
/* an old link, forwarded by its anchor to the page that holds it (tools/bib/calsplit.py, STYLE 14) */
(function(){{
  var D={data};
  function to(x){{
    var f=D.f[x]; if(f) return f.indexOf('#')<0 ? f+'.html#'+x : f.replace('#','.html#');
    var t=x.split(/[.-]/); for(var i=0;i<t.length;i++) if(D.p.indexOf(t[i])>=0) return t[i]+'.html#'+x;
    var m=/^(?:cal\\.|d)?(\\d{{4}})-?(\\d\\d)/.exec(x), k=m?m[1]+'-'+m[2]:null; if(k&&D.y[k]) return D.y[k]+'.html#'+x;
    return null;
  }}
  function go(){{
    var h=location.hash.slice(1); try{{ h=decodeURIComponent(h); }}catch(e){{}}
    if(h&&document.getElementById(h)) return;
    var t=h?to(h):null;
    if(t) location.replace(t);
    else if(!h&&D.r[D.me]) location.replace(D.r[D.me]+'.html');
    else if(D.me!==D.ix) location.replace(D.ix+'.html'+(h?'#'+h:''));
  }}
  go(); window.addEventListener('hashchange',go);
}})();
</script>"""


def stub(lst, fwd, old):
    """An old part's page (cal63.html, cal66.html): a line to the index, and the script that forwards its links."""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Calendar</title>
<style>:root{{--ink:#1a1a1a;--bg:#f6f4ef}}@media (prefers-color-scheme:dark){{:root{{--ink:#e8e6e1;--bg:#16181c}}}}
body{{margin:0;padding:3rem 1rem;background:var(--bg);color:var(--ink);font:18px/1.55 Georgia,serif}}
p{{max-width:36rem;margin:0 auto}}a{{color:inherit}}</style></head>
<body><p>The calendar is now a page a half-year. This address forwards to the page that holds the place it named;
without one, to <a href="{lst.key}.html">the calendar's index</a>.</p>
{forward_script(lst, fwd, old)}
</body></html>
"""


# ---------------------------------------------------------------- a thread's dates

def thread_dates_html(lst, slug, members, esc):
    """The thread's dates in the part being built, by year, with the muted links across the divides (STYLE 1-2)."""
    half = CUR["half"]
    if half is None or not cfg(lst):
        mine, before, after = members, None, None
    else:
        mine = [m for m in members if half_of_date(lst, m["date"]) == half]
        earlier = [m for m in members if half_of_date(lst, m["date"]) < half]
        later = [m for m in members if half_of_date(lst, m["date"]) > half]
        before = earlier[-1] if earlier else None
        after = later[0] if later else None

    def cross(m):
        other = half_of_date(lst, m["date"])
        y = str(m["date"])[:4]
        return (f'<a class="tx ty" href="{href(lst, other, thread_anchor(lst, slug, other))}">{y}</a> '
                f'<a class="tx" href="{href(lst, other, m["id"])}">{esc(m["when"])}</a>')
    # a date the same as the one before it left out, for now (the owner, Nov. 5, 2026: "Pointers in thread indexes with
    # names identical to the immediately prior should be suppressed for now", until same-day entries can be told
    # apart by a time or a place): the first of the run kept, its link the day's first entry (STYLE 16)
    mine = [m for i, m in enumerate(mine) if not i or m["when"] != mine[i - 1]["when"]]
    # the dates by year (datelist STYLE), the links across the divides before or after them
    parts_ = [datelist.part(y, ls) for y, ls in
              datelist.groups([(m["date"], f'<a href="{href(lst, half or 1, m["id"])}">{esc(m["when"])}</a>') for m in mine])]
    if before:
        parts_.insert(0, cross(before))
    if after:
        parts_.append(cross(after))
    return " ".join(datelist.stop(t) for t in parts_)


def days(lst, half):
    """A part's first and last days as its dated sections give them (dates): the seams' days."""
    secs = [x for x in lst.sections if x.extra.get("from") and half_of_section(lst, x) == half]
    return (datetime.date.fromisoformat(min(str(x.extra["from"]) for x in secs)),
            datetime.date.fromisoformat(max(str(x.extra["to"]) for x in secs)))


def seam(lst, sec):
    """(before, after): the links across a seam at the head of a part's first day and the foot of the part before's
    last ("‹ Dec. 31, 1960, in Cal. 1960"; "Jan. 1, 1961, in Cal. 1961 ›"; STYLE 4)."""
    if not cfg(lst) or not sec.extra.get("from"):
        return "", ""
    lab = lambda d: f"{MON[d.month - 1]} {d.day}, {d.year}"
    ps = parts(lst)
    before = after = ""
    for n in range(2, len(ps) + 1):
        a = days(lst, n)[0]
        z = days(lst, n - 1)[1]
        if str(sec.extra["from"]) == a.isoformat():
            before = (f'<p class="seam"><a href="{href(lst, n - 1, "d" + z.isoformat())}">‹ {lab(z)}, '
                      f'in {ps[n - 2].get("abbr", lst.abbr)}</a></p>')
        if str(sec.extra.get("to")) == z.isoformat():
            after = (f'<p class="seam"><a href="{href(lst, n, "d" + a.isoformat())}">{lab(a)}, in '
                     f'{ps[n - 1].get("abbr", lst.abbr)} ›</a></p>')
    return before, after


def other_link(lst, html):
    """In a part's lede, each other part's name (its `called`: "the calendar of 1960") linked to the top of its page, or
    of its block in the reader (STYLE 6)."""
    half = CUR["half"]
    if not cfg(lst) or not half:
        return html
    for n, p in enumerate(parts(lst), start=1):
        word = p.get("called")
        if n == half or not word:
            continue
        key = p["page"]
        u = f"#{key}--top" if CUR["mode"] == "series" else f"{key}.html"
        pat = "[" + word[:1].upper() + word[:1].lower() + "]" + re.escape(word[1:]) + r"(?![\w–-])"   # "The calendar of 1960"
        html = re.sub(pat, lambda m: f'<a href="{u}">{m.group(0)}</a>', html, count=1)
    ix = index_page(lst)
    if ix:                                      # "the calendar's index": its page, or its block in the reader
        u = f"#{ix}--top" if CUR["mode"] == "series" else f"{ix}.html"
        html = re.sub(r"the calendar(['’]s) index", lambda m: f'<a href="{u}">{m.group(0)}</a>', html, count=1)
    return html


MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]

STYLE = """<style>
/* the thread index's years and the links across the calendar's halves (tools/bib/calsplit.py) */
a.tx{color:var(--muted);text-decoration-color:var(--rule)}
a.tx.ty{text-decoration:none}
a.tx.ty:hover{text-decoration:underline;text-decoration-color:var(--rule)}
/* a ghost subthread's name, and a thread's old name, in the thread index: muted, not underlined (STYLE 9, 10) */
li.thg .s,li.thg a.thgl{color:var(--muted);text-decoration:none}
li.thm .s .tho{color:var(--ink)}
/* a thread statement's See also line, set right at its foot, in the thread names' type (STYLE 11) */
.tsa{display:block;text-align:right;font-family:var(--sans);font-weight:700;font-size:.92rem;margin-top:.2rem}
.tsa i{font-weight:700}
.tsa a{color:inherit;text-decoration-color:var(--rule)}
p.seam{font-family:var(--sans);font-size:.8rem;margin:1rem 0}
p.seam a{color:var(--muted);text-decoration-color:var(--rule)}
/* a thread highlighted (STYLE 7) */
:root{--hl:#FFFFFF;--hlmark:#F29F05;--hlmin:3px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--hl:#22262E}}
:root[data-theme="dark"]{--hl:#22262E}

li[data-thread],.tnl[data-t]{cursor:pointer}
canvas.hlm{position:fixed;z-index:27;right:6px;width:28px;pointer-events:none;opacity:0;transition:opacity .18s}
canvas.hlm.on{opacity:1}
@media (prefers-reduced-motion: reduce){canvas.hlm{transition:none}}
</style>"""

SCRIPT = """<script>
/* a thread highlighted: a tap on a thread's entry in the index or on its line under an entry, not on a link (STYLE 7) */
(function(){
  var W='-.515em 0 0 var(--hl),.515em 0 0 var(--hl)', KEY='bib-thread-hl', st=document.createElement('style'); document.head.appendChild(st);
  function set(t){
    try{ t?sessionStorage.setItem(KEY,t):sessionStorage.removeItem(KEY); }catch(e){}
    st.textContent = !t ? '' :
      'li[data-threads~="'+t+'"],li[data-thread="'+t+'"]{background:var(--hl);box-shadow:'+W+'}'+
      '.day ol.e>li[data-threads~="'+t+'"]:first-child{box-shadow:inset 0 1px 0 var(--rule),'+W+'}'+
      '.day ol.e>li[data-threads~="'+t+'"]:last-child{box-shadow:inset 0 -1px 0 var(--rule),'+W+'}'+
      '.day ol.e>li[data-threads~="'+t+'"]:only-child{box-shadow:inset 0 1px 0 var(--rule),inset 0 -1px 0 var(--rule),'+W+'}'+
      '.tnl[data-t="'+t+'"]{color:var(--ink)}';
    document.documentElement.dataset.hl = t || '';
  }
  var now=''; try{ now=sessionStorage.getItem(KEY)||''; }catch(e){}
  if(/^[a-z0-9-]+$/.test(now)) set(now); else now='';
  document.addEventListener('click', function(ev){
    var rt=ev.target.closest('a.rt'), m=rt&&/thread\\.([a-z0-9-]+)$/.exec(rt.getAttribute('href')||'');
    if(m){ if(now!==m[1]){ now=m[1]; set(now); } return; }   // a rubric's thread: lit (never cleared), and the link goes on
    if(ev.target.closest('a,button,summary,input')) return;
    var el=ev.target.closest('li[data-thread],.tnl[data-t]'); if(!el) return;
    var t=el.dataset.thread||el.dataset.t; if(!/^[a-z0-9-]+$/.test(t)) return;
    now = (now===t) ? '' : t; set(now);
  });
  /* the arrow keys, while a thread is lit: the ⟨⟨ or ⟩⟩ of its entry at the top, else the lit entry next below or above
     the top (STYLE 7) */
  var cur=null, curY=-1;
  function link(li,fwd){
    var ln=li.querySelector('.tnl[data-t="'+now+'"]'), as=ln?ln.querySelectorAll('a.tnb'):[], i;
    for(i=0;i<as.length;i++) if(as[i].textContent.trim()===(fwd?'⟩⟩':'⟨⟨')) return as[i];
    return null;
  }
  function tid(a){ return a?decodeURIComponent((a.getAttribute('href')||'').split('#')[1]||''):''; }
  function order(els){                   // the page's lit entries in the thread's order, by their ⟨⟨ ⟩⟩ (a month's undated last)
    var by={}, out=[], seen={}, i, k, e;
    for(i=0;i<els.length;i++) by[els[i][1].id]=els[i];
    for(i=0;i<els.length;i++){
      e=els[i]; if(seen[e[1].id]||by[tid(link(e[1],false))]) continue;      // a head: its ⟨⟨ not on the page
      for(k=e;k&&!seen[k[1].id];k=by[tid(link(k[1],true))]){ seen[k[1].id]=1; out.push(k); }
    }
    for(i=0;i<els.length;i++) if(!seen[els[i][1].id]) out.push(els[i]);
    return out;
  }
  document.addEventListener('keydown', function(ev){
    if(!now||(ev.key!=='ArrowLeft'&&ev.key!=='ArrowRight')||ev.altKey||ev.ctrlKey||ev.metaKey||ev.shiftKey||ev.defaultPrevented) return;
    var tg=ev.target; if(tg&&tg.closest&&tg.closest('input,textarea,select,[contenteditable],canvas,.maplibregl-map,.uplot')) return;
    var top=parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop)||0, fwd=ev.key==='ArrowRight', els=[], i, r, at=null;
    var all=document.querySelectorAll('li[data-threads~="'+now+'"]');
    for(i=0;i<all.length;i++){ r=all[i].getBoundingClientRect(); if(r.height){ els.push([r.top,all[i]]); if(Math.abs(r.top-top)<3) at=all[i]; } }
    if(!els.length) return;
    if(cur&&cur.isConnected&&Math.abs(window.scrollY-curY)<3) at=cur;     // where the last key left it (the page's foot)
    var a=at&&link(at,fwd), go=null, sq, j;
    ev.preventDefault();
    if(a){
      var id=decodeURIComponent((a.getAttribute('href')||'').split('#')[1]||''); go=document.getElementById(id);
      a.click();                         // the thread's own order, on this page or the next part
    } else if(!(at&&at.querySelector('.tnl[data-t="'+now+'"]'))){   // none at the top: the nearest in the thread's order
      sq=order(els);
      if(fwd){ for(j=0;j<sq.length;j++) if(sq[j][0]>top+2){ go=sq[j][1]; break; } }
      else { for(j=sq.length-1;j>=0;j--) if(sq[j][0]<top-2){ go=sq[j][1]; break; } }
      if(go) go.scrollIntoView({block:'start'});
    }
    cur=go; setTimeout(function(){ curY=window.scrollY; },250);
  });
  /* a mark for each lit entry, fixed at the right in the thumb's column, at the thumb's place that brings the entry to
     the top: while a thread is lit; amber while the headings show, white once they go; a click on one goes to its entry
     (STYLE 8) */
  var peek=document.getElementById('peek'), rail=document.getElementById('rail'), thumb=document.getElementById('thumb');
  if(!peek||!rail||!thumb) return;
  function canvas(id){ var c=document.createElement('canvas'); c.id=id; c.className='hlm'; c.setAttribute('aria-hidden','true'); document.body.appendChild(c); return c; }
  var lo=canvas('hlmarks'), hi=canvas('hlmarks-a'), hits=[], queued=false;   // lo white, hi amber over it
  function marks(){
    queued=false; hits=[];
    lo.classList.toggle('on',!!now); hi.classList.toggle('on',!!now&&peek.classList.contains('on'));
    if(!now) return;
    var rr=rail.getBoundingClientRect(), th=thumb.offsetHeight, track=rail.clientHeight-th, dpr=window.devicePixelRatio||1,
        sh=document.documentElement.scrollHeight, k=track/sh, i, r;
    var els=document.querySelectorAll('li[data-threads~="'+now+'"],li[data-thread="'+now+'"]'), ys=[];
    for(i=0;i<els.length;i++){ r=els[i].getBoundingClientRect(); if(r.height) ys.push([r.top+window.scrollY,r.height,els[i]]); }   // one layout read
    var cs=getComputedStyle(document.documentElement),
        least=Math.max(1,Math.round((parseFloat(cs.getPropertyValue('--hlmin'))||0)*dpr)),   // the least height, device pixels
        halo=cs.getPropertyValue('--hlhalo').trim(), hp=Math.round((parseFloat(cs.getPropertyValue('--hlhalow'))||0)*dpr);
    [[lo,cs.getPropertyValue('--hl').trim()||'#fff'],[hi,cs.getPropertyValue('--hlmark').trim()||'#F29F05']].forEach(function(p){
      var c=p[0]; c.style.top=rr.top+'px'; c.style.height=rr.height+'px';
      c.width=Math.round(28*dpr); c.height=Math.round(rr.height*dpr);
      var g=c.getContext('2d'); g.fillStyle=p[1];
      for(i=0;i<ys.length;i++){          // the entry's share of the page, as its share of the thumb's travel; at least `least`
        var y0=(th/2+ys[i][0]*k)*dpr, y1=y0+ys[i][1]*k*dpr, a=Math.floor(y0), h=Math.round(y1)-a;
        if(h<least){ a=Math.round((y0+y1)/2-least/2); h=least; }      // fattened about the entry's middle
        if(halo){ g.fillStyle=halo; g.fillRect(0,a-hp,c.width,h+2*hp); g.fillStyle=p[1]; }
        g.fillRect(0,a,c.width,h);
        if(c===lo) hits.push([a/dpr,(a+h)/dpr,ys[i][2]]);
      }
    });
  }
  function later(){ if(!queued){ queued=true; requestAnimationFrame(marks); } }
  var set0=set; set=function(t){ set0(t); later(); };
  new MutationObserver(later).observe(peek,{attributes:true,attributeFilter:['class']});
  window.addEventListener('resize',later);
  if(window.ResizeObserver) new ResizeObserver(later).observe(document.body);   // the page grows or shrinks: the marks move
  later();
  /* the mark under the pointer, within 6px (a finger's reach for a 3px mark): the nearest */
  function hit(ev){
    if(!now||ev.target.closest('#thumb')) return null;
    var y=ev.clientY-rail.getBoundingClientRect().top, best=null, d=7, i, m, e;
    for(i=0;i<hits.length;i++){ m=hits[i]; e=y<m[0]?m[0]-y:y>m[1]?y-m[1]:0; if(e<d){ d=e; best=m[2]; } }
    return best;
  }
  rail.addEventListener('click',function(ev){ var el=hit(ev); if(el) el.scrollIntoView({block:'start'}); });
  rail.addEventListener('pointermove',function(ev){ rail.style.cursor=hit(ev)?'pointer':''; });
})();
</script>"""
