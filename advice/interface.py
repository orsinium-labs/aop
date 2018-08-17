from .advice import advices, Advice
from .state import state
from .import_patchers import patch_import, patch_cache, unpatch_import, unpatch_cache


def enable():
    if state.active:
        return
    state.active = True
    patch_import()
    patch_cache()


def disable():
    if not state.active:
        return
    state.active = False
    unpatch_import()
    unpatch_cache()


def register(handler, **kwargs):
    enable()
    advices.register(Advice(handler=handler, **kwargs))
