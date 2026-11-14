import subprocess, sys, json
pdf, out = sys.argv[1], sys.argv[2]
txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True).stdout.decode("utf-8", "replace")
FIX = {"−": "\xad", "–": "\x96", "—": "\x97", "‘": "\x91", "’": "\x92",
       "“": "\x93", "”": "\x94", "…": "\x85", "•": "\x95", "ﬁ": "fi", "ﬂ": "fl"}
pages = txt.split("\f")
res = []
for p in pages:
    b = bytearray()
    for ch in p:
        ch = FIX.get(ch, ch)
        for c in ch:
            try: b += c.encode("latin-1")
            except UnicodeEncodeError: b += c.encode("cp1252", "replace")
    r = subprocess.run(["iconv", "-f", "TCVN5712-1", "-t", "UTF-8", "-c"], input=bytes(b), capture_output=True)
    res.append(r.stdout.decode("utf-8", "replace"))
with open(out, "w") as f:
    for i, p in enumerate(res, 1):
        f.write(f"\n===== PDF {i} =====\n{p}")
print(len(pages))
