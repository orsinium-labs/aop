# project
from .advice import Advice, advices
from . import import_patchers as patchers
from .state import state


def enable():
    if state.active:
        return
    state.active = True
    patchers.patch_import()
    patchers.patch_cache()
    patchers.patch_project()


def disable():
    if not state.active:
        return
    state.active = False
    patchers.unpatch_import()
    patchers.unpatch_cache()


def register(handler, **kwargs):
    enable()
    advices.register(Advice(handler=handler, **kwargs))
