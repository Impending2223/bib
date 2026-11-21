"""vis.py: "Made public:" items printed in one country only (R27, the owner, Nov. 21, 2026: a Red Guard printing
makes an act public in China only; elsewhere it is public from the first printing that reached abroad, or the later
open printing). The fixture has no sources/polities.yaml or provenance.yaml: the tests give their own.
"""
import pytest

from bib import vis

POLS = {"polities": {"us": {"name": "United States", "tag": "US", "top": True},
                     "ussr": {"name": "Soviet Union", "tag": "USSR", "top": True},
                     "prc": {"name": "China (the People's Republic)", "tag": "PRC", "top": True},
                     "fr": {"name": "France", "tag": "FR", "top": True},
                     "roc": {"name": "Republic of China", "tag": "ROC"}},
        "names": {}, "places": {}, "threads": {}}
PROV = {"series": [], "frus_volumes": {}, "frus_parties": {}, "publishers": {}, "works": {}}


@pytest.fixture(autouse=True)
def registry(monkeypatch):
    monkeypatch.setattr(vis, "polities", lambda: POLS)
    monkeypatch.setattr(vis, "registry", lambda: PROV)


LOCAL = [
    ("China", "prc"),
    ("the PRC", "prc"),
    ("France", "fr"),                        # by its name in polities.yaml
    ("Republic of China", "roc"),
    ("part", None),                          # "in part, ..." names no polity
    ("1993", None),
    ("", None),
]


@pytest.mark.parametrize("name,want", LOCAL)
def test_local_polity(name, want):
    assert vis.local_polity(name) == want


def entry(mp, tags=("polity:prc", "polity:us", "polity:ussr")):
    return {"id": "cal.1967-01-08.china", "date": "1967-01-08", "thread": "china", "c": "Mao spoke to the group.",
            "n": f"Some source. {mp}", "tags": list(tags)}


MP = ("Made public: in China, *Xin Beida*, June 28, 1967 (a Red Guard tabloid); elsewhere, *Wenku* (2002).")


def test_made_public_items():
    ws = vis.made_public(entry(MP), "1967-01-08", ["prc", "us"])
    got = [(w["label"], w["pub"], w["public"], bool(w.get("local"))) for w in ws]
    assert got == [("Made public: in China, *Xin Beida*, June 28, 1967 (a Red Guard tabloid)", "prc", "1967-06-28",
                    True),
                   ("Made public: *Wenku* (2002)", "?", "2002-01-01", False)]


def test_made_public_plain_item_unchanged():
    ws = vis.made_public(entry("Made public: Drew Pearson's column, May 24, 1968."), "1967-01-08", ["us"])
    assert [(w["pub"], w["public"], w.get("local")) for w in ws] == [("?", "1968-05-24", None)]


def test_made_public_in_part_is_no_place():
    ws = vis.made_public(entry("Made public: in part, *Wenku* (2002)."), "1967-01-08", ["us"])
    assert [(w["label"], w.get("local")) for w in ws] == [("Made public: in part, *Wenku* (2002)", None)]


def pols(e):
    cls = vis.compute(None, None, e)
    assert len(cls) == 1 and cls[0]["computed"]
    return cls[0]["polities"]


def test_local_printing_public_in_china_only():
    p = pols(entry(MP))
    assert p["prc"]["P"] == [None, "1967-06-28"]              # PRC: published there, from the tabloid
    assert p["prc"]["A"] == ["1967-01-08", "1967-06-28"]
    assert p["us"]["A"] == ["1967-01-08", "2002-01-01"]       # elsewhere: from the open printing
    assert p["ussr"]["A"] == ["1967-01-08", "2002-01-01"]
    assert "P" not in p["us"]


def test_local_printing_alone_leaves_others_unpublished():
    p = pols(entry("Made public: in China, *Xin Beida*, June 28, 1967 (a Red Guard tabloid)."))
    assert p["prc"]["A"] == ["1967-01-08", "1967-06-28"]
    assert p["us"]["A"] == ["1967-01-08", None]


def test_without_the_prefix_the_tabloid_counts_everywhere():
    """The old reading, kept for an item with no "in <country>, ": any witness's date is every polity's A."""
    p = pols(entry("Made public: *Xin Beida*, June 28, 1967 (a Red Guard tabloid)."))
    assert p["us"]["A"] == ["1967-01-08", "1967-06-28"]
    assert p["prc"]["A"] == ["1967-01-08", "1967-06-28"]
