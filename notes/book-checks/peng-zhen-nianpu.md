# *Peng Zhen nianpu*, vol. 4 (1960–1978)

## Run 1, 1960–69 (batch 15b; reader of Jan. 6, 1960 to Dec. 31, 1969; patch `inbox/2026-11-20-b15b-pengzhen-1.yaml`, witnesses `inbox/witnesses/2026-11-20-b15b-pengzhen-1.yaml`)

**The copy.** *Peng Zhen nianpu (1902–1997)*, vol. 4 (一九六〇—一九七八), 'Peng Zhen zhuan' Bianxiezu 《彭真传》编写组, Zhongyang wenxian chubanshe 中央文献出版社. Drive `1Ow55z8o5B_Fhci7CWUbosivTbm-BuHDs`: an image scan of 526 PDF pages, simplified characters, no text layer. There is no copyright page in the scan. The year (2012) comes from the National Diet Library's record of the set (Aug. 2012, 5 vols., ISBN 978-7-5073-3572-9). The back cover of vol. 4 gives ISBN 978-7-5073-3573-6, "全5卷", 300.00 yuan.

The scan was OCR'd here (`tesseract -l chi_sim`, 200 dpi from `pdftoppm`, `OMP_THREAD_LIMIT=1`, one file a page). Every name, figure and date used was checked on a crop of the page image where the OCR was in doubt.

**OCR faults to watch.** The OCR must not be trusted for a date or a figure without the image:
- "S月", "s月" and "S$日" for 5;
- "工日" and "1L日" for 1日;
- "25S日" for 25日;
- "8 月56 日" for Aug. 6;
- "人", "和" or "会" for the △ mark;
- "芯真", "茧真", "形真" and "死真" for 彭真.

Names were misread too, among them:
- 胡绳 as 妆强 or 胡强;
- 萧华 as 靖华 or 痕华;
- 曹荻秋 as 曹获秋;
- 埃戈姆 as 挨蕊姆;
- 萧望东 as 痕望东;
- 林彪 as 林虎 or 林崩.

All these were settled on the images.

**The map.** The printed page is the PDF page − 4. PDF 5 is p. 1 (the contents page is unnumbered), PDF 508 is p. 504 and PDF 526 is p. 522. The year headings ("1960年 五十八岁" and so on) begin on these printed pages:

| Year | Printed page |
|---|---|
| 1960 | 1 |
| 1961 | 90 |
| 1962 | 166 |
| 1963 | 237 |
| 1964 | 313 |
| 1965 | 384 |
| 1966 | 458 |
| 1967 | 494 |
| 1968 | 499 |
| 1969 | 503 |
| 1970 | 505 |

The running heads agree with the folios. The book marks a further item of the same date with △.

**The card.** `w.peng-zhen-nianpu-1902` is a new card (`./bib works new`) for the set: 5 vols., the editors as printed, 2012. It is cited by volume and printed page, "IV, 123", as `w.zhou-enlai-nianpu-1949` and `w.deng-xiaoping-nianpu-1904` are cited.

**Pages read.** Pages read: IV, 1–504 (PDF 5–508), every dated item from Jan. 6, 1960 to Dec. 9, 1969, in the book's order. The items of Jan. 2–5, 1960 fall before the calendar's span. Peng's fall is covered at IV, 478–486 (Apr.–May 1966). After it the book is a record of the case against him: the case group, the questionings, the struggle meetings, and the Qincheng prison from July 15, 1968. That record was entered to the end of 1969 as the brief asks.

**Entered.** 1,329 new entries, all in thread `china-leadership`, `polity:prc`:

| Year | Entries |
|---|---|
| 1960 | 136 |
| 1961 | 147 |
| 1962 | 151 |
| 1963 | 188 |
| 1964 | 236 |
| 1965 | 270 |
| 1966 | 134 |
| 1967 | 38 |
| 1968 | 23 |
| 1969 | 6 |

- 1,017 entries carry `place:`. 662 carry a time: a band with `time_zone: Asia/Shanghai`, or the zone of the place abroad: Moscow, Pyongyang, Hanoi (`Asia/Bangkok`), Jakarta.
- Visibility:
  - 877 entries are `vis:only:prc`, with "Made public: 2012.";
  - 36 carry `vis:only:prc+<polity>`, for talks with foreign governing parties or envoys;
  - 416 carry no ruling: rallies, receptions, banquets, airport meetings, published speeches and articles, NPC sessions.
- 1,330 `cite` ops go on entries already in the tree or pending. Most are entries from the Mao, Zhou, Liu and Deng chronologies, the Yang Shangkun diary, Wu Lengxi, MacFarquhar and *Tiandi fanfu*.
- 39 `variant` ops (unit A), listed under the doubts.
- 0 checks.
- 28 `edit` ops set the band or the place on cited entries that lacked them.
- 11 `place-key` ops: huairou, houma, linfen, quwo, yuncheng, sinuiju, ha-long-bay, hon-gai, surabaya, tangshan, fangshan.
- 8 witness rows.
- 1 card.

`./bib patch-check` reports 0 errors, and `./bib fields --patch` 0 findings. Every add is claimed in the ledger, with claims equal to adds (1,329). See links point only backward in time.

**Passed over (R18).** Seven items:
- IV, 1: Jan. 2, 3 and 5, 1960, before the span (R1).
- IV, 202: June 21, 1962. The Korean delegation meets the families of Chinese People's Volunteers who died; Peng is not named, so it is no act of his.
- IV, 203: June 28, 1962. Peng is listed on Long Yun's funeral committee. This is a membership only; his condolence is cited on July 2.
- IV, 290: early August 1963. Floods in five provinces, given as context, with no act.
- IV, 364: Oct. 16, 1964. The TASS report of Khrushchev's removal, given as context, with no act of Peng's.

Nothing else was passed over. Later acts named inside an item ("十二日，中央批转…", "二十九日，毛泽东批示…") were entered on their own days, with backward `See` links, or cited where the act is already in the tree.

**The notes.** The volume's footnotes gloss persons (their posts), terms and events: the Changguanlou review of 1961, the Caolanzi prison decision of 1936, the "three-door" cadres, the 1979 withdrawal of the army forum summary, the 1981 resolution on the May 16 Circular. They name no archival source. The glosses that bear on an act are kept in the entries as "(the editors' note: …)".

**Witness rows.** Eight speeches of Peng's are printed, whole or in part, in *Peng Zhen wenxuan* 《彭真文选》, as the nianpu says. Each is a row with `kind: speech`, `form: print` and `open: not held`. The dates and pages:

| Date | Nianpu page |
|---|---|
| July 8, 1961 | IV, 139 |
| Apr. 15, 1962 | IV, 188 |
| May 28, 1962 | IV, 198 |
| July 22, 1962 | IV, 206 |
| Dec. 18, 1962 | IV, 232 |
| Apr. 2, 1965 | IV, 412 |
| Sept. 23, 1965 | IV, 439 |
| Dec. 10, 1965 | IV, 453 |

The nianpu names many other documents with a date: Peng's reports and letters, and the Center's and the Peking committee's notices. It gives no place for them, and they were not made rows.

**Leads.**
- (1) A card for *Peng Zhen wenxuan* (Renmin chubanshe, 1991), and the eight speeches read against their entries.
- (2) The *Jianguo yilai Mao Zedong wengao* for Mao's comments on Peng's papers. Many are cited here only from the nianpu: Feb. 1966, the outline and the 7,000-cadres speech; Apr. 1, 1966, the army forum summary; Dec. 25, 1965, the Secretariat minutes.
- (3) *Peng Zhen zhuan* for the case years, 1966–69.
- (4) The Peking municipal committee's documents of 1960–66: its reports to the Center of Apr. 6 and Apr. 8, 1966, and the "four clean-ups" speeches criticized in July 1966.

**Doubts.**
- (1) The 39 variants, where this book disagrees with the entry it cites. These are the date and hour cases (IV page in brackets):
  - Mar. 7 against Mar. 8, 1960 (8);
  - the hour of the telephone conference of Mar. 22, 1960 (10);
  - June 17 for the Kozlov talks, June 1960 (35);
  - June 27 for the editorial, June 1960 (42);
  - Mar. 4, 1961, Canton (109);
  - July 11, 1961 (139);
  - Aug. 10–14, 1961 (146);
  - the afternoon of July 22, 1962 (206);
  - Aug. 5, 1962 (209);
  - the afternoon of Sept. 25, 1962 (216);
  - Jan. 9, 1963 (238);
  - noon of Feb. 15, 1963 (247);
  - June 23, 1963 (279);
  - July 13, 1963 (283);
  - Sept. 5, 1963 (289);
  - Oct. 26, 1963 (296);
  - Nov. 21, 1963 (300);
  - Apr. 5, 1964 (326);
  - Feb. 22, 1965 (400);
  - June 19, 1965 (422);
  - July 17, 1965 (426);
  - Aug. 6, 1965 (429);
  - Dec. 8–16, 1965 (452);
  - Feb. 20–Mar. 1, 1966 (470–471);
  - Mar. 26, 1966 (476);
  - Apr. 16, 1966 (482).

  The rest are figures and persons:
  - 3,200,000 at the rally of May 20, 1960;
  - 500,000 on Feb. 18, 1961;
  - 100,000 on Apr. 21, 1961;
  - Khrushchev's 1 hour 40 minutes and Deng's 40 minutes, Nov. 1960;
  - who presided (June 30, 1960; May 5, 1962; Dec. 24, 1964);
  - who spoke, Sept. 8, 1962.
- (2) The Indonesian names of May–June 1965 are given as printed, with the characters. Their Latin forms are not settled:
  - the "埃戈姆" academy near Bogor;
  - Major 明曼贡 of the Gotong Royong parliament (perhaps Mursalin Daeng Mamangung);
  - 萧玉灿;
  - Rear Admiral 苏博诺.

  So too 布特·平姆 of the Khmer People's Revolutionary Party (Nov. 30, 1965) and David 大卫·迪芬培克 (July 31, 1965).
- (3) Jan. 8, 1966. The Deng chronology has Peng and Li Fuchun at both talks with Luo Ruiqing. This book has Dec. 31 with Yang Chengwu and Jan. 3 with Li Fuchun. It is cited, not made a variant.
- (4) Apr. 4, 1966. Peng is "at Deng's" in the evening. The Deng chronology has Deng at Yan'an that afternoon (`cal.1966-04-04.china-leadership-6`). The two can both stand, so no check was made.
- (5) Mar. 4–8, 1966: this book's meeting of the Center's work group on Luo Ruiqing. It is cited on `cal.1966-03-04.china-leadership` (forty-two cadres, to Apr. 8). The two may be different bodies.
- (6) An early ledger claim, `cal.1961-03-19.china-leadership` "the speeches", from another patch (b15b-origins3-1), was not in the tree when Peng's Mar. 19, 1961 group speech was added. The two may overlap.

**Run 2 starts** at IV, 505 (1970, "9月上旬"). It runs to the end of the volume (1978) as far as the calendar's span (1974) requires.

**Persons in these entries with no name entry** (by frequency; a Part III entry proposed for the first):
- Liu Ren 刘仁, Zheng Tianxiang 郑天翔, Wan Li 万里, Deng Tuo 邓拓, Yang Shangkun 杨尚昆;
- Wu Lengxi 吴冷西, Liu Lantao 刘澜涛, Xu Zirong 徐子荣, An Ziwen 安子文, Liu Ningyi 刘宁一, Song Renqiong 宋任穷;
- Gu Mu 谷牧, Guo Moruo 郭沫若, Yang Chengwu 杨成武, Li Xuefeng 李雪峰, Yu Qiuli 余秋里, Wu Han 吴晗;
- Zhao Fan 赵凡, Xu Liqun 许立群, Fan Jin 范瑾, Zhang Jieqing 张洁清, Li Qi 李琪, Song Shuo 宋硕;
- Zhou Yang 周扬, Zhang Linzhi 张霖之, Xiao Hua 萧华, Hu Yaobang 胡耀邦, Lu Ping 陆平, Hu Sheng 胡绳;
- Hu Qiaomu 胡乔木, Lin Feng 林枫, Chen Kehan 陈克寒, Cheng Zihua 程子华, Tian Jiaying 田家英, Wu Xiuquan 伍修权;
- Ping Jiesan 平杰三, Wang Renzhong 王任重, Chen Shutong 陈叔通, Cao Diqiu 曹荻秋, Lin Mohan 林默涵, Liu Zhijian 刘志坚;
- Peng Peiyun 彭珮云, Qi Benyu 戚本禹, Zhang Wensong 张文松, Xu Bing 徐冰, Jia Xingwu 贾星五, Feng Jiping 冯基平;
- Zhang Dingcheng 张鼎丞, Wang Heshou 王鹤寿, Liu Lanbo 刘澜波, Tao Lujia 陶鲁笳, Zhang Zhizhong 张治中, Huang Yanpei 黄炎培;
- Li Zongren 李宗仁, Xiao Wangdong 萧望东, Soong Ching-ling 宋庆龄, Nie Yuanzi 聂元梓, Qi Jinghe 齐景和.

About 350 others appear in all, among them many foreign visitors.

**After the Tiandi fanfu run 5 merge (Nov. 21).** Two adds were folded on the lead's word, and their ledger claims released:
- `cal.1965-11-28.china-leadership-8`, the reprint meeting at the Great Hall, is now a cite on `cal.1965-11-28.china-leadership-7`, the same meeting. The Dec. 2 *Guangming ribao* entry now points there.
- `cal.1965-12-23.china-leadership-4`, the talk alone with Mao at Hangzhou, is now a cite on `cal.1965-12-22.china-leadership`, whose text already carries the Dec. 23 talk. The Jan. 19, 1966 entry now points there.

`cal.1965-11-28.china-leadership-7` already had `place: peking`; neither book gives an hour, so no edit was made.

## Audit of run 1, Nov. 20–21

Opus audit of patch `2026-11-20-b15b-pengzhen-1` (IV, 1–504, Jan. 6, 1960–Dec. 9, 1969), its witness file and the card. The copy was fetched again into a new directory. The OCR: PDF 1–172 twice (tesseract `chi_sim --psm 6`, 200 and 300 dpi); PDF 173–508 once at 300 dpi, the doubtful names, words and days read on crops of the page image. (The default page segmentation the reader used at 200 dpi scrambles these two-column-free pages badly; `--psm 6` reads them in order.) Nothing merged or committed. Copy, images and text deleted after. The original patch, witness file, `works/p.yaml`, this file and the patch's ledger lines are kept in the auditor's scratch. The tree changed during the audit (Chen Yi run 3 and Westad run 1 merged): the pool was rebuilt and every edit base checked again at the end.

**The copy and the card.** The map holds: printed = PDF − 4. There is no copyright page in the scan. The title page gives 《彭真传》编写组 and 中央文献出版社. The back cover gives ISBN 978-7-5073-3573-6 and 定价 300.00元 (全5卷). No 内部发行 mark is on the cover or the title page. The year 2012 (NDL) stands, an open sale. The card's note now says so. The cite form "IV, 123" stands.

**Visibility (whole patch, by class and reading).** The reader's line was right in kind: Secretariat, Politburo and Peking committee sessions, inner reports and letters, inspections and the case years closed; rallies, receptions, banquets, airports, NPC sessions and published speeches public. Faults: 20 of 1,329 (1.5 percent).
- 18 public acts were closed:
  - courtesy calls and farewells of ambassadors and visitors with no substance given (Ghana, Romania twice, Albania, France, Algeria, Syria, Burma, Henry Muli; Aziz; the Albanian prosecutor-general; the call on Aidit at Jakarta; the Korean and Indonesian party delegations met);
  - the United Front Department's banquet (Aug. 28, 1960);
  - the Albanian Ambassador's leave-taking (June 6, 1961);
  - the condolence for Zhou Baozhong (Feb. 25, 1964);
  - Ai Siqi's funeral committee (Mar. 22, 1966).
- 2 closed acts were public or wrongly ruled: talks with substance with a governing party's men, now `+indonesia` (the PKI study delegation, July 26, 1965) and `+albania` (the Interior Ministry delegation briefed, Sept. 30, 1965).
- R27: the nianpu names *Peng Zhen wenxuan* (1991) as printing eight of the speeches. Three closed adds now read "Made public: 1991 (*Peng Zhen wenxuan*, as the nianpu gives it)". Two cited tree entries that said 2001 and 1992 (Dec. 18, 1962; Sept. 23, 1965) now say 1991, by edits.

**Duplicates (all 1,329 adds, by script).** Each add was scored against every entry of its day, the days either side and the spans covering it, in the tree and the pending inbox (TF-IDF on English words and character bigrams, shared name tags). The 430 best pairs were read, and the doubtful ones on the page. 38 adds were wholly the calendar's event (2.9 percent) and are now cites, their claims released. Examples:
- receptions, rallies and performances held in Zhou's, Liu's or Yang Shangkun's entries (Aug. 15 and 22, 1960; Oct. 30, 1960; May 1, 1961; Sept. 25, 1961; Jan. 1, 1964; Apr. 30, 1964; June 26, 1964; July 14, 1964; Oct. 6, 1964; Nov. 1, 1964; Nov. 6, 1964; Jan. 26, 1965; July 22, 1965 twice);
- the Moscow delegation's meetings in the Yang diary (Oct. 3, Oct. 9, Nov. 8, 1960);
- Secretariat and Center acts already in (Sept. 11, 1961; May 4, 1961; the Apr. 9 and Aug. 29, 1960 meetings at Deng's);
- the WFTU council (June 5–9, 1960);
- the Shunyi–Huairou inquiry (Apr. 1961);
- the 1963 tour (now cited on `cal.1963-05.china-leadership-5`, which an edit re-dates to May 15–June 14);
- Mao's Tsinghua struggle meeting of Apr. 10, 1967 (Peng among the cadres made to stand with Wang Guangmei);
- the CPPCC session of Nov. 17, 1963 and the Peking victory meeting of May 1, 1961, both held in Chen Yi run 3's merged entries.

Three of the 38 carry a variant of the day: the Secretariat's 341st meeting (Nov. 22 against Nov. 21, 1962), Osman received (July 20 against July 21, 1965), and the NPC delegation's departure for Korea (Apr. 22 against the trip entry's Apr. 23, 1962). No id that `inbox/deferred.yaml` names was dropped. On June 16, 1962, the dinner was kept on `-7`, the id Chen Yi run 2's deferred cite names, and the afternoon meeting moved to a new `-8`.

**Sample (every sixth add of the original, 222).** Read on the page, the image where the OCR was in doubt. 6 were already folded as duplicates. Faults in about 30 others (14 percent), each class then swept over the whole patch:
- *One act an entry* (3 in the sample). Another man's act or a later day's act was folded into an add: Mao's reception of Goulart at Hangzhou inside the airport send-off of Aug. 18, 1961, and a dinner after a meeting. The sweep found 20:
  - 4 trimmed to cites on the tree's own entries (Mao, Jan. 16, 1962; Aug. 2, 1964; the Taoyuan forwarding, Sept. 1, 1964; Mao and Goulart, Aug. 18, 1961) and 1 on Mao's telegram (the JCP congress, Nov. 25, 1964);
  - 13 new adds, each claimed: July 24 and 26, 1963; Dec. 23, 1963 (two); Jan. 23, 1964; Oct. 7, 1964; Mar. 30, Apr. 1 and Apr. 29, 1965; and the second act of June 16, 1962, Sept. 15, 1963, Feb. 21, 1964 and Oct. 16, 1964.
  - Kept together: a tour day's sights, a meeting continued over its days, routing notes ("back to Peng Zhen").
- *Names and words from the OCR* (1): the Pyongyang gift of July 1, 1963 had 姜布源 for 姜希源 (Kang Hui-won), a hippopotamus for 河麂 (water deer) and seals for 海龟 (sea turtles). Fixed, and the new July 26 add with it. Every other name checked on a crop was right (陈鹏, 贝尔希奥, 朴金喆). Peng's own speech was left out of the coal conference of Jan. 27, 1961; restored.
- *Name tags and "Names:"* (13). Persons with a name key named in `c` were left untagged. Swept: 113 tags added, each in "Names:" (Mao 44, Aidit 9, Liu Shaoqi, Zhou, Stalin, Bo Yibo, Duan Junyi, Chiang Kai-shek, Khrushchev, Luo Ruiqing, Goulart and others).
- *Characters at first appearance*. Swept: 33 persons, 41 "Mao 毛泽东", 70 organs (全国人大, 国务院, 华北局, 北京大学, 公安部 and others).
- *Visibility* (3) and *duplicates* (6): above.
- *Working-note Checks*: 6 found in the patch (the reader reported none). 5 removed: whether two meetings were one (Apr. 9 and Aug. 29, 1960; Apr. 17, 1961; Aug. 1, 1960, all settled above), a name's Czech form, whether a banquet was reported, the day of the plane talk. 1 kept (Oct. 25, 1961: the visits' days).
- *Dates, clock times, bands, places*: right throughout the sample. No 正午 in the adds.

**Cites (all 1,330 by script, about 60 read).** The days agree with their entries but for those carrying variants. **R25a on the cites:** 265 cited single-day entries lacked the hour or part of the day the page gives, and the reader had made 28 edits. 252 edits were added: bands as the patch's own, clock hours as `time`, the zone by the place, and `place: peking` where the cite names a Peking building. 13 were left: ambiguous words ("three afternoons", "toward evening") or an entry with no place and a scene abroad. After the merges of the night, 7 were dropped because the tree now has the hour. 8 equal Chen Yi run 4's identical edits. The one that differs (the Tanzania treaty signing, Feb. 20, 1965: the nianpu has the morning, Chen Yi the afternoon) is a variant instead.

**Edits (the reader's 28).** 4 bases were stale: 3 dropped, since the tree already holds the same band (Sept. 15 and Oct. 28, 1962; Jan. 1, 1963), and 1 rebased (July 28, 1962).

**Variants (the reader's 39).** All are real disagreements. 15 sat on a dateline unit A ("Moscow.", "Peking.") and are moved to the unit that holds the fact (B; C for Nov. 26, 1960). Added: the Dec. 31/Jan. 3 talks with Luo Ruiqing (doubt 3), Nov. 21/22, 1962, the Korea departure, Osman, and the Tanzania signing.

**Witnesses (8 rows).** Right in kind: the nianpu names where each speech is printed. The apostrophes had been lost in eight places (committee's, Peking's, history's, one's, unions', conference's, world's) and are restored. **Place keys.** `sinuiju` named no entry's place: it is now on the Apr. 23, 1962 arrival (`[sinuiju, pyongyang]`).

**Rulings on the reader's doubts.**
- (1) The variants stand, the units corrected.
- (2) Names as printed, with characters: right.
- (3) A variant, not a bare cite: who was at which talk is a disagreement.
- (4) Both stand.
- (5) The cite stands. The work group's meeting is Mar. 4–8; the tree entry runs to Apr. 8.
- (6) `cal.1961-03-19.china-leadership`, claimed by b15b-origins3-1, is still not in the tree. Run 1's Mar. 19, 1961 add stands, and the merger should look at the two together if that claim lands.

**After the audit.** 1,304 new entries:

| Year | Entries |
|---|---|
| 1960 | 126 |
| 1961 | 139 |
| 1962 | 150 |
| 1963 | 190 |
| 1964 | 232 |
| 1965 | 267 |
| 1966 | 134 |
| 1967 | 37 |
| 1968 | 23 |
| 1969 | 6 |

- 987 entries carry `place`, 41 a clock `time` and 597 a band.
- Visibility: 867 `vis:only:prc`, 24 `+polity`, 413 public. "Made public: 2012" on 888, 1991 on 3.
- 1,369 cites, 278 edits, 44 variants, 1 check, 11 `place-key`, 8 witness rows.
- Ledger: 38 claims released, 13 made (and one re-made under corrected words); 1,304 claims, equal to the adds.
- `./bib patch-check`: 0 errors (2,579 warnings, all of the merge's "duplicate?"/"also holds" kind and 2 n-only edits that change a Made public year). `./bib fields --patch`: 0 findings. `./bib check`: 0 errors.
- Fit to merge.

**For run 2 (1970–74), the rules this audit found needed** (on top of the Chen Yi audits' twelve):
1. OCR with `--psm 6` (300 dpi). Read every foreign name, every noun list (gifts, animals, places) and every time word in doubt on the image.
2. One act an entry: no "on the 13th …", "that afternoon Mao …" inside an add. Another man's act or a later day's act is its own entry, or a cite where the tree holds it. An evening dinner or a second meeting at another hour is its own entry.
3. Script every add against the tree and the pending inbox, the day either side and the spans included, and read every pair whose text overlaps. A delegation's meeting, a reception, a rally or a performance that a Zhou, Liu, Mao, Deng or Yang entry holds is a cite.
4. R25a on cites by script: every cited single-day entry without an hour takes the page's band or hour by an edit. Check it against the other pending patches' edits.
5. A meeting with an envoy or a visitor with no substance given is public. Substance with a governing party's or a government's man is `vis:only:prc+<polity>`.
6. Where the nianpu says a speech or a document is printed in *Peng Zhen wenxuan* or elsewhere, "Made public:" is that printing's year.
7. Tag and list every person named in `c` whose key exists (Mao and Zhou by surname too). Put characters at the first appearance of every person and organ.
8. No working notes in "Check:".
9. A variant goes on the unit holding the disputed fact, never on a bare dateline.

**For the merger.**
- (1) Every add carries the "duplicate?" flag: resolve `--take keep`. Those read and kept as distinct from a near entry:
  - `cal.1960-10-17.china-leadership-7`, `cal.1960-10-18.china-leadership-8` (the delegation hears the secretariat's day; the secretariat's sitting is the tree's);
  - `cal.1961-05-28.china-leadership-7` (a meeting at Zhou's, a separate item from Deng's meeting cited the same day);
  - `cal.1961-04-17.china-leadership-8`, `cal.1962-09-08.china-leadership-10`, `cal.1964-10-04.china-leadership-12`, `cal.1965-09-30.china-leadership-12` (Peng's own meetings with Souphanouvong, Aziz, Phạm Văn Đồng and the Albanian delegation; Zhou's are separate);
  - `cal.1963-12-23.china-leadership-10` (the meeting; the banquet is the tree's);
  - `cal.1965-03-20.china-leadership-13` (Peng's condolence; Zhou's the same evening);
  - `cal.1966-05-04.china-leadership-8` (told only inside Liu's entry);
  - `cal.1965-11-28.china-leadership-10`, `cal.1966-03-18.china-leadership-6`.
- (2) `cal.1964-09-08.china-leadership-5` (Peng at the airport for Li Xiannian's delegation) and Chen Yi run 4's pending add `cal.1964-09-08.china-leadership-9` are one event. This patch keeps its add. Chen Yi run 4's auditor or the merger should make theirs a cite here.
- (3) The edit on `cal.1963-05.china-leadership-5` re-dates it to May 15, 1963 (`when: May 15–June 14`, `at` unset). Check that the merge files it on the new day.
- (4) 8 edits on entries that Chen Yi run 4 also edits set the same values or different fields (Apr. 30, June 4, June 11, July 14, Oct. 5, 1964; Dec. 20, 1964; Feb. 4, Apr. 6, 1965). They should merge clean; if the merge flags them, take either.
