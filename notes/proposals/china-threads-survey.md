# China: leadership — a survey of cutting lines

Scratch analysis, Nov. 22, 2026 (Sunday). Read-only; regex over lists/cal/*.yaml (scripts beside this file). Base: the 26,320 entries with `thread: china-leadership`; where noted, also the 1,478 `thread: china` and the entries with `also: [china-leadership]` or `also: [india-and-china-cultural-revolution]` (28,423 in all touching the China threads).

## 1. What the bucket is made of

The first work cited in `n`, the source the entry was read from. The bucket is a set of digested daybooks: one diary and a dozen nianpu give about 70 percent of it.

| first source | entries |
|---|---:|
| `w.yang-shangkun-riji` | 4679 |
| `w.chen-yi-nianpu` | 2405 |
| `w.zhou-enlai-nianpu-1949` | 2172 |
| `w.zhou-enlai-waijiao-huodong` | 1778 |
| `w.zhou-enlai-nianpu-1949-2020` | 1643 |
| `w.zhu-de-nianpu-xinbian` | 1359 |
| `w.peng-zhen-nianpu-1902` | 1304 |
| `w.zedong-mao-zedong-nianpu` | 1276 |
| `w.yang-jisheng-tiandi-fanfu` | 1229 |
| `w.jianguo-yilai-mao-zedong` | 1057 |
| `w.macfarquhar-maos-last-revolution` | 1021 |
| `w.deng-xiaoping-nianpu-1904` | 945 |
| `w.pu-weihua-zalan-jiu-shijie` | 698 |
| `w.yang-jisheng-mubei` | 661 |
| `w.macfarquhar-origins-of-the-cultural` | 577 |
| `w.shaoqi-liu-shaoqi-nianpu-chronology` | 575 |
| `w.peng-dehuai-nianpu` | 465 |
| `w.chen-yun-nianpu-xiuding` | 420 |
| `w.liu-jixian-ye-jianying-nianpu` | 313 |
| `w.dikotter-maos-great-famine` | 282 |
| `w.teiwes-tragedy-of-lin-biao` | 232 |
| `w.lengxi-shinian-lunzhan-1956-1966` | 218 |
| `w.jianguo-yilai-zhongyao-wenxian` | 170 |
| `w.zhonghua-renmin-gongheguo-waijiao` | 151 |
| `w.zhonghua-renmin-gongheguo-waijiao-2001` | 138 |

By year (china-leadership): 1960 3427, 1961 3280, 1962 2613, 1963 2847, 1964 3213, 1965 3256, 1966 3139, 1967 2332, 1968 1235, 1969 956, 1970 22. 869 entries are dated by year only, 2,094 by month only.

## 2. Episodes: the named meetings, campaigns, documents and affairs

Candidates from (a) the brief's list, (b) capitalized multi-word phrases, quoted slogans, numbered formulas and 《》 titles by frequency (`phrases.py`, `phrases.json`), (c) general knowledge of the period. Each is a regex (English and Chinese forms; `lexicon.py`) plus a date window. `all` = entries matching anywhere in 1960–70; `win` = matches inside the window; `CL` = share of `win` already in china-leadership; `CR` = how many carry `also: india-and-china-cultural-revolution`. Density: entries per month across the window, one character a month (blank = none).

Frequency check (phrases, entries naming them): Sixty Articles 53; Seven Thousand Cadres Conference 36–40; Tenth Plenum 28–36; Eleventh Plenum 32–36; Twelfth Plenum 30–34; Ninth Congress 86; Twenty-three Articles 25–31; Ten Points 33; "four clean-ups" 72+; "five antis" 48; Third Five-Year Plan 45; third front 25+9; Three-Family Village 18; Hai Rui 39; Lei Feng 28; Red Guards 288+118; Cultural Revolution Group 113+63; Million Heroes 30; "February adverse current"/"counter-current" 17; "May 16" 12, May 16 Corps 6; 4·22 27. The named episodes are *small*: the sources name an episode in a few dozen entries and then record its days without naming it.

| candidate | window | all | win | first..last | CL | CR | density (per month in window) |
|---|---|---:|---:|---|---:|---:|---|
| Leap of 1960 (`leap-1960`) | 1960-01..1960-08 | 99 | 41 | 1960..1960-08-04 | 98% | 0 | `▄▃█▄▃▂▁▁` |
| Famine (`famine`) | 1959-10..1962-12 | 277 | 247 | 1960..1962-09-04 | 99% | 0 | `   ▂▃▃▃▃▃▁▂▃▇▃▇█▃▅▂▂▂▂▃▁▁▁▁▂ ▂▁▂ ▁ ▁   ` |
| Grain procurement and supply (`grain`) | 1960-01..1963-12 | 97 | 82 | 1960-01-23..1963-12-12 | 100% | 0 | `▁▂ ▂▁▂▂▁▁▃▃█▄▄▂▁▃▁▂▁▁▂▂ ▁▂▁ ▁ ▂▁    ▁       ▁▁ ▁` |
| Communist wind and the Twelve Articles (`rectify-communes`) | 1960-05..1961-02 | 288 | 123 | 1960..1961-02-27 | 97% | 0 | `▂▂▂▂▂▆█▆▇▃` |
| Beidaihe conference of 1960 (`beidaihe-1960`) | 1960-07..1960-08 | 489 | 150 | 1960-07..1960-08-27 | 100% | 0 | `█▆` |
| Soviet experts recalled (`soviet-experts`) | 1960-07..1960-09 | 150 | 25 | 1960..1960-09-27 | 80% | 0 | `█▆▆` |
| Ninth Plenum (`ninth-plenum`) | 1960-12..1961-01 | 38 | 20 | 1960-12-12..1961-01-27 | 100% | 0 | `▁█` |
| Year of investigation (`investigation-1961`) | 1961-01..1961-06 | 23 | 9 | 1961..1961-05-30 | 100% | 0 | `▅▅███ ` |
| Sixty Articles on the communes (`sixty-articles`) | 1961-02..1962-09 | 157 | 136 | 1961-02..1962-09-14 | 100% | 0 | `▂█▇▄▂▂▂▃▃▁▂▁▂▁▁▁▁▁▂▁` |
| Lushan conference of 1961 (`lushan-1961`) | 1961-08..1961-09 | 168 | 101 | 1961..1961-09-29 | 100% | 0 | `▅█` |
| Regulations of 1961: industry, higher education, science, arts (`articles-1961`) | 1961-06..1962-04 | 29 | 17 | 1961-06..1962-04-30 | 100% | 0 | `▆▆▆█ ▅▃   ▃` |
| Retrenchment and the urban sending-down (`retrenchment`) | 1961-05..1963-07 | 238 | 166 | 1961-05-17..1963-07-31 | 100% | 0 | `▃▅▁▁  ▁ ▄▆▇██▅█▁▁▃▃▃▂█▅▅▃▁▃` |
| Verdicts reversed (`verdicts-reversed`) | 1961-06..1962-12 | 44 | 23 | 1961-07-11..1962-09 | 100% | 0 | ` ▅ ▃   ▃▃▃▆█▃▅▃▃   ` |
| Seven Thousand Cadres Conference (`seven-thousand`) | 1961-11..1962-02 | 89 | 60 | 1961-11-16..1962-02-28 | 100% | 0 | `▂▃██` |
| Xilou conference (`xilou`) | 1962-02..1962-04 | 41 | 22 | 1962..1962-04-25 | 100% | 0 | `█▇▆` |
| Household contracting (`household-contracting`) | 1961-03..1962-09 | 442 | 198 | 1961..1962-09-15 | 100% | 0 | `▄▂▃▂▂▂▃▃▃▂▄▃▅▁▅▄▅█▂` |
| Panchen Lama (`tibet-panchen`) | 1960-01..1965-01 | 22 | 16 | 1960-01-25..1964-09-11 | 100% | 0 | `▃█    ▃ ▃  ▃▆     ▃ ▃▃      ▆ ▃                         ▃    ` |
| Yi–Ta flight (`yi-ta`) | 1962-04..1962-10 | 18 | 10 | 1962-04..1962-08-03 | 70% | 0 | `█▅▂ ▂  ` |
| Return to the mainland scare (`taiwan-1962`) | 1962-04..1962-08 | 248 | 21 | 1962..1962-07-16 | 67% | 0 | `▂▅█▂ ` |
| Sino-Indian war (`sino-indian-war`) | 1962-06..1963-03 | 515 | 176 | 1962..1963-03-30 | 60% | 0 | `▂▄▂▃▆█▅▅▃▃` |
| Peng Dehuais letter of 1962 (`peng-letter-1962`) | 1962-06..1962-11 | 11 | 3 | 1962-08..1962-09-06 | 100% | 0 | `  █▅  ` |
| Beidaihe conference of 1962 (`beidaihe-1962`) | 1962-07..1962-08 | 494 | 144 | 1962-07-12..1962-08-30 | 100% | 0 | `▄█` |
| Tenth Plenum (`tenth-plenum`) | 1962-08..1962-11 | 234 | 56 | 1962..1962-10-17 | 96% | 0 | `▅█▄ ` |
| Sino-Soviet polemic (`polemic`) | 1960-04..1964-11 | 1678 | 1171 | 1960..1964-11-30 | 88% | 0 | `▂▂▅▃▂▄▅█▃▂▂▂▂▂▂▂▂▂▄▄▃▂▁▂▂▂▃▂▁▂▂▃▃▃▃▃▂▃▃▅▂▃▂▃▂▄▃▄▄▂▂▂▃▂▃▄` |
| Border clashes of 1969 (`zhenbao`) | 1969-02..1969-12 | 217 | 84 | 1969..1969-12-31 | 89% | 22 | `▁█▂▁▁▁▂▄▃▂▂` |
| Geneva conference on Laos (`geneva-laos`) | 1961-04..1962-08 | 428 | 208 | 1961-04..1962-08-28 | 88% | 0 | `▄█▆▄▂▁▁▂▁▃▁▁▁▁▃▆▂` |
| Boundary treaties (`boundaries`) | 1960-01..1963-12 | 1203 | 598 | 1960-01-12..1963-12-26 | 89% | 0 | `▄▁▅█▅▃▄▄▄▄▂▂▅▂▂▂▂▁▂▂▂▄▁▂▂▂▂▂▃▂▂▂▂▄▄▅▄▂▄▄▂▂▂▂▂▃▃▂` |
| Zhou Enlais tour of Africa and Asia (`african-tour`) | 1963-12..1964-03 | 837 | 214 | 1963-12..1964-03-30 | 99% | 0 | `▇█▅▁` |
| Recognition by France (`france-1964`) | 1963-10..1964-03 | 225 | 46 | 1963-10-23..1964-03-19 | 91% | 0 | `▆▅▄█▆▂` |
| Second Afro-Asian conference (`afro-asian-1965`) | 1964-04..1965-11 | 361 | 220 | 1964-04-09..1965-11-04 | 94% | 0 | `▃▂▁▁▁▁▃▃▂▁▂▃▇▅█▁▅▃▂▁` |
| Indonesia, 1965 (`indonesia-1965`) | 1965-01..1966-06 | 546 | 191 | 1965-01-05..1966-06-29 | 84% | 0 | `▆▂▂█▇▆▄█▆▄▃▂▁▂▂▃▁▂` |
| Aid to Vietnam (`vietnam-aid`) | 1964-08..1969-12 | 1168 | 657 | 1964..1969-12-19 | 82% | 5 | `▄▄▃▂▂▂▄▅█▅▃▃▄▄▂▂▃▂▃▃▂▂▃▃▃▂▂▁▂▁▂▂▂▂▁▂▃▂▂▂▃▂▂▂▃▂▁▂▁▂▂▂▁ ▁ ▁▁▂▂▂▄▃ ▁` |
| Bomb (`nuclear`) | 1963-07..1969-12 | 335 | 238 | 1963..1969-12-12 | 87% | 8 | `▆▃▃ ▃▂▃▂▁▁▁▂▂▂▃█▄▂▂▂▂▂▄▂▂▃  ▁▁▁▂▂▁▃▁▂▂▂▃▂▁▁ ▁▁▂▄▂▂▁▁▁▂ ▂▁▁▁▂     ▃▁▁▁  ▁▁▃▂▂▁▂` |
| Socialist Education Movement (`socialist-education`) | 1962-09..1966-07 | 867 | 632 | 1962..1966-07-29 | 100% | 0 | `▂▁▁▁▁▃▃▅▇▄▂▁▂▂▂▂▂▁▃▃▃▂▃▄▃▄█▅▆▄▅▃▃▂▂▂▂▂▂▁▂▂▂▁▂▆▅` |
| Learn from Lei Feng, Dazhai, Daqing and the Army (`emulation`) | 1963-01..1965-12 | 332 | 146 | 1963..1965-12-30 | 99% | 0 | `▂▄█▁▁▂▂▂▁▁ ▅▅▄▃▅▃▃▄▂▂▄▁▅▃▂▂▁▁▁▂▁▂▃▅▃` |
| Third Front (`third-front`) | 1964-04..1969-12 | 213 | 173 | 1964-04-29..1969-12-11 | 100% | 13 | `▂▅▂▂▄▃▃▂▄▄▄▅▄▆▂▂▄▆▅█▅▄▅▇▂▄▅▂▂▂▂▂▆▃▂▂▂  ▂ ▂    ▂▂ ▂       ▂ ▂ ▄▂ ▂ ▂▂▂` |
| Rectification of the arts (`arts-rectification`) | 1963-09..1966-04 | 327 | 130 | 1963..1966-04-14 | 100% | 0 | ` ▂▃▄▃▂▄▄▃▅█▄▄▆▄▂▃▃▃▃▃ ▄▃▂ ▃▂▃▃▃▂` |
| Two combine into one (`philosophy-1964`) | 1964-05..1965-06 | 47 | 19 | 1964..1965-06-09 | 100% | 0 | `▄▄█▄▂  ▂  ▂  ▂` |
| Successors (`successors-1964`) | 1964-05..1965-12 | 73 | 25 | 1964-05-15..1965-12-07 | 100% | 0 | `█▆██▆█▃▆▃  ▃   ▃   ▃` |
| Fall of Luo Ruiqing (`luo-ruiqing`) | 1965-11..1966-05 | 444 | 109 | 1965..1966-05-27 | 100% | 0 | `▇█▅▂▅▃▆` |
| Hai Rui and the Three-Family Village (`hai-rui`) | 1965-09..1966-06 | 520 | 181 | 1965..1966-06-18 | 99% | 5 | `▁▁█▄▃▄▃▆▅▃` |
| May Sixteenth Circular (`may-16-circular`) | 1966-04..1966-06 | 660 | 69 | 1966..1966-06-28 | 100% | 0 | `▃█▄` |
| Fifty days and the work teams (`work-teams`) | 1966-05..1966-08 | 866 | 251 | 1966..1966-08-31 | 99% | 0 | `▃█▅▅` |
| Eleventh Plenum (`eleventh-plenum`) | 1966-07..1966-08 | 83 | 47 | 1966-07-08..1966-08-28 | 100% | 0 | `▂█` |
| Red Guards (`red-guards`) | 1966-06..1967-03 | 927 | 636 | 1966..1967-03-26 | 96% | 0 | `▂▂█▄▃▃▃▃▂▂` |
| Bourgeois reactionary line (`reactionary-line`) | 1966-09..1967-01 | 103 | 50 | 1966-09-06..1967-01-29 | 98% | 0 | `▃█▃▅█` |
| January Storm (`january-storm`) | 1966-11..1967-02 | 889 | 319 | 1966..1967-02-28 | 96% | 0 | `▃▃█▅` |
| February Countercurrent (`february-countercurrent`) | 1967-01..1967-05 | 1556 | 142 | 1967..1967-05-31 | 100% | 0 | `▇█▆▄▃` |
| Army in the Cultural Revolution (`army-support-left`) | 1967-01..1969-12 | 203 | 199 | 1967..1969-12-29 | 100% | 37 | `▂▄█▄▅▃▃▃▂▂▃▃▁▂▁▁▂▂▂▂▁▁▁▂▁▂ ▁▁▂▂  ▁▂▂` |
| Wuhan incident (`wuhan`) | 1967-04..1967-09 | 747 | 197 | 1967..1967-09-26 | 98% | 0 | `▂▂▂█▃▂` |
| Maos tour of 1967 (`mao-tour-1967`) | 1967-07..1967-09 | 26 | 5 | 1967-07-14..1967-09-16 | 100% | 0 | `▃█▃` |
| Fall of Wang Li, Guan Feng, Qi Benyu (`wang-guan-qi`) | 1967-08..1968-01 | 320 | 54 | 1967..1968-01 | 100% | 0 | `█▄▂  ▂` |
| Foreign Ministry seized; the British mission burned (`foreign-ministry-1967`) | 1967-05..1967-09 | 210 | 59 | 1967..1967-09-18 | 63% | 0 | `▇▄▄█▃` |
| Armed struggle (`factions-1967`) | 1967-03..1968-09 | 770 | 427 | 1967..1968-09-05 | 97% | 58 | `▃▃▆▆▇█▆▃▅▃▃▄▃▃▄▃▇▄▁` |
| Revolutionary committees (`revolutionary-committees`) | 1967-01..1968-09 | 481 | 327 | 1967..1968-09-29 | 100% | 63 | `▂▄▅▃▃▂▃▃▃▂▄▅▄▅▄▄▅▂▆█▆` |
| Yang Chengwu, Yu Lijin and Fu Chongbi (`yang-yu-fu`) | 1968-03..1968-04 | 232 | 35 | 1968..1968-04-07 | 100% | 8 | `█▂` |
| Cleansing the class ranks (`class-ranks`) | 1968-01..1969-12 | 222 | 136 | 1968..1969-11 | 99% | 13 | `▇▅▄▅▇▄▇▂▇█▅▅▅▂▅▄▅▂▂▄▂▇▂ ` |
| Worker propaganda teams (`tsinghua-1968`) | 1968-04..1968-09 | 288 | 34 | 1968..1968-09-29 | 94% | 19 | `▂▂▂▅█▅` |
| Twelfth Plenum and Liu Shaoqi expelled (`twelfth-plenum`) | 1968-09..1968-11 | 65 | 45 | 1968..1968-11-02 | 100% | 17 | `▂█▂` |
| Ninth Congress (`ninth-congress`) | 1968-10..1969-05 | 216 | 117 | 1968..1969-05-31 | 100% | 53 | `▂▁▁▂▂▄█▂` |
| Up to the mountains, down to the villages (`sent-down-youth`) | 1968-06..1969-12 | 52 | 23 | 1968..1969-12-17 | 87% | 3 | ` ▃ ▆▆▃█ ▃      ▆█▃▆` |
| Liu Shaoqis confinement and death (`liu-death`) | 1966-12..1969-11 | 7 | 4 | 1967-01-03..1969-11-12 | 100% | 1 | ` ▅                                █▅` |
| Lushan Plenum of 1970 (`lushan-1970`) | 1970-07..1970-09 | 200 | 0 | .. | 0% | 0 | `   ` |

Notes. `all` far above `win` (Yi–Ta, polemic, February Countercurrent, Red Guards, Luo Ruiqing) means the words recur outside the episode: names of people and places (Ye Jianying, Li Fuchun, Wuhan, Xinjiang) are poor episode keys outside a tight window. Beidaihe and Lushan are places as much as meetings: in July–August every leader's daybook is at Beidaihe, so the window takes his swims with the conference. Soviet experts, Ninth Plenum, Investigation, Xilou, Peng's letter, Philosophy, Successors, Mao's 1967 tour, Liu's death, Yang–Yu–Fu, Panchen, Yi–Ta fall under 40 on their own; they are folded into neighbors in the trial scheme.

## 3. Persons as actors

Actor = the person heads `c` after a place/time prefix is stripped ("Peking 北京, Zhongnanhai. ...", "At ..., ", "Evening, ") and the characters and parentheticals removed: "Mao, on ...", "Mao to ...", "Mao's comment", "Zhou receives". `sole` = alone at the head; `joint` = one of a list at the head ("Mao, Liu Shaoqi and Zhu De receive ..."); `named` = named elsewhere in `c` or tagged `name:` only. `1st src` = entries read from that person's own nianpu/diary. All China threads (28,423).

| person | sole actor | joint actor | named only | 1st src (own nianpu) |
|---|---:|---:|---:|---:|
| Mao Zedong | 2155 | 177 | 2573 | 2480 |
| Zhou Enlai | 5405 | 459 | 1779 | 5722 |
| Chen Yi | 2149 | 241 | 805 | 2406 |
| Yang Shangkun | 1601 | 252 | 2395 | 4684 |
| Zhu De | 1338 | 120 | 365 | 1359 |
| Peng Zhen | 1193 | 83 | 766 | 1304 |
| Deng Xiaoping | 976 | 128 | 1068 | 945 |
| Liu Shaoqi | 665 | 189 | 1380 | 575 |
| Chen Yun | 332 | 19 | 193 | 420 |
| Peng Dehuai | 321 | 2 | 217 | 466 |
| Ye Jianying | 286 | 9 | 186 | 313 |
| Lin Biao | 169 | 21 | 628 | 232 |
| Kang Sheng | 81 | 48 | 540 | — |
| Jiang Qing | 77 | 19 | 346 | — |
| Chen Boda | 47 | 34 | 485 | — |
| Li Fuchun | 44 | 53 | 422 | — |
| Li Xiannian | 44 | 31 | 351 | — |
| Tao Zhu | 27 | 10 | 238 | — |
| Luo Ruiqing | 43 | 18 | 316 | — |
| Tian Jiaying | 56 | 113 | 125 | — |
| Zhang Chunqiao | 34 | 12 | 126 | — |
| Xie Fuzhi | 33 | 14 | 168 | — |
| Wang Li | 19 | 7 | 122 | — |

The Cultural Revolution Group (Kang Sheng, Jiang Qing, Chen Boda, Zhang Chunqiao, Wang Li) are actors in under 130 entries each: they are named, not followed; no source of theirs has been read. Yang Shangkun is the keeper of the largest single source but heads only a third of its entries: his diary's form is "X with Yang Shangkun".

**Mao's own acts by year** (sole + joint at the head; china-leadership and china):

| year | sole | joint | named only |
|---|---:|---:|---:|
| 1960 | 292 | 44 | 305 |
| 1961 | 189 | 18 | 235 |
| 1962 | 200 | 27 | 222 |
| 1963 | 196 | 23 | 171 |
| 1964 | 275 | 17 | 272 |
| 1965 | 181 | 23 | 233 |
| 1966 | 251 | 4 | 446 |
| 1967 | 278 | 7 | 322 |
| 1968 | 151 | 11 | 182 |
| 1969 | 140 | 3 | 181 |
| 1970 | 2 | 0 | 4 |

Total: 2,155 sole + 177 joint = 2,332 of his acts; 2,573 entries name him without his acting. In the best scheme below, 1,019 of his acts (china-leadership only) fall inside an episode and 1,302 go to the Mao thread; by year, episode/Mao thread: 1960 98/238, 1961 65/142, 1962 89/129, 1963 86/133, 1964 146/146, 1965 44/160, 1966 149/106, 1967 194/90, 1968 81/80, 1969 67/76.

Samples of the actor test (first 8 of each class, 1960): 

*mao:sole*

- 1960-01-06 | Mao presides at an enlarged meeting of the Politburo Standing Committee on the agenda of the enlarged Politbur
- 1960-01-06 | Mao on the Qingbao jianxun of Dec. 23, 1959, for Liu, Zhou, Zhu, Lin, Deng and Peng "to discuss international 
- 1960-01-07 | Mao, at the swimming place at 11 a.m., sets the plenary of the enlarged Politburo for 11:30.
- 1960-01-11 | Mao, on the outline of Chen Yi's report of Dec. 27, 1959 to the Party's cultural work conference, "Some views 
- 1960-01-12 | Mao, on the Jan. 9 digest of the Shubao jianxun she, "How the foreign bourgeoisie discusses the Sino-Soviet di
- 1960-01-13 | Mao, on Wang Heshou's Jan. 9 letter and the Metallurgy Ministry Party group's report of Jan. 8 on the small mo

*mao:joint*

- 1960-02-13 | Mao, Liu Shaoqi, Zhu De and Zhou Enlai telegraph Khrushchev and Voroshilov on the tenth anniversary of the Sin
- 1960-03-03 | Mao, Zhou Enlai, Li Fuchun, Kang Sheng and Hu Qiaomu on the draft oral notice of the Central Committee to the 
- 1960-03-07 | Yang Shangkun with Mao on other questions, after Mao's audience for the Soviet Ambassador; back at the Liuyuan
- 1960-03-24 | Mao with Liu Shaoqi, Zhou Enlai, Deng Xiaoping and Peng Zhen on Lenin's anniversary and the propaganda of Mao'
- 1960-04-02 | Mao, Liu Shaoqi, Zhu De and Zhou Enlai telegraph Kádár, Dobi and Münnich on the fifteenth anniversary of Hunga
- 1960-04-20 | Mao, Chen Boda, Hu Qiaomu and Wu Lengxi on Hu's article for Renmin ribao, "Forward along the Path of the Great

*mao:named*

- 1960-01-07 | The enlarged Politburo opens, Mao presiding: the Politburo, the provinces' first secretaries, the central depa
- 1960-01-08 | Yang Shangkun swims after a film; Mao swimming too.
- 1960-01-09 | Shanghai, the enlarged Politburo, after Ke Qingshi, Tao Zhu and Li Jingquan. Mao: productive forces to be free
- 1960-01-12 | The Central Committee to the Communist Youth League's Secretariat, on the campaign to study Mao's works: the f
- 1960-01-12 | Zhu De to the Center and Mao Zedong, by letter: beekeeping should be developed. Its direct return alone beats 
- 1960-01-13 | Wu Xiuquan, on Mao's instruction, sees Chervonenko that evening with words for Khrushchev, approved by the Sta

## 4. Trial partitions

Assignment order: an episode (keyword in its window; for the Cultural Revolution stages also the date window plus a general CR vocabulary; source rules: an entry read from Yang Jisheng's *Mubei* or Dikötter's famine book, 1959-10..1962-12, goes to Famine; from Wu Lengxi's polemic memoir to the polemic thread of its date; from *Tiandi fanfu*, Pu Weihua, MacFarquhar–Schoenhals or Dikötter's CR book to the CR stage of its date); then Mao's act; then a foreign country matching an *existing* thread (Africa, Soviet Union, South Asia, Hanoi, Japan, Korea, Indonesia, Europe, Middle East, Laos, Cuba, Latin America); then the other persons (their act, or read from their nianpu/diary); then places. "Clean" = one candidate at the deciding level; "ambiguous" = two or more (resolved in the counts by the shorter span); "residual" = none.

| scheme | clean | ambiguous | residual | threads | under 40 | over 3,000 |
|---|---:|---:|---:|---:|---|---|
| A. episodes (strong keywords only) | 23.9% | 1.4% | 74.8% | 26 | — | — |
| A2. episodes, stages by date + CR words | 27.1% | 1.6% | 71.3% | 26 | — | — |
| B. episodes + Mao | 32.4% | 1.6% | 66.0% | 27 | — | — |
| C. episodes + Mao + Liu + Zhou | 49.9% | 1.6% | 48.5% | 29 | — | zhou |
| D. episodes + Mao, then country threads, then Liu + Zhou | 58.1% | 4.0% | 37.9% | 41 | — | — |
| E. D + places | 67.2% | 4.7% | 28.1% | 55 | tibet, xinjiang | — |
| F. E + the daybooks (Chen Yi, Zhu De, Yang Shangkun, Peng Zhen, Deng, Peng Dehuai, Chen Yun, Ye Jianying) | 81.6% | 4.4% | 14.1% | 63 | guangxi, inner-mongolia, tibet, xinjiang | — |
| G1. episodes + source rules (no persons, no places) | 32.9% | 2.2% | 64.9% | 26 | — | — |
| G2. G1 + CR stages by date for all domestic entries | 38.2% | 2.3% | 59.5% | 26 | — | — |
| G3. G1 + Mao | 38.1% | 2.2% | 59.7% | 27 | — | — |
| G4. G1 + Mao + country threads + Liu, Zhou | 63.2% | 4.6% | 32.2% | 41 | — | — |
| G5. G4 + places | 69.9% | 5.2% | 24.9% | 55 | tibet, xinjiang | — |
| G6. G4 + all daybooks by actor and by source (no places) | 92.6% | 4.6% | 2.8% | 50 | — | yang |
| G7. G6 + places | 93.4% | 4.7% | 1.9% | 64 | shanghai, guangdong, hubei, hebei, inner-mongolia, sichuan, anhui, gansu, henan, shaanxi, tibet, guangxi, xinjiang | yang |
| G8. G7 with stages by date | 93.5% | 4.8% | 1.7% | 64 | shanghai, guangdong, hubei, hebei, inner-mongolia, sichuan, anhui, gansu, henan, shaanxi, tibet, guangxi, xinjiang | yang |

Reading the table. Episodes alone (A–A2, G1–G2) take a third of the bucket at most, however generous the windows. Mao adds about 5 points. The country threads and Liu and Zhou add 25. The remaining third is the other daybooks, above all Yang Shangkun's diary (G4 residual by first source: Yang diary 3,239; Zhu De 1,093; Chen Yi 903; Peng Zhen 695; Deng 447; Peng Dehuai 323; Chen Yun 320; MacFarquhar *Origins* 255; Ye Jianying 205). Only person threads for the daybook keepers bring the residual under 5 percent (G6).

Sizes in G3 (episodes + Mao): mao 1352, china-red-guards 968, china-famine 930, china-wuhan 816, china-seizures 814, china-four-cleanups 704, china-polemic 680, china-may-sixteenth 679, china-class-ranks 533, china-ninth-congress 470, china-moscow-1960 256, china-shanghai-1960 254, china-tenth-plenum 231, china-africa-tour 224, china-afro-asian 221, china-sixty-articles 212, china-retreat-1962 164, china-bomb 161, china-models 134, china-opera 129, china-third-front 119, china-twelve-articles 114, china-india-war 105, china-hai-rui 104, china-luo-ruiqing 99, china-border-war 68, china-seven-thousand 60.

Most frequent ambiguities (G6): china-class-ranks / china-ninth-congress 99; china-seizures / china-wuhan 83; china-may-sixteenth / china-red-guards 78; soviet-union / vietnam-hanoi 68; laos / vietnam-hanoi 39; china-hai-rui / china-may-sixteenth 33; africa / middle-east 31; africa / latin-america 30; china-retreat-1962 / china-tenth-plenum 30; china-famine / china-twelve-articles 22; africa / south-asia 22; china-africa-tour / china-polemic 22. Of 1,219 ambiguous entries in G6, 635 are between two countries, 363 between two keyword episodes, 221 between two stages by source rule; 290 are year-dated entries that no stage window can place.

## 5. Places within China

Place = the `place:` field (on 14,055 of the 26,320; Peking alone 7,533) or the province/city and its chief people named in `c` with characters. "Held by" = where the entry would go before any place thread is consulted (episode; CR stage by date; Mao; an existing country thread; Liu or Zhou; another daybook keeper); "free" = what a place thread could claim without double-cutting.

| place | entries | by `place:` | span | peak years | episode | stage | Mao | country | Liu/Zhou | other daybook | free | chief episodes |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Peking (the city) | 971 | 0 | 1960..1970-01 | 1966 446, 1965 90, 1964 80 | 494 | 67 | 36 | 21 | 52 | 131 | 170 | china-may-sixteenth 175, china-red-guards 112, china-hai-rui 73 |
| Shanghai | 1024 | 670 | 1960..1970-01 | 1960 226, 1966 175, 1967 144 | 316 | 47 | 63 | 106 | 98 | 227 | 167 | china-seizures 65, china-shanghai-1960 54, china-red-guards 31 |
| Wuhan and Hubei | 531 | 294 | 1960..1969-11 | 1967 158, 1966 87, 1960 60 | 229 | 39 | 73 | 21 | 36 | 56 | 77 | china-wuhan 117, china-seizures 14, china-four-cleanups 13 |
| Sichuan | 722 | 284 | 1960..1970-01 | 1961 118, 1967 109, 1960 102 | 198 | 40 | 25 | 9 | 56 | 217 | 177 | china-wuhan 37, china-third-front 28, china-red-guards 23 |
| Guangxi | 280 | 106 | 1960..1969-11 | 1968 92, 1967 51, 1963 33 | 147 | 9 | 8 | 13 | 11 | 60 | 32 | china-class-ranks 87, china-wuhan 39, china-retreat-1962 5 |
| Guangdong | 615 | 347 | 1960..1969-12 | 1961 164, 1960 115, 1964 79 | 132 | 15 | 41 | 47 | 47 | 216 | 117 | china-sixty-articles 31, china-class-ranks 21, china-wuhan 20 |
| Henan | 317 | 64 | 1960..1969-11 | 1960 131, 1961 51, 1967 30 | 129 | 6 | 26 | 6 | 21 | 66 | 63 | china-famine 60, china-wuhan 20, china-twelve-articles 13 |
| Anhui | 225 | 26 | 1960..1970-01 | 1960 90, 1961 42, 1962 23 | 68 | 8 | 7 | 5 | 8 | 38 | 91 | china-famine 17, china-retreat-1962 11, china-class-ranks 11 |
| Gansu | 218 | 37 | 1960..1969-09 | 1960 54, 1961 32, 1965 32 | 73 | 5 | 3 | 0 | 3 | 21 | 113 | china-four-cleanups 18, china-famine 16, china-wuhan 9 |
| Shandong | 258 | 47 | 1960-01..1969-11 | 1960 80, 1966 34, 1961 28 | 68 | 15 | 39 | 6 | 19 | 45 | 66 | china-famine 21, china-twelve-articles 10, china-red-guards 7 |
| Inner Mongolia | 158 | 19 | 1960-02..1970-01 | 1966 29, 1967 23, 1969 22 | 35 | 3 | 5 | 3 | 34 | 36 | 42 | china-red-guards 5, china-wuhan 4, china-class-ranks 4 |
| Tibet | 116 | 0 | 1960-01..1969-12 | 1960 36, 1961 18, 1965 15 | 23 | 3 | 4 | 23 | 26 | 18 | 19 | china-class-ranks 6, china-red-guards 4, china-shanghai-1960 2 |
| Xinjiang | 151 | 0 | 1960-02..1970-01 | 1962 26, 1965 23, 1966 23 | 50 | 7 | 7 | 17 | 24 | 31 | 15 | china-polemic 8, china-class-ranks 6, china-seizures 5 |
| Hebei | 597 | 221 | 1960..1969-12 | 1961 162, 1960 106, 1966 64 | 184 | 28 | 40 | 8 | 64 | 124 | 149 | china-four-cleanups 53, china-famine 27, china-sixty-articles 22 |
| Shaanxi | 751 | 559 | 1960-01..1970-01 | 1965 400, 1964 179, 1966 53 | 371 | 11 | 12 | 20 | 17 | 145 | 175 | china-four-cleanups 321, china-class-ranks 11, china-red-guards 10 |
| Hangzhou | 512 | 306 | 1960..1970-01 | 1960 110, 1966 86, 1961 85 | 128 | 11 | 75 | 45 | 35 | 152 | 66 | china-four-cleanups 21, china-may-sixteenth 15, china-famine 11 |
| Beidaihe | 496 | 445 | 1960-04..1967-08 | 1960 164, 1962 149, 1961 83 | 324 | 0 | 9 | 5 | 5 | 107 | 46 | china-shanghai-1960 151, china-tenth-plenum 145, china-moscow-1960 10 |
| Lushan | 159 | 79 | 1960-03..1969-02 | 1961 114, 1966 11, 1967 11 | 130 | 2 | 4 | 3 | 6 | 4 | 10 | china-sixty-articles 100, china-hai-rui 7, china-famine 4 |
| Hunan | 395 | 134 | 1960..1969-12 | 1961 94, 1967 73, 1964 54 | 126 | 15 | 73 | 10 | 36 | 58 | 77 | china-wuhan 53, china-four-cleanups 16, china-class-ranks 16 |
| Yunnan | 350 | 174 | 1960..1970-01 | 1965 56, 1964 47, 1961 46 | 83 | 14 | 8 | 35 | 41 | 111 | 58 | china-class-ranks 17, china-third-front 13, china-seizures 7 |
| Niujiao | 271 | 241 | 1964-10..1965-12 | 1965 157, 1964 114 | 271 | 0 | 0 | 0 | 0 | 0 | 0 | china-four-cleanups 271 |
| Xi'an | 363 | 310 | 1960-02..1970-01 | 1965 231, 1964 62, 1966 27 | 85 | 3 | 2 | 14 | 3 | 111 | 145 | china-four-cleanups 70, china-may-sixteenth 4, china-red-guards 4 |
| Dao county | 39 | 37 | 1961-04..1967-10 | 1967 34, 1964 2, 1961 1 | 34 | 0 | 0 | 0 | 0 | 0 | 5 | china-wuhan 33, china-four-cleanups 1 |
| Chongqing | 173 | 137 | 1960-03..1969-07 | 1967 60, 1966 33, 1965 21 | 61 | 17 | 4 | 1 | 13 | 33 | 44 | china-wuhan 29, china-class-ranks 11, china-red-guards 10 |
| Nanning | 107 | 84 | 1960-03..1968-08 | 1968 40, 1964 15, 1962 13 | 59 | 4 | 2 | 6 | 2 | 25 | 9 | china-class-ranks 38, china-wuhan 12, china-four-cleanups 3 |
| Wuhan | 426 | 294 | 1960..1969-11 | 1967 151, 1966 71, 1960 46 | 189 | 32 | 56 | 21 | 24 | 45 | 59 | china-wuhan 113, china-seizures 13, china-red-guards 10 |

Findings.
- **Niujiao** (271, Oct. 1964–Dec. 1965) is Yang Shangkun's Four Cleanups squat point: the Niujiao brigade, Chang'an county, outside Xi'an, where he lived with a work team; every entry is from his diary. All 271 fall to Four Cleanups (a Niujiao rule is in the episode). **Xi'an 1965** (231) is the same stay: Yang posted to the Northwest Bureau, his diary at Xi'an; 70 already Four Cleanups, 145 free, 111 his daybook. Not a place thread: an episode within Four Cleanups, or Yang's thread.
- **Beidaihe** (496) and **Lushan** (159) are the leaders' summer seats: 324 and 130 fall to the conferences held there (1960, 1962; 1961); the rest is leave (swims, doctors). No place thread.
- **Hangzhou** (512) is Mao's base and the leaders' winter stop; its entries are Mao's and the daybooks'. 66 free. No place thread.
- **Wuhan 1967** (151 of 426) and **Dao county** (34 of 39, Aug.–Oct. 1967) are wholly the Wuhan-and-the-army stage; **Nanning 1968** (40) and **Guangxi** (92 in 1968) are the revolutionary-committees stage (the Guangxi killings, the July 3 notice); **Chongqing 1967** (60) splits between the 1967 and 1968 stages. Ruled out: the episodes hold them.
- **Peking the city** (971; peak 446 in 1966): 494 already episodes (May Sixteenth 175, Red Guards 112, Hai Rui 73), 67 stage, 170 free (the municipal committee's rectification reports of 1961, Deng Tuo's columns, the 1964 campus critiques). The 1966 purge of the municipal committee is the May Sixteenth stage. A Peking thread would hold about 170, thinly spread over ten years: ruled out; the 1961–65 municipal and literary matter belongs to Hai Rui (Deng Tuo, Wu Han) once its window is opened back to 1961.
- **Shanghai** (1,024): 316 episodes (seizures of power 65, 1960 conference 54), 227 daybooks, 106 country (receptions), 167 free (Ke Qingshi's cultural forums, 1967 street violence, statistics). **Sichuan** (722): 198 episodes, 217 daybooks, 177 free (famine statistics, Li Jingquan, 1966–67 local violence). **Guangdong** (615), **Hebei** (597), **Shaanxi** (751), **Hunan** (395), **Yunnan** (350): the same shape, 60–180 free each.
- The famine provinces (**Henan** 317, **Anhui** 225, **Gansu** 218, **Shandong** 258) peak in 1960–61, and their free entries are mostly famine reports the keyword rule missed; they belong in Famine, not in provinces.
- **Inner Mongolia** (158), **Tibet** (116), **Xinjiang** (151) are small and scattered (under 50 free each).

Ruling. No place thread survives the rule "not where an episode already holds its entries": in every place, the episodes and the daybooks take most, and what is left is under 200 entries over ten years, with no event of its own. Scheme G5 (places after persons Liu and Zhou) gives Shanghai 316, Sichuan 266, Shaanxi 264, Guangdong 244, Peking 223, Hebei 174; G7 (places after all the daybooks) leaves every place under 40. A place thread works only as a sorting bin for the famine and CR local reports, and for those the famine and stage threads are the better home.

## 6. The best scheme (G6, with conference day-windows; Yang split)

Coverage of the 26,320: clean 92.6%, ambiguous 4.6% (resolved by the narrower window, or the first country), residual 2.8% (724). Of the 26,320: episodes 9,515 (36%), country threads (existing) 4,661 (18%), Mao 1,490 (6%), the other eleven persons 9,930 (38%).

### Episode threads (parent `china`)

| thread (slug) | name | span | entries | statement |
|---|---|---|---:|---|
| `china-shanghai-1960` | Shanghai and Beidaihe, 1960 | 1960-01..1960-08 | 275 | The year's targets set at Shanghai; the experts withdrawn and the summer conference at Beidaihe. {{1960-01-07..1960-01-17|The enlarged Politburo at Shanghai.}} {{1960-07-05..1960-08-10|Beidaihe; the Soviet experts recalled.}} |
| `china-moscow-1960` | Bucharest and Moscow | 1960-04..1961-01 | 255 | The quarrel with Moscow carried into the parties' meetings, from "Long Live Leninism!" to the Moscow Statement. {{1960-04-16|"Long Live Leninism!"}} {{1960-06-24..1960-06-26|Peng Zhen at Bucharest.}} {{1960-11-10..1960-12-01|The eighty-one parties at Moscow; Liu Shaoqi with Khrushchev.}} |
| `china-twelve-articles` | Twelve Articles | 1960-09..1961-01 | 119 | The communes' "communist wind" checked: the emergency letter and the Ninth Plenum. {{1960-11-03|The Emergency Directive Letter, the "Twelve Articles."}} {{1960-11-15|Mao's directive on the "five winds."}} {{1961-01-14..1961-01-18|The Ninth Plenum.}} |
| `china-famine` | Famine | 1959-10..1962-12 | 921 | The famine as the provinces reported it, the grain moved and bought abroad, the deaths counted. {{1960-06-03|The Taolin report on the deaths.}} {{1960-10-03|Chen Yun on Hebei and Shandong.}} {{1961-01-03|Henan's relief directive.}} |
| `china-sixty-articles` | Sixty Articles | 1961-01..1961-09 | 311 | The year of investigation: the communes' regulations drafted at Canton, revised at Peking, and the industrial articles at Lushan. {{1961-03-10..1961-03-23|The Canton conference; the Sixty Articles.}} {{1961-04-02..1961-05-15|Liu Shaoqi in Hunan.}} {{1961-08-23..1961-09-16|Lushan; the Seventy Articles.}} |
| `china-seven-thousand` | Seven Thousand Cadres | 1961-11..1962-02 | 111 | The enlarged work conference of January 1962: Liu's report, Mao's self-criticism, Lin Biao's defense of the Leap. {{1962-01-11|The conference opens.}} {{1962-01-27|Liu Shaoqi's report.}} {{1962-01-30|Mao's speech.}} |
| `china-retreat-1962` | Xilou and the retreat | 1962-02..1962-07 | 165 | Chen Yun's deficit and emergency program, the cities emptied, the household contracts. {{1962-02-21..1962-02-23|The Xilou meeting.}} {{1962-05-07..1962-05-11|The May work conference; the streamlining.}} {{1962-07-06..1962-07-23|Mao against household contracting.}} |
| `china-tenth-plenum` | Beidaihe and the Tenth Plenum | 1962-07..1962-10 | 249 | "Never forget class struggle": the Beidaihe conference, the plenum, Peng Dehuai's case reopened. {{1962-08-06..1962-08-24|Beidaihe.}} {{1962-08-26|The plenum's preparatory meeting.}} {{1962-09-24..1962-09-27|The Tenth Plenum.}} |
| `china-india-war` | India war | 1962-06..1963-03 | 104 | The border war with India and the cease-fire. {{1962-07-22|Mao on the Galwan post.}} {{1962-11-21|The cease-fire declared.}} {{1963-01-05|Zhou and Bandaranaike.}} |
| `china-polemic` | Polemic | 1961-10..1964-11 | 677 | The open polemic with Moscow, from the Twenty-second Congress to Zhou in Moscow after Khrushchev's fall. {{1961-10-17..1961-10-23|Zhou at the Twenty-second Congress.}} {{1963-06-14..1963-07-20|The general line; Deng and Suslov.}} {{1964-11-05..1964-11-14|Zhou in Moscow.}} |
| `china-four-cleanups` | Four Cleanups | 1962-09..1966-05 | 754 | The socialist education movement: the Ten Points, the work teams, Taoyuan, Niujiao, the Twenty-three Articles. {{1963-05-02..1963-05-12|The Hangzhou conference; the First Ten Points.}} {{1964-10-28..1965-12|Yang Shangkun at Niujiao.}} {{1964-12-15..1965-01-14|The work conference; the Twenty-three Articles.}} |
| `china-models` | Lei Feng, Dazhai, Daqing | 1963-01..1965-12 | 134 | The emulation campaigns: Lei Feng, the Dazhai brigade, the Daqing oilfield, the army's political work. {{1963-03-05..1963-03-06|"Learn from Comrade Lei Feng."}} {{1964-01-02|The General Office on Daqing.}} {{1964-12|Dazhai in the Government Work Report.}} |
| `china-opera` | Opera reform | 1963-09..1965-12 | 129 | The arts rectified: Mao's two instructions, the festival of modern Peking opera, the ministry purged. {{1964-06-23|Zhou with the festival's troupes.}} {{1964-06-05..1964-07-31|The festival of modern Peking opera.}} {{1965-04|The Ministry of Culture reorganized.}} |
| `china-africa-tour` | Zhou in Africa | 1963-12..1964-03 | 224 | Zhou Enlai's and Chen Yi's tour of ten African countries and Albania, the eight principles of aid. {{1963-12-14|To Cairo.}} {{1963-12-21..1963-12-27|Algeria.}} {{1964-01-15|Accra; the eight principles.}} |
| `china-third-front` | Third Front | 1964-04..1966-05 | 117 | The interior industrial base: the Third Plan recast for war, Panzhihua and the southwest railways. {{1964-05-15..1964-06-17|The work conference; the third front.}} {{1965-03-29|Zhu De at Chengdu.}} {{1965-11-13|The plan conference.}} |
| `china-afro-asian` | Afro-Asian conference | 1964-04..1965-11 | 221 | The second Asian–African conference sought and lost at Algiers. {{1965-03-30..1965-04-01|Zhou at Algiers.}} {{1965-06-19..1965-06-28|Ben Bella deposed; the conference put off.}} {{1965-11-04|China's withdrawal.}} |
| `china-bomb` | Bomb | 1963-07..1969-12 | 160 | The atomic and hydrogen bombs and the missiles: their decisions and tests. {{1963-07-28|The test ban discussed.}} {{1964-10-16|The first test; the statement.}} {{1966-10-27|The missile with a warhead.}} {{1967-06-17|The hydrogen bomb.}} |
| `china-hai-rui` | Hai Rui | 1965-09..1966-04 | 103 | Yao Wenyuan's article, the Peking committee's defense of Wu Han, the February Outline. {{1965-11-10|Yao Wenyuan's article.}} {{1965-11-29|The *Beijing Daily* reprints it.}} {{1966-02-12|The February Outline circulated.}} |
| `china-luo-ruiqing` | Luo Ruiqing | 1965-11..1966-05 | 103 | The Chief of Staff accused by Lin Biao and removed at the Shanghai conference. {{1965-11-27|Luo with Lin Biao.}} {{1965-12-08..1965-12-15|The Shanghai conference.}} {{1966-03-04..1966-04-08|The struggle meetings.}} |
| `china-may-sixteenth` | May Sixteenth and the work teams | 1966-04..1966-07 | 685 | The enlarged Politburo and its Circular, Peng Zhen's fall, Nie Yuanzi's poster, the fifty days of the work teams. {{1966-05-16|The May 16 Circular.}} {{1966-05-25|Nie Yuanzi's poster.}} {{1966-07-16|Mao in the Yangtze.}} {{1966-07-28|The work teams withdrawn.}} |
| `china-red-guards` | Red Guards | 1966-08..1966-12 | 991 | The Eleventh Plenum and the Red Guards: the rallies, the "four olds," the house searches, the attack on the "reactionary line." {{1966-08-01..1966-08-12|The Eleventh Plenum; "Bombard the Headquarters."}} {{1966-08-18|The first rally.}} {{1966-10-09..1966-10-28|The October work conference.}} |
| `china-seizures` | Seizures of power | 1967-01..1967-04 | 814 | The January Storm at Shanghai, the seizures in the provinces, the army sent in, the February Countercurrent. {{1967-01-06|The rebels take Shanghai.}} {{1967-01-23|The army to support the left.}} {{1967-02-16|The Huairen Hall.}} |
| `china-wuhan` | Wuhan and the army | 1967-05..1967-12 | 816 | The army's factions and the armed struggle: Wuhan, the drive against "the handful in the army," the fall of Wang Li and Guan Feng. {{1967-07-20|The Million Heroes take Wang Li.}} {{1967-08-22|The British office burned.}} {{1967-08-30|Wang Li and Guan Feng detained.}} |
| `china-class-ranks` | Revolutionary committees | 1968-01..1968-09 | 533 | The revolutionary committees completed and the class ranks cleansed: Yang Chengwu's fall, the July notices, the propaganda teams. {{1968-03-24|Yang Chengwu, Yu Lijin and Fu Chongbi dismissed.}} {{1968-07-28|Mao with the five Red Guard leaders.}} {{1968-09-05|The last committees, Tibet and Xinjiang.}} |
| `china-ninth-congress` | Ninth Congress | 1968-10..1969-04 | 476 | Liu Shaoqi expelled at the Twelfth Plenum; the Ninth Congress and Lin Biao as successor. {{1968-10-13..1968-10-31|The Twelfth Plenum.}} {{1969-04-01..1969-04-24|The Ninth Congress.}} {{1969-04-28|Lin Biao's report printed.}} |
| `china-border-war` | Border war | 1969-03..1969-12 | 68 | The clashes on the Ussuri and in Xinjiang, the war scare, the airport talks and the border talks. {{1969-03-02|Zhenbao.}} {{1969-09-11|Kosygin at the Peking airport.}} {{1969-10-17..1969-10-20|Order No. 1; the border talks.}} |

### Person threads (parent `china`)

| thread (slug) | name | span | entries | statement |
|---|---|---|---:|---|
| `china-mao` | Mao | 1960–69 | 1490 | Mao Zedong's own acts outside the episodes: his comments and instructions, letters, talks, audiences, poems, swims, travels. {{1960-10-27|Edgar Snow.}} {{1961-09-24|Montgomery at Wuchang; the Yangtze.}} {{1965-05|Jinggangshan revisited.}} {{1965-11|South, for eight months.}} |
| `china-zhou` | Zhou Enlai | 1960–69 | 2330 | The Premier's day outside the episodes: the State Council, the plan, the guests and the countries without a thread (Burma, Cambodia, the bloc). {{1963-02-16|Sihanouk at the Great Wall.}} {{1965-10-03|The China–Cambodia joint statement.}} {{1965-08-23|The long-term plan.}} |
| `china-liu` | Liu Shaoqi | 1960–68 | 361 | The head of state to his fall: his inspections, receptions and visits abroad. {{1961-04-02..1961-05-15|Hunan.}} {{1963-04-12..1963-05-16|Indonesia, Burma, Cambodia, Vietnam.}} {{1964-09-27|Sihanouk's banquet.}} |
| `china-zhu` | Zhu De | 1960–69 | 1090 | The NPC chairman's inspections, receptions and poems. {{1960-02-01|Conghua.}} {{1963-04-20|Mount Emei.}} {{1964-08-05|Hulunbuir.}} |
| `china-chen-yi` | Chen Yi | 1960–68 | 903 | The Foreign Minister's receptions, travels and poems, and his fall. {{1961-05-16|Sihanouk at Geneva.}} {{1964-12|"Journey to six countries."}} {{1962-07-21|The Geneva reception.}} |
| `china-yang` | Yang Shangkun | 1960–65 | 3112 | The General Office's director: his diary of the Center's business, to his removal (split at 1963: 1,403 and 1,709). {{1964-07-23|Shenyang.}} {{1965-04-21|Hanzhong.}} {{1965-11-30|His last day at the Office.}} |
| `china-peng-zhen` | Peng Zhen | 1960–66 | 669 | The Secretariat and the Peking committee, to his fall. {{1963-12-29|The People's Council on the arts.}} {{1964-09-03|The fifth Peking People's Congress.}} {{1966-03-29|His last NPC session.}} |
| `china-deng` | Deng Xiaoping | 1960–66 | 450 | The General Secretary's Secretariat. {{1961-04|The Peking communes investigated.}} |
| `china-chen-yun` | Chen Yun | 1960–69 | 321 | The planner's investigations and programs. {{1961-07|Qingpu.}} |
| `china-peng-dehuai` | Peng Dehuai | 1961–69 | 324 | The fallen marshal: his letters, the Third Front at Chengdu, the struggle meetings. {{1962-06|The letter of eighty thousand characters.}} {{1965-12-30|To Chengdu.}} {{1967-09-13|Struggled at the Political School.}} |
| `china-ye` | Ye Jianying | 1960–69 | 202 | The marshal's military training and inspections.  |
| `china-lin` | Lin Biao | 1960–69 | 168 | The Defense Minister and successor.  |

### To existing country threads (thread: the country, `also: [china]`)

| thread | entries |
|---|---:|
| `africa` | 880 |
| `soviet-union` | 768 |
| `south-asia` | 628 |
| `vietnam-hanoi` | 609 |
| `japan` | 362 |
| `korea` | 328 |
| `indonesia` | 275 |
| `europe-and-the-alliance` | 256 |
| `middle-east` | 159 |
| `laos` | 144 |
| `cuba` | 131 |
| `latin-america` | 121 |

Stations: every station date was checked by script to fall on an entry the scheme assigns to that thread; the station's wording is mine, from the entries' openings or the period, and should be read against the entries before use (several, e.g. Long Live Leninism, Apr. 16, 1960; the missile, Oct. 27, 1966; the British office, Aug. 22, 1967, were chosen from general knowledge and only their dates verified). The person statements are drafts.

## 7. The residual (best scheme): 30 openings by year

Residual by year: 1960 103, 1961 162, 1962 68, 1963 34, 1964 61, 1965 66, 1966 78, 1967 28, 1968 16, 1969 88, 1970 20. By first source: `w.macfarquhar-origins-of-the-cultural` 215, `w.jianguo-yilai-zhongyao-wenxian` 144, `w.pu-weihua-zalan-jiu-shijie` 77, `w.yang-jisheng-tiandi-fanfu` 66, `w.peng-zhen-nianpu-1902` 57, `w.macfarquhar-maos-last-revolution` 36, `w.deng-xiaoping-nianpu-1904` 26, `w.dikotter-cultural-revolution` 22.

- 1960-08 — The Foreign Ministry to the party committees of Shenyang, Harbin and Changchun, on the coming visit of the MPLA's Viriato da Cruz and the PAIGC's Amílcar Cabral
- 1960-10-16 — The Center 中共中央 forwards and agrees with the minutes of the national finance and trade secretaries' conference on doing the autumn and winter grain work firmly 
- 1960-12 — The Secretariat takes a formal decision to prepare Liu Shaoqi's selected works, by Deng Liqun's account at the end of the year. Mao had suggested it in 1952 and
- 1961-07-24 — The Anhui party's written report renames the policy the field management responsibility system with bonuses and stresses the collective: production guaranteed b
- 1961-07-08 — Sichuan. The provincial party issues a directive on cutting the urban population.
- 1961-09-06 — Li Xiannian 李先念 reports to the Chairman and the Center 中共中央 "On the market, prices and the circulation of currency" 《关于市场、物价和货币流通问题的报告》: currency in circulation
- 1962-02-27 — Wang Jiaxiang, head of the International Liaison Department, writes to the three men running foreign affairs, Zhou Enlai, Deng Xiaoping and Chen Yi. His deputie
- 1962-02-26 — The third draft of Liu Shaoqi's written report is circulated within the party.
- 1962-12 — Prague. The Chinese delegation and its Czech hosts have a five-hour wrangle at what should have been a courtesy farewell lunch.
- 1963-11-11 — Central Party School. Yang Xianzhen, its deputy director, gives his first lecture since his rehabilitation, against the philosophical idealism behind the Great 
- 1963-02 — Djilas's *The New Class* published in China as a *neibu* (internal) book.
- 1963 — At Zhou Enlai 周恩來's inquiry the Central Propaganda Department 中共中央宣傳部 calls over twenty historians on Qi Benyu's article; they condemn it as distorting history,
- 1964-05-08 — The Propaganda Department's draft report on the rectification: the Party's cultural policy not carried out, the cultural bodies confused in aim and blind to cla
- 1964 — Inner Mongolia 内蒙古 prints and issues throughout the region the "Declaration to the people of Inner Mongolia" 〈对内蒙古人民的宣言〉, issued in Mao Zedong's 毛泽东 name on Dec
- 1964 — Gao Anhua, a middle school student, lives through rural conditions in the countryside, to her horror.
- 1965-02-01 — *Zhongguo qingnian*, No. 3, puts on its cover Mao and Liu Shaoqi side by side at the NPC session that re-elected Liu state chairman.
- 1965 — Xin Yuanhua 忻元華 is sentenced to three years' control, to be reformed under the masses' supervision.
- 1965-12-05 — Peking 北京. Xiao Yan 小阎 (Yan Mingfu 阎明复, by the editors' note at II, 668) and others tell Yang Shangkun 杨尚昆 of the translation group's work.
- 1966-07-18 — The office of the Peng Zhen case group 彭真专案小组, Kang Sheng 康生 approving, writes its "First arrangement of work," the stress on "gathering and knowing the materia
- 1966-03-19 — Jiang Qing sends the army forum's summary to Lin Biao.
- 1966 — Taiyuan. Huang Kecheng meets Yang Shangkun by chance, both exiled from the capital.
- 1967-11-23 — The *Renmin ribao* 人民日报, *Hongqi* 红旗 and *Jiefangjun bao* publish a joint editorial, "The struggle between the two roads in China's countryside" 中国农村两条道路的斗争. It
- 1967-07-31 — Peking 北京, the Public Security Ministry 公安部. Peng Zhen 彭真 taken there to be struggled against, and beaten.
- 1967-01-20 — Peng Zhen 彭真 writes a rebuttal of the four "crimes" the case group charges, "On 'Peng, Lu, Luo, Yang' and the 'Changguanlou incident'": no plotting or organizat
- 1968-03-27 — Peng Zhen 彭真 questioned by the case office.
- 1968-03-01 — Qi Jinghe 齐景和 reports to Kang Sheng 康生 that Peng Zhen 彭真 and Luo Ruiqing 罗瑞卿 "served the enemy's spy organs."
- 1968-05-21 — Peng Zhen 彭真, questioned by the case office, answers on the movement in the Northeast for the release of Zhang Xueliang 张学良 (the patriotic Northeastern Army gen
- 1969-08-28 — Xinjiang. The military units and the people are put on high alert.
- 1969-11-26 — Deng Xiaoping 邓小平 writes to Wang Dongxing on his labour and life at Nanchang: from Nov. 9 he and Zhuo Lin have gone to the works, about three and a half hours' 
- 1969-01 — Huang Yongsheng 黄永胜 and Wu Faxian 吴法宪 go to Li Fuchun's 李富春 home and convey Mao's 毛泽东 and Lin Biao's 林彪 notes on the old comrades of the "February adverse curre
- 1970-01-18 — Zhou Enlai, on the Central General Office's letters and visits section's investigation of big building and non-productive building at Xi'an and other places, or
- 1970-01-09 — The Peking 北京 public security, procuracy and courts military control commission 北京市公檢法軍管會 sends the units a "notice" with an execution list of 20, Yu Luoke 遇羅克 
- 1970-01 — The Center, that is Mao 毛泽东, endorses virtually word for word Lin Biao's 林彪 criterion "Everything according to preparing for war," and its application is extend

What it is: the Center's and the State Council's documents on ordinary business (finance and trade, the nationalities, the plan), the scholarship's undated or year-dated generalizations (MacFarquhar's *Origins*, Dikötter), the case groups of the fallen (Peng Zhen questioned, 1967–68; his own thread ends at his fall), and people outside every thread (He Long, Li Zongren, Sun Weishi, Huang Kecheng).

## 8. Boundary problems, candidly

1. **The bucket is cut by its sources, not its events.** Seventy percent of china-leadership is a dozen daybooks (Yang Shangkun's diary 4,679; Zhou Enlai's three chronologies 5,593; Chen Yi 2,405; Zhu De 1,359; Peng Zhen 1,304; Mao's nianpu and manuscripts 2,333; Deng 945). The named episodes, however generously windowed, take about a third (A2 27%, G1 33%, best 39% with conference day-windows). The rest is the routine of the leaders' days: receptions, inspections, calls, reading, health. No cutting by episode makes that legible; only person threads do, and then the threads mirror the books read (the question the owner put about "Leadership" returns in a new form: is "Yang Shangkun" a thread or a source?). Yang's diary (3,112 after the episodes) exceeds the 3,000 ceiling alone and must be split by date (1960–62 / 1963–65) or called what it is, the General Office. Some of it may be R18 "private" (teeth treated, a cold), a matter for the owner, not for threads.
2. **Foreign matter: the country threads or China's.** About 5,300 entries are Zhou's, Chen Yi's, Liu's and Zhu De's receptions and visits. The house already cuts foreign affairs by country (Africa, Laos, South Asia, Hanoi, Japan, Indonesia), so they could go there with `also: [china]` (4,661 to twelve existing threads), but that moves a quarter of the bucket out of China and swells Africa from 203 to about 1,080 and the Soviet Union from 528 to about 1,300. 1,386 more match only countries that have no thread (Albania and the European bloc 1,024 hits; Burma and Cambodia 816; Mongolia 206); in the best scheme they stay with Zhou and Chen Yi. Two-country entries (Soviet Union / Hanoi 68, Laos / Hanoi 39, Africa / Middle East 31) are the largest ambiguity.
3. **Episodes overlap and are place-bound.** The Cultural Revolution stages cut cleanly by date, but a stage's edge splits a continuing affair (Wuhan's factions run from April into 1968; the case groups of the fallen run from 1966 to 1969 and fit no stage); year-dated entries (869) cannot be staged at all (290 of the ambiguities). Before 1966 the conferences are clean only by day-window, and the day-window takes in everything the leaders did those weeks (Beidaihe swims with the Tenth Plenum's preparation). The Leap/famine/retreat sequence has no clean seams: the famine reports, the Twelve Articles, the Sixty Articles and the 1962 retreat share their vocabulary (grain, communes, mess halls, sending down), and the boundaries in the scheme are dates, not content. Small named episodes (Ninth Plenum 20, Xilou 22, Peng's letter 3, Yang–Yu–Fu 35, Mao's 1967 tour 5) do not stand alone and are folded into neighbors.

Smaller: Hai Rui wants its window opened back to 1961 (Deng Tuo's columns, Wu Han's play) to absorb the Peking-city entries; Peng Zhen's, Liu's and Peng Dehuai's threads should run through their persecution (1966–69), or the case groups need an episode of their own; the Cultural Revolution Group (Kang Sheng, Jiang Qing, Chen Boda) never reaches 130 entries as actors and cannot carry person threads; the existing `india-and-china-cultural-revolution` (568, almost all `also:`) is superseded by the six stages; the keyword rules are a first pass (precision checked by sampling only: good on named episodes, loose on "Beidaihe", "Wuhan", "rebels").


## 9. Scripts

In `/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/china-threads-survey-scripts/` (run from that directory in this order: extract, phrases, stats, persons, assign, assign2, places, final, report; `extract.py` reads /home/user/bib/lists/cal directly).

- `extract.py`: regex extraction of every entry touching the China threads → china.jsonl, allthreads.json
- `phrases.py`: frequency of capitalized phrases, quoted slogans, numbered formulas, 《》 titles → phrases.json
- `lexicon.py`: episode candidates: regex and window
- `stats.py`: candidate counts, windows, densities → episode_stats.json
- `persons.py`: actor/named counts → person_counts.json, person_extra.json, actors.json
- `scheme.py`: trial episode threads, country, person and place lexicons
- `assign.py`: schemes A–F → runs.pkl, cl.pkl
- `assign2.py`: schemes G1–G8 (source rules, daybooks) → runs2.pkl
- `places.py`: place clusters → places.json
- `final.py`: best scheme (G6 + conference day-windows) → best.pkl, best_sizes.json
- `report.py`: this file