# Audit of the Times cleanup, part c3

The patch `inbox/2026-11-25-nyt-cleanup-c3.yaml` (a Sonnet reader's), its note `notes/nyt/cleanup-c3.md` and its dating rows `notes/nyt/dating-c3.tsv`, held to R26a, R19a, R33a, R33b, R5, R17, R25a, R25b, R34, R22 and R18a. Audited Nov. 25, 2026 (Opus).

## What was read

All 41 clippings of the *New York Times* of July 6, 1960 (the Drive folder named 1970-07-06), read as images, and the two clippings of July 3, 1960 that the two July 2 entries cite (files Screenshot_20261123-113656, Johnston's rally story, and Screenshot_20261123-114225, "Soviet Tankers on Way to Cuba"). Every one of the 93 entries was read as it stands (`./bib show`) and held against its item. Nothing was left unread.

## Ops checked

The patch had 93 `edit`s of `n`, 2 rewordings of `c` (the Kanba Michiko respelling), 16 `place` ops with their tag removals, 2 `place-key`s, 10 `add-words`, and 2 `names`. All were checked against the clippings.

Held as written: the cite form in all 93 edits, with author and title as the clippings print them, the paper, the day, and a page only where the clipping shows one or its jump line fixes it. The "Once a Castro Backer" column has no byline. The Peshawar story's page is fixed by the jump line beside it (below). The Lesage item shows no page. Also held: the 16 places, the two new gazetteer keys, the Kanba Michiko respelling (R19a), and 7 of the 10 `add-words`.

## Changed

- `cal.1960-06-22.south-asia`, `-south-asia-2` (Grimes, Peshawar): the clipping shows the story on the page that carries Hamilton's runover "Continued From Page 1", which page 1 sends to page 6. The same clipping holds the Morocco and Dutch items, which the patch cites at 6. Both cites now read "at 6", and the dating rows now say a page shows.
- `cal.1960-05.cuba-2`: the added words had "the *Times* reports". The column says only "it was reported yesterday", so the words now read "By a report of July 5, Castro never set a date ...".
- `cal.1960-07-02.japan-4`: the Council's aim is background about the Council, not the rally's act. It is now a sentence attributed to the paper (R26a).
- `cal.1960-07-06.cuba-2`: the law's terms as added had the interest paid "from a dollar surplus on sugar bought above 3,000,000 tons". The item says the interest is due only if the United States buys at least 3,000,000 tons a year at 5.75 cents a pound or more. Reworded to say that, and to name the Council of Ministers as the law's maker.
- `cal.1960-07-04.soviet-union-3`: the note said Mongolia had no thread, but the entry is now filed under `mongolia`. That sentence is struck. A Check takes its place for the names, which the paper spells its own way and the tree has nowhere else (R19a: a name not identified is written as the source has it, with a Check).
- `cal.1960-07-05.europe-and-the-alliance` (Lesage): the note said Canada had no thread, but the entry is now filed under `canada`. That sentence is struck.
- `cal.1960-07-05.elections-1960-nomination-8`: the line made "Truman recognizes DiSalle 'among the riggers'" a fact. The item gives these as Brown's words ("It is readily apparent that Mr. Truman recognizes..."). Now "Truman, he says, recognizes ...", as `kind: correct`, with a sentence in the note saying so.

## Added: entries that held two acts, split (R17, R25b)

- `cal.1960-07-05.south-asia-4`: the helicopter flight near Chushul and the statement at Srinagar "after the flight" are two acts in two places. The flight keeps the id, now placed at Chushul (a new gazetteer key, `chushul`). The statement is the new entry `cal.1960-07-05.south-asia-5`, placed at Srinagar, with `follows` the flight.
- `cal.1960-07-05.japan-and-korea-far-east`: the parade, which is timed, and the Waldorf-Astoria luncheon ("Later, at a luncheon") are two acts. The parade keeps the id and its hour. The luncheon is the new entry `cal.1960-07-05.japan-and-korea-far-east-5`, with `follows` the parade, the midday band, and the cigarette case the King gave the Mayor (p. 13).
- `cal.1960-07-05.labor-disputes-3`: General Electric's estimate and Hartnett's answer, which the item says was given in Washington, are a statement and its reply. The answer is the new entry `cal.1960-07-05.labor-disputes-4`, placed at Washington, with "Check: the day".
- `cal.1960-07-05.democratic-party-2`: Pauley's charge at Mexico City and Butler's "no comment" at Los Angeles are a statement and its reply. Butler's is the new entry `cal.1960-07-05.democratic-party-6`, placed at Los Angeles.

All four are claimed in the ledger, and each has a row in the dating file. The edits that remove words from a line are `kind: reword` where no number, date or tagged name leaves the line. The parade edit is `kind: correct` because a tagged name leaves with the luncheon; the patch tools have no kind for moving words to a new entry.

## Struck

None.

## What is left

- `cal.1960-07-06.cuba-2` still holds the sugar act and its signing in Washington together with Havana's Law 851. These are separate acts by separate governments. The split is left undone because the line's claim map has six rows that name its third part (the Law 851 sentence), and an `edit` in this patch cannot safely rewrite them. The Aug. 6 and Oct. 1960 nationalization entries also point to this entry for the law. A later pass should split the law into its own entry, placed at Havana, move the *Times* cite and the law's terms with it, fix the rows, and point those entries to the new one.
- Entries left as one, read as a single event: `cal.1960-07-05.elections-1960-nomination-5` (Truman's word to the AP and by telephone, the same day at Independence, the two cites each marked with the part it supports); `cal.1960-07-05.europe-and-the-alliance-federal-republic` (the meeting and the Ministry's word on it); `cal.1960-07-05.testing-2` (the United States' decision and the Western delay, both in Washington); `cal.1960-07-05.cuba-5` (two ambassadors' resignations, reported together).
- `cal.1960-07-05.south-asia-3` still ends with "the Cabinet met twice the week before". That meeting is its own entry, `cal.1960-06-27.south-asia`. The clause could be struck.
- Places left unset where the item does not place the act: the Southern governors' private assurances (`democratic-party-5`), Connor's election (`democratic-party-4`), the *Salzburger Nachrichten* (`soviet-union-3`), Kyushu (no gazetteer key), the editorial, and the earlier acts that the July 5 stories only mention.
- Possible duplicate for the merger: cleanup-b has claimed `cal.1960-07-04.europe-and-the-alliance-federal-republic-2`, "Brucker corrects himself through the Embassy". This patch's `cal.1960-07-05.europe-and-the-alliance-federal-republic-2` is the same Embassy statement.

`./bib patch-check` shows 0 errors. The warnings are "edit sets only n" and the duplicate notices on the four new entries, which are distinct events (`resolve --take keep` at the merge).
