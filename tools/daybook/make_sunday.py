"""Write daybook/sunday.yaml: the guests of the Sunday interview programs: Meet the Press, 1945–80.

    python3 tools/daybook/make_sunday.py        (needs pdftotext; the network for the listings, else they are skipped)

Meet the Press (NBC):
  - the record: the Library of Congress's Prints and Photographs Division, "Visual Materials from the Lawrence E. Spivak
    Papers" (pp020019), its inventory of photographs from Meet the Press television programs (LOT 13025), arranged by
    show date, each with its guests as the Library writes them ("Halleck, Charles A."): the radio programs, 1945–50,
    and the television programs, 1947–80. The finding aid's pages (pp. 1–136, as produced Aug. 23, 2026) are kept in
    sources/loc/. A show of which no photograph survives is not in it. Spivak's Keep Posted (1951–53) and The Big
    Issue (1953), in the same aid, write their guests otherwise (running order, with titles) and are not taken.
  - the listings: the Classic TV Archive's episode guides (ctva.biz), compiled from the TV listings, 1947–Aug. 25,
    1963. They fill a Sunday the inventory lacks (LISTED), and where they name another person than the inventory, the
    row says so (`check`). Their misspellings (Sorenson, Norrstad) are not disagreements.
Face the Nation (CBS), Nov. 1959–1970: the index volume of *Face the Nation: The Collected Transcripts from the CBS
  Radio and Television Broadcasts* (Holt Information Systems, 1972), its annotated chronological index, each program
  numbered within its year, with its guests (in capitals, a title before and an office after), the date, and a line of
  topics. Taken: the date and the guests' names, and an office the owner asked for (FTN_ROLES: Percy's, 1960, with
  the page). Not taken: the topics and the other offices, CBS's text. The copy read was
  the owner's and is not kept in the repo: run with --ftn PATH (the index's pages as PDF or as pdftotext's text); run
  without it, the rows already written are kept.
Issues and Answers (ABC): not yet; no list of it has been found.

STYLE (rendered by tools/bib/daybook.py and tools/bib/lives.py):
 1. One row a program: date, show, network, guests (as the Library writes them, one a person; the listings' guest put
    in the same form where the listings alone give the program), network ('NBC'; 'radio' for the radio programs),
    src ('LOC' or 'listings'), lot (the inventory's
    call number), note (the Library's heading for a group: "Governors' Conference"), check (where the listings name
    another person: "Listings: Orville L. Freeman. Check.").
 2. A program on another day than Sunday (Jan. 5, 1962, a Friday) is kept, on its day.
"""
import argparse
import datetime
import html
import os
import re
import subprocess
import sys
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PDFS = [os.path.join(ROOT, "sources", "loc", f"spivak-visual-pp020019-{p}.pdf")
        for p in ("front", "pp7-49", "pp50-74", "pp75-136")]
OUT = os.path.join(ROOT, "daybook", "sunday.yaml")
CTVA = ["https://ctva.biz/US/TalkShow/MeetThePress_(1947-53)_M.Rountree.htm",
        "https://ctva.biz/US/TalkShow/MeetThePress_(1953-65)_NedBrooks.htm"]
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
# the listings' guest, put as the Library writes names, where the listings alone give the program
LISTED = {"1962-05-27": ["Annis, Edward R."]}
# misreadings of the finding aid's text
FIX = {"Mark 0.": "Mark O.", "Bums, James MacGregor": "Burns, James MacGregor", "GronousJci John A.": "Gronouski, John A.",
       "Meredith James H.": "Meredith, James H.", "Cavanagh, Jerome, P.": "Cavanagh, Jerome P."}
# a guest the Library writes by title, put as Part III writes the person (a name in its own order has no comma)
AS_SERIES = {"Nhu, Mme. Ngo Dinh": "Trần Lệ Xuân",
             # as his English-language book styles him: Inside a Soviet Embassy (1962)
             "Kaznacheev, Alexander": "Kaznacheev, Aleksandr"}
# a program whose listings' spelling is settled, so no Check: {date: why}
SETTLED = {"1960-05-22": "the listings' Kaznacheyev is Kaznacheev"}


def inventory():
    """[(date, medium, entry)] from the inventory of LOT 13025: its radio programs, then its television programs; the
    sections after it (the autographed photographs, Keep Posted, The Big Issue) left out."""
    t = "\n".join(subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True, check=True).stdout
                  for p in PDFS)
    t = re.sub(r"\n\s*- Page \d+ -\s*\n", "\n", t)
    t = re.sub(r"\n\s*Visual Materials from the Lawrence E\. Spivak Papers\s*\n", "\n", t)
    end = t.find("Autographed photographs from Meet the Press radio and television programs, 19")
    t = t[:end] if end > 0 else t
    tv_at = t.find("Television programs, 19")
    out = []
    pat = rf"((?:{MONTHS}) \d{{1,2}}, \d{{4}})\s*\n(.*?)(?=\n\s*(?:Box \d+\s+)?(?:{MONTHS}) \d{{1,2}}, \d{{4}}\s*\n|\Z)"
    for m in re.finditer(pat, t, re.S):
        d = datetime.datetime.strptime(m.group(1), "%B %d, %Y").date().isoformat()
        body = m.group(2)
        lot = re.search(r"LOT (13025-\w+)", body)
        g = re.search(r"Guests?:\s*(.*?)(?=\n\s*(?:Related Materials|Separated Materials|Physical Description|Scope|"
                      r"Identifier)|\Z)", body, re.S)
        if not g:
            continue
        text = re.sub(r"\s+", " ", re.sub(r"\bBox \d+\b", "", g.group(1))).strip()
        for a, b in FIX.items():
            text = text.replace(a, b)
        guests, note = split(text)
        guests = [AS_SERIES.get(x, x) for x in guests]
        medium = "radio" if 0 <= m.start() < tv_at else "television"
        out.append((d, medium, {"guests": guests, "note": note, "lot": lot.group(1) if lot else None}))
    return out


RANKS = (r"(?:Viscountess|Viscount|Baroness|Baron|Lady|Lord|Sir|Dame|Duke|Prince|Princess|King|Queen|Archbishop|Mme\.|"
         r"Mrs\.|Dr\.|Rev\.|Gen\.|(?:King|Queen|Shah|Prince|Archbishop|Emperor|Sultan) of .+)")


def split(text):
    """The Library's guests: 'Humphrey, Hubert H., and Morton, Thruston B.' -> (['Humphrey, Hubert H.', 'Morton,
    Thruston B.'], None); "Governors' Conference: Connally, John B., ..., and Smylie, Robert" -> ([...], "Governors'
    Conference"). Each name is 'Surname, Given', a suffix after it kept ('King, Martin Luther, Jr.'); a rank or a
    qualifier after it dropped ('Astor, Nancy Witcher Langhorne Astor, Viscountess'; 'Philip, Prince, consort of
    Elizabeth II, ...'), and so is a form in parentheses; a wife written by her husband's name ('Chiang, Kai-Shek,
    Mme.') is put as 'Madame Chiang Kai-Shek', which names no one else. Semicolons part the persons where the Library
    uses them."""
    note = None
    m = re.match(r"^([^,;]+?):\s+(.*)$", text)
    if m:
        note, text = m.group(1).strip(), m.group(2)
    text = re.sub(r"\s*\([^)]*\)", "", text)
    if ";" in text:
        parts = [p for p in re.split(r";\s*(?:and\s+)?", text) if p.strip()]
    else:
        parts = [text]
    names = []
    for part in parts:
        toks = [x.strip() for x in re.split(r",\s*(?:and\s+)?|\s+and\s+(?=[A-Z][\w'’.\- ]*,)", part) if x.strip()]
        toks = [re.sub(r"^and\s+", "", x) for x in toks]
        i = 0
        while i < len(toks):
            if i + 1 < len(toks) and not re.fullmatch(RANKS, toks[i + 1]):
                sur, given = toks[i], toks[i + 1]
                i += 2
            else:
                sur, given = toks[i], None
                i += 1
            suffix, wife = None, False
            while i < len(toks) and (re.fullmatch(r"Jr\.|Sr\.|II|III|IV", toks[i]) or re.fullmatch(RANKS, toks[i])
                                     or toks[i][:1].islower() or re.match(r"^(?:Queen|King) of\b", toks[i])):
                if re.fullmatch(r"Jr\.|Sr\.|II|III|IV", toks[i]):
                    suffix = toks[i]
                elif toks[i] == "Mme.":
                    wife = True
                i += 1
            if wife:
                names.append(f"Madame {sur} {given}" if given else f"Madame {sur}")
            elif given and re.fullmatch(RANKS, given):
                names.append(sur)
            else:
                names.append(f"{sur}, {given}" + (f", {suffix}" if suffix else "") if given else sur)
    return names, note


def listings():
    out = {}
    for url in CTVA:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "bib-daybook (https://impending2223.github.io/bib/)"})
            t = urllib.request.urlopen(req, timeout=60).read().decode("latin-1")
        except Exception as e:
            print(f"listings skipped: {url}: {e}", file=sys.stderr)
            continue
        s = html.unescape(re.sub(r"<br[^>]*>|</p>|</tr>|</td>|</div>", "\n", t))
        s = re.sub(r"[ \t\xa0]+", " ", re.sub(r"<[^>]+>", "", s))
        for b in re.split(r"\n\s*\[\d+\]\s*Meet the Press\s*\n", s)[1:]:
            m = re.match(r"\s*(\d{2}[A-Z][a-z]{2}\d{4})", b)
            g = re.search(r"Guests?\s*\n(.*?)(?=\n#|\Z)", b, re.S)
            if m and g:
                d = datetime.datetime.strptime(m.group(1), "%d%b%Y").date().isoformat()
                out[d] = re.sub(r"\s+", " ", g.group(1)).strip()
    return out


TITLES = r"(?:RIGHT|SEN|REP|GOV|REV|GEN|COL|ADM|MSGR|PROF|DR|CAPT|AMB|MRS|MR|LT|MAJ|JUDGE|MAYOR|LORD|SIR|ARCHBISHOP|BISHOP|RABBI)\.?"
FTN_FIX = {"ADLAi": "ADLAI", "D-CO)": "D-CT)"}
# an office the index gives a guest, taken where the owner asked: {(date, guest): (office as printed, page)}
FTN_ROLES = {("1960-06-05", "Percy, Charles H."): ("Chairman, Committee on Resolutions, GOP National Convention", 154)}
# surnames of more than one word, as the series writes them
FTN_NAMES = {"Ahmed Ben Bella": "Ben Bella, Ahmed", "Maurice Couve De Murville": "Couve de Murville, Maurice",
             "Francisco Caamano Deno": "Caamaño Deñó, Francisco"}
PARTICLES = {"De", "Van", "Von", "Da", "Di", "La", "Le", "Ben", "Bin", "Ibn", "Al", "El"}


def ftn_text(path):
    if path.lower().endswith(".pdf"):
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout
    return open(path, encoding="utf-8").read()


def ftn_headers(text):
    """[(date, head)]: each program's header, through its date; the year from the index's year lines, or the turn of
    the months where a line is missing."""
    starts = re.compile(r"^(?:\S{1,4}\s+)?(?:Debate|“|\"|[A-Z][A-Za-z.'’\-]*[A-Z][A-Za-z.'’\-]*\b|[A-Z]\.)")
    date_end = re.compile(rf"\b({MONTHS})\s*[-.]?\s*(\d{{1,2}})\b\s*[.,]?\s*(?:Part\s+[IVXl1]+\.?)?\s*$")
    year, prev, out, buf = 1959, 0, [], []
    for line in text.split("\n"):
        s = line.strip()
        if re.match(r"^(\d+\s+)?(FACE\s+THE\s+NATION|ANNOTATED\s+CHRONOLOGICAL)", s):
            continue
        if re.fullmatch(r"19[5-7]\d", s):
            year, prev, buf = int(s), 0, []
            continue
        if not s:
            buf = []
            continue
        if not buf and not starts.match(s):
            continue                         # a line of topics
        buf.append(s)
        if not date_end.search(s):
            if len(buf) > 4:
                buf = []
            continue
        head = re.sub(r"\s+", " ", " ".join(buf))
        m = date_end.search(head)
        buf = []
        head = head[:m.start()].rstrip(" ,")
        if not re.search(r"[A-Z]{3,}", head):
            continue
        mon = MONTHS.split("|").index(m.group(1)) + 1
        if mon < prev - 6:
            year += 1
        prev = mon
        num = re.match(r"^[\[\(]?\d{1,2}[.\]]?\s+", head)
        junk = None if num else re.match(r"^(?![A-Z][A-Za-z]*\.?\s)\S{1,4}\s+(?=[A-Z“\"]{2})", head)
        head = head[num.end():] if num else head[junk.end():] if junk else head
        out.append((f"{year}-{mon:02d}-{int(m.group(2)):02d}", head))
    return out


def ftn_guests(head):
    """'Debate between SEN. BARRY M. GOLDWATER (R-AZ) and SEN. EUGENE J. McCARTHY (D-MN)' ->
    (['Goldwater, Barry M.', 'McCarthy, Eugene J.'], None): the index's debates are programs with two guests. A name is a run of words in capitals (one lower-case
    letter allowed: McNAMARA, DeB.), a title before it set aside, a suffix after a comma kept; a run of one word (CORE,
    AFL-CIO) is an office unless it is the whole header (SUKARNO); a name in its own order (NGUYEN-CAO KY) stays so."""
    for a, b in FTN_FIX.items():
        head = head.replace(a, b)
    note = None
    m = re.match(r"^Debate(?: between|:)?\s+", head)          # the debates of 1961: two guests, like any other
    if m:
        head = head[m.end():]
    if head[:1] in "“\"":
        return [], head.strip("“”\", ")
    head = re.sub(r"[“\"][^”\"]*[”\"]\s*", "", head)                 # a nickname: ERNESTO “CHE” GUEVARA
    head = re.sub(r"\b(?!(?:MSGR|PROF|CAPT|ARCHBISHOP|BISHOP)\.)([A-Z]{3,})([A-Z]\.)", r"\1 \2", head)   # JOHNC.
    head = re.sub(r"\b([A-Z]\.)(?=[A-Z]{2})", r"\1 ", head)          # R.SARGENT -> R. SARGENT
    capsword = lambda w: (sum(c.isupper() for c in w) >= 1 and sum(c.islower() for c in w) <= 1
                          and not re.fullmatch(r"\(.*\)?|[A-Z]-[A-Z]{2}\)?", w))
    toks = re.findall(r"\([^)]*\)|[^\s,;]+|[,;]", head)
    names, run, groups = [], [], []
    first = [True]

    def close():
        words = [w for w in run]
        while words and re.fullmatch(TITLES, words[0].rstrip(".") + ("." if words[0].endswith(".") else "")):
            words.pop(0)
        while words and re.fullmatch(TITLES, words[0]):
            words.pop(0)
        if any(w in ("OF", "THE") for w in words):
            groups.append(" ".join(words).title())  # a group, not a person: CREW OF APOLLO 8
        elif len(words) >= 2 or (len(words) == 1 and not names and first[0]):   # SUKARNO, the header's first word
            names.append(words)
    i = 0
    while i < len(toks):
        w = toks[i]
        if w not in (",", ";") and w.lower() not in ("and", "vs.", "vs") and capsword(w) and not w.startswith("("):
            if run and re.fullmatch(TITLES, w) and not re.fullmatch(TITLES, run[-1]):
                close()                          # a title begins the next name: HOWARD METZENBAUM REP. ROBERT TAFT
                run = []
            run.append(w)
        else:
            if run and w == "," and i + 1 < len(toks) and re.fullmatch(r"JR\.?|SR\.?|II|III", toks[i + 1]):
                run.append(toks[i + 1].rstrip(",") if toks[i + 1].endswith(".") else toks[i + 1] + "")
                run[-1] = "SUFFIX:" + run[-1]
                i += 2
                continue
            if run:
                close()
                run = []
            first[0] = False
        i += 1
    if run:
        close()

    def word(w):
        if w.startswith("SUFFIX:"):
            return w[7:].title()
        if re.fullmatch(r"[A-Z]\.", w):
            return w
        m = re.match(r"^(Mc|Mac|De|Di|La|Le|O')(.+)$", w)
        if m and m.group(2)[:1].isupper() and any(c.islower() for c in m.group(1)):
            return m.group(1) + m.group(2)[:1] + m.group(2)[1:].lower()
        return "-".join(p[:1].upper() + p[1:].lower() for p in w.split("-"))
    out = []
    for words in names:
        suf = [word(w) for w in words if w.startswith("SUFFIX:")]
        ws = [word(w) for w in words if not w.startswith("SUFFIX:")]
        full = " ".join(ws)
        if full in FTN_NAMES:
            out.append(FTN_NAMES[full])
        elif len(ws) == 1:
            out.append(ws[0])
        elif "-" in ws[0]:
            out.append(full)                                      # a name in its own order: NGUYEN-CAO KY
        elif len(ws) > 2 and ws[-2] in PARTICLES:
            out.append(f"{ws[-2]} {ws[-1]}, {' '.join(ws[:-2])}" + (f", {suf[0]}" if suf else ""))
        else:
            out.append(f"{ws[-1]}, {' '.join(ws[:-1])}" + (f", {suf[0]}" if suf else ""))
    if groups and not note:
        note = re.sub(r"\b(Of|The|And)\b", lambda m: m.group(0).lower(), groups[0])
        note = note[:1].upper() + note[1:]
    return out, note


def face_the_nation(path):
    rows = []
    for d, head in ftn_headers(ftn_text(path)):
        guests, note = ftn_guests(head)
        r = {"date": d, "show": "Face the Nation", "network": "CBS", "guests": guests}
        if note:
            r["note"] = note
        roles = {g: {"as": FTN_ROLES[(d, g)][0], "page": FTN_ROLES[(d, g)][1]} for g in guests if (d, g) in FTN_ROLES}
        if roles:
            r["roles"] = roles
        r["src"] = "FTN index"
        rows.append(r)
    return rows


def letters(s):
    return re.sub(r"[^a-z]", "", s.lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ftn", help="the Face the Nation index's pages (PDF or text)")
    args = ap.parse_args()
    inv, lst = inventory(), listings()
    tv_days = {d for d, medium, _ in inv if medium == "television"}
    rows = []
    for d, medium, x in inv:
        r = {"date": d, "show": "Meet the Press", "network": "NBC" if medium == "television" else "radio",
             "guests": x["guests"]}
        if x["note"]:
            r["note"] = x["note"]
        r["src"] = "LOC"
        if x["lot"]:
            r["lot"] = x["lot"]
        other = lst.get(d) if medium == "television" and d not in SETTLED else None
        if other:
            surs = [letters(g.split(",")[0]) for g in r["guests"]]
            if not any(s and s in letters(other) for s in surs):
                r["check"] = f"Listings: {re.sub(r'[.]$', '', other.split(',')[0])}. Check."
        rows.append(r)
    for d, guests in LISTED.items():
        if d not in tv_days:
            rows.append({"date": d, "show": "Meet the Press", "network": "NBC", "guests": guests, "src": "listings"})
    if args.ftn:
        rows += face_the_nation(args.ftn)
    elif os.path.exists(OUT):                # keep the rows of the index read before
        rows += [r for r in (yaml.safe_load(open(OUT, encoding="utf-8")) or {}).get("programs", [])
                 if r.get("show") == "Face the Nation"]
    rows.sort(key=lambda r: (r["date"], {"CBS": 0, "radio": 1, "NBC": 2}.get(r["network"], 3)))
    head = ("# Generated by tools/daybook/make_sunday.py (the Library of Congress's inventory of Meet the Press, with the\n"
            "# listings). Edit the script, not this file. One row a program: date, show, network, guests, src, lot, check.\n")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(head)
        yaml.safe_dump({"programs": rows}, f, allow_unicode=True, sort_keys=False, width=1000)
    print(f"{len(rows)} programs ({sum(r['network'] == 'radio' for r in rows)} radio, "
          f"{sum(r['network'] == 'CBS' for r in rows)} Face the Nation); "
          f"{sum(1 for r in rows if r.get('check'))} with a Check; {rows[0]['date']} to {rows[-1]['date']}", file=sys.stderr)


if __name__ == "__main__":
    main()
