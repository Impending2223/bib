"""The *New York Times* cited by date and not otherwise linked -> linked to TimesMachine's issue of that day (the owner,
Nov. 5, 2026: "link the paper and date to the corresponding TimesMachine page for that date (e.g., '[New York Times,
Jan. 18, 1966](link)')"). '*New York Times*, Jan. 18, 1966' -> '[*New York Times*, Jan. 18, 1966](https://timesmachine
.nytimes.com/timesmachine/1966/01/18/issue.html)', the URL the day layout's line uses (daybook.TM). Not inside a link's
text already; the form '*N.Y. Times*' too. Every list's files. Run: python3 -I THIS [--dry]."""
import re, sys, glob
TM = "https://timesmachine.nytimes.com/timesmachine/{y}/{m:02d}/{d:02d}/issue.html"
MON = {"Jan.": 1, "Feb.": 2, "Mar.": 3, "Apr.": 4, "May": 5, "June": 6, "July": 7, "Aug.": 8, "Sept.": 9, "Oct.": 10,
       "Nov.": 11, "Dec.": 12, "January": 1, "February": 2, "March": 3, "April": 4, "August": 8, "September": 9,
       "October": 10, "November": 11, "December": 12}
PAT = re.compile(r"\*(New York Times|N\.Y\. Times)\*,? (" + "|".join(re.escape(k) for k in MON) + r") (\d{1,2}), (\d{4})")


def inside_link(text, i):
    """True where position i sits within a markdown link's [text] (an open '[' not yet closed)."""
    depth = 0
    for ch in text[:i]:
        if ch == "[":
            depth += 1
        elif ch == "]" and depth:
            depth -= 1
    return depth > 0


def fix(line):
    out, last, k = [], 0, 0
    for m in PAT.finditer(line):
        if inside_link(line, m.start()):
            continue
        mon, d, y = MON[m.group(2)], int(m.group(3)), int(m.group(4))
        out.append(line[last:m.start()])
        out.append(f"[{m.group(0)}]({TM.format(y=y, m=mon, d=d)})")
        last = m.end(); k += 1
    out.append(line[last:])
    return "".join(out), k


def main(dry=False):
    total = files = 0
    for f in sorted(glob.glob("lists/*/*.yaml")):
        lines = open(f).read().split("\n"); ch = 0
        for i, ln in enumerate(lines):
            if "Times*" not in ln:
                continue
            new, k = fix(ln)
            if k:
                assert not re.match(r"^\s*-?\s*\w+: \[", new) or re.match(r"^\s*-?\s*\w+: \[", ln), (f, i, ln[:80])
                lines[i] = new; ch += k
        if ch:
            total += ch; files += 1
            if not dry:
                open(f, "w").write("\n".join(lines))
    print(f"{total} cites linked, in {files} files")


if __name__ == "__main__":
    main("--dry" in sys.argv)
