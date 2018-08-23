# external
import attr

from .matcher import match


match_all = match(regexp='.*')


@attr.s
class Advice:
    """Advice is a rule for joinpoint processing.
    """
    handler = attr.ib()
    paths = attr.ib(default=match_all)
    modules = attr.ib(default=match_all)
    targets = attr.ib(default=match_all)
    methods = attr.ib(default=match(equals='__call__'))


class Advices:
    """Catalog of advices.
    """
    hashsum = 0

    def __init__(self):
        self.catalog = []

    def register(self, advice):
        self.catalog.append(advice)
        self.hashsum += 1

    def __iter__(self):
        return iter(self.catalog)

    def __contains__(self, advice):
        return advice in self.catalog


advices = Advices()
