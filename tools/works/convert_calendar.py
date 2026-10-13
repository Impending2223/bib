"""Once: the calendar's short citations of works become pointers to their cards (Phase 2; the owner's ruling, Oct. 13,
2026: each work by its short form, linked to the A–Z bibliography, no list or section).

    python3 tools/works/convert_calendar.py [--dry-run] [--diff FILE]

A run of short citations before a list reference ("Ball, *Politics and Force Levels*; Kaplan, *Wizards of
Armageddon* (K–J Adm. II.D)") is read item by item. An item becomes [[w.…]] (its pinpoint kept after it: "[[w.gallup-
poll]], III, 1862") where one card answers it strictly: its title begins with the title written (the leading article
aside), and its first author's surname is the first written, the author written as names alone (a label before it
kept: "Also", "Check", "Film:"); the cards listed in the section referred to first, then
in the list, then anywhere. Where every item of the run is converted, the reference goes; otherwise it stays, after
the items left as written (a hearing, a clipped title: notes/works-inventory.md, "The calendar's citations").
Neighbouring runs, once parted by their lists' references, join into one: "[[w.a]]; [[w.b]]; [[w.c]]."
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bib import store, works  # noqa: E402
from bib.refs import Refs  # noqa: E402
from bib.markup import plain  # noqa: E402

SEP = re.compile(r"^[\s;,]*(?:and\s+)?$")
PAREN = re.compile(r"\(([^()]*)\)")
ITEM = re.compile(r"^(?P<lab>[^*:\[\]]*:\s+|(?:Also|Check|Cf\.|Compare|See also)\s+)?(?P<a>[^*\[\]]*?)(?:,\s*)?"
                  r"\*(?P<t>[^*]+)\*(?P<tail>[^*\[\]]*)$")
# the author as the calendar writes it: names only ("Fursenko & Naftali", "Bundy et al.", "O'Brien", "Thích Nhất Hạnh")
WORD = r"(?:[A-ZÀ-ỸĐ][\w'’.\-]*|de|van|von|der|du|da|di|la|le|y|i)"
NAMES = re.compile(rf"^(?:{WORD}(?:\s+{WORD}){{0,4}})(?:\s*(?:&|,|and)\s*{WORD}(?:\s+{WORD}){{0,4}})*(?:\s+et al\.)?$")
ART = re.compile(r"^(the|a|an) ")
# a full stop that ends an initial or an abbreviation, not a sentence ("U.S. Commission", "Arthur M. Schlesinger")
ABBR = re.compile(r"(?:\b[A-Z]\.|\b(?:[A-Z]\.){2,}|\b(?:Jr|Sr|Dept|Comm|Inst|Off|Serv|St|Mr|Mrs|Dr|vols?|eds?|Nos?|Doc|"
                  r"pt|Rev|Gen|Sen|Rep|Gov|Corp|Co|Inc|Bros|Ltd|Univ|Assn|Ass'n)\.)$")


def tkey(t):
    return ART.sub("", store.fold(plain(t)))


# what the rule cannot match, by hand: the item as the calendar writes it -> its card (the title clipped otherwise than at
# a colon, a volume of a series, an author the card names as editor)
MANUAL = {
    "Brauer, *Second Reconstruction*": "w.brauer-john-f-kennedy-and",
    "Heath, *Kennedy and the Business Community*": "w.heath-john-f-kennedy-and",
    "Spector, *Advice and Support*": "w.spector-united-states-army-in",
    "Cosmas, *MACV*": "w.cosmas-united-states-army-in",
    "Carland, *Combat Operations: Stemming the Tide*": "w.carland-united-states-army-in",
    "Shulimson & Johnson, *The Landing and the Buildup, 1965*": "w.shulimson-u-s-marines-in",
    "Loevy ed., *The Civil Rights Act of 1964*": "w.civil-rights-act-of",
    "Miller, *Member of the House*": "w.member-of-the-house",
    "Smith, *Declaration of Conscience*": "w.declaration-of-conscience",
    "Minow, *Equal Time*": "w.equal-time",
    "Takenaka, *Doru kiki to 1961-nen maruku kiriage*": "w.doru-kiki-to-1961",
    "Stockdale, *In Love and War*": "w.jim-in-love-and-war",
    "Malcolm X with Alex Haley, *The Autobiography of Malcolm X*": "w.x-autobiography-of-malcolm-x",
    "*Congress and the Nation*, vol. 1": "w.congress-and-the-nation",
    "*Congress and the Nation*, vol. 2": "w.congress-and-the-nation-1969",
}


class Resolver:
    def __init__(self, series):
        self.s, self.cat, self.refs = series, series.works, Refs(series)
        self.by_sec, self.by_list = {}, {}
        self.authors = {store.fold(a) for c in self.cat.cards for a in (self.cat.fields(c) or {}).get("author") or []}
        for cid, ls in works.where(series).items():
            for lst, sec, e in ls:
                x = sec
                while x is not None:
                    self.by_sec.setdefault((lst.key, x.code), set()).add(cid)
                    x = getattr(x, "parent", None)
                self.by_list.setdefault(lst.key, set()).add(cid)

    def refparen(self, content):
        out, pos, left = [], 0, []
        for a, b, key, code in self.refs.scan(content, "cal"):
            left.append(content[pos:a])
            pos = b
            out.append((key, code))
        left.append(content[pos:])
        return out if out and all(SEP.match(x) for x in left) else None

    def surnames(self, cid):
        f = self.cat.fields(cid) or {}
        return [store.fold(works.name_parts(n)[1].split()[-1]) for n in (f.get("author") or f.get("editor") or [])]

    def title_ok(self, t, cid):
        f = self.cat.fields(cid) or {}
        full, k = tkey(f.get("title") or ""), tkey(t)
        return bool(k) and (full == k or full.startswith(k + " ") or tkey(works.short_title(f.get("title") or "")) == k)

    def card(self, t, a, rs):
        ws = [store.fold(x.strip().split()[-1]) for x in re.split(r"\s*(?:&|,|\band\b)\s*", re.sub(r"\bet al\.?", "", a))
              if x.strip()]
        pools = [self.by_sec.get((k, c), set()) for k, c in rs if c] + [self.by_list.get(k, set()) for k, c in rs] + \
            [set(self.cat.cards)]
        for pool in pools:
            hits = [c for c in pool if self.title_ok(t, c) and (not ws or self.surnames(c)[:1] == ws[:1])]
            if len(hits) > 1:
                hits = [c for c in hits if tkey(works.short_title(self.cat.fields(c).get("title") or "")) == tkey(t)
                        or tkey(self.cat.fields(c).get("title") or "") == tkey(t)]
            if len(hits) == 1:
                return hits[0]
            if hits:
                return None
        return None

    def convert(self, n):
        """(the note with its runs converted, items converted, items left)"""
        edits, done, left = [], 0, 0
        for m in PAREN.finditer(n):
            rs = self.refparen(m.group(1))
            if not rs:
                continue
            before = n[:m.start()]
            b = max([x.end() for x in re.finditer(r"(?:[.)\]]|\]\])\s+(?=\S)", before)
                     if not ABBR.search(before[:x.start() + 1])] + [0])
            seg = before[b:].rstrip()
            items, out, all_done = re.split(r";\s+", seg), [], True
            for it in items:
                mm = ITEM.match(it)
                lab = (mm.group("lab") or "") if mm else ""
                if it[len(lab):] in MANUAL:
                    out.append(lab + f"[[{MANUAL[it[len(lab):]]}]]")
                    done += 1
                    continue
                a = mm.group("a").strip() if mm else ""
                ok = mm and (not a or NAMES.match(a) or store.fold(a) in self.authors)      # names, or a body as written
                cid = self.card(mm.group("t"), mm.group("a"), rs) if ok else None
                if cid:
                    out.append((mm.group("lab") or "") + f"[[{cid}]]" + mm.group("tail").rstrip())
                    done += 1
                else:
                    out.append(it)
                    all_done = False
                    left += 1 if mm else 0
            if out == items:
                continue
            new = "; ".join(out) + ("" if all_done else " " + m.group(0))
            edits.append((b, m.end(), new))
        for a, z, new in reversed(edits):
            n = n[:a] + new + n[z:]
        # runs once parted by their lists' references are one bibliography now: "[[w.a]]; [[w.b]]; [[w.c]]."
        n = re.sub(r"(\[\[w\.[^\]]+\]\][^.\[\]*]*?)\. (?=\[\[w\.)", r"\1; ", n)
        return n, done, left


def main(dry=False, diff=None):
    s = store.Series()
    r = Resolver(s)
    cal = next(l for l in s.lists.values() if l.kind == "calendar")
    total = left = changed = 0
    lines = []
    for sec in cal.walk():
        touched = False
        for e in sec.entries:
            if not e.get("n"):
                continue
            new, d, l = r.convert(e["n"])
            total, left = total + d, left + l
            if new != e["n"]:
                lines += [e["id"], "  - " + e["n"], "  + " + new, ""]
                e["n"] = new
                touched = True
                changed += 1
        if touched and not dry:
            s.save_section(sec)
    if diff:
        open(diff, "w", encoding="utf-8").write("\n".join(lines))
    print(f"{total} citations pointed to cards in {changed} entries; {left} left as written")


if __name__ == "__main__":
    a = sys.argv[1:]
    main("--dry-run" in a, a[a.index("--diff") + 1] if "--diff" in a else None)
