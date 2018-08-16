import re

import attr


@attr.s
class StartsWith:
    pattern = attr.ib()

    def match(self, text: str) -> bool:
        return text.startswith(self.pattern)


@attr.s
class EndsWith:
    pattern = attr.ib()

    def match(self, text: str) -> bool:
        return text.endswith(self.pattern)


@attr.s
class Contains:
    pattern = attr.ib()

    def match(self, text: str) -> bool:
        return self.pattern in text


@attr.s
class RegExp:
    pattern = attr.ib(converter=re.compile)

    def match(self, text: str) -> bool:
        return bool(self.pattern.fullmatch(text))


@attr.s
class Equals:
    pattern = attr.ib()

    def match(self, text: str) -> bool:
        return self.pattern == text


mapping = dict(
    regexp=RegExp,
    startswith=StartsWith,
    endswith=EndsWith,
    contains=Contains,
    equals=Equals,
)


def match(**kwargs):
    name, pattern = next(iter(kwargs.items()))
    return mapping[name](pattern)
