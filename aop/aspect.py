# built-in
from collections import Callable

# project
from .joinpoint import JoinPoint


class AspectMeta(type):
    """Metaclass for isinstance() hack
    """
    def __instancecheck__(cls, obj):
        if len(cls.mro()) < 3:
            return NotImplemented
        parent = cls.mro()[2]
        return isinstance(obj, parent) or NotImplemented


class Aspect:
    """Patcher for classes.

    Place it as first parent for new class for patching.
    """

    def __getattribute__(self, name):
        method = super().__getattribute__(name)

        # dispatch
        if name[:2] == '__':
            return method
        if not isinstance(method, Callable):
            return method
        if isinstance(method, JoinPoint):
            return method

        # prepare and return joinpoint
        joinpoint = JoinPoint(
            aspect=self.__class__.__name__,
            module=self.__module__,
            method=name,
        )
        joinpoint._method = method
        setattr(self, name, joinpoint)  # save joinpoint
        return joinpoint
