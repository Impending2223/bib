"""The register (sources/people.yaml; the owner, Nov. 22, 2026: "Can't we just give the name register and start
going?"): the fourth source of name entries. lives.people reads it; a second man of one name keeps his own key; the
'Names:' linker settles a token by its tag; check holds the keys and the names (lives.register_problems). On the
fixture, with a register written for each test."""
import pytest

from bib import lives, store
from bib.build import Linker


@pytest.fixture
def register(tmp_path, monkeypatch):
    def use(text):
        p = tmp_path / "people.yaml"
        p.write_text(text, encoding="utf-8")
        monkeypatch.setattr(lives, "register_path", lambda: str(p))
        lives._CACHE.clear()
        lives._REG.clear()
        return store.Series()
    yield use
    lives._CACHE.clear()
    lives._REG.clear()


ROWS = """yang-shangkun: {name: Yang Shangkun, chars: 杨尚昆, polity: prc}
feng-xuan: {name: Feng Xuan, chars: 冯铉}
feng-xuan-2: {name: Feng Xuan, chars: 冯弦}
kong-yuan: {name: Kong Yuan}
"""


def by_key(series):
    return {lives.key_of(p["name"]): p for p in lives.people(series)}


def test_key_of_a_second_man(register):
    register(ROWS)
    assert lives.key_of("Feng Xuan 冯弦") == "feng-xuan-2"
    assert lives.key_of("Feng Xuan 冯铉") == "feng-xuan"
    assert lives.key_of("Rusk, Dean") == "rusk-dean"            # every other name its own
    assert lives.register_name({"name": "Kong Yuan"}) == "Kong Yuan"


def test_people_reads_the_register(register):
    ps = by_key(register(ROWS))
    y = ps["yang-shangkun"]
    assert y["reg"] and y["name"] == "Yang Shangkun 杨尚昆" and "Yang Shangkun" in y["names"]
    assert ps["kong-yuan"]["name"] == "Kong Yuan"
    # two men of one name: each by his characters alone, the bare name neither's
    assert ps["feng-xuan"]["names"] == {"Feng Xuan 冯铉"} and ps["feng-xuan-2"]["names"] == {"Feng Xuan 冯弦"}
    assert "rusk-dean" in ps and not ps["rusk-dean"].get("reg")


def test_a_name_as_written_is_one_man(register):
    ps = by_key(register("le-duan: {name: Lê Duẩn}\n"))
    p = ps["le-duan"]                                           # Part III's, the register's row joined to it
    assert not p.get("reg") and {r for _, r in p["ranks"]} == {0, 4}


def test_the_linker_settles_a_token_by_its_tag(register):
    series = register(ROWS)
    lk = Linker(series)
    hit = lk.names_resolved(["Yang Shangkun"], {"yang-shangkun"})[0]
    assert hit and hit[1].endswith("#yang-shangkun")
    assert lk.names_resolved(["Feng Xuan"], {"feng-xuan-2"})[0][1].endswith("#feng-xuan-2")
    assert lk.names_resolved(["Yang Shangkun"], set())[0] is None      # untagged: not guessed


def problems(series):
    return [m for w, m in lives.register_problems(series)]


def test_a_good_register_passes(register):
    assert problems(register(ROWS.replace(", polity: prc", ""))) == []


@pytest.mark.parametrize("text,want", [
    ("kong-yuan: {name: Kong Yuan}\nkong-yuan: {name: Kong Yuan}\n", "kong-yuan: the key 2 times"),
    ("kong: {name: Kong Yuan}\n", "kong: the key is the name's own (kong-yuan)"),
    ("kong-yuan-2: {name: Kong Yuan}\n", None),                        # a second man's key needs no first here
    ("kong-yuan: {name: 'Kong, Yuan'}\n", "kong-yuan: the name as the calendar writes it, in its own order"),
    ("kong-yuan: {name: Kong Yuan, chars: Kong 孔原}\n", "kong-yuan: chars: his characters alone"),
    ("kong-yuan: {name: Kong Yuan, polity: nowhere}\n", "kong-yuan: polity 'nowhere' is not in sources/polities.yaml"),
    ("kong-yuan: {name: Kong Yuan, born: 1906}\n", "kong-yuan: only name, chars, polity, apart (born)"),
    ("kong-yuan: {name: Kong Yuan}\nkong-yuan-2: {name: Kong Yuan}\n", "kong-yuan-2: the same man as kong-yuan"),
    ("rusk: {name: Rusk}\n", "rusk: 'Rusk' is a form of rusk-dean"),        # a surname another source holds
    ("pham-van-dong: {name: Pham Van Dong}\n", "pham-van-dong: 'Pham Van Dong' is a form of pham-van-dong"),
    ("pham-van-dong: {name: Pham Van Dong}\n", "pham-van-dong: the key of another person"),
])
def test_problems(register, text, want):
    got = problems(register(text))
    if want is None:
        assert got == []
    else:
        assert any(m.startswith(want) for m in got), got


def test_apart_names_another_man(register):
    got = problems(register("pham-van-dong-2: {name: Pham Van Dong}\n"))
    assert got == ["pham-van-dong-2: 'Pham Van Dong' is a form of pham-van-dong, whom another source holds (one man: "
                   "leave the row out; another: apart)"]
    assert problems(register("pham-van-dong-2: {name: Pham Van Dong, apart: [pham-van-dong]}\n")) == []
    assert problems(register("pham-van-dong-2: {name: Pham Van Dong, apart: [pham-van-dong, nobody-zz]}\n")) == [
        "pham-van-dong-2: apart: nobody-zz names no person"]
