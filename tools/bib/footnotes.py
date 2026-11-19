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
    (citing the record)", or "88 n.32 (citing ...)" alone. Sources the map has not yet given units (`?`) and items of the
    note no row names close the last footnote.
 4. *id*. (the owner: "italicize the 'id' but leave the full stop in plain roman ... A departure from the Bluebook"): a
    citation of the work cited immediately before, in the same footnote or as the previous footnote's only authority
    (Bluebook 4.1), is "*id*." when the pinpoint is the same, "*id*. at 89 n.35" when it differs within the volume,
    "*id*., V, 12" when the volume differs; capitalized at a footnote's head; a link or an unlinked item cited again,
    word for word, "*id*.".
 5. The first citation of a work on the page is printed in full (works.py, FIRST CITE): the footnotes are run through it
    in their order, so the full form falls in the first footnote that cites the work; the characters after romanized
    Chinese (cjk.py) the same; the line's own characters are dropped and given after the names or in a closing
    "Characters:" sentence (cjk.py, STYLE 3), and its units rendered the same way, so the marks still land.
 6. The marks sit inside the last claim's span (vispage.py), so a hidden claim takes its mark with it.
"""
import re

from . import claims

SEP = "\n\n"          # between footnotes while the note's passes run over them as one text
MARK = "{}"


def _vol(pin):
    m = re.match(r"^([IVXLC]+),\s*(.+)$", pin or "")
    return (m.group(1), m.group(2)) if m else (None, pin or "")


_REG = {}


def _register(series):
    """The witness register, once per series (a build asks for it per entry; witnesses.load stats every file)."""
    if _REG.get("series") is not series:
        _REG["series"], _REG["reg"] = series, claims.register(series)
    return _REG["reg"]


def _cites(series, e):
    """Per unit, its sources as dicts (kind, key, pin, paren, text); the `?` rows and unrowed items: the tail."""
    us = claims.units(e.get("c") or "")
    rows = claims.resolve(e)
    reg = _register(series)
    srcs, _ = claims.note_parts(e.get("n"))
    used = set()

    def card(key, pin, item, row_pin):
        k = claims.item_key(item) if item else None
        if k and k[0] == "card" and k[1] == key and (not row_pin or k[2] == row_pin):
            used.add(item)
            return dict(kind="card", key=key, pin=k[2] or "", paren=k[3] or "", text=item)
        if item:
            used.add(item)
        return dict(kind="card", key=key, pin=row_pin or "", paren="", text=f"[[{key}]]" + (f", {row_pin}" if row_pin else ""))

    def via(key, pin, note, joined):
        rec = reg.get((key, str(pin), str(note)))
        what = f"{rec.get('record')}, {rec.get('where')}" if rec else "a record"
        p = f"{pin} & n.{note}" if joined else f"{pin} n.{note}"
        return dict(kind="card", key=key, pin=p, paren=f"(citing {what})", text=f"[[{key}]], {p} (citing {what})")

    per = []
    for i, _ in enumerate(us):
        L = claims.LETTERS[i]
        mine = [(k, key, pin, note, item) for r, k, key, pin, note, u, item in rows
                if k and u not in (None, "?") and L in u]
        vias = {(key, pin): note for k, key, pin, note, _ in mine if k == "via"}
        out = []
        for k, key, pin, note, item in mine:
            if k == "card" and (key, pin) in vias:
                if item:
                    used.add(item)
                out.append(via(key, pin, vias[(key, pin)], True))
            elif k == "via":
                if any(k2 == "card" and (key2, pin2) == (key, pin) for k2, key2, pin2, _, _ in mine):
                    continue
                out.append(via(key, pin, note, False))
            elif k == "card":
                out.append(card(key, pin, item, pin))
            elif k == "witness":
                text = claims._render_row(series, e, "witness", key, pin, note, item, reg)
                out.append(dict(kind="text", key=text, pin="", paren="", text=text))
            else:
                if item:
                    used.add(item)
                text = item or key
                out.append(dict(kind=k, key=text, pin="", paren="", text=text))
        per.append(out)
    tail = []
    for r, k, key, pin, note, u, item in rows:
        if u == "?" and item and item not in used:
            used.add(item)
            tail.append(dict(kind="text", key=item, pin="", paren="", text=item))
    for it in srcs:                       # an item of the note no row names: kept, at the end
        if it not in used and not any(it == c["text"] for p in per for c in p):
            used.add(it)
            tail.append(dict(kind="text", key=it, pin="", paren="", text=it))
    return us, per, tail


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


def build(series, e):
    """None where the entry is shown as before (STYLE 2); else (groups, notes, rest): groups, the index of each run's
    last unit and its footnote's number; notes, each footnote's markup; rest, the note's other sentences."""
    c = e.get("c")
    if not isinstance(c, str) or not c or not e.get("n"):
        return None
    src = e.get("src")
    if isinstance(src, dict) and src.get("c") and src.get("c") != claims.chash(c):
        return None                       # a stale map: its letters may not fit (claims.py, STYLE 4)
    us, per, tail = _cites(series, e)
    runs = []
    for i in range(len(us)):
        key = [(x["kind"], x["key"], x["pin"]) for x in per[i]]
        if runs and runs[-1][0] == key:
            runs[-1][1] = i
        else:
            runs.append([key, i, per[i]])
    if tail:
        if runs and runs[-1][2]:
            runs[-1][2] = runs[-1][2] + tail
        elif runs:
            runs[-1][2] = tail
    groups, notes, prev_note = [], [], None
    for key, last, cites in runs:
        if not cites:
            continue
        parts, prev = [], None
        single_prev = prev_note if prev_note and len({x["key"] for x in prev_note}) == 1 else None
        for j, x in enumerate(cites):
            p = prev if j else (single_prev[-1] if single_prev else None)
            parts.append(_id(x, p, j == 0))
            prev = x
        notes.append("; ".join(parts) + ("" if parts[-1].endswith(".") else "."))
        groups.append((last, len(notes)))
        prev_note = cites
    if len(notes) <= 1:
        return None
    rest = " ".join(claims.note_parts(e.get("n"))[1])
    return groups, notes, rest


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
