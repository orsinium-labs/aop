# apply advices after module caching

import math
del math
import advices  # noQA
import math  # noQA


result = math.cos(0)
assert math.isclose(result, 100.0), 'not patched'
