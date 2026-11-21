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
