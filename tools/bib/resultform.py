"""Election results in the calendar's text, in one form (the owner's rule, Oct. 23, 2026).

    scan(text)        the results in a calendar entry's `c`: (kind, matched text, message) for each one not in the form
    problems(series)  the calendar entries whose `c` gives a result not in the form [result-form]

The owner (Oct. 23, 2026): "fix the form to a single, prescribed standard", in place of commas, semicolons ("yes
1,876,185, no 3,408,090; 35.5 percent"), colons ("Yes 3,008,328, no 2,834,384: 51.5 percent"), counts without
percentages, percentages without counts, and margins in votes; "the simplest forms here, e.g., 'Anderson (R) over
Governor Docking (D), 511,534 to 402,261, 55.4 percent', are perfectly fine. Keep those everywhere."

STYLE
 1. A race: "Winner (P) over Loser (P), W to L, p percent": commas only, no colon or semicolon; the winner's count
    first; p the winner's share, to one decimal. In a primary the party is the primary's and not written ("Kennedy
    over Humphrey, 476,024 to 366,753, 56.5 percent").
 2. A margin, where the entry gives one or the race was close, after the share: "..., 50.3 percent, a 1,988-vote
    margin" (never "by 1,988 votes").
 3. A measure: yes first, then no, p the yes share: "Proposition 1 carries, 3,008,328 to 2,834,384, 51.5 percent";
    "Proposal 2 fails, 1,876,185 to 3,408,090, 35.5 percent". Never "yes ..., no ...".
 4. Always both counts and the percentage. A third candidate or more, after the two: "Name N, p percent", in the
    same sentence as the two.
 5. The denominator: all the votes cast for the office (for a measure, yes and no) where the source prints that
    total; where it gives only the two leading counts and others ran, their sum, with "of the two" after the
    percentage ("..., 52.1 percent of the two"). Where a rule differs (a measure needing a majority of all voting at
    the election, or two-thirds; a runoff below a majority), a few words after the figures say so.
 6. Several races or measures in one entry: each in the form, a sentence or a clause each.
 7. A count or share the sources read do not give stays out: "Check: the count" (or "the percentage") in the note.
    Quotations are left as printed (the text between double quotation marks is not read); an entry that must keep
    another form (a quotation set off without marks) takes `ok:result-form`.

What `problems` warns on, in an entry's `c`: "yes N"; a count followed by a colon or a semicolon and a share; "by N
votes"; "W to L" (thousands) without its share; a share without "percent"; a share without its counts in an entry on
an election (its thread an election thread, or a tag primary:, governors:, special:, election:); and in the form
itself, a share above W/(W+L), "of the two" that is not W/(W+L), a measure's share that is not, and a margin that is
not W - L. Not read: a convention's ballot ("1,321 to Goldwater's 10"), delegates and electoral votes, the polls
(thread Opinion), and other countries' parliamentary elections (party shares and seats).
"""
import re

N = r"\d{1,3}(?:,\d{3})+|\d{1,7}"
FORM = re.compile(rf"(?<![\d,.$])({N}) to ({N}), (\d{{1,3}}\.\d) percent( of the two)?(?:, an? ({N})-vote margin)?")
ALSO = re.compile(rf"(?<![\d,.$])({N}), (\d{{1,3}}\.\d) percent")
YESNO = re.compile(r"\b[Yy]es,? \d|\bno,? \d{1,3}(?:,\d{3})+")
PUNCT = re.compile(r"(?<![\d.])\d{1,3}(?:,\d{3})+[;:] \d{1,3}(?:\.\d)? percent")
BYVOTES = re.compile(r"\bby (?:about |almost |nearly |some |over |under |fewer than |more than |only |just )?"
                     r"\d{1,3}(?:,\d{3})* votes\b")
TO = re.compile(r"(?<![\d,.$])(\d{1,3}(?:,\d{3})+|\d{4,}) to (\d{1,3}(?:,\d{3})+|\d{4,})(?=[.,;:)]|$)")
PCT = re.compile(r"(?<![\d,.$])\d{1,3}(?:\.\d+)? percent")
BARE = re.compile(r"(?<![\d,.$–-])\d{1,2}\.\d(?![\d,]?\d)(?! percent)(?! (?:million|billion|mills?|cents|points?|"
                  r"seats?|years?|months?|days?|hours?|miles?|acres?|per|to|of)\b)(?=[,;.)]|\s|$)")
QUOTE = re.compile(r'"[^"]*"|“[^”]*”')
LINK = re.compile(r"\]\([^)]*\)|\(https?://[^)]*\)")
MEASURE = re.compile(r"\b(?:carries|carried|fails|failed|adopted|adopts|approved|approves|refused|refuses|rejected|"
                     r"rejects|ratified|ratifies|defeated|repealed)\b(?! (?:the|his|her|its) )")
RACE = re.compile(r"\b(?:over|against|beats|defeats|unseats|ahead of|leads)\b")
COUNT = re.compile(r"(?<![\d,.$])\d{1,3}(?:,\d{3})+(?:(?=[.;)]|, (?!\d)|$)| votes\b)")
VOTING = re.compile(r"\b(?:primary|runoff|election|elected|re-elected|elects|nominee|nominated|nomination|ballot|"
                    r"votes?|voters|canvass|returns|recount|carries|carried|adopted|refused|approved|rejected|"
                    r"write-ins?|unpledged|electors?|first|second|third|over|beats|defeats|unseats|holds the seat|"
                    r"takes the seat|to the seat|amendment|proposition|proposal|question|referendum|initiative)\b",
                    re.I)
# a convention's ballot, of delegates: not a popular vote
CONVENTION = re.compile(r"\b(?:\w+ ballot|delegates'?|convention's|roll call)\b")
UNOPPOSED = re.compile(r"\b(?:unopposed|without opposition|no opposition|no opponent)\b")
WORDED = re.compile(r"\d percent (?:yes|no|for|against)(?=[.,;)]|$)")
RATE = re.compile(r"(?:\bto|\bfrom|\bat|\bthan|\bof|\bby) $")
ELECTION_THREADS = ("elections-", "governors", "mayors", "specials", "state-constitutions", "electoral-college")
ELECTION_TAGS = ("primary:", "governors:", "special:", "election:")
# a share that is not a vote: of the people, the precincts, the registered (in an entry on an election all the same)
NOT_A_VOTE = re.compile(r"\s(?:of (?:the |its |their |all |his )?(?:people|population|precincts?|registered|eligible|"
                        r"adults|voting-age|counties|districts|seats|units|delegates|State's people|electorate|"
                        r"Negroes|Negro)|Negro|registered|turnout|of those registered|of the (?:State's|city's|"
                        r"county's) (?:people|population|voters)|of the voting|of its|above|below|of the ideal|"
                        r"of the average|more|less|fewer|higher|lower|increase|rise|cut|raise|tax)")


def clean(text):
    """The text the rule reads: no links' targets, no quotations."""
    return QUOTE.sub(lambda m: " " * len(m.group(0)), LINK.sub(lambda m: " " * len(m.group(0)), text or ""))


def num(s):
    return int(s.replace(",", ""))


ABBR = {"Jr", "Sr", "No", "Nos", "St", "Mt", "Ft", "Dr", "Mr", "Mrs", "Gov", "Sen", "Rep", "Gen", "Col", "Lt", "Va",
        "Md", "Mo", "Ga", "Fla", "Ala", "Tex", "Ill", "Ind", "Ky", "La", "Miss", "Mass", "Cal", "Wis", "Mich", "Minn",
        "Okla", "Ariz", "Colo", "Conn", "Kan", "Neb", "Nev", "Or", "Ore", "Pa", "Tenn", "Vt", "Wash", "Wyo", "Del",
        "Me", "Mont", "Ark", "vs", "v", "Jan", "Feb", "Mar", "Apr", "Aug", "Sept", "Oct", "Nov", "Dec", "ed", "p", "pp"}


def sentence_start(text, i):
    """Where the sentence (or the party's clause after a colon) holding text[i] begins."""
    for m in reversed(list(re.finditer(r"[.:] ", text[:i]))):
        if m.group(0) == ": ":
            return m.end()
        word = re.search(r"(\S*)$", text[:m.start()]).group(1)
        if word in ABBR or re.fullmatch(r"[A-Z]|(?:[A-Z]\.)+[A-Z]", word):
            continue
        return m.end()
    return 0


def sentence_of(text, i):
    return text[sentence_start(text, i):i]


def scan(text, election=False):
    """The results in `text` not in the form: (kind, the words matched, what is wrong)."""
    t = clean(text)
    out = []
    spans = []
    for m in FORM.finditer(t):
        spans.append(m.span())
        w, l, p = num(m.group(1)), num(m.group(2)), float(m.group(3))
        if w + l == 0:
            continue
        two = 100 * w / (w + l)
        before = sentence_of(t, m.start())
        measure = MEASURE.search(before[-120:]) and not RACE.search(before[-160:])
        if p > two + 0.051:
            out.append(("share", m.group(0), f"{p} percent is more than {w:,} of {w + l:,} ({two:.1f})"))
        elif m.group(4) and abs(p - two) > 0.051:
            out.append(("share", m.group(0), f'"of the two" is {two:.1f} percent, not {p}'))
        elif measure and abs(p - two) > 0.051:
            out.append(("share", m.group(0), f"a measure's share is yes over yes and no, {two:.1f} percent, not {p}"))
        if m.group(5) and num(m.group(5)) != abs(w - l):
            out.append(("margin", m.group(0), f"the margin is {abs(w - l):,} votes, not {m.group(5)}"))

    def inform(i):
        return any(a <= i < b for a, b in spans)
    for m in YESNO.finditer(t):
        out.append(("yes-no", m.group(0), 'yes and no: "Proposition 1 carries, Y to N, p percent"'))
    for m in PUNCT.finditer(t):
        out.append(("punctuation", m.group(0), "commas only: W to L, p percent"))
    for m in BYVOTES.finditer(t):
        out.append(("by-votes", m.group(0), 'a margin: "W to L, p percent, a N-vote margin"'))
    for m in TO.finditer(t):
        if inform(m.start()) or re.search(r"(?:from|between|of|some|about|nearly|ages?|pages?|Nos?\.|\$)\s*$",
                                          t[max(0, m.start() - 12):m.start()]):
            continue
        out.append(("no-share", m.group(0), "W to L without its share: add \", p percent\""))
    if election:
        for m in PCT.finditer(t):
            if inform(m.start()) or NOT_A_VOTE.match(t, m.end()) or CONVENTION.search(sentence_of(t, m.start())) or RATE.search(t, 0, m.start()) or \
                    re.match(r" (?:a year|the ceiling|on |of (?:income|the price|value))", t[m.end():]):
                continue
            sent = sentence_start(t, m.start())
            if re.search(rf"(?:{N}), $", t[:m.start()]) and any(sent <= a < m.start() for a, _ in spans):
                continue
            out.append(("no-count", m.group(0), "a share without its counts: W to L, p percent"))
        for m in COUNT.finditer(t):
            sent = sentence_of(t, m.start())
            if inform(m.start()) or sent.endswith(" to ") or UNOPPOSED.search(sent + t[m.start():m.start() + 40]) \
                    or not VOTING.search(sent) or CONVENTION.search(sent):
                continue
            out.append(("no-share", m.group(0), "a count without its share: W to L, p percent (or Name N, p percent)"))
        for m in WORDED.finditer(t):
            out.append(("worded", m.group(0), 'p percent, the winner\'s (or yes) share, without "yes" or "for"'))
        for m in BARE.finditer(t):
            if inform(m.start()):
                continue
            out.append(("bare-share", m.group(0), 'a share without "percent", or without its counts'))
    return out


def on_election(e):
    threads = [e.get("thread") or ""] + list(e.get("also") or [])
    if any(th.startswith(ELECTION_THREADS) for th in threads):
        return True
    return any(str(tg).startswith(ELECTION_TAGS) for tg in e.get("tags") or [])


def problems(series):
    """The calendar's `c` that gives a result not in the form (STYLE 1-7)."""
    out = []
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for _, e in lst.entries():
            c = e.get("c")
            if not isinstance(c, str) or not e.get("date") or (e.get("thread") or "").startswith("opinion"):
                continue
            for kind, words, msg in scan(c, on_election(e)):
                out.append((e["id"], f"{words!r}: {msg} [result-form]"))
    return out
