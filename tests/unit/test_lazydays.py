"""lazydays.py: the days' blocks moved to a file a month, each under its own day (Nov. 19, 2026: a Sunday's div is
"day sun", and the day's div carries data-h, data-short, data-crumb; the pattern had matched neither)."""
import json
import os

from bib import lazydays


def day(iso, cls="day", blocks=""):
    return (f'<div class="{cls}" id="d{iso}" data-h="4" data-short="x" data-crumb="1"><div class="dh">{iso}</div>'
            f'{blocks}</div>')


def docs(text, cls="docs"):
    return f'<details class="{cls}"><summary>Documents: PPP 1</summary><p id="a-{text}">{text}</p></details>'


def page(*days):
    return "<html><head></head><body><main id=\"doc\">" + "".join(days) + "</main></body></html>"


def months(out):
    d = os.path.join(out, lazydays.SUB)
    got = {}
    for f in sorted(os.listdir(d)):
        got.update(json.load(open(os.path.join(d, f), encoding="utf-8")))
    return got


def test_each_day_its_own_blocks_sunday_included(tmp_path):
    p = page(day("1964-01-04", blocks=docs("sat")),
             day("1964-01-05", cls="day sun", blocks=docs("sun") + docs("sunor", cls="docs or")),
             day("1964-01-06", blocks=docs("mon")))
    out = lazydays.split(p, "cal1964Q1", str(tmp_path))
    got = months(str(tmp_path))
    assert set(got) == {"1964-01-04d", "1964-01-05d", "1964-01-05o", "1964-01-06d"}
    assert "sun" in got["1964-01-05d"] and "sat" not in got["1964-01-05d"]
    assert "sat" in got["1964-01-04d"] and "sun" not in got["1964-01-04d"]
    assert "sunor" in got["1964-01-05o"]
    assert out.count('data-lz="1964-01"') == 4
    assert 'id="a-sun"' not in out.split('id="lzmap"')[0]          # the block's contents left the page
    lz = json.loads(out.split('<script type="application/json" id="lzmap">')[1].split("</script>")[0])
    assert lz["ix"]["a-sun"] == "1964-01"


def test_undated_day_keeps_its_blocks_inline(tmp_path):
    """A day's div without a date's id (an intercalary day, a month's loose dates) does not take the day before's."""
    p = page(day("1964-01-31", blocks=docs("jan31")),
             '<div class="day ix" id="ix-1964-01-31-after" data-h="4"><div class="dh">End of January</div>'
             + docs("loose") + "</div>",
             day("1964-02-01", blocks=docs("feb1")))
    out = lazydays.split(p, "cal1964Q1", str(tmp_path))
    got = months(str(tmp_path))
    assert set(got) == {"1964-01-31d", "1964-02-01d"}
    assert all("loose" not in v for v in got.values())
    assert 'id="a-loose"' in out                                    # still on the page


def test_page_without_blocks_unchanged(tmp_path):
    p = page(day("1964-01-04"))
    assert lazydays.split(p, "cal1964Q1", str(tmp_path)) == p
