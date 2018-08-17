# Advice

[Aspect-oriented programming](https://en.wikipedia.org/wiki/Aspect-oriented_programming)

## Usage

```python
import advice


def multiply(context):
    print(context.args)
    print(context.kwargs)
    yield
    context.result *= 100


advice.register(
    handler=multiply,
    modules=advice.match(equals='math'),
    targets=advice.match(regexp='(sin|cos)')
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
