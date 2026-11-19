"""Characters (漢字, kana, hangul) out of the line; in the citation block the notes' own in full and the 'Names:'
persons' (the owner, Nov. 19, 2026: "I've changed my mind on writing CJK after place, personal names, and titles in
the body text. Drop them. Keep them in the citation block."; "Names in 'Names:' should have their CJK given on their
first appearance on a page."; and, asked of the label "Characters:", about 10:45 a.m.: "What? I'm just saying that the
substantive notes in the citation block should give the full CJK, and that Names in 'Names:' should as well."; of a
quoted original with its English, "Move them, keep English").

STYLE
1. The data keeps the characters wherever a reader wrote them, after the romanized word, a space between:
   "fentian dangan 分田单干", "Tian Jiaying 田家英", "*Hongqi* 红旗", "(the "buying-out," 赎买)"
   (notes/guide/entries.md, "Characters"). The display moves them; nothing in the data changes, and the move is undone
   by changing this file alone.
2. The line (`c`): a run of characters glossing the word or words before it (split: a romanized name, place, term, an
   italic title, a quoted phrase; _label finds them) is dropped with its joining space; so too a parenthesis holding
   characters alone ("... one side" (工商业者应当下决心...)"), and the comma of "(Mai Ye, 麦耶)" or "("Victory
   Goddess," 胜利女神)" with its run; a second script in parentheses goes with the first ("Kim Il Sung 김일성
   (金日成)"). Inside a translated quotation a romanized name's or title's gloss goes too ("Why Xifeng 西馮 brigade");
   the quotation's own words in characters stay ("三面红旗万岁"). Kept where they are: characters standing as the
   sentence's own words, after a preposition, an article or a verb ("led by 莫纳·孟杜", "the 呷咖公", "the book names
   him 阿夫扎尔", "a note headed 关于"), after a plain noun that introduces them ("the slogan 三面红旗", "the line
   不到长城非好汉"; a term of its own words is glossed: "the general line 总路线"), after a comma ("the departing
   Romanian ambassador, 乔治乌"), after no word. Vietnamese is not touched (it is Latin script).
3. A dropped run's characters are not collected (no "Characters:" sentence: the owner, above); a person's in the
   note's "Names:" sentence are given after his name at their first appearance on the page (a calendar half, as
   tools/bib/works.py FIRST CITE counts pages; the entries in the page's order, a day's as the day lays them out:
   dayorder.page_rows): "Names: Liu Shaoqi 刘少奇, Deng Xiaoping 邓小平.". The person is the one the Names: line
   links (build.Linker, by the entry's name: tags); his characters the line's whose label is his token ("Mao
   Zedong"), else those his name entry records, else his surname's alone where no other unmatched token has it
   ("Mao"), else his token's with words before it ("Vice-Premier Li Xiannian") or after it where the Linker finds it
   the same man ("Nosaka Sanzō" for "Nosaka"; never "Mao Yuanxin" for "Mao"); never a given name's ("Xiaoping"), a
   term's or title's holding his name ("Mao Zedong Thought", "Learn from Comrade Lei Feng"). Failing those, his name
   entry's where its subject line records them ("Huang Hua 黄华"), never another's of his surname. Not given again
   later on the page, nor where a card's full cite prints them in the same block (works.py FIRST CITE).
4. The note (`n`, its footnotes too) keeps all its own characters, as written, every time: the documents and titles
   it cites, "To check:", the witnesses, "The words:" (nothing of the note is dropped).
5. A work's characters are its card's (`script`), given at its first cite (works.py FIRST CITE), not here.
6. The claims' units (claims.py), the footnotes' marks (footnotes.py) and the visibility spans (vispage.py) are found
   in the line as rendered: their units are rendered through drop() too (build._unit_renderer), and drop() of a line
   already dropped changes nothing. So too every other place a calendar line is shown: the lives' calendar sentences
   (lives.calendar_sentences), the standing conditions' register (standing.register_html).
7. A quoted original in characters with its English beside it ('"中央决定进行反击战役" (the Center has decided on a
   counterattack)'; 'respond positively ("积极响应")'): the line keeps the English, in the quotation marks
   ('"the Center has decided on a counterattack"'); the original goes to the entry's own citation block, as
   written, in the note's form, "The words: 中央决定进行反击战役." before "Names:", in every entry (not at a first
   appearance only); not where the note already gives it. A quotation with no English beside it stays on the line.
"""
import re

CH = "㐀-䶿一-鿿豈-﫿々〇぀-ヿ가-힯"
PUNCT = "、。，：；·・“”「-』（）—"
_B = r"《[^》\n]*》|〈[^〉\n]*〉|「[^」\n]*」|『[^』\n]*』"
# a word of characters: it opens with a character (or numerals run into one, "23条") and closes with one; numerals,
# brackets and the like inside ("依靠95%干部", "中發[60]364號"); a hyphen inside ("乔治乌-德治", "伊尔-18"), a name's
# ×× ("张××"), a parenthesis of characters at its end ("日中友好协会(正统)")
_X = (rf"(?:{_B}|[{CH}]|\d+(?=[{CH}]))(?:(?:{_B}|[{CH}{PUNCT}\d\[\]×%％-])*"
      rf"(?:{_B}|[{CH}”）×]|(?<=-)\d+|\([{CH}]+\)))?")
CJK_RUN = rf"{_X}(?: {_X})*"                       # a run: characters, their punctuation, a space between words
HAS = re.compile(rf"[{CH}《〈]")
LINE = re.compile(rf"(?P<paren> \((?P<pin>{CJK_RUN}(?:, {CJK_RUN})*)\))|(?P<sp> )(?P<run>{CJK_RUN})")
AFTER_OK = re.compile(r"(?:[\s,.;:!?)\]*'\"’”–]|$)")
WORD = re.compile(rf"^(?![{CH}])[^\W\d_](?:(?![{CH}])[^\W_]|['’–-])*$")   # a word in Latin script
FUNC = {"him", "her", "me", "us", "them", "it", "as", "is", "was", "are", "were", "be", "called", "named", "titled",
        "reads", "read", "says", "said", "writes", "wrote", "word", "words", "name", "names", "and", "or", "but",
        "headed", "entitled", "quotes", "quoted", "reading"}
# a plain noun that introduces words rather than glossing them ("the slogan 三面红旗", "the line 不到长城非好汉"): no
# label alone; a term of its own words keeps it ("the general line 总路线")
INTRO = {"slogan", "slogans", "line", "lines", "inscription", "phrase", "motto", "banner", "title", "text", "verse",
         "couplet", "characters"}
HONOR = {"Comrade", "Comrades"}     # "Comrade Lei Feng 雷锋": the label the name
STOP = {"the", "a", "an", "of", "on", "in", "at", "to", "for", "by", "with", "from", "and", "or", "his", "her", "its",
        "their", "our", "my", "as", "is", "was", "are", "were", "into", "about", "against", "under", "over", "after",
        "before", "this", "that", "these", "those", "some", "any", "no", "not", "each", "every", "all", "both", "than",
        "then", "also", "he", "she", "it", "they", "we", "him", "them", "who", "which", "whom", "whose", "where", "when",
        "but", "so", "if", "at", "upon", "via", "per", "between", "among", "through", "during", "until", "since",
        "why", "what", "how"}
CAPSTOP = {w.capitalize() for w in STOP} - {"He", "An"}   # He Long 贺龙, An Ziwen 安子文: a surname, not the word
CONNECT = {"of", "for", "de", "du", "la", "van", "von", "der", "bin", "al"}
POSS = re.compile(r"['’]s$")


def _quoted(before):
    """The quoted phrase `before` ends with ('"buying-out"', its start), quotes chained by 'and' taken whole; or None."""
    m = re.search(r"(?:^|(?<=[\s(\[]))(\"[^\"]+\"|“[^”]+”|'[^']+'|‘[^’]+’)$", before)
    if not m:
        return None
    start = m.start()
    while True:
        m2 = re.search(r"(?:^|(?<=[\s(\[]))(\"[^\"]+\"|“[^”]+”) and $", before[:start])
        if not m2:
            break
        start = m2.start()
    return before[start:], start


OPEN = "([\"“'‘"


def _label(before, joined=False):
    """The romanized word or words a run glosses: the end of `before` (STYLE 2); None where the run glosses nothing.
    joined: names joined by "and" taken together (a parenthesis of several names' characters)."""
    if not before:
        return None
    it = re.search(r"\*[^*]+\*(?=(?:['’]s)?$)", before)       # an italic title, its possessive aside, without
    if it:                                                      # the glosses inside it
        return split(it.group(0))[0] if HAS.search(it.group(0)) else it.group(0)
    if before.endswith("*"):
        return None
    if before[-1] in "\"”'’" and not POSS.search(before):
        q = _quoted(before)
        if q:
            return q[0]
        if before[-1] not in "'’":
            return None
        before = before[:-1]                         # a plural's possessive ("the Anshan Steel Works' 鞍钢")
    xx = re.search(r" (×+)$", before)                 # "Zhang ×× 张××": the name's ×× with it
    if xx:
        lab = _label(before[:xx.start()], joined)
        return f"{lab} {xx.group(1)}" if lab and lab[0].isupper() and " " not in lab else None
    toks = before.split(" ")
    if "–" in toks[-1] and HAS.search(toks[-1]):     # "Guiyang 贵阳–Kunming 昆明": the word after the dash
        toks = [toks[-1].rsplit("–", 1)[1]]
    last = toks[-1]
    opened = last[:1] in OPEN                    # "(Mai Ye, 麦耶)": the parenthesis opens the label
    last = last.lstrip(OPEN)
    if not last or not WORD.match(last):
        return None
    low = last.lower()
    if last[0].islower() and (low in FUNC or low in STOP):
        return None                              # "led by 莫纳·孟杜": the sentence's own words, not a gloss
    if last in CAPSTOP:
        return None                              # "The 23条": no word to gloss
    got = [last]
    cap = last[0].isupper()
    in_title = before.count("*") % 2 == 1        # "*Selected Works of Mao Zedong 毛泽东*": the name in the title
    for t in ([] if opened else reversed(toks[:-1])):
        stop = t[:1] in OPEN
        t = t.lstrip(OPEN)
        if not t or not WORD.match(t) or len(got) >= 8:
            break
        if cap:
            if t[0].isupper() and t not in CAPSTOP:
                got.append(t)
            elif (t in CONNECT or (joined and t == "and")) and not stop and not in_title:
                got.append(t)
            else:
                break
        else:
            if t.lower() in STOP or t.lower() in FUNC or t.lower() in INTRO or len(got) >= 5:
                break                            # "the phrase dazibao 大字报": the term, not the phrase
            got.append(t)
        if stop:
            break
    while got and (got[-1] in CONNECT or got[-1] == "and"):
        got.pop()
    if len(got) == 1 and got[0] in INTRO:
        return None                              # "the slogan 三面红旗": the words themselves, not a gloss
    while len(got) > 1 and got[-1] in HONOR:
        got.pop()                                # "Comrade Lei Feng": the name
    return POSS.sub("", " ".join(reversed(got)))


def _inside_quote(before):
    return before.count('"') % 2 == 1 or before.count("“") > before.count("”")


def _quote_open(before):
    """Where the quotation `before` is inside opens (the index after its mark)."""
    a = before.rfind('"') if before.count('"') % 2 == 1 else -1
    b = before.rfind("“") if before.count("“") > before.count("”") else -1
    return max(a, b) + 1


def _namey(label):
    """A label a quotation's gloss may have (STYLE 2): a name or title, its glossed (last) word capitalized, or
    italic, or a term in pinyin."""
    words = label.strip("*").split()
    return bool(words) and (words[-1][0].isupper() or label[0] == "*" or all(PINYIN.match(w) for w in words))


def _script(run):
    return "hangul" if re.search("[가-힯]", run) else "kana" if re.search("[぀-ヿ]", run) else "han"


SECOND = re.compile(rf" \(({CJK_RUN})\)")
# a quoted original in characters and its English after it, '"中央决定进行反击战役" (the Center has decided on a
# counterattack)'; or the English and the original after it in parentheses, 'respond positively ("积极响应")'
_ORIG = rf"[^\"“”A-Za-z]*[{CH}][^\"“”A-Za-z]*"
Q_AFTER = re.compile(rf"(?P<q>[\"“])(?P<orig>{_ORIG})[\"”] \((?P<eng>[^()]*(?:\([^()]*\)[^()]*)*)\)")
Q_BEFORE = re.compile(rf" \([\"“](?P<orig>{_ORIG})[\"”]\)")
NOT_EN = re.compile(r"^(?:so printed|sic|as printed|the (?:nianpu|book|diary|editors?)|in the |p\. |\d)", re.I)


def quotes(text):
    """(the line with each quoted original that has its English beside it out, the English in its quotation marks;
    [the originals, as written]) (STYLE 7)."""
    if not text or not HAS.search(text):
        return text, []
    words = []

    def after(m):
        eng = m.group("eng").strip()
        if not re.search("[A-Za-z]", eng) or HAS.search(eng) or NOT_EN.match(eng):
            return m.group(0)
        words.append(m.group("orig"))
        eng = eng[1:-1] if len(eng) > 1 and eng[0] in "\"“" and eng[-1] in "\"”" else eng
        return f'{m.group("q")}{eng}{"”" if m.group("q") == "“" else chr(34)}'

    def before(m):
        b = text[:m.start()].rstrip()
        if not b or not re.search(r"[A-Za-z][\"”']?$", b):
            return m.group(0)
        words.append(m.group("orig"))
        return ""
    text = Q_AFTER.sub(after, text)
    text = Q_BEFORE.sub(before, text)
    return text, words


def split(text):
    """(the line without its glossing runs, [(label, characters)]) (STYLE 2); its quoted originals out first
    (quotes, STYLE 7)."""
    if not text or not HAS.search(text):
        return text, []
    text = quotes(text)[0]
    if not HAS.search(text):
        return text, []
    out, pairs, pos = [], [], 0
    for m in LINE.finditer(text):
        if m.start() < pos:
            continue                                 # taken with the run before (a second script)
        before = text[:m.start()]
        if not AFTER_OK.match(text, m.end()):
            continue
        if _inside_quote(before):                    # a translated quotation: a name's gloss in it goes too, the
            q = _quote_open(before)                  # quotation's own words in characters stay (STYLE 2)
            inner = _label(before[q:]) if before[q:].strip() else None
            if m.group("paren") or not inner or not _namey(inner):
                continue
        if m.group("paren"):
            chars = m.group("pin").split(", ")
            if pairs and m.start() == pos:           # "Liu Shaoqi 刘少奇 and Deng Xiaoping 邓小平 (刘邓)": the line as
                lab = _label("".join(out), joined=True)   # shown labels it, as a second pass would ("drop" twice)
            else:
                lab = _label(before, joined=len(chars) > 1)
            if lab is None:
                continue
            out.append(text[pos:m.start()])
            labs = [re.sub(r"^\S+['’]s ", "", x) for x in re.split(r",? and |, ", lab)]
            if len(chars) > 1 and len(labs) == len(chars):     # "Phạm Hùng and Lê Trọng Tấn (范雄, 黎仲迅)": each its own
                pairs += list(zip(labs, chars))
            else:
                pairs.append((lab, m.group("pin")))
            pos = m.end()
            continue
        cut = m.start()
        b = before
        comma = re.search(r",([\"”'’]?)$", b)
        if comma:                                    # "(Mai Ye, 麦耶)": a gloss only where the parenthesis closes
            if text[m.end():m.end() + 1] != ")":
                continue
            b = b[:comma.start()] + comma.group(1)
        lab = _label(b) if b else None
        if lab is None or (m.group("run")[0] in "「『" and lab[0] not in "\"“'‘"):
            continue                                 # words quoted in corner brackets gloss only a quotation
        if comma:                                    # ... and only where the label is all it holds ("the" aside)
            inner = re.search(r"\(([^()]*)$", b)
            if not inner or re.sub(r"^(?:the|a|an) ", "", inner.group(1)).rstrip("\"”'’").lstrip("\"“'‘") \
                    != lab.strip("\"”'’“‘"):
                continue
            out.append(text[pos:comma.start()] + comma.group(1))
        else:
            out.append(text[pos:cut])
        run, pos = m.group("run"), m.end()
        s2 = SECOND.match(text, pos)                 # "Kim Il Sung 김일성 (金日成)": a second script with the first
        if s2 and _script(s2.group(1)) != _script(run) and AFTER_OK.match(text, s2.end()):
            run, pos = f"{run} ({s2.group(1)})", s2.end()
        pairs.append((lab, run))
    out.append(text[pos:])
    return "".join(out), pairs


def drop(text):
    """The line as shown: its glossing runs dropped (STYLE 2)."""
    return split(text)[0]


# ---------------------------------------------------------------- pinyin

# a word in pinyin, toneless, syllables joined or hyphenated
SYL = (r"(?:zh|ch|sh|[bpmfdtnlgkhjqxrzcsyw])?(?:iang|iong|uang|ueng|ang|eng|ing|ong|ian|iao|uai|uan|ai|ei|ao|ou|an|en"
       r"|in|un|ia|ie|iu|ua|uo|ui|ue|üe|er|a|o|e|i|u|ü|v)r?")
PINYIN = re.compile(rf"(?i)^(?:{SYL})+(?:[-'’](?:{SYL})+)*$")


# ---------------------------------------------------------------- the page (STYLE 3)

def _linker(series):
    """The series' Linker, once (build.Linker: who a 'Names:' token means)."""
    if getattr(series, "_cjk_linker", None) is None:
        from .build import Linker
        series._cjk_linker = Linker(series)
    return series._cjk_linker


def _name_chars(series):
    """{name entry's address: characters}, from the person entries' subject lines that record them ("Huang Hua 黄华"):
    a person's own, found as the 'Names:' line finds him (build.Linker), never by a surname or given name alone."""
    if getattr(series, "_cjk_names", None) is None:
        from . import namelinks
        from .markup import plain
        lk, out = _linker(series), {}
        for lst in series.lists.values():
            if lst.kind == "calendar":
                continue
            for sec, e in lst.entries():
                if not e.get("s") or not HAS.search(str(e["s"])) or not lk.refs.is_person(lst, sec, e):
                    continue
                for s in re.split(r";\s*", plain(str(e["s"]))):
                    m = re.match(rf"^(.+?) ({CJK_RUN})$", s.strip())
                    if not m or HAS.search(m.group(1)):
                        continue
                    hits = lk._named_hits(m.group(1))   # his name entry: the one this entry is, or the name's own
                    us = [u for u, x in hits.items() if x is e] or [namelinks.url(series, m.group(1))]
                    for u in us:
                        if u:
                            out.setdefault(_key(u), m.group(2))
        series._cjk_names = out
    return series._cjk_names


def _key(u):
    """A name entry's address as its key ('zhou-enlai'): the tags' and the Linker's forms alike."""
    return str(u).rsplit("#", 1)[-1]


def _surname(token, east):
    """The token's surname: its first word for a name in East Asian order (`east`: its person's characters are known,
    or every word is pinyin), else its last."""
    w = token.split()
    return w[0] if east or all(PINYIN.match(x) for x in w) else w[-1]


def _fits(label, token, east=False):
    """Whether a pair's label names the person of a 'Names:' token: the token itself, or its surname alone ('Mao' for
    'Mao Zedong'); never a given name ('Xiaoping'), a label running on past the token ('Mao Yuanxin' for 'Mao', 'Mao
    Zedong Thought'), or a title in quotation marks or italics (STYLE 3). A label longer than the token is _longer's."""
    from . import store
    if not label or label[0] in "*\"“'‘":
        return False
    a, b = store.fold(label).split(), store.fold(token).split()
    if not a or not b or len(a) > len(b):
        return False
    return a == b or (len(a) == 1 and a[0] == store.fold(_surname(token, east)))


def _longer(label, token):
    """How a pair's label holds a 'Names:' token, its words capitalized and not in quotation marks or italics:
    'after', the whole token after other words (a title, a given name, a stray word: 'Vice-Premier Li Xiannian',
    'Sékou Touré'); 'before', the token followed by more ('Nosaka Sanzō' for 'Nosaka'; 'Mao Yuanxin' for 'Mao', a
    different man, which plan rejects unless the Linker finds the two one person); else None."""
    from . import store
    if not label or label[0] in "*\"“'‘":
        return None
    a, b = store.fold(label).split(), store.fold(token).split()
    if len(a) <= len(b) or not all(w[:1].isupper() for w in label.split()):
        return None
    return "after" if a[-len(b):] == b else "before" if a[:len(b)] == b else None


def _names(n):
    """The note's 'Names:' tokens, bare."""
    from .build import names_line, names_tokens
    from .markup import plain
    parts = names_line(plain(n or ""))
    return [peel(t)[0] for t, _ in names_tokens(parts[1])] if parts else []


def peel(token):
    """A 'Names:' token and the characters after it: ('Liu Shaoqi', ' 刘少奇'), or (token, '')."""
    m = re.match(rf"^(.*?)( {CJK_RUN})$", token)
    return (m.group(1), m.group(2)) if m and m.group(1) else (token, "")


def plan(series, e):
    """The entry's characters for its citation block, before the page has a say: ([(token, characters)] for 'Names:',
    [(label, characters)] the line's other pairs, not shown: STYLE 3), each characters once."""
    cache = series.__dict__.setdefault("_cjk_plan", {})
    if e.get("id") in cache and cache[e["id"]][0] is e:
        return cache[e["id"]][1]
    pairs = []
    for c in (e.get("c") if isinstance(e.get("c"), list) else [e.get("c")]):
        pairs += split(str(c or ""))[1]
    toks = _names(e.get("n"))
    known = _name_chars(series)
    from . import store
    own = [None] * len(toks)                     # each token's person's characters, where his entry records them
    who = [None] * len(toks)                     # each token's person (his name entry's key)
    tags = {str(x)[5:] for x in e.get("tags") or [] if str(x).startswith("name:")}
    if toks:
        words = series.__dict__.setdefault("_cjk_words", {w for u in known for w in u.split("-")})
        if pairs or any(w in words for t in toks for w in store.fold(t).split()):
            for k, hit in enumerate(_linker(series).names_resolved(toks, tags)):
                who[k] = _key(hit[1]) if hit and hit[1] else None
                own[k] = known.get(who[k]) if who[k] else None

    def same(label, k):
        """Whether the Linker finds the label the token's person (None: it finds no one)."""
        hit = _linker(series).who_named(label, tags)
        return None if not hit or not hit[1] else (who[k] is not None and _key(hit[1]) == who[k])
    pick, used = [None] * len(toks), set()

    def take(k, i):
        pick[k] = i
        used.add(i)
    for k, t in enumerate(toks):                 # the token itself first ("Mao Zedong 毛泽东")
        i = next((i for i, (lab, _) in enumerate(pairs) if i not in used and store.fold(lab) == store.fold(t)
                  and lab[:1] not in "*\"“'‘"), None)
        if i is not None:
            take(k, i)
    for k, t in enumerate(toks):                 # then his own characters, however the line labels them
        if pick[k] is None and own[k]:
            i = next((i for i, (lab, ch) in enumerate(pairs) if i not in used and ch == own[k]
                      and lab[:1] not in "*\"“'‘"), None)
            if i is not None:
                take(k, i)
    for k, t in enumerate(toks):                 # then his surname alone, where no other token has it
        if pick[k] is not None:
            continue
        east = bool(own[k])
        sur = store.fold(_surname(t, east))
        if sum(1 for j, x in enumerate(toks) if pick[j] is None and store.fold(_surname(x, east)) == sur) > 1:
            continue                             # two unmatched tokens with the surname: neither takes it
        i = next((i for i, (lab, ch) in enumerate(pairs) if i not in used and _fits(lab, t, east)), None)
        if i is not None:
            take(k, i)
    for k, t in enumerate(toks):                 # then a longer label: words before the token, unless the Linker
        if pick[k] is not None:                  # finds them another man; words after it, only where it finds him
            continue
        befores = [lab for lab, _ in pairs if _longer(lab, t) == "before"]
        for i, (lab, ch) in enumerate(pairs):
            how = None if i in used else _longer(lab, t)
            if not how:
                continue
            s = same(lab, k)
            if (s is not False) if how == "after" else (s is True or (s is None and who[k] is None
                                                                       and len(befores) == 1)):
                take(k, i)                   # ('Nosaka Sanzō' for 'Nosaka', neither with a name entry: the one
                break                        # such label the line has)
    names, seen = [], set()
    for k, t in enumerate(toks):
        ch = pairs[pick[k]][1] if pick[k] is not None else own[k]
        if ch and ch not in seen:
            seen.add(ch)
            names.append((t, ch))
    rest = []
    for i, (lab, ch) in enumerate(pairs):
        if i in used:
            if ch not in seen:          # a second token's: shown with the first's
                seen.add(ch)
            continue
        if ch not in seen:
            seen.add(ch)
            rest.append((lab, ch))
    cache[e.get("id")] = (e, (names, rest))
    return names, rest


def firsts(series):
    """{(entry id, characters)}: a 'Names:' person's characters at their first appearance on each page of each
    calendar (STYLE 3)."""
    if getattr(series, "_first_cjk", None) is None:
        out = set()
        for lst in series.lists.values():
            if lst.kind != "calendar":
                continue
            seen = set()
            for h, e in page_rows(series, lst):      # the page's own order, a day's included (dayorder.page_rows)
                for _, r in plan(series, e)[0]:
                    if (h, r) not in seen:
                        seen.add((h, r))
                        out.add((e["id"], r))
        series._first_cjk = out
    return series._first_cjk


first_runs = firsts


def page_rows(series, lst):
    """dayorder.page_rows, once a series."""
    cache = series.__dict__.setdefault("_page_rows", {})
    if lst.key not in cache:
        from . import dayorder
        cache[lst.key] = dayorder.page_rows(lst)
    return cache[lst.key]


class Entry:
    """One entry's characters in its citation block: claim() the 'Names:' persons' it gives at their first on the
    page, then tail() the note: their characters after the names, the line's quoted originals in "The words:"."""

    def __init__(self, series, e):
        self.series, self.e = series, e
        self.names = plan(series, e)[0]
        self.words = [w for c in store_list(e.get("c")) for w in quotes(str(c or ""))[1]]

    def claim(self, done):
        first = firsts(self.series)
        eid = self.e["id"]

        def keep(ch):
            if (eid, ch) in first and ch not in done:
                done.add(ch)
                return True
            return False
        self.names = [(t, ch) for t, ch in self.names if keep(ch)]
        return self

    def tail(self, n, printed=frozenset()):
        """The note with its 'Names:' persons' characters after the names (STYLE 3), those a card's full cite in the
        same block prints not given again (`printed`: printed_by, works.py FIRST CITE); and the line's quoted
        originals, as written, in a sentence "The words: ..." before "Names:" (STYLE 7). Nothing of the note's own is
        dropped (STYLE 4)."""
        n = n or ""
        names = [(t, ch) for t, ch in self.names if ch not in printed]
        if names and "Names:" in n:
            n = with_names(n, dict(names))
        own = str(self.e.get("n") or "")             # the note as written, its footnotes' text too
        words = [w for w in self.words if w not in n and w not in own]
        if words:
            sent = "The words: " + "; ".join(words) + "."
            k = n.rfind("Names:")
            if k >= 0:
                n = n[:k] + sent + " " + n[k:]
            else:
                n = f"{n.rstrip()} {sent}" if n.strip() else sent
        return n


def store_list(v):
    return v if isinstance(v, list) else [v]


RUNS = re.compile(CJK_RUN)


def printed_by(before, after):
    """The runs of characters `after` (a text with its cards' full cites) has that `before` (the text as written) has
    not: those the cites print."""
    had = set(RUNS.findall(before or ""))
    return frozenset(r for r in RUNS.findall(after or "") if r not in had)


def with_names(n, chars):
    """The note's 'Names:' line with each named person's characters after the name."""
    from .build import names_line
    parts = names_line(n)
    if not parts:
        return n
    head, body, tail = n[:parts[0]], parts[1], parts[2]

    out = []
    for k, part in enumerate(re.split(r"(,\s*|;\s*|\s+and\s+)", body)):
        bare, own = peel(part.strip())
        if k % 2 == 0 and not own and bare in chars:
            part = part.rstrip() + " " + chars[bare] + part[len(part.rstrip()):]
        out.append(part)
    return head + "".join(out) + tail
