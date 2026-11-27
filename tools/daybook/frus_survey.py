"""The FRUS survey's sorting step (ruling 71; notes/proposals/frus-survey.md): every FRUS document in the daybook
that no calendar entry cites, sorted by what the calendar already holds on its days. It reads nothing of a document
but its heading and its date.

    python3 tools/daybook/frus_survey.py      writes notes/proposals/frus-survey.tsv and prints the counts by volume

What is read: the daybook's FRUS rows (daybook/<YYYY-MM>.yaml: key, date, until, author, title, placed); the head of
each document in sources/frus-text/ (its number and title, and the lists of persons under PARTICIPANTS, PRESENT, TO,
FROM and the like, never the subject or the body); the persons each document names, by volume and number, in
sources/frus-names/<letter>.json, joined to the series' name entries by tools/bib/lives.py (everyone, and its
frus-alias, from sources/frus-joins.yaml); the calendar's entries (lists/cal/*.yaml) and their threads
(lists/cal/th.yaml).

STYLE
 1. Cited: a calendar entry links the document's address at history.state.gov (historicaldocuments/<volume>/<id>),
    anywhere in lists/cal/*.yaml. A cited document is left out of the survey.
 2. Routine, sort (c): an editorial note (its title, or the daybook's `placed`), or a covering note or transmittal by
    its heading (R18, notes/briefs/reader.md): "transmitting", "covering", "enclosing", "with attached", "letter of
    transmittal". Judged before any match.
 3. The document's persons: those its sources list as named in it or as its sender (sources/frus-names), kept only
    where the heading writes one of the person's surnames, whole and capitalized (the title, the author, the lists of
    persons in the head). The sitting President (Eisenhower to Jan. 20, 1961; Kennedy to Nov. 22, 1963; then
    Johnson) is never taken by his bare surname ('(Johnson)' is U. Alexis Johnson): he is a person of the document
    where the heading says "the President" (not "the President's", "the President of"; not "Vice President") or
    "President Kennedy" and the like.
 4. The days: the document's date, the day before and the day after; a document dated over a range (`until`) of a
    week or less, its range and a day either side. A calendar entry falls on them where its own days (its date to the
    last day its `when` gives: tools/bib/daybook.py, end_of) meet them. Month-dated entries never do.
 5. Sort (a), by persons: an entry of those days tags (`name:`) one of the document's persons, other than the sitting
    President. The President alone counts only where the entry is also in the volume's threads (STYLE 6): he is
    tagged on all his own acts, most of them on other matters.
 6. Sort (a), by thread: where no entry matches by persons and the heading names none of the persons, an entry of
    those days whose thread or `also` falls in a thread the volume belongs to (THREADS; a subthread counts as its
    top thread). A document whose heading names persons, none of them in an entry of those days, is not matched by
    thread: it goes to (b).
 7. Sort (b): the rest, the likely missing entries.
 8. THREADS was made by hand from each volume's title in the daybook (`vol`), against the threads' names in
    lists/cal/th.yaml, and where a country has no thread of its own, the thread its entries are filed under (./bib
    find, Nov. 27, 2026: Thailand's under Laos, Cambodia's under Vietnam, Burma's, Taiwan's and Mongolia's under
    China's, Eastern Europe's under the Soviet Union's). A volume of several subjects takes each subject's thread.
 9. The table: one row a document, tab-separated, with a header row: key, volume (as FRUS is cited: "FRUS 1961–63,
    II"), number, date, heading (the daybook's title), sort (a, b, c), by (persons, thread, or the routine reason),
    entries (the matched ids, space-separated; by persons, the persons' keys after them in brackets).
"""
import datetime
import glob
import json
import lzma
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))

# STYLE 8: each volume's threads, from its title.
THREADS = {
    "frus1958-60v01": ["vietnam"],                                            # Vietnam
    "frus1958-60v02": ["united-nations"],                                     # United Nations and General International Matters
    "frus1958-60v03": ["defense", "testing"],                                 # National Security Policy; Arms Control and Disarmament
    "frus1958-60v03mSupp": ["defense", "testing"],
    "frus1958-60v04": ["economy", "trade", "foreign-aid"],                    # Foreign Economic Policy
    "frus1958-60v05": ["latin-america"],                                      # American Republics
    "frus1958-60v05mSupp": ["latin-america"],
    "frus1958-60v06": ["cuba"],                                               # Cuba
    "frus1958-60v07p1": ["europe-and-the-alliance", "european-community", "canada"],  # Western European Integration and Security, Canada
    "frus1958-60v07p2": ["europe-and-the-alliance"],                          # Western Europe
    "frus1958-60v09": ["berlin-and-vienna", "europe-and-the-alliance"],       # Berlin Crisis, 1959-1960; Germany; Austria
    "frus1958-60v10p1": ["soviet-union", "comecon", "cyprus"],                # Eastern Europe Region; Soviet Union; Cyprus
    "frus1958-60v10p2": ["soviet-union", "comecon", "europe-and-the-alliance"],  # Eastern Europe; Finland; Greece; Turkey
    "frus1958-60v11": ["middle-east"],                                        # Lebanon and Jordan
    "frus1958-60v12": ["middle-east", "oil"],                                 # Near East Region; Iraq; Iran; Arabian Peninsula
    "frus1958-60v13": ["middle-east", "africa"],                              # Arab-Israeli Dispute; United Arab Republic; North Africa
    "frus1958-60v14": ["africa", "congo"],                                    # Africa
    "frus1958-60v15": ["south-asia", "laos", "indonesia", "china"],           # South and Southeast Asia
    "frus1958-60v16": ["laos", "vietnam"],                                    # East Asia-Pacific Region; Cambodia; Laos
    "frus1958-60v17": ["indonesia"],                                          # Indonesia
    "frus1958-60v18": ["japan", "korea"],                                     # Japan; Korea
    "frus1958-60v19": ["china"],                                              # China
    "frus1961-63v01": ["vietnam"],                                            # Vietnam, 1961
    "frus1961-63v02": ["vietnam"],
    "frus1961-63v03": ["vietnam"],
    "frus1961-63v04": ["vietnam"],
    "frus1961-63v05": ["soviet-union"],                                       # Soviet Union
    "frus1961-63v06": ["soviet-union"],                                       # Kennedy-Khrushchev Exchanges
    "frus1961-63v07": ["testing"],                                            # Arms Control and Disarmament
    "frus1961-63v07-09mSupp": ["testing", "defense", "economy", "trade", "foreign-aid"],
    "frus1961-63v08": ["defense"],                                            # National Security Policy
    "frus1961-63v09": ["economy", "trade", "foreign-aid"],                    # Foreign Economic Policy
    "frus1961-63v10": ["cuba"],                                               # Cuba, January 1961-September 1962
    "frus1961-63v10-12mSupp": ["latin-america", "cuba", "missile-crisis"],    # American Republics; Cuba; the missile crisis
    "frus1961-63v11": ["missile-crisis", "cuba"],                             # Cuban Missile Crisis and Aftermath
    "frus1961-63v12": ["latin-america"],                                      # American Republics
    "frus1961-63v13": ["europe-and-the-alliance", "european-community", "canada"],  # Western Europe and Canada
    "frus1961-63v14": ["berlin-and-vienna"],                                  # Berlin Crisis, 1961-1962
    "frus1961-63v15": ["berlin-and-vienna"],                                  # Berlin Crisis, 1962-1963
    "frus1961-63v16": ["soviet-union", "comecon", "cyprus", "europe-and-the-alliance"],  # Eastern Europe; Cyprus; Greece; Turkey
    "frus1961-63v17": ["middle-east"],                                        # Near East, 1961-1962
    "frus1961-63v18": ["middle-east"],                                        # Near East, 1962-1963
    "frus1961-63v19": ["south-asia"],                                         # South Asia
    "frus1961-63v20": ["congo"],                                              # Congo Crisis
    "frus1961-63v21": ["africa"],                                             # Africa
    "frus1961-63v22": ["china", "korea", "japan"],                            # Northeast Asia
    "frus1961-63v23": ["indonesia", "singapore", "laos", "vietnam", "china"],  # Southeast Asia
    "frus1961-63v24": ["laos"],                                               # Laos Crisis
    "frus1961-63v25": ["united-nations", "transition-and-staff", "space"],    # Organization; Information Policy; UN; Scientific Matters
    "frus1964-68v01": ["vietnam"],                                            # Vietnam, 1964
    "frus1964-68v02": ["vietnam"],
    "frus1964-68v03": ["vietnam"],
    "frus1964-68v04": ["vietnam"],
    "frus1964-68v05": ["vietnam"],
    "frus1964-68v06": ["vietnam"],
    "frus1964-68v07": ["vietnam"],
    "frus1964-68v08": ["economy", "trade"],                                   # International Monetary and Trade Policy
    "frus1964-68v09": ["foreign-aid", "trade"],                               # International Development and Economic Defense Policy; Commodities
    "frus1964-68v10": ["defense"],                                            # National Security Policy
    "frus1964-68v11": ["testing"],                                            # Arms Control and Disarmament
    "frus1964-68v12": ["europe-and-the-alliance"],                            # Western Europe
    "frus1964-68v13": ["europe-and-the-alliance", "european-community"],      # Western Europe Region
    "frus1964-68v14": ["soviet-union"],                                       # Soviet Union
    "frus1964-68v15": ["berlin-and-vienna", "europe-and-the-alliance"],       # Germany and Berlin
    "frus1964-68v16": ["cyprus", "europe-and-the-alliance"],                  # Cyprus; Greece; Turkey
    "frus1964-68v17": ["soviet-union", "comecon"],                            # Eastern Europe
    "frus1964-68v18": ["middle-east"],                                        # Arab-Israeli Dispute, 1964-1967
    "frus1964-68v19": ["middle-east"],                                        # Arab-Israeli Crisis and War, 1967
    "frus1964-68v20": ["middle-east"],                                        # Arab-Israeli Dispute, 1967-1968
    "frus1964-68v21": ["middle-east", "oil"],                                 # Near East Region; Arabian Peninsula
    "frus1964-68v22": ["middle-east"],                                        # Iran
    "frus1964-68v23": ["congo"],                                              # Congo, 1960-1968
    "frus1964-68v24": ["africa"],                                             # Africa
    "frus1964-68v25": ["south-asia"],                                         # South Asia
    "frus1964-68v26": ["indonesia", "singapore"],                             # Indonesia; Malaysia-Singapore; Philippines
    "frus1964-68v27": ["laos", "vietnam", "china"],                           # Mainland Southeast Asia; Regional Affairs
    "frus1964-68v28": ["laos"],                                               # Laos
    "frus1964-68v29p1": ["korea"],                                            # Korea
    "frus1964-68v29p2": ["japan"],                                            # Japan
    "frus1964-68v30": ["china"],                                              # China
    "frus1964-68v31": ["latin-america"],                                      # South and Central America; Mexico
    "frus1964-68v32": ["latin-america", "cuba"],                              # Dominican Republic; Cuba; Haiti; Guyana
    "frus1964-68v33": ["united-nations", "transition-and-staff"],             # Organization and Management of Foreign Policy; UN
    "frus1964-68v34": ["oil", "space"],                                       # Energy Diplomacy and Global Issues
}

# STYLE 3: the sitting President, by the day his term began
PRESIDENTS = [("1953-01-20", "eisenhower-dwight-d", "Eisenhower"), ("1961-01-20", "kennedy-john-f", "Kennedy"),
              ("1963-11-22", "johnson-lyndon-b", "Johnson"), ("1969-01-20", "nixon-richard-m", "Nixon")]

LINK = re.compile(r"history\.state\.gov/historicaldocuments/(frus[0-9A-Za-z-]+)/([0-9A-Za-z_]+)")
KEY = re.compile(r"frus:(frus[^/]+)/(.+)$")
ROUTINE = re.compile(r"(?i)\b(?:transmitting|covering|enclosing|with attached|letter of transmittal|transmittal)\b")
# the head's lists of persons, by their labels (STYLE 3); any other list (the subject, the references) is not read
PERSON_LISTS = re.compile(r"(?i)^\s*(?:\d+\.\s*)?(?:participants|present|others present|also present|in attendance|"
                          r"attending|attendees|to|from|memorandum (?:for|to)|through|for (?:the )?[A-Z])")
_DSTROKE = str.maketrans({"Đ": "D", "đ": "d", "’": "'", "ʼ": "'", "‘": "'", "Ø": "O", "ø": "o", "Ł": "L", "ł": "l"})


# ---------------------------------------------------------------- pure parts (tests/unit/test_frus_survey.py)

def plain(t):
    """Marks off, the case kept: 'Ngô Đình Diệm' -> 'Ngo Dinh Diem'."""
    t = unicodedata.normalize("NFKD", (t or "").translate(_DSTROKE))
    return "".join(c for c in t if not unicodedata.combining(c))


def words(t):
    """The words of a text, marks off, case kept, apostrophes and hyphens split."""
    return re.findall(r"[A-Za-z]+", plain(t))


def routine(title, placed=False):
    """STYLE 2: the reason a document is routine, or None."""
    if placed or re.search(r"(?i)\beditorial note\b", title or ""):
        return "editorial note"
    if ROUTINE.search(title or ""):
        return "transmittal"
    return None


def head_text(html):
    """STYLE 3: the document's head as text: its title and the lists of persons under it (PARTICIPANTS, PRESENT,
    TO ...), not the subject, the references or the body. The head ends at the first paragraph of the body."""
    html = re.sub(r"<sup\b.*?</sup>", "", html or "", flags=re.S)
    out = []
    m = re.search(r"<h3\b[^>]*>(.*?)</h3>", html, re.S)
    if m:
        out.append(m.group(1))
    pos = m.end() if m else 0
    label = None
    for t in re.finditer(r"<(/?)(p|ul|li|div)\b([^>]*)>", html[pos:]):
        close, tag, attrs = t.group(1), t.group(2), t.group(3)
        if close:
            continue
        if tag == "p":
            cls = re.search(r'class="([^"]*)"', attrs)
            cls = cls.group(1) if cls else ""
            if cls == "lh":
                end = html.find("</p>", pos + t.end())
                label = re.sub(r"<[^>]+>", "", html[pos + t.end():end])
                continue
            if cls.startswith("dl"):
                continue
            break                                 # the body's first paragraph
        if tag == "ul" and "tl" in attrs and "subject" not in attrs and "references" not in attrs:
            if label is None or not PERSON_LISTS.match(label):
                continue                          # a list with no label over it is the body's
            body = _balanced(html, pos + t.start())
            out.append(body)
    text = " ".join(re.sub(r"<[^>]+>", " ", x) for x in out)
    return re.sub(r"\s+", " ", text).strip()


def _balanced(html, start):
    """The <ul> that opens at start, to its own </ul>."""
    depth = 0
    for m in re.finditer(r"<(/?)ul\b[^>]*>", html[start:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return html[start:start + m.end()]
    return html[start:]


def president_on(day):
    """(key, surname) of the sitting President on an ISO day."""
    cur = PRESIDENTS[0]
    for p in PRESIDENTS:
        if day >= p[0]:
            cur = p
    return cur[1], cur[2]


PRES_RE = re.compile(r"(?<!Vice )(?<!Vice-)\b(?:[Tt]he President\b(?!['’ʼ]s|ial| of)|President ([A-Z][a-z]+))")


def names_president(head, surname):
    """STYLE 3: the heading names the sitting President."""
    for m in PRES_RE.finditer(head):
        if m.group(1) is None or m.group(1) == surname:
            return True
    return False


def has_form(head_words, form_words):
    """A surname, as its words, stands whole in the heading, its first word capitalized."""
    n = len(form_words)
    if not n:
        return False
    low = [w.lower() for w in form_words]
    for i in range(len(head_words) - n + 1):
        if head_words[i][:1].isupper() and [w.lower() for w in head_words[i:i + n]] == low:
            return True
    return False


def heading_persons(head, candidates, day):
    """STYLE 3: of the document's persons ({key: [surname, ...]}), those the heading names; the sitting President
    only by "the President" or "President <his surname>"."""
    hw = words(head)
    pkey, psur = president_on(day)
    got = set()
    for k, surs in candidates.items():
        if k == pkey:
            continue
        if any(has_form(hw, words(s)) for s in surs if len(words(s)) and len(plain(s)) > 1):
            got.add(k)
    if names_president(head, psur):
        got.add(pkey)
    return got


def window(date, until=None):
    """STYLE 4: the days a document matches on, (first, last)."""
    d = datetime.date.fromisoformat(date)
    u = datetime.date.fromisoformat(until) if until else d
    if (u - d).days > 7:
        u = d
    return d - datetime.timedelta(days=1), u + datetime.timedelta(days=1)


def meets(a, b, x, y):
    return a <= y and x <= b


def sort_doc(doc, persons, entries, vol_threads, president=None):
    """STYLE 2, 5-7: (sort, by, [(entry id, [shared persons])]). doc: {title, placed}; persons: the heading's persons;
    entries: [{id, names, roots}] of the document's days; vol_threads: the volume's threads (top threads)."""
    why = routine(doc.get("title"), doc.get("placed"))
    if why:
        return "c", why, []
    vt = set(vol_threads)
    hits = []
    for e in entries:
        shared = sorted(set(e["names"]) & set(persons))
        if not shared:
            continue
        others = set(shared) - {president}
        if others and (set(e["roots"]) & vt or len(others) >= 2):
            hits.append((e["id"], shared))
    if hits:
        return "a", "persons", hits
    if not persons:
        th = [(e["id"], []) for e in entries if set(e["roots"]) & vt]
        if th:
            return "a", "thread", th
    return "b", "", []


def cited(texts):
    """STYLE 1: {(volume, id)} the texts link."""
    out = set()
    for t in texts:
        out |= set(LINK.findall(t))
    return out


def volume_of(cite):
    """'FRUS 1961–63, II, doc. 295' -> 'FRUS 1961–63, II'."""
    return re.sub(r",\s*doc\.\s*\S+$", "", cite or "")


# ---------------------------------------------------------------- the run

def main():
    sys.path.insert(0, os.path.join(HERE, ".."))
    from bib import daybook, lives, store

    root = store.ROOT
    docs = []
    for f in sorted(glob.glob(os.path.join(root, "daybook", "[12][0-9][0-9][0-9]-[01][0-9].yaml"))):
        for r in (store.load_yaml(f) or {}).get("docs") or []:
            if r.get("src") != "frus":
                continue
            m = KEY.match(r["key"])
            if m:
                docs.append(dict(r, volkey=m.group(1), id=m.group(2)))

    cal_files = [f for f in sorted(glob.glob(os.path.join(root, "lists", "cal", "*.yaml")))
                 if not f.endswith("th.yaml") and not f.endswith("list.yaml")]
    texts = [open(f, encoding="utf-8").read() for f in glob.glob(os.path.join(root, "lists", "cal", "*.yaml"))]
    done = cited(texts)

    series = store.Series(root)
    everyone = lives.everyone(series)
    alias = lives._CACHE.get("frus-alias", {})
    canon = lambda k: alias.get(k, k)
    surnames = {}
    for p in everyone:
        k = lives.key_of(p["name"])
        forms = surnames.setdefault(k, set())
        for n in set(p.get("names") or ()) | {p["name"]}:
            sur, given = lives.split_name(n)
            forms.add(sur)
            if "," not in n:                      # a name in its own order ('Mao Zedong', 'U Thant'): it whole
                forms.add(n)
    persons_json = os.path.join(root, "sources", "frus-names", "persons.json")
    for k, v in json.load(open(persons_json, encoding="utf-8")).items():
        forms = surnames.setdefault(canon(k), set())
        for n in set(v.get("names") or ()) | {v["name"]}:
            forms.add(lives.split_name(n)[0])

    named = {}                                    # (volume, number) -> {person key}
    for f in sorted(glob.glob(os.path.join(root, "sources", "frus-names", "[A-Z].json"))):
        for k, vols in json.load(open(f, encoding="utf-8")).items():
            ck = canon(k)
            for vol, v in vols.items():
                for row in (v.get("named") or []) + (v.get("sent") or []):
                    named.setdefault((vol, str(row[0])), set()).add(ck)

    heads = {}
    for f in sorted(glob.glob(os.path.join(root, "sources", "frus-text", "*.json.xz"))):
        for k, html in json.load(lzma.open(f, "rt", encoding="utf-8")).get("docs", {}).items():
            heads[k] = head_text(html)

    th = store.load_yaml(os.path.join(root, "lists", "cal", "th.yaml"))["entries"]
    parent = {e["id"][len("cal.thread."):]: e.get("parent") for e in th}

    def top(t):
        seen = set()
        while parent.get(t) and t not in seen:
            seen.add(t)
            t = parent[t]
        return t

    by_day = {}
    for f in cal_files:
        for e in (store.load_yaml(f) or {}).get("entries") or []:
            d = str(e.get("date", ""))
            if len(d) != 10 or not e.get("thread"):
                continue
            a = datetime.date.fromisoformat(d)
            b = daybook.end_of(e) or a
            row = {"id": e["id"], "start": a, "end": b,
                   "names": {canon(t[5:]) for t in store.as_list(e.get("tags")) if str(t).startswith("name:")},
                   "roots": {top(t) for t in [e["thread"]] + store.as_list(e.get("also"))}}
            x = a
            while x <= b:
                by_day.setdefault(x, []).append(row)
                x += datetime.timedelta(days=1)

    rows, counts = [], {}
    for doc in docs:
        if (doc["volkey"], doc["id"]) in done:
            continue
        num = doc["id"][1:] if re.fullmatch(r"d\d+[a-z]?", doc["id"]) else doc["id"]
        head = heads.get(doc["key"]) or doc.get("title") or ""
        if not re.match(r"(?i)telegram from the department of state\b", doc.get("title") or ""):
            head += " " + (doc.get("author") or "")   # STYLE 3: a Department telegram's signer is not its sender
        cands = {k: surnames.get(k, set()) for k in named.get((doc["volkey"], num), ())}
        pkey = president_on(doc["date"])[0]
        cands.setdefault(pkey, {president_on(doc["date"])[1]})
        ps = heading_persons(head, cands, doc["date"])
        a, b = window(doc["date"], doc.get("until"))
        seen, ents = set(), []
        x = a
        while x <= b:
            for e in by_day.get(x, []):
                if e["id"] not in seen and meets(a, b, e["start"], e["end"]):
                    seen.add(e["id"])
                    ents.append(e)
            x += datetime.timedelta(days=1)
        roots = THREADS.get(doc["volkey"], [])
        s, by, hits = sort_doc(doc, ps, ents, roots, president=pkey)
        vol = volume_of(doc.get("cite"))
        ids = " ".join(i + (f" [{', '.join(sh)}]" if sh else "") for i, sh in hits)
        title = re.sub(r"\s+", " ", doc.get("title") or "")
        rows.append([doc["key"], vol, num, doc["date"], title, s, by, ids])
        c = counts.setdefault((doc["volkey"], vol, doc.get("vol") or ""), {"a": 0, "b": 0, "c": 0})
        c[s] += 1

    missing = sorted({d["volkey"] for d in docs} - set(THREADS))
    if missing:
        print("volumes without threads:", ", ".join(missing), file=sys.stderr)
    out = os.path.join(root, "notes", "proposals", "frus-survey.tsv")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("key\tvolume\tnumber\tdate\theading\tsort\tby\tentries\n")
        for r in rows:
            fh.write("\t".join(str(x).replace("\t", " ") for x in r) + "\n")
    tot = {"a": 0, "b": 0, "c": 0}
    print("| Volume | Title | (a) | (b) | (c) |")
    print("|---|---|---:|---:|---:|")
    for (vk, vol, title), c in sorted(counts.items(), key=lambda kv: _order(kv[0][0])):
        print(f"| {vol} | {title} | {c['a']:,} | {c['b']:,} | {c['c']:,} |")
        for k in tot:
            tot[k] += c[k]
    print(f"| All | | {tot['a']:,} | {tot['b']:,} | {tot['c']:,} |")
    print(len(rows), "documents not cited;", out, file=sys.stderr)


def _order(vk):
    """frus1961-63v07-09mSupp after v07; v10p1 before v10p2."""
    m = re.match(r"frus(\d{4})-\d+v(\d+)(.*)$", vk)
    return (m.group(1), int(m.group(2)), m.group(3)) if m else (vk, 0, "")


if __name__ == "__main__":
    main()
