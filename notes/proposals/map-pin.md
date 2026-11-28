# A pin on the maps

Nov. 28, 2026. For the owner, on the request of Nov. 27, 2026: "Could we make it so that tapping a point on the map 'drops a pin' that toggles a display beneath the map listing the latitude and longitude of the pin, the nearest point in the gazette, and all available information about the point from the map layers?"

## Where it works

The pin works on every map of the site. There are two maps, the map of Indochina and the map of China. Each stands on its own page (`indochina.html`, `china.html`), in the calendar's pages, at the head of the threads' pages and on the place pages. All of them use the one script (`tools/bib/vnmap.js`), so the pin is on all of them. No other page of the site draws a map this way.

## What a tap does

- A tap or a click on the map drops a pin at that point. The pin is the map library's own marker, drawn in the page's ink colour.
- A tap somewhere else on the map moves the pin there.
- A tap on the pin takes it away and closes the panel. So does the × at the top right of the panel.
- A tap on a dot still lists the entries placed there, as before. A tap on a city's circle still gives its figures. Neither moves the pin.
- The zoom buttons, the home button, full screen, the layer boxes, the year buttons and the date fields work as before and drop no pin.
- A drag moves the map and drops no pin. A pinch drops no pin. A double tap or a double click zooms in and drops no pin. To tell a double tap from a single one, the pin appears about a third of a second after the tap.
- A pin stays where it is when the dates in the From and to fields change. The panel's counts of entries then follow the new dates.

## What the panel shows

The panel opens just under the map and above the legend. It lists these lines, each only where the map has the layer:

- The pin's latitude and longitude, to three decimal places (about 100 m), with N or S and E or W: "10.861° N, 106.619° E".
- The nearest place in the map's gazetteer: its name as the site writes it, its distance in km, how many entries in the dates shown are placed there, a link to its own page where it has one, and "In the gazetteer", a link to its row in the map's gazetteer.
- The country. It links to the country's page where there is one.
- The province or other unit, with the words a tap on it used to give ("province of late 1966 · III Corps · Southeast"; "province · as of 1966"). A Chinese province links to its page. Where entries are placed in the unit as a whole, their count is shown, and the list of them opens under it.
- On the map of China, the county of 1964, with its line: its name in characters, its kind, its province and prefecture, and what it rests on.
- A disputed area, where the pin falls in one.
- The elevation, read from the relief's tiles, with its band from the legend. At sea, the depth band of the sea instead.
- The contours on either side of the point ("between the 500 m and 1,000 m lines").
- The nearest river within 20 km: its name (both forms where the file has two), its distance, and its size as the file gives it (a mean flow for HydroRIVERS, a width for SWORD).
- The lake the pin is in, with its kind, its dam's year and its area.
- The climate class (Köppen–Geiger, 1961–1990).
- The rain of each month and of the year, and the mean temperature of each month (1961–1990).
- The population density class in 1960 and in 1970, from the modelled grid.
- The nearest city in the Cities layer, its distance and its first figure from the *Demographic Yearbook*.

A layer that holds nothing at the pin still has its line, saying so ("Lakes: none here."; "Rivers: none within 20 km."). While a layer's file is being read its line ends in "…".

The four pictures in `notes/proposals/map-pin/` show the panel with a pin dropped by Saigon (in Gia Định province) and by Wuxi (in Jiangsu), each on a desktop screen and on a phone, at twice the screen's pixels.

## The layers' data, and what the pin costs

Every layer's data is already shipped beside the pages. The pin reads each layer from its own file, not from what the map has drawn. So it reads every layer, whether or not its box is ticked.

Until now no layer's file was fetched before its box was ticked. The pin changes that. When a pin is first dropped, the files of the layers not yet fetched are fetched once for the page. On the map of Indochina this is about 5 MB before compression, on the map of China about 14 MB, mostly the counties, the rain grid and the lakes. The relief and the climate are read from one tile each, at their finest zoom. A second pin fetches nothing new. I took this as the default because the request asks for all available information about the point. I recorded the question in `notes/owner-rulings.md`. If you would rather keep the old rule, the panel can instead read only the layers whose boxes are ticked and say of the others "tick its box to read it here".

The pages themselves are no heavier, apart from one empty element in each map's figure. The manifest each map reads (one file for all its pages) carries three new small items: the contours' levels, every climate class with its colour (the legend leaves out the rarest classes, which the pin may still meet), and the list of the map's places, provinces and countries that have a page of their own. These add about 1 KB to the map of Indochina's manifest and about 5 KB to the map of China's.

No layer's information is left out. Two small things are not shown. The Names layer holds only the labels, so it has no line. The Relief layer is shaded from the same tiles as Elevation, so the elevation's line stands for both.

## Departures from the site's existing style, and why

- The panel is a new element under the map's box, `.vnm-pin`. It shares every rule of the card a tap opens over the map (`.vnm-pop`): the same background, border, corner, padding, type size and line height, the same × button, muted words and lists. The shared rules are now written once for both. The panel's one rule of its own sets its place in the page's flow, with the same space above it as the legend and the folded list have (`.35rem`). Reason: the request puts the display beneath the map, and the existing card already had the look.
- The list of a unit's entries in the panel is folded under its count, with the folded list's own summary rule (`.vnm-list summary`, now shared). Reason: a province can hold hundreds of such entries, and the panel sits in the page's flow, so an open list would push the legend far down.
- The pin itself is the map library's default marker (MapLibre's), in the page's ink colour, which follows the light and dark themes. Reason: the site uses the library's own controls and marks wherever it can.
- A tap on an empty part of the map no longer opens the small card over the map with the unit's name and the month's rain. The panel carries the same lines and more. Reason: two displays of the same facts for one tap would be confusing.
- The pin's distances to places and cities are measured on the sphere. The distance to a river is measured on a flat surface laid at the pin, which is exact enough within 20 km. This is the only arithmetic of its own the map script does with coordinates. The point on a tile is found by the library's own projection.

## Not done, and known limits

- In full screen the panel is outside the map's frame, so it shows when the reader leaves full screen.
- A pin is not kept in the page's address, so it is not there after a reload.
- Building the map of Indochina's page alone (`./bib build indochina`) now takes about 20 seconds longer, because the build works out which places have pages. A full build already does that work.
