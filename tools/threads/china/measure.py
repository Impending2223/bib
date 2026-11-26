#!/usr/bin/env python3
"""Measure the proposed re-threading of `china-leadership` (the brief: notes/briefs/china-threads-measure.md).

One command, from the tree's root:

    python3 tools/threads/china/measure.py [--scratch DIR] [--no-tsv] [--sample N M] [--variant NAME]

It reads `lists/cal/*.yaml` (never `build/`), places every `thread: china-leadership` entry by rule, writes
`notes/threads/china-assign.tsv` (id, date, thread or `-`, rule, second thread or `-`) and prints the tables of
the measurement as Markdown. Nothing else in the tree is written. `--scratch DIR` also writes `measure.json`
(the counts) and, with `--sample N M`, `sample.jsonl` (N entries drawn at random from each proposed thread and
M from the leftovers, seed fixed) into DIR. `--no-tsv` leaves the tsv alone.

The rule, in order (the first that fits takes the entry):
  (a) an episode thread: the survey's 26 (scheme.py, lexicon.py), as mended here (EPISODE MENDS below);
      rule names `ep:word` (a word of the episode inside its window), `ep:days` (a conference's days and a word
      for a meeting), `ep:stage` (a Cultural Revolution stage: its months and a word of the movement), `ep:place` (Yang Shangkun
      at his Four Cleanups post in Shaanxi, October 1964 to May 1965),
      `ep:book` (the entry was read from a book whose whole subject is the episode), and, tried after the
      persons, `ep:fallen` (a line headed by one of the fallen leaders after his fall, May 1966 to April 1969:
      the stage of its month);
  (b) the person thread of Mao, Zhou Enlai or Liu Shaoqi where he is the one acting: he heads the line, alone
      or in a list (`person:head`), the act named at the head is his (`person:his`, "Mao's comment"), he
      presides (`person:presides`), he receives the caller (`person:audience`, "calls on Mao", "at Mao's"), or
      he is the subject of the opening clause after a place or an occasion (`person:clause`);
  (c) the system the business belongs to (systems.py): `sys:matter` (the words of the business),
      `sys:body` (a body of the Center meets or acts and the line states no one system's matter),
      `sys:office` (the person at the head holds an office of one system and the line states no matter).
An entry that fits none is a leftover (`-`), its kind in the rule column (`left:personal`, `left:movement`,
`left:bare`, `left:other`). The second thread is the next that would have fitted.

The audit by reading of Nov. 26, 2026 (notes/threads/china-assign-audit.md) mended the rules; each mend is marked
`AUDIT MEND n` here and in systems.py, numbered as in the audit's note.

Variants (`--variant`): `foreign-first` (a foreign matter goes to the system before the person threads of
Zhou and Liu); `no-book` (no `ep:book` rule); `no-office` (no `sys:office` rule).
"""
import sys, os, re, json, glob, collections, random, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
from scheme import EPISODES, CRW                      # the survey's 26 episodes: words and windows
import systems as SY

# ---------------------------------------------------------------- reading the calendar
FIELDS = ('id', 'date', 'when', 'thread', 'also', 'c', 'n', 'place', 'tags')
def _unq(v):
    v = v.strip()
    if v.startswith("'") and v.endswith("'") and len(v) >= 2: return v[1:-1].replace("''", "'")
    if v.startswith('"') and v.endswith('"') and len(v) >= 2:
        return v[1:-1].encode().decode('unicode_escape') if '\\' in v else v[1:-1]
    return v
def _lst(v):
    v = v.strip()
    if v.startswith('['): return [x.strip().strip("'\"") for x in v[1:-1].split(',') if x.strip()]
    return [v] if v else []
def read_calendar():
    """Every calendar entry touching the China threads, as dicts (regex over the YAML, as the survey's extract.py)."""
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'lists', 'cal', '[0-9]*.yaml'))):
        cur = None; key = None
        def flush():
            if not cur: return
            th = cur.get('thread', '').strip(); al = _lst(cur.get('also', ''))
            if th in ('china-leadership', 'china') or {'china-leadership', 'china', 'india-and-china-cultural-revolution'} & set(al):
                e = {k: cur.get(k, '').strip() for k in ('id', 'when', 'place')}
                e['thread'] = th; e['date'] = cur.get('date', '').strip().strip("'"); e['also'] = al
                e['c'] = _unq(cur.get('c', '')); e['n'] = _unq(cur.get('n', ''))
                e['works'] = re.findall(r'\[\[(w\.[^\]]+)\]\]', e['n']); e['tags'] = _lst(cur.get('tags', ''))
                out.append(e)
        for ln in open(f, encoding='utf-8').read().split('\n'):
            m = re.match(r'  - id: (.*)$', ln)
            if m: flush(); cur = {'id': m.group(1).strip()}; key = 'id'; continue
            if cur is None: continue
            m = re.match(r'    ([a-z_]+):(?: (.*))?$', ln)
            if m: key = m.group(1); cur[key] = (m.group(2) or ''); continue
            if re.match(r'     +\S', ln) and key in FIELDS: cur[key] += ' ' + ln.strip()
            elif re.match(r'    \S', ln) or re.match(r'\S', ln): key = None
        flush()
    return out

HAN = re.compile(r'[㐀-鿿　-〿＀-￯·]+')
def plain(c):
    """The line without cuts ({3}); characters kept."""
    return re.sub(r'\s+', ' ', re.sub(r'\{\d+\}', '', c)).strip()
def roman(c):
    """The line as the page shows it, more or less: no cuts, no characters, no parentheses."""
    c = HAN.sub('', plain(c)); c = re.sub(r'\s*\([^)]*\)', '', c); c = c.replace('*', '')
    c = re.sub(r'\s+', ' ', c).strip()
    return re.sub(r'\s+([,.;:\'])', r'\1', c)
def inwin(d, lo, hi):
    if len(d) >= 7: return lo <= d[:7] <= hi
    return lo[:4] <= d[:4] <= hi[:4]

# ---------------------------------------------------------------- (a) episodes
SPAN = {s: (lo, hi) for s, n, lo, hi, c, w in EPISODES}
EPNAME = {s: n for s, n, lo, hi, c, w in EPISODES}
EPC = [(s, [(a, b, re.compile(r, re.I)) for a, b, r in comps], w) for s, n, lo, hi, comps, w in EPISODES]
# words of the movement the survey's list lacked: the fallen struggled against, questioned, held
CRW_MORE = r"|struggled against|is struggled|\bstruggles? (?:Peng|Liu|Deng|Luo|He Long|Lu Dingyi|Yang Shangkun|Tao Zhu)|taken there to be struggled|case office|case group|interrogat|\bparaded\b|the sentry|his guards?\b|guard officer|in custody|his arrest|\barrested\b|persecuted to death|commits suicide|suicide"
CRWR = re.compile(CRW + CRW_MORE, re.I)
# the conferences' days (the survey's final.py)
CONF = [('china-shanghai-1960', '1960-01-07', '1960-01-17'), ('china-shanghai-1960', '1960-07-05', '1960-08-10'), ('china-twelve-articles', '1961-01-14', '1961-01-18'),
        ('china-sixty-articles', '1961-03-10', '1961-03-23'), ('china-sixty-articles', '1961-05-21', '1961-06-12'), ('china-sixty-articles', '1961-08-23', '1961-09-16'),
        ('china-seven-thousand', '1962-01-11', '1962-02-07'), ('china-retreat-1962', '1962-02-21', '1962-02-23'), ('china-retreat-1962', '1962-05-07', '1962-05-11'),   # AUDIT MEND 12: the May work conference, a station of the thread's statement
        ('china-tenth-plenum', '1962-07-25', '1962-08-24'), ('china-tenth-plenum', '1962-09-24', '1962-09-27'),
        ('china-four-cleanups', '1963-05-02', '1963-05-12'), ('china-four-cleanups', '1964-12-15', '1965-01-14'), ('china-luo-ruiqing', '1965-12-08', '1965-12-15'),
        ('china-may-sixteenth', '1966-05-04', '1966-05-26'), ('china-red-guards', '1966-08-01', '1966-08-12'), ('china-red-guards', '1966-10-09', '1966-10-28'),
        ('china-ninth-congress', '1968-10-13', '1968-10-31'), ('china-ninth-congress', '1969-04-01', '1969-04-24')]
CONFW = re.compile(r"\bconference|会议|大会(?!堂)|plenary|plenum|全会|group meeting|小组|the meeting|Politburo|政治局|Ninth (?:Party )?Congress|Party Congress|\bthe Congress\b|drafting committee|draft report", re.I)
# AUDIT MEND 4: a conference's days are not shown by the Great Hall (人民大会堂), the National People's
# Congress, a mass body's congress, a ceremonial meeting or a named small group (精简小组); these are cut from the line before CONFW is tried.
CONFCUT = re.compile(r"人民大会堂|Great Hall of the People|National People's Congress|People's Congress|全国人大|人民代表大会|\b(?:the )?meeting marking\b|(?:Streamlining|streamlining) [Gg]roup|精简小组|"
                     r"\b(?:national|all-army|army's|ministry's|provincial|municipal|prefectural|county)\b[^.;]{0,50}\b(?:conference|congress)|代表大会|文代会|Congress of (?:Chinese )?Writers")
STAGES = [(s, w) for s, n, lo, hi, c, w in EPISODES if w]
BOOK_CR = {'w.yang-jisheng-tiandi-fanfu', 'w.pu-weihua-zalan-jiu-shijie', 'w.macfarquhar-maos-last-revolution', 'w.dikotter-cultural-revolution'}
BOOK_FAMINE = {'w.yang-jisheng-mubei', 'w.dikotter-maos-great-famine'}
BOOK_POLEMIC = {'w.lengxi-shinian-lunzhan-1956-1966'}
SHAANXI = {'xian', 'niujiao', 'changan-county', 'shaanxi', 'yanan', 'hanzhong', 'baoji', 'lintong', 'doumen', 'huashan', 'xixiang', 'ningshan', 'shiquan', 'mian-county', 'feng-county', 'fengxiang', 'ankang'}
SHAANXIW = re.compile(r"Xi'an|Niujiao|Chang'an|Doumen|Zhangbagou|Shaanxi|Northwest Bureau|sixteen-county|Hanzhong|Yan'an")
# AUDIT MEND 6: the post is Chang'an county (Niujiao, Doumen) and Xi'an; his tour of south Shaanxi and Yan'an (Apr.-May 1965), his journeys,
# his illness and his evenings are not the Four Cleanups.
POST = {'xian', 'niujiao', 'changan-county', 'doumen'}
POSTW = re.compile(r"Xi'an|Niujiao|Chang'an|Doumen|Zhangbagou|Northwest Bureau|sixteen-county")
POSTWORK = re.compile(r"work corps|work teams?|Four Cleanups|四清|poor peasants|brigade|squatting|socialist education", re.I)
TOUR = {'yanan', 'hanzhong', 'baoji', 'xixiang', 'ningshan', 'shiquan', 'mian-county', 'feng-county', 'fengxiang', 'lintong', 'huashan', 'ankang'}
TOURW = re.compile(r"Yan'an|Hanzhong|Baoji|Xixiang|Ningshan|Shiquan|Huashan|Ankang|Lintong")
TOURDAY = re.compile(r"\bfilms?\b|\bdines?\b|\bdinner\b|physician|hospital|palpitation|swollen|\bvisits the\b|\bsees the\b|photograph", re.I)
def winlen(s):
    lo, hi = SPAN[s]; return (int(hi[:4]) * 12 + int(hi[5:7])) - (int(lo[:4]) * 12 + int(lo[5:7]))

# EPISODE MENDS: what the test by reading changed in the survey's rules (notes/proposals/china-threads-measure.md, "What the test changed").
# 1. A key that is only a place or a person is weak: it places an entry only with a strong key of the same episode,
#    or (a conference's seat) with a word for a meeting, or with a second weak key.
WEAK = re.compile(r"^(?:Beidaihe|北戴河|Lushan|庐山|PLACE:\S+|Xilou|西楼|Algiers|阿尔及尔|Jakarta|雅加达|Bandung|Ben Bella|本·贝拉|Boumediene|布迈丁|Tian Jiaying|田家英|Zeng Xisheng|曾希圣|Deng Zihui|邓子恢|"
                  r"Albania|阿尔巴尼亚|Hoxha|Shehu|Khrushchev|赫鲁晓夫|revision\w*|修正主义|split|anti-Chinese|mess halls?|canteens?|食堂|experts|专家|Ministry of Culture|文化部|Zhou Yang|周扬|"
                  r"political departments?|政治部|war preparation|备战|prepare for war|evacuat\w*|Nie Rongzhen's|Kosygin|柯西金|Southwest(?:ern)? Bureau)$", re.I)   # AUDIT MEND 5: the Southwest Bureau alone
SEAT = re.compile(r"^(?:Beidaihe|北戴河|Lushan|庐山|PLACE:\S+|Xilou|西楼)$", re.I)
MEETING = re.compile(r"\bconference|\bplenary|\bplenum|(?<![Pp]arty )\bgroups?\b|\bsession|Politburo|Standing Committee|Secretariat|\bthe meeting\b|\bmeeting of\b|drafting|会议|全会", re.I)
ONLYCONF = {'china-afro-asian': re.compile(r"\bconference|会议", re.I)}
# 2. Words taken out of the line before an episode's keys are tried.
STRIP = {'china-bomb': re.compile(r"(?:Conference|Council|Congress)s? [Aa]gainst (?:Atomic|A-)(?: and Hydrogen| and H-)? ?[Bb]ombs?|against Atomic and Hydrogen Bombs|movement (?:for|against) (?:banning |the banning of )?atomic and hydrogen bombs", re.I),   # AUDIT MEND 10
         'china-india-war': re.compile(r"印度尼西亚|Indian Ocean|Indochina|印度支那")}
# 3. Keys the survey's lists lacked: (first day or month, last, regex).
MORE = {
 'china-bomb': [('1963-07', '1969-12', r"Special Commi(?:ssion|ttee)|Central Special|中央专门委员会|专委|Second Ministry of Machine|Seventh Ministry of Machine|test range|nuclear[- ]industry|warhead")],
 'china-polemic': [('1961-10', '1964-11', r"Pravda|真理报|\b(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth) comment|reply to the CPSU|letter of the CPSU|CPSU(?:'s)? letter|Togliatti|Thorez|anti-revisionis|Whence the differences")],
 'china-moscow-1960': [('1960-04', '1961-01', r"differences between (?:China and the Soviet|the two parties)|Sino-Soviet (?:differences|question)|parties' conference|drafting committee of the parties")],
 'china-four-cleanups': [('1962-09', '1966-05', r"socialist[- ]education")],
 'china-may-sixteenth': [('1966-04-09', '1966-05-31', r"Peng Zhen|彭真")],
 'china-border-war': [('1969-03', '1969-12', r"boundary (?:talks|question|rivers)|Kuznetsov|four marshals|marshals' reports?|prepar\w+ [^.;]{0,40}for war|Sino-Soviet (?:border|boundary)")],
 'china-sixty-articles': [('1961-04', '1961-05', r"Tianhua|天华|Ningxiang|宁乡|Xushui|徐水|Shunyi|顺义|Huairou|怀柔|Working Regulations|工作条例")],
 'china-seven-thousand': [('1962-01-11', '1962-02-07', r"drafting committee|draft report|the report's|起草委员会")],
 'china-shanghai-1960': [('1960-07', '1960-09', r"Soviet experts|苏联专家|experts (?:are |to be )?(?:withdrawn|recalled)|withdraw\w* (?:of )?(?:the |its )?experts|撤走专家")],
}
MOREC = {s: [(lo, hi, re.compile(r, re.I)) for lo, hi, r in rows] for s, rows in MORE.items()}
def inspan(d, lo, hi):
    if len(lo) == 10: return len(d) == 10 and lo <= d <= hi
    return inwin(d, lo, hi)
STAGEWIN = {s: w for s, w in STAGES}
def months_in_year(s, y):
    lo, hi = STAGEWIN[s]; return sum(1 for m in range(1, 13) if lo <= f"{y}-{m:02d}" <= hi)

# AUDIT MEND 1: the Great Leap's words (lexicon 'leap-1960') place an entry in Shanghai and Beidaihe, 1960, only on the two conferences'
# days (Jan. 7-17, July 5-Aug. 10) or in their months where the entry has no day; elsewhere in 1960 they are the year's ordinary business.
from lexicon import EP as _EP
LEAPRX = {r for s_, n_, lo_, hi_, r in _EP if s_ == 'leap-1960'}
def shanghai_days(d):
    if len(d) == 10: return '1960-01-07' <= d <= '1960-01-17' or '1960-07-05' <= d <= '1960-08-10'
    return d[:7] in ('1960-01', '1960-07', '1960-08')
def episodes(e, variant=''):
    """[(slug, rule)] of the episodes the entry fits, the one that takes it first."""
    d = e['date']; c = e['_plain']
    pl = [t.strip() for t in e['place'].split(' - ') if t.strip()]
    base = c + ' ' + ' '.join('PLACE:' + p for p in pl)
    first = e['_first']
    private = bool(e['_phead']) and bool(PERSONAL.search(first[:90]) or POEM.search(first[:70])) and not any(rx.fullmatch(n) for n in e['_head'] for _, rx in THREERX)
    if private and not e['_foreign']: return []           # a swim, a doctor, a poem in a conference's weeks is no part of the conference
    hits = []; weakonly = set(); seatonly = set()
    for s, comps, w in EPC:
        txt = STRIP[s].sub(' ', base) if s in STRIP else base
        keys = set()
        for a, b, r in comps:
            if s == 'china-shanghai-1960' and r.pattern in LEAPRX and not shanghai_days(d): continue
            if inwin(d, a, b): keys |= {m.group(0) for m in r.finditer(txt)}
        for a, b, r in MOREC.get(s, ()):
            if inspan(d, a, b) and r.search(txt): keys.add('+')
        if not keys: continue
        keys = {(HAN.sub('', k).strip() or k) for k in keys}                      # "Beidaihe 北戴河" is the key "Beidaihe"
        strong = [k for k in keys if not WEAK.match(k)]
        if not strong:
            weak = {k.lower() for k in keys if not HAN.fullmatch(k)} or {k for k in keys}     # the characters gloss the same key
            weak = {('albania' if k in ('hoxha', 'shehu') else k) for k in weak}               # one country, not three keys
            if s == 'china-opera' or private: continue
            seat = all(SEAT.match(k) for k in keys)
            meet = (ONLYCONF.get(s) or MEETING).search(c)
            if seat and not meet: continue
            if not seat and len(weak) < 2 and not (s in ONLYCONF and meet): continue
            weakonly.add(s)
            if seat and not any(len(d) == 10 and lo <= d <= hi for s2, lo, hi in CONF if s2 == s): seatonly.add(s)
        if s == 'china-opera' and e['_foreign']: continue          # a guest taken to the theatre is foreign business
        hits.append((s, 'ep:word'))
    if not e['_foreign'] and not private:
        for s, lo, hi in CONF:
            if len(d) == 10 and lo <= d <= hi and CONFW.search(CONFCUT.sub(' ', c)) and s not in [h[0] for h in hits]: hits.append((s, 'ep:days'))
    got = [h[0] for h in hits]
    if '1964-10' <= d[:7] <= '1965-05' and 'Yang Shangkun' in c and 'china-four-cleanups' not in got and (set(pl) & POST or POSTW.search(c)) \
       and (POSTWORK.search(c) or not (set(pl) & TOUR or TOURW.search(c))) and not (PERSONAL.search(first[:90]) or MOVEMENT.search(first) or TOURDAY.search(c)):
        hits.append(('china-four-cleanups', 'ep:place'))   # Yang Shangkun at his post in Chang'an county and at Xi'an
    if not hits:
        if not e['_foreign']:
            hits = [(s, 'ep:stage') for s, w in STAGES if inwin(d, *w) and CRWR.search(c)]
        if not hits and variant != 'no-book' and not private:
            w0 = e['works'][0] if e['works'] else ''
            if w0 in BOOK_FAMINE and inwin(d, '1959-10', '1962-12'): hits.append(('china-famine', 'ep:book'))
            if w0 in BOOK_POLEMIC and not MOVEMENT.search(first):
                hits += [(s, 'ep:book') for s in ('china-moscow-1960', 'china-polemic') if inwin(d, *SPAN[s])]
            if w0 in BOOK_CR: hits += [(s, 'ep:book') for s, w in STAGES if inwin(d, *w)]
    got = [h[0] for h in hits]
    # two episodes: the seams the test found, then the shorter span
    # AUDIT MEND 2: the two seams set which episode goes last; the rest are still ranked, so that a third episode (Famine, in July 1962)
    # no longer takes the entry by coming first in the list. AUDIT MEND 3: an episode found only by a conference's seat (the Xilou,
    # Beidaihe, Lushan) outside that conference's days ranks after one found by a strong key.
    last = set()
    if 'china-retreat-1962' in got and 'china-tenth-plenum' in got:               # the Beidaihe conference opens July 25, 1962
        last.add('china-tenth-plenum' if d < '1962-07-25' else 'china-retreat-1962')
    if 'china-twelve-articles' in weakonly and 'china-famine' in got:              # a mess hall in a famine report
        last.add('china-twelve-articles')
    def rank(h):
        if len(d) == 4 and h[0] in STAGEWIN: return (h[0] in last, h[0] in seatonly, -months_in_year(h[0], d))   # a year-dated entry: the stage that covers most of the year
        return (h[0] in last, h[0] in seatonly, winlen(h[0]))
    hits.sort(key=rank)
    return hits
# The fallen, from the month each was struck down: what is done to him and what he does in custody is the movement's.
FALLEN = {'Peng Zhen': '1966-05', 'Luo Ruiqing': '1966-01', 'Lu Dingyi': '1966-05', 'Yang Shangkun': '1966-05', 'Peng Dehuai': '1966-09', 'Liu Shaoqi': '1967-01',
          'Deng Xiaoping': '1967-01', 'Tao Zhu': '1967-01', 'He Long': '1967-01', 'Wang Guangmei': '1967-01', 'Bo Yibo': '1967-01', 'Huang Kecheng': '1966-09'}
def stage_of_fallen(e):
    """The Cultural Revolution stage of the month, for a line headed by one of the fallen (tried after the persons)."""
    d = e['date']
    if len(d) < 7: return []
    who = [n for n in e['_head'] if n in FALLEN and d[:7] >= FALLEN[n]]
    if not who: return []
    return [(s, 'ep:fallen') for s, w in STAGES if inwin(d, *w)]

# ---------------------------------------------------------------- (b) the three persons
THREE = [('china-mao', 'Mao', r"Mao Zedong|Mao(?! [A-Z][a-z])"), ('china-zhou', 'Zhou Enlai', r"Zhou Enlai|Zhou(?! [A-Z][a-z])"), ('china-liu', 'Liu Shaoqi', r"Liu Shaoqi|Liu(?! [A-Z][a-z])")]
PNAME = {'china-mao': 'Mao', 'china-zhou': 'Zhou Enlai', 'china-liu': 'Liu Shaoqi'}
ANYNAME = re.compile(r"(?:Mao Zedong|Mao|Zhou Enlai|Zhou|Liu Shaoqi|Liu)(?! [A-Z][a-z])|[A-Z][a-zü']+ [A-Z][a-zü']+")
THREERX = [(s, re.compile(r"(?:" + rx + r")\b")) for s, n, rx in THREE]
PREFV = re.compile(r"\b(?:receives?|meets?|talks?|writes?|says?|tells?|is|are|was|were|opens?|reads?|with|reports?|hears?|presides?|calls?|sees?|speaks?|sends?|approves?|goes|leaves?|arrives?|returns?|flies|visits?|attends?|has|have|will|not)\b")
PREP = re.compile(r"^(?:At|In|On|After|Before|From|Evening|Morning|Afternoon|Night|Noon|Late|Early|That (?:evening|night|morning|afternoon)|Later|Then|Midnight|About|Around|During|\d)[^,.;:]{0,110},\s+")
LED = re.compile(r"^(?:Mao|Zhou|Liu|[A-Z][a-zü']+ [A-Z][a-zü']+)(?: Zedong| Enlai| Shaoqi)? (?!of\b)[a-z]")   # a person and what he does: not a place
TIMEEND = re.compile(r"(?:\b[ap]m|\bnoon|\bmidnight|\bevening|\bnight|\bmorning|\bafternoon|\bdawn|\bdusk|\d)$")
def strip_prefix(c):
    """Drop a leading place or time ("Peking, the Great Hall, 3 p.m. ", "In the evening, ")."""
    c = re.sub(r"(\d):(\d\d)", r"\1h\2", c)
    c = re.sub(r"\b(Jan|Feb|Mar|Apr|Aug|Sept|Sep|Oct|Nov|Dec|No|Nos|St|Dr|Col|Gen|Mt|Mrs|Mr)\.(?= )", r"\1", c)
    c = re.sub(r"\b([ap])\.m\.(?= [A-Z])", r"\1m.", re.sub(r"\b([ap])\.m\.(?! [A-Z])", r"\1m", c))
    for _ in range(4):
        m = re.match(r"^([^.:;]{1,110}?)\.\s+(?=[A-Z\"'])", c)
        if m and not LED.match(m.group(1)) and (TIMEEND.search(m.group(1)) or (not PREFV.search(m.group(1)) and len(m.group(1).split()) <= 12)): c = c[m.end():]; continue
        m = PREP.match(c)
        if m: c = c[m.end():]; continue
        break
    return c
def head_names(s):
    """The persons at the head of the line: 'A', 'A and B', 'A, B and C', 'A, with B and C,'."""
    names = []; pos = 0
    while True:
        m = ANYNAME.match(s, pos)
        if not m: break
        names.append(m.group(0)); pos = m.end()
        m2 = re.match(r"(?:, with|, and| with| and|,)\s+", s[pos:])
        if m2 and ANYNAME.match(s, pos + m2.end()): pos += m2.end(); continue
        break
    return names, s[pos:]
HISACT = r"(?:comments?|letters?|talks?|instructions?|notes?|speech(?:es)?|telegrams?|repl(?:y|ies)|reports?|messages?|cables?|remarks?|directives?|orders?|poems?|inscriptions?|articles?|interviews?|conversations?|toasts?|statements?|greetings|condolences|answers?|words|draft|revisions?|visit|tour|trip|journey|inspection)"
CLAUSEV = r"receives?|meets?|tells?|says?|speaks?|visits?|attends?|hears?|calls?|writes?|reads?|approves?|orders?|asks?|sends?|gives?|goes|learns?|reports?|presides?|answers?|agrees?|revises?|decides?|signs?|sees?|talks?|inspects?|notes?|replies|cables?|telegraphs?|convenes?|interjects?|proposes?|has"
def persons(e):
    """[(slug, rule)] of the three who act in the line, the first named first."""
    s = e['_head_s']; names = e['_head']; out = []
    for nm in names:
        for slug, rx in THREERX:
            if rx.fullmatch(nm) and slug not in [o[0] for o in out]: out.append((slug, 'person:head'))
    if not names:
        for slug, rx in THREERX:
            if re.match(r"(?:" + rx.pattern + r")'s " + HISACT + r"\b", s): out.append((slug, 'person:his'))
    first = re.split(r"(?<=[a-z\)\"])\.\s", s, maxsplit=1)[0]
    for slug, rx in THREERX:
        if slug in [o[0] for o in out]: continue
        if re.search(r"(?:" + rx.pattern + r")(?: (?:Zedong|Enlai|Shaoqi))? (?:presid(?:es|ing)|in the chair|chairs|chairing)", first): out.append((slug, 'person:presides'))
    for slug, rx in THREERX:
        if slug in [o[0] for o in out]: continue
        n = r"(?:" + rx.pattern + r")"
        if re.search(r"\b(?:calls? on|received by|goes to see|to see|sent for by|summoned by) " + n + r"|\bat " + n + r"'s(?: place| home| residence| office)?[ ,.;]|" + n + r" sends for\b", first): out.append((slug, 'person:audience'))
    if not names and not out:
        clause = re.split(r"[.;]\s", s, maxsplit=1)[0]
        for slug, rx in THREERX:
            if re.search(r"(?:" + rx.pattern + r")(?::| (?:" + CLAUSEV + r")\b)", clause): out.append((slug, 'person:clause'))
    if e['date'] >= '1968-11': out = [o for o in out if o[0] != 'china-liu']
    return out

# ---------------------------------------------------------------- (c) the systems
MAT = {k: [(w, re.compile(r, re.I)) for w, r in rows] for k, rows in SY.MATTER.items()}
HEADBODY = {k: re.compile(r, re.I) for k, r in SY.HEADBODY.items()}
COUNTRY = re.compile(SY.COUNTRY)
PERSONAL = re.compile(SY.PERSONAL); MOVEMENT = re.compile(SY.MOVEMENT); POEM = re.compile(SY.POEM)
OFFICE = collections.defaultdict(list)
for nm, sysk, lo, hi in SY.OFFICE: OFFICE[nm].append((sysk, lo, hi))
COUNTRY_THREADS = re.compile(r"^(?:soviet-union|africa|south-asia|vietnam-hanoi|vietnam-diplomacy|vietnam-paris|indonesia|japan|laos|middle-east|korea|cuba|latin-america|europe-and-the-alliance|congo|berlin-and-vienna|foreign-aid|india-and-china(?!-cultural)|canada|mongolia|singapore)")
ABROAD = set("""moscow jakarta rangoon geneva algiers hanoi cairo bucharest pyongyang tirana kabul phnom-penh karachi bamako conakry katmandu new-delhi ulan-bator rawalpindi damascus rabat tunis mogadishu colombo accra dacca
dar-es-salaam bogor lahore nairobi khartoum alexandria mandalay taunggyi bandung siem-reap hamhung ngapali asmara surabaya zanzibar craiova bai-chay moulmein tangier korce vlore kindia islamabad bali constanta london
addis-ababa agra pokhara kompong-cham sandoway budapest leningrad haiphong tampaksiring kirirom shkoder labe taxila segou calcutta kampot-province vinh alma-ata tashkent paghman barvikha minsk irkutsk pagan bern lausanne
kaesong sinuiju tokyo viet-tri ha-long-bay hon-gai prague denpasar songnim hamju-county port-said aswan oran casablanca berat tema koulikoro omdurman axum brazzaville tehran helwan herat durres paris khabarovsk warsaw""".split())
RECEIVE = re.compile(r"\b(?:receiv(?:es?|ing)|meets?|sees? off|send-off|seen off|welcomes?|banquets?|receptions?|talks? with|calls? on|dinner|luncheon|farewell|accompan(?:y|ies)|visits?|guests?|takes|shows|hosts?|entertains?|cables?|telegraphs?|congratulat\w+|condolences|rall(?:y|ies)|in support of|solidarity|comrades|Communists|delegates?)\b")
CENTER_BODY = re.compile(r"(?<!'s )(?<!committee )\b[Tt]he Secretariat\b(?! of the (?!Central|Chinese))|\bAt the Secretariat\b|Central Secretariat|中央书记处|\b[Tt]he Politburo\b|Politburo(?:'s)? Standing Committee|Politburo meeting|中央政治局|\b[Tt]he Standing Committee\b(?! of)|Central Work Conference|中央工作会议|\bwork conference\b|\b[Tt]he Center(?:'s)?\b|中共中央|\bCentral Committee (?:issues|forwards|approves|decides|circulates|transmits|sends)|General Office|办公厅|\bplenum\b|regional bureaus' (?:first )?secretaries")
NOT_CENTER = re.compile(r"(?:National People's Congress|NPC|CPPCC|Political Consultative Conference|People's Congress|[Pp]arty committee|provincial committee|municipal committee|[Cc]ommittee's|Supreme People's Assembly)(?:'s)?(?: 全国人大| 政协)? (?:enlarged )?Standing Committee|Standing Committee of the (?:\w+ )?(?:National|NPC|CPPCC|Supreme|Political|\w+ (?:provincial|municipal|[Pp]arty) committee)|Central Committee of the (?!Chinese)|[Pp]olitburo of the (?!Chinese)|(?:Workers' Party|Communist Party of \w+|Lao Động|Labor Party|Labour Party)(?:'s)? (?:Central Committee|Politburo)")
HEADZONE = 200
def foreign_evidence(e):
    """0-3: how strongly the entry is marked as business with another country (tags, also:, place, words)."""
    c = e['_plain']; ev = 0
    if any(t.startswith('polity:') and t not in ('polity:prc', 'polity:roc') for t in e['tags']): ev = 3
    elif any(COUNTRY_THREADS.match(a) for a in e['also']): ev = 2
    elif COUNTRY.search(c): ev = 1
    if set(p.strip() for p in e['place'].split(' - ')) & ABROAD: ev = max(ev, 3)
    return ev
VENUE = re.compile(SY.VENUE)
def system_scores(e):
    c = VENUE.sub(' ', e['_plain']); sc = {}; hitrows = collections.defaultdict(set)
    for k, rows in MAT.items():
        sc[k] = 0
        for i, (w, r) in enumerate(rows):
            m = r.search(c)
            if m: sc[k] += w if m.start() < HEADZONE else 1; hitrows[k].add(i)
    head = e['_head_s'][:70]
    for k, r in HEADBODY.items():
        if r.search(head): sc[k] += 4
    ev = e['_fev']
    if ev:
        sc['foreign'] += ev + (2 if RECEIVE.search(c) else 0)
        if hitrows['culture'] == {1}: sc['foreign'] += 3      # AUDIT MEND 11: a foreign guest at a performance is foreign business
    al = set(e['also'])
    if 'farm' in al: sc['farm'] += 2
    if al & {'economy', 'trade', 'budget', 'taxes', 'oil'}: sc['economy'] += 2
    if al & {'defense'}: sc['army'] += 2
    if al & {'press-and-broadcasting'}: sc['culture'] += 2
    return sc
OFFNAME = re.compile('|'.join(sorted((re.escape(nm) for nm in OFFICE), key=len, reverse=True)))
def office_of(e):
    """The system of the first office-holder at the head of the line; failing that, of the first one named in it."""
    d = e['date'][:7]
    # AUDIT MEND 8 (ruling 58, 5): a caller on the director of the General Office is the Center's daily work, whatever the caller's own office.
    if 'Yang Shangkun' in e['_roman'] and d <= '1965-11': return 'center'
    for nm in e['_head'] + OFFNAME.findall(e['_roman']):
        for sysk, lo, hi in OFFICE.get(nm, ()):
            if (not lo or d >= lo) and (not hi or d <= hi): return sysk
    return None
def systems(e, variant=''):
    """[(slug, rule)] the systems the business fits, best first; and the kind of leftover where none."""
    sc = e['_sc']; c = e['_roman']
    ranked = sorted((k for k in sc if sc[k] >= 2 and k != 'center'), key=lambda k: (-sc[k], SY.ORDER.index(k)))
    body = bool(CENTER_BODY.search(NOT_CENTER.sub(' ', e['_plain'][:HEADZONE]))) or sc['center'] >= 3
    off = office_of(e)
    out = []
    if body and (not ranked or (len(ranked) >= 3 and sc[ranked[2]] >= 3 and sc[ranked[2]] >= sc[ranked[0]] - 2)):
        out.append(('center', 'sys:body'))               # a body of the Center, and no one system's matter
    for k in ranked[:2]: out.append((k, 'sys:matter'))
    if body and 'center' not in [o[0] for o in out]: out.append(('center', 'sys:body'))
    first = e['_first']
    personal = bool(e['_phead']) and bool(PERSONAL.search(first[:90]) or re.search(r"Hospital|医院", e['_plain'][:40])); moving = bool(MOVEMENT.search(first)) and not re.search(r"\bto talk\b|\bto report\b|\bto discuss\b", first)   # AUDIT MEND 7: a line set in a hospital
    if (e['_phead'] and POEM.search(first[:70])) or (personal and (not ranked or sc[ranked[0]] <= 3) and not e['_foreign']):
        e['_left2'] = off or (ranked[0] if ranked else None)   # a poem, a doctor, a swim, a film: no system's business
        return [], 'left:personal'
    if not ranked and not body:
        if off and variant != 'no-office' and not personal and not moving: out.append((off, 'sys:office'))
        elif off: e['_left2'] = off
    kind = 'left:movement' if moving else 'left:bare' if len(c) < 90 else 'left:other'
    return [(SY.NAMES[k][0], r) for k, r in out], kind

# ---------------------------------------------------------------- the assignment
NOTPERSON = {'Peking', 'Central', 'Party', 'State', 'Foreign', 'Great', 'Red', 'Military', 'General', 'National', 'Renmin', 'Jiefangjun', 'Hongqi', 'Xinhua', 'Guangming', 'Zhongguo',
             'Cultural', 'Chinese', 'Shanghai', 'Northwest', 'North', 'East', 'Southwest', 'Streamlining', 'Politburo', 'Standing', 'Seven', 'Youth', 'Women', 'Ministry', 'People'}
def prepare(E):
    for e in E:
        e['_plain'] = plain(e['c']); e['_roman'] = roman(e['c'])
        e['_head_s'] = strip_prefix(e['_roman']); e['_head'], e['_rest'] = head_names(e['_head_s'])
        e['_phead'] = [n for n in e['_head'] if not n.startswith(('The ', 'A ', 'An ')) and n.split()[0] not in NOTPERSON]   # persons, not "The Center"
        e['_first'] = re.split(r"(?<=[a-z\)\"])[.;]\s", e['_head_s'], maxsplit=1)[0]
        e['_fev'] = foreign_evidence(e); e['_foreign'] = e['_fev'] >= 2 or (e['_fev'] == 1 and bool(RECEIVE.search(e['_plain'])))
        e['_sc'] = system_scores(e)
def assign(e, variant=''):
    """(thread or '-', rule, second thread or '-', all fits)."""
    ep = episodes(e, variant); pe = persons(e); sy, kind = systems(e, variant)
    if variant == 'foreign-first' and sy and sy[0][0] == 'china-foreign':
        pe2 = [p for p in pe if p[0] == 'china-mao']; rest = [p for p in pe if p[0] != 'china-mao']
        fits = ep + pe2 + sy[:1] + rest + sy[1:]
    else:
        sd = stage_of_fallen(e) if not ep else []
        fits = ep + pe + sd + sy
    seen = []; uniq = []
    for t, r in fits:
        if t not in seen: seen.append(t); uniq.append((t, r))
    if not uniq: return '-', kind, SY.NAMES[e['_left2']][0] if e.get('_left2') else '-', []
    return uniq[0][0], uniq[0][1], (uniq[1][0] if len(uniq) > 1 else '-'), uniq

def kind_of(t):
    return 'episode' if t in SPAN else 'person' if t in PNAME else 'leftover' if t == '-' else 'system'

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--scratch'); ap.add_argument('--no-tsv', action='store_true')
    ap.add_argument('--sample', nargs=2, type=int); ap.add_argument('--variant', default=''); ap.add_argument('--seed', type=int, default=1126)
    a = ap.parse_args()
    ALL = read_calendar(); prepare(ALL)
    CL = [e for e in ALL if e['thread'] == 'china-leadership']
    for e in CL: e['_t'], e['_r'], e['_t2'], e['_fits'] = assign(e, a.variant)
    n = len(CL)
    if not a.no_tsv and not a.variant:
        os.makedirs(os.path.join(ROOT, 'notes', 'threads'), exist_ok=True)
        with open(os.path.join(ROOT, 'notes', 'threads', 'china-assign.tsv'), 'w', encoding='utf-8') as w:
            w.write('id\tdate\tthread\trule\tsecond\n')
            for e in CL: w.write(f"{e['id']}\t{e['date']}\t{e['_t']}\t{e['_r']}\t{e['_t2']}\n")
    # ---- tables
    size = collections.Counter(e['_t'] for e in CL); years = sorted({e['date'][:4] for e in CL})
    by = collections.defaultdict(collections.Counter)
    for e in CL: by[e['_t']][e['date'][:4]] += 1
    order = [s for s, *_ in EPISODES] + [s for s, *_ in THREE] + [SY.NAMES[k][0] for k in ['center', 'foreign', 'army', 'economy', 'farm', 'legal', 'culture', 'org', 'front']] + ['-']
    print(f"entries: {n}" + (f"   variant: {a.variant}" if a.variant else ''))
    kinds = collections.Counter(kind_of(e['_t']) for e in CL)
    print('\n| kind | entries | share |\n|---|---:|---:|')
    for k in ('episode', 'person', 'system', 'leftover'): print(f"| {k} | {kinds[k]} | {kinds[k]/n:.1%} |")
    print('\n| thread | entries | ' + ' | '.join(years) + ' |\n|---|---:|' + '---:|' * len(years))
    for t in order: print(f"| `{t}` | {size[t]} | " + ' | '.join(str(by[t][y] or '') for y in years) + ' |')
    rules = collections.Counter(e['_r'] for e in CL)
    print('\n| rule | entries | share |\n|---|---:|---:|')
    for r, v in sorted(rules.items()): print(f"| `{r}` | {v} | {v/n:.1%} |")
    two = collections.Counter(); twok = collections.Counter()
    for e in CL:
        if e['_t'] != '-' and e['_t2'] != '-':
            two[(e['_t'], e['_t2'])] += 1; twok[(kind_of(e['_t']), kind_of(e['_t2']))] += 1
    print(f"\nfit two: {sum(two.values())} ({sum(two.values())/n:.1%})")
    print('\n| first kind | second kind | entries |\n|---|---|---:|')
    for (k1, k2), v in twok.most_common(): print(f"| {k1} | {k2} | {v} |")
    print('\n| taken by | also fits | entries |\n|---|---|---:|')
    for (t1, t2), v in two.most_common(40): print(f"| `{t1}` | `{t2}` | {v} |")
    print('\nunder 100: ' + ', '.join(f"{t} {size[t]}" for t in order if t != '-' and size[t] < 100))
    print('over 3,000: ' + ', '.join(f"{t} {size[t]}" for t in order if t != '-' and size[t] > 3000))
    left = [e for e in CL if e['_t'] == '-']
    print('\nleftovers by kind: ' + ', '.join(f"{k} {v}" for k, v in collections.Counter(e['_r'] for e in left).most_common()))
    print('leftovers by year: ' + ', '.join(f"{y} {v}" for y, v in sorted(collections.Counter(e['date'][:4] for e in left).items())))
    print('leftovers by head: ' + ', '.join(f"{k} {v}" for k, v in collections.Counter((e['_head'][0] if e['_head'] else '(no person)') for e in left).most_common(25)))
    print('leftovers, the office they would take: ' + ', '.join(f"{k} {v}" for k, v in collections.Counter(e['_t2'] for e in left).most_common()))
    NINE = ['Zhu De', 'Chen Yi', 'Yang Shangkun', 'Peng Zhen', 'Deng Xiaoping', 'Chen Yun', 'Peng Dehuai', 'Ye Jianying', 'Lin Biao']
    cols = ['episode', 'person'] + [SY.NAMES[k][0] for k in ['center', 'foreign', 'army', 'economy', 'farm', 'legal', 'culture', 'org', 'front']] + ['-']
    print('\nthe nine lesser persons of the survey, the entries each heads:\n\n| person | heads | ' + ' | '.join(x.replace('china-', '') for x in cols) + ' |\n|---|---:|' + '---:|' * len(cols))
    for p in NINE:
        sub = [e for e in CL if e['_head'] and e['_head'][0] == p]
        cnt = collections.Counter(kind_of(e['_t']) if kind_of(e['_t']) in ('episode', 'person') else e['_t'] for e in sub)
        print(f"| {p} | {len(sub)} | " + ' | '.join(str(cnt[x] or '') for x in cols) + ' |')
    from scheme import COUNTRIES
    COU = [(sl, re.compile(r)) for sl, r in COUNTRIES]
    def country(e):
        for sl, r in COU:
            if r.search(e['_plain']): return sl
        return '(no country named)'
    fz = collections.Counter(country(e) for e in CL if e['_t'] == 'china-foreign')
    zz = collections.Counter(country(e) for e in CL if e['_t'] in ('china-zhou', 'china-liu') and e['_t2'] == 'china-foreign')
    print('\nforeign business by the calendar\'s country threads (first country named):\n\n| country thread | in china-foreign | in china-zhou or china-liu, also fitting china-foreign |\n|---|---:|---:|')
    for k in sorted(set(fz) | set(zz), key=lambda k: -(fz[k] + zz[k])): print(f"| {k} | {fz[k]} | {zz[k]} |")
    # the Cultural Revolution subthread as it stands
    cr = [e for e in CL if 'india-and-china-cultural-revolution' in e['also']]
    print(f"\n`also: india-and-china-cultural-revolution` among them: {len(cr)}: " + ', '.join(f"{t} {v}" for t, v in collections.Counter(e['_t'] for e in cr).most_common()))
    oth = [e for e in ALL if e['thread'] != 'china-leadership']
    for e in oth: e['_t'], e['_r'], e['_t2'], e['_fits'] = assign(e, a.variant)
    for th in ('china',):
        sub = [e for e in oth if e['thread'] == th]
        print(f"`thread: {th}`: {len(sub)}; the episode each would fit: " + ', '.join(f"{t} {v}" for t, v in collections.Counter(e['_t'] if kind_of(e['_t']) == 'episode' else '(none)' for e in sub).most_common()))
    sub = [e for e in oth if e['thread'] != 'china']
    print(f"other threads with a China thread in `also:`: {len(sub)}: " + ', '.join(f"{t} {v}" for t, v in collections.Counter(e['thread'] for e in sub).most_common(12)))
    if a.scratch:
        os.makedirs(a.scratch, exist_ok=True)
        json.dump({'n': n, 'size': dict(size), 'by': {t: dict(v) for t, v in by.items()}, 'kinds': dict(kinds), 'rules': dict(rules),
                   'two': [[t1, t2, v] for (t1, t2), v in two.most_common()]}, open(os.path.join(a.scratch, f"measure{('-' + a.variant) if a.variant else ''}.json"), 'w'), indent=1)
        if a.sample:
            rnd = random.Random(a.seed); N, M = a.sample
            with open(os.path.join(a.scratch, 'sample.jsonl'), 'w', encoding='utf-8') as w:
                for t in order:
                    pool = sorted((e for e in CL if e['_t'] == t), key=lambda e: e['id'])
                    for e in rnd.sample(pool, min(len(pool), M if t == '-' else N)):
                        w.write(json.dumps({k: e[k] for k in ('id', 'date', 'c', 'n', 'also', 'place')} | {'t': e['_t'], 'r': e['_r'], 't2': e['_t2']}, ensure_ascii=False) + '\n')
if __name__ == '__main__':
    main()
