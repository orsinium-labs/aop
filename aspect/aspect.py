from collections import Callable

from .joinpoint import JoinPoint


class Aspect:
    def __getattribute__(self, name):
        method = super().__getattribute__(name)

        # dispatch
        if name[:2] == '__':
            return method
        if not isinstance(method, Callable):
            return method
        if name == '_advices':
            return method

        advices = [advice for advice in self._advices if advice.methods.match(name)]
        if not advices:
            return method

        # prepare and return joinpoint
        joinpoint = JoinPoint(
            aspect=self.__class__.__name__,
            module=self.__module__,
            method=name,
        )
        joinpoint._method = method
        joinpoint._advices = advices
        return joinpoint
