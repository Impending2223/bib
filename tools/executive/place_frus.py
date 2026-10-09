"""Place in the Executive Branch roster the persons FRUS's lists of persons give in a post of the Department of State
or a mission abroad, who are not yet in the roster (the owner's brief: "anyone in the Executive Branch named in ...
any of our FRUS ... documents should be placed").

    python3 tools/executive/place_frus.py [--write]     (without --write, a report only)

Reads sources/frus-names: each person's description in each volume's list of persons (the descriptions of one post
worded volume by volume taken as one: tools/bib/lives.py, same_post), and the dates of the documents that name him.
A description is split into its posts ('Foreign Affairs Officer, Office of European Regional Affairs, after July 12,
1950; Officer in Charge of North Atlantic Treaty Economic and Military Assistance after August 15, 1954'). Each post
goes to the office of the career officers it names (GROUPS: a bureau or office of the Department; MISSIONS: an
embassy, legation, consulate or mission abroad, by its country's region in executive/missions.yaml). A post another
department or agency held (an attaché, AID, USIA, the CIA, the services) is not placed here.

Dates: the description's own ('after July 12, 1950' is from; 'until 1956' is to; '1961-63'); a post that ends where
the next begins ends there; otherwise `seen` and `last`, the first and last documents of the volumes giving the
post that name him ("In office by ...", "Last listed ..."), each with "Check". A post wholly outside Jan. 20, 1953,
to Aug. 31, 1974, is left out. Sources: 'FRUS persons list, 1961–63, XIII and XV', by subseries.

Each holder is written into the office's list in order of taking office, the hand-kept entries untouched.
"""
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bib import store, lives as L                      # noqa: E402
from bib.executive_sources import frus_label           # noqa: E402

START, END = "1953-01-20", "1974-08-31"
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                      "September", "October", "November", "December"], 1)}
MON = "|".join(MONTHS)
DATE = rf"(?:(?:{MON})(?: \d{{1,2}},)? )?(?:19[3-7]\d)"
# a post another department or agency held
NOT_STATE = re.compile(r"\b(?:[Aa]ttach[ée]|Agency for International Development|\bAID\b|USIA|USIS|Information Agency|"
                       r"Central Intelligence|\bCIA\b|Department of (?:Defense|the Army|the Navy|the Air Force|the "
                       r"Treasury|Commerce|Agriculture|Labor|Justice)|Treasury|\bUSA\b|\bUSN\b|\bUSAF\b|\bUSMC\b|"
                       r"Military Assistance Advisory|MAAG|Joint Chiefs|Arms Control and Disarmament Agency|\bACDA\b|"
                       r"International Cooperation Administration|\bICA\b|Foreign Operations Administration|\bFOA\b|"
                       r"Mutual Security Agency|Peace Corps|National Security Council|White House|Bureau of the Budget|"
                       r"Congress|Senator|Representative from|Atomic Energy Commission|Export-Import|NATO Secretariat|"
                       r"SHAPE|United Nations Secretariat|Secretary-General of the United Nations|Drug Enforcement|"
                       r"National Aeronautics|NASA|Commission\b|Federal Reserve|Bureau of Mines|Maritime|Coast Guard|"
                       r"Department of (?:Health|the Interior|Transportation|Housing)|Office of Emergency|"
                       r"Office of Science and Technology|Office of Management|Council of Economic Advisers|"
                       r"Special Representative for Trade|Office of the Special Representative|Politburo|Communist|"
                       r"Chancellor|Democratic Republic|People.s Republic|Embassy in Washington|in the United States|"
                       r"Embassy of|Netherlands|Royal|Prince|King|Federal Republic(?! of Germany)|Government of|"
                       r"Ministry|Parliament|Bundestag|Knesset|Viet Cong|DRV|PRG|NLF|ARVN|RVNAF|Narcotics|Department of Energy|"
                       r"Special Assistant for Science|Office of the President|Mutual Security|Science Adviser)\b")
NAT = (r"British|French|Soviet|Canadian|Australian|Israeli|Indian|Pakistani|Japanese|Chinese|Korean|Vietnamese|Lao|"
       r"Laotian|Thai|Philippine|Indonesian|Iranian|Turkish|Greek|Italian|German|Belgian|Dutch|Norwegian|Danish|Swedish|"
       r"Spanish|Portuguese|Brazilian|Mexican|Argentine|Chilean|Cuban|Egyptian|Jordanian|Saudi|Syrian|Iraqi|Lebanese|"
       r"Afghan|Nepalese|Burmese|Ceylonese|Venezuelan|Colombian|Peruvian|Polish|Czech|Yugoslav|Romanian|Hungarian|"
       r"Austrian|Swiss|Finnish|Irish|Icelandic|Moroccan|Tunisian|Algerian|Libyan|Ethiopian|Nigerian|Ghanaian|"
       r"Congolese|Kenyan|Tanzanian|Malaysian|Singaporean|Cambodian|Uruguayan|Bolivian|Ecuadoran|Panamanian|"
       r"Guatemalan|Honduran|Nicaraguan|Costa Rican|Salvadoran|Dominican|Haitian|Jamaican|Republic of Vietnam|ROK|"
       r"Royal Lao|USSR|U\.S\.S\.R\.|United Kingdom|UK")
# a foreign official: a nationality before an institution or a title ('Turkish Delegation', 'British Foreign Office',
# 'Venezuelan Embassy'), or a foreign ministry; not an American desk ('Office of Soviet Union Affairs')
FOREIGN = re.compile(rf"\b(?:{NAT})\s+(?:\w+\s+)?(?:Embassy|Legation|Delegation|Mission|Ministry|Government|Foreign|"
                     rf"Department|Navy|Army|Air Force|Armed|Representative|Minister|Ambassador|Chargé|Counselor|"
                     rf"Consul|Prime|President|Chief|Head|Permanent|Deputy|Secretary|Cabinet|Parliament|Party|Communist|"
                     rf"Central|National|Defense|Political|Economic|Foreign)|\bMinist(?:ry|er) of (?:Foreign|External)|"
                     rf"Foreign Office|Foreign Ministry|\bof (?:the )?(?:{NAT})\b|, (?:France|Britain|Japan|Germany|"
                     rf"Italy|Israel|India|Pakistan|Iran|Turkey|Greece|Canada|Mexico|Brazil|Egypt)\s*$")
STATE = re.compile(r"\b(?:attach[ée]|Agency for International Development|\bAID\b|USIA|USIS|Information Agency|"
                       r"Central Intelligence|\bCIA\b|Department of (?:Defense|the Army|the Navy|the Air Force|the "
                       r"Treasury|Commerce|Agriculture|Labor|Justice)|Treasury|\bUSA\b|\bUSN\b|\bUSAF\b|\bUSMC\b|"
                       r"Military Assistance|MAAG|Joint Chiefs|Arms Control and Disarmament Agency|\bACDA\b|"
                       r"International Cooperation Administration|\bICA\b|Foreign Operations Administration|\bFOA\b|"
                       r"Mutual Security Agency|Peace Corps|National Security Council|White House|Bureau of the Budget|"
                       r"Congress|Senator|Representative from|Atomic Energy Commission|Export-Import|"
                       r"British|French|Soviet|Canadian|Australian|Israeli|Indian|Pakistani|Japanese|Chinese|Korean|"
                       r"Vietnamese|Lao\b|Thai|Philippine|Indonesian|Iranian|Turkish|Greek|Italian|German|Belgian|"
                       r"Dutch|Norwegian|Danish|Swedish|Spanish|Portuguese|Brazilian|Mexican|Argentine|Chilean|Cuban|"
                       r"Egyptian|Jordanian|Saudi|Syrian|Iraqi|Lebanese|Afghan|Nepal|Burmese|Ceylon|NATO|SHAPE|"
                       r"United Nations Secretariat|Secretary-General of the United Nations)\b")
STATE = re.compile(r"Department of State|Department\b|\bBureau of\b|\bOffice of\b|Division of|Embassy|Legation|"
                   r"Consul|Consulate|Mission to|Delegation|Foreign Service|Policy Planning|Legal Adviser|"
                   r"Executive Secretariat|Operations Center|Protocol|Language Services|Historical Office|"
                   r"Chargé|Chief of Mission|Counselor|First Secretary|Second Secretary|Third Secretary|"
                   r"Political Officer|Economic Officer|Desk Officer|Country Director|Officer in Charge|"
                   r"Foreign Affairs Officer|International Relations Officer|Intelligence and Research")
# the Department's offices of career officers, by the words of the post (the first that fits)
GROUPS = [
    ("legal-adviser-staff", r"Legal Adviser"),
    ("policy-planning-members", r"Policy Planning"),
    ("executive-secretariat-staff", r"Executive Secretariat|Operations Center|Secretariat Staff"),
    ("language-services", r"Language Services|[Ii]nterpreter"),
    ("intelligence-research-officers", r"Intelligence and Research|Intelligence Research|\bINR\b|Research and "
                                       r"Analysis|Office of Research|Intelligence"),
    ("politico-military-officers", r"Politico-Military|Political-Military|Atomic Energy and Aerospace|"
                                   r"International Security Affairs"),
    ("disarmament-officers", r"Disarmament|Atomic Energy|Outer Space"),
    ("educational-cultural-officers", r"Educational and Cultural|Cultural Affairs|Cultural Relations"),
    ("international-organization-officers", r"International Organization|United Nations (?:Political|Economic)|"
                                            r"UN Political|Dependent Area"),
    ("african-officers", r"African Affairs|Office of (?:Northern|Southern|Eastern|Western|Central|West|East|North|"
                         r"South) African|AF/|Bureau of African"),
    ("near-eastern-officers", r"Near East|South Asian|Middle East|NEA\b|Greek|Turkish|Iranian|Arabian|Israel|Arab|"
                              r"Egypt|Iraq|Indian|Pakistan|Afghan|Cyprus|Lebanon|Syria|Jordan"),
    ("far-eastern-officers", r"Far East|East Asian|Asian and Pacific|Southeast Asian|Chinese|China|Japan|Korea|"
                             r"Philippine|Vietnam|Laos|Cambodia|Thai|Indonesia|Burma|Malaysia|Australia|Pacific"),
    ("inter-american-officers", r"Inter-American|Latin American|American Republics|Caribbean|Mexic|Central America|"
                                r"South America|Brazil|Argentin|Chile|Cuba|Panama|Venezuela|Colombia|Peru|Bolivia|"
                                r"Ecuador|Andean|Haiti|Dominican|Guatemala|Honduras|Nicaragua|Costa Rica|Salvador"),
    ("european-officers", r"European|Europe|Atlantic|NATO|German|Soviet|Eastern European|British|French|Italian|"
                          r"Iberian|Scandinavian|Nordic|Benelux|Swiss|Austria|Balkan|Polish|Canadian|Berlin|"
                          r"Commonwealth"),
    ("economic-officers", r"Economic|Trade|Commercial|Commodit|Financ|Monetary|Fuels|Petroleum|Transport|Aviation|"
                          r"Shipping|Telecommunications|Resources|Investment|Business|Agricultur|Food|Tariff"),
    ("public-affairs-officers", r"Public Affairs|Public Studies|Historical|Public Opinion|News|Press"),
    ("department-officers", r"."),
]
NEW_OFFICES = {   # offices this placing adds to executive/state.yaml, after the office named
    "public-affairs-officers": ("deputy-assistant-secretary-public", {
        "id": "public-affairs-officers", "title": "Officers of the Bureau of Public Affairs", "rank": "employee",
        "appt": "CAREER", "under": "assistant-secretary-public", "group": "Functional bureaus", "many": True}),
    "department-officers": ("language-services", {
        "id": "department-officers", "title": "Other officers of the Department", "rank": "employee",
        "appt": "CAREER", "group": "Staff offices", "many": True,
        "n": "Officers whom FRUS's lists of persons give in no bureau or office named in this table."}),
}


def missions_regions():
    """{country or post word: the officers' office in executive/missions.yaml for its region}."""
    d = store.load_yaml(os.path.join(ROOT, "executive", "missions.yaml"))
    office = {"Europe": "officers-europe", "Far East": "officers-far-east", "Near East and South Asia":
              "officers-near-east", "Africa": "officers-africa", "American Republics": "officers-american-republics"}
    out = {}
    for o in d["offices"]:
        g = o.get("group")
        if g in office and not o.get("many"):
            for w in re.split(r"\s*\(|\)|,", o.get("title") or ""):
                w = w.strip()
                if w and len(w) > 3:
                    out[w] = office[g]
    # the capitals and other posts the lists name
    out.update({"Saigon": "vietnam-south-officers", "Moscow": "officers-europe", "London": "officers-europe",
                "Paris": "officers-europe", "Bonn": "officers-europe", "Berlin": "officers-europe",
                "Rome": "officers-europe", "Vienna": "officers-europe", "Brussels": "officers-europe",
                "The Hague": "officers-europe", "Ottawa": "officers-europe", "Geneva": "officers-europe",
                "Tokyo": "officers-far-east", "Seoul": "officers-far-east", "Taipei": "officers-far-east",
                "Bangkok": "officers-far-east", "Vientiane": "officers-far-east", "Phnom Penh": "officers-far-east",
                "Djakarta": "officers-far-east", "Jakarta": "officers-far-east", "Manila": "officers-far-east",
                "Hong Kong": "officers-far-east", "Canberra": "officers-far-east", "Rangoon": "officers-far-east",
                "New Delhi": "officers-near-east", "Karachi": "officers-near-east", "Tehran": "officers-near-east",
                "Ankara": "officers-near-east", "Athens": "officers-near-east", "Cairo": "officers-near-east",
                "Tel Aviv": "officers-near-east", "Beirut": "officers-near-east", "Amman": "officers-near-east",
                "Baghdad": "officers-near-east", "Jidda": "officers-near-east", "Kabul": "officers-near-east",
                "Damascus": "officers-near-east", "Nicosia": "officers-near-east", "Mexico City": "officers-american-republics",
                "Havana": "officers-american-republics", "Rio de Janeiro": "officers-american-republics",
                "Buenos Aires": "officers-american-republics", "Santiago": "officers-american-republics",
                "Caracas": "officers-american-republics", "Bogotá": "officers-american-republics",
                "Lima": "officers-american-republics", "Santo Domingo": "officers-american-republics",
                "Panama": "officers-american-republics", "Leopoldville": "officers-africa",
                "Léopoldville": "officers-africa", "Accra": "officers-africa", "Lagos": "officers-africa",
                "Nairobi": "officers-africa", "Addis Ababa": "officers-africa", "Pretoria": "officers-africa",
                "Algiers": "officers-africa", "Rabat": "officers-africa", "Tunis": "officers-africa",
                "Tripoli": "officers-africa", "Khartoum": "officers-africa", "Salisbury": "officers-africa",
                "Zaire": "officers-africa", "Kinshasa": "officers-africa", "Dar es Salaam": "officers-africa",
                "Dakar": "officers-africa", "Monrovia": "officers-africa", "Kampala": "officers-africa",
                "Mogadiscio": "officers-africa", "Aleppo": "officers-near-east", "Dhahran": "officers-near-east",
                "Istanbul": "officers-near-east", "Jerusalem": "officers-near-east", "Calcutta": "officers-near-east",
                "Bombay": "officers-near-east", "Madras": "officers-near-east", "Lahore": "officers-near-east",
                "Dacca": "officers-near-east", "Colombo": "officers-near-east", "Kathmandu": "officers-near-east",
                "Singapore": "officers-far-east", "Kuala Lumpur": "officers-far-east", "Wellington": "officers-far-east",
                "Hue": "vietnam-south-officers", "Da Nang": "vietnam-south-officers", "Frankfurt": "officers-europe",
                "Munich": "officers-europe", "Hamburg": "officers-europe", "Strasbourg": "officers-europe",
                "Barcelona": "officers-europe", "Madrid": "officers-europe", "Lisbon": "officers-europe",
                "Milan": "officers-europe", "Naples": "officers-europe", "Marseille": "officers-europe",
                "Leningrad": "officers-europe", "Belgrade": "officers-europe", "Warsaw": "officers-europe",
                "Prague": "officers-europe", "Budapest": "officers-europe", "Bucharest": "officers-europe",
                "Sofia": "officers-europe", "Helsinki": "officers-europe", "Stockholm": "officers-europe",
                "Oslo": "officers-europe", "Copenhagen": "officers-europe", "Dublin": "officers-europe",
                "Reykjavik": "officers-europe", "Bern": "officers-europe", "Luxembourg": "officers-europe",
                "Montreal": "officers-europe", "Toronto": "officers-europe", "Sao Paulo": "officers-american-republics",
                "São Paulo": "officers-american-republics", "Montevideo": "officers-american-republics",
                "La Paz": "officers-american-republics", "Quito": "officers-american-republics",
                "Guatemala": "officers-american-republics", "Tegucigalpa": "officers-american-republics",
                "Managua": "officers-american-republics", "San Jose": "officers-american-republics",
                "San Salvador": "officers-american-republics", "Port-au-Prince": "officers-american-republics",
                "Kingston": "officers-american-republics", "Asuncion": "officers-american-republics",
                "Brasilia": "officers-american-republics", "Recife": "officers-american-republics",
                "Brasiliá": "officers-american-republics", "Porto Alegre": "officers-american-republics",
                "Guayaquil": "officers-american-republics", "Colon": "officers-american-republics",
                "Vietnam": "vietnam-south-officers", "Hanoi": "officers-far-east", "Osaka": "officers-far-east",
                "Sri Lanka": "officers-near-east", "Casablanca": "officers-africa", "Tangier": "officers-africa",
                "Lubumbashi": "officers-africa", "Stanleyville": "officers-africa", "Elisabethville": "officers-africa",
                "Quebec": "officers-europe", "Manchester": "officers-europe", "Mission to NATO": "officers-europe",
                "NATO": "officers-europe"})
    return out


def parse_day(s, end=False):
    """'August 15, 1954' -> '1954-08-15'; 'August 1954' -> '1954-08'; '1954' -> '1954'."""
    m = re.match(rf"(?:({MON})(?: (\d{{1,2}}),)? )?(19\d\d)$", s.strip())
    if not m:
        return None
    if m.group(2):
        return f"{m.group(3)}-{MONTHS[m.group(1)]:02d}-{int(m.group(2)):02d}"
    if m.group(1):
        return f"{m.group(3)}-{MONTHS[m.group(1)]:02d}"
    return m.group(3)


def post_dates(clause):
    """(the post's words, from, to) as the clause gives them."""
    t, a, b = clause, None, None
    m = re.search(rf",?\s*\b({DATE})\s*[–-]\s*({DATE}|\d{{2}})\b", t)
    if m:
        a = parse_day(m.group(1))
        y = m.group(2)
        b = parse_day(a[:2] + y if re.fullmatch(r"\d{2}", y) else y)
        t = t[:m.start()] + t[m.end():]
    for word, side in (("after|from|since|as of|beginning|effective", "a"), ("until|to|through|till", "b")):
        m = re.search(rf",?\s*\b(?:{word})\s+({DATE})\b", t)
        if m:
            if side == "a":
                a = a or parse_day(m.group(1))
            else:
                b = b or parse_day(m.group(1))
            t = t[:m.start()] + t[m.end():]
    m = re.search(rf",?\s*\bin ({DATE})\b\s*$", t)     # 'in 1952 and 1953' is left alone; 'in 1969' a year seen
    if m and not (a or b):
        a = b = parse_day(m.group(1))
        t = t[:m.start()]
    m = re.search(r",\s*(19[3-7]\d)\s*$", t)           # 'ACDA/IR Political Affairs Division Chief, 1969'
    if m and not (a or b):
        a = b = m.group(1)
        t = t[:m.start()]
    t = re.sub(r"\s+", " ", t).strip(" ,.;:")
    t = re.sub(r"^(?:and|also|then|later|thereafter|subsequently)\s+", "", t, flags=re.I)
    t = re.sub(r",\s*(?:U\.S\. )?Department of State$", "", t).strip(" ,")
    # a span of days without its year ('January 12-May 6'): the dates are the documents'
    t = re.sub(rf",?\s*(?:{MON}) \d{{1,2}}\s*[–-]\s*(?:(?:{MON}) )?\d{{1,2}}\b", "", t).strip(" ,")
    return t, a, b


def clauses(desc):
    return [c for c in re.split(r";\s*|,?\s*\bthereafter\b,?\s*", desc) if c.strip()]


def where(post, regions):
    """The office of the roster the post goes to, or None where it is no post of the Department's."""
    if NOT_STATE.search(post) or FOREIGN.search(post) or not STATE.search(post):
        return None
    if re.fullmatch(r"(?:Acting )?(?:First|Second|Third) Secretary(?: and Consul)?|Counselor|Minister[- –]Counselor|"
                    r"Consul(?: General)?|Political Officer|Economic Officer|Chargé d.Affaires(?: ad interim)?|"
                    r"International Relations Officer|Foreign Affairs Officer|Consultant", post.strip()):
        return None                           # a title without its post: the list does not say where
    if re.search(r"\b(?:Delegation|Mission)\b", post) and not re.search(r"\b(?:Embassy|Consul|Legation|Chief of Mission|"
                                                                     r"Deputy Chief of Mission)", post):
        if not re.search(r"United States|U\.S\.|\bUS\b|American", post):
            return None                       # a delegation or mission not shown to be the United States'
        if re.search(r"United Nations|General Assembly|\bUN\b|USUN", post):
            return ("state", "international-organization-officers")
        return ("state", "department-officers")
    m = re.search(r"\b(?:Embassy|Legation|Consulate(?: General)?|Consul(?: General)?|Mission|Delegation)\b(?: in| at"
                  r"| to)?(?: the)? ([A-Z][\w’'é-]+(?: [A-Z][\w’'é-]+)*)", post)
    if m and not re.search(r"Mission to the United Nations|Delegation to the (?:United Nations|General Assembly)", post):
        place = m.group(1)
        for w, office in sorted(regions.items(), key=lambda t: -len(t[0])):
            if place.startswith(w) or w == place:
                return ("missions", office)
        for w, office in sorted(regions.items(), key=lambda t: -len(t[0])):   # 'Consul General in Aleppo, Syria'
            if re.search(rf"\b{re.escape(w)}\b", post):
                return ("missions", office)
        return None                           # a post abroad not placed by region: left for a reader
    # a title of a mission abroad with its country ('First Secretary in Pakistan'): the region's embassy officers
    if re.search(r"\b(?:First|Second|Third) Secretary|\bCounselor\b|\bConsul\b|Minister[- –]Counselor|Chargé|"
                 r"Deputy Chief of Mission|Political Officer|Economic Officer|Public Affairs Officer", post) \
            and not re.search(r"\b(?:Bureau|Office) of\b|Department", post):
        for w, office in sorted(regions.items(), key=lambda t: -len(t[0])):
            if re.search(rf"\b{re.escape(w)}\b", post):
                return ("missions", office)
    # the bureau the post names decides ('Political Military Adviser, Bureau of Near Eastern, South Asian, and African
    # Affairs' is the Near Eastern bureau's, which held Africa to 1958)
    m = re.search(r"\bBureau (?:of|for) ((?:[^,;]|, (?:South Asian|and))+?)(?:,|;|$)", post)
    if m:
        name = m.group(1)
        if re.search(r"Near Eastern", name):
            return ("state", "near-eastern-officers")
        for office, rx in GROUPS[:-1]:
            if re.search(rx, name):
                return ("state", office)
    bureau = {"officers-europe": "european-officers", "officers-far-east": "far-eastern-officers",
              "vietnam-south-officers": "far-eastern-officers", "officers-near-east": "near-eastern-officers",
              "officers-africa": "african-officers", "officers-american-republics": "inter-american-officers"}
    for office, rx in GROUPS:
        if office == "african-officers":     # a desk that names a country: that country's regional bureau
            for w, mo in sorted(regions.items(), key=lambda t: -len(t[0])):
                if len(w) > 4 and mo in bureau and re.search(rf"\b{re.escape(w[:max(5, len(w) - 1)])}", post) and \
                        re.search(r"Affairs|Desk|Country Director|Officer[- ]in[- ]Charge", post):
                    return ("state", bureau[mo])
        if re.search(rx, post):
            return ("state", office)
    return None


def lo(d):
    return str(d) + ("-01-01" if len(str(d)) == 4 else "-01" if len(str(d)) == 7 else "")


def hi(d):
    return str(d) + ("-12-31" if len(str(d)) == 4 else "-28" if len(str(d)) == 7 else "")


def roster_names():
    names = set()
    for f in os.listdir(os.path.join(ROOT, "executive")):
        if f.endswith(".yaml"):
            d = store.load_yaml(os.path.join(ROOT, "executive", f)) or {}
            for o in d.get("offices") or []:
                for h in o.get("holders") or []:
                    names.add(h.get("name"))
    return names


def placements(series):
    regions = missions_regions()
    held = roster_names()
    out, skipped = [], []
    for p in L.everyone(series):
        if p["names"] & held or L.natural(p["name"]):     # a name in its own order: a foreign official
            continue
        d = L.letter_json("frus-names", L.key_of(p["name"])[:1].upper()).get(L.key_of(p["name"]), {})
        if not d:
            continue
        # one post worded volume by volume, one entry (same_post)
        groups = []
        for vol in sorted(d, key=L.vol_order):
            r = L.run_on((d[vol].get("role") or "").strip(), L.key_of(p["name"]))
            if not r:
                continue
            g = next((g for g in groups if L.same_post(r, g[0])), None)
            if g:
                g[1].append(vol)
            else:
                groups.append([r, [vol]])
        for desc, vols in groups:
            days = sorted(x[1] for v in vols for x in d[v]["named"] + d[v]["sent"] if x[1])
            cl = [post_dates(c) for c in clauses(desc)]
            for i, (post, a, b) in enumerate(cl):
                w = where(post, regions)
                if not w:
                    if post and STATE.search(post) and not (NOT_STATE.search(post) or FOREIGN.search(post)):
                        skipped.append((p["name"], post))
                    continue
                if not b and i + 1 < len(cl) and cl[i + 1][1]:
                    b = cl[i + 1][1]          # ends where the next post begins
                h = {"name": p["name"], "title": post[0].upper() + post[1:]}
                check = []
                if a:
                    h["from"] = a
                elif days:
                    h["seen"] = days[0]
                    check.append("the start")
                else:
                    continue
                if b:
                    h["to"] = b
                elif days:
                    h["last"] = max(days[-1], str(h.get("from") or h.get("seen")))
                    check.append("the end")
                else:
                    h["last"] = h.get("from") or h.get("seen")
                    check.append("the end")
                start = h.get("from") or h.get("seen")
                stop = h.get("to") or h.get("last")
                if hi(stop) < START or lo(start) > END or hi(stop) < lo(start):
                    continue
                if check:
                    h["n"] = "Check " + " and ".join(check) + ": the dates of the FRUS documents that name him."
                subs = {}
                for v in vols:
                    lab = frus_label(v)[5:]            # '1961–63, XIII'; '1952–54, Guatemala'
                    sub, _, vol = lab.partition(", ")
                    vol = vol.split(",")[0]
                    if vol not in subs.setdefault(sub, []):
                        subs[sub].append(vol)
                h["src"] = [f"FRUS persons list, {s}, " + " and ".join(vs) for s, vs in subs.items()]
                out.append((w, h))
    # one post of one person in one office, worded twice ('Political Military Adviser', 'Political-Military
    # Adviser'): one holder, from the earliest day to the latest, the sources together
    merged = []
    for w, h in out:
        prev = next((x for x in merged if x[0] == w and x[1]["name"] == h["name"] and L.same_post(x[1]["title"], h["title"])),
                    None)
        if not prev:
            merged.append((w, h))
            continue
        g = prev[1]
        a1, a2 = g.get("from") or g.get("seen"), h.get("from") or h.get("seen")
        if lo(a2) < lo(a1):
            g.pop("from", None), g.pop("seen", None)
            g["from" if h.get("from") else "seen"] = a2
        b1, b2 = g.get("to") or g.get("last"), h.get("to") or h.get("last")
        if hi(b2) > hi(b1):
            g.pop("to", None), g.pop("last", None)
            g["to" if h.get("to") else "last"] = b2
        g["src"] = list(dict.fromkeys(g["src"] + h["src"]))
        check = [x for x, k in (("the start", "seen"), ("the end", "last")) if g.get(k)]
        g.pop("n", None)
        if check:
            g["n"] = "Check " + " and ".join(check) + ": the dates of the FRUS documents that name him."
    return merged, skipped


def holder_text(h):
    import yaml
    body = yaml.safe_dump([h], allow_unicode=True, sort_keys=False, width=110, default_flow_style=False)
    # dates and flow style as the hand-kept files write them
    lines = []
    for ln in body.rstrip("\n").split("\n"):
        lines.append("      " + ln)
    return "\n".join(lines)


def write(unit, office, hs, new=None):
    """Insert holders hs into office's list in executive/<unit>.yaml in order of taking office."""
    path = os.path.join(ROOT, "executive", f"{unit}.yaml")
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    if new and f"  - id: {office}" not in text:
        after, o = new
        i = next(k for k, ln in enumerate(lines) if ln == f"  - id: {after}")
        j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith("  - id: ")), len(lines))
        import yaml
        block = yaml.safe_dump([dict(o, holders=[])], allow_unicode=True, sort_keys=False, width=110).rstrip("\n")
        block = "\n".join("  " + ln for ln in block.split("\n")).replace("holders: []", "holders:")
        lines[j:j] = block.split("\n")
    i = next(k for k, ln in enumerate(lines) if ln == f"  - id: {office}")
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith("  - id: ")), len(lines))
    while j > i and not lines[j - 1].strip():
        j -= 1
    hk = next((k for k in range(i, j) if lines[k].strip() == "holders:" or lines[k].strip() == "holders: []"), None)
    if hk is None:
        lines.insert(j, "    holders:")
        hk, j = j, j + 1
    lines[hk] = "    holders:"
    # the existing holders, as text chunks, with their dates from the file
    import yaml
    d = yaml.safe_load("\n".join(lines))            # the text as it now stands, the new office included
    o = next(x for x in d["offices"] if x["id"] == office)
    old = o.get("holders") or []
    starts = [k for k in range(hk + 1, j) if lines[k].startswith("      - ")]
    chunks = [lines[s:(starts[n + 1] if n + 1 < len(starts) else j)] for n, s in enumerate(starts)]
    assert len(chunks) == len(old), (unit, office, len(chunks), len(old))
    from bib.executive import lo as xlo                # the roster's own order: '1958' before '1958-01-02'
    key = lambda h: xlo(str(h.get("from") or h.get("seen")))
    items = [(key(h), 0, n, "\n".join(c)) for n, (h, c) in enumerate(zip(old, chunks))]
    have = {(h.get("name"), h.get("title")) for h in old}
    for n, h in enumerate(hs):
        if (h["name"], h["title"]) in have:
            continue
        have.add((h["name"], h["title"]))
        items.append((key(h), 1, n, holder_text(h)))
    items.sort(key=lambda t: (t[0], t[1], t[2]))
    lines[hk + 1:j] = "\n".join(t[3] for t in items).split("\n")
    open(path, "w", encoding="utf-8").write("\n".join(lines))


def main():
    series = store.Series()
    out, skipped = placements(series)
    by = {}
    for (unit, office), h in out:
        by.setdefault((unit, office), []).append(h)
    persons = {h["name"] for _, h in out}
    print(f"{len(out)} posts of {len(persons)} persons", file=sys.stderr)
    for k, v in sorted(by.items(), key=lambda t: -len(t[1])):
        print(f"  {k[0]}.{k[1]}: {len(v)}", file=sys.stderr)
    print(f"{len(skipped)} posts of the Department not placed (abroad, by no known region)", file=sys.stderr)
    if "--write" in sys.argv:
        for (unit, office), hs in by.items():
            write(unit, office, hs, NEW_OFFICES.get(office))
    else:
        for (unit, office), hs in list(by.items())[:3]:
            for h in hs[:3]:
                print(holder_text(h))
        for s in skipped[:30]:
            print("not placed:", s)


if __name__ == "__main__":
    main()
