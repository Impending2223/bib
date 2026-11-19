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
    loose("Kennedy writes.", when="Apr., about the 20th"),        # a qualifier merge cannot place
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
    # STYLE 1e: what merge places itself (loose.at_for, at_problems clean): the ghost-day pass sets `at`
    loose("Kennedy writes.", when="Apr., late"),
    loose("Kennedy writes.", when="Apr., after the 12th"),
    loose("Kennedy writes.", date="1961-03", when="Mar., spring"),
    loose("Late in April Kennedy writes.", when="Apr., late"),
    # another season's, another year's: the "of YYYY" read
    loose("Kennedy recalls the talks in the spring of 1958.", date="1960", when="1960"),
    loose("The famine of the winter of 1959–60 is reported.", date="1960-06", when="June"),
    loose("Some two thousand members by the summer of 1962.", date="1960-08", when="Aug."),
    loose("Khrushchev announces that tests will resume in the fall.", date="1961-07", when="July"),
    loose("475,000 troops by the end of 1966.", date="1966-06", when="June"),   # a year's position, a month's entry
    loose("Kennedy writes.", date="1964-05", when="May, spring"),               # the month's own season: no place
    loose("Kennedy writes.", date="1961-12", when="Dec. (late 1961)"),
]


@pytest.mark.parametrize("e", AT_TRUE)
def test_at_true(e):
    assert "fields-at" in rules(e), fields.at_hits(e)


@pytest.mark.parametrize("e", AT_FALSE)
def test_at_false(e):
    assert "fields-at" not in rules(e), fields.at_hits(e)


def test_at_season_of_year_is_the_entrys():
    # the winter of 1959–60 opens in December 1959: a 1960 entry, or a January one, may sit in it
    assert fields.at_hits(loose("In the winter of 1959–60 the mess halls fail.", date="1960", when="1960"))
    assert fields.at_hits(loose("In the winter of 1959–60 the mess halls fail.", date="1960-01", when="Jan."))
    assert fields.at_hits(loose("Kennedy writes in the spring of 1960.", date="1960", when="1960"))


def test_at_message_says_the_fix():
    (m,) = [m for r, m in fields.findings(loose("Kennedy writes.", when="Apr., about the 20th")) if r == "fields-at"]
    assert "'about the 20th' in when" in m and "set at: before|after YYYY-MM-DD" in m


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
    assert fields.LEVEL == {"fields-time": "error", "fields-time-habitual": "warning", "fields-at": "error",
                            "fields-place": "warning"}


def test_message_names_words_and_fix():
    (m,) = [m for r, m in fields.findings(cal("Mao at Hangzhou.")) if r == "fields-place"]
    assert m.endswith("[fields-place]")
    assert "set place: hangzhou (Hangzhou in c), or tag ok:fields-place if Hangzhou is not where the act was done" in m


# -- the audit's false hits (Nov. 19, 2026), from the reader patches: STYLE 1a-1d ---------------------------------------
_MON = {"01": "Jan.", "02": "Feb.", "03": "Mar.", "04": "Apr.", "05": "May", "06": "June", "07": "July", "08": "Aug.",
        "09": "Sept.", "10": "Oct.", "11": "Nov.", "12": "Dec."}


def day(c, d="1964-01-16", when=None, n="Src, 1.", **kw):
    e = {"id": f"cal.{d}.china-leadership", "date": d, "when": when or f"{_MON[d[5:7]]} {int(d[8:])}",
         "thread": "china-leadership", "c": c, "n": n}
    e.update(kw)
    return e


OTHER_DAY = [   # 1a: another day's or another time's hour
    day("Deng reads the request. Comment: he will receive it the morning of the 17th; asks him to consider.",
        "1964-01-16"),                                                       # cal.1964-01-16.china-leadership-6
    day("Peking. Yang Shangkun clears his papers, to leave on the evening of the 10th.", "1965-12-08"),
    day("Zhou and Deng telephone Yang; the group leaders to meet the next afternoon.", "1964-05-27"),
    day("He proposes to open the first session at 9 a.m. tomorrow, with Li Fuchun to explain.", "1964-05-17"),
    day("Comment: agreed; to be announced at tomorrow afternoon's Secretariat.", "1963-04-12"),
    day("Jinan. Mao, left Wuxi on Dec. 16 at dusk, hears Tan Qilong.", "1961-12-17"),
    day("The delegation home by special plane; in Peking on the morning of the 28th.", "1965-07-27"),
    day("The draft to be settled that afternoon at Liu's; asks Mao's word by the afternoon of the 30th.", "1962-12-29"),
    day("Kennedy to Salinger: ask the networks for half an hour at 7 p.m. the next night.", "1962-10-21"),
    day("The offensive struck 13 capitals in 48 hours from about 2:30 a.m. Jan. 31.", "1968-02-05"),
    day("Kennedy thanks the delegation; the issue as discussed the night before.", "1960-09-27"),
    day("Yang, after a night of sharp toothache, takes antibiotics.", "1965-06-15"),
    day("Zhou on the quake 十七日上午 and the rumors.", "1966-03-23"),
    day("Zhou talks with them; 次日上午 he reports.", "1966-03-23"),
    day("O'Brien calls, a few days after the lunch with Kennedy.", "1968-03-01"),
    dict(day("King asked to the Oval Office for Dec. 3, 11:30 a.m."), date="1963-11", when="Nov."),
]
OWN_DAY = [     # the entry's own day stays a hit
    day("Talks on the 16th and 17th. On the 17th morning, on the home situation.", "1964-02-16", when="Feb. 16–17"),
    day("This meeting is the evening of the 16th.", "1960-11-16"),
    day("Springfield is next, on statewide television at 9 o'clock.", "1960-10-03"),
    day("Before dawn on the 26th, to the state prison.", "1960-10-25", when="Oct. 25–27"),
    day("Zhou, in the evening, receives the delegates.", "1967-09-08"),
    day("Shaoshan, Hunan, evening. The group calls a members' meeting.", "1961-04-19"),
    dict(day("Xinyang prefecture, 10 p.m. Arrests at one hour across the prefecture."), date="1960",
         when="1960, 11th lunar month, 7th day"),
]


@pytest.mark.parametrize("e", OTHER_DAY)
def test_time_other_day(e):
    assert fields.time_hits(e) == [], fields.time_hits(e)


@pytest.mark.parametrize("e", OWN_DAY)
def test_time_own_day(e):
    assert fields.time_hits(e), e["c"]


def test_own_days():
    assert fields.own_days(day("x", "1964-02-16", when="Feb. 16–17")) == {(2, 16), (2, 17)}
    assert fields.own_days(day("x", "1960-02-29", when="Feb. 29–Mar. 2")) == {(2, 29), (3, 1), (3, 2)}
    assert fields.own_days(day("x", "1968-12-31", when="Dec. 31–Jan. 1")) == {(12, 31), (1, 1)}
    assert fields.own_days(dict(day("x"), date="1964-01", when="Jan.")) is None


def test_time_n_check_and_link_gloss():   # 1b
    n5 = ("[[w.deng-xiaoping-nianpu-1904]], III, 1782 (Dec. 17, 1963). Names: Deng Xiaoping, Luo Ronghuan. Check: "
          "whether Deng was at the leave-taking of [[cal.1963-12-17.china-leadership-3]] (Yang Shangkun's diary: 4:30 "
          "p.m., Mao there); the nianpu gives no hour.")                     # cal.1963-12-17.china-leadership-5
    assert fields.time_hits(day("Deng goes to Beijing Hospital to take leave of the body.", "1963-12-17", n=n5)) == []
    n10 = ("[[w.deng-xiaoping-nianpu-1904]], III, 1877 (Oct. 10, 1965). Names: Deng Xiaoping. Check: whether this is "
           "the reception of [[cal.1965-10-10.china-leadership-4]] (Yang Shangkun's diary: Mao receives members of "
           "several bodies, 12:30 to 1 p.m.).")                              # cal.1965-10-10.china-leadership-5
    assert fields.time_hits(day("Deng receives the workers.", "1965-10-10", n=n10)) == []
    # the gloss after another entry's link, outside a Check, is that entry's too
    assert fields.time_hits(day("x.", n="Src, 1. See [[cal.1964-01-15.china-leadership]] (the evening). Names: X.")) == []
    # the entry's own gloss stays
    assert fields.time_hits(day("x.", n="Src, 1 (the evening). Check: the day.")) == [("n", "evening")]


AT_NOT_CLOCK = [    # 1c
    "Rachel Carson dies at Silver Spring, Md., at 56.",
    "Former President Truman dies at 82.",
    "Truman, at 80, speaks for the ticket.",
    "The discount rate held at 3.",
    "Humphrey's youths' bill of rights: the vote at 18; a larger role for students.",
    "The rate set, at 3, by the board.",
    "The tax at 75 percent of plan, rice purchases at 25.",
]


@pytest.mark.parametrize("c", AT_NOT_CLOCK)
def test_at_nn_not_clock(c):
    assert fields.time_hits(cal(c)) == [], fields.time_hits(cal(c))


def test_at_nn_clock_and_page():
    assert fields.time_hits(cal("Kennedy sees Rusk at 4.")) == [("c", "at 4")]
    assert fields.time_hits(cal("The meeting is held at 4.")) == [("c", "at 4")]
    assert fields.time_hits(cal("Yang to bed at 2:30.")) == [("c", "at 2:30")]
    assert fields.time_hits(cal("x.", n="Src, 1 (*New York Times*, Mar. 28 at 4 and Mar. 29, 1963, at 1).")) == []
    assert fields.time_hits(cal("x.", n="Src, 1 ([*Times*](https://example.com/t.html), at 15).")) == []


def test_titles():  # 1d's titles
    assert fields.time_hits(cal("Deng sends the editorial 《陶里亚蒂同志同我们的分歧》 and 「晚上好」.")) == []
    assert fields.time_hits(cal("The Night of the Long Knives is recalled.")) == []
    assert fields.time_hits(cal("Hitler's purge, the Night of the Long Knives, is recalled.")) == []
    assert fields.time_hits(cal("Evening. The cable goes out.")) == [("c", "Evening")]


def test_habitual_is_a_warning():   # 1d
    e = cal("Over 300 men patrol the parks from 4 a.m. to 11 p.m. in shifts, and detain the strippers.")
    assert rules(e) == ["fields-time-habitual"]                          # cal.1961-05-11.china-leadership-7
    e = day("He and Zhuo Lin have gone to the works, about three and a half hours' labour a day; they read the "
            "newspapers, listen to the radio at night.", "1969-11-26")    # cal.1969-11-26.china-leadership-2
    assert rules(e) == ["fields-time-habitual"]
    assert rules(cal("Nixon on television each evening at seven.")) == ["fields-time-habitual"]
    assert rules(dict(e, tags=["ok:fields-time"])) == []
    assert rules(dict(e, tags=["ok:fields-time-habitual"])) == []
    # an hour of the act beside the habit, in its own sentence: the error
    assert rules(cal("The patrols go out daily. That night Kennedy calls Rusk.")) == ["fields-time"]
    # a habit only in a quotation, or in another sentence, is no habit
    assert rules(cal('That night Evers to a mass meeting: "We are armed, every last one of us."')) == ["fields-time"]
    assert rules(cal("Thirty flights a day over Cuba. That night with Mikoyan.")) == ["fields-time"]
    assert rules(cal("Kennedy speaks a day or two later, at noon.")) == ["fields-time"]


CN_TIME = ["周恩来 receives them 一时半.", "毛泽东 talks 四时许.", "二十日一时, Zhou calls.", "毛泽东 talks with Liu 一点半.",
           "周恩来 arrives 两点钟.", "Zhou speaks 晚四时."]
CN_NOT_TIME = ["一时期 the province reports.", "一时间 the rumours spread.", "四时八节 are kept.", "不能有一点半点马虎."]


@pytest.mark.parametrize("c", CN_TIME)
def test_cn_time(c):
    assert fields.time_hits(cal(c)), c


@pytest.mark.parametrize("c", CN_NOT_TIME)
def test_cn_not_time(c):
    assert fields.time_hits(cal(c)) == [], fields.time_hits(cal(c))


def test_place_pattern_follows_the_gazetteer():     # [fields-place]: places.GEN, places.PENDING, places.reset
    from bib import places
    e = cal("Mao at Zzyzxtown.")
    assert fields.place_hits(e) == []
    try:
        places.PENDING["zzyzxtown"] = {"key": "zzyzxtown", "name": "Zzyzxtown", "zone": "UTC", "in": "x"}
        assert fields.place_hits(e) == [("c", "Zzyzxtown", "zzyzxtown")]      # a patch's own row
        places.PENDING.clear()
        assert fields.place_hits(e) == []
        assert places.add_row({"key": "zzyzxtown", "name": "Zzyzxtown", "zone": "UTC", "in": "x"}, save=False) is None
        assert fields.place_hits(e) == [("c", "Zzyzxtown", "zzyzxtown")]      # merged: the next patch sees it
    finally:
        places.PENDING.clear()
        places.reset()
    assert fields.place_hits(e) == []
