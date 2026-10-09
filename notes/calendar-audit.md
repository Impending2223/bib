# The calendar against the brief

Written by `./bib audit-cal` (`tools/bib/calaudit.py`): the dated entries checked against the brief in
CLAUDE.md ("The calendar"). A review list: a hit is a place to look, not an error. Rerun after editing.

349 dated entries.

| Check | Entries |
|---|---|
| A person in `c` with a Part III entry missing from `Names:` | 114 |
| (of which only a President's surname: Eisenhower, Kennedy, Johnson) | 46 |
| Neither a bibliography of its own nor a `See [[id]]` back | 9 |
| No primary record linked or named | 78 |
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
- `cal.1962-03-26.court` (Mar. 26, XVII mar62.yaml): *Baker v. Carr*, [369 U.S. 186](https://tile.loc.gov/storage-services/service/ll/usrep/usrep369/usrep369186/us
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

- `cal.1961-01-05.economy` (Jan. 5, II pro.yaml): Samuelson's task force reports to the President-elect: a recession under way and a weak recovery ahead. Spend 
- `cal.1961-02-10.opinion` (Feb. 10–15, IV feb.yaml): Gallup's first reading: 72 percent approve, 6 disapprove, 22 no opinion.
- `cal.1961-02.economy` (Feb., IV feb.yaml): The recession's trough, as the National Bureau later dated it. Unemployment 6.9 percent in the revised series;
- `cal.1961-03.right-and-the-military` (Mar., V mar.yaml): The John Birch Society reaches the national press: the *Los Angeles Times* series and the newsmagazines. Check
- `cal.1961-03-17.economy` (Mar. 17, V mar.yaml): Heller to the President: even if the whole program passes, output at year's end will be some $40 billion below
- `cal.1961-04-03.states-and-cities` (Apr. 3, VI apr.yaml): Michigan voters approve a constitutional convention. Romney leads Citizens for Michigan.
- `cal.1961-04-04.states-and-cities` (Apr. 4, VI apr.yaml): Texas special election for Johnson's seat. Seventy-one candidates; Tower first, Blakley second. Runoff set.
- `cal.1961-04-06.opinion` (Apr. 6–11, VI apr.yaml): Approval 78 percent, disapproval 5, the lowest of the presidency. In the field the week before the landing.
- `cal.1961-04-18.specials` (Apr. 18, VI apr.yaml): Arkansas 6th, special. Catherine Dorris Norrell to her husband's seat, 43.1 percent of five Democrats. No swin
- `cal.1961-04-28.opinion` (Apr. 28–May 3, VI apr.yaml): After the Bay of Pigs: 83 percent approve, the high of the presidency; 61 percent approve his handling of Cuba
- `cal.1961-05-01.crime-and-hijacking` (May 1, VII may.yaml): First U.S. airliner hijacked to Cuba, a National Airlines flight bound for Key West.
- `cal.1961-05-02.specials` (May 2, VII may.yaml): Arizona 2d, special. Morris Udall holds his brother's seat, 51.0 to 49.0 over Matheson (R). Swing 4.7 to R.
- `cal.1961-05-04.freedom-rides` (May 4, VII may.yaml): Thirteen CORE riders leave Washington on two buses to test *Boynton v. Virginia* (1960).
- `cal.1961-05-09.berlin-and-vienna` (May 9, VII may.yaml): Robert Kennedy's first meeting with Georgi Bolshakov. The back channel to Khrushchev opens.
- `cal.1961-05-14.freedom-rides` (May 14, VII may.yaml): Mother's Day. The Greyhound bus burned outside Anniston; the Trailways riders beaten at the Birmingham termina
- `cal.1961-05-16.specials` (May 16, VII may.yaml): Pennsylvania 16th, special. Kunkel (R) holds Mumma's seat, 65.6 percent. Swing 3.1 to R.
- `cal.1961-05-16.specials-2` (May 16, VII may.yaml): Tennessee 1st, special. Louise Goff Reece (R) to her husband's seat, 62.9 percent. Swing 9.9 to D.
- `cal.1961-05-21.freedom-rides` (May 21, VII may.yaml): Mob besieges King, Abernathy, and the riders in the First Baptist Church; marshals hold it until Patterson sen
- `cal.1961-05-24.freedom-rides` (May 24, VII may.yaml): Riders go on to Jackson under Guard escort and are arrested on arrival; many to Parchman. Robert Kennedy calls
- `cal.1961-05-27.states-and-cities` (May 27, VII may.yaml): Tower beats Blakley in the runoff by about ten thousand votes. The first Republican senator elected from the f
- `cal.1961-05-28.opinion` (May 28–June 2, VII may.yaml): Gallup on the Freedom Riders: of those who knew who they were, 61 percent disapprove. 57 percent think sit-ins
- `cal.1961-05-31.states-and-cities` (May 31, VII may.yaml): Sam Yorty unseats Mayor Norris Poulson in Los Angeles.
- `cal.1961-06-12.right-and-the-military` (June 12, VIII jun.yaml): Walker admonished; his program found improper. He resigns [[cal.1961-11-02.right-and-the-military]].
- `cal.1961-07-30.berlin-and-vienna` (July 30, IX jul.yaml): Fulbright on television: the East Germans have the right to close their border, and he does not know why they 
- `cal.1961-08.mississippi` (Aug., X aug.yaml): Bob Moses opens SNCC's voter registration school in McComb; registration attempts in Amite and Walthall Counti
- `cal.1961-08-31.rules` (Aug. 31, X aug.yaml): Rayburn leaves Washington for Bonham, ill. He does not return. McCormack presides. Check the date.
- `cal.1961-08.opinion` (Aug., X aug.yaml): Approval about three-quarters through the Berlin summer: 75 percent (July 27–Aug. 2), 76 (Aug. 24–29).
- `cal.1961-09-07.states-and-cities` (Sept. 7, XI sep.yaml): New York primary. Mayor Wagner, running against Tammany, beats Levitt; DeSapio loses his own district leadersh
- `cal.1961-09-12.states-and-cities` (Sept. 12, XI sep.yaml): Michigan elects its convention delegates. Romney among them.
- `cal.1961-09-15.testing` (Sept. 15, XI sep.yaml): First U.S. underground test of the series in Nevada.
- `cal.1961-09-19.space` (Sept. 19, XI sep.yaml): NASA names Houston for the Manned Spacecraft Center. Albert Thomas held NASA's appropriations.
- `cal.1961-09-19.berlin-and-vienna` (Sept. 19, XI sep.yaml): Clay arrives in Berlin.
- `cal.1961-09-25.mississippi` (Sept. 25, XI sep.yaml): Herbert Lee, a farmer working with Moses, shot dead at the Liberty cotton gin by state representative E.H. Hur
- `cal.1961-10-01.steel` (Oct. 1, XII oct.yaml): The steelworkers' October wage step. Prices hold.
- `cal.1961-10-03.states-and-cities` (Oct. 3, XII oct.yaml): Michigan's constitutional convention opens at Lansing. Romney a vice president.
- `cal.1961-10-13.peace-corps` (Oct. 13, XII oct.yaml): A volunteer's postcard from Ibadan, describing squalor, found and published. Protests at the university; she g
- `cal.1961-10-16.right-and-the-military` (Oct. 16, XII oct.yaml): Schwarz's Christian Anti-Communism Crusade fills the Hollywood Bowl, televised.
- `cal.1961-10-21.defense` (Oct. 21, XII oct.yaml): Gilpatric to the Business Council at Hot Springs. The American second strike at least equal to any Soviet firs
- `cal.1961-11-02.right-and-the-military` (Nov. 2, XIII nov.yaml): Walker resigns from the Army.
- `cal.1961-11-04.specials` (Nov. 4, XIII nov.yaml): Texas 20th, special. Henry B. González (D) over Goode (R), 54.6 to 44.0, for Kilday's seat. The first Mexican 
- `cal.1961-11-07.states-and-cities` (Nov. 7, XIII nov.yaml): Wagner reelected mayor of New York. In New Jersey Hughes (D) beats Mitchell, Eisenhower's Labor Secretary, for
- `cal.1961-11-07.specials` (Nov. 7, XIII nov.yaml): Michigan 1st, special. Nedzi (D) holds Machrowicz's seat, 85.5 percent. Swing 3.2 to R.
- `cal.1961-11-17.albany` (Nov. 17, XIII nov.yaml): Albany Movement formed: SNCC, the NAACP, the ministers. William G. Anderson president.
- `cal.1961-12-02.cuba` (Dec. 2, XIV dec.yaml): Castro declares himself a Marxist-Leninist.
- `cal.1961-12-10.albany` (Dec. 10–13, XIV dec.yaml): Freedom riders from Atlanta arrested at the Albany station. Marches; hundreds jailed.
- `cal.1961-12-11.vietnam` (Dec. 11, XIV dec.yaml): USNS *Core* docks at Saigon with two Army helicopter companies.
- `cal.1961-12-15.albany` (Dec. 15–18, XIV dec.yaml): King in Albany. Arrested Dec. 16; refuses bail. Dec. 18: a truce; King out.
- `cal.1961-12-19.transition-and-staff` (Dec. 19, XIV dec.yaml): Joseph P. Kennedy's stroke at Palm Beach. Speechless thereafter.
- `cal.1961-12-19.specials` (Dec. 19, XIV dec.yaml): Louisiana 4th, special. Waggonner (D) over Lyons (R), 54.5 to 45.5, for Overton Brooks's seat. Swing 20.3 to R
- `cal.1961-12-22.vietnam` (Dec. 22, XIV dec.yaml): Specialist James T. Davis killed in an ambush west of Saigon. Later counted the first American battle death.
- `cal.1962-01-12.vietnam` (Jan. 12, XV jan62.yaml): Operation Chopper. American H-21s lift about a thousand ARVN paratroopers into action near Saigon.
- `cal.1962-01-23.right-and-the-military` (Jan. 23, XV jan62.yaml): Stennis subcommittee hearings on the "muzzling" of officers open. Thurmond's doing.
- `cal.1962-02-14.press-and-broadcasting` (Feb. 14, XVI feb62.yaml): Jacqueline Kennedy's tour of the White House, CBS and NBC. About fifty million viewers.
- `cal.1962-03-13.cuba` (Mar. 13, XVII mar62.yaml): The Joint Chiefs send McNamara Operation Northwoods: pretexts for invasion, staged attacks among them. Lemnitz
- `cal.1962-03-22.transition-and-staff` (Mar. 22, XVII mar62.yaml): Hoover lunches with Kennedy. The Bureau knows of Judith Campbell and Giancana. Her calls to the White House en
- `cal.1962-04-01.voting-rights` (Apr. 1, XVIII apr62.yaml): Voter Education Project begins: the Southern Regional Council, foundation money, the Justice Department's bles
- `cal.1962-04-25.testing` (Apr. 25, XVIII apr62.yaml): U.S. atmospheric testing resumes near Christmas Island.
- `cal.1962-05-05.elections-1962` (May 5, XIX may62.yaml): Texas Democratic primary. Connally leads for governor; Walker last of six.
- `cal.1962-05-29.elections-1962` (May 29, XIX may62.yaml): Wallace wins the Alabama runoff for governor over DeGraffenried.
- `cal.1962-05.press-and-broadcasting` (May, XIX may62.yaml): The White House cancels its *New York Herald Tribune* subscriptions. Check the month.
- `cal.1962-06-05.elections-1962` (June 5, XX jun62.yaml): California primary. Nixon beats Shell for the Republican nomination for governor.
- `cal.1962-07-09.testing` (July 9, XXI jul62.yaml): Starfish Prime: 1.4 megatons, 250 miles over Johnston Island. Artificial aurora; satellites damaged; streetlig
- `cal.1962-07-10.albany` (July 10–12, XXI jul62.yaml): King and Abernathy choose jail over fines. Out July 12, the fines paid by an unnamed hand.
- `cal.1962-07-15.program` (July 15, XXI jul62.yaml): *Washington Post* (Mintz): Kelsey of the FDA kept thalidomide off the market. Kefauver's drug bill revives.
- `cal.1962-07-20.albany` (July 20–24, XXI jul62.yaml): Elliott enjoins the marches; Tuttle vacates the order. Marion King beaten at the Camilla jail. July 24: rocks 
- `cal.1962-07-27.albany` (July 27, XXI jul62.yaml): King arrested at a City Hall prayer vigil.
- `cal.1962-08-10.albany` (Aug. 10, XXII aug62.yaml): King leaves Albany. Parks and library closed rather than integrated. King later: the mistake was attacking seg
- `cal.1962-08-27.elections-1962` (Aug. 27, XXII aug62.yaml): Edward Kennedy and McCormack debate in South Boston. "If his name was Edward Moore, with his qualifications . 
- `cal.1962-09-10.mississippi` (Sept. 10–13, XXIII sep62.yaml): Black, as circuit justice, vacates Cameron's stays. Sept. 13: Barnett proclaims interposition.
- `cal.1962-10-01.mississippi` (Oct. 1, XXIV oct62.yaml): Meredith registers. Troops in Oxford. Walker arrested for insurrection; sent for psychiatric examination.
- `cal.1962-10-20.india-and-china` (Oct. 20, XXIV oct62.yaml): China attacks in Ladakh and the North-East Frontier Agency.
- `cal.1962-10-25.missile-crisis` (Oct. 25, XXIV oct62.yaml): Stevenson and Zorin at the Security Council. "Until hell freezes over." The photographs shown.
- `cal.1962-11-07.elections-1962` (Nov. 7, XXV nov62.yaml): Nixon at the Beverly Hilton: "You won't have Nixon to kick around anymore."
- `cal.1962-11.opinion` (Nov., XXV nov62.yaml): After the missile crisis, approval in the mid-seventies.
- `cal.1962-12-06.press-and-broadcasting` (Dec. 6, XXVI dec62.yaml): Sylvester, Pentagon spokesman: the government's right to lie to save itself in a nuclear crisis. "Managed news
- `cal.1962-12-08.press-and-broadcasting` (Dec. 8, XXVI dec62.yaml): New York newspaper strike begins. 114 days.
- `cal.1962-12-14.space` (Dec. 14, XXVI dec62.yaml): Mariner 2 passes Venus. First planetary flyby.
- `cal.1962-12-20.latin-america` (Dec. 20, XXVI dec62.yaml): Bosch elected president of the Dominican Republic.

### Named, not linked


## Threads

The brief: what the thread is, and its stations, in one or two clipped sentences.

| Thread | Statement |
|---|---|
| Albany | SNCC and King against segregation in Albany, Georgia, Nov. 1961–Aug. 1962. The station test; the Albany Movement; King jailed, December and July; Elliott's injunction; King leaves. |
| Berlin and Vienna | The second Berlin crisis, from the Vienna ultimatum to the wall and after. Vienna; the July buildup; Aug. 13; Clay in Berlin; Checkpoint Charlie; Powers for Abel; Fechter. |
| Civil rights: the executive | What the President did for civil rights by appointment and order. Weaver; the equal employment committee; the new judgeships, Cox and Marshall; the housing order. |
| Congo | The Congo's civil war and the UN's war in Katanga. Lumumba's death; Rumpunch; Hammarskjöld's death; U Thant; Kitona; Elisabethville and the end of secession. |
| Congress | The 87th Congress as an institution: its leaders and sessions. Rayburn's death; McCormack Speaker; the second session's end; Jan. 3, 1963. |
| Court | The Supreme Court's October 1960 and 1961 Terms, and its new Justices. *Mapp*; *Baker v. Carr*, argued, reargued, decided; *Engel v. Vitale*; White and Goldberg for Whittaker and Frankfurter. |
| Crime and hijacking | Robert Kennedy's crime bills and the first hijackings to Cuba. Three hijackings, May–Aug. 1961; aircraft piracy a federal crime; the Wire and Travel Acts. |
| Cuba | Cuba short of the missile crisis. The Bay of Pigs and its inquiry; Mongoose; Punta del Este; the embargo; Northwoods; the prisoners' ransom; the Orange Bowl. |
| Defense | Strategy and the defense budget under McNamara. No missile gap; the March budget; the Berlin increase; civil defense to the Pentagon; Gilpatric at Hot Springs; the RS-70; counterforce at Ann Arbor. |
| Economy | The recession of 1960–61, the recovery, and the Council's case for a tax cut. The task force; the trough; the Fed's long rates; the gap; the debt limit; the 1962 Report; the May slide; depreciation; the investment credit; the Economic Club. |
| Elections of 1962 | The primaries and midterms of 1962. Connally and Wallace; Nixon in California; Edward Kennedy against McCormack; Nov. 6; Nixon's last press conference. |
| Europe and the alliance | Britain, Europe, and the alliance's nuclear arms. Bermuda; the Declaration of Interdependence; Skybolt cancelled; Nassau. |
| Foreign aid | The aid program remade. The March message; AID created, long-term borrowing denied; the 1962 act and the Hickenlooper amendment. |
| Freedom Rides | CORE's rides to test *Boynton*, May 1961, and the ICC order that came of them. Anniston; Montgomery; Jackson and Parchman; the petition; the order, in force Nov. 1. |
| India and China | India's wars, and American arms for India. Goa; the Chinese attack of October 1962; Nehru's request; Harriman's mission. |
| Laos | The Laos crisis, from Eisenhower's warning to the Geneva accords. The March maps; the cease-fire; the conference; Nam Tha; troops to Thailand; the coalition; the neutrality declaration. |
| Latin America | The Alliance for Progress and the hemisphere's governments. The Alliance proposed; Trujillo killed, his family out; Punta del Este, 1961 and 1962; Goulart; coups in Argentina and Peru; Kennedy in Caracas, Bogotá, Mexico City; Bosch elected. |
| Medicare | Hospital insurance for the aged through Social Security. The 1961 bill; the 1962 message; the Garden rally; the Senate's 52–48. |
| Missile crisis | The Soviet missiles in Cuba, from the decision to the aftermath. The Presidium's plan; the summer warnings; the U-2's find; the ExComm; the quarantine; the letters; the withdrawal; the IL-28s; the Stevenson story. |
| Mississippi | The movement in Mississippi, and Meredith's admission. McComb; Herbert Lee; the Fifth Circuit's order; Barnett's refusals; the calls; Oxford. |
| Opinion | The public's view, by Gallup. Approval from the first reading through the missile crisis; the Bay of Pigs high; the Freedom Riders. |
| Peace Corps | The Peace Corps, from order to statute. The executive order; Ghana; the act; the Ibadan postcard. |
| Press and broadcasting | The President and the press, and broadcasting's regulators. The live press conference; the publishers' speech; Minow's wasteland; the White House tour; the *Herald Tribune* cancelled; Sylvester's right to lie; the newspaper strike; "After Two Years." |
| Program | The domestic program in Congress, bill by bill. The recession bills; minimum wage; area redevelopment; housing; the Status of Women commission; federal unions; Urban Affairs refused; manpower training; the farm bill; thalidomide and the drug amendments; welfare; public works. |
| Right and the military | The radical right and the officers who spoke for it. The Birch Society; Walker relieved, admonished, resigned; Fulbright's memorandum; the crusades; the Seattle and Los Angeles speeches; the muzzling hearings; Walker at Oxford. |
| Rules | Majority rule in each chamber. The Rules Committee enlarged; Rule XXII kept; Rayburn's absence; cloture refused on the literacy test, invoked on the satellite bill. |
| School aid | Federal aid to education, the first great defeat. The 1961 message; the Rules Committee's 8–7; Calendar Wednesday refused; the college bill recommitted. |
| Space | The space race and the moon program. Gagarin; the Space Council; Shepard; the moon message; Grissom, Titov, Glenn, Carpenter, Schirra; Houston; Telstar; Rice Stadium; the moon first; Mariner 2. |
| Special elections | The special elections that filled seats in the 87th Congress. Johnson's Senate seat to Tower; twelve House seats, three to widows. |
| States and cities | State and city politics. The Twenty-Third Amendment; Tower; Yorty; Atlanta's schools; Wagner against Tammany; Michigan's convention and Romney; the elections of 1961. |
| Steel | Steel prices and the guideposts. The letter of September 1961; the early settlement; the April price rise and its rescission. |
| Testing | Nuclear testing and arms control. The Soviet resumption; American tests underground; ACDA; the fifty megatons; atmospheric tests resumed; Geneva; Starfish Prime; Khrushchev's inspection offer. |
| Trade | The Trade Expansion Act, from message to signature. The House and Senate votes; Herter named. |
| Transition and staff | The administration's people and organization. The cabinet; the NSC remade; the back injury; Taylor at the White House; McCone for Dulles; the Thanksgiving reshuffle; Joseph Kennedy's stroke; Hoover's lunch; Taylor to the Joint Chiefs. |
| Vietnam | The deepening commitment in Vietnam. The counterinsurgency plan; Johnson's trip; NSAM 52; Staley; Taylor–Rostow; NSAM 111; helicopters and the first dead; MACV; strategic hamlets; Galbraith's dissent; McNamara's visits; Mansfield's report; Ap Bac. |
| Voting rights | Voting rights in Congress and the field. The poll tax amendment; the Voter Education Project; the literacy-test filibuster. |
