import re
import sys

import pytest

from advice.advice import Advice
from advice.module import AspectModule
from advice.joinpoint import JoinPoint
from advice import import_patchers as patchers


@pytest.fixture()
def clean():
    if 'textwrap' in sys.modules:
        del sys.modules['textwrap']
    patchers.unpatch_import()
    patchers.unpatch_cache()


def handler(context):
    yield
    context.result = 'lol'


advice = Advice(
    handler=handler,
    modules=re.compile('textwrap'),
    targets=re.compile('fill'),
)


def test_source(clean):
    import textwrap
    assert textwrap.fill.__module__ == 'textwrap'


def test_before(register_advice, clean):
    register_advice(advice)
    patchers.patch_import()
    import textwrap

    assert isinstance(textwrap, AspectModule)
    assert isinstance(textwrap.fill, JoinPoint)
    assert textwrap.fill('test') == 'lol'


# def test_after(register_advice, clean):
#     import textwrap
#     register_advice(advice)
#     patchers.patch_import()
#
#     assert isinstance(textwrap, AspectModule)
#     assert isinstance(textwrap.fill, JoinPoint)
#     assert textwrap.fill('test') == 'lol'


def test_from_before(register_advice, clean):
    register_advice(advice)
    patchers.patch_import()
    from textwrap import fill

    assert isinstance(fill, JoinPoint)
    assert fill('test') == 'lol'


# def test_from_after(register_advice, clean):
#     from textwrap import fill
#     register_advice(advice)
#     patchers.patch_import()
#
#     assert isinstance(fill, JoinPoint)
#     assert fill('test') == 'lol'


def test_cached_before(register_advice, clean):
    import textwrap
    del textwrap

    register_advice(advice)
    patchers.patch_cache()
    from textwrap import fill

    assert isinstance(fill, JoinPoint)
    assert fill('test') == 'lol'
