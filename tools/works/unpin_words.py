"""One-time sweep (the owner, Oct. 30, 2026): a work cited in a calendar note's sources with words where its pinpoint
should be ("[[w.x]], on Rusk", "[[w.x]], for the arithmetic", a chapter's title), or with none at all, was recalled,
not read: it goes behind
"To check:", the words kept as its parenthetical ("[[w.x]] (on Rusk)"), and a reader's map (`src`) drops the rows that
named it. A pinpoint names a number or links the place read (claims.is_pin, claims.item_key). The note is edited as
text, the item cut from its sentence and put at the head of the To check run (the build orders the run), so nothing
else in the note moves. Don't rerun: `check` now fails on any new case [claims].

    python3 -I tools/works/unpin_words.py [--dry-run]
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from tools.bib import notemerge as nm                       # noqa: E402
from tools.bib.claims import CARD_ITEM, item_key, note_parts  # noqa: E402
from tools.bib.store import Series                          # noqa: E402


def cut(n, it):
    """The note with the item cut from its sentence (and the sentence gone if it held nothing else)."""
    for a, b in ((it + "; ", ""), ("; " + it, ""), (it + ";", ""), (";" + it, "")):
        if a in n:
            return n.replace(a, b, 1)
    for a in (" " + it + ".", it + ". ", it + "."):
        if a in n:
            return n.replace(a, "", 1).strip()
    raise ValueError(f"cannot cut {it!r}")


def put(n, forms):
    """The note with the forms at the head of its To check run, or a new To check before See, Check or Names."""
    add = "; ".join(forms)
    if "To check: " in n:
        return n.replace("To check: ", f"To check: {add}; ", 1)
    m = re.search(r"(?:^| )(See \[\[|Check: |Names: )", n)
    if m:
        at = m.start(1)
        return n[:at] + f"To check: {add}. " + n[at:]
    return n.rstrip() + f" To check: {add}."


PHRASE = re.compile(r"^([a-z][^\[\]();]{0,40}), (\[\[w\.[^\]|]+\]\])$")   # "for New Haven, [[w.x]]"


def sweep(n):
    moved = []
    for it in note_parts(n)[0]:
            it = it.strip()
            p = PHRASE.match(it)
            if p:
                moved.append((p.group(2)[2:-2], it, f"{p.group(2)} ({p.group(1)})"))
                continue
            m = CARD_ITEM.match(it)
            if m and item_key(it)[2] is None:
                words, paren = (m.group(2) or "").strip(), m.group(3)
                inner = "; ".join(x for x in (words, paren[1:-1] if paren else "") if x)
                moved.append((m.group(1).strip(), it, it[:it.index("]]") + 2] + (f" ({inner})" if inner else "")))
    if not moved:
        return n, []
    for _, it, _ in moved:
        n = cut(n, it)
    return put(n, [f for _, _, f in moved]), moved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    s = Series()
    touched, total = set(), 0
    for lst in s.lists.values():
        if lst.kind != "calendar":
            continue
        for sec in lst.walk():
            for e in sec.entries:
                if not isinstance(e.get("n"), str):
                    continue
                new, moved = sweep(e["n"])
                if not moved:
                    continue
                total += len(moved)
                print(f"{e['id']}\n  - {e['n']}\n  + {new}")
                e["n"] = new
                src = e.get("src")
                if isinstance(src, dict) and isinstance(src.get("rows"), list):
                    gone = {c for c, _, _ in moved}
                    keep = []
                    for r in src["rows"]:
                        head = r.split(":")[0].split(" ", 1)
                        if head[0] in gone and (len(head) == 1 or not re.search(r"\d", head[1])):
                            continue
                        keep.append(r)
                    if keep != src["rows"]:
                        print(f"  src rows dropped: {[r for r in src['rows'] if r not in keep]}")
                    if keep:
                        src["rows"] = keep
                    else:
                        del e["src"]
                touched.add(sec)
    print(f"{total} works moved behind To check, {len(touched)} sections")
    if not a.dry_run:
        for sec in touched:
            s.save_section(sec)


if __name__ == "__main__":
    main()
