"""The owner's editing desk, its bridge to the series (the owner's request, Oct. 29, 2026; the hand-off of Nov. 1, item 0).

The desk (https://claude.ai/artifact/G7GDP7qa9yYsfqJ2wGPcCq) keeps one document an edit in its store, `edits/<id>`:
{kind: entry | thread | new, target, base (the rev the desk showed), fields, status: draft | ready | merged | needs-you,
reason, theirs, updated}. At each 5 p.m. resume, or when the owner says "merge my edits":

  1. read the store: ArtifactData list, collection "edits", out_dir DUMP (each document a file, DUMP/edits/<id>.json)
  2. python3 -I tools/desk/bridge.py patch DUMP          inbox/<date>-owner-desk.yaml from the Ready edits (new entries
                                                         claimed in the ledger), DUMP/plan.json
  3. ./bib merge --auto inbox/<date>-owner-desk.yaml     then ./bib check
  4. python3 -I tools/desk/bridge.py after DUMP          each edit's outcome: merged, or needs-you (a conflict: the
                                                         series' text kept, `./bib resolve ID --take theirs`, both
                                                         texts sent back); DUMP/writeback.json, the batch for ArtifactData
  5. ArtifactData batch from writeback.json; commit, push, PR to main; republish the desk's data
     (python3 -I tools/desk/export.py DIR, the Artifact publish with the same files) so the next edit's base is current.

STYLE
1. Only Ready edits go in; drafts stay drafts. An edit's fields are the owner's whole text for each field it names: a
   field set empty is unset (`time_approx` false likewise).
2. An entry or thread edit is an `edit` op with the desk's base, so the merge is three-way: what the owner changed and
   nobody else did applies; a field both changed is a conflict, which this bridge settles for the series' text and hands
   back to the owner with both texts and the reason. Nothing of the owner's is lost: the edit stays in the store.
3. A new entry gets the series' id, cal.<date>.<thread> (-2 if taken), claimed in the ledger by this patch, and is
   placed by date as any added entry is.
"""
import datetime
import glob
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from tools.bib import ledger, store  # noqa: E402

LISTF = {"also", "tags", "follows", "see_also"}


def load_dump(dump):
    out = []
    for p in sorted(glob.glob(os.path.join(dump, "edits", "*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        doc_id = d.get("id") or os.path.splitext(os.path.basename(p))[0]
        body = d.get("data", d)
        out.append((doc_id, d.get("version"), body))
    return out


def empty(v):
    return v in (None, "", [], False)


def clean(k, v):
    if k in LISTF:
        return [str(x).strip() for x in (v or []) if str(x).strip()]
    if isinstance(v, str):
        return v.strip() if k not in ("c", "n") else v.strip().replace("\r\n", "\n")
    return v


def patch(dump, day=None):
    day = day or datetime.date.today().isoformat()
    name = f"{day}-owner-desk"
    series = store.Series(ROOT)
    ops, plan = [], {}
    for doc_id, version, e in load_dump(dump):
        if e.get("status") != "ready":
            continue
        f = {k: clean(k, v) for k, v in (e.get("fields") or {}).items()}
        if e.get("kind") in ("entry", "thread"):
            tid = e.get("target") or doc_id
            if not series.get(tid):
                plan[doc_id] = {"version": version, "id": tid, "fail": f"{tid} is no longer in the series"}
                continue
            op = {"id": tid, "base": e.get("base")}
            sets = {k: v for k, v in f.items() if not empty(v)}
            unsets = [k for k, v in f.items() if empty(v)]
            if sets:
                op["set"] = sets
            if unsets:
                op["unset"] = unsets
            if sets or unsets:
                ops.append({"edit": op})
                plan[doc_id] = {"version": version, "id": tid, "fields": sorted(f)}
        elif e.get("kind") == "new":
            need = [k for k in ("date", "thread", "c") if empty(f.get(k))]
            if need:
                plan[doc_id] = {"version": version, "fail": "the entry needs " + ", ".join(need)}
                continue
            base = f"cal.{f['date']}.{store.slug(f['thread'], 6)}"
            eid, n = base, 2
            while series.get(eid) or ledger.named(eid):
                eid, n = f"{base}-{n}", n + 1
            err = ledger.add(series, f["date"], f["thread"], eid, " ".join(str(f["c"]).split()[:8]), name)
            if err:
                plan[doc_id] = {"version": version, "fail": err}
                continue
            entry = {"id": eid}
            for k in ("when", "date", "thread", "also", "c", "n", "tags"):
                if not empty(f.get(k)):
                    entry[k] = f[k]
            entry.setdefault("n", "Check: sources.")
            ops.append({"add": {"entry": entry}})
            plan[doc_id] = {"version": version, "id": eid, "fields": sorted(entry), "new": True}
    path = os.path.join(ROOT, "inbox", name + ".yaml")
    if ops:
        store.dump_yaml({"patch": name, "by": "the owner, at the desk", "ops": ops}, path,
                        header=["The owner's edits from the desk (tools/desk/bridge.py). Merge: ./bib merge --auto."])
    json.dump(plan, open(os.path.join(dump, "plan.json"), "w"), indent=1, ensure_ascii=False)
    print(f"{len(ops)} ops -> {path if ops else '(none)'}; {sum('fail' in p for p in plan.values())} refused")


def after(dump):
    plan = json.load(open(os.path.join(dump, "plan.json"), encoding="utf-8"))
    series = store.Series(ROOT)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    writes = []
    for doc_id, p in plan.items():
        upd = {}
        if "fail" in p:
            upd = {"status": "needs-you", "reason": p["fail"]}
        else:
            hit = series.get(p["id"])
            e = hit[2] if hit else None
            if e is None:
                upd = {"status": "needs-you", "reason": "the merge did not land it: ask Claude"}
            else:
                mine = [c for c in e.get("conflict") or [] if "owner-desk" in str(c.get("from", ""))]
                if mine:
                    theirs = {c["field"]: c.get("ours") for c in mine if c.get("field")}   # ours: the tree's
                    for c in mine:
                        if c.get("field"):
                            subprocess.run([os.path.join(ROOT, "bib"), "resolve", p["id"], "--take", "ours",
                                            "--field", c["field"]], cwd=ROOT, check=False)
                    upd = {"status": "needs-you", "theirs": theirs,
                           "reason": "Changed in the series since you opened it: " + ", ".join(sorted(theirs))
                                     + ". The series' text is kept; yours is here. Edit and mark Ready again."}
                else:
                    upd = {"status": "merged", "mergedAt": now, "reason": None}
                    if p.get("new"):
                        upd["merged_id"] = p["id"]
        w = {"op": "update", "collection": "edits", "doc_id": doc_id, "data": upd}
        if p.get("version"):
            w["if_version"] = p["version"]
        writes.append(w)
    json.dump(writes, open(os.path.join(dump, "writeback.json"), "w"), indent=1, ensure_ascii=False)
    print(f"{len(writes)} write-backs -> {os.path.join(dump, 'writeback.json')}")


if __name__ == "__main__":
    cmd, dump = sys.argv[1], sys.argv[2]
    {"patch": lambda: patch(dump, sys.argv[3] if len(sys.argv) > 3 else None), "after": lambda: after(dump)}[cmd]()
