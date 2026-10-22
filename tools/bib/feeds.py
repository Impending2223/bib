"""The White House recordings the Miller Center gives free, as podcast feeds: an RSS 2.0 feed a month, each recording
an item dated by the recording, in date order; and the page that lists the feeds and the ebooks (build/ebooks.html).

    daybook/recordings/millercenter.yaml   the Miller Center's recordings: page, audio, date, time, tape, citation
                             (tools/daybook/make_millercenter.py, from its public JSON:API)
    daybook/recordings/<YYYY-MM>.yaml      PRDE's catalogue: title, speakers, place, length, tape cite
                             (tools/daybook/make_recordings.py); joined to the Miller Center's by daybook.free
    build/feeds/recordings-<YYYY-MM>.xml   written by `./bib build feeds` (and the full build), with
    build/feeds/recordings.opml            every feed, to subscribe to all at once
    build/ebooks.html                      the books (tools/bib/ebooks.py) and the feeds, listed by year

STYLE:
 1. Accessible only: a recording is an item where the Miller Center gives it free (its page and its audio file). One
    PRDE alone catalogues is left out (its audio and transcript are the Edition's, by subscription), counted on the
    page. Machine noise and blank tape are left out, as in the daybook (daybook.NOISE).
 2. A feed a month: 1 to 559 items (Aug. 1964), within what podcast apps and feed readers take in one feed; a year
    would run to 3,645 (1964), which many apps cut short or load slowly. The OPML lists every month's feed. 7,545
    items in 70 feeds, July 1962 to Jan. 1969; 335 PRDE-only recordings left out (Oct. 22, 2026).
 3. An item: its title PRDE's where PRDE catalogues the recording ("Lyndon Johnson and George Reedy"), else the
    Miller Center's in title case (daybook.mc_title); the link the Miller Center's page; the enclosure its audio file,
    linked, never copied (audio/mpeg; length "0", the size not known without fetching each file); the guid the
    series' own key ("bib:mc:6252", "bib:prde:9080110"), not a link, so a moved page leaves it the same.
 4. The date: the recording's day and time as the catalogue gives it (PRDE's time, else the Miller Center's), taken as
    Washington time, Eastern, with the tz database's offset for that day (zoneinfo America/New_York: daylight time
    from the last Sunday of April to the last Sunday of October in these years); a recording without a time at noon
    Eastern. A recording made away from Washington (the LBJ Ranch, in Central time) is not adjusted. RFC 822.
 5. The description: catalogue data only, plain text: the date and time; PRDE's speakers, place and length; the tape
    cite; the Miller Center's title; PRDE's page, marked by subscription; the day in the calendar. No transcript, no
    summary: PRDE's are the Edition's text, and the Miller Center's summaries are the Library's (not taken).
 6. Order: the items in date and time order in the file, and numbered (itunes:episode) in that order, the feed typed
    serial (itunes:type), so an app lists them oldest first. The itunes tags only for the enclosures' sake.
 7. The page: a table a year of the books (month, documents, size) and of the feeds (month, recordings); how to
    subscribe; the sources and their terms. Each calendar page names its months' feeds in its head (link
    rel=alternate) and points to the page under its lede (`inject`).
"""
import datetime
import email.utils
import html
import os
import re

from . import calsplit, daybook, ebooks, store

SITE = ebooks.SITE
OUT = os.path.join(store.ROOT, "build", "feeds")
PAGE = "ebooks.html"


def esc(t):
    return html.escape(str(t), quote=True)


def text(t):
    return html.escape(str(t), quote=False)


def feed_name(month):
    return f"recordings-{month}.xml"


try:
    from zoneinfo import ZoneInfo
    EASTERN = ZoneInfo("America/New_York")
except Exception:                       # noqa: BLE001  (no tz database: the rule of these years, STYLE 4)
    EASTERN = None


def _last_sunday(y, m):
    d = datetime.date(y, m + 1, 1) - datetime.timedelta(days=1)
    return d - datetime.timedelta(days=(d.weekday() + 1) % 7)


def eastern(date, time):
    """The aware datetime of a recording (STYLE 4)."""
    h, mi = (int(time[:2]), int(time[3:5])) if time and re.match(r"\d\d:\d\d", time) else (12, 0)
    d = datetime.date.fromisoformat(date)
    naive = datetime.datetime(d.year, d.month, d.day, h, mi)
    if EASTERN is not None:
        return naive.replace(tzinfo=EASTERN)
    dst = _last_sunday(d.year, 4) <= d < _last_sunday(d.year, 10)
    return naive.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=-4 if dst else -5)))


def time_label(t):
    h, m = int(t[:2]), t[3:5]
    return f"{(h - 1) % 12 + 1}:{m} {'a.m.' if h < 12 else 'p.m.'}"


def items():
    """Every accessible recording (STYLE 1), in date and time order: [{key, date, time, title, link, audio, ...}]."""
    docs, _ = daybook.load()
    out = []
    for i, x in enumerate(docs):
        if x.get("src") == "prde" and x.get("free"):
            y = x["free"]
            out.append({"key": x["key"], "date": x["date"], "time": x.get("time") or y.get("time"),
                        "title": x["title"], "link": y["url"], "audio": y.get("audio"), "mc": y["title"],
                        "speakers": x.get("speakers") or [], "place": x.get("place"), "duration": x.get("duration"),
                        "cite": x.get("tape"), "prde": x.get("url"), "i": i})
        elif x.get("src") == "mc":
            out.append({"key": x["key"], "date": x["date"], "time": x.get("time"), "title": x["title"],
                        "link": x["url"], "audio": x.get("audio"), "mc": None, "speakers": [], "place": None,
                        "duration": None, "cite": daybook.mc_cite(x), "prde": None, "i": i})
    out = [x for x in out if x["audio"] and x["link"]]
    out.sort(key=lambda x: (x["date"], x["time"] or "12:00", x["i"]))
    return out


def prde_only():
    docs, _ = daybook.load()
    return sum(1 for x in docs if x.get("src") == "prde" and not x.get("free"))


def by_month():
    out = {}
    for x in items():
        out.setdefault(x["date"][:7], []).append(x)
    return dict(sorted(out.items()))


def _stop(t):
    return t if t.endswith(".") else t + "."


def description(x, cal):
    d = datetime.date.fromisoformat(x["date"])
    bits = [daybook.day_label(d) + (f", {time_label(x['time'])}" if x["time"] else "") + "."]
    if x["speakers"]:
        bits.append(_stop("Speakers (PRDE): " + "; ".join(x["speakers"])))
    if x["place"]:
        bits.append(_stop(x["place"]))
    if x["duration"]:
        bits.append(f"Length: {x['duration']}.")
    if x["cite"]:
        bits.append(_stop(x["cite"]))
    if x["mc"] and daybook.mc_title(x["mc"]) != x["title"]:
        bits.append(_stop(f"Miller Center: {daybook.mc_title(x['mc'])}"))
    bits.append(f"Free page and audio: the Miller Center, {x['link']}")
    if x["prde"]:
        bits.append(f"PRDE's catalogue (transcript by subscription): {x['prde']}")
    if cal.get(x["date"]):
        bits.append(f"The day in the calendar: {cal[x['date']]}")
    return " ".join(bits)


def feed(month, xs, cal, now):
    label = ebooks.month_label(month)
    self_url = f"{SITE}feeds/{feed_name(month)}"
    out = ['<?xml version="1.0" encoding="utf-8"?>',
           '<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" '
           'xmlns:atom="http://www.w3.org/2005/Atom">', "<channel>",
           f"<title>White House recordings, {esc(label)}</title>",
           f"<link>{esc(SITE + PAGE)}#rec-{month}</link>",
           f'<atom:link href="{esc(self_url)}" rel="self" type="application/rss+xml"/>',
           f"<description>The White House recordings of {esc(label)} that the Miller Center (University of "
           "Virginia, Secret White House Tapes) gives free, a recording an item, dated by the recording and in date "
           "order: the free page and the audio file, linked; PRDE's catalogue data where it catalogues the recording. "
           f"Catalogue data only, no transcripts. From the 1968 series ({esc(SITE)}).</description>",
           "<language>en-us</language>",
           f"<lastBuildDate>{email.utils.format_datetime(now)}</lastBuildDate>",
           "<generator>The 1968 series, tools/bib/feeds.py</generator>",
           "<itunes:author>The 1968 series</itunes:author>",
           "<itunes:type>serial</itunes:type>",
           "<itunes:explicit>false</itunes:explicit>",
           '<itunes:category text="History"/>']
    for n, x in enumerate(xs, start=1):
        dt = eastern(x["date"], x["time"])
        out += ["<item>", f"<title>{text(x['title'])}</title>", f"<link>{esc(x['link'])}</link>",
                f'<guid isPermaLink="false">bib:{esc(x["key"])}</guid>',
                f"<pubDate>{email.utils.format_datetime(dt)}</pubDate>",
                f"<description>{text(description(x, cal))}</description>",
                f'<enclosure url="{esc(x["audio"])}" length="0" type="audio/mpeg"/>',
                f"<itunes:episode>{n}</itunes:episode>", "<itunes:episodeType>full</itunes:episodeType>"]
        if x["duration"] and re.match(r"^\d+(:\d\d){1,2}$", str(x["duration"])):
            out.append(f"<itunes:duration>{esc(x['duration'])}</itunes:duration>")
        out.append("</item>")
    out += ["</channel>", "</rss>", ""]
    return "\n".join(out)


def opml(months, now):
    out = ['<?xml version="1.0" encoding="utf-8"?>', '<opml version="2.0">',
           f"<head><title>White House recordings, a feed a month (the 1968 series)</title>"
           f"<dateCreated>{email.utils.format_datetime(now)}</dateCreated></head>", "<body>"]
    for m, xs in months.items():
        out.append(f'<outline type="rss" text="White House recordings, {esc(ebooks.month_label(m))} ({len(xs)})" '
                   f'title="White House recordings, {esc(ebooks.month_label(m))}" '
                   f'xmlUrl="{esc(SITE)}feeds/{feed_name(m)}" htmlUrl="{esc(SITE + PAGE)}#rec-{m}"/>')
    out += ["</body>", "</opml>", ""]
    return "\n".join(out)


def build(series):
    """Write the feeds and the OPML; return their paths."""
    os.makedirs(OUT, exist_ok=True)
    cal = ebooks.calendar_days(series)
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    months = by_month()
    paths = []
    for m, xs in months.items():
        p = os.path.join(OUT, feed_name(m))
        with open(p, "w", encoding="utf-8") as f:
            f.write(feed(m, xs, cal, now))
        paths.append(p)
    p = os.path.join(OUT, "recordings.opml")
    with open(p, "w", encoding="utf-8") as f:
        f.write(opml(months, now))
    paths.append(p)
    return paths


# ---------------------------------------------------------------- the page (STYLE 7)

def _size(b):
    return f"{b / 1024 / 1024:.1f} MB" if b >= 1024 * 1024 else f"{b // 1024} KB"


def page(series, template):
    books = {m: (fn, size) for m, fn, size in ebooks.listing()}
    doc_months = ebooks.months()
    rec = by_month()
    years = sorted({m[:4] for m in list(doc_months) + list(rec)})
    nrec = sum(len(v) for v in rec.values())
    nfrus = sum(1 for v in doc_months.values() for x in v if x["src"] == "frus")
    nppp = sum(1 for v in doc_months.values() for x in v if x["src"] == "ppp")
    total = sum(s for _, s in books.values())
    main = [
        "<h1>Ebooks and feeds</h1>",
        '<p class="lede">The daybook\'s documents as ebooks, a month a book: every FRUS document of the month in full '
        f'and the President\'s Public Papers by title, day by day ({nfrus:,} and {nppp:,} documents, Jan. 1960 to Jan. '
        f'1969). The White House recordings the Miller Center gives free as podcast feeds, a month a feed, each '
        f'recording dated by the day it was made, in date order ({nrec:,} recordings, July 1962 to Jan. 1969).</p>',
        '<p class="logic">The books are EPUB 3 files: open them in Apple Books, Google Play Books, Kobo, Calibre or '
        'any EPUB reader, or send them to a Kindle. Each opens with a title page (what it holds, its order, its '
        'sources and their terms) and the contents by day; each document carries its heading, its author and '
        'citation, and links to its page on history.state.gov and to its day in the calendar. The feeds are RSS 2.0 '
        'with the audio as enclosures: paste a feed\'s address into a podcast app ("Add a show by URL") or a feed '
        'reader; the OPML file subscribes to every month at once. An app lists a feed\'s recordings oldest first.</p>',
        '<p class="logic">Feeds of all months: <a href="feeds/recordings.opml">feeds/recordings.opml</a>.</p>',
        '<h2 id="ebooks" data-short="Ebooks">Ebooks</h2>',
    ]
    if not books:
        main.append('<p class="logic">Not built here: the books are written by <code>./bib build ebooks</code> from the '
                    'FRUS text extract (sources/frus-text/).</p>')
    else:
        main.append(f'<p class="logic">{len(books)} books, {_size(total)} in all.</p>')
    for y in years:
        rows = []
        for m, docs in doc_months.items():
            if m[:4] != y or m not in books:
                continue
            fn, size = books[m]
            f = sum(1 for x in docs if x["src"] == "frus")
            rows.append(f'<tr id="doc-{m}"><td><a href="ebooks/{esc(fn)}">{esc(ebooks.month_label(m))}</a></td>'
                        f'<td class="n">{f:,}</td><td class="n">{len(docs) - f:,}</td><td class="n">{_size(size)}</td></tr>')
        if rows:
            main.append(f'<h3 id="ebooks-{y}">{y}</h3><table class="eb"><thead><tr><th>Month</th><th class="n">FRUS</th>'
                        f'<th class="n">PPP</th><th class="n">Size</th></tr></thead><tbody>{"".join(rows)}</tbody></table>')
    main.append('<h2 id="feeds" data-short="Feeds">Feeds of the recordings</h2>')
    main.append(f'<p class="logic">{len(rec)} feeds, {nrec:,} recordings. Left out: {prde_only():,} recordings PRDE '
                'catalogues that the Miller Center does not give (by subscription only), and machine noise and blank '
                'tape.</p>')
    for y in years:
        rows = [f'<tr id="rec-{m}"><td><a href="feeds/{feed_name(m)}">{esc(ebooks.month_label(m))}</a></td>'
                f'<td class="n">{len(xs):,}</td><td class="u">{esc(SITE)}feeds/{feed_name(m)}</td></tr>'
                for m, xs in rec.items() if m[:4] == y]
        if rows:
            main.append(f'<h3 id="feeds-{y}">{y}</h3><table class="eb"><thead><tr><th>Month</th>'
                        f'<th class="n">Recordings</th><th>Address</th></tr></thead><tbody>{"".join(rows)}</tbody></table>')
    main += [
        '<h2 id="sources" data-short="Sources">Sources and terms</h2>',
        '<p class="logic">FRUS. <i>Foreign Relations of the United States</i>, U.S. Department of State, Office of the '
        'Historian: the text from the Office\'s TEI files (github.com/HistoryAtState/frus), public domain as a work of '
        'the United States government and dedicated to the public domain worldwide under CC0 1.0 (the repository\'s '
        'LICENSE.md). Images are not reproduced. Dates, authors and order as the calendar\'s daybook gives them.</p>',
        '<p class="logic">The Public Papers. Titles and dates from the American Presidency Project (John Woolley and '
        'Gerhard Peters, University of California, Santa Barbara), each linked to its text there. The papers are '
        'public domain, but the Project\'s transcriptions are its site\'s, under its terms, and are not reproduced; '
        'GPO\'s govinfo gives these years\' volumes as page scans only.</p>',
        '<p class="logic">The recordings. The Miller Center of Public Affairs, University of Virginia, <i>Secret White '
        'House Tapes</i>: each recording\'s page and audio file, linked, not copied; the date, time, tape and citation '
        'from its catalogue. PRDE: the <i>Presidential Recordings Digital Edition</i> (University of Virginia Press), '
        'its catalogue\'s titles, speakers, places and lengths; its transcripts and introductions are by subscription '
        'and are not taken. A recording\'s time is as the catalogue gives it, taken as Eastern time.</p>',
    ]
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", "Ebooks and feeds").replace("{{main}}", "\n".join(main))
    head = (f'<link rel="alternate" type="text/x-opml" title="White House recordings, every month" '
            f'href="feeds/recordings.opml">\n' + CSS)
    return pg.replace("</head>", head + "\n</head>", 1)


CSS = """<style id="ebcss">
/* ebooks.html (tools/bib/feeds.py) */
table.eb{border-collapse:collapse;font-family:var(--sans);font-size:.85rem;line-height:1.35;margin:.4rem 0 1rem}
table.eb th{text-align:left;font-weight:600;color:var(--muted);border-bottom:1px solid var(--rule);padding:.25rem .8rem .25rem 0}
table.eb td{border-bottom:1px solid var(--rule);padding:.25rem .8rem .25rem 0;vertical-align:top}
table.eb .n{text-align:right}
table.eb .u{color:var(--muted);font-size:.78rem;word-break:break-all}
table.eb tr:target td{background:var(--hl-bg,#fff)}
</style>"""


# ---------------------------------------------------------------- the calendar's pages (STYLE 7)

def inject(page, lst, half):
    """A calendar part's head names its months' feeds; under its lede, a line to the page."""
    months = by_month()
    if half:
        months = {m: v for m, v in months.items() if calsplit.half_of_date(lst, f"{m}-01") == half}
    links = "".join(f'<link rel="alternate" type="application/rss+xml" title="White House recordings, '
                    f'{esc(ebooks.month_label(m))}" href="feeds/{feed_name(m)}">\n' for m in months)
    page = page.replace("</head>", links + "</head>", 1)
    line = ('<p class="logic">The documents of each month as an ebook, and the recordings the Miller Center gives free '
            f'as a podcast feed a month: <a href="{PAGE}">Ebooks and feeds</a>.</p>')
    m = re.search(r'<p class="lede">.*?</p>', page, re.S)
    return page[:m.end()] + line + page[m.end():] if m else page
