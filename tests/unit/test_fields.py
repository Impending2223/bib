"""fields.py: R25a's three detectors (the time, the approximate date, the place), true and false, in the languages.

Written Nov. 19, 2026, from the measured hits on the open and merged patches (tools/bib/fields.py, STYLE 3): each row
is a case the detectors were tuned on. A row that fails is a change of behaviour.
"""
import pytest

from bib import fields


def cal(c, **kw):
    e = {"id": "cal.1961-04-20.cuba", "date": "1961-04-20", "when": "Apr. 20", "thread": "cuba", "c": c, "n": "Src, 1."}
    e.update(kw)
    return e


def rules(e):
    return sorted({r for r, _ in fields.findings(e)})


TIME_TRUE = [
    "Kennedy addresses the editors, 10 p.m.",
    "The cabinet sits from 10:30 a.m.",
    "Bundy to Kennedy at noon.",
    "The cable goes out at midnight.",
    "Strike reported 2140Z.",
    "Kennedy sees Rusk at 4.",
    "Rusk and Dulles meet in the morning.",
    "Ball telephones the President that evening.",
    "The vote comes late at night.",
    "Troops land at dawn.",
    "Mao 毛泽东 speaks to the conference, 下午.",
    "周恩来 receives the delegation 晚上十時半.",
    "毛泽东 talks with Liu 9点钟.",
    "Khrushchev receives Thompson в 10 часов.",
    "Хрущёв выступает вечером.",
    "Hồ Chí Minh speaks to the assembly sáng ngày 2.",
    "Bộ Chính trị họp lúc 8 giờ.",
    "The Politburo sits through the đêm.",
    "Kennedy and Macmillan talk over breakfast.",
    "Yang Shangkun 杨尚昆 tells Liu Shaoqi 刘少奇 at lunch of the matter.",
]

TIME_FALSE = [
    "The morning papers carry the speech.",
    "*Time* magazine prints the interview.",
    "Kennedy gives the Evening Star an interview.",
    "Edema stands at about 20,000 at the end of Dec.",
    "Procurement done at 2.011 million tons.",
    'The rite of "asking for instructions in the morning" spreads.',
    "The Center issues its three points 三點意見.",
    "当时 the province reports 同時 to the Center.",
    "Tòa án Tối cao rules on the case.",
    "Sáng kiến of the ministry is published.",
    "Kennedy names Heller to the Council.",
]


@pytest.mark.parametrize("c", TIME_TRUE)
def test_time_true(c):
    assert "fields-time" in rules(cal(c)), fields.time_hits(cal(c))


@pytest.mark.parametrize("c", TIME_FALSE)
def test_time_false(c):
    assert "fields-time" not in rules(cal(c)), fields.time_hits(cal(c))


def test_time_in_n_parenthetical_only():
    assert fields.time_hits(cal("Kennedy speaks.", n="Src, 12 (the evening).")) == [("n", "evening")]
    assert fields.time_hits(cal("Kennedy speaks.", n="Src, 12. The evening was cold.")) == []


def test_time_n_to_check_and_other_day():
    assert fields.time_hits(cal("x.", n="Src, 1. To check: Li, talk with Yang, Apr. 9, 2001 (afternoon, at Li's home).")) == []
    assert fields.time_hits(cal("x.", n="Src, 1 (note 1: the afternoon of Jan. 2, as he left).")) == []
    assert fields.time_hits(cal("x.", n="Src, 1 (note 1: the afternoon of Apr. 20, as he left).")) == [("n", "afternoon")]


def test_time_silenced():
    assert rules(cal("Kennedy speaks at 9 p.m.", time="1961-04-21T02:00Z")) == []
    assert rules(cal("Kennedy speaks at 9 p.m.", time_range=["1961-04-21T01:00Z", "1961-04-21T03:00Z"])) == []
    assert rules(cal("Kennedy speaks at 9 p.m.", tags=["ok:fields-time"])) == []


def loose(c, date="1961-04", when="Apr.", **kw):
    return cal(c, date=date, when=when, **kw)


AT_TRUE = [
    loose("Kennedy writes.", when="Apr., late"),                  # at_for gives it
    loose("Kennedy writes.", when="Apr., after the 12th"),
    loose("Kennedy writes.", date="1961-03", when="Mar., spring"),
    loose("Early April: Kennedy writes to Khrushchev."),
    loose("Kennedy writes, on the eve of the invasion."),
    loose("Soon after the landing, Kennedy writes."),
    loose("Kennedy writes.", date="1961", when="1961, early"),
    loose("Kennedy writes in the spring.", date="1961", when="1961"),
    loose("四月下旬, the province reports."),
    loose("В конце апреля Хрущёв пишет."),
    loose("Cuối tháng tư, Hồ Chí Minh viết."),
]
AT_FALSE = [
    loose("Kennedy writes."),
    loose("Kennedy writes.", at="before 1961-04-21", when="Apr., late"),
    loose("Kennedy writes.", when="Apr., late", tags=["ok:fields-at"]),
    loose("Kennedy writes.", date="1964", when="1964–65"),
    loose("Kennedy writes.", date="1966-09", when="Sept. or Oct."),
    loose("By the end of 1959 the grain is gone; the province reports.", date="1960-03", when="Mar."),
    loose("Mao, touring since late March, writes."),
    cal("Early in the day Kennedy writes."),                      # a day's entry: no `at`
]


@pytest.mark.parametrize("e", AT_TRUE)
def test_at_true(e):
    assert "fields-at" in rules(e), fields.at_hits(e)


@pytest.mark.parametrize("e", AT_FALSE)
def test_at_false(e):
    assert "fields-at" not in rules(e), fields.at_hits(e)


def test_at_message_gives_at_for():
    (m,) = [m for r, m in fields.findings(loose("Kennedy writes.", when="Apr., late")) if r == "fields-at"]
    assert "set at: before 1961-04-21" in m


PLACE_TRUE = [
    ("Peking 北京. Mao receives the delegation.", "peking"),
    ("Ngô Đình Diệm addresses the assembly in Saigon.", "saigon"),
    ("Thompson calls on Khrushchev in Moscow.", "moscow"),
    ("Mao at Hangzhou.", "hangzhou"),
    ("Kennedy, at Hyannis Port, on Cuba with Bundy by telephone.", "hyannis-port"),
]
PLACE_FALSE = [
    "The Sichuan 四川 provincial committee reports.",        # a province: the body, not the scene
    "Kennedy reads *Moscow Diary*.",                            # a title's words
    "Kennedy names Heller to the Council.",
]


@pytest.mark.parametrize("c,key", PLACE_TRUE)
def test_place_true(c, key):
    msgs = [m for r, m in fields.findings(cal(c)) if r == "fields-place"]
    assert any(f"set place: {key} " in m for m in msgs), msgs


@pytest.mark.parametrize("c", PLACE_FALSE)
def test_place_false(c):
    assert "fields-place" not in rules(cal(c)), fields.place_hits(cal(c))


def test_place_silenced():
    assert rules(cal("Mao at Hangzhou.", place="hangzhou")) == []
    assert rules(cal("Mao at Hangzhou.", tags=["ok:fields-place"])) == []


def test_levels():
    assert fields.LEVEL == {"fields-time": "error", "fields-at": "error", "fields-place": "warning"}


def test_message_names_words_and_fix():
    (m,) = [m for r, m in fields.findings(cal("Mao at Hangzhou.")) if r == "fields-place"]
    assert m.endswith("[fields-place]")
    assert "set place: hangzhou (Hangzhou in c), or tag ok:fields-place if Hangzhou is not where the act was done" in m
