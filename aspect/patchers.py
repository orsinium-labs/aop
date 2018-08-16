from collections import Callable

from .aspect import Aspect
from .joinpoint import JoinPoint


def patch_class(aspect, advice):
    # make new object name
    name = aspect.__name__
    if not name.endswith('Aspect'):
        name += 'Aspect'

    # patch
    return type(
        name,
        (Aspect, aspect),
        dict(
            _advices=[advice],
            _advices_hashsum=1,
        ),
    )


def patch_function(aspect, advice):
    joinpoint = JoinPoint(
        aspect=aspect.__name__,
        method='__call__',
        module=aspect.__module__,
    )
    joinpoint._method = aspect
    joinpoint._advices = [advice]
    joinpoint._advices_hashsum = 1
    return joinpoint


def patch_object(aspect, advice):
    # add advice to patched aspect
    if hasattr(aspect, '_advices'):
        if advice not in aspect._advices:
            aspect._advices.append(advice)
            aspect._advices_hashsum += 1
        return aspect

    # class
    if isinstance(aspect, type):
        return patch_class(aspect, advice)

    # function
    if isinstance(aspect, Callable) and advice.methods.match('__call__'):
        return patch_function(aspect, advice)

    return aspect
