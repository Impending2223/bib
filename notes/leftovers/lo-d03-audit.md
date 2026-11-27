# Leftovers, batch lo-d03 (July and August 1960): the audit

Audit of `inbox/2026-11-27-lo-d03.yaml` and `notes/leftovers/lo-d03.md`, Nov. 27, 2026, under R0, R33b and the reader's brief. The patch now holds 110 ops: 57 adds (19 the reader's, 38 the audit's), 41 edits, 12 additive ops. `./bib patch-check`: 0 errors. Every edit's base was refreshed against the tree at the end and none had moved. A trial merge in a scratch copy of the tree, with the duplicate flags kept, gave `./bib check` 0 errors and no warning of this patch's but the election-result form on the nomination tally (tagged `ok:result-form`) and two polity warnings on names already in the tree. Nothing was merged, built or committed here.

## What was read

- The *New York Times* of July 5 and July 6, 1960: the owner's 81 screenshots fetched from the Drive, found by an OCR pass and read as images (Lawrence, "Johnson Backers Urge Health Test"; Fellows, "Cyprus to Shun Military Blocs"; "Betancourt Scores Trujillo on Attack"; the transcript of Kennedy's news conference; the Nepal item; Johnston on the Zengakuren; Sitton and Egan on Butler).
- FRUS 1958–60, VI, doc. 549; XIV, doc. 163; XVI, docs. 361, 363, 366; FRUS 1964–68, XXIII, docs. 12 and 14 (the series' own texts); the Public Papers, 1960–61, items 227, 245, 268 (the series' own texts).
- S. Rep. No. 94-465, pp. 15–16 and 72–73 (page images checked: PDF 26 is p. 15, PDF 84 is p. 73).
- Hammarskjöld's second report, U.N. Doc. S/4417 (Aug. 6, 1960), whole, from documents.un.org.
- *Ross v. Dyer*, 312 F.2d 191, pp. 191–93 (case.law).
- Books, each fetched from the Drive and deleted after: Fursenko and Naftali, *Khrushchev's Cold War*, 310–15, 326–29; Ball, 226–28; Guan, 155–58; Bissell, 142–44; the Zhou Enlai nianpu, II, 329, 338, 342 (images); the Waijiao dashiji, II (2001), 150 (image); Yang Shangkun's diary, I, 538 (image); the Liu Shaoqi chronology (1996), II, 492–93 (images); O'Donnell and Powers, 213–29; Caro, *Passage of Power*, 103–45; Salinger, 40–45; White, *Making of the President 1960*, 159–62, 205–07; O'Brien, 85–88; *Freedom of Communications*, pt. 1, 18–64; Nixon, *RN*, 213–22; Nixon, *Six Crises*, 316–18, 339 (images); Schlesinger, *Journals*, 74–86; Perlstein, 93–95; Young, *Two Suns*, 26–27; White, *Suite 3505*, 21–24; Goldberg, 145–46; Gifford, 135–36, 155–57; Kabaservice, 27–30; Novak, 23; APP's page for the 1960 Republican platform.

## Ops checked and held

The reader's hours and bands hold against their pages, each recomputed with zoneinfo: the Lawrence, Conway and Clifford hours of July 14, the bands of July 13, Aug. 2, 5, 20, 21, 23, 24 and 26, the noon of Aug. 8 (Zhou nianpu, 338), the 6:55 p.m. of Aug. 14 (doc. 361), 12:25 p.m. of Aug. 20 (FoC, 24), the early morning of July 21 (S. Rep., 73). The splits of July 4 (Cyprus, Betancourt, the *Life* advertisement), July 9 (Cuba; Lawrence), July 14 (R25b), July 21, July 26, Aug. 1, 3, 8, 13, 20, 24 and 25 each separate acts of their own record (R17, R25b). The two July 4 day settlements hold: Lawrence's story is datelined July 4 and says "proposed today." The Mani pass sentence holds on the Waijiao dashiji, 150; the nianpu (329) bears only the first sentence, so its map row now names unit 1. Johnston's story bears the Zengakuren split. The Aug. 24 sitting: Yang's diary (538) shows one parties' symposium that afternoon, Zhou reporting, and the Liu chronology (492) has Liu presiding Aug. 24 and 26, so the reader's reading of the pair holds; the two entries stay, one Zhou's report, the other Liu's chairing over two days with his speech of the 26th.

## Ops changed

- The new Cyprus entry reused `cal.1960-07-04.cyprus-3`, an id deleted Nov. 24 (the Denktash fragment, R18a); it is now `cal.1960-07-04.cyprus-4`, the ledger claim moved, and it adds Makarios's four ambassadors.
- `cal.1960-07-10.elections-1960-los-angeles-5`: Beverly Hills, not Los Angeles (White, 161).
- `-24` of July 14 now cites the pages that bear its words (O'Donnell, 220–22; Caro, 130–34). `-26`: "the Sports Arena" is not in its sources (Caro has "the coliseum"), so "the convention"; it now cites O'Donnell, 223, and O'Brien, 85–86, and follows Conway's 7:30 call.
- `-15` and `-16` of July 14: the pages of "at eight o'clock" and "About a half hour after" are 215 and 216, not 214 and 215; `-16` takes a Check, since "He's seeing him now" would put the scene at ten.
- `-19` of July 14 split under R25b: the pact keeps the id, its range now 4:30 to 7 p.m. (the authors' "seven that evening when the floor fight was called off," 222); O'Donnell's 4:30 call to Conway and Conway's 7:30 call are new entries (`-27`, `-28`), with follows.
- `cal.1960-07-15.elections-1960-los-angeles-2`: the night band struck. O'Donnell gives a sequence, "After listening to the speech" (224), not a part of the day; the entry already follows the speech.
- July 27: the withdrawal's words corrected to the reading of Perlstein (95), White (24), Gifford from the Proceedings (136) and Kabaservice (29), "Let's grow up, conservatives. If we want to take this Party back, and I think we can someday, let's get to work"; the release of the delegates added; the Goldberg and Young readings moved from the July 26 entry to `-2` as Checks, Young's page corrected to 27. `-3` takes White's hour, 11:13 p.m. (206), Hatfield's nomination and Arizona's motion, Six Crises at 316–17; the platform entry takes "Check: the day," since Novak (23) gives none and APP dates the platform July 25. Follows added: `-2` after the Youth for Goldwater meeting, `-3` after `-2` (Perlstein, 93), `cal.1960-07-27.goldwater` after `-2`, the late-night leaders' meeting after `-3`.
- `cal.1960-08-02.congo` settled by the record: Hammarskjöld's own report (S/4417, 2–3) and FRUS XIV, doc. 163 n.1 date his statement Aug. 2, at Léopoldville, to the Congolese Cabinet Committee, with Bunche to go Aug. 5 and the troops Aug. 6. Ball's Aug. 3 and Aug. 8 (228) stay as a Check.
- `cal.1960-08-08.china-zhou-foreign`: the nianpu's words as printed (汇报同胡志明谈话情况).
- Laos: Guan (157) does not treat the censure; it reports on Aug. 15 the resignation and the appointment. It is cited on `cal.1960-08-14.laos` (which also takes the day's negotiations from doc. 361) and `cal.1960-08-15.laos`, and keeps a "not the censure" parenthetical on Aug. 13 (patch-check will not let an edit drop a work read). Doc. 363 reports Radio Vientiane's claim, not the King's act, so it left `cal.1960-08-15.laos` for the synopsis's own entry.
- `cal.1960-08-20.elections-1960-kennedy`: Jackson and Symington at the press conference (FoC, 24–28), named and tagged. `cal.1960-08.elections-1960-10` (SAC): the first night's band, "last night" (FoC, 34), and Jackson and Symington with him; its days sentence moved ahead of "Names:".
- `cal.1960-08-26.congo-lumumba`: Bissell cited for his own account (143–44), his later reading of the cable put in a gloss (R19b).
- `cal.1960-08-30.elections-1960-kennedy-3`: the dinner's band now rests on the record, "last night," cocktails, dinner (*Journals*, 84), not on the kind.
- `cal.1960-08-24.china-leadership`: the nianpu (342) names the Association for Promoting Democracy, not the Democratic Construction Association (`kind: correct`); the Hebei Hall and the hundred present moved from the parenthetical into the line.
- Connally's proposal of secret-ballot caucuses (Lawrence, July 5), left by the reader, is part of the same press conference and went into `cal.1960-07-04.elections-1960-2` by `add-words`.
- Also: the Zengakuren split follows the raid (Johnston); the Aug. 15 synopsis follows the appointment it reports; Fursenko (314) cited on `cal.1960-09.cuba` for the August approach to the Mafia.

## Ops struck

None of the reader's ops was struck whole. Struck words and fields: "the Sports Arena" (`-26`); the night band on July 15; the `range_basis: kind` on Aug. 30; doc. 363 as a cite for the King's act.

## Entries added by the audit (38)

Every dated event of the records and pages read that the calendar lacked (R0, R5): from FRUS VI, 549, Herter's calls on the statement's text, Khrushchev's sugar offer to Castro, the Havana rally of July 10, Bonsal's telegram of July 11; from the Church report, 72–73, the Havana station's cable of July 20, the Cuban's agreement by July 22, his return; from White's *Suite 3505*, the South Carolina caucus of July 27; from *Six Crises*, 318, Nixon's call to Lodge at 2:30 a.m. July 28; from S/4417 and FRUS XIV, 163, Wigny's statement, Tshombe's message and Hammarskjöld's reply, the escort and the journalist refused, Bunche's departure, the Elisabethville airport, the 11 a.m. warning, Bunche's report and Hammarskjöld's second report, and the Herter–Scheyven talk of Aug. 5; from FRUS XVI, 361, 363 and 366, Ouane's mission of Aug. 13, John Eisenhower's synopsis, Sarit's irritation, Phoumi's refusal and his request for 10 million kip, Brown's telegram 294 at 8 p.m. and the Department's telegram 176; from Fursenko, 328, Kong Le's provisional government; from *Ross v. Dyer*, 193, the Houston board's rules of Aug. 15, the Fifth Circuit's affirmance of Sept. 6 and the admissions of September; from Schlesinger's *Journals*, 83–84, the Marshall weekend, Cox's talk on Sorensen, Sorensen's words to the Cox group, Cox's call of Aug. 30 and Graham's call of Aug. 31.

## For the merger

Every duplicate flag this patch raises is a distinct act: run `./bib resolve ID --take keep` on each. A trial merge raised 41, on the new entries of July 4, 9, 10, 14, 22, 27 and 28 and Aug. 2, 3, 4, 5, 6, 8, 13, 15 that share a day and thread with others. The ledger holds the audit's claims under the patch's name; `cal.1960-07-04.cyprus-3` and `cal.1960-07-04.elections-1960-los-angeles-10` were released.

## The questions the brief named

- Schlesinger's *Journals* for Aug. 30: read (84–85). The dinner is Graham's report of Aug. 31, "last night"; the entry's line holds, and its hour now rests on the record.
- The July 27 works: all read but Kallina, 93: the Drive file `1gOKSo-mP-2XQZ2FU9W9kw5IGd1JVOOAR` is not shared by link (the download returns Google's sign-in page), so its cite stands as the earlier reader gave it. Guan, 157: read.
- The Butler pair of July 5: not settled. Sitton has Butler at "a news conference" on unity and the Southerners; Egan has him "talking with reporters after his appearance before the committee" on the convention's officials. Neither story gives an hour or says they are one occasion; the Check on `-7` stays.
- Dulles's cable: not settled. FRUS heads the telegram Aug. 27; the Church report (15) and Fursenko (315) give Aug. 26. The entry stays Aug. 26 with the Check.
- Hammarskjöld's moves: settled by S/4417, Aug. 2 and Aug. 6, against Ball.

## What still waits, and on what

- Kallina, 93, on the shared Drive (above).
- The records the new entries name behind "To check:" (the Herter Papers, the Havana and Vientiane telegrams, the Department's telegram 176, *Houston Independent School District v. Ross*, 282 F.2d 95): not read; no witness rows were written for them.
- The day of Bunche's return: S/4417 says "Friday afternoon, 6 August," and Aug. 6, 1960, was a Saturday; the entry carries a Check.
- What R0 disregarded: nothing in the brief narrowed the work. The reader's note left Connally's secret-ballot proposal and Guan, 157, for a later pass; both were done here.
