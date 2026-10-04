"""Pair Wikipedia's candidates with the Clerk's vote lines, and check the shares.

For each state, the Clerk's lines in printed order are walked alongside Wikipedia's races in the
Clerk's order (the Senate first, then the districts). A candidate takes the first unused line at or
after the cursor whose name has the candidate's surname. A fusion line (a party line with no name)
belongs to the candidate above it; the race's other named lines are minor candidates the
Clerk prints and Wikipedia omits; a Scattering line closes the race.
"""
import difflib
import re
import unicodedata

SUF = {"jr", "jr.", "sr", "sr.", "ii", "iii", "iv"}


def fold(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z ]", " ", t.lower())


def surname(name):
    w = [x for x in fold(re.sub(r"\(.*?\)", "", name)).split() if x not in {"jr", "sr", "ii", "iii", "iv"}]
    return w[-1] if w else ""


def same(a, b):
    """Does Clerk line name a carry Wikipedia name b's surname (OCR-tolerant)?"""
    if not a:
        return False
    s = surname(b)
    words = fold(a).split()
    return any(w == s or (len(s) > 3 and difflib.SequenceMatcher(None, w, s).ratio() >= 0.8) for w in words)


def exact(a, b):
    s = surname(b)
    return bool(a) and s in fold(a).split()


def find(lines, used, cur, name, back=8, ahead=30):
    """The line for a candidate: an exact surname near the cursor, then a near spelling near it,
    then an exact surname anywhere after it."""
    ok = lambda i: i not in used and lines[i].get("name") and lines[i]["name"] != "Scattering"
    text = lambda i: re.split(r"[_.]{3,}|-{3,}", lines[i]["raw"])[0]    # the line up to its leader dots
    near = sorted(range(max(0, cur - back), min(len(lines), cur + ahead)), key=lambda i: (abs(i - cur), i < cur))
    for test in (exact, same):
        for i in near:
            if ok(i) and test(text(i), name):
                return i
    for i in list(range(cur + ahead, len(lines))) + list(range(max(0, cur - back) - 1, -1, -1)):
        if ok(i) and exact(text(i), name):
            return i
    return None


def later_names(races, k):
    return [c["name"] for r in races[k + 1:] for c in r["candidates"]]


def align(races, lines):
    """races: Wikipedia races of one state in Clerk order. lines: the Clerk's parsed lines for the state.
    Returns each race with 'clerk': [{name, parties:[...], votes, lines:[...]}] and 'scattering'."""
    used, cur = set(), 0
    for k, race in enumerate(races):
        race["clerk"], race["scattering"], race["span"] = [], None, []
        first = last = None
        start = cur
        for c in race["candidates"]:
            hit = find(lines, used, start, c["name"])
            if hit is None:
                c["clerk"] = None
                continue
            used.add(hit)
            ent = {"name": lines[hit]["name"], "parties": [lines[hit]["party"]], "votes": lines[hit]["votes"], "lines": [hit]}
            j = hit + 1
            while j < len(lines) and lines[j].get("name") is None and j not in used:
                used.add(j)
                ent["parties"].append(lines[j]["party"])
                ent["fusion"] = ent.get("fusion", []) + [lines[j]["votes"]]
                ent["lines"].append(j)
                j += 1
            c["clerk"] = ent
            first = hit if first is None else min(first, hit)
            last = max(last or hit, ent["lines"][-1])
            cur = max(cur, ent["lines"][-1] + 1)
        if first is None:
            continue
        # minor candidates and scattering printed inside or just after the race
        j = first
        while j < len(lines):
            if j in used:
                j += 1
                continue
            ln = lines[j]
            if j > last:
                if ln.get("name") == "Scattering":
                    race["scattering"] = ln["votes"]
                    used.add(j)
                    last = j
                    j += 1
                    continue
                # a named line after the race that names no later candidate: a minor candidate here
                if race.get("chamber") == "s" and ln.get("name") and race["scattering"] is None and not any(same(ln["raw"], n) for n in later_names(races, k)):
                    race.setdefault("minor", []).append({"name": ln["name"], "parties": [ln["party"]], "votes": ln["votes"], "lines": [j]})
                    used.add(j)
                    last = j
                    j += 1
                    continue
                break
            if ln.get("name") == "Scattering":
                race["scattering"] = ln["votes"]
            elif ln.get("name"):
                race.setdefault("minor", []).append({"name": ln["name"], "parties": [ln["party"]], "votes": ln["votes"], "lines": [j]})
            used.add(j)
            j += 1
        race["span"] = [first, last]
        cur = max(cur, last + 1)
    return races


def totals(c):
    """A candidate's total: with fusion lines, the last line's number is the bracketed total when it
    exceeds the first line's votes; otherwise the lines are summed."""
    e = c["clerk"]
    if not e:
        return None
    if e.get("fusion"):
        t = e["fusion"][-1]
        return t if t > e["votes"] else e["votes"] + sum(e["fusion"])
    return e["votes"]


def check(race, tol=0.16):
    """Shares computed from the Clerk against Wikipedia's percentages, with and without scattering."""
    vs = [totals(c) for c in race["candidates"]]
    if any(v is None for v in vs):
        return False, "candidate not found in the Clerk"
    minor = sum(m["votes"] for m in race.get("minor", []))
    base = sum(vs) + minor
    ok_any = False
    for tot in (base, base + (race.get("scattering") or 0)):
        if not tot:
            continue
        good = all(c["pct"] is None or abs(100 * v / tot - c["pct"]) <= tol for c, v in zip(race["candidates"], vs))
        ok_any = ok_any or good
    if all(c["pct"] is None for c in race["candidates"]):
        return True, "unopposed"
    return ok_any, ("ok" if ok_any else "shares differ from Wikipedia")
