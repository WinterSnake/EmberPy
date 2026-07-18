##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## x86_64 Instruction: Mul       ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from ..register import x86Register
from ...mir import (
    MIRInstruction,
    PhysicalRegister,
)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from ...mir import (
        MIRRegister
    )

## Classes
@dataclass(frozen=True, slots=True)
class x86Mul(MIRInstruction):
    """
    Supports:
    mul %reg
    """
    # -Properties
    src: MIRRegister

    @property
    def reads(self) -> Sequence[MIRRegister]:
        return (
            PhysicalRegister.id_from(x86Register.RAX),
            self.src
        )

    @property
    def writes(self) -> Sequence[MIRRegister]:
        return (
            PhysicalRegister.id_from(x86Register.RAX),
            PhysicalRegister.id_from(x86Register.RDX),
        )
