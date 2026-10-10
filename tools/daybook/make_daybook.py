"""The day's executive documents: every Public Papers and FRUS document, filed under its date.
# Usage: python3 tools/daybook/make_daybook.py [--cache DIR]
#   Rewrites daybook/<YYYY-MM>.yaml for the calendar's span (FROM..TO below). Needs the network;
#   the build does not. Abstracts live in daybook/abstracts.yaml, keyed by document, and are not
#   touched here, so a rerun keeps them.
#
#   Public Papers: the American Presidency Project's listing of every presidential document by date
#   (Public Papers items, executive orders, proclamations). Author: the President.
#   FRUS: the Office of the Historian's TEI files (github.com/HistoryAtState/frus), every volume of
#   the 1958-60, 1961-63 and 1964-68 subseries, microfiche supplements included. Date: the document's
#   frus:doc-dateTime-min. Editorial notes carry only their volume's span, so each is filed under
#   the date of the document before it in its volume. Author: a person where the sources give one
#   (see "authors as persons" below: the heading's sender, else the signer, else the drafter, read
#   through each volume's list of persons); else the heading's office ("Embassy in France").
#   Mechanical throughout: titles and authors are the sources' own; nothing is read or summarized.
"""
import datetime, difflib, html, os, re, sys, tempfile, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
import yaml

FROM, TO = '1961-01-01', '1966-01-10'
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'daybook')
UA = {'User-Agent': 'Mozilla/5.0 (bibliography daybook)'}
APP = 'https://www.presidency.ucsb.edu'
RAW = 'https://raw.githubusercontent.com/HistoryAtState/frus/master/volumes/'
HSG = 'https://history.state.gov/historicaldocuments/'
# The volumes, from history.state.gov's lists for the Eisenhower, Kennedy and Johnson administrations.
VOLS = (['frus1958-60v%02d' % i for i in (1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19)]
        + ['frus1958-60v07p1', 'frus1958-60v07p2', 'frus1958-60v10p1', 'frus1958-60v10p2',
           'frus1958-60v03mSupp', 'frus1958-60v05mSupp', 'frus1958-60v11mSupp', 'frus1958-60v15-16mSupp1',
           'frus1958-60v15-16mSupp2', 'frus1958-60v17-18mSupp', 'frus1958-60v19mSupp']
        + ['frus1961-63v%02d' % i for i in range(1, 26)]
        + ['frus1961-63v07-09mSupp', 'frus1961-63v10-12mSupp', 'frus1961-63v13-15mSupp',
           'frus1961-63v17-21mSupp', 'frus1961-63v22-24mSupp']
        + ['frus1964-68v%02d' % i for i in range(1, 35) if i != 29] + ['frus1964-68v29p1', 'frus1964-68v29p2'])
T = '{http://www.tei-c.org/ns/1.0}'
F = '{http://history.state.gov/frus/ns/1.0}'
XID = '{http://www.w3.org/XML/1998/namespace}id'
ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV',
         'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII',
         'XXIX', 'XXX', 'XXXI', 'XXXII', 'XXXIII', 'XXXIV']


def fetch(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                return r.read()
        except Exception:
            time.sleep(3 * (i + 1))
    raise SystemExit('failed: ' + url)


def clean(t):
    return re.sub(r'\s+', ' ', html.unescape(t or '')).strip()


# ---------------------------------------------------------------- Public Papers (APP)

def app_docs():
    f = lambda d: f'{d[5:7]}-{d[8:10]}-{d[:4]}'
    out, page = [], 0
    while True:
        q = {'from[date]': f(FROM), 'to[date]': f(TO), 'items_per_page': 100, 'page': page}
        s = fetch(APP + '/advanced-search?' + urllib.parse.urlencode(q)).decode('utf-8', 'replace')
        n = 0
        for row in re.findall(r'<tr[^>]*>(.*?)</tr>', s, re.S):
            tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)
            if len(tds) < 3:
                continue
            a = re.search(r'href="(/documents/[^"]*)"[^>]*>([^<]*)', tds[2])
            if not a:
                continue
            n += 1
            d = datetime.datetime.strptime(clean(re.sub('<[^>]+>', '', tds[0])), '%b %d, %Y').date().isoformat()
            who = clean(re.sub('<[^>]+>', '', tds[1]))
            g, _, sur = who.rpartition(' ')
            out.append({'key': 'app:' + a.group(1).rsplit('/', 1)[-1], 'src': 'ppp', 'date': d,
                        '_who': [(sur, g, '')], 'title': clean(a.group(2)).rstrip('.'),
                        'url': APP + a.group(1)})
        if n < 100:
            return out
        page += 1


# ---------------------------------------------------------------- FRUS (TEI)

def head_text(head):
    """The heading without its footnotes."""
    parts = [head.text or '']
    for c in head:
        if c.tag != T + 'note':
            parts.append(''.join(c.itertext()))
        parts.append(c.tail or '')
    return clean(''.join(parts))


STOP = re.compile(r'(Assistant|Adviser|Advisor|Representative|Mission|Delegation|Ambassador|Counselor|Envoy|Secretary|Deputy|Liaison)$')


def sender(title):
    """'Memorandum From the President's Special Assistant (Bundy) to the President' -> Bundy."""
    m = re.search(r'\b(?:[Ff]rom|[Pp]repared (?:by|in)|[Bb]y) (.+)$', title)
    if not m:
        return None
    s = m.group(1)
    cut = None
    for t in re.finditer(r' to ', s):
        left = s[:t.start()]
        if left.count('(') == left.count(')') and not STOP.search(left):
            cut = t.start()
            break
    s = s[:cut] if cut is not None else s
    s = re.sub(r',\s*(undated|[A-Z][a-z]+\.? \d{1,2}(, \d{4})?|[A-Z][a-z]+ \d{4})$', '', s)
    names = re.findall(r'\(([^()]+)\)', s)
    if names:
        return names[0]
    return re.sub(r'^the ', '', s).strip() or None


def drafter(head):
    """'Drafted by Kohler and approved ...' in the source note: the author of a memorandum of conversation."""
    for n in head.iter(T + 'note'):
        if n.get('type') == 'source':
            m = re.search(r'\b[Dd]rafted (?:by|in) (.+?)(?=(?: on [A-Z]| and (?:approved|cleared|initialed|revised)|[;.,:]|$))',
                          clean(''.join(n.itertext())))
            if m and len(m.group(1)) < 80:
                return re.sub(r'^the ', '', m.group(1).strip())
    return None


# ---------------------------------------------------------------- authors as persons
# A FRUS author is resolved to a person where the volume allows: each volume's list of persons gives
# full names, and the heading's or the signature's <persName corresp="#p_..."> points into it. In order:
#   1. persons named in the heading's "From ..." part ("Memorandum From the Director of Central
#      Intelligence (Dulles) ..." -> Allen W. Dulles);
#   2. else, where the heading names an office ("Telegram From the Mission at Berlin ..."), whoever
#      signed it (Lightner); initials and first names ("LLC", "Bob K.") resolve only through corresp;
#   3. else the drafter in the source note, else the heading's own words as before.
# Intelligence estimates go to the board the source note says concurred in them (the U.S.
# Intelligence Board from Sept. 1958; the Intelligence Advisory Committee before).
# A person shows by surname alone ("Rusk") unless another person in these volumes' lists, or a
# President in the Public Papers, has that surname; then by full name ("McGeorge Bundy",
# "William P. Bundy", "John S. D. Eisenhower", "John F. Kennedy").

RANK = (r'(?:(?:Lieutenant|Lt\.|Major|Maj\.|Brigadier|Brig\.|Vice|Rear|Air|Air Chief|Field|Fleet|Chief|Sub-?|Acting)\s+)*'
        r'(?:General|Gen\.|Colonel|Col\.|Major|Maj\.|Captain|Capt\.|Commander|Cdr\.|Admiral|Adm\.|Marshal|Lieutenant|'
        r'Lt\.|Sergeant|Ensign|Commodore)|Dr\.|Sir|Lord|Lady|Dame|Prince|Princess|Mr\.|Mrs\.|Miss|Ambassador|Senator|'
        r'Judge|Father|Monsignor|Bishop|Archbishop|Cardinal|Sheikh|Shaikh|Emir|Professor|Prof\.|Rabbi|Reverend|Rev\.')
SUFFIX = re.compile(r',?\s*\b(Jr\.?|Sr\.?|II|III|IV)$')


def parse_name(n):
    """'Eisenhower, Major John S.D.' -> ('Eisenhower', 'John S. D.', ''); 'Nolting, Frederick E., Jr.' ->
    ('Nolting', 'Frederick E.', 'Jr.'); 'Buu Hoi' -> ('Buu Hoi', '', '')."""
    n = clean(n).strip(' ,')
    if ',' not in n:
        return n, '', ''
    sur, rest = (x.strip() for x in n.split(',', 1))
    suf = ''
    m = SUFFIX.search(rest)
    if m:
        suf = m.group(1).rstrip('.') + '.' if m.group(1).startswith(('J', 'S')) else m.group(1)
        rest = rest[:m.start()].strip(' ,')
    rest = re.sub(r'^(?:(?:' + RANK + r')\s*)+', '', rest).strip(' ,')
    rest = re.sub(r'\.(?=[A-Z])', '. ', rest)
    if not rest or not re.match(r'[A-Z]', rest):  # 'Souphanouvong, Prince'; a role in place of a given name
        rest = ''
    return sur, rest, suf


def strip_number(title, n):
    """A heading less its document number: '499. The Ambassador ...'; the 1952-54 volumes' 'No. 499The Ambassador
    ...'; the microfiche supplements' '278J. Memorandum ...' for document 278j."""
    if not n:
        return title
    return re.sub(r'^(?:No\.\s*)?' + re.escape(str(n)) + r'\.?\s*', '', title, flags=re.I)


def first_word(given):
    """The given name a person goes by: 'Allen W.' -> allen; 'C. Douglas' -> douglas (an initial before a name)."""
    w = given.split()
    if len(w) > 1 and re.fullmatch(r'[A-Z]\.', w[0]) and len(re.sub(r'\W', '', w[1])) > 1:
        w = w[1:]
    return re.sub(r'\W', '', w[0]).lower() if w else ''


def tokens(given):
    return [t for t in re.sub(r'\.', ' ', given).split() if t]


def same_given(a, b):
    """Could two given names be one person's? Their initials agree, position by position, and where both
    spell a name out the names agree up to a slip of spelling: 'E. Allan' ~ 'Edwin A.' ~ 'Edwin Allan';
    'John F.' !~ 'Joseph P.'. One may be shorter ('John' ~ 'John F.')."""
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return False
    for x, y in zip(ta, tb):
        if x[0].lower() != y[0].lower():
            return False
        if len(x) > 1 and len(y) > 1 and difflib.SequenceMatcher(None, x.lower(), y.lower()).ratio() < 0.75:
            return False
    return True


class Names:
    """Every person in the volumes' lists, for telling apart those who share a surname: under each
    surname, the given names grouped into persons by same_given()."""
    def __init__(self):
        self.forms = {}        # surname (lower) -> {(given, suffix): count}
        self.case = {}         # surname as written
        self.roles = {}        # (surname, given, suffix) -> the offices the lists give
        self._groups = {}

    def add(self, sur, given, suf='', role=''):
        k = sur.lower()
        if role:
            self.roles[(k, given, suf)] = self.roles.get((k, given, suf), '') + ' ' + role
        self.case.setdefault(k, sur)
        f = self.forms.setdefault(k, {})
        f[(given, suf)] = f.get((given, suf), 0) + 1
        self._groups.pop(k, None)

    def groups(self, sur):
        """[[(given, suffix), ...] per person], the most common form first."""
        k = sur.lower()
        if k not in self._groups:
            f = self.forms.get(k, {})
            out = []
            for g in sorted(f, key=lambda g: (-f[g], g)):
                if not g[0]:
                    continue
                home = next((grp for grp in out if all(same_given(g[0], h[0]) for h in grp)), None)
                (home.append(g) if home is not None else out.append([g]))
            self._groups[k] = out
        return self._groups[k]

    def person(self, sur, given):
        """The group this given name belongs to, if one."""
        hits = [grp for grp in self.groups(sur) if given and all(same_given(given, h[0]) for h in grp)]
        return hits[0] if len(hits) == 1 else None

    def people(self, sur):
        return max(1, len(self.groups(sur)))

    def full(self, sur, given, suf=''):
        """'E. Allan Lightner, Jr.': the person's most common given form and suffix in the lists."""
        grp = self.person(sur, given)
        if grp:
            f = self.forms[sur.lower()]
            given = max((h[0] for h in grp), key=lambda x: (sum(f[h] for h in grp if h[0] == x), len(x)))
            sufs = [h[1] for h in grp if h[1]]
            suf = max(set(sufs), key=sufs.count) if sufs else suf
        return f'{given} {self.case.get(sur.lower(), sur)}' + (f', {suf}' if suf else '')

    def lookup(self, sur, words, hint=''):
        """A surname that no volume's own list resolved: the one person of that name in all the lists,
        the one whose given name is among `words`, or the one whose listed offices fit `hint` best."""
        grps = self.groups(sur)
        if len(grps) > 1:
            grps = [g for g in grps if any(first_word(h[0]) in words for h in g)] or grps
        if len(grps) > 1 and hint:
            fit = [office_fit(hint, ' '.join(self.roles.get((sur.lower(),) + h, '') for h in g)) for g in grps]
            if max(fit) and fit.count(max(fit)) == 1:
                grps = [grps[fit.index(max(fit))]]
        return (self.case[sur.lower()], grps[0][0][0], grps[0][0][1]) if len(grps) == 1 else None


def display(p, names):
    """A person (surname, given, suffix) as shown: the surname, or the full name where it is shared."""
    sur, given, suf = p
    if not given or names.people(sur) <= 1:
        return sur
    return names.full(sur, given, suf)


# Names the lists misprint: the 1961-68 volumes give Ambassador Stevenson (d. July 14, 1965) as "III", his son's
# suffix, as often as "II" (as tools/lives/frus_names.py's ERRATA); the son held no office FRUS records before 1969.
ERRATA = {('Stevenson', 'Adlai E.', 'III'): ('Stevenson', 'Adlai E.', 'II')}


def persons(root):
    """The volume's list: {xml:id: (surname, given, suffix)}, and {xml:id: the office it gives}."""
    P, roles = {}, {}
    for item in root.iter(T + 'item'):
        for pn in item.iter(T + 'persName'):
            if pn.get(XID):
                P[pn.get(XID)] = parse_name(''.join(pn.itertext()))
                P[pn.get(XID)] = ERRATA.get(P[pn.get(XID)], P[pn.get(XID)])
                roles[pn.get(XID)] = clean(''.join(item.itertext()))
    for pn in root.iter(T + 'persName'):
        if pn.get(XID) and pn.get(XID) not in P:
            P[pn.get(XID)] = parse_name(''.join(pn.itertext()))
            P[pn.get(XID)] = ERRATA.get(P[pn.get(XID)], P[pn.get(XID)])
    return P, roles


SMALL = {'the', 'of', 'for', 'and', 'to', 'in', 'on', 'at', 'from', 'with', 'president’s', "president's"}


def office_fit(office, role):
    a = {w.lower().strip('(),.’\'') for w in office.split()} - SMALL
    b = {w.lower().strip('(),.’\'') for w in role.split()} - SMALL
    return len({w for w in a if len(w) > 3} & b)


def text_of(e):
    """An element's text without its footnotes."""
    parts = [e.text or '']
    for c in e:
        if c.tag != T + 'note':
            parts.append(text_of(c))
        parts.append(c.tail or '')
    return clean(''.join(parts))


def possessive(pn):
    """'President Eisenhower’s Special Assistant': the name names someone else's office."""
    return (pn.tail or '').startswith(('’s', "'s", 'ʼs'))


def resolve(pn, P, by_sur, hint=''):
    """A <persName> to a person: by its corresp, else by a surname the volume's list gives one person."""
    ref = (pn.get('corresp') or '').lstrip('#')
    if ref in P:
        return P[ref]
    return by_word(text_of(pn), by_sur, hint)


NAMES = None   # every volume's list (Names), read before any document is resolved


def by_word(t, by_sur, hint=''):
    """A surname in the text that the volume's list gives one person, or one whose given name is also
    there, or (with a `hint`, the heading's sender words) the one whose listed office fits it best;
    failing the volume, all the volumes' lists."""
    words = {x.lower().rstrip('.') for x in t.split()}
    for w in reversed(re.findall(r"[A-Z][\w'’-]{2,}", t)):
        c = list(dict.fromkeys(by_sur.get(w.lower(), ())))
        if len(c) > 1:
            c = [p for p in c if first_word(p[1]) in words] or c
        if len(c) > 1 and hint:
            fit = {p: office_fit(hint, by_sur.get('\0role', {}).get(p, '')) for p in c}
            top = max(fit.values())
            if top and list(fit.values()).count(top) == 1:
                c = [p for p in c if fit[p] == top]
        if len(c) == 1:
            return c[0]
        if not c and NAMES is not None:
            p = NAMES.lookup(w, words, hint)
            if p:
                return p
    return None


OFFICE = re.compile(r'\b(Secretary|Director|President|Vice President|Ambassador|Chairman|Attorney General|Minister|'
                    r'Chancellor|Governor|Senator|Representative|Counselor|Adviser|Advisor|Assistant|Administrator|'
                    r'Chief|Commander|Deputy|Under|Acting|Special|Prime|King|Shah|Premier|Chargé|Consul|Admiral|General|Colonel)\b')


BODY = {'Agency', 'Department', 'Embassy', 'Legation', 'Consulate', 'Committee', 'Board', 'Staff', 'Office', 'Council',
        'Mission', 'Delegation', 'Group', 'Station', 'Bureau', 'Headquarters', 'Command', 'Service', 'Services',
        'Administration', 'Commission', 'Center', 'Centre', 'Government', 'Ministry', 'Chiefs', 'House', 'Institute',
        'University', 'Corporation', 'Company', 'Section', 'Division', 'Branch', 'Team', 'Force', 'Forces', 'Library',
        'Secretariat', 'Members', 'Representatives', 'Personnel', 'Officials', 'Officers', 'Army', 'Navy', 'Air',
        'Intelligence', 'Survey', 'Task', 'Party', 'Program', 'Programs', 'Conference', 'Panel', 'Unit', 'Directorate'}


def person_in(a, by_sur):
    """'Secretary of Defense McNamara', 'Michael V. Forrestal of the National Security Council Staff':
    the person; an office alone ('Embassy in France') is left as it is."""
    core = re.split(r',| of the | of (?=[A-Z][a-z]+ [A-Z])', a)[0].strip()
    core = re.sub(r'^(?:(?:' + RANK + r')\s*)+', '', core)
    toks = core.split()
    if not toks or not re.match(r"[A-Z][\w'’-]{2,}$", toks[-1]):
        return None
    namelike = (all(re.match(r"[A-Z]", x) for x in toks) and len(toks) <= 4
                and not any(x.strip(',.') in BODY for x in toks))
    if not (namelike or OFFICE.search(core)):
        return None
    p = by_word(toks[-1] if not namelike else core, by_sur, a)
    if p is None and namelike and len(toks) > 1:
        p = (toks[-1], re.sub(r'\.(?=[A-Z])', '. ', ' '.join(toks[:-1])), '')
    return p


ESTIMATE = re.compile(r'National Intelligence Estimate')
BOARD = [(re.compile(r'(?:United States|U\. ?S\.) Intelligence Board|USIB'), 'United States Intelligence Board (USIB)'),
         (re.compile(r'Intelligence Advisory Committee'), 'Intelligence Advisory Committee (IAC)')]


def head_persons(head, title, fp):
    """The heading's <persName> elements that begin inside its sender words `fp` (footnotes aside)."""
    full = head_text(head)
    i = title.find(fp)
    if i < 0:
        return []
    lo = len(full) - len(title) + i
    hi = lo + len(fp)
    out, acc = [], ['']

    def walk(e):
        if e.tag == T + 'persName':
            out.append((len(re.sub(r'\s+', ' ', acc[0]).lstrip()), e))
        acc[0] += e.text or ''
        for c in e:
            if c.tag != T + 'note':
                walk(c)
            acc[0] += c.tail or ''
    walk(head)
    return [e for at, e in out if lo - 1 <= at < hi]


def from_part(title):
    """The heading's sender words, as sender() cuts them, before the name in parentheses is taken."""
    m = re.search(r'\b(?:[Ff]rom|[Pp]repared (?:by|in)|[Bb]y) (.+)$', title)
    if not m:
        return ''
    s = m.group(1)
    for t in re.finditer(r' to ', s):
        left = s[:t.start()]
        if left.count('(') == left.count(')') and not STOP.search(left):
            return left
    return s


def authors(d, head, title, P, roles, by_sur):
    """[person or plain text] for a FRUS document, by the order above."""
    note = ' '.join(clean(''.join(n.itertext())) for n in head.iter(T + 'note') if n.get('type') == 'source')
    if ESTIMATE.search(title):
        for pat, who in BOARD:
            if pat.search(note):
                return [who]
    fp = from_part(title)
    found = []
    signed = [text_of(pn) for c in d.iter(T + 'closer') for s in c.iter(T + 'signed')
              for pn in (list(s.iter(T + 'persName')) or [s])]
    if fp:
        typed = [pn for pn in head.iter(T + 'persName') if pn.get('type') == 'from']
        for pn in typed or head_persons(head, title, fp):
            if not text_of(pn) or possessive(pn):
                continue
            ref = (pn.get('corresp') or '').lstrip('#')
            if ref in P:
                # the markup sometimes points to the wrong one of two namesakes: the office in the
                # heading ("the Attorney General (Kennedy)") decides between them
                same = [i for i, q in P.items() if q[0] == P[ref][0] and i != ref]
                office = fp[:fp.find(text_of(pn))] if text_of(pn) in fp else fp
                if same and office.strip():
                    best = max(same, key=lambda i: office_fit(office, roles.get(i, '')))
                    if office_fit(office, roles.get(best, '')) > office_fit(office, roles.get(ref, '')):
                        ref = best
                p = P[ref]
            else:
                p = resolve(pn, P, by_sur, fp)
            # a signature naming another listed person of the same surname is the document's own word
            for t in signed:
                w = t.split()
                if p and NAMES is not None and len(w) > 1 and w[-1] == p[0]:
                    other = NAMES.person(p[0], ' '.join(w[:-1]))
                    if other and other is not NAMES.person(p[0], p[1]):
                        p = (p[0], other[0][0], other[0][1])
            if p and p not in found:
                found.append(p)
        if not found:
            for nm in re.findall(r'\(([^()]+)\)', fp):
                p = by_word(nm, by_sur)
                if p and p not in found:
                    found.append(p)
    if found:
        return found
    for c in d.iter(T + 'closer'):
        for s in c.iter(T + 'signed'):
            pns = list(s.iter(T + 'persName')) or [s]
            for pn in pns:
                p = resolve(pn, P, by_sur, fp) if pn is not s else by_word(text_of(s), by_sur, fp)
                if p and p not in found:
                    found.append(p)
    if found:
        return found
    dr = drafter(head)
    if dr and not fp:
        # a memorandum of conversation or for the record: its drafter(s), by name
        note_el = next((n for n in head.iter(T + 'note') if n.get('type') == 'source'), None)
        tagged = [pn for pn in note_el.iter(T + 'persName') if not possessive(pn)] if note_el is not None else []
        for part in re.split(r',\s*(?:and\s+)?|\s+and\s+', dr):
            p = next((resolve(pn, P, by_sur) for pn in tagged if text_of(pn) and text_of(pn) in part), None)
            p = p or person_in(part, by_sur)
            if not p and re.fullmatch(r"(?:[A-Z][\w.'’-]*\s?){1,4}", part.strip()):
                p = part.strip()              # a name no list gives: as the note writes it
            if p and p not in found:
                found.append(p)
        if not found and OFFICE.search(dr):
            m = re.search(re.escape(dr) + r",\s*((?:[A-Z][\w.'’-]*\s){1,3}[A-Z][\w'’-]+)", note)
            p = m and person_in(m.group(1), by_sur)
            if p:
                found.append(p)
        if found:
            return found
    a = sender(title)
    if a and not a[0].isupper():           # 'Notes from transcripts of JCS meetings': no sender
        a = None
    if a and f'({a})' in title:            # a name in parentheses the markup did not tag
        return [by_word(a, by_sur, fp) or a]
    if a:
        return [person_in(a, by_sur) or a]
    if dr:
        return [by_word(dr, by_sur) or dr] if len(dr.split()) <= 3 else [dr]
    return []


def day_of(stamp, is_max=False):
    """Calendar date of a frus:doc-dateTime value. Some ranges were set in another zone and read
    23:00 the day before (min) or 22:59 (max); those are moved back to the intended day."""
    d = datetime.date.fromisoformat(stamp[:10])
    if not is_max and stamp[11:16] == '23:00':
        d += datetime.timedelta(days=1)
    return d


def cite(vol):
    m = re.match(r'frus(\d{4})-(\d\d)(?:v(\d\d)(?:-(\d\d))?)?(p\d)?(mSupp\d?)?', vol)
    years = f'{m.group(1)}–{m.group(2)}'
    v = ROMAN[int(m.group(3))] + (('–' + ROMAN[int(m.group(4))]) if m.group(4) else '')
    part = f', pt. {m.group(5)[1:]}' if m.group(5) else ''
    supp = ', microfiche supp.' if m.group(6) else ''
    return f'FRUS {years}, {v}{part}{supp}'


def frus_docs(cache, names):
    global NAMES
    os.makedirs(cache, exist_ok=True)
    out = []
    for vol in VOLS:                      # first, every volume's list of persons
        path = os.path.join(cache, vol + '.xml')
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(RAW + vol + '.xml'))
        P0, R0 = persons(ET.parse(path).getroot())
        for i, p in P0.items():
            names.add(*p, role=R0.get(i, ''))
    NAMES = names
    for vol in VOLS:
        path = os.path.join(cache, vol + '.xml')
        if not os.path.exists(path):
            open(path, 'wb').write(fetch(RAW + vol + '.xml'))
        root = ET.parse(path).getroot()
        P, roles = persons(root)
        by_sur = {'\0role': {P[i]: roles.get(i, '') for i in P}}
        for p in dict.fromkeys(P.values()):
            for k in {p[0].lower(), p[0].split()[-1].lower()}:
                by_sur.setdefault(k, []).append(p)
        vt = clean(''.join(root.find(f'.//{T}titleStmt/{T}title[@type="subseries"]').itertext())
                   if root.find(f'.//{T}titleStmt/{T}title[@type="subseries"]') is not None else '')
        vsub = root.find(f'.//{T}titleStmt/{T}title[@type="volume"]')
        vt = clean(''.join(vsub.itertext())) if vsub is not None else vt
        prev = None
        for d in root.iter(T + 'div'):
            if d.get('type') != 'document':
                continue
            head = d.find(T + 'head')
            if head is None:
                continue
            title = head_text(head)
            n = d.get('n')
            title = strip_number(title, n)
            ed = d.get('subtype') == 'editorial-note'
            lo, hi = d.get(F + 'doc-dateTime-min'), d.get(F + 'doc-dateTime-max')
            if ed or not lo:
                if prev is None:
                    continue
                start, end, placed = prev, prev, True
            else:
                start, end, placed = day_of(lo), day_of(hi, True) if hi else day_of(lo), False
                if end < start:
                    end = start
                prev = start
            if not (FROM <= start.isoformat() <= TO):
                continue
            doc = {'key': f'frus:{vol}/{d.get(XID)}', 'src': 'frus', 'date': start.isoformat(),
                   'title': title, 'url': f'{HSG}{vol}/{d.get(XID)}',
                   'cite': f'{cite(vol)}, doc. {n}', 'vol': vt}
            if end != start:
                doc['until'] = end.isoformat()
            if placed:
                doc['placed'] = True
            if lo and not ed and lo[11:16] not in ('00:00', '23:00'):
                doc['time'] = lo[11:16]
            if not ed:
                doc['_who'] = authors(d, head, title, P, roles, by_sur)
            out.append(doc)
    return out


def main():
    cache = sys.argv[sys.argv.index('--cache') + 1] if '--cache' in sys.argv else os.path.join(tempfile.gettempdir(), 'frus-tei')
    names = Names()
    docs = app_docs()
    for x in docs:
        names.add(*x['_who'][0])
    docs += frus_docs(cache, names)
    for x in docs:
        who = [display(p, names) if isinstance(p, tuple) else p for p in x.pop('_who', [])]
        if who:
            x['author'] = who[0] if len(who) == 1 else ', '.join(who[:-1]) + ' and ' + who[-1]
        x.update({k: x.pop(k) for k in ('title', 'url', 'cite', 'vol', 'until', 'placed', 'time') if k in x})
    order = {'ppp': 0, 'frus': 1}
    vol_i = {v: i for i, v in enumerate(VOLS)}

    def frus_pos(x):
        vol, d = x['key'][5:].split('/')
        return (vol_i[vol], int(re.sub(r'\D', '', d) or 0))
    # The President's in APP's order; FRUS by volume, then the volume's own order.
    docs.sort(key=lambda x: (x['date'], order[x['src']]) + (frus_pos(x) if x['src'] == 'frus' else (0, 0)))
    months = {}
    for x in docs:
        months.setdefault(x['date'][:7], []).append(x)
    os.makedirs(OUT, exist_ok=True)
    head = ('# Generated by tools/daybook/make_daybook.py. Edit the script, not this file.\n'
            '# One row per document: key, src (ppp|frus), date, author, title, url; FRUS adds cite, vol (the\n'
            '# volume title), until (last day of a dated range), time, placed (an editorial note filed by its\n'
            '# place in the volume). Abstracts: daybook/abstracts.yaml.\n')
    for m, rows in sorted(months.items()):
        body = yaml.safe_dump({'month': m, 'docs': rows}, sort_keys=False, allow_unicode=True, width=200)
        open(os.path.join(OUT, f'{m}.yaml'), 'w', encoding='utf-8').write(head + body)
        print(m, len(rows))
    print('total', len(docs), 'ppp', sum(x['src'] == 'ppp' for x in docs), 'frus', sum(x['src'] == 'frus' for x in docs))


if __name__ == '__main__':
    main()
