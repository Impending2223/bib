"""The rule check of owner-rulings 53 (Nov. 24, 2026: "We can't have an unmarked citation unless we've read the cited
matter"): what changes on the page when a map's row that reaches a record through a work's note (`via w.… 88 n.32`)
stops printing as a citation (footnotes.py, STYLE 13).

`python3 -I tools/claims/via_rule.py [--write]` reads every calendar entry whose map has such a row and compares, part by
part of the line, the sources printed with the old form (footnotes.VIA_PRINTS True) and the new. A row a line:

  same     the part cites the record's own copy by an item of the note: nothing is lost;
  elsewhere the entry cites the record's copy, but not on this part: a reader may place it here (choice 1) or not;
  work     the part keeps the work's page and loses only "& n.32 (citing ...)";
  bare     the part is left with no source at all: it takes a "Check:" or a reader's cite.

--write: the rows to notes/via-read/rule-2026-11-25.tsv, the counts to stdout. Reads the tree only otherwise."""
import collections
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from tools.bib import claims, footnotes, store  # noqa: E402

OUT = os.path.join(ROOT, "notes", "via-read", "rule-2026-11-25.tsv")


def texts(per):
    return [tuple(x["text"] for x in p) for p in per]


def main():
    s = store.Series(ROOT)
    reg = footnotes._register(s)
    rows_out, counts = [], collections.Counter()
    for sec in s.lists["cal"].sections:
        for e in sec.entries:
            if "via w." not in str(e.get("src") or ""):
                continue
            src, c = e.get("src"), e.get("c")
            if not isinstance(c, str) or not c or not e.get("n"):
                continue
            if isinstance(src, dict) and src.get("c") and src.get("c") != claims.chash(c):
                counts["stale map (one block; not compared)"] += 1
                continue
            rows = claims.resolve(e)
            us = claims.units(e.get("c") or "")
            footnotes.VIA_PRINTS = True
            before = texts(footnotes._cites(s, e)[1])
            footnotes.VIA_PRINTS = False
            after = texts(footnotes._cites(s, e)[1])
            cited = footnotes.Cited(e)
            for r, k, key, pin, note, u, item in rows:
                if k != "via" or not isinstance(u, set):
                    continue
                rec = reg.get((key, str(pin), str(note)))
                if not rec or not rec.get("read"):
                    continue
                whole = cited.printed(rec) or cited.recorded(rec)
                for i, unit in enumerate(us):
                    L = claims.LETTERS[i]
                    if L not in u:
                        continue
                    items = [it for _, k2, _, _, _, u2, it in rows if it and isinstance(u2, set) and L in u2]
                    here = footnotes.Cited({"n": "; ".join(items) + ".", "c": unit})
                    if here.printed(rec) or here.recorded(rec):
                        kind = "same"
                    elif not after[i] and before[i]:
                        kind = "bare"
                    elif whole:
                        kind = "elsewhere"
                    else:
                        kind = "work"
                    counts[kind] += 1
                    if kind != "same":
                        rows_out.append((e["id"], r, rec.get("id") or "", kind, " ".join(unit.split())[:160]))
    for k, v in sorted(counts.items()):
        print(f"{v:6d}  {k}")
    if "--write" in sys.argv:
        with open(OUT, "w") as f:
            f.write("entry\trow\trecord\twhat changes\tthe part of the line\n")
            for row in sorted(rows_out):
                f.write("\t".join(row) + "\n")
        print(len(rows_out), "rows to", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
