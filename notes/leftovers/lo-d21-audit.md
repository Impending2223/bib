# lo-d21 audit (Nov. 28, 2026)

The Opus audit of the reader's patch `inbox/2026-11-27-lo-d21.yaml` (leftovers for March to June 1968, batch 21) and its note `notes/leftovers/lo-d21.md`. The patch is corrected in place and passes `./bib patch-check` with 0 errors and 12 warnings (the three split entries flagged as duplicates, and six edits that set only `n` because they take sentences out). Nothing was merged, built or committed. Printed pages throughout. Nothing in the brief narrowed what is an entry, so nothing was disregarded under R0.

## What was read

Every copy was fetched from the Drive by its download address, read on its page, and deleted. The offsets were checked on the folios each time.

- Witcover, *85 Days* (printed = PDF − 2): 68, 70, 74, 86, 91–92, 122–24, 139–40, 145–46, 181, 196–97, 213–17, 240, 282, 285–86.
- Schlesinger, *Robert Kennedy and His Times* (printed = PDF − 40): 872, 874, 878–79, and the notes of ch. 39 (n.71, Chester 145; n.79, the Lindsay interview and Sheridan's letter).
- Chester, *An American Melodrama*: 143, 145 (in the text layer).
- Solberg, *Hubert Humphrey* (printed = PDF − 4): 325–26.
- Lady Bird Johnson, *A White House Diary* (folio at the foot): 646–48, 669–70, 673–75, and the entries from Apr. 4 to Apr. 30, 1968 (none for Apr. 23).
- Humphrey, *The Education of a Public Man*: 360–62.
- Califano, *The Triumph and Tragedy of Lyndon Johnson*: 273–74, 289–90, and the source notes, 376 (ch. 18, n.4 cites the Daily Diary of Apr. 23 and Temple's oral history), the notes page read on its image.
- White, *The Making of the President 1968*: 162–63, 232.
- Branch, *At Canaan's Edge* (printed = PDF − 40): 724–27, 741–43, 759–64.
- Kotz, *Judgment Days* (printed = PDF − 34): 399–400, 405–07.
- Young, *An Easy Burden*: 463–64, 486.
- O'Brien, *No Final Victories*: 219–23, 241–42.
- Palermo, *In His Own Right* (printed = PDF − 19): 138, 151, 215, and the notes, 295 (nn.33–37; the new wire entries cite them as "296", which is wrong: the notes are on 295).
- Schlesinger, *Journals*: 285–86 (the Apr. 3 entry, read on its image), 288–89 (May 25).
- Shesol, *Mutual Contempt*: 428. Thomas, *Robert Kennedy*: 368.
- Yang Jisheng, *Tiandi fanfu*, I (printed = PDF − 4): 442–45. The Mao nianpu (EPUB), VI, Mar. 22–25, 1968.
- Brezhnev's working notes, the Drive file without a volume number: printed 256 (May 6, 1968).
- *Zhou Enlai waijiao huodong dashiji*: 526, read on the page image.
- *77 Conversations* (the Wilson Center's PDF): 135 n.202.
- Online: FRUS 1964–68, VI, doc. 176 and its notes (from `sources/frus-text`); the Public Papers, 1968–69, I, 609–10 (from `sources/ppp-text`); the Oregon *Official Abstract of Votes, Primary Election 1968*, 34–36 and iii, from the Secretary of State's records site, read on the page images; the President's Daily Diary for Apr. 4, 1968, images 11–13, from the National Archives Catalog.

## Ops checked, and what changed

All 43 of the reader's ops were checked against their pages; the patch now holds 47 (four added: the add-words of Apr. 2, the to-check of Apr. 23, a follows and a check of Apr. 4 and 3). Every `edit` base was compared with the tree as it stands now; all 27 are current.

Held as written: Mar. 5 (O'Brien 220, the last hour before the 5 o'clock deadline), Mar. 7 (O'Brien 221, "that morning"), Mar. 13 (Witcover 70 and White 162, about 4 p.m.), the Mar. 19 correction of the place to Washington (O'Brien 222–23; Shesol 428 has him canvassing in Massachusetts before), the Mar. 22 Check (the Mao nianpu has the order on Mar. 22 and Lin Biao's announcement on the 24th; Yang Jisheng has the meeting at 1 a.m. on the 23rd), the Mar. 24 "By Mar. 24" (Yang Jisheng I, 444–45), the Mar. 26 move of King's night at the Logans' to Mar. 25–26 (Branch 725–27; Kotz 400), Apr. 3 (Schlesinger's journal, 286, "about 7 this evening"), the move of the entertainers to Apr. 8 at about 10:30 p.m. (Witcover 146), May 6 (Brezhnev, 256: the Defense Council 11:00 to 15:00), May 14 (Kennedy's broadcast "that night", Witcover 197), May 18 (the diary, 674–75), May 21, May 25 and May 27 (the Checks; Witcover 213–17 and Schlesinger's journal, 289, bear them), June 1 (Witcover 240, 6:30 p.m. Pacific), June 5 (Witcover 282, 285–86), June 21 (the dashiji, 526, 11:45 a.m.), the June 29 variant (77 Conversations 135 n.202), the three Apr. 4 entries' removals of the moved sentences and tags, the Muncie variant moved to the boarding entry, and the follows links on Mar. 26 and Apr. 9.

Changed:

- The three splits of Apr. 4. The boarding at Muncie (`elections-1968-5`) is borne by Schlesinger 874 and Witcover 139; its line now says "Muncie." without the State, which the thread's earlier entry of the day gives. The old Muncie entry cited Witcover 139–40 for "the afternoon"; Witcover 139 has the rallies but no hour and not the young man's question, so the cite is now 139 with that parenthetical. The Eskridge entry (`king-memphis-3`): Branch 764 has Young back from court "About five o'clock" and Eskridge walking in later, as the motel television turned to the network news, with King logged going upstairs at 5:40. So the line no longer gives Eskridge's word "About 5 p.m."; it gives Young's return about 5 p.m., and the field is a record range from 5 to 5:40 p.m. Central in place of a time of 5 p.m. Eskridge has no name entry, so he is out of "Names:" and Young is in, with his tag; the hearing transcript, which is the hearing's record, is out of this entry's note. The dinner's closing (`democratic-party-2`) holds (Humphrey 361–62; Califano 274; the diary, 648).
- The dinner of Apr. 4 (`democratic-party`). The President's Daily Diary for Apr. 4, image 12, is read and cited first. It has Mrs. Johnson planning dinner at 8:15 p.m. "so they could eat before going to the Congressional dinner", and at 8:20 p.m., on word that King was dead, the President deciding "not to go to Congressional Fund Raising Dinner". This settles Humphrey's "Tuesday" as a slip. "Names:" is now last in the note and names King alone, Humphrey's tag having gone to the closing.
- Apr. 2, "every establishment in America against me". The reader's move to Apr. 3 is struck. FRUS 1964–68, VI, doc. 176, dates Kennedy's meeting with Johnson Apr. 3, and its note 8 dates Humphrey's meeting, right after it, by the Daily Diary. But that dates the meetings, not the dinner. Only Solberg ties the Waldorf dinner to "That night" after it, and Solberg's passage follows Chester's words. Chester (143, 145) has the dinner "On Tuesday evening, after a brief chat with the President", and the remark on Kennedy's plane the same night. And the tree has Kennedy flying back from Philadelphia with reporters on the night of Apr. 2 (`cal.1968-04-02.robert-kennedy-campaign-primaries-2`, from Witcover 135, a page not re-read here). Schlesinger's own "April 2" cites Chester. No record settles it, so the entry stays on Apr. 2, now "Apr. 2, night" with the night band. The occasion goes into the line by `add-words` from Chester 145, Humphrey is named and tagged, and a Check names both readings. The Waldorf dinner (`cal.1968-04-03.elections-1968-5`) is settled the same way: not moved, and a `check` op records the same evidence beside its Check.
- Mar. 16. The old note (`elections-1968-4`) keeps, behind "To check:", the two wires Palermo's notes give for its own two sentences (138 nn.37 and 34). The CBS wire (n.33) stays with its own entry. The forward pointer and the split sentence go, as the reader had them. In the Check on `robert-kennedy-2`, the 10 a.m. announcement is Witcover 86, now named.
- Mar. 25. The old note is the Wise Men's first entry and keeps the event's bibliography (R29); the FRUS links of docs. 156–158 and the pointers go, as the reader had them. Two parentheticals still named the old unit "H" (Johnson's words to Wheeler and Abrams of Mar. 26). They now say what they mean.
- Mar. 30. The reader replaced the Check on the meeting's length with the sentence "the two count different things". No record says so: Kotz 407 has "the ten-hour meeting", with King coming back to it; Branch 743 has eight hours of recriminations after King left. The Check stays, reworded to say both.
- Apr. 8–9, King's associates. The range now starts at about 10:30 p.m., after the entertainers (Witcover 146), not at 10 p.m.
- Apr. 23. Califano's note to the dinner (290; the notes, 376, n.4) cites the Daily Diary of Apr. 23 and Temple's oral history. Both join "To check:", and the Check says so. White 232 gives no place for the Hughes and Miller dinner, so the Check no longer says New York.
- May 15. The Papers' note giving 11:37 a.m. is on 610, not 609.
- May 28, Oregon. The counts read from the abstract's page images: Democratic, Johnson 45,174, Kennedy 141,631, McCarthy 163,990, and write-ins for Reagan 3,082, Rockefeller 2,841, Humphrey 12,421, Wallace 957, Nixon 2,974 (34–35); Republican, Nixon 203,037, Reagan 63,707, and write-ins for Rockefeller 36,305, McCarthy 7,387, Kennedy 1,723 (36). The abstract prints each column's total but no total for the office. Its summary (iii) gives only the 725,431 who voted. So the shares are of the sum of every column printed, write-ins included: 373,070 Democratic and 312,159 Republican. The words now in the house form: Nixon over Reagan, 203,037 to 63,707, 65.0 percent, Rockefeller 36,305 by write-in, 11.6 percent; McCarthy over Kennedy, 163,990 to 141,631, 44.0 percent, Johnson 45,174, 12.1 percent.
- May 21, Illinois. The note's account of where the Blue Book was sought adds the Illinois Digital Archives.
- Added: a `follows` link putting Kennedy's Indianapolis rally after the boarding at Muncie (the boarding's own words show the order), and the `check` on the Waldorf dinner above.

Struck: the move of the Apr. 2 remark to Apr. 3, and the "count different things" sentence of Mar. 30. Everything else the pages bear.

## The four rows matched by day

Each op lands on the entry its item means: Mar. 5 on the Massachusetts filing day (`elections-1968-4`); Mar. 13 on the meeting at Smith's apartment (`elections-1968`), the Clifford call (`robert-kennedy-campaign-decision-6`) already ranged and linked; May 7 on the coffee-shop entry, whose time stays the first act's, about midnight (it carries no `time_zone`, which a later pass should give it: Indianapolis); and May 14 on Kennedy's broadcast from Omaha. McCarthy's broadcast that night has no place on Witcover's page, so it has no zone.

## Duplicate flags for the merge

The merge should settle all three as distinct (`./bib resolve ID --take keep`): `cal.1968-04-04.elections-1968-5`, `cal.1968-04-04.king-memphis-3`, `cal.1968-04-04.democratic-party-2`. Each is a separate act of the day, split off under R17 and R25b.

## What still waits

- Nebraska's *Official Report of the Board of State Canvassers*, 1968 (May 14): govdocs.nebraska.gov resets the connection. The Wayback copy exists (Oct. 30, 2026), but web.archive.org itself fails from this host (the proxy reports the tunnel closed). Nothing on the Drive, and archive.org's search finds no copy.
- The *West Virginia Blue Book*, 1968 (May 14, governors): wvlegislature.gov resets, and the Wayback copy can't be reached for the same reason. archive.org's copy (`westvirginiablue0000vari`) is a restricted loan: its files are private and its search inside the book answers "Item not available". Nothing on the Drive.
- The *Illinois Blue Book*, 1969–70 (May 21): ilsos.gov refuses this host, and cyberdriveillinois.com does not answer. The Illinois Digital Archives (idaillinois.org) has no Blue Book collection among its 266, and archive.org has none for these years. The Wikipedia links stay until it is read.
- The Daily Diary for Apr. 23: the National Archives Catalog holds only 50 days (here Mar. 31 and Apr. 4–7, 1968), and its image server serves no other frames (tried by frame number). discoverlbj.org refuses this host, and its robots file bars Claude. Califano's note shows the Diary bears on the day; it waits for a copy.
- The Salt Lake City bomb scare (Mar. 28): no second record. The days of the Portland rally and of McCarthy's ADA speech (May 25 or 27) and of O'Brien's memorandum (Mar. 18 or 19) also stay under their Checks: no record reached settles them.
