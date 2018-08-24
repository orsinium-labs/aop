from collections import OrderedDict
from pprint import pprint

from .joinpoint import JoinPoint
from .module import AspectModule
from .aspect import Aspect


class Inspector:
    def __init__(self, obj):
        self.obj = obj

    @property
    def is_patched(self) -> bool:
        return isinstance(self.obj, (JoinPoint, AspectModule, Aspect))

    @property
    def is_function(self) -> bool:
        return isinstance(self.obj, JoinPoint)

    @property
    def is_class(self) -> bool:
        return isinstance(self.obj, Aspect)

    @property
    def is_module(self) -> bool:
        return isinstance(self.obj, AspectModule)

    @property
    def advices(self) -> list:
        if not isinstance(self.obj, JoinPoint):
            return
        return [advice.handler for advice in self.obj._get_advices()]


def inspect(obj, *, print=False):
    inspector = Inspector(obj)
    result = OrderedDict((
        ('is_patched', inspector.is_patched),
        ('is_function', inspector.is_function),
        ('is_class', inspector.is_class),
        ('advices', inspector.advices),
    ))
    if print:
        pprint(result)
    else:
        return result
