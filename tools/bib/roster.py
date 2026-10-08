"""The styles the rosters share (templates/roster.css): the Congress blocks, the elections and specials, and
the Executive Branch. ensure(page) puts them in the page's head once, with the script that clears a row's highlight."""
import os

from . import store

CSS = os.path.join(store.ROOT, "templates", "roster.css")


# A highlighted row (the target of a link, or a row flashed by a search) goes plain when the reader clicks anywhere
# outside it; the next link followed highlights its own.
JS = """<script id="roster-js">
document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('a[href*="#"]');
  document.querySelectorAll('details.cgr tr:target,details.cgr tr.hit').forEach(function(r){
    if(r.contains(e.target))return;
    if(a&&a.hash==='#'+r.id){r.classList.remove('unhl');return;}   // the link to this row again: keep it
    r.classList.add('unhl');r.classList.remove('hit');
  });
});
window.addEventListener('hashchange',function(){
  document.querySelectorAll('details.cgr tr.unhl').forEach(function(r){r.classList.remove('unhl');});
});
</script>
"""


def ensure(page):
    if 'id="roster-css"' in page:
        return page
    css = f'<style id="roster-css">\n{open(CSS, encoding="utf-8").read()}</style>\n' + JS
    return page.replace("</head>", css + "</head>", 1) if "</head>" in page else css + page
