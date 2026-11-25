"""The entries whose footnotes change when a work's page and its note count as one source (footnotes.py, STYLE 11;
notes/proposals/claims-model.md, (f) 3). Writes notes/claims/page-note-one.tsv: id, footnotes before, footnotes after
(0: the entry is shown as one block).

    python3 tools/claims/page_note_one.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bib import store, claims, footnotes  # noqa: E402


def marks(series, e):
    b = footnotes.build(series, e)
    return (0, ()) if b is None else (len(b[1]), tuple(b[0]))


def main():
    series = store.Series()
    rows = []
    for _, e in claims.calendar(series):
        if "via " not in str((e.get("src") or {}).get("rows") or ""):
            continue                                   # only a map with a note's row can change
        footnotes.PAGE_NOTE_ONE = False
        a = marks(series, e)
        footnotes.PAGE_NOTE_ONE = True
        b = marks(series, e)
        if a != b:
            rows.append((e["id"], a[0], b[0]))
    os.makedirs(os.path.join(ROOT, "notes", "claims"), exist_ok=True)
    with open(os.path.join(ROOT, "notes", "claims", "page-note-one.tsv"), "w", encoding="utf-8") as f:
        f.write("id\tfootnotes before\tfootnotes after\n")
        for r in rows:
            f.write("\t".join(map(str, r)) + "\n")
    print(f"{len(rows)} entries change; {sum(1 for r in rows if r[2] == 0)} are shown as one block after")


if __name__ == "__main__":
    main()
