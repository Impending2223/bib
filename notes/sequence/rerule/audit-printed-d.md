# Audit of the re-ruling of the printed order, October 1963 to July 1964 (part d)

The patch audited is `inbox/2026-11-25-rerule-printed-d.yaml`, written by a Sonnet reader, with its note `notes/sequence/rerule/printed-d.md`. The rule is R25c as the owner rewrote it on Nov. 25, 2026 (owner-rulings 56). I disregarded nothing under R0: the brief set no limit.

The corrected patch is in place: 46 `follows` ops holding 47 links, and the one restored Check. `./bib patch-check` gives 0 errors and 0 warnings. Every link that rests on a printed order says "the printed order alone" with its page. One link rests on the page's own words instead (Dec. 19, 1963), and its basis says so.

## What I read

- The months' notes: `notes/sequence/<month>.md` and `audit-<month>.md` for 1963-10 to 1964-07, and the `remove:` ops of the merged patches (there is one, Dec. 17, 1963, made on other grounds).
- The day sheets for November 1963 to July 1964 (`day_order.py --full`), and the entries themselves (`./bib show`).
- The pages, as page images, nothing changed on Drive: the *Zhu De nianpu (xinbian)*, III, 1885–88, 1895–99, 1903–04, 1912–15 (printed = PDF − 6); the *Chen Yi nianpu*, 993–94, 999–1012, 1017–18, 1025, 1029–30 (printed = PDF − 13); the *Zhou Enlai waijiao huodong dashiji*, 378–81, 383, 385–86, 389–91, 395–98, 401, 405, 409–10, 413 (printed = PDF − 13); the *Zhou Enlai nianpu*, II, 594–96, 600–04, 631, 646, 656 (printed = PDF − 3); the *Peng Zhen nianpu*, IV, 323, 330, 334, 336, 339 (printed = PDF − 4).
- FRUS 1964–68, I, docs. 33 and 34, from the series' own text (`sources/frus-text/1964-02.json.xz`).
- The Church Committee's report, 222–23 (the AARC copy, text layer), and, for two pairs left on a narrative's order, White, *Suite 3505*, 238–40, and Salinger, *With Kennedy*, 345–46 (the owner's Drive copies, text layer).

## The reader's links: 34 kept, none struck, none turned, none pointed elsewhere

I checked every link on its page: which item stands first, whether the volume keeps the order of time on that day, and whether anything goes against the print. Every printed order is as the reader gives it. Nothing in the entries' words, hours or route goes against any of them.

- One page was wrong: Jan. 7, 1964 (`china-leadership-9` after `-8`) is III, 1895–96, not 1896. The Jan. 7 item begins on 1895. Corrected.
- Jan. 5, 1964, `china-leadership-7` (the embassy reception) now follows both `-6` (Chen Yi's return to Tirana) and `-2` (Zhou's return and the fifth talks). The Chen Yi nianpu (1006) prints the return, the 4:30 p.m. talks, then the reception. This is not an entry following two where one is directly before the other. `-2` cannot be put after `-6`, because `-2` also holds Zhou's own return, which no page places against Chen Yi's. So the two are unordered between themselves, and the reception follows each. The link on `-6` rests on the lines and stays.
- Jan. 10, 1964: the dashiji (385) does not print Chen Yi's noon talks at Government House, so only the Chen Yi nianpu prints both items of that pair. The dashiji does print the Majestic banquet before the farewell at Carthage, as the Chen Yi nianpu does.
- Jan. 15, 1964: the dashiji (386) prints Ouzegane first and the banquet last; it has no item for Nkrumah's presents. Neither volume goes against the two links.
- Mar. 17 and 18, 1964: the two acts are two sentences of one item, not two items. The same nianpu's item of Mar. 20 runs in the order of time to "晚" in the same form, so the presumption holds.
- July 30, 1964: the four works are a list in one sentence (III, 1915). That is the weakest form of print order this patch uses. I kept the two links, and they are the first to strike if the owner rules that a list is no order.
- The restored Check on `cal.1964-01-20.china-leadership-4` is right: the Chen Yi nianpu (1010) prints the embassy dinner before the farewell reception at the palace.
- Feb. 4, 1964: FRUS prints Forrestal's memorandum as doc. 33 and Bundy's as doc. 34. Forrestal's is his "overnight thoughts for your lunch today," and Bundy's repeats his first point ("If Lodge must stay"). Nothing goes against the order.

## Links added: 13

Each is a pair the earlier notes left unlinked because a printed order was then no order, or a pair the earlier notes left "for want of a source" that the pages now order.

- Nov. 1, 1963: `vietnam-saigon-7` (the five-minute ultimatum) after `vietnam-saigon-6` (the 4:30 p.m. radio announcement). I ruled on this under owner-rulings 56, reading 5. The Church report tells Nov. 1 through in the order of its hours (late morning, 1:40 p.m., "shortly afterwards," 4:30 p.m., the ultimatum by Conein's report, "half an hour later," "shortly before nightfall," then 6:20 a.m. on Nov. 2). So its page order counts for the day, and the basis names it as a narrative. The entry's "Check: the hour" stays.
- Dec. 12, 1963: `china-leadership-14` (Chen Yi's call on MacDonald) after `-13` (the independence celebrations), both "上午" (Chen Yi nianpu, 999). An untimed cable to Zanzibar stands between them on the page; I did not link it, because this nianpu puts untimed cables first or last in a day by kind (first on Nov. 6, 1963, last on Nov. 7 and Mar. 2, 1964).
- Dec. 19, 1963: `china-leadership-5` (Chen Yi's poem on the Pyramids) after `-2` (the visit to the Pyramids). The basis is the page's own word, "之后" (afterward), not the print (Chen Yi nianpu, 1000).
- Dec. 27, 1963: `china-leadership-5` (the departure from Algiers) after `-13` (the press communiqué on Tunisia), both "上午" (Chen Yi nianpu, 1002).
- Dec. 29, 1963: `china-leadership-9` (the mayor's luncheon at Tangier) after `-8` (the museum and the city). The page prints the tour, the poem "之后," then the luncheon (1003). I named the tour, not the poem, as the entry directly before. This nianpu places a poem with the visit it is about, whenever it was written (Jan. 16, 1964: the poem on Mali stands before the noon luncheon of the first day of the visit).
- Feb. 5, 1964: `china-leadership-7` (Zhu De's cable to the Center) after `-6` (Yang Shangkui's report), and `-8` (leaving Nanchang) after `-7` (III, 1899). The link of `-8` after `-6` already in the tree rests on the lines. I left it, so that it outlives the printed-order links if they are struck.
- Feb. 24, 1964: `china-leadership-2` (the picnic) after `china-leadership` (the morning sitting of the Assembly) (dashiji, 395–96).
- Feb. 29, 1964: `china-leadership-6` (the Japanese journalists) after `-3` (the third talk, 10:15 a.m.), and `-7` (the banquet) after `-6` (dashiji, 397–98). The dashiji prints the journalists between the 10:15 talk and the 6 p.m. talk.
- Apr. 10, 1964: `china-leadership-3` (Zhou welcomes Hill at the airport) after `-2` (Zhou sees off the Japanese delegation) (dashiji, 401). Yang's diary (II, 367) has one morning trip to the airport and does not order the two.
- July 11, 1964: `china-leadership-12` (Zhu De on Changbai Shan) after `-11` (Zhu De at Yanji) (III, 1912). The nianpu prints Yanji first: "抵达延吉市," then "△ 登长白山看天池." The route does not settle it. The reader of July 1964 thought the map puts the mountain first, on the way from Jilin; but a climb from Yanji and back in the day is possible too, and the nianpu has him at Yanji again on the morning of July 12. That is likelihood, not an order, so the print stands.

## Looked at and left without a link

- Nov. 15, 1963, Goldwater at Pittsburgh (the Bioff remark and the Harvard alumni talk). White, 238, has the Bioff remark "on a November visit to Pittsburgh," in a paragraph on the attacks on Goldwater, not in an account of the day. The book does not tell Nov. 15 through in order there, so its page order does not count (owner-rulings 56, reading 5).
- Nov. 15, 1963, Zhou's meeting with Cheng Siyuan (`china-leadership`) and the Supreme State Conference (`-2`). The Zhou nianpu (II, 594–95) prints the conference as an item of Nov. 15 and 16, after the item of Nov. 15 alone. That is its place by dating, not an item of the same day.
- Nov. 16, 1963, Dec. 21, 1963 and Dec. 27, 1963: three pairs that only the Zhou nianpu prints (the State Council and the talk with Liao Chengzhi, II, 595–96; the cable on the UAR visit and the flight to Algiers, II, 603; the telegram on Tunisia and the China–Algeria communiqué, II, 604). I wrote no link. The Zhou nianpu is shown in the same weeks not to keep the order of the day: on Dec. 15, 1963 it prints the talks with Nasser and then, "同日," the visit to the military academy and the museum (II, 601), which the dashiji (378) puts in the morning, before the 6 p.m. talks; on Dec. 19 it prints the talks and then, "△," the Pyramids (II, 602–03), which the dashiji (379) and the Chen Yi nianpu (1000) put before the talks. It puts the day's talks first. This is a default for the owner: if the owner rules that the presumption holds for this volume on days not shown wrong, these three links go in.
- July 11, 1964, Zhou's signing of the Burmese communiqué after the talks. The Zhou nianpu (II, 656) adds it at the end of the day with "同日." For the reason just given, its place is no order. The dashiji (413) puts the communiqué under July 12, "during the visit." No link, as the reader left it.
- Dec. 19, 1963, the Pyramids and the third talk with Nasser: the dashiji and the Chen Yi nianpu print the visit first, the Zhou nianpu the talks first. No link.
- Dec. 27, 1963, Zhou's wreath at the tomb of Mohammed V (`-6`) and his call on King Hassan (`-7`): the dashiji (381) prints the wreath first, the Chen Yi nianpu (1003) the call first. No link.
- June 11, 1964: the dashiji (409) prints the see-off of Sallal first, and the Peng Zhen nianpu (IV, 336) prints the welcome of Kawawa first. I read both pages; the reader is right.
- June 17, 1964, the Secretariat meeting and the closing plenary. The Peng Zhen nianpu (IV, 339) prints the Secretariat first, both "下午." But Yang's diary (II, 385, as the June audit read it) gives the Secretariat 3:30 to 7 p.m., so an afternoon plenary that Peng also attended falls before 3:30. The hour goes against the print, so there is no link on the print. The hours point the other way, but the Secretariat entry has no `time` and the plenary's hour is not given; that is for a times pass.
- Mar. 12, 1964, Peng Zhen's directive and the Secretariat meeting: the directive is the "十二日" inside the Mar. 10 item (IV, 323), placed by subject. No link, as the reader left it.
- Jan. 3 and Jan. 6, 1964: the reader is right that the entries hold several acts. They need a split (R25b) before a link.
- June 14, 1964, Mao's 7 p.m. meeting with Kawawa and Liu's banquet: the dashiji (410) prints them in that order, and the clock and the evening range already place them. No link is needed.
- Nov. 18, 1963 (Tampa, then Miami) and Mar. 18, 1964 (Goldberg's calls): the earlier notes left these on a book's order, but the tree already holds both links, written by the audits of those months.

## For the owner

- The Chen Yi nianpu also departs from the order of the day on two days: on Jan. 20, 1964 (1010) it prints the embassy dinner before the palace reception, which the dashiji puts "after the reception," and on Feb. 29, 1964 (1017) it prints the signing of the communiqué before the banquet, which the dashiji puts "宴会后." Both departures fall inside one part of the day. I kept the presumption for this volume on other days, as R25c says for "the days in hand." The links whose basis is the Chen Yi nianpu's order and no other volume's are on Nov. 6, Dec. 12, Dec. 27 and Dec. 29, 1963, and on Jan. 5, Jan. 10 (the talks after the luncheon), Jan. 12, Jan. 15 (the presents after Ouzegane), Jan. 27, Mar. 2, Mar. 7, May 3 and May 13, 1964.
- The default on the Zhou nianpu above (no presumption within a day) is a reading the owner can overrule.

## What is left

- Entries that hold acts of different hours (R25b): `cal.1964-01-05.china-leadership-2` (Zhou's return and the 4:30 p.m. talks); `cal.1964-02-23.china-leadership-3` (the flight to Lahore in the morning and the wreath at Iqbal's tomb, which the dashiji, 395, puts in the afternoon after the citizens' reception).
- Hours the pages give that the entries lack: `cal.1964-01-05.china-leadership-2`, the talks at 4:30 p.m. (Chen Yi nianpu, 1006); `cal.1964-06-17.china-leadership`, the Secretariat at 3:30 p.m. (Yang's diary, II, 385, by the June audit).
- Mar. 18 and 19, 1964: Salinger (345–46) tells the lunch at the Sans Souci, the Goldberg calls "while waiting" and the President's 3:30 p.m. meeting as one day, the day after Mar. 17. The tree dates the lunch Mar. 18 and the resignation Mar. 19. One of the days may be wrong.

The patch is ready to merge.
