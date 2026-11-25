# Atomic claims: what we lack without them, and what they would take

For the owner, Nov. 25, 2026. It answers: "Ask the Fable agent what we're missing by not having an atomic claims model and what it would take to get there." Sections 10 and 11 answer the owner's two later questions, on a shorter form for the claims and on compiling prose from them.

Sections 1 to 9 were first written on Nov. 25 and are here put into plainer prose. No finding or number in them is changed. The counts are of the calendar as it stood then: 58,276 entries with a line. They were made by a script, since discarded, that used the tools' own functions. A rough count is marked rough. No code or data was changed.

Terms, used the same way throughout.

- The **line** is an entry's `c`.
- A **unit** is a sentence of the line, or a clause that ends in a semicolon.
- A **part** is the words between two cuts in the line (ruling 35f). An entry with no cut has one part.
- A **claim** is one statement that a source can support or contradict without touching any other statement in the entry.
- A **field** is a named value: the entry's `date`, `time` and `place`, or a named value inside a claim.

## 1. The short answer

- A claim says one thing: who did what, when, where, the number, the words spoken, or on whose word. A sentence of the line holds two or three claims. I took two entries apart by hand. By their measure the calendar holds between 300,000 and 400,000 claims.
- Without claims the page loses almost nothing. The page would read the same. The data loses six things: a source for less than a clause; a variant that names the fact it disputes; a person's role in an event; whose report a statement is; an R22 that a tool can apply; and search by fact.
- The work has two halves, and their costs differ greatly. The content of the claims (who, what, when, the number) can be taken from the line by a model pass and checked largely by rule. The sources of the claims cannot. To say which source supports which claim, someone must read the sources again: 123,000 cited pages. The first half is a few weeks of passes. The second half repeats the whole reading programme. It should be done only as passes come, by the owner's rule of Nov. 24.
- The claims should be stored beside the prose and tied to it. They should not replace it.
- Ruling 35f is a step toward claims. A claim would be tied to a part, and nothing in 35f would be redone. Three small things in 35f should be decided now (section 7).
- Recommendation: do 35f. Do not commit the calendar to claims yet. Run a trial on one month. The trial changes no page and no entry and costs about a million tokens. It would show whether the rest is worth doing (section 8).

## 2. The owner's words

- Oct. 23, 2026, on what a source stands for: "Z's C might be 'Charles bought the red hat at Dorothy's request,' while ABD might be collocated facts about 'Charles buying a red hat' that Z does not speak to (date, price, store, make)".
- Oct. 28: "Should we break the entries down into (invisible?) sentence-by-sentence, clause-by-clause units, and accord to each the appropriate (invisible?) pincite?"
- Oct. 30: "What I ultimately want from the 'records' is a trace/map of *all* the *ultimate*, or *root*, materials that bear on a fact or event."
- Nov. 13, on a report: "Strictly speaking, 'Alekseyev to Moscow: ' is Soviet-only, but 'Guevara says . . .' is Soviet-and-Cuban."
- Nov. 22: "in principle, atomic *claims* `c` should follow the strict R22, and new patches could join *new claims* `c` to an entry under a looser rule. the problem is that `c` actually means something like 'a sentence,' and may include far more than one atomic claim. is there any way to make the world look more like my fantastical world of atomic facts, or are we stuck with `c` sentences?"
- Nov. 24, 2:25 p.m.: "some way to clearly state alternative, irreconcilable accounts of times and follows".
- Nov. 24, 3:45 and 3:50 p.m.: "How can a sourced claim be only 'the date is open'?"; "What dates are open?" A claim must say what it is about.
- Also the owner's, Nov. 24, 3:35 p.m., and against cutting everything at the start: claims with the same sources "should only happen on a second, 'complicating' pass". If every entry is cut into claims and each claim is given the entry's sources, that message's objection applies. Sections 6 and 7 follow it. The content of the claims is written at the start. Their sources are written only when a pass finds a difference.

## 3. What a claim would be here

- The test. A statement is one claim when a source can support it, or give a different reading of it, and say nothing about the rest of the entry. "The letter is dated June 21" and "the letter is in seven parts" are two claims. A source can give the date and be silent on the parts. The test is about evidence. It is not about grammar.
- The smallest size. Claims can always be cut smaller ("Chen Yi attends" holds "Chen Yi was in Peking"). The house's rule for the line sets the size: who, what, the number (CLAUDE.md). To these add the date, the hour, the place, the words quoted, and on whose word.
- The form used in sections 4 to 9. Each claim has an id. It names the part of the line it is in. It has `says`: a short sentence that can be read alone, with its subject written out, so that "what dates are open?" cannot be asked of it. It has a few fields a tool can read: `who`, each person with a role (`actor`, `to`, `present`, `about`); `when`, `time`, `where`; `num`; `by`, the claim that reports it (a cable, a speaker, a delegation's word); `of`, the claim it adds to. A source, a variant or a visibility ruling may then name a claim. Section 10 gives a shorter form.
- The calendar has some claims already. An entry's `date`, `time` and `place` and its `name:` tags are single facts in fields. 25,446 entries have a time field. 29,984 have a place. There are 113,125 name tags. No field has a source of its own. No name tag says what the person did.
- The established model is the factoid of prosopography. The databases built at King's College London use it: a factoid is one statement by one source about a person, and two factoids that disagree are both kept. Wikidata's statement is close to it: a statement, its references, and a rank. Both keep the statements as the record. Here the statements would be kept beside the prose.

## 4. Two entries, three ways

### `cal.1960-06-23.soviet-union`

Today (shortened with "…"; `n` and the other fields left out):

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

As 35f would store it. The same, with cuts in the line and part numbers where the letters were:

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

As claims, beside the same line and the same cuts. Five sentences give thirteen claims:

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
  - {claim: a2, field: time, value: '15:00', witness: w.peng-zhen-nianpu-1902, at: 'IV, 37'}
  - {claim: a3, field: who, value: 'actor:andropov', witness: w.peng-zhen-nianpu-1902, at: 'IV, 37'}
  - {claim: a1, reads: 'at the delegation''s lodging', witness: w.peng-zhen-nianpu-1902, at: 'IV, 37'}
```

The third form shows three things that the first two cannot.

- Yang Jisheng's page gives the handing-over and the date of June 21. Its parenthetical in the note says so. It says nothing of seven parts. Under today's map and under 35f it is cited for the whole of sentence B, the seven parts included.
- The one variant is filed against "Bucharest, morning." It disputes three things: the hour, who handed the letter over, and where.
- The Peng Zhen nianpu is a `?` row today, because no letter names what it supports. As claims it has its place: against three claims, as three readings.

### `cal.1960-02-10.cuba`

Today: "Alekseyev to Moscow: Guevara, at his home, a few days after Castro's dinner of Feb. 3, says Cuba will ask Mikoyan for an enormous credit, $500 million the opening bid (Castro and Alekseyev had spoken of $100 million in November); the Kremlin may announce it. "It is very important for Cuba to feel independent of the U.S. and to demonstrate it." Shown to Mikoyan." One source supports all of it. Tags: `name:guevara-ernesto`, `name:castro-fidel`, `name:mikoyan-anastas`, `vis:only:ussr+cuba`, `vis:frame:ussr`, `vis:only:ussr@D`.

As 35f would store it: cuts for the ruling on the last sentence (`… demonstrate it."{1} Shown to Mikoyan.{2}`, and the tag `vis:only:ussr@2`). The rest is unchanged.

As claims:

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

What it shows.

- The `by` fields state the owner's sentence of Nov. 13. Claims b1 and b8 are known to the Soviet side alone. Claims b2 to b7 are what Guevara said. He knew them, and so did the man he said them to. A tool can compute the visibility from `by`. Today this one entry takes three rulings set by hand.
- The entry is Alekseyev's report. He has a name tag on seven other entries and none on this one. A claim that must name its actor cannot omit him.
- Claim b5: is the $100 million of November in Alekseyev's cable, or is it the book's own remark? The prose does not say. Only the book can. Claims make the writer answer questions that prose can leave unanswered. That is what they are for, and it is also their cost.

## 5. What we lack without claims

Each item says what was counted.

1. **The page.** Almost nothing. The line, the marks and the footnotes would be the same. A footnote mark stands at the end of some words. Claims a4 and a5 are in one clause, and no mark can stand between them. So a source for less than a clause has two possible treatments. It is not shown, and only the tools and the audits use it. Or it is shown by a parenthetical that a tool compiles from the claim: "Yang Jisheng, *Mubei*, II, 1150 (the handing-over; the letter's date)". The owner doubted parentheticals at scale (Nov. 24, 3:55 p.m.). That doubt limits what claims can show on the page.
2. **Footnotes.** Under 35f a source is cited for a whole clause at the least. Some clauses name several people, and some sources are one man's own chronicle or memoir. Such a source is then cited for all the people in the clause. 29,062 units name two or more tagged persons. 10,256 units name three or more. In about 8,500 entries such a unit is cited to a work whose card has one of those persons' names in its id (rough). The time and place fields have no source at all.
3. **Variants.** There are 1,326. By their own words, 282 give another hour, 448 another date, 209 another figure, and 387 differ in words only. So seven variants in ten dispute one field of one fact. Each is stored as a sentence filed against a sentence. No tool can set two of them side by side, compare them with the entry's `time`, or order a day by them. This is the owner's "alternative, irreconcilable accounts of times and follows" (Nov. 24). Besides the variants, 14,298 entries have a "Check:" in the note. 2,172 of those say that a source "gives" another reading. Those are variants written as prose.
4. **Visibility.** `vis.py` says that "tags do not tell the actor from the object, so every tagged person's polity" counts. It finds whom a sentence is addressed to by searching the sentence for surnames. It knows whose report a statement is only for an entry's first sentence, and only on the 20 entries tagged `vis:frame`. Against that: 30,407 entries have two or more name tags. About 38,800 units are reported speech (rough: a verb of saying, or a short heading and a colon). 16,923 entries open with a short heading and a colon. And 19,098 entries, a third of the calendar, have a `vis:only` ruling, set by hand or by a pass, each one overriding the computed answer. With roles and `by`, a tool should compute most of those rulings. A trial would count how many.
5. **R22.** Under 35f a tool can tell an addition (words only added) from a change (words altered). It cannot tell a rewording from a correction. The reader must say which. With claims a tool can tell. It takes the claims again from the new words. The same claims: a rewording. A new claim: an addition. A field's value changed: a correction, which needs its settling record. That is the owner's sentence of Nov. 22, made into a check.
6. **The Names pages.** A person's Life lists every entry that tags him. No name tag among the 113,125 says whether he acted, was spoken to, was present, or was spoken of. About 10,700 tags are on entries whose line does not name him at all (the tag is for his act, as the brief asks for a President). With roles, a Life could be sorted into what he did, what was said to him, and what was said of him. "Who met whom" could be listed.
7. **The Threads pages.** No direct change.
8. **Search.** `./bib find` matches words. It cannot answer "every talk between Rusk and Dobrynin", or "everything Guevara is reported to have said, and by whom", or "every figure given for the credit". 34,583 units hold a figure or a date inside the sentence. 28,357 units hold quoted words. A search cannot ask for either as such.
9. **The audits.** An auditor compares a page with a paragraph and writes a row in his own words. With claims he gives one of three answers for each claim: the page supports it, is silent, or gives another reading. The 19,941 `?` rows are sources that no letter could place. A claim can place them. R37 counts independent witnesses "for each unit". With claims it would count them for each fact. The owner asked for that on Oct. 30.
10. **The readers.** A reader adding to an entry would see a list of what the entry already states, and would add what is new. "One event or two?" could be tested by who, what and when. Today it is tested by shared words.

## 6. What it would take

1. **The data.** The claim of section 3 (or the shorter form of section 10), stored beside the line and tied to a part of it. The page prints the line. The claims index it. They should be stored outside `lists/cal`, in files by year keyed by entry, as the witnesses are. 300,000 to 400,000 claims at about 150 characters each would otherwise double the calendar's 56 MB.
2. **Not prose made from claims.** Section 11 takes this up. In short: a program would then write the house's prose, and every line of the calendar would change. Nothing in section 5 needs it.
3. **Who writes the content.** A model pass reads each entry's line, fields and tags. It needs no source to see that a sentence says the letter is dated June 21. By the owner's rule of Nov. 24, Sonnet writes and Opus audits. Readers go on writing prose. The claims of a new or changed entry are written at the merge and audited with the patch. The reader's brief gets no new format to learn.
4. **How it is checked.** By rule: every claim names a part that exists. Every name, number, date and quoted word in a claim is in that part's words or in the entry's fields; this catches a claim that the line does not make. Every name, figure and quotation of a part is in some claim; this catches a fact left out. Every `name:` tag is someone's role in some claim. `by` and `of` point to claims of the same entry and make no loop. By two passes: the same entry is taken apart twice and the results are compared. If the two results differ often, R22 cannot be based on claims. By audit: for what no rule can test, namely whether the division into claims is right, the roles are right, and `by` is right.
5. **Who writes the sources.** Nobody, for the whole calendar at once. A claim has its part's sources until a pass with the source in hand says otherwise. Then a row names claims. This is the owner's "complicating pass", applied to claims. To do it for the whole calendar at once would mean reading every cited page again: 123,129 rows.
6. **The migration.** A month at a time: the pass, the checks, the audit, then the claims written to their own files. No entry in `lists/cal` changes. The two entries of section 4 give 13 claims in 81 words and 8 claims in 64 words: about one claim to seven words. The calendar's lines hold 2.25 million words.
7. **The cost.** The lines and notes are 33 million characters, about 10 million tokens to read once. The first pass reads that and writes perhaps 6 to 8 million tokens. The audit reads both and writes its corrections. The second pass, for comparison, reads and writes again. In all, 40 to 60 million tokens for the content of the whole calendar, three-fifths of it the audit. I have not priced it. The figure rests on two entries.
8. **The tools.** A loader and the checks above (`claims.py`, `check.py`). `vis.py` computes from roles and `by`, where it now searches a sentence for surnames; the rulings set by hand are kept wherever the computed answer still differs. `lives.py` sorts a Life by role. `find` searches fields. `witnesses.py` takes a variant against a claim and a field, and draws the tree for a claim. `patchcheck.py` and `merge.py` take the claims of an edited part again and classify the edit. `footnotes.py`, if wanted, compiles the parenthetical of section 5, 1.
9. **The briefs.** R22 is restated for claims. R34 and R41 (the map, the variants) are by claim. The auditors' brief gains the three answers for each claim. R5, R15a, R18 and R50 do not change: what counts as an entry is the same.
10. **The risks.** (i) There is no smallest claim. The size set in section 3 will be disputed entry by entry, and a model will divide one entry two ways. (ii) There are two records to keep in agreement, the line and its claims. The checks reduce the disagreement. They do not end it. (iii) A claim looks exact where the prose was deliberately vague. A guessed `by` or a guessed role is worse than none. (iv) Visibility hides text. A wrong role in a claim could hide a sentence on the page. (v) The fields multiply. Each new kind of fact needs one. The owner's word for that was "spaghetti". (vi) The queue. Readers have already waited once for a data model. (vii) 300,000 to 400,000 claims are 300,000 to 400,000 statements that someone must check.

## 7. Is 35f a step toward claims, or away?

Toward.

- Kept unchanged: the line as one string. The cuts and the part numbers; a claim's `part` names one. The form of the rows; a claim's id can stand in a row where a part number stands. A patch that names a part by its words. R22 from the difference between two lines; claims make it more exact. The footnote compile. The conversion and its proofs.
- Redone: nothing that is stored. Replaced later: 35f keeps the units for visibility, and claims would take their place there. Roles would take the place of the search for surnames in a sentence.
- To decide in 35f now, so that claims can be added later without redoing it. (1) Two kinds of id that cannot be confused: a part is `3`, a claim is `a3`. A row, a ruling or a variant can then name either, with no change of grammar. (2) Let a row and a variant name a field that the entry already has (`date`, `time`, `place`), as well as a part. The calendar already stores these single facts. 730 of the 1,326 variants are about an hour or a date. This change is small. It is useful with or without claims. (3) Do not write into 35f that a cut may exist only where a source, a ruling or a variant needs one. Write that nothing else needs one yet. The footnote compile joins the parts on either side of a cut when their sources are the same, so a later change can add cuts and change no page.

## 8. Recommendation, and the smallest trial

1. Do 35f, with the three points above. Claims need it, and so does a calendar without claims.
2. Do not commit the calendar to claims now. Three things are known. The benefit is in the data and not on the page. The content is cheap and the sources are not. The cost and the reliability have been measured on two entries only.
3. Run a trial that changes nothing. It writes claims to a file of its own. It changes no entry, page or patch. So it need not wait for 35f, and it delays no reader.
   - The content: February 1960, every thread. 360 entries, 968 units, 14,562 words. 165 of the entries have a visibility ruling set by hand. 69 have a "Check:". Two Sonnet passes divide each entry independently. The checks of section 6, 4 are run. Opus audits all of it. About 2,200 claims are expected.
   - The sources: the Cuba thread, January to March 1960. 53 entries, 20 of them citing Fursenko and Naftali. The owner put that book's EPUB, with linked notes, on the drive on Nov. 22. One reader with the book says which claims each cited page supports.
   - The cost: about a million tokens in all, by the arithmetic of section 6, 7. One evening's run.
   - What it would show, each as a number. Claims per entry and per word, which tests the estimate of 300,000 to 400,000. How often the two passes divide an entry alike, which shows whether R22 by claim is possible. How many claims the audit removes or corrects. How many of the 165 hand rulings the claims reproduce with no ruling. How many `?` rows and Checks can be attached to a claim. In the Cuba thread, how many sources support less than their clause; in the footnotes, that is all that claims add to 35f. And for the owner to read: one Life (Guevara's, or Mikoyan's) sorted by role, and the questions like b5 that the pass could not answer from the line.
   - What would decide it. For going on: the two passes agree on nine claims in ten; the audit corrects fewer than one claim in twenty; the claims reproduce most of the hand rulings. Against: the two passes do not agree, or the only gain is in the sources, where the cost is a second reading of everything. These thresholds are mine. The owner may change them.
4. Whatever the trial shows, do section 7's second point now: sources and variants that can name the date, the hour and the place.

## 9. How the counts were made

Over `claims.calendar()`, with `claims.units`, `claims.resolve`, `vis.unit_ties` and `vis.frame_text`. A name tag counts as named in a unit when the first or last part of its key is in the text. Variants were sorted by a pattern on their `reads`: a clock time or a word for the time of day; else a month and day; else any digit; else words. Reported speech was counted by a list of verbs of saying, or a short heading and a colon: rough, and probably high. "One man's own chronicle or memoir" was counted when the first two parts of a name tag's key are in a cited card's id: rough, probably low for Western names. Tokens were taken as characters divided by 3.5. No tokenizer was run.

## 10. A shorter form for the claims

The owner, Nov. 25: "your backend renders atomic claims in plain-language sentences. Is there a way to render them that preserves precision and consistency in a less verbose form?"

Yes. Store each claim as a short typed record. Do not store a sentence. When a person needs to read a claim, a tool prints a sentence from the record by a fixed pattern.

### The forms considered

**Form 0. The plain sentence** (section 4). Each claim has `says`, a full sentence, and a few fields.

**Form 1. A fixed set of fields, free words in them.** Every claim has the same fields: subject `s`, verb `v`, object `o`, and `to`, `when`, `where`, `by`, `of` where they apply. The writer chooses the words.

```yaml
# cal.1960-06-23.soviet-union
- {id: a1, of: a3, where: Bucharest}
- {id: a2, of: a3, when: 1960-06-23 morning}
- {id: a3, s: Soviet delegation, v: hands, o: CPSU Central Committee's letter, to: Peng Zhen's delegation}
- {id: a4, s: the letter, v: dated, o: June 21}
- {id: a5, s: the letter, v: in, o: seven parts}
- {id: a6, s: the parts, v: are, o: 'the era; war and peace; … unity'}
- {id: a7, s: the same text, v: had gone, to: the other parties, o: 'as a "notification"', by: a10}
- {id: a8, of: a7, when: June 21, by: a10}
- {id: a9, of: a7, v: before, o: the Chinese had it, by: a10}
- {id: a10, s: 'the Vietnamese, Korean and Albanian delegations', v: say, o: [a7, a8, a9]}
- {id: a11, s: a draft communique, v: follows}
- {id: a12, of: a11, v: for, o: discussion on the 24th}
- {id: a13, s: the delegation, v: cables, o: the points}
# cal.1960-02-10.cuba
- {id: b1, s: Alekseyev, v: reports, to: Moscow}
- {id: b2, s: Guevara, v: says, to: Alekseyev, where: his home, when: a few days after Castro's dinner of Feb. 3, o: [b3, b4, b6, b7], by: b1}
- {id: b3, s: Cuba, v: will ask, to: Mikoyan, o: an enormous credit}
- {id: b4, of: b3, s: the opening bid, v: is, o: $500 million}
- {id: b5, s: Castro and Alekseyev, v: had spoken of, o: $100 million, when: November, by: '?'}
- {id: b6, s: the Kremlin, v: may announce, o: it}
- {id: b7, s: Guevara, v: says, o: '"It is very important for Cuba to feel independent of the U.S. and to demonstrate it."'}
- {id: b8, v: shown, to: Mikoyan, o: the report}
```

**Form 2. A typed record.** Each claim has a kind from a short list. Each kind has its own fields. Values come from lists the calendar already keeps: a person by his name key, a place by its key, a date in the form of the entry's `date`. A verb comes from a fixed list of acts. A thing that several claims speak of (the letter) is named once and given a short label. Exact words from the line, where the wording matters, go in `words`.

The kinds used below: `act` (someone does something), `say` (someone states other claims), `quote` (words spoken), `is` (a thing has a property), `count`, `list`, `place`, `time`, `order` (one act before another).

```yaml
# cal.1960-06-23.soviet-union
things: {L: 'letter of the CPSU Central Committee', D: 'draft communique'}
claims:
  - {a1: place, of: a3, v: bucharest}
  - {a2: time, of: a3, v: 1960-06-23, band: morning}
  - {a3: act, verb: hand, who: 'Soviet delegation', to: 'Peng Zhen''s delegation', what: L}
  - {a4: is, of: L, what: dated, v: 1960-06-21}
  - {a5: count, of: L, what: parts, v: 7}
  - {a6: list, of: a5, words: 'the era; war and peace; … unity'}
  - {a7: act, verb: send, to: 'the other parties', what: L, words: 'as a "notification"', by: a10}
  - {a8: time, of: a7, v: 1960-06-21, by: a10}
  - {a9: order, of: a7, before: a3, by: a10}
  - {a10: say, who: ['Vietnamese delegation', 'Korean delegation', 'Albanian delegation'], what: [a7, a8, a9]}
  - {a11: act, verb: follow, what: D}
  - {a12: is, of: D, what: for discussion, v: 1960-06-24}
  - {a13: act, verb: cable, who: 'Peng Zhen''s delegation', words: 'the points'}
# cal.1960-02-10.cuba
things: {R: report, C: credit}
claims:
  - {b1: act, verb: report, who: alekseyev-aleksandr-i, to: 'Moscow', what: R, time: 1960-02-10}
  - {b2: say, who: guevara-ernesto, to: alekseyev-aleksandr-i, words: 'at his home, a few days after Castro''s dinner of Feb. 3', what: [b3, b4, b6, b7], by: b1}
  - {b3: act, verb: ask, who: 'Cuba', to: mikoyan-anastas, what: C, mood: will, words: 'an enormous credit'}
  - {b4: is, of: C, what: opening bid, v: 500000000 USD}
  - {b5: act, verb: discuss, who: [castro-fidel, alekseyev-aleksandr-i], what: C, v: 100000000 USD, time: 1959-11, by: '?'}
  - {b6: act, verb: announce, who: 'the Kremlin', what: C, mood: may}
  - {b7: quote, who: guevara-ernesto, words: '"It is very important for Cuba to feel independent of the U.S. and to demonstrate it."'}
  - {b8: act, verb: show, to: mikoyan-anastas, what: R}
```

**Form 3. An event code.** Political science has coded events this way since the 1960s (WEIS; COPDAB; today CAMEO, which the large event databases use). One event is four values: the date, the actor, a code for the kind of act, the target. Claim a3 would be about `1960-06-23, USSR, 010, CHN`, where 010 is the code for "make a statement".

**Form 4. Triples.** Wikidata and the semantic web store every fact as subject, property, value. An act becomes several triples about a label made up for the act: `(E1, type, hand)`, `(E1, actor, soviet-delegation)`, `(E1, recipient, peng-zhen-delegation)`, `(E1, object, L)`, `(E1, date, 1960-06-23)`.

Two other established forms deserve a line each. A controlled language (Attempto Controlled English is one) is English cut down to fixed sentence patterns that a program can parse; it is Form 0 made consistent, and no shorter. CIDOC CRM is the museums' model of events, with fixed names for who carried an act out, where and when; it is Form 4 with an agreed list of properties.

### What each keeps and loses

- **Form 0.** Keeps every shade of the line: "may announce", "an enormous credit", "by … delegations' word". Loses consistency: two writers word one fact two ways. A tool can check only that the names and numbers of the sentence are in the line. The sentence and the fields state the fact twice, and the two can disagree.
- **Form 1.** Shorter. The shape is the same for every claim. The words still vary: "hands", "gives" and "delivers" are three verbs to a search. "The letter", "the same text" and "it" are three names for one thing.
- **Form 2.** The shortest of the forms that keep the facts. A tool can check every value: the kind is on the list, the kind's required fields are present, each key is in its list, each date is a date, and `words` is found in the part. Two writers produce the same record more often, and they can be compared field by field. It loses what the lists have no place for, unless `words` holds it: the manner of an act ("suddenly"), a judgment ("enormous"), a phrase such as "for discussion". It makes the writer decide things the line leaves unstated. In b5 the line says "in November"; the record must give the year. The list of persons has no delegations, so a3 and a13 hold "Peng Zhen's delegation" in words, and `check` cannot test it until bodies have keys too. The list of verbs will be asked to grow.
- **Form 3.** The shortest. Too coarse for citation: handing over a letter and making a speech can take one code, and the code holds no object, no figure and no words. It was made for counting events, not for sourcing each one.
- **Form 4.** As exact as Form 2, and longer: five triples for one act. It is the right form for publishing the data to others. It is not a form for people or models to write.

### How it is written and checked

- A model pass writes Form 2 from the line, the fields and the tags, as section 6 says. The lists (kinds, verbs, name keys, place keys) are given to it. A reader or an auditor who corrects a claim edits the same record.
- The checks are those of section 6, 4, and they are stricter here, because every value has a list or a form to be tested against.
- Two passes are compared field by field. That gives a rate of agreement for each kind of field. Two sentences can only be compared by eye.
- For reading, `./bib claims show` prints each record as a sentence by a fixed pattern for its kind: "a4: The letter of the CPSU Central Committee is dated June 21, 1960." The sentence is printed, never stored. So no fact is stated twice in the data.

### Which I would use

Form 2: a typed record with about a dozen kinds, values from the calendar's own lists, and `words` for exact wording, quoted from the line. Form 0's sentence is printed from it for people. Forms 3 and 4 are not for this. The trial of section 8 should write Form 2. It would show how many claims need `words` to hold their content. If most do, the lists are too small or the form does not fit.

## 11. Compiling the line from the claims

The owner, Nov. 25: "your atomic claim model cleaves the prose sentence from the claims. Is there a way to design the claim backend and the prose compiler that would resolve a set of atomic claims into prose mechanically, without the exercise of judgment?"

For some kinds of entry, yes. For the calendar as a whole, no. Where a compiler by rule reproduces the house's prose, it does so because the claims already hold every choice the writer made. The judgment has not gone. It has moved into the claims.

### What the claims would have to hold

A compiler that uses no judgment needs every one of these stored, or fixed by a rule that has no exceptions.

- The order of the claims.
- Which claims share a sentence, and which share a clause.
- The verb of each act, from a fixed list, with its forms: the present ("hands"), the earlier past ("had gone"), the participle ("shown"), the noun ("the handing-over").
- The tense. A rule can supply it: an act on the entry's day is in the present; an earlier act takes "had".
- What is said to be possible or intended: "will ask", "may announce".
- Attribution, and its form: a report ("Alekseyev to Moscow:"), speech ("Guevara says"), a third party's word ("by the … delegations' word").
- How to name a person or thing the second time: "the delegation", "the Chinese", "it".
- Exact words for quotations, lists, and any phrase the lists do not cover.
- The house's clipped style as fixed rules. Today's rule is "drop articles and verbs where the line still reads". "Where the line still reads" is a judgment. A compiler needs "always drop" or "never drop" for each pattern.

This is an established method: text generation from templates. Weather forecasts, sports results and company earnings reports are written by it. The Wikipedia project called Abstract Wikipedia is building it to write encyclopedia sentences from Wikidata. It works where texts are regular and each kind of fact has a pattern. Its two known hard steps are grouping facts into sentences and naming a thing that has been named before.

### What a compiler by rule gives on the two entries

No compiler exists. These are worked by hand from the Form 2 records of section 10, by these rules. The place and time of the first act come first. An act is "who, verb, to whom, what". A thing's properties follow it in stored order: ", dated …", ", in N …", then a list in parentheses. An earlier act takes "had". A third party's word comes last in its clause. A thing named before is "the" and its noun. A person named before is his surname. A date is written in full. No pronouns. An act with no actor is its participle alone.

`cal.1960-06-23.soviet-union`, compiled:

> Bucharest, morning. The Soviet delegation hands Peng Zhen's delegation the letter of the CPSU Central Committee, dated June 21, in seven parts (the era; war and peace; … unity). The letter had gone to the other parties as a "notification" on June 21, before the handing-over, by the Vietnamese, Korean and Albanian delegations' word. The draft communique follows, for discussion on June 24. Peng Zhen's delegation cables the points.

The line as it stands:

> Bucharest, morning. The Soviet delegation hands Peng Zhen's delegation the CPSU Central Committee's letter, dated June 21, in seven parts (the era; war and peace; … unity). The same text had gone to the other parties as a "notification" on June 21, before the Chinese had it, by the Vietnamese, Korean and Albanian delegations' word. A draft communique follows, for discussion on the 24th. The delegation cables the points.

Six differences. "The letter of the CPSU Central Committee" for "the CPSU Central Committee's letter". "The letter" for "The same text": the line means the text, sent in other copies, and the record has one thing, L. "Before the handing-over" for "before the Chinese had it". "The draft communique" for "A draft communique": the rule cannot tell a first mention in the line from a thing declared in the record. "June 24" for "the 24th". "Peng Zhen's delegation" for "The delegation". The second is a difference of fact. The rest are differences of wording.

`cal.1960-02-10.cuba`, compiled:

> Alekseyev to Moscow: Guevara, at his home, a few days after Castro's dinner of Feb. 3, says Cuba will ask Mikoyan for an enormous credit; the opening bid of the credit $500 million; the Kremlin may announce the credit. Castro and Alekseyev had discussed $100 million in November 1959. "It is very important for Cuba to feel independent of the U.S. and to demonstrate it." Shown to Mikoyan.

The line as it stands:

> Alekseyev to Moscow: Guevara, at his home, a few days after Castro's dinner of Feb. 3, says Cuba will ask Mikoyan for an enormous credit, $500 million the opening bid (Castro and Alekseyev had spoken of $100 million in November); the Kremlin may announce it. "It is very important for Cuba to feel independent of the U.S. and to demonstrate it." Shown to Mikoyan.

Five differences. The opening bid is a clause of its own, where the line attaches it to the credit with a comma. The $100 million of November is a separate sentence after Guevara's speech, where the line has it in parentheses inside the speech: the record does not know whose statement it is (`by: '?'`), so the rule has no place for it. "The credit" for "it". "Had discussed" for "had spoken of": the verb list has one verb for both. "November 1959" for "November": the record must give the year.

In both entries the compiled line is close, and in both it is not the line. Each difference can be removed in one of two ways. Store the choice in the claim (the word "same", the parenthesis, "it"). Or accept the compiler's wording as the house's.

### Where rule ends and judgment begins

- Grouping. Which facts go in one sentence, which in parentheses, which after a semicolon. A rule can copy a stored grouping. Someone chose the grouping.
- Naming again. "The Chinese", "the delegation", "it", "the same text". Each is a choice, and "the same text" carries a fact.
- Dropping words. From `cal.1969-04-01.china-leadership`: "Dong, eighty-three, the oldest delegate; 422, 28 percent, for the armed forces." "The congress not announced; no foreign guests." Eight of that line's fifteen units have no finite verb. A rule can drop "is" in every `is` claim. It cannot decide that "422, 28 percent, for the armed forces" still reads.
- Emphasis and choice of detail. "An enormous credit." "Suddenly."
- An unanswered question. Claim b5: the prose can leave open whose remark it is. A compiler must put the remark somewhere, and wherever it puts it says something.

### The designs between

1. **The line kept as written, and checked against the claims by rule.** This is section 6. People write the line. A pass writes the claims. Rules test that the two agree: every name, number, date and quoted word of the part is in a claim, and the reverse. Judgment is used twice, in the writing and in the claims. The checks are mechanical. No line of the calendar changes.
2. **The line compiled, then edited, the edit recorded.** The compiler writes a first line. A person edits it. Both are stored, or the difference is. A rule tests that the edit changed no name, number or date. The cost: two texts for each entry, and an edit that must be made again whenever the claims change.
3. **Templates for some kinds of act.** Where a kind of entry already has a fixed form, the line is compiled from its claims by a pattern, and no one writes it. The house has such forms: the election result ("Winner (P) over Loser (P), W to L, p percent"), which `check` enforces; a roll call; a law signed, with its statute. They are few. By a count of the calendar as it stands today (58,361 entries, after a merge): 500 lines link a roll call, 232 link a statute, and 25 hold an election result in the fixed form (a strict pattern, probably low). More kinds could be given patterns: a nomination, a confirmation, a chamber's vote, an arrival, a meeting with its parties, place and hour. Each would be shown to the owner first.
4. **The round trip as a measure.** Take the claims from a line. Compile them. Compare the result with the line. A line that comes back the same is regular: rule alone can write it. The share of such lines is a number the trial of section 8 can give, for each kind of entry.

A note on the brief. Its model is "Springs and Autumns, but without the subtle words". That chronicle uses a fixed verb for each kind of act. A calendar written wholly by pattern would be nearer to it than today's lines are. It would also be a different text from the one the readers have written: every line would change, and each would lose what its writer chose to keep. That is the owner's choice to make, and design 4 would show its cost first.

### Do the two answers differ?

Yes.

- On the form of the claims (section 10): a shorter form exists that is more exact and more consistent than sentences. I would use it: the typed record, Form 2.
- On compiling the line (this section): rule alone can write the line only for regular kinds of entry, and only when the claims hold the order, the grouping, the verb and the exact words. I would not compile the calendar's lines. I would keep the line as written and check it against the claims by rule (design 1), give patterns to the kinds that already have a fixed form (design 3), and have the trial count the lines that survive the round trip (design 4).
- The two fit together. A pattern for a kind of act needs exactly the typed record of Form 2. So choosing Form 2 now allows compiling later, one kind of entry at a time.
