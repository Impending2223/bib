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
"""
import os
import re

from . import store
from . import notemerge as nm

STOP_WORKS = ("Made public", "See [[", "Check:", "Reply:", "The order:", "Bibliography:")
STOP_TC = ("See [[",)
DEFERRED = os.path.join(store.ROOT, "inbox", "deferred.yaml")
DRY = False                                   # set by merge.apply_patch: a dry run defers nothing


def _text_starts(part, prefixes):
    return part[0] == "text" and part[1].startswith(prefixes)


def _first(parts, pred, default=None):
    return next((k for k, p in enumerate(parts) if pred(p)), len(parts) if default is None else default)


def _clean(parts):
    return [p for p in parts if not (p[0] in ("tc", "works", "names") and not p[1])]


def _units_ok(e, spec):
    from . import claims
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
    if k[0] != "card" or not k[2]:
        return None, f"cite needs a card with a pinpoint (a number or a link): {item!r}"
    card = k[1]
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
        new["src"] = _with_row(new, f"{card} {k[2]}: {body['units']}", replaces=f"{card} {k[2]}")
    elif e.get("src"):                         # a stored map takes the item's mechanical row, as a seeding would
        new["src"] = _with_row(new, f"{card} {k[2]}: {'?' if k[3] else 'all'}")
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
    for it in body.get("add") or []:
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


FNS = {"cite": cite, "primary": primary, "to-check": to_check, "check": check, "names": names, "also": also,
       "src": src, "via": src}


def defer(op, source):
    rows = store.load_yaml(DEFERRED) if os.path.exists(DEFERRED) else None
    rows = rows or []
    rows.append({"from": source, "op": op})
    store.dump_yaml(rows, DEFERRED, header=["Ops on entries not yet in the tree, kept until they land (tools/bib/addops.py, STYLE 7)."])


def make_op(kind):
    fn = FNS[kind]

    def op(series, body, source, report, touched):
        eid = body.get("id")
        hit = series.get(eid)
        if not hit:
            from . import ledger
            if ledger.named(eid):
                if not DRY:
                    defer({kind: body}, source)
                report.add("deferred", eid, f"{kind}: the entry is in the ledger, not yet the tree")
            else:
                report.add("error", eid, "no such entry (and not in the ledger)")
            return
        lst, sec, cur = hit
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
    """Split inbox/deferred.yaml into the ops now applicable and the rest; write the rest back."""
    rows = deferred_patch()
    if not rows:
        return []
    ready, keep = [], []
    for r in rows:
        (kind, body), = r["op"].items()
        (ready if series.get(body.get("id")) else keep).append(r)
    if keep:
        store.dump_yaml(keep, DEFERRED, header=["Ops on entries not yet in the tree, kept until they land (tools/bib/addops.py, STYLE 7)."])
    elif os.path.exists(DEFERRED):
        os.remove(DEFERRED)
    return ready


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
