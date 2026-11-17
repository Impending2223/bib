"""Loose dates: a calendar entry dated to a year or a month, and the intercalary days (偽日) it may sit on
(notes/proposals/loose-dates.md; the owner, Nov. 15, 2026).

    date: '1962'                a year alone: filed in that year's January section, shown first in the year ("1962")
    date: '1962-05'             a month alone: the month's own block, at the head of the month ("May")
    at: before 1962-05-21       hidden, optional, on a year- or month-dated entry only: the intercalary day it sits on,
    at: after 1962-05-12        before or after a day ("Late May"; "After May 12")

STYLE:
 1. An intercalary day is a heading in the day's ordinary style, its text the loose date, from the entry's `when`
    (heading: "May, late" -> "Late May"; "May, after the 12th" -> "After May 12"; "Mar., spring" -> "Spring"; any
    other wording as written). It holds every entry of its section with that `at` and that heading, sorted as the
    month's undated block is (dayorder). Several on one day: the wider first (a season, a third, a day's before or
    after, any other wording), then by heading.
 2. The order of a year: the year's block ("1962"); then each month: the month's block ("May"), "Early May", May 1 ...
    May 10, "Mid-May", May 11 ... May 20, "Late May", May 21 ... May 31. A "before X" day stands straight before X's
    day (under X's week heading when X is a Sunday), an "after X" day straight after it, before any "before" day of
    the next (order_key: the day, then -2 the year, -1 the month, 0 before, 1 the day, 2 after).
 3. Thirds: the first day of third k (0, 1, 2) of a month of L days is floor(kL/3) + 1: 31 and 30 days the 1st, 11th,
    21st; February of 28 the 1st, 10th, 19th; of 29 the 1st, 10th, 20th (thirds).
 4. Seasons: the day of the equinox or solstice that opens each (Meeus, *Astronomical Algorithms*, 2nd ed., ch. 27, the
    mean instant and its 24 periodic terms; ΔT by Espenak and Meeus's polynomials), in SEASON_ZONE (season_starts).
    "Winter" is the winter opening in December of its year; a reader who means the one ending in March sets `at` to the
    December solstice of the year before.
 5. An entry with `at` (or a year alone) is shown in the dated section that holds its day, which may be another month's
    of the same list (hosts); its anchor and its part follow (place_iso). Files and sections are unchanged. Where no
    section holds the day (early January 1960, before the calendar's first day), it stays in its own, at the head.
"""
import calendar
import datetime
import math
import re

# The day an equinox or solstice falls on is taken in Washington time. The owner has not ruled on the zone (Washington
# or UTC; notes/proposals/loose-dates.md, "Open"): change this one constant when he does.
SEASON_ZONE = "America/New_York"

AT = re.compile(r"^(before|after) (\d{4})-(\d\d)-(\d\d)$")
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
MON_OF = {m: i + 1 for i, m in enumerate(MON)}
MONTH_HEAD = re.compile(r"^(Jan\.|Feb\.|Mar\.|Apr\.|May|June|July|Aug\.|Sept\.|Oct\.|Nov\.|Dec\.)(?=$|[,\s(])[,\s]*")
SEASONS = ("spring", "summer", "fall", "winter")
SEASON_MONTH = {"spring": 3, "summer": 6, "fall": 9, "winter": 12}
SEASON_WORD = {"spring": "spring", "summer": "summer", "fall": "fall", "autumn": "fall", "winter": "winter"}
ORD = r"(\d{1,2})(?:st|nd|rd|th)"


# ---------------------------------------------------------------- the days

def thirds(y, m):
    """The first day of each third of a month (STYLE 3)."""
    n = calendar.monthrange(y, m)[1]
    return [datetime.date(y, m, k * n // 3 + 1) for k in range(3)]


_TERMS = [(485, 324.96, 1934.136), (203, 337.23, 32964.467), (199, 342.08, 20.186), (182, 27.85, 445112.039),
          (156, 73.14, 45036.886), (136, 171.52, 22518.443), (77, 222.54, 65928.934), (74, 296.72, 3034.906),
          (70, 243.58, 9037.513), (58, 119.81, 33718.147), (52, 297.17, 150.678), (50, 21.02, 2281.226),
          (45, 247.54, 29929.562), (44, 325.15, 31555.956), (29, 60.93, 4443.417), (18, 155.12, 67555.328),
          (17, 288.79, 4562.452), (16, 198.04, 62894.029), (14, 199.76, 31436.921), (12, 95.39, 14577.848),
          (12, 287.11, 31931.756), (12, 320.81, 34777.259), (9, 227.73, 1222.114), (8, 15.45, 16859.074)]
_MEAN = {   # Meeus, table 27.C (years 1000 to 3000): JDE0 = a + bY + cY^2 + dY^3 + eY^4, Y = (year - 2000) / 1000
    3: (2451623.80984, 365242.37404, 0.05169, -0.00411, -0.00057),
    6: (2451716.56767, 365241.62603, 0.00325, 0.00888, -0.00030),
    9: (2451810.21715, 365242.01767, -0.11575, 0.00337, 0.00078),
    12: (2451900.05952, 365242.74049, -0.06223, -0.00823, 0.00032),
}


def _delta_t(y):
    """ΔT in seconds (Espenak and Meeus, the polynomials for 1941-2005)."""
    if y < 1961:
        t = y - 1950
        return 29.07 + 0.407 * t - t * t / 233 + t ** 3 / 2547
    if y < 1986:
        t = y - 1975
        return 45.45 + 1.067 * t - t * t / 260 - t ** 3 / 718
    t = y - 2000
    return 63.86 + 0.3345 * t - 0.060374 * t ** 2 + 0.0017275 * t ** 3 + 0.000651814 * t ** 4 + 0.00002373599 * t ** 5


def season_instant(y, month):
    """The UTC instant of the March or September equinox or the June or December solstice of year y."""
    Y = (y - 2000) / 1000
    a, b, c, d, e = _MEAN[month]
    jde0 = a + b * Y + c * Y ** 2 + d * Y ** 3 + e * Y ** 4
    T = (jde0 - 2451545.0) / 36525
    W = math.radians(35999.373 * T - 2.47)
    dl = 1 + 0.0334 * math.cos(W) + 0.0007 * math.cos(2 * W)
    S = sum(A * math.cos(math.radians(B + C * T)) for A, B, C in _TERMS)
    jde = jde0 + 0.00001 * S / dl
    jd = jde - _delta_t(y) / 86400
    return datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc) + datetime.timedelta(days=jd - 2440587.5)


_SEASONS = {}


def season_starts(y, zone=None):
    """{'spring': date, 'summer': ..., 'fall': ..., 'winter': ...}: the day each season of year y opens, in zone
    (SEASON_ZONE)."""
    import zoneinfo
    zone = zone or SEASON_ZONE
    if (y, zone) not in _SEASONS:
        z = zoneinfo.ZoneInfo(zone)
        _SEASONS[(y, zone)] = {s: season_instant(y, SEASON_MONTH[s]).astimezone(z).date() for s in SEASONS}
    return _SEASONS[(y, zone)]


# ---------------------------------------------------------------- an entry's place

def parse_at(v):
    """'before 1962-05-21' -> ('before', date(1962, 5, 21)); None if it is not in that form."""
    m = AT.match(str(v or "").strip())
    if not m:
        return None
    try:
        return m.group(1), datetime.date(int(m.group(2)), int(m.group(3)), int(m.group(4)))
    except ValueError:
        return None


def date_of(e):
    """The entry's `date` as text ('1962', '1962-05', '1962-05-14')."""
    return str(e.get("date") or "")


def is_loose(e):
    return len(date_of(e)) in (4, 7)


def first_day(d):
    """The first day a date names: '1962' -> Jan. 1, '1962-05' -> May 1; None for anything else."""
    try:
        if re.fullmatch(r"\d{4}", d):
            return datetime.date(int(d), 1, 1)
        if re.fullmatch(r"\d{4}-\d\d", d):
            return datetime.date(int(d[:4]), int(d[5:7]), 1)
        if re.fullmatch(r"\d{4}-\d\d-\d\d", d):
            return datetime.date.fromisoformat(d)
    except ValueError:
        return None
    return None


def place_day(e):
    """The day an entry is shown at: its `at`'s day; else the first day its date names."""
    a = parse_at(e.get("at")) if is_loose(e) else None
    return a[1] if a else first_day(date_of(e))


def place_iso(e):
    """The place's day as text where `at` gives one, else the date as written: what the calendar's parts and anchors
    go by (calsplit.half_of_date takes either)."""
    a = parse_at(e.get("at")) if is_loose(e) else None
    return a[1].isoformat() if a else date_of(e)


def moves(e):
    """An entry shown in the section that holds its place's day, wherever it is filed (STYLE 5): one with `at`, or a
    year alone."""
    return is_loose(e) and (parse_at(e.get("at")) is not None or len(date_of(e)) == 4)


def _qualifier(e):
    """The words of `when` after its month or year ('May, late' -> 'late'; '1962, spring' -> 'spring')."""
    w = str(e.get("when") or "").strip()
    d = date_of(e)
    if len(d) == 4 and w.startswith(d):
        return w[4:].lstrip(" ,")
    m = MONTH_HEAD.match(w)
    return w[m.end():] if m else w


def _kind(q):
    """(kind, value) of a qualifier: ('', None) none; ('third', 0|1|2); ('before'|'after', day); ('season', name)."""
    q = q.strip().rstrip(".").lower()
    q = re.sub(r"^the ", "", q)
    if not q:
        return "", None
    if q == "early":
        return "third", 0
    if q in ("mid", "mid-month", "middle", "the middle"):
        return "third", 1
    if q == "late":
        return "third", 2
    m = re.fullmatch(r"(before|after) the " + ORD, q)
    if m:
        return m.group(1), int(m.group(2))
    if q in SEASON_WORD:
        return "season", q
    return "other", q


def heading(e):
    """An intercalary day's heading: the loose date, from `when` (STYLE 1)."""
    w = str(e.get("when") or "").strip()
    d = date_of(e)
    q = _qualifier(e)
    k, v = _kind(q)
    full = calendar.month_name[int(d[5:7])] if len(d) == 7 else d
    if k == "third":
        if len(d) == 7:
            return ["Early ", "Mid-", "Late "][v] + full
        return ["Early ", "Mid-", "Late "][v] + d
    if k in ("before", "after") and len(d) == 7:
        return f"{k.capitalize()} {MON[int(d[5:7]) - 1]} {v}"
    if k == "season":
        return v.capitalize()
    if not k:
        a = parse_at(e.get("at"))
        if a and a[0] == "after":
            return f"After {MON[a[1].month - 1]} {a[1].day}"
        if a:
            return f"Before {MON[a[1].month - 1]} {a[1].day}"
        return full
    return w[:1].upper() + w[1:]


def _rank(e):
    k = _kind(_qualifier(e))[0]
    return {"season": 1, "third": 2, "before": 3, "after": 3, "": 3}.get(k, 4)


def order_key(e):
    """The entry's place in the calendar's order (STYLE 2): (day, slot, rank, heading). Slots: -2 a year's block, -1 a
    month's, 0 an intercalary day before the day, 1 the day itself, 2 an intercalary day after it."""
    d = date_of(e)
    a = parse_at(e.get("at")) if is_loose(e) else None
    if a:
        return (a[1], 0 if a[0] == "before" else 2, _rank(e), heading(e))
    day = first_day(d)
    if day is None:
        return (datetime.date.max, 9, 0, "")
    if len(d) == 4:
        return (day, -2, 0, "")
    if len(d) == 7:
        return (day, -1, 0, "")
    return (day, 1, 0, "")


def at_for(e):
    """The `at` the entry's own `when` gives unambiguously (tools/bib/loosedates.py), or None: a month-dated entry's
    early, mid, late (the thirds); before or after the Nth of its month; or the season that opens in its month (spring
    in March, summer in June, fall in September, winter in December)."""
    d = date_of(e)
    if len(d) != 7 or e.get("at"):
        return None
    y, m = int(d[:4]), int(d[5:7])
    k, v = _kind(_qualifier(e))
    if k == "third":
        return f"before {thirds(y, m)[v].isoformat()}"
    if k in ("before", "after"):
        try:
            return f"{k} {datetime.date(y, m, v).isoformat()}"
        except ValueError:
            return None
    if k == "season":
        s = SEASON_WORD[v]
        if SEASON_MONTH[s] == m:
            return f"before {season_starts(y)[s].isoformat()}"
    return None


def at_problems(e):
    """For ./bib check: `at` in its form, on a year- or month-dated entry, its day within the date (a winter's, the
    December solstice before the year, too)."""
    v = e.get("at")
    if v is None:
        return []
    a = parse_at(v)
    if a is None:
        return [f"at {v!r}: 'before YYYY-MM-DD' or 'after YYYY-MM-DD' (loose.py)"]
    d = date_of(e)
    if not is_loose(e):
        return ["at on an entry dated to the day: at is for a date of a year or a month alone"]
    if a[1].isoformat()[:len(d)] == d:
        return []
    y = int(d[:4])
    if a[0] == "before" and a[1] == season_starts(y - 1)["winter"] and (len(d) == 4 or d[5:7] in ("01", "02", "03")):
        return []                       # the winter ending in March: its December solstice (STYLE 4)
    return [f"at {v!r} falls outside the entry's date {d}"]


# ---------------------------------------------------------------- the sections that show them

_HOSTS = {}


def hosts(lst):
    """(guests, away): {section id: [entries shown there, filed elsewhere]} and the set of ids shown away from their
    own section (STYLE 5). The section that holds a moved entry's day: its own where it holds it, else the first dated
    section in the list's order that does; none (the entry stays home) where no section does."""
    key = (id(lst), tuple(len(s.entries) for s in lst.walk()))
    if _HOSTS.get(id(lst), (None,))[0] == key:
        return _HOSTS[id(lst)][1]
    spans = []
    for s in lst.walk():
        lo, hi = s.extra.get("from"), s.extra.get("to")
        if lo and hi:
            spans.append((s, str(lo), str(hi)))
    guests, away = {}, set()
    for sec, e in lst.entries():
        if "when" not in e or not moves(e):
            continue
        day = place_day(e)
        if day is None:
            continue
        iso = day.isoformat()
        mine = sec.extra.get("from") and str(sec.extra["from"]) <= iso <= str(sec.extra.get("to"))
        if mine:
            continue
        host = next((s for s, lo, hi in spans if lo <= iso <= hi), None)
        if host is None:
            continue
        guests.setdefault(host.id, []).append(e)
        away.add(e["id"])
    _HOSTS[id(lst)] = (key, (guests, away))
    return guests, away
