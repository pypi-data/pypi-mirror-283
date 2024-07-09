# vistenum

The 'vistenum' package provides an opinionated 'enum' implementation.

# Usage

## Installation

Available from PyPI:

```bash
pip install vistenum
```

This package provides an opinionated 'enum' implementation through the
base enum class `VistEnum` and the `auto` function. Below is a brief example
implementing a weekday enumeration:

```python
"""Weekday provides an enumeration of the weekdays."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from vistenum import VistEnum, auto


class Weekday(VistEnum):
  """Weekday provides an enumeration of the weekdays."""
  MONDAY = auto()
  TUESDAY = auto()
  WEDNESDAY = auto()
  THURSDAY = auto()
  FRIDAY = auto()
  SATURDAY = auto()
  SUNDAY = auto()
```

### Enum Attributes

The `VistEnum` class provides the following attributes:

- `name`: The name of the enum member. Automatically set to the value as
  it appears in the class body.
- `value`: (Optional) The public value of the enum member. If not provided,
  the name of the enum member is used as the public value.

An internally managed, integer valued private attribute is used for logic
implementation. The name of the enum member is case-insensitive and is
set to the name as it appears in the class body.

### Human Readable Representation

`VistEnum` implements a custom `__str__` method such
that `str(Weekday.MONDAY)` actually returns `'Weekday.MONDAY'`. Of course,
this implementation omits the public value. Inclusion of the public value
depends on the `includeValue` attribute on the enum class. This class
attribute is implemented on the metaclass level, allowing it to be
changed dynamically at runtime.

(Please note that this behaviour must be
implemented on the metaclass level for the value to be shared between all
instances of the class. In general, runtime changes to class attributes
should be avoided.)

Below is an example of runtime toggling of public value inclusion:

```python
"""Weekday provides an enumeration of the weekdays."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from vistenum.example import Weekday

if __name__ == '__main__':
  print(Weekday.includeValue, Weekday.MONDAY)
  Weekday.includeValue = True
  print(Weekday.includeValue, Weekday.MONDAY)
```

The above code outputs:

```bash
False, Weekday.MONDAY
True, Weekday.MONDAY(MONDAY)
```

Please note that the default behaviour is to omit inclusion of the public
value. For the `Weekday` class, the public value is the name of the enum
member making inclusion redundant. In other situations, the public value
could belong to a class without a custom `__str__` implementation, making
inclusion of the public value cluttered and unreadable.

### Iteration Protocol

`VistEnum` implements the iteration protocol, allowing for iteration over
the enum members. The iteration order is the order of the enum members as
they appear in the class body. The iteration protocol is demonstrated in
the example below:

```python
"""Weekday provides an enumeration of the weekdays."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from vistenum.example import Weekday

if __name__ == '__main__':
  for weekday in Weekday:
    print(weekday)  # VistEnum provides a readable __str__ reimplementation
```

The above code outputs:

```bash
Weekday.MONDAY
Weekday.TUESDAY
Weekday.WEDNESDAY
Weekday.THURSDAY
Weekday.FRIDAY
Weekday.SATURDAY
Weekday.SUNDAY
```

### Hashing

The `VistEnum` class provides hashing allowing enum members to be used as
dictionary keys. For example:

```python
"""Ugedag provides a translation of the weekdays to Danish."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations
from vistenum.example import Weekday

if __name__ == '__main__':
  weekly = {Weekday.Monday : 'Family Home Evening',
            Weekday.Tuesday: 'None', Weekday.Wednesday: 'None', }
  print(weekly[Weekday.Monday])
```

The above code outputs:

```bash
Family Home Evening
```

### Public Value

The enum members of `Weekday` used the default public value which is the
name of the member. However, the public value can be set explicitly to
any value of any type as it is entirely semantic with respect to the vistenum
package. In the example below, the `Weekday` class is again implemented, but
this time with explicit public values:

```python
"""Ugedag provides a translation of the weekdays to Danish."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistenum import VistEnum, auto


class Ugedag(VistEnum):
  """Ugedag provides a translation of the weekdays to Danish."""
  includeValue = True
  MONDAY = auto('Mandag')
  TUESDAY = auto('Tirsdag')
  WEDNESDAY = auto('Onsdag')
  THURSDAY = auto('Torsdag')
  FRIDAY = auto('Fredag')
  SATURDAY = auto('Lørdag')
  SUNDAY = auto('Søndag')
```

Please note that the `Ugedag` class sets includeValue to True, meaning
that the public value is included in the string representation of the enum
members. The public value is set to the Danish translation of the weekdays:

```python
"""Ugedag provides a translation of the weekdays to Danish."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistenum.example import Ugedag

if __name__ == '__main__':
  for ugedag in Ugedag:
    print(ugedag)
  print("""Toggle public value inclusion off""")
  Ugedag.includeValue = False  # Toggle public value inclusion
  for ugedag in Ugedag:
    print(ugedag)
```

The above code outputs:

```bash
Ugedag.MONDAY(Mandag)
Ugedag.TUESDAY(Tirsdag)
Ugedag.WEDNESDAY(Onsdag)
Ugedag.THURSDAY(Torsdag)
Ugedag.FRIDAY(Fredag)
Ugedag.SATURDAY(Lørdag)
Ugedag.SUNDAY(Søndag)
Toggle public value inclusion off
Ugedag.MONDAY
Ugedag.TUESDAY
Ugedag.WEDNESDAY
Ugedag.THURSDAY
Ugedag.FRIDAY
Ugedag.SATURDAY
Ugedag.SUNDAY
```