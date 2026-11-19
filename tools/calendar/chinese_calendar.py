# The Chinese calendar, 1957-72, at Peking (UTC+8): new moons (Meeus, Astronomical Algorithms, ch. 49) and the principal solar terms; month 11 holds the winter solstice; a 13-month year takes as leap the first month with no principal term. Run: python3 -I tools/calendar/chinese_calendar.py (it checks every New Year 1960-70 against the known dates). Used Nov. 19, 2026 to date the 1960 festival and lunar entries.
import math, datetime
from lunar_meeus import jde_newmoon, sunlong
EPOCH=datetime.datetime(2000,1,1,12)
def d8(jde):  # the civil date at Peking (UTC+8) of a JDE (ΔT ~35 s in the 1960s, ignored)
    return (EPOCH+datetime.timedelta(days=jde-2451545.0+8/24-35/86400)).date()
def jde_of(date): return 2451545.0+(datetime.datetime.combine(date,datetime.time(0))-EPOCH).total_seconds()/86400
# new moons
nms=[]
k=math.floor((1958-2000)*12.3685)
while True:
    j=jde_newmoon(k); 
    if d8(j)>datetime.date(1972,3,1): break
    if d8(j)>=datetime.date(1957,10,1): nms.append(d8(j))
    k+=1
# principal terms: sun at multiples of 30 deg
zq=[]
j=jde_of(datetime.date(1957,10,1)); prev=sunlong(j)
while d8(j)<datetime.date(1972,3,1):
    n=j+0.5; s=sunlong(n)
    if int(prev//30)!=int(s//30):
        lo,hi=j,n
        for _ in range(50):
            m=(lo+hi)/2
            if int(sunlong(m)//30)==int(prev//30): lo=m
            else: hi=m
        zq.append((d8(hi), (int(s//30)*30)%360))
    j,prev=n,s
def has_zq(i): return [l for d,l in zq if nms[i]<=d<nms[i+1]]
# label months: month 11 contains the winter solstice (270)
labels={}
w=[i for i in range(len(nms)-1) if 270 in has_zq(i)]
for a,b in zip(w,w[1:]):
    n=b-a; leap_done=False; num=11
    for i in range(a,b):
        if i==a: labels[i]=(11,False); continue
        if n==13 and not leap_done and not has_zq(i):
            labels[i]=(labels[i-1][0],True); leap_done=True; continue
        num=labels[i-1][0]%12+1; labels[i]=(num,False)
def lunar_to_greg(year, month, day, leap=False):
    for i,(m,lp) in labels.items():
        if m==month and lp==leap and nms[i].year in (year, year+1) :
            # the lunar year of month m: month 1 starts the year
            start=nms[i]
            # find the month-1 start of this lunar year
            j=i
            while labels.get(j,(0,0))[0]!=1 or labels[j][1]: j-=1
            if nms[j].year==year: return start+datetime.timedelta(days=day-1)
    return None
known={1960:"1960-01-28",1961:"1961-02-15",1962:"1962-02-05",1963:"1963-01-25",1964:"1964-02-13",1965:"1965-02-02",1966:"1966-01-21",1967:"1967-02-09",1968:"1968-01-30",1969:"1969-02-17",1970:"1970-02-06"}
ok=True
for y,v in known.items():
    g=lunar_to_greg(y,1,1); print(y,g,v, "OK" if str(g)==v else "MISMATCH"); ok&= str(g)==v
print("all CNY match" if ok else "SOME MISMATCH")
print("1960 Dragon Boat (5/5):", lunar_to_greg(1960,5,5))
print("1960 11th month 7th day:", lunar_to_greg(1960,11,7))
print("1960 leap month:", [ (m,str(nms[i])) for i,(m,lp) in sorted(labels.items()) if lp and nms[i].year==1960])
print("1963 CNY (for 'after Chinese New Year'):", lunar_to_greg(1963,1,1))
