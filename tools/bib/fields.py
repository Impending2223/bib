"""The fields on every entry a reader adds: the time, the approximate date, the place (the owner, Nov. 19, 2026: "Do our
readers and auditors not know to enter the date, time, approximate date, approximate time, and location fields we
are asking for? Are we not asking for them? Could we fix that? Permanently?"; the reader's brief, R25a).

    ./bib fields ID [ID...]          the findings for entries of the tree
    ./bib fields --patch P [P...]    the findings for a patch's calendar adds

STYLE
 1. Three detectors, each on a calendar entry as a patch adds it (patch-check runs them on every calendar `add`, after
    the patch is applied in the dry run; not on cites or edits):
    [fields-time]  no `time` and no `time_range`, and the record gives the hour or the part of the day: a clock time
                   ("10 p.m.", "10:30 a.m.", "noon", "midnight", "2140Z", "at 4", "4 o'clock"), a part of the day
                   ("morning", "afternoon", "evening", "that night", "late at night", "at dawn", "at lunch", "at
                   dinner", "over breakfast"), in Chinese (上午 下午 晚上 凌晨 深夜, 十時, 9点钟), Russian ("в 10 часов",
                   утром, вечером, ночью) or Vietnamese (sáng, chiều, tối, đêm before a day; "10 giờ"); anywhere in `c`
                   or `when`, and in `n` only inside a parenthetical (where a source's pinpoint is glossed). A
                   newspaper's name or "the morning papers" is not a time (EXCEPT; a capitalized Morning or Evening
                   inside a sentence is a title).
    [fields-at]    a loose entry (a month or a year, loose.is_loose) with no `at`, where loose.at_for gives one from
                   `when`, or where `when` carries a qualifier, or `c` a position word for its month or year ("early",
                   "mid-", "late", "end of", "first week", "the eve of", "shortly after", a season).
    [fields-place] no `place`, and `c` or `when` names a gazetteer place: a row's `name` or an alias, as whole words
                   (Peking, Saigon, Moscow, Hangzhou; "Anniston, Ala." whole). A State (kind: state) is skipped: whether
                   the State is the act's scene is too subtle for a word match.
 2. Each is silenced by setting its field, or by the tag `ok:fields-time`, `ok:fields-at`, `ok:fields-place` where the
    words are not the act's (a city named as a subject, not the scene; a time of another event).
 3. LEVEL says which are errors in patch-check and which warnings: measured on the open and the last twenty merged
    patches (Nov. 19, 2026), a detector whose false hits passed about a fifth is a warning.
 4. Each message names the words that fired, where, and the fix.
"""
import re

from . import loose, places, store

LEVEL = {"fields-time": "error", "fields-at": "error", "fields-place": "warning"}

# -- time ---------------------------------------------------------------------------------------------------------------
_CN_NUM = r"(?:\d{1,2}|[二三五六七八九十]|十[一二]|[一二]十[一二三四五六七八九]?)"
TIME_PATTERNS = [
    r"\b\d{1,2}(?::\d\d)?\s*[ap]\.\s?m\.",
    r"\b\d{1,2}(?::\d\d)?\s*o'clock\b",
    r"\b(?:noon|midnight|midday|mid-morning|midafternoon|mid-afternoon)\b",
    r"\b[0-2]\d[0-5]\dZ\b",
    r"\bat (?:about )?\d{1,2}(?::\d\d)?(?![.,:]?\d)(?=[,.;)]|\s*$| in the | that | on )",
    r"\b(?:morning|afternoon|evening|night-time|nighttime|overnight)\b",
    r"\b(?:that|this|the same|late|last|the) night\b|\bat night\b|\bin the night\b|\blate at night\b|\bnight of\b",
    r"\b(?:at|before|by) (?:dawn|daybreak|dusk|sunrise|sunset|first light)\b",
    r"\b(?:at|over|during|after) (?:a |the |an? \w+ )?(?:breakfast|lunch|luncheon|dinner|supper)\b",
    r"上午|下午|晚上|凌晨|深夜|中午|清晨|早晨|傍晚|午夜|晚間|晚间|夜間|夜间|當晚|当晚|當夜|当夜",
    _CN_NUM + r"(?:時|时)(?![期代間间候局事常刻光節节])(?:半|\d{1,2}分|[一二三四五六七八九十]+分)?",
    _CN_NUM + r"(?:點鐘|点钟|點半|点半|點\d{1,2}分|点\d{1,2}分)",
    r"\bв \d{1,2}(?:[.:]\d\d)?\s*(?:час|ч\.)",
    r"(?<!\w)(?:утром|вечером|ночью|днём|днем)(?!\w)",
    r"\b\d{1,2}\s*giờ\b",
    r"(?<!\w)(?:buổi )?(?:sáng|chiều|tối|trưa)(?= (?:ngày|hôm|nay|qua|mai|sớm|muộn|\d))",
    r"(?<!\w)đêm(?!\w)",
]
TIME = re.compile("|".join(f"(?:{p})" for p in TIME_PATTERNS), re.IGNORECASE)
# a part of the day that names something else: a newspaper, an edition, a broadcast
EXCEPT = re.compile(r"\b(?:morning|evening|afternoon)\s+(?:papers?|newspapers?|press|editions?|daily|dailies|news|"
                    r"star|post|sun|herald|standard|bulletin|journal|tribune|call|telegraph|chronicle|express|"
                    r"examiner|ledger|world|times|record|globe|gazette|independent|leader|report)\b|"
                    r"\b(?:sunday|saturday)\s+(?:morning|evening)\s+post\b|\bgood (?:morning|evening)\b|"
                    r"\bmorning star\b|\bevening of (?:his|her|their) (?:life|lives|career)\b", re.IGNORECASE)
_TITLE_WORD = re.compile(r"^(?:Morning|Evening|Afternoon|Night)$")


def _strip_markup(s):
    s = re.sub(r"\]\((?:https?://)[^)\s]*\)", "]", s)          # a link's address
    s = re.sub(r"https?://\S+", " ", s)
    s = re.sub(r"\[\[[^\]]*\]\]", " ", s)                      # a card's id
    return s


def _italics(s):
    return [(m.start(), m.end()) for m in re.finditer(r"\*[^*\n]+\*", s)]


_OTHER_DAY = re.compile(r"^\s+of (?:the )?(Jan\.|Feb\.|Mar\.|Apr\.|May|June|July|Aug\.|Sept\.|Oct\.|Nov\.|Dec\.|"
                        r"January|February|March|April|August|September|October|November|December) (\d{1,2})\b")


def _month_no(w):
    """'Sept.' or 'September' -> 9."""
    w = w.rstrip(".")
    for i, m in enumerate(("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")):
        if w.startswith(m):
            return i + 1
    return None


def _quoted(s):
    return [(m.start(), m.end()) for m in re.finditer(r'"[^"\n]*"|“[^”\n]*”', s)]


def _time_hits(s, date=""):
    s = _strip_markup(s)
    spans = [(m.start(), m.end()) for m in EXCEPT.finditer(s)] + _italics(s) + _quoted(s)
    out = []
    for m in TIME.finditer(s):
        if any(a <= m.start() < b for a, b in spans):
            continue
        od = _OTHER_DAY.match(s[m.end():])
        if od and len(date) == 10 and (_month_no(od.group(1)), int(od.group(2))) != (int(date[5:7]), int(date[8:10])):
            continue                                   # "the afternoon of Jan. 2": another day's hour
        w = m.group(0)
        if _TITLE_WORD.match(w):                       # Evening Star, the Morning Post: a capital inside a sentence
            before = s[:m.start()].rstrip()
            if before and not re.search(r"[.!?:;(\"']$", before):
                continue
        out.append(w.strip())
    return out


def _parentheticals(n):
    out, depth, start = [], 0, None
    for i, ch in enumerate(n):
        if ch == "(":
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == ")" and depth:
            depth -= 1
            if depth == 0:
                out.append(n[start:i])
    return out


def time_hits(e):
    """[(field, words)]: the clock times and parts of the day in `c`, `when`, and `n`'s parentheticals."""
    out, d = [], str(e.get("date") or "")
    for f in ("c", "when"):
        out += [(f, w) for w in _time_hits(str(e.get(f) or ""), d)]
    n = _strip_markup(str(e.get("n") or ""))
    n = re.sub(r"To check:.*?(?=(?:Names|Check|Made public):|$)", " ", n, flags=re.S)   # records not read: their own hours
    for p in _parentheticals(n):
        out += [("n", w) for w in _time_hits(p, d)]
    return out


# -- at -----------------------------------------------------------------------------------------------------------------
_MONTHS = (r"(?:January|February|March|April|May|June|July|August|September|October|November|December|"
           r"Jan\.|Feb\.|Mar\.|Apr\.|Aug\.|Sept\.|Oct\.|Nov\.|Dec\.)")
_SPAN = rf"(?:{_MONTHS}|the month|the year|(?:19|20)\d\d|the spring|the summer|the fall|the autumn|the winter)"
AT_PATTERNS = [
    rf"\b(?:early|late|mid-?|the middle of|the end of|end of|the beginning of|the start of|the close of|the turn of)\s*(?:in\s+)?{_SPAN}",
    rf"\b(?:early|late) in {_SPAN}",
    r"\b(?:the )?(?:first|second|third|fourth|last) (?:week|half|ten days|days) of\b",
    r"\b(?:on )?the eve of\b",
    r"\b(?:shortly|soon|just|immediately|days|weeks) (?:after|before)\b",
    r"\b(?:in|during|that|this|by) (?:the )?(?:spring|summer|fall|autumn|winter)\b",
    r"^(?:early|late|mid-|after|before|following)\b",
    r"上旬|中旬|下旬|月初|月底|月末|年初|年底|年末|前夕|春季|夏季|秋季|冬季|春天|夏天|秋天|冬天",
    r"(?<!\w)(?:в начале|в середине|в конце|накануне)(?!\w)",
    r"(?<!\w)(?:đầu tháng|giữa tháng|cuối tháng|đầu năm|cuối năm)(?!\w)",
]
AT = re.compile("|".join(f"(?:{p})" for p in AT_PATTERNS), re.IGNORECASE)


def at_hits(e):
    """[(field, words)] for a loose entry without `at`; [] for any other."""
    if not loose.is_loose(e) or e.get("at"):
        return []
    out = []
    a = loose.at_for(e)
    q = loose._qualifier(e).strip()
    d = loose.date_of(e)
    if re.match(r"^(?:[–-]|or |to |and |through )", q):
        q = ""                                         # a span ("1964–65", "Sept. or Oct."), not a place in it
    if q and q != str(e.get("when") or "").strip():
        out.append(("when", q))
    elif q and AT.search(q):
        out.append(("when", AT.search(q).group(0)))
    for m in AT.finditer(_strip_markup(str(e.get("c") or ""))):
        w = m.group(0).strip()
        y = re.search(r"(?:19|20)\d\d", w)
        mo = re.search(_MONTHS, w)
        if y and y.group(0) != d[:4]:
            continue                                   # "the end of 1959" on a 1960 entry: another year's
        if mo and len(d) == 7 and _month_no(mo.group(0)) != int(d[5:7]):
            continue                                   # "late March" on an April entry: another month's
        out.append(("c", w))
    if a and not out:
        out.append(("when", str(e.get("when"))))
    return out


# -- place --------------------------------------------------------------------------------------------------------------
_PLACE_RE = None
_PLACE_OF = {}
# A province or region: named for the body that acts (the Sichuan provincial committee), almost never the scene; the
# place pass left them unset or set the seat (measured Nov. 19, 2026, on the last twenty merged patches: of 216 hits
# on a province the pass set the province on 16). A State is skipped by its row's kind.
SKIP_NAMES = {"Anhui", "Fujian", "Gansu", "Guangdong", "Guangxi", "Guizhou", "Hainan", "Hebei", "Heilongjiang", "Henan",
              "Hubei", "Hunan", "Inner Mongolia", "Jiangsu", "Jiangxi", "Jilin", "Liaoning", "Ningxia", "Qinghai",
              "Shaanxi", "Shandong", "Shanxi", "Sichuan", "Tibet", "Xinjiang", "Yunnan", "Zhejiang", "Manchuria"}


def _alias_words(a):
    return " ".join(w.capitalize() for w in str(a).split("-"))


def _place_index():
    global _PLACE_RE
    if _PLACE_RE is None:
        rows, _ = places._load()
        names = {}
        for r in rows:
            if r.get("kind") == "state":
                continue
            forms = [r.get("name")] + [n.get("name") for n in store.as_list(r.get("names")) if isinstance(n, dict)]
            forms += [_alias_words(a) for a in store.as_list(r.get("aliases")) if len(str(a)) > 3]
            for f in forms:
                f = re.sub(r"^the ", "", str(f or "")).strip()
                if len(f) < 3 or f in SKIP_NAMES:
                    continue
                names.setdefault(f, r["key"])
        _PLACE_OF.clear()
        _PLACE_OF.update(names)
        alts = sorted(names, key=len, reverse=True)
        _PLACE_RE = re.compile(r"(?<![\w-])(?:" + "|".join(re.escape(a) for a in alts) + r")(?![\w-])")
    return _PLACE_RE


def reset():
    global _PLACE_RE
    _PLACE_RE = None


def place_hits(e):
    """[(field, name, key)]: the gazetteer places `c` and `when` name, each once."""
    rx = _place_index()
    out, seen = [], set()
    for f in ("c", "when"):
        s = _strip_markup(str(e.get(f) or ""))
        s = re.sub(r"\*[^*\n]+\*", " ", s)                 # a title's words are not a scene
        for m in rx.finditer(s):
            k = _PLACE_OF[m.group(0)]
            if k not in seen:
                seen.add(k)
                out.append((f, m.group(0), k))
    return out


# -- the findings -------------------------------------------------------------------------------------------------------
def _ok(e, rule):
    return f"ok:{rule}" in {str(t) for t in store.as_list(e.get("tags"))}


def _quote(hits):
    return ", ".join(f"{w!r} in {f}" for f, w in hits[:4]) + (" ..." if len(hits) > 4 else "")


def findings(e):
    """[(rule, message)] for a calendar entry (STYLE 1, 2, 4)."""
    out = []
    eid = e.get("id")
    if not (e.get("time") or e.get("time_range")) and not _ok(e, "fields-time"):
        h = time_hits(e)
        if h:
            out.append(("fields-time", f"{eid}: the record gives the hour or the part of the day ({_quote(h)}): set time "
                        "(time_approx: true where loose), or time_range with time_band and time_zone (R25a; "
                        "tools/bib/dayorder.py), or tag ok:fields-time if it is not the act's time"))
    if not _ok(e, "fields-at"):
        h = at_hits(e)
        if h:
            a = loose.at_for(e)
            fix = f"set at: {a}" if a else "set at: before|after YYYY-MM-DD (its place in the month or year) and the qualifier in when (\"July, early\")"
            out.append(("fields-at", f"{eid}: a loose date with its place in the {'month' if len(loose.date_of(e)) == 7 else 'year'} "
                        f"({_quote(h)}): {fix} (R25a; tools/bib/loose.py), or tag ok:fields-at if it is not the act's"))
    if not e.get("place") and not _ok(e, "fields-place"):
        for f, w, k in place_hits(e):
            out.append(("fields-place", f"{eid}: set place: {k} ({w} in {f}), or tag ok:fields-place if {w} is not "
                        "where the act was done (R25a; notes/briefs/places.md)"))
    return [(r, m + f" [{r}]") for r, m in out]


def is_cal(eid):
    return bool(re.match(r"^cal\.\d{4}", str(eid or "")))


def patch_entries(path):
    """The calendar entries a patch adds, as written."""
    d = store.load_yaml(path) or {}
    out = []
    for op in d.get("ops") or []:
        if isinstance(op, dict) and "add" in op:
            e = (op["add"] or {}).get("entry") or {}
            if is_cal(e.get("id")):
                out.append(e)
    return out
