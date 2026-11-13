# Batch 12: the newspapers the owner reads (Nov. 12, 2026, evening)

The owner reads the *New York Times* day by day (TimesMachine) and sends the items of interest as clippings, a PDF each: the image of the item and a caption line, "Published: February 18, 1960". The readers enter them by the card (`notes/briefs/reader-card.md`), as for any source, with what follows. Never read `build/` or a whole list file.

## Reading a clipping

- The PDF is an image: open it with the Read tool (it shows the page), read the item whole, the headline, the dateline, the byline. Its day is the caption's ("Published: ..."); its page is on the clipping where shown (else no pinpoint).
- The cite, the house form (as `tools/works/newspaper_cites.py` writes it): `[*New York Times*, Feb. 18, 1960](https://timesmachine.nytimes.com/timesmachine/1960/02/18/issue.html), at 1` (the page as printed, "at 1", "at 24"; a section-letter page "at E1"). A headline in quotation marks where it helps ("Byrd Silent on Ticket").
- What the item reports is dated by the event's day, not the paper's: a speech of Sept. 6 reported Sept. 7 is an entry of Sept. 6 (in the calendar already? cite the paper there; not? an entry of Sept. 6, the paper its source). The story itself is an entry on the paper's day only where the publication is the event (a leak, an interview, an editorial with a consequence, a paper's poll; the card's press lines) or where it reports a standing condition (below).
- Search first, every item (`./bib find WORDS -l cal --since D --until D`, a few days around); many will be in: cite the paper there, units by the card (`./bib claims show ID`; '?' where the item does not state a unit whole), a `variant` where it says otherwise.

## Standing conditions: an entry on the paper's day (the owner, Nov. 12, 2026)

A condition of public importance that has no day of its own, reported as such: a senator who has not endorsed the ticket ("the failure of Senator Harry F. Byrd of Virginia to endorse the Democratic ticket"), a governor not yet committed, a bill still in committee, a principal's silence. The report makes it a matter of public knowledge on the paper's day; the entry goes on that day, not on the day the condition ends.

- `c`: "As the *Times* reports it: Byrd of Virginia has not endorsed the Democratic ticket; neither of Georgia's Senators, Russell or Talmadge, has spoken for Kennedy." The condition, as the paper states it; no inference beyond it.
- `tags`: `form:state` (it renders as a condition, not an act), the `name:` tags of the persons, `state:` tags.
- `thread`: the condition's (the campaign's thread for an endorsement).
- `n`: the paper, linked, at the page. A later report of the same condition ("still silent") is its own entry on its own day, its note "See [[the earlier]]". The day the condition ends (an endorsement, a first appearance) is an event: an entry, pointing back to the state entries.
- Not a standing condition: what the paper predicts, guesses or argues; a columnist's view; a condition of no public importance.

## Patches and the report

One patch for each paper's day or two, `inbox/2026-11-12-b12-nyt-<YYYYMMDD>.yaml`; new ids by `./bib new-id` and `./bib ledger add ... <patch>`; `./bib patch-check` to 0 errors. Do not merge or commit; append to the ledger only. Last message: per clipping, its ruling (an entry, a cite under ID, a state entry, passed over and why), the counts, and anything doubtful.
