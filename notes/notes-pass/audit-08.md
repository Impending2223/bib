# Audit of batch 08: the notes pass

Audited Nov. 26, 2026 (Opus). The two patches are `inbox/2026-11-26-notes-pass-08.yaml` (29 entries) and `inbox/2026-11-26-notes-pass-08b.yaml` (the other 31), both corrected in place. `./bib patch-check` on each: 0 errors. The warnings left are the merge's duplicate flags on the new entries this audit added (each a distinct act of a day that already has entries in its thread: the merger keeps them with `./bib resolve ID --take keep`). Nothing merged, built or committed. The originals were kept in the audit's scratch directory until the end and then deleted with it.

## How the pages were read

Every work the two patches cite was fetched from the owner's Drive by its download address into a scratch directory of this audit, and deleted at the end. The English books were read by their text layers, page by page, the printed folio checked on each page used. The Chinese chronologies (Zhou Enlai, Deng Xiaoping, Ye Jianying, Chen Yi, Chen Yun, Zhu De) and Pu Weihua were read as page images, every cited page. Yang Jisheng was read by its text layer, and the three pages in question were read as images. The *Mao Zedong zhuan* was read in the EPUB. *77 Conversations* was read in the Wilson Center's PDF. FRUS was read at history.state.gov (IV, docs. 268, 269; V, doc. 287; XIV, docs. 228, 229, 231, 232, 235). Drea was read in archive.org's text of the DTIC scan, not as images.

Offsets found on the pages used: MacFarquhar, *Mao's Last Revolution*, printed = PDF − 17 to p. 110 and PDF − 33 from p. 155 (p. 155 opens a chapter and prints no number; it follows p. 154). Shesol, printed = PDF − 18 at p. 296 and PDF − 34 at pp. 365–433. Teiwes, printed = PDF − 16 at pp. 53, 67 and 86–88. Califano, printed = PDF − 20 at pp. 135–205 and in the source notes. Gibbons, IV, printed = PDF − 14. Westmoreland, printed = PDF − 32. Palermo, printed = PDF − 19. Brezhnev, II (the Drive file "Брежнев рабочие и дневниковые записи"), printed = PDF + 3. Yang, I, printed = PDF − 4; II, printed = PDF + 578. Zhou nianpu, III, printed = PDF − 4. Deng, printed = PDF + 1328. Ye, II, printed = PDF + 553. Chen Yi, printed = PDF − 13. Chen Yun, III, printed = PDF − 5. Zhu De, printed = PDF − 6. Pu, printed = PDF − 20. Jian, printed = PDF − 20. *77 Conversations*, printed = PDF + 2.

## The Yang Jisheng pins

The first reader thought three Yang pins a page late (240, 348, 425 for 241, 349, 426). They are not. Yang's book prints its page number at the foot of the page, with no running head. In the text layer the footer of one page comes just before the text of the next, and the reader took it for that page's head. The page images settle it: the 1,500 students and Mao's swollen hand are on I, 241 (PDF 245, footer "241"); Mao's meeting of Jan. 8, 1967, with Tang Pingzhu and Hu Chi, is on I, 349 (PDF 353); Lin Biao's seven articles are on I, 426 (PDF 430). The pins stand as the note had them.

## The second reader's open points

- "It's not my State Department": Johnson says it, in reply to Kennedy's "your State Department." Shesol, 366, Dallek, 447, and Thomas, 332–33, agree. The words are now in the line of `cal.1967-02-06.robert-kennedy` as Johnson's.
- Kennedy and Johnson on June 3, 1967: Kennedy spoke after Johnson. Palermo's note says so outright (64 n.26: he gave his "introduction" only after Johnson had spoken, having come from a funeral in England), and Shesol, 397, has him arrive too late to introduce Johnson. The line now says so, from Palermo's note.
- Pu, 122: read as an image. The page has Ye convey Lin Biao's view to the Air Force committee's plenum after the Military Commission meeting of July 11, with no day; the Ye chronology (II, 944) dates Ye's speech to the plenum Sept. 7. The page does not name Wu Faxian or Yu Lijin: the members Ye criticizes are those "who wrote letters of complaint." The words were corrected to that.
- Jian, 578: read. Mao met Yao Dengshan at the gate, "an encounter not arranged by Zhou," and the photograph has Yao between Mao and Jiang Qing. The variant on the clause naming Zhou stands.

## The June 5, 1967 items (Califano, 204–05)

The second reader left Ginsburg's warning, Fortas's call and Johnson's order to Christian and Rusk as a lead, for want of a day. Under R15a and R50 they are entries, dated by their context. Califano places them after McCloskey's statement of June 5, and his source notes date them: ch. 12 n.2 cites his memoranda to Johnson of June 5, 11:05 a.m. and 5:25 p.m., and June 7; n.3 cites records of June 5. Four entries were added, each dated June 5 with "Check: the day": Ginsburg's warning (`-6`), Fortas's call to Califano (`-7`), Johnson's order to Christian and Rusk to back away from McCloskey's statement (`-8`, which follows McCloskey's entry), and Johnson's instruction to Califano to call Krim, Wasserman and Weisl (`-9`). The two June 5 entries keep their `ok:note-substance` tags.

## Ops checked

Every op of both patches was checked against its page: 29 `add-words` and their `names` in patch 08, and 63 `add-words`, one `variant` and their `names` in patch 08b.

## Ops changed, and why

- Aug. 18, 1966, the rally (`india-and-china-cultural-revolution`): MacFarquhar, 107–08, has a million "students and teachers," not "of the capital," and no "celebrating" words. Those come from the Zhou chronology, III, 48–49, which is now the cite for them; MacFarquhar is cited for the six hours alone.
- Aug. 18, 1966, `-12` (Mao's arrival in uniform): Chen Yi reviewing the march, Ye Jianying at the first reception, and Chen Yun's talk with Mao in the hall of the gate tower are acts of the rally, not of Mao's arrival at 5 a.m. They were moved to the rally's entry. Jian's pin is now 551, where Zhou's uniform is.
- Aug. 18, 1966, `-4`: "The order fails" now reads "Order breaks down" (Yang, I, 241).
- Aug. 30, 1966: the list's officials were "the heads of State, Party and democratic-party bodies." The *Mao Zedong zhuan* names the State's vice-chairman, the vice-chairmen of the People's Congress and the Consultative Conference, the vice-premiers, ministers and vice-ministers, and the heads of the democratic parties and of the Court and Procuratorate. There are no Party bodies on the list.
- Oct. 5, 1966: the Ye chronology (II, 946) says only that the rule having the schools' committees lead the movement after the work teams leave is cancelled. "Not in the army at large" is Teiwes's (67). The op was split between the two.
- Oct. 9, 1966: the pin is Yang, I, 299, where both the rebel leaders and Wang Li's words are.
- Dec. 7, 1966: the lunch of 1 to 3 p.m. is an act of its own and became an entry (below).
- Dec. 26, 1966: the toast is now "By MacFarquhar's account," since the note's Checks give Wang Li's other wording.
- Jan. 8, 1967: MacFarquhar's ministries remark is on 157 alone; 161 is another remark.
- Jan. 21, 1967: the words now say what the Nanjing telegram reported, and the cite is the *Mao Zedong zhuan*'s text, ch. 76, not its note. A Check gives Yang's rally of ten thousand (I, 431). The first reader had not found that page; it is there.
- Jan. 24, 1967: Yang (I, 426) dates the scene "late January" and has Lin summon the four men himself, which the entry already holds as a variant. The op now cites the Ye chronology (II, 956–957): Ye and Nie Rongzhen go to Lin at Maojiawan after Xu that evening, and Lin dictates a draft of nine articles. Yang Chengwu's tag goes.
- Feb. 16 and 19, 1967: the pins are Yang, I, 389 and 391. On Feb. 19 Mao's proposal of Chen Yi, Wang Ming and Zhang Guotao is sarcasm, said in anger with Chen Boda and Jiang Qing to be shot and Kang Sheng exiled. The words now say so.
- Mar. 13 and 17, 1967: the line's act is the talk. Its hour is now the field: 10 a.m. on Mar. 13 and 3 p.m. on Mar. 17. The 9 a.m. meeting and the 10 a.m. arrival at Vnukovo became entries of their own.
- Apr. 7, 1967: pins narrowed to 97 and 98. Apr. 11: Zhu Qiwen speaks on p. 104, so the pin is 102–104.
- May 1, 1967: the op cited the Ye chronology for Chen Yun too; Chen Yun's gala is now cited to the Chen Yun chronology, III, 162.
- June 3, 1967: the Kennedy quotation was Palermo's wording cited to Shesol. It now cites Palermo, 64–65.
- June 23, 1967: four items cited the wrong FRUS document. Doc. 228 gives the arrivals and the 1:50 lunch of June 25; the 11:30 to 1:30 private talk is doc. 229; the 3:44 to 4:35 talk is doc. 232, not 231. A Check gives the memorandum's own hours for June 25 (1:30 to 6:30, ending 6:20; the State Department's copy 3 to 6:30).
- July 21, 1967: the words now stand alone at the line's end. A Check gives MacFarquhar's flight at two in the morning, and Yang's boarding after 2 a.m., against the line's 11 a.m.
- July 26, 1967: "brought to Peking on July 24" was taken out, since it is another day's act.
- Aug. 1, 1967: "Nor has Jiang Qing read it beforehand."
- Aug. 9, 1967, the hearings: the Gibbons text is on IV, 743–44, not 744–45.
- Nov. 13, 1966: White, 50, gives the group's membership, not the meeting's ("almost twenty-five"); the words were reworded, and John Lodge and Sears tagged.
- Sept. 19, 1966: Kotz says the supporters "failed by ten votes to secure cloture"; reworded.

## Ops struck, and why

- Aug. 19, 1966: Siemiller's boast that the settlement "destroy[ed]" the guidelines is his later comment, not the ratification. It stays in the note, and his tag goes.
- Oct. 5, 1966: the accounts of who drafted the directive (Qiu Huizuo's, Wang Li's) are of an earlier act, the drafting, as later memoirs tell it. They stay in the note, and five tags go; the entry is tagged `ok:note-substance`.
- Nov. 4, 1966: Johnson's words to Califano before the news conference and after it are two acts of their own. They became entries (below).
- Dec. 14, 1966: Shesol, 296, names Christian only as Moyers's later successor. No act of Dec. 14 is on the page.
- Feb. 6, 1967: Kennedy's morning call to Watson, and Katzenbach's lunch with him, are acts of their own. They became entries (below).
- June 20, 1967: Zhou's call on the Arabs "to continue the war at any cost" and the Arabs' new readiness for Soviet help are Friedman's narrative on pp. 159–60. Only his notes tie them to Brezhnev's speech, and a note is not the record it cites (R35a). Zhou's tag goes.
- July 18, 1967: Zhou's departure at eleven is the act of `cal.1967-07-18.china-leadership-3`. MacFarquhar, 209 is cited there instead.

## Added from the cited pages (R33b)

- Aug. 13, 1966: Zhu De attends (Zhu De, III, 1956); Ye Jianying attends in the morning (Ye, II, 942), and the morning is set as the field.
- Aug. 31, 1966: Lin Biao's and Zhou's speeches (Zhou, III, 53); Ye, Zhu De, Chen Yun and Deng present, each from his own chronology.
- Sept. 2, 1966: Dallek's figures, $1.5 billion, $2 billion and the 7 percent credit (Dallek, 310, which the first reader did not find); O'Brien tagged.
- Sept. 15, 1966: the rally's four hours (MacFarquhar, 108); Zhou's speech (Zhou, III, 63); Chen Yi, Ye, Zhu De and Deng present.
- Sept. 19, 1966: not a vote changed, and Mansfield's words (Sundquist, 282); Hart pronounces the bill dead (Zelizer, 246). Neither had been read before.
- Oct. 1, 1966: Lin Biao's speech (*Mao Zedong zhuan*, VI, ch. 75); Chen Yi, Ye, Zhu De, Chen Yun and Deng present.
- Nov. 4, 1966: the question on the canceled trip and the answer (Califano, 152, which the first reader did not find).
- Nov. 25, 1966: Yang's figures for each day and the trampling at the dispersal (I, 242); Lin, Zhou and Chen Yi on the tower; Ye, Zhu De and Deng present.
- Jan. 13, 1967: Ye attends (Ye, II, 955).
- Jan. 31, 1967: the silent "vigil for peace" (Wells, 119, which had not been opened), and a Check for Wells's 2,400. Wells's "the same day" is Jan. 31, the day of Rusk's meeting with the student leaders.
- Mar. 20, 1967: Westmoreland's review and his request to put pacification under MACV (Westmoreland, 214, which had not been read).
- Apr. 11, 1967: a Check that *77 Conversations* (doc. 25, p. 102) dates Zhou's apology for the Red Guards and Mao's answer Apr. 10.
- July 15, 1967: Yang, I, 524 (which the first reader did not find): the July 17 afternoon report of the "ten great crimes" and "ten great merits," with Yu Lijin at Zhou's side.
- Aug. 18, 1967: who was present, and the hour, 8:45 to 9:50 p.m. by the Daily Diary (FRUS, V, doc. 287); a Check gives Tom Johnson's 8:35 to 9:55.

## New entries (13)

- `cal.1966-11-04.elections-1966-3`, `-4`: Johnson to Califano before the news conference, and at the wire tickers after it (Califano, 291), with `follows` both ways.
- `cal.1966-12-07.soviet-union-leadership-2`: the lunch in the Catherine Hall, 1 to 3 p.m. (Brezhnev, II, 161).
- `cal.1967-02-06.robert-kennedy-2`, `-3`: Kennedy's morning call to Watson, and Katzenbach's lunch with Kennedy and Watson's call setting the 4 p.m. meeting (Shesol, 365–66), with `follows`.
- `cal.1967-03-13.soviet-union-leadership-3`: Brezhnev meets Zhivkov at 9 a.m. (II, 177).
- `cal.1967-03-17.soviet-union-leadership-3`: Brezhnev meets Ceaușescu's delegation at Vnukovo II at 10 a.m. (II, 178).
- `cal.1967-03-20.vietnam-guam`, `-2`: Johnson's address to the airmen at Andersen, the conference's first business, and McNamara's and Westmoreland's agreement on Abrams as deputy (Westmoreland, 213–14).
- `cal.1967-06-05.middle-east-six-day-war-6` to `-9`: the four acts above.

## Fields set (R25a)

Times set: Dec. 7, 1966 (9:20 a.m. Moscow); Feb. 6, 1967 (4:34 p.m., Palermo, 42); Mar. 13 and 17, 1967; Aug. 18, 1967 (8:45 p.m.). The old "kind" range on Aug. 18 was taken out. Parts of the day set: Aug. 13, 1966 (morning); Nov. 13, 1966 (morning, White, 52, replacing a "kind" range); July 15, 1967 (afternoon). Each multi-day entry's note now says the time is the first day's. Place set: Sept. 2, 1966 (Washington, Califano's office). The new entries carry their own times and places.

## Not read, and why

- The Soviet embassy's report that Friedman cites (RGANI): an archive, not reachable from here.
- Pu, 206, for Aug. 18, 1966, `-4`: not opened. Yang, I, 241, read as an image, bears the same words, and Pu's parenthetical was left as it stood.
- Drea, 213, 215–16: read in archive.org's text of the DTIC scan, not as page images (the series' book-check file records the same copy). It bears the line as it stands.
- The Public Papers, for a text of Johnson's remarks at Andersen on Mar. 20, 1967: not searched. The new entry carries it as "To check."
- Thomas, 332: the text layer garbles the hour of the Feb. 6 meeting ("1 p.m."). The page image was not opened. The hour set is Palermo's, 4:34 p.m., from the Daily Diary, and Shesol's 4:00 is the appointment.
- The day-order pass (R25c, `tools/times/day_order.py`) was not run over every day the patches touch. `follows` links were written only where a page read gives the order: Nov. 4, 1966; Feb. 6, 1967; Mar. 20, 1967; June 5, 1967.

## Ready to merge

Yes. Both patches pass `patch-check` with 0 errors. At the merge, the duplicate flags on the 13 new entries are to be resolved with `--take keep`. Every one of them is a distinct act on a day that already has entries in the same thread.
