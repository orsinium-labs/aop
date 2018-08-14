import re
from aspect.patchers import patch_class
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
