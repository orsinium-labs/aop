# 1. enable
# 2. import
# apply aop

# built-in
from math import cos, isclose  # noQA

# project
import advice
import aop  # noQA


advice.enable()


result = cos(0)
assert isclose(result, 100.0), 'not patched'
