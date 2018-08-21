# project
from .advice import Advice, advices
from . import import_patchers as patchers
from .state import state


def enable(*, force=False):
    if not force and state.active:
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
    if state.started:
        raise Exception("Please, don't register advices after aop.start()")
    enable()
    advices.register(Advice(handler=handler, **kwargs))


def start(force=False):
    if not force and state.started:
        raise Exception("Please, don't start AOP twice.")
    state.started = True
    disable()
    enable()
