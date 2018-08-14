import re

import pytest
from aspect.advice import Advice
from aspect.aspect import Aspect


class Source:
    def check_me(self, a, b=None):
        return '{}|{}'.format(a, b)

    def nothing(self):
        return 42


class Patched(Aspect, Source):
    pass


def test_naive():
    def handler(context):
        yield

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    Patched._advice = advice
    instance = Patched()
    result = instance.check_me(1, 2)
    assert result == '1|2'


def test_patch_result():
    def handler(context):
        yield
        context.result += '|3'

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    Patched._advice = advice
    instance = Patched()
    result = instance.check_me(1, 2)
    assert result == '1|2|3'


def test_patch_input():
    def handler(context):
        context.args = (4, 2)
        yield

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    Patched._advice = advice
    instance = Patched()
    result = instance.check_me(1, 2)
    assert result == '4|2'


def test_catch():
    def handler(context):
        try:
            yield
        except TypeError:
            pass

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    Patched._advice = advice
    instance = Patched()
    result = instance.check_me(1, 2, 3)
    assert result is None


def test_uncatch():
    def handler(context):
        yield

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    Patched._advice = advice
    instance = Patched()
    with pytest.raises(TypeError):
        instance.check_me(1, 2, 3)


def test_raise_before():
    def handler(context):
        raise ZeroDivisionError

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    Patched._advice = advice
    instance = Patched()
    with pytest.raises(ZeroDivisionError):
        instance.check_me(1, 2)


def test_raise_after():
    def handler(context):
        yield
        raise ZeroDivisionError

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    Patched._advice = advice
    instance = Patched()
    with pytest.raises(ZeroDivisionError):
        instance.check_me(1, 2)


def test_method_check():
    def handler(context):
        yield
        context.result = 13

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    Patched._advice = advice
    instance = Patched()
    result = instance.nothing()
    assert result == 42
