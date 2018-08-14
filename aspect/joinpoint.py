from collections import Callable
from contextlib import suppress

import attr


@attr.s
class JoinPoint:
    aspect = attr.ib()
    method = attr.ib()

    args = attr.ib(default=None)
    kwargs = attr.ib(default=None)

    result = attr.ib(default=None)

    _method = None
    _advice = None

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        advice = self._advice(self)
        next(advice)
        try:
            self.result = self.method(*args, **kwargs)
        except Exception as e:
            advice.throw(e)
        with suppress(StopIteration):
            next(advice)
        return self.result


class Aspect:
    def __getattribute__(self, name):
        method = super().__getattribute__(name)
        if name[:2] == '__':
            return method
        if name == '_advice':
            return method
        if not isinstance(method, Callable):
            return method

        joinpoint = JoinPoint(
            aspect=self.__class__.__name__,
            method=name,
        )
        joinpoint._method = method
        joinpoint._advice = self._advice
        return joinpoint
