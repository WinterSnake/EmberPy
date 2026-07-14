##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## 3AC Operand: Variable         ##
##-------------------------------##

## Imports
from dataclasses import dataclass


## Classes
@dataclass(frozen=True, slots=True)
class TACTemporary:
    """Represents a compiler-generated temporary variable."""
    index: int


@dataclass(frozen=True, slots=True)
class TACVariable:
    """Represents a user-defined source code variable."""
    id: int
