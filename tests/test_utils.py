from aop import matcher


def test_startswith():
    expr = matcher.StartsWith('abc')
    assert expr.match('abcdef') is True
    assert expr.match('abef') is False
    assert expr.match('dabc') is False


def test_endswith():
    expr = matcher.EndsWith('def')
    assert expr.match('abcdef') is True
    assert expr.match('abef') is False
    assert expr.match('defa') is False


def test_contains():
    expr = matcher.Contains('def')
    assert expr.match('abcdef') is True
    assert expr.match('defabc') is True
    assert expr.match('adefbc') is True
    assert expr.match('abef') is False
    assert expr.match('befa') is False


def test_regexp():
    expr = matcher.RegExp(r'a{3}')
    assert expr.match('a') is False
    assert expr.match('aa') is False
    assert expr.match('aaa') is True
    assert expr.match('aaaa') is False


def test_equals():
    expr = matcher.RegExp('bc')
    assert expr.match('a') is False
    assert expr.match('abc') is False
    assert expr.match('bcd') is False
    assert expr.match('bc') is True


def test_match():
    expr = matcher.match(regexp=r'a{3}')
    assert expr.match('a') is False
    assert expr.match('aa') is False
    assert expr.match('aaa') is True
    assert expr.match('aaaa') is False

    expr = matcher.match(startswith='a')
    assert isinstance(expr, matcher.StartsWith)

    expr = matcher.match(endswith='a')
    assert isinstance(expr, matcher.EndsWith)

    expr = matcher.match(contains='a')
    assert isinstance(expr, matcher.Contains)
