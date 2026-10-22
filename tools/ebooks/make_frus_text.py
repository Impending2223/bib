"""The text of every FRUS document the daybook files (daybook/<YYYY-MM>.yaml), in XHTML, for the ebooks.
# Usage: python3 tools/ebooks/make_frus_text.py [--cache DIR] [--out DIR] [--month YYYY-MM ...]  (--month last)
#   Reads the Office of the Historian's TEI files (github.com/HistoryAtState/frus, volumes/<vol>.xml; public domain
#   and CC0, its LICENSE.md), from DIR if they are there (the cache tools/daybook/make_daybook.py fills), else fetched
#   into DIR. Writes sources/frus-text/<YYYY-MM>.json.xz: {"source", "license", "docs": {key: xhtml}}, a document a key
#   ("frus:frus1961-63v14/d1", the daybook's). tools/bib/ebooks.py binds them into the month's EPUB; the build needs
#   neither the TEI nor the network. Rerun after make_daybook.py.
#
# STYLE (the conversion; mechanical: the text is FRUS's own, nothing summarized or left out but the page breaks
# and the images):
#  1. A document: its heading as FRUS prints it, number first ("1. Telegram From the Mission at Berlin ..."), an <h3>;
#     then the body in order: the opener (place and date, the subject and participants lists), paragraphs, lists,
#     tables, quotations, the closer and signature, attachments under an <h4> each.
#  2. Footnotes: each note's mark where it stands (a superscript link), the notes at the document's end in a
#     <div class="fns">, each linked back; the source note first, as FRUS numbers it. An inline note stays inline.
#  3. Type: italic, bold, small capitals, superscript and subscript, underline, struck text as FRUS marks them.
#     Paragraph alignment (center, right, flush left) as a class. Whitespace collapsed.
#  4. Links: a FRUS cross-reference to the document's page on history.state.gov; persons, places, terms and dates as
#     plain text. An image: "[Image not reproduced: see the document's page.]".
#  5. Ids unique within a book: the volume and the document's id ("f196163v14d1"), its notes "f196163v14d1n3".
"""
import html
import json
import lzma
import os
import re
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "sources", "frus-text")
RAW = "https://raw.githubusercontent.com/HistoryAtState/frus/master/volumes/"
HSG = "https://history.state.gov/historicaldocuments/"
T = "{http://www.tei-c.org/ns/1.0}"
FNS = "{http://history.state.gov/frus/ns/1.0}"
XID = "{http://www.w3.org/XML/1998/namespace}id"
SOURCE = ("Foreign Relations of the United States (U.S. Department of State, Office of the Historian), "
          "TEI files at https://github.com/HistoryAtState/frus")
LICENSE = ("Public domain: a work of the United States government; the Office of the Historian also waives its "
           "rights worldwide under CC0 1.0 (the repository's LICENSE.md)")
UNKNOWN = Counter()


def esc(t):
    return html.escape(t, quote=False)


def attr(t):
    return html.escape(t, quote=True)


def ws(t):
    return re.sub(r"\s+", " ", t or "")


def local(e):
    t = e.tag
    if not isinstance(t, str):
        return ""
    if t.startswith(T):
        return t[len(T):]
    if t.startswith(FNS):
        return "frus:" + t[len(FNS):]
    return t


HI = {"italic": ("i", ""), "strong": ("b", ""), "bold": ("b", ""), "superscript": ("sup", ""), "sub": ("sub", ""),
      "subscript": ("sub", ""), "smallcaps": ("span", "sc"), "underline": ("u", ""), "roman": ("span", "rm"),
      "strikethrough": ("del", "")}
P_CLASS = {"center": "c", "right": "r", "flushleft": "fl", "sectiontitleital": "st", "strong": "b"}
BLOCKY = {"list", "table", "figure", "frus:attachment", "div", "postscript"}


class Doc:
    def __init__(self, vol, did):
        self.vol, self.did = vol, did
        self.pre = "f" + re.sub(r"[^a-z0-9]", "", vol[4:].lower()) + did
        self.notes = []

    def note_ref(self, n, body):
        k = len(self.notes) + 1
        self.notes.append((n or str(k), body, k))
        return (f'<sup class="nr"><a id="{self.pre}r{k}" href="#{self.pre}n{k}" epub:type="noteref">'
                f'{esc(n or str(k))}</a></sup>')


def has_block(e):
    for c in e:
        n = local(c)
        if n in BLOCKY or (n == "quote" and any(local(g) in ("p", "list") for g in c)):
            return True
        if n == "note":
            continue
        if has_block(c):
            return True
    return False


def ref_url(doc, target):
    target = (target or "").strip()
    if target.startswith("http"):
        return target
    m = re.match(r"#(d\d+\w*)$", target)
    if m:
        return f"{HSG}{doc.vol}/{m.group(1)}"
    m = re.match(r"(frus[\w-]+)(?:#|/)(\w+)$", target)
    if m:
        return f"{HSG}{m.group(1)}/{m.group(2)}"
    m = re.match(r"(frus[\w-]+)$", target)
    if m:
        return f"{HSG}{m.group(1)}"
    return None


def inner(e, doc, inline):
    out = [esc(ws(e.text))]
    for c in e:
        out.append(render(c, doc, inline))
        out.append(esc(ws(c.tail)))
    return "".join(out)


def block(tag, cls, body):
    body = body.strip()
    if not body:
        return ""
    c = f' class="{cls}"' if cls else ""
    return f"<{tag}{c}>{body}</{tag}>"


def para_of(e, doc, cls):
    """A TEI paragraph: a <p>, or a <div class="p"> where it holds a list, a table or an attachment."""
    if has_block(e):
        return block("div", ("p " + cls).strip(), inner(e, doc, False))
    return block("p", cls, inner(e, doc, True))


def render(e, doc, inline):
    n = local(e)
    if not n:                                          # a comment or processing instruction
        return ""
    if n in ("pb", "milestone", "anchor"):
        return ""
    if n == "lb":
        return "<br/>"
    if n == "note":
        if e.get("rend") == "inline" or e.get("place") == "inline":
            return f'<span class="ni">{inner(e, doc, True).strip()}</span>'
        body = inner(e, doc, False) if has_block(e) or any(local(c) == "p" for c in e) else inner(e, doc, True)
        if not any(local(c) == "p" for c in e):
            body = f'<div class="p">{body.strip()}</div>' if has_block(e) else f"<p>{body.strip()}</p>"
        return doc.note_ref(e.get("n"), body)
    if n == "hi":
        tag, cls = HI.get(e.get("rend") or "", ("span", ""))
        c = f' class="{cls}"' if cls else ""
        return f"<{tag}{c}>{inner(e, doc, True)}</{tag}>"
    if n == "del":
        return f"<del>{inner(e, doc, True)}</del>"
    if n == "add":
        return f"<ins>{inner(e, doc, True)}</ins>"
    if n == "ref":
        u = ref_url(doc, e.get("target"))
        body = inner(e, doc, True)
        marks = "".join(re.findall(r'<sup class="nr">.*?</sup>', body))     # no link inside a link: the marks after
        body = re.sub(r'<sup class="nr">.*?</sup>', "", body)
        return (f'<a href="{attr(u)}">{body}</a>' if u and "<a " not in body else body) + marks
    if n == "figure" or n == "graphic":
        caption = " ".join(ws("".join(h.itertext())).strip() for h in e if local(h) in ("head", "figDesc", "p"))
        t = "[Image not reproduced: see the document’s page.]" + (f" {esc(caption)}" if caption else "")
        return f'<span class="fig">{t}</span>' if inline else f'<p class="fig">{t}</p>'
    if inline:                                         # a block element met inside a paragraph: inline, marked
        if n in ("p", "dateline", "salute", "signed", "seg", "opener", "closer", "head", "label", "item", "quote",
                 "postscript", "byline", "docAuthor", "docDate", "trailer", "cit", "bibl", "l"):
            return inner(e, doc, True)
        if n == "lg":
            return "<br/>".join(inner(c, doc, True).strip() for c in e if local(c) == "l")
        if n in ("persName", "placeName", "gloss", "date", "term", "orgName", "affiliation", "idno", "rs", "name",
                 "unclear", "sic", "corr", "choice", "time", "roleName", "geogName", "num", "abbr", "expan",
                 "foreign", "title", "emph", "measure", "frus:attachment", "list", "table", "row", "cell", "div"):
            return inner(e, doc, True)
        UNKNOWN[n] += 1
        return inner(e, doc, True)
    # block context
    if n == "p":
        return para_of(e, doc, P_CLASS.get(e.get("rend") or "", ""))
    if n in ("opener", "closer"):
        parts = [esc(ws(e.text)).strip()]
        for c in e:
            parts.append(render(c, doc, False) if local(c) in ("dateline", "salute", "signed", "seg", "p", "list",
                                                                 "address", "note", "lb", "pb") else
                         block("p", "", render(c, doc, True)))
            parts.append(block("p", "", esc(ws(c.tail))))
        return block("div", n, "".join(p for p in parts if p))
    if n == "dateline":
        right = "right" in (e.get("rendition") or "") + (e.get("rend") or "")
        return block("p", "dl" + (" r" if right else ""), inner(e, doc, True))
    if n == "seg":
        return block("p", "seg", inner(e, doc, True))
    if n == "salute":
        return block("p", "sal", inner(e, doc, True))
    if n == "signed":
        return block("p", "sg", inner(e, doc, True))
    if n == "lg":                                      # verse: a line a line
        return block("p", "lg", "<br/>".join(inner(c, doc, True).strip() for c in e if local(c) == "l"))
    if n in ("l", "cit", "bibl"):
        return block("p", "", inner(e, doc, True))
    if n == "address":
        return block("p", "adr", "<br/>".join(inner(c, doc, True).strip() for c in e if local(c) == "addrLine")
                     or inner(e, doc, True))
    if n == "list":
        items, label = [], None
        lh = ""
        for c in e:
            cn = local(c)
            if cn == "head":
                lh = block("p", "lh", inner(c, doc, True))
            elif cn == "label":
                label = inner(c, doc, True).strip()
            elif cn == "item":
                body = inner(c, doc, False) if has_block(c) else inner(c, doc, True)
                lab = f'<span class="lb">{label}</span> ' if label else ""
                items.append(f"<li>{lab}{body.strip()}</li>")
                label = None
            elif cn in ("note", "pb", "lb"):
                r = render(c, doc, True)
                if r and items:
                    items[-1] = items[-1][:-5] + r + "</li>"
            elif cn:
                items.append(f"<li>{render(c, doc, True).strip()}</li>")
        typ = e.get("type") or ""
        cls = "tl" + (f" {typ}" if re.match(r"^[a-z]+$", typ) else "")
        return lh + (f'<ul class="{cls}">{"".join(items)}</ul>' if items else "")
    if n == "table":
        rows, cap = [], ""
        for c in e:
            cn = local(c)
            if cn == "head":
                cap = f"<caption>{inner(c, doc, True).strip()}</caption>"
            elif cn == "row":
                cells = []
                for cell in c:
                    if local(cell) != "cell":
                        continue
                    tag = "th" if cell.get("role") == "label" or c.get("role") == "label" else "td"
                    a = ""
                    if (cell.get("rows") or "1") not in ("", "1") and cell.get("rows").isdigit():
                        a += f' rowspan="{cell.get("rows")}"'
                    if (cell.get("cols") or "1") not in ("", "1") and cell.get("cols").isdigit():
                        a += f' colspan="{cell.get("cols")}"'
                    body = inner(cell, doc, False) if has_block(cell) else inner(cell, doc, True)
                    cells.append(f"<{tag}{a}>{body.strip()}</{tag}>")
                if cells:
                    rows.append(f"<tr>{''.join(cells)}</tr>")
        return f'<table class="tt">{cap}{"".join(rows)}</table>' if rows else ""
    if n == "quote":
        if any(local(c) in ("p", "list", "table") for c in e):
            return block("blockquote", "", inner(e, doc, False))
        if e.get("rend") == "blockquote":
            return block("blockquote", "", f"<p>{inner(e, doc, True).strip()}</p>")
        return block("p", "", inner(e, doc, True))
    if n in ("frus:attachment", "div"):
        out = []
        t = esc(ws(e.text)).strip()
        if t:
            out.append(f"<p>{t}</p>")
        for c in e:
            if local(c) == "head":
                out.append(block("h4", "", inner(c, doc, True)))
            else:
                out.append(render(c, doc, False))
            tl = esc(ws(c.tail)).strip()
            if tl:
                out.append(f"<p>{tl}</p>")
        return block("div", "att", "".join(out))
    if n == "postscript":
        return block("div", "ps", inner(e, doc, False) if has_block(e) or any(local(c) == "p" for c in e)
                     else f"<p>{inner(e, doc, True).strip()}</p>")
    if n == "head":
        return block("p", "h", inner(e, doc, True))
    if n in ("label", "item", "trailer", "byline", "docAuthor", "docDate"):
        return block("p", "", inner(e, doc, True))
    if n in ("persName", "placeName", "gloss", "date", "term", "orgName", "affiliation", "idno", "rs", "name",
             "unclear", "sic", "corr", "choice", "time", "roleName", "geogName", "num", "abbr", "expan", "foreign",
             "title", "emph", "measure"):              # phrases: inline wherever they stand
        return inner(e, doc, True)
    UNKNOWN[n] += 1
    return block("div", "", inner(e, doc, False)) if has_block(e) else block("p", "", inner(e, doc, True))


def document(vol, d):
    """The XHTML of one document div (STYLE 1-5)."""
    doc = Doc(vol, d.get(XID))
    out = []
    for c in d:
        if local(c) == "head":
            out.append(f'<h3 id="{doc.pre}">{inner(c, doc, True).strip()}</h3>')
        else:
            out.append(render(c, doc, False))
        tl = esc(ws(c.tail)).strip()
        if tl:
            out.append(f"<p>{tl}</p>")
    if doc.notes:
        fn = []
        for mark, body, k in doc.notes:
            back = f'<a class="nb" href="#{doc.pre}r{k}">{esc(mark)}</a> '
            body = body.replace("<p>", "<p>" + back, 1) if body.startswith("<p>") else back + body
            fn.append(f'<aside id="{doc.pre}n{k}" epub:type="footnote" class="fn">{body}</aside>')
        out.append(f'<div class="fns">{"".join(fn)}</div>')
    return "".join(x for x in out if x)


def daybook_keys(months=None):
    keys = {}
    for f in sorted(os.listdir(os.path.join(ROOT, "daybook"))):
        if not re.match(r"\d{4}-\d\d\.yaml$", f) or (months and f[:7] not in months):
            continue
        for x in (yaml.safe_load(open(os.path.join(ROOT, "daybook", f), encoding="utf-8")) or {}).get("docs") or []:
            if x.get("src") == "frus":
                keys[x["key"]] = f[:7]
    return keys


def main():
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else os.path.join(tempfile.gettempdir(),
                                                                                                "frus-tei")
    months = set(sys.argv[sys.argv.index("--month") + 1:]) if "--month" in sys.argv else None
    out_dir = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else OUT
    keys = daybook_keys(months)
    vols = sorted({k[5:].split("/")[0] for k in keys})
    by_month = {}
    for vol in vols:
        path = os.path.join(cache, vol + ".xml")
        if not os.path.exists(path):
            os.makedirs(cache, exist_ok=True)
            req = urllib.request.Request(RAW + vol + ".xml", headers={"User-Agent": "bib-ebooks"})
            open(path, "wb").write(urllib.request.urlopen(req, timeout=300).read())
        root = ET.parse(path).getroot()
        for d in root.iter(T + "div"):
            if d.get("type") != "document":
                continue
            k = f"frus:{vol}/{d.get(XID)}"
            if k in keys:
                by_month.setdefault(keys[k], {})[k] = document(vol, d)
        print(vol, file=sys.stderr)
    os.makedirs(out_dir, exist_ok=True)
    total = 0
    for m, docs in sorted(by_month.items()):
        data = json.dumps({"source": SOURCE, "license": LICENSE, "month": m, "docs": docs}, ensure_ascii=False,
                          sort_keys=True, separators=(",", ":")).encode("utf-8")
        p = os.path.join(out_dir, f"{m}.json.xz")
        with open(p, "wb") as f:
            f.write(lzma.compress(data, preset=9 | lzma.PRESET_EXTREME))
        total += os.path.getsize(p)
        print(m, len(docs), os.path.getsize(p) // 1024, "KB")
    missing = set(keys) - {k for d in by_month.values() for k in d}
    print("written", sum(len(d) for d in by_month.values()), "documents;", total // 1024 // 1024, "MB;",
          len(missing), "daybook keys not found in the TEI")
    if UNKNOWN:
        print("unknown elements:", UNKNOWN.most_common(20), file=sys.stderr)


if __name__ == "__main__":
    main()
