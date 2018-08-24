# built-in
from contextlib import suppress

# external
import attr

# project
from .advice import advices as all_advices
from .state import state


@attr.s()
class Context:
    """Context is data class with information about JoinPoint context.

    Target info:
        aspect: name of target.
        method: name of called method or ``__call__`` for functions.
        module: name of module where aspect defined.
        path:   path to module where aspect defined.

    Call info:
        args:   tuple of passed positional args
        kwargs: dict of passed keyword args
        result: target's method response
    """
    aspect = attr.ib()
    method = attr.ib()
    module = attr.ib()
    path = attr.ib()

    args = attr.ib(default=None)
    kwargs = attr.ib(default=None)

    result = attr.ib(default=None)


class JoinPoint:
    """Wrapper around function or class method.
    """
    _method = None
    _advices_cache = None
    _advices_hashsum = None

    def __init__(self, **kwargs):
        self._context = Context(**kwargs)

    def __getattr__(self, name):
        return getattr(self._method, name)

    def __dir__(self):
        return dir(self._method)

    def __hash__(self):
        return hash(self._method)

    def _get_advices(self):
        if self._advices_hashsum == all_advices.hashsum:
            return self._advices_cache

        advices = []
        for advice in all_advices:
            if advice.paths.match(self._context.path):
                if advice.modules.match(self._context.module):
                    if advice.methods.match(self._context.method):
                        if advice.targets.match(self._context.aspect):
                            advices.append(advice)

        self._advices_cache = advices
        self._advices_hashsum = all_advices.hashsum
        return advices

    def __call__(self, *args, **kwargs):
        if not state.active:
            return self._method(*args, **kwargs)

        self._context.args = args
        self._context.kwargs = kwargs
        advices = [advice.handler(self._context) for advice in self._get_advices()]

        # joinpoint before aspect call
        [next(advice) for advice in advices]

        try:
            # aspect call
            self._context.result = self._method(*self._context.args, **self._context.kwargs)
        except Exception as e:
            # exception processing
            for advice in advices:
                with suppress(StopIteration):
                    advice.throw(e)
            return self._context.result

        # joinpoint after aspect call
        for advice in advices:
            with suppress(StopIteration):
                next(advice)

        return self._context.result
