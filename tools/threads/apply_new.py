"""Apply the placings of new threads read entry by entry (notes/owner-rulings.md, 62; the readers' briefs,
notes/briefs/threads-new-*.md; their audits, notes/threads/new/*-audit.md).

    python3 tools/threads/apply_new.py --dry-run notes/threads/new/jd.tsv notes/threads/new/cm-a.tsv ...
    python3 tools/threads/apply_new.py notes/threads/new/jd.tsv ...

Each TSV has the header `id primary also basis`: the entry's thread as it should be, and its whole `also:` list.
A row is read against the entry as it now stands: what the row adds to `also:`, what it takes out of it, and whether
it changes `thread:`. Where two TSVs hold the same entry, their changes are taken together: every thread either adds,
less every thread either takes out; a change of `thread:` in one stands unless the other changes it otherwise, and
then nothing is written. Nothing else in an entry changes; no id changes.

Refused, and then nothing at all is written: a TSV whose audit (`<name>-audit.md`, or for a batch of several,
the audit that names it) is missing; a row whose entry is missing; a slug th.yaml lacks; a thread newly put beside its own
parent or child (a pair the entry already held stays); two TSVs that set one entry's `thread:` differently.
"""
import collections
import csv
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)

from tools.bib import store  # noqa: E402


def line_of(slug, threads):
    out, seen = [], set()
    while slug and slug not in seen:
        out.append(slug)
        seen.add(slug)
        slug = (threads.get(slug) or {}).get("parent")
    return out


def audited(path):
    d, name = os.path.split(path)
    name = name[:-4]
    if os.path.exists(os.path.join(d, f"{name}-audit.md")):
        return True
    for b in glob.glob(os.path.join(ROOT, "notes", "briefs", "threads-new-audit-*.md")):
        out = os.path.basename(b)[len("threads-new-audit-"):-3]
        if f"{name}-ids.tsv" in open(b, encoding="utf-8").read() and os.path.exists(os.path.join(d, f"{out}-audit.md")):
            return True             # the audit brief names the batch, and its audit is written
    for a in glob.glob(os.path.join(d, "*-audit.md")):
        if f"`{name}.tsv`" in open(a, encoding="utf-8").read() or f"{name}.tsv" in open(a, encoding="utf-8").read():
            return True
    return False


def main(argv):
    dry = "--dry-run" in argv
    paths = [a for a in argv if a != "--dry-run"]
    if not paths:
        sys.exit(__doc__.split("\n\n")[1])
    series = store.Series(ROOT)
    cal = series.lists["cal"]
    threads = cal.threads()
    where = {e["id"]: (sec, e) for sec, e in cal.entries() if "when" in e}
    refused = []
    want = {}                      # id -> {"thread": set of new primaries, "add": set, "drop": set}
    for p in paths:
        if not audited(p):
            refused.append(f"{p}: no audit")
            continue
        with open(p, encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                eid = (r.get("id") or "").strip()
                if eid not in where:
                    refused.append(f"{p}: {eid}: no such entry")
                    continue
                e = where[eid][1]
                prim = (r.get("primary") or "").strip()
                also = [t.strip() for t in (r.get("also") or "").split(",") if t.strip()]
                bad = [t for t in [prim] + also if t not in threads]
                if bad:
                    refused.append(f"{p}: {eid}: no thread {bad[0]!r}")
                    continue
                w = want.setdefault(eid, {"thread": set(), "add": set(), "drop": set()})
                old = [e["thread"]] + list(e.get("also") or [])
                if prim != e["thread"]:
                    w["thread"].add(prim)
                new = set([prim] + also)
                w["add"] |= new - set(old)
                w["drop"] |= set(old) - new
    plan, counts = [], collections.Counter()
    for eid, w in want.items():
        sec, e = where[eid]
        if len(w["thread"]) > 1:
            refused.append(f"{eid}: two new threads {sorted(w['thread'])}")
            continue
        prim = next(iter(w["thread"])) if w["thread"] else e["thread"]
        old_also = list(e.get("also") or [])
        also = [t for t in old_also if t not in w["drop"] and t != prim]
        if e["thread"] != prim and e["thread"] not in w["drop"] and e["thread"] not in also:
            also.insert(0, e["thread"])   # the old primary, which the row keeps, goes into also
        for t in sorted(w["add"]):
            if t != prim and t not in also:
                also.append(t)
        every = [prim] + also
        had = set([e["thread"]] + old_also)
        near = [(a, b) for a in every for b in every if a != b and b in line_of(a, threads)[1:]
                and not (a in had and b in had)]   # a pair the entry already held is the calendar's own
        if near:
            refused.append(f"{eid}: {near[0][0]!r} beside its parent {near[0][1]!r}")
            continue
        if prim == e["thread"] and also == old_also:
            counts["unchanged"] += 1
            continue
        counts["thread changed" if prim != e["thread"] else "also changed"] += 1
        plan.append((sec, e, prim, also))
    added = collections.Counter(t for _, e, p, a in plan for t in a if t not in (e.get("also") or []))
    print(f"entries read {len(want)}; thread changed {counts['thread changed']}; also changed "
          f"{counts['also changed']}; unchanged {counts['unchanged']}")
    print("added to also: " + ", ".join(f"`{t}` {n}" for t, n in added.most_common(12)))
    for m in refused[:40]:
        print("REFUSED", m)
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
