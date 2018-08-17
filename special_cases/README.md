
```bash
pip install --user -e .
cd special_cases
python3 1.py

python3 1_before.py
...
```

Doesn't work yet: 2, 5, 7.


Issues:
1. Import before patching creates direct pointer to module, bypass patched module.
2. Import with `from` creates direct link to patched object, bypass patched module. Solution: check advices for module from object.
