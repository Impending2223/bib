# Legislatures

Moved word for word from CLAUDE.md, Nov. 10, 2026 (the owner: "I approve both"); CLAUDE.md keeps the core and an index of these guides.

`elections/legislatures.yaml`, written by `tools/elections/make_legislatures.py` from Carl Klarner's State Partisan Balance Data (Harvard Dataverse; the seats compiled from the *Book of the States* and the States' manuals; never edit): each State's Senate and House by session, 1959–69, as in session (Democrats, Republicans, others, vacancies), the proportion needed to override the governor's veto (the 1956 provisions) and the governor's party. `HAND` in the script for what the data cannot say (North Carolina's governor had no veto; Minnesota's and Nebraska's nonpartisan legislatures); `HAND_YEAR` a Check (Kansas, 1967). `tools/bib/legislatures.py` renders them (STYLE notes there):

- A calendar entry tagged `legislatures:<YYYY>` (the year the session met: 1961 for the legislatures chosen in Nov.
  1960) carries the session's map and table: a party's color where it holds both chambers, light for a majority, middle for the State's override proportion where that lies between a majority and two-thirds, dark for two-thirds of both (the Presentment Clause's and Article V's proportion); divided gray; Nebraska's nonpartisan chamber ivory (`--pNP`, the owner's request, Oct. 23, 2026). Now the five "legislatures-us" entries of Nov. 1960, 1962, 1964, 1966 and 1968.
- Article V's analogue is drawn at the federal two-thirds for every State: each State's own rule for proposing an amendment (the vote, the sessions) is not yet in the data; the *Book of the States*, 1960–67, prints it.
