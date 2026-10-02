"""Each Congress at its opening: party bars, House and Senate maps, rosters.

    congress/<NN>.yaml   the members at the opening (House by state and district,
                         0 = at large; Senate by state and class), editable
    congress/geo.json    district and state shapes, projected (Albers, 960x600)
                         and simplified; generated once from the Lewis district files

A calendar entry tagged congress:<NN> carries that Congress's block, in cal.html
and in the compiled reader; build/congress.html carries all of them.
"""
import json
import os
import re
from collections import Counter, defaultdict

from . import store
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
SHORT = {"samuel": ["sam"], "william": ["bill", "will"], "robert": ["bob"], "thomas": ["tom"], "edward": ["ted", "ed"],
         "james": ["jim"], "michael": ["mike"], "charles": ["charlie"], "richard": ["dick"], "joseph": ["joe"],
         "john": ["jack"], "daniel": ["dan"], "eugene": ["gene"], "frederick": ["fred"], "albert": ["al"],
         "hubert": ["hubert"], "lawrence": ["larry"], "kenneth": ["ken"], "theodore": ["ted"], "henry": ["harry"],
         "everett": ["everett"], "clifford": ["cliff"], "gerald": ["jerry"], "abraham": ["abe"], "barry": ["barry"]}
YEARS = {c: f"{1961 + 2 * (c - 87)}–{str(1963 + 2 * (c - 87))[2:]}" for c in range(87, 94)}


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
        for lst in series.lists.values():
            if lst.kind != "calendar":
                continue
            for sec, e in lst.entries():
                for x in self.named(lst, e):
                    for k, _ in linker.refs.name_keys(x["s"]):
                        if e not in self.cal[k]:
                            self.cal[k].append(e)

    def named(self, lst, e):
        """Part III entries named in a calendar entry's 'Names:' line: by surname
        ("Heller, Tobin (K–J Adm. III.H)"), or, where the line gives only sections
        ("Names: K–J Cong. III.A, III.C"), the people of those sections whose
        surnames appear in the entry."""
        n = plain(e.get("n") or "")
        m = re.search(r"Names: (.*)$", n)
        if not m:
            return []
        out = []
        for g in re.split(r";\s*", m.group(1)):
            gm = re.match(r"^([^()]+?)\s*\(([^)]*)\)", g)
            if gm:
                scanned = list(self.linker.refs.scan(gm.group(2), lst.key))
                if not scanned:
                    continue
                key, codes = scanned[0][2], [c for _, _, k, c in scanned if c]
                for tok in re.split(r",\s*|\s+and\s+", gm.group(1)):
                    if tok.strip():
                        x = self.linker.find_person(tok, key, codes)
                        if x and x not in out:
                            out.append(x)
                continue
            text = plain(e.get("c") or "") + " " + n[:m.start()]
            for _, _, key, code in self.linker.refs.scan(g, lst.key):
                sec = self.linker.refs.section_for(key, code) if code else None
                if not sec:
                    continue
                for x in sec.entries:
                    if not x.get("s") or "," not in x["s"]:
                        continue
                    sur = plain(x["s"]).split(",")[0].strip()
                    if re.search(r"\b" + re.escape(sur) + r"\b", text) and x not in out:
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
            dates, prev = [], None
            for e in cal:
                y = e["date"][:4]
                lab = e["when"] + (f", {y}" if y != prev else "")
                prev = y
                dates.append(f'<a href="{href("cal", e["id"])}">{esc(lab)}</a>')
            out.append("Cal. " + ", ".join(dates))
        return out


# ---------------------------------------------------------------- the block

SOUTH_LINE = ("The eleven Southern States: the thirteen States represented in the Confederate States Congress, "
              "less Missouri and Kentucky.")


def bar(label, rows, senate):
    n = len(rows)
    def kind(r):
        if r.get("vacant"):
            return "vacant"
        if r["party"] == "D":
            return "Ds" if r["st"] in SOUTH else "Dn"
        return r["party"]
    cnt = Counter(kind(r) for r in rows)
    names = {"Dn": "Non-Southern Democrats", "Ds": "Southern Democrats", "vacant": "Vacant"}
    x, segs = 0.0, []
    W = 1000
    for p in ["Dn", "Ds", "ID", "I", "C", "vacant", "R"]:
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
    if cnt.get("vacant"):
        parts.append(f"{cnt['vacant']} vacant")
    cap = f'{label}, {n} seats: ' + ", ".join(parts) + "."
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


def block(c, data, geo, ptr, href, rid):
    """One Congress: bars, two maps, two rosters. rid(c, chamber, st, seat) -> a row id."""
    house, senate = data["house"], data["senate"]
    out = [f'<div class="cg" data-cg="{c}">']
    out.append(f'<p class="cgh">{ordinal(c)} Congress at its opening, {esc(fmt_date(data["opened"]))}</p>')
    out.append(bar("House", house, False))
    out.append(bar("Senate", senate, True))
    out.append(f'<p class="cgsouth">{esc(SOUTH_LINE)}</p>')
    lab = map_labels(house + senate)
    seats = {"h": defaultdict(list), "s": defaultdict(list)}
    for r in house:
        seats["h"][r["st"]].append({"d": r["d"], "p": "V" if r.get("vacant") else r["party"],
                                    "n": lab.get(id(r), "Vacant"), "id": rid(c, "h", r["st"], r["d"])})
    for r in senate:
        seats["s"][r["st"]].append({"cl": r["cl"], "p": "V" if r.get("vacant") else r["party"],
                                    "n": lab.get(id(r), "Vacant"), "id": rid(c, "s", r["st"], r["cl"])})
    out.append(f'<script type="application/json" class="cgseats">{json.dumps(seats, ensure_ascii=False, separators=(",", ":"))}</script>')
    out.append('<div class="cgmaps">'
               f'<figure class="cgmap dots" data-chamber="h"><figcaption>House, by delegation</figcaption></figure>'
               f'<figure class="cgmap" data-chamber="s"><figcaption>Senate, by state</figcaption></figure></div>')
    out.append('<p class="cgkey"><span class="sw pD"></span>Democratic <span class="sw pR"></span>Republican '
               '<span class="sw pO"></span>Other <span class="sw pV"></span>Vacant <span class="sw pX"></span>Split delegation. '
               'Dots: at-large seats beside districts. Zoom with the buttons, a double-click, a pinch, or Ctrl-scroll; drag to pan. Click a district for its representatives, a state for its senators. Delegations, under the House map: a dot a seat, a block a State; hover a dot for its district, click to go to it, click another district to move there, double-click white space to come back.</p>')
    for ch, rows, label in (("h", house, "House"), ("s", senate, "Senate")):
        out.append(f'<details class="cgr"><summary>{label} members, {len(rows)}, by state</summary><table>'
                   '<colgroup><col class="c1"><col class="c2"><col class="c3"><col class="c4"></colgroup>')
        out.append(f'<thead><tr><th>{"District" if ch == "h" else "Class"}</th><th>Member</th><th>Party</th><th>In the series</th></tr></thead><tbody>')
        bystate = defaultdict(list)
        for r in rows:
            bystate[r["st"]].append(r)
        for st in sorted(bystate, key=lambda s: STATE[s]):
            out.append(f'<tr class="st"><th colspan="4">{STATE[st]}</th></tr>')
            for r in bystate[st]:
                seat = r["d"] if ch == "h" else r["cl"]
                lab = ("At large" if seat == 0 else str(seat)) if ch == "h" else ("I", "II", "III")[seat - 1]
                if r.get("vacant"):
                    who, party, pts = "<i>Vacant</i>", "", []
                else:
                    who, party = esc(r["name"]), r["party"]
                    pts = ptr.lines(r["name"], href)
                note = f'<span class="cgn">{to_html(r["n"])}</span>' if r.get("n") else ""
                out.append(f'<tr id="{rid(c, ch, r["st"], seat)}"><td>{lab}</td><td>{who}{note}</td>'
                           f'<td class="p{party or "V"}t">{party}</td><td>{"; ".join(pts)}</td></tr>')
        out.append("</tbody></table></details>")
    out.append("</div>")
    return "\n".join(out)


MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]


def fmt_date(d):
    y, m, dd = str(d).split("-")
    return f"{MONTHS[int(m) - 1]} {int(dd)}, {y}"


def geo_subset(geo, cs):
    """The shapes the given Congresses use, plus state outlines and centers."""
    keys = {k for c in cs for st in geo["congress"][str(c)].values() for k in st.values()}
    return {"shapes": {k: geo["shapes"][k] for k in keys},
            "congress": {str(c): geo["congress"][str(c)] for c in cs},
            "states": geo["states"], "centers": geo["centers"]}


ASSETS = os.path.join(store.ROOT, "templates", "congress.html")


def assets(geo):
    """CSS and JS for the blocks, with the geometry they need."""
    t = open(ASSETS, encoding="utf-8").read()
    return t.replace("{{geo}}", json.dumps(geo, separators=(",", ":")))


def inject(page, series, linker, mode):
    """Put each tagged calendar entry's Congress block into a built page."""
    data, geo = load()
    if not data or not geo:
        return page
    ptr = Pointers(series, linker, data)
    href = (lambda key, eid: f"#{eid}") if mode == "series" else (lambda key, eid: f"{key}.html#{eid}" if key != "cal" else f"#{eid}")
    rid = lambda c, ch, st, seat: f"cg{c}-{ch}-{st}-{seat}"
    used = []
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for sec, e in lst.entries():
            for t in e.get("tags", []):
                m = re.match(r"^congress:(\d+)$", t)
                if m and int(m.group(1)) in data:
                    c = int(m.group(1))
                    blk = block(c, data[c], geo, ptr, href, rid)
                    pat = re.compile(r'(<li id="' + re.escape(e["id"]) + r'"[^>]*>.*?)(</li>)', re.S)
                    page, n = pat.subn(lambda mm: mm.group(1) + blk + mm.group(2), page, count=1)
                    if n:
                        used.append(c)
    if used:
        page = page.replace("</body>", assets(geo_subset(geo, used)) + "\n</body>", 1)
    return page


def page(series, linker, template):
    """build/congress.html: every Congress in congress/."""
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
    main = ["<h1>Congress at each opening, 1961–1973</h1>",
            '<p class="lede">The House and Senate on the day each Congress convened, from the 87th to the 93rd: '
            'the party division, the districts and states, and every member, with pointers to the lists and the calendar.</p>',
            '<p class="logic">Members from <a href="https://github.com/unitedstates/congress-legislators">unitedstates/congress-legislators</a>, '
            'corrected by hand where noted in the rosters (terms missing from the source, seats vacant at the opening). '
            'District shapes from Jeffrey B. Lewis et al., <a href="https://cdmaps.polisci.ucla.edu">United States Congressional District Shapefiles</a>, '
            'simplified. Delegates and resident commissioners are not shown.</p>',
            '<p class="logic">Pointers: the list and section where the member appears in Part III or as the subject of a memoir or '
            'biography, matched on surname and first given name; and the calendar entries that name the member. '
            'The calendar runs January 1961 to January 1963.</p>',
            '<nav class="toc" aria-label="Contents">\n<h3 id="contents" style="border-top:0;margin-top:1.5rem" data-short="Contents">Contents</h3>\n<ol id="tocList"></ol>\n</nav>']
    for c in sorted(data):
        main.append(f'<h2 id="c{c}" data-short="{ordinal(c)}">{ordinal(c)} Congress, {YEARS[c]}</h2>')
        if c in tagged:
            main.append(f'<p class="logic">In the calendar: <a href="cal.html#{tagged[c]["id"]}">{esc(tagged[c]["when"])}, {tagged[c]["date"][:4]}</a>.</p>')
        main.append(block(c, data[c], geo, ptr, href, rid))
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", "Congress at each opening, 1961–1973").replace("{{main}}", "\n".join(main))
    return pg.replace("</body>", assets(geo) + "\n</body>", 1)
