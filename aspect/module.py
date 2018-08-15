from types import ModuleType

from .advice import advices


class AspectModule(ModuleType):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattribute__(self, name):
        obj = super().__getattribute__(name)
        if name[:2] == '__':
            return obj
        # if object already patched by actual advices
        if obj._advices_hashsum == advices.hashsum:
            return obj

        ...
