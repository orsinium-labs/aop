# 1. enable
# 2. import
# apply aop

# built-in
import aop
aop.enable()

from math import cos, isclose  # noQA
import advices  # noQA


result = cos(0)
assert isclose(result, 100.0), 'not patched'
