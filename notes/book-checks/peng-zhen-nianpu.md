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

**Entered.** 1,331 new entries, all in thread `china-leadership`, `polity:prc`:

| Year | Entries |
|---|---|
| 1960 | 136 |
| 1961 | 147 |
| 1962 | 151 |
| 1963 | 188 |
| 1964 | 236 |
| 1965 | 272 |
| 1966 | 134 |
| 1967 | 38 |
| 1968 | 23 |
| 1969 | 6 |

- 1,019 entries carry `place:`. 662 carry a time: a band with `time_zone: Asia/Shanghai`, or the zone of the place abroad: Moscow, Pyongyang, Hanoi (`Asia/Bangkok`), Jakarta.
- Visibility:
  - 879 entries are `vis:only:prc`, with "Made public: 2012.";
  - 37 carry `vis:only:prc+<polity>`, for talks with foreign governing parties or envoys;
  - 416 carry no ruling: rallies, receptions, banquets, airport meetings, published speeches and articles, NPC sessions.
- 1,328 `cite` ops go on entries already in the tree or pending. Most are entries from the Mao, Zhou, Liu and Deng chronologies, the Yang Shangkun diary, Wu Lengxi, MacFarquhar and *Tiandi fanfu*.
- 39 `variant` ops (unit A), listed under the doubts.
- 0 checks.
- 28 `edit` ops set the band or the place on cited entries that lacked them.
- 11 `place-key` ops: huairou, houma, linfen, quwo, yuncheng, sinuiju, ha-long-bay, hon-gai, surabaya, tangshan, fangshan.
- 8 witness rows.
- 1 card.

`./bib patch-check` reports 0 errors, and `./bib fields --patch` 0 findings. Every add is claimed in the ledger, with claims equal to adds (1,331). See links point only backward in time.

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
