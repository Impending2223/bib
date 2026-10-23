"""The Public Papers of the Presidents, 1960-69, from GPO's volumes on govinfo: the cite, the link, the text.

    sources/ppp-text/<package>.json.xz   each volume's items, their headings, dates, pages and cleaned text, with the
                             pagination marked ("[p. 123]"); made by tools/ppp/make_ppp_text.py (its docstring: the
                             reading and the cleaning), public domain; rules.json, the cleaning rules and their counts
    sources/ppp-matches.json the APP documents matched to items, each volume's particulars and an index of its items;
                             made by tools/ppp/match_app.py (its STYLE: the matching)

The build reads the matches file for the cites and links (the calendar's days, the Names, the Executive roster) and
the texts only for the ebooks (tools/bib/ebooks.py). Neither needs the network.

STYLE:
 1. The cite, the Bluebook's for the Public Papers: the volume's years, "Pub. Papers", the item's first page: "1961
    Pub. Papers 1", "1963–64 Pub. Papers 842", "1960–61 Pub. Papers 589". A year's two books are paginated through,
    so the years and the page find the item, and the cite names no book. In a calendar note the document's title
    comes first, then the cite, linked, then the date: "Inaugural Address, [1961 Pub. Papers 1](…) (Jan. 20, 1961)".
 2. The link: GPO's PDF of the volume on govinfo at the item's first page (`#page=N`, the PDF's page: govinfo gives
    these volumes no granules). The hover: the volume's title, the item's number and pages ("Public Papers of the
    Presidents of the United States: John F. Kennedy, 1961, item 1, pp. 1–3").
 3. Wherever the series linked an APP document that an item prints, the item's cite and link stand in its place:
    the daybook's President list, the calendar's notes (rewritten in the data by tools/ppp/relink.py), the Names'
    presidential documents, the Executive roster's sources. APP's link stays where nothing matches: the executive
    orders and proclamations (the volumes list them in an appendix and do not print them), the campaign of 1960,
    Nixon's first days, an item the OCR lost.
 4. A page marker in a text ("[p. 123]") shows as a small muted "p. 123" linked to its PDF page.
"""
import glob
import html
import json
import lzma
import os
import re

from . import store

TEXT = os.path.join(store.ROOT, "sources", "ppp-text")
MATCHES = os.path.join(store.ROOT, "sources", "ppp-matches.json")
APP = "https://www.presidency.ucsb.edu/documents/"
MARK = re.compile(r"\[p\. (\d+)\]")
KINDS = {"p", "s", "h", "b", "n", "f", "q"}

_cache = {}


def esc(t):
    return html.escape(str(t), quote=True)


def data():
    """The matches file: {stats, volumes, matches, unmatched_app, unmatched_ppp}; {} where it is not made."""
    if "m" not in _cache:
        _cache["m"] = json.load(open(MATCHES, encoding="utf-8")) if os.path.exists(MATCHES) else {}
    return _cache["m"]


def norm(url):
    u = (url or "").strip().replace("http://", "https://").rstrip("/")
    return u.replace("https://presidency.ucsb.edu/", "https://www.presidency.ucsb.edu/")


def item(pkg, n):
    """The item's particulars: {pkg, n, title, date, page, page_to, pdf, url, cite, hover}; None if not held."""
    v = data().get("volumes", {}).get(pkg)
    if not v:
        return None
    x = v["items"].get(str(n))
    if not x:
        return None
    title, date, page, page_to, pdf = x
    pp = f"p. {page}" if page == page_to or not page_to else f"pp. {page}–{page_to}"
    return {"pkg": pkg, "n": int(n), "title": title, "date": date, "page": page, "page_to": page_to, "pdf": pdf,
            "url": f"{v['pdf']}#page={pdf}", "cite": cite_of(v, page),
            "hover": f"{v['title']}, item {n}, {pp}", "years": v["years"]}


def cite_of(v, page):
    return f"{v['years']} Pub. Papers {page}"


def match(url):
    """The item an APP document's address matches (STYLE 3), or None."""
    m = data().get("matches", {}).get(norm(url))
    return item(*m) if m else None


def is_app(url):
    return "presidency.ucsb.edu/documents/" in (url or "")


def pdf_page(pkg, page):
    """The PDF page of a printed page of the volume, by its folio runs."""
    v = data().get("volumes", {}).get(pkg)
    if not v:
        return None
    for a, b, off in v["folios"]:
        if a <= page + off <= b:
            return page + off
    return None


def link_html(it, label=None, cls=None):
    """The item's cite (or label), linked to its first page (STYLE 2)."""
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="{esc(it["url"])}" title="{esc(it["hover"])}">{esc(label or it["cite"])}</a>'


# ---------------------------------------------------------------- the texts (the ebooks)

def volume(pkg):
    """A volume's file, its items in full."""
    if ("v", pkg) not in _cache:
        p = os.path.join(TEXT, f"{pkg}.json.xz")
        _cache[("v", pkg)] = json.loads(lzma.decompress(open(p, "rb").read())) if os.path.exists(p) else None
    return _cache[("v", pkg)]


def packages():
    return sorted(os.path.basename(p)[:-len(".json.xz")] for p in glob.glob(os.path.join(TEXT, "PPP-*.json.xz")))


def items_by_day():
    """{iso day: [(pkg, item)]}: every item under its date (or the date it is filed under), in the volume's order."""
    if "days" not in _cache:
        out = {}
        for pkg in packages():
            d = volume(pkg)
            for it in d["items"]:
                day = it.get("date") or it.get("filed")
                if day:
                    out.setdefault(day, []).append((pkg, it))
        _cache["days"] = out
    return _cache["days"]


def marked(t, pkg):
    """A block's text in XHTML, its page markers linked to their PDF pages (STYLE 4)."""
    v = data().get("volumes", {}).get(pkg) or {}
    out, last = [], 0
    for m in MARK.finditer(t):
        out.append(esc(t[last:m.start()]))
        p = pdf_page(pkg, int(m.group(1)))
        lab = f"p. {m.group(1)}"
        out.append(f'<a class="pg" href="{esc(v.get("pdf", ""))}#page={p}">{lab}</a>' if p and v
                   else f'<span class="pg">{lab}</span>')
        last = m.end()
    out.append(esc(t[last:]))
    return re.sub(r"\s{2,}", " ", "".join(out)).strip()


# ---------------------------------------------------------------- check

def problems():
    """The texts and the matches (check): errors [(where, message)], warnings."""
    errs, warns = [], []
    names = set()
    for p in glob.glob(os.path.join(TEXT, "*")):
        b = os.path.basename(p)
        if b == "rules.json":
            continue
        if not re.fullmatch(r"PPP-\d{4}-book\d\.json\.xz", b):
            errs.append((f"sources/ppp-text/{b}", "not a volume's file (PPP-<year>-book<n>.json.xz) or rules.json"))
            continue
        names.add(b[:-len(".json.xz")])
        try:
            d = json.loads(lzma.decompress(open(p, "rb").read()))
        except Exception as e:                              # noqa: BLE001
            errs.append((f"sources/ppp-text/{b}", f"not readable: {e}"))
            continue
        where = f"sources/ppp-text/{b}"
        prev_n, prev_page = 0, 0
        for it in d["items"]:
            w = f"{where} item {it['n']}"
            if it["n"] <= prev_n:
                errs.append((w, "item numbers not ascending"))
            if it["page"] is not None and (it["page"] < prev_page or (it["page_to"] or 0) < it["page"]):
                errs.append((w, f"pages out of order ({it['page']}–{it['page_to']})"))
            if not 1 <= it["pdf"] <= d["pages"]:
                errs.append((w, "PDF page outside the volume"))
            day = it.get("date") or it.get("filed")
            if not day or not (d["span"][0][:7] <= day[:7] <= d["span"][1][:7]):
                errs.append((w, f"date {day} outside the volume's span {d['span'][0]}–{d['span'][1]}"))
            if not it["text"] or any(k not in KINDS for k, t in it["text"]):
                errs.append((w, "no text, or a block of unknown kind"))
            else:
                first = MARK.match(it["text"][0][1])
                if it["page"] is not None and (not first or int(first.group(1)) != it["page"]):
                    errs.append((w, "the text does not open with its first page's marker"))
                pages = [int(x) for k, t in it["text"] for x in MARK.findall(t)]
                if pages != sorted(pages) or (pages and it["page_to"] is not None and pages[-1] > it["page_to"]):
                    errs.append((w, "page markers out of order or past the item's last page"))
            prev_n, prev_page = it["n"], it["page"] or prev_page
        if d.get("missing"):
            warns.append((where, f"items not found in the OCR: {', '.join(map(str, d['missing']))}"))
    m = data()
    if names and not m:
        errs.append(("sources/ppp-matches.json", "missing: run tools/ppp/match_app.py"))
    for url, (pkg, n) in (m.get("matches") or {}).items():
        if pkg not in names or item(pkg, n) is None:
            errs.append(("sources/ppp-matches.json", f"{url}: no item {pkg} #{n}"))
    # a list's link to an APP document the Public Papers print: tools/ppp/relink.py rewrites it (STYLE 3)
    rx = re.compile(r"\]\((https?://(?:www\.)?presidency\.ucsb\.edu/documents/[^)\s]+)\)")
    for p in glob.glob(os.path.join(store.ROOT, "lists", "*", "*.yaml")):
        t = open(p, encoding="utf-8").read()
        for mm in rx.finditer(t):
            if match(mm.group(1)):
                warns.append((f"{os.path.relpath(p, store.ROOT)}:{t.count(chr(10), 0, mm.start()) + 1}",
                              "an APP link the Public Papers print: run tools/ppp/relink.py"))
    if set(m.get("volumes", {})) - names:
        errs.append(("sources/ppp-matches.json", "volumes not in sources/ppp-text: "
                     + ", ".join(sorted(set(m["volumes"]) - names))))
    return errs, warns
