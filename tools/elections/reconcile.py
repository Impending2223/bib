"""Settle each figure from independent readings of the Clerk's page.

For a race: each candidate's figure read three times (the full-line OCR, and two digits-only OCRs of the
figure, one cropped by page position and one by the figure's own word box),
the district's row of the state's recapitulation table read twice (party columns and total), and
Wikipedia's percentages. A figure is settled when
  - two of the three readings agree and the race's figures sum to the recapitulation total, or
  - exactly one choice among the readings (and recapitulation figures one digit away) sums to that total;
or, failing a total, when two of the three readings agree on every figure and the shares match Wikipedia.
Anything else is left for reading by eye (read.py).
"""
import itertools
import re


def nums(t):
    return [int(x.replace(",", "").replace(" ", "")) for x in re.findall(r"\d{1,3}(?:,\s?\d{3})+|\d+", t or "")]


def near(a, b):
    """Same length, at most one digit different."""
    a, b = str(a), str(b)
    return len(a) == len(b) and sum(x != y for x, y in zip(a, b)) <= 1


def majority(rs):
    rs = [r for r in rs if r is not None]
    for r in rs:
        if rs.count(r) >= 2:
            return r
    return None


def options(rs, row):
    opts = {v for v in rs if v is not None}
    for r in row:
        if any(near(r, v) for v in opts):
            opts.add(r)
    return sorted(opts)


def settle(cands, scat, row, totals, pct_ok):
    """cands: [readings] per candidate (fusion totals already applied); scat: the scattering figure or None;
    row: numbers read in the recapitulation row; totals: its totals as read.
    Returns (values, scattering, how) or None."""
    s0 = scat or 0
    maj = [majority(rs) for rs in cands]
    if all(m is not None for m in maj):
        for T in totals:
            if sum(maj) + s0 == T or sum(maj) == T:
                return maj, scat, "readings agree and sum to the total"
    found = set()
    for T in totals:
        for combo in itertools.product(*[options(rs, row) for rs in cands]):
            if (sum(combo) + s0 == T or sum(combo) == T) and pct_ok(list(combo)):
                found.add(combo)
    if len(found) == 1:
        return list(found.pop()), scat, "sum to the total"
    if all(m is not None for m in maj) and pct_ok(maj):
        return maj, scat, "two of three readings agree; shares match"
    return None
