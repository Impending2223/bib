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
    t = REF_RE.sub(lambda m: m.group(2) or (label(m.group(1)) if label else m.group(1)), text)
    t = LINK_RE.sub(r"\1", t)
    return ITAL_RE.sub(r"\1", t)


def italics(text):
    """The italicized spans in text (titles, mostly)."""
    return ITAL_RE.findall(LINK_RE.sub(r"\1", text or ""))
