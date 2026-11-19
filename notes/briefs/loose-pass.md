# The loose-dates pass: every approximate date on its ghost day

The owner, Nov. 19, 2026 (about 6:00 a.m. Pacific): "Could we not check and place all approximate dates? I'm not sure even your 24 catch nearly all the ones I was thinking of." The rulings it applies (notes/owner-brief.md, Nov. 15, and loose.py's STYLE): a loose date sits on an intercalary "ghost" day (偽日), a heading in the day's ordinary style whose text is the loose date; "after X" on a day after X's day ("X bis"), "before X" on a day before it; early, mid, late: the month in thirds, the entry on the day before its third begins ("Early May" after "May" and before "May 1"); a season on the day before it opens (Washington time); the year alone before "January", before "Early January", before "January 1"; and the first ask, "at the earliest date implied by their range".

## What is read

L1. Every calendar entry dated to a month or a year (`date: '1962-05'`, `'1962'`) that has no `at:`. Its `when`, its `c` and its note `n`. The position may be in any of them: `when: July` with `c` "Early July. Kennedy and Jackie Robinson ..." or "Los Angeles, near the convention's close" or "After Kennedy's nomination"; a note's source dating it ("NYT, July 14").

L2. Your list: `scratchpad/loose-pass/<chunk>.tsv` (id, date, when, thread, the start of `c`, the note's first 400 characters; the rows whose `c` or `n` hold a position word first). The whole entry: `./bib show ID`.

## What is set

L3. Where the record (the entry's own `c`, `n`, or the source the note cites, if it is in the repo's texts) fixes a position within the month or year:
- `when:` gets the qualifier in the house form, the month first: `July, early`; `July, after the convention`; `July, before Kennedy's nomination`; `Nov., after the election`; `1961, early`. Keep it short; the ghost day's heading is made from it.
- `at:` per the owner's rules: `before YYYY-MM-DD` / `after YYYY-MM-DD`. Thirds: early `before 1960-07-01`, mid `before 1960-07-11`, late `before 1960-07-21` (February and short months: `loose.thirds`). An event: before or after the event's day as the calendar dates it — find the event's own entries (`./bib find -l cal --thread T --since ... --until ...`) and use their date; a span (a convention, a plenum, "the convention", "convention week") before its first day; "near the close" of a span: before its last day; "the eve of X": before X's first day.
- A year-dated entry: "early"/"first half" `before YYYY-01-01` (after the year's block, before January), "mid-" `before YYYY-05-01`, "late" `before YYYY-09-01`, "second half" `before YYYY-07-01` (the code to show year ghost days before their month block is coming; set them all the same).

L4. Where the record fixes the **day** itself ("July 14", "the next day" after a dated entry, a festival or lunar date converted), the entry is not loose: list it under "Dated to the day" in your report with the date and the evidence; do not change `date` (the lead dates them by patch, as a date change moves the entry's file).

L5. Where nothing fixes a position: no op. Never a guess; never the thread alone; never what you know but the entry does not say. A wrong place is worse than none. "By the 15th" and a span of months stay in the block (the earliest implied day is the first).

## The work

L6. Patch `inbox/<date>-loose-<chunk>.yaml`, ops `edit` with `base:` (the rev `./bib show` prints) and `set: {when: ..., at: ...}`. Batches of ≤40 ops a call; `./bib patch-check` to 0 errors. Touch nothing else; never merge, commit or push.

L7. Report: rows read; ats set by kind (third, season, before/after an event, year), with the events used and their dates; "Dated to the day" list; doubts.
