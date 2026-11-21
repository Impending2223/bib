"""standing.py, STYLE 3 (the owner, Nov. 21, 2026: "Why isn't this just a normal entry?"): "As X has it:" and "As X
reports it:" open only a paper's report of a standing condition; `check` warns [report-opener] where the note cites no
newspaper, wire or broadcast. The registry is given by hand (the fixture holds no sources/provenance.yaml)."""
import pytest

from bib import standing as S, vis

REG = {"series": [
    {"key": "nyt", "kind": "press", "url": ["timesmachine.nytimes.com"], "text": ["New York Times"]},
    {"key": "weeklies", "kind": "press", "text": ["*Time*", "Newsweek"]},
    {"key": "columns", "kind": "press", "text": ["Associated Press"]},
    {"key": "cq", "kind": "press", "text": ["Congressional Quarterly"], "cards": ["w.cq-almanac"]},
    {"key": "us-archives", "kind": "archive", "url": ["www.jfklibrary.org"]},
], "works": {"w.department-of-state-bulletin": {"kind": "press"}, "w.dikotter-cultural-revolution": {"kind": "scholarship"}}}


@pytest.fixture(autouse=True)
def registry(monkeypatch):
    monkeypatch.setattr(vis, "registry", lambda: REG)


@pytest.mark.parametrize("c,want", [
    ("As the *Times* reports it: Byrd of Virginia has not endorsed the ticket.", True),
    ("As a Shanghai 上海 report has it: on a single day more than 400 cadres paraded.", True),
    ("As Shanghai 上海 reports have it: tombstones smashed.", True),
    ("As British officials in Vientiane report it: the Pathet Lao hold back.", True),
    ("As K. Godwin reports it from Shanghai 上海: Red Guards chip the Bund.", True),
    ("As the British consulate-general in Hanoi reports it, from the Czechoslovak ambassador: a malaise.", True),
    ("As the Hunan Office for Statistics reckons it, going back over the records: 2.39 million tonnes.", True),
    ("As the Fujian military control committee counts it: over 2,000 detained.", True),
    ("As Chang gives it: Taiwan's standard of living among the highest in Asia.", True),
    ("Shanghai 上海: on a single day more than 400 cadres paraded.", False),            # the normal entry
    ("British embassy in Peking to the Foreign Office: the press follows Laos.", False),
    ("As expected, the Senate passes the bill: 70 to 20.", False),                      # "As" not a report's frame
    ("Kennedy, as the *Times* reports it: no comment.", False),                          # not at the head
    ("", False),
])
def test_opener(c, want):
    assert S.opener(c) is want


@pytest.mark.parametrize("n,want", [
    ("[*New York Times*, Sept. 7, 1960](https://timesmachine.nytimes.com/timesmachine/1960/09/07/issue.html), at 1.", True),
    ("[the front page](https://timesmachine.nytimes.com/timesmachine/1960/09/07/issue.html).", True),   # the host alone
    ('[[w.dikotter-maos-great-famine]], 109. To check: "Famine and bankruptcy," *Time*, June 2, 1961.', True),
    ("Associated Press, Sept. 8, 1960.", True),
    ("[[w.department-of-state-bulletin]], 45:12.", True),                                    # a press card
    ("[[w.cq-almanac]], 1961, 300.", True),                                                  # a press series' card
    ("[[w.dikotter-cultural-revolution]], 121 n.16. To check: Shanghai Municipal Archives, Aug. 1966.", False),
    ("[a memo](https://www.jfklibrary.org/asset-viewer/x).", False),                         # an archive's host
    ("", False),
])
def test_press_cited(n, want):
    assert S.press_cited(n) is want


class _List:
    def __init__(self, kind, ents):
        self.kind, self._e = kind, ents

    def entries(self):
        return [(None, e) for e in self._e]


class _Series:
    def __init__(self, **lists):
        self.lists = lists


def test_problems():
    press = {"id": "cal.a", "c": "As the *Times* reports it: Byrd has not endorsed.",
             "n": "[*New York Times*, Sept. 7, 1960](https://timesmachine.nytimes.com/x), at 1."}
    archive = {"id": "cal.b", "c": "As a Shanghai 上海 report has it: 400 cadres paraded.",
               "n": "[[w.dikotter-cultural-revolution]], 121 n.16. To check: Shanghai Municipal Archives, Aug. 1966."}
    plain = {"id": "cal.c", "c": "Shanghai 上海: 400 cadres paraded.", "n": archive["n"]}
    other = {"id": "kja.x", "c": "As a Shanghai report has it: a list's note, not the calendar."}
    got = S.problems(_Series(cal=_List("calendar", [press, archive, plain]), kja=_List("bibliography", [other])))
    assert [w for w, _ in got] == ["cal.b"] and "report-opener" == S.RULE
    assert "normal entry" in got[0][1]


def test_tag_retired():
    """STYLE 1: the tag no longer marks anything the day view sets off; is_state reads only the retired tag."""
    assert not S.is_state({"tags": ["polity:prc", "vis:only:prc"]})
    assert not hasattr(S, "LABEL")
