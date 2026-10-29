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
   Gallup.
5. §6's hook, for whatever has passed its backtest.
6. §4's open economy, when its data is built; §7, the game.
