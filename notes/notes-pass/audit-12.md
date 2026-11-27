# Audit of batch 12: the notes pass

The patches are `inbox/2026-11-26-notes-pass-12.yaml` (55 entries) and `inbox/2026-11-26-notes-pass-12r.yaml` (what 12 left, and six new entries). Both were corrected in place. Copies of the patches as the readers left them were kept only in the scratch folder, which has been deleted. Patch 12 now holds 144 ops and patch 12r holds 63, including the audit's 13 new entries and its additions. `./bib patch-check` reports 0 errors on both. Its warnings are the duplicate-day notices for the new entries. Each new entry is a separate act from the entries beside it, and `./bib resolve ID --take keep` settles each one at the merge.

Every op was checked against its page. The books were fetched once each from the owner's Drive with curl, into a folder of my own, and deleted after use. Chinese scans were read as page images, one page at a time. English books were read by their text layers, with each printed page fixed from its running head or folio. The FRUS documents were read at history.state.gov. The Church report was read in the AARC copy (its Diệm chapter, pp. 218–19). The Daily Digest rows were read in `daybook/committees/1963-08.yaml`.

Under R0 I disregarded one limit. The readers' notes treated some reported acts as leads or as "candidates" because they had no day, or because the owner might not want each reaction as its own entry. Under R5, R15a and R50 these are entries, and they are now entered (below). I disregarded nothing else in the brief. The new rule R19b (Nov. 26) was applied: later recollection and commentary was moved into a `gloss`, not struck.

## What was read

- Peng Zhen nianpu, IV (PDF = printed + 4, page images): 221, 223, 242–44, 283–85, 287, 296–97, 306–07.
- Zhu De nianpu, new ed., III (PDF = printed + 6, images): 1852, 1853, 1863, 1881, 1890.
- Chen Yi nianpu (PDF = printed + 13, images): 939, 976, 1000.
- *Jianguo yilai Mao Zedong wengao* (2023), XVI (PDF = printed + 25, images): 435–36, 451, 482–84, 490–91; XVII: 63, 68, 131–32.
- Deng Xiaoping nianpu, III (PDF = printed − 1328, images): 1730, 1739, 1745–46, 1759, 1765, 1776.
- Yang Shangkun riji, II (PDF = printed + 5, images): 250–51, 298, 307–09.
- Wu Lengxi, *Shinian lunzhan* (PDF = printed + 8, images): 527, 567, 610, 613–14, 623–24.
- MacFarquhar, *Origins*, III (text): 351–52, 358, 410.
- Yang Jisheng, *Tiandi fanfu*, I (text): 75. *Mubei*, II (image, PDF 1116): 1127 and n.33.
- *Brothers in Arms* (EPUB pages): 383, 385–87.
- *Prezidium TsK KPSS*, I (text): 622–23.
- Zhou Enlai nianpu, II (1997; image): 566. *Zhou Enlai waijiao huodong dashiji* (1993; image): 339. *Zhonghua renmin gongheguo waijiao dashiji*, II (2001; image): 250.
- O'Donnell and Powers, 310–12, 369–70. Dobrynin, 81–82. Sorensen, *Kennedy*, 701–02, 738–39. Schlesinger, *Robert Kennedy*, 537. Thomas, 237–38. Navasky, 328–29. Guthman, 134–36.
- Novak, *Agony*, 109–10, 239–41. Smith, *On His Own Terms*, 393. Dikötter, *Cultural Revolution*, 22 and n.24. Miller, *Misalliance*, 257–58.
- Purdum, 55–58, 137, 191–92. Risen, 76, 106, 133, 159–60. Whalen, 27, 49–52, 109–11, 116–17, 124–25. Kotz, 63, 90. Mann, 377. Bernstein, 31–32, 34, 36, 52–55, 97, 251–52. Zelizer, 100.
- Lady Bird Johnson, *Diary*, 24–26, 33–35. Salinger, *With Kennedy*, 336. Sorensen, *Counselor*, 346–47, 381. White, *Making of the President 1964*, 108–10. Chen Jian, *Zhou Enlai*, 499–500.
- Taylor, *Swords and Plowshares*, 287, 291–95. Selverstone, 143. Logevall, 51. Kaplan and others, *McNamara Ascendancy*, 138–39. Moyar, 251–52 and nn.38–40. Caro, *Passage of Power*, 422–23. Dallek, *Flawed Giant*, 60, 72. Reeves, 556. Chang, 249, 251. Fursenko and Naftali, *Khrushchev's Cold War*, 511 and nn.65–68.
- FRUS 1961–63, III, doc. 281; IV, docs. 1 and 37; VII, doc. 362. The Church report, 218–19. The Daily Digest for Aug. 14 and 15, 1963 (D391, D396).

## What could not be read

- Harold Ford, *CIA and the Vietnam Policymakers*, 35. The Drive does not hold it; I searched the inventory and ran the Drive search by title. It stays behind "To check:" on `cal.1963-10-02.press-and-broadcasting-2`.
- The *New York Times* of Oct. 4, 1963 (Halberstam). Newspapers are not readable here (R56). It stays behind "To check:".

## The pages that changed the patches

These are listed by entry. "Holds" means the page bears out the op as the reader wrote it.

- `1962-10-26` and `1963-10-31-6`: the reader cited the Peng Zhen nianpu for "Peng Zhen and Zhu De attend", but that page names only Peng. Each line now has two parts, each cited to its own chronology. The Zhu De nianpu, 1890, has Zhu "discuss" the sixth draft, not see it passed.
- `1962-10-28.china`: holds. "The Great Hall of the People" was added from the Peng nianpu, 223. The Deng nianpu, 1730, the Zhou dashiji, 339, and the 2001 volume, 250, were read, and all agree with the line.
- `1963-01-29`: holds. The repin is to 242–43.
- `1963-02-06-3`: holds. Zhu De attends on Feb. 7 (1863). Yang Shangkun's diary (250–51) gives the hours and the day-by-day topics, now put in the line. The time field was set to the first day's 3 p.m., and the note says so.
- `1963-07-08-3`: Suslov's proposal is in the Soviet record (*Brothers in Arms*, 383), not in the Peng nianpu, so it is now a part of its own, attributed to the Soviet record.
- `1963-07-13-2`: the reader's Check was reworded. Wu Lengxi (613) and MacFarquhar (352) have Ponomarev speak on July 12. The Peng nianpu has him on July 13. The line has the delegation answer him on the morning of the 13th.
- `1963-07-14-4`: the reader's Check was struck. The Peng nianpu's evening meeting is the evening meeting of `cal.1963-07-14.china-leadership-5`, which Wu (613) dates "in the evening, again" and which already cites the Peng nianpu. It does not contradict this entry's afternoon.
- `1963-07-17`: holds. Yang (298) gives 10 a.m. to 1:45 p.m. with a twenty-minute break; the words were added and the time field set (07:00Z).
- `1963-07-21`: holds. The cites left unread were read: the Zhou nianpu, 566; the Zhu De nianpu, 1881; MacFarquhar, 358. They bear out the line as their parentheticals say.
- `1963-08-20`: holds. Aug. 24 (Nie Rongzhen and Cheng Zihua, 309) and Peng's "afternoon" were added. The time field was set to the first day's 10 a.m.
- `1962-11-19`: holds. The items were repinned to the notes that carry the words (436 nn.1–2; 435 and 436 n.3).
- `1962-12-30`: Deng's report of Dec. 29 is the act of `cal.1962-12-29.china-leadership-4`. The reader's words were struck here, and "many revisions" was added there, from the Wengao (451 n.3) and the Deng nianpu (1739). Deng's forwarding of Mao's comment is a transmittal (R18), so it was struck.
- `1963-02-20-2`: the Hebei report of Feb. 17 is an act of its own and is now a new entry. The issue of the reports on May 20 as annexes was moved to `cal.1963-05-20.china-leadership-5`.
- `1963-02-06`: holds (Wu, 527). The fourth Wengao item was added: Mao sends Chen the report of de Gaulle's proposal to Khrushchev (483 n.1, 484 n.5).
- `1963-09-13`: Mao's note of Sept. 11, 7 a.m., is a dated act with its own hour, so it is now a new entry. Kang Sheng and Wu Lengxi's report of Sept. 10 (68 n.1) is also a new entry. Mao's closing words to Khrushchev (68, item 14) were added to the line.
- `1962.china-leadership-47`: Mao's earlier criticism is already `cal.1962-07.china-leadership-13`, so the reader's words were struck. Kang Sheng's campaign against Wang Jiaxiang is a new entry, from *Tiandi fanfu*, I, 75, and *Mubei*, II, 1127 (task 2: read; it rests on the same Yan Mingfu article).
- `1963-07-01-4`: the Soviet delegation (Suslov, Andropov) is not part of the July 1 statement (MacFarquhar, 351), so the words and tags were struck and the entry tagged `ok:note-substance`.
- `1963-03-6`: Dikötter (22) holds, as his account. MacFarquhar's words (410) were kept, attributed to him and marked as later ("spurred by the rising leftist tide"). A Check says that the two works name different senders and that neither dates the interrogations.
- `1962-10-22-6`: Dobrynin's noon at the New York airport is a new entry. Kohler's delivery in Moscow belongs to the letter, so it was moved to `cal.1962-10-22.missile-crisis-2`. Rusk's words hold. The time field was set to 6 p.m. (Dobrynin and Sorensen), and the range was dropped.
- `1962-10-20-3`: holds, except that the papers agree to hold the story until Kennedy has confronted Khrushchev. "Monday night" was O'Donnell's request, not their answer.
- `1962-12-24.cuba`: Cushing's and Clay's money is the act of `cuba-2`, so it was struck here. Schlesinger (537), Thomas (237) and Navasky (329) hold.
- `1962-12-24.cuba-2`: "At the President's suggestion" is O'Donnell's own narration, not Cushing's account, and was reworded so. Guthman (136) holds. "Sunday" now refers to the day of Castro's demand.
- `cuba-4` and `cuba-5` (12r's new entries): both hold (Guthman, 136). For `cuba-5`, the time zone was changed to America/Havana, since the 3 p.m. deadline is Castro's.
- `1963-01.states-and-cities`: holds. Novak's $67 million is on 109. Smith's 1923 and 1934 are Rockefeller's argument, and the words now say so.
- `1963-06-15.mississippi`: the funeral is `cal.1963-06-15.mississippi-2`, so the words were moved there.
- `1963-06.civil-rights-bill`: holds. Kotz (63) and Mann (377) both name Stennis and give the words, and the line says so.
- `1964-02-08.women`: Bolton and the others are on Whalen 117, not 116. Griffiths's "I used Smith" is her later account, so it was moved into the gloss under R19b. This settles 12's open point.
- `1963-08-28.civil-rights-bill`: holds (Whalen, 27; Risen, 106). Whalen puts Johnson's remark in the meeting, and the line gives it as Whalen's account. This settles 12's second open point.
- `1963-10-23` and `1963-10-29.civil-rights-bill`: both hold. The time fields were set from the pages: "just after 6:00 p.m." (Purdum, 137) and 10:45 a.m. (Risen, 133). The ranges of kind were dropped.
- `1963-12-29.europe`: von Braun is on 25, so the item was repinned to 25–26. `1964-01.elections-1964-3` was repinned to White 109. White gives Friday, Jan. 10 and the Monday after, and a Check now says so.
- `1963-02-08.middle-east`: the parenthetical quoting Critchfield (2002) and Sa'adi was moved into the gloss under R19b, each with a date.
- `1963-08-24.vietnam`: the cable's words were cited to FRUS III, doc. 281, which prints them, and to the Church report (218–19). Taylor 293 was dropped as a cite, because it bears only part of the words.
- `vietnam-6`: Taylor's reading of the cable was moved into the gloss (R19b).
- `1963-08-28.vietnam`: Selverstone (143) gives Ball's words to Ball and Harriman, so it is now a variant, not a cite.
- `1963-08-31.vietnam-2`: Harkins's approach is part of the day's report, so it was moved to `cal.1963-08-31.vietnam`. Logevall (51) holds.
- `1963-08-15.testing`: Reeves (556) and Chang (249, 251) hold. The Daily Digest (D396) dates Taylor's testimony before Foreign Relations to Aug. 15 and is cited for the date.
- `1963-10-02.press-and-broadcasting-2`: Moyar gives Reston's remark no day. His "two days later" runs from Starnes's column (n.38) to Halberstam (n.40). The entry is now "Oct. 2–4", with a Check.
- These ops hold as written: 10-20 (Peng, Zhu De), 10-27 (protocol, 623), 1963-05-12 (Miller 258), 05-17, 05-30, 06-11 (Sorensen's drafting repinned to 55–56), 07-12, 07-23, 08-13, 09-24 (Kaplan 139), 11-12, 11-24, 11-25 (Bernstein 31–32; Caro 422–23; Dallek 60, 72), 12-13-3, 12-21-3, 12-29 poverty, 1964-01-07 (tag), 01-08, 02-05, 02-07 (Boggs "seconds", Risen), 02-11. Also the 12r Deng additions on 01-29, 02-06-3, 07-17 and 10-31-6.

## New entries (13), claimed in the ledger under `notes-pass-12r`

- `cal.1963-12-13.china-economy`: Peng Zhen forwards Mao's comment on *Qunzhong fanying* no. 84 and instructs Liu Ren and Wan Li (Peng nianpu, IV, 306–07). This is task 3.
- `cal.1963-12-21.china-economy`: Peng sends Jia Xingwu's report on Peking's unemployed (307).
- `cal.1964-06-08.china-four-cleanups`: Mao likes the Baiyin report and the inquiry is widened. It is dated "By June 8" from Dikötter's context, with a Check (task 3).
- The $53 million guarantee (task 3) is the letter of credit of Dec. 16, already `cal.1962-12-16.cuba`. Navasky (329) is cited there, and the Red Cross added.
- `cal.1963-08-14.testing`: Taylor before Stennis's subcommittee (task 3). The Daily Digest (D391) gives Aug. 14, and Taylor (287) gives "successive days". A Check notes Sorensen's other order.
- `cal.1963-02-17.china-four-cleanups`: the Hebei report.
- `cal.1963-09-10.china-polemic` and `cal.1963-09-11.china-polemic`: Kang Sheng and Wu Lengxi's draft; Mao's note at 7 a.m.
- `cal.1962-10-22.missile-crisis-diplomacy-5`: Gromyko's departure at noon and Rusk's summons.
- `cal.1962.china-india-war`: Kang Sheng's campaign against Wang Jiaxiang.
- `cal.1963-05-10.vietnam-3`: the Pentagon spokesman's "one to three years" (Miller, 258).
- `cal.1963-10.goldwater-9` and `-10`: Howard Baker's and Rubel Phillips's statements on Goldwater's TVA letter (Novak, 240).

## Ready to merge

Both patches show 0 errors. Patch 12 should merge before 12r, because 12's edits carry the base revs of the tree as it stands. At the merge, settle the duplicate-day flags of the new entries with `--take keep`.
