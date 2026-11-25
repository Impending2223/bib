# Audit of the re-ruling on the printed order, group G: June to Nov. 1966, Jan. to Mar. 1967, May 1967

The patch audited is `inbox/2026-11-25-rerule-printed-g.yaml`, written by a Sonnet reader, with its note `notes/sequence/rerule/printed-g.md`. The rule is R25c as the owner rewrote it on Nov. 25, 2026 (owner-rulings 56): where a chronology or a volume is otherwise in the order of time, an item it prints after another of the same day follows it, unless something goes against it. I disregarded nothing under R0: the brief added nothing that narrows.

The corrected patch has 62 links. Every basis holds the words "the printed order alone" and the page. `./bib patch-check` shows 0 errors and 0 warnings.

## What I read

- The reader's brief whole, CLAUDE.md, owner-rulings 55 and 56, and the guides the brief names.
- The sequence notes and audits of the ten months, and their merged patches. I compared each merged patch with the reader's patch as first committed in git. The links struck on the printed-order ground are two, June 27 and Aug. 3, 1966, as the reader found.
- The day sheets of June to Nov. 1966 and Jan. to May 1967 (`day_order.py --full`), and every entry the patch names, in full.
- *Zhou Enlai nianpu* (2020), III, pp. 44, 60–64, 73, 78–79, 81–84, 88–89, 118–119, 121–122, 130–138, 147–148, 152–153, each page read as an image (printed page = PDF page − 4).
- *Chen Yi nianpu*, pp. 1153–54, 1162, 1167, 1170, 1172, 1175–76, as images (printed page = PDF page − 13).
- *Ye Jianying nianpu*, II, 947, as an image (printed page = PDF page + 553).
- *Zhou Enlai waijiao huodong dashiji*, pp. 503–04, as images (printed page = PDF page − 13). The reader had not opened it.
- The Mao nianpu EPUB: June 10, 1966; Sept. 5, 1966; Oct. 1–25, 1966.
- For the narrative days: Pu Weihua, *Zalan jiu shijie*, 148 and 163 (images); Yang Jisheng, *Tiandi fanfu*, I, 397 and 490 (text layer); Gibbons, IV, 326–27, 450–52, 463–67 (text layer); Teiwes and Sun, 79 (text layer).

Every copy was fetched into a scratch directory of my own under /tmp and deleted after reading. Nothing on Drive was changed.

## Are the volumes otherwise in the order of time?

Yes, on every page read. In the Zhou nianpu, Oct. 20, 1966 runs 凌晨, then the afternoon Special Commission, then the evening talk with Liu and Deng. In the Chen Yi nianpu, June 26, 1966 runs 上午, 下午, 晚上; Oct. 3 runs 上午, 上午, 下午, 晚上, 晚上; Oct. 24 runs 上午, 上午, 中午12时, 晚上. The dashiji's Aug. 19–20, 1966 run by the clock. The Mao nianpu's Oct. 24, 1966 runs the evening meeting, then the test report, then Chen Boda's speech (11 p.m. in the tree). The audit of August took the "this afternoon" of the third Aug. 3 item as proof of disorder; it is not, since that reply was written before the afternoon and the two items above it have no hour.

## Links checked: 51. Kept: 49. Struck: 2. Turned: 0. Repointed: 0.

### Struck

- Oct. 30, 1966: `-4` (calls on rail transport) after `-3` (the draft provisions). The calls are printed under the heading "10月30日、31日" (III, 84), after the day's own items. That places a two-day heading after a one-day heading. It says nothing of where on Oct. 30 the calls began, or whether any fell on Oct. 30. A link runs within one day.
- Feb. 7, 1967: `-4` (the talks on Xinjiang, Feb. 7–8) after `china-leadership` (Mao's note). The same reason: the talks are printed under "2月7日、8日" (III, 121), after Feb. 7's items.

### Kept, with what I found

- June 10, 1966 (Mao nianpu): Hồ Chí Minh's reception printed first, then "同日 晚上" the meeting. Kept.
- June 19 (Chen Yi, 1153): both 晚上, the reception of the troupe's heads printed before the show. Kept.
- June 27 (Chen Yi, 1153–54): the opening, then "上午" the reception, then "晚上" the banquet. This is the weakest link of the month. Nothing goes against it. Since the editors mark the reception as morning and print the opening before it, the presumption puts the opening in the morning. Kept.
- Aug. 3 (Zhou III, 44): the message to Ye Lin, then the talks with Wang Li and Guan Feng and then with Ye Lin. The first item says the Cultural Revolution Group must be consulted and Ye is to send his draft. The second has Zhou talk with two of the Group's members, then with Ye. The words agree with the order. Kept.
- Aug. 22: Chen Yi, 1162, and the dashiji, 503–04, both print the signing first and the airport second, both in the morning. The basis now names both. Kept.
- Sept. 10, 12, 16 (two), 17, 18; Oct. 7 (two), 20 (four), 26, 28 (two), 29, 30 (two), 31 (two); Nov. 14 (three); Feb. 1 (two), 9 (three); Mar. 7, 10, 13 (two), 23; May 5, 8 (three): each pair is in the order the page prints, and nothing in the entries' words, hours or ranges goes against it. On May 8 the Tibet answer says Zhou settled the matter "last night" (昨夜), which fits the before-dawn talks printed first. Kept.
- Oct. 3 (Chen Yi, 1167): Zhou's reception, then the thanks banquet, both 晚上, after a day printed by the clock. Kept.
- Oct. 24 (Ye II, 947): Ye's words at the second group, then "晚" the report to Mao on the test. The October audit asked whether Ye's words repeat Mao's evening talk at the pool. The Mao nianpu has Mao say much the same on Sept. 5, 1966 ("越开调子越高，一定要说成反党反社会主义"), so Ye may be quoting the earlier words. Nothing goes against the order. Kept.
- Nov. 1 (Chen Yi, 1172): both 晚上, the Algerian reception printed first. Kept.
- Mar. 21, 1967 (Zhou III, 135–36): the four links, the last of them the railway reception ("晚") after Zhou's report at Mao's. The report has no hour in Zhou's chronology and "evening" in Mao's. The editors print it first and mark only the reception "晚". Nothing goes against it. Kept, as the weakest of the month.

## Links added: 13

Cases the reader missed, or days its note left unread where the month's note had left the pairs as "the item after" only:

- June 21, 1966: `-19` (Bo Yibo's call to the work group to strike back) after `-18` (Wang Guangmei: Kuai Dafu means to seize power). Pu, 163, a narrative, tells the day through in order: "21日，王光美明確指出：蒯大富要奪權。薄一波打電話給工作組指示反擊。" then turns to June 24. The basis names the book as a narrative (owner-rulings 56, reading 5).
- Oct. 24, 1966: `-11` (Chen Yi's talks with Pirzada) after `-4` (Zhou's reception of Pirzada). Chen Yi, 1170: both "上午", the reception printed first.
- Nov. 28, 1966: `-6` (Chen Yi at the Albanian rally, afternoon) after `-5` (Chen Yi's cable to Nase). Chen Yi, 1176: the cable, then "下午" the rally, then "晚上".
- Mar. 2, 1967: `-2` (the Xi'an delegates) after `china-leadership` (Yang Dezhong on the Peking Hotel), and `-3` (Daqing) after `-2`. Zhou III, 130.
- Mar. 7: `-4` (the meningitis letter) after `-2` (Mao's note on the Tianjin school report), which the volume prints as the day's first item. Zhou III, 130–131.
- Mar. 14: `-3` (the Huairou telegram) after `-2` (the proclamation on factories). Zhou III, 133.
- Mar. 17: `-3` (the defence-industry reception) after `-2` (the letter to Li Fuchun and the others). Zhou III, 134.
- Mar. 22: `-2` (the talk with Kuai Dafu after the workers' congress) after `china-leadership` (the Peking Hospital notice). Zhou III, 137.
- Mar. 24: `-2` (Qinghai) after `china-leadership` (the Health Ministry meeting), and `-3` (Xinjiang) after `-2`. Zhou III, 137–138.
- May 26: `-3` (the Hohhot delegates) after `-2` (the Academy of Sciences), and `-4` (the Urumqi answer) after `-3`. Zhou III, 153.

## Left without a link, and why

- Mar. 9, 1967: the Public Papers print the special message (item 103) before the news conference (104). At 3:33 p.m. the President opens the conference: "I am sending a message to the Congress this afternoon." That says the message was still going, not gone. The President's own words go against the printed order, and they win. No link.
- The narrative and newspaper days. Reading 5 of owner-rulings 56: a narrative's page order counts only where the book tells that day through in order.
  - June 5, 1966 (Pu, 148): the second poster comes in a sentence that goes back to "在這一天還" (on this day also), after the reaction to the first. The book adds an item of the day, it does not tell what came next. No link.
  - Aug. 3, 1966 (Yang, I, 490): each sentence starts again with "8月3日晚". The book dates two items of one evening; it does not tell one after the other. No link.
  - Feb. 19, 1967 (Yang, I, 397; not in the reader's list): the killing, "矛盾更加激化", then "當天" the meeting. The book starts the meeting's sentence again from "that day". The same reading as the two above. No link.
  - June 2, 1966 (Gibbons, IV, 326–27): the text gives the paper of May 27; the notes give the shorter version and the cover note of June 2. No day told in order. No link.
  - Oct. 10, Nov. 4 and Nov. 11, 1966 (Gibbons, IV, 450–52, 463–67): the book gives the briefing without a day, the meetings of Nov. 4 and 5 together with "no known notes", and the approval of Nov. 11 apart from the memorandum. No link.
  - Mar. 20, 1967 (Teiwes and Sun, 79): the page sets Lin Biao's and Zhou's speeches side by side for contrast. No link.
  - Aug. 23, 1966: two editorials on one front page. A page of a newspaper is not a volume in the order of time. No link.
- Oct. 7, 1966: Mao's reply to Zhou's letter is inside the day's first item ("毛泽东当天批示"); the volume does not place the reply against the items after it. No link.
- Mar. 10, 1967: Mao's note on Zhou's report is not on Zhou III's page for the day. No link.
- Mar. 17 and 18, 1967: the Mao entry of Mar. 17 (his agreement to Zhou's before-dawn proposal) is inside the first item, like Oct. 7. On Mar. 18 the first item, Zhou's letter to Mao and Lin, has no entry. No link.
- May 26, 1967: Zhou's talk with the marshals (`-5`) is printed inside May 25's item as "次日". No link.
- June 27, 1966: the opening and the evening banquet need no link; the banquet's range places it after the reception, which now follows the opening.

## What is left

- Days on the pages read with runs of Zhou's or Chen Yi's items that no note named and that this audit did not take up: Sept. 15, 1966 (the late-night call, then the talk with Nie Rongzhen, III, 63) and Nov. 15, 1966 (four items, III, 89). The Mao nianpu's own runs of items on one day were not read for this pass.
- The Feb. 19, 1967 Xining pair, and the two other narrative pairs above, are for the owner if the owner reads reading 5 more widely.

## Ready to merge

Yes. The patch shows 0 errors and 0 warnings.
