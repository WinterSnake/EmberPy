##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Printer: Format    ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING
from ....ast import (
    UnresolvedSequenceRouterMixin,
    UnresolvedLiteralRouterMixin,
)

if TYPE_CHECKING:
    from ....ast import (
        UnresolvedNode,
        UnresolvedSequenceNode,
        UnresolvedTypeNode,
        UnresolvedUnitNode,
        UnresolvedVariableNode,
        UnresolvedBlockNode,
        UnresolvedConditionalNode,
        UnresolvedExpressionNode,
        UnresolvedGroupNode,
        UnresolvedAssignNode,
        UnresolvedBinaryNode,
        UnresolvedUnaryPrefixNode,
        UnresolvedLiteralNode,
        UnresolvedIdentifierNode,
    )


## Classes
class UnresolvedFormatPrinter(
    UnresolvedSequenceRouterMixin[str],
    UnresolvedLiteralRouterMixin[str],
):
    """
    Unresolved Format Printer

    Prints a formatted trace of each AST node.
    Cleaner printer for higher level information
    """
    # -Constructor
    def __init__(self) -> None:
        self._depth = 0

    # -Instance Methods: Visitor
    # --Types--
    def visit_type(self, node: UnresolvedTypeNode) -> str:
        return str(node.kind)

    # --Declarations--
    def visit_unit(self, node: UnresolvedUnitNode) -> str:
        output = self.visit_sequence(node)
        return output if output else "Empty Unit"

    def visit_variable(self, node: UnresolvedVariableNode) -> str:
        output: list[str] = []
        _type = node.type.accept(self)
        for entry in node:
            _output = f"{entry.name}"
            if entry.has_initializer:
                _output += f" = {entry.initializer.accept(self)}"
            output.append(_output)
        _output = ", ".join(output)
        return f"{self.indent}{_type} [{_output}]"

    # --Statements--
    def visit_block(self, node: UnresolvedBlockNode) -> str:
        self._depth += 1
        output = self.visit_sequence(node)
        self._depth -= 1
        return output if output else f"{self.indent}{{ }}"

    def visit_conditional(self, node: UnresolvedConditionalNode) -> str:
        output = [f"{self.indent}if ({node.condition.accept(self)}) {{"]
        self._depth += 1
        output.append(node.then_branch.accept(self))
        if node.has_else_branch:
            output.append(' ' * (self._depth - 1) + "} else {")
            output.append(node.else_branch.accept(self))
        self._depth -= 1
        output.append(self.indent + '}')
        return '\n'.join(output)

    def visit_expression(self, node: UnresolvedExpressionNode) -> str:
        return f"{self.indent}{node.expression.accept(self)}"

    # --Expressions--
    def visit_group(self, node: UnresolvedGroupNode) -> str:
        return f"({node.inner.accept(self)})"

    def visit_assignment(self, node: UnresolvedAssignNode) -> str:
        l_value = node.l_value.accept(self)
        r_value = node.r_value.accept(self)
        return f"({l_value} {node.operator} {r_value})"

    def visit_binary(self, node: UnresolvedBinaryNode) -> str:
        lhs = node.lhs.accept(self)
        rhs = node.rhs.accept(self)
        return f"({lhs} {node.operator} {rhs})"

    def visit_unary(self, node: UnresolvedUnaryPrefixNode) -> str:
        return f"{node.operator}{node.operand.accept(self)}"

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> str:
        return node.name

    # --Extensions--
    def visit_sequence(self, node: UnresolvedSequenceNode) -> str:
        output: list[str] = []
        for _node in node:
            _output = _node.accept(self)
            output.append(_output)
        return '\n'.join(output)

    def visit_literal(self, node: UnresolvedLiteralNode) -> str:
        return str(node.value)

    # -Static Methods
    @staticmethod
    def run(node: UnresolvedNode) -> None:
        printer = UnresolvedFormatPrinter()
        output = node.accept(printer)
        print(output)

    # -Properties
    @property
    def indent(self) -> str:
        return ' ' * self._depth

    # -Class Properties
    __slots__ = ("_depth",)
