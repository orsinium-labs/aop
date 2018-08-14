from collections import Callable

from .joinpoint import JoinPoint


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
