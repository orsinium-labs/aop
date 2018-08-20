# built-in
import re

# project
from aop.advice import Advice
from aop.patchers import patch_class, patch_function, patch_object


def test_patch_class(register_advice):
    class Source:
        def check_me(self, a, b=None):
            return '{}|{}'.format(a, b)

    def handler(context):
        yield
        context.result = 'lol'

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    register_advice(advice)
    Patched = patch_class(Source)
    instance = Patched()
    result = instance.check_me(1, 2)
    assert result == 'lol'


def test_patch_function(register_advice):
    def check_me(a, b=None):
            return '{}|{}'.format(a, b)

    def handler(context):
        yield
        context.result = 'lol'

    advice = Advice(handler=handler)
    register_advice(advice)
    patched = patch_function(check_me)
    result = patched(1, 2)
    assert result == 'lol'


def test_patch_object(register_advice):
    def check_me(a, b=None):
            return '{}|{}'.format(a, b)

    def handler1(context):
        yield
        context.result += '|3'

    def handler2(context):
        yield
        context.result += '|4'

    advice = Advice(handler=handler1)
    register_advice(advice)
    patched = patch_object(check_me)

    advice = Advice(handler=handler2)
    patched = patch_object(patched)
    register_advice(advice)

    result = patched(1, 2)
    assert result == '1|2|3|4'
