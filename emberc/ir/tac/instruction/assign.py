##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## 3AC Instruction: Assign       ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..operand import (
        TACAddress,
        TACOperand,
    )


## Classes
@dataclass(frozen=True, slots=True)
class TACAssign:
    """Represents a direct assignment instruction."""
    dest: TACAddress
    src: TACOperand
