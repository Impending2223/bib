"""Convert a year's calendar entries from unit letters to stored cuts (rulings 35f, 35g;
notes/proposals/claims-model.md, (f) "The conversion"; tools/bib/cuts.py).

    python3 tools/claims/convert.py 1960            dry run: the counts, proof 1, the lists
    python3 tools/claims/convert.py 1960 --write    the year's files rewritten

STYLE
 1. It touches only an entry in which a stored row (`src`), a visibility ruling (`vis:...@C`) or a variant (`unit: C`)
    names a unit by letter. An entry with none is left as it is: no cut, `all` and `?` as before.
 2. Each pair of neighbouring units is compared. Where the rows, rulings or variants that name the two differ, a cut is
    written between them; and one at the end of the line. The parts are numbered 1, 2, 3 in the line's order.
 3. Letters become numbers: in the rows (`A, C-E` -> `1, 3`), with `all` written out as the numbers and `?` kept; in
    the rulings (`@C-D` -> `@3`, several joined by a dot, `@3.4`); in the variants (`unit: C` -> `unit: '3'`).
 4. Not converted, and listed: an entry whose map is stale (its letters may not fit the line), one whose letters name
    a unit the line does not have, one whose line holds a brace, and one that fails proof 1.
 5. Proof 1, for every entry converted: unit by unit, the same sources (claims.resolve), the same rulings
    (vis.rulings) and the same variants before and after. Proof 2 (the year's pages the same, byte for byte) is made
    by building before and after and comparing the files; this tool does not build.
 6. The map's hash (`src.c`) is of the plain line, as before: a cut holds no words, so the hash does not change.
"""
import collections
import copy
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bib import store, claims, cuts, vis  # noqa: E402

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
    """Per unit: its sources, its rulings, its variants (proof 1)."""
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
    """(the entry converted, None) or (None, why not)."""
    c = e.get("c") or ""
    if "{" in c or "}" in c or e.get("cuts"):
        return None, "a brace in the line, or cuts already"
    src = e.get("src")
    if isinstance(src, dict) and src.get("c") != claims.chash(c):
        return None, "the map is stale"
    us = claims.units(c)
    ends = cuts.unit_ends(c)
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
    cuts.set_line(new, c, ks)
    bad = cuts.problems(new["c"], new["cuts"])
    if bad:
        return None, "; ".join(bad)
    if state(e) != state(new):
        return None, "proof 1 fails: a unit's sources, rulings or variants differ after"
    return new, None


def main():
    year = sys.argv[1]
    write = "--write" in sys.argv
    series = store.Series()
    done, skipped, touched, shown = [], [], set(), []
    n_entries = 0
    for sec, e in claims.calendar(series):
        if str(e.get("date") or "")[:4] != year:
            continue
        n_entries += 1
        if not stored_letters(e):
            continue
        new, why = convert(e)
        if new is None:
            skipped.append((e["id"], why))
            continue
        done.append((e["id"], len(new["cuts"])))
        if len(shown) < 4 and len(new["cuts"]) > 1 and len(done) % 97 == 1:
            shown.append((store.stored_form(e), store.stored_form(new)))
        if write:
            i = next(k for k, x in enumerate(sec.entries) if x is e)
            sec.entries[i] = store.normalize_entry(store.stored_form(new))
            touched.add(sec)
    if write:
        for sec in touched:
            series.save_section(sec)
    out = os.path.join(ROOT, "notes", "claims", f"convert-{year}.tsv")
    with open(out, "w", encoding="utf-8") as f:
        f.write("id\twhat\tdetail\n")
        for eid, k in done:
            f.write(f"{eid}\tconverted\t{k} parts\n")
        for eid, why in skipped:
            f.write(f"{eid}\tnot converted\t{why}\n")
    print(f"{year}: {n_entries} entries; {len(done)} converted ({sum(k for _, k in done)} parts); "
          f"{len(skipped)} not converted" + ("; written" if write else "; dry run"))
    for why, k in collections.Counter(w for _, w in skipped).most_common():
        print(f"  not converted, {k}: {why}")
    return shown


if __name__ == "__main__":
    for old, new in main() or []:
        print("\n" + store._emit([{k: old[k] for k in ("id", "c", "src", "tags", "variants") if k in old}], 0))
        print(store._emit([{k: new[k] for k in ("id", "c", "src", "tags", "variants") if k in new}], 0))
