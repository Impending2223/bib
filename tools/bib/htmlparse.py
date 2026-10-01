"""A small DOM for reading the published pages back in (import only)."""
from html.parser import HTMLParser

VOID = {"br", "img", "input", "meta", "link", "hr", "polyline"}


class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag = tag
        self.attrs = dict(attrs)
        self.parent = parent
        self.children = []

    @property
    def classes(self):
        return (self.attrs.get("class") or "").split()

    def elements(self):
        return [c for c in self.children if isinstance(c, Node)]

    def find_all(self, pred):
        for c in self.elements():
            if pred(c):
                yield c
            yield from c.find_all(pred)

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)


class _Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {})
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def parse(text):
    b = _Builder()
    b.feed(text)
    b.close()
    return b.root
