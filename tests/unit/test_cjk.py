"""cjk.py: characters out of the line and into the citation block, at their first appearance on a page (the owner, Nov.
19, 2026: "I've changed my mind on writing CJK after place, personal names, and titles in the body text. Drop them.
Keep them in the citation block."; "Names in 'Names:' should have their CJK given on their first appearance on a page").

Written with the change (Nov. 19, 2026); the lines are the calendar's own, as readers wrote them.
"""
import re

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
    # a plural's possessive; an italic title's; a dash between two places; numerals run into characters
    ("of the Anshan Steel Works' 鞍钢 planned output.", "of the Anshan Steel Works' planned output.",
     [('Anshan Steel Works', '鞍钢')]),
    ("reads the *Shanxi ribao*'s 山西日报 long report", "reads the *Shanxi ribao*'s long report",
     [('*Shanxi ribao*', '山西日报')]),
    ('the Guiyang 贵阳–Kunming 昆明 railway;', 'the Guiyang–Kunming railway;', [('Guiyang', '贵阳'), ('Kunming', '昆明')]),
    ('the Twenty-three Articles 23条 the guide', 'the Twenty-three Articles the guide',
     [('Twenty-three Articles', '23条')]),
    # words in corner brackets: after a quotation they gloss it; after a name, they are words of their own
    ('it to "readjust, consolidate, fill out, raise" 「調整、鞏固、充實、提高」, the', 'it to "readjust, consolidate, fill out, raise", the',
     [('"readjust, consolidate, fill out, raise"', '「調整、鞏固、充實、提高」')]),
    ('as Lord Bao did at Chenzhou 「包文丞陳州放糧」.', 'as Lord Bao did at Chenzhou 「包文丞陳州放糧」.', []),
    # kept where they are: the sentence's own words, after a comma, in a quotation, after no word
    ('Deng Xiaoping receives the Albanian Ambassador, 帕里夫蒂 as the page prints his name.',
     'Deng Xiaoping receives the Albanian Ambassador, 帕里夫蒂 as the page prints his name.', []),
    ('the book names him 阿夫扎尔.', 'the book names him 阿夫扎尔.', []),
    ('Rostow ("chairman of the council," 罗斯特 in the nianpu) has written.',
     'Rostow ("chairman of the council," 罗斯特 in the nianpu) has written.', []),
    ('county secretary (so printed, 大劳县) with', 'county secretary (so printed, 大劳县) with', []),
    ('he said "we 我们 go" then', 'he said "we 我们 go" then', []),
    ('at the 1960 年 meeting', 'at the 1960 年 meeting', []),
    # (3) after a preposition, an article or a verb: the sentence's own words, not a gloss; a capitalized "The" none
    ('a delegation led by 莫纳·孟杜, and of', 'a delegation led by 莫纳·孟杜, and of', []),
    ('a banquet for 比莱.', 'a banquet for 比莱.', []),
    ('near the 呷咖公 bridge', 'near the 呷咖公 bridge', []),
    ('The 23条 (Twenty-three Articles).', 'The 23条 (Twenty-three Articles).', []),
    # (4) a plain noun or verb that introduces words: the words stay; a term of its own words is glossed
    ('The slogan 三面红旗 rang out.', 'The slogan 三面红旗 rang out.', []),
    ('He quotes the line 不到长城非好汉.', 'He quotes the line 不到长城非好汉.', []),
    ('Mao, in a note headed 关于, writes.', 'Mao, in a note headed 关于, writes.', []),
    ('the inscription 為人民服務 on the gate', 'the inscription 為人民服務 on the gate', []),
    ('the general line 总路线 holds', 'the general line holds', [('general line', '总路线')]),
    ('The phrase dazibao 大字报 everywhere.', 'The phrase dazibao everywhere.', [('dazibao', '大字报')]),
    # (9) a translated quotation: a romanized name's gloss in it goes; the quotation's own words in characters stay
    ('the office, "Why Xifeng 西馮 brigade has had', 'the office, "Why Xifeng brigade has had', [('Xifeng', '西馮')]),
    ('"Shangkun 尚昆 to handle; print it."', '"Shangkun to handle; print it."', [('Shangkun', '尚昆')]),
    ('Mao: "三面红旗万岁".', 'Mao: "三面红旗万岁".', []),
    ('"Learn from Comrade Lei Feng 雷锋, serve', '"Learn from Comrade Lei Feng, serve', [('Lei Feng', '雷锋')]),
    # (10) a hyphen in the run; a name's ××; a second script in parentheses; the surname An
    ('telegraph Gheorghiu-Dej 乔治乌-德治, Maurer', 'telegraph Gheorghiu-Dej, Maurer', [('Gheorghiu-Dej', '乔治乌-德治')]),
    ('the question of the Il-18 伊尔-18.', 'the question of the Il-18.', [('Il-18', '伊尔-18')]),
    ('the team leader Zhang ×× 张×× (so the', 'the team leader Zhang ×× (so the', [('Zhang ××', '张××')]),
    ('Kim Il Sung 김일성 (金日成) in Pyongyang.', 'Kim Il Sung in Pyongyang.', [('Kim Il Sung', '김일성 (金日成)')]),
    ('Liu Shaoqi 刘少奇 and Deng Xiaoping 邓小平 (刘邓) report.', 'Liu Shaoqi and Deng Xiaoping report.',
     [('Liu Shaoqi', '刘少奇'), ('Deng Xiaoping', '邓小平'), ('Liu Shaoqi and Deng Xiaoping', '刘邓')]),
    ('An Ziwen 安子文 reports.', 'An Ziwen reports.', [('An Ziwen', '安子文')]),
    ('the *Selected Works of Mao Zedong 毛泽东* 《毛泽东选集》, and', 'the *Selected Works of Mao Zedong*, and',
     [('Mao Zedong', '毛泽东'), ('*Selected Works of Mao Zedong*', '《毛泽东选集》')]),
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


FITS = [  # (2) the token itself or its surname alone; never a given name, a longer label, a quoted or italic title
    ('Mao', 'Mao Zedong', True), ('Yang Shangkun', 'Yang Shangkun', True), ('Peking', 'Yang Shangkun', False),
    ('He Jun', 'He Long', False), ('Liu Shaoqi', 'Liu', False), ('Shangkun', 'Yang Shangkun', False),
    ('Xiaoping', 'Deng Xiaoping', False), ('Mao Yuanxin', 'Mao', False), ('Mao Zedong Thought', 'Mao Zedong', False),
    ('"Learn from Comrade Lei Feng"', 'Lei Feng', False), ('*Our answer to Khrushchev*', 'Khrushchev', False),
    ('Kennedy', 'John F. Kennedy', True)]


@pytest.mark.parametrize("label,token,want", FITS)
def test_fits(label, token, want):
    assert cjk._fits(label, token) is want


LONGER = [('Vice-Premier Li Xiannian', 'Li Xiannian', 'after'), ('Sékou Touré', 'Touré', 'after'),
          ('Nosaka Sanzō', 'Nosaka', 'before'), ('Mao Yuanxin', 'Mao', 'before'),
          ('Mao Zedong Thought', 'Mao Zedong', 'before'), ('Mao Zedong sixiang xuexi', 'Mao Zedong', None),
          ('"Refute Togliatti"', 'Togliatti', None), ('Liu Shaoqi', 'Liu Shaoqi', None)]


@pytest.mark.parametrize("label,token,want", LONGER)
def test_longer(label, token, want):
    assert cjk._longer(label, token) == want


class _Lk:
    """A Linker's who_named and names_resolved, from a table {token: name entry key}."""
    def __init__(self, who):
        self.who = who

    def who_named(self, t, tags=(), taken=()):
        return (None, f"names.html#{self.who[t]}") if t in self.who else None

    def names_resolved(self, toks, tags=()):
        return [self.who_named(t) for t in toks]


class _Series:
    def __init__(self, chars, who):
        self.lists, self._cjk_names, self._cjk_linker = {}, chars, _Lk(who)


def _plan(c, names, chars, who):
    return cjk.plan(_Series(chars, who), {"id": "t", "c": c, "n": f"[[w.x]], 3. Names: {names}."})


def test_names_by_person():
    """(1) A name entry's characters go to its own person, found as the Names: line finds him, never to another of
    the surname (Huang Zhen is not Huang Hua)."""
    chars, who = {"huang-hua": "黄华"}, {"Huang Hua": "huang-hua", "Huang Zhen": "huang-chen", "Huang": "huang-chen"}
    assert _plan("Huang Zhen in Paris.", "Huang Zhen", chars, who) == ([], [])
    assert _plan("Huang in Paris.", "Huang", chars, who) == ([], [])
    assert _plan("Huang Hua in Ottawa.", "Huang Hua", chars, who) == ([("Huang Hua", "黄华")], [])


def test_terms_are_not_names():
    """(2) A term or a title holding a name is not the person's characters; exact labels first; a given name gloss
    goes to Characters:, a longer label only where it is the same man."""
    who = {"Mao Zedong": "mao-zedong", "Mao": "mao-zedong", "Mao Yuanxin": "mao-yuanxin", "Deng Xiaoping": "deng"}
    p = _plan("Hold high Mao Zedong Thought 毛泽东思想.", "Mao Zedong", {}, who)
    assert p == ([], [("Mao Zedong Thought", "毛泽东思想")])
    p = _plan("Mao 毛泽东 on the list (Mao Yuanxin 毛远新 not to attend).", "Mao Zedong, Mao Yuanxin", {}, who)
    assert p == ([("Mao Zedong", "毛泽东"), ("Mao Yuanxin", "毛远新")], [])
    p = _plan("Mao Yuanxin 毛远新 reports.", "Mao", {}, who)
    assert p == ([], [("Mao Yuanxin", "毛远新")])
    p = _plan('"Xiaoping 小平 to handle."', "Deng Xiaoping", {}, who)
    assert p == ([], [("Xiaoping", "小平")])
    p = _plan("Vice-Premier Li Xiannian 李先念 receives them.", "Li Xiannian", {}, {})
    assert p == ([("Li Xiannian", "李先念")], [])


def test_name_entry_characters(series):
    """A name entry's subject line that records characters gives them to a 'Names:' token the line has none for: by
    his name entry, not by his surname or given name."""
    assert cjk._name_chars(series)['ikeda-hayato'] == '池田勇人'
    assert 'ikeda' not in cjk._name_chars(series) and 'hayato' not in cjk._name_chars(series)
    e = {"id": "x", "c": "Ikeda in Tokyo.", "n": "[[w.x]], 3. Names: Ikeda Hayato."}
    assert cjk.plan(series, e) == ([('Ikeda Hayato', '池田勇人')], [])
    e = {"id": "y", "c": "Ikeda Shigeru in Tokyo.", "n": "[[w.x]], 3. Names: Ikeda Shigeru."}
    assert cjk.plan(series, e) == ([], [])


# ---------------------------------------------------------------- on the fixture's pages

@pytest.fixture(scope="module")
def series():
    return store.Series()


def test_plan(series):
    """Names take their own characters; the rest close the block."""
    e = series.get("cal.1961-04-29.china-leadership-3")[2]
    assert e["c"] == "Xu Zirong 徐子荣 comes to Yang Shangkun 杨尚昆 on a certain case 某案."
    assert cjk.plan(series, e) == ([('Xu Zirong', '徐子荣'), ('Yang Shangkun', '杨尚昆')], [('certain case', '某案')])


def test_page_order(series):
    """(5) The firsts follow the page's own order, a day's entries as daybook lays them out (dayorder.order, the
    subentries after their parent): no entry earlier on the page names the person, or cites the card, that the firsts
    give a later one."""
    from bib import dayorder, subentries, works, loose
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        rows = cjk.page_rows(series, lst)
        days = {}
        for h, e in rows:
            if loose.order_key(e)[1] == 1 and "when" in e and len(str(e.get("date", ""))) == 10:
                days.setdefault((h, str(e["date"])), []).append(e)
        for es in days.values():
            assert es == [x for x, _ in subentries.nest(lst, dayorder.order(lst, es), dayorder.order)]
        pos = {e["id"]: (h, k) for k, (h, e) in enumerate(rows)}
        f, fc = cjk.firsts(series), works.first_cites(series)
        held = {}
        for h, e in rows:
            for ch in [c for _, c in cjk.plan(series, e)[0]]:
                ids = held.setdefault((h, ch), [])
                if e["id"] not in ids:
                    ids.append(e["id"])
        for (h, ch), ids in held.items():
            assert (ids[0], ch) in f and not any((i, ch) in f for i in ids[1:])
        import re
        for eid, cid in fc:
            if eid not in pos:
                continue
            h, k = pos[eid]
            cites = re.compile(r"\[\[" + re.escape(cid) + r"[\]|]")
            assert not any(hx == h and cites.search(x.get("n") or "") for hx, x in rows[:k])


def test_printed_by_cites(series):
    """(11) Characters a card's full cite prints in the block are not given again in Names: or Characters:."""
    assert cjk.printed_by("[[w.x]], 3.", "Wu Lengxi 吴冷西, *Shinian lunzhan* 十年论战, 3.") == {"吴冷西", "十年论战"}
    assert cjk.printed_by("Mao 毛泽东 [[w.x]]", "Mao 毛泽东 *Nianpu* 毛泽东年谱") == {"毛泽东年谱"}
    first = series.get("cal.1961-04-01.china-leadership-3")[2]
    tail = cjk.Entry(series, first).claim(set()).tail(first["n"], frozenset({"杨尚昆", "越南"}))
    assert tail.endswith("Names: Deng Yingchao 邓颖超, Yang Shangkun.") and "越南" not in tail


def test_other_renderers_drop(monkeypatch):
    """(12) The standing conditions' register shows the line as the calendar does."""
    from bib import standing, calsplit
    e = {"id": "cal.x", "date": "1961-04-01", "when": "Apr. 1", "thread": "t", "tags": ["form:state"],
         "c": "Yang Shangkun 杨尚昆 in Hangzhou 杭州.", "n": "Names: Yang Shangkun."}

    class S:
        entries = [e]

    class L:                            # a calendar of one entry, no thread index (chron.sort reads walk, threads)
        key = "cal"

        def entries(self):
            return [(None, e)]

        def walk(self):
            return [S]

        def threads(self):
            return {}
    monkeypatch.setattr(calsplit, "half_of_date", lambda lst, d: 1)
    monkeypatch.setattr(calsplit, "href", lambda lst, h, i: "cal.html#x")
    out = standing.register_html(L(), lambda l, t: t, lambda l, t: t)
    assert "Yang Shangkun in Hangzhou." in out and not cjk.HAS.search(out)


def test_lives_drop(series):
    """(12) The lives' calendar sentences render the line by the calendar's renderer (lives.py, STYLE 9): its characters
    dropped as the calendar's are."""
    from bib import build, lives
    from bib.congress import Pointers
    e = series.get("cal.1961-04-01.china-leadership-3")[2]
    got = lives.calendar_sentences(Pointers(series, build.Linker(series)), [e], "yang-shangkun")
    line = re.sub(r"<[^>]+>", "", re.split(r'<ol class="fn"|<span class="n">', got[0]["text"])[0])
    assert "Yang Shangkun" in line and not cjk.HAS.search(line)


def test_first_on_each_page(series):
    """Each run's first appearance on each page, once: 杨尚昆 on the April half and on the August half."""
    f = cjk.firsts(series)
    assert sorted(i for i, ch in f if ch == "杨尚昆") == ['cal.1961-04-01.china-leadership-3',
                                                         'cal.1961-08-01.china-leadership-6']


def test_tail(series):
    """(a) The block: a Names: person's characters after his name at their first on the page; none for an entry later
    on the page; no "Characters:" sentence, the line's other characters not collected."""
    first = series.get("cal.1961-04-01.china-leadership-3")[2]
    tail = cjk.Entry(series, first).claim(set()).tail(first["n"])
    assert tail.endswith("Names: Deng Yingchao 邓颖超, Yang Shangkun 杨尚昆.") and "Characters:" not in tail
    later = series.get("cal.1961-04-29.china-leadership-3")[2]
    tail = cjk.Entry(series, later).claim(set()).tail(later["n"])
    assert tail.endswith("Names: Xu Zirong 徐子荣, Yang Shangkun.") and "某案" not in tail


def test_note_whole(series):
    """(a) The note keeps all its own characters, as written, every time: a title, a document, "To check:", "The
    words:"; the Names: persons' are added at their first on the page and nothing taken away."""
    later = series.get("cal.1961-04-29.china-leadership-3")[2]
    n = ("[[w.x]], 3 (the *Yang Shangkun riji* 杨尚昆日记; Yang Shangkun 杨尚昆 wrote it). The words: 上午. "
         "To check: *Mao Zedong nianpu* 毛泽东年谱. Names: Xu Zirong, Yang Shangkun.")
    tail = cjk.Entry(series, later).claim(set()).tail(n)
    assert tail == n.replace("Xu Zirong,", "Xu Zirong 徐子荣,")


QUOTES = [  # (b) a quoted original with its English beside it: the English on the line, the original in "The words:"
    ('Mao: "中央决定进行反击战役" (the Center has decided on a counterattack).',
     'Mao: "the Center has decided on a counterattack".', ['中央决定进行反击战役']),
    ('The diary adds "由我主席" ("I in the chair").', 'The diary adds "I in the chair".', ['由我主席']),
    ('a call to respond positively ("积极响应") to the government', 'a call to respond positively to the government',
     ['积极响应']),
    ('"米格式直升机" (MiG helicopters) and "你们会胜利的" (you will win)', '"MiG helicopters" and "you will win"',
     ['米格式直升机', '你们会胜利的']),
    # no English beside it, or a note rather than a rendering: it stays
    ('Mao: "三面红旗万岁".', 'Mao: "三面红旗万岁".', []),
    ('the words "大劳县" (so printed) in the book', 'the words "大劳县" (so printed) in the book', []),
]


@pytest.mark.parametrize("text,line,words", QUOTES)
def test_quotes(text, line, words):
    assert cjk.quotes(text) == (line, words)
    assert cjk.drop(text) == cjk.drop(cjk.drop(text)) == line


def test_quotes_in_block():
    """(b) The original goes to the entry's own block, in every entry, before Names:; not where the note has it."""
    e = {"id": "q", "c": 'Mao: "中央决定进行反击战役" (the Center has decided on a counterattack).',
         "n": "[[w.x]], 3. Names: Mao Zedong."}

    class S:
        lists, _cjk_names, _first_cjk = {}, {}, set()
    x = cjk.Entry(S(), e).claim(set())
    assert x.tail(e["n"]) == "[[w.x]], 3. The words: 中央决定进行反击战役. Names: Mao Zedong."
    assert x.tail("[[w.x]], 3. The words: 中央决定进行反击战役 (p. 9).") == "[[w.x]], 3. The words: 中央决定进行反击战役 (p. 9)."
    assert x.tail("") == "The words: 中央决定进行反击战役."
    e2 = dict(e, id="q2", n="[[w.x]], 3 (中央决定进行反击战役). Names: Mao Zedong.")
    y = cjk.Entry(S(), e2).claim(set())
    assert y.tail("Names: Mao Zedong.") == "Names: Mao Zedong."      # the footnotes' text gives it: not twice


def test_names_line_stops_at_characters():
    from bib.build import names_line
    n = "Names: Liu Shaoqi 刘少奇. Characters: Hangzhou 杭州."
    _, body, tail = names_line(n)
    assert body == "Liu Shaoqi 刘少奇" and tail == ". Characters: Hangzhou 杭州."


# STYLE 2b: a transliterated foreign name with its dot, written in italics: roman, quoted, the characters kept.
DOTTED = [
    ('Chen Yi 陈毅 receives *Abudulake Suxi* 阿卜杜拉克·苏西 and his wife.',
     'Chen Yi receives "Abudulake Suxi" 阿卜杜拉克·苏西 and his wife.'),
    ('led by Brigadier *Abudule Aini Yibulaxin* 阿卜杜勒·埃尼·易卜拉欣.',
     'led by Brigadier "Abudule Aini Yibulaxin" 阿卜杜勒·埃尼·易卜拉欣.'),
    ('meets "Ai\'ermeisi Awumada" 埃尔梅斯·阿乌马达.', 'meets "Ai\'ermeisi Awumada" 埃尔梅斯·阿乌马达.'),
    ('In *Hongqi* 红旗 and *Renmin ribao* 人民日报.', 'In *Hongqi* and *Renmin ribao*.'),
    ('receives *Aijian* 艾坚.', 'receives *Aijian*.'),
]


@pytest.mark.parametrize("text,want", DOTTED)
def test_dotted_transliteration(text, want):
    from bib import cjk
    assert cjk.drop(text) == want
    assert cjk.drop(want) == want                       # STYLE 6: a line already dropped is not changed
