# R27 over the rest of the China entries: the measure, Nov. 28, 2026

This note measures the work left. It changes no entry. The rule is R27 of the reader's brief, as the owner endorsed it on Nov. 21, 2026. The earlier run is the R27 redo of Nov. 25 and its audit (`notes/r27-redo-2026-11-25.md`, `notes/r27-redo-audit-2026-11-25.md`).

## What was measured

- A script read the calendar through `tools/bib/store.Series()`. It did not read `build/`.
- It took every entry whose thread is a China thread, or that has a China thread in `also:`. That is 28,645 entries. It added 115 entries in other threads whose notes cite a Chinese work. That makes 28,760 entries.
- It left out the 186 entries the earlier run settled. These are the 176 entries of the redo's patch and the entries the sweep commit 43298e8 changed. The redo's note speaks of 191; the other five are not named anywhere, so they were measured like the rest.
- The other entries: 18,355 have "Made public:". 426 have "Printed for internal circulation:". None has "Circulated in China:"; every entry with that sentence is one the earlier run settled.
- Other agents were at work in the checkout. The counts are those of the evening of Nov. 28 and will drift a little.

The kind of printing of each work came from four places. These were the cards in `works/`. They were the "Printed for internal circulation" and "Circulated in China" sentences already in the calendar. They were the witness rows marked `circulated: prc`. They were the book-check files and the earlier run's notes. A Chinese printing of 1966 to 1970 that is not a newspaper is taken to be a Red Guard or small-batch printing until someone shows otherwise.

## The kinds of fault, and how many

An entry can have more than one kind of fault. The first count is every entry with that kind. The second count is the entries for which it is the first kind in the proposed order. The second column decides the batches.

| Code | The fault | Entries with it | First kind |
| --- | --- | --- | --- |
| B | "Made public" names a printing for internal circulation, or a Red Guard printing | 6 | 6 |
| F | "Made public" gives no year ("Made public: Check") | 24 | 22 |
| F3 | "Made public" gives a year that no work in the note carries | 3 | 3 |
| E2 | A Red Guard or small-batch printing is cited, and the note has no "Circulated in China" | 211 | 209 |
| E1 | A printing for internal circulation earlier than the "Made public" year is cited, and it is not noted beside it | 220 | 196 |
| C | A Chinese work printed before the "Made public" year is cited in the same note (the 1993/1997 fault) | 995 | 865 |
| D1 | A translation printed abroad before the "Made public" year is cited; the sentence does not name each country | 19 | 3 |
| D2 | "Made public" names a translation abroad; a later Chinese printing is cited; the sentence has no "in China" | 1 | 1 |
| A2 | No "Made public"; the note cites a printing for internal circulation of the act | 72 | 72 |
| G | The note cites a printing of the act's own year or the next, so the act may have been public at the time | 62 | 52 |
| D4 | "Made public" names a work printed abroad; a later Chinese printing is cited; the sentence has no "in China" | 56 | 38 |
| D3 | A work printed abroad before the "Made public" year is cited; the sentence does not name each country | 618 | 267 |
| A4 | No "Made public"; the note rests on an archive file or a record of a conversation | 262 | 262 |
| A3 | No "Made public"; the note cites a Red Guard or small-batch printing | 191 | 191 |
| A5 | No "Made public"; the line reads as a closed meeting, a talk, an instruction or a letter | 85 | 85 |
| H | The work "Made public" rests on has an earlier edition with its own card, and the note does not cite it | 1,868 | 1,729 |
| F2 | "Made public" gives a bare year and names no work | 11,683 | not batched |

In all, 4,001 entries have at least one fault of the kinds B to H. They are the batches. The bare year (F2) is counted apart, below.

## How sure each count is

The script finds candidates. A reader decides each one. I read five to ten entries of each kind to judge how often the script is right.

- B, F and F3 are wrong by the rule's own words in every case read.
- E2 and E1 were right in four or five cases of five. A miss is usually a record of a speech that the script took for a printing.
- C was right in about four cases of five. A miss is usually an earlier work cited for a name or a title, not for the act.
- G is about even. Some of these acts were printed in the press at the time, and then "Made public" should go.
- D3 and D4 depend on a question for the owner (question 2 below). Some misses are reference books, such as a *Who's Who*, cited for a name.
- A4 was right in about two cases of three. Most are Dikötter's famine entries, which rest on provincial archive files.
- A3 was right in about one case of five. Most of these acts were done in the open, before crowds or in the press. The earlier run's note says such acts are not R27's.
- A5 was right in about one case of three.
- H is right by the owner's rulings 14(c) and 19 in every case. Each of these entries should carry the earlier edition behind "To check:" with a Check. Whether the year moves needs a reading of the earlier edition.

Of the 186 settled entries, 21 still trip the script. Eight are D4 entries that the earlier run did not write by country. Most of the others cite a record that the earlier run judged not to be a printing, or carry an open Check that the audit left on purpose. So the script raises few false alarms on work already done.

## Other kinds found

- The bare year (F2). 11,683 "Made public" sentences give a year and name no work ("Made public: 2001."). R27 says the note says where and when the act became public. In 10,071 of them, exactly one work in the note carries that year, so a script could name it. In 84, two or more works carry it. In 1,525, the year is written in the note but is no card's own year (a volume's year, or a date in a note). These need a person.
- The copyright-page marking. About 10,700 entries rest "Made public" on a mainland work whose kind of printing is not written down anywhere. R27 asks for "(marking not seen)" where the copyright page cannot be checked. Only one of these entries says so. This is settled one work at a time, not one entry at a time (the next section).
- "Made public" on an act done in public. About 700 lines with "Made public" use words such as rally, banquet, memorial or airport. Most of them are still private acts (a Politburo decision about National Day). The words alone cannot tell. The readers will see these as they go. They are not counted as a kind.

## Works left to rule on

The full table is `notes/r27/rest-works.tsv`. It lists 638 Chinese works cited in the measured entries. For 556 of them, the kind of printing is not recorded, or a copyright page was read but its marking not written down, or only a catalogue record was seen. These 556 works are cited in 11,774 entries. "Made public" rests on one of them in 10,684 entries. Sixty-five of them are cited in ten entries or more. Fourteen are cited in fifty or more:

| Work | Year | Entries citing it | "Made public" rests on it | What is recorded |
| --- | --- | --- | --- | --- |
| *Yang Shangkun riji*, first edition (`w.shangkun-yang-shangkun-riji-2`) | 2001 | 4,643 | 4,581 | Nothing. Only the 2017 edition's copyright page was read. |
| *Zhou Enlai nianpu, 1949–1976* (`w.zhou-enlai-nianpu-1949`) | 1997 | 2,043 | 1,312 | Nothing. |
| *Zhou Enlai nianpu, 1949–1976*, new edition (`w.zhou-enlai-nianpu-1949-2020`) | 2020 | 1,778 | 1,306 | The copyright page was read; its marking was not written down. |
| *Jianguo yilai Mao Zedong wengao*, revised edition (`w.jianguo-yilai-mao-zedong`) | 2023 | 1,437 | 831 | Nothing. The calendar calls it "the first open printing". |
| *Mao Zedong nianpu, 1949–1976* (`w.zedong-mao-zedong-nianpu`) | 2013 | 1,342 | 643 | Nothing. |
| *Zhou Enlai waijiao huodong dashiji* (`w.zhou-enlai-waijiao-huodong`) | 1993 | 790 | 734 | The copyright page was read; its marking was not written down. |
| *Mao Zedong zhuan*, second edition (`w.mao-zedong-zhuan`) | 2011 | 750 | 284 | The imprints of the e-book were read; no marking written down. |
| Wu Lengxi, *Shinian lunzhan* (`w.lengxi-shinian-lunzhan-1956-1966`) | 1999 | 409 | 281 | The copyright page was read; its marking was not written down. |
| *Zhonghua renmin gongheguo waijiao dashiji*, vol. II (`w.zhonghua-renmin-gongheguo-waijiao-2001`) | 2001 | 228 | 73 | The imprint is on the card; no marking written down. |
| Bo Yibo, *Ruogan zhongda juece* (`w.yibo-ruogan-zhongda-juece-yu-1991-93`) | 1991–93 | 143 | 3 | Nothing. |
| *Zhonghua renmin gongheguo waijiao dashiji*, vol. III (`w.zhonghua-renmin-gongheguo-waijiao`) | 2002 | 131 | 19 | The copyright page was read; its marking was not written down. |
| Zhang Yunsheng, *Maojiawan jishi* (`w.yunsheng-maojiawan-jishi`) | 1988 | 106 | 34 | A catalogue record with no internal mark; the copyright page not seen. |
| *Luo Ruiqing* (`w.yao-luo-ruiqing`) | 1991 | 67 | 40 | Nothing. |
| *Zhongguo gongchandang zhizheng sishinian* (`w.qibin-zhongguo-gongchandang-zhizheng-sishinian`) | 1991 | 57 | 22 | Nothing. |

Thirty further works are Chinese printings of 1966 to 1970 that the script takes to be Red Guard or small-batch printings. Their cards do not say so. The most cited is *Mao zhuxi zuixin zhishi* (`w.mao-zhuxi-zuixin-zhishi`, seven entries).

Works with no card are not in the table. These are the items behind "To check:" given only by title, such as Red Guard tabloids and provincial reports. The script judged them by their titles and years.

## How many readers

At about 60 entries each, the 4,001 entries make 66 batches, `rest-batch-a.tsv` to `rest-batch-bn.tsv`. Each row gives the id, the date, the first kind of fault in words and as a code, the other codes, and the works involved. The entries of one day are always in the same batch. So a batch for one kind also holds the other faulty entries of the same days.

- 48 batches (a to av, 2,914 entries) need a reader each.
- 18 batches (aw to bn, 1,087 entries) are the earlier-edition entries (H) of the two nianpu: aw to bg for the Zhou nianpu of 1997, bh to bn for the Zhu De nianpu of 1986. They need no reader for the default. A script can add the earlier edition behind "To check:" with its Check, as rulings 14(c) and 19 say. A reader is needed only once a copy of the earlier edition is found. Ruling 19 says the 1997 edition's vol. III is not on the Drive.
- One more reader should read the copyright pages of the fourteen works above, and write each marking down. Six of them have already been read and need only the marking written down.

By the owner's rule of Nov. 24, each first reading runs on Sonnet and each audit on Opus. So the work is about 49 Sonnet readers and as many Opus audits, plus the two scripts.

## The proposed order

1. The copyright pages of the fourteen works. This goes first because one finding of "internal circulation" would move "Made public" in thousands of entries. The readers of the batches would then be working on the wrong year.
2. Batches a to l (717 entries). These hold the days with B, F, F3 and E2. These faults are wrong by the rule's own words.
3. Batches m to r (376 entries): E1, the internal printing not noted beside "Made public".
4. Batches s to aj (1,106 entries): C, an earlier Chinese printing cited.
5. Batches ak and al (136 entries): D1, D2, A2 and G.
6. Batches am to ap (229 entries): D3 and D4, each country named.
7. Batches aq to at (213 entries): A4, archive files and records of conversations with no "Made public".
8. Batches au and av (137 entries): A3 and A5. Most of these will need no change.
9. The two scripts, last or at any time: the earlier editions behind "To check:" (H), and naming the work after a bare year (F2), if the owner agrees (question 1).

## Questions for the owner, and the default taken

These follow the rule that nothing blocks on the owner. The session should enter them in `notes/owner-rulings.md`.

1. Does a bare year ("Made public: 2001.") meet R27? Default: no. R27 says the note says where and when. A script names the work where exactly one cited work carries the year. A reader does the rest.
2. Does "each country" apply when the earlier printing abroad is a scholar's book, not a translation? Default: yes. R27 counts "a book" among the printings abroad. The audit named each country for the Lieberthal and Dickson guide of 1989 (`cal.1961-06-12.china-leadership`). The redo did not do so for the books of MacFarquhar, Teiwes and Schoenhals, so 8 settled entries are D4 by this default.
3. An act done in the open whose note cites a Red Guard printing (A3). Default: no "Made public", as the earlier run's note says. The reader checks that the act was done in the open.
