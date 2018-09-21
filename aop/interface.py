# project
from .advice import Advice, advices
from . import import_patchers as patchers
from .state import state


def enable(*, force=False, final=False):
    """Apply patches for import system.

    force: ignore all checks
    final: set it if you already register all advices.
    """
    # check
    if not force:
        # already called with final
        if state.started:
            raise Exception(
                "Please, don't call aop.enable "
                "after calling aop.enable(final=True)")
        # already called without final
        if not final and state.active:
            return False

    # unpatch
    if final and state.active:
        patchers.unpatch_cache()

    # change state
    state.active = True
    if final:
        state.started = True

    # patch
    patchers.patch_import()
    patchers.patch_cache()
    patchers.patch_project()
    patchers.patch_builtins()
    return True


def disable():
    """Unpatch import system
    """
    if not state.active:
        return
    state.active = False
    patchers.unpatch_import()
    patchers.unpatch_cache()
    patchers.unpatch_builtins()


def register(handler, **kwargs):
    """Register new advice
    """
    if state.started:
        raise Exception(
            "Please, don't register advices"
            "after aop.enable(force=True)")
    enable()
    advices.register(Advice(handler=handler, **kwargs))
