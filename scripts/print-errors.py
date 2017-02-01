import sys

from koert.gnucash.tools import open_gcf
from koert.verification.core import (AcMutThenNoSplit, SpNonZero,
                                     TrHaveFin7Softref, TrMutAc,
                                     TrNumsAreContinuous, TrNumsAreWellFormed,
                                     TrsHaveNum, Verifier)
from koert.verification.fin7scheme import scheme


def main(argv):
    path = " ".join(argv[1:]).strip()
    if not path:
        print("please provide a path to a gnucash file as argument.")
        return
    gcf = open_gcf(path, scheme)
    v = Verifier(gcf)
    res = v.verify(TrsHaveNum, TrNumsAreWellFormed,
                   TrNumsAreContinuous,
                   AcMutThenNoSplit, TrMutAc, SpNonZero,
                   TrHaveFin7Softref)
    for fact in res:
        print(fact)
        print(res[fact])
        print("")


if __name__ == "__main__":
    main(sys.argv)
