"""The standing committees and the party leaders of each Congress, 87th-93rd: congress/committees.yaml.

Usage: python3 tools/congress/make_committees.py NELSON_DIR LEGISLATORS_DIR
  NELSON_DIR       Garrison Nelson's files from Charles Stewart III's data page (https://web.mit.edu/17.251/www/data_page.html):
                   hrc8097.mit (House, 80th-97th), snc80102.mit (Senate, 80th-102nd), cb9999 (the codebook); fetched if
                   missing (http://web.mit.edu/cstewart/www/data/<file>)
  LEGISLATORS_DIR  legislators-historical.yaml and legislators-current.yaml of unitedstates/congress-legislators (the
                   rosters' source), for the ICPSR -> Bioguide join and each member's years in the chamber
Hand corrections: congress/committees-hand.yaml (its header). Run once; rerun after changing the hand file; never edit
the output. The build needs no network.

What Nelson's files hold for these Congresses (read Oct. 21, 2026): one row a member a committee a Congress, the
standing committees only (no select, special or joint committee, and no subcommittee, in either file), with the
member's ICPSR id, party, party status on the committee (original listing in the Journal of the first session, an
addition to an enlarged committee, or a replacement), rank within that status, the chairmen and ranking minority
members (first and second where one changed), the dates of assignment and of leaving, and why he left; the Senate's
file also codes its floor leaders and whips (code 620). The House's has no leadership block: its leaders, and the
Senate's President pro tempore and conference chairmen, come from the House's and the Senate's own lists, in the
hand file.
"""
import collections
import datetime
import os
import sys
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bib import store  # noqa: E402

CONGRESSES = range(87, 94)
URL = "http://web.mit.edu/cstewart/www/data/"
FILES = {"h": "hrc8097.mit", "s": "snc80102.mit"}
CLOSE = {c: f"{1963 + 2 * (c - 87)}-01-03" for c in CONGRESSES}

# Nelson's codebook (cb9999), VAR14: the committees of these Congresses, by code, in the names the Congressional
# Directory prints over each committee's list (the editions of Apr. 1, 1961 to Mar. 10, 1973, govinfo's text).
NAMES = {
    102: "Agriculture", 104: "Appropriations", 106: "Armed Services", 111: "Banking and Currency", 115: "Budget",
    120: "District of Columbia", 124: "Education and Labor", 132: "Foreign Affairs", 138: "Government Operations",
    142: "House Administration", 146: "Interior and Insular Affairs", 148: "Internal Security",
    152: "Interstate and Foreign Commerce", 156: "Judiciary", 160: "Merchant Marine and Fisheries",
    168: "Post Office and Civil Service", 172: "Public Works", 176: "Rules", 180: "Science and Astronautics",
    186: "Standards of Official Conduct", 188: "Un-American Activities", 192: "Veterans' Affairs", 196: "Ways and Means",
    302: "Aeronautical and Space Sciences", 304: "Agriculture and Forestry", 306: "Appropriations", 308: "Armed Services",
    313: "Banking and Currency", 314: "Banking, Housing and Urban Affairs", 316: "Budget", 320: "Commerce",
    324: "District of Columbia", 336: "Finance", 338: "Foreign Relations", 342: "Government Operations",
    352: "Interior and Insular Affairs", 354: "Interstate and Foreign Commerce", 358: "Judiciary",
    363: "Labor and Public Welfare", 370: "Post Office and Civil Service", 374: "Public Works",
    380: "Rules and Administration", 388: "Veterans' Affairs",
}
# the codebook's notes on a committee's beginning or end within these Congresses
RENAMED = {188: "renamed Internal Security (148)", 148: "formerly Un-American Activities (188)",
           313: "renamed Banking, Housing and Urban Affairs (314)", 314: "formerly Banking and Currency (313)",
           354: "renamed Commerce (320)", 320: "formerly Interstate and Foreign Commerce (354)"}
DELEGATE = {"DC", "PR", "GU", "VI", "AS"}
PARTY = {100: "D", 137: "D", 200: "R", 328: "I", 360: "C"}
STATUS = {"1": ("maj", "orig"), "2": ("min", "orig"), "3": ("oth", "orig"), "4": ("maj", "added"), "5": ("min", "added"),
          "6": ("maj", "repl"), "7": ("min", "repl"), "8": ("oth", "added")}
ROLE = {11: "chair", 12: "chair1", 13: "chair2", 14: "chair3", 16: "acting", 21: "ranking", 22: "ranking1",
        23: "ranking2", 24: "ranking3"}
LEADER = {41: ("Majority Leader", ""), 42: ("Majority Leader", 1), 43: ("Majority Leader", 2),
          51: ("Majority Whip", ""), 52: ("Majority Whip", 1), 53: ("Majority Whip", 2),
          61: ("Minority Leader", ""), 62: ("Minority Leader", 1), 63: ("Minority Leader", 2),
          71: ("Minority Whip", ""), 72: ("Minority Whip", 1), 73: ("Minority Whip", 2)}
# VAR29: the assignment's status at the end of the Congress (1, remained, is left out)
END = {"2": "left for another committee", "3": "left the committee", "4": "left the committee", "5": "died",
       "6": "resigned from the chamber for another office", "7": "resigned from the chamber to seek another office",
       "8": "resigned from the chamber", "9": "lost a special election"}
OFFICES = ["Speaker", "President pro tempore", "Majority Leader", "Majority Whip", "Minority Leader", "Minority Whip",
           "Democratic Caucus Chairman", "Democratic Conference Chairman", "Republican Conference Chairman"]


def rows(path):
    """Nelson's fixed-width rows (the codebook's Summary of Data Format), for CONGRESSES."""
    for line in open(path, encoding="latin-1"):
        l = line.rstrip("\r\n").ljust(96)
        c = int(l[47:50])
        if c not in CONGRESSES:
            continue
        n = lambda a, b: int(l[a:b].strip() or 0)
        yield dict(office=l[2], icpsr=n(14, 19), name=l[20:45].strip(), c=c, code=n(50, 53), pstat=l[53],
                   rank=n(54, 56), senior=n(56, 58), chsen=n(58, 60), party=n(10, 13),
                   frm=(n(67, 69), n(69, 71), n(71, 75)), to=(n(75, 77), n(77, 79), n(79, 83)), end=l[84])


def iso(mdy):
    m, d, y = mdy
    return f"{y:04d}-{m:02d}-{d:02d}" if y else None


def roster_name(p):
    """make_rosters.py's form: 'Kennedy, Edward M. (Ted)'."""
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


def years_in(p, typ, day):
    """Whole years served in the chamber before the day, from the member's terms (a fortnight's grace for a late
    start)."""
    d0 = datetime.date.fromisoformat(day)
    days = 0
    for t in p["terms"]:
        if t["type"] != typ:
            continue
        a, b = datetime.date.fromisoformat(str(t["start"])), datetime.date.fromisoformat(str(t["end"]))
        if a < d0:
            days += (min(b, d0) - a).days
    return int((days + 15) // 365.25)


def main(nelson, legis):
    for f in list(FILES.values()) + ["cb9999"]:
        p = os.path.join(nelson, f)
        if not os.path.exists(p):
            os.makedirs(nelson, exist_ok=True)
            urllib.request.urlretrieve(URL + f, p)
    L = []
    for f in ("legislators-historical.yaml", "legislators-current.yaml"):
        L += yaml.load(open(os.path.join(legis, f), encoding="utf-8"), Loader=yaml.SafeLoader)
    hand = store.load_yaml(os.path.join(ROOT, "congress", "committees-hand.yaml"))
    by_icpsr = {p["id"]["icpsr"]: p for p in L if p["id"].get("icpsr")}
    by_bio = {p["id"]["bioguide"]: p for p in L}
    for i, x in (hand.get("icpsr") or {}).items():
        by_icpsr[int(i)] = by_bio[x["bio"]]
    rosters = {c: store.load_yaml(os.path.join(ROOT, "congress", f"{c}.yaml")) for c in CONGRESSES}

    def find(who, c, ch):
        sur, first, st = who
        typ = "rep" if ch == "h" else "sen"
        hits = [p for p in L if p["name"]["last"].replace("’", "'") == sur and
                (p["name"]["first"].startswith(first) or (p["name"].get("nickname") or "").startswith(first)) and
                any(t["type"] == typ and t["state"] == st and str(t["start"]) < CLOSE[c] and str(t["end"]) > opened(c)
                    for t in p["terms"])]
        assert len(hits) == 1, (who, c, len(hits))
        return hits[0]

    def opened(c):
        return str(rosters[c]["opened"])

    def seat_of(p, c, ch):
        """The member's seat in this Congress: the roster's at the opening, else his term's."""
        rows_ = rosters[c]["house" if ch == "h" else "senate"]
        for r in rows_:
            if r.get("bio") == p["id"]["bioguide"]:
                return r["st"], (r["d"] if ch == "h" else r["cl"]), r["name"], r["party"], True
        typ = "rep" if ch == "h" else "sen"
        for t in p["terms"]:
            if t["type"] == typ and str(t["start"]) < CLOSE[c] and str(t["end"]) > opened(c):
                return (t["state"], (t.get("district") or 0) if ch == "h" else t.get("class"), roster_name(p),
                        None, False)
        return None

    unjoined, out_c, used = collections.Counter(), {}, collections.defaultdict(set)
    for ch, f in FILES.items():
        for r in rows(os.path.join(nelson, f)):
            if r["code"] not in NAMES and r["code"] != 620:
                continue                         # 770-795: not sworn, died or resigned before assignment, unassigned
            if r["office"] in "78":              # a delegate or resident commissioner: in his committee's ranks, not
                hit = [p for p in L if store.fold(p["name"]["last"]) == store.fold(r["name"].split(",")[0]) and
                       any(t_["state"] in DELEGATE and str(t_["start"]) < CLOSE[r["c"]] and str(t_["end"]) > str(rosters[r["c"]]["opened"])
                           for t_ in p["terms"])]           # in the rosters
                st = next(t_["state"] for t_ in hit[0]["terms"] if t_["state"] in DELEGATE) if len(hit) == 1 else "?"
                cc = out_c.setdefault(r["c"], {"h": {"committees": collections.defaultdict(list), "leaders": []},
                                               "s": {"committees": collections.defaultdict(list), "leaders": []}})[ch]
                side, group = STATUS[r["pstat"]]
                x = {"name": roster_name(hit[0]) if len(hit) == 1 else r["name"], "p": PARTY.get(r["party"], "?"),
                     "st": st, "delegate": True, "side": side, "rank": r["rank"], "from": iso(r["frm"])}
                if len(hit) == 1:
                    x = {"bio": hit[0]["id"]["bioguide"], **x}
                if r["end"] != "1":
                    x["to"], x["why"] = iso(r["to"]), END[r["end"]]
                x["icpsr"] = r["icpsr"]
                cc["committees"][r["code"]].append(x)
                continue
            p = by_icpsr.get(r["icpsr"])
            if not p:
                unjoined[(r["c"], ch, r["icpsr"], r["name"])] += 1
                continue
            fix = ((hand.get("rows") or {}).get(r["c"]) or {}).get(f"{ch} {r['code']} {r['icpsr']}")
            if fix:
                r.update(fix["set"])
            seat = seat_of(p, r["c"], ch)
            if not seat:
                unjoined[(r["c"], ch, r["icpsr"], r["name"] + " (no term)")] += 1
                continue
            st, sn, nm, rp, at_open = seat
            cc = out_c.setdefault(r["c"], {"h": {"committees": collections.defaultdict(list), "leaders": []},
                                           "s": {"committees": collections.defaultdict(list), "leaders": []}})[ch]
            party = PARTY.get(r["party"], "?")
            if party not in ("D", "R") and rp:
                party = rp
            if r["code"] == 620:                 # the Senate's floor leaders and whips
                office, k = LEADER[r["senior"]]
                x = {"office": office, "bio": p["id"]["bioguide"], "name": nm, "p": party, "st": st}
                if iso(r["frm"]) != opened(r["c"]):
                    x["from"] = iso(r["frm"])
                if r["end"] != "1":
                    x["to"], x["why"] = iso(r["to"]), END[r["end"]].capitalize()
                x["src"] = "nelson"
                cc["leaders"].append(x)
                continue
            side, group = STATUS[r["pstat"]]
            x = {"bio": p["id"]["bioguide"], "name": nm, "p": party, "st": st, "seat": sn, "side": side}
            if group != "orig":
                x["group"] = group
            x["rank"] = r["rank"]
            if r["senior"] in ROLE:
                x["role"] = ROLE[r["senior"]]
            x["from"] = iso(r["frm"])
            if r["end"] != "1":
                x["to"], x["why"] = iso(r["to"]), END[r["end"]]
            x["icpsr"] = r["icpsr"]
            cc["committees"][r["code"]].append(x)
            used[r["code"]].add(r["c"])
    if unjoined:
        print("Not joined to congress-legislators:")
        for k, v in sorted(unjoined.items()):
            print("  ", k, v)
    # the hand file's leaders, and the Senate's floor leaders checked against the Senate's lists
    for c, chs in (hand.get("leaders") or {}).items():
        for ch, xs in chs.items():
            for h in xs:
                p = find(h["who"], c, ch)
                st, sn, nm, rp, _ = seat_of(p, c, ch)
                x = {"office": h["office"], "bio": p["id"]["bioguide"], "name": nm, "p": rp or "?", "st": st}
                for k in ("from", "to", "why", "note"):
                    if h.get(k):
                        x[k] = h[k]
                x["src"] = h["src"]
                out_c[c][ch]["leaders"].append(x)
    bad = []
    for c, want in (hand.get("senate_pages") or {}).items():
        got = collections.defaultdict(list)
        for x in out_c[c]["s"]["leaders"]:
            if x["src"] == "nelson":
                got[x["office"]].append(x["name"].split(",")[0])
        for office, names in want.items():
            if got[office] != names:
                bad.append((c, office, names, got[office]))
    for b in bad:
        print("Nelson and the Senate's lists differ:", b)
    assert not bad
    # years in the chamber at the opening, every member of the roster
    years = {}
    for c in CONGRESSES:
        years[c] = {}
        for ch, key, typ in (("h", "house", "rep"), ("s", "senate", "sen")):
            years[c][ch] = {r["bio"]: years_in(by_bio[r["bio"]], typ, opened(c))
                            for r in rosters[c][key] if r.get("bio") in by_bio}
    write(out_c, used, years, hand)


def order(xs):
    """A committee's members: by side (majority, minority, others), the original listing by rank, then the additions
    and replacements by date of assignment."""
    side = {"maj": 0, "min": 1, "oth": 2}
    return sorted(xs, key=lambda x: (side[x["side"]], "group" in x, x["from"] if "group" in x else "", x["rank"]))


def flow(d):
    return yaml.safe_dump(d, default_flow_style=True, allow_unicode=True, width=10 ** 6, sort_keys=False).strip()


def write(out_c, used, years, hand):
    L = ["# Generated by tools/congress/make_committees.py; never edit by hand (corrections: congress/committees-hand.yaml).",
         "# Sources: Garrison Nelson, Committees in the U.S. Congress, 1947-1992, data files House 80th-97th (hrc8097.mit)",
         "#   and Senate 80th-102nd (snc80102.mit), with the codebook cb9999, from Charles Stewart III's data page",
         "#   (https://web.mit.edu/17.251/www/data_page.html); members joined to the rosters by ICPSR id through",
         "#   unitedstates/congress-legislators; the leaders Nelson does not code from the House's and the Senate's lists",
         "#   (congress/committees-hand.yaml, sources).",
         "# Schema:",
         "#   committees: the committee list, one a code (Nelson's VAR14: 1xx House standing, 3xx Senate standing; Nelson's",
         "#     files hold no select, special or joint committee for these Congresses): code, ch (h|s), name (as the",
         "#     Congressional Directory prints it over the committee's list), congresses (those it has members in), note.",
         "#   congress: <NN>: <h|s>:",
         "#     leaders: office, bio (Bioguide), name (as the rosters write it), p (party), st, from and to (where the",
         "#       office changed during the Congress), why, note, src (nelson, or a key of the hand file's sources).",
         "#     committees: <code>: members in order: by side (maj, min, oth), the Journal's original listing at the first",
         "#       session by rank, then additions (group: added, to an enlarged committee) and replacements (group: repl)",
         "#       by date. Each: bio, name, p, st, seat (district, 0 at large; Senate class), side, group, rank (Nelson's,",
         "#       within side and group), role (chair, ranking; chair1/chair2, ranking1/ranking2 where one followed",
         "#       another), from (assigned), to and why (where he left before the end of the Congress), icpsr; a delegate",
         "#       or resident commissioner (delegate: true) in his place in the ranks, without a seat.",
         "#     years: Bioguide -> whole years served in the chamber before the opening (congress-legislators' terms),",
         "#       every member of the roster at the opening.",
         ""]
    L.append("committees:")
    for code in sorted(used):
        cs = sorted(used[code])
        x = {"code": code, "ch": "h" if code < 300 else "s", "name": NAMES[code], "congresses": [cs[0], cs[-1]]}
        if code in RENAMED:
            x["note"] = RENAMED[code]
        L.append("  - " + flow(x))
    L.append("congress:")
    for c in sorted(out_c):
        L.append(f"  {c}:")
        for ch in ("h", "s"):
            d = out_c[c][ch]
            L.append(f"    {ch}:")
            L.append("      leaders:")
            ld = sorted(d["leaders"], key=lambda x: (OFFICES.index(x["office"]), x.get("from") or ""))
            for x in ld:
                L.append("        - " + flow(x))
            L.append("      committees:")
            for code in sorted(d["committees"]):
                L.append(f"        {code}:")
                for x in order(d["committees"][code]):
                    L.append("          - " + flow(x))
            L.append("      years: " + flow(years[c][ch]))
    path = os.path.join(ROOT, "congress", "committees.yaml")
    open(path + ".tmp", "w", encoding="utf-8").write("\n".join(L) + "\n")
    os.replace(path + ".tmp", path)
    yaml.safe_load(open(path, encoding="utf-8"))      # it reads back
    print("wrote", path)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
