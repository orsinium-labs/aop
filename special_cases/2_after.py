# apply aop after module import

import math
import aop  # noQA


result = math.cos(0)
assert math.isclose(result, 100.0), 'not patched'
