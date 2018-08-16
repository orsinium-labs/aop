import sys
from .patchers import patch_object


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
