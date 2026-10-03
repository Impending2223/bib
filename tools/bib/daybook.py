"""The calendar by day: every day of each month, its entries, the day's Times, and its documents.

    daybook/<YYYY-MM>.yaml   every Public Papers (APP) and FRUS document dated that month, in order;
                             made by tools/daybook/make_daybook.py, which see
    daybook/abstracts.yaml   {key: one-sentence abstract}, kept apart so the generator never touches it

Each dated section of the calendar is laid out by day (section_days): the month's undated entries
first, then every day from the section's first to its last, each with its date, a link to that
day's New York Times under it, the entries that open that day, a pointer to any entry still running
from an earlier day, and the day's documents in a list that opens and closes ("Expand all" and
"Collapse all" under each month heading).

STYLE:
 1. Day: "Monday, Apr. 17", bold sans; "New York Times" under it, muted, linked to that day's paper
    (by date only); during the newspaper strike, "No New York Times (strike)".
 2. Entry: the thread as a rubric on its own line above the first line, muted small capitals in sans;
    other threads after a middle dot; a range or a month-only date after a comma ("Cuba, Apr.
    15–19"). The day's own date is not repeated (it shows in link previews and search).
 3. A ranged entry is filed under its first day; each later day of the range carries a muted
    "Continuing" line linking back to it.
 4. Document line: author, title (linked to the text), source in grey. Author is the source's own:
    the President for APP; for FRUS the sender in the heading, else the drafter in the source note,
    else none. FRUS citation "FRUS 1961–63, XIV, doc. 177"; the volume's title on hover; a time of
    day in grey where the document gives one; "through Mar. 9" for a dated range; an editorial note
    filed by its place in the volume says so.
 5. An abstract, where there is one, on its own line under the title: one sentence, the brief's
    register (what the document is and says; no judgment).
"""
import calendar
import datetime
import glob
import html
import os
import re

import yaml

from . import store

DIR = os.path.join(store.ROOT, "daybook")
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
MON_RE = {m.rstrip("."): i + 1 for i, m in enumerate(MON)}
MON_RE["Sept"] = 9
TM = "https://timesmachine.nytimes.com/timesmachine/{y}/{m:02d}/{d:02d}/issue.html"
# No New York Times was published during the New York newspaper strike.
NO_TIMES = (datetime.date(1962, 12, 8), datetime.date(1963, 3, 31))

_cache = {}


def esc(t):
    return html.escape(str(t), quote=True)


def load():
    if "docs" not in _cache:
        docs = []
        for f in sorted(glob.glob(os.path.join(DIR, "[0-9][0-9][0-9][0-9]-[0-9][0-9].yaml"))):
            docs += (yaml.safe_load(open(f, encoding="utf-8")) or {}).get("docs", [])
        ab = {}
        p = os.path.join(DIR, "abstracts.yaml")
        if os.path.exists(p):
            ab = yaml.safe_load(open(p, encoding="utf-8")) or {}
        by_day = {}
        for x in docs:
            by_day.setdefault(x["date"], []).append(x)
        _cache.update(docs=docs, ab=ab, by_day=by_day)
    return _cache["docs"], _cache["ab"]


def day_label(d, year=True):
    return f"{MON[d.month - 1]} {d.day}" + (f", {d.year}" if year else "")


# ---------------------------------------------------------------- entries

def end_of(e):
    """Last day of a calendar entry, from its date and its "when" ("Apr. 15–19", "Apr. 30–May 2")."""
    d = str(e.get("date", ""))
    if len(d) != 10:
        return None
    start = datetime.date.fromisoformat(d)
    m = re.search(r"–\s*(?:([A-Z][a-z]+)\.?\s+)?(\d{1,2})\s*$", e.get("when", ""))
    if not m:
        return start
    mo = MON_RE.get(m.group(1), start.month) if m.group(1) else start.month
    y = start.year + (1 if mo < start.month else 0)
    try:
        end = datetime.date(y, mo, int(m.group(2)))
    except ValueError:
        return start
    return end if end >= start else start


def rubric(lst, e, thread_name):
    """The thread (and others after a middle dot), with the date when it is not simply the day's."""
    if "when" not in e or not e.get("thread"):
        return ""
    names = [thread_name(lst, t) for t in [e["thread"]] + e.get("also", [])]
    d = str(e.get("date", ""))
    single = len(d) == 10 and end_of(e) == datetime.date.fromisoformat(d)
    when = (f'<span class="rw same">, {esc(e["when"])}</span>' if single
            else f'<span class="rw">, {esc(e["when"])}</span>')
    return f'<span class="s rub">{" · ".join(esc(n) for n in names)}{when}</span>'


# ---------------------------------------------------------------- documents

def doc_html(x, ab):
    title = f'<a href="{esc(x["url"])}">{esc(x["title"])}</a>'
    au = f'<span class="au">{esc(x["author"])}</span> ' if x.get("author") else ""
    if x["src"] == "ppp":
        src, hover = "APP", "American Presidency Project"
    else:
        src, hover = x["cite"], x.get("vol", "")
    bits = [f'<span class="src" title="{esc(hover)}">{esc(src)}</span>']
    if x.get("time"):
        bits.append(f'<span class="src">{esc(x["time"])}</span>')
    if x.get("until"):
        u = datetime.date.fromisoformat(x["until"])
        bits.append(f'<span class="src">through {esc(day_label(u, u.year != int(x["date"][:4])))}</span>')
    if x.get("placed"):
        bits.append('<span class="src">filed by its place in the volume</span>')
    a = ab.get(x["key"])
    abstract = f'<span class="ab">{esc(a)}</span>' if a else ""
    return f'<li>{au}{title} {" ".join(bits)}{abstract}</li>'


def docs_html(docs, ab):
    if not docs:
        return ""
    ppp = [x for x in docs if x["src"] == "ppp"]
    frus = [x for x in docs if x["src"] == "frus"]
    counts = []
    if ppp:
        counts.append(f"the President {len(ppp)}")
    if frus:
        counts.append(f"FRUS {len(frus)}")
    body = []
    if ppp:
        body.append('<ol class="dd">' + "".join(doc_html(x, ab) for x in ppp) + "</ol>")
    if frus:
        body.append('<ol class="dd fr">' + "".join(doc_html(x, ab) for x in frus) + "</ol>")
    return (f'<details class="docs"><summary>Documents: {", ".join(counts)}</summary>'
            + "".join(body) + "</details>")


# ---------------------------------------------------------------- a month, by day

def section_days(lst, sec, entry_li, thread_name):
    """HTML for a dated calendar section, laid out by day. entry_li(e, rubric_html) -> '<li ...>'."""
    docs, ab = load()
    by_day = _cache["by_day"]
    lo = datetime.date.fromisoformat(str(sec.extra["from"]))
    hi = datetime.date.fromisoformat(str(sec.extra["to"]))
    out = ['<p class="dtog"><button type="button" data-docs="1">Expand all</button>'
           '<button type="button" data-docs="0">Collapse all</button> <span>the day\'s documents</span></p>']
    undated = [e for e in sec.entries if "when" not in e or len(str(e.get("date", ""))) != 10]
    dated = {}
    running = {}
    for e in sec.entries:
        if "when" not in e or len(str(e.get("date", ""))) != 10:
            continue
        start = datetime.date.fromisoformat(str(e["date"]))
        dated.setdefault(start, []).append(e)
        end = end_of(e)
        k = start + datetime.timedelta(days=1)
        while k <= min(end, hi):
            running.setdefault(k, []).append(e)
            k += datetime.timedelta(days=1)
    if undated:
        out.append(f'<div class="day mo"><div class="dh"><span class="dn">{esc(calendar.month_name[lo.month])}</span></div>'
                   '<ol class="e">' + "".join(entry_li(e, rubric(lst, e, thread_name)) for e in undated) + "</ol></div>")
    d = lo
    while d <= hi:
        iso = d.isoformat()
        h = [f'<div class="day" id="d{iso}"><div class="dh" role="heading" aria-level="4">'
             f'<span class="dn">{calendar.day_name[d.weekday()]}, {esc(day_label(d, d.year != lo.year))}</span>']
        if NO_TIMES[0] <= d <= NO_TIMES[1]:
            h.append('<span class="tm">No <i>New York Times</i> (strike)</span>')
        else:
            h.append(f'<a class="tm" href="{TM.format(y=d.year, m=d.month, d=d.day)}"><i>New York Times</i></a>')
        h.append("</div>")
        if d in dated:
            h.append('<ol class="e">' + "".join(entry_li(e, rubric(lst, e, thread_name)) for e in dated[d]) + "</ol>")
        if d in running:
            h.append('<p class="cont">Continuing: ' + "; ".join(
                f'<a href="#{esc(e["id"])}">{esc(thread_name(lst, e["thread"]))}, {esc(e["when"])}</a>'
                for e in running[d]) + "</p>")
        h.append(docs_html(by_day.get(iso, []), ab))
        h.append("</div>")
        out.append("".join(h))
        d += datetime.timedelta(days=1)
    return out


STYLE = """<style>
.day{padding:.55rem 0 .35rem;border-top:1px solid var(--rule)}
.day .dh{display:flex;flex-direction:column;font-family:var(--sans);line-height:1.3}
.day .dn{font-weight:700;font-size:.92rem}
.day .tm{font-size:.78rem;color:var(--muted);margin-top:.05rem}
.day a.tm{color:var(--muted);text-decoration-color:var(--rule)}
.day ol.e>li{padding:.45rem 0;border-bottom:0}
.day ol.e>li+li{border-top:1px dotted var(--rule)}
.s.rub{display:block;font-family:var(--sans);font-size:.7rem;font-weight:600;letter-spacing:.06em;
  text-transform:uppercase;color:var(--muted);margin:0 0 .1rem}
.s.rub .rw{letter-spacing:.02em}
.day .rw.same{display:none}
#pv .rw.same{display:inline}
p.cont{font-family:var(--sans);font-size:.8rem;color:var(--muted);margin:.25rem 0}
p.cont a{color:var(--muted)}
details.docs{font-family:var(--sans);font-size:.8rem;margin:.25rem 0 .1rem}
details.docs>summary{cursor:pointer;color:var(--muted);list-style-position:inside}
details.docs[open]>summary{margin-bottom:.25rem}
ol.dd{list-style:none;margin:0;padding:0;line-height:1.4}
ol.dd li{padding:.18rem 0;border-bottom:1px solid var(--rule)}
ol.dd.fr{margin-top:.4rem}
ol.dd .au{font-weight:600}
ol.dd .src{color:var(--muted);margin-left:.3rem}
ol.dd .ab{display:block;font-family:var(--serif);font-size:.95rem;color:var(--note);margin-top:.1rem}
p.dtog{font-family:var(--sans);font-size:.78rem;color:var(--muted);margin:.4rem 0 .6rem}
p.dtog button{font:inherit;font-weight:600;border:1px solid var(--rule);background:var(--panel);color:var(--ink);
  border-radius:6px;padding:.2rem .55rem;margin-right:.35rem;cursor:pointer}
</style>"""

SCRIPT = """<script>
document.addEventListener('click',function(ev){
  var b=ev.target.closest&&ev.target.closest('p.dtog button');
  if(!b) return;
  var open=b.getAttribute('data-docs')==='1';
  [].forEach.call(document.querySelectorAll('details.docs'),function(d){d.open=open;});
  window.dispatchEvent(new Event('resize'));
});
// headings move when a list opens or closes: let the outline and breadcrumb re-measure
document.addEventListener('toggle',function(ev){
  if(ev.target.matches&&ev.target.matches('details.docs')){
    clearTimeout(window.__dbT); window.__dbT=setTimeout(function(){window.dispatchEvent(new Event('resize'));},50);
  }
},true);
</script>"""


def inject(page):
    """The styles and the expand/collapse script, where the page has days."""
    if 'class="day' not in page:
        return page
    page = page.replace("</head>", STYLE + "\n</head>", 1)
    return page.replace("</body>", SCRIPT + "\n</body>", 1)


def problems():
    """For ./bib check: duplicate keys, malformed dates, abstracts for documents not in the daybook."""
    docs, ab = load()
    out, seen = [], set()
    for x in docs:
        k = x.get("key")
        if k in seen:
            out.append((k, "daybook: duplicate document key"))
        seen.add(k)
        try:
            datetime.date.fromisoformat(x["date"])
        except Exception:
            out.append((k, f"daybook: bad date {x.get('date')!r}"))
    for k in ab:
        if k not in seen:
            out.append((k, "daybook: abstract for a document not in daybook/"))
    return out
