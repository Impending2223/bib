"""The Threads pages (the owner, Nov. 21, 2026: "Could we create a "Threads", akin to our "Names", compiling the entries
in each thread in calendar-chronological order?"; "Could the Names and Threads entries also get the full footnote
treatment?").

    ./bib build threads      build/threads.html, the index, and a page a thread (threads-<slug>.html)

STYLE
 1. A page a thread, `threads-<slug>.html`: every calendar entry whose `thread` is the thread or whose `also:` names
    it (build.index_members: an entry filed under a subthread is on the subthread's page, not its parent's, unless its
    `also:` names the parent), in the chronological sort (chron.py), place by place (chron.groups), a parent's
    subentries after it, a hair indented, where the thread holds both.
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
    what the page holds and its count, the thread in the calendar's index, its parent's page and its subthreads'.
 6. The budget (pages.py; pages.yaml `threads:`, written by `./bib pages --plan`): a thread's page over budget is in
    parts by date, a year a part, a year over in quarters, a quarter over in months, small ones in a row packed to the
    fill; a part `threads-<slug>-<its first unit>` (threads-china-leadership-1960Q1), labelled by its span ("1961",
    "1962–1964", "Jan.–Mar. 1960", "Apr. 1966"). The thread's own page is then its index: the head, its parts, and an
    old link sent to the part that holds its anchor's date (`forward`). Each part carries the parts' bar at its head
    and the part before and after at its foot (pages.bar, pages.seam). A part a later plan drops forwards the same way.
 7. threads.html, the index: every thread with entries, in the thread index's order (th.yaml), by its full name
    ("Defense: McNamara to Clifford"), linked to its page; its statement for the whole span (its topic and its stations,
    as the calendar's pages give it: the owner, Nov. 23, 2026); its count, a split thread's parts by span.
 8. Links in: each thread's entry in the calendar's thread index and in cal.html's list ("All entries", linked; a
    split thread's parts by span: index_link), the bar's 糸, the reader's drawer and home page.
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


def slugs(lst):
    """The threads with a page: those with entries, not an old name (`see:`), in the index's order."""
    return [s for s, te in lst.threads().items() if not te.get("see") and members(lst, s)]


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


def plan_parts(slug, sizes, target, start=None):
    """[{page, from, label}]: the thread's entries [(date, bytes)] in parts within target (STYLE 6): a year a unit, a
    year over in quarters, a quarter over in months; units in a row packed while they fit. start: the first part's
    `from` (a part planned again keeps its own)."""
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
        out.append({"page": f"{page_of(slug)}-{unit_code(p['kind'], p['lo'])}", "from": str(frm),
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


def _days(series, lst, rows_by_place, text_html, thread_name):
    """The entries place by place, under the year's and the month's headings (STYLE 4)."""
    import calendar as C
    from . import build, daybook
    out, cur_y, cur_m, seen_ix = [], None, None, {}

    def li(e, sub):
        hit = series.get(e["id"])
        sec = hit[1] if hit else None
        h = build.entry_html(series, lst, sec, e, text_html, "", "", daybook.rubric(lst, e, thread_name))
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
                       f'data-crumb="{d.year} / {C.month_name[d.month]}">{esc(name)}</h3>')
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


def _head(series, lst, slug, text_html, lo, hi, count, whole):
    """The page's head (STYLE 5): the statement, the line of what it holds and its links."""
    from . import build
    te = lst.threads()[slug]
    out = []
    if STATEMENT:
        st = _statement(lst, te, lo, hi)
        for i, c in enumerate(store.as_list(st)):
            body = text_html(c, "c")
            out.append(f'<p class="lede">{build.thread_person(series, body) if i == 0 else body}</p>')
    line = [f"{count:,} {'entry' if count == 1 else 'entries'}"
            + ("" if whole else " here") + ", in the calendar's order: the thread's own, and those it holds by "
            "<i>also</i>. Each as the calendar gives it; its □ leads to it there."]
    links = [f'<a href="cal.html#{esc(lst.key)}.thread.{esc(slug)}">The thread in the calendar</a>']
    par = te.get("parent")
    if par and par in lst.threads() and members(lst, par):
        links.append(f'Part of <a href="{page_of(par)}.html">{esc(build.thread_name(lst, par))}</a>')
    kids = [s for s in slugs(lst) if lst.threads()[s].get("parent") == slug and s != slug]
    if kids:
        links.append("Subthreads: " + ", ".join(
            f'<a href="{page_of(s)}.html">{esc(store_plain(lst.threads()[s].get("s") or s))}</a>' for s in kids))
    links.append('<a href="threads.html">All threads</a>')
    out.append(f'<p class="logic">{line[0]} ' + ". ".join(links) + ".</p>")
    return out


def store_plain(t):
    from .markup import plain
    return plain(str(t))


def _wrap(series, template, title, main, scripts=""):
    from . import build, daybook, permalink, vispage
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", esc(title)).replace("{{main}}", vispage.fill("\n".join(main)))
    pg = pg.replace("<head>", "<head>\n" + build.source_note(series, "lists/cal/ (threads)"), 1)
    pg = daybook.inject(pg)                  # the day's style, the footnotes', the dateline's
    pg = permalink.inject(pg)                # the permalink mark's style
    pg = vispage.inject(pg)                  # the visibility panel's assets
    if scripts:
        pg = pg.replace("</body>", scripts + "\n</body>", 1)
    return pg


def thread_page(series, linker, template, lst, slug, ents, part=None, ps=None):
    """One page: the thread's (part None), or a part of it (ps the parts, part its index)."""
    from . import build, calsplit, chron, cjk, pages, vispage
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
    if ps:
        main.append(pages.bar(page_of(slug), ps, part))
    main.append(vispage.MARK)
    vispage.begin()
    with cjk.as_page(series, lst, ents, me):
        body = _days(series, lst, chron.groups(lst, ents), text_html, build.thread_name)
    if ps:
        body.append(pages.seam(page_of(slug), ps, part))
    text = "\n".join(body)
    own = set(IDS.findall("\n".join(main) + text))
    main.append(_rewrite(text, own))
    return _wrap(series, template, title, main)


def thread_index(series, linker, template, lst, slug, ps, counts):
    """A split thread's own page: its head, its parts, and old links forwarded (STYLE 6)."""
    from . import build
    text_html = build.list_text_html(series, lst.key, linker)
    name = build.thread_name(lst, slug)
    from . import calsplit
    lo, hi = calsplit.part_range(lst, None)
    main = [f"<h1>{esc(name)}</h1>"] + _head(series, lst, slug, text_html, lo, hi, sum(counts), True)
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
        ms = members(lst, slug)
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
                    f'{esc(build.thread_name(lst, slug))}</a></span>' + "".join(st) + f'<span class="n">{len(ms):,} '
                    f'{"entry" if len(ms) == 1 else "entries"}{more}.</span></li>', set()))
    main = ["<h1>Threads</h1>",
            '<p class="logic">Each thread of the calendar, a page a thread: its entries, its own and those it holds '
            "by <i>also</i>, in the calendar's order, each as the calendar gives it. A large thread is in parts by "
            "date. In the thread index's order. The threads in the calendar: "
            f'<a href="{esc(lst.key)}.html#th">the calendar\'s index</a>.</p>',
            f'<p class="logic">{len(rows):,} threads.</p>',
            '<ol class="e thx">' + "".join(rows) + "</ol>"]
    return _wrap(series, template, "Threads", main)


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
        slug = next((s for s in slugs(lst) if parts(s) and old.startswith(page_of(s) + "-")), None)
        if slug and (not only or slug in only):
            yield f"{old}.html", pages.stub("Threads", page_of(slug), {}, old).replace(
                pages.forward_script({}, old), forward(parts(slug), old))
