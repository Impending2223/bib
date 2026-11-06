"""Print each day's calendar entries in the order the build lays them out (tools/bib/dayorder.py, `order`), for a
reader checking the day's order: `python3 -I tools/times/day_order.py 1964 [--from 1964-03] [--until 1964-04]
[--all]`. By default only the days with two or more entries; --all, every day.

A line an entry: its place in the day (the time, `~` before an approximate one, or the range, each in the entry's
zone where it has one, else Washington's), the range's basis where it is `kind`, the primary thread, the id, its
`follows`, and the start of its `c`. Unplaced entries are marked `--`. Reads the tree only; writes nothing."""
import argparse
import datetime
import os
import sys
import zoneinfo

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from tools.bib import store, dayorder  # noqa: E402

DC = zoneinfo.ZoneInfo("America/New_York")


def local(t, zone):
    i = dayorder._instant(t)
    if not i:
        return str(t)
    i = i.replace(tzinfo=datetime.timezone.utc).astimezone(zone)
    return i.strftime("%H:%M")


def label(e):
    try:
        zone = zoneinfo.ZoneInfo(e.get("time_zone") or "America/New_York")
    except Exception:
        zone = DC
    if e.get("time"):
        return ("~" if e.get("time_approx") else "") + local(e["time"], zone)
    r = e.get("time_range")
    if isinstance(r, (list, tuple)) and len(r) == 2:
        s = f"{local(r[0], zone)}-{local(r[1], zone)}"
        if e.get("range_basis") == "kind":
            s += " kind"
        return s
    return "--"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("year")
    ap.add_argument("--from", dest="lo")
    ap.add_argument("--until", dest="hi")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    s = store.Series(ROOT)
    lst = s.lists["cal"]
    days = {}
    for sec in lst.sections:
        for e in sec.entries:
            d = str(e.get("date", ""))
            if "when" not in e or len(d) != 10 or not d.startswith(a.year):
                continue
            if a.lo and d[:len(a.lo)] < a.lo or a.hi and d[:len(a.hi)] > a.hi:
                continue
            days.setdefault(d, []).append(e)
    for d in sorted(days):
        es = days[d]
        if len(es) < 2 and not a.all:
            continue
        print(f"== {d}")
        for e in dayorder.order(lst, es):
            f = store.as_list(e.get("follows"))
            fl = f" <{','.join(x.split('.', 2)[-1] for x in f)}" if f else ""
            c = " ".join(str(e.get("c") or "").split())[:150]
            print(f"  {label(e):<18} {e.get('thread', ''):<28} {e['id'].split('.', 2)[-1]}{fl} | {c}")


if __name__ == "__main__":
    main()
