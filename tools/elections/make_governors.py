"""elections/governors.yaml: every general election for governor, 1960 to 1968, from Wikipedia (needs the network; the
build does not).

    python3 tools/elections/make_governors.py [--cache DIR]

The races: Wikipedia's tables of each year's gubernatorial elections ("1962 United States gubernatorial elections"),
which give the State, the incumbent, his party and the result ("Incumbent lost re-election. Republican gain."). The
figures: each race's own article ("1962 Colorado gubernatorial election"), its election boxes: the box of the general
election (its title names no primary, runoff or convention), each candidate's party, votes and share, the total, and
the source the article gives for the box (most cite the State's canvass or abstract; some Our Campaigns or CQ). Where
the article prints no votes, the year table's shares stand, `votes` empty, and the race carries `check`.

STYLE (the file):
 1. `years`: each year's table and its count of governorships by party before and after (Wikipedia's infobox).
    `races`: one race a row, by date and then State: `date` (the general election's), `st` (postal code), `state`, `incumbent`,
    `inc_party` (D, R, or another letter), `result` (the year table's words), `candidates` [{name, party, votes, pct,
    won}], `total`, `source` ({title, url} of the box's reference), `wiki` (the article), `check` (what is open).
 2. Parties by letter: D, R; others by their own name (Prohibition, Socialist Labor, Independent ...).
 3. Odd years: New Jersey and Virginia (1961, 1965), Kentucky and Mississippi (1963, 1967), Louisiana's general of
    Mar. 3, 1964 (its year table is 1963's), and of Feb. 6, 1968 (1967's).
 4. Never edit the file by hand: fix the script (HAND, laid over the race last: `check: None` clears the check) and
    rerun.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "elections", "governors.yaml")
UA = "bib-research/1.0 (calendar of the 1960s; contact through the repository)"

YEARS = {1960: "1960-11-08", 1961: "1961-11-07", 1962: "1962-11-06", 1963: "1963-11-05", 1964: "1964-11-03",
         1965: "1965-11-02", 1966: "1966-11-08", 1967: "1967-11-07",
         1968: "1968-11-05"}
DATE_BY_STATE = {("Louisiana", 1963): "1964-03-03", ("Louisiana", 1967): "1968-02-06"}
SKIP = set()

STATES = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
          "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
          "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
          "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
          "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
          "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
          "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
          "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
          "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
          "Wisconsin": "WI", "Wyoming": "WY"}

PARTY = {"democratic": "D", "republican": "R"}

# what the articles cannot settle, by (year, State): fields laid over the scraped race
HAND = {
    (1962, "Minnesota"): {"note": "Andersen led the first count; the recount gave Rolvaag 91 votes more, and the court "
                                  "declared him elected, Mar. 21, 1963."},
    (1967, "Louisiana"): {"winner": "John McKeithen",
                          "candidates": [{"name": "John McKeithen (incumbent)", "party": "D", "votes": None, "pct": 100.0,
                                          "won": True}],
                          "note": "McKeithen, renominated in the Democratic primary of Nov. 4, 1967, was unopposed in the general election."},
    # 1966: the races Wikipedia sources to Our Campaigns or to nothing, held to America Votes 7 (1968), its figures
    # read off the page images Nov. 1, 2026 (scratch: av7/governors-1966.yaml): the same figures, the book the source;
    # Pennsylvania's votes (the article prints shares only) the book's.
    (1966, 'Alabama'): {'source': {'title': 'America Votes 7 (1968) 12, 19', 'url': 'https://archive.org/details/americavotes7han00scam/page/n25/mode/1up'}, 'check': None},
    (1966, 'Arkansas'): {'source': {'title': 'America Votes 7 (1968) 31, 38', 'url': 'https://archive.org/details/americavotes7han00scam/page/n44/mode/1up'}, 'check': None},
    (1966, 'Florida'): {'source': {'title': 'America Votes 7 (1968) 74, 81', 'url': 'https://archive.org/details/americavotes7han00scam/page/n87/mode/1up'}, 'check': None},
    (1966, 'Hawaii'): {'source': {'title': 'America Votes 7 (1968) 92, 96', 'url': 'https://archive.org/details/americavotes7han00scam/page/n105/mode/1up'}, 'check': None},
    (1966, 'Minnesota'): {'source': {'title': 'America Votes 7 (1968) 195, 204', 'url': 'https://archive.org/details/americavotes7han00scam/page/n208/mode/1up'}, 'check': None},
    (1966, 'New York'): {'source': {'title': 'America Votes 7 (1968) 263, 286', 'url': 'https://archive.org/details/americavotes7han00scam/page/n276/mode/1up'}, 'check': None},
    (1966, 'Pennsylvania'): {'source': {'title': 'America Votes 7 (1968) 333, 349', 'url': 'https://archive.org/details/americavotes7han00scam/page/n346/mode/1up'}, 'check': None, 'candidates': [{'name': 'Raymond P. Shafer', 'party': 'R', 'votes': 2110349, 'pct': 52.1, 'won': True}, {'name': 'Milton Shapp', 'party': 'D', 'votes': 1868719, 'pct': 46.1, 'won': False}, {'name': 'Edward S. Swartz', 'party': 'Constitutional', 'votes': 57073, 'pct': 1.4, 'won': False}, {'name': 'George S. Taylor', 'party': 'Socialist Labor', 'votes': 14527, 'pct': 0.4, 'won': False}], 'total': 4050668},
    (1966, 'South Carolina'): {'source': {'title': 'America Votes 7 (1968) 357, 362', 'url': 'https://archive.org/details/americavotes7han00scam/page/n370/mode/1up'}, 'check': None},
    (1966, 'Texas'): {'source': {'title': 'America Votes 7 (1968) 379, 392', 'url': 'https://archive.org/details/americavotes7han00scam/page/n392/mode/1up'}, 'check': None},
    # 1961-68: the races Wikipedia sources to Our Campaigns or to nothing, held to America Votes 5, 6 and 8, read off the
    # page images Nov. 1, 2026 (scratch: av/out5, out6, out8): the book the source; its figures where they differ or the
    # article prints none. Virginia 1965: a transposition in the article.
    (1962, 'Alabama'): {'source': {'title': 'America Votes 5 (1964) 10, 17', 'url': 'https://archive.org/details/americavotes5han00scam/page/n25/mode/1up'}, 'check': None},
    (1962, 'Arkansas'): {'source': {'title': 'America Votes 5 (1964) 30, 37', 'url': 'https://archive.org/details/americavotes5han00scam/page/n45/mode/1up'}, 'check': None},
    (1962, 'California'): {'source': {'title': 'America Votes 5 (1964) 38, 51', 'url': 'https://archive.org/details/americavotes5han00scam/page/n53/mode/1up'}, 'check': None, 'candidates': [{'name': 'Edmund G. "Pat" Brown (incumbent)', 'party': 'D', 'votes': 3037109, 'pct': 51.89, 'won': True}, {'name': 'Richard M. Nixon', 'party': 'R', 'votes': 2740351, 'pct': 46.82, 'won': False}, {'name': 'Robert L. Wyckoff', 'party': 'Prohibition', 'votes': 69700, 'pct': 1.19, 'won': False}, {'name': 'Joseph C. Shell (write-in)', 'party': 'Independent', 'votes': 3166, 'pct': 0.05, 'won': False}, {'name': 'Herbert Steiner (write-in)', 'party': 'Independent', 'votes': 448, 'pct': 0.01, 'won': False}, {'name': 'R. C. Irvine (write-in)', 'party': 'Independent', 'votes': 159, 'pct': 0.0, 'won': False}, {'name': 'Scattering', 'party': '?', 'votes': 2299, 'pct': 0.04, 'won': False}], 'total': 5853270},
    (1962, 'Georgia'): {'source': {'title': 'America Votes 5 (1964) 82, 92', 'url': 'https://archive.org/details/americavotes5han00scam/page/n97/mode/1up'}, 'check': None},
    (1962, 'Hawaii'): {'source': {'title': 'America Votes 5 (1964) 94, 98', 'url': 'https://archive.org/details/americavotes5han00scam/page/n109/mode/1up'}, 'check': None},
    (1962, 'Minnesota'): {'source': {'title': 'America Votes 5 (1964) 201, 211', 'url': 'https://archive.org/details/americavotes5han00scam/page/n216/mode/1up'}, 'check': None, 'candidates': [{'name': 'Karl Rolvaag', 'party': 'D', 'votes': 619842, 'pct': 49.71, 'won': True}, {'name': 'Elmer Andersen (incumbent)', 'party': 'R', 'votes': 619751, 'pct': 49.7, 'won': False}, {'name': 'William Braatz', 'party': 'Industrial Government', 'votes': 7311, 'pct': 0.59, 'won': False}], 'total': 1246904, 'note': 'Andersen led the first count; the recount gave Rolvaag 91 votes more, and the court declared him elected, Mar. 21, 1963.'},
    (1962, 'New York'): {'source': {'title': 'America Votes 5 (1964) 271, 291', 'url': 'https://archive.org/details/americavotes5han00scam/page/n286/mode/1up'}, 'check': None, 'candidates': [{'name': 'Nelson Rockefeller (incumbent)', 'party': 'R', 'votes': 3081587, 'pct': 53.08, 'won': True}, {'name': 'Robert Morgenthau', 'party': 'D', 'votes': 2552418, 'pct': 43.96, 'won': False}, {'name': 'Robert Morgenthau', 'party': 'Liberal  of New York', 'votes': 2552418, 'pct': 43.96, 'won': False}, {'name': 'Robert Morgenthau', 'party': 'Total', 'votes': 2552418, 'pct': 43.96, 'won': False}, {'name': 'David H. Jaquith', 'party': 'Conservative  of New York', 'votes': 141877, 'pct': 2.44, 'won': False}, {'name': 'Richard Garza', 'party': 'Socialist Workers', 'votes': 19698, 'pct': 0.34, 'won': False}, {'name': 'Eric Hass', 'party': 'Socialist Labor', 'votes': 9762, 'pct': 0.17, 'won': False}], 'total': 5805631},
    (1962, 'Pennsylvania'): {'source': {'title': 'America Votes 5 (1964) 342, 356', 'url': 'https://archive.org/details/americavotes5han00scam/page/n357/mode/1up'}, 'check': None, 'candidates': [{'name': 'William Scranton', 'party': 'R', 'pct': 55.39, 'won': True, 'votes': 2424918}, {'name': 'Richardson Dilworth', 'party': 'D', 'pct': 44.28, 'won': False, 'votes': 1938627}, {'name': 'George Sam Taylor', 'party': 'Socialist Labor', 'pct': 0.33, 'won': False, 'votes': 14340}], 'total': 4378042},
    (1962, 'South Carolina'): {'source': {'title': 'America Votes 5 (1964) 364, 369', 'url': 'https://archive.org/details/americavotes5han00scam/page/n379/mode/1up'}, 'check': None},
    (1962, 'Texas'): {'source': {'title': 'America Votes 5 (1964) 387, 401', 'url': 'https://archive.org/details/americavotes5han00scam/page/n402/mode/1up'}, 'check': None, 'candidates': [{'name': 'John Connally', 'party': 'D', 'votes': 847036, 'pct': 53.98, 'won': True}, {'name': 'Jack Cox', 'party': 'R', 'votes': 715025, 'pct': 45.57, 'won': False}, {'name': 'Jack Carswell', 'party': 'Constitution', 'votes': 7120, 'pct': 0.45, 'won': False}], 'total': 1569181},
    (1964, 'Arkansas'): {'source': {'title': 'America Votes 6 (1966) 33, 40', 'url': 'https://archive.org/details/americavotes6han00scam/page/n46/mode/1up'}, 'check': None},
    (1964, 'Delaware'): {'source': {'title': 'America Votes 6 (1966) 69, 73', 'url': 'https://archive.org/details/americavotes6han00scam/page/n82/mode/1up'}, 'check': None},
    (1964, 'Indiana'): {'source': {'title': 'America Votes 6 (1966) 120, 128', 'url': 'https://archive.org/details/americavotes6han00scam/page/n133/mode/1up'}, 'check': None},
    (1964, 'Missouri'): {'source': {'title': 'America Votes 6 (1966) 226, 236', 'url': 'https://archive.org/details/americavotes6han00scam/page/n239/mode/1up'}, 'check': None},
    (1964, 'Texas'): {'source': {'title': 'America Votes 6 (1966) 397, 412', 'url': 'https://archive.org/details/americavotes6han00scam/page/n410/mode/1up'}, 'check': None},
    (1964, 'West Virginia'): {'source': {'title': 'America Votes 6 (1966) 445, 450', 'url': 'https://archive.org/details/americavotes6han00scam/page/n458/mode/1up'}, 'check': None},
    (1963, 'Louisiana'): {'source': {'title': 'America Votes 6 (1966) 155, 165', 'url': 'https://archive.org/details/americavotes6han00scam/page/n168/mode/1up'}, 'check': None, 'candidates': [{'name': 'John McKeithen', 'party': 'D', 'pct': 60.72, 'won': True, 'votes': 469589}, {'name': 'Charlton Lyons', 'party': 'R', 'pct': 38.5, 'won': False, 'votes': 297753}, {'name': 'Williams', 'party': 'States Rights', 'votes': 6048, 'pct': 0.78, 'won': False}], 'total': 773390},
    (1961, 'Virginia'): {'source': {'title': 'America Votes 6 (1966) 426', 'url': 'https://archive.org/details/americavotes6han00scam/page/n439/mode/1up'}, 'check': None, 'candidates': [{'name': 'Albertis S. Harrison, Jr.', 'party': 'D', 'votes': 251861, 'pct': 63.84, 'won': True}, {'name': 'H. Clyde Pearson', 'party': 'R', 'votes': 142567, 'pct': 36.14, 'won': False}], 'total': 394490},
    (1965, 'Virginia'): {'source': {'title': 'America Votes 6 (1966) 426, 436', 'url': 'https://archive.org/details/americavotes6han00scam/page/n439/mode/1up'}, 'check': None, 'candidates': [{'name': 'Mills E. Godwin Jr.', 'party': 'D', 'votes': 269526, 'pct': 47.89, 'won': True}, {'name': 'A. Linwood Holton Jr.', 'party': 'R', 'votes': 212207, 'pct': 37.71, 'won': False}, {'name': 'William J. Story Jr.', 'party': 'Conservative  of Virginia (1965)', 'votes': 75307, 'pct': 13.38, 'won': False}, {'name': 'George Lincoln Rockwell', 'party': 'White Constitutional', 'votes': 5730, 'pct': 1.02, 'won': False}, {'name': '', 'party': 'Write-ins', 'votes': 19, 'pct': 0.0, 'won': False}], 'total': 562789, 'note': "Wikipedia prints Godwin's vote 296,526, the digits transposed; America Votes 6 prints 269,526."},
    (1968, 'Arkansas'): {'source': {'title': 'America Votes 8 (1970) 23, 32', 'url': 'https://archive.org/details/americavotes8elec/page/n34/mode/1up'}, 'check': None},
    (1968, 'Delaware'): {'source': {'title': 'America Votes 8 (1970) 58, 62', 'url': 'https://archive.org/details/americavotes8elec/page/n69/mode/1up'}, 'check': None},
    (1968, 'Indiana'): {'source': {'title': 'America Votes 8 (1970) 107, 116', 'url': 'https://archive.org/details/americavotes8elec/page/n118/mode/1up'}, 'check': None},
    (1967, 'Louisiana'): {'source': {'title': 'America Votes 8 (1970) 148, 157', 'url': 'https://archive.org/details/americavotes8elec/page/n159/mode/1up'}, 'check': None, 'candidates': [{'name': 'John McKeithen (incumbent)', 'party': 'D', 'votes': 372762, 'pct': 100.0, 'won': True}], 'total': 372762, 'winner': 'John McKeithen', 'note': 'McKeithen, renominated in the Democratic primary of Nov. 4, 1967, was unopposed in the general election.'},
    (1968, 'Missouri'): {'source': {'title': 'America Votes 8 (1970) 208, 221', 'url': 'https://archive.org/details/americavotes8elec/page/n219/mode/1up'}, 'check': None},
    (1968, 'New Hampshire'): {'source': {'title': 'America Votes 8 (1970) 240, 245', 'url': 'https://archive.org/details/americavotes8elec/page/n251/mode/1up'}, 'check': None},
    (1968, 'Texas'): {'source': {'title': 'America Votes 8 (1970) 364, 377', 'url': 'https://archive.org/details/americavotes8elec/page/n375/mode/1up'}, 'check': None, 'candidates': [{'name': 'Preston Smith', 'party': 'D', 'votes': 1662019, 'pct': 56.99, 'won': True}, {'name': 'Paul Eggers', 'party': 'R', 'votes': 1254333, 'pct': 43.01, 'won': False}], 'total': 2916509},
    (1968, 'West Virginia'): {'source': {'title': 'America Votes 8 (1970) 406, 411', 'url': 'https://archive.org/details/americavotes8elec/page/n417/mode/1up'}, 'check': None},
    (1967, 'Mississippi'): {'source': {'title': 'America Votes 8 (1970) 200, 207', 'url': 'https://archive.org/details/americavotes8elec/page/n211/mode/1up'}, 'check': None},
    (1966, "Georgia"): {"winner": "Lester Maddox",
                        "note": "No candidate had a majority; the General Assembly elected Maddox, Jan. 10, 1967."},
}


def fetch(title, cache):
    path = os.path.join(cache, re.sub(r"[^\w.-]", "_", title) + ".txt") if cache else None
    if path and os.path.exists(path):
        return open(path, encoding="utf-8").read()
    url = "https://en.wikipedia.org/w/index.php?" + urllib.parse.urlencode({"title": title, "action": "raw", "redirect": "yes"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                text = r.read().decode("utf-8")
            break
        except Exception as ex:  # noqa: BLE001
            if i == 3:
                print(f"  failed {title}: {ex}", file=sys.stderr)
                return ""
            time.sleep(2 ** (i + 1))
    m = re.match(r"#REDIRECT\s*\[\[([^\]|#]+)", text, re.I)
    if m:
        return fetch(m.group(1), cache)
    if path:
        os.makedirs(cache, exist_ok=True)
        open(path, "w", encoding="utf-8").write(text)
    time.sleep(0.3)
    return text


# ---------------------------------------------------------------- wikitext

def templates(text, name_re):
    """Each top-level {{...}} whose name matches name_re: (name, [params as raw strings], start, end)."""
    out = []
    i = 0
    while True:
        j = text.find("{{", i)
        if j < 0:
            return out
        depth, k = 0, j
        while k < len(text):
            if text.startswith("{{", k):
                depth += 1
                k += 2
            elif text.startswith("}}", k):
                depth -= 1
                k += 2
                if depth == 0:
                    break
            else:
                k += 1
        body = text[j + 2:k - 2]
        parts = split_top(body)
        name = parts[0].strip() if parts else ""
        if re.match(name_re, name, re.I):
            out.append((name, parts[1:], j, k))
            i = k
        else:
            i = j + 2                       # look inside it


def split_top(body):
    parts, cur, depth, sq = [], "", 0, 0
    i = 0
    while i < len(body):
        if body.startswith("{{", i):
            depth += 1; cur += "{{"; i += 2; continue
        if body.startswith("}}", i):
            depth -= 1; cur += "}}"; i += 2; continue
        if body.startswith("[[", i):
            sq += 1; cur += "[["; i += 2; continue
        if body.startswith("]]", i):
            sq -= 1; cur += "]]"; i += 2; continue
        if body[i] == "|" and depth == 0 and sq == 0:
            parts.append(cur); cur = ""; i += 1; continue
        cur += body[i]; i += 1
    parts.append(cur)
    return parts


def params(parts):
    d = {}
    for p in parts:
        if "=" in p:
            k, v = p.split("=", 1)
            d[k.strip().lower()] = v.strip()
    return d


def plain(s):
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\{\{(?:sortname)\|([^|}]*)\|([^|}]*)[^}]*\}\}", r"\1 \2", s, flags=re.I)
    s = re.sub(r"\{\{(?:nowrap|small)\|([^}]*)\}\}", r"\1", s, flags=re.I)
    s = re.sub(r"\{\{[^}]*\}\}", "", s)
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s)
    s = s.replace("'''", "").replace("''", "")
    return re.sub(r"\s+", " ", s).strip()


def party_code(s):
    """D or R, a State's own label for the party included ("California Democratic", "Minnesota Democratic–Farmer–Labor",
    "North Dakota Democratic-NPL"); another party by its name."""
    p = plain(s).replace("(United States)", "").replace("(US)", "").replace("Party", "").strip()
    low = re.sub(r"^(?:%s)\s+" % "|".join(re.escape(x.lower()) for x in STATES), "", p.lower())
    for k, v in PARTY.items():
        if low.startswith(k):
            return v
    return p or "?"


def num(s):
    s = plain(s).replace(",", "")
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return float(m.group(0)) if m else None


def refs(text):
    """named references: name -> {title, url}"""
    out = {}
    for m in re.finditer(r'<ref\s+name\s*=\s*"?([^">/]+?)"?\s*>(.*?)</ref>', text, re.S):
        out[m.group(1).strip()] = cite(m.group(2))
    return out


def cite(body):
    t = templates(body, r"cite|citation")
    if t:
        p = params(t[0][1])
        return {k: plain(p[k]) if k != "url" else p[k] for k in ("title", "url", "publisher", "work", "year", "page", "pages")
                if p.get(k)}
    m = re.search(r"https?://\S+", body)
    return {"url": m.group(0).rstrip("]")} if m else {"title": plain(body)}


def box_source(title_raw, named):
    m = re.search(r'<ref\s+name\s*=\s*"?([^">/]+?)"?\s*/>', title_raw)
    if m and m.group(1).strip() in named:
        return named[m.group(1).strip()]
    m = re.search(r"<ref[^>]*>(.*?)</ref>", title_raw, re.S)
    return cite(m.group(1)) if m else None


def boxes(text):
    """the election boxes: [{title, source, candidates, total}]"""
    named = refs(text)
    out = []
    for m in re.finditer(r"\{\{\s*Election box begin", text, re.I):
        end = text.find("{{Election box end", m.start())
        if end < 0:
            end = len(text)
        seg = text[m.start():end]
        begin = templates(seg, r"Election box begin")
        head = params(begin[0][1]) if begin else {}
        title_raw = head.get("title", "")
        cands, total = [], None
        for name, parts, _, _ in templates(seg, r"Election box"):
            p = params(parts)
            low = name.lower()
            if "candidate" in low:
                cands.append({"name": plain(p.get("candidate", "")), "party": party_code(p.get("party", "")),
                              "votes": num(p.get("votes", "")), "pct": num(p.get("percentage", "")),
                              "won": "winning" in low})
            elif "total" in low:
                total = num(p.get("votes", ""))
        out.append({"title": plain(title_raw), "source": box_source(title_raw, named), "candidates": cands, "total": total})
    return out


GENERAL_NOT = re.compile(r"primary|runoff|run-off|convention|caucus|nominat", re.I)


def general_box(bx, year, state):
    cands = [b for b in bx if b["candidates"] and not GENERAL_NOT.search(b["title"])]
    if not cands:
        return None
    exact = [b for b in cands if str(year) in b["title"] and state.lower() in b["title"].lower()]
    pick = (exact or cands)
    return max(pick, key=lambda b: sum(c["votes"] or 0 for c in b["candidates"]))


# ---------------------------------------------------------------- the year tables

def year_rows(text, year):
    rows = []
    for block in re.split(r"\n\|-", text):
        m = re.search(r"^!\s*(?:scope=\"?row\"?\s*\|)?\s*\[\[([^|\]]*gubernatorial[^|\]]*)\|([^\]]+)\]\]", block, re.M)
        if not m:
            continue
        state = plain(m.group(2))
        if state not in STATES:
            continue
        lines = [ln for ln in block.split("\n") if ln.strip()]
        inc = next((plain(ln.lstrip("|")) for ln in lines if "sortname" in ln.lower()), "")
        party = next((ln for ln in lines if "party shading" in ln.lower() and "result" not in ln.lower()), "")
        pm = re.search(r"party shading/(?:Text/)?([A-Za-z -]+)", party, re.I)
        result = next((plain(ln.split("|", 2)[-1]) for ln in lines if re.search(r"incumbent|retired|term-limited|elected|died|resigned|new state", ln, re.I)
                       and "plainlist" not in ln.lower() and not ln.lstrip().startswith("*")), "")
        shares = []
        for ln in lines:
            if ln.lstrip().startswith("*"):
                won = "{{aye}}" in ln.lower()
                t = plain(ln.lstrip("* "))
                mm = re.match(r"(.*?)\s*\(([^)]*)\)\s*([\d.]+)\s*%", t)
                if mm:
                    shares.append({"name": mm.group(1).strip(), "party": party_code(mm.group(2)),
                                   "pct": float(mm.group(3)), "won": won})
        rows.append({"state": state, "article": m.group(1).strip(), "incumbent": inc,
                     "inc_party": party_code(pm.group(1)) if pm else "?", "result": result, "shares": shares})
    return rows


def oneline_rows(text):
    """the odd years' tables: one row a line, cells parted by '||' (State, incumbent, party, status, candidates)."""
    rows = []
    for ln in text.split("\n"):
        if not ln.startswith("|") or "||" not in ln or "gubernatorial" not in ln:
            continue
        cells = [c.strip() for c in ln[1:].split("||")]
        if len(cells) < 5:
            continue
        m = re.search(r"\[\[([^|\]]*gubernatorial[^|\]]*)\|([^\]]+)\]\]", cells[0])
        if not m or plain(m.group(2)) not in STATES:
            continue
        inc = plain(re.sub(r"^[^|\[]*\|", "", cells[1]))
        shares = []
        for part in re.split(r"<br\s*/?>", cells[4]):
            t = plain(part)
            mm = re.match(r"(.*?)\s*\(([^)]*)\)\s*([\d.]+)\s*%", t)
            if mm:
                shares.append({"name": mm.group(1).strip(), "party": party_code(mm.group(2)), "pct": float(mm.group(3)),
                               "won": "'''" in part})
        rows.append({"state": plain(m.group(2)), "article": m.group(1).strip(), "incumbent": inc,
                     "inc_party": party_code(cells[2]), "result": plain(cells[3]), "shares": shares})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache")
    a = ap.parse_args()
    races, years = [], {}
    for year, date in YEARS.items():
        text = fetch(f"{year} United States gubernatorial elections", a.cache)
        rows = year_rows(text, year) or oneline_rows(text)
        box = params((templates(text, r"Infobox election") or [("", [], 0, 0)])[0][1])
        seats = {}
        for i in (1, 2):
            p = party_code(box.get(f"party{i}", ""))
            b, af = num(re.sub(r"\{\{efn.*", "", box.get(f"seats_before{i}", ""))), num(box.get(f"seats_after{i}", ""))
            if p in ("D", "R") and b is not None:
                seats[p] = {"before": int(b), "after": int(af) if af is not None else None}
        years[year] = {"seats": seats, "table": f"{year} United States gubernatorial elections"}
        print(f"{year}: {len(rows)} races", file=sys.stderr)
        for r in rows:
            if (r["state"], year) in SKIP:
                continue
            art = fetch(r["article"], a.cache)
            bx = general_box(boxes(art), year, r["state"]) if art else None
            race = {"date": DATE_BY_STATE.get((r["state"], year), date), "st": STATES[r["state"]], "state": r["state"],
                    "incumbent": r["incumbent"], "inc_party": r["inc_party"], "result": r["result"]}
            checks = []
            if bx and any(c["votes"] for c in bx["candidates"]):
                cands = []
                for c in bx["candidates"]:
                    cands.append({k: (int(v) if k == "votes" and v is not None else v) for k, v in c.items()})
                race["candidates"] = cands
                race["total"] = int(bx["total"]) if bx["total"] else sum(c["votes"] or 0 for c in cands)
                race["source"] = bx["source"] or {}
                if not race["source"]:
                    checks.append("the article cites no source for the figures")
                elif "ourcampaigns" in race["source"].get("url", ""):
                    checks.append("the article's source is Our Campaigns; the State's canvass")
            else:
                race["candidates"] = [dict(s, votes=None) for s in r["shares"]]
                race["total"] = None
                race["source"] = {}
                checks.append("the article prints no votes; shares from the year table")
            race["wiki"] = r["article"]
            if checks:
                race["check"] = "; ".join(checks)
            race.update(HAND.get((year, r["state"]), {}))       # HAND last: a source it gives clears the check
            if race.get("check") is None:
                race.pop("check", None)
            races.append(race)
    races.sort(key=lambda r: (r["date"], r["state"]))
    head = ("# Every general election for governor, 1960-66: written by tools/elections/make_governors.py from Wikipedia\n"
            "# (its docstring has the fields and the sources). Never edit by hand: fix the script and rerun.\n")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(head)
        yaml.safe_dump({"years": years, "races": races}, f, allow_unicode=True, sort_keys=False, width=120)
    print(f"{len(races)} races -> {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
