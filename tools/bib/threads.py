"""The Threads pages (the owner, Nov. 21, 2026: "Could we create a "Threads", akin to our "Names", compiling the entries
in each thread in calendar-chronological order?"; "Could the Names and Threads entries also get the full footnote
treatment?").

    ./bib build threads      build/threads.html, the index, and a page a thread (threads-<slug>.html)

STYLE
 1. A page a thread, `threads-<slug>.html`: every calendar entry whose `thread` is the thread or whose `also:` names
    it (build.index_members: an entry filed under a subthread is on the subthread's page, not its parent's, unless its
    `also:` names the parent), in the chronological sort (chron.py), place by place (chron.groups), a parent's
    subentries after it, a hair indented, where the thread holds both. Every thread with entries in its family (the
    thread and every thread under it: build.thread_members) has a page; one with none of its own, its head alone
    (STYLE 9).
 2. Each entry as the calendar renders it, by the calendar's own renderer (build.entry_html, build.list_text_html):
    its rubric, place and time, the claims' spans and the visibility panel, the footnotes, the To/From and ⟨⟨ ⟩⟩
    lines, the □ mark to e.html#ID. The firsts are the page's own: a work's first citation on the page in full, a
    statute's, a person's characters (cjk.as_page). The blocks the calendar's injects put under an entry (returns,
    tables, maps) are the calendar's alone.
 3. Anchors (the calendar's ids are never repeated here: e.json and the calendar's router know the calendar's pages
    alone, permalink.py STYLE 4): an entry `t-<id>`; a day `t-d<date>`; an intercalary day `t-<its calendar
    anchor>`; a year `t-y<year>`; a month `t-m<YYYY-MM>`. A link to an entry the page holds stays on the page; any
    other bare link (another entry, a thread's line in the index) goes to the calendar, `cal.html#X`, which the
    calendar's router sends to its part (calsplit.route).
 4. Headings as the calendar's: the year (h2), the month (h3, "April 1961"), then each place: a day ("Monday, Apr.
    17": daybook.day_open), a month's undated block ("April"), a year's, an intercalary day ("Late May"), a year's
    later part before its month's heading (daybook STYLE 17). No Times, programs, weeks or folded blocks: the day's
    materials are the calendar's.
 5. The head: the thread's name; its statement for the page's span (statements.render), where STATEMENT; a line of
    what the page holds and its count, the thread in the calendar's index, its parent's page; then its subthreads
    (STYLE 9; on a split thread's part, their names in the line). Then, on a split thread's part, the parts' bar; then
    the thread's map (the owner, Nov. 25, 2026: "Put them on the relevant threads top, scoped to the thread's content
    and the page's range"): the map of China on the pages of `china` and every thread under it, the map of Indochina
    on those of the threads of Vietnam and Laos, the thread's own entries alone, its span's fields on the page's
    range; none where the page's range holds no placed entry (tools/bib/maps.py, STYLE 4).
 6. The budget (pages.py; pages.yaml `threads:`, written by `./bib pages --plan`): a thread's page over budget is in
    parts by date, a year a part, a year over in quarters, a quarter over in months, small ones in a row packed to the
    fill; a part `threads-<slug>-<its first unit>` (threads-china-leadership-1960Q1), labelled by its span ("1961",
    "1962–1964", "Jan.–Mar. 1960", "Apr. 1966"). The thread's own page is then its index: the head, its parts, and an
    old link sent to the part that holds its anchor's date (`forward`). Each part carries the parts' bar at its head
    and the part before and after at its foot (pages.bar, pages.seam). A part a later plan drops forwards the same way.
 7. threads.html, the index: every thread with a page, in the thread index's order (th.yaml), by its full name
    ("Defense: McNamara to Clifford"), linked to its page; its statement for the whole span (its topic and its stations,
    as the calendar's pages give it: the owner, Nov. 23, 2026); its count (STYLE 9), a split thread's parts by span.
    After the threads, the section "Places": a page a nation, State, province and city (placepages.py, STYLE 5; ruling
    66, Nov. 26, 2026).
 8. Links in: each thread's entry in cal.html's list ("All entries", linked; a split thread's parts by span:
    index_link; not on the calendar's own pages, the owner, Nov. 23, 2026), the bar's 糸, the reader's drawer and
    home page.
 9. A thread and its subthreads (the owner, Nov. 25, 2026: "It seems absurd to exclude the famine and related episodes
    from a thread like "China: agriculture""). A parent's page lists its own entries alone (STYLE 1: the owner's rule
    of Nov. 4), and at the end of its head, under the statement and the line and above the parts' bar and the map,
    names every thread under it that has a page: a line "3 subthreads, each on its own page.", then the index's own
    list (ol.e.thx, a line a thread: STYLE 7), in the index's order, a subthread's own subthreads after it; each by
    its name after the page's thread ("Split with Moscow: Polemic" on the page of "China: Foreign affairs"), linked
    to its page, then its count and the span of its dates as a part's span is written ("1,072 entries, Jan.
    1959–Dec. 1962."). The list stands on the thread's own page (a split thread's: its index); a part keeps the
    subthreads' names in its line. The count, here and in threads.html, says both numbers where they differ: the
    entries that name the thread, and those of the thread and every thread under it, an entry counted once ("876
    entries, Jan. 1960–Dec. 1968; 2,321 with its subthreads."; none of its own, "No entries of its own; 727 in its
    subthreads, Apr. 1960–Mar. 1969."); the page's own line says the same in a sentence. A thread with entries only
    under it has the head alone: its statement, the line, its subthreads; no map, since the map shows the entries the
    page lists.
10. An old link to an entry or a day the page no longer holds (`threads-china-leadership-1960Q1.html#t-<id>`, the
    entry since filed under another thread) is sent on to the calendar: the entry by its permalink (e.html#<id>), a
    day to cal.html#d<date> (`onward`). A part a later plan dropped is its own thread's by its whole name, the page's
    less its unit (`retired_of`), never a thread's whose name its name begins with; where the thread is one page
    again, it forwards there.
"""
import datetime
import html
import json
import os
import re

from . import store

PREFIX = "t-"
STATEMENT = True          # the thread's statement heads its page (STYLE 5; the owner's to decide)
INDEX = "threads"
HREF = re.compile(r'href="#([^"]+)"')
IDS = re.compile(r'\sid="([^"]+)"')
UNIT = re.compile(r"-\d{4}(?:Q[1-4]|-\d\d)?x*$")      # a part's unit at the end of its page's name (unit_code)
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]


def esc(t):
    return html.escape(str(t), quote=True)


def page_of(slug):
    return f"threads-{slug}"


def parts(slug):
    """The thread's parts where the plan splits it (pages.yaml `threads:`), else None: [{page, from, label}]."""
    from . import pages
    ps = (pages.conf().get("threads") or {}).get(slug)
    return [dict(p) for p in ps] if ps else None


def _pad(d):
    s = str(d)[:10]
    return s + {4: "-01-01", 7: "-01"}.get(len(s), "")


def part_index(ps, iso):
    """The part a place's date falls in: the last whose `from` is on or before it (the first takes all before)."""
    s, i = _pad(iso), 0
    for k, p in enumerate(ps):
        if k and s >= _pad(p["from"]):
            i = k
    return i


def members(lst, slug):
    from . import build
    return build.index_members(lst).get(slug, [])


def family(lst, slug):
    """The entries of the thread and of every thread under it, an entry once (build.thread_members)."""
    from . import build
    return build.thread_members(lst).get(slug, [])


def slugs(lst):
    """The threads with a page: those with entries in their family (their own or a subthread's: STYLE 9), not an old
    name (`see:`), in the index's order."""
    return [s for s, te in lst.threads().items() if not te.get("see") and family(lst, s)]


def under(lst, slug):
    """The threads under slug that have a page, in the index's order, a subthread's own subthreads after it."""
    T, kids, out = lst.threads(), {}, []
    for s in slugs(lst):
        kids.setdefault(T[s].get("parent"), []).append(s)

    def walk(p):
        for s in kids.get(p, []):
            if s != slug and s not in out:
                out.append(s)
                walk(s)
    walk(slug)
    return out


def name_under(lst, slug, top):
    """A subthread's name after the thread whose page names it: "Split with Moscow: Polemic" under china-foreign."""
    line = lst.thread_line(slug)
    line = line[:line.index(top)] if top in line else line
    return ": ".join(store_plain(lst.threads()[s].get("s") or s) for s in reversed(line))


def span(ents):
    """The span of the entries' dates, as a part's span is written (label): "Apr. 1961", "Jan. 1959–Dec. 1962",
    "1961–1964"; a month for an entry placed in a month, a year for one placed in a year."""
    from . import loose
    los, his = [], []
    for e in ents:
        iso = str(loose.place_iso(e))[:10]
        try:
            lo = datetime.date.fromisoformat(_pad(iso))
        except ValueError:
            continue
        los.append(unit_start("y" if len(iso) == 4 else "m", lo))
        his.append(_end("y" if len(iso) == 4 else "m", lo))
    return label(min(los), max(his)) if los else ""


def _n(n):
    return f"{n:,} {'entry' if n == 1 else 'entries'}"


def count(lst, slug, spans=False):
    """A thread's count (STYLE 9): "876 entries"; where its family holds more, "876 entries; 2,321 with its
    subthreads"; none of its own, "No entries of its own; 727 in its subthreads". spans: each count's dates after it."""
    own, fam = members(lst, slug), family(lst, slug)
    def sp(ents):
        s = span(ents) if spans else ""
        return f", {s}" if s else ""
    if not own:
        return f"No entries of its own; {len(fam):,} in its subthreads" + sp(fam)
    return _n(len(own)) + sp(own) + (f"; {len(fam):,} with its subthreads" if len(fam) != len(own) else "")


def subthreads(lst, slug):
    """The thread's subthreads at the end of its page's head (STYLE 9): [] where it has none with a page."""
    subs = under(lst, slug)
    if not subs:
        return []
    rows = []
    for s in subs:
        ghost = ' class="thg"' if lst.is_ghost(s) else ""
        rows.append(f'<li{ghost}><span class="s"><a href="{page_of(s)}.html">{esc(name_under(lst, s, slug))}</a></span>'
                    f'<span class="n">{count(lst, s, True)}.</span></li>')
    n = len(rows)
    return [f'<p class="logic">{n:,} {"subthread, on its own page" if n == 1 else "subthreads, each on its own page"}.'
            "</p>", '<ol class="e thx">' + "".join(rows) + "</ol>"]


def calendar(series):
    return next((l for l in series.lists.values() if l.kind == "calendar"), None)


def index_link(lst, slug):
    """Under a thread's entry in the calendar's index: "All entries.", linked to its page; a split thread's parts by
    span (STYLE 8). Empty for a thread with no page."""
    if not members(lst, slug) or (lst.threads().get(slug) or {}).get("see"):
        return ""
    ps = parts(slug)
    if not ps:
        return f'<span class="n tha"><a href="{page_of(slug)}.html">All entries</a>.</span>'
    return (f'<span class="n tha"><a href="{page_of(slug)}.html">All entries</a>: '
            + ", ".join(f'<a href="{esc(p["page"])}.html">{esc(p["label"])}</a>' for p in ps) + ".</span>")


# ---------------------------------------------------------------- the spans of the parts (STYLE 6)

def unit_code(kind, d):
    return {"y": f"{d.year}", "q": f"{d.year}Q{(d.month - 1) // 3 + 1}", "m": f"{d.year}-{d.month:02d}"}[kind]


def unit_start(kind, d):
    if kind == "y":
        return datetime.date(d.year, 1, 1)
    if kind == "q":
        return datetime.date(d.year, (d.month - 1) // 3 * 3 + 1, 1)
    return datetime.date(d.year, d.month, 1)


def label(lo, hi):
    """A part's span: "1961", "1962–1964", "Jan.–Mar. 1960", "Oct. 1961–Mar. 1962", "Apr. 1966" (lo, hi: its first
    and last days)."""
    whole = lo.month == 1 and lo.day == 1 and hi.month == 12 and hi.day == 31
    if whole:
        return f"{lo.year}" if lo.year == hi.year else f"{lo.year}–{hi.year}"
    a, b = MON[lo.month - 1], MON[hi.month - 1]
    if lo.year == hi.year:
        return f"{a} {lo.year}" if lo.month == hi.month else f"{a}–{b} {lo.year}"
    return f"{a} {lo.year}–{b} {hi.year}"


def _end(kind, d):
    s = unit_start(kind, d)
    if kind == "y":
        return datetime.date(s.year, 12, 31)
    months = 3 if kind == "q" else 1
    m = s.month + months
    nxt = datetime.date(s.year + (m > 12), (m - 1) % 12 + 1, 1)
    return nxt - datetime.timedelta(days=1)


def plan_parts(slug, sizes, target, start=None, page=None):
    """[{page, from, label}]: the thread's entries [(date, bytes)] in parts within target (STYLE 6): a year a unit, a
    year over in quarters, a quarter over in months; units in a row packed while they fit. start: the first part's
    `from` (a part planned again keeps its own). page: the page the parts are of, where not the thread's (a place's:
    placepages.py, STYLE 4)."""
    by = {}
    for d, n in sizes:
        by.setdefault(unit_start("y", d), []).append((d, n))
    units = []                                       # [(kind, first day, bytes)]

    def cut(kind, ds):
        tot = sum(n for _, n in ds)
        nxt = {"y": "q", "q": "m"}.get(kind)
        if tot <= target or nxt is None:
            units.append((kind, unit_start(kind, ds[0][0]), tot))
            return
        sub = {}
        for d, n in ds:
            sub.setdefault(unit_start(nxt, d), []).append((d, n))
        for k in sorted(sub):
            cut(nxt, sub[k])
    for k in sorted(by):
        cut("y", by[k])
    packs = []
    for kind, d, n in units:
        if packs and packs[-1]["bytes"] + n <= target:
            packs[-1]["bytes"] += n
            packs[-1]["hi"] = _end(kind, d)
        else:
            packs.append({"kind": kind, "lo": d, "hi": _end(kind, d), "bytes": n})
    out = []
    for i, p in enumerate(packs):
        frm = (start or p["lo"].isoformat()) if i == 0 else p["lo"].isoformat()
        out.append({"page": f"{page or page_of(slug)}-{unit_code(p['kind'], p['lo'])}", "from": str(frm),
                    "label": label(p["lo"], p["hi"])})
    return out


# ---------------------------------------------------------------- the pages

def forward(ps, me):
    """The script that sends an old link to the part that holds its anchor's date (STYLE 6)."""
    data = json.dumps({"f": [[_pad(p["from"]) if i else "", p["page"]] for i, p in enumerate(ps)], "me": me},
                      separators=(",", ":"))
    return f"""<script>
/* an old link, sent by its anchor's date to the part that holds it (tools/bib/threads.py, STYLE 6) */
(function(){{
  var D={data};
  function go(){{
    var h=location.hash.slice(1); try{{ h=decodeURIComponent(h); }}catch(e){{}}
    if(!h||document.getElementById(h)) return;
    var m=/(\\d{{4}})(?:-?(\\d\\d))?(?:-(\\d\\d))?/.exec(h); if(!m) return;
    var d=m[1]+'-'+(m[2]||'01')+'-'+(m[3]||'01'), k=0;
    for(var i=1;i<D.f.length;i++) if(d>=D.f[i][0]) k=i;
    if(D.f[k][1]!==D.me) location.replace(D.f[k][1]+'.html#'+h);
  }}
  go(); window.addEventListener('hashchange',go);
}})();
</script>"""


def onward(key):
    """The script that sends a link to an entry or a day the page no longer holds on to the calendar (STYLE 10)."""
    return f"""<script>
/* a link to an entry or a day this page no longer holds, sent on to the calendar (tools/bib/threads.py, STYLE 10) */
(function(){{
  function go(){{
    var h=location.hash.slice(1); try{{ h=decodeURIComponent(h); }}catch(e){{}}
    if(h.slice(0,{len(PREFIX)})!=='{PREFIX}'||document.getElementById(h)) return;
    var x=h.slice({len(PREFIX)});
    if(x.indexOf('{key}.')===0) location.replace('e.html#'+x);
    else if(/^d\\d{{4}}-\\d\\d-\\d\\d$/.test(x)) location.replace('cal.html#'+x);
  }}
  go(); window.addEventListener('hashchange',go);
}})();
</script>"""


def retired_of(lst, old):
    """The thread a dropped part was a part of: the page's name less its unit ("threads-china-leadership-1960Q1":
    china-leadership), where that is a thread with a page; never a thread whose name its name only begins with
    (STYLE 10)."""
    m = UNIT.search(old)
    slug = old[len(page_of("")):m.start()] if m and old.startswith(page_of("")) else None
    return slug if slug in slugs(lst) else None


def _statement(lst, te, lo, hi):
    from . import statements
    if statements.legacy(te):
        return te.get("c")
    return statements.render(lst, te, lo, hi)


def _rewrite(body, own):
    """STYLE 3: a bare link to an anchor the page holds stays; to an entry it holds, its own anchor; else the
    calendar's."""
    def sub(m):
        a = m.group(1)
        if a in own:
            return m.group(0)
        if PREFIX + a in own:
            return f'href="#{PREFIX}{a}"'
        return f'href="cal.html#{a}"'
    return HREF.sub(sub, body)


def _days(series, lst, rows_by_place, text_html, thread_name, mark=None):
    """The entries place by place, under the year's and the month's headings (STYLE 4). mark: an entry's words at the
    head of its rubric, before its threads, or None (a place's page: placepages.py, STYLE 2)."""
    import calendar as C
    from . import build, daybook
    out, cur_y, cur_m, seen_ix = [], None, None, {}

    def li(e, sub):
        hit = series.get(e["id"])
        sec = hit[1] if hit else None
        rub = daybook.rubric(lst, e, thread_name)
        m = mark(e) if mark else ""
        if m:
            rub = rub.replace('<span class="s rub">', f'<span class="s rub">{m} · ', 1)
        h = build.entry_html(series, lst, sec, e, text_html, "", "", rub)
        h = h.replace(f'<li id="{esc(e["id"])}"', f'<li id="{PREFIX}{esc(e["id"])}"', 1)
        return daybook.sub_li(h) if sub else h

    for k, rows in rows_by_place:
        d, slot = k[0], k[1]
        ol = '<ol class="e">' + "".join(li(e, sub) for e, sub in rows) + "</ol></div>"
        if d == datetime.date.max:                  # no place the calendar can give it
            out.append(daybook.block_open("Undated") + ol)
            continue
        if d.year != cur_y:
            out.append(f'<h2 id="{PREFIX}y{d.year}" data-short="{d.year}" data-crumb="{d.year}">{d.year}</h2>')
            cur_y, cur_m = d.year, None
        if slot not in (-2, -1.5) and d.month != cur_m:
            name = f"{C.month_name[d.month]} {d.year}"
            out.append(f'<h3 id="{PREFIX}m{d.year}-{d.month:02d}" data-short="{esc(name)}" '
                       f'data-crumb="{C.month_name[d.month]}">{esc(name)}</h3>')   # the year is the h2's crumb (Nov. 22)
            cur_m = d.month
        if slot == 1:
            out.append(daybook.day_open(d, 4, False, f"{PREFIX}d{d.isoformat()}") + "</div>" + ol)
        elif slot == -1:
            out.append(daybook.block_open(C.month_name[d.month]) + ol)
        elif slot == -2:
            out.append(daybook.block_open("", "mo yr") + ol)
        else:
            n = seen_ix[(d, slot)] = seen_ix.get((d, slot), 0) + 1
            out.append(daybook.ix_open(k[3], 4, PREFIX + daybook.ix_id(d, slot, n)) + ol)
    return out


def _head(series, lst, slug, text_html, lo, hi, n, whole):
    """The page's head (STYLE 5): the statement, the line of what it holds and its links; on the thread's own page
    (whole), its subthreads (STYLE 9)."""
    from . import build
    te = lst.threads()[slug]
    out = []
    if STATEMENT:
        st = _statement(lst, te, lo, hi)
        for i, c in enumerate(store.as_list(st)):
            body = text_html(c, "c")
            out.append(f'<p class="lede">{build.thread_person(series, body) if i == 0 else body}</p>')
    fam = len(family(lst, slug))
    if not n and whole:                     # entries only under it: no list of entries (STYLE 9)
        line = (f"No entries of its own. Its subthreads hold {fam:,}, an entry counted once; a subthread's entries "
                "are on its own page.")
    else:
        line = (f"{_n(n)}" + ("" if whole else " here") + ", in the calendar's order: the thread's own, and those it "
                "holds by <i>also</i>. " + (f"The thread and its subthreads together hold {fam:,}, an entry counted "
                                            "once; a subthread's entries are on its own page. "
                                            if whole and fam != n else "")
                + "Each as the calendar gives it; its □ leads to it there.")
    links = [f'<a href="cal.html#{esc(lst.key)}.thread.{esc(slug)}">The thread in the calendar</a>']
    par, have = te.get("parent"), slugs(lst)
    if par and par != slug and par in have:
        links.append(f'Part of <a href="{page_of(par)}.html">{esc(build.thread_name(lst, par))}</a>')
    kids = [s for s in have if lst.threads()[s].get("parent") == slug and s != slug]
    if kids and not whole:                  # a part: the subthreads' names; the list is on the thread's own page
        links.append("Subthreads: " + ", ".join(
            f'<a href="{page_of(s)}.html">{esc(store_plain(lst.threads()[s].get("s") or s))}</a>' for s in kids))
    links.append('<a href="threads.html">All threads</a>')
    out.append(f'<p class="logic">{line} ' + ". ".join(links) + ".</p>")
    if whole:
        out += subthreads(lst, slug)
    return out


def store_plain(t):
    from .markup import plain
    return plain(str(t))


def _wrap(series, template, title, main, scripts="", src="threads"):
    from . import build, daybook, permalink, vispage
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", esc(title)).replace("{{main}}", vispage.fill("\n".join(main)))
    pg = pg.replace("<head>", "<head>\n" + build.source_note(series, f"lists/cal/ ({src})"), 1)
    pg = daybook.inject(pg)                  # the day's style, the footnotes', the dateline's
    pg = permalink.inject(pg)                # the permalink mark's style
    pg = vispage.inject(pg)                  # the visibility panel's assets
    if scripts:
        pg = pg.replace("</body>", scripts + "\n</body>", 1)
    from . import maps
    return maps.head(pg)                     # the map's style and script, where the page carries one (STYLE 5)


def thread_page(series, linker, template, lst, slug, ents, part=None, ps=None):
    """One page: the thread's (part None), or a part of it (ps the parts, part its index)."""
    from . import build, calsplit, chron, cjk, maps, pages, vispage
    name = build.thread_name(lst, slug)
    me = ps[part]["page"] if ps else page_of(slug)
    text_html = build.list_text_html(series, lst.key, linker)
    calsplit.CUR.update(half=None, mode="list")
    lo, hi = calsplit.part_range(lst, None)
    if ps:
        lo = max(lo, datetime.date.fromisoformat(_pad(ps[part]["from"]))) if part else lo
        if part + 1 < len(ps):
            hi = datetime.date.fromisoformat(_pad(ps[part + 1]["from"])) - datetime.timedelta(days=1)
    title = f"Threads: {name}" + (f", {ps[part]['label']}" if ps else "")
    main = [f"<h1>{esc(name)}" + (f", {esc(ps[part]['label'])}" if ps else "") + "</h1>"]
    main += _head(series, lst, slug, text_html, lo, hi, len(ents), not ps)
    if not ents and not ps:                  # entries only under it: the head alone (STYLE 9)
        return _wrap(series, template, title, main, onward(lst.key))
    if ps:
        main.append(pages.bar(page_of(slug), ps, part))
    main += [f for f in [maps.thread_figure(series, lst, slug, lo, hi)] if f]   # the thread's map (STYLE 5)
    main.append(vispage.MARK)
    vispage.begin()
    with cjk.as_page(series, lst, ents, me):
        body = _days(series, lst, chron.groups(lst, ents), text_html, build.thread_name)
    if ps:
        body.append(pages.seam(page_of(slug), ps, part))
    text = "\n".join(body)
    own = set(IDS.findall("\n".join(main) + text))
    main.append(_rewrite(text, own))
    return _wrap(series, template, title, main, onward(lst.key))


def thread_index(series, linker, template, lst, slug, ps, counts):
    """A split thread's own page: its head, its parts, and old links forwarded (STYLE 6)."""
    from . import build
    text_html = build.list_text_html(series, lst.key, linker)
    name = build.thread_name(lst, slug)
    from . import calsplit
    lo, hi = calsplit.part_range(lst, None)
    main = [f"<h1>{esc(name)}</h1>"] + _head(series, lst, slug, text_html, lo, hi, sum(counts), True)
    from . import maps
    main += [f for f in [maps.thread_figure(series, lst, slug, lo, hi)] if f]   # the thread's map (STYLE 5)
    main.append('<ul class="pgl">' + "".join(
        f'<li><a href="{esc(p["page"])}.html">{esc(p["label"])}</a>: {n:,} {"entry" if n == 1 else "entries"}</li>'
        for p, n in zip(ps, counts)) + "</ul>")
    from . import pages
    return _wrap(series, template, f"Threads: {name}", main, pages.PART_CSS + forward(ps, page_of(slug)))


def index_page(series, template, lst):
    """threads.html (STYLE 7)."""
    from . import build, calsplit
    rows = []
    text_html = build.list_text_html(series, lst.key)
    lo, hi = calsplit.part_range(lst, None)          # the whole calendar's span
    for slug in slugs(lst):
        ps = parts(slug)
        more = (": " + ", ".join(f'<a href="{esc(p["page"])}.html">{esc(p["label"])}</a>' for p in ps)) if ps else ""
        ghost = ' class="thg"' if lst.is_ghost(slug) else ""
        # the thread's statement, its topic and its stations, as the calendar's pages give it (the owner, Nov. 23,
        # 2026: "between the thread name and the entry count and links, styled as they are on the individual
        # calendar pages"); links to entries go to the calendar
        st = []
        for i, c in enumerate(store.as_list(_statement(lst, lst.threads()[slug], lo, hi))):
            body = text_html(c, "c")
            st.append(f'<span class="c">{build.thread_person(series, body) if i == 0 else body}</span>')
        rows.append(_rewrite(f'<li id="{esc(slug)}"{ghost}><span class="s"><a href="{page_of(slug)}.html">'
                    f'{esc(build.thread_name(lst, slug))}</a></span>' + "".join(st)
                    + f'<span class="n">{count(lst, slug)}{more}.</span></li>', set()))
    main = ["<h1>Threads</h1>",
            '<p class="logic">Each thread of the calendar, a page a thread: its entries, its own and those it holds '
            "by <i>also</i>, in the calendar's order, each as the calendar gives it. A large thread is in parts by "
            "date. A thread's subthreads are named at the head of its page, each with a page of its own. In the "
            "thread index's order. The threads in the calendar: "
            f'<a href="{esc(lst.key)}.html#th">the calendar\'s index</a>.</p>',
            f'<p class="logic">{len(rows):,} threads. After them, <a href="#places">the places</a>.</p>',
            '<ol class="e thx">' + "".join(rows) + "</ol>"]
    from . import placepages                         # the section "Places" (placepages.py, STYLE 5)
    places = placepages.index_section(series)
    if not places:
        main[2] = f'<p class="logic">{len(rows):,} threads.</p>'
    return _wrap(series, template, "Threads", main + places)


def pages_(series, linker, template, only=None):
    """(file name, html), one page at a time: threads.html and every thread's pages (a split thread's index and
    parts); a part a later plan dropped (pages.yaml `retired`), a page that forwards. only: these slugs alone (a test,
    a quick look)."""
    from . import loose, pages
    lst = calendar(series)
    if lst is None:
        return
    yield f"{INDEX}.html", index_page(series, template, lst)
    live = set(pages.live_pages())
    for slug in slugs(lst):
        if only and slug not in only:
            continue
        ents = members(lst, slug)
        ps = parts(slug)
        if not ps:
            yield f"{page_of(slug)}.html", thread_page(series, linker, template, lst, slug, ents)
            continue
        by = [[] for _ in ps]
        for e in ents:
            by[part_index(ps, loose.place_iso(e))].append(e)
        yield f"{page_of(slug)}.html", thread_index(series, linker, template, lst, slug, ps, [len(b) for b in by])
        for i, p in enumerate(ps):
            yield f"{p['page']}.html", thread_page(series, linker, template, lst, slug, by[i], i, ps)
    for old in pages.conf().get("retired") or []:
        if not old.startswith("threads-") or old in live:
            continue
        slug = retired_of(lst, old)
        if slug and (not only or slug in only):       # to its thread's parts; to its one page where it has none now
            yield f"{old}.html", pages.stub("Threads", page_of(slug), {}, old).replace(
                pages.forward_script({}, old), forward(parts(slug) or [{"from": "", "page": page_of(slug)}], old))
