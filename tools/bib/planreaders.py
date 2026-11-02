"""Readers planned by overlap (the owner's request, Oct. 30, 2026; notes/extensions/memos/volume.md, §6, item 5).

    ./bib plan-readers w.card [w.card ...] [--min N]

For each pair of works: the calendar entries both already cite (read or behind "To check:"). Works that share at
least N entries (default 10) and three in ten of the smaller's go to one reader, in order of their first dates, so that its later patches build
on its earlier (R49 of notes/briefs/reader.md); the groups run at once. A work the calendar does not cite yet stands
alone. The bar is high on purpose: the additive ops (tools/bib/addops.py) let two readers cite one entry without a
conflict, and the ledger (tools/bib/ledger.py) keeps them from adding one event twice, so overlap costs little; only
works that cover much the same ground are worth reading in sequence.

STYLE
 1. Read only from the tree: no copy of a book is opened. The overlap is a forecast from what is already cited; a new
    book's own reach shows only once it is read.
 2. The groups are joined transitively (a with b, b with c: one group); a group too large for one reader is the
    owner's call, printed with its size.
"""
import collections
import re


def entries_of(series, cards):
    """card -> set of calendar ids citing it (its aliases too), and card -> (first, last) date."""
    alias = {}
    for c in cards:
        w = series.works.get(c)
        keys = {c}
        if w:
            keys |= set(w.get("aliases") or []) | {w.get("id") or c}
        for k in keys:
            alias[k] = c
    pat = re.compile(r"\[\[(w\.[^\]|]+)")
    hits = collections.defaultdict(set)
    span = {}
    lst = series.lists.get("cal")
    for _, e in lst.entries() if lst else []:
        for m in pat.finditer(e.get("n") or ""):
            c = alias.get(m.group(1).strip())
            if c:
                hits[c].add(e["id"])
                d = str(e.get("date") or "")
                if d:
                    a, b = span.get(c, (d, d))
                    span[c] = (min(a, d), max(b, d))
    return hits, span


def plan(series, cards, minimum=10):
    hits, span = entries_of(series, cards)
    parent = {c: c for c in cards}

    def root(c):
        while parent[c] != c:
            parent[c] = parent[parent[c]]
            c = parent[c]
        return c
    pairs = []
    for i, a in enumerate(cards):
        for b in cards[i + 1:]:
            shared = len(hits[a] & hits[b])
            small = min(len(hits[a]), len(hits[b])) or 1
            if shared:
                pairs.append((shared, a, b))
            if shared >= minimum and shared >= 0.3 * small:
                parent[root(a)] = root(b)
    groups = collections.defaultdict(list)
    for c in cards:
        groups[root(c)].append(c)
    out = []
    for g in groups.values():
        g.sort(key=lambda c: span.get(c, ("9999",))[0])
        out.append(g)
    out.sort(key=lambda g: (-len(g), span.get(g[0], ("9999",))[0]))
    return out, sorted(pairs, reverse=True), hits, span


def report(series, cards, minimum=10):
    groups, pairs, hits, span = plan(series, cards, minimum)
    lines = [f"== {len(groups)} readers for {len(cards)} works (shared entries >= {minimum} and three in ten of the smaller's)"]
    for k, g in enumerate(groups, 1):
        lines.append(f"  reader {k}: " + " -> ".join(
            f"{c} ({len(hits[c])}; {span[c][0]}..{span[c][1]})" if c in span else f"{c} (0)" for c in g))
    lines.append("== the largest overlaps")
    lines += [f"  {n:4} {a} & {b}" for n, a, b in pairs[:15]]
    return "\n".join(lines)
