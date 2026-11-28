"""merge.combine on two calendar entries whose lines carry cut marks (tools/bib/cuts.py): the entry it leaves is
always one store.stored_form can write. Where the lines differ, KEEP's line stands with KEEP's own cuts, claim map and
variants; DROP's go into the conflict record as `theirs`, field by field, for a hand to join. (Nov. 28, 2026: the
combine of cal.1966-08-19.health and cal.1966-08-21.elections-1966 put DROP's cuts on KEEP's unmarked line and died
in stored_form.)"""
import pytest

from bib import cuts, merge, store

KEEP = "cal.1961-01-01.x"
DROP = "cal.1961-01-02.x"
OTHER = "cal.1961-01-03.x"


def _mini(root, keep, drop):
    (root / "lists" / "cal").mkdir(parents=True)
    (root / "series.yaml").write_text("lists:\n  - {key: cal, abbr: Cal.}\n", encoding="utf-8")
    (root / "lists" / "cal" / "list.yaml").write_text(
        "kind: calendar\nsections:\n  - {id: '196101', title: January 1961, file: 196101.yaml}\n", encoding="utf-8")
    other = {"id": OTHER, "date": "1961-01-03", "c": "Event 3.", "n": f"Note 3. See [[{DROP}]]."}
    store.dump_yaml({"list": "cal", "section": "196101", "entries": [keep, drop, other]},
                    str(root / "lists" / "cal" / "196101.yaml"))


@pytest.fixture
def root(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "ROOT", str(tmp_path))
    return tmp_path


def _combine(root):
    series = store.Series(str(root))
    rep, touched = merge.Report(), set()
    merge.combine(series, KEEP, DROP, "combine", rep, touched)
    for s in touched:
        series.save_section(s)
    return store.Series(str(root)), rep


def _conflicts(e):
    return {c["field"]: c for c in e.get("conflict") or [] if "field" in c}


BARE = {"id": KEEP, "date": "1961-01-01", "thread": "x",
        "c": "Ellenville, N.Y. Johnson dedicates the hospital: \"before the sun went down.\"",
        "n": "[[w.a]], 1. Names: Johnson.",
        "src": {"c": "00000000", "rows": ["w.a 1: all"]}}
MARKED = {"id": DROP, "date": "1961-01-01", "thread": "y",
          "c": "The Catskills, Johnson and Kennedy together.{1} Johnson's speech; shrieks of \"Bobby!\"{2} "
               "The headline, Jan. 4.{3}",
          "n": "[[w.b]], 2. Names: Johnson, Kennedy.",
          "src": {"c": "11111111", "rows": ["w.b 2: 1, 2, 3", "w.c 3: 1, 3"]},
          "variants": [{"unit": "2", "witness": "w.c", "reads": "cheers"}],
          "tags": ["name:kennedy", "vis:only:us@2"]}


def test_combine_a_marked_line_into_an_unmarked_one(root):
    _mini(root, dict(BARE), dict(MARKED))
    now, rep = _combine(root)                                     # raised ValueError in stored_form before the fix
    e = now.get(KEEP)[2]
    assert now.get(DROP)[2] is e                                  # DROP is an alias of KEEP
    assert e["c"] == BARE["c"] and "cuts" not in e                # KEEP's line, with KEEP's (no) cuts
    assert e["src"] == BARE["src"] and "variants" not in e        # and KEEP's own map
    assert "vis:only:us@2" not in e["tags"] and "name:kennedy" in e["tags"]
    k = _conflicts(e)
    plain, ks = cuts.strip(MARKED["c"])
    assert k["c"]["ours"] == BARE["c"] and k["c"]["theirs"] == plain
    assert k["cuts"]["ours"] is None and k["cuts"]["theirs"] == ks
    assert k["src"]["ours"] == BARE["src"] and k["src"]["theirs"] == MARKED["src"]
    assert k["variants"]["ours"] is None and k["variants"]["theirs"] == MARKED["variants"]
    assert "vis:only:us@2" in k["tags"]["theirs"] and "vis:only:us@2" not in k["tags"]["ours"]
    assert f"[[{KEEP}]]" in now.get(OTHER)[2]["n"]
    for _, x in now.lists["cal"].entries():
        store.stored_form(x)                                      # every entry writable


def test_combine_an_unmarked_line_into_a_marked_one(root):
    keep, drop = dict(MARKED, id=KEEP), dict(BARE, id=DROP)
    _mini(root, keep, drop)
    now, _ = _combine(root)
    e = now.get(KEEP)[2]
    plain, ks = cuts.strip(MARKED["c"])
    assert e["c"] == plain and e["cuts"] == ks and e["src"] == MARKED["src"]
    assert e["variants"] == MARKED["variants"] and "vis:only:us@2" in e["tags"]
    k = _conflicts(e)
    assert k["c"]["theirs"] == BARE["c"] and k["cuts"]["theirs"] is None and k["src"]["theirs"] == BARE["src"]


def test_combine_two_marked_lines_that_differ(root):
    other = dict(MARKED, id=KEEP, c="Kennedy flies in.{4} Johnson speaks.{5}",
                 src={"c": "22222222", "rows": ["w.d 4: 4, 5"]}, variants=None, tags=["name:kennedy"])
    other.pop("variants")
    _mini(root, other, dict(MARKED))
    now, _ = _combine(root)
    e = now.get(KEEP)[2]
    assert e["c"] == "Kennedy flies in. Johnson speaks." and [n for _, n in e["cuts"]] == ["4", "5"]
    assert e["src"]["rows"] == ["w.d 4: 4, 5"] and "variants" not in e
    k = _conflicts(e)
    assert set(k) >= {"c", "cuts", "src", "variants"}
    assert [n for _, n in k["cuts"]["theirs"]] == ["1", "2", "3"]


def test_combine_one_line_marked_on_one_side_only(root):
    plain, ks = cuts.strip(MARKED["c"])
    _mini(root, dict(BARE, c=plain, src=None), dict(MARKED))
    series = store.Series(str(root))
    series.get(KEEP)[2].pop("src", None)
    rep, touched = merge.Report(), set()
    merge.combine(series, KEEP, DROP, "combine", rep, touched)
    for s in touched:
        series.save_section(s)
    e = store.Series(str(root)).get(KEEP)[2]
    # the same line: DROP's cuts, map and variants fit it, and KEEP had none, so they are taken with no conflict
    assert e["c"] == plain and e["cuts"] == ks and e["src"] == MARKED["src"] and e["variants"] == MARKED["variants"]
    assert not {"c", "cuts", "src", "variants"} & set(_conflicts(e))


def test_combine_refuses_rather_than_writes_an_entry_that_cannot_be_stored(root, monkeypatch):
    _mini(root, dict(BARE), dict(MARKED))
    before = (root / "lists" / "cal" / "196101.yaml").read_text(encoding="utf-8")
    series = store.Series(str(root))
    real = store.stored_form

    def broken(e):
        if e.get("id") == KEEP and "aliases" in e:
            raise ValueError("cuts do not fit")
        return real(e)
    monkeypatch.setattr(store, "stored_form", broken)
    rep, touched = merge.Report(), set()
    merge.combine(series, KEEP, DROP, "combine", rep, touched)
    assert not touched and any("cuts do not fit" in x for x in rep.lines)
    assert series.get(DROP)[2]["id"] == DROP                     # nothing changed in memory
    assert (root / "lists" / "cal" / "196101.yaml").read_text(encoding="utf-8") == before
