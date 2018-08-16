from types import ModuleType

from .advice import advices
from .patchers import patch_object


class AspectModule(ModuleType):
    def __getattribute__(self, name):
        obj = super().__getattribute__(name)
        if name[:2] == '__':
            return obj

        # if object already patched by actual advices
        if getattr(obj, '_advices_hashsum', 0) == advices.hashsum:
            return obj

        # patch
        for advice in advices:
            if advice.modules.match(self.__name__):
                obj = patch_object(obj, advice)
        setattr(self, name, obj)

        return obj


def wrap_module(module):
    if isinstance(module, AspectModule):
        return
    new_module = AspectModule(module.__name__)
    for name in dir(module):
        setattr(new_module, name, getattr(module, name))
    new_module._wrapped_module = module
    return new_module


def unwrap_module(module):
    return getattr(module, '_wrapped_module', module)
