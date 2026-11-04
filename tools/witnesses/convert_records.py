"""Once (Nov. 3, 2026; don't rerun): sources/cited-records/ into the witness registry (tools/bib/witnesses.py; the memo,
notes/extensions/memos/witnesses.md, §5).

    python3 -I tools/witnesses/convert_records.py

Each record row becomes a witness: `record` its `what`, its kind, date, where; `found` a `copies` entry; `read` kept.
Its `cited_by` becomes an edge of the citing work (sources/witnesses/by-work/<card>.yaml: {at: 'PAGE n.NOTE', of,
kind: citation}). Rows naming one record under two works (the same kind and date, the same words folded) become one
witness with two edges; near matches (the same kind and date, the words alike by 0.85 or more) are listed for a
reader in notes/witnesses-near-matches.md, not joined. `agent`, `made`, `form`, `from` and `open` are left blank: the
old files do not say (memo §5). The claim maps' `via` rows need no rewriting: `via w.card PAGE n.NOTE` resolves through
the work's edge (witnesses STYLE 3). sources/cited-records/ then goes to notes/extensions/shelf/cited-records/.
"""
import collections
import difflib
import glob
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from tools.bib import store, witnesses  # noqa: E402

OLD = os.path.join(ROOT, "sources", "cited-records")
KIND = {k: k for k in witnesses.KINDS}


def main():
    if not os.path.isdir(OLD):
        sys.exit("sources/cited-records/ is gone: the conversion has run")
    rows, edges, by_key, used = {}, collections.defaultdict(list), {}, set()
    n_rec = 0
    for p in sorted(glob.glob(os.path.join(OLD, "*.yaml"))):
        card = "w." + os.path.basename(p)[:-5]
        for r in store.load_yaml(p) or []:
            if not isinstance(r, dict) or not r.get("record"):
                continue
            n_rec += 1
            date = str(r["date"]) if r.get("date") is not None else None
            key = (r.get("kind"), date, store.fold(r["record"]))
            wid = by_key.get(key)
            if wid is None:
                base = f"x.{date or 'undated'}.{store.slug(r['record'], 6) or 'record'}"
                wid, k = base, 2
                while wid in used:
                    wid, k = f"{base}-{k}", k + 1
                used.add(wid)
                by_key[key] = wid
                w = {"id": wid, "what": " ".join(str(r["record"]).split()), "kind": KIND.get(r.get("kind"), "other"),
                     "date": date}
                if r.get("where"):
                    w["where"] = r["where"]
                if r.get("found"):
                    w["copies"] = [r["found"]]
                w["read"] = bool(r.get("read"))
                rows[wid] = w
            else:
                w = rows[wid]
                if r.get("found") and r["found"] not in (w.get("copies") or []):
                    w.setdefault("copies", []).append(r["found"])
                if r.get("where") and not w.get("where"):
                    w["where"] = r["where"]
                w["read"] = w["read"] or bool(r.get("read"))
            cb = r.get("cited_by") or {}
            edge = {"at": f"{cb.get('page')} n.{cb.get('note')}", "of": wid, "kind": "citation"}
            if edge not in edges[card]:
                edges[card].append(edge)
    # near matches, for a reader
    groups = collections.defaultdict(list)
    for wid, w in rows.items():
        groups[(w["kind"], w["date"])].append(wid)
    near = []
    for (kind, date), ids in groups.items():
        if len(ids) < 2 or len(ids) > 200:
            continue
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                ra = difflib.SequenceMatcher(None, store.fold(rows[a]["what"]), store.fold(rows[b]["what"])).ratio()
                if ra >= 0.85:
                    near.append((date or "", a, b, ra))
    # write
    os.makedirs(witnesses.BYWORK, exist_ok=True)
    by_file = collections.defaultdict(list)
    for wid in sorted(rows):
        by_file[witnesses.file_for(wid)].append(rows[wid])
    for path, rs in by_file.items():
        store.dump_yaml(rs, path, header=["The witness registry (tools/bib/witnesses.py, its STYLE; the memo, "
                                          "notes/extensions/memos/witnesses.md). Kept by hand or agent."])
    for card, es in edges.items():
        store.dump_yaml(es, os.path.join(witnesses.BYWORK, card[2:] + ".yaml"),
                        header=[f"{card}: its edges, page and note to the witness its text rests on (tools/bib/witnesses.py)."])
    with open(os.path.join(ROOT, "notes", "witnesses-near-matches.md"), "w", encoding="utf-8") as f:
        f.write("# Witnesses that may be one\n\nWritten once by tools/witnesses/convert_records.py (Nov. 3, 2026): the same "
                "kind and date, the words alike by 0.85 or more. Not joined: a reader joins them (one id kept, the "
                "other's edges moved to it, its id left out) or leaves them.\n\n")
        for date, a, b, ra in sorted(near):
            f.write(f"- {a} | {b} ({ra:.2f})\n  - {rows[a]['what']}\n  - {rows[b]['what']}\n")
    shelf = os.path.join(ROOT, "notes", "extensions", "shelf", "cited-records")
    shutil.move(OLD, shelf)
    print(f"{n_rec} records -> {len(rows)} witnesses, {sum(len(v) for v in edges.values())} edges in {len(edges)} works; "
          f"{len(near)} near matches; the old files on the shelf")


if __name__ == "__main__":
    main()
