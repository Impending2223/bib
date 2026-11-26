"""build/china.html: the map of China on a page of its own (the owner, Nov. 22, 2026: "We should probably give ourselves
a China map. Like our Southeast Asia/Indochina map."), with the gazetteer as a table and the sources. The map is
cnmap's (its STYLE): the figure, script and styles of the maps of Indochina; this module writes only the page around
it, as tools/bib/indochina.py does for indochina.html.

STYLE
 1. The page, as indochina.html: a lede (what the map shows), a muted line to the other map's page (vnmap.css's
    .vnm-pg, as the line under each map in the calendar), the map (cnmap.full_figure), the gazetteer, the sources and
    their licences. Plain statements; no color.
 2. The gazetteer: one row a place of the calendar's gazetteer (sources/places.yaml) that lies in China, Hong Kong,
    Macau or Taiwan, in alphabetical order: the place as the calendar writes it, linked to the Wikipedia article or the
    Wikidata item whose coordinates it takes; its name in Chinese, where that item gives one; the province of 1966 and
    the county of 1964 the point falls in; the calendar entries placed there. A place with LIST entries or fewer lists
    them by year, each linked (tools/bib/datelist.py, as indochina.html does); a place with more gives each year's
    count, linked to the map at that year (Peking's entries alone would be some 8,000 links). A place not on the map
    says why. A row is anchored `pl-<key>`; a tap on a dot on the map links to it. The table is indochina.py's
    (.vng), its styles taken from there.
"""
import html
import os

from . import calsplit, cnmap, datelist, indochina, loose, places as gaz, store

esc = lambda s: html.escape(str(s if s is not None else ""), quote=True)
LIST = 30
README = indochina.README


def _gazetteer(series):
    G, U, C = cnmap.gazetteer(), cnmap.units(), cnmap.counties()
    lst = series.lists["cal"]
    at = {}
    for y, rows in sorted(cnmap.by_year(series).items()):
        for e, pl, us in rows:
            for p in pl:
                at.setdefault(p, []).append(e)
    for k, p in G.items():                         # a province named as a place: its entries under its own key
        if p.get("area"):
            at[k] = [e for y, rows in sorted(cnmap.by_year(series).items()) for e, pl, us in rows
                     if any((gaz.get(x) or {}).get("key") == k for x in gaz.keys(e))]
    unplaced = {}                                  # entries at a place not on the map: counted, for its row
    for sec, e in lst.entries():
        if "when" in e and "place" in e:
            for x in gaz.keys(e):
                r = gaz.get(x)
                if r and r["key"] in G and G[r["key"]].get("unplaced"):
                    unplaced.setdefault(r["key"], []).append(e)
    out = ['<div class="vng-w"><table class="vng"><thead><tr><th>Place</th><th>In Chinese</th>'
           '<th>Province, 1966</th><th>County, 1964</th><th>In the calendar</th></tr></thead><tbody>']
    n_on = 0
    for k, p in sorted(G.items(), key=lambda kv: store.fold(cnmap.shown(kv[0]))):
        name = esc(cnmap.shown(k))
        if p.get("wiki"):
            name = f'<a href="{esc(p["wiki"])}">{name}</a>'
        u = U.get(p.get("unit") or "")
        if p.get("unplaced"):
            prov = f'<span class="m">not on the map: {esc(p["unplaced"])}</span>'
        elif u:
            prov = esc(u["name"]) + (' <span class="m">(the province as a whole)</span>' if p.get("area") else "")
        else:
            prov = f'<span class="m">{esc(p.get("country") or "")}</span>'
        c = C.get(p.get("county") or "")
        county = esc(c["name"]) if c else ""
        ents = at.get(k) or unplaced.get(k) or []
        n_on += bool(at.get(k))
        href = lambda e: calsplit.href(lst, calsplit.half_of_date(lst, loose.place_iso(e)) if calsplit.cfg(lst) else 1, e["id"])
        if not ents:
            cal = ""
        elif len(ents) <= LIST:
            cal = datelist.run([(e["date"], f'<a href="{esc(href(e))}">{esc(e["when"])}</a>') for e in ents])
        else:
            by = {}
            for e in ents:
                by[str(e["date"])[:4]] = by.get(str(e["date"])[:4], 0) + 1
            cal = " ".join(datelist.stop(datelist.part(y, [f'<a href="#y{y}">{n:,} entries</a>'])) for y, n in sorted(by.items()))
        out.append(f'<tr id="pl-{esc(k)}"><td>{name}</td><td lang="zh">{esc(p.get("zh") or "")}</td>'
                   f'<td>{prov}</td><td>{county}</td><td class="cl">{cal}</td></tr>')
    out.append("</tbody></table></div>")
    return "".join(out), len(G), n_on


def page(series, template):
    if "cal" not in series.lists or not cnmap.gazetteer() or not cnmap.units():
        return None
    saved = dict(calsplit.CUR)
    calsplit.CUR.update(half=None, mode="list")
    try:
        by = cnmap.by_year(series)
        n_e = sum(len(v) for v in by.values())
        gz, n_g, n_on = _gazetteer(series)
        fig = cnmap.full_figure(series)
        stands = indochina.in_calendar(series, cnmap)
    finally:
        calsplit.CUR.clear()
        calsplit.CUR.update(saved)
    G = cnmap.gazetteer()
    ys = cnmap.years(series)
    n_pt = sum(1 for p in G.values() if p.get("lat") is not None and not p.get("area"))
    n_area = sum(1 for p in G.values() if p.get("area"))
    n_un = sum(1 for p in G.values() if p.get("unplaced"))
    cj = cnmap._json("counties.json", {})
    cs = [c for c in cj.get("counties", []) if c.get("c") != "roc"]
    roc = [c for c in cj.get("counties", []) if c.get("c") == "roc"]
    n_later = sum(1 for c in cs if c.get("later"))
    n_c, n_guess = len(cs) - n_later, sum(1 for c in cs if c.get("guess") and not c.get("later"))
    counties = (
        f'<p class="logic">The counties. No open map of the counties of the 1960s was found. These are the counties, '
        f'cities and like units of the end of 1964, after the mergers of 1958–61 were undone: {n_c:,} of them, each '
        'drawn as a union of the units of a later boundary file (geoBoundaries\' China ADM2, the 1:4,000,000 county '
        'lines of the National Administration of Surveying, Mapping and Geoinformation as Revolutionary GIS gave them '
        f'out, Public Domain Dedication and License; its units are those of about {cj.get("file_year", 1994)}). Which '
        'later units made up each county is taken from the lists of every province\'s counties, year by year, and each '
        'year\'s changes, at 行政区划网 (<a href="http://www.xzqh.org">xzqh.org</a>). A county whose name and place did '
        'not change is the later unit; a city is drawn at its later size, larger than the city of 1964; a unit made '
        'after 1964 is given whole to the county it was taken from, or to the first named where it was taken from '
        f'several. {n_guess:,} of the {n_c:,} rest on a guess, which a tap on the county says. {n_later:,} later '
        'units are shown as they are, under their later names, where the record was not had (all Zhejiang) or the '
        'unit was not traced back to 1964; a tap says so. A line is exact only where it has not moved since. '
        f'<a href="{README}china/README.md">Each kind of case, the counts, and the counties not shown</a>.</p>'
    ) if cs else ""
    if roc:
        n = lambda k: sum(1 for c in roc if c["kind"] == k and c["unit"] == "taiwan")
        counties += (
            '<p class="logic">Taiwan, the Pescadores, Kinmen and Matsu. Drawn by the Republic of China\'s own units of '
            f'the 1960s: Taiwan Province\'s {n("county")} counties, {n("provincial city")} provincial cities and the '
            'Yangmingshan Administrative Bureau, and Fujian Province\'s two counties, Kinmen (Quemoy) and Lienchiang '
            '(Matsu). Each is a union of today\'s townships and districts (g0v\'s twgeojson, made from the Institute '
            'of Transportation\'s boundary files; CC0 1.0). Taipei is the city of before July 1968: Shilin and Beitou '
            'are the Bureau\'s, and Neihu, Nangang, Muzha and Jingmei are Taipei county\'s. Hsinchu and Chiayi cities '
            'are in their counties, as they were until 1982. Taichung, Tainan and Kaohsiung are each a city and a '
            'county, as before 2010, and Xiaogang is Kaohsiung county\'s. '
            f'<a href="{README}china/README.md">Each adjustment</a>.</p>')
    have = {k for k, f in cnmap.FILES.items() if os.path.exists(os.path.join(cnmap.SRC, f))}
    if cnmap.has_cities():
        have.add("cities")
    # the layers, each named only where its file is there (the fixture has none): the boxes' line, then the sources'
    box = [t for k, t in (("dem", "relief, elevation"), ("contours", "contours"),
                          ("rivers", "rivers and lakes (a reservoir from its dam's year)"), ("koppen", "climate"),
                          ("climate", "rain by month"), ("pop", "population (1960 or 1970, modelled)"),
                          ("cities", "the cities' populations as printed then")) if k in have]
    boxes = ("; " + ", ".join(box[:-1]) + (" and " if box[1:] else "") + box[-1]) if box else ""
    lay = [t for k, t in (
        ("dem", "Relief, elevation, depths and contours: NOAA National Centers for Environmental Information, "
                "<i>ETOPO 2022 Global Relief Model</i> (2022), doi:10.25921/fd45-gt74 (public domain), its grid of 30 "
                "arc-seconds, served as elevation tiles that the map shades itself. The bands run on above 2,000 m, to "
                "5,000 m and over; land below sea level is counted 0 m."),
        ("rivers", "Rivers: HydroRIVERS v1.0 (Lehner and Grill, 2013), those with a long-term mean flow of 30 m³/s and "
                   "over; their names from SWORD v17c (Altenau et al., 2021; CC BY 4.0), in its own English forms. "
                   "Lakes: HydroLAKES v1.0 (Messager et al., 2016; CC BY 4.0), those of 10 km² and over, the dams' "
                   "years from GRanD (Lehner et al., 2011), as Lehner's Dam Impoundment Database gives them (CC BY "
                   "4.0). Rivers are today's courses; reservoirs without a year are not thereby older than 1969."),
        ("koppen", "Climate: Köppen–Geiger classes, 1961–1990, Beck et al. (2023), CC BY 4.0."),
        ("climate", "Rain and temperature: CRU CL 2.0, monthly means of 1961–1990 (New et al., 2002), Climatic Research "
                    "Unit, University of East Anglia, in cells of half a degree, each the mean of nine of its cells; "
                    "the derived grid under the Open Database License."),
        ("pop", "Population: ISIMIP3a's gridded historical population, which ISIMIP takes from HYDE 3.2.1 (Klein "
                "Goldewijk et al., <i>Earth System Science Data</i> 9: 927–953, 2017), in cells of a quarter of a "
                "degree, nine of its cells summed: a model, made later from national totals and later maps, not a "
                "census (ISIMIP: CC BY 4.0)."),
        ("cities", "Cities: the United Nations' <i>Demographic Yearbook</i>, 1966 (table 6) and 1970 (table 8), each "
                   "figure cited by page. For the mainland these print the census of June 30, 1953 and the estimates "
                   "of the end of 1957, as the State Statistical Bureau gave them out, and nothing later."),
    ) if k in have]
    layers = ('<p class="logic">The layers. Each is made from the source of the same layer of the map of Indochina, by '
              'the same script, about four times as coarse, since this map opens about four times as far out. '
              + " ".join(lay) + f' <a href="{README}china/README.md">The files, citations and licenses</a>.</p>') if lay else ""
    main = [
        f"<h1>China, {ys[0]}–{ys[-1]}</h1>",
        f'<p class="lede">China: the calendar\'s entries placed on one map, {n_e:,} entries whose place is in the '
        f'People\'s Republic, Hong Kong, Macau or Taiwan, {ys[0]}–{ys[-1]}, at {n_on} of the gazetteer\'s {n_g} places '
        'there. A year at a time, or all together, or any span of dates. The same map stands in each page of the '
        'calendar that holds a placed entry, under the day of the first, and at the head of the pages of the China '
        'threads, each on its page\'s dates.</p>',
        '<p class="vnm-pg">Vietnam, Laos and Cambodia on a map of their own: <a href="indochina.html">Indochina</a>.</p>',
        '<h2 id="map" data-short="Map">The map</h2>',
        fig,
        '<p class="logic">A dot a place, larger by the number of the year\'s entries there; a tap lists them, each '
        'linked to its entry. The gazetteer\'s other places small and gray. The provinces, autonomous regions and '
        'municipalities as of 1966, plain; or the countries\' borders alone; or land and water. A tap on a province '
        'names it and lists the entries placed in the province as a whole. Boxes: the names of the provinces; the '
        f'counties of 1964, drawn from later lines{boxes}. Two fingers or the mouse to move the map; a pinch, a double tap, '
        'the buttons, or Ctrl or ⌘ and the wheel to zoom, to 64 times; full screen from the last button. Above the '
        'map, the year, and the span\'s two fields, From and to: the map shows the entries dated within them. A '
        'year\'s button fills them. A date typed by hand reads in the calendar\'s form (Apr. 15, 1961) or as '
        '1961-04-15; a month or a year alone reads as its first day in the first field and its last in the second; '
        'what does not read changes nothing. Under the map, folded, the span\'s placed entries.</p>',
        f'<p class="logic">The map in the calendar\'s pages, by the day it stands under: {datelist.run(stands)}</p>'
        if stands else "",
        '<h2 id="gazetteer" data-short="Gazetteer">The gazetteer</h2>',
        f'<p class="logic">Every place in China, Hong Kong, Macau and Taiwan that a calendar entry\'s place names, '
        f'{n_g} in all: {n_pt} with a point, {n_area} provinces named as places, {n_un} not on the map. The place as '
        'the calendar writes it, linked to the Wikipedia article or the Wikidata item whose coordinates it takes; its '
        'name in Chinese as that item gives it; the province of 1966 and the county of 1964 the point falls in; the '
        f'calendar entries placed there, by year, each linked; where a place has more than {LIST}, each year\'s count, '
        'linked to the map at that year. Alphabetical.</p>',
        gz,
        '<h2 id="sources" data-short="Sources">Sources and limits</h2>',
        '<p class="logic">The borders. Every line on the map is one geometry, simplified together so that neighbours '
        'meet. The countries, the coast and the disputed areas are geoBoundaries\' Comprehensive Global '
        'Administrative Zones (CGAZ, release 6.0.0; Runfola et al., <i>PLoS ONE</i> 15(4): e0231866, 2020; CC BY 4.0), '
        'whose country lines are the U.S. Department of State\'s Large Scale International Boundaries. The lines '
        'inside China are the county file\'s, below: the provinces are dissolved from its counties. The countries '
        'are named as of the 1960s (the Soviet Union one country, East Pakistan, Burma); their lines are today\'s. '
        'The areas CGAZ marks as disputed (Aksai Chin and the other sectors of the line with India) are drawn as land, '
        'their lines dashed, in no country\'s tint. '
        f'<a href="{README}china/README.md">The files and their making</a>.</p>',
        '<p class="logic">The provinces. Those of 1966: 21 provinces, five autonomous regions and two municipalities, '
        'with Hong Kong and Macau as the colonies they were, and Taiwan a country of the map, drawn by the Republic '
        'of China\'s two provinces, Taiwan and Fujian (Kinmen and Matsu). Made from later lines: '
        'Tianjin put back in Hebei (a municipality again from January 1967), Hainan in Guangdong (a province from '
        '1988), Chongqing in Sichuan (a municipality from 1997). Inner Mongolia in its shape before July 1969, which is '
        'nearly today\'s. Lines moved since 1966 by less than a county are not put back.</p>',
        counties,
        '<p class="logic">The places. Wikidata\'s or Wikipedia\'s coordinates, never guessed; a place neither has is '
        'not on the map, and its row says so. A province named as a place has no point: a tap on the province lists '
        'its entries. The province and the county by point in polygon, so as approximate as the lines.</p>',
        layers,
        '<p class="logic">The software. The map is drawn by MapLibre GL JS 6.13.0 (BSD-3-Clause; © MapLibre '
        'contributors, and Mapbox for its code of 2020 and before), the names set in Libre Franklin (SIL Open Font '
        'License 1.1, © The Libre Franklin Project Authors); both served from this site, with PMTiles 4.5.0 '
        f'(BSD-3-Clause, © Protomaps LLC), through which the relief\'s and the climate\'s tiles are read. '
        f'<a href="{README}vendor/README.md">Their licenses</a>.</p>',
        indochina.HYDROSHEDS if "rivers" in have else "",
    ]
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", f"China, {ys[0]}–{ys[-1]}").replace("{{main}}", "\n".join(x for x in main if x))
    from . import vnmap
    css, js = vnmap.head_tags()
    return pg.replace("</head>", css + "\n" + indochina.CSS + "\n</head>", 1).replace("</body>", js + "\n</body>", 1)
