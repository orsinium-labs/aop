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
