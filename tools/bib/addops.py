"""Additive patch ops: changes that add to an entry, applied to the entry as it stands at the merge (the owner's request,
Oct. 30, 2026: "a performant, compute-economizing solution" for parallel readers; notes/extensions/memos/volume.md, §6).

A reader's `edit` replaces whole fields against a `base`; two readers citing one entry collide on `n` and `src` every
time. Nearly everything a reader does to an entry already in the calendar adds something, and additions commute:
these ops need no `base`, and two patches' ops on one entry give the same note in either order (but the order of
items within a run, which the build orders anyway). What is not an addition (a change to `c`, the date, the thread, a
cite taken out) stays an `edit` with its `base`.

    - cite:     {id, item: '[[w.card]], 123 (the vote)', units: 'A, C'}    a work read, with its pinpoint
    - primary:  {id, text: '[Title, 1961 Pub. Papers 1](https://...) (Jan. 20, 1961).', units: 'B'}
    - to-check: {id, add: ['[[w.card]]', 'Bundy to Johnson, Feb. 7, 1965, ... (cited by [[w.x]], 251 n.14)']}
    - check:    {id, text: 'Check: Sorensen gives Oct. 20.'}
    - src:      {id, rows: ['w.card 123: A', 'via w.card 123 n.4: A']}
    - names:    {id, add: ['Rusk'], tags: ['name:rusk-dean']}
    - also:     {id, add: [vietnam-congress]}
    - variant:  {id, unit: C, witness: w.card, reads: 'Oct. 26', at: '710'}    a variant (R41), added once
    - follows:  {id, add: [cal.1964-08-04.vietnam]}                         the day's order (dayorder STYLE 2)
    - place:    {id, at: peking, basis: c}  or  {id, at: [washington, moscow], basis: n, note: '...'}   places.py

STYLE
 1. `cite`: the card leaves "To check:" (the sentence goes when empty) and joins the run of works read: at the end of
    the first run, or, where the note has none, a run of its own after the primary record and the text, before "Made
    public:", any "Check:", "To check:", "See" and "Names:" (R26 of notes/briefs/reader.md). The item must carry a
    pinpoint (claims.is_pin: a number or a link). A card already read at another pinpoint stays, and the new item is a
    second item of the run (each its `src` row; pages are not joined, so that each row names an item the note prints).
    The same item already there: nothing changes.
 2. `units` (on `cite`, `primary`): the letters the source grounds (claims STYLE). The entry's stored map takes the
    row; an entry with none is seeded first with the mechanical map (claims.mechanical, after the note is changed), and
    the seeded row for the same item gives way to the reader's letters. A `cite` without units, on an entry with a
    stored map, adds the item's mechanical row (`all`, or `?` where it has a parenthetical), as a seeding would: so
    the map comes out the same whichever patch lands first, but for the order of its rows.
 3. `primary`: the sentence goes first in the note, unless a link it holds is already in the note.
 4. `to-check`: each item joins "To check:" (made, where there is none, before "See" and "Names:"), unless its card is
    already cited, read or not, or its text already stands there.
 5. `check`: a sentence beginning "Check:", put after the works and before "To check:", "See" and "Names:", unless the
    note holds it already (by its folded text).
 6. `names`, `also`, `src`: unions. A name joins the "Names:" line (made at the end where there is none); a tag joins
    `tags`; a row joins the stored map (seeded as in 2 where there is none).
 7. An op on an id the tree does not hold: refused, unless the ledger of new entries (tools/bib/ledger.py) names it,
    when it is deferred (inbox/deferred.yaml) and applied by the next `./bib merge --auto` after the entry lands.
 8. Letters need a base (notes/proposals/claims-model.md, (f) 1; rulings 35f). An op that names units by letter
    (`units` on `cite` and `primary`, `unit` on `variant`, a `src` row's letters; `all` and `?` are not letters)
    carries `base:` the rev `./bib show` printed, as an `edit` does. The letters are counted from the line's
    punctuation, so they name other words once the line has changed. The merge applies the op only where the line
    (`c`) is the one the base had: the entry's rev now, its rev when this patch began (an earlier op of the patch
    may have changed its note), or a rev found in git. No base, a base not found, or a line changed since: the op
    is refused, and with it the patch. One exception: a patch whose own `edit` set the line names that line's
    letters without a base. A letter op on an entry not yet in the tree is refused, not deferred.
"""
import os
import re

from . import store
from . import notemerge as nm

STOP_WORKS = ("Made public", "See [[", "Check:", "Reply:", "The order:", "Bibliography:")
STOP_TC = ("See [[",)
DEFERRED = os.path.join(store.ROOT, "inbox", "deferred.yaml")
DRY = False                                   # set by merge.apply_patch: a dry run defers nothing
PENDING = None                                # merge.apply_patch: the ops deferred, written only if no op errored
START = {}                                    # merge.apply_patch: id -> (rev, hash of c) as the patch began (STYLE 8)
OWN_C = {}                                    # merge.op_edit: id -> the line this patch's own edit set (STYLE 8)


def _text_starts(part, prefixes):
    return part[0] == "text" and part[1].startswith(prefixes)


def _first(parts, pred, default=None):
    return next((k for k, p in enumerate(parts) if pred(p)), len(parts) if default is None else default)


def _clean(parts):
    return [p for p in parts if not (p[0] in ("tc", "works", "names") and not p[1])]


def _units_ok(e, spec):
    from . import claims
    if claims.NUMBERED.match(str(spec)):
        return claims.parse_target(str(spec), e) is not None
    n = len(claims.units(e.get("c") or ""))
    u = claims.parse_units(spec, n)
    return u is not None and (u == "?" or u <= set(claims.letters(n)))


def _with_row(e, row, replaces=None):
    """The entry's map with `row` added (STYLE 2); `replaces` (a source key: 'w.card 123', an address) drops the seeded
    row for the same source."""
    from . import claims
    src = e.get("src") or claims.mechanical(e) or {"c": claims.chash(e.get("c")), "rows": []}
    rows = list(src.get("rows") or [])
    if replaces:
        rows = [r for r in rows if r.rsplit(": ", 1)[0] != replaces or r == row]
    if row not in rows:
        rows.append(row)
    return {"c": src.get("c") or claims.chash(e.get("c")), "rows": rows}


def cite(e, body):
    from . import claims
    item = (body.get("item") or "").strip()
    k = claims.item_key(item)
    lm = claims.CARD_LINKED.match(item)
    if lm:                                     # a linked pinpoint with its parenthetical: the row is the link's
        k = ("card", lm.group(1).strip(), lm.group(3), lm.group(4))
    elif k[0] != "card" or not k[2]:
        return None, f"cite needs a card with a pinpoint (a number or a link): {item!r}"
    card = k[1]
    row_key = k[2] if lm else f"{card} {k[2]}"
    if body.get("units") and not _units_ok(e, body["units"]):
        return None, f"units {body['units']!r} not in the entry's {len(claims.units(e.get('c') or ''))}"
    parts = nm.parse(e.get("n") or "")
    for kind, v in parts:
        if kind == "tc":
            v[:] = [x for x in v if nm.card(x) != card]
    runs = [p for p in parts if p[0] == "works"]
    if not any(x.strip() == item for _, v in runs for x in v):
        if runs:
            runs[0][1].append(item)
        else:
            at = _first(parts, lambda p: p[0] in ("tc", "names") or _text_starts(p, STOP_WORKS))
            parts.insert(at, ("works", [item]))
    new = dict(e)
    new["n"] = nm.render(_clean(parts))
    if body.get("units"):
        new["src"] = _with_row(new, f"{row_key}: {body['units']}", replaces=row_key)
    elif e.get("src"):                         # a stored map takes the item's mechanical row, as a seeding would
        new["src"] = _with_row(new, f"{row_key}: {'?' if k[3] else 'all'}")
    return new, None


def primary(e, body):
    from . import claims
    text = (body.get("text") or "").strip()
    links = claims.LINK.findall(text)
    if not links:
        return None, f"primary needs a linked record: {text!r}"
    if body.get("units") and not _units_ok(e, body["units"]):
        return None, f"units {body['units']!r} not in the entry"
    new = dict(e)
    n = e.get("n") or ""
    if not any(url in n for _, url in links):
        new["n"] = (text if text.endswith(".") else text + ".") + (" " + n if n else "")
    if body.get("units"):
        for _, url in links:
            new["src"] = _with_row(new, f"{url}: {body['units']}", replaces=url)
    return new, None


def to_check(e, body):
    parts = nm.parse(e.get("n") or "")
    have = nm.cards_of(parts)
    tc = next((p for p in parts if p[0] == "tc"), None)
    items = body.get("add") or []
    if isinstance(items, str):          # one item given bare, not as a list: never split it letter by letter
        items = [items]
    for it in items:
        it = it.strip().rstrip(".")
        c = nm.card(it)
        if (c and c in have) or (tc and it in tc[1]):
            continue
        if tc is None:
            tc = ("tc", [])
            parts.insert(_first(parts, lambda p: p[0] == "names" or _text_starts(p, STOP_TC)), tc)
        tc[1].append(it)
        if c:
            have[c] = (it, "tc")
    new = dict(e)
    new["n"] = nm.render(_clean(parts))
    return new, None


def check(e, body):
    text = (body.get("text") or "").strip()
    if not text.startswith("Check:"):
        return None, f"check needs a sentence beginning 'Check:': {text!r}"
    text = text if text.endswith(".") else text + "."
    parts = nm.parse(e.get("n") or "")
    if any(p[0] == "text" and store.fold(p[1]) == store.fold(text) for p in parts):
        return dict(e), None
    parts.insert(_first(parts, lambda p: p[0] in ("tc", "names") or _text_starts(p, STOP_TC)), ("text", text))
    new = dict(e)
    new["n"] = nm.render(_clean(parts))
    return new, None


def names(e, body):
    parts = nm.parse(e.get("n") or "")
    np_ = next((p for p in parts if p[0] == "names"), None)
    for x in body.get("add") or []:
        if np_ is None:
            np_ = ("names", [])
            parts.append(np_)
        if x not in np_[1]:
            np_[1].append(x)
    new = dict(e)
    new["n"] = nm.render(_clean(parts))
    tags = list(e.get("tags") or [])
    tags += [t for t in body.get("tags") or [] if t not in tags]
    if tags:
        new["tags"] = tags
    return new, None


def also(e, body):
    new = dict(e)
    al = list(e.get("also") or [])
    al += [t for t in body.get("add") or [] if t not in al and t != e.get("thread")]
    if al:
        new["also"] = al
    return new, None


def src(e, body):
    from . import claims
    new = dict(e)
    for r in body.get("rows") or []:
        if claims.parse_row(r) is None:
            return None, f"src row does not parse: {r!r}"
        new["src"] = _with_row(new, r)
    return new, None


def variant(e, body):
    """A variant (R41) added: {id, unit, witness, reads, at}; one already there the same is not added twice (the Chen
    test, point 6: variants were an `edit`, with a base, on entries others were adding to)."""
    row = {k: body[k] for k in ("unit", "field", "value", "witness", "reads", "at") if body.get(k) not in (None, "")}
    if not row.get("witness") or not row.get("reads"):
        return None, "variant: give at least witness and reads (and unit or field, at)"
    if row.get("field") and (row.get("unit") or row.get("value") is None):
        return None, "variant: a field's variant gives field and value, and no unit (claims.py, STYLE 9)"
    new = dict(e)
    vs = list(e.get("variants") or [])
    if row not in vs:
        vs.append(row)
    new["variants"] = vs
    return new, None


def follows(e, body):
    """`follows` ids added (dayorder STYLE 2); its basis goes in the note by a `check`-like sentence the patch writes
    with an edit, or is already there."""
    new = dict(e)
    fs = list(store.as_list(e.get("follows")))
    fs += [f for f in body.get("add") or [] if f not in fs and f != e.get("id")]
    if fs:
        new["follows"] = fs
    return new, None


def place(e, body):
    """An entry's place (places.py, STYLE 3): set where it has none or the same; another place is an `edit`. `basis`
    and `note` are the pass's record (notes/briefs/places.md, P6), not kept on the entry."""
    from . import places
    at = [str(k) for k in store.as_list(body.get("at"))]
    if not at or len(at) > 2:
        return None, "place: at, a gazetteer key or a list of two"
    for k in at:
        if places.get(k) is None:
            return None, f"place {k!r}: not in the gazetteer (a place-key op in the patch adds it)"
    if body.get("basis") not in ("c", "n", "tag", "seat"):
        return None, "place: basis c, n, tag or seat (notes/briefs/places.md, P6)"
    new = dict(e)
    cur = places.keys(e)
    val = at[0] if len(at) == 1 else at
    if cur and cur != at:
        return None, f"place: the entry has {cur}; an edit changes it"
    new["place"] = val
    return new, None


FNS = {"place": place, "variant": variant, "follows": follows, "cite": cite, "primary": primary, "to-check": to_check, "check": check, "names": names, "also": also,
       "src": src, "via": src}


def defer(op, source):
    if PENDING is not None:                   # inside merge.apply_patch: written with the patch's sections, or not at all
        PENDING.append({"from": source, "op": op})
        return
    defer_rows([{"from": source, "op": op}])


DEFERRED_HEAD = ["Ops on entries not yet in the tree, kept until they land (tools/bib/addops.py, STYLE 7)."]


def defer_rows(new):
    """Rows {from, op} appended to inbox/deferred.yaml."""
    if not new:
        return
    rows = store.load_yaml(DEFERRED) if os.path.exists(DEFERRED) else None
    rows = (rows or []) + list(new)
    store.dump_yaml(rows, DEFERRED, header=DEFERRED_HEAD)


def lettered(kind, body):
    """The letters an op names (STYLE 8), as written, or None: `all` and `?` name none."""
    from . import claims
    specs = []
    if kind in ("cite", "primary"):
        specs = [body.get("units")]
    elif kind == "variant":
        specs = [body.get("unit")]
    elif kind in ("src", "via"):
        specs = [(claims.parse_row(r) or (None,) * 5)[4] for r in body.get("rows") or []]
    hit = [str(x) for x in specs if x not in (None, "", "all", "?") and not claims.NUMBERED.match(str(x))
           and not re.fullmatch(r"\d+(?:\.\d+)*", str(x))]            # a part's number holds through edits: no base
    return ", ".join(hit) or None


def base_problem(series, cur, body, spec):
    """Why a letter op may not be applied to `cur` (STYLE 8), or None."""
    from . import claims, merge
    eid, line = cur.get("id"), claims.chash(cur.get("c"))
    if eid in OWN_C and OWN_C[eid] == cur.get("c"):
        return None                           # the patch's own edit wrote this line
    if not body.get("base"):
        return (f"names units by letter ({spec}) with no base: add base: the rev ./bib show {eid} prints "
                "(the letters name other words once the line changes)")
    rev = merge._base(body["base"])
    if store.rev(cur) == rev:
        return None
    if START.get(eid, (None,))[0] == rev:
        was = START[eid][1]
    else:
        old = merge.find_base(series, eid, rev)
        if old is None:
            return f"base {rev} not found: the letters ({spec}) cannot be held to the line they were read from"
        was = claims.chash(old.get("c"))
    if was != line:
        return (f"the line has changed since base {rev}: the letters ({spec}) may name other words now. "
                f"./bib show {eid}, and name them afresh")
    return None


def make_op(kind):
    fn = FNS[kind]

    def op(series, body, source, report, touched):
        eid = body.get("id")
        hit = series.get(eid)
        spec = lettered(kind, body)
        if not hit:
            from . import ledger
            if spec and ledger.named(eid):
                report.add("error", eid, f"{kind}: names units by letter ({spec}) on an entry not yet in the tree; "
                                         "name them, with a base, once it lands")
            elif ledger.named(eid):
                if not DRY:
                    defer({kind: body}, source)
                report.add("deferred", eid, f"{kind}: the entry is in the ledger, not yet the tree")
            else:
                report.add("error", eid, "no such entry (and not in the ledger)")
            return
        lst, sec, cur = hit
        err = base_problem(series, cur, body, spec) if spec else None
        if err:
            report.add("error", eid, f"{kind}: {err}")
            return
        new, err = fn(cur, body)
        if err:
            report.add("error", eid, err)
            return
        new = store.normalize_entry(new)
        if new == cur:
            report.add("same", eid, kind)
            return
        i = next(k for k, x in enumerate(sec.entries) if x is cur)
        sec.entries[i] = new
        touched.add(sec)
        report.add("added-to", eid, kind)
    return op


def deferred_patch():
    """The deferred ops whose entries have landed, as a patch, and the rest kept."""
    if not os.path.exists(DEFERRED):
        return None
    rows = store.load_yaml(DEFERRED) or []
    return rows


def take_deferred(series):
    """The ops of inbox/deferred.yaml now applicable (their entries have landed). The file is not changed: each is
    removed by drop_deferred once it has applied, so an op that fails, or a run that stops, loses none."""
    rows = deferred_patch()
    if not rows:
        return []
    ready = []
    for r in rows:
        (kind, body), = r["op"].items()
        if series.get(body.get("id")):
            ready.append(r)
    return ready


def drop_deferred(done):
    """The rows applied, removed from inbox/deferred.yaml (each once, as read now); the file goes when it is empty."""
    if not done or not os.path.exists(DEFERRED):
        return
    rows = store.load_yaml(DEFERRED) or []
    for r in done:
        if r in rows:
            rows.remove(r)
    if rows:
        store.dump_yaml(rows, DEFERRED, header=DEFERRED_HEAD)
    else:
        os.remove(DEFERRED)


def join_clean(series, source, save=True):
    """After a patch is applied: its conflicts on `n` that notemerge joins with no problem, joined (both sides kept:
    nothing overwritten), and its conflicts on `src` over the same `c`, the rows united. Returns (joined ids, left)."""
    from . import notemerge
    joined, left = [], 0
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            cs = e.get("conflict") or []
            keep = []
            for c in cs:
                if c.get("from") != source:
                    keep.append(c)
                    continue
                if c.get("field") == "n" and c.get("base") is not None:
                    text, probs = notemerge.propose(c["base"], e.get("n") or "", c.get("theirs") or "")
                    if not probs:
                        e["n"] = text
                        joined.append(e["id"])
                        continue
                if c.get("field") == "src" and isinstance(c.get("ours"), dict) and isinstance(c.get("theirs"), dict) \
                        and c["ours"].get("c") == c["theirs"].get("c"):
                    rows = list(c["ours"].get("rows") or [])
                    rows += [r for r in c["theirs"].get("rows") or [] if r not in rows]
                    e["src"] = {"c": c["ours"]["c"], "rows": rows}
                    joined.append(e["id"])
                    continue
                keep.append(c)
                left += 1
            if len(keep) != len(cs):
                if keep:
                    e["conflict"] = keep
                else:
                    e.pop("conflict", None)
                if save:
                    series.save_section(sec)
    return sorted(set(joined)), left
