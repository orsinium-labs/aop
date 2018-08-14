import re

import attr


@attr.s
class StartsWith:
    pattern = attr.ib()

    def match(self, text):
        return text.startswith(self.pattern)


@attr.s
class EndsWith:
    pattern = attr.ib()

    def match(self, text):
        return text.endswith(self.pattern)


@attr.s
class Contains:
    pattern = attr.ib()

    def match(self, text):
        return self.pattern in text


mapping = dict(
    regexp=re.compile,
    startswith=StartsWith,
    endswith=EndsWith,
    contains=Contains,
)


def match(**kwargs):
    name, pattern = kwargs.pop()
    return mapping[name](pattern)
