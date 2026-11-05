"""Unwrap Markdown files in place (tools/bib/mdwrap.py, its STYLE). Run: python3 -I THIS FILE.md [...]; each file's
words are checked unchanged (whitespace aside) before it is written."""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from bib.mdwrap import unwrap

for p in sys.argv[1:]:
    t = open(p, encoding="utf-8").read()
    n = unwrap(t)
    n = n if n.endswith("\n") else n + "\n"
    if re.sub(r"\s+", " ", t).strip() != re.sub(r"\s+", " ", n).strip():
        sys.exit(f"{p}: words changed; not written")
    if n != t:
        open(p, "w", encoding="utf-8").write(n)
        print(p, t.count("\n"), "->", n.count("\n"), "lines")
