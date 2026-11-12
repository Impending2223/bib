"""Seed the visibility pass's two registries from what the series already says (rerunnable; tools/bib/vis.py, its STYLE;
the spec, notes/proposals/visibility-spec.md §8, §9.1).

    python3 -I tools/vis/seed.py [--dry-run] [--refresh]

    sources/provenance.yaml   series (periodicals, official series, document series, archives: SERIES below, by hand
                              here), FRUS's volumes' years (read off the notes and cards that print them: "Made public:
                              FRUS 1964-68, VI (2002)"; never fetched), FRUS documents' parties (their headings in the
                              daybook and sources/frus-text/), publishers, and every card the calendar cites
    sources/polities.yaml     the polities; every person the calendar tags; the place tags; the threads

A row already in a file is kept as it is (a hand edit wins); a new key is added. --refresh rewrites the seeded rows
too (a hand row marked `hand: true` is kept even then).

STYLE
 1. Persons (polities.yaml `names`): by Part III's role and section (the foreign sections: K-J Adm. III.J and Adm.
    III.J, Abroad; Viet. III.G, South Vietnam; III.H, North Vietnam and the Front; III.I, Others abroad); else the
    rosters (an Executive Branch holder, a member of Congress: the United States); else FRUS's lists of persons, by
    each volume's description (tools/bib/vis_words.py, STYLE 1), a change of polity between volumes kept as dated
    ranges and marked doubtful; else `?`. `basis` says which.
 2. Works (provenance.yaml `works`): the kind from the card or its listing (a memoir: listed under its author as
    subject, or titled so; a diary or oral history: titled so; the tapes and the documents sections: document
    series; a FRUS, Pentagon Papers or command-history card: document series; a case: official; else scholarship);
    the year from the card, `?` where the card is a later edition (its paren: "2d ed.", "trans.", "rev. ed."); the
    country from what the card itself shows (an American government author or title; a network; a journal of
    JOURNALS; a place of publication it prints), else `?`: the cards hold no publisher (tools/bib/works.py, STYLE 5).
 3. FRUS's volumes: the year most of the notes give a volume; a volume given two years is written with the
    majority's and listed under `frus_volume_doubts` with the other.
"""
import collections
import glob
import json
import lzma
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from tools.bib import store, vis, vis_words  # noqa: E402

PROV, POL = vis.PROV, vis.POL

# ---------------------------------------------------------------- the polities (spec §2)

POLITIES = {
    "us": {"name": "United States", "tag": "US", "top": True},
    "ussr": {"name": "Soviet Union", "tag": "USSR", "top": True, "until": "1991-12-26"},
    "prc": {"name": "China (the People's Republic)", "tag": "PRC", "top": True},
    "fr": {"name": "France", "tag": "FR", "top": True},
    "frg": {"name": "Germany (the Federal Republic)", "tag": "FRG", "top": True},
    "uk": {"name": "United Kingdom", "tag": "UK", "top": True},
    "gdr": {"name": "German Democratic Republic", "tag": "GDR", "until": "1990-10-03"},
    "drv": {"name": "Democratic Republic of Vietnam", "tag": "DRV", "until": "1976-07-02", "then": "srv"},
    "srv": {"name": "Socialist Republic of Vietnam", "tag": "SRV", "from": "1976-07-02"},
    "rvn": {"name": "Republic of Vietnam", "tag": "RVN", "until": "1975-04-30"},
    "nlf": {"name": "National Liberation Front (the PRG from 1969)", "tag": "NLF",
            "doubtful": "a front, not a state; kept apart from the DRV until the owner rules"},
    "roc": {"name": "Republic of China", "tag": "ROC"},
    "rok": {"name": "Republic of Korea", "tag": "ROK"}, "dprk": {"name": "North Korea", "tag": "DPRK"},
    "cuba": {"name": "Cuba", "tag": "CUBA"}, "laos": {"name": "Laos", "tag": "LAOS"},
    "cambodia": {"name": "Cambodia", "tag": "CAMBODIA"}, "uar": {"name": "United Arab Republic (Egypt)", "tag": "UAR"},
    "un": {"name": "United Nations", "tag": "UN", "org": True}, "nato": {"name": "NATO", "tag": "NATO", "org": True},
    "oas": {"name": "Organization of American States", "tag": "OAS", "org": True},
    "eec": {"name": "European Economic Community", "tag": "EEC", "org": True},
    "oecd": {"name": "OEEC and OECD", "tag": "OECD", "org": True},
    "imf": {"name": "the IMF and the World Bank", "tag": "IMF", "org": True},
}
OTHER_NAMES = {"israel": "Israel", "india": "India", "pakistan": "Pakistan", "japan": "Japan", "canada": "Canada",
               "italy": "Italy", "poland": "Poland"}

# ---------------------------------------------------------------- threads (spec §4: subthreads inherit)
THREADS = {
    "africa": {"polities": ["us"], "doubtful": "Africa apart from the Congo: many states; to re-pot by state"},
    "africa-algeria-morocco": ["algeria", "morocco", "us"], "africa-rhodesia": ["uk", "rhodesia", "us"],
    "africa-wheelus": ["libya", "us"],
    "testing": ["us", "ussr", "uk"], "testing-missile-talks": ["us", "ussr"],
    "berlin-and-vienna": ["us", "ussr", "frg", "gdr", "uk", "fr"],
    "china": {"polities": ["prc", "us", "roc"], "doubtful": "the Republic of China with the PRC"},
    "congo": ["congo", "belgium", "us"], "congo-lumumba": ["congo", "us"],
    "cuba": ["cuba", "us"], "missile-crisis": ["us", "ussr", "cuba"],
    "cyprus": ["cyprus", "greece", "turkey", "uk", "us"],
    "defense-soviet-forces": ["us", "ussr"], "defense-thule": ["us", "denmark"],
    "europe-and-the-alliance": {"polities": ["us", "uk", "fr", "frg"],
                                "doubtful": "the Western Alliance, to be re-potted (the spec §4: a proposal follows)"},
    "europe-and-the-alliance-france": ["fr", "us"], "europe-and-the-alliance-jupiters": ["us", "turkey", "italy"],
    "europe-and-the-alliance-kennedy-in-europe": ["us", "frg", "ireland", "uk", "italy"],
    "europe-and-the-alliance-turkey": ["turkey", "us"],
    "european-community": ["us", "fr", "frg", "italy", "belgium", "netherlands", "luxembourg", "uk"],
    "indonesia": ["indonesia", "us"], "japan": ["japan", "us"],
    "japan-and-korea-far-east": ["japan", "rok", "roc", "philippines", "us"],
    "korea": ["rok", "us"], "japan-and-korea-pueblo": ["dprk", "us"], "japan-and-korea-blue-house": ["dprk", "rok", "us"],
    "japan-and-korea-korean-troops": ["rok", "rvn", "us"], "japan-and-korea-normalization": ["rok", "japan", "us"],
    "laos": ["laos", "us", "drv"],
    "latin-america": {"polities": ["us"], "doubtful": "the hemisphere: many states; to re-pot by state"},
    "latin-america-dominican-republic": ["dominican-republic", "us"],
    "latin-america-trip": ["us", "brazil", "argentina", "chile", "uruguay"],
    "latin-america-panama": ["panama", "us"], "latin-america-peru": ["peru", "us"],
    "middle-east": {"polities": ["us", "israel", "uar"], "doubtful": "the region: to re-pot by state"},
    "middle-east-dimona": ["israel", "us"], "middle-east-iran-arms": ["iran", "us"], "middle-east-iran-oil": ["iran", "us"],
    "middle-east-johnson-plan": {"polities": ["israel", "uar", "jordan", "syria", "lebanon", "us"],
                                 "doubtful": "the refugees' plan: the Arab hosts and Israel"},
    "middle-east-kuwait": ["kuwait", "iraq", "uk", "us"], "middle-east-johnson-trip": ["us"],
    "middle-east-samu": ["israel", "jordan", "us"],
    "middle-east-six-day-war": ["israel", "uar", "syria", "jordan", "ussr", "us"],
    "middle-east-syria": ["syria", "uar", "us"], "middle-east-yemen": ["yemen", "uar", "saudi-arabia", "uk", "us"],
    "soviet-union": ["ussr", "us"], "soviet-union-czechoslovakia": ["czechoslovakia", "ussr", "us"],
    "south-asia": ["india", "pakistan", "us"],
    "vietnam": ["us", "rvn", "drv"],
    "vietnam-saigon": ["rvn", "us"], "vietnam-elections": ["rvn", "us"], "vietnam-struggle": ["rvn", "us"],
    "vietnam-montagnards": ["rvn", "us"], "vietnam-hanoi": ["drv", "us"],
    "vietnam-rfk-front": {"polities": ["nlf", "drv", "us"], "doubtful": "the Front kept apart from the DRV"},
    "vietnam-asian-trip": ["us", "rvn", "philippines", "thailand", "malaysia", "rok", "australia", "nz"],
    "vietnam-congress": {"polities": ["us", "rvn", "drv"],
                         "doubtful": "Congress and the President on the war: the address may be the US alone"},
    "vietnam-support": {"polities": ["us", "rvn", "drv"], "doubtful": "support at home: the address may be the US alone"},
}
# every other top-level thread: the United States (the calendar is one country's: §1)

# ---------------------------------------------------------------- places (spec §4)
PLACES_HAND = {
    "state:*": ["us"], "city:*": ["us"], "province:*": ["rvn"],
    "place:dmz": {"polities": ["rvn", "drv"], "doubtful": "the zone between them, the Bến Hải its line"},
    "place:ben-hai-river": {"polities": ["rvn", "drv"], "doubtful": "the line between them"},
    "place:gulf-of-tonkin": {"polities": ["drv", "prc"], "doubtful": "the DRV's coast and China's Hainan; beyond 12 "
                                                                    "miles international waters, as the US held"},
    "place:hon-me": {"polities": ["drv"]}, "place:hon-ngu": {"polities": ["drv"]},
}
COUNTRY = {"vn-south": "rvn", "vn-north": "drv", "laos": "laos", "cambodia": "cambodia", "thailand": "thailand",
           "china": "prc"}

# ---------------------------------------------------------------- the registry's series (spec §3, §8)
# url: the address's start (host, or host and path) or a host's suffix; text: words an unlinked item names.
# dated: item (its own date), event (its own, else the event's: a record of the time), volume (FRUS), year (a card's).
S = lambda key, name, polity, kind, url=(), text=(), dated="event", **kw: dict(
    {"key": key, "name": name, "polity": polity, "kind": kind, "dated": dated}, **({"url": list(url)} if url else {}),
    **({"text": list(text)} if text else {}), **kw)
SERIES = [
    S("frus", "Foreign Relations of the United States", "us", "document series",
      ["history.state.gov/historicaldocuments/frus", "static.history.state.gov/frus"], ["FRUS ", "Foreign Relations of the United States"],
      "volume", cards=["w.foreign-relations-of-the", "w.foreign-relations-of-the-1968", "w.foreign-relations-of-the-1988",
                       "w.foreign-relations-of-the-2", "w.foreign-relations-of-the-2002", "w.foreign-relations-of-the-2003",
                       "w.foreign-relations-of-the-2006", "w.foreign-relations-of-the-2018", "w.foreign-relations-of-the-3",
                       "w.carland-foreign-relations-of-the"]),
    S("ppp", "Public Papers of the Presidents", "us", "official",
      ["www.govinfo.gov/content/pkg/PPP-", "www.govinfo.gov/app/details/PPP-", "www.presidency.ucsb.edu"],
      ["Pub. Papers", "Public Papers"]),
    S("cr", "Congressional Record", "us", "official", ["www.govinfo.gov/content/pkg/GPO-CRECB", "www.congress.gov/congressional-record"],
      ["Cong. Rec.", "Congressional Record"]),
    S("stat", "Statutes at Large", "us", "official", ["www.govinfo.gov/content/pkg/STATUTE-", "tile.loc.gov/storage-services/service/ll/llsl"], [" Stat. "]),
    S("fr", "Federal Register", "us", "official", ["www.govinfo.gov/content/pkg/FR-", "www.govinfo.gov/app/details/FR-"], ["Fed. Reg."]),
    S("hearings", "Congressional hearings, prints, documents and the Serial Set", "us", "official",
      ["www.govinfo.gov/app/details/CHRG-", "www.govinfo.gov/content/pkg/CHRG-", "www.govinfo.gov/app/details/CPRT-",
       "www.govinfo.gov/content/pkg/CPRT-", "www.govinfo.gov/app/details/SERIALSET-", "www.govinfo.gov/content/pkg/GPO-CDOC",
       "www.govinfo.gov/content/pkg/HMAN-", "www.govinfo.gov/content/pkg/GPO-CONAN", "www.govinfo.gov/content/pkg/GPO-WARRENCOMMISSIONREPORT",
       "www.govinfo.gov/content/pkg/BUDGET-", "www.govinfo.gov/content/pkg/USCODE-", "www.govinfo.gov/content/pkg/GOVPUB-",
       "www.govinfo.gov", "clerk.house.gov", "www.senate.gov", "www.congress.gov"], dated="item"),
    S("dsb", "Department of State Bulletin", "us", "official", ["archive.org/details/departmentofstat"],
      ["*Bulletin*", "Department of State Bulletin", "Dep't St. Bull."], cards=["w.department-of-state-bulletin"]),
    S("cases", "the courts' reports", "us", "official",
      ["tile.loc.gov/storage-services/service/ll/usrep", "static.case.law", "law.resource.org", "caselaw.findlaw.com",
       "scocal.stanford.edu", "www.supremecourt.gov", "clearinghouse.net", "supreme.justia.com"], [" U.S. ", " F.2d ", " F. Supp. "]),
    S("treaties", "the treaties", "us", "official", ["tile.loc.gov/storage-services/service/ll/lltreaties",
                                                      "tile.loc.gov/storage-services/service/ll/llmlp"], [" U.S.T. "]),
    S("voteview", "the roll calls (Voteview, from the Record and the Journals)", "us", "official", ["voteview.com"]),
    S("church", "the Senate's intelligence inquiries (the Church committee, 1975-76)", "us", "official",
      ["www.intelligence.senate.gov"], ["Church Committee", "Church committee", "Senate Select Committee"], dated="item"),
    S("reports", "the congressional reports and documents, as printed", "us", "official", ["article5library.org"],
      ["S. Rep.", "H. Rep.", "H.R. Rep.", "S. Doc.", "H. Doc.", "S. Exec. Doc."], dated="item"),
    S("pentagon-papers", "the Pentagon Papers (the Times, the Gravel edition, the House committee's print)", "us",
      "document series", [], ["Pentagon Papers", "United States–Vietnam Relations", "U.S.–Vietnam Relations"], dated="year"),
    S("periodicals-us", "American periodicals, digitized", "us", "press",
      ["archive.org/details/per_", "archive.org/details/sim_oil"],
      ["Problems of Communism", "Oil and Gas Journal"], dated="item"),
    S("us-gov-archive", "American official publications on archive.org", "us", "official",
      ["archive.org/details/pub_usgov", "archive.org/details/ViolenceInCi", "archive.org/details/statementofv",
       "archive.org/details/primaryoffic", "archive.org/details/northcarolin", "archive.org/details/annualreport"], dated="event"),
    S("us-reports", "the Executive's reports, studies and opinions, as printed", "us", "official",
      ["www.justice.gov", "www.osti.gov", "ntrs.nasa.gov", "www.nasa.gov", "pubs.usgs.gov", "www.ojp.gov", "www.everycrsreport.com",
       "usccr.gov", "www.ssa.gov", "www.federalreserve.gov", "fraser.stlouisfed.org", "www2.census.gov", "www.census.gov",
       "nmb.gov", "archive.org/details/DTIC", "archive.org/details/reportofnation", "archive.org/details/shootoutinclevel"],
      dated="item"),
    S("states", "the States' and cities' official publications (registers, returns, journals, session laws, manuals)", "us",
      "official", ["archive.org/details/alabama", "archive.org/details/californiastate", "archive.org/details/castatem",
                   "archive.org/details/stateofcaliforn", "archive.org/details/electionstatisti", "archive.org/details/officialvote",
                   "archive.org/details/register", "archive.org/details/manualforgeneral", "archive.org/details/jhouse",
                   "archive.org/details/jsen", "archive.org/details/op-atty-gen", "archive.org/details/Tabulationofofficialvote",
                   "archive.org/details/northcarolinaman", "archive.org/details/federalstatecons", "oklahoma.gov",
                   "msa.maryland.gov", "www.msa.maryland.gov", "lrl.texas.gov", "govdocs.nebraska.gov", "www.wvlegislature.gov",
                   "code.wvlegislature.gov", "www.lrl.mn.gov", "www.leg.mn.gov", "www.revisor.mn.gov", "records.sos.state.or.us",
                   "publications.iowa.gov", "www.nj.gov", "nj.gov", "www.leg.state.nv.us", "clerk.assembly.ca.gov",
                   "elections.ri.gov", "spl.cde.state.co.us", "www.sec.state.vt.us", "www.elections.alaska.gov",
                   "www.elections.il.gov", "vote.utah.gov", "nebraskalegislature.gov", "legislature.idaho.gov",
                   "leg.wa.gov", "app.leg.wa.gov", "www.stlouis-mo.gov", "www.sos.mo.gov", "www.seattle.gov",
                   "www.sandiego.gov", "tlc.texas.gov", "perb.ny.gov", "legis.delaware.gov", "elections.delaware.gov",
                   "apps.legislature.ky.gov", "elect.ky.gov", "www.sos.ok.gov", "www.pa.gov", "www.legislature.mi.gov",
                   "www.legis.state.pa.us", "www.houstontx.gov", "secure.in.gov", "edocs.dlis.state.fl.us",
                   "docs.legis.wisconsin.gov", "va2.elstats2.civera.com", "historical.elections.virginia.gov",
                   "newyork.concon.info", "www.paconstitution.org", "dspace.njstatelib.org", "dc.statelibrary.sc.gov",
                   "archives.lib.state.ma.us", "digital.library.in.gov", "www.sos.nd.gov", "sdsos.gov", "www.sos.wa.gov",
                   "sos.iowa.gov", "www.sos.arkansas.gov", "mn.electionarchives.lib.umn.edu", "digitalmaine.com",
                   "archive.org/details/sim_republican-national-convention", "archive.org/details/sim_democratic"],
      dated="event"),
    S("un", "the United Nations' records", "parties", "official",
      ["undocs.org", "documents.un.org", "docs.un.org", "digitallibrary.un.org", "treaties.un.org", "www.icj-cij.org"],
      ["U.N. Doc", "UN Doc"], dated="item", note="an organization's record: its state parties' (vis.py, STYLE 4)"),
    S("eec", "the European Communities' records", "parties", "official", ["eur-lex.europa.eu"], dated="item"),
    S("hansard", "Hansard (Parliamentary Debates)", "uk", "official", ["api.parliament.uk/historic-hansard", "hansard.parliament.uk"],
      ["Hansard", "Parl. Deb."]),
    S("jo", "Journal officiel de la République française", "fr", "official", [], ["Journal officiel"]),
    S("bt", "Verhandlungen des Deutschen Bundestages (Plenarprotokolle)", "frg", "official", ["dserver.bundestag.de"],
      ["Plenarprotokoll", "Bundestag, Plenar"]),
    S("aapd", "Akten zur Auswärtigen Politik der Bundesrepublik Deutschland", "frg", "document series", [],
      ["AAPD", "Akten zur Auswärtigen Politik"], dated="year"),
    S("ddf", "Documents diplomatiques français", "fr", "document series", [], ["DDF", "Documents diplomatiques"], dated="year"),
    S("vatican", "the Holy See's acts", "vatican", "official", ["www.vatican.va"], dated="item"),
    # the press: public from its date (§3)
    S("nyt", "New York Times", "us", "press", ["timesmachine.nytimes.com", "www.nytimes.com", "select.nytimes.com"],
      ["New York Times"]),
    S("wapo", "Washington Post", "us", "press", ["www.washingtonpost.com"], ["Washington Post"]),
    S("wsj", "Wall Street Journal", "us", "press", [], ["Wall Street Journal"]),
    S("chitrib", "Chicago Tribune", "us", "press", [], ["Chicago Tribune"]),
    S("lat", "Los Angeles Times", "us", "press", [], ["Los Angeles Times"]),
    S("baltsun", "Baltimore Sun", "us", "press", [], ["Baltimore Sun"]),
    S("star", "Evening Star (Washington)", "us", "press", [], ["Evening Star", "Washington Star"]),
    S("herald", "New York Herald Tribune", "us", "press", [], ["Herald Tribune"]),
    S("weeklies", "the American weeklies and monthlies", "us", "press", ["www.time.com", "content.time.com"],
      ["Newsweek", "*Time*", "U.S. News", "*Life*", "*Look*", "Saturday Evening Post", "New Republic", "*Nation*",
       "National Review", "*Harper's", "*Atlantic", "New Yorker", "Reader's Digest", "*Commentary*", "Ripon Forum"]),
    S("cq", "Congressional Quarterly (Weekly Report, Almanac)", "us", "press", [], ["Congressional Quarterly", "CQ Weekly", "CQ Almanac"],
      cards=["w.cq-weekly-report", "w.cq-almanac", "w.congressional-quarterly-almanac", "w.congress-and-the-nation"]),
    S("polls", "the polls' releases (Gallup, Harris)", "us", "press", ["news.gallup.com"], ["Gallup", "Harris Survey", "Louis Harris"],
      cards=["w.gallup-poll"]),
    S("columns", "the American columns and wires", "us", "press", [],
      ["Pearson's column", "Drew Pearson", "Washington Merry-Go-Round", "Evans and Novak", "Evans & Novak", "Alsop",
       "Lippmann", "Associated Press", "United Press", "UPI", "Meet the Press", "Face the Nation", "CBS News", "NBC News", "ABC News"]),
    S("us-papers", "American newspapers, other, and their digitized files", "us", "press",
      ["www.newspapers.com", "newspapers.digitalnc.org", "oregonnews.uoregon.edu", "cdnc.ucr.edu", "newspaper.library.tamu.edu",
       "texashistory.unt.edu", "issues.texasobserver.org", "www.texasobserver.org", "www.thecrimson.com", "www.villagevoice.com",
       "riponsociety.org", "www.livingroomcandidate.org"],
      ["Boston Globe", "Christian Science Monitor", "Post-Dispatch", "Milwaukee", "Atlanta Constitution", "Atlanta Journal",
       "Philadelphia Inquirer", "Detroit Free Press", "Des Moines Register", "Miami Herald", "Houston Post", "Dallas Morning News",
       "Jackson Daily News", "Clarion-Ledger", "Birmingham News", "Montgomery Advertiser", "Denver Post", "Newsday",
       "Daily News", "New York Post", "Texas Observer", "Village Voice"]),
    S("modern-press", "the press since (dated by the item, not the event)", "us", "press",
      ["selmatimesjournal.com", "lasvegassun.com", "annarborchronicle.com", "www.chalkbeat.org", "chalkbeat.org", "vtdigger.org",
       "www.alreporter.com", "www.npr.org", "wnyc.org", "whyy.org", "www.cpr.org", "www.stlpr.org",
       "americanradioworks.publicradio.org"], dated="item"),
    S("soviet-press", "the Soviet press and TASS", "ussr", "press", [], ["Pravda", "Izvestia", "TASS", "Tass", "Krasnaya Zvezda", "Kommunist"]),
    S("prc-press", "the Chinese press and Xinhua", "prc", "press", [], ["Renmin Ribao", "People's Daily", "Xinhua", "New China News Agency", "Hongqi"]),
    S("drv-press", "the DRV's press and radio", "drv", "press", [], ["Nhân Dân", "Học Tập", "Quân Đội Nhân Dân", "Radio Hanoi",
                                                                    "Vietnam News Agency"]),
    S("nlf-press", "the Front's radio and press agency", "nlf", "press", [], ["Liberation Radio", "Liberation Press Agency"]),
    S("rvn-press", "the Saigon press", "rvn", "press", [], ["Saigon Post", "Saigon Daily News", "Vietnam Press"]),
    S("uk-press", "the British press, the BBC and Reuters", "uk", "press", [],
      ["Manchester Guardian", "*Guardian*", "Daily Telegraph", "*Observer*", "*Economist*", "BBC", "Reuters", "Times (London)"]),
    S("fr-press", "the French press and AFP", "fr", "press", [], ["Le Monde", "Le Figaro", "L'Express", "Agence France-Presse", "AFP"]),
    S("frg-press", "the West German press", "frg", "press", [], ["Frankfurter Allgemeine", "Der Spiegel", "Die Zeit", "Die Welt"]),
    S("gdr-press", "the East German press", "gdr", "press", [], ["Neues Deutschland"]),
    S("cuba-press", "the Cuban press", "cuba", "press", [], ["Revolución", "Granma"]),
    # archives: unpublished, public only where a copy or "Made public:" says when
    S("recordings", "the White House recordings (Miller Center, PRDE)", "us", "archive",
      ["millercenter.org", "prde.upress.virginia.edu"], dated="item"),
    S("us-archives", "American archives and libraries' files", "us", "archive",
      ["www.jfklibrary.org", "www.lbjlibrary.org", "discoverlbj.org", "catalog.archives.gov", "www.archives.gov", "www.reaganlibrary.gov",
       "www.cia.gov", "nsarchive.gwu.edu", "nsarchive2.gwu.edu", "aarclibrary.org", "profiles.nlm.nih.gov", "archives.hud.gov",
       "da.mdah.ms.gov", "crmvet.org", "www.crmvet.org", "snccdigital.org", "www.fsm-a.org", "ldfrecollection.org", "naacpldf.org",
       "ivanallen.iac.gatech.edu", "radar.auctr.edu", "findingaids.library.nyu.edu", "archives.nd.edu", "archives.law.virginia.edu",
       "omekas-congress.lib.wvu.edu", "mpl.org", "kinginstitute.stanford.edu", "okra.stanford.edu", "digital.archives.alabama.gov",
       "mdh.contentdm.oclc.org", "kgi.contentdm.oclc.org", "indianamemory.contentdm.oclc.org", "dlg.galileo.usg.edu", "dlg.usg.edu",
       "crdl.usg.edu", "digital.lib.ku.edu", "collections.lib.uwm.edu", "emke.uwm.edu", "uwm.edu", "asset.library.wisc.edu",
       "search.library.wisc.edu", "exploreuk.uky.edu", "library.unt.edu", "mocat.library.unt.edu", "azmemory.azlibrary.gov",
       "repository.uclawsf.edu", "our.oakland.edu", "www.studsterkel.org", "library.law.smu.edu", "law2.umkc.edu",
       "www.mnhs.org", "www2.mnhs.org"], dated="item"),
    S("foreign-archives", "documents of other governments, as translated (the Wilson Center)", "?", "archive",
      ["www.wilsoncenter.org", "digitalarchive.wilsoncenter.org"], dated="item"),
    # reference works: they date nothing and make nothing public (vis.py, KINDS)
    S("reference", "encyclopedias, handbooks, finding aids and the like", None, "reference",
      ["en.wikipedia.org", "en.wikisource.org", "www.tshaonline.org", "encyclopediaofalabama.org", "www.georgiaencyclopedia.org",
       "www.mnopedia.org", "www.historylink.org", "philadelphiaencyclopedia.org", "encyclopediaofarkansas.net", "blackpast.org",
       "explorepahistory.com", "www.foundsf.org", "www.nobelprize.org", "www.nga.org", "governors.rutgers.edu", "www.fjc.gov",
       "mshistory.mdah.ms.gov", "www.wisconsinhistory.org", "wisconsinhistory.org", "guides.jenkinslaw.org", "www.marxists.org",
       "kcparks.org", "pendergastkc.org", "www.archpark.org", "www.dc1968project.com", "ghhsociety.org",
       "historicsites.dcpreservation.org", "ualrexhibits.org", "allthewaywithlbj.com", "sog.unc.edu", "case.hks.harvard.edu",
       "case.edu", "www.k-state.edu", "www.loc.gov", "history.state.gov/departmenthistory", "history.state.gov/milestones", "web.archive.org", "babel.hathitrust.org", "catalog.hathitrust.org",
       "books.google.com", "www.jstor.org", "doi.org", "hdl.handle.net", "www.nber.org", "www.cpr.org/"]),
]

PUBLISHERS = {  # sure of (STYLE 2): the cards hold no publisher yet; a card's `publisher` row takes its country here
    "us": ["W. W. Norton", "Norton", "Doubleday", "Simon & Schuster", "Random House", "Alfred A. Knopf", "Knopf",
           "Harper & Row", "Harper", "HarperCollins", "Little, Brown", "Houghton Mifflin", "Viking", "Penguin Press",
           "Farrar, Straus", "Scribner", "Charles Scribner's Sons", "Macmillan (New York)", "McGraw-Hill", "Atheneum",
           "Basic Books", "Free Press", "Holt, Rinehart and Winston", "Henry Holt", "Crown", "Putnam", "G. P. Putnam's Sons",
           "Morrow", "William Morrow", "Pantheon", "Vintage", "St. Martin's Press", "Praeger", "Brookings Institution",
           "Government Printing Office", "U.S. Government Printing Office", "University of North Carolina Press",
           "University of California Press", "University of Chicago Press", "Harvard University Press", "Yale University Press",
           "Princeton University Press", "Columbia University Press", "Cornell University Press", "Johns Hopkins University Press",
           "University Press of Kansas", "University of Texas Press", "Louisiana State University Press", "University of Georgia Press",
           "University Press of Mississippi", "University of Illinois Press", "University of Michigan Press", "Stanford University Press",
           "MIT Press", "Indiana University Press", "University of Wisconsin Press", "University of Pennsylvania Press",
           "University of Virginia Press", "University Press of Virginia", "Kent State University Press", "Rutgers University Press",
           "Temple University Press", "New York University Press", "Ohio State University Press", "University of Missouri Press",
           "University of Kentucky Press", "University Press of Kentucky", "University of Massachusetts Press",
           "Naval Institute Press", "Center of Military History", "Office of Air Force History", "Air Force History and Museums Program",
           "Naval Historical Center", "Joint History Office", "Historical Division, Joint Secretariat", "Office of the Secretary of Defense Historical Office"],
    "uk": ["Oxford University Press (Oxford)", "Cambridge University Press (Cambridge)", "Macmillan (London)", "Faber and Faber",
           "Weidenfeld & Nicolson", "Hutchinson", "Jonathan Cape", "Allen Lane", "Routledge", "Frank Cass", "I. B. Tauris"],
    "fr": ["Gallimard", "Plon", "Fayard", "Seuil", "Éditions du Seuil", "Julliard", "Flammarion", "Robert Laffont"],
    "frg": ["Deutsche Verlags-Anstalt", "Ullstein", "Oldenbourg", "Propyläen"],
    "ussr": ["Politizdat", "Izdatel'stvo politicheskoi literatury", "Voenizdat", "Progress Publishers"],
    "drv": ["Nhà xuất bản Sự thật (to 1976)", "Foreign Languages Publishing House (Hanoi, to 1976)"],
}

# journals sure of (STYLE 2): the journal's home, its society's or institution's country
JOURNALS = {"Diplomatic Hist.": "us", "Int'l Sec.": "us", "J. Cold War Stud.": "us", "Pac. Hist. Rev.": "us",
            "Yale L.J.": "us", "Pol. Sci. Q.": "us", "Mich. L. Rev.": "us", "J. Legal Stud.": "us", "World Pol.": "us",
            "J. Am. Hist.": "us", "Pub. Health Rep.": "us", "Middle E.J.": "us", "Hist. Educ. Q.": "us",
            "J. Ill. Hist.": "us", "Notre Dame Law.": "us", "Mich. Hist. Rev.": "us", "Mil. Rev.": "us",
            "Wm. & Mary L. Rev.": "us", "Am. Pol. Sci. Rev.": "us", "Pa. Hist.": "us", "Neb. Hist.": "us",
            "Vt. Hist.": "us", "J. Interdisc. Hist.": "us", "Foreign Pol'y": "us", "J. Pol.": "us",
            "St. John's L. Rev.": "us", "Foreign Aff.": "us", "Harv. L. Rev.": "us", "Colum. L. Rev.": "us",
            "Stud. Intel.": "us", "J. Vietnamese Stud.": "us", "Buddhist-Christian Stud.": "us", "New South": "us",
            "Mod. Asian Stud.": "uk", "China Q.": "uk", "Cold War Hist.": "uk"}
NETWORKS = re.compile(r"\b(ABC|CBS|NBC|PBS|HBO|Netflix|Discovery|WGBH|NET|Showtime|Turner|CNN|HBO Films|American Experience)\b")
US_GOV = re.compile(r"\b(?:Joint Chiefs of Staff|United States Army in|U\.S\. Army|U\.S\. Air Force|United States Air Force|"
                    r"U\.S\. Navy|United States Navy|Marine Corps|Department of (?:State|Defense|the Army)|Command History|"
                    r"Office of Air Force History|Center of Military History|Historical Office|Senate|House of Representatives|"
                    r"Committee on|Subcommittee|Congressional Research Service|Central Intelligence Agency|CIA\b|"
                    r"National Commission|President's Commission|Warren Commission|Commission on Civil Rights|"
                    r"Kerner|Pentagon Papers|United States[–-]Vietnam Relations|Public Papers of the Presidents|MACV\b|"
                    r"Bureau of the Census|Statistical Abstract|Economic Report of the President)")
DOC_SERIES = re.compile(r"Foreign Relations of the United States|Pentagon Papers|United States[–-]Vietnam Relations|"
                        r"Command History|Documentary History|Documents on|The Presidential Recordings|Presidential Recordings|"
                        r"Papers of Martin Luther King|Papers of Robert F\. Kennedy|Selected Papers|Collected Works|"
                        r"Tapes\b|Secret White House|Transcripts")
MEMOIR_T = re.compile(r"\bMemoirs?\b|\bHồi ký\b|\bHổi ký\b|\bRecollections\b|\bReminiscences\b|\bAutobiography\b|"
                      r"\bMy Life\b|\bAs I Saw It\b|\bIn Retrospect\b|\bVantage Point\b|\bA Soldier Reports\b|\bCounsel to the President\b")
DIARY_T = re.compile(r"\bDiary\b|\bDiaries\b|\bJournals\b|\bJournal\b(?! of)|\bNhật ký\b")
ORAL_T = re.compile(r"\bOral History\b|\bOral Histories\b|\bin the Words of\b|\bInterviews?\b")
LATER_ED = re.compile(r"\b(?:\d+[a-z]{1,2} ed\.|rev\. ed\.|trans\.|reprint|repr\.|new ed\.|ed\. \d{4}|abridged)")
PLACE_PUB = [(re.compile(r"\b(?:Hà Nội|Hanoi):|\(Hà Nội|\(Hanoi|Nxb\b|Nhà xuất bản"), "drv-or-srv"),
             (re.compile(r"\b(?:Sài Gòn|Saigon):|\(Sài Gòn|\(Saigon"), "rvn"),
             (re.compile(r"\b(?:Moscow|Москва|Moskva):|\(Moscow"), "ussr"),
             (re.compile(r"\bParis:|\(Paris"), "fr"),
             (re.compile(r"\bLondon:|\(London"), "uk")]


# ---------------------------------------------------------------- YAML: one flow row a key, straight quotes

def q(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(q(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{" + ", ".join(f"{k}: {q(x)}" for k, x in v.items()) + "}"
    s = str(v)
    if re.match(r"^[a-z][a-z0-9.-]*$", s) and s not in ("null", "true", "false", "yes", "no", "on", "off"):
        return s
    return "'" + s.replace("'", "''") + "'"


def write(path, header, blocks, dry):
    lines = ["# " + h for h in header]
    for name, val, note in blocks:
        lines.append("")
        for n in note:
            lines.append("# " + n)
        if isinstance(val, list):
            lines.append(f"{name}:")
            for x in val:
                lines.append(f"  - {q(x)}")
        else:
            lines.append(f"{name}:")
            for k, x in val.items():
                lines.append(f"  {q(k)}: {q(x)}")
    text = "\n".join(lines) + "\n"
    if dry:
        print(f"(dry run) {os.path.relpath(path, ROOT)}: {len(text):,} bytes")
        return
    tmp = path + ".tmp"
    open(tmp, "w", encoding="utf-8").write(text)
    os.replace(tmp, path)
    print(f"{os.path.relpath(path, ROOT)}: {len(text):,} bytes")


def merged(old, new, refresh):
    """old rows kept (a hand edit wins), new keys added; --refresh: the seed's rows over the old, a `hand: true` row kept."""
    hand = lambda v: isinstance(v, dict) and v.get("hand")
    out = {k: v for k, v in (old or {}).items() if not refresh or hand(v)}
    for k, v in new.items():
        if k not in out:
            out[k] = v
    return out


# ---------------------------------------------------------------- persons

FOREIGN_SECTIONS = {("kja", "III.J"): None, ("adm", "III.J"): None, ("vn", "III.G"): "rvn", ("vn", "III.H"): "drv",
                    ("vn", "III.I"): None}


def part3(series):
    """{name key: [(list, section code, role, section titles)]} for every person of Part III."""
    from tools.bib import lives
    out = collections.defaultdict(list)
    for lst in series.lists.values():
        for sec, e in lst.entries():
            if (sec.code or "").startswith("III") and e.get("s") and "group" not in (e.get("tags") or []):
                for n in re.split(r";\s*", e["s"]):
                    n = re.sub(r"\s*\(.*?\)\s*$", "", n).strip()
                    if n:
                        code = sec.code if sec.code.count(".") <= 1 else ".".join(sec.code.split(".")[:2])
                        out[lives.key_of(n)].append((lst.key, code, e.get("r") or "", sec.title))
    return out


def frus_roles(key):
    """[(volume id, role)] from FRUS's lists of persons (sources/frus-names/<Letter>.json)."""
    from tools.bib import lives
    js = lives.letter_json("frus-names", key[:1].upper())
    v = js.get(key) or {}
    return [(vol, d.get("role") or "") for vol, d in v.items() if isinstance(d, dict)]


def vol_years(vol):
    m = re.match(r"frus(\d{4})(?:-(\d{2}))?", vol)
    if not m:
        return None
    a = int(m.group(1))
    b = int(m.group(1)[:2] + m.group(2)) if m.group(2) else a
    return a, b


def person_row(key, p3, ranks, frus):
    """(row, basis) for one person (STYLE 1)."""
    foreign = [(l, c, r, t) for l, c, r, t in p3 if (l, c) in FOREIGN_SECTIONS]
    if foreign:
        l, c, r, t = foreign[0]
        p = vis_words.role_polity(r, None)
        if p in (None, "us"):
            p = FOREIGN_SECTIONS[(l, c)] or (vis_words.nation(t) if vis_words.nation(t) not in (None, "rvn") else None)
        if p == "rvn" and (l, c) == ("vn", "III.H"):
            p = "drv"
        if (l, c) == ("vn", "III.H") and re.search(r"Front|NLF|PRG|Provisional Revolutionary|Liberation", r):
            p = "nlf"
        if p is None:
            fr = [vis_words.role_polity(x, None) for _, x in frus]
            fr = [x for x in fr if x and x != "us"]
            p = collections.Counter(fr).most_common(1)[0][0] if fr else "?"
        return {"polity": p, "basis": f"{l} {c}: {r[:70]}" if r else f"{l} {c}"}
    if p3:
        for l, c, r, t in p3:
            p = vis_words.role_polity(r, "us", strict=True)
            if p and p != "us":
                return {"polity": p, "basis": f"{l} {c}: {r[:70]}", "doubtful": "a foreign role in an American section"}
        l, c, r, t = p3[0]
        return {"polity": "us", "basis": f"{l} {c}"}
    if any(rk in (1, 2) for _, rk in ranks):
        return {"polity": "us", "basis": "roster" if any(rk == 1 for _, rk in ranks) else "congress"}
    if frus:
        by = []
        for vol, r in frus:
            p = vis_words.role_polity(r, None)
            if p:
                by.append((vol_years(vol) or (0, 0), p, vol, r))
        if not by:
            return {"polity": "?", "basis": "frus: no role"}
        ps = collections.Counter(p for _, p, _, _ in by)
        if len(ps) == 1 or ps.most_common(1)[0][1] >= 0.75 * len(by):
            p = ps.most_common(1)[0][0]
            (_, _, vol, r) = next(x for x in by if x[1] == p)
            return {"polity": p, "basis": f"frus {vol}: {r[:60]}"}
        # a change between volumes (STYLE 1): the ranges by the volumes' years, marked doubtful
        by.sort()
        top = ps.most_common(1)[0][0]
        firsts = {}
        for (a, b), p, vol, r in by:
            firsts.setdefault(p, (a, b, vol, r))
        return {"polity": top, "basis": f"frus: {', '.join(f'{p} {v[2]}' for p, v in firsts.items())}",
                "doubtful": "the volumes' descriptions differ: dated ranges wanted"}
    return {"polity": "?", "basis": "no role found"}


# ---------------------------------------------------------------- FRUS: volume years, documents' parties

ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman(r):
    n = 0
    for a, b in zip(r, r[1:] + " "):
        n += -ROMAN[a] if ROMAN.get(b, 0) > ROMAN[a] else ROMAN[a]
    return n


def harvest_volumes():
    """{volume id: year} by the notes' and cards' own words (STYLE 3), and {volume: {year: count}} where they differ."""
    seen = collections.defaultdict(collections.Counter)
    rx = re.compile(r"FRUS (\d{4})[–-](\d{2}), ([IVXL]+)(?:, (?:pt\. )?\d)? \(((?:19|20)\d\d)\)")
    rx_card = re.compile(r"Foreign Relations of the United States, (\d{4})[–-](\d{4})\*?, vol\. (\d+)[^()]*\(((?:19|20)\d\d)\)")
    rx_card2 = re.compile(r"Foreign Relations of the United States, (\d{4})[–-](\d{4}), Vol\. (\d+):.*")
    files = glob.glob(os.path.join(ROOT, "lists", "**", "*.yaml"), recursive=True) + \
        glob.glob(os.path.join(ROOT, "works", "*.yaml")) + glob.glob(os.path.join(ROOT, "sources", "witnesses", "*.yaml"))
    for p in files:
        t = open(p, encoding="utf-8").read()
        for m in rx.finditer(t):
            seen[f"frus{m.group(1)}-{m.group(2)}v{roman(m.group(3)):02d}"][m.group(4)] += 1
        for m in rx_card.finditer(t):
            seen[f"frus{m.group(1)}-{m.group(2)[2:]}v{int(m.group(3)):02d}"][m.group(4)] += 1
    # a card whose title is one volume and whose year is its own ("Vol. 42: ...", year 2018)
    from tools.bib import works
    cat = works.Catalogue()
    for cid, c in cat.cards.items():
        m = rx_card2.match(str(c.get("title") or ""))
        if m and re.match(r"\d{4}$", str(c.get("year") or "")):
            seen[f"frus{m.group(1)}-{m.group(2)[2:]}v{int(m.group(3)):02d}"][str(c["year"])] += 1
    vols, doubts = {}, {}
    for v, cnt in sorted(seen.items()):
        vols[v] = cnt.most_common(1)[0][0]
        if len(cnt) > 1:
            doubts[v] = dict(cnt)
    return vols, doubts


def frus_links(series):
    """Every FRUS document the calendar's notes link or its witnesses copy: {volume/dN}."""
    out = set()
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for _, e in lst.entries():
            for m in re.finditer(r"historicaldocuments/(frus[\w-]+/d\d+)", str(e.get("n") or "") + str(e.get("src") or "")):
                out.add(m.group(1))
    return out


def parties(docs, names_pol, surnames):
    """{volume/dN: [polities]} for the documents whose heading names a party other than the US: the title's sender and
    recipients ("Letter From Chairman Khrushchev to President Kennedy"), a memorandum of conversation's participants
    (its first lines in sources/frus-text/). The US is a party to every one (they are its government's records)."""
    from tools.bib import daybook
    by_key = {x["key"][5:]: x for x in daybook.load()[0] if x.get("src") == "frus"}
    months = collections.defaultdict(list)
    for k in docs:
        x = by_key.get(k)
        if x:
            months[x["date"][:7]].append(k)
    out = {}

    def side_polities(text):
        ps = set()
        for part in [text]:
            p = vis_words.role_polity(part, None)
            if p and p != "us":
                ps.add(p)
            for w in re.findall(r"\b([A-ZÀ-Ỹ][\w'-]{2,})\b", vis_words.US_POSTS.sub(" ", part)):
                sp = surnames.get(store.fold(w).lower())
                if sp:
                    ps.add(sp)
        return ps

    for mo, keys in sorted(months.items()):
        path = os.path.join(ROOT, "sources", "frus-text", f"{mo}.json.xz")
        texts = json.load(lzma.open(path))["docs"] if os.path.exists(path) else {}
        for k in keys:
            x = by_key[k]
            title = x.get("title") or ""
            ps = set()
            head = vis_words.US_POSTS.sub(" # ", title)        # the American posts first: "Ambassador to Vietnam"
            head = re.sub(r",? in (?:the )?[A-Z][\w'.-]+(?: [A-Z][\w'.-]+)?(?=\s*$| to |,)", " ", head)   # a traveller
            m = re.search(r"\bFrom (.+?) to (.+)$", head)
            if m:
                ps |= side_polities(m.group(1)) | side_polities(m.group(2))
            body = texts.get("frus:" + k) or ""
            pm = re.search(r"(?i)participants?\s*:?\s*</?\w[^>]*>?(.{0,1500})", body)
            if pm and re.search(r"(?i)memorandum of conversation|conversation|meeting|summary record|minutes", title):
                lines = []                    # the list's short lines, to the first that reads as the text
                for ch in re.split(r"<[^>]+>|;", pm.group(1)):
                    ch = ch.strip()
                    if not ch:
                        continue
                    if len(ch) > 100 or re.match(r"(?i)subject|date|place|time\b", ch) or re.search(
                            r"\b(?:said|called|expressed|thought|noted|discussed|began|opened|asked|was|were|had|is)\b", ch):
                        break
                    lines.append(ch)
                for line in lines:
                    ps |= side_polities(line)
            ps = {p for p in ps if not POLITIES.get(p, {}).get("org")}
            if ps:
                out[k] = ["us"] + sorted(ps)
    return out


# ---------------------------------------------------------------- works

def cited_cards(series):
    out = collections.Counter()
    for lst in series.lists.values():
        if lst.kind != "calendar":
            continue
        for _, e in lst.entries():
            for m in re.finditer(r"\[\[(w\.[^\]|]+)", str(e.get("n") or "") + " " + str(e.get("c") or "")):
                out[series.works.alias.get(m.group(1), m.group(1))] += 1
            for r in ((e.get("src") or {}).get("rows") or []):
                m = re.match(r"^(?:via )?(w\.\S+)", str(r))
                if m:
                    out[series.works.alias.get(m.group(1), m.group(1))] += 1
    return out


def work_row(series, cid, everyone_idx):
    from tools.bib import works, lives
    from tools.bib.refs import Refs
    cat = series.works
    f = cat.fields(cid) or {}
    card = cat.get(cid) or {}
    text = " ".join(str(x) for x in (card.get("c"), f.get("title"), " ".join(f.get("author") or []), f.get("paren"),
                                     " ".join(f.get("editor") or []), f.get("journal"), card.get("n")) if x)
    title = str(f.get("title") or card.get("c") or "")
    basis = []
    kind = None
    agent = None
    # the listings: a memoir is listed under its author as subject; the tapes and the documents sections
    for lst, sec, e in works.where(series).get(cid, []):
        titles = " ".join(s.title for s in _chain(sec))
        if Refs.is_people_section(sec) and not (sec.code or "").startswith("III") and e.get("s"):
            subj = Refs.name_keys(e["s"])
            authors = [store.fold(works.surname(a)) for a in (f.get("author") or [])]
            if subj and authors and subj[0][0].split()[0] in authors:
                kind = kind or "memoir"
                agent = agent or lives.key_of(re.split(r";\s*", e["s"])[0])
                basis.append(f"listed under its author, {lst.key} {sec.code}")
        if re.search(r"\bThe tapes\b|Records and transcripts|Transcripts", titles) and not kind:
            kind, _ = "document series", basis.append(f"{lst.key} {sec.code}")
        if re.search(r"^Cases$", sec.title) and not kind:
            kind, _ = "official", basis.append(f"{lst.key} {sec.code}")
    if not kind:
        if DOC_SERIES.search(title):
            kind = "document series"
        elif DIARY_T.search(title):
            kind = "diary"
        elif ORAL_T.search(title):
            kind = "oral history"
        elif MEMOIR_T.search(title):
            kind = "memoir"
        elif f.get("kind") == "periodical":
            kind = "press"
        if kind:
            basis.append("its title")
    if kind in ("memoir", "diary", "oral history") and not agent and f.get("author"):
        a = f["author"][0]
        k = everyone_idx.get((store.fold(works.surname(a)).lower(), store.fold(a.split()[0]).lower()[:1]))
        if k:
            agent = k
    kind = kind or "scholarship"
    # the year: the card's, unless it is a later edition
    y = str(f.get("year") or "")
    ym = re.match(r"\d{4}", y)
    year = ym.group(0) if ym else "?"
    if LATER_ED.search(str(f.get("paren") or "")) or LATER_ED.search(str(card.get("c") or "")):
        later = year
        year = "?"
        basis.append(f"the card is a later edition ({later})")
    # the country: what the card itself shows (STYLE 2)
    country = "?"
    if US_GOV.search(text):
        country = "us"
        basis.append("an American government author or title")
    elif f.get("kind") == "film" and NETWORKS.search(str(f.get("paren") or "") + " " + str(card.get("c") or "")):
        country = "us"
        basis.append("an American network")
    elif f.get("journal") and JOURNALS.get(f["journal"]):
        country = JOURNALS[f["journal"]]
        basis.append(f"the journal, {f['journal']}")
    else:
        for rx, p in PLACE_PUB:
            if rx.search(str(card.get("c") or "")):
                if p == "drv-or-srv":
                    p = "drv" if year != "?" and int(year) < 1976 else ("srv" if year != "?" else "?")
                country = p
                basis.append("its place of publication")
                break
    if f.get("journal") and kind == "scholarship":
        pass
    row = {"kind": kind, "country": country, "year": year}
    if agent:
        row["agent"] = agent
    if basis:
        row["basis"] = "; ".join(basis)[:120]
    return row


def _chain(sec):
    s, out = sec, []
    while s is not None:
        out.append(s)
        s = s.parent
    return out


# ---------------------------------------------------------------- main

def main(dry, refresh):
    from tools.bib import lives
    series = store.Series()
    old_pol = (store.load_yaml(POL) if os.path.exists(POL) else None) or {}
    old_prov = (store.load_yaml(PROV) if os.path.exists(PROV) else None) or {}

    # persons
    everyone = lives.everyone(series)
    by_key = {lives.key_of(p["name"]): p for p in everyone}
    for p in everyone:                           # a tag may name a person by another of his forms ('colby-william')
        for n in p["names"]:
            by_key.setdefault(lives.key_of(n), p)
    for fk, sk in lives._CACHE.get("frus-alias", {}).items():   # a FRUS list's key for a person the series holds
        if sk in by_key:
            by_key.setdefault(fk, by_key[sk])
    everyone_idx = {}
    for p in everyone:
        k = lives.key_of(p["name"])
        ki = (store.fold(p["sur"]).lower(), store.fold(p["given"]).lower()[:1])
        everyone_idx[ki] = k if ki not in everyone_idx or everyone_idx[ki] == k else None
    everyone_idx = {k: v for k, v in everyone_idx.items() if v}
    p3 = part3(series)
    tagged = collections.Counter()
    for lst in series.lists.values():
        if lst.kind == "calendar":
            for _, e in lst.entries():
                for t in e.get("tags") or []:
                    if str(t).startswith("name:"):
                        tagged[str(t)[5:]] += 1
    cards = cited_cards(series)
    wrows = {cid: work_row(series, cid, everyone_idx) for cid in sorted(cards) if series.works.get(cid)}
    for r in wrows.values():                     # a memoir's subject as its listing writes it: the person's own key
        if r.get("agent"):
            p = by_key.get(r["agent"])
            if p is None:
                parts = r["agent"].split("-")
                p = by_key.get(everyone_idx.get((parts[0], parts[1][:1])) if len(parts) > 1 else None)
            if p is not None:
                r["agent"] = lives.key_of(p["name"])
    agents = {r["agent"] for r in wrows.values() if r.get("agent")}
    names = {}
    for k in sorted(set(tagged) | agents):
        if k not in tagged and k not in by_key:
            continue
        p = by_key.get(k)
        ranks = p["ranks"] if p else set()
        pk = lives.key_of(p["name"]) if p else k
        names[k] = person_row(k, p3.get(k) or p3.get(pk, []), ranks, frus_roles(k) or frus_roles(pk))
    names = merged(old_pol.get("names"), names, refresh)

    # places: the gazetteer's countries, and the hand rows
    from tools.bib import vnmap
    places = dict(PLACES_HAND)
    for k, g in vnmap.gazetteer().items():
        t = f"place:{k}"
        if t not in places:
            c = COUNTRY.get(g.get("country")) or ("rvn" if g.get("province") else None)
            places[t] = [c] if c else {"polities": ["?"], "doubtful": f"the gazetteer's country: {g.get('country')}"}
    places = merged(old_pol.get("places"), places, refresh)

    # threads: the table, every other top-level thread the US
    lst = series.lists["cal"]
    threads = {}
    for slug, te in lst.threads().items():
        if slug in THREADS:
            threads[slug] = THREADS[slug]
        elif not te.get("parent"):
            threads[slug] = ["us"]
    threads = merged(old_pol.get("threads"), threads, refresh)

    pols = dict(POLITIES)
    seen = {x for v in list(names.values()) + list(places.values()) + list(threads.values())
            for x in (store.as_list(v.get("polity") if isinstance(v, dict) and "polity" in v else
                                    v.get("polities") if isinstance(v, dict) else v))}
    for pid in sorted(seen - set(pols) - {"?", None}):
        pols[pid] = {"name": OTHER_NAMES.get(pid, pid.replace("-", " ").title()), "tag": pid.upper()}
    pols = merged(old_pol.get("polities"), pols, refresh)
    write(POL, ["The polities (tools/bib/vis.py, its STYLE; the spec, notes/proposals/visibility-spec.md §2, §4, §8).",
                "Seeded by tools/vis/seed.py (its STYLE 1: who is whose); kept by hand after. A hand row: `hand: true`.",
                "names: a name tag's key -> {polity, basis} (or a list of {polity, from, until} where office or allegiance",
                "changes); places: a tag -> its polities (`state:*` every State); threads: a slug -> its polities (a subthread",
                "not listed takes its parent's). `?`: not known; `doubtful`: a ruling wanted."],
          [("polities", pols, ["Top level (§2): us, ussr, prc, fr, frg, uk; the rest under Other; org: an organization (§2: no polity by default)."]),
           ("threads", threads, []), ("places", places, []), ("names", dict(sorted(names.items())), [])], dry)

    # the registry
    vols, doubts = harvest_volumes()
    vols = merged(old_prov.get("frus_volumes"), vols, refresh)
    surnames = collections.defaultdict(set)
    for k, row in names.items():
        p = row.get("polity") if isinstance(row, dict) else row
        pp = by_key.get(k)
        if pp and p:
            surnames[store.fold(pp["sur"]).lower()].add(p)
    for k, pp in by_key.items():                  # every American's surname: a foreign surname shared with one is no clue
        if k not in names and any(rk in (0, 1, 2) for _, rk in pp["ranks"]):
            surnames[store.fold(pp["sur"]).lower()].add("us")
    surnames = {s: next(iter(ps)) for s, ps in surnames.items() if len(ps) == 1 and "us" not in ps and "?" not in ps}
    fp = parties(frus_links(series), names, surnames)
    fp = merged(old_prov.get("frus_parties"), fp, refresh)
    old_series = {s.get("key"): s for s in old_prov.get("series") or []}
    series_rows = [old_series.get(s["key"]) if s["key"] in old_series and not refresh else s for s in SERIES]
    series_rows += [s for k, s in old_series.items() if k not in {x["key"] for x in SERIES}]
    pubs = {}
    for c, ns in PUBLISHERS.items():
        for n in ns:
            pubs[n] = c
    pubs = merged(old_prov.get("publishers"), pubs, refresh)
    wrows = merged(old_prov.get("works"), wrows, refresh)
    write(PROV, ["The provenance registry (tools/bib/vis.py, its STYLE; the spec, notes/proposals/visibility-spec.md §3, §8).",
                 "Seeded by tools/vis/seed.py (its STYLE 2-3); kept by hand after. A hand row: `hand: true`.",
                 "series: each periodical, official series, document series and archive the calendar cites, its polity and kind",
                 "(vis.KINDS), matched by its links' addresses (`url`) and its names (`text`); frus_volumes: each FRUS volume's",
                 "year of publication as the series' own notes and cards give it; frus_parties: a FRUS document whose heading",
                 "names a party other than the US; publishers: sure of, their country; works: each card the calendar cites,",
                 "its kind, its country (`?` where its publisher is not known) and its first edition's year."],
          [("series", series_rows, []), ("frus_volumes", dict(sorted(vols.items())), []),
           ("frus_volume_doubts", doubts, ["Volumes the notes give two years (the majority's above)."]),
           ("frus_parties", dict(sorted(fp.items())), []), ("publishers", pubs, []),
           ("works", dict(sorted(wrows.items())), [])], dry)


if __name__ == "__main__":
    main("--dry-run" in sys.argv, "--refresh" in sys.argv)
