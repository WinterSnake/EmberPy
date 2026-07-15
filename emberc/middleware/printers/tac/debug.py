##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## TAC Printer: Debug            ##
##-------------------------------##


## Imports
from typing import TYPE_CHECKING
from ....ir import (
    TACVisitor,
    TACLiteral,
    TACTemporary,
    TACVariable,
)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from ...symbol_table import Symbol
    from ....ir import (
        TACUnit,
        TACAssign,
        TACBinary,
        TACDeclare,
        TACOperand,
    )


## Classes
class TACDebugPrinter(TACVisitor[str]):
    """
    A visitor implementation for generating structural information about TAC instructions.

    Provides a static `run` method to output the debug info starting from a tac unit.
    """

    # -Constructor
    def __init__(self, symbols: Sequence[Symbol]) -> None:
        self._symbols: Sequence[Symbol] = symbols

    # -Instance Methods: Visitor
    def visit_assignment(self, tac: TACAssign) -> str:
        l_value = self.get_operand(tac.dest)
        r_value = self.get_operand(tac.src)
        return f"{l_value} = {r_value};"

    def visit_binary(self, tac: TACBinary) -> str:
        lhs = self.get_operand(tac.lhs)
        rhs = self.get_operand(tac.rhs)
        dest = self.get_operand(tac.dest)
        return f"{dest} = {lhs} {str(tac.operator)} {rhs};"

    def visit_declare(self, tac: TACDeclare) -> str:
        return f"declare {self.get_symbol(tac.id)};"

    # -Instance Methods: Helpers
    def get_operand(self, operand: TACOperand) -> str:
        match operand:
            case TACLiteral():
                return str(operand.value)
            case TACTemporary():
                return f"r{operand.index}"
            case TACVariable():
                return self.get_symbol(operand.id)

    def get_symbol(self, _id: int) -> str:
        return self._symbols[_id].name

    # -Static Methods
    @staticmethod
    def run(tac: TACUnit, symbols: Sequence[Symbol]) -> None:
        printer = TACDebugPrinter(symbols)
        output: list[str] = []
        for instruction in tac:
            result = printer.visit(instruction)
            output.append(result)
        result = '\n'.join(output)
        print(result)

    # -Class Properties
    __slots__ = ("_symbols",)
