"""Typographer's quotation marks, made at the build: the YAML keeps the keyboard's ' and ", and every page is written
with ‘ ’ “ ” in its text.

STYLE
 1. Only text is touched: not tags or their attributes (URLs, ids, titles on hover keep their characters), and not
    the contents of <script>, <style>, <pre>, <code> or <textarea>. Entities that stand for a quotation mark in text
    (&quot; &#34; &#39; &#x27; &apos;) are curled as the characters are.
 2. A double quotation mark opens at the start of the text or after a space, an opening bracket, a dash, or an
    opening mark; it closes elsewhere. A single mark is an apostrophe (’) unless it opens a quotation by the same rule
    and is followed by a letter; an elision written with an apostrophe first stays ’ ('60s, '64, 'n', 'em, 'tis,
    'twas, 'til, 'cause).
 3. Tags are transparent: the character before a mark may lie in the text before an <i> or <a> (“<i>Title</i>”).
 4. Marks already curled in the text are left as they are. An inch or a minute is written as a prime (″ ′) in the
    sources, not as a quotation mark.
"""
import re

SKIP = ("script", "style", "pre", "code", "textarea")
OPENERS = set(" \t\n\r ([{—–-/“‘")
ELISIONS = re.compile(r"(?:\d\d(?:s|\b)|n'|em\b|tis\b|twas\b|til\b|cause\b)", re.I)
ENT = re.compile(r"&(?:quot|#34|#x22|#39|#x27|apos);", re.I)
TOKEN = re.compile(r"<!--.*?-->|<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>|[^<]+|<", re.S)


def _curl(text, prev):
    """Curl the marks in one run of text; prev is the character before it (across tags). Returns (text, last)."""
    text = ENT.sub(lambda m: '"' if m.group(0).lower() in ("&quot;", "&#34;", "&#x22;") else "'", text)
    out = []
    for i, ch in enumerate(text):
        before = out[-1] if out else prev
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
    out, skip, prev = [], None, ""
    for m in TOKEN.finditer(page):
        tok = m.group(0)
        if tok.startswith("<") and len(tok) > 1:
            name = (m.group(2) or "").lower()
            if skip:
                if m.group(1) and name == skip:
                    skip = None
            elif name in SKIP and not m.group(1) and not tok.endswith("/>"):
                skip = name
            out.append(tok)
            continue
        if skip:
            out.append(tok)
            continue
        if "'" in tok or '"' in tok or "&" in tok:
            tok, prev = _curl(tok, prev)
        elif tok:
            prev = tok[-1]
        out.append(tok)
    return "".join(out)


def write(path, page):
    """Write a built page, its quotation marks curled."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(smarten(page))
