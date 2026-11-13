"""Subentries: one event, several matters (the owner, Nov. 12, 2026: "Is there a way we could make one ... entry ...
have sub- ... entries? ... one permalinked unit that simply states the headline/'entry-level' predicate that applies to
all subitems ... followed by a citation block ... followed by each subentry, each with its own topic line, statement,
and citation block. We would give the subentries ... a *teeny-tiny* indent"; "I want a within-entry or subentry
'follows:'").

STYLE
1. A subentry is a calendar entry with `part_of: <parent id>`: its own id (a permalink), thread, `c`, `n`, claims and
   visibility. The parent states what is true of all its parts (a news conference, its place and hour; a session, its
   body and days) and carries their common bibliography (the Public Papers' text, the conference's transcript); each
   part carries its own topic, statement and sources. One level only: a parent is no subentry.
2. The day: the parent takes its place in the day's order (dayorder.py); its subentries follow it at once, a hair
   indented, in their own order: `follows` between siblings (a subentry's `follows: [<sibling id>]`, the sequence
   known though the clock is not: the questions of a conference in the order asked), else the day's key (thread,
   then text). A subentry is never placed elsewhere in the day.
3. Threads: a parent carries its subentries' threads for the highlight (data-threads), so a thread turned on lights the
   parent and the part in that thread, not the part's siblings. The thread's own dates name the subentry.
4. check [subentry]: `part_of` naming no calendar entry, an entry of another date, itself, or an entry that is itself a
   subentry (an error); a subentry's `follows` naming an entry outside its parent (an error: the day's order places
   the parent, not its parts).
"""
from . import store

_CACHE = {}


def children(lst):
    """{parent id: [its subentries]} for the list (a calendar), in file order."""
    key = id(lst)
    if key not in _CACHE:
        out = {}
        for sec, e in lst.entries():
            p = e.get("part_of")
            if p:
                out.setdefault(str(p), []).append(e)
        _CACHE[key] = out
    return _CACHE[key]


def nest(lst, entries, order):
    """The day's entries (already in order) with each parent's subentries after it, in their own order (order(lst,
    kids), dayorder's sort, `follows` between siblings honored): [(entry, is_sub)]. A subentry whose parent is not
    among the day's entries stands where the order put it."""
    here = {e["id"] for e in entries}
    kids = {}
    for e in entries:
        p = e.get("part_of")
        if p and str(p) in here:
            kids.setdefault(str(p), []).append(e)
    if not kids:
        return [(e, False) for e in entries]
    out = []
    for e in entries:
        p = e.get("part_of")
        if p and str(p) in here:
            continue
        out.append((e, False))
        for k in order(lst, kids.get(e["id"], [])):
            out.append((k, True))
    return out


def threads_of(lst, e, own):
    """An entry's threads for the highlight: its own (own: entry_threads), and a parent's subentries' (STYLE 3)."""
    out = list(own)
    for k in children(lst).get(e["id"], []):
        for t in [k.get("thread")] + list(k.get("also") or []):
            for s in (lst.thread_line(t) if t else []):
                if s not in out:
                    out.append(s)
    return out


def problems(series):
    """(where, message) for check [subentry] (STYLE 4)."""
    out = []
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        by_id = {e["id"]: e for sec, e in lst.entries()}
        for sec, e in lst.entries():
            p = e.get("part_of")
            if not p:
                continue
            p = str(p)
            par = by_id.get(p)
            if p == e["id"]:
                out.append((e["id"], "part_of names the entry itself"))
            elif par is None:
                out.append((e["id"], f"part_of: {p} is no calendar entry"))
            else:
                if str(par.get("date")) != str(e.get("date")):
                    out.append((e["id"], f"part_of: {p} is of another date ({par.get('date')}, not {e.get('date')})"))
                if par.get("part_of"):
                    out.append((e["id"], f"part_of: {p} is itself a subentry (one level only)"))
            sibs = {k["id"] for k in children(lst).get(p, [])}
            for f in store.as_list(e.get("follows")):
                if f not in sibs:
                    out.append((e["id"], f"follows {f}, not a subentry of {p}: a subentry follows only its siblings"))
    return out
