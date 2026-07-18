##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## IR: 3AC                       ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, assert_never
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
    from collections.abc import Iterator, MutableSequence

## Constants
__all__ = (
    "TACUnit",
    "TACVisitor",
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
    def __iter__(self) -> Iterator[TACInstruction]:
        yield from self.instructions

    # -Properties
    instructions: MutableSequence[TACInstruction]


class TACVisitor[TReturn](ABC):
    """A visitor pattern interface for traversing tac instructions."""
    # -Instance Methods
    def visit(self, tac: TACInstruction) -> TReturn:
        match tac:
            case TACAssign():
                return self.visit_assignment(tac)
            case TACBinary():
                return self.visit_binary(tac)
            case TACDeclare():
                return self.visit_declare(tac)
            case _:
                assert_never(tac)

    @abstractmethod
    def visit_assignment(self, tac: TACAssign) -> TReturn: ...

    @abstractmethod
    def visit_binary(self, tac: TACBinary) -> TReturn: ...

    @abstractmethod
    def visit_declare(self, tac: TACDeclare) -> TReturn: ...

    # -Class Properties
    __slots__ = ()
