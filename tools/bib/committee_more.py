"""The select, special and joint committees of each Congress, 87th-93rd (congress/committees-cdir.yaml, from the
Congressional Directory), and the subcommittees of the 87th and 88th (congress/subcommittees.yaml, from the
Congressional Staff Directory): rendered after the standing committees (tools/bib/committee_rosters.py), in a member's
roster line and his Names entry, and the hearings calendar's links to them.

STYLE
1. Under "Committees, NNth Congress", after the standing committees, folded like them (details.cgr, closed): "Senate
   select and special committees, N", "House select and special committees, N", "Joint committees, N". One tbody a
   committee, anchored cm<NN>-<s|h|j>-<code> as the standing ones are: its name as the hearings calendar gives it
   (the Directory's longer form on hover), the ratio, the chairman and vice chairman; then Democrats and Republicans
   side by side in the order printed, each his name entry's link and his seat (a joint committee's Senator by his
   State, a Representative by his district: the seat says the chamber), linked to his roster row; an officer named
   by his office (the Secretary of the Treasury) under the table's rows, unlinked. The source under the tables: the
   Directory's edition, its page for each committee in the head row.
2. Subcommittees: "Senate subcommittees, N", "House subcommittees, N", "Joint committees' subcommittees, N", folded,
   closed: a table of one column, a group row a parent committee (linked to its tbody above), then a row a
   subcommittee, anchored sc<NN>-<s|h|j>-<code>-<n>: its name, then on the same line, muted, its chairman, and the
   members by party, "D: Eastland, Johnston ... R: Aiken ...", each surname linked to the name entry; a
   subcommittee's "check" (what the rules could not settle) muted after it, and its page in the Staff Directory,
   linked. Text, not columns: nothing wider than the column at 400px. A Congress with no list read says so in one
   line.
3. A member's roster line ("Committees: ...", committee_rosters STYLE 3) goes on with his select, special and joint
   committees, each linked, his rank as there; not his subcommittees (they are in his Names entry).
4. Names: "Committees" goes on with an item a select, special or joint committee ("Joint Committee on Atomic Energy:
   3rd (chairman), 87th-88th Cong."), and one a Congress for his subcommittees ("Subcommittees, 87th Cong.: House
   Agriculture: Wheat (chairman), Cotton"), each subcommittee linked to its row; the sources once under the list.
5. The hearings calendar: a meeting's committee is linked to its tbody on congress.html in the Congress of the day,
   where that Congress's list holds the code; its subcommittee to its row where the name read (or its beginning,
   where the OCR cut it short: one subcommittee of the committee begins so) is one of the committee's in that
   Congress (link_for, sub_for).
"""
import datetime
import os
import re
from collections import defaultdict

from . import store

CDIR = os.path.join(store.ROOT, "congress", "committees-cdir.yaml")
SUBS = os.path.join(store.ROOT, "congress", "subcommittees.yaml")
CHL = {"s": "Senate", "h": "House", "j": "Joint"}
_cache = {}


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def cdir():
    if "c" not in _cache:
        _cache["c"] = store.load_yaml(CDIR) if os.path.exists(CDIR) else {}
    return _cache["c"]


def subs():
    if "s" not in _cache:
        _cache["s"] = store.load_yaml(SUBS) if os.path.exists(SUBS) else {}
    return _cache["s"]


# committees the hearings calendar holds that no Directory read lists (the 86th's, or one created and gone between two
# editions): in the committee list by the Digest's name, with no table of members
DIGEST_ONLY = {"s.select-committee-on-national-water-resources": "Select Committee on National Water Resources",
               "h.select-committee-on-export-control": "Select Committee on Export Control",
               "s.unread": "committee (name unread)", "h.unread": "committee (name unread)",
               "j.unread": "committee (name unread)"}


def names():
    """{code: name}: the select, special and joint committees, for the committee list (committee_rosters.names); and
    DIGEST_ONLY."""
    out = dict(DIGEST_ONLY)
    out.update({x["code"]: x["name"] for x in cdir().get("committees") or []})
    return out


def of(c, ch):
    return ((cdir().get("congress") or {}).get(c) or {}).get(ch) or {}


def subs_of(c, ch):
    return ((subs().get("congress") or {}).get(c) or {}).get(ch) or {}


def congress_on(day):
    """The Congress whose opening (congress/<NN>.yaml) is the last on or before the day ('1963-05-01' -> 88); the
    86th before Jan. 3, 1961."""
    if "open" not in _cache:
        import glob
        _cache["open"] = sorted((str((store.load_yaml(f) or {}).get("opened")), int(os.path.basename(f)[:2]))
                                for f in glob.glob(os.path.join(store.ROOT, "congress", "[0-9][0-9].yaml")))
    hit = [c for o, c in _cache["open"] if o <= str(day)]
    return hit[-1] if hit else 86


def surname(name):
    return re.sub(r"\s*\([^)]*\)", "", name).split(",")[0].strip()


def ordinal(n):
    return f"{n}{'th' if 11 <= n % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def col(m):
    if m.get("p") in ("D", "R"):
        return m["p"]
    from .congress import caucused
    cc = caucused({"party": m.get("p") or "?", "name": m["name"]})
    return cc[0] if cc else "D"


def seat(c, m, here):
    from .committee_rosters import roster_rid, seat_label, href_roster
    ch = m.get("ch") or "s"
    if m.get("seat") is None or not m.get("st"):
        return ""
    return (f' <a class="cmst" href="{href_roster(here)}#{roster_rid(c, ch, m["st"], m["seat"])}">'
            f'{esc(seat_label(ch, m["st"], m["seat"]))}</a>')


ROLE = {"chair": "chairman", "vice": "vice chairman", "cochair": "cochairman"}


# ---------------------------------------------------------------- select, special, joint (STYLE 1)

def other_block(c, series, here=False):
    from . import namelinks
    from .committee_rosters import rid
    ed = (cdir().get("editions") or {}).get(c)
    out = []
    for ch, label in (("s", "Senate select and special committees"), ("h", "House select and special committees"),
                      ("j", "Joint committees")):
        cs = of(c, ch)
        if not cs:
            continue
        out.append(f'<details class="cgr cmc"><summary>{label}, {len(cs)}</summary><table>'
                   '<colgroup><col class="c1"><col class="c2"></colgroup>'
                   '<thead><tr><th>Democrats</th><th>Republicans</th></tr></thead>')
        for code in sorted(cs, key=lambda k: cs[k]["name"]):
            r = cs[code]
            ms = r["members"]
            cnt = defaultdict(int)
            for m in ms:
                cnt[col(m)] += 1
            bits = [f'{cnt["D"]}–{cnt["R"]}']
            for role in ("chair", "cochair", "vice"):
                who = [surname(m["name"]) for m in ms if m.get("role") == role]
                if who:
                    bits.append(f'{ROLE[role].capitalize()}: {esc(", ".join(who))}')
            e_ = r.get("edition") or (ed or {}).get("edition")
            url = f"https://www.govinfo.gov/content/pkg/CDIR-{e_}/pdf/CDIR-{e_}.pdf"
            pg = (f' <a class="cmst" href="{esc(url)}#page={r["pdf"]}" title="Congressional Directory, '
                  f'{esc(ed_label(e_))}">CDir. {esc(r.get("page") or "")}</a>' if e_ and r.get("pdf") else "")
            title = f' title="{esc(r["printed"])}"' if r.get("printed") else ""
            out.append(f'<tbody id="{rid(c, ch, code)}"><tr class="st"><th colspan="2"><span{title}>{esc(r["name"])}'
                       f'</span>{pg} <span class="cgsm">{". ".join(bits)}.</span></th></tr>')
            cols = {"D": [m for m in ms if col(m) == "D"], "R": [m for m in ms if col(m) == "R"]}
            for i in range(max(len(cols["D"]), len(cols["R"]))):
                cells = []
                for k in ("D", "R"):
                    m = cols[k][i] if i < len(cols[k]) else None
                    if not m:
                        cells.append("<td></td>")
                        continue
                    who = namelinks.a(series, m["name"], esc(m["name"])) if m.get("bio") else esc(m["name"])
                    rw = ROLE.get(m.get("role"))
                    role = f' <span class="cmrole">({rw})</span>' if rw else ""
                    ex = ' <span class="cmrole">(ex officio)</span>' if m.get("ex_officio") else ""
                    cells.append(f'<td><span class="cmr">{i + 1}</span>{who}{seat(c, m, here)}{role}{ex}</td>')
                out.append(f"<tr>{''.join(cells)}</tr>")
            for o in r.get("others") or []:
                out.append(f'<tr><td colspan="2"><span class="cmr"></span>{esc(o["name"])}, '
                           f'<span class="cmrole">{esc(o["office"])}</span></td></tr>')
            out.append("</tbody>")
        out.append("</table></details>")
    if out and ed:
        out.append(f'<p class="cgs">The select, special and joint committees: <i>Official Congressional Directory</i>, '
                   f'{esc(ed_label(ed["edition"]))} (<a href="{esc(ed["url"])}">govinfo</a>), the members in the order '
                   'printed, the party the roster\'s; a committee created later in the Congress from the second '
                   'session\'s edition (its page link says which).</p>')
    return "\n".join(out)


def ed_label(e):
    from .congress import fmt_date
    return fmt_date(e)


# ---------------------------------------------------------------- subcommittees (STYLE 2)

def sub_rid(c, ch, code, n):
    return f"sc{c}-{ch}-{code}-{n}"


def all_names():
    from .committee_rosters import names as nn
    return nn()


def subs_block(c, series, here=False):
    from . import namelinks
    from .committee_rosters import rid, href_roster
    nm = all_names()
    ed = (subs().get("editions") or {}).get(c)
    out = []
    for ch, label in (("s", "Senate subcommittees"), ("h", "House subcommittees"),
                      ("j", "Joint committees' subcommittees")):
        cs = subs_of(c, ch)
        if not cs:
            continue
        n = sum(len(v) for v in cs.values())
        out.append(f'<details class="cgr cms"><summary>{label}, {n}</summary><table><colgroup><col></colgroup>')
        for code in sorted(cs, key=lambda k: nm.get(k, str(k))):
            pre = "" if ch == "j" or str(nm.get(code, "")).startswith(("Select", "Special")) else f"{CHL[ch]} "
            out.append(f'<tbody><tr class="st"><th><a href="{"#" if here else "congress.html#"}{rid(c, ch, code)}">'
                       f'{esc(pre + nm.get(code, str(code)))}</a></th></tr>')
            for i, s in enumerate(cs[code], 1):
                parts = []
                chair = [m for m in s["members"] if m.get("role") == "chair"]
                if chair:
                    parts.append("Chairman: " + link(series, chair[0]))
                for side, lab in (("maj", "D"), ("min", "R")):
                    ms = [m for m in s["members"] if m["side"] == side]
                    if ms:
                        parts.append(f"{lab}: " + ", ".join(link(series, m) for m in ms))
                src = (f' <a class="cmst" href="{esc(s["url"])}">CSD {esc(s.get("page") or "")}</a>'
                       if s.get("url") else "")
                ck = f' <span class="cgc">Check: {esc(s["check"])}.</span>' if s.get("check") else ""
                out.append(f'<tr id="{sub_rid(c, ch, code, i)}"><td><span class="cmsn">{esc(s["name"])}</span> '
                           f'<span class="cgn cmsm">{". ".join(parts)}.{src}{ck}</span></td></tr>')
            out.append("</tbody>")
        out.append("</table></details>")
    if out and ed:
        out.append(f'<p class="cgs">The subcommittees: <i>{esc(ed["title"])}</i> (Charles B. Brownson), the Digital '
                   f'Library of India\'s scan on <a href="{esc(ed["url"])}">archive.org</a>, read by its OCR; the '
                   'members by surname, as printed, each matched to his committee\'s members (tools/congress/'
                   'make_subcommittees.py). The <i>Congressional Directory</i> printed no subcommittees until Dec. '
                   '1971.</p>')
    elif not out:
        out.append('<p class="cgs">Subcommittees: none read for this Congress. The <i>Congressional Directory</i> '
                   'printed none until Dec. 1971; no open copy of the <i>Congressional Staff Directory</i> for it '
                   'was found.</p>')
    return "\n".join(out)


def link(series, m):
    from . import namelinks
    t = esc(surname(m["name"]))
    if m.get("bio"):
        t = namelinks.a(series, m["name"], t)
    if m.get("role") == "chair":
        t += ""
    return t


def blocks(c, series, here=False):
    """The select, special and joint committees, then the subcommittees (STYLE 1-2): after the standing ones."""
    a, b = other_block(c, series, here), subs_block(c, series, here)
    return "\n".join(x for x in (a, b) if x)


# ---------------------------------------------------------------- the roster line (STYLE 3)

def by_member(c, ch):
    key = ("bym", c, ch)
    if key not in _cache:
        idx = defaultdict(list)
        for cch in ("s", "h", "j"):
            for code, r in of(c, cch).items():
                for m in r["members"]:
                    if m.get("bio") and (m.get("ch") or cch) == ch:
                        idx[m["bio"]].append((cch, code, r, m))
        _cache[key] = idx
    return _cache[key]


def rank_label(m):
    t = ordinal(m["rank"])
    rw = ROLE.get(m.get("role"))
    return t + (f" ({rw})" if rw else "")


def roster_items(c, ch, bio, here=False):
    """The member's select, special and joint committees, for his roster line: ['<a>Name</a>, 3rd'] ."""
    from .committee_rosters import rid
    pre = "#" if here else "congress.html#"
    return [f'<a href="{pre}{rid(c, cch, code)}">{esc(r["name"])}</a>, {esc(rank_label(m))}'
            for cch, code, r, m in sorted(by_member(c, ch).get(bio) or [], key=lambda x: x[2]["name"])]


# ---------------------------------------------------------------- Names (STYLE 4)

def person_items(bios, site=""):
    """(items, foot): his select, special and joint committees across the Congresses, then his subcommittees, a
    Congress an item (STYLE 4)."""
    from .committee_rosters import rid
    from .congress import ordinal as cord
    runs = defaultdict(list)
    names_ = {}
    for c in sorted((cdir().get("congress") or {})):
        for cch in ("s", "h", "j"):
            for code, r in of(c, cch).items():
                for m in r["members"]:
                    if m.get("bio") in bios:
                        runs[(cch, code)].append((c, rank_label(m)))
                        names_[(cch, code)] = r["name"]
    items = []
    for k in sorted(runs, key=lambda k: (min(c for c, _ in runs[k]), names_[k])):
        seq = sorted(set(runs[k]))
        groups = []
        for c, lab in seq:
            if groups and groups[-1][1] == lab and groups[-1][0][-1] == c - 1:
                groups[-1][0].append(c)
            else:
                groups.append(([c], lab))
        parts = []
        for cs, lab in groups:
            span = f"{cord(cs[0])}–{cord(cs[-1])} Cong." if len(cs) > 1 else f"{cord(cs[0])} Cong."
            parts.append(f'{esc(lab)}, <a class="lvp" href="{site}congress.html#{rid(cs[0], k[0], k[1])}">{span}</a>')
        pre = "" if k[0] == "j" else f"{CHL[k[0]]} "
        items.append(f'{esc(pre + names_[k])}: {"; ".join(parts)}')
    nm = all_names()
    sub_items = []
    for c in sorted((subs().get("congress") or {})):
        per = defaultdict(list)
        for ch in ("s", "h", "j"):
            for code, xs in subs_of(c, ch).items():
                for i, s in enumerate(xs, 1):
                    for m in s["members"]:
                        if m.get("bio") in bios:
                            short = re.sub(r"^(?:Special |Select |Permanent |General |Ad Hoc )*Subcommittee (?:on |to )?",
                                           "", s["name"]) or s["name"]
                            lab = (f'<a class="lvp" href="{site}congress.html#{sub_rid(c, ch, code, i)}">'
                                   f'{esc(short)}</a>' + (" (chairman)" if m.get("role") == "chair" else ""))
                            pre = "" if ch == "j" or str(nm.get(code, "")).startswith(("Select", "Special")) \
                                else f"{CHL[ch]} "
                            per[pre + str(nm.get(code, code))].append(lab)
        if per:
            sub_items.append(f"Subcommittees, {cord(c)} Cong.: " +
                             "; ".join(f"{esc(k)}: {', '.join(v)}" for k, v in per.items()))
    foot = []
    if items:
        foot.append("Select, special and joint committees from the <i>Congressional Directory</i>, each Congress's "
                    "first-session edition.")
    if sub_items:
        foot.append("Subcommittees from the <i>Congressional Staff Directory</i>, 1961 and 1963.")
    return items + sub_items, foot


# ---------------------------------------------------------------- the hearings calendar (STYLE 5)

def known(c, ch, code):
    from .committee_rosters import of as std
    if code in (std(c, ch).get("committees") or {}):
        return True
    return code in of(c, ch)


def link_for(x):
    """The committee's anchor on congress.html for a meeting, or None (STYLE 5)."""
    from .committee_rosters import rid
    c = congress_on(x["date"])
    ch = x["ch"].lower()
    if not c or not known(c, ch, x.get("code")):
        return None
    return rid(c, ch, x["code"])


def sub_for(x):
    """The subcommittee's anchor for a meeting's subcommittee, or None (STYLE 5): its name, or the one name of the
    committee's subcommittees that begins with it (the OCR cut it short)."""
    if not x.get("sub"):
        return None
    c = congress_on(x["date"])
    ch = x["ch"].lower()
    xs = subs_of(c, ch).get(x.get("code")) or []
    f = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
    want = f(x["sub"])
    hits = [i for i, s in enumerate(xs, 1) if f(s["name"]) == want]
    if not hits and len(want) >= 12:
        hits = [i for i, s in enumerate(xs, 1) if f(s["name"]).startswith(want)]
    return sub_rid(c, ch, x["code"], hits[0]) if len(hits) == 1 else None


CSS = """<style id="cmte-more-css">
/* select, special and joint committees; subcommittees (tools/bib/committee_more.py) */
details.cms col{width:100%}
details.cms .cmsn{font-weight:600}
details.cms .cmsm{display:inline;margin:0;font-size:.8rem}
details.cms tr.st th a{color:inherit}
</style>
"""


def ensure(page):
    if 'id="cmte-more-css"' in page:
        return page
    return page.replace("</head>", CSS + "</head>", 1) if "</head>" in page else CSS + page


# ---------------------------------------------------------------- check

def problems(series=None):
    """check: the two files load; every committee code in the committee list; every member with a Bioguide id is in
    the roster at the opening or a seat's successor (a warning: the Directory's and the Staff Directory's dates fall
    after the opening); a subcommittee's code is a committee of its Congress; the hearings calendar's committee codes
    all in the list (a warning, by committee)."""
    out = []
    if not os.path.exists(CDIR):
        return out
    d = cdir()
    codes = {x["code"] for x in d.get("committees") or []}
    from .committee_rosters import names as std_names, of as std
    for c, chs in (d.get("congress") or {}).items():
        for ch in ("s", "h", "j"):
            for code, r in (chs.get(ch) or {}).items():
                if code not in codes:
                    out.append(("error", f"committees-cdir: {c}th Congress, {code}: not in its committee list"))
                if not r.get("members"):
                    out.append(("error", f"committees-cdir: {c}th Congress, {r.get('name')}: no members"))
                for m in r.get("members") or []:
                    if not m.get("bio"):
                        out.append(("warn", f"committees-cdir: {c}th Congress, {r['name']}: {m['name']} not joined"))
    for c, chs in ((subs().get("congress") or {}).items()):
        for ch, cs in chs.items():
            for code, xs in cs.items():
                if not (code in (std(c, "h" if ch == "h" else "s").get("committees") or {}) or code in of(c, ch)):
                    out.append(("error", f"subcommittees: {c}th Congress, {ch} {code}: no such committee"))
                for s in xs:
                    if not s.get("members") or not s.get("url"):
                        out.append(("error", f"subcommittees: {c}th Congress, {s.get('name')}: no members or page"))
    allc = set(std_names()) | codes
    from . import committees as H
    seen = set()
    for day, rows in H.load().items():
        for x in rows:
            if x.get("code") not in allc and x.get("name") != "Conferees" and (x["ch"], x["name"]) not in seen:
                seen.add((x["ch"], x["name"]))
    if seen:
        out.append(("warn", f"committees: {len(seen)} committees of the hearings calendar not in the committee list, by "
                            "chamber and name "
                            f"(e.g. {', '.join(sorted(n for _, n in seen)[:3])}) [committee-list]"))
    return out
