"""Match the American Presidency Project's documents (the daybook's President rows, the Names' index of documents) to
the items of the Public Papers (sources/ppp-text/, tools/ppp/make_ppp_text.py), and write sources/ppp-matches.json.

    python3 -I tools/ppp/match_app.py [--report FILE]

The file also carries each volume's particulars and an index of its items ([title, date (or the date it is
filed under), first page, last page, PDF page], by number), so the build reads the matches (tools/bib/ppp.py): wherever the series links an APP document that a Public Papers item
prints, it links the item's first page in GPO's volume instead, and keeps the APP link where nothing matches. The
build needs no network; rerun after make_ppp_text.py or make_daybook.py.

STYLE (the rule; mechanical):
 1. The APP documents: every daybook row from src ppp (daybook/<YYYY-MM>.yaml) and every row of sources/app-index.jsonl
    dated Jan. 1, 1960, to Jan. 20, 1969, by its address; its date and title as APP gives them, its President.
 2. Not matched: APP's executive orders and proclamations (the Public Papers list them in an appendix and do not
    print them), the party platforms, a candidate's or a Vice President's documents, anything of a President whose
    volumes are not read (Nixon, from Jan. 20, 1969).
 3. Candidates: the items of the same President dated the same day; where none fits, a day either side (a text dated
    one day and released the next), then two or three; an item whose heading gives its month alone, within the month. Score: the titles,
    folded (case, punctuation, "the President's", the volume's misreadings aside), as the larger of the two
    strings' likeness (difflib's ratio) and the share of APP's words the item's title holds (a news conference's
    date in its title aside). Taken: the best at 0.72 or more the same day, 0.85 a day off or by the month alone,
    0.92 two or three days off; ties go to the first in the volume.
 4. Several APP documents may take one item (APP prints an exchange of letters, or a statement and the letter it
    goes with, apart where the volume prints them as one item); the matches say so (`shared`).
"""
import argparse
import datetime
import difflib
import glob
import json
import lzma
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEXT = os.path.join(ROOT, "sources", "ppp-text")
OUT = os.path.join(ROOT, "sources", "ppp-matches.json")
LO, HI = "1960-01-01", "1969-01-20"
NOT_PRINTED = re.compile(r"^(Executive Order|Proclamation)\s+\d|Party Platform|Platform of \d{4}|^\d{4} .*Platform")
PRES = {"Dwight D. Eisenhower": "Eisenhower", "John F. Kennedy": "Kennedy", "Lyndon B. Johnson": "Johnson"}
TERMS = {"Eisenhower": ("1960-01-01", "1961-01-20"), "Kennedy": ("1961-01-20", "1963-11-22"),
         "Johnson": ("1963-11-22", "1969-01-20")}


def fold(t):
    t = (t or "").lower().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("\xad", "")
    t = re.sub(r"\b(of )?(january|february|march|april|may|june|july|august|september|october|november|december)"
               r" \S{1,3},? \d{4}\b", " ", t)                     # a news conference's date
    t = re.sub(r"\bthe president's\b|\bthe president\b|\bpresident's\b", " ", t)
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    t = re.sub(r"\b(the|of|a|an|and|to|on|in|for|at|by|with|upon|his|her)\b", " ", t)
    return " ".join(t.split())


def score(a, b):
    fa, fb = fold(a), fold(b)
    if not fa or not fb:
        return 0.0
    r = difflib.SequenceMatcher(None, fa, fb).ratio()
    wa, wb = set(fa.split()), set(fb.split())
    share = len(wa & wb) / len(wa) if wa else 0
    share2 = len(wa & wb) / len(wb) if wb else 0
    return max(r, min(share, share2) if min(len(wa), len(wb)) >= 2 else 0, (share + share2) / 2)


VOLUMES = {}


def load_items():
    items = []
    for p in sorted(glob.glob(os.path.join(TEXT, "PPP-*.json.xz"))):
        d = json.loads(lzma.decompress(open(p, "rb").read()))
        VOLUMES[d["package"]] = {k: d[k] for k in ("title", "president", "years", "book", "span", "pdf", "details",
                                                   "pages", "folios", "missing")}
        VOLUMES[d["package"]]["items"] = {
            str(it["n"]): [it["title"], it.get("date") or it.get("filed"), it["page"], it["page_to"], it["pdf"]]
            for it in d["items"]}
        who = PRES.get(d["president"], d["president"])
        for i, it in enumerate(d["items"]):
            items.append({"pkg": d["package"], "n": it["n"], "date": it.get("date"), "month": it.get("month"),
                          "title": it["title"], "who": who, "i": i})
    return items


def app_rows():
    rows = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "daybook", "[0-9][0-9][0-9][0-9]-[0-9][0-9].yaml"))):
        for x in (yaml.safe_load(open(p, encoding="utf-8")) or {}).get("docs", []):
            if x.get("src") == "ppp" and x.get("url"):
                rows[x["url"]] = {"date": x["date"], "title": x["title"], "who": (x.get("author") or "").split()[-1:],
                                  "from": "daybook"}
    for l in open(os.path.join(ROOT, "sources", "app-index.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        try:
            d = datetime.datetime.strptime(r["date"], "%b %d, %Y").date().isoformat()
        except ValueError:
            continue
        if LO <= d <= HI and r["url"] not in rows:
            rows[r["url"]] = {"date": d, "title": r["title"].rstrip("."), "who": (r.get("who") or "").split()[-1:],
                              "from": "app-index"}
    for r in rows.values():
        r["who"] = r["who"][0] if r["who"] else ""
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report")
    a = ap.parse_args()
    items = load_items()
    by_day, by_month = {}, {}
    for it in items:
        if it["date"]:
            by_day.setdefault((it["who"], it["date"]), []).append(it)
        elif it["month"]:
            by_month.setdefault((it["who"], it["month"]), []).append(it)
    rows = app_rows()
    out, why = {}, {}
    for url, r in sorted(rows.items(), key=lambda kv: (kv[1]["date"], kv[0])):
        term = TERMS.get(r["who"])
        if NOT_PRINTED.search(r["title"]) or not term or not term[0] <= r["date"] <= term[1]:
            why[url] = "not printed" if NOT_PRINTED.search(r["title"]) else "not a President read"
            continue
        d = datetime.date.fromisoformat(r["date"])
        best = None
        tiers = [([d], .72), ([d - datetime.timedelta(1), d + datetime.timedelta(1)], .85),
                 ([d + datetime.timedelta(k) for k in (-3, -2, 2, 3)], .92)]
        for days, cut in tiers:
            cands = [it for x in days for it in by_day.get((r["who"], x.isoformat()), [])]
            if cut > .8:
                cands += by_month.get((r["who"], r["date"][:7]), [])
            sc = sorted(((score(r["title"], it["title"]), -it["i"], it) for it in cands),
                        key=lambda t: (t[0], t[1]), reverse=True)
            if sc and sc[0][0] >= cut:
                best = sc[0]
                break
        if best:
            it = best[2]
            out[url] = [it["pkg"], it["n"], round(best[0], 2)]
        else:
            why[url] = "no item"
    taken = {}
    for url, (pkg, n, s) in out.items():
        taken.setdefault((pkg, n), []).append(url)
    unmatched_ppp = [f"{it['pkg']}#{it['n']}" for it in items if (it["pkg"], it["n"]) not in taken]
    shared = sum(1 for v in taken.values() if len(v) > 1)
    day = {u for u, r in rows.items() if r["from"] == "daybook"}
    stats = {
        "app documents": len(rows), "daybook rows": len(day),
        "matched": len(out), "daybook rows matched": len(day & set(out)),
        "not printed (orders, proclamations, platforms)": sum(1 for v in why.values() if v == "not printed"),
        "not a sitting President's, or Nixon's": sum(1 for v in why.values() if v == "not a President read"),
        "no item": sum(1 for v in why.values() if v == "no item"),
        "ppp items": len(items), "ppp items matched": len(taken), "items shared by several APP documents": shared,
    }
    doc = {"made": "tools/ppp/match_app.py", "stats": stats,
           "volumes": VOLUMES,
           "matches": {u: v[:2] for u, v in sorted(out.items())},
           "unmatched_app": sorted(u for u, v in why.items() if v == "no item"),
           "unmatched_ppp": unmatched_ppp}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=0, sort_keys=False)
        f.write("\n")
    for k, v in stats.items():
        print(f"{k}: {v}")
    if a.report:
        with open(a.report, "w", encoding="utf-8") as f:
            for u in doc["unmatched_app"]:
                r = rows[u]
                f.write(f"APP {r['date']} {r['who']} {r['from']}: {r['title']}\n")
            ix = {(it["pkg"], it["n"]): it for it in items}
            for k in unmatched_ppp:
                pkg, n = k.split("#")
                it = ix[(pkg, int(n))]
                f.write(f"PPP {it['date'] or it['month']} {k}: {it['title']}\n")


if __name__ == "__main__":
    sys.exit(main())
