"""A short self-check of the visibility pass (tools/bib/vis.py, tools/bib/vis_words.py): the rules on made-up entries
and the words on roles FRUS writes. The repository has no test suite; run it after a change to either module.

    python3 -I tools/vis/selfcheck.py          prints each check and "ok", or what failed; exit 1 on a failure

It reads sources/provenance.yaml and sources/polities.yaml as they stand (the series' own FRUS volume years and the
registry's series), but no list: the entries here are made up, with links only, so no card or witness is needed.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from tools.bib import vis, vis_words  # noqa: E402

FAIL = []


def eq(what, got, want):
    ok = got == want
    print(f"{'ok  ' if ok else 'FAIL'} {what}: {got!r}" + ("" if ok else f" (want {want!r})"))
    if not ok:
        FAIL.append(what)


def tags(e):
    return [c["tags"] for c in vis.compute(None, None, e)]


# the words (vis_words.py, STYLE 1): an American post abroad is American; a nationality or a country after an office
for role, want in [("Ambassador to the Soviet Union", "us"), ("Soviet Ambassador to the United States", "ussr"),
                   ("Prime Minister of India", "india"), ("Director, Office of Soviet Union Affairs, Department of State", "us"),
                   ("Counselor of the Soviet Embassy in the United States", "ussr"),
                   ("Commercial Representative in Paris of the Democratic Republic of Vietnam", "drv"),
                   ("President of the Republic of Vietnam", "rvn"), ("Secretary-General of the United Nations", "un"),
                   ("Vice Premier of the State Council of the People’s Republic of China", "prc"),
                   ("USA, Chief of Staff, Military Assistance Command, Vietnam", "us")]:
    eq(f"role {role!r}", vis_words.role_polity(role, None), want)
eq("strict: an American in an American section", vis_words.role_polity("NSC staff, Vietnam", "us", strict=True), "us")
eq("strict: King of the Belgians", vis_words.role_polity("King of the Belgians, 1951–93", "us", strict=True), "belgium")

# dates (vis.py, STYLE 3)
eq("iso of a month", vis.iso("1961-02"), "1961-02-01")
eq("item date from the cite", vis.item_date("Remarks, [1967 Pub. Papers 778](https://x) (Aug. 16, 1967)", "1967-08-16",
                                            "event"), "1967-08-16")
eq("item date: a later year printed", vis.item_date("DOE/NV-209, rev. 16 (2015), 16–17", "1961-09-01", "event"),
   "2015-01-01")
eq("item date: none, a record of the time", vis.item_date("106 Cong. Rec. 13,819", "1960-06-21", "event"), "1960-06-21")
eq("status before, between, after", [vis.status(["1962-10-22", "1996-01-01"], r) for r in ("1962-10-21", "1970-01-01",
                                                                                          "2000-01-01")],
   [None, "nonpublic", "public"])
eq("tags before the claim's date", vis.tags_at({"us": {"P": ["1962-10-22", None]}}, "1962-10-01", "1962-10-22"), [])

# the rules on made-up entries (STYLE 4-6)
times = {"id": "cal.test.times", "date": "1961-01-10", "thread": "economy", "tags": [],
         "c": "A story in the *Times*.",
         "n": "[*New York Times*, Jan. 10, 1961](https://timesmachine.nytimes.com/timesmachine/1961/01/10/issue.html)."}
eq("the press: public that morning, P for its country", tags(times), [["US:public-PA"]])
frus = {"id": "cal.test.frus", "date": "1964-08-04", "thread": "vietnam-tonkin", "tags": ["name:mcnamara-robert-s"],
        "c": "McNamara to the President on the second attack.",
        "n": "[FRUS 1964–68, I, doc. 278](https://history.state.gov/historicaldocuments/frus1964-68v01/d278)."}
cl = vis.compute(None, None, frus)[0]
eq("a FRUS memorandum: nonpublic at the time", cl["tags"], ["US:nonpublic-PA"])
eq("... public from the volume's year (the notes: FRUS 1964–68, I (1992))", cl["polities"]["us"]["P"],
   ["1964-08-04", "1992-01-01"])
eq("... at a pin of 1995", vis.tags_at(cl["polities"], "1995-01-01", cl["date"]), ["US:public-PA"])
moscow = dict(times, id="cal.test.moscow", tags=["name:khrushchev-nikita-s"], c="Khrushchev in Moscow, to the Times.")
eq("the Times on Moscow: USSR public-A that morning, nonpublic-P (his own act)", tags(moscow),
   [["US:public-P", "USSR:nonpublic-P", "USSR:public-A"]])
un = {"id": "cal.test.un", "date": "1962-10-25", "thread": "missile-crisis", "tags": [],
      "c": "The Council meets.", "n": "[S/PV.1025](https://undocs.org/S/PV.1025)."}
eq("an organization's record: its state parties' P and A (the thread's)", tags(un),
   [["US:public-PA", "USSR:public-PA", "CUBA:public-PA"]])
none = {"id": "cal.test.none", "date": "1965-03-01", "thread": "economy", "tags": [], "c": "Something.",
        "n": "[Wikipedia](https://en.wikipedia.org/wiki/X)."}
eq("nothing computable: the placeholder", tags(none), [["US:all"]])
loose = dict(times, id="cal.test.loose", date="1961-01", n=times["n"])
eq("a month's entry: judged at the end of its window, the Times of the 10th out (the owner, Nov. 11)", tags(loose),
   [["US:public-PA"]])
bolsh = {"id": "cal.test.bolsh", "date": "1962-10-04", "thread": "soviet-union",
         "tags": ["name:bolshakov-georgi", "name:kennedy-robert-f"], "c": "Bolshakov with Robert Kennedy.",
         "n": "[FRUS 1961–63, VI, doc. 1](https://history.state.gov/historicaldocuments/frus1961-63v06/d1)."}
eq("a private talk: both parties addressed and privy (the owner, Nov. 11)", tags(bolsh),
   [["US:nonpublic-PA", "USSR:nonpublic-PA"]])

front = {"id": "cal.test.front", "date": "1963-01-24", "thread": "vietnam", "tags": [],
         "c": "COSVN meets in the South on the year's tasks.",
         "n": "[FRUS 1961–63, III, doc. 1](https://history.state.gov/historicaldocuments/frus1961-63v03/d1)."}
eq("the Front's act: the DRV's, addressed to the South, not presumed known to Saigon (the owner, Nov. 11)",
   [t for t in tags(front)[0] if t.startswith(("DRV", "RVN"))], ["DRV:nonpublic-PA", "RVN:nonpublic-A"])

print(f"{len(FAIL)} failed" if FAIL else "all ok")
sys.exit(1 if FAIL else 0)
