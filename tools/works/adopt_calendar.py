"""Once: the works the calendar cites in full become cards (the owner's request, Oct. 13, 2026: "add all the missing and
unabbreviated bibliographic items to the bibliography"), each citation then a pointer to its card ([[w.…]]), which
the build prints in full at the work's first appearance in each half of the calendar (SHORT FORM, FIRST CITE in
tools/bib/works.py), as the calendar had written it.

    python3 tools/works/adopt_calendar.py [--dry-run] [--report FILE]

A full citation: "Author, *Title* … (… 1996)", the parenthesis holding the year, or a title-first one ("*Playa Girón*
(4 vols., 1961–62)"); read by works.fields_of, which refuses a case, a statute, a hearing or a speech. The calendar's own pointers back
to such a citation ("Smith, *Lucius D. Clay* (see [[cal.…]])") become the card too. A card already holding the work takes it: one printing the same citation, or, where the parenthesis is a year alone (a publisher and a
year), one with the same first author's surname, main title and year (an issue of a periodical, "June 1961", takes a
card of its own); otherwise a new card, structured
where the fields print the citation exactly as written, else verbatim (the citation as written).
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bib import store, works  # noqa: E402
from bib.markup import plain  # noqa: E402

YEAR = r"(?:1[89]\d\d|20\d\d)"
LINK = r"\[[^\[\]]*\]\([^()\s]*(?:\([^()\s]*\)[^()\s]*)*\)"
# the start: the sentence's, a semicolon's, or a label's ("The Cuban record: ")
START = re.compile(r"(?:^|(?<=[.;:)\]]\s)|(?<=\]\]\s))")
ABBR = re.compile(r"(?:\b[A-Z]\.|\b(?:[A-Z]\.){2,}|\b(?:Jr|Sr|Dept|Comm|Inst|St|Mr|Mrs|Dr|vols?|eds?|Nos?|Gen|Sen|Rep|Gov|Co|Inc)\.)$")
CITE = re.compile(rf"(?P<a>(?:[^*.;\[\]()]|\.(?! )|(?<=\b[A-Z])\. )*?,\s)?\*(?P<t>[^*]+)\*(?P<rest>(?:[^()*\[\]]|{LINK})*?)"
                  rf"\((?P<p>[^()]*\b{YEAR}\b[^()]*)\)(?P<on> \(\[online\]\([^()\s]*\)\))?")


def tkey(t):
    return store.fold(works.ARTICLE.sub("", plain(t)))


def key(f):
    a = (f.get("author") or f.get("editor") or [""])[0]
    sur = store.fold(works.name_parts(a)[1]) if a else ""
    return sur, store.fold(works.ARTICLE.sub("", works.short_title(plain(f.get("title") or "")))), str(f.get("year") or "")[:4]


def _paren(c):
    m = re.search(r"\(([^()]*)\)(?: \(\[online\][^)]*\)\))?$", c)
    return m.group(1) if m else ""


works.parse_paren_text = _paren


def candidates(n):
    """(start, end, citation) for each full citation in a note, outside links and pointers."""
    protected = [m.span() for m in re.finditer(rf"\[\[[^\]]*\]\]|{LINK}", n)]
    out = []
    for m in re.finditer(r"\*[^*]+\*", n):
        if any(a <= m.start() < b for a, b in protected):
            continue
        # back to the start of the citation
        i = m.start()
        b = 0
        for x in re.finditer(r"(?:[.)\]]\s+|;\s+|:\s+)", n[:i]):
            if x.group(0).startswith(".") and ABBR.search(n[:x.start() + 1]):
                continue
            b = x.end()
        cm = CITE.match(n, b)
        if not cm or cm.start("t") != m.start() + 1:
            continue
        if cm.group("a") and (len(cm.group("a")) > 90 or re.search(r"\b(?:the|of|in|and the|was|is)\b [a-z]", cm.group("a"))
                              and not re.search(r"\bwith\b", cm.group("a"))):
            continue                      # prose before the title, not an author
        if any(a < cm.end() and cm.start() < b2 for a, b2 in protected if not (a >= cm.start() and b2 <= cm.end())):
            continue
        if " v. " in cm.group("t"):
            continue                      # a case
        if "[[" in cm.group("p") or re.match(r"\s*see\b", cm.group("p")):
            continue                      # a pointer in parentheses, not a work's date
        if re.search(r"\.\s+[A-Z]", re.sub(LINK, "", cm.group("rest"))):
            continue                      # runs past the end of its sentence
        out.append((cm.start(), cm.end(), cm.group(0)))
    return out


def main(dry=False, report=None):
    s = store.Series()
    cat = s.works
    by_key = {}
    for cid in cat.cards:
        by_key.setdefault(key(cat.fields(cid) or {}), []).append(cid)
    taken = set(cat.cards) | set(cat.alias)
    cal = next(l for l in s.lists.values() if l.kind == "calendar")
    rows, new, reused = [], 0, 0
    for sec in cal.walk():
        touched = False
        for e in sec.entries:
            n = e.get("n") or ""
            edits = []
            for a, z, c in candidates(n):
                f = works.fields_of(c)
                if f is None or not f.get("year"):
                    continue
                hits = [h for h in by_key.get(key(f), []) if plain(cat.render(h)) == plain(c)] or \
                    (by_key.get(key(f), []) if re.fullmatch(rf"(?:[^,()]+, )?{YEAR}", works.parse_paren_text(c)) else [])
                if len(hits) == 1:
                    cid = hits[0]
                    reused += 1
                    rows.append(f"= {e['id']}  {c}\n    -> {cid}: {plain(cat.render(cid))}")
                else:
                    card = {k: v for k, v in f.items() if not k.startswith("_")}
                    if card.get("c") or works.render(card, cat=cat) != c:
                        card = {"c": c}
                    cid = works.new_id(f, taken)
                    taken.add(cid)
                    cat.cards[cid] = {"id": cid, **card}
                    cat.file_of[cid] = f"{works.letter(cid)}.yaml"
                    by_key.setdefault(key(cat.fields(cid) or {}), []).append(cid)
                    new += 1
                    rows.append(f"+ {e['id']}  {c}\n    -> {cid}")
                edits.append((a, z, f"[[{cid}]]"))
            for a, z, t in reversed(edits):
                n = n[:a] + t + n[z:]
            if edits:
                e["n"] = n
                touched = True
        if touched and not dry:
            s.save_section(sec)
    # the short form the calendar wrote with a pointer back to the full one, "Smith, *Lucius D. Clay* (see [[cal.…]])":
    # the card, whose first appearance carries the citation now
    back = re.compile(r"(?:(?P<a>[A-Z][\w'’ &.-]*), )?\*(?P<t>[^*]+)\* \(see \[\[(?P<id>cal\.[^\]|]+)\]\]\)")
    for sec in cal.walk():
        touched = False
        for e in sec.entries:
            n = e.get("n") or ""

            def sub(m):
                hit = s.get(m.group("id"))
                for cid in re.findall(r"\[\[(w\.[^\]|]+)\]\]", (hit[2].get("n") or "") if hit else ""):
                    f = cat.fields(cid) or {}
                    if tkey(f.get("title") or "").startswith(tkey(m.group("t"))):
                        rows.append(f"< {e['id']}  {m.group(0)}\n    -> {cid}")
                        return f"[[{cid}]]"
                return m.group(0)
            new_n = back.sub(sub, n)
            if new_n != n:
                e["n"] = new_n
                touched = True
        if touched and not dry:
            s.save_section(sec)
    if not dry:
        cat.save()
    if report:
        open(report, "w", encoding="utf-8").write("\n".join(rows) + "\n")
    print(f"{new} new cards, {reused} citations to cards already held")


if __name__ == "__main__":
    a = sys.argv[1:]
    main("--dry-run" in a, a[a.index("--report") + 1] if "--report" in a else None)
