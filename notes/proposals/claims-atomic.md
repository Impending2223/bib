# Atomic claims: what we lack without them, and what they would take

For the owner, Nov. 25, 2026, in answer to: "Ask the Fable agent what we're missing by not having an atomic claims model and what it would take to get there." It follows `notes/proposals/claims-model-review-fable.md`, whose Q8 said the wish is met by no design on the table. The counts are from the calendar as it stands (58,276 entries with a line), by a throwaway script over the tools' own functions; where a count is rough, it says so. No code or data was changed.

## 1. The short answer

- An atomic claim is one assertion that a source can bear out or contradict by itself: who did what, when, where, the number, the words spoken, on whose word. The calendar's line is prose; a sentence of it holds two or three such assertions. By two entries taken apart by hand, the calendar holds between 300,000 and 400,000 of them.
- What we lack without them is mostly not on the page. The page would read the same. What is lacking is underneath: sources below the clause, variants that name the fact they dispute, a person's part in an event, whose report a statement is, an R22 that a tool can apply, and search by fact.
- Getting there has two halves that cost very differently. The claims' content (who, what, when, the number) can be drawn from the line itself by a model pass and checked in good part by rule. The claims' sources cannot: saying which source bears out which claim means reading the sources again, 123,000 cited pages. The first half is a few weeks' passes. The second is the reading programme over again, and should be done only as passes come, by the rule the owner gave on Nov. 24.
- The claims should be kept beside the prose, tied to it, not in its place. The prose is the calendar.
- 35f is a step toward it. Its parts are what claims would hang on, and nothing in it would be redone. Three small things in 35f should be decided now so the way stays open (section 7).
- Recommendation: do 35f; do not commit the calendar to atomic claims yet; run a trial on one month, which touches no page and no entry, costs about a million tokens, and would show whether the rest is worth doing (section 8).

## 2. The owner's words

- Oct. 23, 2026, on what a source stands for: "Z's C might be 'Charles bought the red hat at Dorothy's request,' while ABD might be collocated facts about 'Charles buying a red hat' that Z does not speak to (date, price, store, make)".
- Oct. 28: "Should we break the entries down into (invisible?) sentence-by-sentence, clause-by-clause units, and accord to each the appropriate (invisible?) pincite?"
- Oct. 30: "What I ultimately want from the 'records' is a trace/map of *all* the *ultimate*, or *root*, materials that bear on a fact or event."
- Nov. 13, on a report: "Strictly speaking, 'Alekseyev to Moscow: ' is Soviet-only, but 'Guevara says . . .' is Soviet-and-Cuban."
- Nov. 22: "in principle, atomic *claims* `c` should follow the strict R22, and new patches could join *new claims* `c` to an entry under a looser rule. the problem is that `c` actually means something like 'a sentence,' and may include far more than one atomic claim. is there any way to make the world look more like my fantastical world of atomic facts, or are we stuck with `c` sentences?"
- Nov. 24, 2:25 p.m.: "some way to clearly state alternative, irreconcilable accounts of times and follows".
- Nov. 24, 3:45 and 3:50 p.m.: "How can a sourced claim be only 'the date is open'?"; "What dates are open?" A claim has to say what it is about.
- Against it, and also the owner's, Nov. 24, 3:35 p.m.: claims with the same sources "should only happen on a second, 'complicating' pass". Cutting every entry into claims up front, each with the entry's sources copied onto it, is what that message objected to. Sections 6 and 7 keep to it: the content of the claims up front, their sources only when a pass complicates.

## 3. What an atomic claim would be here

- The test. A claim is atomic when a source could bear it out, or give a different reading of it, without touching anything else in the entry. "The letter is dated June 21" and "the letter is in seven parts" are two: a source can give the date and be silent on the parts. The test is about evidence, not grammar.
- The floor. There is no natural bottom ("Chen Yi attends" holds "Chen Yi was in Peking"). The house's own rule gives the floor: who, what, the number (CLAUDE.md), with the date, the hour, the place, the words quoted, and on whose word.
- The form. Each claim: an id; the part of the line it sits in; `says`, a short sentence that reads by itself, its subject restored (so "what dates are open?" cannot arise); and a few slots a tool can read: `who`, each person with his part (`actor`, `to`, `present`, `about`); `when`, `time`, `where`; `num`; `by`, the claim that reports it (a cable, a speaker, a delegation's word); `of`, the claim it qualifies. Sources, variants and visibility rulings may then name a claim.
- The calendar already has some. An entry's `date`, `time`, `place` and its `name:` tags are atomic facts in slots. 25,446 entries have a time field, 29,984 a place, and there are 113,125 name tags. None of them has a source of its own, and no name tag says what the person did.
- The established model is the factoid of prosopography (the databases built at King's College London: a factoid is one source's one assertion about a person, and conflicting factoids stand side by side), and, close to it, Wikidata's statement with its references and ranks. Both keep the assertions as the record. Here they would stand beside the prose.

## 4. Two entries, three ways

### `cal.1960-06-23.soviet-union`

Today (abridged with "…"; `n` and the other fields left out):

```yaml
c: Bucharest, morning. The Soviet delegation hands Peng Zhen's delegation the CPSU Central Committee's letter, dated June 21, in seven parts (the era; war and peace; … unity). The same text had gone to the other parties as a "notification" on June 21, before the Chinese had it, by the Vietnamese, Korean and Albanian delegations' word. A draft communique follows, for discussion on the 24th. The delegation cables the points.
src:
  rows:
    - 'w.lengxi-shinian-lunzhan-1956-1966 281–283, 285: all'
    - 'w.yang-jisheng-mubei II, 1150: B'
    - 'w.peng-zhen-nianpu-1902 IV, 37–38: ?'
tags: [polity:prc, name:peng-zhen, vis:only:prc+ussr, 'vis:only:prc+ussr+albania+…@C-D', 'vis:only:prc@E']
variants:
  - {unit: A, witness: w.peng-zhen-nianpu-1902, reads: 'the letter and the "Notification" handed to the delegation at its lodging by Andropov, … at 3 p.m. on June 23', at: 'IV, 37'}
```

As 35f would store it: the same, with cuts in the line and part numbers for the letters.

```yaml
c: Bucharest, morning.{1} The Soviet delegation hands … unity).{2} The same text had gone … word. A draft communique follows, for discussion on the 24th.{3} The delegation cables the points.{4}
src:
  rows:
    - 'w.lengxi-shinian-lunzhan-1956-1966 281–283, 285: 1, 2, 3, 4'
    - 'w.yang-jisheng-mubei II, 1150: 2'
    - 'w.peng-zhen-nianpu-1902 IV, 37–38: ?'
tags: [polity:prc, name:peng-zhen, vis:only:prc+ussr, 'vis:only:prc+ussr+albania+…@3', 'vis:only:prc@4']
variants:
  - {unit: 1, witness: w.peng-zhen-nianpu-1902, reads: …, at: 'IV, 37'}
```

As atomic claims, beside the same line and the same cuts (thirteen claims from five sentences):

```yaml
claims:
  - {id: a1, part: 1, says: 'The letter is handed over at Bucharest.', where: bucharest}
  - {id: a2, part: 1, says: 'It is handed over on the morning of June 23, 1960.', when: '1960-06-23', time: morning}
  - {id: a3, part: 2, says: 'The Soviet delegation hands Peng Zhen''s delegation a letter of the CPSU Central Committee.', who: ['actor:soviet-delegation', 'to:peng-zhen']}
  - {id: a4, part: 2, of: a3, says: 'The letter is dated June 21.', when: '1960-06-21'}
  - {id: a5, part: 2, of: a3, says: 'The letter is in seven parts.', num: 7}
  - {id: a6, part: 2, of: a5, says: 'The parts: the era; war and peace; peaceful coexistence; forms of transition; international mass organizations; China''s breaches of the Declarations; unity.'}
  - {id: a7, part: 3, by: a10, says: 'The same text had gone to the other parties as a "notification".'}
  - {id: a8, part: 3, of: a7, by: a10, says: 'It went to them on June 21.', when: '1960-06-21'}
  - {id: a9, part: 3, of: a7, by: a10, says: 'It went to them before the Chinese had it.'}
  - {id: a10, part: 3, says: 'The Vietnamese, Korean and Albanian delegations say so.'}
  - {id: a11, part: 3, says: 'A draft communique follows.'}
  - {id: a12, part: 3, of: a11, says: 'It is for discussion on June 24.', when: '1960-06-24'}
  - {id: a13, part: 4, says: 'The Chinese delegation cables the points.', who: ['actor:peng-zhen']}
src:
  rows:
    - 'w.lengxi-shinian-lunzhan-1956-1966 281–283, 285: 1, 2, 3, 4'
    - 'w.yang-jisheng-mubei II, 1150: a3, a4'
variants:
  - {claim: a2, slot: time, value: '15:00', witness: w.peng-zhen-nianpu-1902, at: 'IV, 37'}
  - {claim: a3, slot: who, value: 'actor:andropov', witness: w.peng-zhen-nianpu-1902, at: 'IV, 37'}
  - {claim: a1, reads: 'at the delegation''s lodging', witness: w.peng-zhen-nianpu-1902, at: 'IV, 37'}
```

What the third form shows that the first two cannot. Yang Jisheng's page, by its own parenthetical in the note, gives the handing-over and the date of June 21; it says nothing of seven parts. Under today's map and under 35f it stands for the whole of sentence B, the seven parts with it. The one variant, filed against "Bucharest, morning.", in fact disputes three things: the hour, who handed the letter over, and where. And the Peng Zhen nianpu, a `?` row today because no letter fits what it bears on, has its place: against three claims, as three readings.

### `cal.1960-02-10.cuba`

Today: "Alekseyev to Moscow: Guevara, at his home, a few days after Castro's dinner of Feb. 3, says Cuba will ask Mikoyan for an enormous credit, $500 million the opening bid (Castro and Alekseyev had spoken of $100 million in November); the Kremlin may announce it. "It is very important for Cuba to feel independent of the U.S. and to demonstrate it." Shown to Mikoyan." One source, on all of it. Tags: `name:guevara-ernesto`, `name:castro-fidel`, `name:mikoyan-anastas`, `vis:only:ussr+cuba`, `vis:frame:ussr`, `vis:only:ussr@D`.

As 35f would store it: one cut, for the ruling on the last sentence (`… demonstrate it."{1} Shown to Mikoyan.{2}`, the tag `vis:only:ussr@2`); the rest as it is.

As atomic claims:

```yaml
claims:
  - {id: b1, part: 1, says: 'Alekseyev reports to Moscow on Feb. 10, 1960.', who: ['actor:alekseyev-aleksandr-i']}
  - {id: b2, part: 1, by: b1, says: 'Guevara spoke with Alekseyev at Guevara''s home, a few days after Castro''s dinner of Feb. 3.', who: ['actor:guevara-ernesto', 'to:alekseyev-aleksandr-i']}
  - {id: b3, part: 1, by: b2, says: 'Cuba will ask Mikoyan for an enormous credit.', who: ['about:mikoyan-anastas']}
  - {id: b4, part: 1, of: b3, by: b2, says: 'The opening bid is $500 million.', num: 500000000}
  - {id: b5, part: 1, by: '?', says: 'Castro and Alekseyev had spoken of $100 million in November.', who: ['actor:castro-fidel', 'actor:alekseyev-aleksandr-i'], num: 100000000}
  - {id: b6, part: 1, by: b2, says: 'The Kremlin may announce it.'}
  - {id: b7, part: 1, by: b2, says: 'Guevara: "It is very important for Cuba to feel independent of the U.S. and to demonstrate it."'}
  - {id: b8, part: 2, says: 'The report was shown to Mikoyan.', who: ['to:mikoyan-anastas']}
```

What it shows. The chain of `by` is the owner's sentence of Nov. 13: b1 and b8 are the Soviet side's alone; b2 to b7 are what Guevara said, known to him and to the man he said it to. Visibility falls out of the chain; today it takes three hand rulings on this one entry. Alekseyev, whose report the entry is, has a name tag on seven other entries and none on this one; a claim with an actor cannot leave him out. And b5: is the $100 million of November in Alekseyev's cable, or is it the book's own aside? The prose does not say, and only the book can. The atomic form asks questions that the prose can leave open. That is its use, and its cost.

## 5. What we are missing without it

By what the calendar's parts do badly, or cannot do, under 35f. Each count says what was measured.

1. **The page.** Little. The line, the marks and the footnotes would be what they are. A footnote mark sits at the end of words; claims a4 and a5 share a clause, and no mark can sit between them. So sources finer than the clause either stay unseen (used by the audits and the tools) or come back as a parenthetical, compiled from the claim's `says`, not written by hand: "Yang Jisheng, *Mubei*, II, 1150 (the handing-over; the letter's date)". The owner doubted parentheticals at scale (Nov. 24, 3:55 p.m.); that doubt is the limit on what atoms can show.
2. **Footnotes.** Under 35f a source stands for a whole clause at least. Where a clause names several people and a source is one man's own chronicle or memoir, it is cited for all of them: 29,062 units name two or more tagged persons, 10,256 three or more, and in about 8,500 entries such a unit rests on a work whose card bears one of those persons' names (rough: matched on the card's id). The time and place fields have no source at all.
3. **Variants.** There are 1,326. By their own words, 282 give another hour, 448 another date, 209 another figure, and 387 differ in words only. So seven in ten dispute one slot of one fact, and are stored as a sentence filed against a sentence. Nothing can lay them side by side, set the entry's `time` against them, or order a day by them. The owner's "alternative, irreconcilable accounts of times and follows" (Nov. 24) is this. Besides the variants, 14,298 entries carry a "Check:", and 2,172 of those say that a source "gives" another reading: variants in prose.
4. **Visibility.** `vis.py` says of itself that "tags do not tell the actor from the object, so every tagged person's polity" counts. It finds whom a sentence addresses by looking for surnames in it, and knows a report's frame only on an entry's first sentence, on the 20 entries tagged `vis:frame`. Against that: 30,407 entries have two or more name tags; about 38,800 units are reported speech (rough: a verb of saying, or a head and a colon); 16,923 entries open on a head and a colon. And 19,098 entries, a third of the calendar, carry a `vis:only` ruling, set by hand or by a pass, each an override of the computed answer. With actors, addressees and the chain of `by`, most of those rulings should be computed. How many is what a trial would measure.
5. **R22.** Under 35f a tool can tell an addition (words only added) from a change (words altered). It cannot tell a rewording from a correction; the reader must declare which. With claims it can: draw the claims again from the new words; the same claims, a rewording; a new claim, an addition; a slot's value changed, a correction, which needs its settling record. That is the owner's Nov. 22 sentence, as a check.
6. **The Names pages.** A person's Life lists every entry that tags him. Of the 113,125 name tags, none says whether he acted, was spoken to, was present, or was spoken of; about 10,700 are on entries whose line does not name him at all (the tag stands for his act, as the brief asks for a President). With parts, a Life could be sorted or filtered into what he did, what was said to him, and what was said of him; and "who met whom" becomes a list.
7. **The Threads pages.** Nothing directly.
8. **Search.** `./bib find` matches words. It cannot answer "every talk between Rusk and Dobrynin", "everything Guevara is reported to have said, and by whom", or "every figure given for the credit". 34,583 units hold a figure or a date inside the sentence and 28,357 hold quoted words; none can be asked for as such.
9. **The audits.** An auditor sets a page against a paragraph and writes a row in his own words. With claims he gives a verdict on each: bears it out, silent, gives another reading. The 19,941 `?` rows are sources whose part no letter could name; a claim can name it. And R37's count of independent witnesses "for each unit" would be for each fact, which is what the owner asked on Oct. 30.
10. **The readers.** A reader adding to an entry would see what it already asserts as a list, and add what is new. "One event or two?" could be tested by who, what and when, not by words in common.

## 6. What it would take

1. **The data model.** Section 3's claim, kept beside the line and tied to a part of it. The line stays the record that the page prints; the claims are an index over it. Stored apart from `lists/cal` (as the witnesses are, in files by year, keyed by entry), because 300,000 to 400,000 claims at about 150 characters each would otherwise double the calendar's 56 MB.
2. **Not prose from claims.** Generating the line from the claims would put the house's prose ("Compact. Plain. Compressed.") in a program's hands and would change every line of the calendar. Not recommended, and not needed for anything in section 5.
3. **Who writes the content.** A model pass over each entry's line, its fields and its tags; no source is needed to see that a sentence says the letter is dated June 21. By the owner's rule of Nov. 24, Sonnet writes and Opus audits. Readers go on writing prose; the claims of a new or changed entry are drawn at the merge and audited with the patch. The reader's brief gains no schema.
4. **How it is checked.** By rule: every claim names a part that exists; every name, number, date and quoted word in a claim stands in that part's words or the entry's fields (the guard against a claim the line does not make); every name, figure and quotation of a part appears in some claim (the guard against a fact left out); every `name:` tag is someone's part in some claim; `by` and `of` point inside the entry and do not loop. By two passes: the same entry cut twice and compared, since a cut that comes out differently each time is no basis for R22. By audit: what no rule sees, namely whether the cut is right, the parts are right, and `by` is right.
5. **Who writes the sources.** Nobody, in bulk. A claim takes its part's sources until a pass with the source in hand says otherwise; then a row names claims. This is the owner's "complicating pass" one level down. Doing it for the whole calendar at once would mean re-reading every cited page: 123,129 rows.
6. **The migration.** A month at a time: the pass, the checks, the audit, the claims written to the side files. No entry in `lists/cal` changes. By the two entries of section 4 (13 claims in 81 words; 8 in 64), about one claim to seven words; the calendar's lines hold 2.25 million words.
7. **The cost.** The lines and notes are 33 million characters, about 10 million tokens to read once. The first pass reads that and writes perhaps 6 to 8 million; the audit reads both and writes its corrections; the second cut for comparison reads and writes again. Of the order of 40 to 60 million tokens for the content of the whole calendar, three-fifths of it audit. I have not priced it, and the figure rests on two entries.
8. **The tools.** A loader and the checks above (`claims.py`, `check.py`); `vis.py` to compute from parts and `by` in place of surnames found in a sentence, the hand rulings kept where they still differ; `lives.py` to sort a Life by part; `find` to query slots; `witnesses.py` to take a variant against a claim and a slot, and the stemma by claim; `patchcheck.py` and `merge.py` to draw the claims of an edited part again and classify the edit; `footnotes.py`, if wanted, to compile the parenthetical of section 5, 1.
9. **The briefs.** R22 restated on claims; R34 and R41 (the map, the variants) by claim; the auditors' brief gains the verdict by claim. Nothing in R5, R15a, R18 or R50 changes: what is an entry is untouched.
10. **The risks.** (i) No bottom: the floor of section 3 will be argued entry by entry, and a model will cut one entry two ways. (ii) Two records to keep in step, the line and its claims; the checks narrow this and do not close it. (iii) False precision: a claim looks exact where the prose was careful to be vague, and a guessed `by` or a guessed part is worse than none. (iv) Visibility hides text: a wrong part in a claim could hide a sentence from the page. (v) The slots grow: every new kind of fact wants one, and that is the spaghetti the owner named. (vi) The queue: readers have already waited once on a model. (vii) Three or four hundred thousand claims is three or four hundred thousand things to vouch for.

## 7. 35f: toward it or away

Toward it.

- Carried over unchanged: the line as one string; the cuts and the parts' ids, which are what a claim's `part` names; the rows' form, where a claim's id can stand beside a part's; a part named in a patch by its words; R22 from the diff, which the claims sharpen; the footnote compile; the conversion and its proof.
- Redone: nothing stored. Replaced in time: the splitter's sentences inside a part, which 35f keeps for visibility, give way to claims; the surnames-in-a-sentence rule gives way to parts.
- To decide in 35f now, so the way stays open: (1) Ids of two kinds that cannot be confused (a part `3`, a claim `a3`), so that a row, a ruling or a variant can later name either with no change of grammar. (2) Let a row and a variant name a field the entry already has (`date`, `time`, `place`) as well as a part. The fields are the atomic facts the calendar already keeps, and 730 of the 1,326 variants are about an hour or a date. This is small, it is useful without any claims model, and it is the first atom. (3) Do not write into 35f that a cut may exist only where a source, a ruling or a variant needs one; say that nothing else needs one yet. The compile folds any cut that no source distinguishes, so a later layer can add cuts without changing a page.

## 8. Recommendation, and the smallest trial

1. Do 35f, with the three points above. It is the base of either road.
2. Do not commit the calendar to atomic claims now. What is known is that the benefit lies under the page, that the content is cheap and the sources are not, and that the cost and the reliability rest on two entries taken apart by hand.
3. Run a trial that changes nothing. It writes claims to a side file; no entry, page or patch is touched, so it need not wait for 35f and holds up no reader.
   - The content: February 1960, every thread. 360 entries, 968 units, 14,562 words; 165 of the entries carry a hand visibility ruling, 69 a "Check:". Two Sonnet passes, cut independently; the checks of section 6, 4; an Opus audit of all of it. About 2,200 claims expected.
   - The sources: the Cuba thread, January to March 1960, 53 entries, 20 of them citing Fursenko and Naftali, whose EPUB with linked notes the owner put on the drive on Nov. 22. One reader with the book says which claims each cited page bears out.
   - The cost: about a million tokens in all, by the same arithmetic as section 6, 7; an evening's run.
   - What it would show, each a number: claims per entry and per word, so the 300,000 to 400,000 is measured; how often the two passes cut alike, which says whether R22 by claim is possible; how many claims the audit strikes or mends; how many of the 165 hand visibility rulings the claims reproduce without a ruling; how many `?` rows and Checks find a claim to sit on; in the Cuba thread, how many sources turn out to bear on less than their clause, which is the whole gain over 35f in the footnotes; and, for the owner's eye, one Life (Guevara's, or Mikoyan's) laid out by part, and the questions like b5 that the pass could not answer from the line.
   - What would settle it. For going on: the two passes agree on nine claims in ten, the audit mends fewer than one in twenty, and the claims reproduce most of the hand rulings. Against: the cuts do not agree, or the gain shows only in the sources, where the cost is a second reading of everything. These thresholds are mine, to be changed.
4. Whatever the trial shows, take section 7's second point now: sources and variants that can name the date, the hour and the place.

## 9. How the counts were made

Over `claims.calendar()` with `claims.units`, `claims.resolve`, `vis.unit_ties` (a name tag counted as named in a unit when its key's first or last part stands in the text) and `vis.frame_text`. Variants sorted by a pattern on their `reads`: a clock time or a word for the time of day; else a month and day; else any digit; else words. Reported speech by a list of verbs of saying or a short head and a colon: rough, and likely high. "One man's own chronicle or memoir" by the first two parts of a name tag's key standing in a cited card's id: rough, and likely low for Western names, high for none. Tokens taken as characters over 3.5; not run through a tokenizer.
