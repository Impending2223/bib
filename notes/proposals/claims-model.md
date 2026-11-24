# The claims data model (design note, handoff 4aw.1 (a))

The owner's spouse, Nov. 22, 2026: "I don't understand this until I see the data model. Claude, what's the data
model?"; "How do you make sure the text of the claim is consistent with respect to the ellipses?" The owner, the same
day: "a clear improvement on what we have." This note is the design: today's model (1), the new one (2), how the page
renders it (3), the migration (4), the risks and the defaults taken (5). No code changes with it.

## 1. Today

A calendar entry's `c` is one string. Everything that speaks of "a claim" speaks of a piece of that string that a
program cuts out again each time it is wanted:

- **Units.** `claims.units(c)` (tools/bib/claims.py, STYLE 1) splits `c` at sentence ends and at semicolons, never
  inside a quotation, parentheses or brackets, and letters the pieces A, B, C ... Z, AA. Nothing in `c` marks them; a
  reader wanting a finer unit writes a semicolon. 58,276 entries, 154,691 units.
- **The claim map, `src`.** Hidden, after `n`. `c:` is `chash(c)`, the first 8 hex digits of the SHA-1 of the string
  the map was made against; `rows` are `'<source> <pin>: <units>'`, units `all`, letters and runs (`A, C-E`), or `?`
  (not yet mapped). A map whose hash no longer matches is stale: `check` flags it, since the letters may have shifted.
  Where there is no `src`, the mechanical map is derived from `n` (STYLE 5) and never stored. 40,874 entries are
  mapped by a reader; 123,129 rows, 19,941 of them `?`.
- **Visibility.** Rulings are entry tags (vis.py, STYLE 8): `vis:only:ussr`, `vis:from:us:1962-02-10`, and a unit's
  own after `@` with its letters (`@A`, `@B-D`, `@A.C`); a unit's ruling wins over the entry's (257 such tags).
  `vis:frame:ussr` (20 entries) marks the first unit's opening words up to a colon ("Alekseyev to Moscow:") as a
  report's frame with polities of its own; `vis.frame_text()` finds it, and the page gives it a span of its own
  (vispage.py, STYLE 2) with the unit's letter.
- **Variants** (R41): `variants: [{unit: A, witness, reads, at}]`, the unit by letter; `check` (witnesses.py) tests
  the letter against `len(units(c))` (1,326 rows).
- **Footnotes** (footnotes.py, STYLE 1–8): runs of units with the same sources close with a mark; the mark sits inside
  the last unit's span, so a hidden unit takes its mark with it (STYLE 6).
- **The page** (vispage.py, STYLE 2) renders the whole `c` once, then renders each unit alone and looks for it, in
  order, in the whole rendering, to wrap it in `<span class="cl" data-u="B" ...>`. Where a unit is not found (a link or
  title that renders whole but not cut), the entry falls back to one span, unmapped.
- **`follows`** (dayorder.py, STYLE 2) names entries, not units: it is untouched by any of this.
- **Patches**: `cite: {id, item, units}` and `src` rows carry letters; `variant: {id, unit, ...}`; an `edit` replaces
  `c` whole against the entry's `base` rev, so two readers adding to different sentences of one entry conflict.

Example, `cal.1960-06-23.soviet-union` (lists/cal/196006.yaml), as stored:

```yaml
  c: Bucharest, morning. The Soviet delegation hands Peng Zhen's delegation the CPSU Central Committee's letter,
     dated June 21, in seven parts (the era; war and peace; ...; unity). The same text had gone to the other
     parties as a "notification" on June 21, before the Chinese had it, by the Vietnamese, Korean and Albanian
     delegations' word. A draft communique follows, for discussion on the 24th. The delegation cables the points.
  src:
    c: ec205ebb
    rows:
      - 'w.lengxi-shinian-lunzhan-1956-1966 281–283, 285: all'
      - 'w.yang-jisheng-mubei II, 1150: B'
      - 'w.westad-introduction 25: ?'
      - 'w.brothers-in-arms 381: ?'
      - 'via x.1963-07-05.records-cpsu-ccp-delegations: ?'
      - 'w.peng-zhen-nianpu-1902 IV, 37–38: ?'
  tags: [polity:prc, name:peng-zhen, vis:only:prc+ussr,
         vis:only:prc+ussr+albania+bulgaria+czechoslovakia+gdr+hungary+poland+romania+dprk+drv+mongolia@C-D,
         vis:only:prc@E]
  variants:
    - unit: A
      witness: w.peng-zhen-nianpu-1902
      reads: the letter and the "Notification" handed to the delegation at its lodging by Andropov, ... at 3 p.m.
             on June 23 ("下午三时")
      at: IV, 37
```

(`c` and `reads` wrapped here for the page; one line each in the file.) The splitter gives A "Bucharest, morning.",
B "The Soviet delegation hands ...", C "The same text had gone ...", D "A draft communique follows ...", E "The
delegation cables the points." Four structures (the map's rows, two `@` tags, the variant) point at these five pieces
by position. None of them holds the text it means; each trusts that the splitter, run again, cuts the same way. If a
reader inserts a sentence after A, every letter after it now names the wrong sentence, and only the hash notices, and
only for the map: the `@C-D` tag and a variant's `unit:` would silently move to the neighbouring sentence.

A frame, `cal.1960-02-10.cuba` (lists/cal/196002.yaml): `c` is "Alekseyev to Moscow: Guevara, at his home, ... says
Cuba will ask Mikoyan for an enormous credit, $500 million the opening bid (...); the Kremlin may announce it. "It is
very important for Cuba to feel independent of the U.S. and to demonstrate it." Shown to Mikoyan." Units: A (the frame
and Guevara's request), B "the Kremlin may announce it.", C the quotation, D "Shown to Mikoyan."; tags `vis:frame:ussr`,
`vis:only:ussr+cuba`, `vis:only:ussr@D`. B and C are Guevara's words as Alekseyev reported them, but nothing records
it: "Alekseyev to Moscow:" belongs to A alone, and B read alone ("the Kremlin may announce it") has lost both its
reporter and its speaker. That is the ellipsis the spouse asked about.

What is wrong, in one line: the claims are the data's real atoms (sources, visibility and variants all attach to them)
but they are not stored; they are recomputed from prose, and everything else holds positions into the recomputation.

## 2. The model

A calendar entry's `c` becomes a list. Each item is a claim or a frame:

- **claim** `{id, t, src?, variants?}`. `id` is `k1`, `k2` ...: permanent, unique within the entry, never renamed or
  reused (a claim struck leaves its id in the entry's `retired: [k4]`, as an entry's id leaves an alias); its full
  address is `<entry id>#k3`. `t` is its text, one unit by today's splitter (a sentence, a clause closed by a
  semicolon, or a quotation whole), with its own closing punctuation and no space at either end. `src` is the list of
  sources that ground it, each a map row less its units: `'w.yang-jisheng-mubei II, 1150'`, `'via x.…'`, a link's
  address, an unlinked item's first words. `variants` are R41's rows less `unit:`: `{witness, reads, at}`.
- **frame** `{frame, id, src?, claims}`: an element that the claims inside it share and do not repeat (the reporter,
  the speaker, a place-and-time head). `frame` is its text ("Alekseyev to Moscow:", "Rusk:", or a frame with no colon,
  "Guevara, at his home, ..., says"); `id` is from the same `k` sequence, since a frame is itself a claim (that
  Alekseyev reported, that Rusk spoke) with sources and a visibility of its own; `claims` is its list, claims or
  frames (frames nest).

What else changes on the entry:

- `src` (the map) goes. Its rows move onto the claims they name; `all` puts the row on every claim. The `?` rows,
  which a reader has not yet tied to any claim, stay on the entry as `src_open: [...]`, and the footnotes treat them as
  now (the last footnote). The hash `src.c` goes too: an id cannot drift onto a neighbouring claim, so there is
  nothing to go stale. A claim's rev, for a patch's `base`, is `chash(t)`, computed, never stored.
- `variants` go onto their claims.
- Visibility rulings stay entry tags; the part after `@` lists ids joined by "." (`@k3.k4`). Runs (`-`) go: ids are in
  order only when first numbered. `vis:frame:ussr` becomes the frame's own ruling, `vis:only:ussr@k1` (if the vis
  golden shows the two compute the same tags; else `vis:frame:` stays and means "the frame's ruling").
- Nothing else: `n`, `tags`, `when`, `follows` (entries, not claims), the time and place fields stand.
- The letters stay for reading only: `./bib claims show` prints A, B, C beside the ids, in order, as a label; nothing
  stores a letter.
- Only calendar entries (dated and undated) take the list. Every other list's `c` (a work's citation, a person's
  line) and the threads' statements stay strings.

The example entry, `cal.1960-06-23.soviet-union`, in full (only `c`, `src`, `tags` and `variants` differ from the
stored entry; `n`, `when`, the times and place stand as they are):

```yaml
- id: cal.1960-06-23.soviet-union
  when: June 23
  date: '1960-06-23'
  place: bucharest
  thread: soviet-union
  also: [china-leadership]
  c:
    - id: k1
      t: Bucharest, morning.
      src: ['w.lengxi-shinian-lunzhan-1956-1966 281–283, 285']
      variants:
        - witness: w.peng-zhen-nianpu-1902
          reads: the letter and the "Notification" handed to the delegation at its lodging by Andropov, head of the CPSU Central Committee's liaison department, at 3 p.m. on June 23 ("下午三时")
          at: IV, 37
    - id: k2
      t: The Soviet delegation hands Peng Zhen's delegation the CPSU Central Committee's letter, dated June 21, in seven parts (the era; war and peace; peaceful coexistence; forms of transition; international mass organizations; China's breaches of the Declarations; unity).
      src: ['w.lengxi-shinian-lunzhan-1956-1966 281–283, 285', 'w.yang-jisheng-mubei II, 1150']
    - id: k3
      t: The same text had gone to the other parties as a "notification" on June 21, before the Chinese had it, by the Vietnamese, Korean and Albanian delegations' word.
      src: ['w.lengxi-shinian-lunzhan-1956-1966 281–283, 285']
    - id: k4
      t: A draft communique follows, for discussion on the 24th.
      src: ['w.lengxi-shinian-lunzhan-1956-1966 281–283, 285']
    - id: k5
      t: The delegation cables the points.
      src: ['w.lengxi-shinian-lunzhan-1956-1966 281–283, 285']
  src_open:
    - 'w.westad-introduction 25'
    - 'w.brothers-in-arms 381'
    - 'via x.1963-07-05.records-cpsu-ccp-delegations'
    - 'w.peng-zhen-nianpu-1902 IV, 37–38'
  n: '(as now)'
  tags: [polity:prc, name:peng-zhen, vis:only:prc+ussr, vis:only:prc+ussr+albania+bulgaria+czechoslovakia+gdr+hungary+poland+romania+dprk+drv+mongolia@k3.k4, vis:only:prc@k5]
  time_range: ['1960-06-23T04:00Z', '1960-06-23T10:00Z']
  time_band: morning
  time_zone: Europe/Bucharest
```

The frame example, `cal.1960-02-10.cuba`, as the converter would write it (section 4: the frame over what surely
leans on it; "Shown to Mikoyan." is about the cable, not Guevara's words, and stays outside):

```yaml
  c:
    - frame: 'Alekseyev to Moscow:'
      id: k1
      src: ['w.fursenko-one-hell-of-a 38', 'via w.fursenko-one-hell-of-a 38 n.17']
      claims:
        - id: k2
          t: Guevara, at his home, a few days after Castro's dinner of Feb. 3, says Cuba will ask Mikoyan for an enormous credit, $500 million the opening bid (Castro and Alekseyev had spoken of $100 million in November);
          src: ['w.fursenko-one-hell-of-a 38', 'via w.fursenko-one-hell-of-a 38 n.17']
        - id: k3
          t: the Kremlin may announce it.
          src: ['w.fursenko-one-hell-of-a 38', 'via w.fursenko-one-hell-of-a 38 n.17']
        - id: k4
          t: '"It is very important for Cuba to feel independent of the U.S. and to demonstrate it."'
          src: ['w.fursenko-one-hell-of-a 38', 'via w.fursenko-one-hell-of-a 38 n.17']
    - id: k5
      t: Shown to Mikoyan.
      src: ['w.fursenko-one-hell-of-a 38', 'via w.fursenko-one-hell-of-a 38 n.17']
  tags: [name:guevara-ernesto, name:castro-fidel, name:mikoyan-anastas, vis:only:ussr+cuba, vis:only:ussr@k1, vis:only:ussr@k5]
```

(k4's place, inside the frame, is the converter's flag for a reader: it is a new sentence after the frame's first
one; section 4.) A reader can then make Guevara's speech a frame of its own, nested, so that k3 and k4 keep their
speaker, without changing a character of the page (the new frame takes the next free id, k6; no id moves):

```yaml
    - frame: 'Alekseyev to Moscow:'
      id: k1
      claims:
        - frame: Guevara, at his home, a few days after Castro's dinner of Feb. 3, says
          id: k6
          claims:
            - {id: k2, t: 'Cuba will ask Mikoyan for an enormous credit, $500 million the opening bid (Castro and Alekseyev had spoken of $100 million in November);'}
            - {id: k3, t: 'the Kremlin may announce it.'}
            - {id: k4, t: '"It is very important for Cuba to feel independent of the U.S. and to demonstrate it."'}
```

(`src` left out of the last block for space.) k2 keeps its id though its `t` lost the words now in k6: the claim,
Guevara's request, is the same claim (R22: rewording that leaves each claim's substance and sources unchanged is not a
change).

## 3. Rendering, and the consistency rule

**The line.** `text(e)` joins the list: siblings with one space; a frame as its `frame`, a space, then its claims
joined. Since every `t` carries its own punctuation, nothing else is added. The converter's invariant (section 4) is
that `text(e)` equals today's `c` byte for byte, so the page renders `text(e)` exactly as it renders `c` now: the
same renderer, links, titles, curled quotes, characters (cjk.py), first cites (works.py). Every tool that reads `c` as
prose today (find, the Names' Life paragraphs, threads, the EPUB, the feeds, the daybook) reads `text(e)` (one
accessor, `store.ctext(e)`, for the 110 places in 30 modules that now read `e["c"]`).

**The spans** (vispage.py, STYLE 2, unchanged in method): each claim's `t` and each frame's `frame` rendered alone and
found in order in the whole line, a span each, `data-u` its id (`k3`) for today's letter; the spaces outside the
spans; a frame's span ahead of its first claim's, not around its claims, so the spans stay flat and the CSS and
script stand. The fallback (one span, unmapped, where a piece rendered alone is not found) stays for the rare `t` that
renders differently cut; the converter counts them.

**The footnote marks** (footnotes.py, STYLE 1): items in the order of the line, frames counted as items; a run of
consecutive items with the same `src` closes with a mark inside the last claim's span (STYLE 6: a hidden claim takes
its mark). A frame with no `src` of its own joins its first claim's run, as today, where frame and first claim are one
unit. `src_open` goes to the last footnote, as `?` rows do now. Footnote text, *id*., first cites, STYLE 3–10:
unchanged; they read sources, not letters.

**Visibility.** A claim shows in full, greyed or hidden by its tags as now. A frame shows when any claim inside it
shows (in full if any does, greyed if the best is greyed), and is hidden when all of them are; a frame with a ruling of
its own (Alekseyev's report, `vis:only:ussr@k1`) is cut further by that ruling, as `vis:frame` cuts today.

**The consistency rule** (the spouse: "How do you make sure the text of the claim is consistent with respect to the
ellipses?"). A claim's *reading* is the texts of the frames that hold it, outermost first, then its `t`:
"Alekseyev to Moscow: Guevara, ..., says the Kremlin may announce it." The rule: every claim's reading is a whole
statement, and the readings together are the line. Four things keep it:

1. *The elided element is stored once.* "Rusk:" is in the frame, not repeated or implied in each claim; the reading
   is computed, never typed. Two claims cannot disagree about who spoke, and changing the frame changes every reading
   under it at once (an `edit-claim` on the frame: R22 for the frame's claim, section 4).
2. *The cut is the splitter's.* `check` splits `text(e)` with today's splitter and requires exactly the stored
   pieces: each claim one unit, a frame's text at the head of its first claim's unit. No claim straddles a sentence or
   semicolon; none is a fragment the splitter would not make. A reader who wants a finer claim still writes a
   semicolon, now as two claims.
3. *Leaning is declared, not guessed.* A claim that begins in lower case continues a sentence: it must follow a claim
   ending ";" (else an error). If its sentence's head is a frame, the frame holds it; if not (the head is an earlier
   claim's subject or verb, "Guevara ... says Cuba will ...; the Kremlin may announce it"), `check` warns
   `[claim-lean]` until a reader either makes the head a frame (section 2's nested example) or tags the entry
   `ok:claim-lean`. A capitalized sentence inside a frame is the reader's statement that it is the frame's; the
   converter puts none there unflagged (section 4).
4. *Shown alone, a claim shows its reading.* Wherever a claim is printed outside the line (`./bib claims show`, a
   patch's `edit-claim` preview, an audit's row, a variant's head in a footnote), it is printed as its reading; one
   still leaning on an earlier claim (warned under 3) is printed with a leading ellipsis, "… the Kremlin may announce
   it.", so the elision is marked, never silently dropped.

On the page itself nothing changes: with every claim shown the line is today's line. With some hidden, the visible
ones read through their frames, which stay while any claim of theirs is shown. What the page does not do yet: when the
claims after a ";" are hidden, the visible one still ends ";" (as now). Mending that ("." in its place) is a script
change on the page; left out (section 5).
