"""Maps of Vietnam, Laos and Cambodia in the calendar: one a year, 1960–68, at the year's first entry tagged with a
place in the Republic of Vietnam, showing every entry of the year that is tagged with a place.

The data: sources/vn-provinces-1966/ (its README): the provinces of late 1966 rebuilt from today's districts, the corps
zones and regions dissolved from them, the countries around (indochina-outline.geojson), and the gazetteer
(places.json). Calendar entries carry hidden tags: `place:<id>` (a gazetteer place) and `province:<id>` (a 1966 unit);
`check` fails on one that names nothing (`problems`). The layers of sources/indochina/ (relief, rivers, climate, rain;
its README), where present.

STYLE
 1. The map: the RVN's provinces in their corps zone's tint (Corps zones, the default: the records' own division), or
    today's region's (Regions), or plain (Provinces); province lines thin, zone or region lines heavier, the RVN's
    outline in ink; the countries around in the land color, named in italics. Plain Mercator, north up.
 2. The year's places: a dot each, in the accent, larger by the number of the year's entries there (by area); the
    gazetteer's other places small and muted. A tap on a dot lists its entries (date, thread, the first words of the
    statement), each linked to the entry; under the map, folded, the year's placed entries in date order.
 3. Names: the year's places first, those with most entries first, then the gazetteer's by rank (1, the capitals
    and the largest cities; 2, province capitals, the main bases and battlefields; 3, the rest) as the zoom allows;
    each set right of its dot, else left, above, below, where it clears the names already set; never over another.
    A constant size on screen at any zoom.
 4. Zoom: drag to pan, pinch, the buttons, a double tap; the wheel only with Ctrl or ⌘ held (the page scrolls under
    it otherwise). To 64 times the first view, so a battlefield's places stand apart.
 5. The shapes are not in the pages: build/geo/vn-<hash>.json, fetched when the first map nears the screen (as the
    election maps' are: congress.geo_files); the layers' files beside it.
"""
import hashlib
import json
import math
import os
import re
import shutil

from . import store

SRC = os.path.join(store.ROOT, "sources", "vn-provinces-1966")
LAYERS = os.path.join(store.ROOT, "sources", "indochina")
GEO_OUT = os.path.join(store.ROOT, "build", "geo")
B = (99.5, 7.5, 111.0, 24.0)                   # the plane's bounds, lon/lat
W = 1000.0
_C = {}

# names the series writes in English (CLAUDE.md: English names stay), for the gazetteer's Vietnamese ones
ENGLISH = {"Sài Gòn": "Saigon", "Thung lũng Ia Drang": "Ia Drang valley", "Đồi 875": "Hill 875",
           "Tam giác Sắt": "Iron Triangle", "Chiến khu C": "War Zone C", "Căn cứ Không quân Biên Hòa": "Biên Hòa Air Base",
           "Khu phi quân sự (DMZ)": "DMZ", "Thung lũng A Sầu": "A Shau valley", "Địa đạo Củ Chi": "Củ Chi tunnels",
           "Hải Vân Pass": "Hải Vân pass", "Bến Hải": "Bến Hải river", "Hà Nội": "Hanoi", "Hải Phòng": "Haiphong"}


def _m(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


S = W / math.radians(B[2] - B[0])
H = round((_m(B[3]) - _m(B[1])) * S, 1)


def xy(lon, lat):
    return round((lon - B[0]) / (B[2] - B[0]) * W, 1), round((_m(B[3]) - _m(lat)) * S, 1)


def _ring(r):
    pts = [xy(*p[:2]) for p in r]
    out, last = [], None
    for p in pts:
        if p != last:
            out.append(p)
            last = p
    if len(out) < 3:
        return ""
    return "M" + "L".join(f"{x:g},{y:g}" for x, y in out) + "Z"


def path(geom):
    t, c = geom["type"], geom["coordinates"]
    polys = [c] if t == "Polygon" else c if t == "MultiPolygon" else []
    return "".join(_ring(r) for p in polys for r in p)


def _gj(name):
    p = os.path.join(SRC, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {"features": []}


def gazetteer():
    if "pl" not in _C:
        p = os.path.join(SRC, "places.json")
        _C["pl"] = {x["id"]: x for x in (json.load(open(p, encoding="utf-8")) if os.path.exists(p) else [])}
    return _C["pl"]


def units():
    if "u" not in _C:
        _C["u"] = {f["properties"]["id"]: f["properties"] for f in _gj("provinces1966.geojson")["features"]}
    return _C["u"]


def shown(p):
    return ENGLISH.get(p["name"], p["name"])


def in_rvn(p):
    return bool(p.get("province")) or p.get("country") == "vn-south"


def _copy(name):
    """A layer's file copied beside the pages, named by its hash: its path from a page."""
    src = os.path.join(LAYERS, name)
    h = hashlib.sha1(open(src, "rb").read()).hexdigest()[:10]
    base, ext = os.path.splitext(name)
    out = f"vn-{base}-{h}{ext}"
    os.makedirs(GEO_OUT, exist_ok=True)
    if not os.path.exists(os.path.join(GEO_OUT, out)):
        shutil.copyfile(src, os.path.join(GEO_OUT, out))
    return "geo/" + out


def _json_file(stem, d):
    txt = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    name = f"vn-{stem}-{hashlib.sha1(txt.encode()).hexdigest()[:10]}.json"
    path_ = os.path.join(GEO_OUT, name)
    if not os.path.exists(path_):
        for old in os.listdir(GEO_OUT):
            if re.fullmatch(rf"vn-{stem}-[0-9a-f]{{10}}\.json", old):
                os.remove(os.path.join(GEO_OUT, old))
        open(path_, "w", encoding="utf-8").write(txt)
    return "geo/" + name


def _line(geom):
    t, c = geom["type"], geom["coordinates"]
    lines = [c] if t == "LineString" else c if t == "MultiLineString" else []
    out = []
    for ln in lines:
        pts = [xy(*p[:2]) for p in ln]
        if len(pts) > 1:
            out.append("M" + "L".join(f"{x:g},{y:g}" for x, y in pts))
    return "".join(out)


def layers():
    """The layers of sources/indochina/ the maps can draw (its README), each a file of its own beside the pages:
    rasters as they are (rows in Mercator y over LB), vectors and the climate grid projected here."""
    if "lay" in _C:
        return _C["lay"]
    lay = {}
    if not os.path.isdir(LAYERS):
        _C["lay"] = lay
        return lay
    LB = (100.0, 8.0, 110.5, 23.5)
    x0, y1 = xy(LB[0], LB[1])
    x1, y0 = xy(LB[2], LB[3])
    rect = [x0, y0, round(x1 - x0, 1), round(y1 - y0, 1)]
    ex = lambda f: os.path.exists(os.path.join(LAYERS, f))
    if ex("hillshade.png"):
        lay["relief"] = {"kind": "image", "box": rect, "src": _copy("hillshade-coarse.png"),
                         "mid": _copy("hillshade.png"), "fine": _copy("hillshade-fine.png") if ex("hillshade-fine.png") else None}
    if ex("hypso.png"):
        h = json.load(open(os.path.join(LAYERS, "hypso.json"), encoding="utf-8"))
        lay["tint"] = {"kind": "image", "box": rect, "src": _copy("hypso-coarse.png"), "mid": _copy("hypso.png"),
                       "legend": [{"code": c["label"], "name": "", "color": c["color"]} for c in h["classes"] if c["kind"] == "land"]}
    if ex("koppen.png"):
        k = json.load(open(os.path.join(LAYERS, "koppen.json"), encoding="utf-8"))
        lay["koppen"] = {"kind": "image", "box": rect, "src": _copy("koppen-coarse.png"), "mid": _copy("koppen.png"),
                         "period": "1961–1990", "legend": [{"code": c["code"], "name": c["name"], "color": c["color"]}
                                                           for c in k["classes"] if c.get("share_of_land_in_extent", 1) >= 0.001]}
    if ex("rivers.geojson"):
        rv = json.load(open(os.path.join(LAYERS, "rivers.geojson"), encoding="utf-8"))["features"]
        lk = json.load(open(os.path.join(LAYERS, "lakes.geojson"), encoding="utf-8"))["features"] if ex("lakes.geojson") else []
        d = {"r": [{"d": _line(f["geometry"]), "w": f["properties"].get("size", 1),
                    "n": f["properties"].get("name_vi") or f["properties"].get("name")} for f in rv],
             "l": [{"d": path(f["geometry"]), "n": f["properties"].get("name"),
                    "dy": f["properties"].get("dam_year") if f["properties"].get("type") != "lake" else None}
                   for f in lk if f["properties"].get("area_km2", 0) >= 3]}
        lay["rivers"] = {"kind": "rivers", "src": _json_file("rivers", d)}
    if ex("contours.geojson"):
        ct = json.load(open(os.path.join(LAYERS, "contours.geojson"), encoding="utf-8"))["features"]
        lay["contours"] = {"kind": "lines", "src": _json_file("contours", [{"d": _line(f["geometry"]),
                                                                           "e": f["properties"]["elev_m"]} for f in ct])}
    if ex("climate.json"):
        c = json.load(open(os.path.join(LAYERS, "climate.json"), encoding="utf-8"))
        b, cd = c["bounds"], c["cell_deg"]
        P, T = c["precipitation"]["values"], c["temperature"]["values"]
        cells = []
        for r in range(c["nrows"]):
            for k in range(c["ncols"]):
                v = [P[m][r][k] for m in range(12)]
                if all(x is None for x in v):
                    continue
                cx0, cy0 = xy(b["west"] + k * cd, b["north"] - r * cd)
                cx1, cy1 = xy(b["west"] + (k + 1) * cd, b["north"] - (r + 1) * cd)
                cells.append({"x": cx0, "y": cy0, "w": round(cx1 - cx0, 1), "h": round(cy1 - cy0, 1), "v": v,
                              "t": [None if T[m][r][k] is None else T[m][r][k] / 10 for m in range(12)]})
        lay["rain"] = {"kind": "grid", "period": "1961–1990", "src": _json_file("climate", {"cells": cells,
                       "scale": [0, 25, 50, 100, 200, 300, 400, 500]})}
    _C["lay"] = lay
    return lay


def geo_file():
    """build/geo/vn-<hash>.json, the shapes, projected; the layers' files copied beside it. Its path from a page."""
    if "geo" in _C:
        return _C["geo"]
    pv = _gj("provinces1966.geojson")["features"]
    d = {"W": W, "H": H, "b": B,
         "prov": [{"id": f["properties"]["id"], "n": f["properties"]["name"], "p": f["properties"].get("plain"),
                   "z": f["properties"].get("ctz"), "r": f["properties"].get("region"),
                   "c": f["properties"].get("confidence"), "d": path(f["geometry"])} for f in pv],
         "zone": [{"k": f["properties"]["ctz"], "d": path(f["geometry"])} for f in _gj("ctz1966.geojson")["features"]
                  if f["properties"].get("ctz") not in (None, "none")],
         "reg": [{"k": f["properties"]["region"], "d": path(f["geometry"])} for f in _gj("regions.geojson")["features"]],
         "land": [{"id": f["properties"]["id"], "n": f["properties"]["name"], "d": path(f["geometry"])}
                  for f in _gj("indochina-outline.geojson")["features"]],
         "pl": {k: [*xy(p["lon"], p["lat"]), shown(p), p.get("kind"), p.get("rank", 3), p.get("country")]
                for k, p in gazetteer().items() if p.get("lat") is not None},
         "lay": {}}
    os.makedirs(GEO_OUT, exist_ok=True)
    d["lay"] = layers()
    txt = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    name = f"vn-{hashlib.sha1(txt.encode()).hexdigest()[:10]}.json"
    path_ = os.path.join(GEO_OUT, name)
    if not os.path.exists(path_):
        for old in os.listdir(GEO_OUT):
            if re.fullmatch(r"vn-[0-9a-f]{10}\.json", old):
                os.remove(os.path.join(GEO_OUT, old))
        open(path_, "w", encoding="utf-8").write(txt)
    _C["geo"] = "geo/" + name
    return _C["geo"]


def placed(e):
    tags = e.get("tags") or []
    return ([t.split(":", 1)[1] for t in tags if t.startswith("place:")],
            [t.split(":", 1)[1] for t in tags if t.startswith("province:")])


def by_year(series):
    """{year: [(entry, places, provinces)]}, the calendar's entries tagged with a place, in date order."""
    lst = series.lists.get("cal")
    out = {}
    if not lst:
        return out
    for sec, e in lst.entries():
        if "when" not in e:
            continue
        pl, pv = placed(e)
        if pl or pv:
            out.setdefault(str(e["date"])[:4], []).append((e, pl, pv))
    for y in out:
        out[y].sort(key=lambda t: str(t[0]["date"]))
    return out


def anchors(series):
    """{year: entry id}: the map goes with the year's first entry placed in the RVN (1960–68)."""
    G, out = gazetteer(), {}
    for y, rows in by_year(series).items():
        if not "1960" <= y <= "1968":
            continue
        for e, pl, pv in rows:
            if pv or any(in_rvn(G.get(p, {})) for p in pl):
                out[y] = e["id"]
                break
    return out


def _summary(c):
    from .markup import plain
    t = plain(" ".join(store.as_list(c)))
    t = re.sub(r"\s+", " ", t).strip()
    first = re.split(r"(?<=[.;])\s", t, maxsplit=1)[0]
    return first if len(first) <= 150 else first[:147].rsplit(" ", 1)[0] + " …"


def block(series, y):
    from . import calsplit
    from .build import thread_name
    lst = series.lists["cal"]
    rows = by_year(series).get(y, [])
    ents = []
    for e, pl, pv in rows:
        half = calsplit.half_of_date(lst, e["date"]) if calsplit.cfg(lst) else None
        ents.append({"h": calsplit.href(lst, half or 1, e["id"]), "w": e["when"], "t": thread_name(lst, e["thread"]),
                     "s": _summary(e.get("c")), "p": [p for p in pl if p in gazetteer()], "v": pv})
    data = json.dumps({"y": y, "e": ents}, ensure_ascii=False).replace("</", "<\\/")
    n_pl = len({p for x in ents for p in x["p"]})
    return (f'<figure class="vnm" data-geo="{geo_file()}" data-y="{y}">'
            f'<figcaption class="vnm-cap">Vietnam, Laos and Cambodia, {y}: the year\'s {len(ents)} placed entries, at '
            f'{n_pl} places. Provinces as of late 1966; lines approximate (sources/vn-provinces-1966).</figcaption>'
            '<div class="vnm-bar"></div><div class="vnm-box"><svg class="vnm-svg" role="img" '
            f'aria-label="Map of Vietnam, Laos and Cambodia, {y}"></svg><div class="vnm-z">'
            '<button type="button" data-z="in" aria-label="Zoom in">+</button>'
            '<button type="button" data-z="out" aria-label="Zoom out">−</button>'
            '<button type="button" data-z="home" aria-label="Back to the first view">⌂</button></div>'
            '<div class="vnm-pop" hidden></div><div class="vnm-hint" hidden>Ctrl or ⌘ and the wheel to zoom</div></div>'
            f'<div class="vnm-key"></div><details class="vnm-list"><summary>The year\'s placed entries</summary>'
            f'<ol></ol></details><script type="application/json" class="vnm-d">{data}</script></figure>')


def inject(page, series):
    used = False
    for y, eid in anchors(series).items():
        pat = re.compile(r'(<li id="' + re.escape(eid) + r'"[^>]*>.*?)(</li>)', re.S)
        if not pat.search(page):
            continue
        blk = block(series, y)
        page, k = pat.subn(lambda mm: mm.group(1) + blk + mm.group(2), page, count=1)
        used = used or bool(k)
    if used and 'id="vnmcss"' not in page:
        page = page.replace("</head>", CSS + "\n</head>", 1).replace("</body>", JS + "\n</body>", 1)
    return page


def problems(series):
    out = []
    G, U = gazetteer(), units()
    lst = series.lists.get("cal")
    if not lst:
        return out
    for sec, e in lst.entries():
        for t in e.get("tags") or []:
            if t.startswith("place:") and t[6:] not in G:
                out.append((e["id"], f"{t}: no such place in sources/vn-provinces-1966/places.json"))
            elif t.startswith("province:") and t[9:] not in U:
                out.append((e["id"], f"{t}: no such 1966 unit in sources/vn-provinces-1966/provinces1966.geojson"))
    return out


CSS = """<style id="vnmcss">
/* the calendar's maps of Indochina (tools/bib/vnmap.py) */
:root{--vz1:#7A9CC0;--vz2:#C6A46A;--vz3:#C3877A;--vz4:#86AE7B;--vz5:#A58CBC;--vr1:#8EA9C2;--vr2:#7FB0A3;--vr3:#C9B07A;
  --vr4:#CC9A8A;--vr5:#9FBC80;--vpv:#C9CEC6;--vland:#E4E6E2;--vsea:#E3E9EE;--vop:.55;--vdot:#B03A2E}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--vz1:#57789B;--vz2:#937746;--vz3:#925A4E;--vz4:#5C7F52;
  --vz5:#76618C;--vr1:#5E7D99;--vr2:#4F8578;--vr3:#94814E;--vr4:#9A6B5C;--vr5:#6B8A4F;--vpv:#3A413D;--vland:#262A2E;
  --vsea:#1C242B;--vop:.8;--vdot:#F08C74}}
:root[data-theme="dark"]{--vz1:#57789B;--vz2:#937746;--vz3:#925A4E;--vz4:#5C7F52;--vz5:#76618C;--vr1:#5E7D99;--vr2:#4F8578;
  --vr3:#94814E;--vr4:#9A6B5C;--vr5:#6B8A4F;--vpv:#3A413D;--vland:#262A2E;--vsea:#1C242B;--vop:.8;--vdot:#F08C74}
.vnm{margin:.8rem 0 .4rem;font-family:var(--sans)}
.vnm-cap{font-size:.78rem;color:var(--muted);margin-bottom:.35rem}
.vnm-bar{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;font-size:.75rem;margin-bottom:.4rem}
.vnm-bar .seg{display:inline-flex;border:1px solid var(--rule);border-radius:3px;overflow:hidden}
.vnm-bar .seg button{font:inherit;background:transparent;color:var(--ink);border:0;border-left:1px solid var(--rule);padding:3px 8px;cursor:pointer}
.vnm-bar .seg button:first-child{border-left:0}
.vnm-bar .seg button[aria-pressed="true"]{background:var(--ink);color:var(--bg)}
.vnm-bar label{display:inline-flex;gap:4px;align-items:center;color:var(--muted);cursor:pointer}
.vnm-bar select{font:inherit;color:var(--ink);background:var(--bg);border:1px solid var(--rule);border-radius:3px}
.vnm-box{position:relative;aspect-ratio:4/5;max-height:82vh;width:100%;max-width:100%;background:var(--vsea);border:1px solid var(--rule);border-radius:3px;overflow:hidden}
.vnm-svg{display:block;width:100%;height:100%;touch-action:none;cursor:grab;user-select:none;-webkit-user-select:none}
.vnm-svg.drag{cursor:grabbing}
.vnm-z{position:absolute;right:6px;top:6px;display:flex;flex-direction:column;gap:4px}
.vnm-z button{width:28px;height:28px;font:600 14px var(--sans);border:1px solid var(--rule);background:var(--panel);color:var(--ink);border-radius:3px;cursor:pointer}
.vnm-z button:focus-visible,.vnm-bar button:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
.vnm-hint{position:absolute;left:50%;top:8px;transform:translateX(-50%);background:var(--panel);border:1px solid var(--rule);border-radius:3px;padding:3px 8px;font-size:.75rem;color:var(--muted);pointer-events:none}
.vnm-pop{position:absolute;left:8px;right:8px;bottom:8px;max-height:45%;overflow:auto;background:var(--panel);border:1px solid var(--rule);border-radius:3px;padding:8px 10px;font-size:.8rem;line-height:1.35}
.vnm-pop b{font-weight:600}
.vnm-pop ol,.vnm-list ol{margin:.3rem 0 0;padding-left:1.1rem}
.vnm-pop li,.vnm-list li{margin:.15rem 0}
.vnm-pop .x{float:right;border:0;background:none;color:var(--muted);font:inherit;cursor:pointer}
.vnm-pop .m,.vnm-list .m{color:var(--muted)}
.vnm-key{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:.72rem;color:var(--muted);margin-top:.35rem}
.vnm-key i{display:inline-block;width:11px;height:11px;border-radius:2px;vertical-align:-1px;margin-right:4px;border:1px solid var(--rule)}
.vnm-list{font-size:.8rem;margin-top:.35rem}
.vnm-list summary{cursor:pointer;color:var(--muted)}
.vnm .pv{stroke:var(--bg);stroke-width:.5;vector-effect:non-scaling-stroke}
.vnm .zb{fill:none;stroke:var(--ink);stroke-opacity:.75;stroke-width:1.3;vector-effect:non-scaling-stroke;pointer-events:none}
.vnm .rvn{fill:none;stroke:var(--ink);stroke-width:1;vector-effect:non-scaling-stroke;pointer-events:none}
.vnm .ld{fill:var(--vland);stroke:var(--rule);stroke-width:.6;vector-effect:non-scaling-stroke}
.vnm .ln{font-style:italic;fill:var(--muted);text-anchor:middle;pointer-events:none}
.vnm .riv{fill:none;stroke:#5F88AE;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke}
.vnm .lake{fill:#9DB8CF;stroke:none}
.vnm .ctr{fill:none;stroke:#8A6E4B;stroke-opacity:.7;vector-effect:non-scaling-stroke;pointer-events:none}
.vnm .shade{mix-blend-mode:multiply;pointer-events:none}
.vnm .shade image,.vnm image{pointer-events:none}
.vnm-key .cr{flex-basis:100%;font-size:.68rem}
.vnm-key a{color:var(--muted)}
.vnm .dot{fill:var(--vdot);stroke:var(--bg);stroke-width:1;vector-effect:non-scaling-stroke;cursor:pointer}
.vnm .dim{fill:var(--muted);fill-opacity:.65;stroke:none;cursor:pointer}
.vnm .lb{fill:var(--ink);paint-order:stroke;stroke:var(--vsea);stroke-width:3px;stroke-linejoin:round;pointer-events:none;font-weight:600}
.vnm .lb.o{font-weight:400;fill:var(--muted)}
@media (prefers-reduced-motion: reduce){.vnm *{transition:none!important}}
</style>"""

JS = r"""<script>
/* the calendar's maps of Indochina (tools/bib/vnmap.py, STYLE) */
(function(){
  var NS='http://www.w3.org/2000/svg', GEO={}, MAXZ=64;
  var ZC={I:'--vz1',II:'--vz2',III:'--vz3',IV:'--vz4',CMD:'--vz5'}, ZN={I:'I Corps',II:'II Corps',III:'III Corps',IV:'IV Corps',CMD:'Capital Military District'};
  var RC={'North Central Coast':'--vr1','South Central Coast':'--vr2','Central Highlands':'--vr3','Southeast':'--vr4','Mekong Delta':'--vr5'};
  function el(t,a,p){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;}
  function css(v){return getComputedStyle(document.documentElement).getPropertyValue(v).trim();}
  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function load(u){return GEO[u]||(GEO[u]=fetch(u).then(function(r){return r.json();}));}
  function init(fig){
    if(fig.dataset.on)return; fig.dataset.on='1';
    var D=JSON.parse(fig.querySelector('.vnm-d').textContent);
    load(fig.dataset.geo).then(function(G){draw(fig,G,D);});
  }
  function draw(fig,G,D){
    var svg=fig.querySelector('.vnm-svg'), box=fig.querySelector('.vnm-box'), pop=fig.querySelector('.vnm-pop'), hint=fig.querySelector('.vnm-hint');
    var st={mode:'ctz',lay:{},month:7};
    try{var s=JSON.parse(sessionStorage.getItem('vnm')||'{}');if(s.mode)st.mode=s.mode;if(s.lay)st.lay=s.lay;if(s.month)st.month=s.month;}catch(e){}
    function save(){try{sessionStorage.setItem('vnm',JSON.stringify({mode:st.mode,lay:st.lay,month:st.month}));}catch(e){}}
    // the year's places and their entries
    var at={}; D.e.forEach(function(x,i){x.p.forEach(function(p){(at[p]=at[p]||[]).push(i);});});
    // the first view: the RVN and the year's places
    var xs=[], ys=[]; G.prov.forEach(function(p){});
    var R=[1e9,1e9,-1e9,-1e9]; function ext(x,y){R[0]=Math.min(R[0],x);R[1]=Math.min(R[1],y);R[2]=Math.max(R[2],x);R[3]=Math.max(R[3],y);}
    Object.keys(at).forEach(function(k){var p=G.pl[k];if(p)ext(p[0],p[1]);});
    // the RVN's own extent (lon 102.1–109.5, lat 8.4–17.2) in the plane
    var rv=[[102.1,17.2],[109.5,8.4]].map(function(c){return [(c[0]-G.b[0])/(G.b[2]-G.b[0])*G.W, merc(c[1])];});
    function merc(lat){var m=function(l){return Math.log(Math.tan(Math.PI/4+l*Math.PI/360));};return (m(G.b[3])-m(lat))*G.W/((G.b[2]-G.b[0])*Math.PI/180);}
    ext(rv[0][0],rv[0][1]); ext(rv[1][0],rv[1][1]);
    var home; function fitHome(){var bw=box.clientWidth,bh=box.clientHeight,w=R[2]-R[0],h=R[3]-R[1],pad=0.06;
      var sc=Math.max(w*(1+2*pad)/bw,h*(1+2*pad)/bh);home={x:(R[0]+R[2])/2-bw*sc/2,y:(R[1]+R[3])/2-bh*sc/2,w:bw*sc,h:bh*sc};}
    fitHome(); var vb={x:home.x,y:home.y,w:home.w,h:home.h};
    var gL=el('g',{},svg), gR=el('g',{},svg), gP=el('g',{},svg), gS=el('g',{'class':'shade'},svg), gZ=el('g',{},svg), gO=el('g',{},svg), gW=el('g',{},svg), gD=el('g',{},svg), gT=el('g',{},svg), gH=el('g',{},svg);
    G.land.forEach(function(l){el('path',{d:l.d,'class':'ld'},gL);});
    var LN={laos:[102.6,19.4],cambodia:[104.9,12.9],thailand:[101.2,16.3],drv:[105.6,21.3],china:[106.5,23.3],myanmar:[100.0,21.4]};
    var lnames=G.land.map(function(l){var c=LN[l.id];if(!c)return null;var t=el('text',{'class':'ln'},gT);t.textContent=l.n==='Democratic Republic of Vietnam'?'North Vietnam':l.n;t._x=(c[0]-G.b[0])/(G.b[2]-G.b[0])*G.W;t._y=merc(c[1]);return t;}).filter(Boolean);
    var pv=G.prov.map(function(p){var e=el('path',{d:p.d,'class':'pv'},gP);e._p=p;var t=el('title',{},e);t.textContent=p.n+(p.p&&p.p!==p.n?' ('+p.p+')':'')+' · '+(ZN[p.z]||'')+' · '+p.r;return e;});
    var rvn=el('path',{d:G.prov.map(function(p){return p.d;}).join(''),'class':'rvn'},gO); rvn.remove();
    function zones(){gZ.textContent='';(st.mode==='reg'?G.reg:st.mode==='ctz'?G.zone:[]).forEach(function(z){el('path',{d:z.d,'class':'zb'},gZ);});}
    function color(){var f=typeof flat==='function'&&flat();pv.forEach(function(e){var p=e._p,c=st.mode==='ctz'?ZC[p.z]:st.mode==='reg'?RC[p.r]:null;e.setAttribute('fill',css(c||'--vpv'));e.setAttribute('fill-opacity',f?0.12:css('--vop'));});key();}
    // layers (sources/indochina), drawn when chosen; the rasters sharper as the zoom grows
    var LAY=G.lay||{}, lnodes={}, imgs=[], RW=[0.35,0.45,0.6,0.8,1.1,1.5,2.1];
    function flat(){return ['tint','koppen','rain'].some(function(k){return st.lay[k]&&LAY[k];});}
    function layer(k){
      var L=LAY[k]; if(!L) return;
      if(!st.lay[k]){ if(lnodes[k]) lnodes[k].style.display='none'; color(); return; }
      if(lnodes[k]){ lnodes[k].style.display=''; if(k==='rain') rain(); color(); return; }
      var g=el('g',{},k==='relief'?gS:(L.kind==='image'||L.kind==='grid')?gR:gW); lnodes[k]=g;
      if(L.kind==='image'){ var im=el('image',{href:L.src,x:L.box[0],y:L.box[1],width:L.box[2],height:L.box[3],preserveAspectRatio:'none',opacity:k==='relief'?0.55:0.85},g); im._L=L; imgs.push(im); sharpen(); }
      else if(L.kind==='rivers'){ load(L.src).then(function(R){
          R.l.forEach(function(l){ if(l.dy&&+l.dy>+D.y) return; var e=el('path',{d:l.d,'class':'lake'},g); if(l.n){var t=el('title',{},e);t.textContent=l.n;} });
          R.r.forEach(function(r){ var e=el('path',{d:r.d,'class':'riv','stroke-width':RW[Math.max(0,Math.min(6,(r.w||1)-1))]},g); if(r.n){var t=el('title',{},e);t.textContent=r.n;} }); }); }
      else if(L.kind==='lines'){ load(L.src).then(function(C){C.forEach(function(c){el('path',{d:c.d,'class':'ctr','stroke-dasharray':c.e===500?'3 2':null,'stroke-width':c.e>=1500?0.8:0.5},g);});}); }
      else if(L.kind==='grid'){ load(L.src).then(function(Rn){g._d=Rn;rain();}); }
      color();
    }
    function sharpen(){var z=home.w/vb.w;imgs.forEach(function(im){var L=im._L,h=(z>=6&&L.fine)?L.fine:(z>=2.2&&L.mid)?L.mid:L.src;if(im.getAttribute('href')!==h)im.setAttribute('href',h);});}
    function rain(){var g=lnodes.rain;if(!g||!g._d)return;g.textContent='';var Rn=g._d,m=st.month-1,sc=Rn.scale;
      Rn.cells.forEach(function(c){var v=c.v[m];if(v==null)return;var i=0;while(i<sc.length-1&&v>=sc[i+1])i++;
        var r=el('rect',{x:c.x,y:c.y,width:c.w+0.2,height:c.h+0.2,fill:'hsl(205,60%,'+(92-i*9)+'%)'},g);var t=el('title',{},r);t.textContent=v+' mm'+(c.t&&c.t[m]!=null?'; '+c.t[m]+' °C':'');});key();}
    // places
    var P=Object.keys(G.pl).map(function(k){var p=G.pl[k];return {k:k,x:p[0],y:p[1],n:p[2],kind:p[3],r:p[4]||3,c:p[5],hits:at[k]||[]};});
    P.sort(function(a,b){return (b.hits.length-a.hits.length)||(a.r-b.r);});
    P.forEach(function(p){ var on=p.hits.length>0; var c=el('circle',{'class':on?'dot':'dim',cx:p.x,cy:p.y},gD); p.el=c;
      c.addEventListener('click',function(ev){ev.stopPropagation();show(p);}); var t=el('title',{},c);t.textContent=p.n+(on?' · '+p.hits.length+(p.hits.length>1?' entries':' entry'):'');});
    function show(p){ if(!p.hits.length){pop.hidden=false;pop.innerHTML='<button type="button" class="x" aria-label="Close">×</button><b>'+esc(p.n)+'</b><div class="m">No entry placed here this year.</div>';return;}
      pop.hidden=false; pop.innerHTML='<button type="button" class="x" aria-label="Close">×</button><b>'+esc(p.n)+'</b> <span class="m">'+p.hits.length+(p.hits.length>1?' entries':' entry')+'</span><ol>'+
        p.hits.map(function(i){var x=D.e[i];return '<li><a href="'+esc(x.h)+'">'+esc(x.w)+'</a> <span class="m">'+esc(x.t)+'.</span> '+esc(x.s)+'</li>';}).join('')+'</ol>';}
    pop.addEventListener('click',function(e){if(e.target.classList.contains('x'))pop.hidden=true;});
    // the folded list
    fig.querySelector('.vnm-list ol').innerHTML=D.e.map(function(x){return '<li><a href="'+esc(x.h)+'">'+esc(x.w)+'</a> <span class="m">'+esc(x.t)+'.</span> '+esc(x.s)+(x.p.length?' <span class="m">('+x.p.map(function(k){return G.pl[k]?G.pl[k][2]:k;}).join(', ')+')</span>':'')+'</li>';}).join('');
    fig.querySelector('.vnm-list summary').textContent="The year's placed entries ("+D.e.length+')';
    // names: STYLE 3
    function names(){
      gH.textContent=''; var k=box.clientWidth/vb.w, fs=11.5/k, boxes=[], z=home.w/vb.w;
      function free(b){for(var i=0;i<boxes.length;i++){var o=boxes[i];if(b[0]<o[2]&&b[2]>o[0]&&b[1]<o[3]&&b[3]>o[1])return false;}return true;}
      P.forEach(function(p){
        var r=(p.hits.length?Math.max(2.6,Math.sqrt(p.hits.length)*2.4):1.8)/k; p.el.setAttribute('r',r);
        boxes.push([p.x-r,p.y-r,p.x+r,p.y+r]);
      });
      lnames.forEach(function(t){t.setAttribute('x',t._x);t.setAttribute('y',t._y);t.setAttribute('font-size',13/k);});
      P.forEach(function(p){
        var want=p.hits.length>0||p.r===1||(p.r===2&&z>=2.2)||(p.r===3&&z>=6);
        if(!want)return;
        if(p.x<vb.x||p.x>vb.x+vb.w||p.y<vb.y||p.y>vb.y+vb.h)return;
        var w=p.n.length*fs*0.56, h=fs, r=(p.hits.length?Math.max(2.6,Math.sqrt(p.hits.length)*2.4):1.8)/k, g=3/k;
        var spots=[[p.x+r+g,p.y+h*0.35,'start'],[p.x-r-g,p.y+h*0.35,'end'],[p.x,p.y-r-g,'middle'],[p.x,p.y+r+g+h*0.8,'middle']];
        for(var i=0;i<spots.length;i++){var s=spots[i],x0=s[2]==='start'?s[0]:s[2]==='end'?s[0]-w:s[0]-w/2,b=[x0,s[1]-h*0.85,x0+w,s[1]+h*0.2];
          if(free(b)){boxes.push(b);var t=el('text',{'class':'lb'+(p.hits.length?'':' o'),x:s[0],y:s[1],'text-anchor':s[2],'font-size':fs},gH);t.textContent=p.n;break;}}
      });
    }
    function view(){svg.setAttribute('viewBox',vb.x+' '+vb.y+' '+vb.w+' '+vb.h);names();sharpen();}
    function zoomAt(f,cx,cy){var nw=Math.max(home.w/MAXZ,Math.min(home.w*1.5,vb.w/f)),nh=nw*vb.h/vb.w;
      vb.x=cx-(cx-vb.x)*nw/vb.w;vb.y=cy-(cy-vb.y)*nh/vb.h;vb.w=nw;vb.h=nh;view();}
    function pt(ev){var r=svg.getBoundingClientRect();return [vb.x+(ev.clientX-r.left)/r.width*vb.w, vb.y+(ev.clientY-r.top)/r.height*vb.h];}
    svg.addEventListener('wheel',function(ev){ if(!(ev.ctrlKey||ev.metaKey)){hint.hidden=false;clearTimeout(hint._t);hint._t=setTimeout(function(){hint.hidden=true;},1200);return;}
      ev.preventDefault(); var p=pt(ev); zoomAt(Math.exp(-ev.deltaY*0.0025),p[0],p[1]); },{passive:false});
    var ptrs={}, last=null, pinch=null;
    svg.addEventListener('pointerdown',function(ev){svg.setPointerCapture(ev.pointerId);ptrs[ev.pointerId]=[ev.clientX,ev.clientY];svg.classList.add('drag');last=[ev.clientX,ev.clientY];
      var ids=Object.keys(ptrs);if(ids.length===2){var a=ptrs[ids[0]],b=ptrs[ids[1]];pinch=Math.hypot(a[0]-b[0],a[1]-b[1]);}});
    svg.addEventListener('pointermove',function(ev){if(!ptrs[ev.pointerId])return;ptrs[ev.pointerId]=[ev.clientX,ev.clientY];var r=svg.getBoundingClientRect(),ids=Object.keys(ptrs);
      if(ids.length===2&&pinch){var a=ptrs[ids[0]],b=ptrs[ids[1]],d=Math.hypot(a[0]-b[0],a[1]-b[1]);var c=pt({clientX:(a[0]+b[0])/2,clientY:(a[1]+b[1])/2});zoomAt(d/pinch,c[0],c[1]);pinch=d;return;}
      if(last){vb.x-=(ev.clientX-last[0])/r.width*vb.w;vb.y-=(ev.clientY-last[1])/r.height*vb.h;last=[ev.clientX,ev.clientY];svg.setAttribute('viewBox',vb.x+' '+vb.y+' '+vb.w+' '+vb.h);}});
    function up(ev){delete ptrs[ev.pointerId];if(Object.keys(ptrs).length<2)pinch=null;if(!Object.keys(ptrs).length){svg.classList.remove('drag');last=null;names();sharpen();}}
    svg.addEventListener('pointerup',up);svg.addEventListener('pointercancel',up);
    svg.addEventListener('dblclick',function(ev){var p=pt(ev);zoomAt(2,p[0],p[1]);});
    fig.querySelector('.vnm-z').addEventListener('click',function(ev){var z=ev.target.dataset.z;if(!z)return;
      if(z==='home'){vb={x:home.x,y:home.y,w:home.w,h:home.h};view();return;}
      zoomAt(z==='in'?1.8:1/1.8,vb.x+vb.w/2,vb.y+vb.h/2);});
    // controls
    var bar=fig.querySelector('.vnm-bar');
    var h='<span class="seg" data-k="mode"><button type="button" data-v="ctz">Corps zones</button><button type="button" data-v="reg">Regions</button><button type="button" data-v="plain">Provinces</button></span>';
    var LN2={relief:'Relief',tint:'Elevation',contours:'Contours',rivers:'Rivers',koppen:'Climate',rain:'Rain'};
    Object.keys(LN2).forEach(function(k){if(LAY[k])h+='<label><input type="checkbox" data-l="'+k+'"'+(st.lay[k]?' checked':'')+'> '+LN2[k]+'</label>';});
    if(LAY.rain)h+='<select data-m aria-label="Month">'+['Jan.','Feb.','Mar.','Apr.','May','June','July','Aug.','Sept.','Oct.','Nov.','Dec.'].map(function(m,i){return '<option value="'+(i+1)+'"'+(i+1===st.month?' selected':'')+'>'+m+'</option>';}).join('')+'</select>';
    bar.innerHTML=h;
    function seg(){bar.querySelectorAll('.seg button').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.v===st.mode));});}
    bar.addEventListener('click',function(ev){var b=ev.target.closest('.seg button');if(!b)return;st.mode=b.dataset.v;save();seg();zones();color();});
    bar.addEventListener('change',function(ev){var t=ev.target;if(t.dataset.l){st.lay[t.dataset.l]=t.checked;save();layer(t.dataset.l);key();}else if(t.hasAttribute('data-m')){st.month=+t.value;save();rain();}});
    function key(){var k=fig.querySelector('.vnm-key'),s='';
      function sw(c,t){return '<span><i style="background:'+css(c)+';opacity:'+css('--vop')+'"></i>'+t+'</span>';}
      if(st.mode==='ctz')s=Object.keys(ZN).map(function(z){return sw(ZC[z],ZN[z]);}).join('');
      else if(st.mode==='reg')s=Object.keys(RC).map(function(r){return sw(RC[r],r);}).join('');
      s+='<span><i style="background:'+css('--vdot')+';border-radius:50%"></i>this year\'s entries, by number</span>';
      function leg(L){return L.legend.map(function(c){return '<span><i style="background:'+c.color+'"></i>'+esc(c.code)+(c.name?' '+esc(c.name):'')+'</span>';}).join('');}
      if(st.lay.tint&&LAY.tint)s+=leg(LAY.tint);
      if(st.lay.koppen&&LAY.koppen)s+='<span>Köppen–Geiger, 1961–1990:</span>'+leg(LAY.koppen);
      if(st.lay.rain&&LAY.rain){var sc=[0,25,50,100,200,300,400,500];s+='<span>Rain, '+['Jan.','Feb.','Mar.','Apr.','May','June','July','Aug.','Sept.','Oct.','Nov.','Dec.'][st.month-1]+', mean of 1961–1990, mm:</span>'+sc.map(function(v,i){return '<span><i style="background:hsl(205,60%,'+(92-i*9)+'%)"></i>'+v+(i===sc.length-1?'+':'')+'</span>';}).join('');}
      var cr=[];if(st.lay.relief||st.lay.tint||st.lay.contours)cr.push('relief: NOAA, ETOPO 2022');if(st.lay.rivers)cr.push('rivers and lakes: HydroSHEDS v1, © World Wildlife Fund, Inc. (2006–2022), used under license; SWORD v17c');
      if(st.lay.koppen)cr.push('climate: Beck et al. (2023), CC BY 4.0');if(st.lay.rain)cr.push('rain: CRU CL 2.0, Climatic Research Unit, University of East Anglia, ODbL');
      if(cr.length)s+='<span class="cr">Layers: '+esc(cr.join('; '))+'. <a href="https://github.com/impending2223/bib/blob/main/sources/indochina/README.md">Sources and licenses</a></span>';
      k.innerHTML=s;}
    seg(); zones(); color(); Object.keys(st.lay).forEach(layer); gO.appendChild(rvn); view();
    new ResizeObserver(function(){var r=vb.w/home.w;fitHome();var cx=vb.x+vb.w/2,cy=vb.y+vb.h/2;vb.w=home.w*r;vb.h=home.h*r;vb.x=cx-vb.w/2;vb.y=cy-vb.h/2;view();}).observe(box);
    function retheme(){color();names();} matchMedia('(prefers-color-scheme: dark)').addEventListener('change',retheme);
    new MutationObserver(retheme).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
  }
  var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.unobserve(e.target);init(e.target);}});},{rootMargin:'600px'}):null;
  document.querySelectorAll('figure.vnm').forEach(function(f){io?io.observe(f):init(f);});
})();
</script>"""
