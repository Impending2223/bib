"""Markdown without hard wraps (the owner, Nov. 5, 2026: the in-app reader shows a hard wrap as a break mid-sentence;
"unwrap them all, fix the scripts"). `unwrap(text)` joins each paragraph's and each list item's lines into one line.

STYLE:
 1. Kept line for line: headings, blank lines, tables (`|`), horizontal rules, fenced code (```), indented code (four
    spaces or a tab after a blank line, outside a list), block quotes (`>`: the owner's messages are quoted verbatim,
    their own line breaks theirs), HTML lines (`<`), and a line ending in a hard break (two spaces, `\\`, `<br>`).
 2. A list item's continuation lines join the item; a paragraph's lines join the paragraph, a single space between.
 3. Every generator of a `.md` passes its text through `unwrap` before writing (calaudit, works inventory,
    make_listing, law_listing, lag_listing, jacobson, make_pocom, vnmap/validate).
"""
import re

LIST = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+")
HR = re.compile(r"^(-{3,}|\*{3,}|_{3,})$")


def unwrap(text):
    out, buf, fence, in_list = [], None, False, False

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
        if LIST.match(ln):
            flush(); buf = ln.rstrip(); in_list = True
            if ln.endswith(("  ", "\\")) or s.endswith("<br>"):
                flush()
            continue
        indented = ln.startswith(("    ", "\t"))
        if indented and buf is None and not in_list and (not out or not out[-1].strip()):
            out.append(ln); continue
        if indented and buf is None and out and out[-1].startswith(("    ", "\t")) and not in_list:
            out.append(ln); continue
        if buf is not None:
            buf += " " + s
        else:
            buf = ln.rstrip()
            if not ln.startswith((" ", "\t")):
                in_list = False
        if ln.endswith(("  ", "\\")) or s.endswith("<br>"):
            flush()
    flush()
    return "\n".join(out)
