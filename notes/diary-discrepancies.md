# The calendar against the President's Daily Diary

For the owner. Johnson's Daily Diary, read Oct. 23, 2026, on the days the National Archives Catalog gives with their
page images: 50 days, Nov. 22, 1963–Apr. 7, 1968 (`daybook/diary.yaml`, `tools/daybook/make_daily_diary.py`). The
whole Diary, a day an item, is on the LBJ Library's site (discoverlbj.org, `item/pdd-YYYYMMDD`), which refused this
environment (Cloudflare, 403) and whose robots.txt (Cloudflare's managed file) bars the AI crawlers by name, ClaudeBot, anthropic-ai and Claude-Web among them, and leaves other agents to its general rule (allowed: search=yes, ai-train=no, use=reference); it was not read. An image is the
page's number in the Catalog's item, not the Diary's own page number.

Checked: the 42 calendar entries of those days that record an act of Johnson's (a meeting, call, visit, signing,
address, trip). Agreed: 31, now citing the Diary (inbox patch `inbox/2026-10-23-lbj-library.yaml`). Disagreed: 4,
below; each cites the Diary too. The Diary silent: 7, not cited. One cite of another record corrected on the way.

## Disagreements

| Entry | The entry | The Diary | Other record | Ruling |
|---|---|---|---|---|
| `cal.1963-11-22.succession` | Sworn in aboard Air Force One, 2:38 p.m. | Image 9, Marie Fehmer's notes: Judge Hughes gives the oath at 2:40 p.m. (image 7: Hughes called, 2:02). | None read here for 2:38. | Records conflict. Entry kept; "Check: the Daily Diary gives the oath at 2:40 p.m. (image 9)." |
| `cal.1964-08-04.goldwater` | "Johnson calls Goldwater, 10:06 p.m." | Image 7: 6:15 p.m., the President asks the operator to reach Goldwater (Balboa Bay Club); image 9: 8:47, Goldwater on a boat; image 10: 10:06 p.m., *from* Goldwater, "returning the President's call," Newport Beach. | Miller Center catalogue, WH6408-06-4715: "Conversation with Barry Goldwater and office conversation," 10:06 p.m.; silent on who placed it. | The call was Johnson's asking, the connection Goldwater's. Entry kept; "Check: the Daily Diary gives the call at 10:06 p.m. as Goldwater's, returning the President's (image 10)." |
| `cal.1964-11-03.robert-kennedy` | "Johnson and Kennedy by telephone, 11:55 p.m." | Image 5 (Driskill Hotel, Austin): 11:52 p.m., *from* Robert F. Kennedy, NYC. | PRDE and Miller Center catalogues: 23:55, WH6411-02-6142. | Records conflict on the minute; the Diary adds that Kennedy called. Entry kept; "Check: the Daily Diary gives a call from Kennedy at 11:52 p.m. (image 5)." |
| `cal.1965-04-11.school-aid` | "Kate Deadrich Loney" | Image 3: "Mrs. Chester Loney (Miss Kate Diedrich)". | Public Papers, 1965 Pub. Papers 412, the note: "Mrs. Kate Deadrich Loney". | The entry follows the Public Papers. No change. |

## Corrected on the way

- `cal.1967-06-23.soviet-union`: the entry cited the Eisenhower call as "Conversation WH6706-01-11914"; the Miller
  Center's catalogue (`daybook/recordings/millercenter.yaml`) gives tape WH6706.02, citation 11914, June 25, 9:44 p.m.,
  and the Diary (June 25, image 15) a call to General Eisenhower at 9:44 p.m. The patch writes WH6706-02-11914.

## The Diary silent (not cited)

- `cal.1963-11-26.vietnam` (NSAM 273) and `cal.1963-11-26.economy-debt-limit` (the signing): neither in the day's two
  pages.
- `cal.1963-11-29.space` (E.O. 11129): not in the day's pages.
- `cal.1964-11-03.elections-1964`: the results, not an act; the Diary gives the day at the Ranch and Austin.
- `cal.1966-11-02.cuba` (Cuban Adjustment Act): image 20, aboard Air Force One from Elmendorf, "signed a large number
  of bills"; the act not named.
- `cal.1967-12-23.poverty` (Economic Opportunity Amendments): image 10, aboard Air Force One from Cam Ranh Bay to
  Karachi, "signed two bills"; neither named.
- `cal.1968-04-05.civil-disorders` (Proclamation 3840, E.O. 11403): image 16, 10:08 p.m., "two more decisions to make
  tonight--dealing with the 82nd Airborne being sent to Washington"; the order not named.

## Notes for open Checks (the Diary read, nothing changed)

- `cal.1963-11-24.vietnam`, `cal.1963-11-25.japan-and-korea`: the Diary names Rusk, McNamara, McCone, Lodge and Ball,
  not Bundy (FRUS does), and Ikeda at 7 p.m. at State, not Park (FRUS does): silent, not contrary.
- `cal.1968-04-05.king` ("Reynolds ... sent to Memphis (Check the day)"): image 8, 2:23 p.m., a call to "Hon. James
  Reynolds, Under Secy of Labor"; the Diary does not say what about. The Check stays.

## Not done

Every other entry of Nov. 22, 1963–Jan. 20, 1969 whose record is in the Diary: 1,154 calendar entries of the span are
tagged `name:johnson-lyndon-b`; the 1,800-odd days the Catalog does not give wait on discoverlbj.org
(`notes/leads.md`, National).
