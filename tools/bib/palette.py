"""The winner's-share scale for templates/congress.html: six steps a hue (B Democratic, R Republican, A a third
ticket), interpolated in OKLab between the lightest and darkest steps of the election scale (--eB1 to --eB4,
--eR1 to --eR4, --eA1 to --eA4) so that lightness falls evenly. Light and dark each from their own endpoints.

    python3 -m tools.bib.palette            print the three CSS lines (light, dark media query, dark theme)
    python3 -m tools.bib.palette --check    exit 1 if the template's --w* values are not these (./bib check does too)

Change an endpoint in the template, run this, and paste its lines over the template's --w* lines.
"""
import os
import re
import sys

from . import store

TEMPLATE = os.path.join(store.ROOT, "templates", "congress.html")
HUES, STEPS = "BRA", 6


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gam(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def to_oklab(h):
    r, g, b = (_lin(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5))
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def to_hex(L, a, b):
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    return "#" + "".join("%02X" % round(max(0, min(1, _gam(x))) * 255) for x in rgb)


def endpoints(css):
    """{'light': {hue: (step 1, step 4)}, 'dark': {...}}: the --e* values on the template's :root lines."""
    heads = {"light": r"^:root\{(.*)\}$", "dark": r'^:root\[data-theme="dark"\]\{(.*)\}$'}
    out = {}
    for mode, head in heads.items():
        v = dict(re.findall(r"--(e[A-Z]\d):(#[0-9A-Fa-f]{6})", ";".join(re.findall(head, css, re.M))))
        out[mode] = {h: (v[f"e{h}1"], v[f"e{h}4"]) for h in HUES}
    return out


def scale(a, b):
    A, B = to_oklab(a), to_oklab(b)
    return [to_hex(*(A[i] + (B[i] - A[i]) * t / (STEPS - 1) for i in range(3))) for t in range(STEPS)]


def lines(css):
    E = endpoints(css)
    decl = {m: ";".join(f"--w{h}{i + 1}:{c}" for h in HUES for i, c in enumerate(scale(*E[m][h]))) for m in E}
    return [f":root{{{decl['light']}}}",
            f'@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{{decl["dark"]}}}}}',
            f':root[data-theme="dark"]{{{decl["dark"]}}}']


def current():
    """True when the template's --w* lines are the ones lines() makes (./bib check)."""
    css = open(TEMPLATE, encoding="utf-8").read()
    return all(w in css for w in lines(css))


def main():
    if "--check" in sys.argv:
        ok = current()
        print("the template's winner's-share scale is current" if ok else "out of date: run python3 -m tools.bib.palette")
        sys.exit(0 if ok else 1)
    print("\n".join(lines(open(TEMPLATE, encoding="utf-8").read())))


if __name__ == "__main__":
    main()
