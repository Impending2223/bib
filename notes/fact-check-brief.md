# Fact-check brief

You are verifying entries in a working bibliography and calendar of American
politics, 1961–1975. Each entry in your batch file contains the word "Check",
which marks a detail its author was unsure of: a date, a vote tally, a public
law or Statutes at Large number, a Federal Register cite, a case citation, a
quotation's wording, a title, a publication year, a person's dates in office.

## What to do

For each entry in your batch:
1. Find what the "Check" refers to (usually the sentence it ends, or the
   phrase it follows: "Check the date", "Check the vote", "Check the title").
2. Verify it with web search and fetch. Prefer primary or standard sources:
   - presidency.ucsb.edu (American Presidency Project: speeches, messages,
     press conferences, proclamations, executive orders; titles and dates);
   - govinfo.gov / Statutes at Large / congress.gov (public law numbers,
     Stat. cites, signing dates); federalregister.gov; archives.gov;
   - senate.gov cloture tables and roll calls; voteview.com; history.house.gov;
   - supreme.justia.com, loc.gov, law.cornell.edu, courtlistener.com (cases);
   - history.state.gov (FRUS volumes and documents);
   - jfklibrary.org, discoverlbj.org, millercenter.org;
   - for books: publisher pages, WorldCat, Library of Congress catalog;
   - reputable newspapers (NYT archive) and standard reference works.
   Two independent sources for anything you change, where you can get them.
3. Do NOT verify page numbers. Do NOT rewrite anything else in the entry.
4. Do not edit any files in /home/user/bib. Write only your results file.

## Output

Write a JSON array to the results path given in your task, one object per
entry, in the batch's order:

```json
{
  "id": "cal.1961-09-05.crime-and-hijacking",
  "rev": "<copy from the batch>",
  "verdict": "confirmed" | "corrected" | "unresolved",
  "finding": "One line: what was checked and what the sources say.",
  "sources": ["https://…", "https://…"],
  "set": {"c": "…full new text…", "n": "…full new text…"}
}
```

- `confirmed`: the detail is right. In `set`, give the field(s) with the
  "Check" sentence or clause removed and nothing else changed.
- `corrected`: the detail is wrong. In `set`, give the field(s) with the
  fact corrected and the "Check" removed. Change only what the sources
  support.
- `unresolved`: you could not settle it. Omit `set`. Say in `finding`
  what you tried and what is still open.
- If an entry has several "Check"s and you settle only some, set the ones
  you settled and keep a narrowed "Check …" for what remains; verdict is
  whichever applies to the most important one, and `finding` lists each.

## Style for any text you write in `set`

Keep the house style exactly: "Compact. Plain. Compressed." Short
declaratives and fragments; no adjectives of judgment; no added
explanation. Keep all markup as is: `*italics*`, `[[cal.…]]` links,
`[text](url)` links, "(K–J Adm. II.D)"-style references, "Names: …" lines.
Write citations as the entry already does (e.g. "Pub. L. No. 87-197, 75 Stat.
466 (1961)"). Use the same date style ("Sept. 5", "Oct. 1961").
Example: `"c": "Aircraft piracy made a federal crime. Check the date and Pub.
L. number."` confirmed with a correction to the law number becomes
`"c": "Aircraft piracy made a federal crime."` and the n gets the right cite.

When done, reply with three counts (confirmed, corrected, unresolved) and the
ids of anything corrected, in a few lines.
