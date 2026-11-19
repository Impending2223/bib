"""The pages' sizes, their budget, and the splits the budget directs (the owner, Nov. 19, 2026: "Do we not have a pass
that tells us the size of each page, on calendar pages and otherwise, directs splits, and refactors navigation and
pointers after the split pass? Please implement one if not.").

    ./bib pages              every page in build/ with its size and its entries or rows, against its budget; a page
                             over budget marked, with the split its structure proposes
    ./bib pages --plan       write those splits into the plan (pages.yaml; the calendar's into lists/cal/list.yaml
                             `split:`), for the next build to apply; then `./bib build`, `./bib links`, `./bib pages`

pages.yaml, the one place for both:
    budget          bytes a page may hold, its HTML alone (the days' month files load when opened: lazydays.py)
    budgets         a family's own budget (cal: the owner's page-size rule for the calendar, "some 8 MB", Nov. 12)
    fill            a split packs its parts to this share of the budget, room to grow before the next split
    exempt          {page: why}: reported, never split (series.html, the one-page reader)
    names           {letter: [{page, from, label}]}: a letter's page over budget, in surname ranges, each part by the
                    first key it holds (a person's key, `lives.key_of`; one person is never split)
    works           {by: letter}: the A–Z bibliography a page a letter (works-a.html ...; works.html the index)
    executive, congress   {parts: [{page, label, sections: [h2 id, ...]}]}: the page cut at its own top sections
                    (the terms; the Congresses), each part a page, the old page the index
    retired         pages a split has replaced: each forwards a link by its anchor to the page that now holds it

STYLE:
 1. A page's size is its file's bytes. Its units, where its structure gives them: a calendar part's entries, a Names
    page's persons, Works' works, the Executive's offices, the Congresses' seats; else its anchors.
 2. A split follows the page's own structure: the calendar by quarter, then month (calsplit's names: cal1967Q1,
    cal1967-04); Names by surname range within a letter (names-ma-mc.html, labelled "Ma–Mc"); Works by letter;
    the Executive by term, Congress by Congress (their h2 sections, packed in order to the fill).
 3. Pointers: every link to an anchor on a page that is split goes to the part that holds it, from every page: the
    builders ask here (names_href, works_href), and route() rewrites the rest at the write (as calsplit.route does
    for the calendar). Inside a part, a bare '#X' held by another part goes to that part.
 4. Old addresses keep working: a split page's old file (names-m.html, works.html, executive.html, congress.html: the
    last three the index now) carries a script that sends an anchor it does not hold to the part that does, by a
    map (forward_script; compressed by an anchor's first word where that word names one part).
 5. Navigation: each part carries its family's bar (the A–Z, a split letter's ranges under it, the terms, the
    Congresses), the page's own unlinked, and at its foot the part before and after ("‹ Ma–Mc · Index · Md–Mi ›").
"""
import bisect
import json
import os
import re

from . import store

PATH = os.path.join(store.ROOT, "pages.yaml")
CACHE = os.path.join(store.ROOT, ".cache", "pages-map.json")
DEFAULT_BUDGET = 5_000_000
MB = 1_000_000

_CONF = {}


def conf():
    """pages.yaml, read once (an empty plan where there is none: the fixture)."""
    if "c" not in _CONF:
        _CONF["c"] = (store.load_yaml(PATH) or {}) if os.path.exists(PATH) else {}
    return _CONF["c"]


def reset():
    _CONF.clear()
    WORKS.clear()
    MAPS.clear()
    NAMES.clear()


NAMES = {}        # "fn": the maker of {anchor: page} for the names in ranges (lives.anchors), set by prepare; "map"


def names_anchors():
    """{anchor: page} for the Names entries in ranges, made once on first use: a form joined in an entry (a span)
    goes where its person is, not where its own key would file it."""
    if "map" not in NAMES:
        NAMES["map"] = NAMES["fn"]() if NAMES.get("fn") else {}
    return NAMES["map"]


def family(name):
    """The family a built page belongs to: 'cal', 'names', 'works', 'executive', 'congress', or the page itself."""
    n = name[:-5] if name.endswith(".html") else name
    if re.match(r"^cal(\d{4}|primaries$|\d\d$)", n) or n == "cal":
        return "cal"
    for f in ("names", "works", "executive", "congress", "lives"):
        if n == f or n.startswith(f + "-"):
            return f
    return n


def budget(name):
    c = conf()
    return int((c.get("budgets") or {}).get(family(name), c.get("budget") or DEFAULT_BUDGET))


def fill():
    return float(conf().get("fill") or 0.7)


def exempt(name):
    return (conf().get("exempt") or {}).get(name)


# ---------------------------------------------------------------- Names (lives.py): a letter in surname ranges

def names_parts(letter):
    """[{page, from, label}] for a letter split in ranges, else None."""
    ps = (conf().get("names") or {}).get(letter)
    return ps or None


def names_page(letter, key):
    """The page (without .html) that holds the person keyed `key` filed under `letter`."""
    ps = names_parts(letter)
    if not ps:
        return f"names-{letter}"
    froms = [str(p["from"]) for p in ps]
    return ps[max(0, bisect.bisect_right(froms, key) - 1)]["page"]


def names_href(letter, key):
    return f"{names_page(letter, key)}.html#{key}"


def names_sequence(letters):
    """[(page, label, letter)] every Names page in order: a letter, or its ranges."""
    out = []
    for L in letters:
        ps = names_parts(L)
        if ps:
            out += [(p["page"], p.get("label") or p["page"], L) for p in ps]
        else:
            out.append((f"names-{L}", L.upper(), L))
    return out


def _before(s):
    """The last prefix before s, for a range's label ('mc' -> 'mb'; 'mca' -> 'mc')."""
    return s[:-1] + chr(ord(s[-1]) - 1) if s[-1:] > "a" else s[:-1]


def _cap(s):
    return s[:1].upper() + s[1:]


def names_ranges(letter, keys_sizes, target):
    """[{page, from, label}] for a letter's persons [(key, bytes)] packed in key order to the target: each part's
    first key's shortest prefix that still sorts after the last key before it."""
    ks = sorted(keys_sizes)
    chunks, cur, size = [], [], 0
    for k, n in ks:
        if cur and size + n > target:
            chunks.append(cur)
            cur, size = [], 0
        cur.append(k)
        size += n
    if cur:
        chunks.append(cur)
    if len(chunks) < 2:
        return None
    froms = [letter]
    for prev, ch in zip(chunks, chunks[1:]):
        last, first = prev[-1], ch[0]
        p = next((first[:i] for i in range(1, len(first) + 1) if first[:i] > last), first)
        froms.append(p)
    out = []
    for i, f in enumerate(froms):
        lo = f if i else letter + "a"
        hi = _before(froms[i + 1]) if i + 1 < len(froms) else letter + "z"
        lo, hi = re.sub(r"[^a-z]", "", lo) or letter, re.sub(r"[^a-z]", "", hi) or letter
        out.append({"page": f"names-{lo}-{hi}", "from": f, "label": f"{_cap(lo)}–{_cap(hi)}"})
    seen = set()
    for p in out:                      # two ranges of one label (a prefix the rule shortened): numbered
        while p["page"] in seen:
            p["page"] += "x"
        seen.add(p["page"])
    return out


# ---------------------------------------------------------------- Works (bibliography.py): a page a letter

WORKS = {}        # card id or alias -> page, when the A-Z bibliography is split (prepare)


def works_split():
    return (conf().get("works") or {}).get("by") == "letter"


def works_page_of_letter(L):
    return f"works-{L}"


def works_href(cid):
    """The card's entry in the A–Z bibliography: works.html#id, or its letter's page."""
    return f"{WORKS.get(cid, 'works')}.html#{cid}"


def prepare(series):
    """The maps the builders and the router read before any page is written: the works' letters (from the cards'
    filing, bibliography.letters)."""
    WORKS.clear()
    if conf().get("names") and series is not None:
        from . import lives
        NAMES["fn"] = lambda: lives.anchors(series)
    if works_split() and series is not None:
        from . import bibliography
        for cid, L in bibliography.letters(series).items():
            WORKS[cid] = works_page_of_letter(L)
        for L in set(WORKS.values()):
            WORKS[f"az-{L[len('works-'):]}"] = L


# ---------------------------------------------------------------- the Executive, Congress: cut at the h2 sections

MAPS = {}         # family -> {anchor: page}, for the families cut at their sections (cut; the cache between builds)


def sections_plan(fam):
    return ((conf().get(fam) or {}).get("parts")) or None


H2 = re.compile(r'<h2\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h2>', re.S)
IDS = re.compile(r'\sid="([^"]+)"')
TAGS = re.compile(r"<[^>]+>")


def anatomy(page):
    """(pre, intro, [(h2 id, label, html)], post) of a built page: the template before <main>'s contents, the
    contents before the first h2, each h2 section, the template after."""
    a = page.index('<main id="doc">') + len('<main id="doc">')
    b = page.rindex("</main>")
    pre, body, post = page[:a], page[a:b], page[b:]
    ms = list(H2.finditer(body))
    if not ms:
        return pre, body, [], post
    secs = []
    for m, n in zip(ms, ms[1:] + [None]):
        secs.append((m.group(1), TAGS.sub("", m.group(2)).strip(), body[m.start():n.start() if n else len(body)]))
    return pre, body[:ms[0].start()], secs, post


def pack(sizes, target):
    """Consecutive items [(id, bytes)] packed in order: [[id, ...], ...], each run at most the target (an item
    larger alone)."""
    out, cur, n = [], [], 0
    for k, s in sizes:
        if cur and n + s > target:
            out.append(cur)
            cur, n = [], 0
        cur.append(k)
        n += s
    if cur:
        out.append(cur)
    return out


def _slug(sid):
    m = re.match(r"^[a-z]+(\d{4})\d\d$", sid)          # t196101: 1961
    if m:
        return m.group(1)
    m = re.match(r"^[a-z](\d+)$", sid)                  # c87: 87
    return m.group(1) if m else re.sub(r"[^a-z0-9]+", "-", sid.lower()).strip("-")


def sections_parts(fam, secs, target):
    """[{page, label, sections}] for a page's h2 sections [(id, label, bytes)] packed to the target."""
    lab = {s: l for s, l, _ in secs}
    out = []
    for run in pack([(s, n) for s, _, n in secs], target):
        a, b = _slug(run[0]), _slug(run[-1])
        page = f"{fam}-{a}" + (f"-{b}" if b != a else "")
        label = lab[run[0]] if len(run) == 1 else f"{lab[run[0]]} to {lab[run[-1]]}"
        out.append({"page": page, "label": label, "sections": run})
    seen = set()
    for p in out:
        while p["page"] in seen:
            p["page"] += "x"
        seen.add(p["page"])
    return out


TITLE = re.compile(r"<title>(.*?)</title>", re.S)
CRUMB = re.compile(r'(<div id="crumb"><b>)(.*?)(</b>)', re.S)


def _retitle(pre, title):
    pre = TITLE.sub(lambda m: f"<title>{title}</title>", pre, count=1)
    return CRUMB.sub(lambda m: m.group(1) + title + m.group(3), pre, count=1)


def cut(fam, page, title):
    """{file name: html}: a page cut at its h2 sections by the plan (sections_plan): each part a page (the intro, the
    parts' bar, its sections, the bar again with the parts before and after); the old page the index (the intro, the
    parts with their sections, and the script that forwards an old link's anchor). MAPS[fam] the anchors' pages."""
    plan = sections_plan(fam)
    if not plan:
        return {f"{fam}.html": page}
    pre, intro, secs, post = anatomy(page)
    by_id = {s: (l, h) for s, l, h in secs}
    placed = {s for p in plan for s in p["sections"]}
    rest = [s for s, _, _ in secs if s not in placed]            # a section the plan has not seen: on the last part
    parts = [dict(p, sections=[s for s in p["sections"] if s in by_id]) for p in plan]
    if rest:
        parts[-1]["sections"] += rest
    parts = [p for p in parts if p["sections"]]
    amap = {}
    for a in IDS.findall(intro):
        amap.setdefault(a, fam)
    for p in parts:
        for s in p["sections"]:
            for a in IDS.findall(by_id[s][1]):
                amap.setdefault(a, p["page"])
    MAPS[fam] = amap
    out = {}
    for i, p in enumerate(parts):
        body = "".join(by_id[s][1] for s in p["sections"])
        main = intro + bar(fam, parts, i) + body + seam(fam, parts, i)
        html = _retitle(pre, f"{title}: {p['label']}") + "\n" + main + "\n" + post
        out[f"{p['page']}.html"] = route_own(html, fam, p["page"])
    idx = [intro, bar(fam, parts, None)]
    for p in parts:
        idx.append(f'<h2 id="pt-{p["page"]}" data-short="{p["label"]}"><a href="{p["page"]}.html">{p["label"]}</a></h2>')
        idx.append('<ul class="pgl">' + "".join(f'<li><a href="{p["page"]}.html#{s}">{by_id[s][0]}</a></li>'
                                                 for s in p["sections"]) + "</ul>")
    html = pre + "\n" + "\n".join(idx) + "\n" + post
    html = html.replace("</body>", forward_script(amap, fam, here=True) + "\n</body>", 1)
    out[f"{fam}.html"] = route_own(html, fam, fam)
    return out


def bar(fam, parts, cur):
    """The family's parts across the column, the page's own unlinked (STYLE 5)."""
    xs = []
    for i, p in enumerate(parts):
        if i == cur:
            xs.append(f'<span aria-current="page">{p["label"]}</span>')
        else:
            xs.append(f'<a href="{p["page"]}.html">{p["label"]}</a>')
    head = f'<a href="{fam}.html">Index</a>' if cur is not None else '<span aria-current="page">Index</span>'
    return f'<nav class="pgparts" aria-label="Parts"><p>{head} · ' + " · ".join(xs) + "</p></nav>" + PART_CSS


def seam(fam, parts, i):
    """At a part's foot: the part before and the part after (STYLE 5)."""
    xs = []
    if i > 0:
        xs.append(f'<a href="{parts[i - 1]["page"]}.html">‹ {parts[i - 1]["label"]}</a>')
    xs.append(f'<a href="{fam}.html">Index</a>')
    if i + 1 < len(parts):
        xs.append(f'<a href="{parts[i + 1]["page"]}.html">{parts[i + 1]["label"]} ›</a>')
    return '<nav class="pgseam" aria-label="Parts"><p>' + " · ".join(xs) + "</p></nav>"


PART_CSS = ("<style>nav.pgparts p,nav.pgseam p{font-family:var(--sans);font-size:.8rem;line-height:1.7;color:var(--muted);"
            "margin:1rem 0}nav.pgparts a,nav.pgseam a{color:inherit}nav.pgparts span[aria-current]{color:var(--ink);"
            "font-weight:600}nav.pgseam p{margin-top:2.5rem}ul.pgl{font-size:.9rem}</style>")


def load_cache():
    try:
        return json.load(open(CACHE, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_cache(fam):
    c = load_cache()
    c[fam] = MAPS.get(fam) or {}
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    store.atomic_write(CACHE, json.dumps(c, sort_keys=True, separators=(",", ":")))


def ensure_map(fam, build):
    """MAPS[fam] for the router: cut this build (`build` makes the page), or the last build's, kept in .cache."""
    if fam in MAPS or not sections_plan(fam):
        return
    c = load_cache().get(fam)
    if c:
        MAPS[fam] = c
        return
    page = build()
    if page:
        cut(fam, page, fam)
        save_cache(fam)


# ---------------------------------------------------------------- the router (STYLE 3)

HREF = re.compile(r'href="([^"#]*)#([^"]+)"')


def _home(base, anchor):
    """The page (without .html) a link to base#anchor goes to now, or None to leave it."""
    if base.startswith("names-") and len(base) == len("names-x.html"):
        L = base[6]
        if names_parts(L):
            exact = names_anchors()
            return exact.get(anchor) or names_page(L, anchor)
        return None
    if base == "works.html":
        return WORKS.get(anchor) if WORKS else None
    fam = base[:-5]
    if fam in MAPS:
        return MAPS[fam].get(anchor)
    return None


def active():
    c = conf()
    return bool(c.get("names") or WORKS or MAPS)


def route(page):
    """Every link to an anchor on a split page, to the page that holds it now (STYLE 3)."""
    if not active():
        return page

    def sub(m):
        path, anchor = m.group(1), m.group(2)
        base = path.rsplit("/", 1)[-1]
        if not base:
            return m.group(0)
        h = _home(base, anchor)
        if h and f"{h}.html" != base:
            return f'href="{path[:len(path) - len(base)]}{h}.html#{anchor}"'
        return m.group(0)
    return HREF.sub(sub, page)


def route_own(page, fam, me):
    """In a part of a family cut at its sections: a bare '#X' that another part holds goes there."""
    amap = MAPS.get(fam) or {}

    def sub(m):
        path, anchor = m.group(1), m.group(2)
        if path:
            return m.group(0)
        h = amap.get(anchor)
        if h and h != me:
            return f'href="{h}.html#{anchor}"'
        return m.group(0)
    return HREF.sub(sub, page)


# ---------------------------------------------------------------- old addresses (STYLE 4)

def compress(amap):
    """{'t': {first word: page}, 'x': {anchor: page}}: an anchor's first word (to the first '-' or '.') where every anchor
    of that word is on one page; the rest one by one."""
    word = {}
    for a, p in amap.items():
        w = re.split(r"[-.]", a, maxsplit=1)[0]
        word.setdefault(w, set()).add(p)
    t = {w: next(iter(ps)) for w, ps in word.items() if len(ps) == 1}
    x = {a: p for a, p in amap.items() if re.split(r"[-.]", a, maxsplit=1)[0] not in t}
    return {"t": t, "x": x}


def forward_script(amap, me, here=False):
    """The script that sends a link's anchor to the page that holds it: on the index (here) only an anchor the page
    does not hold."""
    data = json.dumps(dict(compress(amap), me=me), ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).replace("</", "<\\/")
    return f"""<script>
/* an old link, forwarded by its anchor to the part that holds it (tools/bib/pages.py, STYLE 4) */
(function(){{
  var D={data};
  function go(){{
    var h=location.hash.slice(1); try{{ h=decodeURIComponent(h); }}catch(e){{}}
    if(!h||document.getElementById(h)) return;
    var p=D.x[h]||D.t[h.split(/[-.]/)[0]];
    if(p&&p!==D.me) location.replace(p+'.html#'+h);
  }}
  go(); window.addEventListener('hashchange',go);
}})();
</script>"""


def names_stub(letter, alias):
    """A letter's old page (names-m.html), now in ranges: sends an anchor to its range's page, an alias to its
    person's page; with none, to the letter's first range."""
    data = json.dumps({"f": [[str(p["from"]), p["page"]] for p in names_parts(letter)], "a": alias},
                      ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    first = names_parts(letter)[0]["page"]
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Names: {letter.upper()}</title>
<style>:root{{--ink:#1a1a1a;--bg:#f6f4ef}}@media (prefers-color-scheme:dark){{:root{{--ink:#e8e6e1;--bg:#16181c}}}}
body{{margin:0;padding:3rem 1rem;background:var(--bg);color:var(--ink);font:18px/1.55 Georgia,serif}}
p{{max-width:36rem;margin:0 auto}}a{{color:inherit}}</style></head>
<body><p>The names under {letter.upper()} are now on {len(names_parts(letter))} pages: """ + ", ".join(
        f'<a href="{p["page"]}.html">{p.get("label") or p["page"]}</a>' for p in names_parts(letter)) + f""". This address
forwards to the page that holds the person it named; without one, to the first.</p>
<script>
/* an old link, forwarded by its anchor to the range that holds it (tools/bib/pages.py, STYLE 4) */
(function(){{
  var D={data};
  function go(){{
    var h=location.hash.slice(1); try{{ h=decodeURIComponent(h); }}catch(e){{}}
    if(!h){{ location.replace('{first}.html'); return; }}
    if(D.a[h]){{ location.replace(D.a[h]); return; }}
    var p=D.f[0][1]; for(var i=0;i<D.f.length;i++) if(h>=D.f[i][0]) p=D.f[i][1];
    location.replace(p+'.html#'+h);
  }}
  go(); window.addEventListener('hashchange',go);
}})();
</script>
</body></html>
"""


def stub(title, to, amap, me):
    """A retired page: a line to its index, and the script that forwards its links."""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>:root{{--ink:#1a1a1a;--bg:#f6f4ef}}@media (prefers-color-scheme:dark){{:root{{--ink:#e8e6e1;--bg:#16181c}}}}
body{{margin:0;padding:3rem 1rem;background:var(--bg);color:var(--ink);font:18px/1.55 Georgia,serif}}
p{{max-width:36rem;margin:0 auto}}a{{color:inherit}}</style></head>
<body><p>This page is now in parts. This address forwards to the part that holds the place it named; without one,
to <a href="{to}.html">the index</a>.</p>
{forward_script(amap, me)}
<script>if(!location.hash)location.replace('{to}.html');</script>
</body></html>
"""


# ---------------------------------------------------------------- the pass: measure (STYLE 1), plan (STYLE 2)

UNITS = {"cal": (re.compile(r'<li id="cal\.\d'), "entries"),
         "names": (re.compile(r'<section class="lv"'), "persons"),
         "works": (re.compile(r'<p class="wk" id='), "works"),
         "executive": (re.compile(r'<tr\b'), "rows"),
         "congress": (re.compile(r'<tr\b'), "rows")}
ANCHOR = re.compile(r'\sid="')
LV = re.compile(r'<section class="lv" id="([^"]+)">')
MONTH = re.compile(r"^(\d{4})(\d\d)b?$")


def built(out):
    """{page name: path} of the built pages."""
    import glob
    return {os.path.basename(p): p for p in sorted(glob.glob(os.path.join(out, "*.html")))}


def stubbed(text):
    """A page that only forwards (an old address)."""
    return len(text) < 40000 and "location.replace" in text and '<main id="doc">' not in text


def measure(out):
    """[{page, bytes, units, unit, budget, over, exempt, stub, family}] for every built page, largest first: the
    HTML alone (a calendar page's days' month files load when opened, lazydays.py)."""
    rows = []
    for name, path in built(out).items():
        text = open(path, encoding="utf-8").read()
        fam = family(name)
        rx, unit = UNITS.get(fam, (ANCHOR, "anchors"))
        n = os.path.getsize(path)
        b = budget(name)
        rows.append({"page": name, "bytes": n, "units": len(rx.findall(text)), "unit": unit, "budget": b,
                     "over": n > b and not exempt(name), "exempt": exempt(name), "stub": stubbed(text),
                     "family": fam})
    return sorted(rows, key=lambda r: -r["bytes"])


def _sizes_of(text, rx_start, end_marks=("</main>",)):
    """[(key, bytes)] of the units a page holds, each from its start to the next's (the last to the end mark)."""
    ms = list(rx_start.finditer(text))
    if not ms:
        return []
    ends = [text.find(e, ms[-1].end()) for e in end_marks]
    end = min([e for e in ends if e > 0] or [len(text)])
    return [(m.group(1), (ms[i + 1].start() if i + 1 < len(ms) else end) - m.start()) for i, m in enumerate(ms)]


def propose(out, rows=None):
    """{family: proposal} for the families with a page over budget: what the plan would write (STYLE 2)."""
    rows = rows if rows is not None else measure(out)
    over = {r["family"] for r in rows if r["over"]}
    pages_ = built(out)
    prop = {}
    if "names" in over:
        letters = {}
        for r in rows:
            m = re.match(r"^names-([a-z])(?:-[a-z]+)?\.html$", r["page"])
            if m and not r["stub"]:
                letters.setdefault(m.group(1), []).append(r)
        props = {}
        for L, rs in sorted(letters.items()):
            if not any(x["over"] for x in rs):
                continue
            sizes, total, body = [], 0, 0
            for x in rs:
                text = open(pages_[x["page"]], encoding="utf-8").read()
                got = _sizes_of(text, LV, ('<p class="lvs"><a class="lvp" href="names', "<script>(function(){var m=",
                                           "</main>"))
                sizes += got
                total += x["bytes"]
                body += sum(n for _, n in got)
            overhead = (total - body) // max(1, len(rs))
            target = int(budget(f"names-{L}.html") * fill()) - overhead
            rng = names_ranges(L, sizes, target)
            if rng:
                props[L] = rng
        if props:
            prop["names"] = props
    if "works" in over and not works_split():
        prop["works"] = {"by": "letter"}
    for fam in ("executive", "congress"):
        if fam not in over:
            continue
        secs, intro = [], 0
        for r in rows:
            if r["family"] != fam or r["stub"]:
                continue
            if r["page"] == f"{fam}.html" and sections_plan(fam):
                continue                       # the index: the parts hold the sections
            text = open(pages_[r["page"]], encoding="utf-8").read()
            pre, it, ss, post = anatomy(text)
            secs += [(s, l, len(h)) for s, l, h in ss]
            intro = max(intro, len(pre) + len(it) + len(post))
        target = int(budget(f"{fam}.html") * fill()) - intro
        prop[fam] = {"parts": sections_parts(fam, secs, target)}
    if "cal" in over:
        c = calendar_proposal(out, rows)
        if c:
            prop["cal"] = c
    return prop


# ---------------------------------------------------------------- the calendar: its parts in list.yaml (calsplit)

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
ABBR = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]


def _calendar():
    s = store.Series()
    return next(l for l in s.lists.values() if l.kind == "calendar")


def calendar_proposal(out, rows):
    """[{page, into: [(kind, months)]}]: each calendar part over its budget, divided by calsplit's rule (the owner's
    names, Nov. 12, 2026: a half H1, H2, a quarter Q1-Q4, then a month, cal1964-01): into quarters, a quarter still
    over its budget into months. A new part's size is estimated as its months' share of the page and the rest of the
    page (the threads' index, the contents: in every part) whole."""
    from . import calsplit
    lst = _calendar()
    pages_ = built(out)
    res = []
    for p in calsplit.parts(lst):
        name = f"{p['page']}.html"
        r = next((x for x in rows if x["page"] == name), None)
        if not r or not r["over"]:
            continue
        text = open(pages_[name], encoding="utf-8").read()
        _, _, secs, _ = anatomy(text)
        months = {}
        for s, _, h in secs:
            m = MONTH.match(s)
            if m:
                k = f"{m.group(1)}-{m.group(2)}"
                months[k] = months.get(k, 0) + len(h)
        if not months:
            continue
        fixed = r["bytes"] - sum(months.values())
        b = budget(name)
        quarters = {}
        for k in sorted(months):
            quarters.setdefault((int(k[5:]) - 1) // 3, []).append(k)
        into = []
        for q, mk in sorted(quarters.items()):
            if len(quarters) > 1 and fixed + sum(months[k] for k in mk) <= b:
                into.append(("Q", mk))
            else:
                into += [("M", [k]) for k in mk]
        if len(into) < 2:
            continue
        res.append({"page": p["page"], "into": into, "est": [fixed + sum(months[k] for k in mk) for _, mk in into]})
    return res


def _part_fields(base, kind, mk, first_day=None):
    """A new calendar part's fields, in the forms of its siblings (list.yaml `split:`)."""
    y = int(mk[0][:4])
    m0, m1 = int(mk[0][5:]), int(mk[-1][5:])
    import calendar as C
    last = C.monthrange(y, m1)[1]
    d0 = first_day or f"{y}-{m0:02d}-01"
    if kind == "Q":
        page = f"cal{y}Q{(m0 - 1) // 3 + 1}"
    else:
        page = f"cal{y}-{m0:02d}"
    if m0 == m1:
        words, ab = f"{MONTHS[m0 - 1]} {y}", f"{ABBR[m0 - 1]} {y}"
        span = f"{ABBR[m0 - 1]} {int(d0[8:])}–{last}, {y}"
        h1 = f"{y}, {MONTHS[m0 - 1]}"
    else:
        words, ab = f"{MONTHS[m0 - 1]}–{MONTHS[m1 - 1]} {y}", f"{ABBR[m0 - 1]}–{ABBR[m1 - 1]} {y}"
        span = f"{ABBR[m0 - 1]} {int(d0[8:])}–{ABBR[m1 - 1]} {last}, {y}"
        h1 = f"{y}, {MONTHS[m0 - 1]}–{MONTHS[m1 - 1]}"
    title = str(base.get("title") or "")
    rest = title.split(": ", 1)[1] if ": " in title else ""
    out = {"from": d0, "page": page, "abbr": f"Cal. {ab}", "called": f"the calendar of {words}",
           "title": f"Calendar, {words}" + (f": {rest}" if rest else ""), "span": span,
           "page_title": f"Calendar, {words}", "h1": h1,
           "lede": f"Executive, legislative, judicial, and state events of {words}."}
    return out, (d0, f"{y}-{m1:02d}-{last:02d}")


def _yq(v):
    """A YAML scalar as list.yaml writes it: quoted where it must be."""
    v = str(v)
    if re.search(r":\s|\s#|^[*\[\]'\"{}&!|>%@`]|^\d{4}-\d\d-\d\d$|^\d", v):
        return "'" + v.replace("'", "''") + "'"
    return v


def apply_calendar(props, path=None):
    """Write the calendar's proposal into lists/cal/list.yaml: each divided part's item replaced by its new parts, the
    old page added to `retired_parts` (its page then forwards an old link: calsplit STYLE 14)."""
    from . import calsplit
    path = path or os.path.join(store.ROOT, "lists", "cal", "list.yaml")
    text = open(path, encoding="utf-8").read()
    lst = _calendar()
    ps = {p["page"]: p for p in calsplit.parts(lst)}
    done = []
    for pr in props:
        base = ps[pr["page"]]
        items, spans = [], []
        for j, (kind, mk) in enumerate(pr["into"]):
            first = str(base["from"]) if j == 0 and base.get("from") else None
            f, span = _part_fields(base, kind, mk, first)
            if j == 0 and not base.get("from"):        # the calendar's first part: no `from`, its first day its own
                f.pop("from")
                lo = re.search(r"(\w+\.?) (\d+)", str(base.get("span") or ""))
                if lo:
                    f["span"] = f["span"].replace(f"{f['span'].split()[0]} 1", f"{lo.group(1)} {lo.group(2)}", 1)
            items.append(f)
            spans.append(span)
        lines = []
        for f in items:
            ks = list(f)
            lines.append(f"  - {ks[0]}: {_yq(f[ks[0]])}")
            lines += [f"    {k}: {_yq(f[k])}" for k in ks[1:]]
        m = re.search(r"(?m)^  - (?:from: [^\n]*\n    )?page: " + re.escape(pr["page"]) + r"\n(?:    [^\n]*\n)*", text)
        if not m:
            raise ValueError(f"list.yaml: no part {pr['page']}")
        text = text[:m.start()] + "\n".join(lines) + "\n" + text[m.end():]
        lo = str(base.get("from") or spans[0][0])
        hi = spans[-1][1]
        rm = list(re.finditer(r"(?m)^  - \{page: [^\n]*\}\n", text[:text.index("\nsplit:")]))
        at = rm[-1].end()
        text = text[:at] + f"  - {{page: {pr['page']}, from: '{lo}', to: '{hi}'}}\n" + text[at:]
        done.append(pr["page"])
    store.atomic_write(path, text)
    return done


# ---------------------------------------------------------------- pages.yaml written

HEAD = """# The pages' size budget and the splits it directs (tools/bib/pages.py, its docstring; ./bib pages, ./bib pages --plan).
# budget: bytes a page may hold, its HTML alone; budgets: a family's own; fill: a split packs its parts to this share
# of the budget; exempt: reported, never split. The rest is the plan, written by `./bib pages --plan` (by hand only to
# set a split aside): names, a letter in surname ranges; works, a page a letter; executive and congress, their top
# sections in parts; retired, the pages a split replaced, each forwarding its old links. The calendar's parts are in
# lists/cal/list.yaml (`split:`, `retired_parts`).
"""


def write_conf(c, path=None):
    import yaml
    path = path or PATH
    keep = {k: c[k] for k in ("budget", "budgets", "fill", "why", "exempt", "works", "names", "executive", "congress",
                              "retired") if c.get(k) not in (None, {}, [])}
    store.atomic_write(path, HEAD + yaml.safe_dump(keep, sort_keys=False, allow_unicode=True, width=110))
    _CONF.clear()


def plan(out):
    """Write the proposal into the plan: pages.yaml for Names, Works, the Executive and Congress; list.yaml for the
    calendar. A page a split replaces is kept in `retired` (pages.yaml) or `retired_parts` (list.yaml)."""
    prop = propose(out)
    c = dict(conf())
    retired = list(c.get("retired") or [])
    if prop.get("names"):
        names = dict(c.get("names") or {})
        for L, rng in prop["names"].items():
            old = [p["page"] for p in names.get(L) or []]
            names[L] = rng
            retired += [p for p in old if p not in {x["page"] for x in rng}]
        c["names"] = dict(sorted(names.items()))
    if prop.get("works"):
        c["works"] = prop["works"]
    for fam in ("executive", "congress"):
        if prop.get(fam):
            old = [p["page"] for p in (c.get(fam) or {}).get("parts") or []]
            c[fam] = prop[fam]
            retired += [p for p in old if p not in {x["page"] for x in prop[fam]["parts"]}]
    c["retired"] = sorted(dict.fromkeys(retired))
    write_conf(c)
    cal = apply_calendar(prop["cal"]) if prop.get("cal") else []
    return prop, cal


def report(rows, prop=None):
    """The table `./bib pages` prints."""
    def mb(n):
        return f"{n / MB:.1f} MB" if n >= 100_000 else f"{n / 1000:.0f} KB"
    out = [f"{'page':<28} {'size':>9} {'units':>16}  budget"]
    for r in rows:
        if r["stub"]:
            continue
        mark = "OVER" if r["over"] else ("exempt" if r["exempt"] else "")
        out.append(f"{r['page']:<28} {mb(r['bytes']):>9} {r['units']:>8,} {r['unit']:<7}  {mb(r['budget']):>6} {mark}")
    stubs = [r["page"] for r in rows if r["stub"]]
    over = [r for r in rows if r["over"]]
    out.append(f"{len(rows) - len(stubs)} pages, {sum(r['bytes'] for r in rows if not r['stub']) / MB:.0f} MB; "
               f"{len(stubs)} forwarding stubs; {len(over)} over budget")
    for r in rows:
        if r["exempt"] and not r["stub"]:
            out.append(f"exempt: {r['page']}: {r['exempt']}")
    if prop:
        out.append("")
        out.append("Proposed splits (./bib pages --plan writes them; then ./bib build, ./bib links, ./bib pages):")
        for L, rng in (prop.get("names") or {}).items():
            out.append(f"  names-{L}: " + ", ".join(f"{p['page']} ({p['label']})" for p in rng))
        if prop.get("works"):
            out.append("  works: a page a letter (works-a.html ...), works.html the index")
        for fam in ("executive", "congress"):
            if prop.get(fam):
                out.append(f"  {fam}: " + ", ".join(f"{p['page']} ({len(p['sections'])} sections)"
                                                    for p in prop[fam]["parts"]))
        for pr in prop.get("cal") or []:
            out.append(f"  {pr['page']}: " + ", ".join(
                (_part_fields({}, k, mk)[0]["page"]) + f" (~{e / MB:.1f} MB)" for (k, mk), e in zip(pr["into"], pr["est"])))
    return "\n".join(out)
