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
