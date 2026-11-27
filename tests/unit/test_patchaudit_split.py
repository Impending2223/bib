"""patchaudit.audit: an edit that splits an entry may drop a work read from the old note when the same patch adds the
entry the work moves to (Nov. 27, 2026: readers had kept moved cites in the old note to get past the drop rule)."""
import re

import yaml

from bib import patchaudit, store


def _entry_with_a_read_card(series):
    for sec, e in series.lists["cal"].entries():
        n = e.get("n") or ""
        m = re.match(r"\[\[(w\.[^\]]+)\]\], [0-9]", n)
        if "when" in e and m:
            return e, m.group(1)
    raise AssertionError("no entry with a read card in the fixture")


def _write(tmp_path, e, card, add):
    ops = [{"edit": {"id": e["id"], "base": store.rev(e), "set": {"n": "Names: none."}}}]
    if add:
        ops.append({"add": {"entry": {"id": e["id"] + "-split", "when": e["when"], "date": str(e["date"]),
                                      "thread": e["thread"], "c": "The other act.",
                                      "n": f"[[{card}]], 1. See [[{e['id']}]]."}}})
    p = tmp_path / "2026-11-27-split.yaml"
    p.write_text(yaml.safe_dump({"patch": "split", "ops": ops}, allow_unicode=True), encoding="utf-8")
    return str(p)


def _drops(series, path):
    return [line for line in patchaudit.audit(series, [path]) if "would drop" in str(line)]


def test_a_moved_work_is_not_a_drop(tmp_path):
    series = store.Series()
    e, card = _entry_with_a_read_card(series)
    assert _drops(series, _write(tmp_path, e, card, add=False))          # dropped and moved nowhere: refused
    assert not _drops(series, _write(tmp_path, e, card, add=True))       # moved to the split's new entry: not a drop
