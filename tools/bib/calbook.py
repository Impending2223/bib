"""The whole calendar as one EPUB (the owner, Nov. 23, 2026: "How big would an EPUB of the whole calendar be? Could you
make one for me?"): `python3 -m tools.bib.calbook` writes build/ebooks/calendar.epub from the built calendar pages.

STYLE
 1. The text is the site's own: each calendar page's days (`div.day`) and week headings (`h3.wk`), as `./bib build cal`
    rendered them, so the book says what the pages say, in their order, with their notes, footnotes and thread links.
    Build the calendar first.
 2. Left out, being the page's controls or other books' matter: the contents navigator, the visibility panel, the
    threads' statements at the head of each page, the indicator tables, the maps and seat charts, the day's documents
    lists (they are the daybook's ebooks), scripts, buttons and forms, the permalink mark.
 3. A file a month, a month over PART in parts at its week headings; a heading for each month. The contents: years,
    then months, then weeks.
 4. Links: to an anchor in the book, inside the book; anything else to the site (SITE), so a name, a work's card or a
    day's other page opens in the browser.
 5. The style: the site's own rules for the classes kept, taken from the page's stylesheet with its colour and font
    tokens resolved (many readers lack CSS variables); the fonts are the readers' own (EPUB readers do not load web
    fonts from Google); no fixed or absolute positioning, no hover.
 6. Validated with ebooks.validate (structure, well-formed files, inner links).
"""
import datetime
import os
import re
import sys
import uuid

import lxml.etree as LET
import lxml.html as LH

from . import ebooks, store

SITE = ebooks.SITE
BUILD = os.path.join(store.ROOT, "build")
OUT = os.path.join(BUILD, "ebooks", "calendar.epub")
PART = 700 * 1024
MONTHS = ebooks.MONTHS
DROP_TAGS = {"script", "style", "details", "figure", "button", "select", "input", "label", "svg", "form", "noscript"}
DROP_CLASSES = {"pl", "tba", "tbt", "seam", "dtog", "cg", "cgmaps", "vnm"}
KEEP_ATTRS = {"class", "id", "href", "title", "colspan", "rowspan", "lang", "dir", "scope"}


def page_keys():
    """The calendar's current parts in order (lists/cal/list.yaml, split)."""
    import yaml
    with open(os.path.join(store.ROOT, "lists", "cal", "list.yaml"), encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return [p["page"] for p in cfg["split"]]


def month_of(el):
    """The month an element belongs to, 'YYYY-MM', or None."""
    i = el.get("id") or ""
    m = re.match(r"d(\d{4}-\d\d)-\d\d$", i) or re.match(r"ix-(\d{4}-\d\d)", i)
    if m:
        return m.group(1)
    for li in el.iter("li"):
        m = re.match(r"cal\.(\d{4}-\d\d)", li.get("id") or "")
        if m:
            return m.group(1)
    return None


def clean(el):
    for e in list(el.iter()):
        if not isinstance(e.tag, str):
            if e.getparent() is not None and isinstance(e, LET._Comment):
                e.drop_tree() if hasattr(e, "drop_tree") else e.getparent().remove(e)
            continue
        cls = set((e.get("class") or "").split())
        if e.tag in DROP_TAGS or cls & DROP_CLASSES or e.get("hidden") is not None:
            e.drop_tree()
            continue
        for a in list(e.attrib):
            if a not in KEEP_ATTRS:
                del e.attrib[a]
    return el


def css_from(page_html):
    """The site's rules for the classes kept, tokens resolved (STYLE 5)."""
    styles = "".join(re.findall(r"<style[^>]*>(.*?)</style>", page_html, re.S))
    styles = re.sub(r"/\*.*?\*/", "", styles, flags=re.S)
    tokens = {}
    for body in re.findall(r"(?<![\w-]):root\s*\{([^}]*)\}", styles):
        for k, v in re.findall(r"(--[\w-]+)\s*:\s*([^;]+)", body):
            tokens.setdefault(k, v.strip())
    # top level only: drop @media/@supports blocks
    flat, depth, buf = [], 0, ""
    i = 0
    while i < len(styles):
        ch = styles[i]
        if ch == "@" and depth == 0:
            j = styles.find("{", i)
            k = styles.find(";", i)
            if k != -1 and (j == -1 or k < j):
                i = k + 1
                continue
            d, i = 0, j
            while i < len(styles):
                d += styles[i] == "{"
                d -= styles[i] == "}"
                i += 1
                if d == 0:
                    break
            continue
        buf += ch
        if ch == "}":
            flat.append(buf.strip())
            buf = ""
        i += 1
    want = re.compile(r"(^|[\s>+~,(])(\.(day|dh|dn|wk|e|c|n|s|tn|tnl|tnb|fm|fk|fn|rw|rubrow|dl|nm|x|rt|tm|tv|en|ec|ev|es|ep"
                      r"|cont|cl|bl|blw|blsrc|elsum|bld|blc|blv|blr|ecs|em|eno|w|pqi|sw|lk|src|au|ty|tx|cgn|cmk|mo|yr|sun"
                      r"|ix)\b|ol\.e|span\.c|span\.n)")
    out = []
    for r in flat:
        sel, _, body = r.partition("{")
        if not want.search(sel) or re.search(r":hover|#drawer|#rail|\.tocc|\.vis|nav\b|header", sel):
            continue
        body = body.rstrip("}")
        for _ in range(3):
            body = re.sub(r"var\((--[\w-]+)(?:,\s*([^()]*))?\)", lambda m: tokens.get(m.group(1), m.group(2) or "inherit"), body)
        body = re.sub(r"position\s*:\s*(sticky|fixed|absolute)", "position:static", body)
        out.append(f"{sel.strip()}{{{body}}}")
    base = ("body{font-family:Georgia,\"Times New Roman\",serif;line-height:1.45;margin:0 .6em;color:"
            + tokens.get("--ink", "#1A1E26") + "}\n"
            "h1,h2,h3{font-family:\"Helvetica Neue\",Arial,sans-serif}\nh2.mo{margin:1.2em 0 .4em}\n"
            "a{color:" + tokens.get("--accent", "#1F4FA3") + "}\n")
    return base + "\n".join(out) + "\n"


def build(out=OUT):
    keys = page_keys()
    files, nav, ids, css = [], [], {}, None
    chunks = []                                   # (month, [xhtml strings])
    for key in keys:
        path = os.path.join(BUILD, key + ".html")
        if not os.path.exists(path):
            print(f"calbook: {key}.html not built; skipped")
            continue
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        if css is None:
            css = css_from(raw)
        root = LH.document_fromstring(raw)
        main = root.find(".//main")
        els = [e for e in main if isinstance(e.tag, str) and
               ((e.tag == "div" and "day" in (e.get("class") or "").split()) or
                (e.tag == "h3" and "wk" in (e.get("class") or "").split()))]
        months = [month_of(e) for e in els]
        nxt = None
        for i in range(len(els) - 1, -1, -1):     # a week heading or undated block: the month of what follows
            months[i] = months[i] or nxt
            nxt = months[i]
        prev = None
        for i, m in enumerate(months):
            months[i] = m or prev
            prev = months[i]
        for e, m in zip(els, months):
            clean(e)
            for x in e.iter():
                if isinstance(x.tag, str) and x.get("id"):
                    x.set("data-page", key)
            if not chunks or chunks[-1][0] != m:
                chunks.append([m, []])
            chunks[-1][1].append(e)
    # files: a month, or parts at week headings
    spine = []
    for m, els in chunks:
        y, mo = int(m[:4]), int(m[5:])
        label = f"{MONTHS[mo - 1]} {y}"
        cur, size, n = [], 0, 1
        fn = f"m{m}.xhtml"
        groups = []
        for e in els:
            s = len(LET.tostring(e, encoding="unicode"))
            if cur and size + s > PART and e.tag == "h3":
                groups.append(cur)
                cur, size = [], 0
            cur.append(e)
            size += s
        if cur:
            groups.append(cur)
        weeks = []
        for gi, g in enumerate(groups):
            name = fn if gi == 0 else f"m{m}-{gi + 1}.xhtml"
            spine.append((name, m, label, g, gi == 0))
            for e in g:
                for x in e.iter():
                    if isinstance(x.tag, str) and x.get("id"):
                        i = x.get("id")
                        if i in ids:              # a second id of the same name: dropped (inner links take the first)
                            del x.attrib["id"]
                        else:
                            ids[i] = (name, x.get("data-page"))
                if e.tag == "h3" and e.get("id"):
                    weeks.append((name, e.get("id"), e.text_content().strip()))
        nav.append((y, m, label, fn, weeks))
    # links (STYLE 4) and serialisation
    body_files = []
    for name, m, label, g, first in spine:
        out_parts = []
        if first:
            out_parts.append(f'<h2 class="mo" id="mo{m}">{ebooks.esc(label)}</h2>')
        for e in g:
            for a in e.iter("a"):
                h = a.get("href")
                if not h:
                    continue
                if h.startswith(("http:", "https:", "mailto:")):
                    continue
                f, _, frag = h.partition("#")
                if frag and frag in ids and (not f or f.endswith(".html")):
                    tgt, _pg = ids[frag]
                    a.set("href", ("" if tgt == name else tgt) + "#" + frag)
                else:
                    pg = f or e.get("data-page") or ""
                    a.set("href", SITE + pg + (("#" + frag) if frag else ""))
            for x in e.iter():
                if isinstance(x.tag, str) and "data-page" in x.attrib:
                    del x.attrib["data-page"]
            out_parts.append(LET.tostring(e, encoding="unicode", method="xml"))
        body_files.append((name, label, "\n".join(out_parts)))
    # the book
    built = datetime.datetime.now(datetime.timezone.utc)
    stamp = built.strftime("%Y-%m-%dT%H:%M:%SZ")
    title = "Calendar, January 6, 1960, to 1970; with the presidential primaries of 1972 and 1976"
    ident = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, SITE + "calendar.epub"))
    tp = (f"<h1>{ebooks.esc(title)}</h1>"
          "<p>The calendar of the 1968 series, as the site prints it: every day of every page, with its entries, "
          "notes, footnotes and thread links; a file a month.</p>"
          f'<p>Built {built:%b. %-d, %Y}, from the pages at <a href="{SITE}cal.html">{SITE}cal.html</a>. Links to '
          "names, works and other pages open the site.</p>"
          "<p>Left out: the pages' navigator and visibility controls, the threads' statements, the indicator tables, "
          "the maps, and the days' documents lists (the documents are in the daybook's monthly ebooks).</p>")
    navl, cur_y = [], None
    for y, m, label, fn, weeks in nav:
        if y != cur_y:
            if cur_y is not None:
                navl.append("</ol></li>")
            navl.append(f'<li><a href="{fn}#mo{m}">{y}</a><ol>')
            cur_y = y
        wk = "".join(f'<li><a href="{f}#{ebooks.esc(i)}">{ebooks.esc(t)}</a></li>' for f, i, t in weeks)
        navl.append(f'<li><a href="{fn}#mo{m}">{ebooks.esc(label)}</a>' + (f"<ol>{wk}</ol>" if wk else "") + "</li>")
    navl.append("</ol></li>")
    navx = ('<nav epub:type="toc" id="toc"><h1>Contents</h1><ol><li><a href="title.xhtml">Title page</a></li>'
            + "".join(navl) + "</ol></nav>")
    items = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
             '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
             '<item id="css" href="style.css" media-type="text/css"/>',
             '<item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>']
    refs = ['<itemref idref="title"/>', '<itemref idref="nav"/>']
    for k, (name, label, _) in enumerate(body_files):
        items.append(f'<item id="f{k}" href="{name}" media-type="application/xhtml+xml"/>')
        refs.append(f'<itemref idref="f{k}"/>')
    opf = ('<?xml version="1.0" encoding="utf-8"?>\n'
           '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="en">\n'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
           f'<dc:identifier id="uid">{ident}</dc:identifier>\n<dc:title>{ebooks.esc(title)}</dc:title>\n'
           '<dc:language>en</dc:language>\n<dc:creator>The 1968 series</dc:creator>\n'
           f'<dc:source>{SITE}cal.html</dc:source>\n<meta property="dcterms:modified">{stamp}</meta>\n'
           '</metadata>\n<manifest>\n' + "\n".join(items) + '\n</manifest>\n<spine toc="ncx">\n'
           + "\n".join(refs) + "\n</spine>\n</package>\n")
    pts, order = [], 0
    for y, m, label, fn, weeks in nav:
        order += 1
        pts.append(f'<navPoint id="n{order}" playOrder="{order}"><navLabel><text>{ebooks.esc(label)}</text>'
                   f'</navLabel><content src="{fn}#mo{m}"/></navPoint>')
    ncx = ('<?xml version="1.0" encoding="utf-8"?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" '
           f'xml:lang="en">\n<head><meta name="dtb:uid" content="{ident}"/><meta name="dtb:depth" content="1"/>'
           '<meta name="dtb:totalPageCount" content="0"/><meta name="dtb:maxPageNumber" content="0"/></head>\n'
           f'<docTitle><text>{ebooks.esc(title)}</text></docTitle>\n<navMap>{"".join(pts)}</navMap>\n</ncx>\n')
    container = ('<?xml version="1.0" encoding="utf-8"?>\n'
                 '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
                 '</rootfiles></container>\n')
    files = [("META-INF/container.xml", container), ("OEBPS/content.opf", opf), ("OEBPS/toc.ncx", ncx),
             ("OEBPS/style.css", css or ""), ("OEBPS/title.xhtml", ebooks.page(title, tp)),
             ("OEBPS/nav.xhtml", ebooks.page("Contents", navx))]
    files += [(f"OEBPS/{n}", ebooks.page(lab, b)) for n, lab, b in body_files]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    ebooks.write_epub(out, files)
    raw = sum(len(b.encode()) if isinstance(b, str) else len(b) for _, b in files)
    return out, raw, len(body_files)


if __name__ == "__main__":
    p, raw, n = build(sys.argv[1] if len(sys.argv) > 1 else OUT)
    print(f"{p}: {os.path.getsize(p) / 1e6:.1f} MB ({raw / 1e6:.0f} MB uncompressed, {n} files)")
    errs = ebooks.validate(p)
    print(f"validate: {len(errs)} problems", *errs[:20], sep="\n  ")
