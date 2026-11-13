"""Endnotes: a book's notes found for a page (the owner, Nov. 12, 2026: "These guys gotta read the footnotes... (Do
the PDFs make that awkward?)"; "Please do re: the notes tool pilot").

A reader citing page 84 of a book with endnotes needs the notes that page's sentences carry: they date what the page
dates loosely ("in July", "shortly after"). The notes sit at the back, keyed by chapter and number, and the text
layer often loses the superscripts. This finds them from the notes section's own structure.

STYLE
1. `index PDF --out DIR` reads the PDF's text layer (pdftotext -layout) once and writes DIR/<stem>.notes.json: each
   PDF page's printed folio (from the running head or foot, gaps filled by the nearest known offset), the notes
   section's pages, and every note (chapter, number, text, its notes page and that page's folio), with the text page
   each note most likely belongs to. The index holds the book's text: keep it in your scratch directory and delete it
   with the PDF when done (the reader's brief, R54).
2. Three forms of notes, found in this order:
   a. "Notes to Pages 77–89" running heads (most university and trade presses): the notes on a notes page belong to
      text pages within its range; each note's page is interpolated along the range (`est`).
   b. Page-keyed notes, no numbers in the text ("84 Bigart's survey: ..."): the leading number is the text page.
   c. Chapter-numbered notes only: the notes of chapter k (numbering restarts at 1) are listed by chapter; a page's
      notes are those of its chapter, interpolated along the chapter's pages where the chapter openings are found.
3. `page INDEX FOLIO [--margin 1]` prints the notes most likely carried by printed page FOLIO (the estimated pages
   FOLIO − margin to FOLIO + margin), each with its chapter and number and its own notes page, so it can be cited
   ("422 n.9"). Estimates are estimates: read the note against the page's sentence (and the page image's
   superscript) before citing it.
4. `note INDEX CHAPTER NUMBER` prints one note; `chapters INDEX` the chapters found, their note counts and pages;
   `pdf INDEX FOLIO` the PDF page(s) of a printed page, from the running heads read (`heads`), not interpolated, so a
   plate section's change of offset does not mislead (the pilot, Nov. 13: folio 84 is PDF 106, not 118).
5. A form the program cannot read (no heads, no numbers it can follow, an OCR text layer too broken): it says so;
   read the notes section by hand (`pdftotext -f N -l M -layout`).
"""
import argparse
import json
import os
import re
import subprocess
import sys

HEAD_RANGE = re.compile(r"Notes\s+to\s+Pages?\s+(\d{1,4})\s*[-–—]\s*(\d{1,4})", re.I)
HEAD_ONE = re.compile(r"Notes\s+to\s+Page\s+(\d{1,4})\b", re.I)
NOTE_LINE = re.compile(r"^\s{0,8}(\d{1,3})[.)]?\s+(\S.*)$")
FOLIO_L = re.compile(r"^\s*(\d{1,4})\s{2,}\S")
FOLIO_R = re.compile(r"\S\s{2,}(\d{1,4})\s*$")
FOLIO_ONLY = re.compile(r"^\s*(\d{1,4})\s*$")
NOTES_TITLE = re.compile(r"^\s*(Notes|NOTES|Endnotes|Source Notes|Notes and Sources)\s*$")
BACK_TITLE = re.compile(r"^\s*(Bibliography|BIBLIOGRAPHY|Index|INDEX|Selected Bibliography|Acknowledg(e)?ments|"
                        r"Sources|A Note on Sources|Bibliographical Essay)\s*$")


def expand(a, b):
    """'102-7' → (102, 107); '107-12' → (107, 112)."""
    a, b = int(a), b
    if len(b) < len(str(a)):
        b = int(str(a)[: len(str(a)) - len(b)] + b)
        if b < a:
            b += 10 ** len(str(b))
    return a, int(b)


def pages_of(pdf):
    out = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
    pages = out.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    return pages


def lines(p):
    return [l for l in p.splitlines() if l.strip()]


def folios(pages):
    """{pdf page: printed folio}, from the running head or foot; gaps by the nearest known offset."""
    known = {}
    for i, p in enumerate(pages, 1):
        ls = lines(p)
        cand = []
        for l in ls[:1] + ls[-1:]:
            for rx in (FOLIO_L, FOLIO_R, FOLIO_ONLY):
                m = rx.search(l)
                if m:
                    cand.append(int(m.group(1)))
                    break
        for f in cand:
            if 0 < f < 2000 and 0 <= i - f < 200:
                known[i] = f
                break
    # keep only folios agreeing with a neighbour's offset (a stray number is no folio)
    offs = {i: i - f for i, f in known.items()}
    good = {}
    ks = sorted(offs)
    for n, i in enumerate(ks):
        near = [offs[j] for j in ks[max(0, n - 3): n + 4] if j != i]
        if near.count(offs[i]) >= 1:
            good[i] = known[i]
    folios.heads = dict(good)
    out = {}
    gk = sorted(good)
    for i in range(1, len(pages) + 1):
        if i in good:
            out[i] = good[i]
            continue
        prev = max((j for j in gk if j < i), default=None)
        nxt = min((j for j in gk if j > i), default=None)
        ref = prev if prev is not None else nxt
        if ref is None:
            continue
        if prev is not None and nxt is not None and (prev - good[prev]) != (nxt - good[nxt]):
            ref = prev if i - prev <= nxt - i else nxt
        out[i] = i - (ref - good[ref])
    return out


def notes_section(pages):
    """(first, last) PDF pages of the notes, or None."""
    heads = [i for i, p in enumerate(pages, 1) if any(HEAD_RANGE.search(l) or HEAD_ONE.search(l) for l in lines(p)[:2])]
    titles = [i for i, p in enumerate(pages, 1) if any(NOTES_TITLE.match(l) for l in lines(p)[:3])]
    start = None
    if heads:
        start = min(heads)
        before = [t for t in titles if t <= start and start - t <= 4]
        if before:
            start = min(before)
    elif titles:
        start = max(t for t in titles if t > len(pages) * 0.5) if any(t > len(pages) * 0.5 for t in titles) else None
    if start is None:
        return None
    end = len(pages)
    for i in range(start + 1, len(pages) + 1):
        ls = lines(pages[i - 1])
        if any(BACK_TITLE.match(l) for l in ls[:3]) and not any(HEAD_RANGE.search(l) for l in ls[:2]):
            end = i - 1
            break
    return start, end


def parse_notes(pages, first, last):
    """[note dicts] in order: pdf, head range, chapter, number, text.

    Two passes: the candidate lines (a number at the margin), then the run of numbers kept: the next number, a near
    one (OCR drops a digit or a note), or 1 opening a chapter only where a 2 or 3 follows soon (an OCR "21." read
    "1." does not open a chapter)."""
    rows = []          # (pdf, range, kind, num, text): kind "cand" or "line" or "head"
    for i in range(first, last + 1):
        ls = lines(pages[i - 1])
        rng = None
        for l in ls[:2]:
            m = HEAD_RANGE.search(l)
            if m:
                rng = expand(m.group(1), m.group(2))
                break
            m = HEAD_ONE.search(l)
            if m:
                rng = (int(m.group(1)), int(m.group(1)))
                break
        skip = 1 if (ls and (rng or NOTES_TITLE.match(ls[0]) or FOLIO_L.search(ls[0]) or FOLIO_R.search(ls[0])
                             or FOLIO_ONLY.match(ls[0]))) else 0
        for l in ls[skip:]:
            m = NOTE_LINE.match(l)
            if m:
                rows.append((i, rng, "cand", int(m.group(1)), m.group(2).strip()))
            elif re.match(r"^\s{12,}\S", l) and len(l.strip()) < 70:
                rows.append((i, rng, "head", None, l.strip()))
            else:
                rows.append((i, rng, "line", None, l.strip()))
    cands = [k for k, r in enumerate(rows) if r[2] == "cand"]
    notes, chapter, cur, heading = [], 0, None, ""
    keep = set()
    last = None
    for pos, k in enumerate(cands):
        num = rows[k][3]
        ahead = [rows[j][3] for j in cands[pos + 1: pos + 5]]
        if num == 1 and (2 in ahead or 3 in ahead):
            keep.add(k); last = 1; continue
        if last is not None and 0 < num - last <= 4:
            keep.add(k); last = num; continue
        if last is None and (2 in ahead or num + 1 in ahead):
            keep.add(k); last = num; continue
    for k, (pdf, rng, kind, num, text) in enumerate(rows):
        if k in keep:
            if cur is None or num <= cur["n"]:
                chapter += 1
                ch_heading = heading
            else:
                ch_heading = cur["heading"]
            cur = {"pdf": pdf, "range": rng, "ch": max(chapter, 1), "n": num, "text": text, "heading": ch_heading}
            notes.append(cur)
            heading = ""
        elif kind == "head" or (cur is None and kind == "line"):
            heading = text
        elif cur is not None:
            cur["text"] += " " + (f"{num} {text}" if kind == "cand" else text)
    return notes


def page_keyed(notes):
    """True where the leading numbers are text pages, not note numbers (2b)."""
    if len(notes) < 20:
        return False
    nums = [x["n"] for x in notes]
    resets = sum(1 for a, b in zip(nums, nums[1:]) if b < a)
    return max(nums) > 60 and resets <= len(nums) * 0.03


def estimate(notes, fol):
    """Each note's likely text page ('est')."""
    by_pdf = {}
    for x in notes:
        by_pdf.setdefault(x["pdf"], []).append(x)
    for pdf, xs in by_pdf.items():
        rng = xs[0]["range"]
        for k, x in enumerate(xs):
            x["folio"] = fol.get(pdf)
            if rng:
                a, b = rng
                x["est"] = round(a + (b - a) * (k / max(1, len(xs) - 1)))
            else:
                x["est"] = None
    # notes pages with no head (the section's first page): take the next headed page's start
    for n, x in enumerate(notes):
        if x["est"] is None:
            nxt = next((y for y in notes[n + 1:] if y["range"]), None)
            if nxt:
                x["est"] = nxt["range"][0]


def build(pdf):
    pages = pages_of(pdf)
    fol = folios(pages)
    sec = notes_section(pages)
    idx = {"pdf": os.path.basename(pdf), "pages": len(pages), "folios": fol, "heads": getattr(folios, "heads", {}),
           "section": sec, "form": None, "notes": []}
    if not sec:
        idx["problem"] = "no notes section found (STYLE 5)"
        return idx
    notes = parse_notes(pages, *sec)
    if any(x["range"] for x in notes):
        idx["form"] = "heads"
        estimate(notes, fol)
    elif page_keyed(notes):
        idx["form"] = "page-keyed"
        for x in notes:
            x["est"], x["folio"] = x["n"], fol.get(x["pdf"])
    else:
        idx["form"] = "chapters"
        for x in notes:
            x["est"], x["folio"] = None, fol.get(x["pdf"])
    idx["notes"] = notes
    if not notes:
        idx["problem"] = "notes section found but no numbered notes read (STYLE 5)"
    return idx


def show(x, width=None):
    head = f"ch. {x['ch']}" + (f" ({x['heading'][:40]})" if x.get("heading") else "")
    where = f"{x['folio']} n.{x['n']}" if x.get("folio") else f"pdf {x['pdf']} n.{x['n']}"
    est = f", text p. ~{x['est']}" if x.get("est") else ""
    t = x["text"] if not width else x["text"][:width]
    return f"[{where}; {head}{est}] {t}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("index")
    a.add_argument("pdf")
    a.add_argument("--out", required=True)
    b = sub.add_parser("page")
    b.add_argument("index")
    b.add_argument("folio", type=int)
    b.add_argument("--margin", type=int, default=1)
    c = sub.add_parser("note")
    c.add_argument("index")
    c.add_argument("chapter", type=int)
    c.add_argument("number", type=int)
    d = sub.add_parser("chapters")
    d.add_argument("index")
    e = sub.add_parser("pdf")
    e.add_argument("index")
    e.add_argument("folio", type=int)
    args = ap.parse_args(argv)
    if args.cmd == "index":
        idx = build(args.pdf)
        os.makedirs(args.out, exist_ok=True)
        path = os.path.join(args.out, os.path.splitext(os.path.basename(args.pdf))[0] + ".notes.json")
        json.dump(idx, open(path, "w"))
        n = idx["notes"]
        print(f"{path}: {idx['pages']} pages; notes pdf {idx['section']}; form {idx['form']}; {len(n)} notes in "
              f"{len(set(x['ch'] for x in n))} chapters" + (f"; {idx['problem']}" if idx.get("problem") else ""))
        return 0
    idx = json.load(open(args.index))
    notes = idx["notes"]
    if args.cmd == "chapters":
        for ch in sorted(set(x["ch"] for x in notes)):
            xs = [x for x in notes if x["ch"] == ch]
            ests = [x["est"] for x in xs if x.get("est")]
            print(f"ch. {ch}: {len(xs)} notes, notes pp. {xs[0].get('folio')}–{xs[-1].get('folio')}"
                  + (f", text pp. ~{min(ests)}–{max(ests)}" if ests else "")
                  + (f"  {xs[0]['heading'][:50]}" if xs[0].get("heading") else ""))
        return 0
    if args.cmd == "pdf":
        heads = {int(k): v for k, v in (idx.get("heads") or {}).items()}
        hit = sorted(k for k, v in heads.items() if v == args.folio)
        if not hit:                     # between read heads: the nearest read head's offset on either side
            below = max((k for k, v in heads.items() if v < args.folio), default=None, key=lambda k: heads[k])
            above = min((k for k, v in heads.items() if v > args.folio), default=None, key=lambda k: heads[k])
            cands = sorted({k + (args.folio - heads[k]) for k in (below, above) if k is not None})
            print(f"folio {args.folio}: no running head read; PDF {' or '.join(map(str, cands))} by the nearest heads "
                  "(check the image)")
            return 1
        print(f"folio {args.folio}: PDF {', '.join(map(str, hit))}")
        return 0
    if args.cmd == "note":
        hit = [x for x in notes if x["ch"] == args.chapter and x["n"] == args.number]
        for x in hit:
            print(show(x))
        return 0 if hit else 1
    if idx["form"] == "chapters":
        print("Notes are numbered by chapter, with no page heads: read the page image's superscripts, then "
              "`note INDEX CHAPTER NUMBER` (`chapters INDEX` lists them).", file=sys.stderr)
        return 2
    lo, hi = args.folio - args.margin, args.folio + args.margin
    hit = [x for x in notes if x.get("est") is not None and lo <= x["est"] <= hi]
    for x in hit:
        print(show(x))
    if not hit:
        print(f"no note estimated for pp. {lo}–{hi}", file=sys.stderr)
    return 0 if hit else 1


if __name__ == "__main__":
    sys.exit(main())
