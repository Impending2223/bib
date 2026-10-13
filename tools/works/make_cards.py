"""Once: make the works catalogue from the lists as they stand (Phase 1), and point the list entries at it.

    python3 tools/works/make_cards.py [--dry-run]

A card for each work a list entry cites (tools/bib/works.py: `fields_of`), one card for every printing of the same
citation; near-variants stay separate cards (notes/works-inventory.md lists them). An entry whose every citation line
is a work gets `work:` in place of `c`; an entry mixing works with primary documents keeps its `c`. Notes: a work listed
once, by an entry citing it alone, gives its note to the card (the card note); a work listed several times with one note
on every such listing gives that note to the card; otherwise the notes stay with their listings. Under a person's subject
line, a citation that names its author anyway gets `byline: true`. Nothing shown changes: the build before and after is
compared page by page.
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bib import store, works  # noqa: E402
from bib.refs import Refs  # noqa: E402
from bib.markup import plain  # noqa: E402


def card_id(f, taken):
    who = store.slug(works.surname(f["author"][0]), 3) if f.get("author") else ""
    t = re.sub(r"^(the|a|an)-", "", store.slug(works.short_title(plain(f["title"])), 6))
    t = "-".join(t.split("-")[:4])
    base = "w." + "-".join(x for x in (who, t) if x)
    cid = base
    if cid in taken and f.get("year"):
        cid = f"{base}-{store.slug(str(f['year']), 2)}"
    n = 2
    while cid in taken:
        cid, n = f"{base}-{n}", n + 1
    return cid


def main(dry=False):
    series = store.Series()
    if series.works.cards:
        sys.exit("works/ already holds cards: this script runs once")
    refs = Refs(series)
    cards = {}                     # the full citation (author written) -> card
    uses = collections.defaultdict(list)    # card id -> [(list, section, entry, single)]
    plan = {}                      # entry id -> [card ids]
    byline = {}                    # entry id -> the cards it prints with the author
    ditto = set()                  # entries naming one author once for several works
    taken = set()
    for lst in series.lists.values():
        if lst.kind == "calendar":
            continue
        for sec, e in lst.entries():
            cs = store.as_list(e.get("c"))
            if not cs:
                continue
            subj = e.get("s") if refs.is_person(lst, sec, e) else None
            fs = [works.fields_of(c, subj) for c in cs]
            if any(f is None for f in fs):
                continue                       # mixes works with documents: stays as written
            # a listing of one author's works names the author at the first only: the rest take it (ditto)
            for i in range(1, len(fs)):
                if not fs[i].get("author") and fs[i - 1].get("author") and cs[i].lstrip().startswith("*") \
                        and not fs[i].get("editor") and not fs[i - 1].get("_subject"):
                    fs[i]["author"] = list(fs[i - 1]["author"])
                    fs[i]["_ditto"] = True
                    ditto.add(e["id"])
            ids = []
            for c, f in zip(cs, fs):
                if f.get("c"):                 # verbatim; printed from the title on (a subject, a ditto), its author a field
                    card = {"c": c, "author": f["author"]} if f.get("_subject") or f.get("_ditto") else {"c": c}
                    full = works.render(card)
                else:
                    card = {k: v for k, v in f.items() if not k.startswith("_")}
                    full = works.render(card)
                if full not in cards:
                    cid = card_id(f, taken)
                    taken.add(cid)
                    cards[full] = {"id": cid, **card}
                cid = cards[full]["id"]
                ids.append(cid)
                uses[cid].append((lst, sec, e, len(cs) == 1))
                # a person's listing that prints the author: say so, or the rendering would drop it
                if subj and not f.get("_subject") and cards[full].get("author") and \
                        store.fold(cards[full]["author"][0]) == store.fold(works.subject_name(subj)):
                    byline.setdefault(e["id"], []).append(cid)
            plan[e["id"]] = ids
    # notes
    card_notes = {}
    for cid, us in uses.items():
        singles = [e for _, _, e, single in us if single]
        notes = [e.get("n") for e in singles]
        if singles and len(singles) == len(us) and notes[0] and all(n == notes[0] for n in notes):
            card_notes[cid] = notes[0]
    by_id = {c["id"]: c for c in cards.values()}
    for cid, n in card_notes.items():
        by_id[cid]["n"] = n
    # write
    cat = series.works
    for c in cards.values():
        cat.cards[c["id"]] = c
    n_entries = 0
    for lst in series.lists.values():
        for sec in lst.walk():
            changed = False
            for e in sec.entries:
                ids = plan.get(e["id"])
                if not ids:
                    continue
                e["work"] = ids if isinstance(e.get("c"), list) else ids[0]
                del e["c"]
                if len(ids) == 1 and ids[0] in card_notes:
                    e.pop("n", None)
                if e["id"] in ditto:
                    e["ditto"] = True
                if e["id"] in byline:      # every line, or only some of a listing's several
                    e["byline"] = True if len(byline[e["id"]]) == len(ids) else byline[e["id"]]
                changed = True
                n_entries += 1
            if changed and not dry:
                series.save_section(sec)
    if not dry:
        cat.save()
    print(f"{len(cards)} cards ({sum(1 for c in cards.values() if not c.get('c'))} structured), {n_entries} entries "
          f"pointed, {len(card_notes)} card notes, {len(byline)} bylines")


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
