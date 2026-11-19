# Loose dates that name a day: for the lead

Nov. 19, 2026. The owner asked "Are our ghost days not propagating?" and approved extending the placement
(tools/bib/loose.py, STYLE 3a). These entries are month- or year-dated, but their `when` names a day: a festival, a
holiday, a lunar date. They are not intercalary days, and `loose.at_for` sets no `at` on them. Each wants its day
found and the entry dated to it (an `edit` patch on `date` and `when`), or, where the source does not bear the day
out, to stay in its block.

The Gregorian days are computed (Christmas; Thanksgiving, the fourth Thursday of November). The lunar ones are left
blank: no lunar-calendar table could be verified in this session (installing one was refused); date them from a
reliable conversion table (the Hong Kong Observatory's Gregorian-lunar tables, or Zheng Hesheng's *Jin shi zhong xi
shi ri duizhao biao*) before writing them in.

| id | when | Gregorian date |
|---|---|---|
| cal.1960-12.transition-and-staff-7 | Dec., Christmas | Dec. 25, 1960 (Sunday) |
| cal.1965-12.students | Dec., Christmas | Dec. 25, 1965 (Saturday) |
| cal.1966-12.robert-kennedy-3 | Dec., Christmas | Dec. 25, 1966 (Sunday) |
| cal.1961-11.transition-and-staff-3 | Nov., Thanksgiving | Nov. 23, 1961 (Thursday) |
| cal.1960.china-leadership-19 | 1960, Spring Festival | (lunar: 1st month, 1st day; blank) |
| cal.1960.china-leadership-33 | 1960, Spring Festival | (lunar: 1st month, 1st day; blank) |
| cal.1960.china-leadership-26 | 1960, Dragon Boat Festival | (lunar: 5th month, 5th day; blank) |
| cal.1960.china-leadership-20 | 1960, 11th lunar month, 7th day | (lunar; blank: the 11th month of the gengzi year runs into Dec. 1960 or Jan. 1961) |
| cal.1963.china-leadership-7 | 1963, after Chinese New Year | (lunar: after the 1st month, 1st day; blank; an "after" day, `at: after YYYY-MM-DD` once dated) |

Two of the 1960 entries (-19, -33) concern the famine's winter and spring; the reader should confirm that the source's
"Spring Festival" is 1960's and not 1961's before the date is written. Nine entries in all.

Not here: wordings relative to an event ("after the convention", "before the primary"), which a reader sets by the
event's day; and wordings whose earliest implied day is the month's or year's first ("by the 15th", "early in the
year" on a January entry), which stay in the block (loose.py, STYLE 3a).
