# built-in
from collections import Callable

# project
from .joinpoint import JoinPoint
from .helpers import ObjectInfo


class AspectMeta(type):
    """Metaclass for isinstance() hack
    """

    def __new__(cls, name, bases, namespace, **kwargs):
        # if aspect not in mro yet
        if not {'Aspect', 'AspectObject'} & {base.__name__ for base in bases}:
            bases = (Aspect, ) + bases
        return super().__new__(cls, name, bases, namespace)

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
        info = ObjectInfo(self)
        joinpoint = JoinPoint(
            aspect=info.name,
            module=info.module_name,
            path=info.module_path,
            method=name,
        )
        joinpoint._method = method
        setattr(self, name, joinpoint)  # save joinpoint
        return joinpoint


class AspectObject(object, metaclass=AspectMeta):
    """Patched object with Aspect as first class in mro.
    """
    pass
