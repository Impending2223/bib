"""patchcheck.py STYLE 13 (Nov. 21, 2026): a `name:` tag on an entry the patch touches must be a person the series
holds, as check's lives rule holds it once merged (nine such tags reached the tree with one patch). On the fixture."""
from bib import patchcheck, store


def run(tmp_path, tags):
    series = store.Series()
    p = tmp_path / "2026-11-21-fx.yaml"
    p.write_text("patch: fx-name-tags\nby: tests\nops:\n  - add:\n      section: '196104'\n"
                 "      entry: {id: cal.1961-04-29.fx, when: Apr. 29, date: '1961-04-29', thread: cuba-bay-of-pigs, "
                 f"c: An event., n: A note., tags: [{tags}]}}\n", encoding="utf-8")
    errors, _ = patchcheck.check(series, str(p))
    return [x for x in errors if "[name-tag]" in x]


def test_unknown_person(tmp_path):
    assert run(tmp_path, "name:nobody-zz-qq") == [
        "cal.1961-04-29.fx: tag name:nobody-zz-qq names no person (a name entry's key, or leave the person in c untagged) [name-tag]"]


def test_no_name_tags(tmp_path):
    assert run(tmp_path, "polity:us") == []
