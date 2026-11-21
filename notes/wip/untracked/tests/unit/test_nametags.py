"""nametags.py (Nov. 21, 2026, the owner: "Please do build the missing name tag check and run the sweep."): a person a
calendar entry's `c` names, whole or by a listed form, without his `name:` tag. Its pure parts on tables of inputs,
the forms' table on persons given by hand, and patch-check's STYLE 14 on the fixture."""
import pytest

from bib import lives, nametags as N, patchcheck, store


INDEX = {}
for form, key in [("Mao Zedong", "mao-zedong"), ("Chairman Mao", "mao-zedong"), ("Ho Chi Minh", "ho-chi-minh"),
                  ("Dean Rusk", "rusk-dean"), ("Harry F. Byrd", "byrd-harry-f"), ("Harry F. Byrd, Jr.", "byrd-harry-f-jr"),
                  ("Madame Nhu", "tran-le-xuan"), ("John F. Kennedy", "kennedy-john-f"), ("Robert Lee", "lee-robert"),
                  ("Chiang Kai-shek", "chiang-kai-shek"), ("U Thant", "u-thant")]:
    INDEX.setdefault(form.split()[0].rstrip("."), []).append((form, key))
for v in INDEX.values():
    v.sort(key=lambda x: -len(x[0]))


def keys(text):
    return [(text[a:b], k) for a, b, k in N.hits(text, INDEX)]


@pytest.mark.parametrize("text,want", [
    ("Rusk to Hồ Chí Minh, a letter.", [("Hồ Chí Minh", "ho-chi-minh")]),          # with its diacritics
    ("Dean Rusk and Ho Chi Minh's reply.", [("Dean Rusk", "rusk-dean"), ("Ho Chi Minh", "ho-chi-minh")]),
    ("Chairman Mao Zedong speaks.", [("Mao Zedong", "mao-zedong")]),                 # the longer form, a capital after
    ("Zhou with Chairman Mao.", [("Chairman Mao", "mao-zedong")]),
    ("Madame Nhu in Rome.", [("Madame Nhu", "tran-le-xuan")]),
    ("Harry F. Byrd, Jr., votes no.", [("Harry F. Byrd, Jr.", "byrd-harry-f-jr")]),  # the son, not the father
    ("Harry F. Byrd Jr. votes no.", []),                                            # a suffix after: a longer name
    ("Secretary General U Thant", [("U Thant", "u-thant")]),
    ("When U Thant arrives", [("U Thant", "u-thant")]),                             # a sentence's head before it
])
def test_hits(text, want):
    assert keys(text) == want


@pytest.mark.parametrize("text", [
    "The troops of the Ho Chi Minh Trail.",          # a place named for him
    "Hồ Chí Minh City.",
    "arm yourselves with Mao Zedong Thought",        # an organ named for him
    "publicize Mao Zedong thought.",
    "the label \"Thought of Mao Zedong\"",
    "Mao Zedong 毛泽东's thought",
    "the study of Chairman Mao's works",
    "the war criminals of the Chiang Kai-shek clique",
    "on the destroyer the John F. Kennedy.",         # an article before: a thing named for him
    "the USS John F. Kennedy sails",
    "Mrs. John F. Kennedy and the children",         # his wife
    "the John F. Kennedy Center for the Performing Arts",   # a capital after
    "*Quotations from Chairman Mao* reprinted",      # an italic title
    "and Henry Robert Lee spoke",                    # a given name before: a longer name
    "General Robert E. Lee",                         # not the form
    "Dean Rusking",                                  # not a whole word
])
def test_not_a_person_named(text):
    assert keys(text) == []


def test_fold_keep_keeps_case_and_length():
    for s in ["Hồ Chí Minh", "Ngô Đình Diệm", "Ưng Văn Khiêm", "Teng Hsiao-p’ing", "plain"]:
        f = N.fold_keep(s)
        assert len(f) == len(s) and f.isascii()
    assert N.fold_keep("Ngô Đình Diệm") == "Ngo Dinh Diem"


@pytest.mark.parametrize("name,want", [
    ("Rusk, Dean", ["Dean Rusk"]),
    ("Byrd, Harry F., Jr.", ["Harry F. Byrd, Jr.", "Harry F. Byrd Jr."]),
    ("Gravel, Maurice R. (Mike)", ["Maurice R. Gravel"]),
    ("Smith,", []),                                   # a surname alone gives none
])
def test_running_forms(name, want):
    assert N.running_forms(name) == want


def test_other_chars():
    assert N.other_chars("陳逸", {"陈毅"})             # another Chen Yi
    assert N.other_chars("陳逸", {"陈毅", "陳毅"})     # his surname's 陳 is the marshal's too: the given name decides
    assert not N.other_chars("陳毅", {"陈毅"})         # the marshal, in the old characters
    assert not N.other_chars("陈毅", set()) and not N.other_chars("", {"陈毅"})


def test_table_drops_forms_two_persons_fit(monkeypatch):
    people = [{"name": n, "names": {n}} for n in
              ["Kennedy, John F.", "Kennedy, John", "Rusk, Dean", "Mao Zedong", "Lee, Robert", "Lee, Robert E."]]
    monkeypatch.setattr(lives, "everyone", lambda series: people)
    monkeypatch.setattr(lives, "name_forms", lambda name: {"Mao Zedong": ["Mao Zedong", "Chairman Mao",
                                                                          "Mao, Zedong"]}.get(name, [name]))
    monkeypatch.setattr(N, "VIET_PLACES", lambda: [])
    index, names = N._table(object())
    forms = {f: k for v in index.values() for f, k in v}
    assert forms["Dean Rusk"] == "rusk-dean" and forms["Chairman Mao"] == "mao-zedong"
    assert forms["John F. Kennedy"] == "kennedy-john-f"
    assert "John Kennedy" not in forms               # a FRUS John fits John F.'s token too
    assert "Robert Lee" not in forms and forms["Robert E. Lee"] == "lee-robert-e"
    assert "Mao, Zedong" not in forms                # a list's inverted form


def test_entry_findings_tags_and_ok():
    e = {"id": "cal.1965-01-01.x", "c": "Dean Rusk to U Thant.", "tags": ["name:rusk-dean"]}
    assert N.entry_findings(e, INDEX, {}) == [("u-thant", "U Thant")]
    e["tags"].append("ok:name-untagged")
    assert N.entry_findings(e, INDEX, {}) == []
    assert N.entry_findings({"id": "cal.thread.x", "c": "U Thant"}, INDEX, {}) == []
    # a FRUS form joined in another's entry stands for him
    assert N.entry_findings({"id": "cal.1965-01-01.y", "c": "U Thant", "tags": ["name:thant-u"]},
                            INDEX, {"thant-u": "u-thant"}) == []


def run(tmp_path, c, tags="polity:us"):
    series = store.Series()
    p = tmp_path / "2026-11-21-fx.yaml"
    p.write_text("patch: fx-untagged\nby: tests\nops:\n  - add:\n      section: '196104'\n"
                 "      entry: {id: cal.1961-04-29.fx, when: Apr. 29, date: '1961-04-29', thread: cuba-bay-of-pigs, "
                 f"c: '{c}', n: A note., tags: [{tags}]}}\n", encoding="utf-8")
    errors, warnings = patchcheck.check(series, str(p))
    return [x for x in warnings if "[name-untagged]" in x]


def test_patch_check_warns_on_an_add(tmp_path):
    w = run(tmp_path, "Zhou Enlai meets Prince Souphanouvong.", "name:zhou-enlai")
    assert w == ["cal.1961-04-29.fx: c names 'Prince Souphanouvong', Souphanouvong, without the tag "
                 "name:souphanouvong: add it, and the name to 'Names:' (the names op), or tag ok:name-untagged "
                 "[name-untagged]"]


def test_patch_check_tagged_or_silenced(tmp_path):
    assert run(tmp_path, "Zhou Enlai meets Prince Souphanouvong.", "name:zhou-enlai, name:souphanouvong") == []
    assert run(tmp_path, "Zhou Enlai meets Prince Souphanouvong.", "name:zhou-enlai, ok:name-untagged") == []
