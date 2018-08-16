from importlib.util import module_from_spec
from _frozen_importlib_external import PathFinder
from .module import wrap_module


class AspectFinder(PathFinder):
    @classmethod
    def find_spec(cls, *args, **kwargs):
        spec = super().find_spec(*args, **kwargs)
        if spec is not None:
            spec.loader = AspectLoader(spec.loader)
        return spec


class AspectLoader:
    def __init__(self, loader):
        self._loader = loader

    def __getattr__(self, name):
        return getattr(self._loader, name)

    def create_module(self, spec):
        spec.loader = spec.loader._loader
        module = module_from_spec(spec)
        spec.loader = spec.loader
        return wrap_module(module)
