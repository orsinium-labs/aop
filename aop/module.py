# project
from .patchers import patch_object
from .state import state
from .advice import advices


class AspectModule:
    def __init__(self, module):
        self._wrapped_module = module

    def __dir__(self):
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

        # TODO: check for started

        # patch
        obj = patch_object(obj)
        setattr(self, name, obj)

        return obj


def wrap_module(module):
    # don't patch twice
    if isinstance(module, AspectModule):
        return module

    # if started, don't patch modules that not match any known advice
    if state.started:
        for advice in advices:
            if advice.modules.match(module.__name__):
                break
        else:
            return module

    return AspectModule(module)


def unwrap_module(module):
    return getattr(module, '_wrapped_module', module)
