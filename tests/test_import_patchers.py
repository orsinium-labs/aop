import sys
from types import ModuleType

from advice import import_patchers as patchers
from advice.module import AspectModule


def test_patch_cache():
    import textwrap
    del textwrap

    patchers.patch_cache()
    assert isinstance(sys.modules['textwrap'], AspectModule)

    patchers.unpatch_cache()
    assert not isinstance(sys.modules['textwrap'], AspectModule)
    assert isinstance(sys.modules['textwrap'], ModuleType)


def test_patch_import():
    import textwrap
    del sys.modules['textwrap']  # drop cache

    assert 'textwrap' not in sys.modules
    patchers.patch_import()
    import textwrap
    assert 'textwrap' in sys.modules
    assert isinstance(sys.modules['textwrap'], AspectModule)
    assert isinstance(textwrap, AspectModule)

    patchers.unpatch_import()
    del sys.modules['textwrap']  # drop cache
    import textwrap
    assert not isinstance(sys.modules['textwrap'], AspectModule)
    assert isinstance(sys.modules['textwrap'], ModuleType)
