"""Golden tests: what the tools print and write on the fixture (tests/fixture), compared with tests/golden/expected/.

They pin today's behaviour, right or wrong: a change that alters any of it fails here, and either the change is
meant (pytest --update-goldens, and the new golden committed with it, read first) or it is a regression.
The commands run as subprocesses (./bib with BIB_ROOT), several at once, each on its own copy of the fixture
where it writes.
"""
import concurrent.futures
import difflib
import hashlib
import os
import re
import shutil
import subprocess

import pytest
import yaml

from conftest import FIXTURE, REPO, bib, fixture_copy, golden, normalize

PATCHES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patches")
POOL = concurrent.futures.ThreadPoolExecutor(max_workers=max(2, min(8, os.cpu_count() or 2)))


# ---------------------------------------------------------------- check and build

@pytest.fixture(scope="module")
def jobs(tmp_path_factory):
    """Every command of this module started at once, on the pool (the suite's time is the longest job's, not the
    sum): the check, the build, the queries, the patch scenarios. Each test waits for its own."""
    base = tmp_path_factory.mktemp("golden")
    built = fixture_copy(base / "built")
    queried = fixture_copy(base / "queried")
    out = {"root": built,
           "check": POOL.submit(bib, built, "check"),
           "build": POOL.submit(bib, built, "build", "--force")}
    out.update({("scenario", n): POOL.submit(run_scenario, n, base / n) for n in SCENARIOS})
    out.update({("query", n): POOL.submit(bib, queried, *args) for n, args in QUERIES})
    return out


@pytest.fixture(scope="module")
def built(jobs):
    """One copy of the fixture: its check output, and its build (all pages, --force: the fixture has errors)."""
    return jobs["root"], jobs["check"].result(), jobs["build"].result()


def test_check(built, update_goldens):
    golden("check.txt", built[1], update_goldens)


def test_build_output(built, update_goldens):
    golden("build-output.txt", built[2], update_goldens)


def test_build_files(built, update_goldens):
    """Every file the build writes, by its sha256 (normalized where the output is not the data's: a feed's time).
    On a failure, see the files' differences: python3 tests/ab.py HEAD . --data tests/fixture"""
    out = os.path.join(built[0], "build")
    lines = []
    for d, _, fs in sorted(os.walk(out)):
        for f in sorted(fs):
            p = os.path.join(d, f)
            data = open(p, "rb").read()
            try:
                data = normalize(data.decode("utf-8")).encode("utf-8")
            except UnicodeDecodeError:
                pass
            lines.append(f"{hashlib.sha256(data).hexdigest()[:16]}  {len(data):9}  {os.path.relpath(p, out)}")
    golden("build-files.txt", "\n".join(lines) + "\n", update_goldens)


# ---------------------------------------------------------------- the read-only commands

QUERIES = [
    ("status", ["status"]),
    ("outline-cal", ["outline", "cal"]),
    ("outline-kja", ["outline", "kja"]),
    ("find-bay-of-pigs", ["find", "bay", "of", "pigs"]),
    ("find-folded", ["find", "Ngô", "Đình", "Diệm"]),
    ("find-thread", ["find", "-l", "cal", "--thread", "cuba-bay-of-pigs"]),
    ("find-month", ["find", "-l", "cal", "--since", "1961-08", "--until", "1961-08", "--ids", "--limit", "500"]),
    ("find-day", ["find", "-l", "cal", "--since", "1961-04-17", "--until", "1961-04-17"]),
    ("find-check", ["find", "-t", "check", "-l", "cal", "--ids", "--limit", "500"]),
    ("find-person-in-cal", ["find", "-t", "person", "-t", "in:cal", "-l", "kja"]),
    ("find-tag-name", ["find", "-t", "name:rusk-dean", "--ids", "--limit", "500"]),
    ("find-month-tag", ["find", "-t", "month:1961-04", "-t", "thread:laos", "--limit", "10"]),
    ("show-cal", ["show", "cal.1961-04-01.cuba", "cal.1961-08-13.berlin-and-vienna"]),
    ("show-thread", ["show", "cal.thread.cuba"]),
    ("show-missing", ["show", "cal.1961-04-31.nothing"]),
    ("works-show", ["works", "show", "w.reeves-president-kennedy"]),
    ("works-words", ["works", "Schlesinger"]),
    ("works-list", ["works", "list", "-t", "in:kja", "--sort", "year"]),
    ("new-id", ["new-id", "cal", "1961-04-17", "cuba-bay-of-pigs"]),
    ("conflicts", ["conflicts"]),
    ("tags", ["tags"]),
    ("ledger-find", ["ledger", "find", "1961-04-17"]),
    ("claims-show", ["claims", "show", "cal.1961-04-01.soviet-union"]),
    ("stemma", ["stemma", "cal.1961-04-01.cuba"]),
    ("executive-who", ["executive", "who", "Rusk"]),
]


@pytest.fixture(scope="module")
def queried(jobs):
    return {name: f"$ ./bib {' '.join(args)}\n" + jobs[("query", name)].result() for name, args in QUERIES}


@pytest.mark.parametrize("name", [q[0] for q in QUERIES])
def test_query(queried, name, update_goldens):
    golden(f"queries/{name}.txt", queried[name], update_goldens)


# ---------------------------------------------------------------- patches: patch-check and merge --auto

SCENARIOS = sorted(d for d in os.listdir(PATCHES) if os.path.isdir(os.path.join(PATCHES, d)))


def git(root, *args):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
               GIT_COMMITTER_EMAIL="t@t", GIT_AUTHOR_DATE="2026-01-01T00:00:00Z", GIT_COMMITTER_DATE="2026-01-01T00:00:00Z")
    subprocess.run(["git", "-c", "init.defaultBranch=main", "-c", "commit.gpgsign=false", *args], cwd=root,
                   env=env, check=True, capture_output=True)


def tree_diff(root):
    """The files the scenario changed or wrote, against the fixture, as unified diffs."""
    skip = {".git", ".cache", "build"}
    seen = set()
    out = []
    for base in (FIXTURE, root):
        for d, ds, fs in os.walk(base):
            ds[:] = sorted(x for x in ds if x not in skip)
            for f in sorted(fs):
                seen.add(os.path.relpath(os.path.join(d, f), base))
    for rel in sorted(seen):
        a, b = os.path.join(FIXTURE, rel), os.path.join(root, rel)
        ta = open(a, encoding="utf-8").read().splitlines() if os.path.exists(a) else []
        tb = open(b, encoding="utf-8").read().splitlines() if os.path.exists(b) else []
        if ta != tb:
            out += list(difflib.unified_diff(ta, tb, f"fixture/{rel}", f"after/{rel}", n=2, lineterm=""))
    return "\n".join(out) + "\n"


def run_scenario(name, where):
    """setup.yaml: `ledger` claims, `git` (the tree committed first), `before` (patches merged and committed
    first: the history a stale base is found in). Then each N.yaml: patch-check; then merge --auto of all of them.
    The transcript and the tree's changes."""
    src = os.path.join(PATCHES, name)
    root = fixture_copy(where)
    setup = yaml.safe_load(open(os.path.join(src, "setup.yaml"))) if os.path.exists(os.path.join(src, "setup.yaml")) else {}
    log = []
    os.makedirs(os.path.join(root, "inbox"), exist_ok=True)
    if setup.get("git"):
        git(root, "init", "-q")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "fixture")
    for f in setup.get("before") or []:
        shutil.copy(os.path.join(src, f), os.path.join(root, "inbox", f"before-{f}"))
        log.append(f"$ ./bib merge inbox/before-{f}\n" + bib(root, "merge", f"inbox/before-{f}"))
        os.remove(os.path.join(root, "inbox", f"before-{f}"))
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "before")
    for row in setup.get("ledger") or []:
        log.append(f"$ ./bib ledger add {' '.join(map(str, row))}\n" + bib(root, "ledger", "add", *map(str, row)))
    patches = sorted(f for f in os.listdir(src) if re.match(r"[1-9]\d*\.yaml$", f))
    for f in patches:
        shutil.copy(os.path.join(src, f), os.path.join(root, "inbox", f"{name}-{f}"))
    for f in patches:
        log.append(f"$ ./bib patch-check inbox/{name}-{f}\n" + bib(root, "patch-check", f"inbox/{name}-{f}"))
    args = [f"inbox/{name}-{f}" for f in patches]
    log.append(f"$ ./bib merge --auto {' '.join(args)}\n" + bib(root, "merge", "--auto", *args))
    if setup.get("git"):
        shutil.rmtree(os.path.join(root, ".git"))
    return "\n".join(log), tree_diff(root)


@pytest.fixture(scope="module")
def scenarios(jobs):
    return {n: jobs[("scenario", n)].result() for n in SCENARIOS}


@pytest.mark.parametrize("name", SCENARIOS)
def test_patch_transcript(scenarios, name, update_goldens):
    golden(f"patches/{name}.txt", scenarios[name][0], update_goldens)


@pytest.mark.parametrize("name", SCENARIOS)
def test_patch_tree(scenarios, name, update_goldens):
    golden(f"patches/{name}.diff", scenarios[name][1], update_goldens)
