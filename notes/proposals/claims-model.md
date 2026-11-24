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
