"""Shared by every test: the tools on sys.path, the fixture (tests/fixture) as BIB_ROOT, the goldens' option.

    pytest -q -m "not slow"          the fast suite (CI)
    pytest -q                        everything, the slow property tests over the real data too
    pytest --update-goldens          rewrite tests/golden/expected/ from what the code does now
"""
import difflib
import os
import re
import shutil
import subprocess
import sys

import pytest

TESTS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TESTS)
FIXTURE = os.path.join(TESTS, "fixture")
EXPECTED = os.path.join(TESTS, "golden", "expected")

# Unit tests import the tools in-process; they read the fixture, never the repository's data.
os.environ["BIB_ROOT"] = FIXTURE
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, TESTS)


def pytest_addoption(parser):
    parser.addoption("--update-goldens", action="store_true",
                     help="rewrite tests/golden/expected/ from the current output instead of comparing")


@pytest.fixture
def update_goldens(request):
    return request.config.getoption("--update-goldens")


def fixture_copy(where):
    """A fresh copy of tests/fixture at `where` (no build/, no .cache/): commands that write work on it."""
    shutil.copytree(FIXTURE, where, ignore=shutil.ignore_patterns("build", ".cache", "__pycache__"))
    return str(where)


def bib(root, *args, env=None):
    """`./bib ARGS` on the tree at root; its output (stdout, then stderr) with the root's path written <ROOT>, and
    the exit status as a last line."""
    e = dict(os.environ, BIB_ROOT=str(root), PYTHONDONTWRITEBYTECODE="1")
    e.update(env or {})
    p = subprocess.run([os.path.join(REPO, "bib"), *args], cwd=root, env=e, capture_output=True, text=True)
    out = p.stdout + (("\n--- stderr\n" + p.stderr) if p.stderr else "")
    return out.replace(str(root), "<ROOT>") + f"\n--- exit {p.returncode}\n"


def golden(name, text, update):
    """Compare text with tests/golden/expected/NAME; with --update-goldens, write it instead."""
    path = os.path.join(EXPECTED, name)
    if update or not os.path.exists(path):
        if not update:
            pytest.fail(f"no golden {name}: run pytest --update-goldens to write it, and read it before committing")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return
    with open(path, encoding="utf-8") as f:
        want = f.read()
    if text != want:
        diff = list(difflib.unified_diff(want.splitlines(), text.splitlines(), "golden", "now", n=1, lineterm=""))
        shown = "\n".join(d[:240] for d in diff[:60])
        pytest.fail(f"{name} differs from its golden ({len(diff)} diff lines; first shown). If the change is "
                    f"meant, run pytest --update-goldens and commit the new golden with the change.\n{shown}")


NONDETERMINISTIC = [(re.compile(r"<dateCreated>[^<]*</dateCreated>"), "<dateCreated>(normalized)</dateCreated>")]


def normalize(text):
    for rx, rep in NONDETERMINISTIC:
        text = rx.sub(rep, text)
    return text
