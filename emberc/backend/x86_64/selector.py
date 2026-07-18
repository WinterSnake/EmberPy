##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## x86_64: Selector              ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING, assert_never
from .instructions import (
    x86Mov,
    x86Add,
    x86Sub,
    x86Mul,
)
from .register import x86Register
from ..mir import (
    MIRUnit,
    PhysicalRegister,
    MIRInstructionSelector,
)
from ...ast import BinaryOperator

if TYPE_CHECKING:
    from collections.abc import Collection, Sequence
    from ..mir import MIRInstruction
    from ...ir import (
        TACUnit,
        TACAssign,
        TACBinary,
        TACDeclare,
    )
    from ...middleware import Symbol


## Classes
class x86_64InstructionSelector(MIRInstructionSelector):
    """"""
    # -Instance Methods
    def visit_assignment(self, tac: TACAssign) -> Collection[MIRInstruction]:
        ''''''
        dest = self.visit_address(tac.dest)
        src = self.visit_operand(tac.src)
        return (x86Mov(dest, src),)

    def visit_binary(self, tac: TACBinary) -> Collection[MIRInstruction]:
        ''''''
        dest = self.visit_address(tac.dest)
        lhs = self.visit_operand(tac.lhs)
        rhs = self.visit_operand(tac.rhs)
        match tac.operator:
            case BinaryOperator.Add:
                return (
                    x86Mov(dest, lhs),
                    x86Add(dest, rhs),
                )
            case BinaryOperator.Sub:
                return (
                    x86Mov(dest, lhs),
                    x86Sub(dest, rhs),
                )
            case BinaryOperator.Mul:
                rax = PhysicalRegister.id_from(x86Register.RAX)
                temporary = self.next_register
                return (
                    x86Mov(rax, lhs),
                    x86Mov(temporary, rhs),
                    x86Mul(temporary),
                    x86Mov(dest, rax),
                )
            case _:
                raise NotImplementedError(f"Operator '{tac.operator}' not implemented in x86_64 instruction selector")
                assert_never(tac.operator)

    def visit_declare(self, tac: TACDeclare) -> Collection[MIRInstruction]:
        ''''''
        self.add_variable_register(tac.id)
        return tuple()

    # -Static Methods
    @staticmethod
    def run(tac: TACUnit, symbols: Sequence[Symbol]) -> MIRUnit:
        ''''''
        instructions: list[MIRInstruction] = []
        selector = x86_64InstructionSelector(symbols)
        for instruction in tac:
            block = selector.visit(instruction)
            instructions.extend(block)
        return MIRUnit(instructions)
