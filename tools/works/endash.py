"""Hyphens to en dashes in ranges (the owner, Nov. 5, 2026: "replace hyphens with ndashes in page ranges and date
ranges"): '317-18' -> '317–18'; 'Jan. 20-22, 1966' -> 'Jan. 20–22, 1966'; 'Jan. 3, 1939-Jan. 3, 1969' -> '... 1939–Jan.
3, 1969'; '1961-63' -> '1961–63'. In the text fields of the hand-kept lists (c, n, r, s, a gloss's text), never in a
URL, an [[id]], a tag, an id or a date key. Not a number that is no range: a public law ('Pub. L. 88-352'), a report
or document number ('S. Rep. No. 88-830', 'No. 61-123'), a tape ('WH6407-11-4288'), a Congress and session ('86-2'
after 'Cong.'), anything joined to letters. Run: python3 -I THIS [--dry] [FILES...]."""
import re, sys, glob

KEYS = ("c", "n", "r", "s", "text", "when", "note")
KEY_LINE = re.compile(r"^(\s*-?\s*)(\w+):(\s|$)")
MASK = re.compile(r"\]\([^)\s]*\)|\[\[[^\]]*\]\]|https?://\S+|`[^`]*`")
MON = r"(?:Jan|Feb|Mar|Apr|May|June?|July?|Aug|Sept?|Oct|Nov|Dec)[a-z]*\.?"
NOT_BEFORE = re.compile(r"(?:L\.|No\.|Nos\.|Rep\.|Doc\.|Res\.|Pub\.|Print|Cong\.|Ex\.|Order|Docket|Case|Serial|Form|"
                        r"Chapter|Ch\.|Tape|Conversation|Citation|Item|Box|Folder|Reel|Roll|EO|NSAM|NSDM|NIE|SNIE)\s*$")
RANGE = re.compile(r"(?<![\w.\-–/#=+])(\d{1,4})-(\d{1,4})(?![\w\-–/%])")
IDS = {"oplan", "grant", "msg", "msgs", "deptel", "embtel", "cable", "telegram", "circular", "airgram", "file", "jcsm",
       "dpm", "memo", "opsum", "nsam", "sm", "cm", "series", "file:", "contract", "project", "op", "plan"}
TO_DATE = re.compile(r"(\d{4}|\d{1,2})-(?=" + MON + r" \d)")


def fix_text(t):
    held = []
    t = MASK.sub(lambda m: held.append(m.group(0)) or f"\x00{len(held) - 1}\x00", t)
    k = [0]

    def rng(m):
        if NOT_BEFORE.search(t[max(0, m.start() - 14):m.start()]):
            return m.group(0)
        a, b = m.group(1), m.group(2)
        full = a[:max(0, len(a) - len(b))] + b                 # '317-18' is 317 to 318
        if int(full) <= int(a):                                # 'JCS 1284-67', 'HE 8-1': a number, no range
            return m.group(0)
        prev = re.search(r"(\S+)\s*$", t[:m.start()])
        if prev and not re.fullmatch(r"[IVXL]+,", prev.group(1)) and (re.fullmatch(r"[A-Z][A-Z/]+[,.:]?", prev.group(1)) or prev.group(1).rstrip(",.").lower() in IDS):
            return m.group(0)                                  # 'OPLAN 37-64', 'LE/FI 11-4', 'Grant 67-580'

        k[0] += 1
        return f"{a}–{b}"
    t = RANGE.sub(rng, t)
    t, n2 = TO_DATE.subn(r"\1–", t)
    t = re.sub(r"\x00(\d+)\x00", lambda m: held[int(m.group(1))], t)
    return t, k[0] + n2


def main(files, dry=False):
    total = nf = 0
    for f in files:
        lines = open(f).read().split("\n")
        key, ch = None, 0
        for i, ln in enumerate(lines):
            m = KEY_LINE.match(ln)
            if m:
                key = m.group(2)
                if key not in KEYS:
                    continue
                head, body = ln[:m.end()], ln[m.end():]
            elif key in KEYS and ln.startswith(" "):
                head, body = "", ln
            else:
                continue
            new, k = fix_text(body)
            if k:
                lines[i] = head + new; ch += k
        if ch:
            total += ch; nf += 1
            if not dry:
                open(f, "w").write("\n".join(lines))
    print(f"{total} ranges, in {nf} files")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args or sorted(glob.glob("lists/*/*.yaml")), "--dry" in sys.argv)
