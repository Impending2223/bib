"""The countries around the RVN for the calendar's maps (one-time, Oct. 21, 2026):
sources/vn-provinces-1966/indochina-outline.geojson, from Natural Earth's 10m admin-0 countries clipped to
lon 99.5–111, lat 7.5–24, the DRV being Vietnam less the RVN of provinces1966.geojson.
python3 -I tools/vnmap/outline.py NE_ADMIN0_GEOJSON"""
import json, os, sys
from shapely.geometry import shape, mapping, box
from shapely.ops import unary_union

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "sources", "vn-provinces-1966")
CLIP = box(99.5, 7.5, 111.0, 24.0)
KEEP = {"Vietnam": "vn", "Laos": "laos", "Cambodia": "cambodia", "Thailand": "thailand", "China": "china",
        "Myanmar": "myanmar"}
NAME = {"vn": "Democratic Republic of Vietnam", "laos": "Laos", "cambodia": "Cambodia", "thailand": "Thailand",
        "china": "China", "myanmar": "Burma"}


def rnd(c):
    return [rnd(x) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], 4), round(c[1], 4)]


def main():
    ne = json.load(open(sys.argv[1]))
    rvn = unary_union([shape(f["geometry"]).buffer(0) for f in
                       json.load(open(os.path.join(ROOT, "provinces1966.geojson")))["features"]])
    out = []
    for f in ne["features"]:
        k = KEEP.get(f["properties"].get("ADMIN") or f["properties"].get("NAME"))
        if not k:
            continue
        g = shape(f["geometry"]).buffer(0).intersection(CLIP)
        if k == "vn":
            g = g.difference(rvn.buffer(0.01))     # what is left south of the DMZ is slivers of two coastlines
            g = unary_union([p for p in getattr(g, "geoms", [g]) if p.geom_type == "Polygon" and p.centroid.y > 16.9])
        g = g.simplify(0.004, preserve_topology=True)
        if g.is_empty:
            continue
        m = mapping(g)
        out.append({"type": "Feature", "properties": {"id": "drv" if k == "vn" else k, "name": NAME[k]},
                    "geometry": {"type": m["type"], "coordinates": rnd(m["coordinates"])}})
    json.dump({"type": "FeatureCollection", "features": out},
              open(os.path.join(ROOT, "indochina-outline.geojson"), "w"), ensure_ascii=False, separators=(",", ":"))
    print(len(out), "countries")


if __name__ == "__main__":
    main()
