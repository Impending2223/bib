"""A person named in a calendar entry's `c` without his `name:` tag (the owner, Nov. 21, 2026: "Please do build the
missing name tag check and run the sweep."). patchcheck STYLE 13 holds that every tag names a person; this holds the
reverse: a person the series holds (a name entry, lives.everyone) whom `c` names is tagged.

    ./bib check                 [name-untagged] warnings, on the whole calendar
    ./bib patch-check PATCH     the same, on the entries the patch adds or edits (patchcheck STYLE 14)

STYLE
 1. Named means one of a person's forms, whole: the name as his name entry writes it, in running order ('Dean Rusk'
    for 'Rusk, Dean'; 'Harry F. Byrd, Jr.' or 'Harry F. Byrd Jr.'; a name in its own order whole, 'Mao Zedong',
    'U Thant'), with or without its diacritics ('Ho Chi Minh', 'Hồ Chí Minh'), or a running form sources/name-forms.yaml
    lists for him ('Chairman Mao', 'Madame Nhu', 'Chou En-lai'). Never a bare surname; never a list's inverted form
    ('Diem, Ngo Dinh'); never a form that fits two persons: the same form of two, or a form another person's name
    could be written by as a 'Names:' token (build.Linker._token_fits: 'John Kennedy' fits John F. and a FRUS John).
 2. Not a person named: the form inside a longer name ('Harry F. Byrd' before 'Jr.'; an initial or a given name
    before it, 'Robert Lee' in 'and Henry Robert Lee'; a capitalized word after it, 'the John F. Kennedy Center');
    a place, a ship, a work or an organ named for him ('the Ho Chi Minh Trail', 'Hồ Chí Minh City', 'Mao Zedong
    Thought', 'the thought of Mao Zedong', 'Chairman Mao's works', 'the Chiang Kai-shek clique', 'the Brien McMahon
    lecture': NAMED_FOR, CANON, THOUGHT_OF; an article before it, 'the C. Turner Joy', 'a John F. Kennedy stamp';
    the USS *John F. Kennedy*: SHIP); his wife ('Mrs. John F. Kennedy'); the form in an italic title or a link's
    address; a form that is also a place's name (PLACE_FORMS, check.VIET_PLACES: Quảng Đức province, not the monk);
    a name followed by characters that are another man's (other_chars: 'its drafter Chen Yi 陳逸', not the marshal,
    陈毅 or 陳毅, whom the calendar writes so where it tags him: the given name's characters decide, the surname's
    being shared).
 3. Tagged means a `name:` tag of his key (lives.key_of), or of a FRUS form joined in his entry (lives frus-alias).
 4. Only calendar entries, not the threads' statements (cal.thread.*). The tag `ok:name-untagged` silences an entry.
 5. One pass: the forms indexed by their first word, the text folded letter for letter (fold_keep: the marks off, the
    case kept, the length kept, so a hit's span is the text's own); each capitalized word looked up, the longest form
    first. The table is built once a series (lives' cache) from lives.everyone, which check already builds.
"""
import re
import unicodedata

from . import store

RULE = "name-untagged"
NAMED_FOR = re.compile(r"\s+(?:[Tt]rail|[Cc]ity|[Tt]hought|[Mm]ausoleum|[Mm]emorial|[Pp]rize|[Dd]octrine|[Ss]chool|"
                       r"[Uu]niversity|[Rr]oad|[Ss]treet|[Aa]venue|[Bb]oulevard|[Ss]quare|[Pp]ort|[Aa]irport|"
                       r"[Ff]oundation|[Ll]ibrary|[Cc]enter|[Cc]entre|[Pp]lan|[Ll]ine|[Cc]ampaign|[Yy]outh|"
                       r"[Ii]nstitute|[Aa]cademy|[Bb]rigade|[Rr]egiment|[Dd]ivision|[Pp]ath|[Hh]ighway|"
                       r"[Ww]orks|[Ff]ield|[Bb]ridge|[Hh]all|[Ss]tadium|[Ss]paceport|[Pp]roject|[Ll]ectures?|"
                       r"[Ss]tamps?|[Pp]ostage|[Hh]alf-dollar|[Aa]ward|[Mm]edal|[Ff]und|[Ff]ellowships?|[Cc]hair|"
                       r"[Cc]lique|[Gg]roup|[Rr]emnants|[Rr]egime|[Gg]overnment|[Ss]pies|[Aa]ircraft|[Tt]roops|"
                       r"[Aa]rmy|[Gg]ang|[Bb]andits|[Aa]gents|[Ee]lements|[Ff]action|[Cc]hronology|[Nn]ianpu)\b")
# his canon, not his act: 'Mao Zedong's military thought', 'Chairman Mao's works'
CANON = re.compile(r"(?:\s*[\u2e80-\u9fff\uf900-\ufaff]+)?'s?\s+(?:[a-z]+\s+)?(?:[Tt]rail|[Cc]ity|[Tt]hought|[Ww]orks|"
                   r"[Ww]ritings|[Pp]oems|[Qq]uotations|[Tt]eachings|[Tt]heory|[Bb]ooks)\b")
# a form that is also a place's name: never a person's (Quảng Đức province; Vĩnh Lộc, Tân Bình; Hoằng Hóa district)
PLACE_FORMS = {"quang duc", "vinh loc", "hoang hoa"}
_CJK = "[\u2e80-\u9fff\uf900-\ufaff]"
THOUGHT_OF = re.compile(r"(?:[Tt]hought|[Ww]orks|[Ss]elected [Ww]orks|[Qq]uotations|[Pp]oems|[Ww]ritings|[Cc]ity|[Tt]rail) "
                        r"(?:of |from )(?:"
                        r"(?:Chairman|President|Comrade) )?$")
SHIP = re.compile(r"(?:U\.S\.S\.|USS|S\.S\.|SS|HMS|H\.M\.S\.|carrier|ship|cruiser|destroyer|submarine) $")
SUFFIX_AFTER = re.compile(r",?\s+(?:Jr\.?|Sr\.?|II|III|IV)(?![\w])")
# words that may stand before a name without making it part of a longer one: titles, offices, honorifics
TITLES = set("""President Premier Chairman Prime Minister Secretary General Gen Senator Sen Governor Gov Ambassador
Prince Princess King Queen Madame Mme Mrs Mr Ms Miss Dr Rep Representative Justice Judge Marshal Admiral Adm Vice
Foreign Defense Party Comrade Archbishop Cardinal Pope Father Reverend Rev Bishop Lieutenant Lt Colonel Col Captain
Capt Major Maj Sergeant Sgt Chief Deputy Mayor Attorney Speaker Leader Commander Field Air Marshal Brother Counselor
Chancellor Emperor Shah Sheikh Sultan Emir Generalissimo Delegate Envoy Minister Monsignor Sister
Thich Venerable Senior Junior Acting Former Late Then Presidential Majority Minority Whip Chairwoman Member Members
Secretary-General Under Assistant Associate Undersecretary Director Administrator Commissioner Treasurer Consul Officer
Professor Prof Editor Publisher Author Columnist Correspondent Reporter Agent Inspector Detective Private Corporal
Ensign Seaman Pilot Astronaut Cosmonaut Lord Lady Sir Dame Baron Count Duke Marquess Earl Viscount Grand Crown
Presidents Premiers Chairmen Ministers Generals Senators Governors Ambassadors Kings Commodore Brigadier
Vice-President Secretary-General Vice-Premier Vice-Chairman""".split())


class Index(dict):
    """{first word: [(form, key), ...]}, with `words`: every word of every person's name, folded (a name's word at a
    sentence's head before a form makes it a longer name: STYLE 2)."""
    words = frozenset()


_FOLD = {"Đ": "D", "đ": "d", "’": "'", "‘": "'", "ʼ": "'", "Ø": "O", "ø": "o", "Ł": "L", "ł": "l", "ı": "i"}


class _FoldTable(dict):
    """str.translate's table for fold_keep, filled as letters are met."""
    def __missing__(self, o):
        ch = chr(o)
        f = _FOLD.get(ch)
        if f is None:
            d = unicodedata.normalize("NFD", ch)
            f = d[0] if d and o > 127 else ch
        self[o] = f
        return f


_FOLD_TABLE = _FoldTable()


def fold_keep(text):
    """The text with its marks off, letter for letter: the case and the length kept ('Hồ Chí Minh' -> 'Ho Chi Minh')."""
    return text if text.isascii() else text.translate(_FOLD_TABLE)


def VIET_PLACES():
    from .check import VIET_PLACES as v
    return v


def running_forms(name):
    """A name entry's own name in running order (STYLE 1): 'Rusk, Dean' -> ['Dean Rusk']; 'Byrd, Harry F., Jr.' ->
    ['Harry F. Byrd, Jr.', 'Harry F. Byrd Jr.']; 'Mao Zedong' -> its forms (lives.name_forms), the inverted ones
    left out. A surname alone gives none."""
    from . import lives
    if lives.natural(name):
        return [f for f in lives.name_forms(name) if "," not in f and f.strip()]
    bare = re.sub(r"\s*\([^)]*\)", "", name)
    parts = [x.strip() for x in bare.split(",")]
    sur, given, suf = parts[0], (parts[1] if len(parts) > 1 else ""), (parts[2] if len(parts) > 2 else "")
    if not given or not sur:
        return []
    if suf:
        return [f"{given} {sur}, {suf}", f"{given} {sur} {suf}"]
    return [f"{given} {sur}"]


def table(series):
    """{first word (folded, case kept): [(form folded, key), ...] longest first}, and {key: name}: every form that
    names one person (STYLE 1). Built once a series (lives' cache)."""
    from . import lives
    return lives.cached("name-untagged", lambda: _table(series))


def _table(series):
    from . import lives
    from .build import Linker
    ev = lives.everyone(series)
    owners, names = {}, {}
    byword = {}                          # a folded word of a name -> the persons whose names hold it
    for p in ev:
        k = lives.key_of(p["name"])
        names[k] = p["name"]
        for f in running_forms(p["name"]):
            owners.setdefault(fold_keep(f), set()).add(k)
        for n in p["names"] | {p["name"]}:
            head = n.split(",")[0] if "," in n else n
            for w in store.fold(re.sub(r"\s*\([^)]*\)", "", head)).split():
                byword.setdefault(w, set()).add(k)
    allnames = {lives.key_of(p["name"]): p["names"] | {p["name"]} for p in ev}
    by_fold = {}                         # the same form, case and stops aside, of two persons
    for f, ks in owners.items():
        by_fold.setdefault(store.fold(f), set()).update(ks)
    index = Index()
    index.words = frozenset(w for ns in allnames.values() for n in ns
                            for w in store.fold(re.sub(r"\s*\([^)]*\)", "", n)).split())
    places = set(PLACE_FORMS) | {store.fold(x) for x in VIET_PLACES()}
    for f, ks in owners.items():
        ks = by_fold[store.fold(f)]
        if len(ks) != 1 or store.fold(f) in places:
            continue
        k, = ks
        words = store.fold(f).split()
        if not words:
            continue
        others = set().union(*(byword.get(w, set()) for w in words)) - {k}
        if any(Linker._token_fits(f, n) for o in others for n in allnames[o]):
            continue
        first = re.match(r"[A-Z][A-Za-z]*", f)
        if first:                        # a form opening lower-case ('al-...') is not looked for
            index.setdefault(first.group(0), []).append((f, k))
    for v in index.values():
        v.sort(key=lambda x: -len(x[0]))
    return index, names


_PROT = re.compile(r"\*[^*]+\*|\]\([^)]*\)|https?://\S+")
_WORD = re.compile(r"(?<![\w'.-])[A-Z][A-Za-z]*")     # a capitalized word's letters: the index's key


def hits(text, index, why=None):
    """[(start, end, key)]: each form of a person `text` names (STYLE 1, 2), the longest at each place, left to right.
    `why`, a list, takes (start, end, key, reason) for each form found and set aside (for review)."""
    if not text:
        return []
    t = fold_keep(text)
    prot = [m.span() for m in _PROT.finditer(t)]
    out, pos = [], 0
    for m in _WORD.finditer(t):
        a = m.start()
        if a < pos:
            continue
        cands = index.get(m.group(0))
        if not cands:
            continue
        for f, k in cands:
            b = a + len(f)
            if not t.startswith(f, a):
                continue
            nxt = t[b:b + 1]
            if nxt and (nxt.isalnum() or nxt == "-" or nxt == "'" and t[b + 1:b + 2].isalpha() and t[b + 1:b + 2] != "s"):
                continue
            reason = _aside(t, a, b, f, prot, getattr(index, "words", ()))
            if reason:
                if why is not None:
                    why.append((a, b, k, reason))
                break
            out.append((a, b, k))
            pos = b
            break
    return out


def _aside(t, a, b, f, prot, words=()):
    """Why the form at t[a:b] names no person here (STYLE 2), or None."""
    if any(x <= a < y for x, y in prot):
        return "title or link"
    rest = t[b:b + 40]
    if not re.search(r",?\s+(?:Jr|Sr|II|III|IV)\.?$", f) and SUFFIX_AFTER.match(rest):
        return "suffix after"
    if NAMED_FOR.match(rest) or CANON.match(rest):
        return "named for"
    if re.match(r"\s+[A-Z]", rest):
        return "capital after"
    before = t[max(0, a - 40):a]
    if SHIP.search(before):
        return "ship"
    if re.search(r"(?<![\w])(?:the|a|an) $", before):
        return "named for"                    # the Chiang Kai-shek clique, the C. Turner Joy, a John F. Kennedy stamp
    if re.search(r"(?<![\w])(?:Mrs\.?|Mme\.?) $", before) and not re.search(r"(?:Madame|Mrs|Mme)\b", f):
        return "his wife"                     # Mrs. John F. Kennedy
    if THOUGHT_OF.search(before):
        return "named for"
    pm = re.search(r"(\S+) $", before)
    if pm:
        pw = pm.group(1)
        if re.fullmatch(r"[A-Z]\.", pw):
            return "initial before"
        if pw[:1].isupper() and pw[-1:].isalpha() and not re.search(r"'s?$", pw) and \
                pw.split("-")[-1].rstrip(".") not in TITLES:
            head = t[:a - len(pw) - 1].rstrip()
            initial = not head or head[-1] in ".!?:;\"(\u2014"
            if not initial or store.fold(pw) in words:
                return "capital before"      # mid-sentence, or a name's word at a sentence's head: a longer name
    return None


def tagged(e, alias):
    """The keys the entry's `name:` tags give, each FRUS form joined in another's entry taken as his (STYLE 3)."""
    ks = set()
    for tg in e.get("tags") or []:
        tg = str(tg)
        if tg.startswith("name:"):
            ks.add(tg[5:])
            ks.add(alias.get(tg[5:], tg[5:]))
    return ks


def _run_after(text, b):
    """The characters written right after a name ('Chen Yi 陈毅'), or ''."""
    m = re.match(rf" ({_CJK}+)", text[b:b + 12])
    return m.group(1) if m else ""


def entry_hits(e, index, alias):
    """[(key, the words of `c` that name him, the characters after them, tagged)] for each form `c` holds."""
    have = tagged(e, alias)
    out = []
    for c in store.as_list(e.get("c")):
        if isinstance(c, str):
            for a, b, k in hits(c, index):
                out.append((k, c[a:b], _run_after(c, b), k in have or alias.get(k, k) in have))
    return out


def other_chars(run, known):
    """Whether the characters after a name are another man's (STYLE 2): his own, as the calendar writes them where it
    tags him, share none of their given name's with these, the surname aside ('its drafter Chen Yi 陳逸', not the
    marshal, 陈毅 or 陳毅, whose 陳 the drafter shares; but 陳毅 is he)."""
    if not (run and known):
        return False
    given = lambda c: set(c[1:]) if len(c) > 1 else set(c)
    return not any(run == c or given(run) & given(c) for c in known)


def chars_of(series):
    """{key: the characters the calendar writes after his name where it tags him}: one pass, kept (lives' cache)."""
    from . import lives

    def make():
        index, _ = table(series)
        alias = lives._CACHE.get("frus-alias", {})
        out = {}
        for e in calendar_entries(series):
            for k, _, run, ok in entry_hits(e, index, alias):
                if ok and run:
                    out.setdefault(k, set()).add(run)
        return out
    return lives.cached("name-untagged-chars", make)


def calendar_entries(series):
    for lst in series.lists.values():
        if lst.kind == "calendar":
            for _, e in lst.entries():
                if not str(e.get("id", "")).startswith(f"{lst.key}.thread."):
                    yield e


def entry_findings(e, index, alias, chars=None, found=None):
    """[(key, the words of `c` that name him)] for each person `c` names whom the entry does not tag (STYLE 1-4),
    each person once. `chars`: chars_of, called only where characters follow a name; `found`: entry_hits, if known."""
    if str(e.get("id", "")).startswith("cal.thread.") or "ok:" + RULE in (e.get("tags") or []):
        return []
    out, seen = [], set()
    for k, words, run, ok in (entry_hits(e, index, alias) if found is None else found):
        if ok or k in seen:
            continue
        if run and chars is not None and other_chars(run, chars().get(k)):
            continue
        seen.add(k)
        out.append((k, words))
    return out


def message(k, words, names):
    return (f"c names {words!r}, {names.get(k, k)}, without the tag name:{k}: add it, and the name to 'Names:' "
            f"(the names op), or tag ok:{RULE}")


def findings(series, entries=None):
    """[(id, key, words)] for the calendar entries given (all, by default) whose `c` names a person they do not tag.
    The whole calendar in one pass: the characters each tagged person is written with learned on the way."""
    from . import lives
    index, names = table(series)
    alias = lives._CACHE.get("frus-alias", {})
    if entries is None:
        rows = [(e, entry_hits(e, index, alias)) for e in calendar_entries(series)]
        if "name-untagged-chars" not in lives._CACHE:
            known = {}
            for _, hs in rows:
                for k, _, run, ok in hs:
                    if ok and run:
                        known.setdefault(k, set()).add(run)
            lives._CACHE["name-untagged-chars"] = known
    else:
        rows = [(e, None) for e in entries]
    out = []
    for e, hs in rows:
        for k, words in entry_findings(e, index, alias, lambda: chars_of(series), hs):
            out.append((e["id"], k, words))
    return out


def problems(series):
    """(id, message) for every calendar entry whose `c` names a person it does not tag ([name-untagged])."""
    _, names = table(series)
    for eid, k, words in findings(series):
        yield eid, message(k, words, names)
