# 1. enable
# 2. import
# apply advices

import advice
advice.enable()
import math  # noQA
import advices  # noQA


result = math.cos(0)
assert math.isclose(result, 100.0), 'not patched'