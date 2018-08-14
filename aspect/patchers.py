import sys

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


def patch_module(module, advice):
    for object_name in dir(module):
        # check object name
        if advice.targets.match(object_name):
            continue

        source_object = getattr(module, object_name)

        # patch class
        if isinstance(source_object, type):
            new_object = patch_class(source_object, advice)
            setattr(module, object_name, new_object)
        elif advice.methods.match('__call__'):
            new_object = patch_function(source_object, advice)
            setattr(module, object_name, new_object)


def patch_past(advice):
    for module_name, module in sys.modules.items():
        if advice.modules.match(module_name):
            patch_module(module, advice)
