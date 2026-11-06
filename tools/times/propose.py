"""Times of day: proposals for review, never written into the entries (the owner, Oct. 30, 2026: "Do we have anyone to
do a pass over the entries that might have a time of day and get them started?"; the hand-off of Nov. 1, item 0c).

    python3 -I tools/times/propose.py            writes notes/times-proposals.yaml and prints the counts

The mechanical tier (no agents), for each calendar entry dated to a day:
  rec   a White House recording the note cites (the Miller Center's page, or PRDE's), its catalogued time; the zone
        by PRDE's place (the LBJ Ranch and Austin, Central; elsewhere Washington, Eastern)
  frus  a FRUS document the note cites, the time the daybook keeps for it (frus:doc-dateTime-min's clock): the
        TEI's stamps are written at UTC-5 (Washington's standard time) whatever the place or season, so the clock is
        read at UTC-5 (zone Etc/GMT+5) and the local hour is the reviewer's, from the document's own heading or
        opener (zone_check always): a cable's time is its sending, a memorandum of conversation the meeting's, so
        the proposal holds only where the entry is the meeting or the paper
  ppp   an item of the Public Papers the note cites, found by the cite's printed page (the item's first page:
        "[1961 Pub. Papers 1](...#page=59)"), else by the PDF page and the entry's day (the item the link names, not
        the first on its page), the hour its NOTE (kind n) or the editors' bracketed line (kind b: "[Delivered from
        the President's office at 8 p.m.]") gives: "at 7:40 p.m.", the OCR's "at io a.m.", "at 4 o'clock" (a.m. or
        p.m. by the sentence's morning, afternoon or evening, else by the hour, with `check`); where the item is the
        entry's day and the sentence names no other day; the zone by the sentence's place
  text  an hour the entry's own `c` names ("at 12:30 p.m.", "noon"); the zone the place where the event happened
        (event_zone: the entry's opening words, "Toledo.", "Hyannis Port, Mass.", or a place after "at" or "in"),
        not any place `c` mentions; else Washington's with `zone_check: true`

The tiers read once from their sources (tools/times/tiers.py writes tools/times/data/<tier>.json; this script reads
them, no network):
  congress  the Daily Digest's hours, for an entry that is a chamber's floor act that day (the chamber named with a
        verb of the floor: "Senate passes", "House, 289 to 126"): the adjournment (or recess) hour the Digest gives
        for that chamber's day ("Adjournment: Adjourned at 7:12 p.m."). Where the entry is the adjournment itself
        ("adjourns sine die") the hour is the event's (role: adjourned); where the Digest says when the chamber met
        and the entry is the meeting ("convenes"), that hour (role: met); otherwise the act came before it (role:
        before, bound: true): an upper bound, for `follows`, never a `time` by itself
  dtg   a message's date-time group in the note ("CINCPAC to JCS, 180612Z Dec. 60", Zulu, UTC) where its day is the
        entry's; the message's time is its sending (the proposal holds only where the entry is the message or the
        act it records); a DTG behind "To check:" is a message unread (unread: true); and a military hour in `c`
        ("at 2115H", Hotel, UTC+8, the Gulf of Tonkin's; "1500 Saigon time"; "2000 GMT")
  launch  a launch the entry is (the space threads; launch words in `c`), its time as the KSC's Summary of Major
        NASA Launchings prints it ("09:47 a.m. EST", the label's own offset), the mission named in `c` or the only
        NASA launch that day (match: date); or as *Astronautics and Aeronautics* (1963-68) gives it that day
  test  a United States nuclear test the entry is, its time (GMT) in DOE/NV-209, the test named in `c`, or the page
        the note cites, or the only test that day (match: date)
  unsc  a Security Council meeting on the entry's day, the entry naming the Council: the verbatim record's hour
        ("Held in New York, on Friday, 1 April 1960, at 3 p.m."; "called to order at 3.20 p.m."), with the hour it
        rose (`rose`); a vote's or a speech's time within it is the record's text, not this hour (role: met)

STYLE
1. A proposal: id, local time as the source gives it, zone (IANA), the UTC instant (zoneinfo, the 1960s rules: the
   States' daylight time as each zone's history records it), approx (where the source rounds or says "about"), source,
   basis (the cite), zone_check where the zone is a guess. Several for an entry: all kept, the reviewer picks.
2. The reviewer moves a proposal into the entry (`time`, `time_approx`) by patch, the source in the note. The file is
   regenerated; never edited by hand.
3. The tiers of the hand-off (2-4): congress, dtg, launch, test, unsc, above. A row may carry, besides STYLE 1's
   fields: role (met, adjourned, before), bound (the hour is a limit, not the event's), until (local: the hour the
   meeting rose), match (what tied the row to the entry where it was not a name: date), unread (the source is behind
   "To check:"), cited (false: the source is not in the note; the reviewer adds it), url (the page read).
4. Zones (the 1965 reviewer's faults, Nov. 6, 2026): the place where the event happened, never a place the entry
   only names ("the Berlin Wall" in a Selma entry; Washington's meetings on Vietnam). Daylight time as the place kept
   it: zoneinfo's America/Chicago keeps Chicago's, but Texas kept no daylight time until the Uniform Time Act (1967):
   the Ranch, Austin, Dallas, Houston, before 1967, are UTC-6 all year (Etc/GMT+6). Alabama, Mississippi, Louisiana
   and Tennessee's places, where daylight time was a city's or county's choice, are read at standard time with
   zone_check: true; so are the places whose 1960s practice zoneinfo does not record (UNSURE: North Dakota,
   Huntsville, New Haven, Albany, Ga., Birmingham, Nashville, Montgomery, Jackson, Atlanta, Miami, Denver; the
   reviewers of 1960-62), read by their zone's rules. A printed zone ("EST", "EDT", "GMT", "Z", "H") is the zone, as a
   fixed offset. FRUS's stamps are UTC-5 (frus, above).
"""
import datetime
import glob
import os
import re
import sys
import zoneinfo

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from tools.bib import store  # noqa: E402
from tools.times import propose_tiers as tiers  # noqa: E402

DC = "America/New_York"
TEXAS = "Texas"          # America/Chicago's offsets, but no daylight time before 1967 (STYLE 4)
SOUTH = "South"          # Central standard time, daylight time a local choice: zone_check (STYLE 4)
ZONES = [  # a place the entry names -> its zone (first match in `c`)
    (r"\bSaigon\b|South Vietnam|\bHuế\b|Đà Nẵng|Khe Sanh", "Asia/Ho_Chi_Minh"),   # zoneinfo: +8 in 1959-75
    (r"\bHanoi\b|North Vietnam|Haiphong", "Asia/Bangkok"),                         # +7
    (r"\bMoscow\b|\bKremlin\b", "Europe/Moscow"),
    (r"\bBerlin\b", "Europe/Berlin"), (r"\bParis\b", "Europe/Paris"), (r"\bLondon\b", "Europe/London"),
    (r"\bHavana\b", "America/Havana"), (r"Puerto Ric|San Juan", "America/Puerto_Rico"),
    (r"\bRio de Janeiro\b|\bBras[ií]lia\b|S[aã]o Paulo", "America/Sao_Paulo"), (r"\bMexico City\b", "America/Mexico_City"),
    (r"\bBonn\b|\bFrankfurt\b|\bCologne\b", "Europe/Berlin"), (r"\bRome\b", "Europe/Rome"), (r"\bDublin\b|Ireland", "Europe/Dublin"),
    (r"\bSeoul\b", "Asia/Seoul"), (r"\bBangkok\b", "Asia/Bangkok"), (r"\bCanberra\b|\bMelbourne\b", "Australia/Sydney"), (r"\bVienna\b", "Europe/Vienna"), (r"\bGeneva\b", "Europe/Zurich"),
    (r"\bTokyo\b", "Asia/Tokyo"), (r"\bManila\b", "Asia/Manila"), (r"\bHonolulu\b", "Pacific/Honolulu"),
    (r"\bDallas\b|\bAustin\b|\bJohnson City\b|LBJ Ranch|\bthe Ranch\b|\bHouston\b|\bSan Antonio\b|\bFort Worth\b|"
     r"\bStonewall, Tex|\bTexas\b", TEXAS),
    (r"\bMemphis\b|\bNashville\b|\bSelma\b|\bMontgomery\b|\bBirmingham\b|\bHuntsville\b|\bTuscaloosa\b|"
     r"\bOxford, Miss|\bJackson(?:, Miss)?\b|\bNew Orleans\b", SOUTH),
    (r"\bAlbany, Ga|\bAtlanta\b|\bMiami\b|\bNew Haven\b", DC),
    (r"\bNorth Dakota\b|\bBismarck\b|\bFargo\b|\bChicago\b", "America/Chicago"),
    (r"\bLos Angeles\b|\bSan Francisco\b|\bWatts\b|\bBerkeley\b|\bOakland\b|\bSacramento\b", "America/Los_Angeles"),
    (r"\bDenver\b", "America/Denver"),
    (r"\bWashington\b|White House|Oval Office|\bthe Capitol\b|\bNew York\b|\bBoston\b|\bAtlantic City\b", DC),
]
# Places whose 1960s daylight time zoneinfo does not record (a State's, a city's or a county's own choice then; the
# reviewers of 1960-62, Nov. 6, 2026): read by the zone's rules, zone_check always (STYLE 4).
UNSURE = re.compile(r"North Dakota|Bismarck|Fargo|Huntsville|New Haven|Albany, Ga|Birmingham|Nashville|Montgomery|"
                    r"Jackson|Memphis|Selma|Tuscaloosa|Oxford, Miss|New Orleans|Atlanta|Miami|Denver")
HOUR = re.compile(r"\b(?:(about|around|some|shortly after|shortly before|near|nearly|by)\s+)?(\d{1,2})(?:[:.](\d{2}))?\s*"
                  r"(a\.m\.|p\.m\.)|\b(?:(about|around)\s+)?(noon|midnight)\b", re.I)


def real_zone(zone, day):
    """A ZONES key -> (the IANA zone or fixed offset to turn the clock by, a zone_check where daylight time is a
    guess)."""
    if zone == TEXAS:
        return ("Etc/GMT+6", False) if day < "1967-01-01" else ("America/Chicago", False)
    if zone == SOUTH:
        return ("Etc/GMT+6", True) if day < "1967-01-01" else ("America/Chicago", False)
    return zone, False


def to_utc(day, hhmm, zone):
    zone = real_zone(zone, day)[0]
    h, m = map(int, hhmm.split(":"))
    local = datetime.datetime.combine(datetime.date.fromisoformat(day), datetime.time(h % 24, m),
                                      tzinfo=zoneinfo.ZoneInfo(zone))
    return local.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def zone_of(text):
    for rx, z in ZONES:
        if re.search(rx, text):
            return z
    return None


def event_zone(c):
    """(zone, the words that placed it), or None. See place_zone."""
    return _event_zone(c)


def place_zone(c):
    """(zone key, zone_check) for the place where the entry's event happened, Washington's with zone_check where
    nothing places it (STYLE 4)."""
    ez = _event_zone(c)
    if not ez:
        return DC, True
    return ez[0], bool(UNSURE.search(ez[1]))


def _event_zone(c):
    """The zone of the place where the entry's event happened: its opening words where they are a place
    ("Toledo.", "Hyannis Port, Mass. Kennedy and Macmillan ..."), else a place after "at" or "in" ("At Geneva",
    "in Saigon"), the first; None where neither names one ZONES knows (STYLE 4)."""
    lead = re.split(r"(?<=[a-z])\.\s|:\s", c, maxsplit=1)[0]
    if len(lead) <= 40:
        z = zone_of(lead)
        if z:
            return (z, lead)
    best = None
    for rx, z in ZONES:
        m = re.search(r"\b(?:[Aa]t|[Ii]n|[Ff]rom)\s+(?:the\s+)?(?:" + rx + ")", c)
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), z, m.group(0))
    return (best[1], best[2]) if best else None


def load_daybook():
    frus, prde, mc = {}, {}, {}
    for f in glob.glob(os.path.join(ROOT, "daybook", "*.yaml")):
        if not re.search(r"\d{4}-\d{2}\.yaml$", f):
            continue
        for r in (store.load_yaml(f) or {}).get("docs") or []:
            if r.get("src") == "frus" and r.get("time"):
                frus[r["key"][5:]] = r
    for f in glob.glob(os.path.join(ROOT, "daybook", "recordings", "*.yaml")):
        d = store.load_yaml(f) or {}
        for r in d.get("docs") or []:
            if not r.get("time"):
                continue
            if r.get("src") == "prde":
                prde[r["url"].rstrip("/").rsplit("/", 1)[1]] = r
            elif str(r.get("key", "")).startswith("mc:"):
                mc[r["url"].split("secret-white-house-tapes/")[1].rstrip("/")] = r
    return frus, prde, mc


PPP_AT = re.compile(r"[^.]*?\bat (about )?([\dIlioO]{1,2})(?:[:.]([\dIlioOS]{2}))? ?(a\.\s?m\.|p\.\s?m\.)[^.]*\.?")
PPP_OCLOCK = re.compile(r"[^.]*?\bat (about )?([\dIlioO]{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
                        r" ?o['’]clock\b[^.]*\.?", re.I)
WORDS = {w: i + 1 for i, w in enumerate("one two three four five six seven eight nine ten eleven twelve".split())}
OCR = str.maketrans({"I": "1", "l": "1", "i": "1", "o": "0", "O": "0", "S": "5"})
MONTHS = r"(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2})"
MONTH_N = {m: i + 1 for i, m in enumerate("January February March April May June July August September October November "
                                          "December".split())}


def ppp_hour(t, idate):
    """The first hour an item's note gives, (sentence, approx, 'HH:MM', check) or None: "at 7:40 p.m.", "at io a.m."
    (the OCR's), "at 4 o'clock" (a.m. or p.m. by the sentence's "morning", "afternoon", "evening", else by the hour, a
    check). A sentence naming another day is not the item's."""
    for rx in (PPP_AT, PPP_OCLOCK):
        m = rx.search(t)
        if not m:
            continue
        sent = m.group(0).strip()
        for mo, dd in re.findall(MONTHS, sent):
            if idate and len(str(idate)) == 10 and (MONTH_N[mo], int(dd)) != (int(str(idate)[5:7]), int(str(idate)[8:10])):
                return None
        g = m.group(2).lower()
        h = WORDS.get(g) or (int(g.translate(OCR)) if g.translate(OCR).isdigit() else 0)
        mi = int((m.group(3) or "0").translate(OCR)) if rx is PPP_AT and (m.group(3) or "0").translate(OCR).isdigit() else 0
        if not 1 <= h <= 12 or mi > 59:
            return None
        check = None
        if rx is PPP_AT:
            pm = m.group(4).startswith("p")
        elif re.search(r"evening|afternoon|night|p\.m\.", sent, re.I):
            pm = True
        elif re.search(r"morning|a\.m\.", sent, re.I):
            pm = False
        else:
            pm = h < 8 or h == 12
            check = "a.m. or p.m. not printed: " + ("p.m." if pm else "a.m.") + " by the hour"
        h = (h % 12) + (12 if pm else 0)
        return sent, bool(m.group(1)), f"{h:02d}:{mi:02d}", check
    return None


def load_ppp():
    """{package: {"page": {printed page: [item]}, "pdf": [item]}}: every item, with the hour its note gives (the
    "NOTE:" after the text, kind n; the editors' bracketed lines, kind b: "[Delivered from the President's office at 8
    p.m.]"), or none."""
    import json
    import lzma
    out = {}
    for f in glob.glob(os.path.join(ROOT, "sources", "ppp-text", "PPP-*.json.xz")):
        d = json.load(lzma.open(f))
        idx = out.setdefault(d["package"], {"page": {}, "pdf": []})
        for it in d["items"]:
            hour = None
            for kind, t in it.get("text") or []:
                if kind in ("n", "b"):
                    hour = ppp_hour(t, it.get("date"))
                    if hour:
                        break
            row = {"pdf": it.get("pdf"), "pdf_to": it.get("pdf_to") or it.get("pdf"), "date": it.get("date"),
                   "page": it.get("page"), "title": it.get("title") or "", "hour": hour}
            idx["page"].setdefault(it.get("page"), []).append(row)
            idx["pdf"].append(row)
    return out


PPP_LINK = re.compile(r"\[(\d{4}(?:[–-]\d{2})? Pub\. Papers (\d+))\]\([^)]*?(PPP-\d{4}-book\d)\.pdf#page=(\d+)\)")


def ppp_items(n, ppp, day):
    """The items the note's Public Papers links cite: by the cite's printed page (the item's first page), else by the
    PDF page and the entry's day."""
    out, seen = [], set()
    for cite, ppage, pkg, pdf in PPP_LINK.findall(n):
        idx = ppp.get(pkg)
        if not idx:
            continue
        its = [i for i in idx["page"].get(int(ppage), []) if i["pdf"] and i["pdf"] <= int(pdf) <= i["pdf_to"]]
        if len(its) > 1:
            its = [i for i in its if str(i["date"]) == day] or its[:0]
        for i in its:
            if id(i) not in seen:
                seen.add(id(i))
                out.append((pkg, cite, i))
    for pkg, pdf in re.findall(r"(PPP-\d{4}-book\d)\.pdf#page=(\d+)\)", n):
        if any(p == pkg and i["pdf"] <= int(pdf) <= i["pdf_to"] for p, _, i in out):
            continue
        its = [i for i in (ppp.get(pkg) or {}).get("pdf", []) if i["pdf"] and i["pdf"] <= int(pdf) <= i["pdf_to"]
               and str(i["date"]) == day]
        if len(its) == 1:
            out.append((pkg, f"{pkg}, PDF p. {pdf}", its[0]))
    return out


def main():
    s = store.Series(ROOT)
    frus, prde, mc = load_daybook()
    ppp = load_ppp()
    data = tiers.load()
    out, counts = [], {"rec": 0, "frus": 0, "ppp": 0, "text": 0, **{k: 0 for k in tiers.SOURCES}}
    for _, e in s.lists["cal"].entries():
        day = str(e.get("date", ""))
        if len(day) != 10 or e.get("time"):
            continue
        c = e.get("c") or ""
        c = " ".join(c) if isinstance(c, list) else str(c)
        n = str(e.get("n") or "")
        props = []
        for slug in re.findall(r"millercenter\.org/the-presidency/secret-white-house-tapes/([^)\s/]+)", n):
            r = mc.get(slug)
            if r and str(r.get("date")) == day:
                props.append(("rec", str(r["time"]), DC, False, f"Miller Center, {r['url']}", False))
        for num in re.findall(r"prde\.upress\.virginia\.edu/conversations/(\d+)", n):
            r = prde.get(num)
            if r and str(r.get("date")) == day:
                z = TEXAS if re.search(r"Ranch|Austin|Texas", str(r.get("place") or "")) else DC
                props.append(("rec", str(r["time"]), z, False, f"PRDE {num} ({r.get('place') or 'place not given'})", False))
        for doc in re.findall(r"historicaldocuments/(frus[^/)\s]+/d\d+)", n):
            r = frus.get(doc)
            if r and str(r.get("date")) == day:
                props.append(("frus", str(r["time"]), "Etc/GMT+5", False,
                              f"{r.get('cite')}: {r.get('title', '')[:90]} (the TEI stamp's clock, UTC-5)", True))
        for pkg, cite, it in ppp_items(n, ppp, day):
            if it["hour"] and str(it["date"]) == day:
                sent, approx, hh, check = it["hour"]
                z, zc = place_zone(sent)
                props.append(("ppp", hh, z, approx, f"{pkg}, p. {it['page']}: {sent[:140]}", zc,
                              {"check": check} if check else {}))
        for m in HOUR.finditer(c):
            approx = bool(m.group(1) or m.group(5))
            if m.group(6):
                hh = "12:00" if m.group(6).lower() == "noon" else "00:00"
            else:
                h, mi = int(m.group(2)), int(m.group(3) or 0)
                if h > 12 or mi > 59:
                    continue
                h = (h % 12) + (12 if m.group(4).lower() == "p.m." else 0)
                hh = f"{h:02d}:{mi:02d}"
            z, zc = place_zone(c)
            props.append(("text", hh, z, approx, f"the entry's text: {m.group(0)!r}", zc))
        props += tiers.proposals(e, day, c, n, data, place_zone, real_zone)
        seen = set()
        for src, hh, z, approx, basis, zc, *more in props:
            extra = more[0] if more else {}
            d = extra.pop("day", day)
            zone, dst = real_zone(z, d)
            if (src, hh, zone, basis if src in tiers.SOURCES else "") in seen:
                continue
            seen.add((src, hh, zone, basis if src in tiers.SOURCES else ""))
            try:
                utc = to_utc(d, hh, zone)
            except (ValueError, zoneinfo.ZoneInfoNotFoundError):
                continue
            row = {"id": e["id"], "local": hh, "zone": zone, "time": utc, "source": src, "basis": basis}
            if approx:
                row["approx"] = True
            if zc or dst:
                row["zone_check"] = True
            row.update({k: v for k, v in extra.items() if v is not None})
            out.append(row)
            counts[src] = counts.get(src, 0) + 1
    out.sort(key=lambda r: (r["id"], r["source"]))
    path = os.path.join(ROOT, "notes", "times-proposals.yaml")
    store.dump_yaml({"proposals": out}, path, header=[
        "Generated by tools/times/propose.py: times of day proposed for the calendar's entries, for review (its STYLE).",
        "Never edit; move a proposal into its entry (time, time_approx) by patch, its source in the note."])
    ids = len({r["id"] for r in out})
    print(f"{len(out)} proposals for {ids} entries: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
    by = {}
    for r in out:
        by.setdefault(r["source"], {}).setdefault(r["id"][4:8], 0)
        by[r["source"]][r["id"][4:8]] += 1
    for src in sorted(by):
        print(f"  {src}: " + ", ".join(f"{y} {k}" for y, k in sorted(by[src].items())))


if __name__ == "__main__":
    main()
