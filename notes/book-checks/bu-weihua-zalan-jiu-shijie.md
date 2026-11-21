# Bu Weihua 卜偉華, *"Zalan jiu shijie": Wenhua dageming de dongluan yu haojie (1966–1968)* 「砸爛舊世界」——文化大革命的動亂與浩劫(1966–1968) (card `w.pu-weihua-zalan-jiu-shijie`)

The file is named for the author as the brief asks; the card's id (and so the by-work file, `sources/witnesses/by-work/pu-weihua-zalan-jiu-shijie.yaml`, as `tools/bib/witnesses.py` requires) keeps Chen Jian's "Pu Weihua".

## Run 1 (reader b15b-buweihua-1, Nov. 21, 2026): ch. 1, pp. 1–40

Patch `inbox/2026-11-21-b15b-buweihua-1.yaml`; witness rows `inbox/witnesses/2026-11-21-b15b-buweihua-1.yaml`; edges `sources/witnesses/by-work/pu-weihua-zalan-jiu-shijie.yaml` (under `# run 1`). Nothing was merged or committed.

**The copy.** Drive `10ZsEXUG5R2dKp99qLL8OahE7B6Qm_Lqx`: a PDF of 849 pages made by Acrobat 9.4 in 2011. It is a scan with **no text layer**: bitonal JBIG2 page images of about 1,250 × 1,820 px, about 300 dpi at the book's size, in traditional characters. It was OCRed with tesseract `chi_tra` at `--psm 6` from the native images (`pdfimages -png`). Names, dates, figures and note numbers in doubt were read on line crops of the images, about 30 crops (for example 12月10日, 12月31日, 12月21日 at pp. 16–19; 馬以鑫, not "馬以春"; 鄧允健; 曲六乙; 余煥椿; 葛恒軍; 郝治平; 傅洋 and 《美洲文匯周刊》 no. 180; 1966年5月6日 at 14 n.28; 1965年11月 at 21 n.41; *Hongqi* 1965 no. 12, not 13, at 19 n.35). Everything was deleted at the end: the download, the images, the OCR text and the crops.

**The imprint and the card.** Title page (PDF 3) and copyright page (PDF 4): 中華人民共和國史‧第六卷; Research Centre for Contemporary Chinese Culture, the Chinese University of Hong Kong, 2008, distributed by the Chinese University Press; ISBN 978-988-17274-6-6. **No 內部發行** appears, so this is an open printing (R27). The card already existed. Its `script` was set from the title page to the full title with 「」 and (1966–1968), and its note was given the series and the imprint.

**Folio.** Printed page = PDF page − 20. Ch. 1 begins on PDF 21, printed p. 1. The front matter runs from the general preface (總序, PDF 5) through Wang Nianyi's preface (PDF 8–11) and the table of contents (PDF 12–20). The running heads confirmed the folio on every page read.

**Chapter map** (from the contents; the page numbers are OCR readings, to be confirmed in run 2):

| ch. | title | starts |
|---|---|---|
| 1 | 導火索 | 1 |
| 2 | (the enlarged Politburo of May 1966; the work groups) | c. 64 |
| 3 | (the Eleventh Plenum; the Red Guards; the Four Olds; the great exchanges) | c. 186 |
| 4 | (the bourgeois reactionary line; Anting; the Workers' HQ) | c. 271 |
| 5 | (the January storm; seizures of power; the February adverse current) | c. 357 |
| 6 | 大批判 | 467 |
| 7 | 天下大亂 | 525 |
| 8 | 理還亂 | 607 |
| 9 | 波瀾再起 | 653 |
| 10 | 全國一片紅 | 725 |

After ch. 10 come 後記, a 大事記 and 參考文獻 (about pp. 790 ff.).

**The notes.** Footnotes stand at the foot of each page and are numbered through each chapter: ch. 1 runs from n.1 on p. 1 to n.62 on p. 40. The anchor is the page and the note's number (`11 n.20`). Several items under one number are lettered in their order (`20 n.37a`, `n.37b`; `29 n.49a`, `n.49b`). Notes that only gloss, with no item, have no edge: 5 n.8, 15 n.30–31 (whose dated deaths were entered), 22 n.42, 26 n.44, 31 n.50 and 36 n.56. Pages cited that have no notes: 7, 10, 23, 24 and 30. `./bib notes-coverage` reads only the tree. It lists the pages that earlier readers put behind "To check:" in card form (310, 356, 449–450, 504–506), which run 1 did not read. A page-by-page comparison of this patch's pinpoints with the edges finds every cited page with a note registered, apart from the pages without notes and the glosses listed above.

**What was read.** Ch. 1 in full, pp. 1–40, with its notes, through the army literary forum of Feb. 1966 (the head of §4, "批文藝黑線"). Pp. 41 ff. were not read.

**What was entered.** 82 new entries: 36 with `place:`, 2 with a time (an afternoon and a night), 29 with `at:`. By year: 1961 5, 1962 1, 1963 1, 1964 11, 1965 40, 1966 22, 1968 1, 1969 1.

There are 71 cites. Units are claimed only where the page bears every place, hour, person, figure and claim in the unit. Elsewhere a parenthetical gives what the page bears.

Other ops:
- 6 variants: the Liao Mosha article printed Feb. 26, not Feb. 16, 1961; Li Xifan in June–July 1964; the *Beijing ribao* note dictated by Peng Zhen; Ye Qun at Hangzhou on Nov. 30 with eleven items; the notice on editing Mao's works dated Feb. 24; the work conference of Feb. 2, 1963.
- 20 `to-check` ops and 2 `src` ops.
- 4 `place` ops on cited entries: Peking ×3 and Beidaihe.
- 3 `edit` ops at the head. Each takes out of an entry's note the plain-text "To check:" item for this book, so that the `cite` can stand in its place: `cal.1964.china-leadership-14`, `cal.1966-03.china-leadership-5` and `cal.1966-04-24.china-leadership-5`, with the revs of this morning.

Witnesses:
- 27 witness rows. Existing rows were reused where one already held the record, for example Mao's comment of June 27, 1964, the Wu Xujun interview, Mao's comment of Dec. 2, 1965, the Mao–Snow talk and Li Xuefeng's essay.
- 62 edges.
- 4 new cards: `w.liu-shaoqi-zhuan` (the 1998 edition), `w.zhongguo-gongchandang-lishi-dashiji` (the 1991 edition of the Party chronology), `w.zhongguo-gongchandang-zhongda-shishi` (Tang Yingwu, ed., 2001) and `w.sanjiacun-chenyuan` (1992).

`./bib patch-check`: 0 errors. The warnings are of the same-day and possible-duplicate kind and the three edits' "sets only n". `./bib fields --patch`: 0 findings. Ledger: 82 claims under the patch, matching the adds; one claim was released (`cal.1963-11.china-leadership-5`, a duplicate of `-2`, now cited).

Threads and visibility: every add is in `china-leadership` with `polity:prc`. Internal acts carry `vis:only:prc`; Kang Sheng's talk with Hồ Chí Minh carries `vis:only:prc+drv`. The press items carry no tag: the *Wenhui bao*, *Beijing wanbao*, *Beijing wenyi*, *Renmin ribao* and *Jiefangjun bao* pieces, and Deng Zihui's release.

"Made public:" is 2008 where Bu names no earlier printing. Otherwise it is the earliest open printing his note names: 1984 (Zheng Qian in *Dangshi tongxun*), 1987 (Luo Diandian), 1992 (*"Sanjiacun" chenyuan*), 2000 (*Wang Shangrong jiangjun*), 2001 (the *Kaozheng* essays) and 2004 (Yu Huanchun). For the Lanzhou report of Nov. 18, 1965, it is the *Wengao* of 1996, noted as a printing for internal circulation. Two `form:state` entries ("As Bu Weihua reports it") give the forums and the press after Nov. 10, 1965, and the scholars' objections.

What run 1 covered:
- **The background, 1961–65.** Cites: the atomic test, Chen Yi's press conference, Li Weihan's dismissal, Mao on the Ministry of Culture, the comment of June 27, 1964, the Secretariat of March 1965, the work conference of Dec. 1964, the "independent kingdoms", the Seven Thousand Cadres Conference and Liu's speech of Feb. 1963. Adds: Deng Zihui (1965) and Wang Jiaxiang (Mar. 1966).
- ***Hai Rui*.** The play's printing, staging and the 1961 exchanges (Wu Han's reply of Feb. 28, the *Beijing wenyi* of March and Ma Lianliang of June 23 added); Jiang Qing in 1962; Lu Dingyi's and Liu Ren's accounts of 1964; Zhang Chunqiao's forums of Nov. 7 and Dec. 10, 1965; the *Wenhui bao* forum of Dec. 31; Ma Yixin's article; the reprints; Peng Zhen's and Luo Ruiqing's acts; Deng Tuo's article of Dec. 15; Mao's Hangzhou talks; Wu Han's self-criticism; Jiang Qing to Guan Feng and Qi Benyu (June 1966); Kang Sheng to Hồ Chí Minh (June 3, 1966).
- **Luo Ruiqing.** From the Guo Xingfu method (Dec. 1963) through the competitions, Ye Qun's reports, Lin's instruction and Luo's revisions, the five rules (May 2, 1965), May 25, Dalian, Suzhou, Lei Yingfu's and Li Zuopeng's material, Mao and Lon Nol (Nov. 26), the Shanghai meeting and its speeches (split one act an entry), the Military Commission of Dec. 15, the resignations, and the Jingxi Hotel meeting to Apr. 30, 1966.
- **"Giving prominence to politics."** The five principles; the political work conference; the *Jiefangjun bao* and *Renmin ribao* editorials of Feb.–May 1966; the provincial study papers of Jan.–Mar. 1966; the notice on editing Mao's works.

**Duplicates.** Every add was scripted against the day's entries in every thread, the month's and year's entries, the ledger and the pending patches (Ang, the conditions restore, Dikötter's *Cultural Revolution*, Chang), by date and by romanized name. Eight acts first drafted as adds proved to be in the tree and were made cites:
- Mao on the Ministry of Culture, `cal.1963-11.china-leadership-2`;
- the play's renaming, `cal.1960-11-13.china-leadership-3`;
- its printing and staging;
- Mao and Ma Lianliang, `cal.1961.china-leadership-16`;
- Liao Mosha's article;
- Jiang Qing in 1962, `cal.1962-07.china-leadership-11`;
- the notice on editing Mao's works, `cal.1966-02-21.china-leadership`;
- the forwarding of the Central-South papers. This one is cited on `cal.1966-02-05.china-leadership-4`, which bundles it, and the forwarding of Feb. 13 is also its own add.

## Passed over (run 1; R44, R18's grounds only)

Made by reading every dated act on pp. 1–40 against the tree and the patch.

| page | date | event | why |
|---|---|---|---|
| 8 | Apr. 2–5, 1959 | the Shanghai plenum; Mao urges learning from Hai Rui | outside the span |
| 8 | June 16, 1959; from Sept. 17, 1959 | Wu Han's "Hai Rui scolds the emperor" and five more articles | outside the span |
| 8 | 1959, second half | Ma Lianliang asks Wu Han for a Hai Rui play | outside the span |
| 8 n.14 | Dec. 1958; Apr. 1959 | the plans' steel and coal targets cut | outside the span |
| 4 n.6–7 | Aug. 18, 1980; Mar. 20, 1943 | Deng's speech on the leadership system; the 1943 decision | outside the span |
| 10 | 1954 | Li Xifan against Yu Pingbo | outside the span |
| 13 n.26 | Dec. 18, 1970 | Mao to Snow | outside the span (registered) |
| 20 n.37 | Jan. 24, 1980 | Guan Feng's confession | outside the span (registered) |
| 21 n.41 | Oct. 1980 | Yang Shangkun rehabilitated | outside the span |
| 22 | 1930s–40s | Lin Biao and Luo Ruiqing in the Red Army and at Yan'an | outside the span |
| 40 | Dec. 21, 1973 | Mao's self-criticism over Luo Ruiqing | outside the span |

## Leads and not yet entered (run 1)

- Leads, undated (R50):
  - 6: Mao to his head nurse Wu Xujun (the interview of Jan. 18, 2002, registered).
  - 13 n.25: Wang Li's account of Mao proposing the criticism of Wu Han at an enlarged Standing Committee with the regional first secretaries.
  - 21: Wu Han's complaint that Hu Qiaomu set him the subject, and his words to a student (n.39–40, registered).
  - 22: Lin Biao's telephone message to Luo of 1962–63 and his note, "praise others, follow others".
  - 26: Zhang Xiuchuan the first to send Lin material against Luo.
  - 34: the General Office's later forwarding of the Hunan, Shanghai, East China, North China and Zhejiang papers on studying Mao's works.
- Loosely dated, to be entered in run 2 (not reached in this run's pass):
  - 6: Mao's remarks to foreign guests in 1963 and 1964 on revisionists in China and "three peaces and one less".
  - 18: Mao's "needles cannot get in, water cannot splash in" of the Peking committee (Nov. 1965).
  - 38 n.59: Peng Zhen in charge of Luo's case at the end of 1965, and his anger at the investigators (Fu Yang, registered).

## Doubts (run 1)

- **Bu's own errors.**
  - 18 and 26 call Lon Nol "the Cambodian premier" (首相). The entry of Nov. 26 says "Lon Nol of Cambodia".
  - 2 n.3 dates Liu's speech to a work conference of Feb. 2, 1963. The tree has the conference Feb. 11–28; this is a variant.
  - 19 has Deng Tuo's "Xiang Yangsheng" article in the *Renmin ribao* of Dec. 15. The tree has it in the *Beijing ribao* of Dec. 12 (`cal.1965-12.china-leadership-5`). Both now stand as two printings; whether the *Renmin ribao* reprinted it is to be checked.
- **Cites resting on Bu's month alone or on uncertain matches.**
  - `cal.1964-12-27.china-leadership`: Bu gives only "Dec. 1964" for the "independent kingdoms".
  - `cal.1965-03-02.china-leadership-5`: "March 1965" only.
  - `cal.1966-04-12.china-leadership`: the tree's letter of that day is on the Secretariat and the Northwest trip. Bu quotes a letter on Luo's report. It may be the same letter or another.
  - `cal.1964-06.china-leadership-8`: Ye Qun sent to the troops, in June in the tree. Bu places the 379th Regiment inquiry after the meetings of August–September, and it was added as "1964, fall"; the two may be one act.
- **Registry.**
  - The Tiandi reader's row `x.2008.bu-weihua-zalan-jiu-shijie-2008` is this card. It should give way to the card at the merge.
  - Mao's comment of June 27, 1964 has two rows (origins3-7 and maozhuan-2); run 1 used the first.
  - `w.liu-shaoqi-zhuan` (1998) and `w.jin-chongji-liu-shaoqi-zhuan` (2008) are two editions to be joined (`edition_of`).
- **The three edits.** They set `n` on entries that other pending patches may also touch. `merge --auto` joins the notes or flags a conflict on `n`.
- **"Made public: 2008".** It stands on acts Bu tells without a note (Lin's words on Luo, the Shanghai meeting's speeches, Mao's remark to Lin). Earlier printings, such as the Luo family's memoirs and Chen Pixian's, may hold some of them.

## Persons named in `c` with no name entry (not tagged)

- *Hai Rui* and the writers, critics and scholars: Deng Zihui, Wang Jiaxiang, Wu Han, Liao Mosha, Qu Liuyi, Deng Yunjian, Ma Lianliang, Zhou Gucheng, Zhou Yutong, Li Pingxin, Ma Yixin, Yang Yongzhi, Qi Sihe, Zhang Zhilian, Zang Kejia, Shang Yue, Weng Dujian, Jian Bozan, Deng Tuo, Liu Ren, Tian Han, Chen Xianghe, Bu Weihua.
- The Cultural Revolution Group circle and the press: Guan Feng, Qi Benyu, Tang Pingzhu, Yang Shangkun, Xi Zhongxun.
- The army and the Luo case: Guo Xingfu, Lin Doudou, Lei Yingfu, Wang Hongkun, Zhang Xiuchuan, Xiao Jinguang, Su Zhenhua, Liu Yalou, Wang Shangrong, Yang Yong, Xiao Hua, Luo Ronghuan, Wang Zhongfang.

## Where run 2 starts

P. 41: ch. 1, §4 "批文藝黑線", the army forum's course after Feb. 2, 1966; then §5, the February Outline (pp. 52 ff.); then ch. 2. Run 2 should also hold up the earlier readers' "To check:" items for this book on the pages it reaches. In plain text: pp. 48–49, 62, 68, 165–166, 191–194, 206, 449–460, 533 and 540, and "51" on `cal.1967-05-13.china-leadership-5`, which looks like a misprint. In card form: pp. 310, 356, 449–450 and 504–506. Each is to be cited where the page bears it, with an `edit` taking out a plain-text item as run 1 did. The entries are listed by a script over `lists/cal/` for "卜偉華" and `pu-weihua-zalan`.

## Counts (run 1)

| | |
|---|---|
| new entries | 82 (36 with place, 2 with time, 29 with `at`) |
| cites | 71 |
| variants | 6 |
| `check` ops | 0 (3 "Check:" sentences in adds) |
| `to-check` ops | 20 |
| `src` ops | 2 |
| `place` ops | 4 |
| `edit` ops | 3 |
| witness rows | 27 |
| edges | 62 |
| cards | 4 new, 1 amended |

## Audit of run 1, Nov. 21

Opus audit of patch `2026-11-21-b15b-buweihua-1` (ch. 1, pp. 1–40; as handed in: 82 adds, 71 cites, 6 variants, 20 to-check, 2 src, 4 place, 3 edits), its witness file (27 rows), its 62 edges under `# run 1`, the four new cards and the amended card, against the reader's brief, the owner's rulings of Nov. 21, R5, R7, R8, R15, R18, R25a, R27 and R35–R43. The copy fetched afresh into a new directory (849 PDF pages, a scan with no text layer; printed = PDF − 20, confirmed by the folios); PDF 21–60 and the title and copyright pages rendered at 300 dpi and OCRed with tesseract `chi_tra` (`--psm 6`); every page read whole in the OCR against the patch's items, and about 45 lines in doubt (dates, names, note numbers, titles) read on crops of the image. All 82 adds and all 71 cites read against their pages; every add scripted against the tree (Tiandi runs 1–5, MacFarquhar and Schoenhals, the Mao, Zhou, Peng Zhen and Chen Yi chronologies, Teiwes and Sun, Chen Jian, the conditions restore as merged) and the pending inbox (Dikötter's *Cultural Revolution* run 1, then merged, run 2, Chang, Zhu De, and Bu run 2, begun during the audit), by day, month and year, name tags, Latin names and runs of characters, and the candidates read. Originals backed up first (scratch `audit-bu1-bak/`: the patch, the witness file, the by-work file, this file, the patch's 82 ledger lines, `works/z.yaml`). Nothing merged or committed; the download, its images, its text and the crops deleted at the end.

**Verdict.** A careful and mostly faithful reading: dates, persons, figures and quotations hold against the page, the closed acts carry `vis:` and "Made public:", the cites say what the page gives, and the reader's registry reuse was good. The faults are of class: characters missing at first appearance (the largest); some adds the calendar already held, or that bundled two acts; one date misread (Feb. 25, 1963 read as Feb. 2) and one misdated add (Ye Qun's dispatch, "fall" for late November 1964); `form:state` on the author's own account; a few visibility and "Made public" slips; two registry rows that repeat rows already registered; and a few events on pages read and passed over. All fixed in place. patch-check 0 errors, `fields --patch` 0 findings, `check` 0 errors after each change to `works/` and the witness file.

**Counts.** Before: 82 adds (36 with `place`, 2 with a time, 29 with `at`), 71 cites, 6 variants, 20 to-check, 2 src, 4 place, 3 edits, no `check` op. After: 83 adds (35 with `place`, 2 with a time, 31 with `at`; 69 with a `vis:` ruling; none `form:state`; by year 1961 5, 1962 2, 1963 1, 1964 12, 1965 38, 1966 23, 1968 1, 1969 1), 80 cites, 8 variants, 22 to-check, 2 check, 2 src, 4 place, 5 edits (the reader's 3; one *Estimates* gloss; one striking a card-form To check this run now reads). Witness file: 27 rows (two of them absorbed into rows already registered) and 4 amendment rows; 62 edges, 3 repointed. Cards: 4 new as made; the 1991 Party chronology given `edition_of`. Ledger: 6 claims released (`cal.1965-01.china-leadership-14`, `cal.1965-12.china-leadership-13`, `cal.1965-12.china-leadership-19`, `cal.1965-11-27.china-leadership-10`, `cal.1964.china-leadership-44`, `cal.1966-01.china-leadership-10`), 7 made (`cal.1964.china-leadership-46`, `cal.1964-11.china-leadership-8`, `cal.1965-12.china-leadership-22`, `cal.1966-01-16.china-leadership-4`, `cal.1962.china-leadership-62`, `cal.1965.china-leadership-31`, `cal.1966.china-leadership-56`); 83 claims under the patch, matching the adds.

**Faults and fixes, by class (rates of the 82 adds as handed in, or of the 71 cites).**
- *Characters at first appearance* (40 adds, 49 percent): organs, units, meetings, documents and titles named in Latin alone, among them the Military Commission 中央军委 (7), the General Political Department 总政治部 and its work group 总政工作组, the Shanghai meeting 上海会议, the city committees 上海市委 and 北京市委, the Central-South Bureau 中南局, the General Staff's operations department 总参作战部, the 379th Regiment 第一二七师三七九团, the 100th Regiment 南京军区第12军100团, the Peking Federation of Literary and Art Circles 北京市文联, People's University 中国人民大学, the Institute of Nationalities 民族研究所, the decisions and notices of Jan. 6, 13 and 16, 1966, "Long live the victory of people's war" 《人民战争胜利万岁》, Ma Yixin's 〈也谈《海瑞罢官》〉, Deng Tuo's 〈从《海瑞罢官》谈道德继承论〉, the Seven Thousand Cadres Conference 七千人大会, "thrice angering Zhou Yu" 三气周瑜, Chen Xianghe's two stories. All added from the page, in the simplified forms the calendar uses; the characters already in `c` (persons and places) checked against the page and the tree's forms: right.
- *Already in the calendar* (4 adds, 4.9 percent), dropped, their claims released, made cites: Luo Ruiqing's revision of Lin Biao's instruction (24) is `cal.1965-01.china-leadership-4` (MacFarquhar), cited for A; Ye Qun's "chief proof," Liu Yalou's four points (29), and Wu Faxian's speech of 10,000 characters (29) are the speeches of the Shanghai meeting that `cal.1965-12-08.china-leadership` holds (units B, C), folded into its cite; Li Zuopeng's material of Nov. 27 (26) is the Li Zuopeng half of `cal.1965-12.china-leadership-4` (MacFarquhar, undated, "Check: the month"), now a cite with a variant giving Bu's day. Partly in, and trimmed: Zhou and Deng passing on Mao's words to Luo during the meeting (36) is the tree's talk of Dec. 11 (Jian), now a second cite there, the add left to Mao's words to Lin; Jian Bozan's objection (17) is the *Guangming ribao* digest's (`cal.1965-11.china-leadership-17`), now cited there and out of the scholars' add.
- *One act an entry* (7 adds, 8.5 percent): the Nanjing meeting of January 1964 and Luo's later proposal of the army-wide competition (split: `cal.1964.china-leadership-46`, "1964, before June"); the approval of Luo's resignations and the setting up of the Central work small group (split: `cal.1965-12.china-leadership-22`, with a Check on the month); Wang Shangrong's and Yang Yong's remarks (Yang's undated in the note: a lead); Shanghai's decision of Jan. 6 and the committee's rule of an hour's study a day (undated in the text: a lead; `ok:fields-time` gone); Gansu's decision and the General Office's later forwarding (a lead); Lin's illness of August 1965 and Luo's written reports after the refusal of September (moved to the September add); the forwarding of Feb. 13 and the Central-South Bureau's decision of Jan. 16, which had no entry while Shanghai's and Peking's had (the decision now its own add, `cal.1966-01-16.china-leadership-4`).
- *Dates and fields* (5 adds, 6.1 percent): Ye Qun's dispatch to the 379th Regiment is printed 11月下旬, late November 1964 (read on the image), not "fall": her four reports re-dated (`cal.1964-11.china-leadership-8`, `at: before 1964-11-21`), and the dispatch itself is the tree's `cal.1964-06.china-leadership-8` (MacFarquhar's June): a cite and a variant on B. Mao's approval of Xiao Hua's report is undated in the text: "1966, after Jan. 18" (`cal.1966.china-leadership-56`), not January. Lei Yingfu's letter `at: after 1965-09-03` (it was set before Sept. 21); Luo's telephone call to Peng after Mao's reception of Lon Nol of the 26th, not the 25th; the forums of November 1965 placed at Peking. Every other date, clock word, band and place right.
- *`form:state` and the author's account* (2 adds): the forums after Yao's article and the scholars' objections were "As Bu Weihua reports it" (one tagged `form:state`): Bu is no source of the time (the restore audit's rule). Both restated as acts; the author's judgment that most intellectuals kept quiet out.
- *Visibility and "Made public"* (6 adds, 7.3 percent): the forums and the papers' columns are public (`vis:` out); the scholars' objections, closed, now "Made public: 1992 ([[w.sanjiacun-chenyuan]])", the earliest printing the note names; Mao's reception of Lon Nol was public, its private exchanges not: `vis:only:prc@C-F`; the Shanghai and Peking decisions of Jan. 6 and 13 had no "Made public" (2008 added); Lin's forwarding of the Lanzhou report claimed "Made public: 1996" from the *Wengao*, an internal printing (R27): now "Made public: 2008. Printed for internal circulation: [[w.zedong-jianguo-yilai-mao-zedong]], XI, 487–488 (1996)." A Check added on the *Wenhui bao* forum of Dec. 31: whether *Dangshi tongxun* (1984) was printed for internal circulation.
- *Checks* (1 add): Nov. 7, 1965, "Check: the day" was a working note (the day is Zhang Chunqiao's "three days before," as the note gives it): struck, the basis in the cite's parenthetical.
- *Names and tags* (2 adds): Luo Ronghuan, held, untagged and out of "Names:" (`cal.1961.china-leadership-81`); Yao Wenyuan untagged on the forums. Fixed. No tag for a person not held.
- *Text* (3 adds): Lin's instruction of May 25, 1965 has the correction of bulletin no. 63 read out in the groups, not the bulletin withdrawn; the Center widens the Jingxi Hotel meeting to the ministries and commissions of the Center and the State Council, the regional bureaus and some regions, services and academies; the 1964 articles against Wu Han are "Peking's," not "the Peking committee's writers'."
- *Passed over on pages read* (R5; R15: a year or season is a date): Lin's telephone message to Luo, 1962, fall (22; `cal.1962.china-leadership-62`); Peng Zhen in charge of Luo's case at the end of 1965, stopping the investigators (38 n.59; `cal.1965.china-leadership-31`; the reader had it as "not reached"); the Central-South decision (above); Bu's totals for the economy of 1965 against 1957 (1, after Wu Li), an *Estimates* gloss on the Central Work Conference of Sept. 18, 1965 (an `edit`, gloss only). Cites the pages bear and the patch lacked: the Peking display of June 15, 1964 (`cal.1964-06-15.china-leadership-2`); Lin and Ye Qun's gathering of material by the autumn of 1965 (`cal.1965.china-leadership`); the Center's forwarding of mid-February on `cal.1966-02-05.china-leadership-4` (the reader's book-check says it was cited; it was not); the Secretariat's instruction to the Peking papers on `cal.1965-11-28.china-leadership-7`. To check added: Li Xuefeng's memoir on `cal.1965-12-08.china-leadership` (with a variant: Li has the meeting presided over by Lin, Mao absent; Bu holds that Mao presided, at the Standing Committee's sessions); Liu Zhijian (1989) and Ge Hengjun (2001) on the army forum of February 1966. A Check on `cal.1965-09-23.china-leadership`: Bu (20 n.37) doubts Mao said "perhaps the truth is on your side."
- *Cites* (2 of 71, 2.8 percent): `cal.1966-05-16.china-leadership-2` cited bare at 39 n.60, which gives only the forwarding's title and day: parenthetical added; and the work conference (below). The rest right for act, day and units; the units claimed only where the page bears the whole unit.

**Rulings on the reader's doubts.**
- *Lon Nol "premier" (18, 26)*: Bu's slip (首相); the add names him "Lon Nol 朗诺 of Cambodia," his office out of `c`: right, no variant.
- *The work conference "Feb. 2, 1963" (2 n.3)*: a misreading; the image prints 1963年2月25日, inside the conference of Feb. 11–28. The variant dropped; the cite moved to the dated entry `cal.1963-02-25.china-leadership` (Liu's report on revisionism, Mao interjecting; the Mao zhuan, which Bu's note cites, has the same), with its to-check; a Check on `cal.1963-02.china-leadership-4` (Mao's interjection, undated) that Bu dates it Feb. 25: the two tree entries may be one act, for the owner.
- *Deng Tuo's article (19)*: read on the image, the *Renmin ribao* of Dec. 15 (12月15日,《人民日報》). Kept as a second printing beside the *Beijing ribao* of Dec. 12, with a Check: Bu names no other printing, the tree no *Renmin ribao* one.
- *Four uncertain matches*: `cal.1966-04-12.china-leadership`: one letter (the same day, the same three signers, Zhou, Deng and Peng; Mao's reply of Apr. 14 acknowledges "your letter of the 12th and its papers"): right. `cal.1964-12-27.china-leadership`: Mao's two "independent kingdoms" in Peking, December 1964 in Bu, the tree's Dec. 27 remark: right, no units, the parenthetical stands. `cal.1965-03-02.china-leadership-5`: the Secretariat of March 1965 under Liu, Deng's remarks: units A–D borne by the page: right. Ye Qun and the 379th Regiment: one dispatch, late November 1964 in Bu (above).
- *The registry*: the Tiandi row `x.2008.bu-weihua-zalan-jiu-shijie-2008` is this card; its 26 edges are in `sources/witnesses/by-work/yang-jisheng-tiandi-fanfu.yaml`, not this run's: for the merger (below). Mao's comment of June 27, 1964: the two rows joined (`absorbs`, the maozhuan-2 row into the origins3-7 row). The Liu Shaoqi biographies: `w.liu-shaoqi-zhuan` (1998, this run's) and `w.jin-chongji-liu-shaoqi-zhuan` (2008, Chen Jian's card): `edition_of` belongs on the 2008 card, not this run's; and Dikötter's row `x.1998.jin-huang-liu-shaoqi-zhuan` (not held) is the 1998 card. Both for the merger. Two of the run's own rows repeated rows already registered: Jiang Qing's speech of Apr. 12, 1967 (= `x.1967-04-12.jiang-qing-speech-enlarged-mac-sentry`, origins3-9) and the Lanzhou Military Region's report on the 55th Division (= `x.1965-11-07.lanzhou-mr-party-committee-report-55th-division-nov-7`, wengao-18, dated by the report, Nov. 7): both absorbed by amendment rows, the edges (11 n.17, 13 n.24, 27 n.45) and the add's `via` repointed. Li Xuefeng's row given the year and volume Bu's note prints (2003, II, 595). The other rows checked against the registry and every pending witness file by date, record and characters: none registered twice.
- *The three edits that set only `n`*: each strikes the plain-text To check for this book that the run's cite replaces, so not additive; bases current at the end of the audit. A fourth of the kind added, striking `[[w.pu-weihua-zalan-jiu-shijie]], 28 (cited by [[w.jian-zhou-enlai]], 531 n.58)` from `cal.1965-12-08.china-leadership`'s To check.
- *"Made public: 2008"*: right under R27 wherever Bu's note names no earlier printing, as on Lin's words of 1965, the Shanghai meeting's speeches and Mao's remark to Lin; an earlier printing not cited for the act (the Luo family's memoir, Chen Pixian's) does not move it. The exceptions are fixed above.

**Witnesses and edges.** The 27 rows read against their notes: what, kind, form, agent, date and `open` right but for the two repeats; "no source named" rows only where the note names a statement or a record (Lu Dingyi's of May 1966, Liu Ren's, Zhang Chunqiao's of May 6 and Dec. 23, 1966, Kang Sheng's to Hồ Chí Minh, Luo's letter), none for an event told without a source (R38). The 62 edges tested by script for page and note against the notes as read (the lettered notes 5 n.11, 11 n.19, 11 n.20, 20 n.37, 29 n.49, 39 n.61 included); all right; the uncited glosses (5 n.8, 15 n.30–31, 22 n.42, 26 n.44, 31 n.50, 36 n.56) rightly without edges.

**Cards.** The four new cards against Bu's notes (5 n.10, 5 n.11, 9 n.16, 15 n.29, the last read on the image: 張占斌、孫建軍): right. `w.zhongguo-gongchandang-lishi-dashiji` (1991) now `edition_of: w.zhongguo-gongchan-dang-lishi` (1989), as its note says. The amended card `w.pu-weihua-zalan-jiu-shijie`: right (title page and copyright page; no 內部發行).

**Leads (added).** Yang Yong's like words on Luo (29 n.49b, undated); the Shanghai committee's rule of an hour's study a day and four on Saturday (34, undated); the General Office's later forwarding of the Gansu, Hunan, Shanghai, East China, North China and Zhejiang papers (34, undated); the *Jiefangjun bao*'s second to sixth editorials (32, between Feb. 3 and Apr. 5, 1966, not dated singly); the criticisms of Sun Yefang, Yang Xianzhen, Feng Ding, Jian Bozan and Luo Ergang (4, undated).

**For the merger.** (1) Keep (`--take keep`) the duplicate flags patch-check raises on all 83 adds (same day, month or year, read and distinct). (2) Repoint the 26 edges of `x.2008.bu-weihua-zalan-jiu-shijie-2008` in `sources/witnesses/by-work/yang-jisheng-tiandi-fanfu.yaml` to `w.pu-weihua-zalan-jiu-shijie` (their pins as they stand) and retire the row; likewise the edges of `x.1998.jin-huang-liu-shaoqi-zhuan` (Dikötter's *Great Famine* 119 n.17e, 120 n.18; *Cultural Revolution* 21 n.20) to `w.liu-shaoqi-zhuan`; set `edition_of: w.liu-shaoqi-zhuan` on `w.jin-chongji-liu-shaoqi-zhuan`. (3) No Check to strike by hand: the To check items this run reads are struck by its four edits that set `n`. (4) Merge after Dikötter's *Cultural Revolution* run 1 (merged during the audit) and before Bu run 2, which may cite this run's adds.

## Run 2 (reader b15b-buweihua-2, Nov. 21, 2026): ch. 1 §§4–5 and ch. 2 to the provincial purges, pp. 41–99

Patch `inbox/2026-11-21-b15b-buweihua-2.yaml`; witness rows `inbox/witnesses/2026-11-21-b15b-buweihua-2.yaml`; edges `sources/witnesses/by-work/pu-weihua-zalan-jiu-shijie.yaml` under `# run 2`. Nothing merged or committed. Run 1 (with its audit, read before this run's adds were checked) was merged while this run worked; every add was scripted against the tree as merged and against the pending inbox (Chang 2, Dikötter's *Cultural Revolution* 2, Ye Jianying 1, Zhu De 2), by day, month and year, Latin names and runs of characters, and the candidates read. The audit of run 1 was applied to this run before hand-in: characters at first appearance for organs, units, meetings, documents and titles in `c`; no `form:state` on Bu's own account; "Made public" from the earliest printing a note names.

**The copy and its keying.** The same Drive PDF as run 1 (849 pages; a scan with no text layer). It was fetched afresh into a new directory. PDF 60–200 and the contents (PDF 12–20) were extracted with `pdfimages -png` and OCRed with tesseract `chi_tra --psm 6` (four at once). The folio held on every page read: printed = PDF − 20. Every date, figure, name and note number an entry rests on was read on crops of the page image (about 60 lines and note strips, stacked in a few dozen images). The download, its images, its OCR text and the crops were deleted at the end.

**The chapter map, confirmed for ch. 2.** Ch. 2 「發動」 begins at p. 73 (PDF 93); its §1 the enlarged Politburo of May 1966 (pp. 74–93), §2 「會外的情況」 from p. 93, its part 1 「運動初期各地整了哪些人」 from p. 97. The notes restart with each chapter: ch. 1 runs to n.91 at p. 72; ch. 2 starts at n.1 on p. 74 and reaches n.28 at p. 98.

**What was read.** Ch. 1 §4 from p. 41 (the army forum's course, the summary's drafts, Mao's revisions, its issue, recall and reissue, the all-army creative conference), §5 「批《二月提綱》」 (pp. 52–72: the Five-Man Group, the Outline and its fate, the Hangzhou meetings of March and April); ch. 2 to p. 99 (the enlarged Politburo of May 4–26, the May 16 Notice, Lin Biao's speech, the self-criticisms and decisions, the Peking committee's reorganization, Jiangsu, and the first provincial purges: Jilin, Shanghai, Tianjin, Liaoning, Tibet, Xinjiang, Hebei, Henan, and Jilin's plenum of June 14–26). All notes of the pages read were read (ch. 1 n.63–91; ch. 2 n.1–28).

**What was entered.**
- 88 new entries: 35 with `place`, 3 with a time (the Xingtai earthquake at 5:29 a.m.; Xinhua's evening notice of Apr. 16; Xiao Hua's afternoon of May 7), 32 with `at`. By year: 1963 1, 1964 3, 1965 3, 1966 78, 1967 3.
  - 3 are `form:state`, each a document-based count Bu cites: Jiangsu after the Wutaishan rally (Jiang Weiqing), Jilin to the end of August (the Jilin committee's chronicle) and Henan by early October (the Henan party chronicle).
  - 1 is in `china`: the Xingtai earthquake of Mar. 8, 1966, with a new gazetteer key, `xingtai`.
- 107 cites, 69 of them with units, every unit claimed only where the page bears every place, person, figure and claim in it.
- 7 variants:
  - the *Guangming ribao*, not the *Renmin ribao*, for the article of July 17, 1964;
  - of the standing members only Mao, Liu, Zhou and Lin at Hangzhou in March 1966;
  - Kang Sheng's "Feb. 7 to 10" for the Wuhan talks;
  - Qi Benyu's article alone on Apr. 2, 1966;
  - Lu Dingyi's self-criticism at the session of May 19, afternoon;
  - Gao Ju's and He Ming's articles of May 8;
  - the Center's decision on Li Xuefeng of May 8.
- 26 `to-check` ops and 12 `src` ops.
- 2 `place` ops (Shanghai on the mid-March revision and on Zhou's rewriting of the comment) and 1 `place-key` (`xingtai`).
- 16 `edit` ops at the head:
  - Six strike the plain-text "To check:" item for this book that the cite replaces: `cal.1966-02-02.china-leadership`, `cal.1966-03-11.china-leadership-3` (with its evening), `cal.1966-03-19.china-leadership-2`, `cal.1966-04-02.china-leadership`, `cal.1966-04-10.china-leadership` and `cal.1966-04-16.china-leadership-8`.
  - The other ten set the time of day the page gives on cited entries: Feb. 20, Mar. 11 (night), Mar. 30, May 5, 7, 16, 17, 18, 19 and 26, 1966.
- Witnesses:
  - 12 witness rows; existing rows reused where the record was registered: Jiang Qing's letter of Mar. 19 and Lin Biao's of Mar. 22, 1966; Liu Zhijian's article of 1989; Gong Yuzhi's and Li Xuefeng's essays in *Huishou "wenge"*; Zhou Enlai's speech of May 21 and Chen Boda's of May 24, 1966; Mao's talk with Shehu of May 5; the *Renmin ribao* printing of the Notice, May 17, 1967.
  - 56 edges under `# run 2`.
- 7 new cards:
  - `w.fengyu-zhengcheng` (Liu Zhijian, 1996);
  - `w.yi-zhou-yang` (Wang Meng and Yuan Ying, eds., 1998);
  - `w.liu-ren-zhuan` (2000);
  - `w.liu-shaoqi-yanjiu` (Huang Zheng, 2002);
  - `w.women-dou-jingliguo-de` (Ji Xianlin, ed., 2001);
  - `w.zhonggong-jilin-sheng-dang` (1990, internal);
  - `w.zhonggong-henan-dangshi-dashiji` (1986). Each takes its `script` from Bu's note.
- The ledger holds 88 claims under the patch, matching the adds. Three claims were released, two drafted adds that proved to be in the tree and one folded into a cite: `cal.1966-02-12.china-leadership-10`, `cal.1966-03.china-leadership-15` (later reclaimed for Wu Lengxi and Zhou), `cal.1966-01.china-leadership-14`.

**Visibility and "Made public."** Internal acts carry `vis:only:prc`. Public ones carry none: the press items, the Xingtai earthquake, Jiang Weiqing's rally and the *Hongqi* and Xinhua items.

"Made public:" is 2008 where Bu names no earlier printing. Otherwise it is the earliest printing his note names:
- 1982, Wang Nianyi;
- 1986, the Henan chronicle;
- 1989, Liu Zhijian in *Zhonggong dangshi ziliao* no. 30;
- 1996, Liu Zhijian's *Fengyu zhengcheng* and Jiang Weiqing's memoir;
- 1998, *Yi Zhou Yang*;
- 2000, *Liu Ren zhuan*;
- 2001, the *Kaozheng* essay;
- 2002, Huang Zheng;
- 2003, *Huishou "wenge"*, the year Bu's note prints (92 n.21).

Some printings were for internal circulation, and these are noted beside the date: the Jilin chronicle (1990) and the *"Wenhua dageming" yanjiu ziliao* (1988).

**Duplicates.** About half of Bu's acts for Feb.–May 1966 were in the tree, and every one of those was made a cite. This run's adds are the acts the tree lacked:
- the summary's drafts (Feb. 20, 26–28; Mar. 1, Mar. 14, after the 17th, the 31st), Apr. 3–4 and Apr. 16–30, the recall and reissue (May 2 and after);
- Xiao Hua's and Yang Chengwu's instructions;
- the all-army creative conference and the May 16 bulletin;
- the Five-Man Group's founding session of July 2, 1964;
- Xu Liqun's forum of Jan. 17 and letter of Jan. 31, 1966;
- the academic criticism office's answers;
- Wang Li's one-line notice;
- Liu Ren's plenum;
- Peng Zhen's suspension;
- the enlarged Politburo's reading and group days;
- the provincial purges.

Two first drafted as adds proved to be in and were made cites: Peng Zhen's notice to Shanghai on Feb. 12 (`cal.1966-02-12.china-leadership-6`), and Zhang Chunqiao's answer to Peng's call (unit B of `cal.1966-03-11.china-leadership-3`).

## Passed over (run 2; R44, R18's grounds only)

Made by reading every dated act on pp. 41–99 against the tree and the patch.

| page | date | event | why |
|---|---|---|---|
| 71 | 1973 | Liu Ren's death in Qincheng prison | outside the span |
| 94 n.24 | June 30, 1978 | the Peking committee's rehabilitation of the Public Security Bureau's "spy group" | outside the span |
| 52 n.72 | 1991, 1996 | the Party histories' judgment that the summary marks Lin Biao's and Jiang Qing's collusion | not an event (historiography); its works registered |

## Leads (run 2; undated, R50)

- 54: the criticisms of Sun Yefang and Feng Ding, tied to Kang Sheng.
- 55: Zhou Yang's talk with the writers of the Fang Qiu article (Gong Yuzhi, Lin Ganquan, Xing Bisi, Dai Yi) on Tian Han and Meng Chao.
- 55: the Fang Qiu article "Cannot evade the crux" on Wu Han's self-criticism (January 1966, not dated).
- 62: Mao's answer to Jiang Qing's complaint, "a little finger", and his word to Kang to tell Jiang and Zhang not to worry (as Lin Mohan recalled Kang's report; cited on `cal.1966-05-05.china-leadership-3`).
- 65 n.86: Peng Zhen's examination, for the Center, of whether Lu Dingyi knew of his wife's letters.
- 83 n.8: Mao in 1964 on a revisionist Center, the provinces able to rebel.
- 83: Mao's guard Chen Changjiang's recollection of a night of alarm.

## Doubts (run 2)

- **Xie Tangzhong 謝鏜忠.** He is the culture department's head at the army forum. Run 1's cite on `cal.1966-02-02.china-leadership` (now in the tree) names him "Xie Tiezhong": 鏜 is *tang*. That should be corrected.
- **The year of *Huishou "wenge"*.** The card says 2000. Bu's notes print 2003 (92 n.21), and the Tiandi reader's row has 2007. This run used 2003.
- **The Check on `cal.1966-04-16.china-leadership-8`**, "whether the rewritten note replaced the one issued Apr. 10". Bu (48) answers it: the recall of May 2 and the reissue under the old number and date. patch-check refuses an `edit` that drops a Check, so it stands for the owner or the merger.
- **Mao's first revision of the summary**, "Mar., before the 14th". It is dated by Bu's order of events. The Mao chronology has 三月上旬.
- **Zhou Yang's talk with Mao** is dated 1963 by "soon after" in Gong Yuzhi's account (a Check on the entry).
- **The North China Bureau's work conference of May 1966** (81). This run cites it on the tree's Qianmen Hotel meeting of May 21 (`cal.1966-05-21.china-leadership-4`) and dates the Tianjin group's attack on Hu Zhaoheng "May". p. 102 (「前門飯店會議」) is the test for run 3.
- ***Zhonggong dangshi ziliao* no. 30 (1989)**: whether it was printed for internal circulation. Three adds rest their "Made public: 1989" on it.
- **Cites resting on accounts.** Several cites rest on Kang Sheng's (May 5–6) or Zhang Chunqiao's (May 6) account to the enlarged Politburo, and each parenthetical says so.

## Persons named in `c` with no name entry (run 2; not tagged)

- *The army forum and the GPD*: Xiao Hua, Yang Chengwu, Liu Zhijian, Li Manchun, Xie Tangzhong, Chen Yading, Chen Qitong, Suo Yunping, Feng Yifu.
- *The Propaganda Department, the Five-Man Group and the press*: Zhou Yang, Wu Lengxi, Lin Mohan, Xu Liqun, Hu Sheng, Lin Jianqing, Wang Ruoshui, Gong Yuzhi, Qi Benyu, Guan Feng, Wang Li, Yang Xianzhen.
- *The Peking committee and police*: Liu Ren, Zheng Tianxiang, Wan Li, Deng Tuo, Li Jian, Feng Jiping, Xing Xiangsheng, Li Xuefeng.
- *Others*: Yang Shangkun, Yan Weibing, Cao Diqiu, Miyamoto Kenji.
- *The provinces*:
  - Jiangsu: Jiang Weiqing, Wei Wenbo, Wu Tianshi;
  - Shanghai: Zhou Gucheng, Li Pingxin, Zhou Yutong, Qu Baiyin, He Luting, Zhou Xinfang, Li Junmin, Xia Zhengnong;
  - Tianjin: Hu Zhaoheng, Ma Ruihua;
  - Liaoning: Xu Juhua, Luo Ding, Zhou Huan;
  - Tibet: Jin Sha, He Zuyin, Hou Jie, Zhi Zemin, Gao Liye, Luo Shisheng, Zhang Minhun, Peng Zhe, Yang Dianjia, Wang Qimei, Guo Xilan, Hui Yiran;
  - Xinjiang: Liu Xiaowu, Wang Yuhu, Wang Gulin, Tiyipjan, Kerim Hoja;
  - Hebei: Lin Tie, Pei Yangshan, Hu Kaiming;
  - Henan: Wang Peiyu, Guo Xiaotang, Zhao Wenfu, Yang Weiping, Shao Wenjie, Peng Xiaoqian, Zhang Boyuan, Liu Hongwen, Liu Yanchun, Song Yuxi, Ren Leiyuan;
  - Jilin: Song Zhenting.

## The notes (run 2)

Every item of every note on the pages cited is registered as an edge or a row. Notes that only gloss, with no item, have no edge:
- 60 n.78 (the four named);
- 65 n.86 and n.88;
- 75 n.2 (the 1963 meetings, cited for their facts);
- 83 n.8;
- 91 n.18 (the Ningdu meeting);
- 94 n.24.

Notes that name a statement as the act, with no record (81 n.5b–c, Zhang Chunqiao's and Qi Benyu's words of 1967), are entries without rows (R38). Pages cited that have no notes: 41, 42, 44, 46, 49, 51, 55, 57, 66–70, 73, 76–79, 88, 94, 95, 99.

`./bib notes-coverage` reads only the tree, so this run's pages show there after the merge.

## Where run 3 starts

P. 99, the Jilin committee's standing committee of Aug. 3, 1966 (Jilin University's second secretary), then Jiangsu (early June), Guangdong (June 7), Jiangxi (June 18), Anhui, Shandong, Hubei, Guangxi (June 15, 28), Guizhou, Yunnan (June 28), Shaanxi, Gansu and Zhejiang (June 24) on pp. 99–101. Then ch. 2 §2.2, the Qianmen Hotel meeting (p. 102), and on. The earlier readers' plain-text "To check:" items for this book still to be read are:
- pp. 165–166, `cal.1966-06-23.china-leadership-8` and `cal.1966-07-13.china-leadership-6`;
- pp. 191–194, `cal.1966-08-04.china-leadership-5`, `cal.1966-08-05.china-leadership` and `cal.1966-08-07.china-leadership-6`;
- p. 206, `cal.1966-08-18.china-leadership-4`;
- pp. 449–460, 533 and 540, and the "51" of `cal.1967-05-13.china-leadership-5`;
- in card form, pp. 310, 356, 449–450 and 504–506.

## Counts (run 2)

| | |
|---|---|
| new entries | 88 (35 with place, 3 with time, 32 with `at`; 3 `form:state`) |
| cites | 107 (69 with units) |
| variants | 7 |
| `check` ops | 0 (3 "Check:" sentences in adds) |
| `to-check` ops | 26 |
| `src` ops | 12 |
| `place` ops | 2, and 1 `place-key` |
| `edit` ops | 16 (6 striking plain-text To check items, 10 setting times) |
| witness rows | 12 |
| edges | 56 |
| cards | 7 new |

## Audit of run 2, Nov. 21

Opus audit of patch `2026-11-21-b15b-buweihua-2` (pp. 41–99: ch. 1 §§4–5 and ch. 2 to the Jilin plenum of June 1966; as handed in 88 adds, 107 cites, 7 variants, 26 to-check, 12 src, 16 edits, 2 place, 1 place-key), its witness file (12 rows), its 56 edges under `# run 2`, and the 7 new cards, against the reader's brief, the owner's rulings of Nov. 21, R5, R7, R8, R15, R18, R25a, R27, R35–R43 and the run 1 audit's rulings. The copy fetched afresh into a new directory (849 PDF pages, no text layer; printed = PDF − 20, the folios confirming it); PDF 60–125 (printed 40–105) taken out with `pdfimages` at the native 300 dpi and OCRed with tesseract `chi_tra --psm 6`, with a TSV pass to find lines; every page of 40–103 read whole in the OCR against the patch, and about 75 lines in doubt read on crops of the image (among them 謝鏜忠; 4月16日; 遵囑, not 連夜; 4月8日至6月11日; 5月16日; 《紅旗》第四期; 1963年1月1日; 5月21日 for Zhou's speech; 1965年9月3日; 薄一波、劉少奇、廖漢生 at 88; 2261人 (省管幹部171人); 何祖蔭 … 楊殿甲; 趙文甫、楊蔚萍、邵文杰、張柏園、劉晏春、宋玉璽; 李劍, 44 and 313; 馮基平, 邢相生; 池必卿; 大約在2月12日左右; 31日當天; the notes 52 n.71, 81 n.5, 83 n.8, 86–87 n.15 whole). All 88 adds and all 107 cites read against their pages; every add scripted against the tree (Tiandi runs 1–5, MacFarquhar and Schoenhals, the Mao, Zhou, Peng Zhen and Chen Yi chronologies, Teiwes and Sun, Chen Jian, Bu run 1 and the conditions restore as merged, Chang run 2 merged during the audit) and the pending inbox (Dikötter's *Cultural Revolution* run 2, Ye Jianying run 1, Zhu De run 2), by day, month and year, name tags, Latin names and runs of characters, and the candidates read. Originals backed up first (scratch `audit-bu2-bak/`: the patch, the witness file, the by-work file, this file, the patch's 88 ledger lines, `works/f, l, w, y, z.yaml`). Nothing merged or committed; the download, its images, its text and the crops deleted at the end.

**Verdict.** A careful, mostly faithful reading of a dense stretch: the dates, clock words, figures and quotations hold against the page, the cites say what the page gives, the registry reuse was good and the seven cards are right. The faults are of class: characters missing at first appearance (the largest); seven adds the calendar already held; units claimed beyond the page; place left off where the record gives it; `form:state` on later chronicles; a few visibility and "Made public" slips; name tags; and dated acts on the pages read left in a parenthetical or passed over. All fixed in place. patch-check 0 errors, `fields --patch` 0 findings, `check` 0 errors after the changes to `works/` and the witness file.

**Counts.** Before: 88 adds (35 with `place`, 3 with a time, 32 with `at`, 3 `form:state`, 79 with a `vis:` ruling; by year 1963 1, 1964 3, 1965 3, 1966 78, 1967 3), 107 cites (69 with units), 7 variants, 26 to-check, 12 src, 16 edits, 2 place, 1 place-key. After: 88 adds (42 with `place`, 4 with a time, 32 with `at`, 2 `form:state`, 77 with a `vis:` ruling; 1963 1, 1964 3, 1965 4, 1966 79, 1967 1), 123 cites (77 with units), 12 variants, 28 to-check, 13 src, 18 edits, 3 place, 1 place-key. Witness file: 12 rows (one absorbed) and 1 amendment row; 57 edges under `# run 2` (2 repointed, 1 added). Cards: 7 as made; `w.huishou-wenge-2-vols` amended. Ledger: 8 claims released (`cal.1964-06.china-leadership-11`, `cal.1965.china-leadership-32`, `cal.1966-03.china-leadership-17`, `cal.1966-03-28.china-leadership-7`, `cal.1966-03-31.china-leadership-8`, `cal.1967-04-30.china-leadership-6`, `cal.1967-05-19.china-leadership-5`, `cal.1966-06-14.china-leadership-6`), 8 made (`cal.1966-06.china-leadership-44`, `cal.1966-09-22.china-leadership-3`, `cal.1964.china-leadership-50`, `cal.1966-03-27.china-leadership-12`, `cal.1965-12-23.china-leadership-3`, `cal.1965.china-leadership-33`, `cal.1966-07.china-leadership-29`, `cal.1966-05-06.china-leadership-7`); 88 claims under the patch, matching the adds.

**Faults and fixes, by class (rates of the 88 adds as handed in, or of the 107 cites).**
- *Characters at first appearance* (29 adds, 33 percent): persons, organs, meetings, titles and places in Latin alone: Wang Ming 王明; Wu Han 吴晗 (4), Guan Feng 关锋, Qi Benyu 戚本禹, Deng Tuo 邓拓, Lu Dingyi 陆定一; *Hai Rui baguan* 海瑞罢官 (4), *Hai Rui shangshu* 海瑞上疏, *Hai Rui beiguan* 海瑞背纤, the Lushan meeting 庐山会议 (5), *Hongqi* 红旗; the national conference on creative work 全国创作会议, the enlarged Politburo's briefing forum 政治局扩大会议介绍情况座谈会, the Outline 二月提纲, the Center 中共中央, the Japanese Communist Party 日本共产党, the region's federation 自治区文联, Zhengzhou University 郑州大学; Mao 毛泽东 (8), Peking 北京 (8), Hangzhou, Shanghai, Wuhan, Nanjing, Jiangsu, the Northeast. All added from the page in the calendar's simplified forms; the characters already in `c` checked against the page and the tree's forms: right (Xie Tangzhong 谢镗忠, Lin Jianqing 林涧青, Hu Chi, Xu Juhua, Luo Ding 洛汀, the Tibetan, Xinjiang and Henan names read on the image).
- *Already in the calendar* (7 adds, 8.0 percent), dropped, their claims released, made cites: Kang Sheng's passing the Xiang Qing article to Mao through Jiang Qing (`cal.1964-06-05.china-leadership-5`, MacFarquhar); Zhou Yang's report of the Five-Man Group's ban on political caps (`cal.1965.china-leadership-16`); the standing members' second talk on the Twenty-third Congress, which is Wu Lengxi's meeting of Mar. 10 (`cal.1966-03-10.china-leadership-4`, with a variant: Bu puts it after Hangzhou, the telegram inclining to go); Mao's revision of the JCP communique (`cal.1966-03-27.china-leadership`, whose own witness is Mao's comments dated Mar. 28: a variant for Bu's day and place Shanghai); the Peking three-man group against Deng Tuo (`cal.1966-04-03.china-leadership-4`, unit C, the Peng Zhen chronology's Standing Committee of Apr. 3; a variant for Bu's Mar. 31 and the Secretariat); Qi Benyu of Apr. 30, 1967 and Zhang Chunqiao of May 19, 1967 on "persons like Khrushchev" (`cal.1967-04.china-leadership` and `cal.1967-05.china-leadership-4`, MacFarquhar, each "Check: the day": now edits setting the day and place by R25a). The add on Zhang carried a mistranslation (没完全想到 "did not fully think of" Liu Shaoqi, not "not at all"); gone with it. A possible eighth, Mao's remark of May 1967 to "foreign guests" on the Notice, kept with a Check against the talk with the foreign military delegation (`cal.1967-05.china-leadership`): Bu names no guests.
- *Units claimed beyond the page* (7 of 69 cites with units, 10 percent): `cal.1964-06-05.china-leadership-4` A ("of Ai and Lin" not on 53); `cal.1964-08-18.china-leadership-4` A (seven cities, the films' faults: not on 54), now B; `cal.1966-02-08.china-leadership` E (Bu has "three years on" of rectifying the left and "no harm" of Guan Feng's essays: not support, now a variant on E); `cal.1966-03-20.china-leadership` C and H; `cal.1966-04-22.china-leadership` C and F; `cal.1966-05-14.china-leadership` B ("on each chair"); `cal.1966-05-23.china-leadership-5` D (the Gao Gang and Peng Dehuai self-criticisms). Text faults in four parentheticals: Guan Feng's He Ming essay was not dated 1962 on 56; Liu Shaoqi among those who spoke against Peng Zhen on May 19 (88); the case group of 92 not dated by Bu; Lin Mohan in spring 1965 said the play would be very hard to criticize (78), not that he criticized it hard.
- *Fields* (12 adds, 14 percent): place left off or set aside with `ok:fields-place` where the record names the scene: Hangzhou on Peng Zhen's loss of freedom (Apr. 24), Peking on the Public Security work group (May 12) and the Tianjin group at the North China Bureau's conference, Jiangsu, Liaoning (2), Hebei and Henan (3) on the provincial acts; the Jiangsu count's `at` set before July 7 for "after July 7" (now `before 1966-08`); the Tianjin group dated "after the 16th" (the conference opened May 21); the Jilin plenum of June 14–26, thirteen days, now month-dated ("June, at the plenum of the 14th–26th") under a new id. A night set on Kang Sheng's talk with Zhou (new add). The ten clock edits right but one: the morning of May 16 was already set by another merge (base stale, a no-op): dropped.
- *`form:state` on later chronicles* (3 adds): the Jilin committee's chronicle (1990) and the Henan party chronicle (1986) are no sources of the time (the restore audit's rule): restated as acts and their counts, "the count of the Jilin committee's chronicle", `form:state` struck. Jiang Weiqing's tally is "據當時統計", a count of the time his memoir relays: kept as `form:state`, its X put right ("As a count of the time has it, by Jiang Weiqing's account").
- *Visibility and "Made public"* (6 adds, 6.8 percent): Mao to foreign guests (May 1967) and Wu De to the police (June 7) lacked "Made public: 2008"; the Explanation of May 24 lacked its internal printing (the *Yanjiu ziliao*, 1988); the Wutaishan rally is public, Mao's settling of Jiang's draft not (split out, below); the Shanghai scholars and the Liaoning writers were criticized by name (點名批判), public acts: `vis:` and "Made public" struck. Five adds gave "Made public: 2003" for *Huishou "wenge"*: now 2000, the card's year (below).
- *Names and tags* (7 adds, 8.0 percent): Mao named and untagged or out of "Names:" (5), Peng Dehuai on Xu Liqun's letter, and Mao tagged on Wang Li's notice after the part naming him was cut. Every tag a held person's key; no tag for a person not held.
- *One act an entry* (3 adds): Wang Li's one-sentence notice carried Mao's displeasure, which is the tree's Apr. 14 entry (cited there): trimmed; the Wutaishan rally carried Mao's settling of the draft: split (`cal.1966-07.china-leadership-29`); the Jilin plenum (above).
- *Passed over on pages read* (R5; R8; R15): adds: the Center's forwarding of Lin Biao's speech, Sept. 22, 1966 (86–87 n.15; the tree has it only inside the speech's entry); Jiang Qing's music forum, "the year before last" (1964, her account at 42); Kang Sheng's night with Zhou before Shanghai (76); Peng Zhen alone with Mao, Dec. 23, 1965 (76, Kang's account, with a Check against the talk of Dec. 22); Lin Mohan at Shanghai, spring 1965 (78, Zhang's account); Zhang Chunqiao's count of over 10,000 letters on Yao's article (78, `form:state`, a report of May 6, 1966). Cites: Mao at the work conference of June 8, 1964, on a revisionist Center and the provinces' right to rebel (83 n.8, which the reader had as an undated lead); Lin Biao's "soul-stirring" passage in Kang's speech (`cal.1966-05.china-leadership`, now dated May 5–6 by an edit); the coup question (`cal.1966-03.china-leadership-6`, with Wang Nianyi to check); the two write-ups of Mao's talk of Dec. 21 (`cal.1965-12.china-leadership-7`); the Outline sent to Mao (`cal.1966-02-07.china-leadership-3`, variant Feb. 6); Jiang Qing and the play in 1962, the forum three days before Yao's article, the pamphlet (`cal.1962-07.china-leadership-11`, `cal.1965-11-07.china-leadership-5`, `cal.1965-11-24.china-leadership-3`); the speech handed out at the Eleventh Plenum (`cal.1966-08.china-leadership-52`). Text: *Hongqi*'s "no. 4" for the reprint of the editorial of Apr. 18 is so printed (crop) but impossible (no. 5 was out Apr. 5, no. 6 late April): a Check on the add.

**Rulings on the reader's doubts.**
- *Xie Tangzhong*: the page prints 謝鏜忠 (40, crop). The merged `cal.1966-02-02.china-leadership` carried "Xie Tiezhong" in run 1's cite; the reader's edit of that entry (which strikes the plain-text To check) now also corrects the name.
- *The year of* Huishou "wenge": the card (made at MacFarquhar and Schoenhals run 1) says 2000; Bu prints 北京：中共黨史出版社，2003 (28 n.47, 92 n.21); Yang Jisheng's row 2007. The pages agree across the three (Gong Yuzhi I, 286–287, 305; Li Xuefeng II, 595–603): printings of one book. The card keeps 2000, the earliest, and now carries its `script` 回首「文革」 from Bu's note and a note on the later printings; "Made public" on this run's five adds is 2000. The Tiandi entries that give 2007 for the same essays are for the owner.
- *The Check on* `cal.1966-04-16.china-leadership-8`: answered by Bu 48–49: the comment Zhou had rewritten replaced the one of Apr. 10, the old copies recalled May 2 (Zhongfa (66) 254) and the summary reissued under the old number and date. The merger strikes it by hand.
- *The North China Bureau's conference of May 1966*: one meeting with the Qianmen Hotel meeting. 81 and 97 name it the Bureau's work conference in Peking that May, conveying the Notice; 102–103 open the Bureau's meeting at the Qianmen Hotel on May 21, while the Politburo still sat, Li Xuefeng conveying the Notice and Lin Biao's speech of May 18, the delegations meeting by province. The cite on `cal.1966-05-21.china-leadership-4` stands (now "81, 102–103"); the Tianjin group's attack on Hu Zhaoheng dated "May, from the 21st", place Peking.
- *Zhonggong dangshi ziliao* no. 30 (1989): Bu's notes (45 n.64, 47 n.67, 50 n.69) do not mark it internal; whether it was printed for internal circulation is for the owner (three adds rest "Made public: 1989" on it). The catalogue holds a card for that very issue, `w.zhonggong-dangshi-ziliao-no` (n.d.), to which run 1's row of Liu Zhijian's article could be tied (`part_of`). The same question stands for Wang Nianyi's *Dangshi yanjiu ziliao* of 1982 (83 n.9).
- *Mao's first revision* ("Mar., before the 14th") and *Zhou Yang's talk with Mao* (1963, "soon after"): right by Bu's order of events; the Check on the second is a real doubt.
- *Cites resting on accounts*: right; each parenthetical names the account.

**Witnesses and edges.** The 12 rows read against their notes: right in kind, form, agent and date but one: the chronicle appended to the May 16 Notice (52 n.71, 58 n.76a) was already registered from the *Mao zhuan* (`x.1966-05-16.dashiji-liang-tiao-daolu-douzheng-wenhua-zhanxian`, which Tiandi's 123 n.39 also cites): absorbed by an amendment row, the two edges and the add's `via` repointed. The other rows checked against the registry and every pending witness file by record, date and characters: none registered twice. 86 n.14 (Lin Biao's article in the *Renmin ribao* of Sept. 3, 1965) had no edge: now one to the article's registered print. The 56 edges tested for page and note against the notes as read: right; the notes without items (60 n.78, 65 n.86, 65 n.88, 75 n.2, 83 n.8, 91 n.18, 94 n.24) and the statements without records (61 n.80, 81 n.5b–c) rightly without edges.

**Edits.** Of the reader's 16, 15 current and doing what they say (six strike the plain-text To check for this book, one of them also setting the evening of Mar. 11; nine more set clock bands the page gives); one stale and a no-op (the morning of May 16), dropped. The edit of `cal.1966-02-02.china-leadership` now also corrects the name (above). Three added: the days and places of `cal.1967-04.china-leadership` (Apr. 30, Peking) and `cal.1967-05.china-leadership-4` (May 19, Shanghai), and `cal.1966-05.china-leadership` dated May 5–6, its `at` unset.

**Cards.** The seven new cards against their notes (48 n.68, 45 n.65, 71 n.89, 82 n.7, 81 n.6, 97 n.27, 98 n.28): right; none held before. `w.huishou-wenge-2-vols` amended (above).

**Leads (added).** Zhou Enlai's own forum on national music, after Jiang Qing's ("separate first, then merge"), undated (42); Kuang Yaming 匡亞明 at Nanjing University, the demand to parade him, undated (95).

**For the merger.** (1) Keep (`--take keep`) the duplicate flags patch-check raises on the 88 adds (same day, month or year), each read and distinct; the nearest: `cal.1965-12.china-leadership-13` (Xu Shiyou, by Xiao Hua's account; the tree's coup question of Mar.–Apr. 1966 is cited with it), `cal.1965-12-23.china-leadership-3` (Check against Dec. 22), `cal.1967-05.china-leadership-33` (Check against the military delegation), `cal.1966-09-22.china-leadership-3` and `cal.1966-05-10.china-leadership-8` (acts the tree holds only inside other entries), `cal.1966-04-29.china-leadership-9`, `cal.1966-05-24.china-leadership-3`, `cal.1966-03-27.china-leadership-12`. (2) Checks to strike by hand once the edits land (patch-check refuses an edit that drops a Check): on `cal.1966-04-16.china-leadership-8`, "Check: whether the rewritten note replaced the one issued Apr. 10."; on `cal.1967-04.china-leadership` and `cal.1967-05.china-leadership-4`, "Check: the day."; on `cal.1966-05.china-leadership`, "Check: the day; MacFarquhar (47) has Kang say it …; whether in his speech of May 5–6." (3) Fold run 2's witness file with its amendment row after maozhuan-2's.

## Run 3 (reader b15b-buweihua-3, Nov. 21, 2026): ch. 2 from the provincial purges to the Nie Yuanzi poster, pp. 99–128

Patch `inbox/2026-11-21-b15b-buweihua-3.yaml`; witness rows `inbox/witnesses/2026-11-21-b15b-buweihua-3.yaml`; edges `sources/witnesses/by-work/pu-weihua-zalan-jiu-shijie.yaml` under `# run 3`. Nothing merged or committed. Run 2 and its audit were merged while this run worked; the audit's rulings (read before hand-in) were applied to this run: characters at first appearance for persons, places, organs, meetings and titles in `c`; the province as `place:` on a provincial organ's act; criticism by name (點名批判) a public act; every held person named in `c` tagged and in "Names:". Every add was scripted against the tree as merged (run 2 included) and the pending inbox (Dikötter's *Cultural Revolution* run 2, Ye Jianying runs 1–2, Zhu De run 3), by day, month and year, Latin names and runs of characters, and the candidates read.

**The copy and its keying.** The same Drive PDF (849 pages, a scan with no text layer), fetched afresh into a new directory. PDF 119–260 taken out with `pdfimages -png` at the native resolution and OCRed with tesseract `chi_tra --psm 6`; every page used was read on the page image itself (the full page at screen size reads well), the OCR used only to copy characters; names in doubt zoomed (2×) and OCRed again (程光遠, 任琛, 劉明鑾, 蕭澤寬, 李止舟, 蕭李廖). The folio held on every page read: printed = PDF − 20. The download, its images, its OCR text and the crops were deleted at the end.

**What was read.** Ch. 2 §2 part 1 from p. 99 (the Jilin standing committee of Aug. 3, 1966) to its end (p. 102); §2 part 2, the Qianmen Hotel meeting (102–106); §3, the May 7 directive (106–108); §4, the deaths of Deng Tuo and Tian Jiaying (108–113); §5, the Capital Work Group (113–116); §6, the Central Cultural Revolution Group (116–119); §7, the army's turmoil (120–125); and ch. 2 part 三, the "first Marxist-Leninist poster", to the foot of p. 128. All notes of these pages read (ch. 2 n.29–71).

**What was entered.**
- 140 new entries: 72 with `place`, 7 with a time (Deng Tuo's letter, night; Ding Yilan, early morning; Tian Jiaying's last talk, about 8 a.m.; the General Staff's meeting, morning, and the Signal Corps poster, afternoon, of Aug. 22; the foreign affairs bureau's protest, afternoon of Aug. 25; Peking University's committee, 4 p.m. May 24), 56 with `at`; 114 with a `vis:` ruling. By year: 1962 1, 1963 1, 1964 2, 1965 2, 1966 129, 1967 3, 1968 2. None `form:state`.
- 53 cites, 13 with units, each unit claimed only where the page bears every place, person, figure and claim in it; elsewhere the parenthetical says what the page gives.
- 6 variants: the Qianmen Hotel meeting's attendance (143 by the organization history, 146 by the gazetteer) and its dates (May 23 to July 20 in Li Xuefeng's later account); Deng Tuo's death, May 18 before dawn, not the night of the 17th; Zhou Enlai's instruction on patrolling the two universities, June 6, not 7; the "International Hotel meeting" held at the Peking Hotel; Nie Yuanzi's own account (2004) that Cao Yi'ou did not prompt the poster.
- 3 `check` ops: the Hebei standing committee's dates, June 24–July 15 (`cal.1966.china-leadership-58`); "Made public" by the 1997 *Zhou Enlai nianpu* on `cal.1966-05-18.china-leadership-3` and `cal.1966-05-31.china-leadership-2` (both 2020 in the tree; Bu cites the 1997 edition, 114 n.46, 115 n.47). 5 "Check:" sentences in adds.
- 13 `to-check`, 16 `src`, 1 `place` op (Peking on `cal.1966-05-22.china-leadership-2`).
- 5 `edit` ops: the afternoon of May 22 and the morning of May 23 on Tian Jiaying's two entries; 2 p.m. on the Nie Yuanzi poster (`cal.1966-05-25.china-leadership`); two *Estimates* glosses, Bu's "over 100,000" for the Peking Garrison during the Cultural Revolution (`cal.1966-06-03.china-leadership-5`) and his count of nine of the Cultural Revolution Group's fourteen members gone by the Ninth Congress (`cal.1969-04-28.china-leadership`).
- Witnesses: 12 rows (Li Danlin on Li Xuefeng, 2002; Ren Jie's interview of Ding Yilan, 1999; Wang Fan on Tian Jiaying, 2004; Zhou Enlai's talk to the Academy of Sciences' units, Jan. 21, 1967; Wang Yi, 1998; He Tingyi, 2001; Fan Shuo, 2000; Chen Hong, 1999; and for 128 n.71 Xiang Luo and Meng Jin, 2002, Liu Yangqiao's statement of 1979, Yang Keming's report of July 1967, Nie Yuanzi, 2004). Rows reused: the Liu–Deng talk with Ulanfu of July 2, 1966; the *Hongqi* editorial of July 1, 1966; Wang Li's *Fansilu*, II (an edge with pin 599 to the row registered at 573). 37 edges under `# run 3`.
- 5 new cards, each with `script` from Bu's note: `w.nei-menggu-zizhiqu-zhi` (Ren Yaping, ed., 1999), `w.zhongguo-sixiang-yundong-shi` (Li Honglin, 1999), `w.shinian-fengyu-jishi` (Wu De, 2004), `w.wo-zai-renmin-jundui` (Liang Biye, 1997), `w.ouyang-yi-huiyilu` (1998).
- The ledger holds 140 claims under the patch, matching the adds.

**Visibility and "Made public."** Internal acts carry `vis:only:prc` and "Made public: 2008" where Bu's note names no earlier printing; otherwise the earliest printing his note names: 1988 (Wang Nianyi; Xiao Jingguang's memoir as Bu dates it), 1989 (Pang Xianzhi in *Mao Zedong he tade mishu Tian Jiaying*), 1997 (Liang Biye), 1998 (Ouyang Yi), 1999 (Fu Chongbi; Chen Hong; the Ding Yilan interview), 2000 (the organization history), 2001 (He Tingyi; Yin Hongbiao), 2002 (Li Danlin; Xiang Luo and Meng Jin), 2004 (Wu De). Zhang Enci's paper of May 5 notes the *Wengao*'s internal printing (XII, 57, 1998). The press items (the provincial papers, the *Renmin ribao* of Aug. 25), the posters, the public meetings and criticism by name carry none.

**Duplicates.** Acts first drafted or read as adds that the tree holds, made cites: the Guizhou plenum on Wang Xiaochuan (`cal.1966-05.china-leadership-18`), Zheng Siqun's suspension, suicide and expulsion, Ren Baige's fall; the Qianmen Hotel meeting (May 21), the Liu–Deng talk with Ulanfu (July 2) and Deng's words there (`cal.1966-07.china-leadership-2`), Ulanfu's dismissal (Aug. 16), the Hebei standing committee (run 2's), the Tianjin group; Mao's letter of May 7, his comment of May 14, the Center's forwarding of May 15, the *Renmin ribao* of Aug. 1; Deng Tuo's death, Qi Benyu's article and its reprint; Tian Jiaying's cut of Mao's words, the three-man group's visit and his death; the capital's guard (May 15 ×2, 18, 26, 31; June 3, 5, 7; the garrison's enlargement); Zhou's talk of Jan. 21, 1967; the Group's list (May 28), its Shanghai meeting, Chen Boda's leave (Aug. 30), the Twelfth Plenum's communique, the *Hongqi* editorial of July 1; Liu Yalou's death; the Navy and Air Force meetings of July 3, 4, 7 and 11 (Ye Jianying run 1's entries and the tree's); Xiao Xiangrong (Nov. 15, 1965); the General Staff's poster and Mao's reception of Aug. 25; the Peking University Socialist Education entries (Nov. 11, 1964; Jan. 23, Mar. 3 and March 1965); Cao Yi'ou's group (May 14), Zhang Enci's paper (May 11), the poster (May 25).

## Passed over (run 3; R44, R18's grounds only)

Made by reading every dated act on pp. 99–128 and their notes against the tree and the patch.

| page | date | event | why |
|---|---|---|---|
| 103 | Dec. 20, 1935 | the Declaration to the people of Inner Mongolia issued in Mao's name | outside the span |
| 103 n.31 | Oct. 1925; May 1947 | the Inner Mongolian People's Revolutionary Party founded; ceases with the region's founding | outside the span |
| 108 | 1956–58 | the *Renmin ribao* editorial against rash advance; Mao's "dead men running the paper"; Deng Tuo moved | outside the span |
| 111 | 1979 | Deng Tuo's letter reaches Ding Yilan after his rehabilitation | outside the span |
| 112 | 1948; 1959 | Tian Jiaying becomes Mao's secretary; his words at Lushan to Li Rui | outside the span |
| 119 n.58 | summer 1955 | Chen Boda and Chen Zhengren made deputy heads of the Rural Work Department | outside the span |
| 126 n.67 | May 19, 1957 | the history department's poster at the same wall | outside the span |
| 128 n.71a | July 16, 1979 | Liu Yangqiao's statement on the poster | outside the span (registered) |
| 128 n.71d | Nov. 17, 2004 | Nie Yuanzi's article on the poster | outside the span (registered; its account a variant) |

## Leads (run 3; undated, R50)

- 99: the persecution to death of Wu Tianshi 吳天石, Jiangsu's head of education, and his wife Li Jingyi 李敬宜 (no date).
- 104: the Inner Mongolia Military Region's later "ferreting out" of Wu Tao 吳濤, Kong Fei 孔飛, Ting Mao 廷懋, Tala 塔拉 and Bao Yinzhabu 鮑蔭扎布 ("later", no year).
- 113: Wang Li's judgment that Tian Jiaying was one of the very few who dared criticize Mao to his face (no date).
- 114 n.46, 115: the 70th Division in Peking in place of the 193rd; Ye Jianying's later instruction putting the 112th, 196th and 193rd divisions at the garrison's call (in the cite on `cal.1966-06.china-leadership-10`, no date of their own).
- 118: Mao's absences from the Politburo, his "Peking's air is bad" and "I do not read the *Renmin ribao*" in "the years before the Cultural Revolution" (no year).
- 119 n.58: Chen Boda placed as a deputy head of the Planning Commission (no date).

## Doubts (run 3)

- **Two names illegible in the copy** (101): the Ningxia regional committee's former standing member and vice-chairman (劉?寰) and Shanxi University's secretary-general (宋華?) are named by office in their entries (`cal.1966.china-leadership-78`, `cal.1966-08-05.china-leadership-13`), not romanized; a clearer copy should give them.
- **The Qianmen Hotel meeting's dates**: May 21 in Bu's text (102), May 23 to July 20 in Li Xuefeng's later account (105); the exposure of Ulanfu June 7 to July 20 (104). Both readings stand as variants on `cal.1966-05-21.china-leadership-4`; acts "at the meeting" with no day are dated "1966, May–July" (`at: before 1966-06`).
- **Cites resting on likely matches**: Zheng Siqun's suspension (Bu, undated) on the tree's June 21 entry; the Guizhou plenum (Bu, undated) on the tree's May entry (Tiandi: "throws out"); the Dong Bian report and Mao's masthead both dated Aug. 25 by Bu's one sentence.
- **Checks put to the owner**: whether Mao's talk "on the eve of May Day, 1967" (106 n.34) is the meeting of Apr. 30 with Zhou and the marshals; whether Zhou's words on the Group at the Twelfth Plenum are the speech of `cal.1968-10.china-leadership-4`; whether Liu and Deng's talks with Lin Tie are the ones Li Xuefeng names (105); who named Liu Zhijian and Xie Tangzhong (Ye Jianying in Wang Nianyi, Lin Biao in Wang Li); the second Air Force standing member who did not sign (121 n.61).
- ***Xiao Jingguang huiyilu xuji***: Bu's note (120 n.59) dates it 1988; the card says 1989.
- **The provinces as places**: year-dated provincial acts carry the province's key, as the run 2 audit ruled for Hebei and Henan.

## Persons named in `c` with no name entry (run 3; not tagged)

- *The provinces*: Chen Jingbo, Fu Zhensheng (Jilin); Tao Bai, Qian Jingren, Zhou Cun, Wu Baitao, Sun Shuping (Jiangsu); Qin Mu (Guangdong); Gu Linguang, Shi Linghe, Li Dingkun (Jiangxi); Li Fanfu (Anhui); Yu Xiu, Liu Dishi, Liu Mingluan, Wang Zhongyin, Liu Zhixia (Shandong); Chen Yixin, Zeng Dun, Liu Jisun (Hubei); Lu Di, Zhong Lin (Guangxi); Qin Tianzhen, Xu Jiansheng (Guizhou); Li Mengbei, Gao Zhiguo, Xia Yu, Zhou Zhongde (Yunnan); Zhao Shouyi, Li Qiming, Feng Jiping, Liu Ziyi (Shaanxi); Ruan Dimin, Wu Jian (Gansu); Liu Dan, Lin Danqiu, Xia Chengtao (Zhejiang); Wu Shengxiu, Yang Xin (Ningxia); Wang Zhongqing, Liu Mei, Zhao Shuli, Li Shuwei, Yuan Zhen (Shanxi); Zhang Liqun, Li Yaqun, Ma Shitu, Sha Ting, Li Banli, Cheng Zijian, Ge Bizhou, Xiao Zekuan, Li Zhizhou, Liao Bokang, Ren Baige, Zheng Siqun, Mu Xin (Sichuan, Chongqing); Cheng Guangyuan, Huang Jingtao, Ren Chen (Qinghai); Kang Zhuo, Kong Anmin, Wang Qunwu, Han Shuguang, Zhang Huimin (Hunan).
- *North China and Inner Mongolia*: Li Xuefeng, Xie Xuegong, Ulanfu, Kui Bi, Ji Yatai, Bilige Batu'er, Lin Tie, Liu Zihou, Hu Zhaoheng.
- *Deng Tuo, Tian Jiaying*: Deng Tuo, Ding Yilan, Liu Ren, Tian Jiaying, Dong Bian, Pang Xianzhi, He Jun.
- *The capital and the Group*: Wu De, Yang Shangkun, Wang Li, Guan Feng, Qi Benyu, Yin Da, Liu Zhijian, Xie Tangzhong, Wang Renzhong, Yang Yongzhi, Guo Yingqiu, Zheng Jiqiao, Yang Zhilin, Liu Wenzhen, Tang Pingzhu, Hu Chi, Wang Dongxing, Zhou Rongxin, Cao Yi'ou.
- *The army*: Zhang Xiuchuan, Xiao Jingguang, Su Zhenhua, Wang Hongkun, Liu Yalou, Yu Lijin, Zhang Tingfa, Wang Bingzhang, Cheng Jun, Liu Zhen, Cao Lihuai, Tan Jiashu, Chang Qiankun, Xu Shenji, Wang Huiqiu, Yang Chengwu, Lu Yang, Xiao Hua, Liang Biye, Pan Zhenwu, Xu Yefu, Wang Shangrong, Lei Yingfu, Chen Renqi, Wu Kehua, Su Jin, Liao Dingxiang, Ouyang Yi.
- *Peking University*: Nie Yuanzi, Lu Ping, Peng Peiyun, Song Shuo, Zhang Enci, Chen Shouyi, Yang Keming, Song Bainian, Gao Aijun, Xu Zhaowen; and Gao Gang, Lu Xun, Wang Ming, Zhou Yang.

## The notes (run 3)

Every item of every note on the pages cited is a row or an edge (lettered 103 n.30a–b, 117 n.49a–b, 128 n.71a–d). Notes with no item: 102 n.29 (Huang Jingtao's posts, in the add), 103 n.31 (the party's history), 108 n.37 (Deng Tuo's seal), 117 n.50, n.51, n.53 and 121 n.61 (facts, entered), 121 n.60 (Liu Yalou's death, cited), 126 n.68 (the group's lodging, in the cite); 106 n.34 is a statement without a record (an entry, no row, R38). Pages cited with no notes: 99, 100, 101, 105, 109. `./bib notes-coverage` reads only the tree, so this run's pages show there after the merge.

## Where run 4 starts

P. 129: the law students' poster of May 26 in full, then the poster's course from May 25 (Zhou Enlai's night dispatch, Kang Sheng's sending it to Mao, the broadcast of June 1). The earlier readers' plain-text "To check:" items for this book are still to be read where run 4 reaches them: pp. 165–166 (`cal.1966-06-23.china-leadership-8`, `cal.1966-07-13.china-leadership-6`), 191–194 (`cal.1966-08-04.china-leadership-5`, `cal.1966-08-05.china-leadership`, `cal.1966-08-07.china-leadership-6`), 206 (`cal.1966-08-18.china-leadership-4`), 449–460, 533 and 540, and the "51" of `cal.1967-05-13.china-leadership-5`; in card form 310, 356, 449–450 and 504–506. Run 3 did not reach them.

## Counts (run 3)

| | |
|---|---|
| new entries | 140 (72 with place, 7 with time, 56 with `at`; none `form:state`) |
| cites | 53 (13 with units) |
| variants | 6 |
| `check` ops | 3 (5 "Check:" sentences in adds) |
| `to-check` ops | 13 |
| `src` ops | 16 |
| `place` ops | 1 |
| `edit` ops | 5 (3 times, 2 *Estimates* glosses) |
| witness rows | 12 |
| edges | 37 |
| cards | 5 new |

## Audit of run 3, Nov. 21

Opus audit of patch `2026-11-21-b15b-buweihua-3` (pp. 99–128: the rest of the provincial purges, the Qianmen Hotel meeting, the May 7 directive, the deaths of Deng Tuo and Tian Jiaying, the Capital Work Group, the Central Cultural Revolution Group, the army's turmoil, the Nie Yuanzi poster; as handed in 140 adds, 115 of them with `vis:`, 53 cites, 6 variants, 3 check ops, 5 Checks in adds, 13 to-check, 16 src, 1 place, 5 edits), its witness file (12 rows), its 37 edges under `# run 3`, the 5 new cards, against the reader's brief, the owner's rulings of Nov. 21, R5, R7, R8, R15, R18, R25a, R27, R35–R43 and the run 1 and run 2 audits' rulings. The copy fetched afresh into a new directory (849 PDF pages, no text layer; printed = PDF − 20, the folios confirming it); PDF 118–149 taken out with `pdfimages` at the native resolution; every page of 99–128 read whole on the page image, with its notes (ch. 2 n.29–71), and the lines in doubt read on enlarged crops (the two names of 101; 西頤賓館 at 126 n.68; 1988 at 120 n.59). All 140 adds and all 53 cites read against their pages; every add scripted against the tree as it stands (Bu runs 1–2 merged, Tiandi runs 1–5, MacFarquhar and Schoenhals, the Mao, Zhou, Deng, Peng Zhen, Ye Jianying and Chen Yi chronologies, the *Wengao*, Teiwes and Sun, Dikötter, the conditions restore) and the pending inbox (Chen Yun 1, Ye Jianying 2, Zhu De 3): every same-day entry of the China threads, the month's and year's entries, every entry of 1962–68 sharing a person's characters or a run of a document title's characters, and a keyword sweep of the army, Peking University, Inner Mongolia and Capital Work Group matter; the candidates read. Originals backed up first (scratch `audit-bu3-bak/`: the patch, the witness file, the by-work file, this file, the ledger, `works/x.yaml`). Nothing merged or committed; the download and its images and crops deleted at the end.

**Verdict.** A careful and faithful reading of a long stretch: the dates, clock words, places, names (characters checked against the page and the tree's simplified forms), figures and quotations hold against the page; the registry work is complete (every note of 43 a row, an edge or a gloss without an item, no row registered twice); the cites say what the page bears; the visibility rulings are right in kind for all but two adds. The faults are few and of class: three acts the calendar already held (one dated by another source), two dates the page does not bear and two loose-date positions set the wrong way, two public acts marked closed, a handful of organs and places without characters, a cite pinned to pages the entry already cites from this book, a variant on the wrong entry, and the run's three check ops (each better an edit). All fixed in place. patch-check 0 errors, `fields --patch` 0 findings, `check` 0 errors after the change to `works/`.

**Counts.** Before: 140 adds (72 with `place`, 7 with a time, 56 with `at`, 115 with a `vis:` ruling, 5 with a Check; by year 1962 1, 1963 1, 1964 2, 1965 2, 1966 129, 1967 3, 1968 2), 53 cites (13 with units), 6 variants, 3 check, 13 to-check, 16 src, 1 place, 5 edits. After: 137 adds (71 with `place`, 7 with a time, 55 with `at`, 111 with a `vis:` ruling, 5 with a Check; 1966 126, the other years as before), 56 cites (13 with units), 7 variants, no check op, 14 to-check, 16 src, 1 place, 9 edits. Witness file and edges unchanged (12 rows, 37 edges). Cards: the 5 new as made; `w.xiao-jingguang-huiyilu-xuji` amended. Ledger: 5 claims released (`cal.1966.china-leadership-84`, `cal.1966-08-25.china-leadership-14`, `cal.1966-07.china-leadership-30`, `cal.1966-04.china-leadership-22`, `cal.1966-07.china-leadership-31`), 2 made (`cal.1966.china-leadership-106`, `cal.1966-09.china-leadership-33`); 137 claims under the patch, matching the adds.

**Faults and fixes, by class (rates of the 140 adds as handed in, or of the 53 cites).**
- *Already in the calendar* (3 adds, 2.1 percent), dropped, made cites: Mao's masthead for *Zhongguo funü* (113, "Aug. 25") is `cal.1966-08-20.china-leadership-2` (the *Wengao*: written Aug. 20 at Cai Chang's request of Aug. 18, made public by the *Renmin ribao* of Aug. 25): a cite and a variant on A (Bu's Aug. 25); the *Renmin ribao* report of Aug. 25 (`cal.1966-08-25.china-leadership-15`) stays an add, now pointing back to Aug. 20. The Inner Mongolia group's attack on Ulanfu at the Qianmen Hotel meeting (103: the 1935 Declaration's reprint made "national splitting") is the charge of `cal.1966-05.china-leadership-5` (MacFarquhar; Tiandi: "national splitting" at the North China Bureau meeting): a cite. Ye Jianying's address to the Air Force plenum after the Military Commission's meeting of July 11 (122, undated) is the address of Sept. 7 in the Ye Jianying chronology (`cal.1966-09-07.china-leadership-6`, "the eleventh plenary": the Cultural Revolution, the Air Force's leading group): a cite; the plenum's close and Zhang Tingfa's suspension, which Bu puts after the address, now `cal.1966-09.china-leadership-33` ("Sept., after the 7th", with a Check on the month, a real one: Bu dates neither). The other adds were scripted and read distinct; the nearest are listed for the merger below.
- *Dates and fields* (6 adds, 4.3 percent): Xie Xuegong's trip to Hohhot was "Apr.", which the page does not give (it follows the Bureau's notice of April and precedes the meeting of May 21): now `cal.1966.china-leadership-106`, "1966, before the meeting of May 21"; the Qianmen Hotel meeting's forty-three days against Ulanfu were one entry spanning June 7–July 20: now the opening of June 7, the span in `c`; the *Qinghai ribao*'s articles and the meetings against Huang Jingtao, "after July 1", had `at: before 1966-07` (shown before the day they follow): now `before 1966-08`; the army's meetings like the all-army creative conference, "after" it, had `before 1966-06`, though the conference ran to June 11: now `before 1966-07`. The rest right: every day, clock word and band (the night of May 17, the early morning of May 18, about 8 a.m. of May 23, 4 p.m. of May 24, the morning and afternoon of Aug. 22, the afternoon of Aug. 25), every `at`, every place.
- *Visibility* (2 adds, 1.7 percent of the 115): Changsha's culture and education circles' open campaign against Kang Zhuo (June 8) and the East District committee's rally against him (大會, June 9) are public acts (the run 2 audit's ruling: a public rally, criticism by name): `vis:` and "Made public" struck. Read and right: the press items, the decisions announced in the papers, the posters at Peking University and the counter-posters (no tag); the provincial committees' and bureaus' decisions, the Qianmen Hotel meeting, the Center's and the army's notices and reports, the inner-army meetings, the General Staff's posters inside its compound at the Qitansi and the protest at its Party committee, Deng Tuo's and Tian Jiaying's last days (`vis:only:prc`, "Made public" from the earliest printing the note names, else 2008). Every add with `vis:` has "Made public", every add without none.
- *Characters at first appearance* (8 adds, 5.7 percent): the Peking Public Security Bureau 北京公安局, Zhejiang University 浙江大学, Guangxi 广西, Chongqing 重庆市 and its Youth League committee 团市委, the defense science commission 国防科委, the Socialist Education pilot 社会主义教育运动试点, Peking University 北京大学 and the Institute of Marxism-Leninism 马列主义研究院 (Zhang Enci's paper), the Ministry of Education 教育部: added from the page. The persons' characters checked against the page and the tree's forms: right (陈静波, 富振声, 谷霁光, 刘明銮, 刘济荪, 程光远, 任琛, 奎璧, 毕力格巴图尔, 何钧, 逄先知, 谢镗忠, 王秉璋 … 王辉球, 育南马场, 宋柏年, 徐昭文 among them).
- *Checks* (2 of 5 in adds): the Check on Liu and Deng's talks with Lin Tie (104–105) was not a doubt: Bu names Liu and Deng where Li Xuefeng's account, which he quotes on 105, has "two leading comrades of the Center" talk with Ulanfu and Lin Tie: one talk; the Check struck, Li's account and Li Danlin's article (2002, now the "Made public" year) put in the note. The Check on "the second Air Force signer" asked for what the source does not know (121 n.61, 待查): struck, `c` now says the other is not known. Two Checks added, each a real doubt: whether the Capital Work Group's plan of June (115–116) is among the four papers Mao approved May 29 (`cal.1966-05-29.china-leadership-3`), and the month of the Air Force plenum's close (above).
- *Cites* (2 of 53, 3.8 percent): the Qianmen Hotel cite (`cal.1966-05-21.china-leadership-4`) was pinned "102–103", the pages run 2's cite on the same entry already bears: now "103", for what 103 alone adds (Li Xuefeng presiding, Ulanfu from the Politburo meeting, the eleven named, 143 in all). The investigation group's lodging (126 n.68) is the Xiyi Hotel 西頤賓館 (crop), not "Xiyuan 西苑". The rest right for act, day and units.
- *Variants* (1 of 6): Nie Yuanzi's account (2004) that Cao Yi'ou was told nothing of the poster's content was set on the run's own add of Nie's asking Cao (`cal.1966-05.china-leadership-40`), which it does not dispute; what it disputes, with the teachers' account Bu gives at 127, is the tree's "at Kang Sheng's and Cao Yiou's prompting" (`cal.1966-05-25.china-leadership`, unit A): moved there. The other five right (143 against 146; Li Xuefeng's May 23–July 20; May 18 before dawn; June 6 for Zhou's patrol instruction; the Peking Hotel).

**Rulings on the reader's doubts.**
- *The two names of p. 101*: read on 4× crops, still illegible in this copy (劉?寰, the middle character a cramped form under 厂; 宋華?, a 艹-topped character): naming them by office is right.
- *Cites on likely matches*: Zheng Siqun's suspension (Bu undated) is the city committee's decision of `cal.1966-06-21.china-leadership-12` (Tiandi: branded and named in the *Chongqing ribao*): right. The Guizhou plenum that stripped Wang Xiaochuan of all posts is the "throwing out" of `cal.1966-05.china-leadership-18`: right. Mao's masthead: the tree holds it on Aug. 20 (above), so Bu's "Aug. 25" belongs to the *Renmin ribao*'s report, which stands on Aug. 25; the masthead's add dropped, Bu's day a variant.
- *The Checks left*: the talk "on the eve of May Day, 1967" (106 n.34, on salaries and learning from the Soviets) may be the unity meeting of Apr. 30 with Zhou and the marshals, whose sources do not give its words: a real doubt, kept. Zhou's words on the Group at the Twelfth Plenum (118, no note) may be a passage of the speech of `cal.1968-10.china-leadership-4` or another: kept. Who named Liu Zhijian and Xie Tangzhong (Ye Jianying in Wang Nianyi, 24; Lin Biao in Wang Li, II, 599): two witnesses disagree on a matter `c` does not state; the Check kept beside the two To-check items. Liu and Deng with Lin Tie, and the second Air Force signer: struck (above).
- *The two check ops on "Made public" by the 1997* Zhou Enlai nianpu: the tree cites for these acts only the 2020 edition (`w.zhou-enlai-nianpu-1949-2020`, "Made public: 2020"), but Bu's notes name the 1997 edition (下卷, 31–32 and 33) for the report of May 18 and the meeting of May 26 and the report of May 31, and the run 1 audit's ruling for this book, with R27, takes the earliest printing a cited note names. So not a Check but the year: three edits set "Made public: 1997 ([[w.zhou-enlai-nianpu-1949]], …)" on `cal.1966-05-18.china-leadership-3`, `cal.1966-05-31.china-leadership-2` and `cal.1966-05-26.china-leadership` (whose "2006" stood though MacFarquhar's note names the same 1997 page), and a to-check of III, 33 on May 31. The check ops dropped.
- *The Hebei standing committee's dates* (check op on run 2's `cal.1966.china-leadership-58`): Bu (105) dates the meeting June 24–July 15, 1966: an edit, not a Check: `date: 1966-06`, "June, from the 24th (to July 15)", `at: after 1966-06-23` (month-dated, as the run 2 audit dated the Jilin plenum of June 14–26).
- *Xiao Jingguang huiyilu xuji*: the note prints 北京：解放軍出版社，1988 (crop); the card's 1989 came with the Teiwes reading and no source. Card set to 1988 with `script` 蕭勁光回憶錄（續集） and a note; the add's "Made public: 1988" now names the card.
- *The provinces as places*: right (the run 2 audit's ruling).

**Witnesses and edges.** The 12 rows read against their notes: right in kind, form, agent, date and `open`; searched in `sources/witnesses/` and every file of `inbox/witnesses/` by date, author, title and characters: none registered elsewhere (Tiandi's Fan Shuo and Chen Hong rows are other articles). The reused rows (the Liu–Deng talk with Ulanfu, the *Hongqi* editorial of July 1, Wang Li's *Fansilu*) right. The 37 edges tested for page and note against the notes as read: right; the notes without items (102 n.29, 103 n.31, 108 n.37, 117 n.50, 51, 53, 121 n.60, 61, 125 n.67, 126 n.68) and the statement without a record (106 n.34) rightly without edges.

**Edits.** The reader's 5 current (bases read again at the end) and right: the afternoon of May 22 (前一天下午) and the morning of May 23 (上午) on Tian Jiaying's entries; 2 p.m. on the poster; the two *Estimates* glosses (115: "在文化大革命期間，北京衛戍區人數達到十萬多人", Bu's own statement after Fu Chongbi's words; 119: nine of fourteen out by the Ninth Congress, five in the Politburo), each on an entry with no gloss. Added: the Hebei dates and the three "Made public" years (above). Now 9.

**For the merger.** (1) Keep (`--take keep`) the duplicate flags patch-check raises on the 137 adds (same day, month or year; each read and distinct). The nearest: `cal.1966-08-25.china-leadership-15` (the report of the masthead; the writing is Aug. 20), `cal.1966.china-leadership-87` (the North China Bureau's report on Ulanfu, a document; the charge itself is `cal.1966-05.china-leadership-5`), `cal.1966-06-07.china-leadership-15` (the opening of the exposure of Ulanfu within the meeting of May 21), `cal.1966-06.china-leadership-43` and `cal.1966-06-03.china-leadership-8` (the plan and Zhou's approval; Check against May 29), `cal.1966-07-03.china-leadership-9` (Ye's call to Xiao Jingguang; his calls to Lin and Deng are the tree's), `cal.1966-07-08.china-leadership-4`, `cal.1966-09.china-leadership-33`, `cal.1967-04.china-leadership-22` (Check against Apr. 30), `cal.1968-10.china-leadership-26` (Check against `-4`), `cal.1966-05-05.china-leadership-8` (Zhang Enci's paper, which the tree holds only inside Mao's comment of May 11), `cal.1966-08-02.china-leadership-10` (Tao Zhu adviser, which the tree holds only in a parenthetical of Aug. 30). (2) No Check to strike by hand: the run's check ops are dropped and its edits strike none. (3) The edits on `cal.1966-05-18.china-leadership-3`, `-05-26` and `-05-31` set `n` (a "Made public" year, so not additive); rebase if another merge touches those notes first.

**For the owner.** The Zhou Enlai chronology entries of 1966–76 read from the 2020 edition carry "Made public: 2020", though the 1997 edition (`w.zhou-enlai-nianpu-1949`, three volumes, 下卷 to 1976) printed the same years; the reading of 1962–65 from the 1997 edition says "Made public: 1997". Three entries are set right here, from Bu's notes; the class is for the owner.

## Run 4 (reader b15b-buweihua-4, Nov. 21, 2026): ch. 2 from the law students' poster to the Tsinghua middle school work group, pp. 129–168

Patch `inbox/2026-11-21-b15b-buweihua-4.yaml`; witness rows `inbox/witnesses/2026-11-21-b15b-buweihua-4.yaml`; edges `sources/witnesses/by-work/pu-weihua-zalan-jiu-shijie.yaml` under `# run 4`. Nothing merged or committed. The run 3 audit (read before the run's later batches and applied to them: characters at first appearance for organs, units, titles, documents and places; public acts, criticism by name and the press without `vis:`; every `vis:` add with "Made public"; a held person named in `c` tagged and in "Names:") binds this run. Run 3 was merged into the tree while this run worked; its adds are cited here where Bu returns to them. Every add was scripted against the tree as it stood (run 3 included) and the pending inbox (Chen Yun 1, Ye Jianying 2, Zhu De 4), by day, month and year, Latin names and runs of characters, and the candidates read; the ledger was read for each id before it was claimed.

**The copy and its keying.** The same Drive PDF (849 pages, a scan with no text layer), fetched afresh into a new directory. PDF 145–240 taken out with `pdfimages -png` at the native resolution and OCRed with tesseract `chi_tra --psm 6` (pages that came back empty under load OCRed again). Every page used was read on the page image, whole or in strips; names, dates and note numbers in doubt on 2× crops (among them 6月1日到7月11日 at 134, not July 1; 2月17日 at 135; 1965年10月28日 at 143 n.85; 5月10日 at 146; 鄧東哲, 袁智平, 李人林 at 161; 惠庶昌 at 152; 章建華, 劉晉 at 167; 錢抵千, 尚力科 at 150; 彭林 at 151; 余煥椿 at 151 n.96). The folio held throughout: printed = PDF − 20. The download, its images, its OCR text and the crops were deleted at the end.

**What was read.** Ch. 2 part 三 from p. 129 (the law students' poster of May 26 and its note; the course of the Nie Yuanzi poster from May 25 to the broadcast of June 1 and the printing of June 2); part 四 「大大小小的『三家村』」 (130–140: the Ministry of Culture's report, the Central-South and East China bureaus' reports, the local "Three-Family Villages", the Northwest "Three-Family Village" and Hu Yaobang in Shaanxi, Wuhan University and Li Da, the *Yunnan ribao*); part 五 「紅衛兵」 (140–149: school education before 1966, the Tsinghua middle school Red Guards to June 8); part 六 「工作組」 to p. 168 (the dispatch of the work groups, Hangzhou, the June 18 incident, the wave against the work groups and the "resist interference" campaign, the Tsinghua middle school work group to June 20). All notes of these pages read (ch. 2 n.72–115).

**What was entered.**
- 144 new entries: 116 with `place`, 16 with a time (among them June 2, 0:30 a.m. at Peking University; 7:30 p.m. of June 2 at the Northwest Bureau; the afternoon, evening and night of June 1; the noon of June 18), 19 with `at`; 86 with a `vis:` ruling. By year: 1962 2, 1963 2, 1964 11, 1965 11, 1966 117, 1968 1. None `form:state`. Two carry an *Estimates* gloss: Bu's count of 8,691 Party members and cadres wrongly handled in Shaanxi's socialist education (`cal.1963-11.china-leadership-5`, from the organization history, 133 n.79) and his over 60,000 households misclassified in the "make-up lessons" (`cal.1966-03.china-leadership-19`).
- 49 cites, 18 with units, each unit claimed only where the page bears every place, person, figure and claim in it; elsewhere the parenthetical says what the page gives.
- 7 variants: Zhu Shaotian 朱劭天, not Zhu Kantian, at Wuhan University (132); over three hundred, not over 3,000, at the Tsinghua middle school on June 8 (149); Xiao Wangdong's army work groups sent to the Ministry of Culture's units, 300 from the General Political Department and 500 from the Nanjing Military Region (153); the Tsinghua work group entering the evening of June 8, not June 9 (156); Wang Tiecheng's poster June 14, not 13 (158); over sixty struggled at Peking University on June 18 (158); Kuai Dafu's note dated June 24, not 21 (163).
- 1 `check` op (`cal.1966-05-29.china-leadership-2`: the hour of the Red Guards' founding, dusk in Bu, the afternoon in Tiandi, after the evening study session in MacFarquhar).
- 15 `to-check`, 3 `src`, 1 `place-key` (`ankang`).
- 8 `edit` ops: the noon of June 1 (Mao's comment), the afternoon of June 2 (the Tsinghua middle school poster), the morning of June 8, the early morning of June 20 (Geological Institute); the *Estimates* gloss on the founding of the first Red Guards (`cal.1966-05-29.china-leadership-2`: tens of millions in the movement; 534,000 college and 12,968,000 secondary students at the end of 1966, 140 n.83); the day June 17 on `cal.1966-06.china-leadership-28` (the girls' middle school poster); and two striking the earlier readers' plain-text To check items for this book that this run's cites replace: p. 165 on `cal.1966-06-23.china-leadership-8` and p. 166 on `cal.1966-07-13.china-leadership-6`.
- Witnesses: 18 rows (the law students' poster in the *Dazibao xuan*; Gong Yuzhi on Peng Zhen and Peking University's socialist education, 2002; the Ministry of Culture's request report, forwarded June 20, 1966; 〈胡耀邦主政陝西的兩百天〉 in *Huainian Yaobang* IV; Bu's own article of 1999 on the Tsinghua middle school Red Guards; six press issues of 1963–64 (144 n.86a–f); Li Xiangqian, 1999; the Tsinghua middle school work group's report of July 4, 1966; Yu Huanchun, 2004 no. 12; Song Qiong and Zhang Wenrong's report of June 21, 1966; the Center's forwarding of the Peking University bulletin no. 9; Hu Keshi and Hui Shuchang's remarks of June 10, 1966; the Tsinghua middle school Red Guards' "Seven questions and answers", Sept. 13, 1966). Rows reused: the *Wenhua geming jianbao* no. 13 (wengao-18b, not edged: Bu names no source for it) and *Yunnan wushi nian* (the conditions restore's row, 140 n.82). 39 edges under `# run 4`.
- 7 new cards, each with `script` from Bu's note: `w.beijing-daxue-jishi-1898` (Wang Xuezhen and others, 1998), `w.shanxi-tongshi` (2001), `w.huainian-yaobang-vol-4` (Zhang Liqun and others, 2001), `w.zaisheng-fenghuang` (Han Suyin, 1991), `w.hongweibing-shidai-japanese-ed` (Zhang Chengzhi, 1992, Japanese; Bu gives only the Chinese title), `w.zhongguo-gongchandang-sichuan-lishi` (2000; made with `--force` beside the national chronology `w.zhongguo-gongchandang-lishi-dashiji`), `w.fengyu-suiyue` (Liu Bing, 1998, the Tsinghua University Press edition; the 2008 edition is Tiandi's row `x.2008.liu-bing-fengyu-suiyue-1964-1976-de-qinghua-2008`).
- The ledger holds 144 claims under the patch, matching the adds. One claim released: `cal.1966-06.china-leadership-52` (Xiao Wangdong's army work groups, made a variant on `cal.1966-06-06.china-leadership-3`), then claimed again by new-id for Liu and Tao Zhu's editorial. Four ids `./bib new-id` handed out had been claimed and released by the run 3 audit and never entered: `cal.1966.china-leadership-84` (now the Shandong standing committee), `cal.1966-07.china-leadership-30` (Li Da's "My confession"), `cal.1966-07.china-leadership-31` (the Lingling official) and `cal.1966-04.china-leadership-22` (the Tsinghua middle school's second request): no tree entry ever held them.

**Visibility and "Made public."** Internal acts carry `vis:only:prc` and "Made public: 2008" where Bu's note names no earlier printing; otherwise the earliest printing his note names: 1994 (Mu Xin), 1996 (Jiang Weiqing), 1998 (*Beijing daxue jishi*; the *Liu Shaoqi zhuan*; Liu Bing), 1999 (*Yunnan wushi nian*; Bu's own article), 2000 (the organization history; the Sichuan chronology), 2001 (*Huainian Yaobang*), 2004 (Yu Huanchun). The Ministry of Culture's report notes the *Yanjiu ziliao*'s internal printing (I, 53, 1988). No `vis:` on the posters, the press, public meetings and marches, the struggles and the deaths.

**Duplicates.** Acts drafted or read as adds that the tree holds, made cites: Mao's comment of June 1 and the broadcast (`cal.1966-06-01.china-leadership`), Peng Zhen at Peking University June 29, 1965, the Center's forwarding of June 23 (Liu's note), Zhang Desheng's death, Wuhan University's work group (June 13), Mao's note on Li Da's letter and Tao Zhu's (Aug. 10), Li Da's death, the *Jiangxi ribao* of June 18 and the Southwest Bureau's reply of June 28 (run 3), Mao's return of July 18, his talk of Mar. 30, 1966, the founding of the Red Guards (May 29), the Tsinghua middle school posters of June 2 and the support of June 8, the decision of May 29 and the letter of May 30, the dispatches of June 3, the enlarged Standing Committee of June 3 and 21, Shanghai's work groups, the Secretariat's work group of June 6, the Hangzhou meeting of June 9–12 and Mao's words of June 12, Tsinghua (June 8, 9, 13, 14, 21, 24), Xi'an Jiaotong (June 3, 7–9), the girls' middle school (June 17), the June 18 incident and bulletin no. 9, Liu's forwarding of June 20 and his talk with the first middle school's work group, Wang Guangmei at Tsinghua, the thirty-nine colleges, the Geological Institute (June 20 and after), Peking Normal University (June 20), Li Xuefeng at the Peking Hotel (June 23), the college group's figures (July 13), Chen Boda's Xiaozhan letter (Aug. 4, 1964) and the instruction of Oct. 24, 1964.

## Passed over (run 4; R44, R18's grounds only)

Made by reading every dated act on pp. 129–168 and their notes against the tree and the patch.

| page | date | event | why |
|---|---|---|---|
| 136 | May 1977 | the Shaanxi committee's broadcast rally still naming Zhao Shouyi and Li Qiming; Zhao's words to two Organization Department cadres | outside the span |
| 136 | Jan. 1979 | the Shaanxi three-level cadres' meeting at Xi'an reversing the verdicts on Hu Yaobang, Zhao, Li and Chen Yuanfang | outside the span |
| 137 | (after 1979) | Jingyang county: 84.6 percent of the cadres punished in the socialist education rehabilitated | outside the span |
| 137 | 1923; 1952 | Li Da leaves the Party; becomes president of Wuhan University | outside the span |
| 165 n.111 | 1918–1989 | Imre Nagy's life (a gloss on Li Xuefeng's words) | outside the span |

## Leads (run 4; undated, R50)

- 132: the Hunan, Wuhan University, Yunnan and Southwest "Three-Family Villages" are listed as found "in the same period"; Hunan's entered under 1966, the others already in.
- 134: the Northwest Bureau's material lists Hu Yaobang's eight points, Chen Yuanfang's draft report, Lin Mu's letter to Mao through Tian Jiaying and the "stealing of intelligence" (the requests for documents through the General Office), none dated.
- 137 n.80: Wuhan University's units each drag out their "Three-Family Villages", over ten in the school, four in the general affairs office (no date).
- 139: the *Yunnan ribao*'s printing of Deng Tuo's Yunnan poems (no date).
- 144: the Center's documents correcting the local excesses against "bizarre clothes" (no date); 144 n.87, Anna Louise Strong's letter that the Red Guards were organized by "Lin Biao's army" (Han Suyin, no date); 144 n.88, Washington's alarm at the Red Guards (Li Xiangqian, no date).
- 145 n.91: the content of the "two recollections and three examinations" at the Tsinghua middle school (in the add of May 1965).
- 154 n.101: some colleges show again the documentary films of the 1957 anti-rightist campaign (*Guangxi wenge dashi nianbiao*, 2; no date).
- 160: Mao's later sharp criticism of Peking University's closed gate (no date).
- 166: Kuai Dafu expelled from the League and held eighteen days; the Peking Forestry Institute's expulsion of two "rightist students" from the Party; over a hundred Peking students branded counter-revolutionaries by the work groups (in the July 13 cite's parenthetical; no dates).

## Doubts (run 4)

- **Run 3's "Gu Linguang 谷霁光"** (`cal.1966-06-18.china-leadership-8`, now in the tree): 霽 is *ji*: Gu Jiguang. To be corrected.
- **The author of 〈胡耀邦主政陝西的兩百天〉** (132 n.78): printed 蔡?人, the middle character cramped (趙 or 越) on the 2× crop; the row leaves the name out of its romanization.
- **The *Guangxi wenge dashi nianbiao*** (154 n.101): Bu prints Guangxi renmin chubanshe, 1999; the card `w.guangxi-wenge-dashi-nianbiao` says 1990. The edge is to the card, pin 2.
- **Gong Yuzhi's article** (130 n.75, 2002) and **Yu Huanchun's** of 2004 no. 12 (151 n.96) are rows, not cards; run 1 registered another Yu Huanchun article (2004 no. 5).
- **"Made public" for the Northwest Bureau's acts** (132–135): 2008, except Liu Lantao's raising of the Northwest "Three-Family Village" (2001, *Huainian Yaobang*, which n.78 names). Bu's narrative of 133–135 likely rests on the same memoir and the organization history; only n.78 and n.79 name them.
- **The press issues of 144 n.86**: six entries, each "carries criticism of" the matters Bu names for all six together; which issue treats which matter is not given.
- **The Yunnan committee's standing committee of May 26** (`cal.1966-05-26.china-leadership-6`) carries a Check against run 3's "work conference" decision (`cal.1966.china-leadership-73`, "1966, before June"): Bu (100) and (139) may describe one decision.
- **Tiandi's Tsinghua middle school figure** of 3,000 (June 8) against Bu's three hundred: a variant, not settled.
- **Two cites rest on accounts in notes**: the June 12 words (Li Dazhang's and Jiang Weiqing's accounts, 154 n.100) and the June 21 Standing Committee (the *Liu Shaoqi zhuan*, 164 n.110); the parentheticals say so.

## Persons named in `c` with no name entry (run 4; not tagged)

- *Peking University and the poster*: Nie Yuanzi, Yang Keming, Zhang Enci, Cao Yi'ou, Ge Hua, Cui Xiongkun, Lu Ping, Jiang Nanxiang, Zhang Yan, Li Xuefeng, Wu De, Zhang Chengxian, Su Qianyi, Chi Biqing, Huang Zhigang, Liu Yangqiao, Yang Yixi, Peng Lin, Wu Zhensheng, Zhang Dehua, Liu Jiabin, Chen Yingfu, Xia Linhan, Xiu Zhicai, Xu Zhaowen.
- *The press and the reports*: Zhou Yang, Tang Pingzhu, the Central-South and East China bureaus' named scholars and writers (Qin Mu, Ke Lin, Liu Zhiming, Li Da, He Dinghua, Zhu Shaotian, Cheng Yun, Wu Keren, Kang Zhuo, Guo Xiaotang, Lu Di; Zhou Gucheng, Li Pingxin, Zhou Yutong, Gu Jiguang, Sun Shuping, Luo Ergang, Qu Baiyin, He Luting, Shi Linghe, Zhou Xinfang, Li Junmin, Xia Zhengnong, Li Fanfu, Yu Xiu, Tao Bai, Kuang Yaming).
- *The provinces*: Fu Jiafen, Lin Zengping, Ma Jigao (Hunan); Li Jingchun, Ding Xiusheng (Shandong); Zhao Zongfu (Shanxi); Liu Lantao, Hu Yaobang, Zhao Shouyi, Li Qiming, Zhang Desheng, Huo Shilian, Liu Geng, Chen Yuanfang, Lin Mu, Xi Zhongxun, Gao Gang (Shaanxi, the Northwest); Zhang Tixue (Hubei); Li Mengbei, Xia Yu, Zhou Zhongde, Xue Bo, Deng Tuo (Yunnan); Yan Kelun, Li Shiying, Song Qiong, Zhang Wenrong (Xi'an).
- *Schools and the work groups*: Mao Yuanxin, Wang Hairong, Lin Feng, Luo Xiaohai, Bu Dahua, Kuang Taosheng, Wang Ming, Zhang Xiaobin, Wang Huicheng, Zhang Chengzhi, Tao Zheng, Gao Hongxu, Niu Wanping, Peng Xiaomeng, Gong Xiaoji, Zhang Jianhua, Liu Jin, Wan Bangru, Hu Keshi, Hui Shuchang, Zhang Wanhe, Deng Dongzhe, He Changgong, Li Renlin, Tao Lujia, Gao Shukui, Tan Houlan, Sun Youyu, Yuan Zhiping, Chen Yongkang, He Fangfang, Gou Deyuan, Niu Delong, Kuai Dafu, Wang Guangmei, Shi Mingyuan, Li Dazhang, Zhao Ziyang, Mu Xin, Qian Dixian, Shang Like, Zhu Yuepeng, Yang Ding, Lu Ying, Shao Yihua.

## The notes (run 4)

Every item of every note on the pages cited is a row or an edge (lettered 144 n.86a–f). Notes with no item: 137 n.80 (Wuhan University's "villages", a lead), 140 n.83 (Bu's statistics, the *Estimates* gloss), 140 n.84 (Mao's words, a statement without a record, cited on `cal.1966-03-30.china-leadership`), 145 n.90 and n.91 (facts, entered), 150 n.94 (Zhang Chengxian's post, in the cite), 160 n.106 (Xiaozhan, cited on the 1964 entries), 165 n.111 (Nagy), 166 n.112 (the twenty-four colleges, in the cite), 167 n.113 (the four classes, in the cite). Pages cited with no notes: 134, 135, 146, 148, 155, 158, 163. `./bib notes-coverage` reads only the tree, so this run's pages show there after the merge.

## Where run 5 starts

P. 168, at the foot: the Tsinghua middle school work group's report material ("over twenty thousand posters so far…"), then the rest of ch. 2 part 六 §4 「工作組與紅衛兵」 and on. The earlier readers' plain-text "To check:" items for this book still to be read: pp. 191–194 (`cal.1966-08-04.china-leadership-5`, `cal.1966-08-05.china-leadership`, `cal.1966-08-07.china-leadership-6`), 206 (`cal.1966-08-18.china-leadership-4`), 449–460, 533 and 540, and the "51" of `cal.1967-05-13.china-leadership-5`; in card form 310, 356, 449–450 and 504–506. Pp. 165 and 166 are now struck by this run's edits.

## Counts (run 4)

| | |
|---|---|
| new entries | 144 (116 with place, 16 with time, 19 with `at`, 86 with `vis:`; none `form:state`; 2 *Estimates* glosses) |
| cites | 49 (18 with units) |
| variants | 7 |
| `check` ops | 1 (1 "Check:" sentence in an add) |
| `to-check` ops | 15 |
| `src` ops | 3 |
| `place-key` | 1 (`ankang`) |
| `edit` ops | 8 (4 times, 1 *Estimates* gloss, 1 day, 2 striking plain-text To check items) |
| witness rows | 18 |
| edges | 39 |
| cards | 7 new |
