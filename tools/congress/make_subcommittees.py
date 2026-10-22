"""The subcommittees of the 87th and 88th Congresses, with their chairmen and members, from the Congressional Staff
Directory: congress/subcommittees.yaml.

Usage: python3 -I tools/congress/make_subcommittees.py CACHE_DIR
  CACHE_DIR   where each edition's page text is kept (<id>.djvu.xml and <id>.pages.json, archive.org's OCR of the
              scan and its page numbers); fetched if missing
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
    congress/committees-cdir.yaml's select, special and joint ones) at .8 of its letters; a subcommittee's when it
    holds "SUBCOMMITTEE" so read. "(Continued)" goes on with the one before. A subcommittee's heading run over two
    lines is one.
 2. The chamber: the full committee's own MAJORITY line ("Senators", "Representatives"); a joint committee's
    members each by the word before them.
 3. A MAJORITY or MINORITY line runs on over the indented lines under it to its stop; a word broken at the line's end
    is joined. Its printed count ("(5 D.)") is kept; where the names read do not make it, the subcommittee carries
    "check".
 4. A name is the member of the parent committee (any time in the Congress; for a joint committee, of his chamber)
    whose surname reads most like it, at .7 of its letters, of the line's party (MAJORITY, the Democrats in these
    Congresses), the State in parentheses settling two of a surname; else, of the chamber's roster at the opening,
    with "check". The chairman: the member of the subcommittee whose surname his line gives.
 5. The subcommittee's name: its heading, each word put right against the words the Directories and the Digest print
    (VOCAB: a word not found at .7 of its letters stays as read), in title case ("Subcommittee on Soil Conservation and
    Forestry").
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
         "amb": "and", "amd": "and", "ano": "and", "amp": "and", "anp": "and", "and": "and", "the": "the", "to": "to",
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
        out.append(sorted(lines, key=lambda l: (l[1], l[0])))
    return out


def letters(t):
    return re.sub(r"[^a-z]", "", t.lower())


def capsy(t):
    ls = re.sub(r"[^A-Za-z]", "", t)
    return len(ls) >= 6 and sum(c.isupper() for c in ls) / len(ls) > .72


def is_sub(t):
    w = letters(t)
    return any(difflib.SequenceMatcher(None, w[i:i + 12], "subcommittee").ratio() >= .7
               for i in range(0, max(1, len(w) - 11)))


MAJ = re.compile(r"^\W*([MA4]\W?[A4]?\W?J|M\W?I\W?N)\w{2,6}\W*\s*\(?\s*(\d+)?\s*([DR])?", re.I)


def maj_line(t):
    """'maj' or 'min' and the printed count, for a MAJORITY or MINORITY line ('A4AJORITY;(3D.)')."""
    m = re.match(r"^\W*([A-Za-z4]{5,9})\s*[:;.,]?\s*(?:\(\s*(\d+)\s*([DR])?\W*\)?)?", t)
    if not m:
        return None
    w = letters(m.group(1).replace("4", "m"))
    for k, ref in (("maj", "majority"), ("min", "minority")):
        if difflib.SequenceMatcher(None, w, ref).ratio() >= .75:
            return k, int(m.group(2)) if m.group(2) else None, m.end()
    return None


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
            if r > score:
                best, score = (code, ch, name), r
    return best if score >= .8 else None


def vocab():
    """VOCAB (RULES 5): the words of the committee lists and of the Digest's subcommittees, the commoner first."""
    from collections import Counter
    c = Counter()
    for f in sorted(os.listdir(os.path.join(ROOT, "daybook", "committees"))):
        if not re.match(r"\d{4}-\d{2}\.yaml$", f):
            continue
        for x in (store.load_yaml(os.path.join(ROOT, "daybook", "committees", f)) or {}).get("docs") or []:
            for t in (x.get("sub"), x.get("name"), x.get("heading")):
                for w in re.findall(r"[A-Za-z]{3,}", t or ""):
                    c[w.lower()] += 1
    return c


def fix_word(w, V):
    lw = re.sub(r"[^a-z0-9]", "", w.lower())
    if lw in SMALL:
        return SMALL[lw]
    if lw.isdigit():
        return lw
    if re.fullmatch(r"[a-z]+", lw) and V.get(lw, 0) >= 2:
        return lw
    best = difflib.get_close_matches(lw, [v for v in V if V[v] >= 2 and abs(len(v) - len(lw)) <= 2], 1, .7)
    return best[0] if best else lw


def sub_name(t, V):
    """'Subcommittee on Soil Conservation and Forestry' from 'SWBCOMMITTH ON SOIL CONSEUVATiON AND FORESTRY'."""
    t = re.sub(r"\(\s*[Cc]on\w*\s*\)", "", t)
    toks = re.findall(r"[A-Za-z0-9©$'&-]+|[.,()]", t)
    out = []
    for w in toks:
        if re.fullmatch(r"[.,()]", w):
            out.append(w)
            continue
        if is_sub(w) and len(w) >= 9:
            out.append("subcommittee")
            continue
        if w == "&":
            out.append("and")
            continue
        out.append(fix_word(w.replace("©", "o").replace("$", "s"), V))
    s = " ".join(out)
    s = re.sub(r"\s+([.,)])", r"\1", s).replace("( ", "(")
    s = re.sub(r"\bno\.?\s+(\d)", r"No. \1", s, flags=re.I)
    words = s.split(" ")
    res = []
    for i, w in enumerate(words):
        if w.startswith("No."):
            res.append(w)
        elif i and w in LOWER:
            res.append(w)
        else:
            res.append("-".join(p[:1].upper() + p[1:] for p in w.split("-")))
    return " ".join(res).replace("Subcommittee No. ", "Subcommittee No. ")


# ---------------------------------------------------------------- the members (RULES 4)

def surname(n):
    return re.sub(r"\s*\([^)]*\)", "", n).split(",")[0].strip()


def tokens(seg):
    """'Holland, Tolmodge, Young (Ohio), and Neuberger.' -> ['Holland', 'Tolmodge', 'Young (Ohio)', 'Neuberger']."""
    seg = re.sub(r"[\\^*†‡§|]+", "", seg)
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
        for y in re.split(r"\s+and\s+|\s+&\s+", x.strip()):
            y = re.sub(r"^and\s+", "", y.strip()).strip(" .;:")
            if y and re.search(r"[A-Za-z]{2}", y):
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
            if r >= .7:
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
        if sub and comm:
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
                if re.search(r"(?i)\(\s*c\w*n\w*\s*\)?", t) and sub:
                    continue
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
            # the line runs on over the indented lines under it (RULES 3)
            j = i
            while not re.search(r"\.\s*$", body.strip()) and j < len(seq) and seq[j][0] == leaf and \
                    seq[j][2] > x + 60 and seq[j][2] < x + 600 and seq[j][1] - y < 220 and not maj_line(seq[j][3]) \
                    and not capsy(seq[j][3]):
                nxt = seq[j][3].strip()
                body = body.rstrip()
                body = body[:-1] + nxt if re.search(r"[A-Za-z][¬-]$", body) else body + " " + nxt
                y = seq[j][1]
                j += 1
            i = j
            ch_words = re.findall(r"\b(Senators?|Representatives?|Reps?\.|Rep|Sen\.|Messrs\.)\s", body)
            if comm["ch"] != "j" and comm["full"] is None:
                comm["full"] = True       # the full committee's own lines: its chamber (RULES 2)
                if ch_words:
                    w0 = ch_words[0]
                    want = "s" if w0.startswith("Sen") else "h"
                    if want != comm["ch"]:
                        alt = [n_ for n_ in names if n_[2] == comm["name"] and n_[1] == want]
                        if alt:
                            comm.update(code=alt[0][0], ch=want)
                if sub is None:
                    continue
            if sub is None:
                continue
            segs = re.split(r"\b(Senators?|Representatives?|Reps?\.|Rep\b|Sen\.)\s+", body)
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
            sub.setdefault("printed_counts", {})[side] = n
            continue
        if sub is not None and not sub["members"] and re.search(r"(?i)c\W?h?\W?\w{0,3}a?\w{0,2}i?\w{0,2}rm|"
                                                                   r"\([DR]\W", t):
            # the chairman's line: 'James O. Easflaiid (P. Miss.), Chairmcsn'
            nm = re.split(r"\s*\(|,\s*C\w{2,}", t)[0].strip(" ,.")
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
                    if best and score >= .6:
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
    V = vocab()
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
                for s in d[ch][code]:
                    s["name"] = sub_name(s["printed"], V)
                    s["url"] = LEAF.format(id=ed["id"], n=s["leaf"] - 1)
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
