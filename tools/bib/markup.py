"""The inline markup used in entry text, and its conversion to HTML.

    *Title*              italics (titles of works, case names, foreign words)
    [text](https://...)  an outside link
    [[id]]               a link to another entry, shown as that entry's label
                         (a calendar entry's date, e.g. "Apr. 15-19")
    [[id|text]]          the same, shown as "text"

Nothing else is special. Write "&", quotes, and dashes as themselves.
"""
import html
import re

REF_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
LINK_RE = re.compile(r"\[([^\[\]]+)\]\((https?://(?:[^()\s]|\([^()\s]*\))+)\)")  # urls may hold (...)
ITAL_RE = re.compile(r"\*([^*]+)\*")


def refs(text):
    """Ids referenced by [[...]] in text."""
    return [m.group(1) for m in REF_RE.finditer(text or "")]


# A card of the works catalogue linked from the text ([[w.beschloss-crisis-years]]): shown by its short form, linked to
# its entry in the A–Z bibliography (tools/bib/works.py, SHORT FORM). store.Series sets WORKS: card id -> short form.
WORKS = None
WORKS_FULL = None          # card id -> its full citation (markup), for a first citation (works.py, FIRST CITE)
WORKS_PAGE = "works.html"
WORKS_ID = lambda cid: cid     # an alias -> the card's own id (set by store.Series)
FULL_MARKS = ("\x01full", "full")


def work_label(eid):
    return WORKS(eid) if WORKS and eid.startswith("w.") else None


def to_html(text, resolve=None):
    """resolve(id, shown_text) -> html for an internal reference, or None if unknown."""
    if text is None:
        return ""
    held = []

    def hold(s):
        held.append(s)
        return f"\x00{len(held) - 1}\x00"

    def ref(m):
        eid, shown = m.group(1).strip(), m.group(2)
        sf = work_label(eid)
        if sf is not None:
            eid = WORKS_ID(eid)
        if sf is not None and shown in FULL_MARKS and WORKS_FULL:
            full = WORKS_FULL(eid)           # the full citation, its author and title the link
            m2 = re.match(r"^[^*\[]*\*[^*]+\*", full)
            if not m2:
                return hold(to_html(full))
            return hold(f'<a class="x xw xf" href="{WORKS_PAGE}#{html.escape(eid)}">{_inline(m2.group(0))}</a>'
                        + to_html(full[m2.end():]))
        if sf is not None:
            return hold(f'<a class="x xw" href="{WORKS_PAGE}#{html.escape(eid)}">{_inline(shown or sf)}</a>')
        out = resolve(eid, shown) if resolve else None
        if out is None:
            out = html.escape(shown or eid, quote=False)
        return hold(out)

    t = REF_RE.sub(ref, text)
    t = LINK_RE.sub(lambda m: hold(f'<a href="{html.escape(m.group(2))}">{_inline(m.group(1))}</a>'), t)
    t = _inline(t)
    return re.sub(r"\x00(\d+)\x00", lambda m: held[int(m.group(1))], t)


def _inline(t):
    t = html.escape(t, quote=False)
    return ITAL_RE.sub(r"<i>\1</i>", t)


def plain(text, label=None):
    """Text with the markup removed. label(id) gives the shown text of [[id]]."""
    if text is None:
        return ""
    t = REF_RE.sub(lambda m: (m.group(2) if m.group(2) not in FULL_MARKS else None) or work_label(m.group(1).strip())
                   or (label(m.group(1)) if label else m.group(1)), text)
    t = LINK_RE.sub(r"\1", t)
    return ITAL_RE.sub(r"\1", t)


def italics(text):
    """The italicized spans in text (titles, mostly)."""
    return ITAL_RE.findall(LINK_RE.sub(r"\1", text or ""))


def lower_from(t):
    """FRUS headings in sentence case for 'from': 'Memorandum From Rusk to Kennedy' -> 'Memorandum from Rusk to Kennedy'."""
    import re
    return re.sub(r"(?<=\S )From\b", "from", t)
