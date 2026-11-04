"""The owner's editing desk: the calendar's data, published beside the desk's page (the owner's request, Oct. 29, 2026;
the hand-off of Nov. 1, item 0).

    python3 -I tools/desk/export.py OUT_DIR

writes into OUT_DIR (the scratchpad, or build/desk/; never the repo's data):

    index.json        the threads (slug, name, parent, sort key, c with its span tags, see_also, rev), the months (file, count), a
                      search row an entry (id, date, when, thread, also, its c, the name keys, its month file),
                      and the short forms of every work the calendar cites ([[w.id]] -> "Beschloss, *Crisis Years*")
    m-<YYYYMM>.json   a month's entries in full, as the desk edits them: id, rev, file, when, date, thread, also, c, n,
                      tags, time, time_approx, follows

STYLE
1. The rev is the store's (`store.rev`), the base a patch quotes: the desk sends it back with each edit, so the merge is
   three-way and the owner's edit never overwrites a change made since the export.
2. Nothing the build derives is exported (rubrics, labels, the thread index): the desk previews the text as the build
   would print it, close enough to read (italics, links, the works' short forms, a link's date), not the page itself.
3. Deterministic: sorted keys, no timestamps but the export's date in index.json.
"""
import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from tools.bib import store, works  # noqa: E402

FIELDS = ["when", "date", "thread", "also", "c", "n", "tags", "time", "time_approx", "follows", "short", "to"]
WREF = re.compile(r"\[\[(w\.[^\]|]+)")


def main(out):
    os.makedirs(out, exist_ok=True)
    s = store.Series(ROOT)
    cal = s.lists["cal"]
    threads, months, search, cited = [], [], [], set()
    for sec in cal.walk():
        if not sec.file:
            continue
        if sec.file == "th.yaml":
            for e in sec.entries:
                f = store.stored_form(e)
                threads.append({"slug": e["id"].split(".", 2)[2], "id": e["id"], "rev": store.rev(e),
                                "s": f.get("s", ""), "parent": f.get("parent"), "sort": f.get("sort"),
                                "c": f.get("c", ""),
                                "see_also": f.get("see_also") or [], "see": f.get("see")})
                for k in ("c",):
                    cited.update(WREF.findall(f.get(k) or ""))
            continue
        name = os.path.splitext(sec.file)[0]
        rows = []
        for e in sec.entries:
            f = store.stored_form(e)
            row = {"id": e["id"], "rev": store.rev(e)}
            for k in FIELDS:
                if k in f:
                    row[k] = f[k]
            rows.append(row)
            cited.update(WREF.findall((f.get("c") or "") + " " + (f.get("n") or "")))
            c = f.get("c") or ""
            search.append({"id": e["id"], "d": str(f.get("date", "")), "w": f.get("when", ""), "t": f.get("thread", ""),
                           "a": f.get("also") or [], "c": c if isinstance(c, str) else " ".join(map(str, c)),
                           "nm": [t[5:] for t in f.get("tags") or [] if t.startswith("name:")], "m": name})
        with open(os.path.join(out, f"m-{name}.json"), "w", encoding="utf-8") as fh:
            json.dump({"section": sec.id, "file": sec.file, "title": sec.title, "entries": rows}, fh,
                      ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        months.append({"m": name, "section": sec.id, "title": sec.title, "count": len(rows)})
    shorts = {}
    for cid in sorted(cited):
        real = s.works.alias.get(cid, cid)
        if s.works.get(real):
            shorts[cid] = works.short_form(real, s.works)
    idx = {"exported": datetime.date.today().isoformat(), "threads": threads, "months": months, "search": search,
           "works": shorts}
    with open(os.path.join(out, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(idx, fh, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    print(f"{len(months)} months, {len(search)} entries, {len(threads)} threads, {len(shorts)} works -> {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "build/desk")
