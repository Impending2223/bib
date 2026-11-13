# Batch 12: the foreign skeletons, USSR and DRV (Nov. 12, 2026, evening)

The owner, Nov. 12, 2026: the October 1962 pilot is accepted; the threads `soviet-leadership` (`soviet-union-leadership`), `britain`, `federal-republic`, `prc-leadership` (`china-leadership`) made; the DRV's records first ("Shouldn't we have the DRV ready to go?"). The plan: `notes/proposals/foreign-leadership-reading.md`. The method is the pilot's (`notes/briefs/batch10.md`, item 4) on a year at a time.

## What is an entry

A dated act of a foreign government's or party's leadership that its own record treats as an event (R5): a session of the Presidium or the Politburo and its decisions, a plenum, a resolution adopted, a directive sent, a speech or report to a party body, a conversation between principals, a public statement. One event an entry: a session is one entry, its decisions in `c` in the session's order (the important ones; the routine named by a word: "and personnel"); a resolution adopted at a session and printed separately is cited on the session's entry, not entered again, unless its day differs. Already in the calendar (the pilot's October 1962; the Soviet entries of earlier batches, `./bib find -l cal --thread soviet-union`, `--thread vietnam-hanoi`): cite there.

## The form

- `thread`: `soviet-union-leadership` for the Soviet leadership's acts (another thread in `also` where the act bears on it: `berlin-and-vienna`, `cuba`, `vietnam`); `vietnam-hanoi` for the DRV's party and government.
- `c`: the polity's actors by name, plainly ("The Presidium: ..."; "The Politburo, Hanoi: ..."); quotations sparse, in the original with a translation in parentheses only where the words matter.
- `tags`: `polity:ussr` or `polity:drv`; `name:` for each person with a name entry (`./bib find -l kja SURNAME`, and the foreign names of Nov. 11, `kja.who.*`); a person with no entry is named in `c` and in "Names:" but not tagged (list them in your report).
- `n`: the volume's cite with the language's own title in italics, the page and the document's own number or heading: `[[w.prezidium-tsk-kpss-1954]], I, 419 (Protocol 258, Malin's notes)`; the Party's documents, `*Văn kiện Đảng toàn tập*, vol. 21, 120 (Nghị quyết ..., No. 98-NQ/TW)` until its card is made (make it first, `./bib works new`: a series card, *Văn kiện Đảng toàn tập* (Chính trị quốc gia, 1998–2007), and cite the volume in it). "Made public: 2003." (the volume's year) for a record secret at the time.
- Visibility follows (the spec, `notes/proposals/visibility-spec.md`): nothing to write by hand.

## The Party's documents (DRV)

The Drive's PDFs carry a text layer in the old TCVN3 font encoding: convert with `python3 -I tools/vn/vkd2txt.py IN.pdf OUT.txt [FIRST LAST]` (headings in the capitals font come out lower-case with capital marks: read them as capitals). Some volumes print two book pages to a PDF page: say so, and give the book's page. Read the volume's table of contents first (at the end or the start), list every document with its date, then read each for its entry. Vietnamese with full diacritics in names (CLAUDE.md, the house form).

## Patches

`inbox/2026-11-12-b12-<polity>-<YYYY>.yaml`; new ids `./bib new-id`, `./bib ledger add ... <patch>`; `./bib patch-check` to 0 errors. A book-check section in the work's file (`notes/book-checks/<card-short>.md`; append only, under a heading of your year). Do not merge or commit. Last message: the counts, the pages read, the persons with no name entry, the documents passed over and why, anything doubtful.

## The owner's rulings of Nov. 12, evening

- The DRV's routine Party circulars stay entries ("we just don't know much about what's happening up there, so we should keep what few clues we have"); commemorations and provincial matters are still passed over and listed.
- A foreign person on FRUS's lists of persons has a name entry (the Names pages: `sources/frus-names/persons.json`): tag `name:<key>` with the key the calendar already uses for the person (`./bib find -t name:<surname>...`), else the FRUS key; where FRUS has several persons of the surname, tag only the one the record names (Marshal G. K. Zhukov is not Yuri Zhukov of *Pravda*).

