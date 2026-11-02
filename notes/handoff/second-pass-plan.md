# Second pass (the owner approved Oct. 28, 2026: "run it in that order"); 4-5 agents at a time
Briefs: brief-common.md, brief-books.md (rules A cited-records with the ABCD claim; B "Passed over"), CLAUDE.md "What the works rest on".
1. Spot-check (running from Oct. 28; notes/spot-check-2026-10-28.md, inbox/2026-10-28-spot-check.yaml). Then merge.
2. Duplicates (similarity sweep across threads, entries added since Oct. 23) and the ~80 logged disagreements settled
   against a third record. After Gibbons and the spot-check merge.
3. Official histories, gap reading (step 3 of brief-books + rules A, B + the informal record): ~4 agents: OSD (Watson IV,
   Kaplan et al. V, Drea VI); JCS (Poole 8, 9; JCS and the War in Vietnam pts. 1-3); Air Force (Futrell, Van Staaveren x2,
   Schlight, Anthony and Sexton); Navy (Marolda and Fitzgerald II). The Oct. 23 run was pinpoints only (315 edits, 0 adds).
4. Primary records for entries resting on a book alone (audit-cal; cited-records `found`).
5. Second reading: Schlesinger RFK, Dittmer, Miller (and Frankum, Victory in Vietnam: support parentheticals), with A and B;
   also retro-fill A and B for the Oct. 24 books.
6. Thread statements (china, soviet-union, Baker, poverty, press, ...).
Parallel: district PVI agent (running from Oct. 28). PR+merge once Gibbons merged (owner's earlier instruction).
Oct. 28: stage 1 merged (68 edits). Finding: the official-histories run of Oct. 23 fails ~46% of its 494 pinpoints
(17% seriously): stage 3 must recheck every one of its pinpoints, not only read for gaps. Also recheck Gibbons-run cites to
other works (39), and parentheticals for Dittmer, Frankum, Victory, Johns, Anthony.
Stage 2 running from Oct. 28: duplicates (inbox/2026-10-28-duplicates.yaml) and disagreements (inbox/2026-10-28-disagreements.yaml).
Claim maps built (tools/bib/claims.py); briefs write `src`. Gallery artifact: https://claude.ai/artifact/8da6JMvh2SXn5g7F1hHnsH
Owner ruling Oct. 28: one event, one entry with also: (CLAUDE.md). After the disagreements merge: fold the duplicates agent's 4 ASK pairs and the older 45 (37 on one PPP item, 8 on one FRUS doc; list in notes/duplicates-2026-10-28.md / scratchpad/dups/) by an agent, reading each.
Oct. 28: PVI committed (31d4258). Folds merged (ea62bfc): 18 events folded, 4 split out, 24 kept. Stage 3 launched: 4 agents,
osd-a (Watson IV, Kaplan V), osd-b (Drea VI), jcs (Poole 8-9, Schulimson/Cosmas), af-navy; patches inbox/2026-10-29-histories-<part>.yaml.
Oct. 29: stage 3 merged (af-navy, osd-b, osd-a, jcs; 497 pinpoints, 846 records, 31 entries; leads in notes/leads.md).
PVI shown (owner: "Show both. Be sure to cite and attribute"). Build speed fixed (thread memo, YAML cache): full build 6 min.
Stage 4 launched: 5 agents by years (1960-62, 1963-64, 1965-66, 1967, 1968-69), brief-primary.md; patches
inbox/2026-10-29-primary-<part>.yaml; notes/primary-records/<part>.md. Merge in order, rebasing overlaps (none expected: years apart).
Oct. 29: stage 4 merged (5 patches; audit 1,132 -> 1,035 none, 118 -> 85 named-not-linked; build clean, 0 missing anchors).
Stage 5 wave 1 launched (brief-backfill.md): schlesinger-rfk (full reread), dittmer-miller (full reread), frankum-victory-johns,
thousand-days-vantage, caro-dallek; patches inbox/2026-10-29-backfill-<part>.yaml. Wave 2 after: garrow-perlstein,
stein-zelizer-schwartz, chen-asselin-nguyen, gibbons (I-IV). Then stage 6 (thread statements).
Oct. 29: owner's rule "The parties and the members" (CLAUDE.md); threads republican-party (+ -congress), democratic-party,
conservative-movement (dd2d76f). Agent republicans-perlstein-johns launched. Queue (after wave 1): Hess and Broder, The
Republican Establishment (Drive 1irnV_Id8SqRP-JSXe1U1TkRGmDnYIL7t); Nixon, RN (1cSYO3uxBPW3hJnQlueDMCJn6m_LXjVij), 1961-68;
Young, Two Suns of the Southwest (1kHiV9VyIYNv836xZHo8ZmDd4bDSaVp3H); Kallina, Kennedy v. Nixon (1gOKSo-mP-2XQZ2FU9W9kw5IGd1JVOOAR).
Then stage 5 wave 2 (garrow-perlstein done; stein-zelizer-schwartz, chen-asselin-nguyen, gibbons) and stage 6.

Oct. 29: Kallina merged (dc271e3); Toledano card fixed (01ad9eb). 4 unused cards (blough, chayes, gage, krock) are
running agents' cards, written ahead of their patches: recheck after merges. Gibbons split: gibbons-1 (Parts I-III;
II and III from the committee prints on archive.org, micro_IA41152619_0216 and micro_IA41152832_0038) running;
Part IV (507 cites, Drive 1vfwUsNGNI0sUaZ3gJDdFGGp36U9mUWdn) to go in two halves (July 1965-1966, 1967-Jan. 1968)
as slots free.

Oct. 29, later: merged Chen/Asselin/Nguyen, Garrow, Schlesinger RFK minor, Stein/Zelizer/Schwartz, Gibbons 4b, Gibbons 1
(last e465ed8). Gibbons 4a (1965-66) running. Owner moved 15 books into the shared folder. Running: Nixon RN
(book-nixon-rn), Hess-Broder + Young rest (republicans-finish), Logevall + Barrett (book-logevall-barrett), Reeves +
Selverstone (book-reeves-selverstone). Queue as slots free: Herring LBJ and Vietnam (1Yi6bz-0NYZ94J3bZPTSiQlN36VJRjc39)
+ Mann Grand Delusion (1eo_ZqbCFBEtv-Y9p94cPhkJJTitEa1s7) + Moyar Triumph Forsaken (16B_NV3kZyxl-D-XI8_KwcXX06pIKz4tI);
Gifford Center Cannot Hold (1MNuABSuml4ne3RlmYmr7p3YukbJ6mpzV) + Palermo In His Own Right (19n4_YUkEXuN9ONzfLaIoIn5CsIZGeUcz,
no card) + Longley LBJ's 1968 (19e_DwLLfXB-sl7MXdTVA8JbDGmb3sBIu, no card); Gavin Gold Dollars and Power
(1jdQbb3GuIyM7X4CjdR-NZcjsM3fcceai) + Zhai China and the Vietnam Wars (1kLDlW8PnT5w1cL-FnOSXCQcX_VXd0DTD). Then stage 6.

Oct. 28, 5:08 p.m. Pacific: resumed after the owner's pause (standing rule: weekdays 7-5 Pacific, "Queued." in between).
Owner: agent ceiling 4x the old 4-5 (about 20). Running (13): Gibbons 4a, Nixon RN, Hess-Broder+Young rest,
Logevall+Barrett, Reeves+Selverstone, and one book each: Herring, Mann, Moyar, Gifford, Palermo (new card), Longley
LBJ's 1968 (new card), Gavin, Zhai (patches inbox/2026-10-29-book-<short>.yaml; brief-onebook.md). Then stage 6.

Oct. 28, 7:45 p.m. Pacific: all book readings merged but Mann's second patch (book-mann-2, the dated leads, running).
Stage 6 started: eight agents rewrite the 121 threads' statements (brief-threads.md; patches
inbox/2026-10-29-threads-1..8.yaml; groups in thread-counts.txt order, vietnam alone in 1). Then: full build, links,
audit-cal; report to the owner.

Oct. 28, 10:30 p.m. Pacific: PR #138 merged (b23c118). Batch 3: the owner added ~73 books and ~61 documents to the
folder (batch3/files.tsv). brief-batch3.md. Running (20): staff (McPherson, Califano), state (Rusk, Ball), defense
(Clifford, McNamara), kennedy (Sorensen, RFK Own Words, Guthman), humphrey (memoir, Solberg), 1960 (Six Crises, White
1960), 1964 (Suite 3505, Novak, White 1964), 1968 (Chester, White 1968), westy (Westmoreland, Berman), soviet (Fursenko
x2, Dobrynin), cuba (Jones, Bissell, Paterson), branch1 (PTW), branch2 (POF), branch3 (ACE), civilrights-hill (Walls of
Jericho, Kotz), rfk (Navasky, Shesol, Thomas), gop (Kabaservice, Goldberg, Smith), advisers (Preston, Bird, Woods),
greatsociety (Sundquist, Zelizer, Bernstein), macv (Command Histories 1964, 65, 67, 68).
QUEUE as slots free: Freedman + Kaiser; Graham + Brauer + Lawson; Carson + Payne + Fairclough x2; Carter + Lesher;
Cannon + Cannato; Abramson; Meltzer + Bremner + Morgan + Zeiler; Powe + Schwartz; Dixon + Ansolabehere + Smith
(doorstep); Gelfand + Flamm + Callcott; Rabe x2; Spiegel + Bass; P: Bulletin v59 (daybook extension); SFRC exec v15-18;
Current Documents 1962-67; hearings (prayer, term, inability, Fortas, migratory labor, poverty Jackson) +
nomination-election-1968 + Rights in Conflict; forces docs (posture fy63-69, WMEAT, NHHC ship force levels, CMH
Maneuver and Firepower, DoD stockpile); FBI files (liuzzo 2-14, mlk1a/1b).
Rule: PR and merge what we have when finished (owner, Oct. 28 night); before the 6:46 a.m. pause, PR+merge what is merged.
Deploy check of #138 scheduled 05:15Z.

Oct. 28, 10:40 p.m.: owner's rulings: (1) other cities' riots into Civil disorders: done (cd6fd4d; Harlem subthread).
(2) Support kept together. (3) Gibbons: enter staff papers, WH memoranda, cables, intelligence memoranda; pass over
covering notes, drafts, preparations, repetitions, private remarks. CLAUDE.md "The papers of government"; brief-batch3
rule 5; all 20 agents messaged. QUEUE FIRST: the Gibbons-ruling agent (prompt as sent Oct. 28 10:35 p.m.: all Passed-over
tables of notes/book-checks/gibbons-u-s-government-and.md; Part IV Drive 1vfwUsNGNI0sUaZ3gJDdFGGp36U9mUWdn, Part I
1vTC5l1BWVhyrEQYv_xmSi8SDy-35wl1o, II/III archive.org; patches b3-gibbons-ruling-1/-2). Hard limit: 20 subagents.

Oct. 28, 10:53 p.m.: container restarted; all 20 batch-3 agents resumed by SendMessage (files on disk survived). Queue unchanged (Gibbons ruling first).

## Queued (Oct. 29, 12 a.m.): sweep of the earlier readings' Passed over lists under the ruling of Oct. 28, late
The owner: "Please do." Every notes/book-checks/*.md not of batch 3: re-rule each "Passed over" row (undated-to-the-day,
itinerary, private, below the level), enter what the rule calls for, patches inbox/2026-10-29-sweep-<card>.yaml.
Groups by size, as slots free. Pending the owner's word on "out of the brief" (Hanoi's and Peking's decisions).

## Added Oct. 29-30 (the owner: "Please do"), for Nov. 2 on
- The readers' brief: rule 5b, keep the raw material (the source's words for a position, with its page; time and
  sequence, `time`/`time_approx`/`follows` once built; every figure with its page). CLAUDE.md the same. Send to the
  resumed agents with the Oct. 29 ruling.
- Event passes beside the book passes: one decision at a time (July 1965; the bombing halt of Oct. 31, 1968), every
  work and record the series holds on it read together, the accounts reconciled, the disagreements kept ("Check:
  Sorensen gives ...").
- Passes over material already held, which the rulings make entries: FRUS month by month (the papers of government:
  staff papers, cables, intelligence memoranda and estimates, from the daybook and sources/frus-text); the Daily
  Digest's witnesses who are officers of unions, lobbies and associations (the ruling of Oct. 29); the Sunday
  programs' guests (their dated public word: an entry where a transcript or a report gives its content); Gallup's
  "mistake" question (Aug. 1965 on), read by page from the volumes already read for approval.
- The overlooked materials: the access survey of Oct. 29-30 (scratchpad/sources-survey/, its artifact), priorities
  there; the owner's Drive additions first.
