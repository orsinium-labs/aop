from aspect import utils


def test_startswith():
    expr = utils.StartsWith('abc')
    assert expr.match('abcdef') is True
    assert expr.match('abef') is False
    assert expr.match('dabc') is False


def test_endswith():
    expr = utils.EndsWith('def')
    assert expr.match('abcdef') is True
    assert expr.match('abef') is False
    assert expr.match('defa') is False


def test_contains():
    expr = utils.Contains('def')
    assert expr.match('abcdef') is True
    assert expr.match('defabc') is True
    assert expr.match('adefbc') is True
    assert expr.match('abef') is False
    assert expr.match('befa') is False


def test_regexp():
    expr = utils.RegExp(r'a{3}')
    assert expr.match('a') is False
    assert expr.match('aa') is False
    assert expr.match('aaa') is True
    assert expr.match('aaaa') is False


def test_match():
    expr = utils.match(regexp=r'a{3}')
    assert expr.match('a') is False
    assert expr.match('aa') is False
    assert expr.match('aaa') is True
    assert expr.match('aaaa') is False

    expr = utils.match(startswith='a')
    assert isinstance(expr, utils.StartsWith)

    expr = utils.match(endswith='a')
    assert isinstance(expr, utils.EndsWith)

    expr = utils.match(contains='a')
    assert isinstance(expr, utils.Contains)
