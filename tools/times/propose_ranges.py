"""Time ranges: proposals for review, never written into the entries (the owner's ruling, Nov. 5, 2026: "Yes, add the
ranges and sort by time first"; dayorder STYLE 5-6).

    python3 -I tools/times/propose_ranges.py     writes notes/times-ranges.yaml and prints the counts
    (python3 -I tools/times/propose.py --ranges  runs it after the times)

For each calendar entry dated to a day with neither `time` nor `time_range`, the span of the day the record places
its event in, where it gives no hour, as `time_range: [from, to]` in UTC. The tiers, each a `source`:

  congress  a chamber's floor act on its day (the entry's first sentence names the chamber with a verb of the floor:
        "Senate passes", "House, 289 to 126, ...", "passed by the House", a speech "on the Senate floor"; not a
        signing, a message, a committee's meeting, a State's legislature): from the hour the chamber met to the hour
        it adjourned or recessed, both from the Daily Digest (tools/times/data/digest.json, tiers.py's reading),
        Eastern time. The hour it met: the Digest's "Senate met at 10 a.m." for the day; else the last order the
        Digest prints for the day ("adjourn until 10 a.m. Monday, February 14"); else the session's standing order
        (noon, "unless otherwise ordered"), with a `check`, since an order the reader missed would make it earlier;
        none where the Digest gives the committees leave to sit while the chamber is in session before noon that
        day and no order gives the hour. A met hour after the closing one is a misreading: no range.
  words  a word in the entry's first sentence (outside quotations and italic titles) that places the event in its
        day (WORDS: "before dawn", "early morning", "morning", "breakfast", "midday", "lunch", "afternoon",
        "evening", "dinner", "that night", "late that night", "after midnight", "overnight", ...), or such a word in a
        short parenthetical the note sets after a work read and pinpointed ("[[w.x]], 123 (that evening)"); not a
        word tied to another day ("next morning", "Sunday evening" of a Saturday's entry, "the night of Oct. 5" of
        another date), nor in "lunch counter", "morning business", "evening newspaper", "Evening Star". Two
        different spans in the sentence: two acts, none taken. The span is a band of dayorder's BANDS where one
        fits the word (`time_band`), else the word's own span (`span`, local hours, past 24 the next day's); in the
        zone of the place the event happened (ZONE below), `time_zone`.
  clocks  the hours the round-1 and round-2 times reviewers refused only because the clock was in doubt (a place
        whose 1960s daylight time is not settled; two clocks, the entry not saying whose): the range from the
        earlier reading to the later, the reviewer's reason the basis (tools/times/data/clocks.yaml, by hand).
  ppp   an item of the Public Papers the note cites, of the entry's day, whose NOTE gives a band word and no hour
        ("The President spoke in the afternoon on the South Lawn"): the word's span, the zone the sentence's place.

ZONE (the place where the event happened, propose.py STYLE 4): the entry's place tags in Indochina (`place:`,
`province:`; the Republic, UTC+8; the North, Laos and Cambodia, UTC+7); else the place the entry's first sentence
opens with, or sets after "at" or "in", else after "from" (event_place: propose.ZONES, MORE, a town with the
Bluebook's State, "Hershey, Pa.", US_CITIES, a country opening the sentence, COUNTRIES); else its one city's or
State's tag (`city:`, `state:`); else
Washington's, with zone_check, and none at all for the Vietnam threads, where Washington and Saigon are twelve hours
apart. Texas before 1967 is UTC-6 all year. A clock in doubt (propose.py's UNSURE places; any city or State but
those whose practice zoneinfo records, before the Uniform Time Act took effect in 1967, April to October): the range
covers both readings, standard and daylight, an hour wider, zone_check.

STYLE
1. A row: id, time_range [from, to] (UTC, '1964-06-10T14:00Z'), source, basis (the words or the record, with its page
   or link), and as they apply: time_band and time_zone (a band, dayorder.band_range's own range unless the clock is
   in doubt), span (a word's own local hours, no band fitting it), time_zone, zone_check (the zone a guess, or two
   readings), readings (the zones the range covers), check (what the reviewer should settle), url, has_time
   (a proposal for this entry in notes/times-proposals.yaml: an exact hour may be had). Several for an entry: all
   kept, the reviewer picks; the narrowest is the likeliest.
2. The reviewer moves a range into the entry (`time_range`, `time_band`, `time_zone`) by patch, its basis in the note.
   The file is regenerated whole; never edited by hand. No network: it reads the tree, the tiers' data
   (tools/times/data/) and sources/ppp-text/.
"""
import datetime
import glob
import json
import lzma
import os
import re
import sys
import zoneinfo

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from tools.bib import store  # noqa: E402
from tools.bib.dayorder import BANDS  # noqa: E402
from tools.bib.claims import units  # noqa: E402
from tools.times import propose  # noqa: E402
from tools.times import propose_tiers as tiers  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
DC = "America/New_York"
OUT = os.path.join(ROOT, "notes", "times-ranges.yaml")
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
VIETNAM = re.compile(r"^(vietnam|laos|cambodia|thailand)")

# ------------------------------------------------------------------------------------------------------- zones

INDOCHINA = {"vn-south": "Asia/Ho_Chi_Minh", "vn-north": "Asia/Bangkok", "laos": "Asia/Vientiane",
             "cambodia": "Asia/Phnom_Penh"}
# A State's zone; `True` where zoneinfo's zone is the State's own 1960s practice (no doubt of its daylight time).
STATE = {
    "dc": (DC, True), "ny": (DC, True), "nj": (DC, False), "pa": (DC, False), "ct": (DC, False), "ma": (DC, False),
    "ri": (DC, False), "nh": (DC, False), "vt": (DC, False), "me": (DC, False), "de": (DC, False), "md": (DC, False),
    "va": (DC, False), "wv": (DC, False), "nc": (DC, False), "sc": (DC, False), "ga": (DC, False), "fl": (DC, False),
    "oh": (DC, False), "mi": ("America/Detroit", True), "in": ("America/Indiana/Indianapolis", True),
    "ky": ("America/Kentucky/Louisville", False), "tn": ("America/Chicago", False), "al": ("America/Chicago", False),
    "ms": ("America/Chicago", False), "la": ("America/Chicago", False), "ar": ("America/Chicago", False),
    "mo": ("America/Chicago", False), "il": ("America/Chicago", True), "wi": ("America/Chicago", False),
    "mn": ("America/Chicago", False), "ia": ("America/Chicago", False), "ok": ("America/Chicago", False),
    "ks": ("America/Chicago", False), "ne": ("America/Chicago", False), "sd": ("America/Chicago", False),
    "nd": ("America/Chicago", False), "tx": (propose.TEXAS, True), "mt": ("America/Denver", False),
    "wy": ("America/Denver", False), "co": ("America/Denver", False), "nm": ("America/Denver", False),
    "ut": ("America/Denver", False), "id": ("America/Boise", False), "az": ("America/Phoenix", True),
    "nv": ("America/Los_Angeles", False), "ca": ("America/Los_Angeles", True), "or": ("America/Los_Angeles", False),
    "wa": ("America/Los_Angeles", False), "ak": ("America/Anchorage", False), "hi": ("Pacific/Honolulu", True),
    "pr": ("America/Puerto_Rico", True),
}
CITY = {  # a city tag whose zone is settled by zoneinfo (the city's own history, or propose.py's ZONES)
    "nyc": DC, "washington": DC, "dc": DC, "boston": DC, "chicago": "America/Chicago",
    "los-angeles": "America/Los_Angeles", "san-francisco": "America/Los_Angeles", "oakland": "America/Los_Angeles",
    "berkeley": "America/Los_Angeles", "detroit": "America/Detroit", "louisville": "America/Kentucky/Louisville",
    "indianapolis": "America/Indiana/Indianapolis", "houston": propose.TEXAS, "dallas": propose.TEXAS,
}
STD = {DC: 5, "America/Detroit": 5, "America/Indiana/Indianapolis": 5, "America/Kentucky/Louisville": 5,
       "America/Chicago": 6, "America/Denver": 7, "America/Boise": 7, "America/Los_Angeles": 8,
       "America/Anchorage": 10}


def gazetteer():
    path = os.path.join(ROOT, "sources", "vn-provinces-1966", "places.json")
    rows = json.load(open(path, encoding="utf-8"))
    places = {r["id"]: r.get("country") for r in rows}
    provinces = {}
    for r in rows:
        provinces.setdefault(r.get("province"), set()).add(r.get("country"))
    return places, provinces


def zone_for(e, c, gaz):
    """(zone, zone_check, readings or None, how): the zone of the place where the entry's event happened (ZONE in the
    docstring); readings, two fixed offsets where the clock is in doubt; None where nothing honest places it."""
    tags = e.get("tags") or []
    day = str(e.get("date"))
    places, provinces = gaz
    cs = {places.get(t[6:]) for t in tags if t.startswith("place:")}
    cs |= {x for t in tags if t.startswith("province:") for x in provinces.get(t[9:], set())}
    cs = {INDOCHINA[x] for x in cs if x in INDOCHINA}
    if cs:
        offs = sorted({int(zoneinfo.ZoneInfo(z).utcoffset(datetime.datetime.fromisoformat(day + "T12:00"))
                           .total_seconds() // 3600) for z in cs})
        if len(offs) == 1:
            return sorted(cs)[0], False, None, "the entry's place tags"
        return sorted(cs)[0], True, [f"Etc/GMT-{o}" for o in offs], "the entry's place tags (two zones)"
    ep = event_place(c)
    if ep:
        key, words, st = ep
        how = f"the place in the entry's words ({words.strip()})"
        if st:
            return state_zone(st, day, how)
        zone, dst = propose.real_zone(key, day)
        if key == propose.SOUTH and day < "1967-01-01":
            return "America/Chicago", True, doubt("America/Chicago", day) or ["Etc/GMT+6"], how
        if propose.UNSURE.search(words) and day < "1967-01-01":
            return zone, True, doubt(zone, day), how
        return zone, bool(dst or propose.UNSURE.search(words)), None, how
    cities = {t[5:] for t in tags if t.startswith("city:")}
    states = {t[6:] for t in tags if t.startswith("state:")}
    if len(cities) == 1 and next(iter(cities)) in CITY:
        z = CITY[next(iter(cities))]
        return propose.real_zone(z, day)[0], False, None, f"the entry's city tag ({next(iter(cities))})"
    if len(states) == 1 and next(iter(states)) in STATE:
        st = next(iter(states))
        return state_zone(st, day, f"the entry's State tag ({st})")
    th = {e.get("thread") or ""} | set(e.get("also") or [])
    if any(VIETNAM.match(t) for t in th):
        return None, None, None, None
    return DC, True, None, "nothing places it: Washington's taken"


SPLIT = ("ky", "tn", "fl", "ks", "ne", "nd", "sd", "id", "or", "ak", "mi", "in", "tx")   # States of two zones


def state_zone(st, day, how):
    """A State's zone (STATE), the clock in doubt before 1967 where zoneinfo does not record its practice."""
    z, settled = STATE[st]
    if z == propose.TEXAS:
        return propose.real_zone(z, day)[0], False, None, how
    if settled or day >= "1967-01-01":
        return z, st in SPLIT, None, how
    return z, True, doubt(z, day), how


# Places propose.ZONES does not name, where an entry's event happens (zoneinfo's history for each).
MORE = [
    (r"\bLisbon\b", "Europe/Lisbon"), (r"\bMadrid\b", "Europe/Madrid"), (r"\bBrussels\b", "Europe/Brussels"),
    (r"\bThe Hague\b|\bAmsterdam\b", "Europe/Amsterdam"), (r"\bAthens\b(?!, Ga)(?!, Ohio)", "Europe/Athens"),
    (r"\bAnkara\b|\bIstanbul\b", "Europe/Istanbul"), (r"\bNicosia\b|\bCyprus\b", "Asia/Nicosia"),
    (r"\bBelgrade\b", "Europe/Belgrade"), (r"\bWarsaw\b", "Europe/Warsaw"), (r"\bPrague\b", "Europe/Prague"),
    (r"\bBudapest\b", "Europe/Budapest"), (r"\bBucharest\b", "Europe/Bucharest"), (r"\bStockholm\b", "Europe/Stockholm"),
    (r"\bOslo\b", "Europe/Oslo"), (r"\bCopenhagen\b", "Europe/Copenhagen"), (r"\bHelsinki\b", "Europe/Helsinki"),
    (r"\bCairo\b", "Africa/Cairo"), (r"\bTel Aviv\b|\bJerusalem\b", "Asia/Jerusalem"), (r"\bTehran\b", "Asia/Tehran"),
    (r"\bKarachi\b|\bRawalpindi\b", "Asia/Karachi"), (r"\bNew Delhi\b|\bDelhi\b|\bBombay\b", "Asia/Kolkata"),
    (r"\bTaipei\b", "Asia/Taipei"), (r"\bHong Kong\b", "Asia/Hong_Kong"), (r"\bDjakarta\b|\bJakarta\b", "Asia/Jakarta"),
    (r"\bVientiane\b", "Asia/Vientiane"), (r"\bPhnom Penh\b", "Asia/Phnom_Penh"), (r"\bRangoon\b", "Asia/Yangon"),
    (r"\bKuala Lumpur\b", "Asia/Kuala_Lumpur"), (r"\bSingapore\b", "Asia/Singapore"), (r"\bOkinawa\b", "Asia/Tokyo"),
    (r"\bGuam\b", "Pacific/Guam"), (r"\bL[ée]opoldville\b", "Africa/Kinshasa"), (r"\bAccra\b", "Africa/Accra"),
    (r"\bLagos\b", "Africa/Lagos"), (r"\bNairobi\b", "Africa/Nairobi"), (r"\bAddis Ababa\b", "Africa/Addis_Ababa"),
    (r"\bAlgiers\b", "Africa/Algiers"), (r"\bCaracas\b", "America/Caracas"), (r"\bBogot[aá]\b", "America/Bogota"),
    (r"\bLima\b", "America/Lima"), (r"\bSantiago\b", "America/Santiago"), (r"\bBuenos Aires\b", "America/Argentina/Buenos_Aires"),
    (r"\bMontevideo\b|\bPunta del Este\b", "America/Montevideo"), (r"\bSanto Domingo\b", "America/Santo_Domingo"),
    (r"\bPanama\b", "America/Panama"), (r"\bGuatemala\b", "America/Guatemala"), (r"\bSan Jos[eé], Costa Rica\b",
                                                                                 "America/Costa_Rica"),
    (r"\bPort-au-Prince\b", "America/Port-au-Prince"), (r"\bOttawa\b|\bMontreal\b|\bToronto\b", "America/Toronto"),
    (r"\bVancouver, B\.C\.|\bVancouver\b(?!, Wash)", "America/Vancouver"),
    (r"\bCamp David\b|\bGlassboro\b|\bthe Elms\b|\bThe Elms\b|\bArlington\b|\bAndrews\b|\bBethesda\b", DC),
    (r"\bHyannis Port\b|\bCape Cod\b", DC), (r"\bStanleyville\b", "Africa/Lubumbashi"),
    (r"\bElisabethville\b", "Africa/Lubumbashi"), (r"\bSalisbury\b, Rhodesia|\bRhodesia\b", "Africa/Harare"),
    (r"\bJohannesburg\b|\bPretoria\b|\bCape Town\b", "Africa/Johannesburg"),
]
# Cities of the States propose.ZONES and CITY do not settle: their State's zone, the clock in doubt before 1967.
US_CITIES = {"Milwaukee": "wi", "Minneapolis": "mn", "St. Paul": "mn", "St. Louis": "mo", "Kansas City": "mo",
             "Cleveland": "oh", "Cincinnati": "oh", "Columbus": "oh", "Toledo": "oh", "Akron": "oh", "Dayton": "oh",
             "Pittsburgh": "pa", "Philadelphia": "pa", "Harrisburg": "pa", "Baltimore": "md", "Seattle": "wa",
             "Portland": "or", "Las Vegas": "nv", "Reno": "nv", "Phoenix": "az", "Salt Lake City": "ut",
             "Omaha": "ne", "Des Moines": "ia", "Oklahoma City": "ok", "Tulsa": "ok", "Little Rock": "ar",
             "Charlotte": "nc", "Raleigh": "nc", "Greensboro": "nc", "Durham": "nc", "Richmond": "va",
             "Norfolk": "va", "Charleston": "sc", "Columbia, S.C": "sc", "Savannah": "ga", "Tallahassee": "fl",
             "Jacksonville": "fl", "Tampa": "fl", "Palm Beach": "fl", "Key West": "fl", "St. Augustine": "fl",
             "Indianapolis": "in", "Louisville": "ky", "Lexington": "ky", "Buffalo": "ny", "Rochester": "ny",
             "Newark": "nj", "Trenton": "nj", "Hartford": "ct", "Providence": "ri", "Manchester": "nh",
             "Anchorage": "ak", "Albuquerque": "nm", "Cheyenne": "wy", "Boise": "id", "Sioux Falls": "sd",
             "Greenwood": "ms", "Philadelphia, Miss": "ms", "Meridian": "ms", "Biloxi": "ms", "Hattiesburg": "ms",
             "Mobile": "al", "Anniston": "al", "Gadsden": "al", "Danville": "va", "Cambridge, Md": "md",
             "Shreveport": "la", "Baton Rouge": "la", "Bogalusa": "la", "Chattanooga": "tn", "Knoxville": "tn",
             "Gettysburg": "pa", "Detroit": "mi", "Lansing": "mi", "Gary": "in", "Springfield, Ill": "il"}
# A country the entry's words open with ("Argentina. The army ..."), where one zone covers it.
COUNTRIES = {"Argentina": "America/Argentina/Buenos_Aires", "Brazil": "America/Sao_Paulo", "Peru": "America/Lima",
             "Chile": "America/Santiago", "Bolivia": "America/La_Paz", "Ecuador": "America/Guayaquil",
             "Colombia": "America/Bogota", "Venezuela": "America/Caracas", "Dominican Republic": "America/Santo_Domingo",
             "Haiti": "America/Port-au-Prince", "Guatemala": "America/Guatemala", "Honduras": "America/Tegucigalpa",
             "El Salvador": "America/El_Salvador", "Nicaragua": "America/Managua", "Costa Rica": "America/Costa_Rica",
             "Panama": "America/Panama", "Cuba": "America/Havana", "Ghana": "Africa/Accra", "Nigeria": "Africa/Lagos",
             "Kenya": "Africa/Nairobi", "Egypt": "Africa/Cairo", "Israel": "Asia/Jerusalem", "Jordan": "Asia/Amman",
             "Syria": "Asia/Damascus", "Iraq": "Asia/Baghdad", "Iran": "Asia/Tehran", "Turkey": "Europe/Istanbul",
             "Greece": "Europe/Athens", "Cyprus": "Asia/Nicosia", "Pakistan": "Asia/Karachi", "India": "Asia/Kolkata",
             "Burma": "Asia/Yangon", "Thailand": "Asia/Bangkok", "Laos": "Asia/Vientiane", "Cambodia": "Asia/Phnom_Penh",
             "South Korea": "Asia/Seoul", "Korea": "Asia/Seoul", "Japan": "Asia/Tokyo", "Taiwan": "Asia/Taipei",
             "France": "Europe/Paris", "Britain": "Europe/London", "England": "Europe/London",
             "West Germany": "Europe/Berlin", "East Germany": "Europe/Berlin", "Italy": "Europe/Rome",
             "Spain": "Europe/Madrid", "Portugal": "Europe/Lisbon", "Belgium": "Europe/Brussels",
             "Czechoslovakia": "Europe/Prague", "Poland": "Europe/Warsaw", "Hungary": "Europe/Budapest",
             "Yugoslavia": "Europe/Belgrade", "Romania": "Europe/Bucharest", "Algeria": "Africa/Algiers",
             "Morocco": "Africa/Casablanca", "Libya": "Africa/Tripoli", "Ethiopia": "Africa/Addis_Ababa",
             "Saudi Arabia": "Asia/Riyadh", "Lebanon": "Asia/Beirut", "Yemen": "Asia/Aden", "Ceylon": "Asia/Colombo",
             "Philippines": "Asia/Manila", "Malaysia": "Asia/Kuala_Lumpur", "Singapore": "Asia/Singapore",
             "Ireland": "Europe/Dublin", "Austria": "Europe/Vienna", "Switzerland": "Europe/Zurich"}
US_RX = re.compile(r"\b(" + "|".join(re.escape(k) for k in sorted(US_CITIES, key=len, reverse=True)) + r")\b")
BLUEBOOK = {"Ala": "al", "Ariz": "az", "Ark": "ar", "Cal": "ca", "Colo": "co", "Conn": "ct", "Del": "de", "Fla": "fl",
            "Ga": "ga", "Idaho": "id", "Ill": "il", "Ind": "in", "Iowa": "ia", "Kan": "ks", "Ky": "ky", "La": "la",
            "Me": "me", "Md": "md", "Mass": "ma", "Mich": "mi", "Minn": "mn", "Miss": "ms", "Mo": "mo", "Mont": "mt",
            "Neb": "ne", "Nev": "nv", "N.H": "nh", "N.J": "nj", "N.M": "nm", "N.Y": "ny", "N.C": "nc", "N.D": "nd",
            "Ohio": "oh", "Okla": "ok", "Or": "or", "Pa": "pa", "R.I": "ri", "S.C": "sc", "S.D": "sd", "Tenn": "tn",
            "Tex": "tx", "Utah": "ut", "Vt": "vt", "Va": "va", "Wash": "wa", "W. Va": "wv", "Wis": "wi", "Wyo": "wy"}
TOWN = r"[A-Z][A-Za-z'.-]+(?: [A-Z][A-Za-z'.-]+){0,2}, (" + "|".join(re.escape(k) for k in
                                                                       sorted(BLUEBOOK, key=len, reverse=True)) + r")\."


def place_rx():
    rows = [(rx, z) for rx, z in MORE] + list(propose.ZONES)
    return rows


def event_place(c):
    """(zone key, the words, a State's postal code or None): the place where the entry's event happened: the place
    its first sentence opens with ("Toledo." "Lisbon, at lunch." "Hershey, Pa., the ... dinner"), else the first after
    "at" or "in", else after "from" (propose.py STYLE 4; the Bluebook's State after a town, the calendar's style)."""
    s = first_sentence(plain(c))
    lead = re.split(r"[,.:;]\s", s + " ", maxsplit=1)[0]
    m = re.match(TOWN, s)
    if m:
        return None, m.group(0), BLUEBOOK[m.group(1)]
    if len(lead) <= 40:
        for rx, z in place_rx():
            if re.search(rx, lead):
                return z, lead, None
        m = US_RX.search(lead)
        if m:
            return None, lead, US_CITIES[m.group(1)]
        if lead.strip() in COUNTRIES:
            return COUNTRIES[lead.strip()], lead, None
    for prep in (r"[Aa]t|[Ii]n", r"[Ff]rom"):
        best = None
        for rx, z in place_rx():
            mm = re.search(r"\b(?:" + prep + r")\s+(?:the\s+)?(?:" + rx + ")", s)
            if mm and (best is None or mm.start() < best[0]):
                best = (mm.start(), z, mm.group(0), None)
        mm = re.search(r"\b(?:" + prep + r")\s+" + TOWN, s)
        if mm and (best is None or mm.start() < best[0]):
            best = (mm.start(), None, mm.group(0), BLUEBOOK[mm.group(1)])
        mm = re.search(r"\b(?:" + prep + r")\s+" + US_RX.pattern, s)
        if mm and (best is None or mm.start() < best[0]):
            best = (mm.start(), None, mm.group(0), US_CITIES[mm.group(1)])
        if best:
            return best[1], best[2], best[3]
    return None


def doubt(zone, day):
    """The two readings of a clock in doubt, standard and daylight, as fixed offsets; None outside April-October
    (daylight time's season then) or for a zone STD does not give."""
    if zone not in STD or not "04" <= day[5:7] <= "10":
        return None
    s = STD[zone]
    return [f"Etc/GMT+{s}", f"Etc/GMT+{s - 1}"]


def utc(day, hours, zone):
    """Local hours (a float, past 24 the next day's, below 0 the day before's) on a day -> 'YYYY-MM-DDTHH:MMZ'."""
    d = datetime.date.fromisoformat(day) + datetime.timedelta(days=int(hours // 24))
    h = hours % 24
    local = datetime.datetime.combine(d, datetime.time(int(h), int(round((h % 1) * 60))), zoneinfo.ZoneInfo(zone))
    return local.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def span_range(day, a, b, zone, readings):
    zs = readings or [zone]
    lo = min(utc(day, a, z) for z in zs)
    hi = max(utc(day, b, z) for z in zs)
    return [lo, hi]


# ------------------------------------------------------------------------------------------------------- words

# (pattern, band or None, start hour, end hour, the words' gloss): the first pattern that matches at a place wins,
# so the longer phrases come first. Hours local; past 24 the next day's, below 0 the day before's.
WORDS = [
    (r"after midnight|shortly after midnight|past midnight", "predawn", 0, 6, "after midnight"),
    (r"early[- ]morning hours|in the early hours|small hours|wee hours", "predawn", 0, 6, "the early-morning hours"),
    (r"before dawn|pre-?dawn|before daybreak", None, 0, 7, "before dawn"),
    (r"at dawn|at daybreak|at first light|dawn", None, 4, 8, "dawn"),
    (r"early (?:that |this |in the )?morning|early on the morning", None, 0, 9, "early morning"),
    (r"late (?:that |this |in the )?morning", "workday morning", 9, 12, "late morning"),
    (r"breakfast", "morning", 6, 12, "breakfast"),
    (r"(?:that|this|in the|on the|the|a|one) morning|morning(?= (?:meeting|session|briefing|news conference|press "
     r"conference|call|talks?|service|rally|speech|address))|^morning\b", "morning", 6, 12, "morning"),
    (r"midday|mid-day|noon hour|at noontime", None, 11, 14, "midday"),
    (r"luncheon|lunch", None, 11, 16, "lunch"),
    (r"early (?:that |this |in the )?afternoon", None, 12, 15, "early afternoon"),
    (r"late (?:that |this |in the )?afternoon", None, 15, 19, "late afternoon"),
    (r"(?:that|this|in the|on the|the|an|one) afternoon|afternoon(?= (?:meeting|session|briefing|news conference|"
     r"press conference|call|talks?|rally|speech|address))|^afternoon\b", "afternoon", 12, 18, "afternoon"),
    (r"at dusk|at sundown|at sunset|at nightfall|dusk", None, 16, 21, "dusk"),
    (r"early (?:that |this |in the )?evening", None, 17, 21, "early evening"),
    (r"late (?:that |this |in the )?evening", None, 20, 24, "late evening"),
    (r"(?:that|this|in the|on the|the|an|one) evening|evening(?= (?:meeting|session|briefing|news conference|press "
     r"conference|call|talks?|rally|speech|address|broadcast|reception))|^evening\b", None, 17, 24, "evening"),
    (r"dinner", None, 17, 24, "dinner"),
    (r"late (?:that |at |in the |into the )night|late-night|late at night", None, 21, 27, "late that night"),
    (r"overnight", None, -6, 30, "overnight: the night into the date or the night after it"),
    (r"(?:that|this) night|at night|in the night|night session|^night\b", None, 18, 27, "that night"),
]
WORD_RX = [(re.compile(r"(?<![\w-])(?:" + rx + r")(?![\w-])", re.I), b, a, z, g) for rx, b, a, z, g in WORDS]
NOT_HERE = re.compile(
    r"lunch[- ]?counter|lunchroom|hot lunch|luncheonette|lunch program|school lunch|lunch money|lunch[- ]counters|"
    r"morning business|morning hour|morning paper|morning newspaper|morning edition|morning star|"
    r"evening paper|evening newspaper|evening news|evening edition|evening dress|evening star|"
    r"afternoon paper|afternoon newspaper|night club|nightclub|night letter|night school|dinner jacket|"
    r"every (?:morning|afternoon|evening|night)|each (?:morning|afternoon|evening|night)|"
    r"(?:next|following|previous|preceding|that same|the same) (?:day'?s? )?(?:morning|afternoon|evening|night|dawn)|"
    r"(?:morning|afternoon|evening|night|dawn) (?:before|after|of the next|following)|"
    r"(?:in|by) the morning(?= ,? ?(?:he|she|they) (?:would|will))|overnight (?:poll|bag|stay)|"
    r"(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)days", re.I)
TITLE = re.compile(r"(?<=\w )(?:Morning|Afternoon|Evening|Night)(?= [A-Z])|(?:Morning|Evening) (?:News|Star|Post|Herald|"
                   r"Bulletin|Call|Sun|Telegraph|Tribune|Journal|Record)")     # a newspaper's name
OTHER_DAY = re.compile(r"(?:morning|afternoon|evening|night|dawn|dinner|lunch|luncheon|breakfast) (?:of|on) "
                       r"((?:Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)[a-z]*\.? \d{1,2})", re.I)
WEEKDAY_BAND = re.compile(r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)(?:'s)? "
                          r"(?:early |late )?(morning|afternoon|evening|night|lunch|luncheon|dinner|breakfast)\b")
YESTERDAY = re.compile(r"\b(?:yesterday|the day before|the night before|the evening before|last night)\b", re.I)


def plain(t):
    """The entry's words without quotations, italic titles, links' addresses and wiki links' ids."""
    t = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[\[[^\]]*\]\]", " ", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"\*[^*]+\*", " ", t)
    t = re.sub(r"“[^”]*”", " ", t)
    t = re.sub(r'"[^"]*"', " ", t)
    return t


def day_of(text, day):
    """False where the words tie the band to another day than the entry's (OTHER_DAY, a weekday, yesterday)."""
    d = datetime.date.fromisoformat(day)
    for m in WEEKDAY_BAND.finditer(text):
        if m.group(1) != WEEKDAYS[d.weekday()]:
            return False
    for m in OTHER_DAY.finditer(text):
        mo = m.group(1)[:3].lower()
        num = int(re.search(r"\d+", m.group(1)).group())
        mm = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"].index(mo) + 1
        if (mm, num) != (d.month, d.day):
            return False
    return not YESTERDAY.search(text)


SAYS = re.compile(r"\b(?:writes|wrote|tells|told|says|said|reports|cables|telegraphs|telegram|letter|memorandum|"
                  r"by telephone|by phone|to [A-Z][a-z]+|warns|asks|answers|replies|announces|statement)\b")
HOUR_WORDS = re.compile(r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)(?: o'clock)? in the "
                        r"(?:morning|afternoon|evening)|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|"
                        r"twelve) o'clock\b", re.I)
# A band the words give another act than the entry's: an end ("until evening"), a thing reported or discussed ("of a
# dinner with Kennedy", "on his lunch with Handleman"), an act before or after the entry's.
REPORTED = re.compile(r"(?:\b(?i:until|till|of|about|after|following|before|since|into|through|by|for)|"
                      r"\b(?i:on) (?:his|her|their))\s+(?:(?:a|an|the|his|her|their|its)\s+)?(?:[A-Za-z.'’-]+\s+){0,3}$"
                      r"|(?:\b(?:together|woven|drafted|written|worked out|prepared)|[a-z]{3,}ed)\s+$")


def bands_in(text):
    """[(band, start, end, gloss, matched words)] in the text, NOT_HERE's phrases taken out first, and a band the
    words tie to another act (REPORTED)."""
    t = TITLE.sub(" ", NOT_HERE.sub(" ", text))
    out, taken = [], []
    for rx, band, a, b, gloss in WORD_RX:
        for m in rx.finditer(t):
            if any(s <= m.start() < e or s < m.end() <= e for s, e in taken):
                continue
            taken.append((m.start(), m.end()))
            pre = t[max(0, m.start() - 40):m.start()]
            if REPORTED.search(pre):
                continue
            out.append((band, a, b, gloss, m.group(0), m.start()))
    return out


def first_sentence(c):
    """The entry's first unit (claims.units: its first sentence, or to its first semicolon), with the second where
    the first is a heading of a few words ("Ohio." "Late afternoon." "Chicago, the Sherman House, the morning.")."""
    us = units(c)
    if not us:
        return ""
    s = us[0]
    if len(us) > 1 and len(s) < 50 and (len(s.split()) <= 3 or HEADING.match(s)):
        s += " " + us[1]
    return s


# A heading: a place, then places or times ("Chicago, the Sherman House, the morning."), no act.
HEADING = re.compile(r"^[A-Z][^,;:]{0,30}(?:, (?:the|at|in|on|early|late|before|after) [^,;:]{1,30}){1,3}[.;]$")


def word_rows(e, day, c, n, zone_info, ppp_hits):
    rows = []
    zone, zc, readings, how = zone_info
    if zone is None:
        return rows
    s = first_sentence(plain(c))
    found = []
    if ":" in s and SAYS.search(s.split(":", 1)[0]):
        s = s.split(":", 1)[0]            # what a message, a call or a letter says is another act's
    if propose.HOUR.search(s) or HOUR_WORDS.search(s):
        s = ""                            # an hour in the sentence: the band another act's, or no more than it
    if day_of(s, day):
        found = [(f, f"the entry's words: {s.strip()[:160]!r}") for f in bands_in(s)
                 if not SAYS.search(s[:f[5]])]       # a band after a letter's or a call's head: what it reports
    # a note's short parenthetical after a work read and pinpointed, not behind "To check:"
    nn = re.split(r"\bTo check:", n)[0]
    for m in re.finditer(r"\]\],? (?:[IVXL]+, )?\d[\d–-]*(?: n\.\s?\d+)?(?:, \d[\d–-]*)? \(([^()]{3,40})\)", nn):
        par = plain(m.group(1))
        if re.search(r"[,;:]", par) or len(par.split()) > 4:
            continue                      # a parenthetical of several claims: the band one claim's, not the entry's
        if day_of(par, day):
            for f in bands_in(par):
                found.append((f, f"the note's parenthetical after a work read: {m.group(0)[2:].strip()!r}"))
    kinds = {(f[1], f[2]) for f, _ in found}
    if len(kinds) != 1:
        return rows                       # none, or two spans: two acts
    (band, a, b, gloss, words, _), basis = found[0]
    rows.append(make_row(e, day, "words", band, a, b, gloss, zone, zc, readings, how,
                         f"{basis}; {gloss!r} ({words!r})"))
    return [r for r in rows if r]


def make_row(e, day, source, band, a, b, gloss, zone, zc, readings, how, basis, extra=None):
    rng = span_range(day, a, b, zone, readings)
    if (datetime.datetime.fromisoformat(rng[1][:-1]) - datetime.datetime.fromisoformat(rng[0][:-1])).total_seconds() \
            > 36 * 3600:
        return None                       # wider than dayorder allows (STYLE 6): the two readings of a night
    row = {"id": e["id"], "time_range": rng, "source": source, "basis": basis}
    if band and not readings and BANDS.get(band) == (a, b):
        row["time_band"] = band
    else:
        row["span"] = f"{fmt_h(a)}-{fmt_h(b)} local" + (f" ({gloss})" if gloss else "")
    row["time_zone"] = zone
    row["zone_from"] = how
    if zc:
        row["zone_check"] = True
    if readings:
        row["readings"] = readings
    if a < 0 or b > 24:
        row["check"] = ("the span runs into the day before or the day after: "
                        + ("the night into the date or the night after it" if a < 0 else "past midnight"))
    if gloss == "after midnight":
        row["check"] = "after midnight: the predawn of the entry's date; where the entry is dated by the evening before, the day before's"
    row.update(extra or {})
    return row


def fmt_h(h):
    d = "" if 0 <= h <= 24 else (" next day" if h > 24 else " day before")
    return f"{int(h % 24 if not 0 <= h <= 24 else h):02d}:00{d}"


# ---------------------------------------------------------------------------------------------------- congress

PASSIVE = re.compile(r"\b(?:passed|adopted|approved|rejected|defeated|confirmed|ratified|tabled|killed) by the "
                     r"(Senate|House)\b")
SPEECH = re.compile(r"\bon the (Senate|House) floor\b|\b(Senate|House) floor speech\b|\bspeech (?:in|to|on the floor of) the "
                    r"(Senate|House)\b|\bin a (Senate|House) speech\b|\btells the (Senate|House)\b|"
                    r"\b(Senate|House) speech\b|\b(Senate|House) (?:roll[- ]call )?vote\b")
NOT_FLOOR = re.compile(r"\bsigns?\b|\bsigned\b|\bvetoe?s?\b|\bmessage\b|\bproclamation\b|\bcommittee\b|"
                       r"\bsubcommittee\b|\bhearings?\b|\bbreakfast|\blunch|\bdinner|\bmeeting\b|\btelephone|"
                       r"\bmemorandum|\bletter\b|\bcable\b|\bcalls?\b|\bplans?\b|\bcannot\b|\bwill\b|\bwould\b", re.I)
REPORT = re.compile(r"^[^:;]{0,70}\bto [A-Z][^:;]{0,50}:")       # "Wilson to O'Brien: ..." a message, not the floor


def chambers(e, c):
    """The chambers whose floor act the entry's first sentence records: {'S', 'H'}."""
    if any(str(t).startswith("state:") for t in e.get("tags") or []) or "states" in (e.get("thread") or "") \
            or re.match(r"^[A-Z][a-z]+(?: [A-Z][a-z]+)?, [A-Z][a-z]{1,4}\.", c):
        if not re.search(r"\bCongress\b|\bU\.S\. (?:Senate|House)|\bin Washington\b", c):
            return set()
    s = first_sentence(plain(c))
    out = set()
    if REPORT.search(s):
        return out
    for m in tiers.CHAMBER_ACT.finditer(s):
        if tiers.STATES.search(s[max(0, m.start() - 30):m.start()]) or m.group(2) == "passed":
            continue
        if NOT_FLOOR.search(s[:m.start()]) or re.match(r"\s*(?:hearings?|committee)", s[m.end():m.end() + 20], re.I):
            continue
        out.add("S" if m.group(1) == "Senate" else "H")
    for rx in (PASSIVE, SPEECH):
        for m in rx.finditer(s):
            if NOT_FLOOR.search(s[:m.start()]):
                continue
            g = next(x for x in m.groups() if x)
            out.add("S" if g == "Senate" else "H")
    if tiers.CLOTURE.search(s) and re.search(r"\bSenate\b", s) and not NOT_FLOOR.search(s):
        out.add("S")
    return out


def meetings(data):
    """{(day, ch): (local, basis, check, url)} the hour each chamber met, from the Digest (the docstring, congress)."""
    dg = data.get("digest") or {}
    orders = dg.get("orders") or []
    standing = {}
    for o in orders:
        if o["kind"] == "standing":
            standing.setdefault(o["ch"], []).append(o)
    for v in standing.values():
        v.sort(key=lambda o: o["day"])
    ordered, early = {}, set()
    for o in orders:                       # in reading order: a later order for a day replaces an earlier one
        for ch in (["S", "H"] if o["ch"] == "SH" else [o["ch"]]):
            if o["kind"] == "order":
                ordered[(o["target"], ch)] = o
            elif o["kind"] == "early":
                early.add((o["target"], ch))
    met = {}
    for rows in (dg.get("by_date") or {}).values():
        for r in rows:
            if r["kind"] in ("met", "reconvened"):
                k = (r["day"], r["ch"])
                if k not in met or r["local"] < met[k]["local"]:
                    met[k] = r
    return met, ordered, early, standing


def cite(r):
    return f"Daily Digest, {r.get('folio') or 'PDF p. ' + str(r['pdf'])}"


def congress_rows(e, day, c, data, meet):
    met, ordered, early, standing = meet
    rows = []
    close_by = {}
    for r in data.get("digest_day", {}).get(day, []):
        if r["kind"] in ("adjourned", "recessed"):
            close_by.setdefault(r["ch"], []).append(r)
    for ch in sorted(chambers(e, c)):
        name = "Senate" if ch == "S" else "House"
        close = close_by.get(ch) or []
        if len(close) != 1:
            continue
        cl = close[0]
        check = None
        if (day, ch) in met:
            m = met[(day, ch)]
            start, sb = m["local"], f"{cite(m)}: \"{m['raw']}\""
        elif (day, ch) in ordered:
            o = ordered[(day, ch)]
            start, sb = o["local"], f"{cite(o)} (the order, of {o['day']}): \"{o['raw'][-120:]}\""
        elif (day, ch) in early:
            continue
        else:
            st = [o for o in standing.get(ch, []) if o["day"] <= day and o["day"][:4] == day[:4]]
            if not st:
                continue
            o = st[-1]
            start, sb = o["local"], (f"{cite(o)} (the session's standing order, {o['day']}): \"{o['raw'][-90:]}\"")
            check = ("the hour of meeting is the session's standing order; the Digest prints no order for the day "
                     "that the reader found (an order missed would make it earlier)")
        lo = propose.to_utc(day, start, DC)
        hi = propose.to_utc(cl["date"], cl["local"], DC)
        if hi <= lo:
            continue
        row = {"id": e["id"], "time_range": [lo, hi], "source": "congress",
               "basis": f"the {name} met: {sb}; rose: {cite(cl)}, \"{cl['raw']}\" (the entry's act between)",
               "time_zone": DC, "url": cl["url"]}
        if check:
            row["check"] = check
        rows.append(row)
    return rows


# --------------------------------------------------------------------------------------------------------- ppp

def load_ppp_notes():
    """{package: {"page": {printed page: [item]}, "pdf": [item]}} as propose.load_ppp, each item with its first
    NOTE or bracketed line (`note`) and the hour propose reads from it (`hour`)."""
    out = {}
    for f in glob.glob(os.path.join(ROOT, "sources", "ppp-text", "PPP-*.json.xz")):
        d = json.load(lzma.open(f))
        idx = out.setdefault(d["package"], {"page": {}, "pdf": []})
        for it in d["items"]:
            note, hour = None, None
            for kind, t in it.get("text") or []:
                if kind in ("n", "b"):
                    hour = hour or propose.ppp_hour(t, it.get("date"))
                    if note is None and kind == "n":
                        note = t
            row = {"pdf": it.get("pdf"), "pdf_to": it.get("pdf_to") or it.get("pdf"), "date": it.get("date"),
                   "page": it.get("page"), "title": it.get("title") or "", "hour": hour, "note": note}
            idx["page"].setdefault(it.get("page"), []).append(row)
            idx["pdf"].append(row)
    return out


def ppp_rows(e, day, n, ppp, gaz):
    rows = []
    its = [(pkg, cite_, it) for pkg, cite_, it in propose.ppp_items(n, ppp, day) if str(it["date"]) == day]
    if not its or any(it["hour"] for _, _, it in its):
        return rows
    pkg, cite_, it = its[0]
    if not it["note"]:
        return rows
    t = re.sub(r"\s+", " ", it["note"])
    sents = [x for x in re.split(r"(?<=\.)\s+(?=[A-Z])", t) if re.search(r"\bspoke|\bread|\bheld|\bdelivered|\bbegan|"
                                                                      r"\bmade|\bbroadcast|\bmet\b", x)]
    if not sents:
        return rows
    sent = sents[0]
    if not day_of(sent, day) or re.match(r"(?:Earlier|Later|Previously|Afterwards?|Before|After)\b", sent):
        return rows
    for mo, dd in re.findall(propose.MONTHS, sent):
        if (propose.MONTH_N[mo], int(dd)) != (int(day[5:7]), int(day[8:10])):
            return rows
    found = bands_in(plain(sent))
    if len({(f[1], f[2]) for f in found}) != 1:
        return rows
    band, a, b, gloss, words, _ = found[0]
    z, zc = propose.place_zone(sent)
    if not propose.event_zone(sent):
        zinfo = zone_for(e, "", gaz)
        if zinfo[0] is None:
            return rows
        zone, zc, readings, how = zinfo
    else:
        zone, dst = propose.real_zone(z, day)
        readings = doubt("America/Chicago" if z == propose.SOUTH else zone, day) if zc else None
        zc = zc or dst
        how = "the place in the Papers' NOTE"
    rows.append(make_row(e, day, "ppp", band, a, b, gloss, zone, zc, readings, how,
                         f"{pkg}, p. {it['page']} ({cite_}): {sent[:160]}; {gloss!r} ({words!r})"))
    return [r for r in rows if r]


# -------------------------------------------------------------------------------------------------------- clocks

def clock_rows(e, day, clocks):
    rows = []
    for k in clocks.get(e["id"], []):
        d = k.get("day", day)
        rng = sorted(propose.to_utc(d, k["local"], z) for z in k["readings"])
        row = {"id": e["id"], "time_range": [rng[0], rng[-1]], "source": "clocks",
               "basis": f"{k['hour']}; read at {' or '.join(k['readings'])}. The reviewer ({k['by']}): {k['reason']}",
               "readings": list(k["readings"]), "zone_check": True}
        if k.get("zone"):
            row["time_zone"] = k["zone"]
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------------------------------------- main

def main():
    s = store.Series(ROOT)
    data = tiers.load()
    meet = meetings(data)
    gaz = gazetteer()
    ppp = load_ppp_notes()
    clocks = {}
    for k in (store.load_yaml(os.path.join(DATA, "clocks.yaml")) or {}).get("clocks") or []:
        clocks.setdefault(k["id"], []).append(k)
    timed = set()
    tp = os.path.join(ROOT, "notes", "times-proposals.yaml")
    if os.path.exists(tp):
        timed = {r["id"] for r in (store.load_yaml(tp) or {}).get("proposals") or [] if not r.get("bound")}
    out, n_dated, n_open = [], 0, 0
    for _, e in s.lists["cal"].entries():
        day = str(e.get("date", ""))
        if len(day) != 10:
            continue
        n_dated += 1
        if e.get("time") or e.get("time_range"):
            continue
        n_open += 1
        c = e.get("c") or ""
        c = " ".join(map(str, c)) if isinstance(c, list) else str(c)
        n = str(e.get("n") or "")
        rows = congress_rows(e, day, c, data, meet)
        rows += word_rows(e, day, c, n, zone_for(e, c, gaz), None)
        rows += clock_rows(e, day, clocks)
        rows += ppp_rows(e, day, n, ppp, gaz)
        for r in rows:
            if e["id"] in timed:
                r["has_time"] = True
            out.append(r)
    out.sort(key=lambda r: (r["id"], r["source"], r["time_range"]))
    store.dump_yaml({"ranges": out}, OUT, header=[
        "Generated by tools/times/propose_ranges.py: time ranges proposed for the calendar's entries that have no",
        "time, for review (its docstring and STYLE; dayorder STYLE 5-6). Never edit; move a range into its entry",
        "(time_range, time_band, time_zone) by patch, its basis in the note."])
    ids = len({r["id"] for r in out})
    counts = {}
    for r in out:
        counts.setdefault(r["source"], {}).setdefault(r["id"][4:8], 0)
        counts[r["source"]][r["id"][4:8]] += 1
    print(f"{n_dated} dated entries, {n_open} with neither time nor time_range; {len(out)} ranges for {ids} entries")
    for src in ("congress", "words", "clocks", "ppp"):
        by = counts.get(src, {})
        print(f"  {src} {sum(by.values())}: " + ", ".join(f"{y} {k}" for y, k in sorted(by.items())))
    return out


if __name__ == "__main__":
    main()
