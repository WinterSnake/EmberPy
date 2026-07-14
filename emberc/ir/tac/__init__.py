##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## IR: 3AC                       ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING
from dataclasses import dataclass

from .instruction import (
    TACInstruction,
    TACInstructionBlock,
    TACAssign,
    TACBinary,
    TACDeclare,
)
from .operand import (
    TACAddress,
    TACOperand,
    TACLiteral,
    TACTemporary,
    TACVariable,
)

if TYPE_CHECKING:
    from collections.abc import Iterable, MutableSequence

## Constants
__all__ = (
    # -Operand
    "TACAddress",
    "TACOperand",
    "TACLiteral",
    "TACTemporary",
    "TACVariable",
    # -Instruction
    "TACInstruction",
    "TACInstructionBlock",
    "TACAssign",
    "TACBinary",
    "TACDeclare",
)


## Classes
@dataclass(slots=True)
class TACUnit:
    """A mutable translation unit holding the final sequence of flattened TAC instructions."""
    # -Dunder Methods
    def __iter__(self) -> Iterable[TACInstruction]:
        yield from self.instructions

    # -Properties
    instructions: MutableSequence[TACInstruction]
