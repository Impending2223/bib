"""The daybook's documents as ebooks: an EPUB a month, every FRUS document of the month in full, with the
President's Public Papers of the month in full, from GPO's volumes, day by day, in the daybook's order.

    sources/ppp-text/<package>.json.xz   the Public Papers' items, their text cleaned from GPO's volumes on govinfo,
                             with their pagination (tools/ppp/make_ppp_text.py; tools/bib/ppp.py); public domain
    sources/frus-text/<YYYY-MM>.json.xz   the FRUS documents' text in XHTML, a document a key (the daybook's), made
                             from the Office of the Historian's TEI files by tools/ebooks/make_frus_text.py (public
                             domain; CC0); the build needs neither the TEI nor the network
    daybook/<YYYY-MM>.yaml   the documents of each month, their dates, authors, citations and links (tools/bib/daybook.py)
    build/ebooks/documents-<YYYY-MM>.epub   written by `./bib build ebooks` (and the full build); listed on
                             build/ebooks.html (tools/bib/feeds.py writes the page and the recordings' feeds)

STYLE:
 1. The unit: a calendar month, both sources together, so the President's documents and the State Department's of a
    day stand side by side, as in the calendar's day. A month runs 26 to 516 FRUS documents, 21,925 to 462,675 words
    (Oct. 1962), an EPUB of 85 KB to 1.1 MB (62 MB the 109 books); a year a source would run to 3.6 million words, more than a reader opens
    comfortably. Every month the daybook holds, Jan. 1960 to Jan. 1969.
 2. The book: a title page (what it holds, how it is ordered, the sources and their terms, when built); the contents
    by day, each document under its day by its heading; then the days, a file a day (a day over about 300 KB in
    parts). EPUB 3, with an NCX for older readers.
 3. A day: its date as a heading ("Monday, Oct. 1, 1962") and a link to the day in the calendar (the site's page and
    the day's anchor); the President's items of the Public Papers dated that day (a dateless item under the date of
    the item before it), in the volume's order; then APP's documents of the day that the Public Papers do not print
    (the executive orders, the proclamations, the campaign of 1960), by title, linked to APP; then the FRUS documents
    in the daybook's order (volume, then number).
 4. A FRUS document: its heading as FRUS prints it; under it, muted, the author as the daybook reads it, the time,
    the citation with the volume's title ("FRUS 1961–63, XI: Cuban Missile Crisis and Aftermath, doc. 1"), "through
    Oct. 3" for a range, "filed by its place in the volume" for an editorial note, then "history.state.gov" (the
    document's page) and "Calendar" (the day); then the text and its footnotes (tools/ebooks/make_frus_text.py,
    STYLE). A document the extract lacks: its heading and links, and "Text not in this book".
 5. A Public Papers item: its heading as the volume prints it, the number first ("1. Inaugural Address"); under
    it, muted, its date, the cite ("1961 Pub. Papers 1") linked to its first page in GPO's PDF on govinfo, the
    volume's title and the item's pages, and "Calendar" (the day); then the text, paragraph by paragraph, each
    printed page's beginning marked "p. 123" (small, muted, linked to that page of the PDF); a line set off (a
    signature, a close) to the right; the editors' bracketed notes in italics; the editors' note ("NOTE: ...") and the
    footnotes in small type after the text. The text: the volume's OCR, cleaned by rule (tools/ppp/make_ppp_text.py,
    its STYLE: the running heads and folios gone, words broken at a line's end rejoined, the commonest misreadings
    put right, the paragraphs restored); a misreading no rule meets stands as printed.
 6. No recordings, no transcripts: the recordings are in the feeds (tools/bib/feeds.py); PRDE's transcripts are the
    Edition's, behind its subscription.
 7. Deterministic: the same inputs make the same file but for the build date on the title page and in the OPF; the
    zip's dates fixed. The mimetype first and stored, as the OCF requires; `validate` checks every book written.
"""
import datetime
import glob
import html
import io
import json
import lzma
import os
import re
import uuid
import xml.etree.ElementTree as ET
import zipfile

from . import daybook, store

SITE = "https://impending2223.github.io/bib/"
TEXT = os.path.join(store.ROOT, "sources", "frus-text")
OUT = os.path.join(store.ROOT, "build", "ebooks")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
PART = 300 * 1024                    # a day's file over this is split between documents (STYLE 2)
LIMIT = 20 * 1024 * 1024             # a book over this is reported by the build
ZDATE = (1980, 1, 1, 0, 0, 0)
XHTML = "http://www.w3.org/1999/xhtml"


def esc(t):
    return html.escape(str(t), quote=True)


def name(month):
    return f"documents-{month}.epub"


def month_label(month):
    y, m = month.split("-")
    return f"{MONTHS[int(m) - 1]} {y}"


def day_head(d):
    return f"{DAYS[d.weekday()]}, {daybook.day_label(d)}"


def load_text(month):
    p = os.path.join(TEXT, f"{month}.json.xz")
    if not os.path.exists(p):
        return None
    return json.loads(lzma.decompress(open(p, "rb").read()))


def months():
    """The months the daybook holds documents for, with their documents (APP and FRUS), in the daybook's order."""
    docs, _ = daybook.load()
    out = {}
    for x in docs:
        if x.get("src") in ("ppp", "frus"):
            out.setdefault(x["date"][:7], []).append(x)
    return dict(sorted(out.items()))


def calendar_days(series):
    """{iso: the day's address on the site}: every day the calendar lays out (its dated sections' spans)."""
    from . import calsplit
    cal = next((l for l in series.lists.values() if l.kind == "calendar"), None) if series else None
    if cal is None:
        return {}
    out = {}
    for sec in cal.walk():
        ex = getattr(sec, "extra", {}) or {}
        if not (ex.get("from") and ex.get("to")):
            continue
        d = datetime.date.fromisoformat(str(ex["from"]))
        hi = datetime.date.fromisoformat(str(ex["to"]))
        while d <= hi:
            iso = d.isoformat()
            page = calsplit.page_key(cal, calsplit.half_of_date(cal, iso)) if calsplit.cfg(cal) else cal.key
            out[iso] = f"{SITE}{page}.html#d{iso}"
            d += datetime.timedelta(days=1)
    return out


# ---------------------------------------------------------------- the pages of a book

CSS = """body{font-family:Georgia,"Times New Roman",serif;line-height:1.45;margin:0 4%}
h1{font-size:1.6em;margin:1.2em 0 .4em}
h2{font-size:1.3em;margin:1.2em 0 .3em}
h3{font-size:1.05em;margin:1.6em 0 .2em;line-height:1.3}
h4{font-size:1em;margin:1.2em 0 .3em}
p{margin:.35em 0;text-indent:0}
.m,.meta,.fns,.cal{font-size:.85em;color:#555}
.meta{margin:.1em 0 .6em}
.cal{margin:.1em 0 1em}
ul.pp{padding-left:1.2em}
ul.pp li{margin:.2em 0}
ul.tl{list-style:none;padding-left:1.2em}
ul.tl li{margin:.2em 0}
.lh{font-variant:small-caps;margin-top:.6em}
.lb{font-weight:normal}
.c{text-align:center}
.r,.dl.r,.sg{text-align:right}
.st{font-style:italic}
.sc{font-variant:small-caps}
.rm{font-style:normal}
.fig{font-style:italic;color:#555}
.att{margin-top:1em;border-top:1px solid #bbb;padding-top:.4em}
blockquote{margin:.5em 1.5em}
table.tt{border-collapse:collapse;font-size:.85em;margin:.6em 0}
table.tt td,table.tt th{border:1px solid #bbb;padding:.15em .35em;vertical-align:top}
.fns{border-top:1px solid #bbb;margin-top:.8em;padding-top:.3em}
aside.fn p{margin:.25em 0}
sup.nr{font-size:.7em;line-height:0}
.ni{font-size:.9em}
nav ol{list-style:none;padding-left:0}
nav ol ol{padding-left:1.2em;font-size:.9em}
.title p{margin:.6em 0}
a.pg,span.pg{font-size:.7em;color:#888;text-decoration:none;font-variant:normal;white-space:nowrap;margin:0 .15em}
.ed{font-style:italic;text-align:center}
.sg{margin-left:40%}
.pnote{font-size:.85em;margin-top:.6em}
.pnote p,.pfn{font-size:.85em}
.psm{font-size:.9em}
h4.ph{font-variant:small-caps;font-weight:normal}
"""


def page(title, body):
    return ("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<!DOCTYPE html>\n"
            f'<html xmlns="{XHTML}" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">\n'
            f'<head><meta charset="utf-8"/><title>{esc(title)}</title>'
            '<link rel="stylesheet" type="text/css" href="style.css"/></head>\n'
            f"<body>\n{body}\n</body>\n</html>\n")


def meta_line(x, cal_url):
    bits = []
    if x.get("author"):
        bits.append(esc(x["author"]))
    if x.get("time"):
        bits.append(esc(x["time"]))
    if x.get("cite"):
        bits.append(esc(daybook.frus_cite(x)))
    if x.get("until"):
        u = datetime.date.fromisoformat(x["until"])
        bits.append(esc("through " + daybook.day_label(u, u.year != int(x["date"][:4]))))
    if x.get("placed"):
        bits.append("filed by its place in the volume")
    if x.get("url"):
        bits.append(f'<a href="{esc(x["url"])}">history.state.gov</a>')
    if cal_url:
        bits.append(f'<a href="{esc(cal_url)}">Calendar</a>')
    return f'<p class="meta">{" · ".join(bits)}</p>'


def frus_block(x, text, cal_url, n):
    """A FRUS document (STYLE 4): the heading, the meta line, the text and notes. Returns (anchor, heading, xhtml)."""
    frag = text.get(x["key"]) if text else None
    if frag and frag.startswith("<h3"):
        h, _, rest = frag.partition("</h3>")
        anchor = re.match(r'<h3 id="([^"]+)"', h).group(1)
        heading = re.sub(r"<sup.*?</sup>", "", h)
        heading = html.unescape(re.sub(r"<[^>]+>", "", heading)).strip()
        return anchor, heading, f"{h}</h3>{meta_line(x, cal_url)}{rest}"
    anchor = f"fx{n}"
    return anchor, x["title"], (f'<h3 id="{anchor}">{esc(x["title"])}</h3>{meta_line(x, cal_url)}'
                                '<p class="m">Text not in this book: see the document’s page.</p>')


def ppp_list(xs, iso):
    items, toc = [], []
    for i, x in enumerate(xs, start=1):
        a = f"pp{iso.replace('-', '')}-{i}"
        t = esc(x["title"])
        items.append(f'<li id="{a}"><a href="{esc(x["url"])}">{t}</a></li>' if x.get("url") else f'<li id="{a}">{t}</li>')
        toc.append((a, x["title"]))
    body = ('<p class="lh">The President: not in the Public Papers (by title; the text at the American Presidency '
            f'Project)</p><ul class="pp">{"".join(items)}</ul>')
    return body, toc


PKIND = {"p": "p", "s": "sg", "h": "ph", "b": "ed", "n": "pnote", "f": "pfn", "q": "psm"}


def ppp_block(pkg, it, cal_url):
    """A Public Papers item (STYLE 5): (anchor, heading, xhtml)."""
    from . import ppp
    v = ppp.data().get("volumes", {}).get(pkg) or {}
    anchor = f"p{pkg[4:8]}{pkg[-1]}n{it['n']}"
    heading = f"{it['n']}. {it['title']}"
    pi = ppp.item(pkg, it["n"])
    day = it.get("date")
    bits = []
    if day:
        bits.append(esc(daybook.day_label(datetime.date.fromisoformat(day), True)))
    else:
        bits.append("undated in its heading; filed by its place in the volume")
    if pi:
        bits.append(f'<a href="{esc(pi["url"])}">{esc(pi["cite"])}</a>')
        pp = f"p. {it['page']}" if it["page"] == it["page_to"] else f"pp. {it['page']}–{it['page_to']}"
        bits.append(esc(f"{v.get('title', '')}, item {it['n']}, {pp}"))
    if cal_url:
        bits.append(f'<a href="{esc(cal_url)}">Calendar</a>')
    out = [f'<h3 id="{anchor}">{esc(heading)}</h3><p class="meta">{" · ".join(bits)}</p>']
    note = []
    for k, t in it["text"]:
        x = ppp.marked(t, pkg)
        if k == "n":
            note.append(f"<p>{x}</p>")
        elif k == "h":
            out.append(f'<h4 class="ph">{x}</h4>')
        else:
            out.append(f'<p class="{PKIND.get(k, "p")}">{x}</p>' if k != "p" else f"<p>{x}</p>")
    if note:
        out.append(f'<div class="pnote">{"".join(note)}</div>')
    return anchor, heading, "".join(out)


def build_book(month, docs, text, cal, built):
    """The book's files: [(name, bytes)], and its counts."""
    from . import ppp
    by_day = {}
    for x in docs:
        by_day.setdefault(x["date"], []).append(x)
    pdays = {d: xs for d, xs in ppp.items_by_day().items() if d[:7] == month}
    for d in pdays:
        by_day.setdefault(d, [])
    spine, nav_days, n = [], [], 0
    nfrus = sum(1 for x in docs if x["src"] == "frus")
    app_only = [x for x in docs if x["src"] == "ppp" and not ppp.match(x.get("url"))]
    nppp = sum(len(xs) for xs in pdays.values())
    with_text = sum(1 for x in docs if x["src"] == "frus" and text and x["key"] in text)
    vols = sorted({x["cite"].rpartition(", doc. ")[0] + (": " + x["vol"] if x.get("vol") else "")
                   for x in docs if x["src"] == "frus"})
    for iso in sorted(by_day):
        d = datetime.date.fromisoformat(iso)
        xs = by_day[iso]
        cal_url = cal.get(iso)
        head = (f'<h2 id="d{iso}">{esc(day_head(d))}</h2>'
                + (f'<p class="cal"><a href="{esc(cal_url)}">The day in the calendar</a></p>' if cal_url else ""))
        toc, blocks = [], []
        for pkg, it in pdays.get(iso, []):         # the Public Papers in full (STYLE 3, 5)
            a, h, body = ppp_block(pkg, it, cal_url)
            blocks.append(f'<div class="doc">{body}</div>')
            toc.append((a, "The President: " + h))
        app = [x for x in xs if x["src"] == "ppp" and not ppp.match(x.get("url"))]
        if app:
            body, t = ppp_list(app, iso)
            blocks.append(body)
            toc += [(a, "The President (APP): " + h) for a, h in t]
        for x in xs:
            if x["src"] != "frus":
                continue
            n += 1
            a, h, body = frus_block(x, text, cal_url, n)
            blocks.append(f'<div class="doc">{body}</div>')
            toc.append((a, h))
        # files: a day, or its parts (STYLE 2)
        files, cur, size = [], [head], len(head)
        for b in blocks:
            if size + len(b) > PART and len(cur) > 1:
                files.append(cur)
                cur, size = [f'<p class="m">{esc(day_head(d))}, continued</p>'], 0
            cur.append(b)
            size += len(b)
        files.append(cur)
        names = [f"d{iso}.xhtml" if i == 0 else f"d{iso}-{i + 1}.xhtml" for i in range(len(files))]
        where = {}
        for fn, parts in zip(names, files):
            body = "\n".join(parts)
            for a in re.findall(r' id="([^"]+)"', body):
                where[a] = fn
            spine.append((fn, page(day_head(d), body)))
        nav_days.append((names[0], f"d{iso}", day_head(d), [(where.get(a, names[0]), a, h) for a, h in toc]))
    title = f"Documents, {month_label(month)}"
    # the title page (STYLE 2)
    vol_list = "".join(f"<li>{esc(v)}</li>" for v in vols)
    not_printed = f"; {len(app_only):,} documents the Public Papers do not print, by title" if app_only else ""
    tp = (f'<div class="title"><h1>{esc(title)}</h1>'
          f'<p>Every document of <i>Foreign Relations of the United States</i> dated in {esc(month_label(month))}, in '
          f'full ({nfrus:,}{"" if with_text == nfrus else f"; {with_text:,} with their text"}), and the President’s '
          f'Public Papers of the month in full ({nppp:,} items{not_printed}), day by day.</p>'
          '<p>Order: as the calendar’s daybook files them. A document under the day it is dated, a range under its '
          'first day; an editorial note under the document before it in its volume. Within a day, the President’s '
          'items in the volume’s order (an item whose heading gives no day under the date of the item before it), '
          'then the documents APP gives that the Public Papers do not print, then FRUS by volume and number. Each '
          'Public Papers item: its number and heading, its date, the cite linked to its first page in GPO’s volume, '
          'the volume and pages; then its text, each printed page’s beginning marked “p. 123”, linked to the page; '
          'the editors’ note after it. Each FRUS document: its '
          'heading as FRUS prints it, then its author (the sender, the signer, or the drafter, as the daybook reads '
          'them), the citation, a link to its page on history.state.gov and to the day in the calendar; then its text '
          'and footnotes.</p>'
          '<p>Sources and terms. <i>Foreign Relations of the United States</i>, U.S. Department of State, Office of the '
          'Historian: the text from the Office’s TEI files (github.com/HistoryAtState/frus), public domain as a work '
          'of the United States government, and dedicated to the public domain worldwide under CC0 1.0 (the '
          'repository’s LICENSE.md). Images are not reproduced. The volumes:</p>'
          f'<ul class="pp">{vol_list}</ul>'
          '<p><i>Public Papers of the Presidents of the United States</i> (Office of the Federal Register, National '
          'Archives and Records Service): the text from the volumes’ scans on govinfo (U.S. Government Publishing '
          'Office), their OCR text layer cleaned by rule: the running heads and folios set aside, words broken at a '
          'line’s end rejoined, the commonest misreadings put right, the paragraphs restored. A misreading no rule '
          'meets stands as printed; the page links show the page itself. Public domain as a work of the United '
          'States government. The documents the Public Papers do not print are listed by title from the American '
          'Presidency Project (John Woolley and Gerhard Peters, University of California, Santa Barbara), each linked '
          'to its text there; the Project’s transcriptions are its site’s, under its terms, and are not '
          'reproduced.</p>'
          f'<p>Made by the 1968 series ({esc(SITE)}), {esc(built.isoformat())}. Ebooks and feeds: '
          f'<a href="{esc(SITE)}ebooks.html">{esc(SITE)}ebooks.html</a>.</p></div>')
    # the contents (nav), also in the spine
    lis = []
    for fn, a, label, docs_ in nav_days:
        sub = "".join(f'<li><a href="{esc(f)}#{esc(x)}">{esc(h)}</a></li>' for f, x, h in docs_)
        lis.append(f'<li><a href="{esc(fn)}#{esc(a)}">{esc(label)}</a>' + (f"<ol>{sub}</ol>" if sub else "") + "</li>")
    nav = (f'<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>{"".join(lis)}</ol></nav>'
           '<nav epub:type="landmarks" hidden=""><ol>'
           '<li><a epub:type="titlepage" href="title.xhtml">Title page</a></li>'
           '<li><a epub:type="toc" href="nav.xhtml">Contents</a></li>'
           f'<li><a epub:type="bodymatter" href="{esc(spine[0][0]) if spine else "title.xhtml"}">The days</a></li>'
           '</ol></nav>')
    ident = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, SITE + "ebooks/" + name(month)))
    stamp = built.strftime("%Y-%m-%dT00:00:00Z")
    items = ['<item id="css" href="style.css" media-type="text/css"/>',
             '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
             '<item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>',
             '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>']
    refs = ['<itemref idref="title"/>', '<itemref idref="nav"/>']
    for i, (fn, _) in enumerate(spine):
        items.append(f'<item id="x{i}" href="{esc(fn)}" media-type="application/xhtml+xml"/>')
        refs.append(f'<itemref idref="x{i}"/>')
    opf = ('<?xml version="1.0" encoding="utf-8"?>\n'
           '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="en">\n'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
           f'<dc:identifier id="uid">{ident}</dc:identifier>\n<dc:title>{esc(title)}</dc:title>\n'
           '<dc:language>en</dc:language>\n'
           '<dc:creator>United States Department of State, Office of the Historian</dc:creator>\n'
           f'<dc:publisher>The 1968 series ({esc(SITE)})</dc:publisher>\n'
           '<dc:source>Foreign Relations of the United States; Public Papers of the Presidents (govinfo); the '
           'American Presidency Project (titles)</dc:source>\n'
           '<dc:rights>FRUS text: public domain (a work of the United States government; CC0 1.0). Public Papers: '
           'public domain (a work of the United States government). APP: titles only, linked.</dc:rights>\n'
           f'<dc:date>{esc(month)}</dc:date>\n'
           f'<meta property="dcterms:modified">{stamp}</meta>\n'
           '</metadata>\n<manifest>\n' + "\n".join(items) + '\n</manifest>\n<spine toc="ncx">\n'
           + "\n".join(refs) + "\n</spine>\n</package>\n")
    # the NCX
    pts, order = [], 0

    def pt(label, src, kids=""):
        nonlocal order
        order += 1
        return (f'<navPoint id="n{order}" playOrder="{order}"><navLabel><text>{esc(label)}</text></navLabel>'
                f'<content src="{esc(src)}"/>{kids}</navPoint>')
    pts.append(pt("Title page", "title.xhtml"))
    pts.append(pt("Contents", "nav.xhtml"))
    for fn, a, label, docs_ in nav_days:
        head = pt(label, f"{fn}#{a}")
        kids = "".join(pt(h, f"{f}#{x}") for f, x, h in docs_)
        pts.append(head[:-len("</navPoint>")] + kids + "</navPoint>")
    ncx = ('<?xml version="1.0" encoding="utf-8"?>\n'
           '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en">\n'
           f'<head><meta name="dtb:uid" content="{ident}"/><meta name="dtb:depth" content="2"/>'
           '<meta name="dtb:totalPageCount" content="0"/><meta name="dtb:maxPageNumber" content="0"/></head>\n'
           f'<docTitle><text>{esc(title)}</text></docTitle>\n<navMap>{"".join(pts)}</navMap>\n</ncx>\n')
    container = ('<?xml version="1.0" encoding="utf-8"?>\n'
                 '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
                 '</rootfiles></container>\n')
    files = [("META-INF/container.xml", container), ("OEBPS/content.opf", opf), ("OEBPS/toc.ncx", ncx),
             ("OEBPS/style.css", CSS), ("OEBPS/title.xhtml", page(title, tp)),
             ("OEBPS/nav.xhtml", page("Contents", nav))]
    files += [(f"OEBPS/{fn}", body) for fn, body in spine]
    return files, {"frus": nfrus, "ppp": nppp, "app": len(app_only), "text": with_text, "days": len(by_day)}


def write_epub(path, files):
    """The OCF zip: the mimetype first, stored, no extra field; the rest deflated; fixed dates (STYLE 7)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        zi = zipfile.ZipInfo("mimetype", date_time=ZDATE)
        zi.compress_type = zipfile.ZIP_STORED
        z.writestr(zi, b"application/epub+zip")
        for fn, body in files:
            zi = zipfile.ZipInfo(fn, date_time=ZDATE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, body.encode("utf-8") if isinstance(body, str) else body, compresslevel=6)
    data = buf.getvalue()
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)


def validate(path):
    """The book's structure: [problem]. The mimetype first and stored; container.xml naming the OPF; every file
    well-formed XML; the manifest's files present; the spine's idrefs in the manifest; one nav; links inside resolve."""
    out = []
    z = zipfile.ZipFile(path)
    infos = z.infolist()
    if not infos or infos[0].filename != "mimetype" or infos[0].compress_type != zipfile.ZIP_STORED \
            or z.read("mimetype") != b"application/epub+zip" or infos[0].extra:
        out.append("mimetype not first, stored and exact")
    names = set(z.namelist())
    try:
        c = ET.fromstring(z.read("META-INF/container.xml"))
        opf_path = c.find(".//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile").get("full-path")
    except Exception as e:                     # noqa: BLE001
        return out + [f"container.xml: {e}"]
    base = os.path.dirname(opf_path)
    opf = ET.fromstring(z.read(opf_path))
    O = "{http://www.idpf.org/2007/opf}"
    man = {i.get("id"): i for i in opf.iter(O + "item")}
    for i in man.values():
        if os.path.join(base, i.get("href")) not in names:
            out.append(f"manifest file missing: {i.get('href')}")
    if sum(1 for i in man.values() if "nav" in (i.get("properties") or "").split()) != 1:
        out.append("not one nav document")
    for r in opf.iter(O + "itemref"):
        if r.get("idref") not in man:
            out.append(f"spine idref not in the manifest: {r.get('idref')}")
    ids = {}
    for n in names:
        if n.endswith((".xhtml", ".opf", ".ncx", ".xml")):
            try:
                root = ET.fromstring(z.read(n))
            except ET.ParseError as e:
                out.append(f"{n}: {e}")
                continue
            if n.endswith(".xhtml"):
                ids[os.path.basename(n)] = {e.get("id") for e in root.iter() if e.get("id")}
    for n in names:
        if not n.endswith(".xhtml"):
            continue
        for e in ET.fromstring(z.read(n)).iter("{%s}a" % XHTML):
            h = e.get("href") or ""
            if h.startswith(("http:", "https:", "mailto:")) or not h:
                continue
            f, _, frag = h.partition("#")
            f = f or os.path.basename(n)
            if f not in ids:
                out.append(f"{n}: link to a missing file {h}")
            elif frag and frag not in ids[f]:
                out.append(f"{n}: link to a missing anchor {h}")
    return out


def build(series, only=None):
    """Write build/ebooks/documents-<YYYY-MM>.epub for every month (or `only`, a list of months); return
    [(path, month, counts)]. Months without the FRUS text extract are skipped, and said so."""
    os.makedirs(OUT, exist_ok=True)
    cal = calendar_days(series)
    built = datetime.datetime.now(datetime.timezone.utc).date()
    out = []
    for month, docs in months().items():
        if only and month not in only:
            continue
        data = load_text(month)
        if data is None and any(x["src"] == "frus" for x in docs):
            print(f"ebooks: no sources/frus-text/{month}.json.xz; {month} not built")
            continue
        files, counts = build_book(month, docs, (data or {}).get("docs", {}), cal, built)
        path = os.path.join(OUT, name(month))
        write_epub(path, files)
        if os.path.getsize(path) > LIMIT:
            print(f"ebooks: {name(month)} is {os.path.getsize(path) // 1024 // 1024} MB, over the limit")
        out.append((path, month, counts))
    return out


def listing():
    """[(month, file name, size in bytes)] of the books in build/ebooks/, for the page."""
    out = []
    for p in sorted(glob.glob(os.path.join(OUT, "documents-*.epub"))):
        m = re.search(r"documents-(\d{4}-\d\d)\.epub$", p)
        if m:
            out.append((m.group(1), os.path.basename(p), os.path.getsize(p)))
    return out


def problems():
    """The extract's files: a name per month, each a month the daybook holds FRUS documents for; the months the daybook
    holds FRUS documents for and the extract lacks (a warning: those books are not built)."""
    errs, warns = [], []
    have = {}
    for p in glob.glob(os.path.join(TEXT, "*")):
        m = re.match(r"(\d{4}-\d\d)\.json\.xz$", os.path.basename(p))
        if not m:
            errs.append((os.path.relpath(p, store.ROOT), "not a month's extract (YYYY-MM.json.xz)"))
            continue
        with open(p, "rb") as f:
            if f.read(6) != b"\xfd7zXZ\x00":
                errs.append((os.path.relpath(p, store.ROOT), "not an xz file"))
        have[m.group(1)] = p
    frus_months = set()
    for p in glob.glob(os.path.join(daybook.DIR, "[0-9][0-9][0-9][0-9]-[0-9][0-9].yaml")):
        frus_months.add(os.path.basename(p)[:7])
    for m in sorted(set(have) - frus_months):
        errs.append((f"sources/frus-text/{m}.json.xz", "no daybook month of that name"))
    if have:
        for m in sorted(frus_months - set(have)):
            warns.append((f"daybook/{m}.yaml", "no FRUS text extract (tools/ebooks/make_frus_text.py): no ebook"))
    return errs, warns
