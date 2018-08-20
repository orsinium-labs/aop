# Implementation details


## Issues and it's solutions

This is some troubles that I got when implemented this library.

* Issue: some packages can define `__spec__` variable
* Examples: [toml](https://github.com/uiri/toml/commit/7ab5a08bc41bc084ea1a6b52e266bcf2ec5e6dde#diff-a6c8ad0879cab1e064573279bfc148bf)
* Solution:
    ```python
    getattr(aspect.__globals__['__spec__'], 'name', '')
    if not getattr(module.__spec__, 'origin', None): continue
    ```

---

* Issue: some modules from stdlib uses starred import
* Examples: [lzma](https://github.com/python/cpython/blob/master/Lib/lzma.py), [locale](https://github.com/python/cpython/blob/master/Lib/locale.py)
* Solution: implement `__dir__` method for module objects.

---

* Issue: `__spec__` can be None
* Examples: see [import system documentation](https://docs.python.org/3/reference/import.html#main-spec)
* Solution: if you need module name, get it from module or it's objects:
    ```python
    module = getattr(aspect, '__module__', '')
    ```

---

* Issue: some modules or objects can be lazy imported
* Examples: [importlib.util.LazyLoader](https://docs.python.org/3/library/importlib.html#importlib.util.LazyLoader) provide this functionality.
* Solution: patch module object and wrap objects on access.

---

* Issue: some objects forbid inherited classes creation.
* Examples: `_bz2.BZ2Compressor`
* Solution: try to patch and ignore object when it doesn't work:
    ```python
    from contextlib import suppress
    with suppress(TypeError):
        ...  # patch
    ```

---

* Issue: creating class instances before class MRO patching broke `isinstance` checks.
* Examples: [traitlets](https://github.com/ipython/traitlets/blob/4.3.2/traitlets/config/configurable.py#L421) (used into IPython)

---

* Issue: some libs adds some functions in sets.
* Solution: implement `__hash__` for joinpoint.

---

* Issue: some functions and methodscan contains attributes.
* Examples: `csrf_exempt` from Django set up attribute to view function.
* Solution: propagate attributes getting from joinpoint to wrapped object.
