"""Merge a batch's continued responses page by page: pages(paths) -> {title: page}; redirects(paths) -> {from: to}"""
import json
def pages(paths):
    out = {}
    for path in paths:
        for p in json.load(open(path))["query"]["pages"]:
            q = out.setdefault(p["title"], {"title": p["title"]})
            for k, v in p.items():
                if k in ("coordinates", "revisions"):
                    q.setdefault(k, [])
                    q[k] += [x for x in v if x not in q[k]]
                else:
                    q.setdefault(k, v)
    return out
def redirects(paths):
    r = {}
    for path in paths:
        q = json.load(open(path))["query"]
        for x in q.get("normalized", []) + q.get("redirects", []):
            r[x["from"]] = x["to"]
    return r
def resolve(t, r):
    seen = set()
    while t in r and t not in seen:
        seen.add(t); t = r[t]
    return t
if __name__ == "__main__":
    import sys
    P = pages(sys.argv[1:])
    for t, p in sorted(P.items()):
        c = p.get("coordinates")
        print(t, "MISSING" if p.get("missing") else "", (round(c[0]["lat"], 4), round(c[0]["lon"], 4)) if c else "NO-COORD")
