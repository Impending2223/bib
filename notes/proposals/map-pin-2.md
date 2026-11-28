# The pin's panel, second round

Nov. 28, 2026. For the owner, on your note of Nov. 27, 2026, about 6:14 p.m., on the pin's panel. The first round is `map-pin.md`. The pictures are in `map-pin-2/`.

## The pictures

- `vietnam-desktop.png` and `vietnam-phone.png`: a pin by Saigon, in Gia Định province, as in the first round.
- `china-desktop.png` and `china-phone.png`: a pin by Wuxi, as in the first round.
- `china-north-desktop.png` and `china-north-phone.png`: a pin in Lanxi county, Heilongjiang, north of Harbin. Its winter months are below freezing, so its temperature bars hang below the zero line, and its winter precipitation falls as snow.
- `rec-labels.png`, `rec-colours.png` and `rec-groups.png`: the three recommendations at the end, each on the Lanxi pin, on a phone.

All are at twice the screen's pixels. The phone is 390 pixels wide, the desktop 1,100.

## What changed, item by item

**"Could we display the monthly temperature and precipitation numbers as two bar graphs, with the same horizontal width as the text?"** Done. Each graph has twelve bars and spans the panel's text from edge to edge. Each month's figure stands over its bar, and the month's initial under it. Above each graph is its label and one figure for the year: "Precipitation: the year, 1,771 mm." and "Temperature: the year's mean, 27.4 °C." Where a month's mean is below freezing, its bar hangs below a thin zero line.

- The figures are always shown, not only on hover. A phone has no hover, and a tap on a bar would have to open something new. A short label over each bar needs nothing new.
- The figures over the bars are whole numbers. On a phone each month's column is about 27 pixels wide. That holds "−19" but not "−18.9". The exact figure, to the tenth, shows when the pointer rests on a bar, and a screen reader reads all twelve exact figures.
- I looked for a chart the site already draws. The indicators' charts use a charting library loaded on the first tap; it draws lines over time, and loading it for twelve bars would be heavy. The Congress pages draw one bar as a picture whose type grows and shrinks with the page's width, so its figures would be large on a desktop and small on a phone. So the bars are plain boxes in the page's own type, sizes and colours. See the departures below.

**"If we have a point estimate of the elevation, we don't need either the "0–100m" band or the contour band. Drop them."** Done. The line now reads "Elevation: about 9 m." The contour line is gone in every case, since it was only read from the same elevation. At sea the line still says "the sea", and the depth's line follows as before.

**"Country" should say "Republic of Viet Nam" or "Republic of Vietnam" ... and the equivalent for the DRV.** Done. The country is now the name the site's register of countries gives (`sources/polities.yaml`): "Republic of Vietnam" and "Democratic Republic of Vietnam", as the calendar writes them. The register's name for the People's Republic is "China (the People's Republic)"; the panel writes it "People's Republic of China", so that it reads alongside "Republic of China" on Taiwan. Where the register has no row, the panel keeps the map file's name: "Vietnam" on the map of China (that file draws Vietnam as one country), "East Pakistan", and "Hong Kong, British colony." and "Macau, Portuguese colony." The register was not changed.

- Each government's own usage. In the English text of the Paris agreement of Jan. 27, 1973 ("Agreement on Ending the War and Restoring Peace in Viet-Nam", 24 U.S.T. 1), which both governments signed, the two are "the Republic of Viet-Nam" and "the Democratic Republic of Viet-Nam", with a hyphen. I read that text from Wikisource's copy. I did not read either government's own publications tonight. To check: Saigon's English publications (its embassy's *Viet-Nam Bulletin*) and Hanoi's (the Foreign Languages Publishing House), which I believe wrote "Viet-Nam" and "Viet Nam".

**"No "Country", county, or province labels. No dates. Just "[Province], [Country]," or "[County], [Province], [Country]."** Done, on both maps. Examples from the pictures:

- "Gia Định, Republic of Vietnam. Capital Military District. Southeast region."
- "Wuxi 无锡县, Suzhou 苏州专区, Jiangsu 江苏省, People's Republic of China."
- "Lanxi 兰西县, Songhuajiang 松花江专区, Heilongjiang 黑龙江省, People's Republic of China."

The words "province of late 1966", "as of 1966", "county, end of 1964" and the province's long description are gone. The province and the country still link to their pages where they have one.

One addition to your form: on the map of China the prefecture of 1964 stands between the county and the province. The panel already named it in characters, and you asked for every tier in pinyin and characters. In the line, its place says what it is, so it needs no label. If you would rather keep your form exactly, it can go after the full stop instead.

Where two tiers have the same name in characters, the panel names it once. A pin in Peking's city reads "Peking 北京市, People's Republic of China." The site's own name for the municipality, "Peking", is kept; it is not the pinyin "Beijing".

**"The regions could just be items after full stop."** Done, as in your example. After the full stop come, where the map has them: the Republic's corps zone ("III Corps." or "Capital Military District."); the region ("Southeast region."); "Today's province." for a province of North Vietnam, Laos or Cambodia, which the map draws by today's lines, not those of the 1960s; a disputed area ("Aksai Chin, disputed."); and a word on a county's lines where they are less sure (next item).

**"I'm not actually sure what "the later unit of the name" means."** No map of China's counties in 1964 was found. So each county of 1964 is drawn with the outline of a county in a boundary file of about 1994. "The later unit of the name" meant: this county kept its name from 1964 to about 1994, so the county of that name in the 1994 file is drawn for it. That is so for 1,815 of the 2,300 counties. At a point it tells the reader nothing, and the page's text under the map already says how the counties were drawn. So it is dropped. A short item stays only where the outline is less sure:

- "The county here is a guess." (79 counties, where the record did not settle which county of 1964 the ground belonged to).
- "Drawn at the city's later, larger size." (149 cities: in 1964 the city was smaller, and the pin may lie in ground that was then a county's).
- "Name and lines of a later year." (138 units the record could not trace back to 1964, among them all of Zhejiang's).

The notes on how each of Taiwan's counties was drawn are dropped for the same reason.

**"Could we give the Pinyin and CJK of all tiers, not just the counties?"** Done for the county, the prefecture and the province. The province's characters come from the map's own file of units. The prefectures' names had no pinyin in the map's files, so I made a table of 249 of them by the same rule the counties' names were made with, and the build puts it in the map's manifest. The country is in English alone; its name in characters would double the line's length. The characters are in the muted colour, as the county's were before.

**"Could we not give the provinces a heavier style all to themselves?"** Done. No tier is bold now. The only bold line is the latitude and longitude at the head, as before.

**"Just "nearest, unnamed" fits this use case."** Done: "Rivers: nearest, unnamed, 2.5 km." A lake with no name reads "unnamed" too, and the cities' line "Cities: nearest, Saigon, 13 km.", so that the three read alike.

**"Just "Climate," "Rain" ..., "Temperature."** Done, but the middle label is "Precipitation". The layer's source, CRU CL 2.0 (New and others, *Climate Research*, 2002), gives precipitation from rain gauges, and a gauge counts snow as the water it melts to, so its winter figures in the north are mostly snow. The years 1961–1990 are no longer in the labels; the text under the map gives them with the source.

**"The population density units should go after the estimate, and the label should be "Population density".** Done: "Population density: 1960, 50–100 persons a km²; 1970, 50–100 persons a km²." The word "modelled" is gone from the line; the text under the map says how the grid was made.

## Departures from the site's existing style, and why

- The bars are a new element, `.vnm-bars`, with three rules of their own in `vnmap.css`. No existing chart fit (above). Everything in them is an existing token or size: the type is the legend's size (`.72rem`); the figures are in ink; the month's initial is the existing muted class (`.m`); the bars are in the muted colour; the zero line is the rule colour the panel's border uses. The one new number is the bars' height, 2.5 rem, about two lines of the panel's text.
- The year's mean temperature is a new figure. It gives the degree sign a place on the line, as the year's total does for the millimetres.
- The prefecture stands in the place line (above).
- A colony that is its own country on the map keeps its kind: "Hong Kong, British colony." Without it the line would read "Hong Kong, Hong Kong."
- The prefectures' pinyin is a new file, `tools/cnmap/prefectures.json`, made by a new script, `tools/cnmap/prefs.py`. The map's other data is in `sources/china/`, which I was asked not to change tonight. It would sit better there.
- The contours' levels are no longer in the manifest, since only the dropped contour line used them.

## Recommendations on the styling

1. **Put each line's label in the muted colour** ("Elevation:", "Rivers:", "Climate:"), and leave the values in ink (`rec-labels.png`). The eye then lands on the facts, and still finds a line by its label. It uses the muted colour the legend's words already have, and no new rule.
2. **Colour the bars from the map's own palette**: the precipitation in the rivers' blue, the temperature in the contours' brown (`rec-colours.png`). The two graphs are then told apart at a glance, and each matches a layer on the map. Both colours already have their dark-theme values. A red for temperature would be more usual, but red marks the entries on this map.
3. **Group the lines with a thin rule into four parts**: the place; the ground and water (elevation, rivers, lakes); the climate (the class and the two graphs); the people (population density, cities) (`rec-groups.png`). The panel has about a dozen lines, and the groups make it quicker to scan. The rule is the same one-pixel line as the panel's border. It adds about one line of height for each group.

The three can be taken together or one at a time. I would take the first and the second.

## Known limits

- On the map of China, a pin in Vietnam says "Vietnam", since that map's file draws Vietnam as one country.
- In full screen the panel is still outside the map's frame, as in the first round.
