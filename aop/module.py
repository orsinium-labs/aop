# project
from .patchers import patch_object


class AspectModule:
    def __init__(self, module):
        self._wrapped_module = module

    def __dir__(self):
        return dir(self._wrapped_module)

    @property
    def __all__(self):
        return dir(self._wrapped_module)

    def __getattribute__(self, name):
        try:
            obj = super().__getattribute__(name)
        except AttributeError:
            obj = getattr(self._wrapped_module, name)
        if name[:2] == '__':
            return obj
        if name == '_wrapped_module':
            return obj

        # patch
        obj = patch_object(obj)
        setattr(self, name, obj)

        return obj


def wrap_module(module):
    if isinstance(module, AspectModule):
        return
    return AspectModule(module)


def unwrap_module(module):
    return getattr(module, '_wrapped_module', module)
