"""The calendar's Record cites by chamber and day -> Bluebook 13.5 (the owner, Nov. 4, 2026):
'[111 Cong. Rec., House, Jan. 4, 1965](url)' -> '[111 Cong. Rec. (1965)](url)', and 'Check: the page.' in the note;
a page given inside the brackets or just after the link (', 3220', ', 4379 ff', ', 899-903, at 902') goes inside:
'[108 Cong. Rec. 3220 (1962)](url)', '[.. 899, 902 (..)](url)'."""
import re, sys, glob
PG = r"\d+(?:[–-]\d+)?"
PAT = re.compile(r"\[(?:(\d{2,3}) )?Cong\. Rec\., (House|Senate), ([A-Z][a-z]+\.? \d{1,2}), (\d{4})(?:, (" + PG + r"))?\]\(([^)]*)\)"
                 r"(?:, (" + PG + r")(?: ff)?(?:, at (\d+))?(?=[\s.;,)']|$))?")
def first_step():
    global total, unpaged, notes
    total = unpaged = notes = 0
    for f in sorted(glob.glob("lists/cal/*.yaml")):
        lines = open(f).read().split("\n"); ch = False
        for i, ln in enumerate(lines):
            if not PAT.search(ln):
                continue
            assert re.match(r"^    n: ", ln), (f, i, ln[:80])
            miss = [0]; cnt = [0]
            def sub(m):
                vol, chamber, day, year, p_in, url, p_out, at = m.groups()
                v = int(year) - 1854
                if vol and int(vol) != v:
                    sys.exit(f"volume {vol} for {year}: {f}:{i+1}")
                cnt[0] += 1
                p = p_in or p_out
                if p and at:
                    p = re.split(r"[–-]", p)[0] + ", " + at
                if not p:
                    miss[0] += 1
                return f"[{v} Cong. Rec. {p + ' ' if p else ''}({year})]({url})"
            new = PAT.sub(sub, ln)
            total += cnt[0]
            if miss[0]:
                unpaged += miss[0]; notes += 1
                chk = "Check: the page." if miss[0] == 1 else "Check: the pages."
                head, val = new.split("n: ", 1)
                if val.startswith("'"):
                    assert val.rstrip().endswith("'"), (f, i)
                    body = val.rstrip()[1:-1]
                else:
                    body = val.rstrip().replace("'", "''")
                body = body + ("" if body.endswith((".", "?", ".)")) else ".") + " " + chk
                new = head + "n: '" + body + "'"
            lines[i] = new; ch = True
        if ch:
            open(f, "w").write("\n".join(lines))
    print(f"{total} cites converted; {unpaged} without a page, in {notes} notes")


# The second step (the owner, Nov. 4, 2026: "Add them to all the citation block items. Leave the gloss as it is for
# now."): the year after the page in the entries' notes (`n`), never a gloss: '[110 Cong. Rec. 14957](url)' ->
# '[110 Cong. Rec. 14957 (1964)](url)', the year the volume's (vol. 106 is 1960). Run: python3 -I THIS --years.
YEARLESS = re.compile(r"\[(\d{3}) Cong\. Rec\. (\d[\d–, -]*\d|\d)\]\(")


def add_years():
    n_cites = n_files = 0
    for f in sorted(glob.glob("lists/cal/*.yaml")):
        lines = open(f).read().split("\n"); ch = False
        for i, ln in enumerate(lines):
            if not re.match(r"^    n: ", ln) or not YEARLESS.search(ln):
                continue
            def sub(m):
                return f"[{m.group(1)} Cong. Rec. {m.group(2)} ({int(m.group(1)) + 1854})]("
            new, k = YEARLESS.subn(sub, ln)
            n_cites += k; lines[i] = new; ch = True
        if ch:
            open(f, "w").write("\n".join(lines)); n_files += 1
    print(f"{n_cites} years added, in {n_files} files")


if __name__ == "__main__":
    add_years() if "--years" in sys.argv else first_step()
