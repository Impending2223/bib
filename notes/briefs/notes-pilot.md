# Pilot: dating the calendar's loose entries by the books' endnotes (Nov. 13, 2026)

The owner, Nov. 12, 2026, on two DeBenedetti entries the notes dated (Bigart's survey, July 25, 1962, by 422 n.9; Sully's *Newsweek* article, Aug. 20, 1962, by 422 nn.7, 9): "These guys gotta read the footnotes... (Do the PDFs make that awkward?)"; then "Please do re: the notes tool pilot." The calendar holds about 5,600 entries dated to a month or carrying "Check: the day". The pilot reads one book's notes for all of its loose entries, to measure how many the notes settle before a sweep goes book by book.

The book: Charles DeBenedetti with Charles Chatfield, *An American Ordeal* (1990), card `w.debenedetti-american-ordeal`; Drive id `1_nFvLjPMNdauVsL3WsIYu9-TbnYGBEou` (53 MB, an Internet Archive scan: OCR text layer, superscripts often garbled). Its loose entries: 134 (120 dated to a month), listed with the pages they cite in `rows.json` (the lead puts it in your scratch directory; or rebuild it: every calendar entry whose `n` cites the card and that is dated to a month or carries "Check: the day/month/date").

## The tool: `tools/works/endnotes.py` (its STYLE)

```
python3 -I tools/works/endnotes.py index BOOK.pdf --out DIR     # once: DIR/BOOK.notes.json
python3 -I tools/works/endnotes.py page DIR/BOOK.notes.json 84   # the notes estimated for p. 84 (±1 page)
python3 -I tools/works/endnotes.py note DIR/BOOK.notes.json 4 9  # chapter 4, note 9
python3 -I tools/works/endnotes.py chapters DIR/BOOK.notes.json
```

Each note prints with its own notes page and number ("[422 n.9; ch. 4 ...]"), the cite form. The page a note belongs to is an estimate (the notes pages' running heads, "Notes to Pages 77–89"): read the page's sentence and its superscript on the page image (`pdftoppm -f N -l N -r 100 -png`) and the note together before you rely on it. The index holds the book's text: keep it in your scratch directory and delete it with the PDF.

## For each entry

1. `./bib show ID` (the rev for `base:`); read the cited page around the entry's matter; find its superscript and its note (`page`, then the image where the superscript is unreadable).
2. Rule:
   - **The note dates it to the day.** A dated source for the event itself (a letter, a memorandum, a speech's text, a statement), or, for a press item whose publication is the event (an article, a column, an advertisement, a broadcast), the issue's date. An `edit` op with `base:`: `date`, `when`; `n`: after the page pin add the note ("84; 422 n.9 (the day: ...)", a few words of the note at most), put the source the note names behind "To check:" ("To check: [*New York Times*, July 25, 1962](https://timesmachine.nytimes.com/timesmachine/1962/07/25/issue.html), at 1 (cited by [[w.debenedetti-american-ordeal]], 422 n.9)."), and strike "Check: the day" (or "the month"). The merge moves the entry to its month. Never change the `id`. Models in the tree: `./bib show cal.1962-07.press-and-broadcasting-2 cal.1962-07.press-and-broadcasting-3`.
   - **The note cites a newspaper's report of an event** (not the publication as the event): the paper's date bounds the event, it does not date it. Narrow the Check ("Check: the day (the *Times* reports it July 25, 1962)") and put the paper behind "To check:"; date the entry to the day only where the note or page gives the event's own day.
   - **The note gives a weekly's issue** (*Newsweek*, *Time*, *The Nation*): the issue's date, with "Check: the day on sale (the issue is dated ...)" as in the model.
   - **The note dates it to a month only, or not at all:** no change; record it.
   - **The note's date disagrees with the entry** (another month, another year): a `check` op (or `variant` where the entry states the date in `c`).
   - **`c` states the loose date** ("In July", "shortly after Bigart's survey"): edit `c` only to drop the words the new date makes wrong; then set `src.c` to the new hash (`python3 -c "import sys; sys.path.insert(0,'tools'); from bib import claims; print(claims.chash(C))"`) and re-letter the rows if a unit went.
3. Check the neighbours on the new day (`./bib find -l cal --since D --until D`): if the calendar already holds the event there, under another thread, report it (do not combine).

## Mechanics and the report

One patch, `inbox/2026-11-13-pilot-notes-debenedetti.yaml` (patch name the same), drafted in your scratch directory, moved into `inbox/` when `./bib patch-check` gives 0 errors. Never merge, never commit, never edit `lists/`, never read `build/` or a whole list file. Fetch the PDF whole by curl (the Drive tool truncates at 10 MB): `curl -sSL -o DIR/deb.pdf "https://drive.usercontent.google.com/download?id=1_nFvLjPMNdauVsL3WsIYu9-TbnYGBEou&export=download&confirm=t"`; delete it and the index when done; never change the file's sharing. Quote no more of the book than a few words.

Write `notes/pilots/notes-debenedetti.md`: a table, one row an entry (id, old date, the note read, ruling, new date); the counts by ruling (dated to the day; bounded; month only; nothing; disagrees); how often the tool's estimate held (the right note within ±1 page) and where it failed; time and tokens if you know them; what a sweep of the other books would need (forms of notes the tool did not read).
