# apply aop before module import

import advices  # noQA
import math


result = math.cos(0)
assert math.isclose(result, 100.0), 'not patched'
