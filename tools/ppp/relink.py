"""Rewrite the lists' links to APP documents as Public Papers cites, where an item matches (tools/bib/ppp.py, STYLE 3).

    python3 tools/ppp/relink.py [--dry-run] [--log FILE]

In every lists/<key>/*.yaml, a link '[Title](https://www.presidency.ucsb.edu/documents/...)' whose document
sources/ppp-matches.json matches becomes 'Title, [1961 Pub. Papers 1](https://www.govinfo.gov/.../PPP-1961-book1.pdf#page=59)'
(the Bluebook's form, the title kept as written, the cite linked to the item's first page; what followed the link,
the date in parentheses, stays). A link whose text is "APP" becomes the cite alone. A link nothing matches is left as
it is. Each file is read and written at once, only where something changed (other sessions edit these files), and
every change is printed: file, line, the APP address, the cite.
"""
import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bib import ppp  # noqa: E402

LINK = re.compile(r"\[((?:[^\[\]]|\[[^\[\]]*\])+?)\]\((https?://(?:www\.)?presidency\.ucsb\.edu/documents/[^)\s]+)\)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--log")
    a = ap.parse_args()
    log, n_files, n_links, kept = [], 0, 0, 0
    for p in sorted(glob.glob(os.path.join(ROOT, "lists", "*", "*.yaml"))):
        with open(p, encoding="utf-8") as f:
            s = f.read()
        if "presidency.ucsb.edu/documents/" not in s:
            continue
        changes = []

        def sub(m):
            nonlocal kept
            text, url = m.group(1), m.group(2)
            it = ppp.match(url)
            if not it:
                kept += 1
                return m.group(0)
            new = f"[{it['cite']}]({it['url']})" if text.strip() == "APP" else f"{text}, [{it['cite']}]({it['url']})"
            line = s.count("\n", 0, m.start()) + 1
            changes.append(f"{os.path.relpath(p, ROOT)}:{line}: {url} -> {it['cite']} ({it['pkg']} #{it['n']})")
            return new
        t = LINK.sub(sub, s)
        if t != s:
            n_files += 1
            n_links += len(changes)
            log += changes
            if not a.dry_run:
                with open(p, encoding="utf-8") as f:            # the file again, at once: unchanged since read?
                    if f.read() != s:
                        print(f"{p}: changed while reading; skipped (rerun)", file=sys.stderr)
                        continue
                with open(p, "w", encoding="utf-8") as f:
                    f.write(t)
    for l in log:
        print(l)
    print(f"{n_links} links in {n_files} files rewritten; {kept} APP links left (no item matches)", file=sys.stderr)
    if a.log:
        with open(a.log, "w", encoding="utf-8") as f:
            f.write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
