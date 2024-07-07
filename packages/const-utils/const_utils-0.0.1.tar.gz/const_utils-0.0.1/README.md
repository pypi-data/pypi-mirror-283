# Const-Utils

`const-utils` is a small-yet-effective library that offers some
tools for working with Python constants. Its main feature is
the *Constant Class*, which includes utilities for accessing
constants, stored within a container class.

Defining constant classes is available by using `ConstClassMeta`
(as a metaclass), or the standard `BaseConstClass` (by inheritance).

## Examples
### Creating a constant class
```python
class CountryConsts(BaseConstClass):
    US = 'United States of America'
    UK = 'United Kingdom'
```

### Access options
#### Access from the class itself
```python
>>> CountryConsts.as_dict()  # {'US': 'United States of America', 'UK': 'United Kingdom'}
>>> CountryConsts['US']  # 'United States of America
>>> Country.const_names  # ['US, 'UK']
>>> Country.const_values  # ['United States of America', 'United Kingdom']
```

#### Access global/local constants
```python
>>> # Access current global/local constants (depends on kwarg `local`)
>>> # as a dictionary of names to values
>>> access_namespace_consts(local=False)
```

### Storing class constants to a namespace
```python
>>> # Store constants in a module
>>> CountryConsts.apply_to_module('some_module_name', override=True)
>>> # Store constants as globals
>>> CountryConsts.apply()
>>> # Store constants as locals
>>> CountryConsts.apply(local=True)
```