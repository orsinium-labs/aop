import sys
from collections import Callable

from .aspect import Aspect
from .joinpoint import JoinPoint


def patch_class(aspect, advice):
    # avoid repeated patching
    if hasattr(aspect, '_advice'):
        if aspect._advice is advice:
            return aspect

    # make new object name
    name = aspect.__name__
    if not name.endswith('Aspect'):
        name += 'Aspect'

    # patch
    return type(
        name,
        (Aspect, aspect),
        {'_advice': advice},
    )


def patch_function(aspect, advice):
    joinpoint = JoinPoint(
        aspect=aspect.__name__,
        method='__call__',
    )
    joinpoint._method = aspect
    joinpoint._advice = advice
    return joinpoint


def patch_object(aspect, advice):
    if isinstance(aspect, type):
        return patch_class(aspect, advice)
    if isinstance(aspect, Callable) and advice.methods.match('__call__'):
        return patch_function(aspect, advice)
    return aspect


def patch_module(module, advice):
    for object_name in dir(module):
        # check object name
        if advice.targets.match(object_name):
            continue

        source_object = getattr(module, object_name)
        setattr(module, object_name, patch_object(source_object))


def patch_past(advice):
    for module_name, module in sys.modules.items():
        if advice.modules.match(module_name):
            patch_module(module, advice)
