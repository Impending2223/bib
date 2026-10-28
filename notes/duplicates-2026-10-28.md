# Duplicates among the calendar entries of Oct. 23–28, 2026

Stage 2 of the second reading pass (approved by the owner, Oct. 28, 2026). The patch: `inbox/2026-10-28-duplicates.yaml`.

## Method

- Population: the 782 dated calendar entries the `add` ops of `inbox/merged/2026-10-23-*` to `2026-10-28-*` put in
  the calendar (784 adds; two were thread entries), each against every dated calendar entry (6,108 entries).
- Candidates: every pair within three days of each other (a ranged entry by its last day, a month-only entry by its
  whole month): 13,122 pairs. Left out: the 76 pairs on the same date and thread, which the merges flagged as
  duplicates and Claude read then.
- Each pair scored on four things: the documents both notes cite (a FRUS document, a recording, a Public Papers page,
  a statute, a case, an opinion, another link; the Daily Diary and a Record day weighted low, as many entries share
  them); a quotation or a run of five words both `c` share; the tf-idf cosine of the distinctive words of `c`; and the
  persons both tag (`name:`), weighted by rarity, a President's tag at a sixth of the weight. Score = 2 x cosine +
  names + quotation + documents - 0.1 x days apart. The script: the scratch directory's `dups/scan.py` and `rank.py`.
- Read, every pair: score 0.6 or more; word cosine 0.12 or more; one day apart or less with two or more named persons
  in common (Presidents aside); the same day with cosine 0.06 or more; one day apart or less with cosine 0.07 or more
  or names 0.3 or more; any shared document. 509 pairs in all. The duplicates found scored from 3.8 down to 0.36; the
  last 200 pairs read, below that, held none, so the rest (some 12,600 pairs, near nothing in common) were not read.

## Counts

- SAME: 3. PART: 4. ASK: 4 pairs, one question. DISTINCT: 498.

## SAME (one event written twice; combined, the dropped id an alias)

- `cal.1968-08-19.testing` keeps `cal.1968-08-19.soviet-union`: Dobrynin's handwritten note to Rusk, Moscow
  "positive" on a visit (FRUS 1964–68, XIV, doc. 286), from the thread's run and from *Vantage Point*; the cable to
  Johnson and the decision that night added to the kept entry, Rostow tagged.
- `cal.1961-09-17.vietnam` keeps `cal.1961-09-18.vietnam`: the Viet Cong take Phước Thành's capital. The record bears
  the night of Sept. 17–18 (Nolting's telegram 385, FRUS 1961–63, I, doc. 135: "Sept 17/18 VC attack"; doc. 138, "Sept
  17/18 setback"), so the entry of Sept. 17–18 is kept; Miller's "shortly after midnight" and Phước Vĩnh kept in `c`,
  the Check on the name kept.
- `cal.1967-11-20.elections-1968` keeps `cal.1967-11.elections-1968`: Westmoreland asked how the troops would take
  Johnson's not running. Westmoreland's notes (Gibbons, IV, 900) date it Nov. 20; Johnson's account (*Vantage Point*,
  429, 434) gives no day, and the month entry's "Check the day" becomes "Check: the day of Johnson's account".

## PART (one entry's event inside the other's: the larger trimmed, a See back)

- `cal.1966-03-15.vietnam-supplemental` held the House's vote on H.R. 13546, entered alone as `cal.1966-03-15.congress`:
  the vote cut from the signing entry, the $13 billion kept from the remarks (1966 Pub. Papers 321), a See to the vote.
- `cal.1961-01-03.rules` held the Senate Democrats' conference that let Johnson preside, entered alone as
  `cal.1961-01-03.congress`: cut from the opening of the 87th (and Johnson's tag with it); Caro, 164–69, moved to the
  conference's entry with the protest and the role never used, out of its To check.
- `cal.1967-10-23.vietnam-pennsylvania` held Phúc Yên's authorization, the meeting of `cal.1967-10-23.vietnam` (FRUS
  1964–68, V, doc. 363): the Pennsylvania entry keeps the leaders told (docs. 362, 364), loses `also: vietnam-air-war`;
  doc. 312 and "authorized Sept. 28 and cancelled" go to the meeting's entry; the See of `cal.1967-11-09.vietnam-air-war`
  follows.
- `cal.1963-11-25.assassination` held "Johnson receives the governors", entered alone as `cal.1963-11-25.succession`:
  the sentence and the Public Papers' remarks to the governors cut from the funeral, a See to them.

## ASK (one occasion, its matter entered under two threads)

The calendar already does this: 37 pairs of entries made before Oct. 23 rest on one Public Papers item on one day (a
news conference's several subjects), and 8 on one FRUS document (as Sept. 6, 1963, Robert Kennedy and Vietnam). So the
pairs below were left as they are, each entry with its own matter, and counted DISTINCT. But they are private
meetings, one event-day each, which the spans rule would make one entry with `also:`. The owner to rule whether a
meeting's matter for two threads is one entry or two:

- `cal.1967-10-03.vietnam` and `cal.1967-10-03.elections-1968`: the meeting of 6:10 p.m. (FRUS 1964–68, V, doc. 341);
  the Vietnam talk, and Johnson's question about not running.
- `cal.1968-05-14.vietnam` and `cal.1968-05-14.economy-surcharge`: the Tuesday lunch (FRUS 1964–68, VI, doc. 232); the
  bombing, and the tax bill.
- `cal.1967-05-19.vietnam-2` and `cal.1967-05-19.middle-east`: the meeting of 5:38 p.m. (FRUS 1964–68, XIX, doc. 22,
  gives the hour); the Hanoi power plant, and the tripartite approach.
- `cal.1963-12-03.civil-rights-bill` and `cal.1963-12-03.foreign-aid`: the leaders' breakfast, Meany there; the
  petition, and the tax cut and the cotton bill (they already point to each other).
