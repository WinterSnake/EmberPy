##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Printer: Debug     ##
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
class UnresolvedDebugPrinter(
    UnresolvedSequenceRouterMixin[str],
    UnresolvedLiteralRouterMixin[str],
):
    """
    Unresolved Debug Printer

    Prints a debug level branch and trace of each AST node.
    Handles nesting markers for connection inner branches to parent branches.
    """
    # -Constructor
    def __init__(self) -> None:
        self._depth = 0
        self._markers: set[int] = set()

    # -Instance Methods: Visitor
    # --Types--
    def visit_type(self, node: UnresolvedTypeNode) -> str:
        return str(node.kind)

    # --Declarations--
    def visit_unit(self, node: UnresolvedUnitNode) -> str:
        output = ["Unit"]
        if _output := super().visit_unit(node):
            output.append(_output)
        return '\n'.join(output)

    def visit_variable(self, node: UnresolvedVariableNode) -> str:
        output = ["Variable"]
        marker = self.push_tree_marker()
        self._depth += 1
        output.append(f"{self.branch_indent}type: {node.type.accept(self)}")
        for i, entry in enumerate(node):
            _indent: str
            if i == (len(node) - 1):
                _indent = self.cap_indent
                self.pop_tree_marker(marker)
            else:
                _indent = self.branch_indent
            output.append(f"{_indent}entry:{entry.name}")
            if entry.has_initializer:
                self._depth += 1
                _initializer = entry.initializer.accept(self)
                output.append(f"{self.cap_indent}initializer:{_initializer}")
                self._depth -= 1
        self.pop_tree_marker(marker)
        self._depth -= 1
        return '\n'.join(output)

    # --Statements--
    def visit_block(self, node: UnresolvedBlockNode) -> str:
        output = ["StmtBlock"]
        if _output := super().visit_block(node):
            output.append(_output)
        return '\n'.join(output)

    def visit_conditional(self, node: UnresolvedConditionalNode) -> str:
        output = ["StmtIf"]
        marker = self.push_tree_marker()
        self._depth += 1
        condition = node.condition.accept(self)
        output.append(f"{self.branch_indent}condition:{condition}")
        _indent: str
        if not node.has_else_branch:
            self.pop_tree_marker(marker)
            _indent = self.cap_indent
        else:
            _indent = self.branch_indent
        then_branch = node.then_branch.accept(self)
        output.append(f"{_indent}then:{then_branch}")
        if node.has_else_branch:
            self.pop_tree_marker(marker)
            else_branch = node.else_branch.accept(self)
            output.append(f"{self.cap_indent}else:{else_branch}")
        self._depth -= 1
        return '\n'.join(output)

    def visit_expression(self, node: UnresolvedExpressionNode) -> str:
        output = [
            f"Expression(Span=({node.location.start}, {node.location.end}))"
        ]
        self._depth += 1
        output.append(f"{self.cap_indent}{node.expression.accept(self)}")
        self._depth -= 1
        return '\n'.join(output)

    # --Expressions--
    def visit_group(self, node: UnresolvedGroupNode) -> str:
        output = [f"Group(Span=({node.location.start}, {node.location.end}))"]
        self._depth += 1
        output.append(f"{self.cap_indent}{node.inner.accept(self)}")
        self._depth -= 1
        return '\n'.join(output)

    def visit_assignment(self, node: UnresolvedAssignNode) -> str:
        span = node.wide_span
        output = [
            f"AssignExpr({node.operator}, Span=({span.start}, {span.end}))"
        ]
        marker = self.push_tree_marker()
        self._depth += 1
        output.append(f"{self.branch_indent}l_value:{node.l_value.accept(self)}")
        self.pop_tree_marker(marker)
        output.append(f"{self.cap_indent}r_value:{node.r_value.accept(self)}")
        self._depth -= 1
        return '\n'.join(output)

    def visit_binary(self, node: UnresolvedBinaryNode) -> str:
        span = node.wide_span
        output = [
            f"BinaryExpr({node.operator}, Span=({span.start}, {span.end}))"
        ]
        marker = self.push_tree_marker()
        self._depth += 1
        output.append(f"{self.branch_indent}lhs:{node.lhs.accept(self)}")
        self.pop_tree_marker(marker)
        output.append(f"{self.cap_indent}rhs:{node.rhs.accept(self)}")
        self._depth -= 1
        return '\n'.join(output)

    def visit_unary(self, node: UnresolvedUnaryPrefixNode) -> str:
        span = node.wide_span
        output = [
            f"UnaryExpr({node.operator}, Span=({span.start}, {span.end}))"
        ]
        self._depth += 1
        output.append(f"{self.cap_indent}{node.operand.accept(self)}")
        self._depth -= 1
        return '\n'.join(output)

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> str:
        return f"Identifier({node.name})"

    # --Extensions--
    def visit_sequence(self, node: UnresolvedSequenceNode) -> str:
        output: list[str] = []
        marker = self.push_tree_marker()
        self._depth += 1
        for i, _node in enumerate(node):
            _indent: str
            if i == len(node) - 1:
                _indent = self.cap_indent
                self.pop_tree_marker(marker)
            else:
                _indent = self.branch_indent
            _output = _node.accept(self)
            output.append(f"{_indent}{_output}")
        self._depth -= 1
        return '\n'.join(output)

    def visit_literal(self, node: UnresolvedLiteralNode) -> str:
        return f"Literal({node.value})"

    # -Instance Methods: Helpers
    def push_tree_marker(self) -> int:
        marker = self._depth + 1
        self._markers.add(marker)
        return marker

    def pop_tree_marker(self, value: int) -> None:
        if value not in self._markers:
            return
        self._markers.remove(value)

    def get_tree_indent(self) -> str:
        indent: list[str] = []
        for i in range(self._depth):
            _indent = '|' if i in self._markers else ' '
            indent.append(_indent)
        return ' '.join(indent)

    # -Static Methods
    @staticmethod
    def run(node: UnresolvedNode) -> None:
        printer = UnresolvedDebugPrinter()
        output = node.accept(printer)
        print(output)

    # -Properties
    @property
    def branch_indent(self) -> str:
        return f"{self.get_tree_indent()} |-"

    @property
    def cap_indent(self) -> str:
        return f"{self.get_tree_indent()} \\-"

    # -Class Properties
    __slots__ = ("_depth", "_markers")
