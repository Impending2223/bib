"""Permalinks (the owner, Nov. 22, 2026: "Is there a place we could put a permalink to a particular entry ... Perhaps a
little hyperlinked box ... that, when clicked, navigates to the permalink, and right-clicked and copied, or the
mobile-equivalent, yields the permalink to the clipboard?"). Approved: a resolver independent of the pages, and the same
mark on the Names pages. Declined: the id on hover, a highlight on arrival, a copy button, a permalink a footnote.

STYLE
 1. The mark. Every calendar entry, a subentry too (not a thread's statement), carries a plain link to its permalink,
    `<a href="e.html#ID" class="pl" title="Permalink">□</a>`: a real link, so a click goes there and "Copy link" (a
    long press on a phone) yields the permalink. Muted, not underlined; in the corner at the entry's text size (the
    owner, Nov. 22, 2026: □ in the corner, at text size; a small glyph's misalignment distracts, and an inline glyph
    does not sit centered after a closing quotation mark). Where it stands is one setting, PLACE:
    "corner", the entry's box's bottom right (the box set relative, its last block kept clear of the mark), clear of
    the dateline at the top right and of the thread line's ⟨⟨ ⟩⟩ at the foot; "inline", after the entry's text, its
    last full stop (and any footnote mark after it), GAP before it. The glyph is GLYPH. The mark stands outside the
    claims' spans (vispage.py, STYLE 2), after the footnote marks (footnotes.py), and the reader's search leaves it out.
 2. The Names pages (lives.py): each calendar entry a person's Life gives, the same mark, by the same setting (corner:
    the paragraph's bottom right; inline: after the line's last full stop).
 3. The resolver. `e.html` at the site's root reads its hash, looks it up in `e.json`, and goes on with
    location.replace to the page and anchor that hold the entry now, an alias (a combined entry's DROP id) to its
    entry; an id it does not know, one line, "Entry not found", and a link to the calendar's index. The pages split
    as their size directs (pages.py, calsplit.py); the permalink does not change.
 4. e.json, compact, written with the calendar's pages from the anchors they hold (calsplit.REAL): `k` the list's key;
    `d` the one page where the calendar is not split; `m` {YYYY-MM: page}, the month's page (calsplit.years); `s` the
    ids' slugs (`cal.1961-04-17.cuba`: `cuba`), the commonest first; `e` {date as the id writes it: the slugs' indexes
    in base 36, space-separated}, every id the pages hold; `x` {id: page}, an id whose page is not its month's (a year's
    or a moved entry's, one of another form); `a` {alias: id}. An id is known if `x` or `e` holds it; its page is `x`'s,
    else its month's (a year alone: its first month's); its anchor is itself. resolve() is the script's rule in Python.
"""
import json
import os
import re

from . import calsplit

PERMALINK_PLACE = "corner"     # "corner" (the box's bottom right) or "inline" (after the text's last full stop)
PERMALINK_GLYPH = "\u25a1"     # □ WHITE SQUARE, at the text's size (the owner's choice, Nov. 22, 2026)
PERMALINK_GAP = " "            # inline only: " ", "\u2002" (en space) or "\u2003" (em space)

PAGE = "e.html"
DATA = "e.json"


def _esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def href(eid, site=""):
    return f"{site}{PAGE}#{eid}"


def mark(eid, site=""):
    return f'<a href="{_esc(href(eid, site))}" class="pl" title="Permalink">{PERMALINK_GLYPH}</a>'


def in_text(body, eid, site=""):
    """The entry's last line of text, with the mark after it where the mark is inline (STYLE 1)."""
    return f"{body}{PERMALINK_GAP}{mark(eid, site)}" if PERMALINK_PLACE == "inline" and body else body


def in_box(eid, inlined=False, site=""):
    """The mark at the box's foot where it is in the corner (an inline mark with no text to follow goes there too)."""
    return "" if PERMALINK_PLACE == "inline" and inlined else mark(eid, site)


def style():
    common = ("a.pl,a.pl:hover,a.pl:focus-visible{color:var(--muted);text-decoration:none;font-weight:400;"
              "font-style:normal}\n"
              "#pv a.pl{display:none}\n")
    if PERMALINK_PLACE == "inline":
        place = "a.pl{font-size:.85em;white-space:nowrap}\n"
    else:
        place = ("ol.e>li:has(>a.pl),.lvl:has(>a.pl){position:relative}\n"
                 "ol.e>li>a.pl,.lvl>a.pl{position:absolute;right:0;bottom:.45rem;font-size:1em;line-height:1}\n"
                 "ol.e>li>:has(+a.pl),.lvl:has(>a.pl){padding-right:1.5em}\n")
    return ('<style id="plstyle">\n/* the permalink mark (tools/bib/permalink.py, STYLE 1) */\n' + common + place
            + "</style>")


def inject(page):
    """The mark's style, where the page has marks."""
    if 'class="pl"' not in page or 'id="plstyle"' in page:
        return page
    return page.replace("</head>", style() + "\n</head>", 1)


# ---------------------------------------------------------------- the map (STYLE 4)

def _id_re(key):
    return re.compile(rf"^{re.escape(key)}\.(\d{{4}}(?:-\d\d){{0,2}})\.(.+)$")


def _rule(D, date):
    if D.get("d"):
        return D["d"]
    if len(date) >= 7:
        return D["m"].get(date[:7])
    ms = sorted(k for k in D["m"] if k[:4] == date[:4])
    return D["m"][ms[0]] if ms else None


def emap(lst, home):
    """e.json's map: home is {entry id: the page (no .html) that holds it}; an id no page holds is left out."""
    split = bool(calsplit.cfg(lst))
    D = {"k": lst.key, "d": None if split else lst.key, "m": calsplit.years(lst) if split else {}}
    rx = _id_re(lst.key)
    by, count, x, al = {}, {}, {}, {}
    for _, e in lst.entries():
        eid = e["id"]
        if eid.startswith(f"{lst.key}.thread.") or not home.get(eid):
            continue
        pg = home[eid]
        m = rx.match(eid)
        if m:
            by.setdefault(m.group(1), []).append(m.group(2))
            count[m.group(2)] = count.get(m.group(2), 0) + 1
            if _rule(D, m.group(1)) != pg:
                x[eid] = pg
        else:
            x[eid] = pg
        for a in e.get("aliases") or []:
            al[str(a)] = eid
    slugs = sorted(count, key=lambda s: (-count[s], s))
    ix = {s: i for i, s in enumerate(slugs)}
    D["s"] = slugs
    D["e"] = {d: " ".join(_b36(ix[s]) for s in ss) for d, ss in sorted(by.items())}
    D["x"] = dict(sorted(x.items()))
    D["a"] = dict(sorted(al.items()))
    return D


def _b36(n):
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    while True:
        n, r = divmod(n, 36)
        out = digits[r] + out
        if not n:
            return out


def resolve(D, eid):
    """(page, anchor) for an id or an alias, or None: the rule e.html's script keeps (STYLE 4)."""
    eid = D["a"].get(eid, eid)
    m = _id_re(D["k"]).match(eid)
    known = eid in D["x"]
    if not known and m and m.group(1) in D["e"]:
        try:
            i = D["s"].index(m.group(2))
        except ValueError:
            i = -1
        known = i >= 0 and _b36(i) in D["e"][m.group(1)].split(" ")
    if not known:
        return None
    pg = D["x"].get(eid) or (_rule(D, m.group(1)) if m else None)
    return (pg, eid) if pg else None


def homes(lst):
    """{entry id: page}: the anchors the built pages hold (calsplit.REAL), else the data's (calsplit._homes); one page
    where the calendar is not split."""
    if not calsplit.cfg(lst):
        return {e["id"]: lst.key for _, e in lst.entries()}
    files = [p["page"] for p in calsplit.parts(lst)]
    data = calsplit._homes(lst)
    out = {}
    for _, e in lst.entries():
        h = calsplit.REAL.get(e["id"])
        h = data.get(e["id"]) if h is None else h
        if h is not None:
            out[e["id"]] = files[h]
    return out


SCRIPT = r"""(function(){
  var M=document.getElementById('m');
  function nf(){M.innerHTML='Entry not found. <a href="IX.html">The calendar’s index</a>.';}
  function rule(D,d){
    if(D.d) return D.d;
    if(d.length>=7) return D.m[d.slice(0,7)]||null;
    var ks=Object.keys(D.m).filter(function(k){return k.slice(0,4)===d;}).sort();
    return ks.length?D.m[ks[0]]:null;
  }
  function find(D,id){
    id=D.a[id]||id;
    var rx=new RegExp('^'+D.k.replace(/\./g,'\\.')+'\\.(\\d{4}(?:-\\d\\d){0,2})\\.(.+)$'), m=rx.exec(id);
    var known=Object.prototype.hasOwnProperty.call(D.x,id);
    if(!known&&m&&D.e[m[1]]){ var i=D.s.indexOf(m[2]); known=i>=0&&D.e[m[1]].split(' ').indexOf(i.toString(36))>=0; }
    if(!known) return null;
    var p=D.x[id]||(m?rule(D,m[1]):null);
    return p?p+'.html#'+id:null;
  }
  var D=null;
  function go(){
    var h=location.hash.slice(1); try{h=decodeURIComponent(h);}catch(e){}
    if(!h){nf();return;}
    var t=find(D,h); if(t) location.replace(t); else nf();
  }
  fetch('DATA').then(function(r){if(!r.ok) throw r; return r.json();}).then(function(d){D=d; go();})
    .catch(function(){M.innerHTML='The entry could not be looked up. <a href="IX.html">The calendar’s index</a>.';});
  window.addEventListener('hashchange',function(){if(D) go();});
})();"""


def page(ix):
    """e.html: the resolver (STYLE 3)."""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Entry</title>
<style>:root{{--ink:#1A1E26;--bg:#F4F6F9}}@media (prefers-color-scheme:dark){{:root{{--ink:#E6E8EC;--bg:#15181D}}}}
body{{margin:0;padding:3rem 1rem;background:var(--bg);color:var(--ink);font:18px/1.55 Georgia,serif}}
p{{max-width:36rem;margin:0 auto}}a{{color:inherit}}</style></head>
<body><p id="m">Finding the entry…</p>
<noscript><p>Without scripts: <a href="{ix}.html">the calendar’s index</a>.</p></noscript>
<script>
/* a permalink, e.html#<entry id>, to the page that holds the entry now (tools/bib/permalink.py, STYLE 3) */
{SCRIPT.replace("IX", ix).replace("DATA", DATA)}
</script>
</body></html>
"""


def write(out, lst):
    """e.json and e.html at the site's root, from the calendar's built pages; their paths."""
    from .store import atomic_write
    D = emap(lst, homes(lst))
    pj, ph = os.path.join(out, DATA), os.path.join(out, PAGE)
    atomic_write(pj, json.dumps(D, ensure_ascii=False, separators=(",", ":")) + "\n")
    atomic_write(ph, page(lst.key))
    return [pj, ph]


def load(out):
    p = os.path.join(out, DATA)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None
