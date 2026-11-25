"""Respell names across the calendar to the series' forms (the reader's brief, R19a; notes/owner-rulings.md, 54).

    python3 -I tools/names/respell.py            dry run: the counts, the report written
    python3 -I tools/names/respell.py --write    the entries rewritten

STYLE
 1. The table (TABLE) is the owner's rulings of Nov. 24, 2026, and the defaults of ruling 54: Guangzhou for Canton;
    Tsinghua for Qinghua; Quemoy for Jinmen; the Yangtze for the Yangzi; Xinjiang for Sinkiang; Kuomintang for
    Guomindang; Ulanhu for Ulanfu.
 2. Not touched: words inside a quotation ("..."), an italic title (*...*), a link's text or address, a card or entry
    reference ([[...]]). A source's own words and a work's own title stay as printed.
 3. "Canton" is respelled only in an entry about China (its thread begins "china", or it is tagged polity:prc, or its
    place is the gazetteer's canton), and never where the entry is tagged for an American State or the word is
    followed by ", Miss." or ", Ohio". The others are listed in the report for a reader.
 4. The line is changed in its stored form, so its cut marks move with their words; the map's hash is renewed where
    it was current (a respelling changes no unit's sources).
 5. The report: notes/names/respell-2026-11-24.tsv (id, field, the change, or why it was left).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bib import store, claims  # noqa: E402

TABLE = [("Canton", "Guangzhou"), ("Qinghua", "Tsinghua"), ("Jinmen", "Quemoy"), ("Yangzi", "Yangtze"),
         ("Sinkiang", "Xinjiang"), ("Guomindang", "Kuomintang"), ("Ulanfu", "Ulanhu")]
PROTECT = re.compile(r'"[^"]*"|“[^”]*”|\*[^*]+\*|\[\[[^\]]*\]\]|\[[^\]]*\]\([^)]*\)')


def chinese(e):
    tags = [str(t) for t in e.get("tags") or []]
    if any(t.startswith("state:") for t in tags):
        return False
    return str(e.get("thread") or "").startswith("china") or "polity:prc" in tags or "canton" in store.as_list(e.get("place")) \
        or any(str(a).startswith("china") for a in e.get("also") or [])


def respell(text, e, log, field):
    out, last = [], 0
    spans = [(m.start(), m.end()) for m in PROTECT.finditer(text)]

    def free(seg):
        for old, new in TABLE:
            rx = re.compile(rf"\b{old}\b(?!ese)")
            for m in list(rx.finditer(seg)):
                if old == "Canton" and (not chinese(e) or re.match(r", (Miss|Ohio|N\.Y|Ill|Mass)", seg[m.end():])):
                    log.append((e["id"], field, f"left: Canton (not an entry about China): {seg[max(0, m.start() - 30):m.end() + 20]!r}"))
                    continue
                log.append((e["id"], field, f"{old} -> {new}"))
            if old == "Canton" and not chinese(e):
                continue
            seg = re.sub(rf"\b{old}\b(?!ese)(?!, (?:Miss|Ohio|N\.Y|Ill|Mass))", new, seg)
        return seg
    for a, b in spans:
        out.append(free(text[last:a]))
        prot = text[a:b]
        for old, _ in TABLE:
            if re.search(rf"\b{old}\b", prot):
                log.append((e["id"], field, f"left: {old} inside a quotation, a title or a link: {prot[:60]!r}"))
        out.append(prot)
        last = b
    out.append(free(text[last:]))
    return "".join(out)


def main():
    write = "--write" in sys.argv
    series = store.Series()
    log, touched, n = [], set(), 0
    for sec, e in claims.calendar(series):
        st = store.stored_form(e)
        new = dict(st)
        for f in ("c", "n", "at"):
            if isinstance(st.get(f), str) and any(re.search(rf"\b{old}\b", st[f]) for old, _ in TABLE):
                new[f] = respell(st[f], e, log, f)
        if new == st:
            continue
        n += 1
        if write:
            was_current = isinstance(e.get("src"), dict) and e["src"].get("c") == claims.chash(e.get("c"))
            ne = store.normalize_entry(new)
            if was_current:
                ne["src"] = dict(ne["src"], c=claims.chash(ne.get("c")))
            i = next(k for k, x in enumerate(sec.entries) if x is e)
            sec.entries[i] = ne
            touched.add(sec)
    if write:
        for sec in touched:
            series.save_section(sec)
    os.makedirs(os.path.join(ROOT, "notes", "names"), exist_ok=True)
    with open(os.path.join(ROOT, "notes", "names", "respell-2026-11-24.tsv"), "w", encoding="utf-8") as fh:
        fh.write("id\tfield\twhat\n")
        for r in log:
            fh.write("\t".join(r) + "\n")
    import collections
    c = collections.Counter(r[2] if not r[2].startswith("left") else r[2].split(":")[0] + ":" + r[2].split(":")[1].split(" ")[1] for r in log)
    print(f"{n} entries change" + ("; written" if write else "; dry run"))
    for k, v in sorted(c.items()):
        print(f"  {v:5} {k}")


if __name__ == "__main__":
    main()
