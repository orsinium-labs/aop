import re

import pytest
from advice.advice import Advice
from advice.aspect import Aspect


class Source:
    def check_me(self, a, b=None):
        return '{}|{}'.format(a, b)

    def nothing(self):
        return 42


class Patched(Aspect, Source):
    pass


def test_naive(register_advice):
    def handler(context):
        yield

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    register_advice(advice)
    instance = Patched()
    result = instance.check_me(1, 2)
    assert result == '1|2'


def test_patch_result(register_advice):
    def handler(context):
        yield
        context.result += '|3'

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    register_advice(advice)
    instance = Patched()
    result = instance.check_me(1, 2)
    assert result == '1|2|3'


def test_patch_input(register_advice):
    def handler(context):
        context.args = (4, 2)
        yield

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    register_advice(advice)
    instance = Patched()
    result = instance.check_me(1, 2)
    assert result == '4|2'


def test_catch(register_advice):
    def handler(context):
        try:
            yield
        except TypeError:
            pass

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    register_advice(advice)
    instance = Patched()
    result = instance.check_me(1, 2, 3)
    assert result is None


def test_uncatch(register_advice):
    def handler(context):
        yield

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    register_advice(advice)
    instance = Patched()
    with pytest.raises(TypeError):
        instance.check_me(1, 2, 3)


def test_raise_before(register_advice):
    def handler(context):
        raise ZeroDivisionError

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    register_advice(advice)
    instance = Patched()
    with pytest.raises(ZeroDivisionError):
        instance.check_me(1, 2)


def test_raise_after(register_advice):
    def handler(context):
        yield
        raise ZeroDivisionError

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    register_advice(advice)
    instance = Patched()
    with pytest.raises(ZeroDivisionError):
        instance.check_me(1, 2)


def test_method_check(register_advice):
    def handler(context):
        yield
        context.result = 13

    advice = Advice(methods=re.compile('check_me'), handler=handler)
    register_advice(advice)
    instance = Patched()
    result = instance.nothing()
    assert result == 42
