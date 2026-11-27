# Audit of leftovers lo-d12 (February to April 1964)

Opus audit, Nov. 27, 2026, of `inbox/2026-11-27-lo-d12.yaml` and `notes/leftovers/lo-d12.md`. The patch is corrected in place. `./bib patch-check` shows 0 errors. The warnings are the usual "one event?" and "duplicate of" flags on new entries. Nothing was merged, built or committed.

## What was read

Every page below was read on the page itself: on a page image for the Chinese scans, on the text layer for the English books, and online for the records.

- Whalen, *The Longest Debate*: 108–09, 121–22, 124–27, and the note page 256.
- Kotz: 112–14, 138–39.
- Risen: 161–64, 175, 188, 197.
- Purdum: 201–02, 209–10, 263–64.
- Salinger, *With Kennedy*: 345–49.
- Lady Bird Johnson, *A White House Diary*: 68, 70–71, 95–96, 98–99, 110–11, 124–25.
- Zelizer, *Taxing America*: 204.
- Schlesinger, *Robert Kennedy and His Times*: 636, and notes 75–76.
- White, *Suite 3505*: 306.
- The Zhou dashiji: 395–98.
- The Chen Yi nianpu: 1015, 1017, 1018.
- Yang Shangkun's diary, vol. II: 352, 355, 356, 363, 367.
- The Deng nianpu, vol. III: 1797, 1809.
- Wu Lengxi: 744, 745, 747, 727, 769, 770.
- The Mao nianpu, vol. V: Feb. 27 to Apr. 26, 1964.
- *Jianguo yilai Mao Zedong wengao*, vol. XVII: 242–43.
- The Zhou Enlai nianpu, vol. II: 621–22.
- FRUS 1964–68, XXXII, docs. 229 and 235. FRUS 1964–68, XXIII, docs. 344, 347 and 352.
- 110 Cong. Rec. 1708–09, 6861 and 6863.
- 1963–64 Pub. Papers, items 211 and 232 (pp. 338–45 and 404–08).
- The Miller Center's pages for every call of Feb. 10, 1964 from 6:30 to 10:10 p.m., for Feb. 7, 1964 (citation 1955) and for Feb. 8, 1964 (citation 1971).
- PRDE's open transcript of citation 1971.

Every copy, page image and text dump was deleted after use.

## Ops checked

All 53 of the reader's items were checked against their pages. Every edit's base was current against the tree. The changes and additions are listed below. Every op not named here held as the reader wrote it.

## Changed

- **Feb. 3–4.** The Record (1708–09) makes Dowdy's amendment one to count only a living elector's vote cast in person in his precinct. The line now says so instead of "against fraudulent voting". A Check is added on Feb. 4: Whalen (109) has the DSG message sent "That night", Feb. 3, but the memorandum is dated Feb. 4 (256).
- **Feb. 7, 9 a.m. (`cuba-2`).** FRUS doc. 229 puts the meeting in the Cabinet Room and names those present. The President joined at about 10:05 a.m., called using the base's own water "a mild slap on the wrist", and sent the group to meet again at 4. All of this is now in the line. The tags for Johnson and Robert Kennedy, which the reader had removed, are restored, and `also: robert-kennedy` is kept. Robert Kennedy's later account (Schlesinger, 636) is moved to a Commentary gloss (R19b). It answers the reader's Check: the adjournment in that account is this meeting.
- **Feb. 7, 5 p.m. (new `cuba-5`).** The line now follows FitzGerald's record (doc. 235): who was present; the boats and crews; McNamara and Taylor for dismissing the workers; Kennedy and McCone against; Bundy for the second alternative; Johnson chooses the first, the dismissal. The reader's line said "The workers are dismissed", which doc. 235 does not say. Robert Kennedy's "Barry Goldwater" remark is a recollection of May 14, 1964, so it is moved to a gloss, and the Goldwater and Mann tags come off.
- **Feb. 7, O'Brien call (new `economy-3`).** The line now also has what the Miller Center's summary gives: thank Smathers and Long; the conference; the gasoline tax; the House bill. The note's "(n.103)" is dropped. Zelizer 204 is cited for the page itself.
- **Feb. 8, Baker calls.** The two Checks on the clock are rewritten. The Daily Diary could not be reached, because discoverlbj.org refuses this machine. But the Library's own log keeps the Ranch's clock. Ball's call of Nov. 22, 1964 is at 5 p.m. in his Washington record (FRUS XXIII, doc. 347) and is logged at 4 p.m. (Miller Center, citation 6450). So 17:25Z and 22:46Z (Central time) are kept, and the audit of Nov. 25, which read them as Eastern time, is not followed. The Salinger call's Check keeps PRDE's 4:56 p.m.
- **Feb. 8, evening.** The entry `civil-rights-bill-2` gets `place: washington`.
- **Feb. 10, 6:30 and 9:07 p.m.** Risen 163–64 quotes the instruction to meet O'Brien and Mansfield "in the morning". That instruction belongs to the 9:07 p.m. call: the Miller Center's summary of citation 2034 says so, and so does Purdum 202. Risen is therefore moved back to `-3`, the instruction is added to that line, and a Check notes that Risen puts the call "the morning after". The 6:30 p.m. call (`-7`) now carries the Miller Center's topics: Mansfield, Byrd, Dirksen, Russell, cloture, Wilkins. It is before the final vote.
- **Feb. 10, the congratulatory calls.** The Miller Center's catalogue gives each call's hour, so each entry now has its `time` and its recording, cited first:
  - O'Hara, 8:36.
  - McCormack and Celler together, 8:38. This is the call in which Johnson thanks Celler, so it is `-10`, and it follows Celler's remarks to reporters.
  - Rodino, 8:44, thanked for his work.
  - Corman, 8:46.
  - Roosevelt, 8:48.
  - Keogh, 8:49.
  - Thompson, 8:52, with Medicare to come next.
  - Katzenbach, 9:45, on the Senate strategy for both bills.
  - `-8` is now Celler's return call at 8:45. Johnson tells him they have already spoken.
  - Robert Kennedy's call to Rodino (`-17`) has no recording and keeps its evening range.
  - Halleck's call (`-6`, already in the tree) gets 8:35 p.m. and its recording.
- **Feb. 23.** Ayub Khan seeing Zhou off at the airport is added to the line (dashiji 395). The new wreath entry cites the Zhou nianpu, II, 622. It follows the Lahore citizens' reception on the printed order alone (395).
- **Feb. 27.** The talk was in the 总理办公厅, not the 总理办公室 (dashiji 396). The wreath's range is now the whole morning band, not one ending at 11. The order of the wreath and the talk now rests on "the printed order alone" (dashiji 396; Chen Yi nianpu 1017).
- **Feb. 28–29.** The tree already holds both private talks in `cal.1964-02-28.china-leadership-4` (Feb. 28–29). That entry is split under R17: it keeps the first talk (Feb. 28, 11 p.m.), and the new `cal.1964-02-29.china-africa-tour` takes the second (Feb. 29, 6 p.m.) and points back to it.
- **Mar. 19, 3:30 p.m. (`transition-and-staff-4`).** A Check is added: at his news conference Johnson puts Salinger's word to him at "about 4 o'clock", then "5 or 5:30" (1963–64 Pub. Papers 408).
- **Mar. 20, the arrival.** The Check on the filing deadline is reworded. Salinger's own hours ("twenty-two hours" from 7 p.m. California time, 348) put the deadline on Mar. 20.
- **Apr. 12–13, Changsha.**
  - The reader's moves of the redrafting (`-6`) to Apr. 13–14 and of Deng's call to Zhou (`-5`) to Apr. 13 are right. The Deng nianpu (III, 1809) and the Mao nianpu (Apr. 13–14) both put them there.
  - Moving `-4` whole to Apr. 13 was not right. Its line also held the General Office's summons on "the second night at Lanzhou" (Wu 744). That night is Apr. 12, the night before the flight.
  - So `-4` stays on Apr. 12 as the summons: evening, Lanzhou, with a Check that Wu's own dates make it Apr. 11.
  - The flight's details (Wugong, noon at Changsha, Peng Zhen on to Xi'an) go by `add-words` into `cal.1964-04-13.china-leadership-11`. That entry is already the flight, on the Deng nianpu. It gets a Check that Wu dates the flight Apr. 12.
  - The links from `-5` and `-6` to `-4` now cross two days, so they are removed, and their "See" now points to the Changsha meeting.
  - Deng nianpu III, 1809 is added to `-5`.
- **Apr. 26.** The JMZW page (XVII, 242) confirms 12:05 a.m. A Check is added: the printed note says "broadcast today" (今日), where Wu (769) has "tonight" (今晚).

## Struck

- The Check on `cuba-5` saying Schlesinger's adjournment "may be an earlier meeting". Doc. 229 settles it.
- Risen's cite and its Check on the 6:30 p.m. call. Both moved to the 9:07 p.m. call.
- The "Goldwater" sentence in the line of `cuba-5`. It is now gloss.
- The sentence in the Feb. 27 wreath's note on the order. It is replaced by the `follows` basis.

## Added

Five entries, all claimed in the ledger:

- `cal.1964-02-10.civil-rights-bill-18`: O'Brien, 8:20 p.m., with the House in the midst of the final vote, on the members to thank.
- `cal.1964-02-10.civil-rights-bill-19`: Brooks, 8:22 p.m., on the vote.
- `cal.1964-02-10.civil-rights-bill-20`: Albert, 8:32 p.m., congratulations.
- `cal.1964-02-10.civil-rights-bill-21`: McDowell, 8:55 p.m.
- `cal.1964-03-19.elections-1964-primaries-2`: Salinger leaves National Airport at 10 p.m. (Salinger, 348–49).

## For the merger

- **Do not run the proposed combine** of `cal.1964-04-13.china-leadership-11` into `cal.1964-04-12.china-leadership-4`. After this audit the two are distinct: the summons on Apr. 12, the flight on Apr. 13.
- **Settle these duplicate flags as distinct** (`./bib resolve ID --take keep`):
  - `cal.1964-02-07.cuba-5`
  - `cal.1964-02-07.economy-3`
  - `cal.1964-02-10.civil-rights-bill-7` to `-21`
  - `cal.1964-02-11.civil-rights-bill-5`
  - `cal.1964-02-20.china-africa-tour`
  - `cal.1964-02-23.china-zhou-foreign`
  - `cal.1964-02-27.china-africa-tour`
  - `cal.1964-02-29.china-africa-tour`
  - `cal.1964-03-19.press-and-broadcasting-2` (the 6 p.m. briefing; the existing entry is Merriman Smith's delegation at 4)
  - `cal.1964-03-19.elections-1964-primaries-2`

## What still waits

- The Daily Diary of Feb. 8, 1964, for the Ranch's clock. discoverlbj.org refuses this machine. The clock now rests on the Library's own log, as described above.
- The room of the Standing Committee meeting of Mar. 16. Wu (727) has the west hall of the Yinian Tang; the Mao nianpu has Room 118 of the Hall of the People. No record settles it, so the Check stays.
- The Feb. 10 calls the Miller Center lists that are not about the vote have not been entered: Carter, 8:15; the drafting of the statement with Salinger and Sorensen, 8:25–8:42; Valenti, 10:00; Jenkins, 10:10. They are items still to enter from the catalogue already read.
