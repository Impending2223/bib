import re, calendar, datetime as dt, sys
SRC=sys.argv[1]; OUT=sys.argv[2]
h=open(SRC).read()
head=h[:h.index('<main class="mock">')]
blocks=h.split('<h2 class="mk">')[1:]
MON='Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
FULL=[calendar.month_name[i] for i in range(13)]
def titles(grid):
    d={}
    for t,n in re.findall(r'<a [^>]*title="([^"]+)"[^>]*>(\d+)</a>',grid):
        m=re.match(r'(\w+) (\d+), (\d+)',t)
        if m: d[(FULL.index(m.group(1)),int(m.group(2)))]=t
    return d
ex=[]
for b in blocks:
    nav=b[b.find('<nav'):b.rfind('</nav>')+6]
    gs=nav.index('<table class="tocg dayg"'); ge=nav.index('</table>',gs)+8
    grid=nav[gs:ge]
    before=nav[:gs].replace('<div class="lb"></div>','')
    after=nav[ge:].replace('<div class="lb"></div>','')
    yth=re.search(r'<tr>(<th scope="rowgroup">.*?</th>)<th class="wd">',grid)
    ex.append(dict(before=before,after=after,T=titles(grid),yth=yth.group(1) if yth else '<th></th>'))
P=[dict(y=1960,ms=range(1,7),start=dt.date(1960,1,6),cur=dt.date(1960,3,15),name='Cal. 1960, first half (Jan. 6–June 30), read at Mar. 15'),
   dict(y=1964,ms=range(7,10),start=dt.date(1964,7,1),cur=dt.date(1964,8,7),name='Cal. 1964, third quarter (July–Sept.), read at Aug. 7')]
def cell(d,p,T,cls=''):
    if d<p['start']: return '<td></td>'
    c=(' class="cur alt"' if cls else ' class="cur"') if d==p['cur'] else cls
    t=T.get((d.month,d.day),f'{FULL[d.month]} {d.day}, {d.year}')
    return f'<td><a{c} href="#" title="{t}">{d.day}</a></td>'
def wd_row(yth): return '<tr>'+yth+''.join(f'<th class="wd">{x}</th>' for x in 'SMTWTFS')+'</tr>'
cal=calendar.Calendar(6)
def grid_breaks(p,e):
    out=['<table class="tocg dayg"><colgroup><col class="y"><col><col><col><col><col><col><col></colgroup><tbody>'+wd_row(e['yth'])+'</tbody>']
    for m in p['ms']:
        rows=[]
        for wk in cal.monthdatescalendar(p['y'],m):
            if all(d.month!=m or d<p['start'] for d in wk): continue
            cells=''.join(cell(d,p,e['T']) if d.month==m else '<td></td>' for d in wk)
            rows.append(cells)
        r=''.join(f'<tr><th>{MON[m-1] if i==0 else ""}</th>{c}</tr>' for i,c in enumerate(rows))
        out.append(f'<tbody class="gap">{r}</tbody>')
    return ''.join(out)+'</table>'
def grid_cont(p,e):
    out=['<table class="tocg dayg"><colgroup><col class="y"><col><col><col><col><col><col><col></colgroup><tbody>'+wd_row(e['yth'])]
    first=dt.date(p['y'],p['ms'][0],1); last=dt.date(p['y'],p['ms'][-1],calendar.monthrange(p['y'],p['ms'][-1])[1])
    d=first-dt.timedelta(days=(first.weekday()+1)%7)
    while d<=last:
        wk=[d+dt.timedelta(i) for i in range(7)]; d+=dt.timedelta(7)
        if all(x<p['start'] or x>last for x in wk): continue
        lab=next((MON[x.month-1] for x in wk if x.day==1 and first<=x<=last),'')
        cells=''.join('<td></td>' if x>last else cell(x,p,e['T'],' class="alt"' if x.month%2==0 else '') for x in wk)
        out.append(f'<tr><th>{lab}</th>{cells}</tr>')
    return ''.join(out)+'</tbody></table>'
ALIGN={'L':'','C':'table.tocg.dayg td,table.tocg.dayg th.wd{text-align:center}\n','R':'table.tocg.dayg td,table.tocg.dayg th.wd{text-align:right}\n'}
CUR={'L':'margin-left:-.25rem','C':'','R':'margin-right:-.25rem'}
V=[('A','Month breaks; numerals right-aligned','R','breaks',None,[1,0]),
   ('B','Month breaks; numerals centred','C','breaks',None,[1]),
   ('C','Month breaks; numerals left-aligned','L','breaks',None,[1]),
   ('D','Continuous weeks; alternate months tinted (the earlier tint)','R','cont','color-mix(in srgb,var(--rule) 30%,transparent)',[1]),
   ('E','Continuous weeks; alternate months on the panel white (--panel)','R','cont','var(--panel)',[1])]
NOTE={'A':'Departure: numerals right-aligned, with the weekday letters set the same way (a number column); the current-day marker pulled back by its own padding so the numeral keeps its place.',
'B':'Departure: numerals and weekday letters centred. The marker is symmetrical, so it needs no adjustment.',
'C':'No departure in alignment: left, as the navigator sets its months. The marker is pulled back by its padding.',
'D':'Departures: as in A, and a tint on alternate months (the earlier mock-up\'s, a 30% mix of the rule colour). The site uses no such tint anywhere else yet.',
'E':'Departures: as in A, and alternate months on the panel white, a colour the site already uses for its panels.'}
css=[]; body=[]
for k,lab,al,kind,tint,which in V:
    sc=f'#v{k} '
    if al!='L': css.append(f'{sc}table.tocg.dayg td,{sc}table.tocg.dayg th.wd{{text-align:{"center" if al=="C" else "right"}}}')
    if CUR[al]: css.append(f'{sc}.tocc table.tocg.dayg a.cur{{{CUR[al]}}}')
    if tint: css.append(f'{sc}table.tocg.dayg td:has(a.alt){{background:{tint}}} {sc}.tocc table.tocg.dayg a.alt{{color:var(--ink)}}')
    body.append(f'<section id="v{k}"><h2 class="mk">{k}. {lab}</h2><p class="mk">{NOTE[k]}</p>')
    for i in which:
        p=P[i]; e=ex[i]
        g=grid_breaks(p,e) if kind=='breaks' else grid_cont(p,e)
        body.append(f'<p class="mk" style="margin-top:{"1.6rem" if i!=which[0] else "0"}">{p["name"]}</p>'+e['before'].replace('</nav>','')+('<div class="lb"></div>' if '<table' in e['before'] else '')+g+'<div class="lb"></div>'+e['after'])
    body.append('</section>')
head=head.replace('table.tocg.dayg{width:100%}\n','').replace('table.tocg.dayg col.yw{width:4.32rem}\n','').replace('.tocc table.tocg.dayg a.cur{background:var(--hl-bg);color:var(--hl-ink);padding:0 .25rem;margin-left:-.25rem}','.tocc table.tocg.dayg a.cur{background:var(--hl-bg);color:var(--hl-ink);padding:0 .25rem}')
head=head.replace('</style>','\n'.join(css)+'\n</style>')
intro='''<h2 class="mk">Day grid at the navigator's width: five alternatives</h2>
<p class="mk">Each grid is the navigator's own table: 27rem wide, the year column 16%, the site's fonts, colours and current-day marker. Months are separated by the gap the navigator already puts between years.</p>
<p class="mk">Departures from the site, in all five: (1) seven columns where the navigator has six, so below the year column the day columns can't line up with the month columns; (2) a weekday row, in the muted colour at regular weight, so it doesn't read as a heading; (3) a blank line before and after the grid; (4) the year label moves onto the weekday row when no months come before the page.</p>'''
open(OUT,'w').write(head+'<main class="mock">'+intro+''.join(body)+'</main>\n')
