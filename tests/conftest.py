# external
import pytest

# project
from aop.advice import advices
from aop.state import state


state.active = True


@pytest.fixture()
def register_advice():
    catalog = advices.catalog.copy()
    yield advices.register
    advices.catalog = catalog
