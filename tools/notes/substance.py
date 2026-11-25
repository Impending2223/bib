"""The entries whose citations hold substance the line lacks, strongest first (tools/bib/notesub.py, its STYLE).
Run: python3 -I tools/notes/substance.py [--strong]   (tab-separated: score, id, what; the counts on stderr)."""
import collections
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from bib import store, notesub  # noqa: E402

rows = notesub.survey(store.Series())
if "--strong" in sys.argv:
    rows = [r for r in rows if r[0] >= 3]
for r in rows:
    print("\t".join(map(str, r)))
c = collections.Counter(r[0] for r in rows)
print(f"# {len(rows)} entries; by score: {sorted(c.items())}", file=sys.stderr)
