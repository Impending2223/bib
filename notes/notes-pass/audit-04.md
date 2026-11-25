Audit of batch 04 of the notes pass (patch `inbox/2026-11-25-notes-pass-04.yaml`), Nov. 25, 2026, by Claude (Opus). The reader had added words to 59 entries from the notes' parentheticals without opening the cited pages. I read every cited page against its words, rewrote the patch in place from those pages, and ran `./bib patch-check` to 0 errors. Two warnings are left on purpose: they mark the new entry of Sept. 1, 1961 as a possible duplicate of the Soviet test entry of the same day. It is a different act, so at the merge it should be kept (`./bib resolve cal.1961-09-01.testing-2 --take keep`). Nothing was merged or committed.

## How the pages were read

Every copy came from the owner's Drive by curl into my own scratch directory and was deleted when done. The Chinese scans have no text layer, so I read their pages as images at 75 to 90 dpi and checked each folio on the image. These were: Peng Zhen nianpu IV (printed = PDF − 4); Deng Xiaoping nianpu III (printed = PDF + 1328); Chen Yun nianpu III (− 5); Zhu De nianpu III (the scan's pages 7–1356 are blank, and III begins at PDF 1357; printed = PDF − 6); Liu Shaoqi nianpu II (1996; − 5); Yang Shangkun riji II (− 5); Wu Lengxi (− 8); Zhongyao wenxian XIV (− 15); Mao wengao XVI (− 25); Waijiao dashiji II (− 9); Peng Dehuai nianpu (− 7); Chen Yi nianpu (− 13); Zhou Enlai nianpu II (the vol. II file; 398 = PDF 401); and Mubei (the book-check's offsets, every folio seen). I read *Tiandi fanfu* I by its text layer (66 = PDF 70) and *Mao Zedong zhuan* by its epub text, by chapter. The English books I read by their text layers, with the folio found on each page: O'Donnell, MacFarquhar III, Sorensen *Counselor* (+ 22 here, not + 21), Schlesinger *Journals*, Fursenko and Naftali, Thomas, Smith, Dobrynin, Westmoreland, Sorensen *Kennedy*, *RFK in His Own Words*, Clifford, Moyar, *McNamara in Retrospect*, Dikötter (both books), Jian, Chang, Ang, Jones, Navasky, Ball, Futrell (govinfo), Humphrey's memoir, Westad's *Brothers in Arms* (epub, pages marked), and the Presidium volumes I and III. jcs.mil refused the download, so I read Poole from the archive.org copy the book-check names (DTIC_ADA551509). There the text layer gives 0357, but the page image shows "0337".

## What the pages showed: the ops changed

Many ops credited one source with what other sources in the note say. I split each such op so that every part is cited to the page that bears it out. The changes, entry by entry:

- `cal.1960-12-07.china-leadership`: Zhu De's attendance moved from Peng Zhen IV 83 to Zhu De III 1789. Added the afternoon time field (Deng III 1603; Peng IV 83).
- `cal.1960-12-16.robert-kennedy`: Clifford's errand to Joseph Kennedy struck. It is another act, Nov. 1960, already its own entry (`cal.1960-11.robert-kennedy`). "Joseph Kennedy is for it" struck: RFK 74 gives the father's view, not an act of the day. Kept O'Donnell 273, with "that morning" and Goldberg present. Set the morning time field and place `washington` in place of the range by kind.
- `cal.1960-12-19.china-leadership-3`: struck the reader's Check on "shipping" against "air transport". Both chronologies print 航运合作协定 (Waijiao 177; Chen Yi 849), so the difference was in the old note's English only. "Air-transport agreement" corrected to "shipping agreement", and Chen Yi 848–849 cited for the same words.
- `cal.1960-12-24.china-leadership`: the billion yuan and the price rises are the conference's decisions, not Chen Yun's speech (Chen Yun III 61); the op now says so. Added the grain-price group under Chen Yun. Zhu De's attendance moved to Zhu De III 1790.
- `cal.1960-12-26.china-leadership`: Mao has not chaired the Politburo since 1953–54. Added "more than an hour" (Westad 365–369).
- `cal.1961-01-09.transition-and-staff`: Kennedy left "shortly after 5", not before (Schlesinger *Journals* 102). The pin for Sorensen's *Counselor* is 219.
- `cal.1961-01-09.china-leadership`: the Mao zhuan words are in the body of ch. 67, so the pin is "ch. 67", not "n.7". Peng Zhen pinned at IV 90–91.
- `cal.1961-03-15.china-leadership-2`: Zhou does not speak on the 22nd. He speaks on the 19th and 20th and revises the letter on the 22nd (Zhou II 398–99). Peng Zhen's attendance moved to Peng IV 112. The Three South and Three North origin is in Zhu De's note (III 1800 n.1), so that part is cited to the note. Added a Check: Zhou's chronology has Zhou presiding on the 20th, Liu's has Liu.
- `cal.1961-03-23.china-leadership-3`: struck the op with the trips of Liu, Zhu, Deng and Peng Zhen (Peng Dehuai nianpu 763). They are later acts, not the letter's.
- `cal.1961-04-19.cuba`: Lemnitzer's "go guerrilla" and Burke's hour of air cover moved from Poole to Thomas 121. Added a Check: Poole (116) places "go guerrilla" on the morning of the 19th.
- `cal.1961-04-22.china-leadership-2`: split three ways. Chen Yi 868 gives those present and the times. Ang 190 gives "cordial and friendly". Waijiao 192–93 gives the common views.
- `cal.1961-04-26.china-leadership-2`: Deng's sending moved to Mao zhuan ch. 68. Mubei II 1173 does not name Deng. Hu's figures pinned at Wenxian XIV 301–302, with the county's 30,000 added.
- `cal.1961-04-28.opinion`: dropped the 82 percent from the words, since the entry's variant already holds it. Added "late afternoon"; the pin is 120–21.
- `cal.1961-05-25.space`: added the Marines' strength before the rise, 178,000 (Poole 65).
- `cal.1961-06-03.berlin-and-vienna`: the three inspections were on June 4 in the session, not in the garden walk (Fursenko 362). "Cold winter" pinned at Presidium III 214.
- `cal.1961-06-12.china-leadership`: "eleven years ... another eleven" is Yang Shangkun's diary (II 41), not Mao zhuan. Set the time field to 11 a.m. from the diary.
- `cal.1961-06-12.china-leadership-3`: "afternoon" struck from the Liu op, since Liu II 526 gives no hour. Added Peng Zhen at the airport.
- `cal.1961-06-17.china-leadership-2`: the 10 a.m. to 2 p.m. hours and the coal reports are Yang's diary, not Deng III 1645, so they were struck from the op. The entry's Check on whether it is the same session stands. Set the morning time field (Deng). Added the 259th meeting (Peng).
- `cal.1961-07-06.china-leadership-2`: rebuilt from four pages. Yang II 48 gives 3 to 7 p.m. Liu II 528 gives Liu presiding and his words. MacFarquhar 98–99 gives the reports and Kang Sheng's question. Deng III 1647 gives "a constitution for scientific work". Set the time field to 3 p.m.
- `cal.1961-07-24.berlin-and-vienna`: struck "Heller and Samuelson argue against". Heller's meeting came days later, and Samuelson is not on O'Donnell's pages. Struck the whole Fursenko op ("no national emergency ... Acheson and Johnson kept out"). That is the Berlin decision of about July 20, another act.
- `cal.1961-08-01.transition-and-staff`: struck Anthony Lewis's story of July 3. It is now its own entry, `cal.1961-07-03.confirmations` (Navasky 363).
- `cal.1961-08-31.testing`: the meeting began shortly after 10, and 10:45 was the leaders' hour, not the meeting's. Scoville added. Set the time field (approximate) in place of the range by kind.
- `cal.1961-09-01.testing`: the reader's op on Kennedy in his bathrobe was struck here. It is another act from the Soviet test, now its own entry, `cal.1961-09-01.testing-2` (Schlesinger 132–33). Dean was with McCloy.
- `cal.1961-09-15.china-leadership`: Deng Xiaoping was not there. He had gone to Korea (Wu 460), so his name tag was struck. Added Mao's "foot-binding cloth".
- `cal.1961-10-11.vietnam`: "Gilpatric records the meeting" struck. That is FRUS doc. 156, not Moyar 135. Set the morning time field (Futrell 80); the pin is 80.
- `cal.1961-11-06.china-leadership`: "the Politburo, the Secretariat and the six bureaus" is Yang's diary, not Deng's, so it was struck. The Nov. 7 and 10 words are now given as Deng's. Added Peng's "all agree to full contracting".
- `cal.1961-11-08.vietnam`: Ball's 205,000 is McNamara's maximum ground force. The Mann Check now names the card; Mann was not read.
- `cal.1961-11.china-leadership`: "Deng" is now Deng Zihui wherever the report is meant. Pinned at Mao wengao XVI 170, with Peng IV 160–161 for the same part.
- `cal.1961-12-06.china-leadership-2`: added those briefed. MacFarquhar's grain figure is his own, from TJNJ, so it is no longer called the briefing's. The pin is 138.
- `cal.1962-01-17.china-leadership`: added Jan. 17's hours, hall and first speakers (Yang II 114), with the time field and place. *Tiandi fanfu*'s 艄公 is rendered "boatman". The Check now adds Peng IV 168 and *Tiandi fanfu* I 66 for twenty-one members.
- `cal.1962-01-18.china-leadership-2`: set the time field to 3 p.m.
- `cal.1962-01-27.china-leadership`: the 7,000 cadres moved to Dikötter 335. The Hunan saying is cited to Liu II 547. Mubei pinned at II 1125, where the body bears it.
- `cal.1962-04-09.china-leadership`: rebuilt. Yang gives the hours and Liu II 553 gives Liu presiding. Peng IV 187 gives Peng. Zhou, Deng and Zhu De are not added, since their pages were not read in this audit. Set the time field to 3 p.m.
- `cal.1962-05-24.missile-crisis`: Rashidov, Biryuzov and Castro's acceptance moved from Dobrynin 74–76 to Fursenko 438. Fursenko has "late in May", not May 29–30. Dobrynin 76 is kept for Castro's words. Malinovsky, Gromyko and the eleven speakers added (Fursenko 436).
- `cal.1962-06-16.china-leadership-2`: "illicit relations with a foreign country" is not the page's phrase, so I give the denial in plain words. The Check now has both readings: Peng's chronology has him hand the statement to Yang on June 16 (775), Yang's diary has the evening of June 18, "over sixty thousand characters".
- `cal.1962-06-27.court`: Sorensen's passage is on 165, not 166. "The same message goes to Warsaw" struck, as another act.
- `cal.1962-07-02.china-leadership-5`: "the 328th meeting" struck. It is Peng IV 204, not Deng. Deng III 1713 cited beside Mao zhuan for Peng Zhen's call.
- `cal.1962-07.china-leadership-9`: Liu said history will write of Mao and Liu, not of Chen and Tian (Mubei II 1175).
- `cal.1962-08-05.china-leadership`: "noon" struck from the words; the entry's midday range stands. Peng Dehuai's part is pinned at Mubei II 1130, and "his demand refused" is struck.
- `cal.1962-08-06.china-leadership`: Mao's words are now marked as spoken through the conference, not on Aug. 6 (Chen Yun III 137).
- `cal.1962-08-09.china-leadership`: only the first speech is now given as the day's. The rest is given as MacFarquhar's account of the six speeches (277–80).
- `cal.1962-08-10.cuba`: "Murrow present with Rusk, McNamara and McCone" struck. It is the Church report, not Thomas 159. Goodwin's Harvey quotation given in full.
- `cal.1962-08-26.china-leadership`: the Dikötter op struck. Dikötter (CR 17–18) speaks of the Beidaihe conference, not the Aug. 26 meeting, and the cite already on the entry may belong there. In its place: Peng Zhen and Liu Shaoqi attend (Peng IV 213; Liu II 559).
- `cal.1962-09-17.governors-ny`: Smith 379 does not give Robert Kennedy's part or "turned from O'Connor". It says the Harris poll was at the President's behest and that Wagner and Morgenthau needed Buckley. Rewritten so, and the Robert Kennedy tag struck.
- `cal.1962-09-27.china-leadership`: MacFarquhar pinned at 286–88. Kang Sheng tagged.
- `cal.1962-10-16.missile-crisis`: "Johnson sits in the ExComm" and "Taylor is for strikes" struck. They are Caro's and Taylor's, not Sorensen 285–86. Added "about 8 a.m." (Thomas 209).
- `cal.1962-10-20.missile-crisis`: the 2:30 meeting and Rusk's summary are Ball's, not O'Donnell's. Robert Kennedy's call is Thomas 219, on Saturday morning. Added a Check: O'Donnell (364) has the call the night before.
- `cal.1962-10-22.missile-crisis-4`: Humphrey and Hickenlooper moved to Humphrey's memoir, 249. Dirksen's support and Halleck's words (O'Donnell 372) added.
- `cal.1962-10-27.missile-crisis`: Dobrynin has "late Saturday night" at the Justice Department. The 7:45 p.m. hour is Thomas's, so it was struck from the Dobrynin op.
- `cal.1962-10-27.missile-crisis-2`: Protocol 62 and the 5 p.m. broadcast are cited to Presidium I 623, not O'Donnell. Thompson's words are pinned at O'Donnell 381–82.

These ops held as written, or with a pinpoint narrowed: 1960-12-26 (Westad), 1961-01-18 (Wu 445–451), 1961-06-10, 1961-07-20, 1961-09-26, 1961-10-06, 1961-11-23, 1962-01-18 (Jian, *Tiandi fanfu*), 1962-02-26, 1962-06-06, 1962-08-01, 1962-09-24 (the `ok:note-substance` tag), 1962-10-27 (Sorensen), 1961-05-25 (Sorensen 336–37).

## Fields (R25a)

Time fields set by edit, from the pages: 1960-12-07 (afternoon), 1960-12-16 (morning), 1961-06-12 (11 a.m.), 1961-06-17 (morning), 1961-07-06 (3 p.m.), 1961-08-31 (shortly after 10, approximate), 1961-10-11 (morning), 1962-01-17 (3 p.m.), 1962-01-18 (3 p.m.), 1962-04-09 (3 p.m.). Places set: `washington` on 1960-12-16, and `peking` on 1962-01-17 (the Huairen Tang). Fields left unset, and why:

- 1961-01-09 (Cambridge, 2:20 p.m.): the entry's first act is the morning address, whose hour no page gives.
- 1961-11-06: Yang's 3 p.m. is on a page I did not read.
- 1962-10-20: two places on one day, Chicago in the morning and the White House in the afternoon.
- Places for Secretariat and Politburo meetings: no page names one.

## Pages not read, and why

- Taylor's *Swords and Plowshares*, Caro, Reeves, Salinger, Mann, Fursenko and Naftali's *One Hell of a Gamble*: cited in the notes but not on Drive under those titles, or not searched for. No op now rests on them; they are named only in the Checks.
- Chen Yi nianpu 930, Zhu De III 1834 and 1849, Zhou II 470, and Deng III 1700: not read. The attendances they hold were therefore not added.
- Peng Zhen IV 204: not opened, so "the 328th meeting" was struck rather than moved to it.

## What I disregarded under R0

The batch note's limit, "no page newly checked against its image", was the reader's method, not a rule of the brief, so every page above was read. I disregarded nothing else.
