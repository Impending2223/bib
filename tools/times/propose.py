"""Times of day: proposals for review, never written into the entries (the owner, Oct. 30, 2026: "Do we have anyone to
do a pass over the entries that might have a time of day and get them started?"; the hand-off of Nov. 1, item 0c).

    python3 -I tools/times/propose.py            writes notes/times-proposals.yaml and prints the counts

The mechanical tier (no agents), for each calendar entry dated to a day:
  rec   a White House recording the note cites (the Miller Center's page, or PRDE's), its catalogued time; the zone
        by PRDE's place (the LBJ Ranch and Austin, Central; elsewhere Washington, Eastern)
  frus  a FRUS document the note cites, the time the daybook keeps for it (frus:doc-dateTime-min); the zone is
        Washington's unless confirmed (the daybook keeps the TEI stamp's clock as written, not its offset: re-read
        the stamp, `frus:doc-dateTime-min`, before taking one): a cable's time is its sending, a memorandum of conversation the meeting's, so
        the proposal holds only where the entry is the meeting or the paper
  text  an hour the entry's own `c` names ("at 12:30 p.m.", "noon"); Washington's zone unless the entry names a place
        this file knows (ZONES), else `zone_check: true`

STYLE
1. A proposal: id, local time as the source gives it, zone (IANA), the UTC instant (zoneinfo, the 1960s rules: the
   States' daylight time as each zone's history records it), approx (where the source rounds or says "about"), source,
   basis (the cite), zone_check where the zone is a guess. Several for an entry: all kept, the reviewer picks.
2. The reviewer moves a proposal into the entry (`time`, `time_approx`) by patch, the source in the note. The file is
   regenerated; never edited by hand.
3. Not yet: the Public Papers' hours (the items' notes, "at 4 p.m."), the Congress's hours (the Daily Digest), the war's
   date-time groups, launches and tests, the Security Council (the hand-off's tiers 2-4).
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

DC = "America/New_York"
ZONES = [  # a place the entry names -> its zone (first match in `c`)
    (r"\bSaigon\b|South Vietnam|\bHuế\b|Đà Nẵng|Khe Sanh", "Asia/Ho_Chi_Minh"),   # zoneinfo: +8 in 1959-75
    (r"\bHanoi\b|North Vietnam|Haiphong", "Asia/Bangkok"),                         # +7
    (r"\bMoscow\b|\bKremlin\b", "Europe/Moscow"),
    (r"\bBerlin\b", "Europe/Berlin"), (r"\bParis\b", "Europe/Paris"), (r"\bLondon\b", "Europe/London"),
    (r"\bHavana\b", "America/Havana"), (r"\bVienna\b", "Europe/Vienna"), (r"\bGeneva\b", "Europe/Zurich"),
    (r"\bTokyo\b", "Asia/Tokyo"), (r"\bManila\b", "Asia/Manila"), (r"\bHonolulu\b", "Pacific/Honolulu"),
    (r"\bDallas\b|\bAustin\b|\bJohnson City\b|LBJ Ranch|\bthe Ranch\b|\bHouston\b|\bChicago\b|\bMemphis\b|\bSelma\b|"
     r"\bMontgomery\b|\bBirmingham\b|\bOxford, Miss|\bJackson, Miss|\bNew Orleans\b", "America/Chicago"),
    (r"\bLos Angeles\b|\bSan Francisco\b|\bWatts\b|\bBerkeley\b|\bOakland\b|\bSacramento\b", "America/Los_Angeles"),
    (r"\bDenver\b", "America/Denver"),
    (r"\bWashington\b|White House|Oval Office|\bthe Capitol\b|\bNew York\b|\bBoston\b|\bAtlantic City\b|\bMiami\b", DC),
]
HOUR = re.compile(r"\b(?:(about|around|some|shortly after|shortly before|near|nearly|by)\s+)?(\d{1,2})(?:[:.](\d{2}))?\s*"
                  r"(a\.m\.|p\.m\.)|\b(?:(about|around)\s+)?(noon|midnight)\b", re.I)


def to_utc(day, hhmm, zone):
    h, m = map(int, hhmm.split(":"))
    local = datetime.datetime.combine(datetime.date.fromisoformat(day), datetime.time(h % 24, m),
                                      tzinfo=zoneinfo.ZoneInfo(zone))
    return local.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def zone_of(text):
    for rx, z in ZONES:
        if re.search(rx, text):
            return z
    return None


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


def main():
    s = store.Series(ROOT)
    frus, prde, mc = load_daybook()
    out, counts = [], {"rec": 0, "frus": 0, "text": 0}
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
                z = "America/Chicago" if re.search(r"Ranch|Austin|Texas", str(r.get("place") or "")) else DC
                props.append(("rec", str(r["time"]), z, False, f"PRDE {num} ({r.get('place') or 'place not given'})", False))
        for doc in re.findall(r"historicaldocuments/(frus[^/)\s]+/d\d+)", n):
            r = frus.get(doc)
            if r and str(r.get("date")) == day:
                z = zone_of(c) or DC
                props.append(("frus", str(r["time"]), z, False, f"{r.get('cite')}: {r.get('title', '')[:90]}", True))
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
            z = zone_of(c)
            props.append(("text", hh, z or DC, approx, f"the entry's text: {m.group(0)!r}", z is None))
        seen = set()
        for src, hh, z, approx, basis, zc in props:
            if (src, hh, z) in seen:
                continue
            seen.add((src, hh, z))
            try:
                utc = to_utc(day, hh, z)
            except (ValueError, zoneinfo.ZoneInfoNotFoundError):
                continue
            row = {"id": e["id"], "local": hh, "zone": z, "time": utc, "source": src, "basis": basis}
            if approx:
                row["approx"] = True
            if zc:
                row["zone_check"] = True
            out.append(row)
            counts[src] += 1
    out.sort(key=lambda r: (r["id"], r["source"]))
    path = os.path.join(ROOT, "notes", "times-proposals.yaml")
    store.dump_yaml({"proposals": out}, path, header=[
        "Generated by tools/times/propose.py: times of day proposed for the calendar's entries, for review (its STYLE).",
        "Never edit; move a proposal into its entry (time, time_approx) by patch, its source in the note."])
    ids = len({r["id"] for r in out})
    print(f"{len(out)} proposals for {ids} entries: " + ", ".join(f"{k} {v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
