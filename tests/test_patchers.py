import re
from aspect.patchers import patch_class, patch_function, patch_object
from aspect.advice import Advice


def test_patch_class():
    class Source:
        def check_me(self, a, b=None):
            return '{}|{}'.format(a, b)

    def handler(context):
        yield
        context.result = 'lol'

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    Patched = patch_class(Source, advice)
    instance = Patched()
    result = instance.check_me(1, 2)
    assert result == 'lol'


def test_patch_function():
    def check_me(a, b=None):
            return '{}|{}'.format(a, b)

    def handler(context):
        yield
        context.result = 'lol'

    advice = Advice(handler=handler)
    patched = patch_function(check_me, advice)
    result = patched(1, 2)
    assert result == 'lol'


def test_patch_object():
    def check_me(a, b=None):
            return '{}|{}'.format(a, b)

    def handler1(context):
        yield
        context.result += '|3'

    def handler2(context):
        yield
        context.result += '|4'

    advice = Advice(handler=handler1)
    patched = patch_object(check_me, advice)

    advice = Advice(handler=handler2)
    patched = patch_object(patched, advice)

    result = patched(1, 2)
    assert result == '1|2|3|4'
