"""Visibility on the page (notes/proposals/visibility-spec.md, §6-§7; phase 3, §9.3, Nov. 12, 2026): every calendar
page (each year's, the primaries', and each year's block in the reader, series.html) carries its claims as spans and
the panel that filters them. The compute is tools/bib/vis.py; this module renders what it computes. It grew out of the
October 1962 prototype (tools/vis/prototype.py, now a wrapper that builds that one month with this code), which the
owner passed on Nov. 11, 2026: "The visibility setup looks good to go."

    tools/bib/vispage.py    the spans, the panel's HTML, the cache, the assets
    tools/bib/vispage.css   the panel's and the claims' style  }  written once a build as build/vis/vispage-<hash>.css
    tools/bib/vispage.js    the panel's script                 }  and .js, linked from each page that has a panel

STYLE
 1. Once a build. The claims of every calendar entry are computed once (vis.entry_claims, the registry and the polities
    read once for the whole pass) on the first entry a page renders, and kept by entry id for the rest of the run: the
    year pages and the reader's blocks read the same cache. Nothing is stored; every tag and date is derived (§8).
 2. The spans. A calendar entry's `c` (a dated or undated entry, not a thread's statement) is rendered unit by unit
    (tools/bib/claims.py, STYLE 1) with the page's own renderer, a span a claim, `<span class="cl" ...>`; the units are
    found in the entry's own rendering in order, and the text between them (the spaces) stays outside the spans, so
    with the spans taken out the line is byte for byte what it was. Where a unit's rendering is not found in order (a
    link or a title that the whole line renders and the unit alone does not), the entry is one span, unmapped, its
    claims' spans merged, the earliest of each date. An entry of one claim is one span. The li takes `data-cl="1"`.
    The renderer's link count (the reader's home page quotes it) is put back after the units are rendered.
 3. A span's data: data-u, the unit's letter (`all` where the entry is one claim); data-d, the claim's date (the
    entry's, the first day of a loose one); data-r, the reference "at the time", only where it is not the next day (a
    loose date: the day after its window's end, vis.py STYLE 3); data-t, its tags at the time (vis.py, STYLE 6);
    data-p, each polity's P and A spans, [nonpublic from, public from], compact: `US/P=,1996-10-01/A,=`, a polity's
    tag code, then each of P and A, its two dates, empty for none, `=` for the claim's own date, `?` public but not
    known when; data-um, unmapped (a faint dotted underline: the panel's legend says what it means, no hover on each);
    data-x, nothing computable (the placeholder `US:all`, §7). Short, so a year's page grows by about a seventh.
 4. The panel (§6): on a year's page after the contents, above the threads; in the reader, a year's block's after its
    lede, above its threads. Polities a cell each: the US, the USSR, China, France, Germany, the UK; Other, its states
    folded below it (those any claim of the page, or the block, carries, at any date); public and nonpublic indented
    under each. A polity's line sets both its sub-items ("mixed" where they differ); Other's line every other state's.
    Each toggle cycles on, greyed, off, in words. The P/A switch: by provenance, by address, either. The pin: a date,
    empty for "at the time". Defaults: the US on, every other polity greyed, either, no pin. The summary line counts
    the page's (the block's) claims in full, greyed, not yet known (at a pin) and hidden, and its entries shown. Its
    ids carry the block's key in the reader (`cal1962--visibility`), none on a page (`visibility`).
 5. The rule (§6, the prototype's STYLE 4): a claim shows in full if any of its tags is on, greyed if none is on and
    one is greyed, hidden if all are off. A tag's item is its polity's public or nonpublic; "by provenance" counts
    only its P, "by address" only its A; `US:all` is the US's public and nonpublic both, under any switch. At a pin
    before a claim's date the claim is greyed and marked not yet known, whatever the toggles (§5), the placeholder's
    too. An entry takes its claims' fullest state; greyed, its note and its lines go grey with it; hidden, it is
    hidden; a day all of whose entries are hidden has its date dimmed.
 6. Memory (§6): the choices in localStorage (`bib-vis-v1`), one state for every page and every panel; a state of a
    polity a page does not list is kept for the pages that do. Every read and write is in try/catch: with storage
    blocked the page starts from the defaults and works the same. 390 px: two columns of cells, the bar wraps.
 7. Assets (as tools/bib/vnmap.py's): the CSS and the script are written once a build to build/vis/, named by their
    content's hash, and linked from the head and the foot of each page holding a panel; nothing is inlined.
"""
import hashlib
import json
import html
import os

from . import store, vis

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(store.ROOT, "build")
TOP = [("us", "US"), ("ussr", "USSR"), ("prc", "China"), ("fr", "France"), ("frg", "Germany"), ("uk", "UK")]
MARK = "<!--vis-panel-->"
_C = {}                    # the build's cache (STYLE 1): series, claims by id, assets
PAGE = {"used": set()}     # the tag codes the page (the block) being rendered carries
STATS = {"entries": 0, "claims": 0, "merged": 0, "unmapped": 0, "placeholder": 0}
MERGED = []                # the entries made one span (STYLE 2), for a reader of the report


def esc(t):
    return html.escape(str(t), quote=True)


def claims(series, e):
    """The entry's claims, from the build's cache (STYLE 1)."""
    if _C.get("series") is not series:
        _C.clear()
        _C["series"] = series
        _C["by_id"] = {x["id"]: cls for _, x, cls in vis.entry_claims(series)}
    return _C["by_id"].get(e["id"])


def begin():
    """A page, or a block of the reader, begins: its polities counted afresh."""
    PAGE["used"] = set()


def _date(v, d):
    return "" if not v else "=" if v == d else str(v)


def encode(pol, d):
    """data-p (STYLE 3): 'US/P=,1996-10-01/A,= USSR/A=,1996-10-01'."""
    out = []
    for X in sorted(pol, key=vis.order_key):
        code = vis.tag_code(X)
        PAGE["used"].add(code)
        rec = pol[X]
        out.append(code + "".join(f"/{k}{_date(rec[k][0], d)},{_date(rec[k][1], d)}" for k in ("P", "A") if k in rec))
    return " ".join(out)


def merge_pols(cls):
    """The claims' polities merged: for each polity and P/A, the earliest nonpublic and public dates."""
    out = {}
    for cl in cls:
        for X, rec in (cl.get("polities") or {}).items():
            o = out.setdefault(X, {})
            for k, (np_from, pub) in rec.items():
                a, b = o.get(k, [None, None])
                a = min([x for x in (a, np_from) if x] or [None])
                dated = [x for x in (b, pub) if x and x != "?"]
                b = min(dated) if dated else (b or pub)
                o[k] = [a, b]
    return out


def span(inner, cl, unit, pol):
    d = cl.get("date") or ""
    for t in cl["tags"]:
        PAGE["used"].add(t.split(":")[0])
    a = [f'data-u="{esc(unit)}"', f'data-d="{esc(d)}"']
    ref = cl.get("ref")
    if d and ref and ref != vis.plus_days(d, vis.REF_DAYS):
        a.append(f'data-r="{esc(ref)}"')
    a.append(f'data-t="{esc(" ".join(cl["tags"]))}"')
    p = encode(pol, d)
    if p:
        a.append(f'data-p="{esc(p)}"')
    if cl["unmapped"]:
        a.append('data-um="1"')
    if not cl["computed"]:
        a.append('data-x="1"')
    STATS["claims"] += 1
    STATS["unmapped"] += 1 if cl["unmapped"] else 0
    STATS["placeholder"] += 0 if cl["computed"] else 1
    return f'<span class="cl" {" ".join(a)}>{inner}</span>'


def c_html(series, lst, e, whole, render):
    """The entry's `c`, rendered as `whole`, with its claims as spans (STYLE 2); None where the entry has none.
    render(text): a unit rendered as the page renders `c`."""
    if lst.kind != "calendar" or e["id"].startswith(f"{lst.key}.thread.") or not isinstance(e.get("c"), str) \
            or not e.get("c"):
        return None
    cls = claims(series, e)
    if not cls:
        return None
    STATS["entries"] += 1
    if len(cls) == 1:
        return span(whole, cls[0], cls[0]["unit"], cls[0].get("polities") or {})
    out, pos = [], 0
    for cl in cls:
        part = render(cl["text"])
        i = whole.find(part, pos) if part else -1
        if i < 0 or whole[pos:i].strip():
            break
        out.append((whole[pos:i], part))
        pos = i + len(part)
    else:
        if not whole[pos:].strip():
            return "".join(gap + span(part, cl, cl["unit"], cl.get("polities") or {})
                           for (gap, part), cl in zip(out, cls)) + whole[pos:]
    STATS["merged"] += 1
    MERGED.append(e["id"])
    one = dict(cls[0], unmapped=True, computed=any(c["computed"] for c in cls),
               tags=sorted({t for c in cls for t in c["tags"]}))
    return span(whole, one, "all", merge_pols(cls))


def panel(prefix=""):
    """The panel's HTML (STYLE 4), for the polities the page (the block) carries. prefix: the reader's block key and
    '--', so the ids are the page's own."""
    pol = vis.polities()["polities"]
    by_code = {vis.tag_code(k): k for k in pol}
    top_codes = [vis.tag_code(k) for k, _ in TOP]
    others = sorted(c for c in PAGE["used"] if c not in top_codes and c != "US")

    def label(code):
        name = (pol.get(by_code.get(code)) or {}).get("name") or code
        return (name if len(name) <= 14 or len(code) > 8 else code), name

    def cell(code, short, full, tail=""):
        return (f'<div class="vcell" role="group" aria-label="{esc(full)}">'
                f'<button type="button" class="vt top" data-k="{esc(code)}" data-lvl="line" data-name="{esc(full)}" '
                f'title="{esc(full)} ({esc(code)}): the claims carrying its tags"><span class="vl">{esc(short)}'
                f'<span class="vn"></span></span><span class="vs">on</span></button>'
                f'<button type="button" class="vt sub" data-k="{esc(code)}" data-lvl="public" data-name="{esc(full)}, public">'
                f'<span class="vl">public</span><span class="vs">on</span></button>'
                f'<button type="button" class="vt sub" data-k="{esc(code)}" data-lvl="nonpublic" '
                f'data-name="{esc(full)}, nonpublic"><span class="vl">nonpublic</span><span class="vs">on</span></button>'
                f'{tail}</div>')

    cells = [cell(vis.tag_code(k), short, (pol.get(k) or {}).get("name") or short) for k, short in TOP]
    other_meta, ocells = [], []
    for code in others:
        short, full = label(code)
        other_meta.append([code, short])
        ocells.append(cell(code, short, full))
    p = esc(prefix)
    cells.append(cell("OTHER", "Other", "Every other state",
                      f'<button type="button" class="vfold" aria-controls="{p}vother" aria-expanded="false">'
                      f'Show the {len(others)} states</button>'))
    meta = {"top": [[vis.tag_code(k), s] for k, s in TOP], "other": other_meta}
    return (f'<section class="vis" id="{p}vis" aria-labelledby="{p}visibility">'
            f'<h3 id="{p}visibility" data-short="Visibility">Visibility</h3>'
            f'<p class="logic">Whose record each claim is, and who knew it. Tap a toggle to cycle it: on, greyed, off. A claim '
            f'shows in full if any of its tags is on; greyed if none is on and one is greyed; hidden if all are off. '
            f'A polity\'s own line sets its public and nonpublic both. A dotted underline: an unmapped entry, filtered as a '
            f'whole.</p>'
            f'<div class="vgrid">{"".join(cells)}</div>'
            f'<div class="vother" id="{p}vother" hidden><div class="vgrid">{"".join(ocells)}</div></div>'
            f'<div class="vbar"><div><span class="lab" id="{p}vpalab">Tags by</span><span class="vpa" role="group" '
            f'aria-labelledby="{p}vpalab"><button type="button" data-pa="p">provenance</button>'
            f'<button type="button" data-pa="a">address</button><button type="button" data-pa="either">either</button>'
            f'</span></div>'
            f'<div class="vpin"><label class="lab" for="{p}vpin">Pin date</label><input type="date" class="vpinin" '
            f'id="{p}vpin" min="1960-01-01" max="2030-12-31" aria-describedby="{p}vpinnote">'
            f'<span class="vnote" id="{p}vpinnote">empty: at the time</span>'
            f'<button type="button" class="vpinclr" hidden>Clear: at the time</button></div></div>'
            f'<div class="vfoot"><p class="vsum" aria-live="polite"></p>'
            f'<button type="button" class="vreset">Defaults</button></div>'
            f'<script type="application/json" class="vismeta">{json.dumps(meta)}</script></section>')


def fill(text, prefix=""):
    """The panel put at its mark, for the page (the block) just rendered; no panel where it holds no claim."""
    if MARK not in text:
        return text
    return text.replace(MARK, panel(prefix) if PAGE["used"] else "", 1)


def _put(rel, data):
    path = os.path.join(OUT, rel)
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    return rel


def assets():
    """The CSS and the script beside the pages (STYLE 7): their paths from a page in build/."""
    if "assets" not in _C:
        out = []
        for ext in ("css", "js"):
            data = open(os.path.join(HERE, f"vispage.{ext}"), "rb").read()
            out.append(_put(f"vis/vispage-{hashlib.sha1(data).hexdigest()[:10]}.{ext}", data))
        _C["assets"] = tuple(out)
    return _C["assets"]


def inject(page):
    """The assets linked from a page that holds a panel."""
    if 'class="vis"' not in page or 'class="vis-css"' in page:
        return page
    css, js = assets()
    page = page.replace("</head>", f'<link class="vis-css" rel="stylesheet" href="{css}">\n</head>', 1)
    return page.replace("</body>", f'<script src="{js}"></script>\n</body>', 1)


def report():
    s = STATS
    return (f"visibility (every page and the reader): {s['entries']:,} entries rendered, {s['claims']:,} claim spans ({s['unmapped']:,} unmapped, "
            f"{s['placeholder']:,} US:all), {s['merged']:,} entries one span (units not found in their rendering)")
