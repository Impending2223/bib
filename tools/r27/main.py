import sys, re, os, glob, json, yaml, collections, pickle
SP='/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad'
sys.path.insert(0,'/home/user/bib/tools'); sys.path.insert(0,SP)
from bib import store, claims
from pinyin import is_pinyin_title
OPENPRESS=re.compile(r'Renmin ribao|人民日报|人民日報|Hongqi\\*|\\*Hongqi|紅旗》|红旗》|《紅旗|《红旗|Jiefangjun bao|解放军报|解放軍報|Guangming ribao|光明日报|光明日報|Wenhui bao|文汇报|文匯報|Peking Review|Beijing Review|Xinhua|NCNA|Dagong bao|大公报|大公報|Gongren ribao|Zhongguo qingnian bao|Renmin [Cc]hubanshe|人民出版社|Foreign Languages Press')
S=store.Series()
cards=pickle.load(open(SP+'/cards.pkl','rb'))
for _c in ('w.li-wang-li-fansi-lu','w.song-yongyi-zhongguo-wenhua-dageming-wenku'):
    if cards.get(_c): cards[_c]['abroad']=True
settled=set(json.load(open(SP+'/settled.json')))
# resolve settled through aliases
settled_ids=set()
for i in settled:
    g=S.get(i)
    settled_ids.add(g[2]['id'] if g else i)
# witnesses
wit={}
for f in glob.glob('/home/user/bib/sources/witnesses/*.yaml'):
    for r in yaml.load(open(f),Loader=yaml.CSafeLoader) or []:
        wit[r['id']]=r
CJK=re.compile(r'[㐀-鿿]')
CARD=re.compile(r'\[\[(w\.[^\]|]+)\]\]')
ABROAD_SERIES=re.compile(r'Current Background|Survey of China Mainland Press|\bSCMP\b|SCMM|Selections from China Mainland Magazines|Extracts from China Mainland|\bJPRS\b|Joint Publications Research|Miscellany of Mao|Union Research|URI\b|Red Guard Publications|Center for Chinese Research Materials|Chinese Law and Government|Collected Works of Liu|Chinese Communist Party Documents of the Great Proletarian|CCP Documents of the Great Proletarian|Issues and Studies|Chinese Studies in History|FBIS|Daily Report',re.I)
ABROAD_CARDS={'w.current-background','w.tse-tung-miscellany-of-mao-tse','w.collected-works-of-liu','w.survey-of-china-mainland'}
REDTXT=re.compile(r'Red Guard|紅衛兵|红卫兵|wansui|萬歲|万岁|big-character poster|dazibao|大字報|大字报|tabloid|leaflet|传单|傳單|wall poster|兵團|兵团|總部|总部|司令部|聯絡站|联络站|造反|战报|戰報|Zhan ?[Bb]ao|Dongfanghong|東方紅|东方红|Xin Beida|新北大|Jinggangshan|井岡山|井冈山|(?:紅旗|红旗) ?(?:战报|戰報)|a faction|work unit|compilation of (leaders|Mao|Lin)|Zhongyang shouzhang|中央首長|中央首长|首長講話|首长讲话|cankao ziliao|參考資料|参考资料|Pipan ziliao|批判|Dadao|打倒|Ziliao xuanbian|資料選編|资料选编|Xuexi wenjian|學習文件|学习文件|Xuexi ziliao|學習資料|学习资料')
INTTXT=re.compile(r'内部|內部|neibu|Neibu cankao|internal circulation|internal bulletin|党内|黨內|机密|機密|for official use|Kuaibao|快報|快报|Jianbao|簡報|简报|Yaoshi huibao|要事匯報|要事汇报|Xindian kuaibao|Wenhua geming jianbao')
PRESS_NOW=re.compile(r'Renmin ribao|People.s Daily|人民日报|人民日報|Peking Review|Beijing Review|NCNA|Xinhua(?! shudian)|New China News Agency|Hongqi|Red Flag|Guangming ribao|Jiefangjun bao|Wenhui bao|Radio Peking|New York Times|Times \(London\)|Pravda|communiqu|joint statement|Daily Report',re.I)
def ent_year(e):
    return int(str(e.get('date'))[:4])
ABBR=re.compile(r'(?:\b(?:no|nos|vol|vols|ed|eds|p|pp|n|nn|cf|Jan|Feb|Mar|Apr|Aug|Sept|Sep|Oct|Nov|Dec|Mr|Mrs|Dr|St|al|trans|comp|repr|Pub|Cong|Rec|Stat|ch|chs|fig|ser|Supp|suppl|U\.S|Gen|Lt|Col|Adm|Sen|Rep|Gov|Jr|Sr|ca|c|approx|est|e\.g|i\.e|viz|vs|v|Inc|Co|Ltd|Bros|Univ|Mass|Calif|Conn|Wash|Penn|Pa|Ill|N\.Y|Md|Va|D\.C|Ga|Ala|Fla|Tex|Mich|Minn|Wis|Colo|Ariz|Okla|Kan|Neb|Ore|Tenn|Ky|Miss|La|Ark|Mo|Ind|Del|Vt|Me|R\.I|N\.J|N\.H|N\.C|S\.C|W\.Va|Nev|Mont|Wyo|Ida|Utah|Ont|Que|Hist|Dept|Doc|Docs|Sess|Res|Rept|Ex|Exec|Conf|Comm|Corp|Govt|Ibid|ibid|Id|id|et|Nat|Natl|Int|Intl|Rev|Soc|Sci|Q|J|Bull|Mag|Mo|Wk|Ann|Proc|Ser|Mss|MS|Pt|pt|art|sec|secs|para|paras|Vol|No|Nr|Bd|Hft|S|Nr|t|tr|r|v|f|ff|l|ll)\.)$')
def mysplit(n):
    out=[];cur='';d=0;b=0;i=0
    while i<len(n):
        ch=n[i]; cur+=ch
        if ch in '([': d+=1
        elif ch in ')]': d=max(0,d-1)
        if ch=='.' and d==0 and i+2<len(n) and n[i+1]==' ' and (n[i+2].isupper() or n[i+2] in '[*"\'(《〈“'):
            if not ABBR.search(cur[-12:]) and not re.search(r'\b[A-Z]\.$',cur[-3:]):
                out.append(cur.strip()); cur=''
        i+=1
    if cur.strip(): out.append(cur.strip())
    return out
def sentences(n):
    out=[]
    for s in mysplit(n or ''):
        if s.startswith('Made public'): k='MP'
        elif s.startswith('Printed for internal'): k='PIC'
        elif s.startswith('Circulated in'): k='CIC'
        elif s.startswith('To check'): k='TC'
        elif s.startswith('Check'): k='CK'
        elif s.startswith('Names'): k='NM'
        elif s.startswith('See '): k='SEE'
        else: k='SRC'
        out.append((k,s))
    return out
YR=re.compile(r'(?<![\d.])(19[4-9]\d|20[0-3]\d)(?![\d])')
def split0(t):
    out=[];d=0;cur=''
    i=0
    while i<len(t):
        ch=t[i]
        if ch=='(': d+=1
        elif ch==')': d=max(0,d-1)
        if ch==';' and d==0:
            out.append(cur); cur=''; i+=1
            while i<len(t) and t[i]==' ': i+=1
            continue
        cur+=ch; i+=1
    out.append(cur)
    return out
def mainof(t):
    return re.split(r'\(?\bcited (?:by|in)\b',t)[0]
def card_info(cid):
    return cards.get(cid) or None
def is_abroad_card(cid):
    c=card_info(cid)
    if not c: return False
    if cid in ABROAD_CARDS: return True
    return c['abroad'] or not c['chinese']
def is_mainland(cid):
    c=card_info(cid)
    return bool(c and c['chinese'] and not c['abroad'])
def work_items(s):
    """(card id or None, year, text) for each work in a sentence: card cites, and text items with a year."""
    items=[]
    for part in split0(s):
        cs=CARD.findall(part)
        # main card of the part = first card before '(cited by'
        main=mainof(part)
        mc=CARD.findall(main)
        if mc:
            for cid in mc[:1]:
                c=card_info(cid)
                y=c['year'] if c else None
                if c and c['rng']: y=None
                if cid=='w.macfarquhar-origins-of-the-cultural':
                    mv=re.search(re.escape('[['+cid+']]')+r',\s*(III|II|I)\b',main)
                    y={'I':1974,'II':1983,'III':1997}.get(mv.group(1)) if mv else None
                # explicit year right after cite: "[[w.x]], 11 (1993"
                m=re.search(re.escape('[['+cid+']]')+r'[^;()\[]{0,40}\(((?:19|20)\d\d)[;),]',main)
                if m and c and y is None: y=int(m.group(1))
                items.append((cid,y,part))
        else:
            # a text item counts as a printing only where it names a title and a later year
            ys=[int(x) for x in YR.findall(re.sub(r'\b(1[89]\d\d|20\d\d)年\d+月\d+日','',main))]
            titled = bool(re.search(r'\*[^*]{3,}\*|《[^》]+》',main))
            if not titled:
                items.append((None,None,'#record '+part)); continue
            items.append((None,(min(ys) if ys and titled else None),part))
    return items
PRC_EN=re.compile(r'Peking Review|Beijing Review|Foreign Languages Press|Waiwen chubanshe|China Reconstructs|Peking: |Beijing: ',re.I)
def item_kind(cid,text,ey):
    """internal / circulated / abroad / mainland / unknown for a cited item."""
    if cid:
        c=card_info(cid)
        if cid in AUDIT_INTERNAL or (TREE_PIC[cid] and not TREE_CIC[cid]): return 'internal'
        if TREE_CIC[cid]: return 'circulated'
        if c and c['kind']: return c['kind']
        if c and c['chinese'] and not c['abroad'] and c['year'] and 1966<=c['year']<=1970 and c.get('ckind')!='periodical': return 'circulated?'
        if c and not c['chinese'] and PRC_EN.search(c['title']+' '+c['n']+' '+c['paren']) and not c['abroad']: return 'mainland'

        if cid in ABROAD_CARDS: return 'abroad'
        if c and c['chinese'] and not c['abroad']: return 'mainland'
        if c and c.get('ckind')=='periodical' and ABROAD_SERIES.search(c['title']+c['n']): return 'abroad'
        return 'abroad' if c else 'unknown'
    if text.startswith('#record '): return 'record'
    t=mainof(text)
    t=re.sub(r'\([^()]*(marking|copyright page|CiNii|Xinhua)[^()]*\)','',t)
    if OPENPRESS.search(t) and not re.search(r'Cankao ziliao|参考资料|參考資料|Neibu|内部|內部',t): return 'mainland' if not ABROAD_SERIES.search(t) else 'abroad'
    if INTTXT.search(t): return 'internal'
    ys=[int(x) for x in YR.findall(t)]
    ital=re.findall(r'\*([^*]{3,})\*',t)
    if ys and 1966<=min(ys)<=1970 and (CJK.search(t) or any(is_pinyin_title(x) or is_pinyin_title(x+' '+x) for x in ital)) and not OPENPRESS.search(t): return 'circulated?'
    if REDTXT.search(t): return 'circulated'
    if ABROAD_SERIES.search(t): return 'abroad'
    if CJK.search(t): 
        if re.search(r'Hong Kong|香港|Taipei|臺北|台北|Taiwan',t): return 'abroad'
        return 'mainland'
    return 'unknown'
LOCALRX=re.compile(r'in China,|abroad,|elsewhere,',re.I)
res=[]
cal=S.lists['cal']
chinese_cards={k for k,v in cards.items() if v and v['chinese']}
TREE_PIC=collections.Counter(); TREE_CIC=collections.Counter()
for sec0,e0 in cal.entries():
    for k0,s0 in sentences(e0.get('n') or ''):
        if k0 in ('PIC','CIC'):
            for part in split0(s0):
                for cid in CARD.findall(mainof(part))[:1]:
                    (TREE_PIC if k0=='PIC' else TREE_CIC)[cid]+=1
AUDIT_INTERNAL={'w.zhonggong-dangshi-jiaoxue-cankao','w.zhonggong-dangshi-jiaoxue-cankao-n-d','w.nongye-jitihua-zhongyao-wenjian','w.zedong-jianguo-yilai-mao-zedong'}
for c0 in list(cards):
    v=cards[c0]
    if not v: continue
    t0=(v['title']+' '+v['script']).lower()
    if 'sanzhong quanhui yilai' in t0 or '三中全会以来' in t0 or 'wenhua dageming" yanjiu ziliao' in t0 or 'wenhua dageming yanjiu ziliao' in t0 or '文化大革命”研究资料' in t0 or '文化大革命研究资料' in t0: AUDIT_INTERNAL.add(c0)
pickle.dump((TREE_PIC,TREE_CIC,AUDIT_INTERNAL),open(SP+'/tree_pic_cic.pkl','wb'))
for sec,e in cal.entries():
    t=str(e.get('thread','')); al=[str(a) for a in (e.get('also') or [])]
    n=e.get('n') or ''
    inthread = t.startswith('china') or any(a.startswith('china') for a in al)
    cited=set(CARD.findall(n))
    citesch = bool(cited & chinese_cards)
    if not (inthread or citesch): continue
    sents=sentences(n)
    ey=ent_year(e)
    kinds=[]; detail=[]; worksinv=set()
    mp=[s for k,s in sents if k=='MP']
    pic=' '.join(s for k,s in sents if k=='PIC')
    cic=' '.join(s for k,s in sents if k=='CIC')
    # cited items in SRC and TC sentences
    cit=[]
    for k,s in sents:
        if k in ('SRC','TC'):
            for cid,y,txt in work_items(s):
                cit.append((k,cid,y,txt,item_kind(cid,txt,ey)))
    # via rows
    vias=[r.split()[1].rstrip(':') for r in ((e.get('src') or {}).get('rows') or []) if isinstance(r,str) and r.startswith('via ')]
    circ_vias=[v for v in vias if (wit.get(v) or {}).get('circulated')]
    rep_vias=[v for v in vias if (wit.get(v) or {}).get('kind') in ('report','memorandum','minutes','telegram','letter','notes','speech','transcript','recording','file','diary')]
    has_int=[x for x in cit if x[4]=='internal']
    has_circ=[x for x in cit if x[4] in ('circulated','circulated?')]
    rec=dict(id=e['id'],date=str(e.get('date')),thread=t,file=sec.file,settled=e['id'] in settled_ids,inthread=inthread,
             mp=' '.join(mp),c=e.get('c',''))
    # ---------- K1: no Made public
    if not mp:
        if pic or cic:
            kinds.append('A1'); detail.append('has "Printed for internal circulation" or "Circulated in China" but no "Made public"')
        elif has_int:
            kinds.append('A2'); detail.append('cites an internal printing, no "Made public"'); worksinv|={x[1] or x[3][:80] for x in has_int}
        elif has_circ or circ_vias:
            kinds.append('A3'); detail.append('cites a Red Guard or small-batch printing, no "Made public"'); worksinv|={x[1] or x[3][:80] for x in has_circ}|set(circ_vias)
        rec['candidate_noMP']=True
    else:
        mps=' '.join(mp)
        # MP items
        mpitems=[]
        for s in mp:
            body=re.sub(r'^Made public[^:]*:\s*','',s)
            for part in split0(body):
                local=None
                m=re.match(r'\s*(in China|abroad|elsewhere|in [A-Z][a-z]+(?: [A-Z][a-z]+)?),\s*',part)
                if m: local=m.group(1)
                cs=CARD.findall(mainof(part))
                ys=[int(x) for x in YR.findall(re.sub(r'NCID \S+','',part))]
                cid=cs[0] if cs else None
                y=None
                if ys: y=min([v for v in ys if v>=ey] or ys)
                elif cid and card_info(cid): y=card_info(cid)['year']
                mpitems.append(dict(local=local,cid=cid,y=y,text=part,kind=item_kind(cid,part,ey)))
        mpy=[i['y'] for i in mpitems if i['y']]
        mpyear=min(mpy) if mpy else None
        rec['mpyear']=mpyear
        if not any(i['cid'] for i in mpitems) and not re.search(r'\*[^*]+\*|《|\[[^\]]+\]\(http',mps):
            kinds.append('F2'); detail.append('"Made public" gives a year but names no work')
        if not any(i['cid'] for i in mpitems) and mpyear and not re.search(r'\*[^*]+\*|《|\[[^\]]+\]\(http',mps):
            cy={x[2] for x in cit if x[2]} | {x[2] for x in cit if x[2]}
            # years of cited works (open or not), and years written in the note
            allys={int(y) for y in YR.findall(re.sub(r'NCID \S+','',n))}
            if mpyear not in cy and mpyear not in allys-{ey}:
                kinds.append('F3'); detail.append(f'"Made public: {mpyear}" names no work, and no work cited carries that year')
            else:
                rec['f2_fix']=sorted({x[1] for x in cit if x[2]==mpyear and x[1]})
        if mpyear is None:
            kinds.append('F'); detail.append('"Made public" names no year or dated work')
        # K2: MP names internal/circulated
        bad=[i for i in mpitems if i['kind'] in ('internal','circulated','circulated?')]
        if bad:
            kinds.append('B'); detail.append('"Made public" names an internal or circulated printing: '+'; '.join((i['cid'] or i['text'][:60]) for i in bad)); worksinv|={i['cid'] or i['text'][:60] for i in bad}
        # earliest open printing cited
        mpcards={i['cid'] for i in mpitems if i['cid']}
        opens=[x for x in cit if x[4] in ('abroad','mainland','unknown') and x[2] and x[2]>=ey and x[1] not in mpcards and (x[1] or x[2]>ey or PRESS_NOW.search(mainof(x[3])))]
        china_now = any(i['local']=='in China' for i in mpitems)
        abroad_now = any(i['local'] in ('abroad','elsewhere') for i in mpitems)
        if mpyear:
            earlier=[x for x in opens if x[2]<mpyear]
            # contemporaneous press: maybe public at the time
            nowpress=[x for x in earlier if x[2]<=ey+1 and (PRESS_NOW.search(mainof(x[3])) or (x[1] and card_info(x[1]) and card_info(x[1]).get('ckind')=='periodical'))]
            if nowpress:
                kinds.append('G'); detail.append('cites a printing of the act\'s own year or the next: '+'; '.join((x[1] or x[3][:60]) for x in nowpress[:3])); worksinv|={x[1] or x[3][:60] for x in nowpress}
            earlier=[x for x in earlier if x not in nowpress]
            e_main=[x for x in earlier if x[4]=='mainland']
            e_abr=[x for x in earlier if x[4] in ('abroad','unknown')]
            mp_main = any(i['kind']=='mainland' for i in mpitems)
            if e_main:
                kinds.append('C'); detail.append('an earlier Chinese printing is cited: '+'; '.join(f"{x[1] or x[3][:60]} ({x[2]})" for x in e_main[:4])+f' before {mpyear}'); worksinv|={x[1] or x[3][:60] for x in e_main}
            if e_abr:
                tr=[x for x in e_abr if (x[1] in ABROAD_CARDS) or ABROAD_SERIES.search(mainof(x[3]))]
                if tr:
                    kinds.append('D1'); detail.append('an earlier translation abroad is cited, not named in "Made public": '+'; '.join(f"{x[1] or x[3][:60]} ({x[2]})" for x in tr[:3])); worksinv|={x[1] or x[3][:60] for x in tr}
                oth=[x for x in e_abr if x not in tr]
                if oth:
                    kinds.append('D3'); detail.append('an earlier work abroad is cited, not named in "Made public": '+'; '.join(f"{x[1] or x[3][:60]} ({x[2]})" for x in oth[:3])); worksinv|={x[1] or x[3][:60] for x in oth}
            # D2: MP abroad only, a later Chinese printing cited, no "in China"
            mp_is_abroad = all(i['kind']=='abroad' for i in mpitems if i['y']) and any(i['kind']=='abroad' and i['y'] for i in mpitems)
            later_main=[x for x in cit if x[4]=='mainland' and x[2] and x[2]>mpyear]
            if mp_is_abroad and later_main and not china_now:
                trans_mp = any(ABROAD_SERIES.search(i['text']) or i['cid'] in ABROAD_CARDS for i in mpitems)
                kinds.append('D2' if trans_mp else 'D4'); detail.append(('"Made public" gives a translation abroad' if trans_mp else '"Made public" gives a work abroad')+', a later Chinese printing is cited, no "in China": '+'; '.join(f"{x[1] or x[3][:60]} ({x[2]})" for x in later_main[:3])); worksinv|={x[1] or x[3][:60] for x in later_main}
        # E: internal cited but no PIC
        for x in has_int:
            key=x[1] or ''
            iy=x[2]
            if key=='w.zedong-jianguo-yilai-mao-zedong':
                mv=re.search(r'jianguo-yilai-mao-zedong\]\],\s*(?:vol\.\s*)?([0-9]+|[IVX]+)\b',x[3])
                v=mv.group(1) if mv else None
                if v and not v.isdigit(): v=str({'IX':9,'X':10,'XI':11,'XII':12,'XIII':13}.get(v,0))
                iy={'9':1996,'10':1996,'11':1996,'12':1998,'13':1998}.get(v or '',1996)
            if iy is None:
                ys=[int(y) for y in YR.findall(mainof(x[3]))]; iy=max(ys) if ys else None
            if mpyear and iy and iy>=mpyear: continue
            if not pic or (key and key not in pic):
                kinds.append('E1'); detail.append('cites an internal printing not noted beside "Made public": '+(x[1] or x[3][:60])); worksinv.add(x[1] or x[3][:60]); break
        circ_missing=[x for x in has_circ if not cic or (x[1] and x[1] not in cic)]
        if circ_missing or (circ_vias and not cic):
            kinds.append('E2'); detail.append('cites a Red Guard or small-batch printing not noted as "Circulated in China": '+'; '.join((x[1] or x[3][:60]) for x in circ_missing[:3])+(' '+' '.join(circ_vias[:2]) if circ_vias and not cic else '')); worksinv|={x[1] or x[3][:60] for x in circ_missing}
        # H: MP rests on a mainland work: record for item 2
        rec['mp_mainland']=[i['cid'] for i in mpitems if i['kind']=='mainland' and i['cid']]
        rec['mp_marking_noted']= bool(re.search(r'marking not seen|内部|CiNii|Xinhua|copyright page',mps+' '.join(s for k,s in sents if k=='CK')))
    rec['kinds']=list(dict.fromkeys(kinds)); rec['detail']=detail; rec['works']=sorted(w for w in worksinv if w)
    rec['cited_cards']=sorted(cited)
    rec['n']=n
    res.append(rec)
pickle.dump(res,open(SP+'/res.pkl','wb'))
cnt=collections.Counter(); cnt_s=collections.Counter()
for r in res:
    for k in r['kinds']:
        (cnt_s if r['settled'] else cnt)[k]+=1
print(len(res), sum(r['inthread'] for r in res), sum(1 for r in res if r['settled']))
print('rest',sorted(cnt.items())); print('settled',sorted(cnt_s.items()))
print('entries with any kind (rest):',sum(1 for r in res if r['kinds'] and not r['settled']))
# ---------- H: an earlier edition with its own card, not cited
import unicodedata
def norm(t): return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',t).lower())
earlier={}
for cid,v in cards.items():
    if not v: continue
    cand=set()
    if v.get('edition_of'): cand.add(v['edition_of'])
    for m in re.finditer(r'(?:edition|ed\.)[^.]{0,80}?\[\[(w\.[^\]]+)\]\]|\[\[(w\.[^\]]+)\]\][^.]{0,40}?edition|(?:edition|ed\.)[^.]{0,80}?\b(w\.[a-z0-9-]+)',v['n']):
        cand.add(m.group(1) or m.group(2) or m.group(3))
    for o,ov in cards.items():
        if ov and o!=cid and ov['title'] and norm(ov['title'])==norm(v['title']) and len(norm(v['title']))>12 and ov['year'] and v['year'] and ov['year']<v['year'] and (ov['chinese']==v['chinese']):
            cand.add(o)
    cand={c for c in cand if c in cards and cards[c] and cards[c]['year'] and v['year'] and cards[c]['year']<v['year']}
    if cand: earlier[cid]=sorted(cand)
pickle.dump(earlier,open(SP+'/earlier.pkl','wb'))
nH=collections.Counter()
for r in res:
    if not r['mp'] or r['settled']: continue
    ey=int(r['date'][:4]); my=r.get('mpyear')
    # the work the MP rests on: card in MP, else the cited card whose year is the MP year
    base=set(CARD.findall(r['mp'])) or set(r.get('f2_fix') or [])
    hits=[]
    for b in base:
        bb=cards.get(b)
        if not bb or bb['year']!=my: continue
        for o in earlier.get(b,[]):
            ov=cards[o]
            if o in r['cited_cards'] or ov['kind']=='internal' or o in AUDIT_INTERNAL or ov['year']<ey: continue
            hits.append(f"{o} ({ov['year']}) before {b} ({bb['year']})")
    if hits:
        r['kinds'].append('H'); r['detail'].append('an earlier edition of the work "Made public" rests on has a card and is not cited: '+'; '.join(hits)); r['works']=sorted(set(r['works'])|{h.split()[0] for h in hits})
        nH[hits[0].split(' before')[0]]+=1
print('H',sum(nH.values()),nH.most_common(15))
print({k:v for k,v in earlier.items() if any(cards[x]['chinese'] for x in v)})
pickle.dump(res,open(SP+'/res.pkl','wb'))
# ---------- A4/A5 and fix H false pairs
from priv import private_candidate, record_candidate, PRESS
for r in res:
    if 'H' in r['kinds'] and all('zhonghua-renmin-gongheguo-waijiao-2001' in d or 'mao-zedong-sixiang-wansui' in d for d in r['detail'] if d.startswith('an earlier edition')):
        i=r['kinds'].index('H'); r['kinds'].pop(i)
        r['detail']=[d for d in r['detail'] if not d.startswith('an earlier edition')]
    if r['mp'] or not r['inthread'] or any(k.startswith('A') for k in r['kinds']): continue
    if record_candidate(r) and not PRESS.search(r['c'] or '') and 'Cong. Rec' not in r['n']:
        r['kinds'].append('A4'); r['detail'].append('no "Made public"; the note rests on an archive file or a record of conversation')
    elif private_candidate(r):
        r['kinds'].append('A5'); r['detail'].append('no "Made public"; the line describes a closed meeting, a talk, an instruction or a letter')
pickle.dump(res,open(SP+'/res.pkl','wb'))
cnt=collections.Counter(k for r in res if not r['settled'] for k in r['kinds'])
print(sorted(cnt.items()))
