# Fursenko and Naftali: the visibility audit (Nov. 13, 2026)

## 1962–64

The audit of `inbox/2026-11-13-fn-vis-1962.yaml` (76 `tag` ops) and `inbox/2026-11-13-fn-vis-1963.yaml` (20 ops, 1963–64), by `notes/briefs/fursenko-visibility.md`, vis.py STYLE 4, 5, 8, and the spec, §3–4. Every ruled entry read whole (`./bib show`); for 1962, 42 of the 139 unruled rows sampled across the threads; for 1963–64, all 51 unruled rows. Corrected patches: `inbox/2026-11-13-fn-vis-1962-audited.yaml` (65 ops) and `inbox/2026-11-13-fn-vis-1963-audited.yaml` (19 ops), the same `patch:` names; `./bib patch-check`, 0 errors, 0 warnings, each. The readers' files left as they are.

**Counts.** 1962: 76 ruled; 59 upheld, 6 polities corrected, 11 removed; none added (42 unruled sampled). 1963–64: 20 ruled; 18 upheld, 1 corrected, 1 removed; none added (51 unruled read). Every polity id in the audited patches is in `sources/polities.yaml` `polities:`.

**Corrected (a partner added, or one missing).**
- `cal.1962-04-03.cuba`, `ussr+cuba` to `ussr`: Escalante, in exile, reporting to the CPSU's Central Committee; Havana not told.
- `cal.1962-05-11.soviet-union-2`, `ussr+cuba` to `ussr`: the Presidium adopts the letter to Castro; its delivery is a later act.
- `cal.1962-07-06.missile-crisis`, `ussr+cuba` to `ussr`: a Presidium session, the Cubans not present; their urging is background.
- `cal.1962-10-26.missile-crisis-7`, `ussr+cuba` to `ussr`: Pliyev's own reading and measures; the Cubans were his informants, not privy to the dispersal. (The launchers' readiness was also in the CIA's photographic estimates of Oct. 26–27: the US saw the state, not the orders.)
- `cal.1962-10-29.cuba`, `ussr+cuba` to `ussr`: Alekseyev's cable to Moscow, a Soviet report, as the reader ruled the KGB's of the same day (`cal.1962-10-29.cuba-2`).
- `cal.1962-12-25.missile-crisis`, `ussr+cuba` to `ussr`: the last tactical warheads out; the Cubans had been told they were all gone (`cal.1962-11-22.soviet-union`).
- `cal.1964-02.soviet-union-2`, `ussr+italy` to `ussr+italy+uk`: the remark to a foreign visitor; the entry's one record is the British Embassy's dispatch of Mar. 6.

**Removed (no ruling).**
- `cal.1962-03-20.laos`: three events, Souphanouvong to Abramov (Mar. 20), Abramov to Hồ in Hanoi (Mar. 21), the PLA's column from Kunming; each its own partners.
- `cal.1962-03.cuba-2`: two events, one public: the ORI's leadership widened (announced), then the closed-door rebuke of Escalante (Cuban only).
- `cal.1962-03.cuba-4`: two events, Valdés's request in Moscow and Alekseyev's answer in Havana (a request and its reply); each `ussr+cuba` when split.
- `cal.1962-04-27.cuba`: the recall telegram, Alekseyev's request to stay, the instructions changed: request and reply; each `ussr+cuba` (the telegram `ussr`) when split.
- `cal.1962-05-24.missile-crisis`: two events, the Presidium's decision (`ussr`) and Castro's consent at month's end (`ussr+cuba`); the crisis's bibliography hub besides.
- `cal.1962-05-30.missile-crisis`: two events, the Cuban leaders alone (`cuba`: "the Soviets had no report of the talk") and Castro's acceptance to Rashidov, Biryuzov and Alekseyev (`ussr+cuba`).
- `cal.1962-07-07.missile-crisis`: two events, Khrushchev with his military advisers and the Presidium's naming of Pliyev (the protocol of July 6, by `cal.1962-07-06.missile-crisis`); each `ussr`.
- `cal.1962-07.missile-crisis`: three events (Raúl Castro in Moscow; the agreement initialed; Soviet shipping begins), the last seen by the US at the time (FRUS X, doc. 383, its first source).
- `cal.1962-10-10.missile-crisis-2`: two events, Semichastny's proposal (Oct. 10) and the Presidium's decision (Oct. 16); each `ussr`. The entry's own Check asks for the split.
- `cal.1962-10-23.soviet-union`: mixed: the Presidium's orders to the ships private; the alert of the Soviet and Warsaw Pact forces, leaves stopped, announced that day.
- `cal.1962-11-15.missile-crisis-3`: two events, Castro at the battery and with Mikoyan that night; the order to fire public the same day in his letter to U Thant.
- `cal.1963-04-26.cuba`: an open act: the flight secret for a day, the visit announced on arrival at Murmansk and reported by the American Embassy (the entry's WEEKA); "More than a month in the Soviet Union" is the public visit.

**Upheld, with notes.** The Pathet Lao (`cal.1962-01.laos`, `cal.1962-02-03.laos`, `cal.1962-09-28.laos`): `ussr`, `laos` being the Royal Lao state; `cal.1962-03-07.laos`, `ussr+prc+drv`. `cal.1963-07-05.china` (`ussr+prc`): the talks' opening was in the press, their words the two parties' only; by the brief ("talks with the Chinese") and the computed tags already. `cal.1963-11-22.soviet-union-2` (`ussr`): Gromyko to Khrushchev; the channel's "goes unused" a comment, not an act. `cal.1962-11-05.cuba` (`ussr+cuba`): "Moscow to back his five points" may be a later decision; check the page (496).

**The readers' doubts.** +laos for the Pathet Lao: no; `ussr` stands. Cuban-only acts: `vis:only:cuba` is right where an act is the Cubans' alone; none ruled here. The first half of `cal.1962-05-30.missile-crisis`, once split, takes it; `cal.1962-03-20.cuba` (the ORI's vote on Escalante) may, if the vote was not announced before Castro's broadcast; `cal.1962-03.cuba-3` and `cal.1962-10-26.missile-crisis-8` already compute as Cuba's only. Kroll, Sept. 11 (`cal.1962-09-11.berlin-and-vienna`): no ruling; Kroll told the American Embassy and the Canadian Ambassador the same day (F&N, 459).

**Unruled rows.** None should have been ruled. In the 1962 sample, mixed or several events (no ruling; to split): `cal.1962-03.soviet-union` (Gromyko's instruction, and Bolshakov's telling Salinger, Apr. 5), `cal.1962-04-11.cuba` (*Pravda*, and Semichastny's report the same day), `cal.1962-07-05.berlin-and-vienna` (the letter to Kennedy, and Khrushchev to Ulbricht, July 11), `cal.1962-10-25.press-and-broadcasting` (Lippmann's column, and Khrushchev's reading of it), `cal.1962-03.cuba-3` (the leave asked and given; the flight to Moscow). `cal.1962-06-14.soviet-union` left unruled: its `c` is the message as given to Robert Kennedy, the delivery the US's. In 1963–64: `cal.1963-09-30.soviet-union` (Kennedy's proposal through Salinger; Khrushchev's approval), `cal.1963-11.soviet-union` (the book of condolences at the American Embassy; the KGB's search), `cal.1963-11-25.assassination-6` (Havana; Mexico City), `cal.1964-01-05.soviet-union` (Bartlett's talk; its forwarding), `cal.1964-05.middle-east` (the Aswan ceremony; the delegation's private words), `cal.1964-10-12.soviet-union` and `cal.1964-10-13.soviet-union` (the launch, the Presidium, Palewski). Outside the brief: `cal.1964-10.vietnam-hanoi`, a DRV representative to a French official, computes as US and USSR; at the time it was the DRV's, France's and, by Oct. 24, the UK's (`vis:only:drv+fr+uk` would say so); a ruling for the lead.

**For the lead.** `cal.1962-02-08.soviet-union` and `cal.1962-02-08.cuba` are one event, the Presidium's $133 million for Cuba, Feb. 8: a duplicate for `./bib combine`. `souphanouvong` is `polity: laos` in `sources/polities.yaml` ("leader of the Pathet Lao"); from June 23, 1962, he was a Deputy Premier of the coalition, so the person's polity and the ruling disagree: a dated polity for him wants a ruling.

## 1960–61

The audit of `inbox/2026-11-13-fn-vis-1960.yaml` (54 ops) and `inbox/2026-11-13-fn-vis-1961.yaml` (43), Nov. 13, 2026, by the brief (`notes/briefs/fursenko-visibility.md`). Every ruled entry read whole (`./bib show`). The corrected patches: `inbox/2026-11-13-fn-vis-1960-audited.yaml` (50 ops) and `inbox/2026-11-13-fn-vis-1961-audited.yaml` (44); `tag` ops only; `./bib patch-check` 0 errors each. The readers' files left as they were.

### Counts

| | ruled | right | fixed | dropped | added (sample) | audited ops |
|---|---|---|---|---|---|---|
| 1960 | 54 | 49 | 1 | 4 | 0 | 50 |
| 1961 | 43 | 39 | 0 | 4 | 5 | 44 |
| | 97 | 88 | 1 | 8 | 5 | 94 |

Every polity id in the ops is in `sources/polities.yaml` `polities:`.

### Fixes and drops

- `cal.1960-12-07.laos`: `ussr` to `ussr+prc+drv`. The entry records the overflight asked of Peking and Hanoi.
- `cal.1960-07-13.congo-2`: dropped. Kasavubu and Lumumba's cable was an open appeal. Khrushchev answered it in public on July 15 ([[cal.1960-07-15.congo]]). The entry also holds Gromyko's circulation of it, a private act: mixed. Check: the cable in the press of July 15, 1960.
- `cal.1960-10-29.cuba`: dropped, mixed. Castro's talk with Alekseyev is private. "He mobilizes the capital's militia" is an open act.
- `cal.1960-11-23.laos`: dropped, mixed. The talk with Abramov is private. "Before the meeting he tells the press" is public (the *Times*, Nov. 24, cited).
- `cal.1960-12-09.laos`: dropped, mixed. Pholsena's errand to Hanoi is private. Quinim's provisional government in Vientiane, Dec. 12, is public.
- `cal.1961-06-17.soviet-union`: dropped, mixed. The Presidium session is private. The minutes went to foreign Communist leaders and were read by ambassadors in eighteen countries, and the cited copy is in the Bohlen Papers. The death penalty widened in July: published decrees.
- `cal.1961-08-24.berlin-and-vienna`: dropped, mixed. Pervukhin and Konev to Ulbricht is private. On Aug. 25 Ulbricht rescinds the security zone, a published order of Aug. 22 ([[cal.1961-08-22.berlin-and-vienna]]). Two days, two events.
- `cal.1961-09.berlin-and-vienna-2`: dropped. Spaak's visit to Moscow was public. The entry also holds his report to the NATO Council (its own entry, `cal.1961-09.europe-and-the-alliance`; the *Times*, Sept. 25, 1961).
- `cal.1961-10-08.intelligence`: dropped. Bolshakov's source was close to Rostow, perhaps Rostow himself: a channel with an American.

### The sample (40 unruled rows a year, across the threads)

1960: none should have been ruled. All are open events, US records or channels with Americans (Lodge, Thompson, Burden, Robert Kennedy), or mixed.

1961: five should have been ruled, all added:
- `cal.1961-04-08.cuba-bay-of-pigs`, `vis:only:ussr`: the KGB's New York station to the Center. A Soviet intelligence report.
- `cal.1961-08-07.berlin-and-vienna-2`, `vis:only:gdr`: Ulbricht to the East German Politburo.
- `cal.1961-08-11.berlin-and-vienna`, `vis:only:gdr`: Mielke to the security police, "under the strictest secrecy."
- `cal.1961-10-27.berlin-and-vienna-3`, `vis:only:gdr`: Ulbricht, from Moscow, to his colleagues in East Berlin.
- `cal.1961-10-28.berlin-and-vienna`, `vis:only:gdr`: Ulbricht to his colleagues at home.

These answer the 1961 reader's question on GDR-internal acts. Each is an act known only to the East German state, by the East German record (Harrison), with no Soviet official present or told.

### Mixed entries found (no ruling; one event an entry)

Among the ruled: the six dropped as mixed above.

Among the sample:
- `cal.1960-05-17.soviet-union-u2-2`: Khrushchev's cable to the Kremlin is private. The message to the French reached the Western leaders.
- `cal.1960-08-11.congo`: the Presidium's letter to Ghana is private. The Il-14's arrival in the Congo is open.
- `cal.1960-10-13.laos-3`: Abramov's arrival is public. His talk with the Indian Ambassador is private.
- `cal.1960-11-07.cuba-2`: Guevara on the mausoleum is public. The reported probe on missiles is private.
- `cal.1960-12-20.laos`: the departures and flights are open. The Chinese representative to his Soviet colleague is private.
- `cal.1961-04-07.laos`: Moscow's announcement is public. The private asks of Peking, Hanoi and the Pathet Lao are not.
- `cal.1961-07-19.cuba`: the arrests are open. The KGB's plan to run "Tony" is private.
- `cal.1961-08-10.berlin-and-vienna`: Ulbricht's timetable to Khrushchev is private. Konev's return is announced, and he speaks to the Western mission chiefs.

Two ruled entries also carry a second private event, kept:
- `cal.1961-07-26.berlin-and-vienna-2` (`ussr+gdr`): it also has the invitations to the Warsaw Pact meeting, which went to the other members. Hungary, Bulgaria and Albania have no polity.
- `cal.1960-06-16.cuba` (`ussr+cuba`): Núñez Jiménez's word in Moscow "later that week."

### The 1961 reader's questions

- GDR-internal acts: `vis:only:gdr`, the four above.
- Spaak, `cal.1961-07.berlin-and-vienna-2`, `ussr+belgium+poland`: kept. The feelers went to the Poles in Brussels. Moscow had them by July 29 ([[cal.1961-07-29.berlin-and-vienna-2]], `ussr+poland`). The ruling cuts the privity computed now and adds none. Poland, with no tag on the entry, gets no privity from it.
- The Pathet Lao: no polity, and not `laos` (the brief). Where only the Soviets and the Pathet Lao knew (`cal.1961-08-31.laos`), `vis:only:ussr`. Where the Chinese and North Vietnamese were present (`cal.1961-09-22.laos`), `ussr+prc+drv`.

### Doubts, for the lead or the owner

- Powers's questioning (`cal.1960-05-03.soviet-union-u2`, `-05-06`, `-05-10`, `-06-10`, and the capture, `cal.1960-05-01.soviet-union-u2-2`): kept at `vis:only:ussr`. An American was present, but held incommunicado, so the American state did not know. The spec (§4) makes a person present privy for his polity. A ruling is wanted on whether a prisoner counts.
- `cal.1961-11-09.berlin-and-vienna` (Khrushchev to Kroll, `ussr+frg`): kept. Bonn may have told the allies within days. Check FRUS 1961–63, XIV.
- `cal.1960-08-05.congo` (Khrushchev to Lumumba, `ussr+congo`): kept. Lumumba may have published it. Check the press.
- `cal.1961-01-09.laos` (`ussr+poland`): kept. Khrushchev's support for Sihanouk's call for a conference may have been public. If so, the entry is mixed.
- Reports of a partner's words, "Alekseyev to Moscow: Guevara says ..." (`cal.1960-02-07.cuba`, `-02-10`, `cal.1961-05-19.berlin-and-vienna`, others): kept with the partner, as the readers ruled. The partner knew what was said, though not of the report. Ruled in the other direction, these entries would be `ussr` alone.
- The ruling only cuts. A partner named in the ruling but untagged on the entry (Escalante, the PSP, the Polish Ambassador) gets no privity from it. Adding `polity:` tags was outside this pass.
- `cal.1961-06-04.berlin-and-vienna` (Kreisky with Khrushchev) and `cal.1961-11.laos` (Peking with the Pathet Lao): left unruled. They might be `ussr+austria` and `prc`, but whether the US or the Poles (Thee) knew at the time is unsettled.
