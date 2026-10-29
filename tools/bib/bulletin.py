"""Checks for the *Department of State Bulletin* list of the daybook (daybook/bulletin/<YYYY>.yaml).

The rows are written by tools/daybook/make_bulletin.py (its docstring: the rules, RULES 1-8) and shown by
tools/bib/daybook.py (STYLE 11). Here only what `./bib check` holds them to:

- every row filed within the calendar's span (Jan. 6, 1960, to Jan. 20, 1969);
- its issue an issue of sources/dsb-issues.yaml, a Monday, and the day filed not after the issue nor more than sixty
  days before it (a release the issue prints);
- `dated` release or issue, and a row dated by the issue filed on the issue's day;
- a page, a title, and a key `dsb:<issue>:<page>:<n>` that agrees with them, each key once.
"""
import datetime
import glob
import os
import re


from . import store

DIR = os.path.join(store.ROOT, "daybook", "bulletin")
ISSUES = os.path.join(store.ROOT, "sources", "dsb-issues.yaml")
FROM, TO = datetime.date(1960, 1, 6), datetime.date(1969, 1, 20)


def problems():
    out = []
    issues = {str(r["date"]) for r in (store.load_yaml(ISSUES) or {}).get("issues", [])}
    seen = set()
    for f in sorted(glob.glob(os.path.join(DIR, "[0-9][0-9][0-9][0-9].yaml"))):
        name = os.path.basename(f)
        for x in (store.load_yaml(f) or {}).get("docs", []):
            k = x.get("key", "?")
            where = f"{name} {k}"
            if k in seen:
                out.append((where, "duplicate key"))
            seen.add(k)
            try:
                day = datetime.date.fromisoformat(str(x["date"]))
                iss = datetime.date.fromisoformat(str(x["issue"]))
            except Exception:
                out.append((where, "bad date or issue"))
                continue
            if not FROM <= day <= TO:
                out.append((where, f"filed {day}, outside the calendar's span"))
            if str(iss) not in issues or iss.weekday() != 0:
                out.append((where, f"issue {iss} is no issue of sources/dsb-issues.yaml"))
            if not iss - datetime.timedelta(days=60) <= day <= iss:
                out.append((where, f"filed {day}, not within sixty days before its issue {iss}"))
            if x.get("dated") not in ("release", "issue") or x.get("dated") == "issue" and day != iss:
                out.append((where, "dated must be release or issue, and an issue's row filed on its day"))
            if not x.get("title") or not isinstance(x.get("page"), int):
                out.append((where, "no title or page"))
            elif not re.match(rf"^dsb:{iss}:{x['page']}:\d+$", k):
                out.append((where, "key does not agree with the issue and page"))
    return out
