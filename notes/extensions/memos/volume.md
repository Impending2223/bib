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

A table or map in the calendar is shown open, from now on. The forces tables under Armed Forces Day (`forces.py`,
`afday.py`: each a `<details>`) are unfolded: a table a kind, its title and date as a caption, no summary to open. The
folds already in the build stay for now (the owner, Oct. 30, 2026: "Keep the other folds for now"): the day's
materials ("Documents", "Other records", the owner's request of Oct. 22), the select, special and joint committees and
the subcommittees (`committee_more.py`), the standing committees' tables (`committee_rosters.py`), the State tables of
State finance (`statefin.py`), the PVI tables under the races (`pvi.py`). A new table is not folded; page weight is no
reason to fold (§3 answers it).

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
abbreviations: "Cal. 1961", not Cal. I. The contents (the owner, Oct. 30, 2026: "The 'list' should include link-throughs to the months,
headings, and tables on the individual calendar pages"): the calendar's index page, and each year's page, carry the
whole calendar's contents, the months grid and the "Tables and maps" list for every year, each month, heading and
table linked through to its place on its year's page (`contents.py`; the router already sends an anchor to its page).

## 4. Thread statements written once

Today a statement is written for each part a thread has entries in (`c`, `c2`, `c3`), and every new division means
new statements. Instead (the owner, Oct. 30, 2026: the dates, ranges and tagged years "invisible to the human reader.
They're just sorting and redrafting aids"; no "Stations:"):

- **The scope, once.** `c` says what the thread is: one or two clipped sentences, true of every part.
- **The events, from the events.** Each event has a short name, written once on the event (§5: the event record; until
  then, the `short:` of its first entry). A page's statement is the scope, then the names of the events that fall on
  the page, in date order, as a clipped sentence of names ("Bay of Pigs; Mongoose."), each linked to the event's first
  entry; no label, no dates shown. The dates that choose and order them are the events' own and stay hidden.
- **What is not an event, by span.** A sentence that belongs to some years only is written once with a hidden span, in
  the syntax the indicators' master already uses (`{{1961..1962-06|...}}`; `tools/bib/concepts.py`, `parse`,
  `ranges`), and shown, without its span, on every page whose range it meets.
- The conversion: each thread's `c` cut to its scope; `c2`, `c3` turned into span-tagged sentences or into events'
  names; `check` warns on a span it cannot read and on a statement whose text names a year outside its spans.

## 5. Events as records

An event is now only its first entry and the "See [[id]]" links back to it. An explicit record carries what belongs to
the event, not to a day: `event: <slug>` on every entry of it; the event's name, its span (computed), its
bibliography, its witnesses' trees for what the event as a whole rests on (`notes/extensions/memos/witnesses.md`). The
first entry stops doing two jobs; "See" lines are made from the key; the stations of §4 are the events. Built with the
witness registry, which hangs on the same object.

## 6. Parallel readers and the merge

The owner, Oct. 30, 2026, on R29 and R44 of the reader's brief (a work cited in every entry whose claims it bears out;
"already in" no reason to pass over): "we should be more thoughtful about queuing and threading parallel agents, and
merging entries. Is there a performant, compute-economizing solution here? Can you implement it and follow it?"

Where the cost goes now: a reader's edit to an existing entry replaces whole fields (`n`, `src`) against a `base` read
just before writing. Two readers citing one entry, which R29 and R44 make the common case, collide on `n` and `src`
every time; the merge records a conflict, `notemerge.propose` drafts the join, and the merger reads it. Each reader
also reads every pending patch's adds for its days (`grep` and read), and the merger audits every op of every patch.
The 32 patches waiting now are the result.

The fix: most of what a reader does to an existing entry adds something, and additions commute.

1. **Additive ops.** New patch ops, applied to the entry as it stands at merge time, needing no `base`:
   - `cite: {id, item, units, from_to_check}`: puts a work, with its pinpoint and parenthetical, into the run of read
     works (in the build's order), takes its card out of "To check:", and adds its `src` row with the units. A card
     the note already cites at another page: the pages joined ("123, 211"), each row kept.
   - `to-check: {id, add: [...]}`; `check: {id, text}` (a "Check:" sentence, kept if already there); `src: {id, rows}`;
     `via: {id, rows}`; `names: {id, add: [...]}` (the Names line and the `name:` tags together); `also: {id, add}`;
     `witness:` rows, once the registry is built.
   Two readers' additive ops on one entry merge in either order to the same note (`notemerge`'s matching by card and
   by sentence, STYLE 1-3, already does the hard part). `edit` with `base` stays for what is not an addition: `c`, the
   date, the thread, a cite removed; those are rare and still three-way.
2. **A ledger of new entries.** `inbox/new-entries.tsv`, append-only, written under a lock (`flock`): a line an entry,
   before it goes into a patch: date, thread, id, a few words, the patch. A reader adding an entry greps the ledger
   for the day; where the event is there, it `cite`s the pending id instead of adding a second entry. The merge applies
   adds before additive ops, so a cite to a pending id lands. A grep of one file replaces reading every pending patch.
3. **Rolling merge.** A finished patch is merged when it lands, not in a batch: `./bib merge --auto PATCH` runs the
   patch's checks, applies it, and stops only at a real conflict (two edits of `c`, a cite removed by one and pinned
   by another) or a flagged duplicate. The merger reads those and a sample (one entry in ten), not every op. Bases for
   the remaining `edit`s stay fresh; the inbox stays short.
4. **The checks at write time.** `patchaudit`'s refusals, and the brief's forms (the Names line, To check, pinpoints,
   claim maps, the ledger), become `./bib patch-check PATCH`, which a reader runs before it finishes: the patch arrives
   clean, and the merger's audit is the sample.
5. **Scheduling.** Before a batch, `./bib plan-readers CARDS`: each pair of works' overlap, from the entries they
   already share and the spans they cover; works that overlap heavily go to one reader, in sequence (its later patches
   build on its earlier, R49); readers whose works share little run at once. The width of a batch is set so that the
   expected overlap stays low, not to a fixed number of agents.

The 32 patches now waiting are in the old form: merged first, by the audit as it is (queue item 2), before the readers
resume under this. The reader's brief's R49 and R51 take the new ops and the ledger once built.

## 7. Finding things on the site

A search and filter in the pages (thread, person, place, date, tag, words), from an index the build writes beside them
and the page fetches when first used, as the day materials are fetched.

## 8. Not now

The regional grouping of the thread index (the owner: "I'll believe it when I see it").

## 9. Order

§1 (small); §2 and §4 with the year split, §3, since the split is what makes §4 pay; §5 with the witness registry
(queue item 0d); §6 before the readers resume (queue item 0f); §7 after §3.
