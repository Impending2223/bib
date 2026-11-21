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
10. R25a, the fields (the owner, Nov. 19, 2026: "Could we fix that? Permanently?"): each calendar `add`, as the dry run
    leaves it, held to tools/bib/fields.py: a clock time or a part of the day without `time` or `time_range`
    [fields-time], a loose date's position merge cannot set without `at` [fields-at] (errors); an hour that recurs
    [fields-time-habitual] and a gazetteer place in `c` without `place` [fields-place] (warnings: a fifth of the
    place hits name a subject, not the scene), the place findings the first few and their count (`./bib fields
    --patch P` lists them all). Tags `ok:fields-time`, `ok:fields-at`, `ok:fields-place` silence each. Not on cites
    or edits.
11. `place:` set by an `add` or an `edit` (`set: {place: ...}`), as the dry run leaves the entry, held to check's
    [place] (places.entry_problems): every key in the gazetteer, sources/places.yaml, or added by the patch's own
    `place-key` ops (places.PENDING); a single key or a list of at most two. The `place` additive op holds its own
    (addops.place).
12. The day's order (dayorder.problems, check's day rules) on the calendar as the dry run leaves it: a `follows` naming
    nothing, itself, or an entry of another day (an exact day: two month- or year-dated entries cannot follow one
    another), a time before the one it follows, a cycle. Held on the whole calendar, not the touched ids: a cycle is
    reported on whichever end the search meets last, and an entry following one the patch moves or deletes is not
    the patch's. An error the tree already had is not the patch's.
13. The calendar's `name:` tags as the dry run leaves it, held to check's lives rule (lives.problems): each the key
    of a person the series holds (lives.everyone, FRUS's persons among them, and the forms joined in another's
    entry, frus-alias). A tag the patch adds, and a tag the tree has that a patch changing or dropping a name entry
    leaves unheld; a tag the tree already left unheld is not the patch's. The lives cache is cleared before each
    build (the series has changed under it); who the series held before is built only for a patch with an op
    outside the calendar.
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
    from . import places
    places.PENDING.clear()
    for op in ops:                       # the patch's gazetteer rows, for its place ops (places.py, STYLE 3)
        if isinstance(op, dict) and "place-key" in op:
            b = op["place-key"] or {}
            errs = places.row_problems({k: b.get(k) for k in ("key", "name", "zone")})
            cur = places.get(str(b.get("key")))
            if cur is not None and not b.get("fix") and any(cur.get(x) != b.get(x) for x in ("name", "zone") if b.get(x)):
                errs.append(f"{b.get('key')}: the gazetteer has it ({cur.get('name')}, {cur.get('zone')}); fix: true to change it")
            if not (b.get("st") or b.get("in")):
                errs.append(f"{b.get('key')}: give st (a U.S. State) or in (a polity)")
            errors += [f"place-key {m}" for m in errs]
            places.PENDING[str(b.get("key"))] = dict(b)
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
        errors += [f"{kind} {i}: {m}" for i, m in merge.op_problems(kind, body)]   # bookkeeping fields (merge.py)
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
                if lst is not None and hit[0] is lst:      # STYLE 11: the place keys an add or an edit sets
                    out |= {(eid, chk.ERROR, f"{m} [place]") for m in places.entry_problems(hit[2])}
        return out
    before = {(i, m) for i, m in claims.problems(series)[0]}
    wbefore = set(witnesses.problems(series)[0])
    ebefore = entry_errs()

    from . import dayorder                                # STYLE 12: on the whole calendar (a cycle's other end; the
    dbefore = set(dayorder.problems(series))              # follower of an entry the patch moves or deletes)
    nbefore = name_tags(lst)                              # STYLE 13: the calendar's name tags, and who the series
    kbefore = person_keys(series) if people_ops(ops, lst) else None   # held where the patch may change it (Part III)
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
    errors += [f"{w}: {m} [day-order]" for w, m in sorted(set(dayorder.problems(series)) - dbefore)]
    errors += name_tag_errors(series, lst, nbefore, kbefore)  # STYLE 13
    for l in rep.lines:
        if l.startswith("error"):
            msg = l.split(None, 1)[1]
            if not any(msg.split(": ", 1)[-1] in x for x in errors):
                errors.append(msg)
    se, sw = subentry_problems(series, ops)
    errors.extend(se)
    warnings.extend(sw)
    fe, fw = fields_problems(series, ops, path)
    errors.extend(fe)
    warnings.extend(fw)
    return errors, warnings


def name_tags(lst):
    """The (id, tag) pairs of the calendar's `name:` tags."""
    if lst is None:
        return set()
    return {(e["id"], str(tg)) for _, e in lst.entries() for tg in e.get("tags") or [] if str(tg).startswith("name:")}


def people_ops(ops, lst):
    """Whether an op may change whom the series holds (lives.people: the names of Part III): one on an entry
    outside the calendar."""
    pre = f"{lst.key}." if lst is not None else None
    for op in ops:
        if isinstance(op, dict) and len(op) == 1:
            (kind, body), = op.items()
            body = body if isinstance(body, dict) else {}
            ids = (body.get("id"), (body.get("entry") or {}).get("id"), body.get("keep"), body.get("drop"))
            if any(i and (pre is None or not str(i).startswith(pre)) for i in ids):
                return True
    return False


def person_keys(series):
    """check's keys (lives.problems): each person's, and each FRUS form joined in another's entry; built afresh (the
    lives cache cleared: the series has changed under it). None in a tree without the people's sources (a test's)."""
    from . import lives
    if not os.path.isdir(os.path.join(store.ROOT, "congress")):
        return None
    for k in ("people", "everyone", "frus-alias", "frus-union"):
        lives._CACHE.pop(k, None)
    return {lives.key_of(p["name"]) for p in lives.everyone(series)} | set(lives._CACHE.get("frus-alias", {}))


def name_tag_errors(series, lst, before, kbefore=None):
    """STYLE 13: check's lives rule on the calendar as the dry run leaves it: each `name:` tag the key of a person
    the series holds. A tag the tree already left unheld is not the patch's; one the patch adds, or leaves unheld
    by changing a name entry, is."""
    after = name_tags(lst)
    if after <= before and kbefore is None:          # no tag added, no person changed
        return []
    keys = person_keys(series)
    if keys is None:
        return []
    kb = keys if kbefore is None else kbefore
    bad = {(i, t) for i, t in after if t[5:] not in keys} - {(i, t) for i, t in before if t[5:] not in kb}
    return [f"{i}: tag {t} names no person (a name entry's key, or leave the person in c untagged) [name-tag]"
            for i, t in sorted(bad)]


def fields_problems(series, ops, path=None):
    """STYLE 10: R25a's fields on each calendar entry the patch adds, as the dry run left it (tools/bib/fields.py)."""
    from . import fields
    out, warn, place = [], [], []
    for op in ops:
        if not (isinstance(op, dict) and len(op) == 1 and "add" in op):
            continue
        eid = ((op["add"] or {}).get("entry") or {}).get("id")
        if not fields.is_cal(eid):
            continue
        hit = series.get(eid)
        e = hit[2] if hit else (op["add"] or {}).get("entry") or {}
        for rule, msg in fields.findings(e):
            (out if fields.LEVEL[rule] == "error" else place if rule == "fields-place" else warn).append(msg)
    warn += place[:fields.PLACE_SHOWN]
    if len(place) > fields.PLACE_SHOWN:
        warn.append(f"{len(place)} [fields-place] findings in all, the first {fields.PLACE_SHOWN} above: "
                    f"./bib fields --patch {path or 'PATCH'} lists them")
    return out, warn


def subentry_problems(series, ops):
    """check [subentry] (subentries.py STYLE 4) on the tree as the patch would leave it: each part's parent an entry
    of its date and no subentry itself; a part's `follows` only its siblings."""
    lst = series.lists.get("cal")
    if lst is None:
        return [], []
    ents = {e["id"]: dict(e) for _, e in lst.entries()}
    for op in ops:
        if not isinstance(op, dict) or len(op) != 1:
            continue
        (kind, body), = op.items()
        body = body or {}
        if kind == "add" and (body.get("entry") or {}).get("id"):
            ents[body["entry"]["id"]] = dict(body["entry"])
        elif kind == "edit" and body.get("id") in ents:
            e = ents[body["id"]]
            e.update(body.get("set") or {})
            for k in body.get("unset") or []:
                e.pop(k, None)
    kids = {}
    for e in ents.values():
        if e.get("part_of"):
            kids.setdefault(str(e["part_of"]), set()).add(e["id"])
    touched = set()
    for op in ops:
        if isinstance(op, dict) and len(op) == 1:
            (kind, body), = op.items()
            body = body or {}
            touched.add(body.get("id") or (body.get("entry") or {}).get("id"))
    out, warn = [], []
    for eid in touched:
        e = ents.get(eid)
        if not e:
            continue
        group = [e] + [ents[k] for k in kids.get(eid, set())]   # an edited parent's parts too
        for x in group:
            p = str(x.get("part_of") or "")
            if p:
                par = ents.get(p)
                if p == x["id"]:
                    out.append(f"{x['id']}: part_of names the entry itself [subentry]")
                elif par is None:
                    out.append(f"{x['id']}: part_of: {p} is no calendar entry [subentry]")
                else:
                    if str(par.get("date")) != str(x.get("date")):
                        out.append(f"{x['id']}: part_of: {p} is of another date [subentry]")
                    if par.get("part_of"):
                        out.append(f"{x['id']}: part_of: {p} is itself a subentry [subentry]")
                for f in store.as_list(x.get("follows")):
                    if f not in kids.get(p, set()):
                        out.append(f"{x['id']}: follows {f}, not a subentry of {p} [subentry]")
            else:
                for f in store.as_list(x.get("follows")):
                    if ents.get(f, {}).get("part_of"):
                        warn.append(f"{x['id']}: follows {f}, a subentry of {ents[f]['part_of']}: follow the parent?")
    return sorted(set(out)), sorted(set(warn))


def report(series, path, legacy=False):
    errors, warnings = check(series, path, legacy)
    out = [f"== {os.path.basename(path)}: {len(errors)} errors, {len(warnings)} warnings"]
    out += ["  error  " + x for x in errors] + ["  warn   " + x for x in warnings]
    return "\n".join(out), bool(errors)
