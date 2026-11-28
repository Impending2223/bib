import re
INI=['','b','p','m','f','d','t','n','l','g','k','h','j','q','x','zh','ch','sh','r','z','c','s','y','w']
FIN=['a','o','e','ai','ei','ao','ou','an','en','ang','eng','ong','er','i','ia','ie','iao','iu','ian','in','iang','ing','iong','u','ua','uo','uai','ui','uan','un','uang','ueng','v','ve','ue','van','vn','iou','uei','uen']
SYL=set(i+f for i in INI for f in FIN)
SYL-= {''}
def seg(w):
    w=w.lower()
    n=len(w)
    ok=[False]*(n+1); ok[0]=True
    for i in range(n):
        if not ok[i]: continue
        for L in range(1,7):
            if i+L<=n and w[i:i+L] in SYL: ok[i+L]=True
    return ok[n]
ENG=set('the of and in a to on for from with by at an as is chinese china history mao new war people party life years revolution red'.split())
def is_pinyin_title(t):
    t=re.sub(r'\(.*?\)','',t)
    t=re.sub(r'[‘’\'"“”«»:;,.?!–\-—/\[\]*0-9]',' ',t)
    toks=[x for x in t.split() if x]
    if len(toks)<2: return False
    good=sum(1 for x in toks if x.lower() not in ENG and seg(x))
    return good/len(toks)>=0.75
if __name__=='__main__':
    for t in ['Lin Biao 1959 nian yihou','1949–1989 Niande Zhongguo, 2: Quzhe Fazhande Suiyue (China 1949–1989, 2: Years of tortuous development)','The Origins of the Cultural Revolution','Mao Zedong Sixiang Wan Sui','Zhou Enlai: A Life','Hong Kong and China','Liu Shaoqi nianpu']:
        print(t,is_pinyin_title(t))
