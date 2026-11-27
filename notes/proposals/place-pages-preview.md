# The place pages: a preview of four

Nov. 27, 2026. For the owner. This follows `notes/proposals/place-pages.md` and ruling 66.

## Where to look

The four pages are in `notes/proposals/place-preview/`: `places-laos.html`, `places-alabama.html`, `places-shaanxi.html` and `places-chicago.html`. The threads' index with its new section "Places" is beside them, as `threads.html` (go to the end, or to `threads.html#places`).

Open the folder through a small web server, as the guide for the maps says (`npx http-server notes/proposals/place-preview`). Opened straight from the disk, the pages read, but the maps do not draw.

The folder holds what the pages need to show: their styles, their scripts, and the map data for Laos and Shaanxi. It leaves out the map's relief and climate layers, which are large (about 55 MB). Those two boxes do nothing in the preview. The folder is 16 MB.

Links from the preview to pages outside it (the calendar, the threads, the other places) do not work in the folder. They will on the site.

## What the four pages hold

Each page lists its entries in the calendar's order, under the same year, month and day headings a thread's page has. Each entry is shown as the calendar shows it.

### Laos: 751 entries

- 126 took place in Laos. Their `place:` is a place in Laos, such as Vientiane or the Plain of Jars.
- 442 concern Laos by their tags: a Lao person named (Souvanna Phouma, Phoumi Nosavan, Souphanouvong), a place in Laos tagged, or the tag `polity:laos`.
- 183 concern Laos only by their thread. They have no tag that names any nation, and their thread is one the register gives to Laos (the Laos thread gives Laos, the United States and North Vietnam).
- Each line says which: "In Laos" or "About Laos", at the head of the small line above the entry, before the thread's name.
- The map of Indochina stands at the head, with only this page's entries placed on it (35 entries at 9 places).
- The proposal guessed 346 entries. That guess counted only an entry's place and its `polity:` tag. This page also counts the people and the threads, as ruling 66 says.

### Alabama: 386 entries

- 306 took place in Alabama: Birmingham, Montgomery, Selma, Tuscaloosa and the rest.
- 77 carry the tag `state:al` but took place elsewhere or have no place (a hearing in Washington on Alabama, a ruling of the Supreme Court).
- 3 carry the tag of a city in Alabama but not the State's own tag.
- The page has no map, since neither map covers the United States.

### Shaanxi: 393 entries

- All 393 took place in Shaanxi as it was in 1966: 311 in Xi'an, 15 in Yan'an, 20 in the province as a whole, the rest in its other places.
- No entry carries a tag for a Chinese province, so the page comes from `place:` alone.
- Most are from 1965 (259) and from the Four Cleanups thread (226). That reflects what has been read, not Shaanxi's history.
- The map of China stands at the head. A few dots lie outside Shaanxi (Peking, Chengdu, Guiyang): those entries have two places, one of them in Shaanxi.

### Chicago: 866 entries

- 806 took place in Chicago.
- 60 carry the tag `city:chicago` but took place elsewhere.
- Most are from 1966 (208) and 1968 (210).

### Sizes

The pages are 1.8 MB (Laos), 1.3 MB (Alabama), 0.9 MB (Shaanxi) and 2.3 MB (Chicago). All are under the 5 MB budget, so none of the four is in parts. A larger page (China, the United States, Peking, Washington) is cut into parts by date, as a large thread's page is. The tests check that on a small budget.

## The whole set

The code makes 248 pages: 119 nations, 50 States, 28 provinces and 51 cities. The cities are the places of the gazetteer with 50 entries or more. Some of these are not cities: Beidaihe, Lushan, the LBJ Ranch, Hyannis Port. They are kept because the rule is the gazetteer's, not a list.

The choices made along the way are in ruling 68 (`notes/owner-rulings.md`). In short: the Pathet Lao's entries go to the Laos page; the Front's to North Vietnam's; Washington, D.C., is a city, not a State; Peking and Shanghai each have one page, the province's.

## Every change from the thread page's style and layout

The pages use the thread page's own code for the entries, the headings, the parts, the map and the styles. No new CSS was written. These are the differences, each with its reason.

1. No statement under the name. A thread has a statement; a place has none.
2. The grey line under the name says what the page holds and why, in place of the thread's line. It links to "All places" only. A place has no parent, no subthreads and no entry in the calendar's thread index to link to.
3. On a nation's page, the small capital line above each entry begins with "In Laos" or "About Laos", then the thread's name, in the same type. Ruling 66 asks that each line say which. The State, province and city pages carry no such mark, as the ruling asks it only of nations.
4. The map at the head shows only the page's own entries. A thread's map picks its entries by thread; a place's page has no thread, so the page hands the map the list of its entries. This took three lines in the map's script (`tools/bib/vnmap.js`). The figure, its controls and its look are the same.
5. The threads' index ends with a new section, "Places", under its own heading. It has four smaller headings (Nations; States; Provinces of China, 1966; Cities). Each list uses the index's own list markup. A place has no statement, so its line is its name and its count only.
6. The page's title in the browser is "Places: Laos", in the pattern of "Threads: Laos". The address is `places-laos.html`; a State's is by its name, `places-new-york-state.html`.

## What needs fixing in the data (not done here)

- The register names New Zealand "Nz" (`sources/polities.yaml`). Its page will be titled "Nz" until that is changed.
- Two entries carry `state:california` and `state:alabama` for `state:ca` and `state:al`. The pages read either form, so these entries are not lost.
- An entry whose place is tagged (`place:vientiane`) but which has no `place:` field is marked "About Laos", not "In Laos". The later pass that fills `place:` will move such entries.

## What is not done yet

- The code is not on `main`, so nothing has reached the site.
- The full set of 248 pages has not been built. `./bib build places` builds them, and so does the full build. The first build of a large page (China, the United States) renders it twice: once whole, to measure it, and once in parts. It keeps the parts in `.cache`, and `./bib pages --plan` writes them into `pages.yaml`, so that later builds render them once and their addresses stay fixed. This adds time to the full build; I have not measured how much.
- The front page, the reader's drawer and the calendar's thread list do not link to the place pages yet. Only the threads' index does.
