# Audit of the patch 2026-11-25-via-bare (Opus, Nov. 25, 2026)

## What I read

- The reader's brief whole, CLAUDE.md, `notes/guide/brief.md` and `notes/guide/reading-a-copy.md`.
- The patch `inbox/2026-11-25-via-bare.yaml` as the session wrote it: one `cite` op.
- The entry `cal.1966-06-14.vietnam-air-war` in full, with its note and its claim map (`./bib show`, `./bib claims show`).
- FRUS 1964–68, IV, doc. 156, whole, with its three notes, in `sources/frus-text/1966-06.json.xz` and on history.state.gov (printed pp. 426–428). The two texts agree.
- Rows 656–657 of `notes/via-read/rule-2026-11-25.tsv` and ruling 53 of `notes/owner-rulings.md`.
- Hansard for the Commons, Feb. 8, 1966, the debate on South and South-East Asia (vol. 724, cc. 224–347), at api.parliament.uk, for the words doc. 156 n.3 quotes.
- The entries of June 2, 3, 6, 10, 14 and 23, 1966, and Feb. 8, 1966, and the ledger for those days.

## The line, part by part, against the document

- Part 1 ("Johnson to Wilson, after Rusk's private talk with him: "I see no way of avoiding such action," the corridor through Laos, the buildup, Cambodia, no interest in peace in Hanoi"): borne out. The document gives the four reasons in that order.
- Part 2 (""not ... an air assault on civilian centers.""): borne out, word for word with the ellipsis.
- "Not to "speak in terms of disassociation."": borne out. Johnson writes that he "earnestly hope[s]" Wilson will not find it necessary.
- "A visit late in July.": not borne out as written. The document says "mid- or late July," the dates left open, and "mid-July appears to be a mutually convenient time." The line had dropped "mid-".

## The patch's one op

- The words in `on:` were the whole of part 3, two sentences. The document bears out the first and not the second as written.
- The op was not in the house form. `cite` takes a card; a linked record is cited by a `src` row on its address. `patch-check` refused the op as written ("cite needs a card with a pinpoint").
- The entry already cites the document, by the same link, for parts 1 and 2. The right op extends that citation to the new parts. It does not add a second item to the note.
- The item's words are the entry's own ("FRUS 1964–68, IV, doc. 156"). R28 would add the volume's title ("Vietnam, 1966"). I kept the entry's form so that the note prints one item, not two.

## What I changed

- An `edit` (`kind: correct`, base 3349c51d): "A visit late in July." becomes "A visit in mid- or late July." The note gains the sentence that names the record: the message itself gives "mid- or late July." This is R22: the message is the record, and it settles the words. The brief asked for a "Check:" where the line and the document disagree; after the correction they no longer disagree, so there is no Check.
- Two `src` ops in place of the `cite`: the document's link for "Not to "speak in terms of disassociation."" and for "A visit in mid- or late July." Each sentence is now its own part.
- Four `add-words` ops, each cited to the document alone (R33a): the target, the oil installations of Hanoi and Haiphong, orders not yet issued; the seven points Johnson asks Wilson to include if he must dissociate (four named; "Peiping" written Peking, R19a); "a good deal of blue sky" between the visit and any action, nothing before mid-July, the dates left open; the drafting by Rusk, review by Johnson, redrafting by Rusk and Rostow, and the information copy to McNamara (from n.1; the note gains a label, "The drafting and the copy to McNamara: doc. 156 n.1").
- A `names` op: Rostow and McNamara, named and tagged.
- Four new entries, each claimed in the ledger first, for dated acts the document's text and notes report (R5, R8):
  - `cal.1966-02-08.vietnam-air-war`: Wilson in the Commons, the words n.3 quotes. Cited first to Hansard, c. 259, which I read. Hansard reads "Hanoi or Haiphong"; Bruce's report in n.3 reads "Hanoi and Haiphong". The line follows Hansard and the note carries a "Check:". Wilson rose at 4.48 p.m.; the time is set to his speech's start.
  - `cal.1966-06-02.vietnam-air-war-2`: London 5768, Bruce reporting those words (n.3). The telegram itself is behind "To check:". `patch-check` warns that June 2 already holds `cal.1966-06-02.vietnam-air-war` (Wheeler to Sharp and Westmoreland, JCS 3086). It is a different act; the merger should take `keep`.
  - `cal.1966-06-10.vietnam-air-war`: Rusk with Wilson in London (n.2 gives the day and the place), by Johnson's account of Rusk's report: the oil strikes, the points on dissociation, the "revival of SEATO", Rhodesia and the maritime strike.
  - `cal.1966-06-14.africa`: "By June 14", Johnson suggests to Senghor a visit July 11–13, with "Check: the day" (R15a). Tagged `ok:fields-place`: Washington in the line is where Senghor would go, not where the act was done.
- `./bib patch-check` on the patch: 0 errors, 2 warnings (the June 2 duplicate flag, above). I merged it in a scratch copy of the tree only, to read the parts and footnotes; nothing was merged in the repository.

## The day's order (R25c)

I printed June 1966 with the patch merged in the scratch copy and read June 2, 10 and 14 and Feb. 8. No link is shown by the entries' words or sources. The Senghor suggestion is dated only "by June 14", so it has no order against the message.

## Left as it was, and why

- The rest of the message is not in the line: monsoon fighting and casualties; solidarity asked despite Wilson's words in the Commons; SEATO; Britain as co-chairman not to stand aside; the Geneva Accords; best wishes on Rhodesia and the maritime strike. I left them out to keep the line within the house's compression. A later reader may add any of them by `add-words`.
- The note cites Gibbons, IV, 370 twice, once bare and once with a parenthetical; the second item has no row in the map. I did not read Gibbons, so I did not touch these.
- The via row (Gibbons 370 n.58) now names parts 1, 2, 4 and 5. Since ruling 53 it is no longer printed as a citation, so nothing turns on it.

## Passed over

- n.1: Rostow's memorandum to Read, June 14, that the message had been sent and an information copy had gone to McNamara. A transmittal (R18). The information copy is in the line.

## Leads

- Foreign: the message names Pompidou's visit to London, July 6–8, Wilson's possible visit to Moscow, July 9–10, and Johnson's week away around July 4, as plans. The document does not report them as done; a record of each visit is needed (Hansard, the British press, the Daily Diary).

## What I did not do

No merge, build, commit or push in the repository. Nothing in `lists/` edited. The copies of the FRUS page and of Hansard, and the scratch tree, were deleted.
