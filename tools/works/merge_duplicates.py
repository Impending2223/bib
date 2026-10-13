"""Once: fold the cards that are one work written twice into one (the owner's request, Oct. 13, 2026).

    python3 tools/works/merge_duplicates.py [--dry-run]

A group is the cards with the same first author (a film's director), the same main title (its leading article aside)
and the same year. The card kept is the fullest citation (the longest), unless KEEP names it (where the longer is the
wrong title or name); NOT_ONE keeps apart cards that only look alike (a volume and its set). works.combine does the
folding: the other id stays an alias, every listing and [[w.…]] follows, the notes are joined (a bare "Also …"
pointer gives way).
"""
import collections
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bib import store, works  # noqa: E402
from bib.markup import plain  # noqa: E402

NOT_ONE = {"w.foreign-relations-of-the-2003", "w.foreign-relations-of-the-3",   # vol. 7, and the set
           "w.gibbons-u-s-government-and-1986"}                                  # Pt. 1, and the set
KEEP = {
    "w.sorley-better-war",                 # "and Final Tragedy", as printed
    "w.sorley-thunderbolt",                # the 1992 subtitle (the longer is the 2005 reissue's)
    "w.statler-replacing-france",          # Kathryn
    "w.johnson-vantage-point",             # "Perspectives of the Presidency"
    "w.advise-and-consent",                # Advise & Consent, as the film is titled
    "w.white-for-president-kennedy",       # the article as printed in Life
    "w.chapman-cauldron-of-resistance",    # the title as printed, without the marks
    "w.miller-misalliance",
    "w.halberstam-best-and-the-brightest",  # the other carries a stray page, "553"
}


def groups(series):
    cat = series.works
    g = collections.defaultdict(list)
    for cid in cat.cards:
        if cid in NOT_ONE:
            continue
        f = cat.fields(cid) or {}
        who = works.filed_name(cid, cat)
        sur = store.fold(works.name_parts(who)[1]) if who else ""
        t = store.fold(works.ARTICLE.sub("", works.short_title(plain(f.get("title") or ""))))
        if t:
            g[(sur, t, str(f.get("year") or "")[:4])].append(cid)
    return [v for v in g.values() if len(v) > 1]


def main(dry=False):
    s = store.Series()
    cat = s.works
    where = works.where(s)
    touched, n = {}, 0
    for ids in groups(s):
        keep = next((c for c in ids if c in KEEP), None) or \
            max(ids, key=lambda c: (len(plain(cat.render(c))), len(where.get(c, [])), c))
        for drop in ids:
            if drop == keep:
                continue
            print(f"{drop} -> {keep}   {plain(cat.render(keep))[:90]}")
            n += 1
            if not dry:
                for sec in works.combine(s, keep, drop):
                    touched[id(sec)] = sec
    if not dry:
        for sec in touched.values():
            s.save_section(sec)
        cat.save()
    print(f"{n} cards folded into others")


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
