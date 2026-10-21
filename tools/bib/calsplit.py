"""The calendar in two halves: one list in the data (lists/cal/), two pages in the build, parted at the 88th Congress's
opening (January 1963; the sections are calendar months, so the second begins Jan. 1), as the first opens at the 86th's
second session (Jan. 6, 1960).

    lists/cal/list.yaml, `split:`   the date the second half begins (`from`), its page (`page`: cal63), and its own
                                    page_title, h1, lede, logic, abbr and title; the list's own fields are the first's

The threads section (`th`) is in both halves: each half's thread index lists only the threads with entries in it, each
with its statement for that half (`c` in the first; in the second `c2`, or `c` where the thread has entries in the second
alone) and its dates there. Everything else goes by date: a dated section to the half its first day falls in.

STYLE:
 1. A thread's dates by year, as every list of calendar dates is written (tools/bib/datelist.py, its STYLE):
    ("1961 Jan. 23, Feb. 20. 1962 ..."), each date linked to its entry.
 2. Across the divide, muted, linked: in the first half, after its dates, the year of the thread's next entry in the
    second, linked to the thread's entry in the second half's index, and that entry's date, linked to the entry
    (". 1963 Jan. 14."); the year not underlined; in the second, before its dates, the year and date of the thread's last entry in the first,
    linked the same way ("1962 Dec. 11. 1963 ...").
 3. The second half's thread entries take the anchor cal63.thread.<slug>, so that both indexes can stand in the
    reader's one page; a rubric links to its own half's index.
 4. At the seam, muted, in sans: at the head of the second half's first day, "‹ Dec. 31, 1962, in the first calendar";
    at the foot of the first half's last, "Jan. 1, 1963, in the second calendar ›" (seam).
 5. On the standalone pages a link to an anchor that lives in the other half goes to that page; on every other page,
    a link to cal.html#X where X is in the second half goes to cal63.html#X (route).
 7. A thread highlighted: a tap on a thread's entry in the index, or on a thread's line under a calendar entry ("⟨⟨ Testing
    ⟩⟩"), anywhere but on a link, sets that thread's entries, and its entry in the index, on
    white (in the dark theme, a lighter panel): the entry's own box, square, from its rule to the next, and an en dash (.515em of the serif)
    past the rules' ends on either side, into the margin (side shadows of the fill); nothing moves and no edge crosses
    text. A day's first entry, which has no rule above
    it, and its last, none below, take one while lit, drawn inside the box; the same tap again clears it, a tap on another thread moves it. The
    links (⟨⟨ and ⟩⟩) go where they go and leave the highlight as it is. A rubric's thread name, a link to the thread's
    entry in the index, goes there and lights the thread too; it never clears it. It holds across the two halves and
    the reader for the session (sessionStorage), and is the reader's alone: nothing in the address.
 6. Each half's lede names the other ("The second calendar takes up at ..."); the words linked to its page's top.
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
 9. A ghost subthread (a `parent:` and no statement) has a line in the index, in its place under its parent: its name
    (`s`), linked to its first entry in the part, and its dates there, by year (1, 2), the whole line muted, as the A–Z
    bibliography's ghost entries are, nothing underlined; no line in a part where it has no entries. A rubric naming it
    links to that line, and a tap on it lights the ghost's entries (7). Given a statement, it is a thread's entry
    like any other (`ghost_thread_html` in build.py).
"""
import datetime
import re

from . import datelist, store

# the half being built and the page kind, set by the build around each half
CUR = {"half": None, "mode": "list"}


def parts(lst):
    """The calendar's parts, in order: [{page, from, abbr, title, span, page_title, h1, lede, logic}]; the first's page
    is the list's own and its page texts the list's (list.yaml `split:`: the first item the first part's labels, each
    later item a part with its `from` and `page`). One part where the list has no split."""
    s = (lst.data or {}).get("split") if lst is not None else None
    if not s:
        return [{"page": lst.key if lst is not None else None, "from": None}]
    first = dict(s[0], page=lst.key, **{"from": None})
    return [first] + [dict(x) for x in s[1:]]


def cfg(lst):
    """The parts where the calendar has more than one, else None."""
    p = parts(lst) if lst is not None else None
    return p if p and len(p) > 1 else None


def page_key(lst, half):
    return parts(lst)[half - 1]["page"]


def half_of_date(lst, d):
    """The part a date falls in (1, 2, 3 ...): the last whose first day is on or before it."""
    n = 1
    for i, p in enumerate(parts(lst)[1:], start=2):
        if str(d)[:10] >= str(p["from"]):
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
    return f"{lst.key}.thread.{slug}" if (half or 1) == 1 else f"{page_key(lst, half)}.thread.{slug}"


def href(lst, half, anchor):
    """A link to an anchor in a part: in the page itself, or the other page; in the reader always in the page."""
    if CUR["mode"] == "series" or half == CUR["half"]:
        return f"#{anchor}"
    return f"{page_key(lst, half)}.html#{anchor}"


def statement(lst, e, half, first):
    """The thread's statement in a part (STYLE 9): its own (c2, c3 ...) where the thread begins in an earlier part;
    else the latest before it; c in the part the thread begins in."""
    for n in range(half, (first or 1), -1):
        if e.get(f"c{n}"):
            return e[f"c{n}"]
    return e.get("c")


# ---------------------------------------------------------------- the anchors of the second half

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


def route(page, lst, own):
    """Links to anchors that live on another part's page: own is the part (1, 2, 3 ...) for the calendar's pages (a bare
    '#X' whose X lives in another part), None for any other page ('cal.html#X' whose X lives in another part)."""
    if not cfg(lst):
        return page
    bags = anchors(lst)
    files = [f"{p['page']}.html" for p in parts(lst)]

    def home(anchor):
        hs = [i for i, b in enumerate(bags) if anchor in b]
        return hs[0] if len(hs) == 1 else None

    def sub(m):
        path, anchor = m.group(1), m.group(2)
        if own and path == "":
            h = home(anchor)
            if h is not None and h != own - 1:
                return f'href="{files[h]}#{anchor}"'
            return m.group(0)
        for i, f in enumerate(files):
            if path.endswith(f) and (path == f or path.endswith("/" + f)):
                h = home(anchor)
                if h is not None and h != i:
                    return f'href="{path[:-len(f)]}{files[h]}#{anchor}"'
        return m.group(0)
    return HREF.sub(sub, page)


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
    # the dates by year (datelist STYLE), the links across the divides before or after them
    parts_ = [datelist.part(y, ls) for y, ls in
              datelist.groups([(m["date"], f'<a href="{href(lst, half or 1, m["id"])}">{esc(m["when"])}</a>') for m in mine])]
    if before:
        parts_.insert(0, cross(before))
    if after:
        parts_.append(cross(after))
    return " ".join(datelist.stop(t) for t in parts_)


ORDINAL = ["first", "second", "third", "fourth", "fifth"]


def seam(lst, sec):
    """(before, after): the links across a divide at the head of a part's first day and the foot of the part before's
    last ("‹ Dec. 31, 1962, in the first calendar"; "Jan. 1, 1963, in the second calendar ›")."""
    if not cfg(lst) or not sec.extra.get("from"):
        return "", ""
    lab = lambda d: f"{MON[d.month - 1]} {d.day}, {d.year}"
    before = after = ""
    for n, p in enumerate(parts(lst)[1:], start=2):
        b = datetime.date.fromisoformat(str(p["from"]))
        last = (b - datetime.timedelta(days=1)).isoformat()
        if str(sec.extra["from"]) == b.isoformat():
            before = (f'<p class="seam"><a href="{href(lst, n - 1, "d" + last)}">‹ {lab(b - datetime.timedelta(days=1))}, '
                      f'in the {ORDINAL[n - 2]} calendar</a></p>')
        if str(sec.extra.get("to")) == last:
            after = (f'<p class="seam"><a href="{href(lst, n, "d" + b.isoformat())}">{lab(b)}, in the {ORDINAL[n - 1]} '
                     f'calendar ›</a></p>')
    return before, after


def other_link(lst, html):
    """In a part's lede, each other part's name ("the second calendar") linked to the top of its page, or of its block
    in the reader (STYLE 6)."""
    half = CUR["half"]
    if not cfg(lst) or not half:
        return html
    for n in range(1, len(parts(lst)) + 1):
        if n == half:
            continue
        word = ORDINAL[n - 1]
        key = page_key(lst, n)
        u = f"#{key}--top" if CUR["mode"] == "series" else f"{key}.html"
        html = html.replace(f"{word} calendar", f'<a href="{u}">{word} calendar</a>', 1)
    return html


MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]

STYLE = """<style>
/* the thread index's years and the links across the calendar's halves (tools/bib/calsplit.py) */
a.tx{color:var(--muted);text-decoration-color:var(--rule)}
a.tx.ty{text-decoration:none}
a.tx.ty:hover{text-decoration:underline;text-decoration-color:var(--rule)}
/* a ghost subthread's line in the thread index, muted, nothing underlined (STYLE 9) */
li.thg,li.thg .s,li.thg .ty,li.thg a{color:var(--muted);text-decoration:none}
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
    var rt=ev.target.closest('a.rt'), m=rt&&/thread\.([a-z0-9-]+)$/.exec(rt.getAttribute('href')||'');
    if(m){ if(now!==m[1]){ now=m[1]; set(now); } return; }   // a rubric's thread: lit (never cleared), and the link goes on
    if(ev.target.closest('a,button,summary,input')) return;
    var el=ev.target.closest('li[data-thread],.tnl[data-t]'); if(!el) return;
    var t=el.dataset.thread||el.dataset.t; if(!/^[a-z0-9-]+$/.test(t)) return;
    now = (now===t) ? '' : t; set(now);
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
