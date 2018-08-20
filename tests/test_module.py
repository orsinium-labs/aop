# built-in
import re
import textwrap

# project
from aop.advice import Advice, advices
from aop.module import wrap_module


def handler1(context):
    yield
    context.result += '|3'


def handler2(context):
    yield
    context.result += '|4'


module = wrap_module(textwrap)


def test_wrapping():
    advices.catalog = []
    advices.register(Advice(
        handler=handler1,
        modules=re.compile('textwrap'),
        targets=re.compile('fill'),
    ))
    result = module.fill('12')
    assert result == '12|3'
