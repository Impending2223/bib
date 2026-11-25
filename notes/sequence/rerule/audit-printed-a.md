# Audit of the re-ruling of the printed order, months 1960-01 and 1960-03 to 1960-11 (owner-rulings 56)

The patch audited is `inbox/2026-11-25-rerule-printed-a.yaml`, written by a Sonnet reader, with its note `notes/sequence/rerule/printed-a.md`. The rule is R25c as the owner rewrote it on Nov. 25, 2026: the order in which a chronology or a volume prints a day's items is the weakest of presumptions, and a link that rests on it alone says "the printed order alone" in its note, with the page. I read the reader's brief whole first. I disregarded nothing under R0: the brief set no limit. The patch is corrected in place and `./bib patch-check` shows 0 errors and 0 warnings.

## What I read

- The reader's note and patch, and the sequence notes of the ten months (`notes/sequence/1960-01.md` to `1960-11.md`, the reader's and the auditor's for each), with the merged patches of September, October and November.
- The day sheet of Jan. 6 to Nov. 30, 1960 (`day_order.py --full`), and every entry the patch names, in full (`./bib show`).
- The page images of the Drive copies: the Zhou Enlai waijiao huodong dashiji, 269–72 and 288; the Zhou Enlai nianpu, II, 283–84, 286, 295–96 and 298–99; the Chen Yi nianpu, 800–02, 807–09 and 835; the Zhu De nianpu, III, 1767–68; the Chen Yun nianpu, III, 30 and 33; the Deng Xiaoping nianpu, III, 1573–74. On each page the printed folio matched the offset in the work's book-check file.
- *Freedom of Communications*, Part 1, through its text layer (offset 17, checked on pp. 5, 84 and 600): the items of Aug. 1 to 23, Sept. 2 and 7, Oct. 7, 14 and 25, the contents for October (p. VIII), and the text of every item in the chains of September to November listed below.
- Two records online: the American Presidency Project's text of the second debate (Oct. 7, 1960) and of the Owosso remarks (Oct. 14, 1960).
- Every copy was fetched into a scratch directory of my own and deleted after reading. Nothing on Drive was changed.

Every volume read is in the order of time on the days read, where it gives hours or parts of the day.

## The reader's links: 25 checked

- Kept as written: 22. Jan. 18 (two), Jan. 20, 24, 26, 27 and 31; Mar. 11, 12, 13 and 21 (two); Apr. 3; Aug. 6 (two); Sept. 2; Sept. 20; Oct. 7; Oct. 14; Oct. 25 (two). On each the page shows the printed order the basis names and nothing I read goes against it. The Sept. 2 basis names the printed order and the Portland press conference's "your speech at Manchester this morning" (p. 90); it rests on more than the printed order, so it rightly does not say "alone".
- Kept, the basis rewritten: 2. Both are on Mar. 15, and both rest on more than the printed order, so the words "the printed order alone" came out. The cocktail party (`-5`) after Zhou's third talk with Koirala (`-4`): the dashiji puts the talk "下午" (271) and the Chen Yi nianpu puts the party "晚上" (807). The delegates of the five conferences (`-9`) after the Summer Palace and lunch (`-10`): the Chen Yi nianpu has the lunch ("共进午餐") and then the delegates "下午" (807).
- Pointed at the entry directly before: 1. Aug. 23, the Senate's votes (`medicare`) now follow the release on the VFW officials' wire (`elections-1960-kennedy-2`), not the telegram. The volume prints the telegram, then the release on the wire, then the floor statement (39–40), and the release is already linked after the telegram.
- Struck: 0. Turned round: 0.

The reader wrote no link on the days where the audits showed the volume out of order (Sept. 9, 13 and 22; Oct. 3, 12 and 22; Nov. 5; Aug. 26 and 30). I agree: on those days the printed order carries no presumption (owner-rulings 56, reading 3). The reader also wrote none on Sept. 6 and none between the East Lansing and Lansing stops of Oct. 14. I agree with both: the Sept. 6 statement sits among releases printed at the day's end, and the note of p. 590 does not order the two Lansing stops against each other.

## Links added: 2

- Oct. 7: Howard University (`elections-1960-kennedy-3`) after the second debate (`elections-1960`). At Howard Kennedy says, "I said tonight when we offered 300 scholarships to the Congo, we offered only 200 to Africa" (p. 519). He said it in the debate: "We gave more scholarships to the Congo ... than we've given to all of Africa the year before"; "Less than two hundred for all the countries of Africa" (the debate's text, APP). So Howard came after the debate. The link to American University on the printed order stays; nothing orders American University against the debate.
- Mar. 27: Chen Yun's letter to Zhou Enlai (`-10`) after his return from Shanghai to Peking (`-9`). The Chen Yun nianpu, III, 33, prints the return and then, "△", the letter. Nothing goes against it. The March notes had left the pair without a link and without naming the source's order.

I also looked at the other March pairs the notes left open. Mar. 28: the Zhou nianpu (II, 298–99) prints the State Council's 98th plenary and not the Secretariat, so there is no printed order between them. Mar. 8 and Mar. 10 rest on different volumes or on a day in dispute, not on one volume's order.

## Links already in the tree on the printed order alone: 140 links, 138 ops

The audits of September, October and November kept most of the Kennedy chains "on the printed order and the route alone", but no entry's note said so. For each such link the patch now has `follows: {id, add: [the earlier], basis: 'the printed order alone ([[w.card]], pages)'}`. The link stays as it is; the op writes the sentence into the note (addops.py, STYLE 11).

I took a link as resting on the printed order alone unless the words of the two items order that pair: a stop named as past or next, or a part of the day that puts one before the other ("this morning" against "tonight", a breakfast against an evening rally). A route that fits the order without forcing it was not counted as a basis. The links written, by day:

- September (51 ops): Sept. 2 (2), 5 (5), 7 (4), 12 (3, and the Deng nianpu link, `china-leadership-6` after `-2`, III, 1573–74), 14 (3), 15 (5), 16 (5), 17 (5), 19 (2), 21 (4), 25 (1), 27 (6), 28 (5).
- October (83 ops, 85 links): Oct. 2 (5), 3 (10), 4 (2), 5 (6), 6 (1), 8 (2), 9 (4), 14 (6 ops, 8 links: Jackson after Ann Arbor, Grand Rapids after Kalamazoo, the three stops of the note at p. 590 after Grand Rapids, and Saginaw after the three), 15 (6), 16 (1, the crowd outside the Silver Spring school), 17 (6), 18 (4; Jacksonville after Tampa rests on the contents, p. VIII, as Jacksonville is printed out of place at p. 970), 22 (1, the Park Plaza breakfast after Jennings), 23 (3), 24 (5), 26 (4), 28 (5), 29 (7), 31 (5).
- November (4 ops): Nov. 3, the Oklahoma City auditorium after the shopping center; Nov. 5, the Concourse Plaza after Fordham Road, and Flushing after Nassau County; Nov. 6, Teterboro after Newark. These are the four the November audit named; its other links rest on the texts or on O'Donnell's lists of the stops (248–49).

Left without the words, because something more than the printed order shows the order:

- The links whose two items' words order them: Sept. 2, the stadium after the press conference; Sept. 5, the airport at the day's end; Sept. 12, the plaza after the breakfast, and the Coliseum after the Alamo; Sept. 14, New York after St. Louis "this morning"; Sept. 15, Paramus at 10 after Jersey City at 8, and Harrisburg "tonight" after Trenton; Sept. 19, Charleston after the Steelworkers "this afternoon"; Sept. 21, Sioux City after "today in the Tennessee Valley"; Sept. 27, Hellriegel's Inn after Lausche's arrival; Sept. 28, the Erie rally after the breakfast, and Buffalo after "earlier this evening ... in Rochester"; Oct. 3, Springfield after the Marion airport; Oct. 31, Reyburn Plaza in the evening after the Bonds for Israel luncheon.
- Sept. 8: the train ran south from Dunsmuir at six in the morning to Oakland at night, and the stops lie in that order on the line.
- Oct. 14: Albion, Marshall and Battle Creek are printed out of place (962–66), so the links from Jackson through them to Kalamazoo rest on the rail line, not on the printed order.
- The days the audits kept on the texts' own words (Sept. 3, 4, 6, 10, 11, 23 and 29; Oct. 1, 10, 19, 20, 25, 27 and 30; Nov. 1, 2, 4 and 7) I did not reread link by link.

## What is left

- The days the audits kept on the texts' words may hold single links that rest on the printed order alone. A pass over them, link by link, would find any.
- Several chains above rest on the printed order with a route that fits it. If the owner rules that a route which fits counts as a basis, those links keep the words wrongly and can be found by them.
- The reader's own list stands: the October and November statements, letters and telegrams that are not stops (Oct. 2, 9, 12, 20, 28 and 31; Nov. 6) were never placed in the chains; they could be linked by the same rule.
- Jan. 8 and Apr. 7 (the Presidium's items under an agenda typed beforehand) stay unlinked under ruling 55's fifth default, which ruling 56 left as it was.
- Sept. 12: the dashiji (288) puts Deng at Mao's audience and banquet for Touré. The link of the Standing Committee after the audience rests on the Deng nianpu's printed order alone and is now marked so.
- Aug. 23: the telegram to the VFW says the Senate "is going to vote Tuesday", which reads as written before the day. If its date moves, its link to the release on the wire goes.
- Fields the sources give and the entries lack: Oct. 7, Howard University, "tonight" and after the debate; the debate itself has no time field. Mar. 15 `-10`, the lunch, has no midday range, so it sorts last on the day.

## Ready to merge

Yes. `./bib patch-check` shows 0 errors and 0 warnings. The patch now holds 164 ops: 26 that write a link (the reader's 24, of which one is pointed elsewhere and two have a new basis, and the 2 added) and 138 that write the basis of a link already in the tree.
