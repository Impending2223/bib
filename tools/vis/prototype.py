#!/usr/bin/env python3
"""The visibility panel's October 1962 prototype (notes/proposals/visibility-spec.md, §9.2), now a wrapper (phase 3,
Nov. 12, 2026): the spans, the panel and its style and script are the build's own (tools/bib/vispage.py, its STYLE),
on every calendar page; this builds one month's page standalone, for trying a change at phone and desktop width
without a build. Nothing is written under build/.

    python3 tools/vis/prototype.py [--month 1962-10] [--out PATH]

STYLE
 1. The month is rendered by the site's own code (build.build_list and the calendar's injects, as build.run does for a
    year's page), the page's sections narrowed to the threads section (the threads with an entry in the month) and the
    month itself. The days' folded blocks stay inline (no lazydays.split: no month files beside a standalone page).
    The quotation marks are curled as smart.write curls them.
 2. The panel's style and script (tools/bib/vispage.css, .js) inlined, a standalone page having no build/vis/ beside it.
 3. Links the standalone page cannot hold (another year's page, a day of 1962 outside October, the site's other pages)
    point to the site (SITE).
"""
import argparse
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from bib import store, build, calsplit, contents, daybook, smart, vispage   # noqa: E402

SITE = "https://impending2223.github.io/bib/"
DEFAULT_OUT = "/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/vis-proto"


def esc(t):
    return html.escape(str(t), quote=True)


def install(series, lst, month):
    """The site's renderer, narrowed to the month (STYLE 1); its entries carry their claims as the build's do."""
    sec = next(s for s in lst.sections if str(s.extra.get("from", ""))[:7] == month)
    half = calsplit.half_of_section(lst, sec)
    members = build.thread_members(lst)
    orig_half_sections = build.half_sections

    def half_sections(l, h):
        out = []
        for s in orig_half_sections(l, h):
            if not s.extra.get("from"):                      # the threads section: the month's threads only
                import copy
                c = copy.copy(s)
                c.entries = [e for e in s.entries
                             if any(str(m.get("date", ""))[:7] == month
                                    for t in store.as_list(e.get("see") or e["id"].split(".", 2)[2])
                                    for m in members.get(t, []))]
                out.append(c)
            elif s is sec:
                out.append(s)
        return out
    build.half_sections = half_sections
    return sec, half


def render(series, month):
    """The month's page as the site renders a year's (build.run's calendar chain), narrowed (STYLE 1)."""
    from bib import (appropriations, bills, budgets, congress, conventions, dayblocks, executive, feeds, governors,
                     indicators, legislatures, oilworld, primaries, specials, statefin, vnmap)
    lst = next(l for l in series.lists.values() if l.kind == "calendar")
    sec, half = install(series, lst, month)
    daybook.SERIES = series
    linker = build.Linker(series)
    contents.FOUND.clear()
    calsplit.CUR.update(half=half, mode="list")
    page = build.build_list(series, lst.key, linker, half)
    page = congress.inject(page, series, linker, "list")
    page = executive.inject(page, series, linker, "list")
    for m in (specials, primaries, conventions, governors, legislatures, oilworld, statefin, budgets, bills,
              appropriations, vnmap):
        page = m.inject(page, series)
    page = indicators.inject(page, series, "list")
    page = dayblocks.inject(page, series, "list")
    page = daybook.inject(page)
    page = feeds.inject(page, lst, half)
    page = contents.finish(page, lst, half, defer=True)
    page = contents.fill(page, lst, half)
    page = page.replace("</head>", calsplit.STYLE + "\n</head>", 1)
    page = page.replace("</body>", calsplit.SCRIPT + "\n</body>", 1)
    page = calsplit.route(page, lst, half)
    calsplit.CUR.update(half=None)
    return page, lst, sec, half


def site_links(page, own):
    """Links the standalone page cannot hold, to the site (STYLE 5)."""
    ids = set(re.findall(r'\sid="([^"]+)"', page))

    def fix(m):
        h = html.unescape(m.group(2))
        if h.startswith("#"):
            if h[1:] in ids or not h[1:]:
                return m.group(0)
            return f'{m.group(1)}"{esc(SITE + own + ".html" + h)}"'
        if re.match(r"^(?:[a-z][a-z0-9+.-]*:|//)", h):
            return m.group(0)
        return f'{m.group(1)}"{esc(SITE + h)}"'
    return re.sub(r'(\shref=)"([^"]*)"', fix, page)


def inline(page):
    """The panel's style and script inlined: a standalone page has no build/vis/ beside it."""
    css = open(os.path.join(vispage.HERE, "vispage.css"), encoding="utf-8").read()
    js = open(os.path.join(vispage.HERE, "vispage.js"), encoding="utf-8").read()
    page = page.replace("</head>", f"<style>\n{css}</style>\n</head>", 1)
    return page.replace("</body>", f"<script>\n{js}</script>\n</body>", 1)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--month", default="1962-10")
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    out = a.out or os.path.join(DEFAULT_OUT, f"vis-prototype-{a.month}.html")
    smart_write = smart.write
    smart.write = lambda *x, **k: (_ for _ in ()).throw(RuntimeError("the prototype writes nothing to build/"))
    try:
        series = store.Series()
        page, lst, sec, half = render(series, a.month)
    finally:
        smart.write = smart_write
    own = calsplit.page_key(lst, half)
    title = f"{sec.title}: visibility (prototype)"
    page = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", page, count=1, flags=re.S)
    page = page.replace('<div id="crumb"><b>', f'<div id="crumb"><b>{esc(sec.title)}, prototype · ', 1)
    page = inline(page)                           # the panel itself the build puts (vispage.py, STYLE 4)
    page = site_links(page, own)
    page = smart.smarten(page)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(out, f"{len(page) // 1024} KB")
    print(vispage.report())
    print("polities the month's claims carry:", " ".join(sorted(vispage.PAGE["used"])))

if __name__ == "__main__":
    main()
