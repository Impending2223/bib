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


def probe(url):
    """(access, detail) for one URL."""
    try:
        r = subprocess.run(["curl", "-sS", "-L", "-A", UA, "--max-time", "30", "-r", "0-4095", "-D", "-", "-o", "/dev/null", url],
                           capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return "other", "timeout"
    err, head = r.stderr, r.stdout
    if "CONNECT tunnel failed" in err:
        return "blocked", err.strip()[-60:]
    if "Could not resolve host" in err:
        return "dead", "no such host"
    codes = re.findall(r"^HTTP/\S+ (\d{3})", head, re.M)
    code = codes[-1] if codes else ""
    if code in ("200", "206"):
        return "open", code
    if code == "403" and re.search(r"(?i)cf-mitigated|cf-ray", head):
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
                if o.get("access") == "borrow" or not o.get("url"):
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
                lines[i] = re.sub(r"(access: )[\w-]+", r"\g<1>" + changes[url], lines[i])
                lines[i] = re.sub(r"(checked: )['\"]?[\d-]+['\"]?", r"\g<1>'" + today + "'", lines[i])
        open(REG, "w", encoding="utf-8").write("\n".join(lines))
        print(f"wrote {len(changes)} access results to {os.path.relpath(REG, ROOT)}")


if __name__ == "__main__":
    main()
