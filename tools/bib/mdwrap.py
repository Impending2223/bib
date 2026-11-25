"""Markdown without hard wraps (the owner, Nov. 5, 2026: the in-app reader shows a hard wrap as a break mid-sentence;
"unwrap them all, fix the scripts"). `unwrap(text)` joins each paragraph's and each list item's lines into one line.

STYLE:
 1. Kept line for line: headings, blank lines, tables (`|`), horizontal rules, fenced code (```), indented code (four
    spaces or a tab after a blank line, outside a list), block quotes (`>`: the owner's messages are quoted verbatim,
    their own line breaks theirs), HTML lines (`<`), and a line ending in a hard break (two spaces, `\\`, `<br>`).
 2. A list item's continuation lines join the item; a paragraph's lines join the paragraph, a single space between.
 4. `careful=True`, for notes written by hand (tools/notes/unwrap_md.py; Nov. 24-25, 2026: run over the owner's
    brief, the reader's brief and the handoff it joined paragraphs that were already a line each). These notes set
    one paragraph under another with no blank line between, so two lines together are not always one paragraph. A
    line is joined to the one above only where the one above looks cut by a wrap: it is no longer than WIDE, the
    next line's first word would not have fitted within NARROW, and it does not end a sentence. Never joined: a
    line that opens with "-- " (the owner's brief's nested points); a line that is not indented, under a list item;
    an item numbered "4a." or "10a." (a list item, as "4." is). A wrapped line that happens to end a sentence
    stays as it is: the tool leaves a wrap sooner than join two paragraphs.
 3. Every generator of a `.md` passes its text through `unwrap` before writing (calaudit, works inventory,
    make_listing, law_listing, lag_listing, jacobson, make_pocom, vnmap/validate).
"""
import re

LIST = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+")
DASHES = re.compile(r"^\s*--\s+")
HR = re.compile(r"^(-{3,}|\*{3,}|_{3,})$")


WIDE, NARROW = 125, 72
LIST_CAREFUL = re.compile(r"^(\s*)([-*+]|\d+[a-z]{0,2}[.)])\s+")


def _cut(above, word):
    """Whether the line above looks cut by a wrap before `word` (STYLE 4)."""
    a = above.rstrip()
    return len(a) <= WIDE and len(a) + 1 + len(word) > NARROW and not re.search(r"[.?!:;\"”)\]*`]$", a)


def unwrap(text, careful=False):
    out, buf, fence, in_list, item, last = [], None, False, False, False, ""
    is_list = (lambda ln: LIST_CAREFUL.match(ln) or DASHES.match(ln)) if careful else LIST.match

    def flush():
        nonlocal buf
        if buf is not None:
            out.append(buf)
            buf = None

    for ln in text.split("\n"):
        s = ln.strip()
        if s.startswith("```") or s.startswith("~~~"):
            flush(); fence = not fence; out.append(ln); continue
        if fence:
            out.append(ln); continue
        if not s:
            flush(); out.append(ln); in_list = in_list and True; continue
        if (s.startswith(("#", "|", ">", "<")) or HR.match(s)):
            flush(); out.append(ln); in_list = False if s.startswith("#") else in_list; continue
        if is_list(ln):
            flush(); buf = ln.rstrip(); in_list = True; item = True; last = ln
            if ln.endswith(("  ", "\\")) or s.endswith("<br>"):
                flush()
            continue
        indented = ln.startswith(("    ", "\t"))
        if indented and buf is None and not in_list and (not out or not out[-1].strip()):
            out.append(ln); continue
        if indented and buf is None and out and out[-1].startswith(("    ", "\t")) and not in_list:
            out.append(ln); continue
        if careful and buf is not None and ((item and not ln.startswith((" ", "\t"))) or not _cut(last, s.split()[0])):
            flush()                           # a paragraph of its own, not the line above cut by a wrap (STYLE 4)
        if buf is not None:
            buf += " " + s
        else:
            buf = ln.rstrip()
            item = False
            if not ln.startswith((" ", "\t")):
                in_list = False
        last = ln
        if ln.endswith(("  ", "\\")) or s.endswith("<br>"):
            flush()
    flush()
    return "\n".join(out)
