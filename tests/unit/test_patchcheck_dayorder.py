"""patchcheck.py STYLE 12 (Nov. 20, 2026): the day's order (dayorder.problems) on the entries a patch touches, before
the merge: a `follows` to an entry of another day, or between two loosely dated entries, is refused, as check refuses
it once merged (two such links reached the tree on Nov. 20). On the fixture (April 1961)."""
from bib import patchcheck, store

EID = "cal.1961-04-30.cuba-bay-of-pigs"          # the fixture's


def run(tmp_path, ops):
    series = store.Series()
    p = tmp_path / "2026-11-20-fx.yaml"
    p.write_text("patch: fx-day-order\nby: tests\nops:\n" + ops, encoding="utf-8")
    errors, _ = patchcheck.check(series, str(p))
    return [x for x in errors if "[day-order]" in x]


def add(eid, when, date, follows):
    return ("  - add:\n      section: '196104'\n"
            f"      entry: {{id: {eid}, when: '{when}', date: '{date}', thread: cuba-bay-of-pigs, "
            f"c: An event., n: A note., follows: [{follows}]}}\n")


def test_follows_another_day(tmp_path):
    errs = run(tmp_path, add("cal.1961-04-29.fx", "Apr. 29", "1961-04-29", EID))
    assert errs == [f"cal.1961-04-29.fx: follows {EID}, an entry of another day (1961-04-30) [day-order]"]


def test_follows_the_same_day(tmp_path):
    assert run(tmp_path, add("cal.1961-04-30.fx", "Apr. 30", "1961-04-30", EID)) == []


def test_follows_between_month_dated_entries(tmp_path):
    ops = (add("cal.1961-04.fx", "Apr.", "1961-04", "cal.1961-04.fx-2")
           + "  - add:\n      section: '196104'\n      entry: {id: cal.1961-04.fx-2, when: Apr., date: '1961-04', "
             "thread: cuba-bay-of-pigs, c: Another event., n: A note.}\n")
    assert run(tmp_path, ops) == ["cal.1961-04.fx: follows cal.1961-04.fx-2, an entry of another day (1961-04) [day-order]"]


A, B = "cal.1961-08-04.china-leadership-4", "cal.1961-08-04.china-leadership-5"   # the fixture's: B follows A, untimed


def test_cycle_on_the_other_end(tmp_path):
    # the search meets the back edge at B, which the patch does not touch
    assert run(tmp_path, f"  - follows: {{id: {A}, add: [{B}]}}\n") == [
        f"{B}: a cycle of follows: {A} -> {B} -> {A} [day-order]"]


def test_followed_entry_moved_to_another_day(tmp_path):
    base = store.rev(store.Series().get(A)[2])
    ops = f"  - edit:\n      id: {A}\n      base: '{base}'\n      set: {{when: Aug. 5, date: '1961-08-05'}}\n"
    assert run(tmp_path, ops) == [f"{B}: follows {A}, an entry of another day (1961-08-05) [day-order]"]


def test_followed_entry_deleted(tmp_path):
    base = store.rev(store.Series().get(A)[2])
    assert run(tmp_path, f"  - delete:\n      id: {A}\n      base: '{base}'\n") == [
        f"{B}: follows {A}: no such entry [day-order]"]
