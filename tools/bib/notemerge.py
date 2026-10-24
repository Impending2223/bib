"""Two patches' notes on one calendar entry, reconciled (the owner's rule, Oct. 24, 2026: no agent's work overwrites
another's sight-unseen). The merge records a conflict where two patches set an entry's `n`; this proposes the joined
note for a person to read and accept, never writes it unread.

    propose(base, ours, theirs) -> (text, problems)

STYLE
 1. Works are matched by card, not by text: a card each side cites, moved or pinpointed. A card only one side changed
    (moved out of "To check:", given a pinpoint, a parenthetical, or newly cited) takes that side's form and place; a
    card both changed alike, that form; a card both changed differently keeps ours and is a problem to settle (two
    pinpoints for one card: the pages may be joined by hand).
 2. Sentences other than works runs are matched by their text with the works taken out: a sentence only theirs added
    ("Check: Dallek gives ...", a new primary record) is put in ours where it stood in theirs (after the sentence it
    followed, else before "To check:", "See" and "Names:"); one only theirs removed goes; one both rewrote is a problem.
 3. "Names:" takes both sides' names, ours' order first. "To check:" holds the cards neither side has read; it goes
    when it is empty.
 4. What is proposed is shown beside base, ours and theirs (tools/bib/patchaudit.py, `./bib reconcile`), and only a
    person's yes writes it.
"""
import re

ITEM = (r"\[\[w\.[^\]]+\]\](?:,[^;.\[\]()]*(?:\.[^;\s][^;.\[\]()]*)*)?(?: \((?:[^()]|\([^()]*\))*\))?")
CARD = re.compile(r"\[\[(w\.[^\]|]+)")
# a sentence ends at ". " before a capital, a bracket, a quotation or an asterisk; abbreviations kept by a short list
ABBR = re.compile(r"(?:\b(?:Jan|Feb|Mar|Apr|Aug|Sept|Oct|Nov|Dec|Pub|Rec|Cong|Res|Rep|Doc|No|Nos|Stat|Op|Att|Gen|Sess|Mr|"
                  r"Dr|St|Jr|Sr|Ft|Mt|vol|vols|ed|eds|pt|doc|docs|p|pp|n|nn|ch|sec|art|cl|U\.S|D\.C|N\.Y|"
                  r"[A-Z]))$")


def sentences(n):
    out, cur, i = [], "", 0
    while i < len(n):
        cur += n[i]
        if n[i] == "." and (i + 1 == len(n) or (n[i + 1] == " " and i + 2 < len(n) and re.match(r"[A-Z\[*\"'(]", n[i + 2]))):
            depth = cur.count("(") - cur.count(")") + cur.count("[") - cur.count("]")
            if depth == 0 and not ABBR.search(cur[:-1]):
                out.append(cur.strip())
                cur = ""
        i += 1
    if cur.strip():
        out.append(cur.strip())
    return out


def items(s):
    """A sentence's top-level items (split at semicolons outside brackets and parentheses)."""
    out, depth, cur = [], 0, ""
    for ch in s:
        depth += (ch in "([") - (ch in ")]")
        if ch == ";" and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    return [x for x in out + [cur.strip()] if x]


def card(x):
    m = CARD.match(x.strip())
    return m.group(1).strip() if m else None


def parse(n):
    """The note as ordered parts: ('tc', [items]) the To check run; ('works', [items]) a run of cited works;
    ('names', [names]); ('text', sentence)."""
    parts = []
    for s in sentences(n or ""):
        body = s[:-1] if s.endswith(".") else s
        if body.startswith("To check: "):
            parts.append(("tc", items(body[len("To check: "):])))
        elif body.startswith("Names: "):
            parts.append(("names", [x.strip() for x in body[len("Names: "):].split(",") if x.strip()]))
        else:
            its = items(body)
            if its and all(card(x) and re.fullmatch(ITEM, x) for x in its):
                parts.append(("works", its))
            else:
                parts.append(("text", s))
    return parts


def cards_of(parts):
    """card -> (form, where): where is 'tc' or the index of its works run."""
    out = {}
    for k, (kind, v) in enumerate(parts):
        if kind in ("tc", "works"):
            for x in v:
                c = card(x)
                if c:
                    out[c] = (x, "tc" if kind == "tc" else "hard")
    return out


def texts_of(parts):
    return [v for kind, v in parts if kind == "text"]


def render(parts):
    out = []
    for kind, v in parts:
        if kind == "tc":
            if v:
                out.append("To check: " + "; ".join(v) + ".")
        elif kind == "works":
            if v:
                out.append("; ".join(v) + ".")
        elif kind == "names":
            if v:
                out.append("Names: " + ", ".join(v) + ".")
        else:
            out.append(v)
    return " ".join(out)


def propose(base, ours, theirs):
    """The joined note and the problems a person must settle (STYLE 1-3)."""
    B, O, T = parse(base), parse(ours), parse(theirs)
    cb, co, ct = cards_of(B), cards_of(O), cards_of(T)
    problems = []
    want = {}                                   # card -> (form, where)
    for c in set(cb) | set(co) | set(ct):
        b, o, t = cb.get(c), co.get(c), ct.get(c)
        if o == t:
            v = o
        elif o == b:
            v = t
        elif t == b:
            v = o
        else:
            v = o
            problems.append(f"{c}: ours {o and o[0]!r} ({o and o[1]}), theirs {t and t[0]!r} ({t and t[1]})")
        if v:
            want[c] = v
    # sentences of text: theirs' additions and removals (STYLE 2)
    tb, to, tt = texts_of(B), texts_of(O), texts_of(T)
    strip = lambda s: re.sub(ITEM, "", s)
    added = [s for s in tt if s not in tb and s not in to]
    removed = [s for s in tb if s not in tt and s in to]
    if set(tb) - set(to) and set(tb) - set(tt) and (set(tb) - set(to)) != (set(tb) - set(tt)):
        changed = [s for s in tb if s not in to and s not in tt]
        if changed:
            problems.append("both sides rewrote: " + " | ".join(changed))
    for s in added:                             # a rewrite of a base sentence ours kept is a problem
        twin = [x for x in tb if strip(x)[:40] == strip(s)[:40]]
        if twin and twin[0] in to:
            problems.append(f"theirs rewrote: {twin[0]!r} -> {s!r}")
    # build from ours
    out = []
    for kind, v in O:
        if kind == "text" and v in removed:
            continue
        if kind in ("tc", "works"):
            v = [want[card(x)][0] for x in v if card(x) in want and want[card(x)][1] == ("tc" if kind == "tc" else "hard")
                 and want[card(x)][0] is not None]
        out.append([kind, v])
    # place theirs' added text after the sentence it followed in theirs
    for s in added:
        if any(p[0] == "text" and strip(p[1])[:40] == strip(s)[:40] for p in out):
            continue
        prev = None
        for kind, v in T:
            if kind == "text" and v == s:
                break
            prev = (kind, v)
        at = None
        if prev and prev[0] == "text":
            at = next((i + 1 for i, p in enumerate(out) if p[0] == "text" and p[1] == prev[1]), None)
        elif prev and prev[0] == "names":           # after the names: a Check of its own, at the end
            at = len(out)
        if at is None:
            at = next((i for i, p in enumerate(out) if p[0] in ("tc", "names") or
                       (p[0] == "text" and p[1].startswith("See "))), len(out))
        out.insert(at, ["text", s])
    # cards placed where wanted but not yet in ours' runs
    have = {card(x) for kind, v in out if kind in ("tc", "works") for x in v}
    for c, (form, where) in want.items():
        if c in have:
            continue
        if where == "hard":
            run = next((p for p in out if p[0] == "works"), None)
            if run is None:
                at = next((i for i, p in enumerate(out) if p[0] in ("tc", "names") or
                           (p[0] == "text" and (p[1].startswith("See ") or p[1].startswith("Made public")))), len(out))
                out.insert(at, ["works", []])
                run = out[at]
            run[1].append(form)
        else:
            run = next((p for p in out if p[0] == "tc"), None)
            if run is None:
                at = next((i for i, p in enumerate(out) if p[0] == "names" or
                           (p[0] == "text" and p[1].startswith("See "))), len(out))
                out.insert(at, ["tc", []])
                run = out[at]
            run[1].append(form)
    # names: both sides' (STYLE 3)
    nt = next((v for kind, v in T if kind == "names"), [])
    for p in out:
        if p[0] == "names":
            p[1] = p[1] + [x for x in nt if x not in p[1]]
    if not any(p[0] == "names" for p in out) and nt:
        out.append(["names", nt])
    return render([tuple(p) for p in out]), problems


def conflicts(series):
    """Every calendar entry with a conflict on `n`: (section, entry, conflict, proposal, problems)."""
    out = []
    for lst in series.lists.values():
        for sec, e in lst.entries():
            for c in e.get("conflict") or []:
                if c.get("field") == "n" and c.get("base") is not None:
                    text, probs = propose(c["base"], e.get("n") or "", c.get("theirs") or "")
                    out.append((sec, e, c, text, probs))
    return out
