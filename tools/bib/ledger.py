"""The ledger of new entries: one line an entry, written before the entry goes into a patch (the owner's request, Oct.
30, 2026; notes/extensions/memos/volume.md, §6).

    inbox/new-entries.tsv      date <TAB> thread <TAB> id <TAB> a few words <TAB> patch

    ./bib ledger add DATE THREAD ID "words" PATCH      claims the event (refused where the id is taken)
    ./bib ledger find DATE [--until DATE] [--thread T] the day's entries: in the tree, and claimed in the ledger
    ./bib ledger prune                                 drops the lines whose entries are in the tree

A reader adding an entry runs `ledger find` for its day first. Where the event is there, under another reader's id,
it cites that id (tools/bib/addops.py) and adds nothing; the merge applies a cite to a claimed id once the entry lands
(addops STYLE 7). A grep of one file replaces reading every pending patch. The file is appended under a lock (fcntl),
so readers at work together cannot interleave lines.
"""
import fcntl
import os

from . import store

PATH = os.path.join(store.ROOT, "inbox", "new-entries.tsv")
COLS = ("date", "thread", "id", "words", "patch")


def rows():
    if not os.path.exists(PATH):
        return []
    out = []
    with open(PATH, encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) == len(COLS):
                out.append(dict(zip(COLS, p)))
    return out


def named(eid):
    return any(r["id"] == eid for r in rows())


def add(series, date, thread, eid, words, patch):
    """Claim an id; refused where the tree or the ledger holds it. Returns an error or None."""
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    words = " ".join(str(words).split())
    for v in (date, thread, eid, words, patch):
        if "\t" in str(v) or "\n" in str(v):
            return "no tabs or newlines in a field"
    with open(PATH, "a+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            f.seek(0)
            taken = {line.split("\t")[2] for line in f if line.count("\t") >= 4}
            if eid in taken:
                return f"{eid} is claimed in the ledger"
            if series.get(eid):
                return f"{eid} is in the tree"
            f.seek(0, os.SEEK_END)
            f.write("\t".join([date, thread, eid, words, patch]) + "\n")
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
    return None


def find(series, since, until=None, thread=None):
    """The entries of the days, in the tree and in the ledger: (where, date, thread, id, words)."""
    until = until or since
    out = []
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for s, e in lst.entries():
            d = str(e.get("date") or "")
            if d and since <= d[:len(since)] and d[:len(until)] <= until:
                if thread and thread not in [e.get("thread")] + list(e.get("also") or []):
                    continue
                out.append(("tree", d, e.get("thread"), e["id"], (e.get("c") or "")[:90]))
    for r in rows():
        d = r["date"]
        if since <= d[:len(since)] and d[:len(until)] <= until and (not thread or r["thread"] == thread):
            if not series.get(r["id"]):
                out.append((f"ledger ({r['patch']})", d, r["thread"], r["id"], r["words"]))
    return sorted(out, key=lambda x: (x[1], x[2] or "", x[3]))


def prune(series):
    """Drop the lines whose entries are in the tree. Returns how many were dropped."""
    if not os.path.exists(PATH):
        return 0
    with open(PATH, "r+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            lines = f.readlines()
            keep = [l for l in lines if l.count("\t") < 4 or not series.get(l.split("\t")[2])]
            f.seek(0)
            f.truncate()
            f.writelines(keep)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
    return len(lines) - len(keep)
