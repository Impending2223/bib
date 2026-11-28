# Audit of leftovers batch lo-d23

Patch audited and corrected in place: `inbox/2026-11-27-lo-d23.yaml` (now 81 ops: 45 new entries, 24 edits, 12 additive ops). Witness rows: `inbox/witnesses/2026-11-27-lo-d23.yaml`, held as they stand. `./bib patch-check`: 0 errors, 80 warnings (the duplicate flags and the "one event?" notes on the new entries, the "sets only n" notes on the edits, the polity and place tags). Every edit's base was checked against the tree twice, at the start and at the end of the audit; all 24 are current. Nothing was merged, built, committed or pushed; `lists/` and `sources/` were not touched. Every copy was fetched from the Drive by the download address, read, and deleted.

## What was read

- The two NARA records the owner supplied, as page images, every page: Belin's interview of Edwards, Apr. 9, 1975 (178-10002-10352, memo pp. 1–11), and Edwards's Church Committee testimony, May 30, 1975 (157-10002-10048, pp. 1–24).
- Kallina, *Kennedy v. Nixon*, 93 and 151–55 (the folio is at the foot of the page; checked on the image).
- Branch, *Pillar of Fire*, 517 and 611, and the note to 611 (Int. Susannah Heschel, Nov. 15, 1990; int. Sylvia Heschel, Feb. 4, 1991).
- Branch, *At Canaan's Edge*, 160–70 (the folio at the head of the page).
- Kotz, *Judgment Days*, 323–24.
- Gibbons, III, 77 and 431, with their notes.
- Califano, *Triumph and Tragedy*, 89–91 and the notes to chapter 4 (nn.13, 14, 19).
- Taylor, *Swords and Plowshares*, 332 (checked on the image).
- FRUS 1964–68, II, docs. 29, 42 and 43.
- The House's Record of Mar. 17, 1965: 111 Cong. Rec. 5261 (met at noon), 5324 (adjourned 6:42 p.m.), 5325 (H.R. 6400, by Celler, to Judiciary).
- The eight Miller Center pages of Feb. 10, 1964, and the catalogue's hours in `daybook/recordings/millercenter.yaml`.
- Brezhnev's workbook, II, 115–18, the text layer and the page images for every hour.
- Yang Shangkun's diary, I, 558–59; Wu Lengxi, *Shinian lunzhan*, 365–67; the Deng nianpu, III, 1580–81 and 1909; the Zhou nianpu (2020), III, 22 and 28; the Peng Zhen nianpu, IV, 475. All read as page images.
- Not read by the audit: the Ye Jianying nianpu, II, 935 (the reader's reading stands in the Check on `cal.1966-03-18.china-leadership-6`); Garrow, 413 (an older cite, unchanged).

## The ops, by matter

**Feb. 10, 1964, the eight calls.** Each summary, tape and citation number holds against its Miller Center page; the hours are the catalogue's (the pages give the date, Feb. 10, but no hour; their titles read Feb. 11). Changed: the hour now said to be the catalogue's; Arends, named in the 8:37 call, tagged and named. The `follows` links: kept where the lines show the order (8:25 after the vote; 8:37, the draft read, after 8:25, the draft asked for; 8:40, "Salinger is doing it now," now after 8:25; the second 8:42 call after the first, by the tape's order; 10:00, the final count, after the vote). Struck where only the catalogue's clock gave the order, which the clock already gives (8:42 after 8:40; 10:10 after 10:00), and the 10:10 call's "See" to an unrelated call of that morning.

**Oct. 14, 1964.** Branch, 517, bears both entries: Reedy "soon" confirms to reporters in New York, after the wire's 8:09 p.m.; "at 10:15" the follow-up announcement. Changed: Reedy's entry takes the evening range instead of `ok:fields-time`; a broken link (single brackets) mended.

**Kallina.** Every page holds: 93 for Goldwater (the new entry of July, "Just before the convention," holds); 153 for the call, Mitchell's sentence of Monday, Oct. 24 and the release of Oct. 27; 154 for Robert Kennedy's call after Vandiver's word and King's thanks; 155 for King Sr.'s "suitcase of votes." No change.

**The Edwards records.** Every cite was held against its page. Changed:
- `cal.1960-09.cuba`: the two records now stand ahead of the works, as records read (R39), their parentheticals rewritten to say what they bear (Bissell's request and the chain from Maheu to Rosselli; not the month, the Plaza Hotel or the day). "August" is only Schwarz's question; Edwards answers "I was approached by Mr. Bissell" (5).
- The Check on the date, rewritten: in the testimony Edwards does not agree to the fall of 1960; he agrees the contact was before the Bay of Pigs and answers Schwarz's "fall of 1960" with "Oh." (4). In the interview the Bay of Pigs is p. 2 alone.
- `cal.1960-09.cuba-3`, the $150,000: the testimony bears it only as the Inspector General's report, read to Edwards by Schwarz (8–9). The reader had Edwards say the money was the syndicate's; he says only that, as he recalls, it was the syndicate that wanted Castro out of the picture (9). The figure is now a sentence of the line, attributed to the report; Edwards's remark is a gloss paragraph (R19b).
- `cal.1962-04.cuba-2`: Edwards's memorandum, read into the record (20), says "In early April": the entry now `Apr., early`, `at: before 1962-04-11`.
- `cal.1962-05-07.robert-kennedy`: "at least half an hour" (interview, 7) added to the line as Edwards's account.
- The Papich entry (`cal.1962.cuba`): it holds (testimony 14–15; interview 6, "at the same time I briefed Papich," 1962 to Belin's question). Added: the testimony's p. 18, where Schwarz places the meeting after McCone succeeded Dulles, and a Check on the year, since the testimony takes up the visit to Papich after the Las Vegas tap.
- The Inspector General's interview (`cal.1967.cuba`): it holds (7–8, 11). Struck: the tag and name of Johnson, who is not in the line or the record. Added: Earman, whom Edwards names (8). Its forward pointer to May 23 now points back to `cal.1967-03.cuba`.
- The two witness rows are right as they stand.
- What else the records date and the calendar already holds: May 14, 1962, Edwards's memorandum on Harvey's call (`cal.1962-05-14.cuba`, testimony 20–22), not cited there by this patch; Orta's loss of nerve, "'61" (interview 5; testimony 12). Both wait for a cite.

**Oct. 1, 1960, the hand combine.** Nothing either line held is lost:
- The opening sitting is in `-9` alone, with Yang, I, 558–59 and the Deng nianpu, III, 1580 cited for their parts, and Wu's "from Oct. 2" (365) as a date variant.
- The CPSU's draft is in `-9` ("the Soviet draft the basis").
- The Chinese reading of the draft is the gloss of `cal.1960-09-30.china-leadership-6`. Wu writes of "our party," not the delegation, and the gloss now says so.
- Wu and Chen Boda in Peking is its own entry; it holds against Wu, 367.
- The three weeks' disputes stay in `cal.1960-10-02.soviet-union` (Deng, 1580; Wu, 366–67, both hold).
- Wu's note that the delegation was large, with most of the writers in it (367), which the edit had dropped, is restored to the Wu parenthetical.
- `-soviet-union` keeps no forward pointer: its one sentence of pointers names the entries of Sept. 30 and Oct. 1, both earlier or the same day.
- Added to `-9`: Deng's words at the sitting, from the Deng nianpu, 1580–81 (the document must give the enemy nothing to use; views to be exchanged calmly and fully).

**Gibbons, III, 77.** The NSC record is n.93 and Cooper's notes n.94 (read on the page). The via row's repointing holds. For the merger, in `sources/witnesses/by-work/gibbons-u-s-government-and.yaml`: the edge `at: III, 77 n.83` (of `x.1965-02-10.summary-record-of-nsc-meeting-no`) should read `III, 77 n.93`, and `at: III, 77 n.84` (of `x.1965-02-10.coopers-notes-of-the-preliminary-meeting`) should read `III, 77 n.94`.

**Jan. 1965.**
- Jan. 27: the split holds against FRUS docs. 42 and 43; doc. 44 already has its own entry (`-5`). A broken link mended in the new entry.
- Jan. 19–20: the split holds against doc. 29 and Taylor, 332 (the Jan. 20 presentation "on the following day"; its 5 p.m. is the cable's plan, so said).

**Mar. 1965.**
- Mar. 17: the split holds against the Record (5261, 5324, 5325); no link between the letter and the introduction.
- Mar. 21, Heschel: Branch, 611, has the words in the epilogue, sourced to the two interviews of 1990 and 1991, with no day of the march. The gloss is right. It is reworded to name the two interviews with their dates, and the note's "his interviews" is now "Branch's" (R57). The line keeps that Heschel marched beside King.
- Mar. 25: the split holds. "Almost noon in Washington" is 161, about 11 a.m. at Montgomery. The speech is "that afternoon" (164) and "this afternoon" (165, 170); the flatbed and the networks, 164; "How long? Not long!", 170. Kotz, 323–24, bears the march, the capitol and the two quotations, but not the flatbed, the hour, the networks or "How long?". His cite on the speech now says so.

**July 27, 1965.** Gibbons, 431, holds for the speech ("that night") and the call ("Meanwhile"). Struck from the call's entry: the cite of note 131 itself. That note's text names Evans and Novak and supports nothing in the line; Evans stays behind "To check:".

**Aug. 1965, steel.** Califano, 89–91, holds: the briefing "that Saturday afternoon" (90); the call "after midnight Sunday" and the memorandum of Aug. 30, 2:45 a.m. (n.14); Eisenhower "That afternoon" (91, n.19). Struck: the sentences in the two older notes that pointed forward to the new entries (the guide's rule on splits). A broken link mended. Eisenhower's entry keeps the link after the back channel on "the printed order alone," as the reader labelled it.

**Brezhnev's workbook, II, 116–18.** Every hour holds against the page image (Mar. 31 10:00–19:00 and 19:00–20:30; Apr. 2 10:00–17:30; Apr. 3 11:30–15:45; Apr. 4 17:30–19:00; Apr. 5 18:30–20:30; Apr. 6 18:00–20:30 and 0:35; Apr. 8 9:30–10:15, 15:00–17:30, 18:00–22:00; Apr. 9 9:00, 9:30, 10:00, 10:30, 14:15, 15:00, 15:00–16:00). The pages: Mar. 29–30 on 116, Mar. 31–Apr. 5 on 117, Apr. 6–9 on 118. Changed:
- The Presidium of Apr. 6 is pinned to 118, not 117–18.
- The Congress sitting of Apr. 6 now follows that morning's Presidium ("from the morning," then "from 10:00").
- Kádár's reception: Suslov and Andropov are named after all three receptions of Apr. 9, not the first alone, now a Check.
- Mar. 29: a forward sentence struck.
- The Mar. 31 dinner: the workbook's cite there stood for the whole line, the Ceaușescu–Shelepin talk included. It now stands for the time, and for a new sentence, "Brezhnev at the dinner, 19:00 to 20:30," with his tag and name.
- Added: two entries the reader passed over, Brezhnev's work on the Congress documents on Mar. 31, 20:30–22:15 (`cal.1966-03-31.soviet-union-leadership-3`) and on Apr. 3, no hour (`cal.1966-04-03.soviet-union-leadership-2`), both claimed in the ledger.
- The editorial commission of Apr. 7, the plenum and the last sitting of Apr. 8 were already in the tree; the reader's entries do not repeat them.

**Apr. 16, 1966.** The Zhou nianpu, III, 28, names Deng among those Zhou talked with at Hangzhou, so the line does not rest on the Deng nianpu. The 6 p.m. talk carries the Deng cite in its own entry, and the talks of Apr. 18 and 19 are entries too. The cite should be struck, but `patch-check` refuses any edit that drops a work read. It stays, narrowed as the reader left it, for the merger to strike by hand.

**Mar. 18, 1966.** The Check holds against the Peng nianpu, IV, 475 (morning enlarged meeting, afternoon with Chen Boda, evening at Mao's) and the Zhou nianpu, III, 22 (Mar. 18–20, no hour). Kept distinct.

**The reader's other rulings** (items 7 and 8 of the reader's note, no op): accepted. They were not re-read.

## For the merger

- Settle every duplicate flag as distinct (`--take keep`): all 33 the dry run raises, on the 45 new entries. Each is a separate call, sitting, reception, session or act of its own hour.
- The two by-work edges of Gibbons, III, 77, above.
- The Deng nianpu cite on `cal.1966-04-16.china-leadership-3`, above.

## What waits

- **Brezhnev's reception and call lists.** The reader did not enter the people Brezhnev received and telephoned each day, Mar. 29–Apr. 9 (II, 116–18), as lists with no business named; earlier Brezhnev readers did the same. Under R0 that ground is disregarded: these are the informal record (R7), and only R18 can take them out. They are not added in this audit, which ran out of budget for them, and wait for a pass over the workbook.
- **Two cites still to add.** The Church testimony to `cal.1962-05-14.cuba` (Exhibit 1, 20–22); the interview and the testimony to the Orta entry of 1961.
- **Two pages not read by the audit.** The Ye Jianying nianpu, II, 935; Garrow, 413.
- **No online link for the NARA records.** Both are cited by record number; the archives.gov paths tried all return 404. A link, once found, would let the new sentences be mapped to the records.
