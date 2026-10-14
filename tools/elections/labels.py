"""Party labels as the Clerk prints them, with the OCR's misreadings put right.

The Clerk's volumes were read by OCR (tools/elections/make_elections.py, president.py); the readings confuse c and e
('Demoeratic', 'Republiean'), c and o ('Amorican'), n and a ('Soeinlist'), and run the dot leaders and the figures of
a line into its label ('Republican_~ 22-8 161, 597'). clean() is the label as printed: the leaders and figures cut off,
each word that is a near miss of a word the parties' names use (WORDS) put right, the rest as printed.

STYLE
 1. A word is put right only to a word of WORDS with the same length or one letter more or less, the same first
    letter (or an OCR's C for O, I for l), and a close likeness (difflib ratio 0.8 or more); FIX holds the misreadings
    that rule cannot reach. A label a person wrote ('Politicians Are Jokers') keeps its words.
 2. 'Democrat' and 'Democratic' are both printed (the Clerk writes 'Democrat' for the House and Senate, 'Democratic'
    for the presidential slates); each is kept as printed.
"""
import difflib
import re

WORDS = """Democrat Democratic Democrats Republican Republicans Liberal Liberals Conservative Independent Independents
Socialist Socialists Labor Workers Worker Prohibition American Americans Constitution Constitutional Communist
Christian Nationalist National States Rights Peace Freedom Party Economy Politics Iowa Farmer Government Industrial
Citizens Union United Taxpayers Tax Payers Voters Alliance Environment Majority Veterans Veteran Justice Integrity
Progress Unpledged Electors Pledged Write-in Scattering Vermonters Teacher Militant Afro-American Petition Nomination
Raza Unida Human Equal Constitutional Righteous Decency Vigilance Common Sense People Peoples America Economic Right
Taxpayer Independence Write-ins writein""".split()
WSET = {w.lower(): w for w in WORDS}
FIX = {"Deinoerat": "Democrat", "Soeinlist": "Socialist", "Probihition": "Prohibition", "lowa": "Iowa",
       "Ohristian": "Christian"}
FIRST = {"o": "c", "c": "o", "l": "i", "i": "l"}
JUNK = re.compile(r"\s*(?:[_~]|\.\s*[.\-—]|\.{2,}|\s[\-—]\s|\s[\-—]$|\s\d|—$|-$).*$")


def word(w):
    """One word put right, its punctuation kept."""
    m = re.match(r"^([^\w]*)([\w\-']+)([^\w]*)$", w)
    if not m:
        return w
    pre, core, post = m.groups()
    if core in FIX:
        return pre + FIX[core] + post
    if core.lower() in WSET or re.search(r"['’]", w):
        return w
    best, score = None, 0.0
    for v in WORDS:
        if abs(len(v) - len(core)) > 1:
            continue
        a, b = core[0].lower(), v[0].lower()
        if a != b and FIRST.get(a) != b:
            continue
        r = difflib.SequenceMatcher(None, core.lower(), v.lower()).ratio()
        if r > score:
            best, score = v, r
    if best and score >= 0.8:
        if core.islower():
            best = best.lower()
        return pre + best + post
    return w


def clean(p):
    """The label as printed, the OCR's leaders, figures and misreadings put right ('Republican_~ 22-8 161, 597'
    -> 'Republican'; 'Demoeratic' -> 'Democratic')."""
    if not p:
        return p
    s = JUNK.sub("", p.strip().replace("’", "'").replace("‘", "'"))
    s = re.sub(r"^[\W_]+(?=\w)", "", s).strip(" .,;:-—")
    s = re.sub(r"(\w)[’',]\s+(Workers|Labor)\b", r"\1 \2", s)
    return " ".join(word(w) for w in s.split())


NAME_FIX = {"Danicl": "Daniel"}


def name(n):
    """A candidate's name as printed, the OCR's slips put right: a stray mark before it ('_ Rudolph Nesmith'), a
    doubled stop ('James R..Jungroth'), an 8 read for an S initial ('Suzanne 8. Stevenson', 'Neil 8S. Bishop'), and
    the words of NAME_FIX."""
    if not n:
        return n
    s = re.sub(r"^[\W_]+(?=\w)", "", n.strip()) if not n.strip().startswith("(") else n.strip()
    s = re.sub(r"\.\.(?=\w)", ". ", s)
    s = re.sub(r"\b8S?\.", "S.", s)
    return " ".join(NAME_FIX.get(w, w) for w in s.split())


def not_a_name(n):
    """A line the OCR took for a candidate that is a heading ('For unexpired term ending Jan. 3, 1967')."""
    return bool(re.match(r"(?i)for (the )?(unexpired|full) term", n or ""))
