"""A calendar entry's dateline: its place and time of day at the right of its rubric (the owner, Nov. 18, 2026: "Implement
(a), threads wrap and date stays, vague times as words, and Washington when the day differs ... Keep everything in plain
Roman ... Default to showing the times. Don't give a toggle").

STYLE
 1. The line: the rubric (the threads) at the left, the dateline at the right, on one line; a rubric too long for the
    room ends in an ellipsis flush to its last letter, and a tap on it wraps it below within the same right edge, the
    dateline staying where it is (the preview's (a)). Plain roman, the rubric's sans, muted, one weight.
 2. The time, from the entry's fields (dayorder.py), its start only (the owner, Nov. 19, 2026: "Set the dateline to
    show only the first, start times. Keep the balance of the information either somewhere hidden or in the citation
    block, but keep the display line clean"): `time` an hour ("11:30 a.m."; "about 4 p.m." where `time_approx`); a
    `time_range` from the record its start ("10:20 a.m.", not "10:20–11:20 a.m."); a range from the event's kind
    (`range_basis: kind`), or any range a reader gave a `time_band` (the record's "morning", 上午), its band as words
    ("workday", "early morning", "election night", "morning", "before dawn"), a word, not a range or its start shown,
    but only where the range is the band's own hours (dayorder.band_range): hours of record a reader also gave a band
    word show their start ("10:30 a.m.", not "workday"), the range and Washington's in the title; a band of the
    record's own hours keeps Washington's day in the title, "morning (Jan. 5 Wash.)", no hour, none having been
    recorded (STYLE 4: "the balance ... somewhere hidden"); no time, no dateline. Noon is "12:00 p.m." (the owner,
    Nov. 19, 2026: "Write 'noon' as '12:00 p.m.'"), in a span "12:00–2 p.m."; midnight "12:00 a.m." (Nov. 19,
    about 10:45 a.m.: "Yes, '12:00 a.m.'"), "10 p.m.–12:00 a.m.", "12:00–6 a.m."; in the datelines only, the
    notes' prose as written (the same: "Datelines only").
 3. The place: the entry's `place:` (places.py; the first of two), its gazetteer name without a leading article
    ("LBJ Ranch", "Plain of Jars": the owner, Nov. 27, 2026; `_bare`); else, until the location pass
    reaches it, its city (`city:` tag), else its State (`state:`), else its zone's city (Washington for the eastern
    zone, Peking, Moscow, Saigon ...). The clock: `time_zone`, else the place's zone; an exact time with neither
    takes its thread's (the Chinese leadership's Peking, the Soviet's Moscow), else Washington's, shown as "Wash."
    after the hour, no place.
 4. Washington when the day differs: where the local day is not Washington's, "(Mar. 10, 11 p.m. Wash.)", not on
    the line but in its `title` (shown on hover or a long press), with the range's end: the title is the dateline in
    full ("Peking · 10–11 a.m. (Mar. 10, 9 p.m. Wash.)"), given only where it says more than the line.
 5. The place's page: a place in the line that has a page of its own (a city, a State, a province) links to it, in
    the site's one style for its own links (placepages.py, STYLE 6); a tap on it follows it, never opening the rubric.
"""
import datetime
import html
import re
from zoneinfo import ZoneInfo

from . import store

WASH = ZoneInfo("America/New_York")
MON = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
BAND = {"workday daytime": "workday", "workday afternoon": "afternoon", "workday midday": "midday",
        "workday morning": "morning", "pre-work morning": "early morning", "early morning": "early morning",
        "election night": "election night", "afternoon": "afternoon", "evening": "evening", "morning": "morning",
        "night": "night", "daytime": "daytime", "midday": "midday", "after-workday daytime": "evening",
        "predawn": "before dawn"}
ZONE = {"America/New_York": "Washington", "Asia/Shanghai": "Peking", "Europe/Moscow": "Moscow",
        "Asia/Ho_Chi_Minh": "Saigon", "Europe/Berlin": "Germany", "Etc/GMT+6": "Texas",
        "America/Kentucky/Louisville": "Louisville", "America/Indiana/Indianapolis": "Indianapolis",
        "Asia/Yangon": "Rangoon", "Asia/Kolkata": "New Delhi", "Europe/Tirane": "Tirana", "Asia/Ulaanbaatar": "Ulan Bator",
        "Africa/Kinshasa": "Léopoldville", "Asia/Karachi": "Karachi", "Asia/Dhaka": "Dacca", "Asia/Colombo": "Colombo",
        "Europe/Bucharest": "Bucharest", "Asia/Jakarta": "Djakarta", "Asia/Phnom_Penh": "Phnom Penh",
        "Asia/Vientiane": "Vientiane", "Pacific/Honolulu": "Honolulu"}
CITY = {"nyc": "New York", "washington": "Washington", "los-angeles": "Los Angeles", "san-francisco": "San Francisco",
        "new-orleans": "New Orleans", "st-louis": "St. Louis", "st-augustine": "St. Augustine", "kansas-city": "Kansas City"}
_STATES = None


def _state(code):
    global _STATES
    if _STATES is None:
        import os
        rows = store.load_yaml(os.path.join(store.ROOT, "sources", "states.yaml")) or []
        _STATES = {str(r.get("st", "")).lower(): r.get("name") for r in rows if isinstance(r, dict)}
    return _STATES.get(code.lower())


def _city(slug):
    if slug in CITY:
        return CITY[slug]
    parts = slug.split("-")
    if len(parts) > 1 and len(parts[-1]) == 2 and _state(parts[-1]):
        parts = parts[:-1]                              # "albany-ga": Albany
    return " ".join(p.capitalize() for p in parts)


def _hour(dt):
    if dt.minute == 0 and dt.hour in (0, 12):
        return "12:00"                                  # noon, midnight (STYLE 2)
    h = dt.hour % 12 or 12
    return f"{h}:{dt.minute:02d}" if dt.minute else f"{h}"


def _mer(dt):
    return " a.m." if dt.hour < 12 else " p.m."


def _clock(dt):
    return _hour(dt) + _mer(dt)


def _span(a, b):
    if _mer(a) == _mer(b) and _mer(a):
        return f"{_hour(a)}–{_hour(b)}{_mer(b)}"
    return f"{_clock(a)}–{_clock(b)}"


def _utc(x):
    return datetime.datetime.fromisoformat(str(x).replace("Z", "+00:00"))


def _tags(e, ns):
    return [str(t)[len(ns) + 1:] for t in store.as_list(e.get("tags")) if str(t).startswith(ns + ":")]


def _zlabel(zone, e):
    if zone == "Asia/Bangkok":                          # Hanoi's clock (+7) as the zone database keeps it
        return "Hanoi" if "hanoi" in str(e.get("thread") or "") else "Bangkok"
    return ZONE.get(zone, (zone or "").split("/")[-1].replace("_", " "))


def _guess(e):
    t = str(e.get("thread") or "")
    if t.startswith("china"):
        return "Asia/Shanghai"
    if t.startswith("soviet"):
        return "Europe/Moscow"
    return None


def _conventional(e, zone):
    """Whether a range with a band word is the band's own hours (dayorder.band_range: none recorded), not hours of
    record that a reader also gave a word ("10:30 a.m.–5 p.m.", "workday")."""
    from . import dayorder
    band, r = str(e.get("time_band")), e.get("time_range")
    if band not in dayorder.BANDS or not zone:
        return False
    try:
        conv = [_utc(x) for x in dayorder.band_range(str(e.get("date"))[:10], band, zone)]
        got = [_utc(x) for x in r[:2]]
    except Exception:
        return False
    if got == conv:
        return True
    # a band's hours set an hour off at one end in a zone that changes its clocks that year (summer time taken for
    # standard, or the reverse, when the range was written): still the band's own, not hours of record
    off = [abs((x - y).total_seconds()) for x, y in zip(got, conv)]
    return sorted(off) == [0, 3600] and _shifts(zone, got[0].year)


def _shifts(zone, year):
    """Whether the zone's clocks change in the year (summer time)."""
    import datetime
    z = ZoneInfo(zone)
    return datetime.datetime(year, 1, 15, tzinfo=z).utcoffset() != datetime.datetime(year, 7, 15, tzinfo=z).utcoffset()


def _wash_days(a, b):
    """Washington's day or days for a band from a to b, local ("Jan. 5", "Jan. 9–10"), where not the local day."""
    import datetime
    w1, w2 = a.astimezone(WASH).date(), (b - datetime.timedelta(minutes=1)).astimezone(WASH).date()
    if w1 == w2 == a.date():
        return ""
    if w1 == w2:
        return f"{MON[w1.month - 1]} {w1.day}"
    if w1.month == w2.month:
        return f"{MON[w1.month - 1]} {w1.day}–{w2.day}"
    return f"{MON[w1.month - 1]} {w1.day}–{MON[w2.month - 1]} {w2.day}"


def _bare(name):
    """A dateline's place without a leading article: "LBJ Ranch", "Plain of Jars" (the owner, Nov. 27, 2026: "Shouldn't
    'the LBJ Ranch' dateline read 'LBJ Ranch'?"); the gazetteer's name, article and all, stays for running text."""
    return re.sub(r"^the ", "", str(name)) if name else name


def parts(e):
    """(the line, the dateline in full): the line its start alone, the full its range and Washington's hour where the
    day differs (STYLE 2, 4); ('', '') where there is no time."""
    t, r = e.get("time"), e.get("time_range")
    if not t and not r:
        return "", ""
    from . import places
    pr = places.first(e)
    zone = e.get("time_zone") or (pr.get("zone") if pr else None) or (_guess(e) if t else None)
    wash_only = t and not zone
    try:
        lz = ZoneInfo(zone) if zone else WASH
    except Exception:
        lz, wash_only = WASH, True
    city, st = _tags(e, "city"), _tags(e, "state")
    if pr:
        place, wash_only = _bare(places.name_on(pr, e.get("date"))), False
    else:
        place = None if wash_only else (_city(city[0]) if city and e.get("time_zone") else
                                        (_state(st[0]) if st and e.get("time_zone") else _zlabel(zone, e)))
    if t:
        a = _utc(t).astimezone(lz)
        when = full = ("about " if e.get("time_approx") else "") + _clock(a)
        start = a
    else:
        a, b = (_utc(x).astimezone(lz) for x in r[:2])
        start = a
        if e.get("range_basis") == "kind" or e.get("time_band") == "election night":
            band = str(e.get("time_band") or "")
            when = full = BAND.get(band, band)
            start = None                                 # a kind's band: no hours of record, none against Washington's
        elif e.get("time_band") and _conventional(e, zone or "America/New_York"):
            band = str(e.get("time_band"))               # a band of record ("morning", 上午), its hours the band's own:
            when = full = BAND.get(band, band)           # its word; in the title Washington's day, no hour (none was
            wd = _wash_days(a, b)                        # recorded) (STYLE 2, 4)
            if wd:
                full += f" ({wd} Wash.)"
            start = None
        else:                                            # hours of record, a band word or not: the start
            when, full = _clock(a), _span(a, b)
    if not when:
        return "", ""
    if wash_only:
        return f"{when} Wash.", f"{full} Wash."
    line = f"{place} · {when}" if place else when
    whole = f"{place} · {full}" if place else full
    if start is not None and zone != "America/New_York":
        w = start.astimezone(WASH)
        if w.date() != start.date():
            whole += f" ({MON[w.month - 1]} {w.day}, {_clock(w)} Wash.)"
    return line, whole


def text(e):
    """The dateline's text, its start alone, or '' (STYLE 2-4)."""
    return parts(e)[0]


def full(e):
    """The dateline in full (its `title`), or '' (STYLE 4)."""
    return parts(e)[1]


def html_(e):
    s, whole = parts(e)
    if not s:
        return ""
    title = f' title="{html.escape(whole)}"' if whole != s else ""
    inner = html.escape(s)
    place = s.split(" · ", 1)[0] if " · " in s else None
    if place:                           # the place's page, where it has one (placepages.py, STYLE 6)
        from . import placepages
        href = placepages.dateline_link(e, place)
        if href:
            inner = f'<a href="{href}.html">{html.escape(place)}</a>' + html.escape(s[len(place):])
    return f'<span class="dl"{title}>{inner}</span>'


STYLE = """<style id="dlstyle">
/* the dateline at the right of an entry's rubric (tools/bib/dateline.py, STYLE 1) */
.rubrow{display:flex;align-items:baseline;gap:.6rem;min-width:0}
.rubrow>.s.rub{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rubrow.clip>.s.rub{cursor:pointer}
.rubrow.open>.s.rub{white-space:normal;overflow:visible}
.rubrow>.dl{flex:none;font-family:var(--sans);font-size:.7rem;line-height:1.2;color:var(--muted);white-space:nowrap;
  font-variant-numeric:tabular-nums;text-align:right}
.rubrow>.dl[title]{cursor:help}
</style>"""

SCRIPT = """<script>
/* a rubric cut short by its dateline: its ellipsis, and a tap that opens it (tools/bib/dateline.py, STYLE 1) */
(function(){
  function mark(){[].forEach.call(document.querySelectorAll('.rubrow'),function(r){
    if(r.classList.contains('open'))return; var s=r.firstElementChild;
    r.classList.toggle('clip', s.scrollWidth>s.clientWidth+1);});}
  document.addEventListener('click',function(ev){var r=ev.target.closest&&ev.target.closest('.rubrow.clip');
    if(!r||r.classList.contains('open')||ev.target.closest('.dl a'))return; ev.preventDefault(); r.classList.add('open'); r.classList.remove('clip');},true);
  window.addEventListener('resize',mark); window.addEventListener('load',mark);
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(mark);
  document.addEventListener('toggle',mark,true); setTimeout(mark,0);
})();
</script>"""
