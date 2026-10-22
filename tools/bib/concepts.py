"""Indicators: concepts and sources. The master and its servants (the owner's rule, Oct. 21, 2026).

    indicators/concepts.yaml   the master text, kept by hand: one statement a series of what it measures then and
                               today and where its figures come from, each piece tagged with the periods it concerns
                               ({{SPAN|text}}; the file's header has the syntax).

The master. build/indicators.html ("Indicators"; `page`): the whole statement, by group, then every series' full table,
every period, as first reported and today. Listed in the series index and the README, not in the top bar.

The servants. Each calendar page (Cal. I, II, III; the reader's three blocks alike) writes, right after the month table
where a series first appears on that page, a block of the statements of the series first used there (`Plan`): of each,
only the pieces whose span holds a period the page's tables file for that series. A series not on the page, and a
piece about periods the page does not file, are not written. Each row's name, in that table and every later one on the
page, links to its servant on the page; where a series has no servant there (no text survives), to the master, and
`check` warns [indicator-servant].

STYLE (settled; keep it):
 1. A servant: muted caption "Indicators: concepts and sources", then by group under a small-capital line (the groups of
    ORDER and GROUP in tools/bib/indicators.py: Prices, Employment, Output, Federal finance, International, Oil, The war,
    Money and credit, Opinion), each series' name (linked to its master statement) and its statement. The page's first
    servant opens with the general paragraph. Each closes: "See the master entry for a full statement of indicator
    concepts and sources used in the series."
 2. Anchors: a servant's statement `ind-<page>-<series>` (ind-cal63-cpi), on its page and in the reader; the servant
    `ind-<page>-at-<section>`. The master: `indicators.html#<series>` (the statement), `#t-<series>` (its table).
 3. Spans are by the period a row reports on (its end: a month's last day, a quarter's, June 30 for a fiscal year, Dec.
    31 for a year), not by release: a page is matched by the rows it files, so a piece follows its figures across a
    seam. The master keeps every positive piece and drops every {{not ...}}.
 4. A separator left at an opening or a close by a dropped piece is tidied away (`tidy`); write the text so that each
    page's cut reads as a sentence.
 5. The master's tables: one a series, every row; a column no row of the series fills is left out (the CBO gap has no
    first column; the over-all balance of payments no today); a column some rows fill keeps "—" in the rest.
"""
import bisect
import datetime
import os
import re

from . import store
from .markup import to_html

PATH = os.path.join(store.ROOT, "indicators", "concepts.yaml")
MASTER = "indicators.html"
LINE = "See the {a}master entry</a> for a full statement of indicator concepts and sources used in the series."
_CACHE = {}


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ---------------------------------------------------------------- the file

def load():
    """{'general': text, 'series': {sid: text}} with the vars substituted; {} where the file is missing."""
    if not os.path.exists(PATH):
        return {}
    st = os.stat(PATH)
    sig = (st.st_mtime_ns, st.st_size)
    if _CACHE.get("sig") == sig:
        return _CACHE["data"]
    raw = store.load_yaml(PATH) or {}
    vs = {k: str(v) for k, v in (raw.get("vars") or {}).items()}

    def sub(t):
        for _ in range(3):                 # a var may hold another ({SCB_NOTE} holds {SCB})
            t = re.sub(r"(?<!\{)\{([A-Z][A-Z0-9_]*)\}(?!\})", lambda m: vs.get(m.group(1), m.group(0)), t)
        return t
    data = {"general": sub(str(raw.get("general") or "")),
            "series": {k: sub(str(v)) for k, v in (raw.get("series") or {}).items()}}
    _CACHE.update(sig=sig, data=data)
    return data


# ---------------------------------------------------------------- spans

def _start(tok):
    if tok.startswith("FY"):
        return datetime.date(int(tok[2:]) - 1, 7, 1)
    m = re.match(r"^(\d{4})Q([1-4])$", tok)
    if m:
        return datetime.date(int(m.group(1)), 3 * int(m.group(2)) - 2, 1)
    if re.match(r"^\d{4}$", tok):
        return datetime.date(int(tok), 1, 1)
    if re.match(r"^\d{4}-\d{2}$", tok):
        return datetime.date(int(tok[:4]), int(tok[5:]), 1)
    return datetime.date.fromisoformat(tok)


def _end(tok):
    import calendar
    if re.match(r"^\d{4}-\d{2}-\d{2}$", tok):
        return datetime.date.fromisoformat(tok)
    if tok.startswith("FY"):
        return datetime.date(int(tok[2:]), 6, 30)
    m = re.match(r"^(\d{4})Q([1-4])$", tok)
    if m:
        y, mo = int(m.group(1)), 3 * int(m.group(2))
        return datetime.date(y, mo, calendar.monthrange(y, mo)[1])
    if re.match(r"^\d{4}$", tok):
        return datetime.date(int(tok), 12, 31)
    if re.match(r"^\d{4}-\d{2}$", tok):
        y, mo = int(tok[:4]), int(tok[5:])
        return datetime.date(y, mo, calendar.monthrange(y, mo)[1])
    raise ValueError(f"span token {tok!r}")


def ranges(spec):
    """'1961..1962-06, 1965Q3..' -> [(date, date)]; ValueError on a token it cannot read."""
    out = []
    for part in spec.split(","):
        part = part.strip()
        if ".." in part:
            a, b = part.split("..", 1)
            lo = _start(a.strip()) if a.strip() else datetime.date.min
            hi = _end(b.strip()) if b.strip() else datetime.date.max
        else:
            lo, hi = _start(part), _end(part)
        if lo > hi:
            raise ValueError(f"span {part!r} ends before it begins")
        out.append((lo, hi))
    return out


def parse(text):
    """The text as nodes: a string, or (ranges, negated, [nodes]) for {{SPAN|...}} / {{not SPAN|...}}."""
    def run(i, top):
        nodes, buf = [], []
        while i < len(text):
            if text.startswith("{{", i):
                bar = text.find("|", i)
                if bar < 0:
                    raise ValueError(f"'{{{{' without '|' at {i}")
                spec = text[i + 2:bar].strip()
                neg = spec.startswith("not ")
                rs = ranges(spec[4:] if neg else spec)
                kids, i = run(bar + 1, False)
                if buf:
                    nodes.append("".join(buf))
                    buf = []
                nodes.append((rs, neg, kids))
                continue
            if text.startswith("}}", i):
                if top:
                    raise ValueError(f"'}}}}' without its '{{{{' at {i}")
                if buf:
                    nodes.append("".join(buf))
                return nodes, i + 2
            buf.append(text[i])
            i += 1
        if not top:
            raise ValueError("'{{' not closed")
        if buf:
            nodes.append("".join(buf))
        return nodes, i
    return run(0, True)[0]


def tidy(t):
    """Separators a dropped piece left behind: at an opening, a close, or doubled."""
    t = re.sub(r"\s{2,}", " ", t)
    for _ in range(2):
        t = re.sub(r"\(\s*[;,]\s*", "(", t)
        t = re.sub(r"\s*[;,]\s*\)", ")", t)
        t = re.sub(r":\s*[;,]\s*", ": ", t)
        t = re.sub(r"[;,]\s*([.:])(?=\s|$)", r"\1", t)
        t = re.sub(r"[;,]\s*[;,]", ";", t)
        t = re.sub(r"\s*\(\s*\)", "", t)
        t = re.sub(r"\s+([.,;:)])(?=\s|$|[)\]])", r"\1", t)
        t = re.sub(r":\s*\.(?=\s|$)", ".", t)
    return t.strip()


def render(text, ends=None):
    """The text for a page whose tables file rows of the series ending on `ends` (sorted dates); None: the master."""
    def hit(rs):
        if ends is None:
            return True
        for lo, hi in rs:
            k = bisect.bisect_left(ends, lo)
            if k < len(ends) and ends[k] <= hi:
                return True
        return False

    def walk(nodes):
        out = []
        for n in nodes:
            if isinstance(n, str):
                out.append(n)
                continue
            rs, neg, kids = n
            if ends is None:
                keep = not neg
            else:
                keep = hit(rs) != neg
            if keep:
                out.append(walk(kids))
        return "".join(out)
    return tidy(walk(parse(text)))


def master_texts():
    """{sid: the master's statement}, for DEFS in tools/bib/indicators.py, oil.py, war.py."""
    out = {}
    for sid, t in (load().get("series") or {}).items():
        try:
            out[sid] = render(t)
        except ValueError:
            out[sid] = t
    return out


# ---------------------------------------------------------------- groups

def group_of(sid, s):
    from .indicators import GROUP
    if s and s.get("kind") == "rate":
        return "Money and credit"
    if s and s.get("kind") == "poll":
        return "Opinion"
    return GROUP.get(sid) or "Other"


def groups(data, sids):
    """[(group, [sid])] in ORDER's order."""
    from .indicators import ORDER
    order = [x for x in ORDER if x in sids] + sorted(x for x in sids if x not in ORDER)
    out = {}
    for sid in order:
        out.setdefault(group_of(sid, data.get(sid)), []).append(sid)
    return list(out.items())


# ---------------------------------------------------------------- the plan of a calendar's servants

class Plan:
    """Which rows each dated section of the calendar files, its part (page), where each series first appears in each
    part, and each part's text for it. Built once a page (or check); cheap: the rows are filed as inject files them."""

    def __init__(self, series, data):
        from . import calsplit
        from .indicators import rows_for, period_end
        self.data = data
        self.lst = next((l for l in series.lists.values() if l.kind == "calendar"), None)
        self.parts = {}                  # part -> {"key", "abbr", "first": {sid: sec.id}, "at": {sec.id: [sid]}, "ends", "text"}
        self.sec_part = {}
        if self.lst is None or not data:
            return
        lst = self.lst
        multi = calsplit.cfg(lst)
        info = calsplit.parts(lst)
        dated = [s for s in lst.sections if s.extra.get("from") and s.extra.get("to")]
        master = load().get("series") or {}
        ends = {}
        for i, sec in enumerate(dated):
            part = calsplit.half_of_section(lst, sec) if multi else 1
            self.sec_part[sec.id] = part
            P = self.parts.setdefault(part, {"key": info[part - 1]["page"] if multi else lst.key,
                                             "abbr": info[part - 1].get("abbr") or lst.abbr,
                                             "first": {}, "at": {}, "text": {}, "order": []})
            lo, hi = datetime.date.fromisoformat(str(sec.extra["from"])), datetime.date.fromisoformat(str(sec.extra["to"]))
            prv = datetime.date.fromisoformat(str(dated[i - 1].extra["to"])) if i else None
            nxt = datetime.date.fromisoformat(str(dated[i + 1].extra["from"])) if i + 1 < len(dated) else None
            for sid, s, r in rows_for(data, lo, hi, prv, nxt):
                ends.setdefault(part, {}).setdefault(sid, set()).add(period_end(r["p"]))
                if sid not in P["first"]:
                    P["first"][sid] = sec.id
                    P["at"].setdefault(sec.id, []).append(sid)
                    P["order"].append(sid)
        for part, P in self.parts.items():
            for sid, es in ends.get(part, {}).items():
                t = master.get(sid)
                try:
                    P["text"][sid] = render(t, sorted(es)) if t else ""
                except ValueError:
                    P["text"][sid] = ""
            P["sections"] = [s.id for s in dated if self.sec_part.get(s.id) == part]

    def part_of(self, sec):
        return self.sec_part.get(sec.id)

    def anchor(self, part, sid):
        return f"ind-{self.parts[part]['key']}-{sid}"

    def href(self, sec):
        """sid -> the link for a row's name in this section's table: its servant on the page, else the master."""
        part = self.part_of(sec)
        P = self.parts.get(part)

        def h(sid):
            if P and P["text"].get(sid):
                return f"#{self.anchor(part, sid)}"
            return f"{MASTER}#{sid}"
        return h

    def gaps(self):
        """[(abbr, sid)]: a series a part's tables show with no servant there (its rows link to the master)."""
        return [(P["abbr"], sid) for part, P in sorted(self.parts.items()) for sid in P["order"] if not P["text"].get(sid)]

    def servant(self, sec):
        """The servant block after this section's table: the series first used here, or ''."""
        part = self.part_of(sec)
        P = self.parts.get(part)
        if not P:
            return ""
        sids = [x for x in P["at"].get(sec.id, []) if P["text"].get(x)]
        if not sids:
            return ""
        first = next((s for s in P["sections"] if any(P["text"].get(x) for x in P["at"].get(s, []))), None) == sec.id
        out = [f'<div class="ind-defs ind-srv" id="ind-{P["key"]}-at-{esc(sec.id)}">'
               '<p class="ind-cap">Indicators: concepts and sources</p>']
        if first and load().get("general"):
            out.append(f'<p class="ind-gen">{to_html(load()["general"])}</p>')
        for g, gs in groups(self.data, sids):
            out.append(f'<p class="ind-g">{esc(g)}</p><dl>')
            for sid in gs:
                out.append(f'<dt id="{self.anchor(part, sid)}"><a href="{MASTER}#{esc(sid)}">'
                           f'{esc(self.data[sid]["name"])}</a></dt><dd>{to_html(P["text"][sid])}</dd>')
            out.append("</dl>")
        out.append(f'<p class="ind-master">{LINE.format(a=f"<a href={chr(34)}{MASTER}{chr(34)}>")}</p></div>')
        return "".join(out)


_PLANS = {}


def plan(series, data):
    """The Plan for this run's series (one a run: the three calendar pages and the reader share it)."""
    st = os.stat(PATH) if os.path.exists(PATH) else None
    key = (id(series), st and (st.st_mtime_ns, st.st_size))
    if key not in _PLANS:
        _PLANS.clear()
        _PLANS[key] = Plan(series, data)
    return _PLANS[key]


def link_logic(page):
    """The calendar's paragraph on the indicators names "the Indicators page": link it."""
    return re.sub(r'(<p class="logic">Indicators\.(?:(?!</p>).)*?)the Indicators page',
                  lambda m: m.group(1) + f'<a href="{MASTER}">the Indicators page</a>', page, flags=re.S)


# ---------------------------------------------------------------- the master page

def _table(sid, s, P_links):
    from . import indicators as I
    rows = sorted(s.get("rows", []), key=lambda r: (I.period_end(r["p"]), 0 if "Q" in str(r["p"]) or "-" in str(r["p"]) else 1))
    kind = s.get("kind")
    href = lambda x: f"#{x}"
    trs = []
    if kind == "poll":
        head = "<th>Reading</th><th>As published</th><th>Released</th><th>Today</th>"
        for r in rows:
            pname, per, first, rel, now = I.poll_row(sid, s, r, None)
            trs.append(f'<tr><td class="iname">{esc(pname)} <span class="per">{esc(per)}</span></td><td>{first}</td>'
                       f'<td class="rel">{rel}</td><td>{now}</td></tr>')
    elif kind == "rate":
        head = "<th>Month</th><th>Percent</th>"
        for r in rows:
            trs.append(I.rate_row(sid, s, r, None, href=href, label=I.period_label(r["p"])))
    else:
        has_first = any("first" in r or r.get("est") for r in rows)
        has_now = any(r.get("now") is not None for r in rows)
        head = "<th>Period</th>" + ("<th>As first reported</th><th>Released</th>" if has_first else "") + \
               ("<th>Revised, today</th>" if has_now else "")
        for r in rows:
            first, rel, now = I.cells(sid, s, r, None)
            trs.append(f'<tr><td class="iname"><span class="per">{esc(I.period_label(r["p"]))}</span></td>'
                       + (f"<td>{first}</td><td class=\"rel\">{rel}</td>" if has_first else "")
                       + (f"<td>{now}</td>" if has_now else "") + "</tr>")
    return (f'<div class="ind ind-full"><table><thead><tr>{head}</tr></thead><tbody>' + "".join(trs)
            + "</tbody></table></div>")


def page(series, template):
    """build/indicators.html: the master statement, by group, and every series' full table."""
    from . import indicators as I
    data = I.load()
    m = load()
    if not data or not m:
        return None
    plan_ = plan(series, data)
    sids = [x for x in I.ORDER if x in data] + sorted(x for x in data if x not in I.ORDER)
    gs = groups(data, sids)
    n_rows = sum(len(data[x].get("rows", [])) for x in sids)
    main = ["<h1>Economic indicators, 1960–1969: concepts, sources, and tables</h1>",
            '<p class="lede">The figures the calendar sets under each month, series by series: what each measured then '
            'and measures today, where the figures come from, and every figure, as first reported and as revised. '
            f'{len(sids)} series, {n_rows:,} rows.</p>',
            '<p class="logic">This is the master statement. Each calendar writes, after the month where a series first '
            'appears in it, the part of this statement that concerns its own months, and links each row\'s name to it; '
            'under each statement here, the calendars that carry it, linked to their statements.</p>',
            f'<p class="logic">{to_html(m.get("general", ""))}</p>',
            '<nav class="toc" aria-label="Contents">\n<h3 id="contents" style="border-top:0;margin-top:1.5rem" '
            'data-short="Contents">Contents</h3>\n<ol id="tocList" data-depth="3"></ol>\n</nav>',
            '<h2 id="concepts" data-short="Concepts and sources">Concepts and sources</h2>']
    texts = master_texts()
    for g, xs in gs:
        main.append(f'<h3 id="g-{esc(_slug(g))}" data-short="{esc(g)}">{esc(g)}</h3><div class="ind-defs ind-mst"><dl>')
        for sid in xs:
            where = []
            for part, P in sorted(plan_.parts.items()):
                if P["text"].get(sid):
                    sec = P["first"][sid]
                    where.append(f'<a href="{P["key"]}.html#{plan_.anchor(part, sid)}">{esc(P["abbr"])}, '
                                 f'{esc(_sec_label(plan_.lst, sec))}</a>')
            line = (" In the calendar: " + "; ".join(where) + ".") if where else ""
            main.append(f'<dt id="{esc(sid)}">{esc(data[sid]["name"])} <a class="ind-tl" href="#t-{esc(sid)}">table</a></dt>'
                        f'<dd>{to_html(texts.get(sid, ""))}<span class="ind-in">{line}</span></dd>')
        main.append("</dl></div>")
    main.append('<h2 id="tables" data-short="Tables">Tables</h2>'
                '<p class="logic">Every row of each series, by the period it reports on; the cells as the calendar '
                'shows them (the source figure on hover). A column no row of the series fills is left out.</p>')
    for g, xs in gs:
        main.append(f'<h3 id="tg-{esc(_slug(g))}" data-short="{esc(g)}">{esc(g)}</h3>')
        for sid in xs:
            main.append(f'<h4 id="t-{esc(sid)}" data-short="{esc(data[sid]["name"])}">{esc(data[sid]["name"])} '
                        f'<a class="ind-tl" href="#{esc(sid)}">concepts and sources</a></h4>')
            main.append(_table(sid, data[sid], None))
    pg = open(template, encoding="utf-8").read()
    pg = pg.replace("{{page_title}}", "Indicators").replace("{{main}}", "\n".join(main))
    return pg.replace("</head>", I.STYLE + "\n" + STYLE + "\n</head>", 1)


def _slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def _sec_label(lst, sec_id):
    from .indicators import MON
    for s in lst.sections:
        if s.id == sec_id and s.extra.get("from"):
            d = str(s.extra["from"])
            return f"{MON[int(d[5:7]) - 1]} {d[:4]}"
    return sec_id


STYLE = """<style>
div.ind-defs .ind-cap{margin:0 0 .3rem;font-family:var(--sans);font-size:.72rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
div.ind-defs .ind-g{margin:.7rem 0 0;font-size:.72rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
div.ind-defs .ind-gen{margin:.2rem 0 .3rem}
div.ind-defs dt a{color:inherit;text-decoration-color:var(--rule)}
div.ind-defs .ind-master{margin:.7rem 0 0;color:var(--muted)}
div.ind-srv{margin:.2rem 0 1.4rem;padding:.1rem 0 .2rem}
div.ind-mst{margin:.3rem 0 1rem}
.ind-tl{font-family:var(--sans);font-size:.72rem;font-weight:400;color:var(--muted)}
div.ind-defs .ind-in{color:var(--muted)}
div.ind.ind-full table{min-width:0}
div.ind.ind-oil table + table{margin-top:.6rem}
</style>"""


def problems(series):
    """For ./bib check: (level, where, message). Span syntax, unknown vars, a statement for no series, and the
    series a calendar page shows with no servant there [indicator-servant]."""
    from . import indicators as I
    out = []
    if not os.path.exists(PATH):
        return [("error", "indicators/concepts.yaml", "the master statement of indicator concepts is missing")]
    m = load()
    data = I.load()
    for sid, t in (m.get("series") or {}).items():
        if sid not in data:
            out.append(("warn", "indicators/concepts.yaml", f"statement for {sid!r}, which is no series in indicators/"))
        try:
            parse(t)
        except ValueError as e:
            out.append(("error", "indicators/concepts.yaml", f"{sid}: {e}"))
        left = re.findall(r"(?<!\{)\{([A-Z][A-Z0-9_]*)\}(?!\})", t)
        if left:
            out.append(("error", "indicators/concepts.yaml", f"{sid}: unknown var {left[0]!r}"))
    for sid in data:
        if sid not in (m.get("series") or {}):
            out.append(("error", "indicators/concepts.yaml", f"no statement for series {sid!r}"))
    for abbr, sid in plan(series, data).gaps():
        out.append(("warn", "indicators/concepts.yaml",
                    f"{abbr}: series {sid!r} has no servant (no statement survives for its periods); its rows link "
                    "to the master"))
    return out
