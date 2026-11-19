"""Characters (漢字, kana, hangul) out of the line and into the citation block (the owner, Nov. 19, 2026: "I've changed
my mind on writing CJK after place, personal names, and titles in the body text. Drop them. Keep them in the citation
block."; "Do we not have 'give the CJK of personal names, location, work titles, etc., on their first appearance' as a
standing rule for the citation block? Names in 'Names:' should have their CJK given on their first appearance on a
page."). Before, Nov. 18: "If we can make the CJK appear the first time the word is given on a page, but not the later
times, as we do for long titles and short, I would also have us give the CJK for personal and place names".

STYLE
1. The data keeps the characters wherever a reader wrote them, after the romanized word, a space between:
   "fentian dangan 分田单干", "Tian Jiaying 田家英", "*Hongqi* 红旗", "(the "buying-out," 赎买)"
   (notes/guide/entries.md, "Characters"). The display moves them; nothing in the data changes, and the move is undone
   by changing this file alone.
2. The line (`c`): a run of characters glossing the word or words before it (split: a romanized name, place, term, an
   italic title, a quoted phrase; _label finds them) is dropped with its joining space; so too a parenthesis holding
   characters alone ("... one side" (工商业者应当下决心...)"), and the comma of "(Mai Ye, 麦耶)" or "("Victory
   Goddess," 胜利女神)" with its run. Kept where they are: characters inside a quotation, characters standing as the
   sentence's own words ("the departing Romanian ambassador, 乔治乌"; "the book names him 阿夫扎尔"), anything that
   follows no word. Vietnamese is not touched (it is Latin script).
3. Each dropped run leaves a pair (its label, its characters), shown in the citation block at its first appearance on
   the page (a calendar half, as tools/bib/works.py FIRST CITE counts pages; the entries in the page's order; in an
   entry its line before its note): a person in the note's "Names:" sentence takes them after the name ("Names: Liu
   Shaoqi 刘少奇, Deng Xiaoping 邓小平."), from the entry's own pairs, or else from the person's name entry where its
   subject line records them ("Huang Hua 黄华"); every other pair in one closing sentence, "Characters: Hangzhou 杭州;
   Henan Provincial Supervisory Committee 河南省监委; *Hongqi* 红旗." (the label "Characters:" the series' own; the
   owner named none). Later on the page the same characters are not given again.
4. The note (`n`) keeps its own runs in place (the citation block), shown at their first appearance on the page and
   dropped after, as before (runs, _gloss; strip).
5. A work's characters are its card's (`script`), given at its first cite (works.py FIRST CITE), not here.
6. The claims' units (claims.py), the footnotes' marks (footnotes.py) and the visibility spans (vispage.py) are found
   in the line as rendered: their units are rendered through drop() too (build._unit_renderer).
"""
import re

CH = "㐀-䶿一-鿿豈-﫿々〇぀-ヿ가-힯"
PUNCT = "、。，：；·・“”「-』（）—"
_X = rf"(?:《[^》\n]*》|〈[^〉\n]*〉|[{CH}])(?:《[^》\n]*》|〈[^〉\n]*〉|[{CH}{PUNCT}])*"
CJK_RUN = rf"{_X}(?: {_X})*"                       # a run: characters, their punctuation, a space between words
HAS = re.compile(rf"[{CH}《〈]")
LINE = re.compile(rf"(?P<paren> \((?P<pin>{CJK_RUN}(?:, {CJK_RUN})*)\))|(?P<sp> )(?P<run>{CJK_RUN})")
AFTER_OK = re.compile(r"(?:[\s,.;:!?)\]*'\"’”]|$)")
WORD = re.compile(r"^[^\W\d_](?:[^\W_]|['’-])*$")
FUNC = {"him", "her", "me", "us", "them", "it", "as", "is", "was", "are", "were", "be", "called", "named", "titled",
        "reads", "read", "says", "said", "writes", "wrote", "word", "words", "name", "names", "and", "or", "but"}
STOP = {"the", "a", "an", "of", "on", "in", "at", "to", "for", "by", "with", "from", "and", "or", "his", "her", "its",
        "their", "our", "my", "as", "is", "was", "are", "were", "into", "about", "against", "under", "over", "after",
        "before", "this", "that", "these", "those", "some", "any", "no", "not", "each", "every", "all", "both", "than",
        "then", "also", "he", "she", "it", "they", "we", "him", "them", "who", "which", "whom", "whose", "where", "when",
        "but", "so", "if", "at", "upon", "via", "per", "between", "among", "through", "during", "until", "since"}
CAPSTOP = {w.capitalize() for w in STOP} - {"He"}       # He Jun 何均, He Long 贺龙: a surname, not the pronoun
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
    if before.endswith("*"):
        m = re.search(r"\*[^*]+\*$", before)
        return m.group(0) if m else None
    if before[-1] in "\"”'’" and not POSS.search(before):
        q = _quoted(before)
        return q[0] if q else None
    toks = before.split(" ")
    last = toks[-1]
    opened = last[:1] in OPEN                    # "(Mai Ye, 麦耶)": the parenthesis opens the label
    last = last.lstrip(OPEN)
    if not last or not WORD.match(last):
        return None
    if last[0].islower() and last.lower() in FUNC:
        return None
    got = [last]
    cap = last[0].isupper()
    for t in ([] if opened else reversed(toks[:-1])):
        stop = t[:1] in OPEN
        t = t.lstrip(OPEN)
        if not t or not WORD.match(t) or len(got) >= 8:
            break
        if cap:
            if t[0].isupper() and t not in CAPSTOP:
                got.append(t)
            elif (t in CONNECT or (joined and t == "and")) and not stop:
                got.append(t)
            else:
                break
        else:
            if t.lower() in STOP or len(got) >= 5:
                break
            got.append(t)
        if stop:
            break
    while got and (got[-1] in CONNECT or got[-1] == "and"):
        got.pop()
    return POSS.sub("", " ".join(reversed(got)))


def _inside_quote(before):
    return before.count('"') % 2 == 1 or before.count("“") > before.count("”")


def split(text):
    """(the line without its glossing runs, [(label, characters)]) (STYLE 2)."""
    if not text or not HAS.search(text):
        return text, []
    out, pairs, pos = [], [], 0
    for m in LINE.finditer(text):
        before = text[:m.start()]
        if not AFTER_OK.match(text, m.end()) or _inside_quote(before):
            continue
        if m.group("paren"):
            chars = m.group("pin").split(", ")
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
        if lab is None:
            continue
        if comma:                                    # ... and only where the label is all it holds ("the" aside)
            inner = re.search(r"\(([^()]*)$", b)
            if not inner or re.sub(r"^(?:the|a|an) ", "", inner.group(1)).rstrip("\"”'’").lstrip("\"“'‘") \
                    != lab.strip("\"”'’“‘"):
                continue
            out.append(text[pos:comma.start()] + comma.group(1))
        else:
            out.append(text[pos:cut])
        pairs.append((lab, m.group("run")))
        pos = m.end()
    out.append(text[pos:])
    return "".join(out), pairs


def drop(text):
    """The line as shown: its glossing runs dropped (STYLE 2)."""
    return split(text)[0]


# ---------------------------------------------------------------- the note's own runs (STYLE 4)

RUN = re.compile(r" ([㐀-䶿一-鿿豈-﫿々·・]+)(?=[\s,.;:!?)\]*'\"’”]|$)")
# the word before: pinyin (toneless, syllables joined or hyphenated) or a capitalized word (a name in another
# romanization, "Chiang Kai-shek 蔣介石"), or an italic title's closing star ("*Hongqi* 红旗")
SYL = (r"(?:zh|ch|sh|[bpmfdtnlgkhjqxrzcsyw])?(?:iang|iong|uang|ueng|ang|eng|ing|ong|ian|iao|uai|uan|ai|ei|ao|ou|an|en"
       r"|in|un|ia|ie|iu|ua|uo|ui|ue|üe|er|a|o|e|i|u|ü|v)r?")
PINYIN = re.compile(rf"(?i)^(?:{SYL})+(?:[-'’](?:{SYL})+)*$")
ENGLISH = {"a", "an", "he", "she", "her", "in", "and", "or", "the", "of", "as", "is", "him", "me", "men"}


def _gloss(text, m):
    """A run of characters glossing the romanized word before it, outside parentheses and quotation marks."""
    before = text[: m.start()]
    if before.count("(") > before.count(")") or before.count('"') % 2 or before.count("“") > before.count("”"):
        return False
    w = re.search(r"(\S+)$", before)
    if not w:
        return False
    w = w.group(1)
    if w.endswith("*"):
        return True
    w = w.strip("'’")
    if not re.fullmatch(r"[A-Za-zÀ-ÿ'’-]+", w) or w.lower() in ENGLISH:
        return False
    return bool(PINYIN.match(w)) or w[0].isupper()


def runs(text):
    text = text or ""
    return [m.group(1) for m in RUN.finditer(text) if _gloss(text, m)]


# ---------------------------------------------------------------- the page (STYLE 3)

def _name_chars(series):
    """{folded name: characters} from the name entries' subject lines ("Huang Hua 黄华"); a surname alone where one
    person has it."""
    if getattr(series, "_cjk_names", None) is None:
        from . import store
        full, part = {}, {}
        for lst in series.lists.values():
            if lst.kind == "calendar":
                continue
            for _, e in lst.entries():
                for s in re.split(r";\s*", str(e.get("s") or "")):
                    m = re.match(rf"^(.+?) ({CJK_RUN})$", s.strip())
                    if not m or HAS.search(m.group(1)):
                        continue
                    k = store.fold(m.group(1))
                    full.setdefault(k, m.group(2))
                    for w in {k.split()[0], k.split()[-1]}:
                        part.setdefault(w, set()).add(m.group(2))
        for w, v in part.items():
            if len(v) == 1 and w not in full:
                full[w] = next(iter(v))
        series._cjk_names = full
    return series._cjk_names


def _fits(label, token):
    """Whether a pair's label names the person of a 'Names:' token: the one's words the other's, or their start or
    end ('Mao' and 'Mao Zedong'; 'Liu Shaoqi' and 'Liu')."""
    from . import store
    a, b = store.fold(label).split(), store.fold(token).split()
    if not a or not b:
        return False
    n = min(len(a), len(b))
    return a[:n] == b[:n] or a[-n:] == b[-n:]


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
    [(label, characters)] for 'Characters:'), each characters once."""
    pairs = []
    for c in (e.get("c") if isinstance(e.get("c"), list) else [e.get("c")]):
        pairs += split(str(c or ""))[1]
    toks = _names(e.get("n"))
    names, used, seen = [], set(), set()
    known = _name_chars(series)
    from . import store
    for t in toks:
        hit = next((i for i, (lab, _) in enumerate(pairs) if i not in used and _fits(lab, t)), None)
        if hit is not None:
            used.add(hit)
            ch = pairs[hit][1]
        else:
            ch = known.get(store.fold(t))
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
    return names, rest


def firsts(series):
    """{(entry id, characters)}: each run's first appearance on each page of each calendar (STYLE 3, 4)."""
    if getattr(series, "_first_cjk", None) is None:
        from . import calsplit, loose
        out = set()
        for lst in series.lists.values():
            if lst.kind != "calendar":
                continue
            rows = []
            for k, sec in enumerate(lst.walk()):
                for i, e in enumerate(sec.entries):
                    if e["id"].startswith(f"{lst.key}.thread."):
                        continue
                    h = (calsplit.half_of_date(lst, loose.place_iso(e)) if loose.moves(e) and calsplit.cfg(lst)
                         else (calsplit.half_of_section(lst, sec) or 1))
                    rows.append((h, loose.order_key(e), k, i, e))
            seen = set()
            for h, _, _, _, e in sorted(rows, key=lambda r: r[:4]):
                names, rest = plan(series, e)
                for r in [ch for _, ch in names] + [ch for _, ch in rest] + runs(str(e.get("n") or "")):
                    if (h, r) not in seen:
                        seen.add((h, r))
                        out.add((e["id"], r))
        series._first_cjk = out
    return series._first_cjk


first_runs = firsts


class Entry:
    """One entry's characters on its page: claim() what the citation block gives (before the note's own runs are
    stripped, so a run the line gave is not given twice), then tail() the note."""

    def __init__(self, series, e):
        self.series, self.e = series, e
        self.names, self.rest = plan(series, e)

    def claim(self, done):
        first = firsts(self.series)
        eid = self.e["id"]

        def keep(ch):
            if (eid, ch) in first and ch not in done:
                done.add(ch)
                return True
            return False
        self.names = [(t, ch) for t, ch in self.names if keep(ch)]
        self.rest = [(lab, ch) for lab, ch in self.rest if keep(ch)]
        return self

    def tail(self, n):
        """The note with the characters of its 'Names:' and its closing 'Characters:' sentence (STYLE 3)."""
        n = n or ""
        if self.names and "Names:" in n:
            n = with_names(n, dict(self.names))
        if self.rest:
            sent = "Characters: " + "; ".join(f"{lab} {ch}" for lab, ch in self.rest) + "."
            n = f"{n.rstrip()} {sent}" if n.strip() else sent
        return n


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


def strip(series, e, text, done):
    """The note's text with each of its own runs shown only where it first appears on the page; `done` is the entry's
    own set of characters already shown (STYLE 4)."""
    if not text or not RUN.search(text):
        return text
    first = firsts(series)

    def sub(m):
        r = m.group(1)
        if not _gloss(text, m):
            return m.group(0)
        if (e["id"], r) in first and r not in done:
            done.add(r)
            return m.group(0)
        return ""
    return RUN.sub(sub, text)
