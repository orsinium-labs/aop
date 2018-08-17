import sys
from _frozen_importlib_external import PathFinder

from .hooks import AspectFinder
from .module import wrap_module, unwrap_module


def patch_past():
    for module_name, module in sys.modules.copy().items():
        sys.modules[module_name] = wrap_module(module)


def unpatch_past():
    for module_name, module in sys.modules.items():
        sys.modules[module_name] = unwrap_module(module)


def patch_future():
    if AspectFinder in sys.meta_path:
        return
    index = sys.meta_path.index(PathFinder)
    sys.meta_path[index] = AspectFinder


def unpatch_future():
    if AspectFinder not in sys.meta_path:
        return
    index = sys.meta_path.index(AspectFinder)
    sys.meta_path[index] = PathFinder
