"""Newspapers and magazines in the lists' notes: titles in italics, the *New York Times* linked to TimesMachine, a
run of cites to one paper written once, serially (the owner, Nov. 6-10, 2026: "Newspapers should have their titles in
italics throughout"; a read cite "[*New York Times*, Feb. 7, 1960](issue), at [E1](page)"; "serial citations to the
same paper like that should be given as '*New York Times*, [Feb. 18](link), [Feb. 20](link), [Feb. 22](link), and
[Mar. 1, 1960](link)' when the pincite isn't known, and '*New York Times*, [Feb. 18 at X](link), [Feb. 20 at Y](link),
[Feb. 22 at Z](link), and [Mar. 1, 1960, at A](link)' when it is").

Scope: every entry's note (`n`) and every gloss's text in lists/<key>/*.yaml; never `c`, a role, a thread's
statement, a list's intro. Rerunnable: what it writes it leaves alone the next time.

Run: python3 -I tools/works/newspaper_cites.py [--write] [--root DIR] [--titles] [--quiet]
  (default a dry run: each change printed as id, before, after; --write edits the files in place, each changed line's
  value alone rewritten, every other byte as it was; --root another checkout or a copy; --titles the candidate titles
  found in cite position, "Title, Month day, year", plain or italic, with their counts and whether the list holds them)

STYLE
1. Titles. TITLES below, newspapers and magazines only, built from what the notes cite (`--titles` lists the
   candidates). A title written plain is put in italics wherever it stands in a note, outside a [[...]] link, a link's
   address, a bare address, an italic span (a book's title, a title already italic) and a quotation ("...", "...").
   A title that is also a common word or a phrase used otherwise (AMBIG: Time, Life, Look, Jet, Nation, Reporter,
   Afro-American ...) only in a cite's position: followed by ", Month" or a year, or after an article's title
   (',"' before it), and where a cite may begin (after "; ", "(", "the ", ", " ...: BOUND). Not where the words run on
   into a capitalized word or "v." ("New York Times Co.", "Washington Post Book World", "New York Times v. Sullivan",
   "Congressional Quarterly Weekly Report XVIII"). The longest title wins ("Washington Post and Times
   Herald" over "Washington Post"). "the" stays roman ("the *Washington Post*"); a magazine whose name is "The ..."
   (THE_IN) takes its capital "The" inside ("*The Reporter*"). The plain title is kept as written (its
   spelling, hyphens), but EXPAND: the abbreviations that stand for one paper and no other in a cite's position
   (NYT, WP, LAT, NYT Magazine, NY Herald Tribune) are written out. Branch's other keys (SC, STJ, MCA, MS, CST, DT-H)
   are left as they stand (reported): his key is not read here.
2. The *New York Times* by a single day, not linked, is linked to TimesMachine's issue of that day (nyt_links.TM),
   the title and date the link's text, as nyt_links.py does; not a range of
   days, or a date that is not a day; not inside a link's text; never the *New York Times Magazine*.
3. A pinpoint after a cite's date is written ", at X" (Bluebook 16.6: "N.Y. Times, Feb. 7, 1960, at E1"): "14",
   "p. 14", "pp. 1, 3", "A1", "B-1", "14A", "28ff" as written, "p." and "pp." dropped. One the pattern cannot read
   ("pole", "sec. 4, p. 2") is left as written, and so is a cite whose date runs on into anything but the end of a
   cite (";", " (", ")", ".", the end, ", and", " and").
4. A run: cites to one paper one after another, joined by "; ", ", ", ", and " or " and ", each the title and a date,
   or a date alone after the first (the paper understood), each date with or without its pinpoint. Written once:
   "*Atlanta Constitution*, Feb. 18 at 1 and Feb. 19, 1960, at 9"; the *Times* each date linked, the pinpoint inside
   the link ("[Feb. 18 at 14](issue)"). Two dates joined by " and " (", and " after a year), three or more by commas
   and ", and". The year at the last date of each stretch of one year, ", at X" after it; without the year " at X".
   A "(cited by ...)" after the run stays after it. A run is broken by another paper, a parenthetical, an article's
   title or a byline. Not joined (left as single cites, each in the form of 2 and 3): a run whose first cite follows
   an article's title or a byline (',"', ', ' before the title: the next cite may be another article); a cite linked
   elsewhere than its issue, or with its page linked ("at [E1](page)"); a run of another paper whose pinpoints hold a
   comma ("1, 3"), which would read as two dates.
5. Dates. One day ("Feb. 18, 1960", "March 8, 1966") or a range ("Feb. 24–25, 1968", unlinked) as written; several
   days of one month ("Oct. 2 and 3, 1968", "May 13, 14, 17, 24, 1966"): for the *Times* each day linked, as a run
   ("[Oct. 2](issue) and [Oct. 3, 1968](issue)"), for another paper left as written; with a pinpoint after them,
   left as written (whose page?). The military histories' form ("Jul 13, 65", "Sep 18, 65, p 1") and, for the
   *Times*, a day first ("31 July 1966") are written in the series' form ("July 13, 1965", "Sept. 18, 1965, at 1",
   "July 31, 1966"); "May" with a two-digit year only in a note that writes another month so.
6. Never inside a quotation, a [[...]] link or an address; a value whose straight double quotes do not pair is
   reported, and in it only the cite's position counts (rule 1, for every title).
7. The file: the value's quoting kept (single quotes, apostrophes doubled); a plain value that now needs quotes (it
   begins with "*" or "[") takes single quotes. Every rewritten line is parsed back and must give the new value.
8. The claim map. An entry's `src` rows name the note's items (tools/bib/claims.py: a link's address, a text's first
   words); a row that finds its item in the note before must find one after (`claims.resolve`). Where joining a run
   would lose one (the rows name its dates one by one), the run is left as single cites; where even that would, the
   note is left as it stands. Both reported.
"""
import argparse
import collections
import datetime
import glob
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from nyt_links import TM, MON  # noqa: E402
from bib import claims  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
# The strike of Dec. 8, 1962–Mar. 31, 1963: the Western Edition went on; its days are linked (the owner, Nov. 12, 2026).

# Newspapers and magazines the notes cite, as they write them (STYLE 1). Built from `--titles`.
TITLES = """
New York Times; New York Times Magazine; New York Times Index; N.Y. Times; New York Herald Tribune;
International Herald Tribune; New York Post; New York Daily News; New York World-Telegram; New York World Telegram;
New York Journal-American; N.Y. Journal-American; New York Amsterdam News; Amsterdam News; New York Courier;
New York Review of Books; Newsday; Long Island Star Journal; Long Island Press;
Washington Post; Washington Post and Times Herald; Washington Star; Washington Evening Star; Washington Daily News;
Wall Street Journal; Christian Science Monitor; Baltimore Sun; Baltimore Afro-American; Afro-American;
Chicago Tribune; Chicago Sun-Times; Chicago Daily News; Chicago Defender; Chicago Daily Defender; Chicago's American;
Los Angeles Times; Los Angeles Sentinel; Los Angeles Herald-Dispatch; Los Angeles Herald-Examiner;
Atlanta Constitution; Atlanta Journal; Atlanta Journal-Constitution; Atlanta Journal and Constitution;
Atlanta Journal and Constitution Magazine; Atlanta Daily World; Atlanta Inquirer;
Montgomery Advertiser; Alabama Journal; Birmingham News; Birmingham Post-Herald; Birmingham World;
Selma Times-Journal; Southern Courier; Mobile Register; Tuscaloosa News; Huntsville Times; Anniston Star;
Albany Herald; Albany Journal; Macon Telegraph; Savannah Morning News; Augusta Chronicle; Thomasville Times-Enterprise;
Jackson Clarion-Ledger; Clarion-Ledger; Jackson Daily News; Meridian Star; Greenwood Commonwealth;
Mississippi Free Press; Delta Democrat-Times; McComb Enterprise-Journal; Hattiesburg American;
Memphis Commercial Appeal; Commercial Appeal; Memphis Press-Scimitar; Memphis Tri-State Defender; Tri-State Defender;
Nashville Tennessean; Nashville Banner; Knoxville Journal; Chattanooga Times;
Louisville Courier-Journal; Louisville Defender; Lexington Herald;
Pittsburgh Courier; Pittsburgh Post-Gazette; Cleveland Call and Post; Cleveland Plain Dealer; Plain Dealer;
Cleveland Press; Detroit News; Detroit Free Press; Michigan Chronicle; Milwaukee Journal; Milwaukee Sentinel;
Madison Capital Times; Capital Times; Minneapolis Tribune; Minneapolis Star; St. Paul Pioneer Press;
Des Moines Register; Omaha World-Herald; Kansas City Star; St. Louis Post-Dispatch; St. Louis Globe-Democrat;
Indianapolis Star; Indianapolis News; Peoria Journal-Star; Peoria Journal Star; Chicago Sun-Times Magazine;
Dallas Morning News; Dallas Times Herald; Houston Post; Houston Chronicle; Fort Worth Star-Telegram;
San Antonio Light; San Antonio Express; Waco News-Tribune; Austin American-Statesman; Austin American;
Texas Observer; Arkansas Gazette; Arkansas Democrat; New Orleans Times-Picayune; Times-Picayune;
New Orleans States-Item; Shreveport Times; Baton Rouge Morning Advocate;
Florida Times-Union; Jacksonville Times-Union; Miami Herald; Miami News; St. Petersburg Times; Tampa Tribune;
St. Augustine Record; Orlando Sentinel;
Richmond Times-Dispatch; Richmond News Leader; Norfolk Virginian-Pilot; Charleston News and Courier;
News and Courier; Charlotte Observer; Raleigh News and Observer; Greensboro Daily News; Columbia State;
Manchester Union Leader; Boston Globe; Boston Herald; Providence Journal; Hartford Courant;
Philadelphia Inquirer; Philadelphia Bulletin; Philadelphia Evening Bulletin; Philadelphia Daily News;
Philadelphia Tribune; Newark Star-Ledger; Newark Evening News;
Dayton Daily News; Cincinnati Enquirer; Toledo Blade; Akron Beacon Journal; Columbus Dispatch;
Denver Post; Rocky Mountain News; Arizona Republic; Salt Lake Tribune; Portland Oregonian; Oregonian;
San Francisco Chronicle; San Francisco Examiner; Sacramento Bee; San Diego Union; Oakland Tribune; Seattle Times;
Seattle Post-Intelligencer; Honolulu Star-Bulletin; Honolulu Advertiser; Anchorage Daily Times; Prescott Courier;
Rome Daily American; London Daily Telegraph; Daily Telegraph; Manchester Guardian; Times of London; Le Monde;
Sunday Times; Pravda; Izvestia;
Time; Newsweek; Life; Look; Jet; Ebony; Nation; New Republic; National Review; Reporter; Saturday Evening Post;
Saturday Review; New Yorker; U.S. News & World Report; U.S. News and World Report; Business Week; Fortune;
Christian Century; Christianity and Crisis; Commonweal; Commentary; New Leader; National Observer;
National Catholic Reporter; I. F. Stone's Weekly; Muhammad Speaks; Harper's; Harper's Magazine;
Atlantic Monthly; Esquire; Ramparts; Freedomways; Progressive; Village Voice;
Human Events; Ladies' Home Journal; McCall's; Reader's Digest; Coronet; Redbook;
Congressional Quarterly Weekly Report; CQ Weekly Report; Congressional Quarterly; Washington Monthly;
Columbia Journalism Review; Ave Maria; Catholic Worker; Jewish Week; Militant; Courier-Journal;
Valdosta Daily Times; New York World-Telegram and Sun; Daily Sentinel; Nation's Business; Las Vegas Review-Journal;
Hope Star; Daily Express; Northwest Arkansas Times; Pontiac Press; Harrington Journal; Aviation Week;
Aviation Week and Space Technology; Herald Tribune; University Daily Kansan; New Haven Register; Lincoln Star;
Holmes County Herald; Times of Viet Nam Magazine;
Minneapolis Sunday Tribune; Lima News; Pittsburgh Press; Medical World News; Beijing Review; Nhân Dân
"""
TITLES = [t.strip() for t in TITLES.replace("\n", " ").split(";") if t.strip()]

# Titles that are also words or phrases used otherwise: only in a cite's position (STYLE 1).
AMBIG = {"Time", "Life", "Look", "Jet", "Nation", "Reporter", "Fortune", "Commentary", "Progressive", "Ebony",
         "Afro-American", "Columbia State", "Commercial Appeal", "Capital Times", "Clarion-Ledger", "Times-Picayune",
         "Oregonian", "Sunday Times", "Daily Telegraph", "News and Courier", "Human Events", "Esquire", "Coronet",
         "Redbook", "Ramparts", "Congressional Quarterly", "Plain Dealer", "Tri-State Defender", "Amsterdam News",
         "Le Monde", "Ave Maria", "Catholic Worker", "Jewish Week", "Commonweal", "Harper's", "Pravda", "Izvestia",
         "Village Voice", "Muhammad Speaks", "New Leader", "Austin American", "Times of London", "Militant",
         "Daily Sentinel", "Daily Express", "Herald Tribune", "Courier-Journal"}
# Magazines whose name begins "The" (STYLE 1).
THE_IN = {"Nation", "Reporter", "Commonweal", "New Republic", "New Yorker", "Progressive",
          "New Leader", "Village Voice", "Christian Century", "National Observer",
          "Atlantic Monthly", "Saturday Evening Post", "Saturday Review", "Militant"}
# Abbreviations written out (STYLE 1); in a cite's position only.
EXPAND = {"NYT": "New York Times", "NYT Magazine": "New York Times Magazine", "WP": "Washington Post",
          "LAT": "Los Angeles Times", "NY Herald Tribune": "New York Herald Tribune"}
NYT = {"New York Times", "N.Y. Times"}
# A title run on into a name of another kind (STYLE 1): "New York Times Co.", "Washington Post Book World".
RUN_ON = re.compile(r" (?:v\.|[A-Z])")
# Before a title that is also a word (AMBIG): where a cite begins (STYLE 1).
BOUND = re.compile(r"(?:^|[;:(]\s*|[,.][\"”'’]?\s+|\b(?:the|in|and|also|Also|see|See|cf\.|from|by|citing)\s)$")
SERIES = {1: "Jan.", 2: "Feb.", 3: "Mar.", 4: "Apr.", 5: "May", 6: "June", 7: "July", 8: "Aug.", 9: "Sept.",
          10: "Oct.", 11: "Nov.", 12: "Dec."}
MON_N = dict(MON, **{"Sep.": 9})
FULLS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December"]
BARE_MON = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Sept": 9, "Oct": 10,
            "Nov": 11, "Dec": 12}
M = "(?:" + "|".join(re.escape(m) for m in sorted(MON_N, key=len, reverse=True)) + ")"
MB = "(?:" + "|".join(sorted(BARE_MON, key=len, reverse=True)) + ")"
DAYS = r"\d{1,2}(?:(?:, | and |, and )\d{1,2}(?!\d))+"
Y4 = r"(?P<y>1[89]\d\d|20\d\d)(?!\d)"
# The forms of a date a cite may give (STYLE 5): one day, or a range ("Feb. 24–25", "Feb. 21–Mar. 13"); several
# days of one month ("Oct. 2 and 3, 1968", "May 13, 14, 17, 24, 1966"); the military's ("Jul 13, 65"); day first
# ("30 July 1966"). The last two are written in the series' form where they are rewritten.
D_STD = re.compile(r"(?P<mon>" + M + r") (?P<d>\d{1,2})(?P<rng>[–-](?:" + M + r" )?\d{1,2})?,? " + Y4)
D_MANY = re.compile(r"(?P<mon>" + M + r") (?P<days>" + DAYS + r"),? " + Y4)
D_TWO = re.compile(r"(?P<mon>" + MB + r"|May) (?P<days>\d{1,2}(?:(?:, | and |, and )\d{1,2}(?!\d))*),? (?P<y>[4-7]\d)"
                   r"(?![\d])")
D_DAY1 = re.compile(r"(?P<d>\d{1,2}) (?P<mon>" + "|".join(FULLS) + r") " + Y4)
CITE_POS = re.compile(r",? (?:(?:" + M + "|" + MB + r")[ ,]|\d{1,2} (?:" + "|".join(FULLS) + r") |1[89]\d\d\b)")
PINTOK = r"[A-Z]?-?\d{1,4}[A-Z]?(?:ff?\.?)?(?:[–-][A-Z]?-?\d{1,4}[A-Z]?)?"
PIN = re.compile(r", (?:at )?(?:pp?\.? ?)?(?P<pin>" + PINTOK + r"(?:, " + PINTOK + r"(?=[;,)(. ]|$))*)")
END = re.compile(r";|,? and |, (?=(?:" + M + "|" + MB + r") \d)|\s\(|\)|\.(?=\s|$|['\"])|$")
JOIN = re.compile(r"; |, and | and |, ")
URLTM = re.compile(r"https://timesmachine\.nytimes\.com/timesmachine/(\d{4})/(\d\d)/(\d\d)/issue\.html")


def protected(s, italics=True):
    """Spans no title may be touched in (STYLE 6): [[...]], a link's address, a bare address, a quotation, and (for
    the titles' pass) an italic span; and, apart, the text of each link (for rule 2). Returns (mask, intext, paired)."""
    n = len(s)
    mask, intext = [False] * n, [False] * n

    def cover(a, b, arr):
        for i in range(a, min(b, n)):
            arr[i] = True
    for m in re.finditer(r"\[\[.*?\]\]", s):
        cover(m.start(), m.end(), mask)
    for m in re.finditer(r"\]\(([^)\s]*)\)", s):
        cover(m.start(1), m.end(1), mask)
    for m in re.finditer(r"https?://[^\s)]+", s):
        cover(m.start(), m.end(), mask)
    if italics:
        for m in re.finditer(r"(?<![\w*])\*(?!\s)[^*]+?(?<!\s)\*(?![\w*])", s):
            if not any(mask[m.start():m.end()]):
                cover(m.start(), m.end(), mask)
    paired = s.count('"') % 2 == 0
    if paired:
        for m in re.finditer(r'"[^"]*"', s):
            if not mask[m.start()]:
                cover(m.start(), m.end(), mask)
    for m in re.finditer(r"“[^”]*”", s):
        cover(m.start(), m.end(), mask)
    for m in re.finditer(r"(?<!\[)\[(?!\[)((?:[^\[\]]|\[[^\[\]]*\])*)\]\(", s):
        cover(m.start(1), m.end(1), intext)
    return mask, intext, paired


def title_re():
    forms = sorted(set(TITLES) | set(EXPAND), key=len, reverse=True)
    return re.compile(r"(?<![\w*'’.-])(?P<the>The )?(?P<t>" + "|".join(re.escape(t) for t in forms) + r")(?![\w*-])")


TITLE_RE = title_re()


def italicize(s, log):
    """STYLE 1: a pass over the value; returns the new value."""
    mask, _, paired = protected(s)
    if not paired:
        log.append(("ambiguous", "unpaired double quotes: only cite positions read"))
    out, last = [], 0
    for m in TITLE_RE.finditer(s):
        a, b = m.start("t"), m.end("t")
        if any(mask[a:b]):
            continue
        t = m.group("t")
        after = s[b:]
        lead = m.start("the") if m.group("the") else a
        cite = bool(CITE_POS.match(after)) or bool(re.search(r",[\"”'’] ?$", s[:lead]))
        if RUN_ON.match(after):
            continue
        if t in EXPAND or t in AMBIG or not paired:
            if not cite:
                continue
        if t in AMBIG and not BOUND.search(s[:lead]):
            continue
        full = EXPAND.get(t, t)
        lead = m.start("t")
        if m.group("the") and full in THE_IN:
            lead = m.start()
            full = "The " + full
        out.append(s[last:lead])
        out.append("*" + full + "*")
        last = b
        log.append(("expand" if t in EXPAND else "italicize", full if t not in EXPAND else f"{t} -> *{full}*"))
        if not cite:
            log.append(("in-prose", f"{full}: ...{s[max(0, lead - 50):b + 40]}..."))
    out.append(s[last:])
    return "".join(out)


ITAL = sorted({"*" + EXPAND.get(t, t) + "*" for t in TITLES} | {"*The " + t + "*" for t in THE_IN}, key=len,
              reverse=True)
HEAD = re.compile(r"(?P<open>\[)?(?P<t>" + "|".join(re.escape(t) for t in ITAL) + r"),? ")


def norm(t):
    t = t.strip("*")
    if t.startswith("The "):
        t = t[4:]
    return "New York Times" if t in NYT else t


class Day:
    """One date of a cite: its month as it is to be written, day, range, year."""

    def __init__(self, mon, d, rng, y, n):
        self.mon, self.d, self.rng, self.y = mon, d, rng, y
        try:
            self.day = None if rng else datetime.date(y, n, int(d))
        except ValueError:
            self.day = None

    def text(self, year):
        return f"{self.mon} {self.d}{self.rng}" + (f", {self.y}" if year else "")


def parse_date(s, k, two_ok, day1_ok=True):
    """The date at k: (end, [Day], form) or None. form: std, many, two (the military's), day1 (day first)."""
    m = D_MANY.match(s, k)
    if m:
        n = MON_N[m.group("mon")]
        days = re.split(r", and |, | and ", m.group("days"))
        return m.end(), [Day(m.group("mon"), d, "", int(m.group("y")), n) for d in days], "many"
    m = D_STD.match(s, k)
    if m:
        return m.end(), [Day(m.group("mon"), m.group("d"), m.group("rng") or "", int(m.group("y")),
                             MON_N[m.group("mon")])], "std"
    m = D_TWO.match(s, k)
    if m and (m.group("mon") != "May" or two_ok):
        n = BARE_MON.get(m.group("mon"), 5)
        days = re.split(r", and |, | and ", m.group("days"))
        return m.end(), [Day(SERIES[n], d, "", 1900 + int(m.group("y")), n) for d in days], "two"
    m = D_DAY1.match(s, k) if day1_ok else None
    if m:
        n = FULLS.index(m.group("mon")) + 1
        return m.end(), [Day(m.group("mon"), m.group("d"), "", int(m.group("y")), n)], "day1"
    return None


class Item:
    """One cite: its span, its title (None for a date alone), its dates, pinpoint, link."""

    def __init__(self, s, a, title, k, open_, two_ok, day1_ok):
        self.a, self.title = a, title
        r = parse_date(s, k, two_ok, day1_ok)
        self.ok = r is not None
        if not r:
            return
        e, self.days, self.form = r
        self.url = None
        if open_:
            u = re.compile(r"\]\(([^)\s]*)\)").match(s, e)
            if not u:
                self.ok = False
                return
            self.url, e = u.group(1), u.end()
        self.pagelink = bool(re.match(r", at \[", s[e:]))
        self.pin, self.pin_raw = None, ""
        p = PIN.match(s, e)
        if p and END.match(s, p.end()):
            self.pin, self.pin_raw = p.group("pin"), s[e:p.end()]
            e = p.end()
        self.e = e
        self.raw = s[a:e]
        self.ends = bool(END.match(s, e)) and not self.pagelink
        # several days with a pinpoint: whose page is it? left as written
        self.keep = len(self.days) > 1 and self.pin is not None


def nyt_url(day):
    if day.day is None:
        return None
    return TM.format(y=day.day.year, m=day.day.month, d=day.day.day)


def item_at(s, k, mask, intext, two_ok, paper=None):
    """A cite at k: the title and a date (of `paper` where given), or, where paper is given, a date alone."""
    m = HEAD.match(s, k)
    if m and (paper is None or norm(m.group("t")) == paper):
        if any(mask[m.start("t"):m.end("t")]) or (intext[k] and not m.group("open")):
            return None
        it = Item(s, k, m.group("t"), m.end(), m.group("open"), two_ok, norm(m.group("t")) == "New York Times")
        return it if it.ok else None
    if paper is None:
        return None
    open_ = s.startswith("[", k) and not s.startswith("[[", k)
    j = k + 1 if open_ else k
    if j >= len(s) or mask[j] or (intext[j] and not open_):
        return None
    it = Item(s, k, None, j, open_, two_ok, paper == "New York Times")
    return it if it.ok else None


def runs(s, log, join=True):
    """STYLE 2-5: a pass over the italicized value; returns the new value."""
    mask, intext, _ = protected(s, italics=False)
    two_ok = bool(re.search(r"\b" + MB + r" \d{1,2}, [4-7]\d\b", s))
    out, pos, i = [], 0, 0
    while True:
        m = HEAD.search(s, i)
        if not m:
            break
        head = item_at(s, m.start(), mask, intext, two_ok)
        if not head:
            i = m.end()
            continue
        a = m.start()
        paper = norm(head.title)
        is_nyt = paper == "New York Times" and head.title.strip("*") in NYT
        before = s[:a]
        attached = bool(re.search(r"(?:,[\"”'’] ?|[\w.)], )$", before))
        items, joins, e = [head], [], head.e
        while not attached and items[-1].ends and not items[-1].keep:
            j = JOIN.match(s, e)
            if not j:
                break
            it = item_at(s, j.end(), mask, intext, two_ok, paper)
            if not it or it.keep or (not is_nyt and (len(it.days) > 1 or len(items[-1].days) > 1)):
                break
            items.append(it)
            joins.append(j.group(0))
            e = it.e
        while len(items) > 1 and not items[-1].ends:
            items.pop()
            joins.pop()
        if attached and head.ends:
            j = JOIN.match(s, head.e)
            if j and item_at(s, j.end(), mask, intext, two_ok, paper):
                log.append(("ambiguous", f"run to {paper} not joined: its first cite follows an article's title "
                                         f"or a byline"))
        out.append(s[pos:a])
        out.append(render(items, joins, is_nyt, attached, log, join))
        pos = i = items[-1].e
    out.append(s[pos:])
    return "".join(out)


def serial(days, is_nyt, log):
    """[(Day, pin, its link already)] written once (STYLE 4)."""
    texts = []
    for k, (d, pin, url) in enumerate(days):
        year = k == len(days) - 1 or days[k + 1][0].y != d.y
        t = d.text(year)
        if pin:
            t += (", at " if year else " at ") + pin
        if is_nyt:
            u = url or nyt_url(d)
            if u:
                if not url:
                    log.append(("nyt-link", d.text(True)))
                t = f"[{t}]({u})"
            else:
                log.append(("ambiguous", f"New York Times, {d.text(True)}: no single issue to link "
                                         f"({'the strike' if d.day else 'not a single day'})"))
        texts.append(t)
    if len(texts) == 2:            # a year is followed by a comma: "Apr. 3, 1966, and Mar. 19, 1967"
        return texts[0] + (", and " if days[0][0].y != days[1][0].y else " and ") + texts[1]
    return ", ".join(texts[:-1]) + ", and " + texts[-1]


def single(it, is_nyt, log):
    """One cite in the form of STYLE 2-3 (a title of None: a date alone, after the run's first)."""
    if it.keep or it.pagelink or (it.url and is_nyt and not URLTM.fullmatch(it.url)):
        return it.raw
    lead = f"{it.title}, " if it.title else ""
    if len(it.days) > 1:
        if not is_nyt:
            return it.raw
        log.append(("serial", f"{len(it.days)} days of one month to New York Times"))
        return lead + serial([(d, None, None) for d in it.days], True, log)
    d = it.days[0]
    if it.form in ("two", "day1"):
        log.append(("date-form", f"{it.raw[len(lead):].split(', at')[0]} -> {d.text(True)}"))
    text = lead + d.text(True)
    if is_nyt:
        u = it.url or nyt_url(d)
        if u:
            if not it.url:
                log.append(("nyt-link", d.text(True)))
            text = f"[{text}]({u})"
        else:
            log.append(("ambiguous", f"New York Times, {d.text(True)}: no single issue to link "
                                     f"({'the strike' if d.day else 'not a single day'})"))
    elif it.url:
        text = f"[{text}]({it.url})"
    if it.pin is not None:
        text += f", at {it.pin}"
        if it.pin_raw != f", at {it.pin}":
            log.append(("pin-at", f"{it.pin_raw.strip(', ')} -> at {it.pin}"))
    return text


def render(items, joins, is_nyt, attached, log, join=True):
    title = items[0].title
    linked_off = any(x.url and (not is_nyt or not URLTM.fullmatch(x.url) or x.url != nyt_url(x.days[0]))
                     for x in items)
    mergeable = (len(items) > 1 and join and not attached and not linked_off
                 and all(x.ends and not x.pagelink and not x.keep for x in items)
                 and (is_nyt or not any(x.pin and "," in x.pin for x in items)))
    if not mergeable:
        if len(items) > 1:
            why = ("its first cite follows an article's title or a byline" if attached else
                   "the entry's claim map (src) names its cites one by one" if not join else
                   "a cite linked elsewhere, or a pinpoint holding a comma")
            log.append(("ambiguous", f"run of {len(items)} to {norm(title)} not joined: {why}"))
        parts = []
        for k, it in enumerate(items):
            parts.append(single(it, is_nyt, log))
            if k < len(joins):
                parts.append(joins[k])
        return "".join(parts)
    days = []
    for it in items:
        if it.form in ("two", "day1"):
            log.append(("date-form", f"{it.raw.split(', ', 1)[-1] if it.title else it.raw} -> series form"))
        days += [(d, None, None) for d in it.days[:-1]] + [(it.days[-1], it.pin, it.url)]
    log.append(("serial", f"{len(days)} cites to {norm(title)}"))
    return f"{title}, " + serial(days, is_nyt, log)


def transform(v, join=True):
    log = []
    s = italicize(v, log)
    s = runs(s, log, join)
    return s, log


def src_kept(entry, old, new):
    """STYLE 8: every row of the entry's claim map that finds its item in the old note finds one in the new."""
    if not entry or not entry.get("rows"):
        return True

    def found(n):
        e = {"c": entry.get("c") or "", "n": n, "src": {"c": "", "rows": entry["rows"]}}
        return [r for r, kind, *_, item in claims.resolve(e) if kind and item is not None]
    return set(found(old)) <= set(found(new))


# --- the files ---------------------------------------------------------------------------------------------------

def emit(prefix, old_raw, new):
    """The line with its value rewritten: the quoting kept (STYLE 7)."""
    if old_raw.startswith("'") or old_raw.startswith('"') or new[:1] in "*[&!|>'\"%@`{#?-:,":
        val = "'" + new.replace("'", "''") + "'"
    else:
        val = new
        try:
            if yaml.safe_load(val) != new or ": " in new or " #" in new:
                val = "'" + new.replace("'", "''") + "'"
        except yaml.YAMLError:
            val = "'" + new.replace("'", "''") + "'"
    line = prefix + val
    return line


def values(lines):
    """(index, prefix, raw value, entry id, field) for every note and gloss text line."""
    eid, gloss, text = None, False, False
    for i, ln in enumerate(lines):
        m = re.match(r"^  - id: (\S+)", ln)
        if m:
            eid, gloss, text = m.group(1), False, False
            continue
        if ln.startswith("    gloss:"):
            gloss, text = True, False
            continue
        if gloss:
            if re.match(r"^    \S", ln) or re.match(r"^  - ", ln) or not ln.strip():
                gloss = text = False
            elif ln.startswith("      text:"):
                text = True
                continue
            elif re.match(r"^      \S", ln):
                text = False
                continue
            elif text:
                m = re.match(r"^(        - )(.*)$", ln)
                if m:
                    yield i, m.group(1), m.group(2), eid, "gloss"
                continue
        m = re.match(r"^(    n: )(.*)$", ln)
        if m:
            yield i, m.group(1), m.group(2), eid, "n"


def entries(lines):
    """Each entry's `c` and claim-map rows (src), read off the lines: {id: {"c": str, "rows": [str]}}."""
    out, eid, where = {}, None, None
    for ln in lines:
        m = re.match(r"^  - id: (\S+)", ln)
        if m:
            eid, where = m.group(1), None
            out[eid] = {"c": "", "rows": []}
            continue
        if eid is None:
            continue
        if ln.startswith("    c: "):
            try:
                out[eid]["c"] = yaml.safe_load(ln[7:]) or ""
            except yaml.YAMLError:
                pass
        if re.match(r"^    \S", ln):
            where = "src" if ln.startswith("    src:") else None
        elif where and ln.startswith("      rows:"):
            where = "rows"
        elif where == "rows" and ln.startswith("        - "):
            try:
                out[eid]["rows"].append(str(yaml.safe_load(ln[10:])))
            except yaml.YAMLError:
                pass
    return out


def candidates(root):
    """--titles: every phrase in a cite's position, 'Title, Month day, year', plain or italic, with its count."""
    pat = re.compile(r"((?:\*?(?:The )?[A-Z][\w'’&.-]*(?: (?:of|and|the|&)? ?[A-Z][\w'’&.-]*)*\*?)),? (?:"
                     + M + "|" + MB + r") \d")
    c = collections.Counter()
    for f in sorted(glob.glob(os.path.join(root, "lists", "*", "*.yaml"))):
        lines = open(f, encoding="utf-8").read().split("\n")
        for i, pre, raw, eid, fld in values(lines):
            try:
                v = yaml.safe_load(raw)
            except yaml.YAMLError:
                continue
            if isinstance(v, str):
                for m in pat.finditer(v):
                    c[m.group(1).lstrip("[")] += 1
    known = set(TITLES) | set(EXPAND) | {"The " + t for t in THE_IN}
    for t, n in c.most_common():
        k = t.strip("*")
        print(f"{n:5d}  {'IN ' if k in known else '   '} {t}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--root", default=REPO)
    ap.add_argument("--titles", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    if a.titles:
        candidates(a.root)
        return
    kinds, titles, amb = collections.Counter(), collections.Counter(), collections.Counter()
    nvals = nfiles = 0
    for f in sorted(glob.glob(os.path.join(a.root, "lists", "*", "*.yaml"))):
        text = open(f, encoding="utf-8").read()
        lines = text.split("\n")
        info = entries(lines)
        changed = False
        for i, pre, raw, eid, fld in values(lines):
            if "*" not in raw and not TITLE_RE.search(raw):
                continue
            try:
                v = yaml.safe_load(raw)
            except yaml.YAMLError:
                continue
            if not isinstance(v, str):
                continue
            new, log = transform(v)
            if fld == "n" and new != v and not src_kept(info.get(eid), v, new):
                new, log = transform(v, join=False)
                if not src_kept(info.get(eid), v, new):
                    new, log = v, [("ambiguous", "the claim map (src) names an item the change would break")]
            for k, d in log:
                if k == "ambiguous":
                    amb[d] += 1
                    if not a.quiet:
                        print(f"# {eid} ({fld}): left alone: {d}")
                else:
                    kinds[k] += 1
                    if k in ("italicize", "expand"):
                        titles[d] += 1
            if new == v:
                continue
            line = emit(pre, raw, new)
            back = yaml.safe_load(line[len(pre):])
            assert back == new, (f, i + 1)
            if not a.quiet:
                print(f"{eid} ({fld}) {os.path.relpath(f, a.root)}:{i + 1}\n  before: {v}\n  after:  {new}")
            lines[i] = line
            changed = True
            nvals += 1
        if changed:
            nfiles += 1
            if a.write:
                open(f, "w", encoding="utf-8").write("\n".join(lines))
    print(f"\n{nvals} values changed in {nfiles} files" + ("" if a.write else " (dry run)"))
    for k, n in kinds.most_common():
        print(f"  {k}: {n}")
    print("titles italicized:")
    for t, n in titles.most_common():
        print(f"  {n:5d} {t}")
    print(f"left alone: {sum(amb.values())}")
    for t, n in amb.most_common(60):
        print(f"  {n:5d} {t}")


if __name__ == "__main__":
    main()
