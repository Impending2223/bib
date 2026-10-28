"""The register of State election sources (sources/states.yaml): its shape, checked by ./bib check.

The register is read by people and sessions, not by the build; the header of the YAML is its schema. The checks
keep it usable: every State and D.C. once, each source with a title and an online list, each online copy with a
url, an access from the legend, and the date it was checked; every source and county or city record (`local`) with a
basis (a ground from the legend and a ref) and `cited_as` patterns that compile. `warnings()`: the listings
(notes/state-sources.md, notes/state-law-sources.md, by tools/sources/make_listing.py) stale against their registers;
the law register's own checks are in tools/bib/state_law.py."""
import os
import re

import yaml

from . import store

PATH = os.path.join(store.ROOT, "sources", "states.yaml")
STATES = set("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC "
             "ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split())
ACCESS = {"open", "borrow", "bot-check", "blocked", "dead", "other"}
GROUNDS = {"seen", "catalog", "law", "cited", "assumed"}


def basis_problems(where, it):
    """A register item's basis and cited_as (sources/states.yaml and sources/state-law.yaml share the form)."""
    out = []
    bs = it.get("basis")
    if not bs:
        return [(where, "no basis")]
    for b in bs:
        if not isinstance(b, dict) or b.get("ground") not in GROUNDS:
            out.append((where, f"basis ground {b.get('ground') if isinstance(b, dict) else b!r} not in the legend"))
        elif not str(b.get("ref") or "").strip():
            out.append((where, f"a {b['ground']} basis without a ref"))
    if any(isinstance(b, dict) and b.get("ground") == "assumed" for b in bs) and len(bs) > 1:
        out.append((where, "assumed beside another ground"))
    for c in it.get("cited_as") or []:
        try:
            re.compile(str(c))
        except re.error as e:
            out.append((where, f"cited_as {c!r} does not compile: {e}"))
        if not isinstance(c, str):
            out.append((where, f"cited_as {c!r} is not a string (quote it)"))
    return out


def online_problems(label, it, where="sources/states.yaml"):
    """Each online copy: a url, an access from the legend, the date it was checked."""
    out = []
    for o in it.get("online") or []:
        if not o.get("url"):
            out.append((where, f"{label}: an online copy without a url"))
        if o.get("access") not in ACCESS:
            out.append((where, f"{label} {o.get('url')}: access {o.get('access')!r} not in the legend"))
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(o.get("checked", ""))):
            out.append((where, f"{label} {o.get('url')}: no checked date"))
    return out


def problems():
    if not os.path.exists(PATH):
        return [("sources/states.yaml", "missing")]
    try:
        reg = yaml.safe_load(open(PATH, encoding="utf-8"))
    except yaml.YAMLError as e:
        return [("sources/states.yaml", f"does not load: {e}")]
    out, seen = [], set()
    for e in reg or []:
        st = e.get("st")
        if st not in STATES:
            out.append(("sources/states.yaml", f"unknown State {st!r}"))
        if st in seen:
            out.append(("sources/states.yaml", f"{st} twice"))
        seen.add(st)
        for i, s in enumerate(e.get("sources") or []):
            if not s.get("title"):
                out.append(("sources/states.yaml", f"{st}: a source without a title"))
            out += [(w, f"{st}-{i + 1}: {m}") for w, m in basis_problems("sources/states.yaml", s)]
            out += online_problems(f"{st}-{i + 1}", s)
        for j, l in enumerate(e.get("local") or []):
            if not l.get("body") or not l.get("record"):
                out.append(("sources/states.yaml", f"{st}-L{j + 1}: a local record without body or record"))
            out += [(w, f"{st}-L{j + 1}: {m}") for w, m in basis_problems("sources/states.yaml", l)]
            out += online_problems(f"{st}-L{j + 1}", l)
    for st in sorted(STATES - seen):
        out.append(("sources/states.yaml", f"{st} missing"))
    return out


def warnings():
    """The listings stale against their registers (tools/sources/make_listing.py writes them); a register title with
    a hyphen in a span of years (tools/bib/titles.py STYLE 2)."""
    import hashlib
    from .titles import span_dashes
    out = []
    try:
        reg = yaml.safe_load(open(PATH, encoding="utf-8")) or []
    except (OSError, yaml.YAMLError):
        reg = []
    for e in reg:
        for i, s in enumerate(e.get("sources") or []):
            t = str(s.get("title") or "")
            if span_dashes(t) != t:
                out.append(("sources/states.yaml", f"{e.get('st')}-{i + 1}: {t[:60]}: an en dash in a span of years [titles]"))
    for reg, md in (("states.yaml", "state-sources.md"), ("state-law.yaml", "state-law-sources.md")):
        rp = os.path.join(store.ROOT, "sources", reg)
        mp = os.path.join(store.ROOT, "notes", md)
        if not os.path.exists(rp):
            continue
        h = hashlib.sha256(open(rp, "rb").read()).hexdigest()[:16]
        first = open(mp, encoding="utf-8").readline() if os.path.exists(mp) else ""
        if f"<!-- register: {h} -->" not in first:
            out.append((f"notes/{md}", f"stale against sources/{reg}: rerun python3 tools/sources/make_listing.py"))
    return out
