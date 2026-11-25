# Audit of the second cleanup patch of the Times entries (c2)

Patch: `inbox/2026-11-25-nyt-cleanup-c2.yaml`, corrected in place. Reader's note: `notes/nyt/cleanup-c2.md` (left as the reader wrote it; where it differs from the patch, the patch and this note stand). Dating rows: `notes/nyt/dating-c2.tsv`, four rows added for the new entries.

## What was read

All five entries were read against the owner's clippings of the *New York Times* of July 6, 1960 (the Drive folder named 1970-07-06), each as a page image: the Hong Kong item under "Ghana Asks 'Bold' Western Aid"; Jorden's story on page 1 and its runover on page 2; Egan's story on page 20, Lawrence's story on page 1 and its runover on page 20, and Sitton's story on page 20 (for Butler's news conference); the Wagner story, no page shown; Handler's story on page 1 and its runover on page 15. Nothing was left unread. OCR was used only to find the items.

## Ops checked, kept, changed, added, struck

Ops checked: 17. Kept as written: 6 (the china edit and its add-words; the soviet-union edit and its Furtseva names op; the nomination and los-angeles edits as to their cites, with the changes below). Changed: 6. Struck: 4. Added by the audit: 7 (3 new entries, a names op, a follows op, and two add-words).

- cal.1960-07-05.china: held. The item has no headline of its own and runs under the Ghana headline; no page shows. Xinhua and Peking are in the series' spelling. No place: the item says only that the announcement was reported in Hong Kong, not where the act was done.
- cal.1960-07-05.cuba-2: two acts in the line already (Agriculture's halt; the State Department's announcement), and the reader added a third (the White House's word on the signing). Split under R17, by an edit with `kind: correct`: the line keeps Agriculture's halt and the quota figure, attributed to the paper; the White House's word is the new cal.1960-07-05.cuba-8; the State Department's announcement, with Herter's absence and the public members, is the new cal.1960-07-05.cuba-9, which takes Dillon and the reader's names and tags. The old line had the agenda from State; the clipping gives it to "informed sources", and the new entry says so. Place Washington on both new entries, by the dateline.
- cal.1960-07-05.elections-1960-los-angeles: Lawrence's pinpoint cut from "at 1, 20" to "at 1": the hearing is on page 1 only. Bishop Gerald H. Kennedy's church (Methodist) added; "nearly ninety" witnesses and Butler's prediction of no floor fight added (both stories give the prediction). The reader's sentence on Butler with reporters struck from this line: Egan says he spoke "after his appearance before the committee", another act (R17). It is the new cal.1960-07-05.elections-1960-los-angeles-7, with `follows:` the hearing and a Check on whether it is the news conference of cal.1960-07-05.democratic-party (Sitton's story). Place Los Angeles.
- cal.1960-07-05.elections-1960-nomination: two acts in the line (Wagner's news conference; the Stevenson pickets, "earlier" that day). Split under R17 by an edit with `kind: correct`; the pickets, with Ira Lesser and their purpose, are the new cal.1960-07-05.elections-1960-nomination-12 (New York), and the news conference takes `follows:` it. The reader's add-words on Lesser struck (it is in the new entry). Wagner's answer on Truman and the delegation's count kept; his words on Stevenson added, which keep Stevenson's name in the line; Kennedy named and tagged.
- cal.1960-07-05.soviet-union: place changed from `[kaprun, villach]` to `kaprun`. The item places the remark at the Kaprun dam, which overrides the Villach dateline (R26a), and a day of travel takes its first stop (places brief, P5). The Villach gazetteer row is struck, being unused. His praise of the dam's builders, and the paper's statement that Kaprun was built largely with United States aid funds, added.
- Checks: none of the five entries had a Check in the old cite form, so nothing to settle.

## Patch-check

0 errors. The warnings are the usual "sets only n" notices and the "one event?" and duplicate notices on the four new entries. All four are distinct acts: the merger should `resolve --take keep` them.

## What is left

- Whether Butler's talk with reporters (los-angeles-7) and his news conference (democratic-party) are one occasion: a Check on the new entry.
- The reader's note `notes/nyt/cleanup-c2.md` still describes the patch before the audit.
