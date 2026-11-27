# Audit of lo-c (leftovers: zones and duplicates)

The audit of the reader's patch `inbox/2026-11-27-lo-c.yaml` and note `notes/leftovers/lo-c.md`, Nov. 27, 2026. Read from the entries (`./bib show`) and the records online: the Cow Palace speech (American Presidency Project), FRUS 1961–63, I, doc. 31, FRUS 1964–68, V, doc. 238, and the Miller Center page of conversation 4129 (July 2, 1964). Nothing was fetched from the Drive (its download quota is spent). Where a ruling needs a Drive book, this note says so.

## What this audit disregarded, and two counts

Nothing in the brief narrowed what is an entry. Two counts in the brief are off. The patch holds 22 `check` ops, not 45. And the 70 "combine" items are 69 pairs: the Cow Palace pair is listed twice, once from each side.

## How the merger should use this note

Run only the `./bib combine` lines below. Do not run the lines in the reader's note. For seven pairs, this audit strikes the reader's combine. For ten more, it changes the ruling. Where a line below says to split, do the split by an `edit` after the combine.

Six check ops named the entry that a combine drops (for example, "Check: the day; [[cal.1964-10-15.china-leadership-8]] has ..."). After the combine, each would have pointed to its own entry. The audit rewrote them to name the work instead. It also wrote each work the check ops named as plain text ("Zhou chronology III, 167", "Mao nianpu V") as its card.

## Combines confirmed (40)

- `./bib combine cal.1960-11-02.peace-corps cal.1960-11-02.elections-1960-kennedy-5` (the speech text at APP has both passages)
- `./bib combine cal.1960-11-22.soviet-union cal.1960-11-22.china-leadership-6`
- `./bib combine cal.1960-12-30.china-leadership cal.1960-12-30.china-leadership-6`
- `./bib combine cal.1961-04-19.china-leadership-3 cal.1961-04-19.china-leadership-2`
- `./bib combine cal.1961-06-22.china-leadership-3 cal.1961-06.china-leadership-2`
- `./bib combine cal.1961-08-24.china-leadership-2 cal.1961-08-24.china-leadership-3`
- `./bib combine cal.1962-07-19.china-leadership-10 cal.1962-07-18.china-leadership-4` (the Check on the day is in the patch)
- `./bib combine cal.1963-05-08.china-leadership cal.1963-05-08.china-leadership-9`
- `./bib combine cal.1963-05-22.vietnam-force-levels cal.1963-05-22.testing`
- `./bib combine cal.1963-05-29.transition-and-staff cal.1963-05-29.elections-1964`
- `./bib combine cal.1963-07-16.europe-and-the-alliance cal.1963-07-16.japan`
- `./bib combine cal.1963-10-01.china-leadership-10 cal.1963-10-01.china-leadership-3`
- `./bib combine cal.1963-10-16.democratic-party cal.1963-10-16.transition-and-staff`
- `./bib combine cal.1963-11-21.elections-1964-3 cal.1963-11-21.democratic-party`
- `./bib combine cal.1963-12-23.elections-1964-vice-presidency cal.1963-12-23.robert-kennedy`
- `./bib combine cal.1964-01-10.latin-america-panama-3 cal.1964-01-10.defense` (one Miller Center conversation, WH6401-10-1303)
- `./bib combine cal.1964-01-16.transition-and-staff cal.1964-01-16.confirmations` (one Miller Center conversation)
- `./bib combine cal.1964-04-24.elections-1964-state-conventions cal.1964-04-25.elections-1964-state-conventions`
- `./bib combine cal.1964-04-27.china-leadership-9 cal.1964-04-27.china-leadership-7`
- `./bib combine cal.1964-07-02.civil-rights-bill-16 cal.1964-07-02.civil-rights-bill-6` (the Miller Center summary of 4129: the timing of the signing for the best TV coverage. The note of -6 also cites Purdum, 314, for a different call, on waiting. It comes over with the combine and says so.)
- `./bib combine cal.1964-10-14.china-leadership-2 cal.1964-10-15.china-leadership-8` (the Check on the day is in the patch)
- `./bib combine cal.1964-12-15.china-leadership cal.1964-12-15.china-leadership-4`
- `./bib combine cal.1965-02-08.vietnam-force-levels-2 cal.1965-02-09.vietnam-force-levels` (the audit added the Check on the day, which names MACV, 478)
- `./bib combine cal.1965-11-10.vietnam-2 cal.1965-11-10.vietnam-force-levels`
- `./bib combine cal.1965-11-21.opinion cal.1965-11-21.opinion-2`
- `./bib combine cal.1965-12-06.opinion cal.1965-12-06.opinion-2`
- `./bib combine cal.1965-12-20.china-leadership-2 cal.1965-12-20.china-leadership`
- `./bib combine cal.1966-02-09.china-leadership-4 cal.1966-02-09.china-leadership-3`
- `./bib combine cal.1966-02-25.press-and-broadcasting cal.1966-02-25.vietnam-support`
- `./bib combine cal.1966-02-26.vietnam-air-war cal.1966-02-25.vietnam-air-war` (the Check on the day is in the patch)
- `./bib combine cal.1966-07-10.china cal.1966-07-10.china-leadership-5`
- `./bib combine cal.1966-07-13.china-leadership-4 cal.1966-07-13.china-leadership-2`
- `./bib combine cal.1966-07-15.open-housing cal.1966-07-16.open-housing-2` (the Check on the hours is in the patch)
- `./bib combine cal.1966-07-28.china-leadership-12 cal.1966-07-28.china-leadership-14`
- `./bib combine cal.1966-09-24.china-leadership-6 cal.1966-09-23.china-leadership-4` (the Check on the day is in the patch)
- `./bib combine cal.1966-10-17.china cal.1966-10-17.china-leadership-3`
- `./bib combine cal.1967-02-07.china-leadership-6 cal.1967-02-07.china-leadership-2`
- `./bib combine cal.1968-04-26.economy-surcharge cal.1968-04-26.cities-and-housing`
- `./bib combine cal.1968-06-18.elections-1968-ny cal.1968-06-18.elections-1968-state-conventions`
- `./bib combine cal.1968-06-20.china-leadership-2 cal.1968-06-20.china-leadership`

## Combines confirmed, with a split after (10)

In each of these, the kept entry holds a second act. The merger splits it out into an entry of its own, and that entry points back to the kept one.

- `./bib combine cal.1960-04-13.china-leadership-3 cal.1960-04-13.china-leadership-2`. Split out: the arrival at Kunming in the afternoon (Waijiao huodong 273; Chen Yi nianpu 809), with `place: kunming`, an afternoon range and a link that it follows the departure.
- `./bib combine cal.1960-12-01.transition-and-staff-2 cal.1960-12-01.transition-and-staff-cabinet-3`. Split out: Blair sounding Stevenson out that night ({4}). Lovett's lunch with Kennedy ({5}) is a third act.
- `./bib combine cal.1962-01-17.china-leadership cal.1962-01-17.china-leadership-3`. Split out: the later sittings of Jan. 18, 19, 20 and 22 and Zhou's own revising of Jan. 19–22 ({2}). `when` then narrows to Jan. 17. The variant on the first speaker comes over from -3.
- `./bib combine cal.1965-02-23.vietnam-diplomacy cal.1965-02-23.soviet-union`. Split out: the approach to the British government. No source in hand gives its day; its own entry carries "Check: the day".
- `./bib combine cal.1966-03-26.china-leadership-4 cal.1966-03-26.china-leadership-3`. Split out: Liu's talks with Ayub Khan, and Ayub's banquet that evening at Islamabad, where Liu speaks (Chen Yi nianpu 1140). The kept entry is then the departure from Urumqi and the arrival at Rawalpindi, and it holds the trip's bibliography.
- `./bib combine cal.1966-04-25.vietnam-congress-foreign-relations cal.1966-04-26.vietnam-congress-foreign-relations`, then `./bib combine cal.1966-04-25.vietnam-congress-foreign-relations cal.1966-04-27.vietnam-congress-foreign-relations`. This changes the kept entry. The reader's prose said to keep Apr. 25, but the command kept Apr. 26. Apr. 25 is the only one of the three that rests on a dated record (Lee Williams to Fulbright, Apr. 25, 1966, cited by Woods, 132 n.23). The patch's Check on the day was rewritten to name the works. Split out: Fulbright's refusal, which is the reply to the invitation. Its day is open, and it follows the invitation.
- `./bib combine cal.1966-05-06.china-leadership-2 cal.1966-05-06.china-leadership-7`. Split out: Kang Sheng's eight hours over May 5 and 6, in the line, if [[cal.1966-05-05.china-leadership-3]] does not already hold them. Peng Zhen nianpu IV, 484 puts Zhang's speech on May 6, afternoon, and on May 7, morning. That is a Check for the merger to carry.
- `./bib combine cal.1967-05-09.vietnam-air-war-2 cal.1967-05-09.vietnam-air-war-4`. Split out: "The same day State's experts, Helms backing them, for restraint." It goes to cal.1967-05-09.vietnam-air-war, with Drea, 208.
- `./bib combine cal.1967-07-12.vietnam-force-levels cal.1967-07-12.vietnam-program-5`. FRUS 1964–68, V, doc. 238 is the meeting: the Cabinet Room, 1:05–2:38 p.m., with both "stalemate" lines. Its source note says McNamara held a press conference afterward. Split out, first: the July 13 scene at the residence ({2}) and Westmoreland's account of Johnson's choice ({3}). Split out, second: McNamara's words to the press ({2} of the dropped entry). That entry follows the meeting.
- `./bib combine cal.1968-06-13.governors-nd cal.1968-06-13.elections-1968-state-conventions`. Split out: Rockefeller's address to the convention on June 15, dated that day.

## Combines struck (7)

- cal.1960-03-08.china-leadership-3 and -2: two events. Both entries cite Waijiao huodong 271 and Peng Zhen nianpu IV, 8 for two acts. One is the commemorative meeting with the reception of the foreign delegations, on Mar. 7, afternoon (-2). The other is the evening gathering of more than 20,000 of the capital's women, on Mar. 8 (-3). Only Zhou nianpu II, 292 dates the meeting Mar. 8. The reader's Check, which it put on -3, belonged on -2, so the audit moved it there and reworded it. -2 is to be dated Mar. 7 once the books are read (Drive).
- cal.1960-03-20.china-leadership-7 and -8: this waits on the Yang diary, I, 490 (Drive). The notice of "last night" (昨晚) is cited from the entry of Mar. 20. If so, it is of the night of Mar. 19, not Gao Zhi's call at 12:30 a.m. after the meeting of Mar. 20. The audit added a Check on -8.
- cal.1963-12-05.robert-kennedy and -2: this waits on the Schlesinger journal, 211–13 (Drive). The journal at 212 puts the talk of the FBI on the flight back from Boston. The entries do not say on which flight the talk of the vice presidency took place. That could make two talks. The audit added a Check on the kept entry.
- cal.1964-04-20.china-leadership-7 and -6: two acts, Ke Qingshi's operation at Shanghai and Yang's telephone call that evening reporting it. -7 already follows -6.
- cal.1964-12-14.laos and cal.1964-12-12.laos: two acts, the principals' approval of Barrel Roll and the order to CINCPAC on Dec. 12 (Cosmas, 189–90; Anthony, 144), and the first mission on Dec. 14. The reader's Check on Dec. 14 ("Check: the date of Barrel Roll's start ...") was wrong, because Dec. 14 rests on three works. The audit struck it and put a Check on Dec. 12: the line should say the approval, and its missions go to Dec. 14.
- cal.1965-11-09.china-leadership-9 and cal.1965-11-12.china-leadership-11: two acts. Teiwes, 209 gives Lin Biao's comments "of Nov. 9 and 12", one each day. The reader's Check on Nov. 9 is struck.
- cal.1967-01-13.china-leadership-5 and cal.1967-01-11.china-leadership-7: two acts, the Center's notice of Jan. 11, dated by its own record, and the issue by the General Office's secretariat on Jan. 13 of three such notices. The other notices of Jan. 11 have their own entries too.

## Rulings changed (12)

- cal.1960-11-25.china-leadership and -6: no combine. The kept entry holds two acts, the delegation's deliberation (afternoon to night) and its cable deep at night. The cable is -6's act. The sentence "The delegation cables Peking deep at night ..." moves to -6, with Lengxi, 397–400, and -6 follows the deliberation.
- cal.1961-01-27.china-leadership and -3: no combine. Waijiao huodong 302 and Chen Yi nianpu 856 give two clocks for two acts: the signing of the trade agreement at 6 p.m. (the kept entry's hour) and Zhou's banquet at 6:30 p.m. (-3). The banquet clause, with Zhou's words (Zhou nianpu II, 387), moves to -3. The kept entry is then the signing.
- cal.1961-04-20.vietnam-2 and cuba-2: no combine, as the reader said. The ruling is filled out from FRUS 1961–63, I, doc. 31. Kennedy names Gilpatric at the 11 a.m. Cabinet meeting, and McNamara's memorandum on a program goes to the President that afternoon. These are two acts. vietnam-2 is the task force: it takes cuba-2's {3}, with FRUS I, doc. 31 as its primary record, place Washington, and the hour of the Cabinet meeting. McNamara's memorandum ({6} of cuba-2, and the second sentence of vietnam-2) becomes an entry of its own. The Oval Office meeting ({4}, {5}) is also a second act in cuba-2.
- cal.1963-10-30.elections-1964 and democratic-party: no combine, as the reader said. The dinner sentence ({4}) comes out of democratic-party, and its variant from White goes with it.
- cal.1965-02-16.vietnam-diplomacy and china-2: no combine. The Soviet approach to Hanoi with Phạm Văn Đồng's answer is one act. The approach to Peking with China's answer is another. The second sentence of vietnam-diplomacy moves to china-2 with the Romanian transcript, and china-2 already follows.
- cal.1965-05-19.vietnam-air-war and cal.1965-05-22.vietnam-air-war-2: a different pair. Staaveren, 137 (cal.1965-05-20.vietnam-air-war, cal.1965-05-22.vietnam-air-war), Drea, 61, and Cosmas's own note (366 n.16, the OPSUM of May 22) put the first strike above the 20th parallel, on the Quang Soui barracks, on May 22. Run `./bib combine cal.1965-05-22.vietnam-air-war cal.1965-05-22.vietnam-air-war-2`. May 19 stays apart. Its note already has the Check that the reader's new op repeated, so the audit struck that op.
- cal.1966-06-03.china-leadership and -9: a different pair. -9, the new committee beginning to send work groups into some schools (Pu, 152, June 3–4), follows the Standing Committee's agreement of -2. It is not Mao's approval of the two dispatches. It is the act of cal.1966-06-04.china-leadership-6 ("sends work groups into the schools", Yang Jisheng II, 1143). Run `./bib combine cal.1966-06-03.china-leadership-9 cal.1966-06-04.china-leadership-6`.
- cal.1967-05-30.china-leadership-3 and -4: no combine. -3 holds the reception (morning range) and the luncheon. The luncheon at noon is -4's act (Chen Yi nianpu 1191, 中午). "And gives a luncheon" comes out of -3, and the Diaoyutai and Waijiao huodong 512 go with it to -4.
- cal.1968-02-04.china-leadership and -2: no combine. -2 is Zhou's liaison meeting and his letter to Mao; the meeting can be split from the letter. The kept entry is Mao's reply, "fully agreed". A letter and its reply are two entries (R17). The kept entry already follows -2. Its first sentence, the letter, is to be cut to a clause that names what Mao answers.
- cal.1968-03-31.vietnam-205000 and -3: no combine. The kept entry holds two calls: McPherson to Clifford, and Johnson to McPherson "about five". The sentence "About five, Johnson to McPherson ..." moves to -3, with McPherson, 438–39, and -3 takes the hour (about 5 p.m., `time_approx`).
- cal.1968-04-05.elections-1968 and cal.1968-04-07.elections-1968: no combine. Miller's request through Califano (Califano, 290, Apr. 5) is one act. Johnson's "full speed ahead", after Califano's memorandum of Apr. 7 (cited by Dallek, 545), is the reply. "Johnson: full speed ahead" comes out of Apr. 5, and {1} comes out of Apr. 7, which points back. The reader's Check on Apr. 5 is struck.
- cal.1968-06-14.elections-1968-3 and cal.1968-06-16.elections-1968-2: no combine. June 14 is the radio interview. The remark by telephone to reporters, "emerge on his own", is in the same words as the line of June 16 (CQ), and it moves there with Chester, 154. Mondale's statement "a few days later" ({3}) becomes an entry of its own, with "Check: the day". The patch's Check on June 14 was rewritten to say this.

## The sample

25 of the 66 pairs kept apart, chosen with random seed 20261127. All 25 are rightly kept apart. These are the pairs: 1960-04-16 -2/-3; 1960-04-25 -9/-13; 1960-11-29 -7/soviet-union-4; 1960-12-22/12-23 -8; 1961-03-13 -1/-2; 1961-04-05 laos/laos-2; 1961-05-30 laos/laos-2; 1961-08-31 testing-2/berlin-and-vienna; 1962-03-22/03-23; 1962-07-11 -2/07-12; 1964-02-29 defense/transition-and-staff; 1964-09-28 elections/program; 1965-01-21 program/vietnam; 1965-02-08/02-07; 1965-03-01 -1/-2; 1965-06-07 -1/-2; 1965-06-09 -1/-2; 1965-12-22/12-23 -3; 1966-06-03 -3; 1966-07-12 -2/-3; 1966-11-16 -5/11-17 -2; 1967-01-22 -6/01-23; 1967-05-17/05-18; 1967-05-18 -2/05-19; 1967-07-20 -2/-15. For 1961-04-05 laos, the Check is the right course, because Kaplan, 240 is cited on laos for Phoumi's offensive of the same day. Several of these entries hold a second act apart from the overlap (Felt's report in laos of Apr. 5, 1961). The merger's sentence moves will not fix those.

15 of the 46 zones set, with the same seed, then all 48 zone edits by a script. The 48 include the reader's two additions, 1960-05-10 -2 and 1960-08-02. Each stored instant was turned back into local time by the zone set, using its history. Each agrees with the clock in the line or the note. Each zone fits the place: China +8; Saigon +8 in 1965 and 1968; Vientiane +7; Athens +2, with no summer time in 1964; Paris +1, with none in 1960; Los Angeles on daylight time in July 1960; Cairo +3, summer time, in June 1965; the LBJ Ranch and Selma Central. One small point: cal.1965-06-23.china-leadership has "3 a.m." in its line and 3:15 a.m. in its note and its time. The line should say 3:15.

## The check ops

All 22 say something a reader can act on, except the one on cal.1965-05-19.vietnam-air-war, which repeats a Check already in the note. That one is struck. Four were struck because the ruling above changed (1960-03-08 -3, 1964-12-14, 1965-11-09 -9, 1968-04-05). Five were added (1960-03-08 -2, 1960-03-20 -8, 1963-12-05, 1964-12-12, 1965-02-08 -2). Eleven were rewritten: six that named an entry a combine drops, four that wrote a work as a plain title, and the one on June 14, 1968. The patch still holds 22 check ops and the one `follows`.

## Other points for the merger

- The reader's item on cal.1968-03-31.elections-1968-9 calls cal.1968-03-31.elections-1968-mccarthy-2 and "the call clause of -mccarthy-4" one call, "to be combined by the merger". That is a sentence to move out of -mccarthy-4, not a combine, because -mccarthy-4 holds other acts.
- The reader's item on cal.1966-09-02.alabama-al calls the federal time law "the Uniform Time Act of 1967". It is the Uniform Time Act of 1966, in force in 1967. The zone still waits.

## Fit to merge

Yes. `./bib patch-check inbox/2026-11-27-lo-c.yaml` gives 0 errors and 0 warnings. The patch holds no combine. The merger runs the combines and splits from this note, not from the reader's note.
