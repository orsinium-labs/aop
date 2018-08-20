# import from module, patch before import

from math import cos, isclose
import advices  # noQA


result = cos(0)
assert isclose(result, 100.0), 'not patched'
