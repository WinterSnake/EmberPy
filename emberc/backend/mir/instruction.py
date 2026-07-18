##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## MIR: Instruction              ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from .register import MIRRegister


## Classes
class MIRInstruction(ABC):
    """"""
    # -Properties
    @property
    @abstractmethod
    def reads(self) -> Sequence[MIRRegister]:
        ''''''
        ...

    @property
    @abstractmethod
    def writes(self) -> Sequence[MIRRegister]:
        ''''''
        ...

    # -Class Properties
    __slots__ = ()
