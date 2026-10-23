"""The war's other numbers: the enemy, the Republic of Vietnam's forces, and the other allies. Writes, beside
war-deaths.yaml and war-strength.yaml (tools/indicators/make_war.py), the series of The war table (tools/bib/wartable.py):

    indicators/war-enemy-ob.yaml          MACV's order of battle, the military forces (combat, administrative services,
                                          guerrillas), monthly, Dec. 1964-June 1968, in the format MACV adopted Oct. 31, 1967
    indicators/war-enemy-ob-old.yaml      MACV's order of battle in the format it used before Oct. 31, 1967 (the self-defense
                                          militia and the political cadre counted), Oct. 1967
    indicators/war-enemy-snie.yaml        SNIE 14.3-67 (Nov. 13, 1967), the estimate's figures as of Oct. 1, 1967
    indicators/war-enemy-strength-q.yaml  enemy force strength, quarter's end, Dec. 1967-Dec. 1968, as OSD printed MACV's in
                                          Jan. 1969 (the North Vietnamese fillers in Viet Cong units counted with the NVA)
    indicators/war-infiltration.yaml      infiltration from North Vietnam, monthly, 1965-68: MACV's estimates as first given
                                          and as later revised
    indicators/war-enemy-kia.yaml         enemy killed in action, as MACV reported them (the "body count"), by year and quarter
    indicators/war-rvnaf-kia.yaml         RVNAF killed in action, by year 1960-65 and by month 1966-68: as first counted and as
                                          later revised
    indicators/war-rvnaf-strength.yaml    the Republic of Vietnam Armed Forces' strength: quarterly 1966-68, and by year and
                                          service (Collins, 1975)
    indicators/war-fwmaf-strength.yaml    the Free World Military Assistance Forces in South Vietnam: by year and country,
                                          1964-68 (Larsen and Collins, 1975), and as reported then

    python3 tools/indicators/make_war_forces.py

No network: every figure below was read by eye off the page named with it (the owner's rule: nothing from memory), and
the script checks each table's totals before it writes. The sources:

  Thayer   Thomas C. Thayer ed., *A Systems Analysis View of the Vietnam War, 1965-1972*, 12 vols. (OASD (PA&E), Feb. 18,
           1975): every article of OASD (Systems Analysis)'s monthly *Southeast Asia Analysis Report*, 1967-72, and its
           tables, which cite MACV's and OSD's statistical summaries; open on the Internet Archive from DTIC (vol. 1
           DTIC_ADA039313, vol. 2 DTIC_ADA051609, vol. 8 DTIC_ADA051613). Cited by volume and the volume's page (the
           number at the foot, right).
  Collins  James Lawton Collins, Jr., *The Development and Training of the South Vietnamese Army, 1950-1972* (CMH, 1975),
           app. D, p. 151 (archive.org CMHPub90-10-1).
  Larsen   Stanley Robert Larsen and James Lawton Collins, Jr., *Allied Participation in Vietnam* (CMH, 1975), table 1,
           p. 23 (archive.org CMHPub90-5).
  FRUS     FRUS 1964-68, V, doc. 397: SNIE 14.3-67, Nov. 13, 1967, and the editors' note to it.

Each row: p (period), first (as first given: a count, or a dict of counts; a range is [low, high]), released, source;
now (as later revised or retrospectively given), now_released, now_source; unit 'thousands' where the source prints
thousands (the cells multiply out); note, check (a detail to verify), printed (where a printed total and its parts
disagree). Where only one figure was read for a period, it is "first" if its source is dated within twelve months of
the period's end, else "now" (later): a figure given years after is a retrospective, not a report.
"""
import datetime
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "indicators")

V1 = "https://archive.org/details/DTIC_ADA039313"
V2 = "https://archive.org/details/DTIC_ADA051609"
V8 = "https://archive.org/details/DTIC_ADA051613"
COLLINS_URL = "https://archive.org/details/CMHPub90-10-1"
LARSEN_URL = "https://archive.org/details/CMHPub90-5"
FRUS397 = "https://history.state.gov/historicaldocuments/frus1964-68v05/d397"

T = "Thayer, A Systems Analysis View of the Vietnam War"


# ---------------------------------------------------------------- the enemy's order of battle (thousands)

# MACV's monthly order of battle in its new format (Oct. 31, 1967): combat (VC, NVA), administrative services,
# guerrillas. Thayer, vol. 8, p. 24 (Annex 1 to "VC/NVA Personnel Losses: A New Estimate From Captured Documents",
# SEA Analysis Report, Jan. 1968): "Jan 65-Oct 67 - MACV OB Summary, 31 Oct 67: Nov 67 - MACV OB updating change
# 67-11-3; Dec 67 - MACV OB updating change 67-11-7." The 1965 rows of that copy are too faint to read: 1966-67 only.
OB_P24 = f"MACV OB Summary, Oct. 31, 1967 (Nov.-Dec. 1967: MACV's updating changes); {T}, vol. 8, p. 24"
# (vc, nva, combat, admin, guer, total); None: not legible in the copy
OB67 = {
    "1966-01": (68.6, 28.9, 97.5, 42.8, 95.1, 235.4), "1966-02": (69.0, 35.1, 104.1, 44.3, 96.2, 244.6),
    "1966-03": (69.4, 39.0, 108.4, 45.8, 103.7, 257.9), "1966-04": (70.2, 40.8, 111.0, 46.9, 101.3, 259.2),
    "1966-05": (69.5, 41.7, 111.2, 47.5, 104.8, 263.5), "1966-06": (69.7, 53.9, 123.6, 50.1, 102.2, 275.9),
    "1966-07": (70.8, 54.6, 125.4, 50.1, 106.9, 282.4), "1966-08": (70.9, 55.4, 126.3, 50.1, 109.0, 285.4),
    "1966-09": (72.0, 55.2, 127.2, 50.5, 109.0, 286.7), "1966-10": (69.7, 51.6, 121.3, 47.9, 118.7, 287.9),
    "1966-11": (68.0, 47.9, 115.9, 45.1, 123.1, 284.1), "1966-12": (66.9, 49.1, 116.0, 41.7, 126.2, 283.9),
    "1967-01": (66.4, 48.5, 114.9, 41.6, 124.8, 281.3), "1967-02": (65.9, 48.4, 114.3, 40.9, 120.2, 275.4),
    "1967-03": (64.0, 52.8, 116.8, 39.7, 113.1, 269.6), "1967-04": (63.6, 56.4, 120.0, 39.0, 104.5, 263.5),
    "1967-05": (63.9, 54.8, 118.7, 38.1, 99.0, 255.8), "1967-06": (63.3, 54.8, 118.1, 37.8, 94.7, 250.6),
    "1967-07": (63.5, 54.7, 118.2, 37.3, 89.2, 244.7), "1967-08": (63.9, 54.0, 117.9, 37.6, None, None),
    "1967-09": (63.5, 53.8, 117.3, 38.0, None, None), "1967-10": (62.8, 53.7, 116.5, 38.0, 81.3, 235.8),
    "1967-11": (60.3, 54.3, 114.6, 37.6, 81.3, 233.5), "1967-12": (59.8, None, None, 37.7, 71.7, None),
}
OB67_CHECK = {"1967-08": "the guerrillas and the total faint in the copy (86.8? 241.8?)",
              "1967-09": "the guerrillas and the total faint in the copy (82.8? 236.1?)",
              "1967-12": "the NVA, the combat total and the total faint in the copy (55.4? 115.2? 224.6?)"}
# The same summary, semiannual and October, in the new format's retrospective: Thayer, vol. 2, p. 7, table 2
# ("Retrospective Total Enemy Strength (New MACV Presentation Format)", from the MACV Monthly Order of Battle
# Summary, Oct. 31, 1967; SEA Analysis Report, Dec. 1967): the months p. 24 lacks. (combat, admin, guer, total)
OB_V2P7 = f"MACV Monthly Order of Battle Summary, Oct. 31, 1967; {T}, vol. 2, p. 7, table 2"
OB67_SEMI = {"1964-12": (54.8, 35.0, 81.2, 171.0), "1965-06": (70.6, 38.5, 90.3, 199.4),
             "1965-12": (92.3, 41.3, 91.2, 224.8)}
# Revised: OSD Southeast Asia Statistical Summary, table 105, Sept. 3, 1968; Thayer, vol. 8, p. 38 (Annex 1 to
# "VC/NVA Personnel Losses Estimated From Captured Documents", SEA Analysis Report, Oct. 1968). (vc, nva, combat, guer,
# admin, total)
OB_P38 = f"OSD Southeast Asia Statistical Summary, table 105, Sept. 3, 1968; {T}, vol. 8, p. 38"
OB68 = {
    "1965-01": (52.9, 5.9, 58.8, 82.4, 36.8, 178.0), "1965-02": (52.1, 7.7, 59.8, 87.9, 37.1, 184.8),
    "1965-03": (54.9, 8.1, 63.0, 89.5, 37.2, 189.7), "1965-04": (55.9, 10.7, 66.6, 91.0, 37.6, 195.2),
    "1965-05": (60.4, 10.7, 71.1, 88.2, 38.1, 197.4), "1965-06": (61.1, 10.7, 71.8, 90.3, 38.5, 200.6),
    "1965-07": (61.3, 11.0, 72.3, 92.7, 38.8, 203.8), "1965-08": (62.7, 11.7, 74.4, 92.7, 39.0, 206.1),
    "1965-09": (63.5, 16.2, 79.7, 95.7, 39.2, 214.6), "1965-10": (63.8, 22.5, 86.3, 95.4, 40.1, 221.8),
    "1965-11": (65.4, 26.6, 92.0, 90.4, 40.9, 223.3), "1965-12": (65.4, 28.1, 93.5, 89.9, 41.3, 224.7),
    "1966-01": (68.3, 30.5, 98.8, 93.4, 43.2, 235.4), "1966-02": (69.5, 36.7, 106.2, 93.7, 44.7, 244.6),
    "1966-03": (69.0, 40.6, 109.6, 102.0, 46.2, 257.8), "1966-04": (66.7, 42.4, 109.1, 99.7, 47.3, 256.1),
    "1966-05": (69.0, 43.1, 112.1, 103.8, 47.9, 263.8), "1966-06": (69.2, 55.4, 124.6, 101.5, 50.5, 276.6),
    "1966-07": (70.4, 56.1, 126.5, 106.4, 50.5, 283.4), "1966-08": (70.4, 56.9, 127.3, 108.4, 50.5, 286.2),
    "1966-09": (71.6, 56.7, 128.3, 108.3, 50.9, 287.5), "1966-10": (68.6, 53.8, 122.4, 118.6, 48.2, 289.2),
    "1966-11": (66.8, 50.5, 117.3, 122.7, 45.4, 285.4), "1966-12": (66.2, 51.4, 117.6, 126.1, 41.6, 285.3),
    "1967-01": (66.2, 50.8, 117.0, 126.1, 41.2, 284.3), "1967-02": (64.4, 51.1, 115.5, 122.3, 40.4, 278.2),
    "1967-03": (63.2, 55.5, 118.7, 115.3, 39.2, 273.2), "1967-04": (63.4, 58.6, 122.0, 109.2, 38.5, 269.7),
    "1967-05": (64.3, 58.2, 122.5, 102.9, 37.6, 263.0), "1967-06": (62.9, 59.4, 122.3, 102.1, 37.3, 261.7),
    "1967-07": (63.5, 59.2, 122.7, 93.7, 36.8, 253.2), "1967-08": (63.5, 61.7, 125.2, 91.2, 37.1, 253.5),
    "1967-09": (63.6, 61.1, 124.7, 85.1, 37.8, 247.6), "1967-10": (62.7, 62.9, 125.6, 79.3, 37.6, 242.5),
    "1967-11": (62.0, 61.4, 123.4, 76.5, 37.6, 237.5), "1967-12": (61.5, 63.6, 125.1, 69.8, 37.6, 232.5),
    "1968-01": (62.4, 83.4, 145.8, 64.0, 37.6, 247.4), "1968-02": (51.8, 80.3, 132.1, 70.9, 33.6, 236.6),
    "1968-03": (51.4, 83.9, 135.3, 66.0, 33.6, 234.9), "1968-04": (51.8, 82.8, 134.6, 63.3, 33.6, 231.5),
    "1968-05": (50.8, 82.1, 132.9, 53.9, 33.6, 220.4), "1968-06": (50.7, 84.0, 134.7, 51.2, 33.6, 219.5),
}

# The format before Oct. 31, 1967, its October figures: Thayer, vol. 2, p. 8, table 1, column 1 ("Old Estimate, Total
# OB": "the presentation and strength estimates used by MACV before 31 October 1967"); SEA Analysis Report, Dec. 1967.
OLD_SRC = f"MACV's presentation before Oct. 31, 1967; {T}, vol. 2, p. 8, table 1, col. 1"
OLD = {"1967-10": {"vc": 62852, "nva": 53700, "combat": 116552, "admin": 25753, "guer": 37587, "sd": 75173,
                   "political": 39175, "total": 294240}}

# SNIE 14.3-67, "Capabilities of the Vietnamese Communists for Fighting in South Vietnam", Nov. 13, 1967, its figures
# "current as of 1 October 1967" (FRUS 1964-68, V, doc. 397, conclusion C and the editors' note): regular forces
# (NVA/VC main and local forces) 118,000; guerrillas 70,000-90,000; support (administrative services) 35,000-40,000;
# political cadre 75,000-85,000, outside the military total; the self-defense militia not estimated.
SNIE_SRC = "SNIE 14.3-67, Nov. 13, 1967 (as of Oct. 1, 1967); FRUS 1964-68, V, doc. 397 and its note"
SNIE = {"1967-09": {"regular": 118000, "guer": [70000, 90000], "admin": [35000, 40000],
                    "political": [75000, 85000]}}

# Enemy force strength at the quarter's end, 1968: Thayer, vol. 1, p. 126, table 4 ("Trends in 1968", SEA Analysis
# Report, Jan. 1969). The NVA combat troops include 14,500 NVA "fillers and replacements in VC units" (note c); the
# Dec. 1968 figures preliminary (note a); NVA administration "about 5% of the total NVA" where not given (note f).
# (nva, vc, combat, guer, admin_vc, admin_nva, support, total)
Q_SRC = f"OSD, Trends in 1968 (SEA Analysis Report, Jan. 1969), table 4; {T}, vol. 1, p. 126"
ENEMY_Q = {"1967-12": (77.6, 48.6, 126.2, 79.9, 37.5, 0.6, 118.0, 244.2),
           "1968-03": (97.1, 39.1, 136.2, 56.1, 33.5, 0.6, 90.2, 226.4),
           "1968-06": (101.7, 38.8, 140.5, 55.6, 33.5, 0.6, 89.7, 230.2),
           "1968-09": (99.0, 38.8, 137.8, 82.0, 33.5, 1.8, 117.3, 255.1),
           "1968-12": (125.0, 37.0, 162.0, 65.0, 39.0, None, 104.0, 266.0)}

# ---------------------------------------------------------------- infiltration (persons)

# Total infiltration (confirmed, probable and possible) as MACV first gave each month: the first figure in Thayer,
# vol. 2, p. 64, table 2 ("Total Infiltration Over Time - Monthly"; source: MACV monthly reports of NVN infiltration
# into SVN; SEA Analysis Report, Feb. 1968): (figure, months after the month when MACV gave it).
INF_FIRST_SRC = f"MACV monthly report of NVN infiltration into SVN; {T}, vol. 2, p. 64, table 2"
INF_FIRST = {
    "1966-01": (2600, 2), "1966-02": (3450, 1), "1966-03": (4000, 1), "1966-04": (130, 1), "1966-05": (4450, 1),
    "1966-06": (2500, 0), "1966-07": (2120, 0), "1966-08": (350, 0), "1966-09": (400, 1), "1966-10": (2000, 0),
    "1966-11": (280, 1), "1966-12": (530, 1),
    "1967-01": (700, 1), "1967-02": (500, 1), "1967-03": (900, 1), "1967-04": (100, 0), "1967-05": (500, 1),
    "1967-06": (3300, 2), "1967-07": (400, 1), "1967-08": (400, 0), "1967-09": (1300, 1), "1967-10": (1200, 1),
    "1967-11": (800, 1),
}
# Oct.-Dec. 1965 as of Mar. 1, 1967 (the earliest read): Thayer, vol. 2, p. 33, table 1 ("Infiltration Estimates";
# source: MACV Monthly Report of NVN Infiltration into SVN, Mar. 1, 1967). (accepted, possible, total)
INF_MAR67_SRC = f"MACV Monthly Report of NVN Infiltration into SVN, Mar. 1, 1967; {T}, vol. 2, p. 33, table 1"
INF_MAR67 = {"1965-10": (6000, 700, 6700), "1965-11": (1800, 600, 2400), "1965-12": (2400, 200, 2600)}
# MACV's estimates of Dec. 31, 1967, by month, 1965-67: Thayer, vol. 2, p. 62, table 1 ("NVA Infiltration into South
# Vietnam"; source: MACV; SEA Analysis Report, Feb. 1968). (confirmed, probable, accepted, possible, total); 0: "-".
INF_DEC67_SRC = f"MACV, as of Dec. 31, 1967; {T}, vol. 2, p. 62, table 1"
INF_DEC67 = {
    "1965-01": (2000, 0, 2000, 1200, 3200), "1965-02": (2800, 400, 3200, 600, 3800),
    "1965-03": (500, 400, 900, 400, 1300), "1965-04": (2400, 0, 2400, 700, 3100),
    "1965-05": (0, 300, 300, 100, 400), "1965-06": (0, 200, 200, 300, 500),
    "1965-07": (400, 0, 400, 700, 1100), "1965-08": (0, 0, 0, 900, 900),
    "1965-09": (5700, 0, 5700, 2200, 7900), "1965-10": (7000, 0, 7000, 400, 7400),
    "1965-11": (3300, 0, 3300, 1000, 4300), "1965-12": (200, 400, 600, 800, 1400),
    "1966-01": (4200, 2000, 6200, 3000, 9200), "1966-02": (6800, 2300, 9100, 2100, 11200),
    "1966-03": (11800, 1300, 13100, 3600, 16700), "1966-04": (100, 500, 600, 600, 1200),
    "1966-05": (1800, 400, 2200, 3600, 5800), "1966-06": (12300, 700, 13000, 2200, 15200),
    "1966-07": (4000, 700, 4700, 4200, 8900), "1966-08": (1800, 400, 2200, 3700, 5900),
    "1966-09": (1400, 700, 2100, 700, 2800), "1966-10": (100, 600, 700, 5200, 5900),
    "1966-11": (900, 100, 1000, 600, 1600), "1966-12": (1000, 600, 1600, 2500, 4100),
    "1967-01": (1000, 800, 1800, 4300, 6100), "1967-02": (1700, 2000, 3700, 1500, 5200),
    "1967-03": (4300, 400, 4700, 4600, 9300), "1967-04": (4300, 600, 4900, 400, 5300),
    "1967-05": (4000, 1300, 5300, 1500, 6800), "1967-06": (5400, 0, 5400, 1800, 7200),
    "1967-07": (1600, 0, 1600, 1300, 2900), "1967-08": (3800, 0, 3800, 2000, 5800),
    "1967-09": (400, 100, 500, 1800, 2300), "1967-10": (1100, 0, 1100, 800, 1900),
    "1967-11": (0, 0, 0, 800, 800),
}
INF_DEC67_TOTALS = {"1965": (24300, 1700, 26000, 9300, 35300), "1966": (46200, 10300, 56500, 32000, 88500),
                    "1967": (27600, 5200, 32800, 20800, 53600)}
# MACV's estimate of Oct. 31, 1968: Thayer, vol. 2, p. 71, table 1 ("Estimated NVA Infiltration Into SVN - 1968",
# column "31 Oct 68 MACV Estimate", from OSD SEA Statistical Summary, table 5, Nov. 12, 1968). Oct. 1968 "NA".
INF_OCT68_SRC = f"MACV, as of Oct. 31, 1968 (OSD SEA Statistical Summary, Nov. 12, 1968, table 5); {T}, vol. 2, p. 71"
INF_OCT68 = {"1967-07": 7400, "1967-08": 8400, "1967-09": 6300, "1967-10": 4800, "1967-11": 6200, "1967-12": 6300,
             "1968-01": 21900, "1968-02": 12100, "1968-03": 19900, "1968-04": 18100, "1968-05": 11600,
             "1968-06": 11200, "1968-07": 4200, "1968-08": 4300, "1968-09": 400}
# MACV's reported figures of Aug. 7 and Sept. 2, 1969 (thousands): Thayer, vol. 2, p. 80, annex table 1 ("Reported
# and Adjusted MACV Infiltration Estimates, June 1968-June 1969", the "reported figure"; SEA Analysis Report, Sept.
# 1969). The adjusted figures are OSD's projections, not MACV's: not taken.
INF_69_SRC = f"MACV Monthly Report of NVN Infiltration into SVN, Aug. 7 and Sept. 2, 1969; {T}, vol. 2, p. 80"
INF_69 = {"1968-06": 11.6, "1968-07": 10.1, "1968-08": 11.5, "1968-09": 4.4, "1968-10": 3.5, "1968-11": 2.9,
          "1968-12": 1.2}

# ---------------------------------------------------------------- killed

# Enemy killed in action, as reported (body counts). CY 1966: Thayer, vol. 8, p. 5 ("Estimates of VC/NVA Combat
# Deaths", SEA Analysis Report, Nov. 1967: "Official reports of enemy combat deaths (KIA) ... numbered 55,524 for CY
# 66"). 1967, 1968 and the quarters of 1968: Thayer, vol. 1, p. 123, table 1 ("Trends in 1968", Jan. 1969; source: OSD
# (C) SEA Statistical Summary; "P indicates preliminary figure").
KIA_66_SRC = f"Official reports (body counts); {T}, vol. 8, p. 5 (SEA Analysis Report, Nov. 1967)"
KIA_68_SRC = f"OSD (C) SEA Statistical Summary; {T}, vol. 1, p. 123, table 1 (SEA Analysis Report, Jan. 1969)"
ENEMY_KIA = [("1966", 55524, "1967-11", KIA_66_SRC, None),
             ("1967", 88104, "1969-01", KIA_68_SRC, None),
             ("1968Q1", 72455, "1969-01", KIA_68_SRC, None), ("1968Q2", 46620, "1969-01", KIA_68_SRC, None),
             ("1968Q3", 34666, "1969-01", KIA_68_SRC, None), ("1968Q4", 27217, "1969-01", KIA_68_SRC, "preliminary"),
             ("1968", 180966, "1969-01", KIA_68_SRC, "preliminary")]
KIA_68_PRINTED = "the quarters as printed add to 180,958; the year is printed 180,966P"

# RVNAF killed in action (died of wounds included; non-combat deaths excluded), by year, 1960-65: Thayer, vol. 8, p.
# 205, table 1 ("Friendly Casualties in SVN (Yearly Totals)", from the SEA Statistical Summary, table 15, Aug. 8, 1967).
RVN_YEAR_SRC = f"SEA Statistical Summary, table 15, Aug. 8, 1967; {T}, vol. 8, p. 205, table 1"
RVN_YEAR = {"1960": 2223, "1961": 4004, "1962": 4457, "1963": 5665, "1964": 7457, "1965": 11243}
RVN_YEAR_REST = {"1966": 9469, "1967-07": 6174, "cum": 50692}     # the table's 1966, 1967 through July 31, total
# By month, 1966-67: Thayer, vol. 8, p. 212, table 1 ("US Versus RVNAF Combat Deaths", SEA Analysis Report, Feb.
# 1968): OSD's figures (OASD SEA Statistical Summary, table 2, "based on MACV Combat Operations Center reports in weekly
# OpRep 5 summaries"), as Washington held them, and MACV J-1's refined figures.
RVN_M_SRC = f"OASD SEA Statistical Summary, table 2 (from OPREP-5); {T}, vol. 8, p. 212, table 1"
RVN_M_J1_SRC = f"MACV J-1, refined (Feb. 1968); {T}, vol. 8, p. 212, table 1"
RVN_OSD = {"1966": [747, 1016, 938, 574, 661, 850, 860, 722, 566, 906, 804, 815],
           "1967": [887, 771, 1118, 935, 1026, 771, 666, 852, 740, 753, 1122]}
RVN_J1 = {"1966": [903, 1359, 1145, 945, 961, 1165, 1006, 914, 803, 844, 907, 981],
          "1967": [910, 885, 1297, 1057, 1184, 981, 675, 1068, 1090, 1066, 1299]}
RVN_M_TOTALS = {("osd", "1966"): 9469, ("osd", "1967"): 9641, ("j1", "1966"): 11953, ("j1", "1967"): 11513}
# By month, 1968: Thayer, vol. 8, p. 216, table 1 ("Comparison of RVNAF Verified and OPREP-5 KIA Numbers for 1968";
# "RVNAF KIA in 1968", SEA Analysis Report, Mar. 1969; source OASD(C) Statistical Services; Regular, Regional and
# Popular Forces): OPREP-5, as held in Washington, and the final verified figures of the Joint General Staff.
RVN_68_SRC = f"OPREP-5, as held in Washington; {T}, vol. 8, p. 216, table 1"
RVN_68_V_SRC = f"JGS final verified figures (Mar. 1969); {T}, vol. 8, p. 216, table 1"
RVN_68_OP = [1449, 2443, 1544, 1312, 1969, 1367, 828, 1544, 1538, 678, 849, 832]
RVN_68_V = [2662, 4524, 2238, 1562, 2977, 1702, 1206, 2091, 1850, 971, 1257, 1225]
RVN_68_TOTALS = (16353, 24265)

# ---------------------------------------------------------------- the RVNAF's strength

# Average strength (Regular, Regional and Popular Forces), by quarter, thousands: Thayer, vol. 8, p. 212, table 2
# ("Revised US and RVNAF Combat Death Rates", Feb. 1968).
RVNAF_AVG_SRC = f"{T}, vol. 8, p. 212, table 2 (average strength, Regular, RF and PF)"
RVNAF_AVG = {"1966Q1": 581.7, "1966Q2": 588.4, "1966Q3": 602.9, "1966Q4": 618.8,
             "1967Q1": 609.1, "1967Q2": 607.6, "1967Q3": 613.3}
# At the period's end, thousands: Thayer, vol. 1, p. 126, table 4 (Jan. 1969; Dec. 1968 preliminary).
RVNAF_Q = {"1967-12": 643.1, "1968-03": 677.6, "1968-06": 765.3, "1968-09": 816.0, "1968-12": 826.3}
# By year and service: Collins, app. D, p. 151 ("Republic of Vietnam Armed Forces Strength"; "all figures are
# approximate only"). (army, af, navy, marines, regular, rf, pf, territorial, total)
COLLINS_SRC = "Collins, The Development and Training of the South Vietnamese Army (1975), app. D, p. 151"
COLLINS = {"1964": (220000, 11000, 12000, 7000, 250000, 96000, 168000, 264000, 514000),
           "1967": (303000, 16000, 16000, 8000, 343000, 151000, 149000, 300000, 643000),
           "1968": (380000, 19000, 19000, 9000, 427000, 220000, 173000, 393000, 820000)}

# ---------------------------------------------------------------- the other allies

# By year and country: Larsen and Collins, table 1, p. 23 ("Strength of Free World Military Assistance Forces,
# 1964-1970 (Strength by Calendar Year)"). (korea, australia, thailand, nz, phil, roc, spain, total)
LARSEN_SRC = "Larsen and Collins, Allied Participation in Vietnam (1975), table 1, p. 23"
LARSEN = {"1964": (200, 200, 0, 30, 17, 20, 0, 467), "1965": (20620, 1557, 16, 119, 72, 20, 0, 22404),
          "1966": (45566, 4525, 244, 155, 2061, 23, 13, 52566), "1967": (47829, 6818, 2205, 534, 2020, 31, 13, 59450),
          "1968": (50003, 7661, 6005, 516, 1576, 29, 12, 65802)}
LARSEN_BN = {"1965": (10, 1, 0), "1966": (22, 2, 0), "1967": (22, 2, 1), "1968": (22, 3, 3)}   # maneuver battalions
LARSEN_PRINTED = {"1966": "the countries as printed add to 52,587; the total is printed 52,566"}
# Third Nation Forces, thousands, at the period's end: Thayer, vol. 1, p. 126, table 4 (Jan. 1969).
FW_Q = {"1967-12": 59.4, "1968-03": 61.0, "1968-06": 62.4, "1968-09": 66.0, "1968-12": 65.7}
# SNIE 14.3-67, conclusion C's note: the forces arrayed against the Communists, Oct. 1, 1967.
SNIE_FW = {"korea": 45000, "australia": 6300, "thailand": 2500, "phil": 2000, "nz": 400}


# ---------------------------------------------------------------- checks of the transcription

def _close(a, b, tol=0.05):
    return abs(a - b) < tol


def check():
    bad = []
    for k, (vc, nva, c, a, g, t) in OB67.items():
        if None not in (vc, nva, c) and not _close(vc + nva, c):
            bad.append(f"OB67 {k}: VC+NVA")
        if None not in (c, a, g, t) and not _close(c + a + g, t):
            bad.append(f"OB67 {k}: total")
    for k, (c, a, g, t) in OB67_SEMI.items():
        if not _close(c + a + g, t):
            bad.append(f"OB67_SEMI {k}")
    for k, (vc, nva, c, g, a, t) in OB68.items():
        if not _close(vc + nva, c) or not _close(c + g + a, t):
            bad.append(f"OB68 {k}")
    o = OLD["1967-10"]
    if o["vc"] + o["nva"] != o["combat"] or o["combat"] + o["admin"] + o["guer"] + o["sd"] + o["political"] != o["total"]:
        bad.append("OLD")
    for k, (nva, vc, c, g, av, an, s, t) in ENEMY_Q.items():
        if not _close(nva + vc, c) or not _close(g + av + (an or 0), s) or not _close(c + s, t):
            bad.append(f"ENEMY_Q {k}")
    for k, (cf, pr, ac, po, tt) in INF_DEC67.items():
        if cf + pr != ac or ac + po != tt:
            bad.append(f"INF_DEC67 {k}")
    for y, tot in INF_DEC67_TOTALS.items():
        rows = [v for k, v in INF_DEC67.items() if k.startswith(y)]
        if tuple(sum(r[i] for r in rows) for i in range(5)) != tot:
            bad.append(f"INF_DEC67 {y} totals")
    for k, (ac, po, tt) in INF_MAR67.items():
        if ac + po != tt:
            bad.append(f"INF_MAR67 {k}")
    if sum(RVN_YEAR.values()) + RVN_YEAR_REST["1966"] + RVN_YEAR_REST["1967-07"] != RVN_YEAR_REST["cum"]:
        bad.append("RVN_YEAR cumulative")
    if sum(RVN_OSD["1967"][:7]) != RVN_YEAR_REST["1967-07"]:
        bad.append("RVN_OSD 1967 Jan.-July against p. 205")
    if (sum(RVN_68_OP), sum(RVN_68_V)) != RVN_68_TOTALS:
        bad.append("RVN_68 totals")
    for k, r in COLLINS.items():
        if sum(r[:4]) != r[4] or r[5] + r[6] != r[7] or r[4] + r[7] != r[8]:
            bad.append(f"COLLINS {k}")
    for k, r in LARSEN.items():
        if sum(r[:7]) != r[7] and k not in LARSEN_PRINTED:
            bad.append(f"LARSEN {k}")
    return bad


# ---------------------------------------------------------------- writing

def ends(p):
    p = str(p)
    if "Q" in p:
        y, q = p.split("Q")
        m = 3 * int(q)
        y = int(y)
    elif "-" in p:
        y, m = int(p[:4]), int(p[5:7])
    else:
        y, m = int(p), 12
    nxt = datetime.date(y + (m == 12), m % 12 + 1, 1)
    return nxt - datetime.timedelta(days=1)


def rel_date(r):
    r = str(r)
    if len(r) == 4:
        return datetime.date(int(r), 1, 1)
    if len(r) == 7:
        y, m = int(r[:4]), int(r[5:])
        return datetime.date(y, m, 1)
    return datetime.date.fromisoformat(r)


def one(p, v, released, source, **kw):
    """A period read from one source only: first if the source is dated within a year of the period's end, else now."""
    late = (rel_date(released) - ends(p)).days > 366
    r = {"p": p}
    if late:
        r.update(now=v, now_released=released, now_source=source)
    else:
        r.update(first=v, released=released, source=source)
    r.update({k: x for k, x in kw.items() if x is not None})
    return r


def add_month(p, k):
    y, m = int(p[:4]), int(p[5:7]) + k
    y += (m - 1) // 12
    m = (m - 1) % 12 + 1
    return f"{y}-{m:02d}"


def q(s):
    return "'" + str(s).replace("'", "''") + "'"


def val(v):
    if isinstance(v, dict):
        return "{" + ", ".join(f"{a}: {val(b)}" for a, b in v.items()) + "}"
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(val(x) for x in v) + "]"
    if isinstance(v, str):
        return q(v)
    return str(v)


def write(sid, name, then, now, rows, extra=""):
    rows = sorted(rows, key=lambda r: (ends(r["p"]), 0 if ("-" in r["p"] or "Q" in r["p"]) else 1))
    text = ("# Generated by tools/indicators/make_war_forces.py. Edit the script, not this file.\n"
            "# p: period; first: as first given (released, source); now: as later given (now_released, now_source);\n"
            "# unit: thousands where the source prints thousands; a range is [low, high].\n"
            f"id: {sid}\nname: {q(name)}\nfreq: M\nmanual: true\nkind: war\n{extra}"
            f"then: {{label: {q(then)}}}\nnow: {{label: {q(now)}}}\nrows:\n"
            + "\n".join("- " + val(r) for r in rows) + "\n")
    open(os.path.join(OUT, f"{sid}.yaml"), "w").write(text)
    return len(rows)


def nz(d):
    return {k: v for k, v in d.items() if v is not None}


def main():
    bad = check()
    if bad:
        sys.exit("transcription does not add: " + "; ".join(bad))
    out = {}

    # the order of battle, new format
    rows = []
    for p in sorted(set(OB67) | set(OB67_SEMI) | set(OB68)):
        r = {"p": p, "unit": "thousands"}
        if p in OB67:
            vc, nva, c, a, g, t = OB67[p]
            r.update(first=nz({"combat": c, "vc": vc, "nva": nva, "admin": a, "guer": g, "total": t}),
                     released="1967-10-31" if p <= "1967-10" else "1968-01", source=OB_P24)
            if p in OB67_CHECK:
                r["check"] = OB67_CHECK[p]
        elif p in OB67_SEMI:
            c, a, g, t = OB67_SEMI[p]
            r.update(first={"combat": c, "admin": a, "guer": g, "total": t}, released="1967-10-31", source=OB_V2P7)
        if p in OB68:
            vc, nva, c, g, a, t = OB68[p]
            v = {"combat": c, "vc": vc, "nva": nva, "admin": a, "guer": g, "total": t}
            if "first" in r:
                r.update(now=v, now_released="1968-09-03", now_source=OB_P38)
            else:
                rr = one(p, v, "1968-09-03", OB_P38)
                rr["unit"] = "thousands"
                r = rr
        rows.append(r)
    out["war-enemy-ob"] = write(
        "war-enemy-ob", "Enemy forces, MACV's order of battle", "MACV's order of battle, new format, as first given",
        "MACV's order of battle, new format, as revised (OSD, Sept. 3, 1968)", rows)

    out["war-enemy-ob-old"] = write(
        "war-enemy-ob-old", "Enemy forces, MACV's order of battle, old format",
        "MACV's order of battle in its presentation before Oct. 31, 1967", "—",
        [{"p": "1967-10", "first": OLD["1967-10"], "released": "1967-10-31", "source": OLD_SRC}])

    out["war-enemy-snie"] = write(
        "war-enemy-snie", "Enemy forces, the national estimate (SNIE 14.3-67)",
        "SNIE 14.3-67, the figures as of Oct. 1, 1967", "—",
        [{"p": "1967-09", "first": SNIE["1967-09"], "released": "1967-11-13", "source": SNIE_SRC,
          "note": "political cadre outside the military total; self-defense militia not estimated"}])

    rows = []
    for p, (nva, vc, c, g, av, an, s, t) in ENEMY_Q.items():
        v = nz({"combat": c, "vc": vc, "nva": nva, "guer": g, "admin": av, "admin_nva": an, "total": t})
        rows.append(one(p, v, "1969-01", Q_SRC, unit="thousands",
                        note="NVA include 14,500 fillers in VC units"
                        + ("; preliminary" if p == "1968-12" else "")))
    out["war-enemy-strength-q"] = write(
        "war-enemy-strength-q", "Enemy forces at the quarter's end", "MACV's figures as OSD printed them, Jan. 1969",
        "MACV's figures as OSD printed them, Jan. 1969", rows)

    # infiltration
    rows = []
    months = sorted(set(INF_FIRST) | set(INF_MAR67) | set(INF_DEC67) | set(INF_OCT68) | set(INF_69))
    for p in months:
        vint = []                      # (released, value, source)
        if p in INF_MAR67:
            ac, po, tt = INF_MAR67[p]
            vint.append(("1967-03-01", {"accepted": ac, "possible": po, "total": tt}, INF_MAR67_SRC, None))
        if p in INF_FIRST:
            v, k = INF_FIRST[p]
            vint.append((add_month(p, k), {"total": v}, INF_FIRST_SRC, None))
        if p in INF_DEC67:
            cf, pr, ac, po, tt = INF_DEC67[p]
            vint.append(("1967-12-31", {"accepted": ac, "possible": po, "total": tt}, INF_DEC67_SRC, None))
        if p in INF_OCT68:
            vint.append(("1968-10-31", {"total": INF_OCT68[p]}, INF_OCT68_SRC, None))
        if p in INF_69:
            vint.append(("1969-09-02", {"total": INF_69[p]}, INF_69_SRC, "thousands"))
        vint.sort(key=lambda x: rel_date(x[0]))
        if len(vint) == 1:
            r = one(p, vint[0][1], vint[0][0], vint[0][2])
            if vint[0][3]:
                r["unit_" + ("now" if "now" in r else "first")] = vint[0][3]
        else:
            (fr, fv, fs, fu), (lr, lv, ls, lu) = vint[0], vint[-1]
            r = {"p": p, "first": fv, "released": fr, "source": fs, "now": lv, "now_released": lr, "now_source": ls}
            if fu:
                r["unit_first"] = fu
            if lu:
                r["unit_now"] = lu
        rows.append(r)
    out["war-infiltration"] = write(
        "war-infiltration", "Infiltration from North Vietnam", "MACV's estimate as first given",
        "MACV's estimate as later given", rows)

    # enemy killed
    rows = []
    for p, v, rel, src, note in ENEMY_KIA:
        r = one(p, v, rel, src, note=note)
        if p == "1968":
            r["printed"] = KIA_68_PRINTED
        rows.append(r)
    out["war-enemy-kia"] = write("war-enemy-kia", "Enemy killed in action, as reported",
                                 "Enemy KIA as MACV reported them (body counts)", "—", rows)

    # RVNAF killed
    rows = [one(p, {"rvnaf": v}, "1967-08-08", RVN_YEAR_SRC) for p, v in RVN_YEAR.items()]
    for y in ("1966", "1967"):
        for i, (a, b) in enumerate(zip(RVN_OSD[y], RVN_J1[y])):
            rows.append({"p": f"{y}-{i + 1:02d}", "first": {"rvnaf": a}, "released": "1968-02", "source": RVN_M_SRC,
                         "now": {"rvnaf": b}, "now_released": "1968-02", "now_source": RVN_M_J1_SRC})
    for i, (a, b) in enumerate(zip(RVN_68_OP, RVN_68_V)):
        rows.append({"p": f"1968-{i + 1:02d}", "first": {"rvnaf": a}, "released": "1969-03", "source": RVN_68_SRC,
                     "now": {"rvnaf": b}, "now_released": "1969-03", "now_source": RVN_68_V_SRC})
    for r in rows:
        if r["p"] == "1966-12":
            r["printed"] = "the months of 1966 as read add to 9,459 (OSD) and 11,933 (J-1); printed 9,469 and 11,953"
        if r["p"] == "1967-11":
            r["printed"] = "the months of 1967 as read add to 11,512 (J-1); printed 11,513"
    out["war-rvnaf-kia"] = write("war-rvnaf-kia", "South Vietnamese forces killed in action",
                                 "RVNAF KIA as first counted (OPREP-5)", "RVNAF KIA as revised (MACV J-1; JGS)", rows)

    # RVNAF strength
    rows = [one(p, {"total": v}, "1968-02", RVNAF_AVG_SRC, unit="thousands", note="quarterly average")
            for p, v in RVNAF_AVG.items()]
    rows += [one(p, {"total": v}, "1969-01", Q_SRC, unit="thousands",
                 note="preliminary" if p == "1968-12" else None) for p, v in RVNAF_Q.items()]
    for p, (ar, af, nv, mc, rg, rf, pf, tr, tt) in COLLINS.items():
        rows.append(one(p, {"army": ar, "af": af, "navy": nv, "marines": mc, "regular": rg, "rf": rf, "pf": pf,
                            "territorial": tr, "total": tt}, "1975", COLLINS_SRC, note="approximate"))
    out["war-rvnaf-strength"] = write("war-rvnaf-strength", "South Vietnamese armed forces, strength",
                                      "RVNAF strength as reported then", "RVNAF strength by year and service (1975)", rows)

    # the other allies
    rows = []
    for p, (ko, au, th, nzl, ph, roc, sp, tt) in LARSEN.items():
        v = {"korea": ko, "australia": au, "thailand": th, "nz": nzl, "phil": ph, "roc": roc, "spain": sp, "total": tt}
        r = one(p, v, "1975", LARSEN_SRC)
        if p in LARSEN_BN:
            r["battalions"] = {"korea": LARSEN_BN[p][0], "australia": LARSEN_BN[p][1], "thailand": LARSEN_BN[p][2]}
        if p in LARSEN_PRINTED:
            r["printed"] = LARSEN_PRINTED[p]
        rows.append(r)
    rows += [one(p, {"total": v}, "1969-01", Q_SRC, unit="thousands",
                 note="preliminary" if p == "1968-12" else None) for p, v in FW_Q.items()]
    rows.append({"p": "1967-09", "first": SNIE_FW, "released": "1967-11-13", "source": SNIE_SRC})
    out["war-fwmaf-strength"] = write("war-fwmaf-strength", "Other allied forces in South Vietnam",
                                      "Third-nation forces as reported then", "By year and country (1975)", rows)
    print("; ".join(f"{k} {n} rows" for k, n in out.items()))


if __name__ == "__main__":
    main()
