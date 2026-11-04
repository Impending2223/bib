"""Fold the readers' pending witnesses into the registry (rerunnable; tools/bib/witnesses.py, its docstring).

    python3 -I tools/witnesses/fold.py [--dry-run] [FILE...]

With FILEs (paths under inbox/witnesses/), only those are folded: a merger folds the pending file of the patch it
merged while other readers are still writing theirs.

Each new row of inbox/witnesses/*.yaml goes to its year's file (witnesses.file_for), the file kept in id order; a new
row whose id the registry already holds refuses its whole file (printed; kept for the merger to settle). An amendment
row (`amend:`) is applied to its witness on disk (witnesses.apply_amend); one that absorbs another removes the other's
row and points its edges (by-work files, `from` edges, the entries' `via x.` rows) at the keeper. A file folded whole
is deleted.
"""
import collections
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from tools.bib import store, witnesses  # noqa: E402

HEAD = ["The witness registry (tools/bib/witnesses.py, its STYLE; the memo, notes/extensions/memos/witnesses.md). "
        "Kept by hand or agent."]


def main(dry, only=None):
    rows = {}
    for p in witnesses.files():
        for r in store.load_yaml(p) or []:
            rows[r["id"]] = r
    refused, done, amends, new = [], [], [], 0
    pend = witnesses.pending_files()
    if only:
        want = {os.path.abspath(f) for f in only}
        pend = [p for p in pend if os.path.abspath(p) in want]
    for p in pend:
        got = store.load_yaml(p) or []
        bad = [r.get("id") for r in got if isinstance(r, dict) and not r.get("amend") and (not r.get("id") or r["id"] in rows)]
        if bad:
            refused.append((p, bad))
            continue
        for r in got:
            if r.get("amend"):
                amends.append(r)
            else:
                rows[r["id"]] = r
                new += 1
        done.append(p)
    absorbed = {}
    for a in amends:
        if a["amend"] in rows:
            witnesses.apply_amend(rows[a["amend"]], a, rows, absorbed)
        else:
            print(f"amend {a['amend']}: no such witness (dropped)")
    for p, bad in refused:
        print(f"refused {os.path.relpath(p, ROOT)}: ids taken or missing: {', '.join(map(str, bad[:5]))}")
    print(f"{new} new rows, {len(amends)} amendments, {len(absorbed)} absorbed, from {len(done)} files"
          + (" (dry run)" if dry else ""))
    if dry:
        return
    for w in rows.values():
        for f in w.get("from") or []:
            if f.get("of") in absorbed:
                f["of"] = absorbed[f["of"]]
    by_file = collections.defaultdict(list)
    for wid in sorted(rows):
        by_file[witnesses.file_for(wid)].append(rows[wid])
    for path, rs in by_file.items():
        store.dump_yaml(rs, path, header=HEAD)
    for path in witnesses.files():
        if path not in by_file:
            os.remove(path)
    if absorbed:
        for path in witnesses.work_files():
            es = store.load_yaml(path) or []
            if any(e.get("of") in absorbed for e in es):
                for e in es:
                    e["of"] = absorbed.get(e.get("of"), e.get("of"))
                store.dump_yaml(es, path, header=[f"w.{os.path.basename(path)[:-5]}: its edges, page and note to the "
                                                  "witness its text rests on (tools/bib/witnesses.py)."])
        s = store.Series(ROOT)
        for lst in s.lists.values():
            for sec in lst.walk():
                hit = False
                for e in sec.entries:
                    src = e.get("src") or {}
                    rs = src.get("rows") or []
                    nr = [re.sub(r"^via (x\.\S+):", lambda m: f"via {absorbed.get(m.group(1), m.group(1))}:", r) for r in rs]
                    if nr != rs:
                        src["rows"], hit = nr, True
                if hit:
                    s.save_section(sec)
    for p in done:
        os.remove(p)


if __name__ == "__main__":
    main("--dry-run" in sys.argv, [a for a in sys.argv[1:] if not a.startswith("--")])
