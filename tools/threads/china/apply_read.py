"""Apply the China entries read one by one after the re-threading (notes/briefs/china-threads-read-a.md to -g.md;
their audits, notes/briefs/china-threads-read-audit-a.md to -g.md; notes/owner-rulings.md, 59 and 61).

    python3 tools/threads/china/apply_read.py --dry-run a b ...   # what it would do; writes nothing
    python3 tools/threads/china/apply_read.py a b ...             # writes the entries

Each letter names a batch, notes/threads/read/batch-<letter>.tsv (id, primary, also, basis), as its audit left it.
A batch is refused unless its audit, notes/threads/read/batch-<letter>-audit.md, is there.

For each row: `thread:` becomes the primary thread, and `also:` becomes the row's list, in its order, with these
taken out: `china-leadership` and `china` where the entry moves (as on Nov. 25: an entry that moves keeps neither);
the Center's daily work (ruling 59: never a secondary thread); the primary itself. Nothing else in an entry changes;
no id changes.

Refused, and then nothing at all is written: a row whose entry is missing; an entry whose present thread is not
`china-leadership` (the thread every batch was drawn from), unless it is already as this script would leave it (so
the script may be run again); a slug th.yaml lacks; a thread beside its own parent or child; two rows for one id; a
row of the ids list with no row in the batch.
"""
import collections
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)

from tools.bib import store  # noqa: E402

READ = os.path.join(ROOT, "notes", "threads", "read")
FROM = "china-leadership"
BASE = ("china-leadership", "china")
NEVER_SECOND = {"china-center"}


def line_of(slug, threads):
    out, seen = [], set()
    while slug and slug not in seen:
        out.append(slug)
        seen.add(slug)
        slug = (threads.get(slug) or {}).get("parent")
    return out


def rows_of(letter):
    with open(os.path.join(READ, f"batch-{letter}.tsv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    with open(os.path.join(READ, f"batch-{letter}-ids.tsv"), encoding="utf-8") as f:
        ids = [r["id"] for r in csv.DictReader(f, delimiter="\t")]
    return rows, ids


def plan_entry(e, r):
    prim = r["primary"].strip()
    also = [t.strip() for t in (r.get("also") or "").split(",") if t.strip()]
    out, dropped = [], collections.Counter()
    for t in also:
        if t == prim or t in out:
            continue
        if t in NEVER_SECOND:
            dropped[t] += 1
            continue
        if prim != FROM and t in BASE:
            dropped[t] += 1
            continue
        out.append(t)
    return prim, out, dropped


def main(argv):
    dry = "--dry-run" in argv
    letters = [a for a in argv if a != "--dry-run"]
    if not letters:
        sys.exit(__doc__.split("\n\n")[1])
    series = store.Series(ROOT)
    cal = series.lists["cal"]
    threads = cal.threads()
    where = {e["id"]: (sec, e) for sec, e in cal.entries() if "when" in e}
    refused, plan, seen = [], [], set()
    counts, prim_n, dropped_n, also_n = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    for L in letters:
        if not os.path.exists(os.path.join(READ, f"batch-{L}-audit.md")):
            refused.append(f"batch {L}: no audit")
            continue
        rows, ids = rows_of(L)
        missing = set(ids) - {r["id"] for r in rows}
        for m in sorted(missing):
            refused.append(f"batch {L}: {m}: no row")
        for r in rows:
            eid = r["id"]
            if eid in seen:
                refused.append(f"{eid}: two rows")
                continue
            seen.add(eid)
            if eid not in where:
                refused.append(f"{eid}: no such entry")
                continue
            sec, e = where[eid]
            prim, also, dropped = plan_entry(e, r)
            bad = [t for t in [prim] + also if t not in threads]
            if bad:
                refused.append(f"{eid}: no thread {bad[0]!r}")
                continue
            every = [prim] + also
            near = [(a, b) for a in every for b in every if a != b and b in line_of(a, threads)[1:]
                    and not (a == FROM and b == "china")]
            if near:
                refused.append(f"{eid}: {near[0][0]!r} beside its parent {near[0][1]!r}")
                continue
            old_also = list(e.get("also") or [])
            if e["thread"] == prim and old_also == also:
                counts["already"] += 1
                continue
            if e["thread"] != FROM:
                refused.append(f"{eid}: its thread is {e['thread']!r}, not {FROM!r}")
                continue
            counts["moved" if prim != FROM else "kept"] += 1
            prim_n[prim] += 1
            dropped_n.update(dropped)
            for t in also:
                if t not in old_also:
                    also_n[t] += 1
            plan.append((sec, e, prim, also))
    print(f"batches {' '.join(letters)}: rows {len(seen)}; moved {counts['moved']}; kept in {FROM} {counts['kept']}; "
          f"already applied {counts['already']}")
    print("\n| primary | entries |\n|---|---:|")
    for t, n in prim_n.most_common():
        print(f"| `{t}` | {n} |")
    print("\nalso added: " + ", ".join(f"`{t}` {n}" for t, n in also_n.most_common()))
    print("taken out of the rows' also: " + (", ".join(f"`{t}` {n}" for t, n in dropped_n.most_common()) or "none"))
    for msg in refused[:40]:
        print("REFUSED", msg)
    if refused:
        print(f"{len(refused)} refused: nothing written")
        return 1
    if dry:
        print("dry run: nothing written")
        return 0
    for sec, e, prim, also in plan:
        e["thread"] = prim
        if also:
            e["also"] = also
        else:
            e.pop("also", None)
    touched = {id(sec): sec for sec, *_ in plan}
    for sec in touched.values():
        series.save_section(sec)
    print(f"written: {len(plan)} entries in {len(touched)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
