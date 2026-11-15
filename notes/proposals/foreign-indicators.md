# Indicators for the other sovereigns: a proposal (Nov. 15, 2026)

The owner, Nov. 15: "Didn't we have an indicator extension plan plotted? IIRC, that plan only spoke to a few indicators of concern to the US. What can we do for our other sovereigns? What indicators can we calendar for them?"

The plan on file, `notes/extensions/memos/indicators-suggestions.md` ("Other IMF / bond-market numbers worth tracking, 1960-69"), is American: the gold stock, the debt, yields, money, the balance of payments. The only foreign series kept are the sterling, mark and franc rates (`indicators/fx-*.yaml`) and the world's oil (`sources/oil-world.yaml`). The series' convention for an indicator is the figure as first reported, filed by the period it covers, with today's value beside it (`notes/guide/indicators.md`). The proposal keeps it.

## 1. Where the figures are

- **As first reported, for many countries at once.** The *Federal Reserve Bulletin*'s international section, read monthly already for the American series (FRASER): the gold reserves of central banks and governments, the foreign central banks' discount rates with the dates of change, open-market rates abroad, foreign exchange rates. The IMF's *International Financial Statistics* (monthly, from 1948) and the OECD's *Main Economic Indicators* (monthly, from 1962) for prices, production, unemployment and trade by country. Where a country's own bulletin is open, it as the first report: the Bank of England's *Quarterly Bulletin*, the Bundesbank's *Monatsberichte* (on bundesbank.de), INSEE's *Bulletin mensuel de statistique*, the Bank of Japan's monthly.
- **Today's values.** FRED's OECD and IMF series (checked Nov. 15 by CSV): consumer prices for the United Kingdom, Germany, France, Japan, Italy and Canada, monthly from 1955; industrial production for the United Kingdom (1948), Germany (1958), France (1956) and Japan (1955); reserves less gold for every IMF member, monthly from 1950; Japan's unemployment rate (1955) and discount rate (1960). The United Kingdom's, Germany's and France's unemployment and central bank rates from the central banks' long series (the Bank of England's "A millennium of macroeconomic data"; the Bundesbank's time-series database; the Banque de France's Webstat).

## 2. What to calendar, by sovereign

**The United Kingdom, the FRG, France, Japan (Italy and Canada to follow).** Monthly, beside the American table: consumer prices, industrial production, unemployment, gold and reserves, the central bank's rate; quarterly, the balance of payments; the exchange rate (kept for three). Dated events, as entries: the changes of Bank Rate and of the Bundesbank's, the Banque de France's and the Bank of Japan's discount rates; the devaluations and revaluations (the mark and guilder, Mar. 1961; sterling, Nov. 18, 1967; the franc, Aug. 1969; the mark, Oct. 1969); the IMF drawings and standby arrangements (Britain's, 1961, 1964, 1965, 1967; France's, 1968).

**The world.** The London gold price and the gold pool's sales (to the two-tier market, Mar. 17, 1968); the Eurodollar rate.

**The Soviet Union.** No monthly figures were published. What can be calendared: the Central Statistical Administration's plan-fulfilment communiqués (each January, and at the half-year, in *Pravda*), the budget at the Supreme Soviet's December session, the harvest and the grain bought abroad (the wheat deals of 1963–65), and the American estimates of Soviet output and defense spending as reported (the CIA's, in FRUS; the Joint Economic Committee's compendia of 1962, 1966 and 1968).

**The People's Republic.** The statistical blackout of 1960–77: the claims made at the National People's Congress (Zhou's report of Dec. 1964), the grain bought from Canada and Australia (dated contracts), the trade with Japan, and the American estimates (the JEC's *An Economic Profile of Mainland China*, 1967; the CIA's).

**The two Vietnams.** The RVN: Saigon's retail price index and the piaster (official and free market), from USAID and the Mission; the refugee counts (the GVN's and the Mission's, which differ: the *Times* of Jan. 6, 1968 gives 527,000 and 409,000). The DRV: the American estimates already in the Southeast Asia tables and the order of battle.

**The GDR and Cuba.** The flight from the GDR, monthly to Aug. 1961 (the refugee camps' counts) and the escapes after; Cuba's sugar harvest and the emigration (the Camarioca boatlift, 1965; the Freedom Flights, monthly from Dec. 1965).

**Opinion abroad, beside Gallup's.** The United Kingdom: Gallup's monthly government and Prime Minister ratings (King and Wybrow, *British Political Opinion, 1937–2000*); France: IFOP's monthly satisfaction with de Gaulle (from 1958); Japan: Jiji's monthly cabinet approval (from June 1960); the FRG: Allensbach's and Emnid's soundings (irregular; the *Jahrbuch der öffentlichen Meinung*).

## 3. Order of work (a suggestion)

The *Federal Reserve Bulletin*'s international tables first: one source already read, many countries, the figures as first reported. Then today's values from FRED and the central banks. Then the dated events (rate changes, devaluations, drawings) as entries. Then the communiqués and estimates for the Soviet Union and China, a reading job. Then opinion abroad, a reading job for the books named.

Queued Nov. 15 (the owner: "Put it ahead of the 1969 foundations, after the pilots"): handoff C0.
