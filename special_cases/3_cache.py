# apply aop after module caching

# built-in
import math  # noQA

# project
import aop  # noQA


del math


result = math.cos(0)
assert math.isclose(result, 100.0), 'not patched'
