# external
import pytest

# project
from aop.advice import advices


@pytest.fixture()
def register_advice():
    catalog = advices.catalog.copy()
    yield advices.register
    advices.catalog = catalog
