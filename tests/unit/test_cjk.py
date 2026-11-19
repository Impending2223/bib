"""cjk.py: characters out of the line and into the citation block, at their first appearance on a page (the owner, Nov.
19, 2026: "I've changed my mind on writing CJK after place, personal names, and titles in the body text. Drop them.
Keep them in the citation block."; "Names in 'Names:' should have their CJK given on their first appearance on a page").

Written with the change (Nov. 19, 2026); the lines are the calendar's own, as readers wrote them.
"""
import pytest

from bib import cjk, store

SPLIT = [
    # names and places: the run and its space go; the pair stays
    ('Peking 北京. Luo Daorang 罗道让 and Ye Zilong 叶子龙 report to Yang Shangkun 杨尚昆 on the Chunou zhai 春藕斋 in '
     'Zhongnanhai 中南海.',
     'Peking. Luo Daorang and Ye Zilong report to Yang Shangkun on the Chunou zhai in Zhongnanhai.',
     [('Peking', '北京'), ('Luo Daorang', '罗道让'), ('Ye Zilong', '叶子龙'), ('Yang Shangkun', '杨尚昆'),
      ('Chunou zhai', '春藕斋'), ('Zhongnanhai', '中南海')]),
    # an organ in English, an italic title, a place
    ('the Henan Provincial Supervisory Committee 河南省监委 reads the *Political Economy* 《政治经济学》 at Hangzhou 杭州.',
     'the Henan Provincial Supervisory Committee reads the *Political Economy* at Hangzhou.',
     [('Henan Provincial Supervisory Committee', '河南省监委'), ('*Political Economy*', '《政治经济学》'),
      ('Hangzhou', '杭州')]),
    ('the *Hongqi* 红旗 editorial', 'the *Hongqi* editorial', [('*Hongqi*', '红旗')]),
    # a possessive: the label without it, the line as written
    ("Yang Shangkun 杨尚昆 to Peng Zhen's 彭真 for a talk.", "Yang Shangkun to Peng Zhen's for a talk.",
     [('Yang Shangkun', '杨尚昆'), ('Peng Zhen', '彭真')]),
    # a term in quotation marks; in a parenthesis, its comma goes with the run
    ('in 1956 (the "buying-out," 赎买). On how long', 'in 1956 (the "buying-out"). On how long',
     [('"buying-out"', '赎买')]),
    ('a "current counterrevolutionary clique" 現行反革命集團.', 'a "current counterrevolutionary clique".',
     [('"current counterrevolutionary clique"', '現行反革命集團')]),
    ('the ambassador (Mai Ye, 麦耶) on the war.', 'the ambassador (Mai Ye) on the war.', [('Mai Ye', '麦耶')]),
    # a parenthesis holding characters alone goes whole; several names, each its own
    ('to "look after one side" and "lean to one side" (工商业者应当下决心“顾一头”、“一边倒”), drafted',
     'to "look after one side" and "lean to one side", drafted',
     [('"look after one side" and "lean to one side"', '工商业者应当下决心“顾一头”、“一边倒”')]),
    ("Zhou receives Vietnam's Phạm Hùng and Lê Trọng Tấn (范雄, 黎仲迅) in the Fujian Hall.",
     "Zhou receives Vietnam's Phạm Hùng and Lê Trọng Tấn in the Fujian Hall.",
     [('Phạm Hùng', '范雄'), ('Lê Trọng Tấn', '黎仲迅')]),
    # a Korean run with a space inside; a title with quotation marks inside its brackets
    ('the Kukka Chaegŏn Ch\'oego Hoeŭi 國家再建最高會議 議長室 announces', 'the Kukka Chaegŏn Ch\'oego Hoeŭi announces',
     [("Kukka Chaegŏn Ch'oego Hoeŭi", '國家再建最高會議 議長室')]),
    ('on "What the message shows" 《艾森豪威尔的"国情咨文"说明了什么》, sent', 'on "What the message shows", sent',
     [('"What the message shows"', '《艾森豪威尔的"国情咨文"说明了什么》')]),
    # kept where they are: the sentence's own words, after a comma, in a quotation, after no word
    ('Deng Xiaoping receives the Albanian Ambassador, 帕里夫蒂 as the page prints his name.',
     'Deng Xiaoping receives the Albanian Ambassador, 帕里夫蒂 as the page prints his name.', []),
    ('the book names him 阿夫扎尔.', 'the book names him 阿夫扎尔.', []),
    ('Rostow ("chairman of the council," 罗斯特 in the nianpu) has written.',
     'Rostow ("chairman of the council," 罗斯特 in the nianpu) has written.', []),
    ('county secretary (so printed, 大劳县) with', 'county secretary (so printed, 大劳县) with', []),
    ('he said "we 我们 go" then', 'he said "we 我们 go" then', []),
    ('at the 1960 年 meeting', 'at the 1960 年 meeting', []),
    # Vietnamese is Latin script: untouched
    ('Ngô Đình Diệm meets Lê Duẩn.', 'Ngô Đình Diệm meets Lê Duẩn.', []),
    ('', '', []),
]


@pytest.mark.parametrize("text,line,pairs", SPLIT)
def test_split(text, line, pairs):
    assert cjk.split(text) == (line, pairs)


@pytest.mark.parametrize("text,line,pairs", SPLIT)
def test_drop_twice(text, line, pairs):
    """The units are rendered through drop() again (footnotes, claims' spans): a second pass changes nothing."""
    assert cjk.drop(cjk.drop(text)) == cjk.drop(text) == line


PEEL = [
    ('Liu Shaoqi 刘少奇', ('Liu Shaoqi', ' 刘少奇')),
    ('Liu Shaoqi', ('Liu Shaoqi', '')),
    ('Heller', ('Heller', '')),
]


@pytest.mark.parametrize("tok,want", PEEL)
def test_peel(tok, want):
    assert cjk.peel(tok) == want


WITH_NAMES = [
    ('[[w.x]], 3. Names: Liu Shaoqi, Deng Xiaoping.', {'Liu Shaoqi': '刘少奇', 'Deng Xiaoping': '邓小平'},
     '[[w.x]], 3. Names: Liu Shaoqi 刘少奇, Deng Xiaoping 邓小平.'),
    ('Names: Heller and Liu Shaoqi. Check: the day.', {'Liu Shaoqi': '刘少奇'},
     'Names: Heller and Liu Shaoqi 刘少奇. Check: the day.'),
    ('Names: Liu Shaoqi 刘少奇.', {'Liu Shaoqi': '刘少奇'}, 'Names: Liu Shaoqi 刘少奇.'),
    ('No names here.', {'Liu Shaoqi': '刘少奇'}, 'No names here.'),
]


@pytest.mark.parametrize("n,chars,want", WITH_NAMES)
def test_with_names(n, chars, want):
    assert cjk.with_names(n, chars) == want


FITS = [('Mao', 'Mao Zedong', True), ('Liu Shaoqi', 'Liu', True), ('Yang Shangkun', 'Yang Shangkun', True),
        ('Peking', 'Yang Shangkun', False), ('Shangkun', 'Yang Shangkun', True), ('He Jun', 'He Long', False)]


@pytest.mark.parametrize("label,token,want", FITS)
def test_fits(label, token, want):
    assert cjk._fits(label, token) is want


# ---------------------------------------------------------------- on the fixture's pages

@pytest.fixture(scope="module")
def series():
    return store.Series()


def test_plan(series):
    """Names take their own characters; the rest close the block."""
    e = series.get("cal.1961-04-29.china-leadership-3")[2]
    assert e["c"] == "Xu Zirong 徐子荣 comes to Yang Shangkun 杨尚昆 on a certain case 某案."
    assert cjk.plan(series, e) == ([('Xu Zirong', '徐子荣'), ('Yang Shangkun', '杨尚昆')], [('certain case', '某案')])


def test_name_entry_characters(series):
    """A name entry's subject line that records characters gives them to a 'Names:' token the line has none for."""
    assert cjk._name_chars(series)['ikeda hayato'] == '池田勇人'
    e = {"id": "x", "c": "Ikeda in Tokyo.", "n": "[[w.x]], 3. Names: Ikeda Hayato."}
    assert cjk.plan(series, e) == ([('Ikeda Hayato', '池田勇人')], [])


def test_first_on_each_page(series):
    """Each run's first appearance on each page, once: 杨尚昆 on the April half and on the August half."""
    f = cjk.firsts(series)
    assert sorted(i for i, ch in f if ch == "杨尚昆") == ['cal.1961-04-01.china-leadership-3',
                                                         'cal.1961-08-01.china-leadership-6']


def test_tail(series):
    """The block: characters after the names at their first on the page, the rest in one closing sentence; none for
    an entry later on the page."""
    first = series.get("cal.1961-04-01.china-leadership-3")[2]
    tail = cjk.Entry(series, first).claim(set()).tail(first["n"])
    assert tail.endswith("Names: Deng Yingchao 邓颖超, Yang Shangkun 杨尚昆. Characters: Vietnam 越南.")
    later = series.get("cal.1961-04-29.china-leadership-3")[2]
    tail = cjk.Entry(series, later).claim(set()).tail(later["n"])
    assert tail.endswith("Names: Xu Zirong 徐子荣, Yang Shangkun. Characters: certain case 某案.")


def test_note_runs_after_line(series):
    """A run the line gives the block is not given again by the note's own text (the line's claim comes first)."""
    first = series.get("cal.1961-04-01.china-leadership-3")[2]
    done = set()
    cjk.Entry(series, first).claim(done)
    assert "杨尚昆" in done and cjk.strip(series, first, "Yang Shangkun 杨尚昆 wrote.", done) == "Yang Shangkun wrote."


def test_names_line_stops_at_characters():
    from bib.build import names_line
    n = "Names: Liu Shaoqi 刘少奇. Characters: Hangzhou 杭州."
    _, body, tail = names_line(n)
    assert body == "Liu Shaoqi 刘少奇" and tail == ". Characters: Hangzhou 杭州."
