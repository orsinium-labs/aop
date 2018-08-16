import sys
from _frozen_importlib_external import PathFinder

from .hooks import AspectFinder
from .module import wrap_module


def patch_past():
    for module_name, module in sys.modules.items():
        setattr(module, wrap_module(module_name))


def patch_future():
    index = sys.meta_path.index(PathFinder)
    sys.meta_path[index] = AspectFinder
