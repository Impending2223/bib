"""Write sources/nomination-hearings.yaml: the printed nomination hearings on govinfo, Jan. 1, 1953-Aug. 31, 1974.

    python3 -I tools/sources/make_nomination_hearings.py --cache DIR [--fetch] [--print]

--fetch reads govinfo (needs the network; the build does not): the hearings collection's sitemaps, a year a file
(https://www.govinfo.gov/sitemap/CHRG_<YEAR>_sitemap.xml, 1952-1975: a package is filed by its dateIssued, which for
these scanned hearings is the first day held), then the MODS of every Senate and joint committee package listed
(https://www.govinfo.gov/metadata/pkg/<ID>/mods.xml), and of the House's in 1973 (Ford's nomination as Vice
President under the Twenty-fifth Amendment), three requests at a time, a short pause after each, each kept in DIR/mods/ so a rerun
reads only what is missing. Without --fetch the script reads DIR alone. The output is generated: never edit it.

Sources. govinfo's MODS for each package: its title as printed (`titleInfo/title`), its days held (`heldDate`, the
extension's), its Congress and session, its chamber, its committee (`congCommittee`'s authority name; a subcommittee
the title names is kept as the title gives it), its `isNomination` flag, and the package's details page, the link
(https://www.govinfo.gov/app/details/<ID>).

RULES
1. A hearing is a nomination hearing where GPO's MODS flags it (`isNomination` true) or its title says so: the words
   "nomination" or "nominations" (as "Nomination of", "Nominations", "Proposed nomination"), or "-designate"
   ("Secretary of Defense-designate"), before the title's "hearing(s) before" (a bill's hearing whose subject runs on
   to a nomination is caught by its subject, not its committee's name). Both are listed with the ground found
   (`ground`: flag, title, both). A package flagged but whose title names no nominee is kept, `nominees` empty, with
   a `check`.
2. Span: a day held from Jan. 1, 1953 to Aug. 31, 1974 (the Executive roster's span); a hearing with no day held is
   kept by its dateIssued and says so (`dated: issued`).
3. Nominees: read from the title's subject: "Nomination of A, to be B", "Nominations of A, B, and C", "A, to be B",
   "A, Secretary of Defense-designate", "on the nomination of A to be B", a list separated by semicolons. Each
   nominee is his name as the title prints it (`name`), the office as the title gives it (`office`, or none), and
   the name parsed (`surname`, `given`, `suffix`): the surname the last word but a suffix (Jr., Sr., II, III), a
   particle with it (de, Van, Mc). A title the rules cannot read (no "of", a list too garbled) keeps its nominees
   empty and carries a `check` naming why; nothing is guessed.
4. Left out (the run of Nov. 5, 2026, 4,086 packages' MODS read: every Senate and joint package of 1952-75, the House's
   of 1973):
   - outside the span: 61 packages GPO flags or titles as nominations, held Sept. 1974 to 1975 (the 1975 sitemap's,
     and the 93d Congress's last months); and none before 1955 is on govinfo (the 1952-60 sitemaps hold 38 hearings
     in all, three of them nominations, 1955);
   - a title naming a nomination only as the subject of a bill or an inquiry, GPO's flag false (NOT_NOM): "Nomination
     and election of President and Vice President and qualifications for voting", parts 1-5 (CHRG-87shrg70784p1-p5,
     1961) and CHRG-88shrg20601 (1963); "Nomination and appointment of committee members and chairmen"
     (CHRG-92shrg56866, 1971: the Senate's own committee assignments);
   - no House package of 1973 is flagged or titled a nomination in GPO's catalogue (Ford's nomination as Vice
     President is here by the Senate Rules Committee's hearing, CHRG-93shrg23712O); no joint committee's package is.
   EXCLUDED holds any package left out by hand later, with its reason (none now).
5. A package's days are GPO's (`heldDate`); where a hearing's own heading gives another day (CHRG-89shrg59943: Mar. 2,
   1966; GPO, Mar. 3) or the days of a sundry volume are incomplete (CHRG-87shrg91496: GPO gives Feb. 8 and Oct. 4,
   1962; its text holds a dozen days), the calendar's entry follows the heading and says so; the file keeps GPO's.

STYLE
1. One row a package, in the order of the first day held, then the package id. Titles as GPO's MODS print them, but
   the trailing full stop; nothing abridged in the file (the pages shorten it where they need: tools/bib/lives.py).
2. The days held as ISO dates, a list; the session as MODS gives it; the committee by its authority name ("Committee
   on Armed Services"), the chamber "S", "H" or "J".
3. Matching each nominee to a person in the series is not done here: tools/bib/hearings.py does it at build, by the
   series' rules, and sources/nomination-hearing-matches.yaml settles by hand what the rules cannot.
"""
import argparse
import concurrent.futures
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "sources", "nomination-hearings.yaml")
SITEMAP = "https://www.govinfo.gov/sitemap/CHRG_{y}_sitemap.xml"
MODS = "https://www.govinfo.gov/metadata/pkg/{p}/mods.xml"
DETAILS = "https://www.govinfo.gov/app/details/{p}"
YEARS = range(1952, 1976)
FROM, TO = "1953-01-01", "1974-08-31"
NS = {"m": "http://www.loc.gov/mods/v3"}

# Packages left out by hand, with the reason (RULES 4). Filled from the run's review.
EXCLUDED = {}


def get(url, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "bib-series research (nomination hearings)"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if isinstance(e, urllib.error.HTTPError) and e.code == 404:
                return None
            time.sleep(5 * (k + 1))
    raise RuntimeError("failed: " + url)


def wanted(pid, year):
    """The packages whose MODS are read: the Senate's and the joint committees'; the House's of 1973."""
    m = re.match(r"CHRG-\d+([shj])hrg", pid)
    if not m:
        return False
    return m.group(1) in "sj" or (m.group(1) == "h" and year == 1973)


def fetch(cache):
    os.makedirs(os.path.join(cache, "sitemaps"), exist_ok=True)
    os.makedirs(os.path.join(cache, "mods"), exist_ok=True)
    todo = []
    for y in YEARS:
        p = os.path.join(cache, "sitemaps", "%d.xml" % y)
        if not os.path.exists(p):
            body = get(SITEMAP.format(y=y)) or b""
            with open(p, "wb") as f:
                f.write(body)
            time.sleep(1)
        with open(p, "rb") as f:
            ids = re.findall(rb"/app/details/(CHRG-[^<\s]+)", f.read())
        todo += [(i.decode(), y) for i in ids if wanted(i.decode(), y)]
    left = [pid for pid, y in todo if not os.path.exists(os.path.join(cache, "mods", pid + ".xml"))]

    def one(pid):
        body = get(MODS.format(p=pid))
        with open(os.path.join(cache, "mods", pid + ".xml"), "wb") as f:
            f.write(body or b"")
        time.sleep(0.5)
    with concurrent.futures.ThreadPoolExecutor(3) as ex:      # three at a time, a pause after each
        for n, _ in enumerate(ex.map(one, left), 1):
            if n % 200 == 0:
                print("fetched", n, "of", len(left), file=sys.stderr)
    return todo


# ---------------------------------------------------------------- reading the MODS

def text(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip() if el is not None else ""


def read_mods(path):
    """The particulars of one package (RULES 1-2), or None for an empty or unreadable file."""
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return None
    m = "{http://www.loc.gov/mods/v3}"
    pid = os.path.basename(path)[:-4]
    title = text(root.find(m + "titleInfo/" + m + "title"))
    out = {"package": pid, "title": title, "held": [], "nominees_mods": [], "flag": False}
    for ext in root.findall(m + "extension"):
        for el in ext:
            tag = el.tag.replace(m, "")
            if tag == "heldDate" and el.text:
                out["held"].append(el.text.strip()[:10])
            elif tag == "congress" and el.text:
                out["congress"] = int(el.text.strip())
            elif tag == "session" and el.text:
                out["session"] = el.text.strip()
            elif tag == "chamber" and el.text:
                out["chamber"] = {"SENATE": "S", "HOUSE": "H", "JOINT": "J"}.get(el.text.strip(), el.text.strip())
            elif tag == "isNomination":
                out["flag"] = (el.text or "").strip() == "true"
            elif tag == "congCommittee" and "committee" not in out:
                nm = el.find(m + "name[@type='authority-standard']")
                out["committee"] = text(nm)
                out["committee_chamber"] = el.get("chamber")
            elif tag == "nominee":
                out["nominees_mods"].append((text(el.find(m + "name")), text(el.find(m + "position"))))
    out["issued"] = text(root.find(m + "originInfo/" + m + "dateIssued"))[:10]
    out["held"] = sorted(set(out["held"]))
    if "chamber" not in out:
        c = re.match(r"CHRG-\d+([shj])", pid)
        out["chamber"] = c.group(1).upper() if c else ""
    return out


# ---------------------------------------------------------------- the title (RULES 1, 3)

MONTH = r"(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan\.|Feb\.|Mar\.|Apr\.|Aug\.|Sept?\.|Oct\.|Nov\.|Dec\.)"
HEAD = re.compile(r":\s*(?:joint\s+)?(?:hearings?|executive session|report|nomination hearings?)\b", re.I)
NOMWORD = re.compile(r"\bnominations?\b|-designate\b|\bdesignate[ds]?\b", re.I)
NOT_NOM = re.compile(r"nominations? (?:of|for) (?:candidates|presidential|president(?:ial)? candidates|electors)"
                     r"|nominating|nomination (?:process|system|procedures?)|presidential nominations? reform"
                     r"|nomination and election of (?:the )?president|appointment of committee members", re.I)


def is_nomination(h):
    """RULES 1: (ground or None)."""
    main = HEAD.split(h["title"], 1)[0]
    by_title = bool(NOMWORD.search(main)) and not NOT_NOM.search(h["title"])
    if not by_title:          # a subject that names a nomination: 'on the nomination of ...', '... -designate'
        sub = subject(h["title"])
        by_title = bool(re.search(r"\bon (?:the )?(?:proposed )?(?:\w+ )?nominations?\b|-designate\b", sub, re.I)) \
            and not NOT_NOM.search(h["title"])
    if h["flag"] and by_title:
        return "both"
    return "flag" if h["flag"] else ("title" if by_title else None)


def subject(title):
    """What the hearing is on: the title after its session ('... first session, on ...'), its dates cut."""
    m = re.search(r"\bsession\b[,.]?\s*(.*)$", title, re.I | re.S)
    t = m.group(1) if m else ""
    return cut_dates(t)


def cut_dates(t):
    t = re.sub(r"\s*(?:\.\.\.|…)\s*", " ", t)
    t = re.sub(r"[,.;]?\s*(?:\(?(?:held )?(?:on )?)" + MONTH + r"\s*\d.*$", "", t, flags=re.S)
    t = re.sub(r"[,.;]?\s*\d{4}\.?$", "", t)
    return t.strip(" .,;:")


SFX = r"(?:,?\s+(?:Jr\.?|JR\.?|Sr\.?|SR\.?|II|III|IV|2d|3d))"
TITLE_WORDS = (r"(?:(?:Hon\.|Honorable|Mr\.|Mrs\.|Miss|Ms\.|Dr\.|Rev\.|Judge|Gov\.|Governor|Senator|Gen\.|General|"
               r"Adm\.|Admiral|Vice Adm\.|Vice Admiral|Rear Adm\.|Rear Admiral|L[Tt]\.? Gen\.|Lieutenant General|"
               r"Maj\.? Gen\.|Major General|Col\.|Colonel|Capt\.|Captain|Brig\.? Gen\.|Brigadier General|Ambassador|"
               r"Prof\.|Professor)\s+)")
SERVICE = r"(?:,?\s+(?:USCG|USN|USAF|USA|USMC|U\.S\.N\.|U\.S\.A\.|U\.S\.A\.F\.|Usn|Uscg|Usaf))"
NAME = (r"(?P<name>" + TITLE_WORDS + r"*(?:[A-Z][\w'’.\-]*\.?)(?:\s+(?:[A-Z][\w'’.\-]*|[a-z]{1,3}[A-Z][\w'’.\-]*|de|De|del|van|Van|von|la|La|"
        r"du|di|der|St\.|y|d'|O'[A-Z]\w+|Mac\w+|Mc\w+|[A-Z]\.)){1,5}" + SFX + r"?)")
STATE = r"(?:,?\s+of\s+(?:the\s+)?(?:[A-Z][\w.]*)(?:\s+[A-Z][\w.]*){0,2})"
LINK = r"(?:,\s*|\s+)(?:to\s+be|as|nominated\s+to\s+be|for|to|-|–|—)\s+"


def nominees_of(title):
    """The nominees a title names (RULES 3): [(name as printed, office or '')], and a note where the rules fail."""
    sub = subject(title)
    main = HEAD.split(title, 1)[0].strip()
    m = re.search(r"\b(?:on|for)\s+(?:the\s+)?(?:proposed\s+)?(?:(?:\w+|ambassadorial)\s+)?nominations?"
                  r"(?:\s+(?:of|for))?\s*:?\s*(.*)$", sub, re.I | re.S)
    if m:
        body = m.group(1)
    elif re.match(r"on\s+", sub, re.I) and re.search(r"-designate|nominated", sub, re.I):
        body = re.sub(r"^on\s+", "", sub, flags=re.I)
    else:
        mm = re.match(r"(?:proposed\s+)?nominations?\s+of\s+(.*)$", main, re.I)
        body = mm.group(1) if mm else ""
    body = cut_dates(body)
    if not body:
        return [], "the title names no nominee"
    out = []
    # a list: semicolons, else commas before a capitalized name, and 'and'
    parts = [p for p in re.split(r";\s*(?:and\s+|\[and\]\s+)?", body) if p.strip()]
    if len(parts) == 1:
        parts = split_commas(body)
    for part in parts:
        part = re.sub(r"^\s*(?:and|\[and\])\s+", "", part.strip()).strip(" ,.")
        part = re.sub(r"\s*\[and\]\s*", " and ", part)
        mm = re.match(NAME + STATE + r"?(?:" + LINK + r"(?P<office>.+)|,\s*(?P<office2>[^,]*-designate.*)|"
                      r",\s*(?P<office3>(?:to be |as )?[^,]+))?$", part)
        if not mm:
            return [], "the title's list could not be read: " + part[:80]
        name = mm.group("name").strip()
        office = (mm.group("office") or mm.group("office2") or mm.group("office3") or "").strip(" ,.")
        office = re.sub(r"^(?:to be|as)\s+", "", office)
        out.append((name, office))
    # several names sharing one office ('A, B, and C to be members of ...')
    if out and out[-1][1]:
        for k in range(len(out) - 1, -1, -1):
            if out[k][1]:
                last = out[k][1]
            else:
                out[k] = (out[k][0], last)
    return out, None


ORG_END = (r"^(?:[A-Z][\w.'’-]*\s+){0,4}(?:Commission|Board|Division|Agency|Affairs|Mobilization|Development|"
           r"Administration|Service|Services|Corporation|Authority|Bureau|Department|Office|Logistics|Welfare|Finance|"
           r"Commerce|Budget|Reserve|Council|Institute|Foundation|Bank|Fund|Planning|Security|Programs|Resources|"
           r"Reserve Affairs|Personnel|Engineering|Installations|Materiel|Research|Space|Labor|Industry|Navigation|"
           r"Wildlife|Parks|Power|Mines|Reclamation|Insular Affairs)\b(?:\s*\([^)]*\))?$")


def split_commas(body):
    """'A, to be X, B, to be Y, and C, to be Z' or 'A, B, and C to be members': the parts, a name a part."""
    toks = re.split(r"(,\s*(?:and\s+|\[and\]\s+)?|\s+and\s+(?=(?:Mrs?\.|Dr\.|[A-Z])))", body)
    seps = toks[1::2] + [""]
    toks = toks[0::2]
    # a part that is the rest of an office's name ('Securities and Exchange Commission', 'Office of Civil and
    # Defense Mobilization') goes back to the part before it, with its separator
    merged = []
    for i, t in enumerate(toks):
        if merged and re.search(ORG_END, t.strip()) and not re.search(r"\b(?:to be|as)\b", t):
            merged[-1] = merged[-1] + seps[i - 1] + t
        else:
            merged.append(t)
    toks = merged
    parts = []
    for t in toks:
        t = t.strip()
        if not t:
            continue
        starts_name = re.match(TITLE_WORDS + r"*[A-Z][\w'’.\-]*\.?\s+(?:[A-Z]|de |van |von |la )", t) and not re.match(
            r"(?:of|to|as|for)\b|(?:Jr|Sr)\.?$|I[IV]+$", t) and not re.match(
            r"(?:Assistant|Under|Deputy|Secretary|Director|Administrator|Commissioner|Chairman|Member|Members|Judge|"
            r"Ambassador|General Counsel|Associate|Chief|United States|U\.S\.|Department|Board|Federal|"
            r"Office|Bureau|Agency|Commission|Comptroller|Treasurer|Solicitor|Governor of|Representative|Alternate|"
            r"Special|Inspector|Executive|Civil|Atomic|National|Interstate|Securities|Small|Tennessee|Export|"
            r"Veterans|International|Housing|Public|Panama|Canal|Coast|Selective|Arms|Peace|Central|Foreign|"
            r"Renegotiation|Subversive|Tariff|Railroad|Postmaster|Register|Archivist|Librarian|Public Printer)\b", t)
        if starts_name or not parts:
            parts.append(t)
        elif re.match(r"(?:Jr|Sr)\.?$|I[IV]+$|2d$|3d$", t):
            parts[-1] += ", " + t
        else:
            parts[-1] += ", " + t
    return parts


def parse_name(name):
    """(surname, given, suffix): the title words dropped, the particle with the surname."""
    n = re.sub(r"^" + TITLE_WORDS + r"+", "", name, flags=re.I).strip()
    n = re.sub(SERVICE + r"$", "", n).strip(" ,")
    sfx = ""
    m = re.search(SFX + r"$", n)
    if m:
        sfx = m.group(0).strip(" ,").rstrip(".")
        sfx = {"2d": "II", "3d": "III", "JR": "Jr", "SR": "Sr"}.get(sfx, sfx)
        n = n[:m.start()].strip(" ,")
    w = n.split()
    k = len(w) - 1
    while k > 1 and w[k - 1] in ("de", "De", "del", "van", "Van", "von", "la", "La", "du", "di", "der", "St."):
        k -= 1
    return " ".join(w[k:]), " ".join(w[:k]), sfx


# ---------------------------------------------------------------- the rows

def clean_office(t):
    t = re.sub(r"\s+", " ", t or "").strip(" ,.;")
    t = re.sub(r"^(?:to be|as|for|nominee-designate for|nominated to be)\s+", "", t, flags=re.I)
    return t


def nominee(name, office):
    name = re.sub(r"\s+", " ", name).strip(" ,.;")
    if name and name == name.lower() or re.search(r"\b[a-z]{3,}$", name):   # GPO's 'Newell brown'
        name = " ".join(w[:1].upper() + w[1:] if w.islower() and len(w) > 2 else w for w in name.split())
    sur, given, sfx = parse_name(name)
    return {"name": name, "office": clean_office(office), "surname": sur, "given": given, "suffix": sfx}


def rows(cache):
    out, excluded = [], []
    for f in sorted(os.listdir(os.path.join(cache, "mods"))):
        h = read_mods(os.path.join(cache, "mods", f))
        if not h:
            continue
        g = is_nomination(h)
        if not g:
            continue
        if h["package"] in EXCLUDED:
            excluded.append((h["package"], EXCLUDED[h["package"]]))
            continue
        first = (h["held"] or [h["issued"]])[0]
        if not (FROM <= first <= TO):
            continue
        r = {"package": h["package"], "title": h["title"].rstrip(" ."), "chamber": h.get("chamber"),
             "committee": h.get("committee") or "", "congress": h.get("congress"), "session": h.get("session"),
             "held": h["held"]}
        if not h["held"]:
            r["issued"], r["dated"] = h["issued"], "issued"
        r["ground"] = g
        why = None
        if h["nominees_mods"]:
            r["nominees"] = [nominee(n, o) for n, o in h["nominees_mods"] if n.strip()]
            r["nominees_from"] = "mods"
        else:
            ns, why = nominees_of(h["title"])
            if not ns:            # a title that is its nominee: 'Robert F. Kennedy, Attorney-General-designate'
                main = HEAD.split(h["title"], 1)[0].strip()
                m = re.match(NAME + r",\s*(?P<office>[^,]*-?designate.*)$", main, re.I)
                if m and not re.match(r"Nominations?\b", main, re.I):
                    ns, why = [(m.group("name"), m.group("office"))], None
            r["nominees"] = [nominee(n, o) for n, o in ns]
            r["nominees_from"] = "title"
        if why or not r["nominees"]:
            r["check"] = why or "the title names no nominee"
        r["url"] = DETAILS.format(p=h["package"])
        out.append(r)
    out.sort(key=lambda r: ((r["held"] or [r.get("issued")])[0], r["package"]))
    return out, excluded


HEADER = """# Generated by tools/sources/make_nomination_hearings.py from govinfo's MODS (its docstring: sources, rules, STYLE).
# Never edit: rerun the script. Who each nominee is: tools/bib/hearings.py and sources/nomination-hearing-matches.yaml.
"""


def write(out):
    body = yaml.safe_dump({"hearings": out}, allow_unicode=True, sort_keys=False, width=120)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(HEADER + body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--print", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch(a.cache)
    out, excluded = rows(a.cache)
    if a.print:
        for r in out:
            print(r["package"], (r["held"] or [r.get("issued")])[0], r["ground"], r["nominees_from"],
                  "|", HEAD.split(r["title"], 1)[0][:90])
            for n in r["nominees"]:
                print("    ", n["name"], "|", n["office"], "|", n["surname"], "/", n["given"], "/", n["suffix"])
            if r.get("check"):
                print("    !!", r["check"])
        return
    write(out)
    print(len(out), "hearings;", sum(len(r["nominees"]) for r in out), "nominees;",
          sum(1 for r in out if r.get("check")), "with a check;", len(excluded), "excluded by hand", file=sys.stderr)


if __name__ == "__main__":
    main()
