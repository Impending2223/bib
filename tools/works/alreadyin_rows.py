"""The book-checks' "already in" Passed over rows, each with whether its work is cited by page under the entry it names
(batch 7, notes/briefs/batch7.md). python3 -I tools/works/alreadyin_rows.py OUT.json [--summary]
States: cited (the work cited with a pinpoint under every entry the row names), absent (not cited under one), to-check
(only behind To check), no-id (the row names no entry), missing (an entry it names is not in the tree)."""
import collections, glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from tools.bib import store  # noqa: E402


def main():
    s = store.Series(ROOT)
    ents = {}
    for sec in s.lists["cal"].sections:
        for e in sec.entries:
            ents[e["id"]] = e
            for a in e.get("aliases") or []:
                ents[a] = e
    out, stat = [], collections.Counter()
    for f in sorted(glob.glob(os.path.join(ROOT, "notes/book-checks/*.md"))):
        t = open(f).read()
        cm = re.search(r"`(w\.[a-z0-9-]+)`", t[:2000]) or re.search(r"(w\.[a-z0-9-]+)", os.path.basename(f))
        card = cm.group(1) if cm else None
        m = re.search(r"^#+ Passed over.*?$(.*?)(?=^## |\Z)", t, re.M | re.S | re.I)
        if not m:
            continue
        for l in m.group(1).split("\n"):
            if not (re.search(r"already (in|entered|in the calendar)|in the calendar already|already has", l, re.I)
                    and (l.startswith("|") or l.startswith("- "))):
                continue
            ids = re.findall(r"cal\.\d{4}-\d{2}(?:-\d{2})?\.[a-z0-9-]+", l)
            state = "no-id"
            if ids and card:
                st = []
                for i in ids:
                    e = ents.get(i)
                    if not e:
                        st.append("missing")
                        continue
                    n = str(e.get("n") or "")
                    if re.search(re.escape("[[" + card) + r"(\|[^\]]*)?\]\],? ?[0-9IVXLC]", n):
                        st.append("cited")
                    else:
                        st.append("to-check" if "[[" + card in n else "absent")
                state = ("cited" if all(x == "cited" for x in st) else "absent" if "absent" in st
                         else "to-check" if "to-check" in st else "missing")
            stat[state] += 1
            out.append({"file": os.path.relpath(f, ROOT), "card": card, "ids": ids, "state": state, "row": l.strip()})
    json.dump(out, open(sys.argv[1], "w"), indent=0)
    print(dict(stat))


if __name__ == "__main__":
    main()
