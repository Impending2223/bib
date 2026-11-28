import pickle,re,collections,glob
SP='/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad'
res=pickle.load(open(SP+'/res.pkl','rb'))
cards=pickle.load(open(SP+'/cards.pkl','rb'))
for _c in ('w.li-wang-li-fansi-lu','w.song-yongyi-zhongguo-wenhua-dageming-wenku'): cards[_c]['abroad']=True
TREE_PIC,TREE_CIC,AUDIT_INTERNAL=pickle.load(open(SP+'/tree_pic_cic.pkl','rb'))
summary,batched=pickle.load(open(SP+'/batches.pkl','rb'))
bids={r['id'] for r in batched}
CARD=re.compile(r'\[\[(w\.[^\]|]+)\]\]')
calt=''.join(open(f).read() for f in glob.glob('/home/user/bib/lists/cal/*.yaml'))
bear=[r for r in res if not r['settled'] and (r['mp'] or r['kinds'] or 'Printed for internal' in r['n'] or 'Circulated in' in r['n'])]
use=collections.Counter(); rest=collections.Counter(); flag=collections.Counter()
for r in bear:
    base=set(CARD.findall(r['mp'])) | set(r.get('f2_fix') or [])
    for c in set(r['cited_cards']):
        v=cards.get(c)
        if not v or not v['chinese'] or v['abroad']: continue
        use[c]+=1
        if c in base: rest[c]+=1
        if r['id'] in bids: flag[c]+=1
MAN={
 'w.yang-shangkun-riji':'open; copyright page read (2017 ed.)',
 'w.zhu-de-nianpu-xinbian':'open; copyright page read','w.chen-yun-nianpu-xiuding':'open; copyright page read','w.chen-yi-nianpu':'open; copyright page read',
 'w.peng-dehuai-nianpu':'open; copyright page read','w.liu-jixian-ye-jianying-nianpu':'open; copyright page read','w.deng-xiaoping-nianpu-1904':'open; copyright page read',
 'w.shaoqi-liu-shaoqi-nianpu-chronology':'open; copyright page of vol. 2 read (the R27 audit)','w.nianyi-da-dongluande-niandai':'open; copyright page read (the R27 redo)',
 'w.jin-1949-1989-niande-zhongguo':'open; copyright page read (the R27 redo)','w.jianguo-yilai-zhongyao-wenxian':'open; copyright pages of vols. 13 and 14 read; the other volumes not seen',
 'w.peng-zhen-nianpu-1902':'open; no copyright page in the scan; cover and catalogue show an open sale',
 'w.xianzhi-mao-zedong-zhuan-1949':'open by its catalogue record (the R27 audit); copyright page not seen','w.xiaoping-deng-xiaoping-wenxuan-1938':'open by its catalogue record (sold through Xinhua)',
 'w.zhou-enlai-waijiao-huodong':'copyright page read (book-check), marking not written down','w.zhou-enlai-nianpu-1949-2020':'copyright page read (book-check), marking not written down',
 'w.lengxi-shinian-lunzhan-1956-1966':'copyright page read (book-check), marking not written down','w.zhonghua-renmin-gongheguo-waijiao':'copyright page read (book-check), marking not written down',
 'w.zhonghua-renmin-gongheguo-waijiao-2001':'imprint and CIP on the card, marking not written down','w.mao-zedong-zhuan':'imprints of the epub read, marking not written down',
 'w.jianguo-yilai-mao-zedong':'not recorded (the series calls it "the first open printing"; its copyright page is not described)',
 'w.shangkun-yang-shangkun-riji-2':'not recorded (only the 2017 edition\'s copyright page was read)',
}
AUD_CAT={'w.lin-biao-1959-nian','w.yunsheng-maojiawan-jishi','w.shinian-houde-pingshuo','w.gailong-dangdai-zhongguo-zhengzhi-dashidian','w.zhonghua-renmin-gongheguo-zuzhi','w.bianjibu-dangdai-zhongguode-hebei-contemporary','w.chuncai-peng-dehuai-zai-san','w.xin-ban-guangming-ribao-shinian'}
def status(c):
    v=cards[c]
    if c in MAN: return MAN[c]
    if c in AUDIT_INTERNAL or v['kind']=='internal' or (TREE_PIC[c] and not TREE_CIC[c]): return 'internal; recorded'
    if v['kind']=='circulated' or TREE_CIC[c]: return 'Red Guard or small-batch; recorded'
    if v['year'] and 1966<=v['year']<=1970 and v.get('ckind')!='periodical': return 'presumed Red Guard or small-batch (a Chinese printing of 1966–70); not recorded'
    t=v['n']+' '+v['paren']
    if re.search(r'no 内部|no 內部|no internal|sold through Xinhua|新华书店|新華書店|Xinhua shudian',t,re.I): return 'open; recorded on the card'
    if c in AUD_CAT or re.search(re.escape('[['+c+']]')+r'[^\[\n]{0,120}?CiNii',calt): return 'catalogue record only (no internal mark noted); copyright page not seen'
    if re.search(re.escape('[['+c+']]')+r'[^\]\n]{0,60}?marking not seen',calt): return 'not recorded ("marking not seen" in its entries)'
    return 'not recorded'
rows=[]
for c,n in use.most_common():
    v=cards[c]
    rows.append((c,v['title'],v['script'],v['year'] or '',n,rest[c],flag[c],status(c)))
with open('/home/user/bib/notes/r27/rest-works.tsv','w') as f:
    f.write('card\ttitle\tcharacters\tyear\tR27 entries citing it\tentries whose "Made public" rests on it\tentries in the batches citing it\tkind of printing, as recorded\n')
    for r in rows: f.write('\t'.join(str(x).replace('\t',' ') for x in r)+'\n')
cnt=collections.Counter(r[7].split(';')[0].split(' (')[0] for r in rows)
print(cnt)
nr=[r for r in rows if r[7].startswith('not recorded') or 'not written down' in r[7] or r[7].startswith('presumed') or r[7].startswith('catalogue')]
print('to rule on',len(nr), 'entries touched', sum(r[4] for r in nr))
for r in nr[:45]: print(r[0],r[3],r[4],r[5],r[6],'|',r[7])
pickle.dump(rows,open(SP+'/works_final.pkl','wb'))
