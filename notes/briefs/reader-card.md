# The reader's card (Nov. 10, 2026)

One page for row-by-row reading: re-ruling a book-check's rows, reading a page against an entry. It stands in for the full brief (`notes/briefs/reader.md`, R1–R54); open the brief only for a case the card does not settle, and say which rule you used. CLAUDE.md (the core) and this card are all you need to start.

## The test: ask these of what the page records, in order

1. **Is it dated, and in the span?** A day, or a looser date ("after the convention": an entry with "Check: the day"). Between Jan. 6, 1960 and Jan. 20, 1969 (the primary seasons of 1972 and 1976 too). Undated even to the month: a lead.
2. **Who acted, who was there, who arranged it?** An officeholder, a candidate, a party or movement figure, a member's or the President's staff, a foreign counterpart, an organized interest, the press: then it can bear on politics or policy.
3. **Was it done before the public or for it?** The press, cameras, a crowd, a staged appearance, a statement, a publication, a broadcast. Yes: an entry, whatever the activity was.
4. **Was public business or a political career said, done, asked, granted or drafted, even in private, even in passing?** A remark, a favour, a complaint, a confidence, a vote asked about, a draft of a speech or statement by a principal or for one. Yes: an entry (the informal record, R7).
5. **Only if all of 2–4 come up empty**: a family or social matter with no bearing on public business or politics, a covering note, a draft no principal wrote or used, a meeting's preparation, a repetition. Passed over, with those words as the ground (R18).

Judge by who, arranged by whom, before whom, and about what. Never by the name of the activity ("a ride", "a party", "a lunch", "a letter", "a family matter"). Where in doubt, enter it: the owner's rulings lean in.

## Examples (the owner's rulings)

- Johnson puts Humphrey on a horse at the Ranch, after the 1964 convention, in a rancher's outfit too big for him, before "an acre of cameramen and reporters": **an entry**. The President stages the ticket for the press; the subject being a horseback ride is beside the point. (Ruled "private" twice; the owner, Nov. 10, 2026.)
- Rodino asks Kennedy to see his son; Robert Kennedy: "How did Libonati vote?"; Libonati: "my political career is over": **entries** (a favour asked of an officeholder; private talk of votes and careers).
- Busby's draft of the address to Congress: **an entry** (a principal's speech, drafted), dated to the draft.
- Johnson at Dirksen's Christmas party, at Mansfield's surprise party, at the Texas delegation's lunch: **entries** (social occasions among the principals of pending business).
- Humphrey, called off the Senate floor on June 17, 1964: his son has cancer and faces surgery; he stays for the civil rights debate: **an entry**. A family matter met by a principal's choice in public business bears on it. (The pilot and the audit split; the owner, Nov. 11, 2026.)
- A family illness, a wedding, a holiday, with nothing done or said of public business: **passed over** ("family matter, no bearing on public business").

## Writing it

- One event, one entry. Never two in one: a flight and the briefings at its end, an announcement and the act, a toast and the talks, dinners on several days. Split them, each with its own day.
- Cite only what the page bears. A cite, and each unit of a claim map, stands for what the page itself says; where it bears out part of `c`, say which part ("(the vote)") and put "Check:" on the rest. Never map a unit the page does not state, however likely.
- Map a unit only when the page states every fact in it: the who, the what, the number, the day, the words. Read the unit's text (`./bib claims show ID`) beside the page before you write its letter. Where the page bears only part of a unit, write `units: '?'` and say in the parenthetical what the page bears and what it does not ("(the vote; not the hour or the speakers)"). A unit the page disputes takes a `variant`, never the letter. (The audits of Nov. 11, 2026 found a quarter of the readers' unit maps claiming more than the page.)
- A `check` or a `variant` records a disagreement: the page says something that a unit of the entry says otherwise (another day, number, speaker, wording). What the page adds that the entry lacks, or leaves out, is no disagreement: say it in the cite's parenthetical. A different count of a different thing (a week's dead against one battle's) is no variant; Saigon's date against Washington's for the same act is none either.
- Cite the entry whose event the page tells: compare the page with the entry's `c`, not only its date and thread. A neighbouring entry on the same day (the order, the ships, the alert) is not the instructions to the embassy.
- Visibility (notes/proposals/visibility-spec.md; the program does most of it): where a claim names a country outright and no person or place in it does ("the U.S. bandits", "Moscow's line"), tag the entry `polity:us`, `polity:ussr`, `polity:prc`, `polity:fr`, `polity:frg`, `polity:uk` (others: `polity:drv`, `polity:rvn`, ... as the spec's list). For a private document you cite (a FRUS document, a cable, a memorandum of conversation), give its sender and recipients in the parenthetical where the record's heading names them ("(Rusk to Lodge)"). Never `state:` for a country: that is a US State.
- Before adding an entry, search the calendar for the event on its day and the days around it (`./bib find WORDS -l cal --since ... --until ...`): two of every ten new entries in the audits were events the calendar already held, under another thread.
- `c`: who, what, the number, in one to three clipped sentences; the source's words in quotation marks where it quotes. Say only what the page says (a hat is not a whole outfit); name in `c` everyone `Names:` lists, and list everyone `c` names.
- `when`: a date as the work gives it, never with a question mark; a loose date takes "Check: the day" (or "the month") in `n`.
- `n`: the primary record if the page names one you can link; the work by its card and the page you read (`[[w.card]], 307–08`), read off the page image as well as the text; "To check:" for what the page cites and you did not read ("(cited by [[w.card]], 308 n.4)"); `Names:` the persons with name entries; "Check: the day" where the date is loose. `name:` tags for them.
- Already in the calendar (`./bib ledger find DATE`, `./bib find WORDS -l cal --since ... --until ...`): cite the work under it (the `cite` op). If the page says otherwise (a day, a number, a speaker, the words): a `variant` op or a `check` op, and the cite for what it bears out.
- A work with no card: `./bib works new` first. A new entry: `./bib new-id`, then `./bib ledger add` before you write it.

## Mechanics

Work outside the repository until you are done: write your patch, your witnesses and any by-work edges in your own scratch directory, and move the patch into `inbox/<date>-<batch>-<short>.yaml` and the witnesses into `inbox/witnesses/` under the same name only at the end, once they check (a half-written file in the tree stops everyone's merges and keeps the tree from being committed). Claim new ids in the ledger as you go (`./bib ledger add`). `./bib patch-check` once at the end of each file, not after every op. Never run `./bib merge`, not even in a copy. Never commit. Keep your scripts and copies in your own scratch directory; delete the copies when done. Stop at a clean point at the time your brief gives.

Last message: per work, the patch and its size; each row's ruling in a table (row, ruling, entry or ground); the rows you could not settle and why; any rule you had to look up.
