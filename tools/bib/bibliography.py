"""The A–Z bibliography: every card in the works catalogue on one page, build/works.html.

STYLE:
 1. One list, A to Z, filed by the owner's rules (FILING in tools/bib/works.py): a work under its first-listed author's
    surname, a film under its director's, an organization only where the card names it as author; a work without one
    under its short title, the leading article dropped; then year, then short title.
 2. Every work under a heading in the heavier weight: an author's name, inverted ("Beschloss, Michael R."; a name in
    its own order as written), linked to the name entry where one person fits; a work filed under its title, its
    short title in italics, the article and subtitle dropped (FILING 9). A compilation under the writer it collects
    (FILING 6); one person written two ways under one heading (FILING 8). A work is entered again, a ghost, under its
    other authors, its editors and translators (FILING 7): its citation in the muted gray, the whole of it a link to
    the work's own entry, not underlined, and nothing more (no "Filed under"; the owner's ruling, Oct. 20, 2026). Under it, each work's full citation, the author named in running order ("Jean Lacouture, *Vietnam* ...").
    Nothing indented, first line or hanging: the headings' weight sets the works apart.
 3. No notes here (the card notes show in the lists). After each citation, on its line, muted and with no closing
    stop: the list sections that hold it, each linked to its listing ("K–J Adm. II.D, Viet. II.C.1"); the calendar
    entries whose notes point to it ([[w.…]]; or cite it by short title and list, not yet converted), by year
    (tools/bib/datelist.py, its last stop dropped); the chapters a volume holds, the volume a chapter is in, an
    edition's original; a semicolon between. The anchor is the card's id (works.html#w.beschloss-crisis-years).
 4. A work followed to (its anchor) is lit as a row of the rosters is: white (a lighter panel in the dark theme), an en
    dash past it on either side, plain again when the reader clicks outside it (templates/roster.css, tools/bib/roster.py).
 5. The typefaces (the owner's, Oct. 13, 2026, after Bluebook's large and small caps were tried and set aside): a
    book's author and title, a film's or an edited collection's title, in plain roman; an article's or a chapter's
    title in italics, its journal or collection in roman. works.render(..., caps=True) marks the roman parts (class
    "sc"). A title heading takes its citation's face. Here only; the themed lists keep their italics.
 6. The type of the series' entries (the template's 18px, line height 1.55), the pointers .8rem; a heading in the
    same size, heavier.
 7. A letter a heading (h2, for the scroll wheel and the Outline drawer). The A–Z bar under the lede, as on the Names
    pages (lives.py STYLE 7), the letters at 1rem, 0.36em apart. A title beginning with a number files under the
    number spelled out (FILING 5 in tools/bib/works.py).
 8. Split by letter where pages.yaml says (tools/bib/pages.py; the owner, Nov. 19, 2026): works.html the index (the
    lede, the bar, each letter with its count and its first and last headings, linked to its page), works-a.html ...
    works-0.html a page a letter, each with the bar (its own letter unlinked), a line to the index, and at the foot
    the letters before and after. A card's anchor is on its letter's page; a link anywhere goes there
    (pages.works_href, pages.route), and works.html#<card> forwards an old link by script.
 9. The top bar names the heading the reader is under, an author's name or a title in full, as it names the person on
    a Names page, not the letter alone (the owner, Nov. 25, 2026: "show the full name of the author or work, as the
    Names navigation bar does, rather than just the first letter"): each heading carries an id ("wh." and its folded
    words), `data-h` (the template's mark for a heading that is not an h2-h4: level 2 on a letter's own page, as a
    person's is, 3 where all the letters share one page) and `data-short`, its words. The scroll wheel and the
    Outline drawer read the same marks. No new rule in the CSS and none in the script.
"""
import html
import re

from . import chron, datelist, pages, store, works
from .markup import ITAL_RE, REF_RE, plain, to_html

esc = html.escape

CSS = """<style>
/* the A–Z bibliography (tools/bib/bibliography.py) */
:root{--tgt:#FFFFFF}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--tgt:#22262E}}
:root[data-theme="dark"]{--tgt:#22262E}
body{--dash:.515em}
div.azw{margin:.4rem 0 .8rem}
p.az{display:flex;flex-wrap:wrap;gap:0 .36em;margin:0;font-family:var(--sans);font-weight:600;font-size:1rem;line-height:1.4}
p.az a{color:var(--muted);text-decoration:none}
p.az a:hover{color:var(--ink);text-decoration:underline;text-decoration-thickness:1px}
.wz h2{margin-top:2rem}
.wz p{margin:0;padding:0;text-indent:0}
.wz .wh{margin:.9rem 0 .15rem;font-weight:600}
.wz .wh a.nm{font-weight:600}
.wz .wk{margin:.15rem 0 .3rem;scroll-margin-top:3.5rem}
.wz .sc{font-style:normal}
.wz .wk:target:not(.unhl){background:var(--tgt);box-shadow:calc(-1*var(--dash)) 0 0 var(--tgt),var(--dash) 0 0 var(--tgt)}
.wz .wp{font-size:.8rem;color:var(--muted)}
.wz .wp a{color:var(--muted)}
.wz .wg,.wz a.wgl{color:var(--muted);text-decoration:none}
</style>
<script>
document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('a[href*="#"]');
  document.querySelectorAll('.wz .wk:target').forEach(function(r){
    if(r.contains(e.target))return;
    if(a&&a.hash==='#'+r.id){r.classList.remove('unhl');return;}
    r.classList.add('unhl');
  });
});
window.addEventListener('hashchange',function(){
  document.querySelectorAll('.wz .wk.unhl').forEach(function(r){r.classList.remove('unhl');});
});
</script>"""

LEDE = ['<p class="lede">Every work the series cites, one entry a work, A to Z: by the first-listed author\'s surname '
        '(a film by its director\'s), then year, then title; a work without an author (an edited volume, a series) by '
        'its title, the leading article dropped; a number as it is said. After each, where the series cites it: the '
        'lists that hold it and the calendar entries whose notes name it.</p>']


def caps(h):
    """Bluebook's large and small caps (works.SC ... SC_END) as the page's element."""
    return h.replace(works.SC, '<span class="sc">').replace(works.SC_END, "</span>")


def nostop(t):
    """A run of dates without its closing stop (STYLE 3)."""
    return t[:-1] if t.endswith(".") else t


def letter_of(key):
    ch = (key or "")[:1]
    return ch if ch.isalpha() else "0"


def calendar_cites(series, linker):
    """card id -> [calendar entry]: the calendar's notes that point to the card ([[w.…]]), or cite it by its short title
    and a list and section ("Kaplan, *Wizards of Armageddon* (K–J Adm. II.D)"), each title of a run before one
    reference taken to it."""
    cat, refs = series.works, linker.refs
    out = {}
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for _, e in lst.entries():
            n = e.get("n") or ""
            for m in REF_RE.finditer(n):          # the pointers: [[w.…]]
                cid = cat.alias.get(m.group(1).strip(), m.group(1).strip())
                if cid in cat.cards and e not in out.setdefault(cid, []):
                    out[cid].append(e)
            for m in ITAL_RE.finditer(n):         # a short title and a list, not yet a pointer
                tail = n[m.end():m.end() + 300]
                hit = next(((a, key, code) for a, b, key, code in refs.scan(tail, lst.key) if code), None)
                if not hit or re.search(r"[a-z)]\.\s+[A-Z]", tail[:hit[0]]):
                    continue                 # no reference, or one past the end of the sentence
                x = linker.find_title(m.group(1), hit[1], hit[2])
                if not x or not x.get("work"):
                    continue
                ids = store.as_list(x["work"])
                k = re.sub(r"^(the|a|an) ", "", store.fold(m.group(1)))
                pick = [i for i in ids if k and k in store.fold(plain((cat.fields(i) or {}).get("title") or ""))]
                for cid in (pick or ids)[:1]:
                    cid = cat.alias.get(cid, cid)
                    if e not in out.setdefault(cid, []):
                        out[cid].append(e)
    return out


def groups(series):
    """The A–Z page's blocks, in order: [{key, hd, title, raw, items: [(sort key, ghost, card id)]}] (STYLE 1-2): an
    author's works under the heading; a work without one by itself, its short title the heading."""
    cat = series.works
    groups = {}

    def into(hd, key, cid, ghost=False, raw=None):
        if not hd:
            title = (cat.fields(cid) or {}).get("title") or works.short_title(plain(cat.render(cid)))
            t = works.ARTICLE.sub("", works.short_title(plain(title))).strip()
            t = t[:1].upper() + t[1:]
            g = groups.setdefault(("t", store.fold(t)), {"key": key[0], "hd": None, "title": t, "items": []})
        else:
            g = groups.setdefault(("h", store.fold(hd)), {"key": key[0], "hd": hd, "items": [], "raw": raw})
            if not ghost and g.get("ghosted", True):
                g["raw"], g["ghosted"] = raw, False          # the name as a work filed here writes it
            if marks(hd) > marks(g["hd"]):           # one name written with and without its marks: the marks
                g["hd"] = hd
        g["items"].append((key[1:], ghost, cid))

    def marks(h):
        return sum(1 for ch in h or "" if ord(ch) > 127)

    for cid in cat.cards:
        hd, key = works.filing(series, cid)
        into(hd, key, cid, raw=works.filed_name(cid, cat))
        f = cat.fields(cid) or {}
        for n in works.ghost_names(cid, cat):    # the same work, entered again under its other names (FILING 7)
            gh, gk = works.heading(n)
            into(gh, (gk, str(f.get("year") or ""), key[-1]), cid, True, n)
    return sorted(groups.values(), key=lambda g: (g["key"], g["hd"] or "", g["items"][0][0]))


def letters(series):
    """{card id or alias: its letter}: the letter of the heading each card is filed under (not its ghosts'), for the
    pages a letter (tools/bib/pages.py)."""
    out = {}
    for g in groups(series):
        L = letter_of(g["key"])
        for _, gh, cid in g["items"]:
            if not gh:
                out[cid] = L
                for a in store.as_list(series.works.get(cid).get("aliases")):
                    out.setdefault(a, L)
    return out


def pages_(series, linker, template):
    """{file name: html}: works.html, the whole bibliography; or, split by letter (pages.yaml), works.html the
    index and works-a.html ... a page a letter (STYLE 8)."""
    from . import namelinks
    cat = series.works
    where = works.where(series)
    cal = calendar_cites(series, linker)
    holds = {}
    for cid, c in cat.cards.items():
        if c.get("in"):
            holds.setdefault(c["in"], []).append(cid)

    def resolve(eid, shown):
        hit = series.get(eid)
        if not hit:
            return None
        return f'<a href="{hit[0].key}.html#{esc(hit[2]["id"])}">{esc(shown or eid)}</a>'

    def short(cid):
        f = cat.fields(cid) or {}
        who = works.filed_name(cid, cat)
        t = works.short_title(plain(f.get("title") or "")) or plain(cat.render(cid))[:60]
        t = re.sub(r"^(?:The|A|An) ", "", t)
        book = cat.render(cid, caps=True).startswith(works.SC)        # a book's title roman, a paper's italic
        return (works.surname(who) + ", " if who else "") + (esc(t) if book else f"<i>{esc(t)}</i>")

    translated_in = {}
    for y, cy in cat.cards.items():
        if cy.get("translates"):
            translated_in.setdefault(cy["translates"], []).append(y)

    def pointers(cid):
        out = []
        seen = []
        for lst, sec, e in where.get(cid, []):
            lab = f"{lst.abbr} {sec.code}"
            if lab not in [x for x, _ in seen]:
                seen.append((lab, f'<a href="{lst.key}.html#{esc(e["id"])}">{esc(lab)}</a>'))
        if seen:
            out.append(", ".join(h for _, h in seen))
        es = chron.sort(series, cal.get(cid, []))      # in the calendar's order (chron.py)
        if es:
            out.append("Cal. " + nostop(datelist.run((e.get("date"), f'<a href="cal.html#{esc(e["id"])}">{esc(e.get("when") or "")}</a>')
                                              for e in es)))
        c = cat.get(cid)
        if c.get("in") and cat.get(c["in"]):
            out.append(f'In: <a href="#{esc(c["in"])}">{short(c["in"])}</a>')
        if holds.get(cid):
            out.append("Holds: " + "; ".join(f'<a href="#{esc(x)}">{short(x)}</a>' for x in sorted(holds[cid])))
        if c.get("edition_of") and cat.get(c["edition_of"]):
            out.append(f'Edition of: <a href="#{esc(c["edition_of"])}">{short(c["edition_of"])}</a>')
        if c.get("translates") and cat.get(c["translates"]):    # derivative cards (the owner, Nov. 12, 2026): "Y.
            out.append(f'Translation of <a href="#{esc(c["translates"])}">{short(c["translates"])}</a>')   # Translation
        if translated_in.get(cid):                              # of [X]." and on X, "Translated in [Y]."
            out.append("Translated in " + "; ".join(f'<a href="#{esc(y)}">{short(y)}</a>' for y in sorted(translated_in[cid])))
        return "; ".join(out)

    def item(cid, ghost=False):
        if ghost:                        # entered again under another name: the citation in gray, linked to the entry
            inner = re.sub(r"</?a\b[^>]*>", "", caps(to_html(cat.render(cid, caps=True), resolve)))
            return f'<p class="wk wg"><a class="wgl" href="#{esc(cid)}">{inner}</a></p>'
        h = f'<p class="wk" id="{esc(cid)}">' + "".join(f'<span id="{esc(a)}"></span>' for a in store.as_list(cat.get(cid).get("aliases"))) \
            + caps(to_html(cat.render(cid, caps=True), resolve))
        p = pointers(cid)
        if p:
            h += f' <span class="wp">{p}</span>'
        return h + "</p>"

    blocks = groups(series)

    seen = {}
    lv = 2 if pages.works_split() else 3     # on a letter's own page the heading stands where the Names' does

    def bar_mark(text, cid):
        """STYLE 9: the heading's id and what the top bar, the scroll wheel and the Outline read."""
        base = re.sub(r"[^a-z0-9]+", "-", store.fold(text)).strip("-") or cid
        seen[base] = seen.get(base, 0) + 1
        hid = "wh." + base + (f"-{seen[base]}" if seen[base] > 1 else "")
        return f' id="{esc(hid)}" data-h="{lv}" data-short="{esc(text)}"'

    def head(hd, raw, cid):
        name = works.SAME.get(raw or hd, raw or hd)
        who = namelinks.written(series, re.sub(r"\s+et al\.\??$", "", name)) or namelinks.person(series, hd)
        u = namelinks.url(series, who) if who else None
        inner = esc(hd)
        return f'<p class="wh"{bar_mark(hd, cid)}>' + (f'<a class="nm" href="{esc(u)}">{inner}</a>' if u else inner) + "</p>"

    by_letter = {}
    for g in blocks:
        by_letter.setdefault(letter_of(g["key"]), []).append(g)
    letters = sorted(by_letter, key=lambda L: (L != "0", L))
    lab = {L: ("0–9" if L == "0" else L.upper()) for L in letters}
    n_auth = sum(1 for g in blocks if g["hd"] and any(not gh for _, gh, _ in g["items"]))
    count = f'<p class="logic">{len(cat.cards):,} works; {n_auth:,} authors and directors.</p>'

    def body(L):
        out = []
        for g in by_letter[L]:
            items = sorted(g["items"])
            if g["hd"]:
                hh = head(g["hd"], g.get("raw"), items[0][2])
            else:                          # the short title, in italics (the owner's ruling, Oct. 15, 2026)
                hh = f'<p class="wh"{bar_mark(g["title"], items[0][2])}><i>{esc(g["title"])}</i></p>'
            out.append('<div class="wa">' + hh + "".join(item(cid, gh) for _, gh, cid in items) + "</div>")
        return out

    def wrap(title, main):
        pg = open(template, encoding="utf-8").read()
        pg = pg.replace("{{page_title}}", title).replace("{{main}}", "\n".join(main))
        return pg.replace("</body>", CSS + "\n</body>", 1)
    if not pages.works_split():
        bar = '<div class="azw"><p class="az">' + "".join(f'<a href="#az-{L}">{lab[L]}</a>' for L in letters) + "</p></div>"
        main = ["<h1>Works</h1>"] + LEDE + [count, bar, '<div class="wz">']
        for L in letters:
            main.append(f'<h2 id="az-{L}" data-short="{lab[L]}">{lab[L]}</h2>')
            main += body(L)
        main.append("</div>")
        return {"works.html": wrap("Works", main)}
    # a page a letter (STYLE 8; tools/bib/pages.py; the owner, Nov. 19, 2026: "Do we need to split Works? ... I think
    # we do."): works.html the index, its bar to the letters' pages; each letter's page the bar, its own unlinked
    def bar(cur=None):
        return '<div class="azw"><p class="az">' + "".join(
            f'<span aria-current="page">{lab[L]}</span>' if L == cur else
            f'<a href="{pages.works_page_of_letter(L)}.html">{lab[L]}</a>' for L in letters) + "</p></div>"

    def counted(L):
        n = sum(1 for g in by_letter[L] for _, gh, _ in g["items"] if not gh)
        return f"{n:,} {'work' if n == 1 else 'works'}"
    out = {}
    index = ["<h1>Works</h1>"] + LEDE + [count, bar(), '<p class="logic">A page a letter.</p>']
    for L in letters:
        pg = pages.works_page_of_letter(L)
        first, last = by_letter[L][0], by_letter[L][-1]
        rng = " to ".join(dict.fromkeys(esc(g["hd"] or g["title"]) for g in (first, last)))
        index.append(f'<h2 id="az-{L}" data-short="{lab[L]}"><a href="{pg}.html">{lab[L]}</a></h2>'
                     f'<p class="logic"><a href="{pg}.html">{counted(L)}</a>: {rng}.</p>')
    html = wrap("Works", index)
    out["works.html"] = html.replace("</body>", pages.forward_script(dict(pages.WORKS), "works", here=True)
                                     + "\n</body>", 1)
    for i, L in enumerate(letters):
        me = pages.works_page_of_letter(L)
        seam = ([f'<a href="{pages.works_page_of_letter(letters[i - 1])}.html">‹ {lab[letters[i - 1]]}</a>'] if i else []) \
            + ['<a href="works.html">Index</a>'] \
            + ([f'<a href="{pages.works_page_of_letter(letters[i + 1])}.html">{lab[letters[i + 1]]} ›</a>']
               if i + 1 < len(letters) else [])
        main = [f"<h1>Works: {lab[L]}</h1>"] + LEDE + [
            f'<p class="logic">{counted(L)} under {lab[L]}; {len(cat.cards):,} in all.</p>', bar(L),
            '<p class="lvs"><a href="works.html">Index</a></p>', '<div class="wz">',
            f'<h2 id="az-{L}" data-short="{lab[L]}">{lab[L]}</h2>'] + body(L) + [
            "</div>", '<nav class="pgseam" aria-label="Letters"><p>' + " · ".join(seam) + "</p></nav>" + pages.PART_CSS]
        out[f"{me}.html"] = OWN.sub(lambda m: f'href="{pages.works_href(m.group(1))}"'
                                    if pages.WORKS.get(m.group(1), me) != me else m.group(0),
                                    wrap(f"Works: {lab[L]}", main))
    return out


OWN = re.compile(r'href="#([^"]+)"')


def page(series, linker, template):
    """The A–Z bibliography on one page (the build writes pages_(), a page a letter where pages.yaml says)."""
    return pages_(series, linker, template)["works.html"]
