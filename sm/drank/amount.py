# ad-hoc solution for parsing amounts in Counts
from decimal import Decimal

from common import MildErr


# parse the string representation  s  of an amount of the object  obj.


def parse_amount(s=None, obj=None):
    if s is None:
        return Decimal(0)
    term_strs = s.split("+")
    return sum(parse_amount_term(ts, obj) for ts in  term_strs)


def parse_amount_term(t, obj):
    t = t.strip()
    if ":" not in t:
        return Decimal(t)
    command, args_str = t.split(":", 2)
    res = getattr(obj, "parse_command", None)
    if res is None:
        raise MildErr("object '%r' does not support 'parse_command'"
                      % (obj,))
    return res(command, args_str)
