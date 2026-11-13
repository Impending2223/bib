"""Standing conditions (the owner, Nov. 12, 2026): a condition of public importance a paper reports as such (a senator who
has not endorsed the ticket, a bill held in committee) is an entry on the paper's day, tagged `form:state`
(notes/briefs/batch12-press.md). "As reported. Every standing condition, grouped by thread."

STYLE
1. On the day: a state entry is set off by a rule at its left and the label "As reported" above its rubric, so it does
   not read as an act (daybook.py).
2. The register: on the calendar's index (cal.html), every state entry, grouped by its thread (the thread index's
   order), each by its date, linked to the entry on its page, then its `c`. A later report of the same condition is
   a row of its own (its note points back, "See [[...]]"); nothing is kept apart from the entries.
"""
import html
import re

from . import calsplit, store

LABEL = "As reported"


def is_state(e):
    return "form:state" in store.as_list(e.get("tags"))


def _inline(s):
    s = html.escape(str(s or ""), quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', s)
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
        for e in sorted(rows[t], key=lambda e: str(e["date"])):
            half = calsplit.half_of_date(lst, e["date"])
            link = calsplit.href(lst, half, e["id"])
            out.append(f'<li><a href="{html.escape(link)}">{html.escape(str(e.get("when") or e["date"]))}, '
                       f'{str(e["date"])[:4]}</a>: {_inline(e.get("c"))}</li>')
        out.append("</ul>")
    out.append("</section>")
    return "".join(out)


STYLE = """<style>
.streg{margin:2.4rem 0 1rem}.streg h2{font-size:1.15rem}.streg h3{font-family:var(--sans);font-size:.75rem;
  font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:1.2rem 0 .3rem}
.streg ul{list-style:none;margin:0;padding:0}.streg li{padding:.3rem 0;border-top:1px dotted var(--rule)}
.streg .stn{font-size:.9rem;color:var(--muted)}
</style>"""
