"""Convert thread statements to one statement each (notes/extensions/memos/volume.md, §4; tools/bib/statements.py).

    python3 -I tools/statements/apply.py FRAGMENT.yaml [--dry-run]

FRAGMENT.yaml: a list of rows (or a mapping whose `rows:` is the list), each

    - id: cal.thread.<slug>
      c: 'The scope. {{1961..1962-06|A sentence of those months.}} {{1966..|Another.}}'
      short:                                # optional: the events' names, on their first entries
        cal.1961-04-15.cuba: Bay of Pigs
        cal.1961-11-30.cuba: Mongoose

Writes each row's `c` into lists/cal/th.yaml, deleting the thread's `c2`, `c3` (any cN), and each `short:` onto the
entry named, saving only the sections touched (store.Series.save_section), nothing else. Prints what it changed, and
any other line the save rewrote into the store's canonical form (a list hand-written in flow style where the emitter
writes a block: `see_also: [a, b]` in th.yaml), to be put back by hand or kept.

Refused, the whole row, nothing of it written: a thread id th.yaml does not hold; a `c` whose span cannot be read;
an entry id that is no dated calendar entry; a new `short:` for an address (an entry with `to:`) that already has
another, since that name prints in its From lines too (statements.py, STYLE 4). Printed and written all the same: a
`short:` on an entry outside the thread's own (its `thread:` neither the thread nor a ghost subthread of it), whose
name will show in its own thread's statement, not this one's. Exits 1 where any row was refused.
"""
import difflib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from tools.bib import store, statements  # noqa: E402
from tools.bib.concepts import parse  # noqa: E402


def rows_of(path):
    d = store.load_yaml(path)
    if isinstance(d, dict):
        d = d.get("rows")
    if not isinstance(d, list):
        sys.exit(f"{path}: expected a list of rows (or rows: [...])")
    return d


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__.split("\n\n")[1])
    series = store.Series(ROOT)
    cal = series.lists["cal"]
    th = cal.section(cal.data.get("threads_section", "th"))
    threads = cal.threads()
    touched, refused = {}, 0
    for row in rows_of(args[0]):
        tid = str((row or {}).get("id") or "")
        slug = tid.split(".", 2)[2] if tid.startswith("cal.thread.") else None
        why = []
        if slug not in threads:
            why.append(f"no thread {tid!r} in th.yaml")
        c = row.get("c")
        if not c:
            why.append("no c")
        else:
            for t in store.as_list(c):
                try:
                    parse(str(t))
                except ValueError as err:
                    why.append(f"a span it cannot read: {err}")
        shorts = row.get("short") or {}
        if not isinstance(shorts, dict):
            why.append("short: is not a mapping of entry id to name")
            shorts = {}
        notes = []
        for eid, name in shorts.items():
            hit = series.get(str(eid))
            e = hit[2] if hit else None
            if not e or hit[0] is not cal or "when" not in e or not e.get("date"):
                why.append(f"short: {eid} is no dated calendar entry")
                continue
            if e.get("to") and e.get("short") and e["short"] != name:
                why.append(f"short: {eid} is an address named {e['short']!r} in its From lines; not renamed {name!r}")
            line = cal.thread_line(e["thread"])
            if slug and not (slug in line and all(cal.is_ghost(x) for x in line[:line.index(slug)])):
                notes.append(f"  note: {eid} is filed under {e['thread']!r}, not {slug!r} or a ghost of it: its name "
                             "shows in that thread's statement, not this one's")
        if why:
            refused += 1
            print(f"REFUSED {tid}: " + "; ".join(why))
            continue
        te = threads[slug]
        print(f"{tid}:")
        if te.get("c") != c:
            print(f"  c: {te.get('c')!r}\n   -> {c!r}")
            te["c"] = c
            touched[id(th)] = th
        for k in statements.LEGACY:
            if k in te:
                print(f"  {k} deleted: {te[k]!r}")
                del te[k]
                touched[id(th)] = th
        for eid, name in shorts.items():
            lst, sec, e = series.get(str(eid))
            if e.get("short") != name:
                print(f"  short {e['id']}: {e.get('short')!r} -> {name!r}")
                e["short"] = name
                touched[id(sec)] = sec
        for n in notes:
            print(n)
    if dry:
        print(f"dry run: nothing written ({len(touched)} sections would be)")
    else:
        for sec in touched.values():
            path = os.path.join(ROOT, "lists", cal.key, sec.file)
            before = open(path, encoding="utf-8").read().splitlines()
            series.save_section(sec)
            after = open(path, encoding="utf-8").read().splitlines()
            # the save writes the file in the store's canonical form: a line hand-written otherwise (a flow list
            # the emitter writes as a block) changes too; named here, to be put back by hand or kept
            other = [ln for ln in difflib.unified_diff(before, after, lineterm="", n=0)
                     if ln[:1] in "+-" and not ln.startswith(("+++", "---"))
                     and not re.match(r"^[+-]    (c|c\d|short): ", ln)]
            for ln in other:
                print(f"  also rewritten in {sec.file} (canonical form): {ln[:120]}")
        print(f"{len(touched)} sections written")
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
