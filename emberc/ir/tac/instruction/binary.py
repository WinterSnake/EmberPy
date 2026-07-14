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
    from ....ast import BinaryOperator


## Classes
@dataclass(frozen=True, slots=True)
class TACBinary:
    """Represents a binary operation instruction."""
    dest: TACAddress
    left: TACOperand
    operator: BinaryOperator
    right: TACOperand
