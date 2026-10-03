"""The day's executive documents: one page per calendar month, every day under its own heading.

    daybook/<YYYY-MM>.yaml   every Public Papers (APP) and FRUS document dated that month, in order;
                             made by tools/daybook/make_daybook.py, which see
    daybook/abstracts.yaml   {key: one-sentence abstract}, kept apart so the generator never touches it

Each day: the New York Times for that date in TimesMachine (a link by date, nothing read); the
calendar entries that open on it; the President's documents; the FRUS documents. build/days.html
lists the months, and each calendar month links to its page.

STYLE:
 1. Line: author, title (linked to the text), source in grey. Author is the source's own: the President
    for APP; for FRUS the sender in the heading, else the drafter in the source note, else none.
 2. FRUS citation "FRUS 1961–63, XIV, doc. 177"; the volume's title on hover; a time of day in grey
    where the document gives one; a dated range as "through Mar. 9"; an editorial note filed by its
    place in the volume says so.
 3. An abstract, where there is one, on its own line under the title: one sentence, the brief's
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
TM = "https://timesmachine.nytimes.com/timesmachine/{y}/{m:02d}/{d:02d}/issue.html"
# No New York Times was published during the New York newspaper strike.
NO_TIMES = (datetime.date(1962, 12, 8), datetime.date(1963, 3, 31))


def esc(t):
    return html.escape(str(t), quote=True)


def load():
    docs = []
    for f in sorted(glob.glob(os.path.join(DIR, "[0-9][0-9][0-9][0-9]-[0-9][0-9].yaml"))):
        docs += (yaml.safe_load(open(f, encoding="utf-8")) or {}).get("docs", [])
    ab = {}
    p = os.path.join(DIR, "abstracts.yaml")
    if os.path.exists(p):
        ab = yaml.safe_load(open(p, encoding="utf-8")) or {}
    return docs, ab


def day_label(d, year=True):
    return f"{MON[d.month - 1]} {d.day}" + (f", {d.year}" if year else "")


def span(a, b):
    if a == b:
        return day_label(a, False)
    if (a.year, a.month) == (b.year, b.month):
        return f"{day_label(a, False)}–{b.day}"
    return f"{day_label(a, False)}–{day_label(b, a.year != b.year)}"


def page_name(month):
    return f"days-{month}.html"


def pages(series):
    """[(month, first day, last day, [calendar sections])] from the calendar's dated sections."""
    out = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec in lst.sections:
            if not (sec.extra.get("from") and sec.extra.get("to")):
                continue
            lo = datetime.date.fromisoformat(str(sec.extra["from"]))
            hi = datetime.date.fromisoformat(str(sec.extra["to"]))
            m = f"{lo.year}-{lo.month:02d}"
            a = out.setdefault(m, [lo, hi, []])
            a[0], a[1] = min(a[0], lo), max(a[1], hi)
            a[2].append((lst, sec))
    return [(m, v[0], v[1], v[2]) for m, v in sorted(out.items())]


def cal_entries(series):
    by_day = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            d = str(e.get("date", ""))
            if len(d) == 10:
                by_day.setdefault(d, []).append((lst, e))
    return by_day


def thread_name(lst, slug):
    for sec, e in lst.entries():
        if e.get("id") == f"{lst.key}.thread.{slug}":
            return e.get("s") or slug
    return slug


def doc_html(x, ab):
    title = f'<a href="{esc(x["url"])}">{esc(x["title"])}</a>'
    au = f'<span class="au">{esc(x["author"])}</span> ' if x.get("author") else ""
    if x["src"] == "ppp":
        src = "APP"
        hover = "American Presidency Project"
    else:
        src = x["cite"]
        hover = x.get("vol", "")
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


def day_html(d, docs, cal, ab, series):
    iso = d.isoformat()
    out = [f'<h2 id="d{iso}" data-short="{esc(day_label(d, False))}">{calendar.day_name[d.weekday()]}, {esc(day_label(d))}</h2>']
    meta = []
    if NO_TIMES[0] <= d <= NO_TIMES[1]:
        meta.append("No <i>New York Times</i>: the New York newspaper strike, Dec. 8, 1962–Mar. 31, 1963.")
    else:
        meta.append(f'<i>New York Times</i>: <a href="{TM.format(y=d.year, m=d.month, d=d.day)}">TimesMachine, {esc(day_label(d))}</a>.')
    if cal:
        links = []
        for lst, e in cal:
            name = thread_name(lst, e.get("thread", "")) if e.get("thread") else ""
            links.append(f'<a href="{lst.key}.html#{esc(e["id"])}">{esc(e.get("when", ""))}{" (" + esc(name) + ")" if name else ""}</a>')
        meta.append("In the calendar: " + "; ".join(links) + ".")
    out.append('<p class="dmeta">' + " ".join(meta) + "</p>")
    ppp = [x for x in docs if x["src"] == "ppp"]
    frus = [x for x in docs if x["src"] == "frus"]
    if ppp:
        out.append('<h3 class="dk">The President</h3><ol class="dd">' + "".join(doc_html(x, ab) for x in ppp) + "</ol>")
    if frus:
        out.append(f'<h3 class="dk">Foreign Relations of the United States ({len(frus)})</h3><ol class="dd">'
                   + "".join(doc_html(x, ab) for x in frus) + "</ol>")
    if not docs:
        out.append('<p class="dmeta">No document in either series.</p>')
    return "\n".join(out)


STYLE = """<style>
h2[id^="d1"]{font-family:var(--sans);font-size:1.05rem;margin:2rem 0 .3rem;padding-top:.6rem;border-top:1px solid var(--rule)}
p.dmeta{font-family:var(--sans);font-size:.85rem;color:var(--muted);margin:.2rem 0 .5rem}
h3.dk{font-family:var(--sans);font-size:.75rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);font-weight:600;margin:.7rem 0 .2rem;border:0;padding:0}
ol.dd{list-style:none;margin:0;padding:0;font-family:var(--sans);font-size:.85rem;line-height:1.4}
ol.dd li{padding:.22rem 0;border-bottom:1px solid var(--rule)}
ol.dd .au{font-weight:600}
ol.dd .src{color:var(--muted);margin-left:.3rem}
ol.dd .ab{display:block;font-family:var(--serif);font-size:.95rem;color:var(--note);margin-top:.1rem}
nav.mo{font-family:var(--sans);font-size:.85rem;margin:.5rem 0 1rem}
nav.mo a{margin-right:1rem}
</style>"""


def lede(n_ppp, n_frus, n_ab):
    return ('<p class="lede">Every presidential document and every document in <i>Foreign Relations of the United States</i> '
            'dated this month, filed under its date, with the day\'s <i>New York Times</i>.</p>'
            '<p class="logic">The President: the American Presidency Project\'s documents by date (Public Papers items, '
            'executive orders, proclamations). FRUS: every volume of the 1958–60 and 1961–63 subseries, microfiche '
            'supplements included, from the Office of the Historian\'s files; an undated editorial note is filed under the '
            'document before it. Titles are the sources\'; authors are the sender in the heading or the drafter in the source '
            'note. The <i>Times</i> link opens that day\'s paper in TimesMachine (subscription). '
            f'This month: {n_ppp} presidential, {n_frus} FRUS'
            + (f'; {n_ab} with abstracts' if n_ab else '') + '. Data: daybook/ in the repository.</p>')


def build(series, template):
    """{filename: html} for every month page and the index."""
    docs, ab = load()
    if not docs:
        return {}
    by_day = {}
    for x in docs:
        by_day.setdefault(x["date"], []).append(x)
    cal = cal_entries(series)
    tpl = open(template, encoding="utf-8").read()
    pg = pages(series)
    out, index = {}, []
    for i, (m, lo, hi, secs) in enumerate(pg):
        y, mo = int(m[:4]), int(m[5:7])
        name = f"{calendar.month_name[mo]} {y}"
        main = [f"<h1>Day by day: {esc(name)}</h1>"]
        days = [lo + datetime.timedelta(days=k) for k in range((hi - lo).days + 1)]
        mdocs = [x for d in days for x in by_day.get(d.isoformat(), [])]
        n_ppp = sum(x["src"] == "ppp" for x in mdocs)
        n_frus = len(mdocs) - n_ppp
        n_ab = sum(1 for x in mdocs if x["key"] in ab)
        main.append(lede(n_ppp, n_frus, n_ab))
        nav = ['<a href="days.html">All months</a>']
        if i > 0:
            nav.append(f'<a href="{page_name(pg[i - 1][0])}">← {esc(calendar.month_abbr[int(pg[i - 1][0][5:])])} {pg[i - 1][0][:4]}</a>')
        if i + 1 < len(pg):
            nav.append(f'<a href="{page_name(pg[i + 1][0])}">{esc(calendar.month_abbr[int(pg[i + 1][0][5:])])} {pg[i + 1][0][:4]} →</a>')
        nav.append(f'<a href="cal.html#{esc(secs[0][1].id)}">The calendar</a>')
        main.append('<nav class="mo">' + "".join(nav) + "</nav>")
        main.append('<nav class="toc" aria-label="Contents">\n<h3 id="contents" style="border-top:0;margin-top:1.5rem" data-short="Contents">Contents</h3>\n<ol id="tocList"></ol>\n</nav>')
        for d in days:
            main.append(day_html(d, by_day.get(d.isoformat(), []), cal.get(d.isoformat(), []), ab, series))
        main.append('<nav class="mo">' + "".join(nav) + "</nav>")
        page = tpl.replace("{{page_title}}", f"Day by day: {name}").replace("{{main}}", "\n".join(main))
        out[page_name(m)] = page.replace("</head>", STYLE + "\n</head>", 1)
        index.append(f'<li><a href="{page_name(m)}">{esc(name)}</a> <span class="src">{n_ppp} presidential, {n_frus} FRUS</span></li>')
    main = ["<h1>Day by day, January 1961–January 3, 1963</h1>", lede(sum(x["src"] == "ppp" for x in docs),
            sum(x["src"] == "frus" for x in docs), sum(1 for x in docs if x["key"] in ab)).replace("dated this month", "dated in the calendar's span").replace("This month", "In all"),
            '<ol class="dd">' + "".join(index) + "</ol>"]
    page = tpl.replace("{{page_title}}", "Day by day").replace("{{main}}", "\n".join(main))
    out["days.html"] = page.replace("</head>", STYLE + "\n</head>", 1)
    return out


def inject(page, series, mode):
    """Under each calendar month's heading, a link to that month's day-by-day page."""
    docs, _ = load()
    if not docs:
        return page
    for m, lo, hi, secs in pages(series):
        for lst, sec in secs:
            a = datetime.date.fromisoformat(str(sec.extra["from"]))
            b = datetime.date.fromisoformat(str(sec.extra["to"]))
            n = sum(1 for x in docs if a.isoformat() <= x["date"] <= b.isoformat())
            link = (f'<p class="logic">Day by day: <a href="{page_name(m)}#d{a.isoformat()}">the President\'s papers, '
                    f'FRUS, and the <i>Times</i>, {esc(span(a, b))}</a> ({n} documents).</p>')
            hid = f"{lst.key}--{sec.id}" if mode == "series" else sec.id
            pat = re.compile(r'(<h\d id="' + re.escape(hid) + r'"[^>]*>.*?</h\d>)', re.S)
            page = pat.sub(lambda mm: mm.group(1) + "\n" + link, page, count=1)
    return page


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
