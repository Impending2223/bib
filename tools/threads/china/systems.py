"""The nine systems (xitong, kou) of the liked proposal: the words that tell which one an entry's business belongs to.

Data only; `measure.py` reads it. A system is told from the line (`c`), never from the book the entry was read
from: by the matter (MATTER: words for the business), by the body that meets or acts (BODY), and by the office of
the person acting (OFFICE: a person at the head of the line, where the line states no matter). Each MATTER row is
(weight, regex), case-insensitive. HEADBODY: the ministry or department that acts, at the head of the line (4 points). A system's score is the sum of the
weights of the rows that hit (each row counted once; a row that hits only after the first 200 characters of the
line, where the line no longer says what happened, counts 1). The highest score takes the entry; a tie goes to the system
earlier in ORDER. Scores under 2 are no evidence.
"""

# slug suffix, name, the tie-break order
ORDER = ['foreign', 'army', 'legal', 'front', 'farm', 'economy', 'culture', 'org', 'center']
NAMES = {
    'center': ('china-center', "Center's daily work"),
    'foreign': ('china-foreign', 'Foreign affairs'),
    'army': ('china-army', 'Army'),
    'economy': ('china-economy', 'Finance and economy'),
    'farm': ('china-agriculture', 'Agriculture'),
    'legal': ('china-political-legal', 'Political-legal work'),
    'culture': ('china-propaganda', 'Propaganda and culture'),
    'org': ('china-organization', 'Organization'),
    'front': ('china-united-front', 'United front and nationalities'),
}

# Countries and their people: a mention is weak evidence of foreign business (the line may only name them).
COUNTRY = (r"Soviet|USSR|苏联|Moscow|Khrushchev|Kosygin|Brezhnev|Mikoyan|Chervonenko|Vietnam|越南|DRV\b|Hồ Chí Minh|Phạm Văn Đồng|Lê Duẩn|Hanoi|NLF\b|Laos|Lao\b|Souvanna|Souphanouvong|Pathet|Korea|朝鲜|Kim Il|Pyongyang|"
           r"Japan|日本|Tokyo|Indonesia|印尼|Sukarno|Subandrio|Aidit|PKI\b|Jakarta|India\b|Indian\b|Nehru|Pakistan|Ayub|Bhutto|Ceylon|Bandaranaike|Nepal|Mahendra|Koirala|Afghan|Bhutan|Sikkim|"
           r"Africa|Ghana|Guinea|Mali\b|Algeri|Tanzania|Tanganyika|Zanzibar|Congo|Somali|Sudan\b|Ethiopia|Morocc|Tunisia|Kenya|Uganda|Zambia|Nkrumah|Nyerere|Touré|Keita|Keïta|Ben Bella|Boumediene|Mauritania|Senegal|Cameroon|Burundi|Nigeria|Rhodesia|Angola|Mozambique|"
           r"\bUAR\b|Egypt|Nasser|Cairo|Syria|Iraq|Yemen|Palestin|Iran\b|Lebanon|Kuwait|Israel|Cuba|Castro|Guevara|Havana|Brazil|Chile|Mexic|Argentin|Venezuel|Peru\b|Bolivia|Uruguay|Colombia\b|Ecuador|Latin America|"
           r"France|French|de Gaulle|Britain|British|London|Ital(?:y|ian)|Sweden|Swedish|Switzerland|Swiss|Norw(?:ay|egian)|Denmark|Danish|Netherlands|Dutch|Finland|Finnish|Austria|Belgi|West German|Federal Republic|"
           r"Albania|Hoxha|Shehu|Tirana|Romania|Bucharest|Maurer|Poland|Polish|Czech|Hungar|Bulgaria|GDR\b|East German|Ulbricht|Yugoslav|Tito|Burm|Ne Win|U Nu\b|Rangoon|Cambodia|Sihanouk|Phnom Penh|Mongolian People's Republic|Tsedenbal|Ulan Bator|"
           r"America|United States|\bU\.S\.|Washington|Kennedy|Johnson|Nixon|Canad|Australia|New Zealand|Thai|Malay|Singapore|Philippine|Turk(?:ey|ish)|Greece|Greek|Spain|Spanish|Portug")

# Rows are case-insensitive; a part that must keep its case is written (?-i:...).
MATTER = {
 'foreign': [
  (3, r"\bambassadors?\b|chargé|\bembass(?:y|ies)\b|\bconsul(?:ate|s)?\b|\benvoys?\b|\bdiplomat|Foreign Ministry|外交部|Foreign Affairs Office|外事办|International Liaison Department|中联部|Liaison Department"),
  (3, r"\bforeign (?:guests?|affairs|policy|visitors?|friends|correspondents?|journalists?|students|relations|aid)\b|\bjoint (?:communiqué|statement|press)|\bcommuniqué|\btreat(?:y|ies)\b|\bstate visit|goodwill|friendship (?:association|delegation|group|mission|visit)"),
  (3, r"\b(?:government|party|military|trade|economic|cultural|parliamentary|friendship|youth|trade[- ]union|press|scientific|goodwill|women's|medical) (?:delegations?|missions?)\b|(?-i:\b[A-Z][a-z]+(?:n|ese|ish|i|an) (?:delegations?|missions?)\b)"),
  (2, r"\bdelegation\b|\bstate banquet|national[- ]day reception|\bboundary (?:talks|treaty|agreement|question|committee)|(?-i:\bPrime Minister\b|\bPresident [A-Z]|\bKing [A-Z]|\bPrince [A-Z]|\bQueen [A-Z]|\bForeign Minister [A-Z]|\bChancellor\b)"),
  (3, r"United Nations|(?-i:\bUN\b)|Warsaw talks|ambassadorial talks|aide-mémoire|\bprotest(?:s|ed)? (?:to|against) the|(?-i:\bnotes? (?:to|from) the [A-Z])|fraternal part(?:y|ies)|international communist|world peace|Afro-Asian|Asian[- ]African|World Federation|Peace Council|peace committee|solidarity (?:committee|conference)"),
  (3, r"(?-i:Communist Party of [A-Z]|\b[A-Z][a-z]+(?:ian|ese|ish|ean|can|vian) (?:Communist|Communists|Workers'|Labou?r|Socialist|People's|Party|[Aa]mbassador|[Gg]overnment|comrades|guests|friends|writer|journalists?|[Pp]arliament|National Assembly|people's)\b|Communist Party \((?:Left|Marxist))|\bon a visit to China|\bvisiting China\b|\bvisit to China\b|\bof the [A-Z][a-z]+ (?:Communist|Workers'|Labou?r) Party"),
  (2, r"(?-i:\b(?:aid|loans?|credits?|experts) to [A-Z])|\b(?:trade|aid|payments|cultural|air|shipping|economic|scientific)[^.;]{0,25} (?:agreement|protocol)s? (?:with|between)|\bimperialis|\brevisionis|overseas visits?|visit(?:s|ing)? abroad|\babroad\b|world situation|international (?:situation|questions?|affairs)"),
 ],
 'army': [
  (3, r"Military Commission|军委|(?-i:\bCMC\b)|General Staff|总参|General Political Department|总政|General Logistics|总后|Defense Ministry|Ministry of (?:National )?Defen[cs]e|国防部|National Defense Council|(?-i:\bPLA\b)|People's Liberation Army|解放军"),
  (3, r"\b(?:army|armies|navy|air force|troops|garrison|militia|naval|military regions?|military districts?|armed forces|artillery|armou?red|infantry|regiments?|divisions? of|corps commanders?|soldiers?|officers and men|servicemen|warships?|fleet|air defen[cs]e|anti-aircraft)\b"),
  (2, r"\bmilitary\b|\bdefen[cs]e\b|\bwar preparations?|备战|\bmarshals?\b|\bgenerals\b|\bcommanders?\b|\bcombat|\bshot down|\bshell(?:ing|ed)\b|\bU-2\b|Fujian front|Jinmen|Quemoy|Matsu|\bcoastal defen[cs]e|\bfrontier (?:defen[cs]e|troops)|军区|部队|军事"),
  (2, r"military (?:academy|academies|training|work|science|industry|production|ranks?|service)|defen[cs]e industr|国防工业|conscript|demobili[sz]|\bveterans\b|\bwar (?:plans?|games?)|\bstrategic|\boperational|Academy of Military Science|军事科学院|\bweapons?\b|\bmunitions|\bordnance"),
 ],
 'legal': [
  (3, r"public security|公安|procurator|检察|Supreme (?:People's )?Court|法院|\bcourts?\b(?! of)|\bjudges?\b|\bprisons?\b|\bprisoners?\b|labou?r (?:reform|re-education|camps?)|劳改|劳教|political[- ](?:and[- ])?legal|政法|Ministry of (?:the )?Interior|Internal Affairs Ministry|内务部"),
  (3, r"(?<!house )\barrest(?:ed)?\b|\bexecut(?:ed|ions?)\b(?! committee)|\bsentenced\b|\bcounter-?revolutionar(?:y|ies) (?:cases?|crimes?|arrested|suppressed)|suppress(?:ion|ing)? of counter|\bspecial pardons?\b|\bamnest|特赦|\bwar criminals?\b|\bcriminals?\b|\bpolice\b|\bespionage|\bspies\b|\bsecret agents?|armed agents"),
  (3, r"National People's Congress|全国人大|人民代表大会|(?-i:\bNPC\b)|\bdeputies\b|\bconstitution\b(?! of the party)|\bdraft law|\blaw on\b|\bmarriage law|\blegal\b|\blegislat|household registration|户口|\bcensus\b|\bsocial order|\bpublic order|\bsecurity work"),
 ],
 'front': [
  (3, r"United Front|统战|统一战线|CPPCC|政协|Political Consultative|democratic part(?:y|ies)|民主党派|non-party|无党派|democratic (?:personages|figures)|parties' figures|industrialists? and (?:businessmen|merchants)|Federation of Industry and Commerce|工商联|\bcapitalists\b|fixed interest|定息|national bourgeoisie|\bthe bourgeoisie"),
  (3, r"\bnationalit(?:y|ies)\b(?! (?:Cultural )?(?:Palace|Hotel))(?<!Palace of Nationalities)|民族|\bminorit(?:y|ies)\b|\bTibet|西藏|Dalai|Panchen|班禅|\bLhasa|\bUighur|\bUyghur|\bKazakh|(?-i:\bHui\b)|\bMuslims?\b|\bIslam|\bBuddhis|\bCatholic|\bChristian|\breligio|宗教|autonomous (?:region|prefecture|county)|Ngapoi|Saifudin|Burhan"),
  (2, r"\bTaiwan\b|台湾|Chiang Kai-shek|Chiang Ching-kuo|Kuomintang|国民党"),
  (3, r"overseas Chinese|华侨|returned Chinese|Li Zongren|李宗仁|Zhang Zhizhong|Fu Zuoyi|Cai Tingkai|Shao Lizi|Zhang Shizhao|Huang Yanpei|Chen Shutong|Shen Junru|Li Jishen|Cheng Qian|Soong Ching-ling|Song Qingling|He Xiangning|Puyi|溥仪|Hong Kong|香港|Macao|Macau|澳门|compatriots|Revolutionary Committee of the Kuomintang"),
  (2, r"Nationalities Affairs|Nationalities Committee|Religious Affairs|\bpatriotic (?:personages|figures)|meetings? of immortals|神仙会|\bintellectuals\b"),
 ],
 'farm': [
  (3, r"\bagricultur|农业|\bfarm(?:s|ing|ers?|land)?\b|\brural\b|农村|\bpeasants?\b|\bcommunes?\b|公社|production (?:teams?|brigades?)|生产队|\bbrigades?\b|private plots?|自留地|\bgrain\b|粮食|\bcotton\b(?! mill| textile| cloth)|\bharvests?\b|\bsowing\b|\bcrops?\b|\bwheat\b|\brice\b|\bpigs?\b|\blivestock|draft animals"),
  (3, r"water conservancy|水利|\birrigat|\breservoirs?\b|\bdrought|\bfloods?\b|\bflood(?:ed)? (?:control|areas?)|\bforestr|\bafforest|\bfisher|\bstate farms?\b|\breclam|\bfertili[sz]er|\btractors?\b|farm machinery|agricultural machinery|\bhusbandry|\bsilkworm|\bsugar ?cane|\borchards?\b|\bnursery garden|\bsluice|\bfruit trees|\bbeekeep|\boil[- ]crops|\bfamine|\bdisaster"),
  (2, r"Rural Work Department|农村工作部|Ministry of Agriculture|Agriculture and Forestry|农林|\bvillages?\b|\bcountryside|work[- ]points?|mess[- ]halls?|food ration|rural (?:markets?|fairs?)"),
 ],
 'economy': [
  (3, r"Planning Commission|计委|Economic Commission|经委|Capital Construction Commission|建委|Finance and Trade|财贸|Industry and Communications|工交|Ministry of Finance|Finance Ministry|财政部|People's Bank|人民银行|\bbudget|\bfinanc(?:e|es|ial)\b|\bcurrency|\bbanks?\b|\bprices?\b|\bwages?\b|\btax(?:es|ation)?\b|\bdeficit"),
  (3, r"\b(?:annual|national economic|economic|five-year|long-term|[12]9\d\d|year's|ten-year|seven-year|quarter(?:ly|'s)?) plans?\b|\bthe plan\b|Five-Year Plan|五年计划|\bplanning (?:conference|work|meeting)|national economy|国民经济|\beconom(?:y|ic)\b|capital construction|基本建设|基建|\binvestment"),
  (3, r"\bindustr(?:y|ial|ies)\b|工业|\bsteel\b|\bcoal\b|\boil ?fields?\b|\bpetroleum|\belectric(?:ity| power)|power stations?|\brailways?\b|\btransport\b|\bshipping\b|\bhighways?\b|\bcivil aviation|\bfactor(?:y|ies)\b|\bworks\b(?! of)|\bmines?\b|\bmining|\bmachine[- ]building|\bmachinery|\benterprises?\b|\bmetallurg|\bchemical|\btextiles?\b|light industry|handicrafts?|\bgeolog|\boutput\b"),
  (2, r"\btrade\b(?! unions?)|贸易|\bcommerce|商业|\bmarkets?\b|\bcommodit|\bexports?\b|\bimports?\b|foreign exchange|\bworkers and staff|\blabou?r force|\blabou?r and wages|\bstreamlin|精简|\btechnical (?:innovation|revolution|transformation)|\bindustrial production|\bplants?\b(?! trees)|\bexhibition of (?:industr|export)|export commodities"),
 ],
 'culture': [
  (3, r"Propaganda Department|宣传部|\bpropaganda\b|宣传|\bXinhua\b|新华社|(?-i:\bNCNA\b)|\bnewspapers?\b|\bjournalis|\bbroadcast|\bradio\b|\bpublish(?:ing|ed|ers?)?\b|\bpublication|Selected Works|选集|Quotations|语录|\bcensor"),
  (3, r"\bfilms?\b|\btheat(?:re|er)s?\b|\bopera\b|\bdrama\b|\bplays (?:about|on|of|by)\b|\bthe play\b|\bplaywrights?\b|\btroupes?\b|\bballet|song[- ]and[- ]dance|\bliteratur|\bliterary\b|\bwriters?\b|\bnovels?\b|\bartists?\b|\bthe arts\b|\bart (?:festival|troupes?|work|circles|exhibition)|\bamateur\b|文艺|\bmuseums?\b|Ministry of Culture|文化部|\bcultural (?:work|policy|relics|affairs)"),
  (3, r"\beducation(?:al)?\b|教育|\buniversit(?:y|ies)\b|\bcolleges?\b|\bschools?\b(?<!Party School)(?<!Party Schools)|\bstudents?\b|\bteachers?\b|\btextbooks?\b|\bscien(?:ce|ces|tific|tists?)\b|科学|Academy of Sciences|科学院|\bresearch institutes?|\bhealth work|Ministry of Health|卫生部|public health|\bmedical (?:work|teams?|schools?|colleges?)|\bsports?\b|\bathlet|table tennis|\bphysical culture"),
  (2, r"Renmin ribao|人民日报|People's Daily|\bHongqi\b|红旗杂志|Red Flag\b|\beditorials?\b|Guangming ribao|Jiefangjun bao|\btheoretical\b|\bphilosoph|\bhistorians?\b|\bparty history|\bstud(?:y|ying) of Mao|Mao Zedong Thought|毛泽东思想|\bideolog|\bacademic|\bscholars?\b|\blanguage reform|\bscript reform|\bjournals?\b|\bmagazines?\b|\breference (?:news|materials)|Cankao"),
 ],
 'org': [
  (3, r"Organization Department|组织部|Control Commission|监察委员会|监委|\bcadres?\b|干部|\bappoint(?:s|ed|ments?)\b|\b(?:named|becomes|made|succeeds [A-Z][a-z]+ [A-Z][a-z]+ as) (?:first |second )?(?:secretary|minister|director|head|commander)|\bremov(?:ed|al) from (?:office|his posts?)|\bdismiss(?:ed|al)\b|\breplaces [A-Z][a-z]+ [A-Z][a-z]+ as\b|\bis moved to [A-Z][a-z]+ as\b|\bpersonnel\b|人事|\bstaffing|编制"),
  (3, r"party (?:members?|membership|branches|building|organization|life|discipline|constitution)|党员|\bexpel(?:s|led)?\b|\bdisciplin|\brehabilitat|甄别|平反|\bverdicts?\b|\bself-criticism|\bexamination of (?:his|the) (?:case|history)|\bcase (?:group|office)|专案|审查|\bconfession|\bwork of supervision|\binterrogat|\bin custody|\bunder guard\b|\bsentry\b|\bguards? (?:officer|refuse)|\bstruggled against|\bstruggle (?:meeting|session)|\bquestioned by"),
  (3, r"Youth League|共青团|青年团|trade unions?|工会|Federation of Trade Unions|Women's Federation|妇联|\bmass organizations?\b|Party School|党校|\bsalar(?:y|ies)\b|\bold cadres|\bveteran cadres|regional bureaus? (?:set up|established|restored)"),
  (2, r"\bfuneral|\bmemorial (?:meeting|service)|\bobituar|\bdies\b|\bdied\b|\bdeath of\b|追悼|pays (?:his )?(?:last )?respects"),
 ],
 'center': [
  (3, r"General Office|中央办公厅|中办|办公厅|Confidential (?:Bureau|Office)|机要|Archives Bureau|档案|\barchives\b|\bcentral documents?|中央文件|\bdocuments? of the Cent(?:er|ral Committee)|\bletters and visits|信访|\bpetition|\bGuards? Bureau|警卫局|Central Investigation Department|调查部|\bintelligence (?:work|conference)|organs directly under|中直|central state organs"),
  (2, r"\bagenda\b|\bminutes\b|\btelegrams? (?:to|from) the (?:Center|provinces|bureaus)|\btelephone conference|(?-i:\bZhongnanhai\b|\bYinian Tang\b|\bHuairen (?:Tang|Hall)\b|\bQinzheng\b)|\bcentral organs\b|\barrangement of work|\bwho is to go up Tiananmen"),
 ],
}

# The ministry, department or commission that acts: named at the head of the line, it settles the system.
HEADBODY = {
 'foreign': r"Foreign Ministry|International Liaison Department|Liaison Department|Foreign Affairs Office|Chinese Embassy|Chinese Ambassador|Chinese (?:government|party) delegation",
 'army': r"Military Commission|General Staff|General Political Department|General Logistics|Defense Ministry|Ministry of National Defense|National Defense Council|(?-i:PLA\b)|Jiefangjun bao|Air Force|Navy\b",
 'legal': r"Public Security|Supreme People's (?:Court|Procurator)|Ministry of (?:the )?Interior|National People's Congress|(?-i:NPC\b)|political[- ](?:and[- ])?legal",
 'front': r"United Front Department|CPPCC|Political Consultative|Nationalities Affairs|Overseas Chinese Affairs",
 'farm': r"Ministry of Agriculture|Rural Work Department|Agriculture and Forestry|Ministry of Water|Ministry of Forestry|Ministry of State Farms|Ministry of Grain|Grain Ministry",
 'economy': r"Planning Commission|Economic Commission|Capital Construction Commission|Finance and Trade|Industry and Communications|Ministry of Finance|Finance Ministry|People's Bank|Ministry of (?:Commerce|Foreign Trade|Metallurg|Coal|Petroleum|Railways|Communications|Labor|Light Industry|Textile|Chemical|Machine)|Foreign Trade Ministry|Streamlining Group",
 'culture': r"Propaganda Department|Ministry of Culture|Ministry of (?:Higher )?Education|Ministry of Health|Academy of Sciences|Science and Technology Commission|Culture and Education",
 'org': r"Organization Department|Control Commission|Youth League|Federation of Trade Unions|Women's Federation|Central Party School|Higher Party School",
 'center': r"General Office|Central Investigation Department",
}

# The office a person held: where he heads a line that states no matter, his business is his office's.
# (name, system, from, to); dates YYYY-MM, '' open. Only persons whose office is one system's.
OFFICE = [
 ('Yang Shangkun', 'center', '', '1965-11'), ('Deng Xiaoping', 'center', '', '1966-08'), ('Peng Zhen', 'center', '', '1966-04'),
 ('Wang Dongxing', 'center', '', ''), ('Gong Zirong', 'center', '', ''), ('Zeng San', 'center', '', ''), ('Tian Jiaying', 'center', '', '1966-05'),
 ('Ye Zilong', 'center', '', ''), ('Lai Zulie', 'center', '', ''), ('Kang Yimin', 'center', '', ''), ('Deng Diantao', 'center', '', ''),
 ('Wang Yuming', 'center', '', ''), ('He Jun', 'center', '', ''), ('Mei Xing', 'center', '', ''), ('Yan Mingfu', 'center', '', ''),
 ('Kong Yuan', 'center', '', ''), ('Luo Qingchang', 'center', '', ''), ('Li Jie', 'center', '', ''), ('Tong Xiaopeng', 'center', '', ''),
 ('Chen Yi', 'foreign', '', '1968-12'), ('Zhang Hanfu', 'foreign', '', ''), ('Ji Pengfei', 'foreign', '', ''), ('Qiao Guanhua', 'foreign', '', ''),
 ('Geng Biao', 'foreign', '', ''), ('Luo Guibo', 'foreign', '', ''), ('Zeng Yongquan', 'foreign', '', ''), ('Liu Xiao', 'foreign', '', ''),
 ('Wang Bingnan', 'foreign', '', ''), ('Wang Jiaxiang', 'foreign', '', ''), ('Wu Xiuquan', 'foreign', '', ''), ('Liu Ningyi', 'foreign', '', ''),
 ('Liao Chengzhi', 'foreign', '', ''), ('Huang Zhen', 'foreign', '', ''), ('Han Nianlong', 'foreign', '', ''),
 ('Lin Biao', 'army', '', ''), ('Luo Ruiqing', 'army', '', '1965-12'), ('He Long', 'army', '', ''), ('Ye Jianying', 'army', '', ''),
 ('Nie Rongzhen', 'army', '', ''), ('Xu Xiangqian', 'army', '', ''), ('Liu Bocheng', 'army', '', ''), ('Xiao Hua', 'army', '', ''),
 ('Yang Chengwu', 'army', '', ''), ('Huang Yongsheng', 'army', '', ''), ('Wu Faxian', 'army', '', ''), ('Qiu Huizuo', 'army', '', ''),
 ('Su Yu', 'army', '', ''), ('Zhang Aiping', 'army', '', ''), ('Tan Zheng', 'army', '', ''), ('Liu Zhijian', 'army', '', ''),
 ('Chen Yun', 'economy', '', ''), ('Li Fuchun', 'economy', '', ''), ('Li Xiannian', 'economy', '', ''), ('Bo Yibo', 'economy', '', ''),
 ('Yu Qiuli', 'economy', '', ''), ('Gu Mu', 'economy', '', ''), ('Yao Yilin', 'economy', '', ''),
 ('Tan Zhenlin', 'farm', '', ''), ('Deng Zihui', 'farm', '', ''), ('Liao Luyan', 'farm', '', ''),
 ('Xie Fuzhi', 'legal', '', ''), ('Dong Biwu', 'legal', '', ''), ('Xu Zirong', 'legal', '', ''), ('Zhang Dingcheng', 'legal', '', ''), ('Xie Juezai', 'legal', '', ''),
 ('Lu Dingyi', 'culture', '', '1966-05'), ('Zhou Yang', 'culture', '', ''), ('Hu Qiaomu', 'culture', '', ''), ('Wu Lengxi', 'culture', '', ''),
 ('Chen Boda', 'culture', '', '1966-05'), ('Kang Sheng', 'culture', '', '1966-05'), ('Jiang Qing', 'culture', '', '1966-05'), ('Xu Liqun', 'culture', '', ''), ('Deng Tuo', 'culture', '', ''),
 ('An Ziwen', 'org', '', ''), ('Hu Yaobang', 'org', '', ''), ('Wang Congwu', 'org', '', ''), ('Qian Ying', 'org', '', ''), ('Shuai Mengqi', 'org', '', ''),
 ('Li Weihan', 'front', '', ''), ('Xu Bing', 'front', '', ''), ('Ulanhu', 'front', '', ''),
]

# A lesser figure's own day with no business in it: left over, not a system's (the three person threads take theirs).
POEM = r"\b(?:poems?|verses?|calligraphy|inscriptions?|writes the name)\b"
PERSONAL = (r"\b(?:hospital|doctors?|dentist|teeth|tooth|a cold|his cold|fever|ill\b|illness|unwell|blood pressure|X-ray|treatment|injection|check-?up|operation|convalesc|rests?\b|resting|on leave|sick leave|"
            r"swims?|swimming|films?|bridge|cards|billiards|walks?|strolls?|fishing|hunting|sightsee|scenery|temples?|pagoda|tombs?|park|hot springs?|climbs|scenic|birthday|grandson|his family|"
            r"photograph|table tennis exhibition|plays (?:ball|badminton|bridge|cards|billiards|table tennis|chess)|dances?|dancing|a play|a show|a performance|an opera|Peking opera|acrobat|"
            # AUDIT MEND 7: more of the private day (notes/threads/china-assign-audit.md)
            r"cold worse|palpitations?|swollen|(?:ear|nose|throat|eyes?|teeth)[^.;]{0,20}examined|electrotherapy|wedding|zoo|storytellers?|lunch(?:es)? at|dines? at)\b")
# AUDIT MEND 9: a building is where a thing happens, not its system's business (the CPPCC's auditorium, the Nationalities Palace).
VENUE = (r"CPPCC auditorium|auditorium of the CPPCC|CPPCC's auditorium|政协礼堂|Overseas Chinese Building|华侨大厦|(?:Cultural )?Palace of (?:the )?Nationalities|"
         r"Nationalities Cultural Palace|Nationalities Palace|民族文化宫|民族宫")
MOVEMENT = (r"\b(?:arrives?|leaves?|left|flies|flew|returns?|returned|reaches|sets out|goes (?:on |back |by |from |to )|travels?|by (?:special )?train|by air|by car|by ship|the train|the plane|en route|"
            r"on the way|back (?:in|at|to)|go(?:es)? (?:from|to)|passes through|stops at|departs?|sails|drives?|moves to|stays? at|overnight)\b")
