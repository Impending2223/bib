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

## The test for a part

A source's note names a part only when the part, with the words it names, stands as a statement on its own: who, what, and the matter it bears on, without leaning on a part the source does not support. "Rusk to Dobrynin … Moscow will send Zorin" passes. "The date is open" does not: "the date" is the talks', so the source bears on the whole, and its note is a whole-entry note. Where in doubt, the whole entry.

## Display: footnotes, compiled (the owner's design)

The owner, Nov. 24, 4:00 p.m.: "What's wrong with footnotes? ... I have no objection to footnotes ... I just have an objection to four footnotes that all say the same thing. When a new pass complicates and splits the original into parts, shouldn't those parts compile, mechanically, into footnoted passages, with the contents of a footnote compiled, mechanically, from the supporting citations? Shouldn't things look identical online, in print, and in the ebook? Should I have to tap or hover to see the matching?" (This withdraws a tap-to-highlight display proposed a few minutes before, a departure from the site's style that the style rule forbids.)

- An entry starts as one passage, the whole of `c`, with one footnote: its sources, each with its pinpoint (the owner's claim_0).
- A later pass that speaks to part of it splits the entry there: its note names the part (a quote of the words), and the entry is now two or more passages, each ending with a footnote mark.
- The passages are compiled mechanically from the notes: a passage is a stretch of `c` over which the set of supporting notes is the same; its mark falls at its end; its footnote lists exactly those notes' citations, in the house form (footnotes.py, STYLE 3–10, unchanged: *id*., first cites, the order).
- No parentheticals are added to name a part: the mark's place names it. A footnote after a clause supports that clause read in its sentence, as footnotes do, so a passage needs no frame or speaker of its own ("what dates are open?" does not arise: the passage is read in its sentence, never stored or shown alone).
- No passage arises without a difference in sources, so no two adjacent footnotes say the same thing (today's footnotes.py STYLE 8 problem, "four footnotes each repeating the note", is cured at the root).
- The same on the site, in print and in the EPUB: the footnotes are text, compiled at the build, nothing to tap or hover.
- The test for a part (above) still governs where a pass may split: at the end of words that, read in their sentence, are what the source supports.

In the example: FRUS's note on the whole, Beschloss's on "Moscow will send Zorin".

> Rusk to Dobrynin: the talks will resume on Monday;¹ Moscow will send Zorin.²
>
> ¹ FRUS 1961–63, V, doc. 12.
>
> ² *Id*.; Beschloss, *Crisis Years*, 123.

## Side by side

| | Today | Stored claims and compiler | Stand-off annotation |
|---|---|---|---|
| What is stored | text, and maps by letter | a list of claims | text, and notes |
| Where claims come from | punctuation | written up front | where sources differ |
| An entry with one source | cut anyway | cut anyway | one claim |
| What readers write | a sentence and letters | a list | a sentence; a quote only where needed |
| A shared speaker | stuck in the first unit | a frame | read in the sentence, as footnotes are |
| After an edit | letters shift | ids hold | ids hold; orphaned notes flagged |
| Rebuilding the line | none | a compiler | none |
| Precedent | ours | ours | the W3C standard |

## Recommendation

Design 3, with the test for a part. It is the default taken (`notes/owner-rulings.md`, 35 and 35a), and the design note is to be rewritten to it before any converter.
