"""Card table: language, place, printing kind, year, and where the kind is recorded."""
import sys, re, os, glob, json, yaml, collections, pickle
sys.path.insert(0,'/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad')
from pinyin import is_pinyin_title
sys.path.insert(0,'/home/user/bib/tools')
from bib import works as W
ROOT='/home/user/bib'
SP='/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad'
cat=W.Catalogue(ROOT)
CJK=re.compile(r'[㐀-鿿]')
def txt(c):
    return ' '.join(str(c.get(k) or '') for k in ('title','script','trans','paren','n','c','year','journal','short'))+' '+' '.join(map(str,(c.get('author') or [])+(c.get('editor') or [])))
ABROAD=re.compile(r'Hong Kong|Hongkong|Xianggang|香港|Taipei|Taibei|Tai-?pei|臺北|台北|Taiwan|臺灣|台灣|Mirror Books|Mingjing|明鏡|明镜|Tiandi tushu|天地圖書|天地图书|Cosmos Books|Chinese University|Zhongwen daxue|中文大學|中文大学|Union Research|Youlian|友聯|友联|Carle Place|New York|London|Stockholm|Universities Service Centre|Zhongguo wenge lishi wenku|Kaifang|開放|Xin dalu|新大陸|Shidai guoji|時代國際|Dafeng|大風|Mingbao|明報|Ming Pao|Zhongbao|Taiyuan chubanshe|Tianyuan shuwu|天元書屋|Xinshiji|新世紀|New Century|Kaixin|Wenhua jiaoyu chubanshe youxian|Joint Publishing \(H|Sanlian shudian \(Xianggang|Xianggang Sanlian|Princeton|Harvard|Cambridge|Oxford|Stanford|Berkeley|Armonk|M\. ?E\. Sharpe|Washington|JPRS|Joint Publications|Current Background|Survey of China Mainland|Selections from China Mainland|Chinese Law and Government|American Consulate|Consulate General|Center for Chinese Research Materials|Paris|Tokyo|Moscow|Kyoto',re.I)
INTERNAL=re.compile(r'内部|內部|neibu|internal circulation|internal printing|internal distribution|internally circulated|党内发行|黨內發行|机密|機密|for official use|nei bu|internal use',re.I)
NOINT=re.compile(r'no 内部|no 內部|no internal|No 内部|without 内部|sold through Xinhua|新华书店经销|新華書店|新华书店发行|Xinhua shudian|open printing|open trade|open sale|新華書店発行|新华书店',re.I)
REDGUARD=re.compile(r'Red Guard|紅衛兵|红卫兵|wansui|萬歲|万岁|Hongweibing|zaofan|造反|dazibao|大字報|大字报|tabloid|wall poster|leaflet|传单|傳單|work unit|faction|Zhongyang shouzhang|中央首長|中央首长|shouzhang jianghua|首長講話|首长讲话|Gaoju Mao Zedong|cankao ziliao|參考資料|参考资料|Pipan ziliao|批判資料|批判资料|Dadao|打倒|Qiandao wangua|千刀萬剮|Ziliao xuanbian|資料選編|资料选编|Xuexi wenjian|學習文件|学习文件|Xuexi ziliao|學習資料|学习资料|Wuchanjieji wenhua dageming|無產階級文化大革命|无产阶级文化大革命|Wenge tongxun|Hongqi zhandou|bingtuan|兵團|兵团|zongbu|總部|总部|silingbu|司令部|lianluozhan|聯絡站|联络站|fan geming xiuzhengzhuyi|反革命修正主義|反革命修正主义',re.I)
def year_of(c):
    y=str(c.get('year') or '')
    m=re.findall(r'(1[89]\d\d|20[0-3]\d)',y)
    if not m: return None, y
    rng = bool(re.search(r'\d{4}\s*[–-]\s*\d',y)) or len(m)>1
    return int(m[0]), ('range' if rng else '')
# book-check files
bc={}
for f in glob.glob(ROOT+'/notes/book-checks/*.md'):
    t=open(f).read()
    base=os.path.basename(f)[:-3]
    cid=base if base.startswith('w.') else 'w.'+base
    ids=set(re.findall(r'`(w\.[a-z0-9-]+)`',t[:3000]))|({cid} if cat.get(cid) else set())
    for i in ids:
        bc.setdefault(i,[]).append((base,t))
cards={}
for cid,c in cat.cards.items():
    t=txt(c)
    y,rng=year_of(c)
    chinese=is_pinyin_title(str(c.get('title') or '')) or bool(CJK.search(str(c.get('script') or '')+str(c.get('title') or '')+' '.join(map(str,(c.get('author') or [])+(c.get('editor') or [])))))
    abroad=bool(ABROAD.search(t))
    kind=None; basis=[]
    if INTERNAL.search(t) and not re.search(r'no 内部|no 內部|no internal',t,re.I): kind='internal'; basis.append('card')
    elif REDGUARD.search(str(c.get('title') or '')+' '+str(c.get('script') or '')+' '+str(c.get('trans') or '')+' '+str(c.get('n') or '')) and (y is None or 1966<=y<=1970): kind='circulated'; basis.append('card')
    if NOINT.search(t): basis.append('card: open')
    for base,bt in bc.get(cid,[]):
        own = base==cid[2:] or base==cid
        hit=None
        for m in re.finditer(r'[Nn]o 内部|[Nn]o 內部|[Nn]o internal|新华书店经销|新華書店經銷|sold through Xinhua|open (trade|printing|sale|Western)',bt):
            win=bt[max(0,m.start()-600):m.start()]
            if cid in win[-150:] or (own and not re.search(r'w\.[a-z0-9-]+',win[-400:].replace(cid,''))):
                hit='open'; break
        if hit: basis.append('book-check: open ('+base+')')
    cards[cid]=dict(year=y,rng=rng,chinese=chinese,abroad=abroad,kind=kind,basis=basis,title=str(c.get('title') or ''),script=str(c.get('script') or ''),
                    edition_of=c.get('edition_of'),translates=c.get('translates'),n=str(c.get('n') or ''),paren=str(c.get('paren') or ''),ckind=c.get('kind'),journal=c.get('journal'))
for a,cid in cat.alias.items(): cards.setdefault(a,cards.get(cid))
pickle.dump(cards,open(SP+'/cards.pkl','wb'))
cc=collections.Counter((v['chinese'],v['abroad'],v['kind']) for k,v in cards.items() if v)
print(cc)
print(sum(1 for v in cards.values() if v and v['basis']))
