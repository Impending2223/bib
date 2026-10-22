"""build/indochina.html: the map of Vietnam, Laos and Cambodia on a page of its own (the owner's request, Oct. 22, 2026),
with the gazetteer as a table and the sources. The map is vnmap's (its STYLE 6): the same shapes, layers, script and
styles as the calendar's annual maps; this module writes only the page around it.

STYLE
 1. The page: a lede (what the map shows), the map (vnmap.full_figure: every placed entry, a year selector, all years
    by default), the gazetteer, the sources and their licenses. Plain statements; no color.
 2. The gazetteer: one row a place of sources/vn-provinces-1966/places.json, in alphabetical order:
    the place as the series writes it (English names stay: CLAUDE.md), linked to the Wikipedia article whose
    coordinates it takes; the plain form; the kind; the 1966 province (or, outside the Republic, the country, muted);
    the corps zone; the calendar entries tagged there, by year (tools/bib/datelist.py), each linked to its entry on
    its calendar page. A row is anchored `pl-<id>`; a tap on a dot on the map links to it.
 3. Credits as the layers' READMEs require: HydroSHEDS's statement in full where the rivers are credited; CC BY and
    ODbL sources named with their licenses.
"""
import html
import os

from . import calsplit, datelist, store, vnmap

esc = lambda s: html.escape(str(s if s is not None else ""), quote=True)

KIND = {"city": "city", "town": "town", "base": "base", "battle": "battlefield", "operation": "operation",
        "region-feature": "area", "sea": "sea"}
COUNTRY = {"vn-north": "North Vietnam", "laos": "Laos", "cambodia": "Cambodia", "sea": "at sea"}
ZONE = {"I": "I Corps", "II": "II Corps", "III": "III Corps", "IV": "IV Corps", "CMD": "Capital Military District"}
README = "https://github.com/impending2223/bib/blob/main/sources/"


def _gazetteer(series):
    G, U = vnmap.gazetteer(), vnmap.units()
    lst = series.lists["cal"]
    at = {}
    for y, rows in sorted(vnmap.by_year(series).items()):
        for e, pl, pv in rows:
            for p in pl:
                at.setdefault(p, []).append(e)
    out = ['<div class="vng-w"><table class="vng"><thead><tr><th>Place</th><th>Plain form</th><th>Kind</th>'
           '<th>Province, 1966</th><th>Corps zone</th><th>In the calendar</th></tr></thead><tbody>']
    for k, p in sorted(G.items(), key=lambda kv: store.fold(vnmap.shown(kv[1]))):
        u = U.get(p.get("province") or "")
        prov = esc(vnmap.ENGLISH.get(u["name"], u["name"])) if u else \
            f'<span class="m">{esc(COUNTRY.get(p.get("country"), ""))}</span>'
        zone = esc(ZONE.get(u.get("ctz"), "")) if u else ""
        name = esc(vnmap.shown(p))
        if p.get("wiki"):
            name = f'<a href="{esc(p["wiki"])}">{name}</a>'
        ents = at.get(k, [])
        cal = datelist.run([(e["date"], f'<a href="{esc(calsplit.href(lst, calsplit.half_of_date(lst, e["date"]) if calsplit.cfg(lst) else 1, e["id"]))}">'
                                        f'{esc(e["when"])}</a>') for e in ents]) if ents else ""
        plain = p.get("plain") if p.get("plain") and p.get("plain") != vnmap.shown(p) else ""
        out.append(f'<tr id="pl-{esc(k)}"><td>{name}</td><td>{esc(plain)}</td><td>{esc(KIND.get(p.get("kind"), p.get("kind") or ""))}</td>'
                   f'<td>{prov}</td><td>{zone}</td><td class="cl">{cal}</td></tr>')
    out.append("</tbody></table></div>")
    return "".join(out), len(G), sum(1 for k in G if at.get(k))


def page(series, template):
    if "cal" not in series.lists or not vnmap.gazetteer():
        return None
    saved = dict(calsplit.CUR)
    calsplit.CUR.update(half=None, mode="list")
    try:
        by = vnmap.by_year(series)
        n_e = sum(len(v) for v in by.values())
        gz, n_g, n_used = _gazetteer(series)
        fig = vnmap.full_figure(series)
        lst = series.lists["cal"]
        annual = []
        for y, eid in sorted(vnmap.anchors(series).items()):
            hit = series.get(eid)
            if hit:
                e = hit[2]
                h = calsplit.href(lst, calsplit.half_of_date(lst, e["date"]) if calsplit.cfg(lst) else 1, eid)
                annual.append((e["date"], f'<a href="{esc(h)}">{esc(e["when"])}</a>'))
    finally:
        calsplit.CUR.clear()
        calsplit.CUR.update(saved)
    ys = vnmap.years(series)
    main = [
        f"<h1>Indochina, {ys[0]}–{ys[-1]}</h1>",
        f'<p class="lede">Vietnam, Laos and Cambodia: the calendar\'s entries placed on one map, {n_e} entries tagged with '
        f'a place or a province, {ys[0]}–{ys[-1]}, at {n_used} of the gazetteer\'s {n_g} places. A year at a time, or '
        'all together. The same map stands in the calendar a year at a time, at each year\'s first entry placed in the '
        'Republic of Vietnam.</p>',
        '<h2 id="map" data-short="Map">The map</h2>',
        fig,
        '<p class="logic">A dot a place, larger by the number of the year\'s entries there; a tap lists them, each '
        'linked to its entry. The gazetteer\'s other places small and gray. The Republic\'s provinces as of late 1966, '
        'in the tint of their corps zone, of today\'s region, or plain. Layers: relief, elevation, contours, rivers and '
        'lakes (a reservoir from its dam\'s year), climate, rain by month. Drag to pan; the buttons, a double tap, a '
        'pinch, or Ctrl or ⌘ and the wheel to zoom, to 64 times. Above the map, the year; under it, folded, the year\'s '
        'placed entries.</p>',
        f'<p class="logic">The annual maps in the calendar: {datelist.run(annual)}</p>' if annual else "",
        f'<h2 id="gazetteer" data-short="Gazetteer">The gazetteer</h2>',
        f'<p class="logic">Every place the series has placed or may place, {n_g} in all: the place as the series writes '
        'it, linked to the Wikipedia article whose coordinates it takes; the plain form; the kind; the province of '
        'late 1966 the point falls in, or the country; the corps zone; the calendar entries tagged there, by year. '
        'Alphabetical.</p>',
        gz,
        '<h2 id="sources" data-short="Sources">Sources and limits</h2>',
        '<p class="logic">The provinces. No map of the Republic of Vietnam\'s provinces is published. These are rebuilt '
        'from today\'s districts (GADM 4.1, level 2, drawn before Vietnam\'s 2025 province mergers), each district '
        'given whole to the 1966 province that held most of it, after Wikipedia\'s articles on the old provinces and '
        'the Vietnamese list <i>Tỉnh (Việt Nam Cộng hòa)</i>. A line exact where it follows a district line that has '
        'not moved; off by a district where one straddled two 1966 provinces (Hậu Nghĩa, Kiến Tường, Phú Bổn, the '
        'Quảng Tín–Quảng Nam line). Huế and Đà Lạt drawn at today\'s size, several times the cities of 1964; Phú Bổn '
        'may lack Ea H\'leo. Corps zones as of late 1966; Bình Tuy in II Corps from Sept. 1964, in III by 1968 (the date '
        'not found: Check). Regions today\'s, before 2025. The countries around from Natural Earth (public domain). '
        f'<a href="{README}vn-provinces-1966/README.md">The files and their making</a>.</p>',
        '<p class="logic">The places. Wikipedia\'s coordinates, never guessed; the Iron Triangle, War Zone C and '
        'Junction City at a parent place\'s. The province by point in polygon, so as approximate as the lines.</p>',
        '<p class="logic">The layers. Relief, elevation and contours: NOAA National Centers for Environmental '
        'Information, <i>ETOPO 2022 15 Arc-Second Global Relief Model</i> (2022), doi:10.25921/fd45-gt74 (public domain); '
        'the sea from Natural Earth. Rivers: HydroRIVERS v1.0 (Lehner and Grill, 2013); in the delta, SWORD v17c '
        '(Altenau et al., 2021; CC BY 4.0). Lakes: HydroLAKES v1.0 (Messager et al., 2016; CC BY 4.0), the dams\' years '
        'from GRanD (Lehner et al., 2011), as Lehner\'s Dam Impoundment Database gives them (CC BY 4.0). Rivers are today\'s courses; reservoirs without a year are not '
        'thereby older than 1969. Climate: Köppen–Geiger classes, 1961–1990, Beck et al. (2023), CC BY 4.0. Rain and '
        'temperature: CRU CL 2.0, monthly means of 1961–1990 (New et al., 2002), Climatic Research Unit, University of '
        'East Anglia; the derived grid under the Open Database License. '
        f'<a href="{README}indochina/README.md">The files, citations and licenses</a>.</p>',
        '<p class="logic vng-q">This product, the 1968 series\' map layers, incorporates data from the HydroSHEDS version 1 '
        'database which is © World Wildlife Fund, Inc. (2006-2022) and has been used herein under license. WWF has not '
        'evaluated the data as altered and incorporated within the 1968 series\' map layers, and therefore gives no '
        'warranty regarding its accuracy, completeness, currency or suitability for any particular purpose. Portions of '
        'the HydroSHEDS v1 database incorporate data which are the intellectual property rights of © USGS (2006-2008), '
        'NASA (2000-2005), ESRI (1992-1998), CIAT (2004-2006), UNEP-WCMC (1993), WWF (2004), Commonwealth of Australia '
        '(2007), and Her Royal Majesty and the British Crown and are used under license. The HydroSHEDS v1 database and '
        'more information are available at <a href="https://www.hydrosheds.org">https://www.hydrosheds.org</a>.</p>',
    ]
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", "Indochina, 1960–1968").replace("{{main}}", "\n".join(main))
    return pg.replace("</head>", vnmap.CSS + "\n" + CSS + "\n</head>", 1).replace("</body>", vnmap.JS + "\n</body>", 1)


CSS = """<style id="vngcss">
/* the gazetteer on indochina.html (tools/bib/indochina.py) */
.vng-w{overflow-x:auto;margin:.6rem 0 1rem}
.vng{border-collapse:collapse;font-family:var(--sans);font-size:.78rem;line-height:1.35;width:100%}
.vng th{text-align:left;font-weight:600;color:var(--muted);border-bottom:1px solid var(--rule);padding:.25rem .5rem .25rem 0;white-space:nowrap}
.vng td{vertical-align:top;border-bottom:1px solid var(--rule);padding:.3rem .5rem .3rem 0}
.vng td.cl{min-width:9rem}
.vng .m{color:var(--muted)}
.vng tr:target td{background:var(--panel)}
.vng-q{font-size:.85em}
</style>"""
