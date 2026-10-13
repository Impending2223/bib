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
    repeated: the citation starts at the title, as the lists have always printed it (`byline` keeps it). A listing of
    several works by one author names the author at the first only (`ditto: true`).
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

def render(f, omit_author=False, cat=None):
    """The full citation, as the lists print it. A card `in` another (a chapter in a volume) needs the catalogue
    (`cat`) to find it."""
    if f.get("in") and not f.get("c"):
        return render_part(f, omit_author, cat)
    if f.get("c"):              # verbatim; one printed from the title on carries its author as a field
        if f.get("author") and f["c"].lstrip().startswith("*") and not omit_author:
            return join_names(f["author"]) + ", " + f["c"]
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


def render_part(f, omit_author, cat):
    """A chapter in its volume, Bluebook's way: 'Author, *Chapter*, *in* *Volume* 127 (Editor ed., 2006)'; ', at 223'
    where the volume's title ends in a number; in a volume of a set, the set's title after the volume's number
    ('*in* 2 *The Cambridge History of the Vietnam War* 123'). The volume's parenthetical and link close it."""
    vol = cat.get(f["in"]) if cat else None
    if vol is None:
        return f"{join_names(f['author'])}, *{f['title']}*" if f.get("author") else f"*{f['title']}*"
    out = "" if omit_author or not f.get("author") else join_names(f["author"]) + ", "
    out += f"*{f['title']}*, *in* "
    vt = vol.get("title")
    if vol.get("in") and vol.get("vol"):                 # a volume of a set
        st = cat.get(vol["in"]) or {}
        out += f"{vol['vol']} *{st.get('title', '')}*"
        vt = st.get("title", "")
    else:
        out += f"*{vt}*"
    if f.get("page"):
        out += (", at " if re.search(r"\d$", vt or "") else " ") + str(f["page"])
    shell = {k: v for k, v in vol.items() if k in ("editor", "translator", "paren", "year")}
    if "year" not in shell and vol.get("in"):
        shell.setdefault("year", (cat.get(vol["in"]) or {}).get("year"))
    roles = [f"{join_names(shell[r])} {lab}" for r, lab in (("editor", "eds." if len(shell.get("editor") or []) > 1 else "ed."),
                                                           ("translator", "trans.")) if shell.get(r)]
    out += f" ({shell['paren']})" if shell.get("paren") else " (" + ", ".join(roles + [str(shell.get("year") or "")]) + ")"
    if vol.get("online"):
        out += f" ([online]({vol['online']}))"
    return out


def surname(name):
    words = [w for w in name.replace(".", ". ").split() if w not in ("Jr.", "Sr.", "II", "III", "IV")]
    return words[-1] if words else name


def short_title(title):
    return re.split(r"(?<=\w)[:?!]\s|\s—", title)[0]


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


# ---------------------------------------------------------------- the interface: the catalogue and its questions

CARD_FIELDS = ["id", "kind", "author", "editor", "translator", "director", "title", "journal", "vol", "page", "link",
               "paren", "year", "online", "c", "in", "edition_of", "translates", "short", "n", "tags", "aliases"]


def letter(cid):
    ch = cid[2:3]
    return ch if ch.isalpha() else "0"


class Catalogue:
    """The cards, by id. Nothing outside this module reads works/ (STYLE: the interface)."""

    def __init__(self, root=store.ROOT):
        self.root = root
        self.dir = os.path.join(root, "works")
        self.cards = {}          # id -> the card as stored
        self.alias = {}
        self.file_of = {}
        if os.path.isdir(self.dir):
            for fn in sorted(os.listdir(self.dir)):
                if not fn.endswith(".yaml"):
                    continue
                doc = store.load_yaml(os.path.join(self.dir, fn)) or {}
                for c in doc.get("cards") or []:
                    self.cards[c["id"]] = c
                    self.file_of[c["id"]] = fn
                    for a in store.as_list(c.get("aliases")):
                        self.alias[a] = c["id"]
        self._fields = {}

    def get(self, cid):
        return self.cards.get(self.alias.get(cid, cid))

    def fields(self, cid):
        """The card's fields for sorting, short forms and queries: a verbatim card's read from its citation."""
        if cid not in self._fields:
            c = self.get(cid)
            if c is None:
                return None
            f = dict(loose(c["c"]) or {}) if c.get("c") else {}
            f.update(c)
            self._fields[cid] = f
        return self._fields[cid]

    def chain(self, cid):
        """The card and every card it is `in`, nearest first."""
        out, seen = [], set()
        while cid and cid not in seen:
            c = self.get(cid)
            if c is None:
                break
            seen.add(cid)
            out.append(c)
            cid = c.get("in")
        return out

    def tags(self, cid):
        """Its own tags and every container's (STYLE 4)."""
        return [t for c in self.chain(cid) for t in store.as_list(c.get("tags"))]

    def render(self, cid, omit_author=False):
        return render(self.get(cid), omit_author, self)

    def save(self, cid=None):
        """Write the card files (all, or the one holding `cid`)."""
        groups = {}
        for c in self.cards.values():
            groups.setdefault(self.file_of.get(c["id"]) or f"{letter(c['id'])}.yaml", []).append(c)
        os.makedirs(self.dir, exist_ok=True)
        for fn, cs in groups.items():
            if cid and fn != self.file_of.get(cid):
                continue
            cs.sort(key=lambda c: c["id"])
            for c in cs:
                self.file_of[c["id"]] = fn
            store.dump_yaml({"cards": [order(c) for c in cs]}, os.path.join(self.dir, fn),
                            header=[f"The works catalogue: cards whose id begins w.{fn[:-5]}. "
                                    "The fields: tools/bib/works.py. Run ./bib check after editing."])


def order(c):
    out = {k: c[k] for k in CARD_FIELDS if k in c and c[k] not in (None, [], "")}
    out.update({k: v for k, v in c.items() if k not in out and not k.startswith("_")})
    return out


def omit_author(e, sec, card, prev=None):
    """Under a person's subject line the author it names is not repeated (STYLE 2), unless the listing says
    `byline: true` (or names the cards that print it: `byline: [w.…]`). In a listing of several works marked
    `ditto: true`, a work by the same authors as the one before it does not repeat them."""
    from .refs import Refs
    if e.get("ditto") and prev is not None and card.get("author") and card.get("author") == prev.get("author"):
        return True              # a listing of one author's works names the author once, at the first
    b = e.get("byline")
    if b is True or card["id"] in store.as_list(b) or not e.get("s") or not card.get("author") or \
            not Refs.is_people_section(sec):
        return False
    return store.fold(card["author"][0]) == store.fold(subject_name(e["s"]))


def listing_note(e, cards):
    """The note a listing shows: the card note, then its own (STYLE 1). A listing citing several works shows its own
    note alone."""
    own = e.get("n")
    if len(cards) != 1 or e.get("card_note") in ("replace", "omit"):
        return own
    cn = cards[0].get("n")
    return " ".join(x for x in (cn, own) if x) or None


def resolve(series):
    """Give each listing that points to cards its citation and notes, in memory (store.stored_form takes them off)."""
    cat = series.works
    for lst in series.lists.values():
        for sec, e in lst.entries():
            if not e.get("work"):
                continue
            ids = store.as_list(e["work"])
            cards = [cat.get(i) for i in ids]
            if any(c is None for c in cards):
                e["_missing"] = [i for i, c in zip(ids, cards) if c is None]
                continue
            cs = [render(c, omit_author(e, sec, c, cards[i - 1] if i else None), cat) for i, c in enumerate(cards)]
            shown_c = cs if isinstance(e["work"], list) else cs[0]
            shown_n = listing_note(e, cards)
            e["_derived"] = {"c": (shown_c, None), "n": (shown_n, e.get("n"))}
            e["c"] = shown_c
            if shown_n is None:
                e.pop("n", None)
            else:
                e["n"] = shown_n


# ---------------------------------------------------------------- where, and queries

def where(series):
    """card id -> [(list, section, entry)]: every listing that points to it (the reverse index; built once a run)."""
    if getattr(series, "_where", None) is None:
        out = {}
        for lst in series.lists.values():
            for sec, e in lst.entries():
                for cid in store.as_list(e.get("work")):
                    out.setdefault(series.works.alias.get(cid, cid), []).append((lst, sec, e))
        series._where = out
    return series._where


def attributes(series, cid):
    """What a card answers to in a query: its tags and its containers' (STYLE 4); and, worked out, kind:, year:,
    pub:1990s, author:<surname>, in:<list>, section:<list>.<code>, form:structured|verbatim."""
    cat = series.works
    f = cat.fields(cid) or {}
    out = set(cat.tags(cid))
    out.add("kind:" + (f.get("kind") or "book"))
    out.add("form:" + ("verbatim" if f.get("c") else "structured"))
    y = re.match(r"\d{4}", str(f.get("year") or ""))
    if y:
        out.add("year:" + y.group(0))
        out.add("pub:" + y.group(0)[:3] + "0s")
    for a in f.get("author") or []:
        out.add("author:" + store.slug(surname(a), 3))
    for lst, sec, _ in where(series).get(cid, []):
        out.add("in:" + lst.key)
        out.add(f"section:{lst.key}.{sec.code}")
    return out


def index(series):
    """attribute -> set of card ids (built once a run; a query is set arithmetic on it)."""
    if getattr(series, "_windex", None) is None:
        idx = {}
        for cid in series.works.cards:
            for a in attributes(series, cid):
                idx.setdefault(a, set()).add(cid)
        series._windex = idx
    return series._windex


def query(series, all_of=(), any_of=(), none_of=()):
    """The cards answering every one of all_of, at least one of any_of (where given), and none of none_of. An
    attribute ending in ':' matches any value ('in:' is any list); a prefix ending in '*' matches by prefix
    ('section:vn.II.C*')."""
    idx = index(series)

    def ids(a):
        if a.endswith("*") or a.endswith(":"):
            p = a.rstrip("*")
            return set().union(*(v for k, v in idx.items() if k.startswith(p))) if any(k.startswith(p) for k in idx) else set()
        return idx.get(a, set())
    out = set(series.works.cards)
    for a in all_of:
        out &= ids(a)
    if any_of:
        out &= set().union(*(ids(a) for a in any_of))
    for a in none_of:
        out -= ids(a)
    return out


def sort_key(series, how):
    cat = series.works

    def k(cid):
        f = cat.fields(cid) or {}
        who = store.fold(surname(f["author"][0])) if f.get("author") else ""
        t = re.sub(r"^(the|a|an) ", "", store.fold(plain(f.get("title") or "")))
        y = str(f.get("year") or "")
        return {"year": (y, who, t), "title": (t, y), "id": (cid,)}.get(how, (who or t, t, y))
    return k


def line(series, cid):
    """One line for a listing of cards: the id, the citation, where it is listed."""
    cat = series.works
    ws = sorted({f"{l.abbr} {s.code}" for l, s, _ in where(series).get(cid, [])})
    parts = [k for k, c in cat.cards.items() if c.get("in") == cid]
    out = f"{cid}\n    {plain(cat.render(cid))}"
    if parts:
        out += f"\n    holds: {', '.join(sorted(parts))}"
    return out + (f"\n    listed: {', '.join(ws)}" if ws else "" if parts else "\n    listed: nowhere")


# ---------------------------------------------------------------- check

def problems(series):
    """(level, where, message): errors fail `check`; warnings are shown."""
    cat = series.works
    out = []
    seen = {}
    for cid, c in cat.cards.items():
        where = f"works/{cat.file_of.get(cid)}"
        if not re.match(r"^w\.[a-z0-9][a-z0-9-]*$", cid):
            out.append(("error", where, f"{cid}: a card id is w. and lowercase words joined by hyphens"))
        if not c.get("c") and not c.get("title"):
            out.append(("error", where, f"{cid}: a card needs a title (structured) or c (verbatim)"))
        if c.get("c") and c.get("title"):
            out.append(("error", where, f"{cid}: a card is structured (title) or verbatim (c), not both"))
        if not c.get("c") and not c.get("year") and not c.get("paren") and not c.get("in"):
            out.append(("error", where, f"{cid}: a structured card needs a year"))
        for k in ("in", "edition_of", "translates"):
            if c.get(k) and cat.get(c[k]) is None:
                out.append(("error", where, f"{cid}: {k}: {c[k]} is no card"))
        x, steps = c.get("in"), set()
        while x and x not in steps:
            if x == cid:
                out.append(("error", where, f"{cid}: its `in` comes round to itself"))
                break
            steps.add(x)
            x = (cat.get(x) or {}).get("in")
        if cat.file_of.get(cid) != f"{letter(cid)}.yaml":
            out.append(("warn", where, f"{cid}: belongs in works/{letter(cid)}.yaml"))
        for a in [cid] + store.as_list(c.get("aliases")):
            if a in seen and seen[a] != cid:
                out.append(("error", where, f"{a}: two cards claim this id"))
            seen[a] = cid
    w = where_all(series)
    for lst in series.lists.values():
        for sec, e in lst.entries():
            for cid in e.get("_missing") or []:
                out.append(("error", e["id"], f"work: {cid} is no card"))
            if e.get("work"):
                b = e.get("byline")
                if isinstance(b, list) and not set(b) <= set(store.as_list(e["work"])):
                    out.append(("error", e["id"], "byline names a card the entry does not point to"))
                if e.get("card_note") not in (None, "replace", "omit"):
                    out.append(("error", e["id"], "card_note is replace or omit"))
    loose_ = [e["id"] for lst in series.lists.values() for sec, e in lst.entries() if adoptable(series, lst, sec, e)]
    if loose_:
        out.append(("warn", "lists/", f"{len(loose_)} entries cite works as text; ./bib works adopt "
                    f"{' '.join(loose_[:3])}{' …' if len(loose_) > 3 else ''} (or --all) makes them cards"))
    unused = [cid for cid in cat.cards if cid not in w]
    if unused:
        out.append(("warn", "works/", f"{len(unused)} cards nothing points to: {', '.join(sorted(unused)[:5])}"
                    + (" …" if len(unused) > 5 else "")))
    return out


def where_all(series):
    """Every card something points to: a listing, or another card (`in`, `edition_of`, `translates`)."""
    used = set(where(series))
    for c in series.works.cards.values():
        used |= {c[k] for k in ("in", "edition_of", "translates") if c.get(k)}
    return used


# ---------------------------------------------------------------- adopting a citation written as text

def new_id(f, taken):
    who = store.slug(surname(f["author"][0]), 3) if f.get("author") else ""
    t = re.sub(r"^(the|a|an)-", "", store.slug(short_title(plain(f["title"])), 6))
    t = "-".join(t.split("-")[:4])
    base = "w." + "-".join(x for x in (who, t) if x)
    cid = base
    if cid in taken and f.get("year"):
        cid = f"{base}-{store.slug(str(f['year']), 2)}"
    n = 2
    while cid in taken:
        cid, n = f"{base}-{n}", n + 1
    return cid


def adoptable(series, lst, sec, e):
    """The fields of each citation line of an entry that cites works as text, or None (no `c`, a pointer already,
    the calendar, a person in Part III, or a line that is no work: a case, a law, a speech)."""
    from .refs import Refs
    if lst.kind == "calendar" or e.get("work") or not e.get("c"):
        return None
    if Refs.is_people_section(sec) and (sec.code or "").startswith("III"):
        return None
    subj = e.get("s") if Refs.is_people_section(sec) and e.get("s") else None
    cs = store.as_list(e["c"])
    fs = [fields_of(c, subj) for c in cs]
    if any(f is None for f in fs):
        return None
    for i in range(1, len(fs)):          # one author named once for several works (ditto)
        if not fs[i].get("author") and fs[i - 1].get("author") and cs[i].lstrip().startswith("*") \
                and not fs[i].get("editor") and not fs[i - 1].get("_subject"):
            fs[i]["author"] = list(fs[i - 1]["author"])
            fs[i]["_ditto"] = True
    return list(zip(cs, fs))


def adopt(series, entries):
    """Make each entry's works cards (or find the card already holding the same citation), and point the entry at
    them; the note stays the listing's. Returns [(entry id, [card ids], [new card ids])]."""
    cat = series.works
    by_full = {render(c, cat=cat): cid for cid, c in cat.cards.items()}
    taken = set(cat.cards) | set(cat.alias)
    done = []
    for lst, sec, e in entries:
        pairs = adoptable(series, lst, sec, e)
        if not pairs:
            continue
        ids, new, byline = [], [], []
        subj = e.get("s")
        for c, f in pairs:
            if f.get("c"):
                card = {"c": c, "author": f["author"]} if f.get("_subject") or f.get("_ditto") else {"c": c}
            else:
                card = {k: v for k, v in f.items() if not k.startswith("_")}
            full = render(card, cat=cat)
            cid = by_full.get(full)
            if cid is None:
                cid = new_id(f, taken)
                taken.add(cid)
                cat.cards[cid] = {"id": cid, **card}
                cat.file_of[cid] = f"{letter(cid)}.yaml"
                by_full[full] = cid
                new.append(cid)
            ids.append(cid)
            if subj and not f.get("_subject") and card.get("author") and \
                    store.fold(card["author"][0]) == store.fold(subject_name(subj)):
                byline.append(cid)
        e["work"] = ids if isinstance(e["c"], list) else ids[0]
        del e["c"]
        if any(f.get("_ditto") for _, f in pairs):
            e["ditto"] = True
        if byline:
            e["byline"] = True if len(byline) == len(ids) else byline
        done.append((e["id"], ids, new))
    return done
