"""Convert a year's calendar entries from unit letters to stored cuts (rulings 35f, 35g;
notes/proposals/claims-model.md, (f) "The conversion"; tools/bib/cuts.py).

    python3 tools/claims/convert.py 1960            dry run: the counts, proof 1, the lists
    python3 tools/claims/convert.py 1960 --write    the year's files rewritten

STYLE
 1. It touches only an entry in which a stored row (`src`), a visibility ruling (`vis:...@C`) or a variant (`unit: C`)
    names a unit by letter. An entry with none is left as it is: no cut, `all` and `?` as before.
 2. Each pair of neighbouring units is compared. Where the rows, rulings or variants that name the two differ, a cut is
    written between them; and one at the end of the line. The parts are numbered 1, 2, 3 in the line's order.
 3. Letters become numbers: in the rows (`A, C-E` -> `1, 3`), with `all` written out as the numbers and `?` kept; in
    the rulings (`@C-D` -> `@3`, several joined by a dot, `@3.4`); in the variants (`unit: C` -> `unit: '3'`).
 4. Not converted, and listed: an entry whose map is stale (its letters may not fit the line), one whose letters name
    a unit the line does not have, one whose line holds a brace, and one that fails proof 1.
 5. Proof 1, for every entry converted: unit by unit, the same sources (claims.resolve), the same rulings
    (vis.rulings) and the same variants before and after. Proof 2 (the year's pages the same, byte for byte) is made
    by building before and after and comparing the files; this tool does not build.
 6. The map's hash (`src.c`) is of the plain line, as before: a cut holds no words, so the hash does not change.
"""
import collections
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bib import store, claims, cuts  # noqa: E402

stored_letters, state, convert = cuts.stored_letters, cuts.state, cuts.convert


def main():
    year = sys.argv[1]
    write = "--write" in sys.argv
    series = store.Series()
    done, skipped, touched, shown = [], [], set(), []
    n_entries = 0
    for sec, e in claims.calendar(series):
        if str(e.get("date") or "")[:4] != year:
            continue
        n_entries += 1
        if not stored_letters(e):
            continue
        new, why = convert(e)
        if new is None:
            skipped.append((e["id"], why))
            continue
        done.append((e["id"], len(new["cuts"])))
        if len(shown) < 4 and len(new["cuts"]) > 1 and len(done) % 97 == 1:
            shown.append((store.stored_form(e), store.stored_form(new)))
        if write:
            i = next(k for k, x in enumerate(sec.entries) if x is e)
            sec.entries[i] = store.normalize_entry(store.stored_form(new))
            touched.add(sec)
    if write:
        for sec in touched:
            series.save_section(sec)
    out = os.path.join(ROOT, "notes", "claims", f"convert-{year}.tsv")
    with open(out, "w", encoding="utf-8") as f:
        f.write("id\twhat\tdetail\n")
        for eid, k in done:
            f.write(f"{eid}\tconverted\t{k} parts\n")
        for eid, why in skipped:
            f.write(f"{eid}\tnot converted\t{why}\n")
    print(f"{year}: {n_entries} entries; {len(done)} converted ({sum(k for _, k in done)} parts); "
          f"{len(skipped)} not converted" + ("; written" if write else "; dry run"))
    for why, k in collections.Counter(w for _, w in skipped).most_common():
        print(f"  not converted, {k}: {why}")
    return shown


if __name__ == "__main__":
    for old, new in main() or []:
        print("\n" + store._emit([{k: old[k] for k in ("id", "c", "src", "tags", "variants") if k in old}], 0))
        print(store._emit([{k: new[k] for k in ("id", "c", "src", "tags", "variants") if k in new}], 0))
