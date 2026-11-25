# Audit: inbox/2026-11-24-nyt-1960-07-leftovers.yaml

The leftovers patch for the *New York Times* of July 3 and July 4, 1960, held against the owner's screenshots of Nov. 23 (Drive folders `1960-07-03` and `1960-07-04`, `notes/nyt/inbox-2026-11-23.tsv`). All 73 screenshots of the two days were downloaded to the scratchpad. Tesseract's text was used only to find the stories. The stories were then read as images, and the images deleted. Audited Nov. 25, 2026, under R0 and the reader's brief.

**Ops checked: 2** (2 `add`). **Ops after the audit: 4** (4 `add`). Each entry was compared with the tree and the ledger for its day in every thread, and with the other inbox patches. The same-day, same-thread warnings of `patch-check` were read one by one: each pair is a distinct act, so `resolve --take keep` at the merge. After the audit: 0 errors, 6 warnings.

## Struck (0)

None.

## Changed (2)

- `cal.1960-07-02.japan-4` (the Hibiya Park rally): the clipping (file 22, Screenshot_20261123-113656) bears out the Council's name, the park, the afternoon, the 100,000 called and the "slightly more than 1,000" who came. The rally's makeup (Government employees, union members and students) moved from the note into `c`, since it says who was called (R33a). The paper does not say whose count the 1,000 is, so "Check: the count, by whose" added (R50). The afternoon band, 03:00Z to 09:00Z for Tokyo, is right.
- `cal.1960-07-02.cuba-10` (the *Jean Jaurès*): the clipping (file 32, Screenshot_20261123-114225) bears out the ship's name, Morro Castle "earlier this week", Matanzas, the cargo, "Monday" and the speculation about arms. July 3, 1960, was a Sunday, so Monday is July 4. The paper gives no day of its own for the call off Morro Castle, so "By July 2" (R15a) is right. The note now says the speculation is the London dispatch's, since the "port officials here" and "shipping circles" of that dispatch are in London, not Havana.

## Held

Everything else in the two ops: the dates, the place keys (`tokyo`, `havana`), the threads, `also: [soviet-union]`, the links, and "page not shown" on both (neither clipping shows a page number).

## Added (2)

The note `leftovers.md` had left three July 4 fragments out as leads. Re-read from the images under R5, R15a and R50:

- `cal.1960-07-04.civil-disorders`: the headline "Festival Closed Because of Rioting", p. 1 (file 1, Screenshot_20261123-152157). It sits over a photograph that the clippings cut off, so the festival, the place and the caption are not shown. A headline reports a dated event, and R15a dates it by the paper: "By July 4". Entered with only what the headline says, and Checks for the festival, the place, who closed it and the day. No `place`, because the clipping gives none. Filed under Civil disorders, the thread for riots.
- `cal.1960-07-04.cyprus-3`: the Denktash fragment, p. 2, top of a column (file 6, Screenshot_20261123-152417). It opens on "demands today", so it reports a dated act, though the act and its actor are cut off. It names Denktash as deputy leader of the Turkish community and calls him the champion of a tougher line in negotiations than Küçük. Entered as "By July 4", with Checks for the act, whose it is and the day. The fragment's "He" is read as Denktash, and the note says so. No `place`, because the dateline is not shown. Küçük is tagged and named. Denktash has no name entry.

Both ids were claimed in the ledger first (`./bib ledger add`).

## Not entered (1)

- The nurses' fragment, p. 1, foot of a column (file 2, Screenshot_20261123-152232). Its one dated item is a nurse shortage of 58 percent "last Oct. 31". In a paper of July 1960 that is Oct. 31, 1959, before the span (R18, out of the brief). The rest describes conditions in the hospitals, with no act and no day. Its head is not in the clippings.

## For the merger

- The four new entries each carry a "one event?" or duplicate warning. Each is distinct from the entries it names: `resolve --take keep`.
- `notes/nyt/1960-07-04.md` still calls the festival headline, the nurses' fragment and the Denktash fragment leads (its lines 14, 15 and 66). This audit was told not to touch that file. The merger should point those lines to the two new entries and to the ruling on the nurses' fragment above.

## For the owner

- The two July 4 entries are thin: each says no more than a headline or the tail of a story shows. They are entered because R0 and R15a say a report dates what it reports and nothing a source in hand dates is a lead. If the owner would rather keep such fragments as leads until the full story is read, the two entries can be struck by that rule.
