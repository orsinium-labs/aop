# project
from aop.patchers import patch_function


def test_hashable():
    def func(a, b):
        return a + b

    {func}
    patched = patch_function(func)
    {patched}
