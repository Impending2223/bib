"""Day blocks: a table or map set under a date in the calendar's day layout, not under an entry.

    marker(iso)                    tools/bib/daybook.py calls it for each day it lays out (section_days), after the day's
                                   entries and before its documents: a placeholder where some block falls on that day
    inject(page, series, mode)     after the indicators (tools/bib/build.py, both chains): the placeholders filled, each
                                   block's anchor registered with the contents (contents.day_mark), the styles added
    held_days(series)              the days the calendar's dated sections hold

Two kinds now (the owner's request, Oct. 22, 2026): The war table under the first Thursday of each month
(tools/bib/wartable.py) and the forces tables under Armed Forces Day (tools/bib/afday.py). A new kind adds itself to
PROVIDERS (its days, its block for a day) and registers its contents kind in contents.KINDS.

STYLE (keep it):
 1. A day block stands under the date and the day's entries, before the day's folded documents; several on one day in
    PROVIDERS' order.
 2. Its anchor (contents.day_mark: a span before the block, as contents.put's) carries the day and its threads, so the
    page's contents and the threads' "Tables and maps" list it like an entry's table (contents.py, STYLE 2 and 4); a
    provider says which of its blocks are listed (the war table: the first of each year on a page).
 3. A block is set only on a day a dated section of the calendar holds; check warns on a war table that falls outside
    them (wartable.problems).
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
    seen_war, seen_year = set(), set()
    afd = afday.dates()

    def part_of(iso):
        return calsplit.half_of_date(lst, iso) if calsplit.cfg(lst) else 1

    def sub(m):
        iso = m.group(1)
        part = part_of(iso)
        out = []
        for name in _days().get(iso, []):
            if name == "war":
                blk = wartable.block(plan, part, iso, part not in seen_war)
                if not blk:
                    continue
                seen_war.add(part)
                key = (part, iso[:4])
                if key not in seen_year:          # the first war table of the year on the page is listed (STYLE 2)
                    seen_year.add(key)
                    blk = contents.day_mark("war", iso[:4], iso, wartable.THREADS, part) + blk
                out.append(blk)
            elif name == "afd":
                blk = afday.block(iso, afd[iso])
                if blk:
                    out.append(contents.day_mark("forces", str(afd[iso]), iso, afday.THREADS, part) + blk)
        return "".join(out)
    page = MARK_RE.sub(sub, page)
    if 'id="wartstyle"' not in page:
        page = page.replace("</head>", wartable.STYLE + afday.STYLE + "\n</head>", 1)
    return page
