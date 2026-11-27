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
    threads         {slug: [{page, from, label}]}: a thread's page over budget in parts by date (threads.py, STYLE 6):
                    a year a part, a year over in quarters, a quarter over in months, small ones in a row packed to
                    the fill; the thread's own page then its index
    places          {slug: [{page, from, label}]}: a place's page in parts by date, as a thread's (placepages.py,
                    STYLE 4); a place the build had to divide before a plan held it, its parts as the build made them
                    (.cache/pages-map.json `places-planned`), written here so that they keep their names
    retired         pages a split has replaced: each forwards a link by its anchor to the page that now holds it

STYLE:
 1. A page's size is its file's bytes. Its units, where its structure gives them: a calendar part's entries, a Names
    page's persons, Works' works, the Executive's offices, the Congresses' seats; else its anchors.
 2. A split follows the page's own structure: the calendar by quarter, then month (calsplit's names: cal1967Q1,
    cal1967-04); Names by surname range within a letter (names-ma-mc.html, labelled "Ma–Mc"); Works by letter;
    the Executive by term, Congress by Congress (their h2 sections, packed in order to the fill); a thread's page by
    date (a year, a quarter, a month: threads-china-leadership-1960Q1).
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
import html
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
    for f in ("names", "works", "executive", "congress", "lives", "threads", "places"):
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
    i = max(0, bisect.bisect_right(froms, key) - 1)
    if ps[i].get("only") and key != str(ps[i]["only"]) and i + 1 < len(ps):    # a page of one person: his alone
        i += 1
    return ps[i]["page"]


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


def _readable(prefix):
    """A key's prefix as the name it begins ('kennedy-jo' -> 'Kennedy, Jo'; 'mcgo' -> 'Mcgo')."""
    w = [x for x in prefix.split("-") if x]
    if not w:
        return prefix
    return _cap(w[0]) + (", " + " ".join(_cap(x) for x in w[1:]) if len(w) > 1 else "")


def _cap(s):
    return s[:1].upper() + s[1:]


def names_ranges(letter, keys_sizes, target, names=None):
    """[{page, from, label}] for a letter's persons [(key, bytes)] packed in key order to the target: each part's
    first key's shortest prefix that still sorts after the last key before it; a range of one person labelled by his
    name as his entry writes it (names: {key: name})."""
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
        hi = chunks[i][-1][:len(froms[i + 1])].rstrip("-") if i + 1 < len(froms) else letter + "z"
        a, b = _readable(lo), _readable(hi)
        one = len(chunks[i]) == 1 and 0 < i < len(froms) - 1
        if one:                                              # one person a page (a President): his name
            lo = hi = chunks[i][0]
            a = b = (names or {}).get(lo) or _readable(lo)
        page = "names-" + re.sub(r"[^a-z]", "", lo) + ("-" + re.sub(r"[^a-z]", "", hi) if b != a else "")
        part = {"page": page, "from": f, "label": a if a == b else f"{a}–{b}"}
        if one:            # bounded to him: a later person of a key beside his goes to the page before or after
            part.update({"from": chunks[i][0], "only": chunks[i][0]})
        out.append(part)
    seen = set()
    for p in out:                      # two ranges of one label (a prefix the rule shortened): numbered
        while p["page"] in seen:
            p["page"] += "x"
        seen.add(p["page"])
    return out


def recut(part, sub):
    """A range over budget (part) in the pieces names_ranges made of its persons alone (sub): the first piece begins
    where the range began, its label's and its page's start the range's; the last ends where it ended."""
    sub = [dict(q) for q in sub]
    start, end = (part["label"].split("–", 1) + [part["label"]])[:2]
    slugs = part["page"][len("names-"):].split("-")
    sub[0]["from"] = part["from"]
    sub[0]["label"] = f"{start}–{sub[0]['label'].split('–', 1)[-1]}"
    sub[0]["page"] = "names-" + "-".join([slugs[0]] + sub[0]["page"][len("names-"):].split("-")[1:])
    sub[-1]["label"] = f"{sub[-1]['label'].split('–', 1)[0]}–{end}"
    sub[-1]["page"] = "names-" + "-".join(sub[-1]["page"][len("names-"):].split("-")[:1] + [slugs[-1]])
    return sub


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


SHORT = re.compile(r'<h2\b[^>]*\bdata-short="([^"]+)"')


def short(section):
    """A section's short label: its h2's data-short (the scroll wheel's), or None."""
    m = SHORT.match(section)
    return m.group(1) if m else None


H3 = re.compile(r'<h3\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h3>', re.S)
SHORT3 = re.compile(r'<h3\b[^>]*\bdata-short="([^"]+)"')
PGCONT = re.compile(r'<h2 class="pgcont" id="[^"]*" data-of="([^"]+)"')


def subcut(sid, label, section, starts):
    """[(piece id, label, html)]: an h2 section too large for a page alone, cut at the h3s named (starts), each piece
    after the first opened by the section's heading again, "continued", anchored pgc-<h3> (STYLE 2): the piece ids
    'h2/h3' ('t196101/t196101-departments')."""
    if not starts:
        return [(sid, label, section)]
    cuts = [(m.start(), m.group(1), TAGS.sub("", m.group(2)).strip()) for m in H3.finditer(section)
            if m.group(1) in starts]
    h = H2.match(section)
    sh = short(section) or label
    out = []
    bounds = [0] + [c for c, _, _ in cuts] + [len(section)]
    for i in range(len(bounds) - 1):
        piece = section[bounds[i]:bounds[i + 1]]
        if i == 0:
            out.append((sid, label, piece))
            continue
        _, h3, l3 = cuts[i - 1]
        head = (f'<h2 class="pgcont" id="pgc-{h3}" data-of="{sid}" data-short="{sh}, {l3}">'
                f'{h.group(2) if h else label}, continued</h2>')
        out.append((f"{sid}/{h3}", f"{label}: {l3}", head + piece))
    return out


def split_large(secs, target):
    """[(piece id, short label, bytes)]: the sections [(id, short label, html)] in order, one larger than the target
    cut at its h3s, packed in order (the first piece holding what comes before its first h3)."""
    out = []
    for sid, lab, h in secs:
        ms = list(H3.finditer(h)) if len(h) > target else []
        if not ms:
            out.append((sid, lab, len(h)))
            continue
        units = []
        for i, m in enumerate(ms):
            a = 0 if i == 0 else m.start()
            b = ms[i + 1].start() if i + 1 < len(ms) else len(h)
            sm = SHORT3.match(h[m.start():])
            units.append((m.group(1), sm.group(1) if sm else m.group(1), b - a))
        sizes = {u[0]: u[2] for u in units}
        shorts = {u[0]: u[1] for u in units}
        for j, run in enumerate(pack([(u[0], u[2]) for u in units], target)):
            pid = sid if j == 0 else f"{sid.split('/', 1)[0]}/{run[0]}"     # flat: h2/h3, a piece re-cut too
            out.append((pid, lab if j == 0 else f"{lab}, {shorts[run[0]]}", sum(sizes[x] for x in run)))
    return out


def pack(sizes, target, alone=()):
    """Consecutive items [(id, bytes)] packed in order: [[id, ...], ...], each run at most the target (an item
    larger alone; an item in `alone`, a piece of a section cut, with nothing else)."""
    out, cur, n = [], [], 0
    for k, s in sizes:
        if cur and (n + s > target or k in alone or cur[-1] in alone):
            out.append(cur)
            cur, n = [], 0
        cur.append(k)
        n += s
    if cur:
        out.append(cur)
    return out


def _slug(sid):
    if "/" in sid:                                      # a piece of a section: t196101/t196101-departments
        a, b = sid.split("/", 1)
        return f"{_slug(a)}-{b[len(a) + 1:] if b.startswith(a + '-') else _slug(b)}"
    m = re.match(r"^[a-z]+(\d{4})\d\d$", sid)          # t196101: 1961
    if m:
        return m.group(1)
    m = re.match(r"^[a-z](\d+)$", sid)                  # c87: 87
    return m.group(1) if m else re.sub(r"[^a-z0-9]+", "-", sid.lower()).strip("-")


def sections_parts(fam, secs, target):
    """[{page, label, sections}] for a page's h2 sections [(id, label, bytes)] packed to the target."""
    lab = {s: l for s, l, _ in secs}
    out = []
    cut = {x.split("/", 1)[0] for x, _, _ in secs if "/" in x}
    alone = {x for x, _, _ in secs if "/" in x or x in cut}
    for run in pack([(s, n) for s, _, n in secs], target, alone):
        a, b = _slug(run[0]), _slug(run[-1])
        page = f"{fam}-{a}" + (f"-{b}" if b != a else "")
        label = lab[run[0]] if len(run) == 1 else f"{lab[run[0]]}–{lab[run[-1]]}"
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
    placed = {s for p in plan for s in p["sections"]}
    secs = [x for s, l, h in secs for x in subcut(s, l, h, {q.split("/", 1)[1] for q in placed
                                                            if q.startswith(s + "/")})]
    by_id = {s: (l, h) for s, l, h in secs}
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
        full = by_id[p["sections"][0]][0] + (f" to {by_id[p['sections'][-1]][0]}" if len(p["sections"]) > 1 else "")
        html = _retitle(pre, f"{title}: {full}") + "\n" + main + "\n" + post
        out[f"{p['page']}.html"] = route_own(html, fam, p["page"])
    idx = [intro, bar(fam, parts, None)]
    for p in parts:
        idx.append(f'<h2 id="pt-{p["page"]}" data-short="{p["label"]}"><a href="{p["page"]}.html">{p["label"]}</a></h2>')
        idx.append('<ul class="pgl">' + "".join(f'<li><a href="{p["page"]}.html#{_anchor(s)}">{by_id[s][0]}</a></li>'
                                                 for s in p["sections"]) + "</ul>")
    html = pre + "\n" + "\n".join(idx) + "\n" + post
    html = html.replace("</body>", forward_script(amap, fam, here=True) + "\n</body>", 1)
    out[f"{fam}.html"] = route_own(html, fam, fam)
    return out


def _anchor(sid):
    """A section's anchor on its page: its h2's id; a piece of a section cut (h2/h3), its "continued" heading's."""
    return f"pgc-{sid.split('/', 1)[1]}" if "/" in sid else sid


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


def plan_key(fam):
    """The plan a family's map was cut by: a map kept in .cache serves only a build of the same plan."""
    import hashlib
    return hashlib.sha1(json.dumps(sections_plan(fam), sort_keys=True).encode("utf-8")).hexdigest()[:16]


def save_cache(fam):
    c = load_cache()
    c[fam] = {"plan": plan_key(fam), "map": MAPS.get(fam) or {}}
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    store.atomic_write(CACHE, json.dumps(c, sort_keys=True, separators=(",", ":")))


def ensure_map(fam, build):
    """MAPS[fam] for the router: cut this build (`build` makes the page), or the last build's, kept in .cache."""
    if fam in MAPS or not sections_plan(fam):
        return
    c = load_cache().get(fam)
    if isinstance(c, dict) and c.get("plan") == plan_key(fam) and c.get("map"):     # the same plan's map
        MAPS[fam] = c["map"]
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
    data = json.dumps({"f": [[str(p["from"]), p["page"]] + ([str(p["only"])] if p.get("only") else [])
                             for p in names_parts(letter)], "a": alias},
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
<noscript><p>Without scripts: <a href="{first}.html">the first of them</a>, or <a href="names.html">the Names
index</a>.</p></noscript>
<script>
/* an old link, forwarded by its anchor to the range that holds it (tools/bib/pages.py, STYLE 4) */
(function(){{
  var D={data};
  function go(){{
    var h=location.hash.slice(1); try{{ h=decodeURIComponent(h); }}catch(e){{}}
    if(!h){{ location.replace('{first}.html'); return; }}
    if(D.a[h]){{ location.replace(D.a[h]); return; }}
    var k=0; for(var i=0;i<D.f.length;i++) if(h>=D.f[i][0]) k=i;
    if(D.f[k][2]&&h!==D.f[k][2]&&k+1<D.f.length) k++;    /* a page of one person: his alone */
    location.replace(D.f[k][1]+'.html#'+h);
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
<noscript><p>Without scripts: <a href="{to}.html">the index</a>.</p></noscript>
{forward_script(amap, me)}
<script>if(!location.hash)location.replace('{to}.html');</script>
</body></html>
"""


# ---------------------------------------------------------------- the pass: measure (STYLE 1), plan (STYLE 2)

UNITS = {"cal": (re.compile(r'<li id="cal\.\d'), "entries"),
         "names": (re.compile(r'<section class="lv"'), "persons"),
         "works": (re.compile(r'<p class="wk" id='), "works"),
         "executive": (re.compile(r'<tr\b'), "rows"),
         "congress": (re.compile(r'<tr\b'), "rows"),
         "threads": (re.compile(r'<li (?:class="[^"]*" )?id="t-cal\.'), "entries"),
         "places": (re.compile(r'<li (?:class="[^"]*" )?id="t-cal\.'), "entries")}
THENTRY = re.compile(r'<li (?:class="[^"]*" )?id="t-cal\.(\d{4}(?:-\d\d){0,2})\.')
ANCHOR = re.compile(r'\sid="')
LV = re.compile(r'<section class="lv" id="([^"]+)">')
LVNAME = re.compile(r'<section class="lv" id="([^"]+)"><h2 [^>]*>(.*?)</h2>', re.S)
MONTH = re.compile(r"^(\d{4})(\d\d)b?$")


def built(out):
    """{page name: path} of the built pages."""
    import glob
    return {os.path.basename(p): p for p in sorted(glob.glob(os.path.join(out, "*.html")))}


def stubbed(text):
    """A page that only forwards (an old address)."""
    return "location.replace" in text and "<main id=\"doc\">" not in text


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
        units = len(rx.findall(text))
        over = n > b and not exempt(name)
        rows.append({"page": name, "bytes": n, "units": units, "unit": unit, "budget": b,
                     "over": over, "exempt": exempt(name), "stub": stubbed(text), "family": fam,
                     "alone": over and fam == "names" and units == 1})    # one person: no split divides him
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
        of = {f"{p['page']}.html": L for L, ps in (conf().get("names") or {}).items() for p in ps}   # a range's letter
        for r in rows:
            m = re.match(r"^names-([a-z])\.html$", r["page"])
            L = m.group(1) if m else of.get(r["page"])
            if L and not r["stub"]:
                letters.setdefault(L, []).append(r)
        props = {}

        def measured(rs):
            """[(key, bytes)] of the persons on the pages rs, their names, and a page's overhead (its template)."""
            sizes, total, body, nm = [], 0, 0, {}
            for x in rs:
                text = open(pages_[x["page"]], encoding="utf-8").read()
                nm.update({k: html.unescape(TAGS.sub("", v)) for k, v in LVNAME.findall(text)})
                got = _sizes_of(text, LV, ('<p class="lvs"><a class="lvp" href="names', "<script>(function(){var m=",
                                           "</main>"))
                sizes += got
                total += x["bytes"]
                body += sum(n for _, n in got)
            return sizes, nm, (total - body) // max(1, len(rs))

        for L, rs in sorted(letters.items()):
            if not any(x["over"] and not x.get("alone") for x in rs):    # one person over: no new ranges help
                continue
            target = int(budget(f"names-{L}.html") * fill())
            old = names_parts(L)
            if not old:                                                  # a letter's one page, in ranges
                sizes, nm, oh = measured(rs)
                rng = names_ranges(L, sizes, target - oh, nm)
                if rng:
                    props[L] = rng
                continue
            by = {x["page"]: x for x in rs}                              # a letter in ranges: a range within
            cut, changed = [], False                                     # budget kept as it is; one over, re-cut
            for part in old:
                x = by.get(f"{part['page']}.html")
                if not x or not x["over"] or x.get("alone"):
                    cut.append(dict(part))
                    continue
                sizes, nm, oh = measured([x])
                sub = names_ranges(L, sizes, target - oh, nm)
                if not sub:
                    cut.append(dict(part))
                    continue
                cut += recut(part, sub)
                changed = True
            if changed:
                seen = set()
                for q in cut:
                    while q["page"] in seen:
                        q["page"] += "x"
                    seen.add(q["page"])
                props[L] = cut
        if props:
            prop["names"] = props
    if "works" in over and not works_split():
        prop["works"] = {"by": "letter"}
    for fam in ("executive", "congress"):
        if fam not in over:
            continue
        plan_ = sections_plan(fam)
        over_ = {r["page"] for r in rows if r["over"]}
        groups = []                         # [(the parts kept as they are, or None; the pages whose sections to plan)]
        if plan_:                           # a family split before: a part within budget stays as it is (stable
            for p in plan_:                 # addresses); one over is planned again, alone
                groups.append(([p], None) if f"{p['page']}.html" not in over_ else (None, [f"{p['page']}.html"]))
        else:
            groups.append((None, [f"{fam}.html"]))
        parts = []
        for keep, names_ in groups:
            if keep:
                parts += keep
                continue
            secs, intro = [], 0
            for name in names_:
                if name not in pages_:
                    continue
                text = open(pages_[name], encoding="utf-8").read()
                pre, it, ss, post = anatomy(text)
                for s, l, h in ss:
                    m = PGCONT.match(h)
                    of = m.group(1) if m else s
                    at = next((k for k, x in enumerate(secs) if x[0] == of), None)
                    if at is not None:             # a section cut before: its pieces joined again
                        secs[at] = (of, secs[at][1], secs[at][2] + (h[h.index("</h2>") + 5:] if m else h))
                    else:
                        secs.append((f"{of}/{s[len('pgc-'):]}" if m else s, short(h) or l, h))   # a piece alone: h2/h3
                intro = max(intro, len(pre) + len(it) + len(post))
            target = int(budget(f"{fam}.html") * fill()) - intro
            parts += sections_parts(fam, split_large(secs, target), target)
        kept = {p["page"] for keep, _ in groups if keep for p in keep}
        seen = set(kept)
        for p in parts:                     # a new part's page never a kept part's name
            if any(p is k for keep, _ in groups if keep for k in keep):
                continue
            while p["page"] in seen:
                p["page"] += "x"
            seen.add(p["page"])
        prop[fam] = {"parts": parts}
    if "threads" in over:
        t = threads_proposal(out, rows)
        if t:
            prop["threads"] = t
    t = dict(planned("places"))                  # the places the build divided before a plan held them (placepages)
    if "places" in over:
        t.update(threads_proposal(out, rows, "places"))
    if t:
        prop["places"] = t
    if "cal" in over:
        c = calendar_proposal(out, rows)
        if c:
            prop["cal"] = c
    return prop


# ---------------------------------------------------------------- the Threads (threads.py, STYLE 6): a thread by date

def threads_parts(slug, fam="threads"):
    return ((conf().get(fam) or {}).get(slug)) or None


PLANNED = "places-planned"


def planned(fam):
    """{slug: parts}: the pages of a family the build divided by its own entries' sizes, with no plan in pages.yaml
    to hold them (placepages.py, STYLE 4), kept in .cache until `./bib pages --plan` writes them."""
    got = (load_cache().get(PLANNED) or {}) if fam == "places" else {}
    held = conf().get(fam) or {}
    return {k: v for k, v in got.items() if k not in held}


def save_planned(fam, slug, ps):
    c = load_cache()
    c.setdefault(PLANNED, {})[slug] = ps
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    store.atomic_write(CACHE, json.dumps(c, sort_keys=True, separators=(",", ":")))


def _thread_sizes(text):
    """[(date, bytes)] of the entries a Threads page holds, each from its li to the next's; and the page's rest."""
    import datetime
    got = _sizes_of(text, THENTRY, ('<nav class="pgseam"', "</main>"))
    out = []
    for d, n in got:
        y, m, dd = (d.split("-") + ["01", "01"])[:3]
        out.append((datetime.date(int(y), int(m), int(dd)), n))
    return out, len(text.encode("utf-8")) - sum(n for _, n in got)


def threads_proposal(out, rows, fam="threads"):
    """{slug: [{page, from, label}]}: each thread's page over budget in parts by date (threads.plan_parts); a thread in
    parts already, a part within budget kept as it is, one over planned again alone, from its own first day. fam:
    "places", a place's page the same way (placepages.py, STYLE 4)."""
    from . import threads
    pages_ = built(out)
    over = {r["page"] for r in rows if r["over"] and r["family"] == fam}
    of = {f"{p['page']}.html": slug for slug, ps in (conf().get(fam) or {}).items() for p in ps}
    target = int(budget(f"{fam}-x.html") * fill())
    props = {}
    for name in sorted(over):
        slug = of.get(name) or (name[len(fam) + 1:-len(".html")] if name.startswith(fam + "-") else None)
        if not slug or name not in pages_:
            continue
        sizes, rest = _thread_sizes(open(pages_[name], encoding="utf-8").read())
        if not sizes:
            continue
        old = props.get(slug) or threads_parts(slug, fam)
        if name not in of:                                   # a thread's one page, in parts
            new = threads.plan_parts(slug, sizes, target - rest, page=f"{fam}-{slug}")
            if len(new) > 1:
                props[slug] = new
            continue
        i = next(k for k, p in enumerate(old) if f"{p['page']}.html" == name)
        sub = threads.plan_parts(slug, sizes, target - rest, start=str(old[i]["from"]) if i else None,
                                 page=f"{fam}-{slug}")
        if len(sub) < 2:
            continue
        if i:
            sub[0]["from"] = old[i]["from"]
        cut = [dict(p) for p in old[:i]] + sub + [dict(p) for p in old[i + 1:]]
        seen = set()
        for q in cut:
            while q["page"] in seen:
                q["page"] += "x"
            seen.add(q["page"])
        props[slug] = cut
    return props


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
        rm = list(re.finditer(r"(?m)^  - \{page: [^\n]*\}\n", text[:text.index("\nsplit:") + 1]))
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
# sections in parts; threads, a thread's page in parts by date; places, a place's the same; retired, the pages a
# split replaced, each forwarding
# its old links. The calendar's parts are in
# lists/cal/list.yaml (`split:`, `retired_parts`).
"""


def write_conf(c, path=None):
    import yaml
    path = path or PATH
    keep = {k: c[k] for k in ("budget", "budgets", "fill", "why", "exempt", "works", "names", "executive", "congress",
                              "threads", "places", "retired") if c.get(k) not in (None, {}, [])}
    store.atomic_write(path, HEAD + yaml.safe_dump(keep, sort_keys=False, allow_unicode=True, width=110))
    _CONF.clear()


def live_pages(c=None):
    """Every page (without .html) the plan builds: the Names ranges, the Executive's and Congress's parts, the Works'
    letters, the families' indexes. A retired page is never one of them (a stub must not overwrite a live page)."""
    c = conf() if c is None else c
    out = {"names", "works", "executive", "congress"}
    out |= {p["page"] for ps in (c.get("names") or {}).values() for p in ps or []}
    for fam in ("executive", "congress"):
        out |= {p["page"] for p in ((c.get(fam) or {}).get("parts") or [])}
    if (c.get("works") or {}).get("by") == "letter":
        out |= {f"works-{L}" for L in "0abcdefghijklmnopqrstuvwxyz"}
    for fam in ("threads", "places"):                      # a thread or a place in parts: its own page the index,
        for slug, ps in (c.get(fam) or {}).items():        # and its parts
            out |= {f"{fam}-{slug}"} | {p["page"] for p in ps or []}
    return out


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
    for fam in ("threads", "places"):
        if prop.get(fam):
            th = dict(c.get(fam) or {})
            for slug, ps in prop[fam].items():
                old = [p["page"] for p in th.get(slug) or []]
                th[slug] = ps
                retired += [p for p in old if p not in {x["page"] for x in ps}]
            c[fam] = dict(sorted(th.items()))
    live = live_pages(c)
    c["retired"] = sorted(p for p in dict.fromkeys(retired) if p not in live)    # never a page the plan holds
    write_conf(c)
    cal = apply_calendar(prop["cal"]) if prop.get("cal") else []
    return prop, cal


def one_person_warnings(rows):
    """A Names page labelled for one person: bounded to him (`only`), and holding him alone (STYLE 2)."""
    units = {r["page"]: r["units"] for r in rows if r["family"] == "names"}
    out = []
    for L, ps in sorted((conf().get("names") or {}).items()):
        for p in ps or []:
            label = str(p.get("label") or "")
            if "–" in label:
                continue
            n = units.get(f"{p['page']}.html")
            if not p.get("only") and 0 < ps.index(p) < len(ps) - 1:
                out.append(f"warn: {p['page']} is labelled for one person ({label}) but not bounded to him "
                           f"(pages.yaml `only:`): a person filed beside him would land on it")
            if n is not None and n != 1:
                out.append(f"warn: {p['page']} is labelled for one person ({label}) and holds {n}")
    return out


def report(rows, prop=None):
    """The table `./bib pages` prints."""
    def mb(n):
        return f"{n / MB:.1f} MB" if n >= 100_000 else f"{n / 1000:.0f} KB"
    out = [f"{'page':<28} {'size':>9} {'units':>16}  budget"]
    for r in rows:
        if r["stub"]:
            continue
        mark = ("OVER, one person: no split divides him" if r.get("alone") else "OVER") if r["over"] else (
            "exempt" if r["exempt"] else "")
        out.append(f"{r['page']:<28} {mb(r['bytes']):>9} {r['units']:>8,} {r['unit']:<7}  {mb(r['budget']):>6} {mark}")
    stubs = [r["page"] for r in rows if r["stub"]]
    over = [r for r in rows if r["over"]]
    out.append(f"{len(rows) - len(stubs)} pages, {sum(r['bytes'] for r in rows if not r['stub']) / MB:.0f} MB; "
               f"{len(stubs)} forwarding stubs; {len(over)} over budget"
               + (f" ({sum(1 for r in over if r.get('alone'))} a single person's Names entry, which no split divides)"
                  if any(r.get("alone") for r in over) else ""))
    for r in rows:
        if r["exempt"] and not r["stub"]:
            out.append(f"exempt: {r['page']}: {r['exempt']}")
    out += one_person_warnings(rows)
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
        for fam in ("threads", "places"):
            for slug, ps in (prop.get(fam) or {}).items():
                out.append(f"  {fam}-{slug}: " + ", ".join(f"{p['page']} ({p['label']})" for p in ps))
        for pr in prop.get("cal") or []:
            out.append(f"  {pr['page']}: " + ", ".join(
                (_part_fields({}, k, mk)[0]["page"]) + f" (~{e / MB:.1f} MB)" for (k, mk), e in zip(pr["into"], pr["est"])))
    return "\n".join(out)
