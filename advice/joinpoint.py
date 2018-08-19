from contextlib import suppress

import attr

from .advice import advices as all_advices


@attr.s(hash=False)
class JoinPoint:
    aspect = attr.ib()
    method = attr.ib()
    module = attr.ib()

    args = attr.ib(default=None)
    kwargs = attr.ib(default=None)

    result = attr.ib(default=None)

    _method = None
    _advices = None
    _advices_hashsum = None

    def __getattr__(self, name):
        return getattr(self._method, name)

    def __hash__(self):
        return hash(self._method)

    @property
    def advices(self):
        if self._advices_hashsum == all_advices.hashsum:
            return self._advices

        advices = []
        for advice in all_advices:
            if advice.modules.match(self.module):
                if advice.methods.match(self.method):
                    if advice.targets.match(self.aspect):
                        advices.append(advice)

        self._advices = advices
        self._advices_hashsum = all_advices.hashsum
        return advices

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        advices = [advice.handler(self) for advice in self.advices]

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
