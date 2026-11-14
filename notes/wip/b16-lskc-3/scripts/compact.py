import re, sys
src, out = sys.argv[1], sys.argv[2]
t = open(src).read()
parts = re.split(r"\n===== PDF (\d+) =====\n", t)
res = []; prev = 0
for i in range(1, len(parts), 2):
    pdf = int(parts[i]); body = parts[i+1]
    lines = [l.strip() for l in body.split("\n") if l.strip()]
    if not lines: continue
    m = re.match(r"^(\d{1,3})\b", lines[0]) or re.search(r"\b(\d{1,3})$", lines[0])
    if m and int(m.group(1)) in range(prev, prev+3): folio = int(m.group(1)); lines = lines[1:]
    else: folio = prev + 1
    prev = folio
    txt = " ".join(lines)
    txt = txt.replace("Ỏ", "“").replace("Õ", "”")
    res.append(f"[p{folio}] {txt}")
open(out, "w").write("\n".join(res))
