##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Printer: Nodes     ##
##-------------------------------##

## Imports
from collections.abc import Collection
from typing import TYPE_CHECKING, assert_never, cast
from ...unresolved import (
    UnresolvedNode,
    UnresolvedNodeVisitor,
    UnresolvedTypeNode,
    UnresolvedModifierNode,
    UnresolvedStructNode,
    UnresolvedEnumNode,
    UnresolvedVariableNode,
    UnresolvedBlockNode,
    UnresolvedFlowNode,
    UnresolvedAssignmentNode,
    UnresolvedBinaryNode,
    UnresolvedUnaryPrefixNode,
    UnresolvedUnaryPostfixNode,
)

if TYPE_CHECKING:
    from ...unresolved import (
        STRUCT_MEMBER_TYPES,
        ENUM_ENTRY_TYPES,
        UnresolvedUnitNode,
        UnresolvedFunctionNode,
        UnresolvedConditionalNode,
        UnresolvedSwitchNode,
        UnresolvedWhileNode,
        UnresolvedDoNode,
        UnresolvedForNode,
        UnresolvedReturnNode,
        UnresolvedDeferNode,
        UnresolvedExprNode,
        UnresolvedGroupNode,
        UnresolvedAccessNode,
        UnresolvedObjectNode,
        UnresolvedArrayNode,
        UnresolvedLiteralNode,
        UnresolvedIdentifierNode,
        UnresolvedEmptyNode,
    )


## Classes
class UnresolvedNodePrinter(UnresolvedNodeVisitor[str]):
    """
    A diagnostic visitor that transforms an Unresolved AST into a human-readable string.

    This printer is designed for the 'Unresolved' phase of the Ember compiler, where
    identifiers are not yet bound and ambiguities are still present in the tree.
    """

    # -Constructor
    def __init__(self) -> None:
        self._indent: int = 0
    
    # -Instance Methods: Visitor
    def visit_unit(self, node: UnresolvedUnitNode) -> str:
        EMPTY = f"[Unit: {node.location.file} -- Empty]"
        if not node.nodes:
            return EMPTY
        nodes: list[str] = []
        for _node in node.nodes:
            if (_str := self.visit(_node)) != '':
                nodes.append(_str)
        if not nodes:
            return EMPTY
        return '\n'.join((f"[Unit: {node.location.file}]", *nodes))

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
        # -Modifier
        modifier: str
        match node.kind:
            case UnresolvedModifierNode.Kind.Const:
                modifier = "const"
            case UnresolvedModifierNode.Kind.Immut:
                modifier = "immut"
            case _:
                assert_never(node.kind)
        return f"({modifier} {self.visit(node.target)})"

    def visit_decl_struct(self, node: UnresolvedStructNode) -> str:
        # -Internal Functions
        def _visit_members(members: Collection[STRUCT_MEMBER_TYPES]) -> str:
            _members: list[str] = []
            for member in members:
                _member: str
                match member:
                    case UnresolvedStructNode.Field():
                        _member = _visit_field(member)
                    case UnresolvedStructNode():
                        _member = _visit_struct(member)
                _members.append(f"{self.get_indent()}Member: {_member}")
            return '\n'.join(_members)

        def _visit_field(field: UnresolvedStructNode.Field) -> str:
            output = f"{self.visit(field.type)} {field.name}"
            if field.has_initializer:
                output += f" = {self.visit(field.initializer)}"
            return output

        def _visit_struct(struct: UnresolvedStructNode) -> str:
            output = '(' + ("union" if struct.is_union else "struct") + ')'
            output += f" {struct.name}"
            self._indent += 1
            members = _visit_members(struct.members)
            self._indent -= 1
            return '\n'.join((output, members))
        # -Body
        output = f"{self.get_indent()}Struct Decl[Name={node.name}]"
        self._indent += 1
        members = _visit_members(node.members)
        self._indent -= 1
        return '\n'.join((output, members))

    def visit_decl_function(self, node: UnresolvedFunctionNode) -> str:
        output = [
            f"{self.get_indent()}Function Decl[Name={node.name},"
            f"Type={self.visit(node.return_type)}]"
        ]
        self._indent += 1
        # -Parameters
        if node.arity == 0:
            output.append("Params=None")
        else:
            for parameter in node.parameters:
                _parameter = f"{self.get_indent()}Param: {self.visit(parameter.type)} "
                _parameter += f"{parameter.name}"
                if parameter.has_initializer:
                    _parameter += f" = {self.visit(parameter.initializer)}"
                output.append(_parameter)
        # -Body
        self._indent -= 1
        output.append(self._get_corrected_block(node.body))
        return '\n'.join(output)

    def visit_decl_enum(self, node: UnresolvedEnumNode) -> str:
        # -Internal Functions
        def _visit_value(value: ENUM_ENTRY_TYPES) -> str:
            match value:
                case UnresolvedNode():
                    return f" = {self.visit(value)}"
                case _:
                    tags: list[str] = []
                    for tag in cast(Collection[UnresolvedEnumNode.Tag], value):
                        tags.append(f"{self.visit(tag.type)} {tag.name}")
                    return '{' + ','.join(tags) + '}'
        # -Body
        output = f"{self.get_indent()}Enum Decl[Name={node.name}, Type="
        output += self.visit(node.type) if node.has_type else "None"
        output += f", Tagged={node.is_tagged}]"
        self._indent += 1
        entries: list[str] = []
        for entry in node.entries:
            _entry = f"{self.get_indent()}Entry: {entry.name}"
            if entry.has_value:
                _entry += _visit_value(entry.value)
            entries.append(_entry)
        self._indent -= 1
        return '\n'.join((output, *entries))

    def visit_decl_variable(self, node: UnresolvedVariableNode) -> str:
        output = [
            f"{self.get_indent()}Variable Decl[Type={self.visit(node.type)}]"
        ]
        self._indent += 1
        for entry in node.entries:
            _entry = f"{self.get_indent()}Entry: {entry.name}"
            if entry.has_initializer:
                _entry += f" = {self.visit(entry.initializer)}"
            output.append(_entry)
        self._indent -= 1
        return '\n'.join(output)

    def visit_stmt_block(self, node: UnresolvedBlockNode) -> str:
        output = [f"{self.get_indent()}{{"]
        self._indent += 1
        for _node in node.nodes:
            if (_str := self.visit(_node)):
                output.append(_str)
        self._indent -= 1
        return '\n'.join((*output, f"{self.get_indent()}}}"))

    def visit_stmt_conditional(self, node: UnresolvedConditionalNode) -> str:
        output = [f"{self.get_indent()}if({self.visit(node.condition)})"]
        output.append(self._get_corrected_block(node.if_branch))
        if node.has_else_branch:
            output.extend((
                f"{self.get_indent()}else",
                self._get_corrected_block(node.else_branch),
            ))
        return '\n'.join(output)

    def visit_stmt_switch(self, node: UnresolvedSwitchNode) -> str:
        output = [f"{self.get_indent()}switch({self.visit(node.condition)})"]
        self._indent += 1
        # -Groups
        for i, group in enumerate(node.groups):
            output.append(f"{self.get_indent()}Group[{i}]")
            self._indent += 1
            for case in group.cases:
                _case = f"{self.get_indent()}Case "
                if case.has_name:
                    _case += f"'{case.name}' "
                _case += f"({self.visit(case.condition)}):"
                output.append(_case)
            output.append(self._get_corrected_block(group.body))
            self._indent -= 1
        # -Default
        if node.has_default:
            output.extend((
                f"{self.get_indent()}Default",
                self._get_corrected_block(node.default)
            ))
        self._indent -= 1
        return '\n'.join(output)

    def visit_stmt_while(self, node: UnresolvedWhileNode) -> str:
        return '\n'.join((
            f"{self.get_indent()}while({self.visit(node.condition)})",
            self._get_corrected_block(node.body)
        ))

    def visit_stmt_do(self, node: UnresolvedDoNode) -> str:
        return '\n'.join((
            f"{self.get_indent()}do-while({self.visit(node.condition)})",
            self._get_corrected_block(node.body)
        ))

    def visit_stmt_for(self, node: UnresolvedForNode) -> str:
        output: list[str] = []
        # -Initializer
        initializer: str = ''
        if node.has_initializer:
            match node.initializer:
                case UnresolvedVariableNode():
                    initializer = f"{self.visit(node.initializer.type)} "
                    entries: list[str] = []
                    for entry in node.initializer.entries:
                        _entry = f"{entry.name}"
                        if entry.has_initializer:
                            _entry += f" = {self.visit(entry.initializer)}"
                        entries.append(_entry)
                    initializer += ','.join(entries)
                case _:
                    initializer = self.visit(node.initializer)
        # -Condition
        condition = self.visit(node.condition)
        # -Increment
        increment: str = ''
        if node.has_increment:
            increment = self.visit(node.increment)
        output.extend((
            f"{self.get_indent()}for({initializer};{condition};{increment})",
            self._get_corrected_block(node.body)
        ))
        return '\n'.join(output)

    def visit_stmt_flow(self, node: UnresolvedFlowNode) -> str:
        match node.kind:
            case UnresolvedFlowNode.Kind.Break:
                return f"{self.get_indent()}break"
            case UnresolvedFlowNode.Kind.Continue:
                return f"{self.get_indent()}continue"

    def visit_stmt_return(self, node: UnresolvedReturnNode) -> str:
        output = f"{self.get_indent()}return"
        if node.has_expression:
            output += f" {self.visit(node.expression)}"
        return output

    def visit_stmt_defer(self, node: UnresolvedDeferNode) -> str:
        output = f"{self.get_indent()}defer"
        match node.node:
            case UnresolvedBlockNode():
                output += f"\n{self.visit(node.node)}"
            case _:
                output += f" {self.visit(node.node)}"
        return output

    def visit_stmt_expression(self, node: UnresolvedExprNode) -> str:
        if node.has_expression:
            return f"{self.get_indent()}{self.visit(node.expression)}"
        return ''

    def visit_expr_group(self, node: UnresolvedGroupNode) -> str:
        inner = self.visit(node.inner)
        if node.has_target:
            inner += f" -> [{self.visit(node.target)}]"
        return f"({inner})"

    def visit_expr_assignment(self, node: UnresolvedAssignmentNode) -> str:
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
        return f"({self.visit(node.l_value)} {operator} {self.visit(node.r_value)})"

    def visit_expr_binary(self, node: UnresolvedBinaryNode) -> str:
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
        return f"({self.visit(node.lhs)} {operator} {self.visit(node.rhs)})"

    def visit_expr_unary_prefix(self, node: UnresolvedUnaryPrefixNode) -> str:
        operand = self.visit(node.operand)
        operator: str
        match node.operator:
            # -Math
            case UnresolvedUnaryPrefixNode.Operator.NumericalNegate:
                operator = '-'
            case UnresolvedUnaryPrefixNode.Operator.LogicalNegate:
                operator = '!'
            case UnresolvedUnaryPrefixNode.Operator.BitwiseNegate:
                operator = '~'
            # -Memory
            case UnresolvedUnaryPrefixNode.Operator.Pointer:
                operator = '*'
            case UnresolvedUnaryPrefixNode.Operator.Slice:
                operator = "[]"
            case UnresolvedUnaryPrefixNode.Operator.SlicePointer:
                operator = "[*]"
            case UnresolvedUnaryPrefixNode.Operator.AddressOf:
                operator = '@'
            case UnresolvedUnaryPrefixNode.Operator.Dereference:
                return f"({operand}.*)"
        return f"({operator}{operand})"

    def visit_expr_unary_postfix(self, node: UnresolvedUnaryPostfixNode) -> str:
        head = self.visit(node.head)
        arguments = ','.join(
            self.visit(argument)
            for argument in node.arguments
        )
        match node.kind:
            case UnresolvedUnaryPostfixNode.Kind.Call:
                return f"{head}({arguments})"
            case UnresolvedUnaryPostfixNode.Kind.Subscript:
                return f"{head}[{arguments}]"
            case UnresolvedUnaryPostfixNode.Kind.Object:
                return f"{head}{{{arguments}}}"

    def visit_expr_access(self, node: UnresolvedAccessNode) -> str:
        return f"({self.visit(node.head)}.{node.name})"

    def visit_expr_object(self, node: UnresolvedObjectNode) -> str:
        fields = ','.join(
            f"{field.name}={self.visit(field.value)}"
            for field in node.fields
        )
        return f"{{ {fields} }}"

    def visit_expr_array(self, node: UnresolvedArrayNode) -> str:
        values = ','.join(
            self.visit(value)
            for value in node.values
        )
        return f"[ {values} ]"

    def visit_expr_literal(self, node: UnresolvedLiteralNode) -> str:
        return str(node.value)

    def visit_expr_identifier(self, node: UnresolvedIdentifierNode) -> str:
        return node.name

    def visit_expr_empty(self, node: UnresolvedEmptyNode) -> str:
        return ''

    # -Instance Methods: Helpers
    def get_indent(self) -> str:
        return ' ' * self._indent * 2

    def _get_corrected_block(self, node: UnresolvedNode) -> str:
        match node:
            case UnresolvedBlockNode():
                return self.visit(node)
            case _:
                self._indent += 1
                output = self.visit(node)
                self._indent -= 1
                return output

    # -Static Methods
    @staticmethod
    def run(node: UnresolvedNode) -> None:
        printer = UnresolvedNodePrinter()
        print(printer.visit(node))
