import sys


def patch_object(aspect, advice):
    pass


def patch_module(module, advice):
    for object_name in dir(module):
        if advice.targets.match(object_name):
            new_object = patch_object(getattr(module, object_name), advice)
            setattr(module, object_name, new_object)


def patch_past(advice):
    for module_name, module in sys.modules.items():
        if advice.modules.match(module_name):
            patch_module(module, advice)
