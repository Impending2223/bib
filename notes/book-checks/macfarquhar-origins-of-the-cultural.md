# Roderick MacFarquhar, *The Origins of the Cultural Revolution*, vol. 3, *The Coming of the Cataclysm, 1961–1966* (1997)

Card `w.macfarquhar-origins-of-the-cultural` (made Nov. 17, 2026: the first author's surname and the main title, "vol. 3" in the title field because the card is for this volume; the later cards for vols. 1 and 2 will need their own ids). Batch 15, second wave, run 1 (the reader reassigned from Liu Shaoqi's chronology): patch `inbox/2026-11-17-b15b-origins3-1.yaml`; witnesses `inbox/witnesses/2026-11-17-b15b-origins3-1.yaml`; edges `sources/witnesses/by-work/macfarquhar-origins-of-the-cultural.yaml`.

## Run 1: the copy, the pages

The owner's Drive copy (`158VMAnmx38VMf6ltbnpQ0FZloy93Gldp`, 20 MB, 749 PDF pages, a FineReader text layer; the Oxford/Columbia edition of 1997). Printed page = PDF page − 16 in the text and in the notes (the notes begin at PDF 495, printed 479). Folio checked on the text layer's headers at pp. 1, 11 (chapter 1), 137 (chapter 7) and 479, and p. 144 against the page image (the timetable). Pinpoints are printed pages.

Read: the Introduction, chapters 1–6 (Part One, "The Third Bitter Year") and chapter 7 to p. 151 (the Seven Thousand Cadres Conference, to the start of the discussion of Liu Shaoqi's written report: the paragraph on the "3/8" rules). The next run begins at p. 151. The notes of every page read (479–537, to note 59 of chapter 7) with them. Appendix 1 (the birth and death rates, pp. 7–8) and the tables of figures were read as statistics: no event.

## The citations it had

None: the calendar's one hit for the name is `cal.1966-07-28.india-and-china-cultural-revolution`, which cites no volume of it. The cards for vols. 1 and 2 do not exist; "Origins I" and "Origins II" in the notes are witnesses (`x.1974.macfarquhar-origins-i`, `x.1983.macfarquhar-origins-ii`).

## The patch

- 145 entries added (143 under China: Leadership, 2 under Soviet Union): Dec. 1960 to Feb. 1962, chiefly the grain imports and the cutting of the urban population (Chen Yun, Li Xiannian, Li Fuchun and the provinces' meetings), the rural investigations of 1961 (Zhou's at Handan, Liu Shaoqi's forty-four days in Hunan, the Peking teams), the Sixty Articles' drafts and the June revision, the programmatic articles of 1961 (the Forty on commerce, the Thirty-five on handicrafts, the Seventy on industry, the Fourteen on science, the Sixty on higher education, the Eight on literature and art), Chen Yi's and Zhou's speeches on the arts, Mao and He Qifang on the ghost stories, the Soviet and Albanian dealings (the MiG-21 letter, the grain loan, Li Xiannian at Tirana, Zhou at the Twenty-second Congress), and the Seven Thousand Cadres Conference's timetable (Dec. 16 to Feb. 26).
- 53 cites to entries already in the calendar (the Beidaihe and the Peking and Lushan work conferences, the Ninth Plenum, the Canton conference and its three drafting stages, Mao's letters, the Berlin and Laos entries the chapter on China's isolation bears on, the January 1962 conference days), each with its page and a parenthetical for what it bears out; 6 `check` ops where this volume's date differs from the entry's (Tian Jiaying's report, Feb. 5 or 6; the Handan meeting, Sept. 26 or 27; the Twenty-second Congress days; the decision of Dec. 21 for the larger meeting; Li Fuchun's day at the plenum; the day of Zhou's return).
- 61 of the new entries carry a "Check:" sentence, nearly all for a day the book gives only as a month, a season or "at about this time"; these take `date` as a month or a year and, where the book gives early, late or a stretch, an `at:` (nine).
- No `variant` ops: the differences are all of day, and are written as Checks.
- Visibility: the acts inside the leadership `vis:only:prc` (126 entries) with "Made public: 1997." (the volume's year); the foreign dealings `vis:only:prc+ussr`; what was published at the time (the People's Daily's editorials, Zhou's visit to Burma, the Australian and Canadian sales, Mao's letter to the Jiangxi Labour University) no ruling.
- Claim maps: each new entry's `src` ties the page to all of `c`, with `via` rows to the witnesses of the notes of the pages cited; the cites' `src` ops add `via` rows (`?`: the parenthetical).

## The notes pass

The notes were not in the text layer as the book prints them: the note numbers are lost or garbled on many pages (the superscript figures come out as symbols). I OCRed the notes pages (pp. 479–537, `tesseract`, 200 dpi), split the notes at the printed paragraph breaks, numbered them in sequence against the printed figures where they survive, and found each note's call page from the text pages and each notes page's "NOTES TO PAGES" header. Of the 764 notes of the Introduction and chapters 1–7 (to p. 151), 744 were recovered as separate notes; 20 were glued to a neighbour by the scan (their items stand under the neighbour's anchor): Intro 15; ch. 1, 15; ch. 2, 25 and 72; ch. 3, 98–100 and 128–130; ch. 4, 17; ch. 5, 117–119, 129 and 165; ch. 6, 12, 40 and 53; ch. 7, 50.

- Edges: 1,035, an item of a note each, anchored "page n.note" (a letter after the number where a note has several items: "11 n.3a"), to 231 witnesses, each a study, memoir, collection or press row (`kind` study, memoir, collection, press; `open: not held`; `read: false`), and 30 to the card `w.zedong-jianguo-yilai-mao-zedong` (the *Wengao*). The Chinese compilations the notes lean on most (the Guofang Daxue *Cankao Ziliao* 23, *Liu Shaoqi Xuanji*, Bo Yibo's *Ruogan Zhongda Juece*, the *Jingji Dashiji*, *Mao Zedong sixiang wan sui*, *Mao Zedong he tade Mishu Tian Jiaying*, Chen Yun's *Wengao*) are each a row, with the pages in the edges' items.
- 667 of the 744 notes carry at least one edge. The 77 with none are notes the scan's text did not let me read into items (expository sentences, a statistic's derivation, a translation of a title, a conversion rate), and 332 fragments of the others' text were passed as not a citation (a clause cut at a semicolon, a quotation, an expository remark). I have not read those 77 notes one by one; a second pass should (and should re-read my edges against the notes for the items split at a semicolon inside a sentence).
- The rows are at the level of the work, not of the document the note gives from it: where the note names a document (the 3 Dec. 1960 directive, "Mao's letter of instruction to Tian," Liu's speech of Jan. 27, 1962 in the mimeo version) the edge goes to the collection that prints it, with the pages in the entry's To-check line. The documents are not yet witnesses of their own (`part_of` rows): a second pass.
- `./bib notes-coverage w.macfarquhar-origins-of-the-cultural`, run in a scratch copy of the tree with the patch merged (the card is cited nowhere in the tree before the merge): 703 cites (the To-check pointers count among them), 120 pages cited, 116 with notes registered, 1,035 edges, 1.47 edges per cite; the 4 pages cited with no notes registered (20, 53, 105, 144) have no note on them. `./bib check` in that copy: no error on any entry of the patch but the 75 "possible duplicate" conflicts the merge writes for same-day, same-thread entries (each to be settled `--take keep`).
- Pages cited by the patch: 119 of the 151 (the others are the tables of figures and the pages of argument no entry rests on alone). Pages cited with no note on them, so no edge: 20, 53, 105 and 144 (a page of argument, a page of Liu's anecdotes, a table of drafts, the conference's timetable).
- "To check:" lines: on each new entry and each cite, the first items (eight, five) of the notes of its pages, as "Work, pages (cited by [[card]], page n.note)". The `via` rows tie the entry's units to the same witnesses.
- Not yet done for the pages of this run: the items beyond the first five or eight of the notes of a cited page appear as edges but not in a To-check line.

## Passed over (R44)

Dated events the book treats that this run did not enter, with the ground. None is R18's; each is an event a second pass should enter or a lead (R50: undated).

| page | date | event | why |
|---|---|---|---|
| 5 | 1959–61 | Zhou's grain ration, the abacus, no meat or eggs, the scolding over vegetables | undated ("during this period"): a lead |
| 22 | 1961, early | two unpublished poems of Mao against revisionism; the publication of *Stories About Not Being Afraid of Ghosts* "shortly thereafter" (*PR* No. 10, 1961) | undated: a lead |
| 33 | Mar.–June 1962 | Tianjin: Wan Xiaotang assigns the population-reduction tasks (Mar.); a leading small group (Apr.); the target raised between Apr. 14 and June 8 | dated to 1962; not yet entered |
| 39 | Jan. 26–Feb. 24, 1961 | Mao's journey by rail to Canton (Tianjin, Jinan, Nanjing, Shanghai, Hangzhou, Nanchang, Changsha) | in the calendar by its days; not yet cited (n.4) |
| 45 | 1961 | Mao's praise of Canton's *Yang Cheng Wan Bao* | undated: a lead |
| 60 | 1961 | Liu orders an inquiry into the press coverage of the Leap, "habitual lying" | "at about this time": a lead |
| 59 | 1961 | Tao Zhu to Hunan; Deng Zihui and Zhang Dingcheng to Fujian | undated: a lead |
| 112 | 1960 | Chen Yi's poem "Heavy snow weighs down the pine" | undated: a lead |
| 124–125 | June–Nov. 1960 | the Bucharest confrontation, Peng Zhen and Khrushchev; Hoxha at the Moscow conference | before the run's chapters' span; the calendar has the Moscow meeting: not yet cited |
| 126 | end of May 1961 | the Soviet submarines leave Vlorë | Soviet thread: not yet cited |

## Persons with no name entry

Tian Jiaying, Hu Qiaomu, Wang Renzhong, Zhang Pinghua, Deng Zihui, Zhang Jingfu, Du Runsheng, Wu Mingyu, Han Guang, Zhou Yang, He Qifang, Lin Mohan, Jiang Nanxiang, Yao Yilin, Ye Jizhuang, Xi Zhongxun, Yang Shangkun, An Ziwen, Pang Xianzhi, Liao Luyan, Zhao Ziyang, Wu Zhipu, Liu Jianxun, Wang Guangmei, Liu Xiao, Manush Myftiu, Enver Hoxha, Gu Mu, Lei Renmin, Zhang Guohua. Named in `c`, not tagged. Proposed for Part III: Tian Jiaying, Hu Qiaomu, Yao Yilin, Zhou Yang, Yang Shangkun, Deng Zihui, Wang Guangmei, Hoxha.

## Doubts

- The dating of the speeches of the Canton conference (Liu and Zhou on investigation: Mar. 15 by Pang Xianzhi, Mar. 19 by the collection of Liu's speeches) and of the Handan meeting (Sept. 27, the calendar Sept. 26) is a Check.
- The book's account of the Dec. 1960 grain decision (Dec., "at some point") and of Zhou's flight (the end of the month; he was in Burma Jan. 2–9) leaves the day open; both entries are month-dated with `at`.
- MacFarquhar reads the Cultural Revolution's sources against the post-Mao ones; entries from those say so in `c` ("by Cultural Revolution accounts").
- Several same-month, same-thread entries are flagged by `patch-check` as possible duplicates ("one event?"): they are distinct (the provinces' meetings on the urban population, the investigations of April–May, the programmatic articles of June 19); the merge will want `./bib resolve ID --take keep` on them.
- The card's title carries "vol. 3"; the A–Z form is "*The Origins of the Cultural Revolution, vol. 3: The Coming of the Cataclysm, 1961–1966* (1997)".

## Leads

National / Foreign: *Peking Review* 1961, Nos. 4 and 10 (the plenum's communiqué and resolution; the ghost stories), cited by the book's notes at pp. 15, 21–22; *Qi Qian Ren Dahui Ziliao*, *Zhonggong Dangshi Jiaoxue Cankao Ziliao* vol. 23 (the texts of the 1960–61 directives: the Twelve Articles, the 3 Dec. steel directive, the nine methods of June 16, the June 28 circular, Li Fuchun's plenum speech, pp. 434–45): where to read the documents themselves; the *Jianguo yilai Mao Zedong wengao* vol. 9 (pp. 421–29) and the *Chen Yun wengao* (1956–62) for Chen Yun's speeches of May 30–31, 1961. The Canadian and Australian grain contracts (International Wheat Council papers Nos. 2 and 7).

## Audit of run 1 (Opus, Nov. 17, 2026)

The copy re-fetched and read against the text layer and page images (offset −16 confirmed at pp. 1, 11, 137; notes at PDF 495 = 479). Verdict: not fit to merge until the notes pass is redone; the entries' fixes below are in the patch.

**Entries, a sample of 30** (pp. 2–51 and 63, 81, 121–131): 10 clean; 20 with at least one error: 9 bundles of several acts or days in one entry (a letter and its reply, Feb. 27 and Mar. 8; a meeting and the next day's; five leaders' investigations in one, Apr.–July), 6 Names lines naming persons not in `c`, 4 `at:` not by the rule (late as "after the 20th", early as "before the 11th", mid as "before the 21st", "after Canton" as after Mar. 20), 5 duplicates of entries in the Zhou patches, 1 interpretation in `c`, 1 misdated (Mao's consent to American grain through France, put on May 30; note 29 has it at Lushan, Aug.–Sept.). Fixed in the patch: 19 new entries split off or made from mis-hung cites (claimed in the ledger), 26 `c` trimmed or rewritten (src hashes remade), 16 Names and tag corrections, 10 `at:` set by `loose.at_for` or the season, curly quotes straightened.

**Cites, all 53; checks, all 6:** 41 held (11 of them in part, the parenthetical naming the part); 3 cut or replaced by a new entry (Oct. 19, the Standing Committee: the book does not treat it; Apr. 26 and Jan. 26, 1962: the pages bear on another act of the day, now entries); 2 moved (Aug. 13 to the Wall's own entry; July 14, 1960 to the Beidaihe conference's opening, with a Check of the book's July 15); the rest not read line by line (pp. 133–134, 142). Checks: 4 held, 1 dropped (Oct. 24: no difference), 1 reworded as the variant it is (the Stalin wreath laid on arrival).

**Duplicates, a sample of 20:** 11 are one event with another entry: 2 in the tree (Sept. 15, 1961, the higher-schools regulations: `cal.1961-09-15.china-leadership-2`; Oct. 17, 1961, Khrushchev's report: `cal.1961-10-17.berlin-and-vienna`), 9 in the Zhou patches (Dec. 3, 1960; Jan. 2, Mar. 19, Mar. 23 (this patch's March letter on investigation), Apr. 28, June 19, July 6, Oct. 15 (this patch's mid-October delegation), 1961; Jan. 17, 1962). This run claimed first in the ledger for most; the Zhou chronology dates them more closely. At the merge: the Zhou patches first, then `./bib combine` each pair, the Zhou or tree entry kept.

**The notes pass (15 pages: 11, 12, 23–27, 41, 49–51, and the timetable at 144–145):** not acceptable under R35–R38. (1) Anchors wrong in runs: ch. 2 nn. 18–25 each carry the next note's items (the *New York Times* of note 18 lost), ch. 3 nn. 78–84 likewise. (2) Items missing: about a fifth to a third of a note's items (ch. 1 n.8 Liao Gailong and *Song Renqiong Huiyilu*; n.9 the Guangdong teaching materials; n.12 *Gansu Sishi Nian*, Klein & Clark; ch. 3 n.11 Informant C, an interview; n.12 Zhang Xixian; n.18 Thompson, *Report from Xunwu*; n.74 three of four items; n.76 two of four; the timetable's five sources, p. 145, none). (3) No document is a row: the directives, letters and speeches the notes give (the Dec. 3, 1960 directive, the Twelve Articles, Li Xiannian's letter of May 17, Liu's speeches) stand only as their collections; the press as the paper, not the day's issue. (4) No edge carries `pin`, the page the note cites (0 of 1,035). (5) The To-check lines give works as text, not cards (R53), and only the first five to eight items of a page's notes. (6) Witness rows: garbled names ("sichtian"), titles missing ("CCP CC Party History Research Centre"), years known but "undated", a card ignored (Lewis & Xue, *China Builds the Bomb*). The notes pass is to be redone for every page of the run, from the page images, before the patch merges.

**The card:** the series cites a multi-volume work by one card with the volume in the pinpoint (Gibbons, the nianpu, *Prezidium*; works.py STYLE 9). Recommended: `w.macfarquhar-origins-of-the-cultural` as the set (title *The Origins of the Cultural Revolution*, `paren: 3 vols.`, year 1974–97, `n` naming the three volumes and their years), cited "III, 11", edges anchored "III, 11 n.3a" (R35), and Origins I and II in the notes as edges to the same card (`pin: 'II, 323'`) rather than witness rows. The id stays. The run's rework is the time to make the change.
