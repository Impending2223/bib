# Audit of the re-ruling of the printed order, group e (Aug. 1964 to May 1965)

The patch audited is `inbox/2026-11-25-rerule-printed-e.yaml`, written by a Sonnet reader, with its note `notes/sequence/rerule/printed-e.md`. The rule is R25c as the owner rewrote it on Nov. 25, 2026 (owner-rulings 56). I read the reader's brief, the rulings 55 and 56, the guides the brief names, and the twenty notes of the ten months (`notes/sequence/<month>.md` and `audit-<month>.md`). I read each link's two entries with `./bib show`, the day sheets for the ten months, and the page of every volume a link rests on. The patch is corrected in place. `./bib patch-check` gives 0 errors and 0 warnings. I disregarded nothing under R0: the brief narrowed nothing.

## What I read on the page

- *Chen Yi nianpu*, 1052–54, 1064, 1067–69, 1071, 1073, 1075–77, 1081, 1085, 1090, 1097 (page images; the printed page is the file's page less 13).
- *Zhou Enlai waijiao huodong dashiji*, 416, 417, 425, 426, 431, 433, 437, 442, 443, 446, 447 (page images; the printed page is the file's page less 13).
- *Zhou Enlai nianpu*, II, 698–700 (page images; the printed page is the file's page less 3). The Drive file is the whole volume, 773 pages. The `file` command reports "4 page(s)"; `pdfinfo` gives the real count. That is likely why the reader thought the copy held four pages.
- *Peng Zhen nianpu*, IV, 381–83 and 399 (page images; the printed page is the file's page less 4).
- *Mao Zedong nianpu*, the EPUB, the item of Dec. 23, 1964.
- *Liu Shaoqi nianpu* (1996), II, 610 (page image), for Dec. 16, 1964.
- *Nikita Khrushchev. 1964*, 148–53, docs. 21–23 (text layer).
- Mann, *A Grand Delusion*, 355–59, and Woods, *Fulbright*, 353–54 (text layers).
- The Public Papers, 1963–64, 1116–28, items 596–598 (govinfo's PDF).

Each copy was fetched into a directory of my own under /tmp and deleted after reading. Nothing on Drive was changed.

## The counts

- Links in the reader's patch: 11.
- Kept: 10. Seven rest on the printed order alone, as the reader wrote them. Three are kept on a better basis (Aug. 5, Sept. 25, Mar. 22).
- Struck: 1 (Dec. 23).
- Turned round: none. Pointed at another entry: none.
- Added: 20.
- The patch now holds 30 links and 1 `check` op. Of the 30 links, 25 rest on the printed order alone and say so in their basis; 5 rest on words, parts of the day or the route.

## Struck

- Dec. 23, 1964, the reception of the Cuban ballet's heads (`cal.1964-12-23.china-leadership-5`) after Zhou at the performance and the dinner (`-2`). The *Chen Yi nianpu*, 1075, prints the performance, then the dinner ("随后"), then the reception as a separate evening item. Two other chronologies go against that order. The *Mao Zedong nianpu*, Dec. 23, has Mao and the others meet the heads "并观看古巴芭蕾舞团的演出" (and watch the performance). The *Peng Zhen nianpu*, IV, 381, has Peng watch the performance "并接见" the heads. Both tie the reception to the performance, and neither puts it after the dinner. The entry `-2` also holds two acts, the performance and the dinner. So the reception's place against them is not known. No link.

## Kept on a better basis

- Aug. 5, 1964, the meeting in Mansfield's office (`cal.1964-08-05.vietnam-congress`) after Fulbright at the White House (`-2`). Mann is a narrative book. It does not tell Aug. 5 through in order: it tells the Syracuse speech of Aug. 5 (355), then goes back to the briefing of Aug. 4 after a section break, and gives the White House meeting no hour (356). So its page order is no basis under ruling 56, reading 5. But the sources' words show the order. Woods, 353: at the White House Fulbright agrees to manage the resolution "that Johnson would submit to Congress that day", so the resolution had not yet gone up. Mann, 357: in Mansfield's office that afternoon Mansfield wants it passed "just as Johnson had submitted it". The basis now says this. Woods puts the Mansfield meeting on the morning of Aug. 6, a Check already on that entry; the link holds while both entries stay on Aug. 5.
- Sept. 25, 1964, Eufaula (`cal.1964-09-25.elections-1964`) after El Paso (`cal.1964-09-25.latin-america`). The Papers print El Paso as item 596 (1117) and Eufaula as item 597 (1122). But the President's own words settle the order. At Eufaula he speaks of "this peaceful site out here this afternoon" and says "I flew over this afternoon from Muskogee" (1126). At Oklahoma City he says "This morning I stood with the President of Mexico" (1128). The basis now gives these words, not the printed order.
- Mar. 22, 1965, Zhou leaves Peking for Romania (`cal.1965-03-22.china-leadership-2`) after he sees Chen Yi off at the airport (`-4`). The dashiji, 442, prints the seeing-off first, both in the morning. The route also shows the order: Zhou sees Chen Yi off at the Peking airport and leaves Peking himself that morning. The basis now says "the printed order ... and the route", without the word "alone". The day of the seeing-off is in doubt: the *Chen Yi nianpu*, 1090, has Chen Yi leave Peking on Mar. 19, and the entry carries that as a Check and a variant. That is a doubt of the day, not of the order. The link holds while both entries stay on Mar. 22, as other audits have ruled for such days.

## Kept as the reader wrote them

Each of these I read on the page. The volume is in the order of time on the day, and nothing in the entries, their hours, the route or another source goes against the printed order.

- Sept. 29, 1964, Khrushchev's toast at the lunch for Sukarno (`soviet-union-leadership-2`) after the talk (`soviet-union-leadership`). The volume prints doc. 21 (Sept. 26), doc. 22 (the talk) and doc. 23 (the toast), then Part II from Oct. 1. The talk opens with the two men's greetings (150). The basis now names the documents.
- Oct. 24, 1964, Chen Yi and Guo Moruo receive the ballet's directors and dancers (`-12`) after *Coppélia* (`-11`). *Chen Yi nianpu*, 1064: the afternoon item, then the performance, then the reception.
- Dec. 13, 1964, the reception of the Reda troupe's heads (`-5`) after its first performance (`-4`). *Chen Yi nianpu*, 1073.
- Dec. 16, 1964, Liu Shaoqi receives Ouzegane (`-4`) after Chen Yi's banquet for him (`-8`). *Chen Yi nianpu*, 1073: the airport in the morning, the talks at noon, the banquet, then Liu's reception. The *Liu Shaoqi nianpu*, II, 610, has no item for the reception. The entry's other source, as its note gives it, has no hour.
- Dec. 27, 1964, the reception of the minority nationalities' representatives (`-6`) after the reception of the CPPCC members (`-5`). *Chen Yi nianpu*, 1076. The *Peng Zhen nianpu*, IV, 381, prints the two in the same order; the basis now names it too.
- Dec. 31, 1964, Chen Yi and Guo Moruo receive the Cuban delegations (`-12`) after the capital's meeting (`-11`). *Chen Yi nianpu*, 1077.
- Feb. 17, 1965, the banquet for Nyerere (`-3`) after the meeting with him (`-2`). *Chen Yi nianpu*, 1085: the airport in the morning, the meeting, then the banquet. The dashiji, 437, prints the meeting and the banquet in the same order. On that day the dashiji does not keep the order of time: it prints an afternoon visit to the museum after the two evening items. So the dashiji carries no presumption on Feb. 17, and the link rests on the *Chen Yi nianpu* alone.

## Added: 20 links

These are pairs the months' notes left without a link because nothing but a volume's order spoke to them ("nothing says which came first", "no order in the nianpu", "no order in their words"). I read each page.

- Sept. 27, 1964, Liu's speech at the banquet for Sihanouk (`-4`) after Liu's and Zhou's meeting with him (`-2`). *Chen Yi nianpu*, 1052–53; the dashiji, 416, has Zhou "会见……并出席……欢迎宴会".
- Sept. 29, 1964, Zhou and Liu meet Keita and give the banquet (`-8`) after Mao meets Massamba-Débat (`china-leadership`). The dashiji, 417, prints Mao's meeting at 7 p.m., then the Keita meeting and banquet in the evening. The *Chen Yi nianpu*, 1053, prints the same order (it puts Mao's meeting in the afternoon).
- Sept. 29, 1964, Chen Yi at the evening of arts (`-16`) after the Keita meeting and banquet (`-8`). *Chen Yi nianpu*, 1053–54.
- Nov. 2, 1964, Zhou at the evening of arts for Keita (`-4`) after his banquet for Keita (`-3`). The dashiji, 426.
- Nov. 9, 1964, Chen Yi's afternoon call on Lon Nol (`-12`) after the independence ceremony and the wreath (`-11`); and Sihanouk's state banquet (`-14`) after the banquet of Sihanouk's wife (`-13`). *Chen Yi nianpu*, 1067–68.
- Nov. 10, 1964, a chain of six. Chen Yi at Phnom Penh: the stadium and museum (`-12`), the aircraft's wreckage (`-13`), the advisers (`-14`), Huot Sambath (`-15`), all in the morning; then Kantol receives him (`-16`), he receives the Friendship Association (`-17`), and the evening of arts (`-18`). Each follows the one before. *Chen Yi nianpu*, 1068–69.
- Nov. 13, 1964, Chen Yi leaves Phnom Penh in the morning (`-7`) after his talks with Sihanouk (`-6`). *Chen Yi nianpu*, 1069.
- Dec. 4, 1964, Chen Yi's call on Maung Lwin and the banquet (`-8`) after his morning call on Ne Win (`-7`). *Chen Yi nianpu*, 1071.
- Dec. 30, 1964, the presidium adopts the lists in the evening (`-5`) after the Supreme State Conference (`-2`). *Peng Zhen nianpu*, IV, 382–83: the conference, then "晚" the presidium. This is the pair the reader left unread.
- Jan. 23, 1965, Zhou at the airport for Subandrio (`-4`) after Zhou receives Raza in the airport's VIP room at 4 p.m. (`-3`). The dashiji, 433, prints the 4 p.m. talk first. Without the link the welcome's afternoon range puts it before 4 p.m.
- Mar. 24, 1965, Zhou's calls on the heads of the Korean, Vietnamese and Albanian delegations (`-3`) after the funeral (`-2`). The dashiji, 442: the funeral in the morning, the calls in the afternoon and evening. This rests on the parts of the day, not on the printed order.
- Mar. 29, 1965, Zhou's farewell banquet at Tirana (`-2`) after the rally in Skanderbeg Square (`china-leadership`). The dashiji, 443–44: the rally in the afternoon, the banquet in the evening. This too rests on the parts of the day. The rally entry has no range, so without the link it sorted after the banquet.
- Apr. 16, 1965, Zhou meets Kim Il Sung at Subandrio's residence (`-3`) after Zhou and Chen Yi call on Subandrio (`-9`). *Chen Yi nianpu*, 1097.
- Apr. 17, 1965, Zhou and Chen Yi call on Sihanouk (`-2`) after they call on Sukarno (`china-leadership`). The dashiji, 447, and the *Chen Yi nianpu*, 1097, print the two calls in this order.

## The check added

- Jan. 5, 1965, `cal.1965-01-05.china-leadership-2`. Its line begins with Zhou's election as the CPPCC's chairman and cites the Zhou nianpu, II, 699. That page gives his words at the presidium's fourth (enlarged) meeting and his closing speech, but not the election. A `check` op says so.

## Left without a link

- Jan. 5, 1965, Zhou's closing speech (`-3`) and the entry for his election and his presidium remarks (`-2`). The nianpu, II, 699, prints the presidium remarks first, and those remarks look ahead to the election ("选出以后"). But `-2` holds two acts, and the page does not print the election, so a link would place the election before the speech with no page to show it. Split `-2` under R25b; the presidium remarks would then come before the closing speech on the printed order.
- Apr. 17, 1965, the three-party talks at Bogor (`-3`) against the two calls. The dashiji, 447, prints the talks last; the *Chen Yi nianpu*, 1097, prints them first. The two volumes disagree, so no link.
- Dec. 23, 1964 (struck, above).
- Jan. 4, 1965, the NPC's closing and Chen Yi with the deputies; Dec. 3, 1964, Chen Yi leaves Jakarta and the joint communiqué; Sept. 27, 1964, Mao's meeting with Sihanouk. In each the two entries rest on different volumes, so no one volume prints them both. The dashiji, 416, puts Mao's meeting with Sihanouk on Sept. 28 at 6 p.m., against the Mao nianpu's Sept. 27.
- Sept. 2, 1964 (the Statutes' page order and Public Law numbers) and the diary days (Yang Shangkun; Lady Bird Johnson, Nov. 17, 1964) stay as the reader left them: serial numbers and diaries fall under ruling 55's second and third defaults, not under this pass.

## What is left

- Other pairs the notes leave with "nothing says which came first", where a chronology may print both items, were not read in this pass: for example Oct. 3 and 5, 1964 (the Congolese communiqué and the see-off; Ouzegane's cable and his see-off), Nov. 1, 1964 (Zhu De's reception of the Matsuyama Ballet's heads and its performance), Dec. 12 and 21, 1964, and May 19, 24 and 26, 1965. Each wants its volume's page.
- Oct. 29, 1964: the note of `cal.1964-10-29.china-leadership-5` puts Zhou's talk with the ambassadors at 7 p.m. that day, but the dashiji, 425, prints a talk with six ambassadors at 9 a.m. on Oct. 30. The day wants checking.
- Fields the pages give that the entries lack (R25a): Eufaula, Sept. 25, 1964, the afternoon (1963–64 Pub. Papers 1126); the Skanderbeg Square rally, Mar. 29, 1965, the afternoon (dashiji, 443); Mao's meeting with Massamba-Débat, Sept. 29, 1964, 7 p.m. (dashiji, 417); the funeral of Mar. 24, 1965, the morning (dashiji, 442). The Khrushchev talk of Sept. 29, 1964 has a Check on its place; the record has a crystal "на рабочем столе" (on the desk), which suggests Khrushchev's office.
- `cal.1964-12-23.china-leadership-2` holds two acts, the performance and the dinner: split under R25b.

The patch is ready to merge.
