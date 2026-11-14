import re, sys
t = open(sys.argv[1]).read()
parts = re.split(r"\n===== PDF (\d+) =====\n", t)
prev=None
for i in range(1, len(parts), 2):
    pdf = int(parts[i]); lines=[l.strip() for l in parts[i+1].split("\n") if l.strip()]
    f=None
    if lines:
        m = re.match(r"^(\d{1,3})\b", lines[0]) or re.search(r"\b(\d{1,3})$", lines[0])
        if m: f=int(m.group(1))
    off = pdf-f if f is not None else None
    if off!=prev: print(pdf, f, off, (lines[0][:60] if lines else ''))
    prev=off
