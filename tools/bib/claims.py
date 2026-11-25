"""Each calendar entry's claims and the sources for each (the owner's request, Oct. 28, 2026: "break the entries down
into (invisible?) sentence-by-sentence, clause-by-clause units, and accord to each the appropriate (invisible?)
pincite"; and that it "be readily and programmatically transformed into a 'verbose' citation format, with its
invisible citations remapped to footnotes or inline citations"). Invisible for now: nothing here reaches a page.

    ./bib claims show ID [--inline]    the entry's units, lettered, and its sources as footnotes (or inline)
    ./bib claims stats                 how much of the calendar is mapped, and how finely
    ./bib claims seed ID [ID...]       the mechanical map as a `src` to start a reader's map from (for a patch)

Every entry has a map: the mechanical one, worked out from its note whenever it is wanted (STYLE 5), never stored;
or a reader's, stored in the entry as `src` (hidden; tools/bib/store.py keeps it after `n`), written by patch:

    src:
      c: 1a2b3c4d                              # the hash of `c` the map was made against (STYLE 4)
      rows:
      - 'https://www.govinfo.gov/...#page=59: all'          # a link the note (or `c`) prints
      - 'w.dallek-flawed-giant 70: A, C-E'                  # a work read, at that page, for those units
      - 'w.caro-passage-of-power 492: A'
      - 'via w.dallek-flawed-giant 70 n.36: B, E'           # a witness the work's note gives (sources/witnesses/)
      - '"Pearson''s column": all'                          # an item of the note without a link, by its first words

STYLE
 1. Units: `c` split at its sentences' ends and at semicolons, never inside a quotation, parentheses or brackets
    (a quotation of several sentences is one unit; a link's text and address too), lettered A, B, C ... Z, AA. A
    reader wanting a finer unit writes a semicolon: nothing is marked in `c`. The letters are the owner's ABCD.
 2. A row is one source at one pincite for the units it grounds: `all`, a list (`A, C`), a run (`C-E`), or `?` (not
    yet mapped: the note narrows it by a parenthetical a reader has still to turn into letters). A work cited at two
    pages for two claims is two rows. So each unit has its own sources and pages, and a footnote can be printed for
    each (verbose()).
 3. Every row names an item the note prints (or a link `c` prints): a card, a link's address, a cited record's
    work, page and note, or an unlinked item's first words. The note stays the visible record; the map says which
    claim each of its sources grounds, and `check` holds the two together (problems()).
 4. Only what a reader decides is stored. The mechanical map follows the note and `c` as they change; a reader's
    map is made against one `c` (its hash), and if `c` changes its letters may no longer fit: `check` reports it
    stale until a reader looks again and writes the new hash.
 9. Parts and fields (cuts.py; rulings 35f, 35g). A row may name, where it named letters, the numbers of the line's
    parts (`w.x 88: 3`, `w.x 88: 3, 5`): the number is stored in the line by a cut and stays with its words when the
    line is edited. Or a field, for a fact with no words in the line: `date`, `time` (whichever time field the entry
    has), `place` (`w.x 285: time`). resolve() turns numbers into their units' letters, so the footnotes, the
    visibility and the stemma work unit by unit as before. A number the line lacks, or a field the entry lacks, is
    an error. Letters stay the labels of the units as computed (the mechanical map, `claims show`).
 5. The mechanical map, from the note as written under the owner's rule "omission implies" (CLAUDE.md, "What each
    source stands for"): a work read (with its pinpoint, a number or a link: is_pin) and no parenthetical, `all`; with one, `?`; a link in the
    note's sources, `all`; a link in `c` (a statute, a case), the unit holding it; an unlinked item, no row (in the notes it is nearly always
    prose, a work's version of the event; a reader's map names an unlinked source by its first words). The note's
    sources are its sentences other than "To check:", "See ...", "Names:", "Check:", "Made public:" and the pointers
    ("Reply:", "The order:", "Bibliography:", "Statute (", "Opinion (").
 6. Verbose (verbose()): the units in order, a run of units with the same sources closed by one footnote (or one
    parenthetical, inline); each source in its form in the note (a work by its short form and the row's page; a link
    by the note's text for it; a cited record "citing" its description, joined to the work's page where both ground
    the unit, Bluebook's "70 & n.36 (citing ...)"); the `?` rows in a last footnote with the
    note's parenthetical; then the note's other sentences (To check, See, Names, Check) as they stand.
 7. A label (the reader's brief, R32: a sentence of the note that states a fact with its source, "The Senate sat from
    noon to 7:02 p.m.: [Daily Digest, D468](…)", "Votes: ...") stands for the unit it bears on, not the whole line;
    the mechanical map cannot tell which, and gives its items the first unit, where the entry's date and its day's
    facts sit (the owner, Nov. 21, 2026: "'The Senate sat from noon to 7:02 p.m.' should only be in the first
    footnote here"), never all; a reader's map says otherwise where it should. The label stays the item's head
    (note_labels). An item that only points to a themed list's section, "(Viet. II.I.3)", is no source: it goes
    with the note's other sentences (is_xref).
"""
import collections
import hashlib
import re

from . import markup, store

LETTERS = [chr(65 + i) for i in range(26)] + [chr(65 + i) + chr(65 + j) for i in range(26) for j in range(26)]
NOT_SOURCE = ("To check:", "See ", "Names:", "Check:", "Made public", "Reply:", "The order:", "Bibliography:",
              "Statute (", "Opinion (", "Also ")
LINK = markup.LINK_RE
FIELDS = ("date", "time", "place")           # an entry's facts with no words in the line (STYLE 9; 35g, 2)
_TARGET = r"(?:a?\d+|date|time|place)"       # a part's number, a claim's id (cuts.py, STYLE 7), a field
ROW = re.compile(r"^(?P<src>.+?): (?P<units>all|\?|[A-Z]{1,2}(?:-[A-Z]{1,2})?(?:, [A-Z]{1,2}(?:-[A-Z]{1,2})?)*|"
                 + _TARGET + r"(?:, " + _TARGET + r")*)$")
NUMBERED = re.compile(r"^" + _TARGET + r"(?:, " + _TARGET + r")*$")
QUOTES = '"“”'


def chash(c):
    return hashlib.sha1((c or "").encode("utf-8")).hexdigest()[:8]


UNIT_NEXT = re.compile(r"[A-Z0-9\[*\"“'(]")       # what starts a unit after ". " (and after a closing quotation:
UNIT_NEXT_Q = re.compile(r"[A-Z0-9\[*\"“(]")      # the same less the apostrophe)


def units(c):
    """The units of `c` (STYLE 1), as strings in order: a new list each call, of a split made once for each `c`
    (_units; code review C, PERF 8)."""
    return list(_units(c))


@store.memo
def _units(c):
    from .notemerge import ABBR
    out, cur, depth, inq, i, s = [], "", 0, False, 0, c or ""
    while i < len(s):
        ch = s[i]
        cur += ch
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(0, depth - 1)
        elif ch in QUOTES:
            inq = not inq if ch == '"' else (ch == "“")
        nxt = s[i + 1:i + 3]
        if depth == 0 and not inq:
            end = False
            if ch == ";" and nxt[:1] == " ":
                end = True
            elif ch in ".?!" and (i + 1 == len(s) or (nxt[:1] == " " and UNIT_NEXT.match(nxt[1:2] or ""))):
                end = ch != "." or not ABBR.search(cur[:-1])
            elif ch in QUOTES and cur[-2:-1] in (".", "?", "!") and (i + 1 == len(s) or (nxt[:1] == " " and
                                                                                              UNIT_NEXT_Q.match(nxt[1:2] or ""))):
                end = True
            if end:
                out.append(cur.strip())
                cur = ""
        i += 1
    if cur.strip():
        out.append(cur.strip())
    return tuple(out)


def letters(n):
    return LETTERS[:n]


def parse_units(spec, n):
    """`all`, `?`, or letters and runs -> a set of letters (or the string '?'); None where it does not parse."""
    if spec == "all":
        return set(letters(n))
    if spec == "?":
        return "?"
    out = set()
    for part in spec.split(", "):
        if "-" in part:
            a, b = part.split("-")
            if a not in LETTERS or b not in LETTERS or LETTERS.index(a) > LETTERS.index(b):
                return None
            out |= set(LETTERS[LETTERS.index(a):LETTERS.index(b) + 1])
        else:
            out.add(part)
    return out


def parse_target(spec, e):
    """A row's numbers and fields (STYLE 9) -> the letters of the parts' units, with the fields' names beside them
    ({'B', 'C', 'time'}); None where the line has no such part or the entry no such field. Everything downstream
    works unit by unit, as before; a field's name is no unit's letter, so it gives no unit a source."""
    from . import cuts
    us = cuts.units_of(e)
    out = set()
    for t in spec.split(", "):
        if t in FIELDS:
            if not has_field(e, t):
                return None
            out.add(t)
        elif t in us:
            out |= {LETTERS[i] for i in us[t]}
        else:
            return None
    return out


def named_letters(e, spec):
    """The letters a ruling's `@` or a variant's `unit` names: a letter, or parts' numbers joined by a dot or a comma
    (`3`, `3.4`), turned into their units' letters; None where the line has no such unit or part."""
    spec = str(spec)
    if re.fullmatch(r"a?\d+(?:(?:\.|, )a?\d+)*", spec):
        u = parse_target(spec.replace(".", ", "), e)
        return u
    n = len(units(e.get("c") or ""))
    return {spec} if spec in letters(n) else None


def has_field(e, f):
    if f == "time":
        return any(e.get(k) not in (None, "") for k in ("time", "time_approx", "time_range"))
    return e.get(f) not in (None, "")


def parse_row(row):
    """(kind, key, pin, note, units spec) or None. kind: card, via, url, text."""
    m = ROW.match(row or "")
    if not m:
        return None
    src, spec = m.group("src"), m.group("units")
    x = re.match(r"^via (x\.\S+)$", src)                 # a witness of the registry (tools/bib/witnesses.py)
    if x:
        return ("witness", x.group(1), None, None, spec)
    v = re.match(r"^via (w\.\S+) ((?:[IVXL]+, )?\S+) n\.(\S+)$", src)   # a part or volume before the page: "IV, 118"
    if v:
        return ("via", v.group(1), v.group(2), v.group(3), spec)
    w = re.match(r"^(w\.\S+)(?: (.+))?$", src)
    if w:
        return ("card", w.group(1), w.group(2), None, spec)
    if re.match(r"^https?://\S+$", src):
        return ("url", src, None, None, spec)
    t = re.match(r'^"(.+)"$', src)
    if t:
        return ("text", t.group(1), None, None, spec)
    return None


OWN_SENTENCE = re.compile(r" (?=(?:To check: |Names: |See \[\[|Check: ))")


def note_parts(n):
    """The note's sentences split into its sources (STYLE 5) and the rest, in order: ([source items], [other]); new
    lists each call, of a split made once for each note (_note_parts; code review C, PERF 8)."""
    src, other = _note_parts(n)
    return list(src), list(other)


def note_labels(n):
    """{item: its label}: the items of a sentence that opens on a label (STYLE 7), each with it."""
    return dict(_note_parts3(n)[2])


@store.memo
def _note_parts(n):
    src, other, _ = _note_parts3(n)
    return src, other


# A label (R32: "Votes: ...", "The Senate sat from noon to 7:02 p.m.: [Daily Digest, D468](…)"): prose before ": " at a
# source sentence's head, words in it, no brackets, its italics and quotations closed, a cite after it
LABEL = re.compile(r"^(?P<label>(?:[^\[\]():;]|(?<=\d):(?=\d\d)|\([^()\[\]]*\)){2,120}?):\s+(?=\S)")
# A pointer to a themed list's section, "(Viet. II.I.3)", "(K–J Cong. II.J.2)": no source (STYLE 5)
XREF = re.compile(r"\((?:[A-Z][\w–'’]*\.?|\d{4})(?: [A-Z][\w–'’]*\.?)? [IVX]+(?:\.[A-Z0-9]+)*\)")


def label_of(item):
    """The label an item opens on (LABEL), or None."""
    m = LABEL.match(item or "")
    if not m or item.startswith(NOT_SOURCE):
        return None
    lab = m.group("label").strip()
    if not item[m.end():].startswith(("[", "FRUS ")):     # a cite after it, not a title's subtitle ("Special Message
        return None                                       # to the Congress: Program for ...")
    if not re.search(r"[a-z]{3}", lab) or lab.count("*") % 2 or lab.count('"') % 2 or re.search(r"\d{4}[–-]\d", lab):
        return None
    return lab


def is_xref(item):
    """An item that points to a themed list's section and cites nothing ("Report of McNamara and Taylor to the President
    (Viet. II.I.3)")."""
    return bool(XREF.search(item or "")) and "[[" not in item and "](" not in item


@store.memo
def _note_parts3(n):
    from .notemerge import items, sentences
    src, other, labels = [], [], []
    chunks = []
    for s in sentences(n or ""):        # a sentence the splitter ran on past an abbreviation ("86th Cong. To check: ...")
        chunks += [c.strip() for c in OWN_SENTENCE.split(s) if c.strip()]
    for s in chunks:
        if s.startswith(NOT_SOURCE):
            other.append(s)
        else:
            body = s[:-1] if s.endswith(".") else s
            its = items(body)
            lab = label_of(its[0]) if its else None
            for it in its:
                if is_xref(it):
                    other.append(it.rstrip(".") + ".")
                    continue
                src.append(it)
                if lab:
                    labels.append((it, lab))
    return tuple(src), tuple(other), tuple(labels)


CARD_ITEM = re.compile(r"^\[\[(w\.[^\]|]+)(?:\|[^\]]*)?\]\](?:, ([^(]+?))?\s*(\((?:[^()]|\([^()]*\))*\))?$")
# A card whose pinpoint is a link and which takes a parenthetical too ("[[w.x]], [77–81](…#page=75) (the talk)"): read
# by the claims as its link (item_key: a url item), taken by the `cite` op all the same (the Chen test, point 9).
CARD_LINKED = re.compile(r"^\[\[(w\.[^\]|]+)(?:\|[^\]]*)?\]\], (\[[^\]]*\]\((https?://[^)\s]+)\))\s*(\((?:[^()]|\([^()]*\))*\))$")


def is_pin(text):
    """Whether what follows a work's card is a pinpoint: it names a number (a page, a volume and page, a document, a
    chapter, a footnote) or links the place read. A pointer in words ("on Rusk", "for the arithmetic", a chapter's
    title) is no pinpoint: it is recalled, and the work stands behind "To check:" (the owner, Oct. 30, 2026)."""
    return bool(text) and (re.search(r"\d", text) is not None or "](http" in text or ROMAN_PIN.match(text) is not None)


# A front-matter page in lower-case roman ("xi–xii"), standing first after the card: a valid numeral under 400, so a
# word ("civil", "ill") is none.
_ROMAN = r"c{0,3}(?:xc|xl|l?x{0,3})(?:ix|iv|v?i{0,3})"
ROMAN_PIN = re.compile(rf"^[\s,]*(?:pp?\. )?(?=[clxvi])({_ROMAN})(?:[–-](?=[clxvi]){_ROMAN})?(?=$|[\s,;.()])")


def item_key(item):
    """A source item's kind and key: ('card', id, pin, paren) | ('url', address) | ('text', first words). A card's pin
    is None where what follows it is no pinpoint (is_pin)."""
    m = CARD_ITEM.match(item.strip())
    if m:
        pin = (m.group(2) or "").strip() or None
        linked = bool(pin) and pin.endswith("]") and (m.group(3) or "").startswith("(http")   # ", at [site](url)"
        return ("card", m.group(1).strip(), pin if pin and (linked or is_pin(pin)) else None, m.group(3))
    lk = LINK.search(item)
    if lk:
        return ("url", lk.group(2))
    return ("text", " ".join(item.split()[:4]))


def mechanical(e):
    """The mechanical map (STYLE 5): {c, rows} or None where the note names no source."""
    c, rows = e.get("c") or "", []
    us = units(c) if isinstance(c, str) else []
    srcs, _ = note_parts(e.get("n"))
    labels = note_labels(e.get("n"))
    for it in srcs:
        k = item_key(it)
        whole = "A" if it in labels and len(us) > 1 else "all"   # a label's item: the first unit (STYLE 7)
        if k[0] == "card":
            if k[2]:
                rows.append(f"{k[1]} {k[2]}: {'?' if k[3] else whole}")
        elif k[0] == "url":
            rows.append(f"{k[1]}: {whole}")
        # an unlinked item is no row of the mechanical map: in the notes it is nearly always prose (a work's version of
        # the event, "Johnson gives 7:40 p.m."), seldom a source; a reader's map names an unlinked source by its words
    for i, u in enumerate(us):
        for lk in LINK.finditer(u):
            rows.append(f"{lk.group(2)}: {LETTERS[i]}")
    seen, out = set(), []
    for r in rows:
        if r not in seen:
            seen.add(r)
            out.append(r)
    if not out:
        return None
    return {"c": chash(c), "rows": out}


def effective(e):
    """The entry's map: a reader's, else the mechanical one (STYLE 4)."""
    return e.get("src") or mechanical(e)


def calendar(series):
    for lst in series.lists.values():
        if lst.kind == "calendar":
            for sec in lst.walk():
                for e in sec.entries:
                    if not e["id"].startswith(f"{lst.key}.thread.") and isinstance(e.get("c"), str):
                        yield sec, e


def resolve(e, cards=None):
    """The entry's rows as (row, kind, key, pin, note, units set or '?', the note's item) for rendering and checking."""
    n_units = len(units(e.get("c") or ""))
    srcs, _ = note_parts(e.get("n"))
    by, all_ = {}, {}
    for it in srcs:
        k = item_key(it)
        by.setdefault((k[0], k[1]), it)
        all_.setdefault((k[0], k[1]), []).append(it)
    out = []
    for r in (effective(e) or {}).get("rows") or []:
        p = parse_row(r)
        if p is None:
            out.append((r, None, None, None, None, None, None))
            continue
        kind, key, pin, note, spec = p
        u = parse_target(spec, e) if NUMBERED.match(spec) else parse_units(spec, n_units)
        if kind in ("card", "via") and len(all_.get(("card", key)) or []) > 1 and pin:
            want = _pages(pin)                 # a card cited twice (two issues of a periodical): the item whose pages
            fit = [it for it in all_[("card", key)]       # hold the row's
                   if want is not None and (_pages(item_key(it)[2]) or set()) >= want]
            if fit:
                out.append((r, kind, key, pin, note, u, fit[0]))
                continue
        if kind == "witness":                 # reached through the note's works (witnesses.problems holds it)
            item = next((v for (k, kk), v in by.items() if k == "card"), None) or next(iter(by.values()), None)
            out.append((r, kind, key, pin, note, u, item))
            continue
        item = by.get(("card", key)) if kind in ("card", "via") else by.get((kind, key)) if kind == "url" else \
            next((v for (k, kk), v in by.items() if k == "text" and kk.startswith(key[:30])), None)
        if kind == "url" and item is None:      # a link not first in its item ("X, as given in Y": one item, two links)
            item = next((it for it in srcs if any(m.group(2) == key for m in LINK.finditer(it))), None)
        if kind == "url" and item is None:
            lk = next((m for m in LINK.finditer(e.get("c") or "") if m.group(2) == key), None)
            item = lk.group(0) if lk else None
        out.append((r, kind, key, pin, note, u, item))
    return out


def _pages(s):
    """The page numbers a pinpoint names (arabic; '492–94' → 492..494), or None where it names none we can read."""
    out = set()
    for a, b in re.findall(r"(\d+)(?:[–-](\d+))?", s or ""):
        lo = int(a)
        hi = int(b) if b else lo
        if b and len(b) < len(a):
            hi = int(a[:len(a) - len(b)] + b)
        if hi - lo > 400:
            return None
        out |= set(range(lo, hi + 1))
    return out or None


def problems(series):
    """(errors, warnings): errors are rows that do not parse or name nothing the note prints; warnings are counts
    (a stale map, unmapped rows, a source with no row, a unit no source covers), one line each, the entries listed by
    `./bib claims stats`."""
    errors, counts = [], collections.Counter()
    reg = register(series)
    for _, e in calendar(series):
        if e.get("src") is not None:
            src = e["src"]
            if not isinstance(src, dict) or not isinstance(src.get("rows"), list) or set(src) - {"c", "rows"}:
                errors.append((e["id"], "src: {c, rows} (tools/bib/claims.py)"))
                continue
            if src.get("c") != chash(e.get("c")):
                counts["stale"] += 1
        elif mechanical(e) is None:
            continue
        n_units = len(units(e.get("c")))
        cover = set()
        for r, kind, key, pin, note, u, item in resolve(e):
            if kind is None:
                errors.append((e["id"], f"src row does not parse: {r!r}"))
                continue
            if u is None or (u != "?" and not u <= set(letters(n_units)) | set(FIELDS)):
                errors.append((e["id"], f"src row names a unit the entry lacks ({n_units} units): {r!r}"))
                continue
            if item is None:
                errors.append((e["id"], f"src row names nothing the note prints: {r!r} (a row names "
                                        "a card the note cites at that page, a link the note or c prints, or a record "
                                        "the note names: add the item to the note, or mend or drop the row)"))
                continue
            if kind == "via" and (key, str(pin), str(note)) not in reg:
                errors.append((e["id"], f"src row names a record sources/witnesses/ does not hold at that note: {r!r}"))
            if kind == "card" and series.works.get(key) is None:
                errors.append((e["id"], f"src row names no card: {key}"))
            if kind in ("card", "via") and pin:
                k = item_key(item)
                have, want = _pages(k[2] if k[0] == "card" else ""), _pages(pin)
                if have is not None and want is not None and not want <= have:
                    errors.append((e["id"], f"src row's pages {pin} not among the note's ({k[2]}): {r!r}"))
            if u is None:
                errors.append((e["id"], f"src row names a part the line does not have, or a field the entry lacks "
                                        f"(./bib claims show {e['id']} prints the parts): {r!r}"))
            elif u == "?":
                counts["unmapped"] += 1
                cover |= set(letters(n_units))
            else:
                cover |= u
        if set(letters(n_units)) - cover:
            counts["uncovered"] += 1
        mapped = {(k, key) for _, k, key, *_ in resolve(e) if k}
        for it in note_parts(e.get("n"))[0]:
            m = CARD_ITEM.match(it.strip()) or re.match(r"^[a-z][^\[\]();]{0,40}, (\[\[w\.[^\]|]+\]\])$", it.strip())
            if m and item_key(it)[0] != "card" or (m and item_key(it)[2] is None):
                errors.append((e["id"], f"a work cited among the sources read without a pinpoint, {it.strip()[:70]!r}: "
                                        "a pinpoint names a number or links the place read; else the work goes behind "
                                        "\"To check:\""))
        for it in note_parts(e.get("n"))[0]:
            k = item_key(it)
            if (k[0] == "card" and k[2] and ("card", k[1]) not in mapped) or (k[0] == "url" and ("url", k[1]) not in mapped):
                counts["unrowed"] += 1
                break
    warns = []
    words = {"stale": "readers' maps made against an earlier `c` (map again; write the new hash)",
             "unmapped": "rows not yet mapped to units (`?`: the note's parenthetical, to be turned into letters)",
             "unrowed": "entries with a source in the note and no row for it",
             "uncovered": "entries with a unit no source covers"}
    for k in ("stale", "unrowed", "uncovered", "unmapped"):
        if counts[k]:
            warns.append(("lists/cal/", f"{counts[k]} {words[k]}"))
    return errors, warns


def stats(series):
    t = collections.Counter()
    for _, e in calendar(series):
        t["entries"] += 1
        if not effective(e):
            t["no source in the note"] += 1
            continue
        t["mapped by a reader" if e.get("src") else "mechanical"] += 1
        rows = resolve(e)
        n_units = len(units(e.get("c")))
        t["units"] += n_units
        if any(u not in ("?", None) and u != set(letters(n_units)) for *_, u, _ in rows):
            t["finer than the whole entry"] += 1
        t["rows"] += len(rows)
        t["rows ?"] += sum(1 for *_, u, _ in rows if u == "?")
    return t


def _render_row(series, e, kind, key, pin, note, item, register):
    from .works import short_form
    if kind == "card":
        return f"{short_form(key, series.works)}{', ' + pin if pin else ''}"
    if kind == "via":
        rec = register.get((key, str(pin), str(note)))
        from . import witnesses
        where = witnesses.cite_where(rec.get("where")) if rec else ""
        what = (f"{rec.get('record')}, {where}" if where else rec.get("record")) if rec else "a record"
        return f"{short_form(key, series.works)}, {pin} n.{note} (citing {what})"
    if kind == "witness":
        from . import witnesses
        w = witnesses.load()[0].get(key)
        where = witnesses.cite_where(w.get("where")) if w else ""
        return f"{w.get('what')}, {where}" if w and where else (w or {}).get("what") or key
    if kind == "url":
        return item or key
    return item or key


def register(series):
    """{(card, page, note): witness} through the works' edges in sources/witnesses/ (tools/bib/witnesses.py)."""
    from . import witnesses
    return witnesses.register(series)


def verbose(series, e, inline=False):
    """The entry with its sources as footnotes (or inline parentheticals): (text, [footnotes], [the note's other
    sentences]) (STYLE 6)."""
    us = units(e.get("c") or "")
    reg = register(series)
    rows = resolve(e)
    per = []
    for i, _ in enumerate(us):
        L = LETTERS[i]
        mine = [(k, key, pin, note, item) for r, k, key, pin, note, u, item in rows if k and u not in (None, "?") and L in u]
        vias = {(key, pin): note for k, key, pin, note, _ in mine if k == "via"}
        out = []
        for k, key, pin, note, item in mine:
            if k == "card" and (key, pin) in vias:          # the page and its note, one citation: "70 & n.36 (citing ...)"
                v = _render_row(series, e, "via", key, pin, vias[(key, pin)], item, reg)
                out.append(v.replace(f", {pin} n.", f", {pin} & n.", 1))
            elif k == "via" and any(k2 == "card" and (key2, pin2) == (key, pin) for k2, key2, pin2, _, _ in mine):
                continue
            else:
                out.append(_render_row(series, e, k, key, pin, note, item, reg))
        per.append(tuple(out))
    q = [(_render_row(series, e, k, key, pin, note, item, reg), item) for r, k, key, pin, note, u, item in rows
         if u == "?"]
    text, notes = [], []
    for i, u in enumerate(us):
        text.append(u)
        last = i + 1 == len(us)
        if last or per[i + 1] != per[i]:
            srcs = list(per[i])
            if last and q:
                srcs += [f"{s} {re.search(r'(\(.*\))$', it or '').group(1) if re.search(r'(\(.*\))$', it or '') else ''}".strip()
                         for s, it in q]
            if not srcs:
                continue
            if inline:
                text[-1] = text[-1] + " (" + "; ".join(srcs) + ")"
            else:
                notes.append("; ".join(srcs) + ".")
                text[-1] = text[-1] + f"[^{len(notes)}]"
    return " ".join(text), notes, note_parts(e.get("n"))[1]
