"""Typographer's quotation marks, made at the build: the YAML keeps the keyboard's ' and ", and every page is written
with ‘ ’ “ ” in its text.

STYLE
 1. Only text is touched: not tags or their attributes (URLs, ids, titles on hover keep their characters; a '>' inside a
    quoted attribute value does not end the tag), and not
    the contents of <script>, <style>, <pre>, <code> or <textarea>. Entities that stand for a quotation mark in text
    (&quot; &#34; &#39; &#x27; &apos;) are curled as the characters are.
 2. A double quotation mark opens at the start of the text or after a space, an opening bracket, a dash, or an
    opening mark; it closes elsewhere. A single mark is an apostrophe (’) unless it opens a quotation by the same rule
    and is followed by a letter; an elision written with an apostrophe first stays ’ ('60s, '64, 'n', 'em, 'tis,
    'twas, 'til, 'cause).
 3. Tags are transparent: the character before a mark may lie in the text before an <i> or <a> (“<i>Title</i>”).
    But a double mark right after a tag and followed by a letter or a digit opens: a link's text that begins with a
    title in quotation marks (<a>“Robert Kennedy Assures Vietnam,”</a>), a paragraph that begins with a quotation, a
    calendar line after its rubric ("…, Dec. 17</span>“After Two Years”"). A single mark so placed opens only where the
    text before the tag did not end in a letter or a digit (it<a>’s</a>; <i>Times</i>’s).
 4. Marks already curled in the text are left as they are. An inch or a minute is written as a prime (″ ′) in the
    sources, not as a quotation mark.
"""
import re

SKIP = ("script", "style", "pre", "code", "textarea")
OPENERS = set(" \t\n\r ([{—–-/“‘")
ELISIONS = re.compile(r"(?:\d\d(?:s|\b)|n'|em\b|tis\b|twas\b|til\b|cause\b)", re.I)
ENT = re.compile(r"&(?:quot|#34|#x22|#39|#x27|apos);", re.I)
# a tag runs to the first '>' outside a quoted attribute value (onclick="...forEach(d=>d.open=true)")
TAG = r"<(/?)([a-zA-Z][a-zA-Z0-9]*)\b(?:[^>\"']|\"[^\"]*\"|'[^']*')*>"
TOKEN = re.compile(r"<!--.*?-->|" + TAG + r"|[^<]+|<", re.S)
TAGS = re.compile(r"<!--.*?-->|" + TAG, re.S)


def _curl(text, prev, fresh=False):
    """Curl the marks in one run of text; prev is the character before it (across tags); fresh where the run begins
    an element's text, right after an opening tag (STYLE 3). Returns (text, last)."""
    text = ENT.sub(lambda m: '"' if m.group(0).lower() in ("&quot;", "&#34;", "&#x22;") else "'", text)
    out = []
    for i, ch in enumerate(text):
        before = out[-1] if out else prev
        if i == 0 and fresh and text[1:2].isalnum() and (ch == '"' or not (prev or " ").isalnum()):
            before = ""
        if ch == '"':
            ch = "“" if before in OPENERS or before == "" else "”"
        elif ch == "'":
            after = text[i + 1:i + 2]
            opening = (before in OPENERS or before == "") and after.isalpha()
            if (before in OPENERS or before == "") and ELISIONS.match(text, i + 1):
                opening = False
            ch = "‘" if opening else "’"
        out.append(ch)
    s = "".join(out)
    return s, (s[-1] if s else prev)


def smarten(page):
    """The page with its text's quotation marks curled (STYLE 1-4)."""
    out, skip, prev, fresh = [], None, "", False
    for m in TOKEN.finditer(page):
        tok = m.group(0)
        if tok.startswith("<") and len(tok) > 1:
            name = (m.group(2) or "").lower()
            if skip:
                if m.group(1) and name == skip:
                    skip = None
            elif name in SKIP and not m.group(1) and not tok.endswith("/>"):
                skip = name
            fresh = not tok.startswith("<!--")     # a run right after a tag (STYLE 3)
            out.append(tok)
            continue
        if skip:
            out.append(tok)
            continue
        if "'" in tok or '"' in tok or "&" in tok:
            tok, prev = _curl(tok, prev, fresh)
        elif tok:
            prev = tok[-1]
        fresh = False
        out.append(tok)
    return "".join(out)


def write(path, page):
    """Write a built page, its quotation marks curled; its tags must come out as they went in (STYLE 1)."""
    out = smarten(page)
    if TAGS.findall(out) != TAGS.findall(page):
        a, b = TAGS.findall(page), TAGS.findall(out)
        i = next((k for k, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
        raise ValueError(f"smart.py changed a tag in {path}: {a[i] if i < len(a) else ''!r}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
