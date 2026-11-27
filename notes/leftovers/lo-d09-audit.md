# Leftovers lo-d09: the audit

Auditor: Claude (Opus), Nov. 27, 2026. The patch `inbox/2026-11-27-lo-d09.yaml` was corrected in place. It had 76 ops; it now has 130. Of the 76, 26 stand as the reader wrote them, 49 were changed, and 1 was struck (a `follows` that tied the Oct. 20 meeting to the wrong entry). 54 ops are new: 30 new entries, 9 `follows`, 2 cites, 2 primary records, 2 checks, 1 edit and 2 gazetteer rows. `./bib patch-check` shows 0 errors. The 90 warnings are the usual "one event?" and "duplicate of ...?" flags, and the Laos edit's "sets only n". Every claimed id is added, and every added id is claimed.

Nothing in the brief narrowed what is an entry, so nothing was disregarded under R0. Following R0, I entered the dated events I met on the pages I opened, even where they lay outside the batch's rows. The rest are listed below as still to read.

## What was read

- Kaplan, *McNamara Ascendancy*, 112, 204–06, 213–14, 222 (the Drive copy, text layer; printed page = PDF less 18).
- Branch, *Parting the Waters*, 607 and its notes, and 609 (PDF less 34).
- Garrow, *Bearing the Cross*, 205–06 and 211, and the note to 211 (PDF less 4).
- Young, *An Easy Burden*, 179 (checked on the page image).
- *Kelly v. Page*, 335 F.2d 114 (5th Cir. 1964), and *Anderson v. City of Albany*, 321 F.2d 649 (5th Cir. 1963), on case.law.
- Yang Shangkun's diary, II, 195–97 (page images; printed page = PDF less 5).
- The Mao nianpu EPUB, for July 18 and 22 and Nov. 5, 18 and 19, 1962.
- Jian, *Zhou Enlai*, 468, 478, 480 and 482.
- The Chen Yi nianpu, 926 (image).
- The Zhou Enlai nianpu, II, 490 and 513 (images; the 1997 middle volume).
- Chang, *Friends and Enemies*, 251–52 and the note n.48.
- Macmillan's diaries, II, 506–07 and 513 (PDF less 58).
- Salinger, *With Kennedy*, 250–52, 258–62, 267 and 272–73 (printed page = PDF less 34 in this stretch).
- O'Donnell and Powers, 363–70 and 381–82.
- Thomas, *Robert Kennedy*, 209, 219–20, 224, 227–28 and 232.
- Schlesinger's *Journals*, 172 and 175–78.
- Schlesinger, *Robert Kennedy and His Times*, 506–07, 510–11, 520–23 and 526–27.
- Smith, *On His Own Terms*, 383.
- Fursenko and Naftali, *One Hell of a Gamble*, 222–27, 234–35, 254–55, 277–78, 281–82, 299–300, 304–5 and 309–10, with the notes to 254–55, 300 and 304–5.
- Fursenko and Naftali, *Khrushchev's Cold War*, 465–66, 486–89, 499 and 504–05.
- *Prezidium TsK KPSS*, I, 646, and the notes at 1115.
- MacFarquhar, *Origins*, III, 301, 308–10 and 319–20, with notes 69 and 119 (in this copy the text runs at PDF less 14).
- Sorensen, *Counselor*, 285–86 and 300–01 (PDF less 22 here).
- Sorensen, *Kennedy*, 673–78, 692–93, 713 and 715.
- Reeves, 368–77, 385–88, 410–23 and 435.
- Gavin, 78–80.
- Ball, 288–89 and 294–95.
- Taylor, *Swords and Plowshares*, 264–68 (PDF less 38 here).
- Poole, 166 and 179–81 (archive.org's DTIC text).
- Caro, *Passage of Power*, 207–22.
- Rusk, 230–42.
- Dobrynin, 87–93.
- O'Brien, 140–41.
- Preston, 63–68.
- *A Thousand Days*, 794–810.
- FRUS 1961–63: XI, docs. 16, 18, 21, 34, 38, 94 and 96; XIII, doc. 258; and XVIII, docs. 4, 5 and 8.
- The Minnesota Supreme Court's opinion in *Rolvaag v. Donovan* and the State Canvassing Board's report.

Every copy was deleted after use.

## The splits

I applied the new rule in `notes/guide/changing.md`, "Splitting an entry", to every split. Each old note now keeps only the works whose pages bear the act left in it. Each work stands under the act its page bears. No old note points forward. Each new entry points back with "See [[id]]", and the "Split under R17" sentences are gone.

- **Oct. 16.** The old entry is now Bundy's report to the President. Out of its note went the recordings, FRUS docs. 18 and 21, Caro, Poole, *Robert Kennedy and His Times*, Ball and *Counselor*, none of which bears the breakfast. Kept: Kaplan, Fursenko and Naftali, Rusk, Sorensen's *Kennedy*, Preston, *Khrushchev's Cold War*, Thomas, Taylor (265: "Bundy had already shown him the photos"), *A Thousand Days*, Reeves and FRUS doc. 16. A Check sets out the hour: Kaplan, Reeves and *A Thousand Days* give 8:45, Thomas about 8, Sorensen about 9.
- **Oct. 16, -6 and -7.** The meeting (-6) now carries doc. 18 first, and a Check giving 11:45 in five accounts against 11:50 on the transcript. The call to Sorensen (-7) also cites Sorensen's *Kennedy*, 674. FRUS doc. 21, the 6:30–7:55 p.m. meeting, goes as the primary record to `cal.1962-10-16.missile-crisis-3`.
- **Oct. 20.** The reader's old entry repeated `cal.1962-10-20.missile-crisis-9`, Salinger's bedside scene, which the tree already held. It also kept two acts with their own hours or places: the departure at 11 a.m., and Johnson's return from Hawaii.
  - The old id is now the departure: airborne at 11 a.m. Chicago time, at the White House at 1:30. Its sources are Salinger, Sorensen's *Kennedy*, O'Donnell, O'Brien, Ball, Fursenko and Naftali, Thomas, Caro and Reeves.
  - O'Donnell's version of the bedside scene, with the note in other words, and O'Brien's version go to -9, by a cite and a Check.
  - New entries: the White House pool, between 1:30 and 2:30 (Reeves 388, Thomas 220, Caro 211); Sorensen with the President before the meeting (Sorensen's *Kennedy*, 693); the 9 a.m. review of the draft speech (Sorensen's *Kennedy*, 693; Ball 294); Johnson's return (O'Donnell 365, Caro 212); and the *Post* editor's question to Salinger (O'Donnell 365).
  - The meeting (-11) now follows the pool. Out of its note went O'Donnell's bedside material, Salinger and O'Brien, and Johnson's name.
  - Robert Kennedy's call (-12) now names the President, and adds Fursenko and Naftali, 234, and Caro, 211. Its Check gives O'Donnell's call of the night before and Reeves, 387.
  - The links on -3, -5 and -excomm move from the old id to -11. The Truman Balcony (-excomm-3) now also follows -11 (O'Donnell 366, "When the meeting broke up").
- **Oct. 27.** The old entry is now the U-2 shot down. Dobrynin goes to -18 only. The Alaska U-2 (-16) now carries Kaplan 213, Poole 180 (word at 1:40 p.m.), FRUS doc. 94 (Rusk's report at the 4 p.m. meeting), Sorensen's *Kennedy* 713 and Thomas 227.
  - Sorensen's urging (-17) happened "during the ExComm meeting Saturday afternoon" (*Counselor* 300). It now follows `cal.1962-10-27.missile-crisis-excomm-2`, the 4 p.m. ExComm, not the U-2.
  - Robert Kennedy and Dobrynin (-18) now has FRUS doc. 96, Robert Kennedy's memorandum, as its primary record. Doc. 94, which does not treat the meeting, is out.
  - New: Robert Kennedy's call to Dobrynin at about 7:15 p.m. (doc. 96; Fursenko and Naftali, 281), which follows the 7 p.m. Oval Office meeting. -18 follows the call.
  - New: the Chiefs' reminder that a SAM downing a U-2 brings retaliation, and the President's "Let's wait and see" (*Counselor* 301).
  - The links on `cal.1962-10-27.missile-crisis-diplomacy` and `-excomm` move to -18.
  - The U-2's hour is 10:22 a.m. under the book's heading "Havana, 10 A.M. (5 P.M., Moscow Time)". Those two clocks do not agree with the day's offsets, so the hour stays approximate, and the note says why.
- **July 18, the Middle East.** The old line said the deficit was $110–120 million. That figure is Komer's, of July 19. The Embassy's verdict is telegram 78. The line now holds the resignation and the naming alone. New entries:
  - Embassy telegram 78 (doc. 8 n.1).
  - Talbot's call to Kennedy with the aid figures, by July 18 (doc. 5, the source note).
  - Komer to Kennedy of July 16 (doc. 4). The reader had dropped it from the note, and it was in the calendar nowhere else.
  - Holmes's telegram 15 of July 4, and State's telegram 33 of July 13 (doc. 4 n.1).
- **July 22 and 23, Chen Yi and Menon.**
  - Out of the July 22 note went these, now under "To check" on July 23: Gopal (MacFarquhar n.30, the communiqué), and Whiting and Lall (Jian n.64, the statement not issued). MacFarquhar, 301, is now also cited on July 23 for the communiqué. Lall's map row moved with it.
  - Jian's sentence that Chen asked to meet again the next day is now in the July 22 line.
- **Nov. 19.** The Mao nianpu settles it. The first meeting was in the morning. The meeting at 4:30 p.m., at Juxiang Shuwu, followed the 4 p.m. note, to study peace talks with India.
  - The old id, which Jian's "half an hour later" fixes, is now the 4:30 meeting, at 4:30 exactly.
  - The new -3 is the morning meeting, with no `follows`.
  - The reader's "between the two" (the Foreign Ministry talk) is not on Zhou nianpu, II, 513, which says only "after", and it is gone.
- **Nov. 9.**
  - The report to the President early in the Gavin dinner (Fursenko and Naftali, 300) is now its own entry.
  - The call to Bolshakov follows the dinner entry. The call takes no range, because *Khrushchev's Cold War*, 499, puts it an hour after the meeting at home and gives no clock.
  - Gavin is out of the old line's names.
- **Nov. 15.** The battery rests on note 63 (Mikoyan's cable of Nov. 18 and Burris to Johnson), not on the cable of Nov. 17. The notes were corrected, and the map row for n.66 moved to the dinner.
- **Oct. 22, Rockefeller.** The statement after the address now follows the address, `cal.1962-10-22.missile-crisis`, not the afternoon entry.
- **Oct. 23, the *Aleksandrovsk*.** The hour is set approximate. A Check notes that pages 254–55 do not name the R-14 or cruise-missile warheads that the line names.
- **Oct. 24.** Schlesinger's memorandum to the President that night is split from Harriman's call. Kennedy's call to Harriman "the next day" (Oct. 25) is a new entry.
- **July 2/3, July 14/15, Nov. 1, Nov. 24, Nov. 28/29.** The forward pointers came out, and each old note keeps a sentence naming its source.
  - July 14: Branch's note n.2 (the *Herald* of July 14) was dropped from the map and is restored for the headline. The "To check" now reads "nn.2, 3".
  - July 15: Katzenbach's letter is in Branch's note to the Department's dealings with the FBI (607 n.4), not with the denials. The note now says so, and the Check stays.

## Hours, places and the order of the day

- Every hour and band was converted again with the zone of the day. Chicago was on CDT and London on BST in October 1962. Havana, Geneva, Budapest and Peking had no summer time. Washington changed back to standard time on Oct. 28.
- Oct. 16: Macmillan's afternoon was at the Forth Bridge and Bathgate, not Edinburgh. Two gazetteer rows are added: `south-queensferry` and `bathgate`.
- `cal.1962-10-20.missile-crisis-excomm-3` is settled by the record. O'Donnell has the talk "when the meeting broke up", and FRUS XI, doc. 34 has the 505th meeting ending at 5:10 p.m. The time is set at 5:10, approximate. Thomas's "evening" and "night" stay as a Check.
- July 27, Albany: the hour is "shortly after 2:00 P.M." (Garrow 211), now set.
- Nov. 26, Minnesota: the Board met at 2 p.m. by its report, now set in place of the kind-range.
- Oct. 21: -13 also follows the 506th meeting (FRUS doc. 38), which Salinger's "Immediately following the meeting" names.
- `python3 tools/times/day_order.py` prints the tree alone. The patch's days were read against it by hand.

## What waits, and on what

- **Elliott's order, July 20.** The city's complaint was filed July 20 (*Kelly v. Page*, 116; now an entry, which the order follows). Tuttle's dissolution of the order is cited as its primary record (117 n.2). Neither opinion dates the order. The date stays, with the variants (Garrow and Branch, July 21) and a Check that names the District Court's file (M.D. Ga.), not reached.
- **The Army–Navy game.** Reeves, 435, has it on Monday, Nov. 26, a day on which the game is not played. No record in hand gives the day. The Check now names the President's Appointment Book and the press. The reader's "reference page" is gone, being no citable record.
- **The Hoover memorandum of July 28.** Garrow's note to 211 cites it ("Director to Attorney General, 7/28/62, 157-6-2-513"). It now stands behind "To check" with that file number, and with OKRA's catalogue record, which has no text.
- **Bundy's Weekend Reading (2).** Chang cites it at 252 n.48 for a sentence on 251, which the Check now says. The paper itself is in NSF box 318 at the Kennedy Library and was not reached.

## Items still to read

These are dated events on pages I opened and did not enter. They wait for a reader's run, not for a source.

- Garrow 205: the Albany Movement's days of July 16–18.
- *Kelly v. Page* and *Anderson v. City of Albany*: their dated events after July 24.
- *Rolvaag v. Donovan*: the petitions to the court.
- Smith 383: the State Defense Council meeting of Oct. 23.
- Fursenko and Naftali: 223, Bohlen's talk with the President before noon on Oct. 16; and 309, Thompson's call to Dobrynin and Mikoyan's meeting of 5 p.m., Nov. 19.
- Taylor 264: the dinner of Oct. 15.
- Ball 288: Hilsman's call of Oct. 15.
- Yang II, 195: the days of July 16 and 17.

## Duplicate flags

The merge should keep every flagged new entry as distinct. Each is a different act or a different hour of its day:

- July 18–19: middle-east-2 to -5, and the July 19 Komer to Bundy.
- July 19–24: china-center (all), georgia-albany (all), economy-3 and china-india-war.
- Oct. 16: missile-crisis-6 and -7.
- Oct. 20: missile-crisis-11 to -14, excomm-4 and -5, and warnings-3.
- Oct. 22: -39. Oct. 23: quarantine-4.
- Oct. 24–25: diplomacy-4 and -5.
- Oct. 27: missile-crisis-16 to -20.
- Nov. 1: settlement-2.
- Nov. 9: settlement and settlement-2.
- Nov. 15: anadyr.
- Nov. 19: china-3.
- Nov. 20: settlement.
- Nov. 24: china-polemic.

Two overlaps in the tree are older than this patch, and the merger should read them. `cal.1962-10-20.missile-crisis-diplomacy` repeats Stevenson's argument from the meeting (-11). `cal.1962-10-27.missile-crisis-5` tells the same afternoon's deliberation as -17, by another account.

## Left as they are

- Oct. 22, Rockefeller's afternoon: one entry holds the statement held back and the alert at the women's meeting.
- July 23: the telegram holds Zhou's draft and Mao's approval "that evening".
- Nov. 21, Laos: the edit replaces the note whole, because the Prezidium parenthetical changes. The quotation holds on page 646.
