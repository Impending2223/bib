"""Day blocks: a table or map set under a date in the calendar's day layout, not under an entry.

    marker(iso)                    tools/bib/daybook.py calls it for each day it lays out (section_days), after the day's
                                   entries and before its documents: a placeholder where some block falls on that day
    inject(page, series, mode)     after the indicators (tools/bib/build.py, both chains): the placeholders filled, each
                                   block's anchor registered with the contents (contents.day_mark), the styles added
    held_days(series)              the days the calendar's dated sections hold (held_on_disk: the same, read from
                                   lists/cal/list.yaml, for the modules that file before a series is loaded)

Two kinds now (the owner's request, Oct. 22, 2026): the Southeast Asia table under the first Monday of the month its
figures refer to (tools/bib/wartable.py; the year's first with the year's map above it, tools/bib/vnmap.py, STYLE 8) and
the forces tables under Armed Forces Day (tools/bib/afday.py). A new kind adds itself to
PROVIDERS (its days, its block for a day) and registers its contents kind in contents.KINDS.

STYLE (keep it):
 1. A day block stands under the date and the day's entries, before the day's folded documents; several on one day in
    PROVIDERS' order.
 2. Its anchor (contents.day_mark: a span before the block, as contents.put's) carries the day and its threads, so the
    page's contents and the threads' "Tables and maps" list it like an entry's table (contents.py, STYLE 2 and 4); a
    provider says which of its blocks are listed (the Southeast Asia table: the first of each year on a page) and
    whether the anchor brings the small-capital title (Armed Forces Day, with its 〈〈 〉〉) or not (the Southeast Asia
    table, whose own caption is its title: wartable STYLE 2).
 3. A block is set only on a day a dated section of the calendar holds; check warns on a Southeast Asia table that
    falls outside them (wartable.problems).
"""
import functools
import re

from . import calsplit, contents

MARK = "<!--dblk:{}-->"
MARK_RE = re.compile(r"<!--dblk:(\d{4}-\d{2}-\d{2})-->")


@functools.lru_cache(maxsize=1)
def _days():
    """{iso: [provider name]} for every day some block falls on."""
    from . import wartable, afday
    out = {}
    for d in wartable.filed():
        out.setdefault(d, []).append("war")
    for d in afday.dates():
        out.setdefault(d, []).append("afd")
    return out


def marker(iso):
    """The placeholder daybook.section_days sets in a day: '' where no block falls on it."""
    return MARK.format(iso) if iso in _days() else ""


@functools.lru_cache(maxsize=1)
def held_on_disk():
    """held_days, read from lists/cal/list.yaml's sections (their from and to) without loading the series."""
    import datetime
    import os
    from . import store
    cfg = store.load_yaml(os.path.join(store.ROOT, "lists", "cal", "list.yaml")) or {}
    out = set()
    for s in cfg.get("sections") or []:
        a, b = s.get("from"), s.get("to")
        if not (a and b):
            continue
        d, e = datetime.date.fromisoformat(str(a)), datetime.date.fromisoformat(str(b))
        while d <= e:
            out.add(d.isoformat())
            d += datetime.timedelta(days=1)
    return frozenset(out)


def held_days(series):
    import datetime
    lst = next((l for l in series.lists.values() if l.kind == "calendar"), None)
    out = set()
    for s in (lst.sections if lst else []):
        a, b = s.extra.get("from"), s.extra.get("to")
        if not (a and b):
            continue
        d, e = datetime.date.fromisoformat(str(a)), datetime.date.fromisoformat(str(b))
        while d <= e:
            out.add(d.isoformat())
            d += datetime.timedelta(days=1)
    return out


def inject(page, series, mode):
    """Fill the day blocks' placeholders on a calendar page (mode "list") or in the reader ("series")."""
    if "<!--dblk:" not in page:
        return page
    from . import wartable, afday
    lst = next((l for l in series.lists.values() if l.kind == "calendar"), None)
    days = [m.group(1) for m in MARK_RE.finditer(page)]
    plan = wartable.Plan(lst, days)
    held = held_days(series)
    seq = wartable.sequence(held)                 # every Southeast Asia table, for its 〈〈 and 〉〉 (wartable STYLE 2)
    afd = afday.dates()
    aseq = sorted(d for d, y in afd.items() if d in held and afday.block(d, y))   # every Armed Forces Day (afday STYLE 5)
    seen_year = set()

    def part_of(iso):
        return calsplit.half_of_date(lst, iso) if calsplit.cfg(lst) else 1

    def sub(m):
        iso = m.group(1)
        part = part_of(iso)
        out = []
        for name in _days().get(iso, []):
            if name == "war":
                blk = wartable.block(plan, part, iso, seq)
                if not blk:
                    continue
                key = (part, iso[:4])
                if key not in seen_year:          # the first of the year on the page is listed, untitled (STYLE 2)
                    seen_year.add(key)
                    blk = contents.day_mark("war", wartable.filed()[iso][0], iso, wartable.THREADS, titled=False) + blk
                out.append(blk)
            elif name == "afd":
                blk = afday.block(iso, afd[iso])
                if blk:
                    out.append(contents.day_mark("forces", str(afd[iso]), iso, afday.THREADS,
                                                 nav=afday.nav(iso, afd[iso], aseq)) + blk)
        return "".join(out)
    page = MARK_RE.sub(sub, page)
    if 'id="wartstyle"' not in page:
        page = page.replace("</head>", wartable.STYLE + "\n</head>", 1)
    if 'id="fcstyle"' not in page and afday.STYLE:
        page = page.replace("</head>", afday.STYLE + "\n</head>", 1)
    return page
