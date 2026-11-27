# Leftovers, batch lo-d06 (November 1960 to February 1961): the audit

Opus audit of the reader's patch `inbox/2026-11-27-lo-d06.yaml`, Nov. 27, 2026, against the pages. The patch was corrected in place. `./bib patch-check` now gives 0 errors and 20 warnings: nine duplicate flags (below), nine "one event?" notes on busy days, and two edits that set only `n` (they reword a Check or correct "Made public", so they cannot be additive ops). Every `edit` base was checked against the tree as it stands; all 36 are current. Nothing was merged, built or committed. The reader's 60 ops are now 86.

## What was read

Every page was read from the owner's Drive copy (each deleted after use), or from the record online. Scans were read as page images.

- *Freedom of Communications*, pt. 1 (printed page = PDF page less 17): 850, 867–68, 875, 882–87, 899–911, 923–31, 938–58, and the volume searched for Burlington.
- O'Donnell and Powers (less 20): 245–52, 274–75, 283. White, *Making of the President 1960* (less 16): 23, 311–13, 329, 338, 341–44. Nixon, *Six Crises* (less 22, images): 371–74. Goodwin (less 12): 127–29. O'Brien (less 14): 94–96, 105–06. Cohen (less 22): 264–65. Thomas (less 2): 110–11. Schlesinger, *A Thousand Days* (less 18): 129–31, 162; *Journals*: 102. Wofford: 85, 130. Branch: 398. Wolff, Senate Republican minutes (less 28): 867, 871.
- Yang Shangkun's diary I (less 6, images): 587, 604–07, 625, 657. Zhou Enlai nianpu II (less 3): 370, 378, 382. Deng nianpu III (images): 1592, 1598–99, 1604. Wu Lengxi (less 8): 387. Peng Zhen nianpu IV (less 4): 75, 103–04. Chen Yun nianpu, revised, III (less 5): 76. Zhu De nianpu, new ed., III (less 6): 1795–96. *Jianguo yilai zhongyao wenxian* XIV (less 15): 126–27. The Mao nianpu EPUB: Nov. 16 and Dec. 9, 1960; Feb. 5 and 19, 1961. Jian, *Zhou Enlai*: 457 and its notes 65–66. Guan: 170–71 and notes 74–76. Westad, *Brothers in Arms* (EPUB): 27.
- FRUS 1961–63, XXIV, docs. 7 and 8 (`sources/frus-text`). The American Presidency Project's text of Eisenhower's election-eve remarks.

## The questions the brief left to the audit

- Lewiston, Nov. 6, 1960. O'Donnell (248) has Kennedy fly "at night" from Jersey City to Lewiston, "arriving there at one-thirty," and "Later that night" go on to Providence. The act is 1:30 a.m. on Monday. The entry keeps its id and is now dated Nov. 7 (`kind: correct`, the record named in the note). The volume's heading, Nov. 6 (927), is a date variant. Its link to Jersey City, now on another day, is removed. Providence's airport remarks (Nov. 7) now follow it.
- Zhou's call of Nov. 16, 1960. The Mao nianpu settles it: Mao's meeting on the delegation's telegram was in the evening, in the Huairen Tang's lounge, and "after the meeting" Zhou telephoned Deng Xiaoping. Deng's nianpu has Deng on the line. Yang's diary (607) has Deng report the call at the embassy after the day's session. The Zhou nianpu (370) gives the evening meeting but not the call. So the call's line now says "after Mao's meeting" and "Zhou Enlai calls Deng Xiaoping" (`kind: correct`). Its morning range is taken out, and it follows the meeting. Wu's "next morning" and his "for Yang Shangkun" (387) are variants. The meeting's entry was given the evening range its line already stated. The call is left unordered against Deng's two evening talks at the embassy: Deng's nianpu prints the call after them, while Yang has it reported at the dinner after the session. The note says so.
- Nov. 5, 1960, the lost motorcade. Goodwin (127–28) has O'Donnell say they "spent the whole afternoon riding around the Bronx". The Senate's print has Kennedy at a Queens rally "at 2:15 in the afternoon" (904) and in Nassau County "on a Saturday afternoon" (905). Under R24 the line now says the account is Goodwin's (`kind: reword`). The FoC reading is a variant, and the Check names all three books.
- Nov. 5, 1960, the evening stops. White's "midnight" street corner (329) prints the words of the remarks outside the Coliseum (908–09), so that entry's place is now "outside the Coliseum" (`kind: correct`). Its Check on the place is settled; a Check on the hour remains (White's own 12:30 a.m. at Bridgeport, 338). The 90th Street rally now follows both the remarks outside the Coliseum and the Commodore. Its text says "We will now move on to Waterbury" (907) and puts the Waterbury rally at 2 a.m., where the remarks outside the Coliseum say 1 a.m. The remarks outside the Coliseum follow the Coliseum speech: Goodwin puts the speech about two hours after 6 p.m., and White puts the remarks at midnight. The Commodore against the Coliseum speech and the remarks outside is still unordered: no page read orders them.
- Dec. 3, 1960. Guan (170) has Lê Duẩn and Nguyễn Chí Thanh in Hồ's delegation, back in Peking that day, and their afternoon meeting with Central Committee members told apart from the welcome, in a report of its own (n.75). So the meeting follows the airport welcome. The reader's Check is replaced by the link. The meeting's own note, n.75 (NCNA, SWB/FE/507/A3/2), is added to "To check:" and the map. The tree had cited n.74a, which is the welcome's.
- The splits' claim maps. Each was checked against its line. Rows that went with words moved to another entry were taken out, and each map's hash was checked against its new line. Rows were changed on the telethon (Dewey and the half hour gone), the Manchester park, Chicago, Dec. 1, Jan. 9 and Nov. 16. The Eisenhower Public Papers row had been mapped to Dewey's quarter hour; it goes, with its Check, to the Chicago telecast.

## Ops changed

- Nov. 7, Nixon: the telethon's line had also held Dewey's quarter hour, which White times at 6:30 Eastern (312). Under R25b it is now an entry of its own (`cal.1960-11-07.elections-1960-nixon-2`, claimed). Lodge's part by split screen goes into the telethon's line (Six Crises, 372). The Chicago telecast loses "Nixon leaves for Los Angeles", which is the next entry's act. It takes the Public Papers item, White 312 and White's "eleven in the evening" as a time variant. Nixon's departure now follows the telecast (Six Crises, 374), not the studio scene.
- Nov. 7, Kennedy: the Boston Garden's line named "Jean Kennedy" as a sister. The text (950) has two sisters and "The wife of my brother, Teddy", and the line is corrected. White's order is now cited 343–44 ("Then he proceeded to Faneuil Hall"). The names on the park and the television program now match their lines, and Burlington takes White 344 too. The watching of Nixon's telethon on the Caroline now follows the telethon.
- Nov. 8, Chicago. White (23) gives Robert Kennedy's calls to Daley no hour: his "about one a.m." is Eisenhower's wire, and Cohen's "around 1:00 a.m." (265) misreads him. The entry's time field, which rested on Cohen alone, is taken out, and the Check stays. The entry keeps Nov. 8. Daley's call to O'Donnell "At three o'clock in the morning" (252) is a time on another day, so the new entry is dated Nov. 9, under a new id (`cal.1960-11-09.elections-1960-chicago`). The old claim was released in the ledger. The broken single-bracket link was repaired.
- Nov. 3, Phoenix: the breakfast's hour is now quoted whole: "at 3 o'clock in the morning or at 9 o'clock in the morning," the breakfast being the second.
- Dec. 1: the Foreign Relations hearing and Wofford 85 move to the Williams entry. Ribicoff's entry gets "Check: the day of Ribicoff's naming", because Schlesinger has him only decided (130).
- Dec. 9: Liu's evening report also takes the Mao nianpu (晚上, the Yinian Tang, Peng Zhen present).
- Dec. 20: "Made public" is now 1997, the *Wenxian* volume, which the entry cites as read. Before, it was the 2016 book.
- Jan. 9: the new afternoon entry lacked *A Thousand Days*, 162, which is the only page that bears out Bundy's post, Chayes, Seaborg's offer and Bowles. It now cites it, takes the place `cambridge-ma`, and follows the morning's entry ("After luncheon"). The morning entry's note, names and tags now cover its own line only. Its note had said "leaving shortly before 5", where the Journals say "shortly after 5"; this is corrected.
- Jan. 24: the Rules remark's 9 a.m. rested on Caro, a book the entry does not cite. It is replaced by O'Brien's "That morning" (105), and the remark follows the breakfast it names.
- Jan. 3: the order now also rests on the Republican conference's adjournment at 11:45 a.m. (Wolff, 871).
- Feb. 8, Zhu De: the nianpu's own "昨日" makes the trip Feb. 8, but on that day the same nianpu has him at the Gutian reservoir's power station (1795). The Check is reworded rather than settled.
- Feb. 28: Chervonenko's handing Liu Khrushchev's letter (Chen Yun nianpu, 76 n.1, the source of the afternoon) goes into the line (R33b).
- Nov. 16: Zhou's talk with Li Fuchun and others on the Moscow conference now comes before Mao's evening meeting, on the printed order alone (Zhou II, 370).

## Struck

- The new entry for Mao's endorsement of grain imports on Dec. 30, 1960, and its link. Jian's endorsement (457 n.65, "the chairman's comments during reports by the central bureaus") is the afternoon report meeting already in the tree (`cal.1960-12-30.china-leadership`), which already cites Jian 457. Jian's order is also against the records: Zhou left Peking in the morning (Zhou waijiao huodong, Chen Yi and Peng Zhen nianpu), and the meeting was in the afternoon. Jian's words go into the meeting's line as his account, with Zhou named. The airport entry takes a Check on the order.

## Held as the reader had them

The hours and zones of the evening, morning and afternoon ranges were each checked against the page and against the bands in `tools/bib/dayorder.py`. The Laos time (FRUS XXIV, doc. 7, "this morning at 9:00 o'clock"; doc. 8, "approximately 9:45 a.m.") holds. So do the Nov. 5 Moscow link (Yang I, 587, the diary's order), the Nov. 23 variant (Yang I, 625), the Feb. 7 date variants (Wofford 130, Branch 398), the Feb. 5 and 19 evenings (Mao nianpu), the Feb. 17 split (Peng IV, 104), the Feb. 26 entry (Yang I, 657), the Dec. 20 forwarding (XIV, 126) and the Jan. 20, 21 and 24 ranges. No later commentary was found in any line the patch writes (R19b).

## For the merge

- Settle as distinct (`./bib resolve ID --take keep`): `cal.1960-11-07.elections-1960-nixon`, `cal.1960-11-07.elections-1960-nixon-2`, `cal.1960-11-07.elections-1960-kennedy-8`, `-9` and `-10`, `cal.1960-12-01.transition-and-staff-cabinet-5`, `cal.1961-01-09.transition-and-staff-2`, `cal.1961-02-17.china-center`, and `cal.1961-02-26.china-leadership-8`. Each is a separate act from the entries flagged with it.
- The Lewiston entry keeps the id `cal.1960-11-06.elections-1960-kennedy-7` and moves to Nov. 7. The merge re-sorts it by date.

## What still waits

- The order of the Commodore dinner against the Coliseum speech and the remarks outside it (Nov. 5). This waits on the day's schedule or the papers of Nov. 6, which cannot be read here (R56).
- Zhou's call against Deng's evening talks with Lukman and Sharkey (Nov. 16). Every page that bears on it was read; the pages give no order.
- The hour of Robert Kennedy's calls to Daley (Nov. 8). This waits on a record with the hour.
- The day of Ribicoff's naming (Dec. 1). This waits on the Kennedy Library's release or the papers of Dec. 1–2.
- Not read: Sorensen's *Kennedy* (210, 233–34), Kallina (159, 165), *RN* (221–22), the Liu Shaoqi nianpu (II, 499) and *Mao Zedong zhuan* (V, ch. 66). Their earlier pinpoints were kept where the words they stand for stayed. They were not cited for anything new.

Disregarded under R0: nothing in the brief narrowed what is an entry.
