"""A run of calendar dates, grouped by year: the one form for every list of calendar dates in the series.

STYLE (the standard; every list of calendar dates follows it):
 1. The dates in order, grouped by year. Each group opens with its year, in the headings' sans serif, a little
    heavier, unlinked (`<b class="ty">`, its CSS in templates/list.html and series.html), then the dates as the
    entries write them ("when": Jan. 20, Nov. 8–11, Dec. 28–Jan. 8), each linked to its entry, a comma between.
 2. A full stop after each year's dates, none added after a date that ends in one ("Dec."):
    "1961 Jan. 20, May 16, Nov. 8–11. 1962 Jan. 22–31, Mar. 14."
 3. Where the run follows a label ("Cal."), the label, a space, the run.

Used by the calendar's thread index (tools/bib/calsplit.py), the pointers under each member of the Congress rosters and
each holder of the Executive roster, executive.html's and the calendar's alike (tools/bib/congress.py), and the
"In the series" line of the Names (tools/bib/lives.py).
"""
import re


def groups(items):
    """items: (iso date, link html) in order. [(year, [link, ...]), ...]"""
    out = []
    for d, link in items:
        y = str(d)[:4]
        if out and out[-1][0] == y:
            out[-1][1].append(link)
        else:
            out.append((y, [link]))
    return out


def part(y, links):
    return f'<b class="ty">{y}</b> ' + ", ".join(links)


def stop(t):
    """A full stop after a year's dates, none added after a date that ends in one."""
    return t if re.sub(r"<[^>]+>", "", t).endswith(".") else t + "."


def run(items):
    """The whole run: "1961 Jan. 20, May 16. 1962 Jan. 22–31." """
    return " ".join(stop(part(y, ls)) for y, ls in groups(items))
