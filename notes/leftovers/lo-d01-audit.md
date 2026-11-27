# Audit of leftovers lo-d01 (January to March 1960)

Opus audit, Nov. 27, 2026, of the patch `inbox/2026-11-27-lo-d01.yaml` and the reader's note `notes/leftovers/lo-d01.md`. The patch is corrected in place. `./bib patch-check`: 0 errors; 57 warnings, all of the kinds named below (the merge's duplicate flags, the same-day "one event?" notices, and three edits that set only `n`). Nothing merged, built or committed. A scratch copy of the tree with the patch merged (deleted after) gave `./bib check` 0 errors; its only warnings on the patch's entries were two "Names: none", now taken out.

## What was read

Every page below was read as an image (or, for the Mao nianpu and two English books, in the text, checked against the image where it mattered). All copies were fetched from the Drive, read, and deleted.

- Mao nianpu, IV (EPUB): Jan. 1 to Jan. 31, Mar. 2, Mar. 3, Mar. 17 to 19, 1960, with notes 2, 4, 7 and 8 of January.
- Yang Shangkun riji, I: printed pp. 468–493 (Jan. 6 to Mar. 30), page by page.
- Zhou Enlai nianpu, II (1997): pp. 281, 282, 286, 291, 292, 293, 295, 299.
- Zhou Enlai waijiao huodong dashiji: pp. 270–272.
- Peng Zhen nianpu, IV: pp. 2–4, 8, 9, 11.
- Peng Dehuai nianpu: p. 758 (not opened by the reader).
- Liu Shaoqi nianpu, II (1996): pp. 476–478 and 481 (481 not opened by the reader).
- Chen Yi nianpu: pp. 802, 806, 807, 808.
- Deng Xiaoping nianpu, III: pp. 1525, 1527, 1532, 1534, 1536.
- Jianguo yilai Mao Zedong wengao, XV: pp. 27, 49, 51, 55, 58.
- Zhu De nianpu (xinbian), III: pp. 1760, 1761.
- Schlesinger, *Journals*: pp. 64–65.
- Branch, *At Canaan's Edge*: pp. 437–38 and the notes, pp. 888–89.
- The Wilson Center transcript of Chen Yi and Chervonenko, Jan. 22, 1960: digitalarchive.umd.edu still answers 403 and digitalarchive.wilsoncenter.org does not connect from here, so it was read in the Internet Archive's copy of the Wilson Center page (captured Nov. 28, 2022).

## Ops checked

All 70 ops of the reader's patch were held to their pages. Every `edit`'s base was checked against the tree as it now stands: all 25 were current, and so are the 4 new ones. No other patch waiting in `inbox/` touches these entries. The hours and their UTC values were checked against the record's own words and the zone (Asia/Shanghai, America/New_York). The days touched were printed with `tools/times/day_order.py` (the brief names `tools/bib/day_order.py`, which does not exist) with the patch merged in the scratch copy, and read for their order.

Held as the reader wrote them: the hours on Jan. 6, 7, 9, 17 and 22, Jan. 23 (the dinner), Jan. 24 (2 a.m.), Mar. 7, Mar. 18 (the match) and Mar. 29; the new entries for Jan. 8, 10 (both), 11, 12, 13, 14, 15 (both), 19, 20, 24, 26 (the second Ne Win talk), 29, 31 and Mar. 2 (6 a.m.); the Jan. 25 split; the Mar. 7 day note; the cites and `add-words` on the Mar. 11 Secretariat; the Feb. 12, 1966 survey, entered under its right year.

## Ops changed

- Jan. 7: the Mao nianpu puts the opening session in the afternoon, at the Jinjiang Hotel's small hall; the diary has 11:30 a.m. The hour stays the diary's; the nianpu's reading is added as a variant on the time, and the diary is named as the time's source.
- Jan. 18 (Mao back at Hangzhou): the reader's cite put the evening, Liu Zhuang and the four companions in a parenthetical, and added "by train", which the page does not say. The facts now go into the line by `add-words`, with the names and tags, and the nianpu is named as the source of the time.
- Jan. 23, the flight: the talk with Mao is split off as before, but the forward pointer is gone, Mao's name and tag leave the flight, and the diary's cite is struck (I, 472 says only that Zhou will fly the next day). The Zhou nianpu prints the flight and the talk under Jan. 22 ("于次日"); the parenthetical now says so.
- Jan. 23, the talk with Mao: "Made public" is 1997 (the Zhou nianpu prints the talk), not 2013; the line adds "come from Peking for instructions" from the nianpu.
- Jan. 23, the ADA board meeting: kept; it now follows nothing and the rewrite of Humphrey's speech follows it, on the journal's order alone.
- Jan. 24, Deng's train: the Peng Zhen nianpu (IV, 3) puts Deng, Peng Zhen, Li Fuchun, Liu Lantao, Yang Shangkun and Hu Qiaomu on one special train. The reader had written this after "Names:", which only a Check may follow. It is now in the line by `add-words`, with the names and tags, and the train's hour, 10 a.m. from Yang's diary (I, 473), is set. Deng's entry and Yang's (`cal.1960-01-24.china-leadership-6`) record one departure; they are left as two entries, each man's act, and a later pass may combine them.
- Jan. 25: the second talk's cites stay on the first entry, because an edit may not drop a work read, and their parentheticals now say they are for the second talk.
- Jan. 25 and 26, Mao's train: each day held two acts, the arrival at dawn and a talk. Each arrival is now its own entry ("晨", early morning). The 2 p.m. talk is placed at Xiangtang (the gazetteer has the key), not Nanchang. The talk with Zhang Pinghua follows the arrival, and the afternoon talk follows it on the printed order.
- Jan. 28 (Peng Zhen and Yang call on Peng Dehuai): the Peng Dehuai nianpu dates the call only "春节期间" under Jan. 28. Yang's diary has Yang away from Peking from Jan. 24 to at least Feb. 21, and the Peng Zhen nianpu has Peng Zhen away from Jan. 24 to Feb. 27. Neither records the call in their days in Peking before Jan. 24. The Check now says this: the call is not Jan. 28, nor within the festival, for both men, and no record read gives its day.
- Jan. 29: the Liu Shaoqi nianpu has nothing on Jan. 29. The Check now asks whether the meeting at Liu's was the hearing on Peking's city plan the same afternoon (`cal.1960-01-29.china-leadership-2`).
- Jan. 30, Jan. 31 and Mar. 18 (Zhou's return): each edit dropped a person from the line but kept the name and the tag. Liu Shaoqi (Jan. 30), Mao (Jan. 31) and Liu Shaoqi (Mar. 18) are taken out of "Names:" and the tags.
- Jan. 17, Mao's lunch with Soong Ching Ling: "中午" has no hour, so it is now the band "workday midday" rather than a clock time of 12. The Zhu De nianpu (III, 1761) gives the banquet no hour, so the Check stays. The pointer to the plenary, another event, is gone.
- Mar. 2 (3 a.m.): the forward pointer and "3 and 6 a.m." in the cite are gone; the cite now gives the 3 a.m. date line.
- Mar. 3 (Mao's 4 a.m. comment): the reader's Check is settled, so it is not added. Mao's notes plan the meeting for the afternoon (XV, 55, 58). The Zhou nianpu has Zhou propose "三日下午或晚上" and go to Mao's "三日晚" (II, 291), and the Mao nianpu has the meeting that evening. A sentence of the note now says so.
- Mar. 6: finding the house repaired belongs with the evening's move (the nianpu's second item), not with the return. The later talk with He Qian ("后来") is an act of its own, dated "Mar., after the 6th". He Qian has no name entry, so he leaves "Names:".
- Mar. 11 (Zhou on the Koirala talks): the reader read "应邀于三月十日来华访问" as the date of the invitation. It says Koirala came to China on Mar. 10. The line keeps "who came on Mar. 10", and a Check sets it beside the airport welcome of Mar. 11 (Waijiao huodong 271; Chen Yi nianpu 806).
- Mar. 11, Liu's night meeting (`-5`): the Peng Zhen nianpu (IV, 8) gives 11 p.m. to 12:30 a.m. and has Zhou Enlai and Peng Zhen there. The hour and the two names are put in; the reader had left this unchecked.
- Mar. 15: the variant's value is now the evening range, the field's form, not the word "evening".
- Mar. 18: the Liu Shaoqi nianpu, II, 481 (read) bears out the Politburo meeting; it is cited there and is no longer "To check". The follows basis cited the *Mao Zedong zhuan*, which was not read; it now rests on the Mao nianpu ("晨" at Hangzhou) and the diary. The morning talk of Mao with Zhou Enlai and Chen Yi on Nepal, which was a parenthesis inside the Koirala entry, is its own entry, and Zhou's return follows it.
- Mar. 20: the hour's sentence stood after "Names:"; it is moved before it.
- Mar. 24: the 9-to-noon range was inferred; the diary gives no hour for the call. The range is struck and the Check reworded.
- Mar. 26: "中午" is now the band "workday midday" rather than an approximate clock time. The note quotes the nianpu and drops the reader's reading of noon as the train's start.
- The 1966 survey: "Names: none" is taken out.

## Ops struck

- `cal.1960-01-23.democratic-party-3`, Schlesinger's rewrite of Humphrey's speech, is struck as a duplicate of `cal.1960-01-23.elections-1960-nomination`, and its ledger claim is dropped. Its two `follows` ops go with it.
- The diary cite on the Jan. 23 flight.
- The parenthetical cite on Jan. 18, replaced by `add-words`.
- The Mar. 24 time range.
- The Mar. 3 Check, settled as above.

## Added

These are entries from pages the batch read that the tree lacked (R0, R5, R17). Each is claimed in the ledger.

- Jan. 9: Mao on *Xuanjiao dongtai* no. 1.
- Jan. 13: Mao on the material on *Mingzi*.
- Jan. 14: Mao on Li Xiannian's report on the villages' grain.
- Jan. 25 and 26: the train's two arrivals.
- Jan. 27: Mao's talks with Lin Biao and with Li Xiannian. The Mao nianpu's morning arrival and the Xiaodao guesthouse are added to the tree's Jan. 27 entry.
- Mar. 2: Mao reads the fourth volume of the *Selected Works*, 5 to 9 p.m.
- Mar., after the 6th: Zhou Enlai to He Qian.
- Mar. 18: Mao with Zhou Enlai and Chen Yi at Hangzhou.
- Feb. 1966: the *Montgomery Advertiser* on women jurors (Branch, 438; no note, so "Check: the day").

`follows` links were added on Jan. 23 (the call on Chen Yun follows the flight, which its own line shows), Jan. 26 (two), Jan. 27, and Mar. 18.

## The duplicate flags: settle all as distinct

The merge will flag these 26 entries. Each is a separate act from the entry it is flagged against, so each should be settled with `./bib resolve ID --take keep`:

- January, the evening meetings and comments at Shanghai: `cal.1960-01-08.china-shanghai-1960`, `cal.1960-01-09.china-shanghai-1960`, `cal.1960-01-10.china-shanghai-1960`, `cal.1960-01-10.china-shanghai-1960-2`, `cal.1960-01-11.china-shanghai-1960`, `cal.1960-01-12.china-shanghai-1960`, `cal.1960-01-13.china-shanghai-1960`, `cal.1960-01-13.china-shanghai-1960-2`, `cal.1960-01-14.china-shanghai-1960`, `cal.1960-01-14.china-shanghai-1960-2`, `cal.1960-01-15.china-shanghai-1960`, `cal.1960-01-15.china-shanghai-1960-2`.
- January, Zhou, the ADA and the second Ne Win talk: `cal.1960-01-23.china-zhou`, `cal.1960-01-23.democratic-party-2`, `cal.1960-01-26.china-zhou-foreign`.
- January, Mao's train and Guangzhou: `cal.1960-01-25.china-mao`, `cal.1960-01-26.china-mao`, `cal.1960-01-26.china-mao-2`, `cal.1960-01-27.china-mao`, `cal.1960-01-27.china-mao-2`, `cal.1960-01-31.china-zhou`.
- March: `cal.1960-03-02.china-mao`, `cal.1960-03-02.china-mao-2`, `cal.1960-03-06.china-zhou`, `cal.1960-03-18.china-mao-foreign`, `cal.1960-03.china-zhou`.

## What still waits, and on what

- Jan. 22, Chervonenko and Chen Yi, `-2` and `-5`: the transcript, now read, is the whole record of the 5 p.m. talk. It is on Laos only, and Chervonenko says he has nothing more to tell. The Zhou nianpu's India message (II, 281) has no hour. Nothing read shows the two to be one sitting, so they stay two entries and the Check on `-5` stands.
- Jan. 23: `cal.1960-01-23.china-leadership-9` has Zhou "flown in that morning", from the Chen Yun nianpu (III, 30), which was not opened. The flight's morning waits on that page.
- Jan. 28: the day of the call on Peng Dehuai waits on a record not yet found.
- Mar. 11: the day Koirala came (Mar. 10 or 11) waits on a third record, such as a Nepalese or press account.
- Mar. 20: `cal.1960-03-20.china-leadership-8` (Mao's office tells Yang of the Tianjin meeting, night) and `-7` (Gao Zhi's call, 12:30 a.m.) may be one act. The diary's "昨晚主席处通知" does not settle it.
- Mar. 17: the Mao nianpu has a morning meeting with the East China first secretaries at Hangzhou. It was not checked against the tree.
- The Mao nianpu's January month-dated items ("1月", "同月") and Jan. 1 to 5 were not checked against the tree in this audit; they are items still to read, not passed over.
- Branch, 437: Fred Graham's *New York Times* column of Feb. 13, 1966 is in the Feb. 7 entry's note, not an entry of its own (R13). It is an item still to enter.
