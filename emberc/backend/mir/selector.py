##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## MIR: Selector                 ##
##-------------------------------##

## Imports
from abc import ABC
from collections.abc import Collection
from typing import TYPE_CHECKING, assert_never
from .instruction import MIRInstruction
from .register import VirtualRegister
from ...ir import (
    TACVisitor,
    TACLiteral,
    TACTemporary,
    TACVariable,
)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from .operand import MIROperand
    from ...ir import TACOperand, TACAddress
    from ...middleware import Symbol


## Classes
class MIRInstructionSelector(TACVisitor[Collection[MIRInstruction]], ABC):
    """"""
    # -Constructor
    def __init__(self, symbols: Sequence[Symbol]) -> None:
        self._symbols: Sequence[Symbol] = symbols
        self._register: int = 0
        self._temporary_registers: dict[int, VirtualRegister] = {}
        self._variable_registers: dict[int, VirtualRegister] = {}
    
    # -Instance Methods: Helpers
    def add_variable_register(self, _id: int) -> VirtualRegister:
        ''''''
        register = self.next_register
        self._variable_registers[_id] = register
        return register

    def add_temporary_register(self, index: int) -> VirtualRegister:
        ''''''
        register = self.next_register
        self._temporary_registers[index] = register
        return register

    # -Instance Methods: Visitors
    def visit_operand(self, operand: TACOperand) -> MIROperand:
        ''''''
        match operand:
            case TACLiteral():
                return operand.value
            case TACTemporary() | TACVariable():
                return self.visit_address(operand)
            case _:
                assert_never(operand)

    def visit_address(self, address: TACAddress) -> VirtualRegister:
        ''''''
        match address:
            case TACTemporary():
                if address.index not in self._temporary_registers:
                    self.add_temporary_register(address.index)
                return self._temporary_registers[address.index]
            case TACVariable():
                return self._variable_registers[address.id]
            case _:
                assert_never(address)

    # -Properties
    @property
    def next_register(self) -> VirtualRegister:
        ''''''
        _register = self._register
        self._register += 1
        return VirtualRegister(_register)

    # -Class Properties
    __slots__ = (
        "_symbols",
        "_register",
        "_temporary_registers",
        "_variable_registers"
    )
