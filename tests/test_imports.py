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
    # assert isinstance(textwrap.fill, JoinPoint)

    # assert textwrap.fill._method.__module__ == textwrap.fill.module
    # assert textwrap.fill._method.__module__ == 'textwrap'

    # assert textwrap.fill('test') == 'lol'
