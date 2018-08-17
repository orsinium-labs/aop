# apply advices after module import

import math
import advices  # noQA


result = math.cos(0)
assert math.isclose(result, 100.0), 'not patched'
