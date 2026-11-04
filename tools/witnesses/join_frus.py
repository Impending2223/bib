"""Join the witnesses that are one FRUS document (rerunnable).

    python3 -I tools/witnesses/join_frus.py [--dry-run]

Two witnesses whose `copies` name the same FRUS document ("FRUS 1964–68, VI, doc. 64"), and whose dates do not differ,
are one document cited by two works under two descriptions (Dallek's "Tom Johnson's notes", Longley's "Notes of
Meeting"): counted as two roots they would be circular reporting (the memo, §1-2). The first id (sorted) is kept; the
other's edges in by-work/ and its `from` edges elsewhere are moved to it, its descriptions kept in `also_as`, its
copies, where and read merged; its id is left out of the registry and never reused. A claim map's `via x.` row naming
the old id is rewritten (none at the first run). Each join is printed.
"""
import collections
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from tools.bib import store, witnesses  # noqa: E402

FRUS = re.compile(r"FRUS (\d{4})[–-](\d{2}),\s*([IVXL]+)(?:,\s*(pt\. \d|microfiche supp\.))?,\s*doc\.\s*(\d+)", re.I)


def key(copy):
    m = FRUS.search(str(copy))
    return m and (m.group(1), m.group(2), m.group(3).upper(), (m.group(4) or "").lower(), m.group(5))


def main(dry):
    rows, edges, where = witnesses.load()
    groups = collections.defaultdict(list)
    for wid, w in rows.items():
        for c in w.get("copies") or []:
            k = key(c)
            if k:
                groups[k].append(wid)
    moved = {}
    for k, ids in sorted(groups.items()):
        ids = sorted(set(ids) - set(moved))
        if len(ids) < 2:
            continue
        keep = ids[0]
        for d in ids[1:]:
            a, b = str(rows[keep].get("date") or ""), str(rows[d].get("date") or "")
            if a and b and not (a.startswith(b) or b.startswith(a)):
                continue
            moved[d] = keep
    for d, keep in moved.items():
        while keep in moved:
            keep = moved[keep]
        moved[d] = keep
    for d, keep in sorted(moved.items()):
        k, w = rows[keep], rows[d]
        print(f"{d} -> {keep}: {w.get('what')!r} as {k.get('what')!r}")
        if w.get("what") != k.get("what") and w.get("what") not in (k.get("also_as") or []):
            k.setdefault("also_as", []).append(w["what"])
        for c in w.get("copies") or []:
            if c not in (k.get("copies") or []):
                k.setdefault("copies", []).append(c)
        if w.get("where") and not k.get("where"):
            k["where"] = w["where"]
        k["read"] = bool(k.get("read") or w.get("read"))
    if dry or not moved:
        print(f"{len(moved)} joins" + (" (dry run)" if dry else ""))
        return
    for w in rows.values():
        for f in w.get("from") or []:
            if f.get("of") in moved:
                f["of"] = moved[f["of"]]
    by_file = collections.defaultdict(list)
    for wid in sorted(rows):
        if wid not in moved:
            by_file[witnesses.file_for(wid)].append(rows[wid])
    head = ["The witness registry (tools/bib/witnesses.py, its STYLE; the memo, notes/extensions/memos/witnesses.md). "
            "Kept by hand or agent."]
    for path in witnesses.files():
        if path not in by_file:
            os.remove(path)
    for path, rs in by_file.items():
        store.dump_yaml(rs, path, header=head)
    for card, es in edges.items():
        changed = False
        for ed in es:
            if ed.get("of") in moved:
                ed["of"], changed = moved[ed["of"]], True
        if changed:
            store.dump_yaml(es, os.path.join(witnesses.BYWORK, card[2:] + ".yaml"), header=[
                f"{card}: its edges, page and note to the witness its text rests on (tools/bib/witnesses.py)."])
    s = store.Series(ROOT)
    n = 0
    for lst in s.lists.values():
        for sec in lst.walk():
            hit = False
            for e in sec.entries:
                src = e.get("src") or {}
                rows_ = src.get("rows") or []
                new = [re.sub(r"^via (x\.\S+):", lambda m: f"via {moved.get(m.group(1), m.group(1))}:", r) for r in rows_]
                if new != rows_:
                    src["rows"], hit, n = new, True, n + 1
            if hit:
                s.save_section(sec)
    print(f"{len(moved)} joins; {n} entries' via rows rewritten")


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
