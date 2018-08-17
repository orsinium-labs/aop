from .patchers import patch_object


class MethodGetter:
    def __init__(self, module, name):
        self.module = module
        self.name = name

    def __get__(self, **args):
        obj = getattr(self.module, self.name)
        return patch_object(obj)


class AspectModule:
    def __init__(self, module):
        self._wrapped_module = module
        # for name in dir(module):
        #     setattr(self, name, MethodGetter(module, name))

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
