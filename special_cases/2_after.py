# apply aop after module import

# built-in
import math

# project
import aop  # noQA


result = math.cos(0)
assert math.isclose(result, 100.0), 'not patched'
