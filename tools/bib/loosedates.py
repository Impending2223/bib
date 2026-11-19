"""./bib loose-dates [--apply] [--list]: set `at` on the calendar's month- and year-dated entries from their own
`when` (tools/bib/loose.py, STYLE 3, 3a; notes/proposals/loose-dates.md). ./bib check warns [loose-at] on any it
would set; ./bib merge sets them on the sections a patch touched.

Unambiguous, and set (loose.at_for):
    "May, early", "May, first week"       before 1962-05-01      the first third
    "May, mid", "May, mid-month", "May, middle", "May, mid-"   before 1962-05-11      the middle third
    "May, late", "May, last week", "May, end", "May, about the end", "May, the last days"
                                          before 1962-05-21      the last third
    "May, second week", "May, third week" before 1962-05-08, before 1962-05-15
    "May, after the 12th"                 after 1962-05-12
    "May, before the 12th"                before 1962-05-12
    "Mar., spring", "June, summer", "Sept., fall" or "autumn", "Dec., winter": the season that opens in the entry's
                                          month, before its first day (loose.season_starts)
    "1962, early", "1962, first half"     before 1962-01         after "1962", before "January"
    "1962, mid-", "1962, mid-year"        before 1962-05         before "May"
    "1962, second half"                   before 1962-07         before "July"
    "1962, late"                          before 1962-09         before "September"
    "1962, spring" ...                    before 1962-03-20      the day the season opens
A month or a year alone, or a span of them ("Oct.–Dec.", "1964–65"), needs none. Everything else whose `when` says
more than its month or year is left for a reader and listed (--list): a season in a month it does not open in ("Apr.,
spring": the month is the source's, or the season is), "by the 15th", "early in the year" on a month's entry, a
festival or a lunar date (notes/proposals/loose-dates-days.md), "after the convention", and the rest. An entry that
has an `at` already is not touched.

The default is a dry run: the counts by pattern. --apply writes the files (only the `at` line is added).
"""
import collections
import re

from . import loose

MON = r"(?:Jan\.|Feb\.|Mar\.|Apr\.|May|June|July|Aug\.|Sept\.|Oct\.|Nov\.|Dec\.)"
MONTH_ONLY = re.compile(rf"^{MON}(?:–{MON})?$")          # a month, or a span of months ("Oct.–Dec."): no at needed
YEAR_ONLY = re.compile(r"^\d{4}(?:–\d{2,4})?$")            # a year, or a span of years ("1964–65")


def pattern(e):
    """The `when` with its month and numbers made general: 'May, after the 12th' -> 'MON, after the Nth'."""
    g = loose.MONTH_HEAD.sub("MON, ", str(e.get("when") or ""), count=1)
    g = re.sub(MON, "MON", g)
    return re.sub(r"\d+", "N", g).rstrip(", ")


def plan(series):
    """(set, left): [(sec, e, at)] the entries to set, [(sec, e)] the loosely worded ones left for a reader."""
    lst = series.lists.get("cal")
    put, left = [], []
    for sec, e in lst.entries():
        d = loose.date_of(e)
        w = str(e.get("when") or "").strip()
        if "when" not in e or len(d) not in (4, 7) or e.get("at") or MONTH_ONLY.match(w) or YEAR_ONLY.match(w):
            continue
        a = loose.at_for(e)
        if a and not loose.at_problems(dict(e, at=a)):
            put.append((sec, e, a))
        else:
            left.append((sec, e))
    return put, left


def run(series, apply=False, listing=False):
    put, left = plan(series)
    by = collections.Counter(pattern(e) for _, e, _ in put)
    rest = collections.Counter(pattern(e) for _, e in left)
    out = [f"at to set: {len(put)}"] + [f"  {n:4d}  {p}" for p, n in by.most_common()]
    out.append(f"left for a reader: {len(left)} (--list names them)")
    out += [f"  {n:4d}  {p}" for p, n in rest.most_common()]
    if listing:
        out.append("")
        out += [f"{e['id']}\t{e['date']}\t{e['when']}\t{sec.file}" for sec, e in left]
    if apply and put:
        touched = {}
        for sec, e, a in put:
            e["at"] = a
            touched[id(sec)] = sec
        for sec in touched.values():
            series.save_section(sec)
        out.append(f"written: {len(put)} entries in {len(touched)} files")
    return "\n".join(out)
