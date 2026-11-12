/* The visibility panel's script (tools/bib/vispage.py, STYLE 5-7; the spec, notes/proposals/visibility-spec.md, §5-§7).
   One file for every calendar page and the reader, written beside them as build/vis/vispage-<hash>.js. Every panel on the
   page (one on a year's page; one a year's block in the reader) shares one state, kept in localStorage where the browser
   allows it; each panel counts the claims of its own block. */
(function(){
  'use strict';
  var panels=[].slice.call(document.querySelectorAll('section.vis'));
  if(!panels.length) return;
  var KEY='bib-vis-v1', NEXT={on:'greyed',greyed:'off',off:'on',mixed:'on'}, RANK={off:0,greyed:1,on:2};
  var ALL=[], seen={};
  panels.forEach(function(p){
    var m={top:[],other:[]};
    try{ m=JSON.parse(p.querySelector('script.vismeta').textContent); }catch(e){}
    p._other=m.other.map(function(x){return x[0];});
    m.top.concat(m.other).forEach(function(x){ if(!seen[x[0]]){ seen[x[0]]=1; ALL.push(x[0]); } });
    p._lists=p.closest('section.list');
  });
  function dflt(k){ return k.split('/')[0]==='US'?'on':'greyed'; }
  var st={s:{},pa:'either',pin:'',open:false};
  function get(k){ return st.s[k]||dflt(k); }
  function defaults(){ st.s={}; st.pa='either'; st.pin=''; }
  try{
    var saved=JSON.parse(window.localStorage.getItem(KEY)||'null');
    if(saved&&typeof saved==='object'){
      Object.keys(saved.s||{}).forEach(function(k){ if(/^[A-Za-z0-9_-]+\/(public|nonpublic)$/.test(k)&&saved.s[k] in RANK) st.s[k]=saved.s[k]; });
      if(['p','a','either'].indexOf(saved.pa)>=0) st.pa=saved.pa;
      if(typeof saved.pin==='string'&&/^(\d{4}-\d\d-\d\d)?$/.test(saved.pin)) st.pin=saved.pin;
      st.open=!!saved.open;
    }
  }catch(e){}
  function save(){ try{ window.localStorage.setItem(KEY,JSON.stringify(st)); }catch(e){} }

  function plus1(d){ var t=new Date(d+'T12:00:00Z'); t.setUTCDate(t.getUTCDate()+1); return t.toISOString().slice(0,10); }
  // data-p: "US/P=,1996-10-01/A,= USSR/A=,1996-10-01": a polity, then its P and A spans [nonpublic from, public from];
  // "" none, "=" the claim's own date, "?" public but not known when (vispage.py, STYLE 3)
  function decode(s,d){
    var out={};
    (s||'').split(' ').forEach(function(item){
      if(!item) return;
      var bits=item.split('/'), rec={};
      bits.slice(1).forEach(function(b){
        var v=b.slice(1).split(',').map(function(x){ return x===''?null:x==='='?d:x; });
        rec[b.charAt(0)]=[v[0]||null,v.length>1?v[1]:null];
      });
      out[bits[0]]=rec;
    });
    return out;
  }
  var claims=[].slice.call(document.querySelectorAll('span.cl')).map(function(el){
    var d=el.getAttribute('data-d')||'';
    return {el:el, d:d, r:el.getAttribute('data-r')||(d?plus1(d):''), p:decode(el.getAttribute('data-p'),d),
            x:el.hasAttribute('data-x'), li:el.closest('li'), sec:el.closest('section.list')};
  });
  var lis=[], liIdx=new Map();
  claims.forEach(function(c){ if(c.li&&!liIdx.has(c.li)){ liIdx.set(c.li,lis.length); lis.push({li:c.li,sec:c.sec,day:c.li.closest('.day')}); } });
  var days=[], dayIdx=new Map();
  lis.forEach(function(l){ if(l.day){ if(!dayIdx.has(l.day)){ dayIdx.set(l.day,days.length); days.push({el:l.day,lis:[]}); } days[dayIdx.get(l.day)].lis.push(l); } });

  function status(span,r){                       // vis.py, status(): public, nonpublic or null at r
    if(!span) return null;
    var np=span[0], pub=span[1];
    if(pub&&pub!=='?'&&pub<=r) return 'public';
    if(np&&np<=r) return 'nonpublic';
    return null;
  }
  function tagsAt(c,r){                          // vis.py, tags_at(): [code, status, kinds]; null, not yet known
    if(c.d&&r<c.d) return null;
    if(c.x) return [['US','all','PA']];
    var out=[];
    Object.keys(c.p).forEach(function(code){
      var rec=c.p[code], p=status(rec.P,r), a=status(rec.A,r);
      if(p&&p===a) out.push([code,p,'PA']);
      else { if(p) out.push([code,p,'P']); if(a) out.push([code,a,'A']); }
    });
    return out;
  }
  function itemState(t){
    if(t[1]==='all'){ var a=get('US/public'), b=get('US/nonpublic'); return RANK[a]>=RANK[b]?a:b; }
    if(st.pa==='p'&&t[2].indexOf('P')<0) return null;
    if(st.pa==='a'&&t[2].indexOf('A')<0) return null;
    return get(t[0]+'/'+t[1]);
  }
  function tagText(t){ return t[1]==='all'?'US:all':t[0]+':'+t[1]+'-'+t[2]; }
  window.visTagsAt=function(i,r){ var c=claims[i], ts=tagsAt(c,r||c.r); return ts&&ts.map(tagText); };

  function scopeOf(p){ return panels.length===1?null:p._lists; }
  function apply(){
    var tally=panels.map(function(){ return {full:0,greyed:0,hidden:0,notyet:0,total:0,shown:0,entries:0,per:{OTHER:0}}; });
    var bySec=new Map(); panels.forEach(function(p,i){ bySec.set(scopeOf(p),i); });
    function T(sec){ var i=bySec.has(sec)?bySec.get(sec):bySec.get(null); return i===undefined?null:tally[i]; }
    var liBest=lis.map(function(){ return {r:-1,ny:true}; });
    var other=panels.map(function(p){ return p._other; });
    claims.forEach(function(c){
      var r=st.pin||c.r, ts=tagsAt(c,r), s, t=T(panels.length===1?null:c.sec);
      var oth=t?other[tally.indexOf(t)]:[];
      if(ts===null){ s='greyed'; if(t) t.notyet++; }
      else {
        var seenP={}, o=false, best=-1;
        ts.forEach(function(g){
          var v=itemState(g); if(v===null) return;
          best=Math.max(best,RANK[v]);
          if(t&&!seenP[g[0]]){ seenP[g[0]]=1; t.per[g[0]]=(t.per[g[0]]||0)+1; if(oth.indexOf(g[0])>=0) o=true; }
        });
        if(t&&o) t.per.OTHER++;
        s=best===2?'on':best===1?'greyed':'off';
      }
      c.el.classList.toggle('vg',s==='greyed'); c.el.classList.toggle('vh',s==='off');
      c.el.setAttribute('data-vs',s);
      if(t){ t.total++; t[s==='on'?'full':s==='greyed'?'greyed':'hidden']++; }
      if(c.li){ var b=liBest[liIdx.get(c.li)]; b.r=Math.max(b.r,RANK[s]); b.ny=b.ny&&ts===null; }
    });
    lis.forEach(function(l,i){
      var b=liBest[i], li=l.li, t=T(panels.length===1?null:l.sec);
      li.classList.toggle('vh',b.r===0); li.classList.toggle('vg',b.r===1);
      li.classList.toggle('vny',b.ny&&!!st.pin);
      if(st.pin) li.setAttribute('data-pin',st.pin); else li.removeAttribute('data-pin');
      if(t){ t.entries++; if(b.r>0) t.shown++; }
    });
    days.forEach(function(d){
      d.el.classList.toggle('vq',!d.lis.some(function(l){ return !l.li.classList.contains('vh'); }));
    });
    panels.forEach(function(p,i){
      var n=tally[i], sum=p.querySelector('.vsum');
      p._counts=n;
      sum.innerHTML='Claims: <b>'+n.full+'</b> in full, <b>'+n.greyed+'</b> greyed'+(st.pin?' ('+n.notyet+' not yet known)':'')+
        ', <b>'+n.hidden+'</b> hidden, of '+n.total+'. Entries shown: '+n.shown+' of '+n.entries+'. '+
        (st.pin?'Judged at '+st.pin+'.':'Judged at the time: each claim at its own date and the next morning’s papers.');
    });
    window.visCounts=panels.map(function(p){ var n=p._counts; return {full:n.full,greyed:n.greyed,hidden:n.hidden,notyet:n.notyet,
      total:n.total,entriesShown:n.shown,entries:n.entries}; });
    paint();
  }

  function keysOf(p,b){
    var k=b.getAttribute('data-k'), lvl=b.getAttribute('data-lvl'), codes=k==='OTHER'?p._other:[k], out=[];
    codes.forEach(function(c){
      if(lvl==='line'||lvl==='public') out.push(c+'/public');
      if(lvl==='line'||lvl==='nonpublic') out.push(c+'/nonpublic');
    });
    return out;
  }
  function lineState(keys){
    if(!keys.length) return 'greyed';
    var v=keys.map(get);
    return v.every(function(x){ return x===v[0]; })?v[0]:'mixed';
  }
  function paint(){
    panels.forEach(function(p){
      var per=(p._counts||{per:{}}).per;
      [].forEach.call(p.querySelectorAll('.vt'),function(b){
        var s=lineState(keysOf(p,b)); b.setAttribute('data-s',s);
        b.querySelector('.vs').textContent=s;
        b.setAttribute('aria-label',b.getAttribute('data-name')+': '+s+'. Tap to make it '+NEXT[s]+'.');
        if(b.getAttribute('data-lvl')==='line'){ var el=b.querySelector('.vn'); if(el) el.textContent=per[b.getAttribute('data-k')]||0; }
      });
      [].forEach.call(p.querySelectorAll('.vpa button'),function(b){ b.setAttribute('aria-pressed',String(b.getAttribute('data-pa')===st.pa)); });
      var pin=p.querySelector('.vpinin'); if(pin.value!==st.pin) pin.value=st.pin;
      p.querySelector('.vpinclr').hidden=!st.pin; p.querySelector('.vnote').hidden=!!st.pin;
      var o=p.querySelector('.vother'), f=p.querySelector('.vfold');
      if(o&&f){ o.hidden=!st.open; f.setAttribute('aria-expanded',String(st.open)); f.textContent=(st.open?'Hide':'Show')+' the '+p._other.length+' states'; }
    });
  }
  panels.forEach(function(p){
    p.addEventListener('click',function(ev){
      var b=ev.target.closest('button'); if(!b||!p.contains(b)) return;
      if(b.classList.contains('vt')){ var ks=keysOf(p,b), nx=NEXT[lineState(ks)]; ks.forEach(function(k){ st.s[k]=nx; }); save(); apply(); }
      else if(b.hasAttribute('data-pa')){ st.pa=b.getAttribute('data-pa'); save(); apply(); }
      else if(b.classList.contains('vpinclr')){ st.pin=''; save(); apply(); }
      else if(b.classList.contains('vfold')){ st.open=!st.open; save(); paint(); }
      else if(b.classList.contains('vreset')){ var o=st.open; defaults(); st.open=o; save(); apply(); }
    });
    var pin=p.querySelector('.vpinin');
    pin.addEventListener('change',function(){ st.pin=/^\d{4}-\d\d-\d\d$/.test(pin.value)?pin.value:''; save(); apply(); });
  });
  window.visState=st; window.visApply=apply;
  apply();
})();
