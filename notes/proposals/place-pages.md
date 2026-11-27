# Following a nation, a State, a province or a city

Nov. 26, 2026, about 9:10 p.m. PT. For the owner, on the question of 8:50 p.m.: "Are you sure we shouldn't have threads for Chinese provinces, the several States of the United States, certain municipalities (New York, Chicago, Beijing, Shanghai), and the sovereign nations of the world?"

## The short answer

You should be able to follow every nation, State, province and large city. I would do it with pages that work like thread pages but are built from where each entry happened and whom it concerns, not by making places into threads. The work has started on that default (ruling 66). You can overrule it.

## Why the China pass warned against place threads

A thread is an entry's subject. Each entry has one main thread and may list others under `also:`. The China survey of Nov. 25 asked whether a province or a city could be an entry's main thread. It found that most entries in a province already belong to an episode or a stage (the famine, the Four Cleanups, the Red Guards), so a province thread would take entries away from the episode they belong to. That is why it advised against them. It did not weigh whether you should be able to read a province's entries together. That question it left open.

## Why not make places threads anyway

- Every entry would need its places added to `also:` by hand or by a reading pass: about 59,000 entries.
- A thread's statement, its place in the tree and its rules (no thread beside its own parent) do not fit a place.
- An entry about Laos decided in Washington is about Laos but took place in Washington. A thread cannot say both.

## What the entries already carry

- `place:`, on 31,108 of the 59,260 entries. The gazetteer (`sources/places.yaml`, 1,878 places) gives each place its nation and, in the United States, its State.
- `polity:` tags (40,062), `state:` tags (5,251) and `city:` tags (2,775).
- The visibility register (`sources/polities.yaml`) already gives each person, each place tag and each thread its nation. The build uses it to say which nations each entry concerns.
- The China map gives each place in China its province of 1966.

From these alone, without reading anything, 126 nations, every State and 51 cities with 50 entries or more can each gather their entries. Some examples: China 27,978; the United States 12,800; North Vietnam 2,539; the Soviet Union 1,953; South Vietnam 1,429; Indonesia 495; India 420; Japan 382; Laos 346; Britain 341; Cuba 329; Algeria 269; New York State 1,321; Illinois 1,002; Alabama 380; Peking 8,032; New York City 1,014; Chicago 866; Shanghai 710. 13,209 entries have neither a place nor a nation the data can find. Most of them sit in a thread that names its nation, which will place most of them.

## The default taken (ruling 66)

1. A page for each sovereign nation in `sources/polities.yaml` with entries, each U.S. State, each Chinese province of 1966, and each city with 50 entries or more (New York, Chicago, Peking and Shanghai among them).
2. An entry is on a nation's page if it happened there or concerns that nation (its people, its places, its threads); each line marks which. On a State's, province's or city's page, if it happened there or carries that State's or city's tag.
3. The pages look and work like thread pages: the same layout, day headings, year sections and splits by the page budget, and the same CSS. A new section of the threads' index, "Places", lists them. No new styles beyond what the index needs; every departure will be listed when the preview is shown.
4. Nothing is re-read or re-threaded. The pages are rebuilt from the entries on every build, so they stay right as entries are added.
5. A later pass fills the gaps: a place on entries that lack one, where the line or the note names it; and the tags that are wrong (two entries carry `state:california` and `state:alabama` for `state:ca` and `state:al`; a China entry carried a Vietnam province tag, removed tonight).

## What you see first

A preview of four pages, Laos, Alabama, Shaanxi and Chicago, before the rest are built and before anything reaches the site.

## The dateline and the citation block (the owner, Nov. 26, 9:19 p.m.)

- **The dateline.** A place in an entry's dateline that has a page of its own (a nation, a State, a province, a city) links to that page. The calendar's cross-references, to the Works and to the Names, use one style: the text in its own color with a faint solid underline, darker on hover (`templates/list.html`, the rule for links inside the page; `a.nm` for names). It is not dotted or dashed. The place links take the same rule, so the dateline needs no new style. The dateline itself is not lengthened.
- **The citation block.** A line "Places:" just before "Names:", naming the nations, States, provinces and cities the entry happened in or concerns, each linked to its page, in the same style as the names. It is written by the build from the entry's place, tags and the register, not stored in the entry, so no reader writes it and it cannot go stale.
- Both are added to the preview.

## The tags' codes (the owner's question of 9:19 p.m.)

- **What we have.** The six nations the visibility work began with have short codes (`us`, `ussr`, `prc`, `fr`, `frg`, `uk`), as do a few more (`drv`, `rvn`, `dprk`, `rok`, `roc`, `gdr`, `uar`, `nz`). The other 110 or so have their names spelled out (`polity:indonesia`, `polity:czechoslovakia`, `polity:central-african-republic`), because they were made from the names when the list was seeded. The States use the postal codes (`state:il`). Cities and Vietnam's provinces use spelled-out names.
- **Recommendation.** Use ISO 3166-1's two-letter codes, in lower case, as the standard stood in its first edition of 1974, the last year of the span. That edition still has the states of the time, among them the two Germanys, the Soviet Union, Czechoslovakia, Yugoslavia and both Vietnams; each code is to be confirmed against the standard's text when the change is made. Our own additions, of three letters, for the states that were gone before 1974 (the United Arab Republic of Egypt and Syria, Tanganyika, Zanzibar, the Federation of Rhodesia and Nyasaland, the Mali Federation) and for the movements and bodies that are not states (the National Liberation Front, the Pathet Lao, the UN, NATO and the rest keep their present short names). The standard's code for the German Democratic Republic is `dd`, not `ddr`; I would keep the standard's code.
- **Would readers find them hard?** No. `./bib check` refuses a tag that is not in the list, `sources/polities.yaml` gives each code its name, and patch-check can accept an old spelled-out tag and turn it into the code, so nobody has to remember the list.
- **Cities and Vietnam's provinces** keep their spelled-out names: there is no short standard for them that a reader would know.
- **When.** After the place pages are in, as one change made by a script (the tags, the register and the code that names the six), the old names kept as aliases so old links and patches still work. Ruling 67.

## Conflicts, checked before the change (the owner's question of 9:24 p.m.)

The two- and three-letter scheme does not rule out conflicts. Within the nations' tags no two nations can share a code, because the standard gives each one its own and our additions have three letters. But there are four other kinds of conflict, and a script can find them all before anything is renamed. It reads nothing and changes nothing.

1. **The same letters in another kind of tag.** The States' postal codes and the nations' codes are often the same two letters: `al` is Alabama and Albania, `ca` California and Canada, `de` Delaware and the Federal Republic, `ga` Georgia and Gabon, `id` Idaho and Indonesia, `il` Illinois and Israel, `in` Indiana and India, `la` Louisiana and Laos, `pa` Pennsylvania and Panama, `va` Virginia and the Vatican, and more. The tags' kinds keep them apart (`state:la`, `polity:la`), so the build cannot mix them up, but a reader can write the wrong kind and `check` would accept it. So `check` will warn where a tag does not fit the entry: a `state:` tag on an entry that happened outside the United States and concerns no State, or a nation's tag that no place, person or thread of the entry supports.
2. **Codes that meant something else later.** The 1974 edition gave codes that were later dropped or given to other countries: `cs` was Czechoslovakia and later Serbia and Montenegro; `vn` was the Republic of Vietnam in Saigon, and after 1976 the unified Vietnam; `vd` was the Democratic Republic in Hanoi; `su` the Soviet Union; `dd` the German Democratic Republic; `dy` Dahomey; `hv` Upper Volta; `bu` Burma; `zr` Zaire (the Congo of Léopoldville, renamed only in 1971). A reader who knows today's codes could misread them, above all `vn`. So the register will give each code its name for the span, and the script will list every code that the standard later reassigned, for you to rule on one by one. For the two Vietnams I would keep our own `drv` and `rvn`, which every reader of the series already knows, rather than the standard's `vd` and `vn`.
3. **States whose name or form changed in the span.** Some states were joined, split or renamed between 1960 and 1974: Egypt was the United Arab Republic (with Syria to 1961, alone to 1971); Tanganyika and Zanzibar became Tanzania in 1964; Malaya became Malaysia in 1963, and Singapore left it in 1965; the Congo of Léopoldville became Zaire. The script lists each one, with the entries that fall on each side of the change, so the rule (one code for the state throughout, or one code for each form) can be set before the rename.
4. **Our own short names.** The bodies and movements that are not states (`un`, `nato`, `oas`, `eec`, `oecd`, `imf`, `nlf`, `pathet-lao`) and the exceptions already in use (`uk`, which the standard reserves for the United Kingdom though its code is `gb`) are checked against the standard's list, so that none of them is a state's code.

The script writes its findings to a note for you before the rename runs. Where a finding needs a ruling, the default taken is the one above, recorded as ruling 67 is.
