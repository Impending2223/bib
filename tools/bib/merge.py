"""Merging changes from several hands without losing any of them.

Three ways changes arrive, one set of rules for all of them:

1. Patch files (inbox/*.yaml), written by an instance that may never have seen
   the repo. `./bib merge inbox/x.yaml` applies them.
2. Git branches. The merge driver (`./bib setup`) merges section files entry by
   entry instead of line by line.
3. Two entries found to be the same thing. `./bib combine KEEP DROP`.

The rules, field by field (three-way: base = what the editor started from):
    unchanged on one side      -> take the other side's change
    same change on both sides  -> take it
    tags / also / aliases      -> set merge: keep both sides' additions, honor removals
    different text changes     -> CONFLICT: ours stays in place; both versions are
                                  recorded in the entry's `conflict:` list
A conflict never blocks the merge. It is data: `./bib conflicts` lists them,
`./bib check` fails on them, `./bib resolve` or a hand edit clears them.
"""
import datetime
import difflib
import os
import re
import subprocess

from . import store
from .markup import plain, REF_RE
from .refs import Refs

SET_FIELDS = ("tags", "also", "aliases")
SKIP = ("id", "conflict")


# ---------------------------------------------------------------- entry-level three-way

def _set_merge(b, o, t):
    b, o, t = store.as_list(b), store.as_list(o), store.as_list(t)
    keep = [x for x in o if x in t or x not in b]
    keep += [x for x in t if x not in keep and x not in b]
    return keep


def three_way(base, ours, theirs, source):
    """Merge one entry. base may be None (unknown). Returns the merged entry."""
    out = {"id": ours.get("id") or theirs.get("id")}
    conflicts = list(ours.get("conflict", [])) + [c for c in theirs.get("conflict", []) if c not in ours.get("conflict", [])]
    fields = [f for f in store.ENTRY_FIELDS if f not in SKIP]
    fields += [f for f in list(ours) + list(theirs) if f not in fields and f not in SKIP]
    for f in fields:
        b = base.get(f) if base else None
        o, t = ours.get(f), theirs.get(f)
        if o == t:
            v = o
        elif f in SET_FIELDS:
            v = _set_merge(b if base else [], o, t) or None
        elif base is not None and b == o:
            v = t
        elif base is not None and b == t:
            v = o
        elif o is None and base is None:
            v = t  # a field only one side has, with no base to say it was removed
        elif t is None and base is None:
            v = o
        else:
            v = o
            conflicts.append({"field": f, "ours": o, "theirs": t, "base": b, "from": source})
        if v is not None and v != []:
            out[f] = v
    if conflicts:
        out["conflict"] = conflicts
    return store.normalize_entry(out)


def merge_entry_lists(base, ours, theirs, source):
    """Three-way merge of a section's entries (git driver). Keeps our order and
    places entries only they added after their nearest predecessor."""
    B = {e["id"]: e for e in base}
    O = {e["id"]: e for e in ours}
    T = {e["id"]: e for e in theirs}
    out = []
    for e in ours:
        i = e["id"]
        if i in T:
            out.append(three_way(B.get(i), e, T[i], source))
        elif i in B:  # they deleted it
            if e == B[i]:
                continue
            x = dict(e)
            x.setdefault("conflict", []).append({"kind": "deleted-by-theirs", "from": source})
            out.append(store.normalize_entry(x))
        else:
            out.append(e)
    pos = {e["id"]: n for n, e in enumerate(out)}
    for n, e in enumerate(theirs):
        i = e["id"]
        if i in O:
            continue
        if i in B:  # we deleted it
            if e == B[i]:
                continue
            e = dict(e)
            e.setdefault("conflict", []).append({"kind": "deleted-by-ours", "from": source})
        at = 0
        for prev in reversed(theirs[:n]):
            if prev["id"] in pos:
                at = pos[prev["id"]] + 1
                break
        out.insert(at, store.normalize_entry(e))
        pos = {x["id"]: k for k, x in enumerate(out)}
    return out


# ---------------------------------------------------------------- finding the base an editor saw

def git(*args, cwd=store.ROOT):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def find_base(series, eid, rev):
    """The version of entry `eid` whose rev is `rev`, from the store or git history."""
    hit = series.get(eid)
    if hit and store.rev(hit[2]) == rev:
        return hit[2]
    key = eid.split(".", 1)[0]
    log = git("log", "--format=%H", "--", f"lists/{key}")
    for commit in log.stdout.split():
        files = git("grep", "-l", f"id: {eid}$", commit, "--", f"lists/{key}")
        for line in files.stdout.splitlines():
            path = line.split(":", 1)[1]
            text = git("show", f"{commit}:{path}").stdout
            doc = store.yaml.load(text, Loader=store._Loader) or {}
            for e in doc.get("entries") or []:
                e = store.normalize_entry(e)
                if e.get("id") == eid and store.rev(e) == rev:
                    return e
    return None


# ---------------------------------------------------------------- placing a new entry

YEAR_RE = re.compile(r"\((?:[^()]*?,\s*)?(\d{4})(?:[–-]\d{2,4})?\)")


def pub_year(e):
    m = YEAR_RE.search(plain(store.as_list(e.get("c"))[0] if e.get("c") else ""))
    return int(m.group(1)) if m else None


def section_for_date(lst, date):
    for s in lst.walk():
        lo, hi = s.extra.get("from"), s.extra.get("to")
        if lo and hi and lo[:len(date)] <= date <= hi[:len(date)]:
            return s
    return None


def auto_position(sec, e):
    """Index where a new entry belongs, following the section's own order:
    calendars by date; 'Alphabetical' sections by subject; others by year."""
    ents = sec.entries
    if "date" in e:
        d = e["date"]
        at = len(ents)
        for n, x in enumerate(ents):
            xd = x.get("date", "")
            if len(xd) == 10 and len(d) == 10 and xd > d:
                return n
        return at
    logic = " ".join(sec.logic + (sec.parent.logic if sec.parent else []))
    if re.search(r"alphabetical", logic, re.I) and e.get("s"):
        key = store.fold(plain(e["s"]))
        for n, x in enumerate(ents):
            if x.get("s") and store.fold(plain(x["s"])) > key:
                return n
        return len(ents)
    y = pub_year(e)
    if y:
        for n, x in enumerate(ents):
            xy = pub_year(x)
            if xy and xy > y:
                return n
    return len(ents)


def similar(a, b):
    return difflib.SequenceMatcher(None, store.fold(a), store.fold(b)).ratio()


def find_duplicates(series, lst, e):
    """Entries in the same list that look like the same event, work, or person."""
    out = []
    refs = Refs(series)
    for s, x in lst.entries():
        if x["id"] == e.get("id"):
            continue
        if lst.kind == "calendar" and "date" in e and "date" in x:
            if x["date"] == e["date"] and (x.get("thread") == e.get("thread")
                                           or similar(plain(x.get("c", "")), plain(e.get("c", ""))) > 0.6):
                out.append(x["id"])
            continue
        wk = set(refs.work_keys(e)) & set(refs.work_keys(x))
        nk = e.get("s") and x.get("s") and refs.name_key(e) and refs.name_key(e) == refs.name_key(x)
        if wk or nk:
            out.append(x["id"])
    return out


# ---------------------------------------------------------------- patches

class Report:
    def __init__(self):
        self.lines = []
        self.conflicts = 0

    def add(self, status, eid, msg=""):
        if status == "conflict":
            self.conflicts += 1
        self.lines.append(f"{status:9} {eid}{': ' + msg if msg else ''}")


def apply_patch(series, patch, source, report, dry=False):
    touched = set()
    for op in patch.get("ops") or []:
        (kind, body), = op.items()
        fn = OPS.get(kind)
        if not fn:
            report.add("error", "-", f"unknown op {kind!r}")
            continue
        fn(series, body or {}, source, report, touched)
        series.invalidate()
    if not dry:
        for sec in touched:
            series.save_section(sec)
    return touched


def _locate(series, eid, report):
    hit = series.get(eid)
    if not hit:
        report.add("error", eid, "no such entry")
    return hit


def op_add(series, body, source, report, touched):
    e = store.normalize_entry(dict(body.get("entry") or {}))
    eid = e.get("id")
    lst = series.lists.get(body.get("list") or (eid or "").split(".", 1)[0])
    if not eid or not lst:
        report.add("error", eid or "?", "add needs entry.id and a list")
        return
    hit = series.get(eid)
    if hit:  # already here: treat as an edit with no known base
        cur = hit[2]
        merged = three_way(None, cur, e, source)
        if merged == cur:
            report.add("same", eid)
            return
        _replace(hit[1], cur, merged)
        touched.add(hit[1])
        report.add("conflict" if merged.get("conflict") else "updated", eid, "id existed; merged without a base")
        return
    sec = None
    if body.get("section"):
        sec = lst.section(body["section"])
    elif "date" in e:
        sec = section_for_date(lst, e["date"])
    if body.get("after"):
        ah = series.get(body["after"])
        if ah and (sec is None or ah[1] is sec):
            sec = ah[1]
    if sec is None:
        report.add("error", eid, "say which section (section: II.D, or a date in range)")
        return
    dups = find_duplicates(series, lst, e)
    if dups:
        e.setdefault("conflict", []).append({"kind": "duplicate", "of": dups, "from": source})
    if body.get("after") and series.get(body["after"]) and series.get(body["after"])[1] is sec:
        at = [x["id"] for x in sec.entries].index(body["after"]) + 1
    else:
        at = auto_position(sec, e)
    sec.entries.insert(at, e)
    touched.add(sec)
    report.add("conflict" if dups else "added", eid, f"possible duplicate of {', '.join(dups)}" if dups else f"{lst.abbr} {sec.code or sec.id}")


def _replace(sec, old, new):
    i = next(n for n, x in enumerate(sec.entries) if x is old)
    sec.entries[i] = new


def op_edit(series, body, source, report, touched):
    eid = body.get("id")
    hit = _locate(series, eid, report)
    if not hit:
        return
    lst, sec, cur = hit
    theirs = dict(cur)
    for k, v in (body.get("set") or {}).items():
        theirs[k] = v
    for k in body.get("unset") or []:
        theirs.pop(k, None)
    theirs = store.normalize_entry(theirs)
    named = list((body.get("set") or {}).keys()) + list(body.get("unset") or [])
    if not body.get("base"):
        # No base: the editor did not say which version they changed. Apply,
        # and say so; use a base whenever two hands may be at work.
        merged = theirs
        note = "applied without a base (last writer wins)"
    else:
        base = find_base(series, eid, body["base"])
        note = ""
        if base is None:
            # The version they edited is unknown: any named field that differs
            # from the current text is a conflict.
            base = dict(cur)
            for k in named:
                base[k] = "\x00unknown"
            note = f"base {body['base']} not found"
        merged = three_way(base, cur, theirs, source)
        for c in merged.get("conflict", []):
            if c.get("base") == "\x00unknown":
                c["base"] = None
    if merged == cur:
        report.add("same", eid)
        return
    _replace(sec, cur, merged)
    touched.add(sec)
    report.add("conflict" if len(merged.get("conflict", [])) > len(cur.get("conflict", [])) else "edited", eid, note)


def op_tag(series, body, source, report, touched):
    eid = body.get("id")
    hit = _locate(series, eid, report)
    if not hit:
        return
    lst, sec, cur = hit
    tags = [t for t in cur.get("tags", []) if t not in (body.get("remove") or [])]
    tags += [t for t in body.get("add") or [] if t not in tags]
    new = dict(cur)
    if tags:
        new["tags"] = tags
    else:
        new.pop("tags", None)
    new = store.normalize_entry(new)
    if new != cur:
        _replace(sec, cur, new)
        touched.add(sec)
        report.add("tagged", eid, " ".join(tags))
    else:
        report.add("same", eid)


def op_move(series, body, source, report, touched):
    eid = body.get("id")
    hit = _locate(series, eid, report)
    if not hit:
        return
    lst, sec, cur = hit
    dest = series.lists[body.get("list", lst.key)].section(body["section"]) if body.get("section") else sec
    if dest is None:
        report.add("error", eid, f"no section {body.get('section')!r}")
        return
    sec.entries.remove(cur)
    touched.add(sec)
    if body.get("after") and body["after"] in [x["id"] for x in dest.entries]:
        dest.entries.insert([x["id"] for x in dest.entries].index(body["after"]) + 1, cur)
    else:
        dest.entries.insert(auto_position(dest, cur), cur)
    touched.add(dest)
    report.add("moved", eid, f"to {dest.lst.abbr} {dest.code or dest.id}")


def op_delete(series, body, source, report, touched):
    eid = body.get("id")
    hit = _locate(series, eid, report)
    if not hit:
        return
    lst, sec, cur = hit
    if body.get("base") and store.rev(cur) != body["base"]:
        x = dict(cur)
        x.setdefault("conflict", []).append({"kind": "delete-of-changed-entry", "from": source,
                                             "note": "the patch deletes a version that has since changed"})
        _replace(sec, cur, store.normalize_entry(x))
        touched.add(sec)
        report.add("conflict", eid, "deleting an entry that changed since the patch's base")
        return
    users = backlinks(series, eid)
    if users:
        report.add("note", eid, f"still referenced by {', '.join(users[:5])}; those [[links]] will fail check")
    sec.entries.remove(cur)
    touched.add(sec)
    report.add("deleted", eid)


def op_combine(series, body, source, report, touched):
    combine(series, body["keep"], body["drop"], source, report, touched)


OPS = {"add": op_add, "edit": op_edit, "tag": op_tag, "move": op_move, "delete": op_delete, "combine": op_combine}


# ---------------------------------------------------------------- combining duplicates

def backlinks(series, eid):
    out = []
    for lst in series.lists.values():
        for s, e in lst.entries():
            for f in ("s", "r", "n", "c"):
                for t in store.as_list(e.get(f)):
                    if any(m.group(1) == eid for m in REF_RE.finditer(t or "")):
                        out.append(e["id"])
    return sorted(set(out))


def combine(series, keep_id, drop_id, source, report, touched):
    """Fold entry DROP into KEEP. Lists are unioned, DROP's id becomes an alias of
    KEEP so old links still resolve, [[DROP]] links are rewritten, and any text
    the two disagree on becomes a conflict on KEEP."""
    hk, hd = series.get(keep_id), series.get(drop_id)
    if not hk or not hd:
        report.add("error", keep_id if not hk else drop_id, "no such entry")
        return
    (lk, sk, keep), (ld, sd, drop) = hk, hd
    new = dict(keep)
    conflicts = list(keep.get("conflict", []))
    for f in SET_FIELDS:
        v = _set_merge([], keep.get(f), drop.get(f))
        if v:
            new[f] = v
    new["aliases"] = [a for a in new.get("aliases", []) if a != keep_id] + [drop_id] + \
        [a for a in drop.get("aliases", []) if a not in new.get("aliases", [])]
    kc, dc = store.as_list(keep.get("c")), store.as_list(drop.get("c"))
    if lk.kind == "calendar" and dc and kc != dc:
        # one event, one line: differing event lines are for a person to settle
        if store.fold(plain(dc[0])) not in store.fold(plain(kc[0])):
            conflicts.append({"field": "c", "ours": keep.get("c"), "theirs": drop.get("c"), "base": None,
                              "from": f"{source}: combined {drop_id}"})
    elif dc and kc != dc:
        extra = [c for c in dc if store.fold(plain(c)) not in {store.fold(plain(x)) for x in kc}]
        new["c"] = kc + extra
    for f in store.ENTRY_FIELDS:
        if f in SKIP or f in SET_FIELDS or f == "c":
            continue
        a, b = keep.get(f), drop.get(f)
        if b is None or a == b:
            continue
        if a is None:
            new[f] = b
        elif f == "n" and store.fold(plain(b)) in store.fold(plain(a)):
            continue
        elif f == "n" and store.fold(plain(a)) in store.fold(plain(b)):
            new[f] = b
        else:
            conflicts.append({"field": f, "ours": a, "theirs": b, "base": None, "from": f"{source}: combined {drop_id}"})
    conflicts = [c for c in conflicts if not (c.get("kind") == "duplicate")]
    if conflicts:
        new["conflict"] = conflicts
    else:
        new.pop("conflict", None)
    new = store.normalize_entry(new)
    _replace(sk, keep, new)
    sd.entries.remove(drop)
    touched.update({sk, sd})
    # rewrite links
    for lst in series.lists.values():
        for s, e in lst.entries():
            changed = False
            for f in ("s", "r", "n"):
                if e.get(f) and f"[[{drop_id}" in e[f]:
                    e[f] = e[f].replace(f"[[{drop_id}]]", f"[[{keep_id}]]").replace(f"[[{drop_id}|", f"[[{keep_id}|")
                    changed = True
            if changed:
                touched.add(s)
    report.add("conflict" if conflicts else "combined", keep_id, f"absorbed {drop_id}")


# ---------------------------------------------------------------- resolving

def resolve(series, eid, take, field=None):
    """take: ours | theirs | base | both (text joined) | keep (accept as is)."""
    hit = series.get(eid)
    if not hit:
        raise SystemExit(f"no entry {eid}")
    lst, sec, cur = hit
    new = dict(cur)
    left = []
    for c in cur.get("conflict", []):
        if field and c.get("field") != field:
            left.append(c)
            continue
        if "field" in c:
            if take in ("ours", "keep"):
                v = c["ours"]
            elif take == "theirs":
                v = c["theirs"]
            elif take == "base":
                v = c["base"]
            elif take == "both":
                v = " ".join(x for x in (c["ours"], c["theirs"]) if x) if isinstance(c["ours"], str) else c["ours"]
            else:
                raise SystemExit(f"--take must be ours, theirs, base, both, or keep")
            if v is None:
                new.pop(c["field"], None)
            else:
                new[c["field"]] = v
        elif c.get("kind") == "deleted-by-theirs" and take == "theirs" or c.get("kind") == "deleted-by-ours" and take == "ours":
            sec.entries.remove(cur)
            series.save_section(sec)
            return "deleted"
        # duplicate / delete conflicts with any other answer: keep the entry
    if left:
        new["conflict"] = left
    else:
        new.pop("conflict", None)
    _replace(sec, cur, store.normalize_entry(new))
    series.save_section(sec)
    return "resolved" if not left else f"{len(left)} left"


# ---------------------------------------------------------------- git merge driver

def git_merge_driver(base_path, ours_path, theirs_path, name=""):
    """Called by git as: bib git-merge %O %A %B %P. Writes the result to %A."""
    def load(p):
        try:
            return store.load_yaml(p) or {}
        except Exception:
            return None
    O, A, B = load(base_path), load(ours_path), load(theirs_path)
    if not all(isinstance(x, dict) and "entries" in x for x in (A, B)) or O is None:
        r = subprocess.run(["git", "merge-file", "-L", "ours", "-L", "base", "-L", "theirs",
                            ours_path, base_path, theirs_path])
        return 1 if r.returncode else 0
    base = [store.normalize_entry(e) for e in (O.get("entries") or [])]
    ours = [store.normalize_entry(e) for e in (A.get("entries") or [])]
    theirs = [store.normalize_entry(e) for e in (B.get("entries") or [])]
    merged = merge_entry_lists(base, ours, theirs, f"git merge {name}".strip())
    doc = dict(A)
    doc["entries"] = merged
    header = []
    with open(ours_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                header.append(line[2:].rstrip("\n"))
            else:
                break
    store.dump_yaml(doc, ours_path, header=header or None)
    return 0  # conflicts live in the data; ./bib check reports them


# ---------------------------------------------------------------- patch files

def new_patch_path(name):
    d = os.path.join(store.ROOT, "inbox")
    os.makedirs(d, exist_ok=True)
    stamp = datetime.date.today().isoformat()
    return os.path.join(d, f"{stamp}-{store.slug(name, 8)}.yaml")
