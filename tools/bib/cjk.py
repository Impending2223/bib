"""Characters after romanized Chinese, shown at their first appearance on a page (the owner, Nov. 18, 2026: "If we
can make the CJK appear the first time the word is given on a page, but not the later times, as we do for long
titles and short, I would also have us give the CJK for personal and place names").

STYLE
1. The data keeps the characters wherever a reader wrote them, after the romanized word, a space between:
   "fentian dangan 分田单干", "Tian Jiaying 田家英" (notes/guide/entries.md, after "Vietnamese names").
2. On a calendar page (a half, as tools/bib/works.py FIRST CITE counts them) a run of characters after a space is
   shown at its first appearance only, in the order the page shows the entries, the text (`c`) before the note
   (`n`) in each; later the run and its space are dropped. A run counts only where it glosses the word before it
   (pinyin, a capitalized name, an italic title: _gloss); characters inside parentheses or quotation marks, or
   standing as a sentence's own words ("the book names him 阿夫扎尔"), stay as written.
3. first_runs (the page's firsts, computed once) and strip (an entry's text, as shown).
"""
import re

RUN = re.compile(r" ([\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3005\u00b7\u30fb]+)(?=[\s,.;:!?)\]*'\"\u2019\u201d]|$)")
# the word before: pinyin (toneless, syllables joined or hyphenated) or a capitalized word (a name in another
# romanization, "Chiang Kai-shek 蔣介石"), or an italic title's closing star ("*Hongqi* 红旗")
SYL = (r"(?:zh|ch|sh|[bpmfdtnlgkhjqxrzcsyw])?(?:iang|iong|uang|ueng|ang|eng|ing|ong|ian|iao|uai|uan|ai|ei|ao|ou|an|en"
       r"|in|un|ia|ie|iu|ua|uo|ui|ue|üe|er|a|o|e|i|u|ü|v)r?")
PINYIN = re.compile(rf"(?i)^(?:{SYL})+(?:[-'’](?:{SYL})+)*$")
ENGLISH = {"a", "an", "he", "she", "her", "in", "and", "or", "the", "of", "as", "is", "him", "me", "men"}


def _gloss(text, m):
    """A run of characters glossing the romanized word before it, outside parentheses and quotation marks."""
    before = text[: m.start()]
    if before.count("(") > before.count(")") or before.count('"') % 2 or before.count("\u201c") > before.count("\u201d"):
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


def first_runs(series):
    """{(entry id, run)}: each run's first appearance on each page of each calendar."""
    if getattr(series, "_first_cjk", None) is None:
        from . import calsplit, loose, store
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
                text = " ".join(str(c) for c in store.as_list(e.get("c"))) + " " + str(e.get("n") or "")
                for r in runs(text):
                    if (h, r) not in seen:
                        seen.add((h, r))
                        out.add((e["id"], r))
        series._first_cjk = out
    return series._first_cjk


def strip(series, e, text, done):
    """The text with each run shown only where it first appears on the page; `done` is the entry's own set of runs
    already shown (the text before the note)."""
    if not text or not RUN.search(text):
        return text
    first = first_runs(series)

    def sub(m):
        r = m.group(1)
        if not _gloss(text, m):
            return m.group(0)
        if (e["id"], r) in first and r not in done:
            done.add(r)
            return m.group(0)
        return ""
    return RUN.sub(sub, text)
