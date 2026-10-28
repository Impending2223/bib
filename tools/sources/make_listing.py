"""Write the listings of the States' sources from their registers (deterministic; no network).

    python3 tools/sources/make_listing.py            notes/state-sources.md and notes/state-law-sources.md
    python3 tools/sources/make_listing.py --check    exit 1 if either is stale against its register

notes/state-sources.md, from sources/states.yaml: a section a State; each publication, archival series and county or
city record with its editions, what it prints, its copies and their access as last tested (open; closed: borrow,
bot-check, blocked, dead, other; paper only where no copy is online), the basis of our belief that it exists, and
what the series has used it for: the calendar entries, the specials read (congress/specials-state.yaml), the readings
(elections/readings/), the other election files and the leads that cite it, found by the register's `cited_as`
patterns and its copies' addresses. Then the Check pointers to State records in the calendar, the specials, the
governors' races and the readings, each ruled: the register item it names and that item's basis ("found": a copy
read, a catalog record, a law, a citation; "assumed": no ground yet; "unmatched": it names nothing the register holds).

notes/state-law-sources.md, from sources/state-law.yaml: a section a State; the session laws, the code, the
constitution as then in force, the journals and the attorney general's opinions, with the authority for each and the
copies' access; then the calendar's Check pointers to the journals and the session laws.

STYLE
1. Generated: never edit the .md files; edit the registers and rerun. Each file carries the hash of its register
   (`<!-- register: ... -->`); `./bib check` warns when it no longer matches [state-sources].
2. Matching. A `cited_as` pattern is a Python regular expression, case ignored. One with a space (a title) counts
   only where its State is meant: a calendar entry tagged `state:<xx>`, a specials or readings key of the State, a
   governors race of the State; one without a space (an address, an id) counts anywhere. A copy's address counts
   anywhere, its fragment and page parameters aside (a search page's address never).
3. A match inside a Check sentence ("Check: ...", "check against ...") is a pointer, not a use; "To check:" (the works
   not yet read, CLAUDE.md "Hard and soft") is neither a Check nor a pointer. The sentence runs to
   the next full stop that ends a word of four letters or more, a closing parenthesis or bracket, or an italic title.
   "The State's canvass" (the governors' races) names the State's publications that print the governor's race.
4. Order: States by postal code as the register has them, publications as the register lists them, entries by id.
"""
import argparse
import glob
import hashlib
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "sources", "states.yaml")
LAW = os.path.join(ROOT, "sources", "state-law.yaml")
OUT = os.path.join(ROOT, "notes", "state-sources.md")
LAW_OUT = os.path.join(ROOT, "notes", "state-law-sources.md")
Loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)

NAMES = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
         "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia",
         "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
         "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan",
         "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
         "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
         "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
         "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
         "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
         "WI": "Wisconsin", "WY": "Wyoming"}
GROUNDS = ["seen", "law", "catalog", "cited", "assumed"]
CLOSED = ("borrow", "bot-check", "blocked", "dead", "other")
# what a Check must name to be a pointer to a State's own records (the register's matter)
ELECTION_TERM = re.compile(r"canvass|returns|abstract|tabulation|statement of (the )?vote|official vote|(?-i:Register)\b|"
                           r"manual|blue book|directory|election report|secretary of state|board of (state )?canvassers|"
                           r"election commission|board of elections?|clerk|registrar|supervisor of elections|"
                           r"state archives|state library|historical society|certificate|count book", re.I)
LAW_TERM = re.compile(r"\bjournals?\b|session laws|\bacts of\b|\blaws of\b|statutes|\bcode\b|attorney general's opinion|"
                      r"house journal|senate journal|journal of the", re.I)
ABBR = {"Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "Aug", "Sept", "Oct", "vol", "pp", "ed", "eds", "No", "nos", "St",
        "Mr", "Mrs", "Jr", "Sr", "Co", "Inc", "Leg", "Sess", "Gen", "Rev", "Stat", "Ann", "Ct", "Cal", "Tex", "Pa",
        "Ill", "Mich", "Miss", "Ala", "Fla", "Wis", "Wash", "Ind", "Mass", "Tenn", "Minn", "Okla", "Ariz"}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16] if os.path.exists(path) else "none"


def load(path):
    return yaml.load(open(path, encoding="utf-8"), Loader=Loader)


# ---------------------------------------------------------------- the series' texts, as units with their States

def units():
    """(kind, id, states, text, file) for every place the series may cite a State source."""
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "lists", "*", "*.yaml"))):
        if f.endswith("list.yaml"):
            continue
        d = load(f)
        ents = d.get("entries") if isinstance(d, dict) else d
        lst = os.path.basename(os.path.dirname(f))
        for e in ents or []:
            if not isinstance(e, dict) or not e.get("id"):
                continue
            g = e.get("gloss") or {}
            txt = " ".join(str(e.get(k) or "") for k in ("c", "n", "r")) + " " + " ".join(
                str(x) for x in (g.get("text") or []) if isinstance(g, dict))
            sts = sorted({str(t)[6:].upper() for t in e.get("tags") or [] if str(t).startswith("state:")})
            out.append(("cal" if lst == "cal" else "list", e["id"], sts, txt, f))
    p = os.path.join(ROOT, "congress", "specials-state.yaml")
    for k, v in sorted((load(p) or {}).items()):
        m = re.search(r"-[hs]-([A-Z]{2})-", k)
        st = [m.group(1)] if m else []
        read = " ".join(str(v.get(x) or "") for x in ("cite", "source", "where", "url", "checked", "remarks", "note"))
        if read.strip():
            out.append(("special", k, st, read, p))
        for pd in v.get("pending") or []:
            out.append(("special-pending", k, st, "Check: " + str(pd.get("cite") or "") + " " + str(pd.get("url") or ""), p))
    for f in sorted(glob.glob(os.path.join(ROOT, "elections", "readings", "*.yaml"))):
        out += line_units("reading", f)
    for name in ("facts", "renominations", "primaries", "conventions", "cq"):
        f = os.path.join(ROOT, "elections", name + ".yaml")
        if os.path.exists(f):
            out += line_units(name, f)
    p = os.path.join(ROOT, "elections", "governors.yaml")
    for r in (load(p) or {}).get("races") or []:
        if not isinstance(r, dict):
            continue
        rid = f"{r.get('date')} {r.get('st')}"
        src = r.get("source") or {}
        txt = " ".join(str(src.get(x) or "") for x in ("title", "url", "publisher"))
        if r.get("check"):
            txt += " Check: " + str(r["check"]) + "."
        out.append(("governor", rid, [r.get("st")] if r.get("st") else [], txt, p))
    for name in ("leads.md", "procurement.md"):
        f = os.path.join(ROOT, "notes", name)
        if os.path.exists(f):
            for i, l in enumerate(open(f, encoding="utf-8"), 1):
                sts = [st for st, nm in NAMES.items() if re.search(r"\b" + re.escape(nm) + r"\b", l)]
                out.append(("note", f"{name}:{i}", sts, l, f))
    return out


KEYLINE = re.compile(r"^\s{0,6}['\"]?(?:(?:[hs]) )?([A-Z]{2})(?:\b[^:\n]*)?['\"]?:\s*(?:$|\S)")


def line_units(kind, f):
    """Blocks of a YAML file under each key naming a State ('h NY 9', 'AR:'), as text units."""
    out, cur, buf, key = [], None, [], None
    year = re.sub(r"\D", "", os.path.basename(f)) or os.path.basename(f)
    for i, l in enumerate(open(f, encoding="utf-8"), 1):
        m = KEYLINE.match(l)
        if m and m.group(1) in NAMES:
            if buf:
                out.append((kind, key, [cur], " ".join(buf), f))
            cur, buf, key = m.group(1), [], f"{year} {l.strip().rstrip(':').strip(chr(39) + chr(34))}"[:60]
        if cur:
            buf.append(l.strip())
    if buf:
        out.append((kind, key, [cur], " ".join(buf), f))
    return out


def check_spans(text):
    """The Check sentences of a text, as (start, end)."""
    spans = []
    for m in re.finditer(r"(?<!To )\b[Cc]heck(?:s)?(?::| against| it)", text):     # not "To check:" (works unread)
        j = m.end()
        while True:
            k = text.find(".", j)
            if k < 0:
                k = len(text)
                break
            w = re.search(r"(\w+)$", text[max(0, k - 12):k])
            word = w.group(1) if w else ""
            nxt = text[k + 1:k + 3]
            if (len(word) >= 4 and word not in ABBR and not word.isdigit()) or text[k - 1:k] in (")", "*", "]") or nxt[:1] in ("", "'"):
                if not re.match(r"\d", nxt.strip()[:1] or "x"):
                    break
            j = k + 1
        spans.append((m.start(), k))
    return spans


def in_span(pos, spans):
    return any(a <= pos <= b for a, b in spans)


def url_key(u):
    """A copy's address as matched: no scheme, www., fragment, page or view parameters; None if too general."""
    u = re.sub(r"#.*$", "", str(u or ""))
    u = re.sub(r"[?&](seq|view|page|q1|ui)=[^&]*", "", u).rstrip("/?&")
    u = re.sub(r"^https?://(www\.)?", "", u)
    if "/" not in u or len(u.split("/", 1)[1]) < 6 or re.search(r"/(search|advancedsearch)", u):
        return None
    return u


# ---------------------------------------------------------------- the register

def items(reg):
    """Every register item: (st, n, item, label). n counts within the State."""
    out = []
    for e in reg:
        st = e["st"]
        for i, s in enumerate(e.get("sources") or []):
            out.append((st, f"{st}-{i + 1}", s, "source"))
        for j, l in enumerate(e.get("local") or []):
            out.append((st, f"{st}-L{j + 1}", l, "local"))
    return out


def best_ground(it):
    gs = [b.get("ground") for b in it.get("basis") or []]
    for g in GROUNDS:
        if g in gs:
            return g
    return "none"


def access_line(it):
    on = it.get("online") or []
    acc = sorted({o.get("access") for o in on})
    if "open" in acc:
        return "open"
    if not on:
        return "paper only (no copy online found)"
    return "closed (" + ", ".join(a for a in acc if a) + ")"


def matchers(st, it):
    pats = []
    for c in it.get("cited_as") or []:
        try:
            pats.append((re.compile(c, re.I), " " in c))
        except re.error:
            pass
    for o in it.get("online") or []:
        k = url_key(o.get("url"))
        if k:
            pats.append((re.compile(re.escape(k), re.I), False))
    return pats


def scan(reg):
    """uses[(st, n)] = [(kind, id, 'use'|'check', snippet)]; pointers = [(kind, id, sts, text, [(st, n)])]."""
    its = items(reg)
    M = {(st, n): matchers(st, it) for st, n, it, _ in its}
    by_st = {}
    for st, n, it, _ in its:
        by_st.setdefault(st, []).append(n)
    uses, pointers = {}, []
    for kind, uid, sts, text, f in units():
        spans = check_spans(text)
        hits = []
        for (st, n), pats in M.items():
            for rx, needs_state in pats:
                if needs_state and st not in sts:
                    continue
                for m in rx.finditer(text):
                    how = "check" if kind == "special-pending" or in_span(m.start(), spans) else "use"
                    hits.append((st, n, how, m.start()))
        seen = set()
        for st, n, how, pos in sorted(hits):
            if (st, n, how) in seen:
                continue
            seen.add((st, n, how))
            uses.setdefault((st, n), []).append((kind, uid, how))
        if kind in ("note", "list", "facts", "cq", "primaries", "renominations", "conventions"):
            continue
        for a, b in spans:
            s = text[a:b + 1]
            if not ELECTION_TERM.search(s) or not sts:
                continue
            if kind == "cal" and LAW_TERM.search(s) and not re.search(r"canvass|returns|abstract|tabulation", s, re.I):
                continue
            named = sorted({(st, n) for st, n, how, pos in hits if a <= pos <= b})
            if not named and re.search(r"the State's canvass", s):
                named = generic_canvass(reg, sts)
            pointers.append((kind, uid, sts, s.strip(), named))
    return its, uses, pointers


def generic_canvass(reg, sts):
    """For "the State's canvass" (the governors' races): the State's publications that print the governor's race."""
    out = []
    for e in reg:
        if e["st"] not in sts:
            continue
        for i, s in enumerate(e.get("sources") or []):
            sr = str((s.get("contents") or {}).get("state_races") or "")
            if re.search(r"governor|state offic|statewide", sr, re.I) and not re.match(r"(?i)unverified|no\b|none", sr.strip()):
                out.append((e["st"], f"{e['st']}-{i + 1}"))
    return out


def ruling(named, idx):
    if not named:
        return "unmatched", "names nothing the register holds"
    gs = []
    for key in named:
        it = idx[key]
        gs.append((GROUNDS.index(best_ground(it)) if best_ground(it) in GROUNDS else 9, key, best_ground(it), access_line(it)))
    gs.sort()
    _, key, g, acc = gs[0]
    if g == "assumed":
        return "assumed", f"{key[1]}: no ground yet; {acc}"
    return "found", f"{key[1]}: {g}; {acc}"


# ---------------------------------------------------------------- writing

def md_escape(s):
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


def short(s, n=240):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def write_sources(reg, h):
    its, uses, pointers = scan(reg)
    idx = {(st, n): it for st, n, it, _ in its}
    L = [f"<!-- register: {h} -->",
         "# State election sources: the listing",
         "",
         "Generated by `tools/sources/make_listing.py` from `sources/states.yaml` (the register, kept by hand; its header the",
         "schema). Do not edit: edit the register and rerun. Each State: its publications, archival series and county or city",
         "records; for each, the editions, what it prints, its copies and their access as last tested from this environment",
         "(open; closed: borrow, bot-check, blocked, dead, other; paper only where no copy is online), the basis of our belief",
         "that it exists, and what the series has used it for. Then the Check pointers to the State's records, each ruled.",
         "",
         "Basis: *seen*, a copy read; *catalog*, a catalog, holdings or finding-aid record seen, not the text; *law*, a statute",
         "or rule obliging an officer to make, keep or publish it (as read, or as the publication itself cites it); *cited*, a",
         "source naming it; *assumed*, no ground yet. A pointer is *found* where it names a register item with a ground other",
         "than assumed, *assumed* where the item it names has none, *unmatched* where it names nothing the register holds.",
         ""]
    cnt = {g: 0 for g in GROUNDS}
    for st, n, it, _ in its:
        g = best_ground(it)
        cnt[g] = cnt.get(g, 0) + 1
    allg = {g: 0 for g in GROUNDS}
    for st, n, it, _ in its:
        for g in {b.get("ground") for b in it.get("basis") or []}:
            allg[g] = allg.get(g, 0) + 1
    acc = {}
    for st, n, it, _ in its:
        a = access_line(it).split(" (")[0]
        acc[a] = acc.get(a, 0) + 1
    rul = {}
    for p in pointers:
        r = ruling(p[4], idx)[0]
        rul[r] = rul.get(r, 0) + 1
    L += ["## Summary", "",
          f"{len(its)} items: {sum(1 for x in its if x[3] == 'source')} publications, databases and archival series, "
          f"{sum(1 for x in its if x[3] == 'local')} county and city records.", "",
          "| basis | items (strongest ground) | items with the ground |", "|---|---|---|"]
    for g in GROUNDS:
        L.append(f"| {g} | {cnt.get(g, 0)} | {allg.get(g, 0)} |")
    L += ["", "| access | items |", "|---|---|"]
    for a in sorted(acc):
        L.append(f"| {a} | {acc[a]} |")
    L += ["", f"Check pointers to State records: {len(pointers)} "
          f"({', '.join(f'{k} {v}' for k, v in sorted(rul.items()))}).", ""]
    for e in reg:
        st = e["st"]
        L += [f"## {e.get('name') or NAMES.get(st, st)} ({st})", ""]
        for st2, n, it, what in its:
            if st2 != st:
                continue
            title = it.get("title") or it.get("body")
            L.append(f"### {n}. {md_escape(title)}")
            L.append("")
            if what == "local":
                L.append(f"- Record: {md_escape(it.get('record'))}")
            meta = [x for x in (it.get("kind"), it.get("publisher"), it.get("frequency")) if x]
            if meta:
                L.append("- " + md_escape("; ".join(str(x) for x in meta)))
            if it.get("covers"):
                L.append(f"- Editions: {md_escape(it['covers'])}")
            c = it.get("contents") or {}
            for k, lab in (("general", "General"), ("specials", "Specials"), ("state_races", "State races"),
                           ("primaries", "Primaries"), ("checked_in", "Read in")):
                if c.get(k) not in (None, "", False):
                    L.append(f"- {lab}: {md_escape(short(c[k], 400))}")
            L.append(f"- Access: {access_line(it)}")
            for o in it.get("online") or []:
                note = f" ({md_escape(short(o.get('note'), 160))})" if o.get("note") else ""
                L.append(f"  - {o.get('access')}, checked {o.get('checked')}: {md_escape(o.get('host'))}, "
                         f"{md_escape(short(o.get('years'), 160))}: <{o.get('url')}>{note}")
            L.append("- Basis:")
            for b in it.get("basis") or []:
                u = f" <{b['url']}>" if b.get("url") else ""
                L.append(f"  - *{b.get('ground')}*: {md_escape(b.get('ref'))}{u}")
            if not it.get("basis"):
                L.append("  - none recorded")
            us = uses.get((st, n), [])
            used = sorted({(k, i) for k, i, how in us if how == "use"})
            chk = sorted({(k, i) for k, i, how in us if how == "check"})
            L.append("- Used for: " + (fmt_ids(used) if used else "nothing yet"))
            if chk:
                L.append("- Pointed to by a Check: " + fmt_ids(chk))
            L.append("")
        ps = [p for p in pointers if st in p[2]]
        if ps:
            L += [f"### Check pointers in {NAMES.get(st, st)}", "", "| where | the Check | ruling |", "|---|---|---|"]
            for kind, uid, sts, s, named in sorted(ps, key=lambda p: (p[0], p[1])):
                r, why = ruling([x for x in named if x[0] == st] or named, idx)
                L.append(f"| {kind} `{uid}` | {md_escape(short(s, 200))} | {r}: {md_escape(why)} |")
            L.append("")
        for k in ("best_for_specials", "gaps"):
            if e.get(k):
                L.append(f"- {k.replace('_', ' ').capitalize()}: {md_escape(e[k])}")
        L.append("")
    return "\n".join(L).rstrip() + "\n"


KIND_LABEL = {"cal": "Cal.", "list": "lists", "special": "specials read", "special-pending": "specials pending",
              "reading": "readings", "governor": "governors", "note": "notes", "facts": "facts", "cq": "cq",
              "primaries": "primaries", "renominations": "renominations", "conventions": "conventions"}


def fmt_ids(pairs):
    by = {}
    for k, i in pairs:
        by.setdefault(k, []).append(i)
    return "; ".join(f"{KIND_LABEL.get(k, k)}: " + ", ".join(f"`{i}`" for i in sorted(v)) for k, v in sorted(by.items()))


def write_law(law, h):
    from importlib import util
    spec = util.spec_from_file_location("law_listing", os.path.join(os.path.dirname(__file__), "law_listing.py"))
    mod = util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.render(law, h, units, check_spans, NAMES)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    jobs = [(REG, OUT, lambda d, h: write_sources(d, h))]
    if os.path.exists(LAW):
        jobs.append((LAW, LAW_OUT, write_law))
    stale = []
    for src, out, fn in jobs:
        h = sha(src)
        if a.check:
            if not os.path.exists(out) or f"<!-- register: {h} -->" not in open(out, encoding="utf-8").readline():
                stale.append(out)
            continue
        text = fn(load(src), h)
        open(out, "w", encoding="utf-8").write(text)
        print(f"wrote {os.path.relpath(out, ROOT)} ({text.count(chr(10))} lines)")
    if stale:
        print("stale: " + ", ".join(os.path.relpath(s, ROOT) for s in stale))
        sys.exit(1)


if __name__ == "__main__":
    main()
