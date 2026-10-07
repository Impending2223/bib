"""Lives: a name entry for each person, gathered from the series' own files. build/lives.html.

Each entry: the name as Part III writes it, the Directory's description, the pointers into the series, then
  Life                 running text, in order of date: each fact with the date in it and its pincite, linked
                       to the ground source; the series' own pages as pointers beside it (sans serif, not underlined)
                         the Biographical Directory (BD, the 2005 printed edition, by page), one fact a clause;
                         offices held, with their ex officio offices after them (the holder's sources; the
                         Executive Roster as a pointer); seats (BD; the Congress rosters as pointers); elections
                         (the Clerk's Statistics, by page; the election's block as a pointer); the calendar
  Publications         the person's own works in the series and in the Directory's bibliography
  FRUS documents sent  by the daybook's rules for authors
  Primary sources      oral histories, papers, speeches and recordings in the series
  Secondary sources    works on the person: the series' entries, the Directory's bibliography, works citing the name
  Named                FRUS documents that name the person, by volume; the Public Papers (PPP: a President's own
                       papers in his term) and other presidential documents (APP), one a line, by year

STYLE:
 1. Telegraphic: the Directory's clauses as printed, the first letter raised; nicknames and honors of color cut.
 2. Each fact cites its ground source, linked; the series' pages are pointers, not sources. A run of facts from
    the same page of the same source cites it once, at the end of the run.
 3. A fact the Directory and our structured files both give shows once, with both cites.
 4. Abbreviations: BD, CDir., CR, FR, DSB, GOM, PPP; FRUS by subseries, volume and doc.; Clerk, Election
    Statistics, by year and page; pointers: Exec. Roster, Roster (a Congress at its opening), Election, Cal.
 5. FRUS headings with 'from' in lower case; works from the Directory's bibliography in the series' form.
"""
import datetime
import json
import os
import re

from . import store
from .markup import to_html, plain, lower_from

SITE = ""   # a base url for the links to the other pages ('' on the site itself)
MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
FULL = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                     "September", "October", "November", "December"], 1)}
BD_URL = "https://www.govinfo.gov/content/pkg/GPO-CDOC-108hdoc222/pdf/GPO-CDOC-108hdoc222-4-{part}.pdf#page={pdf}"
BD_CITE = ("*Biographical Directory of the United States Congress, 1774–2005*, H. Doc. 108-222 (Government "
           "Printing Office, 2005)")
HSG = "https://history.state.gov/historicaldocuments/"
# The Presidents' terms, for PPP: a President's own papers in his term
PRESIDENTS = [("Dwight D. Eisenhower", "1953-01-20", "1961-01-20"), ("John F. Kennedy", "1961-01-20", "1963-11-22"),
              ("Lyndon B. Johnson", "1963-11-22", "1969-01-20"), ("Richard Nixon", "1969-01-20", "1974-08-09"),
              ("Gerald R. Ford", "1974-08-09", "1977-01-20")]
# Clauses of the Directory left out: color, not record
CUT = re.compile(r"^(known (in|as)|called |nicknamed )", re.I)


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def a(url, text):
    return f'<a href="{esc(url)}">{text}</a>'


def ptr(url, text):
    """A pointer into the series: not a source."""
    return f'<a class="lvp" href="{esc(url)}">{text}</a>'


def fmt(d):
    d = str(d)
    if len(d) == 10:
        return f"{MONTHS[int(d[5:7]) - 1]} {int(d[8:])}, {d[:4]}"
    if len(d) == 7:
        return f"{MONTHS[int(d[5:7]) - 1]} {d[:4]}"
    return d


def key_of(name):
    return re.sub(r"[^a-z]+", "-", store.fold(re.sub(r",\s*(Jr|Sr|II|III)\.?$", "", name)).lower()).strip("-")


def split_name(name):
    bare = re.sub(r"\s*\([^)]*\)", "", name)
    p = [x.strip() for x in bare.split(",")]
    return p[0], (p[1] if len(p) > 1 else "")


def same_person(sur, given, other_sur, other_given):
    from .executive_names import compatible
    f = lambda g: (store.fold(g).replace(".", " ").split() or [""])[0]
    return store.fold(sur) == store.fold(other_sur) and compatible(given, other_given) and \
        (f(given) == f(other_given) or len(f(given)) == 1 or len(f(other_given)) == 1)


# ---------------------------------------------------------------- sentences

def sent(key, text, ext=(), intl=(), para=False, kind="", dates=()):
    return {"key": str(key), "text": text, "ext": list(ext), "int": list(intl), "para": para, "kind": kind,
            "dates": set(dates)}


DATE_RE = re.compile(r"(January|February|March|April|May|June|July|August|September|October|November|December) "
                     r"(\d{1,2}), (\d{4})")


def iso_dates(t):
    return [f"{y}-{FULL[m]:02d}-{int(d):02d}" for m, d, y in DATE_RE.findall(t)]


def bd_entry(sur, given):
    p = os.path.join(store.ROOT, "sources", "bd", sur[0].upper() + ".json")
    if not os.path.exists(p):
        return None
    for e in json.load(open(p, encoding="utf-8")):
        m = re.match(r"([A-Z][A-Z'’\- ]+), ([^,(]+)", e["name"])
        if m and same_person(m.group(1).title(), m.group(2), sur, given):
            return e
    return None


def bd_cite(e):
    return a(BD_URL.format(part=e["part"], pdf=e["pdf"]), f"BD {e['page']}")


def bd_sentences(e):
    text = e["text"].replace("‘‘", "“").replace("’’", "”")
    out, last = [], "0000"
    for c in [c.strip() for c in re.split(r";\s+", text)][1:]:     # the first: the name and description
        if CUT.match(c):
            continue
        ds = iso_dates(c)
        yrs = re.findall(r"\b(1[789]\d\d|20\d\d)\b", c)
        k = ds[0] if ds else (yrs[0] if yrs else last)
        last = k
        t = re.sub(r"\b(1[789]\d\d|20\d\d)-(1[789]\d\d|20\d\d)\b", r"\1–\2", c)
        t = re.sub(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b",
                   lambda m: MONTHS[FULL[m.group(1)] - 1], t)
        t = t[0].upper() + t[1:]
        t = re.sub(r"(\d)-(\d)", r"\1–\2", t)
        out.append(sent(k, esc(t.rstrip(".")) + ".", [bd_cite(e)], kind="bd", dates=ds))
    return out


def roster_href(day):
    from . import executive as X
    return max(j for j, t in enumerate(X.TERMS) if t[0] <= day)


def office_sentences(sur, given):
    """Each office held, with the ex officio offices held by virtue of it after it."""
    from . import executive as X, executive_sources as S
    units = X.load()
    held = []
    for u in units.values():
        for o in u.get("offices") or []:
            for h in o.get("holders") or []:
                hs, hg = split_name(h["name"])
                if same_person(hs, hg, sur, given):
                    held.append((u, o, h))

    def cites(u, o, h):
        s = S.html(h)
        ext = [s.replace('<span class="exs">Sources: ', "").replace(".</span>", "")] if s else []
        start = max(str(h["from"]), X.TERMS[0][0]).ljust(10, "0").replace("-00", "-01")
        i = roster_href(start)
        rid = X.rid_for()(i, u["unit"], o["id"])
        return ext, [ptr(f"{SITE}executive.html#{rid}", f"Exec. Roster {X.TERMS[i][0][:4]}")]

    def when(h, host=None):
        f, t = h["from"], h.get("to")
        if host and str(f) == str(host["from"]) and str(t) == str(host.get("to")):
            return ""
        a_ = (f"in office by {fmt(f)}" if h.get("_seen") else f"from {fmt(f)}") if not host or str(f) != str(host["from"]) else ""
        b_ = (f"last listed {fmt(t)}" if h.get("_last") else f"to {fmt(t)}") if t and (not host or str(t) != str(host.get("to"))) else ""
        return " ".join(x for x in (a_, b_) if x)

    xo = [(u, o, h) for u, o, h in held if o.get("appt") == "XO"]
    hosts = [(u, o, h) for u, o, h in held if o.get("appt") != "XO"]
    out = []
    for u, o, h in sorted(hosts, key=lambda x: str(x[2]["from"])):
        title = h.get("title") or X.title_at(o, h["from"])
        pairs = [(k, h[k]) for k in ("nominated", "confirmed") if h.get(k)]
        if h.get("recess"):
            pairs.insert(0, ("recess appointment", h["recess"]))
        extra = "; " + X.dates_run(pairs) if pairs else ""
        out_ = " " + to_html(h["out"]).rstrip(".") + "." if h.get("out") else ""
        t = f"{'Acting ' if h.get('acting') else ''}{esc(title)} {when(h)}{extra}.{out_}"
        ext, intl = cites(u, o, h)
        ds = {str(h[k]) for k in ("from", "to", "nominated", "confirmed", "appointed") if h.get(k)}
        out.append(sent(h["from"], t, ext, intl, para=not h.get("acting"), kind="office", dates=ds))
        # the ex officio offices held by virtue of this one, with their own dates where they differ
        for xu, xo_, xh in sorted(xo, key=lambda x: str(x[2]["from"])):
            if (xh.get("title") or "") == title or (xh.get("title") and xh["title"] in title):
                w = when(xh, h)
                ext, intl = cites(xu, xo_, xh)
                t = f"{esc(X.title_at(xo_, xh['from']))}, ex officio{', ' + w if w else ''}."
                out.append(sent(h["from"], t, ext, intl, kind="xo"))
                xh["_placed"] = True
    for xu, xo_, xh in xo:
        if not xh.pop("_placed", False):
            ext, intl = cites(xu, xo_, xh)
            out.append(sent(xh["from"], f"{esc(X.title_at(xo_, xh['from']))}, ex officio, {when(xh)}.", ext, intl,
                            kind="office"))
    return out


def roster_pointers(sur, given):
    """[(day, Congress, pointer)] for each Congress at whose opening the person held a seat."""
    from .congress import ordinal
    out = []
    for f in sorted(os.listdir(os.path.join(store.ROOT, "congress"))):
        m = re.match(r"(\d\d)\.yaml$", f)
        if not m:
            continue
        c = int(m.group(1))
        d = store.load_yaml(os.path.join(store.ROOT, "congress", f)) or {}
        for ch, rows in (("s", d.get("senate") or []), ("h", d.get("house") or [])):
            for r in rows:
                rs, rg = split_name(r.get("name") or ",")
                if r.get("name") and same_person(rs, rg, sur, given):
                    seat = r.get("cl") if ch == "s" else r.get("d", 0)
                    out.append((str(d.get("opened")), c, ch, r["st"],
                                ptr(f"{SITE}congress.html#cg{c}-{ch}-{r['st']}-{seat}", f"Roster, {ordinal(c)} Cong.")))
    return out





def election_sentences(sur, given):
    from .elections import rid as erid
    from .congress import STATE
    out = []
    first = store.fold(given.split()[0]) if given else ""
    mine = lambda n: n and store.fold(n.split()[-1]) == store.fold(sur) and store.fold(n.split()[0]) == first
    for f in sorted(os.listdir(os.path.join(store.ROOT, "elections"))):
        m = re.match(r"(\d{4})\.yaml$", f)
        if not m or m.group(1) == "1956":
            continue
        y = m.group(1)
        d = store.load_yaml(os.path.join(store.ROOT, "elections", f)) or {}
        url = (d.get("source") or {}).get("url", "")

        def clerk(pg=None):
            return a(url + (f"#page={pg}" if pg else ""), f"Clerk, Election Statistics {y}" + (f", p. {pg}" if pg else ""))
        for r in d.get("races") or []:
            cs = r.get("cands") or []
            me = next((c for c in cs if mine(c.get("n"))), None)
            if not me:
                continue
            tot = sum(c.get("v") or 0 for c in cs) + (r.get("scat") or 0)
            share = f" ({100 * me['v'] / tot:.1f} percent)" if tot and me.get("v") else ""
            others = ", ".join(f"{esc(c['n'])} ({c['p']}) {c['v']:,}" for c in cs if c is not me and c.get("v"))
            inc = any(mine(i.get("n")) for i in r.get("inc") or [])
            what = ("Reelected" if inc else "Elected") if me.get("w") else ("Defeated for reelection" if inc else "Defeated")
            where = STATE.get(r["st"], r["st"])
            seat = "Senate" if r["ch"] == "s" else f"House, {r['st']}-{r['seat'] or 'AL'}"
            t = f"{what} to the {seat}{', ' + where if r['ch'] == 's' else ''}, {fmt(d['date'])}: {me['v']:,} votes{share}; {others}."
            out.append(sent(d["date"], t, [clerk(r.get("page"))], [ptr(f"{SITE}congress.html#{erid(y, r)}", f"Election {y}")],
                            para=True, kind="election", dates={d["date"]}))
        p = d.get("president")
        k = next((c["k"] for c in (p or {}).get("cands") or [] if mine(c.get("n"))), None)
        if k:
            pv = sum(s_["v"] for st in p["states"] for s_ in st.get("slates") or [] if s_.get("k") == k)
            ev = sum((st.get("cast") or {}).get(k, 0) for st in p["states"])
            allv = sum(s_["v"] for st in p["states"] for s_ in st.get("slates") or [])
            party = next((c.get("party") for c in p["cands"] if c["k"] == k), "")
            t = (f"{esc(party)} candidate for President, {fmt(d['date'])}: {pv:,} popular votes "
                 f"({100 * pv / allv:.1f} percent); {ev} electoral votes.")
            out.append(sent(d["date"], t, [clerk()], [ptr(f"{SITE}congress.html#e{y}", f"Election {y}")],
                            para=True, kind="election", dates={d["date"]}))
    return out


def calendar_sentences(ptrs, name):
    out, seen = [], set()
    for k in ptrs.keys(name)[0]:
        for e in ptrs.cal.get(k, []):
            if e["id"] in seen:
                continue
            seen.add(e["id"])
            c = to_html(store.as_list(e.get("c"))[0] if e.get("c") else "")
            n = to_html(re.sub(r"\s*Names:.*$", "", e.get("n") or "").strip()) if e.get("n") else ""
            out.append(sent(e["date"], f"{esc(e['when'])}, {e['date'][:4]}: {c}", [n] if n else [],
                            [ptr(f"{SITE}cal.html#{e['id']}", f"Cal. {esc(e['when'])}, {e['date'][:4]}")], kind="cal"))
    return out


def merge(structured, bd, rosters):
    """The Directory's clauses into the structured sentences: a clause whose full dates all fall in one sentence's
    dates, or whose year and words match one, becomes that sentence's second cite. The rosters as pointers on the
    clause that gives the service they fall in."""
    out = [s for s in structured]
    hosts = [s for s in structured if s["kind"] in ("office", "election")]
    W = lambda t: set(re.findall(r"[a-z]{4,}", plain(re.sub(r"<[^>]+>", " ", t)).lower())) - {"united", "states", "with", "from", "until"}
    for b in bd:
        words = W(b["text"])
        cand = [s for s in hosts if b["dates"] and s["dates"] and b["dates"] <= s["dates"]]
        if not cand and not b["dates"]:
            cand = [s for s in hosts if s["key"][:4] == b["key"][:4] and len(words & W(s["text"])) >= 2]
        if cand:
            host = max(cand, key=lambda s: (len(words & W(s["text"])), -len(W(s["text"]) - words)))
            host["ext"] = host["ext"] + [x for x in b["ext"] if x not in host["ext"]]
            continue
        out.append(b)
    from .congress import ordinal

    def serves(b, day):
        """A clause of service ('served from Jan. 3, 1971, until his death') that holds the day."""
        if b["kind"] != "bd" or not re.search(r"served from", b["text"]) or not b["dates"]:
            return False
        end = max(b["dates"]) if len(b["dates"]) >= 2 else "9999"
        return min(b["dates"]) <= day <= end
    for day, c, ch, st, p in rosters:
        span = next((b for b in out if serves(b, day)), None)
        if span:
            span["int"].append(p)
        else:
            out.append(sent(day, f"In the {'Senate' if ch == 's' else 'House'} at the opening of the {ordinal(c)} "
                                 f"Congress.", [], [p], kind="seat"))
    return sorted(out, key=lambda s: (s["key"][:10].ljust(10, "0")))


def pointers(ps):
    """'Roster, 87th Cong.' and 'Roster, 88th Cong.' as one pointer, 'Roster, 87th, 88th Cong.', each linked."""
    out, ros = [], []
    for p in dict.fromkeys(ps):
        m = re.match(r'(<a class="lvp" href="[^"]+">)Roster, (\d+\w+) Cong\.</a>', p)
        if m:
            ros.append(m.group(1) + m.group(2) + "</a>")
        else:
            out.append(p)
    if ros:
        out.insert(0, '<span class="lvp">Roster,</span> ' + ", ".join(ros) + ' <span class="lvp">Cong.</span>')
    return "; ".join(out)


def life_html(sents):
    """Running text: paragraphs at each office and election; a run of sentences with the same cites cites once."""
    paras, cur, pend = [], [], None

    def flush():
        nonlocal pend
        if pend:
            cur.append(f'<span class="lvc">{"; ".join(x.rstrip(".") for x in dict.fromkeys(pend))}.</span>')
        pend = None
    for s in sents:
        if pend is not None and (s["ext"] != pend or s["para"] or s["int"] and False):
            flush()
        if s["para"] and cur:
            flush()
            paras.append(" ".join(cur))
            cur = []
        cur.append(s["text"])
        if s["int"]:
            cur.append('<span class="lvq">' + pointers(s["int"]) + "</span>")
        pend = s["ext"] or None
    flush()
    if cur:
        paras.append(" ".join(cur))
    return "".join(f'<p class="lvl">{p}</p>' for p in paras)


# ---------------------------------------------------------------- the lists

def bd_work(item):
    """The Directory's 'Thurber, Timothy N. The Politics of Equality. New York: Columbia University Press, 1999.'
    in the series' form: 'Timothy N. Thurber, *The Politics of Equality* (1999)'."""
    m = re.match(r"^([A-Z][\w'’\- ]+), (.*)$", item)
    if not m:
        return f"*{item.rstrip('.')}*"
    sur, toks = m.group(1), m.group(2).split(" ")
    # the given names run to a word that ends with a period, or to an initial not followed by another initial
    k = 0
    while k < len(toks):
        t_ = toks[k]
        if re.fullmatch(r"[A-Z]\.", t_):
            if k + 1 < len(toks) and re.fullmatch(r"[A-Z]\.", toks[k + 1]):
                k += 1
                continue
            break
        if t_.endswith("."):
            break
        k += 1
    given, rest = " ".join(toks[:k + 1]).rstrip("."), " ".join(toks[k + 1:])
    given = re.sub(r"\b([A-Z])$", r"\1.", given)
    # the title runs to the imprint ('. New York: Columbia University Press, 1999') or the bare year ('. 1976.')
    imp = re.search(r"\.\s+(?:[A-Z][A-Za-z ,'’]*(?:[A-Z]\.){0,3}: [^.:]*?, |)(1[89]\d\d|20\d\d)\b", rest)
    title = rest[:imp.start()] if imp else rest.rstrip(".")
    return f"{given} {sur}, *{title}*" + (f" ({imp.group(1)})" if imp else "")


def bd_bib(e, sur, lines):
    if not e or not e.get("bib"):
        return [], []
    own, about = [], []
    for item in re.split(r";\s+", e["bib"]):
        parts = item.split(". ")
        title = store.fold(parts[1] if len(parts) > 1 and "," in parts[0] else parts[0])
        title = re.split(r"[:.]", title)[0].strip()
        hit = next((i for i, l in enumerate(lines) if title and title in store.fold(plain(re.sub(r"<[^>]+>", "", l)))), None)
        if hit is not None:
            lines[hit] = lines[hit][:-len("</span>")] + f"; {bd_cite(e)}</span>"
            continue
        line = f'{to_html(bd_work(item))}. <span class="lvc">{bd_cite(e)}</span>'
        (own if re.match(re.escape(sur) + r",", item, re.I) else about).append(line)
    return own, about


def frus_lists(name):
    p = os.path.join(store.ROOT, "sources", "frus-names", key_of(name) + ".json")
    if not os.path.exists(p):
        return [], []
    d = json.load(open(p, encoding="utf-8"))
    from .executive_sources import frus_label
    sent_, named = [], []
    for vol, v in d.items():
        lab = frus_label(vol)
        rows = {r["n"]: r for r in v["named"]}
        for n in v["sent"]:
            r = rows.get(n, {"title": "", "date": ""})
            sent_.append((r["date"], f'{fmt(r["date"]) + ". " if r["date"] else ""}{esc(lower_from(r["title"]))}. '
                                     f'<span class="lvc">{a(f"{HSG}{vol}/d{n}", f"{esc(lab)}, doc. {n}")}</span>'))
        docs = ", ".join(a(f"{HSG}{vol}/d{r['n']}", esc(r["n"])) for r in v["named"])
        k = len(v["named"])
        named.append((vol, f'<i>{esc(lab)}</i>{": " + esc(v["title"]) if v.get("title") else ""}: '
                           f'{"doc." if k == 1 else "docs."} {docs}.'))
    sent_.sort()
    return [x for _, x in sent_], [x for _, x in sorted(named, key=lambda t: vol_order(t[0]))]


def vol_order(vol):
    m = re.match(r"frus(\d{4})-\d+v(e?)(\d+)", vol)
    return (m.group(1), m.group(2), int(m.group(3))) if m else (vol, "", 0)


def ppp_or_app(who, day):
    """PPP for a President's own papers in his term; APP for the rest (a candidate's, a Vice President's)."""
    return "PPP" if any(n == who and f <= day < t for n, f, t in PRESIDENTS) else "APP"


def app_list(name, sur):
    p = os.path.join(store.ROOT, "sources", "app-names", key_of(name) + ".json")
    if not os.path.exists(p):
        return []
    rows = json.load(open(p, encoding="utf-8"))
    keep = []
    for r in rows:
        # a hit only on the given name must name this person, not a namesake ('Hubert R. Harmon')
        if all(q.strip('"').count(" ") == 0 for q in r["q"]):
            if all(re.search(r"\b" + r["q"][0].strip('"') + r"\s+(?!" + sur + r"|H\.|Horatio)[A-Z]", s_) for s_ in r["snip"]):
                continue
        d = datetime.datetime.strptime(r["date"], "%b %d, %Y").date().isoformat()
        keep.append((d, r))
    keep.sort(key=lambda t: t[0])
    by_year = {}
    for d, r in keep:
        lab = ppp_or_app(r["who"], d)
        by_year.setdefault(d[:4], []).append(
            f'{fmt(d)[:-6]}. {esc(r["title"].rstrip("."))}' + (f' ({esc(r["who"])})' if lab == "APP" else "")
            + f'. <span class="lvc">{a(r["url"], lab)}</span>')
    return [f'<b>{y}</b><br>' + "<br>".join(v) for y, v in by_year.items()]


# ---------------------------------------------------------------- the entry

def entry(series, linker, ptrs, name):
    sur, given = split_name(name)
    e = bd_entry(sur, given)
    structured = office_sentences(sur, given) + election_sentences(sur, given) + calendar_sentences(ptrs, name)
    life = merge(structured, bd_sentences(e) if e else [], roster_pointers(sur, given))
    works = series_works(series, linker, ptrs, name)
    sent_, named = frus_lists(name)
    ppp = app_list(name, sur)
    out = [f'<section class="lv" id="{key_of(name)}"><h2 data-short="{esc(sur)}">{esc(name)}</h2>']
    if e:
        head = re.split(r";\s+", e["text"])[0]
        desc = head.split("), ", 1)[-1] if "), " in head else head.split(", ", 2)[-1]
        out.append(f'<p class="lvd">{esc(desc[0].upper() + desc[1:])}. <span class="lvc">{bd_cite(e)}.</span></p>')
    pts = ptrs.lines(name, lambda k, i: f"{SITE}{k}.html#{i}")
    if pts:
        pts = [re.sub(r'<a href=', '<a class="lvp" href=', p) for p in pts]
        out.append('<p class="lvs">In the series: ' + "; ".join(pts) + ".</p>")
    out.append("<h3>Life</h3>" + life_html(life))

    def section(title, items, empty="None in the series.", cls="lvb"):
        out.append(f"<h3>{title}</h3>")
        out.append(f'<ul class="{cls}">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>" if items
                   else f'<p class="lvn">{empty}</p>')
    kinds = lambda k: [w for w in works if w[0] == k]
    g_own, g_prim, g_about = grouped(kinds("own")), grouped(kinds("primary")), grouped(kinds("about"))
    every = g_own + g_prim + g_about
    bown, babout = bd_bib(e, sur, every)
    n1, n2 = len(g_own), len(g_own) + len(g_prim)
    g_own, g_prim, g_about = every[:n1], every[n1:n2], every[n2:]
    pron = "him"
    section("Publications", g_own + bown)
    section("FRUS documents sent", sent_, "None found.")
    section("Oral histories given, papers, and other primary sources", g_prim)
    section("Secondary sources", g_about + babout)
    section(f"FRUS documents that name {pron}", named, "None found.", "lvb lvf")
    section(f"Oral histories that name {pron}", [], "None in the series.")
    section(f"The Public Papers and other presidential documents that name {pron}", ppp, "None found.", "lvb lvf lvy")
    out.append("</section>")
    return "\n".join(out)


CSS = """<style>
/* Lives (tools/bib/lives.py) */
.lv h2{margin-top:2rem}
.lv h3{font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:1.4rem 0 .4rem}
.lvd{font-size:.95rem}
.lvs{font-size:.82rem;color:var(--muted)}
p.lvl{margin:.5rem 0;line-height:1.55}
.lvc{font-size:.85em;color:var(--muted)}
.lvc a{color:inherit}
/* pointers into the series: sans serif, not underlined, as the headings */
a.lvp,span.lvp{font-family:var(--sans);font-size:.74em;font-weight:600;letter-spacing:.01em;color:var(--muted);text-decoration:none}
a.lvp:hover{color:var(--ink);text-decoration:underline}
.lvq{white-space:normal}
.lvq a.lvp{margin-left:.15em}
ul.lvb{margin:.2rem 0 .6rem;padding-left:1.1rem;font-size:.9rem;line-height:1.45}
ul.lvb li{margin:.25rem 0}
ul.lvf{font-size:.84rem}
ul.lvy{list-style:none;padding-left:0}
ul.lvy li{margin:.6rem 0}
.lvn{font-size:.85rem;color:var(--muted)}
</style>"""


def page(series, linker, template, names):
    from .congress import Pointers
    ptrs = Pointers(series, linker)
    main = ["<h1>Lives</h1>",
            '<p class="lede">A name entry for each person: the life, each fact with its source; then the person\'s '
            "publications and papers, the FRUS documents the person sent, the works on the person, and the FRUS and "
            "presidential documents that name the person.</p>",
            '<p class="logic">Sources: BD, the ' + to_html(BD_CITE) + ", by page; CDir., the *Congressional "
            "Directory*; CR, the *Congressional Record*; FR, the *Federal Register*; DSB, the *Department of State "
            "Bulletin*; GOM, the *Government Organization Manual*; Clerk, Election Statistics, the Clerk of the House's "
            "*Statistics of the Presidential and Congressional Election* of that year, by page; FRUS, by subseries, "
            "volume, and document; PPP, the *Public Papers of the Presidents* (a President's own papers in his term, "
            "from the American Presidency Project's copy); APP, the Project's other documents. Pointers into the series "
            '(<a class="lvp" href="#">in this type</a>): Exec. Roster, the Executive Branch at the term named; Roster, '
            "a Congress at its opening; Election, the election's block; Cal., the calendar.</p>"]
    for n in names:
        main.append(entry(series, linker, ptrs, n))
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", "Lives").replace("{{main}}", "\n".join(main))
    return pg.replace("</body>", CSS + "\n</body>", 1)
PRIMARY = re.compile(r"Recording|Archive|Document|Record|Paper|Oral|Speech|Tape|Interview|Film|Screen")


def series_works(series, linker, ptrs, name):
    """[(kind, citation html, pointer html)] for every citation in the series that is by or names the person:
    kind 'own' (the person's work), 'primary' (the person's speech, recording, or papers: an entry in a section
    of documents, recordings, or archives), or 'about'."""
    sur, given = split_name(name)
    out, seen = [], set()
    hits = []
    for k in ptrs.keys(name)[0]:
        for l, s, e in linker.people.get(k, []):
            if e["id"] not in seen and not (s.code or "").startswith("III"):
                seen.add(e["id"])
                hits.append((l, s, e, True))
    q = [store.fold(x) for x in ([f"{given.split()[0]} {sur}", f"{sur}, {given.split()[0]}", f"{given} {sur}"]
                                 if given else [sur])]
    for l in series.lists.values():
        if l.kind == "calendar":
            continue
        for s, e in l.entries():
            if e["id"] in seen or (s.code or "").startswith("III"):
                continue
            txt = store.fold(plain(" ".join(store.as_list(e.get("c"))) + " " + (e.get("n") or "") + " " + (e.get("s") or "")))
            if any(x in txt for x in q):
                seen.add(e["id"])
                hits.append((l, s, e, False))
            elif PRIMARY.search(" ".join(x.title for x in chain(s))) and \
                    re.search(r"\b" + re.escape(store.fold(sur)) + r"(?:s| papers)\b", txt):
                seen.add(e["id"])        # an archive holding the person's papers ('Humphrey's papers')
                hits.append((l, s, e, "papers"))
    for l, s, e, subject in hits:
        sec = " ".join(x.title for x in chain(s))
        ptr_html = ptr(f"{SITE}{l.key}.html#{e['id']}", f"{esc(l.abbr)} {esc(s.code or s.id)}")
        if subject == "papers":
            out.append(("primary", esc(e.get("s") or ""), f" {to_html(e['n'])}" if e.get("n") else "", ptr_html))
            continue
        cs = store.as_list(e.get("c"))
        for i, c in enumerate(cs):
            mine = is_own(c, e, sur, subject and len(cs) == 1)
            if not mine and not any(x in store.fold(plain(c)) for x in q) and not (subject and len(cs) == 1):
                continue           # another work in the same entry
            kind = ("primary" if PRIMARY.search(sec) else "own") if mine else "about"
            note = f" {to_html(e['n'])}" if e.get("n") and len(cs) == 1 else ""
            out.append((kind, to_html(c), note, ptr_html))
    return out


def chain(s):
    while s is not None:
        yield s
        s = s.parent


def is_own(c, e, sur, subject_only):
    c = plain(c)
    author = c.split(", *")[0] if ", *" in c else (c.split(",")[0] if "," in c else "")
    if subject_only and not re.search(r"[A-Z][a-z]+ [A-Z]", author or ""):
        return True                     # a subject entry whose citation names no other author: the person's own
    return bool(author) and store.fold(sur) in store.fold(author)


def grouped(items):
    """Citations of the same work (by its title in italics) on one line, with every pointer."""
    by, order = {}, []
    for kind, c, note, ptr in items:
        m = re.search(r"<i>(.*?)</i>", c)
        k = store.fold(re.sub(r":.*", "", m.group(1))) if m else c
        if k not in by:
            by[k] = [c, note, []]
            order.append(k)
        if len(c) > len(by[k][0]):
            by[k][0] = c
        if note and not by[k][1]:
            by[k][1] = note
        by[k][2].append(ptr)
    return [f'{by[k][0]}.{by[k][1]} <span class="lvc">{"; ".join(dict.fromkeys(by[k][2]))}</span>' for k in order]


