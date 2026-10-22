"""The select, special and joint committees of each Congress, 87th-93rd, from the Congressional Directory:
congress/committees-cdir.yaml.

Usage: python3 -I tools/congress/make_cdir_committees.py CACHE_DIR LEGISLATORS_DIR
  CACHE_DIR        where each edition's text is kept: <edition>.layout.txt (pdftotext -layout of govinfo's PDF, one
                   page a form feed); fetched and made if missing (the PDF, 130-200 MB, deleted after)
  LEGISLATORS_DIR  legislators-historical.yaml and legislators-current.yaml of unitedstates/congress-legislators (the
                   rosters' source), to join the members to the rosters
Run once; rerun after changing the rules here; never edit the output. The build needs no network.

The editions (EDITIONS): each Congress's first-session Directory on govinfo (CDIR-<date>), a scan with an OCR text
layer, read Oct. 22, 2026. What they print (read page by page):
  - "Select and Special Committees of the Senate", "... of the House", and "Congressional Joint Committees,
    Commissions, and Boards": each committee under its name, the law creating it, its room, then "Chairman.--", "Vice
    Chairman.--" (or "Cochairman.--") and the members, one a line, "John J. Sparkman, Senator from Alabama.", the
    majority first, then the minority; then its staff. No party is printed: the party is the roster's.
  - No subcommittee in any edition from 1961 to Mar. 1971. From Dec. 3, 1971 the Directory prints under each standing
    committee its subcommittees, each with its chairman and ranking minority member only, in two columns the OCR runs
    together; not read here (the subcommittees: tools/congress/make_subcommittees.py).
RULES
 1. A committee: a heading in the select and special or the joint section whose name begins "Select", "Special",
    "Permanent Select" or "Joint" (the Joint Economic Committee too); not the party committees (Policy, Steering,
    Legislative Review), the House's housekeeping committees (Restaurant, Recording Studio, Beauty Shop, Parking), nor
    the commissions and boards. A heading run over two lines is one.
 2. A member: a line "Name, Senator from State." ("Representative", "Delegate", "Resident Commissioner"), a line run on
    joined; his role from the prefix (Chairman, Vice Chairman, Cochairman); "ex officio" kept; one named twice (the
    cochairmen over the list) once. The margin's marks the OCR sets before or after a line are dropped. A member named
    by an office alone ("Douglas Dillon, Secretary of the Treasury.") is kept apart (others). The members end at the
    committee's first staff line (a prefix not a member's role) or the next heading.
 3. The member is joined to congress-legislators by surname, chamber and State (the given names where two of the
    surname sat for the State; a given name spelled out first, "J. William Stanton"), among the roster's members at
    the opening and those serving on the edition's date (congress-legislators omits some last terms: Dirksen's of
    1969, Prouty's of 1971); the surname as printed, else within the OCR's misreading of a letter or two
    ("Kluezynski", "Brynes"), the State's likewise ("Kentueky", "Towa"). His seat and party are the roster's at the
    opening, else his term's (a successor). The ranks: the order printed within his chamber and party.
 4. Codes: the committee as the hearings calendar (tools/daybook/make_committees.py, COMMITTEES and code_of) names
    it, "s.special-committee-on-aging", "j.atomic-energy"; the Directory's longer forms answer to it (ALIAS).
 5. The page: the printed folio of the PDF page, read from the page's running head or foot and placed by its
    neighbours where the OCR lost it.
"""
import datetime
import difflib
import os
import re
import subprocess
import sys
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bib import store  # noqa: E402

EDITIONS = {87: "1961-04-01", 88: "1963-03-01", 89: "1965-03-01", 90: "1967-02-28", 91: "1969-03-01",
            92: "1971-03-10", 93: "1973-03-10"}
PDF = "https://www.govinfo.gov/content/pkg/CDIR-{e}/pdf/CDIR-{e}.pdf"
DETAILS = "https://www.govinfo.gov/app/details/CDIR-{e}"
UA = {"User-Agent": "bib-congress (https://impending2223.github.io/bib/)"}
STATES = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
          "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
          "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
          "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
          "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
          "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
          "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
          "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
          "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
          "Wisconsin": "WI", "Wyoming": "WY", "Puerto Rico": "PR", "District of Columbia": "DC", "Guam": "GU",
          "Virgin Islands": "VI"}
# the Directory's longer or later forms of a committee's name, to the name the hearings calendar gives it
ALIAS = [(r"Select Committee To Conduct a Study and Investigation of the Problems of Small Business|"
          r"Permanent Select Committee on Small Business", "Select Committee on Small Business"),
         (r"Select Committee on Government Research", "Select Committee on Government Research"),
         (r"Joint Committee on (the )?Organization of (the )?Congress", "Joint Committee on the Organization of the Congress"),
         (r"Joint Committee on Navajo-Hopi Indian Administration", "Joint Committee on Navajo-Hopi Indian Administration")]
EXCLUDE = re.compile(r"Policy Committee|Steering|Legislative Review|Restaurant|Recording|Beauty|Parking|Conference|"
                     r"Caucus")
COMMITTEE = re.compile(r"^(?:Select|Special|Permanent Select|Joint)\b.*\bCommittee\b|^Joint Economic Committee")
MEMBER = re.compile(r"^(?:(?P<role>[A-Z][A-Za-z -]{2,22}?)\s*[.,:]?\s*[—–-]+\s*)?(?P<name>[A-Z][^,]*?(?:,\s*(?:Jr|Sr)\.?|"
                    r",\s*(?:II|III|IV|2d|3d))?),\s*(?P<what>Senator|Representative|Delegate|Resident Commissioner)"
                    r"\s+(?:from|for)\s+(?:the\s+)?(?P<state>[A-Z][A-Za-z. ]+?)(?:,\s*(?P<ex>ex officio))?[.,]?\s*$")
ROLE = {"chairman": "chair", "vice chairman": "vice", "cochairman": "cochair", "cochairmen": "cochair",
        "co-chairman": "cochair"}
HEADS = {"ss": r"SELECT\s+AND\s+SPECIAL\s+COMMITTEES\s+OF\s+THE\s+SENATE",
         "sh": r"SELECT\s+AND\s+SPECIAL\s+COMMITTEES\s+OF\s+THE\s+HOUSE",
         "j": r"CONGRESSIONAL\s+JOINT\s+COMMITTEES",
         "end": r"STAFFS\s+OF\s+(SENATE|HOUSE)\s+COMMITTEES|COMMITTEE\s+ASSIGNMENTS|ASSIGNMENTS\s+OF\s+SENATORS|"
                r"OFFICERS\s+OF\s+UNITED\s+STATES\s+GROUP|STANDING\s+COMMITTEES\s+OF\s+THE"}

sys.path.insert(0, os.path.join(ROOT, "tools", "daybook"))
import make_committees as DAYBOOK  # noqa: E402  (the hearings calendar's committee names and codes)


def fetch(e, cache):
    p = os.path.join(cache, f"{e}.layout.txt")
    if os.path.exists(p):
        return p
    pdf = os.path.join(cache, f"{e}.pdf")
    if not os.path.exists(pdf):
        with urllib.request.urlopen(urllib.request.Request(PDF.format(e=e), headers=UA), timeout=900) as r, \
                open(pdf + ".part", "wb") as f:
            while True:
                b = r.read(1 << 20)
                if not b:
                    break
                f.write(b)
        os.rename(pdf + ".part", pdf)
    subprocess.run(["pdftotext", "-layout", pdf, p + ".part"], check=True)
    os.rename(p + ".part", p)
    os.remove(pdf)
    return p


def norm(t):
    t = t.replace("’", "'").replace("“", '"').replace("”", '"')
    t = re.sub(r"[|{}¥§]", " ", t)
    t = re.sub(r"\s+", " ", t).strip(" :;!'")
    # the margin's marks the OCR set before a line ('il Thomas G. Morris', ': Richard B. Russell'): not 'A. Willis'
    return re.sub(r"^(?:(?:[a-z]{1,3}|[^\w\s]+|[A-Z])\s+)+(?=[A-Z][a-z.])", "", t)


def folios(pages):
    """{pdf page: printed page} (RULES 5): a number alone at the head or foot of the page, or before or after
    'Congressional Directory' or a section's running title; the offset agreeing with its neighbours."""
    raw = {}
    for i, p in enumerate(pages, 1):
        ls = [l.strip() for l in p.split("\n") if l.strip()]
        cand = ls[:2] + ls[-2:]
        for l in cand:
            m = re.match(r"^\D{0,6}?(\d{1,4})\s+[A-Z]", l) or re.search(r"[a-z]\s+(\d{1,4})\D{0,4}$", l) or \
                re.fullmatch(r"\D{0,3}(\d{1,4})\D{0,3}", l)
            if m and 0 <= i - int(m.group(1)) <= 80:
                raw[i] = int(m.group(1))
                break
    off = {i: i - f for i, f in raw.items()}
    out = {}
    for i in range(1, len(pages) + 1):
        near = [off[j] for j in range(i - 8, i + 9) if j in off]
        if not near:
            continue
        o = max(set(near), key=lambda x: (near.count(x), -abs(x - off.get(i, x))))
        out[i] = i - o
    return out


def lines_of(pages, kind):
    """The section's lines [(pdf page, text)] from its title to the next section's (HEADS)."""
    out, on = [], False
    for i, p in enumerate(pages, 1):
        for l in p.split("\n"):
            t = norm(l)
            if not t:
                continue
            if re.search(HEADS[kind], t):
                on = True
                continue
            if on and re.search(HEADS["end"], t) and not re.search(HEADS[kind], t):
                return out
            if on and re.search(HEADS["j" if kind != "j" else "ss"], t):
                return out
            if on:
                out.append((i, t))
    return out


def canonical(name, ch):
    for rx, to in ALIAS:
        if re.fullmatch(rx, name):
            return to
    return name


def code(ch, name):
    return DAYBOOK.code_of(ch.upper(), name)


def parse(lines, kind):
    """[{name, printed, ch, pdf, members: [...], others: [...]}] (RULES 1-2)."""
    out, cur, open_ = [], None, False
    i = 0
    while i < len(lines):
        pi, t = lines[i]
        h = re.sub(r"^\W+", "", t)
        h = re.sub(r"^(?:[A-Za-z]{1,2}|\d)\s+(?=(?:Joint|Select|Special|Permanent)\b)", "", h)   # 'B Joint ...'
        h = re.sub(r"\s+(?!(?:of|on|to|an|or|by|in)$)(?:[A-Za-z]{1,2}|\d)$", "", h)   # a stray mark at the end ('Ba')
        h = re.sub(r"\ben\b", "on", h)                          # 'Joint Committee en Navajo-Hopi'
        if (COMMITTEE.match(h) or re.match(r"^(?:Committee on|Commission|Board|House |Senate |Democratic|Republican|"
                                           r"[A-Z][\w-]+(?: [A-Z][\w-]+)* (?:Commission|Board|Fund|Group))\b", h)) \
                and not MEMBER.match(t) and "—" not in t and not re.search(r"\d{2}", h):
            # the heading run over two lines: '... Investigation of the' / 'Problems of Small Business'
            if re.search(r"\b(?:of|the|and|for|on|to)$", h) and i + 1 < len(lines):
                h = h + " " + re.sub(r"^\W+", "", lines[i + 1][1])
                i += 1
            cur = None
            if COMMITTEE.match(h) and not EXCLUDE.search(h):
                ch = {"ss": "s", "sh": "h", "j": "j"}[kind]
                h = re.sub(r"[\s\W]+$", "", h)
                cur = {"printed": h, "name": canonical(h, ch), "ch": ch, "pdf": pi, "members": [], "others": []}
                out.append(cur)
            open_ = True
            i += 1
            continue
        if cur is None:
            i += 1
            continue
        if re.match(r"^Members?\s*:?\s*$", t) or re.match(r"^MEMBERS$", t) or \
                re.match(r"^Members?\s*[—–-]+\s*Continued", t) or re.search(r"\[Vacan\w*\.?\]", t):
            i += 1
            continue
        line = re.sub(r"\.(?:\s+\S{1,3})+$", ".", t)          # stray marks after the line's stop ('Iowa. i')
        # a member's line run on: 'John Sherman Cooper, Senator from' / 'Kentucky.'
        if re.search(r"(?:Senator|Representative|Delegate|Commissioner)(?:\s+(?:from|for))?\s*\w*$", line) and \
                not MEMBER.match(line) and i + 1 < len(lines):
            line = line + " " + lines[i + 1][1]
            i += 1
        m = MEMBER.match(line)
        if m:
            role = (m.group("role") or "").lower()
            role = "cochairman" if role.startswith("coch") else re.sub(r"\bc\w{3,6}rm(a|e)n\b", r"chairm\1n", role)
            x = {"printed": norm(m.group("name")), "what": m.group("what"), "state": m.group("state").strip(),
                 "pdf": pi}
            if role in ROLE:
                x["role"] = ROLE[role]
            elif role:
                x["role_printed"] = role
            if m.group("ex"):
                x["ex_officio"] = True
            if not open_:
                pass
            cur["members"].append(x)
            i += 1
            continue
        mo = re.match(r"^(?:(?:Chairman|Vice Chairman)\s*\.?\s*[—–-]+\s*)?([A-Z][\w.' ]+?),\s+((?:Secretary|Director|"
                      r"Comptroller|Attorney|Postmaster|Chairman|Administrator|Architect|Librarian|Under Secretary)\b"
                      r"[^.]*)\.?$", line)
        if mo and cur["members"] and not re.search(r"\d", line):
            cur["others"].append({"name": mo.group(1).strip(), "office": mo.group(2).strip()})
            i += 1
            continue
        if re.match(r"^[A-Z][A-Za-z ,]+\.?\s*[—–]", t) and not re.match(r"^(?:C\w{3,6}rm[ae]n|Vice|Coch)", t):
            open_ = False          # the staff: the members are over
            cur = None if cur["members"] else cur
        i += 1
    return out


# ---------------------------------------------------------------- the join (RULES 3)

def legislators(path):
    L = []
    for f in ("legislators-historical.yaml", "legislators-current.yaml"):
        L += yaml.load(open(os.path.join(path, f), encoding="utf-8"), Loader=yaml.SafeLoader)
    return L


def roster_name(p):
    n = p["name"]
    first, mid, last, suf, nick = n["first"], n.get("middle"), n["last"], n.get("suffix"), n.get("nickname")
    if mid and first.endswith("."):
        s = f"{last}, {first} {mid}"
        nick = None if nick == mid else nick
    else:
        s = f"{last}, {first}" + (f" {mid[0]}." if mid and not mid.startswith("(") else "")
    if suf:
        s += f", {suf}"
    if nick and nick != first:
        s += f" ({nick})"
    return s


def surname_of(printed):
    t = re.sub(r",?\s*(?:Jr|Sr)\.?$|,?\s+(?:II|III|IV|2d|3d)$", "", printed)
    t = re.sub(r"\([^)]*\)", " ", t)
    return t.split()[-1] if t.split() else t


def given_of(printed):
    t = re.sub(r",?\s*(?:Jr|Sr)\.?$|,?\s+(?:II|III|IV|2d|3d)$", "", printed)
    t = re.sub(r"\([^)]*\)", " ", t)
    return t.split()[:-1]


class Join:
    def __init__(self, L, c, day):
        self.c, self.day = c, day
        self.L = L
        self.roster = store.load_yaml(os.path.join(ROOT, "congress", f"{c}.yaml")) or {}

    def find(self, x):
        """The member's congress-legislators entry: the roster's at the opening first (its seat, chamber, State),
        else one serving on the edition's date; the surname as printed, else within the OCR's misreadings (a
        letter or two: 'Kluezynski'); two of the surname told apart by the given names."""
        typ = "sen" if x["what"] == "Senator" else "rep"
        st = STATES.get(x["state"])
        if not st:          # the OCR's 'Kentueky', 'Towa': the one State it reads most like
            r_, k_ = max((difflib.SequenceMatcher(None, store.fold(k), store.fold(x["state"])).ratio(), k)
                         for k in STATES)
            st = STATES[k_] if r_ >= .7 else None
        if not st:
            return None, "state not read"
        sur = store.fold(surname_of(x["printed"]))
        bio = {p["id"]["bioguide"]: p for p in self.L}
        rows = [r for r in self.roster.get("senate" if typ == "sen" else "house") or []
                if r.get("st") == st and r.get("bio") in bio]
        serving = [p for p in self.L if any(t["type"] == typ and t["state"] == st and
                                            str(t["start"]) <= self.day <= str(t["end"]) for t in p["terms"])]
        pool = list({id(p): p for p in [bio[r["bio"]] for r in rows] + serving}.values())

        def last(p):
            return {store.fold(p["name"]["last"]), store.fold(p["name"]["last"].split()[-1])}
        hits = [p for p in pool if sur in last(p)]
        if not hits:
            hits = [p for p in pool if any(difflib.SequenceMatcher(None, sur, n).ratio() >= .8 for n in last(p))]
        if len(hits) > 1:
            g = [store.fold(w) for w in given_of(x["printed"]) if w.strip(".")]

            def names_of(p):
                return [store.fold(p["name"].get(k) or "") for k in ("first", "middle", "nickname")]
            # a given name spelled out ('J. William Stanton': William), then the first initial
            full = [w for w in g if len(w) > 1]
            h2 = [p for p in hits if full and all(any(n == w or n.startswith(w) for n in names_of(p)) for w in full)]
            if not h2:
                h2 = [p for p in hits if g and names_of(p)[0][:1] == g[0][:1]]
            hits = h2 or hits
        if len(hits) != 1:
            return None, f"{len(hits)} in congress-legislators"
        return hits[0], None

    def seat(self, p, typ):
        rows = self.roster.get("senate" if typ == "sen" else "house") or []
        for r in rows:
            if r.get("bio") == p["id"]["bioguide"]:
                return r["st"], (r["cl"] if typ == "sen" else r["d"]), r["name"], r["party"]
        for t in p["terms"]:
            if t["type"] == typ and str(t["start"]) <= self.day <= str(t["end"]):
                party = {"Democrat": "D", "Republican": "R"}.get(t.get("party"), "I")
                return t["state"], (t.get("class") if typ == "sen" else t.get("district") or 0), roster_name(p), party
        return None


def caucus(p, name):
    from bib.congress import caucused
    cc = caucused({"party": p, "name": name})
    return cc[0] if cc else p


def join_members(cm, J):
    bad = []
    by = {}
    seen = {}
    for x in cm["members"]:
        p, why = J.find(x)
        if p and p["id"]["bioguide"] in seen:      # named again (a cochairman over the members' list): one member
            if x.get("role"):
                seen[p["id"]["bioguide"]].setdefault("role", x["role"])
            continue
        typ = "sen" if x["what"] == "Senator" else "rep"
        y = {}
        if p:
            st, seat, nm, party = J.seat(p, typ)
            y = {"bio": p["id"]["bioguide"], "name": nm, "p": party, "st": st, "seat": seat}
        else:
            bad.append((cm["printed"], x["printed"], x["state"], why))
            y = {"name": x["printed"], "p": "?", "st": STATES.get(x["state"], "?")}
            y["check"] = f"not joined: {why}"
        y["ch"] = "s" if x["what"] == "Senator" else "h"
        if x["what"] in ("Delegate", "Resident Commissioner"):
            y["delegate"] = True
        y["printed"] = x["printed"]
        for k in ("role", "ex_officio"):
            if x.get(k):
                y[k] = x[k]
        side = caucus(y["p"], y["name"]) if y["p"] != "?" else "?"
        key = (y["ch"] if cm["ch"] == "j" else "", side)
        by[key] = by.get(key, 0) + 1
        y["rank"] = by[key]
        y["pdf"] = x["pdf"]
        cm.setdefault("joined", []).append(y)
        if p:
            seen[p["id"]["bioguide"]] = y
    return bad


# ---------------------------------------------------------------- write

def flow(d):
    return yaml.safe_dump(d, default_flow_style=True, allow_unicode=True, width=10 ** 6, sort_keys=False).strip()


def main(cache, legis):
    L = legislators(legis)
    data, used, bad = {}, {}, []
    eds = {}
    for c, e in sorted(EDITIONS.items()):
        pages = open(fetch(e, cache), encoding="utf-8").read().split("\f")
        fol = folios(pages)
        J = Join(L, c, e)
        eds[c] = {"edition": e, "url": PDF.format(e=e)}
        data[c] = {}
        for kind in ("ss", "sh", "j"):
            for cm in parse(lines_of(pages, kind), kind):
                if not cm["members"]:
                    continue
                bad += [(c,) + b for b in join_members(cm, J)]
                k = code(cm["ch"], cm["name"])
                rec = {"name": cm["name"]}
                if cm["printed"] != cm["name"]:
                    rec["printed"] = cm["printed"]
                rec["page"] = fol.get(cm["pdf"])
                rec["pdf"] = cm["pdf"]
                rec["members"] = []
                for y in cm["joined"]:
                    y["page"] = fol.get(y.pop("pdf"))
                    rec["members"].append(y)
                if cm["others"]:
                    rec["others"] = cm["others"]
                data[c].setdefault(cm["ch"], {})[k] = rec
                used.setdefault(k, {"code": k, "ch": cm["ch"], "name": cm["name"], "congresses": []})
                used[k]["congresses"].append(c)
    for b in bad:
        print("not joined:", b)
    write(data, used, eds)


def write(data, used, eds):
    L = ["# Generated by tools/congress/make_cdir_committees.py from the Congressional Directory (govinfo); never edit by",
         "# hand: change the script's rules and rerun.",
         "# Schema:",
         "#   editions: <NN>: the first-session edition read (edition, url).",
         "#   committees: the select, special and joint committees, added to the committee list (congress/committees.yaml's",
         "#     standing committees): code (as the hearings calendar codes it), ch (s, h, j), name, congresses.",
         "#   congress: <NN>: s | h | j: <code>: name (the hearings calendar's), printed (the Directory's, where longer),",
         "#     page (the printed page of the committee's heading), pdf (the PDF's page), members (in the order printed:",
         "#     bio, name (the rosters' form), p, st, seat, ch, delegate, printed (the Directory's form), role (chair, vice,",
         "#     cochair), ex_officio, rank (the order within chamber and party), page, check), others (members named by an",
         "#     office: name, office).",
         ""]
    L.append("editions:")
    for c, e in sorted(eds.items()):
        L.append(f"  {c}: " + flow(e))
    L.append("committees:")
    for k in sorted(used, key=lambda k: (used[k]["ch"], used[k]["name"])):
        x = dict(used[k])
        x["congresses"] = sorted(set(x["congresses"]))
        L.append("  - " + flow(x))
    L.append("congress:")
    for c in sorted(data):
        L.append(f"  {c}:")
        for ch in ("s", "h", "j"):
            if ch not in data[c]:
                continue
            L.append(f"    {ch}:")
            for k in sorted(data[c][ch], key=lambda k: data[c][ch][k]["name"]):
                rec = data[c][ch][k]
                L.append(f"      {k}:")
                for f in ("name", "printed", "page", "pdf"):
                    if f in rec:
                        L.append("        " + flow({f: rec[f]})[1:-1])
                L.append("        members:")
                for y in rec["members"]:
                    L.append("          - " + flow(y))
                if rec.get("others"):
                    L.append("        others:")
                    for y in rec["others"]:
                        L.append("          - " + flow(y))
    path = os.path.join(ROOT, "congress", "committees-cdir.yaml")
    open(path + ".tmp", "w", encoding="utf-8").write("\n".join(L) + "\n")
    os.replace(path + ".tmp", path)
    yaml.safe_load(open(path, encoding="utf-8"))
    print("wrote", path)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
