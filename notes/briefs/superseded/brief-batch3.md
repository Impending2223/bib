# Batch 3: several books an agent (read CLAUDE.md, then brief-common.md, brief-books.md, brief-onebook.md; this brief
# overrides them where it differs)

The owner put some seventy more books into the shared Drive folder on Oct. 28, 2026. You have a group of related
books (your prompt: each book's card and Drive file id, in the order to read them). About twenty-five agents read at
the same time; the merger (the main session) merges every patch by hand, after an audit.

1. **One book at a time, one patch a book.** For each book in turn: download it into your own new directory under
   the scratchpad (`.../scratchpad/b3-<you>/`), `pdftotext -layout` it, and DELETE THE PDF AT ONCE (keep the .txt):
   the disk is small and shared; never hold more than one PDF. An image-only scan: OCR it (`ocrmypdf --sidecar` or
   `pdftoppm` + `tesseract`), then delete the images. Find the page offset on three pages. Then do brief-onebook.md's
   steps 1-4 for that book and write its patch, `inbox/2026-10-29-b3-<short>.yaml` (patch name b3-<short>), with
   `./bib merge --dry-run` clean, and its `notes/book-checks/<card without w.>.md` and
   `sources/cited-records/<card without w.>.yaml`, BEFORE you start the next book. A run may be stopped at any time
   (the owner's working hours: agents stop at 6:46 a.m. Pacific); a finished book's patch survives a stop.
2. **Your books overlap one another, and other agents' books overlap yours.** Within your group, the second book's
   patch builds on the first's: an event the first book's patch adds is an event the second edits once merged; until
   then, in the second book's patch, don't add it again: put the second book's pinpoint in its book-check file under a
   heading "For entries in pending patches" (`entry id | card, page (parenthetical) | units`), and the merger adds it.
   Across agents: before adding an entry, compare it with every entry on its day in the tree (`./bib find -l cal
   --since D --until D`) AND with the adds in the other pending patches (`grep -l "date: 'D'" inbox/*.yaml`, then read
   them). An event already added in a pending patch goes under "For entries in pending patches", not into your patch.
3. **Bases at the last moment.** Read each edit's `base` just before you write the patch (`./bib show ID`); keep every
   cite, sentence and claim-map row other runs wrote; append; re-letter only where `c` changes.
4. **Memoirs.** A memoir (Rusk, Ball, Clifford, McNamara, Califano, McPherson, Humphrey, Nixon, Westmoreland,
   Dobrynin, Bissell, Sorensen, Robert Kennedy's interviews, Guthman) is its author's account: "by Rusk's account",
   "Ball writes"; where the record (FRUS, the Public Papers, the tapes, the Daily Diary) gives the same event, the record
   first; where they differ, "Check: FRUS gives ...". A journalist's narrative (White, Chester et al., Novak, Hess and
   Broder) is a secondary source: date its events by the record where you can find one.
5. **What is an entry.** Brief-books.md and CLAUDE.md hold: the informal record (meetings, calls, staff and campaign
   memoranda, strategy sessions, appointments settled) and the parties' and members' dated word are entries, never
   "minor". The owner's ruling of Oct. 28, 2026 (CLAUDE.md, "The papers of government"): a staff or planning paper, a
   White House staff memorandum, an ambassador's, commander's or consulate's cable and an intelligence memorandum or
   estimate are ENTRIES too, dated by the paper (the record FRUS prints first; else the book, the record behind
   "To check:" as rule A says). Passed over: a covering note or transmittal, a draft not sent, a meeting's preparation, a
   repetition with nothing new, private remarks. A dated event is an entry, not a lead: a lead is only what you cannot
   date or verify.
   AND (the owner's ruling, Oct. 28, 2026, late: too much was being cut as "private", "below the level", "undated",
   "itinerary"; the Suite 3505 reading is the model): an event dated to a month, a season or a stretch of days is an
   entry, dated so (`date: '1961-03'`, or the first day, "Check: the day"), never "undated"; a trip, tour, campaign
   swing or visit is an entry with its places named ("I want to know where these guys went!"); a private meeting,
   call, conversation or letter of a person with a public role on public business or politics is an entry (only
   family and social matters with no bearing pass); the operations, actions and incidents of an event the calendar
   records (the Bay of Pigs' landing and its days) are entries. 
   AND (the owner's ruling, Oct. 30, 2026; CLAUDE.md, "Military matters"): a military operation, action or incident
   the work dates and treats is an entry, whether or not the calendar has it: a named operation, a battle, an
   engagement; a deployment, a unit's arrival or withdrawal, a base opened; a logistical decision or act; an order,
   the rules of engagement; an incident at sea or in the air; an alert, a nuclear accident; every theater. Its
   sorties, losses and strength go in `n` with their pages. "Below the level" only for a unit's routine the work does
   not treat as an event (a patrol without contact). NO BLANKET EXCLUSIONS: every dated event not entered is its own
   row in "Passed over"; never "passed over as minor throughout" or "not listed event by event".
5b. **Keep the raw material** (the owner, Oct. 30, 2026: the later passes need it, "so long as we're not losing the
   raw material for those passes to the cutting-room floor"; code nothing). (a) A position or an argument in the
   source's own words, briefly, with its page, in `n` ("Ball: 'a long protracted war' ([[w.x]], 412)"), not only the
   clipped `c` ("Ball against"). (b) Time and sequence where the source gives them: from Nov. 2, `time:` (UTC, a full
   ISO instant), `time_approx: true` for "that evening", "about 7", and `follows: [<id>]` for "afterward", "then"
   (CLAUDE.md, "The calendar by day"); until those fields are built, the words in `n` ("at about 7 p.m., p. 412"). (c)
   Every figure the source gives (votes, whip and head counts, dollars, troops, polls, tons, sorties) with its page.
   No positions ledger, no warning codes, no scores: those are later passes (notes/extensions/memos/simulations.md).
6. **Copyright.** The books are the owner's copies, for this research: nothing of their text into the repo beyond a
   short quotation an entry needs, marked and cited by printed page; never a paraphrase at length.
7. **Report** under 400 words: per book, the copy and offset, cites pinned or cut, new entries (count, the chief ones),
   records found and read, Passed over by reason, leads; and the patches written. Don't commit, push or merge.
