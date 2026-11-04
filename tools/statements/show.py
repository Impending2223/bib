"""A thread's statements, as they stand and as a draft would print (tools/bib/statements.py; the conversion, volume.md §4).

    python3 -I tools/statements/show.py SLUG [--c 'a draft c, with span tags'] [--short ID=NAME ...]

Prints the thread's c, c2, c3; the calendar's parts and their ranges, with the statement each now shows; its entries'
dates and ids by year, as the index counts them (the primary thread, `also`, a subthread's under its parent; `*`
before an entry filed under the thread or a ghost subthread of it, so one whose `short:` would name an event in this
thread's statement, and the `short:` where it has one); then what the new rendering prints for each year, 1960 to 1969 (the year split to
come) and for each part as it stands: the draft `--c` (else the thread's own `c`), with the drafts' `--short` names
laid over the entries' own. Nothing is written.
"""
import argparse
import datetime
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from tools.bib import calsplit, store, statements  # noqa: E402
from tools.bib.build import thread_members  # noqa: E402
from tools.bib.concepts import parse  # noqa: E402


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("slug")
    ap.add_argument("--c", help="a draft c, with span tags")
    ap.add_argument("--short", action="append", default=[], metavar="ID=NAME", help="a draft event name")
    a = ap.parse_args(argv)
    series = store.Series(ROOT)
    cal = series.lists["cal"]
    te = cal.threads().get(a.slug)
    if te is None:
        sys.exit(f"no thread {a.slug!r} in th.yaml")
    for k in ("c",) + statements.LEGACY:
        if te.get(k):
            print(f"{k}: {te[k]}")
    if te.get("parent"):
        print(f"parent: {te['parent']}")

    # the drafts, laid over a copy of the thread's entry and the entries named
    draft = dict(te)
    if a.c is not None:
        try:
            parse(a.c)
        except ValueError as err:
            sys.exit(f"--c: a span it cannot read: {err}")
        draft["c"] = a.c
    for k in statements.LEGACY:
        draft.pop(k, None)
    for item in a.short:
        eid, _, name = item.partition("=")
        hit = series.get(eid)
        if not hit or hit[0] is not cal or not hit[2].get("date"):
            sys.exit(f"--short: {eid} is no dated calendar entry")
        hit[2]["short"] = name               # in memory only
    statements._EVENTS.clear()

    print("\nparts:")
    first = min((calsplit.half_of_date(cal, m["date"]) for m in thread_members(cal).get(a.slug, [])), default=1)
    for n, p in enumerate(calsplit.parts(cal), start=1):
        lo, hi = calsplit.part_range(cal, n)
        has = any(lo <= statements.day(m["date"]) <= hi for m in thread_members(cal).get(a.slug, []))
        now = calsplit.statement(cal, te, n, first) if has else "(no entries: not shown)"
        print(f"  {n} {p['page']}: {lo} .. {hi}\n      now: {now}")

    print("\nentries (* filed under the thread or a ghost subthread: its short: names an event here):")
    own = {a.slug} | {s for s in cal.threads() if a.slug in cal.thread_line(s)
                      and all(cal.is_ghost(x) for x in cal.thread_line(s)[:cal.thread_line(s).index(a.slug)])}
    by = {}
    for m in thread_members(cal).get(a.slug, []):
        mark = "*" if m["thread"] in own else " "
        sh = f" [{m['short']}]" if m.get("short") else ""
        by.setdefault(str(m["date"])[:4], []).append(f"{mark}{m['id'].split('.', 1)[1]}{sh}")
    for y, ids in by.items():
        print(f"  {y} ({len(ids)}): " + "  ".join(ids))

    lo0, hi0 = calsplit.bounds(cal)
    print("\nthe draft, a year a page:" if a.c is not None or a.short else "\nthe new rendering of c, a year a page:")
    for y in range(1960, 1970):
        lo, hi = max(lo0, datetime.date(y, 1, 1)), min(hi0, datetime.date(y, 12, 31))
        print(f"  {y}: {statements.render(cal, draft, lo, hi)}" if str(y) in by else f"  {y}: (no entries: not shown)")
    print("\nthe draft, a part a page:" if a.c is not None or a.short else "\nthe new rendering of c, a part a page:")
    for n, p in enumerate(calsplit.parts(cal), start=1):
        lo, hi = calsplit.part_range(cal, n)
        has = any(lo <= statements.day(m["date"]) <= hi for m in thread_members(cal).get(a.slug, []))
        print(f"  {p['page']}: {statements.render(cal, draft, lo, hi) if has else '(no entries: not shown)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
