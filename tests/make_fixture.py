"""Write tests/fixture: a small frozen slice of the real data, a tree of the repository's layout (BIB_ROOT).

    python3 tests/make_fixture.py            # from this checkout's data, into tests/fixture (replaced whole)

The slice:
- series.yaml, cut to the lists the slice holds;
- the calendar's threads (th.yaml) and two months (MONTHS), verbatim; list.yaml cut to them;
- the Part III entries, in any list, of the persons the months tag (name:<key>), and the Executive roster's units
  with their holders of the months' year (YEAR);
- the witnesses the slice cites (sources/witnesses/), the edges its "via" rows walk (by-work/), and the
  witnesses and cards those name;
- the works cards the slice cites, and the cards those cite, to a fixed point;
- the 87th Congress at its opening, the small congress/ files, the gazetteer, the templates, and every file of
  sources/ of SMALL bytes or less (WHOLE, SMALL); a few larger hand files (EXTRA).
Files the slice does not need are left out: the modules read a missing file as empty, and the check's complaints
about what is missing (an entry's link to another month, a race in a year not held) are part of the golden.

The fixture is frozen: regenerate it only deliberately, and rewrite the goldens with it (pytest --update-goldens),
saying why in the commit. The output depends only on the data it is cut from.
"""
import os
import re
import shutil
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
OUT = os.path.join(HERE, "fixture")
os.environ.pop("BIB_ROOT", None)
sys.path.insert(0, os.path.join(SRC, "tools"))
from bib import store  # noqa: E402

MONTHS = ["196104", "196108"]
YEAR = "1961"
WHOLE = [                                # copied as they are
    "templates",
    "congress/87.yaml", "congress/switches.yaml", "congress/changes.yaml", "congress/specials.yaml",
    "congress/specials-cq.yaml", "congress/specials-state.yaml", "congress/bills.yaml",
    "congress/appropriations.yaml", "congress/committees-hand.yaml",
    "sources/places.yaml", "sources/dsb-issues.yaml", "sources/states.yaml",
]
SMALL = 25 * 1024                        # and every file of sources/ this small
EXTRA = []                               # larger files the check or the build needs whole (none yet)


def src(*p):
    return os.path.join(SRC, *p)


def out(*p):
    return os.path.join(OUT, *p)


def copy(rel):
    s, d = src(rel), out(rel)
    if os.path.exists(d):
        return
    os.makedirs(os.path.dirname(d), exist_ok=True)
    if os.path.isdir(s):
        shutil.copytree(s, d)
    else:
        shutil.copy2(s, d)


def load(rel):
    with open(src(rel), encoding="utf-8") as f:
        return yaml.load(f, Loader=store._Loader)


def header(rel):
    """A file's own leading comment lines."""
    lines = []
    with open(src(rel), encoding="utf-8") as f:
        for line in f:
            if not line.startswith("#"):
                break
            lines.append(line[1:].strip())
    return lines


def dump(obj, rel, note):
    os.makedirs(os.path.dirname(out(rel)), exist_ok=True)
    store.dump_yaml(obj, out(rel), header=header(rel) + [f"tests/make_fixture.py: {note}"])


def cut_sections(secs, keep):
    """The outline with only the sections whose file is kept (and their parents)."""
    res = []
    for s in secs:
        s = dict(s)
        kids = cut_sections(s.get("sections") or [], keep)
        if kids:
            s["sections"] = kids
        else:
            s.pop("sections", None)
        if kids or s.get("file") in keep:
            res.append(s)
    return res


def walk_files(secs):
    for s in secs:
        if s.get("file"):
            yield s["file"], s
        yield from walk_files(s.get("sections") or [])


def text_of(obj):
    return yaml.safe_dump(obj, allow_unicode=True, width=10**9)


def cards_in(obj):
    return set(re.findall(r"\b(w\.[a-z0-9][a-z0-9.-]*[a-z0-9])", text_of(obj)))


def witnesses_in(obj):
    return set(re.findall(r"\b(x\.(?:\d{4}(?:-\d\d(?:-\d\d)?)?|undated)\.[a-z0-9][a-z0-9-]*)", text_of(obj)))


def person_keys(e):
    from bib.lives import key_of
    return {key_of(re.sub(r"\s*\(.*?\)\s*$", "", n)) for n in re.split(r";\s*", e.get("s") or "") if n.strip()}


def overlaps(h, year):
    a, b = str(h.get("from") or "0000"), str(h.get("to") or "9999")
    return a[:4] <= year <= b[:4]


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    note = "cut to the fixture's slice"

    # the calendar: its threads and two months, verbatim
    cal = load("lists/cal/list.yaml")
    keep = {"th.yaml"} | {m + ".yaml" for m in MONTHS}
    cal["sections"] = cut_sections(cal["sections"], keep)
    # the parts (a page a half year, calsplit.py): those the months fall in, the first without its `from`
    firsts = [m[:4] + "-" + m[4:] + "-01" for m in MONTHS]
    parts = cal.get("split") or []
    starts = [str(p.get("from") or "0000") for p in parts] + ["9999"]
    parts = [p for i, p in enumerate(parts) if any(starts[i] <= d < starts[i + 1] for d in firsts)]
    if parts:
        parts[0] = {k: v for k, v in parts[0].items() if k != "from"}
        cal["split"] = parts
    cal["retired_parts"] = [p for p in cal.get("retired_parts") or []
                            if any(str(p["from"]) <= d <= str(p["to"]) for d in firsts)]
    dump(cal, "lists/cal/list.yaml", f"the outline {note}")
    entries = []
    for f in sorted(keep):
        copy(f"lists/cal/{f}")
        entries += (load(f"lists/cal/{f}") or {}).get("entries") or []
    names = {t[5:] for e in entries for t in e.get("tags") or [] if t.startswith("name:")}

    # Part III, in every list: the persons the months tag
    series = load("series.yaml")
    held = ["cal"]
    for meta in series["lists"]:
        key = meta["key"]
        if key == "cal" or not os.path.exists(src("lists", key, "list.yaml")):
            continue
        lm = load(f"lists/{key}/list.yaml")
        kept = {}
        for path, d in walk_files(lm["sections"]):
            if not (d.get("num") or "").startswith("III"):
                continue
            doc = load(f"lists/{key}/{path}") or {}
            es = [e for e in doc.get("entries") or [] if person_keys(e) & names]
            if es:
                doc["entries"] = es
                kept[path] = doc
                entries += es
        if not kept:
            continue
        held.append(key)
        lm["sections"] = cut_sections(lm["sections"], set(kept))
        dump(lm, f"lists/{key}/list.yaml", f"the outline {note}")
        for path, doc in kept.items():
            dump(doc, f"lists/{key}/{path}", "the persons the fixture's months tag")
    series["lists"] = [m for m in series["lists"] if m["key"] in held]
    dump(series, "series.yaml", "the lists the fixture holds")

    # the Executive roster: the units a person the months tag held office in in YEAR (and the units above them),
    # each with its heads and those persons' offices, and their holders of YEAR
    from bib.lives import key_of
    units = {}
    for f in sorted(os.listdir(src("executive"))):
        if f.endswith(".yaml"):
            u = load(f"executive/{f}") or {}
            offices = []
            for o in u.get("offices") or []:
                hs = [h for h in o.get("holders") or [] if overlaps(h, YEAR)]
                if hs and (o.get("rank") == "head" or any(key_of(h["name"]) in names for h in hs)):
                    offices.append(dict(o, holders=hs))
            u["offices"] = offices
            units[f] = u
    by_id = {u.get("unit"): f for f, u in units.items()}
    take = {f for f, u in units.items()
            if any(key_of(h["name"]) in names for o in u["offices"] for h in o["holders"])}
    for f in list(take):
        up = units[f].get("under")
        while up in by_id and by_id[up] not in take:
            take.add(by_id[up])
            up = units[by_id[up]].get("under")
    for f in sorted(take):
        dump(units[f], f"executive/{f}", f"the holders of {YEAR}")

    # witnesses: those the slice names, the edges its via rows walk, and what those name
    wrows, wfile = {}, {}
    wfiles = [f"{d}/{f}" for d in ("sources/witnesses", "inbox/witnesses") if os.path.isdir(src(d))
              for f in sorted(os.listdir(src(d))) if f.endswith(".yaml")]
    for f in wfiles:
        for r in load(f) or []:
            if isinstance(r, dict) and r.get("id"):
                wrows[r["id"]] = r
                wfile[r["id"]] = f
    vias = {}
    for e in entries:
        for row in (e.get("src") or {}).get("rows") or []:
            m = re.match(r"via (w\.[a-z0-9.-]+) (.+?): ", str(row))
            if m:
                vias.setdefault(m.group(1), set()).add(m.group(2))
    edges = {}
    for card, ats in vias.items():
        p = f"sources/witnesses/by-work/{card[2:]}.yaml"
        if os.path.exists(src(p)):
            edges[p] = [ed for ed in load(p) or [] if isinstance(ed, dict) and str(ed.get("at")) in ats]
    want_w, todo = set(), witnesses_in(entries) | witnesses_in(list(edges.values()))
    while todo:
        wid = todo.pop()
        if wid in want_w or wid not in wrows:
            continue
        want_w.add(wid)
        todo |= witnesses_in(wrows[wid]) - want_w
    byfile = {}
    for wid in sorted(want_w):
        byfile.setdefault(wfile[wid], []).append(wrows[wid])
    for f in wfiles:
        amends = [r for r in load(f) or [] if isinstance(r, dict) and r.get("amend") in want_w]
        if byfile.get(f) or amends:
            dump(byfile.get(f, []) + amends, f, "the witnesses the fixture's slice names")
    for p, es in edges.items():
        if es:
            dump(es, p, "the edges the fixture's via rows walk")

    # works: the cards cited, and the cards they cite (to a fixed point)
    cards = {}
    for f in sorted(os.listdir(src("works"))):
        if f.endswith(".yaml"):
            for c in (load(f"works/{f}") or {}).get("cards") or []:
                cards[c["id"]] = (f, c)
                for a in c.get("aliases") or []:
                    cards.setdefault(a, (f, c))
    want, todo = set(), cards_in(entries) | cards_in([wrows[w] for w in want_w]) | cards_in(list(edges.values()))
    todo |= {"w." + os.path.basename(p)[:-5] for p, es in edges.items() if es}
    while todo:
        cid = todo.pop()
        if cid in want or cid not in cards:
            continue
        want.add(cid)
        todo |= cards_in(cards[cid][1]) - want
    keep_cards = {}
    for cid in want:
        f, c = cards[cid]
        keep_cards.setdefault(f, set()).add(c["id"])
    for f in sorted(os.listdir(src("works"))):
        if f.endswith(".yaml"):
            doc = load(f"works/{f}") or {}
            doc["cards"] = [c for c in doc.get("cards") or [] if c["id"] in keep_cards.get(f, ())]
            dump(doc, f"works/{f}", "the cards the fixture's slice cites")
        elif os.path.isfile(src("works", f)):
            copy(f"works/{f}")

    for rel in WHOLE + EXTRA:
        copy(rel)
    for f in sorted(os.listdir(src("sources"))):
        if os.path.isfile(src("sources", f)) and os.path.getsize(src("sources", f)) <= SMALL:
            copy(f"sources/{f}")
    total = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(OUT) for f in fs)
    print(f"tests/fixture: {total // 1024} KB in {sum(len(fs) for _, _, fs in os.walk(OUT))} files; "
          f"lists {', '.join(held)}; {len(want)} cards, {len(want_w)} witnesses")


if __name__ == "__main__":
    main()
