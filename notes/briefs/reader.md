# The reader's brief

**Draft of Oct. 30, 2026, for the owner to read. Not yet in force.** Until the owner approves it, the rules in force
are CLAUDE.md's and the batch briefs' (the latter kept in `notes/briefs/superseded/`). Once approved, this is the one
text every agent that reads a source against the calendar, or drafts calendar entries, works from; a batch brief adds
only its assignment (the sources, the entries, the patch's name). CLAUDE.md keeps the series' conventions (the files,
the forms, the build) and points here for the reader's rules.

Each rule is numbered (R1, R2 ...). Where each comes from, in the owner's words and dated, is the table at the foot,
"The rulings"; the owner's messages in full are in `notes/owner-brief.md`. To amend a rule: change its text here and
add a row to the table. Never append a ruling to a rule's text.

Part E (what the sources rest on) describes the registry of witnesses, to be built Nov. 2, 2026
(`notes/extensions/memos/witnesses.md`). Until it is built, Part E is not in force.

## A. The work

**R1. What the calendar is.** A calendar of executive and legislative events, and of any other events that left a
trace, or should have left a trace, on the political and policy histories of the Kennedy and Johnson Administrations,
their Congresses, or those of their members. Its span runs from Jan. 6, 1960, to Jan. 20, 1969, plus the primary
seasons of 1972 and 1976. Each entry is a memory aid and a bibliographic record, not a narrative. Each event carries a
bibliography, or points to the entry that does.

**R2. A reading run.** Read one source at a time, in this order:
1. Hold up every cite the calendar already makes to the source (R30).
2. Read the whole source against the calendar over its span. Give each event the calendar holds its pinpoint, and
   enter each event it lacks (Part B).
3. Log what the source rests on (Part E).
4. Log what you pass over (Part F).
5. Write your patch, your book-check file and your report (Part G).

A run may be stopped at any time. Finish each source's patch before you start the next source.

**R3. Read the source itself.** Never write from memory. Every date, figure, name and quotation comes from a page
you have read. Anything you recall but have not verified is a lead (R46), never an entry.

## B. What is an entry

**R4. The test.** A dated event within the span that a thread follows, or should follow, is an entry. When you are
reading a work, its own notice is the test: what the work dates and treats as an event is an entry, whether or not
the calendar holds it yet. Rules R5 to R15 name the kinds of event that readers have passed over; each is an entry.

**R5. The public record.** Messages, addresses, press conferences, orders, proclamations, signings, statutes, votes,
hearings, reports, decisions, elections and appointments.

**R6. The informal record.** These are the transactions behind the public record, for any person with a public role:
- meetings, calls, conversations and letters on public business or politics;
- lobbying and bargains;
- the planning of policy, personnel, operations and communications;
- strategy sessions;
- appointments settled.

They happen in the West Wing, the members' offices and the campaign headquarters, and their record is mostly
memoirs, biographies, oral histories, recordings and diaries. Date each by its source, cite it by page, and say whose
account it is where it is one participant's ("by O'Donnell's account").

**R7. The papers of government.** These are entries, each dated by the paper:
- a staff or planning paper;
- a White House staff memorandum;
- an ambassador's, commander's or consulate's cable;
- an intelligence memorandum or estimate.

**R8. The parties and the members.** These are entries, never "minor":
- what either party does out of the White House: its statements, papers, declarations and platforms;
- its committees' and leaderships' meetings and decisions;
- the founding and doings of its factions and allied groups (Ripon, the Free Society Association, YAF, the ACU, the
  DSG);
- the dated public word on policy or politics (a speech, statement, press conference, interview, or article under
  the person's own name) of any member of Congress, a governor, a party officer, or a party figure out of office.

Threads: Republican Party and its subthread In Congress, Democratic Party, Conservative movement.

**R9. The counterparts.** These are entries:
- the decisions, meetings, papers, orders, envoys and public word of the governments, parties and commands
  Washington dealt with, ally or adversary (Hanoi, Peking, Moscow, the NLF, Saigon, Bonn, London, Havana), on a matter
  a thread follows;
- what Washington did not see at the time: date it by its record, and add "Made public:" where the record was
  private.

**R10. The organized interests.** These are entries:
- the dated public word on policy or politics of the unions and their officers; the business, farm and professional
  bodies; the lobbies and associations; the churches' bodies; the civil-rights and peace organizations; the
  foundations and study groups;
- their dealings with officials and members;
- their acts that start, fund or shape a program, a bill or a campaign the calendar follows (a grant, a study taken
  up, a strike, a contribution);
- the investigations and prosecutions of them.

Threads: Labor for the unions' politics; Labor disputes for strikes; the event's own thread otherwise.

**R11. The parties to an event.** A defendant, a witness or a plaintiff in an event the calendar records, speaking
on that event, is an entry (Hoffa's interviews on his trials).

**R12. The columnists.** Two kinds of column are entries:
- a column by a named columnist (one with an entry in Part III's press sections) on policy or politics, where the
  work being read dates and treats it;
- another journalist's column, but only where it carried an act (a leak, a trial balloon) or made news.

No run of the papers is read. Where a work treats a columnist as a voice and the columnist has no Part III entry,
propose the columnist in your leads.

**R13. Military matters.** A military operation, action or incident that the work dates and treats is an entry, in
every theater:
- a named operation, a battle, an engagement;
- a deployment, a unit's arrival or withdrawal, a base opened;
- a logistical decision or act;
- an order, a directive, the rules of engagement;
- an incident at sea or in the air;
- an alert, a nuclear accident.

**R14. Trips and stretches.** A trip, tour, campaign swing or visit is an entry, with its places named. An event the
source dates only to a month, a season or a stretch of days is still an entry:
- dated to the month (`date: '1961-03'`), or to the first day with "Check: the day";
- never "undated": only what no source dates even to the month is undated, and that is a lead.

**R15. The operations of an event.** The days, stops, actions and incidents of an event the calendar records are
entries (the Bay of Pigs' landing and its days, the Freedom Rides' stops, a campaign's rallies).

**R16. One event, one entry; an entry is an event-day.**
- Each act gets its own entry, dated by its own record: an announcement and the act it announces, hearings and the
  vote, a note and its reply.
- Spans of two or three days are good, under a week tolerable, anything longer suspect.
- A meeting, document or address whose matter falls in several threads is one entry: file it under its chief thread
  (`thread:`) and list the others in `also:`.
- Before adding an entry, compare it with every entry on its day, in every thread (`./bib find -l cal --since D
  --until D`), and with the pending patches. If an entry already records the event, edit that entry.

**R17. What is not an entry.** Only these, and each passed-over event gets its own row in Passed over (R44):
- **out of the brief:** outside the span, or matter no thread follows nor should (another country's domestic
  politics with no bearing on its dealings with Washington, a change of its head of government excepted);
- **minor:** a repetition of a position already entered, with nothing new; private or social trivia (family and
  social matters with no bearing on public business or politics); a unit's routine the work does not treat as an
  event (a patrol without contact, a supply run);
- **the passed-over papers:** a covering note or transmittal, a draft not sent, a meeting's preparation, private
  remarks.

Never "below the level" for anything else, and never a blanket exclusion of a whole class of event.

## C. Writing the entry

**R18. The prose.** Compact, plain and compressed. Record what happened, not what it meant:
- no praise, blame, irony or color;
- short declaratives and fragments, dropping articles and verbs where the line still reads;
- match the register of the section you add to: read a few of its entries first.

**R19. The fields.**
- `c`: what happened, in one to three clipped sentences: who, what, the number.
- `n`: the pointers (Part D).
- `tags`, hidden: a `name:` tag for each person the entry names or whose act it records, if that person has a name
  entry. Tag the President where the entry is his act. Never tag a namesake.
- `state:` and `city:` tags for the States and the cities.
- `place:` and `province:` tags for events in Indochina.
- No `s:`. The id comes from `./bib new-id`.

The places, the diacritics, the election results and the laws in `c` follow CLAUDE.md ("Places", "Vietnamese names",
"Election results", "House style").

**R20. Names.** `n` ends with "Names:" followed by every person in `c` who has a name entry, by surname, commas
between ("Names: Heller, Tobin."). Write the given name where the tagged persons share a surname, and the suffix for a
son or father. Put nothing after the names but a sentence of its own ("Check: …").

**R21. Accounts.** A memoir is its author's account; say so where it matters ("by Rusk's account", "Ball writes").
Never set it as plain fact against another record. Where the record (FRUS, the Public Papers, a tape, the Daily
Diary) gives the same event, cite the record first. Where two accounts differ, give both: "Check: Sorensen gives …".
A journalist's narrative is a secondary source: date its events by the record where you can find one.

**R22. Corrections.** Change `c` only where a record settles the question beyond doubt, and say so ("The Papers date
it Aug. 26."). Otherwise add a Check. Never rewrite an entry beyond what the source needs.

**R23. The raw material.** Code nothing; keep what later passes will code:
- a position or argument in the source's own words, briefly, with its page, in `n`;
- the time and sequence the source gives: `time:` (UTC, a full ISO instant), `time_approx: true` for "that evening"
  or "about 7", and `follows: [id]` for "afterward" or "then" (all three from Nov. 2, 2026; until then, the words in
  `n`);
- every figure the source gives, with its page: votes, whip and head counts, dollars, troops, polls, tons, sorties,
  losses, strength.

## D. Citing

**R24. The order of `n`.**
1. The primary record, read and linked (R25).
2. The works read, each with its pinpoint and, where it stands for only part of `c`, its parenthetical.
3. "Made public:" where the event was done in private and became public later.
4. "To check:" (R28).
5. "See [[id]]" back to the event's first entry.
6. "Names:".

**R25. The primary record.** Cite it first, linked, in the series' forms:
- a statute: "[77 Stat. 56](…)";
- the Public Papers: "Title, [1961 Pub. Papers 1](…) (Jan. 20, 1961)", with APP only where the Papers do not print
  the document;
- the Federal Register;
- the Congressional Record, by chamber and day;
- FRUS, with its volume's title and the document number;
- the U.S. Reports;
- a Miller Center recording;
- a day of the Daily Diary;
- the presidential library's file;
- a State's session laws or canvass.

The series' copies are listed in CLAUDE.md (the daybook, `sources/ppp-matches.json`, the recordings, the diary). A
record found but not readable joins "To check:" with where it is.

**R26. The event's bibliography.** The event's first entry carries its full bibliography; later entries of the same
event point back with `See [[id]]`. An entry that opens a new event within a thread carries its own. Write each work
as its card, `[[w.id]]`, and make the card first if it has none. Never name a list or a section.

**R27. A pinpoint names a number.** A page, a volume and page, a document, a chapter or a note, or a link to the
place read. A pointer in words ("on Rusk", "for the arithmetic") is no pinpoint: the work goes behind "To check:".

**R28. Hard and soft.** The sources read come first, and every work not yet read stands behind "To check:", a
sentence of its own. When you read a work, move it out of "To check:" with its pinpoint. When you find a source and
do not read it, add it to "To check:". "Check:" marks a detail to verify; "To check:" marks sources not yet read.

**R29. What each source stands for.** A source cited under an entry stands for the whole of `c` unless the note says
otherwise:
- Where it does not, say which claim each source is for: a parenthetical after the cite ("[[w.x]], 123 (the vote)"),
  a label before it, or the cite in the sentence it supports.
- Omission implies, determinately: under an entry ABCD, "X; Y; Z (C)" means X and Y stand for A, B and D, and Z
  stands for C and its tie to the rest.
- A source read that does not bear out a claim is no cite for that claim. The claim takes a Check or goes.

**R30. Holding up the cites already made.** For each entry that already cites your source:
- If the page bears it out, pin it and move the work out of "To check:".
- If the page bears out only part, pin it with a parenthetical.
- If the source gives another date, figure, name or account, settle it against a third record if one exists;
  otherwise add "Check: <Surname> gives …".
- If the source does not treat the matter, the cite goes.

Every case that is not a plain "holds" gets a row in your book-check file.

**R31. The claim map.** Each entry's `c` is lettered into units, split at sentence ends and semicolons (`./bib claims
show ID`). For each entry you cite or edit, write its map by patch:
- set `src`, starting from `./bib claims seed ID`;
- give one row per source per page, with the letters it grounds: `'w.card 123: A, C-D'`, `'<the link's address>:
  all'`;
- keep the rows other runs wrote, and re-letter only where `c` changes.

## E. What the sources rest on (from Nov. 2, 2026)

**R32. Witnesses.** A witness is anything that bears on a claim:
- a document, a recording, a transcript;
- a print, an edition or a translation of any of these;
- a statement, a press account, a hearing;
- a study, a memoir, an oral history, an interview;
- a person's testimony.

Works are witnesses (their cards). A documentary collection (FRUS, JMZW, *Current Documents*) is the print of each
document it prints. The registry is `sources/witnesses/`.

**R33. Edges and roots.** Tie each witness to what it derives from, and say how: a copy, print, edition,
transcription, translation, quotation, citation, recollection or report.
- A **root** has nothing identifiable and recoverable upstream for the claim. A claim often has several roots.
- An **open upstream** is a source that is named but not recovered: name it exactly and mark why the branch ends
  (closed archive, not found, not held).
- **Independence** is counted by distinct roots and distinct agents, never by number of works.

The tree is drawn for each unit of `c`, not for the entry.

**R34. Register everything.** Register every witness you meet that bears on a claim, however well attested the
claim already is. A copy of a witness already registered goes in as an edge to it, one line. It never counts as
support, and it is never dropped.

**R35. Follow each branch.** Follow each branch as far as the series can: a card you hold, the daybook's FRUS, the
Public Papers, a recording, the Diary, an open scan. Where you cannot follow it, name the upstream and mark the
branch open. A record the series holds and you have read is cited in `n` as the primary record (R25). An unread one
joins "To check:" with the witness it comes from ("To check: Bundy to Johnson, Feb. 7, 1965, NSF, LBJ Library (cited
by [[w.dallek-flawed-giant]], 251 n.14).").

**R36. Describe each witness.** Record, as the witness gives it, without grading:
- whose account it is (`agent`);
- when it was made (`made`: contemporaneous or later, with its date);
- its form (`form`);
- for each claim it bears on, whether it is firsthand (`knows`).

**R37. Variants.** Where witnesses differ, record each reading against its unit, in the witness's words, with its
page. "Check: … gives …" stays in the note for the reader.

**R38. The record that is the act.** Where the series cites the record that constitutes the act, the unit closes on
that record and needs no tree: the statute or session law, the order or proclamation, the regulation, the reported
decision, the certified canvass, the release of a figure as first reported, the journal of a confirmation.
- It closes only what the record constitutes (the act, its text, its date, its number, the figure). The
  circumstances keep their trees.
- A compilation or a print of a non-dispositive text (the Clerk's *Statistics*, CQ, the *Directory*, FRUS, the
  Record's text of a speech) does not close a unit.
- Witnesses that agree with the record are not sought. One that disagrees is recorded as a variant.
- Where the record itself is in question (a contested election, a date that differs from the act's, a disputed
  validity), the unit is marked `disputed` and takes a tree.

**R39. Already in.** A witness to an entry that already exists is added to that entry's map. It is never a reason to
pass the witness over.

## F. What you pass over, and leads

**R44. Passed over.** Your book-check file has a section "## Passed over". It lists every dated event within the
span that the source treats and you did not enter, one row each: page | date | event, in a few words | why. The
reason is one of the R17 reasons, "already in as <id>", or "to leads". Say how you made the list. Never write a
blanket row or sentence ("minor throughout", "not listed event by event"); `check` warns on one. The owner rules on
the list.

**R45. Pending patches.** An event already added in another pending patch goes in your book-check file under "For
entries in pending patches", as `entry id | card, page (parenthetical) | units`. Do not add it again.

**R46. Leads.** Anything recalled but not placed or verified goes to `notes/leads.md`, under its heading, with the
entry it concerns and where to look: an event without a date, a figure without a source read, a source not reached,
a columnist to propose. Never put it into the calendar unchecked.

## G. The mechanics

**R47. By patch.**
- All calendar changes go in one patch per source (`inbox/<date>-<name>.yaml`).
- Give every edit a `base`, read with `./bib show` just before you write it, and keep everything other runs wrote.
- Run `./bib merge <patch> --dry-run` clean.
- Never edit `lists/cal/*.yaml` directly, never merge, never run git.

**R48. The files.**
- Never read `build/`, nor a whole list. Find entries with `./bib find` and `./bib show`, and read only the lines you
  need.
- Make new cards with `./bib works adopt`, or by the lock script your batch brief names, re-reading the letter's file
  just before writing.

**R49. The copies.**
- Download the owner's copies into your own directory under the scratchpad, never into the repo.
- Read the text layer (`pdftotext -layout`), or OCR a scan and say so.
- Delete the PDF at once and hold one at a time.
- Find the offset between PDF pages and printed folios on three pages, and cite by the printed page.

**R50. Copyright.** The books are the owner's copies, for this research. Put none of their text into the repo beyond
a short quotation an entry needs, marked and cited by page, and never paraphrase at length.

**R51. The network.**
- Never get around a bot check; record a refused host as a lead.
- Never disable TLS.
- Never read presidency.ucsb.edu or discoverlbj.org, nor PRDE's transcripts.
- Run Python with `-I` on downloaded data.
- Never write a key anywhere.

**R52. Pronouns.** No gendered pronoun for an author in a note: use "the note" or the surname.

**R53. The report.** Under 400 words, per source:
- the copy and its offset;
- cites pinned, cut and disputed;
- new entries (the count, and the chief ones);
- witnesses registered (roots, open upstreams, variants);
- Passed over, by reason;
- leads;
- the patch written.

R40–R43 are left free for Part E's additions once the registry is built.

## The rulings

The owner's words behind each rule, or "house rule" where a rule is the series' practice and no ruling of the owner's. Dates are 2026. "OB" is `notes/owner-brief.md`, which has the messages in
full; "CL" is CLAUDE.md, where the later rulings are quoted.

| Rule | Ruling | The owner's words |
|---|---|---|
| R1 | Oct. 1 (OB, "The prose") | "a calendar of executive and legislative events, and any other events that left a trace, or should have left a trace ... a memory aid and a bibliographic record, or a set of bibliographic pointers" |
| R1 | Oct. 1 (OB, "The calendar extended") | the span; later extended to Jan. 6, 1960 and Jan. 20, 1969 (CL, table) |
| R3, R46 | Oct. 18 (CL, "Leads") | anything recalled but not placed or verified goes to the leads, "never into the calendar unchecked" |
| R4 | Oct. 29, Oct. 30 (CL) | "the work's notice is the filter" (the columnists); the same test for operations |
| R6 | Oct. 23 (OB, "Scope") | "The sinews of the public history: informal meetings, informal lobbying, informal agreements, informal policy and personnel and operational and communications planning." |
| R7, R17 | Oct. 28 (CL, "The papers of government") | on the Gibbons readings: the staff papers, cables and estimates are entries; transmittals, drafts not sent, preparations, repetitions, private remarks passed over |
| R8 | Oct. 29 (CL, "The parties and the members") | "What rule makes this kind of position-taking ... 'minor'? Can we amend it?"; "I'm quite interested in what the Republicans were up to, and what they were saying, in these years" |
| R9–R12 | Oct. 29 (CL, "Out of the brief") | on Asselin, Chen, Zhai, Nguyen, Sundquist, Schlesinger: "or should have left a trace" takes in what Washington did not see; "Give me the lobbies and foundations too. And Hoffa!"; the "name" columnists |
| R13, R17, R44 | Oct. 30 (CL, "Military matters") | on the services' and the Joint Chiefs' histories, which passed over operations "as minor throughout" |
| R14, R15, R17 | Oct. 28 (CL, "What is passed over at all") | too much cut as "private", "below the level", "undated", "itinerary"; "I want to know where these guys went!"; the reading of *Suite 3505* the model |
| R16 | Oct. 20 (CL, "Spans"); Oct. 28 (CL, "One event, one entry") | "One entry, listed in both threads" |
| R18 | Oct. 1 (OB, "The prose") | "Compact. Plain. Compressed. Springs and Autumns, but without the subtle words." |
| R19 | Oct. 12–23 (CL) | the places (Oct. 12); the election results, "a single, prescribed standard" (Oct. 23) |
| R20 | Oct. 14 (CL) | "Names, events"; no list or section after the names |
| R21 | Oct. 23 (CL, "The informal record") | "name whose account it is"; "where accounts differ, say so" |
| R22 | Oct. 5 (OB, "Check") | "write 'Check' ... so it can be looked up/verified later" |
| R23 | Oct. 30 (CL) | "so long as we're not losing the raw material for those passes to the cutting-room floor"; the time fields (the owner, Oct. 29–30: UTC; a flag for an approximate time) |
| R24, R25 | Oct. 2 (OB, "Primary records"); Oct. 22 (CL, "The Public Papers") | "link the bibliographic notes under each event to the relevant primary records"; the Papers' cite over APP's |
| R26 | Oct. 1 (OB); Oct. 13 (CL) | "a bibliography for each event, if not each entry"; one A–Z list, no sections; the cards |
| R27 | Oct. 30 (CL, "Hard and soft") | a pinpoint names a number; a pointer in words is recalled |
| R28 | Oct. 23 (OB, "Citation") | "separate the hard sources ... from the 'soft' sources"; "put a 'To check: ' in front of all the as-yet unread 'soft' sources" |
| R29, R30 | Oct. 23 (OB, "Citation") | "be precise about what the cited source states"; "Implication by omission permitted if disciplined and determinate" |
| R31 | Oct. 28 (CL, "Claims and their sources") | "break the entries down into (invisible?) sentence-by-sentence, clause-by-clause units, and accord to each the appropriate (invisible?) pincite" |
| R32–R37, R39 | Oct. 28 (CL, "What the works rest on"); Oct. 30 (memo, witnesses.md) | "a trace/map of *all* the *ultimate*, or *root*, materials that bear on a fact or event"; "even after a fact or event is 'sufficiently' attested"; "Don't drop the first rule" |
| R38 | Oct. 30 (memo, witnesses.md §2a) | "Where we have the record, and the record is sufficient and complete attestation ... the 'witness' collapses to the record itself" |
| R47, R48 | the series' practice (CL, "Changing things", "Do not") | none: house rules, not rulings |
| R49, R50 | the series' practice, since the owner's copies of Oct. 23 (CL, "Do not"; the batch briefs) | none: house rules |
| R51 | the sites' own terms (robots.txt; the bot checks); CL, "The Public Papers", "The calendar by day" | none: house rules |
| R52 | the series' practice (the batch briefs, Oct. 29) | none: a house rule |
