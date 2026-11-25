"""A calendar entry's citation block as footnotes (the owner, Nov. 18, 2026, choosing layout A of the preview: "Implement A
and superscript"; "Implement 'Id.' both within and across citations"; "Citation blocks with only one citation should be
rendered without the footnote"; the indent as the law reviews set it).

STYLE
 1. The claims are the units of `c` (claims.py, STYLE 1) and each unit's sources the rows of the entry's map (a reader's
    `src`, else the mechanical one). A run of units with the same sources closes with a mark, a superscript numeral; the
    numbers restart with each entry. The note's sources follow the line as footnotes, numbered; the rest of the note
    ("Made public", "To check", "See", "Names", "Check") after them, as now.
 2. One footnote or none: the entry is shown as before, the note as one block, no mark (the owner: "they should look like
    they do at present"). So too where the map is stale or its units cannot be found in the rendered line.
 3. A footnote's sources in the map's order, each as the note prints it (its pinpoint and parenthetical); a row whose
    page differs from the note's item gives its own page; a work's note reached through it (`via`) as "Work, 88 & n.32
    (citing the record)", or "88 n.32 (citing ...)" alone, several of its notes at one page as one, "190 & n.27
    (citing A; B)" (the note's letters dropped; a note keyed by its words, the page alone); the record's "printed,
    FRUS ..." not repeated where it names its print or the note cites it. A record the map names that the note cites
    in its printing or recording (a FRUS document, the Papers' page, the Miller Center's or PRDE's tape) is no
    source of its own: the print cited is (the owner, Nov. 21, 2026). One item twice (two links of one cite) once.
    Sources the map has not yet given units (`?`) and items of the note no row names close the last footnote, but the
    day's label's (the chamber's sitting, DAY_LABEL), which go in the first, as the mechanical map gives them
    (claims.py, STYLE 7; the owner, Nov. 21, 2026: "should only be in the first footnote"). A label's items (claims.py, STYLE 7: "The Senate sat from noon to 7:02 p.m.: Daily Digest, D468") are a sentence of
    their own under the label, the footnote's other cites citation sentences; each sentence closes with a full stop.
 4. *id*. (the owner: "italicize the 'id' but leave the full stop in plain roman ... A departure from the Bluebook"): a
    citation of the work cited immediately before, in the same footnote or as the previous footnote's only authority
    (Bluebook 4.1), is "*id*." when the pinpoint is the same, "*id*. at 89 n.35" when it differs within the volume,
    "*id*., V, 12" when the volume differs; capitalized at a footnote's head; a link or an unlinked item cited again,
    word for word, "*id*.".
 5. The first citation of a work on the page is printed in full (works.py, FIRST CITE): the footnotes are run through it
    in their order, so the full form falls in the first footnote that cites the work; the footnotes' own characters
    stay as written; the line's characters are dropped (a 'Names:' person's given after his name, a quoted original
    in "The words:", cjk.py, STYLE 3, 7), and its units rendered the same way, so the marks still land.
 6. The marks sit inside the last claim's span (vispage.py), so a hidden claim takes its mark with it.
 7. A record the map names (`via x.…`, or a work's note, `via w.… 88 n.32`) that no reader has read (its row's `read`
    not true) is no source of a claim and is not printed in a footnote (the owner, Nov. 21, 2026: "the citation block
    has unmarked citations to unread works, which should be behind 'To check:' with a 'via'/'cited by' note"); it is
    joined to the note's "To check:" as the page shows it, in the footnotes' layout and the one block's alike, unless
    the note holds it already (below, "what the note already cites"; the owner, the same day: "I don't want to drop
    the unread works. Can you check and fix the doubles instead?").
 8. Sources every footnote shares (the owner: "Citation blocks with only one citation should be rendered without the
    footnote"; of four footnotes each repeating the note): where COMMON (3) or more of them stand under every mark,
    REPEAT "block" shows the entry as one block, as STYLE 2 does (shared()); "first" gives them once, in note 1, the
    later notes opening "Sources cited *supra* note 1"; None repeats them, as before.
 9. A link the line itself carries (a vote, a statute, a case: claims.py, STYLE 5) is the line's own citation; in a
    footnote it is given in its citation form, not as the bare link text (_line): a roll call "[S. Roll Call No. 144,
    88th Cong. (1963)](…) (Voteview)"; a statute as the Statutes list (K–J Cong. II.J.2) and Bluebook 12 write it, at
    its first on the page in full, "Act of Oct. 17, 1963, Pub. L. No. 88-152, [77 Stat. 271](…)" (its name where the
    list has one, "Area Redevelopment Act, Pub. L. No. 87-27, [75 Stat. 47](…) (1961)"), short after, "Pub. L. No.
    88-152, [77 Stat. at 271](…)" (_line_firsts); a case or treaty with the name the line gives it and its year,
    "*Baker v. Carr*, [369 U.S. 186](…) (1962)".
10. The other pages that show a calendar entry's line and note (the owner, Nov. 21, 2026: "Could the Names and Threads
    entries also get the full footnote treatment?") set them by apply() and notes_html(), the calendar's own: the
    Threads pages through the calendar's renderer (threads.py), the Names' Life paragraphs (lives.py), whose anchors
    carry the person's key (an entry two persons of one page give, each its own).
11. A work's page and a note on that page are one source when neighbouring units are compared
    (notes/proposals/claims-model.md, (f) 3; ruling 35f): a unit that cites "88" and the next that cites "88 & n.32
    (citing ...)", or the note alone, make one run, under the fuller citation, with the page where either unit cites
    it. Two different notes of one page stay two sources. The registry and the map keep the rows apart.
"""
import collections
import re

from . import claims, witnesses

PAGE_NOTE_ONE = True                      # STYLE 11

# the day's label: the chamber's sitting ("The Senate sat from noon to 8:05 p.m.: [Daily Digest, D3](…)"); a label
# of one fact ("After the NSC: …") stays with the sources no row names, at the end (STYLE 3)
DAY_LABEL = re.compile(r"The (?:Senate|House)\b[^:]*\b(?:sat|met)\b")
SEP = "\n\n"          # between footnotes while the note's passes run over them as one text
MARK = "{}"


def _vol(pin):
    m = re.match(r"^([IVXLC]+),\s*(.+)$", pin or "")
    return (m.group(1), m.group(2)) if m else (None, pin or "")


_REG = {}


def _register(series):
    """The witness register, once per series (a build asks for it per entry; witnesses.load stats every file)."""
    if _REG.get("series") is not series:
        _REG["series"], _REG["reg"], _REG["load"] = series, claims.register(series), witnesses.load()
    return _REG["reg"]


def _load(series):
    """witnesses.load(), once per series (as _register)."""
    _register(series)
    return _REG["load"]


# How the footnotes treat sources every footnote shares (STYLE 8): where COMMON or more of them stand under every
# footnote, "block" shows the entry as one block (STYLE 2); "first" gives them once, in note 1, the later notes opening
# "Sources cited *supra* note 1"; None repeats them under every mark, as before Nov. 21, 2026.
REPEAT = "block"
COMMON = 3
MONTHS = r"(?:Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)\.?"


def _ord(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


_STATS = {}


def _statutes(series):
    """{(vol, page): (name, Pub. L. number, year)}: the Statutes list's entries (K–J Cong. II.J.2, "Area Redevelopment
    Act, [Pub. L. No. 87-27, 75 Stat. 47](…) (1961)"), and sources/statute-links.json's public-law numbers."""
    if _STATS.get("series") is series:
        return _STATS["idx"]
    import json
    import os
    from . import store
    idx = {}
    p = os.path.join(store.ROOT, "sources", "statute-links.json")
    try:
        for k in json.load(open(p, encoding="utf-8")):
            v, pg, _, pl = (k.split("|") + ["", "", "", ""])[:4]
            m = re.match(r"Pub\. L\. (\d+-\d+)", pl)
            if m:
                idx[(v, pg)] = (None, m.group(1), None)
    except (OSError, ValueError):
        pass
    for lst in series.lists.values():
        if lst.kind == "calendar":
            continue
        for _, e in lst.entries():
            m = re.match(r"^(.+?),\s*\[Pub\. L\. No\. (\d+-\d+), (\d+) Stat\. (\d+)[^\]]*\]\([^)]*\)(?:\s*\((\d{4})\))?",
                         str(e.get("c") or ""))
            if m:
                idx[(m.group(3), m.group(4))] = (m.group(1), m.group(2), m.group(5))
    _STATS.update(series=series, idx=idx)
    return idx


def _line(series, e, unit, lk):
    """A link the line carries, as a footnote cites it (STYLE 9): a roll call, "[S. Roll Call No. 144, 88th Cong.
    (1963)](…) (Voteview)"; a statute in full, "Act of Oct. 17, 1963, Pub. L. No. 88-152, [77 Stat. 271](…)", and
    short, "Pub. L. No. 88-152, [77 Stat. at 271](…)"; a case or other cite with the name the line gives it before and
    its year, "*Gideon v. Wainwright*, [372 U.S. 335](…) (1963)"."""
    text, url = lk.group(1), lk.group(2)
    year = str(e.get("date") or "")[:4]
    before, after = unit[:lk.start()], unit[lk.end():]
    yu = re.search(r"\b(19\d\d)\b", before)
    year = yu.group(1) if yu and re.search(MONTHS + r" \d{1,2}, 19\d\d\s*,?\s*$", before) else year
    v = re.search(r"voteview\.com/rollcall/R([HS])(\d{3})(\d{4})", url)
    if v:
        full = f"[{v.group(1)}. Roll Call No. {int(v.group(3))}, {_ord(int(v.group(2)))} Cong. ({year})]({url}) (Voteview)"
        return dict(kind="line", key=url, pin="", paren="", text=full, full=full, short=full, stat=None)
    s = re.match(r"^(?:Pub\. L\.(?: No\.)? (\d+-\d+), )?(\d+) Stat\. (\d+)$", text)
    if s and "STATUTE" in url:
        vol, page = s.group(2), s.group(3)
        name, pl, y = _statutes(series).get((vol, page), (None, None, None))
        pl = pl or s.group(1)
        d = re.search(r"\b(?:[Ss]igned|[Aa]pproved|[Ee]nacted)\b[^.;]*?\b(" + MONTHS + r" \d{1,2})(?:, (\d{4}))?[^.;]*$",
                      before)
        if not d and re.search(r"\b(?:[Ss]igned|[Aa]pproved|[Ee]nacted)\b[^.;]*$", before) and e.get("when"):
            w = re.match(r"^(" + MONTHS + r" \d{1,2})$", str(e["when"]).strip())
            d = w and re.match(r"(.*)()", w.group(1))
        y = y or (d.group(2) if d and d.group(2) else year)
        pls = f"Pub. L. No. {pl}, " if pl else ""
        if name:
            head = f"{name}, "
        elif d:
            head = f"Act of {d.group(1)}, {y}, "
        else:
            head = ""
        full = f"{head}{pls}[{vol} Stat. {page}]({url})" + ("" if y in head else f" ({y})")
        short = f"{pls}[{vol} Stat. at {page}]({url})"
        return dict(kind="line", key=f"stat:{vol}:{page}", pin="", paren="", text=full, full=full, short=short,
                    stat=(vol, page))
    nm = re.search(r"\*([^*]+)\*,?\s*$", before)
    pr = re.match(r"^,?\s*(\([^()]*\b\d{4}\))", after)
    tail = f" {pr.group(1)}" if pr else ("" if re.search(r"\b\d{4}\b", text) else f" ({year})")
    full = (f"*{nm.group(1)}*, " if nm else "") + lk.group(0) + tail
    return dict(kind="line", key=url, pin="", paren="", text=full, full=full, short=full, stat=None)


def _citing(rec, cited):
    """A record a work's note cites, as "citing" gives it: its words and where it is, the "printed, FRUS ..." echo left
    out where the record already names the print or the note cites it (STYLE 3)."""
    if not rec:
        return "a record"
    what = str(rec.get("record") or rec.get("what") or "")
    keep = []
    for seg in witnesses._split_top(witnesses.cite_where(rec.get("where"))):
        if _PROV.match(seg):                 # "repository not given in the note", "as cited": the registry's own words
            continue
        seg = _PROV_TAIL.sub("", seg).strip()
        body = re.sub(r"^(?:printed|published|reprinted)(?:,| in)?\s*", "", seg)
        if body != seg and (cited.printed(rec) or (fold(body).split()[:1] and fold(body).split()[0] in fold(what).split())):
            continue
        if seg:
            keep.append(seg)
    where = "; ".join(keep)
    return f"{what}, {where}" if where and fold(where) not in fold(what) else what


def _cites(series, e):
    """Per unit, its sources as dicts (kind, key, pin, paren, text, label); the `?` rows and unrowed items: the tail;
    the unread records (STYLE 7)."""
    c = e.get("c") or ""
    us = claims.units(c)
    rows = claims.resolve(e)
    reg = _register(series)
    wrows = _load(series)[0]
    srcs, _ = claims.note_parts(e.get("n"))
    labels = claims.note_labels(e.get("n"))
    cited = Cited(e)
    used = set()

    def lab(item, d):
        """An item's label (STYLE 7): kept as the head of its sentence, the item without it."""
        L = labels.get(item)
        if L:
            d["label"] = L
            if d["text"].startswith(L + ": "):
                d["text"] = d["text"][len(L) + 2:]
        return d

    def card(key, pin, item, row_pin):
        k = claims.item_key(item) if item else None
        if k and k[0] == "card" and k[1] == key and (not row_pin or k[2] == row_pin):
            used.add(item)
            return lab(item, dict(kind="card", key=key, pin=k[2] or "", paren=k[3] or "", text=item))
        if item:
            used.add(item)
        return dict(kind="card", key=key, pin=row_pin or "", paren="", text=f"[[{key}]]" + (f", {row_pin}" if row_pin else ""))

    def via(key, pin, notes, joined):
        recs = [reg.get((key, str(pin), str(nt))) for nt in notes]
        for r in recs:                           # a record no reader has read: behind "To check:" (STYLE 7)
            if r and not r.get("read"):
                unread.setdefault(r.get("id"), None)
        keep = [(nt, r) for nt, r in zip(notes, recs) if not r or r.get("read")]
        if not keep:
            if not joined:
                return None
            return dict(kind="card", key=key, pin=str(pin), paren="", text=f"[[{key}]], {pin}")
        notes, recs = [nt for nt, _ in keep], [r for _, r in keep]
        nums = list(dict.fromkeys(re.sub(r"(?<=\d)[a-z]$", "", str(nt)) for nt in notes))
        if not all(re.fullmatch(r"\d+(?:[–-]\d+)?", x) for x in nums):
            ns = ""                              # a note keyed by its words ("i-cant-buy-this.a"): the page alone
        else:
            ns = (f"n.{nums[0]}" if len(nums) == 1 else "nn." + ", ".join(nums))
        what = "; ".join(dict.fromkeys(_citing(r, cited) for r in recs))
        p = (f"{pin} & {ns}" if joined else f"{pin} {ns}") if ns else str(pin)
        d = dict(kind="card", key=key, pin=p, paren=f"(citing {what})", text=f"[[{key}]], {p} (citing {what})",
                 base=str(pin), notes=tuple(str(nt) for nt in notes), joined=joined)
        if not joined:                           # the form it takes where a neighbouring unit cites the page (STYLE 11)
            d["alt"] = via(key, pin, notes, True)
        return d

    per, unread = [], {}
    for i, unit in enumerate(us):
        L = claims.LETTERS[i]
        mine = [(k, key, pin, note, item) for r, k, key, pin, note, u, item in rows
                if k and u not in (None, "?") and L in u]
        vias = collections.defaultdict(list)
        for k, key, pin, note, _ in mine:
            if k == "via":
                vias[(key, pin)].append(note)
        out, done = [], set()
        for k, key, pin, note, item in mine:
            if k == "card" and (key, pin) in vias:
                if item:
                    used.add(item)
                out.append(via(key, pin, vias[(key, pin)], True))
                done.add((key, pin))
            elif k == "via":
                if (key, pin) in done or any(k2 == "card" and (key2, pin2) == (key, pin) for k2, key2, pin2, _, _ in mine):
                    continue
                done.add((key, pin))
                v = via(key, pin, vias[(key, pin)], False)
                if v:
                    out.append(v)
            elif k == "card":
                out.append(card(key, pin, item, pin))
            elif k == "witness":
                w = wrows.get(key) or {}
                if not w.get("read"):            # a record no reader has read: behind "To check:" (STYLE 7)
                    unread.setdefault(key, None)
                    continue
                if cited.printed(w) or cited.recorded(w):
                    continue                     # its print or recording the note cites: that is the source (STYLE 3)
                text = claims._render_row(series, e, "witness", key, pin, note, item, reg)
                out.append(dict(kind="text", key=text, pin="", paren="", text=text))
            else:
                if item:
                    used.add(item)
                lk = next((m for m in claims.LINK.finditer(unit) if m.group(2) == key), None) if k == "url" else None
                if lk and item not in srcs:      # the line's own link (STYLE 9)
                    out.append(_line(series, e, unit, lk))
                    continue
                text = item or key
                out.append(lab(item, dict(kind=k, key=text, pin="", paren="", text=text)))
        seen, uniq = set(), []
        for x in out:                            # one item twice (two links of one cite): once
            if (x["kind"], x["key"], x["text"]) not in seen:
                seen.add((x["kind"], x["key"], x["text"]))
                uniq.append(x)
        per.append(uniq)
    tail = []

    def unrowed(item):
        """An item no row gives units: at the end; the day's label's (DAY_LABEL), the first unit's, where the day's
        facts sit (STYLE 3; claims.py, STYLE 7)."""
        d = lab(item, dict(kind="text", key=item, pin="", paren="", text=item))
        (per[0] if per and DAY_LABEL.match(d.get("label") or "") else tail).append(d)
    for r, k, key, pin, note, u, item in rows:
        if u == "?" and item and item not in used:
            used.add(item)
            unrowed(item)
    for it in srcs:                       # an item of the note no row names: kept, at the end
        if it not in used and not any(it == x["text"] for p in per for x in p):
            used.add(it)
            unrowed(it)
    return us, per, tail, list(unread)


def _id(cur, prev, head):
    """The citation, or its id. form where it repeats prev (STYLE 4)."""
    I = "*Id*." if head else "*id*."
    if prev is None or cur["key"] != prev["key"]:
        return cur["text"]
    if cur["kind"] != "card":
        return I if cur["text"] == prev["text"] else cur["text"]
    paren = (" " + cur["paren"]) if cur["paren"] else ""
    if cur["pin"] == prev["pin"]:
        return I + paren
    cv, cp = _vol(cur["pin"])
    pv, _ = _vol(prev["pin"])
    if not cur["pin"]:
        return cur["text"]
    if cv == pv or cv is None:
        return f"{I} at {cp}{paren}"
    return f"{I}, {cur['pin']}{paren}"


def _ck(x):
    return (x["kind"], x["key"], x["pin"], x.get("label"))


def _footnote(cites, prev_note, stat_first, printed):
    """One footnote's text (STYLE 3, 4, 7): its cites in order, a label's items a sentence of their own under the label,
    the rest citation sentences, each closed with a full stop."""
    sents = []
    for x in cites:
        if x.get("label"):
            s = next((s for s in sents if s[0] == x["label"]), None)
            if s:
                s[1].append(x)
            else:
                sents.append([x["label"], [x]])
        elif sents and sents[-1][0] is None:
            sents[-1][1].append(x)
        else:
            sents.append([None, [x]])
    single_prev = prev_note if prev_note and len({y["key"] for y in prev_note}) == 1 else None
    prev, out = (single_prev[-1] if single_prev else None), []
    for L, xs in sents:
        parts = []
        for j, x in enumerate(xs):
            if x["kind"] == "line" and x.get("stat"):
                full = stat_first(x["stat"]) and x["stat"] not in printed
                printed.add(x["stat"])
                x = dict(x, text=x["full"] if full else x["short"])
            parts.append(x["text"] if L else _id(x, prev, j == 0))
            prev = None if L else x
        body = "; ".join(parts)
        out.append((f"{L}: " if L else "") + body + ("" if body.endswith(".") else "."))
    return " ".join(out)


def shared(runs, mode=REPEAT, k=COMMON):
    """The runs [(key, last unit, cites)] with the sources every one of them cites (STYLE 8): None (the entry one
    block) where k or more and mode "block"; given once, in the first, where mode "first"; else as they are."""
    if not mode or len(runs) < 2:
        return runs
    common = set.intersection(*[{_ck(x) for x in r[2]} for r in runs])
    if len(common) < k:
        return runs
    if mode == "block":
        return None
    sup = dict(kind="supra", key="supra", pin="", paren="", text="Sources cited *supra* note 1")
    return [runs[0]] + [[key, last, [sup] + [x for x in cites if _ck(x) not in common]] for key, last, cites in runs[1:]]


def _one(a, b):
    """Two neighbouring units' sources as one list, where they differ only in that one cites a work's page and the
    other a note on that page, or the page with the note (STYLE 11); else None."""
    if len(a) != len(b):
        return None
    out = []
    for x, y in zip(a, b):
        if (x["kind"], x["key"], x["pin"]) == (y["kind"], y["key"], y["pin"]):
            out.append(x)
            continue
        if x["kind"] != "card" or y["kind"] != "card" or x["key"] != y["key"]:
            return None
        if x.get("base", x["pin"]) != y.get("base", y["pin"]):
            return None
        nx, ny = x.get("notes"), y.get("notes")
        if nx is not None and ny is not None and nx != ny:
            return None                        # two notes of one page: two sources
        full = x if nx is not None else y
        page = nx is None or ny is None or x.get("joined") or y.get("joined")     # a unit cites the page itself
        out.append(full if full.get("joined") or not page else full["alt"])
    return out


def build(series, e, _probe=False):
    """None where the entry is shown as before (STYLE 2); else (groups, notes, rest): groups, the index of each run's
    last unit and its footnote's number; notes, each footnote's markup; rest, the note's other sentences."""
    c = e.get("c")
    if not isinstance(c, str) or not c or not e.get("n"):
        return None
    src = e.get("src")
    if isinstance(src, dict) and src.get("c") and src.get("c") != claims.chash(c):
        return None                       # a stale map: its letters may not fit (claims.py, STYLE 4)
    us, per, tail, unread = _cites(series, e)
    runs = []
    for i in range(len(us)):
        key = [(x["kind"], x["key"], x["pin"]) for x in per[i]]
        one = _one(runs[-1][2], per[i]) if runs and PAGE_NOTE_ONE else None
        if runs and runs[-1][0] == key:
            runs[-1][1] = i
        elif one is not None:                  # a page and its note, one source (STYLE 11)
            runs[-1][1:] = [i, one]
            runs[-1][0] = [(x["kind"], x["key"], x["pin"]) for x in one]
        else:
            runs.append([key, i, per[i]])
    if tail:
        if runs and runs[-1][2]:
            runs[-1][2] = runs[-1][2] + tail
        elif runs:
            runs[-1][2] = tail
    runs = [r for r in runs if r[2]]
    if len(runs) <= 1:
        return None
    runs = shared(runs, REPEAT, COMMON)    # the sources every footnote shares (STYLE 8)
    if runs is None:
        return None
    firsts = set() if _probe else _line_firsts(series)
    printed = set()
    groups, notes, prev_note, stats = [], [], None, set()
    for key, last, cites in runs:
        stats |= {x["stat"] for x in cites if x.get("stat")}
        notes.append(_footnote(cites, prev_note, lambda st: _probe or (e["id"], st) in firsts, printed))
        groups.append((last, len(notes)))
        prev_note = cites
    if _probe:
        return stats
    rest = with_unread(series, e, " ".join(claims.note_parts(e.get("n"))[1]))
    return groups, notes, rest


def apply(series, e, c, body, render, anchor=None):
    """A calendar entry's line with its footnotes, on any page that shows it (the calendar's, the Names', the
    Threads'): (body, fns), body the rendered line `c` with each run's mark placed (STYLE 1, 6; render, a unit
    rendered as the line is) and fns as build() gives it; (body, None) where the entry is one block (STYLE 2) or its
    units are not found in order. anchor: the marks' and the footnotes' anchors' base (the entry's id; a page that may
    show the entry twice gives each its own)."""
    fns = build(series, e)
    if not fns:
        return body, None
    us = claims.units(c)
    if len(us) != len(claims.units(e.get("c") or "")):
        return body, None
    marked = place(body, render, us, fns[0], anchor or e["id"])
    return (body, None) if marked is None else (marked, fns)


def _line_firsts(series):
    """{(entry id, (vol, page))}: each statute the footnotes cite from the line, at its first on the page (each half of
    the calendar, in the pages' order, as works.first_cites): printed there in full, short after (STYLE 9)."""
    if getattr(series, "_stat_firsts", None) is None:
        from . import cjk
        out = set()
        series._stat_firsts = out           # set first: build(_probe) never asks again
        for lst in series.lists.values():
            if lst.kind != "calendar":
                continue
            seen = set()
            for h, e in cjk.page_rows(series, lst):
                if "STATUTE-" not in str(e.get("c") or ""):
                    continue
                for st in build(series, e, _probe=True) or ():
                    if (h, st) not in seen:
                        seen.add((h, st))
                        out.add((e["id"], st))
    return series._stat_firsts


def place(whole, render, units, groups, eid):
    """The rendered line with its marks after each run's last unit (inside its claim's span); None where a unit's
    rendering is not found in order."""
    from html import escape
    pos, cuts = 0, {}
    for i, u in enumerate(units):
        part = render(u)
        k = whole.find(part, pos) if part else -1
        if k < 0:
            return None
        pos = k + len(part)
        cuts[i] = pos
    out, last = [], 0
    for i, n in sorted(groups):
        at = cuts[i]
        a = escape(f"{eid}-{n}", quote=True)
        out.append(whole[last:at] + f'<sup class="fm"><a href="#fn-{a}" id="fr-{a}">{n}</a></sup>')
        last = at
    return "".join(out) + whole[last:]


def notes_html(notes, eid, render):
    from html import escape
    lis = []
    for n, t in enumerate(notes, start=1):
        a = escape(f"{eid}-{n}", quote=True)
        lis.append(f'<li id="fn-{a}"><a class="fk" href="#fr-{a}">{n}</a>&ensp;{render(t)}</li>')
    return f'<ol class="fn">{"".join(lis)}</ol>'


STYLE = """<style id="fnstyle">
/* a calendar entry's footnotes (tools/bib/footnotes.py): the first line indented, the number in the indent, the
   hanging lines flush with the text (the law reviews' setting) */
sup.fm{font-family:var(--sans);font-size:.62em;line-height:0;vertical-align:.55em;font-weight:600;padding:0 .04em}
sup.fm a{color:var(--accent);text-decoration:none}
ol.fn{list-style:none;margin:.25rem 0 0;padding:0;font-size:.88rem;line-height:1.42;color:var(--note)}
ol.fn li{text-indent:1.4em;margin:.1rem 0}
ol.fn a.fk{font-family:var(--sans);font-size:.8em;font-weight:600;color:var(--accent);text-decoration:none}
ol.fn li:target{background:color-mix(in srgb,var(--accent) 12%,transparent)}
ol.e .n{font-size:.88rem;line-height:1.42}
</style>"""


# ---------------------------------------------------------------- what the note already cites; the unread records
#
# STYLE 7 continued (the owner, Nov. 21, 2026, 11:14 a.m.: "I don't want to drop the unread works. Can you check and
# fix the doubles instead?"): each record the map names (a `via x.` row, or a work's note, `via w.… 88 n.32`) that no
# reader has read is joined to the note's "To check:" as the page shows it (in a sentence of its own, before "See",
# "Names:" and "Check:", where the note has none), in the footnotes' layout and the one block's alike: 'what, where
# (cited by [[card]], 257 n.4)', through the edge from a work the note cites, at a page the note cites it at where
# one is (its `at`, the note's letter dropped: "n.4f" is the book's note 4; a note keyed by its words, the page alone);
# the record's own "cited by", "as X cites it", "repository not given", "published" go where the edge supplies the
# cited-by; a passage of a work with a card is that card at its page. Never a double (DOUBLES): a record is left out
# when the note already holds it in its own words (its numbers and most of its words; its head; the note's shorter
# form of it; its title; its parties and day; its file's or message's number), or by its place (the same card at that
# page and note, as many items as records, else the item's closest record), or as a card the note cites; when the
# note cites its printing or recording as a primary record (a link's address, a FRUS document, the Papers' or the
# Record's page, a print the note cites by its card, a tape's or conversation's number, a call's hour and a party);
# when it is a passage or print of a work the note cites; when its row is a stub (the conversion's fragments: "Int",
# "Ibid., p. 24"); and when two rows are one record. The data is not changed: the join is the page's (with_unread).

DOUBLES = ("words", "pointer", "card", "printed", "recorded", "passage", "stub", "same record")
_STOP = set("a an the of and to in on for with by at from as or is was his her their its this that re no nd vol pp p n nn "
            "ed eds memo memorandum letter telegram cable message notes note record file files box folder papers "
            "library lbj jfk lbjl jfkl ibid see also printed cited january february march april may june july "
            "august september october november december jan feb mar apr jun jul aug sep sept oct nov dec".split())
_STUB = re.compile(r"^(?:i?bid\b|id\.|pp?\.\s*\d|p\d|frus,? vol\.|vol\.\s|\W*$|"
                   r"(?:Jan|Feb|Mar|Apr|May|June|July|Aug|Sept?|Oct|Nov|Dec)[a-z]*\.? \d)", re.I)   # a date, no source
_REC_HOST = re.compile(r"millercenter\.org|prde\.upress|discoverlbj|lbjlibrary|jfklibrary\.org|nixonlibrary|"
                       r"youtube\.com|archive\.org/details|c-span", re.I)
_CLOCK = re.compile(r"\b(\d{1,2}(?::\d\d)?)\s*([ap])\.?m\b", re.I)
_PRES = {"johnson", "lbj", "kennedy", "jfk", "nixon", "president", "the", "and", "with", "to", "phone", "call",
         "telephone", "conversation", "recording", "meeting", "tape", "dictabelt", "white", "house", "draft",
         "transcript", "oval", "office", "cabinet", "room", "between"}


def _clocks(s):
    """The hours a text gives: {(hour, minutes, 'a' | 'p')}."""
    return {(int(h.split(":")[0]), (h.split(":") + ["00"])[1], ap.lower()) for h, ap in _CLOCK.findall(s or "")}


def fold(s):
    """Comparison form: accents stripped, lower case, other than letters and digits to spaces."""
    import unicodedata
    s = "".join(ch for ch in unicodedata.normalize("NFKD", str(s or "")) if not unicodedata.combining(ch))
    return " ".join(re.sub(r"[\W_]+", " ", s.lower().replace("đ", "d")).split())


_ABBR = {"nyt": "new york times", "wsj": "wall street journal", "wp": "washington post", "csm": "christian science monitor",
         "lat": "los angeles times", "ac": "atlanta constitution", "aj": "atlanta journal", "subcomm": "subcommittee",
         "comm": "committee", "oh": "oral history", "int": "interview", "intvw": "interview", "rfk": "robert kennedy",
         "hhh": "hubert humphrey", "mlk": "martin luther king"}


def _toks(s):
    out = []
    for t in fold(s).split():
        out += _ABBR.get(t, t).split()
    return [t for t in out if (t.isdigit() or len(t) > 1) and t not in _STOP]


def _has(tok, toks):
    """A word among others, or its abbreviation or full form ("subcomm" and "subcommittee")."""
    if tok in toks:
        return True
    return len(tok) >= 4 and any(len(t) >= 4 and (t.startswith(tok) or tok.startswith(t)) for t in toks)


# A record "A to B, <date>": its parties' surnames and its date's numbers
_PARTIES = re.compile(r"^([A-Z][\w'’.-]*(?: [A-Z][\w'’.-]*){0,3}) to (?:the )?([A-Z][\w'’.-]*(?: [A-Z][\w'’.-]*){0,3}),"
                      r"\s*([^,]*\d[^,]*)")


_NICK = {"rfk": "kennedy", "jfk": "kennedy", "lbj": "johnson", "hhh": "humphrey", "president": "johnson"}


def _num_in(x, toks):
    """A number among the item's: "66" is "1966" in a date."""
    return x in toks or (len(x) == 2 and 55 <= int(x) <= 79 and "19" + x in toks) or \
        (len(x) == 4 and x.startswith("19") and x[2:] in toks)


def _url(u):
    u = re.sub(r"^https?://(www\.)?", "", str(u or "").strip()).rstrip("/")
    return u


class Cited:
    """What an entry's note (and `c`) already cites, for the doubles' tests: its folded text, its links' addresses,
    the FRUS documents it names, its items' words, and its pointers (card, page, note)."""

    def __init__(self, e, titles=None, canon=None):
        from .notemerge import items, sentences
        self.titles = titles or {}
        cn = canon or (lambda x: x)
        n, c = e.get("n") or "", e.get("c") if isinstance(e.get("c"), str) else ""
        links = list(claims.LINK.finditer(n)) + list(claims.LINK.finditer(c))
        self.urls = {_url(m.group(2)) for m in links}
        self.text = fold(re.sub(r"(\d),(\d{3})\b", r"\1\2", claims.markup.strip_links(n)) + " " +
                         " ".join(m.group(2) for m in links))
        self.frus = {k for k in (witnesses.frus_key_of_url(m.group(2)) for m in links) if k}
        for m in re.finditer(r"FRUS (\d{4})[–-](\d{2}),\s*([IVXL]+)\b([^.;]*(?:;\s*docs?\.[^.;]*)*)", n):
            for d in re.findall(r"\b(\d+)\b", re.sub(r"\]\([^)]*\)", "]", m.group(4))):
                self.frus.add((m.group(1), m.group(2), witnesses._roman(m.group(3)), d))
        self.segs = []
        for s in sentences(n):
            if s.startswith(("Names: ", "See [[")):
                continue
            for it in items(s[:-1] if s.endswith(".") else s):
                its = [m.group(2) for m in claims.LINK.finditer(it)]
                bare = _CITED_BY.sub("", claims.markup.strip_links(_LABEL.sub("", it)))
                bare = re.sub(r"\[\[w\.[^\]]*\]\]", " ", bare)
                self.segs.append((set(_toks(bare)), fold(claims.markup.strip_links(it)), its, it))
        self.ptrs = []                    # (card, volume, its pages, its note numbers, the item): a work at a page and note
        for i, (_, _, _, raw) in enumerate(self.segs):
            for m in re.finditer(r"\[\[(w\.[^\]|]+)[^\]]*\]\],\s*(?:([IVXL]+), )?([^;()]*)", raw):
                for p in re.finditer(r"(\d+(?:[–-]\d+)?)\s+nn?\.\s?(\d+)([a-z])?(?:[–-](\d+|[a-z]\b))?", m.group(3)):
                    lo = int(p.group(2))
                    hi = int(p.group(4)) if p.group(4) and p.group(4).isdigit() else lo
                    many = (ord(p.group(4)) - ord(p.group(3)) + 1) if p.group(3) and p.group(4) and p.group(4).isalpha() \
                        else 1                   # "n.2a–e": five records
                    self.ptrs.append((cn(m.group(1)), m.group(2) or "", claims._pages(p.group(1)) or set(),
                                      set(range(lo, hi + 1)), i, max(1, many)))
        self.cards = [cn(m.group(1)) for m in re.finditer(r"\[\[(w\.[^\]|]+)", n)]
        tc = n.find("To check:")
        self.read_cards = [cn(m.group(1)) for m in re.finditer(r"\[\[(w\.[^\]|]+)", n[:tc] if tc >= 0 else n)]
        self.pages = collections.defaultdict(set)     # card -> the pages the note cites it at
        for m in re.finditer(r"\[\[(w\.[^\]|]+)[^\]]*\]\],\s*(?:([IVXL]+), )?([^;()\[\]]*)", n):
            for pg in claims._pages(re.sub(r"\bnn?\.\s*\d+[a-z]?(?:[–-]\d+)?", "", m.group(3))) or ():
                self.pages[cn(m.group(1))].add((m.group(2) or "", pg))

    def words(self, what, where=""):
        """Whether one item of the note gives the record in its own words: every number of it (a year aside, "66"
        for "1966" too; its parentheticals aside) and most of its words (three in five, two at least; or four in five,
        four at least, numbers or not; or five and two in five); its head (its first eight words: author and title)
        four in five, four at least; or the item is a shorter form of it, record and `where` (four in five of the
        item's words in the record's, two numbers shared or the record's in the item: "Coffin, *Once to Every Man*
        (1977), 238–44" for "Coffin, William Sloane, Jr, Once to Every Man: A Memoir (1977)")."""
        plain = re.sub(r"\s*\((?:[^()]|\([^()]*\))*\)", " ", what or "")
        t = _toks(plain) or _toks(what)
        nums = [x for x in t if x.isdigit() and not re.fullmatch(r"(?:19|20)\d\d", x)]
        wds = [x for x in t if not x.isdigit()]
        if not wds:
            return False
        own = set(t) | set(_toks(what))
        tset = own | set(_toks(where))
        days = re.findall(r"\b(?:Jan|Feb|Mar|Apr|May|June|July|Aug|Sept?|Oct|Nov|Dec)[a-z]*\.? (\d{1,2})\b", plain)
        for title in re.findall(r"[\"“*]([^\"“”*]{10,})[\"”*]", what or ""):   # a title, quoted or italic, main part
            title = fold(title.split(":")[0])
            if len(title.split()) >= 2 and f" {title} " in f" {self.text} " and \
                    all(_num_in(x, set(self.text.split())) for x in days):
                return True
        dtg = set(re.findall(r"\b(\d{6}z)\b", fold(what)))                # a message's date-time group
        pm = _PARTIES.match(plain.strip())                            # "Manatos to O'Brien, May 6, 1964"
        if pm:
            a, b = fold(pm.group(1)).split()[-1:], fold(pm.group(2)).split()[-1:]
            a, b = [_NICK.get(x, x) for x in a], [_NICK.get(x, x) for x in b]
            day = [x for x in _toks(pm.group(3)) if x.isdigit() and not re.fullmatch(r"(?:19|20)\d\d", x)]
            for toks, _, _, _ in self.segs:
                if a and b and len(a[0]) > 2 and len(b[0]) > 2 and _has(a[0], toks) and _has(b[0], toks) and day \
                        and all(_num_in(x, toks) for x in day):
                    return True
        head = wds[:8]
        fw = f" {fold(what)} {fold(where)} "
        big = {x for x in tset if x.isdigit() and len(x) >= 5}       # a file's or a document's number: "160122"
        for toks, _, _, raw in self.segs:
            if big & toks and sum(1 for x in nums if _num_in(x, toks)) >= 2:
                return True
            if dtg & toks:
                return True
            if len(wds) >= 2 and _has(wds[0], toks) and _has(wds[1], toks) and days and \
                    all(_num_in(x, toks) for x in days) and sum(1 for x in wds if _has(x, toks)) >= 4:
                return True                 # its author and its day ("Cheng Guanghua ..., Nov. 29, 1960")
            sw0 = {x for x in toks if not x.isdigit()}
            if sw0 and sw0 == set(wds) and all(_num_in(x, toks) for x in nums):
                return True                 # the same words ("Crisis, Aug.–Sept. 1962")
            for it in re.findall(r"\*([^*]{8,})\*", raw):    # the item's italic title, the record's words hold it
                ti = fold(it.split(":")[0])
                if len(ti.split()) >= 2 and f" {ti} " in fw and all(_num_in(x, toks) for x in days):
                    return True
            hit = sum(1 for x in wds if _has(x, toks))
            if hit >= 4 and hit >= 0.8 * len(wds) or hit >= 5 and hit >= 0.4 * len(wds):
                return True
            hh = sum(1 for x in head if _has(x, toks))
            if len(head) >= 5 and (hh >= 4 and hh >= 0.8 * len(head) or hh >= 5):
                return True
            sw = [x for x in toks if not x.isdigit()]
            sn = [x for x in toks if x.isdigit() and not re.fullmatch(r"(?:19|20)\d\d", x)]
            inn = all(_num_in(x, toks) for x in nums)
            back = sum(1 for x in sw if _has(x, tset))
            if sw and back >= 0.8 * len(sw) and (back >= 2 or back == 1 and len(nums) >= 1) and \
                    (inn or sum(1 for x in sn if _num_in(x, tset)) >= 2 or
                     (not sn and sum(1 for x in sw if _has(x, own)) >= max(3, 0.8 * len(sw))) or
                     (not sn and back >= 3 and back == len(sw) and any(_has(x, own) for x in sw)) or
                     (back >= 4 and back == len(sw) and any(_num_in(x, tset) for x in sn))):
                return True
            if not inn:
                continue
            if hit >= 2 and hit >= 0.6 * len(wds) or (len(wds) == 1 and hit == 1 and nums):
                return True
        return False

    def printed(self, w):
        """Whether the note cites the record's printing or copy: a link's address, a FRUS document, the Papers' or
        the Record's page, a numbered document of an archive's site."""
        for cp in [str(x) for x in (w.get("copies") or [])] + [str(w.get("where") or ""), str(w.get("what") or "")]:
            for u in re.findall(r"https?://\S+", cp):
                if _url(u.rstrip(").,;")) in self.urls:
                    return True
            k = witnesses.frus_key_of_copy(cp)
            if k and k in self.frus:
                return True
            for m in re.finditer(r"\b(\d{4}(?:[–-]\d{2})? Pub\. Papers \d+|\d{2,3} Cong\. Rec\. \d[\d,]*\d)",
                                 re.sub(r"(\d),(\d{3})\b", r"\1\2", cp)):
                if fold(m.group(1)) in self.text:
                    return True
            m = re.search(r"document (\d{5,})", cp)
            if m and any(re.search(rf"/document/{m.group(1)}\b", u) for u in self.urls):
                return True
        pm = _PARTIES.match(re.sub(r"\s*\([^()]*\)", "", str(w.get("what") or "")).strip())
        if pm and w.get("date") and self.frus:     # a FRUS document the note links, of its day, its parties in the title
            a, b = fold(pm.group(1)).split()[-1:], fold(pm.group(2)).split()[-1:]
            for k in self.frus:
                d = _frus_docs().get(k)
                if d and d[0] == str(w["date"]) and a and b and all(f" {x} " in f" {d[1]} " for x in a + b):
                    return True
        for cp in [str(w.get("what") or ""), str(w.get("where") or "")]:   # "Congressional Record, ..., vol. 110, ..., 8192"
            m = re.search(r"Congressional Record\b[^;]*?\bvol\. (\d+)\b[^;]*?\b(\d{3,5})\b", cp)
            if m and f"{m.group(1)} cong rec {m.group(2)}" in self.text:
                return True
        for cp in w.get("copies") or []:     # its print a work the note cites ("Robert Kennedy in His Own Words")
            f = fold(cp)
            if any(t and len(t.split()) >= 2 and f" {t} " in f" {f} " for t in self.titles.values()):
                return True
        return False

    def recorded(self, w):
        """Whether the note links the recording the record is: its tape or conversation number, or its hour and a
        party, in an item that links a recording."""
        what = " ".join(str(x) for x in [w.get("what"), w.get("where")] + list(w.get("copies") or []))
        if not (w.get("kind") in ("recording", "transcript") or re.search(r"\b(call|conversation|tape|recording|"
                                                                         r"dictabelt|telephone)\b", what, re.I)):
            return False
        cits = {x for x in re.findall(r"(?:Citation\s*#?|#)\s*(\d{3,})", what, re.I)}
        tapes = set()                       # a tape's or dictabelt's number, its parts as a pattern ("40.3", "114/A49")
        for x in re.findall(r"(?:Dictabelt|Tape|Conversation|PNO)\s*(?:No\.\s*)?((?:WH)?\d[\w./_-]*\w)", what, re.I):
            parts = re.findall(r"[a-z]+|\d+", x.lower())
            if len("".join(parts)) >= 3 and not re.fullmatch(r"(?:19|20)\d\d", "".join(parts)):
                tapes.add(r"(?<![a-z0-9])" + r"[\s._/-]?".join(parts) + r"(?![0-9])")
        clock = _clocks(str(w.get("what") or ""))
        party = {x for x in _toks(str(w.get("what") or "")) if not x.isdigit() and x not in _PRES}
        for toks, ftext, its, raw in self.segs:
            flat = re.sub(r"[^a-z0-9]", "", ftext + " ".join(its).lower())
            if cits:                        # a conversation's own number ("Citation #5008", "WH6408-27-5008")
                if any(re.search(rf"(?<!\d){c}(?!\d)", ftext + " " + " ".join(its)) for c in cits):
                    return True
            elif tapes and any(re.search(x, ftext + " " + fold(" ".join(its))) for x in tapes):
                return True                 # its tape or dictabelt ("JFK Dictabelt 28A.3", "Meeting Tape 114/A49")
            if any(_REC_HOST.search(u) for u in its) and clock and clock & _clocks(claims.markup.strip_links(raw)) \
                    and party & toks:
                return True                 # its hour and a party, in an item linking a recording
        return False

    def pointed(self, recs):
        """The records (of [(id, card, at, what)]) the note names by their place, the same card at that page and note
        (the note's letter aside): where the note's items there are as many as the records, all; else each item
        takes the record whose words it shares most."""
        groups = collections.defaultdict(list)
        for x, card, at, what in recs:
            m = witnesses.AT.match(at or "")
            num = m and re.match(r"(\d+)", m.group("note"))
            if num:
                vol, pg = _vol(m.group("page"))
                groups[(card, vol or "", (claims._pages(pg) or {None}).pop(), int(num.group(1)))].append((x, what))
        out = set()
        for (card, vol, pg, num), xs in groups.items():
            hit = {i: many for c, v, pages, nums, i, many in self.ptrs
                   if c == card and v == vol and pg in pages and num in nums}
            items = sorted(hit)
            if sum(hit.values()) >= len(xs):
                out |= {x for x, _ in xs}
                continue
            pool = list(xs)
            for i in items:
                toks = self.segs[i][0]
                best = max(pool, key=lambda xw: sum(1 for t in _toks(xw[1]) if not t.isdigit() and _has(t, toks)),
                           default=None)
                if best and sum(1 for t in _toks(best[1]) if not t.isdigit() and _has(t, toks)) >= 1:
                    out.add(best[0])
                    pool.remove(best)
        return out

    def at_page(self, card, at):
        """Whether the note cites the card at the edge's page."""
        m = witnesses.AT.match(at or "")
        if not m:
            return False
        vol, pg = _vol(m.group("page"))
        return any((vol or "", x) in self.pages.get(card, ()) for x in claims._pages(pg) or ())


_FRUS = {}


def _frus_docs():
    """{FRUS key: (date, its title and author folded)}: the daybook's FRUS documents (daybook/)."""
    if "idx" not in _FRUS:
        from . import daybook
        idx = {}
        try:
            for d in daybook.load()[0]:
                k = witnesses.frus_key_of_url(d.get("url") or "") if d.get("src") == "frus" else None
                if k:
                    idx[k] = (str(d.get("date") or ""), fold(f"{d.get('title') or ''} {d.get('author') or ''}"))
        except Exception:                   # the daybook not there (a fixture without it): no such test
            pass
        _FRUS["idx"] = idx
    return _FRUS["idx"]


_REV = {}


def _edges_to(series, wid):
    """The works' edges to a witness: [(card, at)], an index built once per load."""
    rows, edges, _ = _load(series)
    if _REV.get("of") is not edges:
        idx = collections.defaultdict(list)
        for card, es in edges.items():
            for ed in es or []:
                if isinstance(ed, dict) and ed.get("of"):
                    idx[ed["of"]].append((card, str(ed.get("at") or "")))
        _REV.update({"of": edges, "idx": idx})
    return _REV["idx"].get(wid, [])


_LABEL = re.compile(r"^(?:To check|Check|Names|Made public|See|Also|Reply|The order|Bibliography):?\s+")
_CITED_BY = re.compile(r"\s*\((?:(?:cited|quoted|given|described|named|printed) (?:by|at|in)|as cited)\b[^()]*(?:\([^()]*\)[^()]*)*\)")


# A `where` clause on the record's provenance, which the note's own cited-by gives instead
_PROV = re.compile(r"^(?:cited by\b|cited in\b|named (?:by|in)\b|as (?:cited|quoted)\b|as [^;]{0,60}\bcites?\b|"
                   r"quoted (?:by|in)\b|printed in the work cited|repository not given|not given\b|year not given|"
                   r"no note\b|given with the book|the newspaper or magazine named|(?:the )?newspaper$|published$|"
                   r"original not seen|not deposited$|listed in\b)", re.I)
_REG_WORDS = re.compile(r"^(?:published|printed|(?:the )?newspaper|original not seen|not deposited|"
                        r"repository not given\b.*|year not given|no note|not given)$", re.I)   # the registry's words
_PROV_PAREN = re.compile(r"\s*\((?:as cited|[^()]*\bcites?\b[^()]*|[^()]*\bnot given\b[^()]*|"
                         r"[A-Z][\w'’-]+, \d[^()]*)\)")


_PROV_TAIL = re.compile(r",\s*(?:as [^,;]{0,60}\bcites?(?: (?:it|them))?|as cited|cited by [^;]*|named in [^;]*)\s*$", re.I)


# The record's own words on where it was met ("(described by Sorensen, Kennedy, 238)", ", as Westmoreland quotes it"),
# which the cited-by gives instead
_PROV_WHAT = re.compile(r"\s*\((?:described|given|quoted|named|cited|printed|reported) (?:by|in|at)\b[^()]*\)|"
                        r",\s*as [A-Z][\w'’-]+ (?:quotes|gives|cites|prints|reports) it\b")


def _where(w, edge):
    wh = "; ".join(x for x in witnesses._split_top(witnesses.cite_where(w.get("where"))) if not _REG_WORDS.match(x))
    if edge:
        keep = []
        for seg in witnesses._split_top(wh):
            if _PROV.match(seg):
                continue
            seg = _PROV_PAREN.sub("", _PROV_TAIL.sub("", seg)).strip()
            if seg:
                keep.append(seg)
        wh = "; ".join(keep)
    keep = []
    for seg in witnesses._split_top(wh):            # "printed, Hanoi, 1995" where the record already says so
        body = re.sub(r"^(?:printed|published)(?:,| in)?\s*", "", seg)
        if seg in ("published", "printed") or (body != seg and fold(body) and fold(body) in fold(w.get("what"))):
            continue
        keep.append(seg)
    wh = "; ".join(keep)
    if wh and fold(wh) in fold(w.get("what")):
        return ""
    return wh


def _at(at):
    """An edge's anchor as the note prints it: the note's letter dropped ('257 n.4f' -> '257 n.4'), a note keyed by its
    words given by its page alone."""
    m = witnesses.AT.match(at or "")
    if not m:
        return at
    num = re.match(r"^(\d+)[a-z]?$", m.group("note"))
    if num:
        return f"{m.group('page')} n.{num.group(1)}"
    num = re.match(r"^(\d+)[–-](\d+)$", m.group("note"))
    return f"{m.group('page')} nn.{m.group('note')}" if num else m.group("page")


_UNREAD = {}


def unread(series, e):
    """The records the entry's rows name that no reader has read: (added, left): added, [(witness id, the To check
    item)], in the map's order; left, [(witness id, the class of double, DOUBLES)]. Once per entry and note a run
    (first_cites asks, then the page)."""
    _register(series)
    key = (e.get("id"), e.get("n"), repr(e.get("src")))
    if _UNREAD.get("of") is not _REG.get("load"):
        _UNREAD.clear()
        _UNREAD["of"] = _REG.get("load")
    if key not in _UNREAD:
        _UNREAD[key] = _unread(series, e)
    return _UNREAD[key]


def _unread(series, e):
    src = e.get("src")
    if not isinstance(src, dict) or not e.get("n"):
        return [], []
    rows = _load(series)[0]
    ids = []
    reg = _register(series)
    for r in src.get("rows") or []:
        p = claims.parse_row(r)
        if p and p[0] == "witness" and p[1] not in ids:
            ids.append(p[1])
        elif p and p[0] == "via":           # a work's note: the record its edge leads to
            rec = reg.get((p[1], str(p[2]), str(p[3])))
            if rec and rec.get("id") and rec["id"] not in ids:
                ids.append(rec["id"])
    ids = [x for x in ids if x in rows and not rows[x].get("read")]
    if not ids:
        return [], []
    canon = (lambda c: series.works.alias.get(c, c))
    cited = Cited(e, canon=canon)
    cited.titles = {c: fold(str((series.works.fields(c) or {}).get("title") or "").split(":")[0])
                    for c in dict.fromkeys(cited.cards)}
    recs = []
    for x in ids:
        es = [(canon(c), a) for c, a in _edges_to(series, x) if canon(c) in cited.cards]
        es.sort(key=lambda ca: (not cited.at_page(*ca), ca[0] not in cited.read_cards, cited.cards.index(ca[0])))
        if es:
            recs.append((x, es[0][0], es[0][1], str(rows[x].get("what") or "")))
    pointed = cited.pointed(recs)
    added, left, seen = [], [], []
    for x in ids:
        w = rows[x]
        what = str(w.get("what") or "").strip()
        es = [(canon(c), a) for c, a in _edges_to(series, x) if canon(c) in cited.cards]
        es.sort(key=lambda ca: (not cited.at_page(*ca), ca[0] not in cited.read_cards, cited.cards.index(ca[0])))
        edge = es[0] if es else None
        part = w.get("part_of")
        wh0 = str(w.get("where") or "")
        cm = re.search(r"(?<!as )(?<!by )\b(w\.[a-z0-9][a-z0-9-]*[a-z0-9])(?![\w-]* cites)(?:,\s*([0-9ivxlc][^,;()]*))?",
                       re.sub(r"\s*\((?:[^()]|\([^()]*\))*\)", " ", what))    # the record is a work with a card
        cid = cm and series.works.alias.get(cm.group(1), cm.group(1))
        if cid and (series.works.get(cid) is None or any(cid == c for c, _ in _edges_to(series, x))):
            cid = None
        if w.get("base"):                   # a work's whole source base, not a record of a claim: never joined
            left.append((x, "base"))          # (the owner, Nov. 21, 2026: "Drop the Rusk taped interviews.")
        elif len(what) < 12 or _STUB.match(what):
            left.append((x, "stub"))
        elif (cid and cid in cited.cards) or _a_card(cited, what):
            left.append((x, "card"))
        elif _titled(series, cited, what) or _printed_in(series, cited, what + " ; " + wh0):
            left.append((x, "passage"))
        elif part and (part in cited.cards or (rows.get(part) or {}).get("part_of") in cited.cards):
            left.append((x, "passage"))
        elif edge and re.search(r"printed in the work cited", str(w.get("where") or ""), re.I) and \
                edge[0] in cited.read_cards:
            left.append((x, "passage"))
        elif cited.printed(w):
            left.append((x, "printed"))
        elif cited.recorded(w):
            left.append((x, "recorded"))
        elif x in pointed:
            left.append((x, "pointer"))
        elif cited.words(what, str(w.get("where") or "")) or any(cited.words(a) for a in w.get("also_as") or []):
            left.append((x, "words"))
        elif any(_same(w, rows[y]) for y in seen):
            left.append((x, "same record"))
        elif part and str(part).startswith("w.") and series.works.get(part) is not None:
            seen.append(x)                  # a passage of a work with a card: the card, at its page
            text = f"[[{part}]]" + (f", {w.get('pin')}" if w.get("pin") else "")
            if edge:
                text += f" (cited by [[{edge[0]}]], {_at(edge[1])})"
            added.append((x, text))
        elif cid:                           # a work with a card, registered as a record: its card
            seen.append(x)
            text = f"[[{cid}]]" + (f", {cm.group(2).strip()}" if cm.group(2) else "")
            if edge:
                text += f" (cited by [[{edge[0]}]], {_at(edge[1])})"
            added.append((x, text))
        else:
            seen.append(x)
            wh = _where(w, edge)
            if edge:
                what = _PROV_WHAT.sub("", what).strip()
                what = re.sub(r"\s*\(([^()]*)\)", lambda m: "" if any(
                    t and len(t.split()) >= 2 and f" {t} " in f" {fold(m.group(1))} " for t in cited.titles.values())
                    else m.group(0), what).strip()
            what = what.rstrip(",; ")
            if what.endswith(".") and not re.search(r"(?:\b[ap]\.m|\b[A-Z]|\b(?:Jr|Sr|Inc|Co|al|ed|eds|no|vol))\.$", what):
                what = what[:-1]
            wh = re.sub(r"\s*\(([^()]*)\)", lambda m: "" if any(
                t and len(t.split()) >= 2 and f" {t} " in f" {fold(m.group(1))} " for t in cited.titles.values())
                else m.group(0), wh).strip() if edge else wh
            text = what + (f", {wh}" if wh else "")
            if edge:
                text += f" (cited by [[{edge[0]}]], {_at(edge[1])})"
            added.append((x, text))
    return added, left


def _a_card(cited, what):
    """Whether the record is a work the note cites by its card: the card's main title in its words, three words or
    more, or quoted or in italics ("Cheng Hua, *Zhou Enlai he tade Mishumen* (1992)" for [[w.hua-zhou-enlai-he-tade]])."""
    f = f" {fold(re.sub(r'[(（][^()（）]*[)）]', ' ', what or ''))} "      # its own words, not a parenthetical's
    marked = " ".join(fold(x) for x in re.findall(r"\*([^*]+)\*|[\"“]([^\"”]+)[\"”]", what or "") for x in x if x)
    for t in cited.titles.values():
        if t and (len(t.split()) >= 3 and f" {t} " in f or len(t.split()) >= 2 and f" {t} " in f" {marked} "):
            return True
        head = " ".join(t.split()[:4]) if t else ""      # a long title's head: its translation may be the card's
        if len(t.split()) >= 5 and sum(1 for x in head.split() if x not in _STOP) >= 3 and f" {head} " in f:
            return True
    return False


def _printed_in(series, cited, text):
    """Whether the record says it is printed in a work the note cites as read ("printed in Berman, app. B, 220–29")."""
    for m in re.finditer(r"\bprinted in ([A-Z][\w'’-]+)", text):
        sur = fold(m.group(1))
        for c in dict.fromkeys(cited.read_cards):
            au = (series.works.fields(c) or {}).get("author") or []
            if any(fold(str(a)).split()[-1:] == [sur] for a in (au if isinstance(au, list) else [au])):
                return True
    return False


def _titled(series, cited, text):
    """Whether the record is a passage of a work the note cites as read: its main title (two words or more) and a page
    in the record's own words, outside their parentheticals and its cited-by ("McPherson's account, A Political
    Education, 410-11")."""
    plain = re.sub(r"\s*\((?:[^()]|\([^()]*\))*\)", " ", _PROV_WHAT.sub("", text))
    plain = fold(re.split(r"\b(?:cited|quoted|named|given) (?:by|in)\b", plain)[0])
    for c in dict.fromkeys(cited.read_cards):
        t = fold(str((series.works.fields(c) or {}).get("title") or "").split(":")[0])
        if len(t.split()) >= 2 and re.search(rf"(?:^| ){re.escape(t)} \d", plain):
            return True
    return False


def _same(a, b):
    """Two rows that are one record (the registry's duplicates): the same words, numbers and all."""
    ta, tb = set(_toks(a.get("what"))), set(_toks(b.get("what")))
    return bool(ta) and (ta <= tb or tb <= ta) and str(a.get("date") or "") == str(b.get("date") or "")


def with_unread(series, e, text):
    """The note (or the footnotes' rest of it) with the entry's unread records joined to its "To check:" (STYLE 7):
    at the end of that sentence, or in a sentence of their own before "See", "Names:" and "Check:" (else last)."""
    from .notemerge import sentences
    added, _ = unread(series, e)
    if not added or not text:
        return text
    more = "; ".join(t for _, t in added)
    ss = sentences(text)
    for i, s in enumerate(ss):
        if s.startswith("To check: "):
            ss[i] = (s[:-1] if s.endswith(".") else s) + "; " + more + "."
            return " ".join(ss)
    k = next((i for i, s in enumerate(ss) if s.startswith(("See [[", "Names: ", "Check: "))), len(ss))
    return " ".join(ss[:k] + [f"To check: {more}."] + ss[k:])
