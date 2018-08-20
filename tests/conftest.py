from aop.advice import advices
import pytest


@pytest.fixture()
def register_advice():
    catalog = advices.catalog.copy()
    yield advices.register
    advices.catalog = catalog
