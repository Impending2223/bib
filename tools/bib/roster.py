"""The styles the rosters share (templates/roster.css): the Congress blocks, the elections and specials, and
the Executive Branch. ensure(page) puts them in the page's head once."""
import os

from . import store

CSS = os.path.join(store.ROOT, "templates", "roster.css")


def ensure(page):
    if 'id="roster-css"' in page:
        return page
    css = f'<style id="roster-css">\n{open(CSS, encoding="utf-8").read()}</style>\n'
    return page.replace("</head>", css + "</head>", 1) if "</head>" in page else css + page
