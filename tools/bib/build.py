"""Render the store to HTML.

    build/<key>.html   one page per list, published to that list's artifact
    build/series.html  the compiled reader: every list, live cross-references,
                       "Elsewhere" lines, and the names index

Nothing in build/ is edited by hand; it is regenerated from lists/.
"""
import html
import json
import os
import re

from . import daybook, primaries, specials, store
from .markup import to_html, plain, italics, ITAL_RE, REF_RE
from .refs import Refs, split_protected

TEMPLATES = os.path.join(store.ROOT, "templates")
OUT = os.path.join(store.ROOT, "build")


NUMBERS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
           11: "eleven", 12: "twelve"}


def esc(t):
    return html.escape(t, quote=False)


def attr(t):
    return html.escape(t, quote=True)


# ---------------------------------------------------------------- calendar helpers

def thread_name(lst, slug):
    t = lst.threads().get(slug)
    return plain(t["s"]) if t else slug


def entry_subject(lst, e):
    """The bold line. Calendar entries build it from when + thread."""
    if lst.kind == "calendar" and "when" in e:
        return f"{e['when']} ({thread_name(lst, e['thread'])})"
    return e.get("s")


def thread_members(lst):
    """thread slug -> entries in document order (primary thread or 'also')."""
    out = {}
    for sec, e in lst.entries():
        if "when" not in e:
            continue
        for t in [e["thread"]] + e.get("also", []):
            out.setdefault(t, []).append(e)
    return out


_NAV = {}


def thread_nav(series, lst, e, year, text_html):
    """Under a calendar entry, for each of its threads, the entries before and after it in the thread:
    "‹ Apr. 24 · Testing · June 10 ›" (the year added where it differs). A thread's first entry has no ‹, its
    last no ›."""
    key = id(lst)
    if key not in _NAV:
        _NAV[key] = {t: [m["id"] for m in ms] for t, ms in thread_members(lst).items()}
    out = []
    for t in [e["thread"]] + e.get("also", []):
        ids = _NAV[key].get(t, [])
        if e["id"] not in ids or len(ids) < 2:
            continue
        i = ids.index(e["id"])
        prev = f"‹ [[{ids[i - 1]}]] · " if i > 0 else ""
        nxt = f" · [[{ids[i + 1]}]] ›" if i + 1 < len(ids) else ""
        line = year_qualified(series, f"{prev}{thread_name(lst, t)}{nxt}", year)
        out.append(f'<span class="tnl">{text_html(line, "tn")}</span>')
    return f'<span class="tn">{"".join(out)}</span>' if out else ""


def program_links(lst):
    """The calendar's To/From links: an entry that sets several threads going (a State of the Union, an address to
    Congress) names them in `to:` (a thread slug, which resolves to the thread's next entry after it, or
    {slug: entry id}; an entry of the thread's own before one it holds through `also`); `short:` names it for the other end. -> ({initiator id: [(slug, target id)]},
    {target id: [initiator id]}). Unresolved items are left out (check reports them)."""
    key = ("to", id(lst))
    if key in _NAV:
        return _NAV[key]
    members = thread_members(lst)
    fwd, back = {}, {}
    for sec, e in lst.entries():
        for item in e.get("to") or []:
            slug, tid = (next(iter(item.items())) if isinstance(item, dict) else (item, None))
            if tid is None:          # the thread's next entry of its own, before one it holds through `also` (a poll)
                later = [m for m in members.get(slug, []) if str(m.get("date", "")) > str(e.get("date", ""))
                         and m["id"] != e["id"]]
                tid = next((m["id"] for m in later if m["thread"] == slug), next((m["id"] for m in later), None))
            if tid:
                fwd.setdefault(e["id"], []).append((slug, tid))
                back.setdefault(tid, []).append(e["id"])
    _NAV[key] = (fwd, back)
    return _NAV[key]


def program_html(series, lst, e, year, text_html):
    """'To: Taxes, Jan. 24 · Health, Feb. 5' under an initiating entry; 'From: State of the Union, Jan. 14' under each
    entry it reaches."""
    fwd, back = program_links(lst)
    out = []
    if e["id"] in fwd:
        items = sorted(fwd[e["id"]], key=lambda x: str((series.get(x[1]) or (0, 0, {}))[2].get("date", "")))
        out.append(("To:", " · ".join(f"{thread_name(lst, slug)}, [[{tid}]]" for slug, tid in items)))
    if e["id"] in back:
        names = []
        for iid in back[e["id"]]:
            ie = series.get(iid)[2]
            names.append(f"[[{iid}|{ie.get('short') or thread_name(lst, ie['thread'])}, {date_label(ie, year)}]]")
        out.append(("From:", "; ".join(names)))
    # the label in the line's italic, what follows it upright (.tn.tp .tpv)
    return "".join(f'<span class="tnl">{lab} <span class="tpv">{text_html(year_qualified(series, t, year), "tn")}</span></span>'
                   for lab, t in out)


def date_label(e, year=None):
    """A calendar entry's label: its "when", with the year added when it is not `year`."""
    y = (e.get("date") or "")[:4]
    return f"{e['when']}, {y}" if y and y != year else e["when"]


def year_qualified(series, text, year):
    """Give bare [[id]] links to calendar entries of another year their year,
    so "See Dec. 21–22" written in 1962 reads "See Dec. 21–22, 1961"."""
    def sub(m):
        if m.group(2):
            return m.group(0)
        hit = series.get(m.group(1).strip())
        if not hit or hit[0].kind != "calendar" or "when" not in hit[2]:
            return m.group(0)
        e = hit[2]
        label = date_label(e, year)
        return m.group(0) if label == e["when"] else f"[[{m.group(1)}|{label}]]"
    return REF_RE.sub(sub, text) if text and year else text


def label_of(series, eid):
    hit = series.get(eid)
    if not hit:
        return None
    lst, sec, e = hit
    return e.get("when") or plain(entry_subject(lst, e) or store.as_list(e.get("c"))[0])


# ---------------------------------------------------------------- entry markup

def entry_html(series, lst, sec, e, text_html, extra_attrs="", extra_spans="", rubric=None):
    """rubric: for a calendar entry laid out by day, the thread line that opens its first sentence."""
    parts = []
    year = (e.get("date") or "")[:4] if lst.kind == "calendar" else None
    subj = None if rubric is not None else entry_subject(lst, e)
    if subj:
        parts.append(f'<span class="s">{text_html(subj, "s")}</span>')
    for i, c in enumerate(store.as_list(e.get("c"))):
        lead = rubric if (rubric and i == 0) else ""
        parts.append(f'<span class="c">{lead}{text_html(year_qualified(series, c, year), "c")}</span>')
    if e.get("r"):
        parts.append(f'<span class="r">{text_html(e["r"], "r")}</span>')
    n = year_qualified(series, e.get("n"), year)
    if lst.kind == "calendar" and e["id"].startswith(f"{lst.key}.thread."):
        slug = e["id"].split(".", 2)[2]
        members = thread_members(lst).get(slug, [])
        # the year on the first date of each year
        shown, prev = [], None
        for m in members:
            y = m["date"][:4]
            shown.append(f"[[{m['id']}|{date_label(m, prev)}]]" if y != prev else f"[[{m['id']}]]")
            prev = y
        n = "; ".join(shown)
        if members and not members[-1]["when"].endswith("."):
            n += "."
    if n:
        parts.append(f'<span class="n">{text_html(n, "n")}</span>')
    if rubric is not None and lst.kind == "calendar" and e.get("thread"):
        prog = program_html(series, lst, e, year, text_html)
        if prog:
            parts.append(f'<span class="tn tp">{prog}</span>')
        nav = thread_nav(series, lst, e, year, text_html)
        if nav:
            parts.append(nav)
    if e.get("conflict"):
        parts.append('<span class="n"><b>Unresolved merge conflict.</b></span>')
    return f'<li id="{attr(e["id"])}"{extra_attrs}>' + "".join(parts) + extra_spans + "</li>"


def headings(lst, sec, idfmt):
    tag = f"h{min(sec.level, 4)}"
    num = f'<span class="num">{esc(sec.num)}</span>' if sec.num else ""
    return f'<{tag} id="{idfmt(sec)}" data-short="{attr(sec.label)}">{num}{to_html(sec.title)}</{tag}>'


def by_day(lst, sec):
    """A dated calendar section is laid out by day (tools/bib/daybook.py)."""
    return lst.kind == "calendar" and sec.extra.get("from") and sec.extra.get("to")


def section_body(series, lst, sec, idfmt, text_html, li_extra=None):
    out = [headings(lst, sec, idfmt)]
    for p in sec.logic:
        out.append(f'<p class="logic">{text_html(p, "logic")}</p>')
    if by_day(lst, sec):
        def li(e, rub):
            a, s = li_extra(sec, e) if li_extra else ("", "")
            return entry_html(series, lst, sec, e, text_html, a, s, rub)
        out.extend(daybook.section_days(lst, sec, li, thread_name))
    elif sec.entries:
        out.append('<ol class="e">')
        for e in sec.entries:
            a, s = li_extra(sec, e) if li_extra else ("", "")
            out.append(entry_html(series, lst, sec, e, text_html, a, s))
        out.append("</ol>")
    for c in sec.children:
        out.extend(section_body(series, lst, c, idfmt, text_html, li_extra))
    return out


# ---------------------------------------------------------------- one list, standalone

def build_list(series, key, linker=None):
    lst = series.lists[key]
    from . import namelinks

    def resolve(eid, shown):
        if eid.startswith("§nmx:"):      # a person's name entry (tools/bib/namelinks.py)
            return f'<a class="nm" href="{attr(eid[5:])}">{to_html(shown)}</a>'
        hit = series.get(eid)
        if not hit:
            return None
        tl, ts, te = hit
        text = esc(shown or label_of(series, eid))
        if tl.key == key:
            return f'<a href="#{attr(te["id"])}">{text}</a>'
        return text

    def text_html(t, field):
        # the persons a line names, linked to their name entries: a subject line's, a citation's authors, a note's
        # 'Names:' (tools/bib/namelinks.py)
        if field == "s":
            return "; ".join(namelinks.a(series, plain(part), part) for part in to_html(t, resolve).split("; "))
        if field == "c":
            lead, rest = namelinks.author_split(series, t)
            return (lead or "") + to_html(rest, resolve)
        if field == "n" and linker and "Names:" in t:
            t = linker.names_markup(t, key, internal=False)
        return to_html(t, resolve)

    main = [f"<h1>{esc(lst.data['h1'])}</h1>"]
    if lst.data.get("lede"):
        main.append(f'<p class="lede">{text_html(lst.data["lede"], "lede")}</p>')
    for p in store.as_list(lst.data.get("logic")):
        main.append(f'<p class="logic">{text_html(p, "logic")}</p>')
    main.append('<p class="logic">To navigate, use the Outline button, the contents below, or the handle on the right edge, which you can drag to see nearby headings. '
                'All the lists in one reader: <a href="series.html">the series</a>. Each Congress at its opening: <a href="congress.html">Congress</a>. '
                'The Executive Branch at each inauguration: <a href="executive.html">Executive</a>.</p>')
    main.append('<nav class="toc" aria-label="Contents">\n<h3 id="contents" style="border-top:0;margin-top:1.5rem" data-short="Contents">Contents</h3>\n<ol id="tocList"></ol>\n</nav>')
    for s in lst.sections:
        main.extend(section_body(series, lst, s, lambda sec: attr(sec.id), text_html))
    page = open(os.path.join(TEMPLATES, "list.html"), encoding="utf-8").read()
    page = page.replace("{{page_title}}", esc(lst.data["page_title"])).replace("{{main}}", "\n".join(main))
    return page.replace("<head>", "<head>\n" + source_note(series, f"lists/{key}/"), 1)


def source_note(series, path):
    repo = series.data.get("source_repo", "")
    return (f"<!-- Generated from {repo} ({path}) by ./bib build. Do not edit this file: edit the data and rebuild. "
            "Each entry's id attribute is its id in the data; CLAUDE.md in the repository explains how to "
            "find, change, and merge entries. -->")


# ---------------------------------------------------------------- the compiled reader

class Linker:
    """Turns the prose conventions into links for the compiled reader."""

    def __init__(self, series):
        self.series = series
        self.refs = Refs(series)
        self.works = {}   # work key -> [(list, section, entry)]
        self.people = {}  # name key -> [(list, section, entry)]
        for lst in series.lists.values():
            for sec, e in lst.entries():
                for k in self.refs.work_keys(e):
                    self.works.setdefault(k, []).append((lst, sec, e))
                if self.refs.is_person(lst, sec, e):
                    for k, _ in self.refs.name_keys(e["s"]):
                        self.people.setdefault(k, []).append((lst, sec, e))
        self.links = 0
        self.n_elsewhere = 0

    def sec_id(self, sec):
        return f"{sec.lst.key}--{sec.id}"

    def a(self, href, cls, inner):
        self.links += 1
        return f'<a class="x {cls}" href="#{attr(href)}">{inner}</a>'

    def same_thing(self, e, key):
        """The entry in list `key` for the same work or person as e."""
        for nk, _ in (self.refs.name_keys(e["s"]) if e.get("s") else []):
            for l, s, x in self.people.get(nk, []):
                if l.key == key:
                    return x
        for wk in self.refs.work_keys(e):
            for l, s, x in self.works.get(wk, []):
                if l.key == key:
                    return x
        return None

    def find_title(self, title, key, sec_code):
        """An entry in list `key` (section first) whose citation has this title.
        Short titles in prose match a longer cited title word for word."""
        k = re.sub(r"^(the|a|an) ", "", store.fold(title))
        if len(k) < 4:
            return None
        pad = f" {k} "
        art = re.compile(r"^(the|a|an) ")
        lst = self.series.lists.get(key)
        if not lst:
            return None
        sec = self.refs.section_for(key, sec_code)
        pools = ([sec] if sec else []) + [None]
        for pool in pools:
            for s, e in lst.entries():
                if pool is not None and s is not pool and s.parent is not pool:
                    continue
                for t in self.refs.full_titles(e):
                    t = art.sub("", t)
                    if t == k or pad in f" {t} " and (len(k) >= 8 or t.startswith(k)):
                        return e
        return None

    def calendar_entry_citing(self, e):
        """The first calendar entry whose note cites one of e's works."""
        mine = {k for _, k in self.refs.work_keys(e)}
        if not mine:
            return None
        for lst in self.series.lists.values():
            if lst.kind != "calendar":
                continue
            for s, x in lst.entries():
                for t in italics(x.get("n") or ""):
                    k = re.sub(r"^(the|a|an) ", "", store.fold(re.split(r"[:?!]\s", t)[0]))
                    if k in mine:
                        return x
        return None

    def find_person(self, token, key, codes):
        def expand(c):                   # 'III.C–D': III.C and III.D
            m = re.match(r"^([IVX]+)\.([A-Z])–([A-Z])$", c)
            return [f"{m.group(1)}.{chr(x)}" for x in range(ord(m.group(2)), ord(m.group(3)) + 1)] if m else [c]

        lst = self.series.lists.get(key)
        if not lst:
            return None
        words = token.strip().split()
        if not words:
            return None
        sur = store.fold(words[-1])
        given = store.fold(words[0]) if len(words) > 1 else None
        codes = [x for c in codes for x in expand(c)]
        secs = [self.refs.section_for(key, c) for c in codes] or [None]
        cands = []
        from . import lives as L
        tok = store.fold(re.sub(r"\s*\([^)]*\)", "", token)).strip()
        natural, named = [], []          # names in their own order: by their last word; by a form that gives the word
        for s, e in lst.entries():
            if secs != [None] and s not in secs:
                continue
            if not e.get("s"):
                continue
            if "," not in e["s"]:        # a name in its own order ('Ngo Dinh Diem'): the whole, or the word it goes by
                if "group" in (e.get("tags") or []):
                    continue
                for n in re.split(r";\s*", plain(e["s"])):
                    n0 = re.sub(r"\s*\([^)]*\)", "", n).strip()
                    n = store.fold(n0)
                    if tok == n:
                        return e
                    if len(words) != 1:
                        continue
                    # the word it goes by: a form filed under it ('Diem, Ngo Dinh'; 'Ikeda, Hayato') or a title and it
                    # ('President Diem'); else the last word, where no other name of the section ends in it (Bui Diem)
                    forms = [store.fold(f) for f in L.name_forms(n0)[1:]]
                    own = set(n.split())
                    if tok in own and any("," in f and f.split(",")[0].strip() == tok
                                          and set(f.split(",", 1)[1].split()) <= own
                                          or f.split()[1:] == [tok] and len(f.split()) == 2 for f in forms):
                        named.append(e)
                    elif n.split()[-1:] == [sur]:
                        natural.append(e)
                continue
            for one in re.split(r";\s*", plain(e["s"])):     # 'Huntley, Chet; Brinkley, David': each
                if "," not in one:
                    continue
                esur, egiven = one.split(",", 1)
                if store.fold(esur).strip() == tok:  # the whole surname, of several words ('de Gaulle', 'Van Pelt')
                    cands.append(e)
                    break
                if store.fold(esur).split()[-1:] == [sur] or store.fold(esur) == sur:
                    if given and not store.fold(egiven).strip().startswith(given):
                        continue
                    cands.append(e)
                    break
        if cands:
            return cands[0]
        if len(named) == 1:
            return named[0]
        return natural[0] if len(natural) == 1 and not named else None

    def names_markup(self, chunk, key, internal=True):
        """A calendar note's 'Names: Heller, Tobin (K–J Adm. III.H)': each name marked to link to the person's name
        entry (or, failing one and where internal, to the Part III entry in the reader)."""
        refs = self.refs
        m = re.search(r"Names: (.*)$", chunk)
        if not m:
            return chunk
        head, body = chunk[:m.start(1)], m.group(1)
        groups = []
        for g in re.split(r"(;\s*)(?![^()]*\))", body):     # not at a ';' within the parentheses
            gm = re.match(r"^([^()]+?)\s*\(([^)]*)\)(.*)$", g)
            if not gm:
                groups.append(g)
                continue
            names_part, ref_part, rest = gm.groups()
            scanned = list(refs.scan(ref_part, key))
            if not scanned or "," in names_part and not re.search(r"[A-Za-z]", names_part):
                groups.append(g)
                continue
            lkey = scanned[0][2]
            codes = [c for _, _, k, c in scanned if c]
            linked = []
            for tok in re.split(r"(,\s*)", names_part):
                if re.match(r"^,\s*$", tok) or not tok.strip():
                    linked.append(tok)
                    continue
                x = self.find_person(tok, lkey, codes)
                u = self.name_url(x, tok) if x else None
                linked.append(f"[[§nmx:{u}|{tok}]]" if u else f"[[§nm:{x['id']}|{tok}]]" if x and internal else tok)
            groups.append("".join(linked) + f" ({ref_part})" + rest)
        return head + "".join(groups)

    def name_url(self, x, tok=None):
        """The name entry of the person a Part III entry names (the name of its subject line that tok's surname
        matches, where it names several), or None."""
        from . import namelinks
        names = [re.sub(r"\s*\([^)]*\)\s*$", "", n).strip() for n in re.split(r";\s*", plain(x.get("s") or ""))]
        names = [n for n in names if n]  # 'Rusk, Dean'; a name in its own order too ('Ngo Dinh Diem')
        if not names:
            return None
        if tok:
            sur = store.fold(tok.strip().split()[-1])
            names = [n for n in names if store.fold(n.split(",")[0]).split()[-1:] == [sur]] or names
        return namelinks.url(self.series, names[0])

    # -------------------------------------------------------- text
    def text_html(self, lst, sec, e):
        """A text renderer bound to one entry (or section prose when e is None)."""
        series, refs = self.series, self.refs

        def resolve(eid, shown):
            if eid.startswith("§"):
                cls, href = eid[1:].split(":", 1)
                if cls == "nmx":         # a person's name entry, on its own page (tools/bib/namelinks.py)
                    return f'<a class="nm" href="{attr(href)}">{to_html(shown)}</a>'
                return self.a(href, cls, to_html(shown))
            hit = series.get(eid)
            if not hit:
                return None
            return self.a(hit[2]["id"], "xd", esc(shown or label_of(series, eid)))

        def link_plain(chunk, field):
            out, pos = [], 0
            for a, b, key, code in refs.scan(chunk, lst.key):
                tgt_list = series.lists.get(key)
                if not tgt_list:
                    continue
                shown = chunk[a:b]
                if code:
                    s = refs.section_for(key, code)
                    if not s:
                        continue
                    out.append(chunk[pos:a] + f"[[§xr:{self.sec_id(s)}|{shown}]]")
                else:
                    target = f"{key}--top"
                    cls = "xl"
                    before = chunk[max(0, a - 40):a]
                    if e is not None and re.search(r"Also(?: in)?(?:[^.;()]*?)$", before) and key != lst.key:
                        x = self.same_thing(e, key)
                        if x:
                            target, cls = x["id"], "xr"
                    elif e is not None and tgt_list.kind == "calendar" and key != lst.key:
                        x = self.calendar_entry_citing(e)
                        if x:
                            target, cls = x["id"], "xr"
                    out.append(chunk[pos:a] + f"[[§{cls}:{target}|{shown}]]")
                pos = b
            out.append(chunk[pos:])
            return "".join(out)

        def link_titles(chunk):
            # *Title* followed (in the same clause) by a list and section
            def sub(m):
                tail = chunk[m.end():m.end() + 200]
                for a, b, key, code in refs.scan(tail, lst.key):
                    if re.search(r"\*|;|[a-z]\.\s", tail[:a]):
                        break  # the reference belongs to a later clause
                    if code:
                        x = self.find_title(m.group(1), key, code)
                        if x and (e is None or x["id"] != e["id"]):
                            return f"[[§xr xt:{x['id']}|*{m.group(1)}*]]"
                    break
                return m.group(0)
            return ITAL_RE.sub(sub, chunk)

        def link_names(chunk):
            return self.names_markup(chunk, lst.key)

        def render(t, field):
            if field in ("s",):
                h = to_html(t, resolve)
                if e is not None and refs.is_person(lst, sec, e):
                    from . import namelinks   # the subject's name entry, each name of a shared line its own
                    h = "; ".join(namelinks.a(series, plain(part), part) for part in h.split("; "))
                return h
            lead = ""
            if field == "c":             # the citation's authors, linked to their name entries
                from . import namelinks
                lead, t = namelinks.author_split(series, t)
                lead = lead or ""
            pieces = []
            for prot, chunk in split_protected(t):
                if prot:
                    pieces.append(chunk)
                    continue
                if field == "n":
                    chunk = link_names(chunk)
                    sub = []
                    for p2, c2 in split_protected(chunk):
                        sub.append(c2 if p2 else link_titles(c2))
                    chunk = "".join(sub)
                sub = []
                for p2, c2 in split_protected(chunk):
                    sub.append(c2 if p2 else link_plain(c2, field))
                pieces.append("".join(sub))
            return lead + to_html("".join(pieces), resolve)

        return render

    def elsewhere(self, lst, sec, e):
        if lst.kind == "calendar":
            return ""
        seen, out = set(), []
        hits = []
        if self.refs.is_person(lst, sec, e):
            for k, _ in self.refs.name_keys(e["s"]):
                hits += self.people.get(k, [])
        for wk in self.refs.work_keys(e):
            hits += self.works.get(wk, [])
        for l, s, x in hits:
            if l.key == lst.key or l.kind == "calendar" or x["id"] in seen:
                continue
            seen.add(x["id"])
            out.append(self.a(x["id"], "xr", esc(f"{l.abbr} {s.code}")))
        if not out:
            return ""
        self.n_elsewhere += 1
        return '<span class="x2">Elsewhere: ' + ", ".join(out) + "</span>"


def names_index(series, linker):
    people = {}
    for lst in series.lists.values():
        for sec, e in lst.entries():
            if not linker.refs.is_person(lst, sec, e):
                continue
            part = (sec.code or "").split(".")[0]
            for k, shown in linker.refs.name_keys(e["s"]):
                rec = people.setdefault(k, {"name": shown, "lines": []})
                role = plain(e["r"]) if part == "III" and e.get("r") else "Memoir or biography"
                rec["lines"].append((lst, sec, e, role))
    order = {k: i for i, k in enumerate(series.lists)}
    for rec in people.values():
        rec["lines"].sort(key=lambda x: (order[x[0].key], 0 if (x[1].code or "").startswith("III") else 1))
    by_letter = {}
    for k, rec in sorted(people.items(), key=lambda kv: store.fold(kv[1]["name"])):
        by_letter.setdefault(store.fold(rec["name"])[:1].upper(), []).append((k, rec))
    out = [f'<section class="list" id="L-nx" data-key="nx" hidden><h1 id="nx--top">{esc(series.data["names_index"]["title"])}</h1>',
           '<p class="lede">Every person in Part III of the lists, and every subject of a memoir or biography in Part II, merged by name. Each line gives the list, the section, and the role recorded there.</p>',
           '<p class="logic">Merged on surname and first given name. Two people who share both are run together; the roles will show it.</p>']
    for letter, recs in by_letter.items():
        out.append(f'<h2 id="nx--{letter}" data-short="{letter}">{letter}</h2><ol class="e nx">')
        for k, rec in recs:
            lines = "".join(
                f'<span class="o">{linker.a(e["id"], "xr", esc(f"{l.abbr} {s.code}"))} {esc(role)}</span>'
                for l, s, e, role in rec["lines"])
            out.append(f'<li id="nx--{attr(k.replace(" ", "-"))}"><span class="s">{esc(rec["name"])}</span>{lines}</li>')
        out.append("</ol>")
    out.append("</section>")
    return "\n".join(out), len(people)


def build_series(series):
    linker = Linker(series)
    body = []
    meta, order = {}, ["home"]
    for lst in series.lists.values():
        m = lst.meta
        meta[lst.key] = {"abbr": m["abbr"], "title": m["title"], "span": m.get("span", ""), "group": m.get("group", "")}
        order.append(lst.key)
        idfmt = linker.sec_id
        out = [f'<section class="list" id="L-{lst.key}" data-key="{lst.key}" hidden><h1 id="{lst.key}--top">{esc(lst.data["h1"])}</h1>']
        prose = linker.text_html(lst, None, None)
        if lst.data.get("lede"):
            out.append(f'<p class="lede">{prose(lst.data["lede"], "lede")}</p>')
        for p in store.as_list(lst.data.get("logic")):
            out.append(f'<p class="logic">{prose(p, "logic")}</p>')

        def text_html_for(sec):
            return linker.text_html(lst, sec, None)

        def li_extra(sec, e):
            return f' data-sec="{idfmt(sec)}"', linker.elsewhere(lst, sec, e)

        for s in lst.sections:
            out.extend(_section_series(series, lst, s, linker, li_extra))
        out.append("</section>")
        body.append("\n".join(out))
    meta["home"] = {"abbr": "Series", "title": series.data["title"], "span": "", "group": ""}
    meta["nx"] = {"abbr": "Names", "title": series.data["names_index"]["title"], "span": "", "group": ""}
    order.append("nx")
    nx, n_people = names_index(series, linker)

    # home page, written last so it can quote the counts
    h = series.data["home"]
    home = [f'<section class="list" id="L-home" data-key="home" hidden><h1 id="home--top">{esc(h["h1"])}</h1>',
            f'<p class="lede">{to_html(h["lede"])}</p>']
    for p in h.get("logic", []):
        p = p.replace("{counts}", f"{linker.links} links and {linker.n_elsewhere} such lines in all.")
        home.append(f'<p class="logic">{to_html(p)}</p>')
    groups = {}
    for lst in series.lists.values():
        groups.setdefault(lst.meta.get("group", ""), []).append(lst)
    for g, lsts in groups.items():
        gid = "home--" + (g.split("–")[0] if g else "other")
        home.append(f'<h2 id="{gid}" data-short="{attr(g)}">{esc(g)}</h2><ol class="e lists">' + "".join(
            f'<li><a class="lk" href="#{l.key}--top"><span class="ab">{esc(l.abbr)}</span>'
            f'<span class="tt">{esc(l.meta["title"])}, {esc(l.meta.get("span", ""))}</span></a>'
            f'<span class="r">{sum(1 for _ in l.entries())} entries</span></li>' for l in lsts) + "</ol>")
    home.append('<h2 id="home--nx" data-short="Names">Names</h2><ol class="e lists"><li><a class="lk" href="#nx--top">'
                f'<span class="ab">Names</span><span class="tt">Every person across the {NUMBERS.get(len(series.lists), len(series.lists))} lists, merged</span></a>'
                f'<span class="r">{n_people} names</span></li></ol>')
    home.append('<h2 id="home--cg" data-short="Congress">Congress</h2><ol class="e lists"><li><a class="lk" href="congress.html">'
                '<span class="ab">Congress</span><span class="tt">Each Congress at its opening, 1961–1973: party bars, House and Senate maps, every member</span></a>'
                '<span class="r">87th–93rd</span></li></ol>')
    home.append('<h2 id="home--ex" data-short="Executive">The Executive Branch</h2><ol class="e lists"><li><a class="lk" href="executive.html">'
                '<span class="ab">Executive</span><span class="tt">The Executive Branch at each inauguration, 1953–1974: every office, its authority, its holders</span></a>'
                '<span class="r">1953–74</span></li></ol>')
    home.append("</section>")

    page = open(os.path.join(TEMPLATES, "series.html"), encoding="utf-8").read()
    page = (page.replace("{{title}}", esc(series.data["title"]) + ": bibliographies and calendar")
                .replace("{{main}}", "\n".join(home) + "\n" + "\n".join(body) + "\n" + nx)
                .replace("{{meta}}", json.dumps(meta, ensure_ascii=False))
                .replace("{{order}}", json.dumps(order)))
    page = page.replace("<head>", "<head>\n" + source_note(series, "lists/"), 1)
    return page, linker


def _section_series(series, lst, sec, linker, li_extra):
    out = [headings(lst, sec, linker.sec_id)]
    prose = linker.text_html(lst, sec, None)
    for p in sec.logic:
        out.append(f'<p class="logic">{prose(p, "logic")}</p>')
    if by_day(lst, sec):
        def li(e, rub):
            a, s = li_extra(sec, e)
            return entry_html(series, lst, sec, e, linker.text_html(lst, sec, e), a, s, rub)
        out.extend(daybook.section_days(lst, sec, li, thread_name))
    elif sec.entries:
        out.append('<ol class="e">')
        for e in sec.entries:
            a, s = li_extra(sec, e)
            out.append(entry_html(series, lst, sec, e, linker.text_html(lst, sec, e), a, s))
        out.append("</ol>")
    for c in sec.children:
        out.extend(_section_series(series, lst, c, linker, li_extra))
    return out


def run(series, which=None):
    os.makedirs(OUT, exist_ok=True)
    written = []
    PAGES = ("series", "congress", "executive", "names", "lives")
    keys = [which] if which and which not in PAGES else ([] if which in PAGES else list(series.lists))
    from . import congress, executive, indicators
    daybook.SERIES = series                  # the FRUS senders' name entries
    linker = None
    for k in keys:
        path = os.path.join(OUT, f"{k}.html")
        linker = linker or Linker(series)
        page = build_list(series, k, linker)
        if series.lists[k].kind == "calendar":
            linker = linker or Linker(series)
            page = congress.inject(page, series, linker, "list")
            page = executive.inject(page, series, linker, "list")
            page = specials.inject(page, series)
            page = primaries.inject(page, series)
            page = indicators.inject(page, series, "list")
            page = daybook.inject(page)
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
        written.append(path)
    if which in (None, "series"):
        page, linker = build_series(series)
        page = congress.inject(page, series, linker, "series")
        page = executive.inject(page, series, linker, "series")
        page = specials.inject(page, series)
        page = primaries.inject(page, series)
        page = indicators.inject(page, series, "series")
        page = daybook.inject(page)
        path = os.path.join(OUT, "series.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
        written.append(path)
    if which in (None, "congress"):
        linker = linker or Linker(series)
        page = congress.page(series, linker, os.path.join(TEMPLATES, "list.html"))
        if page:
            path = os.path.join(OUT, "congress.html")
            with open(path, "w", encoding="utf-8") as f:
                f.write(page)
            written.append(path)
    if which in (None, "executive"):
        linker = linker or Linker(series)
        page = executive.page(series, linker, os.path.join(TEMPLATES, "list.html"))
        if page:
            path = os.path.join(OUT, "executive.html")
            with open(path, "w", encoding="utf-8") as f:
                f.write(page)
            written.append(path)
    if which in (None, "names", "lives"):
        from . import lives
        linker = linker or Linker(series)
        for name, page in lives.pages(series, linker, os.path.join(TEMPLATES, "list.html")).items():
            path = os.path.join(OUT, name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(page)
            written.append(path)
    return written
