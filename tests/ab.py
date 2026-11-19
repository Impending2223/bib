"""A/B: the same data checked and built by the code of two git revisions, and the outputs compared.

    python3 tests/ab.py REV_A REV_B [--data DIR] [--build WHICH | --no-build] [--keep]

For each revision, the code (`tools/`, `bib`, `templates/`) is taken out of git (`git archive`; a REV of "." is the
working tree, uncommitted changes and all) into a temporary tree, and every other top-level entry of the data directory (--data; default: this checkout) is linked into it, so
both sides read the very same files, whatever the revisions' own data. Each side runs `./bib check` and then
`./bib build [WHICH] --force` (all pages unless --build names one; --no-build skips it), each in its own tree, so
their build/ directories are their own. Then: the check outputs compared, and every file under build/ compared byte
for byte (but for NONDETERMINISTIC, a feed's time of writing): the files only one side wrote, the files that differ, and the first differing lines of each.

Exit 0 when both sides agree in everything; 1 when anything differs. A rewrite is proved byte-identical on the full
data by `tests/ab.py main HEAD` (it takes the time two full builds take: run it in the background); on the
tests' fixture, in seconds, by `tests/ab.py HEAD . --data tests/fixture` (what a golden test's failure points to).
The data is read, never written: the trees, their build/ and .cache/ are under a temporary directory, removed after
unless --keep.
"""
import argparse
import difflib
import filecmp
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CODE = ["tools", "bib", "templates"]          # taken from each revision
SKIP = {".git", "build", ".cache", ".venv", "tests"} | set(CODE)


def tree(rev, data, where):
    """A tree with REV's code and DATA's files (linked)."""
    os.makedirs(where)
    if rev == ".":                       # the working tree's code, uncommitted changes and all
        for name in CODE:
            s = os.path.join(REPO, name)
            if os.path.isdir(s):
                shutil.copytree(s, os.path.join(where, name), ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copy2(s, os.path.join(where, name))
    else:
        arch = subprocess.run(["git", "archive", "--format=tar", rev, "--", *CODE], cwd=REPO, capture_output=True)
        if arch.returncode:
            sys.exit(f"git archive {rev}: {arch.stderr.decode().strip()}")
        subprocess.run(["tar", "-x", "-C", where], input=arch.stdout, check=True)
    for name in sorted(os.listdir(data)):
        if name not in SKIP:
            os.symlink(os.path.join(data, name), os.path.join(where, name))
    return where


def run(where, args, log):
    env = dict(os.environ, BIB_ROOT=where, PYTHONDONTWRITEBYTECODE="1")
    t = time.time()
    p = subprocess.run(["./bib", *args], cwd=where, env=env, capture_output=True, text=True)
    with open(log, "w", encoding="utf-8") as f:
        f.write(p.stdout + p.stderr + f"exit {p.returncode}\n")
    return p.returncode, time.time() - t


def files(root):
    out = set()
    for d, _, fs in os.walk(root):
        for f in fs:
            out.add(os.path.relpath(os.path.join(d, f), root))
    return out


# Output that is not a function of the data and the code: the time a feed was written. Blanked before comparing.
NONDETERMINISTIC = [(re.compile(rb"<dateCreated>[^<]*</dateCreated>"), b"<dateCreated>(normalized)</dateCreated>")]


def normalized(path):
    with open(path, "rb") as f:
        data = f.read()
    for rx, rep in NONDETERMINISTIC:
        data = rx.sub(rep, data)
    return data


def same(a, b):
    return filecmp.cmp(a, b, shallow=False) or normalized(a) == normalized(b)


def first_diff(a, b, n=8):
    try:
        la = open(a, encoding="utf-8").read().splitlines()
        lb = open(b, encoding="utf-8").read().splitlines()
    except UnicodeDecodeError:
        return ["  (binary files differ)"]
    d = list(difflib.unified_diff(la, lb, "A", "B", n=0, lineterm=""))
    return ["  " + x[:200] for x in d[2:2 + n]]


def compare(a, b, label):
    """Lines describing how two output trees (or files) differ; empty when identical."""
    if os.path.isfile(a) or os.path.isfile(b):
        if os.path.isfile(a) and os.path.isfile(b) and same(a, b):
            return []
        return [f"{label}: differs"] + first_diff(a, b)
    fa, fb = files(a) if os.path.isdir(a) else set(), files(b) if os.path.isdir(b) else set()
    out = []
    for f in sorted(fa - fb):
        out.append(f"{label}/{f}: only A")
    for f in sorted(fb - fa):
        out.append(f"{label}/{f}: only B")
    diff = [f for f in sorted(fa & fb) if not same(os.path.join(a, f), os.path.join(b, f))]
    for f in diff:
        out.append(f"{label}/{f}: differs")
        out += first_diff(os.path.join(a, f), os.path.join(b, f))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("rev_a")
    ap.add_argument("rev_b")
    ap.add_argument("--data", default=REPO, help="the data directory both sides read (default: this checkout)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--build", metavar="WHICH", help="build one page (a list key, 'series', 'names' ...)")
    g.add_argument("--no-build", action="store_true", help="compare the check only")
    ap.add_argument("--keep", action="store_true", help="keep the temporary trees (their paths are printed)")
    a = ap.parse_args(argv)
    data = os.path.abspath(a.data)
    tmp = tempfile.mkdtemp(prefix="bib-ab-")
    try:
        sides = {}
        for side, rev in (("A", a.rev_a), ("B", a.rev_b)):
            where = tree(rev, data, os.path.join(tmp, side))
            code, secs = run(where, ["check"], os.path.join(tmp, f"check-{side}.txt"))
            print(f"{side} {rev}: check exit {code} ({secs:.0f} s)")
            if not a.no_build:
                code, secs = run(where, ["build"] + ([a.build] if a.build else []) + ["--force"],
                                 os.path.join(tmp, f"build-{side}.txt"))
                print(f"{side} {rev}: build {a.build or 'all'} exit {code} ({secs:.0f} s)")
            sides[side] = where
        out = compare(os.path.join(tmp, "check-A.txt"), os.path.join(tmp, "check-B.txt"), "check output")
        if not a.no_build:
            out += compare(os.path.join(tmp, "build-A.txt"), os.path.join(tmp, "build-B.txt"), "build output")
            out += compare(os.path.join(sides["A"], "build"), os.path.join(sides["B"], "build"), "build")
        n = len(files(os.path.join(sides["A"], "build"))) if not a.no_build else 0
        if out:
            print("\n".join(out))
            print(f"DIFFERENT: {sum(1 for x in out if not x.startswith('  '))} differences")
        else:
            print(f"IDENTICAL: check output" + (f", build output and {n} files under build/" if not a.no_build else ""))
        if a.keep:
            print(f"trees kept: {tmp}")
        return 1 if out else 0
    finally:
        if not a.keep:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
