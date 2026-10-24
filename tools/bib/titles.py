"""Titles of works and sources, as the series writes them (the owner's request, Oct. 23, 2026).

    tidy(s)          title_case and span_dashes together: for a title the series renders from a generated file
    title_case(s)    a run of words in capitals put in title case
    span_dashes(s)   a span of years with a hyphen given an en dash
    problems(series) the hand-kept titles that do not follow STYLE 1-2

STYLE
 1. Title case: "Assimilate works titles to title case." A title, or a run of three words or more in one, printed in
    capitals ("OFFICIAL VOTE OF THE STATE OF ILLINOIS Cast at the GENERAL ELECTION") is put in title case: each word
    capitalized, but the articles, the conjunctions and the short prepositions (MINOR) after the first word and not
    after a colon, a dash or a bullet. A run of two words or more with one of four letters or more: a word with a
    period in it (U.S., D.C.), a roman numeral and a short word not MINOR (CIA, ER) stay in capitals, taken for
    initials, and the acronyms in ACRONYMS (NAACP, NATO). A word already in mixed case is left as written. Nothing else in the title changes.
 2. Year spans: "Assimilate hyphens to ndashes in the date spans of sources and works titles ... Don't otherwise
    refactor dates in sources and works titles." A span of years written with a hyphen (1959-1960, 1958-62) takes an
    en dash (1959–1960, 1958–62); the years' form is kept. Not in a URL, an id, a report number (ER IM 68-59) or a
    span of months or days.
 3. Applied where a title is rendered from a generated file (the governors' figures' sources, from Wikipedia's
    citations: governors.source_html); a hand-kept title is written so in its file, and `check` warns on one that is
    not [titles]: the works' titles, the State sources' titles, the italic titles in the calendar's notes.
"""
import re

MINOR = {"a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet", "as", "at", "by", "in", "of", "on", "to",
         "up", "via", "per", "from", "with", "into", "over"}
ACRONYMS = {"NAACP", "NATO", "SEATO", "CENTO", "SNCC", "SCLC", "NASA", "USIA", "HUAC", "UNESCO", "AFL-CIO", "USSR",
            "UAW", "OPEC", "NSAM", "MACV", "ARVN", "CINCPAC"}
ROMAN = re.compile(r"^(?=[MDCLXVI])M*(?:C[MD]|D?C{0,3})(?:X[CL]|L?X{0,3})(?:I[XV]|V?I{0,3})$")
CAPS_RUN = re.compile(r"\b[A-Z][A-Z'’]+(?:[ ,]+[A-Z][A-Z'’.]*)+\b")
SPAN = re.compile(r"(?<![\w/.#=:-])((?:1[6-9]|20)\d\d)-((?:1[6-9]|20)?\d\d)(?![\w-])")


def _word(w, first):
    core = w.strip(",;:")
    if "." in core or ROMAN.match(core) or not core.isupper() or core in ACRONYMS or (len(core) <= 3 and core.lower() not in MINOR):
        return w
    low = core.lower()
    out = low if (low in MINOR and not first) else low[:1].upper() + low[1:]
    return w.replace(core, out)


def title_case(s):
    """A run of capitals in title case (STYLE 1)."""
    def run(m):
        words = m.group(0).split(" ")
        if not any(len(w.strip(",;:")) >= 4 for w in words):
            return m.group(0)               # initials and acronyms (CIA, ER IM)
        start = m.start() == 0 or bool(re.search(r"[:•—–-]\s*$", s[:m.start()]))
        out, first = [], start
        for w in words:
            out.append(_word(w, first))
            first = w.endswith(":")
        return " ".join(out)
    return CAPS_RUN.sub(run, s or "")


def span_dashes(s):
    """A span of years with an en dash (STYLE 2), the later year's form kept."""
    def sub(m):
        a, b = m.group(1), m.group(2)
        later = int(b) if len(b) == 4 else int(a[:2] + b)
        return f"{a}–{b}" if later > int(a) else m.group(0)
    return SPAN.sub(sub, s or "")


def tidy(s):
    return span_dashes(title_case(s))


def problems(series):
    """Hand-kept titles with a hyphen in a span of years or a run of capitals (STYLE 3)."""
    out = []
    cat = series.works
    for cid in cat.cards:
        f = cat.get(cid) or {}
        for k in ("title", "c"):
            v = f.get(k)
            if isinstance(v, str):
                v = re.sub(r"\(https?://[^)]*\)", "", v)
                if (k == "title" and span_dashes(v) != v) or (k == "title" and title_case(v) != v):
                    out.append((cid, f"{k}: {v[:80]}: title case and en dashes in spans of years [titles]"))
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for _, e in lst.entries():
            for m in re.finditer(r"\*([^*\n]+)\*", re.sub(r"\(https?://[^)]*\)", "", e.get("n") or "")):
                if span_dashes(m.group(1)) != m.group(1):
                    out.append((e["id"], f"*{m.group(1)[:60]}*: an en dash in a span of years [titles]"))
    return out
