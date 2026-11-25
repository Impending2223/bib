# The claims model: three designs compared

For the owner, Nov. 24, 2026. Written to a file at the owner's word ("I'm not sure you should be writing these to a reply rather than to an MD"). A paragraph a line, as the house rule asks.

**Corrected Nov. 25, 2026.** Neither Design 2 nor Design 3 below is adopted. Two reviews found that today's build already makes the footnotes described under "Display": neighbouring units with the same sources share one mark and one footnote. Design 2 cuts every entry into stored claims, most with the same sources, which the owner objected to on Nov. 24. Design 3 stores a copy of the words with every source; the copy goes out of date when the line is edited, a third of the copies would hold quotation marks, and a visibility ruling cannot hold one. The design adopted is ruling 35f, with 35g's additions: the line stays one string, and a numbered cut is stored in it where a source, a ruling or a variant bears on part. It is set out in `notes/proposals/claims-model.md`. This file is kept for the comparison and for the owner's words, which stand as they were written.

## The question

Each calendar entry's statement (`c`) rests on sources. The calendar needs to know which source bears on which part of the statement, so that footnotes, variants (a source that disagrees), visibility and R22 (changes to an entry) can work part by part. How should that be stored?

## An example entry

`c`: "Rusk to Dobrynin: the talks will resume on Monday; Moscow will send Zorin."

Its sources:

- FRUS 1961–63, V, doc. 12 bears on all of it.
- Beschloss, *Crisis Years*, 123 bears only on Zorin's being sent, as Rusk told Dobrynin; he says nothing of Monday.

The two halves can be told apart: "Rusk told Dobrynin Moscow will send Zorin" stands as a statement without the talks' day. (The earlier example was "the talks will resume; the date is open". Corrected Nov. 25: this paragraph said that example could not be split, and that a source on the date was a source on the whole. That was wrong. A source that says only that the date is open is cited at the end of "the date is open", and for those words alone. See "Where a part ends", below.)

## Design 1: today

`c` is one string. A splitter cuts it at full stops and semicolons into units with letters: A = "Rusk to Dobrynin: the talks will resume on Monday;", B = "Moscow will send Zorin." A claim map says FRUS covers A and B, Beschloss B.

- The build joins neighbouring units that have the same sources. They share one footnote mark and one footnote. An entry whose sources all support the whole line is one block with no mark.
- A mark can fall only where a unit ends.
- The letters shift when the text is edited. This is the fault that ruling 35f mends.
- A source on part of a unit cannot say so.

## Design 2: stored claims and a compiler (not adopted)

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

## Design 3: stand-off annotation (the W3C Web Annotation model; not adopted)

The text stays one string, never cut. Each source is a note attached to the text: by default to all of it; to a part only where a source bears on a part, by quoting the words it supports, where they end.

```yaml
c: 'Rusk to Dobrynin: the talks will resume on Monday; Moscow will send Zorin.'
notes:
  - {id: a1, cites: frus-12}                                                      # the whole entry
  - {id: a2, cites: beschloss-123, on: 'Moscow will send Zorin'}
```

At the build the passages are compiled from the notes and footnoted, as set out under "Display" below.

- An entry with one source, or whose sources all bear on the whole, is one claim, never cut: the owner's claim_0. Claims appear only where a source makes them (the owner's "complicating pass").
- Nothing turns on punctuation.
- Readers write a sentence, and quote a part only where a source speaks to a part.
- A shared speaker or subject needs no frame: a footnoted passage is read in its sentence.
- Variants, visibility rulings and Checks attach the same way, each a note with its own purpose (supporting, disputing, ...).
- Ids live on the notes and hold through edits; an edit touches only the notes whose words it changes (R22); `check` lists a note whose words no longer appear, for a reader to re-attach.
- An established design (web annotation; the stand-off markup of TEI editions), not one of ours.
- Costs: a phrase that occurs twice in one entry is pinned by a few words either side (the standard provides for it); converting today's maps turns lettered units into quoted words, with care.

## Where a part ends

(Corrected Nov. 25. This section was "The test for a part". It sent a source that supports only part of an entry to the whole entry when the part could not stand alone. That cited the source for words it does not support, against the owner's rule of Oct. 23.) A source is cited for the words it supports, and for no others. The footnote mark goes at the end of those words. A footnote is read in its sentence, so the words need not make a statement by themselves: a mark after "; the date is open." is an ordinary footnote. A part ends where a sentence or a semicolon clause ends.

## Display: footnotes, compiled (the owner's design)

The owner, Nov. 24, 4:00 p.m.: "What's wrong with footnotes? ... I have no objection to footnotes ... I just have an objection to four footnotes that all say the same thing. When a new pass complicates and splits the original into parts, shouldn't those parts compile, mechanically, into footnoted passages, with the contents of a footnote compiled, mechanically, from the supporting citations? Shouldn't things look identical online, in print, and in the ebook? Should I have to tap or hover to see the matching?" (This withdraws a tap-to-highlight display proposed a few minutes before, a departure from the site's style that the style rule forbids.)

- An entry starts as one block, as today: the whole of `c`, then its sources, each with its pinpoint, and no footnote mark (the owner's claim_0; the owner, Nov. 18: "Citation blocks with only one citation should be rendered without the footnote").
- A later pass that speaks to part of it splits the entry there: its patch names the part by quoting the words, the merge stores a cut at the part's end (ruling 35f), and the entry is now two or more passages, each ending with a footnote mark.
- The passages are compiled mechanically from the rows, as `footnotes.py` does today: a passage is a stretch of `c` over which the set of supporting sources is the same; its mark falls at its end; its footnote lists exactly those sources' citations, in the house form (footnotes.py, STYLE 3–10, unchanged: *id*., first cites, the order).
- No parentheticals are added to name a part: the mark's place names it. A footnote after a clause supports that clause read in its sentence, as footnotes do, so a passage needs no frame or speaker of its own ("what dates are open?" does not arise: the passage is read in its sentence, never stored or shown alone).
- No passage arises without a difference in sources, so no two neighbouring footnotes are the same. Today's build already ensures this. A source that every footnote of an entry shares is still printed under each; how to print it once is a display question, kept apart (`notes/proposals/claims-model.md`, section (g)).
- The same on the site, in print and in the EPUB: the footnotes are text, compiled at the build, nothing to tap or hover.
- A pass may split at the end of the words that its source supports, where a sentence or a semicolon clause ends.

In the example: FRUS for the whole, Beschloss for "Moscow will send Zorin".

> Rusk to Dobrynin: the talks will resume on Monday;¹ Moscow will send Zorin.²
>
> ¹ FRUS 1961–63, V, doc. 12.
>
> ² *Id*.; Beschloss, *Crisis Years*, 123.

## Side by side

| | Today | Stored claims and compiler (not adopted) | Stand-off annotation (not adopted) | Cuts in the line (35f, adopted) |
|---|---|---|---|---|
| What is stored | the line, and rows by letter | a list of claims | the line, and notes that quote it | the line with numbered cuts, and rows by number |
| Where a footnote mark falls | where neighbouring units' sources differ | after each run of claims with the same sources | where the quoted words end | where neighbouring units' sources differ, as today |
| An entry with one source | one block, no mark | a list of claims, one block on the page | one block, no mark | one block, no mark; no cut |
| What readers write | a sentence and letters | a list | a sentence; a quote where needed | a sentence; a quote where needed, in the patch only |
| A shared speaker | read in the sentence | a frame | read in the sentence | read in the sentence |
| After an edit | letters shift | ids hold | a quote may no longer be found | numbers hold |
| Rebuilding the line | none | a compiler | none | none (the cuts are taken out on load) |
| Precedent | ours | ours | the W3C standard | the footnote call; an edition's anchors |

## Recommendation

(Corrected Nov. 25.) Ruling 35f, with 35g's additions: cuts in the line, the footnotes compiled as today. It is the default taken (`notes/owner-rulings.md`, 35f and 35g), and the design note, `notes/proposals/claims-model.md`, is written to it. The recommendation that stood here was Design 3 with the test for a part (rulings 35 and 35a).
