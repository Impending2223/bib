"""The month tables' tints and charts (the owner's choice from the chart gallery, Oct. 28, 2026: the heatmap, "the
'hot/inflationary/bullish/high-demand'-sign readings in green and 'cold/deflationary/bearish/weak-demand'-sign readings
in brown"; the FRED-alike, "just the level and year-over-year, and default every chart to year-over-year except the UE
rate and the instrument rates"; both to fit a phone). The prototype: claude.ai artifact "Month Indicators Prototype".

STYLE (settled; keep it):
 1. The tint. A value cell of the economic indicators table and of Money and credit is tinted by its period's move:
    green on the hot side (prices, output, jobs, money, debt or nominal interest rates rising, unemployment falling;
    a real rate falling; a gap below zero), brown on the cold. HOT gives each series' sign; a series not in it is not
    tinted. The move: the change from the period before (chg, chg_now: each column its own), or, for the gaps
    (LEVEL), the level itself. The depth: the move against the series' usual move over the calendar's span, column
    by column: |move| / (2.2 sd), capped at 1, mixed from nothing at 10 percent to 72 at the cap, so a pale cell is
    an ordinary month and a deep one a rare month. A move of exactly zero takes no tint.
 2. The key: one muted line under the indicators table names the tint ("Tint: green, the hot side ...; brown, the
    cold"), once a table.
 3. The chart. A small button before a row's name (▸, "Chart" to screen readers; the name still links to its
    statement of concepts) opens a row beneath it, the table's width: the series over the calendar's span, as first
    reported (solid, the accent) and today (dashed, muted), a band at the row's period; a switch Level | Year over
    year, the default year over year but where the series is a rate or ratio in percent (unemployment, the interest
    rates, the real rates and gaps, the ratios to GNP: LEVEL_DEFAULT, every series whose change is in points); a
    line under it reads the period the pointer is at (the row's own at first). Tapped again, closed.
 4. Year over year: the release's own figure where it printed one (yoy, yoy_now); else, in each column's own figures,
    the change from twelve months (four quarters, a year) before: percent for a level, points for a rate; a first-
    reported figure whose base or unit differs from the year before's (an index rebased) gives none.
 5. Nothing heavy in the page: the figures (one JSON file for all the charted series, build/ind/charts-<hash>.json)
    and uPlot (vendored, sources/vendor/uplot-1.6.30/, MIT; build/ind/) load at the first tap. Opened as a file, not
    through a server, no chart draws.
 6. Charted: every series of the two tables with a single figure a period (not a stacked budget, not the two OMB
    ratios); Oil, the exchange rates, the war and the polls have their own tables and no charts yet.
"""
import calendar
import datetime
import hashlib
import json
import math
import os
import shutil

from . import store

VENDOR = os.path.join(store.ROOT, "sources", "vendor", "uplot-1.6.30")
OUT = os.path.join(store.ROOT, "build", "ind")

HOT = {"cpi": 1, "wpi": 1, "deflator": 1, "unemployment": -1, "payrolls": 1, "industrial-production": 1, "gnp": 1,
       "real-gnp": 1, "public-debt": 1, "debt-gnp": 1, "money-m1": 1, "money-m1-time": 1, "money-m2": 1,
       "discount-rate": 1, "federal-funds": 1, "prime-rate": 1, "treasury-bill": 1, "treasury-10-year": 1,
       "corporate-aaa": 1, "corporate-baa": 1, "mortgage-fha": 1, "mortgage-conventional": 1,
       "mortgage-conventional-eff": 1, "unit-labor-cost": 1, "compensation-hour": 1,
       "real-bill-cpi": -1, "real-10-cpi": -1, "real-bill": -1, "real-10": -1, "taylor-gap": -1, "rstar-gap": -1,
       "spread": 1}
LEVEL = {"taylor-gap", "rstar-gap"}
SKIP = {"oil-production", "oil-supplied", "oil-trade", "oil-trade-year", "oil-reserves", "fx-sterling", "fx-mark",
        "fx-franc", "gold-london", "debt-gdp-omb", "approval"}
SPAN = ("1960-01-01", "1968-12-31")


def _end(p):
    from .indicators import period_end
    return period_end(p)


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _moves(s, which):
    """The tint's moves over the span: changes, or levels for LEVEL."""
    f = which if s["id"] in LEVEL else {"first": "chg", "now": "chg_now"}[which]
    out = []
    for r in s.get("rows", []):
        if SPAN[0] <= str(_end(r["p"])) <= SPAN[1] and _num(r.get(f)):
            out.append(r[f])
    return f, out


_SD = {}


def _sd(s, which):
    k = (s["id"], which)
    if k not in _SD:
        f, xs = _moves(s, which)
        if len(xs) < 4:
            _SD[k] = (f, None)
        else:
            m = sum(xs) / len(xs)
            sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) if s["id"] not in LEVEL else \
                math.sqrt(sum(x * x for x in xs) / len(xs))
            _SD[k] = (f, sd or None)
    return _SD[k]


def tint(sid, s, r, which):
    """(class, style) for a value cell: STYLE 1. Empty where the series has no sign or the move is missing."""
    sign = HOT.get(sid)
    if not sign or not s:
        return "", ""
    f, sd = _sd(s, which)
    v = r.get(f)
    if sd is None or not _num(v) or v == 0:
        return "", ""
    z = min(abs(v) / sd / 2.2, 1.0)
    cls = "tH" if (v > 0) == (sign > 0) else "tC"
    return cls, f"--tz:{round(10 + 62 * z)}%"


def chartable(sid, s):
    if sid in SKIP or not s or s.get("kind") in ("war", "poll") or s.get("fields"):
        return False
    return any(_num(r.get("first")) or _num(r.get("now")) for r in s.get("rows", []))


def level_default(sid, s):
    return sid == "unemployment" or s.get("kind") in ("rate", "derived") or s.get("change") == "pts"


def _back(s):
    return {"M": 12, "Q": 4}.get(s.get("freq"), 1)


def _yoy(s, rows, i, field):
    r = rows[i]
    own = r.get("yoy" if field == "first" else "yoy_now")
    if _num(own):
        return own
    k = i - _back(s)
    if k < 0 or not _num(r.get(field)) or not _num(rows[k].get(field)):
        return None
    if field == "first" and rows[k].get("unit") != r.get("unit"):
        return None
    a, b = r[field], rows[k][field]
    if s.get("change") == "pts" or s.get("kind") in ("rate", "derived"):
        return round(a - b, 2)
    return round((a / b - 1) * 100, 2) if b else None


def payload(data):
    out = {}
    for sid, s in data.items():
        if not chartable(sid, s):
            continue
        rows = sorted((r for r in s["rows"] if SPAN[0] <= str(_end(r["p"])) <= SPAN[1]), key=lambda r: _end(r["p"]))
        if not rows:
            continue
        ts = [calendar.timegm(_end(r["p"]).timetuple()) for r in rows]
        num = lambda v: v if _num(v) else None
        unit = (s.get("now") or {}).get("unit") or next((r.get("unit") for r in rows if r.get("unit")), "")
        out[sid] = {"n": s["name"], "t": ts, "p": [str(r["p"]) for r in rows],
                    "a": [num(r.get("first")) for r in rows], "b": [num(r.get("now")) for r in rows],
                    "ya": [_yoy(s, rows, i, "first") for i in range(len(rows))],
                    "yb": [_yoy(s, rows, i, "now") for i in range(len(rows))],
                    "u": unit, "lv": level_default(sid, s),
                    "yy": "pts" if (s.get("change") == "pts" or s.get("kind") in ("rate", "derived")) else "pct"}
    return out


def _put(rel, data):
    path = os.path.join(store.ROOT, "build", rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(data)
    return rel


def assets(data):
    """Write the charts' figures and uPlot beside the pages (STYLE 5); their paths from a page."""
    body = json.dumps(payload(data), separators=(",", ":")).encode()
    js = open(os.path.join(VENDOR, "uPlot.iife.min.js"), "rb").read()
    return (_put(f"ind/charts-{hashlib.sha1(body).hexdigest()[:10]}.json", body),
            _put("ind/uPlot-1.6.30.iife.min.js", js))


def button(sid):
    return f'<button type="button" class="ich" data-s="{sid}" aria-expanded="false" aria-label="Chart">▸</button>'


KEY = ('<p class="ind-key"><span class="sw tH" style="--tz:60%"></span> the hot side (prices, output, jobs, money, '
       'debt or rates rising; unemployment falling; a real rate falling) · <span class="sw tC" style="--tz:60%"></span> '
       'the cold; deeper, a rarer move. ▸ opens the series\' chart.</p>')


def css():
    up = open(os.path.join(VENDOR, "uPlot.min.css"), encoding="utf-8").read()
    return """<style>
:root{--ind-hot:#2E7D4F;--ind-cold:#8A5A2B}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--ind-hot:#5DBB86;--ind-cold:#C9955E}}
:root[data-theme="dark"]{--ind-hot:#5DBB86;--ind-cold:#C9955E}
div.ind td.tH{background:color-mix(in srgb,var(--ind-hot) var(--tz),transparent)}
div.ind td.tC{background:color-mix(in srgb,var(--ind-cold) var(--tz),transparent)}
div.ind .ind-key{margin:.25rem 0 0;font-family:var(--sans);font-size:.72rem;color:var(--muted)}
div.ind .ind-key .sw{display:inline-block;width:1.6em;height:.8em;vertical-align:-.05em;border:1px solid var(--rule)}
div.ind .ind-key .sw.tH{background:color-mix(in srgb,var(--ind-hot) var(--tz),transparent)}
div.ind .ind-key .sw.tC{background:color-mix(in srgb,var(--ind-cold) var(--tz),transparent)}
div.ind button.ich{all:unset;cursor:pointer;color:var(--muted);font-size:.8em;padding:0 .3em 0 0;display:inline-block;transition:transform .15s}
div.ind button.ich[aria-expanded="true"]{transform:rotate(90deg)}
div.ind button.ich:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
div.ind tr.ichd>td{padding:.4rem 0 .8rem;white-space:normal}
div.ind .ich-tools{display:flex;flex-wrap:wrap;gap:.3rem .8rem;align-items:center;font-size:.75rem;color:var(--muted);margin-bottom:.3rem}
div.ind .ich-seg{display:inline-flex;border:1px solid var(--rule);border-radius:5px;overflow:hidden}
div.ind .ich-seg button{all:unset;cursor:pointer;padding:.15rem .55rem;color:var(--ink)}
div.ind .ich-seg button+button{border-left:1px solid var(--rule)}
div.ind .ich-seg button[aria-pressed="true"]{background:var(--ink);color:var(--bg)}
div.ind .ich-key i{display:inline-block;width:16px;border-top:2px solid var(--accent);vertical-align:middle;margin:0 .3em 0 .6em}
div.ind .ich-key i.d{border-top:2px dashed var(--muted)}
div.ind .ich-box{width:100%;min-height:190px}
div.ind .ich-ro{font-size:.75rem;color:var(--ink);margin-top:.2rem;min-height:1.2em}
""" + up + "\n</style>"


SCRIPT = r"""<script>
(function(){
var DATA=null,LIB=null;
function load(cfg){
  if(!LIB)LIB=new Promise(function(ok,no){var s=document.createElement("script");s.src=cfg.lib;s.onload=ok;s.onerror=no;document.head.appendChild(s);});
  if(!DATA)DATA=fetch(cfg.data).then(function(r){return r.json();});
  return Promise.all([LIB,DATA]).then(function(x){return x[1];});
}
function tok(n){return getComputedStyle(document.documentElement).getPropertyValue(n).trim()||"#888";}
var MON=["Jan.","Feb.","Mar.","Apr.","May","June","July","Aug.","Sept.","Oct.","Nov.","Dec."];
function plab(p){if(/^\d{4}-\d{2}$/.test(p))return MON[+p.slice(5,7)-1]+" "+p.slice(0,4);var m=/^(\d{4})Q(\d)$/.exec(p);return m?"Q"+m[2]+" "+m[1]:p;}
function fmt(v,yoy,S){if(v==null)return "—";var s=(Math.abs(v)<10?v.toFixed(2):Math.abs(v)<1000?v.toFixed(1):Math.round(v).toLocaleString());if(yoy)return (v>0?"+":"")+s+(S.yy=="pct"?"%":" pt");return s+(S.lv&&/percent|pts|points/.test(S.u||"percent")?"%":"");}
function open(btn,cfg){
  var tr=btn.closest("tr"),nx=tr.nextElementSibling;
  if(nx&&nx.classList.contains("ichd")){nx.remove();btn.setAttribute("aria-expanded","false");return;}
  btn.setAttribute("aria-expanded","true");
  var d=document.createElement("tr");d.className="ichd";var td=document.createElement("td");td.colSpan=tr.children.length;d.appendChild(td);tr.after(d);
  td.innerHTML='<div class="ich-tools"><span class="ich-seg"><button type="button" data-m="level">Level</button><button type="button" data-m="yoy">Year over year</button></span><span class="ich-key"><i></i>as first reported<i class="d"></i>today</span></div><div class="ich-box"></div><div class="ich-ro">Loading…</div>';
  var sid=btn.dataset.s,per=(tr.querySelector(".per")||{}).textContent||"";
  load(cfg).then(function(all){
    var S=all[sid];if(!S){td.querySelector(".ich-ro").textContent="No figures to chart.";return;}
    var mode=S.lv?"level":"yoy",u=null,box=td.querySelector(".ich-box"),ro=td.querySelector(".ich-ro");
    var here=S.p.map(plab).indexOf(per.trim());
    function say(i){if(i==null||i<0){ro.textContent="";return;}var y=mode=="yoy";ro.textContent=plab(S.p[i])+": as first reported "+fmt((y?S.ya:S.a)[i],y,S)+"; today "+fmt((y?S.yb:S.b)[i],y,S)+(y?" from a year before":"");}
    function draw(){
      var y=mode=="yoy",a=y?S.ya:S.a,b=y?S.yb:S.b;
      td.querySelectorAll(".ich-seg button").forEach(function(x){x.setAttribute("aria-pressed",String(x.dataset.m==mode));});
      if(u){u.destroy();u=null;}
      var w=Math.max(260,box.clientWidth||td.clientWidth||320);
      var opts={width:w,height:190,legend:{show:false},cursor:{y:false,points:{size:6}},scales:{x:{time:true}},
        axes:[{stroke:tok("--muted"),grid:{stroke:tok("--rule"),width:1},ticks:{stroke:tok("--rule")},font:"11px sans-serif"},
              {stroke:tok("--muted"),grid:{stroke:tok("--rule"),width:1},ticks:{stroke:tok("--rule")},size:46,font:"11px sans-serif"}],
        series:[{},{stroke:tok("--accent"),width:1.6,spanGaps:false,points:{show:false}},{stroke:tok("--muted"),width:1.4,dash:[4,3],spanGaps:false,points:{show:false}}],
        hooks:{setCursor:[function(uu){say(uu.cursor.idx==null?here:uu.cursor.idx);}],
               drawClear:[function(uu){if(here<0)return;var ctx=uu.ctx,x=uu.valToPos(S.t[here],"x",true),x2=here+1<S.t.length?uu.valToPos(S.t[here+1],"x",true):x+4;var x1=here>0?uu.valToPos(S.t[here-1],"x",true):x-4;ctx.save();ctx.fillStyle=tok("--rule");ctx.globalAlpha=.55;ctx.fillRect((x1+x)/2,uu.bbox.top,Math.max(3,(x2-x1)/2),uu.bbox.height);ctx.restore();}]}};
      u=new uPlot(opts,[S.t,a,b],box);say(here);
    }
    td.querySelectorAll(".ich-seg button").forEach(function(x){x.addEventListener("click",function(){mode=x.dataset.m;draw();});});
    draw();
    var ro2=new ResizeObserver(function(){if(u){var w=Math.max(260,box.clientWidth);if(Math.abs(w-u.width)>8)u.setSize({width:w,height:190});}});ro2.observe(box);
  }).catch(function(){td.querySelector(".ich-ro").textContent="The chart could not be loaded (opened as a file? serve the pages).";});
}
document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest("button.ich");if(!b)return;e.preventDefault();open(b,window.ICH);});
})();
</script>"""


def head_and_tail(data):
    """The page's additions: styles in the head; the chart's paths and script before the body's end."""
    dpath, lpath = assets(data)
    tail = (f'<script>window.ICH={{data:{json.dumps(dpath)},lib:{json.dumps(lpath)}}};</script>' + SCRIPT)
    return css(), tail


def problems():
    out = []
    for f in ("uPlot.iife.min.js", "uPlot.min.css", "LICENSE"):
        if not os.path.exists(os.path.join(VENDOR, f)):
            out.append(("indchart", f"sources/vendor/uplot-1.6.30/{f}: missing"))
    return out
