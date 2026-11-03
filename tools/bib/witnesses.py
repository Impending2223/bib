"""Witnesses: the tree of what each claim rests on (the owner, Oct. 30, 2026: "a trace/map of *all* the *ultimate*, or
*root*, materials that bear on a fact or event"; "Don't drop the first rule"). The memo: notes/extensions/memos/
witnesses.md (the terms §2, the record that is the act §2a, the readers' rules §3, the data §4).

    sources/witnesses/<YYYY>.yaml       the registry: one witness a row, filed by the year of its date
    sources/witnesses/undated.yaml      those with no date
    sources/witnesses/by-work/<card>.yaml   a work's edges: [{at: '251 n.14', of: x.…, kind: citation}], its page and
                                        note pointing to the witness its text rests on (the card is the work's node)

A witness:

    - id: x.1965-02-07.bundy-to-johnson         # permanent; never reused: x.<its date or 'undated'>.<a slug>
      what: Bundy to Johnson, Feb. 7, 1965      # as the citing witness gives it: author to recipient, or the title
      kind: memorandum                          # KINDS
      date: '1965-02-07'                        # YYYY-MM-DD, YYYY-MM, YYYY, or null
      where: NSF, Memos to the President, Bundy, vol. 8, box 2, LBJ Library   # repository and file, as cited
      agent: [name:bundy-mcgeorge]              # whose account it is: name tags, else the name as written
      made: contemporaneous                     # MADE; `made_on` for a later one's date
      form: original                            # FORMS
      from: [{of: x.…, kind: recollection}]     # upstream edges (EDGES); none: a root, which says why in `open`
      open: closed archive                      # OPEN: why the branch ends here
      copies: [FRUS 1964–68, II, doc. 84]       # a copy the series can read (FRUS, the Papers, a recording, a scan)
      read: false                               # read and cited as an entry's primary record

Readers at work together write their new witnesses to `inbox/witnesses/<patch name>.yaml` (the same rows), never to the
year files, so no two write one file; check reads them with the registry, and the merger folds them in
(`python3 -I tools/witnesses/fold.py`: each row to its year's file, a repeated id refused). A work's edges go in its own
by-work file, which only its reader writes.

STYLE
1. Every witness met that bears on a claim is registered, however well attested the claim (memo §3, rule 1). A copy of
   one registered (the same text, nothing added) is its `copy`, `print` or `edition` edge: kept, never counted as
   support.
2. Studies, memoirs and documentary collections are witnesses: a work in the catalogue is its card (no row here), its
   edges in by-work/; a study the series does not hold is a row, its source `open` where the reader cannot follow it.
3. The claim map's `via` rows name a witness: `via x.1965-02-07.bundy-to-johnson: B`, or, as written before the
   registry, `via w.dallek-flawed-giant 251 n.14: B` (the work's edge at that page and note leads to it). Both resolve.
4. The record that is the act (memo §2a): a map row to a linked dispositive record (DISPOSITIVE: the statute, the
   session law, the treaty, the order, the proclamation, the regulation, the decision, the canvass, the release, the
   journal) closes its units; `stemma` says so and asks no root of them. Not built into the rows yet: shown by stemma
   from the link's address (STATUTE, the Federal Register, the U.S. Reports, govinfo's PPP for a proclamation).
5. Independence is counted by roots and agents, never by works (memo §2).
6. check [witnesses]: an error on an id malformed or repeated, a kind, form, edge kind or `made` outside its list, an
   edge to nothing, to itself, or round in a cycle, a by-work file naming no card, a `via` to a witness no item of the
   note leads to, a variant's unit not in `c` or its witness unknown; a warning (one line, a count) on the roots that
   do not say why (`open` blank: the conversion left them so, memo §5).
"""
import collections
import glob
import os
import re

from . import store

DIR = os.path.join(store.ROOT, "sources", "witnesses")
PENDING = os.path.join(store.ROOT, "inbox", "witnesses")    # a reader's new witnesses, a file a reader, until folded
BYWORK = os.path.join(DIR, "by-work")
KINDS = {"memorandum", "letter", "telegram", "minutes", "notes", "diary", "recording", "transcript", "interview",
         "oral history", "file", "report", "hearing", "speech", "statement", "press", "manuscript", "study", "memoir",
         "collection", "other"}
EDGES = {"copy", "print", "edition", "transcription", "translation", "quotation", "citation", "recollection", "report"}
FORMS = {"original", "copy", "print", "translation", "transcription", "account", "study"}
MADE = {"contemporaneous", "later"}
OPEN = {"closed archive", "not found", "not held", "none known", "not recorded"}
DISPOSITIVE = {"statute", "session law", "treaty", "order", "proclamation", "regulation", "decision", "canvass",
               "release", "journal"}
ID = re.compile(r"^x\.(\d{4}(-\d\d(-\d\d)?)?|undated)\.[a-z0-9][a-z0-9-]*$")
DATE = re.compile(r"^\d{4}(-\d\d(-\d\d)?)?$")
AT = re.compile(r"^(?P<page>(?:[IVXL]+, )?\S+) n\.(?P<note>\S+)$")
_cache = {}


def files():
    return sorted(glob.glob(os.path.join(DIR, "*.yaml")))


def pending_files():
    return sorted(glob.glob(os.path.join(PENDING, "*.yaml")))


def work_files():
    return sorted(glob.glob(os.path.join(BYWORK, "*.yaml")))


def file_for(wid):
    y = wid.split(".")[1][:4]
    return os.path.join(DIR, ("undated" if not y.isdigit() else y) + ".yaml")


def load():
    """(witnesses {id: row}, edges {card: [edge]}, where {id: file}), parsed once a run."""
    key = tuple((p, os.path.getmtime(p)) for p in files() + pending_files() + work_files())
    if _cache.get("key") == key:
        return _cache["val"]
    rows, where, edges = {}, {}, {}
    for p in files() + pending_files():
        for r in store.load_yaml(p) or []:
            if isinstance(r, dict) and r.get("id"):
                if r["id"] in rows:
                    where.setdefault("_dup", []).append(r["id"])
                rows[r["id"]] = r
                where[r["id"]] = os.path.relpath(p, store.ROOT)
    for p in work_files():
        edges["w." + os.path.basename(p)[:-5]] = store.load_yaml(p) or []
    _cache.update(key=key, val=(rows, edges, where))
    return rows, edges, where


def register(series=None):
    """{(card, page, note): witness} through the works' edges, for the claim maps' `via w.card PAGE n.NOTE` rows. Each
    witness carries `record` (its `what`) for the renderers written before the registry."""
    rows, edges, _ = load()
    out = {}
    for card, es in edges.items():
        for ed in es:
            m = AT.match(str(ed.get("at", "")))
            w = rows.get(ed.get("of"))
            if m and w:
                out.setdefault((card, m.group("page"), m.group("note")), dict(w, record=w.get("what")))
    return out


def upstream(wid, rows, seen=None):
    """The witnesses above one, itself included, each once (cycles are check's)."""
    seen = seen if seen is not None else []
    if wid in seen or wid not in rows:
        return seen
    seen.append(wid)
    for f in rows[wid].get("from") or []:
        upstream(f.get("of"), rows, seen)
    return seen


def reachable(cards, rows, edges):
    out = set()
    for c in cards:
        for ed in edges.get(c) or []:
            upstream(ed.get("of"), rows, [])
            out.update(upstream(ed.get("of"), rows, []))
    return out


def roots(wid, rows):
    return [w for w in upstream(wid, rows, []) if not rows[w].get("from")]


def problems(series):
    """(errors, warnings): (where, message)."""
    from . import claims
    rows, edges, where = load()
    errors, warns = [], []
    for d in where.get("_dup", []):
        errors.append((where.get(d, "sources/witnesses"), f"{d}: id repeated"))
    blank = 0
    for wid, r in rows.items():
        at = f"{where.get(wid)}: {wid}"
        if not ID.match(wid):
            errors.append((at, "id: x.<date or undated>.<slug>, a-z 0-9 -"))
        elif where.get(wid) != os.path.relpath(file_for(wid), store.ROOT) and not where.get(wid, "").startswith("inbox/"):
            errors.append((at, f"filed in {where.get(wid)}, its year's file is {os.path.relpath(file_for(wid), store.ROOT)}"))
        if not r.get("what"):
            errors.append((at, "no `what`"))
        if r.get("kind") not in KINDS:
            errors.append((at, f"kind {r.get('kind')!r} not in KINDS"))
        if r.get("date") is not None and not DATE.match(str(r["date"])):
            errors.append((at, f"date {r['date']!r}: YYYY-MM-DD, YYYY-MM, YYYY or null"))
        for k, allowed in (("form", FORMS), ("made", MADE), ("open", OPEN)):
            if r.get(k) is not None and r[k] not in allowed:
                errors.append((at, f"{k} {r[k]!r} not in {sorted(allowed)}"))
        for f in r.get("from") or []:
            if f.get("kind") not in EDGES:
                errors.append((at, f"edge kind {f.get('kind')!r} not in EDGES"))
            if f.get("of") == wid:
                errors.append((at, "an edge to itself"))
            elif f.get("of") not in rows:
                errors.append((at, f"an edge to nothing: {f.get('of')}"))
        if not r.get("from") and not r.get("open"):
            blank += 1
    state = {}

    def visit(n, path):
        state[n] = 1
        for f in rows[n].get("from") or []:
            m = f.get("of")
            if m in rows and m != n:
                if state.get(m) == 1:
                    errors.append((where.get(n), f"a cycle: {' -> '.join(path + [m])}"))
                elif not state.get(m):
                    visit(m, path + [m])
        state[n] = 2
    for n in rows:
        if not state.get(n):
            visit(n, [n])
    for card, es in edges.items():
        w = f"sources/witnesses/by-work/{card[2:]}.yaml"
        if series.works.get(card) is None:
            errors.append((w, f"names no card: {card}"))
        for i, ed in enumerate(es):
            if not isinstance(ed, dict) or not AT.match(str(ed.get("at", ""))):
                errors.append((f"{w}[{i}]", "at: 'PAGE n.NOTE'"))
            elif ed.get("of") not in rows:
                errors.append((f"{w}[{i}]", f"of {ed.get('of')!r}: no such witness"))
            elif ed.get("kind") not in EDGES:
                errors.append((f"{w}[{i}]", f"kind {ed.get('kind')!r} not in EDGES"))
    for _, e in claims.calendar(series):
        cards = None
        for r in (e.get("src") or {}).get("rows") or []:
            m = re.match(r"^via (x\.\S+):", r)
            if not m:
                continue
            if m.group(1) not in rows:
                errors.append((e["id"], f"via {m.group(1)}: no such witness"))
                continue
            if cards is None:
                cards = set(re.findall(r"\[\[(w\.[^\]|]+)", str(e.get("n") or "")))
                cards |= {series.works.alias.get(c, c) for c in cards}
            if m.group(1) not in reachable(cards, rows, edges):
                errors.append((e["id"], f"via {m.group(1)}: no item of the note leads to it"))
        if e.get("variants"):
            n_units = len(claims.units(e.get("c") or ""))
            for v in e["variants"]:
                if not isinstance(v, dict) or v.get("unit") not in claims.letters(n_units):
                    errors.append((e["id"], f"variant's unit {v.get('unit') if isinstance(v, dict) else v!r} not in c"))
                elif v.get("witness") not in rows and not str(v.get("witness", "")).startswith("w."):
                    errors.append((e["id"], f"variant's witness {v.get('witness')!r} unknown"))
    if blank:
        warns.append(("sources/witnesses", f"{blank:,} roots do not say why (`open` blank): each reader fills them for "
                                           "the entries it touches (memo §5)"))
    return errors, warns


DISP_LINK = [(re.compile(r"govinfo\.gov/[^)\s]*STATUTE|/statute/|Stat\.\]"), "statute"),
             (re.compile(r"federalregister|FR-\d{4}"), "regulation"),
             (re.compile(r"/us/\d+/|supreme\.justia|U\.S\. \d+"), "decision")]


def stemma(series, eid, unit=None):
    """Lines: each unit's tree, from the note's items to the roots; the roots and agents counted; copies marked."""
    from . import claims
    rows, edges, _ = load()
    hit = series.get(eid)
    if not hit:
        return [f"# {eid}: no such entry"]
    e = hit[2]
    us = claims.units(e.get("c") or "")
    reg = register(series)
    out = [f"# {eid}"]
    for i, u in enumerate(us):
        L = claims.LETTERS[i]
        if unit and L != unit:
            continue
        out.append(f"{L}  {u}")
        found_roots, agents = set(), set()
        for r, kind, key, pin, note, uu, item in claims.resolve(e):
            if uu is None or (uu != "?" and L not in uu):
                continue
            if kind == "card":
                out.append(f"   {key} {pin or ''}".rstrip())
                for ed in edges.get(key) or []:
                    m = AT.match(str(ed.get("at", "")))
                    if m and pin and m.group("page") == str(pin):
                        out.extend(_tree(ed["of"], rows, 2, found_roots, agents))
            elif kind == "via":
                w = reg.get((key, str(pin), str(note)))
                out.append(f"   {key} {pin} n.{note}")
                if w:
                    out.extend(_tree(w["id"], rows, 2, found_roots, agents))
                else:
                    out.append("      (no witness registered at that note)")
            elif kind == "url":
                disp = next((k for rx, k in DISP_LINK if rx.search(item or key or "")), None)
                out.append(f"   {key}" + (f"   [dispositive: {disp}; closes the units it constitutes]" if disp else ""))
            elif kind == "witness":
                out.extend(_tree(key, rows, 1, found_roots, agents))
            else:
                out.append(f"   {r}")
        for v in e.get("variants") or []:
            if v.get("unit") == L:
                out.append(f"   variant: {v.get('witness')} reads {v.get('reads')!r} ({v.get('at', '')})")
        out.append(f"   roots {len(found_roots)}, agents {len(agents)}")
    return out


def _tree(wid, rows, depth, found_roots, agents, seen=None):
    seen = seen if seen is not None else set()
    r = rows.get(wid)
    pad = "   " * depth
    if not r:
        return [f"{pad}{wid} (no such witness)"]
    if wid in seen:
        return [f"{pad}{wid} (above)"]
    seen.add(wid)
    for a in r.get("agent") or []:
        agents.add(a)
    tag = []
    if r.get("copies"):
        tag.append("copy: " + "; ".join(map(str, r["copies"])))
    if not r.get("from"):
        found_roots.add(wid)
        tag.append("ROOT" + (f", open: {r['open']}" if r.get("open") else ""))
    out = [f"{pad}{wid}  {r.get('what')}" + (f"  [{'; '.join(tag)}]" if tag else "")]
    for f in r.get("from") or []:
        out.append(f"{pad}   <-{f.get('kind')}-")
        out.extend(_tree(f.get("of"), rows, depth + 1, found_roots, agents, seen))
    return out


def leads():
    rows, _, _ = load()
    return sorted((r.get("open") or "not recorded", wid, r.get("what"), r.get("where"))
                  for wid, r in rows.items() if not r.get("from") and r.get("open") not in (None, "none known")
                  and not r.get("read"))
