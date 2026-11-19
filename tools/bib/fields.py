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
                   dinner", "over breakfast"), in Chinese (上午 下午 晚上 凌晨 深夜, 十時, 9点钟, 一点半, 两点钟; 一时
                   and 四时 only after a day or a part of the day or before a minute: 十七日一时, 四时半), Russian ("в 10
                   часов", утром, вечером, ночью) or Vietnamese (sáng, chiều, tối, đêm before a day; "10 giờ"); anywhere
                   in `c` or `when`, and in `n` only inside a parenthetical (where a source's pinpoint is glossed). A
                   newspaper's name or "the morning papers" is not a time (EXCEPT); nor a title: italics, a quotation,
                   《》「」『』〈〉, a capitalized Morning, Evening, Afternoon or Night inside a sentence ("the Night of the
                   Long Knives"). Set aside as not the act's (measured Nov. 19, 2026: these were most of the false hits):
                   a. another day's or another time's hour: "of the 17th", "on the evening of the 10th", "at 2 p.m. on
                      the 14th", "the 17th morning" or "on Dec. 16 at dusk" where that day is not the entry's own (its
                      date, or the days its `when` spans, own_days; on a loose entry any day named is another's);
                      next, following, previous, tomorrow, yesterday (次日 翌日 明天 昨天) by the hit, "the night
                      before"; a plan ("to be settled that afternoon", "will", "is to"); "days after the lunch";
                   b. in `n`, "To check:" and "Check:" (records not read, and doubts: their own hours), and the gloss
                      after a link to another entry ("[[cal.…]] (Yang's diary: 4:30 p.m.)": that entry's hour);
                   c. "at NN" that is no clock: past 12 without a colon ("dies at 82", "Truman, at 80,", "vote at 18"),
                      after dies, died, aged, age, held, kept, fixed, stands and the like (unless a meeting is the
                      subject: "the meeting held at 4"), set off by commas, before "percent", and in `n` a page after a
                      date or a link ("the *Times*, Mar. 28, 1963, at 4").
                   d. An hour that recurs (the sentence says every or each day, daily, nightly, in shifts, usually, "N
                      a day"; in `n` the hit's clause): [fields-time-habitual], a warning ("patrol the parks from 4
                      a.m. to 11 p.m. in shifts"; "three and a half hours' labour a day; ... the radio at night").
    [fields-at]    a loose entry (a month or a year, loose.is_loose) with no `at`, whose position merge cannot set itself:
                   where loose.at_for gives an `at` that loose.at_problems passes, merge sets it (the ghost-day pass),
                   and nothing is reported. Otherwise a qualifier in `when` ("July, about the 20th", "1960, Spring
                   Festival"), or `c`'s position word for its month or year ("early", "mid-", "late", "end of", "first
                   week", "the eve of", "shortly after", a season). e. Not another time's: a year not the entry's
                   ("the end of 1959" on a 1960 entry), a year's position on a month's entry ("by the end of 1966" in
                   June), a month not the entry's ("late March" in April), a season of another year (its "of YYYY":
                   "in the spring of 1958" on a 1960 entry; "the winter of 1959–60" is December 1959 to March 1960) or
                   of other months ("in the fall" in July); a month's `when` naming its season or year ("May, spring",
                   "Dec. (late 1961)") has no place in the month.
    [fields-place] no `place`, and `c` or `when` names a gazetteer place: a row's `name` or an alias, as whole words
                   (Peking, Saigon, Moscow, Hangzhou; "Anniston, Ala." whole), a patch's own place-key rows with them.
                   A State (kind: state) is skipped: whether the State is the act's scene is too subtle for a word
                   match. The pattern is built again when the gazetteer changes (places.GEN), so a row one patch adds
                   counts for the next.
 2. Each is silenced by setting its field, or by the tag `ok:fields-time` (both time rules), `ok:fields-at`,
    `ok:fields-place` where the words are not the act's (a city named as a subject, not the scene; a time of another
    event).
 3. LEVEL says which are errors in patch-check and which warnings: measured on the open and the last merged reader
    patches (Nov. 19, 2026), a detector whose false hits pass a tenth is a warning. [fields-time]: 14 false of 46
    hits before 1a-1d, 1 of 33 after (2 more habitual, warnings); [fields-at]: 0 of 7; [fields-place] stays a warning.
 4. Each message names the words that fired, where, and the fix.
 5. patch-check prints the first PLACE_SHOWN [fields-place] findings and their count, not all of them; `./bib fields
    --patch P` lists them all.
"""
import datetime
import re

from . import loose, places, store

LEVEL = {"fields-time": "error", "fields-time-habitual": "warning", "fields-at": "error", "fields-place": "warning"}
PLACE_SHOWN = 3        # STYLE 5: the [fields-place] findings patch-check prints before their count

# -- time ---------------------------------------------------------------------------------------------------------------
_CN_NUM = r"(?:\d{1,2}|[二三五六七八九十]|十[一二]|[一二]十[一二三四五六七八九]?)"
_CN_NUM_DOT = r"(?:\d{1,2}|[一两兩二三四五六七八九十]|十[一二]|[一二]十[一二三四五六七八九]?)"   # 一点半, 两点钟: the 点 forms
TIME_PATTERNS = [
    r"\b\d{1,2}(?::\d\d)?\s*[ap]\.\s?m\.",
    r"\b\d{1,2}(?::\d\d)?\s*o'clock\b",
    r"\b(?:noon|midnight|midday|mid-morning|midafternoon|mid-afternoon)\b",
    r"\b[0-2]\d[0-5]\dZ\b",
    r"\bat (?:about )?\d{1,2}(?::\d\d)?(?![.,:]?\d)(?=[,.;)]|\s*$| in the | that | on )",
    r"\b(?:morning|afternoon|evening|night-time|nighttime|overnight)\b",
    r"\b(?:that|this|the same|late|last|the) night\b|\bat night\b|\bin the night\b|\blate at night\b|(?<!\ba )night of\b",
    r"\b(?:at|before|by) (?:dawn|daybreak|dusk|sunrise|sunset|first light)\b",
    r"\b(?:at|over|during|after) (?:a |the |an? \w+ )?(?:breakfast|lunch|luncheon|dinner|supper)\b",
    r"上午|下午|晚上|凌晨|深夜|中午|清晨|早晨|傍晚|午夜|晚間|晚间|夜間|夜间|當晚|当晚|當夜|当夜",
    _CN_NUM + r"(?:時|时)(?![期代間间候局事常刻光節节])(?:半|\d{1,2}分|[一二三四五六七八九十]+分)?",
    # 一时 ("for a time") and 四时 ("the four seasons") only with a day before or a minute after: 十七日一时, 四时半
    r"(?<=[日号號午晚夜晨])[一四](?:時|时)(?![期代間间候局事常刻光節节])|[一四](?:時|时)(?=半|许|許|左右|正|\d{1,2}分|[一二三四五六七八九十]+分)",
    _CN_NUM_DOT + r"(?:點鐘|点钟|點半(?![點点])|点半(?![點点])|點\d{1,2}分|点\d{1,2}分)",   # not 一点半点, "a little"
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
def _strip_markup(s):
    s = re.sub(r"\]\((?:https?://)[^)\s]*\)", "]", s)          # a link's address
    s = re.sub(r"https?://\S+", " ", s)
    s = re.sub(r"\[\[[^\]]*\]\]", " ", s)                      # a card's id
    return s


def _italics(s):
    return [(m.start(), m.end()) for m in re.finditer(r"\*[^*\n]+\*", s)]


_MON = (r"(?:Jan\.|Feb\.|Mar\.|Apr\.|May|June|July|Aug\.|Sept\.|Oct\.|Nov\.|Dec\.|January|February|March|April|"
        r"August|September|October|November|December)")
_ORD = r"(\d{1,2})(?:st|nd|rd|th)"
# STYLE 1a, another day's hour: "the morning of the 17th", "on the evening of Jan. 2", "at 2 p.m. on the 14th"
_DAY_AFTER = re.compile(rf"^\s*,?\s*(?:(?:of|on)\s+(?:the\s+)?{_ORD}|(?:(?:of|on)\s+)?({_MON})\s+(\d{{1,2}})(?!\d))")
# "left Wuxi on Dec. 16 at dusk", "On the 17th morning", "(Oct. 5, 5:30: ...)": a day at most two words before
_DAY_BEFORE = re.compile(rf"(?:\bthe\s+{_ORD}|\b({_MON})\s+(\d{{1,2}})(?!\d)(?:,\s*(?:19|20)\d\d)?)[,:;]?\s+(?:[\w'’]+\s+){{0,2}}$")
_CN_DAY_BEFORE = re.compile(r"(\d{1,2}|[一二三四五六七八九十]{1,3})[日号號]\s*$")
_NEXT_BEFORE = re.compile(r"\b(?:next|following|previous|preceding|tomorrow|tomorrow's|yesterday|yesterday's)\s+"
                          r"(?:[\w'’]+\s+){0,2}$|(?:次日|翌日|明天|明日|第二天|昨天|昨日|前一天|次晨|翌晨)\s*$", re.IGNORECASE)
_NEXT_AFTER = re.compile(r"^(?:'s|’s)?\s*,?\s*(?:tomorrow|yesterday|(?:the\s+)?(?:next|following|previous) "
                         r"(?:day|night|morning|afternoon|evening)|the day after|the day before)\b|"
                         r"^\s+before(?=\s*[,.;)]|\s*$)", re.IGNORECASE)          # "the night before."
# "a few days after the lunch": another day's meal
_DAYS_BEFORE = re.compile(r"\b(?:days?|weeks?|months?|hours?)\s+$", re.IGNORECASE)
# another time's hour: a plan ("to be settled that afternoon", "Deng will receive it the morning of the 17th")
_FUTURE_BEFORE = re.compile(r"\b(?:will|shall|to be|is to|are to)\s+(?:[\w'’]+\s+){0,3}$", re.IGNORECASE)
# STYLE 1c, "at NN" that is no clock: an age, a rate, a page
_AT_NOT_CLOCK = re.compile(r"\b(?:dies|died|dead|aged|age|ages|born|held|holds|kept|keeps|fixed|pegged|stands|stood|"
                           r"remains|remained|priced|valued|capped|estimated)\b[^.;]{0,40}$", re.IGNORECASE)
_EVENT_NOUN = re.compile(r"\b(?:meeting|meets|session|sitting|conference|rally|talks?|hearings?|service|funeral|ceremony|"
                         r"dinner|lunch|luncheon|reception|briefing|vote)\b", re.IGNORECASE)
_PAGE_BEFORE = re.compile(rf"(?:\b(?:19|20)\d\d|\b{_MON}\s+\d{{1,2}}|[\]\)\*]),?\s*$")
# STYLE 1d, habitual hours: a warning, not an error ("patrol from 4 a.m. to 11 p.m. in shifts", "the radio at night")
HABIT = re.compile(r"\b(?:(?:every|each) (?:day|night|morning|afternoon|evening|week)|daily|nightly|in shifts|usually|"
                   r"habitually|regularly)\b|每天|每日|每晚|每夜|"
                   r"\b(?:\d[\d,.]*|one|two|three|four|five|six|seven|eight|nine|ten|twelve|fifteen|twenty|thirty|fifty|"
                   r"a hundred|half)\b[^.;:]{0,40}?\ba day\b(?! or)", re.IGNORECASE)
_CJK_TITLE = re.compile(r"《[^》]*》|「[^」]*」|『[^』]*』|〈[^〉]*〉")
_TITLE_WORD = re.compile(r"\b(?:Morning|Evening|Afternoon|Night)\b")


def _month_no(w):
    """'Sept.' or 'September' -> 9."""
    w = w.rstrip(".")
    for i, m in enumerate(("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")):
        if w.startswith(m):
            return i + 1
    return None


_CN_DIGIT = {c: i for i, c in enumerate("〇一二三四五六七八九")}


def _cn_int(w):
    """'17' or '十七' -> 17."""
    if w.isdigit():
        return int(w)
    if "十" in w:
        a, _, b = w.partition("十")
        return (_CN_DIGIT.get(a, 1) if a else 1) * 10 + (_CN_DIGIT.get(b, 0) if b else 0)
    return _CN_DIGIT.get(w)


def own_days(e):
    """{(month, day)} the entry's own days: its date, and the span its `when` gives ("Feb. 16–17", "Feb. 29–Mar. 8");
    None for a loose entry (a month or a year)."""
    d = str(e.get("date") or "")
    if not re.match(r"^\d{4}-\d\d-\d\d$", d):
        return None
    y, m0, d0 = int(d[:4]), int(d[5:7]), int(d[8:10])
    out = {(m0, d0)}
    w = str(e.get("when") or "")
    r = re.match(rf"^\s*({_MON})\s+(\d{{1,2}})\s*[–-]\s*(?:({_MON})\s+)?(\d{{1,2}})(?!\d)", w)
    if r:
        m1, a = _month_no(r.group(1)), int(r.group(2))
        m2, b = (_month_no(r.group(3)) if r.group(3) else m1), int(r.group(4))
        try:
            day = datetime.date(y, m1, a)
            last = datetime.date(y + (m2 < m1), m2, b)
        except ValueError:
            return out
        while day <= last and len(out) < 40:
            out.add((day.month, day.day))
            day += datetime.timedelta(days=1)
    return out


def _is_own(own, month, day):
    """Whether a day the text names is the entry's own: on a loose entry (own None) no named day is ("for Dec. 3, 11:30
    a.m." on a November entry: an appointment's hour, not the month's)."""
    if not day:
        return True
    if own is None:
        return False
    return (month, day) in own if month else any(dd == day for _, dd in own)


def _other_day(s, a, b, own):
    """True where the hour at s[a:b] is another day's or another time's (STYLE 1a)."""
    before, after = s[max(0, a - 60):a], s[b:b + 40]
    if _NEXT_BEFORE.search(before) or _NEXT_AFTER.match(after) or _FUTURE_BEFORE.search(before):
        return True
    if re.match(r"(?:after|before)\b", s[a:b], re.IGNORECASE) and _DAYS_BEFORE.search(before):
        return True
    for r in (_DAY_AFTER.match(after), _DAY_BEFORE.search(before)):
        if r:
            day = int(r.group(1) or r.group(3))
            mon = _month_no(r.group(2)) if r.group(2) else None
            if not _is_own(own, mon, day):
                return True
    r = _CN_DAY_BEFORE.search(s[max(0, a - 6):a])
    if r and not _is_own(own, None, _cn_int(r.group(1))):
        return True
    return False


def _not_clock(s, a, w, field):
    """True where "at NN" is an age, a rate, a count or a page, not a clock (STYLE 1c)."""
    r = re.match(r"^at (?:about )?(\d{1,2})(?::(\d\d))?$", w)
    if not r:
        return False
    hour, colon = int(r.group(1)), r.group(2)
    end = a + len(w)
    if colon:
        return hour > 24
    if hour > 12:
        return True                                    # "dies at 82", "Truman, at 80,", "vote at 18"
    before = s[max(0, a - 60):a]
    sentence = re.split(r"[.;!?]\s", before)[-1]
    if _AT_NOT_CLOCK.search(sentence) and not _EVENT_NOUN.search(sentence):
        return True                                    # "the rate held at 3.", not "the meeting held at 4."
    if before.rstrip().endswith(",") and s[end:end + 1] == ",":
        return True                                    # ", at 9," an age set off by commas
    if re.match(r"^\s*(?:percent|per cent|%)", s[end:]):
        return True
    if field == "n" and _PAGE_BEFORE.search(before):
        return True                                    # "(the *Times*, Mar. 28, 1963, at 4)": a page
    return False


def _sentence(s, a, clause=False):
    """The sentence around position a; clause=True, its clause between semicolons (a gloss in `n` runs its clauses
    together)."""
    ends = [m.end() for m in re.finditer(r"[.!?。]\s+(?=[A-Z\"“《\u4e00-\u9fff])", s)]
    if clause:
        ends += [m.end() for m in re.finditer(r";", s)]
    st = max([x for x in ends if x <= a] or [0])
    return s[st:min([x for x in ends if x > a] or [len(s)])]


def _time_hits(s, own=None, field="c"):
    """[(words, habitual)] the clock times and parts of the day in s, less those STYLE 1a, 1c, 1d set aside."""
    s = _strip_markup(s)
    spans = [(m.start(), m.end()) for m in EXCEPT.finditer(s)] + _italics(s) + _quoted(s)
    spans += [(m.start(), m.end()) for m in _CJK_TITLE.finditer(s)]
    out = []
    for m in TIME.finditer(s):
        a, w = m.start(), m.group(0)
        if any(x <= a < y for x, y in spans):
            continue
        t = _TITLE_WORD.search(w)                       # Evening Star, the Night of the Long Knives: a title
        if t:
            before = s[:a + t.start()].rstrip()
            if before and not re.search(r"[.!?:;(\"'“]$", before):
                continue
        if _other_day(s, a, m.end(), own) or _not_clock(s, a, w, field):
            continue
        sen = _sentence(s, a, clause=field == "n")
        sen = re.sub(r'"[^"\n]*"|“[^”\n]*”', " ", sen)                 # a quotation's words are not the record's
        out.append((w.strip(), bool(HABIT.search(sen))))
    return out


def _quoted(s):
    return [(m.start(), m.end()) for m in re.finditer(r'"[^"\n]*"|“[^”\n]*”', s)]


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


_LINK_GLOSS = re.compile(r"\[\[cal\.[^\]]*\]\]\s*\((?:[^()]|\([^()]*\))*\)")
_UNREAD = re.compile(r"(?:To check|Check):.*?(?=(?:Names|To check|Check|Made public):|$)", re.S)


def _time_hits_all(e):
    """[(field, words, habitual)]: `c`, `when`, and `n`'s parentheticals (STYLE 1b: not "To check:" or "Check:", not
    the gloss on another entry's link)."""
    out, own = [], own_days(e)
    for f in ("c", "when"):
        out += [(f, w, h) for w, h in _time_hits(str(e.get(f) or ""), own, f)]
    n = _LINK_GLOSS.sub(" ", str(e.get("n") or ""))          # "[[cal.…]] (Yang's diary: 4:30 p.m.)": that entry's hour
    n = _UNREAD.sub(" ", _strip_markup(n))                    # records not read, and checks: their own hours
    for p in _parentheticals(n):
        out += [("n", w, h) for w, h in _time_hits(p, own, "n")]
    return out


def time_hits(e, habitual=None):
    """[(field, words)]: the clock times and parts of the day in `c`, `when`, and `n`'s parentheticals; habitual=False
    the act's own, True the habitual ones (STYLE 1d), None both."""
    return [(f, w) for f, w, h in _time_hits_all(e) if habitual is None or h == habitual]


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


_SEASON_MONTHS = {"spring": {3, 4, 5, 6}, "summer": {6, 7, 8, 9}, "fall": {9, 10, 11, 12}, "autumn": {9, 10, 11, 12},
                  "winter": {12, 1, 2, 3}}
_SEASON_YEAR = re.compile(r"^\s+of\s+((?:19|20)\d\d)(?:\s*[–-]\s*((?:19|20)?\d\d))?(?!\d)")


def _season_other(w, after, d):
    """True where a season in `c` is another season than the entry's (STYLE 1e): "in the spring of 1958" on a 1960
    entry; "the winter of 1959–60" on a June entry; "in the fall" on a July one."""
    s = re.search(r"spring|summer|fall|autumn|winter", w, re.IGNORECASE)
    if not s:
        return False
    s = s.group(0).lower()
    y = int(d[:4])
    r = _SEASON_YEAR.match(after)
    if r:
        y1 = int(r.group(1))
        y2 = (int(r.group(2)) if len(r.group(2)) == 4 else y1 // 100 * 100 + int(r.group(2))) if r.group(2) else None
        if y2 and s == "winter":                       # the winter of 1959–60: December 1959 to March 1960
            if len(d) == 4:
                return y not in (y1, y2)
            m = int(d[5:7])
            return not ((y == y1 and m == 12) or (y == y2 and m <= 3))
        if y not in ({y1, y2} if y2 else {y1}):
            return True
    if len(d) == 7 and int(d[5:7]) not in _SEASON_MONTHS[s]:
        return True                                    # "tests will resume in the fall" on a July entry
    return False


def at_hits(e):
    """[(field, words)] for a loose entry without `at` whose position merge cannot set; [] for any other (STYLE 1e)."""
    if not loose.is_loose(e) or e.get("at"):
        return []
    a = loose.at_for(e)
    if a and not loose.at_problems(dict(e, at=a)):
        return []                                      # `when` places it: merge sets the `at` itself
    out = []
    q = loose._qualifier(e).strip()
    d = loose.date_of(e)
    if re.match(r"^(?:[–-]|or |to |and |through )", q):
        q = ""                                         # a span ("1964–65", "Sept. or Oct."), not a place in it
    if len(d) == 7 and (loose._kind(q)[0] == "season" or re.fullmatch(r"\(?(?:early|mid-?|late)\s*(?:19|20)\d\d\)?", q, re.I)):
        q = ""                                         # "May, spring", "Dec. (late 1961)": the month's season or year, no place in it
    if q and q != str(e.get("when") or "").strip():
        out.append(("when", q))
    elif q and AT.search(q):
        out.append(("when", AT.search(q).group(0)))
    c = _strip_markup(str(e.get("c") or ""))
    for m in AT.finditer(c):
        w = m.group(0).strip()
        y = re.search(r"(?:19|20)\d\d", w)
        mo = re.search(_MONTHS, w)
        if y and y.group(0) != d[:4]:
            continue                                   # "the end of 1959" on a 1960 entry: another year's
        if y and not mo and len(d) == 7:
            continue                                   # "by the end of 1966" on a June entry: the year's, not the month's
        if mo and len(d) == 7 and _month_no(mo.group(0)) != int(d[5:7]):
            continue                                   # "late March" on an April entry: another month's
        if _season_other(w, c[m.end():m.end() + 20], d):
            continue
        out.append(("c", w))
    return out


# -- place --------------------------------------------------------------------------------------------------------------
_PLACE_RE = None
_PLACE_GEN = None
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
    """The gazetteer's names as one pattern, built again when the gazetteer changes (places.GEN: a row a merged patch
    added counts for the next patch) or a patch's own rows are pending (places.PENDING)."""
    global _PLACE_RE, _PLACE_GEN
    gen = (places.GEN, tuple(sorted(places.PENDING)))
    if _PLACE_RE is None or _PLACE_GEN != gen:
        rows, idx = places._load()
        names = {}
        for r in list(rows) + [r for k, r in places.PENDING.items() if k not in idx and r.get("key")]:
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
        _PLACE_GEN = gen
    return _PLACE_RE


def reset():
    """The place pattern dropped (places.reset calls it; the next finding builds it again)."""
    global _PLACE_RE, _PLACE_GEN
    _PLACE_RE = _PLACE_GEN = None


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
        hits = _time_hits_all(e)
        firm = [(f, w) for f, w, h in hits if not h]
        if firm:
            out.append(("fields-time", f"{eid}: the record gives the hour or the part of the day ({_quote(firm)}): set time "
                        "(time_approx: true where loose), or time_range with time_band and time_zone (R25a; "
                        "tools/bib/dayorder.py), or tag ok:fields-time if it is not the act's time"))
        elif hits and not _ok(e, "fields-time-habitual"):
            out.append(("fields-time-habitual", f"{eid}: an hour or a part of the day that recurs "
                        f"({_quote([(f, w) for f, w, _ in hits])}): set time if one day's act has it, or tag "
                        "ok:fields-time (R25a; tools/bib/dayorder.py)"))
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
