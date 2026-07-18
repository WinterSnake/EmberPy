##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backend: MIR                  ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .instruction import MIRInstruction
from .operand import MIROperand
from .register import (
    MIRRegister,
    PhysicalRegister,
    VirtualRegister,
)
from .selector import MIRInstructionSelector

if TYPE_CHECKING:
    from collections.abc import (
        Iterator,
        MutableSequence,
    )

## Constants
__all__ = (
    "MIRUnit",
    "MIRInstruction",
    "MIROperand",
    "MIRRegister",
    "PhysicalRegister",
    "VirtualRegister",
    "MIRInstructionSelector",
)


## Classes
@dataclass(slots=True)
class MIRUnit:
    """"""
    # -Dunder Methods
    def __iter__(self) -> Iterator[MIRInstruction]:
        yield from self.instructions

    # -Properties
    instructions: MutableSequence[MIRInstruction]
