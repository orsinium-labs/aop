from .advice import advices, Advice
from .state import state
from .import_patchers import patch_future, patch_past, unpatch_future, unpatch_past


def enable():
    if state.active:
        return
    state.active = True
    patch_future()
    patch_past()


def disable():
    if not state.active:
        return
    state.active = False
    unpatch_future()
    unpatch_past()


def register(handler, **kwargs):
    enable()
    advices.register(Advice(handler=handler, **kwargs))
