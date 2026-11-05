"""Write `Hearing CHRG-...` into the `src` of each Executive roster holder whose printed nomination hearing
tools/bib/hearings.py finds (its RULES 2; STYLE 2). Rerunnable: a source already there is left; nothing else in the
files changes (a line inserted into a block list, or the item appended to a one-line flow list).

    python3 -I tools/executive/add_hearing_src.py [--dry-run]

Written Nov. 5, 2026; `./bib check` warns [hearings] on a matched holder whose src lacks his hearing, the cue to rerun.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from bib import executive as X, hearings, store   # noqa: E402


def holder_blocks(lines, name):
    """(start, end) of each holder block '- name: NAME' in the file's lines."""
    out = []
    for i, l in enumerate(lines):
        m = re.match(r"^(\s*)- name: (.+?)\s*$", l)
        if not m or m.group(2).strip("'\"").replace("''", "'") != name:
            continue
        ind = len(m.group(1))
        j = i + 1
        while j < len(lines):
            m2 = re.match(r"^(\s*)(\S)", lines[j])
            if m2 and (len(m2.group(1)) < ind + 2 or (len(m2.group(1)) == ind and m2.group(2) == "-")):
                break
            j += 1
        out.append((i, j, ind))
    return out


def office_span(lines, oid):
    """The lines of the office '- id: OID' (to the next office at its indent)."""
    for i, l in enumerate(lines):
        m = re.match(r"^(\s*)- id: '?(.+?)'?\s*$", l)
        if m and m.group(2) == oid:
            ind = len(m.group(1))
            j = i + 1
            while j < len(lines) and not re.match(r"^\s{0,%d}\S" % ind, lines[j]):
                j += 1
            return i, j
    return 0, len(lines)


def insert(lines, start, end, ind, item):
    """Add item to the block's src; True where the block changed."""
    for k in range(start, end):
        m = re.match(r"^(\s*)src:\s*(.*)$", lines[k])
        if not m:
            continue
        rest = m.group(2)
        if rest.startswith("[") and rest.rstrip().endswith("]"):
            if item in rest:
                return False
            lines[k] = lines[k].rstrip()[:-1] + f", {item}]\n"
            return True
        if rest.strip():                 # an anchor or alias ('&id001', '*id001'): left to the hand
            raise ValueError(f"src not a plain list at line {k + 1}")
        j = k + 1
        last = k
        while j < end and re.match(r"^\s*- ", lines[j]) and len(re.match(r"^(\s*)", lines[j]).group(1)) <= len(m.group(1)) + 2:
            if item in lines[j]:
                return False
            last = j
            j += 1
        pre = re.match(r"^(\s*- )", lines[last + 0]).group(1) if last > k else m.group(1) + "- "
        lines.insert(last + 1, f"{pre}{item}\n")
        return True
    lines.insert(end, " " * (ind + 2) + f"src: [{item}]\n")
    return True


def main():
    dry = "--dry-run" in sys.argv
    series = store.Series()
    units = X.load()
    changed = 0
    for (unit, oid, name, frm), pkgs in sorted(hearings.by_holder(series).items()):
        path = os.path.join(X.DIR, units[unit]["_file"])
        lines = open(path, encoding="utf-8").readlines()
        did = False
        for p in sorted(set(pkgs)):
            lo_, hi_ = office_span(lines, oid)
            blocks = [b for b in holder_blocks(lines, name) if lo_ <= b[0] < hi_]
            pick = [b for b in blocks if any(re.match(rf"^\s*(?:from|seen):\s*'?{re.escape(frm)}'?\s*$", lines[k])
                                             for k in range(b[0], b[1]))] or blocks
            if len(pick) != 1:
                print(f"skipped {unit}.{oid} {name} {frm}: {len(pick)} blocks", file=sys.stderr)
                break
            try:
                did = insert(lines, *pick[0], f"Hearing {p}") or did
            except ValueError as e:
                print(f"skipped {unit}.{oid} {name}: {e}", file=sys.stderr)
                break
        if did:
            changed += 1
            if not dry:
                open(path, "w", encoding="utf-8").writelines(lines)
    print(changed, "holders given their hearing", file=sys.stderr)


if __name__ == "__main__":
    main()
