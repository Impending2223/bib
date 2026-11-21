# splice.py IDSFILE: stage, for each modified lists/cal file, HEAD with only the entries in IDSFILE taken from the working tree.
import subprocess, sys, re
ids = set(l.strip() for l in open(sys.argv[1]) if l.strip())
def blocks(t):
    head, rest = t.split("entries:\n", 1)
    parts = re.split(r"(?m)^(?=  - id: )", rest)
    pre = parts[0]; out = []
    for p in parts[1:]:
        m = re.match(r"  - id: (\S+)", p); out.append((m.group(1), p))
    return head + "entries:\n" + pre, out
files = subprocess.run(["git", "diff", "--name-only", "lists/cal/"], capture_output=True, text=True, cwd="/home/user/bib").stdout.split()
staged = []
for f in files:
    H = subprocess.run(["git", "show", "HEAD:" + f], capture_output=True, text=True, cwd="/home/user/bib").stdout
    W = open("/home/user/bib/" + f).read()
    hpre, hb = blocks(H); wpre, wb = blocks(W)
    hd = dict(hb); wd = dict(wb)
    if not (ids & (set(hd) | set(wd))): continue
    out = []
    for i, b in wb:
        if i in ids: out.append(b)
        elif i in hd: out.append(hd[i])
        else: print("DROP (not ours, not in HEAD):", f, i)
    for i in hd:
        if i not in wd and i not in ids: print("MISSING in working (not ours):", f, i)
    # keep HEAD's order for entries that are not ours
    new = hpre + "".join(out)
    if not new.endswith("\n"): new += "\n"
    for i in ids & set(hd):
        if "form:state" in hd[i] or re.search(r"Made public: 196[6-9]", hd[i]): print("OVERLAP risk:", i)
    h = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=new, capture_output=True, text=True, cwd="/home/user/bib").stdout.strip()
    subprocess.run(["git", "update-index", "--cacheinfo", f"100644,{h},{f}"], cwd="/home/user/bib", check=True)
    staged.append(f)
print("staged", len(staged), staged)
