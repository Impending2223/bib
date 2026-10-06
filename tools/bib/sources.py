"""The register of State election sources (sources/states.yaml): its shape, checked by ./bib check.

The register is read by people and sessions, not by the build; the header of the YAML is its schema. The checks
keep it usable: every State and D.C. once, each source with a title and an online list, each online copy with a
url, an access from the legend, and the date it was checked."""
import os
import re

import yaml

from . import store

PATH = os.path.join(store.ROOT, "sources", "states.yaml")
STATES = set("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC "
             "ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split())
ACCESS = {"open", "borrow", "bot-check", "blocked", "dead", "other"}


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
        for s in e.get("sources") or []:
            if not s.get("title"):
                out.append(("sources/states.yaml", f"{st}: a source without a title"))
            for o in s.get("online") or []:
                if not o.get("url"):
                    out.append(("sources/states.yaml", f"{st} {s.get('title')}: an online copy without a url"))
                if o.get("access") not in ACCESS:
                    out.append(("sources/states.yaml", f"{st} {o.get('url')}: access {o.get('access')!r} not in the legend"))
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(o.get("checked", ""))):
                    out.append(("sources/states.yaml", f"{st} {o.get('url')}: no checked date"))
    for st in sorted(STATES - seen):
        out.append(("sources/states.yaml", f"{st} missing"))
    return out
