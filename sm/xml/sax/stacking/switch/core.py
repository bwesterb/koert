import six
from cases import No as NoCase

from koert.xml.sax.stacking.core import SH


class SwitchSH(SH):

    def __init__(self, ot, cases, default=NoCase):
        SH.__init__(self, ot)
        self.cases = cases
        self.default = default
        self.child_results = dict()
        self.init_child_results()

    def init_child_results(self):
        for case in six.itervalues(self.cases):
            case.init(self.child_results)

    def get_case(self, name):
        if name in self.cases:
            return self.cases[name]
        print("warning:  unexpected node-name %s" % name)
        return self.default

    def startElement(self, sh, name, attrs):
        return self.get_case(name).handler

    def endElement(self, sh, name, spawned_handler):
        if spawned_handler.result is None:
            return
        case = self.get_case(name)
        case.apply_result(spawned_handler.result, self.child_results)

    def goodbye(self, sh):
        for case in six.itervalues(self.cases):
            case.final(self.child_results)
        self.post_result(sh, self.child_results)

    def reclaim(self):
        self.result = None
        self.child_results = dict()
        self.init_child_results()
        return True
