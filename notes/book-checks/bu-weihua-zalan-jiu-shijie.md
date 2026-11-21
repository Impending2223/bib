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
