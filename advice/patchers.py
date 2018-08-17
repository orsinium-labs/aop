from collections import Callable

from .aspect import Aspect
from .joinpoint import JoinPoint


def patch_class(aspect):
    # make new object name
    name = aspect.__name__
    if not name.endswith('Aspect'):
        name += 'Aspect'
    # patch
    return type(name, (Aspect, aspect), {})


def patch_function(aspect):
    joinpoint = JoinPoint(
        aspect=aspect.__name__,
        method='__call__',
        module=aspect.__module__,
    )
    joinpoint._method = aspect
    return joinpoint


def patch_object(aspect):
    # don't patch object twice
    if isinstance(aspect, (Aspect, JoinPoint)):
        return aspect
    # class
    if isinstance(aspect, type):
        return patch_class(aspect)
    # function
    if isinstance(aspect, Callable):
        return patch_function(aspect)
    return aspect
