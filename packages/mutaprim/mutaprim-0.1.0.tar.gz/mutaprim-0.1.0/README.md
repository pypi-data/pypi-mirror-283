# Mutaprim

Mutaprim is very simple package containing a single module: `mutaprim`. The module contain 5 "mutable primitive" types, 
all inheriting from a base class called `MutablePrimitive`:
- `MutableBool`
- `MutableInt`
- `MutableFloat`
- `MutableStr`
- `MutableBytes`

An instance of any `MutablePrimitive` subclass will have the `value` property, as well as equivalent  `get` and `set` 
functions.

Here is a very simple demonstration:

```python
from mutaprim import MutableInt

def increment(integer: MutableInt):
    integer.value += 1

# `__init__` and `__str__`
mutable_int = MutableInt(0)
print(mutable_int)  # 0

# `get` and `set`
mutable_int.set(10)
print(mutable_int.get())  # 10

# `value`
increment(mutable_int)
print(mutable_int.value)  # 11
```