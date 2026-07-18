##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## MIR: Register                 ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from enum import IntEnum
from typing import Self

## Constants
type MIRRegister = PhysicalRegister | VirtualRegister


## Classes
@dataclass(frozen=True, slots=True)
class PhysicalRegister:
    """"""
    # -Instance Methods
    def id_as[T: IntEnum](self, _type: type[T]) -> T:
        return _type(self.id)

    # -Class Methods
    @classmethod
    def id_from(cls, name: IntEnum) -> Self:
        return cls(name.value)

    # -Properties
    id: int


@dataclass(frozen=True, slots=True)
class VirtualRegister:
    """"""
    id: int
