# The claims model: three designs compared

For the owner, Nov. 24, 2026. Written to a file at the owner's word ("I'm not sure you should be writing these to a reply rather than to an MD"). The design note itself, `notes/proposals/claims-model.md`, is to be rewritten to the choice made here (`notes/owner-rulings.md`, items 31–35a). A paragraph a line, as the house rule asks.

## The question

Each calendar entry's statement (`c`) rests on sources. The calendar needs to know which source bears on which part of the statement, so that footnotes, variants (a source that disagrees), visibility and R22 (changes to an entry) can work part by part. How should that be stored?

## An example entry

`c`: "Rusk to Dobrynin: the talks will resume on Monday; Moscow will send Zorin."

Its sources:

- FRUS 1961–63, V, doc. 12 bears on all of it.
- Beschloss, *Crisis Years*, 123 bears only on Zorin's being sent, as Rusk told Dobrynin; he says nothing of Monday.

The two halves can be told apart: "Rusk told Dobrynin Moscow will send Zorin" stands as a statement without the talks' day. (The earlier example, "the talks will resume; the date is open", could not be split: "the date" is the talks' date, so a source on it is a source on the whole. That is the test below.)

## Design 1: today

`c` is one string. A splitter cuts it at full stops and semicolons into units with letters: A = "Rusk to Dobrynin: the talks will resume on Monday;", B = "Moscow will send Zorin." A claim map says FRUS covers A and B, Beschloss B.

- The cuts come from punctuation, not from the sources.
- The letters shift when the text is edited.
- B alone loses its speaker ("Rusk to Dobrynin" is inside A).
- A source on part of a unit cannot say so.

## Design 2: stored claims and a compiler (the design note's present text)

`c` becomes a list of claims, each with a permanent id and its sources; the shared head ("Rusk to Dobrynin") a frame over them; a compiler joins them back into the sentence.

```yaml
c:
  - frame: 'Rusk to Dobrynin'
    claims:
      - {id: k1, t: 'the talks will resume on Monday', src: [frus-12]}
      - {id: k2, t: 'Moscow will send Zorin', src: [frus-12, beschloss-123]}
```

- Permanent ids; R22 claim by claim.
- Every entry is cut up front, most into claims with the same sources (the owner: "several 'claims' that have identical mapping").
- The cuts still follow the old punctuation.
- Frames, joining rules and a compiler to keep in step; readers write lists, not sentences.

## Design 3: stand-off annotation (the W3C Web Annotation model)

The text stays one string, never cut. Each source is a note attached to the text: by default to all of it; to a part only where a source bears on a part, by quoting all the words of the statement it supports, in one stretch or several.

```yaml
c: 'Rusk to Dobrynin: the talks will resume on Monday; Moscow will send Zorin.'
notes:
  - {id: a1, cites: frus-12}                                                      # the whole entry
  - {id: a2, cites: beschloss-123, on: ['Rusk to Dobrynin', 'Moscow will send Zorin']}
```

At the build the page finds where the set of notes changes, and those are the claims: "the talks will resume on Monday" has FRUS; "Rusk to Dobrynin … Moscow will send Zorin" has FRUS and Beschloss. A footnote mark falls at a note's last word; notes that end together share one mark. Here both end at "Zorin.", so the line keeps one mark, as now:

> Rusk to Dobrynin: the talks will resume on Monday; Moscow will send Zorin.¹
>
> ¹ FRUS 1961–63, V, doc. 12; Beschloss, *Crisis Years*, 123.

Which words Beschloss covers is in the note, and the page shows it on a tap or hover (below), not in a parenthetical.

- An entry with one source, or whose sources all bear on the whole, is one claim, never cut: the owner's claim_0. Claims appear only where a source makes them (the owner's "complicating pass").
- Nothing turns on punctuation.
- Readers write a sentence, and quote a part only where a source speaks to a part.
- A shared speaker or subject needs no frame: several notes claim the same words.
- Variants, visibility rulings and Checks attach the same way, each a note with its own purpose (supporting, disputing, ...).
- Ids live on the notes and hold through edits; an edit touches only the notes whose words it changes (R22); `check` lists a note whose words no longer appear, for a reader to re-attach.
- An established design (web annotation; the stand-off markup of TEI editions), not one of ours.
- Costs: a phrase that occurs twice in one entry is pinned by a few words either side (the standard provides for it); converting today's maps turns lettered units into quoted words, with care.

## The test for a part

A source's note names a part only when the part, with the words it names, stands as a statement on its own: who, what, and the matter it bears on, without leaning on a part the source does not support. "Rusk to Dobrynin … Moscow will send Zorin" passes. "The date is open" does not: "the date" is the talks', so the source bears on the whole, and its note is a whole-entry note. Where in doubt, the whole entry.

## Showing which part a source supports, without parentheticals

The owner (Nov. 24, 3:55 p.m.): "Does Design 3 require the parenthetical? It seems like it would lead to unreadable/unparseable sourcing blocks at scale." It does not. The parenthetical above was carried over from today's house form; in Design 3 the note's target is data, so the page need not say it in words.

- The footnote block stays as now: the sources at a mark, each with its pinpoint, and nothing more ("FRUS 1961–63, V, doc. 12; Beschloss, *Crisis Years*, 123").
- The part is shown by the page itself: tapping or hovering a source in a footnote highlights the words its note covers in the line (the visibility spans' machinery, already on the page, does the highlighting). Printed or in the EPUB, where nothing can be tapped, the block reads as above.
- Marks: one at each place a note's statement ends, notes ending together sharing it; a source on part of the entry whose statement ends earlier gets its own mark there. In the example both statements end at "Zorin.", so one mark.
- The existing parentheticals stay where they say something the target cannot: a page's subject ("(the vote)") where a reader wrote it as a gloss, "citing ...", a document's own date. New readers write none to name a part; the converter turns today's part-naming parentheticals into targets where the claim map already gives the part, and leaves the rest as written.

## Side by side

| | Today | Stored claims and compiler | Stand-off annotation |
|---|---|---|---|
| What is stored | text, and maps by letter | a list of claims | text, and notes |
| Where claims come from | punctuation | written up front | where sources differ |
| An entry with one source | cut anyway | cut anyway | one claim |
| What readers write | a sentence and letters | a list | a sentence; a quote only where needed |
| A shared speaker | stuck in the first unit | a frame | claimed by several notes |
| After an edit | letters shift | ids hold | ids hold; orphaned notes flagged |
| Rebuilding the line | none | a compiler | none |
| Precedent | ours | ours | the W3C standard |

## Recommendation

Design 3, with the test for a part. It is the default taken (`notes/owner-rulings.md`, 35 and 35a), and the design note is to be rewritten to it before any converter.
