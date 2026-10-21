"""The leaders and the standing committees of each Congress, 87th-93rd (congress/committees.yaml, written by
tools/congress/make_committees.py from Garrison Nelson's committee files; the hand corrections in
congress/committees-hand.yaml).

On congress.html, under each Congress at its opening, a Leadership block and a Committees block; a calendar entry
tagged committees:<NN> carries the same two blocks (congress.inject). In each member's roster line his committees
and rank, and a column of his years in the chamber at the opening (congress.block); in his Names entry a section
"Committees" across the Congresses (lives.entry).

STYLE
1. Leadership: one table a chamber, House first: the office, the holder (his name entry and his roster row), the
   party. The offices in the order of OFFICES; a holder who took or left the office during the Congress has the
   change and its date under his name, in the source's words ("Died, Nov. 16, 1961."; "Elected to fill the vacancy,
   Jan. 10, 1962."). Sources under the tables: Nelson for the Senate's floor leaders and whips, the House's and the
   Senate's lists for the rest, each named and linked.
2. Committees: one collapsible table a chamber (details.cgr, as the rosters), one tbody a committee, its anchor
   cm<NN>-<h|s>-<code> (lit as a roster row is). The committee's head row: its name as the Directory prints it, the
   ratio at the first listing (majority-minority, "and 1 other" for a third-party member), the chairman and the
   ranking minority member (where one followed another in the Congress, both, the first with his leaving: "Cannon
   (died May 12, 1964), then Mahon"). Then two columns, Democrats and Republicans (a member of neither party in the
   column of the party he caucused with), each in Nelson's order: the Journal's first listing by rank, then the
   additions and replacements by the date of assignment. A member's cell: his rank (a "+" for an addition or a
   replacement), his name linked to his name entry, his seat (MA-6; a Senator's State) linked to his roster row at the
   opening (the seat's row, for a successor), and, muted, any change: "Added Jan. 31, 1961." (to an enlarged
   committee), "From Jan. 21, 1964." (a replacement), "Died Apr. 14, 1964." A delegate or resident commissioner in
   his place in the ranks, marked so, with no roster link.
3. In a member's roster line, muted: "Committees: Ways and Means, 1st (chairman); Joint ...", each linked to the
   committee's tbody; the rank as an ordinal within his party, the additions and replacements by their date. The
   roster's column "Yrs": whole years served in the chamber before the opening (congress-legislators' terms).
4. Names: "Committees", one item a committee and chamber: "House Ways and Means: 2nd, 87th Cong.; 1st (chairman),
   88th-93rd Cong.", Congresses with the same rank and role run together, each run a pointer to the committee in its
   first Congress; the source once, under the list.
5. Subcommittees, and the select, special and joint committees, are not in Nelson's files for these Congresses: not
   shown (notes/leads.md).
"""
import os
import re
from collections import defaultdict

from . import store

PATH = os.path.join(store.ROOT, "congress", "committees.yaml")
HAND = os.path.join(store.ROOT, "congress", "committees-hand.yaml")
OFFICES = ["Speaker", "President pro tempore", "Majority Leader", "Majority Whip", "Minority Leader", "Minority Whip",
           "Democratic Caucus Chairman", "Democratic Conference Chairman", "Republican Conference Chairman"]
NELSON = ("Garrison Nelson, <i>Committees in the U.S. Congress, 1947–1992</i>, data files (House, 80th–97th "
          "Congresses; Senate, 80th–102nd), on Charles Stewart III's "
          '<a href="https://web.mit.edu/17.251/www/data_page.html">data page</a>')
_cache = {}


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def load():
    if "d" not in _cache:
        _cache["d"] = store.load_yaml(PATH) if os.path.exists(PATH) else {}
    return _cache["d"]


def names():
    return {x["code"]: x["name"] for x in load().get("committees") or []}


def of(c, ch):
    return ((load().get("congress") or {}).get(c) or {}).get(ch) or {}


def ordinal(n):
    return f"{n}{'th' if 11 <= n % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def fmt(d):
    from .congress import fmt_date
    return fmt_date(d)


def rid(c, ch, code):
    return f"cm{c}-{ch}-{code}"


def roster_rid(c, ch, st, seat):
    return f"cg{c}-{ch}-{st}-{seat}"


def surname(name):
    return re.sub(r"\s*\([^)]*\)", "", name).split(",")[0].strip()


def seat_label(ch, st, seat):
    return f"{st}-{'AL' if seat == 0 else seat}" if ch == "h" else st


def column(m):
    """'D' or 'R': the party's column, a third-party member's by the party he caucused with."""
    if m["p"] in ("D", "R"):
        return m["p"]
    from .congress import caucused
    cc = caucused({"party": m["p"], "name": m["name"]})
    return cc[0] if cc else ("D" if m["side"] == "maj" else "R")


def change(m):
    """The member's change on the committee during the Congress, as a sentence: '' where none."""
    out = []
    if m.get("group") == "added":
        out.append(f"Added {fmt(m['from'])}.")
    elif m.get("group") == "repl":
        out.append(f"From {fmt(m['from'])}.")
    if m.get("to"):
        why = (m.get("why") or "left").capitalize()
        out.append(f"{why} {fmt(m['to'])}.")
    return " ".join(out)


def role_word(m):
    r = m.get("role") or ""
    if r.startswith("chair"):
        return "chairman"
    if r.startswith("ranking"):
        return "ranking minority member"
    if r == "acting":
        return "acting chairman"
    return ""


def href_roster(here):
    return "" if here else "congress.html"


# ---------------------------------------------------------------- leadership (STYLE 1)

SRC = {}


def sources():
    if not SRC:
        h = store.load_yaml(HAND) if os.path.exists(HAND) else {}
        SRC.update(h.get("sources") or {})
    return SRC


def leaders_block(c, series, here=False):
    from . import namelinks
    out = [f'<div class="cg cgk" id="ld{c}"><p class="cgh">Leadership, {ordinal(c)} Congress</p>']
    used = []
    for ch, label in (("h", "House"), ("s", "Senate")):
        ls = sorted(of(c, ch).get("leaders") or [], key=lambda x: (OFFICES.index(x["office"]), x.get("from") or ""))
        if not ls:
            continue
        out.append(f'<details class="cgr cml" open><summary>{label}</summary><table>'
                   '<colgroup><col class="c1"><col class="c2"><col class="c3"></colgroup>'
                   '<thead><tr><th>Office</th><th>Holder</th><th>Party</th></tr></thead><tbody>')
        last = None
        for x in ls:
            seat = seat_of(c, ch, x["bio"])
            who = namelinks.a(series, x["name"], esc(x["name"]))
            if seat:
                who += (f' <a class="cmst" href="{href_roster(here)}#{roster_rid(c, ch, x["st"], seat[1])}">'
                        f'{esc(seat_label(ch, x["st"], seat[1]))}</a>')
            notes = []
            if x.get("from"):
                notes.append(f"{x['why']}, {fmt(x['from'])}." if x.get("why") and not x.get("to") else f"From {fmt(x['from'])}.")
            if x.get("to"):
                notes.append(f"{x['why']}, {fmt(x['to'])}." if x.get("why") else f"To {fmt(x['to'])}.")
            if x.get("note"):
                from .markup import to_html
                notes.append(to_html(x["note"]))
            note = f'<span class="cgn cgc">{" ".join(notes)}</span>' if notes else ""
            office = x["office"] if x["office"] != last else ""
            last = x["office"]
            out.append(f'<tr><td>{esc(office)}</td><td>{who}{note}</td><td class="p{x["p"]}t">{esc(x["p"])}</td></tr>')
            if x["src"] not in used:
                used.append(x["src"])
        out.append("</tbody></table></details>")
    cites = []
    if "nelson" in used:
        cites.append("the Senate's floor leaders and whips, " + NELSON)
    pages = [k for k in used if k != "nelson"]
    if pages:
        links = []
        for k in pages:
            s = sources().get(k)
            if s:
                *who, title, url = s
                links.append(f'{esc(", ".join(who))}, <a href="{esc(url)}">{esc(title)}</a>')
        cites.append(("the other offices, " if "nelson" in used else "") + "; ".join(links))
    out.append(f'<p class="cgs">Sources: {"; ".join(cites)}.</p></div>')
    return "\n".join(out)


def seat_of(c, ch, bio):
    """(st, seat) of the member's row in the roster at the opening, or None."""
    key = ("seats", c, ch)
    if key not in _cache:
        d = store.load_yaml(os.path.join(store.ROOT, "congress", f"{c}.yaml")) or {}
        _cache[key] = {r["bio"]: (r["st"], r["d"] if ch == "h" else r["cl"])
                       for r in d.get("house" if ch == "h" else "senate") or [] if r.get("bio")}
    return _cache[key].get(bio)


# ---------------------------------------------------------------- committees (STYLE 2)

def heads(ms, role):
    xs = sorted([m for m in ms if (m.get("role") or "").startswith(role)], key=lambda m: m.get("role"))
    out = []
    for m in xs:
        t = esc(surname(m["name"]))
        if len(xs) > 1 and m.get("to"):
            t += f" ({esc((m.get('why') or 'left'))} {fmt(m['to'])})"
        out.append(t)
    return ", then ".join(out)


def cell(m, c, ch, series, here):
    from . import namelinks
    if not m:
        return "<td></td>"
    rank = f'<span class="cmr">{m["rank"] if "group" not in m else "+"}</span>'
    who = namelinks.a(series, m["name"], esc(m["name"])) if not m.get("delegate") else esc(m["name"])
    if m.get("delegate"):
        seat = f' <span class="cmst">{esc(m["st"])}, {"Resident Commissioner" if m["st"] == "PR" else "Delegate"}</span>'
    else:
        seat = (f' <a class="cmst" href="{href_roster(here)}#{roster_rid(c, ch, m["st"], m["seat"])}">'
                f'{esc(seat_label(ch, m["st"], m["seat"]))}</a>')
    rw = role_word(m)
    role = f' <span class="cmrole">({rw})</span>' if rw else ""
    ch_ = change(m)
    note = f'<span class="cgn cgc">{esc(ch_)}</span>' if ch_ else ""
    gone = ' class="cmgone"' if m.get("to") else ""
    return f"<td{gone}>{rank}{who}{seat}{role}{note}</td>"


def committees_block(c, series, here=False):
    nm = names()
    out = [f'<div class="cg cgk" id="cm{c}"><p class="cgh">Committees, {ordinal(c)} Congress</p>']
    for ch, label in (("h", "House"), ("s", "Senate")):
        cs = of(c, ch).get("committees") or {}
        if not cs:
            continue
        out.append(f'<details class="cgr cmc"><summary>{label} standing committees, {len(cs)}</summary><table>'
                   '<colgroup><col class="c1"><col class="c2"></colgroup>'
                   '<thead><tr><th>Democrats</th><th>Republicans</th></tr></thead>')
        for code in sorted(cs, key=lambda k: nm[k]):
            ms = cs[code]
            orig = [m for m in ms if "group" not in m]
            maj = sum(1 for m in orig if m["side"] == "maj")
            mn = sum(1 for m in orig if m["side"] == "min")
            oth = sum(1 for m in orig if m["side"] == "oth")
            ratio = f"{maj}–{mn}" + (f" and {oth} other" if oth == 1 else f" and {oth} others" if oth else "")
            bits = [ratio]
            ch_ = heads(ms, "chair")
            if ch_:
                bits.append(f"Chairman: {ch_}")
            rk = heads(ms, "ranking")
            if rk:
                bits.append(f"Ranking minority member: {rk}")
            out.append(f'<tbody id="{rid(c, ch, code)}"><tr class="st"><th colspan="2">{esc(nm[code])} '
                       f'<span class="cgsm">{". ".join(bits)}.</span></th></tr>')
            cols = {"D": [], "R": []}
            for m in ms:
                cols[column(m)].append(m)
            for i in range(max(len(cols["D"]), len(cols["R"]))):
                d = cols["D"][i] if i < len(cols["D"]) else None
                r = cols["R"][i] if i < len(cols["R"]) else None
                out.append(f"<tr>{cell(d, c, ch, series, here)}{cell(r, c, ch, series, here)}</tr>")
            out.append("</tbody>")
        out.append("</table></details>")
    out.append(f'<p class="cgs">The standing committees: {NELSON}; its ranks are the House and Senate '
               "<i>Journals</i>' listing at the first session, then the additions and replacements by date. Seats link "
               "to the roster at the opening.</p></div>")
    return "\n".join(out)


def blocks(c, series, here=False):
    if not of(c, "h") and not of(c, "s"):
        return ""
    return leaders_block(c, series, here) + "\n" + committees_block(c, series, here)


# ---------------------------------------------------------------- the roster line (STYLE 3)

def by_member(c, ch):
    key = ("bym", c, ch)
    if key not in _cache:
        idx = defaultdict(list)
        for code, ms in (of(c, ch).get("committees") or {}).items():
            for m in ms:
                if m.get("bio"):
                    idx[m["bio"]].append((code, m))
        nm = names()
        for v in idx.values():
            v.sort(key=lambda x: ("group" in x[1], x[1]["from"] if "group" in x[1] else "", nm[x[0]]))
        _cache[key] = idx
    return _cache[key]


def years(c, ch, bio):
    return (of(c, ch).get("years") or {}).get(bio)


def label(m):
    """'1st (chairman)'; 'from Jan. 21, 1964'; with ', to Apr. 14, 1964' where he left."""
    t = ordinal(m["rank"]) if "group" not in m else f"from {fmt(m['from'])}"
    rw = role_word(m)
    if rw:
        t += f" ({rw})"
    if m.get("to"):
        t += f", to {fmt(m['to'])}"
    return t


def roster_line(c, ch, bio, here=False):
    xs = by_member(c, ch).get(bio) or []
    if not xs:
        return ""
    nm = names()
    pre = "#" if here else "congress.html#"
    items = [f'<a href="{pre}{rid(c, ch, code)}">{esc(nm[code])}</a>, {esc(label(m))}' for code, m in xs]
    return f'<span class="cgn cgel cmln">Committees: {"; ".join(items)}.</span>'


# ---------------------------------------------------------------- Names (STYLE 4)

def person_items(rp, names_=(), site=""):
    """The person's committees across the Congresses, from his roster rows (rp: lives.roster_pointers) and any row
    whose name is one of his names. Returns (items, foot)."""
    from .congress import ordinal as cord
    bios = set()
    for x in rp:
        c, ch, st, seat = x[1], x[2], x[3], x[5]
        for b, s in ((b, s) for b, s in _seats(c, ch).items()):
            if s == (st, seat):
                bios.add(b)
    nm = names()
    runs = defaultdict(list)       # (ch, code) -> [(c, label)]
    for c in sorted((load().get("congress") or {})):
        for ch in ("h", "s"):
            for code, ms in (of(c, ch).get("committees") or {}).items():
                for m in ms:
                    if m.get("bio") in bios or (not m.get("bio") and m["name"] in names_) or \
                            (m["name"] in names_ and m.get("bio") in bios | {None}):
                        runs[(ch, code)].append((c, label(m)))
    items = []
    order = sorted(runs, key=lambda k: (min(c for c, _ in runs[k]), k[0] != "h", nm[k[1]]))
    for ch, code in order:
        seq = sorted(set(runs[(ch, code)]))
        groups = []
        for c, lab in seq:
            if groups and groups[-1][1] == lab and groups[-1][0][-1] == c - 1 and "from " not in lab and ", to " not in lab:
                groups[-1][0].append(c)
            else:
                groups.append(([c], lab))
        parts = []
        for cs, lab in groups:
            span = f"{cord(cs[0])}–{cord(cs[-1])} Cong." if len(cs) > 1 else f"{cord(cs[0])} Cong."
            parts.append(f'{esc(lab)}, <a class="lvp" href="{site}congress.html#{rid(cs[0], ch, code)}">{span}</a>')
        items.append(f'{"House" if ch == "h" else "Senate"} {esc(nm[code])}: {"; ".join(parts)}')
    foot = [f"Committees from {NELSON}."] if items else []
    return items, foot


def _seats(c, ch):
    seat_of(c, ch, None)
    return _cache[("seats", c, ch)]


# ---------------------------------------------------------------- styles

CSS = """<style id="cmte-css">
/* Leadership and committees (tools/bib/committees.py): the roster tables' rules (templates/roster.css), their own
   columns here */
details.cml col.c1{width:34%}details.cml col.c3{width:3rem}
details.cml td:nth-child(3){font-weight:700}
details.cmc col.c1,details.cmc col.c2{width:50%}
details.cmc tr.st th .cgsm{display:block;font-size:.78rem;font-family:var(--sans);margin-top:.1rem}
.cg .cmr{display:inline-block;min-width:1.5em;color:var(--muted);font-variant-numeric:tabular-nums}
.cg a.cmst,.cg span.cmst{font-size:.76rem;color:var(--muted);text-decoration-color:color-mix(in srgb,var(--muted) 45%,transparent)}
.cg .cmrole{font-size:.8rem;color:var(--muted)}
.cg td.cmgone>a.nm,.cg td.cmgone{color:var(--muted)}
.cgn.cmln a{color:inherit}
details.cgm col.c3b{width:2.4rem}
details.cgm td.cmy{color:var(--muted);font-variant-numeric:tabular-nums}
</style>
"""


def ensure(page):
    if 'id="cmte-css"' in page:
        return page
    return page.replace("</head>", CSS + "</head>", 1) if "</head>" in page else CSS + page


# ---------------------------------------------------------------- check

def problems(series=None):
    """check: the file loads; every committee code named; ranks consecutive within side and group (the additions
    numbered on from the first listing); every member a roster member at the opening or the successor the changes
    give for his seat; every leader a member; one chairman at least on each committee."""
    out = []
    if not os.path.exists(PATH):
        return out
    d = load()
    nm = names()
    chg = store.load_yaml(os.path.join(store.ROOT, "congress", "changes.yaml")) or {}
    for c, chs in (d.get("congress") or {}).items():
        roster = store.load_yaml(os.path.join(store.ROOT, "congress", f"{c}.yaml")) or {}
        for ch, key in (("h", "house"), ("s", "senate")):
            bios = {r["bio"] for r in roster.get(key) or [] if r.get("bio")}
            later = [x for x in chg.get(c) or [] if x["ch"] == ch]

            def resolves(m):
                if m.get("bio") in bios:
                    return True
                sur = store.fold(surname(m["name"]))
                return any(x["st"] == m["st"] and x["seat"] == m.get("seat") and x.get("into") and
                           sur in store.fold(x["into"]) for x in later)
            cc = chs.get(ch) or {}
            for code, ms in (cc.get("committees") or {}).items():
                where = f"committees: {c}th Congress, {'House' if ch == 'h' else 'Senate'} {nm.get(code, code)}"
                if code not in nm:
                    out.append(("error", f"{where}: code {code} not in the committee list"))
                for side in ("maj", "min", "oth"):
                    orig = sorted(m["rank"] for m in ms if m["side"] == side and "group" not in m)
                    add = sorted(m["rank"] for m in ms if m["side"] == side and m.get("group") == "added")
                    rep = sorted(m["rank"] for m in ms if m["side"] == side and m.get("group") == "repl")
                    if orig != list(range(1, len(orig) + 1)):
                        out.append(("error", f"{where}: {side} ranks not consecutive: {orig}"))
                    if add and add != list(range(len(orig) + 1, len(orig) + len(add) + 1)):
                        out.append(("error", f"{where}: {side} additions not numbered on from the listing: {add}"))
                    if rep != list(range(1, len(rep) + 1)):
                        out.append(("error", f"{where}: {side} replacements not consecutive: {rep}"))
                for m in ms:
                    if not m.get("delegate") and not resolves(m):
                        out.append(("error", f"{where}: {m['name']} ({m['st']}) is in neither the roster at the "
                                             "opening nor the changes as his seat's successor"))
                if not any((m.get("role") or "").startswith("chair") for m in ms):
                    out.append(("warn", f"{where}: no chairman"))
            for x in cc.get("leaders") or []:
                if x["office"] not in OFFICES:
                    out.append(("error", f"committees: {c}th Congress: unknown office {x['office']}"))
                if not resolves({**x, "seat": None}):
                    out.append(("error", f"committees: {c}th Congress, {x['office']}: {x['name']} not in the roster"))
                if series is not None:
                    from . import namelinks
                    if not namelinks.url(series, x["name"]):
                        out.append(("warn", f"committees: {c}th Congress, {x['office']}: {x['name']} has no name entry"))
    return out
