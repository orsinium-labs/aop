# import from module, patch before import

from math import cos, isclose
import advices  # noQA

import pdb; pdb.set_trace()

result = cos(0)
assert isclose(result, 100.0), 'not patched'
