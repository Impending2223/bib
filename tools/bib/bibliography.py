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
"""
import html
import re

from . import datelist, store, works
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


def page(series, linker, template):
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

    def pointers(cid):
        out = []
        seen = []
        for lst, sec, e in where.get(cid, []):
            lab = f"{lst.abbr} {sec.code}"
            if lab not in [x for x, _ in seen]:
                seen.append((lab, f'<a href="{lst.key}.html#{esc(e["id"])}">{esc(lab)}</a>'))
        if seen:
            out.append(", ".join(h for _, h in seen))
        es = sorted(cal.get(cid, []), key=lambda e: str(e.get("date") or ""))
        if es:
            out.append("Cal. " + nostop(datelist.run((e.get("date"), f'<a href="cal.html#{esc(e["id"])}">{esc(e.get("when") or "")}</a>')
                                              for e in es)))
        c = cat.get(cid)
        if c.get("in") and cat.get(c["in"]):
            out.append(f'In: <a href="#{esc(c["in"])}">{short(c["in"])}</a>')
        if holds.get(cid):
            out.append("Holds: " + "; ".join(f'<a href="#{esc(x)}">{short(x)}</a>' for x in sorted(holds[cid])))
        for fld, lab in (("edition_of", "Edition of"), ("translates", "Translation of")):
            if c.get(fld) and cat.get(c[fld]):
                out.append(f'{lab}: <a href="#{esc(c[fld])}">{short(c[fld])}</a>')
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

    # file every card: an author's works under the heading; a work without, by itself (its short title the heading)
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
    blocks = sorted(groups.values(), key=lambda g: (g["key"], g["hd"] or "", g["items"][0][0]))

    def head(hd, raw):
        name = works.SAME.get(raw or hd, raw or hd)
        who = namelinks.written(series, re.sub(r"\s+et al\.\??$", "", name)) or namelinks.person(series, hd)
        u = namelinks.url(series, who) if who else None
        inner = esc(hd)
        return f'<p class="wh">' + (f'<a class="nm" href="{esc(u)}">{inner}</a>' if u else inner) + "</p>"

    by_letter = {}
    for g in blocks:
        by_letter.setdefault(letter_of(g["key"]), []).append(g)
    letters = sorted(by_letter, key=lambda L: (L != "0", L))
    lab = {L: ("0–9" if L == "0" else L.upper()) for L in letters}
    bar = '<div class="azw"><p class="az">' + "".join(f'<a href="#az-{L}">{lab[L]}</a>' for L in letters) + "</p></div>"
    n_auth = sum(1 for g in blocks if g["hd"] and any(not gh for _, gh, _ in g["items"]))
    main = ["<h1>Works</h1>"] + LEDE + [
        f'<p class="logic">{len(cat.cards):,} works; {n_auth:,} authors and directors.</p>', bar, '<div class="wz">']
    for L in letters:
        main.append(f'<h2 id="az-{L}" data-short="{lab[L]}">{lab[L]}</h2>')
        for g in by_letter[L]:
            items = sorted(g["items"])
            if g["hd"]:
                hh = head(g["hd"], g.get("raw"))
            else:                          # the short title, in italics (the owner's ruling, Oct. 15, 2026)
                hh = f'<p class="wh"><i>{esc(g["title"])}</i></p>'
            main.append('<div class="wa">' + hh + "".join(item(cid, gh) for _, gh, cid in items) + "</div>")
    main.append("</div>")
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", "Works").replace("{{main}}", "\n".join(main))
    return pg.replace("</body>", CSS + "\n</body>", 1)
