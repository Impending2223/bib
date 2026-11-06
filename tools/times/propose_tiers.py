"""The tiers of propose.py read once from their sources (tools/times/tiers.py writes tools/times/data/<tier>.json):
congress, dtg, launch, test, unsc. Their rules are propose.py's docstring and STYLE 3-4; this module only applies them.
Each proposal: (source, 'HH:MM' local, zone, approx, basis, zone_check, {extra fields}).
"""
import datetime
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
SOURCES = ("congress", "dtg", "launch", "test", "unsc")
DC = "America/New_York"
MON = {m: i + 1 for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def load():
    out = {}
    for t in ("digest", "unsc", "launches", "tests"):
        path = os.path.join(DATA, t + ".json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                out[t] = json.load(f)
    if "digest" in out:                                  # by the legislative day the Digest heads
        by_day = {}
        for rows in out["digest"]["by_date"].values():
            for r in rows:
                by_day.setdefault(r["day"], []).append(r)
        out["digest_day"] = by_day
    if "unsc" in out:
        by = {}
        for m in out["unsc"]["meetings"]:
            by.setdefault(m["date"], []).append(m)
        out["unsc_day"] = by
    if "launches" in out:
        by = {}
        for r in out["launches"]["ksc"]:
            by.setdefault(r["date"], []).append(r)
        out["ksc_day"] = by
        by = {}
        for r in out["launches"]["chronology"]:
            by.setdefault(r["date"], []).append(r)
        out["chron_day"] = by
    if "tests" in out:
        by = {}
        for r in out["tests"]["tests"]:
            by.setdefault(r["date"], []).append(r)
        out["test_day"] = by
    return out


def threads(e):
    return {e.get("thread") or ""} | set(e.get("also") or [])


def shift(day, k):
    return (datetime.date.fromisoformat(day) + datetime.timedelta(days=k)).isoformat()


# ------------------------------------------------------------------------------------------------------ congress

CHAMBER_ACT = re.compile(
    r"(?<!White )\b(Senate|House)(?: of Representatives)?\b(?:,? \d{1,3}[ –-]to[ –-]\d{1,3},?)?\s+"
    r"(?:again |also |then |finally |unanimously |narrowly |quickly |overwhelmingly |at last |formally )?"
    r"(passes|passed|votes|approves|adopts|rejects|confirms|consents|ratifies|kills|tables|recommits|defeats|"
    r"overrides|sustains|invokes|refuses|agrees|concurs|clears|accepts|condemns|censures|seats|expels|elects|"
    r"convenes|adjourns|reconvenes|recesses|debates|takes up|begins|gives|advises|fails|strikes|amends|sends|"
    r"completes|cuts|restores|turns down|denies|upholds|returns|insists|recedes|meets|opens|closes|ends)\b")
CLOTURE = re.compile(r"\bcloture\b", re.I)


STATES = re.compile(r"(Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|"
                    r"Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|"
                    r"Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|Hampshire|Jersey|Mexico|York|Carolina|"
                    r"Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|Tennessee|Texas|Utah|Vermont|Virginia|"
                    r"Washington|Wisconsin|Wyoming|[Ss]tate|lower|upper|[Ll]egislature|General Assembly)('s)?\s+$")


def congress(e, day, c, n, data):
    rows = data.get("digest_day", {}).get(day)
    if not rows:
        return []
    # a State's legislature is not the Congress: an entry on the States, or a chamber its State names
    if any(str(t).startswith("state:") for t in e.get("tags") or []) or "states" in (e.get("thread") or "") \
            or re.match(r"^[A-Z][a-z]+(?: [A-Z][a-z]+)?, [A-Z][a-z]{1,4}\.", c):
        if not re.search(r"\bCongress\b|\bU\.S\. (?:Senate|House)|\bin Washington\b", c):
            return []
    acts = {}
    for m in CHAMBER_ACT.finditer(c):
        if STATES.search(c[max(0, m.start() - 30):m.start()]):
            continue
        acts.setdefault("S" if m.group(1) == "Senate" else "H", set()).add(m.group(2))
    if CLOTURE.search(c) and "S" not in acts and re.search(r"\bSenate\b", c):
        acts["S"] = {"cloture"}
    out = []
    for ch, verbs in sorted(acts.items()):
        name = "Senate" if ch == "S" else "House"
        mine = [r for r in rows if r["ch"] == ch]
        close = [r for r in mine if r["kind"] in ("adjourned", "recessed")]
        met = [r for r in mine if r["kind"] in ("met", "reconvened")]
        cite = lambda r: (f"Daily Digest, {r['folio'] or 'PDF p. ' + str(r['pdf'])}: {name}, "  # noqa: E731
                          f"\"{r['raw']}\"")
        if verbs & {"adjourns", "recesses", "closes", "ends"}:
            for r in close:
                out.append(("congress", r["local"], DC, False, cite(r) + " (the entry is the adjournment)", False,
                            {"role": "adjourned", "url": r["url"], "day": r["date"]}))
            continue
        if verbs & {"convenes", "reconvenes", "meets", "opens"}:
            for r in met:
                out.append(("congress", r["local"], DC, False, cite(r) + " (the entry is the meeting)", False,
                            {"role": "met", "url": r["url"], "day": r["date"]}))
            if met:
                continue
        for r in close:
            out.append(("congress", r["local"], DC, False,
                        cite(r) + f" (the {name}'s act before it; the Digest gives no hour of the act)", False,
                        {"role": "before", "bound": True, "url": r["url"], "day": r["date"]}))
    return out


# ----------------------------------------------------------------------------------------------------------- dtg

DTG = re.compile(r"\b([0-3]\d)([0-2]\d)([0-5]\d)\s?Z\b(?:\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept?|Oct|Nov|Dec)[a-z]*\.?"
                 r"(?:\s*(\d{4}|\d{2})\b)?)?")
MIL = re.compile(r"\b(?:at |by |of |from |until )?([0-2]\d)([0-5]\d)\s?(H|hours|Saigon time|GMT|Z)\b(?:,?\s*("
                 + "|".join(m[:3] for m in MONTHS) + r")[a-z]*\.?\s+(\d{1,2})\b)?")


def dtg(e, day, c, n, data, place_zone, real_zone):
    import zoneinfo
    out = []
    y0, m0 = int(day[:4]), int(day[5:7])
    zkey, _ = place_zone(c)
    zones = {real_zone(zkey, day)[0], DC}
    for m in DTG.finditer(n):
        dd, hh, mi = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if hh > 23 or not 1 <= dd <= 31:
            continue
        mo = MON.get((m.group(4) or "")[:3], m0)
        yr = int(m.group(5)) if m.group(5) else y0
        if yr < 100:
            yr += 1900
        if not m.group(4) and dd > int(day[8:]) + 1:          # no month given: the month before
            mo, yr = (12, yr - 1) if m0 == 1 else (m0 - 1, yr)
        try:
            at = datetime.datetime(yr, mo, dd, hh, mi, tzinfo=datetime.timezone.utc)
        except ValueError:
            continue
        if not any(at.astimezone(zoneinfo.ZoneInfo(z)).date().isoformat() == day for z in zones):
            continue
        before = n[:m.start()]
        st = max(before.rfind("; "), before.rfind("("), before.rfind(": "), before.rfind(". "))
        msg = (before[st + 1:].strip(" ;(:.") + " " + m.group(0)).strip()
        tc = before.rfind("To check:")
        unread = tc >= 0 and not re.search(r"\.\s+(?:See|Names|Check|Made public|Reply|Bibliography)\b|\]\]\.\s", before[tc:])
        out.append(("dtg", f"{hh:02d}:{mi:02d}", "Etc/UTC", False,
                    f"the note's message, {msg[-110:]} (DTG, Zulu: the sending)", False,
                    {"unread": True if unread else None, "day": at.date().isoformat()}))
    for m in MIL.finditer(c):
        hh, mi, z = int(m.group(1)), int(m.group(2)), m.group(3)
        if hh > 23:
            continue
        if m.group(4):
            try:
                if datetime.date(int(day[:4]), MON[m.group(4)[:3]], int(m.group(5))).isoformat() != day:
                    continue
            except (ValueError, KeyError):
                continue
        zone, zc = {"H": ("Etc/GMT-8", False), "Saigon time": ("Asia/Ho_Chi_Minh", False), "GMT": ("Etc/UTC", False),
                    "Z": ("Etc/UTC", False)}.get(z, (zkey, True))
        out.append(("dtg", f"{hh:02d}:{mi:02d}", zone, False,
                    f"the entry's text: {m.group(0).strip()!r}" + (" (H: Hotel, UTC+8)" if z == "H" else ""), zc, {}))
    return out


# -------------------------------------------------------------------------------------------------------- launch

SPACE = {"space", "space-apollo", "soviet-union-space"}
LAUNCH_WORDS = re.compile(r"\blaunch|\borbit|suborbital|\blifts? off|\bflight\b|\bfired\b|\bshot\b", re.I)
GENERIC = {"the", "mercury", "first", "nasa", "project", "test", "flight", "launch", "satellite", "and", "with"}


def words(t):
    return {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z-]{2,}", t)}


def launch(e, day, c, n, data):
    if not (threads(e) & SPACE) or not LAUNCH_WORDS.search(c):
        return []
    out = []
    ks = data.get("ksc_day", {}).get(day, [])
    cw = words(c)
    hits = []
    for r in ks:
        nm = {w for w in words(r["name"]) if w not in GENERIC}
        people = {w.lower() for w in re.findall(r"\b([A-Z][a-z]{3,})\b", r["remarks"])} - GENERIC
        why = (nm & cw) or (people & cw & {w.lower() for w in re.findall(r"\b[A-Z][a-z]{3,}\b", c)})
        if why:
            hits.append((r, None))
    if not hits and len(ks) == 1:
        hits = [(ks[0], "date")]
    for r, match in hits:
        out.append(("launch", r["local"], r["zone"], False,
                    f"KSC, Summary of Major NASA Launchings (1973), PDF p. {r['pdf']}: {r['name']}, {r['printed']}", False,
                    {"url": r["url"], "match": match, "cited": False if "19740015280" not in n else None}))
    if not hits:
        caps = {w.lower() for w in re.findall(r"\b[A-Z][A-Za-z]{3,}\b", c)} - GENERIC
        for r in data.get("chron_day", {}).get(day, []):
            if caps & words(r["sentence"]):
                out.append(("launch", r["local"], r["zone"], False,
                            f"Astronautics and Aeronautics, {r['chronology']}, PDF p. {r['pdf']}: {r['sentence'][:140]}",
                            False, {"url": r["url"], "cited": False if r["url"].split("#")[0].rsplit("/", 1)[1] not in n
                                    else None}))
    return out


# ---------------------------------------------------------------------------------------------------------- test

TESTING = {"testing", "testing-missile-talks"}
TEST_WORDS = re.compile(r"detonat|explo|kiloton|megaton|\bshot\b|first\b.{0,40}?\btest\b|\b(?:an?|the) [^.]{0,30}"
                        r"\btest of\b|series begins|testing resumes|\bburst\b", re.I)
US_TEST = re.compile(r"\bUnited States\b|\bU\.S\.|\bAmerican\b|\bNevada\b|Christmas Island|Johnston|\bPacific\b|"
                     r"Amchitka|\bunderground\b|Plowshare|Dominic|Starfish|Sedan|Gnome|Bluegill|Kingfish|Checkmate|"
                     r"Frigate Bird|Swordfish|Long Shot|Milrow|Boxcar|Faultless|Gasbuggy", re.I)
OTHER_TEST = re.compile(r"\bSoviet|\bFrench\b|\bFrance\b|\bChin(a|ese)\b|\bBritish\b|\bKhrushchev\b|\btreaty\b", re.I)


def test(e, day, c, n, data):
    if not (threads(e) & TESTING) or not TEST_WORDS.search(c) or not US_TEST.search(c) or OTHER_TEST.search(c):
        return []
    td = data.get("test_day", {})
    cand = [r for k in (-1, 0, 1) for r in td.get(shift(day, k), [])]
    cw = words(c)
    pages = {int(p) for p in re.findall(r"osti\.gov/servlets/purl/1351809#page=(\d+)", n)}
    out = []
    named = [r for r in cand if any(w in cw for x in r["names"] for w in words(x.replace("", ""))
                                    if len(w) > 3 and w not in {"accidental", "release", "radioactivity", "detected",
                                                               "onsite", "offsite", "only", "drillback", "venting",
                                                               "first", "test", "underground", "surface", "crater"})]
    if named:
        hits = [(r, None) for r in named]
    else:
        import zoneinfo
        la = zoneinfo.ZoneInfo("America/Los_Angeles")
        same = [r for r in cand if re.search(r"NNSS|NTTR|Nevada", r["location"] + " " + r.get("place", ""))]
        same = [r for r in same if datetime.datetime.fromisoformat(r["date"] + "T" + r["utc"]).replace(
            tzinfo=datetime.timezone.utc).astimezone(la).date().isoformat() == day]
        if pages:
            same = [r for r in same if r["pdf"] in pages] or same
        hits = [(same[0], "date")] if len(same) == 1 else []
    for r, match in hits:
        out.append(("test", r["utc"][:5], "Etc/UTC", False,
                    f"DOE/NV-209 Rev. 16 (2015), PDF p. {r['pdf']}: no. {r['no']}, {r['date']} {r['utc']} GMT, "
                    f"{r['location'] or r.get('place', '')}, {r['type']}", "NNSS" in r["location"] and False,
                    {"url": r["url"], "match": match, "cited": False if r["pdf"] not in pages else None,
                     "day": r["date"]}))
    return out


# ---------------------------------------------------------------------------------------------------------- unsc

UNSC_RX = re.compile(r"Security Council|S/RES|S/PV")


def unsc(e, day, c, n, data):
    if not UNSC_RX.search(c + " " + n):
        return []
    ms = data.get("unsc_day", {}).get(day, [])
    res = set(re.findall(r"S/RES/(\d+)", n))
    pick = [m for m in ms if res & set(m.get("resolutions") or [])]
    match = "resolution" if pick else "date"
    out = []
    for m in (pick or ms):
        t = m.get("called") or m.get("held")
        if not t:
            continue
        txt = m.get("called_text") or m.get("held_text")
        out.append(("unsc", t, DC, False, f"{m['symbol']}: \"{txt}\"" + (f"; \"{m['rose_text']}\"" if m.get("rose") else ""),
                    False, {"role": "met", "until": m.get("rose"), "url": m["url"], "match": match,
                            "cited": None if m["symbol"] in n else False}))
    return out


def proposals(e, day, c, n, data, place_zone, real_zone):
    out = []
    out += congress(e, day, c, n, data)
    out += dtg(e, day, c, n, data, place_zone, real_zone)
    out += launch(e, day, c, n, data)
    out += test(e, day, c, n, data)
    out += unsc(e, day, c, n, data)
    return out
