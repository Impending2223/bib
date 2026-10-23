"""Recheck whether this machine can open each online source in sources/states.yaml.

    python3 tools/sources/check_access.py              report only: State, host, old access -> new access
    python3 tools/sources/check_access.py --write      also write the new access and today's date back
    python3 tools/sources/check_access.py --st CT NH   only these States

Access, as recorded in the register (sources/states.yaml, header):
    open      the page answers 200 with content
    borrow    an Internet Archive lending copy (set by hand; this script leaves it alone)
    bot-check the site answers with a bot challenge (HTTP 403 with cf-mitigated, "Just a moment...").
              Do not try to get around it; a person in a browser can open it.
    blocked   this environment's network policy refuses the host ("CONNECT tunnel failed, response 403").
              The owner can allow the host in the environment's network settings.
    dead      404/410, or the name does not resolve
    other     anything else (the HTTP status is kept in the report)

A check is one GET with a browser User-Agent, following redirects; it reads no more than the first few KB.
The proxy's own "HTTP/1.1 200 Connection Established" is not the page's status (before Oct. 23, 2026 it was read as
one, so a page whose TLS failed showed open); a page answering 200 with a challenge in its first KB (Anubis's "Making
sure you're not a bot!", Cloudflare's Turnstile, Imperva's _Incapsula_Resource, AWS WAF, "Just a moment...") is
bot-check; a firewall's "Request Rejected" page, a TLS failure (an expired certificate, an incomplete chain) and a
proxy 502 to CONNECT are other. Google Books entries are left alone, as borrow is: their preview (full, snippet, none)
is read by hand, and the page answers 200 whatever it shows.
--write edits each online entry's line in place (`access:` and `checked:`), so comments and order survive; the register
keeps every online entry on one line, as a flow mapping, for that reason.
"""
import argparse
import datetime
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "sources", "states.yaml")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


CHALLENGE = re.compile(r"(?i)making sure you(?:&#39;|')re not a bot|/turnstile/|_Incapsula_Resource|awswaf|"
                       r"<title>just a moment|cf-chl-|challenge-platform")


def probe(url):
    """(access, detail) for one URL."""
    import tempfile
    with tempfile.NamedTemporaryFile() as body:
        try:
            r = subprocess.run(["curl", "-sS", "-L", "-A", UA, "--max-time", "30", "-r", "0-4095", "-D", "-",
                                "-o", body.name, "-w", "\nEFFECTIVE %{url_effective}\n", url],
                               capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            return "other", "timeout"
        text = open(body.name, encoding="utf-8", errors="replace").read(4096)
    err, head = r.stderr, r.stdout
    if "CONNECT tunnel failed, response 403" in err:
        return "blocked", err.strip()[-60:]
    if "CONNECT tunnel failed" in err:
        return "other", "proxy " + err.strip()[-20:]
    if "Could not resolve host" in err:
        return "dead", "no such host"
    if "SSL certificate problem" in err or "SSL" in err and r.returncode:
        return "other", "TLS: " + err.strip().split("\n")[0][-50:]
    codes = re.findall(r"^HTTP/\S+ (\d{3})(?! Connection established)", head, re.M | re.I)
    code = codes[-1] if codes else ""
    if r.returncode and not code:
        return "other", err.strip()[-60:] or "curl %d" % r.returncode
    eff = (re.findall(r"^EFFECTIVE (\S+)", head, re.M) or [""])[-1]
    if code in ("200", "206"):
        if CHALLENGE.search(text) or CHALLENGE.search(eff):
            return "bot-check", code + " challenge"
        if re.search(r"(?i)<title>\s*request rejected", text) or "Request Rejected" in text[:400]:
            return "other", code + " rejected"
        return "open", code
    if code in ("403", "405", "202") and (re.search(r"(?i)cf-mitigated|cf-ray|x-amzn-waf|x-iinfo", head)
                                          or CHALLENGE.search(text)):
        return "bot-check", code
    if code in ("404", "410"):
        return "dead", code
    return "other", code or err.strip()[-60:]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--st", nargs="*")
    a = ap.parse_args()
    reg = yaml.safe_load(open(REG, encoding="utf-8"))
    today = datetime.date.today().isoformat()
    changes = {}
    for s in reg:
        if a.st and s["st"] not in a.st:
            continue
        for src in s.get("sources", []):
            for o in src.get("online", []) or []:
                if o.get("access") == "borrow" or not o.get("url") or str(o.get("host", "")).startswith("Google Books"):
                    continue
                new, detail = probe(o["url"])
                mark = "" if new == o.get("access") else "  <- was " + str(o.get("access"))
                print(f"{s['st']:3} {new:9} {detail:>6}  {o['url']}{mark}")
                changes[o["url"]] = new
    if a.write and changes:
        lines = open(REG, encoding="utf-8").read().split("\n")
        url = None
        for i, l in enumerate(lines):
            m = re.search(r"url: ['\"]?([^'\",}]+)", l)
            if m:
                url = m.group(1).strip()
            if url in changes:
                lines[i] = re.sub(r"(access: )[\w-]+", r"\g<1>" + changes[url], lines[i], count=1)
                lines[i] = re.sub(r"(checked: )['\"]?[\d-]+['\"]?", r"\g<1>'" + today + "'", lines[i], count=1)
        open(REG, "w", encoding="utf-8").write("\n".join(lines))
        print(f"wrote {len(changes)} access results to {os.path.relpath(REG, ROOT)}")


if __name__ == "__main__":
    main()
