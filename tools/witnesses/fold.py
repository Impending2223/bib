"""Fold the readers' pending witnesses into the registry (rerunnable; tools/bib/witnesses.py, its docstring).

    python3 -I tools/witnesses/fold.py [--dry-run]

Each row of inbox/witnesses/*.yaml goes to its year's file (witnesses.file_for), the file kept in id order; a row whose
id the registry already holds is refused (printed; the file is kept for the merger to settle); a file folded whole is
deleted.
"""
import collections
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from tools.bib import store, witnesses  # noqa: E402

HEAD = ["The witness registry (tools/bib/witnesses.py, its STYLE; the memo, notes/extensions/memos/witnesses.md). "
        "Kept by hand or agent."]


def main(dry):
    have = {}
    for p in witnesses.files():
        for r in store.load_yaml(p) or []:
            have[r["id"]] = p
    add, refused = collections.defaultdict(list), []
    done = []
    for p in witnesses.pending_files():
        rows = store.load_yaml(p) or []
        bad = [r.get("id") for r in rows if not isinstance(r, dict) or not r.get("id") or r["id"] in have]
        if bad:
            refused.append((p, bad))
            continue
        for r in rows:
            add[witnesses.file_for(r["id"])].append(r)
            have[r["id"]] = p
        done.append(p)
    for p, bad in refused:
        print(f"refused {os.path.relpath(p, ROOT)}: ids taken or missing: {', '.join(map(str, bad[:5]))}")
    if dry:
        print(f"{sum(len(v) for v in add.values())} rows from {len(done)} files (dry run)")
        return
    for path, rows in add.items():
        old = (store.load_yaml(path) or []) if os.path.exists(path) else []
        store.dump_yaml(sorted(old + rows, key=lambda r: r["id"]), path, header=HEAD)
    for p in done:
        os.remove(p)
    print(f"{sum(len(v) for v in add.values())} rows folded from {len(done)} files; {len(refused)} refused")


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
