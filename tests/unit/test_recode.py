"""tools/places/recode.py (ruling 67: the nations' tags to ISO 3166-1's codes of 1974, the old ids kept as aliases),
on small texts and a small tree of the test's own; and the code's reading of an old id as its polity's (vis.aliases,
canon, tag_canon; store.normalize_entry; placepages.moved; merge's tag op)."""
import importlib.util
import os

import pytest

from bib import merge, placepages as pp, store, vis

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    "recode", os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools", "places", "recode.py"))
recode = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recode)

REGISTER = """# The polities (a test's).

# Top level (§2): us, ussr, prc, fr, frg, uk; the rest under Other; org: an organization (§2: no polity by default).
polities:
  us: {name: 'United States', tag: 'US', top: true}
  frg: {name: 'Germany (the Federal Republic)', tag: 'FRG', top: true}
  drv: {name: 'Democratic Republic of Vietnam', tag: 'DRV', until: '1976-07-02', then: srv}
  srv: {name: 'Socialist Republic of Vietnam', tag: 'SRV', from: '1976-07-02'}
  cuba: {name: 'Cuba', tag: 'CUBA'}
  laos: {name: 'Laos', tag: 'LAOS'}
  pathet-lao: {name: 'Pathet Lao', tag: 'PATHET-LAO', ruling: 'laos is the Royal Lao state'}
  norway: {name: 'Norway', tag: 'NORWAY'}
  un: {name: 'United Nations', tag: 'UN', org: true}

threads:
  cuba: [cuba, us]
  laos: {polities: [laos, us, drv], doubtful: 'cuba, laos'}

places:
  'state:*': [us]
  'place:plain-of-jars': [laos]

names:
  castro-fidel: {polity: cuba, basis: 'kja III.J: Prime Minister of Cuba'}
  adenauer-konrad: [{polity: frg, until: '1963-10-16'}, {polity: frg, private: true, from: '1963-10-16'}]
  unknown-x: {polity: '?', basis: roster}
"""


# ---------------------------------------------------------------- the register's text

def test_register_rows():
    text, n = recode.recode_register(REGISTER)
    assert "  de: {name: 'Germany (the Federal Republic)', tag: 'DE', aliases: [frg], top: true}" in text
    assert "  cu: {name: 'Cuba', tag: 'CU', aliases: [cuba]}" in text
    assert "  'no': {name: 'Norway', tag: 'NO', aliases: [norway]}" in text          # bare, YAML reads false
    assert "  us: {name: 'United States', tag: 'US', top: true}" in text              # kept, no alias
    assert "  pathet-lao: {name: 'Pathet Lao', tag: 'PATHET-LAO', ruling: 'laos is the Royal Lao state'}" in text
    assert "# Top level (§2): us, ussr, prc, fr, de, uk; the rest" in text
    assert "  cuba: [cu, us]" in text                                                 # a thread's slug stays
    assert "  laos: {polities: [la, us, drv], doubtful: 'cuba, laos'}" in text       # and its quoted words
    assert "  'place:plain-of-jars': [la]" in text
    assert "  castro-fidel: {polity: cu, basis: 'kja III.J: Prime Minister of Cuba'}" in text
    assert "[{polity: de, until: '1963-10-16'}, {polity: de, private: true, from: '1963-10-16'}]" in text
    assert "{polity: '?', basis: roster}" in text
    assert n == 11
    assert recode.recode_register(text) == (text, 0)                                  # a second run: nothing


def test_register_loads():
    d = store._parse_yaml("x.yaml", recode.recode_register(REGISTER)[0])
    assert list(d["polities"]) == ["us", "de", "drv", "srv", "cu", "la", "pathet-lao", "no", "un"]
    assert d["polities"]["no"]["aliases"] == ["norway"] and d["polities"]["drv"]["then"] == "srv"


# ---------------------------------------------------------------- tags

@pytest.mark.parametrize("old, new", [
    ("tags: [polity:cuba, name:castro-fidel]", "tags: [polity:cu, name:castro-fidel]"),
    ("tags: [polity:congo-brazzaville, polity:congo]", "tags: [polity:cg, polity:zr]"),
    ("tags: [vis:only:ussr+cuba@B-D]", "tags: [vis:only:ussr+cu@B-D]"),
    ("tags: [vis:from:frg:1962-02-10@A]", "tags: [vis:from:de:1962-02-10@A]"),
    ("tags: [vis:frame:gdr]", "tags: [vis:frame:ddr]"),
    ("tags: [polity:prc, vis:only:prc+drv]", "tags: [polity:prc, vis:only:prc+drv]"),   # kept
    ("tags: [polity:norway]", "tags: [polity:no]"),                                       # no quotes in a tag
    ("thread: cuba\n  tags: [name:cuba-x, place:laos-x]", "thread: cuba\n  tags: [name:cuba-x, place:laos-x]"),
    ("a `polity:` tag", "a `polity:` tag"),
])
def test_tags(old, new):
    assert recode.recode_tags(old)[0] == new


# ---------------------------------------------------------------- the other registers

def test_gazetteer():
    text = ("- key: vientiane\n  name: Vientiane\n  in: laos\n- key: alexandria\n  in:\n    - uar\n    - syria\n"
            "- key: x\n  in: [cuba, us]\n- key: oslo\n  in: norway\n- key: y\n  st: NY\n")
    got, n = recode.recode_gazetteer(text)
    assert got == ("- key: vientiane\n  name: Vientiane\n  in: la\n- key: alexandria\n  in:\n    - uar\n    - sy\n"
                   "- key: x\n  in: [cu, us]\n- key: oslo\n  in: 'no'\n- key: y\n  st: NY\n") and n == 4


def test_registry():
    text = ("series:\n  - {key: bt, name: 'Bundestag', polity: frg, kind: official, privity: [frg, us], cards: [w.cuba]}\n"
            "frus_parties:\n  'frus1961-63v10/d1': [us, cuba]\n  'frus1964-68v21/d9': [us, south-arabia]\n"
            "publishers:\n  'Ullstein': frg\n  'Charles Scribner''s Sons': us\n"
            "works:\n  w.a: {kind: memoir, country: gdr, year: '1970'}\n  w.cuba: {kind: scholarship, country: '?'}\n")
    got, n = recode.recode_registry(text)
    assert "polity: de, kind: official, privity: [de, us], cards: [w.cuba]}" in got
    assert "[us, cu]" in got and "[us, fsa]" in got                     # a state gone before 1974: three letters
    assert "  'Ullstein': de\n  'Charles Scribner''s Sons': us\n" in got
    assert "country: ddr" in got and "w.cuba: {kind: scholarship, country: '?'}" in got and n == 6


def test_pages_plan():
    text = "places:\n  cuba:\n  - from: '1960-01-01'\n    page: places-cuba-1960\n  drv:\n    page: places-drv-1960\n"
    assert recode.recode_pages(text) == ("places:\n  cu:\n  - from: '1960-01-01'\n    page: places-cu-1960\n"
                                         "  drv:\n    page: places-drv-1960\n", 2)


# ---------------------------------------------------------------- the code's literals

CODE = '''"""Doc: `vis:only:ussr+cuba`."""
TOP = ("us", "frg", "uk")
FOLD = {"nlf": ("drv", "rvn"), "pathet-lao": ("laos",)}
WORDS = {"laos": ["Lao"], "cuba": ["Castro"]}
THREADS = {"cuba": ["cuba", "us"], "laos": {"polities": ["laos"], "doubtful": "the kingdom"}}
NATIONS = [(r"Cuban", "cuba"), (r"Malta", "malta")]
S("cuba-press", "the Cuban press", "cuba", "press")
POLS = {"polities": {"laos": {"name": "Laos", "tag": "LAOS"}}, "names": {"x": {"polity": "laos"}},
        "threads": {"laos": ["laos"]}}
YML = """polities:
  laos: {name: 'Laos', tag: 'LAOS'}
"""


def _map(k, s):
    return k == "nation" and s in ("rvn", "laos")


def test():
    assert w["nation"] == {"laos"}
    assert other == {"laos"}
'''
RULES = [("all", "TOP"), ("all", "FOLD"), ("keys", "WORDS"), ("values", "THREADS"), ("item", "NATIONS", 1),
         ("arg", "S", 2), ("register", "POLS"), ("yaml", "YML"), ("func-tuple", "_map"), ("asserts", "nation"),
         ("text", "vis:only:ussr+cuba", "vis:only:ussr+cu")]


def test_python_literals():
    got, n, missing = recode.recode_python(CODE, RULES)
    assert not missing
    assert 'TOP = ("us", "de", "uk")' in got and '"pathet-lao": ("la",)' in got
    assert 'WORDS = {"la": ["Lao"], "cu": ["Castro"]}' in got
    assert 'THREADS = {"cuba": ["cu", "us"], "laos": {"polities": ["la"], "doubtful": "the kingdom"}}' in got
    assert '(r"Cuban", "cu"), (r"Malta", "mt")' in got                    # an id with no row in the register too
    assert 'S("cuba-press", "the Cuban press", "cu", "press")' in got
    assert '{"la": {"aliases": ["laos"], "name": "Laos", "tag": "LA"}}' in got and '{"polity": "la"}' in got
    assert '"threads": {"laos": ["la"]}' in got
    assert "  la: {name: 'Laos', tag: 'LA', aliases: [laos]}" in got
    assert 's in ("rvn", "la")' in got and 'w["nation"] == {"la"}' in got and 'other == {"laos"}' in got
    assert "`vis:only:ussr+cu`" in got
    again = recode.recode_python(got, RULES)
    assert again[0] == got and again[2] == []                             # idempotent; the text rule's new form found


def test_python_missing_rule():
    assert recode.recode_python("X = 1\n", [("text", "nowhere", "else")])[2] == ["text 'nowhere': found in neither form"]
    assert recode.recode_python("X = 1\n", [("all", "TOP")])[2] == ["('all', 'TOP'): its name is not in the file"]


# ---------------------------------------------------------------- the pass on a small tree

def _tree(tmp_path):
    (tmp_path / "sources").mkdir()
    (tmp_path / "sources" / "polities.yaml").write_text(REGISTER, encoding="utf-8")
    (tmp_path / "lists" / "cal").mkdir(parents=True)
    (tmp_path / "lists" / "cal" / "196104.yaml").write_text(
        "entries:\n- id: cal.1961-04-17.cuba\n  thread: cuba\n  tags: [polity:cuba, vis:only:us+cuba@A]\n"
        "- id: cal.1961-04-18.x\n  tags: [polity:prc]\n", encoding="utf-8")
    (tmp_path / "inbox").mkdir()
    return tmp_path


def test_dry_run_writes_nothing(tmp_path, capsys):
    root = _tree(tmp_path)
    before = (root / "lists" / "cal" / "196104.yaml").read_text(encoding="utf-8")
    assert recode.main(["--root", str(root)]) == 0
    out = capsys.readouterr().out
    assert "     11  sources/polities.yaml" in out and "      2  lists/cal/" in out and "a dry run" in out
    assert (root / "lists" / "cal" / "196104.yaml").read_text(encoding="utf-8") == before


def test_apply_and_again(tmp_path, capsys):
    root = _tree(tmp_path)
    (root / "inbox" / "2026-11-28-x.yaml").write_text("patch: x\n", encoding="utf-8")
    assert recode.main(["--root", str(root), "--apply"]) == 1               # a patch waits
    assert "polity:cuba" in (root / "lists" / "cal" / "196104.yaml").read_text(encoding="utf-8")
    os.remove(root / "inbox" / "2026-11-28-x.yaml")
    assert recode.main(["--root", str(root), "--apply"]) == 0
    assert (root / "lists" / "cal" / "196104.yaml").read_text(encoding="utf-8") == (
        "entries:\n- id: cal.1961-04-17.cuba\n  thread: cuba\n  tags: [polity:cu, vis:only:us+cu@A]\n"
        "- id: cal.1961-04-18.x\n  tags: [polity:prc]\n")
    capsys.readouterr()
    assert recode.plan(str(root)) == []                                     # a second run finds nothing


def test_the_codes():
    new = [n for _, n, _ in recode.TABLE]
    assert len(new) == len(set(new))                                         # no two polities share a code
    assert not set(recode.CODES.values()) & set(recode.CODES)              # no new code is an old id
    assert all(len(n) == 2 for o, n in recode.CODES.items() if o != "gdr")   # the standard's two letters; ddr ruled
    assert set(recode.EXTRA.values()).isdisjoint(new)


# ---------------------------------------------------------------- the code reads an old id as its polity's

@pytest.fixture
def recoded(monkeypatch, tmp_path):
    """The register after the change: the test's REGISTER recoded, as vis reads it."""
    p = tmp_path / "polities.yaml"
    p.write_text(recode.recode_register(REGISTER)[0], encoding="utf-8")
    monkeypatch.setattr(vis, "POL", str(p))
    monkeypatch.setattr(vis, "_cache", {})
    pp.reset()
    yield
    pp.reset()


def test_aliases(recoded):
    assert vis.aliases() == {"frg": "de", "cuba": "cu", "laos": "la", "norway": "no"}
    assert vis.canon("norway") == "no" and vis.canon("prc") == "prc" and vis.canon(None) is None
    assert vis.canon_tag("polity:frg") == "polity:de" and vis.canon_tag("name:cuba-x") == "name:cuba-x"
    assert vis.canon_tag("vis:from:frg:1962-02-10@A") == "vis:from:de:1962-02-10@A"
    assert vis.canon_tag("vis:only:ussr+cuba") == "vis:only:ussr+cu"
    assert vis.person_polity("castro-fidel", "1962-01-01") == "cu"
    assert vis.thread_polities(None, "laos") == ["la", "us", "drv"]
    assert vis.is_org("un") and vis.tag_code("cuba") == "CU"


def test_old_ids_read_on_loading(recoded):
    e = store.normalize_entry({"id": "x", "tags": ["polity:cuba", "polity:cu", "vis:only:us+frg@A", "state:la"]})
    assert e["tags"] == ["polity:cu", "vis:only:us+de@A", "state:la"]                 # the State's code untouched
    assert pp.tag_name("polity:cuba") == "Cuba" and pp.tag_errors({"tags": ["polity:laos"]}) == []
    assert vis.rulings({"tags": ["vis:only:us+cuba"]})[0]["pols"] == {"us", "cu"}
    assert vis.tag_polities(["polity:laos"], "1962-01-01")[0] == ["la"]


def test_without_aliases_nothing_changes(monkeypatch, tmp_path):
    p = tmp_path / "polities.yaml"
    p.write_text(REGISTER, encoding="utf-8")
    monkeypatch.setattr(vis, "POL", str(p))
    monkeypatch.setattr(vis, "_cache", {})
    assert vis.tag_canon() is None and store.polity_canon() is None
    assert store.normalize_entry({"id": "x", "tags": ["polity:cuba"]})["tags"] == ["polity:cuba"]


def test_nation_words_keep_the_old_id(recoded):
    assert pp.nation_words("cu").search("The Cuban note.") and pp.nation_words("cu").search("CUBA")
    assert not pp.nation_words("no").search("NO answer.")          # a two-letter code is no word of the line
    assert pp.nation_words("de").search("the FRG's note")           # the old code still the nation's


def test_old_page_addresses(recoded):
    got = {("nation", "cu"): {"page": "places-cu", "name": "Cuba"}, ("city", "havana"): {"page": "places-havana"}}
    assert pp.moved(got) == {"places-cuba": got[("nation", "cu")]}


def test_tag_op_removes_by_an_old_id(recoded, monkeypatch):
    cur = {"id": "cal.x", "tags": ["polity:cu", "name:castro-fidel"]}
    sec = type("S", (), {"entries": [cur]})()
    monkeypatch.setattr(merge, "_locate", lambda series, eid, report: (None, sec, cur))
    rep, touched = merge.Report(), set()
    merge.op_tag(None, {"id": "cal.x", "remove": ["polity:cuba"], "add": ["polity:frg"]}, "t", rep, touched)
    assert sec.entries[0]["tags"] == ["name:castro-fidel", "polity:de"]
