"""A calendar entry's dateline: its place and time of day at the right of its rubric (the owner, Nov. 18, 2026: "Implement
(a), threads wrap and date stays, vague times as words, and Washington when the day differs ... Keep everything in plain
Roman ... Default to showing the times. Don't give a toggle").

STYLE
 1. The line: the rubric (the threads) at the left, the dateline at the right, on one line; a rubric too long for the
    room ends in an ellipsis flush to its last letter, and a tap on it wraps it below within the same right edge, the
    dateline staying where it is (the preview's (a)). Plain roman, the rubric's sans, muted, one weight.
 2. The time, from the entry's fields (dayorder.py): `time` an hour ("11:30 a.m.", "noon"; "about 4 p.m." where
    `time_approx`); a `time_range` from the record its hours ("10:20–11:20 a.m."); a range from the event's kind
    (`range_basis: kind`) its band as words ("workday", "early morning", "election night"); no time, no dateline.
 3. The place: the entry's city (`city:` tag), else its State (`state:`), else its zone's city (Washington for the
    eastern zone, Peking, Moscow, Saigon ...). An exact time with no zone stored takes its thread's (the Chinese
    leadership's Peking, the Soviet's Moscow), else Washington's, shown as "Wash." after the hour, no place.
 4. Washington when the day differs: where the local day is not Washington's, "(Mar. 10, 11 p.m. Wash.)" after.
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
        "night": "night", "daytime": "daytime", "midday": "midday"}
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
    if dt.hour == 12 and dt.minute == 0:
        return "noon"
    if dt.hour == 0 and dt.minute == 0:
        return "midnight"
    h = dt.hour % 12 or 12
    return f"{h}:{dt.minute:02d}" if dt.minute else f"{h}"


def _mer(dt):
    return "" if (dt.hour, dt.minute) in ((12, 0), (0, 0)) else (" a.m." if dt.hour < 12 else " p.m.")


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


def text(e):
    """The dateline's text, or '' (STYLE 2-4)."""
    t, r = e.get("time"), e.get("time_range")
    if not t and not r:
        return ""
    zone = e.get("time_zone") or (_guess(e) if t else None)
    wash_only = t and not zone
    try:
        lz = ZoneInfo(zone) if zone else WASH
    except Exception:
        lz, wash_only = WASH, True
    city, st = _tags(e, "city"), _tags(e, "state")
    place = None if wash_only else (_city(city[0]) if city and e.get("time_zone") else
                                    (_state(st[0]) if st and e.get("time_zone") else _zlabel(zone, e)))
    if t:
        a = _utc(t).astimezone(lz)
        when = ("about " if e.get("time_approx") else "") + _clock(a)
        start = a
    else:
        a, b = (_utc(x).astimezone(lz) for x in r[:2])
        start = a
        if e.get("range_basis") == "kind" or e.get("time_band") == "election night":
            band = str(e.get("time_band") or "")
            when = BAND.get(band, band)
            start = None                                 # a kind's band: no hour to set against Washington's
        else:
            when = _span(a, b)
    if not when:
        return ""
    if wash_only:
        return f"{when} Wash."
    out = f"{place} · {when}" if place else when
    if start is not None and zone != "America/New_York":
        w = start.astimezone(WASH)
        if w.date() != start.date():
            out += f" ({MON[w.month - 1]} {w.day}, {_clock(w)} Wash.)"
    return out


def html_(e):
    s = text(e)
    return f'<span class="dl">{html.escape(s)}</span>' if s else ""


STYLE = """<style id="dlstyle">
/* the dateline at the right of an entry's rubric (tools/bib/dateline.py, STYLE 1) */
.rubrow{display:flex;align-items:baseline;gap:.6rem;min-width:0}
.rubrow>.s.rub{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rubrow.clip>.s.rub{cursor:pointer}
.rubrow.open>.s.rub{white-space:normal;overflow:visible}
.rubrow>.dl{flex:none;font-family:var(--sans);font-size:.7rem;line-height:1.2;color:var(--muted);white-space:nowrap;
  font-variant-numeric:tabular-nums;text-align:right}
</style>"""

SCRIPT = """<script>
/* a rubric cut short by its dateline: its ellipsis, and a tap that opens it (tools/bib/dateline.py, STYLE 1) */
(function(){
  function mark(){[].forEach.call(document.querySelectorAll('.rubrow'),function(r){
    if(r.classList.contains('open'))return; var s=r.firstElementChild;
    r.classList.toggle('clip', s.scrollWidth>s.clientWidth+1);});}
  document.addEventListener('click',function(ev){var r=ev.target.closest&&ev.target.closest('.rubrow.clip');
    if(!r||r.classList.contains('open'))return; ev.preventDefault(); r.classList.add('open'); r.classList.remove('clip');},true);
  window.addEventListener('resize',mark); window.addEventListener('load',mark);
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(mark);
  document.addEventListener('toggle',mark,true); setTimeout(mark,0);
})();
</script>"""
