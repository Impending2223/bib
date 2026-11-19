"""The live bugs of the code review of Nov. 19, 2026 (notes/proposals/code-review-2026-11.md, cluster 2): one test, or
a few, for each fix."""
import os
import re
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from tools.bib import addops, claims, notemerge  # noqa: E402


# ---------------------------------------------------------------- 1. the note's sentences after an abbreviation

def test_opener_after_abbreviation_starts_a_sentence():
    n = "S. 3361, 87th Cong. To check: [[w.a]]. Names: Kennedy."
    assert notemerge.sentences(n) == ["S. 3361, 87th Cong.", "To check: [[w.a]].", "Names: Kennedy."]
    for abbr in ("Cong.", "Sess.", "B.", "n.", "Rep."):
        for opener in ("To check: [[w.a]].", "Check: the day.", "Names: Rusk.", "See [[cal.1961-01-20.x]].",
                       "Made public: 1975.", "Reply: [[cal.1961-01-21.x]].", "The order: x.", "Bibliography: x."):
            n = f"H.R. 1, 87th {abbr} {opener}"
            assert notemerge.sentences(n) == [f"H.R. 1, 87th {abbr}", opener], n


def test_abbreviation_still_holds_inside_a_sentence():
    assert notemerge.sentences("106 Cong. Rec. 13,819 (1960). Names: X.") == ["106 Cong. Rec. 13,819 (1960).",
                                                                          "Names: X."]
    assert notemerge.sentences("[[w.x]], 258 n. Kotz says so.") == ["[[w.x]], 258 n. Kotz says so."]


def test_to_check_joins_the_existing_run():
    e = {"id": "cal.1962-10-24.x", "c": "A bill.", "n": "S. 3361, 87th Cong. To check: [[w.a]]. Names: X."}
    new, err = addops.to_check(e, {"add": ["[[w.b]]"]})
    assert err is None
    assert new["n"] == "S. 3361, 87th Cong. To check: [[w.a]]; [[w.b]]. Names: X."
    assert new["n"].count("To check:") == 1
    again, _ = addops.to_check(new, {"add": ["[[w.b]]"]})
    assert again["n"] == new["n"]


def test_claims_reads_made_public_after_an_abbreviation_as_no_source():
    src, other = claims.note_parts("[[w.k]], 320 n. Made public: Check; Kotz cites the taps. Names: King.")
    assert src == ["[[w.k]], 320 n"]
    assert other == ["Made public: Check; Kotz cites the taps.", "Names: King."]


# ---------------------------------------------------------------- 2. a link whose address holds (...)

UN = "[S.C. Res. 232](https://undocs.org/S/RES/232(1966)) (Dec. 16, 1966)."
UN_URL = "https://undocs.org/S/RES/232(1966)"


def test_one_link_pattern_reads_the_whole_address():
    from tools.bib import calaudit, claims, dayorder, markup, resultform, standing, statements, vis, works
    assert [m.group(2) for m in markup.LINK_RE.finditer(UN)] == [UN_URL]
    assert claims.LINK is markup.LINK_RE and vis.LINK is markup.LINK_RE
    assert claims.LINK.findall(UN) == [("S.C. Res. 232", UN_URL)]
    assert claims.item_key(UN) == ("url", UN_URL)
    assert standing._inline(UN) == f'<a href="{UN_URL}">S.C. Res. 232</a> (Dec. 16, 1966).'
    assert statements.plain(UN) == "S.C. Res. 232 (Dec. 16, 1966)."
    assert markup.strip_links(UN) == "S.C. Res. 232 (Dec. 16, 1966)."
    assert works.bluebook_pin("*Title*, [online](" + UN_URL + ")", "12") == ", 12"
    blank = resultform.clean(UN)
    assert UN_URL not in blank and "1966)) " not in blank and blank.endswith("(Dec. 16, 1966).")
    assert "S/RES" not in resultform.clean("see (" + UN_URL + ") here")
    assert re.findall(r"\[((?:[^\[\]]|\[[^\]]*\])*)\]\((" + markup.URL + r")\)", UN) == [("S.C. Res. 232", UN_URL)]
    assert calaudit.markup is markup


def test_dayorder_plain_strips_a_paren_link():
    from tools.bib import dayorder, store
    assert dayorder.plain_c({"c": UN}) == store.fold("S.C. Res. 232 (Dec. 16, 1966).")


def test_plain_links_unchanged():
    from tools.bib import claims, markup
    t = "[FRUS 1961–63, IV, doc. 34](https://history.state.gov/historicaldocuments/frus1961-63v04/d34). [a](http://x.org/b)"
    assert claims.LINK.findall(t) == [("FRUS 1961–63, IV, doc. 34",
                                       "https://history.state.gov/historicaldocuments/frus1961-63v04/d34"),
                                      ("a", "http://x.org/b")]
    assert markup.strip_links(t) == "FRUS 1961–63, IV, doc. 34. a"


# ---------------------------------------------------------------- 3. content left out of the build, counted

def test_committees_month_that_fails_is_counted(tmp_path, monkeypatch):
    from tools.bib import committees, faults
    faults.reset()
    (tmp_path / "1961-01.yaml").write_text("docs:\n  - {date: '1961-01-03', x: 1}\n", encoding="utf-8")
    (tmp_path / "1961-02.yaml").write_bytes(b"docs: \xff\xfe\n")          # not UTF-8: the load raises
    monkeypatch.setattr(committees, "DIR", str(tmp_path))
    monkeypatch.setattr(committees, "_cache", {})
    by = committees.load()
    assert list(by) == ["1961-01-03"]
    assert len(faults.FAULTS) == 1 and "1961-02.yaml" in faults.FAULTS[0][0]
    assert "1 build fault" in faults.report()
    faults.reset()


def test_vis_pass_that_fails_is_counted(monkeypatch):
    from tools.bib import faults, vis
    faults.reset()

    def boom(series):
        raise ValueError("no")
    monkeypatch.setattr(vis, "_problems", boom)
    assert vis.problems(None) == [("tools/bib/vis.py", "the visibility pass failed: ValueError: no")]
    assert faults.FAULTS == [("tools/bib/vis.py", "the visibility pass failed: ValueError: no")]
    faults.reset()


# ---------------------------------------------------------------- 4. DataError is an ordinary error

def test_data_error_is_an_exception_not_an_exit():
    from tools.bib import store
    assert issubclass(store.DataError, Exception) and not issubclass(store.DataError, SystemExit)


def test_a_patch_that_does_not_load_is_a_finding(tmp_path):
    from tools.bib import patchaudit, patchcheck
    bad = tmp_path / "2026-11-19-bad.yaml"
    bad.write_text("patch: bad\nops:\n  - add: [unclosed\n", encoding="utf-8")
    errors, warnings = patchcheck.check(None, str(bad))
    assert len(errors) == 1 and errors[0].startswith("does not load: ") and "not valid YAML" in errors[0]
    (p, d, err), = patchaudit.load([str(bad)])
    assert d is None and "not valid YAML" in err
    marked = tmp_path / "2026-11-19-marked.yaml"
    marked.write_text("patch: x\n<<<<<<< ours\nops: []\n=======\nops: []\n>>>>>>> theirs\n", encoding="utf-8")
    errors, _ = patchcheck.check(None, str(marked))
    assert "git conflict markers" in errors[0]


def test_cli_turns_a_data_error_into_exit_1(monkeypatch, capsys):
    from tools.bib import cli, store

    def bad(*a, **k):
        raise store.DataError("lists/cal/196101.yaml:3: not valid YAML (x).")
    monkeypatch.setattr(store, "Series", bad)
    assert cli.main(["status"]) == 1
    assert "lists/cal/196101.yaml:3: not valid YAML" in capsys.readouterr().err


# ---------------------------------------------------------------- 5. merge safety

def _mini(root):
    """A series of one calendar month, three entries, in `root`."""
    (root / "lists" / "cal").mkdir(parents=True)
    (root / "series.yaml").write_text("lists:\n  - {key: cal, abbr: Cal.}\n", encoding="utf-8")
    (root / "lists" / "cal" / "list.yaml").write_text(
        "kind: calendar\nsections:\n  - {id: '196101', title: January 1961, file: 196101.yaml}\n", encoding="utf-8")
    from tools.bib import store
    store.dump_yaml({"list": "cal", "section": "196101", "entries": [
        {"id": f"cal.1961-01-0{i}.x", "date": f"1961-01-0{i}", "c": f"Event {i}.", "n": f"Note {i}."}
        for i in (1, 2, 3)]}, str(root / "lists" / "cal" / "196101.yaml"))


@pytest.fixture
def mini(tmp_path, monkeypatch):
    from tools.bib import markup, store
    for k in ("WORKS", "WORKS_FULL", "WORKS_ID"):
        monkeypatch.setattr(markup, k, getattr(markup, k))
    _mini(tmp_path)
    monkeypatch.setattr(store, "ROOT", str(tmp_path))
    return tmp_path


def _entry(series, eid):
    return series.get(eid)[2]


def test_save_section_merges_a_change_made_on_disk(mini):
    from tools.bib import store
    mine = store.Series(str(mini))
    other = store.Series(str(mini))                    # another hand, at work on the same month
    lst, sec, e = other.get("cal.1961-01-02.x")
    sec.entries[1] = dict(e, n="Note 2, theirs.")
    other.save_section(sec)
    lst, sec, e = mine.get("cal.1961-01-01.x")
    sec.entries[0] = dict(e, n="Note 1, ours.")
    mine.save_section(sec)                              # must not overwrite theirs
    now = store.Series(str(mini))
    assert _entry(now, "cal.1961-01-01.x")["n"] == "Note 1, ours."
    assert _entry(now, "cal.1961-01-02.x")["n"] == "Note 2, theirs."
    assert not any(e.get("conflict") for _, e in now.lists["cal"].entries())
    # both change one field: a conflict recorded, neither text lost
    lst, sec, e = other.get("cal.1961-01-03.x")
    sec.entries[2] = dict(e, c="Event 3, theirs.")
    other.save_section(sec)
    lst, sec, e = mine.get("cal.1961-01-03.x")
    sec.entries[2] = dict(e, c="Event 3, ours.")
    mine.save_section(sec)
    e3 = _entry(store.Series(str(mini)), "cal.1961-01-03.x")
    assert e3["c"] == "Event 3, ours."
    assert e3["conflict"] == [{"field": "c", "ours": "Event 3, ours.", "theirs": "Event 3, theirs.",
                               "base": "Event 3.", "from": "disk"}]
    assert _entry(store.Series(str(mini)), "cal.1961-01-02.x")["n"] == "Note 2, theirs."


def test_save_section_refuses_a_changed_file_that_does_not_load(mini):
    from tools.bib import store
    mine = store.Series(str(mini))
    path = mini / "lists" / "cal" / "196101.yaml"
    path.write_text(path.read_text(encoding="utf-8") + "<<<<<<< ours\n", encoding="utf-8")
    lst, sec, e = mine.get("cal.1961-01-01.x")
    sec.entries[0] = dict(e, n="Note 1, ours.")
    with pytest.raises(store.DataError, match="changed on disk during this run"):
        mine.save_section(sec)
    assert path.read_text(encoding="utf-8").endswith("<<<<<<< ours\n")


def test_apply_patch_is_all_or_nothing(mini, monkeypatch):
    from tools.bib import addops, merge, store
    monkeypatch.setattr(addops, "DEFERRED", str(mini / "inbox" / "deferred.yaml"))
    path = mini / "lists" / "cal" / "196101.yaml"
    before = path.read_bytes()
    s = store.Series(str(mini))
    rep = merge.Report()
    merge.apply_patch(s, {"ops": [{"tag": {"id": "cal.1961-01-01.x", "add": ["topic:x"]}},
                                  {"edit": {"id": "cal.1961-01-09.nothing", "set": {"c": "x"}}}]}, "t", rep)
    assert rep.errors == 1
    assert path.read_bytes() == before                  # the good op not written either
    rep = merge.Report()
    merge.apply_patch(store.Series(str(mini)), {"ops": [{"tag": {"id": "cal.1961-01-01.x", "add": ["topic:x"]}}]},
                      "t", rep)
    assert rep.errors == 0 and "topic:x" in path.read_text(encoding="utf-8")


def test_merge_with_a_failed_op_exits_1_and_keeps_the_patch(mini, monkeypatch, capsys):
    import functools
    from tools.bib import cli, store
    monkeypatch.setattr(store, "Series", functools.partial(store.Series, str(mini)))
    patch = mini / "inbox" / "2026-11-19-t.yaml"
    patch.parent.mkdir()
    patch.write_text("patch: t\nops:\n  - tag: {id: cal.1961-01-01.x, add: [topic:x]}\n"
                     "  - edit: {id: cal.1961-01-09.nothing, set: {c: x}}\n", encoding="utf-8")
    before = (mini / "lists" / "cal" / "196101.yaml").read_bytes()
    assert cli.main(["merge", "--archive", str(patch)]) == 1
    assert "1 ops failed: nothing written" in capsys.readouterr().out
    assert patch.exists() and (mini / "lists" / "cal" / "196101.yaml").read_bytes() == before


def test_deferred_ops_leave_the_file_only_once_applied(tmp_path, monkeypatch):
    from tools.bib import addops, store
    monkeypatch.setattr(addops, "DEFERRED", str(tmp_path / "deferred.yaml"))
    rows = [{"from": "p1", "op": {"to-check": {"id": "cal.a", "add": ["[[w.x]]"]}}},
            {"from": "p2", "op": {"names": {"id": "cal.b", "add": ["Rusk"]}}}]
    addops.defer_rows(rows)
    before = (tmp_path / "deferred.yaml").read_bytes()

    class S:
        def get(self, eid):
            return ("l", "s", {"id": eid}) if eid == "cal.a" else None
    ready = addops.take_deferred(S())
    assert ready == rows[:1]
    assert (tmp_path / "deferred.yaml").read_bytes() == before     # nothing removed yet
    addops.drop_deferred(ready)
    assert store.load_yaml(str(tmp_path / "deferred.yaml")) == rows[1:]
    addops.drop_deferred(rows[1:])
    assert not (tmp_path / "deferred.yaml").exists()


def test_merge_lock_one_at_a_time(tmp_path, monkeypatch):
    import fcntl
    import threading
    from tools.bib import merge, store
    monkeypatch.setattr(store, "ROOT", str(tmp_path))
    with merge.lock() as waited:
        assert waited is False
        with pytest.raises(store.DataError, match="another merge is running"):
            with merge.lock(wait=False):
                pass
    holder = open(tmp_path / ".cache" / "merge.lock", "a+")
    fcntl.flock(holder, fcntl.LOCK_EX)
    threading.Timer(0.3, lambda: (fcntl.flock(holder, fcntl.LOCK_UN), holder.close())).start()
    with merge.lock() as waited:
        assert waited is True


# ---------------------------------------------------------------- 6. ops that would change bookkeeping fields

def test_op_problems_refuses_bookkeeping_fields():
    from tools.bib import merge
    for k in ("id", "aliases", "conflict", "_derived"):
        assert merge.op_problems("edit", {"id": "cal.x", "set": {k: "y"}}), k
        assert merge.op_problems("edit", {"id": "cal.x", "unset": [k]}), k
    assert merge.op_problems("edit", {"id": "cal.x", "set": {"c": "y", "n": "z"}, "unset": ["time"]}) == []
    assert merge.op_problems("add", {"list": "kja", "entry": {"id": "cal.1961-01-01.x"}}) == [
        ("cal.1961-01-01.x", "add to list 'kja': the id is not of that list (its ids begin kja.)")]
    assert merge.op_problems("add", {"list": "cal", "entry": {"id": "cal.1961-01-01.x"}}) == []
    assert merge.op_problems("add", {"entry": {"id": "cal.1961-01-01.x"}}) == []


def test_apply_patch_refuses_a_rename(mini):
    from tools.bib import merge, store
    path = mini / "lists" / "cal" / "196101.yaml"
    before = path.read_bytes()
    for ops in ([{"edit": {"id": "cal.1961-01-01.x", "set": {"id": "cal.1961-01-02.x"}}}],
                [{"edit": {"id": "cal.1961-01-01.x", "unset": ["id"]}}],
                [{"add": {"list": "cal", "section": "196101",
                          "entry": {"id": "kja.someone", "date": "1961-01-05", "c": "x"}}}]):
        rep = merge.Report()
        merge.apply_patch(store.Series(str(mini)), {"ops": ops}, "t", rep)
        assert rep.errors == 1, rep.lines
        assert path.read_bytes() == before


def test_patch_check_refuses_a_rename(mini):
    from tools.bib import patchcheck, store
    p = mini / "2026-11-19-rename.yaml"
    p.write_text("patch: rename\nops:\n  - edit: {id: cal.1961-01-01.x, set: {id: cal.1961-01-09.y}}\n"
                 "  - edit: {id: cal.1961-01-02.x, unset: [conflict]}\n", encoding="utf-8")
    errors, _ = patchcheck.check(store.Series(str(mini)), str(p))
    assert "edit cal.1961-01-01.x: an edit may not set 'id' (id, aliases, conflict and _ fields change by " \
           "./bib combine, ./bib resolve, or by hand)" in errors
    assert any(x.startswith("edit cal.1961-01-02.x: an edit may not unset 'conflict'") for x in errors)
    assert sum("may not set 'id'" in x for x in errors) == 1          # said once, not again from the dry run
