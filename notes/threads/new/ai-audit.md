# American Indians: the audit of the placing

The audit was run on Opus. It checks the Sonnet reader's `ai.tsv` against the reader's brief, `notes/briefs/threads-new-ai.md`, rules 1 and 2. Nothing in `lists/`, `th.yaml` or `sources/` was changed.

## What I read

- `CLAUDE.md`, `notes/guide/brief.md`, rulings 58–62 and 75 of `notes/owner-rulings.md`, the thread's entry in `lists/cal/th.yaml` (`cal.thread.american-indians`), the reader's brief, `ai-ids.tsv`, `ai.tsv` and `ai.md`.
- The 23 entries the reader put in the thread. I read each line and note whole, along with the entries it named as doubtful.
- Every row the reader left out whose line or note names a tribe, a reservation, the Bureau of Indian Affairs or American Indians: 46 entries, read whole. These include the Sioux City and Sioux Falls rows, the Navajo, Pueblo, Choctaw, Hopi, Apache and Mohawk rows, the rows on tribes abroad, and the rows with "reservation" and "termination".
- The 15 India rows whose text has "Indians", read at each place the word stands. All 15 mean the people or troops of India.
- A random sample of 40 rows, seed 4271, drawn from the 301 rows outside my first word search, read whole. All 40 are right: India, the Sino-Indian dispute, the Indian members of the Control Commission, or (in two that name tribes) Burma's and North Vietnam's hill peoples.
- Six more rows read whole while I tracked one fault, which is described below.
- In all, 113 rows of the list read whole, and 15 more read where "Indians" stands.
- Twelve calendar entries not on the list, found by my own searches, read whole.

## Checks by script, over the whole tsv

- One row for every id of `ai-ids.tsv`: yes, 376 rows and no duplicates. After the audit there are 378 rows, the two added being the entries found.
- Every slug is in `th.yaml`: yes. `american-indians` is at the top level, with no parent and no children.
- No `also` holds the primary: none does.
- No row adds `american-indians` beside a parent or child: none does. One row keeps a pair the entry already has: `cal.1960-06-27.vietnam-hanoi` has `vietnam-hanoi` as its thread and its parent `vietnam` in `also:`. The row leaves the entry as it stands, so the apply would not change it. I did not mend it, because it has nothing to do with this thread. Ruling 62 (14) set the same default for Comecon.
- Every row keeps the entry's present thread and `also:`, adding only `american-indians`. The three entries that move to the new thread as primary drop their old thread: `states-and-cities` twice and `civil-rights-the-executive` once. Those threads held the entries only for want of a better one. This follows ruling 59's default that an entry that moves does not keep its holding thread.

## Judgments on the reader's 23 entries

- All 23 belong in the thread, and each is placed correctly under rule 2.
- The two primaries are right. The Washington court's Puyallup and Nisqually ruling of Jan. 12, 1967 was filed under "States and cities", which holds what no narrower thread holds. The message on the American Indian of Mar. 6, 1968 was filed under "Civil rights: the executive", which does not fit it.
- The Supreme Court's steps in *Puyallup* and *Menominee* (argued, reargued, decided: five entries) stay under the Court, with the new thread secondary. The Court's thread fits them, so the new thread is not their primary.
- The protest of May 29, 1968 stays primary under the Poor People's Campaign, with the Court and the new thread in `also:`. This is the same placing ruling 75 made, now reached under rule 2. The Campaign's thread is not a holding place. *CQ* files the protest under the Campaign, and the protesters acted for its Indian contingent. So the Campaign fits it, and rule 2 makes the new thread secondary.
- The Campaign's other Indian entries are judged the same way. King's meeting of Mar. 14, 1968 with the tribes' delegates, Udall hearing the Indians on June 3, and the Indians' protest at the Press Club on June 3 are all secondary.
- The Kennedy letter of 1960, the Senate vote and the signing of the Civil Rights Act of 1968 for its Indian titles, Lady Bird Johnson's tour of the reservations, and Robert Kennedy's eight entries are all rightly secondary.

## The mends

There was one kind of fault. For the India entries the reader read only the opening of each line, and it gave two rows the India label that do not concern India. I searched by script for every India row with "Indian" outside any South Asian context, and for every out row with an American use of the word ("Indian problems", "Indian school", "Indian reservation" and the like). Then I read each row that turned up. These two were the only ones:

- `cal.1968-01.robert-kennedy-campaign-decision-9`: Robert Kennedy at Senate committee hearings on Indian problems in California, with Edelman. This row is now in the thread, as a secondary thread. The campaign thread stays primary, because it fits the rest of the line, Unruh's poll and his advice. The entry holds two events, the hearings and Unruh's advice, and it may want splitting. That is outside this assignment.
- `cal.1967-10-21.war-opposition`: John Lewis's "We don't want to play Indian outside the white man's fort" is a figure of speech. The row stays out, and only its basis is corrected.

## The entries found

I searched the whole calendar with words of my own. They were the names of the tribes, the places, the bodies and the people that the thread's entries name: the Bureau, the Commissioners, Udall, La Farge, Hank Adams, Haskell, the Puyallup, Nisqually and Menominee cases and their reporters, *Kautz*, the Department of Game, the Wolf River treaty, termination, Alcatraz, the Alaska Natives' claims, Indian education, the Oahe and other dams, and the other words of the thread. I also searched for every entry that links to one of the thread's entries. Two entries were missed, and each now has a row marked `AUDIT: found`:

- `cal.1967-03-02.states-and-cities-2`: the Washington Supreme Court denies rehearing in *Department of Game v. Kautz*, the Nisqually case of Jan. 12. Its primary thread is now the new one, as with the Jan. 12 entry, since it too was filed under the holding thread.
- `cal.1966-09-23.poverty`: Mrs. Johnson and Udall at San Ildefonso Pueblo, at Head Start, and at the studio of Maria and Popovi Da. The new thread is secondary, and the War on poverty stays primary. This matches how her reservation visits of August 1964 are placed.

I read these and left them out:

- The Senate's passage of H.R. 2516 on Mar. 11, 1968 and the House's on Apr. 10. Their lines are about the bill as a whole and do not name the Indian titles.
- Udall's memorandum of Sept. 2, 1965. Its business is water pollution, and the reservation schools appear in it only as a possible trade.
- Entries that name Indians only in the note: Berry's bill on Jan. 30, 1964; Mundt's Indian jewelry makers on May 13, 1964; an Indian precinct on June 4, 1968.
- The Oahe Dam entries. None of their lines names a tribe.
- H.R. 10256, the land claims along the Colorado River, Oct. 25, 1968. I read the memorandum of disapproval in the American Presidency Project. The claimants are 19 private persons and companies, not Indians.

## The counts after the audit

- Rows: 378, which are the 376 of the list and the 2 entries found.
- Primary: 3, the Washington court's decision of Jan. 12, 1967, its denial of rehearing of Mar. 2, 1967, and the message of Mar. 6, 1968.
- Secondary: 23, the reader's 21 plus the Kennedy hearings in California and the San Ildefonso visit.
- Out: 352.
- Rows marked `AUDIT:`: 4. Two are mends and two are entries found.

## Is the tsv fit to apply

Yes. Every row has a known slug. No `also` holds its primary. The new thread stands beside no parent or child. Each row changes only `thread:` and `also:`. The 40 rows of the random sample were all right, and the one fault that repeats has been searched out over the whole list and mended. The one pre-existing pair of parent and child (`cal.1960-06-27.vietnam-hanoi`) is left as the entry already has it.

Nothing in the audit brief narrowed the work, so nothing was disregarded under R0.
