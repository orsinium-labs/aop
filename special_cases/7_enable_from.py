# 1. enable
# 2. import
# apply aop

import advice
advice.enable()
from math import isclose, cos  # noQA
import aop  # noQA


result = cos(0)
assert isclose(result, 100.0), 'not patched'
