"""Văn kiện Đảng toàn tập PDFs: their text layers are in the TCVN3 (ABC) font encoding, extracted as
Latin-1/cp1252 look-alikes. Usage: python3 -I vkd2txt.py IN.pdf OUT.txt [FIRST LAST]
Converts to Unicode by way of glibc iconv (TCVN5712-1). Headings set in the ABC capitals font come out
in lower case letters with capital diacritics ("NGHị QUYếT"): read them as capitals."""
import subprocess, sys
pdf, out = sys.argv[1], sys.argv[2]
rng = sys.argv[3:5]
cmd = ["pdftotext", "-layout"] + (["-f", rng[0], "-l", rng[1]] if rng else []) + [pdf, "-"]
txt = subprocess.run(cmd, capture_output=True).stdout.decode("utf-8", "replace")
FIX = {"−": "\xad", "–": "\x96", "—": "\x97", "‘": "\x91", "’": "\x92",
       "“": "\x93", "”": "\x94", "…": "\x85", "•": "\x95", "ﬁ": "fi", "ﬂ": "fl"}
b = bytearray()
for ch in txt:
    ch = FIX.get(ch, ch)
    for c in ch:
        try:
            b += c.encode("latin-1")
        except UnicodeEncodeError:
            b += c.encode("cp1252", "replace")
r = subprocess.run(["iconv", "-f", "TCVN5712-1", "-t", "UTF-8", "-c"], input=bytes(b), capture_output=True)
open(out, "wb").write(r.stdout)
print(len(r.stdout), "bytes;", r.stderr.decode()[:200])
