"""The works catalogue: one card a work, every list entry and citation pointing to it.

    works/<letter>.yaml     the cards, grouped by the first letter of the card's id after "w." (works/b.yaml)

Everything outside this module asks it, and nothing else reads the cards (see "the interface" below). A card:

    - id: w.beschloss-crisis-years           # permanent; never renamed or reused
      author: [Michael R. Beschloss]          # running order, as printed
      title: 'The Crisis Years: Kennedy and Khrushchev, 1960–1963'
      year: '1991'
      n: Interviews with nearly everyone.     # the card note: true of the work wherever it is listed
      tags: [topic:berlin]

A card is structured (fields; the citation is rendered from them, `render`) or verbatim (`c`, the citation as written,
where the fields cannot yet render it exactly); either way `fields` gives author, title and year for sorting,
short forms and queries. Fields of a structured card:

    author, editor, translator, director   lists of names in running order
    title                                   the italic title, subtitle and all
    year                                    as printed ('1991', '1962–66')
    paren                                   the parenthetical when it is more than roles and a year ('2d ed. 1999')
    journal, vol, page, link                an article: '45 Diplomatic Hist. 330', linked to `link`
    online                                  a link printed after the citation: '([online](…))'
    in                                      the card this one is part of (a chapter in a volume, a volume in a set);
                                            its fields fill what this card lacks
    kind                                    book, article, chapter, volume, set, film, thesis (where not plain)

STYLE:
 1. A list entry points to its card (`work: w.…`, or a list for several) and keeps its own note (the listing note);
    the card's note (the card note) is shown first, then the listing note. A listing may replace the card note
    (`card_note: replace`) or leave it out (`card_note: omit`).
 2. Under a person's subject line (a memoir, a biography section) the author named by the subject line is not
    repeated: the citation starts at the title, as the lists have always printed it.
 3. Editions, translations and chapters are cards of their own; a chapter or a volume points to its container
    (`in`), and takes from it what it lacks. A multi-volume work's short form is Bluebook's: "Logevall, Title,
    2 CHVW 123".
 4. Tags pass down: a card answers a tag query for its own tags and those of every card it is `in`.
"""
import os
import re

from . import store
from .markup import plain

WORKS = os.path.join(store.ROOT, "works")

# ---------------------------------------------------------------- parsing a citation as the lists write it

NAME = r"[A-ZÀ-ɏḀ-ỿ][\wÀ-ɏḀ-ỿ.'’\-]*"
PERSON = re.compile(rf"^(?:{NAME}|de|van|von|der|du|da|di|la|le|al-[\w\-]+|[A-Z]\.)(?:,?\s+(?:{NAME}|de|van|von|der|du|"
                    rf"da|di|la|le|y|bin|ibn|al-[\w\-]+|[A-Z]\.(?:[A-Z]\.)*|Jr\.|Sr\.|II|III|IV))*$")
YEAR = r"\d{4}(?:[–-]\d{2,4})?"
ROLE = {"ed.": "editor", "eds.": "editor", "trans.": "translator", "dir.": "director"}


def is_person(s):
    return bool(PERSON.match(s)) and 1 <= len(s.split()) <= 7


SUFFIX = ("Jr.", "Sr.", "II", "III", "IV")


def split_names(s):
    """'A, B & C' -> [A, B, C]; 'A & B' -> [A, B]; 'Rod Andrew, Jr.' is one name."""
    parts = []
    for p in s.split(", "):
        head, _, rest = p.partition(" & ")
        if parts and head in SUFFIX:
            parts[-1] += ", " + head
            if rest:
                parts.append(rest)
            continue
        parts.append(p)
    last = parts.pop()
    if not re.search(r", (?:Jr\.|Sr\.|II|III|IV) & ", last) and " & " in last:
        return parts + last.split(" & ")
    return parts + [last]


def join_names(ns):
    if len(ns) == 1:
        return ns[0]
    if len(ns) == 2:
        return f"{ns[0]} & {ns[1]}"
    return ", ".join(ns[:-1]) + " & " + ns[-1]


def parse_paren(p):
    """'Melvin Small ed., 2011' -> {editor: [...], year}; '1991' -> {year}; else {paren, year}."""
    m = re.match(rf"^(?:(?P<names>[^()]+?) (?P<role>eds?\.|trans\.|dir\.), )?(?P<year>{YEAR})$", p)
    if m:
        out = {"year": m.group("year")}
        if m.group("names"):
            ns = split_names(m.group("names"))
            if not all(is_person(n) for n in ns):
                return {"paren": p, "year": m.group("year")}
            out[ROLE[m.group("role")]] = ns
            if m.group("role") == "eds." and len(ns) == 1 or m.group("role") == "ed." and len(ns) > 1:
                return {"paren": p, "year": m.group("year")}
        return out
    y = re.findall(YEAR, p)
    return {"paren": p, **({"year": y[-1]} if y else {})}


ONLINE = re.compile(r" \(\[online\]\((?P<url>[^)\s]+)\)\)$")


def parse(c, subject=None):
    """A citation as written -> a card's fields, or None where it is not a work this catalogue holds yet (a case,
    a law, a hearing, a speech, a web resource: primary documents come later). `subject` is the listing's subject
    line where the listing sits under a person (a memoir): the citation then starts at the title, and the author is
    the subject."""
    if not c or "*" not in c:
        return None
    t = plain(c)
    if re.search(r"\bv\. ", t) and re.search(r"\d+ (?:U\.S\.|F\.|S\. Ct\.|Cal\.|N\.Y\.|So\.|A\.|P\.|N\.E\.|N\.W\.|S\.E\.|S\.W\.)", c):
        return None
    if re.search(r"Stat\.|Exec\. Order|Fed\. Reg\.|Proclamation|Pub\. L\.|Hearings? Before|Cong\. Rec\.|"
                 r"H\.R\. Rep|S\. Rep|H\.R\. Doc|S\. Doc|Cong\.(?:,| \()", c):
        return None
    f = {}
    body = c
    m = ONLINE.search(body)
    if m:
        f["online"] = m.group("url")
        body = body[:m.start()]
    # the parenthetical at the end: the year and its company
    m = re.search(r" \(([^()]*(?:\([^()]*\)[^()]*)*)\)$", body)
    if not m:
        return None
    pa = parse_paren(m.group(1))
    if "year" not in pa:
        return None
    head = body[:m.start()]
    # an article: '*Title*, [45 J. 330](url)' or '*Title*, 45 J. 330'
    art = re.search(r"\*, (?:\[(?P<cite>\d+ [^\]]+? \d+)\]\((?P<link>[^)\s]+)\)|(?P<cite2>\d+ [A-Z][^*]*? \d+))$", head)
    if art:
        cite = art.group("cite") or art.group("cite2")
        cm = re.match(r"^(\d+) (.+) (\d+)$", cite)
        f.update(vol=cm.group(1), journal=cm.group(2), page=cm.group(3), kind="article")
        if art.group("link"):
            f["link"] = art.group("link")
        head = head[:art.start() + 1]
    m = re.match(r"^(?:(?P<auth>[^*]+?), )?\*(?P<title>[^*]+)\*$", head)
    if not m:
        return None
    if m.group("auth"):
        ns = split_names(m.group("auth"))
        if not all(is_person(n) for n in ns):
            return None
        f["author"] = ns
    elif subject and not pa.get("editor") and not f.get("journal"):
        f["author"] = [subject_name(subject)]
        f["_subject"] = True          # the listing prints no author: the subject line gives it
    f["title"] = m.group("title")
    f.update(pa)
    if f.get("director"):
        f["kind"] = "film"
    return f


def subject_name(s):
    """'Schlesinger, Arthur M., Jr.' -> 'Arthur M. Schlesinger Jr.'; 'Mao Zedong' as written."""
    s = plain(s).split(";")[0].strip()
    s = re.sub(r"\s*\([^)]*\)", "", s)
    if "," not in s:
        return s
    parts = [p.strip() for p in s.split(",")]
    sur, given, rest = parts[0], parts[1] if len(parts) > 1 else "", parts[2:]
    return " ".join(x for x in [given, sur] + rest if x)


# ---------------------------------------------------------------- rendering a card

def render(f, omit_author=False):
    """The full citation, as the lists print it."""
    if f.get("c"):
        return f["c"]
    out = ""
    if f.get("author") and not omit_author:
        out = join_names(f["author"]) + ", "
    out += f"*{f['title']}*"
    if f.get("journal"):
        cite = f"{f['vol']} {f['journal']} {f['page']}"
        out += ", " + (f"[{cite}]({f['link']})" if f.get("link") else cite)
    if f.get("paren"):
        out += f" ({f['paren']})"
    else:
        roles = [f"{join_names(f[r])} {lab}" for r, lab in (("editor", "eds." if len(f.get("editor") or []) > 1 else "ed."),
                                                           ("translator", "trans."), ("director", "dir."))
                 if f.get(r)]
        out += " (" + ", ".join(roles + [f["year"]]) + ")"
    if f.get("online"):
        out += f" ([online]({f['online']}))"
    return out


def surname(name):
    words = [w for w in name.replace(".", ". ").split() if w not in ("Jr.", "Sr.", "II", "III", "IV")]
    return words[-1] if words else name


def short_title(title):
    return re.split(r"(?<=\w)[:?!]\s|\s—", title)[0]


def key_of(f):
    """Identity within the catalogue: (first author's surname, main title, the parenthetical as printed). Two
    printings of one work with the same parenthetical are one card; another edition or year is another card."""
    who = store.fold(surname(f["author"][0])) if f.get("author") else ""
    t = re.sub(r"^(the|a|an) ", "", store.fold(short_title(f["title"])))
    return (who, t, store.fold(render({**f, "author": None, "online": None, "link": None}) if not f.get("c") else f["c"]))


PRIMARY = re.compile(r"Stat\.|Exec\. Order|Fed\. Reg\.|Proclamation|Pub\. L\.|Hearings? Before|Cong\. Rec\.|"
                     r"H\.R\. Rep|S\. Rep|H\.R\. Doc|S\. Doc|Cong\.(?:,| \()|U\.S\. Const")


def loose(c, subject=None):
    """For a citation `parse` cannot render: the fields a verbatim card is sorted, shortened and found by (the first
    italic title, the author before it, the last year), or None where it is no work (a case, a law, a hearing, a
    cross-reference: 'See II.B.')."""
    if not c or "*" not in c:
        return None
    t = plain(c)
    if re.search(r"\bv\. ", t) and re.search(r"\d+ (?:U\.S\.|F\.|S\. Ct\.|Cal\.|N\.Y\.|So\.|A\.|P\.)", c) or PRIMARY.search(c):
        return None
    if re.match(r"^(?:See|Cf\.|\*See)\b", c) or re.search(r"\*(?:ante|infra|supra|id)\.?\*", c):
        return None
    m = re.match(r"^(?:(?P<auth>[^*]+?), )?\*(?P<title>[^*]+)\*", c)
    if not m:
        return None
    f = {"c": c, "title": m.group("title")}
    if m.group("auth"):
        f["author"] = [re.sub(r"\s+with\s+.*$", "", a) for a in split_names(m.group("auth"))]
    elif subject:
        f["author"] = [subject_name(subject)]
        f["_subject"] = True
    y = re.findall(r"\b(1[5-9]\d\d|20\d\d)\b", plain(c))
    if y:
        f["year"] = y[-1]
    return f


def fields_of(c, subject=None):
    """A citation as written -> a card's fields: structured where `render` gives the citation back exactly,
    verbatim (`c`) otherwise; None where it is no work the catalogue holds."""
    f = parse(c, subject)
    if f is not None and render(f, omit_author=bool(f.get("_subject"))) == c:
        return f
    return loose(c, subject)


def bucket(f):
    """Where to look for another printing of the same work: the first author's surname and the main title."""
    who = store.fold(surname(f["author"][0])) if f.get("author") else ""
    return who, re.sub(r"^(the|a|an) ", "", store.fold(short_title(f["title"])))


# ---------------------------------------------------------------- the inventory (Phase 0: read-only)

def listings(series, refs):
    """Every work a list entry cites: [(list, section, entry, citation, fields)], the calendar aside."""
    out = []
    for lst in series.lists.values():
        if lst.kind == "calendar":
            continue
        for sec, e in lst.entries():
            subj = e.get("s") if refs.is_person(lst, sec, e) else None
            for c in store.as_list(e.get("c")):
                f = fields_of(c, subj)
                if f is not None:
                    out.append((lst, sec, e, c, f))
    return out


def inventory(series):
    """A report of what the catalogue would hold, written for the owner (notes/works-inventory.md)."""
    import collections
    from .build import Linker
    from .markup import italics
    linker = Linker(series)
    refs = linker.refs
    L = listings(series, refs)
    total_lines = sum(len(store.as_list(e.get("c"))) for l in series.lists.values() if l.kind != "calendar"
                      for _, e in l.entries())
    cards = collections.OrderedDict()            # the full citation, author written -> listings
    for x in L:
        f = x[4]
        full = render({k: v for k, v in f.items() if k != "_subject"}) if not f.get("c") else \
            (join_names(f["author"]) + ", " + f["c"] if f.get("_subject") else f["c"])
        cards.setdefault(full, []).append(x)
    structured = sum(1 for v in cards.values() if not v[0][4].get("c"))
    multi = {k: v for k, v in cards.items() if len({(l.key, s.code) for l, s, *_ in v}) > 1}
    buckets = collections.defaultdict(list)
    for full, v in cards.items():
        buckets[bucket(v[0][4])].append(full)
    variants, editions = [], []
    for b, fulls in buckets.items():
        if len(fulls) < 2 or not b[1]:
            continue
        years = {cards[f][0][4].get("year") for f in fulls}
        (variants if len(years) < len(fulls) else editions).append(fulls)
    # notes
    same_note = diff_note = 0
    diffs = []
    for full, v in multi.items():
        notes = {plain(e.get("n") or "") for _, _, e, _, _ in v if len(store.as_list(e.get("c"))) == 1}
        notes.discard("")
        if len(notes) <= 1:
            same_note += 1
        else:
            diff_note += 1
            diffs.append((full, v))
    single_noted = sum(1 for v in cards.values() if len(v) == 1 and v[0][2].get("n") and len(store.as_list(v[0][2].get("c"))) == 1)
    several = sum(1 for l in series.lists.values() if l.kind != "calendar" for _, e in l.entries()
                  if len(store.as_list(e.get("c"))) > 1)
    # the calendar's citations
    cal = series.lists.get("cal")
    linked = unlinked_ref = full_only = other = shared = 0
    unl = []
    for _, e in cal.entries():
        n = e.get("n") or ""
        for m in re.finditer(r"\*([^*]+)\*", n):
            tail = n[m.end():m.end() + 200]
            ref = None
            for a, b2, key, code in refs.scan(tail, "cal"):
                ref = (a, key, code)
                break
            if re.match(r"\s*\((?:[^()]*\b(1[5-9]\d\d|20\d\d))\)", tail):
                full_only += 1
            elif ref and code_ok(ref, tail):
                x = linker.find_title(m.group(1), ref[1], ref[2])
                if x:
                    linked += 1
                else:
                    unlinked_ref += 1
                    unl.append((e["id"], m.group(1), tail[:ref[0] + 20]))
            elif ref and not re.search(r"[a-z)]\.\s+[A-Z]", tail[:ref[0]]):
                shared += 1                  # one of several titles before a single list and section
            else:
                other += 1
    w = []
    add = w.append
    add("# The works catalogue: inventory (Phase 0)")
    add("")
    add("Read-only: what the catalogue would hold if built from the lists as they stand. Written by `./bib works "
        "inventory`; nothing in the series changed. See `tools/bib/works.py`.")
    add("")
    add("## Citation lines in the lists (the calendar aside)")
    add("")
    add(f"- {total_lines} citation lines; {len(L)} are works the catalogue would hold; the rest are primary documents "
        "(cases, laws, orders, hearings, speeches), web resources, archives and cross-references, which wait.")
    add(f"- {len(cards)} cards: {structured} structured (rendered from fields, exactly as printed now), "
        f"{len(cards) - structured} verbatim (the citation kept as written; fields read from it for sorting and search).")
    add(f"- {len(multi)} cards listed in more than one place; {several} list entries cite several works at once.")
    add("")
    add("## Notes")
    add("")
    add(f"- Cards listed once, with a note: {single_noted}. The note becomes the card note (your default).")
    add(f"- Cards listed more than once: {same_note} with one note or none (it becomes the card note); "
        f"{diff_note} with differing notes (kept as listing notes, below).")
    add(f"- Entries citing several works keep their note as a listing note ({several}).")
    add("")
    add("## Probably one work, written differently")
    add("")
    add("Same author and main title, same year, different text. Phase 1 keeps them as separate cards (so no page "
        "changes); each group wants one form, and then they become one card.")
    add("")
    for g in sorted(variants, key=lambda g: g[0]):
        add("- " + "\n  - ".join([""] + [f"{f}  ({', '.join(sorted({l.abbr + ' ' + s.code for l, s, *_ in cards[f]}))})" for f in g]).lstrip("\n  - ").replace("\n  - ", "\n  - ", 1))
        add("")
    add("## Editions and printings of one work")
    add("")
    add("Same author and main title, different years: separate cards, as editions are. Listed so a translation or "
        "edition can point to its original (`translates:`, `edition_of:`) where wanted.")
    add("")
    for g in sorted(editions, key=lambda g: g[0]):
        add("- " + " · ".join(f"{f}  ({', '.join(sorted({l.abbr + ' ' + s.code for l, s, *_ in cards[f]}))})" for f in g))
    add("")
    add("## Listed in several places with differing notes")
    add("")
    for full, v in diffs:
        add(f"- {full}")
        for l, s, e, _, _ in v:
            if e.get("n"):
                add(f"  - {l.abbr} {s.code}: {plain(e['n'])}")
    add("")
    add("## The calendar's citations of works")
    add("")
    add(f"- Short titles followed by a list and section, matched to a list entry now: {linked}.")
    add(f"- Short titles followed by a list and section, not matched (the title or section does not answer): {unlinked_ref}.")
    add(f"- Full citations (a work found only in the calendar, cited in full): {full_only}. These become cards too.")
    add(f"- Short titles in a run sharing one list and section after the last (\"Ball, *Politics and Force Levels*; "
        f"Kaplan, *Wizards of Armageddon* (K–J Adm. II.D)\"): {shared}. Only the last title of such a run is linked now.")
    add(f"- Other italics (a newspaper, a ship, a word, a title with no reference): {other}.")
    add("")
    for eid, t, tail in unl:
        add(f"- {eid}: *{t}* {tail.strip()}")
    add("")
    add("## Suspected errors in the data")
    add("")
    add("Citations the parser reads one way and prints another: usually a misplaced italic or comma.")
    add("")
    for l, sec, e, c, f in L:
        g = parse(c, e.get("s") if refs.is_person(l, sec, e) else None)
        if g is not None and render(g, omit_author=bool(g.get("_subject"))) != c:
            add(f"- {l.abbr} {sec.code} `{e['id']}`: {c}")
    return "\n".join(w) + "\n"


def code_ok(ref, tail):
    """A reference that belongs to this title: none of another title's marks or a clause's end between them."""
    return not re.search(r"\*|;|[a-z]\.\s", tail[:ref[0]])
