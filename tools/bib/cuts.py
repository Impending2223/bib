"""Cuts: the stored marks that give the parts of a calendar entry's line their permanent numbers (rulings 35f, 35g;
notes/proposals/claims-model.md, (c)).

A row of an entry's map, a visibility ruling or a variant that bears on less than the whole line names its words. Until
now it named them by letter, counted from the line's punctuation each time, so the letters shifted when the line was
edited. A cut is a number stored in the line itself, at the end of the words it names: the number stays with its words.

    c: 'Rusk to Dobrynin: the talks will resume on Monday;{1} Moscow will send Zorin.{2}'

STYLE
 1. The mark: `{3}`, a brace, the part's number, a brace, directly after the last character of the part (its full stop
    or semicolon, or the closing quotation mark or bracket after that) and before the space. A calendar line holds no
    other brace.
 2. All or none: a line has no cut, or one at the end of every part, the last included; so a line with cuts ends in
    one. A part is the words between two cuts: a run of whole units (claims.py, STYLE 1).
 3. A number is unique in its entry, never changed and never used again. A new part takes the highest number the entry
    has used, plus one (next_id: the line's numbers and those `cut_from` records). The numbers need not be in order.
 4. When a part is cut in two, both halves take new numbers, and `cut_from` records the old: {'5': '2', '6': '2'}.
 5. In memory the line is plain: store.normalize_entry takes the marks out of a calendar entry's `c` (strip) and keeps
    them as `cuts`, a list of [place, number], the place an offset into the plain line (the mark stood after
    line[:place]). store.stored_form puts them back (insert) and leaves `cuts` out. The rev is of the stored form.
 6. Code that changes a line that has cuts sets the two together (set_line); stored_form refuses cuts that do not fit
    their line (problems), so a line changed alone cannot be written with its marks in the wrong words.
 7. Two kinds of id (35g, 1): a part's is digits, `3`; a claim's, if the calendar takes atomic claims, `a3`. Only parts
    are marked in a line; the grammars that name them (a row, a ruling's `@`, a variant's `unit`) take both (ID).
"""
import re

from . import claims

MARK = re.compile(r"\{(\d+)\}")
ID = r"a?\d+"


def strip(c):
    """(the plain line, [[place, number], ...]) of a stored line."""
    out, cuts, last = [], [], 0
    n = 0
    for m in MARK.finditer(c or ""):
        out.append(c[last:m.start()])
        n += m.start() - last
        cuts.append([n, m.group(1)])
        last = m.end()
    out.append((c or "")[last:])
    return "".join(out), cuts


def insert(c, cuts):
    """The stored line: the plain line with its marks back."""
    out, last = [], 0
    for place, num in sorted(cuts, key=lambda x: x[0]):
        out.append(c[last:place] + "{" + str(num) + "}")
        last = place
    out.append(c[last:])
    return "".join(out)


def unit_ends(c):
    """The offset just past each unit of the plain line, in order."""
    ends, at = [], 0
    for u in claims.units(c):
        i = c.find(u, at)
        if i < 0:
            return None
        at = i + len(u)
        ends.append(at)
    return ends


def problems(c, cuts):
    """What is wrong with a plain line and its cuts (STYLE 1-3), as messages; none where it has no cut."""
    out = []
    if "{" in (c or "") or "}" in (c or ""):
        out.append("a brace in the line that is no cut mark")
    if not cuts:
        return out
    nums = [str(n) for _, n in cuts]
    if any(not re.fullmatch(r"\d+", n) for n in nums):
        out.append("a cut's number is digits")
    if len(set(nums)) != len(nums):
        out.append("a cut's number used twice")
    places = [p for p, _ in cuts]
    if len(set(places)) != len(places):
        out.append("two cuts at one place")
    ends = unit_ends(c)
    if ends is None:
        return out + ["the line's units cannot be found in it"]
    if max(places) != len(c.rstrip()):
        out.append("a line with cuts ends in one")
    bad = [p for p in places if p not in ends]
    if bad:
        out.append("a cut that does not follow the end of a sentence or a semicolon clause (inside a link, italics, "
                   "a quotation or parentheses, or moved from its words): after " +
                   "; ".join(repr(c[max(0, p - 24):p]) for p in sorted(bad)))
    return out


def parts(c, cuts):
    """[(number, [unit indices])] in the line's order; one part, None for its number, where the line has no cut."""
    ends = unit_ends(c) or []
    if not cuts:
        return [(None, list(range(len(ends))))]
    out, lo = [], 0
    for place, num in sorted(cuts, key=lambda x: x[0]):
        hi = next((i for i, e in enumerate(ends) if e == place), None)
        if hi is None:
            return None
        out.append((str(num), list(range(lo, hi + 1))))
        lo = hi + 1
    return out


def units_of(e):
    """number -> the unit indices of the part, for an entry (in memory: `c` plain, `cuts`)."""
    ps = parts(e.get("c") or "", e.get("cuts") or [])
    out = {n: us for n, us in ps or [] if n is not None}
    cf = {str(k): str(v) for k, v in (e.get("cut_from") or {}).items()}
    for _ in range(len(cf)):                       # a number that was cut still resolves, to its halves (STYLE 4)
        for new, old in cf.items():
            if new in out:
                out[old] = sorted(set(out.get(old, [])) | set(out[new]))
    return out


def next_id(e):
    """The number a new part of the entry takes (STYLE 3)."""
    used = [int(n) for _, n in e.get("cuts") or []]
    for new, old in (e.get("cut_from") or {}).items():
        used += [int(new), int(old)]
    return str(max(used, default=0) + 1)


def set_line(e, c, cuts=None):
    """The entry's line and its cuts set together (STYLE 6). `c` plain with `cuts`, or a stored line with its marks."""
    if cuts is None:
        c, cuts = strip(c)
    e["c"] = c
    if cuts:
        e["cuts"] = [[int(p), str(n)] for p, n in cuts]
    else:
        e.pop("cuts", None)
    return e
