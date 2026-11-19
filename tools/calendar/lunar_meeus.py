# The Chinese calendar from Meeus's new moons (ch. 49) and solar longitudes (ch. 25, low precision), Peking time (UTC+8)
import math, datetime
def jde_newmoon(k):
    T=k/1236.85; E=1-0.002516*T-0.0000074*T*T
    jde=2451550.09766+29.530588861*k+0.00015437*T*T-0.00000015*T**3+0.00000000073*T**4
    M=math.radians((2.5534+29.10535670*k-0.0000014*T*T-0.00000011*T**3)%360)
    Mp=math.radians((201.5643+385.81693528*k+0.0107582*T*T+0.00001238*T**3-0.000000058*T**4)%360)
    F=math.radians((160.7108+390.67050284*k-0.0016118*T*T-0.00000227*T**3+0.000000011*T**4)%360)
    Om=math.radians((124.7746-1.56375588*k+0.0020672*T*T+0.00000215*T**3)%360)
    c=(-0.40720*math.sin(Mp)+0.17241*E*math.sin(M)+0.01608*math.sin(2*Mp)+0.01039*math.sin(2*F)+0.00739*E*math.sin(Mp-M)
       -0.00514*E*math.sin(Mp+M)+0.00208*E*E*math.sin(2*M)-0.00111*math.sin(Mp-2*F)-0.00057*math.sin(Mp+2*F)
       +0.00056*E*math.sin(2*Mp+M)-0.00042*math.sin(3*Mp)+0.00042*E*math.sin(M+2*F)+0.00038*E*math.sin(M-2*F)
       -0.00024*E*math.sin(2*Mp-M)-0.00017*math.sin(Om)-0.00007*math.sin(Mp+2*M)+0.00004*math.sin(2*Mp-2*F)
       +0.00004*math.sin(3*M)+0.00003*math.sin(Mp+M-2*F)+0.00003*math.sin(2*Mp+2*F)-0.00003*math.sin(Mp+M+2*F)
       +0.00003*math.sin(Mp-M+2*F)-0.00002*math.sin(Mp-M-2*F)-0.00002*math.sin(3*Mp+M)+0.00002*math.sin(4*Mp))
    return jde+c
def sunlong(jde):
    T=(jde-2451545.0)/36525; L0=280.46646+36000.76983*T+0.0003032*T*T; M=math.radians(357.52911+35999.05029*T-0.0001537*T*T)
    C=(1.914602-0.004817*T-0.000014*T*T)*math.sin(M)+(0.019993-0.000101*T)*math.sin(2*M)+0.000289*math.sin(3*M)
    om=math.radians(125.04-1934.136*T); return (L0+C-0.00569-0.00478*math.sin(om))%360
def jd_to_date(jd):  # civil date in UTC+8 (ignoring ΔT ~35 s in the 1960s)
    return (datetime.datetime(2000,1,1,12)+datetime.timedelta(days=jd-2451545.0+8/24)).date()
def zhongqi_day(target):  # dates (UTC+8) where the sun reaches a multiple of 30 deg
    pass
def principal_terms(y0,y1):
    out=[]; jd=2451545.0+ (datetime.date(y0,1,1)-datetime.date(2000,1,1)).days
    end=2451545.0+(datetime.date(y1,1,1)-datetime.date(2000,1,1)).days
    prev=sunlong(jd)
    while jd<end:
        nxt=jd+0.25; s=sunlong(nxt)
        if int(prev//30)!=int(s//30) and int(s//30)%1==0:
            lo,hi=jd,nxt
            for _ in range(40):
                mid=(lo+hi)/2
                if int(sunlong(mid)//30)==int(prev//30): lo=mid
                else: hi=mid
            if int(s//30)*30 % 30==0: out.append((jd_to_date(hi), int(s//30)*30))
        jd,prev=nxt,s
    return out
def months(y0,y1):
    k0=math.floor((y0-2000)*12.3685)-2; nm=[]
    for k in range(k0, k0+int((y1-y0+1)*12.4)+4): nm.append(jd_to_date(jde_newmoon(k)))
    zq=[(d,l) for d,l in principal_terms(y0-1,y1+2) if l%30==0]  # all 12 principal terms (even multiples of 30 incl. 0,30..)
    zq=[(d,l) for d,l in zq if (l//30)%1==0]
    return nm, zq
