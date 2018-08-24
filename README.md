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


## Example

```python
import aop

def multiply(context):
    print(context.aspect, context.args, context.kwargs)
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
import math
math.cos(0)
# prints: cos (0,) {}
# returns: 100.0
```


# Usage

Register new advice:

```python
aop.register(
    handler=some_handler,
    modules=aop.match(equals='math'),
    targets=aop.match(regexp='(sin|cos)')
)
```

Parameters for `aop.register`:
* `handler` -- advice for joinpoint processing.
* `paths` -- expression for path to module.
* `modules` -- expression for module name.
* `targets` -- expression for object name.
* `methods` -- expression for called object's method. It's `__call__` for functions.


Handler looks like:

```python
def multiply(context):
    ...  # before aspect call
    yield
    ...  # after aspect call
```

Context's properties:
* `aspect` -- name of target.
* `method` -- name of called method or `__call__` for functions.
* `module` -- name of module where aspect defined.
* `path` --   path to module where aspect defined.
* `args` --   tuple of passed positional args
* `kwargs` -- dict of passed keyword args
* `result` -- target's method response

Register all advices or just enable patching before all other imports in project:

```python
import aop
aop.enable()
...  # all other imports
```

Also it's recommend finally enable patching after register last advice:

```python
aop.register(...)
aop.register(...)
aop.enable(final=True)
```

If you want to disable patching:
```python
aop.disable()
```

Inspect object:

```python
aop.inspect(math.isclose, print=True)
```

## Patch import system automatically

Now this package can't patch modules that imported before `aop.enable()` or `aop.register(...)`:

```bash
$ python3 special_cases/2_after.py
...
AssertionError: not patched
```

Although you can run your script via aop runner:

```bash
$ python3 -m aop special_cases/2_after.py
cos (0,) {}
```
