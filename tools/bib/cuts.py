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
 8. The conversion (convert; tools/claims/convert.py runs it a year at a time, and the merge runs it on an entry whose
    map is seeded as an op names a part): where a stored row, a ruling or a variant names units by letter, a cut is
    written wherever the things that name two neighbouring units differ, and at the line's end; the parts are
    numbered 1, 2, 3 in order; the letters become numbers, `all` written out as the numbers. It is refused, and the
    entry left, where the map is stale, a letter is not the line's, or any unit's sources, rulings or variants would
    differ after.
 9. A patch names a part by its words, never by its number (`on:`; addops.py, STYLE 9): the words from the part's
    first to its last, as the line has them, or the first and the last words with three dots between. They are in
    the line once; they begin where a sentence or a semicolon clause begins and end where one ends. The merge finds
    them in the line as it then stands (locate), readies the entry (ensure), and cuts where it must (name).
10. `add-words` puts new words into the line as a part of their own (add_words), with their own source: no earlier
    source is made to support them, and two readers adding to one entry do not conflict.
11. R22 from the difference (edit_problems; patch-check): an `edit` that only adds sentences or clauses states
    nothing. One that changes or removes words already in the line states `kind: reword` (no number, no date and no
    tagged person's name changes) or `kind: correct` (the same edit adds to the note the sentence that names the
    settling record). The comparison is unit by unit: a sentence or clause found word for word in the new line is
    unchanged.
 7. Two kinds of id (35g, 1): a part's is digits, `3`; a claim's, if the calendar takes atomic claims, `a3`. Only parts
    are marked in a line; the grammars that name them (a row, a ruling's `@`, a variant's `unit`) take both (ID).
"""
import collections
import copy
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


# ---------------------------------------------------------------- naming a part by its words (the patch ops)

def unit_spans(c):
    """(start, end) of each unit in the plain line."""
    out, at = [], 0
    for u in claims.units(c):
        i = c.find(u, at)
        if i < 0:
            return None
        at = i + len(u)
        out.append((i, at))
    return out


def _all(c, words):
    out, i = [], c.find(words)
    while i >= 0:
        out.append(i)
        i = c.find(words, i + 1)
    return out


def locate(c, on):
    """The units a patch's `on:` names (STYLE 9): ((first index, last index), None) or (None, why not)."""
    on = " ".join(str(on or "").split())
    spans = unit_spans(c)
    if not on or spans is None:
        return None, "no words given" if not on else "the line's units cannot be found in it"
    hits = [(i, i + len(on)) for i in _all(c, on)]
    m = re.fullmatch(r"(.+?) ?(?:…|\.\.\.) ?(.+)", on)
    if not hits and m:                               # a long part by its first and last words
        a, b = m.group(1).strip(), m.group(2).strip()
        starts, ends = _all(c, a), [i + len(b) for i in _all(c, b)]
        if len(starts) > 1 or len(ends) > 1:
            return None, "the first or the last words are in the line more than once: quote more"
        hits = [(s, e) for s in starts for e in ends if e >= s + len(a)]
    if not hits:
        return None, "the words are not in the line"
    if len(hits) > 1:
        return None, "the words are in the line more than once: quote more"
    s, e = hits[0]
    i = next((k for k, (a, _) in enumerate(spans) if a == s), None)
    j = next((k for k, (_, b) in enumerate(spans) if b == e), None)
    if i is None:
        return None, "the words do not begin where a sentence or a semicolon clause begins"
    if j is None:
        return None, "the words do not end where a sentence or a semicolon clause ends"
    return (i, j), None


def _tokens(spec, sep):
    return [x for x in str(spec).split(sep) if x]


def rename(e, old, news):
    """Every row, ruling and variant of the entry that names part `old` names `news` (STYLE 4)."""
    def swap(tokens):
        out = []
        for x in tokens:
            for y in (news if x == old else [x]):
                if y not in out:
                    out.append(y)
        return out
    src = e.get("src")
    if isinstance(src, dict):
        rows = []
        for r in src.get("rows") or []:
            key, _, spec = r.rpartition(": ")
            if key and claims.NUMBERED.match(spec):
                r = f"{key}: {', '.join(swap(_tokens(spec, ', ')))}"
            if r not in rows:
                rows.append(r)
        src["rows"] = rows
    if e.get("tags"):
        tags = []
        for t in e["tags"]:
            m = re.match(r"^(vis:.*)@(\d+(?:\.\d+)*)$", str(t))
            tags.append(f"{m.group(1)}@{'.'.join(swap(_tokens(m.group(2), '.')))}" if m else t)
        e["tags"] = tags
    for v in e.get("variants") or []:
        if isinstance(v, dict) and re.fullmatch(r"\d+(?:\.\d+)*", str(v.get("unit") or "")):
            v["unit"] = ".".join(swap(_tokens(v["unit"], ".")))


def every(e):
    """The numbers of all the line's parts, in its order."""
    return [str(n) for _, n in sorted(e.get("cuts") or [], key=lambda x: x[0])]


def ensure(e):
    """The entry ready for a part to be named (STYLE 9): its map stored (seeded where it had none), its letters
    converted, and a line with no cut given one at its end, every `all` then that number, so that the old sources
    stay with the old words. (a new entry, None) or (None, why not)."""
    new = copy.deepcopy(e)
    c = new.get("c") or ""
    if not isinstance(new.get("src"), dict):
        new["src"] = claims.mechanical(new) or {"c": claims.chash(c), "rows": []}
    if new["src"].get("c") != claims.chash(c):
        return None, "the entry's map is stale (made against an earlier line): map it again before naming a part"
    if stored_letters(new):
        new, why = convert(new)
        if new is None:
            return None, f"the entry's letters cannot be converted ({why})"
    if not new.get("cuts"):
        ends = unit_ends(c)
        if not ends or ends[-1] != len(c.rstrip()) or "{" in c or "}" in c:
            return None, "the line's units cannot be found in it"
        set_line(new, c, [[ends[-1], next_id(new)]])
    nums = ", ".join(every(new))
    new["src"]["rows"] = [f"{r[:-5]}: {nums}" if r.endswith(": all") else r for r in new["src"].get("rows") or []]
    return new, None


def name(e, i, j):
    """(a new entry, the numbers of the parts that are units i..j), a part that straddles either end cut there:
    its pieces take new numbers, `cut_from` records the old, and what named it names the pieces (STYLE 4)."""
    new = copy.deepcopy(e)
    ends = unit_ends(new["c"])
    out = []
    for num, idx in parts(new["c"], new["cuts"]) or []:
        inside = [k for k in idx if i <= k <= j]
        if not inside:
            continue
        if len(inside) == len(idx):
            out.append(num)
            continue
        groups = [g for g in ([k for k in idx if k < i], inside, [k for k in idx if k > j]) if g]
        nums = []
        for g in groups:
            n = next_id(new)
            nums.append(n)
            new.setdefault("cut_from", {})[n] = num
            new["cuts"].append([ends[g[-1]], n])
            if g is inside:
                out.append(n)
        new["cuts"] = [x for x in new["cuts"] if x[1] != num]
        rename(new, num, nums)
    new["cuts"].sort(key=lambda x: x[0])
    return new, out


def part_for(e, on):
    """(a new entry, the numbers the words name, None) or (None, None, why not): ensure, locate, name."""
    new, why = ensure(e)
    if new is None:
        return None, None, why
    hit, why = locate(new["c"], on)
    if hit is None:
        return None, None, why
    new, nums = name(new, *hit)
    return new, nums, None


def add_words(e, after, words):
    """(a new entry, the new part's number, None) or (None, None, why not): the words put into the line after the
    place named (`end`, or words of the line that end a sentence or a semicolon clause), a part of their own; no
    earlier source is made to support them (STYLE 10)."""
    words = " ".join(str(words or "").split())
    if not words:
        return None, None, "no words given"
    new, why = ensure(e)
    if new is None:
        return None, None, why
    c = new["c"]
    us = claims.units(c)
    if str(after).strip() == "end":
        k = len(us) - 1
    else:
        hit, why = locate(c, after)
        if hit is None:
            return None, None, f"after: {why}"
        k = hit[1]
    first = next(idx[0] for _, idx in parts(c, new["cuts"]) if k in idx)
    new, _ = name(new, first, k)                    # the part that holds the place ends there now
    pos = unit_ends(c)[k]
    c2 = c[:pos] + " " + words + c[pos:]
    if list(claims.units(c2)) != us[:k + 1] + list(claims.units(words)) + us[k + 1:]:
        return None, None, "the words are not whole sentences or semicolon clauses where they are put"
    n = next_id(new)
    ks = [[p + (len(words) + 1 if p > pos else 0), x] for p, x in new["cuts"]] + [[pos + 1 + len(words), n]]
    set_line(new, c2, sorted(ks, key=lambda x: x[0]))
    new["src"]["c"] = claims.chash(c2)
    bad = problems(new["c"], new["cuts"])
    if bad:
        return None, None, "; ".join(bad)
    return new, n, None


def carry(old_c, old_cuts, new_c):
    """An old line's cuts placed in a new plain line (an `edit` whose line has no marks): each after the same words,
    where the sentence or clause it followed stands unchanged, and once. (the cuts, the numbers not placed)."""
    olds, oe = claims.units(old_c), unit_ends(old_c) or []
    news, ne = claims.units(new_c), unit_ends(new_c) or []
    out, lost = [], []
    for place, num in old_cuts:
        text = olds[oe.index(place)] if place in oe else None
        hits = [k for k, u in enumerate(news) if u == text]
        if len(hits) == 1 and len(ne) == len(news):
            out.append([ne[hits[0]], num])
        else:
            lost.append(num)
    return sorted(out, key=lambda x: x[0]), lost


# ---------------------------------------------------------------- R22 from the difference (patch-check)

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec")


def _facts(texts, names):
    """The numbers, the months and the tagged persons' names in some units: what a rewording may not change."""
    s = " ".join(texts)
    out = collections.Counter(re.findall(r"\d[\d,.:]*\d|\d", s))
    out.update(m for m in re.findall(r"[A-Z][a-z]+", s) if m.rstrip(".") in MONTHS or m in names)
    return out


def edit_problems(old, new_line, body, names=()):
    """What an `edit` that changes a calendar line must state (R22; STYLE 11), as messages. `old`: the entry the edit
    was made against; `new_line`: its new `c` as the patch writes it; `body`: the op; `names`: the surnames of the
    persons the entry tags."""
    new_c = strip(new_line)[0]
    olds, news = claims.units(old.get("c") or ""), claims.units(new_c)
    if olds == news:
        return []
    kept = [u for u in olds if u in news]
    was = [u for u in olds if u not in news]              # units changed or removed
    now = [u for u in news if u not in olds]              # units changed or new
    if not was:
        return []                                         # only new words: an addition (R33a), free
    kind = body.get("kind")
    if kind not in ("reword", "correct"):
        return ["the edit changes words already in the line: state kind: reword (the same facts in other words) or "
                "kind: correct (a record settles it; R22). New words alone need neither: add them with add-words"]
    if kind == "reword":
        a, b = _facts(was, names), _facts(now, names)
        if a != b:
            diff = sorted(set((a - b) + (b - a)))
            return [f"kind: reword, but a number, a date or a tagged person's name changes ({', '.join(diff)[:120]}): "
                    "that is kind: correct, with the sentence in the note that names the settling record (R22)"]
        return []
    n = (body.get("set") or {}).get("n")
    if not isinstance(n, str) or n.strip() == (old.get("n") or "").strip():
        return ["kind: correct: the same edit adds to the note the sentence that names the settling record "
                "(\"The Papers date it Aug. 26.\"; R22)"]
    return []


# ---------------------------------------------------------------- from letters to cuts (tools/claims/convert.py)

LETTER_SPEC = re.compile(r"^[A-Z]{1,2}(?:-[A-Z]{1,2})?(?:, [A-Z]{1,2}(?:-[A-Z]{1,2})?)*$")
RULE_AT = re.compile(r"^(vis:.*)@([A-Z.-]+)$")


def stored_letters(e):
    """What in the entry names units by letter: ('row', i, spec), ('rule', i, spec), ('variant', i, letter)."""
    out = []
    for i, r in enumerate((e.get("src") or {}).get("rows") or []):
        p = claims.parse_row(r)
        if p and LETTER_SPEC.match(p[4]):
            out.append(("row", i, p[4]))
    for i, t in enumerate(e.get("tags") or []):
        m = RULE_AT.match(str(t))
        if m:
            out.append(("rule", i, m.group(2)))
    for i, v in enumerate(e.get("variants") or []):
        if isinstance(v, dict) and re.fullmatch(r"[A-Z]{1,2}", str(v.get("unit") or "")):
            out.append(("variant", i, str(v["unit"])))
    return out


def state(e):
    """Per unit: its sources, its rulings, its variants (the conversion's proof 1)."""
    from . import vis
    us = claims.units(e.get("c") or "")
    rows = claims.resolve(e)
    rules = vis.rulings(e)
    out = []
    for i in range(len(us)):
        L = claims.LETTERS[i]
        srcs = sorted((r.rsplit(": ", 1)[0], "?" if u == "?" else "") for r, k, key, pin, note, u, item in rows
                      if u == "?" or (u is not None and L in u))
        rl = sorted((r["kind"], tuple(sorted(r["pols"])), r["date"] or "") for r in rules
                    if r["units"] is None or L in r["units"])
        vs = sorted((str(v.get("witness")), str(v.get("reads")), str(v.get("at"))) for v in e.get("variants") or []
                    if isinstance(v, dict) and v.get("unit") is not None and L in (claims.named_letters(e, v["unit"]) or ()))
        out.append((srcs, rl, vs))
    return out


def convert(e):
    from . import vis
    """(the entry converted, None) or (None, why not)."""
    c = e.get("c") or ""
    if "{" in c or "}" in c or e.get("cuts"):
        return None, "a brace in the line, or cuts already"
    src = e.get("src")
    if isinstance(src, dict) and src.get("c") != claims.chash(c):
        return None, "the map is stale"
    us = claims.units(c)
    ends = unit_ends(c)
    n = len(us)
    if not n or ends is None or ends[-1] != len(c.rstrip()):
        return None, "the line's units cannot be found in it"
    L = claims.LETTERS
    names = collections.defaultdict(set)            # unit index -> what names it
    sets = {}
    for kind, i, spec in stored_letters(e):
        u = vis._units(spec) if kind == "rule" else claims.parse_units(spec, n) if kind == "row" else {spec}
        if u is None or not u <= set(L[:n]):
            return None, f"{kind} {spec}: a letter the line does not have"
        sets[(kind, i)] = {L.index(x) for x in u}
        for k in sets[(kind, i)]:
            names[k].add((kind, i))
    new = copy.deepcopy(e)
    ks, part_of, num = [], {}, 0
    for k in range(n):
        if k == n - 1 or names[k] != names[k + 1]:
            num += 1
            ks.append([ends[k], str(num)])
        part_of[k] = num if (k == n - 1 or names[k] != names[k + 1]) else None
    cur = num
    for k in range(n - 1, -1, -1):                  # each unit's part: the next cut at or after it
        if part_of[k] is None:
            part_of[k] = cur
        else:
            cur = part_of[k]
    every = ", ".join(str(i) for i in range(1, num + 1))

    def nums(idx, sep):
        return sep.join(str(p) for p in sorted({part_of[k] for k in idx}))
    rows = list(new["src"]["rows"]) if isinstance(new.get("src"), dict) else []
    for i, r in enumerate(rows):
        p = claims.parse_row(r)
        if p is None:
            continue
        key = r.rsplit(": ", 1)[0]
        if p[4] == "all":
            rows[i] = f"{key}: {every}"
        elif ("row", i) in sets:
            rows[i] = f"{key}: {nums(sets[('row', i)], ', ')}"
    if rows:
        seen = []
        for r in rows:
            if r not in seen:
                seen.append(r)
        new["src"]["rows"] = seen
    for (kind, i), idx in sets.items():
        if kind == "rule":
            m = RULE_AT.match(str(new["tags"][i]))
            new["tags"][i] = f"{m.group(1)}@{nums(idx, '.')}"
        elif kind == "variant":
            new["variants"][i]["unit"] = nums(idx, ".")
    set_line(new, c, ks)
    bad = problems(new["c"], new["cuts"])
    if bad:
        return None, "; ".join(bad)
    if state(e) != state(new):
        return None, "proof 1 fails: a unit's sources, rulings or variants differ after"
    return new, None
