"""Unwrap a Markdown file's hard-wrapped paragraphs and list items into one line each (the owner, Nov. 5, 2026: the
in-app reader shows a hard wrap as a break mid-sentence). Headings, blank lines, tables, code blocks and block quotes'
line structure are kept; a list item's continuation lines join the item. Run: python3 -I THIS FILE.md [...]."""
import re, sys

LIST = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+")


def unwrap(text):
    out, buf, fence = [], None, False
    def flush():
        nonlocal buf
        if buf is not None:
            out.append(buf)
            buf = None
    for ln in text.split("\n"):
        s = ln.strip()
        if s.startswith("```"):
            flush(); fence = not fence; out.append(ln); continue
        if fence:
            out.append(ln); continue
        if not s or s.startswith("#") or s.startswith("|") or re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
            flush(); out.append(ln); continue
        if s.startswith(">"):
            if buf is not None and buf.lstrip().startswith(">"):
                buf += " " + s.lstrip("> ").strip(); continue
            flush(); buf = ln.rstrip(); continue
        if LIST.match(ln):
            flush(); buf = ln.rstrip(); continue
        if buf is not None:
            buf += " " + s
        else:
            buf = ln.rstrip()
    flush()
    return "\n".join(out)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        t = open(p).read()
        n = unwrap(t)
        open(p, "w").write(n if n.endswith("\n") else n + "\n")
        print(p, len(t.split("\n")), "->", len(n.split("\n")), "lines")
