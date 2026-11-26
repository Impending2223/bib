# Jewish diaspora: the audit of the reader's placings

The rule audited is the reader's brief, `notes/briefs/threads-new-jd.md`, rules 1 and 2. The thread holds Jews outside Israel: their communities and bodies, the acts against them, and what governments, parties and churches did about them. A Jew acting as anything else is not the thread's business unless the act is about Jews.

## What I read

- All 46 entries the reader put in the thread, 13 as the primary thread and 33 as a secondary one, each line and note whole.
- The 8 entries the reader named as nearest to a doubt, whole.
- A random sample of 40 of the other 94 entries the reader left out (Python's `random`, seed 52917), whole.
- The other 38 entries left out that were not word matches, whole, to find every row of a fault that repeats.
- In all, 132 of the 148 entries of the list. The 16 left unread are word matches outside the sample (jewelry, rabbits, Jewel stores and the like).
- For entries the list missed: searches of the whole calendar, 59,001 entries, for words the list's words do not cover. Among them: synagogue, temple, B'nai B'rith, Anti-Defamation, Hadassah, Yiddish, Hebrew, Zionist, rabbinical, kosher, Yeshiva, Eichmann, Auschwitz, Treblinka, the Warsaw ghetto, Nazi, swastika, Rockwell, Heschel, Prinz, Goldmann, Oberländer, Globke, Ocean Hill, Shanker, the Vatican Council, the Jewish Agency's hearings, Meridian, Beth Israel, Emanu-El, and every other entry dated Jan. 4–7, 1960. I read each hit that might be the thread's.

## The script checks over the whole tsv

- One row for every id of `jd-ids.tsv`: yes, 148, no id twice.
- Every slug a thread of `th.yaml`: yes.
- No `also` holding the primary thread: none found.
- No thread beside its parent or child: one found, `cal.1965-08-01.latin-america` (Latin America with Dominican Republic). The fault was in the entry before the reader; the reader's row only copied it. Mended below.
- The same checks pass on the tsv as mended, with its 157 rows.

## What I found right

- The 13 primary placings are sound. Each sat in a holding place for want of this thread: the *Times* entries of Jan. 6, 1960 under crime, the Federal Republic, the Soviet Union, the cities and the civil rights bodies, and the Vatican declaration under Europe.
- The secondary placings are sound but one: the Bonn Cabinet, the city of New York, the Saudi bar on Jewish servicemen, the Jewish Agency's hearings, the Klan bombings in Mississippi, Faisal on "Jews of the world", Zhou Enlai on Zionism and the Jews, and the rest.
- The out rows of the sample are sound but for one kind of fault, below. The word matches, the polls, Israel as a state, and the campaigns' dealings with Jewish voters are rightly out.

## The mends (11 rows, each marked `AUDIT:` in `basis`)

- The repeating fault: a Jewish body acting as a body on another cause. The reader left these out, reading "a Jew acting as anything else" to cover a Jewish body too. The rule names the community's "bodies" as the thread's business, and its exception speaks of a Jew, not a body. So a Jewish body's own act is the thread's business, as a secondary thread. I read every out row of that kind and brought in 8:
  - `cal.1960-07-04.elections-1960-los-angeles-5`: the Union of American Hebrew Congregations before the platform committee.
  - `cal.1963-05-08.alabama-birmingham-4`: nineteen rabbis sent to Birmingham by a rabbinical conference.
  - `cal.1964-04-06.civil-rights-bill`: B'nai B'rith Women's wire day.
  - `cal.1965-05-24.jobs-and-wages-14b`: the Central Conference of American Rabbis for the repeal of 14(b).
  - `cal.1966-01-15.war-opposition`: the Synagogue Council of America to Johnson on the war.
  - `cal.1967-04-05.king-2`: the Jewish War Veterans against King's stand on the war.
  - `cal.1968-01-05.war-opposition-2`: the American Jewish Congress, by its president, to Johnson on the bombing.
  - `cal.1968-03-25.king`: the Rabbinical Assembly's convention, King answering the rabbis.
- Left out, on the same reading: a speaker at a Jewish body's dinner or convention where the speaker, not the body, is the actor (King to the American Jewish Congress and to the Synagogue Council; Kennedy to the Zionists of America; Humphrey to the American Jewish Committee; Robert Kennedy to the Federation of Jewish Philanthropies and to the Synagogue Council). Left out too: rabbis acting one by one as clergy (Albany, St. Augustine, Tallahassee, Lelyveld at Hattiesburg), and meetings of clergy of the three faiths where no Jewish body is named.
- `cal.1967-05-28.war-opposition`: taken out. Levison's remark on the wiretap about Jews in the peace movement is a passing remark, like the others the reader left out. The entry keeps King and the Six-Day War in `also`.
- `cal.1965-08-01.latin-america`: Dominican Republic dropped from `also`. It is a child of Latin America, and the line, a dinner talk of a trip to Rio, names no Dominican business. This changes a thread the brief does not audit; the session may restore it as primary in place of Latin America if it holds the line to be Dominican business.
- `cal.1960-01-06.soviet-union-6` (arrests of Jews in Rumania): Comecon added to `also`. The Comecon reader's tsv, `cm-a.tsv`, makes Comecon the primary thread of the same entry, with this thread nowhere. The two rows disagree on the primary thread. I keep this thread primary, since the line's business is the arrest of Jews as Jews, and Rumania's government is the secondary matter. The apply must take one of the two rows.

## The entries found (9 rows, marked `AUDIT: found`)

- `cal.1960-01-06.crime-and-hijacking-2`: neo-Nazi vandalism in Bavaria, from the same *Times* story as the Kiel swastikas.
- `cal.1960-01-06.europe-and-the-alliance-federal-republic-10`: Seidel on twelve such cases in Bavaria since Christmas.
- `cal.1960-06-08.middle-east`, `cal.1960-07-04.middle-east`, `cal.1960-07-05.middle-east`: the Eichmann case between Argentina and Israel.
- `cal.1960-07-02.europe-and-the-alliance-federal-republic`: Ludwig Hahn arrested for the Warsaw ghetto and Treblinka.
- `cal.1960-07-04.cities-and-housing`: Yeshiva University plans its building.
- `cal.1967-09.mississippi-2`: a bomb destroys Temple Beth Israel, Jackson.
- `cal.1968-02-21.consumers`: the kosher processors and the kosher exemption at the poultry hearings.
- Each is secondary, with its present thread and `also` kept. The two Bavarian rows rest on the reader's reading of the January 1960 wave, which counts swastikas with no Jewish target named. If that reading goes, they go with the four swastika rows.
- Read and left out: the neo-Nazi torchlight parade in Berlin and its two entries, the New European Order in Milan, the star of David on collaborators' cafés in Brussels, and the *Daily Mail* on a Hitlerite revival. None names an act against Jews. Also left out: the Chinese statements on Nazi war criminals of 1965, the American Nazi party against King, Heschel and the other clergy against the war, and the Ocean Hill–Brownsville strikes, whose lines name no Jews.
- The Hahn row is also in `cm-a.tsv`, where the Comecon reader left it out of that thread. The two rows agree.

## The counts

- Before the audit: 13 primary, 33 secondary, 102 out, in 148 rows.
- After: 13 primary, 49 secondary, 95 out, in 157 rows. The secondary count gained 8 bodies' acts and 9 found entries, and lost Levison's remark.

## Left for the session

- `cal.1960-01-06.europe-and-the-alliance-federal-republic` (the Bonn Cabinet's penal amendment) carries Civil rights organizations in `also` from before the reader. That thread is the movement's bodies in the United States and does not fit the line. I did not mend it, as no rule I audit covers it.
- The Romania row disagrees with `cm-a.tsv`, as above.

## Whether the tsv is fit to apply

Yes, with one condition. Every row passes the script checks, and every row I read is placed by the rule. The Romania row must be settled against `cm-a.tsv` before both tsvs are applied, since each sets that entry's primary thread. Nothing in `lists/`, `th.yaml` or `sources/` was changed.
