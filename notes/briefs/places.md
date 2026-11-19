# The location pass: a `place:` for every calendar entry the record places

The owner, Nov. 18, 2026 (about 6:50 p.m. Pacific): "Please do add a place field. Put the location pass in the next
available slot." The field: `notes/guide/entries.md`, "The place". The gazetteer: `sources/places.yaml`
(tools/bib/places.py, its STYLE). This brief is the pass's.

## What a place is

P1. **Where the act was done**: where the actor was when acting. A meeting where it sat; a speech where it was given;
a signature where the pen was; a vote where the body sat; a statement or communiqué where it was issued; a decision
of a court where the court sat; an attack, a battle or an incident where it happened; an arrest where made; a
publication (a newspaper's editorial, a magazine's article) the city it was printed in; a broadcast where it went out
from.

P2. **Two places** where the act joined them: a telephone call (the caller's place first), an exchange of messages
counted as one act (the sender's first), a summit held across a line. `place: [washington, moscow]`. A cable or letter
alone: the sender's place only. A trip: the place the entry's act is done in (an arrival: where he arrived; a
departure: where he left from; "flies from Peking to Hangzhou": `[peking, hangzhou]`, the departure first).

P3. **Only on the record.** The place must be stated or fixed by what the entry holds: its `c`; its note (a Public
Papers title, "Remarks in Seattle"; "Hyannis Port"; a FRUS heading, "Moscow, March 3"; a cable's dateline; a source's
parenthetical, "(at Lushan)"); its tags (`city:`, `state:`, `place:`), read as evidence, not as proof (a city tag can
name the subject, not the scene: "Kennedy, at the White House, on Birmingham" is Washington). Or by **the seat**
(P4). Never from what you know but the entry does not say; never from the thread alone; never a guess. An entry you
cannot place stays without one: no op. A wrong place is worse than none.

P4. **The seat.** An act a body does only where it sits takes the seat, basis `seat`:
- the Congress's floor acts (passage, votes, adoption, confirmation, a bill's introduction, a session convened or
  adjourned) and its committees' hearings and votes: Washington, unless the entry says a field hearing elsewhere;
- the Supreme Court's decisions and orders: Washington;
- the White House, the Oval Office, the Cabinet Room, the State Department, the Pentagon, named in the entry:
  Washington; Camp David: `camp-david`; the LBJ Ranch: `lbj-ranch`; Hyannis Port, Palm Beach, Newport, Key Biscayne,
  San Clemente: themselves;
- a foreign legislature's sitting (the Bundestag: Bonn; the Commons: London; the National Assembly: Paris; the
  Supreme Soviet: Moscow; the NPC: Peking);
- the Presidium of the CPSU Central Committee and the plenums of the Central Committee: Moscow, unless the entry
  says otherwise (Pitsunda, the Crimea);
- the French Council of Ministers: Paris; the Federal Cabinet: Bonn; the British Cabinet: London;
- the DRV's Politburo and National Assembly: Hanoi, unless the entry says otherwise; the RVN's government
  (the Palace, the National Assembly, a Saigon junta's meeting): Saigon;
- NOT the Chinese leadership's meetings (Mao and the Standing Committee met in Peking, Hangzhou, Wuhan, Shanghai,
  Lushan, Beidaihe, on trains): only where the entry names the place, or the note's source does ("at Hangzhou",
  "in the Yinian Tang", "Huairen Tang", "Zhongnanhai", "Diaoyutai", "the Great Hall of the People" are Peking);
- NOT a President's acts in general: a press conference, a signing, a statement, a message have no seat; place them
  where the entry or the Public Papers title says ("The President's News Conference" without a place: Washington
  only if the note's link or text says the State Department auditorium or the White House).
- NOT an election: a State's election (its returns) is the State (`state` places in the gazetteer, `kind: state`);
  a national election has no place (no op).

P5. **A span or a series** (a week's hearings, a run of raids): the place of the entry's acts if one; two at most
(P2); a campaign day across several cities: the first stop and no other (the entry's `c` order), basis `c`.

P6. **Basis**, on each op: `c` (the entry's text names it), `n` (its note does), `tag` (a tag, read with the text, is
the only evidence and the text does not contradict it), `seat` (P4). Give `note:` a few words where the basis is not
plain (`note: 'the PPP title, "Remarks at Fort Worth"'`).

## The gazetteer

G1. A place the gazetteer (`sources/places.yaml`) lacks takes a `place-key` op in your patch, before the ops that use
it: `- place-key: {key: anniston-al, name: 'Anniston, Ala.', zone: America/Chicago, st: AL}`; abroad
`- place-key: {key: hangzhou, ...}` with `in:` the polity key of `sources/polities.yaml` (`prc`, `ussr`, `rvn`,
`drv`, `laos`, `frg` ...). Check the gazetteer first (`grep -n "key: hang" sources/places.yaml`, by name too), and
your own earlier `place-key` ops; never two keys for one place (Peking is `peking`, not `beijing`).

G2. **Keys**: the place's name folded, lowercase, hyphens (`st-augustine`, `ho-chi-minh-trail`); a U.S. town that
shares its name with another: its State's code after (`albany-ga`, `oxford-ms`). **Names** as the calendar writes them
(the house style, `notes/guide/entries.md`, "Places"): Peking, Canton, Saigon, Hanoi, Huế, Đà Nẵng (Vietnamese with
diacritics but for the English names the guide lists); Hangzhou, Wuhan, Beidaihe, Lushan, Tianjin (Pinyin as the
calendar has it); a U.S. city or town under 75,000 at both censuses with its State's Bluebook abbreviation ("Anniston,
Ala."); a military base with its State ("Fort Benning, Ga."). The seeded rows from the Vietnam `place:` tags carry
names without diacritics where the seed had none (`phu-bai` "Phu Bai"): give the right form in a `place-key` op with
the same key and `fix: true`, and it replaces the row's name.

G3. **Zones**: the IANA zone of the place's clock (`zone:`), the series' usage for its own places:
`Asia/Shanghai` for all of China; `Asia/Ho_Chi_Minh` for the RVN (Saigon kept UTC+8 in the span; the zone database
has it); `Asia/Bangkok` for the DRV (Hanoi, UTC+7); `Asia/Vientiane`, `Asia/Phnom_Penh`; `Europe/Moscow` for
Moscow and Leningrad; a U.S. place its State's zone (`sources/daylight-time.yaml`, `states:`, `zones:`; in a State of
two zones, the zone of that county, `zones_split:` gives the line). A ship at sea or an aircraft: no place, unless the
entry names the waters (`gulf-of-tonkin`) or the base.

## The work

W1. Your list: `scratchpad/places-pass/chunkNN.tsv` (columns: id, date, thread, time_zone, place tags, c, the note's
first 500 characters). The full entry, where the 500 characters cut off what you need: `./bib show ID`. Never read
`build/` or a whole list file.

W2. Read every row. Script what helps (find the gazetteer's names in `c` and `n`, the seats' patterns), but judge each
row yourself before an op is written: a name in the text is not always the scene ("Kennedy, in Washington, on
Berlin"; "Moscow's note"; "the Peking line"). A `time_zone` on the row is a hint, not a place: a Washington
time_zone on a Hanoi act is the hour as Washington read it.

W3. Your patch: `inbox/2026-11-19-places-NN.yaml` (`patch: 2026-11-19-places-NN`; `by:`), ops:
```yaml
ops:
- place-key: {key: hangzhou, name: Hangzhou, zone: Asia/Shanghai, in: prc}
- place: {id: cal.1961-01-01.china-leadership, at: peking, basis: c}
- place: {id: cal.1963-07-25.testing, at: [moscow], basis: c}
- place: {id: cal.1962-10-27.cuba, at: [washington, moscow], basis: n, note: 'the message, sent from Moscow; the reply'}
```
Write it in batches (a script that appends is fine), never more than about 40 ops by hand in one call. `./bib
patch-check` your patch to 0 errors. Touch nothing else: not the lists, not `sources/places.yaml` (the merge writes
it from your `place-key` ops), not other patches. Never merge, commit or push.

W4. Report (your last message): rows read; ops by basis (c, n, tag, seat); rows left without a place, and the main
kinds of them (a sentence each); new gazetteer keys; doubts (a row's place disputed by its sources: list them, no op).
Stop at a clean point by 6:30 a.m. Pacific on a weekday (`TZ=America/Los_Angeles date`), saying where you stopped.
