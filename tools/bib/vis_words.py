"""The words that name a polity, for the visibility pass (tools/bib/vis.py): a nationality, a country, a government's
paper, as the name entries' roles, FRUS's lists of persons and its headings, and the witnesses' agents write them.
Read by tools/vis/seed.py to seed sources/polities.yaml and sources/provenance.yaml; by vis.py for a witness's agent
written as words ("British Embassy, Peking").

STYLE
 1. FRUS's convention (its lists of persons): an American official is described without his nationality ("Ambassador
    to the Soviet Union", "Assistant Secretary of State"); a foreign one with it, or with his country after his office
    ("Soviet Ambassador to the United States", "Prime Minister of India"). So role_polity() takes a nationality or a
    country after an office as foreign, and the American posts abroad ("Ambassador to", "Embassy in", "Consul
    General in", "Office of Soviet Union Affairs") as American, whatever country they name.
 2. A word that does not settle the polity is left out: "Chinese" alone (the PRC or the Republic of China), "German"
    alone is the Federal Republic only after an office ("German Ambassador"), as FRUS uses it; "Vietnamese" and
    "Vietnam" alone, in FRUS of 1961-68, the Republic of Vietnam (its volumes' usage: "Ambassador in Vietnam").
 3. Organizations (the UN, NATO, the OAS, the EEC) are named by ORGS: a person whose office is an organization's is
    that organization's (vis.py's STYLE 4: no polity of his own).
"""
import re

# (pattern, polity), the more particular first: "East German" before "German", "North Vietnam" before "Vietnam"
NATIONS = [
    (r"East German|German Democratic Republic|\bGDR\b|East Germany|East Berlin|Neues Deutschland|\bSED\b", "gdr"),
    (r"West German|Federal Republic of Germany|\bFRG\b|West Germany|Federal Republic|Bundestag|Bonn government|"
     r"West Berlin|Frankfurter Allgemeine|Der Spiegel|Die Zeit|Die Welt|Bundesbank|Bundeswehr|\bCDU\b|\bCSU\b|"
     r"\bSPD\b|\bFDP\b", "frg"),
    (r"North Vietnam|Democratic Republic of (?:Viet ?Nam|Vietnam)|\bDRV\b|\bDRVN\b|Lao Dong|Hanoi government|"
     r"Nhân Dân|Học Tập|Quân Đội Nhân Dân|Vietnam News Agency|(?:Viet ?Nam|Vietnam|Vietnamese) Workers['’]? Party|"
     r"Đảng Lao động|Lao Động|Party Center|\bPolitburo\b(?=.*(?:Viet|Hanoi|Lê Duẩn|Workers))|Central Military Party "
     r"Committee|\bVKD\b|Văn kiện Đảng|Van kien Dang", "drv"),
    (r"National Liberation Front|\bNLF\b|Viet ?Cong|Provisional Revolutionary Government|\bPRG\b|\bCOSVN\b|"
     r"Liberation Radio|Liberation Press Agency", "drv"),      # the Front is the DRV's (the owner, Nov. 11, 2026)
    (r"South Vietnam|Republic of (?:Viet ?Nam|Vietnam)|\bRVN\b|\bGVN\b|\bARVN\b|Saigon government", "rvn"),
    (r"Soviet|U\.S\.S\.R\.|\bUSSR\b|\bCPSU\b|Kremlin|Pravda|Izvestia|\bTASS\b|\bTass\b|Krasnaya Zvezda|"
     r"Presidium of the Supreme Soviet|\bKGB\b|\bGRU\b", "ussr"),
    (r"People['’]?s Republic of China|Communist China|Chinese Communist|\bPRC\b|\bCCP\b|Peking government|Renmin Ribao|"
     r"People['’]s Daily|Xinhua|New China News Agency|Red Flag|Hongqi", "prc"),
    (r"Republic of China|Nationalist China|Chinese Nationalist|Taiwan|Formosa|\bGRC\b|Kuomintang|\bKMT\b", "roc"),
    (r"North Korea|Democratic People'?s Republic of Korea|\bDPRK\b", "dprk"),
    (r"South Korea|Republic of Korea|\bROK\b|Korean", "rok"),
    (r"British|United Kingdom|\bU\.K\.|\bUK\b|Great Britain|Britain|Her Majesty|Foreign Office|Whitehall|Hansard|"
     r"\bHMG\b|Manchester Guardian|Daily Telegraph|The Economist|\bBBC\b|Reuters", "uk"),
    (r"French|France|Quai d'Orsay|Élysée|Elysee|Le Monde|Le Figaro|Journal officiel|Agence France", "fr"),
    (r"Cuban|Cuba\b|Granma|Revolución", "cuba"),
    (r"Laotian|\bLaos\b|\bLao\b|Pathet Lao|Neo Lao|Vientiane", "laos"),
    (r"Cambodian|Cambodia|Khmer", "cambodia"),
    (r"Thai\b|Thailand", "thailand"), (r"Burmese|Burma", "burma"),
    (r"Indonesian|Indonesia", "indonesia"), (r"Malaysian|Malaysia|Malaya", "malaysia"),
    (r"Philippine|Philippines|Filipino", "philippines"), (r"Japanese|Japan\b", "japan"),
    (r"Australian|Australia", "australia"), (r"New Zealand", "nz"),
    (r"Indian\b|India\b", "india"), (r"Pakistani|Pakistan", "pakistan"), (r"Ceylon", "ceylon"),
    (r"Nepal", "nepal"), (r"Afghan", "afghanistan"),
    (r"Israeli|Israel\b|Knesset", "israel"),
    (r"United Arab Republic|\bUAR\b|Egyptian|Egypt", "uar"),
    (r"Syrian|Syria", "syria"), (r"Jordanian|Jordan\b", "jordan"), (r"Lebanese|Lebanon", "lebanon"),
    (r"Iraqi|Iraq", "iraq"), (r"Iranian|\bIran\b|Persian|Shah of", "iran"), (r"Saudi", "saudi-arabia"),
    (r"Kuwaiti|Kuwait", "kuwait"), (r"Yemeni|Yemen", "yemen"), (r"Turkish|Turkey", "turkey"),
    (r"Greek|Greece", "greece"), (r"Cypriot|Cyprus", "cyprus"),
    (r"Libyan|Libya", "libya"), (r"Moroccan|Morocco", "morocco"), (r"Algerian|Algeria", "algeria"),
    (r"Tunisian|Tunisia", "tunisia"), (r"Sudanese|Sudan", "sudan"), (r"Ethiopian|Ethiopia", "ethiopia"),
    (r"Kenyan|Kenya", "kenya"), (r"Ghanaian|Ghana", "ghana"), (r"Nigerian|Nigeria|Biafra", "nigeria"),
    (r"Congolese|the Congo|Congo\b|Katanga", "congo"), (r"South African|South Africa|African National Congress", "south-africa"),
    (r"Rhodesian|Rhodesia", "rhodesia"), (r"Guinean|Guinea\b", "guinea"), (r"Tanzania|Tanganyika|Zanzibar", "tanzania"),
    (r"Ivory Coast|Côte d.Ivoire", "ivory-coast"), (r"\bMali\b|Malian", "mali"), (r"Liberia", "liberia"),
    (r"Cameroon", "cameroon"), (r"Upper Volta", "upper-volta"), (r"Dahomey", "dahomey"), (r"\bTogo", "togo"),
    (r"\bNiger\b", "niger"), (r"\bChad\b", "chad"), (r"Gabon", "gabon"), (r"Sierra Leone", "sierra-leone"),
    (r"Mauritania", "mauritania"), (r"Malawi|Nyasaland", "malawi"), (r"Malagasy|Madagascar", "madagascar"),
    (r"Rwanda|Ruanda", "rwanda"), (r"Burundi", "burundi"), (r"Trinidad", "trinidad"), (r"Malta\b|Maltese", "malta"),
    (r"Singapore", "singapore"), (r"Bahrain", "bahrain"), (r"Oman|Muscat", "oman"), (r"Aden\b|South Arabia", "south-arabia"),
    (r"Senegal", "senegal"), (r"Somali", "somalia"), (r"Ugand", "uganda"), (r"Zambia", "zambia"),
    (r"Portuguese|Portugal", "portugal"), (r"Spanish|Spain", "spain"), (r"Italian|Italy", "italy"),
    (r"Belgian|Belgium", "belgium"), (r"Dutch|Netherlands", "netherlands"), (r"Luxembourg", "luxembourg"),
    (r"Norwegian|Norway", "norway"), (r"Swedish|Sweden", "sweden"), (r"Danish|Denmark|Greenland", "denmark"),
    (r"Finnish|Finland", "finland"), (r"Icelandic|Iceland", "iceland"), (r"Irish|Ireland", "ireland"),
    (r"Austrian|Austria", "austria"), (r"Swiss|Switzerland", "switzerland"),
    (r"Polish|Poland", "poland"), (r"Czechoslovak|Czech", "czechoslovakia"), (r"Hungarian|Hungary", "hungary"),
    (r"Yugoslav", "yugoslavia"), (r"Romanian|Rumanian|Romania|Rumania", "romania"), (r"Bulgarian|Bulgaria", "bulgaria"),
    (r"Albanian|Albania", "albania"), (r"Mongolia", "mongolia"),
    (r"Canadian|Canada", "canada"), (r"Mexican|Mexico", "mexico"), (r"Brazilian|Brazil", "brazil"),
    (r"Argentine|Argentina", "argentina"), (r"Chilean|Chile\b", "chile"), (r"Venezuelan|Venezuela", "venezuela"),
    (r"Colombian|Colombia", "colombia"), (r"Peruvian|Peru\b", "peru"), (r"Bolivian|Bolivia", "bolivia"),
    (r"Ecuadorian|Ecuador", "ecuador"), (r"Uruguay", "uruguay"), (r"Paraguay", "paraguay"),
    (r"Panamanian|Panama", "panama"), (r"Nicaragua", "nicaragua"), (r"Guatemala", "guatemala"),
    (r"Hondura", "honduras"), (r"Salvador", "el-salvador"), (r"Costa Rica", "costa-rica"),
    (r"Dominican", "dominican-republic"), (r"Haitian|Haiti", "haiti"), (r"Jamaica", "jamaica"),
    (r"British Guiana|Guyana", "guyana"), (r"Holy See|Vatican|Pope\b|Pontiff", "vatican"),
    (r"Vietnamese|Vietnam|Viet Nam", "rvn"),
    (r"(?:^|\b)German\b|Germany", "frg"),
]
NATIONS = [(re.compile(p), pid) for p, pid in NATIONS]
ORGS = [(re.compile(r"Secretary[- ]General of the United Nations|United Nations Secretary|U\.N\. Secretary|"
                    r"\bUN Secretariat|U\.N\. (?:mediator|representative in)|of the U\.N\.|of the United Nations\b"),
         "un"),
        (re.compile(r"Secretary[- ]General of NATO|NATO Secretary|Supreme Allied Commander"), "nato"),
        (re.compile(r"Secretary[- ]General of the OAS|Organization of American States\b"), "oas"),
        (re.compile(r"International Monetary Fund|\bIMF\b|World Bank|International Bank for Reconstruction"), "imf"),
        (re.compile(r"Organization for European Economic Cooperation|\bOEEC\b|\bOECD\b|Organization for Economic "
                    r"Cooperation"), "oecd"),
        (re.compile(r"European Economic Community|EEC Commission|\bEEC\b|Common Market Commission|Euratom|"
                    r"European Coal and Steel"), "eec")]
# American posts abroad and desks at home: their country names are not the officer's (STYLE 1)
_PLACE = r"(?:the )?[A-Z][\w'.-]*(?: [A-Z][\w'.-]*)*(?:(?:,| and|, and) (?:the )?[A-Z][\w'.-]*(?: [A-Z][\w'.-]*)*)*"
US_POSTS = re.compile(r"(?:Ambassador|Ambassador-[Dd]esignate|Minister|Chargé(?: d'Affaires)?|Counselor|Consul(?: General)?|"
                      r"Representative|Commissioner|Attaché|Adviser|Chief of Mission|Deputy Chief of Mission|"
                      r"Delegate|Political Officer|Officer|Director|Secretary)(?: of Embassy)? (?:in|to|at) " + _PLACE + "|"
                      r"(?:Embass(?:y|ies)|Embasy|Consulates?(?: General)?|Legations?|Missions?|Delegations?|Station|MAAG|"
                      r"AID Mission|USOM|Office|Military Assistance (?:Advisory Group|Command)|Country Team)"
                      r"(?: Office)?(?: in| to| at|,)? " + _PLACE + "|"
                      r"(?:Office|Bureau|Division|Desk|Working Group|Task Force)(?: of| for)? (?:the )?[A-Z][\w'., -]*?"
                      r"(?:Affairs|Desk|Group|Force)\b|"
                      r"(?:Country Director|Desk Officer|Officer in Charge)(?:,)? (?:for |of )?(?:the )?"
                      r"[A-Z][\w'. -]*?(?:Affairs\b|[A-Z][\w'.-]*(?= |,|;|$))|"
                      r"(?:for|on) (?:the )?[A-Z][\w'. -]*?(?:Affairs|Desk|Working Group|Task Force|Coordinating Committee|"
                      r"Program|Matters|Operations|Policy)\b|"
                      r"(?:Consultant|Adviser|Coordinator|Envoy|Conference) (?:on|for) " + _PLACE + "|"
                      r"(?:[A-Z][\w'.-]*(?: [A-Z][\w'.-]*)? )(?:Task Force|Working Group|Study Group|Coordinating Committee|"
                      r"Moratorium Committee|Subcommittee|Affairs)\b|"
                      r"(?:Soviet|Chinese|Asian|European|African|Latin American|Middle Eastern|Vietnamese|French|"
                      r"British|German|Cuban|Laotian|Korean|Japanese|Indian|Israeli|Arab) (?:affairs|specialist|expert|desk|"
                      r"[Aa]ffairs)")
US_MARKS = re.compile(r"Department of (?:State|Defense|the Army|the Navy|the Air Force|Justice|Commerce|Labor|"
                      r"Agriculture|the Treasury|the Interior|Health)|White House|National Security Council|"
                      r"Central Intelligence|\bCIA\b|\bFBI\b|Joint Chiefs|Foreign Service|\bU\.S\.|\bUS\b|"
                      r"United States|American|Senator|Representative from|Congressman|Governor of [A-Z]|"
                      r"Secretary of (?:State|Defense|the Treasury|Agriculture|Commerce|Labor|the Army|the Navy|"
                      r"the Air Force|Health|the Interior)|Attorney General|Assistant to the President|"
                      r"President's|Vice President\b(?! of)|Peace Corps|\bUSIA\b|\bUSIS\b|\bAID\b|\bMACV\b|\bCINCPAC\b|"
                      r"Policy Planning|Bureau of the Budget|Council of Economic Advisers|Federal Reserve|"
                      r"Supreme Court|Court of Appeals|District (?:Court|Judge)|(?:Democratic|Republican) (?:Party|National|Senator|"
                      r"Representative|Governor|leader|nominee|candidate)|AFL-CIO|"
                      r"Atomic Energy Commission|\bNASA\b|National Aeronautics|\bSenate\b|House of Representatives|"
                      r"House (?:Committee|Armed|Foreign|Rules|Ways)|\b(?:CBS|NBC|ABC)\b|Associated Press|United Press|"
                      r"New York Times|Washington Post|Newsweek|\bTime\b magazine|Los Angeles Times|Chicago Tribune|"
                      r"Christian Science Monitor|Wall Street Journal")
# an American institution named before a foreign country: the officer is American ("CIA Station Chief in Saigon")
US_INST = re.compile(r"Department of (?:State|Defense|the Army|the Navy|the Air Force)|White House|National Security "
                     r"Council|\bNSC\b|Central Intelligence|\bCIA\b|\bFBI\b|Joint Chiefs|Foreign Service|\bU\.S\.|\bUSIA\b|"
                     r"\bUSIS\b|\bAID\b|\bMACV\b|\bCINCPAC\b|Peace Corps|Senator|Congressman|Embassy\b")
OFFICE = (r"(?:President|Vice President|Prime Minister|Premier|Chairman|Chancellor|King|Queen|Shah|Emperor|Emir|Amir|"
          r"Sultan|Imam|Ruler|Foreign Minister|Minister|Deputy Prime Minister|Defense Minister|Secretary[- ]General|"
          r"First Secretary|General Secretary|Head of State|Leader|Chief of Staff|Commander|Ambassador|Chargé|"
          r"Governor[- ]General|High Commissioner|Party|Army|Navy|Air Force|Embassy|government|delegation|"
          r"Council|Assembly|parliament|Parliament|opposition|Communist|Socialist|leader|Head|head|Chief|chief|"
          r"Director|Editor|editor|Mayor|mayor|Marshal|General|Admiral|Colonel|Senator|Deputy|deputy|"
          r"Secretary|official|officer|intelligence|diplomat|Representative|representative|delegate|Delegate|"
          r"spokesman|Bishop|Archbishop|Cardinal|Patriarch|monk|Monk|bonze|Bonze|Buddhist)")
OF_COUNTRY = re.compile(OFFICE + r"\b[^;,()]{0,60}? of (?:the )?(?P<c>[A-Z][\w'.-]*(?: [A-Z][\w'.-]*)*)")


def nation(text):
    """The first polity a text's words name (NATIONS), or None."""
    for rx, pid in NATIONS:
        if rx.search(text or ""):
            return pid
    return None


def org(text):
    for rx, oid in ORGS:
        if rx.search(text or ""):
            return oid
    return None


def first_nation(text):
    """The polity of the earliest nationality or country the text names (the longer match first where two start
    together: "East German" before "German"), or None."""
    best = None
    for i, (rx, pid) in enumerate(NATIONS):
        m = rx.search(text or "")
        if m and (best is None or (m.start(), -len(m.group(0)), i) < best[0]):
            best = ((m.start(), -len(m.group(0)), i), pid)
    return best[1] if best else None


HEAD_OFFICE = re.compile(r"^\W*(?:Former |former |Acting |acting |Crown )?(?:King|Queen|Prince|Princess|Emperor|Empress|Shah|"
                         r"President|Prime Minister|Premier|Chancellor|Foreign Minister|Minister|Ambassador|Amir|Emir|"
                         r"Sultan|Chairman|General Secretary|First Secretary|Ruler|Head of State)\b[^;,]{0,40}? of ")


def role_polity(role, default=None, strict=False):
    """A person's polity by a role as FRUS or Part III writes it (STYLE 1): the American posts abroad and desks at home
    taken out, the earliest nationality or country left names it; an organization's office, where none; the United
    States where the role has an American mark; else `default`. `strict` (a role in one of Part III's American
    sections): foreign only where the role opens with a nationality, a country's possessive, or a head of state's or
    a minister's office "of" the country ("King of the Belgians", "Cuba's ambassador to the UN")."""
    r = (role or "").replace("\u2019", "'").replace("\u2018", "'")
    stripped = US_POSTS.sub(" ", r)
    if re.match(r"^\W*(?:U\.S\.|United States|American|USA|USN|USAF|USMC|USAR)\b", stripped):
        return "us"
    c = first_nation(stripped)
    if c and not strict:
        pos = min((m.start() for rx, pid in NATIONS if pid == c for m in [rx.search(stripped)] if m), default=0)
        inst = US_INST.search(stripped)
        if inst and inst.start() < pos:
            return "us"
    if strict:
        head = re.split(r"[;(]", stripped)[0]
        lead = re.match(r"^\W*(?:Former |former )?([A-Z][\w'.-]*(?: [A-Z][\w'.-]*)?)", head)
        lc = first_nation(lead.group(1)) if lead else None
        if lc and not US_MARKS.search(head):
            return lc
        h = HEAD_OFFICE.match(head)
        if h:
            hc = first_nation(" ".join(head[h.end():].split()[:4]))
            if hc:
                return hc
        return "us" if default is None else default
    if c:
        return c
    o = org(r)
    if o:
        return o
    if US_MARKS.search(r) or US_POSTS.search(r):
        return "us"
    return default


def polity_of(text):
    """A witness's agent or place as words ("British Embassy, Peking"; "Department of State"): its polity, or None.
    An American post abroad is American (STYLE 1)."""
    t = text or ""
    if US_POSTS.search(t) and not nation(US_POSTS.sub(" ", t)) or US_MARKS.search(t) and not nation(t.split(",")[0]):
        return "us"
    return first_nation(t.split(",")[0]) or first_nation(t)
