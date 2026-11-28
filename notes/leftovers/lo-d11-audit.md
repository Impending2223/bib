# Audit of lo-d11: July 1963 to January 1964

Opus audit, Nov. 27, 2026, of the reader's patch `inbox/2026-11-27-lo-d11.yaml` and note `notes/leftovers/lo-d11.md`. The patch is corrected in place. `./bib patch-check` shows 0 errors. Nothing merged, built or committed. The brief's wording narrowed nothing, so nothing was disregarded under R0.

## What was read

Each work was fetched from the Drive by the direct route into a directory of my own and deleted after. The offset is PDF page over printed page.

- Yang Shangkun's diary, II (plus 5): pp. 296, 299, 317, 334, 337, 344, as page images.
- The Zhou Enlai nianpu, II (plus 3): pp. 581, 584–85, 588, 592, 600, 605–07, 609, 616–17, from the text layer (its digits garbled, its words clean).
- The Zhou Enlai *Waijiao huodong dashiji* (plus 13): pp. 372, 373, 377, 383–85, 387, 390, 391, as images.
- The Chen Yi nianpu (plus 13): pp. 990, 1004–06, 1008, 1011–12, as images.
- The Peng Zhen nianpu, IV (plus 4): pp. 283, 293, as images.
- The Zhu De nianpu, III (plus 6): p. 1885, as an image.
- The Deng Xiaoping nianpu, III (PDF page plus 1328): p. 1764, as an image.
- Wu Lengxi, *Shinian lunzhan* (plus 8): pp. 608, 616, as images.
- The *Wengao*, XVII (plus 25): p. 101 and its note 1, as an image.
- The *Zhonghua renmin gongheguo waijiao dashiji*, II (2001) (plus 9): p. 319, as an image.
- The Mao nianpu (EPUB): Oct. 29 and 31, 1963.
- From the text layers or the EPUB: *Brothers in Arms*, 385–86; MacFarquhar, III, 352, 394; Fursenko and Naftali, *One Hell of a Gamble*, 284–86; Chang, 241–42, 248–49 and notes 27, 41–43; Dallek, 77–78; Humphrey, 274–75; Kabaservice, 79–80 and notes 27–30; O'Donnell, 441; O'Brien, 156–57; Shesol, 115; Whalen, 64–66; Purdum, 171–72; Albert, 283; White, *Suite 3505*, 240, 259–60; White, *Making of the President 1964*, 12–13 and its footnote, 45; Branch, *Parting the Waters*, 888; Goodwin, *Remembering America*, 244.
- Records: FRUS 1961–63, XV, docs. 222, 224, 225, 227 and 248–256, from `sources/frus-text/`; the Public Papers of 1963, item 349, from `sources/ppp-text/`; the Daily Digest of Oct. 8, 1963 (govinfo), D483–84; the Church Committee's interim report, 223 (AARC copy).

## Ops checked and held

The page bears out the op as written for these:

- The Chinese splits and hours of Oct. 8, Oct. 18, Oct. 31, Jan. 3, Jan. 5, Jan. 6–7, Jan. 10, Jan. 11, Jan. 17, Jan. 26–27, Jan. 28–29 and Jan. 30–31, every clock time and part of the day among them. The fields were checked against the zones of 1963–64.
- The move of the fifth meeting to July 13. Yang (II, 296), the Soviet record (*Brothers in Arms*, 386: Deng's address "yesterday"), the Peng Zhen nianpu (IV, 283) and the Deng nianpu (III, 1764) all give July 13. Wu (608) and MacFarquhar (III, 352) put it on July 12 and stand as variants. The link across two days is rightly removed.
- July 12 at 2 to 6 p.m. (Yang, II, 296), and July 19 at 10 a.m. to 1 p.m. (Yang, II, 299). Wu's "下午会谈" (616) is read on the page and kept as a variant.
- Zhou Yang's article on Dec. 27. The Yang editors (II, 337 n.2) and the *Wengao* (XVII, 101 and n.1) give Dec. 27; MacFarquhar (III, 394) gives Dec. 26 and stands as a variant. Yang's reading of the article now follows the publication.
- Dec. 13: the dashiji (377) has no 上午, so the morning range is rightly taken out.
- FRUS XV, docs. 222, 224, 225 and 227 (Oct. 11–12) and docs. 248–253 (Dec. 28): each new entry holds to its document and its hour.
- The July 31 row's five cites. Fursenko and Naftali (284–85): noon, Novo-Ogarevo, "save the world," Pliyev's "responsive blow," and Troyanovsky before the dictation. Chang (241–42 and n.27): Zorin's welcome on July 14. Dallek (77–78): the evening meeting of Feb. 2. Humphrey (274): "early in the year." Kabaservice (79 and n.28): Rockefeller's letter of Jan. 7.
- Whalen's three votes (64–66), the Daily Digest of Oct. 8 (336 to 3; the Senate gives no count), O'Brien (156–57), O'Donnell (441), White (12–13, 45, 240), the Papers' note on the Huntley–Brinkley broadcast, and the Church report (223, "shortly before nightfall" after the offer "half an hour later").

## Ops changed

- Oct. 3. The Fang Yi entry, after the split, no longer rests on the dashiji. It is now made public 1997, not 1993. Its `also` becomes China's foreign affairs and Africa, and its Pakistan tags come off.
- Sept. 30. The order is reversed. The Peng Zhen nianpu (IV, 293) has the meetings with Mao and the others, then (随后) the banquet. That defeats the dashiji's printed order. The reception speech (`-7`) now follows the meetings (`-8`).
- July 12. "Asks to meet again in the afternoon" is corrected to "at 2 p.m. the next day," by Yang (II, 296: 苏方提出明天下午2时继续会谈), the Soviet record and both nianpus. Wu's "that afternoon" (608) is now a variant. The claim map's rows are adjusted to match. The sentence on the hour is moved before "Names:".
- July 13. The Soviet record's figures for Ponomarev's answer were a "variant" that agreed with the line. They now go into the line by `add-words` (*Brothers in Arms*, 386), and the variant is dropped.
- Dec. 23–24, Albert's call to Colmer, is now split. The night's calls stay Dec. 23 in the night band. The call that reached Colmer at 2 a.m. is new, `cal.1963-12-24.foreign-aid-3`, dated Dec. 24 by the clock. Its day rests on Purdum (172): the House's 7 a.m. meeting was the morning after the party of Dec. 23.
- Jan. 31 and Feb. 1. The 2001 book (319) has the China–Ethiopia communiqué *issued* Feb. 1, which does not conflict with its signing on Jan. 31. The signing entry loses its Check and the book's parenthetical. A new entry, `cal.1964-02-01.china-africa-tour`, records the issue.
- Jan. 10 and Jan. 11. The persons the dashiji names are put into the line: Chaker and Habib Bourguiba Jr. in the morning; Botsio, Bensah and the ambassador on the drive.
- Jan. 7. The tour takes both places, Vlorë and Tirana, and Chen Yi's 中午.
- Jan. 26. The place (Conakry) and the zone are set.
- Dec. 28 (`-5`). Westrick, McGhee, Tyler and Bundy are named in the line.
- Oct. 12. The bombs-in-orbit exchange is added from doc. 227, with Foster.
- Nov. 16. Dave Powers is named.
- Kabaservice: the note to the Jan. 7 entry is on 79, not 80.
- The Papers' note on the Huntley–Brinkley broadcast is on 661, not 658.
- Shesol's 3:38 p.m. is said to carry no zone.
- Whalen: the final vote to report was "scheduled" for the afternoon, not taken. The Whalen Check is now answered.
- Alabama Act No. 514: 8:06 a.m. central standard time is `Etc/GMT+6`, since `America/Chicago` would show 9:06. The note's sentence is mended.
- Fursenko: the new words go at the end of the line, in the session's order, so that "He dictates" does not follow Pliyev.
- White, 45: the old entry's note no longer carries the Funston call, which moved.
- `add-words` on Jan. 18 is moved after its `edit`.

## Struck

Nothing. Every op the reader wrote is borne out by its page, as written or as corrected above.

## Added

- Dec. 29, FRUS XV, docs. 254–256 (R5): `cal.1963-12-29.europe-and-the-alliance-5` (Johnson and Erhard, with Bundy, 11 a.m.) and `-6` (Rusk and Schroeder, 11:30 a.m., docs. 255 and 256, one meeting). `-6` follows `-5` on doc. 255's words.
- Kabaservice's notes 29 and 30 (R13, cited articles): `cal.1964-02-11.elections-1964-primaries` (the Draft Lodge release, with a Check on what it says) and `cal.1964-02-29.elections-1964-primaries` (Mullen's release).
- `cal.1963-12-24.foreign-aid-3` and `cal.1964-02-01.china-africa-tour`, above.
- Order links:
  - Chen Yi's textile-combine poem after the visit (Jan. 3, 之后);
  - the sixth talks after the Vlorë tour (Jan. 7);
  - the Khartoum farewell after the Gezira (Jan. 29);
  - the second Asmara talks after Axum (Jan. 31, the printed order alone);
  - Sept. 30, above.
- Checks:
  - Mao's place on Oct. 31: the Zhou nianpu has Shanghai, the Mao nianpu Hangzhou.
  - Dec. 13: Zhou telephoned Yang at 1 o'clock.
  - The day of the Harrington luncheon, Feb. 3, on `cal.1964-02.poverty-4` (Dallek, 78).
- All six new ids are claimed in the ledger.

## Day order

The days touched were printed with `tools/times/day_order.py` and read together with the patch's entries. Left without a link, the pages read and giving no order:

- Jan. 10, the Neo-Destour visit against the banquet and the farewell call. The dashiji (385) and the Chen Yi nianpu (1008) print them in different orders.
- Jan. 31, the communiqué's signing against the 5 p.m. talks.
- Nov. 22, the Funston call against the toast at the Elms (White, 45).

## Duplicate flags to settle as distinct

At the merge, each of the following is a distinct act of its own day. Settle each with `./bib resolve ID --take keep`.

- Oct. 1963: `cal.1963-10-03.china-zhou-foreign`; `cal.1963-10-08.china-foreign`; `cal.1963-10-11.berlin-and-vienna-5`, `-6`, `-7`.
- Nov. 1963: `cal.1963-11-15.goldwater-4`; `cal.1963-11-16.white-house-2`; `cal.1963-11-17.white-house-2`; `cal.1963-11-22.succession-32`; `cal.1963-11-23.press-and-broadcasting-2`.
- Dec. 1963: `cal.1963-12-24.foreign-aid-3`; `cal.1963-12-28.europe-and-the-alliance-4`, `-5`, `-6`; `cal.1963-12-29.europe-and-the-alliance-5`, `-6`.
- Jan. 1964: `cal.1964-01-03.china-africa-tour`; `cal.1964-01-05.china-africa-tour`; `cal.1964-01-07.china-africa-tour`; `cal.1964-01-10.china-africa-tour`, `-2`; `cal.1964-01-11.china-africa-tour`; `cal.1964-01-27.china-africa-tour`; `cal.1964-01-28.china-africa-tour`; `cal.1964-01-29.china-africa-tour`; `cal.1964-01-31.china-africa-tour`, `-2`, `-3`.
- Feb. 1964: `cal.1964-02-01.china-africa-tour`; `cal.1964-02-02.poverty-2`.

`cal.1964-02-02.poverty-2` keeps the reader's Check on whether Dallek's evening meeting is the task force's first meeting.

## Bases

Every `edit`'s base was compared with `./bib show` after the audit's changes. All 32 are current.

## What still waits, and on what

- Oct. 5, 1963, the hour of the Cabinet Room meeting (`cal.1963-10-05.vietnam-2`). FRUS gives 9:30 a.m. and PRDE 11 a.m. The Miller Center's catalogue was tried. Its pages for JFK Meeting Tape 114 could not be found by address. Its database is a script page that returns no rows to curl, and the repository's Miller Center list has no Kennedy meeting of that day. The tape was not heard.
- Sept. 24, Dillon and Byrd (`cal.1963-09-24.economy-2`). This waits on *Newsweek* of Oct. 7, 1963. The Drive holds no *Newsweek* of 1963: a search by title, and the inventory, show only 1968.
- Aug. 19, LeMay (`cal.1963-08-19.testing`). Chang (249, n.43) cites the Foreign Relations Committee's *Nuclear Test Ban Treaty* (274–75, 397) and the Preparedness Subcommittee's *Military Aspects* (676–77, 707, 738). Neither is on the Drive, by title or full-text search.
- Dec. 14, the hour of Salinger's announcement of Mann (`cal.1963-12-14.latin-america`). Goodwin (244) gives "Saturday, December 14" only. The briefing's transcript is not in hand.
- Sept. 1, the *Pravda* statement's own day (`cal.1963-09-01.soviet-union`). This waits on the paper.
