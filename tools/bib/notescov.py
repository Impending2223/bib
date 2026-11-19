"""Notes coverage: the pages the calendar cites for a work against the pages its notes are registered for (the
owner, Nov. 16, 2026, approving `notes/proposals/notes-pass.md`: "Approved. Immediate.").

A reader's notes pass (the reader's brief, R3 and R35) registers, for every page it cites, every item of that page's
notes: a row or an edge in `sources/witnesses/by-work/<card>.yaml`, each edge `at:` the page and its note ("107 n.21",
"IV, 228 n.46", "452 Bigart's survey"). This lists the pages cited with no edge at that page.

STYLE
1. A cite is `[[w.CARD]]` in a calendar entry's `n`, and its pinpoint the text after it up to the next `;`, `.` that
   ends a sentence, or `(`: "123", "123–25", "123 n.4", "IV, 228 n.46", "123, 130". Each page of a range counts.
2. An edge's page is the leading number of its `at` (with its volume, a Roman numeral before a comma, where it has
   one). A note's page is the text page it carries, as the reader anchored it.
3. A page cited with no edge is uncovered. Some are right to be (a page whose passage has no note; a work with no
   notes): the reader says so in the book-check file. The audit reads the list; a run whose pages cited have no
   notes registered goes back.
4. The figures: cites, pages cited, pages covered, edges, edges per cite (the proposal's measure).
"""
import glob
import os
import re

from . import store

ROMAN = r"(?:[IVXLC]+)"
PIN = re.compile(rf"^\s*,?\s*(?:({ROMAN}),\s*)?(.*)")
NUM = re.compile(r"(\d+)(?:\s*[–-]\s*(\d+))?")


def _pages(pin):
    """(volume, page) pairs a pinpoint names: '228 n.46' -> [(None, 228)]; 'IV, 228–30' -> IV 228, 229, 230."""
    m = PIN.match(pin)
    vol, rest = m.group(1), m.group(2)
    out = []
    for part in re.split(r",\s*", rest):
        part = re.sub(r"\bn\.\s*\S+", "", part)          # a note number is not a page
        n = NUM.match(part.strip())
        if not n:
            break
        a = int(n.group(1))
        b = n.group(2)
        if b:
            b = int(b)
            if b < a:                                      # '123–25'
                b = int(str(a)[: len(str(a)) - len(str(b))] + str(b))
            out += [(vol, p) for p in range(a, min(b, a + 30) + 1)]
        else:
            out.append((vol, a))
    return out


def cites(card):
    """{(vol, page): [entry ids]} and the number of cites, from the calendar's notes."""
    pat = re.compile(r"\[\[" + re.escape(card) + r"\]\]([^;()]*)")
    pages, n = {}, 0
    for path in sorted(glob.glob(os.path.join(store.ROOT, "lists", "cal", "*.yaml"))):
        data = store.load_yaml(path) or {}
        for e in data.get("entries") or []:
            text = str(e.get("n") or "")
            for m in pat.finditer(text):
                pin = re.split(r"\.\s+[A-Z]", m.group(1))[0]
                n += 1
                for vp in _pages(pin):
                    pages.setdefault(vp, []).append(e.get("id"))
    return pages, n


def edges(card):
    path = os.path.join(store.ROOT, "sources", "witnesses", "by-work", card[2:] + ".yaml")
    rows = store.load_yaml(path) if os.path.exists(path) else []
    covered, count = set(), 0
    for r in rows or []:
        if not isinstance(r, dict) or "at" not in r:
            continue
        count += 1
        for vp in _pages(str(r["at"]))[:1]:
            covered.add(vp)
    return covered, count


def report(card, limit=60):
    if not card.startswith("w."):
        card = "w." + card
    pages, ncites = cites(card)
    covered, nedges = edges(card)
    miss = sorted((vp for vp in pages if vp not in covered), key=lambda vp: (vp[0] or "", vp[1]))
    lines = [f"{card}: {ncites} cites, {len(pages)} pages cited, {len(pages) - len(miss)} with notes registered, "
             f"{nedges} edges, {nedges / ncites if ncites else 0:.2f} edges per cite"]
    if miss:
        lines.append(f"pages cited with no notes registered ({len(miss)}):")
        for vp in miss[:limit]:
            ids = sorted(set(pages[vp]))
            lines.append(f"  {(vp[0] + ', ') if vp[0] else ''}{vp[1]}  " + " ".join(ids[:4]) + (" ..." if len(ids) > 4 else ""))
        if len(miss) > limit:
            lines.append(f"  ... {len(miss) - limit} more (--limit)")
    return "\n".join(lines)
