from _frozen_importlib_external import PathFinder, SourceFileLoader
from .module import wrap_module


class AspectFinder(PathFinder):
    @classmethod
    def find_spec(cls, *args, **kwargs):
        spec = super().find_spec(*args, **kwargs)
        spec.loader = AspectLoader
        return spec


class AspectLoader(SourceFileLoader):
    def create_module(self, spec):
        module = super().create_module(spec)
        return wrap_module(module)
