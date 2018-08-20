# AOP

[Aspect-oriented programming](https://en.wikipedia.org/wiki/Aspect-oriented_programming)

Features:

1. Patch any module: your project, stdlib, built-ins.
1. Patch any object: functions, class instances.
1. Pure Python implementation: run it on CPython or PyPy.

TODO:

1. Patch already imported objects
1. Patch `__init__` and `__new__`.
1. Test PyPy
1. Test cases via tox


## Usage

```python
import aop


def multiply(context):
    print(context.args)
    print(context.kwargs)
    yield
    context.result *= 100


aop.register(
    handler=multiply,
    modules=aop.match(equals='math'),
    targets=aop.match(regexp='(sin|cos)')
)
```

Ok, let's check:

```python
In [2]: import math

In [3]: math.cos(0)
(0,)
{}
Out[3]: 100.0
```
