# 1. enable
# 2. import
# apply aop

# built-in
import math  # noQA

# project
import advice
import aop  # noQA


advice.enable()


result = math.cos(0)
assert math.isclose(result, 100.0), 'not patched'
