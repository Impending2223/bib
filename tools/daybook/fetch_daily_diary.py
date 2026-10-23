#!/usr/bin/env python3
"""Fetch Johnson's Daily Diary from the LBJ Library, a PDF a day: for the owner to run on his own computer.

Why this exists. The Diary (the President's Daily Diary, Nov. 22, 1963-Jan. 20, 1969) is on discoverlbj.org, a day an
item (`https://www.discoverlbj.org/item/pdd-YYYYMMDD`). The site's robots.txt allows general readers (`User-agent: *`,
`Allow: /`; its content signals: search=yes, ai-train=no, use=reference) and bars the AI crawlers by name; its Cloudflare
protection refuses requests from cloud data centres, so the series' environment cannot read it. A person may, in a
browser or with a polite script from his own connection. This is that script. It is the owner's own access: it says
who it is (--contact, put in its User-Agent), fetches one page every few seconds, never retries a refusal, and stops at
the first challenge or block rather than trying to pass it. Run it, then put the PDFs in the Drive folder "1968 series:
sources for Claude" (one zip is fine). The series reads them against the calendar (notes/diary-discrepancies.md) and
cites the Library's own address, not the copy.

Usage (Python 3.8+, nothing to install):
    python3 fetch_daily_diary.py --contact you@example.org --probe            # one day: shows what the page offers
    python3 fetch_daily_diary.py --contact you@example.org --limit 100        # the 100 busiest days first
    python3 fetch_daily_diary.py --contact you@example.org --from 1965-01-01 --to 1965-12-31
    python3 fetch_daily_diary.py --contact you@example.org --all              # every day, Nov. 22, 1963-Jan. 20, 1969
Files go to ./lbj-diary/pdd-YYYYMMDD.pdf; a day already there is skipped, so a stopped run resumes where it stopped.
A log of each day (saved, no PDF found, refused) goes to ./lbj-diary/log.tsv.

The order. RANKED is the 804 days of the span that hold calendar entries recording an act of Johnson's (tagged
name:johnson-lyndon-b) and are not among the 50 the National Archives Catalog already gives, busiest first (the number
after each day: its entries), as of Oct. 23, 2026. --limit takes the first N of it; --from/--to and --all go by date.

How the PDF is found. The item page is read for a link to a PDF (an href ending .pdf, or a download link naming a PDF);
if the page itself answers with a PDF, that is saved. --probe prints every link it considers on one day, so that if the
site's layout differs the owner can send the output back and the rule can be fixed. Nothing else is taken from the page.
"""

RANKED = " ".join([
    "19650210:5 19661103:5 19680729:5 19640121:4 19650204:4 19650825:4 19680410:4 19680701:4",
    "19681022:4 19631217:3 19640902:3 19640903:3 19641016:3 19650217:3 19650402:3 19650518:3",
    "19650727:3 19650728:3 19650826:3 19650830:3 19650903:3 19660210:3 19660331:3 19660624:3",
    "19660628:3 19660720:3 19660809:3 19660921:3 19661015:3 19661108:3 19661111:3 19670302:3",
    "19670816:3 19670824:3 19671114:3 19671122:3 19671129:3 19680129:3 19680228:3 19680306:3",
    "19680312:3 19680930:3 19681011:3 19681016:3 19681018:3 19631207:2 19631213:2 19631216:2",
    "19631218:2 19631221:2 19640123:2 19640127:2 19640205:2 19640214:2 19640226:2 19640317:2",
    "19640403:2 19640409:2 19640410:2 19640414:2 19640422:2 19640424:2 19640513:2 19640524:2",
    "19640601:2 19640605:2 19640619:2 19640622:2 19640721:2 19640807:2 19640808:2 19640822:2",
    "19640918:2 19640924:2 19640925:2 19641015:2 19641026:2 19641102:2 19641209:2 19641216:2",
    "19641218:2 19650112:2 19650121:2 19650128:2 19650207:2 19650208:2 19650209:2 19650213:2",
    "19650302:2 19650309:2 19650318:2 19650323:2 19650428:2 19650512:2 19650517:2 19650603:2",
    "19650630:2 19650709:2 19650714:2 19650723:2 19650810:2 19650813:2 19650829:2 19650908:2",
    "19650924:2 19651003:2 19651020:2 19651022:2 19651103:2 19651217:2 19651220:2 19651229:2",
    "19660112:2 19660113:2 19660117:2 19660119:2 19660120:2 19660204:2 19660221:2 19660223:2",
    "19660302:2 19660309:2 19660315:2 19660322:2 19660328:2 19660330:2 19660601:2 19660615:2",
    "19660629:2 19660712:2 19660729:2 19660802:2 19660928:2 19661030:2 19661113:2 19661231:2",
    "19670104:2 19670110:2 19670124:2 19670127:2 19670202:2 19670206:2 19670208:2 19670213:2",
    "19670227:2 19670316:2 19670410:2 19670428:2 19670525:2 19670530:2 19670613:2 19670630:2",
    "19670714:2 19670727:2 19670729:2 19670803:2 19670809:2 19670815:2 19670818:2 19670828:2",
    "19670929:2 19671021:2 19671023:2 19671101:2 19671109:2 19671115:2 19671121:2 19671130:2",
    "19671205:2 19671215:2 19671218:2 19671219:2 19671220:2 19680102:2 19680103:2 19680107:2",
    "19680121:2 19680123:2 19680125:2 19680127:2 19680201:2 19680202:2 19680205:2 19680206:2",
    "19680214:2 19680221:2 19680227:2 19680304:2 19680314:2 19680316:2 19680318:2 19680322:2",
    "19680327:2 19680402:2 19680403:2 19680408:2 19680411:2 19680422:2 19680426:2 19680430:2",
    "19680505:2 19680525:2 19680528:2 19680605:2 19680606:2 19680610:2 19680619:2 19680620:2",
    "19680624:2 19680626:2 19680627:2 19680711:2 19680716:2 19680730:2 19680731:2 19680801:2",
    "19680816:2 19680818:2 19680819:2 19680820:2 19680823:2 19680830:2 19680911:2 19681002:2",
    "19681008:2 19681010:2 19681014:2 19681023:2 19681029:2 19681103:2 19681108:2 19681126:2",
    "19681220:2 19690117:2 19690120:2 19631204:1 19631220:1 19631224:1 19631226:1 19631227:1",
    "19631228:1 19640101:1 19640106:1 19640107:1 19640108:1 19640110:1 19640113:1 19640114:1",
    "19640115:1 19640116:1 19640117:1 19640120:1 19640124:1 19640125:1 19640129:1 19640130:1",
    "19640201:1 19640207:1 19640210:1 19640211:1 19640212:1 19640220:1 19640221:1 19640223:1",
    "19640225:1 19640229:1 19640302:1 19640304:1 19640308:1 19640309:1 19640310:1 19640312:1",
    "19640316:1 19640319:1 19640320:1 19640323:1 19640324:1 19640327:1 19640331:1 19640401:1",
    "19640411:1 19640412:1 19640418:1 19640420:1 19640421:1 19640428:1 19640429:1 19640504:1",
    "19640507:1 19640508:1 19640512:1 19640515:1 19640516:1 19640518:1 19640526:1 19640527:1",
    "19640608:1 19640610:1 19640611:1 19640612:1 19640618:1 19640621:1 19640626:1 19640629:1",
    "19640701:1 19640707:1 19640709:1 19640711:1 19640713:1 19640724:1 19640727:1 19640730:1",
    "19640731:1 19640805:1 19640809:1 19640810:1 19640811:1 19640813:1 19640814:1 19640815:1",
    "19640820:1 19640823:1 19640824:1 19640826:1 19640827:1 19640830:1 19640831:1 19640904:1",
    "19640907:1 19640908:1 19640910:1 19640922:1 19640926:1 19641003:1 19641006:1 19641007:1",
    "19641008:1 19641014:1 19641018:1 19641019:1 19641021:1 19641028:1 19641030:1 19641116:1",
    "19641118:1 19641201:1 19641203:1 19641206:1 19641207:1 19641212:1 19641215:1 19641219:1",
    "19641224:1 19650104:1 19650106:1 19650107:1 19650113:1 19650116:1 19650124:1 19650125:1",
    "19650126:1 19650127:1 19650131:1 19650202:1 19650205:1 19650211:1 19650218:1 19650221:1",
    "19650225:1 19650226:1 19650303:1 19650304:1 19650308:1 19650317:1 19650320:1 19650324:1",
    "19650325:1 19650326:1 19650330:1 19650406:1 19650407:1 19650409:1 19650412:1 19650420:1",
    "19650429:1 19650430:1 19650502:1 19650504:1 19650507:1 19650508:1 19650513:1 19650524:1",
    "19650525:1 19650601:1 19650602:1 19650604:1 19650609:1 19650615:1 19650619:1 19650621:1",
    "19650624:1 19650625:1 19650701:1 19650708:1 19650713:1 19650718:1 19650720:1 19650721:1",
    "19650722:1 19650725:1 19650802:1 19650805:1 19650814:1 19650815:1 19650820:1 19650821:1",
    "19650824:1 19650827:1 19650831:1 19650906:1 19650909:1 19650912:1 19650920:1 19650922:1",
    "19650929:1 19650930:1 19651001:1 19651002:1 19651006:1 19651008:1 19651018:1 19651021:1",
    "19651023:1 19651027:1 19651031:1 19651106:1 19651108:1 19651109:1 19651111:1 19651116:1",
    "19651118:1 19651124:1 19651130:1 19651205:1 19651207:1 19651210:1 19651214:1 19651215:1",
    "19651218:1 19651227:1 19651228:1 19651230:1 19651231:1 19660109:1 19660110:1 19660124:1",
    "19660126:1 19660127:1 19660131:1 19660201:1 19660203:1 19660205:1 19660206:1 19660222:1",
    "19660226:1 19660228:1 19660303:1 19660307:1 19660311:1 19660312:1 19660316:1 19660320:1",
    "19660321:1 19660323:1 19660325:1 19660402:1 19660404:1 19660408:1 19660413:1 19660416:1",
    "19660419:1 19660420:1 19660422:1 19660424:1 19660428:1 19660507:1 19660511:1 19660513:1",
    "19660517:1 19660520:1 19660521:1 19660525:1 19660526:1 19660602:1 19660606:1 19660608:1",
    "19660609:1 19660613:1 19660614:1 19660618:1 19660621:1 19660622:1 19660630:1 19660701:1",
    "19660702:1 19660704:1 19660705:1 19660708:1 19660713:1 19660714:1 19660717:1 19660719:1",
    "19660724:1 19660728:1 19660801:1 19660804:1 19660812:1 19660813:1 19660815:1 19660819:1",
    "19660821:1 19660824:1 19660825:1 19660828:1 19660908:1 19660909:1 19660911:1 19660919:1",
    "19660922:1 19660923:1 19660926:1 19660930:1 19661005:1 19661007:1 19661010:1 19661011:1",
    "19661014:1 19661017:1 19661019:1 19661020:1 19661022:1 19661024:1 19661028:1 19661101:1",
    "19661104:1 19661105:1 19661106:1 19661110:1 19661114:1 19661115:1 19661116:1 19661119:1",
    "19661120:1 19661123:1 19661129:1 19661203:1 19661204:1 19661206:1 19661208:1 19661213:1",
    "19661221:1 19661222:1 19661223:1 19661224:1 19670105:1 19670112:1 19670116:1 19670120:1",
    "19670121:1 19670123:1 19670126:1 19670128:1 19670129:1 19670130:1 19670209:1 19670212:1",
    "19670214:1 19670215:1 19670216:1 19670218:1 19670222:1 19670223:1 19670228:1 19670301:1",
    "19670304:1 19670306:1 19670309:1 19670312:1 19670313:1 19670314:1 19670315:1 19670318:1",
    "19670320:1 19670321:1 19670322:1 19670324:1 19670326:1 19670328:1 19670329:1 19670401:1",
    "19670408:1 19670409:1 19670420:1 19670422:1 19670423:1 19670427:1 19670429:1 19670504:1",
    "19670507:1 19670509:1 19670510:1 19670515:1 19670519:1 19670523:1 19670527:1 19670531:1",
    "19670602:1 19670603:1 19670605:1 19670606:1 19670607:1 19670608:1 19670609:1 19670611:1",
    "19670612:1 19670619:1 19670627:1 19670701:1 19670702:1 19670705:1 19670706:1 19670707:1",
    "19670713:1 19670716:1 19670717:1 19670718:1 19670720:1 19670724:1 19670725:1 19670730:1",
    "19670731:1 19670802:1 19670805:1 19670811:1 19670814:1 19670817:1 19670820:1 19670822:1",
    "19670823:1 19670831:1 19670901:1 19670903:1 19670906:1 19670910:1 19670911:1 19670915:1",
    "19670917:1 19670926:1 19670927:1 19670928:1 19671001:1 19671002:1 19671004:1 19671005:1",
    "19671009:1 19671010:1 19671013:1 19671018:1 19671022:1 19671025:1 19671026:1 19671103:1",
    "19671107:1 19671108:1 19671117:1 19671118:1 19671119:1 19671120:1 19671127:1 19671202:1",
    "19671203:1 19671206:1 19671214:1 19671216:1 19671227:1 19680101:1 19680110:1 19680114:1",
    "19680116:1 19680117:1 19680118:1 19680119:1 19680124:1 19680126:1 19680130:1 19680131:1",
    "19680204:1 19680207:1 19680208:1 19680210:1 19680211:1 19680212:1 19680215:1 19680216:1",
    "19680219:1 19680220:1 19680222:1 19680223:1 19680225:1 19680301:1 19680308:1 19680311:1",
    "19680317:1 19680324:1 19680325:1 19680329:1 19680330:1 19680401:1 19680409:1 19680415:1",
    "19680417:1 19680424:1 19680425:1 19680428:1 19680503:1 19680507:1 19680509:1 19680514:1",
    "19680516:1 19680520:1 19680529:1 19680602:1 19680608:1 19680611:1 19680612:1 19680613:1",
    "19680617:1 19680621:1 19680622:1 19680628:1 19680702:1 19680703:1 19680705:1 19680706:1",
    "19680709:1 19680710:1 19680715:1 19680717:1 19680718:1 19680719:1 19680721:1 19680723:1",
    "19680724:1 19680725:1 19680726:1 19680805:1 19680807:1 19680808:1 19680810:1 19680812:1",
    "19680815:1 19680822:1 19680826:1 19680828:1 19680829:1 19680906:1 19680909:1 19680910:1",
    "19680912:1 19680916:1 19680917:1 19680923:1 19680926:1 19681001:1 19681003:1 19681007:1",
    "19681012:1 19681025:1 19681030:1 19681031:1 19681102:1 19681104:1 19681105:1 19681111:1",
    "19681112:1 19681113:1 19681115:1 19681118:1 19681124:1 19681125:1 19681130:1 19681211:1",
    "19681213:1 19681219:1 19681221:1 19681222:1 19681227:1 19681229:1 19681231:1 19690107:1",
    "19690109:1 19690114:1 19690115:1 19690116:1",
]).split()

import argparse, datetime, html, os, re, sys, time, urllib.error, urllib.parse, urllib.request

SITE = "https://www.discoverlbj.org"
START, END = datetime.date(1963, 11, 22), datetime.date(1969, 1, 20)
CHALLENGE = re.compile(r"cf-chl|challenge-platform|Just a moment\.\.\.|Attention Required|you have been blocked", re.I)


def ua(contact):
    return f"1968-series-research/1.0 (fetching the President's Daily Diary for a bibliography; contact: {contact})"


def get(url, contact, accept="*/*"):
    req = urllib.request.Request(url, headers={"User-Agent": ua(contact), "Accept": accept})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read(), r.geturl()


def pdf_links(page, base):
    out = []
    for m in re.finditer(r"""href\s*=\s*["']([^"']+)["']""", page, re.I):
        href = html.unescape(m.group(1))
        low = href.lower()
        if ".pdf" in low or ("download" in low and "pdd" in low) or "/files/original/" in low:
            out.append(urllib.parse.urljoin(base, href))
    seen = set()
    return [u for u in out if not (u in seen or seen.add(u))]


def days(args):
    if args.all or args.date_from or args.date_to:
        a = datetime.date.fromisoformat(args.date_from) if args.date_from else START
        b = datetime.date.fromisoformat(args.date_to) if args.date_to else END
        d = max(a, START)
        while d <= min(b, END):
            yield d.strftime("%Y%m%d")
            d += datetime.timedelta(days=1)
    else:
        for i, tok in enumerate(RANKED):
            if args.limit and i >= args.limit:
                break
            yield tok.split(":")[0]


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--contact", required=True, help="your e-mail or web address, sent in the User-Agent")
    p.add_argument("--out", default="lbj-diary")
    p.add_argument("--limit", type=int, default=0, help="the first N days of the ranked list (default: all 804)")
    p.add_argument("--from", dest="date_from")
    p.add_argument("--to", dest="date_to")
    p.add_argument("--all", action="store_true", help="every day of the span, not the ranked list")
    p.add_argument("--delay", type=float, default=4.0, help="seconds between requests (at least 2)")
    p.add_argument("--probe", action="store_true", help="read one day and print the links considered; save nothing")
    args = p.parse_args()
    delay = max(args.delay, 2.0)
    os.makedirs(args.out, exist_ok=True)
    log = open(os.path.join(args.out, "log.tsv"), "a", encoding="utf-8")
    todo = ["19640121"] if args.probe else list(days(args))
    print(f"{len(todo)} days to consider; {delay:.0f} s between requests.")
    for n, ymd in enumerate(todo, 1):
        dest = os.path.join(args.out, f"pdd-{ymd}.pdf")
        if os.path.exists(dest) and not args.probe:
            continue
        item = f"{SITE}/item/pdd-{ymd}"
        try:
            status, ctype, body, final = get(item, args.contact, "text/html,application/pdf")
        except urllib.error.HTTPError as e:
            text = e.read(4000).decode("utf-8", "replace")
            why = "a challenge or block page" if CHALLENGE.search(text) else f"HTTP {e.code}"
            print(f"{ymd}: refused ({why}). Stopping: don't retry; try later, or fetch the day in a browser.")
            log.write(f"{ymd}\trefused\t{e.code}\n"); break
        except urllib.error.URLError as e:
            print(f"{ymd}: network error ({e.reason}). Stopping."); log.write(f"{ymd}\terror\t{e.reason}\n"); break
        if "pdf" in ctype.lower():
            if not args.probe:
                open(dest, "wb").write(body)
            print(f"{ymd}: the page is the PDF ({len(body):,} bytes)"); log.write(f"{ymd}\tsaved\t{final}\n")
            time.sleep(delay); continue
        page = body.decode("utf-8", "replace")
        if CHALLENGE.search(page):
            print(f"{ymd}: a challenge page. Stopping: open {item} in a browser instead."); log.write(f"{ymd}\tchallenge\t\n"); break
        links = pdf_links(page, final)
        if args.probe:
            print(f"{item} -> {final} ({ctype}, {len(body):,} bytes)")
            print("PDF candidates:", *(links or ["none"]), sep="\n  ")
            allh = re.findall(r"""href\s*=\s*["']([^"']+)["']""", page, re.I)
            print(f"all links on the page ({len(allh)}):", *allh[:80], sep="\n  ")
            return
        if not links:
            print(f"{ymd}: no PDF link on the page"); log.write(f"{ymd}\tno-pdf\t{final}\n"); time.sleep(delay); continue
        time.sleep(delay)
        try:
            status, ctype, pdf, final2 = get(links[0], args.contact, "application/pdf")
        except urllib.error.HTTPError as e:
            print(f"{ymd}: the PDF refused (HTTP {e.code}). Stopping."); log.write(f"{ymd}\trefused-pdf\t{e.code}\n"); break
        if not pdf.startswith(b"%PDF"):
            print(f"{ymd}: {links[0]} did not answer with a PDF ({ctype}). Stopping; run --probe and send the output back.")
            log.write(f"{ymd}\tnot-pdf\t{links[0]}\n"); break
        open(dest, "wb").write(pdf)
        print(f"[{n}/{len(todo)}] {ymd}: {len(pdf):,} bytes"); log.write(f"{ymd}\tsaved\t{final2}\n"); log.flush()
        time.sleep(delay)
    print(f"Done. The PDFs are in {os.path.abspath(args.out)}.")


if __name__ == "__main__":
    main()
