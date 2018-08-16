import sys

from aspect import import_patchers as patchers
from aspect.module import AspectModule


def test_patch_past():
    import textwrap
    del textwrap

    patchers.patch_past()
    assert isinstance(sys.modules['textwrap'], AspectModule)
