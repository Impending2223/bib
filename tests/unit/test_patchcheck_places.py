"""patchcheck.py STYLE 11 (the audit, Nov. 19, 2026): a `place:` set by an `add` or an `edit` held to check's [place]
before the merge, against the gazetteer and the patch's own `place-key` rows; places.entry_problems, the rule both use.
On the fixture (April 1961)."""
import pytest

from bib import patchcheck, places, store

EID = "cal.1961-04-30.cuba-bay-of-pigs"          # the fixture's, with no place
UNKNOWN = "place 'nowhere-zz': not in the gazetteer (sources/places.yaml; a place-key op adds it) [place]"
UPPERVILLE = "  - place-key: {key: upperville-va, name: 'Upperville, Va.', zone: America/New_York, st: VA}\n"


def run(tmp_path, ops):
    series = store.Series()
    base = store.rev(series.get(EID)[2])
    p = tmp_path / "2026-11-20-fx.yaml"
    p.write_text("patch: fx-place-check\nby: tests\nops:\n" + ops.replace("BASE", base), encoding="utf-8")
    errors, _ = patchcheck.check(series, str(p))
    return [x for x in errors if "[place]" in x]


def edit(place):
    return f"  - edit: {{id: {EID}, base: 'BASE', set: {{place: {place}}}}}\n"


def add(place):
    return ("  - add:\n      section: '196104'\n      entry: {id: cal.1961-04-29.fx, when: Apr. 29, date: '1961-04-29', "
            f"thread: cuba-bay-of-pigs, c: An event., n: A note., place: {place}}}\n")


def test_edit_unknown_key(tmp_path):
    assert run(tmp_path, edit("nowhere-zz")) == [f"{EID}: {UNKNOWN}"]


def test_edit_known_key_and_list(tmp_path):
    assert run(tmp_path, edit("washington")) == []
    assert run(tmp_path, edit("[washington, moscow]")) == []


def test_edit_list_with_an_unknown_key(tmp_path):
    assert run(tmp_path, edit("[washington, nowhere-zz]")) == [f"{EID}: {UNKNOWN}"]


def test_edit_three_keys(tmp_path):
    assert run(tmp_path, edit("[washington, moscow, washington]")) == \
        [f"{EID}: place: a gazetteer key, or a list of two [place]"]


def test_edit_key_the_patch_adds(tmp_path):
    assert run(tmp_path, UPPERVILLE + edit("upperville-va")) == []
    assert run(tmp_path, edit("upperville-va")) == \
        [f"{EID}: " + UNKNOWN.replace("nowhere-zz", "upperville-va")]


def test_add_unknown_key(tmp_path):
    assert run(tmp_path, add("nowhere-zz")) == [f"cal.1961-04-29.fx: {UNKNOWN}"]


def test_add_keys_of_the_tree_and_the_patch(tmp_path):
    assert run(tmp_path, UPPERVILLE + add("[upperville-va, washington]")) == []


ENTRY_PROBLEMS = [
    ({}, []),
    ({"place": "washington"}, []),
    ({"place": ["washington", "moscow"]}, []),
    ({"place": "nowhere-zz"}, [UNKNOWN[:-len(" [place]")]]),
    ({"place": []}, ["place: a gazetteer key, or a list of two"]),
    ({"place": ["washington", "moscow", "washington"]}, ["place: a gazetteer key, or a list of two"]),
]


@pytest.mark.parametrize("e,want", ENTRY_PROBLEMS)
def test_entry_problems(e, want):
    places.PENDING.clear()
    assert places.entry_problems(dict(e, id="cal.x")) == want
