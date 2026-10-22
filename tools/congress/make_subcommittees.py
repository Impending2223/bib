"""The subcommittees of the 87th and 88th Congresses, with their chairmen and members, from the Congressional Staff
Directory: congress/subcommittees.yaml.

Usage: python3 -I tools/congress/make_subcommittees.py CACHE_DIR
  CACHE_DIR   where each edition's page text is kept (<id>_djvu.xml and <id>_page_numbers.json, archive.org's OCR of
              the scan and its page numbers); fetched if missing
Run once; rerun after changing the rules here; never edit the output. The build needs no network.

Why this source. The Congressional Directory prints no subcommittee in any edition from 1961 to Mar. 1971, and from
Dec. 1971 only each subcommittee's chairman and ranking minority member (tools/congress/make_cdir_committees.py). The
Congressional Staff Directory (Charles B. Brownson, annual from 1959) prints every standing, select and joint
committee's subcommittees with their members, by surname. Its editions of 1961 and 1963 are open on archive.org, the
Digital Library of India's scans (EDITIONS); 1965, 1967 and 1969 were not found there (notes/leads.md). Only the
facts are taken (who sat on which subcommittee); the scans stay where they are.

What an edition prints, under each committee ("COMMITTEE ON AGRICULTURE AND FORESTRY", "JOINT ECONOMIC COMMITTEE"),
after the full committee's list: each subcommittee's heading in capitals ("SUBCOMMITTEE ON SOIL CONSERVATION AND
FORESTRY", "SUBCOMMITTEE NO. 2", "PERMANENT SUBCOMMITTEE ON INVESTIGATIONS"), its chairman ("James O. Eastland (D.
Miss.), Chairman"), and two lines "MAJORITY: (5 D.) Senators Eastland, Johnston, Proxmire, Hart, and McCarthy." and
"MINORITY: (3 R.) Senators Aiken, Hickenlooper, and Boggs." (a joint committee's: "Senators Gore and Anderson,
Representatives Holifield and Price"), a surname with its State where two of the name sit ("Young (Ohio)").
RULES
 1. The lines of each page in the order of their height on it. A heading: a line nearly all capitals; a committee's
    when it reads as "COMMITTEE ON", "SELECT", "SPECIAL" or "JOINT" ... "COMMITTEE" (the OCR's misreadings allowed),
    and names a committee of the committee list (congress/committees.yaml's standing committees,
    congress/committees-cdir.yaml's select, special and joint ones) at .75 of its letters (a long name's first line
    against its beginning); a subcommittee's when it
    holds "SUBCOMMITTEE" so read. "(Continued)" goes on with the one before. A subcommittee's heading run over two
    lines is one.
 2. The chamber: each MAJORITY or MINORITY line's own word ("Senators", "Representatives"), the committee of the
    heading's name in that chamber; a joint committee's members each by the word before them. A MINORITY line the
    OCR runs into the MAJORITY line is read as its own.
 3. A MAJORITY or MINORITY line runs on over the lines under it to its stop, or till it holds its printed count of
    names, never into the staff's table beside it (Prof. Staff Mbr., NSOB, Clerk); a word broken at the line's end
    is joined; 'ond' and the like are the OCR's 'and'. Its printed count ("(5 D.)") is kept; where the names read do not make it, the subcommittee carries
    "check".
 4. A name is the member of the parent committee (any time in the Congress; for a joint committee, of his chamber)
    whose surname reads most like it, at .7 of its letters (.65 for a name of four letters or fewer: 'Kyi', Kyl), of the line's party (MAJORITY, the Democrats in these
    Congresses), the State in parentheses settling two of a surname; else, of the chamber's roster at the opening,
    with "check". The chairman: the member of the subcommittee whose surname his line gives.
 5. The subcommittee's name: its heading, the word after SUBCOMMITTEE "on" (or "No." before a number), each other
    word put right against VOCAB (WORDS, and the words of the Digest's committees and subcommittees, 1961-64: a word
    counted COMMON times there is kept, another goes to the nearest, at .7 of its letters, the commoner of two near
    alike, or stays as read), in title case; then, where one of the Digest's names of the committee's subcommittees
    reads as it at .9 (not a numbered one), the Digest's; a numbered one whose number is lost or not above the one
    before it, the number after that one; a word left unread, "check" ("Subcommittee on Soil Conservation and Forestry").
 6. The page: the edition's printed page (archive.org's page numbers), linked to the leaf.
"""
import difflib
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bib import store  # noqa: E402

EDITIONS = {87: {"id": "dli.ernet.166100", "file": "166100-Congressional Staff Directory 1961 Staff Biographies",
                 "title": "Congressional Staff Directory, 1961", "year": 1961},
            88: {"id": "dli.ernet.169159", "file": "169159-Congressional Staff Directory 1963",
                 "title": "Congressional Staff Directory, 1963", "year": 1963}}
DL = "https://archive.org/download/{id}/{file}"
LEAF = "https://archive.org/details/{id}/page/n{n}/mode/1up"
UA = {"User-Agent": "bib-congress (https://impending2223.github.io/bib/)"}
# the State in a member's parentheses, as the Staff Directory writes it
ABBR = {"ala": "AL", "alaska": "AK", "ariz": "AZ", "ark": "AR", "calif": "CA", "cal": "CA", "colo": "CO", "conn": "CT",
        "del": "DE", "fla": "FL", "ga": "GA", "hawaii": "HI", "idaho": "ID", "ill": "IL", "ind": "IN", "iowa": "IA",
        "kans": "KS", "kan": "KS", "ky": "KY", "la": "LA", "maine": "ME", "me": "ME", "md": "MD", "mass": "MA",
        "mich": "MI", "minn": "MN", "miss": "MS", "mo": "MO", "mont": "MT", "nebr": "NE", "neb": "NE", "nev": "NV",
        "nh": "NH", "nj": "NJ", "nmex": "NM", "nm": "NM", "ny": "NY", "nc": "NC", "ncar": "NC", "nd": "ND", "ndak": "ND",
        "ohio": "OH", "okla": "OK", "oreg": "OR", "ore": "OR", "pa": "PA", "ri": "RI", "sc": "SC", "scar": "SC",
        "sd": "SD", "sdak": "SD", "tenn": "TN", "tex": "TX", "utah": "UT", "vt": "VT", "va": "VA", "wash": "WA",
        "wva": "WV", "wis": "WI", "wyo": "WY", "pr": "PR"}
SMALL = {"0f": "of", "of": "of", "oh": "on", "0m": "on", "om": "on", "on": "on", "0n": "on", "an0": "and", "anb": "and",
         "amb": "and", "amd": "and", "ano": "and", "amp": "and", "anp": "and", "and": "and", "ahb": "and", "aho": "and",
         "anq": "and", "an": "and", "the": "the", "to": "to",
         "for": "for", "in": "in", "no": "No."}
LOWER = {"of", "on", "and", "the", "to", "for", "in", "a"}


def fetch(ed, cache):
    out = {}
    for suf in ("_djvu.xml", "_page_numbers.json"):
        p = os.path.join(cache, ed["id"] + suf)
        if not os.path.exists(p):
            url = DL.format(id=ed["id"], file=urllib.parse.quote(ed["file"] + suf))
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600) as r, \
                    open(p + ".part", "wb") as f:
                f.write(r.read())
            os.rename(p + ".part", p)
        out[suf] = p
    return out


def pages(xml):
    """[[(x, y, text)] a leaf], the leaf's lines in the order of their height (RULES 1)."""
    s = open(xml, encoding="utf-8").read()
    out = []
    for obj in re.finditer(r"<OBJECT .*?</OBJECT>", s, re.S):
        lines = []
        for ln in re.finditer(r"<LINE>(.*?)</LINE>", obj.group(0), re.S):
            ws = re.findall(r"<WORD coords=\"([^\"]*)\"[^>]*>(.*?)</WORD>", ln.group(1), re.S)
            if ws:
                xs = [int(c.split(",")[0]) for c, _ in ws]
                ys = [int(c.split(",")[1]) for c, _ in ws]
                lines.append((min(xs), max(ys), " ".join(html.unescape(w) for _, w in ws)))
        # the pieces the OCR made of one printed line ('MINORITY: (10 R.) Senators' 'Bridg' 'es, Saltonstall'): one
        # line, left to right, a word broken between two pieces joined
        rows = []
        for l in sorted(lines, key=lambda l: (l[1], l[0])):
            if rows and l[1] - rows[-1][0] <= 14:
                rows[-1][1].append(l)
            else:
                rows.append([l[1], [l]])
        merged = []
        for y0, ls in rows:
            ls.sort(key=lambda l: l[0])
            t = ls[0][2]
            for l in ls[1:]:
                t = t + l[2] if re.search(r"[a-z]$", t) and re.match(r"[a-z]", l[2]) else t + " " + l[2]
            merged.append((ls[0][0], max(l[1] for l in ls), t))
        out.append(merged)
    return out


def letters(t):
    return re.sub(r"[^a-z]", "", t.lower())


def capsy(t):
    ls = re.sub(r"[^A-Za-z]", "", t)
    return len(ls) >= 6 and sum(c.isupper() for c in ls) / len(ls) > .72


def is_sub(t):
    """A word reading as SUBCOMMITTEE ('SWBCOMMITTH', 'SyBCOMMiTTIE'), nearer it than COMMITTEE."""
    for tok in t.split():
        w = letters(tok)
        if len(w) >= 10 and 2 <= w.find("comm") <= 4:      # 'SPECOMMIITEE', 'SUaCOMMITIli'
            return True
        r = difflib.SequenceMatcher(None, w, "subcommittee").ratio()
        if r >= .7 and r > difflib.SequenceMatcher(None, w, "committee").ratio():
            return True
    return False


MAJ = re.compile(r"^\W*([MA4]\W?[A4]?\W?J|M\W?I\W?N)\w{2,6}\W*\s*\(?\s*(\d+)?\s*([DR])?", re.I)


def maj_line(t):
    """'maj' or 'min' and the printed count, for a MAJORITY or MINORITY line ('A4AJORITY;(3D.)')."""
    m = re.match(r"^\W*([A-Za-z4]{5,9})\s*[:;.,]?\s*(?:\(\s*(\d+)\s*([DR])?\W*\)?)?", t)
    if not m:
        return None
    w = letters(m.group(1).replace("4", "m"))
    r, k = max((difflib.SequenceMatcher(None, w, ref).ratio(), k) for k, ref in (("maj", "majority"),
                                                                              ("min", "minority")))
    return (k, int(m.group(2)) if m.group(2) else None, m.end()) if r >= .75 else None


def committee_name(t, names):
    """(code, ch, name) of the committee list's committee a heading names, else None (RULES 1)."""
    h = re.sub(r"\(.*$", "", t)
    w = letters(h)
    if not w or is_sub(t):
        return None
    best, score = None, 0
    for (code, ch, name) in names:
        forms = [name] if re.match(r"^(Select|Special|Joint)", name) else [f"Committee on {name}",
                                                                         f"Committee on the {name}"]
        if name == "Select Committee on Small Business" and ch == "h":
            forms.append("Select Committee to Conduct a Study and Investigation of the Problems of Small Business")
        for f in forms:
            r = difflib.SequenceMatcher(None, w, letters(f)).ratio()
            if len(w) >= 30:      # the first line of a long name ('SELECT COMMITTEE TO CONDUCT A STUDY AND ...')
                r = max(r, difflib.SequenceMatcher(None, w, letters(f)[:len(w)]).ratio() - .01)
            if r > score:
                best, score = (code, ch, name), r
    return best if score >= .75 else None


def digest_rows():
    """The Daily Digest's meetings of 1961-64 (daybook/committees/), for the words and the forms of RULES 5."""
    out = []
    for f in sorted(os.listdir(os.path.join(ROOT, "daybook", "committees"))):
        if re.match(r"196[1-4]-\d{2}\.yaml$", f):
            out += (store.load_yaml(os.path.join(ROOT, "daybook", "committees", f)) or {}).get("docs") or []
    return out


# the words the committees' and subcommittees' names are made of, beside the Digest's own
WORDS = ("subcommittee special select permanent general ad hoc legislative investigating consultative and of on the to "
         "for in affairs agricultural agriculture appropriations armed services banking currency business commerce "
         "communications conservation constitutional amendments credit dairy defense department departments "
         "development district columbia economic education elections electrification employment european far east "
         "eastern federal finance financial fiscal flood control foreign forests forestry freight government "
         "grounds harbors health housing immigration independent offices indian institutions insurance interior "
         "intergovernmental international investigations irrigation judicial judiciary justice labor lands "
         "legislation library machinery manpower marketing military minerals materials fuels mines mining monopoly "
         "national naturalization oversight parks patents trademarks copyrights policy postal power prices "
         "privileges procurement production public reclamation related relations research retirement rivers roads "
         "rules rural safety securities security small stabilization state statistics stockpile surface taxation "
         "territories territorial insular tobacco trade transportation treasury veterans water watershed welfare "
         "wheat wildlife cotton livestock feed grains oilseeds rice poultry operations organization reorganization "
         "executive civil service census aviation antitrust claims bankruptcy revision laws merchant marine "
         "fisheries coast guard geodetic survey navigation panama canal oceanography accounts printing enrolled "
         "bills memorials buildings construction real estate central intelligence agency naval petroleum reserves "
         "officer grade citations article status forces treaty conflict interest preparedness supplemental "
         "deficiencies deficiency compensation pension pensions hospitals training scientific science space "
         "sciences aeronautics astronautics regulatory agencies administrative procedure health compensation "
         "charter holiday celebration penitentiaries internal juvenile delinquency refugees escapees railroad "
         "unemployment migratory life benefits contested nominations standing smithsonian institution "
         "distribution metals aid basic advertising growth opportunities matters affecting problems consider nasa "
         "parking communities radiation applications tracking data acquisition manned flight budget foundations impact "
         "their disarmament monetary south asian asia codification elderly automobile practices shortage retailing "
         "financing taxes facilities activities wherry shipyard utilization donable property information submerged "
         "imports electrical mechanical office equipment contracts natural resources legal staffing technology "
         "automation regulations relationships inter american intermediate care africa europe near pacific review "
         "programs board impact domestic family farms consumer departmental supplies extension forests livestock "
         "equipment cooperation applications raw organizations disposal").split()


def vocab(rows):
    """VOCAB (RULES 5): the words of the Digest's committees and subcommittees (1961-64) and WORDS, with counts."""
    from collections import Counter
    c = Counter({w: COMMON for w in WORDS})
    for x in rows:
        for t in (x.get("sub"), x.get("name")):
            for w in re.findall(r"[A-Za-z]{3,}", t or ""):
                c[w.lower()] += 1
    return c


def forms(rows):
    """{(ch, code): Counter of the Digest's names of the committee's subcommittees} (RULES 5)."""
    from collections import Counter
    out = {}
    for x in rows:
        if x.get("sub"):
            out.setdefault((x["ch"].lower(), x["code"]), Counter())[re.sub(r"[\s,.;:]+$", "", x["sub"])] += 1
    return out


COMMON = 12        # a word of VOCAB counted this often is a word, not the OCR's


def fix_word(w, V):
    lw = re.sub(r"[^a-z0-9]", "", w.lower())
    if lw in SMALL:
        return SMALL[lw]
    if lw.isdigit():
        return lw
    if re.fullmatch(r"[a-z]+", lw) and V.get(lw, 0) >= COMMON:
        return lw
    near = 1 if len(lw) <= 4 else 2
    import math
    sc = [(difflib.SequenceMatcher(None, lw, v).ratio(), v) for v in V if V[v] >= COMMON and abs(len(v) - len(lw)) <= near]
    sc = [(r + .02 * math.log10(V[v]), v) for r, v in sc if r >= .7]      # the nearer, then the commoner
    return max(sc)[1] if sc else lw


def sub_name(t, V, known=None):
    """'Subcommittee on Soil Conservation and Forestry' from 'SWBCOMMITTH ON SOIL CONSEUVATiON AND FORESTRY'
    (RULES 5): the word after SUBCOMMITTEE "on" (or "No." before a number); each word put right; then the Digest's
    form of the name where one reads as it at .85."""
    t = re.sub(r"\(\s*[Cc]on\w*\s*\)", "", t)
    toks = re.findall(r"[A-Za-z0-9©$'&-]+|[.,()]", t)
    out = []
    for k, w in enumerate(toks):
        if re.fullmatch(r"[.,()]", w):
            out.append(w)
            continue
        if is_sub(w) and len(w) >= 9:
            out.append("subcommittee")
            continue
        if out and out[-1] == "subcommittee" and len(letters(w)) <= 4 and letters(w) not in ("to", "for"):
            nxt = next((x for x in toks[k + 1:] if not re.fullmatch(r"[.,()]", x)), "")
            out.append("No." if re.fullmatch(r"[0-9IlTS§]{1,2}", nxt) else "on")
            continue
        if out and out[-1] == "No." and re.fullmatch(r"[0-9IlTS§]{1,2}", w):
            out.append(w.translate(str.maketrans("IlTS§", "11755")))
            continue
        if w == "&":
            out.append("and")
            continue
        out.append(fix_word(w.replace("©", "o").replace("$", "s"), V))
    s = " ".join(out)
    s = re.sub(r"\s+([.,)])", r"\1", s).replace("( ", "(").replace("No.. ", "No. ").replace("No. .", "No.")
    s = re.sub(r"\s+", " ", s).strip(" -")
    words = s.split(" ")
    res = []
    for i, w in enumerate(words):
        if w.startswith("No.") or (i and w in LOWER):
            res.append(w)
        else:
            res.append("-".join(p[:1].upper() + p[1:] for p in w.split("-")))
    name = " ".join(res)
    if known:
        best, score = None, 0
        for f, n in known.most_common():
            r = max(difflib.SequenceMatcher(None, letters(name), letters(f)).ratio(),
                    difflib.SequenceMatcher(None, letters(t), letters(f)).ratio())
            if r > score + .001:
                best, score = f, r
        if best and score >= .9 and "No." not in name and "No." not in best and re.match(r"(?i)(?:special |select |permanent |general |ad hoc )*subcommittee",
                                                best):
            return best
    return name


# ---------------------------------------------------------------- the members (RULES 4)

def surname(n):
    return re.sub(r"\s*\([^)]*\)", "", n).split(",")[0].strip()


STAFF = re.compile(r"\b(?:Prof\.?|Staff|Mbr\W?|NSOB|OSOB|OHOB|NHOB|Chf\.|Chief|Clerk|Asst\.?|Counsel|Secy\.?|"
                   r"Consultant|CAPITOL|Ext\.|Bldg\.)(?=\W|$)")


def tokens(seg):
    """'Holland, Tolmodge, Young (Ohio), and Neuberger.' -> ['Holland', 'Tolmodge', 'Young (Ohio)', 'Neuberger']."""
    seg = re.sub(r"[\\^*†‡§|]+", "", seg)
    m = STAFF.search(seg)
    if m:                                    # the staff's table beside the line: not members
        seg = seg[:m.start()]
        seg = re.sub(r"\s+[A-Z][a-z]+,?\s+[A-Z][a-z]+(?:\s+[A-Z]\.)?,?\s*$", "", seg) if not seg.rstrip().endswith(",") else seg
    seg = re.sub(r"(?<=[a-z]{3})\.\s+(?=[A-Z][a-z])", ", ", seg)          # 'Hayden. Hill': the OCR's stop a comma
    seg = re.sub(r"\s*/\s*", ", ", seg)                                   # 'Hayden/ Rusself/ McClellan'
    seg = re.sub(r"\.$", "", seg.strip())
    out, depth, cur = [], 0, ""
    for ch_ in seg:
        if ch_ == "(":
            depth += 1
        elif ch_ == ")":
            depth = max(0, depth - 1)
        if ch_ == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch_
    out.append(cur)
    res = []
    for x in out:
        for y in re.split(r"\s+(?:and|ond|aud|rrnd|und|anrl)\s+|\s+&\s+", x.strip()):
            y = re.sub(r"^and\s+|\s+and$", "", y.strip().strip(" .;:")).strip(" .;:")
            if y and re.search(r"[A-Za-z]{2}", y) and y.lower() not in ("and", "ond", "aid", "vacancy", "vacant"):
                res.append(y)
    return res


def state_of(paren):
    k = re.sub(r"[^a-z]", "", paren.lower())
    return ABBR.get(k)


def match(tok, pool, side, roster):
    """The member a token names (RULES 4): (member, check or None)."""
    m = re.match(r"^(.+?)\s*\(([^)]*)\)?\s*$", tok)
    name, st = (m.group(1), state_of(m.group(2))) if m else (tok, None)
    name = re.sub(r"^(?:Mr|Mrs|Miss|Rep|Sen)\.?\s+", "", name).strip()
    w = store.fold(name).replace(" ", "")
    if not w:
        return None, f"unread: {tok}"

    def scored(cands):
        out = []
        for x in cands:
            s_ = store.fold(surname(x["name"])).replace(" ", "")
            r = difflib.SequenceMatcher(None, w, s_).ratio()
            if r >= (.65 if len(s_) <= 4 else .7):
                out.append((r, x))
        return out
    for cands, how in ((pool, None), (roster, "not of the parent committee")):
        sc = scored(cands)
        if not sc:
            continue
        top = max(r for r, _ in sc)
        best = [x for r, x in sc if r == top]
        if len({x.get("bio") or x["name"] for x in best}) > 1 and side:
            same = [x for x in best if x.get("col") == side]
            best = same or best
        if len({x.get("bio") or x["name"] for x in best}) > 1 and st:
            best = [x for x in best if x["st"] == st] or best
        if len({x.get("bio") or x["name"] for x in best}) > 1:
            return None, f"two of the name: {tok}"
        return best[0], (f"{how}: {tok}" if how else (f"read as {surname(best[0]['name'])}: {tok}" if top < .86 else None))
    return None, f"no member of the name: {tok}"


# ---------------------------------------------------------------- one edition

def parse(c, ed, pg, nums, names, members, rosters, V):
    out, comm, sub, last = {}, None, None, None
    seq = [(leaf, x, y, t) for leaf, lines in enumerate(pg, 1) for x, y, t in lines]
    i = 0

    def close():
        nonlocal sub
        if sub and comm and sub["members"]:       # a heading with no members under it is no subcommittee
            out.setdefault(comm["ch"], {}).setdefault(comm["code"], []).append(sub)
        sub = None
    while i < len(seq):
        leaf, x, y, t = seq[i]
        i += 1
        if capsy(t) and not maj_line(t):
            cn = committee_name(t, names)
            if cn and not re.search(r"(?i)\(\s*c\w*n\w*\s*\)?", t):
                close()
                comm = {"code": cn[0], "ch": cn[1], "name": cn[2], "full": None}
                last = None
                continue
            if cn:                    # '(Continued)' over the committee's later pages
                continue
            if comm and is_sub(t):
                if re.search(r"(?i)[(-]\s*c\w*n\w*\s*\)?", t) and sub:
                    continue
                if re.search(r"(?i)SUBCOMM\w*ES\b|SENATOR|\bRE[PF]\.|STAFFS|REPRESENTATIVE|\bASS\w{0,3}N\w*|"
                             r"COMM\w* A\w{2} SU", t) or \
                        re.match(r"^\W*AND\b", t):
                    continue      # the members' assignments pages, a running head: not a subcommittee
                close()
                head = t
                # a heading run over two lines: '... PRODUCTION, MARKETING.' / 'AND STABILIZATION OF PRICES'
                while i < len(seq) and capsy(seq[i][3]) and not maj_line(seq[i][3]) and not is_sub(seq[i][3]) and \
                        not committee_name(seq[i][3], names) and seq[i][1] - y < 140 and \
                        not re.search(r"(?i)STAFF|CAPITOL|EXT\b|OSOB|NSOB|OHOB|NHOB", seq[i][3]):
                    head += " " + seq[i][3]
                    y = seq[i][1]
                    i += 1
                sub = {"printed": re.sub(r"\s+", " ", head).strip(), "leaf": leaf, "page": nums.get(leaf),
                       "chair": None, "members": []}
                continue
            continue
        if comm is None:
            continue
        mm = maj_line(t)
        if mm:
            side, n, end = mm
            body = t[end:]
            # the line runs on over the lines under it (RULES 3): to its stop, or to its printed count of names
            j = i
            while not re.search(r"\.\s*$", body.strip()) and j < len(seq) and seq[j][0] == leaf and \
                    seq[j][1] < x + 600 and seq[j][2] - y < 130 and not maj_line(seq[j][3]) \
                    and not capsy(seq[j][3]) and not (n and len(tokens(re.sub(r"^[^A-Z]*", "", body))) >= n + 1) \
                    and not STAFF.search(seq[j][3]) and not re.match(r"^[A-Z][a-z]+, [A-Z][a-z]+ [A-Z]\.?,?$", seq[j][3]):
                nxt = seq[j][3].strip()
                body = body.rstrip()
                body = body[:-1] + nxt if re.search(r"[A-Za-z][¬-]$", body) else body + " " + nxt
                y = seq[j][1]
                j += 1
            i = j
            mn = re.search(r"\bM\W?I\W?N\W?O\W?R\W?I\W?T\W?Y\b", body)
            if side == "maj" and mn:      # the MINORITY line read into the same line: its own line, next
                seq.insert(i, (leaf, x, y, body[mn.start():]))
                body = body[:mn.start()]
            ch_words = re.findall(r"\b(Senators?|Representatives?|Reps?\.|Rep|Sen\.|Messrs\.)\s", body)
            if comm["ch"] != "j" and ch_words:
                # the chamber the line's members sit in (RULES 2): the committee of that name in that chamber
                want = "s" if ch_words[0].startswith("Sen") else "h"
                if want != comm["ch"]:
                    alt = [n_ for n_ in names if n_[2] == comm["name"] and n_[1] == want]
                    if alt:
                        comm.update(code=alt[0][0], ch=want)
            if comm["full"] is None:
                comm["full"] = True       # the full committee's own lines
                if sub is None:
                    continue
            if sub is None:
                continue
            segs = re.split(r"\b(Sen[a-z]{3,6}s?|Rep[a-z]{5,12}s?|Reps?\.|Rep\b|Sen\.)\s+", body)
            cur_ch = comm["ch"] if comm["ch"] != "j" else None
            names_ = []
            pre = segs[0]
            if pre.strip(" .,;:)") and not re.search(r"[A-Za-z]{3}", pre.split(")")[-1] if ")" in pre else ""):
                pass
            for k in range(1, len(segs), 2):
                cur_ch = "s" if segs[k].startswith("Sen") else "h"
                names_ += [(cur_ch, tk) for tk in tokens(segs[k + 1])]
            if len(segs) == 1:
                tail = re.sub(r"^[^A-Za-z]*\)?\s*", "", pre)
                names_ = [(cur_ch or "s", tk) for tk in tokens(tail)]
            col = "D" if side == "maj" else "R"
            got = []
            split = []
            for chm, tk in names_:        # 'Patman Reuss': two surnames the OCR ran together, each a member
                ws_ = tk.split()
                pool = members.get((comm["code"], chm), [])
                if len(ws_) == 2 and all(re.fullmatch(r"[A-Z][a-z'’-]{3,}", w_) for w_ in ws_) and all(
                        any(difflib.SequenceMatcher(None, store.fold(w_), store.fold(surname(m_["name"]))).ratio()
                            >= .8 for m_ in pool) for w_ in ws_):
                    split += [(chm, w_) for w_ in ws_]
                else:
                    split.append((chm, tk))
            names_ = split
            for chm, tk in names_:
                pool = [m_ for m_ in members.get((comm["code"], chm), [])]
                m_, why = match(tk, pool, col, rosters[chm])
                rec = {"ch": chm} if comm["ch"] == "j" else {}
                if m_:
                    rec.update({k_: m_[k_] for k_ in ("bio", "name", "p", "st", "seat") if m_.get(k_) is not None})
                else:
                    rec.update({"name": tk})
                rec["side"] = side
                rec["printed"] = tk
                if why:
                    rec["check"] = why
                got.append(rec)
            sub["members"] += got
            pc = sub.setdefault("printed_counts", {})       # a joint committee's two lines a side: summed
            pc[side] = None if n is None or (side in pc and pc[side] is None) else (pc.get(side) or 0) + n
            continue
        if sub is not None and not sub["members"] and re.search(r"(?i)c\W?h?\W?\w{0,3}a?\w{0,2}i?\w{0,2}rm|"
                                                                   r"\([DR]\W", t):
            # the chairman's line: 'James O. Easflaiid (P. Miss.), Chairmcsn'
            nm = re.split(r"\s*[({\[]|\s+C[DR]\.|,\s*C\w{2,}|\s+C\w{0,3}a\w{0,3}rm", t)[0].strip(" ,.")
            nm = re.sub(r"^(?:Senator|Sen\.|Rep\.|Representative)\s+", "", nm)
            if re.search(r"[A-Za-z]{3}", nm):
                sub["chair_printed"] = nm
    close()
    return out


def finish(c, data, rosters):
    """The chairman marked among the members (RULES 4), ranks, the count checks (RULES 3)."""
    for ch, comms in data.items():
        for code, subs in comms.items():
            for s in subs:
                ms = s["members"]
                cp = s.pop("chair_printed", None)
                if cp:
                    sur = store.fold(cp.split()[-1]) if cp.split() else ""
                    best, score = None, 0
                    for m in ms:
                        if m["side"] != "maj":
                            continue
                        r = difflib.SequenceMatcher(None, sur, store.fold(surname(m["name"]))).ratio()
                        if r > score:
                            best, score = m, r
                    if best and score >= .45:
                        best["role"] = "chair"
                    else:
                        s.setdefault("check", []).append(f"chairman not among the members: {cp}")
                    s["chair"] = cp
                else:
                    s.pop("chair", None)
                rank = {}
                for m in ms:
                    k = (m.get("ch", ""), m["side"])
                    rank[k] = rank.get(k, 0) + 1
                    m["rank"] = rank[k]
                pc = s.pop("printed_counts", {})
                for side in ("maj", "min"):
                    n = sum(1 for m in ms if m["side"] == side)
                    if pc.get(side) is not None and pc[side] != n and not (s.get("joint_split")):
                        s.setdefault("check", []).append(f"{side}: {n} names read, the count printed {pc[side]}")
                if pc:
                    s["counts"] = {k: v for k, v in pc.items() if v is not None}
                if any(m.get("check") for m in ms):
                    s.setdefault("check", []).append("names: " + "; ".join(m["check"] for m in ms if m.get("check")))
                if s.get("check"):
                    s["check"] = " ".join(s["check"]) if isinstance(s["check"], list) else s["check"]


def main(cache):
    os.makedirs(cache, exist_ok=True)
    cm = store.load_yaml(os.path.join(ROOT, "congress", "committees.yaml")) or {}
    cd = store.load_yaml(os.path.join(ROOT, "congress", "committees-cdir.yaml")) or {}
    rows = digest_rows()
    V, F = vocab(rows), forms(rows)
    data, eds = {}, {}
    for c, ed in sorted(EDITIONS.items()):
        f = fetch(ed, cache)
        pg = pages(f["_djvu.xml"])
        nums = {p["leafNum"]: p["pageNumber"] for p in json.load(open(f["_page_numbers.json"]))["pages"]
                if p.get("pageNumber")}
        # the committee list and each committee's members, any time in the Congress
        names, members = [], {}
        for ch in ("h", "s"):
            for code, ms in ((cm.get("congress") or {}).get(c, {}).get(ch, {}).get("committees") or {}).items():
                nm = next(x["name"] for x in cm["committees"] if x["code"] == code)
                names.append((code, ch, nm))
                members[(code, ch)] = [dict(m, col=(m["p"] if m["p"] in ("D", "R") else "D")) for m in ms]
        for ch in ("s", "h", "j"):
            for code, r in ((cd.get("congress") or {}).get(c, {}).get(ch) or {}).items():
                names.append((code, ch, r["name"]))
                for m in r["members"]:
                    members.setdefault((code, m["ch"]), []).append(dict(m, col=m["p"] if m["p"] in ("D", "R") else "D"))
        rosters = {}
        roster = store.load_yaml(os.path.join(ROOT, "congress", f"{c}.yaml")) or {}
        for ch, key in (("s", "senate"), ("h", "house")):
            rosters[ch] = [{"bio": r["bio"], "name": r["name"], "p": r["party"], "st": r["st"],
                            "seat": r["cl"] if ch == "s" else r["d"], "col": r["party"] if r["party"] in ("D", "R") else "D"}
                           for r in roster.get(key) or [] if r.get("bio")]
        d = parse(c, ed, pg, nums, names, members, rosters, V)
        finish(c, d, rosters)
        for ch in d:
            for code in d[ch]:
                last = 0
                for s in d[ch][code]:
                    s["name"] = sub_name(s["printed"], V, F.get((ch, code)))
                    s["url"] = LEAF.format(id=ed["id"], n=s["leaf"] - 1)
                    # a numbered subcommittee whose number the OCR lost: the one after the last (RULES 5)
                    m = re.match(r"^Subcommittee\s+No\.\s*(\S*)(.*)$", s["name"]) or \
                        re.match(r"^Subcommittee\s+(?:On\.|N)\s*(\S*)()$", s["name"])
                    if m:
                        num = int(m.group(1)) if m.group(1).isdigit() and int(m.group(1)) > last else last + 1
                        if not (m.group(1).isdigit() and int(m.group(1)) == num):
                            s.setdefault("check", "")
                            s["check"] = (s["check"] + " " if s["check"] else "") + f"number placed by order: {num}"
                        last = num
                        s["name"] = f"Subcommittee No. {num}" + (m.group(2) if m.group(2).strip()[:2] == "on" else "")
                    odd = [w for w in re.findall(r"[A-Za-z]+", s["name"]) if w.lower() not in V and
                           w.lower() not in SMALL and w not in ("No",)]
                    if odd:
                        s["check"] = ((s.get("check") or "") + " name not settled: " + " ".join(odd)).strip()
        data[c] = d
        eds[c] = {"title": ed["title"], "id": ed["id"], "url": f"https://archive.org/details/{ed['id']}"}
    write(data, eds)


def flow(d):
    return yaml.safe_dump(d, default_flow_style=True, allow_unicode=True, width=10 ** 6, sort_keys=False).strip()


def write(data, eds):
    L = ["# Generated by tools/congress/make_subcommittees.py from the Congressional Staff Directory (archive.org's scans",
         "# of the 1961 and 1963 editions); never edit by hand: change the script's rules and rerun.",
         "# Schema:",
         "#   editions: <NN>: the edition read (title, id, url).",
         "#   congress: <NN>: <s|h|j>: <committee code>: [subcommittees in the order printed]: name (put right, RULES 5),",
         "#     printed (the heading as the OCR reads it), chair (the chairman's line as read), counts (maj, min: as",
         "#     printed), members (in the order printed: bio, name, p, st, seat (the rosters'), ch (a joint committee's),",
         "#     side (maj, min), printed (as read), role (chair), rank (within side, and chamber), check), page (the",
         "#     printed page), leaf, url (the leaf on archive.org), check (what the rules could not settle).",
         ""]
    L.append("editions:")
    for c, e in sorted(eds.items()):
        L.append(f"  {c}: " + flow(e))
    L.append("congress:")
    for c in sorted(data):
        L.append(f"  {c}:")
        for ch in ("s", "h", "j"):
            if ch not in data[c]:
                continue
            L.append(f"    {ch}:")
            for code in sorted(data[c][ch], key=str):
                if not data[c][ch][code]:
                    continue
                L.append(f"      {code}:")
                for s in data[c][ch][code]:
                    ms = s.pop("members")
                    head = {k: s[k] for k in ("name", "printed", "chair", "counts", "page", "leaf", "url", "check")
                            if s.get(k) is not None}
                    for n_, k in enumerate(head):
                        L.append(("        - " if n_ == 0 else "          ") + flow({k: head[k]})[1:-1])
                    L.append("          members:")
                    for m in ms:
                        L.append("            - " + flow(m))
    path = os.path.join(ROOT, "congress", "subcommittees.yaml")
    open(path + ".tmp", "w", encoding="utf-8").write("\n".join(L) + "\n")
    os.replace(path + ".tmp", path)
    yaml.safe_load(open(path, encoding="utf-8"))
    print("wrote", path)


if __name__ == "__main__":
    main(sys.argv[1])
