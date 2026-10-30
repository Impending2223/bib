# Volume: the calendar braced for many times its size

The owner, Oct. 30, 2026: "I want the volume! The purpose of what you're building—the tagging, the threading, the
navigational aids, the discipline applied to the writing, sourcing, and organization—is to make the volume
manageable. The structure is meant to be braced for, and should be robust to, *even greater* volumes." On the
proposals that followed (the same day): "I'm with you on everything but 6", the regional grouping of the thread index,
which waits until a need shows ("I'll believe it when I see it"); on 2, "more an invitation to create subthreads,
promote subthreads to threads, and exclude entries exclusive to a subthread, than to simply collapse threads"; "I'm not
a fan of the collapsed military tables, for example. I want that reversed and not followed as a norm"; "I'm also more
of a fan of splitting the calendars than you've been in the past. That's the great thing about dates—they can be
divided and subdivided as needed!"; and the thread statements: "Is there no better, more elegant solution here?"

Nothing here is built. The counts are of Oct. 30, 2026: 8,325 dated entries; the busiest day 48 (Nov. 8, 1966), the
busiest month 168 (Mar. 1968), the largest thread 781 (Vietnam); Cal. I 8.3 MB, Cal. II 10.4, Cal. III 12.0, the
reader 32.2.

## 1. Nothing folded by default

A table or map in the calendar is shown open. Folding is kept only for what the owner asked folded: the day's
materials ("Documents", "Other records", Oct. 22, 2026). The forces tables under Armed Forces Day (`forces.py`,
`afday.py`: each a `<details>`) are unfolded: a table a kind, its title and date as a caption, no summary to open.
The other folds now in the build, for the owner to rule on one by one: the select, special and joint committees and the
subcommittees (`committee_more.py`), the standing committees' tables (`committee_rosters.py`), the State tables of
State finance (`statefin.py`), the PVI tables under the races (`pvi.py`). Page weight is not a reason to fold: §3
answers it.

## 2. Big threads: subthreads, and promotion

A thread that holds several events at once is split into subthreads; a subthread that grows a life of its own is
promoted to a thread (its `parent:` dropped, the old name kept as a redirect). The index changes with it:

- A parent's dates in the thread index are its own entries only: an entry filed under a subthread (`thread:` the
  subthread) is listed under the subthread's line, not the parent's, unless it is also listed in the parent (`also:`).
  The ⟨⟨ ⟩⟩ line and the highlight keep the family together as now; only the index is pruned.
- A soft warning, `check` [thread-size], names a thread with more than 150 entries of its own in one part of the
  calendar (Vietnam, Opinion, Vietnam: Congress and the President, now), as a prompt to split, never a rule.
- Proposals for the splits come by patch, from the readers (R2 of the reader's brief) and from a thread pass, for the
  owner to rule.

## 3. The calendar split by year

The parts are a list of dates (`split:` in `lists/cal/list.yaml`; `tools/bib/calsplit.py`), so any division costs a line
a part. Proposed: a page a year, `cal1960.html` ... `cal1969.html` (Jan. 1969 to Jan. 20), and the primary seasons,
each with its own index of threads and its seams; the old pages (`cal.html`, `cal63.html`, `cal66.html`) kept as
indexes of their years, so old links land (the router already sends an anchor to the page that holds it). A year at
today's volume is 1–4 MB; a busy year that grows past some 8 MB splits again by half-year, by quarter, by month, by the
same line. The FIRST CITE rule (a work in full at its first appearance in each part) follows the parts. The
abbreviations: "Cal. 1961", not Cal. I.

## 4. Thread statements written once

Today a statement is written for each part a thread has entries in (`c`, `c2`, `c3`), and every new division means
new statements. Instead:

- **The scope, once.** `c` says what the thread is, without its stations: one or two clipped sentences, true of every
  part.
- **The stations from the events.** Each event has a short name, written once on the event (§5: the event record; until
  then, the `short:` of its first entry). A part's statement is the scope and then the events whose dates fall in the
  part, generated: "Stations: Bay of Pigs (Apr. 1961); Mongoose (Nov. 1961–Oct. 1962)". Any division of the calendar,
  any page of a thread, gets its stations for nothing.
- **What is not an event, by span.** A sentence that belongs to some years only is written once, tagged with its span,
  in the syntax the indicators' master already uses (`{{1961..1962-06|...}}`; `tools/bib/concepts.py`, `parse`,
  `ranges`), and shown on every page whose range it meets.
- The conversion: each thread's `c` cut to its scope; `c2`, `c3` turned into span-tagged sentences or into events'
  names; `check` warns on a statement that names a date outside its spans.

## 5. Events as records

An event is now only its first entry and the "See [[id]]" links back to it. An explicit record carries what belongs to
the event, not to a day: `event: <slug>` on every entry of it; the event's name, its span (computed), its
bibliography, its witnesses' trees for what the event as a whole rests on (`notes/extensions/memos/witnesses.md`). The
first entry stops doing two jobs; "See" lines are made from the key; the stations of §4 are the events. Built with the
witness registry, which hangs on the same object.

## 6. The merge

Every patch is audited and merged by hand (32 waiting now). More of the audit becomes `check`: the duplicate by day and
thread, the base drift, the brief's forms (the Names line, the To check, the pinpoints, the claim maps), so that the
merger reads only the conflicts, the flagged duplicates and a sample.

## 7. Finding things on the site

A search and filter in the pages (thread, person, place, date, tag, words), from an index the build writes beside them
and the page fetches when first used, as the day materials are fetched.

## 8. Not now

The regional grouping of the thread index (the owner: "I'll believe it when I see it").

## 9. Order

§1 (small); §2 and §4 with the year split, §3, since the split is what makes §4 pay; §5 with the witness registry
(queue item 0d); §6 as the batches grow; §7 after §3.
