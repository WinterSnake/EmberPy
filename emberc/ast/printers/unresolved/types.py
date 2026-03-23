##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Printer: Types     ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING
from ...unresolved import (
    UnresolvedNodeVisitor,
    UnresolvedNullVisitorMixin,
    UnresolvedTypeNode,
    UnresolvedModifierNode,
    UnresolvedAssignmentNode,
    UnresolvedBinaryNode,
    UnresolvedUnaryPrefixNode,
    UnresolvedUnaryPostfixNode,
)

if TYPE_CHECKING:
    from ...unresolved import (
        UnresolvedNode,
        UnresolvedGroupNode,
        UnresolvedAccessNode,
        UnresolvedArrayNode,
        UnresolvedLiteralNode,
        UnresolvedIdentifierNode,
        UnresolvedEmptyNode,
    )


## Classes
class UnresolvedTypePrinter(
    UnresolvedNullVisitorMixin[str],
    UnresolvedNodeVisitor[str | None]
):
    """
    A diagnostic visitor that transforms an Unresolved Type Node into a human-readable string.
    """

    # -Constructor
    def __init__(self) -> None:
        self._indent: int = 0
    
    # -Instance Methods: Visitor
    def visit_type(self, node: UnresolvedTypeNode) -> str:
        match node.kind:
            case UnresolvedTypeNode.Kind.Void:
                return "void"
            case UnresolvedTypeNode.Kind.Boolean:
                return "bool"
            case UnresolvedTypeNode.Kind.Int8:
                return "int8"
            case UnresolvedTypeNode.Kind.Int16:
                return "int16"
            case UnresolvedTypeNode.Kind.Int32:
                return "int32"
            case UnresolvedTypeNode.Kind.Int64:
                return "int64"
            case UnresolvedTypeNode.Kind.UInt8:
                return "uint8"
            case UnresolvedTypeNode.Kind.UInt16:
                return "uint16"
            case UnresolvedTypeNode.Kind.UInt32:
                return "uint32"
            case UnresolvedTypeNode.Kind.UInt64:
                return "uint64"
            case UnresolvedTypeNode.Kind.SSize:
                return "ssize"
            case UnresolvedTypeNode.Kind.USize:
                return "usize"
            case UnresolvedTypeNode.Kind.Function:
                return "fn"

    def visit_modifier(self, node: UnresolvedModifierNode) -> str:
        target = self.visit(node.target)
        assert target is not None, f"Invalid type node: {node.target}"
        match node.kind:
            case UnresolvedModifierNode.Kind.Const:
                return f"const {target}"

    def visit_expr_group(self, node: UnresolvedGroupNode) -> str:
        inner = self.visit(node.inner)
        assert inner is not None, f"Invalid type node: {node.inner}"
        assert not node.has_target, f"Invalid type node: {node}"
        return inner

    def visit_expr_assignment(self, node: UnresolvedAssignmentNode) -> str:
        l_value = self.visit(node.l_value)
        r_value = self.visit(node.r_value)
        assert l_value is not None, f"Invalid type node: {node.l_value}"
        assert r_value is not None, f"Invalid type node: {node.r_value}"
        operator: str
        match node.operator:
            case UnresolvedAssignmentNode.Operator.Eq:
                operator = '='
            case UnresolvedAssignmentNode.Operator.AddEq:
                operator = "+="
            case UnresolvedAssignmentNode.Operator.SubEq:
                operator = "-="
            case UnresolvedAssignmentNode.Operator.MulEq:
                operator = "*="
            case UnresolvedAssignmentNode.Operator.DivEq:
                operator = "/="
            case UnresolvedAssignmentNode.Operator.ModEq:
                operator = "%="
            case UnresolvedAssignmentNode.Operator.BitXorEq:
                operator = "^="
            case UnresolvedAssignmentNode.Operator.BitAndEq:
                operator = "&="
            case UnresolvedAssignmentNode.Operator.BitOrEq:
                operator = "|="
            case UnresolvedAssignmentNode.Operator.ShiftLEq:
                operator = "<<="
            case UnresolvedAssignmentNode.Operator.ShiftREq:
                operator = ">>="
        return f"({l_value} {operator} {r_value})"

    def visit_expr_binary(self, node: UnresolvedBinaryNode) -> str:
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        assert lhs is not None, f"Invalid type node: {node.lhs}"
        assert rhs is not None, f"Invalid type node: {node.rhs}"
        operator: str
        match node.operator:
            case UnresolvedBinaryNode.Operator.Range:
                operator = ".."
            # -Math
            case UnresolvedBinaryNode.Operator.Add:
                operator = "+"
            case UnresolvedBinaryNode.Operator.Sub:
                operator = "-"
            case UnresolvedBinaryNode.Operator.Mul:
                operator = "*"
            case UnresolvedBinaryNode.Operator.Div:
                operator = "/"
            case UnresolvedBinaryNode.Operator.Mod:
                operator = "%"
            # -Bitwise
            case UnresolvedBinaryNode.Operator.BitXor:
                operator = "^"
            case UnresolvedBinaryNode.Operator.BitAnd:
                operator = "&"
            case UnresolvedBinaryNode.Operator.BitOr:
                operator = "|"
            case UnresolvedBinaryNode.Operator.ShiftL:
                operator = "<<"
            case UnresolvedBinaryNode.Operator.ShiftR:
                operator = ">>"
            # -Comparisons
            case UnresolvedBinaryNode.Operator.LogOr:
                operator = "or"
            case UnresolvedBinaryNode.Operator.LogAnd:
                operator = "and"
            case UnresolvedBinaryNode.Operator.Eq:
                operator = "=="
            case UnresolvedBinaryNode.Operator.NtEq:
                operator = "!="
            case UnresolvedBinaryNode.Operator.Lt:
                operator = "<"
            case UnresolvedBinaryNode.Operator.Gt:
                operator = ">"
            case UnresolvedBinaryNode.Operator.LtEq:
                operator = "<="
            case UnresolvedBinaryNode.Operator.GtEq:
                operator = ">="
        return f"({lhs} {operator} {rhs})"

    def visit_expr_unary_prefix(self, node: UnresolvedUnaryPrefixNode) -> str:
        # -Operand
        self._indent += 1
        operand = self.visit(node.operand)
        assert operand is not None, f"Invalid type node: {node.operand}"
        self._indent -= 1
        # -Operator
        operator: str
        match node.operator:
            # -Math
            case UnresolvedUnaryPrefixNode.Operator.NumericalNegate:
                return f"(-{operand})"
            case UnresolvedUnaryPrefixNode.Operator.LogicalNegate:
                return f"(!{operand})"
            case UnresolvedUnaryPrefixNode.Operator.BitwiseNegate:
                return f"(~{operand})"
            # -Memory
            case UnresolvedUnaryPrefixNode.Operator.Pointer:
                operator = f"`*` pointer to"
            case UnresolvedUnaryPrefixNode.Operator.Slice:
                operator = f"`[]` slice of"
            case UnresolvedUnaryPrefixNode.Operator.SlicePointer:
                operator = f"`[*]` pointer of"
            case _:
                assert False, f"Tried parsing non-type '{node}' node in UnresolvedTypePrinter"
        return f"{operator}\n{self.get_indent(1)}{operand}"

    def visit_expr_unary_postfix(self, node: UnresolvedUnaryPostfixNode) -> str:
        # -Head
        self._indent += 1
        head = self.visit(node.head)
        assert head is not None, f"Invalid type node: {node.head}"
        head = f"{self.get_indent()}{head}"
        self._indent -= 1
        # -Arguments
        self._indent += 1
        arguments: list[str] = []
        for argument in node.arguments:
            arg = self.visit(argument)
            assert arg is not None, f"Invalid type node: {argument}"
            arguments.append(f"{self.get_indent()}{arg}")
        self._indent -= 1
        # -Operator
        operator: str
        match node.kind:
            case UnresolvedUnaryPostfixNode.Kind.Subscript:
                operator = "array of [\n"
                operator += ",\n".join(arguments)
                operator += f"\n{self.get_indent()}]"
            case _:
                assert False, f"Tried parsing non-type '{node}' node in UnresolvedTypePrinter"
        return f"{operator}\n{head}"

    def visit_expr_access(self, node: UnresolvedAccessNode) -> str:
        return f"({self.visit(node.head)}.{node.name})"

    def visit_expr_array(self, node: UnresolvedArrayNode) -> str:
        values: list[str] = []
        self._indent += 1
        for value in node.values:
            val = self.visit(value)
            assert val is not None, f"Invalid type node: {value}"
            values.append(f"{self.get_indent()}{val}")
        self._indent -= 1
        return "[\n" + ",\n".join(values) + f"\n{self.get_indent()}]"

    def visit_expr_literal(self, node: UnresolvedLiteralNode) -> str:
        return str(node.value)

    def visit_expr_identifier(self, node: UnresolvedIdentifierNode) -> str:
        return node.name

    def visit_expr_empty(self, node: UnresolvedEmptyNode) -> str:
        return "<inferred>"

    # -Instance Methods: Helpers
    def get_indent(self, temporary: int = 0) -> str:
        return ' ' * (self._indent + temporary) * 2

    # -Static Methods
    @staticmethod
    def run(node: UnresolvedNode) -> None:
        printer = UnresolvedTypePrinter()
        print(printer.visit(node))
