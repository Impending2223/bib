"""Rebase the stale claim maps (notes/proposals/claims-model.md, (f) 2; ruling 35f).

A reader's map (`src`) records the hash of the line (`c`) it was made against. Where the line has changed since, the
map's letters may name other units, and the build shows the entry as one block. This tool finds, in git history, the
line each stale map was made against, matches its units to the present units by their text, and rewrites the rows.

    python3 tools/claims/rebase_stale.py            dry run: the counts, and the report written
    python3 tools/claims/rebase_stale.py --write    the maps rewritten in lists/cal, and the report

STYLE
 1. The old line: every `c:` line git history holds under lists/ (added, removed or context, in `git log -p`), hashed
    as claims.chash hashes it. A stale map whose hash matches none is not touched; it is listed ("no old line").
    A map that recorded no hash (written whole by an `add` or an `edit`; an additive op always writes one): the
    line the entry had in the commit that wrote the map's `rows:` line (`git blame`). Where blame stops at the
    edge of the history fetched, the old line is not known ("no old line"). The same for a map whose hash matches
    no line in history (a reader hashed a draft, and the audit changed the line before the merge), where its rows
    name no letters: `all` and `?` do not depend on the lettering, and the map was merged with that line. Where
    such a map names letters, the line they were counted on is lost: it is not touched, and is listed.
 2. Matching: the old units and the present units, in order (difflib on the two lists). An old unit found word for
    word is "the same". Of the rest, an old and a present unit in the same gap whose texts are alike (ratio at least
    RATIO) are "changed": the row keeps the unit, and the entry is listed for a reader. A present unit matched to no
    old unit is new: no row takes it. An old unit matched to no present unit is gone.
 3. A row's letters become the present letters of the old units it named. `all` stays `all` where no present unit is
    new, and otherwise becomes those letters. `?` stays. Where a row's units are all gone, or it names letters the
    old line never had, the map is not rewritten ("lost"): it stays stale, and the entry is listed for a reader.
 4. Variants (`unit:`) and visibility rulings (`@C`) also name letters, and record no hash: which line they were
    made against is not known. They are not changed. An entry that has one, and whose units moved, is listed.
 5. The new hash is written. The report: notes/claims/stale-rebase.md (the counts and the lists) and
    notes/claims/stale-rebase.tsv (a row an entry: id, what was done, the old letters -> the new).
"""
import collections
import difflib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bib import store, claims  # noqa: E402

RATIO = 0.6
C_LINE = re.compile(r"^[-+ ]    c: (.*)$")


def old_lines(want):
    """hash -> line, for the hashes wanted, from every `c:` line in the history of lists/ (STYLE 1)."""
    found = {}
    p = subprocess.Popen(["git", "log", "-p", "-U0", "--format=", "--", "lists"], cwd=ROOT, stdout=subprocess.PIPE,
                         text=True, encoding="utf-8", errors="replace")
    for line in p.stdout:
        m = C_LINE.match(line)
        if not m:
            continue
        try:
            c = store.yaml.safe_load("c: " + m.group(1))["c"]
        except Exception:
            continue
        if not isinstance(c, str):
            continue
        h = claims.chash(c)
        if h in want and h not in found:
            found[h] = c
            if len(found) == len(want):
                p.kill()
                break
    return found


def names_letters(e):
    return any((claims.parse_row(r) or (None,) * 5)[4] not in (None, "all", "?") for r in e["src"]["rows"])


def blamed_lines(stale, found):
    """id -> the line the entry had when its map was written, for a map with no hash, or with a hash history does
    not hold and no letters (STYLE 1)."""
    out, shown = {}, {}
    by_file = collections.defaultdict(list)
    for sec, e in stale:
        h = e["src"].get("c")
        if not h or (h not in found and not names_letters(e)):
            by_file[os.path.join("lists", sec.lst.key, sec.file)].append(e["id"])
    for path, ids in by_file.items():
        text = open(os.path.join(ROOT, path), encoding="utf-8").read().split("\n")
        at = {m.group(1): i for i, ln in enumerate(text) for m in [re.match(r"^  - id: (\S+)$", ln)] if m}
        for eid in ids:
            i = at.get(eid)
            if i is None:
                continue
            j = next((k for k in range(i + 1, len(text)) if text[k].startswith("  - id: ") or text[k] == "      rows:"), None)
            if j is None or text[j] != "      rows:":
                continue
            b = subprocess.run(["git", "blame", "-L", f"{j + 1},{j + 1}", "--porcelain", "--", path], cwd=ROOT,
                               capture_output=True, text=True).stdout.split("\n")
            if not b or not b[0] or any(x == "boundary" for x in b):
                continue
            sha = b[0].split()[0]
            name = next((x[9:] for x in b if x.startswith("filename ")), path)
            if (sha, name) not in shown:
                shown[(sha, name)] = subprocess.run(["git", "show", f"{sha}:{name}"], cwd=ROOT, capture_output=True,
                                                    text=True).stdout
            m = re.search(r"^  - id: " + re.escape(eid) + r"\n(?:    .*\n|      .*\n)*?    c: (.*)$", shown[(sha, name)], re.M)
            if not m:
                continue
            try:
                c = store.yaml.safe_load("c: " + m.group(1))["c"]
            except Exception:
                continue
            if isinstance(c, str):
                out[eid] = c
    return out


def match(old, new):
    """(same, changed, fresh, gone): old index -> new index for the units the same and the units changed; the new
    indices matched to nothing; the old indices matched to nothing (STYLE 2)."""
    same, changed = {}, {}
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                same[i1 + k] = j1 + k
        elif tag == "replace":
            j = j1
            for i in range(i1, i2):                      # in order: each old unit takes the first present unit like it
                for jj in range(j, j2):
                    if difflib.SequenceMatcher(None, old[i], new[jj], autojunk=False).ratio() >= RATIO:
                        changed[i] = jj
                        j = jj + 1
                        break
    took = set(same.values()) | set(changed.values())
    fresh = [j for j in range(len(new)) if j not in took]
    gone = [i for i in range(len(old)) if i not in same and i not in changed]
    return same, changed, fresh, gone


def spec_of(idx, n):
    """Indices -> 'A, C-E' (claims STYLE 2)."""
    idx = sorted(idx)
    L = claims.LETTERS
    out, k = [], 0
    while k < len(idx):
        m = k
        while m + 1 < len(idx) and idx[m + 1] == idx[m] + 1:
            m += 1
        out.append(L[idx[k]] if m == k else f"{L[idx[k]]}-{L[idx[m]]}")
        k = m + 1
    return ", ".join(out)


def rebase(e, old_c):
    """(new src, kind, detail) for a stale entry, its old line known."""
    old, new = claims.units(old_c), claims.units(e.get("c") or "")
    same, changed, fresh, gone = match(old, new)
    to = dict(same)
    to.update(changed)
    rows, lost, detail = [], False, []
    for r in e["src"]["rows"]:
        p = claims.parse_row(r)
        if p is None:
            rows.append(r)
            continue
        key, spec = r.rsplit(": ", 1)
        if spec == "?":
            rows.append(r)
            continue
        if spec == "all":
            if not fresh:
                rows.append(r)
                continue
            was = set(range(len(old)))
        else:
            u = claims.parse_units(spec, len(old))
            if u is None or not u <= set(claims.letters(len(old))):
                rows.append(r)                               # letters the old line never had: left, and listed
                lost = True
                detail.append(f"{spec} not in the old line")
                continue
            was = {claims.LETTERS.index(x) for x in u}
        now = {to[i] for i in was if i in to}
        if not now:
            rows.append(f"{key}: ?")
            lost = True
            detail.append(f"{spec} -> ? (its units are gone)")
            continue
        ns = spec_of(now, len(new))
        if ns != spec:
            detail.append(f"{spec} -> {ns}")
        rows.append(f"{key}: {ns}")
    seen, uniq = set(), []
    for r in rows:
        if r not in seen:
            seen.add(r)
            uniq.append(r)
    kind = "lost" if lost else "changed" if changed else "moved" if (fresh or gone or detail) else "same"
    if changed:
        detail.append("words changed in " + spec_of(set(changed.values()), len(new)))
    if fresh:
        detail.append("new: " + spec_of(fresh, len(new)))
    if gone:
        detail.append("gone (old letters): " + spec_of(gone, len(old)))
    return {"c": claims.chash(e.get("c")), "rows": uniq}, kind, "; ".join(detail)


def lettered_elsewhere(e):
    """An entry with a variant's `unit` or a visibility ruling's `@` letters (STYLE 4)."""
    if any(v.get("unit") for v in e.get("variants") or [] if isinstance(v, dict)):
        return True
    return any(re.search(r"^vis:.*@[A-Z]", str(t)) for t in e.get("tags") or [])


def main():
    write = "--write" in sys.argv
    series = store.Series()
    stale = [(sec, e) for sec, e in claims.calendar(series)
             if isinstance(e.get("src"), dict) and e["src"].get("c") != claims.chash(e.get("c"))]
    want = {e["src"].get("c") for _, e in stale}
    found = old_lines(want - {None})
    blamed = blamed_lines(stale, found)
    rows, counts, touched = [], collections.Counter(), set()
    for sec, e in stale:
        old_c = found.get(e["src"].get("c")) or blamed.get(e["id"])
        if old_c is None:
            counts["no old line"] += 1
            rows.append((e["id"], "no old line", ""))
            continue
        new_src, kind, detail = rebase(e, old_c)
        if kind != "same" and lettered_elsewhere(e):
            detail = (detail + "; " if detail else "") + "has a variant or a visibility ruling that names letters"
            counts["with a variant or ruling"] += 1
        counts[kind] += 1
        rows.append((e["id"], kind, detail))
        if write and kind != "lost":                     # a map with a row that cannot be carried over is left stale
            e["src"] = new_src
            touched.add(sec)
    if write:
        for sec in touched:
            series.save_section(sec)
    os.makedirs(os.path.join(ROOT, "notes", "claims"), exist_ok=True)
    with open(os.path.join(ROOT, "notes", "claims", "stale-rebase.tsv"), "w", encoding="utf-8") as f:
        f.write("id\twhat\tdetail\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    print(f"stale maps: {len(stale)}; " + "; ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
    return rows, counts


if __name__ == "__main__":
    main()
