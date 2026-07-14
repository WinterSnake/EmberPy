##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## IR 3AC: Instruction           ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self
from .assign import TACAssign
from .binary import TACBinary
from .declare import TACDeclare

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

## Constants
__all__ = (
    "TACInstruction",
    "TACInstructionBlock",
    "TACAssign",
    "TACBinary",
    "TACDeclare",
)
type TACInstruction = TACAssign | TACBinary | TACDeclare


## Classes
@dataclass(frozen=True, slots=True)
class TACInstructionBlock:
    """An immutable, iterable sequence of TAC instructions, supporting flattened filtering."""
    # -Dunder Methods
    def __iter__(self) -> Iterator[TACInstruction]:
        yield from self.instructions

    # -Static Methods
    @staticmethod
    def filter(
        *instructions: TACInstruction | TACInstructionBlock | None
    ) -> Iterator[TACInstruction]:
        '''Flattens nested blocks, filters out None values, and yields a clean instruction stream.'''
        for instruction in instructions:
            match instruction:
                case TACInstructionBlock():
                    yield from instruction
                case None:
                    continue
                case _:
                    yield instruction

    # -Properties
    instructions: Sequence[TACInstruction]
