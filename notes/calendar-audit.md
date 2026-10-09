# The calendar against the brief

Written by `./bib audit-cal` (`tools/bib/calaudit.py`): the dated entries checked against the brief in
CLAUDE.md ("The calendar"). A review list: a hit is a place to look, not an error. Rerun after editing.

349 dated entries.

| Check | Entries |
|---|---|
| A person in `c` with a Part III entry missing from `Names:` | 114 |
| (of which only a President's surname: Eisenhower, Kennedy, Johnson) | 46 |
| Neither a bibliography of its own nor a `See [[id]]` back | 9 |
| No primary record linked or named | 207 |
| A primary record named but not linked | 0 |
| Threads (statements listed for review) | 36 |

## Names

Each person found in `c` by a surname that has a Part III entry, and the entries of that surname (one is
the person; several mean the surname is shared). "?" marks a surname that is also a place or a thing
(White, Byrd, Lodge as a word): look before adding.

- `cal.1961-01-03.rules` (Jan. 3, II pro.yaml): 87th Congress convenes. Senate 65 D–35 R, Hickey (D) appointed in Wyoming for Keith Thomson (R), elected and d
  - Thomson: Thomson, James C., Jr. (Viet. III.A)
  - Rayburn: Rayburn, Sam (K–J Cong. III.C)
  - Mansfield: Mansfield, Mike (K–J Cong. III.A, Cong. III.A, Viet. III.E)
  - Humphrey: Humphrey, Hubert H. (K–J Adm. III.D, K–J Cong. III.A, 1968 III.I, 1968 III.P, Cong. III.B)
  - Johnson: Johnson, Lady Bird (K–J Adm. III.A, 1968 III.Q); Johnson, Lynda Bird (K–J Adm. III.A); Johnson, Luci Baines (K–J Adm. III.A); Johnson, Lyndon B. (K–J Adm. III.D, Viet. III.A); Johnson, Paul B., Jr. (K–J Cong. III.F); Johnson, Frank M., Jr. (K–J Cong. III.G); Johnson, Tom (1968 III.A); Johnson, U. Alexis (Viet. III.C)
  - Eisenhower: Eisenhower, Dwight D. (Opp. III.E); Eisenhower, David (Adm. III.A); Eisenhower, Julie Nixon (Adm. III.A, Wg. III.A)
- `cal.1961-01-06.berlin-and-vienna` (Jan. 6, II pro.yaml): Khrushchev's speech on wars of national liberation. Kennedy reads it to his staff and quotes it to the cabinet
  - Khrushchev: Khrushchev, Nikita S. (K–J Adm. III.J)
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-01-14.economy` (Jan. 14, II pro.yaml): Eisenhower's executive order bars Americans from holding gold abroad, after the October run on the London mark
  - Eisenhower: Eisenhower, Dwight D. (Opp. III.E); Eisenhower, David (Adm. III.A); Eisenhower, Julie Nixon (Adm. III.A, Wg. III.A)
- `cal.1961-01-17.congo` (Jan. 17, II pro.yaml): Lumumba killed in Katanga. Not announced until Feb. 13. Eisenhower's farewell address the same day.
  - Eisenhower: Eisenhower, Dwight D. (Opp. III.E); Eisenhower, David (Adm. III.A); Eisenhower, Julie Nixon (Adm. III.A, Wg. III.A)
- `cal.1961-01-18.economy` (Jan. 18, II pro.yaml): Eisenhower's last Economic Report, two days after his last budget. Neither proposes measures against the reces
  - Eisenhower: Eisenhower, Dwight D. (Opp. III.E); Eisenhower, David (Adm. III.A); Eisenhower, Julie Nixon (Adm. III.A, Wg. III.A)
- `cal.1961-01-19.laos` (Jan. 19, II pro.yaml): Eisenhower–Kennedy transition meeting. Laos called the key to Southeast Asia; accounts of what Eisenhower advi
  - Eisenhower: Eisenhower, Dwight D. (Opp. III.E); Eisenhower, David (Adm. III.A); Eisenhower, Julie Nixon (Adm. III.A, Wg. III.A)
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-01-20.transition-and-staff` (Jan. 20, III jan.yaml): Inauguration. The cabinet confirmed and sworn in over two days: Rusk, Dillon, McNamara, Robert Kennedy, Day, U
  - Rusk: Rusk, Dean (K–J Adm. III.E, 1968 III.E, Viet. III.A)
  - Dillon: Dillon, C. Douglas (K–J Adm. III.H)
  - McNamara: McNamara, Robert S. (K–J Adm. III.F, Viet. III.A)
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
  - ? Day: Day, J. Edward (K–J Adm. III.G)
  - Udall: Udall, Stewart L. (K–J Adm. III.G); Udall, Morris K. (K–J Cong. III.D)
  - Freeman: Freeman, Orville L. (K–J Adm. III.G)
  - Hodges: Hodges, Luther H. (K–J Adm. III.G)
  - Goldberg: Goldberg, Arthur J. (K–J Adm. III.E, K–J Adm. III.G, K–J Cong. III.G)
  - Ribicoff: Ribicoff, Abraham A. (K–J Adm. III.G); Ribicoff, Abraham (1968 III.N)
  - Stevenson: Stevenson, Adlai E. (K–J Adm. III.E); Stevenson, Adlai E., III (Cong. III.B)
  - McGovern: McGovern, George (K–J Cong. III.B, Cong. III.B)
- `cal.1961-01-28.vietnam` (Jan. 28, III jan.yaml): Kennedy approves the Counterinsurgency Plan for Vietnam after reading Lansdale's report. More aid for a larger
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
  - Lansdale: Lansdale, Edward G. (K–J Adm. III.F, Viet. III.C)
- `cal.1961-02-06.defense` (Feb. 6, IV feb.yaml): McNamara tells reporters on background there is no missile gap. The story runs; the White House says no conclu
  - McNamara: McNamara, Robert S. (K–J Adm. III.F, Viet. III.A)
- `cal.1961-02-09.medicare` (Feb. 9, IV feb.yaml): Health message: hospital insurance for the aged through Social Security. King–Anderson bill introduced soon af
  - ? King: King, Martin Luther, Jr. (K–J Cong. III.H, Viet. III.E)
- `cal.1961-02-09.civil-rights-the-executive` (Feb. 9, IV feb.yaml): Senate confirms Robert C. Weaver as Housing and Home Finance administrator over southern objection.
  - Weaver: Weaver, Robert C. (K–J Adm. III.G)
- `cal.1961-02-13.congo` (Feb. 13, IV feb.yaml): Katanga announces Lumumba's death. Feb. 15: demonstrators break up the Security Council during Stevenson's fir
  - Stevenson: Stevenson, Adlai E. (K–J Adm. III.E); Stevenson, Adlai E., III (Cong. III.B)
- `cal.1961-02-18.transition-and-staff` (Feb. 18, IV feb.yaml): Executive order abolishes Eisenhower's Operations Coordinating Board. National security policy moves into Bund
  - Eisenhower: Eisenhower, Dwight D. (Opp. III.E); Eisenhower, David (Adm. III.A); Eisenhower, Julie Nixon (Adm. III.A, Wg. III.A)
- `cal.1961-03-06.civil-rights-the-executive` (Mar. 6, V mar.yaml): Executive order creates the President's Committee on Equal Employment Opportunity. Johnson chairs it. Contract
  - Johnson: Johnson, Lady Bird (K–J Adm. III.A, 1968 III.Q); Johnson, Lynda Bird (K–J Adm. III.A); Johnson, Luci Baines (K–J Adm. III.A); Johnson, Lyndon B. (K–J Adm. III.D, Viet. III.A); Johnson, Paul B., Jr. (K–J Cong. III.F); Johnson, Frank M., Jr. (K–J Cong. III.G); Johnson, Tom (1968 III.A); Johnson, U. Alexis (Viet. III.C)
- `cal.1961-03-17.economy` (Mar. 17, V mar.yaml): Heller to the President: even if the whole program passes, output at year's end will be some $40 billion below
  - Heller: Heller, Walter W. (K–J Adm. III.H)
- `cal.1961-03-24.economy` (Mar. 24, V mar.yaml): Special message on budget and fiscal policy: the recession and the new requests turn Eisenhower's projected su
  - Eisenhower: Eisenhower, Dwight D. (Opp. III.E); Eisenhower, David (Adm. III.A); Eisenhower, Julie Nixon (Adm. III.A, Wg. III.A)
- `cal.1961-04-03.states-and-cities` (Apr. 3, VI apr.yaml): Michigan voters approve a constitutional convention. Romney leads Citizens for Michigan.
  - Romney: Romney, George W. (Opp. III.H, Adm. III.F)
- `cal.1961-04-04.states-and-cities` (Apr. 4, VI apr.yaml): Texas special election for Johnson's seat. Seventy-one candidates; Tower first, Blakley second. Runoff set.
  - Johnson: Johnson, Lady Bird (K–J Adm. III.A, 1968 III.Q); Johnson, Lynda Bird (K–J Adm. III.A); Johnson, Luci Baines (K–J Adm. III.A); Johnson, Lyndon B. (K–J Adm. III.D, Viet. III.A); Johnson, Paul B., Jr. (K–J Cong. III.F); Johnson, Frank M., Jr. (K–J Cong. III.G); Johnson, Tom (1968 III.A); Johnson, U. Alexis (Viet. III.C)
  - Tower: Tower, John G. (K–J Cong. III.E, Opp. III.B, Cong. III.C)
  - Blakley: Blakley, William A. (K–J Cong. III.B)
- `cal.1961-04-04.cuba` (Apr. 4, VI apr.yaml): State Department meeting on the invasion plan. Fulbright, invited, argues against it. The plan goes ahead.
  - Fulbright: Fulbright, J. William (K–J Cong. III.B, Cong. III.B, Viet. III.E)
- `cal.1961-04-17.court` (Apr. 17, VI apr.yaml): *Burton v. Wilmington Parking Authority*, [365 U.S. 715](https://tile.loc.gov/storage-services/service/ll/usre
  - Burton: Burton, Phillip (Cong. III.E)
- `cal.1961-04-19.court` (Apr. 19–20, VI apr.yaml): *Baker v. Carr* argued.
  - ? Baker: Baker, Ella (K–J Cong. III.H); Baker, Howard H., Jr. (Cong. III.C, Wg. III.F)
- `cal.1961-04-20.cuba` (Apr. 20, VI apr.yaml): Address to the newspaper editors: the lessons of Cuba, and no retreat. Same day Kennedy asks Johnson, as Space
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
  - Johnson: Johnson, Lady Bird (K–J Adm. III.A, 1968 III.Q); Johnson, Lynda Bird (K–J Adm. III.A); Johnson, Luci Baines (K–J Adm. III.A); Johnson, Lyndon B. (K–J Adm. III.D, Viet. III.A); Johnson, Paul B., Jr. (K–J Cong. III.F); Johnson, Frank M., Jr. (K–J Cong. III.G); Johnson, Tom (1968 III.A); Johnson, U. Alexis (Viet. III.C)
- `cal.1961-04-21.cuba` (Apr. 21, VI apr.yaml): Press conference: Kennedy takes responsibility. "Victory has a hundred fathers." His approval rises.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-04-22.cuba` (Apr. 22, VI apr.yaml): Kennedy meets Eisenhower at Camp David. The Cuba Study Group formed: Taylor, Robert Kennedy, Dulles, Burke.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
  - Eisenhower: Eisenhower, Dwight D. (Opp. III.E); Eisenhower, David (Adm. III.A); Eisenhower, Julie Nixon (Adm. III.A, Wg. III.A)
  - Taylor: Taylor, Maxwell D. (K–J Adm. III.F, Viet. III.A); Taylor, Maxwell (1968 III.F)
  - Dulles: Dulles, Allen W. (K–J Adm. III.I)
  - Burke: Burke, Arleigh A. (K–J Adm. III.F)
- `cal.1961-04-25.space` (Apr. 25, VI apr.yaml): Statute makes the Vice President chairman of the Space Council. Johnson's memorandum of Apr. 28 recommends the
  - Johnson: Johnson, Lady Bird (K–J Adm. III.A, 1968 III.Q); Johnson, Lynda Bird (K–J Adm. III.A); Johnson, Luci Baines (K–J Adm. III.A); Johnson, Lyndon B. (K–J Adm. III.D, Viet. III.A); Johnson, Paul B., Jr. (K–J Cong. III.F); Johnson, Frank M., Jr. (K–J Cong. III.G); Johnson, Tom (1968 III.A); Johnson, U. Alexis (Viet. III.C)
- `cal.1961-05-01.program` (May 1, VII may.yaml): Area Redevelopment Act signed. Douglas's bill, twice vetoed by Eisenhower.
  - Eisenhower: Eisenhower, Dwight D. (Opp. III.E); Eisenhower, David (Adm. III.A); Eisenhower, Julie Nixon (Adm. III.A, Wg. III.A)
- `cal.1961-05-01.court` (May 1, VII may.yaml): *Baker v. Carr* restored to the calendar for reargument.
  - ? Baker: Baker, Ella (K–J Cong. III.H); Baker, Howard H., Jr. (Cong. III.C, Wg. III.F)
- `cal.1961-05-09.berlin-and-vienna` (May 9, VII may.yaml): Robert Kennedy's first meeting with Georgi Bolshakov. The back channel to Khrushchev opens.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
  - Khrushchev: Khrushchev, Nikita S. (K–J Adm. III.J)
- `cal.1961-05-09.vietnam` (May 9–24, VII may.yaml): Johnson's trip to Saigon, Manila, Taipei, Bangkok, New Delhi, Karachi. In Saigon he calls Diem the Churchill o
  - Johnson: Johnson, Lady Bird (K–J Adm. III.A, 1968 III.Q); Johnson, Lynda Bird (K–J Adm. III.A); Johnson, Luci Baines (K–J Adm. III.A); Johnson, Lyndon B. (K–J Adm. III.D, Viet. III.A); Johnson, Paul B., Jr. (K–J Cong. III.F); Johnson, Frank M., Jr. (K–J Cong. III.G); Johnson, Tom (1968 III.A); Johnson, U. Alexis (Viet. III.C)
- `cal.1961-05-14.freedom-rides` (May 14, VII may.yaml): Mother's Day. The Greyhound bus burned outside Anniston; the Trailways riders beaten at the Birmingham termina
  - ? Day: Day, J. Edward (K–J Adm. III.G)
- `cal.1961-05-16.laos` (May 16, VII may.yaml): The Geneva conference on Laos opens. Harriman leads the delegation.
  - Harriman: Harriman, W. Averell (K–J Adm. III.E, 1968 III.F, Viet. III.A)
- `cal.1961-05-16.transition-and-staff` (May 16, VII may.yaml): Ottawa. Kennedy injures his back at a tree planting; the pain and its treatment follow him to Vienna.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-05-19.civil-rights-the-executive` (May 19, VII may.yaml): Omnibus judgeship act signed: seventy-three new federal judgeships for Kennedy to fill, many in the South.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-05-20.freedom-rides` (May 20, VII may.yaml): Montgomery. The Nashville riders beaten at the Greyhound station; Seigenthaler clubbed unconscious. Byron Whit
  - Seigenthaler: Seigenthaler, John (K–J Adm. III.I)
  - ? White: White, Lee C. (K–J Adm. III.B); White, Byron R. (K–J Adm. III.I, K–J Cong. III.G); White, F. Clifton (Opp. III.F); White, Theodore H. (Opp. III.J, 1968 III.O)
- `cal.1961-05-21.freedom-rides` (May 21, VII may.yaml): Mob besieges King, Abernathy, and the riders in the First Baptist Church; marshals hold it until Patterson sen
  - ? King: King, Martin Luther, Jr. (K–J Cong. III.H, Viet. III.E)
  - ? Church: Church, Frank (K–J Cong. III.B, Cong. III.B, Viet. III.E)
  - Patterson: Patterson, John (K–J Cong. III.F)
- `cal.1961-05-24.freedom-rides` (May 24, VII may.yaml): Riders go on to Jackson under Guard escort and are arrested on arrival; many to Parchman. Robert Kennedy calls
  - ? Jackson: Jackson, Henry M. (K–J Cong. III.B, Cong. III.B)
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-05-27.states-and-cities` (May 27, VII may.yaml): Tower beats Blakley in the runoff by about ten thousand votes. The first Republican senator elected from the f
  - Johnson: Johnson, Lady Bird (K–J Adm. III.A, 1968 III.Q); Johnson, Lynda Bird (K–J Adm. III.A); Johnson, Luci Baines (K–J Adm. III.A); Johnson, Lyndon B. (K–J Adm. III.D, Viet. III.A); Johnson, Paul B., Jr. (K–J Cong. III.F); Johnson, Frank M., Jr. (K–J Cong. III.G); Johnson, Tom (1968 III.A); Johnson, U. Alexis (Viet. III.C)
- `cal.1961-05-28.opinion` (May 28–June 2, VII may.yaml): Gallup on the Freedom Riders: of those who knew who they were, 61 percent disapprove. 57 percent think sit-ins
  - Gallup: Gallup, George H. (K–J Cong. III.J)
- `cal.1961-05-29.freedom-rides` (May 29, VII may.yaml): Robert Kennedy petitions the Interstate Commerce Commission to forbid segregation in interstate bus terminals.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-05-31.berlin-and-vienna` (May 31–June 2, VII may.yaml): Paris. De Gaulle advises firmness on Berlin. "I am the man who accompanied Jacqueline Kennedy to Paris."
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-06-03.berlin-and-vienna` (June 3–4, VIII jun.yaml): Vienna summit. Khrushchev hands over an aide-mémoire: a German peace treaty within six months, and an end to W
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
  - Reston: Reston, James (K–J Cong. III.J)
- `cal.1961-06-05.berlin-and-vienna` (June 5, VIII jun.yaml): London. Macmillan.
  - Macmillan: Macmillan, Harold (K–J Adm. III.J)
- `cal.1961-06-05.court` (June 5, VIII jun.yaml): *Communist Party v. SACB*, [367 U.S. 1](https://tile.loc.gov/storage-services/service/ll/usrep/usrep367/usrep3
  - Smith: Smith, Stephen E. (K–J Adm. III.A); Smith, Howard W. (K–J Cong. III.D); Smith, Margaret Chase (Opp. III.A, Cong. III.A); Smith, Gerard C. (Adm. III.D)
- `cal.1961-06-12.right-and-the-military` (June 12, VIII jun.yaml): Walker admonished; his program found improper. He resigns [[cal.1961-11-02.right-and-the-military]].
  - Walker: Walker, Edwin A. (K–J Adm. III.F)
- `cal.1961-06-15.berlin-and-vienna` (June 15, VIII jun.yaml): Khrushchev repeats the deadline on Soviet television. Tower sworn in.
  - Khrushchev: Khrushchev, Nikita S. (K–J Adm. III.J)
  - Tower: Tower, John G. (K–J Cong. III.E, Opp. III.B, Cong. III.C)
- `cal.1961-06-26.transition-and-staff` (June 26, VIII jun.yaml): Taylor named Military Representative of the President, from July 1. A general between Kennedy and the Joint Ch
  - Taylor: Taylor, Maxwell D. (K–J Adm. III.F, Viet. III.A); Taylor, Maxwell (1968 III.F)
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-06.civil-rights-the-executive` (June, VIII jun.yaml): W. Harold Cox, Eastland's college roommate, appointed to the Southern District of Mississippi; the first Kenne
  - Eastland: Eastland, James O. (K–J Cong. III.B)
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-07-25.economy` (July 25, IX jul.yaml): The Berlin requests come without new taxes. A temporary tax increase to pay for them, which Kennedy had favore
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
  - Heller: Heller, Walter W. (K–J Adm. III.H)
  - Samuelson: Samuelson, Paul A. (K–J Adm. III.H)
- `cal.1961-08-02.right-and-the-military` (Aug. 2, X aug.yaml): Fulbright's memorandum to McNamara on military officers propagandizing for the radical right, written in June,
  - Fulbright: Fulbright, J. William (K–J Cong. III.B, Cong. III.B, Viet. III.E)
  - McNamara: McNamara, Robert S. (K–J Adm. III.F, Viet. III.A)
  - Thurmond: Thurmond, Strom (K–J Cong. III.B, Opp. III.B, Cong. III.C)
- `cal.1961-08-03.crime-and-hijacking` (Aug. 3, X aug.yaml): A Continental Air Lines 707 seized at El Paso; Kennedy follows from the White House; the FBI and Border Patrol
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-08-13.berlin-and-vienna` (Aug. 13, X aug.yaml): East Germany seals the sector border overnight. Kennedy at Hyannis Port. The response is a protest.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-08-16.berlin-and-vienna` (Aug. 16, X aug.yaml): Brandt's letter to Kennedy; three hundred thousand at the city hall rally.
  - Brandt: Brandt, Willy (K–J Adm. III.J)
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-08-19.berlin-and-vienna` (Aug. 19–20, X aug.yaml): Johnson and Clay in Berlin. A battle group of the 18th Infantry drives up the autobahn and is received by John
  - Johnson: Johnson, Lady Bird (K–J Adm. III.A, 1968 III.Q); Johnson, Lynda Bird (K–J Adm. III.A); Johnson, Luci Baines (K–J Adm. III.A); Johnson, Lyndon B. (K–J Adm. III.D, Viet. III.A); Johnson, Paul B., Jr. (K–J Cong. III.F); Johnson, Frank M., Jr. (K–J Cong. III.G); Johnson, Tom (1968 III.A); Johnson, U. Alexis (Viet. III.C)
- `cal.1961-08-30.states-and-cities` (Aug. 30, X aug.yaml): Atlanta desegregates four high schools with nine Black students, peacefully. Kennedy praises the city at that 
  - ? Black: Black, Hugo L. (K–J Cong. III.G)
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-08-31.rules` (Aug. 31, X aug.yaml): Rayburn leaves Washington for Bonham, ill. He does not return. McCormack presides. Check the date.
  - Rayburn: Rayburn, Sam (K–J Cong. III.C)
  - McCormack: McCormack, John W. (K–J Cong. III.C, Cong. III.D)
- `cal.1961-09-05.testing` (Sept. 5, XI sep.yaml): Kennedy orders U.S. testing resumed, underground and in the laboratory.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-09-06.steel` (Sept. 6, XI sep.yaml): Kennedy writes the heads of twelve steel companies asking them to hold prices when the October wage step comes
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-09-12.states-and-cities` (Sept. 12, XI sep.yaml): Michigan elects its convention delegates. Romney among them.
  - Romney: Romney, George W. (Opp. III.H, Adm. III.F)
- `cal.1961-09-13.crime-and-hijacking` (Sept. 13, XI sep.yaml): Robert Kennedy's organized-crime bills signed: the Wire Act, the Travel Act, and the wagering-paraphernalia ac
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-09-19.space` (Sept. 19, XI sep.yaml): NASA names Houston for the Manned Spacecraft Center. Albert Thomas held NASA's appropriations.
  - Albert: Albert, Carl (K–J Cong. III.C, Cong. III.D)
- `cal.1961-09-21.program` (Sept. 21, XI sep.yaml): Mutual Educational and Cultural Exchange Act signed: the Fulbright–Hays Act.
  - Fulbright: Fulbright, J. William (K–J Cong. III.B, Cong. III.B, Viet. III.E)
  - Hays: Hays, Wayne L. (Cong. III.E)
- `cal.1961-09-22.peace-corps` (Sept. 22, XI sep.yaml): Peace Corps Act signed. Juvenile delinquency act signed the same day, Robert Kennedy's committee behind it.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-09-23.civil-rights-the-executive` (Sept. 23, XI sep.yaml): Thurgood Marshall nominated to the Second Circuit; recess-appointed in October. Eastland's subcommittee holds 
  - Eastland: Eastland, James O. (K–J Cong. III.B)
- `cal.1961-09-25.mississippi` (Sept. 25, XI sep.yaml): Herbert Lee, a farmer working with Moses, shot dead at the Liberty cotton gin by state representative E.H. Hur
  - Lee: Lee, Richard C. (K–J Cong. III.F)
  - Moses: Moses, Robert P. (K–J Cong. III.H)
- `cal.1961-10-09.court` (Oct. 9, XII oct.yaml): *Baker v. Carr* reargued. Cox for the United States as amicus.
  - ? Baker: Baker, Ella (K–J Cong. III.H); Baker, Howard H., Jr. (Cong. III.C, Wg. III.F)
- `cal.1961-10-16.right-and-the-military` (Oct. 16, XII oct.yaml): Schwarz's Christian Anti-Communism Crusade fills the Hollywood Bowl, televised.
  - ? Christian: Christian, George (K–J Adm. III.C, 1968 III.A)
- `cal.1961-10-18.vietnam` (Oct. 18, XII oct.yaml): Taylor and Rostow in Saigon. Diem declares a state of emergency. Mekong floods.
  - Taylor: Taylor, Maxwell D. (K–J Adm. III.F, Viet. III.A); Taylor, Maxwell (1968 III.F)
  - Rostow: Rostow, Walt W. (K–J Adm. III.E, 1968 III.E, Viet. III.A); Rostow, Eugene (1968 III.F)
- `cal.1961-11-02.testing` (Nov. 2, XIII nov.yaml): Kennedy orders preparations for atmospheric tests.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-11-04.specials` (Nov. 4, XIII nov.yaml): Texas 20th, special. Henry B. González (D) over Goode (R), 54.6 to 44.0, for Kilday's seat. The first Mexican 
  - González: González, Virgilio R. (Wg. III.C)
- `cal.1961-11-07.states-and-cities` (Nov. 7, XIII nov.yaml): Wagner reelected mayor of New York. In New Jersey Hughes (D) beats Mitchell, Eisenhower's Labor Secretary, for
  - Hughes: Hughes, Harold E. (K–J Cong. III.F, Cong. III.B); Hughes, Emmet John (Opp. III.G)
  - Mitchell: Mitchell, Clarence, Jr. (K–J Cong. III.H); Mitchell, John N. (Adm. III.H, Wg. III.B); Mitchell, Martha (Wg. III.B)
  - Eisenhower: Eisenhower, Dwight D. (Opp. III.E); Eisenhower, David (Adm. III.A); Eisenhower, Julie Nixon (Adm. III.A, Wg. III.A)
- `cal.1961-11-08.vietnam` (Nov. 8–11, XIII nov.yaml): McNamara, Gilpatric, and the Chiefs advise a commitment, with troops; up to six divisions. Nov. 11: McNamara a
  - Gilpatric: Gilpatric, Roswell L. (K–J Adm. III.F, Viet. III.A)
- `cal.1961-11-16.congress` (Nov. 16, XIII nov.yaml): Rayburn dies at Bonham. Kennedy, Johnson, Truman, and Eisenhower at the funeral.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
  - Johnson: Johnson, Lady Bird (K–J Adm. III.A, 1968 III.Q); Johnson, Lynda Bird (K–J Adm. III.A); Johnson, Luci Baines (K–J Adm. III.A); Johnson, Lyndon B. (K–J Adm. III.D, Viet. III.A); Johnson, Paul B., Jr. (K–J Cong. III.F); Johnson, Frank M., Jr. (K–J Cong. III.G); Johnson, Tom (1968 III.A); Johnson, U. Alexis (Viet. III.C)
  - Eisenhower: Eisenhower, Dwight D. (Opp. III.E); Eisenhower, David (Adm. III.A); Eisenhower, Julie Nixon (Adm. III.A, Wg. III.A)
- `cal.1961-11-17.albany` (Nov. 17, XIII nov.yaml): Albany Movement formed: SNCC, the NAACP, the ministers. William G. Anderson president.
  - Anderson: Anderson, George W., Jr. (K–J Adm. III.F); Anderson, Clinton P. (K–J Cong. III.B); Anderson, John B. (Opp. III.D, Cong. III.D); Anderson, Jack (Cong. III.M, Wg. III.H)
- `cal.1961-11-19.latin-america` (Nov. 19, XIII nov.yaml): American warships off Santo Domingo. The Trujillo brothers leave.
  - Trujillo: Trujillo, Rafael (K–J Adm. III.J)
- `cal.1961-11-25.berlin-and-vienna` (Nov. 25, XIII nov.yaml): Adzhubei, Khrushchev's son-in-law, interviews Kennedy at Hyannis Port. *Izvestia* prints it whole, Nov. 28.
  - Khrushchev: Khrushchev, Nikita S. (K–J Adm. III.J)
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-11-28.transition-and-staff` (Nov. 28, XIII nov.yaml): Kennedy at Langley; the National Security Medal for Dulles. McCone sworn in, Nov. 29.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-12-15.vietnam` (Dec. 15, XIV dec.yaml): Diem's request and Kennedy's pledge of more aid published.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-12-16.latin-america` (Dec. 16–17, XIV dec.yaml): Kennedy in Caracas and Bogotá.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1961-12-21.europe-and-the-alliance` (Dec. 21–22, XIV dec.yaml): Kennedy and Macmillan at Bermuda. Testing, Berlin, Britain's Common Market application.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-01-24.program` (Jan. 24, XV jan62.yaml): House Rules Committee kills the Urban Affairs department, 9–6. Kennedy names Weaver its secretary-to-be and se
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-02-10.berlin-and-vienna` (Feb. 10, XVI feb62.yaml): Powers exchanged for Abel on the Glienicke Bridge; Pryor freed at Checkpoint Charlie. Donovan negotiated.
  - Powers: Powers, David F. (K–J Adm. III.B)
- `cal.1962-02-20.specials` (Feb. 20, XVI feb62.yaml): New York 6th, special. Benjamin Rosenthal (D) holds Lester Holtzman's seat, 44.5 to 43.8 over Galvin (R). Swin
  - Holtzman: Holtzman, Elizabeth (Cong. III.E, Wg. III.G)
- `cal.1962-03-13.cuba` (Mar. 13, XVII mar62.yaml): The Joint Chiefs send McNamara Operation Northwoods: pretexts for invasion, staged attacks among them. Lemnitz
  - McNamara: McNamara, Robert S. (K–J Adm. III.F, Viet. III.A)
- `cal.1962-03-21.defense` (Mar. 21, XVII mar62.yaml): The RS-70. Vinson's bill would "direct" bomber spending; after a Rose Garden walk with Kennedy, "authorize."
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-03-22.transition-and-staff` (Mar. 22, XVII mar62.yaml): Hoover lunches with Kennedy. The Bureau knows of Judith Campbell and Giancana. Her calls to the White House en
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-03-26.court` (Mar. 26, XVII mar62.yaml): *Baker v. Carr*, 369 U.S. 186. Apportionment justiciable. Brennan for six; Frankfurter and Harlan dissent.
  - ? Baker: Baker, Ella (K–J Cong. III.H); Baker, Howard H., Jr. (Cong. III.C, Wg. III.F)
- `cal.1962-04-04.vietnam` (Apr. 4, XVIII apr62.yaml): Galbraith from New Delhi: seek a neutral settlement, through Harriman. Kennedy sends it to McNamara; the Chief
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
  - McNamara: McNamara, Robert S. (K–J Adm. III.F, Viet. III.A)
- `cal.1962-04-10.specials` (Apr. 10, XVIII apr62.yaml): South Carolina 2d, special. Corinne Boyd Riley (D), unopposed, to her husband's seat. No swing: Riley unoppose
  - Boyd: Boyd, Alan S. (K–J Adm. III.G)
- `cal.1962-04-29.press-and-broadcasting` (Apr. 29, XVIII apr62.yaml): Dinner for the Nobel laureates. "With the possible exception of when Thomas Jefferson dined alone."
  - Thomas: Thomas, Albert (K–J Cong. III.D)
- `cal.1962-05-24.space` (May 24, XIX may62.yaml): Carpenter's *Aurora 7* lands 250 miles off target.
  - ? Carpenter: Carpenter, Liz (1968 III.A)
- `cal.1962-06-29.latin-america` (June 29–July 1, XX jun62.yaml): Kennedy in Mexico City.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-07-10.space` (July 10, XXI jul62.yaml): Telstar launched. July 23: first live transatlantic television, Kennedy's press conference among it.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-07-17.medicare` (July 17, XXI jul62.yaml): Senate tables the Anderson–Javits amendment, [52–48](https://voteview.com/rollcall/RS0870297). Randolph with t
  - Randolph: Randolph, A. Philip (K–J Cong. III.H)
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-07-27.albany` (July 27, XXI jul62.yaml): King arrested at a City Hall prayer vigil.
  - ? King: King, Martin Luther, Jr. (K–J Cong. III.H, Viet. III.E)
- `cal.1962-07.missile-crisis` (July, XXI jul62.yaml): Raúl Castro in Moscow. Defense agreement initialed. Soviet shipping to Cuba begins. Check the initialing.
  - Castro: Castro, Fidel (K–J Adm. III.J)
- `cal.1962-08-10.albany` (Aug. 10, XXII aug62.yaml): King leaves Albany. Parks and library closed rather than integrated. King later: the mistake was attacking seg
  - ? King: King, Martin Luther, Jr. (K–J Cong. III.H, Viet. III.E)
- `cal.1962-08-22.missile-crisis` (Aug. 22–23, XXII aug62.yaml): McCone warns Kennedy the shipments may include offensive missiles. Aug. 23: NSAM 181, contingency planning.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-08-27.elections-1962` (Aug. 27, XXII aug62.yaml): Edward Kennedy and McCormack debate in South Boston. "If his name was Edward Moore, with his qualifications . 
  - Moore: Moore, Harold G. (Viet. III.D)
- `cal.1962-09-04.missile-crisis` (Sept. 4, XXIII sep62.yaml): Statement on Cuba. No offensive weapons found; were there, "the gravest issues would arise." Dobrynin assures 
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-09-07.missile-crisis` (Sept. 7, XXIII sep62.yaml): Kennedy asks standby authority to call 150,000 reservists.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-09-10.mississippi` (Sept. 10–13, XXIII sep62.yaml): Black, as circuit justice, vacates Cameron's stays. Sept. 13: Barnett proclaims interposition.
  - Cameron: Cameron, Ben F. (K–J Cong. III.G)
- `cal.1962-09-18.elections-1962` (Sept. 18, XXIII sep62.yaml): Massachusetts primary. Edward Kennedy over McCormack, better than two to one. George Cabot Lodge the Republica
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
  - McCormack: McCormack, John W. (K–J Cong. III.C, Cong. III.D)
  - ? Lodge: Lodge, Henry Cabot (K–J Adm. III.E, Viet. III.C)
- `cal.1962-09-20.mississippi` (Sept. 20–26, XXIII sep62.yaml): Barnett, as special registrar, refuses Meredith at Oxford. Again at Jackson, Sept. 25. Lieutenant Governor Joh
  - ? Jackson: Jackson, Henry M. (K–J Cong. III.B, Cong. III.B)
- `cal.1962-10-16.missile-crisis` (Oct. 16, XXIV oct62.yaml): Bundy tells Kennedy at breakfast. First ExComm meeting, 11:50 a.m., taped. Air strike, invasion, blockade.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-10-18.missile-crisis` (Oct. 18, XXIV oct62.yaml): Gromyko at the White House: Soviet aid to Cuba defensive. Kennedy does not show the photographs.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-10-20.missile-crisis` (Oct. 20, XXIV oct62.yaml): Kennedy leaves Chicago with a "cold." Quarantine chosen over air strike.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-10-27.missile-crisis` (Oct. 27, XXIV oct62.yaml): Black Saturday. Second letter, broadcast: the Jupiters in Turkey added. Anderson's U-2 shot down over Cuba; an
  - ? Black: Black, Hugo L. (K–J Cong. III.G)
  - Anderson: Anderson, George W., Jr. (K–J Adm. III.F); Anderson, Clinton P. (K–J Cong. III.B); Anderson, John B. (Opp. III.D, Cong. III.D); Anderson, Jack (Cong. III.M, Wg. III.H)
- `cal.1962-11-02.missile-crisis` (Nov. 2, XXV nov62.yaml): Kennedy reports the bases being dismantled. Mikoyan in Havana three weeks: inspection, the IL-28s.
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-11-06.elections-1962` (Nov. 6, XXV nov62.yaml): Midterms. Democrats lose a few House seats, gain in the Senate. Brown beats Nixon. Romney, Scranton, Rockefell
  - Nixon: Nixon, Richard M. (Opp. III.E, 1968 III.M, Wg. III.A, Viet. III.B); Nixon, Pat (Adm. III.A)
  - Bayh: Bayh, Birch (Cong. III.B)
- `cal.1962-11-20.missile-crisis` (Nov. 20, XXV nov62.yaml): Khrushchev agrees to remove the IL-28s. Quarantine lifted, at the press conference.
  - Khrushchev: Khrushchev, Nikita S. (K–J Adm. III.J)
- `cal.1962-11-21.space` (Nov. 21, XXV nov62.yaml): Kennedy and Webb, Cabinet Room, taped. The moon first. "I'm not that interested in space."
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-12.missile-crisis` (Dec., XXVI dec62.yaml): Alsop and Bartlett, *Saturday Evening Post*, Dec. 8: Stevenson "wanted a Munich." Bartlett a Kennedy friend. S
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-12-26.vietnam` (Dec. 26, XXVI dec62.yaml): Mansfield reports to Kennedy at Palm Beach. The war not being won; more Americans make it an American war. Che
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)
- `cal.1962-12-29.cuba` (Dec. 29, XXVI dec62.yaml): Orange Bowl. Kennedy takes the brigade's flag: "This flag will be returned to this brigade in a free Havana."
  - Kennedy: Kennedy, Jacqueline (K–J Adm. III.A); Kennedy, Joseph P. (K–J Adm. III.A); Kennedy, Robert F. (K–J Adm. III.A, K–J Cong. III.B, 1968 III.K); Kennedy, Edward M. (K–J Cong. III.B, 1968 III.K, 1968 III.P, Cong. III.A); Kennedy, John F. (Viet. III.A)

## Event

No work of its own and no `See [[id]]` back to the event's first entry.

- `cal.1961-01-30.program` (Jan. 30, III jan.yaml): First State of the Union. The tide running against the United States in every area of crisis; the economy in r
- `cal.1961-03-22.program` (Mar. 22, V mar.yaml): Emergency feed grain program signed.
- `cal.1961-03-24.program` (Mar. 24, V mar.yaml): House adopts the weaker Ayres–Kitchin minimum wage substitute, [216–203](https://voteview.com/rollcall/RH08700
- `cal.1961-04-27.press-and-broadcasting` (Apr. 27, VI apr.yaml): Address to the newspaper publishers in New York: a call for self-restraint in a cold war. The press reads it a
- `cal.1961-05-01.crime-and-hijacking` (May 1, VII may.yaml): First U.S. airliner hijacked to Cuba, a National Airlines flight bound for Key West.
- `cal.1961-06-06.berlin-and-vienna` (June 6, VIII jun.yaml): Report to the nation on Vienna. "A very sober two days."
- `cal.1961-08-01.berlin-and-vienna` (Aug. 1, X aug.yaml): Congress authorizes the call-up of up to 250,000 reservists for a year.
- `cal.1961-09-05.crime-and-hijacking` (Sept. 5, XI sep.yaml): Aircraft piracy made a federal crime.
- `cal.1961-09-21.program` (Sept. 21, XI sep.yaml): Mutual Educational and Cultural Exchange Act signed: the Fulbright–Hays Act.

## Primary record

### None linked or named

Some events have none (a speech outside the Public Papers, a march, a strike); the rest want the statute,
the order, the APP document, the FRUS document, the case.

- `cal.1961-01-03.rules` (Jan. 3, II pro.yaml): 87th Congress convenes. Senate 65 D–35 R, Hickey (D) appointed in Wyoming for Keith Thomson (R), elected and d
- `cal.1961-01-05.economy` (Jan. 5, II pro.yaml): Samuelson's task force reports to the President-elect: a recession under way and a weak recovery ahead. Spend 
- `cal.1961-01-06.berlin-and-vienna` (Jan. 6, II pro.yaml): Khrushchev's speech on wars of national liberation. Kennedy reads it to his staff and quotes it to the cabinet
- `cal.1961-01-17.congo` (Jan. 17, II pro.yaml): Lumumba killed in Katanga. Not announced until Feb. 13. Eisenhower's farewell address the same day.
- `cal.1961-01-18.economy` (Jan. 18, II pro.yaml): Eisenhower's last Economic Report, two days after his last budget. Neither proposes measures against the reces
- `cal.1961-01-20.transition-and-staff` (Jan. 20, III jan.yaml): Inauguration. The cabinet confirmed and sworn in over two days: Rusk, Dillon, McNamara, Robert Kennedy, Day, U
- `cal.1961-01-25.press-and-broadcasting` (Jan. 25, III jan.yaml): First presidential press conference carried live, from the State Department auditorium. Announces the Soviet r
- `cal.1961-01-29.economy` (Jan. 29, III jan.yaml): Heller takes office as chairman of the Council of Economic Advisers, with Tobin and Gordon.
- `cal.1961-02-10.opinion` (Feb. 10–15, IV feb.yaml): Gallup's first reading: 72 percent approve, 6 disapprove, 22 no opinion.
- `cal.1961-02-20.economy` (Feb. 20, IV feb.yaml): The Federal Reserve announces it will buy longer-term Treasury securities. The end of "bills only" in practice
- `cal.1961-02.economy` (Feb., IV feb.yaml): The recession's trough, as the National Bureau later dated it. Unemployment 6.9 percent in the revised series;
- `cal.1961-03.right-and-the-military` (Mar., V mar.yaml): The John Birch Society reaches the national press: the *Los Angeles Times* series and the newsmagazines. Check
- `cal.1961-03-04.economy` (Mar. 4–6, V mar.yaml): Bonn revalues the mark 4.75 percent: announced Saturday the 4th, effective Monday, 4.00 marks to the dollar in
- `cal.1961-03-06.economy` (Mar. 6, V mar.yaml): Heller before the Joint Economic Committee: a gap between actual and potential output, and 4 percent unemploym
- `cal.1961-03-17.economy` (Mar. 17, V mar.yaml): Heller to the President: even if the whole program passes, output at year's end will be some $40 billion below
- `cal.1961-03-29.states-and-cities` (Mar. 29, V mar.yaml): Twenty-Third Amendment ratified. Three electoral votes for the District.
- `cal.1961-04-03.states-and-cities` (Apr. 3, VI apr.yaml): Michigan voters approve a constitutional convention. Romney leads Citizens for Michigan.
- `cal.1961-04-04.states-and-cities` (Apr. 4, VI apr.yaml): Texas special election for Johnson's seat. Seventy-one candidates; Tower first, Blakley second. Runoff set.
- `cal.1961-04-04.cuba` (Apr. 4, VI apr.yaml): State Department meeting on the invasion plan. Fulbright, invited, argues against it. The plan goes ahead.
- `cal.1961-04-06.opinion` (Apr. 6–11, VI apr.yaml): Approval 78 percent, disapproval 5, the lowest of the presidency. In the field the week before the landing.
- `cal.1961-04-12.space` (Apr. 12, VI apr.yaml): Gagarin orbits the earth.
- `cal.1961-04-17.right-and-the-military` (Apr. 17, VI apr.yaml): Major General Edwin Walker relieved of his division in Germany pending inquiry into his "Pro-Blue" troop progr
- `cal.1961-04-18.specials` (Apr. 18, VI apr.yaml): Arkansas 6th, special. Catherine Dorris Norrell to her husband's seat, 43.1 percent of five Democrats. No swin
- `cal.1961-04-19.court` (Apr. 19–20, VI apr.yaml): *Baker v. Carr* argued.
- `cal.1961-04-22.cuba` (Apr. 22, VI apr.yaml): Kennedy meets Eisenhower at Camp David. The Cuba Study Group formed: Taylor, Robert Kennedy, Dulles, Burke.
- `cal.1961-04-28.opinion` (Apr. 28–May 3, VI apr.yaml): After the Bay of Pigs: 83 percent approve, the high of the presidency; 61 percent approve his handling of Cuba
- `cal.1961-05-01.crime-and-hijacking` (May 1, VII may.yaml): First U.S. airliner hijacked to Cuba, a National Airlines flight bound for Key West.
- `cal.1961-05-01.court` (May 1, VII may.yaml): *Baker v. Carr* restored to the calendar for reargument.
- `cal.1961-05-02.specials` (May 2, VII may.yaml): Arizona 2d, special. Morris Udall holds his brother's seat, 51.0 to 49.0 over Matheson (R). Swing 4.7 to R.
- `cal.1961-05-03.laos` (May 3, VII may.yaml): Cease-fire in Laos.
- `cal.1961-05-04.freedom-rides` (May 4, VII may.yaml): Thirteen CORE riders leave Washington on two buses to test *Boynton v. Virginia* (1960).
- `cal.1961-05-09.press-and-broadcasting` (May 9, VII may.yaml): Minow tells the broadcasters their schedules are "a vast wasteland."
- `cal.1961-05-09.berlin-and-vienna` (May 9, VII may.yaml): Robert Kennedy's first meeting with Georgi Bolshakov. The back channel to Khrushchev opens.
- `cal.1961-05-14.freedom-rides` (May 14, VII may.yaml): Mother's Day. The Greyhound bus burned outside Anniston; the Trailways riders beaten at the Birmingham termina
- `cal.1961-05-16.laos` (May 16, VII may.yaml): The Geneva conference on Laos opens. Harriman leads the delegation.
- `cal.1961-05-16.transition-and-staff` (May 16, VII may.yaml): Ottawa. Kennedy injures his back at a tree planting; the pain and its treatment follow him to Vienna.
- `cal.1961-05-16.specials` (May 16, VII may.yaml): Pennsylvania 16th, special. Kunkel (R) holds Mumma's seat, 65.6 percent. Swing 3.1 to R.
- `cal.1961-05-16.specials-2` (May 16, VII may.yaml): Tennessee 1st, special. Louise Goff Reece (R) to her husband's seat, 62.9 percent. Swing 9.9 to D.
- `cal.1961-05-20.freedom-rides` (May 20, VII may.yaml): Montgomery. The Nashville riders beaten at the Greyhound station; Seigenthaler clubbed unconscious. Byron Whit
- `cal.1961-05-21.freedom-rides` (May 21, VII may.yaml): Mob besieges King, Abernathy, and the riders in the First Baptist Church; marshals hold it until Patterson sen
- `cal.1961-05-24.freedom-rides` (May 24, VII may.yaml): Riders go on to Jackson under Guard escort and are arrested on arrival; many to Parchman. Robert Kennedy calls
- `cal.1961-05-27.states-and-cities` (May 27, VII may.yaml): Tower beats Blakley in the runoff by about ten thousand votes. The first Republican senator elected from the f
- `cal.1961-05-28.opinion` (May 28–June 2, VII may.yaml): Gallup on the Freedom Riders: of those who knew who they were, 61 percent disapprove. 57 percent think sit-ins
- `cal.1961-05-29.freedom-rides` (May 29, VII may.yaml): Robert Kennedy petitions the Interstate Commerce Commission to forbid segregation in interstate bus terminals.
- `cal.1961-05-31.states-and-cities` (May 31, VII may.yaml): Sam Yorty unseats Mayor Norris Poulson in Los Angeles.
- `cal.1961-05.economy` (May, VII may.yaml): Unemployment 7.1 percent, the high of the year in the revised series; reported at the time as 6.9. Output and 
- `cal.1961-06-05.berlin-and-vienna` (June 5, VIII jun.yaml): London. Macmillan.
- `cal.1961-06-12.right-and-the-military` (June 12, VIII jun.yaml): Walker admonished; his program found improper. He resigns [[cal.1961-11-02.right-and-the-military]].
- `cal.1961-06-13.cuba` (June 13, VIII jun.yaml): The Cuba Study Group reports. Blame shared; the CIA's covert role to be reduced; the Joint Chiefs to advise on
- `cal.1961-06-15.berlin-and-vienna` (June 15, VIII jun.yaml): Khrushchev repeats the deadline on Soviet television. Tower sworn in.
- `cal.1961-06-26.transition-and-staff` (June 26, VIII jun.yaml): Taylor named Military Representative of the President, from July 1. A general between Kennedy and the Joint Ch
- `cal.1961-06.civil-rights-the-executive` (June, VIII jun.yaml): W. Harold Cox, Eastland's college roommate, appointed to the Southern District of Mississippi; the first Kenne
- `cal.1961-07-18.school-aid` (July 18, IX jul.yaml): House Rules Committee votes 8–7 to hold the school bills. Delaney, a Catholic Democrat, joins the conservative
- `cal.1961-07-21.space` (July 21, IX jul.yaml): Grissom's suborbital flight.
- `cal.1961-07-24.crime-and-hijacking` (July 24, IX jul.yaml): An Eastern Air Lines flight hijacked to Havana.
- `cal.1961-07-30.berlin-and-vienna` (July 30, IX jul.yaml): Fulbright on television: the East Germans have the right to close their border, and he does not know why they 
- `cal.1961-08.mississippi` (Aug., X aug.yaml): Bob Moses opens SNCC's voter registration school in McComb; registration attempts in Amite and Walthall Counti
- `cal.1961-08-02.right-and-the-military` (Aug. 2, X aug.yaml): Fulbright's memorandum to McNamara on military officers propagandizing for the radical right, written in June,
- `cal.1961-08-03.crime-and-hijacking` (Aug. 3, X aug.yaml): A Continental Air Lines 707 seized at El Paso; Kennedy follows from the White House; the FBI and Border Patrol
- `cal.1961-08-06.space` (Aug. 6, X aug.yaml): Titov orbits for a day.
- `cal.1961-08-13.berlin-and-vienna` (Aug. 13, X aug.yaml): East Germany seals the sector border overnight. Kennedy at Hyannis Port. The response is a protest.
- `cal.1961-08-16.berlin-and-vienna` (Aug. 16, X aug.yaml): Brandt's letter to Kennedy; three hundred thousand at the city hall rally.
- `cal.1961-08-19.berlin-and-vienna` (Aug. 19–20, X aug.yaml): Johnson and Clay in Berlin. A battle group of the 18th Infantry drives up the autobahn and is received by John
- `cal.1961-08-28.congo` (Aug. 28, X aug.yaml): UN forces' Operation Rumpunch against Katanga's mercenaries.
- `cal.1961-08-30.peace-corps` (Aug. 30, X aug.yaml): The first volunteers arrive in Ghana.
- `cal.1961-08-30.berlin-and-vienna` (Aug. 30, X aug.yaml): Clay named the President's personal representative in Berlin. The Soviet Union announces it will resume nuclea
- `cal.1961-08-31.rules` (Aug. 31, X aug.yaml): Rayburn leaves Washington for Bonham, ill. He does not return. McCormack presides. Check the date.
- `cal.1961-08.opinion` (Aug., X aug.yaml): Approval about three-quarters through the Berlin summer: 75 percent (July 27–Aug. 2), 76 (Aug. 24–29).
- `cal.1961-09-03.economy` (Sept. 3, XI sep.yaml): The 1961 minimum wage takes effect: $1.15 an hour, $1.25 from 1963. Newly covered retail and service workers s
- `cal.1961-09-06.steel` (Sept. 6, XI sep.yaml): Kennedy writes the heads of twelve steel companies asking them to hold prices when the October wage step comes
- `cal.1961-09-07.states-and-cities` (Sept. 7, XI sep.yaml): New York primary. Mayor Wagner, running against Tammany, beats Levitt; DeSapio loses his own district leadersh
- `cal.1961-09-12.states-and-cities` (Sept. 12, XI sep.yaml): Michigan elects its convention delegates. Romney among them.
- `cal.1961-09-15.testing` (Sept. 15, XI sep.yaml): First U.S. underground test of the series in Nevada.
- `cal.1961-09-18.congo` (Sept. 18, XI sep.yaml): Hammarskjöld killed in a crash near Ndola on his way to meet Tshombe.
- `cal.1961-09-19.space` (Sept. 19, XI sep.yaml): NASA names Houston for the Manned Spacecraft Center. Albert Thomas held NASA's appropriations.
- `cal.1961-09-19.berlin-and-vienna` (Sept. 19, XI sep.yaml): Clay arrives in Berlin.
- `cal.1961-09-22.freedom-rides` (Sept. 22, XI sep.yaml): The ICC orders segregation signs out of interstate terminals from Nov. 1.
- `cal.1961-09-23.civil-rights-the-executive` (Sept. 23, XI sep.yaml): Thurgood Marshall nominated to the Second Circuit; recess-appointed in October. Eastland's subcommittee holds 
- `cal.1961-09-25.mississippi` (Sept. 25, XI sep.yaml): Herbert Lee, a farmer working with Moses, shot dead at the Liberty cotton gin by state representative E.H. Hur
- `cal.1961-09-27.transition-and-staff` (Sept. 27, XI sep.yaml): John McCone named to succeed Dulles at the CIA. First session of the 87th Congress adjourns.
- `cal.1961-10-01.steel` (Oct. 1, XII oct.yaml): The steelworkers' October wage step. Prices hold.
- `cal.1961-10-01.defense` (Oct. 1, XII oct.yaml): Defense Intelligence Agency activated.
- `cal.1961-10-03.states-and-cities` (Oct. 3, XII oct.yaml): Michigan's constitutional convention opens at Lansing. Romney a vice president.
- `cal.1961-10-09.court` (Oct. 9, XII oct.yaml): *Baker v. Carr* reargued. Cox for the United States as amicus.
- `cal.1961-10-13.peace-corps` (Oct. 13, XII oct.yaml): A volunteer's postcard from Ibadan, describing squalor, found and published. Protests at the university; she g
- `cal.1961-10-16.right-and-the-military` (Oct. 16, XII oct.yaml): Schwarz's Christian Anti-Communism Crusade fills the Hollywood Bowl, televised.
- `cal.1961-10-17.berlin-and-vienna` (Oct. 17, XII oct.yaml): Twenty-Second Party Congress opens. Khrushchev drops the year-end deadline for a German treaty; announces a fi
- `cal.1961-10-18.vietnam` (Oct. 18, XII oct.yaml): Taylor and Rostow in Saigon. Diem declares a state of emergency. Mekong floods.
- `cal.1961-10-21.defense` (Oct. 21, XII oct.yaml): Gilpatric to the Business Council at Hot Springs. The American second strike at least equal to any Soviet firs
- `cal.1961-10-22.berlin-and-vienna` (Oct. 22, XII oct.yaml): Lightner, senior American diplomat in Berlin, stopped at Checkpoint Charlie. Clay sends armed escorts.
- `cal.1961-10-27.berlin-and-vienna` (Oct. 27–28, XII oct.yaml): Soviet and American tanks face each other at Checkpoint Charlie. Sixteen hours. The Soviets pull back first, a
- `cal.1961-10-30.testing` (Oct. 30, XII oct.yaml): Soviet test of about fifty megatons over Novaya Zemlya. The largest ever.
- `cal.1961-11-01.freedom-rides` (Nov. 1, XIII nov.yaml): ICC order in force. SNCC tests the Albany, Georgia, bus station.
- `cal.1961-11-02.right-and-the-military` (Nov. 2, XIII nov.yaml): Walker resigns from the Army.
- `cal.1961-11-03.congo` (Nov. 3, XIII nov.yaml): U Thant acting Secretary-General.
- `cal.1961-11-04.specials` (Nov. 4, XIII nov.yaml): Texas 20th, special. Henry B. González (D) over Goode (R), 54.6 to 44.0, for Kilday's seat. The first Mexican 
- `cal.1961-11-07.states-and-cities` (Nov. 7, XIII nov.yaml): Wagner reelected mayor of New York. In New Jersey Hughes (D) beats Mitchell, Eisenhower's Labor Secretary, for
- `cal.1961-11-07.specials` (Nov. 7, XIII nov.yaml): Michigan 1st, special. Nedzi (D) holds Machrowicz's seat, 85.5 percent. Swing 3.2 to R.
- `cal.1961-11-16.congress` (Nov. 16, XIII nov.yaml): Rayburn dies at Bonham. Kennedy, Johnson, Truman, and Eisenhower at the funeral.
- `cal.1961-11-17.albany` (Nov. 17, XIII nov.yaml): Albany Movement formed: SNCC, the NAACP, the ministers. William G. Anderson president.
- `cal.1961-11-24.congo` (Nov. 24, XIII nov.yaml): Security Council authorizes force against Katanga's mercenaries.
- `cal.1961-11-26.transition-and-staff` (Nov. 26, XIII nov.yaml): The Thanksgiving reshuffle. Bowles out as Under Secretary; Ball in. Harriman to the Far East; Rostow to Policy
- `cal.1961-11-28.transition-and-staff` (Nov. 28, XIII nov.yaml): Kennedy at Langley; the National Security Medal for Dulles. McCone sworn in, Nov. 29.
- `cal.1961-12-02.cuba` (Dec. 2, XIV dec.yaml): Castro declares himself a Marxist-Leninist.
- `cal.1961-12-08.vietnam` (Dec. 8, XIV dec.yaml): State's white paper on Hanoi's direction of the insurgency.
- `cal.1961-12-10.albany` (Dec. 10–13, XIV dec.yaml): Freedom riders from Atlanta arrested at the Albany station. Marches; hundreds jailed.
- `cal.1961-12-11.vietnam` (Dec. 11, XIV dec.yaml): USNS *Core* docks at Saigon with two Army helicopter companies.
- `cal.1961-12-11.court` (Dec. 11, XIV dec.yaml): *Garner v. Louisiana*, 368 U.S. 157. Sit-in convictions reversed for want of evidence.
- `cal.1961-12-15.albany` (Dec. 15–18, XIV dec.yaml): King in Albany. Arrested Dec. 16; refuses bail. Dec. 18: a truce; King out.
- `cal.1961-12-19.transition-and-staff` (Dec. 19, XIV dec.yaml): Joseph P. Kennedy's stroke at Palm Beach. Speechless thereafter.
- `cal.1961-12-19.specials` (Dec. 19, XIV dec.yaml): Louisiana 4th, special. Waggonner (D) over Lyons (R), 54.5 to 45.5, for Overton Brooks's seat. Swing 20.3 to R
- `cal.1961-12-22.vietnam` (Dec. 22, XIV dec.yaml): Specialist James T. Davis killed in an ambush west of Saigon. Later counted the first American battle death.
- `cal.1962-01-10.congress` (Jan. 10, XV jan62.yaml): Second session convenes. McCormack Speaker; Albert majority leader; Boggs whip.
- `cal.1962-01-12.vietnam` (Jan. 12, XV jan62.yaml): Operation Chopper. American H-21s lift about a thousand ARVN paratroopers into action near Saigon.
- `cal.1962-01-13.vietnam` (Jan. 13, XV jan62.yaml): Ranch Hand's first defoliation runs, along Route 15.
- `cal.1962-01-23.right-and-the-military` (Jan. 23, XV jan62.yaml): Stennis subcommittee hearings on the "muzzling" of officers open. Thurmond's doing.
- `cal.1962-01-24.program` (Jan. 24, XV jan62.yaml): House Rules Committee kills the Urban Affairs department, 9–6. Kennedy names Weaver its secretary-to-be and se
- `cal.1962-01-27.specials` (Jan. 27, XV jan62.yaml): Texas 13th, special. Purcell (D) over Meissner (R), 62.9 to 37.1, for Ikard's seat. No swing: Ikard unopposed 
- `cal.1962-01-30.specials` (Jan. 30, XV jan62.yaml): Texas 4th, special. Ray Roberts (D) to Rayburn's seat over Slagle (D), 54.3 percent. No swing: Rayburn unoppos
- `cal.1962-02-08.vietnam` (Feb. 8, XVI feb62.yaml): MACV established. Harkins commands.
- `cal.1962-02-10.berlin-and-vienna` (Feb. 10, XVI feb62.yaml): Powers exchanged for Abel on the Glienicke Bridge; Pryor freed at Checkpoint Charlie. Donovan negotiated.
- `cal.1962-02-13.specials` (Feb. 13, XVI feb62.yaml): Michigan 14th, special. Harold Ryan (D) holds Rabaut's seat, 50.5 to 49.2 over Waldron (R). Swing 12.1 to R.
- `cal.1962-02-14.press-and-broadcasting` (Feb. 14, XVI feb62.yaml): Jacqueline Kennedy's tour of the White House, CBS and NBC. About fifty million viewers.
- `cal.1962-02-18.vietnam` (Feb. 18, XVI feb62.yaml): Robert Kennedy in Saigon: the United States stays until it wins.
- `cal.1962-02-20.space` (Feb. 20, XVI feb62.yaml): Glenn orbits three times in *Friendship 7*. A heat-shield warning; the shield holds.
- `cal.1962-02-20.specials` (Feb. 20, XVI feb62.yaml): New York 6th, special. Benjamin Rosenthal (D) holds Lester Holtzman's seat, 44.5 to 43.8 over Galvin (R). Swin
- `cal.1962-02-27.vietnam` (Feb. 27, XVI feb62.yaml): Two South Vietnamese pilots bomb Independence Palace. Diem and the Nhus unhurt.
- `cal.1962-02-27.medicare` (Feb. 27, XVI feb62.yaml): Health message. Hospital insurance again.
- `cal.1962-03-13.cuba` (Mar. 13, XVII mar62.yaml): The Joint Chiefs send McNamara Operation Northwoods: pretexts for invasion, staged attacks among them. Lemnitz
- `cal.1962-03-21.defense` (Mar. 21, XVII mar62.yaml): The RS-70. Vinson's bill would "direct" bomber spending; after a Rose Garden walk with Kennedy, "authorize."
- `cal.1962-03-22.vietnam` (Mar. 22, XVII mar62.yaml): Operation Sunrise, Binh Duong. The first strategic hamlets; villagers moved.
- `cal.1962-03-22.transition-and-staff` (Mar. 22, XVII mar62.yaml): Hoover lunches with Kennedy. The Bureau knows of Judith Campbell and Giancana. Her calls to the White House en
- `cal.1962-03-26.court` (Mar. 26, XVII mar62.yaml): *Baker v. Carr*, 369 U.S. 186. Apportionment justiciable. Brennan for six; Frankfurter and Harlan dissent.
- `cal.1962-03-29.latin-america` (Mar. 29, XVII mar62.yaml): Argentina's armed forces depose Frondizi after Peronist gains.
- `cal.1962-03-30.court` (Mar. 30, XVII mar62.yaml): Whittaker retires. White named; confirmed Apr. 11.
- `cal.1962-03-31.steel` (Mar. 31, XVII mar62.yaml): Steelworkers and companies settle early. No wage increase; about ten cents in benefits. Goldberg brokered it.
- `cal.1962-04-01.voting-rights` (Apr. 1, XVIII apr62.yaml): Voter Education Project begins: the Southern Regional Council, foundation money, the Justice Department's bles
- `cal.1962-04-03.latin-america` (Apr. 3–4, XVIII apr62.yaml): Goulart in Washington; addresses Congress.
- `cal.1962-04-10.steel` (Apr. 10, XVIII apr62.yaml): Blough at the White House, 5:45 p.m., with the release. Six dollars a ton.
- `cal.1962-04-10.specials` (Apr. 10, XVIII apr62.yaml): South Carolina 2d, special. Corinne Boyd Riley (D), unopposed, to her husband's seat. No swing: Riley unoppose
- `cal.1962-04-13.steel` (Apr. 13, XVIII apr62.yaml): Inland and Kaiser hold. Bethlehem rescinds; U.S. Steel follows.
- `cal.1962-04-25.testing` (Apr. 25, XVIII apr62.yaml): U.S. atmospheric testing resumes near Christmas Island.
- `cal.1962-05-05.elections-1962` (May 5, XIX may62.yaml): Texas Democratic primary. Connally leads for governor; Walker last of six.
- `cal.1962-05-06.laos` (May 6, XIX may62.yaml): Nam Tha falls to the Pathet Lao and North Vietnamese. Phoumi's garrison flees to the Mekong.
- `cal.1962-05-09.vietnam` (May 9–11, XIX may62.yaml): McNamara's first visit. "Every quantitative measurement we have shows that we're winning this war." Check the 
- `cal.1962-05-24.space` (May 24, XIX may62.yaml): Carpenter's *Aurora 7* lands 250 miles off target.
- `cal.1962-05-28.economy` (May 28, XIX may62.yaml): The Dow's largest point drop since 1929, more than 5 percent. Recovered within days.
- `cal.1962-05-29.elections-1962` (May 29, XIX may62.yaml): Wallace wins the Alabama runoff for governor over DeGraffenried.
- `cal.1962-05.press-and-broadcasting` (May, XIX may62.yaml): The White House cancels its *New York Herald Tribune* subscriptions. Check the month.
- `cal.1962-06-05.elections-1962` (June 5, XX jun62.yaml): California primary. Nixon beats Shell for the Republican nomination for governor.
- `cal.1962-06-11.economy` (June 11, XX jun62.yaml): Yale commencement. The myths of the budget, the debt, and business confidence.
- `cal.1962-06-16.defense` (June 16, XX jun62.yaml): McNamara at Ann Arbor. Counterforce: in nuclear war, strike forces, spare cities.
- `cal.1962-06-23.laos` (June 23, XX jun62.yaml): Souvanna Phouma's coalition formed, with Souphanouvong and Phoumi.
- `cal.1962-06-25.court` (June 25, XX jun62.yaml): *Engel v. Vitale*, 370 U.S. 421. The Regents' prayer struck down, 6–1; Stewart dissents. Outcry in Congress.
- `cal.1962-06-25.mississippi` (June 25, XX jun62.yaml): Fifth Circuit, Wisdom writing: Meredith refused for his race; admit him. Cameron's stays follow.
- `cal.1962-07-09.testing` (July 9, XXI jul62.yaml): Starfish Prime: 1.4 megatons, 250 miles over Johnston Island. Artificial aurora; satellites damaged; streetlig
- `cal.1962-07-10.space` (July 10, XXI jul62.yaml): Telstar launched. July 23: first live transatlantic television, Kennedy's press conference among it.
- `cal.1962-07-10.albany` (July 10–12, XXI jul62.yaml): King and Abernathy choose jail over fines. Out July 12, the fines paid by an unnamed hand.
- `cal.1962-07-11.economy` (July 12, XXI jul62.yaml): Treasury's new depreciation guidelines. Faster write-offs, by ruling.
- `cal.1962-07-15.program` (July 15, XXI jul62.yaml): *Washington Post* (Mintz): Kelsey of the FDA kept thalidomide off the market. Kefauver's drug bill revives.
- `cal.1962-07-20.albany` (July 20–24, XXI jul62.yaml): Elliott enjoins the marches; Tuttle vacates the order. Marion King beaten at the Camilla jail. July 24: rocks 
- `cal.1962-07-23.laos` (July 23, XXI jul62.yaml): Geneva. Declaration on the Neutrality of Laos; fourteen signatories.
- `cal.1962-07-27.albany` (July 27, XXI jul62.yaml): King arrested at a City Hall prayer vigil.
- `cal.1962-07.missile-crisis` (July, XXI jul62.yaml): Raúl Castro in Moscow. Defense agreement initialed. Soviet shipping to Cuba begins. Check the initialing.
- `cal.1962-08-07.program` (Aug. 7, XXII aug62.yaml): Kelsey receives the President's Award for Distinguished Federal Civilian Service.
- `cal.1962-08-10.albany` (Aug. 10, XXII aug62.yaml): King leaves Albany. Parks and library closed rather than integrated. King later: the mistake was attacking seg
- `cal.1962-08-17.berlin-and-vienna` (Aug. 17, XXII aug62.yaml): Peter Fechter, eighteen, shot at the wall. Dies unaided in sight of the West. Riots in West Berlin.
- `cal.1962-08-27.elections-1962` (Aug. 27, XXII aug62.yaml): Edward Kennedy and McCormack debate in South Boston. "If his name was Edward Moore, with his qualifications . 
- `cal.1962-08-28.court` (Aug. 28, XXII aug62.yaml): Frankfurter retires. Goldberg named, Aug. 29; Wirtz to Labor.
- `cal.1962-08-29.missile-crisis` (Aug. 29, XXII aug62.yaml): A U-2 photographs SAM sites in western Cuba.
- `cal.1962-08-31.missile-crisis` (Aug. 31, XXII aug62.yaml): Keating on the Senate floor: Soviet troops and rocket bases in Cuba.
- `cal.1962-09-04.missile-crisis` (Sept. 4, XXIII sep62.yaml): Statement on Cuba. No offensive weapons found; were there, "the gravest issues would arise." Dobrynin assures 
- `cal.1962-09-07.missile-crisis` (Sept. 7, XXIII sep62.yaml): Kennedy asks standby authority to call 150,000 reservists.
- `cal.1962-09-10.mississippi` (Sept. 10–13, XXIII sep62.yaml): Black, as circuit justice, vacates Cameron's stays. Sept. 13: Barnett proclaims interposition.
- `cal.1962-09-11.missile-crisis` (Sept. 11, XXIII sep62.yaml): TASS: no Soviet need for missiles outside Soviet territory.
- `cal.1962-09-18.elections-1962` (Sept. 18, XXIII sep62.yaml): Massachusetts primary. Edward Kennedy over McCormack, better than two to one. George Cabot Lodge the Republica
- `cal.1962-09-20.mississippi` (Sept. 20–26, XXIII sep62.yaml): Barnett, as special registrar, refuses Meredith at Oxford. Again at Jackson, Sept. 25. Lieutenant Governor Joh
- `cal.1962-09-27.mississippi` (Sept. 27–30, XXIII sep62.yaml): Kennedy–Barnett calls, recorded. A staged confrontation agreed, then called off. Sept. 30: Meredith flown to O
- `cal.1962-10-01.mississippi` (Oct. 1, XXIV oct62.yaml): Meredith registers. Troops in Oxford. Walker arrested for insurrection; sent for psychiatric examination.
- `cal.1962-10-01.transition-and-staff` (Oct. 1, XXIV oct62.yaml): Taylor Chairman of the Joint Chiefs. Lemnitzer to NATO.
- `cal.1962-10-03.space` (Oct. 3, XXIV oct62.yaml): Schirra's six orbits.
- `cal.1962-10-13.congress` (Oct. 13, XXIV oct62.yaml): Second session adjourns. Passed: trade, the investment credit, manpower, welfare, public works. Lost: Medicare
- `cal.1962-10-14.missile-crisis` (Oct. 14, XXIV oct62.yaml): Heyser's U-2 photographs MRBM sites near San Cristóbal.
- `cal.1962-10-16.missile-crisis` (Oct. 16, XXIV oct62.yaml): Bundy tells Kennedy at breakfast. First ExComm meeting, 11:50 a.m., taped. Air strike, invasion, blockade.
- `cal.1962-10-20.missile-crisis` (Oct. 20, XXIV oct62.yaml): Kennedy leaves Chicago with a "cold." Quarantine chosen over air strike.
- `cal.1962-10-20.india-and-china` (Oct. 20, XXIV oct62.yaml): China attacks in Ladakh and the North-East Frontier Agency.
- `cal.1962-10-22.missile-crisis` (Oct. 22, XXIV oct62.yaml): Address, 7 p.m. Quarantine. A missile from Cuba to bring full retaliation on the Soviet Union.
- `cal.1962-10-24.missile-crisis` (Oct. 24, XXIV oct62.yaml): Soviet ships stop or turn back. Rusk: "the other fellow just blinked."
- `cal.1962-10-25.missile-crisis` (Oct. 25, XXIV oct62.yaml): Stevenson and Zorin at the Security Council. "Until hell freezes over." The photographs shown.
- `cal.1962-10-27.missile-crisis` (Oct. 27, XXIV oct62.yaml): Black Saturday. Second letter, broadcast: the Jupiters in Turkey added. Anderson's U-2 shot down over Cuba; an
- `cal.1962-10-28.missile-crisis` (Oct. 28, XXIV oct62.yaml): Radio Moscow: the missiles to be dismantled and returned. Castro refuses inspection.
- `cal.1962-11-06.elections-1962` (Nov. 6, XXV nov62.yaml): Midterms. Democrats lose a few House seats, gain in the Senate. Brown beats Nixon. Romney, Scranton, Rockefell
- `cal.1962-11-07.elections-1962` (Nov. 7, XXV nov62.yaml): Nixon at the Beverly Hilton: "You won't have Nixon to kick around anymore."
- `cal.1962-11-19.india-and-china` (Nov. 19–21, XXV nov62.yaml): Nehru asks for American air squadrons. Arms already flying; Harriman's mission to New Delhi. Nov. 21: China's 
- `cal.1962-11-21.space` (Nov. 21, XXV nov62.yaml): Kennedy and Webb, Cabinet Room, taped. The moon first. "I'm not that interested in space."
- `cal.1962-11.opinion` (Nov., XXV nov62.yaml): After the missile crisis, approval in the mid-seventies.
- `cal.1962-12-06.press-and-broadcasting` (Dec. 6, XXVI dec62.yaml): Sylvester, Pentagon spokesman: the government's right to lie to save itself in a nuclear crisis. "Managed news
- `cal.1962-12.missile-crisis` (Dec., XXVI dec62.yaml): Alsop and Bartlett, *Saturday Evening Post*, Dec. 8: Stevenson "wanted a Munich." Bartlett a Kennedy friend. S
- `cal.1962-12-08.press-and-broadcasting` (Dec. 8, XXVI dec62.yaml): New York newspaper strike begins. 114 days.
- `cal.1962-12-11.europe-and-the-alliance` (Dec. 11, XXVI dec62.yaml): McNamara in London tells Thorneycroft Skybolt will likely be cancelled.
- `cal.1962-12-14.space` (Dec. 14, XXVI dec62.yaml): Mariner 2 passes Venus. First planetary flyby.
- `cal.1962-12-18.europe-and-the-alliance` (Dec. 18–21, XXVI dec62.yaml): Nassau. Polaris for Britain in place of Skybolt, assigned to a NATO force. The same offered de Gaulle.
- `cal.1962-12-20.latin-america` (Dec. 20, XXVI dec62.yaml): Bosch elected president of the Dominican Republic.
- `cal.1962-12-23.cuba` (Dec. 23–24, XXVI dec62.yaml): Bay of Pigs prisoners flown to Homestead. Ransom: about $53 million in drugs and food. Donovan's deal.
- `cal.1962-12-28.congo` (Dec. 28, XXVI dec62.yaml): UN forces take Elisabethville. Katanga's secession ends in January.
- `cal.1963-01-02.vietnam` (Jan. 2, XXVI dec62.yaml): Ap Bac. The ARVN 7th Division, with American helicopters and advisers, fails against a Viet Cong battalion. Fi
- `cal.1963-01-03.congress` (Jan. 3, XXVI dec62.yaml): 87th Congress ends at noon. 88th convenes Jan. 9.

### Named, not linked


## Threads

The brief: what the thread is, and its stations, in one or two clipped sentences.

| Thread | Statement |
|---|---|
| Albany | The Albany Movement and King's arrests, Nov. 1961–Aug. 1962. |
| Berlin and Vienna | Khrushchev's ultimatum at Vienna, the buildup, the wall, Clay, the tanks. |
| Civil rights: the executive | Johnson's committee, the judges, Marshall, the housing order. |
| Congo | Lumumba's death, Katanga, Hammarskjöld, the end of secession. |
| Congress | Rayburn's death, McCormack, the second session, the end of the 87th. |
| Court | The October 1960 and 1961 Terms. *Baker v. Carr*; *Engel v. Vitale*; White and Goldberg. |
| Crime and hijacking | Robert Kennedy's bills; the first hijackings to Cuba. |
| Cuba | The Bay of Pigs and its inquiries; Mongoose; the embargo; the ransom. |
| Defense | The missile gap retracted; the budget recast; the Berlin buildup; counterforce. |
| Economy | Recession and recovery, the Council's case, the Fed's twist, the dollar, the debt limit, the guideposts, the investment credit, the tax cut. |
| Elections of 1962 | Primaries and midterms: Nixon, Edward Kennedy, Wallace. |
| Europe and the alliance | Bermuda, the Grand Design, Skybolt, Nassau. |
| Foreign aid | AID, the long-term lending fight, Hickenlooper. |
| Freedom Rides | Washington to Jackson; the ICC order. |
| India and China | Goa; the border war; American arms. |
| Laos | The crisis Eisenhower handed on; the cease-fire; Geneva; Nam Tha; the 1962 accords. |
| Latin America | The Alliance for Progress, Trujillo, Punta del Este, Brazil, the coups, Bosch. |
| Medicare | The hospital insurance bill. Introduced 1961; beaten in the Senate, July 1962. |
| Missile crisis | The Soviet decision, the warnings, the thirteen days, the IL-28s. |
| Mississippi | SNCC in McComb; Herbert Lee; Meredith and Oxford. |
| Opinion | Gallup's approval readings, and the public on Cuba, the Freedom Riders, Medicare. |
| Peace Corps | Order, volunteers, statute, the postcard. |
| Press and broadcasting | The live press conference; the publishers; Minow; the White House tour; managed news. |
| Program | The recession bills: unemployment, feed grains, minimum wage, area redevelopment, housing, Social Security. Then manpower, welfare, urban affairs, farm, public works, drugs. |
| Right and the military | The Birch Society, Walker, Fulbright's memorandum, the muzzling hearings. |
| Rules | The House Rules Committee enlarged; the Senate's filibuster rule untouched; cloture on Comsat. |
| School aid | The administration's first major defeat; the college bill, 1962. |
| Space | Gagarin to Houston; Glenn; Rice; Mariner. |
| Special elections | Texas Senate; the House: Arkansas, Arizona, Pennsylvania, Tennessee, Texas, Michigan, Louisiana, New York, South Carolina. |
| States and cities | Texas, Los Angeles, New York, Michigan, Atlanta, New Jersey. |
| Steel | The letter of September 1961; April 1962. |
| Testing | Moratorium broken; ACDA; the Soviet giant; American tests resumed; the inspection count. |
| Trade | The Trade Expansion Act. |
| Transition and staff | Taking office, the Bundy NSC, Taylor, McCone, the Thanksgiving reshuffle. |
| Vietnam | The counterinsurgency plan, Johnson's trip, NSAM 52, Staley, Taylor–Rostow, MACV, Ap Bac. The war: Viet. |
| Voting rights | The poll tax amendment; the literacy-test filibuster; the Voter Education Project. |
