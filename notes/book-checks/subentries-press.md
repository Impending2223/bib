# News conferences made into subentries: the audit of `2026-11-13-b13-subentries-press`

The reader's patch (worker b13a, Sonnet): `inbox/2026-11-13-b13-subentries-press.yaml`, 5 parent adds and 10 part edits, for the conferences of Aug. 30, 1961; May 23 and Nov. 20, 1962; July 13, 1965; Oct. 6, 1966 (`notes/briefs/batch13.md`, "A and B. Subentries"; `tools/bib/subentries.py`). Audited Nov. 12-13, 2026 (Opus) against the Public Papers' text (`sources/ppp-text/`, each conference's item read whole) and the tree (`./bib show`, `./bib find`). Corrected patch: `inbox/2026-11-13-b13-subentries-press-audited.yaml`, the same `patch:` name, ids and ledger claims, 15 ops, `./bib patch-check` 0 errors, 0 warnings; the reader's file left as it was. Merge the audited file only: the two add the same five ids.

**Counts:** 15 ops; 6 right as written, 9 fixed, none dropped.

## What was checked

Each parent: number, place and hour against the item's note; `time` in UTC (EDT in Aug. 1961, May 1962, July 1965 and Oct. 1966; EST in Nov. 1962); the range against the item's pages (`page`, `page_to`); the parenthetical for the note. All five parents are right in `c`, `n` and `time`. Each part: `part_of`; `follows` against the order of the transcript; the shortened first cite and its pinpoint against the page markers; `c` against the text.

## The patch would have broken `./bib check`

`cal.1962-11-20.missile-crisis` carries `follows: [cal.1962-11-20.missile-crisis-3, cal.1962-11-20.missile-crisis-2]`, entries outside its new parent. Once it is a part, check [subentry] fails on both ("a subentry follows only its siblings"). `./bib patch-check` passed the reader's patch with 0 errors because patch-check does not run `subentries.problems` (`tools/bib/patchcheck.py`; check runs it at `tools/bib/check.py:289`). After a merge the next `./bib check`, and the Pages deploy, would have stopped. Fix: the parent takes the two `follows` (the conference came four hours after both), and the part's own `follows` is unset. Dry-applying the audited patch in memory and running `subentries.problems` gives no new problem; the reader's patch gave these two.

## Fixes (one line each)

1. `cal.1961-08-30.cuba-bay-of-pigs`: "News conference." stripped. It was unit A of its own, so the rows are re-lettered: Sorensen 316, B to A; Kaplan 191, A-B to A; Graham 24-25, A, D-E to C-D. `src.c` 22e558a6.
2. `cal.1962-05-23.medicare`: the reader's strip kept; `src` set with `c` f2be1137 (rows "all", none re-lettered).
3. `cal.1962-11-20.press-and-broadcasting-2` (parent): `follows: [missile-crisis-3, missile-crisis-2]`, moved from the part (above).
4. `cal.1962-11-20.missile-crisis`: `follows` unset. The missing space restored ("at 830 (the quarantine)"). ", at the press conference" struck from unit A, since the parent says it ("Quarantine lifted."). Units unchanged; `src.c` dff4be46.
5. `cal.1962-11-20.civil-rights-the-executive`: the reader set only `part_of` and `follows`. "Same press conference:" struck, since under the parent "Same" points to nothing; `c` now "The housing order. No discrimination ...". The Papers cite moved first in its short form, "[1962 Pub. Papers 830](…), at 831–32, 835" (the order announced, 831-32; effective at once, 835). The old "At the news conference, 6 p.m.: ... (Nov. 20, 1962)." dropped. Units unchanged; `src.c` 0b6640c1.
6. `cal.1965-07-13.court`: "News conference." stripped. It was unit A, so the rows are re-lettered: Branch 261, B to A; diary 295-96, A (the conference, now the parent's) to A (Marshall named Solicitor General, as its parenthetical limits it). Kotz 330 was mapped to E, "Confirmed Aug. 11", but its parenthetical, "the answer, after Ford's charge", is the closing quotation: the Kotz reader counted sentences, not semicolons. Now F, the quotation. Pinpoint "at 736, 742" to "at 736–37, 742" ("the 33d", 737). `src.c` efaba2c2.
7. `cal.1965-07-13.transition-and-staff`: "News conference, watched at the Ranch:" struck whole. Under an East Room parent, "watched at the Ranch" reads as the President's act; it is the diary's vantage, which the note already gives. The Papers read and cited first, "at 737, 743", and "To check: 1965 Pub. Papers." dropped. The Rusk answer requoted from the transcript ("He sits to my right in the Cabinet room. He ranks first in the Cabinet and he ranks first with me."), with "Check: the answer on Rusk as the diary words it, against the transcript's." added. No `src`.
8. `cal.1966-10-06.vietnam-asian-trip`: the reader stripped the opening but left the Papers behind "To check:". Now read and cited first, "at 1117 (the posts; Manila), 1120 (the box score), 1123 (the itinerary; Mrs. Johnson; not the miles, the refueling stop in Alaska or 'the important business')". Bunker's post corrected from the transcript (1117): Ambassador at Large, in Thompson's place. Mrs. Johnson's "Ambassador to the government of Vietnam" is kept in the diary's parenthetical, "against the transcript". The box score requoted ("85 bills out of 90"). "Check: Bunker's post." kept, though the transcript settles it: patch-check refuses an edit that drops a Check (`patchaudit.drops`), so the lead or the owner may strike it. No `src`.
9. `cal.1966-10-06.cities-and-housing`: `src` set with `c` e3865449 (one unit, rows unchanged). Pinpoint "at 1119" to "at 1119–20": the question is on 1119, the words quoted on 1120.

Right as written: the four other parents; `cal.1961-08-30.berlin-and-vienna` (at 573, the Clay announcement); `cal.1962-05-23.immigration` (at 431). Small thing left: immigration's "food already sent" is looser than the transcript's "providing food ... and have been for some years".

## Item 2: the reader's borderline days (each ruled: not a part, as the entry stands)

All three have one shape: another party's act, with the President's comment on it at the conference in the same entry. Each entry's subject (its first sentence, its `short`, its thread) is the other act, so it is not a part, and the reader is right. Each holds two events, though. Split, the President's answer would be a second part on each day, and the day would then want a parent:

- `cal.1961-03-01.africa`: Williams's "Africa for the Africans" in Kenya, earlier, the date unsettled ("Check the date"); Kennedy's answer, Q17, 1961 Pub. Papers 135, at 139. The one part now is `cal.1961-03-01.school-aid-2` (Q27). `cal.1961-03-01.peace-corps` is not a part either: it records the executive order itself (the act), not its announcement (item 5, at 136). Lead: that entry's "Shriver named director" is against the same conference, where Kennedy says the head will be chosen "in several days" (Q9, 137). A Check for that entry.
- `cal.1962-01-24.program`: the Rules Committee's 9-6 vote; Kennedy's answer, Q1, 1962 Pub. Papers 60, at 60-61 (the reorganization plan), and Q8, 62-63 (Weaver if the department is made). The one part now is `cal.1962-01-24.antisubversion-2`. Lead: "Kennedy names Weaver its secretary-to-be and sends a reorganization plan" goes further than the transcript ("If we did receive the authority, I would appoint Mr. Weaver"; the plan sent Jan. 30, as the entry's own note shows). A Check.
- `cal.1966-01-13.jobs-and-wages-transit`: the settlement in New York; Johnson's answer, Q15, 1966 Pub. Papers 14, at 19-20 (the figures in note 8). The one part now is `cal.1966-01-13.cities-and-housing`.

No parent added for any of the three.

## Item 3: five "one part only" days, spot-checked

Taken from the brief's case list, the days with no parent in the patch. Each has one part as the entries stand. On four of them a second conference matter sits inside an entry:

- 1961-04-21: `cal.1961-04-21.cuba` holds the Bay of Pigs ("Victory has a hundred fathers"), a poll ("His approval rises"), and medical care (Q13, 1961 Pub. Papers 307), a second matter on another thread. The other Bay of Pigs entries of the day (the breakfast, Robert Kennedy watching, the office after) are not parts.
- 1961-10-11: `cal.1961-10-11.vietnam` is the NSC's decision and the conference's announcement of Taylor's mission in one ("announced at the press conference"; item 1 and Q10, 1961 Pub. Papers 656, at 656, 660). Split, the announcement is a second part beside `cal.1961-10-11.foreign-aid`.
- 1963-01-24: `cal.1963-01-24.trade` holds the most-favored-nation answer, the Jupiters, the Khrushchev letters' release (a White House act, not the conference's) and the "peculiar logic" answer. Split, that is three parts. The Merchant entry is a separate statement (1963 Pub. Papers 100), not a part.
- 1965-07-28: `cal.1965-07-28.vietnam` holds the war and the Fortas nomination ("Fortas named to Goldberg's seat"): an earlier combine folded `cal.1965-07-28.court` into it (the alias). Split, Fortas is a second part. `cal.1965-07-28.court-2` (the Oval Office, 12:15, Califano's statement) is the preparation, not a part.
- 1967-03-02: really one (`cal.1967-03-02.defense-abm`). Lead: `cal.1967-03-02.states-and-cities` (the governors invited) and `cal.1967-03-02.transition-and-staff` (Luci) each carry "Check: the occasion". The transcript (1967 Pub. Papers 259) has neither, so the occasion was not this news conference.

## Item 4: entries holding two matters (not split here)

- `cal.1961-08-30.berlin-and-vienna`: split it. Unit A, Clay named (item 3, at 573), is the conference's. Unit B, the Soviet announcement of resumed testing, is another party's act, made after the conference: the transcript's Q15 still awaits Dean's report from Geneva, and the White House statement came that night. As a part, B shows under the conference indent. Kept as a part in the audited patch, since its thread, tags and first unit are the conference's. Split, B goes to its own entry (thread `testing`, before `cal.1961-08-30.testing`), and `cal.1961-08-30.testing`'s `follows` is retargeted to that entry. In the same edit, the row for the conference's link (`…#page=630: all`) should become `A`: the conference does not bear B.
- `cal.1961-08-30.cuba-bay-of-pigs`: split it. School aid (Q6, at 574) and *Time*'s version of the invasion (Q26, at 580) are two matters on two threads. The alias `cal.1961-08-30.school-aid-2` shows they were once two entries, folded together. Split, they are two parts: school aid, following `berlin-and-vienna`; then *Time*. The rows divide with them: Graham to school aid; Sorensen and Kaplan to *Time*.

Also holding several: `cal.1966-10-06.vietnam-asian-trip` (the posts, the trip, the Great Society box score) and `cal.1965-07-13.court` (the nomination, with the confirmation of Aug. 11 and the swearing-in of Aug. 24, later events, inside it).

## For the lead or the owner

- patch-check misses check [subentry]. The lead's merges of subentry patches should run `./bib check` before pushing, or patch-check should call `subentries.problems` (a one-line gap in `tools/bib/patchcheck.py`).
- "Check: Bunker's post." (`cal.1966-10-06.vietnam-asian-trip`) is settled by the transcript, but patch-check cannot drop it. Strike it at the merge if the owner agrees.
- The other parents could carry a work on the whole conference as their common bibliography: Mrs. Johnson's diary, 295-96 and 428-29, treats each of the 1965 and 1966 conferences as a whole. Not added; the model of July 19, 1961 carries none.
- On Aug. 30, 1961 two Papers items begin on 572 (no. 333, a White House statement; no. 334, the conference). The parts' short cites carry no title, so the build's APP parenthetical (ppp STYLE 5) may not resolve them; the parent's titled cite does.
- Leads, the conferences' matters no entry holds (not in scope): Aug. 30, 1961, the Belgrade message (573), Goodwin and Executive privilege (574-75), steel prices (576-77), the foreign aid conference (577); May 23, 1962, Billie Sol Estes (433, 434, 436), the cigarette question (436); Nov. 20, 1962, India and the Harriman mission (832-33), the Sylvester and Manning directives (836-37); July 13, 1965, Vietnam (735-36: "Increased aggression from the North may require an increased American response on the ground"), Talbot to Greece and Hare (737), the Geneva disarmament committee (737-38), the poll tax (740-41); Oct. 6, 1966, the segregationist governors (1118), Foley and Davis (1117).
