import pickle,re,collections,os,string,itertools
SP='/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad'
res=pickle.load(open(SP+'/res.pkl','rb'))
ORDER=['B','F','F3','E2','E1','C','D1','D2','A2','G','D4','D3','A4','A3','A5','H']
LABEL={'B':'"Made public" names an internal or Red Guard printing',
'F':'"Made public" gives no year',
'F3':'"Made public" year matches no work cited',
'E2':'Red Guard or small-batch printing cited, no "Circulated in China"',
'E1':'internal printing earlier than "Made public" cited, not noted beside it',
'C':'an earlier Chinese printing is cited (the 1993/1997 fault)',
'D1':'an earlier translation abroad is cited; "Made public" names neither it nor each country',
'D2':'"Made public" names a translation abroad; a later Chinese printing is cited; no "in China"',
'A2':'no "Made public"; an internal printing of the act is cited',
'G':'a printing of the act\'s own year or the next is cited (perhaps public at the time)',
'D4':'"Made public" names a work abroad; a later Chinese printing is cited; no "in China"',
'D3':'an earlier work abroad is cited; "Made public" does not name each country',
'A4':'no "Made public"; the note rests on an archive file or a record of conversation',
'A3':'no "Made public"; a Red Guard or small-batch printing is cited',
'A5':'no "Made public"; the line reads as a closed meeting, a talk, an instruction or a letter',
'H':'an earlier edition of the work "Made public" rests on is not cited',
'F2':'"Made public" gives a bare year and names no work'}
rest=[r for r in res if not r['settled']]
batched=[r for r in rest if any(k in ORDER for k in r['kinds'])]
def prim(r): return min((ORDER.index(k) for k in r['kinds'] if k in ORDER))
for r in batched: r['prim']=ORDER[prim(r)]
# day groups: the date field
days=collections.defaultdict(list)
for r in batched: days[r['date']].append(r)
groups=[]
for d,rs in days.items():
    p=min(ORDER.index(r['prim']) for r in rs)
    key2=''
    if ORDER[p]=='H':
        key2=min(re.findall(r'(w\.[a-z0-9-]+) \(\d{4}\) before',' '.join(x for r in rs for x in r['detail'])) or [''])
    groups.append((p,key2,d,sorted(rs,key=lambda r:r['id'])))
PHASE={'B':1,'F':1,'F3':1,'E2':1,'E1':2,'C':3,'D1':4,'D2':4,'A2':4,'G':4,'D4':5,'D3':5,'A4':6,'A3':7,'A5':7,'H':8}
phases=collections.defaultdict(list)
for p,k2,d,rs in groups:
    ph=PHASE[ORDER[p]]
    phases[(ph,k2 if ph==8 else '')].append((d,rs))
def chunk(items,size=60):
    items=sorted(items,key=lambda x:x[0])
    total=sum(len(rs) for d,rs in items)
    nb=max(1,round(total/size)); target=total/nb
    out=[];cur=[]
    for d,rs in items:
        if cur and len(cur)+len(rs)/2>target*(len(out)+1)-sum(len(b) for b in out) and len(out)<nb-1:
            out.append(cur); cur=[]
        cur+=rs
    if cur: out.append(cur)
    return out
batches=[]; phase_of=[]
for key in sorted(phases, key=lambda k:(k[0], -sum(len(rs) for d,rs in phases[k]))):
    for b in chunk(phases[key]):
        batches.append(b); phase_of.append(key)
merged=[];mphase=[]
for b,ph in zip(batches,phase_of):
    if len(b)<20 and merged:
        merged[-1]=merged[-1]+b
    else:
        merged.append(b); mphase.append(ph)
batches,phase_of=merged,mphase
def name(i):
    letters=string.ascii_lowercase
    if i<26: return letters[i]
    return letters[i//26-1]+letters[i%26]
os.makedirs('/home/user/bib/notes/r27',exist_ok=True)
summary=[]
for i,b in enumerate(batches):
    nm=name(i)
    with open(f'/home/user/bib/notes/r27/rest-batch-{nm}.tsv','w') as f:
        f.write('id\tdate\tkind of fault\tcode\tother codes\tworks involved\n')
        for r in b:
            other=','.join(k for k in r['kinds'] if k!=r['prim'])
            works='; '.join(r['works'])[:600].replace('\t',' ').replace('\n',' ')
            f.write(f"{r['id']}\t{r['date']}\t{LABEL[r['prim']]}\t{r['prim']}\t{other}\t{works}\n")
    kc=collections.Counter(r['prim'] for r in b)
    summary.append((nm,len(b),min(r['date'] for r in b),max(r['date'] for r in b),dict(kc),phase_of[i]))
pickle.dump((summary,batched),open(SP+'/batches.pkl','wb'))
for s in summary: print(s)
print(len(batched),len(batches))
pc=collections.Counter(r['prim'] for r in batched); print(sorted(pc.items(),key=lambda x:ORDER.index(x[0])))
