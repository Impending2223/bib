#!/usr/bin/env python3
"""The visibility panel, a prototype (notes/proposals/visibility-spec.md, §9.2): one month's calendar page, standalone,
with the panel of §6 at its head and each claim its own span carrying its tags and dates (§7). It does not touch the
site's build: nothing is written under build/, the templates and the build code are only called.

    python3 tools/vis/prototype.py [--month 1962-10] [--out PATH]

STYLE
 1. The month is rendered by the site's own code (tools/bib/build.py's build_list and the calendar's injects, as
    build.run does for a year's page), with the page's sections narrowed to the threads section (the threads with an
    entry in the month) and the month itself. The days' folded blocks stay inline (no lazydays.split: no month files
    beside a standalone page). The quotation marks are curled as smart.write curls them.
 2. Each calendar entry's `c` is rendered unit by unit (tools/bib/claims.py, STYLE 1), a span a claim (class `cl`) with:
    data-u, the unit's letter (`all` where the entry is one claim); data-d, the claim's date; data-t, its tags at the
    time (tools/bib/vis.py, STYLE 6); data-p, its polities' P and A spans, [nonpublic from, public from], as JSON, for
    the script to judge at a pin; data-um, unmapped; data-x, nothing computable (the placeholder `US:all`). Where the
    units, rendered and joined, do not give back the entry's own rendering, the entry is one span, unmapped, its
    claims' spans merged (the earliest of each date): counted in the report.
 3. The panel (§6) after the contents, above the threads. Polities a cell each (US, USSR, China, France, Germany, UK;
    Other, its states folded below: those any of the month's claims names); public and nonpublic indented under each.
    A polity's own line sets both its sub-items (it reads "mixed" where they differ); Other's lines set every other
    state's. Each toggle cycles on, greyed, off, its state in words. The P/A switch: by provenance, by address, either.
    The pin: a date; empty, "at the time".
 4. The rule (§6): a claim shows in full if any of its tags is on, greyed if none is on and one is greyed, hidden if all
    are off. A tag's item is its polity's public or nonpublic; under "by provenance" only its P counts, under "by
    address" only its A; `US:all` is the US's public and nonpublic both, under any switch. At a pin before a claim's
    date, the claim is greyed and marked as not yet known, whatever the toggles (§5). An entry takes its claims'
    fullest state; greyed, its note is greyed with it; hidden, it is hidden.
 5. Links the standalone page cannot hold (another year's page, a day of 1962 outside October, the site's other pages)
    point to the site (SITE).
"""
import argparse
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from bib import store, build, calsplit, contents, daybook, smart, vis   # noqa: E402
from bib import claims as C                                              # noqa: E402

SITE = "https://impending2223.github.io/bib/"
TOP = [("us", "US"), ("ussr", "USSR"), ("prc", "China"), ("fr", "France"), ("frg", "Germany"), ("uk", "UK")]
DEFAULT_OUT = "/tmp/claude-0/-home-user-bib/0eff10cc-e92b-525c-82ae-0e08a8f79d60/scratchpad/vis-proto"
STATS = {"entries": 0, "claims": 0, "merged": 0, "unmapped": 0, "placeholder": 0}
USED = set()          # the polities' tag codes any claim of the month carries (at any date)


def esc(t):
    return html.escape(str(t), quote=True)


def merge_pols(cls):
    """The claims' polities merged: for each polity and P/A, the earliest nonpublic and public dates."""
    out = {}
    for cl in cls:
        for X, rec in (cl.get("polities") or {}).items():
            o = out.setdefault(X, {})
            for k, (np_from, pub) in rec.items():
                a, b = o.get(k, [None, None])
                a = min([x for x in (a, np_from) if x] or [None])
                dated = [x for x in (b, pub) if x and x != "?"]
                b = min(dated) if dated else (b or pub)
                o[k] = [a, b]
    return out


def pol_json(pol):
    """{TAG: {P: [np, pub], A: [np, pub]}}, the codes the page's script reads."""
    out = {}
    for X in sorted(pol, key=vis.order_key):
        code = vis.tag_code(X)
        USED.add(code)
        out[code] = {k: v for k, v in pol[X].items()}
    return json.dumps(out, separators=(",", ":"))


def claim_span(inner, cl, unit, pol):
    tags = " ".join(cl["tags"])
    for t in cl["tags"]:
        USED.add(t.split(":")[0])
    a = [f'data-u="{esc(unit)}"', f'data-d="{esc(cl.get("date") or "")}"', f'data-t="{esc(tags)}"',
         f'data-p="{esc(pol_json(pol))}"']
    if cl["unmapped"]:
        a.append('data-um="1" title="Unmapped: filtered as a whole entry, not claim by claim"')
    if not cl["computed"]:
        a.append('data-x="1"')
    return f'<span class="cl" {" ".join(a)}>{inner}</span>'


def install(series, lst, month):
    """The site's renderer, narrowed to the month (STYLE 1) and its entries split into claims (STYLE 2)."""
    sec = next(s for s in lst.sections if str(s.extra.get("from", ""))[:7] == month)
    half = calsplit.half_of_section(lst, sec)
    members = build.thread_members(lst)
    orig_half_sections = build.half_sections

    def half_sections(l, h):
        out = []
        for s in orig_half_sections(l, h):
            if not s.extra.get("from"):                      # the threads section: the month's threads only
                import copy
                c = copy.copy(s)
                c.entries = [e for e in s.entries
                             if any(str(m.get("date", ""))[:7] == month
                                    for t in store.as_list(e.get("see") or e["id"].split(".", 2)[2])
                                    for m in members.get(t, []))]
                out.append(c)
            elif s is sec:
                out.append(s)
        return out
    build.half_sections = half_sections

    orig_entry_html = build.entry_html

    def entry_html(series_, lst_, sec_, e, text_html, extra_attrs="", extra_spans="", rubric=None):
        page = orig_entry_html(series_, lst_, sec_, e, text_html, extra_attrs, extra_spans, rubric)
        if (lst_.kind != "calendar" or e["id"].startswith(f"{lst_.key}.thread.") or not isinstance(e.get("c"), str)
                or not e.get("c")):
            return page
        year = (e.get("date") or "")[:4]
        lead = rubric or ""
        whole = text_html(build.year_qualified(series_, e["c"], year), "c")
        old = f'<span class="c">{lead}{whole}</span>'
        if old not in page:
            return page
        cls = vis.compute(series_, lst_, e)
        STATS["entries"] += 1
        parts = [text_html(build.year_qualified(series_, cl["text"], year), "c") for cl in cls]
        if len(cls) > 1 and re.sub(r"\s+", " ", " ".join(parts)) != re.sub(r"\s+", " ", whole):
            STATS["merged"] += 1
            one = dict(cls[0], unmapped=True, computed=any(c["computed"] for c in cls),
                       tags=sorted({t for c in cls for t in c["tags"]}))
            spans = [claim_span(whole, one, "all", merge_pols(cls))]
            STATS["claims"] += 1
            STATS["unmapped"] += 1
            STATS["placeholder"] += 0 if one["computed"] else 1
        else:
            spans = []
            for cl, inner in zip(cls, parts):
                spans.append(claim_span(inner, cl, cl["unit"], cl.get("polities") or {}))
                STATS["claims"] += 1
                STATS["unmapped"] += 1 if cl["unmapped"] else 0
                STATS["placeholder"] += 0 if cl["computed"] else 1
        new = f'<span class="c">{lead}{" ".join(spans)}</span>'
        return page.replace(old, new, 1).replace("<li ", '<li data-cl="1" ', 1)
    build.entry_html = entry_html
    return sec, half


def render(series, month):
    """The month's page as the site renders a year's (build.run's calendar chain), narrowed (STYLE 1)."""
    from bib import (appropriations, bills, budgets, congress, conventions, dayblocks, executive, feeds, governors,
                     indicators, legislatures, oilworld, primaries, specials, statefin, vnmap)
    lst = next(l for l in series.lists.values() if l.kind == "calendar")
    sec, half = install(series, lst, month)
    daybook.SERIES = series
    linker = build.Linker(series)
    contents.FOUND.clear()
    calsplit.CUR.update(half=half, mode="list")
    page = build.build_list(series, lst.key, linker, half)
    page = congress.inject(page, series, linker, "list")
    page = executive.inject(page, series, linker, "list")
    for m in (specials, primaries, conventions, governors, legislatures, oilworld, statefin, budgets, bills,
              appropriations, vnmap):
        page = m.inject(page, series)
    page = indicators.inject(page, series, "list")
    page = dayblocks.inject(page, series, "list")
    page = daybook.inject(page)
    page = feeds.inject(page, lst, half)
    page = contents.finish(page, lst, half, defer=True)
    page = contents.fill(page, lst, half)
    page = page.replace("</head>", calsplit.STYLE + "\n</head>", 1)
    page = page.replace("</body>", calsplit.SCRIPT + "\n</body>", 1)
    page = calsplit.route(page, lst, half)
    calsplit.CUR.update(half=None)
    return page, lst, sec, half


def site_links(page, own):
    """Links the standalone page cannot hold, to the site (STYLE 5)."""
    ids = set(re.findall(r'\sid="([^"]+)"', page))

    def fix(m):
        h = html.unescape(m.group(2))
        if h.startswith("#"):
            if h[1:] in ids or not h[1:]:
                return m.group(0)
            return f'{m.group(1)}"{esc(SITE + own + ".html" + h)}"'
        if re.match(r"^(?:[a-z][a-z0-9+.-]*:|//)", h):
            return m.group(0)
        return f'{m.group(1)}"{esc(SITE + h)}"'
    return re.sub(r'(\shref=)"([^"]*)"', fix, page)


# ---------------------------------------------------------------- the panel

PANEL_CSS = r"""
<style>
/* the visibility panel (tools/vis/prototype.py; the spec, §6) */
#vis{margin:1.6rem 0 0;padding:.9rem .9rem 1rem;border:1px solid var(--rule);border-radius:10px;background:var(--panel);font-family:var(--sans)}
#vis h3{margin:0 0 .25rem;padding-top:0;border-top:0;font-size:1.05rem}
#vis p.logic{margin:.15rem 0 .7rem;font-size:.8rem}
#vis .vgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.55rem .45rem}
@media (min-width:700px){#vis .vgrid{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media (min-width:560px) and (max-width:699px){#vis .vgrid{grid-template-columns:repeat(3,minmax(0,1fr))}}
#vis .vcell{min-width:0;display:flex;flex-direction:column;gap:.2rem}
#vis .vt{display:flex;align-items:baseline;justify-content:space-between;gap:.25rem;width:100%;min-width:0;min-height:34px;
  font:inherit;font-size:.82rem;line-height:1.15;text-align:left;cursor:pointer;color:var(--ink);
  background:transparent;border:1px solid var(--rule);border-radius:6px;padding:.38rem .5rem}
#vis .vt.sub{margin-left:.6rem;width:calc(100% - .6rem);font-size:.78rem;min-height:30px;padding:.3rem .35rem .3rem .45rem}
#vis .vt .vl{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#vis .vt.top .vl{font-weight:700}
#vis .vt .vn{color:var(--muted);font-weight:400;font-size:.72rem;margin-left:.25rem}
#vis .vt .vs{flex:none;font-size:.62rem;font-weight:700;letter-spacing:.02em;text-transform:uppercase;border-radius:4px;padding:.08rem .22rem}
/* on: solid, the accent; greyed: dashed, muted; off: struck through, hollow; mixed: half */
#vis .vt[data-s="on"]{border-color:var(--accent);box-shadow:inset 3px 0 0 var(--accent)}
#vis .vt[data-s="on"] .vs{background:var(--accent);color:var(--panel)}
#vis .vt[data-s="greyed"]{border-style:dashed;color:var(--muted)}
#vis .vt[data-s="greyed"] .vs{border:1px dashed var(--muted);color:var(--muted)}
#vis .vt[data-s="off"]{color:var(--muted);opacity:.75}
#vis .vt[data-s="off"] .vl{text-decoration:line-through;text-decoration-thickness:1px}
#vis .vt[data-s="off"] .vs{border:1px solid var(--rule);color:var(--muted)}
#vis .vt[data-s="mixed"] .vs{border:1px solid var(--accent);color:var(--accent)}
#vis .vfold{font:inherit;font-size:.74rem;margin-left:.6rem;width:calc(100% - .6rem);text-align:left;background:none;border:0;
  color:var(--accent);cursor:pointer;padding:.25rem .1rem}
#vother{margin-top:.6rem;padding-top:.6rem;border-top:1px dashed var(--rule)}
#vother[hidden]{display:none}
#vis .vbar{display:flex;flex-wrap:wrap;gap:.6rem 1.1rem;align-items:center;margin-top:.85rem;padding-top:.75rem;border-top:1px solid var(--rule)}
#vis .vbar .lab{font-size:.78rem;font-weight:700;margin-right:.35rem}
#vis .vpa{display:inline-flex;border:1px solid var(--rule);border-radius:6px;overflow:hidden}
#vis .vpa button{font:inherit;font-size:.78rem;background:transparent;color:var(--ink);border:0;border-left:1px solid var(--rule);padding:.4rem .55rem;cursor:pointer;min-height:32px}
#vis .vpa button:first-child{border-left:0}
#vis .vpa button[aria-pressed="true"]{background:var(--accent);color:var(--panel);font-weight:700}
#vis .vpin{display:inline-flex;align-items:center;gap:.35rem;flex-wrap:wrap}
#vis .vpin input{font:inherit;font-size:.82rem;padding:.3rem .4rem;border:1px solid var(--rule);border-radius:6px;background:var(--bg);color:var(--ink);min-height:32px;max-width:11rem}
#vis .vpin button,#vis .vreset{font:inherit;font-size:.76rem;border:1px solid var(--rule);background:var(--bg);color:var(--ink);border-radius:6px;padding:.3rem .55rem;cursor:pointer;min-height:32px}
#vis .vsum{margin:.7rem 0 0;font-size:.8rem;color:var(--muted)}
#vis .vfoot{display:flex;gap:.6rem;align-items:flex-start;justify-content:space-between}
#vis .vfoot .vreset{flex:none;margin-top:.55rem}
#vis .vnote{font-size:.76rem;color:var(--muted)}
#vis .vsum b{color:var(--ink)}
:root{color-scheme:light dark}
/* the claims */
.cl[data-um]{text-decoration:underline dotted;text-decoration-color:color-mix(in srgb,var(--muted) 55%,transparent);text-decoration-thickness:1px;text-underline-offset:.28em}
.cl.vg{opacity:.36}
.cl.vh{display:none}
li.vh{display:none !important}
li.vg>.n,li.vg>.tn,li.vg>.r,li.vg>.gl,li.vg .rub{opacity:.36}
li.vny::before{content:"not yet known at " attr(data-pin);display:block;font-family:var(--sans);font-size:.7rem;font-weight:600;letter-spacing:.03em;color:var(--muted);text-transform:uppercase}
.day.vq>.dh{opacity:.45}
</style>
"""

PANEL_JS = r"""
<script>
/* the visibility panel (tools/vis/prototype.py, STYLE 3-4; the spec, §5-§7) */
(function(){
  var KEY='bib-vis-proto-v1', META=JSON.parse(document.getElementById('vismeta').textContent);
  var CODES=META.top.map(function(p){return p[0];}).concat(META.other.map(function(p){return p[0];}));
  var OTHER=META.other.map(function(p){return p[0];});
  var NEXT={on:'greyed',greyed:'off',off:'on',mixed:'on'}, RANK={off:0,greyed:1,on:2};
  var st={s:{},pa:'either',pin:'',open:false};
  function defaults(){
    st.s={};
    CODES.forEach(function(c){var d=c==='US'?'on':'greyed'; st.s[c+'/public']=d; st.s[c+'/nonpublic']=d;});
    st.pa='either'; st.pin='';
  }
  defaults();
  try{
    var saved=JSON.parse(localStorage.getItem(KEY)||'null');
    if(saved&&saved.s){
      Object.keys(st.s).forEach(function(k){ if(saved.s[k] in RANK) st.s[k]=saved.s[k]; });
      if(['p','a','either'].indexOf(saved.pa)>=0) st.pa=saved.pa;
      if(typeof saved.pin==='string'&&/^(\d{4}-\d\d-\d\d)?$/.test(saved.pin)) st.pin=saved.pin;
      st.open=!!saved.open;
    }
  }catch(e){}
  function save(){ try{ localStorage.setItem(KEY,JSON.stringify(st)); }catch(e){} }

  var claims=[].slice.call(document.querySelectorAll('span.cl')).map(function(el){
    var p={}; try{ p=JSON.parse(el.getAttribute('data-p')||'{}'); }catch(e){}
    return {el:el, d:el.getAttribute('data-d'), t:(el.getAttribute('data-t')||'').split(' ').filter(Boolean), p:p,
            x:el.hasAttribute('data-x'), li:el.closest('li')};
  });
  var lis=[]; claims.forEach(function(c){ if(c.li&&lis.indexOf(c.li)<0) lis.push(c.li); });

  function plus1(d){ var t=new Date(d+'T12:00:00Z'); t.setUTCDate(t.getUTCDate()+1); return t.toISOString().slice(0,10); }
  function status(span,r){                       // vis.py, status(): public, nonpublic or null at r
    if(!span) return null;
    var np=span[0], pub=span[1];
    if(pub&&pub!=='?'&&pub<=r) return 'public';
    if(np&&np<=r) return 'nonpublic';
    return null;
  }
  function tagsAt(c,r){                          // vis.py, tags_at(): [code, status, kinds]
    if(c.x) return [['US','all','PA']];
    if(c.d&&r<c.d) return null;                  // not yet known
    var out=[];
    Object.keys(c.p).forEach(function(code){
      var rec=c.p[code], p=status(rec.P,r), a=status(rec.A,r);
      if(p&&p===a) out.push([code,p,'PA']);
      else { if(p) out.push([code,p,'P']); if(a) out.push([code,a,'A']); }
    });
    return out;
  }
  function itemState(tag){
    if(tag[1]==='all') return RANK[st.s['US/public']]>=RANK[st.s['US/nonpublic']]?st.s['US/public']:st.s['US/nonpublic'];
    if(st.pa==='p'&&tag[2].indexOf('P')<0) return null;
    if(st.pa==='a'&&tag[2].indexOf('A')<0) return null;
    return st.s[tag[0]+'/'+tag[1]]||'greyed';
  }
  function tagText(t){ return t[1]==='all'?'US:all':t[0]+':'+t[1]+'-'+t[2]; }
  window.visTagsAt=function(i,r){ var c=claims[i], ts=tagsAt(c,r||plus1(c.d)); return ts&&ts.map(tagText); };

  var per={};                                   // claims carrying a tag of each polity at the reference
  function apply(){
    var n={full:0,greyed:0,hidden:0,notyet:0}, liBest=new Map();
    per={OTHER:0};
    claims.forEach(function(c){
      var r=st.pin||plus1(c.d), ts=tagsAt(c,r), s;
      if(ts===null){ s='greyed'; n.notyet++; }
      else {
        var seen={}, oth=false;
        ts.forEach(function(t){ if(itemState(t)!==null&&!seen[t[0]]){ seen[t[0]]=1; per[t[0]]=(per[t[0]]||0)+1; if(OTHER.indexOf(t[0])>=0) oth=true; } });
        if(oth) per.OTHER++;
        var best=-1;
        ts.forEach(function(t){ var v=itemState(t); if(v!==null) best=Math.max(best,RANK[v]); });
        s=best===2?'on':best===1?'greyed':'off';
      }
      c.el.classList.toggle('vg',s==='greyed'); c.el.classList.toggle('vh',s==='off');
      c.el.setAttribute('data-vs',s);
      n[s==='on'?'full':s==='greyed'?'greyed':'hidden']++;
      if(c.li){ var b=liBest.get(c.li)||{r:-1,ny:true}; b.r=Math.max(b.r,RANK[s]); b.ny=b.ny&&ts===null; liBest.set(c.li,b); }
    });
    var shownLi=0;
    lis.forEach(function(li){
      var b=liBest.get(li);
      li.classList.toggle('vh',b.r===0); li.classList.toggle('vg',b.r===1);
      li.classList.toggle('vny',b.ny&&!!st.pin);
      if(st.pin) li.setAttribute('data-pin',st.pin); else li.removeAttribute('data-pin');
      if(b.r>0) shownLi++;
    });
    [].forEach.call(document.querySelectorAll('.day'),function(d){
      var ls=d.querySelectorAll('li[data-cl]'); if(!ls.length) return;
      var any=[].some.call(ls,function(l){return !l.classList.contains('vh');});
      d.classList.toggle('vq',!any);
    });
    window.visCounts={full:n.full,greyed:n.greyed,hidden:n.hidden,notyet:n.notyet,total:claims.length,
                      entriesShown:shownLi,entries:lis.length};
    var sum=document.getElementById('vsum');
    sum.innerHTML='Claims: <b>'+n.full+'</b> in full, <b>'+n.greyed+'</b> greyed'+(st.pin?' ('+n.notyet+' not yet known)':'')+
      ', <b>'+n.hidden+'</b> hidden, of '+claims.length+'. Entries shown: '+shownLi+' of '+lis.length+'. '+
      (st.pin?'Judged at '+st.pin+'.':'Judged at the time: each claim at its own date and the next morning’s papers.');
    paint();
  }

  // the panel's buttons
  function lineState(keys){
    var v=keys.map(function(k){return st.s[k];});
    return v.every(function(x){return x===v[0];})?v[0]:'mixed';
  }
  function keysOf(b){
    var k=b.getAttribute('data-k'), lvl=b.getAttribute('data-lvl'), codes=k==='OTHER'?OTHER:[k];
    var out=[];
    codes.forEach(function(c){
      if(lvl==='line'||lvl==='public') out.push(c+'/public');
      if(lvl==='line'||lvl==='nonpublic') out.push(c+'/nonpublic');
    });
    return out;
  }
  var btns=[].slice.call(document.querySelectorAll('#vis .vt'));
  function paint(){
    btns.forEach(function(b){
      var s=lineState(keysOf(b)); b.setAttribute('data-s',s);
      b.querySelector('.vs').textContent=s;
      b.setAttribute('aria-label',b.getAttribute('data-name')+': '+s+'. Tap to make it '+NEXT[s]+'.');
    });
    [].forEach.call(document.querySelectorAll('#vis .vpa button'),function(b){ b.setAttribute('aria-pressed',String(b.getAttribute('data-pa')===st.pa)); });
    var pin=document.getElementById('vpin'); if(pin.value!==st.pin) pin.value=st.pin;
    document.getElementById('vpinclr').hidden=!st.pin; document.getElementById('vpinnote').hidden=!!st.pin;
    btns.forEach(function(b){
      if(b.getAttribute('data-lvl')!=='line') return;
      var k=b.getAttribute('data-k'), n=per[k]||0;
      var el=b.querySelector('.vn'); if(el) el.textContent=n;
    });
    var o=document.getElementById('vother'), f=document.getElementById('vfold');
    if(o&&f){ o.hidden=!st.open; f.setAttribute('aria-expanded',String(st.open)); f.textContent=(st.open?'Hide':'Show')+' the '+OTHER.length+' states'; }
  }
  btns.forEach(function(b){
    b.addEventListener('click',function(){
      var ks=keysOf(b), nx=NEXT[lineState(ks)];
      ks.forEach(function(k){ st.s[k]=nx; });
      save(); apply();
    });
  });
  [].forEach.call(document.querySelectorAll('#vis .vpa button'),function(b){
    b.addEventListener('click',function(){ st.pa=b.getAttribute('data-pa'); save(); apply(); });
  });
  var pin=document.getElementById('vpin');
  pin.addEventListener('change',function(){ st.pin=/^\d{4}-\d\d-\d\d$/.test(pin.value)?pin.value:''; save(); apply(); });
  document.getElementById('vpinclr').addEventListener('click',function(){ st.pin=''; save(); apply(); });
  var fold=document.getElementById('vfold');
  if(fold) fold.addEventListener('click',function(){ st.open=!st.open; save(); paint(); });
  document.getElementById('vreset').addEventListener('click',function(){ var o=st.open; defaults(); st.open=o; save(); apply(); });
  window.visState=st; window.visApply=apply;
  apply();
})();
</script>
"""


def panel(lst):
    """The panel's HTML (STYLE 3) and the polities it lists."""
    pol = vis.polities()["polities"]
    by_code = {vis.tag_code(k): k for k in pol}
    top_codes = [vis.tag_code(k) for k, _ in TOP]
    others = sorted(c for c in USED if c not in top_codes and c != "US")

    def label(code):
        name = (pol.get(by_code.get(code)) or {}).get("name") or code
        return (name if len(name) <= 14 or len(code) > 8 else code), name

    def cell(code, short, full):
        return (f'<div class="vcell" role="group" aria-label="{esc(full)}">'
                f'<button type="button" class="vt top" data-k="{esc(code)}" data-lvl="line" data-name="{esc(full)}" '
                f'title="{esc(full)} ({esc(code)}): the claims carrying its tags"><span class="vl">{esc(short)}<span class="vn"></span></span>'
                f'<span class="vs">on</span></button>'
                f'<button type="button" class="vt sub" data-k="{esc(code)}" data-lvl="public" data-name="{esc(full)}, public">'
                f'<span class="vl">public</span><span class="vs">on</span></button>'
                f'<button type="button" class="vt sub" data-k="{esc(code)}" data-lvl="nonpublic" '
                f'data-name="{esc(full)}, nonpublic"><span class="vl">nonpublic</span><span class="vs">on</span></button></div>')

    cells = []
    for k, short in TOP:
        code = vis.tag_code(k)
        full = (pol.get(k) or {}).get("name") or short
        cells.append(cell(code, short, full))
    other_meta = []
    ocells = []
    for code in others:
        short, full = label(code)
        other_meta.append([code, short])
        ocells.append(cell(code, short, full))
    oc = cell("OTHER", "Other", "Every other state")[:-len("</div>")]    # its cell, with the fold under it
    oc += (f'<button type="button" class="vfold" id="vfold" aria-controls="vother" aria-expanded="false">'
           f'Show the {len(others)} states</button></div>')
    meta = {"top": [[vis.tag_code(k), s] for k, s in TOP], "other": other_meta}
    return (f'<section id="vis" aria-labelledby="visibility">'
            f'<h3 id="visibility" data-short="Visibility">Visibility</h3>'
            f'<p class="logic">Whose record each claim is, and who knew it. Tap a toggle to cycle it: on, greyed, off. A claim '
            f'shows in full if any of its tags is on; greyed if none is on and one is greyed; hidden if all are off. '
            f'A polity\'s own line sets its public and nonpublic both. A dotted underline: an unmapped entry, filtered as a whole.</p>'
            f'<div class="vgrid">{"".join(cells)}{oc}</div>'
            f'<div id="vother" hidden><div class="vgrid">{"".join(ocells)}</div></div>'
            f'<div class="vbar"><div><span class="lab" id="vpalab">Tags by</span><span class="vpa" role="group" '
            f'aria-labelledby="vpalab"><button type="button" data-pa="p">provenance</button>'
            f'<button type="button" data-pa="a">address</button><button type="button" data-pa="either">either</button></span></div>'
            f'<div class="vpin"><label class="lab" for="vpin">Pin date</label><input type="date" id="vpin" min="1960-01-01" '
            f'max="2030-12-31" aria-describedby="vpinnote"><span class="vnote" id="vpinnote">empty: at the time</span>'
            f'<button type="button" id="vpinclr" hidden>Clear: at the time</button></div></div>'
            f'<div class="vfoot"><p class="vsum" id="vsum" aria-live="polite"></p>'
            f'<button type="button" class="vreset" id="vreset">Defaults</button></div></section>'
            f'<script type="application/json" id="vismeta">{json.dumps(meta)}</script>')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--month", default="1962-10")
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    out = a.out or os.path.join(DEFAULT_OUT, f"vis-prototype-{a.month}.html")
    smart_write = smart.write
    smart.write = lambda *x, **k: (_ for _ in ()).throw(RuntimeError("the prototype writes nothing to build/"))
    try:
        series = store.Series()
        page, lst, sec, half = render(series, a.month)
    finally:
        smart.write = smart_write
    own = calsplit.page_key(lst, half)
    title = f"{sec.title}: visibility (prototype)"
    page = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", page, count=1, flags=re.S)
    page = page.replace('<div id="crumb"><b>', f'<div id="crumb"><b>{esc(sec.title)}, prototype · ', 1)
    # the panel after the contents, above the threads (§6)
    i = page.find('<h3 id="contents"')
    j = page.find("</nav>", i)
    if i < 0 or j < 0:
        raise SystemExit("no contents on the page")
    j += len("</nav>")
    page = page[:j] + "\n" + panel(lst) + page[j:]
    page = page.replace("</head>", PANEL_CSS + "</head>", 1)
    page = page.replace("</body>", PANEL_JS + "</body>", 1)
    page = site_links(page, own)
    page = smart.smarten(page)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(out, f"{len(page) // 1024} KB")
    print("entries split into claims:", STATS["entries"], " claims:", STATS["claims"], " unmapped:", STATS["unmapped"],
          " placeholder US:all:", STATS["placeholder"], " entries merged to one span:", STATS["merged"])
    print("polities the month's claims carry:", " ".join(sorted(USED)))


if __name__ == "__main__":
    main()
