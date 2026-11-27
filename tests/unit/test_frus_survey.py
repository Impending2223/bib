"""frus_survey.py (ruling 71, notes/proposals/frus-survey.md): the sorting of the uncited FRUS documents. Its pure
parts on tables of inputs: the routine headings, the head's lists of persons, the President, the persons a heading
names, the days, the sort, the links counted as cites."""
import datetime
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools", "daybook"))
import frus_survey as F  # noqa: E402


@pytest.mark.parametrize("title,placed,want", [
    ("Editorial Note", False, "editorial note"),
    ("Memorandum From Rusk to President Kennedy", True, "editorial note"),          # filed by its place
    ("Memorandum from Mann to Rusk, February 11, transmitting a memorandum from Rusk to the President", False,
     "transmittal"),
    ("Memorandum from Edwin M. Martin to Rusk, November 8, covering a memorandum from Hurwitch to Martin", False,
     "transmittal"),
    ("Memorandum from William Harvey to McCone, August 8, with attached Operation Plan", False, "transmittal"),
    ("Telegram From the Embassy in Vietnam to the Department of State", False, None),
    ("Memorandum of Conversation", False, None),
])
def test_routine(title, placed, want):
    assert F.routine(title, placed) == want


HTML = ('<h3 id="x">253. Memorandum of Conversation<sup class="nr"><a>0</a></sup></h3><div class="opener">'
        '<p class="dl r">Washington, October 18, 1962, 5 p.m.</p></div><p class="lh">SUBJECT</p>'
        '<ul class="tl subject"><li>Talks with Gromyko on Berlin</li></ul><p class="lh">PARTICIPANTS</p>'
        '<ul class="tl participants"><li><i>US</i> <ul class="tl"><li>The President</li><li>Ambassador Thompson</li>'
        '</ul></li><li><i>USSR</i> <ul class="tl"><li>Foreign Minister Gromyko<sup class="nr"><a>1</a></sup></li>'
        '</ul></li></ul><p>Mr. Gromyko said that Ball and McNamara agreed.</p><ul class="tl"><li>Dobrynin</li></ul>')


def test_head_text_takes_title_and_participants():
    h = F.head_text(HTML)
    assert "Memorandum of Conversation" in h and "Ambassador Thompson" in h and "Foreign Minister Gromyko" in h
    assert "The President" in h


def test_head_text_leaves_subject_and_body():
    h = F.head_text(HTML)
    assert "Berlin" not in h                    # the subject
    assert "Ball" not in h and "Dobrynin" not in h   # the body, and a list in it
    assert "1" not in h.split("Gromyko")[-1]    # the note's number


def test_head_text_unlabeled_list_is_body():
    html = '<h3>386. Memorandum From McNamara to President Kennedy</h3><ul class="tl"><li>1. Lemnitzer agrees</li></ul>'
    assert F.head_text(html) == "386. Memorandum From McNamara to President Kennedy"


@pytest.mark.parametrize("day,want", [
    ("1960-06-01", "eisenhower-dwight-d"), ("1961-01-20", "kennedy-john-f"), ("1963-11-21", "kennedy-john-f"),
    ("1963-11-22", "johnson-lyndon-b"), ("1969-01-19", "johnson-lyndon-b"),
])
def test_president_on(day, want):
    assert F.president_on(day)[0] == want


@pytest.mark.parametrize("head,want", [
    ("Memorandum From Secretary of Defense McNamara to President Kennedy", True),
    ("Memorandum for the President", True),
    ("The President Ambassador Thompson", True),
    ("Memorandum From the President’s Special Assistant (Bundy) to Rusk", False),
    ("Letter From the President of Brazil (Goulart)", False),
    ("Letter From President Goulart to Rusk", False),
    ("Memorandum From Vice President Johnson to Rusk", False),
    ("Memorandum to the Vice President", False),
])
def test_names_president(head, want):
    assert F.names_president(head, "Kennedy") is want


CANDS = {"wood-chalmers-b": {"Wood"}, "nolting-frederick-e-jr": {"Nolting"}, "rostow-walt-w": {"Rostow"},
         "johnson-u-alexis": {"Johnson"}, "kennedy-john-f": {"Kennedy"}, "kennedy-robert-f": {"Kennedy"},
         "de-gaulle-charles": {"de Gaulle"}, "ngo-dinh-diem": {"Diem", "Ngo Dinh Diem"}}


@pytest.mark.parametrize("head,day,want", [
    ("Letter From the Director of the Vietnam Working Group (Wood) to the Ambassador in Vietnam (Nolting)",
     "1962-10-01", {"wood-chalmers-b", "nolting-frederick-e-jr"}),
    ("Telegram From the Embassy in Vietnam to the Department of State", "1962-10-01", set()),
    ("woodland report", "1962-10-01", set()),                       # a surname whole and capitalized only
    ("Memorandum From the Deputy Under Secretary (Johnson) to Rusk", "1962-10-01",
     {"johnson-u-alexis"}),
    ("Memorandum From the Attorney General (Kennedy) to Rusk", "1962-10-01", {"kennedy-robert-f"}),
    ("Memorandum From Rusk to President Kennedy", "1962-10-01", {"kennedy-john-f"}),   # not Robert by "Kennedy"
    ("Memorandum From Rusk to President Johnson", "1965-03-01", {"johnson-lyndon-b"}),  # not U. Alexis
    ("Memorandum of Conversation The President General de Gaulle", "1961-05-31", {"kennedy-john-f",
                                                                                  "de-gaulle-charles"}),
    ("Telegram From the Embassy in Vietnam (Durbrow) to Ngô Đình Diệm", "1960-04-01", {"ngo-dinh-diem"}),
])
def test_heading_persons(head, day, want):
    assert F.heading_persons(head, CANDS, day) == want


def test_window():
    d = datetime.date
    assert F.window("1962-10-01") == (d(1962, 9, 30), d(1962, 10, 2))
    assert F.window("1962-10-01", "1962-10-05") == (d(1962, 9, 30), d(1962, 10, 6))
    assert F.window("1962-10-01", "1962-11-30") == (d(1962, 9, 30), d(1962, 10, 2))   # a long range: its date


def test_meets():
    d = datetime.date
    assert F.meets(d(1961, 4, 14), d(1961, 4, 16), d(1961, 4, 15), d(1961, 4, 19))
    assert not F.meets(d(1961, 4, 10), d(1961, 4, 12), d(1961, 4, 15), d(1961, 4, 19))


PRES = "kennedy-john-f"
ENTS = [{"id": "cal.1962-10-01.vietnam", "names": {"nolting-frederick-e-jr"}, "roots": {"vietnam"}},
        {"id": "cal.1962-10-01.cuba", "names": {"rusk-dean"}, "roots": {"cuba"}},
        {"id": "cal.1962-10-01.program", "names": {PRES}, "roots": {"program"}},
        {"id": "cal.1962-10-01.vietnam-2", "names": {PRES}, "roots": {"vietnam"}},
        {"id": "cal.1962-10-01.berlin", "names": {"rusk-dean", "gromyko-andrei"}, "roots": {"berlin-and-vienna"}}]


@pytest.mark.parametrize("persons,want", [
    ({"nolting-frederick-e-jr"}, ("a", "persons", ["cal.1962-10-01.vietnam"])),     # a person, in the thread
    ({"rusk-dean"}, ("b", "", [])),                                                 # a person, another thread
    ({"rusk-dean", "gromyko-andrei"}, ("a", "persons", ["cal.1962-10-01.berlin"])),   # two persons, any thread
    ({PRES}, ("b", "", [])),                                                        # the President alone: never
    ({PRES, "nolting-frederick-e-jr"}, ("a", "persons", ["cal.1962-10-01.vietnam"])),
    (set(), ("a", "thread", ["cal.1962-10-01.vietnam", "cal.1962-10-01.vietnam-2"])),  # no persons: the thread
])
def test_sort_doc(persons, want):
    s, by, hits = F.sort_doc({"title": "Telegram"}, persons, ENTS, ["vietnam"], president=PRES)
    assert (s, by, [i for i, _ in hits]) == want


def test_sort_doc_routine_first():
    assert F.sort_doc({"title": "Editorial Note"}, {"nolting-frederick-e-jr"}, ENTS, ["vietnam"],
                      president=PRES) == ("c", "editorial note", [])


def test_sort_doc_nothing_on_the_days():
    assert F.sort_doc({"title": "Telegram"}, set(), [], ["vietnam"], president=PRES) == ("b", "", [])


def test_cited():
    t = ("n: '[FRUS 1961–63, X, doc. 231](https://history.state.gov/historicaldocuments/frus1961-63v10/d231).'\n"
         "rows:\n  - 'https://history.state.gov/historicaldocuments/frus1961-63v10-12mSupp/d278a: 1'\n"
         "  - 'https://history.state.gov/historicaldocuments/frus1961-63v12'")
    assert F.cited([t]) == {("frus1961-63v10", "d231"), ("frus1961-63v10-12mSupp", "d278a")}


def test_volume_of():
    assert F.volume_of("FRUS 1961–63, II, doc. 295") == "FRUS 1961–63, II"
    assert F.volume_of("FRUS 1961–63, X–XII, microfiche supp., doc. 278a") == "FRUS 1961–63, X–XII, microfiche supp."


def test_threads_map_names_threads():
    assert all(isinstance(v, list) and v and all(isinstance(t, str) and t == t.lower() for t in v)
               for v in F.THREADS.values())
