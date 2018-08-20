# import from module, patch before import

import advices  # noQA
from math import cos, isclose


result = cos(0)
assert isclose(result, 100.0), 'not patched'
