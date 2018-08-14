import re

import attr


rex_all = re.compile('.*')


@attr.s
class Advice:
    handler = attr.ib()
    paths = attr.ib(default=rex_all)
    modules = attr.ib(default=rex_all)
    targets = attr.ib(default=rex_all)
    methods = attr.ib(default=re.compile('__call__'))


class Advices:
    def __init__(self):
        self.catalog = []

    def register(self, advice):
        self.catalog.append(advice)

    def __iter__(self):
        return iter(self.catalog)


advices = Advices()
