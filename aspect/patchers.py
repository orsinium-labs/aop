import sys

from .aspect import Aspect


def patch_object(aspect, advice):
    name = aspect.__name__
    if not name.endswith('Aspect'):
        name += 'Aspect'
    return type(
        name,
        [Aspect, aspect],
        {'_advice': advice},
    )


def patch_module(module, advice):
    for object_name in dir(module):
        if advice.targets.match(object_name):
            source_object = getattr(module, object_name)
            if isinstance(source_object, type):
                new_object = patch_object(source_object, advice)
                setattr(module, object_name, new_object)


def patch_past(advice):
    for module_name, module in sys.modules.items():
        if advice.modules.match(module_name):
            patch_module(module, advice)
