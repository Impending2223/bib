"""Combine the map layers into one JSON for the page, rings clockwise (d3's spherical winding), 3 decimals."""
import json, re
from shapely.geometry import shape, mapping
from shapely.geometry.polygon import orient
from shapely.geometry import MultiPolygon, Polygon

def cw(geom):
    g = shape(geom)
    if isinstance(g, Polygon):
        g = orient(g, sign=-1.0)
    elif isinstance(g, MultiPolygon):
        g = MultiPolygon([orient(p, sign=-1.0) for p in g.geoms])
    m = mapping(g)
    def rnd(c):
        return [rnd(x) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], 3), round(c[1], 3)]
    return {"type": m["type"], "coordinates": rnd(m["coordinates"])}

def layer(path, keep=None):
    fc = json.load(open(path))
    out = []
    for f in fc["features"]:
        p = f["properties"] if keep is None else {k: f["properties"].get(k) for k in keep}
        out.append({"type": "Feature", "properties": p, "geometry": cw(f["geometry"])})
    return {"type": "FeatureCollection", "features": out}

import yaml
xw = {u["id"]: u for u in yaml.safe_load(open("crosswalk.yaml"))["units"]}
import unicodedata
def sp(t):
    t = unicodedata.normalize("NFC", t or "")
    return "".join((" " + c) if i and c.isupper() and t[i - 1].islower() else c for i, c in enumerate(t))
data = {
    "provinces": layer("provinces1966.geojson", ["id", "name", "plain", "kind", "capital", "ctz", "region", "confidence"]),
    "ctz": layer("ctz1966.geojson", ["ctz", "name"]),
    "regions": layer("regions.geojson", ["region"]),
    "outline": layer("outline.geojson", ["name", "kind"]),
    "places": json.load(open("places.json")),
}
for f in data["provinces"]["features"]:
    u = xw.get(f["properties"]["id"], {})
    f["properties"]["note"] = u.get("note")
    f["properties"]["area"] = u.get("area_km2_gadm")
    f["properties"]["today"] = sorted({f"{sp(d['name_2'])} ({sp(d['name_1'])})" for d in u.get("districts", [])})
    f["properties"]["src"] = (u.get("sources") or [None])[-1]
s = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
open("page/data.json", "w").write(s)
print(len(s) // 1024, "KB")
