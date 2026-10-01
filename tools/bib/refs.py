"""Reading the conventions the prose already uses: section references
("K–J Adm. II.D", "(II.C, II.E)"), "Also Opp.", "Names: Heller, Tobin (K–J Adm. III.H)",
and the keys that say two entries are the same work or the same person.

Nothing here changes the data. The build uses it to make links; `check` uses it
to find references that point nowhere and works cited under two sections.
"""
import re

from . import store
from .markup import plain, italics, REF_RE, LINK_RE

CODE = r"[IVX]+(?:\.[A-Z](?:\.\d+)?)?"
RANGE = rf"{CODE}(?:–(?:{CODE}|[A-Z](?:\.\d+)?))?"
BARE = r"[IVX]+\.[A-Z](?:\.\d+)?"


class Refs:
    def __init__(self, series):
        self.series = series
        names = {}
        for lst in series.lists.values():
            names[lst.abbr] = lst.key
            for a in lst.meta.get("cite_as", []):
                names[a] = lst.key
        self.abbr_to_key = names
        words = sorted((a for a in names if not a.isdigit()), key=len, reverse=True)
        digits = sorted(a for a in names if a.isdigit())  # "1968" is a list only before a code
        alts = "|".join(re.escape(a) for a in words)
        dalts = "|".join(re.escape(a) for a in digits) or "(?!x)x"
        # an abbreviation, optionally followed by a section code; or a bare code.
        # "87th Cong." is a Congress, not the list.
        self.rx = re.compile(
            rf"(?P<abbr>(?<![\w])(?<!\dth )(?<!\dst )(?<!\dnd )(?<!\drd )(?:{alts}))(?:\s+(?P<code>{RANGE}))?(?![\w])"
            rf"|(?P<dabbr>(?<![\w(])(?:{dalts}))\s+(?P<dcode>{RANGE})(?![\w])"
            rf"|(?<![\w.–])(?P<bare>{BARE}(?:–(?:{CODE}|[A-Z](?:\.\d+)?))?)(?![\w])(?!\.\s*[A-Z][a-z])"  # not "I.M. Destler"
        )

    # ------------------------------------------------------------ section refs
    def scan(self, text, home):
        """Yield (start, end, list_key, code_or_None) for each reference in plain
        text. Bare codes belong to the list named just before them in the same
        parenthesis or clause, otherwise to `home`."""
        ctx, last_end = None, 0
        for m in self.rx.finditer(text):
            between = text[last_end:m.start()]
            if ctx and re.search(r"[);]|\.\s", between):
                ctx = None
            if m.group("abbr") or m.group("dabbr"):
                key = self.abbr_to_key[m.group("abbr") or m.group("dabbr")]
                code = m.group("code") or m.group("dcode")
                ctx = key if code else None
                yield m.start(), m.end(), key, code
            else:
                yield m.start(), m.end(), ctx or home, m.group("bare")
            last_end = m.end()

    def section_for(self, key, code):
        lst = self.series.lists.get(key)
        if not lst or not code:
            return None
        return lst.section(code.split("–")[0])

    # ------------------------------------------------------------ identity keys
    @staticmethod
    def work_keys(e):
        """(author surname, main title) for each work an entry cites, folded.
        The surname is '' for works cited title-first (films, edited volumes,
        cases), so a novel and the film made from it stay distinct."""
        keys = []
        for c in store.as_list(e.get("c")):
            ts = italics(c)
            if not ts:
                continue
            t = re.split(r"[:?!]\s", ts[0])[0]
            k = re.sub(r"^(the|a|an) ", "", store.fold(t))
            if len(k) < 4:
                continue
            text = plain(c)
            sur = ""
            if c.lstrip().startswith("*") and e.get("s") and "," in plain(e["s"]):
                # a memoir entry: "Kissinger, Henry A." then "*White House Years*"
                sur = store.fold(plain(e["s"]).split(",")[0]).split()[-1]
            elif not c.lstrip().startswith("*") and "," in text:
                author = re.split(r"\s+(?:&|with)\s+", text.split(",")[0])[0]
                words = [w for w in author.replace(".", " ").split() if w not in ("Jr", "Sr", "II", "III")]
                sur = store.fold(words[-1]) if words else ""
            keys.append((sur, k))
        return keys

    @staticmethod
    def full_titles(e):
        """Every italic title in an entry's citation lines, folded."""
        return [store.fold(t) for c in store.as_list(e.get("c")) for t in italics(c)]

    @staticmethod
    def name_key(e):
        """'Kennedy, Robert F.' -> 'kennedy robert'; 'Mao Zedong' -> 'mao zedong'."""
        keys = Refs.name_keys(e.get("s") or "")
        return keys[0][0] if keys else None

    @staticmethod
    def name_keys(s):
        """[(key, shown name)] for each person in a subject line; 'A; B' names two."""
        out = []
        for part in plain(s).split(";"):
            shown = part.strip()
            bare = re.sub(r"\s*\([^)]*\)", "", shown)
            if not bare:
                continue
            if "," in bare:
                sur, given = bare.split(",", 1)
                g = [w for w in store.fold(given).split() if w not in ("jr", "sr", "ii", "iii")]
                key = (store.fold(sur) + (" " + g[0] if g else "")).strip()
            else:
                key = store.fold(bare)
            if key:
                out.append((key, shown))
        return out

    @staticmethod
    def is_people_section(sec):
        """Part III, or a section of memoirs and biographies (subject lines are people)."""
        if (sec.code or "").startswith("III"):
            return True
        s = sec
        while s is not None:
            if re.search(r"memoir|biograph", s.title, re.I):
                return True
            s = s.parent
        return False

    def is_person(self, lst, sec, e):
        if lst.kind == "calendar" or not e.get("s"):
            return False
        return self.is_people_section(sec) and bool(self.name_keys(e["s"]))


def split_protected(text):
    """Split markup text into (is_protected, chunk) so refs inside [[...]] and
    [..](url) are left alone."""
    spans = sorted([m.span() for m in REF_RE.finditer(text)] + [m.span() for m in LINK_RE.finditer(text)])
    out, pos = [], 0
    for a, b in spans:
        if a < pos:
            continue
        if a > pos:
            out.append((False, text[pos:a]))
        out.append((True, text[a:b]))
        pos = b
    if pos < len(text):
        out.append((False, text[pos:]))
    return out
