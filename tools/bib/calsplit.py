"""The calendar in two halves: one list in the data (lists/cal/), two pages in the build, parted at the 88th Congress's
opening (Jan. 3, 1963), as the first opens at the 87th's (Jan. 3, 1961).

    lists/cal/list.yaml, `split:`   the date the second half begins (`from`), its page (`page`: cal63), and its own
                                    page_title, h1, lede, logic, abbr and title; the list's own fields are the first's

The threads section (`th`) is in both halves: each half's thread index lists only the threads with entries in it, each
with its statement for that half (`c` in the first; in the second `c2`, or `c` where the thread has entries in the second
alone) and its dates there. Everything else goes by date: a dated section to the half its first day falls in.

STYLE:
 1. A thread's dates by year: the year in the headings' sans serif, a little heavier, unlinked, a full stop after each year's dates
    ("1961 Jan. 23, Feb. 20. 1962 ..."), each date linked to its entry.
 2. Across the divide, muted, linked: in the first half, after its dates, the year of the thread's next entry in the
    second, linked to the thread's entry in the second half's index, and that entry's date, linked to the entry
    (". 1963 Jan. 14."); the year not underlined; in the second, before its dates, the year and date of the thread's last entry in the first,
    linked the same way ("1962 Dec. 11. 1963 ...").
 3. The second half's thread entries take the anchor cal63.thread.<slug>, so that both indexes can stand in the
    reader's one page; a rubric links to its own half's index.
 4. At the seam, muted, in sans: at the head of the second half's first day, "‹ Jan. 2, 1963, in the first calendar";
    at the foot of the first half's last, "Jan. 3, 1963, in the second calendar ›" (seam).
 5. On the standalone pages a link to an anchor that lives in the other half goes to that page; on every other page,
    a link to cal.html#X where X is in the second half goes to cal63.html#X (route).
 7. A thread highlighted: a tap on a thread's entry in the index, or on a thread's line under a calendar entry ("⟨⟨ Testing
    ⟩⟩"), anywhere but on a link, sets that thread's entries, and its entry in the index, on
    white (in the dark theme, a lighter panel): the entry's own box, square, from its rule to the next, and an en dash (.515em of the serif)
    past the rules' ends on either side, into the margin (side shadows of the fill); nothing moves and no edge crosses
    text. A day's first entry, which has no rule above
    it, and its last, none below, take one while lit, drawn inside the box; the same tap again clears it, a tap on another thread moves it. The
    links (⟨⟨ and ⟩⟩) go where they go and leave the highlight as it is. It holds across the two halves and
    the reader for the session (sessionStorage), and is the reader's alone: nothing in the address.
 6. Each half's lede names the other ("The second calendar takes up at ..."); the words linked to its page's top.
 8. While a thread is lit and the scroll wheel is held (the headings showing), a mark for each of its lit entries, as a
    find-on-page bar marks its hits: in the highlight's color, no edge, the thumb's width, in the thumb's column, right
    of the headings. The thumb's travel stands for the page: a mark's place and height are the entry's place and
    height as shares of the page (at least one device pixel), so the thumb's centre on a mark brings the entry to the
    top, and the marks hold still while the page scrolls under the drag. One canvas, drawn once a drag (#hlmarks,
    SCRIPT), on a bar of their width the length of the thumb's travel, in a darker color (the canvas's background;
    --hlsh, --hla). Shown and gone with the headings.
"""
import datetime
import re

from . import store

# the half being built and the page kind, set by the build around each half
CUR = {"half": None, "mode": "list"}


def cfg(lst):
    s = (lst.data or {}).get("split") if lst is not None else None
    return s or None


def boundary(lst):
    s = cfg(lst)
    return str(s["from"]) if s else None


def page_key(lst, half):
    return lst.key if half == 1 else cfg(lst)["page"]


def half_of_date(lst, d):
    b = boundary(lst)
    if not b:
        return 1
    return 2 if str(d)[:10] >= b else 1


def half_of_section(lst, sec):
    """1 or 2; None for the threads section, which is in both."""
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
    """The list's top sections in the half, the threads section first."""
    return [s for s in lst.sections if half_of_section(lst, s) in (None, half)]


def half_of_entry(lst, sec, e):
    h = half_of_section(lst, sec)
    if h is None:
        return CUR["half"] or 1
    return h


def thread_anchor(lst, slug, half):
    return f"{lst.key}.thread.{slug}" if half != 2 else f"{cfg(lst)['page']}.thread.{slug}"


def href(lst, half, anchor):
    """A link to an anchor in a half: in the page itself, or the other page; in the reader always in the page."""
    if CUR["mode"] == "series" or half == CUR["half"]:
        return f"#{anchor}"
    return f"{page_key(lst, half)}.html#{anchor}"


def statement(lst, e, half, has_first):
    """The thread's statement in a half: the second half's own (c2) where the thread is in both."""
    if half == 2 and has_first and e.get("c2"):
        return e["c2"]
    return e.get("c")


# ---------------------------------------------------------------- the anchors of the second half

_ANCHORS = {}


def anchors(lst):
    """(first, second): the anchors each half's page holds of the list's own: entries, days, sections."""
    key = id(lst)
    if key in _ANCHORS:
        return _ANCHORS[key]
    first, second = set(), set()
    for sec in lst.sections:
        h = half_of_section(lst, sec)
        if h is None:
            continue
        bag = first if h == 1 else second

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
    _ANCHORS[key] = (first, second)
    return first, second


HREF = re.compile(r'href="([^"#]*)#([^"]+)"')


def route(page, lst, own):
    """Links to anchors that live on the other half's page: own is 1 or 2 for the calendar's pages (a bare '#X' whose X
    lives in the other half), None for any other page ('cal.html#X' whose X lives in the second half)."""
    if not cfg(lst):
        return page
    first, second = anchors(lst)
    p1, p2 = f"{lst.key}.html", f"{cfg(lst)['page']}.html"

    def sub(m):
        path, anchor = m.group(1), m.group(2)
        if own in (1, 2) and path == "":
            if own == 1 and anchor in second and anchor not in first:
                return f'href="{p2}#{anchor}"'
            if own == 2 and anchor in first and anchor not in second:
                return f'href="{p1}#{anchor}"'
            return m.group(0)
        if path.endswith(p1) and anchor in second and anchor not in first:
            return f'href="{path[:-len(p1)]}{p2}#{anchor}"'
        return m.group(0)
    return HREF.sub(sub, page)


# ---------------------------------------------------------------- a thread's dates

def thread_dates_html(lst, slug, members, esc):
    """The thread's dates in the half being built, by year, with the muted links across the divide (STYLE 1-2)."""
    half = CUR["half"]
    if half is None or not cfg(lst):
        mine, before, after = members, None, None
    else:
        mine = [m for m in members if half_of_date(lst, m["date"]) == half]
        others = [m for m in members if half_of_date(lst, m["date"]) != half]
        before = others[-1] if half == 2 and others else None
        after = others[0] if half == 1 and others else None
    other = 2 if half == 1 else 1

    def cross(m):
        y = str(m["date"])[:4]
        return (f'<a class="tx ty" href="{href(lst, other, thread_anchor(lst, slug, other))}">{y}</a> '
                f'<a class="tx" href="{href(lst, other, m["id"])}">{esc(m["when"])}</a>')
    groups, prev = [], None
    for m in mine:
        y = str(m["date"])[:4]
        link = f'<a href="{href(lst, half or 1, m["id"])}">{esc(m["when"])}</a>'
        if y != prev:
            groups.append([f'<b class="ty">{y}</b>', [link]])
            prev = y
        else:
            groups[-1][1].append(link)
    parts = [f"{y} " + ", ".join(ls) for y, ls in groups]
    if before:
        parts.insert(0, cross(before))
    if after:
        parts.append(cross(after))
    # a full stop after each year's dates; none added after a date that ends in one ("Dec.")
    stop = lambda t: t if re.sub(r"<[^>]+>", "", t).endswith(".") else t + "."
    return " ".join(stop(t) for t in parts)


def seam(lst, sec):
    """(before, after): the links across the divide at the head of the second half's first day and the foot of the
    first half's last ("‹ Jan. 2, 1963, in the first calendar"; "Jan. 3, 1963, in the second calendar ›")."""
    if not cfg(lst) or not sec.extra.get("from"):
        return "", ""
    b = datetime.date.fromisoformat(boundary(lst))
    last = (b - datetime.timedelta(days=1)).isoformat()
    lab = lambda d: f"{MON[d.month - 1]} {d.day}, {d.year}"
    before = after = ""
    if str(sec.extra["from"]) == b.isoformat():
        before = (f'<p class="seam"><a href="{href(lst, 1, "d" + last)}">‹ {lab(b - datetime.timedelta(days=1))}, '
                  f'in the first calendar</a></p>')
    if str(sec.extra.get("to")) == last:
        after = (f'<p class="seam"><a href="{href(lst, 2, "d" + b.isoformat())}">{lab(b)}, in the second calendar ›'
                 f'</a></p>')
    return before, after


def other_link(lst, html):
    """In a half's lede, "the second calendar" (or "the first") linked to the top of the other half's page, or of its
    block in the reader (STYLE 6)."""
    half = CUR["half"]
    if not cfg(lst) or half not in (1, 2):
        return html
    other = 2 if half == 1 else 1
    word = "second" if other == 2 else "first"
    key = page_key(lst, other)
    u = f"#{key}--top" if CUR["mode"] == "series" else f"{key}.html"
    return html.replace(f"{word} calendar", f'<a href="{u}">{word} calendar</a>', 1)


MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]

STYLE = """<style>
/* the thread index's years and the links across the calendar's halves (tools/bib/calsplit.py) */
.ty{font-family:var(--sans);font-weight:600;font-size:.92em}
a.tx{color:var(--muted);text-decoration-color:var(--rule)}
a.tx.ty{text-decoration:none}
a.tx.ty:hover{text-decoration:underline;text-decoration-color:var(--rule)}
p.seam{font-family:var(--sans);font-size:.8rem;margin:1rem 0}
p.seam a{color:var(--muted);text-decoration-color:var(--rule)}
/* a thread highlighted (STYLE 7) */
:root{--hl:#FFFFFF;--hlsh:120,132,150;--hla:.4}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--hl:#22262E;--hlsh:0,0,0;--hla:.4}}
:root[data-theme="dark"]{--hl:#22262E;--hlsh:0,0,0;--hla:.4}

li[data-thread],.tnl[data-t]{cursor:pointer}
#hlmarks{position:fixed;z-index:27;right:6px;width:28px;pointer-events:none;opacity:0;transition:opacity .18s;background:rgba(var(--hlsh),var(--hla))}
#hlmarks.on{opacity:1}
@media (prefers-reduced-motion: reduce){#hlmarks{transition:none}}
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
    if(ev.target.closest('a,button,summary,input')) return;
    var el=ev.target.closest('li[data-thread],.tnl[data-t]'); if(!el) return;
    var t=el.dataset.thread||el.dataset.t; if(!/^[a-z0-9-]+$/.test(t)) return;
    now = (now===t) ? '' : t; set(now);
  });
  /* while the scroll wheel is held, a mark for each lit entry, fixed at the right, right of the headings: at the
     thumb's place that brings the entry to the top (STYLE 8) */
  var peek=document.getElementById('peek'), rail=document.getElementById('rail'), thumb=document.getElementById('thumb');
  if(!peek||!rail||!thumb) return;
  var box=document.createElement('canvas'); box.id='hlmarks'; box.setAttribute('aria-hidden','true'); document.body.appendChild(box);
  function marks(){
    if(!now||!peek.classList.contains('on')) return;
    var rr=rail.getBoundingClientRect(), th=thumb.offsetHeight, track=rail.clientHeight-th, dpr=window.devicePixelRatio||1,
        sh=document.documentElement.scrollHeight, k=track/sh, ys=[], i, r;
    box.style.top=rr.top+'px'; box.style.height=rr.height+'px';
    box.width=Math.round(28*dpr); box.height=Math.round(rr.height*dpr);
    var els=document.querySelectorAll('li[data-threads~="'+now+'"],li[data-thread="'+now+'"]');
    for(i=0;i<els.length;i++){ r=els[i].getBoundingClientRect(); if(r.height) ys.push(r.top+window.scrollY, r.height); }
    var cs=getComputedStyle(document.documentElement), g=box.getContext('2d'),
        least=Math.max(1,Math.round((parseFloat(cs.getPropertyValue('--hlmin'))||0)*dpr));   // the least height, device pixels
    var ink=cs.getPropertyValue('--hlmark').trim()||cs.getPropertyValue('--hl').trim()||'#fff',
        halo=cs.getPropertyValue('--hlhalo').trim(), hp=Math.round((parseFloat(cs.getPropertyValue('--hlhalow'))||0)*dpr);
    g.fillStyle=ink;
    for(i=0;i<ys.length;i+=2){           // the entry's share of the page, as its share of the thumb's travel; at least `least`
      var y0=(th/2+ys[i]*k)*dpr, y1=y0+ys[i+1]*k*dpr, a=Math.floor(y0), h=Math.round(y1)-a;
      if(h<least){ a=Math.round((y0+y1)/2-least/2); h=least; }      // fattened about the entry's middle
      if(halo){ g.fillStyle=halo; g.fillRect(0,a-hp,box.width,h+2*hp); g.fillStyle=ink; }
      g.fillRect(0,a,box.width,h);
    }
  }
  new MutationObserver(function(){ box.classList.toggle('on',!!now&&peek.classList.contains('on')); marks(); })
    .observe(peek,{attributes:true,attributeFilter:['class']});
})();
</script>"""
