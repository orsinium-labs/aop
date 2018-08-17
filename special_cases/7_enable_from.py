# 1. enable
# 2. import
# apply advices

import advice
advice.enable()
from math import isclose, cos  # noQA
import advices  # noQA


result = cos(0)
assert isclose(result, 100.0), 'not patched'
