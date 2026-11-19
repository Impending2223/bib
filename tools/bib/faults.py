"""Faults the build survives: a person's entry or a month of committee meetings that raised an error and was left out
so the other pages could still be written. Each is counted and printed (stderr) where it happens; `./bib build` writes
the other pages, names them all at its end and exits 1 when any occurred (cli.cmd_build), so CI does not deploy a site
with content silently missing; `./bib check` exits 1 too. The visibility pass is not counted: its output is warnings
only and drops no content (the spec §9.1).

    record(where, message)    a fault: printed now, kept for the report
    FAULTS                    [(where, message)] this run
    report()                  the lines for the end of the build
"""
import sys

FAULTS = []


def record(where, message, line=None):
    """A fault the run survives. `line`, if given, is what is printed (a caller's own form); else 'where: message'."""
    FAULTS.append((where, message))
    print(line if line is not None else f"{where}: {message}", file=sys.stderr)


def reset():
    FAULTS.clear()


def report():
    out = [f"{len(FAULTS)} build {'fault' if len(FAULTS) == 1 else 'faults'}: content left out of the pages"]
    out += [f"  {w}: {m}" for w, m in FAULTS]
    return "\n".join(out)
