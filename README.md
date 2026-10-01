# bib

The 1968 series: eight linked working bibliographies and a calendar for
American politics from 1961 to 1974, with a ninth bibliography for the war in
Vietnam. They are kept here as data and rendered to
the pages published on claude.ai.

| list | published page |
|------|----------------|
| Kennedy and Johnson administrations, 1961–69 (K–J Adm.) | https://claude.ai/artifact/GUYbuovFgtY7vupMuTTJ4g |
| Congress, the nation, and the states, 1961–69 (K–J Cong.) | https://claude.ai/artifact/9APT15miQoMTDCewtvQTmq |
| The Republican opposition, 1961–69 (Opp.) | https://claude.ai/artifact/RJgBq4vjC92oWH91e1b9wR |
| Calendar, January 1961–January 1963: the 87th Congress (Cal.) | https://claude.ai/artifact/RfxuiEcENspJmjbGyT5zXh |
| The 1968 campaign (1968) | https://claude.ai/artifact/728hqXTjcv3aogmvCBnpgM |
| Nixon and his administration, 1969–74 (Adm.) | https://claude.ai/artifact/UnACbvVAd3HguTvpsaE6RM |
| Congress, the nation, and the states, 1969–74 (Cong.) | https://claude.ai/artifact/1rzmmHQPAvEZpqVvxshNkc |
| Watergate, 1971–74 (Wg.) | https://claude.ai/artifact/R7oEex8RCkSQhjjec7puCG |
| Vietnam and the American war, 1945–75 (Viet.) | not yet published |
| All of them in one reader, with live cross-references | https://claude.ai/artifact/9VsXuvj8UhFT9pLFxVMav5 |

## How it is kept

- Every entry is a small YAML record with a permanent id, in a file per
  section (`lists/kja/II.D.yaml`, `lists/cal/apr.yaml`). An editor, human or
  Claude, opens only the section it is changing.
- `./bib find`, `show`, `works`, and `outline` locate entries across all eight
  lists without reading them. Entries carry stored tags (`topic:berlin`, `todo`)
  and derived ones the tools compute (`check`, `person`, `thread:cuba`,
  `in:opp`).
- `./bib check` catches broken links, calendar dates outside their month,
  threads that don't exist, section references that point nowhere, and books
  cited under the wrong section.
- Changes from several hands merge entry by entry: patch files (`./bib merge`)
  and git branches (`./bib setup`) both use a three-way, field-by-field merge.
  Duplicates are flagged and can be folded together (`./bib combine`).
  Disagreements are recorded in the entry as conflicts to settle, never lost.
- `./bib build` regenerates every page, including the compiled reader's links,
  "Elsewhere" lines, and names index.

Requires Python 3 and PyYAML. Start with `./bib status`. CLAUDE.md is the
working manual.
