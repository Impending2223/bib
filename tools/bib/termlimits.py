"""The bars on a governor's re-election: elections/term-limits.yaml (kept by hand; its header is the schema).

A race whose incumbent the race tables call "term-limited" (governors.fate: "barred from another term") takes the
provision in force on the day of the race, put into its note by governors.note (governors STYLE 9).

STYLE
 1. The bar in a parenthesis after "barred from another term": the provision as the Bluebook cites it, linked to the
    first source read, then a colon and the bar in a few words: "(Mo. Const. art. IV, § 17 (1945, amended 1965): not eligible for
    election as his own successor)".
 2. A provision not yet read: "(the provision not yet read)", and the rule's Check.
 3. What the sources read do not settle follows the note's own sentences as "Check: ..." (the rule's `check`).
 4. A rule governs from its `from` to the day before its `to`; a year alone stands for the year's first day.
"""
import os
import re

from . import store

PATH = os.path.join(store.ROOT, "elections", "term-limits.yaml")
_C = {}
SPAN = re.compile(r"^\d{4}(-\d\d(-\d\d)?)?$")


def load():
    if "d" not in _C:
        _C["d"] = (store.load_yaml(PATH) if os.path.exists(PATH) else {}) or {}
    return _C["d"]


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def rule(st, date):
    """The State's provision in force on the ISO date (STYLE 4), or None."""
    for r in (load().get(st) or {}).get("rules") or []:
        if str(r.get("from") or "0") <= date and (not r.get("to") or date < str(r["to"])):
            return r
    return None


def bar_html(st, date):
    """' (cite: short)' for the race's note (STYLE 1, 2), or ''."""
    r = rule(st, date)
    if not r:
        return ""
    if not r.get("cite"):
        return " (the provision not yet read)"
    src = next((s for s in r.get("sources") or [] if s.get("url")), None)
    cite = esc(r["cite"])
    if src:
        cite = f'<a href="{esc(src["url"])}">{cite}</a>'
    return f" ({cite}: {esc(r.get('short') or '')})" if r.get("short") else f" ({cite})"


def check_html(st, date):
    """'Check: ...' for the race's note (STYLE 3), or ''."""
    r = rule(st, date)
    if not r or not r.get("check"):
        return ""
    c = str(r["check"]).strip().rstrip(".")
    return f"Check: {esc(c)}."


def problems(races=()):
    """The file: each State a State, each rule's span readable and in order, a rule with a cite has its words, short,
    scope and a source with a url; each barred race finds a rule."""
    from .congress import STATE
    where = "elections/term-limits.yaml"
    out = []
    for st, v in load().items():
        if st not in STATE:
            out.append((where, f"{st}: not a State"))
            continue
        last = None
        for r in v.get("rules") or []:
            for k in ("from", "to"):
                if r.get(k) is not None and not SPAN.match(str(r[k])):
                    out.append((where, f"{st}: bad {k} {r[k]!r}"))
            if r.get("to") and str(r["to"]) <= str(r.get("from") or ""):
                out.append((where, f"{st}: rule ends before it begins"))
            if last is not None and str(r.get("from") or "") < last:
                out.append((where, f"{st}: rules out of order"))
            last = str(r.get("to") or "9999")
            if r.get("cite"):
                for k in ("short", "words", "scope"):
                    if not r.get(k):
                        out.append((where, f"{st}: {r['cite']}: no {k}"))
                if not any(s.get("url") for s in r.get("sources") or []):
                    out.append((where, f"{st}: {r['cite']}: no source with a url"))
            elif not r.get("check"):
                out.append((where, f"{st}: a rule not read and no check"))
            for s in r.get("sources") or []:
                if not s.get("label"):
                    out.append((where, f"{st}: a source without a label"))
        for c in v.get("changes") or []:
            if not SPAN.match(str(c.get("date") or "")) or not c.get("sources"):
                out.append((where, f"{st}: a change without its date or sources"))
    for r in races:
        if not rule(r["st"], r["date"]):
            out.append((where, f"{r['date']} {r['st']}: incumbent barred, no provision in the file"))
    return out
