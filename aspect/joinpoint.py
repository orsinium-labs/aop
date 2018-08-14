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
        advice = self._advice.handler(self)
        next(advice)
        try:
            self.result = self._method(*self.args, **self.kwargs)
        except Exception as e:
            with suppress(StopIteration):
                advice.throw(e)
        else:
            with suppress(StopIteration):
                next(advice)
        return self.result
