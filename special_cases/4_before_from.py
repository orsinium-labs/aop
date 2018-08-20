# import from module, patch before import

# built-in
from math import cos, isclose

# project
import aop  # noQA


result = cos(0)
assert isclose(result, 100.0), 'not patched'
