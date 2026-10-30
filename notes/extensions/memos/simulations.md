# Simulations: discrete proposals and actions, run against the record

The owner, Oct. 29, 2026: "an extension memo, oriented towards making building extensions that 'simulate' the
effects of simple, discrete policy proposals (in Congress) or policy actions (fiscal, monetary, financial) at given
points in time. then, as a 'hook', we could summon and place a simulation in the calendar whenever a bill, budget, or
monetary intervention is amenable to/tractable for the models we've deployed thus far." With it, the question of the
war ("military/COIN simulation. what could we do there?"), §5. Further off, a game (the same conversation: "a big,
narrative-driven, political CYOA/VN/simulation game, one that starts in media res, grounded in a vast body of
ascertained fact, before branching off"), §7. Nothing here is built. Citations marked Check are from memory, not read.

## 1. The rule that keeps the record a record

A simulation reads the record and never writes into it. Its results are a model's, labelled so wherever they show:
never in an entry's `c` or `n`, never a lead, never a source for anything. Each result names its model, its inputs
(each a series figure with its source), the model's own sources, its range, and how the model does on the record
(the backtest, §6). A counterfactual's point of departure is a dated entry; everything after it is the model's.

## 2. The world on a date (the groundwork)

One function, `tools/bib/world.py` (to write), assembling the state of things on any day from what the series holds:
the holders of every office (the Executive roster), each chamber's members, parties and committees, the leaders
(`congress/`), the indicators as first reported and today, the latest poll (`indicators/`, `sources/gallup-approval.yaml`),
the war's figures (the war table), the threads under way and the day's documents (the daybook). Every model below
starts from it; so would the game. Mostly assembly: the pieces exist.

## 3. Congress: what could have passed, and where

- **The data.** DW-NOMINATE's ideal points, both dimensions, for every member of the 86th–91st Congresses, and every
  roll call with its cutting line (Voteview, open; the series already reads its nomination votes:
  `tools/executive/make_votes.py`). The second dimension matters in these Congresses: the civil-rights split within the
  Democrats.
- **The model.** Krehbiel's pivots (Keith Krehbiel, *Pivotal Politics* (1998)): the floor median, the filibuster pivot
  (cloture at two-thirds of those present and voting, Rule XXII until Mar. 7, 1975), the veto pivot (two-thirds of each
  chamber); and the gatekeepers (Gary W. Cox and Mathew D. McCubbins, *Setting the Agenda* (2005)): the Rules
  Committee's median and the committee of jurisdiction's, its chairman (`congress/committees.yaml`, with the dated
  changes). A proposal is a point or a cutting line; the answer, on a date, which pivots it clears and by how much, and
  the members nearest each line.
- **The backtest.** The bills whose course `congress/bills.yaml` traces, and every roll call: how often the model calls
  the outcome, and where it fails (Rules bottling up a bill a floor majority wanted; cloture on civil rights, 1964).
- **The calendar hook.** A signing, a passage, a cloture vote or a bill's death in committee (§4): what the pivots
  were that day, and the margin.
- **Then and now.** The period's own counting: the whip counts and head counts the memoirs and the tapes give (the
  informal record, by page), beside the model's.

## 4. Fiscal, monetary and financial actions

- **The period's own models (first).** Each published, each on FRASER or open: the Council's arithmetic in the
  *Economic Report* (Okun's law: Arthur M. Okun, *Potential GNP: Its Measurement and Significance* (1962); the
  full-employment surplus; each January's forecast); the St. Louis equation (Leonall C. Andersen and Jerry L. Jordan,
  *Monetary and Fiscal Actions: A Test of Their Relative Importance in Economic Stabilization*, Fed. Res. Bank St.
  Louis Rev., Nov. 1968; Check: volume, page); the Federal Reserve–MIT model (Frank de Leeuw and Edward M. Gramlich,
  *The Federal Reserve–MIT Econometric Model*, Fed. Res. Bull., Jan. 1968; Check: page); the Brookings model (James S.
  Duesenberry, Gary Fromm, Lawrence R. Klein and Edwin Kuh eds., *The Brookings Quarterly Econometric Model of the
  United States* (1965)). Their disagreement, money against fiscal policy, was the period's argument; run side by side,
  it is history as well as a model.
- **Today's estimates (second).** Responses to a shock, each cited, applied to the baseline as first reported, with
  their ranges: taxes (Christina D. Romer and David H. Romer, *The Macroeconomic Effects of Tax Changes*, 100 Am. Econ.
  Rev. 763 (2010)); defense spending (Valerie A. Ramey, *Identifying Government Spending Shocks: It's All in the
  Timing*, 126 Q.J. Econ. 1 (2011)); monetary policy (the Romers' dates, from Dec. 1968; the policy-rule gaps the series
  already computes, `tools/indicators/make_derived.py`). The estimates disagree (a tax multiplier near 3 against others
  near 1): show the spread, never one figure.
- **The open economy (third, once the data is built).** What bound policy then: the gold stock and the dollar
  overhang, the balance of payments, Operation Twist, the Interest Equalization Tax, the London gold pool, sterling's
  devaluation (Nov. 18, 1967), the gold crisis (Mar. 1968), Regulation Q's ceilings and the credit crunch of 1966. The
  series holds the U.S. side (exchange rates, reserve assets, the payments balances, money, rates, the debt's terms);
  it lacks the other economies, capital flows, the London gold price (`gold-london` waits a source), the ceilings, and
  the flow of funds. To find: the Federal Reserve's Financial Accounts (Z.1, from 1945, FRED), the IMF's International
  Financial Statistics and the OECD's Main Economic Indicators (historical, the major economies), the *Federal Reserve
  Bulletin*'s international tables and Regulation Q's ceilings.
- **The calendar hook.** A tax act with Tempalski's revenue effect (the signing entries already cite it); a budget
  entry (`budget:<FY>`); a discount-rate change (the Money and credit table's dated changes); the surcharge's delay
  (Jan. 1967–June 1968). Each: the period's models' answer, then today's, the range.

## 5. The war

- **The period's own analysis (first).** The Systems Analysis office's figures the series already reads (Thomas C.
  Thayer, *A Systems Analysis View of the Vietnam War* (1975): the war table): the crossover point (losses against
  infiltration and recruitment, McNamara's and Westmoreland's measure), and Thayer's finding that the enemy began most
  engagements and so set his own losses (Alain C. Enthoven and K. Wayne Smith, *How Much Is Enough?* (1971)). A
  crossover calculator from the war table's figures, as first given and later: when, at the rates of a given month,
  the enemy's strength turns down, and how much a change in infiltration or initiative moves it.
- **Lanchester's equations and their guerrilla form.** Frederick W. Lanchester, *Aircraft in Warfare* (1916): attrition
  in proportion to the enemy's numbers (aimed fire) or to both sides' (area fire). The guerrilla model of the period:
  Seymour J. Deitchman, *A Lanchester Model of Guerrilla Warfare*, 10 Operations Research 818 (1962) (Check: page),
  the guerrilla hidden, so attacked by area fire, the government seen, so attacked by aimed fire; RAND's extensions
  (Check: Schaffer, 1967). Cheap to build, easy to fit to Thayer's engagement figures, plain about what it leaves out.
- **What planners used.** Force ratios (three to one in the attack; for counterinsurgency the period's rule of ten
  to one, from Malaya; today's force density, 20 to 25 troops a 1,000 people: James T. Quinlivan, *Force Requirements
  in Stability Operations*, Parameters, Winter 1995); Trevor N. Dupuy's quantified judgment (*Numbers, Predictions and
  War* (1979); *Attrition* (1990)); the supply arithmetic (tons a day down the trail against interdiction: the Jason
  summer study of Aug. 1966, printed in the Pentagon Papers; Check). The Army's and the Joint Staff's models (CEM,
  TACWAR) are not open.
- **The period's wargames.** The Joint War Games Agency's SIGMA I-64 (Apr. 1964) and SIGMA II-64 (Sept. 1964), the
  escalation games whose players found Hanoi would not fold: papers of government, so calendar entries in their own
  right (Check: where FRUS or the Pentagon Papers print them).
- **Board wargames, for their logic.** Volko Ruhnke and Mark Herman's *Fire in the Lake* (GMT, 2014), of the COIN series
  designed by a CIA analyst: four factions; control and support kept apart (who holds a province, and whom its people
  back); resources, operations and special activities; events by card. Nick Karp's *Vietnam 1965–1975* (Victory
  Games, 1984): the operational war with the home front's will as a track. Their abstractions are worth borrowing; their
  numbers are designers' judgments, not data.
- **The home front.** John E. Mueller, *War, Presidents and Public Opinion* (1973): support falling with the log of
  cumulative casualties; Scott Sigmund Gartner and Gary M. Segura on recent losses (Check: 42 J. Conflict Resol. 278
  (1998)). Testable against the series' own Gallup readings and the DCAS counts.
- **The ground truth, where it exists.** The Hamlet Evaluation System's monthly ratings, 1967–73 (NARA, RG 472; the
  military memo's §5, not yet built); its use since (Stathis N. Kalyvas and Matthew Adam Kocher, *The Dynamics of
  Violence in Vietnam*, 46 J. Peace Res. 335 (2009); Melissa Dell and Pablo Querubin, *Nation Building Through Foreign
  Intervention*, 133 Q.J. Econ. 701 (2018); Check both pages). The base rates of insurgencies' length and end (Ben
  Connable and Martin C. Libicki, *How Insurgencies End* (2010)).
- **What no model gives.** The war's outcome turned on politics no equation holds: Saigon's legitimacy, Hanoi's
  will, Washington's patience. The models give attrition, logistics, force and the home front's arithmetic; the rest
  is the record's, and in a game, fiction's.

## 5b. Conventional, air and nuclear war

The owner, the same day: "and conventional warfare? aerial warfare? we already have a little sandbox war in the
calendar, in 1967, and we have other little conventional box wars in prospect (DPRK/ROK) or just outside our window
(Lam Son, Easter Offensive, Yom Kippur, Black April), and it would be interesting to model what would happen if
NATO/the US gave up their first-use doctrine altogether".

- **The June war, 1967.** Trevor N. Dupuy, *Elusive Victory: The Arab-Israeli Wars, 1947–1974* (1978): each
  engagement scored (weapons, terrain, posture, surprise) and a combat effectiveness value fitted, how much better a
  side fought than its numbers. A model fitted to his engagements, then asked (Egypt's air force not caught on the
  ground June 5; Jordan out). The same tools for 1973 and, outside the window, Lam Son 719, the Easter Offensive, 1975.
- **Force scoring and theater models.** The Army's Weapon Effectiveness Indices and Weighted Unit Values (WEI/WUV),
  armored division equivalents; Joshua M. Epstein, *The Calculus of Conventional War* (1985); Barry R. Posen,
  *Measuring the European Conventional Balance*, 9 Int'l Sec. 47 (1984–85) (Check: page); John J. Mearsheimer, *Why
  the Soviets Can't Win Quickly in Central Europe*, 7 Int'l Sec. 3 (1982). After the window, but formalizing what
  Systems Analysis argued in it: that NATO could hold without early nuclear use (Enthoven and Smith; FRUS).
- **Numbers against how forces fight.** Stephen Biddle, *Military Power* (2004): the "modern system" of force
  employment, tested against numbers and technology, explains outcomes better than either; a correction to every
  Lanchester-type model, and a variable the record can score (§5c).
- **Korea, 1968.** The balance from the forces tables (the *Military Balance* as the *Statistical Abstract*
  reprinted it), the terrain, the defense of Seoul; the Blue House raid and the Pueblo the occasions.
- **The air war.** Sorties against losses against what the targets were worth: the series holds the attack sorties
  (OSD's reports; CACTA, by route package); losses a sortie wanted. Air-to-air: the Air Force's Red Baron reports
  (DTIC) and the Navy's Ault Report (1968). Coercion: Robert A. Pape, *Bombing to Win* (1996), punishment against
  denial; Mark Clodfelter, *The Limits of Air Power* (1989). June 5, 1967: an attack on sortie generation, a
  well-understood problem.
- **No first use.** The doctrine: MC 14/2, then MC 14/3, flexible response, adopted Jan. 1968; China's declaration of
  Oct. 16, 1964. The conventional side by force scoring and Epstein's or Posen's model (without the nuclear threat,
  does NATO hold, and how many days); the nuclear side the period's own arithmetic, McNamara's assured-destruction
  tables in the posture statements (the forces job queued for Nov. 2 gathers them).
- **Off the shelf.** *Command: Modern Operations* (Matrix Games): a serious air and naval simulator with 1960s
  scenarios and equipment, for exploring, not for scripting into the series. Nothing open at that level found. The
  models above are small enough to write; the work is the data (orders of battle, equipment counts, weights, loss
  rates).

## 5c. Surprise, morale, command and political will

The owner, the same day: "Any suggestions as to how to begin building out the groundwork for a simulation 'surprise,
morale, command, and political will'? There's a reason we have all these intra-administration events and domestic
political data, formal and informal—and why I was disappointed to see the agents discard that, both at home and
abroad. ... There's a lot of political science out there!" The groundwork is the record made structured: what the
informal record holds, laid out so a model can read it. Each layer derived from the calendar (tags on entries, files
beside them), never a second record; each from the literature that has measured it.

- **Political will at home: opinion.** The literature: John E. Mueller, *War, Presidents and Public Opinion* (1973),
  and *Presidential Popularity from Truman to Johnson*, 64 Am. Pol. Sci. Rev. 18 (1970) (the rally, the coalition of
  minorities); John R. Zaller, *The Nature and Origins of Mass Opinion* (1992) (elite cues; Vietnam his case); Adam J.
  Berinsky, *In Time of War* (2009) (partisan cues over casualties); Christopher Gelpi, Peter D. Feaver and Jason
  Reifler, *Paying the Human Costs of War* (2009) (expectations of success); Steven Casey, *Selling the Korean War*
  (2008) and *When Soldiers Fall* (2014) (the administration's selling, the reporting of the dead); Douglas L.
  Kriner and Francis X. Shen, *The Casualty Gap* (2010) (local losses); Daniel C. Hallin, *The "Uncensored War"*
  (1986) (the press, following the elite debate); Benjamin I. Page and Robert Y. Shapiro, *The Rational Public*
  (1992); Nathan P. Kalmoe on partisanship and violence (*With Ballots and Bullets* (2020); with Lilliana Mason,
  *Radical American Partisanship* (2022)). The data: the series' Gallup readings; Gallup's "mistake" question from
  Aug. 1965 (to add, by page, as the approval series is); the Policy Agendas Project's "most important problem" and its
  coding of hearings, laws and the State of the Union (open); the American National Election Studies of 1964 and 1968
  (open); the elite cue itself, the members' dated public word (the parties-and-members rule) and their roll calls.
  Models: Mueller's log of casualties; Zaller's and Berinsky's cue-taking; the expectations of success; each tested
  against the series' own readings.
- **Political will at home: elections and Congress.** Douglas A. Hibbs's "Bread and Peace" (real disposable income
  growth and cumulative military deaths in Korea and Vietnam, the incumbent party's presidential vote; the series holds
  both inputs); Edward R. Tufte, *Determinants of the Outcomes of Midterm Congressional Elections*, 69 Am. Pol. Sci.
  Rev. 812 (1975), and *Political Control of the Economy* (1978); William G. Howell and Jon C. Pevehouse, *While
  Dangers Gather* (2007) and Douglas L. Kriner, *After the Rubicon* (2010) (Congress's constraint on the use of
  force); Richard E. Neustadt, *Presidential Power* (1960), and Samuel Kernell, *Going Public* (1986), for what the
  President's persuasion could and could not do.
- **Command: the decisions inside the administration.** The literature: Graham T. Allison, *Essence of Decision*
  (1971); Morton H. Halperin, *Bureaucratic Politics and Foreign Policy* (1974); Irving L. Janis, *Victims of
  Groupthink* (1972) (the Bay of Pigs; escalation); John P. Burke and Fred I. Greenstein, *How Presidents Test Reality*
  (1989) (Eisenhower, 1954, and Johnson, 1965); Yuen Foong Khong, *Analogies at War* (1992); Leslie H. Gelb with Richard
  K. Betts, *The Irony of Vietnam: The System Worked* (1979); Elizabeth N. Saunders, *Leaders at War* (2011). The
  groundwork: a positions ledger for each decision the calendar follows (Jan.–July 1965; the bombing pauses; Mar.
  1968): each participant's recorded position by date, from the entries and their pages ("by Ball's account"),
  disagreements of account kept as the brief keeps them. Ideal points for the executive, from the informal record:
  what the agents passed over as private is this layer's data.
- **Command: the leaders' beliefs, from their own words.** Operational code analysis (Alexander L. George, *The
  "Operational Code"*, 13 Int'l Stud. Q. 190 (1969); Stephen G. Walker and Mark Schafer on Johnson and his advisers,
  21 Pol. Psychol. (2000), Check: title and page) and Margaret G. Hermann's leadership trait analysis: dictionaries run
  over a leader's spontaneous words. The series holds the corpora: the press conferences in the cleaned Public Papers,
  by date; the cables and memoranda in FRUS. A belief score by month for Kennedy, Johnson, Rusk, McNamara, replicated
  first where the literature has scored them.
- **Surprise: the warning record.** Richard K. Betts, *Surprise Attack* (1982); Roberta Wohlstetter, *Pearl Harbor:
  Warning and Decision* (1962); James J. Wirtz, *The Tet Offensive: Intelligence Failure in War* (1991). For each
  surprise the calendar holds (the Sino-Indian war, the missiles in Cuba, the June war, Tet, Czechoslovakia), the
  indicators and estimates by date, now entries under the ruling on the papers of government: a hidden tag
  (`warning:<event>`) and, from the entries, what was known, by whom, when, and what was estimated.
- **Morale.** The literature: Edward A. Shils and Morris Janowitz on cohesion (1948); Jasen J. Castillo, *Endurance and
  War* (2014); Dan Reiter and Allan C. Stam, *Democracies at War* (2002); Kenneth M. Pollack, *Arabs at War* (2002);
  Caitlin Talmadge, *The Dictator's Army* (2015) (coup-proofing against battlefield effectiveness; North and South
  Vietnam among her cases). The data the series already reads or can: ARVN desertions and the Chieu Hoi ralliers
  (Thayer), U.S. desertion and AWOL rates (DoD), the HES's ratings (§5).
- **Abroad, the same layers.** The decisions of Hanoi, Peking, Moscow, Saigon, now entries under the ruling of Oct. 29
  (the counterparts): their positions ledger, their warning record. Event data for the dyads, day by day: Edward E.
  Azar's Conflict and Peace Data Bank (COPDAB, 1948–78) and Charles McClelland's World Event/Interaction Survey (WEIS,
  from 1966) (Check: where open). The formal frames: Thomas C. Schelling, *Arms and Influence* (1966) and Herman Kahn,
  *On Escalation* (1965), the period's own, Kahn's ladder a game's skeleton; James D. Fearon, *Rationalist
  Explanations for War*, 49 Int'l Org. 379 (1995), and *Domestic Political Audiences and the Escalation of
  International Disputes*, 88 Am. Pol. Sci. Rev. 577 (1994); Bruce Bueno de Mesquita et al., *The Logic of Political
  Survival* (2003).
- **What it asks of the readings, and what it does not.** Every meeting, call, position and estimate, dated and by
  page, the source's words for a position kept: the rulings of Oct. 28 and 29 already ask it. A reading's "Passed
  over" list is this layer's loss. The coding is not the readers' (the owner, Oct. 30, 2026: "I'm not confident that
  *I* grasp the appropriate way to state or operationalize these concepts, much less assign it to agents to code on
  the fly. ... this would be better done in later passes, at least so long as we're not losing the raw material for
  those passes to the cutting-room floor").
- **Recommended.** The positions ledger and the warning record as later passes, each over the entries the readings
  have made, with the concept stated first from the literature (what a position is, what counts as warning), tried on
  one decision (July 1965) and one surprise (Tet), and put to the owner before it runs wider.

## 6. How a simulation is built and shown

- **Precomputed, not run at build.** Each model a script in `tools/sims/` (the network and its libraries there, as
  the other makers), writing its results to `sims/<model>/<key>.yaml`: inputs with their sources, the model and its
  sources, the results with ranges, the backtest's score, the version. The build only renders (CI has pyyaml alone).
- **The hook.** A hidden tag on the calendar entry, `sim:<model>:<key>` (`sim:pivot:civil-rights-1964-cloture`,
  `sim:shock:surcharge-1967-01`, `sim:crossover:1967-q3`), rendered through `contents.put` as a block of its own kind,
  titled in the tables' small capitals and set apart in look (a model's, not the record's): the question, the inputs,
  each model's answer, the range, the backtest. `check` fails on a tag with no results file, a result without its
  inputs' sources, a stale result (its inputs changed since).
- **Tractable, so placed.** A model goes on an entry only where its inputs are all in the series: a bill with its roll
  calls; a tax act with its revenue figure; a rate change; a month with the war table's figures. The rest wait.
- **Backtest first.** No model is placed until it has been run against what happened, and its score shows with it.

## 7. The game, later

Starts from §2 on a date (the first, Chicago, Aug. 26–29, 1968: the conventions data, the roll calls, the delegations
and how chosen; the Democratic Proceedings of 1968 still a lead), a handful of decisions, the consequences from §3–5,
the narration drafted by Claude in an artifact (the account grants pages `sample` and `db`: narration and saved
playthroughs), every branch marked fiction from its point of departure. Nothing from a playthrough enters the series.

## 8. Order

1. §2, the world on a date.
2. §3, the pivots, backtested on `congress/bills.yaml` and the roll calls.
3. §4, the period's own models; then today's estimates.
4. §5, the crossover calculator and the guerrilla Lanchester model on the war table's figures; the home front against
   Gallup. §5c's layers as later passes over the readings' entries (above, "Recommended"), the readings meanwhile
   keeping the raw material.
5. §5b, the June war on Dupuy's engagements; then the Central Front and no first use, with the posture statements.
6. §6's hook, for whatever has passed its backtest.
7. §4's open economy, when its data is built; §7, the game.
