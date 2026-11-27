"""placepages.py STYLE 8 and 9, check's and patch-check's hold on the place tags (ruling 67; notes/proposals/
place-pages.md, "The States' tags"): a `state:` tag not a postal code and a `polity:` tag not in the register are
errors; a polity, State or city tag nothing else in the entry supports is a warning, [polity-tag], [state-tag],
[city-tag], silenced by `ok:<rule>`; patch-check prints each place tag a patch adds with what it names. On the
fixture, with a small register of the test's own (the fixture has none)."""
import pytest

from bib import check, patchcheck, placepages as pp, store, vis

REGISTER = {
    "polities": {"us": {"name": "United States", "tag": "US"}, "prc": {"name": "China (the People's Republic)", "tag": "PRC"},
                 "laos": {"name": "Laos", "tag": "LAOS"}, "switzerland": {"name": "Switzerland", "tag": "SWITZERLAND"},
                 "rvn": {"name": "Republic of Vietnam", "tag": "RVN"}, "drv": {"name": "Democratic Republic of Vietnam",
                 "tag": "DRV"}, "nlf": {"name": "NLF", "tag": "NLF", "folded": "drv"},
                 "bulgaria": {"name": "Bulgaria", "tag": "BULGARIA"}, "un": {"name": "United Nations", "org": True}},
    "names": {"souvanna-phouma": {"polity": "laos"}},
    "places": {"state:*": ["us"], "city:*": ["us"]},
    "threads": {"laos": ["laos", "us"]},
}


@pytest.fixture
def register(monkeypatch):
    monkeypatch.setattr(vis, "polities", lambda: REGISTER)
    pp.reset()
    yield
    pp.reset()


@pytest.fixture(scope="module")
def series():
    return store.Series()


@pytest.fixture(scope="module")
def cal(series):
    return series.lists["cal"]


def E(**kw):
    e = {"id": "cal.1961-04-01.x", "when": "Apr. 1", "date": "1961-04-01", "thread": "none", "c": "A meeting."}
    e.update(kw)
    return e


def rules(cal, e):
    return [r for r, _ in pp.tag_findings(cal, e)]


# ---------------------------------------------------------------- errors: tags that name nothing

def test_state_codes(register):
    assert pp.tag_errors(E(tags=["state:al", "state:dc", "state:wy"])) == []
    errs = pp.tag_errors(E(tags=["state:california", "state:IL", "state:zz"]))
    assert len(errs) == 3
    assert errs[0].startswith("state:california: not a State's postal code") and errs[0].endswith("write state:ca")
    assert errs[1].endswith("write state:il")
    assert "write" not in errs[2]


def test_polity_in_the_register(register):
    assert pp.tag_errors(E(tags=["polity:prc", "polity:un"])) == []
    usa, spain = pp.tag_errors(E(tags=["polity:usa", "polity:spain"]))
    assert usa == "polity:usa: no such polity in sources/polities.yaml (polity:us, United States?)"
    assert spain.endswith("add its row there first")


def test_no_register_no_polity_errors(monkeypatch):
    monkeypatch.setattr(vis, "polities", lambda: {"polities": {}, "names": {}, "places": {}, "threads": {}})
    assert pp.tag_errors(E(tags=["polity:anything"])) == []


def test_check_holds_them(series, cal, register):
    sec = next(iter(cal.walk()))
    got = [(lvl, rule) for lvl, _, rule in check.entry_problems(series, cal, sec, E(tags=["polity:usa"], place="chicago"))
           if rule in ("place-tags", "polity-tag", "state-tag", "city-tag")]
    assert got == [(check.ERROR, "place-tags")]
    got = [(lvl, rule) for lvl, _, rule in check.entry_problems(series, cal, sec, E(tags=["state:la"], place="chicago"))
           if rule in ("place-tags", "polity-tag", "state-tag", "city-tag")]
    assert got == [(check.WARN, "state-tag")]


# ---------------------------------------------------------------- polity: what supports a nation's tag

def test_polity_supported(cal, register):
    assert rules(cal, E(place="peking", tags=["polity:prc"])) == []                  # its place
    assert rules(cal, E(tags=["polity:laos", "name:souvanna-phouma"])) == []         # its people
    assert rules(cal, E(thread="laos", tags=["polity:laos"])) == []                  # its thread
    assert rules(cal, E(tags=["polity:prc", "vis:only:prc"])) == []                  # a vis: ruling
    assert rules(cal, E(tags=["polity:switzerland"], c="Talks at Geneva.")) == []     # a place its line names
    assert rules(cal, E(tags=["polity:bulgaria"], c="Zhou receives the Bulgarian delegation.")) == []
    assert rules(cal, E(tags=["polity:laos"], c="The Laotian question.")) == []      # its name with a suffix
    assert rules(cal, E(tags=["polity:prc"], c="The PRC answers.")) == []             # its code
    assert rules(cal, E(place="saigon", tags=["polity:nlf"])) == []                  # folded: the NLF's are the RVN's too
    assert rules(cal, E(tags=["polity:un"])) == []                                    # an organization: no nation
    assert rules(cal, E(tags=["polity:usa"])) == []                                   # an error, not a warning too


def test_polity_unsupported(cal, register):
    e = E(place="peking", tags=["polity:switzerland"], c="Zhou receives the Chinese delegation.")
    (rule, msg), = pp.tag_findings(cal, e)
    assert rule == "polity-tag" and msg.startswith("polity:switzerland (Switzerland): nothing in the entry gives it")
    assert rules(cal, dict(e, tags=["polity:switzerland", "ok:polity-tag"])) == []


# ---------------------------------------------------------------- state: placed elsewhere, tied by nothing

def test_state_unsupported(cal, register):
    e = E(place="chicago", tags=["state:la"], c="A delegation meets.")
    (rule, msg), = pp.tag_findings(cal, e)
    assert rule == "state-tag"
    assert msg.startswith("state:la (Louisiana): the entry is placed at Chicago, in Illinois, and no thread")
    assert rules(cal, dict(e, tags=["state:la", "ok:state-tag"])) == []
    assert rules(cal, E(place="washington", tags=["state:la"])) == ["state-tag"]      # D.C. is in no State
    assert rules(cal, E(place="geneva", tags=["state:la"])) == ["state-tag"]          # abroad


def test_state_supported(cal, register):
    assert rules(cal, E(tags=["state:la"])) == []                                     # no place: nothing to set it against
    assert rules(cal, E(place="new-orleans", tags=["state:la"])) == []                # placed in it
    assert rules(cal, E(place="alabama", tags=["state:al"])) == []                    # the State as a place
    assert rules(cal, E(place="chicago", tags=["state:la"], c="The Louisiana delegation.")) == []
    assert rules(cal, E(place="chicago", tags=["state:la"], c="Monroe, La., votes.")) == []   # the Bluebook's form
    assert rules(cal, E(place="chicago", tags=["state:la", "city:new-orleans"])) == ["city-tag"]   # a city tag in it
    assert rules(cal, E(place="washington", tags=["state:al"], thread="alabama-birmingham")) == []  # a thread of it
    assert rules(cal, E(place="washington", tags=["state:al"], c="The Court on Montgomery's buses.")) == []


# ---------------------------------------------------------------- city: placed at another city elsewhere

def test_city(cal, register):
    e = E(place="springfield-ma", tags=["city:springfield"], c="The city's election for mayor.")
    (rule, msg), = pp.tag_findings(cal, e)
    assert rule == "city-tag" and msg.startswith("city:springfield (Springfield, Ill., in Illinois): the entry is placed "
                                                 "at Springfield, Mass., in Massachusetts")
    assert rules(cal, E(place="springfield-ma", tags=["city:springfield-ma"])) == []   # its own place
    assert rules(cal, E(place="portland-me", tags=["city:portland"], c="Portland, Ore., and Portland, Me.")) == []
    assert rules(cal, E(tags=["city:chicago"])) == []                                 # no place
    assert rules(cal, E(place="washington", tags=["city:chicago"], c="Daley to the White House.")) == ["city-tag"]
    assert rules(cal, E(place="washington", tags=["city:chicago"], c="Chicago's schools.")) == []


# ---------------------------------------------------------------- what a tag names (STYLE 9), and patch-check

def test_tag_name(register):
    assert pp.tag_name("polity:switzerland") == "Switzerland"
    assert pp.tag_name("polity:un") == "United Nations (an organization)"
    assert pp.tag_name("state:la") == "Louisiana" and pp.tag_name("state:dc") == "District of Columbia"
    assert pp.tag_name("city:chicago") == "Chicago"
    assert pp.tag_name("polity:zz") is None and pp.tag_name("state:LA") is None and pp.tag_name("city:nowhere-zz") is None


EID = "cal.1961-04-30.cuba-bay-of-pigs"          # the fixture's, with no place


def test_patch_check_prints_the_names(tmp_path, register):
    series = store.Series()
    p = tmp_path / "2026-11-27-fx.yaml"
    p.write_text("patch: fx-place-tags\nby: tests\nops:\n"
                 f"  - names: {{id: {EID}, tags: ['polity:switzerland', 'state:la', 'polity:usa']}}\n", encoding="utf-8")
    tags = []
    errors, warnings = patchcheck.check(series, str(p), tags=tags)
    assert tags == [f"{EID}: polity:switzerland: Switzerland", f"{EID}: state:la: Louisiana",
                    f"{EID}: polity:usa: names nothing"]
    assert any("polity:usa: no such polity" in x for x in errors)
    assert any("polity:switzerland (Switzerland): nothing in the entry gives it" in w and "[polity-tag]" in w
               for w in warnings)
    text, err = patchcheck.report(store.Series(), str(p))
    assert err and f"  tag    {EID}: polity:switzerland: Switzerland" in text
