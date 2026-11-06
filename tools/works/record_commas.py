"""Five-digit Record pages with a comma (the owner's ruling, Nov. 5, 2026, on the docket: "Comma: '15,678'"):
'106 Cong. Rec. 13819' -> '106 Cong. Rec. 13,819'; a run of pages after it too ('12522-29, 12535' -> '12,522-29,
12,535'). Every list's files; the tables format theirs at build (pages(), bills.py, appropriations.py). A daily
edition's lettered page (H1234, D322) is left. Run: python3 -I THIS [--dry]."""
import re, sys, glob

RUN = re.compile(r"(\d{2,3} Cong\. Rec\. )((?:\d[\d,]*(?:[–-]\d+)?)(?:, (?:at )?\d[\d,]*(?:[–-]\d+)?)*)")


def comma(n):
    return f"{int(n):,}" if len(n) >= 5 else n


def pages(run):
    """'13819–20, 13825' -> '13,819–20, 13,825' (a page's figure; the range's second number as written)."""
    return re.sub(r"(?<![\d–-])\d{5,}(?!\d)", lambda m: comma(m.group(0)), run)


def main(dry):
    n = nf = 0
    for f in sorted(glob.glob("lists/*/*.yaml")):
        t = open(f).read()
        new = RUN.sub(lambda m: m.group(1) + pages(m.group(2).replace(",", "") if False else m.group(2)), t)
        k = sum(1 for a, b in zip(RUN.finditer(t), RUN.finditer(new)) if a.group(0) != b.group(0))
        if new != t:
            n += k; nf += 1
            if not dry:
                open(f, "w").write(new)
    print(f"{n} cites, in {nf} files")


if __name__ == "__main__":
    main("--dry" in sys.argv)
