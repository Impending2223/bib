# Witnesses: the tree of what each claim rests on

The owner, Oct. 30, 2026, on the records the readers log (CLAUDE.md, "What the works rest on"): "What I ultimately
want from the 'records' is a trace/map of *all* the *ultimate*, or *root*, materials that bear on a fact or event";
agents to "continue to find and register materials ... even after a fact or event is 'sufficiently' attested, even if
the new material 'merely' confirms the existing entry statements—that is, unless the new material is, in all its
contents, strictly inferior to the existing as a matter of the 'ultimate,' or 'root'"; "'Ultimate' or 'root' here
means 'from which no material is upstream'", which "really means 'from which no *identifiable and recoverable*
material is upstream'"; "the kinds of manuscript/editio trees you see in textual criticism ... But with a recognition
that here, in history, unlike philology, the ultimate 'ultimate,' the root 'root,' is the event, not the document";
"we'll often have multiple items 'from which no material is upstream'"; the readers have been "too restrictive in
their definition of 'record' ..., too inhibited in their enumeration of multiple ultimate/root items for a fact or
event, and too unwilling to name the 'upstream' source that could be followed further"; "credit the matter that has a
strictly superior claim to being upstream." On the copies, the same day: "Don't drop the first rule" (§3, rule 1: a
copy is kept as an edge, not dropped).

Nothing here is built. The citations in §1 are recalled, not read: Check.

## 0. What went wrong

Three rules of `tools/bib/cited_records.py` (Oct. 28), not the owner's brief:

- Works were not records. STYLE 1 took "only what the work's own note gives", and the readers read that as documents
  only: Chen's file says so in its header ("Published studies, memoirs and Chinese military histories the notes cite
  ... are works, not records, and are not listed"). A study, a memoir or a documentary collection the note cites fell
  out, and with it the branch behind it.
- One step back. A record was described as the note gives it and the trace stopped there: nothing asked whether the
  series holds the record's own source, or for the source to be named where it does not.
- Enough was enough. Nothing asked a reader to go on registering once an entry was grounded, and "already in under
  another id" in a Passed over list sent a second account of an event out of the map.

The claim maps (`src`, `via`) are sound and stay: they tie units of `c` to items of `n`. What changes is what a `via`
row points at.

## 1. Names for the thing (recalled; Check)

- Textual criticism: the *stemma* (Lachmann), a tree of *witnesses*, each tied to the exemplar it was copied from; the
  *codex descriptus*, a witness copied from one that survives, and its *eliminatio*, the owner's "strictly inferior";
  *contamination*, a witness drawing on two branches; Pasquali, *Storia della tradizione e critica del testo* (1934),
  *recentiores non deteriores*: a later witness is not therefore a worse one.
- Historical method: *Quellenforschung*, the tracing of a chronicler's sources; Droysen's and Bernheim's
  *Überreste* (what an act left behind: the tape, the ledger, the cable) against *Tradition* (accounts made to
  inform: the memoir, the history); Bloch, *Apologie pour l'histoire*, the unintentional and the intentional witness;
  Langlois and Seignobos, *Introduction aux études historiques* (1898): the agreement of witnesses who depend on one
  another is one testimony.
- Genealogy, the nearest working model: Elizabeth Shown Mills, *Evidence Explained*, and the Genealogical Proof
  Standard. Three layers kept apart: the *source* (original, derivative, authored work), the *information* it gives
  for a claim (primary: from one with firsthand knowledge; secondary; undetermined), and the *evidence*, relative to a
  question (direct, indirect, negative). The Standard asks a "reasonably exhaustive search": attestation does not end
  the search.
- Law: hearsay within hearsay (each layer its own footing; Fed. R. Evid. 805); the original-document rule (1002);
  personal knowledge (602); chain of custody. The owner's relativity of title: the better claim to be upstream wins.
- Intelligence: *circular reporting*, several reports from one sub-source taken for corroboration; a source's
  reliability graded apart from its information's credibility.
- Data: the W3C's PROV-O (`prov:wasDerivedFrom`, `prov:hadPrimarySource`, `prov:wasQuotedFrom`,
  `prov:wasRevisionOf`); CIDOC CRM, with the event at the center and documents that document it (`P70 documents`). The
  series' terms below map onto PROV's, so an export is a translation.

## 2. The terms

- **Witness.** Anything that bears on a claim of the calendar: a document (a memorandum, a cable, minutes, a letter, a
  diary), a recording, a transcript, a print, edition or translation of any of them, a statement, a press account, a
  hearing, a study, a memoir, an oral history, an interview, a person's testimony. A work in the catalogue is a
  witness (its card); so is a documentary collection (FRUS, JMZW, *Current Documents*), as the print of what it
  prints.
- **Edge.** A witness derives from another: `copy` (a carbon, a file copy, a facsimile), `print` (a documentary
  collection's or a newspaper's text of it), `edition` (a later printing, a corrected edition), `transcription` (a
  tape's transcript), `translation`, `quotation` (a passage quoted), `citation` (a work's note pointing to it; the
  work's text resting on it), `recollection` (a memoir, an oral history, an interview, from its author's memory of
  the event), `report` (one who heard of it from another: "Bundy told me that Johnson ...").
- **Root.** A witness with nothing identifiable and recoverable upstream of it, for the claim. Several roots for one
  claim are the ordinary case: an event leaves several traces at once (the tape, the memorandum of conversation, the
  Diary's line, two participants' notes), and a trace lost or not found leaves the witnesses below it as roots for
  now. Above all the roots, notionally, the event; it is not a node.
- **Open upstream.** A witness whose source is named (or is plain: a memoir quoting a letter) and not recovered: a
  closed archive, a book the series does not hold, a file not found. It ends its branch for now and is a lead.
- **Agent.** Whose account a witness is: the writer, the speaker, the recorded. A participant's memory is the root of
  his accounts; his diary, his letter of the next week, his oral history and his memoir are witnesses of one agent,
  never independent of one another.
- **Independence.** Counted by distinct roots and distinct agents, never by works. Two studies citing one memorandum
  are one root; the tape and the memorandum of the same meeting, two roots of one event; Sorensen's memoir and
  Sorensen's oral history, one agent.

The tree is drawn for a claim, a lettered unit of `c` (CLAUDE.md, "Claims and their sources"), not for an entry: a
memorandum may ground the date and not the decision. An event's map is the union of its units' trees.

## 2a. The record that is the act

The owner, Oct. 30, 2026: "Where we have the record, and the record is sufficient and complete attestation of the
fact or event for which it's cited—the canvass, the session law, the executive order, the reported decision, the
indicator—the 'witness' collapses to the record itself, and no 'witness' tree need be compiled."

Diplomatics' name for it (recalled; Check: Duranti, *Diplomatics: New Uses for an Old Science*): the *dispositive*
document, which brings the act into being, against the *probative*, which gives evidence of an act already done. The
law is the statute; the order is the order; the result is the certified canvass; the figure first reported is the
release. Nothing upstream of them can say better what they are.

- **What it closes.** Only the units the record constitutes: the act, its text, its date, its number, the figure as
  released. Not its circumstances: who drafted the order, who was in the room at the signing, why the figure was
  late, what the decision was taken to mean. Those units keep their trees.
- **Which copy.** The record or its official print, as the series already cites them: the Statutes at Large (legal
  evidence of the law, 1 U.S.C. § 112), the session laws, the Federal Register, the U.S. Reports or the reporter, the
  State's certified canvass, the release or the publication that first printed the figure (the *Survey*, the
  *Economic Report*), the Senate's *Executive Journal* for a confirmation. A compilation from records (the Clerk's
  *Statistics*, CQ's *Guide*, the *Congressional Directory*), a print of a document that is not itself the act
  (FRUS, the Public Papers' texts of remarks), and the Record's text of a speech (members revise their remarks) are
  probative: the ordinary rules hold.
- **What still enters.** Witnesses that agree with the record are not sought or registered. A witness that disagrees
  with it (another date, another figure, another text), or an official text at odds with another (the History of
  Bills' misprinted page; the Clerk against the canvass), is recorded as a variant against the unit, since it is
  evidence of an error or a dispute.
- **When the tree comes back.** Where the record itself is in question: a contested or recounted election (Illinois
  and Texas, 1960; Minnesota, 1962), a document's date that differs from the act's (an order signed one day and
  dated or published another; a bill signed at a ceremony after its signing), a disputed authenticity or validity
  (a pocket veto). The unit then takes a tree like any other, the record its first root.
- **In the data.** A claim-map row to the linked record, its kind one of a short list (`DISPOSITIVE` in the module:
  statute, session law, treaty, order, proclamation, regulation, decision, canvass, release, journal), closes the
  unit: `stemma` shows it so, and `check` asks no root of it. A unit marked `disputed` reopens it.

## 3. The rules for the readers

1. **Register every witness met that bears on a claim, however well attested the claim already is.** A witness
   copied from one already registered (a codex descriptus: the same text, nothing added) is entered as its edge to
   that one (`copy`, `print`, `edition`), one line, and never counts as support; it is not dropped (the owner, Oct.
   30: "Don't drop the first rule"). The edge is what finds circular reporting, and it keeps a later witness that
   corrects an earlier (a better transcription, a fuller print) from going out on a wrong ruling.
2. **Studies, memoirs and documentary collections are witnesses.** The study a note cites is registered, with the
   edge from the work read and its own source an open upstream where the reader cannot follow it (Chen's Li Ke and
   Hao Shengzhang). A collection is registered as the print of the document it prints: the document is the witness
   the claim rests on, the collection its `print` edge, the page its place.
3. **Follow each branch as far as the series can.** Where the series holds the upstream (a card read, the daybook's
   FRUS document, the Public Papers, the Miller Center's recording, the Daily Diary, an open scan), follow it and
   register what it rests on. Where it cannot, name the upstream as exactly as the witness lets (the file, the box,
   the collection, the author and date) and mark it open. "Cited by" is not the end of a branch.
4. **Describe each witness by** whose account it is (`agent`), when it was made (`made`: its date, and
   `contemporaneous` or `later`), its form (`form`: original, copy, print, translation, transcription, account,
   study), and, for each claim it bears on, whether its information is firsthand (`knows`: firsthand, secondhand,
   undetermined). Kept as the witness gives it; nothing graded.
5. **Record each disagreement as a variant against the unit**, each witness's reading in its own words, briefly, with
   its page: the apparatus. "Check: Sorensen gives ..." stays in the note for the reader of the page; the variant is
   its data.
6. **"Already in under another id" adds the witness to that entry's map**; it is never a reason to pass it over.

What a reader still passes over is as CLAUDE.md says (out of the brief, private trivia, a repetition with nothing
new); a witness to an entry is never minor.

## 4. The data

```
sources/witnesses/<prefix>.yaml   the registry: one witness a row, by a stable id (x.<date>.<slug>), a file a year
                                  of the witness's date and `undated.yaml`; works are not rows (their cards are)
```

```yaml
- id: x.1964-08-13.mao-le-duan                # permanent; never reused
  what: Transcript, Mao Zedong's conversations with Lê Duẩn, 16:00-18:00, Aug. 13, 1964
  kind: transcript                            # the KINDS of cited_records.py
  date: '1964-08-13'
  agent: [name:mao-zedong, name:le-duan]      # name tags where the person has a name entry, else the name
  made: contemporaneous                       # or later, with `made_on`
  form: transcription
  where: Chinese Central Archives, Beijing    # repository and file, as the citing witness gives it
  from: []                                    # upstream edges: [{of: x.…, kind: recollection}]; empty: a root
  open: closed archive                        # why the branch ends here: closed archive, not found, not held, none known
  copies: []                                  # a copy the series can read: FRUS doc, Papers item, recording, scan
  read: false
```

- The works are the cards. A work's edges are rows of its own file (`sources/witnesses/by-work/<card>.yaml`): `{at:
  '213 n.36', of: x.1964-08-13.mao-le-duan, kind: citation}`, its page and note, as the `cited_by` of today.
- The claim map's rows stay as they are (`w.jian-maos-china-and-the 213: B`); a `via` row names a witness id
  (`via x.1964-08-13.mao-le-duan: B`), and the path from the item to the root is computed from the edges, so a row
  never has to be written twice.
- Variants: on the entry, hidden, `variants: [{unit: B, witness: x.…, reads: '…', at: '…'}]`, held to the map by
  `check`.
- `check` [witnesses]: an id that names nothing; an edge to itself or a cycle; a witness with no `from` and no
  `open` (a root must say why it is one); a `via` to a witness no item of the note leads to; a variant's unit not in
  `c`; a `copies` entry that names nothing the series holds.
- `./bib stemma ID [UNIT]`: each unit's tree, from the items of the note down to the roots; the count of roots and of
  independent agents; the copies marked as copies; the variants; the open upstreams, which `./bib stemma --leads`
  lists for the procurement and the primary-record runs.
- The verbose citation form (CLAUDE.md, "Claims and their sources") then says what each unit rests on: "Rests on two
  roots: the tape (Miller Center); Bundy to Johnson, Feb. 7, 1965 (FRUS 1964-68, II, doc. 84)."

## 5. The conversion

Mechanical, once (`tools/witnesses/convert_records.py`, to write): each row of `sources/cited-records/` (8,080, in 72
files) becomes a witness, its `cited_by` an edge from the work's card, its `found` a `copies` entry; each `via` row
(6,032 in the calendar) points at the new id; rows naming one record under two works become one witness with two
edges (matched by kind, date and the `record` text, a list of near matches for a reader). `sources/cited-records/`
then goes to `notes/extensions/shelf/`, and CLAUDE.md's "What the works rest on" is rewritten to these rules. The
records' `open` and `agent` are left blank where the old files do not say: the first pass of each reader fills them
for the entries it touches.

## 6. The order

1. The schema, the check, the conversion, `stemma` (one session).
2. The readers' brief: §3 in its place (rules 5 and 5b of brief-batch3.md, and CLAUDE.md).
3. A test: the Chen and Asselin backfill read again under the rules, their trees checked against the books by a
   second reader; what the rules miss, fixed.
4. Then the twenty batch-3 readers resume.
5. Later, a pass by event rather than by work: for each event's first entry, the other witnesses the series already
   holds (the daybook's FRUS documents and recordings of the day, the Public Papers, the Diary, the cards cited under
   later entries) gathered into its map. This is the compilation of accounts the readers do not do, reading one
   work each.

The cost is reading time: rules 1 and 3 make each run longer, as they mean to.
