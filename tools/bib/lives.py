"""Lives: a name entry for each person, gathered from the series' own files. build/lives.html.

Each entry: a heading (the name as Part III writes it; the Directory's description), then
  Life           a chronology, one line a fact, each with its pincites, linked:
                   the Biographical Directory (BD, the 2005 printed edition, by page), one fact a clause;
                   offices held (the Executive roster, by term); seats at each Congress's opening (the rosters);
                   elections (the Clerk's Statistics, by page, and the election's block); departures from a seat
                   (changes.yaml); and the calendar entries that name the person
  Writings       the person's own works in the series and in the Directory's bibliography
  Sent           FRUS documents the person sent (the daybook's rules for authors)
  Primary        oral histories and papers in the series (none is searched for elsewhere)
  About          works on the person: the series' entries, the Directory's bibliography, works that cite the name
  Named          FRUS documents that name the person, by volume; Public Papers (APP) documents, by year
  In the series  the Part III and Part II entries and the calendar, as the rosters point to them

STYLE:
 1. Telegraphic: the Directory's clauses as printed, the first letter raised; dates first, in the calendar's form.
 2. Every fact cites its source in a short form (ABBR below), linked to the page or row.
 3. A fact the Directory and our structured files both give shows once, with both cites.
"""
import datetime
import json
import os
import re

from . import store
from .markup import to_html, plain

SITE = ""   # a base url for the links to the other pages ('' on the site itself)
MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
FULL = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                     "September", "October", "November", "December"], 1)}
BD_URL = "https://www.govinfo.gov/content/pkg/GPO-CDOC-108hdoc222/pdf/GPO-CDOC-108hdoc222-4-{part}.pdf#page={pdf}"
BD_CITE = ("*Biographical Directory of the United States Congress, 1774–2005*, H. Doc. 108-222 (Government "
           "Printing Office, 2005)")
HSG = "https://history.state.gov/historicaldocuments/"


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def a(url, text):
    return f'<a href="{esc(url)}">{text}</a>'


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


# ---------------------------------------------------------------- the Directory

def bd_entry(sur, given):
    p = os.path.join(store.ROOT, "sources", "bd", sur[0].upper() + ".json")
    if not os.path.exists(p):
        return None
    for e in json.load(open(p, encoding="utf-8")):
        m = re.match(r"([A-Z][A-Z'’\- ]+), ([^,(]+)", e["name"])
        if m and same_person(m.group(1).title(), m.group(2), sur, given):
            return e
    return None


DATE_RE = re.compile(r"(January|February|March|April|May|June|July|August|September|October|November|December) "
                     r"(\d{1,2}), (\d{4})")


def iso_dates(t):
    return [f"{y}-{FULL[m]:02d}-{int(d):02d}" for m, d, y in DATE_RE.findall(t)]


def bd_facts(e):
    """[(sort key, label, text, full dates)] from the Directory's clauses."""
    text = e["text"].replace("‘‘", "“").replace("’’", "”")
    clauses = [c.strip() for c in re.split(r";\s+", text)]
    out, last = [], "0000"
    for c in clauses[1:]:                      # the first is the name and description
        ds = iso_dates(c)
        yrs = re.findall(r"\b(1[789]\d\d|20\d\d)\b", c)
        rng = re.search(r"\b(1[789]\d\d|20\d\d)-(1[789]\d\d|20\d\d)\b", c)
        if ds:
            k, label = ds[0], fmt(ds[0])
        elif rng:
            k, label = rng.group(1), f"{rng.group(1)}–{rng.group(2)}"
        elif yrs:
            k, label = yrs[0], yrs[0]
        else:
            k, label = last, ""
        last = k
        t = re.sub(r"\b(1[789]\d\d|20\d\d)-(1[789]\d\d|20\d\d)\b", r"\1–\2", c)
        # the date column carries the date: drop it from the clause where it ends the clause
        if ds and t.endswith(DATE_RE.findall(t)[-1][2]) and len(ds) == 1:
            t = DATE_RE.sub("", t).rstrip(" ,")
        elif label and t.endswith(" " + label):
            t = re.sub(r"\s+(in|on|from|of)$", "", t[: -len(label) - 1].rstrip(" ,"))
        t = re.sub(r"^born in ", "born, ", t)
        t = t[0].upper() + t[1:]
        out.append((k, label, t.rstrip(".") + ".", set(ds)))
    return out


def bd_cite(e):
    return a(BD_URL.format(part=e["part"], pdf=e["pdf"]), f"BD {e['page']}")


# ---------------------------------------------------------------- our files

def exec_facts(sur, given):
    from . import executive as X
    units = X.load()
    out = []
    for u in units.values():
        for o in u.get("offices") or []:
            for h in o.get("holders") or []:
                hs, hg = split_name(h["name"])
                if not same_person(hs, hg, sur, given):
                    continue
                start = max(str(h["from"]), X.TERMS[0][0])
                i = max(j for j, t in enumerate(X.TERMS) if t[0] <= start.ljust(10, "0").replace("-00", "-01"))
                rid = X.rid_for()(i, u["unit"], o["id"])
                day = X.TERMS[i][0]
                title = X.title_at(o, h["from"])
                if h.get("title"):
                    title = f"{title}, ex officio as {h['title']}" if o.get("appt") == "XO" else h["title"]
                # the dates of taking and leaving office are the line's label
                line = re.sub(r"(?:Took office|Left) .*?\d{4}\.\s*", "", X.holder_line(h, None, None, o)).strip()
                line = re.sub(r", took office .*?\d{4}\.", ".", line)
                lab = X.span(h["from"], h.get("to")) if not h.get("_seen") else f"by {fmt(h['from'])}"
                ds = {str(h[k]) for k in ("from", "to", "nominated", "confirmed", "appointed") if h.get(k)}
                cite = a(f"{SITE}executive.html#{rid}", f"Exec. {day[:4]}")
                src = executive_src(h)
                out.append([lo(h["from"]), lab, f"{esc(title)}{' (acting)' if h.get('acting') else ''}. {line}".strip(), ds,
                            [cite] + ([src] if src else [])])
    return out


def executive_src(h):
    from . import executive_sources as S
    s = S.html(h)
    return s.replace('<span class="exs">Sources: ', "").replace(".</span>", "") if s else ""


def lo(d):
    return str(d)


def congress_facts(sur, given):
    out = []
    from .congress import ordinal
    for f in sorted(os.listdir(os.path.join(store.ROOT, "congress"))):
        m = re.match(r"(\d\d)\.yaml$", f)
        if not m:
            continue
        c = int(m.group(1))
        d = store.load_yaml(os.path.join(store.ROOT, "congress", f)) or {}
        for ch, rows in (("s", d.get("senate") or []), ("h", d.get("house") or [])):
            for r in rows:
                if not r.get("name"):
                    continue
                rs, rg = split_name(r["name"])
                if same_person(rs, rg, sur, given):
                    seat = r.get("cl") if ch == "s" else r.get("d", r.get("district", 0))
                    rid = f"cg{c}-{ch}-{r['st']}-{seat}"
                    what = (f"Senator, {r['st']}, class {seat}" if ch == "s" else
                            f"Representative, {r['st']}-{seat if seat else 'AL'}")
                    day = str(d.get("opened") or f"{1789 + 2 * (c - 1)}-01-03")
                    out.append([day, fmt(day), f"{what}, at the opening of the "
                                f"{ordinal(c)} Congress ({r.get('party', '')}).", set(),
                                [a(f"{SITE}congress.html#{rid}", f"{ordinal(c)} Cong.")]])
    ch = store.load_yaml(os.path.join(store.ROOT, "congress", "changes.yaml")) or {}
    for c, rows in (ch.items() if isinstance(ch, dict) else []):
        for r in rows or []:
            w = (r.get("out") or "").split()
            if w and store.fold(w[-1]) == store.fold(sur) and store.fold(w[0]) == store.fold(given.split()[0]):
                ds = iso_dates(r.get("reason") or "")
                k = ds[0] if ds else str(c)
                txt = f"{esc(r.get('reason') or '')} Successor: {esc(r.get('into') or '')} ({esc(r.get('into_party') or '')}), seated {esc(r.get('seated') or '')}."
                seat = r.get("seat")
                out.append([k, fmt(k), txt, set(ds), [a(f"{SITE}congress.html#cg{c}-{r['ch']}-{r['st']}-{seat}",
                                                         f"{ordinal(int(c))} Cong., changes")]])
    return out


def election_facts(sur, given):
    out = []
    from .elections import rid as erid
    first = store.fold(given.split()[0]) if given else ""
    for f in sorted(os.listdir(os.path.join(store.ROOT, "elections"))):
        m = re.match(r"(\d{4})\.yaml$", f)
        if not m or m.group(1) == "1956":
            continue
        y = m.group(1)
        d = store.load_yaml(os.path.join(store.ROOT, "elections", f)) or {}
        src = d.get("source") or {}
        mine = lambda n: n and store.fold(n.split()[-1]) == store.fold(sur) and store.fold(n.split()[0]) == first
        for r in d.get("races") or []:
            cs = r.get("cands") or []
            me = next((c for c in cs if mine(c.get("n"))), None)
            if not me:
                continue
            tot = sum(c.get("v") or 0 for c in cs) + (r.get("scat") or 0)
            share = f"; {100 * me['v'] / tot:.1f} percent" if tot and me.get("v") else ""
            others = ", ".join(f"{esc(c['n'])} ({c['p']}) {c['v']:,}" for c in cs if c is not me and c.get("v"))
            inc = any(mine(i.get("n")) for i in r.get("inc") or [])
            what = ("Reelected" if inc else "Elected") if me.get("w") else ("Defeated for reelection" if inc else "Defeated")
            what += " to the Senate" if r["ch"] == "s" else " to the House"
            share = share.replace("; ", " (") + ")" if share else ""
            txt = f"{what}, {r['st']}{'' if r['ch'] == 's' else '-' + str(r['seat'] or 'AL')}: {me['v']:,} votes{share}; {others}."
            pg = r.get("page")
            clerk = a(src.get("url", "") + (f"#page={pg}" if pg else ""), f"Clerk {y}" + (f", p. {pg}" if pg else ""))
            out.append([d["date"], fmt(d["date"]), txt, set(), [clerk, a(f"{SITE}congress.html#{erid(y, r)}", f"Election {y}")]])
        p = d.get("president")
        if p:
            k = next((c["k"] for c in p.get("cands") or [] if mine(c.get("n"))), None)
            if k:
                pv = sum(s_["v"] for st in p["states"] for s_ in st.get("slates") or [] if s_.get("k") == k)
                ev = sum((st.get("cast") or {}).get(k, 0) for st in p["states"])
                allv = sum(s_["v"] for st in p["states"] for s_ in st.get("slates") or [])
                txt = f"Candidate for President: {pv:,} popular votes ({100 * pv / allv:.1f} percent), {ev} electoral votes."
                out.append([d["date"], fmt(d["date"]), txt, set(),
                            [a(src.get("url", ""), f"Clerk {y}"), a(f"{SITE}congress.html#e{y}", f"Election {y}")]])
    return out


def calendar_facts(ptr, name):
    out, seen = [], set()
    for k in ptr.keys(name)[0]:
        for e in ptr.cal.get(k, []):
            if e["id"] in seen:
                continue
            seen.add(e["id"])
            c = to_html(store.as_list(e.get("c"))[0] if e.get("c") else "")
            out.append([e["date"], f"{e['when']}, {e['date'][:4]}", c, set(),
                        [a(f"{SITE}cal.html#{e['id']}", f"Cal. {esc(e['when'])}, {e['date'][:4]}")]])
    return out


# ---------------------------------------------------------------- the lists

PRIMARY = re.compile(r"Recording|Archive|Document|Record|Paper|Oral|Speech|Tape|Interview|Film|Screen")


def series_works(series, linker, ptr, name):
    """[(kind, citation html, pointer html)] for every citation in the series that is by or names the person:
    kind 'own' (the person's work), 'primary' (the person's speech, recording, or papers: an entry in a section
    of documents, recordings, or archives), or 'about'."""
    sur, given = split_name(name)
    out, seen = [], set()
    hits = []
    for k in ptr.keys(name)[0]:
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
        ptr_html = a(f"{SITE}{l.key}.html#{e['id']}", f"{esc(l.abbr)} {esc(s.code or s.id)}")
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


def bd_bib(e, sur, lines):
    """The Directory's bibliography, own works and works about; an item already among the series' lines (by its
    title) adds its cite to that line."""
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
        line = f'{esc(item.rstrip("."))}. <span class="lvc">{bd_cite(e)}</span>'
        (own if re.match(re.escape(sur) + r",", item, re.I) else about).append(line)
    return own, about


def frus_lists(name):
    p = os.path.join(store.ROOT, "sources", "frus-names", key_of(name) + ".json")
    if not os.path.exists(p):
        return [], []
    d = json.load(open(p, encoding="utf-8"))
    from .executive_sources import frus_label
    sent, named = [], []
    for vol, v in d.items():
        lab = frus_label(vol)
        rows = {r["n"]: r for r in v["named"]}
        for n in v["sent"]:
            r = rows.get(n, {"title": "", "date": ""})
            sent.append((r["date"], f'{fmt(r["date"]) + ". " if r["date"] else ""}{esc(r["title"])}. '
                                    f'<span class="lvc">{a(f"{HSG}{vol}/d{n}", f"{esc(lab)}, {n}")}</span>'))
        docs = ", ".join(a(f"{HSG}{vol}/d{r['n']}", esc(r["n"])) for r in v["named"])
        named.append((vol, f'<i>{esc(lab)}</i>{": " + esc(v["title"]) if v.get("title") else ""}: {len(v["named"])} '
                           f'{"document" if len(v["named"]) == 1 else "documents"}, {docs}.'))
    sent.sort()
    return [x for _, x in sent], [x for _, x in sorted(named, key=lambda t: vol_order(t[0]))]


def vol_order(vol):
    m = re.match(r"frus(\d{4})-\d+v(e?)(\d+)", vol)
    return (m.group(1), m.group(2), int(m.group(3))) if m else (vol, "", 0)


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
        by_year.setdefault(d[:4], []).append(f'{fmt(d)[:-6]}: {a(r["url"], esc(r["title"]))}' + (
            f' ({esc(r["who"])})' if r["who"] and "Johnson" not in r["who"] else ""))
    return [f'<b>{y}</b> ({len(v)}). ' + "; ".join(v) + "." for y, v in by_year.items()]


# ---------------------------------------------------------------- the entry

def merge(facts, bd, e):
    """The Directory's clauses into the structured facts: a clause whose full dates all fall in one fact's dates
    becomes that fact's second cite; the rest stand as their own lines."""
    out = list(facts)
    for k, label, t, ds in bd:
        words = set(re.findall(r"[a-z]{4,}", t.lower()))
        hosts = [f for f in out if ds and f[3] and ds <= f[3]]
        def score(f):
            w = set(re.findall(r"[a-z]{4,}", plain(f[2]).lower()))
            return (len(words & w), -len(w - words))
        host = max(hosts, key=score) if hosts else None
        if host:
            host[4].append(bd_cite(e))
        else:
            out.append([k, label, esc(t), ds, [bd_cite(e)]])
    return sorted(out, key=lambda f: (str(f[0])[:10].ljust(10, "0")))


def entry(series, linker, ptr, name):
    sur, given = split_name(name)
    e = bd_entry(sur, given)
    facts = exec_facts(sur, given) + congress_facts(sur, given) + election_facts(sur, given) + calendar_facts(ptr, name)
    for f in facts:
        f[3] = set(f[3])
    life = merge(facts, bd_facts(e) if e else [], e)
    works = series_works(series, linker, ptr, name)
    sent, named = frus_lists(name)
    ppp = app_list(name, sur)
    desc = ""
    if e:
        head = re.split(r";\s+", e["text"])[0]
        desc = head.split("), ", 1)[-1] if "), " in head else head.split(", ", 2)[-1]
        desc = f'<p class="lvd">{esc(desc[0].upper() + desc[1:])}. {bd_cite(e)}.</p>'
    out = [f'<section class="lv" id="{key_of(name)}"><h2 data-short="{esc(sur)}">{esc(name)}</h2>', desc]
    pts = ptr.lines(name, lambda k, i: f"{SITE}{k}.html#{i}")
    if pts:
        out.append('<p class="lvs">In the series: ' + "; ".join(p.replace("Cal. ", "Cal. ") for p in pts) + ".</p>")
    out.append('<h3>Life</h3><ol class="lvl">')
    for k, label, t, ds, cites in life:
        out.append(f'<li><span class="lvt">{esc(label)}</span><span class="lvx">{t} '
                   f'<span class="lvc">{"; ".join(dict.fromkeys(cites))}</span></span></li>')
    out.append("</ol>")

    def section(title, items, empty="None in the series.", cls="lvb"):
        out.append(f"<h3>{title}</h3>")
        out.append(f'<ul class="{cls}">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>" if items
                   else f'<p class="lvn">{empty}</p>')
    kinds = lambda k: [w for w in works if w[0] == k]
    g_own, g_prim, g_about = grouped(kinds("own")), grouped(kinds("primary")), grouped(kinds("about"))
    every = g_own + g_prim + g_about
    bown, babout = bd_bib(e, sur, every)
    g_own, g_prim, g_about = every[:len(g_own)], every[len(g_own):len(g_own) + len(g_prim)], every[len(g_own) + len(g_prim):]
    section("Writings", g_own + bown)
    section("FRUS documents sent", sent, "None found.")
    section("Oral histories given, papers, and other primary sources", g_prim)
    section("About", g_about + babout)
    section("FRUS documents that name him", named, "None found.", "lvb lvf")
    section("Oral histories that name him", [], "None in the series.")
    section("Presidential documents that name him (APP: the Public Papers and the campaign documents)", ppp,
            "None found.", "lvb lvf")
    out.append("</section>")
    return "\n".join(x for x in out if x)


CSS = """<style>
/* Lives (tools/bib/lives.py) */
.lv h2{margin-top:2rem}
.lv h3{font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:1.2rem 0 .3rem}
.lvd{font-size:.95rem}
.lvs{font-size:.82rem;color:var(--muted)}
ol.lvl{list-style:none;margin:0;padding:0}
ol.lvl li{display:grid;grid-template-columns:9.5rem 1fr;gap:.6rem;padding:.25rem 0;border-bottom:1px solid var(--rule);font-size:.9rem;line-height:1.4}
.lvt{color:var(--muted);font-size:.82rem;font-variant-numeric:tabular-nums}
.lvc{font-size:.76rem;color:var(--muted)}
.lvc a{color:inherit}
ul.lvb{margin:.2rem 0 .6rem;padding-left:1.1rem;font-size:.88rem;line-height:1.4}
ul.lvb li{margin:.2rem 0}
ul.lvf{font-size:.8rem}
.lvn{font-size:.85rem;color:var(--muted)}
@media (max-width:640px){ol.lvl li{grid-template-columns:1fr;gap:0}}
</style>"""


def page(series, linker, template, names):
    from .congress import Pointers
    ptr = Pointers(series, linker)
    main = ["<h1>Lives</h1>",
            '<p class="lede">A name entry for each person: a chronology of the life, each fact with its pincite, then '
            "the person's writings and papers, the FRUS documents the person sent, works about the person, and the "
            "FRUS and Public Papers documents that name the person.</p>",
            '<p class="logic">Abbreviations: BD, the ' + to_html(BD_CITE) + ", by page; Exec., the Executive roster at "
            "the term named; Cong., a Congress at its opening (the rosters) or its changes; Election, the election's "
            "block, and Clerk, the Clerk of the House's <i>Statistics</i> of that election, by page; Cal., the calendar; "
            "FRUS, by subseries, volume, and document; APP, the American Presidency Project.</p>"]
    for n in names:
        main.append(entry(series, linker, ptr, n))
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", "Lives").replace("{{main}}", "\n".join(main))
    return pg.replace("</body>", CSS + "\n</body>", 1)
