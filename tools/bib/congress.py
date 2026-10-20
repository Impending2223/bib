"""Each Congress at its opening: party bars, House and Senate maps, rosters.

    congress/<NN>.yaml   the members at the opening (House by state and district,
                         0 = at large; Senate by state and class), editable
    congress/geo.json    district and state shapes, projected (Albers, 960x600)
                         and simplified; generated once from the Lewis district files

A calendar entry tagged congress:<NN> carries that Congress's block, in cal.html
and in the compiled reader; build/congress.html carries all of them.

The maps' switch at an opening: Party (the default), Result and Margin, the last two of the race that seated each
member (seatlinks.seat_figures; gray where he was not elected to the seat); each map's types, the map, the dots and
the Chamber (elections.py, STYLE 12).
"""
import json
import os
import re
from collections import Counter, defaultdict

from . import datelist, namelinks, specials, store
from .markup import to_html, plain

DIR = os.path.join(store.ROOT, "congress")
SOUTH = {"AL", "AR", "FL", "GA", "LA", "MS", "NC", "SC", "TN", "TX", "VA"}
PARTY = {"D": "Democrat", "R": "Republican", "C": "Conservative", "I": "Independent", "ID": "Independent Democrat"}
STATE = dict(AL="Alabama", AK="Alaska", AZ="Arizona", AR="Arkansas", CA="California", CO="Colorado", CT="Connecticut",
             DE="Delaware", FL="Florida", GA="Georgia", HI="Hawaii", ID="Idaho", IL="Illinois", IN="Indiana", IA="Iowa",
             KS="Kansas", KY="Kentucky", LA="Louisiana", ME="Maine", MD="Maryland", MA="Massachusetts", MI="Michigan",
             MN="Minnesota", MS="Mississippi", MO="Missouri", MT="Montana", NE="Nebraska", NV="Nevada", NH="New Hampshire",
             NJ="New Jersey", NM="New Mexico", NY="New York", NC="North Carolina", ND="North Dakota", OH="Ohio",
             OK="Oklahoma", OR="Oregon", PA="Pennsylvania", RI="Rhode Island", SC="South Carolina", SD="South Dakota",
             TN="Tennessee", TX="Texas", UT="Utah", VT="Vermont", VA="Virginia", WA="Washington", WV="West Virginia",
             WI="Wisconsin", WY="Wyoming")
# The States as the Bluebook abbreviates them (Table T10), for citations and the Lives' tables.
BLUEBOOK = dict(AL="Ala.", AK="Alaska", AZ="Ariz.", AR="Ark.", CA="Cal.", CO="Colo.", CT="Conn.", DE="Del.",
                DC="D.C.", FL="Fla.", GA="Ga.", HI="Haw.", ID="Idaho", IL="Ill.", IN="Ind.", IA="Iowa", KS="Kan.",
                KY="Ky.", LA="La.", ME="Me.", MD="Md.", MA="Mass.", MI="Mich.", MN="Minn.", MS="Miss.", MO="Mo.",
                MT="Mont.", NE="Neb.", NV="Nev.", NH="N.H.", NJ="N.J.", NM="N.M.", NY="N.Y.", NC="N.C.", ND="N.D.",
                OH="Ohio", OK="Okla.", OR="Or.", PA="Pa.", RI="R.I.", SC="S.C.", SD="S.D.", TN="Tenn.", TX="Tex.",
                UT="Utah", VT="Vt.", VA="Va.", WA="Wash.", WV="W. Va.", WI="Wis.", WY="Wyo.")
SHORT = {"samuel": ["sam"], "william": ["bill", "will", "wm"], "robert": ["bob"], "thomas": ["tom"], "edward": ["ted", "ed"],
         "james": ["jim", "jimmy"], "michael": ["mike"], "charles": ["charlie"], "richard": ["dick"], "joseph": ["joe"],
         "john": ["jack"], "daniel": ["dan"], "eugene": ["gene"], "frederick": ["fred"], "albert": ["al"],
         "hubert": ["hubert"], "lawrence": ["larry"], "kenneth": ["ken"], "theodore": ["ted"], "henry": ["harry"],
         "everett": ["everett"], "clifford": ["cliff"], "gerald": ["jerry"], "abraham": ["abe"], "barry": ["barry"], "nicholas": ["nick"], "cornelius": ["neil"], "clement": ["clem"], "david": ["dave"]}
YEARS = {c: f"{1961 + 2 * (c - 87)}–{str(1963 + 2 * (c - 87))[2:]}" for c in range(85, 95)}


def ordinal(n):
    return f"{n}{'th' if 11 <= n % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def load():
    out = {}
    if not os.path.isdir(DIR):
        return out, None
    for f in sorted(os.listdir(DIR)):
        m = re.match(r"^(\d+)\.yaml$", f)
        if m:
            out[int(m.group(1))] = store.load_yaml(os.path.join(DIR, f))
    gp = os.path.join(DIR, "geo.json")
    geo = json.load(open(gp, encoding="utf-8")) if os.path.exists(gp) else None
    return out, geo


# ---------------------------------------------------------------- cross-references

class Pointers:
    """Member -> the series' name-index lines and the calendar entries that name them."""

    def __init__(self, series, linker, data=None):
        self.series, self.linker = series, linker
        self.senior = set()   # name keys held by a member without "Jr."
        for d in (data or {}).values():
            for r in d["house"] + d["senate"]:
                if r.get("name"):
                    ks, suf = self.keys(r["name"])
                    if "Jr" not in suf:
                        self.senior.update(ks[:1])
        self.cal = defaultdict(list)   # name key -> [calendar entry]
        self.calx = defaultdict(list)  # Part III entry id -> [calendar entry]
        for lst in series.lists.values():
            if lst.kind != "calendar":
                continue
            for sec, e in lst.entries():
                for x in self.named(lst, e):
                    if e not in self.calx[x["id"]]:
                        self.calx[x["id"]].append(e)
                    for k, _ in linker.refs.name_keys(x["s"]):
                        if e not in self.cal[k]:
                            self.cal[k].append(e)

    def named(self, lst, e):
        """The person entries a calendar entry's 'Names:' line names ("Names: Heller, Tobin"), each found by
        Linker.who_named from the entry's name: tags and the name index; a line still written with its list and
        section ("Heller, Tobin (K–J Adm. III.H)") takes the section as a hint where those do not settle a name."""
        n = plain(e.get("n") or "")
        m = re.search(r"Names: (.*)$", n)
        if not m:
            return []
        tags = {str(t)[5:] for t in (e.get("tags") or []) if str(t).startswith("name:")}
        from .build import names_line, names_tokens
        out = []
        toks = names_tokens(names_line(n)[1])
        for (tok, ref_part), hit in zip(toks, self.linker.names_resolved([t for t, _ in toks], tags)):
            x = hit[0] if hit else None
            if hit and not x:                # a name entry with no Part III entry: nothing to point to here
                continue
            if not x and ref_part:
                scanned = list(self.linker.refs.scan(ref_part, lst.key))
                if scanned:
                    x = self.linker.find_person(tok, scanned[0][2], [c for _, _, k, c in scanned if c], tags)
            if x and x not in out:
                out.append(x)
        return out

    def keys(self, name):
        """'Kennedy, Edward M. (Ted)' -> name keys to try, and the suffix."""
        nick = re.search(r"\(([^)]+)\)", name)
        bare = re.sub(r"\s*\([^)]*\)", "", name)
        parts = [p.strip() for p in bare.split(",")]
        sur, given = parts[0], (parts[1] if len(parts) > 1 else "")
        suffix = " ".join(parts[2:])
        g = store.fold(given).split()
        ks = []
        if "," not in bare:              # a name in its own order ('Ngo Dinh Diem'): the whole name, as refs keys it
            ks.append(store.fold(bare))
        if g:
            ks.append(f"{store.fold(sur)} {g[0]}")
        if nick:
            ks.append(f"{store.fold(sur)} {store.fold(nick.group(1)).split()[0]}")
        if g and g[0] in SHORT:
            ks += [f"{store.fold(sur)} {v}" for v in SHORT[g[0]]]
        if len(g) > 1 and len(g[1]) > 1:
            ks.append(f"{store.fold(sur)} {g[1]}")
        return ks, suffix

    def lines(self, name, href):
        ks, suffix = self.keys(name)
        out, seen = [], set()
        for k in ks:
            for l, s, e in self.linker.people.get(k, []):
                if e["id"] in seen:
                    continue
                ejr, mjr = bool(re.search(r"\bJr\b", e.get("s", ""))), "Jr" in suffix
                if ejr and not mjr:
                    continue
                if mjr and not ejr and k in self.senior:
                    continue   # Harry F. Byrd, Jr., is not his father's entry
                seen.add(e["id"])
                out.append(f'<a href="{href(l.key, e["id"])}">{esc(l.abbr)} {esc(s.code)}</a>')
        cal = []
        for k in ks:
            for e in self.cal.get(k, []):
                if e["id"] not in seen:
                    seen.add(e["id"])
                    cal.append(e)
        if cal:
            cal.sort(key=lambda e: e["date"])
            out.append("Cal. " + datelist.run([(e["date"], f'<a href="{href("cal", e["id"])}">{esc(e["when"])}</a>')
                                               for e in cal]))     # by year (datelist STYLE)
        return out


# ---------------------------------------------------------------- the block

SOUTH_LINE = ("The eleven Southern States: the thirteen States represented in the Confederate States Congress, "
              "less Missouri and Kentucky.")


def caucused(r):
    """'Di' or 'Ri' for a member of neither major party, by the party caucused with; else None."""
    if r.get("vacant") or r["party"] in ("D", "R"):
        return None
    from .elections import caucus
    cc = caucus({"p": r["party"], "n": r["name"].split(",")[0].strip()})
    return cc + "i" if cc in ("D", "R") else None


def third_name(r):
    """'Conservative, caucusing with the Republicans'."""
    from .elections import third_label
    return third_label({"p": r["party"], "n": r["name"].split(",")[0].strip(), "party": PARTY.get(r["party"])})


def bar(label, rows, senate):
    n = len(rows)
    def kind(r):
        if r.get("vacant"):
            return "vacant"
        if r["party"] == "D":
            return "Ds" if r["st"] in SOUTH else "Dn"
        return caucused(r) or r["party"]
    cnt = Counter(kind(r) for r in rows)
    names = {"Dn": "Non-Southern Democrats", "Ds": "Southern Democrats", "vacant": "Vacant",
             "Di": "Caucusing with the Democrats", "Ri": "Caucusing with the Republicans"}
    x, segs = 0.0, []
    W = 1000
    for p in ["Dn", "Ds", "Di", "ID", "I", "C", "vacant", "Ri", "R"]:
        k = cnt.get(p, 0)
        if not k:
            continue
        w = W * k / n
        segs.append(f'<rect class="p{p}" x="{x:.1f}" y="18" width="{w:.1f}" height="30"><title>{esc(names.get(p, PARTY.get(p, p)))}: {k}</title></rect>')
        if w > 40:
            segs.append(f'<text class="bn b{p}" x="{x + (8 if p != "R" else w - 8):.1f}" y="38" text-anchor="{"start" if p != "R" else "end"}">{k}</text>')
        x += w
    maj = n // 2 + 1
    two3 = -(-2 * n // 3)
    marks = [(W / 2, f"{maj}: majority"), (W * 2 / 3, f"{two3}: two-thirds"), (W / 3, "")]
    lines = []
    for pos, txt in marks:
        lines.append(f'<line class="mk" x1="{pos:.1f}" x2="{pos:.1f}" y1="12" y2="54"/>')
        if txt:
            lines.append(f'<text class="ml" x="{pos:.1f}" y="9" text-anchor="middle">{txt}</text>')
    lines.append(f'<text class="ml" x="{W / 3:.1f}" y="66" text-anchor="middle">two-thirds from the right</text>')
    d = cnt.get("Dn", 0) + cnt.get("Ds", 0)
    parts = [f"{d} Democrats ({cnt.get('Dn', 0)} non-Southern, {cnt.get('Ds', 0)} Southern)"]
    parts += [f"{cnt.get(p)} {PARTY[p] if cnt.get(p) == 1 else PARTY[p] + 's'}" for p in ("R", "C", "I", "ID") if cnt.get(p)]
    parts += [f"1 {third_name(r)}" for r in rows if caucused(r)]
    if cnt.get("vacant"):
        parts.append(f"{cnt['vacant']} vacant")
    cap = f'{label}, {n} seats: ' + ("; " if any(caucused(r) for r in rows) else ", ").join(parts) + "."
    if senate:
        cap += " The two-thirds line is both the veto override and cloture (Rule XXII as amended in 1959: two-thirds of those present and voting)."
    else:
        cap += " The two-thirds line is the veto override (two-thirds of those present and voting, here of the whole House)."
    return (f'<figure class="cgbar"><svg viewBox="0 -4 1000 74" role="img" aria-label="{esc(cap)}">'
            + "".join(segs) + "".join(lines) + f'</svg><figcaption>{esc(cap)}</figcaption></figure>')


def initials(given):
    return "".join(w[0] + "." for w in given.replace(".", " ").split())


def map_labels(rows):
    """Surname alone; given-name initials where a surname is shared in this Congress;
    full given names where the initials are shared too."""
    def parts(r):
        bare = re.sub(r"\s*\([^)]*\)", "", r["name"])
        p = [x.strip() for x in bare.split(",")]
        return p[0], r.get("given") or (p[1] if len(p) > 1 else ""), ", ".join(p[2:])
    people = [r for r in rows if r.get("name")]
    by_sur = defaultdict(list)
    for r in people:
        by_sur[parts(r)[0]].append(r)
    out = {}
    for sur, rs in by_sur.items():
        if len(rs) == 1:
            out[id(rs[0])] = sur
            continue
        by_ini = defaultdict(list)
        for r in rs:
            by_ini[initials(parts(r)[1])].append(r)
        for ini, rr in by_ini.items():
            for r in rr:
                _, given, suffix = parts(r)
                first = given if len(rr) > 1 else ini
                out[id(r)] = f"{first} {sur}" + (f" {suffix}" if suffix and len(rr) > 1 else "")
    return out


FULL = {"January": "Jan.", "February": "Feb.", "March": "Mar.", "April": "Apr.", "August": "Aug.",
        "September": "Sept.", "October": "Oct.", "November": "Nov.", "December": "Dec."}


def changes():
    p = os.path.join(DIR, "changes.yaml")
    return store.load_yaml(p) if os.path.exists(p) else {}


def change_note(x, sp=None, here=False):
    """'Died Nov. 16, 1961. Ray Roberts (D), elected Jan. 30, 1962, seated Jan. 30, 1962.' (HTML): the
    election date, linked to the race, from congress/specials.yaml where a special filled the seat."""
    t = (x.get("reason") or "").strip()
    if sp:   # the special's own date over the changes table's ("Successor elected June 14, 1961")
        t = re.sub(r"\s*Successor elected [^.]*\.", "", t)
    if t and not t.endswith("."):
        t += "."
    if x.get("into"):
        t += f" {x['into']}" + (f" ({x['into_party']})" if x.get("into_party") else "")
        if sp:
            t += f", elected \x00{sp['date']}\x00"
        t += (f", seated {x['seated']}." if x.get("seated") and re.search(r"\d{4}", x["seated"]) else ".")
    else:
        t += " Not filled."
    for k, v in FULL.items():
        t = re.sub(r"\b" + k + r"\b", v, t)
    t = esc(t.strip())
    if sp:
        from . import specials
        lab = specials.fmt_date(sp["date"]) + ("" if sp.get("with_general") else " (special)")
        target = (("#" if here else "congress.html#") + specials.rid(sp)) if not sp.get("with_general") else ""
        link = f'<a href="{target}">{esc(lab)}</a>' if target else esc(lab)
        t = t.replace(f"\x00{sp['date']}\x00", link)
    return t


def block(c, data, geo, ptr, href, rid, here=False):
    """One Congress: bars, two maps, two rosters. rid(c, chamber, st, seat) -> a row id."""
    house, senate = data["house"], data["senate"]
    out = [f'<div class="cg el op" data-cg="{c}">']
    out.append(f'<p class="cgh">{ordinal(c)} Congress at its opening, {esc(fmt_date(data["opened"]))}</p>')
    out.append(bar("House", house, False))
    out.append(bar("Senate", senate, True))
    out.append(f'<p class="cgsouth">{esc(SOUTH_LINE)}</p>')
    lab = map_labels(house + senate)
    seats = {"h": defaultdict(list), "s": defaultdict(list)}
    def rec(r, ch, seat):
        x = {("d" if ch == "h" else "cl"): seat, "p": "V" if r.get("vacant") else (caucused(r) or r["party"]),
             "n": lab.get(id(r), "Vacant"), "id": rid(c, ch, r["st"], seat)}
        if caucused(r):
            x["pl"] = third_name(r)
        if not r.get("vacant"):                   # the race that seated him, for the Result and Margin views
            from . import seatlinks
            x.update(seatlinks.seat_figures(str(data["opened"]), ch, r["st"], seat, r["name"]))
        return x
    for r in house:
        seats["h"][r["st"]].append(rec(r, "h", r["d"]))
    for r in senate:
        seats["s"][r["st"]].append(rec(r, "s", r["cl"]))
    out.append(f'<script type="application/json" class="cgseats">{json.dumps(seats, ensure_ascii=False, separators=(",", ":"))}</script>')
    out.append('<div class="cgmaps">'
               '<figure class="cgmap dots" data-chamber="h"><figcaption>House, by delegation</figcaption>'
               '<div class="cgv" style="aspect-ratio:1085/660"></div></figure>'
               '<figure class="cgmap" data-chamber="s"><figcaption>Senate, by state</figcaption>'
               '<div class="cgv" style="aspect-ratio:960/660"></div></figure></div><span data-views="n r s"></span>')
    from .elections import margin_scale
    sw = lambda k: f'<span class="sw e{k}"></span>'
    gray = f'{sw("N")}Not elected to the seat (appointed), or a race without figures. '
    out.append('<p class="cgkey elkey"><span class="lk lk-n"><span class="sw pD"></span>Democratic <span class="sw pR"></span>Republican '
               '<span class="sw pDi"></span>Caucusing with the Democrats <span class="sw pRi"></span>Caucusing with the Republicans '
               '<span class="sw pO"></span>Other <span class="sw pV"></span>Vacant <span class="sw pX"></span>Split delegation. </span>'
               f'<span class="lk lk-r">The race that seated each member: {sw("B2")}Democratic held {sw("B4")}Democratic pickup '
               f'{sw("R2")}Republican held {sw("R4")}Republican pickup <span class="sw pDi"></span><span class="sw pRi"></span>'
               f'Independent or third party, by the party caucused with {gray}</span>'
               '<span class="lk lk-s">The race that seated each member, the winner\'s margin over the runner-up, points of all '
               f'the votes: {margin_scale()} {gray}</span>'
               'Dots: at-large seats beside districts. Zoom with the buttons, a double-click, a pinch, or Ctrl-scroll; drag to pan. Click a district for its representatives, a state for its senators. Delegations, under the House map: a dot a seat, a block a State; hover a dot for its district, click a dot to open it; then click a district to select it, double-click to go there; double-click white space to come back. Chamber: a dot a seat in a half-circle, the Democrats and those caucusing with them on the left, the Republicans and theirs on the right, by the margin of the race that seated each, the narrowest in the middle; those not elected to the seat at the ends.</p>')
    later = defaultdict(list)
    for x in changes().get(c, []) or []:
        later[(x["ch"], x["st"], x["seat"])].append(x)
    for ch, rows, label in (("h", house, "House"), ("s", senate, "Senate")):
        out.append(f'<details class="cgr cgm"><summary>{label} members, {len(rows)}, by state</summary><table>'
                   '<colgroup><col class="c1"><col class="c2"><col class="c3"><col class="c4"></colgroup>')
        out.append(f'<thead><tr><th>{"" if ch == "h" else "Class"}</th><th>Member</th><th>Party</th><th>In the series</th></tr></thead><tbody>')
        bystate = defaultdict(list)
        for r in rows:
            bystate[r["st"]].append(r)
        for st in sorted(bystate, key=lambda s: STATE[s]):
            out.append(f'<tr class="st"><th colspan="4">{STATE[st]}</th></tr>')
            for r in bystate[st]:
                seat = r["d"] if ch == "h" else r["cl"]
                lab = ("AL" if seat == 0 else str(seat)) if ch == "h" else ("I", "II", "III")[seat - 1]
                if r.get("vacant"):
                    who, party, pts = "<i>Vacant</i>", "", []
                else:
                    who, party = namelinks.a(ptr.series, r["name"], esc(r["name"])), r["party"]
                    pts = ptr.lines(r["name"], href)
                    if caucused(r):
                        party = f'<span title="{esc(third_name(r))}">{party} ({caucused(r)[0]})</span>'
                note = f'<span class="cgn">{to_html(r["n"])}</span>' if r.get("n") else ""
                sws = specials.switch_for(c, ch, r["st"], seat)
                for x in later.get((ch, r["st"], seat), []):
                    if any(specials.surname(s_["name"]) == specials.surname(x.get("out") or "") and
                           (x.get("into") or "") == (x.get("out") or "") or re.search(r"[Cc]hanged part|[Ss]witched part", x.get("reason") or "")
                           for s_ in sws):
                        continue            # a party switch: the note below says it, with the date
                    note += f'<span class="cgn cgc">{change_note(x, specials.for_change(c, x), here)}</span>'
                for s_ in sws:
                    note += f'<span class="cgn cgc">{esc(specials.switch_note(s_))}</span>'
                from . import seatlinks
                note += seatlinks.member_line(c, str(data["opened"]), ch, r["st"], seat,
                                              "" if r.get("vacant") else r["name"], here)
                out.append(f'<tr id="{rid(c, ch, r["st"], seat)}"><td>{lab}</td><td>{who}{note}</td>'
                           f'<td class="p{(caucused(r) or r.get("party") or "V") if not r.get("vacant") else "V"}t">{party}</td><td>{"; ".join(pts)}</td></tr>')
        out.append("</tbody></table></details>")
    out.append("</div>")
    return "\n".join(out)


MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]


def fmt_date(d):
    y, m, dd = str(d).split("-")
    return f"{MONTHS[int(m) - 1]} {int(dd)}, {y}"


def geo_subset(geo, cs):
    """The shapes the given Congresses use, fine and coarse, plus state outlines and centers."""
    keys = {k for c in cs for st in geo["congress"][str(c)].values() for k in st.values()}
    return {"shapes": {k: geo["shapes"][k] for k in keys},
            "coarse": {k: geo["coarse"][k] for k in keys},
            "congress": {str(c): geo["congress"][str(c)] for c in cs},
            "states": geo["states"], "statesC": geo["statesC"], "centers": geo["centers"]}


ASSETS = os.path.join(store.ROOT, "templates", "congress.html")


MARGINS = os.path.join(store.ROOT, "elections", "pres-margins.csv")


def margin_quantiles(step=2.5):
    """The Margin view's quantile table (QM in the template): the margin at every 2.5th percentile of the
    contested races for presidential electors, 1824-2024 (elections/pres-margins.csv, tools/elections/pres_margins.py)."""
    import csv
    ms = sorted(float(r["margin"]) for r in csv.DictReader(open(MARGINS, encoding="utf-8")))
    out = []
    for i in range(int(100 / step) + 1):
        x = (len(ms) - 1) * i * step / 100
        lo = int(x)
        out.append(round(ms[lo] + (ms[min(lo + 1, len(ms) - 1)] - ms[lo]) * (x - lo), 2))
    return out


GEO_OUT = os.path.join(store.ROOT, "build", "geo")
_geo_src = None


def geo_files():
    """The shapes as files of their own beside the pages, shared by every page with a map (the owner's ruling, Oct. 16,
    2026: the shapes out of the pages): build/geo/base-<hash>.json, the coarse shapes, the State outlines, their
    centers and each Congress's districts, fetched when the first map nears the screen; fine-<hash>.json, the detailed
    shapes, fetched when a map is first zoomed past FINE. The hash in the name lets a browser keep them until they
    change. Returns {base, fine}: their paths from a page in build/."""
    global _geo_src
    if _geo_src:
        return _geo_src
    import hashlib
    _, geo = load()
    parts = {"base": {k: geo[k] for k in ("coarse", "statesC", "centers", "congress")},
             "fine": {k: geo[k] for k in ("shapes", "states")}}
    os.makedirs(GEO_OUT, exist_ok=True)
    out = {}
    for k, d in parts.items():
        txt = json.dumps(d, separators=(",", ":"))
        name = f"{k}-{hashlib.sha1(txt.encode()).hexdigest()[:10]}.json"
        path = os.path.join(GEO_OUT, name)
        if not os.path.exists(path):
            for old in os.listdir(GEO_OUT):
                if old.startswith(k + "-"):
                    os.remove(os.path.join(GEO_OUT, old))
            open(path, "w", encoding="utf-8").write(txt)
        out[k] = "geo/" + name
    _geo_src = out
    return out


def assets(geo=None):
    """CSS and JS for the blocks, with the paths of the shapes they fetch (geo_files)."""
    t = open(ASSETS, encoding="utf-8").read()
    return t.replace("{{geo}}", json.dumps(geo_files())).replace("{{qm}}", json.dumps(margin_quantiles()))


def inject(page, series, linker, mode):
    """Put each tagged calendar entry's Congress block into a built page."""
    from . import elections
    elections.SERIES = specials.SERIES = series      # the candidates' name entries
    data, geo = load()
    if not data or not geo:
        return page
    ptr = Pointers(series, linker, data)
    href = (lambda key, eid: f"#{eid}") if mode == "series" else (lambda key, eid: f"{key}.html#{eid}" if key != "cal" else f"#{eid}")
    rid = lambda c, ch, st, seat: f"cg{c}-{ch}-{st}-{seat}"
    used = []
    from . import elections
    edata = elections.load()
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^election:(\d{4})$", t)
                if m and int(m.group(1)) in edata:
                    y = int(m.group(1))
                    blk = elections.block(y, edata)
                    pat = re.compile(r'(<li id="' + re.escape(e["id"]) + r'"[^>]*>.*?)(</li>)', re.S)
                    page, n = pat.subn(lambda mm: mm.group(1) + blk + mm.group(2), page, count=1)
                    if n:
                        used.append(edata[y]["congress"])
                m = re.match(r"^congress:(\d+)$", t)
                if m and int(m.group(1)) in data:
                    c = int(m.group(1))
                    blk = block(c, data[c], geo, ptr, href, rid)
                    pat = re.compile(r'(<li id="' + re.escape(e["id"]) + r'"[^>]*>.*?)(</li>)', re.S)
                    page, n = pat.subn(lambda mm: mm.group(1) + blk + mm.group(2), page, count=1)
                    if n:
                        used.append(c)
    if used:
        from . import roster
        page = roster.ensure(page.replace("</body>", assets(geo_subset(geo, sorted(set(used)))) + "\n</body>", 1))
    return page


def page(series, linker, template):
    """build/congress.html: every Congress in congress/."""
    from . import elections
    elections.SERIES = specials.SERIES = series      # the candidates' name entries
    data, geo = load()
    if not data or not geo:
        return None
    ptr = Pointers(series, linker, data)
    href = lambda key, eid: f"{key}.html#{eid}"
    rid = lambda c, ch, st, seat: f"cg{c}-{ch}-{st}-{seat}"
    tagged = {}
    for lst in series.lists.values():
        if lst.kind == "calendar":
            for sec, e in lst.entries():
                for t in e.get("tags", []):
                    if t.startswith("congress:"):
                        tagged[int(t.split(":")[1])] = e
    main = ["<h1>Elections, 1958–1974, and Congress at each opening, 1961–1973</h1>",
            '<p class="lede">Every general election from 1958 (the 86th Congress) to 1974 (the 94th): every House and Senate '
            'race, and in presidential years the vote for President and the Electors\' ballots; with them, the States\' '
            'elections for governor, 1960–66, and the legislatures they chose, 1959–67. After each, the House and Senate on '
            'the day the Congress convened, from the 87th to the 93rd: the party division, the districts and states, and every '
            'member, with pointers to the lists and the calendar; then the special elections during the Congress.</p>',
            '<p class="logic">Members from <a href="https://github.com/unitedstates/congress-legislators">unitedstates/congress-legislators</a>, '
            'corrected by hand where noted in the rosters (terms missing from the source, seats vacant at the opening). '
            'District shapes from Jeffrey B. Lewis et al., <a href="https://cdmaps.polisci.ucla.edu">United States Congressional District Shapefiles</a>, '
            'simplified. Delegates and resident commissioners are not shown.</p>',
            '<p class="logic">Pointers: the list and section where the member appears in Part III or as the subject of a memoir or '
            'biography, matched on surname and first given name; and the calendar entries that name the member. '
            'The calendar runs January 1961 to January 1963.</p>',
            '<nav class="toc" aria-label="Contents">\n<h3 id="contents" style="border-top:0;margin-top:1.5rem" data-short="Contents">Contents</h3>\n<ol id="tocList"></ol>\n</nav>']
    from . import elections, governors, legislatures
    governors.SERIES = series
    edata = elections.load()
    etag = elections.tagged(series)
    gdates = sorted({r["date"] for r in governors.load().get("races") or []})
    sessions = legislatures.sessions()

    def state_blocks(c, y, after_election):
        """The States' elections in the Congress's span: with the federal election (after_election), the governors
        chosen that day and the legislatures it chose; else the governors chosen between (the odd years)."""
        out = []
        day = str(edata[y]["date"]) if y in edata else f"{y}-11-99"
        nxt = str(edata[y + 2]["date"]) if y + 2 in edata else f"{y + 2}-11-99"
        for d in gdates:
            if (d == day) if after_election else (day < d < nxt):
                out.append(f'<h3 id="gv{d}" data-short="Governors, {d[:4]}">Governors, {esc(governors.fmt_date(d))}</h3>')
                out.append(governors.block(d))
        if after_election and y + 1 in sessions:
            out.append(f'<h3 id="lg{y + 1}h" data-short="Legislatures, {y + 1}">The State legislatures in session, {y + 1}</h3>')
            out.append(legislatures.block(y + 1))
        return out
    shown = sorted(set(data) | {87 + (y - 1960) // 2 for y in edata if y >= 1958} | {c for c in specials.load() if c >= 85})
    for c in shown:
        main.append(f'<h2 id="c{c}" data-short="{ordinal(c)}">{ordinal(c)} Congress, {YEARS[c]}</h2>')
        y = 1960 + 2 * (c - 87)
        if y in edata:
            main.append(f'<h3 id="e{y}" data-short="Election of {y}">The election, {esc(fmt_date(edata[y]["date"]))}</h3>')
            if y in etag:
                main.append(f'<p class="logic">In the calendar: <a href="cal.html#{etag[y]["id"]}">{esc(etag[y]["when"])}, {y}</a>.</p>')
            main.append(elections.block(y, edata))
            main += state_blocks(c, y, True)
            if c in data:
                main.append(f'<h3 id="o{c}" data-short="Opening">At the opening</h3>')
        if c not in data:                # no roster (the 86th): its specials still follow its election
            main += state_blocks(c, y, False)
            sp = specials.block(c, edata)
            if sp:
                main.append(f'<h3 id="sp{c}" data-short="Specials">Special elections during the {ordinal(c)} Congress</h3>')
                main.append(sp)
            continue
        if c in tagged:
            main.append(f'<p class="logic">In the calendar: <a href="cal.html#{tagged[c]["id"]}">{esc(tagged[c]["when"])}, {tagged[c]["date"][:4]}</a>.</p>')
        main.append(block(c, data[c], geo, ptr, href, rid, here=True))
        main += state_blocks(c, y, False)
        sp = specials.block(c, edata)
        if sp:
            main.append(f'<h3 id="sp{c}" data-short="Specials">Special elections during the {ordinal(c)} Congress</h3>')
            main.append(sp)
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", "Elections and Congress").replace("{{main}}", "\n".join(main))
    from . import roster
    return roster.ensure(pg.replace("</body>", assets(geo) + "\n</body>", 1))
