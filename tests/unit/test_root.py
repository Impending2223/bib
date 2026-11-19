"""BIB_ROOT: the tools read the data from it when it is set, else from the checkout; their own scripts from the code."""
import os
import subprocess
import sys

from conftest import REPO

PROBE = ("import sys; sys.path.insert(0, 'tools'); from bib import store, diary, check, pvi; "
         "print(store.ROOT); print(diary.ROOT); print(check.TOOLS); print(pvi.ROOT)")


def probe(env):
    e = {k: v for k, v in os.environ.items() if k != "BIB_ROOT"}
    e.update(env)
    out = subprocess.run([sys.executable, "-c", PROBE], cwd=REPO, env=e, capture_output=True, text=True, check=True)
    return out.stdout.split()


def test_unset_is_the_checkout():
    assert probe({}) == [REPO, REPO, os.path.join(REPO, "tools"), REPO]


def test_set_is_that_tree(tmp_path):
    root = str(tmp_path)
    assert probe({"BIB_ROOT": root}) == [root, root, os.path.join(REPO, "tools"), root]


def test_relative_is_made_absolute():
    fx = os.path.join(REPO, "tests", "fixture")
    assert probe({"BIB_ROOT": "tests/fixture"})[0] == fx
