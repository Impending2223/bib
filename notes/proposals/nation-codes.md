# The nations' codes (ruling 67)

The owner asked, on Nov. 26, 2026, why the nations' tags spell out their names when a short standard code would do. Ruling 67 took ISO 3166-1's two-letter codes, as the standard stood in its first edition of 1974, in lower case. It keeps the short forms the series already writes, and it keeps the old names as aliases. This note gives the table of codes, the places where two things could be confused, the default taken for each, and what the script changes.

The script is `tools/places/recode.py`. It has not been run on the data. It will be run when no patch waits in `inbox/`.

## The rule

- A nation takes the standard's code for the state as it stood in 1974.
- The short forms the ruling names stay: `ussr`, `prc`, `uar`, `uk`. Three of the old ids are already the standard's code: `us`, `fr`, `nz`.
- Each half of a divided state keeps the short form of its own name: `rok` and `dprk`, `rvn` and `drv`, `roc` and `prc`.
- Germany is as the owner ruled: `de` for the Federal Republic, `ddr` for the Democratic Republic.
- A movement or an organization keeps its id: `nlf`, `pathet-lao`, `un`, `nato`, `oas`, `eec`, `oecd`, `imf`.
- A state gone before 1974 takes three letters of our own.
- The old id stays in the register as an alias. A tag, a link or a patch that uses it still means the same nation.

## The table

The register has 129 polities. 21 keep their id, and 108 take a new code.

### The polities that keep their id

| Id | Why it stays |
|---|---|
| `us` | The standard's code. |
| `ussr` | A short form the ruling keeps (the standard's SU). |
| `prc` | A half of a divided state, the short form of its own name (the standard's CN). |
| `fr` | The standard's code. |
| `uk` | A short form the ruling keeps (the standard's GB). |
| `drv` | A half of a divided state (the standard's VD). |
| `srv` | A state formed in 1976, after the standard of 1974; the series' short form beside drv and rvn. |
| `rvn` | A half of a divided state (the standard's VN). |
| `nlf` | A movement, not a state. |
| `roc` | A half of a divided state (the standard's TW). |
| `rok` | A half of a divided state (the standard's KR). |
| `dprk` | A half of a divided state (the standard's KP). |
| `pathet-lao` | A movement, not a state. |
| `uar` | A short form the ruling keeps (Egypt from Sept. 1971; the standard's EG). |
| `un` | An organization. |
| `nato` | An organization. |
| `oas` | An organization. |
| `eec` | An organization. |
| `oecd` | An organization. |
| `imf` | An organization. |
| `nz` | The standard's code. |

### The polities that take a new code

| Now | New | Why |
|---|---|---|
| `frg` | `de` | The standard's code, as the owner ruled for the Federal Republic. |
| `gdr` | `ddr` | The owner's ruling (the standard's DD). |
| `cuba` | `cu` | The standard's code. |
| `laos` | `la` | The standard's code. |
| `cambodia` | `kh` | The standard's code (the Khmer Republic from Oct. 1970). |
| `afghanistan` | `af` | The standard's code. |
| `albania` | `al` | The standard's code. |
| `algeria` | `dz` | The standard's code. |
| `argentina` | `ar` | The standard's code. |
| `australia` | `au` | The standard's code. |
| `austria` | `at` | The standard's code. |
| `belgium` | `be` | The standard's code. |
| `bolivia` | `bo` | The standard's code. |
| `brazil` | `br` | The standard's code. |
| `bulgaria` | `bg` | The standard's code. |
| `burma` | `bu` | The standard's code of 1974 (dropped in 1989 for MM). |
| `burundi` | `bi` | The standard's code. |
| `cameroon` | `cm` | The standard's code. |
| `canada` | `ca` | The standard's code. |
| `central-african-republic` | `cf` | The standard's code. |
| `ceylon` | `lk` | The standard's code (Sri Lanka from May 1972). |
| `chad` | `td` | The standard's code. |
| `chile` | `cl` | The standard's code. |
| `colombia` | `co` | The standard's code. |
| `congo` | `zr` | The standard's code of 1974, Zaire's (the name from Oct. 1971; today's CD). |
| `congo-brazzaville` | `cg` | The standard's code. |
| `costa-rica` | `cr` | The standard's code. |
| `cyprus` | `cy` | The standard's code. |
| `czechoslovakia` | `cs` | The standard's code of 1974 (given to Serbia and Montenegro, 2003-06). |
| `dahomey` | `dy` | The standard's code of 1974 (Benin from 1975: BJ). |
| `denmark` | `dk` | The standard's code. |
| `dominican-republic` | `do` | The standard's code. |
| `ecuador` | `ec` | The standard's code. |
| `el-salvador` | `sv` | The standard's code. |
| `ethiopia` | `et` | The standard's code. |
| `finland` | `fi` | The standard's code. |
| `gabon` | `ga` | The standard's code. |
| `ghana` | `gh` | The standard's code. |
| `greece` | `gr` | The standard's code. |
| `guatemala` | `gt` | The standard's code. |
| `guinea` | `gn` | The standard's code. |
| `guyana` | `gy` | The standard's code (British Guiana to May 1966). |
| `honduras` | `hn` | The standard's code. |
| `hungary` | `hu` | The standard's code. |
| `iceland` | `is` | The standard's code. |
| `india` | `in` | The standard's code. |
| `indonesia` | `id` | The standard's code. |
| `iran` | `ir` | The standard's code. |
| `iraq` | `iq` | The standard's code. |
| `ireland` | `ie` | The standard's code. |
| `israel` | `il` | The standard's code. |
| `italy` | `it` | The standard's code. |
| `ivory-coast` | `ci` | The standard's code. |
| `japan` | `jp` | The standard's code. |
| `jordan` | `jo` | The standard's code. |
| `kenya` | `ke` | The standard's code. |
| `kuwait` | `kw` | The standard's code. |
| `lebanon` | `lb` | The standard's code. |
| `liberia` | `lr` | The standard's code. |
| `libya` | `ly` | The standard's code. |
| `luxembourg` | `lu` | The standard's code. |
| `malaysia` | `my` | The standard's code (Malaya to Sept. 1963). |
| `mali` | `ml` | The standard's code (the Mali Federation to Aug. 1960). |
| `mauritania` | `mr` | The standard's code. |
| `mexico` | `mx` | The standard's code. |
| `mongolia` | `mn` | The standard's code. |
| `morocco` | `ma` | The standard's code. |
| `nepal` | `np` | The standard's code. |
| `netherlands` | `nl` | The standard's code. |
| `nicaragua` | `ni` | The standard's code. |
| `niger` | `ne` | The standard's code. |
| `nigeria` | `ng` | The standard's code. |
| `norway` | `no` | The standard's code (quoted in YAML: STYLE 3). |
| `pakistan` | `pk` | The standard's code (East Pakistan Bangladesh from 1971). |
| `panama` | `pa` | The standard's code. |
| `paraguay` | `py` | The standard's code. |
| `peru` | `pe` | The standard's code. |
| `philippines` | `ph` | The standard's code. |
| `poland` | `pl` | The standard's code. |
| `portugal` | `pt` | The standard's code. |
| `rhodesia` | `rh` | The standard's code of 1974, Southern Rhodesia's (Zimbabwe from 1980: ZW). |
| `romania` | `ro` | The standard's code. |
| `saudi-arabia` | `sa` | The standard's code. |
| `senegal` | `sn` | The standard's code. |
| `sierra-leone` | `sl` | The standard's code. |
| `singapore` | `sg` | The standard's code (in Malaysia, Sept. 1963-Aug. 1965). |
| `somalia` | `so` | The standard's code. |
| `south-africa` | `za` | The standard's code. |
| `south-yemen` | `yd` | The standard's code of 1974, Democratic Yemen's (the PDRY from 1970). |
| `sudan` | `sd` | The standard's code. |
| `spain` | `es` | The standard's code. |
| `sweden` | `se` | The standard's code. |
| `switzerland` | `ch` | The standard's code. |
| `syria` | `sy` | The standard's code (in the UAR to Sept. 1961). |
| `tanzania` | `tz` | The standard's code (Tanganyika and Zanzibar to Apr. 1964). |
| `thailand` | `th` | The standard's code. |
| `togo` | `tg` | The standard's code. |
| `tunisia` | `tn` | The standard's code. |
| `turkey` | `tr` | The standard's code. |
| `uganda` | `ug` | The standard's code. |
| `upper-volta` | `hv` | The standard's code of 1974 (Burkina Faso from 1984: BF). |
| `uruguay` | `uy` | The standard's code. |
| `vatican` | `va` | The standard's code. |
| `venezuela` | `ve` | The standard's code. |
| `western-samoa` | `ws` | The standard's code. |
| `yemen` | `ye` | The standard's code (the Yemen Arab Republic). |
| `yugoslavia` | `yu` | The standard's code of 1974 (dropped in 2003). |
| `zambia` | `zm` | The standard's code (Northern Rhodesia to Oct. 1964). |

### Ids with no row in the register

The code and the source registry use ten more ids that have no row in the register. The script gives them codes by the same rule, so that a row added later already has its code. They need no alias, since nothing in the calendar is tagged with them.

| Now | New | What it is |
|---|---|---|
| `malawi` | `mw` | Malawi, in the visibility pass's list of words. |
| `madagascar` | `mg` | Madagascar, the same. |
| `rwanda` | `rw` | Rwanda, the same. |
| `trinidad` | `tt` | Trinidad and Tobago, the same. |
| `malta` | `mt` | Malta, the same. |
| `bahrain` | `bh` | Bahrain, the same. |
| `oman` | `om` | Oman, the same. |
| `haiti` | `ht` | Haiti, the same. |
| `jamaica` | `jm` | Jamaica, the same. |
| `south-arabia` | `fsa` | The Federation of South Arabia, gone in 1967: three letters, as the ruling gives a state gone before 1974. Two FRUS documents name it as a party. |

## Where two things could be confused, and the default taken

1. **Two polities with one code.** None. Every new code is different, and no new code is the old id of another polity.
2. **A new code that is already another polity's id or alias.** None.
3. **The same letters as a State's postal code.** Seventeen codes are also a State's code: `al` (Albania, Alabama), `ar` (Argentina, Arkansas), `ca` (Canada, California), `co` (Colombia, Colorado), `de` (West Germany, Delaware), `ga` (Gabon, Georgia), `id` (Indonesia, Idaho), `il` (Israel, Illinois), `in` (India, Indiana), `la` (Laos, Louisiana), `ma` (Morocco, Massachusetts), `mn` (Mongolia, Minnesota), `ne` (Niger, Nebraska), `pa` (Panama, Pennsylvania), `sd` (Sudan, South Dakota), `tn` (Tunisia, Tennessee), `va` (the Vatican, Virginia). Default: keep both. The kind of tag keeps them apart (`polity:la` is Laos, `state:la` is Louisiana), `check` warns on a place tag that nothing in the entry supports, and `patch-check` prints the name of each place tag a patch adds.
4. **The same letters as a city, a place or a province.** None. No city, place or province key is a new code. Two cities have a nation's old id as their key: Luxembourg and Singapore. Default: they stay on the nation's page, as they are now. The code reads the old id as the nation's.
5. **A thread with the nation's old id as its name.** Six threads have one: `cuba`, `laos`, `congo`, `cyprus`, `indonesia`, `japan`. Default: the threads keep their names. Only the nation's tag changes, so `thread: cuba` and `polity:cu` will appear on the same entry.
6. **The organizations.** `un`, `nato`, `oas`, `eec`, `oecd` and `imf` stay as they are. None of them is a state's code in the standard.
7. **Codes the standard later dropped or gave to another country.** `bu` (Burma; later MM), `cs` (Czechoslovakia; later Serbia and Montenegro), `dy` (Dahomey; later Benin, BJ), `hv` (Upper Volta; later Burkina Faso, BF), `rh` (Rhodesia; later Zimbabwe, ZW), `yd` (South Yemen; dropped in 1990), `yu` (Yugoslavia; dropped in 2003), `zr` (the Congo of Léopoldville; later CD). Default: the code of 1974, as the ruling says. The register gives each code its name for the span, and `patch-check` prints it.
8. **The Congo.** Its code of 1974 is Zaire's, `zr`, though the calendar calls it "Congo" for most of the span and the state took the name Zaire only in October 1971. Default: `zr`, by the ruling's rule of 1974. Today's code, `cd`, would be the other choice.
9. **States whose name or shape changed within 1960 to 1974.** Cambodia became the Khmer Republic in 1970 (`kh`). Ceylon became Sri Lanka in 1972 (`lk`). The Congo became Zaire in 1971 (`zr`). Egypt dropped the name United Arab Republic in 1971 (`uar`, kept by the ruling). Malaya became Malaysia in 1963, and Singapore left it in 1965 (`my`, `sg`). Tanganyika and Zanzibar became Tanzania in 1964 (`tz`). Syria left the United Arab Republic in 1961 (`sy`). Northern Rhodesia became Zambia in 1964 (`zm`). British Guiana became Guyana in 1966 (`gy`). The Mali Federation broke up in 1960 (`ml`). East Pakistan became Bangladesh in 1971 (`pk`). Default: one code for each state throughout the span, its code of 1974. The register keeps the name the series writes ("Ceylon", "Congo").
10. **A state formed after 1974.** The Socialist Republic of Vietnam dates from 1976, after the standard of 1974. Default: keep `srv`, the series' form beside `drv` and `rvn`. The standard's later code, `vn`, was the Republic of Vietnam's in 1974, and a reader would misread it.
11. **A code that is a common word.** Several new codes are also short English words or other things: `in`, `is`, `it`, `id`, `do`, `be`, `no`, `so`, `my`. Default: the standard's codes as they are. Two safeguards come with them. First, the check that looks for a nation's name in the entry's line does not count a new two-letter code as the nation's word, so "IN" or "NO" in a line does not support a tag. Second, Norway's `no` is written in quotes in the data files, because YAML would otherwise read a bare `no` as "false". In a tag, `polity:no` needs no quotes.
12. **Codes a reader could mistake for another country.** `ch` is Switzerland, not China. `at` is Austria, and Australia is `au`. `ci` is the Ivory Coast. Default: the standard's codes. `check` and `patch-check` catch a wrong one as in point 3.
13. **The labels on the visibility pages.** Each polity's label is its code in capitals. Default: the label follows the code, so "CUBA:public-PA" becomes "CU:public-PA" and "FRG" becomes "DE". The six at the top of the visibility page read "US, USSR, PRC, FR, DE, UK".
14. **The nations' page addresses.** A nation's page is named by its id. 108 nation pages change address, for example `places-cuba.html` to `places-cu.html`. Default: each old address becomes a page that sends the reader on to the new one, with the place in the page kept.

## What the script changes

A dry run on the data as it stands today gives these counts:

- `sources/polities.yaml`: 469 values. These are the 108 polities' rows (each with its new code, its label in capitals and its old id as an alias), the polities of the threads and places, and the people's polities. A thread's name, a place tag and a person's key are not changed.
- The calendar: 6,126 `polity:` tags and 1,301 `vis:` rulings, in 5,876 entries in 122 month files.
- `sources/places.yaml`: 287 values of `in:`.
- `sources/provenance.yaml`: 147 values (the series' polities, the parties of FRUS documents, the publishers' countries, the works' countries).
- `sources/people.yaml`: nothing. Its polities are all kept ones (`prc`, `drv`, `ussr`, `rok`).
- The code: the lists of nations written into `tools/bib/vis.py`, `vispage.py`, `vis_words.py` and `placepages.py`, the seeding script `tools/vis/seed.py`, and the answers in `tools/vis/selfcheck.py`. Each change is made by its place in the code, so a thread's name or a map's own key is never touched.
- The tests: three test files' small registers and their expected results, and the test data's tags and places (116 tags and rulings, and 240 values of `in:`).

In all, 8,996 values in 137 files.

The script finds each list in the code by its place in the code's structure. Where one has moved or changed and the script cannot find it, the script says so and refuses to write anything.

## How an old id keeps working

The code now reads an old id as its nation's id wherever it reads a tag or a register's value. This part is already in the code, and it does nothing until the register has aliases.

- When the calendar is loaded, and when a patch is merged, an old tag is turned into the new one. `polity:cuba` becomes `polity:cu`, and `vis:only:ussr+cuba` becomes `vis:only:ussr+cu`. So a patch written before the change merges, and the file holds the new code once it is saved.
- `./bib find -t polity:cuba` finds the entries tagged `polity:cu`.
- A tag removed by its old id is removed.
- A place added by a patch with an old id in `in:` is written with the new code.
- A nation's old name and old label still count as its words in the line, so the check's warnings do not change.
- The visibility pass reads an old id in any register as the new one.

## When it runs

The script is run when no patch waits in `inbox/`. It refuses to write while one does, unless it is told to go ahead anyway. Patches in `inbox/held/` are not counted as waiting. Old ids in them still merge.

After it runs, two steps follow. First, the tests' saved outputs that list tags are rewritten (`python3 -m pytest -q -m "not slow" --update-goldens`), and the change in them is read. The list of tags is sorted by name, so its order changes. Second, `./bib check` is run.

## What was checked before this note

- The script was run on a copy of the data and the code, not on this checkout. Every changed value was compared with the old one. The register, the gazetteer, the source registry and all 59,899 changed calendar entries matched value for value, with only the ids changed.
- On that copy, the place pages were the same 253 pages with the same entry counts, the "Places:" lines of 2,500 sampled entries were the same apart from their links, the visibility labels of the same entries were the same apart from the codes, and `./bib check` gave the same warnings.
- A second run of the script on the copy found nothing to change.
- A patch written with `polity:cuba`, `polity:frg` and `vis:only:us+cuba@A` passed `patch-check` and merged on the copy as `polity:cu`, `polity:de` and `vis:only:us+cu@A`.
- On the copy, the fast tests passed, apart from the four saved outputs that list tags, which the step above rewrites.
