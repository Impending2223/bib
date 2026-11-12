# Visibility: whose record, and who knew (spec, Nov. 11, 2026)

The owner's design (Nov. 11, 2026, messages in `notes/owner-brief.md`), written out for building. Where the owner has not ruled, the default is marked **(ruling wanted)** and the build starts from it.

## 1. What it is for

The calendar today is one country's: the United States'. It is to take in the high politics, policy, leadership and alternatives to the leadership of the USSR, the PRC, the UK, France and West Germany, and to let the reader see any part of it by country and by knowledge: what was public, what was known only within a government, and from when. The reader filters with toggles at the head of every calendar page and may pin a date of knowledge.

## 2. Terms

- **Polity**: a state (or a group of them, below). The top level: the US, the USSR, China (the PRC), France, Germany (the Federal Republic), the UK. Under **Other**, folded: every other state the calendar meets (the DRV, the RVN, the GDR, Cuba, Laos, Cambodia, Poland, Israel, the UAR, India, Pakistan, Japan, the ROK, Canada, Italy, ...), each with its own toggles, added as entries need them.
- **International organizations** (the owner, Nov. 11: "International organizations are 'inter-national.' The provenance and address of the interested state-parties should be filleted out."): the UN, NATO, the OAS, the EEC and the rest are not polities by default. A claim from or about one takes the P and A of the state parties concerned: the Soviet delegate in a colloquy with the American at the UN is `USSR:public-PA` and `US:public-PA`; a NATO or EEC conference takes the provenance and address of its relevant member states. An organization becomes a polity of its own (under Other) only for a claim nonpublic-P to it and to none of its state parties (`EEC:nonpublic-P`: the Commission's own deliberations, unknown to the Six).
- **Claim**: a unit of an entry's `c`, as its claim map divides it (`./bib claims show ID`). Where an entry has no map, or its rows map to `?`, the whole entry is one claim, marked unmapped (§7).
- **Witness**: a source a claim rests on (a work card, a primary record, a "via" record behind a work).
- **P (provenance or privity) for X**: the claim was published in X, or known within X's government in private.
- **A (address) for X**: the claim is about X: X itself, its government, its agents, its territory.
- **public / nonpublic**: whether, at the reference date (§5), a witness of the kind that makes it public exists.

A claim carries, for each polity, P or A or both (shown PA), each public or nonpublic at the reference date. Tags read `US:public-P`, `USSR:nonpublic-A`, `US:public-PA`.

## 3. The rules (the owner's)

**P, public.** A witness published in polity X makes the claim `X:public-P` from its date of publication. Provenance is the country of the newspaper, the publisher, the official series (the *New York Times*, US; *Pravda*, USSR; *Học Tập*, DRV; Hansard, UK; the *Journal officiel*, France; a memoir's first edition, its publisher's country).

**P, nonpublic (privity).** Before it is public in X, a claim is `X:nonpublic-P` from the event's date where:
- *territory*: the act took place within X's territory (as stated, every act there, with rulings for the exceptions; ruled Nov. 11);
- *agency*: the act was X's, or its agents' (so a claim resting only on the memoir or diary of an X official is `X:nonpublic-P` from the event, `X:public-P` from the book's first publication: a Humphrey claim resting only on Solberg, 1984, or Humphrey's memoir, 1976, is `US:nonpublic-P` to 1976 or 1984, whichever is the earliest publication that is authority for it);
- *parties*: the claim is a private communication, visible to its parties only (a FRUS document: its sender's and recipients' polities; the DDF; the AAPD).

**A.** A claim that addresses X is `X:public-A` from the date of the earliest public witness anywhere (the *Times* on Moscow makes the claim `USSR:public-A` that morning; *Pravda*'s "We condemn President Kennedy" makes it `US:public-A` that day), and `X:nonpublic-A` before it, from the event's date (the FRUS memorandum on Moscow: `USSR:nonpublic-A` until the volume's publication).

**Public sources.** The press, public laws, the Public Papers, the *Bulletin*, the *Congressional Record*, Hansard, the *Journal officiel*, the Bundestag's *Plenarprotokolle*, the published economic indicators: public from their date, P for their country, A for each polity the claim addresses.

**Rulings override** any of this, claim by claim or entry by entry (§8).

## 4. Address: how it is inferred

An entry is one event, so every claim addresses the event's parties: the entry's name, place and polity tags, with any the claim map ties to the unit added; where the entry has none, its thread's polities and its `also` threads'. (The owner, Nov. 11, on the prototype: Robert Kennedy's "It's like this, Georgie" to Bolshakov and the *Post*'s "MiG Deal with India Appears Off" both address the USSR. The first build took a unit's own names in place of the entry's, so the remark addressed the US alone; and a thread's polities without its `also` threads', so the MiG entry missed the USSR.) A person present is an agent of his polity: the talk is privy to both (`USSR:nonpublic-PA` as well as `US:nonpublic-PA`).
- **Persons**: one polity, with dates where allegiance or office changes (from the name entries' roles).
- **Places**: usually one polity, several where contested or shared (Berlin, the Gulf of Tonkin, the Taiwan Strait, Jerusalem).
- **Threads**: a list of polities; subthreads inherit it unless they set their own. Threads will need re-potting to keep their lists honest (the Western Alliance first: a proposal follows).
- **Polities named outright** ("the U.S. bandits"): a `polity:` tag the reader writes. Never guessed from the wording.

The namespace is `polity:` (`polity:us`, `polity:ussr`), not `state:`, which is the US States'.

## 5. The reference date: at the time, unless pinned

The owner, Nov. 11: "Public at the time, with a pin date to override it."
- **Default**: each claim is judged at its own date (the entry's `date`, the first day of a loose one). A memorandum of Oct. 22, 1962 is `US:nonpublic-P` there, though FRUS printed it in 1996. "At the time" is the event's day and the next morning's papers (the newspaper band of `tools/bib/dayorder.py`; ruled Nov. 11).
- **Pin**: the reader picks one date for the whole page; every claim is judged at it. A pin of Jan. 1, 1964 shows what was public or privately known by then.
- **Loose dates.** A witness's loose date resolves to the first day of its window (a memoir of "1976" is public from Jan. 1, 1976). A claim of a loose date ("Oct.") is nonpublic from the window's first day and judged at its end, with the next morning's papers (Nov. 1 for October), so a paper of Oct. 30 counts (Nov. 11, on the prototype). An undated record takes a year it prints ("*New Times*, no. 5, 1989"), never the event's day.
- **Before the event.** At a pin earlier than a claim's date, nothing is known of it. Such entries are shown greyed, as not yet known (ruled Nov. 11).

## 6. The toggles

- **Place**: at the head of every calendar page, under the table of contents, above the threads.
- **Layout**: two columns at phone width, three or four at desktop; each polity a line, with *public* and *nonpublic* indented under it; *Other* folded, its states under it.
- **States**: each toggle cycles **on**, **greyed**, **off**.
- **Combination**: a claim shows in full if any of its tags is on; greyed if none is on and any is greyed; hidden if all are off.
- **P/A**: one switch for the panel: *by provenance*, *by address*, *either* (default *either*). (The alternative, P and A toggles under each polity's public and nonpublic, is twenty-four lines for six states: too long on a phone.)
- **Pin**: a date field, empty for "at the time".
- **Defaults**: the US and its sub-items on; every other polity and sub-item greyed.
- **Memory**: the reader's choices kept in the browser (`localStorage`), per reader; the page works without it.

## 7. Claims on the page, and the unmapped

Each claim is rendered as its own span carrying its tags and dates as data; the page's script filters. An entry with no claim map, or whose witnesses map only to `?`, is one claim with the union of its witnesses' tags, marked *unmapped* (a faint mark), so the reader knows its filtering is coarse. Every batch that maps units refines it. Until the programmatic pass (§9) reaches an entry, it carries the placeholder `US:all` (derived, not stored), to be deprecated as entries are computed (the owner: "All current items are to be tagged US until ruled otherwise").

## 8. What is stored and what is derived

Derived at build, never stored: every `X:public-P`, `X:nonpublic-A` and the rest, and their dates, and `US:all`.

Stored:
- **The provenance registry**, `sources/provenance.yaml`: for each periodical, publisher, official series and document series: its polity and kind (press, official public record, document series, memoir or diary, oral history, scholarship). Filled by program where the source says it (FRUS, the Papers, the *Record*, the *Bulletin*, the press), by recall or by hand otherwise.
- **On works**: the first edition's year and country (cards hold the year; the country comes from the registry's publisher).
- **On name entries**: `polity`, with date ranges.
- **On places**: `polities`.
- **On threads**: `polities` (th.yaml).
- **On entries**: `polity:` tags where address is named outright; `vis:` rulings (an override of any computed tag, with a reason).
- **On primary records**: the parties (FRUS: sender and recipients, from the document's heading).

## 9. Phases

1. **Registry and polities.** The provenance registry; polities on names, places and threads (threads as proposed for re-potting); the program to compute each claim's tags and dates; `./bib show` to print them; a `vis` section in `./bib check` (a claim with no computable tag; a person with no polity).
2. **Prototype.** The panel and the filtering on one month's page (October 1962: dense, every kind of witness), for the owner to try at phone and desktop width.
3. **Roll-out.** Every calendar page; `US:all` shrinks as entries are computed. **Phase 3 done**, Nov. 12, 2026 (the owner, Nov. 11: "The visibility setup looks good to go"): the panel and the filtering on every calendar page and in the reader's year blocks, by the build itself (`tools/bib/vispage.py`, its STYLE; the prototype, `tools/vis/prototype.py`, now a wrapper of it).
4. **Going forward.** The reader card: each new claim's witnesses carry what the program needs (kind, country, parties); `polity:` tags where address is named outright. The audits check them.
5. **Rulings.** The `vis:` overrides, as the owner rules.

## 10. Rulings wanted

Ruled Nov. 11 (the owner: "Defaults on the other three"):
1. "At the time": the event's day and the next morning's papers (§5).
2. The territory rule: as stated, every act within the territory, rulings for the exceptions (§3).
3. Entries dated after the pin: greyed, as not yet known (§5).
4. ~~Organizations~~: ruled Nov. 11 (§2): state parties' P and A; an organization a polity only where a claim is nonpublic-P to it and to no state party.
