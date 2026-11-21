"""Standing conditions (the owner, Nov. 12, 2026): a condition of public importance a paper reports as such (a senator who
has not endorsed the ticket, a bill held in committee) is an entry on the paper's day, `c` "As the *Times* reports it:
..." (notes/briefs/batch12-press.md), an entry like any other. "As reported. Every standing condition, grouped by thread."

    ./bib check        [report-opener] warnings: a `c` opening "As ... has it:" or "As ... reports it:" whose note cites
                       no newspaper, wire or broadcast

STYLE
1. No label, no rule, no tag (the owner, Nov. 21, 2026: "Could we rename the "As reported" label to save future
   readers/auditors from this error? It's not a particularly lucid label. Actually, yes. Just drop the label
   altogether."): a standing condition renders on its day exactly as any other entry (daybook.py), and the tag
   `form:state`, which made the label and the left rule of Nov. 12, is retired from every entry. is_state and
   register_html below read the retired tag and so find nothing; nothing in the build calls them.
2. No register (the owner, Nov. 18, 2026: "They shouldn't have a separate human-readable bucket at all. They're just a
   kind of calendar entry ... they should sit in the calendar with all the others"): the index's register of Nov. 12
   is taken off; register_html stays for a reader's own query, called by nothing in the build. A later report of the
   same condition is an entry of its own (its note points back, "See [[...]]").
3. The opener is the press's alone (the owner, Nov. 21, 2026: "Why isn't this just a normal entry?"): only a
   newspaper's, a wire's or a broadcast's report of a standing condition on its day opens "As the *Times* reports
   it: ..."; an archive's, an embassy's, a ministry's or a historian's report is a normal entry, its source in the
   note ("Shanghai 上海: on a single day ..."; a dated dispatch as the event, "British embassy in Peking to the
   Foreign Office: ..."). `check` warns [report-opener] (problems()) on a `c` opening "As X has it:" or "As X
   reports it:" (X up to the first colon; "have it", "report it" too, and the frames the retired entries used,
   "gives it", "counts it", "reckons it") whose note cites no press: a link to a host,
   a run of words or a card that the provenance registry (sources/provenance.yaml) files as `press`, its series or
   its works (vis.registry). `ok:report-opener` silences an entry.
"""
import html
import re

from . import calsplit, chron, cjk, loose, markup, store

RULE = "report-opener"
OPENER = re.compile(r"^As\s[^:]{1,300}?\b(?:has|have|reports|report|gives|give|counts|count|reckons|reckon)\s+it\b"
                    r"[^:]{0,200}:")


def is_state(e):
    """The retired tag (STYLE 1): no entry carries it."""
    return "form:state" in store.as_list(e.get("tags"))


def _inline(s):
    s = html.escape(str(s or ""), quote=False)
    s = markup.LINK_RE.sub(r'<a href="\2">\1</a>', s)
    s = re.sub(r"\[\[[^\]|]+\|([^\]]+)\]\]", r"\1", s)
    s = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s)
    return re.sub(r"\*([^*]+)\*", r"<i>\1</i>", s)


def register_html(lst, thread_name, thread_key):
    """The register (STYLE 2), or '' where the calendar holds no state entry."""
    rows = {}
    for sec, e in lst.entries():
        if is_state(e) and e.get("thread") and e.get("date"):
            rows.setdefault(e["thread"], []).append(e)
    if not rows:
        return ""
    out = ['<section class="streg" id="standing"><h2>Standing conditions, as reported</h2>'
           '<p class="stn">Conditions of public importance a paper reported as such, each on the day of the report '
           '(a senator who has not endorsed the ticket, a bill held in committee), by thread.</p>']
    for t in sorted(rows, key=lambda t: thread_key(lst, t)):
        out.append(f'<h3>{html.escape(thread_name(lst, t))}</h3><ul>')
        for e in chron.sort(lst, rows[t]):            # in the calendar's order (chron.py)
            half = calsplit.half_of_date(lst, loose.place_iso(e))
            link = calsplit.href(lst, half, e["id"])
            out.append(f'<li><a href="{html.escape(link)}">{html.escape(str(e.get("when") or e["date"]))}, '
                       f'{str(e["date"])[:4]}</a>: {_inline(cjk.drop(e.get("c")))}</li>')   # the line as shown (cjk.py)
        out.append("</ul>")
    out.append("</section>")
    return "".join(out)


STYLE = """<style>
.streg{margin:2.4rem 0 1rem}.streg h2{font-size:1.15rem}.streg h3{font-family:var(--sans);font-size:.75rem;
  font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:1.2rem 0 .3rem}
.streg ul{list-style:none;margin:0;padding:0}.streg li{padding:.3rem 0;border-top:1px dotted var(--rule)}
.streg .stn{font-size:.9rem;color:var(--muted)}
</style>"""


def opener(c):
    """True where `c` opens with a report's frame, "As X has it:", "As X reports it:" (or gives, counts, reckons it)
    (STYLE 3)."""
    return bool(OPENER.match(str(c or "")))


def _press_series():
    from . import vis
    return [s for s in vis.registry()["series"] if s.get("kind") == "press"]


def press_cited(n, press=None):
    """True where the note cites the press: a link to a press series' host, a press series' words, or a card the
    registry files as press (its works' kind, or a press series' cards)."""
    from . import vis
    n = str(n or "")
    press = _press_series() if press is None else press
    for m in markup.LINK_RE.finditer(n):
        s = vis.series_for_url(m.group(2))
        if s and s.get("kind") == "press":
            return True
    for s in press:
        if any(pat and pat in n for pat in store.as_list(s.get("text"))):
            return True
    works = vis.registry().get("works") or {}
    for cid in re.findall(r"\[\[(w\.[^\]|]+)", n):
        if (works.get(cid) or {}).get("kind") == "press" or any(cid in store.as_list(s.get("cards")) for s in press):
            return True
    return False


def problems(series):
    """[report-opener] (STYLE 3): (id, message) for each calendar entry whose `c` opens with a report's frame and whose
    note cites no newspaper, wire or broadcast."""
    out, press = [], None
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for _, e in lst.entries():
            if not opener(e.get("c")):
                continue
            press = _press_series() if press is None else press
            if not press_cited(e.get("n"), press):
                out.append((e.get("id", "?"), "c opens \"As ... has it:\" or \"As ... reports it:\" but the note cites no "
                            "newspaper, wire or broadcast: write it as a normal entry, the source in the note "
                            "(standing.py, STYLE 3)"))
    return out
