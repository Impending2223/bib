"""A patch held to the rules before it is handed in (the owner's request, Oct. 30, 2026; notes/extensions/memos/volume.md,
§6): the reader runs it, so the patch arrives clean and the merger reads only the conflicts and a sample.

    ./bib patch-check inbox/<patch>.yaml      errors (the patch is refused) and warnings; exit 1 on an error

STYLE
 1. Every op a known kind (tools/bib/merge.py OPS, tools/bib/addops.py).
 2. `edit` and `delete`: patchaudit's refusals (no base; a base the tree and git do not know; an edit dropping what the
    note now holds; one entry edited twice). A base written unquoted, all digits (69735970), loads as a number: it
    is read back as the rev (merge._base), and accepted where it is one, with a warning to quote it. An `edit` that only adds to `n`, `src`, `tags` or `also` is a warning:
    write it as additive ops (addops), which need no base and do not collide.
 3. `add`: the entry's id, date, thread, `c` and `n`; not in the tree; claimed in the ledger (tools/bib/ledger.py) by
    this patch. A new entry on a day and thread the tree or the ledger already holds is a warning (the same event?).
 4. Additive ops: each tried on the entry as it stands (addops.FNS): an op the entry refuses is an error. An op on an id
    the tree lacks is an error, unless the ledger claims it (then deferred at the merge, addops STYLE 7).
 5. A patch written before the ledger (`--legacy`): an add the ledger does not claim is a warning, not an error.
 6. The claim maps: the patch applied in memory, `claims.problems` before and after; an error it adds is an error here.
 7. `add` of a thread (`cal.thread.<slug>`, th.yaml): not a dated entry, so neither date, `c`, `n` nor the ledger; its
    name (`s`), not in the tree, its `parent` a thread of the tree or added earlier in the patch, and its place
    (`section` the threads section, `after`); `check` [thread-order] holds the order once merged.
 8. The entries the patch adds, edits or adds to, as they stand after it (applied in memory, as in 6), held to
    `./bib check`'s rules for an entry, by its own functions, so a patch that passes here passes `check` once merged:
    check.entry_problems (`when` against `date`, check.when_matches_date; `thread`, `also` and `to` naming a thread's
    slug, not an alias; every `[[id]]` an entry, every `[[w.id]]` a card; the date within the section the entry lands
    in, January 1966's two sections among them), witnesses.problems (a `via x.` row's witness reached from an item of
    the note; a variant's unit and witness) and claims.problems (6: a `src` row naming what the note prints). An error
    the tree already had is not the patch's. Each message says the fix. A conflict the merge leaves is a warning.
 9. `add` of an entry of another list (a Part III name, `kja.who.<key>`; a work): not a calendar entry, so neither
    date, thread, `n` nor the ledger (the ledger claims a day and thread); its id, `s` or `c`, its `section`, not in
    the tree nor added twice; the rest is 8's (the entry as check holds it, once placed).
"""
import collections
import os

from . import store


def check(series, path, legacy=False):
    from . import addops, claims, ledger, merge, patchaudit, witnesses
    from . import check as chk
    errors, warnings = [], []
    try:
        d = store.load_yaml(path) or {}
    except Exception as x:                          # noqa: BLE001: a patch that does not load is the finding
        return [f"does not load: {x}"], []
    name = d.get("patch") or os.path.basename(path)
    claimed = {r["id"]: r for r in ledger.rows()}
    ops = d.get("ops") or []
    added = set()
    from .merge import patch_parts
    parts = patch_parts(ops)
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
        if kind == "add" and lst and str(eid or "").startswith(f"{lst.key}.thread."):
            # a thread (th.yaml): its name, and its parent a thread the tree or the patch holds (STYLE 7)
            e = body.get("entry") or {}
            if not e.get("s"):
                errors.append(f"add {eid}: a thread takes s, its name")
            if series.get(eid):
                errors.append(f"add {eid}: the tree has it")
            par = e.get("parent")
            if par and par not in lst.threads() and f"{lst.key}.thread.{par}" not in added:
                errors.append(f"add {eid}: parent {par!r} is no thread of the tree or the patch")
            if body.get("section") != lst.data.get("threads_section", "th") or not body.get("after"):
                errors.append(f"add {eid}: a thread goes in the threads section, after the thread it follows")
            added.add(eid)
        elif kind == "add" and not (lst and str(eid or "").startswith(f"{lst.key}.")):
            # an entry of a list, not the calendar (a Part III name, a work): neither date, thread nor the ledger
            # (STYLE 9); its id, its `s` or `c`, its section, not in the tree; check.entry_problems holds the rest (8)
            e = body.get("entry") or {}
            if not e.get("id"):
                errors.append(f"add {eid}: no id")
            if not (e.get("s") or e.get("c")):
                errors.append(f"add {eid}: no s or c")
            if not body.get("section"):
                errors.append(f"add {eid}: no section")
            if series.get(eid) or eid in added:
                errors.append(f"add {eid}: the tree has it" if series.get(eid) else f"add {eid}: added twice")
            added.add(eid)
        elif kind == "add":
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
            others = [i for i in by_day.get((str(e.get("date")), e.get("thread")), []) if i != eid
                      and (i, eid) not in parts and (eid, i) not in parts]   # a parent and its subentries: no duplicate
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
        if kind in ("edit", "delete") and body.get("base") is not None and not isinstance(body["base"], str):
            # YAML reads an all-digit rev as a number (STYLE 2): read back as the rev, merge._base; quote it
            warnings.append(f"{kind} {eid}: base {body['base']!r} loads as a number; quote it: base: "
                            f"'{merge._base(body['base'])}'")
        if kind == "edit":
            sets = set((body.get("set") or {}).keys())
            if sets and sets <= {"n", "src", "tags", "also"} and not body.get("unset"):
                warnings.append(f"edit {eid}: sets only {', '.join(sorted(sets))}; if it only adds, write additive ops "
                                "(cite, to-check, check, src, names, also: tools/bib/addops.py)")
    for head, lines in patchaudit.audit(series, [path])[:1]:
        errors += lines
    # STYLE 6 and 8: the claim maps, the witnesses, and the entries the patch touches, before and after
    touched = []
    for op in ops:
        if isinstance(op, dict) and len(op) == 1:
            (kind, body), = op.items()
            eid = (body or {}).get("id") or ((body or {}).get("entry") or {}).get("id")
            if eid and kind not in ("delete", "combine") and eid not in touched:
                touched.append(eid)

    def entry_errs():
        out = set()
        for eid in touched:
            hit = series.get(eid)
            if hit:
                out |= {(eid, lvl, msg) for lvl, msg, _ in chk.entry_problems(series, *hit) if lvl == chk.ERROR}
        return out
    before = {(i, m) for i, m in claims.problems(series)[0]}
    wbefore = set(witnesses.problems(series)[0])
    ebefore = entry_errs()
    rep = merge.Report()
    merge.apply_patch(series, d, name, rep, dry=True)
    addops.join_clean(series, name, save=False)          # as the rolling merge will join them
    after = {(i, m) for i, m in claims.problems(series)[0]}
    errors += [f"claims {i}: {m}" for i, m in sorted(after - before)]
    errors += [f"witnesses {i}: {m}" for i, m in sorted(set(witnesses.problems(series)[0]) - wbefore, key=str)]
    for eid, lvl, msg in sorted(entry_errs() - ebefore):
        if msg.startswith("unresolved merge conflict"):     # the merge's to settle, not the patch's to refuse
            cs = (series.get(eid)[2].get("conflict") or []) if series.get(eid) else []
            what = "; ".join(f"a duplicate of {', '.join(c.get('of') or [])}?" if c.get("kind") == "duplicate"
                             else f"a conflict on {c.get('field')}" for c in cs if isinstance(c, dict))
            warnings.append(f"{eid}: {what or 'a conflict'} at the merge (./bib resolve {eid} --take ...; keep, for a duplicate that is distinct)")
        else:
            errors.append(f"{eid}: {msg}")
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
