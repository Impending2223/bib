"""A patch held to the rules before it is handed in (the owner's request, Oct. 30, 2026; notes/extensions/memos/volume.md,
§6): the reader runs it, so the patch arrives clean and the merger reads only the conflicts and a sample.

    ./bib patch-check inbox/<patch>.yaml      errors (the patch is refused) and warnings; exit 1 on an error

STYLE
 1. Every op a known kind (tools/bib/merge.py OPS, tools/bib/addops.py).
 2. `edit` and `delete`: patchaudit's refusals (no base; a base the tree and git do not know; an edit dropping what the
    note now holds; one entry edited twice). An `edit` that only adds to `n`, `src`, `tags` or `also` is a warning:
    write it as additive ops (addops), which need no base and do not collide.
 3. `add`: the entry's id, date, thread, `c` and `n`; not in the tree; claimed in the ledger (tools/bib/ledger.py) by
    this patch. A new entry on a day and thread the tree or the ledger already holds is a warning (the same event?).
 4. Additive ops: each tried on the entry as it stands (addops.FNS): an op the entry refuses is an error. An op on an id
    the tree lacks is an error, unless the ledger claims it (then deferred at the merge, addops STYLE 7).
 5. A patch written before the ledger (`--legacy`): an add the ledger does not claim is a warning, not an error.
 6. The claim maps: the patch applied in memory, `claims.problems` before and after; an error it adds is an error here.
"""
import collections
import os

from . import store


def check(series, path, legacy=False):
    from . import addops, claims, ledger, merge, patchaudit
    errors, warnings = [], []
    try:
        d = store.load_yaml(path) or {}
    except Exception as x:                          # noqa: BLE001: a patch that does not load is the finding
        return [f"does not load: {x}"], []
    name = d.get("patch") or os.path.basename(path)
    claimed = {r["id"]: r for r in ledger.rows()}
    ops = d.get("ops") or []
    added = set()
    by_day = collections.defaultdict(list)
    lst = series.lists.get("cal")
    if lst:
        for _, e in lst.entries():
            by_day[(str(e.get("date")), e.get("thread"))].append(e["id"])
    for r in claimed.values():
        if not series.get(r["id"]):
            by_day[(r["date"], r["thread"])].append(r["id"])
    for k, op in enumerate(ops):
        if not isinstance(op, dict) or len(op) != 1:
            errors.append(f"op {k}: one kind an op")
            continue
        (kind, body), = op.items()
        body = body or {}
        if kind not in merge.OPS:
            errors.append(f"op {k}: unknown kind {kind!r}")
            continue
        eid = body.get("id") or (body.get("entry") or {}).get("id")
        if kind == "add":
            e = body.get("entry") or {}
            miss = [f for f in ("id", "date", "thread", "c", "n") if not e.get(f)]
            if miss:
                errors.append(f"add {eid}: no {', '.join(miss)}")
            if series.get(eid):
                errors.append(f"add {eid}: the tree has it")
            if eid not in claimed:
                (warnings if legacy else errors).append(f"add {eid}: not claimed in the ledger (./bib ledger add ...)")
            elif claimed[eid]["patch"] not in (name, os.path.basename(path)):
                errors.append(f"add {eid}: claimed by {claimed[eid]['patch']}, not this patch")
            others = [i for i in by_day.get((str(e.get("date")), e.get("thread")), []) if i != eid]
            if others:
                warnings.append(f"add {eid}: {e.get('date')} {e.get('thread')} also holds {', '.join(others)} (one event?)")
            added.add(eid)
        elif kind in addops.FNS:
            hit = series.get(eid)
            if not hit:
                if eid not in claimed and eid not in added:
                    errors.append(f"{kind} {eid}: no such entry, and not in the ledger")
                continue
            _, err = addops.FNS[kind](hit[2], body)
            if err:
                errors.append(f"{kind} {eid}: {err}")
        elif kind == "edit":
            sets = set((body.get("set") or {}).keys())
            if sets and sets <= {"n", "src", "tags", "also"} and not body.get("unset"):
                warnings.append(f"edit {eid}: sets only {', '.join(sorted(sets))}; if it only adds, write additive ops "
                                "(cite, to-check, check, src, names, also: tools/bib/addops.py)")
    for head, lines in patchaudit.audit(series, [path])[:1]:
        errors += lines
    # STYLE 6: the claim maps, before and after
    before = {(i, m) for i, m in claims.problems(series)[0]}
    rep = merge.Report()
    merge.apply_patch(series, d, name, rep, dry=True)
    addops.join_clean(series, name, save=False)          # as the rolling merge will join them
    after = {(i, m) for i, m in claims.problems(series)[0]}
    errors += [f"claims {i}: {m}" for i, m in sorted(after - before)]
    for l in rep.lines:
        if l.startswith("error"):
            msg = l.split(None, 1)[1]
            if not any(msg.split(": ", 1)[-1] in x for x in errors):
                errors.append(msg)
    return errors, warnings


def report(series, path, legacy=False):
    errors, warnings = check(series, path, legacy)
    out = [f"== {os.path.basename(path)}: {len(errors)} errors, {len(warnings)} warnings"]
    out += ["  error  " + x for x in errors] + ["  warn   " + x for x in warnings]
    return "\n".join(out), bool(errors)
