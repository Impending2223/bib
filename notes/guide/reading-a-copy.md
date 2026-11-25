# Getting a source and reading its page: the recipes

For every reader and auditor, and for the session that briefs them. These problems are solved; do it this way. The rules are the reader's brief, R4, R54 and R54a. The owner, Nov. 24, 2026: "these are all solved problems... can you write the solution to them somewhere the readers (and you!) can find and read?"

The recipes below are the ones the Opus auditors used on the night of Nov. 24, 2026, to read both volumes of Yang Shangkun's diary (24 MB and 20 MB scans with no text layer) and seven other works. Earlier runs used the same download line (`notes/book-checks/thomas-robert-kennedy.md`, `young-two-suns.md`).

## 1. Work in a directory of your own

The scratchpad is shared by every agent of the session. Make a directory with a name nobody else will pick, and keep everything in it.

```
D=/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/<your batch or audit name>-$$
mkdir -p "$D" && cd "$D"
```

Never write to a generic name such as `audit/`, `dump.txt` or `ids.txt` at the top of the scratchpad: on Nov. 24 three agents overwrote one another's files that way. Never put a copy of a source in the repository.

## 2. Find the Drive file

Try these in order.

1. The work's book-check file, `notes/book-checks/<card without w.>.md`: it usually gives the Drive id and the page offset.
2. `grep -i '<a word of the title>' notes/drive-inventory-2026-11-25.tsv notes/drive-additions-2026-11.md`: the first column of the TSV is the Drive id.
3. `./bib works show w.<card>`: the card's note may name the file.
4. The Drive search tool. Load it with ToolSearch (`select:mcp__Google_Drive__search_files`). Search by title, in the work's own script too, with `excludeContentSnippets: true`: `title contains '杨尚昆' or title contains 'Yang Shangkun'`. The result gives each file's id and size.

### Files whose names mislead

- **The Mao nianpu** (`w.zedong-mao-zedong-nianpu`): Drive id `1ch6UXFFBQiWlpRwvFjUhVyGw-CyDKgxy`, an EPUB of 5.6 MB. Until Nov. 24, 2026 its file name contained "年月目录" ("index by year and month"), which named the EPUB's navigation, not its content; the owner took those words out of the name that evening. The EPUB still opens on its index of years and months, so a tool that returns only a file's first pages (the Drive connector's `read_file_content`) shows an index and nothing else. The file is the whole chronology: 123 parts, about 4 million characters, running to 1976 (checked Nov. 24, 2026). It is not "only a table of contents". Fetch it with the curl line below, unzip it, and find the day under its year and month (recipe 6, "An EPUB"); a day is written "7月16日" under the year's heading, so search for the month and day, not the full date.
- A card's Drive id is in `notes/drive-cards-2026-11-25.tsv` (card, id) where the inventory of Nov. 25 found the file; ids are never written into a card's note, which the site prints.

## 3. Get the file onto disk, whatever its size

Use curl on Drive's download address with the file's id. This works for every file in the owner's shared folder. It worked on the first try for files of 20, 24, 25 and 69 MB.

```
curl -sSL -o book.pdf "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"
file book.pdf        # must say PDF document (or EPUB, Zip archive)
pdfinfo book.pdf     # the real page count; ignore the page count `file` prints
```

Do not use the Drive connector's own tools to fetch a book. `download_file_content` refuses a file over 10 MB. `read_file_content` returns only the text of about the first 170 pages, and nothing of a scan.

If `file` says "HTML document", the file is not shared by link and curl got a sign-in page. Then, and only then, the file cannot be fetched. Say so in your report, with the file's name and id, so the owner can move it into the shared folder. Do not cite its pages.

## 4. Find the PDF page for a printed page

The PDF page is the printed page plus an offset. The offset differs from volume to volume, and can change after the front matter or the plates.

1. Take the offset from the book-check file if it gives one.
2. Check it: render one page small and read the printed page number on it.

```
pdftoppm -f 485 -l 485 -r 60 -png book.pdf probe      # then open probe-485.png with the Read tool
```

Yang Shangkun's diary: volume I is printed page plus 6, volume II plus 5 on the pages the auditors of Nov. 24 read (to about p. 390). The offset does not hold through volume II: a reader of Nov. 25 found printed 565 at page 520 of the file, and an auditor the same night found printed 649–664 at the file's page less 45 (the printed number is the file's page plus 45 there). So start from the offset, look at the printed number on the image, and step from there. Every page image shows its own printed number, so check each page as you read it. Where an offset from a book-check file does not hold, find the passage by its words instead (recipe 6).

Salinger, *With Kennedy*: in printed pp. 176–88 the printed page is the file's page less 26, not less 20 as the work's book-check file says (an auditor, Nov. 25). Longley, *LBJ's 1968*: the copy on the Drive holds one chapter only, 25 pages (an auditor, Nov. 25). Take the page from the image in both, as everywhere.

A page count from the `file` command is not the file's page count: on the copy of the Zhou Enlai nianpu, II, it prints "4 page(s)" for a volume of 773 pages, and a reader of Nov. 25 took the copy for a fragment and left a page unread. Count the pages with `pdfinfo` (or `mutool info`), and open the page.

## 5. Read one page of a scan

Render the page and open the image with the Read tool. You can read a page image directly, in any script. At 80 to 90 dpi a page of Chinese is clearly legible; use 150 or 200 for small print or footnotes.

```
p=479; off=6
pdftoppm -f $((p+off)) -l $((p+off)) -r 90 -png book.pdf page
```

Read the image. That is the reading. A file's size, a missing text layer and poor OCR are never grounds to take a page's content from an earlier reader's parenthetical (R54a).

## 6. Find a passage: text layers, OCR, EPUBs

A PDF with a text layer:

```
pdftotext -layout book.pdf book.txt            # or one stretch: pdftotext -layout -f 300 -l 320 book.pdf part.txt
grep -n "Kharlamov\|Minow" book.txt
sed -n '4120,4160p' book.txt
```

Running heads in the text give the printed page ("212 WITH KENNEDY"). Some text layers come out garbled (old Vietnamese font encodings; broken CJK fonts). They are often still good enough to find a date or an hour; then read the page as an image (recipe 5).

A scan with no text layer, when you need to find where a passage is: OCR the few pages you suspect, only to locate it, and then read the image.

```
pdftoppm -f 480 -l 490 -r 150 -png book.pdf s
for f in s-*.png; do tesseract "$f" "${f%.png}" -l chi_sim 2>/dev/null; done    # chi_tra for traditional; eng for English
grep -l "十二月" s-*.txt
```

`ocrmypdf` is not installed here; use `pdftoppm` and `tesseract`. The languages installed are `chi_sim`, `chi_tra`, `chi_tra_vert` and `eng`. A chronology (nianpu) is in date order, so the date finds the page faster than OCR does: render a page, read its date, and step toward the day you want.

An EPUB:

```
mkdir book && cd book && unzip -q -o ../book.epub
grep -l "8月5日" -r . | head
python3 -I -c "import re,sys; t=open(sys.argv[1],encoding='utf-8').read(); t=re.sub(r'<[^>]+>','',t); i=t.find(sys.argv[2]); print(t[max(0,i-200):i+600])" text/part0094.html "8月5日"
```

An EPUB has no printed pages. Cite it as the card or its book-check file says (by date, chapter or section).

## 7. Records online and in the repository

- FRUS: the document's page at history.state.gov (the entry's note links it). Read it with WebFetch or curl. The daybook keeps each document's date and time under `daybook/`.
- The Public Papers: the govinfo PDF the note links, at its `#page=`; and the item's page on the American Presidency Project (presidency.ucsb.edu), read with WebFetch. Ask WebFetch to quote the date line and the words you need.
- White House recordings: the catalogues under `daybook/recordings/` give each recording's time and participants.
- The Congressional Record, the Statutes and the cases: the links the notes give.

A host the session's network does not allow fails with a proxy error. Say which host in your report; do not go round it.

## 8. Clean up, and what never to do

- Delete the PDF, the EPUB's files, the text dumps and the page images when you finish with a work: `rm -rf "$D/<the work's files>"`. Nothing of a copyrighted source stays on disk or goes into the repository.
- Quote no more than a few words of a copyrighted work anywhere.
- Change nothing on Drive: no moves, no renames, no sharing changes, no trash.

## 9. When something still fails

Say in your report exactly what you ran and what came back (the command, the error, `file`'s output). Leave the words that depended on that page out of your patch, and list the entry for the audit. Do not describe a solved problem as an obstacle: if the recipe above was not tried, try it first.
