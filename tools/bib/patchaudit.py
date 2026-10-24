"""Patches read together before any is merged (the owner's rule, Oct. 24, 2026: "Be sure we do before letting one
agent's work overwrite another's, sight-unseen").

    ./bib audit-patches inbox/*.yaml      what the pending patches would do to one another and to the tree

The merge (tools/bib/merge.py) is three-way field by field: a field two patches both change becomes a conflict
recorded in the entry, never a silent overwrite, so long as each edit names its base. It cannot do more: it cannot
join two notes that each add a book's pages, nor tell two events given one id from one event given two. This reads
every pending patch before the first is merged and lists what a person must settle by hand:

STYLE
 1. Refused outright: an edit or delete without a base (the merge would let the last writer win); an edit whose base
    is in neither the tree nor git's history (the merge would treat every field it names as a conflict); one patch
    editing an entry twice (its second edit would conflict with its first).
 2. Overlaps: every entry two or more patches edit, with the fields each sets. Where two set the same field, the
    merge records a conflict and the reconciling is by hand: both books' pages kept, both moves out of "To check:",
    both Checks (CLAUDE.md, "Hard and soft").
 3. Collisions: a new id two patches add (two events under one id, or one event twice); a new id already in the tree.
 4. Neighbors: new entries on the same date and thread, from two patches or from a patch and the tree: likely the same
    event written twice, to be folded into one entry with both cites, or told apart in their wording.
"""
import collections
import os

from . import store


def load(paths):
    out = []
    for p in paths:
        try:
            d = store.load_yaml(p) or {}
        except Exception as x:                  # noqa: BLE001: a patch that does not load is itself a finding
            out.append((p, None, str(x)))
            continue
        out.append((p, d, None))
    return out


def audit(series, paths):
    """The findings, as lines grouped under headings (STYLE 1-4)."""
    from .merge import find_base
    patches = load(paths)
    refused, overlaps, collide, near = [], [], [], []
    edits = collections.defaultdict(list)              # id -> [(patch, fields)]
    adds = collections.defaultdict(list)               # id -> [(patch, entry)]
    by_day = collections.defaultdict(list)             # (date, thread) -> [(patch, id)]
    for path, d, err in patches:
        name = os.path.basename(path)
        if d is None:
            refused.append(f"{name}: does not load ({err})")
            continue
        seen = collections.Counter()
        for op in d.get("ops") or []:
            (kind, body), = op.items()
            if kind in ("edit", "delete"):
                eid = body.get("id")
                seen[eid] += 1
                if not body.get("base"):
                    refused.append(f"{name}: {kind} {eid} has no base")
                elif series.get(eid) and find_base(series, eid, body["base"]) is None:
                    refused.append(f"{name}: {kind} {eid}: base {body['base']} not in the tree or git history")
                if kind == "edit":
                    edits[eid].append((name, sorted((body.get("set") or {}).keys()) + sorted(body.get("unset") or [])))
            elif kind == "add":
                e = body.get("entry") or {}
                adds[e.get("id")].append((name, e))
                if e.get("date") and e.get("thread"):
                    by_day[(str(e["date"]), e["thread"])].append((name, e.get("id")))
        for eid, n in seen.items():
            if n > 1:
                refused.append(f"{name}: edits {eid} {n} times")
    for eid, xs in sorted(edits.items()):
        if len({p for p, _ in xs}) > 1:
            fields = collections.Counter(f for _, fs in xs for f in fs)
            same = sorted(f for f, n in fields.items() if n > 1)
            overlaps.append(f"{eid}: " + "; ".join(f"{p} ({', '.join(fs)})" for p, fs in xs)
                            + (f"  SAME FIELD: {', '.join(same)}" if same else ""))
    for eid, xs in sorted(adds.items()):
        if len(xs) > 1:
            collide.append(f"{eid}: added by " + ", ".join(p for p, _ in xs))
        if series.get(eid):
            collide.append(f"{eid}: added by {xs[0][0]}, but the tree has it")
    lst = series.lists.get("cal")
    tree = collections.defaultdict(list)
    if lst:
        for _, e in lst.entries():
            if e.get("thread"):
                tree[(str(e.get("date")), e["thread"])].append(e["id"])
    for key, xs in sorted(by_day.items()):
        old = [i for i in tree.get(key, []) if i not in {x for _, x in xs}]
        if len({p for p, _ in xs}) > 1 or old:
            near.append(f"{key[0]} {key[1]}: " + ", ".join(f"{i} ({p})" for p, i in xs)
                        + (f"; in the tree: {', '.join(old)}" if old else ""))
    return [("Refused (STYLE 1)", refused), ("Entries edited by two or more patches (STYLE 2)", overlaps),
            ("Ids added twice or already present (STYLE 3)", collide),
            ("New entries on a date and thread already taken (STYLE 4)", near)]


def report(series, paths):
    out = []
    for head, lines in audit(series, paths):
        out.append(f"== {head}: {len(lines)}")
        out += ["  " + x for x in lines]
    return "\n".join(out)
