# Thread lines off the web pages; the rubric's taps

Nov. 28, 2026. For the owner. This answers two requests of Nov. 27, 2026.

The first: "Drop the threadlines from the bottom of the web entries. Keep the navigation highlights and keyboard shortcuts. Keep the threadlines on the ebook."

The second: "Could we make it so that tapping empty space in the top line of any entry, to the right of the thread label or labels, 'untoggles' active thread highlights? And could we make it so that a single click/tap on a top-line thread label 'toggles' the thread highlight, but only double clicks/taps navigate to the thread summary?"

Nothing is merged or published. The change is in the code only. The pictures in `notes/proposals/threadlines-off/` are of February 1965 (Monday, Feb. 8, a day of 30 entries), built from the current data.

## What changed on the page

- No entry on the web pages ends in thread lines ("⟨⟨ China ⟩⟩") any more. This holds on the calendar's pages, the reader, the Names pages, the Threads pages and the Places pages, which all carried them.
- Each entry is shorter by one line for each of its threads. A calendar page is lighter by about a sixth: February 1965 went from 1,931 KB to 1,667 KB, March 1965 from 2,527 KB to 2,115 KB.
- The small square in each entry's lower right corner (the link to the entry's own page) now sits beside the note's last line. It keeps its rule: the corner of the entry's box.
- The "To:" and "From:" lines stay. They stand under an address that sets several threads going, such as a State of the Union, and under each entry it reaches. They are not thread lines. They name the entries the address led to, and a reader would lose those links without them.
- Nothing else on the page moves or changes.

Pictures, before and after, on a phone and on a desktop: `before-phone.png`, `after-phone.png`, `before-desktop.png`, `after-desktop.png`. The same with the thread "China" lit: `before-phone-lit.png`, `after-phone-lit.png`, `before-desktop-lit.png`, `after-desktop-lit.png`.

## How the rubric's taps work now

The rubric is the line of small capitals at the top of each entry that names its threads.

- One click or tap on a thread's name lights that thread at once. If that thread is already lit, the same tap clears it. The page stays where it is.
- A second click or tap on the same name within half a second goes to the thread's summary in the index at the top of the page. The highlight goes back to how it was before the first tap. A mouse double click counts even when the computer is set to a slower double click.
- The single tap does not wait to see whether a second tap is coming. It acts at once. The second tap leaves the thread lit and goes to the summary (amended on the owner's word, Nov. 27, 2026: "The second tap should go to the summary but not undo the highlight.").
- A tap on the empty part of the rubric's line clears whatever thread is lit. The empty part is everything on that line that is not a thread's name and not the place and time at the right. On a phone, the space between the names and the place and time can be narrow, and a tap close to a name may count as a tap on the name. Where a line has room, the tap clears.
- A tap on the place and time at the right does what it did before. The place's link still goes to the place's page.
- A rubric too long for its line still ends in "…", and a tap on it still opens it to its full length. That tap does nothing else if it lands on the empty part. If it lands on a thread's name, it also lights or clears that thread, as before, when such a tap lit it.
- Each thread's name is still a real link. Without the page's script it goes to the summary. With Ctrl or Cmd held down, a click opens the summary in a new tab and changes no highlight. With the keyboard, Tab to a name and Enter goes to the summary and changes no highlight.
- A tap on a thread's entry in the index at the top of the page lights or clears it, as before.
- The Names, Threads and Places pages have no thread highlights, so their rubrics are plain links, as before.

## How the arrow keys work now

While a thread is lit, the left and right arrow keys go to the thread's entry before or after the one at the top of the screen. They follow the same order the ⟨⟨ and ⟩⟩ links gave, and they still go to the next or previous page where the thread continues there.

The keys used to read that order from the thread lines. With the lines gone, each calendar page carries a small list instead: for each thread with an entry on the page, the thread's entries on the page in order, with the entry just before and just after each. For an entry on another page, the page carries a hidden link to it, which the build points at the right page in the same way it pointed the ⟨⟨ ⟩⟩ links. This list adds about 56 KB to February 1965's page and 84 KB to March's, against the 326 KB and 499 KB the lines took.

## The ebook

The calendar's ebook keeps its thread lines, word for word and in the same place in each entry: after the note and any "To:" or "From:" line, before any gloss. The ebook is made from the built pages, which no longer hold the lines, so it now makes them itself from the data, with the same code the pages used.

## Departures from the site's existing style

- `touch-action: manipulation` on the rubric's thread names. Without it, a phone may treat a double tap on a name as a request to zoom, and the second tap would never reach the page. It changes nothing that can be seen.
- The pointer cursor rule for the thread lines, and the rule that darkened a lit thread's line, are removed. Nothing is left for them to apply to.

No colour, size, spacing, font or alignment is new.

## How it was checked

- The arrow keys: on February and March 1965, for every entry and every thread it belongs to (7,218 pairs), the entry the keys now go to was compared with the entry the old ⟨⟨ or ⟩⟩ link went to, link address and all. All match. In a browser, the keys were pressed through five threads on the old page and on the new one, across from February into March and back. Every step landed on the same entry. In the reader (`series.html`, on the test data), one click lights a thread without moving the page, a double click goes to the summary, and the keys step through the thread in the same order as on the calendar's page.
- The taps: a browser script on the new February page, with a mouse on a desktop and with touch on a phone. It checked one tap, a later second tap, a double click and a double tap, a tap on the empty part of the line, a tap on the place and time, Enter on a name, and Ctrl or Cmd with a click. Each did what is described above. A double click leaves no word selected.
- The ebook: for each of the 2,127 entries of February and March 1965, the entry as the ebook takes it from the new page, with its lines put back, was compared with the entry as it took it from the old page. The thread lines match in every one, links and all. Three entries differ elsewhere, in a bill's table, because the data changed between the two builds. An ebook made from the new pages passes the ebook check.
- The unit tests pass. The golden tests' record of the built pages was rewritten for the pages this change shortens (the calendar's, the reader, Names, Threads and Places), and then passed. A later change by another task, D.C.'s place in the "Places:" lines, moves a few of those pages by one byte; its record is that task's to rewrite. `./bib check` ends with no errors.
