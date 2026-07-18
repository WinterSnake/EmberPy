##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## x86_64 Instruction: Sub       ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from ...mir import MIRInstruction

if TYPE_CHECKING:
    from collections.abc import Sequence
    from ...mir import (
        MIROperand,
        MIRRegister
    )

## Classes
@dataclass(frozen=True, slots=True)
class x86Sub(MIRInstruction):
    """
    Supports:
    sub %reg, %reg
    sub %reg, <immediate>
    """
    # -Properties
    dest: MIRRegister
    src: MIROperand

    @property
    def reads(self) -> Sequence[MIRRegister]:
        match self.src:
            case int():
                return (self.dest,)
            case _:
                return (self.dest, self.src)

    @property
    def writes(self) -> Sequence[MIRRegister]:
        return (self.dest,)
