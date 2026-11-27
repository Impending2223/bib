# The Drive and what the series has read of it: a reading plan

Written Nov. 26, 2026, and recut Nov. 27, 2026, for the owner to approve or change. The recut follows the owner's words of Nov. 26 (ruling 63, `notes/owner-rulings.md`): the batches are by subject, a government document goes with its subject, apportionment leaves civil rights, and a batch is read by readers one after another. It starts no reading. It answers the owner's words of Nov. 24 and Nov. 26: a full inventory of the works on the Drive and a suggested breakdown of the unread items into reading batches. Nothing in `lists/`, `sources/` or on the Drive was changed. The full list is `notes/proposals/drive-reading-plan.tsv`, one row a work.

R0 governs this plan and I disregarded nothing in it. The plan sets no scope. Every batch below is a list of sources to read for every dated event they report.

## A side effect to know before any reading

To count pages I asked the Drive for the end of each PDF, in about 1,800 PDFs, with many small requests each, and kept no copy. That ran the Drive's download limit out: a test of 12 files picked at random, minutes after I stopped, gave Google's "Quota exceeded" page and not the PDF. I stopped the counting at once and made no further requests. I cannot lift the limit and do not know when it lifts; Google's usual period is about a day.

Until then a reader who fetches a file by the curl line in `notes/guide/reading-a-copy.md` gets an HTML page, and `file` will say "HTML document". The guide reads that as "the file is not shared by link". Here it means the limit, and the reader should wait and not report the file as unshared. Whoever starts the first batch should try one file before briefing readers.

## What the Drive holds

- The shared folder "1968 series: sources for Claude" was listed afresh on Nov. 26. Its top level holds 975 items: 12 folders and 963 files. The inventory of Nov. 25 recorded 878 top-level items, so 97 files are new since it. Nothing it recorded is gone.
- The new files are mostly Chinese books of the Nov. 25 and Nov. 26 uploads: the lives of Chen Yun, Liu Shaoqi and Zhou Enlai, Peng Dehuai's own account, Walder's books on the Cultural Revolution, Shu Guang Zhang's two books, the PLA histories, the Party-history reference books, and a run of English books on Vietnam, Korea, Japan and the Johnson administration. The TSV marks them in the column `new_since_nov25`.
- The sub-folders were checked for anything created after Nov. 20 or changed after Nov. 25: nothing in JFK OH (589 files), RFK OH (258), Congressional Quarterly (45) or Newsweek (5). The New York Times folder 1960-07-07 holds screenshots uploaded after the inventory's snapshot of its ids; they are pages of a newspaper, not works.
- After grouping volumes, parts and duplicate copies, the 963 top-level files make 625 works or sets of documents. With the CQ issues, the Newsweek issues, the oral histories and the New York Times day folders the TSV has 1,522 rows.
- 157 of the 625 works have no card. The TSV leaves their `card` column empty. They are listed there and not carded, as asked.
- The owner's My Drive outside the shared folder was not opened or listed.

## How much of it the series has read

A work is rated from the repository: its card, the calendar entries that cite it before any "To check:", the claim-map rows, its book-check file, `./bib notes-coverage`, and the briefs and the hand-off that name it. "Read through" means the book-check or the calendar shows every page for the calendar's span was read. "Read in part" means some pages, chapters or years. "Cited only from other works" means the calendar names it behind "To check:" or its card says it was cited by another book, and no one has opened it. "Not read" means no trace of any of these. Pages are the PDF page counts taken from the files; where a file would not be counted, or is an EPUB, the count is estimated from the file's size (the median size per page of the counted files of that size class, with no file put above 1,500 pages) and the TSV says so in the column `pages_basis`.

| Rating | Rows | Files | Pages |
|---|---|---|---|
| read through (for the calendar span) | 21 | 264 | 19,422 |
| read in part | 183 | 276 | 162,291 |
| cited only from other works | 247 | 271 | 109,589 |
| not read | 1,071 | 1,321 | 184,245 |

The oral histories and the CQ, Newsweek and New York Times rows are in those counts. Without them the works are:

| Rating | Works |
|---|---|
| read through (for the calendar span) | 15 |
| read in part | 174 |
| cited only from other works | 205 |
| not read | 231 |

The ratings come from the repository and are not re-checked against the books. The split between "through" and "in part" is least sure: I called a work "through" only for the chronologies, diaries and books whose book-check or calendar cites run across 1960 to 1969, and every other work with any cite or book-check "in part". A work's pages read and unread are in its book-check file.

## The unread, in batches

A batch is the unread works of one subject, read together. "Readers" is the number of reader-runs, as before: pages divided by 70 for a dense book, by 150 for a work read by date (a chronology, a set of documents or hearings, a periodical, a diary, an oral history); each work rounds up. The plan of Nov. 26 did not say which works it read by date; I took chronologies, documents, hearings, reports, periodicals, diaries and letters at 150, and the total fell from 5,202 to 4,872. The 36 CQ issues and the 840 oral histories round up one reader each at least, so their counts overstate. "Queue" is the number of the batch's works that a queue item (9 to 22) or the older queue already reaches. "Proposed Nov. 25 only" counts works that only the runs proposed in the inventory of Nov. 25 name, which wait on this plan. "Neither" counts works no queue item and no earlier proposal reaches. Pages are for the whole file, not only the span. The remainders of works already read in part (old batch R, 51 works, 57,250 pages) are now in the batch of their subject and are marked in the TSV (`moved_from` is R).

Every batch is read by readers one after another (ruling 63): reader 1 works from the tree as it stands, the audit of reader 1's patch is merged, and reader 2 starts from that tree. Batches whose entries do not overlap (another subject, other years) may run at the same time. The reader numbers below are positions in that sequence, counted from the readers' rule above. The same numbers are in the TSV, with the column `order` the position of the work in its batch.

| Batch | Subject | Works | Files | Pages | Readers | Queue | Proposed Nov. 25 only | Neither |
|---|---|---|---|---|---|---|---|---|
| A1 | Soviet leadership and the Kremlin | 11 | 25 | 12,379 | 123 | 3 | 4 | 4 |
| A2 | The Sino-Soviet split | 6 | 6 | 2,143 | 33 | 2 | 1 | 3 |
| A3 | China: leaders, lives, memoirs and Mao | 22 | 31 | 18,786 | 252 | 10 | 0 | 12 |
| A4 | China: the Cultural Revolution | 21 | 25 | 10,314 | 157 | 0 | 0 | 21 |
| A5 | China: the Great Leap, famine, economy and the Third Front | 12 | 16 | 10,367 | 139 | 2 | 0 | 10 |
| A6 | China: party history, foreign relations and the army (reference, documents and the Foreign Ministry files) | 22 | 75 | 16,663 | 183 | 2 | 0 | 20 |
| A8 | Eastern Europe: Czechoslovakia, Romania, Albania, Hungary and the GDR (archives and the Prague Spring) | 8 | 49 | 2,006 | 26 | 4 | 0 | 4 |
| V1 | Vietnam: Hanoi, Saigon and the Vietnamese-language works | 17 | 36 | 11,545 | 117 | 2 | 1 | 14 |
| V2 | Vietnam: American war histories, memoirs and intelligence | 43 | 53 | 21,784 | 288 | 0 | 1 | 42 |
| V3 | Vietnam: Washington, Congress and the protest | 5 | 8 | 4,653 | 68 | 1 | 1 | 3 |
| U1 | The Kennedy and Johnson administrations (lives, memoirs, policy) | 25 | 32 | 20,417 | 292 | 0 | 0 | 25 |
| U2 | Nixon, the Republicans and the presidential campaigns | 53 | 56 | 27,141 | 410 | 20 | 4 | 29 |
| U3 | Congress and its members | 55 | 56 | 10,833 | 179 | 0 | 0 | 55 |
| U4 | Civil rights, King and race (books, FBI files, reports and the civil rights bill) | 49 | 70 | 27,797 | 394 | 10 | 0 | 39 |
| U5 | The FBI, the CIA, the NSA and surveillance | 24 | 52 | 16,478 | 187 | 14 | 0 | 10 |
| U6 | Economy, finance and trade | 15 | 15 | 4,619 | 73 | 0 | 0 | 15 |
| U8 | The parties, liberalism and labor (Democrats, Humphrey) | 16 | 16 | 6,573 | 103 | 1 | 6 | 9 |
| U9 | Cities and States | 6 | 6 | 2,788 | 42 | 1 | 1 | 4 |
| E1 | Apportionment, districts and the vote | 6 | 25 | 4,838 | 45 | 0 | 0 | 6 |
| J1 | The Supreme Court and the Constitution | 7 | 10 | 7,277 | 68 | 0 | 0 | 7 |
| H1 | Poverty, welfare, health and labor | 7 | 9 | 5,483 | 51 | 0 | 0 | 7 |
| D1 | Defense, nuclear strategy, intelligence estimates and space | 17 | 17 | 8,938 | 87 | 0 | 1 | 16 |
| F1 | United States foreign policy (State Department and Senate Foreign Relations documents) | 11 | 11 | 11,438 | 83 | 0 | 0 | 11 |
| W1 | Britain | 11 | 13 | 9,948 | 105 | 6 | 5 | 0 |
| W2 | France | 6 | 22 | 15,368 | 132 | 5 | 1 | 0 |
| W3 | Berlin, Germany and Western Europe | 7 | 7 | 3,140 | 47 | 0 | 4 | 3 |
| W4 | Cuba, the missile crisis and Latin America | 12 | 12 | 5,447 | 78 | 0 | 5 | 7 |
| W5 | Africa | 10 | 10 | 4,301 | 60 | 0 | 2 | 8 |
| W6 | The Middle East | 8 | 11 | 6,769 | 90 | 1 | 1 | 6 |
| W7 | Korea, Japan and South Asia | 5 | 22 | 6,891 | 64 | 0 | 2 | 3 |
| P1 | The press: books on it, the weeklies and the newspapers | 12 | 50 | 4,180 | 51 | 2 | 0 | 10 |
| O1 | Oral histories (JFK and RFK libraries) | 840 | 840 | 29,780 | 845 | 0 | 0 | 840 |
| | Total | 1,369 | 1,686 | 351,084 | 4,872 | 86 | 40 | 1,243 |

Batch A7 (the Foreign Ministry files) and the old batches R and U7 no longer exist; their works are in the batches above. The new batches are V3, U8, U9, E1, J1, H1, D1 and F1. Batch O1 is the 840 oral-history transcripts (about 35 pages each): the JFK Library 587 and the RFK Library 253 (the plan of Nov. 26 gave 577 for the JFK Library; the count by the library named in each row is 587). They are on file, not queued.

## What moved and why

Nothing in `lists/` or `sources/` or on the Drive was changed. Each line is a move from an old batch to a new one, with its reason. A work that stayed in its batch is not listed. Batches A2, W1, W2, W5 and W6 are unchanged.

- A1 to A4, 4 works: Civil War in Guangxi: The Cultural Revolutio; China Under Mao: A Revolution Derailed; Agents of Disorder: Inside China’s Cultural ; A Decade of Upheaval: The Cultural Revolutio. Walder's four books on the Cultural Revolution and the Maoist state are about China, not the Kremlin.
- A1 to D1, 2 works: The Soviet Estimate; Intentions and Capabilities. Prados and the volume of estimates are about American intelligence on Soviet forces, not about the Kremlin; they sit with defense.
- A1 to V1, 1 work: Ilya V. Gaiduk, Confronting Vietnam. Gaiduk's book is about the Soviet side of the Vietnam war.
- A1 to W3, 2 works: Berlin 1961; Driving the Soviets up the Wall. Kempe on Berlin 1961 and Harrison on the Berlin Wall are about Berlin and Germany.
- A1 to W4, 3 works: The Soviet Cuban Missile Crisis; Nuclear Folly; New Russian Evidence on Soviet-Cuban Relatio. Mikoyan's, Plokhy's and Hershberg's books on the missile crisis and Soviet-Cuban relations are about Cuba.
- A1 to W7, 1 work: Kim Il Sung in the Khrushchev Era. Szalontai on Kim Il Sung is about Korea.
- A4 to A3, 5 works: 岁月艰难: 吴法宪回忆录 _Sui yue jian nan; 王力反思录; Li Zuopeng huiyilu; 邱会作回忆录(下); San Ci Da Nan Bu Si Di Luo Ruiqing Da Jiang . The memoirs and lives of the generals and of Wang Li and Luo Ruiqing go with the other lives and memoirs.
- A4 to A5, 2 works: 中国共产党与三线建设; Mao's Third Front: The Militarization of Col. The two books on the Third Front are about industry and defense building.
- A6 to A3, 1 work: Mao Zedong sixiang wansui. The Wansui collection is Mao's own words.
- A7 to A6, 1 work: PRC Foreign Ministry Archives (Wilson Center. The Foreign Ministry files are a record of China's foreign relations; there is no batch of documents.
- A8 to A1, 1 work: Russian archives (RGANI, AVPRF). The Russian archive files (RGANI, AVPRF) are Soviet.
- P1 to U3, 36 works: 36 CQ Weekly issues, in date order. The 36 CQ Weekly issues are Congress's own weekly record.
- U1 to D1, 4 works: Eisenhower and the Missile Gap; The Wizards of Armageddon; ...the Heavens and the Earth; John F. Kennedy and the Missile Gap. The two missile-gap books, Kaplan on the nuclear strategists and McDougall on space are defense and space.
- U1 to F1, 1 work: Dean Rusk. Zeiler's life of Rusk is foreign policy.
- U1 to H1, 3 works: Mr. Social Security; From Opportunity to Entitlement; Launching the War on Poverty. Cohen's life, Davies on the entitlement programs and Gillett on the war on poverty are about welfare, health and poverty.
- U1 to U2, 1 work: In the Arena. Weinberger's memoir is a California Republican's.
- U1 to U9, 1 work: A Nation of Cities. Gelfand's book on urban policy is about the cities.
- U2 to U8, 1 work: Hubert. The Humphrey memoir of 1976 by a friend is a life of Humphrey.
- U2 to U9, 1 work: California Rising. Rarick on Pat Brown is a governor's life.
- U3 to E1, 2 works: On Democracy's Doorstep; The End of Inequality. Smith on One Person One Vote and Ansolabehere are apportionment.
- U3 to J1, 2 works: The Warren Court and American Politics; Explicit and Authentic Acts. Powe on the Warren Court and Kyvig on amending the Constitution are the Court and the Constitution.
- U3 to U4, 1 work: I Shared the Dream. "I Shared the Dream" (taken to be Georgia Davis Powers's memoir) is a civil rights memoir.
- U3 to U8, 12 works: JFK, LBJ, and the Democratic Party; The Decline and Fall of the Liberal Republic; Presidential Party Building; The Losing Parties; Humphrey; Law and Order; The UAW and the Heyday of American Liberalis; The Unraveling of America; Politics and Vision; The President and the Parties; Hubert: An Unauthorized Biography of the Vic; Almost to the Presidency. The books on the parties, liberalism, the ADA, the UAW and the three lives of Humphrey, with Matusow and Flamm on liberalism, form a batch of their own.
- U3 to U9, 4 works: Governing New York City; Goodbye to Good-Time Charlie; Maryland & America, 1940 to 1980; The Ungovernable City. The books on New York, Maryland and the governors are about cities and States.
- U4 to E1, 1 work: Democratic Representation. Dixon on reapportionment leaves civil rights, as ruling 63 directs.
- U4 to H1, 1 work: With Dignity. David on Medicare is about health.
- U4 to U2, 1 work: Nixon. Ambrose's *Nixon* is a life of Nixon.
- U4 to U3, 1 work: Wheeling and dealing confessions of a Capito. Baker's memoir is a Senate staffer's.
- U4 to U8, 2 works: Never stop running; Civil Rights and the Crisis of Liberalism. Martin on the Democratic Party and Chafe on Lowenstein go with the Democrats and liberalism.
- U5 to U4, 6 works: The Informant; "Racial Matters"; The Last Crusade; mkl1a; The FBI and Martin Luther King, Jr.; mlk1b. The coded King files, Garrow's and McKnight's books on the FBI and King, May on the Liuzzo murder and O'Reilly on the FBI and black America are about civil rights.
- U7 to D1, 11 works: hathi-posture-fy67-1966; hathi-posture-fy69-1968; dod-stockpile-fact-sheet-2010; nhhc-ship-force-levels; hathi-posture-statement-fy69-1968; hathi-posture-statement-fy68-1967; cmh-maneuver-and-firepower; hathi-posture-fy66-1965; hathi-posture-fy64-1963; OSDSeries_Vol5; hathi-posture-fy63-1962. The yearly Defense posture statements and the four small Defense and service-history files are about defense.
- U7 to E1, 3 works: Congressional District Data (Census); America Votes (Scammon); hathi-nomination-election-1968. The Census district data, America Votes and the 1968 nomination and election hearings are about apportionment and the vote.
- U7 to F1, 10 works: hathi-sfrc-exec-v16; hathi-current-documents-1962; hathi-current-documents-1963; hathi-sfrc-exec-v15; hathi-dsb-v59; hathi-current-documents-1966; hathi-current-documents-1964; hathi-current-documents-1967; hathi-sfrc-exec-v18; hathi-sfrc-exec-v17. The State Department's yearly documents, the Bulletin and the Senate Foreign Relations executive sessions are about foreign policy.
- U7 to H1, 3 works: hathi-hrg-migratory-labor-1967; hathi-hrg-migratory-labor-1965-1966; hathi-hrg-war-on-poverty-1967.2-jackson. The migratory labor and war-on-poverty hearings are about poverty and labor.
- U7 to J1, 5 works: hathi-hrg-inability-1964; hathi-hrg-prayer-1964.2; hathi-hrg-prayer-1962; hathi-hrg-four-year-term-1966; hathi-hrg-fortas-1968.2. The prayer hearings, the inability hearings, the four-year-term hearings and the Fortas hearings are about the Court and the Constitution.
- U7 to U4, 4 works: FBI Liuzzo files; H. Rep. No. 88-914 (1963); Legislative_History_of_Titles_VII_and_XI; Justice Department task force report January. The Liuzzo files, the Justice Department task force report on King, the Legislative History of Titles VII and XI and H. Rep. 88-914 are about civil rights.
- U7 to U5, 2 works: Dated CIA/NSA memos and cables, 1960-68; Senate hearings on federal data banks (1971,. The Senate data-bank hearings and the dated CIA and NSA memos are about intelligence and surveillance.
- U7 to U6, 1 work: hathi-wmeat-1963-73. "hathi-wmeat-1963-73" is unidentified (see the last section); placed with the economy until a reader opens it.

The 51 remainders (old batch R) went to the batch of their subject:

- R to A1, 2: Prezidium TsK KPSS 1954-64; Brezhnev, Rabochie i dnevnikovye zapisi.
- R to A3, 2: Zhou Enlai nianpu (1949-76); Mao Zedong zhuan, 1949–1976.
- R to A4, 3: The Origins of the Cultural Revolution; The Tragedy of Lin Biao; Mao's Last Revolution.
- R to A5, 2: Yang Jisheng, Mubei; Mao's Great Famine.
- R to A6, 2: Friends and Enemies; Jianguo yilai zhongyao wenxian.
- R to U1, 10: Guns or Butter; The Passage of Power; LBJ's 1968; With Kennedy; We Band of Brothers; Kenneth P. O'Donnell & David F. Powers with ; Robert Kennedy and His Times; Kennedy; Journals, 1952–2000; Robert Kennedy.
- R to U2, 10: Six Crises; The Center Cannot Hold; The Agony of the G.O.P. 1964; The Making of the President 1968; On His Own Terms; RN; Before the Storm; 85 Days; The Making of the President 1964; The Making of the President 1960.
- R to U3, 2: Taxing America; The Fierce Urgency of Now.
- R to U4, 6: Bearing the Cross; Pillar of Fire; Judgment Days; An Idea Whose Time Has Come; At Canaan's Edge; Of Kennedys and Kings.
- R to U6, 1: Gold, Dollars, and Power.
- R to U8, 1: The Education of a Public Man.
- R to V1, 2: Van kien Dang toan tap; Lich su khang chien chong My.
- R to V2, 1: MACV Command History.
- R to V3, 5: Choosing War; Who Spoke Up? American Protest Against the W; The U.S. Government and the Vietnam War; Fulbright; Charles DeBenedetti with Charles Chatfield, .
- R to W3, 1: Lyndon Johnson and Europe.
- R to W4, 1: The Bay of Pigs.

The review of every batch for works that do not belong found the moves above. Two I am least sure of: Chafe's life of Lowenstein (U8; it runs through the Mississippi project, the dump-Johnson drive and Congress, and the first reader may move it back to U4), and Gaiduk (V1; it could stay with the Soviet works). The oral histories are by interviewee, not by subject; I did not split them, because their subjects are not in the file names. The alternative is to read each interview with the batch of its interviewee's subject; the default taken is to read them last, after the subject batches, by library and name.

## Each batch: what it is, and its order of reading

The order in every batch follows one rule. The record and the chronologies come before the books that rest on them (stage 1 and stage 2). Histories and studies come next, earliest publication first, so a later book can be read against an earlier one. Lives, memoirs and diaries come last, because they are the most partial. Series that run by year (the Posture statements, the Current Documents, the Senate Foreign Relations volumes, the CQ issues, the Newsweek issues) go in date order. A reader who finds that a book cited the day before is better read earlier should say so in the audit and the order be changed; the order is a default.

### A1. Soviet leadership and the Kremlin

- 11 works, 25 files, 12,379 pages, 123 readers. It would add 1960 to 1968; threads soviet-union, soviet-union-leadership, defense-soviet-forces, soviet-union-czechoslovakia. The Soviet side is the thinnest large thread: 1,164 calendar entries for the Soviet Union, 212 in 1960 and between 67 and 156 a year after, against 27,834 for China.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 51: Prezidium TsK KPSS 1954-64 (1 to 25); Идеологические комиссии ЦК КПСС 1958 - 1964: (26 to 29); Brezhnev, Rabochie i dnevnikovye zapisi (30 to 46); CWIHP_Bulletin_16 (47 to 50); Russian archives (RGANI, AVPRF) (51).
- Stage 2, histories and studies, readers 52 to 123: The Sword and the Shield (52 to 62); The World Was Going Our Way (63 to 73); A Failed Empire (74 to 80); To Run the World (81 to 91); Записки из чемодана. Тайные дневник...дс...в (92 to 113); Р. Г. Пихоя  СОВЕТСКИЙ СОЮЗ. история власти  (114 to 123).

### A2. The Sino-Soviet split

- 6 works, 6 files, 2,143 pages, 33 readers. The Sino-Soviet works the calendar names behind To check but has not read, with the scholarship the owner put ahead of some nianpu (queue item 12, 4i.3). It would add 1960 to 1969; threads china-moscow-1960, china-moscow, china-polemic, china-border-war, china-foreign.
- Stage 1, histories and studies, readers 1 to 33: The Sino-Soviet Conflict, 1956–1961 (1 to 8); Yi Mao Zhuxi (Remembering Chairman Mao) (9 to 11); The Sino-Soviet Split (12 to 17); The Sino-Soviet Alliance (18 to 22); Economic Cold War: America&_039_s Embargo ag (23 to 28); Li Danhui & Yafeng Xia, Mao and the Sino-Sov (29 to 33).

### A3. China: leaders, lives, memoirs and Mao

- 22 works, 31 files, 18,786 pages, 252 readers. Lives, chronologies, papers and memoirs of the Chinese leaders, with Mao's own words and the memoirs of the army chiefs of 1971; the owner's order for the memoirs is in queue item 12 (4g). It would add 1960 to 1971; threads china-leadership, china-mao, china-liu, china-zhou, china-center, china-luo-ruiqing, china-army.
- Stage 1, chronologies and reference, readers 1 to 15: Zhou Enlai nianpu (1949-76) (1 to 15).
- Stage 2, the record (documents, hearings, reports, periodicals), readers 16 to 24: Zhou Enlai Shuxin Xuanji (16 to 20); Zhou Enlai waijiao wenxuan (21 to 24).
- Stage 3, histories and studies, readers 25 to 86: Mao Zedong sixiang wansui (25); Wang Dongxing gongkai Mao Zedong si shenghuo (26 to 30); Mao The Real Story (Alexander V. Pantsov, St (31 to 41); San Ci Da Nan Bu Si Di Luo Ruiqing Da Jiang  (42 to 47); 晚年周恩来 (48 to 56); 评说晚年周恩来 (57 to 78); 金冲及, 中共中央文献研究室 - 刘少奇传（上、下册） (1998, 中央文献出版社) (79 to 86).
- Stage 4, lives, memoirs and diaries, readers 87 to 252: Huiyi yu Huainian (87 to 96); Liu Shaoqi Yi Sheng (A life of Liu Shaoqi) (97 to 107); Mao Zedong zhuan, 1949–1976 (108 to 140); Li Zuopeng huiyilu (141 to 155); Qiu Huizuo huiyilu (156 to 163); Chen Yun zhuan (4 vols.) (164 to 203); Peng Dehuai Zishu (Memoirs of a Chinese Mars (204 to 208); 岁月艰难: 吴法宪回忆录 _Sui yue jian nan (209 to 216); 汪东兴回忆  毛泽东与林彪反革命集团的斗争  第2版 (217 to 219); 王力反思录 (220 to 236); 邱会作回忆录(下) (237 to 244); 黄峥 - 王光美访谈录 (中央文献出版社) (245 to 252).

### A4. China: the Cultural Revolution

- 21 works, 25 files, 10,314 pages, 157 readers. Works on the Cultural Revolution, the factions and the regions, with the Walder books moved here from A1. The calendar holds 3,300 China entries a year to 1966 and about 1,300 in 1968, so these add detail to a covered thread. It would add 1966 to 1969; threads china-red-guards, china-seizures, china-wuhan, china-may-sixteenth, china-class-ranks, china-ninth-congress.
- Stage 1, the record (documents, hearings, reports, periodicals), reader 1: 中共中央、国务院、中央军委、中央文革 关于广西文化大革命问题的重要文件汇编 (1).
- Stage 2, histories and studies, readers 2 to 143: Peking and the New Left (2 to 4); The Origins of the Cultural Revolution (5 to 22); Born Red (23 to 28); Haojie zhongde yi mu (29 to 32); Red Flower of China (33 to 36); Failure of Charisma (37 to 42); The Tragedy of Lin Biao (43 to 46); Mao's Last Revolution (47 to 57); A Chinese Rebel beyond the Great Wall: The C (58 to 64); Agents of Disorder: Inside China’s Cultural  (65 to 69); Civil War in Guangxi: The Cultural Revolutio (70 to 74); China Under Mao: A Revolution Derailed (75 to 81); Collective killings in rural China during th (82 to 86); A Decade of Upheaval: The Cultural Revolutio (87 to 90); Fractured Rebellion: The Beijing Red Guard M (91 to 96); Geming zaofan niandai (Li Xun) (97 to 120); Shanghai wenhua dageming shihua (draft) (121 to 128); Zai Li Shi De Dang An Li: Wen Ge Shi Nian Fe (129 to 133); 文革受难者 (wang youqin（王友琴）) (134 to 143).
- Stage 3, lives, memoirs and diaries, readers 144 to 157: 内蒙文革风雷——一位造反派领袖的口述史 (144 to 157).

### A5. China: the Great Leap, famine, economy and the Third Front

- 12 works, 16 files, 10,367 pages, 139 readers. The Great Leap, the famine, the economy and the Third Front; queue item 12 (4i.3a) holds Yang Jisheng and Dikotter, which stay with their queue item and are named below only as a remainder. It would add 1960 to 1969; threads china-famine, china-economy, china-agriculture, china-retreat-1962, china-sixty-articles, china-third-front.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 13: 农业集体化重要文件汇编(1958-1981)下册 (1 to 13).
- Stage 2, histories and studies, readers 14 to 139: 'Da Yuejin' Qin Li Ji (A record of my own ex (14 to 27); Zhonghua renmin gongheguo jingji shi, 1949–1 (28 to 38); Mao's Great Famine (39 to 49); Beijing&_039_s Economic Statecraft during th (50 to 63); Mao&_039_s War against Nature: Politics and  (64 to 68); Mao's Third Front: The Militarization of Col (69 to 73); The River Dragon Has Come!: Three Gorges Dam (74 to 77); Yang Jisheng, Mubei (78 to 112); 中国共产党与三线建设 (113 to 122); 大饥荒：1959-1961年的中国人口 (123 to 126); 林蕴晖 - 中华人民共和国史04.乌托邦运动—从大跃进到大饥荒（1958-1961) 0 (127 to 139).

### A6. China: party history, foreign relations and the army (reference, documents and the Foreign Ministry files)

- 22 works, 75 files, 16,663 pages, 183 readers. Party-history chronologies and reference books, the official histories of the army, the border war with India and the Sino-American talks, and the 45 Foreign Ministry files that the Wilson Center translates (queue item 14, Batch 17). Read by date. It would add 1960 to 1969; threads china-foreign, china-india-war, china-army, china-nuclear, china-afro-asian, china-center, china-mao-foreign.
- Stage 1, chronologies and reference, readers 1 to 16: Xin Zhongguo biannianshi (1949–1989) (1 to 5); Zhong Gong Dang Shi Zhong Da Shi Jian Shu Sh (6 to 8); Zhonggong Dangshi Dashi Nianbiao (A chronolo (9 to 12); 中国共产党历史大事记 (13 to 16).
- Stage 2, the record (documents, hearings, reports, periodicals), readers 17 to 60: Jianguo yilai zhongyao wenxian (17 to 58); PRC Foreign Ministry Archives (Wilson Center (59 to 60).
- Stage 3, histories and studies, readers 61 to 183: India's China War (61 to 68); Friends and Enemies (69 to 74); Yuan Yue Kang Mei Shilu (75 to 83); Xin Zhongguo Liu Ci Fan Qinlue Zhanzheng Shi (84 to 88); Zhong-Yin bianjing ziwei fanji zuozhan shi (89 to 93); Zhonghua renmin gongheguo fengyun shilu, 2 v (94 to 115); Negotiating with the Enemy (116 to 121); 1949-1989年的中国_曲折发展的岁月 (122 to 131); Spying for the People: Mao’s Secret Agents,  (132 to 135); Zhongguo Gong Chan Dang Zhi Zheng Si Shi Nia (136 to 145); 中国人民解放军军史 第五卷 (《中国人民解放军军史》编写组) (146 to 151); 中国人民解放军军史 第六卷 (《中国人民解放军军史》编写组) (152 to 158); 中国共产党重大史实考证  (第一-四卷) (159 to 169); 中美会谈九年回顾 (170 to 172); 困守与反攻 (173 to 177); 第5卷. 歷史的變局: 從挽救危機到反修防修, 1962-1965 - 錢庠理 (178 to 183).

### A8. Eastern Europe: Czechoslovakia, Romania, Albania, Hungary and the GDR (archives and the Prague Spring)

- 8 works, 49 files, 2,006 pages, 26 readers. Czechoslovak, Romanian, Albanian, Hungarian and East German files, and the works on the Prague Spring; queue item 14 holds the archives. It would add 1965 to 1968; threads soviet-union-czechoslovakia, comecon, china-foreign, vietnam-hanoi, europe-and-the-alliance.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 11: MOL XIX-J-1j SZU.IV-10.003348.1966 104.d (1); „Пражская весна“ и международный кризис 1968 (2 to 4); Albanian archives (AQSH) (5); Hungarian archives (MOL) (6); Romanian archives (ANR, AMAE) (7 to 10); Stasi (BStU, MfS Abt. X) (11).
- Stage 2, histories and studies, readers 12 to 26: The Prague Spring and Its Aftermath (12 to 16); Jaromir Navratíl (editor): Antonín Benčík (e (17 to 26).

### V1. Vietnam: Hanoi, Saigon and the Vietnamese-language works

- 17 works, 36 files, 11,545 pages, 117 readers. Hanoi's side, Saigon's side and the Vietnamese-language works, with Gaiduk on Soviet policy moved here. Queue item 13 (Batch 16) is about page cites to works already read, not these. It would add 1960 to 1969; threads vietnam-hanoi, vietnam-saigon, vietnam-elections, vietnam-tet, vietnam-struggle.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 51: 8058 – “Báo cáo của Phó Thủ tướng Lê Thanh N (1); Lich su khang chien chong My (2 to 24); Van kien Dang toan tap (25 to 51).
- Stage 2, histories and studies, readers 52 to 93: The Twenty-Five Year Century (52 to 58); Voices from the Second Republic of South Vie (59 to 61); The Vietnam War (62 to 66); Vietnam's Communist Revolution (67 to 73); The Republic of Vietnam 1955–1975 (74 to 77); Building a Republican Nation in Vietnam, 192 (78 to 81); HAI MƯƠI NĂM QUA Việc từng ngày (1945-1964)  (82 to 85); Ilya V. Gaiduk, Confronting Vietnam (86 to 90); Những ngày chưa quên (1954-1963) (91 to 93).
- Stage 3, lives, memoirs and diaries, readers 94 to 117: Twenty Years and Twenty Days (94 to 97); Our Endless War (98 to 102); Hoàng Linh Đỗ Mậu, Việt Nam (103 to 108); Hồi ký chính trị 1965-1975 đại tá Phạm Bá Ho (109 to 111); Nguyen Cao Ky with Marvin J. Wolf, Buddha's  (112 to 117).

### V2. Vietnam: American war histories, memoirs and intelligence

- 43 works, 53 files, 21,784 pages, 288 readers. American histories, memoirs and intelligence studies of the war on the ground and in Saigon. It would add 1960 to 1969; threads vietnam-commitments, vietnam-operations, vietnam-macv, vietnam-pacification, vietnam-tet, vietnam-khe-sanh.
- Stage 1, chronologies and reference, readers 1 to 8: Facts on File, South Vietnam (Sobel, Millet) (1 to 8).
- Stage 2, the record (documents, hearings, reports, periodicals), readers 9 to 41: MACV Command History (9 to 31); Porter, Vietnam (32 to 41).
- Stage 3, histories and studies, readers 42 to 275: South Vietnam (42 to 45); The Two Viet-Nams (46 to 51); The Last Confucian (52 to 56); Our Vietnam Nightmare (57 to 61); The Making of a Quagmire (62 to 66); The Lost Revolution (67 to 73); Viet Cong (74 to 82); Westmoreland (83 to 88); War Comes to Long An (89 to 93); Politics in War (94 to 98); The War Managers (99 to 102); America in Vietnam (103 to 110); The McNamara Strategy and the Vietnam War (111 to 113); Village at War (114 to 117); Vietnam (118 to 129); William Fulbright and the Vietnam War (130 to 133); War by Other Means (134 to 138); The Tet Offensive (139 to 143); Trapped by Success (144 to 148); The Johnson Years (149 to 156); Lodge in Vietnam (157 to 160); Mansfield and Vietnam (161 to 166); American Tragedy (167 to 175); Kennedy's Wars (176 to 184); Our Vietnam (185 to 196); Death of a Generation (197 to 205); Cold War Mandarin (206 to 209); Inventing Vietnam (210 to 213); Vietnam's Forgotten Army (214 to 219); Nine Days in May (220 to 226); Drawn Swords in a Distant Land (227 to 233); The History of South Vietnam (234 to 236); An eye for the dragon; Southeast Asia observ (237 to 243); Intervention (244 to 252); South Vietnam; a political history, 1954-197 (253 to 255); The Tuesday Cabinet; deliberation and decisi (256 to 259); Vietnam: A Dragon Embattled (260 to 269); Village in Vietnam (270 to 275).
- Stage 4, lives, memoirs and diaries, readers 276 to 288: In the Midst of Wars (276 to 282); In the jaws of history (283 to 288).

### V3. Vietnam: Washington, Congress and the protest

- 5 works, 8 files, 4,653 pages, 68 readers. The war as American government and public business: the executive and Congress, Fulbright and Mansfield, the choice of 1964 to 1965, the protest. It would add 1961 to 1969; threads vietnam-commitments, vietnam-congress, vietnam-hearings, vietnam-protest.
- Stage 1, histories and studies, readers 1 to 57: Who Spoke Up? American Protest Against the W (1 to 7); The U.S. Government and the Vietnam War (8 to 40); Choosing War (41 to 49); Charles DeBenedetti with Charles Chatfield,  (50 to 57).
- Stage 2, lives, memoirs and diaries, readers 58 to 68: Fulbright (58 to 68).

### U1. The Kennedy and Johnson administrations (lives, memoirs, policy)

- 25 works, 32 files, 20,417 pages, 292 readers. Lives and memoirs of the Kennedy and Johnson circle, and the policy histories of their administrations, cited behind To check and never read. It would add 1960 to 1969; threads white-house, transition-and-staff, program, succession.
- Stage 1, histories and studies, readers 1 to 231: Kennedy (1 to 12); Lyndon B. Johnson (13 to 69); The Johnson Eclipse (70 to 74); Robert F. Kennedy (75 to 93); John F. Kennedy and the Second Reconstructio (94 to 99); Robert Kennedy and His Times (100 to 115); Promises Kept (116 to 121); Guns or Butter (122 to 131); Robert Kennedy (132 to 139); LBJ (140 to 165); Legacies of Camelot (166 to 169); The Passage of Power (170 to 181); The Patriarch (182 to 195); LBJ's 1968 (196 to 201); Dallek on Johnson (202 to 223); Kenneth P. O'Donnell & David F. Powers with  (224 to 231).
- Stage 2, lives, memoirs and diaries, readers 232 to 292: The Professional (232 to 236); With Kennedy (237 to 243); Ambassador's Journal (244 to 248); We Band of Brothers (249 to 254); Lyndon (255 to 264); Spanning the Century (265 to 274); Chief of Staff (275 to 280); Journals, 1952–2000 (281 to 287); P: S (288 to 292).

### U2. Nixon, the Republicans and the presidential campaigns

- 53 works, 56 files, 27,141 pages, 410 readers. Nixon, the Republicans and the campaigns of 1960, 1964 and 1968; queue item 20 (Batch 18) holds most of it. It would add 1960, 1964 and 1968; threads elections-1960-nixon, elections-1964-goldwater, elections-1968-nixon, elections-1968-republican-nomination, republican-party, conservative-movement.
- Stage 1, histories and studies, readers 1 to 307: The Making of the President 1960 (1 to 6); The Agony of the G.O.P. 1964 (7 to 13); The Making of the President 1964 (14 to 20); Five States for Goldwater (21 to 23); George Romney (24 to 29); 85 Days (30 to 34); McCarthy for President (35 to 39); The Making of the President 1968 (40 to 46); The Selling of the President 1968 (47 to 50); Nixon Agonistes (51 to 60); Nobody Knows (61 to 66); The Resurrection of Richard Nixon (67 to 73); Catch the Falling Flag (74 to 78); White Knight (79 to 85); Rockefeller of New York (86 to 97); Making It Perfectly Clear (98 to 105); Nixon (106 to 127); 1968 in America (128 to 135); One of Us (136 to 146); Goldwater (147 to 155); The Right Moment (156 to 160); A Time for Choosing (161 to 165); Before the Storm (166 to 176); Suburban Warriors (177 to 182); Governor Reagan (183 to 191); A Glorious Disaster (192 to 196); 1960 (197 to 205); The Center Cannot Hold (206 to 209); The Making of a Catholic President (210 to 213); The Real Making of the President (214 to 217); Resilient America (218 to 223); The Greatest Comeback (224 to 230); The President and the Apprentice (231 to 242); Richard Nixon (243 to 254); American Maelstrom (255 to 260); Eisenhower the President (261 to 266); Goldwater (267 to 273); Irwin F. Gellman - Campaign of the Century:  (274 to 281); Luke A. Nichter - The Year That Broke Politi (282 to 287); The Men and the Moment (288 to 291); The road to Camelot (292 to 298); We Were the Campaign: New Hampshire to Chica (299 to 302); Winning's a lot more fun (303 to 307).
- Stage 2, lives, memoirs and diaries, readers 308 to 410: Six Crises (308 to 321); With Nixon (322 to 328); RN (329 to 346); With No Apologies (347 to 351); The Imperial Rockefeller (352 to 356); Crazy Rhythm (357 to 363); In the Arena (364 to 370); Richard M. Nixon (371 to 387); On His Own Terms (388 to 401); Aitken, Jonathan: Nixon, Richard Milhous - N (402 to 410).

### U3. Congress and its members

- 55 works, 56 files, 10,833 pages, 179 readers. The House and Senate through the lives of their members, the weekly record of Congress (36 CQ Weekly issues, moved here from the press batch), and the Mills and Johnson legislative histories. It would add 1960 to 1969; threads congress, rules, house, senate.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 36: 36 CQ Weekly issues, in date order, from 1962-05-04 to 1968-12-27 (1 to 36).
- Stage 2, histories and studies, readers 37 to 103: Dirksen (37 to 43); Dirksen of Illinois (44 to 48); Keeper of the Rules (49 to 59); Richard B. Russell, Jr., Senator from Georgi (60 to 68); Colleagues (69 to 73); Taxing America (74 to 79); Mike Mansfield, Majority Leader (80 to 84); Everett Dirksen and His Presidents (85 to 90); On Capitol Hill (91 to 96); The Fierce Urgency of Now (97 to 103).
- Stage 3, lives, memoirs and diaries, readers 104 to 179: In the Fullness of Time (104 to 113); Preserving the Constitution (114 to 120); Fighting the Odds (121 to 132); Henry M. Jackson (133 to 141); Senator Mansfield (142 to 151); Strom (152 to 158); Javits (159 to 167); Sam Rayburn a biography (Steinberg, Alfred,  (168 to 174); Wheeling and dealing confessions of a Capito (175 to 179).

### U4. Civil rights, King and race (books, FBI files, reports and the civil rights bill)

- 49 works, 70 files, 27,797 pages, 394 readers. Civil rights, King, the South and race, with the civil rights bill's own record (the House report, the legislative history of Titles VII and XI), the FBI Liuzzo files, the two coded King files and the books on the FBI and King moved here. Many of the books are cited dozens of times behind To check; queue item 18 holds the King and FBI group. It would add 1960 to 1969; threads king, civil-rights-bill, voting-rights-selma, freedom-rides, sit-ins, mississippi, alabama-birmingham, civil-disorders.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 28: H. Rep. No. 88-914 (1963) (1 to 3); Justice Department task force report January (4 to 6); FBI Liuzzo files (7 to 21); Legislative_History_of_Titles_VII_and_XI (22 to 26); mkl1a (27); mlk1b (28).
- Stage 2, histories and studies, readers 29 to 347: A Bill Becomes a Law (29 to 31); Wallace (32 to 35); Black Ballots (36 to 43); Southern Governors and Civil Rights (44 to 50); The Transformation of Southern Politics (51 to 58); Protest at Selma (59 to 64); Of Kennedys and Kings (65 to 72); The FBI and Martin Luther King, Jr. (73 to 88); At the River I Stand (89 to 94); Bearing the Cross (95 to 106); To Redeem the Soul of America (107 to 114); We Are Not Afraid (115 to 122); "Racial Matters" (123 to 129); And the Walls Came Tumbling Down (130 to 142); The Civil Rights Era (143 to 151); To End All Segregation (152 to 157); Calculating Visions (158 to 167); George Wallace (168 to 177); I've Got the Light of Freedom (178 to 194); Race and Democracy (195 to 204); Pillar of Fire (205 to 216); The Last Crusade (217 to 220); Carry Me Home (221 to 231); Kennedy, Johnson, and the Quest for Justice (232 to 237); Judgment Days (238 to 245); The Informant (246 to 252); At Canaan's Edge (253 to 268); The Bystander (269 to 277); Delaying the Dream (278 to 283); Some of It Was Fun (284 to 288); Sweet Land of Liberty (289 to 300); The Fifth Freedom (301 to 307); Racial Propositions (308 to 313); Behind the Dream (314 to 317); James J. Kilpatrick (318 to 322); The March on Washington (323 to 327); An Idea Whose Time Has Come (328 to 334); I Shared the Dream (335 to 340); The Judas factor (341 to 347).
- Stage 3, lives, memoirs and diaries, readers 348 to 394: My Life with Martin Luther King, Jr. (348 to 371); The Death and Life of Malcolm X (372 to 379); Lay Bare the Heart (380 to 385); Malcolm X (386 to 394).

### U5. The FBI, the CIA, the NSA and surveillance

- 24 works, 52 files, 16,478 pages, 187 readers. The FBI as an institution, the CIA, the NSA and the Army at home, the Hoover lives, the Church and House assassination reports and the Senate data-bank hearings; queue item 18 holds most of it. It would add 1960 to 1974; threads intelligence, antisubversion, assassination.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 58: Dated CIA/NSA memos and cables, 1960-68 (1 to 3); Senate hearings on federal data banks (1971, (4 to 42); NARA RG 59 (INR) reports (43); NSA-60th-Anniversary (44); Report_of_the_Select_Committee_on_Assass (45 to 49); Security_Practices_in_the_National_Secur (50); The COINTELPRO papers (51 to 54); sites-default-files-94465 (55 to 57); “Betrayers of the Trust” (part), National Se (58).
- Stage 2, histories and studies, readers 59 to 112: The Age of Surveillance (59 to 67); Army Surveillance in America, 1775–1980 (68 to 72); Enemies (73 to 81); MH_CHAOS (82 to 95); Secrets (96 to 99); The secret sentry (100 to 106); There’s Something Happening Here (107 to 112).
- Stage 3, lives, memoirs and diaries, readers 113 to 187: Secrecy and Power (113 to 122); The Boss (123 to 130); J. Edgar Hoover (131 to 143); Hoover's FBI (144 to 150); G-Man (151 to 163); From the secret files of J: Edgar Hoover (164 to 169); Spying on Americans (170 to 182); William C. Sullivan with Bill Brown, The Bur (183 to 187).

### U6. Economy, finance and trade

- 15 works, 15 files, 4,619 pages, 73 readers. Money, the budget, the Federal Reserve and trade. It would add 1960 to 1969; threads economy, economy-gold, economy-franc, economy-surcharge, trade.
- Stage 1, the record (documents, hearings, reports, periodicals), reader 1: hathi-wmeat-1963-73 (1).
- Stage 2, histories and studies, readers 2 to 73: New Dimensions of Political Economy (2 to 5); The Dollar and World Liquidity (6 to 11); The Political Economy of Prosperity (12 to 14); The Arena of International Finance (15 to 18); The International Monetary System, 1945–1976 (19 to 25); Presidential Economics (26 to 33); Eisenhower Versus "The Spenders" (34 to 37); American Trade and Power in the 1960s (38 to 43); Deficit Government (44 to 47); Globalizing Capital (48 to 52); Butter and Guns (53 to 57); Chairman of the Fed (58 to 63); Gold, Dollars, and Power (64 to 68); More: The Politics of Economic Growth in Pos (69 to 73).

### U8. The parties, liberalism and labor (Democrats, Humphrey)

- 16 works, 16 files, 6,573 pages, 103 readers. The Democratic and Republican parties as organisations, liberalism, the unions, and the lives of Humphrey. It would add 1960 to 1969; threads democratic-party, republican-party, labor, elections-1968-humphrey.
- Stage 1, histories and studies, readers 1 to 74: Civil Rights and the Crisis of Liberalism (1 to 5); The Unraveling of America (6 to 14); Politics and Vision (15 to 19); The Decline and Fall of the Liberal Republic (20 to 24); The President and the Parties (25 to 31); The Losing Parties (32 to 36); The UAW and the Heyday of American Liberalis (37 to 42); JFK, LBJ, and the Democratic Party (43 to 49); Law and Order (50 to 54); Presidential Party Building (55 to 60); Hubert (61 to 65); Never stop running (66 to 74).
- Stage 2, lives, memoirs and diaries, readers 75 to 103: Almost to the Presidency (75 to 83); The Education of a Public Man (84 to 91); Hubert: An Unauthorized Biography of the Vic (92 to 97); Humphrey (98 to 103).

### U9. Cities and States

- 6 works, 6 files, 2,788 pages, 42 readers. The cities (New York, Maryland, California) and the governors. It would add 1960 to 1969; threads mayors, states-and-cities, governors, state-and-city-finance.
- Stage 1, histories and studies, readers 1 to 42: Governing New York City (1 to 6); A Nation of Cities (7 to 14); Goodbye to Good-Time Charlie (15 to 18); Maryland & America, 1940 to 1980 (19 to 24); The Ungovernable City (25 to 34); California Rising (35 to 42).

### E1. Apportionment, districts and the vote

- 6 works, 25 files, 4,838 pages, 45 readers. Apportionment and reapportionment, the districts as they stood, and the election returns; moved out of civil rights by ruling 63. It would add 1960 to 1968; threads reapportionment, elections-1962, elections-1964, elections-1968, congress.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 24: hathi-nomination-election-1968 (1 to 2); America Votes (Scammon) (3 to 18); Congressional District Data (Census) (19 to 24).
- Stage 2, histories and studies, readers 25 to 45: Democratic Representation (25 to 34); The End of Inequality (35 to 39); On Democracy's Doorstep (40 to 45).

### J1. The Supreme Court and the Constitution

- 7 works, 10 files, 7,277 pages, 68 readers. The Supreme Court and the Constitution: the prayer decisions, presidential inability and the 25th Amendment, the four-year term, the Fortas nomination, the Warren Court. It would add 1962 to 1968; threads court, court-fortas, constitution.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 35: hathi-hrg-prayer-1962 (1 to 2); hathi-hrg-inability-1964 (3 to 4); hathi-hrg-prayer-1964.2 (5 to 24); hathi-hrg-four-year-term-1966 (25); hathi-hrg-fortas-1968.2 (26 to 35).
- Stage 2, histories and studies, readers 36 to 68: Explicit and Authentic Acts (36 to 53); The Warren Court and American Politics (54 to 68).

### H1. Poverty, welfare, health and labor

- 7 works, 9 files, 5,483 pages, 51 readers. Poverty, welfare, health and farm and migrant labor: the hearings and the books on the programs. It would add 1960 to 1969; threads poverty, program, jobs-and-wages, health.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 28: hathi-hrg-migratory-labor-1965-1966 (1 to 6); hathi-hrg-migratory-labor-1967 (7 to 20); hathi-hrg-war-on-poverty-1967.2-jackson (21 to 28).
- Stage 2, histories and studies, readers 29 to 44: With Dignity (29 to 32); From Opportunity to Entitlement (33 to 37); Launching the War on Poverty (38 to 44).
- Stage 3, lives, memoirs and diaries, readers 45 to 51: Mr. Social Security (45 to 51).

### D1. Defense, nuclear strategy, intelligence estimates and space

- 17 works, 17 files, 8,938 pages, 87 readers. Defense posture, nuclear strategy, the estimates of Soviet strength and space. The Posture statements are the Secretary of Defense's yearly statements to Congress. It would add 1962 to 1968; threads defense, defense-soviet-forces, space, missile-gap.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 49: hathi-posture-fy63-1962 (1 to 5); hathi-posture-fy64-1963 (6 to 10); hathi-posture-fy66-1965 (11 to 15); hathi-posture-fy67-1966 (16 to 25); hathi-posture-statement-fy68-1967 (26 to 28); hathi-posture-fy69-1968 (29 to 39); hathi-posture-statement-fy69-1968 (40 to 41); OSDSeries_Vol5 (42 to 46); cmh-maneuver-and-firepower (47); dod-stockpile-fact-sheet-2010 (48); nhhc-ship-force-levels (49).
- Stage 2, histories and studies, readers 50 to 87: The Soviet Estimate (50 to 55); The Wizards of Armageddon (56 to 62); ...the Heavens and the Earth (63 to 71); Eisenhower and the Missile Gap (72 to 75); Intentions and Capabilities (76 to 83); John F. Kennedy and the Missile Gap (84 to 87).

### F1. United States foreign policy (State Department and Senate Foreign Relations documents)

- 11 works, 11 files, 11,438 pages, 83 readers. The State Department's yearly documents, the Department of State Bulletin of 1968 and the Senate Foreign Relations Committee's executive-session volumes of 1963 to 1966. These carry every foreign subject; each reader dates what the page reports. It would add 1962 to 1968; threads europe-and-the-alliance, vietnam-diplomacy, vietnam-congress, foreign-policy.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 79: hathi-current-documents-1962 (1 to 12); hathi-current-documents-1963 (13 to 22); hathi-current-documents-1964 (23 to 32); hathi-current-documents-1966 (33 to 41); hathi-current-documents-1967 (42 to 51); hathi-dsb-v59 (52 to 57); hathi-sfrc-exec-v15 (58 to 64); hathi-sfrc-exec-v16 (65 to 67); hathi-sfrc-exec-v17 (68 to 72); hathi-sfrc-exec-v18 (73 to 79).
- Stage 2, histories and studies, readers 80 to 83: Dean Rusk (80 to 83).

### W1. Britain

- 11 works, 13 files, 9,948 pages, 105 readers. Britain has no thread of its own; the alliance thread has a Britain strand. The Nov. 25 inventory proposed a Britain run and noted the owner has not said whether Britain is a covered nation (default taken: yes). It would add 1960 to 1970; threads europe-and-the-alliance-britain, europe-and-the-alliance, vietnam-diplomacy, economy-gold.
- Stage 1, histories and studies, readers 1 to 55: The Labour Government, 1964–1970 (1 to 13); Harold Wilson (14 to 26); Never Had It So Good (27 to 40); White Heat (41 to 55).
- Stage 2, lives, memoirs and diaries, readers 56 to 105: The Cecil King Diary 1965–1970 (56 to 58); The Diaries of a Cabinet Minister, vol. 3 (59 to 76); The Castle Diaries 1964–70 (77 to 82); Out of the Wilderness (83 to 87); Office Without Power (88 to 91); Wilson (92 to 101); Years of Hope (102 to 105).

### W2. France

- 6 works, 22 files, 15,368 pages, 132 readers. de Gaulle's letters and notes, Peyrefitte, Viansson-Ponte and the Documents diplomatiques francais; queue item 21 holds the French pilot. It would add 1960 to 1969; threads europe-and-the-alliance-france, european-community, economy-franc.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 82: Discours et messages, vol. 4 (1 to 4); DDF (5 to 59); de Gaulle, Lettres, notes et carnets (60 to 82).
- Stage 2, histories and studies, readers 83 to 124: C'était de Gaulle (83 to 104); Viansson-Ponte, Histoire de la Republique ga (105 to 124).
- Stage 3, lives, memoirs and diaries, readers 125 to 132: Mémoires d'espoir (125 to 132).

### W3. Berlin, Germany and Western Europe

- 7 works, 7 files, 3,140 pages, 47 readers. Berlin, Germany and Western Europe, with the two Berlin books moved here from A1 and Schwartz on Johnson and Europe moved here from the remainders. The German pilot in queue item 21 is not yet chosen. It would add 1960 to 1969; threads europe-and-the-alliance-federal-republic, berlin-and-vienna, european-community.
- Stage 1, chronologies and reference, readers 1 to 3: Germany and Eastern Europe since 1945 (1 to 3).
- Stage 2, histories and studies, readers 4 to 47: Adenauer and Kennedy (4 to 6); A Constructed Peace (7 to 13); Driving the Soviets up the Wall (14 to 19); Lyndon Johnson and Europe (20 to 25); Berlin 1961 (26 to 35); Adenauer Bd: 2: Der Staatsmann (36 to 47).

### W4. Cuba, the missile crisis and Latin America

- 12 works, 12 files, 5,447 pages, 78 readers. Cuba, the missile crisis and Latin America, with the Mikoyan, Plokhy and Hershberg books moved here from A1 and Jones on the Bay of Pigs from the remainders. The missile crisis and Bay of Pigs have heavy coverage, the rest less. It would add 1960 to 1969; threads cuba, cuba-bay-of-pigs, missile-crisis, latin-america, latin-america-dominican-republic.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 3: CIA Documents on the Cuban Missle Crisis of  (1 to 3).
- Stage 2, histories and studies, readers 4 to 78: Eisenhower and Latin America (4 to 7); The Most Dangerous Area in the World (8 to 11); The Castro Obsession (12 to 16); The Bay of Pigs (17 to 20); That Infernal Little Cuban Republic (21 to 31); The Soviet Cuban Missile Crisis (32 to 40); Back Channel to Cuba (41 to 48); New Russian Evidence on Soviet-Cuban Relatio (49); Nuclear Folly (50 to 65); Cuba on the brink (66 to 73); G. Pope Atkins - The Dominican Republic and  (74 to 78).

### W5. Africa

- 10 works, 10 files, 4,301 pages, 60 readers. Africa and the Congo, 253 and 201 calendar entries. It would add 1960 to 1969; threads africa, africa-algeria-morocco, congo, congo-lumumba.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 7: сост.: Антошин А. В. и др. (1 to 7).
- Stage 2, histories and studies, readers 8 to 60: Crisis in the Congo (8 to 11); American Foreign Policy in the Congo, 1960–1 (12 to 18); The Congo Cables (19 to 26); JFK (27 to 32); Cold War and Black Liberation (33 to 37); A Diplomatic Revolution (38 to 44); Betting on the Africans (45 to 50); Death in the Congo (51 to 55); Africa independent;: A survey of political d (56 to 60).

### W6. The Middle East

- 8 works, 11 files, 6,769 pages, 90 readers. The Middle East, 374 calendar entries, 98 of them in 1967; queue item 17 holds Pollack. It would add 1960 to 1969; threads middle-east, middle-east-six-day-war, middle-east-yemen, middle-east-iran-oil.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 10: Naumkin, Blizhnevostochnyi konflikt (documen (1 to 10).
- Stage 2, histories and studies, readers 11 to 90: The Turkish Revolution, 1960–1961 (11 to 13); The Other Arab-Israeli Conflict (14 to 29); The Eagle and the Lion (30 to 37); Peace Process (38 to 45); Arabs at War (46 to 78); Support Any Friend (79 to 84); Nasser's Gamble (85 to 90).

### W7. Korea, Japan and South Asia

- 5 works, 22 files, 6,891 pages, 64 readers. Korea, Japan and India, with Szalontai on Kim Il Sung moved here from A1; the Japanese files are the ones whose names give no title (see the last section). A few hundred calendar entries between them. It would add 1960 to 1969; threads japan, japan-and-korea, korea, south-asia, india-and-china-kashmir.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 33: Japan (1 to 33).
- Stage 2, histories and studies, readers 34 to 64: Protest in Tokyo (34 to 40); Kim Il Sung in the Khrushchev Era (41 to 46); Nation Building in South Korea (47 to 51); The Park Chung Hee Era (52 to 64).

### P1. The press: books on it, the weeklies and the newspapers

- 12 works, 50 files, 4,180 pages, 51 readers. The press: three books on it, Keesing's for 1963 to 1964, five Newsweek issues of January 1968, one New Yorker, one New York Times day. The 36 CQ Weekly issues that stood here have moved to U3. It would add 1960, 1963 to 1964 and 1968; threads press-and-broadcasting, elections-1968.
- Stage 1, chronologies and reference, readers 1 to 10: KEESING'S Contemporary archives: Vol: 14: 19 (1 to 10).
- Stage 2, the record (documents, hearings, reports, periodicals), readers 11 to 16: NYT 1960-07-07 (day folder, 39 pages as imag (11); Newsweek 1968-01-01 (12); Newsweek 1968-01-08 (13); Newsweek 1968-01-15 (14); Newsweek 1968-01-22 (15); Newsweek 1968-01-29 (16).
- Stage 3, histories and studies, readers 17 to 45: The Powers That Be (17 to 28); The Place to Be (29 to 35); Heather Hendershot - When the News Broke: Ch (36 to 41); The New Yorker  1960-11-05: Vol 36 Iss 38 (42 to 45).
- Stage 4, lives, memoirs and diaries, readers 46 to 51: Confessions of a muckraker (46 to 51).

### O1. Oral histories (JFK and RFK libraries)

- 840 transcripts, 29,780 pages, 845 readers. Oral histories (JFK and RFK libraries) would add 1960 to 1968; all threads with a Kennedy or Johnson side. The hand-off keeps them on file, not queued.
- Stage 1, the JFK Library, 587 transcripts in the order of the interviewee's name, then the interview number; stage 2, the RFK Library, 253 in the same order. A reader takes about 150 pages, a few transcripts of one interviewee together. The first reader of each library should say whether the transcripts are better read by interviewee's subject, and the order be changed.

## What the queue holds and what it does not

- U3 to U4, 1 work: I Shared the Dream. "I Shared the Dream" (taken to be Georgia Davis Powers's memoir) is a civil rights memoir.
- U3 to U8, 12 works: JFK, LBJ, and the Democratic Party; The Decline and Fall of the Liberal Republic; Presidential Party Building; The Losing Parties; Humphrey; Law and Order; The UAW and the Heyday of American Liberalis; The Unraveling of America; Politics and Vision; The President and the Parties; Hubert_ An Unauthorized Biography of the Vic; Almost to the Presidency. The books on the parties, liberalism, the ADA, the UAW and the three lives of Humphrey, with Matusow and Flamm on liberalism, form a batch of their own.
- U3 to U9, 4 works: Governing New York City; Goodbye to Good-Time Charlie; Maryland & America, 1940 to 1980; The Ungovernable City. The books on New York, Maryland and the governors are about cities and States.
- U4 to E1, 1 work: Democratic Representation. Dixon on reapportionment leaves civil rights, as ruling 63 directs.
- The works no queue item reaches, by batch: A1 4; A2 3; A3 12; A4 21; A5 10; A6 20; A8 4; V1 14; V2 42; V3 3; U1 25; U2 29; U3 55; U4 39; U5 10; U6 15; U8 9; U9 4; E1 6; J1 7; H1 7; D1 16; F1 11; W3 3; W4 7; W5 8; W6 6; W7 3; P1 10.

## A suggested order of batches

The calendar's weight is lopsided. China has 27,834 of its 59,038 entries and Vietnam 7,720, the 1968 elections 1,512, the Soviet Union 1,164. Europe and the alliance has 373, the Middle East 374, Africa 253, Korea and Japan about 300, South Asia 157. The order below puts what the owner already queued first, then the subjects the calendar covers least, then the large subjects the calendar covers already. Within a step the batches may run at the same time if their entries do not overlap; two batches that touch the same entries (the civil rights bill, the Court, the 1968 campaign) go one after the other. Within every batch, readers go one after another.

1. Queue items 12, 13, 14, 17, 18, 20 and 21, which name Drive works, in the owner's order. This plan changes none of them. Where a queue item names a work now in a recut batch (item 18: the King and FBI group, now in U4 and U5; item 14: the Foreign Ministry files, now in A6 and the archives in A8), the queue item keeps it and the batch drops it when the item has read it.
2. A1, the Soviet leadership, then A2, the Sino-Soviet split: the thinnest large thread, and the works the Nov. 25 inventory already described (its Runs A and B). W3 and W4 (Berlin and Germany; Cuba and the missile crisis) may run beside them, since their entries are other threads.
3. W1, W2, W5, W6 and W7 (Britain, France, Africa, the Middle East, Korea and Japan): small batches, each adding entries to threads with a few hundred. Britain waits on the owner's word on whether it is a covered nation; the default taken is yes. These five touch different threads and may run side by side.
4. U4, then E1, J1 and U3: the American books the calendar names behind To check many times and has never read (The Warren Court and American Politics 67; Democratic Representation 42; The Civil Rights Era 36; To Redeem the Soul of America 32; Protest at Selma 28; Black Ballots 27). U4 first because it carries the record of the civil rights bill; E1 and J1 then read the apportionment and Court material against it; U3 last of the four because the CQ issues cover all three. These four overlap, so they run one after the other.
5. U1, with H1, D1 and F1 beside it: the Kennedy and Johnson administrations, poverty and health, defense and space, foreign policy documents.
6. U2 and U5 as queue items 20 and 18 set them; U8 and U9 beside them; U6 after.
7. A3, A4, A5, A6 and A8: China and the archives. The queue's item 12 and item 14 come first; these are the rest. They are the largest batches by pages, and China is already the calendar's biggest thread. A6 goes first (chronologies, then the Foreign Ministry files), A3 next, then A4 and A5 together, then A8.
8. V1, V2 and V3: Vietnam, already the second-largest thread, after the above. V3 (Congress and the protest) may run beside V1.
9. P1, then O1: the press and the weeklies, and the oral histories, which the hand-off keeps on file.

Each batch would be briefed as the owner's rules direct: R0 first, the first pass on Sonnet, the audit on Opus, a book-check file for each work. Any batch the owner does not approve stays unread.

- R to A5, 2: Yang Jisheng, Mubei; Mao's Great Famine.
- R to A6, 2: Friends and Enemies; Jianguo yilai zhongyao wenxian.
- Placements I am least sure of, because I opened no file and went by title: "hathi-wmeat-1963-73" (141 pages; the name does not say; it is in U6 only because no other batch fits); `H. Rep. No. 88-914 (1963)` (by its number it is the House Judiciary Committee's report on the civil rights bill, and is in U4); `OSDSeries_Vol5` (by its name, a volume of the Office of the Secretary of Defense's history, in D1); the "Dated CIA/NSA memos and cables, 1960-68" (23 files, 388 pages, in U5; each memo may belong to another subject, and the first reader should say so); "Report of the Select Committee on Assassinations" and `sites-default-files-94465` (in U5); `mkl1a.pdf` and `mlk1b.pdf` (taken to be King files, in U4; if they are not King's they go back to U5); "Security Practices in the National Security Agency" (in U5); "I Shared the Dream" (taken to be Georgia Davis Powers's memoir, in U4).
- The oral histories are not split by subject (see "What moved and why").
- Two reading rates, 70 and 150 pages, are assumed, and I chose which works take which; the total fell from 5,202 to 4,872 readers by that choice alone. The pages of the remainders, now in their subject batches, are whole books and overstate what is left.

- R to U1, 10: Guns or Butter; The Passage of Power; LBJ's 1968; With Kennedy; We Band of Brothers; Kenneth P. O'Donnell & David F. Powers with ; Robert Kennedy and His Times; Kennedy; Journals, 1952–2000; Robert Kennedy.
- R to U2, 10: Six Crises; The Center Cannot Hold; The Agony of the G.O.P. 1964; The Making of the President 1968; On His Own Terms; RN; Before the Storm; 85 Days; The Making of the President 1964; The Making of the President 1960.
- R to U3, 2: Taxing America; The Fierce Urgency of Now.
- R to U4, 6: Bearing the Cross; Pillar of Fire; Judgment Days; An Idea Whose Time Has Come; At Canaan's Edge; Of Kennedys and Kings.
- R to U6, 1: Gold, Dollars, and Power.
- R to U8, 1: The Education of a Public Man.
- R to V1, 2: Van kien Dang toan tap; Lich su khang chien chong My.
- R to V2, 1: MACV Command History.
- R to V3, 5: Choosing War; Who Spoke Up? American Protest Against the W; The U.S. Government and the Vietnam War; Fulbright; Charles DeBenedetti with Charles Chatfield, .
- R to W3, 1: Lyndon Johnson and Europe.
- R to W4, 1: The Bay of Pigs.

The review of every batch for works that do not belong found the moves above. Two I am least sure of: Chafe's life of Lowenstein (U8; it runs through the Mississippi project, the dump-Johnson drive and Congress, and the first reader may move it back to U4), and Gaiduk (V1; it could stay with the Soviet works). The oral histories are by interviewee, not by subject; I did not split them, because their subjects are not in the file names. The alternative is to read each interview with the batch of its interviewee's subject; the default taken is to read them last, after the subject batches, by library and name.

## Each batch: what it is, and its order of reading

The order in every batch follows one rule. The record and the chronologies come before the books that rest on them (stage 1 and stage 2). Histories and studies come next, earliest publication first, so a later book can be read against an earlier one. Lives, memoirs and diaries come last, because they are the most partial. Series that run by year (the Posture statements, the Current Documents, the Senate Foreign Relations volumes, the CQ issues, the Newsweek issues) go in date order. A reader who finds that a book cited the day before is better read earlier should say so in the audit and the order be changed; the order is a default.

### A1. Soviet leadership and the Kremlin

- 11 works, 25 files, 12,379 pages, 123 readers. It would add 1960 to 1968; threads soviet-union, soviet-union-leadership, defense-soviet-forces, soviet-union-czechoslovakia. The Soviet side is the thinnest large thread: 1,164 calendar entries for the Soviet Union, 212 in 1960 and between 67 and 156 a year after, against 27,834 for China.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 51: Prezidium TsK KPSS 1954-64 (1 to 25); Идеологические комиссии ЦК КПСС 1958 - 1964_ (26 to 29); Brezhnev, Rabochie i dnevnikovye zapisi (30 to 46); CWIHP_Bulletin_16 (47 to 50); Russian archives (RGANI, AVPRF) (51).
- Stage 2, histories and studies, readers 52 to 123: The Sword and the Shield (52 to 62); The World Was Going Our Way (63 to 73); A Failed Empire (74 to 80); To Run the World (81 to 91); Записки из чемодана. Тайные дневник...дс...в (92 to 113); Р. Г. Пихоя  СОВЕТСКИЙ СОЮЗ. история власти  (114 to 123).

### A2. The Sino-Soviet split

- 6 works, 6 files, 2,143 pages, 33 readers. The Sino-Soviet works the calendar names behind To check but has not read, with the scholarship the owner put ahead of some nianpu (queue item 12, 4i.3). It would add 1960 to 1969; threads china-moscow-1960, china-moscow, china-polemic, china-border-war, china-foreign.
- Stage 1, histories and studies, readers 1 to 33: The Sino-Soviet Conflict, 1956–1961 (1 to 8); Yi Mao Zhuxi (Remembering Chairman Mao) (9 to 11); The Sino-Soviet Split (12 to 17); The Sino-Soviet Alliance (18 to 22); Economic Cold War_ America&_039_s Embargo ag (23 to 28); Li Danhui & Yafeng Xia, Mao and the Sino-Sov (29 to 33).

### A3. China: leaders, lives, memoirs and Mao

- 22 works, 31 files, 18,786 pages, 252 readers. Lives, chronologies, papers and memoirs of the Chinese leaders, with Mao's own words and the memoirs of the army chiefs of 1971; the owner's order for the memoirs is in queue item 12 (4g). It would add 1960 to 1971; threads china-leadership, china-mao, china-liu, china-zhou, china-center, china-luo-ruiqing, china-army.
- Stage 1, chronologies and reference, readers 1 to 15: Zhou Enlai nianpu (1949-76) (1 to 15).
- Stage 2, the record (documents, hearings, reports, periodicals), readers 16 to 24: Zhou Enlai Shuxin Xuanji (16 to 20); Zhou Enlai waijiao wenxuan (21 to 24).
- Stage 3, histories and studies, readers 25 to 86: Mao Zedong sixiang wansui (25); Wang Dongxing gongkai Mao Zedong si shenghuo (26 to 30); Mao The Real Story (Alexander V. Pantsov, St (31 to 41); San Ci Da Nan Bu Si Di Luo Ruiqing Da Jiang  (42 to 47); 晚年周恩来 (48 to 56); 评说晚年周恩来 (57 to 78); 金冲及, 中共中央文献研究室 - 刘少奇传（上、下册） (1998, 中央文献出版社) (79 to 86).
- Stage 4, lives, memoirs and diaries, readers 87 to 252: Huiyi yu Huainian (87 to 96); Liu Shaoqi Yi Sheng (A life of Liu Shaoqi) (97 to 107); Mao Zedong zhuan, 1949–1976 (108 to 140); Li Zuopeng huiyilu (141 to 155); Qiu Huizuo huiyilu (156 to 163); Chen Yun zhuan (4 vols.) (164 to 203); Peng Dehuai Zishu (Memoirs of a Chinese Mars (204 to 208); 岁月艰难_ 吴法宪回忆录 _Sui yue jian nan (209 to 216); 汪东兴回忆  毛泽东与林彪反革命集团的斗争  第2版 (217 to 219); 王力反思录 (220 to 236); 邱会作回忆录(下) (237 to 244); 黄峥 - 王光美访谈录 (中央文献出版社) (245 to 252).

### A4. China: the Cultural Revolution

- 21 works, 25 files, 10,314 pages, 157 readers. Works on the Cultural Revolution, the factions and the regions, with the Walder books moved here from A1. The calendar holds 3,300 China entries a year to 1966 and about 1,300 in 1968, so these add detail to a covered thread. It would add 1966 to 1969; threads china-red-guards, china-seizures, china-wuhan, china-may-sixteenth, china-class-ranks, china-ninth-congress.
- Stage 1, the record (documents, hearings, reports, periodicals), reader 1: 中共中央、国务院、中央军委、中央文革 关于广西文化大革命问题的重要文件汇编 (1).
- Stage 2, histories and studies, readers 2 to 143: Peking and the New Left (2 to 4); The Origins of the Cultural Revolution (5 to 22); Born Red (23 to 28); Haojie zhongde yi mu (29 to 32); Red Flower of China (33 to 36); Failure of Charisma (37 to 42); The Tragedy of Lin Biao (43 to 46); Mao's Last Revolution (47 to 57); A Chinese Rebel beyond the Great Wall_ The C (58 to 64); Andrew G. Walder - Agents of Disorder_ Insid (65 to 69); Andrew G. Walder - Civil War in Guangxi_ The (70 to 74); China Under Mao_ A Revolution Derailed{Andre (75 to 81); Collective killings in rural China during th (82 to 86); Dong Guoqiang & Andrew G. Walder - A Decade  (87 to 90); Fractured Rebellion_ The Beijing Red Guard M (91 to 96); Geming zaofan niandai (Li Xun) (97 to 120); Shanghai wenhua dageming shihua (draft) (121 to 128); Zai Li Shi De Dang An Li_ Wen Ge Shi Nian Fe (129 to 133); 文革受难者 (wang youqin（王友琴）) ( (134 to 143).
- Stage 3, lives, memoirs and diaries, readers 144 to 157: 内蒙文革风雷——一位造反派领袖的口述史 (144 to 157).

### A5. China: the Great Leap, famine, economy and the Third Front

- 12 works, 16 files, 10,367 pages, 139 readers. The Great Leap, the famine, the economy and the Third Front; queue item 12 (4i.3a) holds Yang Jisheng and Dikotter, which stay with their queue item and are named below only as a remainder. It would add 1960 to 1969; threads china-famine, china-economy, china-agriculture, china-retreat-1962, china-sixty-articles, china-third-front.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 13: 农业集体化重要文件汇编(1958-1981)下册 (1 to 13).
- Stage 2, histories and studies, readers 14 to 139: 'Da Yuejin' Qin Li Ji (A record of my own ex (14 to 27); Zhonghua renmin gongheguo jingji shi, 1949–1 (28 to 38); Mao's Great Famine (39 to 49); Beijing&_039_s Economic Statecraft during th (50 to 63); Mao&_039_s War against Nature_ Politics and  (64 to 68); Mao's Third Front_ The Militarization of Col (69 to 73); The River Dragon Has Come!_ Three Gorges Dam (74 to 77); Yang Jisheng, Mubei (78 to 112); 中国共产党与三线建设{陈夕}(2014, 中共党史出版社) (113 to 122); 大饥荒：1959-1961年的中国人口 (123 to 126); 林蕴晖 - 中华人民共和国史04.乌托邦运动—从大跃进到大饥荒（1958-1961) 0 (127 to 139).

### A6. China: party history, foreign relations and the army (reference, documents and the Foreign Ministry files)

- 22 works, 75 files, 16,663 pages, 183 readers. Party-history chronologies and reference books, the official histories of the army, the border war with India and the Sino-American talks, and the 45 Foreign Ministry files that the Wilson Center translates (queue item 14, Batch 17). Read by date. It would add 1960 to 1969; threads china-foreign, china-india-war, china-army, china-nuclear, china-afro-asian, china-center, china-mao-foreign.
- Stage 1, chronologies and reference, readers 1 to 16: Xin Zhongguo biannianshi (1949–1989) (1 to 5); Zhong Gong Dang Shi Zhong Da Shi Jian Shu Sh (6 to 8); Zhonggong Dangshi Dashi Nianbiao (A chronolo (9 to 12); 中国共产党历史大事记 (13 to 16).
- Stage 2, the record (documents, hearings, reports, periodicals), readers 17 to 60: Jianguo yilai zhongyao wenxian (17 to 58); PRC Foreign Ministry Archives (Wilson Center (59 to 60).
- Stage 3, histories and studies, readers 61 to 183: India's China War (61 to 68); Friends and Enemies (69 to 74); Yuan Yue Kang Mei Shilu (75 to 83); Xin Zhongguo Liu Ci Fan Qinlue Zhanzheng Shi (84 to 88); Zhong-Yin bianjing ziwei fanji zuozhan shi (89 to 93); Zhonghua renmin gongheguo fengyun shilu, 2 v (94 to 115); Negotiating with the Enemy (116 to 121); 1949-1989年的中国_曲折发展的岁月 (122 to 131); Spying for the People_ Mao’s Secret Agents,  (132 to 135); Zhongguo Gong Chan Dang Zhi Zheng Si Shi Nia (136 to 145); 中国人民解放军军史 第五卷 (《中国人民解放军军史》编写组) (146 to 151); 中国人民解放军军史 第六卷 (《中国人民解放军军史》编写组) (152 to 158); 中国共产党重大史实考证  (第一-四卷) (159 to 169); 中美会谈九年回顾 (170 to 172); 困守与反攻 (173 to 177); 第5卷. 歷史的變局_ 從挽救危機到反修防修, 1962-1965 - 錢庠理 (178 to 183).

### A8. Eastern Europe: Czechoslovakia, Romania, Albania, Hungary and the GDR (archives and the Prague Spring)

- 8 works, 49 files, 2,006 pages, 26 readers. Czechoslovak, Romanian, Albanian, Hungarian and East German files, and the works on the Prague Spring; queue item 14 holds the archives. It would add 1965 to 1968; threads soviet-union-czechoslovakia, comecon, china-foreign, vietnam-hanoi, europe-and-the-alliance.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 11: MOL XIX-J-1j SZU.IV-10.003348.1966 104.d (1); „Пражская весна“ и международный кризис 1968 (2 to 4); Albanian archives (AQSH) (5); Hungarian archives (MOL) (6); Romanian archives (ANR, AMAE) (7 to 10); Stasi (BStU, MfS Abt. X) (11).
- Stage 2, histories and studies, readers 12 to 26: The Prague Spring and Its Aftermath (12 to 16); Jaromir Navratíl (editor)_ Antonín Benčík (e (17 to 26).

### V1. Vietnam: Hanoi, Saigon and the Vietnamese-language works

- 17 works, 36 files, 11,545 pages, 117 readers. Hanoi's side, Saigon's side and the Vietnamese-language works, with Gaiduk on Soviet policy moved here. Queue item 13 (Batch 16) is about page cites to works already read, not these. It would add 1960 to 1969; threads vietnam-hanoi, vietnam-saigon, vietnam-elections, vietnam-tet, vietnam-struggle.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 51: 8058 – “Báo cáo của Phó Thủ tướng Lê Thanh N (1); Lich su khang chien chong My (2 to 24); Van kien Dang toan tap (25 to 51).
- Stage 2, histories and studies, readers 52 to 93: The Twenty-Five Year Century (52 to 58); Voices from the Second Republic of South Vie (59 to 61); The Vietnam War (62 to 66); Vietnam's Communist Revolution (67 to 73); The Republic of Vietnam 1955–1975 (74 to 77); Building a Republican Nation in Vietnam, 192 (78 to 81); HAI MƯƠI NĂM QUA Việc từng ngày (1945-1964)  (82 to 85); Ilya V. Gaiduk, Confronting Vietnam (86 to 90); Những ngày chưa quên (1954-1963) (91 to 93).
- Stage 3, lives, memoirs and diaries, readers 94 to 117: Twenty Years and Twenty Days (94 to 97); Our Endless War (98 to 102); Hoàng Linh Đỗ Mậu, Việt Nam (103 to 108); Hồi ký chính trị 1965-1975 đại tá Phạm Bá Ho (109 to 111); Nguyen Cao Ky with Marvin J. Wolf, Buddha's  (112 to 117).

### V2. Vietnam: American war histories, memoirs and intelligence

- 43 works, 53 files, 21,784 pages, 288 readers. American histories, memoirs and intelligence studies of the war on the ground and in Saigon. It would add 1960 to 1969; threads vietnam-commitments, vietnam-operations, vietnam-macv, vietnam-pacification, vietnam-tet, vietnam-khe-sanh.
- Stage 1, chronologies and reference, readers 1 to 8: Facts on File, South Vietnam (Sobel, Millet) (1 to 8).
- Stage 2, the record (documents, hearings, reports, periodicals), readers 9 to 41: MACV Command History (9 to 31); Porter, Vietnam (32 to 41).
- Stage 3, histories and studies, readers 42 to 275: South Vietnam (42 to 45); The Two Viet-Nams (46 to 51); The Last Confucian (52 to 56); Our Vietnam Nightmare (57 to 61); The Making of a Quagmire (62 to 66); The Lost Revolution (67 to 73); Viet Cong (74 to 82); Westmoreland (83 to 88); War Comes to Long An (89 to 93); Politics in War (94 to 98); The War Managers (99 to 102); America in Vietnam (103 to 110); The McNamara Strategy and the Vietnam War (111 to 113); Village at War (114 to 117); Vietnam (118 to 129); William Fulbright and the Vietnam War (130 to 133); War by Other Means (134 to 138); The Tet Offensive (139 to 143); Trapped by Success (144 to 148); The Johnson Years (149 to 156); Lodge in Vietnam (157 to 160); Mansfield and Vietnam (161 to 166); American Tragedy (167 to 175); Kennedy's Wars (176 to 184); Our Vietnam (185 to 196); Death of a Generation (197 to 205); Cold War Mandarin (206 to 209); Inventing Vietnam (210 to 213); Vietnam's Forgotten Army (214 to 219); Nine Days in May (220 to 226); Drawn Swords in a Distant Land (227 to 233); The History of South Vietnam (234 to 236); An eye for the dragon; Southeast Asia observ (237 to 243); Intervention (244 to 252); South Vietnam; a political history, 1954-197 (253 to 255); The Tuesday Cabinet; deliberation and decisi (256 to 259); Vietnam_ A Dragon Embattled (260 to 269); Village in Vietnam (270 to 275).
- Stage 4, lives, memoirs and diaries, readers 276 to 288: In the Midst of Wars (276 to 282); In the jaws of history (283 to 288).

### V3. Vietnam: Washington, Congress and the protest

- 5 works, 8 files, 4,653 pages, 68 readers. The war as American government and public business: the executive and Congress, Fulbright and Mansfield, the choice of 1964 to 1965, the protest. It would add 1961 to 1969; threads vietnam-commitments, vietnam-congress, vietnam-hearings, vietnam-protest.
- Stage 1, histories and studies, readers 1 to 57: Who Spoke Up? American Protest Against the W (1 to 7); The U.S. Government and the Vietnam War (8 to 40); Choosing War (41 to 49); Charles DeBenedetti with Charles Chatfield,  (50 to 57).
- Stage 2, lives, memoirs and diaries, readers 58 to 68: Fulbright (58 to 68).

### U1. The Kennedy and Johnson administrations (lives, memoirs, policy)

- 25 works, 32 files, 20,417 pages, 292 readers. Lives and memoirs of the Kennedy and Johnson circle, and the policy histories of their administrations, cited behind To check and never read. It would add 1960 to 1969; threads white-house, transition-and-staff, program, succession.
- Stage 1, histories and studies, readers 1 to 231: Kennedy (1 to 12); Lyndon B. Johnson (13 to 69); The Johnson Eclipse (70 to 74); Robert F. Kennedy (75 to 93); John F. Kennedy and the Second Reconstructio (94 to 99); Robert Kennedy and His Times (100 to 115); Promises Kept (116 to 121); Guns or Butter (122 to 131); Robert Kennedy (132 to 139); LBJ (140 to 165); Legacies of Camelot (166 to 169); The Passage of Power (170 to 181); The Patriarch (182 to 195); LBJ's 1968 (196 to 201); Dallek on Johnson (202 to 223); Kenneth P. O'Donnell & David F. Powers with  (224 to 231).
- Stage 2, lives, memoirs and diaries, readers 232 to 292: The Professional (232 to 236); With Kennedy (237 to 243); Ambassador's Journal (244 to 248); We Band of Brothers (249 to 254); Lyndon (255 to 264); Spanning the Century (265 to 274); Chief of Staff (275 to 280); Journals, 1952–2000 (281 to 287); P_ S_ (288 to 292).

### U2. Nixon, the Republicans and the presidential campaigns

- 53 works, 56 files, 27,141 pages, 410 readers. Nixon, the Republicans and the campaigns of 1960, 1964 and 1968; queue item 20 (Batch 18) holds most of it. It would add 1960, 1964 and 1968; threads elections-1960-nixon, elections-1964-goldwater, elections-1968-nixon, elections-1968-republican-nomination, republican-party, conservative-movement.
- Stage 1, histories and studies, readers 1 to 307: The Making of the President 1960 (1 to 6); The Agony of the G.O.P. 1964 (7 to 13); The Making of the President 1964 (14 to 20); Five States for Goldwater (21 to 23); George Romney (24 to 29); 85 Days (30 to 34); McCarthy for President (35 to 39); The Making of the President 1968 (40 to 46); The Selling of the President 1968 (47 to 50); Nixon Agonistes (51 to 60); Nobody Knows (61 to 66); The Resurrection of Richard Nixon (67 to 73); Catch the Falling Flag (74 to 78); White Knight (79 to 85); Rockefeller of New York (86 to 97); Making It Perfectly Clear (98 to 105); Nixon (106 to 127); 1968 in America (128 to 135); One of Us (136 to 146); Goldwater (147 to 155); The Right Moment (156 to 160); A Time for Choosing (161 to 165); Before the Storm (166 to 176); Suburban Warriors (177 to 182); Governor Reagan (183 to 191); A Glorious Disaster (192 to 196); 1960 (197 to 205); The Center Cannot Hold (206 to 209); The Making of a Catholic President (210 to 213); The Real Making of the President (214 to 217); Resilient America (218 to 223); The Greatest Comeback (224 to 230); The President and the Apprentice (231 to 242); Richard Nixon (243 to 254); American Maelstrom (255 to 260); Eisenhower the President (261 to 266); Goldwater (267 to 273); Irwin F. Gellman - Campaign of the Century_  (274 to 281); Luke A. Nichter - The Year That Broke Politi (282 to 287); The Men and the Moment (288 to 291); The road to Camelot (292 to 298); We Were the Campaign_ New Hampshire to Chica (299 to 302); Winning's a lot more fun (303 to 307).
- Stage 2, lives, memoirs and diaries, readers 308 to 410: Six Crises (308 to 321); With Nixon (322 to 328); RN (329 to 346); With No Apologies (347 to 351); The Imperial Rockefeller (352 to 356); Crazy Rhythm (357 to 363); In the Arena (364 to 370); Richard M. Nixon (371 to 387); On His Own Terms (388 to 401); Aitken, Jonathan_ Nixon, Richard Milhous - N (402 to 410).

### U3. Congress and its members

- 55 works, 56 files, 10,833 pages, 179 readers. The House and Senate through the lives of their members, the weekly record of Congress (36 CQ Weekly issues, moved here from the press batch), and the Mills and Johnson legislative histories. It would add 1960 to 1969; threads congress, rules, house, senate.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 36: 36 CQ Weekly issues, in date order, from 1962-05-04 to 1968-12-27 (1 to 36).
- Stage 2, histories and studies, readers 37 to 103: Dirksen (37 to 43); Dirksen of Illinois (44 to 48); Keeper of the Rules (49 to 59); Richard B. Russell, Jr., Senator from Georgi (60 to 68); Colleagues (69 to 73); Taxing America (74 to 79); Mike Mansfield, Majority Leader (80 to 84); Everett Dirksen and His Presidents (85 to 90); On Capitol Hill (91 to 96); The Fierce Urgency of Now (97 to 103).
- Stage 3, lives, memoirs and diaries, readers 104 to 179: In the Fullness of Time (104 to 113); Preserving the Constitution (114 to 120); Fighting the Odds (121 to 132); Henry M. Jackson (133 to 141); Senator Mansfield (142 to 151); Strom (152 to 158); Javits (159 to 167); Sam Rayburn a biography (Steinberg, Alfred,  (168 to 174); Wheeling and dealing confessions of a Capito (175 to 179).

### U4. Civil rights, King and race (books, FBI files, reports and the civil rights bill)

- 49 works, 70 files, 27,797 pages, 394 readers. Civil rights, King, the South and race, with the civil rights bill's own record (the House report, the legislative history of Titles VII and XI), the FBI Liuzzo files, the two coded King files and the books on the FBI and King moved here. Many of the books are cited dozens of times behind To check; queue item 18 holds the King and FBI group. It would add 1960 to 1969; threads king, civil-rights-bill, voting-rights-selma, freedom-rides, sit-ins, mississippi, alabama-birmingham, civil-disorders.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 28: H. Rep. No. 88-914 (1963) (1 to 3); Justice Department task force report January (4 to 6); FBI Liuzzo files (7 to 21); Legislative_History_of_Titles_VII_and_XI (22 to 26); mkl1a (27); mlk1b (28).
- Stage 2, histories and studies, readers 29 to 347: A Bill Becomes a Law (29 to 31); Wallace (32 to 35); Black Ballots (36 to 43); Southern Governors and Civil Rights (44 to 50); The Transformation of Southern Politics (51 to 58); Protest at Selma (59 to 64); Of Kennedys and Kings (65 to 72); The FBI and Martin Luther King, Jr. (73 to 88); At the River I Stand (89 to 94); Bearing the Cross (95 to 106); To Redeem the Soul of America (107 to 114); We Are Not Afraid (115 to 122); "Racial Matters" (123 to 129); And the Walls Came Tumbling Down (130 to 142); The Civil Rights Era (143 to 151); To End All Segregation (152 to 157); Calculating Visions (158 to 167); George Wallace (168 to 177); I've Got the Light of Freedom (178 to 194); Race and Democracy (195 to 204); Pillar of Fire (205 to 216); The Last Crusade (217 to 220); Carry Me Home (221 to 231); Kennedy, Johnson, and the Quest for Justice (232 to 237); Judgment Days (238 to 245); The Informant (246 to 252); At Canaan's Edge (253 to 268); The Bystander (269 to 277); Delaying the Dream (278 to 283); Some of It Was Fun (284 to 288); Sweet Land of Liberty (289 to 300); The Fifth Freedom (301 to 307); Racial Propositions (308 to 313); Behind the Dream (314 to 317); James J. Kilpatrick (318 to 322); The March on Washington (323 to 327); An Idea Whose Time Has Come (328 to 334); I Shared the Dream (335 to 340); The Judas factor (341 to 347).
- Stage 3, lives, memoirs and diaries, readers 348 to 394: My Life with Martin Luther King, Jr. (348 to 371); The Death and Life of Malcolm X (372 to 379); Lay Bare the Heart (380 to 385); Malcolm X (386 to 394).

### U5. The FBI, the CIA, the NSA and surveillance

- 24 works, 52 files, 16,478 pages, 187 readers. The FBI as an institution, the CIA, the NSA and the Army at home, the Hoover lives, the Church and House assassination reports and the Senate data-bank hearings; queue item 18 holds most of it. It would add 1960 to 1974; threads intelligence, antisubversion, assassination.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 58: Dated CIA/NSA memos and cables, 1960-68 (1 to 3); Senate hearings on federal data banks (1971, (4 to 42); NARA RG 59 (INR) reports (43); NSA-60th-Anniversary (44); Report_of_the_Select_Committee_on_Assass (45 to 49); Security_Practices_in_the_National_Secur (50); The COINTELPRO papers (51 to 54); sites-default-files-94465 (55 to 57); “Betrayers of the Trust” (part), National Se (58).
- Stage 2, histories and studies, readers 59 to 112: The Age of Surveillance (59 to 67); Army Surveillance in America, 1775–1980 (68 to 72); Enemies (73 to 81); MH_CHAOS (82 to 95); Secrets (96 to 99); The secret sentry (100 to 106); There’s Something Happening Here (107 to 112).
- Stage 3, lives, memoirs and diaries, readers 113 to 187: Secrecy and Power (113 to 122); The Boss (123 to 130); J. Edgar Hoover (131 to 143); Hoover's FBI (144 to 150); G-Man (151 to 163); From the secret files of J_ Edgar Hoover (164 to 169); Spying on Americans (170 to 182); William C. Sullivan with Bill Brown, The Bur (183 to 187).

### U6. Economy, finance and trade

- 15 works, 15 files, 4,619 pages, 73 readers. Money, the budget, the Federal Reserve and trade. It would add 1960 to 1969; threads economy, economy-gold, economy-franc, economy-surcharge, trade.
- Stage 1, the record (documents, hearings, reports, periodicals), reader 1: hathi-wmeat-1963-73 (1).
- Stage 2, histories and studies, readers 2 to 73: New Dimensions of Political Economy (2 to 5); The Dollar and World Liquidity (6 to 11); The Political Economy of Prosperity (12 to 14); The Arena of International Finance (15 to 18); The International Monetary System, 1945–1976 (19 to 25); Presidential Economics (26 to 33); Eisenhower Versus "The Spenders" (34 to 37); American Trade and Power in the 1960s (38 to 43); Deficit Government (44 to 47); Globalizing Capital (48 to 52); Butter and Guns (53 to 57); Chairman of the Fed (58 to 63); Gold, Dollars, and Power (64 to 68); More_ The Politics of Economic Growth in Pos (69 to 73).

### U8. The parties, liberalism and labor (Democrats, Humphrey)

- 16 works, 16 files, 6,573 pages, 103 readers. The Democratic and Republican parties as organisations, liberalism, the unions, and the lives of Humphrey. It would add 1960 to 1969; threads democratic-party, republican-party, labor, elections-1968-humphrey.
- Stage 1, histories and studies, readers 1 to 74: Civil Rights and the Crisis of Liberalism (1 to 5); The Unraveling of America (6 to 14); Politics and Vision (15 to 19); The Decline and Fall of the Liberal Republic (20 to 24); The President and the Parties (25 to 31); The Losing Parties (32 to 36); The UAW and the Heyday of American Liberalis (37 to 42); JFK, LBJ, and the Democratic Party (43 to 49); Law and Order (50 to 54); Presidential Party Building (55 to 60); Hubert (61 to 65); Never stop running (66 to 74).
- Stage 2, lives, memoirs and diaries, readers 75 to 103: Almost to the Presidency (75 to 83); The Education of a Public Man (84 to 91); Hubert_ An Unauthorized Biography of the Vic (92 to 97); Humphrey (98 to 103).

### U9. Cities and States

- 6 works, 6 files, 2,788 pages, 42 readers. The cities (New York, Maryland, California) and the governors. It would add 1960 to 1969; threads mayors, states-and-cities, governors, state-and-city-finance.
- Stage 1, histories and studies, readers 1 to 42: Governing New York City (1 to 6); A Nation of Cities (7 to 14); Goodbye to Good-Time Charlie (15 to 18); Maryland & America, 1940 to 1980 (19 to 24); The Ungovernable City (25 to 34); California Rising (35 to 42).

### E1. Apportionment, districts and the vote

- 6 works, 25 files, 4,838 pages, 45 readers. Apportionment and reapportionment, the districts as they stood, and the election returns; moved out of civil rights by ruling 63. It would add 1960 to 1968; threads reapportionment, elections-1962, elections-1964, elections-1968, congress.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 24: hathi-nomination-election-1968 (1 to 2); America Votes (Scammon) (3 to 18); Congressional District Data (Census) (19 to 24).
- Stage 2, histories and studies, readers 25 to 45: Democratic Representation (25 to 34); The End of Inequality (35 to 39); On Democracy's Doorstep (40 to 45).

### J1. The Supreme Court and the Constitution

- 7 works, 10 files, 7,277 pages, 68 readers. The Supreme Court and the Constitution: the prayer decisions, presidential inability and the 25th Amendment, the four-year term, the Fortas nomination, the Warren Court. It would add 1962 to 1968; threads court, court-fortas, constitution.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 35: hathi-hrg-prayer-1962 (1 to 2); hathi-hrg-inability-1964 (3 to 4); hathi-hrg-prayer-1964.2 (5 to 24); hathi-hrg-four-year-term-1966 (25); hathi-hrg-fortas-1968.2 (26 to 35).
- Stage 2, histories and studies, readers 36 to 68: Explicit and Authentic Acts (36 to 53); The Warren Court and American Politics (54 to 68).

### H1. Poverty, welfare, health and labor

- 7 works, 9 files, 5,483 pages, 51 readers. Poverty, welfare, health and farm and migrant labor: the hearings and the books on the programs. It would add 1960 to 1969; threads poverty, program, jobs-and-wages, health.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 28: hathi-hrg-migratory-labor-1965-1966 (1 to 6); hathi-hrg-migratory-labor-1967 (7 to 20); hathi-hrg-war-on-poverty-1967.2-jackson (21 to 28).
- Stage 2, histories and studies, readers 29 to 44: With Dignity (29 to 32); From Opportunity to Entitlement (33 to 37); Launching the War on Poverty (38 to 44).
- Stage 3, lives, memoirs and diaries, readers 45 to 51: Mr. Social Security (45 to 51).

### D1. Defense, nuclear strategy, intelligence estimates and space

- 17 works, 17 files, 8,938 pages, 87 readers. Defense posture, nuclear strategy, the estimates of Soviet strength and space. The Posture statements are the Secretary of Defense's yearly statements to Congress. It would add 1962 to 1968; threads defense, defense-soviet-forces, space, missile-gap.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 49: hathi-posture-fy63-1962 (1 to 5); hathi-posture-fy64-1963 (6 to 10); hathi-posture-fy66-1965 (11 to 15); hathi-posture-fy67-1966 (16 to 25); hathi-posture-statement-fy68-1967 (26 to 28); hathi-posture-fy69-1968 (29 to 39); hathi-posture-statement-fy69-1968 (40 to 41); OSDSeries_Vol5 (42 to 46); cmh-maneuver-and-firepower (47); dod-stockpile-fact-sheet-2010 (48); nhhc-ship-force-levels (49).
- Stage 2, histories and studies, readers 50 to 87: The Soviet Estimate (50 to 55); The Wizards of Armageddon (56 to 62); ...the Heavens and the Earth (63 to 71); Eisenhower and the Missile Gap (72 to 75); Intentions and Capabilities (76 to 83); John F. Kennedy and the Missile Gap (84 to 87).

### F1. United States foreign policy (State Department and Senate Foreign Relations documents)

- 11 works, 11 files, 11,438 pages, 83 readers. The State Department's yearly documents, the Department of State Bulletin of 1968 and the Senate Foreign Relations Committee's executive-session volumes of 1963 to 1966. These carry every foreign subject; each reader dates what the page reports. It would add 1962 to 1968; threads europe-and-the-alliance, vietnam-diplomacy, vietnam-congress, foreign-policy.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 79: hathi-current-documents-1962 (1 to 12); hathi-current-documents-1963 (13 to 22); hathi-current-documents-1964 (23 to 32); hathi-current-documents-1966 (33 to 41); hathi-current-documents-1967 (42 to 51); hathi-dsb-v59 (52 to 57); hathi-sfrc-exec-v15 (58 to 64); hathi-sfrc-exec-v16 (65 to 67); hathi-sfrc-exec-v17 (68 to 72); hathi-sfrc-exec-v18 (73 to 79).
- Stage 2, histories and studies, readers 80 to 83: Dean Rusk (80 to 83).

### W1. Britain

- 11 works, 13 files, 9,948 pages, 105 readers. Britain has no thread of its own; the alliance thread has a Britain strand. The Nov. 25 inventory proposed a Britain run and noted the owner has not said whether Britain is a covered nation (default taken: yes). It would add 1960 to 1970; threads europe-and-the-alliance-britain, europe-and-the-alliance, vietnam-diplomacy, economy-gold.
- Stage 1, histories and studies, readers 1 to 55: The Labour Government, 1964–1970 (1 to 13); Harold Wilson (14 to 26); Never Had It So Good (27 to 40); White Heat (41 to 55).
- Stage 2, lives, memoirs and diaries, readers 56 to 105: The Cecil King Diary 1965–1970 (56 to 58); The Diaries of a Cabinet Minister, vol. 3 (59 to 76); The Castle Diaries 1964–70 (77 to 82); Out of the Wilderness (83 to 87); Office Without Power (88 to 91); Wilson (92 to 101); Years of Hope (102 to 105).

### W2. France

- 6 works, 22 files, 15,368 pages, 132 readers. de Gaulle's letters and notes, Peyrefitte, Viansson-Ponte and the Documents diplomatiques francais; queue item 21 holds the French pilot. It would add 1960 to 1969; threads europe-and-the-alliance-france, european-community, economy-franc.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 82: Discours et messages, vol. 4 (1 to 4); DDF (5 to 59); de Gaulle, Lettres, notes et carnets (60 to 82).
- Stage 2, histories and studies, readers 83 to 124: C'était de Gaulle (83 to 104); Viansson-Ponte, Histoire de la Republique ga (105 to 124).
- Stage 3, lives, memoirs and diaries, readers 125 to 132: Mémoires d'espoir (125 to 132).

### W3. Berlin, Germany and Western Europe

- 7 works, 7 files, 3,140 pages, 47 readers. Berlin, Germany and Western Europe, with the two Berlin books moved here from A1 and Schwartz on Johnson and Europe moved here from the remainders. The German pilot in queue item 21 is not yet chosen. It would add 1960 to 1969; threads europe-and-the-alliance-federal-republic, berlin-and-vienna, european-community.
- Stage 1, chronologies and reference, readers 1 to 3: Germany and Eastern Europe since 1945 (1 to 3).
- Stage 2, histories and studies, readers 4 to 47: Adenauer and Kennedy (4 to 6); A Constructed Peace (7 to 13); Driving the Soviets up the Wall (14 to 19); Lyndon Johnson and Europe (20 to 25); Berlin 1961 (26 to 35); Adenauer Bd_ 2_ Der Staatsmann (36 to 47).

### W4. Cuba, the missile crisis and Latin America

- 12 works, 12 files, 5,447 pages, 78 readers. Cuba, the missile crisis and Latin America, with the Mikoyan, Plokhy and Hershberg books moved here from A1 and Jones on the Bay of Pigs from the remainders. The missile crisis and Bay of Pigs have heavy coverage, the rest less. It would add 1960 to 1969; threads cuba, cuba-bay-of-pigs, missile-crisis, latin-america, latin-america-dominican-republic.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 3: CIA Documents on the Cuban Missle Crisis of  (1 to 3).
- Stage 2, histories and studies, readers 4 to 78: Eisenhower and Latin America (4 to 7); The Most Dangerous Area in the World (8 to 11); The Castro Obsession (12 to 16); The Bay of Pigs (17 to 20); That Infernal Little Cuban Republic (21 to 31); The Soviet Cuban Missile Crisis (32 to 40); Back Channel to Cuba (41 to 48); New Russian Evidence on Soviet-Cuban Relatio (49); Nuclear Folly (50 to 65); Cuba on the brink (66 to 73); G. Pope Atkins - The Dominican Republic and  (74 to 78).

### W5. Africa

- 10 works, 10 files, 4,301 pages, 60 readers. Africa and the Congo, 253 and 201 calendar entries. It would add 1960 to 1969; threads africa, africa-algeria-morocco, congo, congo-lumumba.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 7: сост._ Антошин А. В. и др. (1 to 7).
- Stage 2, histories and studies, readers 8 to 60: Crisis in the Congo (8 to 11); American Foreign Policy in the Congo, 1960–1 (12 to 18); The Congo Cables (19 to 26); JFK (27 to 32); Cold War and Black Liberation (33 to 37); A Diplomatic Revolution (38 to 44); Betting on the Africans (45 to 50); Death in the Congo (51 to 55); Africa independent;_ A survey of political d (56 to 60).

### W6. The Middle East

- 8 works, 11 files, 6,769 pages, 90 readers. The Middle East, 374 calendar entries, 98 of them in 1967; queue item 17 holds Pollack. It would add 1960 to 1969; threads middle-east, middle-east-six-day-war, middle-east-yemen, middle-east-iran-oil.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 10: Naumkin, Blizhnevostochnyi konflikt (documen (1 to 10).
- Stage 2, histories and studies, readers 11 to 90: The Turkish Revolution, 1960–1961 (11 to 13); The Other Arab-Israeli Conflict (14 to 29); The Eagle and the Lion (30 to 37); Peace Process (38 to 45); Arabs at War (46 to 78); Support Any Friend (79 to 84); Nasser's Gamble (85 to 90).

### W7. Korea, Japan and South Asia

- 5 works, 22 files, 6,891 pages, 64 readers. Korea, Japan and India, with Szalontai on Kim Il Sung moved here from A1; the Japanese files are the ones whose names give no title (see the last section). A few hundred calendar entries between them. It would add 1960 to 1969; threads japan, japan-and-korea, korea, south-asia, india-and-china-kashmir.
- Stage 1, the record (documents, hearings, reports, periodicals), readers 1 to 33: Japan (1 to 33).
- Stage 2, histories and studies, readers 34 to 64: Protest in Tokyo (34 to 40); Kim Il Sung in the Khrushchev Era (41 to 46); Nation Building in South Korea (47 to 51); The Park Chung Hee Era (52 to 64).

### P1. The press: books on it, the weeklies and the newspapers

- 12 works, 50 files, 4,180 pages, 51 readers. The press: three books on it, Keesing's for 1963 to 1964, five Newsweek issues of January 1968, one New Yorker, one New York Times day. The 36 CQ Weekly issues that stood here have moved to U3. It would add 1960, 1963 to 1964 and 1968; threads press-and-broadcasting, elections-1968.
- Stage 1, chronologies and reference, readers 1 to 10: KEESING'S Contemporary archives_ Vol_ 14_ 19 (1 to 10).
- Stage 2, the record (documents, hearings, reports, periodicals), readers 11 to 16: NYT 1960-07-07 (day folder, 39 pages as imag (11); Newsweek 1968-01-01 (12); Newsweek 1968-01-08 (13); Newsweek 1968-01-15 (14); Newsweek 1968-01-22 (15); Newsweek 1968-01-29 (16).
- Stage 3, histories and studies, readers 17 to 45: The Powers That Be (17 to 28); The Place to Be (29 to 35); Heather Hendershot - When the News Broke_ Ch (36 to 41); The New Yorker  1960-11-05_ Vol 36 Iss 38 (42 to 45).
- Stage 4, lives, memoirs and diaries, readers 46 to 51: Confessions of a muckraker (46 to 51).

### O1. Oral histories (JFK and RFK libraries)

- 840 transcripts, 29,780 pages, 845 readers. Oral histories (JFK and RFK libraries) would add 1960 to 1968; all threads with a Kennedy or Johnson side. The hand-off keeps them on file, not queued.
- Stage 1, the JFK Library, 577 transcripts in the order of the interviewee's name, then the interview number; stage 2, the RFK Library, 253 in the same order. A reader takes about 150 pages, a few transcripts of one interviewee together. The first reader of each library should say whether the transcripts are better read by interviewee's subject, and the order be changed.

## What the queue holds and what it does not

Of the 436 unread works (not read, or cited only from other works), 77 are reached by a queue item (items 9 to 22, or the older queue's lists), 37 are only in a run the Nov. 25 inventory proposed and the hand-off holds for this plan (item 9), and 322 are reached by neither.

- The queue items that reach unread works, with how many: 12 (China order, 4g memoirs) 8; 12 (China order, 4h wansui) 1; 12 (China order, 4i.3 scholarship) 3; 14 (Batch 17, Wilson Center documents) 6; 17 (Pollack) 1; 18 (King and the FBI) 10; 18 (surveillance at home) 13; 20 (Batch 18) 24; 21 (French pilot, then German) 5; C2 (older queue: foreign leaderships, UK) 6.
- The queue items that name no Drive work: 10 (the 1960 conventions), 11 (the rest of the Nov. 21 and 22 queue), 15 (the re-read pass), 16 (the notes pass re-run, which goes back over works already read), 19 (the time-of-day pass) and 22 (indicators).
- The works no queue item reaches, by batch: A1 4; A2 3; A3 12; A4 21; A5 10; A6 20; A8 4; V1 14; V2 42; V3 3; U1 25; U2 29; U3 55; U4 39; U5 10; U6 15; U8 9; U9 4; E1 6; J1 7; H1 7; D1 16; F1 11; W3 3; W4 7; W5 8; W6 6; W7 3; P1 10.
- The 25 of them that the calendar most often names behind To check (the number is the count of entries): The Warren Court and American Politics 67; Failure of Charisma: The Cultural Revolution 50; Democratic Representation: Reapportionment i 42; Huiyi yu Huainian 38; Haojie zhongde yi mu: Wuhan qi er ling shiji 36; The Civil Rights Era: Origins and Developmen 36; India's China War 34; To Redeem the Soul of America: The Southern  32; Protest at Selma: Martin Luther King, Jr., a 28; Black Ballots: Voting Rights in the South, 1 27; Law and Order: Street Crime, Civil Unrest, a 22; American Tragedy: Kennedy, Johnson, and the  20; Maryland & America, 1940 to 1980 20; Zhong-Yin bianjing ziwei fanji zuozhan shi 19; Vietnam: A History 18; Lyndon: An Oral Biography 18; Governor Reagan: His Rise to Power 18; American Trade and Power in the 1960s 18; George Wallace: American Populist 17; At the River I Stand: Memphis, the 1968 Stri 17; Dirksen: Portrait of a Public Man 17; I've Got the Light of Freedom: The Organizin 17; ...the Heavens and the Earth: A Political Hi 17; The International Monetary System, 1945–1976 16; We Are Not Afraid: The Story of Goodman, Sch 15.

## A suggested order of batches

The calendar's weight is lopsided. China has 27,834 of its 59,038 entries and Vietnam 7,720, the 1968 elections 1,512, the Soviet Union 1,164. Europe and the alliance has 373, the Middle East 374, Africa 253, Korea and Japan about 300, South Asia 157. The order below puts what the owner already queued first, then the subjects the calendar covers least, then the large subjects the calendar covers already. Within a step the batches may run at the same time if their entries do not overlap; two batches that touch the same entries (the civil rights bill, the Court, the 1968 campaign) go one after the other. Within every batch, readers go one after another.

1. Queue items 12, 13, 14, 17, 18, 20 and 21, which name Drive works, in the owner's order. This plan changes none of them. Where a queue item names a work now in a recut batch (item 18: the King and FBI group, now in U4 and U5; item 14: the Foreign Ministry files, now in A6 and the archives in A8), the queue item keeps it and the batch drops it when the item has read it.
2. A1, the Soviet leadership, then A2, the Sino-Soviet split: the thinnest large thread, and the works the Nov. 25 inventory already described (its Runs A and B). W3 and W4 (Berlin and Germany; Cuba and the missile crisis) may run beside them, since their entries are other threads.
3. W1, W2, W5, W6 and W7 (Britain, France, Africa, the Middle East, Korea and Japan): small batches, each adding entries to threads with a few hundred. Britain waits on the owner's word on whether it is a covered nation; the default taken is yes. These five touch different threads and may run side by side.
4. U4, then E1, J1 and U3: the American books the calendar names behind To check many times and has never read (The Warren Court and American Politics 67; Democratic Representation 42; The Civil Rights Era 36; To Redeem the Soul of America 32; Protest at Selma 28; Black Ballots 27). U4 first because it carries the record of the civil rights bill; E1 and J1 then read the apportionment and Court material against it; U3 last of the four because the CQ issues cover all three. These four overlap, so they run one after the other.
5. U1, with H1, D1 and F1 beside it: the Kennedy and Johnson administrations, poverty and health, defense and space, foreign policy documents.
6. U2 and U5 as queue items 20 and 18 set them; U8 and U9 beside them; U6 after.
7. A3, A4, A5, A6 and A8: China and the archives. The queue's item 12 and item 14 come first; these are the rest. They are the largest batches by pages, and China is already the calendar's biggest thread. A6 goes first (chronologies, then the Foreign Ministry files), A3 next, then A4 and A5 together, then A8.
8. V1, V2 and V3: Vietnam, already the second-largest thread, after the above. V3 (Congress and the protest) may run beside V1.
9. P1, then O1: the press and the weeklies, and the oral histories, which the hand-off keeps on file.

Each batch would be briefed as the owner's rules direct: R0 first, the first pass on Sonnet, the audit on Opus, a book-check file for each work. Any batch the owner does not approve stays unread.

## What I could not identify or settle

- Placements I am least sure of, because I opened no file and went by title: "hathi-wmeat-1963-73" (141 pages; the name does not say; it is in U6 only because no other batch fits); `H. Rep. No. 88-914 (1963)` (by its number it is the House Judiciary Committee's report on the civil rights bill, and is in U4); `OSDSeries_Vol5` (by its name, a volume of the Office of the Secretary of Defense's history, in D1); the "Dated CIA/NSA memos and cables, 1960-68" (23 files, 388 pages, in U5; each memo may belong to another subject, and the first reader should say so); "Report of the Select Committee on Assassinations" and `sites-default-files-94465` (in U5); `mkl1a.pdf` and `mlk1b.pdf` (taken to be King files, in U4; if they are not King's they go back to U5); "Security Practices in the National Security Agency" (in U5); "I Shared the Dream" (taken to be Georgia Davis Powers's memoir, in U4).
- The oral histories are not split by subject (see "What moved and why").
- Two reading rates, 70 and 150 pages, are assumed, and I chose which works take which; the total fell from 5,202 to 4,872 readers by that choice alone. The pages of the remainders, now in their subject batches, are whole books and overstate what is left.

- 157 works have no card. I made none. They are the rows with an empty `card` column. A few are archive sets (the Wilson Center files, the Romanian files) that one card would not describe.
- 126 of the 468 card matches are weak: the author's name and part of the title matched. They are marked `weak` in the TSV. I rejected a few false ones by hand. A brief should check the card before it names it.
- Files whose names give no title: `mkl1a.pdf` and `mlk1b.pdf` (probably FBI files on King, by the pattern of `liuzzo2.pdf`); `k_list.pdf`, `t_list.pdf` and the `k_`, `t_` and `hokoku_` files, which the Nov. 25 inventory took for the Japanese secret-agreements report and its annexes; `dod-stockpile-fact-sheet-2010.pdf`, `nhhc-ship-force-levels.pdf`, `cmh-maneuver-and-firepower.pdf` and `OSDSeries_Vol5.pdf`, which name their issuing offices only; `sites-default-files-94465.pdf`, which is probably S. Rep. No. 94-465 (the Church Committee's assassinations report). I opened none of them.
- The Batch 4 brief of Nov. 5 named 70 of the books on the Drive; 47 of them have neither a book-check file nor a calendar cite, and the hand-off does not say what became of them. They are in the batches above. The owner may know whether they were read.
- 13 files are copies of another file in the same set (same size); they are one row each with the copies listed. Some works are on the Drive in two formats (a PDF and an EPUB).
- A work can be on the Drive but rated unread because its card and its book-check carry different names; I matched book-checks by Drive id and by card name. A missed match would show a read work as unread.
- The reader-run figures rest on two assumed rates, 70 and 150 pages. They are not measured. The earlier inventory used about 6,100 pages for the 14 Soviet works at three agents, which is about 2,000 pages an agent.
- Files over 10 MB cannot be fetched through the Drive connector; the readers' route is `notes/guide/reading-a-copy.md`. The counts are from the files' own page trees; the limit above stopped me before the last 88 big PDFs were counted, and those are estimated from size.



