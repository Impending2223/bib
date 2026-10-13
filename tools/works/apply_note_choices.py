"""Once: fold the listings' notes into the cards (Oct. 13, 2026), as the owner chose them in the Card Notes page.

    python3 tools/works/apply_note_choices.py DIR [--dry-run]

DIR holds notes-data.json (the items the page offered) and choices/*.json (the page's saved choices, one a work or
listing: pick A/B/C (that note), all, none, text (the owner's own); for a listing of several works: each, first,
drop, text (on each)). Every other note on a listing of one work (a work with one note among its listings) becomes
the card's note. Afterwards no listing of a work carries a note.
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bib import store, works  # noqa: E402


def stored_note(e):
    d = e.get("_derived") or {}
    return d.get("n", (None, e.get("n")))[1]


def clear_note(e):
    """Take the listing's own note off (store.stored_form writes the derived value back as absent)."""
    if "_derived" in e and "n" in e["_derived"]:
        shown = e["_derived"]["n"][0]
        e["_derived"]["n"] = (shown, None)
        if shown is None:
            e.pop("n", None)
        else:
            e["n"] = shown
    else:
        e.pop("n", None)


def main(d, dry):
    items = json.load(open(os.path.join(d, "notes-data.json")))
    offered = {x["k"]: x for x in items["notes"]}
    groups = {x["k"]: x for x in items["groups"]}
    picks = {}
    for f in glob.glob(os.path.join(d, "choices", "*.json")):
        x = json.load(open(f))
        x = x.get("data", x)
        picks[x["k"]] = x
    series = store.Series()
    cat = series.works
    where = works.where(series)
    touched = set()
    n_card = n_auto = n_group = 0
    for cid, us in where.items():
        card = cat.get(cid)
        singles = [(l, s, e) for l, s, e in us if not isinstance(e.get("work"), list)]
        if cid in offered:
            x, p = offered[cid], picks.get(cid)
            if p is None:
                print("no choice for", cid)
                continue
            texts = [o["text"] for o in x["notes"]]
            pick = p["pick"]
            if pick == "text":
                note = p["text"]
            elif pick == "all":
                note = " ".join(texts)
            elif pick == "none":
                note = None
            else:
                note = texts["ABCDEFG".index(pick)]
            if note:
                card["n"] = note
            else:
                card.pop("n", None)
            n_card += 1
        else:
            notes = [stored_note(e) for _, _, e in singles if stored_note(e)]
            if notes:
                if not card.get("n"):
                    card["n"] = notes[0]
                n_auto += 1
        for l, s, e in singles:
            if stored_note(e):
                clear_note(e)
                touched.add(id(s))
                touched_secs[id(s)] = s
    for l in series.lists.values():
        for s, e in l.entries():
            if e["id"] not in groups or not isinstance(e.get("work"), list):
                continue
            p = picks.get(e["id"])
            if p is None:
                print("no choice for", e["id"])
                continue
            text = groups[e["id"]]["text"] if p["pick"] in ("each", "first") else p.get("text")
            targets = {"each": e["work"], "first": e["work"][:1], "text": e["work"], "drop": []}[p["pick"]]
            for cid in targets:
                c = cat.get(cid)
                c["n"] = " ".join(x for x in (c.get("n"), text) if x)
            clear_note(e)
            touched_secs[id(s)] = s
            n_group += 1
    print(f"{n_card} chosen card notes, {n_auto} single notes moved, {n_group} grouped listings settled")
    if not dry:
        for s in touched_secs.values():
            series.save_section(s)
        cat.save()


touched_secs = {}

if __name__ == "__main__":
    main(sys.argv[1], "--dry-run" in sys.argv)
