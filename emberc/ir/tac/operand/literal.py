##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## 3AC Operand: Literal          ##
##-------------------------------##

## Imports
from dataclasses import dataclass


## Classes
@dataclass(frozen=True, slots=True)
class TACLiteral:
    """Represents a constant integer literal value."""
    value: int
