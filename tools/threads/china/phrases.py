import json,re,collections
E=[json.loads(l) for l in open('china.jsonl')]
E=[e for e in E if e['thread'] in ('china-leadership','china') or 'india-and-china-cultural-revolution' in e['also']]
cap=collections.Counter(); ttl=collections.Counter(); quo=collections.Counter(); num=collections.Counter()
SMALL=r'(?:of|the|and|on|for|to|in|at|de|a)'
W=r"[A-Z][a-z'’\-]+|[A-Z]{2,}|[0-9]+(?:th|st|nd|rd)"
pat=re.compile(rf"(?:(?:{W})(?:\s+(?:{SMALL}\s+)*(?:{W}))+)")
numpat=re.compile(r"\b(?:Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve|Fifteen|Sixteen|Seventeen|Twenty|Twenty-three|Thirty|Forty|Fifty|Sixty|Seventy|Seven Thousand|Hundred|Thousand|First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth)(?:[\s-][A-Za-z]+){1,3}",re.I)
for e in E:
    c=re.sub(r'[㐀-鿿　-〿＀-￯]+','',e['c'])
    for m in set(pat.findall(c)): cap[m]+=1
    for m in set(re.findall(r'《([^》]{1,40})》',e['c'])): ttl[m]+=1
    for m in set(re.findall(r'"([^"]{3,60})"',c)): quo[m]+=1
    for m in set(numpat.findall(c)): num[m.strip()]+=1
json.dump({'cap':cap.most_common(1500),'ttl':ttl.most_common(300),'quo':quo.most_common(300),'num':num.most_common(400)},open('phrases.json','w'),ensure_ascii=False,indent=0)
for k,C in (('cap',cap),('ttl',ttl),('quo',quo),('num',num)):
    print('==',k); print('; '.join(f'{a} {b}' for a,b in C.most_common(250 if k in('cap','num') else 80)))
