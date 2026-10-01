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

from . import store
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

def entry_html(series, lst, sec, e, text_html, extra_attrs="", extra_spans=""):
    parts = []
    year = (e.get("date") or "")[:4] if lst.kind == "calendar" else None
    subj = entry_subject(lst, e)
    if subj:
        parts.append(f'<span class="s">{text_html(subj, "s")}</span>')
    for c in store.as_list(e.get("c")):
        parts.append(f'<span class="c">{text_html(year_qualified(series, c, year), "c")}</span>')
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
    if e.get("conflict"):
        parts.append('<span class="n"><b>Unresolved merge conflict.</b></span>')
    return f'<li id="{attr(e["id"])}"{extra_attrs}>' + "".join(parts) + extra_spans + "</li>"


def headings(lst, sec, idfmt):
    tag = f"h{min(sec.level, 4)}"
    num = f'<span class="num">{esc(sec.num)}</span>' if sec.num else ""
    return f'<{tag} id="{idfmt(sec)}" data-short="{attr(sec.label)}">{num}{to_html(sec.title)}</{tag}>'


def section_body(series, lst, sec, idfmt, text_html, li_extra=None):
    out = [headings(lst, sec, idfmt)]
    for p in sec.logic:
        out.append(f'<p class="logic">{text_html(p, "logic")}</p>')
    if sec.entries:
        out.append('<ol class="e">')
        for e in sec.entries:
            a, s = li_extra(sec, e) if li_extra else ("", "")
            out.append(entry_html(series, lst, sec, e, text_html, a, s))
        out.append("</ol>")
    for c in sec.children:
        out.extend(section_body(series, lst, c, idfmt, text_html, li_extra))
    return out


# ---------------------------------------------------------------- one list, standalone

def build_list(series, key):
    lst = series.lists[key]

    def resolve(eid, shown):
        hit = series.get(eid)
        if not hit:
            return None
        tl, ts, te = hit
        text = esc(shown or label_of(series, eid))
        if tl.key == key:
            return f'<a href="#{attr(te["id"])}">{text}</a>'
        return text

    def text_html(t, field):
        return to_html(t, resolve)

    main = [f"<h1>{esc(lst.data['h1'])}</h1>"]
    if lst.data.get("lede"):
        main.append(f'<p class="lede">{text_html(lst.data["lede"], "lede")}</p>')
    for p in store.as_list(lst.data.get("logic")):
        main.append(f'<p class="logic">{text_html(p, "logic")}</p>')
    main.append('<p class="logic">To navigate, use the Outline button, the contents below, or the handle on the right edge, which you can drag to see nearby headings.</p>')
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
        lst = self.series.lists.get(key)
        if not lst:
            return None
        words = token.strip().split()
        if not words:
            return None
        sur = store.fold(words[-1])
        given = store.fold(words[0]) if len(words) > 1 else None
        secs = [self.refs.section_for(key, c) for c in codes] or [None]
        cands = []
        for s, e in lst.entries():
            if secs != [None] and s not in secs:
                continue
            if not e.get("s") or "," not in e["s"]:
                continue
            esur, egiven = plain(e["s"]).split(",", 1)
            if store.fold(esur).split()[-1:] == [sur] or store.fold(esur) == sur:
                if given and not store.fold(egiven).startswith(given):
                    continue
                cands.append(e)
        return cands[0] if cands else None

    # -------------------------------------------------------- text
    def text_html(self, lst, sec, e):
        """A text renderer bound to one entry (or section prose when e is None)."""
        series, refs = self.series, self.refs

        def resolve(eid, shown):
            if eid.startswith("§"):
                cls, href = eid[1:].split(":", 1)
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
            m = re.search(r"Names: (.*)$", chunk)
            if not m:
                return chunk
            head, body = chunk[:m.start(1)], m.group(1)
            groups = []
            for g in re.split(r"(;\s*)", body):
                gm = re.match(r"^([^()]+?)\s*\(([^)]*)\)(.*)$", g)
                if not gm:
                    groups.append(g)
                    continue
                names_part, ref_part, rest = gm.groups()
                scanned = list(refs.scan(ref_part, lst.key))
                if not scanned or "," in names_part and not re.search(r"[A-Za-z]", names_part):
                    groups.append(g)
                    continue
                key = scanned[0][2]
                codes = [c for _, _, k, c in scanned if c]
                linked = []
                for tok in re.split(r"(,\s*)", names_part):
                    if re.match(r"^,\s*$", tok) or not tok.strip():
                        linked.append(tok)
                        continue
                    x = self.find_person(tok, key, codes)
                    linked.append(f"[[§nm:{x['id']}|{tok}]]" if x else tok)
                groups.append("".join(linked) + f" ({ref_part})" + rest)
            return head + "".join(groups)

        def render(t, field):
            if field in ("s",):
                return to_html(t, resolve)
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
            return to_html("".join(pieces), resolve)

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
    if sec.entries:
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
    keys = [which] if which and which != "series" else ([] if which == "series" else list(series.lists))
    for k in keys:
        path = os.path.join(OUT, f"{k}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build_list(series, k))
        written.append(path)
    if which in (None, "series"):
        page, linker = build_series(series)
        path = os.path.join(OUT, "series.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
        written.append(path)
    return written
