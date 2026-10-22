"""The air war, by month: attack sorties in North Vietnam, Laos and South Vietnam. Writes, for The war table
(tools/bib/wartable.py):

    indicators/war-air-attack.yaml     U.S. and VNAF fixed-wing attack sorties by the country of the target, monthly:
                                       as OSD's *Southeast Asia Analysis Report* first printed them (Thayer, vol. 5),
                                       and as the Combat Air Activities file (CACTA) counts them
    indicators/war-air-nvn-rp.yaml     the attack sorties in North Vietnam by route package, CACTA's count only
    sources/war-air-cacta.json         the counts, one block a month CACTA holds (written by --count; kept, so the
                                       series rebuild without the network)

    python3 -I tools/indicators/make_war_air.py --count     reads every CACTA month over the network, writes the counts
    python3 -I tools/indicators/make_war_air.py             writes the two series from the counts and THEN below

The sources:

  CACTA   Combat Air Activities Files (CACTA), Records of U.S. Pacific Command, RG 529, National Archives (series NAID
          2123846), the translation files CACTA.PC.TR.YYMM: one record a target struck on a sortie of a mission, filed by
          the Joint Staff (J-3) from CINCPAC's and CINCSAC's daily reports, Oct. 1965-Jan. 1971. Fifty months survive;
          of Oct. 1965-Dec. 1968 the archive holds 32: no file for Aug. 1966, July and Nov. 1967, Mar., Apr., July and
          Nov. 1968, and July 1966 to the 15th only (the file unit's dates). The layout: CACTA.PC.TR.LAY; the codes: the
          Preliminary File Description of July 10, 1970, in NARA's documentation (137.1DP.pdf, pp. 79, 99, 133 of the
          PDF: Table CB03S, the functions; CB38S, the route packages).
  Thayer  Thomas C. Thayer ed., *A Systems Analysis View of the Vietnam War, 1965-1972*, vol. 5, *The Air War*
          (OASD (PA&E), 1975; archive.org DTIC_ADA051611): the *Report*'s monthly "Aircraft Sorties and Losses", 1967-69,
          cited by the volume's page. Figures read by eye off the page images (the OCR is poor), in THEN.

COUNT (the rules; keep them):
 1. A translated record repeats its fixed set (positions 1-253) for each further occurrence of a periodic set (NARA's
    user note, "Record Format"): a fixed set is counted once.
 2. Only target records (STYPE 'T'); the sortie summaries ('S') carry no target country.
 3. A sortie is its mission date, mission number, sortie letter and launch unit (MSNDT, MSNID, SRTID, LAUIC): a
    sortie that struck several targets (TGTID A, B, ...) is one sortie, filed under its first target's country.
 4. Attack: the sortie function (SFUNC) 01-06 of Table CB03S: strike, flak suppression, air interdiction, armed
    reconnaissance, close air support, direct air support. Reconnaissance, combat air patrol, escort, ECM, FAC,
    flare, tanker and transport sorties are not attack sorties.
 5. The count is of aircraft: each sortie record's number of aircraft (SNRAC), as OSD counted a sortie (one aircraft's
    flight). B-52 (Arc Light) sorties are not in the files read (no B-52 in ACRFT).
 6. Country: CNTRY VN (North Vietnam), LA (Laos), VS (South Vietnam); others (TH, blank, miscoded) counted in "other".
    Route package (RTCOR, CB38S): 1-5, 6 = 6A, 7 = 6B, 0 unknown. The files code no route package before Sept.
    1966 (every North Vietnam sortie 0 or blank): the route-package series begins there.

Checked against Thayer: Jan. and Feb. 1968 together, CACTA counts 9,090 attack sorties in North Vietnam (the Report,
9,638), 12,273 in Laos (14,174), 35,161 in South Vietnam (34,891): the file is the record as kept, not the figures
OSD printed then; both are shown, never one for the other.
"""
import collections
import datetime
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "indicators")
COUNTS = os.path.join(ROOT, "sources", "war-air-cacta.json")
SERIES_NAID = 2123846
SEARCH = "https://catalog.archives.gov/proxy/records/search?ancestorNaId=%d&limit=100&rows=100" % SERIES_NAID
CATALOG = "https://catalog.archives.gov/id/%s"
FIRST, LAST = "6510", "6812"
ATTACK = {"01", "02", "03", "04", "05", "06"}
RP = {"1": "rp1", "2": "rp2", "3": "rp3", "4": "rp4", "5": "rp5", "6": "rp6a", "7": "rp6b", "0": "rp_unk"}
COUNTRY = {"VN": "nvn", "LA": "laos", "VS": "svn"}


def f(line, a, b):
    return line[a - 1:b]


def months():
    """[(yymm, naid, title, url)] of the series' data files, Oct. 1965-Dec. 1968."""
    d = json.loads(urllib.request.urlopen(SEARCH, timeout=120).read())
    out = []
    for h in d["body"]["hits"]["hits"]:
        r = h["_source"]["record"]
        for o in r.get("digitalObjects", []):
            u = o.get("objectUrl", "")
            m = re.search(r"CACTA\.PC\.TR\.(\d{4})$", u)
            if m and FIRST <= m.group(1) <= LAST:
                out.append((m.group(1), r["naId"], r["title"], u))
    return sorted(out)


def count(lines):
    seen, sortie = set(), {}
    nrec = 0
    for line in lines:
        nrec += 1
        fx = f(line, 1, 253)
        if fx in seen:
            continue
        seen.add(fx)
        if f(line, 110, 110) != "T":
            continue
        k = (f(line, 1, 6), f(line, 7, 11), f(line, 13, 13), f(line, 14, 19))
        sortie.setdefault(k, line)
    c = collections.Counter()
    days = set()
    for line in sortie.values():
        if f(line, 22, 23) not in ATTACK:
            continue
        n = int(f(line, 90, 92)) if f(line, 90, 92).strip().isdigit() else 0
        area = COUNTRY.get(f(line, 114, 115), "other")
        c[area] += n
        c["total"] += n
        if area == "nvn":
            c[RP.get(f(line, 116, 116), "rp_unk")] += n
        days.add(f(line, 1, 6))
    return {"records": nrec, "sorties_keys": len(sortie), "days": len(days), **dict(c)}


def run_count():
    have = json.load(open(COUNTS)) if os.path.exists(COUNTS) else {"months": {}}
    for yymm, naid, title, url in months():
        if yymm in have["months"]:
            continue
        print("reading", yymm, url, file=sys.stderr)
        resp = urllib.request.urlopen(url, timeout=600)
        lines = (raw.decode("latin-1") for raw in resp)
        c = count(lines)
        c.update({"naid": naid, "title": title, "file": url.rsplit("/", 1)[1], "url": url})
        have["months"][yymm] = c
        have["read"] = datetime.date.today().isoformat()
        json.dump(have, open(COUNTS, "w"), indent=1, sort_keys=True)
        print(yymm, c, file=sys.stderr)


if __name__ == "__main__" and "--count" in sys.argv:
    run_count()


# ---------------------------------------------------------------- as the Report first printed them (Thayer, vol. 5)
# Attack sorties by fighter and attack aircraft, U.S. and VNAF, read by eye off the page images. (period, {area: n},
# the Report's issue, the page, a note on how the page gives it, printed: where the page's figures disagree)
THAYER5 = "https://archive.org/details/DTIC_ADA051611"
T5 = "Thayer, A Systems Analysis View of the Vietnam War, vol. 5, p. %d (SEA Analysis Report, %s)"
THEN = [
    ("1966-11", {"nvn": 7261}, "1967-03", "Mar. 1967", 222, None, None),
    ("1966-12", {"nvn": 6672}, "1967-03", "Mar. 1967", 222, None, None),
    ("1967-01", {"svn": 14502, "nvn": 6572, "laos": 5329, "total": 26403}, "1967-03", "Mar. 1967", 222, None, None),
    ("1967-02", {"svn": 13543, "nvn": 5472, "laos": 6442, "total": 25457}, "1967-03", "Mar. 1967", 222, None, None),
    ("1967-05", {"svn": 18319, "nvn": 11292}, "1967-06", "June 1967", 240, None, None),
    ("1967-11", {"nvn": 7192, "laos": 4392, "total": 26831}, "1967-12", "Dec. 1967", 254, None, None),
    ("1967-12", {"laos": 6722, "total": 27651}, "1968-01", "Jan. 1968", 260, None, None),
    ("1968-04", {"svn": 18367, "nvn": 7259, "laos": 6887, "total": 32513}, "1968-07", "July 1968", 275, None, None),
    ("1968-05", {"svn": 21386, "nvn": 9739, "laos": 3598, "total": 35173}, "1968-07", "July 1968", 275, None,
     "South Vietnam printed 21,386; the month's total (35,173) and the quarter's (61,592) give 21,836"),
    ("1968-06", {"svn": 21389, "nvn": 10376, "laos": 2346, "total": 34110}, "1968-07", "July 1968", 275, None,
     "the parts as printed add to 34,111; the total is printed 34,110"),
    ("1968-07", {"svn": 19116, "nvn": 14339, "laos": 2728}, "1968-08", "Aug. 1968", 280, "North Vietnam: \"over 14,339\"",
     None),
    ("1968-08", {"nvn": 12940}, "1968-09", "Sept. 1968", 284, None, None),
    ("1968-10", {"laos": 4729}, "1968-12", "Dec. 1968", 289, None, None),
    ("1968-11", {"svn": 16322, "nvn": 330, "laos": 12796, "total": 29448}, "1968-12", "Dec. 1968", 289,
     "North Vietnam: before the halt took effect, Nov. 1", None),
]
NOW_RELEASED = "2015-10-15"     # the date NARA prepared the translation files (CACTA_TSS_137.pdf)
ORDER_KEYS = ("nvn", "laos", "svn", "total")
RP_KEYS = ("rp1", "rp2", "rp3", "rp4", "rp5", "rp6a", "rp6b", "rp_unk")
HEAD = ("# Generated by tools/indicators/make_war_air.py. Edit the script, not this file.\n"
        "# p: period; first: as the Southeast Asia Analysis Report first printed it (released, source); now: as the\n"
        "# Combat Air Activities file counts it (now_released, now_source); counts of sorties (one aircraft's flight).\n")


def period(yymm):
    return "19%s-%s" % (yymm[:2], yymm[2:])


def flow(d):
    """A YAML flow mapping, keys in the order given, strings single-quoted."""
    def val(v):
        if isinstance(v, dict):
            return flow(v)
        if isinstance(v, int):
            return str(v)
        return "'" + str(v).replace("'", "''") + "'"
    return "{" + ", ".join("%s: %s" % (k, val(v)) for k, v in d.items()) + "}"


def cacta_source(c):
    return "CACTA, %s (NARA, NAID %s), counted by tools/indicators/make_war_air.py" % (c["file"], c["naid"])


def build():
    counts = json.load(open(COUNTS))["months"]
    then = {p: x for p, *x in THEN}
    rows = {}
    for yymm, c in counts.items():
        p = period(yymm)
        r = {"p": p, "now": {k: c.get(k, 0) for k in ORDER_KEYS},
             "now_released": NOW_RELEASED, "now_source": cacta_source(c)}
        if c.get("other"):
            r["now"]["other"] = c["other"]
        if c.get("days", 0) < 28:
            r["note"] = "the file holds %s days" % c["days"]
        rows[p] = r
    for p, (v, rel, issue, page, note, printed) in then.items():
        r = rows.setdefault(p, {"p": p})
        first = {k: v[k] for k in ORDER_KEYS if k in v}
        r.update({"first": first, "released": rel, "source": T5 % (page, issue)})
        if note:
            r["note"] = "; ".join(x for x in (r.get("note"), note) if x)
        if printed:
            r["printed"] = printed
    out = [HEAD, "id: war-air-attack\n", "name: 'Attack sorties, by country'\n", "freq: M\n", "manual: true\n",
           "kind: war\n", "then: {label: 'As the Southeast Asia Analysis Report first printed them'}\n",
           "now: {label: 'As the Combat Air Activities file counts them'}\n", "rows:\n"]
    order = ("p", "first", "released", "source", "now", "now_released", "now_source", "note", "printed")
    for p in sorted(rows):
        r = rows[p]
        out.append("- " + flow({k: r[k] for k in order if k in r}) + "\n")
    open(os.path.join(OUT, "war-air-attack.yaml"), "w").write("".join(out))
    out = [HEAD, "id: war-air-nvn-rp\n", "name: 'Attack sorties in North Vietnam, by route package'\n", "freq: M\n",
           "manual: true\n", "kind: war\n", "then: {label: '—'}\n",
           "now: {label: 'As the Combat Air Activities file counts them'}\n", "rows:\n"]
    for yymm in sorted(counts):
        c = counts[yymm]
        if not c.get("nvn") or c.get("rp_unk", 0) == c["nvn"]:
            continue                    # no route package coded (the files before Sept. 1966)
        v = {k: c.get(k, 0) for k in RP_KEYS if c.get(k)}
        v["total"] = c["nvn"]
        assert sum(x for k, x in v.items() if k != "total") == v["total"], yymm
        r = {"p": period(yymm), "now": v, "now_released": NOW_RELEASED, "now_source": cacta_source(c)}
        if c.get("days", 0) < 28:
            r["note"] = "the file holds %s days" % c["days"]
        out.append("- " + flow(r) + "\n")
    open(os.path.join(OUT, "war-air-nvn-rp.yaml"), "w").write("".join(out))
    for p, (v, *_rest) in then.items():
        parts = [v[k] for k in ("nvn", "laos", "svn") if k in v]
        if "total" in v and len(parts) == 3 and sum(parts) != v["total"] and not _rest[-1]:
            raise SystemExit("%s: the parts do not make the total and no printed note" % p)
    print("wrote war-air-attack.yaml (%d rows), war-air-nvn-rp.yaml" % len(rows))


if __name__ == "__main__" and "--count" not in sys.argv:
    build()
