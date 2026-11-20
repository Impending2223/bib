# The crime rule: what readers passed over as crimes (Nov. 20, 2026)

The owner, Nov. 20, about 1:10 a.m. Pacific: "Civil disorder killings and lesser crimes would also go in, wouldn't they? ... Have we dropped content there because of the 'crime' rule? ... Heck, just drop it." R18's crime clause is struck (`notes/briefs/reader.md`, R18; commit 9b82810). This sweep lists the events the record shows were left out on the ground that they were crimes, so the lead can have them entered.

## The window

The lead's narrowing, relaying the owner ("I believe the crime rule is too recent to have had much of an effect ... Don't search anything before its date."): R18 first named crimes on Nov. 14, 2026, about 7:23 p.m. Pacific (commit ad55daa, 2026-11-15 03:23 UTC). Only work written after that moment is searched here.

How it was made. `git log --since="2026-11-15 03:23 UTC" --name-only -- notes/book-checks notes/briefs notes/proposals inbox/merged` gave 146 files: 17 book-checks, 8 briefs, 7 proposals and 114 merged patches. `git blame --since=...` on each note file kept only the lines written in the window, along with the working tree's uncommitted lines (6,475 lines). Those lines were searched with `rg -i`: first for the grounds (crime, criminal, "no trace", "police matter", "not political", "routine of order", 犯罪, 刑事, tội phạm, hình sự), then for the acts (murder, killing, rape, theft, robbery, arson, looting, riot, sniper, lynching, bombing, hijacking, cannibalism; 杀/殺, 打死, 盗, 偷, 抢/搶, 强奸/強姦, 人吃人, 武斗; giết, cướp). Each hit was read in its row. The merged patches were searched for "passed over", "a crime", "no trace" and "police matter". Each event was then looked for in the calendar by its day, place and page (the cal tree and `inbox/*.yaml`).

The 17 book-checks in the window are all on Chinese and Vietnamese sources, plus *77 Conversations*: Dikötter; Yang Jisheng, *Mubei* and *Tiandi fanfu*; MacFarquhar, *Origins* and *Mao's Last Revolution*; the *nianpu* of Mao, Zhou, Liu and Deng; the *wengao*; *Mao Zedong zhuan*; Wu Lengxi; Yang Shangkun's diary; the *Waijiao dashiji*; Zhou's *waijiao huodong dashiji*; *Lịch sử kháng chiến chống Mỹ*; *Văn kiện Đảng toàn tập*. Two of them have rows passed over on the crime ground. Each reading section in the window has its Passed-over list or a statement that nothing was passed over, with one exception: *Liu Shaoqi nianpu*'s "1960–69" section, a run that stopped before writing any entry. No US source falls in the window.

## Dikötter, *Mao's Great Famine* (`notes/book-checks/dikotter-maos-great-famine.md`)

Copy: Drive `1y0-egg5cfmJCT-R12r4OxJDP92h6xVTl` (Bloomsbury paperback, 2017; PDF = printed + 28 to p. 198, + 36 after).

| Book-check line | Page | Date | Event | Ground given | Calendar now |
|---|---|---|---|---|---|
| 75 (run 2, Passed over) | 322 | Jan. 9, 1960 | Linxia list: Kang Gamai kills and eats Maha Maiji, Maiji commune | "a crime, with no trace in politics or policy beyond the list itself" | Pending, not merged: added by the run-3 audit (uncommitted, line 156: "3 Linxia cases"), `inbox/2026-11-19-b15c-dikotter-3.yaml` (place linxia). The list itself is held: `cal.1961-03.china-leadership-22`. |
| 75 | 322 | Feb. 25, 1960 | Linxia list: Yang Zhongsheng kills and eats his brother, Hongtai commune | the same | Pending, the same patch |
| 75 | 322 | Mar. 1960 | Linxia list: Zhu Shuangxi exhumes and eats her husband and son, Hongtai commune | the same | Pending, the same patch |
| 76 (run 2, Passed over) | 258 | 1960 | Two commune party secretaries of Wengcheng rape or coerce thirty-four women | "a crime (R18), no policy trace in the book" | Held: the run-2 audit, line 103 (j), overruled it ("using their office"); `cal.1960.china-leadership-39` |
| 109 (run-2 audit, "Not entered, for run 3") | 224 n.1 | July 1961, after the typhoon | Cangzhou villagers, armed with sickles, steal the corn from the fields | "Passed over (R18, a crime with no trace in the book)" | Pending, `inbox/2026-11-19-b15c-dikotter-3.yaml` ("some villagers of Cangzhou ... steal the corn"). The party secretary's raids are held: `cal.1961-07.china-leadership-8`. |

The record carries 5 events passed over on the crime ground. 1 is held; 4 are pending in the run-3 patch, which waits to be merged. No re-read is needed.

## Yang Jisheng, *Mubei* (`notes/book-checks/yang-jisheng-mubei.md`)

Copy: Drive `1Fb2pT-0OZvyMccyoGrIoXfRGiHIegqSW` (the June 2016 printing; one 1,205-page image scan, traditional characters, no text layer). The folio offset changes by chapter; each page's footer gives it (ch. 2 +1 to ch. 14 +8, lines 9 and 114).

Run 1, line 58 ("Passed over (R44; only R18's grounds)"), and run 2, line 152 ("*Crime with no trace in politics or policy* (the act is a private person's, no organ's act dated)"). Both readers entered the organs' reports of the cases and passed over the cases themselves. The calendar holds the reports. For the cases below no entry of their own was found on their day or place (tree and inbox).

| Book-check line | Page | Date | Event | Ground given | Calendar now |
|---|---|---|---|---|---|
| 58 (run 1) | I, 40–42, 62–64 | to Jan. 8, 1960 (the in-span days, Jan. 6–8) | Huaidian commune and Guangshan: the atrocities and deaths the chapter lists by day, the death of a cadre on Jan. 8 among them (Oct. 1959–Jan. 5, 1960 out of the span) | "crimes, and deaths, with no act of the Party or state" | Not held as cases. The figures are held through the reports: Henan committee, Nov. 1; Li Li, `cal.1960-11-28.china-leadership-10`. |
| 152 (run 2) | I, 210–211 | June 1960; winter 1960 | Mianzhu: killings or eating of the dead (from a letter of 2011) | "Crime with no trace in politics or policy" | Not held |
| 152 | I, 223 | Dec. 13–15, 1960 | Longwang and Zhuyan communes, Sichuan: the cases; the Sichuan suicides of the same days | the same | Not held |
| 152 | I, 274–281 | Feb.; Mar. 3; Mar. 24; May; June; July 1960 | Fengyang, Anhui: cadres' beatings and burials (six dated cases or groups) | the same | Not held as cases. The county's reports and meetings are held (e.g. `cal.1961-01-08.china-leadership-7`, `cal.1961-01-15.china-leadership-5`, `cal.1961-02-10.china-leadership-9`, `cal.1961-11-07.china-leadership-4`). |
| 152 | I, 288–291 | Apr. 1960; May 1960 | Wuwei 無為, Anhui: the cases | the same | Not held as cases. Reports held: `cal.1960-07-18.china-leadership-5`, `cal.1960-11-27.china-leadership-3`, `cal.1961-01-14.china-leadership-7`. |
| 152 | I, 309–312 | Mar. 17–21; Mar. 28; spring 1960 | Bo 亳 county (Haoxian): the cases, told from recollections | the same | Not held as cases. The reports of Mar. 3, late March and May 25 are held (e.g. `cal.1960-03-03.china-leadership-11`, `cal.1960-03.china-leadership-6`). |
| 152 | I, 417–418 | Mar. 1960 | Shixing, Guangdong: the cases | the same | Not held as cases. Report held: `cal.1960-07-31.china-leadership-6`. |
| 152 | I, 422–423 | 1960 (the row gives no days) | Guangdong cases | the same | Not held as cases. The four-level meetings' reports are held (`cal.1960-12-26.china-leadership-5`, `cal.1961-01-21.china-leadership-4`). |
| 152 | I, 392–395 | 1960 (the row gives no days) | Jiangsu cases | the same | Not held as cases. Reports held: `cal.1960-08-24.china-leadership-5`, `cal.1960-09-18.china-leadership-4`, `cal.1960-10-19.china-leadership-9`, `cal.1960-12-27.china-leadership-4`. |
| 152 | I, 216 | undated | The Guanghan hospital head buries a living man | the same (undated in the book) | A lead (R50), not an entry. The hospital report is held: `cal.1960-12-13.china-leadership-5`. |

The same row names cases that the reader says are already in through their reports, and that are held: Puyang and Chongyi, Mar. 16 (`cal.1960-03-26.china-leadership-8`); Dayi, Apr. 23 (`cal.1960-04-25.china-leadership-12`); the withheld meals of Jiangjin (`cal.1960-05-02.china-leadership-5`, `cal.1960-05-03.china-leadership-6`); Meitan (`cal.1960-01.china-leadership-7`, `-04.china-leadership-15`, `-06.china-leadership-5`, `-08.china-leadership-7`); Wu county (`cal.1960-09-05.china-leadership-5`); the Hebei poisonings (`cal.1960-09-21.china-leadership-5`, `cal.1960-10-07.china-leadership-9`). Whether each case in those reports also wants an entry of its own, by the ruling of Nov. 20 (`notes/briefs/batch15b-prc.md`: "each dated case the source records is an entry ... and the list or report that gathers them is its own entry besides"), is for the re-reader to settle on the page.

Runs 3 to 6 of *Mubei* pass over no crime (their Passed-over lists: lines 225, 271, 294, 390, 450). Run 4 enters the police cases of 1961–62 (its Doubts, line 314).

The record carries 2 rows and about 17 dated cases or groups, plus 2 page ranges whose days the row does not give. None is held as a case of its own. All want a reader's re-read.

## Other rows in the window, near the question but not on the crime ground

- Yang Jisheng, *Tiandi fanfu* (`notes/book-checks/yang-jisheng-tiandi-fanfu.md`, line 138): "the beatings and deaths of teachers and others from Aug. 4 to Sept. 27" (I, 249–250, 267–270, 279). These were passed over on a scope limit ("outside 'organs and leaders'"), not as crimes. The run-2 audit (line 186) ruled them in under R5 and the owner's Nov. 20 words, with 51 entries on the scope ruling, in `inbox/2026-11-19-b15c-tiandi-2.yaml` (pending). For run 3 it left pp. 254–256, 259–260, 263, 273–278 (the Pickets' acts, the daily death toll) and leads for undated victims (line 188).
- MacFarquhar, *Origins*, line 613 (408 n.50, Nov.–Dec. 1964, the Hongdong and Tong xian beatings, suicides and deaths) and *Mubei*, line 452 (II, 1144, the four cleans suicides): passed over as statistics with no day, not as crimes.
- The merged patches in the window carry no passed-over row on a crime ground. Their "a crime" hits are words inside entries (Zhou Enlai on the vault robbery; Zhang Chunqiao at Anting; the NLF on Huế).

## Summary

- **Events passed over as crimes, in the window: two sources, both on the Chinese famine.** Dikötter has 5 (3 cannibalism cases, 1 rape case, 1 theft): 1 held and 4 pending in the run-3 patch. *Mubei* has 2 rows covering about 17 dated cases or groups (killings, beatings, cannibalism, suicides; Sichuan, Anhui, Guangdong, Jiangsu, Henan, 1960), plus 2 ranges with no days and 1 undated case (a lead). None is held as a case of its own; the organs' reports of them are.
- **Sources to re-read:** *Mubei* only, Drive `1Fb2pT-0OZvyMccyoGrIoXfRGiHIegqSW`, pp. I, 40–42, 62–64 (Jan. 6–8, 1960 only), 210–211, 223, 274–281, 288–291, 309–312, 392–395, 417–418, 422–423. Each dated case becomes an entry, with the report that gathers it in the note, as `notes/briefs/batch15b-prc.md` (the famine's crimes) directs. Dikötter needs no re-read, only the merge of `inbox/2026-11-19-b15c-dikotter-3.yaml`.
- **The US civil disorders:** no reader or audit in the window passed over a disorder event (a killing, a looting, sniper fire, an arson, an arrest or a trial) as a crime. No US source was read in the window, and no batch brief in the window sends out a source on the disorders. Within the window the crime rule cost the disorders nothing. Older coverage is not inventoried here, by the lead's narrowing.
- **Civil-rights crimes, organized crime, hijackings:** nothing in the window.
- **A caveat on the window:** one row older than ad55daa gives the ground in R18's later words. Branch, *At Canaan's Edge*, pp. 501 and 511 (Speck's murders, July 13, 1966; Whitman's shootings, Aug. 1, 1966): "out of the brief: a crime with no political or policy trace on the page." It was written in early November under the old wording ("no bearing on politics or policy"). It falls outside the window and was not searched for. It is named only so that the window's premise, that before ad55daa R18 named no crimes, is not taken to mean no reader used the ground.
