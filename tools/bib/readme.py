"""README.md kept current (the owner, Nov. 18, 2026: "the readme.md entry should list and link to all calendar and other
human-read pages ... Give the repo and PR/merge pass whatever simple tooling/tool call it needs to keep this readme.md
number updated").

    ./bib readme           rewrite README.md's calendar rows and counts from the data
    ./bib readme --check   say what is stale, exit 1 if anything is (the step before a PR and merge: changing.md)

STYLE
1. The site table's calendar row links the index (cal.html) and says what the calendar holds; its count line reads
   "N entries in T threads and S subthreads." (entries: every calendar entry but the threads' own; threads: th.yaml's
   entries without a parent; subthreads: with one).
2. The calendar's pages: a table of their own, under the site table, between the markers
   <!-- calendar-pages:start --> and <!-- calendar-pages:end -->, a row a page (calsplit.parts: every part, in order),
   the page's span linked, its contents (the part's title after the colon) beside it.
3. The works count in the Works row ("one entry a work (N)") from the catalogue.
4. The other pages: a table under the calendar's, between <!-- other-pages:start --> and <!-- other-pages:end -->, a
   row a family the pages' pass splits (tools/bib/pages.py): Names, its letters and ranges; Works, its letters; the
   Executive and Congress, their parts; every page linked by its label.
"""
import os
import re
import sys

from . import calsplit, store

URL = "https://impending2223.github.io/bib/"
START, END = "<!-- calendar-pages:start -->", "<!-- calendar-pages:end -->"


def counts(series):
    lst = series.lists["cal"]
    n = threads = subs = 0
    for sec, e in lst.entries():
        if e["id"].startswith("cal.thread."):
            if e.get("parent"):
                subs += 1
            else:
                threads += 1
        else:
            n += 1
    return n, threads, subs


def pages_table(series):
    lst = series.lists["cal"]
    rows = ["| page | contents |", "|------|----------|"]
    for p in calsplit.parts(lst):
        pt = str(p.get("page_title") or p.get("page"))
        span = re.sub(r"^Calendar,?\s*", "", pt) or pt
        title = str(p.get("title") or "")
        what = title.split(": ", 1)[1] if ": " in title else ""
        what = what[:1].upper() + what[1:] if what else "—"
        span = span[:1].upper() + span[1:]
        rows.append(f"| [{span}]({URL}{p['page']}.html) | {what} |")
    return "\n".join(rows)


PSTART, PEND = "<!-- other-pages:start -->", "<!-- other-pages:end -->"


def other_pages(series):
    """STYLE 4: the other human-read pages a page a part (tools/bib/pages.py): Names by letter and range, Works by
    letter, the Executive and Congress by their parts; a row a page family, every page linked."""
    from . import bibliography, lives, pages
    rows = ["| pages | parts |", "|-------|-------|"]
    letters = sorted({lives.letter_of(p) for p in lives.everyone(series)})
    rows.append(f"| [Names]({URL}names.html) | " + " · ".join(
        f"[{lab}]({URL}{pg}.html)" for pg, lab, _ in pages.names_sequence(letters)) + " |")
    if pages.works_split():
        ls = sorted(set(bibliography.letters(series).values()), key=lambda L: (L != "0", L))
        rows.append(f"| [Works]({URL}works.html) | " + " · ".join(
            f"[{'0–9' if L == '0' else L.upper()}]({URL}{pages.works_page_of_letter(L)}.html)" for L in ls) + " |")
    for fam, name in (("congress", "Elections and Congress"), ("executive", "Executive")):
        ps = pages.sections_plan(fam)
        if ps:
            rows.append(f"| [{name}]({URL}{fam}.html) | " + " · ".join(
                f"[{p['label']}]({URL}{p['page']}.html)" for p in ps) + " |")
    return "\n".join(rows)


def render(series, text):
    n, t, s = counts(series)
    text = re.sub(r"[\d,]+ entries in \d+ threads and \d+ subthreads\.", f"{n:,} entries in {t} threads and {s} subthreads.", text)
    nw = len(series.works.cards)
    text = re.sub(r"one entry a work \([\d,]+\)", f"one entry a work ({nw:,})", text)
    text = re.sub(r"\| page \| what it holds \|", "| page | contents |", text)
    block = f"{START}\n{pages_table(series)}\n{END}"
    if START in text and END in text:
        text = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block, text, flags=re.S)
    if PSTART in text and PEND in text:
        block2 = f"{PSTART}\n{other_pages(series)}\n{PEND}"
        text = re.sub(re.escape(PSTART) + r".*?" + re.escape(PEND), lambda m: block2, text, flags=re.S)
    return text


def run(series, check=False):
    path = os.path.join(store.ROOT, "README.md")
    old = open(path, encoding="utf-8").read()
    new = render(series, old)
    if START not in new:
        print("README.md: no calendar-pages markers; add them once (readme.py, STYLE 2)")
        return 1
    if new == old:
        print("README.md is current")
        return 0
    if check:
        print("README.md is stale: run ./bib readme")
        return 1
    open(path, "w", encoding="utf-8").write(new)
    print("README.md rewritten")
    return 0
