# Audit of the second time splits, Nov. 25, 2026

The patch is `inbox/2026-11-25-time-splits-2.yaml`, corrected in place. The reader's own copy is kept outside the repository for comparison only. `./bib patch-check` now shows 0 errors; its warnings are the same-day and "one event?" flags, which the merger settles.

## What the audit found, in general

- No edit named the record that gives the moved act its own hour or day, so none met R22. Each edit's note now says it, by page or document ("Branch, 145, gives Moyers's report to Johnson its own hour").
- Many notes said how a page was read ("read on the page images, PDF page = printed page + 8", "hour read on the text layer", "the copy is a table of contents only", "not among the Drive copies"). CLAUDE.md now forbids anything about a copy in a note the site prints. All of it is out.
- The reader thought the Mao nianpu on Drive was only a table of contents. It is the whole chronology, despite its file name. It was read here, and it gives the hours the reader could not set: Bengbu, a little after 3 a.m. on June 29, 1960; Zhou's draft of the reply to Moscow at 10 p.m. on Nov. 17, 1960 (so there is no conflict of day with Zhou's chronology); the note handed to the Indian embassy at 3:40 p.m. on Sept. 19, 1965; Mao's talk on the train at noon on Sept. 16, 1967.
- Shulimson and Cosmas were read online (archive.org). Shulimson gives the hours of Harvest Moon: the ambush of the rangers at 1:30 p.m. on Dec. 8, the attack on the 5th ARVN Regiment's command group at about 6:45 a.m. on Dec. 9, and the Marines' lift at 10 a.m. MACV's volumes give Phase II of Junction City at 12:01 a.m. on Mar. 18, 1967, the Tet cease-fire at 8 a.m. on Feb. 8, 1967, and IV Corps at about 2:30 a.m. on Jan. 31, 1968.
- Several first entries kept names in "Names:" or in tags after the person's act had moved out (Clark at Selma; Moyers and Johnson in Birmingham; Johnson and Dulles in Mississippi; Rusk in the Berlin convoy; Wheeler in the May 1 Dominican entry; Bhutto, Thant, Moyers and Johnson on Sept. 20, 1965; Harriman, Vance, Xuân Thủy and Johnson in Paris; Moss in Seattle). These are now matched to the line.
- `follows:` is added where the record gives the order, with its basis in the note.
- Since the patch was written, other runs changed two of its entries in the tree (Santo Domingo, Apr. 28, 1965, and the Wise Men). Those two edits are rebased on the current text, and what the other runs added is kept. A new rule of Nov. 25 makes an edit list the Checks it answers in `settles:`; seven edits now do.

## Each split

- Freedom Rides, May 15, 1961: Branch, *Parting the Waters*, 426–29 read. The 10 a.m. call and the flight near midnight held. Patterson's refusal to guarantee safe passage was said on the radio (427), not to Kennedy; the first line now says so. Seigenthaler's entry now names Robert Kennedy, who sent him.
- San Blas, Apr. 17, 1961: Jones, 105 read. "About 3:00 p.m." held. The reader quoted "About 3:00 p.m. local", but "local" belongs to "local militia", so the quotation is cut back.
- Khrushchev's greeting, Dec. 31, 1960: Salinger, 61–62 read. The hours held. Merriman Smith was of UPI, not the AP; Arrowsmith was the AP's. The new entry now says so.
- Selma, Mar. 15, 1965: Branch, *At Canaan's Edge*, 105–08 read. The service set for two o'clock and the march at 5:08 p.m. held. Bernstein's crowd Check moved with the march.
- Birmingham, Mar. 21, 1965: Branch, 140 and 145 read. Johnson was at the LBJ Ranch, so Moyers's report is placed at Washington and the Ranch, not Birmingham. Branch's note dates the memorandum 10:45 p.m., so the report now has that hour instead of a range. The two bombs found on Monday, Mar. 22, are an entry of their own.
- SNCC, Mar. 5–7, 1965: Branch, 29, 40–42, 50 read. All held. The first entry is now Mar. 5 only.
- Mississippi, June 21–23, 1964: Dittmer, 247 and Branch, *Pillar of Fire*, 366–67 read. All held. The first note had the arrest's time twice and an old Check on the station wagon's day; Branch settles the day, so the Check is listed as settled. The station-wagon entry no longer cites the Public Papers or the Court, which say nothing of the find, and no longer names Price.
- Berlin convoy, Nov. 4–5, 1963: FRUS XV, docs. 234 and 236 read. All held. Doc. 234, n. 1 places the convoy at Marienborn and gives the hour its detention was reported (5:02 a.m., Nov. 4); the first entry now has the place (a new place key, `marienborn`) and a Check on the hour of the stop. The release is placed at Marienborn, not Berlin. The record the note cites (telegram 641) now stands behind "To check:".
- Ball at Athens and Ankara, June 10–11, 1964: Ball, 352–55 read. All held. Ball's talk with İnönü now has a range: after the 9 a.m. meeting with Erkin and before Ball took off at 12:30. FRUS XVI, doc. 64 is Ball's report of June 11 and says nothing of the 2 a.m. arrival or the Erkin meeting, so it is cited only on the İnönü entry.
- Santo Domingo, Apr. 28, 1965: FRUS XXXII, docs. 28, 29, 32, 34, 35, 36 and the Public Papers' note read. The reader turned 2327Z into 7:27 p.m. local. 2327Z is 23:27 UTC, which is 7:27 p.m. in Washington; the `time` field is corrected. Doc. 34's stamp is likewise Washington's 7:02 p.m. Another run had added doc. 32 (Bennett's Critic 5, 2040Z) to the first entry. Docs. 28, 29 and 32 give three more acts their own hours, and each is now an entry: Benoit's telephoned request for 1,200 Marines (1900Z), the junta's written request (2015Z), and Bennett's "I recommend immediate landing" (2040Z). The first entry keeps the junta's officers alone.
- Dominican plans, May 1–2, 1965: Poole, 141–42 read (archive.org). All held. The hours are on p. 141, so the pinpoints are narrowed to that page. Masterson's reply is no longer placed at Washington. A `follows` across the two days was removed, since check refuses it.
- India–Pakistan, Sept. 20–22, 1965: FRUS XXV, docs. 222–223 and the Public Papers' note read. All held. The cease-fire's taking effect is no longer placed at New York.
- Indonesia, Mar. 12–15, 1967: FRUS XXVI, doc. 233 and its note 2 read. All held. Telegram 4239 now stands behind "To check:".
- Railroads, July 9–10, 1963: the American Presidency Project's pages read. Neither gives an hour. Kennedy is added to "Names:".
- Feb. 5–6, 1964: the Weizmann dinner's page read (APP). It gives the Waldorf's ballroom and no hour.
- Johnson's day, Oct. 27, 1964: White, *1964*, 372–73 read, and the APP pages for the three stops. The first entry had kept the 2:30 a.m. end of the night's paper work as its time, though its act is Johnson's waking at nine. It now has 9 a.m., and the paper work (11:30 p.m. Oct. 26 to 2:30 a.m.) is an entry of Oct. 26. The Papers' notes give Pittsburgh 9 p.m. and Evansville 11 p.m., which the reader said no source gave; both are set, with a Check on Evansville's clock. White's page gives three more acts that are now entries: Glenn's promotion, the hour with Latin American diplomats, and the taping of spots before the flight.
- The editorial of June 29, 1960: the Mao nianpu read. The hour (a little after 3 a.m., at Bengbu) is now set. A Check on the "Mao leaves Shanghai June 29" entry notes that he reached Bengbu at 3 a.m. that day.
- The reply to Moscow, Nov. 17, 1960: Zhou's chronology, II, 370 (page image) and the Mao nianpu read. The nianpu gives "十七日晚十时", so the hour is set and the day agrees with Zhou's chronology.
- Hunan, Jan. 24–26, 1968: Zhou's chronology (2020), III, 210–211 (page images) read. The hour held. The page does not say the talk came after the Liaoning and Jilin reception, so that claim is out.
- The Yunnan earthquake, Jan. 5–7, 1970: III, 335 (page image) read. All held.
- Chengdu and Emei, June 25–26, 1963: Wu Lengxi, 594–595 (page images) read. All held. The first line's "and back" went with the return, and its `when` is now June 25. `follows` was added through the evening and the night.
- Yang Shangkun's acupuncture, Dec. 1963: the diary, II, 335–336 (page images) read. All held.
- Mao's revision of the note to India, Sept. 19, 1965: the Mao nianpu read. The 3:40 p.m. hand-over is set on the Foreign Ministry's entry (`cal.1965-09-19.china`), in place of the reader's "to check". A Check notes that India's note was of Sept. 17 by the nianpu and the Wengao, not Sept. 7.
- Election eve, Nov. 7, 1960: APP's Faneuil Hall program read. "Eleven o'clock, election eve" held.
- Chicago, Aug. 24 and 27, 1968: *Rights in Conflict*, 135, 138, 184–85, 189–90 read. All held. The barn arrival at about 8:56 is on pp. 189–90, not 189.
- Portland, Sept. 27–28, 1968: Chester, 646 and Solberg, 379–80 read. Chester says "Shortly after midnight", so the night's work now has a one-hour range in place of the whole predawn band. The reader's Check is answered.
- Seattle and Salt Lake City, Sept. 29, 1968: Humphrey, 401–02 read. It places the 2 p.m. meeting in Seattle, before the flight to Salt Lake City, so its place and Pacific hour are set. The night's session in Salt Lake City, to about 2 a.m., had stayed in the first entry. It is now an entry of its own, with Chester's, Solberg's and O'Brien's differing ends as Checks and Solberg's 4:30 a.m. as a variant.
- Paris, Oct. 30–31, 1968: FRUS VII, docs. 153, 156, 158 read. All held.
- Election day, Nov. 5, 1968: Solberg, 403–04 and White, 395 read. The hours held, though "Even at nine" says the hall was full at nine; the vote's line now says so. Humphrey's dinner at Andreas's on Lake Minnetonka, which the first entry's cite named, is now an entry between the vote and the Leamington.
- Berkeley, Oct. 1–4, 1964: the leaflet read. All held. It also gives 500 police on the campus at 5 p.m. on Oct. 2, which is now an entry before the pact.
- The Wise Men, Mar. 25–26, 1968: FRUS VI, docs. 156–158 read. Doc. 158 n. 1 times Bundy's summary to a third meeting, 3:15 to 4:32 p.m. The reader had folded it into the meeting of 1:15 to 3:05. It is now an entry of its own, and the 1:15 entry holds that meeting's own words (Wheeler's and Abrams's briefings). Another run had added a Check that the line gave the group the wrong hours; the split answers it.
- Nixon and Johnson, Dec. 11–12, 1968: FRUS XIV, doc. 331 read. See below.
- The commission, Mar. 16–17, 1968: Palermo, 138 and 296 nn.33–37 read. All held. The first entry's Check on whose clock is answered by "received by the LBJ Ranch CommCenter". Each wire is placed at Washington and the Ranch, and each wire now stands behind "To check:".
- Cẩm Khê, Dec. 1965: *Lịch sử kháng chiến chống Mỹ*, IV, 63–64 (page images) read. The page puts the attack on Cẩm Khê market on the morning of Dec. 18 ("sáng ngày 18"), not on the first entry's day. So the Dec. 18 entry now holds the market battle from the morning to its end at 3 p.m., and Lê Hữu Trữ's words with it. The first entry holds Regiment 1's attacks and the blocking of the withdrawal.
- Harvest Moon, Dec. 8–9, 1965: Shulimson, 103–05 read online. All three acts now have their hours (above).
- Mao on the train, Sept. 16, 1967: the Mao nianpu read. The talk is at noon (中午), after the morning's arrival at Hangzhou. A midday range is set.
- Junction City, Mar. 1967: MACV 1967, 388 and Cosmas, 33–34 read. Phase II "180001H March" is set.
- The Tet truce, Feb. 8–9, 1967: MACV 1967, 494 read. The reader's cease-fire entry duplicated `cal.1967-02-08.vietnam-2`, already in the tree (MACV's chronology, 1258, has 7 a.m.). It is struck and its ledger claim released. That entry instead gets MACV's 0800 as a variant on the hour and a Check. The *Stoddard* entry now says where (off Hòn Mát Island) and who fired (North Vietnamese shore batteries).
- Tet in IV Corps, 1968: MACV 1968, 397 read. Vĩnh Long held, and "approximately 0230" is set.

## The entries the reader did not split

- `cal.1965-09-19.china-leadership`: held to R25b and R17, it is one act, Mao's revision at 4:30 a.m. The hand-over is the Foreign Ministry's, and its hour is now on that entry.
- `cal.1966-01-31.vietnam`: split here. Gibbons, IV, 140, 155–58, 163–64 was read, with the APP pages of both replies. The first entry keeps the resumption and the 10 a.m. broadcast, and the event's bibliography. These are now entries of their own: the House members' letter (Jan. 21), Johnson's reply (Jan. 22), the Senators' letter (Jan. 27, in the afternoon by Harriman's account), Johnson's reply read by Moyers at 4:15 p.m. (Jan. 28), the request to the Security Council (Jan. 31), and the Council's vote to inscribe the item (Feb. 2, with a Check on the day). The Zaroulis variant (76 members) became a Check on the House letter. Hồ's letter and the NSC were already entries. The NSC entry (`cal.1966-01-29.vietnam-pause-3`) now has FRUS IV, doc. 55 as its record, Rusk's "no runs, no hits, no errors", its time of 1:20 p.m. from the Daily Diary, and a Check on Gibbons's Jan. 30.
- `cal.1968-12-11.transition-and-staff` and `cal.1968-12-12.transition-and-staff`: they did overlap. The tree's Dec. 12 entry held both the evening and, by Nixon's account, the Oval Office talk. The talk is now one entry: the Diary's 5:35 to 7:25 p.m., Nixon's account of it, and Nixon leaving at 7:42. Johnson's call to Nixon in New York at 9:36 p.m. and Rostow's briefing notes at 3:15 p.m., both from doc. 331, are entries of their own. The Dec. 12 entry keeps the evening (the families, the Cabinets, the staffs) and follows the talk. Its note keeps the Nixon cite, pointing to the talk's entry, because an edit may not drop a work read. The Dec. 11 entry is now Dec. 11 only.

## Pages read

- Owner's copies, fetched from Drive and deleted after:
  - Branch: *Parting the Waters*, 426–29; *Pillar of Fire*, 366–67; *At Canaan's Edge*, 29, 40–42, 50, 105–08, 140, 145.
  - Jones, 105. Salinger, 61–62. Dittmer, 247. Ball, 352–55. White, *1964*, 372–73. Solberg, 379–80, 403–04. Chester, 646–48. Humphrey, 401–02. White, *1968*, 395. Palermo, 138, 296. *Rights in Conflict*, 135, 138, 183–85, 189–90.
  - Chinese: the Mao nianpu (epub), June 29 and Nov. 16, 1960, Sept. 19, 1965, Sept. 16, 1967. Zhou's chronology, II, 370 (1997) and III, 210–211 and 335 (2020). Yang Shangkun's diary, I, 609 and II, 335–336. Wu Lengxi, 594–595. These were read as page images.
  - Vietnamese and MACV: *Lịch sử kháng chiến chống Mỹ*, IV, 63–64 (page images). MACV 1967, 388 and 494. MACV 1968, 397. Gibbons, IV, 140, 155–58, 163–64.
- Online:
  - On archive.org: Poole, 141–42; Cosmas, 33–34; Shulimson, 98–105.
  - The American Presidency Project's pages for Apr. 28 and Sept. 22, 1965; July 9 and 10, 1963; the Weizmann dinner; Boston, Pittsburgh and Evansville, Oct. 27, 1964; Faneuil Hall, Nov. 7, 1960; and the two replies of Jan. 22 and 28, 1966.
  - The FSM leaflet.
- FRUS (the series' text files): XV, docs. 234, 236; XVI, doc. 64; XXV, docs. 222, 223; XXVI, doc. 233; XXXII, docs. 28, 29, 32, 34–36; VII, docs. 153, 156, 158; VI, docs. 156–158; XIV, doc. 331; IV, doc. 55.

## Not read, and why

- The Wengao, XV, 260–261 and XVIII, 151–152 were not reopened. The reader read them on the page images, and the hours now rest on the Mao nianpu.
- MACV 1965, 164–65, the *Victory in Vietnam* volume, Drea, Kotz, Bernstein, Mann, Zaroulis, the Deng nianpu and the *Mao Zedong zhuan* were not reopened. They are cited for the parts that earlier readers' notes gave them.
- The marines.mil copy of Shulimson refused this host (Access Denied). archive.org's copy (TheLandingAndTheBuildup) was read instead.
- The leaflet dates more events (Oct. 4–15, 1964) and MACV 1968, 397 reports other dated acts of the same days (Trà Vinh, Sóc Trăng, Bến Tre, Châu Đốc, Cao Lãnh). They were not entered here: they are items still to read, not leads.
