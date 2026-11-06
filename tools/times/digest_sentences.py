"""The Daily Digest's sitting hours in the calendar's notes, put in one form (notes/briefs/times.md, round 3).

    python3 -I tools/times/digest_sentences.py              a dry run: every change (id, before, after), then every
                                                            Digest sentence it could not put in the form, with why
    python3 -I tools/times/digest_sentences.py --write      applies the changes to lists/cal/*.yaml
    python3 -I tools/times/digest_sentences.py --root DIR   reads (and with --write, writes) DIR/lists/cal/*.yaml,
                                                            a copy, instead of the repository's (the volumes are
                                                            read from the repository: daybook/committees/volumes.yaml)

Rerunnable: a sentence already in the form is left as it is.

THE FORM

    The Senate sat from noon to 5:26 p.m.: [Daily Digest, D3](U1), [D21](U2).

The chamber; the hour it met; the hour it adjourned or recessed (both "to"); then the Digest's pages, each linked:
the page that gives the hour of meeting first (the standing order at the session's opening, or the order that set
the day's hour), the page that gives the rising second, one page once where they are the same. A start set by an
order or by consent, not by the standing hour, is named in parentheses after it, as the sentence named it ("by its
order of June 12", "the order of June 12" and "the hour of meeting, the order of June 12" all as "its order of June
12"; "by unanimous consent", "by the order entered" as written):

    The Senate sat from 10 a.m. (its order of June 12) to 5:03 p.m.: [Daily Digest, D281](U), [D284](U).

A sitting past midnight keeps its words ("to 12:51 a.m.", "to midnight"). Both chambers in one sentence: each in
the form, a sentence each, in the order written.

RULES

 1. What is read: a sentence of an entry's `n` (split at a full stop outside brackets and parentheses, before a
    capital, a bracket or the end, not after an abbreviation) that names the Senate or the House, the Digest, and the
    hour it met or sat. The forms the time reviewers wrote (the counts the dry run prints, by FORM below):
      sat      "The Senate sat from noon to 5:26 p.m.: [Daily Digest, D20](U)." (the form; its labels still mended)
      cr       "The Senate met at noon, the session's standing hour, and adjourned at 5:51 p.m.: Daily Digest,
               [106 Cong. Rec. D3](U), [D27](U) (1960)." (1960-61: the Record's label and the year drop)
      paren    "The House met at noon, its standing hour ([Daily Digest, D4](U)), and adjourned at 1:40 p.m.:
               [Daily Digest, D28](U)."; "The Senate met at noon (its standing order, Daily Digest, D3) and
               adjourned at T: [Daily Digest, D21](U)."; "The Senate met at noon ([Daily Digest, D498](U)) and
               adjourned at 5:12 p.m. ([Daily Digest, D505](U))."
      hours    "Hours: [Daily Digest, D7](U) (the Senate met at noon, its standing hour; adjourned at 1:49 p.m.)."
      lead     "[Daily Digest, D284](U) (the Senate met at 10 a.m. by its order of June 12, D281; recessed at
               5:03 p.m.)."
    Anything else in such a sentence (a clause the forms do not hold, a third page of the meeting, no rising hour)
    and the sentence is left as written and reported, with the reason.
 2. Pages. A page is "D" and its folio. A label "PDF p. N" is the PDF's page: it becomes its folio by the volume's
    offset (daybook/committees/volumes.yaml: folio = PDF page + offset), its link kept. An unlinked page ("Daily
    Digest, D4", "D281", "PDF p. 371") takes its link: the volume of the sentence's other linked pages (each
    agreeing with volumes.yaml), else of the entry's year, at the PDF page the offset gives; where neither settles
    it, it stays as written and is reported. A linked page whose label and link disagree (the folio less the offset
    not the link's page) is kept as written and reported.
 3. Which page is which: a page inside the clause of the hour of meeting (the parenthesis or the order after "met
    at") is the meeting's; the rest the rising's, in order; where the clause names none and the sentence two or
    more pages, the first is the meeting's (the standing order, D3 or D4 at the session's opening), the rest the
    rising's; one page, both.
 4. Nothing else in the note changes; the sentence keeps its place. The YAML is edited in place, the `n` line
    alone (single-quoted, apostrophes doubled; a plain value that the form's colon would break is quoted), so a
    file stays byte for byte as it was outside the changed values; each new line is read back with yaml and must
    give the new note.
"""

import argparse
import glob
import os
import re
import sys

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

T = r"(?:noon|midnight|\d{1,2}(?::\d{2})? [ap]\.m\.)"
MONTH = r"(?:Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)\.?"
DATE = MONTH + r" \d{1,2}"
CH = r"(?P<ch>Senate|House)"
P = r"⟦\d+⟧"                         # a page's placeholder in the skeleton
PL = P + r"(?:, " + P + r")*"                  # a run of pages
END = r"(?: \(\d{4}\))?\.$"                    # the 1960-61 form's year, then the stop
RISE = r"(?:adjourned|recessed)"

# a page as written: linked, "[Daily Digest, D3](U)", "[106 Cong. Rec. D3](U)", "[D21](U)", "[Daily Digest, PDF
# p. 74](U)", the 1960-61 "Daily Digest, " before the bracket; or unlinked, "Daily Digest, D4", "D281", "PDF p. 371"
LINKED = re.compile(r"(?:Daily Digest, )?\[(?:Daily Digest(?:, |(?=\]))|(?=[\dDP]))(?:(?P<vol>\d{3}) Cong\. Rec\. )?"
                    r"(?:D(?P<d>\d+)|PDF p\. (?P<p>\d+))?\]\((?P<url>https://[^)\s]+)\)")
UNLINKED = re.compile(r"(?<![\w\[])(?:Daily Digest, )?(?:(?P<vol>\d{3}) Cong\. Rec\. )?"
                      r"(?:D(?P<d>\d+)|PDF p\. (?P<p>\d+))\b(?!\])")

# the forms (RULES 1), over the skeleton: pages as placeholders. `q`, the clause of the hour of meeting
FORMS = [
    ("sat", re.compile(r"^The " + CH + r" sat from (?P<t1>" + T + r")(?: \((?P<q>[^()]*)\)|, (?P<q3>[^()]*(?: \(" + P
                       + r"\))?),)? to (?P<t2>" + T + r"(?: " + DATE + r")?): (?P<pl>" + PL + r")(?: \(the hour of meeting, (?P<q2>the order "
                       r"of " + DATE + r"): (?P<qp>" + P + r")\))?" + END)),
    ("cr", re.compile(r"^The " + CH + r" met at (?P<t1>" + T + r")(?:, (?P<q>[^,]*),)? and " + RISE + r" at (?P<t2>"
                      + T + r"): (?P<pl>" + PL + r")" + END)),
    ("paren", re.compile(r"^The " + CH + r" met at (?P<t1>" + T + r")(?: \((?P<q>[^()]*)\)|, (?P<q3>[^,()]*(?: \("
                         + P + r"\))?),)? and (?:" + RISE + r" at (?P<t2>" + T + r")|sat through the night, recessing "
                         r"at (?P<t2n>" + T + " " + DATE + r"))(?:: (?P<pl>" + PL + r")| \((?P<pl2>" + PL + r")\))"
                         + END)),
    ("hours", re.compile(r"^Hours: (?P<pl>" + PL + r") \(the " + CH + r" met at (?P<t1>" + T + r")(?:,? (?P<q>[^;]*))?; "
                         + RISE + r" at (?P<t2>" + T + r")\)" + END)),
    ("lead", re.compile(r"^(?P<pl>" + PL + r") \(the " + CH + r" met at (?P<t1>" + T + r")(?:,? (?P<q>[^;]*))?; "
                        + RISE + r" at (?P<t2>" + T + r")\)" + END)),
]
# where a sentence opens: a time reviewer's hours sentence begins so (RULES 1)
OPENS = re.compile(r"The (?:Senate|House) (?:sat|met) |Hours: \[|\[Daily Digest[^\]]*\]\([^)]*\) \(the (?:Senate|House) met ")

STANDING = re.compile(r"^(?:its|the session's|the) standing (?:hour|order|order's hour)(?:, (?:Daily Digest, )?"
                      + P + r"| \(" + P + r"\))?$|^(?:Daily Digest, )?" + P + r"$")
ORDER = re.compile(r"^(?:by its|the|its) order of (?P<date>" + DATE + r")(?P<words> [^()\u27e6]*?)?(?:,? \(?(?:Daily "
                   r"Digest, )?(?P<p>" + P + r")\)?)?$")
CONSENT = re.compile(r"^(?P<w>by unanimous consent|by the order entered)$")

ABBR = {"a.m", "p.m", "Cong", "Rec", "p", "pp", "U.S", "D.C", "Jr", "Sr", "St", "No", "Nos", "vol", "vols", "Mr",
        "Mrs", "Dr", "Gen", "Sen", "Rep", "Jan", "Feb", "Mar", "Apr", "Aug", "Sept", "Oct", "Nov", "Dec", "ed",
        "eds", "n", "nn", "ff", "cf", "v", "Pub", "Stat", "Doc", "Res", "Con", "H", "S", "R", "J", "Co", "Inc"}


def volumes(repo):
    """{year: (url, [(from, to, offset)])} from daybook/committees/volumes.yaml."""
    with open(os.path.join(repo, "daybook", "committees", "volumes.yaml"), encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return {v["year"]: (v["url"], [(r["from"], r["to"], r["offset"]) for r in v["runs"]]) for v in data["volumes"]}


VOLS = volumes(REPO)
BY_URL = {u: y for y, (u, _) in VOLS.items()}


def offset_at(year, page=None, folio=None):
    """The offset (folio = page + offset) of the run holding a PDF page, or a folio."""
    for a, b, off in VOLS[year][1]:
        if page is not None and a <= page <= b:
            return off
        if folio is not None and a <= folio - off <= b:
            return off
    return None


def split_sentences(text):
    """Spans (start, end) of the note's sentences (RULES 1)."""
    out, depth, start, i = [], 0, 0, 0
    while i < len(text):
        ch = text[i]
        if ch in "[(":
            depth += 1
        elif ch in "])":
            depth = max(0, depth - 1)
        elif ch == "." and depth == 0:
            nxt = text[i + 1:i + 3]
            word = re.search(r"([\w.]*)$", text[start:i]).group(1)
            at_end = i + 1 == len(text)
            if at_end or (nxt[:1] == " " and nxt[1:2] and (nxt[1].isupper() or nxt[1] in "[*\"'")
                          and word not in ABBR):
                out.append((start, i + 1))
                start = i + 2
        i += 1
    if start < len(text):
        out.append((start, len(text)))
    return out


def is_candidate(s):
    return ("Digest" in s and re.search(r"\b(Senate|House)\b", s)
            and re.search(r"\b(met at|sat from|Hours:)", s))


class Fail(Exception):
    pass


def pages(s, year):
    """The skeleton (pages as placeholders) and the pages: dicts of folio, url, how written, notes."""
    refs, notes = [], []

    def linked(m):
        url = m.group("url")
        base, _, frag = url.partition("#page=")
        vy = BY_URL.get(base)
        if vy is None or not frag.isdigit():
            raise Fail("a Digest link to no volume read: " + url)
        pg = int(frag)
        off = offset_at(vy, page=pg)
        if m.group("d"):
            folio = int(m.group("d"))
            if off is None or folio - off != pg:
                raise Fail("label and link disagree: D%s at PDF page %d" % (folio, pg))
        elif m.group("p") is None:
            if off is None:
                raise Fail("no offset for page %d" % pg)
            folio = pg + off
            notes.append("[Daily Digest] at page %d is D%d" % (pg, folio))
        else:
            if int(m.group("p")) != pg:
                raise Fail("label and link disagree: PDF p. %s at page %d" % (m.group("p"), pg))
            if off is None:
                raise Fail("no offset for PDF p. %d" % pg)
            folio = pg + off
            notes.append("PDF p. %d is D%d" % (pg, folio))
        refs.append({"folio": folio, "url": url, "year": vy})
        return "⟦%d⟧" % (len(refs) - 1)

    s = LINKED.sub(linked, s)
    linked_years = {r["year"] for r in refs}

    def unlinked(m):
        vy = None
        if len(linked_years) == 1:
            vy = next(iter(linked_years))
        elif not linked_years and year in VOLS:
            vy = year
        if vy is None:
            refs.append({"folio": None, "text": m.group(0), "unsettled": True})
            notes.append("unlinked page not settled: " + m.group(0))
            return "⟦%d⟧" % (len(refs) - 1)
        if m.group("d"):
            folio = int(m.group("d"))
            off = offset_at(vy, folio=folio)
            if off is None:
                raise Fail("no offset for " + m.group(0))
            pg = folio - off
        else:
            pg = int(m.group("p"))
            off = offset_at(vy, page=pg)
            if off is None:
                raise Fail("no offset for " + m.group(0))
            folio = pg + off
        url = VOLS[vy][0] + "#page=%d" % pg
        notes.append("linked %s as D%d (page %d)" % (m.group(0), folio, pg))
        refs.append({"folio": folio, "url": url, "year": vy, "was": m.group(0)})
        return "⟦%d⟧" % (len(refs) - 1)

    s = UNLINKED.sub(unlinked, s)
    return s, refs, notes


def ids(txt):
    return [int(x) for x in re.findall(r"⟦(\d+)⟧", txt or "")]


def qualifier(q):
    """(the order's words or None, the meeting's pages) of the clause of the hour of meeting."""
    if q is None or q == "":
        return None, []
    q = q.strip()
    if STANDING.match(q):
        return None, ids(q)
    m = ORDER.match(q)
    if m:
        return "its order of " + m.group("date") + (m.group("words") or ""), ids(m.group("p"))
    m = CONSENT.match(q)
    if m:
        return m.group("w"), []
    raise Fail("the hour of meeting's clause not read: " + q)


def link(i, ref, first):
    if ref.get("unsettled"):
        raise Fail("unlinked page not settled: " + ref["text"])
    lab = ("Daily Digest, D%d" if first else "D%d") % ref["folio"]
    return "[%s](%s)" % (lab, ref["url"])


def render(ch, t1, order, t2, meet, rise, refs):
    seq, seen = [], set()
    for i in meet + rise:
        f = refs[i]["folio"]
        if f in seen:
            continue
        seen.add(f)
        seq.append(i)
    pl = ", ".join(link(i, refs[i], k == 0) for k, i in enumerate(seq))
    return "The %s sat from %s%s to %s: %s." % (ch, t1, " (%s)" % order if order else "", t2, pl)


def parse(s, year):
    """(form, the sentence in the form, notes) or raises Fail."""
    sk, refs, notes = pages(s, year)
    if len(set(re.findall(r"\b(Senate|House)\b", sk))) > 1:
        # both chambers, a clause each: "The Senate met ... (P); the House met ... (P)."
        both = re.match(r"^(?P<a>The (?:Senate|House) [^;]*); the (?P<b>(?:Senate|House) [^;]*)$", sk)
        if not both:
            raise Fail("both chambers in one sentence, not split")
        fa, oa = one(both.group("a") + ".", refs)
        fb, ob = one("The " + both.group("b"), refs)
        return fa + "+" + fb, oa + " " + ob, notes
    form, out = one(sk, refs)
    return form, out, notes


def one(sk, refs):
    for name, rx in FORMS:
        m = rx.match(sk)
        if not m:
            continue
        g = m.groupdict()
        order, meet = qualifier(g.get("q") if g.get("q") is not None else g.get("q3"))
        if g.get("q2"):
            if order or meet:
                raise Fail("two orders of the hour of meeting")
            order, meet = "its order of " + g["q2"][len("the order of "):], ids(g["qp"])
        pl = ids(g.get("pl") or g.get("pl2"))
        if len(meet) > 1:
            raise Fail("more than one page for the hour of meeting")
        if meet:
            rise = pl
        elif len(pl) >= 2:
            meet, rise = pl[:1], pl[1:]
        else:
            rise = pl
        if not rise:
            raise Fail("no page for the rising")
        return name, render(g["ch"], g["t1"], order, g.get("t2") or g.get("t2n"), meet, rise, refs)
    if re.search(r"\bsine die\b", sk):
        raise Fail("adjourned sine die: the form has no place for it")
    if not re.search(r"\b(adjourned|recessed|recessing)\b| to " + T, sk):
        raise Fail("no hour of rising")
    raise Fail("a form not read")


def decode(raw):
    """The note's text from its YAML line value, and how it was written."""
    if raw.startswith("'") and raw.endswith("'") and len(raw) >= 2:
        return raw[1:-1].replace("''", "'"), "single"
    if raw[:1] in "\"|>":
        return None, "other"
    return raw, "plain"


def encode(text, style):
    if style == "plain" and not re.search(r": | #|^[\[\]{}*&!|>'\"%@`,?:-]|^\s|\s$", text):
        return text
    return "'" + text.replace("'", "''") + "'"


def run(root, write):
    files = sorted(glob.glob(os.path.join(root, "lists", "cal", "*.yaml")))
    changes, fails, forms, linked_n, pdf_n = [], [], {}, 0, 0
    for path in files:
        with open(path, encoding="utf-8", newline="") as f:
            lines = f.read().split("\n")
        eid, dirty = None, False
        for i, line in enumerate(lines):
            m = re.match(r"^  - id: (\S+)", line)
            if m:
                eid = m.group(1)
                continue
            m = re.match(r"^(    n: )(.*)$", line)
            if not m:
                continue
            text, style = decode(m.group(2))
            if text is None:
                if "Digest" in m.group(2):
                    fails.append((eid, m.group(2)[:200], "a note not single-quoted or plain"))
                continue
            ym = re.match(r"cal\.(\d{4})", eid or "")
            year = int(ym.group(1)) if ym else None
            new, pos = [], 0
            for a, b in split_sentences(text):
                s = text[a:b]
                if not is_candidate(s):
                    continue
                o = [x.start() for x in OPENS.finditer(s) if x.start() >= 2 and s[x.start() - 2:x.start()] == ". "]
                if not OPENS.match(s) and o:
                    a, s = a + o[0], s[o[0]:]       # a sentence the split ran on into: "86th Cong. The Senate ..."
                try:
                    form, out, notes = parse(s, year)
                except Fail as e:
                    fails.append((eid, s, str(e)))
                    continue
                forms[form] = forms.get(form, 0) + 1
                if out != s:
                    linked_n += sum(n.startswith("linked") for n in notes)
                    pdf_n += sum(n.startswith("PDF p.") for n in notes)
                    changes.append((eid, s, out, notes, os.path.relpath(path, root), i + 1, form))
                    new.append(text[pos:a] + out)
                    pos = b
            if not new:
                continue
            ntext = "".join(new) + text[pos:]
            nline = m.group(1) + encode(ntext, style)
            back = yaml.safe_load(nline.strip())
            if back != {"n": ntext}:
                raise SystemExit("%s:%d: the new line does not read back as the note" % (path, i + 1))
            lines[i] = nline
            dirty = True
        if dirty and write:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write("\n".join(lines))
    return changes, fails, forms, linked_n, pdf_n


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true", help="apply the changes")
    ap.add_argument("--root", default=REPO, help="the tree whose lists/cal/*.yaml to read (default: the repository)")
    ap.add_argument("--quiet", action="store_true", help="counts and failures only")
    a = ap.parse_args()
    changes, fails, forms, linked_n, pdf_n = run(a.root, a.write)
    if not a.quiet:
        for eid, before, after, notes, path, ln, form in changes:
            print("%s  (%s:%d, %s)" % (eid, path, ln, form))
            print("  - " + before)
            print("  + " + after)
            for n in notes:
                print("    . " + n)
    print("\nNot put in the form (%d):" % len(fails))
    for eid, s, why in fails:
        print("%s: %s\n    %s" % (eid, why, s))
    print("\nSentences read by form: " + ", ".join("%s %d" % kv for kv in sorted(forms.items())))
    print("Changed: %d (%s); pages linked %d; PDF labels made folios %d; not read %d"
          % (len(changes), "written" if a.write else "dry run", linked_n, pdf_n, len(fails)))


if __name__ == "__main__":
    sys.exit(main())
