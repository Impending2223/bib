"""Renew the hash of the maps left stale by audited edits made before merge.op_edit renewed it (cuts.py, STYLE 12).

    python3 -I tools/claims/renew_hash.py            dry run: the counts
    python3 -I tools/claims/renew_hash.py --write    the hashes written in lists/cal; the rest listed

A map is renewed where it names no unit by letter and every part its rows name is still in the line. The rest stay
stale and are listed in notes/claims/stale-left.tsv for a reader (a lettered row; a part the line has lost)."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from tools.bib import claims, cuts, store  # noqa: E402


def main():
    s = store.Series(ROOT)
    done, left, touched = [], [], set()
    for sec in s.lists["cal"].sections:
        for e in sec.entries:
            src = e.get("src")
            if not isinstance(src, dict) or not src.get("c") or src.get("c") == claims.chash(e.get("c") or ""):
                continue
            if cuts.renew(e):
                done.append(e["id"])
                touched.add(sec)
            else:
                why = "a row names units by letter" if any(k == "row" for k, _, _ in cuts.stored_letters(e)) \
                    else "a row names a part the line no longer has"
                left.append((e["id"], why))
    print(f"renewed: {len(done)}; left stale: {len(left)}")
    if "--write" in sys.argv:
        for sec in touched:
            s.save_section(sec)
        with open(os.path.join(ROOT, "notes", "claims", "stale-left.tsv"), "w") as f:
            f.write("entry\twhy the map stays stale\n")
            for row in left:
                f.write("\t".join(row) + "\n")


if __name__ == "__main__":
    main()
