##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## 3AC Instruction: Declare      ##
##-------------------------------##

## Imports
from dataclasses import dataclass


## Classes
@dataclass(frozen=True, slots=True)
class TACDeclare:
    """Represents an explicit variable declaration instruction."""
    id: int
