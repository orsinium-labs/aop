# project
from .advice import Advice, advices
from .import_patchers import patch_cache, patch_import, patch_project, unpatch_cache, unpatch_import
from .state import state


def enable():
    if state.active:
        return
    state.active = True
    patch_import()
    patch_cache()
    patch_project()


def disable():
    if not state.active:
        return
    state.active = False
    unpatch_import()
    unpatch_cache()


def register(handler, **kwargs):
    enable()
    advices.register(Advice(handler=handler, **kwargs))
