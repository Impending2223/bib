"""The President's Daily Diary (Johnson's): the days the National Archives Catalog gives with their page images
(daybook/diary.yaml, written by tools/daybook/make_daily_diary.py, which see), and the calendar's citations of them.

Not yet in the day layout: the Diary's line in each day's Documents block waits on the coordinator's design.

STYLE:
 1. A calendar note cites a day as "[President's Daily Diary, Aug. 4, 1964](https://catalog.archives.gov/id/192446),
    images 3, 5 (LBJ Library; National Archives Catalog)": after the document of the act itself (the statute, the Public
    Papers item, the FRUS document) and the other records, before the bibliography; further days of the same entry
    after a semicolon, by date alone ("[Aug. 3](...), image 1"). The images are the item's page images by their number
    in the Catalog's item (its viewer's order), not the Diary's own page numbers, which skip and repeat ("5a", "5b").
 2. Where the Diary disagrees with an entry, the entry keeps its words and ends "Check: the Daily Diary gives ...";
    every such disagreement is set out in notes/diary-discrepancies.md, with the ruling.

check [diary]: fails on a row out of the Diary's span, a key not its date, a duplicate day, an address not the
Catalog's item, a page count not a positive number; and on a calendar note whose Diary link names one day and points
to another day's item, or to an item the file does not hold.
"""
import os
import re


from . import store

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "daybook", "diary.yaml")
FROM, TO = "1963-11-22", "1969-01-20"
MONTHS = {m: i for i, m in enumerate("Jan. Feb. Mar. Apr. May June July Aug. Sept. Oct. Nov. Dec.".split(), 1)}
LINK = re.compile(r"\[(?:President's Daily Diary, )?([A-Z][a-z]+\.?) (\d{1,2})(?:, (\d{4}))?\]"
                  r"\(https://catalog\.archives\.gov/id/(\d+)\)")
_cache = {}


def load():
    if "days" not in _cache:
        rows = []
        if os.path.exists(PATH):
            rows = (store.load_yaml(PATH) or {}).get("days") or []
        _cache["days"] = rows
    return _cache["days"]


def by_naid():
    return {int(r["naid"]): r for r in load() if r.get("naid")}


def problems(series=None):
    seen = set()
    for r in load():
        d, k = str(r.get("date")), r.get("key")
        if not (FROM <= d <= TO):
            yield "daybook/diary.yaml", f"{k}: {d} is outside the Diary's span"
        if k != "pdd:" + d.replace("-", ""):
            yield "daybook/diary.yaml", f"{k}: the key is not its date {d}"
        if d in seen:
            yield "daybook/diary.yaml", f"{k}: a second row for {d}"
        seen.add(d)
        if r.get("url") != f"https://catalog.archives.gov/id/{r.get('naid')}":
            yield "daybook/diary.yaml", f"{k}: url is not the Catalog's item {r.get('naid')}"
        if not isinstance(r.get("pages"), int) or r["pages"] < 1:
            yield "daybook/diary.yaml", f"{k}: pages is not a positive number"
    if series is None:
        return
    items = by_naid()
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            n = e.get("n") or ""
            if "catalog.archives.gov/id/" not in n or "Daily Diary" not in n:
                continue
            year = None
            for m in LINK.finditer(n):
                mon, day, y, naid = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
                year = y or year or str(e.get("date"))[:4]
                r = items.get(naid)
                if mon not in MONTHS:
                    continue
                want = f"{year}-{MONTHS[mon]:02d}-{day:02d}"
                if not r:
                    yield "lists/cal", f"{e['id']}: Diary link to item {naid}, not in daybook/diary.yaml"
                elif r["date"] != want:
                    yield "lists/cal", f"{e['id']}: Diary link names {want} but item {naid} is {r['date']}"
