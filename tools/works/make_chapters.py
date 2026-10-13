"""Once: the chapters the lists cite as text ('Author, *Chapter*, *in* *Volume* 127 (Ed. ed., 2006)') become chapter
cards pointing to volume cards (`in:`), one volume card for every chapter whose volume is printed alike. A chapter is
converted only where the cards render its citation exactly as before.

    python3 tools/works/make_chapters.py [--dry-run]
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bib import store, works  # noqa: E402

RX = re.compile(r"^(?P<auth>[^*]+?), \*(?P<title>[^*]+)\*, \*in\* \*(?P<vt>[^*]+)\*(?:(?:, at | )(?P<page>\d+))?"
                r" \((?P<paren>[^()]+)\)(?: \(\[online\]\((?P<online>[^)\s]+)\)\))?$")


def main(dry):
    series = store.Series()
    cat = series.works
    vols = {}                        # (title, paren, online) -> volume card id
    taken = set(cat.cards)
    n = 0
    skipped = []
    for cid, c in list(cat.cards.items()):
        m = RX.match(c.get("c") or "")
        if not m:
            continue
        authors = works.split_names(m.group("auth"))
        pa = works.parse_paren(m.group("paren"))
        key = (m.group("vt"), m.group("paren"), m.group("online"))
        vid = vols.get(key)
        vol = {"title": m.group("vt"), **pa}
        if m.group("online"):
            vol["online"] = m.group("online")
        if vid is None:
            vid = works.new_id({"title": m.group("vt"), "author": vol.get("editor"), "year": pa.get("year")}, taken)
            taken.add(vid)
        chap = {"id": cid, "kind": "chapter", "author": authors, "title": m.group("title"), "in": vid}
        if m.group("page"):
            chap["page"] = m.group("page")
        trial = dict(cat.cards)
        trial[vid] = {"id": vid, "kind": "volume", **vol}
        tcat = type("T", (), {"get": lambda self, i: trial.get(i)})()
        if works.render(chap, cat=tcat) != c["c"] or not all(works.is_person(a) for a in authors):
            skipped.append(c["c"])
            continue
        vols[key] = vid
        cat.cards[vid] = trial[vid]
        cat.file_of[vid] = f"{works.letter(vid)}.yaml"
        keep = {k: v for k, v in c.items() if k in ("n", "tags", "aliases")}
        cat.cards[cid] = {**chap, **keep}
        n += 1
    print(f"{n} chapters, {len(vols)} volumes; not converted: {len(skipped)}")
    for x in skipped:
        print("  ", x)
    if not dry:
        cat.save()


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
