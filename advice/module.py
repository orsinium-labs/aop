from .patchers import patch_object


class AspectModule:
    def __init__(self, module):
        self._wrapped_module = module

    def __getattr__(self, name):
        return getattr(self._wrapped_module, name)

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
