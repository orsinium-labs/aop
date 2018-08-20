# project
from aop.hooks import AspectFinder, AspectLoader
from aop.module import AspectModule


def test_finder_and_loader():
    spec = AspectFinder.find_spec('pytest')
    assert spec is not None
    assert isinstance(spec.loader, AspectLoader)

    module = spec.loader.create_module(spec)
    assert isinstance(module, AspectModule)
