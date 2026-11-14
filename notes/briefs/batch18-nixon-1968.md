# Batch 18: Nixon, 1968, California, Agnew, and *Freedom of Communications* (planned Nov. 14, 2026)

The owner, Nov. 14, 2026: "Put RMN after Batch 17 and ahead of the pilots, along with some other materials, scoped to the full calendar rather than for RMN alone: Freedom of Communications, the 1968 campaign volumes, the 'lightly, for context' volumes, the other Nixon biographies (not read lightly or for context alone; Pat Brown and his California is also within-scope), and our Agnew materials." The gap it answers: `notes/inventory-2026-11-14.md`, section 4 (Nixon entries by year: 1960, 445; 1961–67, 23 to 56 a year, a third of them polls; 1968, 433).

## The rule for every reader
**Scoped to the full calendar, to Jan. 20, 1969.** Each book is read for every event it dates and treats from Jan. 1, 1960 to the inauguration, Jan. 20, 1969 (the owner, Nov. 14: "This project only runs through January 20, 1969, not to the end of our calendar. For the period after that, we start with a different skeleton."), whoever the actors: Nixon's acts first, but the Democrats', the Republicans', the press's, the States', the war's equally; nothing passed over because it is not Nixon's. Read in full, not for context; no book here is read "lightly."

The method is the reader's brief (`notes/briefs/reader.md`; CLAUDE.md is the core): an event already in the calendar takes a `cite` (one pinpoint and one parenthetical per cite op), a `variant` or a `check` where the book differs; new entries only for what the calendar lacks; R7's informal record (calls, meetings, letters, planning, staff memoranda) and the owner's ruling for opinion and gossip (Nov. 14: "I like opinion and gossip!"), each as its teller's account; whose account it is named (R24). A card first (`./bib works new`) where the book has none. Visibility (`tools/bib/vis.py` STYLE 4 and 8): what was private at the time ruled, the legislators' and private persons' rules of Nov. 14 applied, an opposition politician's talk abroad given "Check: whether X reported the talk to the Y government." Fetch the Drive file whole by curl into a new empty directory of your own (`curl -sSL -o DIR/x.pdf "https://drive.usercontent.google.com/download?id=ID&export=download&confirm=t"`); scripts elsewhere; Python with -I; delete the copy when done. Never more than about 40 entries in one tool call (an agent failed at the 128,000-token output limit): build the patch a year or a chapter at a time. Patch `inbox/<date>-b18-<name>.yaml`, ids by `./bib new-id`, claimed with `./bib ledger add`; `./bib patch-check` to 0 errors; a book-check file per book (`notes/book-checks/<card>.md`). Every patch audited by Opus before it merges.

## The readers (one a book unless marked; the Drive id; the card where one is held; cites so far)

**The Nixon biographies (in full, Jan. 1960–Jan. 20, 1969)**
1. Ambrose, *Nixon: The Education of a Politician, 1913–1962*: from 1960 to its end. `1r987nsz4qw9ffY9_Xk3xanCXasgjD4pZ`; `w.ambrose-nixon` (5).
2. Ambrose, *Nixon: The Triumph of a Politician, 1962–1972*: to the inauguration, Jan. 20, 1969. `18jW3Oc4bgCs8EboPAZ-vHJ34w-f7rIpN`; `w.ambrose-nixon` (the card is the set: say which volume).
3. Farrell, *Richard Nixon: The Life* (2017): 1960 to the inauguration. `1NAtqmoFROUuN56DfytE5mlWJd66kKIGN`; `w.farrell-richard-nixon` (4).
4. Aitken, *Nixon: A Life* (1993): 1960 to the inauguration. `1dQKXMOX2DTnpvdH0vtYD-QYzBAuB1PWF`; `w.aitken-nixon` (0).
5. Black, *Richard M. Nixon: A Life in Full* (2007): 1960 to the inauguration. `18fXPDTPH-mzl65v720Hu1sbo-wHMLO7H`; `w.black-richard-m-nixon` (0).
6. Wicker, *One of Us* (1991): 1960 to the inauguration. `1SYRkjuzqe3bx2SngkKBz5kLYB_AoRz0m`; `w.wicker-one-of-us` (0).
7. Gellman, *The President and the Apprentice* (2015), its 1960–61 chapters, and *Campaign of the Century* (2022), whole. `1neKeviTQGNffe_3Dt9LXe8a2jiA207Sw` (`w.gellman-president-and-the-apprentice`, 8); `1HlZIAdBdh7aATvpoCaVTJO5-ExqnH78p` (card to make).

**Nixon's staff and insiders**
8. Buchanan, *The Greatest Comeback* (2014). `1e2EmVouea6YKkpSB1UHePVaIijTX0T3Z`; `w.buchanan-greatest-comeback` (0).
9. Price, *With Nixon* (1977): to the inauguration. `1fwKb5Ts_Lnq2k7YwfVNpjhu2_Fo5kYVv`; `w.price-with-nixon` (0).
10. Klein, *Making It Perfectly Clear* (1980): 1960 to the inauguration. `1aayfq3Z7o7XHIN7yc7Xgb7vaZ8KJdwwx`; `w.klein-making-it-perfectly-clear` (0).
11. Safire, *Before the Fall* (1975): to the inauguration. `14CZgaGSnoXdF2lT1qItre48QuOAylsiJ`; `w.safire-before-the-fall` (6).
12. Garment, *Crazy Rhythm* (1997): 1960 to the inauguration. `1M2nU_GtRpMe2eeN49TkYPGY-KIN_3cmc`; `w.garment-crazy-rhythm` (1).
13. Whalen, *Catch the Falling Flag* (1972). `1X9me96dzYnklHl6uEC64GHJNRshXK_UI`; `w.whalen-catch-the-falling-flag` (1).

**The 1968 campaign**
14. Witcover, *The Resurrection of Richard Nixon* (1970). `1Ke3jfY1V0SsKTcOLgWH65h1-fQUK1r18`; `w.witcover-resurrection-of-richard-nixon` (8).
15. Wills, *Nixon Agonistes* (1970). `1uG0eYCrwvgE1JCXVNx3TRTkduI-antRb`; `w.wills-nixon-agonistes` (0).
16. McGinniss, *The Selling of the President, 1968* (1969). `1_otzU8F_f-MdwJOVv22dt6-3-YHnBKWX`; `w.mcginniss-selling-of-the-president` (0).
17. Nelson, *Resilient America* (2014). `1F50c-XZJLvyKRhuj4j0suqB5SCOFjMvG`.
18. Cohen, *American Maelstrom* (2016). `1w_KzE-jMkEh_2slF99t3ox3tOOVYMqZW`.
19. Goudsouzian, *The Men and the Moment* (2019). `1pRUc3i4jSXOenwPMH7P0YB9fi1WrjlW2`.
20. Nichter, *The Year That Broke Politics* (2023). `1ZEslp2heZdrCCOXT-tkfr98X2QKu-JWy`.
21. Hendershot, *When the News Broke: Chicago 1968* (2022). `14ZyaQfDJmywKoQJg3lzZjbzzFKWJhXw2`.
22. Eisele, *Almost to the Presidency: A Biography of Two American Politicians* (1972), Humphrey and McCarthy, 1960 to the inauguration (the owner, Nov. 14: "bring back Eisele. Lays the groundwork for later McCarthy and Humphrey runs at a lower cost than the memoir material."). `1y8D_hc4FctURtNTfvFI5_I_GVwzLkPcj` (9).
Skipped for now (the owner, Nov. 14: "Skip McCarthy, the McCarthy people, Boomhower and Chafe on Lowenstein for now."): Stavis, Hoeh, Larner and Herzog on the McCarthy campaign; McCarthy, *The Year of the People*; Boomhower, *Robert F. Kennedy and the 1968 Indiana Primary*; Chafe, *Never Stop Running*. Their Drive ids are in the inventory and the Drive list.

**California**
23. Rarick, *California Rising: The Life and Times of Pat Brown* (2005): 1960 to Jan. 20, 1969 (the governorship, the 1962 and 1966 races). `1rrtfM95s-7bIHlTbH6WqX4-sRQkKFMni` (8).
24. HoSang, *Racial Propositions* (2010): the 1960s chapters (Proposition 14, 1964). `1Q_uFIybQ7mZa1e4IT-7VuDn4jIPclwt2`.

**Agnew**
25. Witcover, *White Knight: The Rise of Spiro Agnew* (1972) (`1H_BEe0iMMDdTb_Svmpb7UWLoYMedvBl2`; `w.witcover-white-knight`, 10) and Agnew, *Go Quietly ... or Else* (1980), its chapters on 1966 to the inauguration (`1ErgMYVDsaGwOUTMHh1QYzU-5ZaujfF3s`; `w.agnew-go-quietly-or-else`, 0).

**The record: *Freedom of Communications* (S. Rep. No. 87-994, 1961)**
26. Pt. 2, Nixon's speeches, remarks, press conferences and statements, Aug. 1–Nov. 7, 1960 (the Drive's "Freedom of Communications - Freedom of Communications", `12DPt8MZA56iB679KBfjbs0FWQ-JXX9IS`; confirm the part from its title page): two readers, Aug.–Sept. and Oct.–Nov. A primary record: each speech or statement its day's entry or a primary cite on the entry held (the `primary` op; the form of pt. 1, card `w.communications-freedom-of-communications-part`, 439 cites).
27. Pt. 3, the joint appearances (the debates; `1pp7JZ5UFtnED6rdFmPMLdfIV5OzCzrnH`), and pt. 4 (`14KvfZ7IHKCcJSyeCruqRpTL68xRRslnk`; say what it holds).

## Wanted, not held (for the owner to procure; see the inventory)
Mazo and Hess, *Nixon: A Political Portrait* (1968); Parmet, *Richard Nixon and His America* (1990); Rosen, *The Strong Man* (2008); Stans, *One of the Presidents' Men* (1995); Phillips, *The Emerging Republican Majority* (1969); Dent, *The Prodigal South Returns to Power* (1978); Ehrlichman, *Witness to Power* (1982); Hughes, *Chasing Shadows* (2014); Witcover, *Very Strange Bedfellows* (2007); Coffey, *Spiro Agnew and the Rise of the Republican Right* (2015); Lippman, *Spiro Agnew's America* (1972); Nixon's articles and column, 1961–68, the 1968 speech collections, and the Nixon Library's Wilderness Years Collection.

## Order and pace
After batch 17, before the French and German pilots. Five or six readers at once, then their audits: the biographies and Buchanan and Witcover first (they set the spine), the insiders next, the 1968 books, then California, Agnew and *Freedom of Communications*.
