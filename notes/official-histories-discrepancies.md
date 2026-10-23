# The calendar against the official histories

For the owner. The official histories read against the calendar, Oct. 23, 2026, by their open copies (archive.org's
DTIC scans, the OSD Historical Office's PDF for vol. V), page by page, each page's folio read from its running head:

- OSD: Watson, *Into the Missile Age* (IV); Kaplan, Landa and Drea, *The McNamara Ascendancy* (V); Drea, *McNamara,
  Clifford, and the Burdens of Vietnam* (VI).
- JCS: Poole, *The Joint Chiefs of Staff and National Policy*, 1961–1964 (vol. 8) and 1965–1968 (vol. 9); *The Joint
  Chiefs of Staff and the War in Vietnam, 1960–1968*, pts. 1 (Schulimson, as the title page prints the name), 2 and 3
  (Cosmas).
- Navy: Marolda and Fitzgerald, *From Military Assistance to Combat* (vol. II). Vol. I (Hooper, Allard and
  Fitzgerald) has no open copy: not read.
- Air Force: Futrell, *The Advisory Years*; Van Staaveren, *Gradual Failure* and *Interdiction in Southern Laos*;
  Schlight, *The Years of the Offensive*; Anthony and Sexton, *The War in Northern Laos*.

Read against the dated entries of Defense, Vietnam and its subthreads, Berlin and Vienna, Cuba, Laos, the Dominican
Republic, the Middle East, NATO, testing and arms control, 1960–68: 1,585 entries; 899 carry a bibliography (the
event's first entry) and were matched page by page; 317 take pinpoints (490 pages), in
`inbox/2026-10-23-official-histories.yaml` (patch `official-histories`, every edit with its `base`).

## Disagreements

| Entry | The entry | The history | Other record | Ruling |
|---|---|---|---|---|
| `cal.1960-11-25.defense` | SIOP-62; the Chiefs' approval Dec. 2 (Check). | Watson, 494: the Joint Chiefs approve SIOP-62 Dec. 9, effective Apr. 1, 1961; Dec. 2 the day Gates announced it approved. | None read. | Check added. |
| `cal.1961-06-03.berlin-and-vienna` | Vienna, June 3–4. | Schulimson, 87: June 2–3. | FRUS 1961–63, V, docs. 83–89; XIV, docs. 32–33: dated June 3 and 4. | FRUS settles it. Entry stands. |
| `cal.1962-02-27.vietnam` | The palace bombed Feb. 27. | Marolda and Fitzgerald, 272: Feb. 26. | Schulimson, 186, and Nolting's telegram of Feb. 27 (as he cites it, n. 48): Feb. 27. | Entry stands. |
| `cal.1965-08-18.vietnam` | Starlite, Aug. 18–24. | Drea, 98: Aug. 18–24; 115: Aug. 18–19. | — | Drea against himself; the entry agrees with 98. Entry stands. |
| `cal.1966-07-15.vietnam-operations` | Hastings launched July 15. | Cosmas, 449: "15 June". | Shulimson, *U.S. Marines in Vietnam: An Expanding War, 1966*, the entry's source: July 15. | Entry stands. |
| `cal.1966-10-17.vietnam` | The Asian trip, from Washington Oct. 17. | Drea, 79: Oct. 23–Nov. 2. | The Public Papers: the departure Oct. 17. | Entry stands; not cited there. |
| `cal.1966-12-24.vietnam` | Christmas truce, 48 hours (Check the hours). | Cosmas, 536: the allies' stand-down 0700 Dec. 24 to 0700 Dec. 26, as Saigon announced it Nov. 30. | — | The Check settled: the hours written into `c`, Cosmas cited. |
| `cal.1967-02-22.vietnam-2` | Johnson with McNamara, Eugene Rostow, Taylor and Wheeler. | Drea, 135: Rusk at the meeting, not Eugene Rostow. | FRUS 1964–68, V, doc. 88, n. 2 (the Daily Diary): Eugene Rostow, McNamara, Taylor, Wheeler, Smith, Christian. | Entry stands; Check added naming FRUS. |
| `cal.1967-03-20.vietnam` | Guam, Mar. 20–21. | Cosmas, 104: Mar. 19–21. | The Public Papers: the arrival, the opening session and the dinner Mar. 20; the joint statement and departure Mar. 21. | Entry stands. |
| `cal.1967-06-07.middle-east` | Johnson names the Special Committee June 7. | Drea, 444: decided June 6; 445: its first meeting June 7. | None read. | Check added. |
| `cal.1967-08-14.vietnam-program-5` | McNamara approves Program 5 Aug. 14. | Cosmas, 65: Aug. 10, his memorandum to Wheeler of that date; Drea, 142 (table): Aug. 14. | The memorandum, not read. | Check added; the memorandum added as cited in Cosmas. |
| `cal.1968-05-17.vietnam-operations` | Delaware: some 850 of the enemy killed; 142 American and 26 South Vietnamese dead. | Cosmas, 205: "more than 860"; 168 allied dead. | None read. | The dead agree (142 and 26 are 168). Check added on the enemy count. |
| `cal.1968-06-27.vietnam` | Khe Sanh to be left (Check the day of the announcement). | Cosmas, 211: MACV releases it June 27, Saigon time. | *Victory in Vietnam*, 229 (another agent's Check): June 26. | Not settled. Check added. |
| `cal.1968-07-02.defense` | Harold Johnson retires July 2. | Drea, 194: June 30. | Cosmas, 261, and Poole, 261 (the tables of officers): his term to July 2. | Entry stands. |
| `cal.1968-07-03.vietnam-abrams` | Abrams in acting command since June 11. | Cosmas, 204: acting from May 29; Westmoreland gave up the command June 11. | None read. | Check added. |
| `cal.1968-11-01.vietnam` | About 1,000 contested hamlets (Check the figure and the dates). | Cosmas, 247: more than 1,200, contested or Viet Cong-controlled; Nov. 1–Jan. 31. | — | The dates settled (the Check narrowed to the figure); Check added on the figure. |

## Primary records added

Three, as the histories cite them, marked "(as cited in …)": McNamara's memorandum to Wheeler on Program 5, Aug. 10,
1967 (`cal.1967-08-14.vietnam-program-5`); JCSM-286-67 and JCSM-288-67, May 20, 1967
(`cal.1967-05-20.vietnam-program-5`); JCSM-91-68, Feb. 12, 1968 (`cal.1968-02-12.vietnam-tet`). The JCS histories'
notes cite some fifty other JCSMs on the days of entries; read against them, they are other matters of the same day,
not the entries' acts, and are not added.
