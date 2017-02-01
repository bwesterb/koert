import argparse

from six.moves import range

from koert.drank.boozedir import BoozeDir
from koert.drank.reporting import EventReport

TESTS = None


def parse_args():
    parser = argparse.ArgumentParser(description="Test booze directory")
    parser.add_argument("booze_dir")
    parser.add_argument("test", choices=TESTS.keys())
    return parser.parse_args()


def get_bd(args):
    return BoozeDir(args.booze_dir)


def main():
    args = parse_args()
    bd = get_bd(args)
    TESTS[args.test](args, bd)


# The tests

def check_pricelists(args, bd):
    pls = bd.pricelistdir.pricelists.values()
    cms = bd.commoditydir.commodities.values()
    print("")
    print(' -  --   ---     Checking Pricelists     ---   --  - ')
    print("")
    print("   found pricelists: %s" % ", ".join(str(x) for x in pls))
    print("")
    print("")

    missing = {}
    for c in cms:
        if c.proper:
            continue
        pl = c.pricelist
        if pl not in missing:
            missing[pl] = []
        missing[pl].append(c.product)
    if missing:
        print("__________________________________________")
        print("The following pricelist miss some products:")
        print("")
        for pl in missing:
            missing[pl].sort(key=lambda x: x.handle)
            print("%s" % (pl,))
            print("")
            print(", ".join(str(x) for x in missing[pl]))
            print("")
        print("")
        print("")


def check_events(args, bd):
    print("")
    print(' -  --   ---     Checking Events     ---   --  - ')
    print("")
    print("")
    dates = bd.eventdir.events.keys()
    dates.sort(key=lambda x: (x is None, x))
    for date in dates:
        event = bd.eventdir.events[date]
        tags = set()
        if event.beertank_activity:
            tags.add("beertank")
        if event.btc is not None:
            tags.add("btc")
        if len(event.delivs) > 0:
            tags.add("deliv")
        if len(event.shifts) > 0:
            tags.add("barform")
        if event.invcount:
            tags.add("invcount")
        print("event on %s (%s):" % (event.date,
                                     ', '.join(tags)))
        for line in EventReport(event, bd).generate():
            print("\t* " + line)


def check_barforms(args, bd):
    print("")
    print(' -  --   ---     Checking Barforms     ---   --  - ')
    print("")
    print("")
    barforms = bd.barformdir.barforms
    codes = barforms.keys()
    check_barforms_numbering(args, bd, barforms, codes)


def check_barforms_numbering(args, bd, barforms, codes):
    intcodes = [int(x) for x in barforms.keys()]
    m = min(intcodes)
    M = max(intcodes)
    print("Codes range from %s to %s." % (m, M))
    if len(intcodes) == M + 1 - m:
        print("No barforms seem to be missing.")
        return
    print("Some barforms are missing:")
    print("\tOne expects %s barforms in total" % (M + 1 - m,))
    print("\tbut there are only %s barforms." % (len(intcodes),))
    print()
    print("Indeed, the following codes are not present: ")
    ics = set(intcodes)
    for i in range(m, M + 1):
        if i not in ics:
            print("\t%s" % (str(i),))


TESTS = {
    "pricelists": check_pricelists,
    "events": check_events,
    "barforms": check_barforms,
    "no": lambda *args, **kwargs: 42
}


# finally:
if __name__ == "__main__":
    main()
