"""The days' folded materials, loaded when opened (daybook STYLE 14).

A calendar page (cal.html, cal63.html, cal66.html) and the reader (series.html) keep, under each day, only the closed
blocks' summaries ("Documents: PPP 3, FRUS 12"; "Other records: Committees 9, Bulletin 2"). The blocks' contents go to
a file a month beside the page, build/days/<page>-<YYYY-MM>-<hash>.json, {"<day>d": html, "<day>o": html} (d the
Documents, o the Other records), named by its content's hash so a cache never serves an old month. The page carries
the months' file names and the anchors the files hold (<script type="application/json" id="lzmap">), and a small
script (SCRIPT):

  - a block opened (by a tap, Expand all, or a link) fetches its month once and fills every block of that month;
    while it loads, its summary says "loading"; a failed fetch says so and is tried again at the next opening;
  - Expand all queues the months from the button's month on, then the months before it, two at a time;
  - a link to an anchor inside an unloaded block (by the map) loads its month, opens the blocks around it, and goes
    there; the reader's jump asks window.lzGo first.

split() runs on the finished page (after the injects and the routing, before smart.write); the contents are curled as
the page's text is (smart.py). `./bib links` reads the month files with their page (fragments()).
"""
import glob
import hashlib
import json
import os
import re

from . import smart

SUB = "days"
TOK = re.compile(r'<div class="day" id="d(\d{4}-\d\d-\d\d)">'
                 r'|<details class="(docs[^"]*)"><summary>(.*?)</summary>(.*?)</details>', re.S)
IDS = re.compile(r'\sid="([^"]+)"')


def split(page, name, out):
    """The page with its day blocks emptied, each month's contents written to out/days/ (the module's docstring)."""
    if '<details class="docs' not in page:
        return page
    months, ix, parts, pos, day = {}, {}, [], 0, None
    for m in TOK.finditer(page):
        if m.group(1):
            day = m.group(1)
            continue
        if day is None:
            continue
        mon = day[:7]
        key = day + ("o" if " or" in f' {m.group(2)}' else "d")
        body = smart.smarten("0" + m.group(4))[1:]       # curled as in the page: the summary ends in a digit
        months.setdefault(mon, {})[key] = body
        for a in IDS.findall(body):
            ix[a] = mon
        parts.append(page[pos:m.start()])
        parts.append(f'<details class="{m.group(2)}" data-lz="{mon}"><summary>{m.group(3)}</summary></details>')
        pos = m.end()
    if not months:
        return page
    parts.append(page[pos:])
    page = "".join(parts)
    d = os.path.join(out, SUB)
    os.makedirs(d, exist_ok=True)
    files = {}
    for mon, blocks in sorted(months.items()):
        text = json.dumps(blocks, ensure_ascii=False, separators=(",", ":"))
        h = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
        f = f"{SUB}/{name}-{mon}-{h}.json"
        files[mon] = f
        p = os.path.join(out, f)
        if not os.path.exists(p):
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(text)
    keep = {os.path.basename(f) for f in files.values()}
    for p in glob.glob(os.path.join(d, f"{name}-[0-9][0-9][0-9][0-9]-[0-9][0-9]-*.json")):
        if os.path.basename(p) not in keep:
            os.remove(p)
    lzmap = json.dumps({"m": files, "ix": ix}, separators=(",", ":")).replace("</", "<\\/")
    page = page.replace("</head>", STYLE + "\n</head>", 1)
    return page.replace("</body>", f'<script type="application/json" id="lzmap">{lzmap}</script>\n{SCRIPT}\n</body>', 1)


def fragments(path):
    """The HTML of the month files a built page names (for ./bib links): '' for a page without them."""
    text = open(path, encoding="utf-8").read()
    m = re.search(r'<script type="application/json" id="lzmap">(.*?)</script>', text, re.S)
    if not m:
        return ""
    out = []
    for f in json.loads(m.group(1).replace("<\\/", "</"))["m"].values():
        p = os.path.join(os.path.dirname(path), f)
        if os.path.exists(p):
            out.extend(json.load(open(p, encoding="utf-8")).values())
    return "\n".join(out)


STYLE = """<style>
details.docs.lzw>summary::after{content:" \\00b7 loading";font-style:italic}
details.docs.lzx>summary::after{content:" \\00b7 not loaded; close and open again";font-style:italic}
</style>"""

SCRIPT = """<script>
(function(){
  var MAP=null, wait={}, queue=[], busy=0;
  function map(){ if(!MAP){ var s=document.getElementById('lzmap'); MAP=s?JSON.parse(s.textContent):{m:{},ix:{}}; } return MAP; }
  function blocks(m){ return document.querySelectorAll('details[data-lz="'+m+'"]'); }
  function fill(m,data){
    [].forEach.call(blocks(m),function(d){
      var day=d.closest('.day'), h=day&&data[day.id.slice(1)+(d.classList.contains('or')?'o':'d')];
      if(h!=null) d.insertAdjacentHTML('beforeend',h);
      d.removeAttribute('data-lz'); d.classList.remove('lzw','lzx');
    });
    clearTimeout(window.__lzT); window.__lzT=setTimeout(function(){window.dispatchEvent(new Event('resize'));},60);
  }
  function pump(){
    while(busy<2&&queue.length){
      var job=queue.shift(), m=job.m, f=map().m[m];
      if(!f){ job.done.forEach(function(cb){cb(false);}); continue; }
      busy++;
      (function(job){
        fetch(f).then(function(r){ if(!r.ok) throw new Error(r.status); return r.json(); })
        .then(function(data){ fill(job.m,data); job.ok=true; })
        .catch(function(){ [].forEach.call(blocks(job.m),function(d){ if(d.open){ d.classList.remove('lzw'); d.classList.add('lzx'); } }); })
        .then(function(){ busy--; delete wait[job.m]; job.done.forEach(function(cb){cb(job.ok);}); pump(); });
      })(job);
    }
  }
  // a month's file, once; first: ahead of the queue (a block the reader opened alone, a link)
  function load(m,first,cb){
    if(!blocks(m).length){ if(cb) cb(true); return; }
    var job=wait[m];
    if(!job){ job=wait[m]={m:m,done:[]}; if(first) queue.unshift(job); else queue.push(job); }
    else if(first&&queue.indexOf(job)>0){ queue.splice(queue.indexOf(job),1); queue.unshift(job); }
    if(cb) job.done.push(cb);
    pump();
  }
  document.addEventListener('toggle',function(ev){
    var d=ev.target;
    if(d.open&&d.matches&&d.matches('details[data-lz]')){ var m=d.getAttribute('data-lz'); d.classList.remove('lzx'); d.classList.add('lzw'); load(m,!wait[m]); }
  },true);
  // Expand all: the months from the button's on, then those before it (daybook.SCRIPT opens the blocks)
  document.addEventListener('click',function(ev){
    var b=ev.target.closest&&ev.target.closest('p.dtog button');
    if(!b||b.getAttribute('data-docs')!=='1') return;
    var all=[].slice.call((b.closest('section.list')||document).querySelectorAll('details[data-lz]')), ms=[], seen={}, at=0;
    all.forEach(function(d,i){ var m=d.getAttribute('data-lz'); if(!seen[m]){ seen[m]=1; ms.push(m); }
      if(!at&&(b.compareDocumentPosition(d)&Node.DOCUMENT_POSITION_FOLLOWING)) at=ms.length; });
    ms=ms.slice(at?at-1:0).concat(ms.slice(0,at?at-1:0));
    ms.forEach(function(m){ load(m,false); });
  },true);
  // a link to an anchor in a month not yet loaded: load it, open what holds the anchor, go there
  function go(id){
    if(!id||document.getElementById(id)) return false;
    var m=map().ix[id]; if(!m) return false;
    load(m,true,function(){
      var el=document.getElementById(id); if(!el) return;
      for(var d=el.closest('details');d;d=d.parentElement&&d.parentElement.closest('details')) d.open=true;
      el.scrollIntoView();
      if(decodeURIComponent(location.hash.slice(1))===id) window.dispatchEvent(new HashChangeEvent('hashchange'));
    });
    return true;
  }
  window.lzGo=go;
  function fromHash(){ go(decodeURIComponent(location.hash.slice(1))); }
  window.addEventListener('hashchange',fromHash);
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',fromHash); else fromHash();
})();
</script>"""
