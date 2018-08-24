# built-in
from collections import Callable
from contextlib import suppress
from functools import update_wrapper

# project
from .aspect import Aspect, AspectMeta
from .joinpoint import JoinPoint
from .helpers import ObjectInfo


def patch_class(aspect):
    # make new object name
    name = aspect.__name__
    if not name.endswith('Aspect'):
        name += 'Aspect'
    # patch
    # TypeError: type '_bz2.BZ2Compressor' is not an acceptable base type
    with suppress(TypeError):
        aspect = AspectMeta(name, (Aspect, aspect), {})
    return aspect


def patch_function(aspect):
    module = getattr(aspect, '__module__', '')
    if not module:
        module = aspect.__module__ = getattr(aspect.__globals__['__spec__'], 'name', '')

    info = ObjectInfo(aspect)
    joinpoint = JoinPoint(
        aspect=info.name,
        method='__call__',
        module=info.module_name,
        path=info.module_path,
    )
    joinpoint._method = aspect
    return update_wrapper(joinpoint, aspect)


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
