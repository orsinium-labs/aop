from types import ModuleType

from .advice import advices
from .patchers import patch_object


class AspectModule(ModuleType):
    def __getattribute__(self, name):
        obj = super().__getattribute__(name)
        if name[:2] == '__':
            return obj

        # if object already patched by actual advices
        if obj._advices_hashsum == advices.hashsum:
            return obj

        # patch
        for advice in advices:
            if advice.modules.match(self.__name__):
                obj = patch_object(obj, advice)
        setattr(self, name, obj)

        return obj
