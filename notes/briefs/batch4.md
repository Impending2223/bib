# Batch 4: the owner's books of Nov. 5, 2026

The owner put some seventy books into the shared Drive folder on Nov. 5, 2026, most of them works the calendar cites only behind "To check:" (the never-read list of that day), and ruled the same day on the leads canvass ("Send them all back, work by work, a reader a work, the largest first"). A reader a group below.

## For every reader

1. Read `CLAUDE.md`, then `notes/briefs/reader.md` in full: the rules in force, among them R5 (what is an entry), R13 (the press), R14 (military matters), R17 (spans; one event, one entry), R18 (what is not an entry), R35-R43 (the witnesses), R44 and R48 (Passed over), R49-R51 (the ledger and the additive ops), R50 (leads, as restated Nov. 5: a lead is only what cannot go in on a source in hand), R54 (the copies). Never read `build/` or a whole list file.
2. Your books: the owner's PDFs in Drive, by the ids in the table. Download each by the direct route of R54 (`curl -sSL -o <dir>/<short>.pdf "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`) into a new empty directory under the session's scratchpad, `books/b4-<group>/`; check it with `file`; read its text layer, or OCR it and say so. Find the folio offset (R54). Read each page you cite off the page image as well as the text. Never change a file's sharing. Delete your copies when you finish.
3. The card: `./bib works show <card>`. A book without a card (the table says NEW): make one in `works/` (structured: author, title, year), as CLAUDE.md's works catalogue says.
4. First, the entries waiting on the book: every calendar entry citing it behind "To check:" (`grep -rn '<card>' lists/cal/`, reading only the entry's lines; `./bib show ID`). For each, read the pages that treat the entry's event and: move the work out of "To check:" with its pinpoint and, where it stands for part of the entry, its parenthetical (the additive `cite` op, with `units`); where it disagrees, a variant (R41) or a `check` op; where it does not treat the event at all, leave it behind "To check:" and say so in the book-check file (a work in an event's bibliography need not treat every entry).
5. Then the leads sent back: `notes/leads-canvass.md`, section "B: entry-writable now, by work", and the C list, under your card's short name, if any (`grep -n '<short>' notes/leads-canvass.md`). Each is an entry now (R50, as restated), a variant or a Check, or a row of Passed over with its R18 ground.
6. Then the book through, within the span (Jan. 6, 1960 to Jan. 20, 1969, and the primary seasons of 1972 and 1976): every event it dates and treats is an entry (R5), or cited under the entry already there (`./bib ledger find DATE [--until DATE]`; `./bib find WORDS -l cal --since ... --until ...`), or a row of its own in Passed over with its R18 ground. A memoir's or a study's own account of what the author did and said is primary for that (R5). A book in another language: the series' rules for names and transliteration; quote nothing beyond a few words; cite by page.
7. Witnesses (R35-R43): the records the book's notes give for the units you cite, to `inbox/witnesses/2026-11-05-b4-<group>.yaml` (never the year files), and the work's edges to `sources/witnesses/by-work/<card>.yaml`; `via` rows in the `src` you write.
8. One patch a group, `inbox/2026-11-05-b4-<group>.yaml` (a second, `-2`, past some 400 ops): new entries claimed first in the ledger (`./bib ledger add`); additive ops wherever you only add (R51); `edit` with a fresh base (`./bib show`) only where you change `c` or rewrite `n`. `./bib patch-check` until it has no errors.
9. The book-check file, `notes/book-checks/<card without w.>.md` (new, or carry on an old one): the copy read and its offset; the To-check entries, each ruled; what you entered; Passed over row by row (R44, R48); "## The press" (R13); "## Leads" (R50). Markdown not hard-wrapped.
10. Do not merge, fold or commit: the merger does. Working hours: CLAUDE.md, "Working hours"; if told to pause, stop at a clean point, leave your files consistent, and say in the book-check file where you stopped.
11. Your last message: the patch's name and size (entries added, cites, checks), what you could not read, and anything the merger must know.

## The groups

| # | Group | Books (card; entries waiting) | Drive ids |
|---|---|---|---|
| 1 | prezidium | w.prezidium-tsk-kpss-1954 (16 to check); w.prezidium-tsk-kpss-1954 (16 to check); w.prezidium-tsk-kpss-1954 (16 to check) | 1S5BJVMgeahEnBqre5tItBlITqVRmfYZX (28 MB); 12I51GojUZ_L7PcFEet6n3GioqFmdmjTB (44 MB); 1S2n-L-D_8BN8Zh8f_e5L5D9O5Zm-cl2X (112 MB) |
| 2 | peirce-great | w.peirce-great-plains-states-of (38 to check) | 1H2oT8DVRokLh6xYaoaGnO4TweQJlCCUd (28 MB) |
| 3 | young-easy | w.young-easy-burden (32 to check) | 1nfsQPCtZW69q429KTn7GsPTMvq7S2juF (30 MB) |
| 4 | cohen-american | w.cohen-american-pharaoh (32 to check) | 1YGoRogLjix0RLqMZ60GDMC7304UKr2wH (37 MB) |
| 5 | whalen-longest | w.whalen-longest-debate (31 to check) | 1SJE2gXIzngIzj3SF514-9PdDy6KyYuyO (13 MB) |
| 6 | peirce-mountain | w.peirce-mountain-states-of-america (30 to check) | 1-FPhvqcuZahJv3r0s1Ic_IEjcYICMYTU (34 MB) |
| 7 | anderson-confronting | w.anderson-confronting-the-color-line (29 to check) | 1-5M_4I_zQRlixmWJqbbb9-WdAtKJk6ua (44 MB) |
| 8 | wofford-of | w.wofford-of-kennedys-and-kings (29 to check) | 1lbcfunlMXDxQel1H7kSiJVkU6XVVWMZd (26 MB) |
| 9 | debenedetti-american | w.debenedetti-american-ordeal (27 to check) | 1_nFvLjPMNdauVsL3WsIYu9-TbnYGBEou (53 MB) |
| 10 | taking-charge | w.taking-charge (25 to check) | 1NkEeNniIBmF0is2eEqIozpxq75cJqTmq (45 MB) |
| 11 | zaroulis-who | w.zaroulis-who-spoke-up (24 to check) | 1E-M1yQmXAtB2-_wfo7x576BfpfXwHW-B (34 MB) |
| 12 | wells-war | w.wells-war-within (24 to check) | 1cyXavHHqBSvXgqmpAterOd0D-gIYJ1FQ (45 MB) |
| 13 | taylor-swords | w.taylor-swords-and-plowshares (21 to check) | 1NT5EZhhkS0qn2L4c1Dy5xEQ0XOma5C8i (22 MB) |
| 14 | graham-uncertain | w.graham-uncertain-triumph (20 to check) | 1KR6bbpkmvbtnG4UPN7G2EysMfQlzwz0L (14 MB) |
| 15 | ralph-northern | w.ralph-northern-protest (20 to check) | 13Vnlssr2f9dU8iSlrmVEaGI-FxHdpW_w (21 MB) |
| 16 | garrow-protest | w.garrow-protest-at-selma (20 to check) | 1HeSaDxoS5k_JNa_C5xHT2QVXv6WpndoS (27 MB) |
| 17 | goodwin-remembering | w.goodwin-remembering-america (19 to check) | 1zMNbWrVGW4PjoYibl9C_6UnqSIHs-RE9 (68 MB) |
| 18 | pair-blair-brazinsky | w.blair-lodge-in-vietnam (9 to check); w.brazinsky-nation-building-in-south (9 to check) | 1OR030ZPaEyULQWAhIHaidFRTbWnXsk3- (12 MB); 15bMpRpFF43lbCpiuiZ1auguy2k2imkwI (2 MB) |
| 19 | pair-collins-david | w.collins-more (9 to check); w.david-with-dignity (9 to check) | 19_vTxQlz80GadOvCWOYe9uY3lvvT6rew (1 MB); 1d9OKJstUYdCaNwYSTHo51PHZjzfdGCX- (7 MB) |
| 20 | seaborg-stemming | w.seaborg-stemming-the-tide (17 to check) | 17GlQwhfItSmSXT1EnDoWUuC0e1A1qXnn (36 MB) |
| 21 | beifuss-at | w.beifuss-at-the-river-i (17 to check) | 1Fdq7rmhuv1Cw1Zo60JiIjZiOviN3U1kQ (23 MB) |
| 22 | mcknight-last | w.mcknight-last-crusade (17 to check) | 1LCPxj0qu0MgR7-IOR1_GwSiWG2WUDWte (13 MB) |
| 23 | payne-ive | w.payne-ive-got-the-light (17 to check) | 1NCpLZpHMqc0kDCNbNDuSUElPdKrrlBL7 (28 MB) |
| 24 | pair-berkowitz-beschloss | w.berkowitz-mr-social-security (8 to check); w.beschloss-crisis-years (9 to check) | 19xXO8i7EecR2m6C0rz77I9S4FV5TeJn4 (41 MB); 1kjNZ4GRtgsH_yXZgBcpLW0gVARKvxSm9 (91 MB) |
| 25 | pair-middendorf-mollenhoff | w.middendorf-glorious-disaster (8 to check); w.mollenhoff-george-romney (9 to check) | 1dgzeuIoXhLMcWcYgr37RoZsbwlZXGqhx (20 MB); 1fg8dcWFq1u_lAnoazbKmYlFvRAa4B606 (12 MB) |
| 26 | pair-witcover-zelizer | w.witcover-resurrection-of-richard-nixon (8 to check); w.zelizer-on-capitol-hill (9 to check) | 1Ke3jfY1V0SsKTcOLgWH65h1-fQUK1r18 (18 MB); 15nwju8e9uD-ujXyVrBIWJAGT3q_AScTc (7 MB) |
| 27 | macneil-dirksen | w.macneil-dirksen (16 to check) | 1M3f2u73qr7Ty3yVmXO6C_wHQxKLIDGrC (20 MB) |
| 28 | solomon-international | w.solomon-international-monetary-system-1945 (16 to check) | 1JXWVILVf9sfEZzYaQ4jv_b5m61OQLgOq (18 MB) |
| 29 | pair-bryant-casey | w.bryant-bystander (8 to check); w.casey-making-of-a-catholic (8 to check) | 1EsqMJ-DJmje35jwDS-TdRxtlMiOpETkp (40 MB); 1dNSDWMhrryDEV6bo8Q3BWqSmFmZjXwxE (1 MB) |
| 30 | pair-quandt-rarick | w.quandt-peace-process (8 to check); w.rarick-california-rising (8 to check) | 1a2IGUG-7XAa3lAsAz6AEwQzijm9xDNte (4 MB); 1rrtfM95s-7bIHlTbH6WqX4-sRQkKFMni (4 MB) |
| 31 | cagin-we | w.cagin-we-are-not-afraid (15 to check) | 1nd6kjdQOqL1_agvTtFICToyew3NSQdG7 (30 MB) |
| 32 | connery-rockefeller | w.connery-rockefeller-of-new-york (15 to check) | 1nvlr2B2S_70GWCI7YE3dl7G5J4RBhizV (31 MB) |
| 33 | meier-core | w.meier-core (15 to check) | 1Ca7jKPEfBVbbjgJQfHrXgKVln3oglrVu (29 MB) |
| 34 | pair-dierenfield-evans | w.dierenfield-keeper-of-the-rules (6 to check); w.evans-lyndon-b-johnson (9 to check) | 1yoKkEX6nogUoMH3q0sKRH0jqsMnSKduV (19 MB); 1WRGa2XmeRAC3mSPKOFfuAuzk0IHgfnrU (38 MB) |
| 35 | goldman-death | w.goldman-death-and-life-of (14 to check) | 12QU7noBGK5B9-WmeYEz0j1JQ1D_w4EgQ (10 MB) |
| 36 | muehlenbeck-betting | w.muehlenbeck-betting-on-the-africans (14 to check) | 11f54Uk9YVsypr-EP-IcTUz-eKdPRLPCZ (24 MB) |
| 37 | spiegel-other | w.spiegel-other-arab-israeli-conflict (14 to check) | 1cf7_LC_DYNeWMXRIeVNV9vlmjBrPk-wH (9 MB) |
| 38 | pair-oberdorfer-odonnell | w.oberdorfer-senator-mansfield-2003 (5 to check); w.odonnell-johnny-we-hardly-knew (9 to check) | 18qosptfjgbyOJvpxoc81bWDluTkWpfB5 (52 MB); 1_MbZCrilcsncM9PdtrgVtONk4tO9tl28 (26 MB) |
| 39 | okun-political | w.okun-political-economy-of-prosperity (13 to check) | 1Cw-2g-C7QexDJG5P8aUVFfp396GUvG8f (6 MB) |
| 40 | kahin-intervention | w.kahin-intervention (12 to check) | 1Z4H4ZXR6bMjOU8e3pmi_I3wFbrZl26rX (22 MB) |
| 41 | farmer-lay | w.farmer-lay-bare-the-heart (12 to check) | 1Fgl36mqR4VeGMclXflr6JfYmi2RSzN3a (23 MB) |
| 42 | abernathy-and | w.abernathy-and-the-walls-came (12 to check) | 1xjtMD5BkA8NK48HtpfihxTWIrLSJnJKo (47 MB) |
| 43 | persico-imperial | w.persico-imperial-rockefeller (12 to check) | 17Ghwa-vXkfRqaTP1-7-Uy54TsM8IqkXQ (24 MB) |
| 44 | pair-halberstam-kempe | w.halberstam-powers-that-be (5 to check); w.kempe-berlin-1961 (7 to check) | 1W7bwFCfKLt5jMS6d1g8GD1B5UtK-nOLN (42 MB); 15iRfNcAWy7TjIjlKI762kCk2e7x1wMO2 (26 MB) |
| 45 | coombs-arena | w.coombs-arena-of-international-finance (11 to check) | 19E3NY_VKbyATMHjX4NSO42FVSSscFML2 (12 MB) |
| 46 | berman-william | w.berman-william-fulbright-and-the (11 to check) | 1ctFpn-OpbjDr6EOLrndKNu3U_ODBraR5 (14 MB) |
| 47 | taubman-khrushchev | w.taubman-khrushchev (11 to check) | 1zVdw8LhfXHq7LAhG5a3z1cYWO91lP-7J (25 MB) |
| 48 | obrien-no | w.obrien-no-final-victories (11 to check) | 1v8WJW0lfjezt6OEM6B6bAPlrYLWdMpP5 (19 MB) |
| 49 | davies-from | w.davies-from-opportunity-to-entitlement (10 to check) | 1YB2wR8uGoCfaQKfgdf-4U-0J3skHDEy7 (16 MB) |
| 50 | bohning-castro | w.bohning-castro-obsession (10 to check) | 1Cg_SeqEn9EB8xwhaJ6io3CqJDOjJo5Sq (19 MB) |
| 51 | dallek-right | w.dallek-right-moment (10 to check) | 1cunfhaNiXWvmK78Kbr8wNcf7XOPnEo-5 (12 MB) |
| 52 | witcover-85 | w.witcover-85-days (10 to check) | 1d_R_ZkYVDewfcHVw8FRS_GaEmdNdtQuU (19 MB) |
| 53 | edwards-goldwater | w.edwards-goldwater (10 to check) | 1dopV8BB2_yht0LhpDjNpR8-rcXyymlxW (36 MB) |
| 54 | harrison-driving | w.harrison-driving-the-soviets-up (10 to check) | 1qdkFnU9EFjshJUBA1iuwhlPt5VY-euY- (2 MB) |
| 55 | pair-garbade-goldwater | w.garbade-after-the-accord (1 to check); w.goldwater-with-no-apologies (9 to check) | 1xYf4QjO7whceduc2yGvIwAUg43MGonY_ (8 MB); 1QXL9uw3Q6MpJ-ziwSw9XAYULwjBqoVHA (21 MB) |
| 56 | pair-stein-trachtenberg | w.stein-presidential-economics (1 to check); w.trachtenberg-constructed-peace (8 to check) | 1AjCJAHMIwrl2XLSEYQNKvXOjOFZeJ3v3 (26 MB); 1UotA9yg8Om4DJzTHrvjCDgzqvuLU6-Ji (11 MB) |
| 57 | pair-steinberg-baker | NEW: w.steinberg-sam-rayburn (Alfred Steinberg, *Sam Rayburn: A Biography*, 1975) (0 to check); w.baker-wheeling-and-dealing (6 to check) | 1Happ-gVQIsyGce90BJKH-qQ4hTgG1u3a (29 MB); 1BI3MROhq4uoUY2iT3l33xz4EU6HZ0jwS (30 MB) |
