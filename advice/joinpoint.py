from contextlib import suppress

import attr


@attr.s
class JoinPoint:
    aspect = attr.ib()
    method = attr.ib()
    module = attr.ib()

    args = attr.ib(default=None)
    kwargs = attr.ib(default=None)

    result = attr.ib(default=None)

    _method = None
    _advices = None

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        advices = [advice.handler(self) for advice in self._advices]

        # joinpoint before aspect call
        [next(advice) for advice in advices]

        try:
            # aspect call
            self.result = self._method(*self.args, **self.kwargs)
        except Exception as e:
            # exception processing
            for advice in advices:
                with suppress(StopIteration):
                    advice.throw(e)
            return self.result

        # joinpoint after aspect call
        for advice in advices:
            with suppress(StopIteration):
                next(advice)

        return self.result
